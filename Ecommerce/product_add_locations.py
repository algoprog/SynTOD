import concurrent
import json
import math
import random
import time
import threading

import hashlib

from concurrent.futures import ThreadPoolExecutor
from tqdm.auto import tqdm
from ecom_path_generation import TaskPathGenerator
from ecom_path_skeleton import UniversalPaths, AltTaskPathGenerator


from ecom_prompts import *
from ecom_retriever import Retriever
from constants import *
# from gpt4_free import GPT4_Free_API
import matplotlib.pyplot as plt


lock = threading.Lock()
gpt_resp_lock = threading.Lock()
# inventory_file = "data/final_product_catalog_v0.jsonl"
pos_lock = threading.Lock()

# gpt4 = GPT4_Free_API()

gpt_4_turbo = 'gpt-4-1106-preview'#'gpt-4-turbo'
gpt_4 = 'gpt-4'

def write_error(error):
    with lock:
        with open('errors.jsonl', 'a') as file:
            file.write(json.dumps({"error": error}) + "\n")
            file.flush()
def write_gpt_resp(prompt,response):
    with gpt_resp_lock:
        with open('gpt_responses.jsonl', 'a') as file:
            file.write(json.dumps({"prompt" :prompt, "response": response}) + "\n")
            file.flush()
def write_gpt_resp_None(prompt,response):
    with gpt_resp_lock:
        with open('gpt_responses_None.jsonl', 'a') as file:
            file.write(json.dumps({"prompt" :prompt, "response": response}) + "\n")
            file.flush()

def md5_hash(string):
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()


def format_product( d):
    product = d.copy()
    if 'rank' in product.keys() :
        del product['rank']
    if 'also_view' in product.keys() :
        del product['also_view']
    if 'date' in product.keys() :
        del product['date']
    if 'imageURL' in product.keys() :
        del product['imageURL']
    if 'imageURLHighRes' in product.keys() :
        del product['imageURLHighRes']
    if 'meta_category' in product.keys() :
        del product['meta_category']
    if 'paragraphs' in product.keys() :
        del product['paragraphs']
    


    return product 

def add_locations( d) :
    l = random.randint(0, len(locations)-1)
    d['location'] = locations[:l]
    return d

def add_ids(older_files, added_ids) :
    
    for file in older_files :
        with open(file,'r') as f:
            for line in f:
                d = json.loads(line.rstrip('\n'))
                added_ids.add(d['id'])


    return added_ids

def generate_locations():
    added_ids = set()
    # older_files = ['data/conversations_final_r_2.jsonl']
    
    # added_ids = add_ids(older_files, added_ids)
    products = []
    with open(inventory_file, 'r') as file:
        for line in file:
            d = json.loads(line)
            d = add_locations(d)
            if d['id'] not in added_ids:
                prdt = format_product(d)
                products.append(prdt)
    
    with open(inventory_with_locations_file, 'w') as file :
        for product in products :
            json.dump(product, file)
            file.write('\n')
    
# def get_inventory_stats():
    
#     desc_length = {}

#     with open(combined_inventory_file, 'r') as file:
#         for line in file:
#             d = json.loads(line)
#             if len(d['description']) >=0 :
#                 if len(d['description'])  not in desc_length :
#                     desc_length[len(d['description'])] = 0
#                 desc_length[len(d['description'])] += 1
    
#     return desc_length

def get_inventory_stats(variable = 'category' , inv_file = combined_inventory_file):
    
    variable_stats = {}

    with open(inv_file, 'r') as file:
        for line in file:
            d = json.loads(line)
            if d[variable] not in variable_stats :
                variable_stats[d[variable]]  = 0
            variable_stats[d[variable]] += 1
    
    return variable_stats



def remove_items(list, item): 
  
    # using list comprehension to perform the task 
    res = [i for i in list if i != item] 
    return res 

def create_right_extra_products():
    
    products = []
    with open(inventory_with_locations_file, 'r') as file:
        for line in file:
            d = json.loads(line)
            if 'description' in d :
                list = d['description']
                list = remove_items(list, "")
                desc_str = " ".join(list)

                d['description'] = [desc_str]
                if len(d['description']) == 1 :
                    products.append(d)
            
    
    with open(inventory_file_original_with_description, 'w') as file :
        for product in products :
            json.dump(product, file)
            file.write('\n')

def create_combined_inventory():
    
    products = []
    with open(inventory_file_original_with_description, 'r') as file:
        for line in file:
            d = json.loads(line)
            if 'description' in d and len(d['description']) == 1 :
                products.append(d)
    with open(inventory_file_extra, 'r') as file:
        for line in file:
            d = json.loads(line)
            if 'description' in d and len(d['description']) == 1 :
                products.append(d)
            
    
    with open(combined_inventory_file, 'w') as file :
        for product in products :
            json.dump(product, file)
            file.write('\n')

def create_4k_inventory():
    
    # stats = get_inventory_stats()
    # # print(stats)

    # # check how many are there above some threshold and their total
    # combined_total = 0
    # total = 0
    # threshold = 60
    # unique_categories = set()
    # for category in stats :
    #     combined_total += stats[category]
    #     if stats[category] > threshold :
    #         total += stats[category]
    #         unique_categories.add(category)
    
    append_categories = ['Bird Food', 'Golf Bags','Door Mats','Toy Playsets']
    products = []
    with open(combined_inventory_file, 'r') as file:
        for line in file:
            d = json.loads(line)
            if d['category'] in append_categories : #unique_categories :
                products.append(d)

    
   
    
    # print(total)
    # print(combined_total)
    # print(len(unique_categories))
    # print(len(products))
    
    
            
    
    with open(inventory_file_4k, 'a') as file :
        for product in products :
            json.dump(product, file)
            file.write('\n')


def create_test_train_inventory():
    
    stats = get_inventory_stats()
    # print(stats)

    # check how many are there above some threshold and their total
    unique_categories = set()
    for category in stats :
        unique_categories.add(category)
    
    products_train = []
    products_test = []
    products = {}
    
    with open(inventory_file_4k, 'r') as file:
        for line in file:
            d = json.loads(line)
            if d['category'] in products :
                products[d['category']].append(d)
            else :
                products[d['category']] = [d]

    # sample out approximately 4 from each category

    for category in products:
        # print(f'Category: {category}, Count: {len(list)}')

        # get around 2 from each valid category
        # if category in consider_cat :
        list = products[category]
        random_samples = random.sample(list, min(6, len(list)))
        products_test += random_samples
        for sample in random_samples :
            list.remove(sample)
        products_train += list
    
    with open(inventory_file_train, 'w') as file :
        for product in products_train :
            json.dump(product, file)
            file.write('\n')
    
    with open(inventory_file_test, 'w') as file :
        for product in products_test :
            json.dump(product, file)
            file.write('\n')

def build_histogram(inv_file = inventory_file) :

    data = get_inventory_stats(inv_file=inv_file)

    keys = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(15, 8))  # Adjust the figure size as needed
    plt.bar(keys, values)
    plt.xlabel('Categories')
    plt.ylabel('Frequency')
    plt.title(f'Histogram {inv_file.split(".")[0]}')

    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
    plt.tight_layout()

    plt.show()   
    plt.savefig(f"{inv_file.split('.')[0]}.png")     

def print_diff_in_data(data, data4k):
    cat_data = data.keys()
    cat_4k = data4k.keys()

    intersection_keys = set(cat_data) & set(cat_4k)

    print("Intersection of categories:", intersection_keys)

def get_rel_stats() :
    # build_histogram(inv_file=inventory_file_original_with_description)
    build_histogram(inv_file=inventory_file_4k)

    # data = get_inventory_stats(inv_file=inventory_file_original_with_description)

    # data4k = get_inventory_stats(inv_file=inventory_file_4k)

    # print_diff_in_data(data, data4k)

def create_test_100_inventory() :

    stats = get_inventory_stats()
    # print(stats)

    # check how many are there above some threshold and their total
    unique_categories = set()
    for category in stats :
        unique_categories.add(category)
    
    products_train = []
    products_test = []
    products = {}
    
    with open(inventory_file_test, 'r') as file:
        for line in file:
            d = json.loads(line)
            if d['category'] in products :
                products[d['category']].append(d)
            else :
                products[d['category']] = [d]

    # sample out approximately 2 from each category

    for category in products:
        # print(f'Category: {category}, Count: {len(list)}')

        # get around 2 from each valid category
        # if category in consider_cat :
        list = products[category]
        random_samples = random.sample(list, min(2, len(list)))
        products_test += random_samples
        for sample in random_samples :
            list.remove(sample)
        products_train += list
    
    
    with open(inventory_100_file_test, 'w') as file :
        for product in products_test :
            json.dump(product, file)
            file.write('\n')




if __name__ == '__main__':
    

    # create_right_extra_products()
    get_rel_stats()
    # create_combined_inventory()
    # create_4k_inventory()
    # create_test_train_inventory()
    # create_test_100_inventory()



    # 0.26 3
    # 0.37 3
    '''
    20 :  {'gpt-4-1106-preview': 216121, 'gpt-4': 31256}
            Estimated cost: $1.84
    9 :  Estimated cost: $0.90
    31 :  {'gpt-4-1106-preview': 322693, 'gpt-4': 38345}
            Estimated cost: $2.37
    40 :  {'gpt-4-1106-preview': 436949, 'gpt-4': 55665}
            Estimated cost: $3.38
Total = 2.74 + 2.37 + 3.38  = 8.49
    '''
