import json

from constants import *
from openai import OpenAI
import time


gpt_4_turbo = 'gpt-4-1106-preview'#'gpt-4-turbo'
gpt_4 = 'gpt-4'

gpt_client = OpenAI(
    # This is the default and can be omitted
    api_key=openai_key,
)


def write_dict_to_jsonl(dictionary, filename):
    with open(filename, 'a') as jsonl_file:
        # Iterate over the dictionary and write each entry as a separate line in the JSON Lines file
        
        json_line = json.dumps(dictionary)
        jsonl_file.write(json_line)
        jsonl_file.write("\n")

def create_aux_products_map() :
    aux_cart_map = {}
    aux_compare_map = {}
    # prdt_map = {}
    data_file = 'data/ecom_conversations_test_100_llama.jsonl'
    with open(data_file, 'r') as file:
        for line in file:
            econv_conversation = json.loads(line)
            
            prdt_id = econv_conversation['id']
            aux_cart = econv_conversation['aux_cart']
            aux_compare = econv_conversation['aux_compare']
            aux_cart_map[prdt_id] = aux_cart
            aux_compare_map[prdt_id] = aux_compare
    return aux_cart_map, aux_compare_map


def create_products_map() :
    prdt_map = {}
    data_file = 'data/complete_conversation_mistral.jsonl'
    with open(data_file, 'r') as file:
        for line in file:
            econv_conversation = json.loads(line)
            
            prdt_id = econv_conversation['id']
            prdt_map[prdt_id] = econv_conversation
    
    data_file = 'data/complete_conversation_mistral_entire.jsonl'
    with open(data_file, 'r') as file:
        for line in file:
            econv_conversation = json.loads(line)
            
            prdt_id = econv_conversation['id']
            prdt_map[prdt_id] = econv_conversation
    
    test_sets = []
    for id_p in prdt_map.keys() :
        test_sets.append(prdt_map[id_p])

    re_data_file = 'data/ecom_complete_conversations_mistral_test_set.jsonl'

    for t_sample in test_sets :
        write_dict_to_jsonl(t_sample, re_data_file)
    
            
    return 



def get_correct_product(prdt_id, aux_cart) :

    prdt = None

    for prd in aux_cart :
        if prd["id"] == prdt_id :
            prdt = prd
            break

    return prdt


def get_correct_product(path, path_pos, aux_compare,compare_i, aux_cart, cart_i ) :
        path_i = path_pos
        while path_i < len(path) and path[path_i] not in [intents.add_for_compare, intents.add_to_cart] :
            path_i +=1
        prdt = aux_cart[cart_i]
        if path_i < len(path) and path[path_i] == intents.add_for_compare :
            prdt = aux_compare[compare_i]
        return prdt


def trigger_prompt_again(utterance, conversation):

    # if utterance['intent'] == intents.search_product:
    #     prdt = self.get_correct_product(utterance['path'], path_i, aux_compare,compare_i, aux_cart, cart_i )
    #     prompt = SEARCH_PRODUCT_PROMPT['prompt'].format(self.product_to_string(prdt))
    #     json_format = SEARCH_PRODUCT_PROMPT['json_format']
    #     other_product = prdt
    #     temperature = 0.5
    #     maximum_token_length = 256
    #     # model = gpt_4
    # elif utterance['intent'] == intents.suggest_product:
    #     prdt = self.get_correct_product(utterance['path'], path_i, aux_compare,compare_i, aux_cart, cart_i )
    #     product_info = self.product_to_string(prdt)
    #     prompt = SUGGEST_PRODUCT_PROMPT['prompt'].format(product_info)
    #     json_format = SUGGEST_PRODUCT_PROMPT['json_format']
    #     other_product = prdt
    #     # model = gpt_4
    #     temperature = 0.5
    #     maximum_token_length = 256
        
        

    return 

def update_fields(dictionary):
    # Prompt the user to choose which fields to update
    print("Current dictionary:")
    print(dictionary)
    fields_to_update = input("Enter the fields you want to update (comma-separated): ").split(',')
    
    # Update the selected fields
    for field in fields_to_update:
        if field.strip() in dictionary:
            new_value = input(f"Enter new value for '{field.strip()}': ")
            dictionary[field.strip()] = new_value
        else:
            print(f"Field '{field.strip()}' not found in the dictionary.")
    
    return dictionary


def chatgpt_api(prompt, model=gpt_4_turbo, temperature=0.5, max_retries=64, max_tokens = 2000):

    for i in range(max_retries):
        try:
            response = gpt_client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=40,
                messages=[{'role': 'user', 'content': prompt}]
            )
            # write_gpt_resp(prompt,response)
            used_tokens = response.usage.total_tokens
            return response.choices[0].message.content.strip(), used_tokens
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in {2} seconds...")
            time.sleep(2)
    return None, 0

# test_set_file = 'data/complete_conversations_llama_test_100.jsonl'

# test_set_file = 'data/complete_conversation_mistral.jsonl'

# test_set_file = 'data/complete_conversations_llama_test_100_corrected.jsonl'
# test_set_file = 'data/ecom_conversations_test_llama_short_desc_entire.jsonl'
test_set_file = 'data/ecom_conversations_test_mistral7b_short_desc_completed_entire.jsonl'





prompt_for_attribute_list_correction = {
"PROMPT" : """
Text  : {}

Derive list of attributes from the text and should be like [{{color:c}},{{brand: b}}], keep at max 4 most relevant attributes, every text may not have these attributes mentioned, in that case use a blank list []

return response strictly in the following format
{{"attributes_list":[...]}}
""" , 
"json_format" : None
}

'''
1. open file
2. get an entire conversation
3. check in the utterance if attribute_list is there and 
4. if it's not in the required format trigger gpt-4 with it and get attribute list in correct format
5. write the results in another file again.
'''
# re_write_file = 'data/complete_conversations_llama_test_entire.jsonl'
# re_write_file = 'data/ecom_conversations_test_llama_short_desc_completed_entire.jsonl'
re_write_file = 'data/ecom_conversations_test_mistral7b_short_desc_completed_entire_2.jsonl'
count = 0
total = 0

# ignore_ids = set()
# with open(re_write_file, 'r') as file:
#     for line in file :
#         econv_conversation = json.loads(line)
#         ignore_ids.add(econv_conversation['id'])
count_less_text = 0
intent_map = {}
with open(test_set_file, 'r') as file:
    for line in file:
        econv_conversation = json.loads(line)
        # if econv_conversation['id'] in ignore_ids :
        #     continue
        conversation = econv_conversation['conversation']
        conversation_modified = []
        prdt_id = econv_conversation['id']
        for utterance in conversation :
            total +=1
            # if 'text' in utterance.keys() and len(utterance['text']) < 20 :
            #     te = utterance['text']
            #     count_less_text += 1
            #     if utterance['intent'] in intent_map.keys() :
            #         intent_map[utterance['intent']] += 1
            #     else :
            #         intent_map[utterance['intent']] = 1
            #     # new_utter = trigger_prompt_again(utterance, conversation)
            #     utterance = update_fields(utterance)

            if 'attributes_list' in utterance.keys() :
                total += 1
                attri_list =utterance['attributes_list']
                attri_list_new = []
                # if len(attri_list) == 0 :
                #     count += 1
                if len(utterance['text']) < 20 :
                    te = utterance['text']
                    count_less_text += 1
                    # utterance = update_fields(utterance)

                if type(attri_list) == type({}) :
                    for key in attri_list.keys() :
                        attri_list_new.append({key:attri_list[key]})
                    utterance['attributes_list'] = attri_list_new
                
                elif len(attri_list) > 0 :
                    

                    attr = attri_list[0]
                    
                    if type(attr) == type("String") :
                        prmpt = prompt_for_attribute_list_correction['PROMPT'].format(utterance['text'])
                        # trigger gpt turbo
                        response = chatgpt_api(prmpt, max_retries=1, max_tokens=512)
                        # # get attr_list
                        try :
                            resp = json.loads(response[0])
                        except :
                            resp = {'attributes_list' : []}
                        attri_list_new = resp['attributes_list']
                        utterance['attributes_list'] = attri_list_new
                        count += 1
            conversation_modified.append(utterance)
        econv_conversation['conversation'] = conversation_modified
        write_dict_to_jsonl(econv_conversation, re_write_file)
        


print(count_less_text)
print(count)
print(total)
print(intent_map)

''''

Handle following intents:
{'search_product': 6, 'add_to_cart': 1, 'suggest_product': 1, 'acknowledge': 2}
{'buy_cart': 2, 'search_product': 17, 'suggest_product': 12, 'shown_cart': 1, 'add_to_cart': 5}

'''


# create_products_map()