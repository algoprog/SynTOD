import json
import random
import argparse
intents_list = [
    # Recipe Related
    'search_recipe', 'suggest_recipe', 'more_results', 'select', 'show_ingredients',

    # Task Management
    'begin', 'next_step', 'goto_step', 'finish',
    
    # Question-Answering
    'open_domain_qa', 'in_task_qa', 
    
    # Miscellaneous
    'chitchat', 'set_timer'
]
intents = ', '.join(intents_list)

LLM_PROMPT = f"Conversation between human and AI that helps with recipes, allowed user intents are; {intents}:"
USER_PREFIX = " ### HUMAN: "
SYSTEM_PREFIX = " ### ASSISTANT: "
SUGGESTIONS_PREFIX = " ### SUGGESTIONS: "
RESULTS_PREFIX = " ### RESULTS: "
RECIPE_PREFIX = " ### RECIPE: "
SEPARATOR = " ## "
HISTORY_SIZE = -1

def get_metadata(utterance):
    metadata = {"intent": utterance['intent']} if 'intent' in utterance else {}
    if 'selection' in utterance:
        metadata['selection'] = utterance['selection']
    if 'query' in utterance:
        metadata['query'] = utterance['query']
    if 'recipe_name' in utterance:
        metadata['query'] = utterance['recipe_name']
    metadata = json.dumps(metadata)
    return metadata

def recipe_run(args):
    random.seed(args.seed)
    o_train = open(args.output_file, 'w+')
    data = []
    # max_len = 0

    recipes = {}
    with open(args.seed_file) as f:
        for line in f:
            d = json.loads(line.rstrip('\n'))
            recipes[d['id']] = d

    conversations = []
    with open(args.conversation_file) as f:
        for line in f:
            d = json.loads(line.rstrip('\n'))
            conversations.append(d)

    random.shuffle(conversations)

    for d in conversations:
        recipe = recipes[d['id']]
        history = []
        current_step = 'not started'
        recipe_info = ''
        skip_next = False
        add_next = 0

        for i, utterance in enumerate(d['conversation']):
            if skip_next:
                skip_next = False
                continue
            if  'intent' in utterance and  utterance['intent'] in [
                "deny",
                "financial_advice",
                "legal_advice",
                "medical_advice",
                "offense",
                "repeat",
                "subjective_qa",
                "suicide_attempt",
                "personal_information",
                "dangerous_task"
            ]:
                skip_next = True
                continue

            metadata = ''
            utterance['text'] = utterance['text'].strip()

            if 'intent' in utterance and utterance['intent'] == 'option_selected':
                steps_str = ', '.join([f"'{i+1}: {s['text']}'" for i, s in enumerate(recipe['steps'])])
                ingredients = [item['ingredient'] for item in recipe['ingredients']]
                info = f"title: {recipe['title']}, description: {recipe['description']}, ingredients: [{', '.join(ingredients)}], steps: [{steps_str}]"
                recipe_info = f"{RECIPE_PREFIX}{info}"
                history.append(recipe_info)

            if 'step' in utterance:
                current_step = utterance['step']

            prefix = SYSTEM_PREFIX if utterance['role'] == 'system' else USER_PREFIX
            
            results_info = ''
            if 'intent' in utterance and utterance['intent'] in ['show_results', 'show_suggestions']:
                if utterance['intent'] == 'show_suggestions':
                    suggestions_str = '\n'.join(utterance['suggestions'])
                    results_info += f"{SUGGESTIONS_PREFIX}{suggestions_str}"
                metadata = json.dumps({"selected_ids": utterance['recipe_ids']})
                results_info += f"{RESULTS_PREFIX}{utterance['results_str']}"
            
            if i+1 < len(d['conversation']) and 'intent' in d['conversation'][i+1] and d['conversation'][i+1]['intent'] == 'select':
                metadata_str = f"{SEPARATOR}{metadata}" if metadata != '' else ''
                next_metadata = get_metadata(d['conversation'][i+1])
                history.append(f"{results_info}{prefix}{utterance['text']}{metadata_str}{USER_PREFIX}{d['conversation'][i+1]['text']}{SEPARATOR}{next_metadata}")
                skip_next = True
            else:
                history.append(f"{results_info}{prefix}{utterance['text']}")

            if utterance['role'] == 'user':
                metadata = get_metadata(utterance)
            
            if metadata != '':
                history[-1] += f"{SEPARATOR}{metadata}"
        
        text = ''.join(history)
        example = f"{LLM_PROMPT}{text}"
        data.append(example)
        # max_len = max(max_len, len(example.split()))

    for i, d in enumerate(data):
        o_train.write(json.dumps({"text": d}) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file", default="train_nograph_v8.jsonl")
    parser.add_argument("--seed", default=43)
    parser.add_argument("--seed_file", default="data/corpus.jsonl")
    parser.add_argument("--conversation_file", default="/project/pi_hzamani_umass_edu/chris/convtod/data/recipe_nograph_2.jsonl")
    args = parser.parse_args()
    recipe_run(args)
    
