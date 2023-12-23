import json

def read_jsonl(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            json_obj = json.loads(line)
            data.append(json_obj)
    return data

def write_jsonl(file_path, entry):
    with open(file_path, 'a') as file:
        json.dump(entry, file)
        file.write('\n')

def get_product_attributes_as_dict(attributes_list) :
    attributes = {}

    if attributes_list!= None :
        for attr in attributes_list :
            key = attr['key']
            evidences = attr['evidences']
            values = []
            for evidence in evidences :
                if 'value' in evidence :
                    val = evidence['value']
                    values.append(val)
            attributes[key] = values



    return attributes

corrected_file = "./data/final_product_catalog_v0.jsonl"
filename = './data/product_catalog_v0.jsonl'

# corrected_file = "./data/final_valid_product_catalog.jsonl"
# filename = './data/valid_product_catalog.jsonl'


products = read_jsonl(filename)
attributes_stats = {}

for product in products :
    product['overall'] = round(product['overall'], 2)
    product['attributes'] = get_product_attributes_as_dict(product['attributes'])
    for attr in product['attributes']:
        if attr in attributes_stats :
            attributes_stats[attr] += 1
        else :
            attributes_stats[attr] = 1
    # write_jsonl(corrected_file, product)



print(attributes_stats)
print(len(attributes_stats))