import json
from constants import *



valid_product_catalog =  inventory_file_4k #"./data/valid_product_catalog.jsonl"

product_catalog = "./data/product_catalog_v0.jsonl"

def read_jsonl( file_path):
    with open(file_path, 'r') as file:
        for l in file :
           entry = json.loads(l)
           yield entry


# create a map for the review and metadata combined file
def get_catalog_stats(catalog) :
    product_stat = {}

    for entry in read_jsonl(catalog) :
        cat = entry['category']
        if cat in product_stat :
            product_stat[cat] +=1
        else :
            product_stat[cat] = 1

    return product_stat

valid_stat = get_catalog_stats(valid_product_catalog)
stat = get_catalog_stats(product_catalog)

print(f"valid_stat : {valid_stat}")
# print(f"prdt stat: {stat}")

