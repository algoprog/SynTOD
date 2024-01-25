import json
import random
from constants import *

inventory_file = inventory_file_4k # "data/product_catalog.jsonl"


def get_attributes(attributes) :
    attri = {}
    for key_evid in attributes :
        vals = key_evid['evidences']
        
        str = ''
        for val in vals :
            val2 = val['value']
            if val2 in str : # string matching
                str = val


        attri['key'] = str


    return attri

def attri_to_string( attributes):
    attri = get_attributes(attributes)
    final_Str = '['
    
    for key in attri.keys():
        t = f"({key} , {attri[key]}), "
        final_Str += t
    if final_Str[-2:] == ", " :
        final_Str = final_Str[:-2]
    
    final_Str += ']'
    if '[(key , )]' in final_Str :
        final_Str = ''
    return final_Str
    
def features_to_string( features) :
    final_str = '['

    for feat in features :
        t = f"{feat}, "
        final_str += t

    if final_str[-2:] == ", " :
        final_str = final_str[:-2]
    final_str += ']'

    return final_str
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

products = []
no_desc = 0
no_feat = 0
noattr = 0
total_products = 0
no_feat_desc = 0
with open(inventory_file, 'r') as file:
    for line in file:
        d = json.loads(line)
        # d = add_locations(d)
        product = format_product(d)
        f_S = product['title']
        try :
            if 'description' in product.keys() :
                f_S += f", description: {product['description'][0]}"
            else :
                no_desc +=1
                try :

                    if 'feature' in product.keys() :
                        feat = features_to_string(product['feature'])
                        if attr!= '' :
                            f_S += f", features: {feat}\n"
                    else:
                        no_feat_desc +=1
                except : 
                    no_feat_desc +=1
        except :
            no_desc +=1
            try :

                if 'feature' in product.keys() :
                    feat = features_to_string(product['feature'])
                    if attr!= '' :
                        f_S += f", features: {feat}\n"
                else:
                    no_feat_desc +=1
            except : 
                no_feat_desc +=1
        try :

            if 'attributes' in product.keys() :
                attr = attri_to_string(product['attributes'])
                if attr!= '' :
                    f_S += f", attributes: {attr}\n"
            else:
                noattr +1
        except : 
            noattr +=1
        
        try :

            if 'feature' in product.keys() :
                feat = features_to_string(product['feature'])
                if attr!= '' :
                    f_S += f", features: {feat}\n"
            else:
                no_feat +=1
        except : 
            no_feat +=1


        products.append(f_S)
        total_products +=1

print(f"total products : {total_products}")
print(f"missing desc in products : {no_desc}")
print(f"missing attr in products : {noattr}")
print(f"missing features in products : {no_feat}")
print(f"missing features and desc in products : {no_feat_desc}")



