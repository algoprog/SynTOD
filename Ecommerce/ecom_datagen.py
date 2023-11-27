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

from ecom_prompts import *
from ecom_retriever import Retriever
from constants import *
from gpt4_free import GPT4_Free_API

openai.api_key = openai_key
lock = threading.Lock()
gpt_resp_lock = threading.Lock()
inventory_file = "data/product_catalog.jsonl"
pos_lock = threading.Lock()

gpt4 = GPT4_Free_API()

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


def chatgpt_api(prompt, model='gpt-3.5-turbo', temperature=0.0, max_retries=64):
    for i in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                max_tokens=2000,
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

# def chatgpt_api(prompt, model='gpt-3.5-turbo', temperature=0.0, max_retries=64):
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

def generate_conversation(task_name): 
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
    response, used_tokens = chatgpt_api(prompt)
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


def generate_conversation_and_write(task_name):
    conversation, used_tokens = generate_conversation(task_name)
    write_conversation_to_file(conversation)
    print(used_tokens)


class DataGenerator:
    def __init__(self) -> None:
        self.retriever = Retriever()

    def get_attributes(self, attributes) :
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
    
    def attri_to_string(self, attributes):
        attri = self.get_attributes(attributes)
        final_Str = '['
        
        for key in attri.keys():
            t = f"({key} , {attri[key]}), "
            final_Str += t
        if final_Str[-2:] == ", " :
            final_Str = final_Str[:-2]
        
        final_Str += ']'
        return final_Str
    
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
        if short :
            f_S = f"{product['title']}"
            if 'description' in product.keys() :
                f_S += f", {product['description'][0]}"
            if 'attributes' in product.keys() :
                f_S += f", {self.attri_to_string(product['attributes'])}\n"
            
        if shortest :
            f_S = f"{product['title']}"

            if 'description' in product.keys() :
                f_S += f", {product['description'][0]}"
            
        if short or shortest :
            if "overall" in product and "rating" in append:
                f_S += f", rating: {product['overall']}"
            return f_S

        des = ''
        if 'description' in product.keys() :
                des = f", description:  {product['description'][0]}"
        f_S = f"title: {product['title']}{des}, overall: {product['overall']}, reviewCount: ({product['reviewCount']}), attributes: {self.attri_to_string(product['attributes'])}"

        # if 'feature' in product.keys() :
        #     f_S += f", features : {self.features_to_string(product['feature'])}"
        # if 'details' in product.keys() :
        #     if(len(product['details']) <= 200) :
        #         f_S += f", details: {self.details_to_string(product['details'])}"

        return f_S

    def generate_response(self, intent, next_intent=None, prev_intent=None, args=None):
        
        total_used_tokens = {'gpt-3.5-turbo': 0, 'gpt-4': 0}
        temperature = 1.0
        json_format = None
        model = 'gpt-3.5-turbo'
        multi_output = False
        golden_result_position = args['golden_result_position']
        search_results = None
        suggestions = None
        returned_intent = intent
        prompt = None
        compare_list = args['compare_list']
        cart = args['cart']

        if args['product'] != None :
            product_info = self.product_to_string(args['product'])
        

        if intent == intents.start:  
            prompt = START_PROMPT['prompt']
            #model = 'gpt-4'
        elif intent == intents.search_product:
            prompt = SEARCH_PRODUCT_PROMPT['prompt'].format(args['product'])
            json_format = SEARCH_PRODUCT_PROMPT['json_format']
            # model = 'gpt-4'
        elif intent == intents.suggest_product:
            product_info = self.product_to_string(args['product'])
            # product_info = f"title: {args['product']['title']}, description: {args['product']['description']}, attributes: [{', '.join(args['product']['attributes'])}]"
            prompt = SUGGEST_PRODUCT_PROMPT['prompt'].format(product_info)
            json_format = SUGGEST_PRODUCT_PROMPT['json_format']
            # model = 'gpt-4'
        elif intent == intents.show_results :
            model = 'gpt-4'
            temperature = 0.0
            product_id = args['product']['id']
            # retrieve 20 results, remove the current product id doc, and get the next 2-3 results
            results = self.retriever.search(args['query'], limit=20)

            #print("\nretriever results:", ', '.join([r[0]['title'] for r in results]))

            if next_intent == intents.select_i:
                results = [r[0] for r in results if r[0]['id'] != product_id][(args['page']-1)*2 : args['page']*2]
                # add the current recipe id doc to the results in random position k
                golden_result_position = random.randint(0, len(results))
                results.insert(golden_result_position, args['product'])
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
            else:
                prompt_template = SHOW_RESULTS_PROMPT

            prompt = prompt_template['prompt'].format(args['query'], results)
            json_format = prompt_template['json_format']
        elif intent == intents.more_results :
            prompt = MORE_OPTIONS_PROMPT['prompt'].format(args['query'])
            json_format = MORE_OPTIONS_PROMPT['json_format']
            temperature = 1.2
        elif intent == intents.select_i:
            # model = 'gpt-4'
            results = [f"id: {i+1}, {self.product_to_string(d, shortest=True, append =['rating'])}" for i, d in enumerate(args['results'])]
            results = '\n'.join(results)
            prompt = SELECT_I_PROMPT['prompt'].format(args['golden_result_position']+1, results)
            json_format = SELECT_I_PROMPT['json_format']
            multi_output = True
        elif intent == intents.option_selected:
            desc = ''
            if 'description' in args['product'] :
                desc = args['product']['description']
            elif 'feature' in args['product'] :
                desc = args['product']['feature']
            prompt = OPTION_SELECTED_PROMPT['prompt'].format(args['product']['title'], desc)
            json_format = OPTION_SELECTED_PROMPT['json_format']
        
        elif intent == intents.shown_attributes :
            model = 'gpt-4'
            # product_info = f"title: {args['product']['title']}, description: {args['product']['description']}, attributes: [{', '.join(args['product']['attributes'])}]]"
            product_info = self.product_to_string(args['product'])
            prompt = SHOWN_ATTRIBUTES_PROMPT['prompt'].format(product_info)
            json_format = SHOWN_ATTRIBUTES_PROMPT['json_format']
        elif intent == intents.show_attributes :
            model = 'gpt-4'
            product_info = self.product_to_string(args['product'])
            prompt = SHOW_ATTRIBUTES_BEGIN_PROMPT['prompt'].format(product_info)
            json_format = SHOW_ATTRIBUTES_BEGIN_PROMPT['json_format']
            multi_output = True
        
        elif intent == intents.acknowledge:
            # model = 'gpt-4'
            prompt = ACKNOWLEDGE_PROMPT['prompt']
            json_format = ACKNOWLEDGE_PROMPT['json_format']
            multi_output = True
        
        elif intent in [intents.show_suggestions, intents.shown_cart, intents.show_comparison] :
            model = 'gpt-4'
            topk = 10
            prompt = FIND_SUGGESTIONS_PROMPT['prompt'].format(topk, args['query'])
            response, used_tokens = chatgpt_api(prompt, model='gpt-3.5-turbo', temperature=0.0, max_retries=7)
            if response is None:
                write_error(f'ERROR: {prompt}')
                return None, total_used_tokens, None, prompt
            total_used_tokens['gpt-3.5-turbo'] += used_tokens
            ungrounded_suggestions = response.split('\n')
            ungrounded_suggestions = [r for r in ungrounded_suggestions if r != '']
            suggestions = ungrounded_suggestions
            grounded_suggestions = []
            added_ids = set()
            i = 1
            for q in ungrounded_suggestions:
                d, score = self.retriever.search(q, limit=1)[0]
                if score > 0.4 and d['id'] != args['product']['id'] and d['id'] not in added_ids:
                    grounded_suggestions.append(d)
                    added_ids.add(d['id'])
                    i += 1

            # retrieve up to 10 results, remove the current product id doc, and get the next 2-3 results
            if next_intent == intents.select_i :
                grounded_suggestions = grounded_suggestions[(args['page']-1)*2 : args['page']*2]
                golden_result_position = random.randint(0, len(grounded_suggestions))
                grounded_suggestions.insert(golden_result_position, args['product'])
            else:
                grounded_suggestions = grounded_suggestions[(args['page']-1)*3 : args['page']*3]
            
            search_results = grounded_suggestions

            grounded_suggestions = [f"id: {j+1}, {self.product_to_string(d, shortest=True)}" for j, d in enumerate(grounded_suggestions)] # rating: {d['overall']} ({d['vote']}), 
            # may need to handle grounded suggestions for compare and cart list !!!
            if prev_intent == intents.more_options:
                prompt_template = SHOW_MORE_RESULTS_PROMPT
            elif prev_intent == intents.show_cart :
                prompt_template = SHOWN_CART_PROMPT['prompt']
            elif prev_intent == intents.compare_products :
                prompt_template = SHOW_COMPARISON_PROMPT['prompt']
            else:
                prompt_template = SHOW_RESULTS_PROMPT

            prompt = prompt_template['prompt'].format(args['query'], '\n'.join(grounded_suggestions))
            if prev_intent in [intents.show_cart, intents.show_comparison] :
                if prev_intent == intents.show_cart :
                    state_list = args['cart']
                else :
                    state_list = args['compare_list']
                    # if args['list_of_products'] != None:
                    #     state_list = args['list_of_products']
                search_results = state_list
                prompt = prompt_template['prompt'].format(args['query'], '\n'.join(state_list) )
            json_format = prompt_template['json_format']

            if len(search_results) == 0:
                returned_intent = intents.no_results
        
        elif intent == intents.open_domain_qa:
            
            prompt = OPEN_DOMAIN_QA_PROMPT['prompt']
            json_format = OPEN_DOMAIN_QA_PROMPT['json_format']
        
        elif intent == intents.chitchat :
            prompt = CHITCHAT_PROMPT['prompt']
            json_format = CHITCHAT_PROMPT['json_format']
            #model = 'gpt-4'
        
        
        elif intent == intents.subjective_qa :
            prompt = SUBJECTIVE_QA_PROMPT['prompt']
            json_format = SUBJECTIVE_QA_PROMPT['json_format']
            multi_output = True
            model = 'gpt-4'
        
        elif intent == intents.user_start:
            prompt = START_PROMPT_USER['prompt']
            json_format = START_PROMPT_USER['json_format']
            multi_output = True
        
            #model = 'gpt-4'
        
        elif intent == intents.repeat :
            prompt = REPEAT_PROMPT['prompt']
            json_format = REPEAT_PROMPT['json_format']
            multi_output = True
            # model = 'gpt-4'
        elif intent == intents.deny :
            prompt = DENY_PROMPT['prompt'].format(args['bot'])
            json_format = DENY_PROMPT['json_format']
            # model = 'gpt-4'
        elif intent == intents.stop :
            prompt = STOP_PROMPT['prompt']
            json_format = STOP_PROMPT['json_format']
            multi_output = True
            # model = 'gpt-4'
        
        elif intents.system_response in intent: # string in a string
            # if prev_intent in [intents.open_domain_qa, intents.product_qa, intents.shown_attributes]:
                # model = 'gpt-4'
            if prev_intent == intents.shown_attributes:
                prompt = SHOWN_ATTRIBUTES_PROMPT['prompt'].format('\n'.join(args['product'][attributes]))
                # json_format = SHOWN_ATTRIBUTES_PROMPT['json_format']
            elif prev_intent in [intents.open_domain_qa, intents.deny, intents.chitchat, intents.dangerous_product, intents.subjective_qa]:
                prompt = SYSTEM_PROMPT['prompt'].format(args['user'])
            elif prev_intent in [intents.product_qa, intents.show_attributes, intents.remove_from_cart, intents.remove_from_compare, intents.add_for_compare, intents.add_to_cart]:
                # product_info = f"title: {args['product']['title']}, description: {args['product']['description']}, {attributes}: [{', '.join(args['product'][attributes])}]]"
                product_info = self.product_to_string(args['product'])
                prompt = IN_CONVERSATION_SYSTEM_PROMPT['prompt'].format( product_info, args['user'])
            
            elif prev_intent == intents.repeat:
                prompt = SYSTEM_REPEAT_PROMPT['prompt'].format(args['bot'], args['user'])
            
            else :
                product_info = self.product_to_string(args['product'])
                prompt = IN_CONVERSATION_SYSTEM_PROMPT['prompt'].format( product_info, args['user'])
        
        elif intent == intents.show_cart : 
            prompt = SHOW_CART_PROMPT['prompt'].format(args['bot'])
            # json_format = SEARCH_PRODUCT_PROMPT['json_format']
            model = 'gpt-4'
        
        elif intent == intents.buy_cart:
            prompt = BUY_CART_PROMPT['prompt'].format(args['bot'])
            
            # model = 'gpt-4'
        elif intent == intents.add_to_cart:
            # product_info = f"title: {args['product']['title']}, description: {args['product']['description']}, attributes: [{', '.join(args['product']['attributes'])}]"
            product_info = self.product_to_string(args['product'])
            prompt = ADD_TO_CART_PROMPT['prompt'].format(product_info,args['bot'])
            
            if 'cart' in args.keys() :
                cart = args['cart']
            cart.append(args['product'])
            
            model = 'gpt-4'
        elif intent == intents.add_for_compare:
            # product_info = f"title: {args['product']['title']}, description: {args['product']['description']}, attributes: [{', '.join(args['product']['attributes'])}]"
            product_info = self.product_to_string(args['product'])
            
            if 'compare_list' in args.keys():
                compare_list = args['compare_list']
            compare_list.append(args['product'])
            

            prompt = ADD_FOR_COMPARE_PROMPT['prompt'].format(args['product'],args['bot'])
            
            model = 'gpt-4'
        elif intent == intents.remove_from_compare:
            # product_info = f"title: {args['product']['title']}, description: {args['product']['description']}, attributes: [{', '.join(args['product']['attributes'])}]"
            product_info = self.product_to_string(args['product'])
            prompt = REMOVE_FROM_COMPARE_PROMPT['prompt'].format(args['product'],args['bot'])
            
            if 'compare_list' in args.keys() :
                compare_list = args['compare_list']
                compare_list.remove(args['product'])


            
            # model = 'gpt-4'
        elif intent == intents.remove_from_cart:
            # product_info = f"title: {args['product']['title']}, description: {args['product']['description']}, attributes: [{', '.join(args['product']['attributes'])}]"
            product_info = self.product_to_string(args['product'])
            prompt = REMOVE_FROM_CART_PROMPT['prompt'].format(args['product'],args['bot'])
            
            if 'cart' in args.keys():
                cart = args['cart']
                cart.remove(args['product'])

            # model = 'gpt-4'

        elif intent == intents.generic_product_query:
            # product_info = f"title: {args['product']['title']}, description: {args['product']['description']}, attributes: [{', '.join(args['product']['attributes'])}]"
            product_info = self.product_to_string(args['product'])
            prompt = USER_GENERIC_PRODUCT_PROMPT['prompt'].format(args['product'],args['bot'])
            
            # model = 'gpt-4'

        elif intent == intents.product_qa:
            # product_info = f"title: {args['product']['title']}, description: {args['product']['description']}, attributes: [{', '.join(args['product']['attributes'])}]"
            product_info = self.product_to_string(args['product'])
            prompt = PRODUCT_QA_PROMPT['prompt'].format(args['product'])
            
            # model = 'gpt-4'
        elif intent == intents.compare_products:
            # product_info = f"title: {args['product']['title']}, description: {args['product']['description']}, attributes: [{', '.join(args['product']['attributes'])}]"
            # title = 'title'
            # description = 'description'
            delm = ', '
            # if args['list_of_products']!=None :
            #     list_of_products = args['list_of_products']

            # prompt = COMPARE_PRODUCTS_PROMPT['prompt'].format(f"[{delm.join([ f'title: {product[title]}, description: {product[description]}, attributes: [{delm.join(product[attributes])}]' for product in args['compare_list']])}]")
            prompt = COMPARE_PRODUCTS_PROMPT['prompt'].format(f"[{delm.join([ f'[{self.product_to_string(product)}]' for product in args['compare_list']])}]")
            
            model = 'gpt-4'
        elif intent == intents.delivery_address:
            # product_info = f"title: {args['product']['title']}, description: {args['product']['description']}, attributes: [{', '.join(args['product']['attributes'])}]"
            product_info = self.product_to_string(args['product'])
            prompt = CHECK_DELIVERY_AVAILABILITY_PROMPT['prompt'].format(product_info, args['user'])
            # model = 'gpt-4'
        
        elif intent == intents.refine_query:
            # product_info = f"title: {args['product']['title']}, description: {args['product']['description']}, attributes: [{', '.join(args['product']['attributes'])}]"
            product_info = self.product_to_string(args['product'])
            prompt = USER_PREFERENCE_PROMPT['prompt'].format(product_info)
            # model = 'gpt-4'
            json_format = USER_PREFERENCE_PROMPT['json_format']
        
        elif intent == intents.more_results :
            prompt = MORE_OPTIONS_PROMPT['prompt']
            json_format = MORE_OPTIONS_PROMPT['json_format']
        
        elif intent == intents.bought_cart :
            prompt = BOUGHT_CART_PROMPT['prompt']
        
        elif intent == intents.bought_cart :
            prompt = BOUGHT_CART_PROMPT['prompt']
        
        elif intent == intents.clarifying_questions :
            prompt = ASK_CLARIFICATION_PROMPT['prompt'].format(args['user'])
        
        elif intent == intents.no_more_clarifying_questions :
            prompt = IN_CONVERSATION_SYSTEM_PROMPT['prompt'].format( product_info, args['user'])

        
        elif intent == intents.product_info :
            prompt = SHOW_PRODUCT_PROMPT['prompt'].format( product_info)
        
        


        
        #print(f"\n*** prompt ***\n{prompt}\n***\n")

        if prompt is None:
            write_error(f'ERROR: {intent}')

        response, used_tokens = chatgpt_api(prompt, model=model, temperature=temperature, max_retries=7)
        total_used_tokens[model] += used_tokens
        if response is None:
            write_error(f'ERROR: {prompt}')
            return None, total_used_tokens, None, prompt

        if json_format:
            try:
                response = json.loads(response)
            except:
                prompt = "fix the json below, expected format is {}, give only the correct json in your response nothing else:\n{}".format(json_format, response)
                response, used_tokens = chatgpt_api(prompt, model='gpt-4', max_retries=7)
                total_used_tokens['gpt-4'] += used_tokens
                if response is None:
                    write_error(f'ERROR: {prompt}')
                    return None, total_used_tokens, None, prompt
                try:
                    response = json.loads(response)
                except:
                    write_error(f'ERROR: {prompt}')
                    response = None
        elif multi_output:
            if intent == intents.show_attributes and "text" in response.keys():
                options = response['text']
            else :
                 options = response.split('\n')
            options = [r for r in options if r != '']
            response = random.choice(options)
        
        state = {'search_results': search_results,
                 'golden_result_position': golden_result_position,
                 'intent': returned_intent,
                 'cart' : cart,
                 'compare_list' : compare_list,
                 'suggestions': suggestions,
                 'model': model}

        return response, total_used_tokens, state, prompt

    def generate_conversation(self, product, max_length=30): #  pos ,
        
        
        path_generator = TaskPathGenerator()
        path = path_generator.generate_path(max_length=max_length)
        # path = path_generator.get_path_from_file(pos, 'generated_paths.csv')
        path_length = len(path)

        conversation = []
        prev_intent = None
        total_used_tokens = {'gpt-3.5-turbo': 0, 'gpt-4': 0}

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
                                                                 })
            if response is None:
                print("Got response None")
                write_gpt_resp_None(prompt, response)
                return conversation, total_used_tokens, product['id'], path
            
            if isinstance(response, str):
                if "\"question\":" in response or "\"text\":" in response :
                    response = json.loads(response)
                else:
                    response = {'text': response}
            
            if intent == intents.more_results:
                results_page += 1
            
            elif intent in [intents.search_product, intents.suggest_product, intents.refine_query]: # in search queries
                results_page = 1
            elif intent in [intents.show_results, intents.show_suggestions] and len(response['product_ids']) == 0:
                intent = intents.no_results

            intent = state['intent']
            prev_intent = intent
            golden_result_position = state['golden_result_position']
            cart = state['cart']
            compare_list = state['compare_list']
            
            if state['suggestions'] != None:
                response['suggestions'] = state['suggestions']
            if state['search_results'] != None:
                search_results = state['search_results']
            
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
            

            response['role'] = role
            response['intent'] = intent
            response['model'] = state['model']
            response['prompt'] = prompt

            if intent in [intents.show_results, intents.show_suggestions ]:
                response['results'] = [r['id'] for r in search_results]

                response['results_str'] = '\n'.join([f"id: {j+1}, {self.product_to_string(d,shortest=True)}" for j, d in enumerate(search_results)])
            
            elif intent == 'select_i':
                response['selection'] = golden_result_position+1

            #print(response)
            conversation.append(response)

            if role == 'system':
                prev_bot_response = response['text']
            else:
                if 'text' in response :
                    prev_user_response = response['text']
                else :
                    prev_user_response = response['question']
            
            total_used_tokens['gpt-3.5-turbo'] += used_tokens['gpt-3.5-turbo']
            total_used_tokens['gpt-4'] += used_tokens['gpt-4']
            
            # if intent == intents.no_results:
            #     break
        
        return conversation, total_used_tokens, product['id'], path
    
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


    def generate_conversations(self, limit=10):
        added_ids = set()
        with open("data/conversations.jsonl",'r') as f:
            for line in f:
                d = json.loads(line.rstrip('\n'))
                added_ids.add(d['id'])
        with open("data/conversations2.jsonl",'r') as f:
            for line in f:
                d = json.loads(line.rstrip('\n'))
                added_ids.add(d['id'])
        
        products = []
        with open(inventory_file, 'r') as file:
            for line in file:
                d = json.loads(line)
                if d['id'] not in added_ids:
                    prdt = self.format_product(d)
                    products.append(prdt)

        o = open('data/conversations3.jsonl', 'a')
        total_used_tokens = {'gpt-3.5-turbo': 0, 'gpt-4': 0}
        completed = 0
        
        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = []
            # selected_paths_pos = [2,3,5,6,8,10,18,21,39]
            # pos = 0
            for prod in products[:limit]:
                with pos_lock :
                    futures.append(executor.submit(self.generate_conversation, prod)) # , selected_paths_pos[pos]
                    # pos +=1
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                conversation, used_tokens, product_id, path = future.result()
                with lock:
                    if len(conversation) > 0:
                        o.write(json.dumps({"id": product_id, "path": path, "conversation": conversation}) + "\n")
                        o.flush()
                total_used_tokens['gpt-3.5-turbo'] += used_tokens['gpt-3.5-turbo']
                total_used_tokens['gpt-4'] += used_tokens['gpt-4']
                completed += 1
        
        print(total_used_tokens)
        estimated_cost = (total_used_tokens['gpt-3.5-turbo']/2*0.0015/1000 + total_used_tokens['gpt-3.5-turbo']/2*0.002/1000) + \
            (total_used_tokens['gpt-4']/2*0.03/1000 + total_used_tokens['gpt-4']/2*0.06/1000)
        print("Estimated cost: ${:.2f}".format(estimated_cost))

if __name__ == '__main__':
    generator = DataGenerator()

    generator.generate_conversations(limit=1)
