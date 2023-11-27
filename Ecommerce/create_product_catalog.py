import json


mave_file = "./data/sampled_example_top_50_4200.jsonl"
combined_file = "./data/review_metadata_combined_file.jsonl"

product_catalog = "./data/product_catalog.jsonl"

def write_to_jsonl(entry, file_path):
    with open(file_path, 'a') as file:
        json.dump(entry, file)
        file.write('\n')

def read_jsonl( file_path):
    with open(file_path, 'r') as file:
        for l in file :
           entry = json.loads(l)
           yield entry


# create a map for the review and metadata combined file

product_join = {}

for entry in read_jsonl(combined_file) :
    entry_copy = entry.copy()
    entry_copy['meta_category'] = entry_copy['category']
    # del entry_copy['category']
    product_join[entry['asin']] = entry_copy

# read from mave file 
for mave_entry in read_jsonl(mave_file) :
    asin = mave_entry['id']
    if asin in product_join.keys() :
        prdt_cat = product_join[asin]
        prdt_cat.update(mave_entry)
        write_to_jsonl(prdt_cat, product_catalog)

