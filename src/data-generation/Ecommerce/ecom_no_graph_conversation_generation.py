'''
Script to generate conversations using a single prompt
'''

import json

import concurrent

from openai import OpenAI
from tqdm import tqdm
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor

# use proper apis
GOOGLE_API_KEY = 'AIzaSyCqwA72HpU3wAASrwvhXUssTYahoBoON6o'
MISTRAL_KEY = '69Bm2dEEn10ZDK5EKQtgiiEtB8FF2UGN'
LLAMA_KEY = 'gAbxAVfNYXdFSQxFbR4W4xRJOCVz6UU0'

openai_key = "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"



gpt_client = OpenAI(
    # This is the default and can be omitted
    api_key=openai_key,
)

pos_lock =  threading.Lock()

lock =  threading.Lock()
 
gpt_4_turbo = 'gpt-4-1106-preview'#'gpt-4-turbo'
# gpt_4 = 'gpt-4'

def chatgpt_api(prompt, model=gpt_4_turbo, temperature=0.7, max_retries=64, max_tokens = 2000):

    for i in range(max_retries):
        try:
            response = gpt_client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=120,
                messages=[{'role': 'user', 'content': prompt}]
            )
            # write_gpt_resp(prompt,response)
            used_tokens = response.usage.total_tokens
            return response.choices[0].message.content.strip(), used_tokens
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in {2} seconds...")
            time.sleep(2)
    return None, 0

def save_to_jsonl(data, filename="data/responses_nograph_ecom_3.jsonl"):
    with open(filename, "a") as file:
        file.write(json.dumps(data) + "\n")
        file.flush()


def json_loads(text, used_tokens2 = 0):
    try:
        return json.loads(text), used_tokens2
    except:
        print("Error")
        prompt = "fix the json below, expected format is {{\"role\":\"system\", \"text\": <text>}} or {{\"role\":\"user\", \"text\": <text>, ...}}, give only the correct json in your response nothing else:\n{}".format(text)
        response, used_tokens = chatgpt_api(prompt, model=gpt_4_turbo, max_retries=7)
        return json.loads(response), used_tokens


def get_attributes( attributes) :
    attri = {}
    for key in attributes :
        val = attributes[key][0]
        attri[key] = val


    return attri


def truncate_to( trstr, max_length = 200) :
    return " ".join(trstr.split(" ")[:max_length])

def attri_to_string( attributes):
    attri = get_attributes(attributes)
    
    return attri

def features_to_string(features) :
    final_str = '['

    for feat in features :
        t = f"{feat}, "
        final_str += t
    final_str = truncate_to(final_str, max_length=200)

    if final_str[-2:] == ", " :
        final_str = final_str[:-2]

    final_str += ']'

    return final_str
def details_to_string( details) :
    final_str = f'[{details}]'
    return final_str


def product_to_string(product, short = False, shortest = False, append = ["rating"]):
    
    f_S = ""
    if short :
        f_S += f"product_title: {product['title']}"
        try :
            if 'description' in product.keys() :
                f_S += f", description: {truncate_to(product['description'][0], max_length=200)}"
            else :
                try :

                    if 'feature' in product.keys() :
                        feat = features_to_string(product['feature'])
                        if feat!= '' :
                            f_S += f", features: {feat}\n"
                    
                except : 
                    print(f"no feature and description found for product {product['title']} ")
        except :
            
            if 'feature' in product.keys() :
                feat = features_to_string(product['feature'])
                if feat!= '' :
                    f_S += f", features: {feat}\n"
        
        if 'attributes' in product.keys() :
            attr = attri_to_string(product['attributes'])
            if attr!= '' :
                f_S += f", attributes: {attr}\n"
        
    if shortest :
        f_S += f"product_title: {product['title']}"

        if 'description' in product.keys() and len(product['description']) >0 :
            f_S += f", description: {truncate_to(product['description'][0], max_length=200)}"
        
    if short or shortest :
        if "overall" in product and "rating" in append:
            f_S += f", user rating: {product['overall']}"
        return f_S
    

    des = ''
    if 'description' in product.keys() and len(product['description']) > 0:
            des = f", description:  {truncate_to(product['description'][0], max_length=200)}"
    f_S = f"title: {product['title']}{des}, user rating: {product['overall']}, reviewCount: ({product['reviewCount']}), attributes: {attri_to_string(product['attributes'])}, available_location: {product['location']}"

    return f_S


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
locations = [ "United States", "United Kingdom", "South Africa", "Australia", "India", "Thailand", "Greece", "Bangladesh", "China", "Canada", "Mexico", "France", "Germany", "Japan", "South Korea"]

def add_locations( d) :
    l = random.randint(0, len(locations)-1)
    d['location'] = locations[:l]
    return d

def get_random_products( products, product, x = 1) :
    '''
    randomly sample around x products 
    '''
    aux_cart = [product]

    for i in range(0, x+1) :
        found = False
        while(not found) :
            l = random.randint(0, len(products)-1) 
            prd = products[l]
            if prd not in aux_cart :
                aux_cart.append(prd)
                found = True

    return aux_cart[1:]

def get_random_similar_products( products, product, y = 1) :
    
    '''
    randomly sample around y similar products 
    similar product means check same category as product told by mave dataset
    '''
    aux_compare = [product]

    for i in range(0, y+1) :
        found = False
        inwhile = 0
        while(not found) :
            l = random.randint(0, len(products)-1) 
            inwhile += 1
            prd = products[l]
            if inwhile > 1000 or prd not in aux_compare  and prd['category'] == product['category']:
                aux_compare.append(prd)
                found = True
                inwhile = 0
    

    return aux_compare[1:]

def generate_conversation_nograph(prompt, product_id):
    response, used_tokens = chatgpt_api(prompt)
    response = response.replace("jsonl", "")
    response = response.replace("\n\n", "\n")
    items = response.split("\n")
    items_new = []
    gpt4_tokens_used = 0
    for item in items :
        if item != "" and len(item)>10 :
            js, used_tokens2 = json_loads(item, 0)
            items_new.append(js)
            gpt4_tokens_used += used_tokens2
    return {"id":product_id,"conversation": items_new, "prompt":prompt, "used_tokens" : used_tokens, "gpt4_tokens_used":gpt4_tokens_used}

def get_product_info(product) :
    # description/attributes will be limited to just 200 words max
    product_info = product_to_string(product)
    # steps_str = ', '.join([f"'{i+1}: {s}'" for i, s in enumerate(product['steps'])])
    # product_info = f"title: {product['title']}, description: {product['description']}, ingredients: [{', '.join(product['ingredients'])}], steps: [{steps_str}]"
        

    return product_info

def get_other_prdt_info_string(other_products) :
    prdts_info = "["

    for prdt in other_products :
        prdts_info += "\n"
        prdts_info += get_product_info(prdt)
        prdts_info += ","


    prdts_info = prdts_info[:-1]
    prdts_info += "\n]"
    return prdts_info

def generate_conversations_nograph(limit=100):
    products = []
    with open('data/4k_final_valid_product_catalog.jsonl', 'r') as file:
        for line in file:
            d = json.loads(line)
            products.append(d)
    all_products = products[:limit]
    products = products[1700:limit]
    


    # for product in tqdm(products):
        

    # with ThreadPoolExecutor(max_workers=1) as executor:
    #     futures = []
        
    for product in tqdm(products):
        product_info = get_product_info(product)
        aux_cart = get_random_products(all_products, product)
        aux_compare = get_random_similar_products(all_products, product)
        all_prdts = aux_cart + aux_compare
        other_products = get_other_prdt_info_string(all_prdts)
        
        prompt = """
                Simulate a conversation between human and AI (called as MarunaShopper) that helps with selling products in an inventory, allowed user intents are:
                'suggest_product' (user asks task bot to recommend some product based on need or ocassion, do not include the product's name), 
                'generic_product_query' (user asks for a vague product recommendation e.g I want a shirt),
                'user_clarifies' (user gives more details about the product, if the system asks for more clarification about the generic product search), 
                'search_product'(user searches a product with a proper name), 
                'open_domain_qa' (random question about a product), 
                'show_cart' (user asks to display current cart), 
                
                'more_results', 
                'show_results' (user asks to show result), 
                'add_to_cart', 
                'select_i' (user selects a product), 
                'delivery_check' (user asks if the product is deliverable in a certain location or not, location should be a country based on product information, sometimes you may ask to deliver product to some different location where system should reply that it can't deliver product there), 
                'product_qa'(user asks question regarding a product), 
                'add_for_compare', 
                'acknowledge', 
                'show_attributes',  
                'select_i_remove_from_cart' (user asks to remove a product from cart), 
                'chitchat', 
                'select_i_remove_from_compare' (user asks to remove a product from compare list), 
                'compare_products' (user asks to compare products in a compare list)
                'buy_cart'. 
                Each of these user utterances must be more than three words and choose the flow of utterances in a logical but random fashion.
                The conversation should start with introduction from the system, when user asks for searching a product or to suggest a product, the system provides 3 options for the user to choose. 
                User is going to finally buy following product : {} 
                You can use following products to form a cart list or compare list (no need to use all of them in conversation) : {} 
                For each of following user intents provide appropriate slot values as well:
                search_product provide text, product_name, query, attributes_list ([{{"attribute1":"value1"}}, ...])
                suggest_product provide text, query, attributes_list ([{{"attribute1":"value1"}}, ...])
                show_attributes provide text, title, product_id (corresponding displayed number in the conversation)
                product_qa provide question, title, product_id (corresponding displayed number in the conversation)
                open_domain_qa provide question, topic (keep question around type of product)
                add_to_cart provide text, title, product_id
                remove_from_cart provide text, title, product_id
                add_for_compare provide text, title, product_id
                remove_from_compare provide text, title, product_id
                user_clarifies provide text, query, attributes_list
                delivery_check provide text, address
                

                STRICTLY use following jsonl format and do not add any extra words:

                {{"role":"system", "text": <text>}}
                {{"role":"user", "text": <text>, "intent": ..., <corresponding slots>:...}}
                ...
                """
        final_prmpt = prompt.format(product_info, other_products)
        
        result = generate_conversation_nograph(final_prmpt, product['id'])
        save_to_jsonl(result)
        


def get_cost_till_now() :
    total_cost = 0.0
    gpt_4_tokens = 0
    gpt4_turbo_tokens = 0
    conversations = []
    with open('data/responses_nograph_ecom_3.jsonl', 'r') as file:
        for line in file:
            d = json.loads(line)
            conversations.append(d)
            # gpt_4_tokens += d['gpt4_tokens_used']
            gpt4_turbo_tokens += d['used_tokens']

    total_cost = ((0.01 + 0.03)/2.0*(gpt4_turbo_tokens+ gpt_4_tokens))/1000 
    print(f"total cost: {total_cost}")
    return total_cost

def add_product_seed_id_cost_till_now(limit = 2000) :

    products = []
    with open('../../../data/4k_final_valid_product_catalog.jsonl', 'r') as file:
        for line in file:
            d = json.loads(line)
            products.append(d)
    products = products[:limit]

    conversations = []
    with open('../../../data/responses_nograph_ecom_gpt4turbo.jsonl', 'r') as file: 
        for line in file:
            d = json.loads(line)             
            conversations.append(d)

    conversations_modified = []
    ids_mapped = 0
    ids_not_mapped = 0
    show_comparisons = 0
    compare_products = 0
    add_to_cart = 0
    for conv, prdt in zip(conversations, products) :
        # put proper product_id
        if "id" in conv.keys() :
            product_id = conv['id']
            if product_id == prdt['id']:
                ids_mapped += 1

        else :
            conv['id'] = prdt['id']
            ids_not_mapped += 1
        
        # change the intent show_comparison to compare_products
        updated_convs = []
        for utternace in conv['conversation'] :
            if utternace['role'] == 'user' and'intent' in utternace.keys() : #  355 and 340
                intent = utternace['intent']
                if intent == 'delivery_check' :
                    show_comparisons += 1
                    utternace['intent'] = "delivery_address" #"compare_products"
                # elif intent == 'compare_products' :
                #     compare_products += 1
                elif intent == 'select_i_add_to_cart' :
                    utternace['intent'] = 'add_to_cart'
                    add_to_cart += 1
            updated_convs.append(utternace)
        conv['conversation'] = updated_convs
        
        
        conversations_modified.append(conv)
            
    with open('data/ecom_responses_nograph_gpt4turbo.jsonl', 'w') as file:
        for conv in conversations_modified:
            d = json.dumps(conv)
            file.write(d)
            file.write("\n")

    
    return 

generate_conversations_nograph(limit=10)
get_cost_till_now()

