import concurrent
import json
import math
import random
import time
import threading
import openai
import hashlib

from concurrent.futures import ThreadPoolExecutor
from tqdm.auto import tqdm
from ecom_path_generation import TaskPathGenerator
from ecom_path_skeleton import UniversalPaths, AltTaskPathGenerator

import google.generativeai as genai

GOOGLE_API_KEY = ''

from ecom_prompts import *
from ecom_retriever import Retriever
from constants import *
# from gpt4_free import GPT4_Free_API


lock = threading.Lock()
gpt_resp_lock = threading.Lock()

pos_lock = threading.Lock()

# gpt4 = GPT4_Free_API()

gpt_4_turbo = 'gpt-4-1106-preview'#'gpt-4-turbo'
gpt_4 = 'gpt-4'

model = genai.GenerativeModel('gemini-pro')

def write_error(error):
    with lock:
        with open('errors.jsonl', 'a') as file:
            file.write(json.dumps({"error": error}) + "\n")
            file.flush()
def write_error_product_id(product_id):
    with lock:
        with open('errors_product_id.jsonl', 'a') as file:
            file.write(json.dumps({"id": product_id}) + "\n")
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


def gemini_api(prompt, model='gemini_pro', temperature=0.5, max_retries=64, max_tokens = 2000) :
    for i in range(max_retries) :
        response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            candidate_count=1,
            # stop_sequences=['space'],
            max_output_tokens=max_tokens,
            temperature=temperature)
            )
        if response != None:
            return response.text, 0

    return None, 0

def llm_api(prompt, model=gpt_4_turbo, temperature=0.5, max_retries=64, max_tokens = 2000, api = useapi) :
    if api == "gemini" :
        model = 'gemini_pro'
        return gemini_api(prompt,model, temperature, max_retries, max_tokens)
    elif api == 'openai' :
        return chatgpt_api(prompt, model=model, temperature=temperature, max_retries=7,max_tokens = max_tokens)
    
    return None, 0
    



def chatgpt_api(prompt, model=gpt_4_turbo, temperature=0.5, max_retries=64, max_tokens = 2000):
    for i in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                request_timeout=40,
                messages=[{'role': 'user', 'content': prompt}]
            )
            write_gpt_resp(prompt,response)
            used_tokens = response["usage"]["total_tokens"]
            return response["choices"][0]["message"]["content"].strip(), used_tokens
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in {2} seconds...")
            time.sleep(2)
    return None, 0

# def chatgpt_api(prompt, model=gpt_4_turbo, temperature=0.0, max_retries=64):
#     for i in range(max_retries):
#         try:
#             response = gpt4.get_gpt_response(prompt, model)
            
#             # openai.ChatCompletion.create(
#             #     model=model,
#             #     max_tokens=2000,
#             #     temperature=temperature,
#             #     request_timeout=40,
#             #     messages=[{'role': 'user', 'content': prompt}]
#             # )
#             # used_tokens = response["usage"]["total_tokens"]
#             # return response["choices"][0]["message"]["content"].strip(), used_tokens
#             return response, 0
#         except Exception as e:
#             print(f"Error occurred: {e}. Retrying in {2} seconds...")
#             time.sleep(2)
#     return None, 0

def generate_conversation(task_name, api = 'gemini'): 
    prompt = f"""Simulate a conversation between a taskbot system and a user about {task_name}. 
- The taskbot helps users with selling products in an inventory. 
- First the system introduces itself, then the user asks for help about a product. 
- System provides 3 relevant options, user selects one, system responds to the choice and guides the user for buying that product. 
- Sometimes user asks product related or open-domain questions in between, or even chitchats. 
- In the end the user may thank the taskbot, taskbot asks if he has any other question, user might ask something related to the ask or open-domain and eventually the conversation ends. 

Use this format:

#system:...
#user:...,
..."""
    response, used_tokens = llm_api(prompt, api = useapi)
    return response, used_tokens


def generate_conversation_html(conversation):
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conversation</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row">
            <div class="col">
                <div class="card">
                    <div class="card-body">'''

    for i, text in enumerate(conversation):
        if i % 2 == 0:
            html += '''
                        <div class="alert alert-primary" role="alert">
                            <strong>System: </strong> {0}
                        </div>'''.format(text)
        else:
            html += '''
                        <div class="alert alert-secondary" role="alert">
                            <strong>User: </strong> {0}
                        </div>'''.format(text)

    html += '''
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.min.js"></script>
</body>
</html>
    '''
    return html


def write_conversation_to_file(conversation):
    with lock:
        with open('conversations.jsonl', 'a') as file:
            utterances = conversation.split('#')
            if utterances[0] == "":
                utterances.pop(0)
            utterances = [u.rstrip("\n").strip().replace("user: ", "").replace("system: ", "")
                          for u in utterances]
            file.write(json.dumps({"conversation": utterances}) + "\n")
            open("html/{}.html".format(md5_hash(" ".join(utterances))), "w+").write(
                generate_conversation_html(utterances)
            )


def extract_response(response, conversation, path, prompt):
    resp = None
    if "fix the json below, expected format is" in prompt :
        resp = prompt.split(", give only the correct json in your response nothing else:\n")[-1]
        resp = resp.replace("{\"text\":..., \"title\":..., \"product_id\" :... }","")
        


    return resp

def generate_conversation_and_write(task_name):
    conversation, used_tokens = generate_conversation(task_name)
    write_conversation_to_file(conversation)
    print(used_tokens)


class DataGenerator:
    def __init__(self) -> None:
        self.retriever = Retriever()

    def get_attributes(self, attributes) :
        attri = {}
        # for key_evid in attributes :
        #     vals = key_evid['evidences']
            
        #     str = ''
        #     for val in vals :
        #         val2 = val['value']
        #         if val2 in str : # string matching
        #             str = val


        #     attri['key'] = str
        for key in attributes :
            val = attributes[key][0]
            attri[key] = val


        return attri
    
    def attri_to_string(self, attributes):
        attri = self.get_attributes(attributes)
        # final_Str = '['
        
        # for key in attri.keys():
        #     t = f"({key} , {attri[key]}), "
        #     final_Str += t
        # if final_Str[-2:] == ", " :
        #     final_Str = final_Str[:-2]
        
        # final_Str += ']'
        # if '[(key , )]' in final_Str :
        #     final_Str = ''
        return attri
    
    def features_to_string(self, features) :
        final_str = '['

        for feat in features :
            t = f"{feat}, "
            final_str += t

        if final_str[-2:] == ", " :
            final_str = final_str[:-2]
        final_str += ']'

        return final_str
    def details_to_string(self, details) :
        final_str = f'[{details}]'

        # for detail in details.keys() :
        #     t = f"{detail}, "
        #     final_str += t

        # if final_str[-2:] == ", " :
        #     final_str = final_str[:-2]
        # final_str += ']'

        return final_str


    def product_to_string(self, product, short = False, shortest = False, append = []):
        # steps_str = ', '.join([f"'{i+1}: {s}'" for i, s in enumerate(task['steps'])])
        # f_S = f"product_id: {product['id']}, "
        f_S = ""
        if short :
            f_S += f"product_title: {product['title']}"
            try :
                if 'description' in product.keys() :
                    f_S += f", description: {product['description'][0]}"
                else :
                    try :

                        if 'feature' in product.keys() :
                            feat = self.features_to_string(product['feature'])
                            if feat!= '' :
                                f_S += f", features: {feat}\n"
                        
                    except : 
                        print(f"no feature and description found for product {product['title']} ")
            except :
                
                if 'feature' in product.keys() :
                    feat = self.features_to_string(product['feature'])
                    if feat!= '' :
                        f_S += f", features: {feat}\n"
            
            if 'attributes' in product.keys() :
                attr = self.attri_to_string(product['attributes'])
                if attr!= '' :
                    f_S += f", attributes: {attr}\n"
            
        if shortest :
            f_S += f"product_title: {product['title']}"

            if 'description' in product.keys() and len(product['description']) >0 :
                f_S += f", description: {product['description'][0]}"
            
        if short or shortest :
            if "overall" in product and "rating" in append:
                f_S += f", user rating: {product['overall']}"
            return f_S

        des = ''
        if 'description' in product.keys() and len(product['description']) > 0:
                des = f", description:  {product['description'][0]}"
        f_S = f"title: {product['title']}{des}, user rating: {product['overall']}, reviewCount: ({product['reviewCount']}), attributes: {self.attri_to_string(product['attributes'])}"

        return f_S
    
    def get_correct_product(self, path, path_pos, aux_compare,compare_i, aux_cart, cart_i ) :
        path_i = path_pos
        while path_i < len(path) and path[path_i] not in [intents.add_for_compare, intents.add_to_cart] :
            path_i +=1
        prdt = aux_cart[cart_i]
        if path_i < len(path) and path[path_i] == intents.add_for_compare :
            prdt = aux_compare[compare_i]
        return prdt
    
    def recognize_transition(self, path, path_pos, current_intent ) :
        transition = False
        lookout_intents = [intents.show_results, intents.show_comparison, intents.shown_cart]


        if path_pos -1 >=0 :
            # current_intent = path[path_pos -1]
            i = path_pos -2
            while( i >=0 and path[i] not in lookout_intents) :
                i -=1
            if path[path_pos -1] in [intents.show_comparison, intents.shown_attributes] and current_intent == intents.add_to_cart :
                transition = True
            elif path[path_pos -1] in [intents.shown_cart, intents.shown_attributes] and current_intent == intents.add_for_compare :
                transition = True
        
        if i > 0 and path[i] != intents.show_results and not transition:
            if path[i] == intents.show_comparison and current_intent == intents.add_to_cart :
                transition = True
            elif path[i] == intents.shown_cart and current_intent == intents.add_for_compare :
                transition = True
            

        return transition
    
    def exchange_elements(self, arr, idx1, idx2):
        cart2= arr
        if 0 <= idx1 < len(cart2) and 0 <= idx2 < len(cart2):
            cart2[idx1], cart2[idx2] = cart2[idx2], cart2[idx1]
        else:
            print("Indices out of range. Please provide valid indices.")
        return cart2
    
    def fix_json_string(self, json_string):
        corrected_string = json_string.replace("\\'", "'")
        return json.loads(corrected_string)


    def generate_response(self, intent, next_intent=None, prev_intent=None, args=None):
        
        total_used_tokens = {gpt_4_turbo: 0, gpt_4: 0}
        temperature = 1.0
        json_format = None
        model = gpt_4_turbo
        multi_output = False
        golden_result_position = args['golden_result_position']
        search_results = args['results']
        suggestions = None
        returned_intent = intent
        prompt = None
        compare_list = args['compare_list']
        cart = args['cart']
        other_product = args['other_product']
        path = args['path']
        path_pos = args["path_pos"]
        cart_i = args["cart_i"] 
        aux_cart = args["aux_cart"]
        compare_i = args["compare_i"]
        aux_compare = args["aux_compare"]
        path_i = path_pos + 1
        prdt = args['product']
        clarification_conversation = args['clarification_conversation']
        maximum_token_length = 2000

        if args['product'] != None :
            product_info = self.product_to_string(args['product'])


        

        if intent == intents.start:  
            prompt = START_PROMPT['prompt']
            #model = gpt_4
        elif intent == intents.search_product:
            prdt = self.get_correct_product(path, path_i, aux_compare,compare_i, aux_cart, cart_i )
            prompt = SEARCH_PRODUCT_PROMPT['prompt'].format(self.product_to_string(prdt))
            json_format = SEARCH_PRODUCT_PROMPT['json_format']
            other_product = prdt
            temperature = 0.5
            maximum_token_length = 256
            # model = gpt_4
        elif intent == intents.suggest_product:
            prdt = self.get_correct_product(path, path_i, aux_compare,compare_i, aux_cart, cart_i )
            product_info = self.product_to_string(prdt)
            prompt = SUGGEST_PRODUCT_PROMPT['prompt'].format(product_info)
            json_format = SUGGEST_PRODUCT_PROMPT['json_format']
            other_product = prdt
            # model = gpt_4
            temperature = 0.5
            maximum_token_length = 256
        
        elif intent == intents.show_results :
            model = gpt_4
            prdt = other_product
            clarification_conversation = None
            if prdt == None :
                prdt = self.get_correct_product(path, path_i, aux_compare,compare_i, aux_cart, cart_i )
            
            product_id = prdt['id']
            # retrieve 20 results, remove the current product id doc, and get the next 2-3 results
            results = self.retriever.search(args['query'], limit=20)

            #print("\nretriever results:", ', '.join([r[0]['title'] for r in results]))

            if next_intent == intents.select_i:
                results = [r[0] for r in results if r[0]['id'] != product_id][(args['page']-1)*2 : args['page']*2]
                # add the current recipe id doc to the results in random position k
                golden_result_position = random.randint(0, len(results))
                results.insert(golden_result_position, prdt)
                #print('results offsets:', (args['page']-1)*2, args['page']*2)
            else:
                results = [r[0] for r in results if r[0]['id'] != product_id][(args['page']-1)*3 : args['page']*3]
                #print('results offsets:', (args['page']-1)*3, args['page']*3)
            
            search_results = results
            if len(search_results) == 0:
                returned_intent = intents.no_results

            # format the results
            results = [f"id: {i+1}, {self.product_to_string(r, short = True)}" for i, r in enumerate(results)] # , overall: {r['overall']} ({r['vote']})
            results = '\n'.join(results)

            if prev_intent == intents.more_results :
                prompt_template = SHOW_MORE_RESULTS_PROMPT
            elif next_intent == intents.more_results :
                prompt_template = SHOW_RESULTS_BEFORE_MORE_RESULTS_PROMPT
            else:
                prompt_template = SHOW_RESULTS_PROMPT

            prompt = prompt_template['prompt'].format(args['query'], results)
            temperature = 0.5
            json_format = prompt_template['json_format']
        elif intent == intents.more_results :
            prompt = MORE_OPTIONS_PROMPT['prompt'].format(args['query'])
            json_format = MORE_OPTIONS_PROMPT['json_format']
            temperature = 0.8
            maximum_token_length = 256
        elif intent == intents.select_i:
            # model = gpt_4
            search_results = args['results']
            results = [f"id: {i+1}, {self.product_to_string(d, shortest=True, append =['rating'])}" for i, d in enumerate(args['results'])]
            results = '\n'.join(results)
            prompt = SELECT_I_PROMPT['prompt'].format(args['golden_result_position']+1, results, args['bot'])
            json_format = SELECT_I_PROMPT['json_format']
            multi_output = True
            temperature = 0.5
            maximum_token_length = 1024

        
        elif intent == intents.select_i_remove_from_compare:
            # model = gpt_4
            
            prdt = other_product
            product_info = self.product_to_string(prdt)
            prompt_list = [REMOVE_FROM_COMPARE_PROMPT, REMOVE_FROM_COMPARE_REFERENTIAL_PROMPT]
            z = random.randint(0, len(prompt_list)-1)
            temperature = 0.5
            maximum_token_length = 512
            prompt = prompt_list[z]['prompt'].format(product_info, args['bot'])
            json_format = prompt_list[z]['json_format']
            
        
        elif intent == intents.select_i_remove_from_cart:
            # model = gpt_4
            prdt = other_product
            product_info = self.product_to_string(prdt)
            prompt_list = [REMOVE_FROM_CART_PROMPT, REMOVE_FROM_CART_REFERENTIAL_PROMPT]
            z = random.randint(0, len(prompt_list)-1)
            temperature = 0.5
            maximum_token_length = 512
            prompt = prompt_list[z]['prompt'].format(product_info, args['bot'])
            json_format = prompt_list[z]['json_format']
            
        
        elif intent == intents.option_selected:
            search_results = args['results']
            # results = [f"id: {i+1}, {self.product_to_string(d, shortest=True, append =['rating'])}" for i, d in enumerate(args['results'])]
            # results = '\n'.join(results)
            
            prdt = other_product
            if prdt == None :
                prdt = self.get_correct_product(path, path_i, aux_compare,compare_i, aux_cart, cart_i )
            
            desc = ''
            if 'description' in prdt :
                desc = prdt['description']
            elif 'feature' in prdt :
                desc = prdt['feature']
            prompt = OPTION_SELECTED_PROMPT['prompt'].format(prdt['title'], desc)
            json_format = OPTION_SELECTED_PROMPT['json_format']
            temperature = 0.5
            maximum_token_length = 256
        
        elif intent == intents.shown_attributes :
            model = gpt_4
            prdt = other_product
            if prdt == None :
                prdt = self.get_correct_product(path, path_i, aux_compare,compare_i, aux_cart, cart_i )
            
            product_info = self.product_to_string(prdt)
            prompt = SHOWN_ATTRIBUTES_PROMPT['prompt'].format(product_info)
            json_format = SHOWN_ATTRIBUTES_PROMPT['json_format']
            temperature = 0.8

        elif intent == intents.show_attributes :
            model = gpt_4
            prdt = other_product
            if prdt == None :
                prdt = self.get_correct_product(path, path_i, aux_compare,compare_i, aux_cart, cart_i )
                
            product_info = self.product_to_string(prdt)
            prompt = SHOW_ATTRIBUTES_BEGIN_PROMPT['prompt'].format(product_info, args['last_shown_options_string'])
            json_format = SHOW_ATTRIBUTES_BEGIN_PROMPT['json_format']
            temperature = 0.5
            maximum_token_length = 256
            
        elif intent == intents.acknowledge:
            # model = gpt_4
            prdt = other_product
            if prdt == None :
                prdt = self.get_correct_product(path, path_i, aux_compare,compare_i, aux_cart, cart_i )
            
            prompt = ACKNOWLEDGE_PROMPT['prompt'].format(args['bot'])
            json_format = ACKNOWLEDGE_PROMPT['json_format']
            multi_output = True
            temperature = 0.3
            maximum_token_length = 256
        
        elif intent in [ intents.shown_cart, intents.show_comparison] :
            
            # prdt = other_product
            # if prdt == None :
            prdt = aux_cart[cart_i -1]
            if intent == intents.show_comparison:
                prdt = aux_compare[compare_i-1]
            other_product = prdt
            if intent == intents.show_comparison:
                ungrounded_suggestions = compare_list 
            elif intent == intents.shown_cart :
                ungrounded_suggestions = cart 
            
            if next_intent in [intents.select_i, intents.select_i_remove_from_cart, intents.select_i_remove_from_compare] :
                
                golden_result_position = random.randint(0, len(ungrounded_suggestions)-1)
                
                prdt_ind = ungrounded_suggestions.index(prdt)
                ungrounded_suggestions = self.exchange_elements(ungrounded_suggestions, prdt_ind, golden_result_position)
                other_product = prdt
                
            search_results = ungrounded_suggestions
            grounded_suggestions = [f"id: {j+1}, {self.product_to_string(d, shortest=True)}" for j, d in enumerate(ungrounded_suggestions)] # rating: {d['overall']} ({d['vote']}), 
            # need to handle grounded suggestions for compare and cart list !!!
            if prev_intent == intents.show_cart :
                prompt_template = SHOWN_CART_PROMPT
                
                
            elif prev_intent == intents.compare_products :
                prompt_template = SHOW_COMPARISON_PROMPT
                
            prompt = prompt_template['prompt'].format('\n'.join(grounded_suggestions))
            json_format = prompt_template['json_format']
            

        
        elif intent == intents.open_domain_qa:
            
            prompt = OPEN_DOMAIN_QA_PROMPT['prompt']
            json_format = OPEN_DOMAIN_QA_PROMPT['json_format']
        
        elif intent == intents.chitchat :
            prompt = CHITCHAT_PROMPT['prompt']
            json_format = CHITCHAT_PROMPT['json_format']
            # model = gpt_4
        
        
        elif intent == intents.subjective_qa :
            prompt = SUBJECTIVE_QA_PROMPT['prompt']
            json_format = SUBJECTIVE_QA_PROMPT['json_format']
            multi_output = True
            model = gpt_4
        
        elif intent == intents.user_start:
            prompt = START_PROMPT_USER['prompt']
            json_format = START_PROMPT_USER['json_format']
            multi_output = True
        
            #model = gpt_4
        
        elif intent == intents.repeat :
            prompt = REPEAT_PROMPT['prompt']
            json_format = REPEAT_PROMPT['json_format']
            multi_output = True
            # model = gpt_4
        elif intent == intents.deny :
            prompt = DENY_PROMPT['prompt'].format(args['bot'])
            json_format = DENY_PROMPT['json_format']
            # model = gpt_4
        elif intent == intents.stop :
            prompt = STOP_PROMPT['prompt']
            json_format = STOP_PROMPT['json_format']
            multi_output = True
            # model = gpt_4
        
        elif intents.system_response in intent: # string in a string
            prdt = other_product
            if prdt == None :
                prdt = self.get_correct_product(path, path_i, aux_compare,compare_i, aux_cart, cart_i )
            product_info = self.product_to_string(prdt)
            if prev_intent == intents.shown_attributes:
                attr = ''
                if 'attributes' in prdt :
                    attr = '\n'.join(prdt[attributes])
                elif 'description' in prdt :
                    attr = prdt['description']
                elif 'feature' in prdt :
                    attr = prdt['feature']
                prompt = SHOWN_ATTRIBUTES_PROMPT['prompt'].format(attr)
                
            elif prev_intent in [intents.open_domain_qa, intents.deny, intents.chitchat, intents.subjective_qa]:
                prompt = SYSTEM_PROMPT['prompt'].format(args['user'])
            elif prev_intent in [intents.add_for_compare, intents.add_to_cart]:
                prdt = other_product
                product_info = self.product_to_string(prdt)
            
                prompt = IN_CONVERSATION_SYSTEM_PROMPT['prompt'].format( product_info, args['user'])
            
            elif prev_intent == intents.repeat:
                prompt = SYSTEM_REPEAT_PROMPT['prompt'].format(args['bot'], args['user'])
            
            elif prev_intent == intents.product_qa :
                last_shown_options_string = args['last_shown_options_string']
                if last_shown_options_string == None :
                    last_shown_options_string = args['bot']

                prompt = SHOW_PRODUCT_PROMPT['prompt'].format( product_info, args['user'], last_shown_options_string)

            elif prev_intent in [intents.select_i_remove_from_compare, intents.select_i_remove_from_cart ] :
                prdt = other_product

                if prdt == None:
                    if prev_intent == intents.select_i_remove_from_compare :
                        prdt = aux_compare[compare_i]
                    else :
                        prdt = aux_cart[cart_i]
                product_info_oth = self.product_to_string(prdt)
                # compare_i -=1
                last_shown_options_string = args['last_shown_options_string']
                if last_shown_options_string == None :
                    last_shown_options_string = args['bot']
                prompt = IN_CONVERSATION_SYSTEM_PROMPT['prompt'].format(product_info_oth,args['user'])
                
                if prev_intent == intents.select_i_remove_from_compare and 'compare_list' in args.keys() :
                    compare_list = args['compare_list']
                    compare_list.remove(prdt)
                    other_product = prdt
            
            
                if prev_intent == intents.select_i_remove_from_cart and 'cart' in args.keys():
                    cart = args['cart']
                    cart.remove(prdt)
                    other_product = prdt


        
            
            else :
                prompt = IN_CONVERSATION_SYSTEM_PROMPT['prompt'].format( product_info, args['user'])
        
        elif intent == intents.show_cart : 
            prompt = SHOW_CART_PROMPT['prompt'].format(args['bot'])
            # json_format = SEARCH_PRODUCT_PROMPT['json_format']
            model = gpt_4
            temperature = 0.5
            maximum_token_length = 256
        
        elif intent == intents.buy_cart:
            prompt = BUY_CART_PROMPT['prompt'].format(args['bot'])
            temperature = 0.5
            maximum_token_length = 256
            
            # model = gpt_4
        # need to handle aux cart 
        elif intent == intents.add_to_cart:
            if other_product!=None and self.recognize_transition(path, path_pos, intent) : # and other_product != aux_cart[cart_i] 
                # this is to ensure if element from compare is added here if required
                if other_product in aux_cart :
                    cart_i = aux_cart.index(other_product)
                else :
                    aux_cart.insert(cart_i, other_product)
            
            prdt = aux_cart[cart_i]
            product_info_oth = self.product_to_string(prdt)
            if cart_i == 0:
                compare_i +=1
            cart_i +=1
            other_product = prdt
            last_shown_options_string = args['last_shown_options_string']
            if last_shown_options_string == None :
                last_shown_options_string = args['bot']

            
            if 'cart' in args.keys() :
                cart = args['cart']

            cart.append(prdt)
            
            prompt_list = [ADD_TO_CART_PROMPT, ADD_TO_CART_REFERENTIAL_PROMPT]
            z = random.randint(0, len(prompt_list)-1)
            temperature = 0.5
            maximum_token_length = 512
            prompt = prompt_list[z]['prompt'].format(product_info_oth,last_shown_options_string)
            json_format  = prompt_list[z]['json_format']
            # model = gpt_4
            
        # need to handle aux compare 
        elif intent == intents.add_for_compare:
            #### some major issue here
            if other_product!=None and  self.recognize_transition(path, path_pos, intent) : # other_product != aux_compare[compare_i] and
                # this is to ensure if element from cart is added here if required
                if other_product in aux_compare :
                    compare_i = aux_compare.index(other_product)
                else :
                    aux_compare.insert(compare_i, other_product)
            
            prdt = aux_compare[compare_i]
            product_info_oth = self.product_to_string(prdt)
            if compare_i == 0:
                cart_i +=1
            compare_i +=1
            other_product = prdt

            last_shown_options_string = args['last_shown_options_string']
            if last_shown_options_string == None :
                last_shown_options_string = args['bot']
            
            if 'compare_list' in args.keys():
                compare_list = args['compare_list']
            compare_list.append(prdt)
            
            prompt_list = [ADD_FOR_COMPARE_PROMPT, ADD_FOR_COMPARE_REFERENTIAL_PROMPT]
            z = random.randint(0, len(prompt_list)-1)
            temperature = 0.5
            maximum_token_length = 512
            
            prompt = prompt_list[z]['prompt'].format(product_info_oth,last_shown_options_string)
            json_format  = prompt_list[z]['json_format']
            
            # model = gpt_4
        
        elif intent == intents.generic_product_query:
            
            prdt = self.get_correct_product(path, path_i, aux_compare,compare_i, aux_cart, cart_i )
            product_info = self.product_to_string(prdt)
            prompt = USER_GENERIC_PRODUCT_PROMPT['prompt'].format(product_info,args['bot'])
            other_product = prdt
            # model = gpt_4

        elif intent == intents.product_qa:
            prdt = other_product
            if prdt == None :
                prdt = self.get_correct_product(path, path_i, aux_compare,compare_i, aux_cart, cart_i )
            last_shown_options_string = args['last_shown_options_string']
            if last_shown_options_string == None :
                last_shown_options_string = args['bot']

            product_info = self.product_to_string(prdt)
            prompt = PRODUCT_QA_PROMPT['prompt'].format(product_info, last_shown_options_string)
            json_format  = PRODUCT_QA_PROMPT['json_format']
            
            # model = gpt_4
        elif intent == intents.compare_products:
            
            delm = ', '
            prompt = COMPARE_PRODUCTS_PROMPT['prompt'].format(f"[{delm.join([ f'[{self.product_to_string(product)}]' for product in args['compare_list']])}]")
            
            model = gpt_4
        elif intent == intents.delivery_address:
            prdt = other_product
            if prdt == None :
                prdt = self.get_correct_product(path, path_i, aux_compare,compare_i, aux_cart, cart_i )
            product_info = self.product_to_string(prdt)
            
            loc = locations[random.randint(0, len(locations)-1)]
            prompt = CHECK_DELIVERY_AVAILABILITY_PROMPT['prompt'].format(product_info, loc , args['user'])
            json_format = CHECK_DELIVERY_AVAILABILITY_PROMPT['json_format']
            temperature = 0.2
            # model = gpt_4
        
        elif intent == intents.delivery_check :
            prdt = other_product
            if prdt == None :
                prdt = self.get_correct_product(path, path_i, aux_compare,compare_i, aux_cart, cart_i )
            product_info = self.product_to_string(prdt)
            locs = prdt['location']
            prompt = CHECK_DELIVERY_PROMPT['prompt'].format(args['delivery_address'], product_info , ", ".join(locs) )
            temperature = 0.2
            # model = gpt_4
        
        elif intent == intents.more_results :
            prompt = MORE_OPTIONS_PROMPT['prompt']
            json_format = MORE_OPTIONS_PROMPT['json_format']
        
        elif intent == intents.bought_cart :
            prompt = BOUGHT_CART_PROMPT['prompt']
        
        elif intent == intents.bought_cart :
            prompt = BOUGHT_CART_PROMPT['prompt']
        
        elif intent == intents.clarifying_questions :
            clarification_conversation = args['clarification_conversation']
            if clarification_conversation == None :
                clarification_conversation = f"User : {args['user']} "
            else :
                clarification_conversation = f"{clarification_conversation} \n User: {args['user']}"
            
            prompt = ASK_CLARIFICATION_PROMPT['prompt'].format(clarification_conversation)
        
        elif intent == intents.user_clarifies :
            # similar to suggest product prompt
            prdt = other_product
            if prdt == None :
                prdt = self.get_correct_product(path, path_i, aux_compare,compare_i, aux_cart, cart_i )
            product_info = self.product_to_string(prdt)
            clarification_conversation = args['clarification_conversation']
            if clarification_conversation == None :
                clarification_conversation = f"Bot : {args['bot']} "
            else :
                clarification_conversation = f"{clarification_conversation} \n Bot : {args['bot']}"
            prompt =  USER_CLARIFIES_AFTER_CLARIFICATION_PROMPT['prompt'].format(product_info, clarification_conversation)
            json_format = USER_CLARIFIES_AFTER_CLARIFICATION_PROMPT['json_format']
            other_product = prdt
            

        
        model = gpt_4_turbo
        
        #print(f"\n*** prompt ***\n{prompt}\n***\n")

        if prompt is None:
            write_error(f'ERROR: {intent}')

        response, used_tokens = llm_api(prompt, model=model, temperature=temperature, max_retries=7,max_tokens = maximum_token_length, api = useapi)
        total_used_tokens[model] += used_tokens
        if response is None:
            write_error(f'ERROR: {prompt}')
            return None, total_used_tokens, None, prompt

        if json_format:
            try:
                response = json.loads(response)
            except:
                # try :
                #     response = self.fix_json_string(response)
                # except :
                prompt = "fix the json below, expected format is {}, give only the correct json in your response nothing else:\n{}".format(json_format, response)
                response, used_tokens = llm_api(prompt, model=gpt_4, max_retries=7, api = useapi) # gpt_4 # gpt_4_turbo
                total_used_tokens[gpt_4] += used_tokens
                # total_used_tokens[gpt_4] += 1
                if response is None:
                    write_error(f'ERROR: {prompt}')
                    return None, total_used_tokens, None, prompt
                try:
                    response = json.loads(response)
                except:
                    write_error(f'ERROR: {prompt}')
                    response = None
        elif multi_output:
            options = []
            # if intent == intents.show_attributes :
            #     contents = response.split("\n")
            #     options = [json.loads(content) for content in contents if 'text' in content]

                
            if len(options)==0 :
                options = response.split('\n')
                options = [r for r in options if r != '']
            
            response = random.choice(options)
        
        last_shown_options_string = args['last_shown_options_string']
        if intent in [intents.option_selected, intents.select_i_remove_from_cart, intents.select_i_remove_from_compare]:
            search_results = args['results']
            results = [f"id: {i+1}, {self.product_to_string(d, shortest=True, append =['rating'])}" for i, d in enumerate(args['results'])]
            results = '\n'.join(results)
            text = response
            last_shown_options_string = f' text : {text} , relevant results : \n {results}'
            
        
        state = {'search_results': search_results,
                 'golden_result_position': golden_result_position,
                 'intent': returned_intent,
                 'cart' : cart,
                 'compare_list' : compare_list,
                 'suggestions': suggestions,
                 'model': model, 
                 'other_product': other_product,
                 'cart_i' :cart_i,
                 'compare_i' : compare_i,
                 'aux_compare' : aux_compare,
                 'aux_cart' : aux_cart,
                 'last_shown_options_string' : last_shown_options_string,
                 'clarification_conversation' : clarification_conversation
                 }
        
        return response, total_used_tokens, state, prompt
    
    def get_path_stats(self, path) :
        total_add_to_cart = 0
        total_add_for_compare = 0
        l = 0
        for intent in path :
            if intent == intents.add_for_compare :
                total_add_for_compare +=1
                l = 0
            elif intent == intents.add_to_cart :
                total_add_to_cart +=1
                l = 0
            else :
                l+=1
        if l > 0 :
            total_add_to_cart +=1


        return total_add_to_cart, total_add_for_compare
    
    def get_random_products(self, products, product, x = 1) :
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

        return aux_cart
    
    def get_random_similar_products(self, products, product, y = 1) :
        
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
        

        return aux_compare
    
    

    def generate_conversation(self, product, products ,max_length=30): #  pos ,
        
        skeleton = AltTaskPathGenerator()
    
        path_generator = TaskPathGenerator(graph = skeleton.graph)
        path = path_generator.generate_path(max_length=max_length)
        
        path_length = len(path)
        total_add_to_cart, total_add_for_compare = self.get_path_stats(path)

        aux_cart = self.get_random_products(products, product, total_add_to_cart)
        cart_i = 0
        aux_compare = self.get_random_similar_products(products, product, total_add_for_compare)
        compare_i = 0


        conversation = []
        prev_intent = None
        total_used_tokens = {gpt_4_turbo: 0, gpt_4: 0}

        results_page = 1
        
        search_results = []
        query = None
        golden_result_position = None
        prev_bot_response = ''
        prev_user_response = ''
        compare_list = []
        cart = []
        question = None
        product_id = None
        address = None
        title = None
        list_of_products = None
        attributes_list = None # not necessary works on the fly as query  is regenerated 
        topic = None
        product_name = None
        product_ids = None
        delivery_address = None
        other_product = None
        last_shown_options_string = None
        clarification_conversation = None
        problem_with_product_ids = 0

        try :
            for i, intent in enumerate(path):
                if intent == intents.stop:
                    continue
                if i % 2 == 0:
                    role = 'system'
                else:
                    role = 'user'
                if i < path_length - 1:
                    next_intent = path[i + 1]
                else:
                    next_intent = None

                response, used_tokens, state, prompt = self.generate_response(intent, next_intent=next_intent, prev_intent=prev_intent, 
                                                            args={'product': product, 
                                                                    'query': query,
                                                                    'page': results_page, 
                                                                    'results': search_results,
                                                                    'golden_result_position': golden_result_position,
                                                                    'bot': prev_bot_response,
                                                                    'user': prev_user_response,
                                                                    'compare_list':compare_list,
                                                                    'cart':cart,
                                                                    'question' :question,
                                                                    'product_id' :product_id,
                                                                    'address' : address,
                                                                    'title' : title,
                                                                    'list_of_products' : list_of_products,
                                                                    'attributes_list' : attributes_list,
                                                                    'topic' : topic,
                                                                    'product_name' : product_name,
                                                                    'product_ids' : product_ids,
                                                                    'delivery_address' : delivery_address,
                                                                    'path' : path,
                                                                    "path_pos" : i,
                                                                    "other_product" : other_product,
                                                                    "cart_i" : cart_i,
                                                                    "aux_cart" : aux_cart,
                                                                    "compare_i" : compare_i,
                                                                    "aux_compare" : aux_compare,
                                                                    'last_shown_options_string' :last_shown_options_string,
                                                                    'clarification_conversation' : clarification_conversation,
                                                                    })
                if response is None:
                    print("Got response None")
                    write_gpt_resp_None(prompt, response)
                    response = extract_response(response, conversation, path, prompt)
                    if response is None :
                        print("Exited path here!!")
                        return response, total_used_tokens, product['id'], path
                
                if isinstance(response, str):
                    if "\"question\":" in response or "\"text\":" in response :
                        response = json.loads(response)
                    else:
                        response = {'text': response}
                
                if intent == intents.more_results:
                    results_page += 1
                
                elif intent in [intents.search_product, intents.suggest_product, intents.refine_query]: # in search queries
                    results_page = 1
                elif intent in [intents.show_results] and len(response['product_ids']) == 0:
                    intent = intents.no_results

                intent = state['intent']
                prev_intent = intent
                golden_result_position = state['golden_result_position']
                cart = state['cart']
                compare_list = state['compare_list']
                other_product = state['other_product']
                aux_cart = state['aux_cart']
                aux_compare = state['aux_compare']
                clarification_conversation = state['clarification_conversation']
                
                if state['suggestions'] != None:
                    response['suggestions'] = state['suggestions']
                if state['search_results'] != None:
                    search_results = state['search_results']
                if state['cart_i'] != None :
                    cart_i = state['cart_i']
                if state['compare_i'] !=None :
                    compare_i = state['compare_i']
                last_shown_options_string = state['last_shown_options_string']
                
                # getting query from response 
                if 'query' in response:
                    query = response['query']
                if 'question' in response:
                    question = response['question']
                if 'product_id' in response:
                    product_id = response['product_id']
                if 'address' in response:
                    address = response['address']
                if 'title' in response:
                    title = response['title']
                if 'list_of_products' in response:
                    list_of_products = response['list_of_products']
                if 'attributes_list' in response:
                    attributes_list = response['attributes_list']
                if 'topic' in response:
                    topic = response['topic']
                
                if 'product_name' in response:
                    product_name = response['product_name']
                if 'product_ids' in response:
                    product_ids = response['product_ids']
                if 'address' in response and not isinstance(response, str):
                    delivery_address = response['address']

                

                response['role'] = role
                response['intent'] = intent
                response['model'] = state['model']
                response['prompt'] = prompt

                if intent == intents.show_results :
                    response['results'] = [r['id'] for r in search_results]

                    response['results_str'] = '\n'.join([f"id: {j+1}, {self.product_to_string(d,shortest=True)}" for j, d in enumerate(search_results)])
                
                elif intent == 'select_i':
                    response['selection'] = golden_result_position+1

                #print(response)
                response['gtp_4_turbo'] = used_tokens[gpt_4_turbo]
                response[gpt_4] = used_tokens[gpt_4]
                conversation.append(response)

                if role == 'system':
                    prev_bot_response = response['text']
                else:
                    if 'text' in response :
                        prev_user_response = response['text']
                    else :
                        prev_user_response = response['question']
                
                total_used_tokens[gpt_4_turbo] += used_tokens[gpt_4_turbo]
                total_used_tokens[gpt_4] += used_tokens[gpt_4]
                
            if problem_with_product_ids > 0 :
                print(f"Found {problem_with_product_ids} problems with product_ids")
            return conversation, total_used_tokens, product['id'], path, aux_cart, aux_compare
        except :
            print(f"Found error in a conversation with product id : {product['id']}")
            write_error_product_id(product['id'])
            return conversation, total_used_tokens, product['id'], path, aux_cart, aux_compare
    
    def format_product(self, d):
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
    
    def add_locations(self, d) :
        l = random.randint(0, len(locations)-1)
        d['location'] = locations[:l]
        return d
    
    def add_ids(self, older_files, added_ids) :
        
        for file in older_files :
            with open(file,'r') as f:
                for line in f:
                    d = json.loads(line.rstrip('\n'))
                    added_ids.add(d['id'])


        return added_ids


    def generate_conversations(self, limit=10):
        added_ids = set()
        # older_files = ['data/ecom_conversations_test.jsonl']
        # added_ids = self.add_ids(older_files, added_ids)
        # remove_ids = set()
        # remove_ids = self.add_ids(['errors_product_id.jsonl'], remove_ids)
        # added_ids
        products = []
        products_for_sampling = []
        with open(inventory_file, 'r') as file:
            for line in file:
                d = json.loads(line)
                # d = self.add_locations(d)
                products_for_sampling.append(d)
                if d['id'] not in added_ids : # or d['id'] in remove_ids
                    prdt = self.format_product(d)
                    products.append(prdt)

        o = open('data/ecom_conversations_test.jsonl', 'a')
        total_used_tokens = {gpt_4_turbo: 0, gpt_4: 0}
        completed = 0
        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = []
            
            for prod in products[:limit]:
                with pos_lock :
                    # futures.append(executor.submit(self.generate_conversation, prod, products)) 
                    futures.append(executor.submit(self.generate_conversation, prod, products_for_sampling)) 
                    
                    
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                conversation, used_tokens, product_id, path, aux_cart, aux_compare = future.result()
                with lock:
                    if len(conversation) > 0:
                        o.write(json.dumps({"id": product_id, "path": path,"aux_cart":aux_cart, "aux_compare": aux_compare , "conversation": conversation}) + "\n")
                        o.flush()
                total_used_tokens[gpt_4_turbo] += used_tokens[gpt_4_turbo]
                total_used_tokens[gpt_4] += used_tokens[gpt_4]
                completed += 1
        
        print(total_used_tokens)
        estimated_cost = (total_used_tokens[gpt_4_turbo]/2*0.001/1000 + total_used_tokens[gpt_4_turbo]/2*0.003/1000) + \
            (total_used_tokens[gpt_4]/2*0.03/1000 + total_used_tokens[gpt_4]/2*0.06/1000)
        print("Estimated cost: ${:.2f}".format(estimated_cost))

if __name__ == '__main__':
    generator = DataGenerator()

    generator.generate_conversations(limit=100)



