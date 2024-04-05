import json
from collections import OrderedDict
import argparse
require_attr = {
    'suggest_product' : ['query', 'attributes_list'],
    'show_results' : ['results_str'], 
    'select_i': ['selection'],
    'add_to_cart' : ['product_ids'],
    'buy_cart': [],
    'more_results': [],
    'search_product': ['attributes_list', 'query', 'product_name'],
    'add_for_compare': ['product_ids'],
    'open_domain_qa': ['question','topic'],
    'show_cart' : [],
    'shown_cart': ['product_ids'], 
    'product_qa': ['question','product_ids'],
    'acknowledge': [],
    'select_i_remove_from_cart': ['product_ids'],
    'repeat' : [],
    'generic_product_query': [],
    'user_clarifies' : ['query','attributes_list'],
    'delivery_address': ['address'],
    'show_attributes': ['product_ids'],
    'chitchat' : [],
    'compare_products' : ['query','list_of_products'],
    'show_comparison': ['product_ids'],
    'select_i_remove_from_compare': ['product_ids']
}

additional_convert = {
    'select_i_remove_from_cart' : 'remove_from_cart',
    'select_i_remove_from_compare' : 'remove_from_comparison'
}

intent_list = [additional_convert[intent] if intent in additional_convert else intent for intent in require_attr.keys()]
LLM_PROMPT = "Conversation between human and AI that helps with shopping, allowed user intents are; {}: ".format(", ".join(intent_list))
USER_PREFIX = " ### HUMAN: "
SYSTEM_PREFIX = " ### ASSISTANT: "
SUGGESTIONS_PREFIX = " ### SUGGESTIONS: "
RESULTS_PREFIX = " ### RESULTS: "
RECIPE_PREFIX = " ### RECIPE: "
SEPARATOR = " ## "

def get_intent(message):
    if 'intent' in message:
        return message['intent']
    return None

def dialog_builder(messages):
    prompt = LLM_PROMPT
    for message in messages:
        if message["role"] == "user":

            prompt += USER_PREFIX
            prompt += f"{message['text']} " if 'text' in message else f"{message['question']} "

            attr = require_attr[message['intent']] if 'intent' in message else []
            content = OrderedDict()
            intent = message["intent"] 
            content["intent"] = additional_convert[intent] if intent in additional_convert else intent
            for k,v in message.items():
                if k in attr:
                    content[k] = v
            prompt += SEPARATOR + f"{json.dumps(content)}"

        elif message["role"] == "system":

            if get_intent(message) == 'show_results': 
                prompt += RESULTS_PREFIX + f"{message['results_str']}"
            
            prompt += SYSTEM_PREFIX + f"{message['text']} "

            if get_intent(message) != 'show_results' and message['intent'] in require_attr:
                attr = require_attr[message['intent']] + ['intent']
                content = OrderedDict()
                intent = message["intent"]
                content["intent"] = additional_convert[intent] if intent in additional_convert else intent
                for k,v in message.items():
                    if k in attr:
                        content[k] = v
                prompt += f" ## {json.dumps(content)}"
        else:
            raise ValueError(f"Invalid role: {message['role']}")

    return prompt

def ecommerce_run(args):
    writer = open(args.generate_file,"w")
    with open(args.data_path) as f:
        for row in f.readlines():
            obj = json.loads(row)
            prompt = dialog_builder(obj["conversation"])
            writer.write(json.dumps({"text" : prompt}) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default="/project/pi_hzamani_umass_edu/chris/convtod/E2E-TOD-ECOM/data/ecom_responses_nograph_gpt4turbo.jsonl")
    parser.add_argument("--generate_file", default="train_v2_nograph.jsonl")
    args = parser.parse_args()
    ecommerce_run(args)
    


