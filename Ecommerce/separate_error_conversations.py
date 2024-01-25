import json
from constants import *




def add_ids(older_files, added_ids) :
    
    for file in older_files :
        with open(file,'r') as f:
            for line in f:
                d = json.loads(line.rstrip('\n'))
                added_ids.add(d['id'])


    return added_ids


def separate_conversations() :
    conversations = []
    error_conversations = []

    remove_ids = set()
    remove_ids = add_ids(['data/incomplete_conversation_product_id.jsonl'], remove_ids) # incomplete_conversation_product_id # errors_product_id_2



    with open('data/ecom_conversations.jsonl', 'r') as file:
        for line in file:
            d = json.loads(line)
            if d['id'] in remove_ids :
                error_conversations.append(d)
            else :
                conversations.append(d)
            
    
    # with open("data/error_conversation.jsonl", 'w') as file :
    #     for product in error_conversations :
    #         json.dump(product, file)
    #         file.write('\n')
    
    with open("data/sep_ecom_conversation_2.jsonl", 'w') as file :
        for product in conversations :
            json.dump(product, file)
            file.write('\n')



def create_single_file() :

    products = []

    with open('data/complete_conversations_llama_4.jsonl', 'r') as file:
        for line in file:
            d = json.loads(line)
            products.append(d)

    # with open('data/complete_conversations_llama_2.jsonl', 'r') as file:
    #     for line in file:
    #         d = json.loads(line)
    #         products.append(d)    

    with open("data/complete_conversations_llama_test_100.jsonl", 'a') as file :
        for d in products :
            json.dump(d, file)
            file.write('\n')


def separate_incomplete_conversations():
    incomplete_conversations = []
    complete_conversations = []
    with open("data/ecom_conversations_test_100_llama_3.jsonl", 'r') as file :
        for line in file:
            d = json.loads(line)
            path_length = len(d['path'])
            conv_length = len(d['conversation'])
            if path_length == 31 and conv_length == 30 :
                complete_conversations.append(d)
            elif path_length != conv_length + 1 :
                incomplete_conversations.append(d)
            else :
                complete_conversations.append(d)
    
    with open("data/incomplete_conversation_llama.jsonl", 'w') as file :
        for d in incomplete_conversations :
            json.dump(d, file)
            file.write('\n')
    
    with open("data/complete_conversations_llama_4.jsonl", 'w') as file :
        for d in complete_conversations :
            json.dump(d, file)
            file.write('\n')

    with open("data/incomplete_conversation_product_id_llama.jsonl", 'w') as file :
        for d in incomplete_conversations :
            json.dump({"id":d['id']}, file)
            file.write('\n')


def separate_incomplete_recipe_conversations():
    incomplete_conversations = []
    complete_conversations = []
    with open("data/conversations_llama_recipe.jsonl", 'r') as file :
        for line in file:
            d = json.loads(line)
            path_length = len(d['path'])
            conv_length = len(d['conversation'])
            if path_length == 41 and conv_length == 40 :
                complete_conversations.append(d)
            elif path_length != conv_length + 1 :
                incomplete_conversations.append(d)
            else :
                complete_conversations.append(d)
    
    with open("data/incomplete_conversations_llama_recipe.jsonl", 'w') as file :
        for d in incomplete_conversations :
            json.dump(d, file)
            file.write('\n')
    
    with open("data/complete_conversations_llama_recipe.jsonl", 'w') as file :
        for d in complete_conversations :
            json.dump(d, file)
            file.write('\n')

    with open("data/incomplete_conversation_product_id_llama_recipe.jsonl", 'w') as file :
        for d in incomplete_conversations :
            json.dump({"id":d['id']}, file)
            file.write('\n')



separate_incomplete_recipe_conversations()

# create_single_file()

# separate_conversations()