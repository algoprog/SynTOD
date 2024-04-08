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
from path_generation import TaskPathGenerator

from prompts_modified import *
from retriever import Retriever

from openai import OpenAI

import google.generativeai as genai
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


# please specify which llm you intend to use
useapi = 'llama'
# useapi = 'llama' # 'mistral' #'llama' # gpt_4_turbo  


# please specify openai API key
openai.api_key = ""
lock = threading.Lock()

gpt_4_turbo = 'gpt-4-1106-preview'#'gpt-4-turbo'
gpt_4 = 'gpt-4'

# please specify google gemini API key
GOOGLE_API_KEY = ''
# please specify mistral API key
MISTRAL_KEY = ''
# please specify llama API key 
LLAMA_KEY = ''


gpt_client = OpenAI(
    # This is the default and can be omitted
    # please specify openai API key
    api_key="",
)

gemini_api_key = GOOGLE_API_KEY
genai.configure(api_key = gemini_api_key)

model_gemini = genai.GenerativeModel('gemini-pro')


# Create an OpenAI client with your deepinfra token and endpoint
openai_client = OpenAI(
    api_key=LLAMA_KEY,
    base_url="https://api.deepinfra.com/v1/openai",
)

def write_error(error):
    with lock:
        with open('errors.jsonl', 'a') as file:
            file.write(json.dumps({"error": error}) + "\n")
            file.flush()

def md5_hash(string):
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()


def gemini_api(prompt, model='gemini_pro', temperature=0.5, max_retries=64, max_tokens = 2000) :
    for i in range(max_retries) :
        response = model_gemini.generate_content(
                                prompt,
                                generation_config=genai.types.GenerationConfig(
                                    candidate_count=1,
                                    # stop_sequences=['space'],
                                    max_output_tokens=max_tokens,
                                    temperature=temperature/2.0)
                                )
        if response != None:
            return response.text, 0

    return None, 0



def llama_api(prompt, model="meta-llama/Llama-2-70b-chat-hf", temperature=0.5, max_retries=64, max_tokens = 2000):
    for i in range(max_retries) :
        try :
            
            response = openai_client.chat.completions.create(
                    model="meta-llama/Llama-2-70b-chat-hf",
                    max_tokens=max_tokens,
                    temperature=temperature,
                    timeout=40.0,
                    messages=[{'role': 'user', 'content': prompt}]
                    )
            
            used_tokens = response.usage.total_tokens
            return response.choices[0].message.content, used_tokens

            
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in {20} seconds...")
            if e.status_code == 400 :
                prompt = prompt + ". Keep response SHORT"
            time.sleep(2)

    return None, 0 


def mistral_api(prompt, model="mistral-tiny", temperature=0.5, max_retries=64, max_tokens = 2000):
    
    model = "mistral-medium" # tiny small medium

    for i in range(max_retries):
        api_key = MISTRAL_KEY
        
        client = MistralClient(api_key=api_key)

        messages = [
            ChatMessage(role="user", content=prompt)
        ]
        try:
            
            # No streaming
            response = client.chat(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                
            )
            used_tokens = response.usage.total_tokens
            return response.choices[0].message.content.strip(), used_tokens
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in {20} seconds...")
            time.sleep(20)
    return None, 0


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


def llm_api(prompt, model=gpt_4_turbo, temperature=0.5, max_retries=64, max_tokens = 2000, api = useapi) :
    if api == "gemini" :
        model = 'gemini_pro'
        return gemini_api(prompt,model, temperature, max_retries, max_tokens)
    elif api == gpt_4_turbo or api == gpt_4 :
        return chatgpt_api(prompt, model=model, temperature=temperature, max_retries=7,max_tokens = max_tokens)
    elif api == 'llama' :
        return llama_api(prompt, model="meta-llama/Llama-2-70b-chat-hf", temperature=temperature, max_retries=7,max_tokens = max_tokens)
    elif api == "mistral" :
        return mistral_api(prompt, model=model, temperature=temperature, max_retries=7,max_tokens = max_tokens)
    
    
    return None, 0
    


def generate_conversation(task_name):
    prompt = f"""Simulate a conversation between a taskbot system and a user about {task_name}. 
- The taskbot helps users with recipes or tasks. 
- First the system introduces itself, then the user asks for help about a recipe or task. 
- System provides 3 relevant options, user selects one, system responds to the choice and guides the user step by step after user finishes every step. 
- Sometimes user asks in-task or open-domain questions in between, or even chitchats. 
- Sometimes the system mentions some relevant fun facts.
- In the end the user may thank the taskbot, taskbot asks if he has any other question, user might ask something related to the ask or open-domain and eventually the conversation ends. 
- Remember that the taskbot should guide the user step by step after getting confirmation from the user. Only show one step at a time. 

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

    def task_to_string(self, task, current_step=None):
        steps_str = ', '.join([f"'{i+1}: {s}'" for i, s in enumerate(task['steps'])])
        return f"title: {task['title']}, description: {task['description']}, minutes: {task['minutes']}, rating: {task['rating']} ({task['ratingCount']}), ingredients: [{self.get_dict_to_str_joined(task['ingredients'])}], current step: {current_step}, steps: [{steps_str}]"

    def get_dict_to_str_joined(self, dictionaries, delim = ", ") :
        sts  = []
        for d in dictionaries :
            sts.append(str(d))
        return delim.join(sts)

    def generate_response(self, intent, next_intent=None, prev_intent=None, args=None):
        #print("\nintent:", intent)

        total_used_tokens = {'gpt-3.5-turbo': 0, 'gpt-4': 0, useapi : 0}
        temperature = 1.0
        json_format = None
        model = 'gpt-3.5-turbo'
        multi_output = False
        golden_result_position = args['golden_result_position']
        search_results = None
        suggestions = None
        returned_intent = intent
        prompt = None
        step = None
        if 0 < args['step'] <= len(args['recipe']['steps']):
            prev_step_text = args['recipe']['steps'][args['step']-1]
        else:
            prev_step_text = '-'

        if intent == 'start':
            prompt = START_PROMPT['prompt']
            #model = 'gpt-4'
        elif intent == 'search_recipe':
            prompt = SEARCH_RECIPE_PROMPT['prompt'].format(args['recipe']['query'])
            json_format = SEARCH_RECIPE_PROMPT['json_format']
            model = 'gpt-4'
        elif intent == 'suggest_recipe':
            # recipe = f"title: {args['recipe']['title']}, description: {args['recipe']['description']}, ingredients: [{', '.join(args['recipe']['ingredients'])}]"
            recipe = f"title: {args['recipe']['title']}, description: {args['recipe']['description']}, ingredients: [{self.get_dict_to_str_joined(args['recipe']['ingredients'])}]" # , ingredients: [{self.get_dict_to_str_joined(args['recipe']['ingredients'])}]
            prompt = SUGGEST_RECIPE_PROMPT['prompt'].format(recipe)
            json_format = SUGGEST_RECIPE_PROMPT['json_format']
            model = 'gpt-4'
        elif intent == 'show_results':
            #model = 'gpt-4'
            temperature = 0.0
            recipe_id = args['recipe']['id']
            # retrieve 20 results, remove the current recipe id doc, and get the next 2-3 results
            ress = self.retriever.search(args['query'], limit=20)
            results = []
            for res in ress :
                results.append((self.remove_urls(res[0]),res[1]))

            #print("\nretriever results:", ', '.join([r[0]['title'] for r in results]))

            if next_intent == 'select_i':
                results = [r[0] for r in results if r[0]['id'] != recipe_id][(args['page']-1)*2 : args['page']*2]
                # add the current recipe id doc to the results in random position k
                golden_result_position = random.randint(0, len(results))
                results.insert(golden_result_position, args['recipe'])
                #print('results offsets:', (args['page']-1)*2, args['page']*2)
            else:
                results = [r[0] for r in results if r[0]['id'] != recipe_id][(args['page']-1)*3 : args['page']*3]
                #print('results offsets:', (args['page']-1)*3, args['page']*3)
            
            search_results = results
            if len(search_results) == 0:
                returned_intent = 'no_results'

            # format the results
            # results = [f"id: {i+1}, {r['title']}, {r['minutes']} minutes, rating: {r['rating']} ({r['ratingCount']}), {r['description']}, ingredients: [{', '.join(r['ingredients'])}]\n" for i, r in enumerate(results)]
            results = [f"id: {i+1}, {r['title']}, {r['minutes']} minutes, rating: {r['rating']} ({r['ratingCount']}), {r['description']}, ingredients: [{self.get_dict_to_str_joined(r['ingredients'])}]\n" for i, r in enumerate(results)]
            results = '\n'.join(results)

            if prev_intent == 'more_results':
                prompt_template = SHOW_MORE_RESULTS_PROMPT
            else:
                prompt_template = SHOW_RESULTS_PROMPT

            prompt = prompt_template['prompt'].format(args['recipe']['query'], results)
            json_format = prompt_template['json_format']
        elif intent == 'more_results':
            prompt = MORE_OPTIONS_PROMPT['prompt'].format(args['recipe']['query'])
            json_format = MORE_OPTIONS_PROMPT['json_format']
            temperature = 1.2
        elif intent == 'select_i':
            model = 'gpt-4'
            results = [f"id: {i+1}, {d['title']}, {d['minutes']} minutes, rating: {d['rating']} ({d['ratingCount']}), {d['description']}" for i, d in enumerate(args['results'])]
            results = '\n'.join(results)
            prompt = SELECT_I_PROMPT['prompt'].format(args['golden_result_position']+1, results)
            json_format = SELECT_I_PROMPT['json_format']
            multi_output = True
        elif intent == 'option_selected':
            prompt = OPTION_SELECTED_PROMPT['prompt'].format(args['recipe']['title'], args['recipe']['description'])
            json_format = OPTION_SELECTED_PROMPT['json_format']
        elif intent == 'begin_task':
            prompt = BEGIN_TASK_PROMPT['prompt']
            json_format = BEGIN_TASK_PROMPT['json_format']
            multi_output = True
        elif intent == 'started_task':
            model = 'gpt-4'
            prompt = STARTED_TASK_PROMPT['prompt'].format(args['recipe']['title'], args['recipe']['steps'][0])
            json_format = STARTED_TASK_PROMPT['json_format']
        elif 'goto_step' in intent:
            model = 'gpt-4'
            step = int(intent.split('_')[-1])
            returned_intent = 'goto_step'
            prompt = GOTO_STEP_PROMPT['prompt'].format(step)
            json_format = GOTO_STEP_PROMPT['json_format']
            multi_output = True
        elif intent == 'show_step':
            #model = 'gpt-4'
            steps_str = ', '.join([f"'{i+1}: {s}'" for i, s in enumerate(args['recipe']['steps'])])
            # recipe_info = f"title: {args['recipe']['title']}, description: {args['recipe']['description']}, ingredients: [{', '.join(args['recipe']['ingredients'])}], steps: [{steps_str}]"
            recipe_info = f"title: {args['recipe']['title']}, description: {args['recipe']['description']}, steps: [{steps_str}] , ingredients: [{self.get_dict_to_str_joined(args['recipe']['ingredients'])}]" # , ingredients: [{self.get_dict_to_str_joined(args['recipe']['ingredients'])}]
            prompt = SHOW_STEP_PROMPT['prompt'].format(recipe_info, args['step'])
            json_format = SHOW_STEP_PROMPT['json_format']
        elif intent == 'acknowledge_step':
            #model = 'gpt-4'
            prompt = ACKNOWLEDGE_STEP_PROMPT['prompt'].format(args['recipe']['title'], prev_step_text)
            json_format = ACKNOWLEDGE_STEP_PROMPT['json_format']
            multi_output = True
        elif intent == 'acknowledge_task':
            model = 'gpt-4'
            prompt = ACKNOWLEDGE_TASK_PROMPT['prompt']
            json_format = ACKNOWLEDGE_TASK_PROMPT['json_format']
            multi_output = True
        elif intent == 'next_step':
            #model = 'gpt-4'
            prompt = NEXT_STEP_PROMPT['prompt'].format(args['recipe']['title'], prev_step_text)
            json_format = NEXT_STEP_PROMPT['json_format']
            multi_output = True
            temperature = 0.0
        elif intent == 'done_step':
            #model = 'gpt-4'
            prompt = DONE_STEP_PROMPT['prompt'].format(args['recipe']['title'], prev_step_text)
            json_format = DONE_STEP_PROMPT['json_format']
            multi_output = True
        elif intent == 'show_suggestions':
            #model = 'gpt-4'
            topk = 10
            prompt = FIND_SUGGESTIONS_PROMPT['prompt'].format(topk, args['query'])
            # response, used_tokens = chatgpt_api(prompt, model='gpt-3.5-turbo', temperature=0.0, max_retries=7)
            response, used_tokens = llm_api(prompt, model='gpt-3.5-turbo', temperature=temperature, max_retries=7,max_tokens = 2000, api = useapi)
        
            if response is None:
                write_error(f'ERROR: {prompt}')
                return None, total_used_tokens, None, prompt
            total_used_tokens[useapi] += used_tokens # 'gpt-3.5-turbo'
            ungrounded_suggestions = response.split('\n')
            ungrounded_suggestions = [r for r in ungrounded_suggestions if r != '']
            suggestions = ungrounded_suggestions
            grounded_suggestions = []
            added_ids = set()
            i = 1
            for q in ungrounded_suggestions:
                d, score = self.retriever.search(q, limit=1)[0]
                if score > 0.4 and d['id'] != args['recipe']['id'] and d['id'] not in added_ids:
                    grounded_suggestions.append(d)
                    added_ids.add(d['id'])
                    i += 1

            # retrieve up to 10 results, remove the current recipe id doc, and get the next 2-3 results
            if next_intent == 'select_i':
                grounded_suggestions = grounded_suggestions[(args['page']-1)*2 : args['page']*2]
                golden_result_position = random.randint(0, len(grounded_suggestions))
                grounded_suggestions.insert(golden_result_position, args['recipe'])
            else:
                grounded_suggestions = grounded_suggestions[(args['page']-1)*3 : args['page']*3]
            
            search_results = grounded_suggestions

            grounded_suggestions = [f"id: {j+1}, {d['title']}, {d['minutes']} minutes, rating: {d['rating']} ({d['ratingCount']}), {d['description']}" for j, d in enumerate(grounded_suggestions)]
            
            if prev_intent == 'more_options':
                prompt_template = SHOW_MORE_RESULTS_PROMPT
            else:
                prompt_template = SHOW_RESULTS_PROMPT

            prompt = prompt_template['prompt'].format(args['query'], '\n'.join(grounded_suggestions))
            json_format = prompt_template['json_format']

            if len(search_results) == 0:
                returned_intent = 'no_results'
        elif intent == 'in_task_qa':
            task_info = self.task_to_string(args['recipe'], args['step'])
            prompt = IN_TASK_QA_PROMPT['prompt'].format(args['step'], task_info)
            json_format = IN_TASK_QA_PROMPT['json_format']
            #model = 'gpt-4'
        elif intent == 'open_domain_qa':
            task_info = self.task_to_string(args['recipe'], args['step'])
            if args['step'] == 0:
                prompt = OPEN_DOMAIN_QA_PROMPT['prompt']
                json_format = OPEN_DOMAIN_QA_PROMPT['json_format']
            else:
                prompt = OPEN_DOMAIN_QA_PROMPT_IN_TASK['prompt'].format(args['step'], task_info)
                json_format = OPEN_DOMAIN_QA_PROMPT_IN_TASK['json_format']
            #model = 'gpt-4'
        elif intent == 'chitchat':
            prompt = CHITCHAT_PROMPT['prompt']
            json_format = CHITCHAT_PROMPT['json_format']
            #model = 'gpt-4'
        elif intent == 'offense':
            prompt = OFFENSE_PROMPT['prompt']
            json_format = OFFENSE_PROMPT['json_format']
            multi_output = True
            model = 'gpt-4'
        elif intent == 'legal_advice':
            prompt = LEGAL_ADVICE_PROMPT['prompt']
            json_format = LEGAL_ADVICE_PROMPT['json_format']
            multi_output = True
            model = 'gpt-4'
        elif intent == 'financial_advice':
            prompt = FINANCIAL_ADVICE_PROMPT['prompt']
            json_format = FINANCIAL_ADVICE_PROMPT['json_format']
            multi_output = True
            model = 'gpt-4'
        elif intent == 'medical_advice':
            prompt = MEDICAL_ADVICE_PROMPT['prompt']
            json_format = MEDICAL_ADVICE_PROMPT['json_format']
            multi_output = True
            model = 'gpt-4'
        elif intent == 'dangerous_task':
            prompt = DANGEROUS_TASK_PROMPT['prompt']
            json_format = DANGEROUS_TASK_PROMPT['json_format']
            multi_output = True
            model = 'gpt-4'
        elif intent == 'personal_information':
            prompt = PERSONAL_INFORMATION_PROMPT['prompt']
            json_format = PERSONAL_INFORMATION_PROMPT['json_format']
            multi_output = True
            model = 'gpt-4'
        elif intent == 'suicide_attempt':
            prompt = SUICIDE_ATTEMPT_PROMPT['prompt']
            json_format = SUICIDE_ATTEMPT_PROMPT['json_format']
            multi_output = True
            model = 'gpt-4'
        elif intent == 'subjective_qa':
            prompt = SUBJECTIVE_QA_PROMPT['prompt']
            json_format = SUBJECTIVE_QA_PROMPT['json_format']
            multi_output = True
            model = 'gpt-4'
        elif intent == 'set_timer':
            SET_TIMER_PROMPT = random.choice([SET_TIMER_PROMPT_1, SET_TIMER_PROMPT_2, SET_TIMER_PROMPT_3])
            prompt = SET_TIMER_PROMPT['prompt']
            json_format = SET_TIMER_PROMPT['json_format']
            multi_output = True
            model = 'gpt-4'
        elif intent == 'user_start':
            prompt = START_PROMPT_USER['prompt']
            json_format = START_PROMPT_USER['json_format']
            multi_output = True
        elif intent == 'no_more_steps':
            recipe_info = f"title: {args['recipe']['title']}, description: {args['recipe']['title']}"
            prompt = NO_MORE_STEPS_PROMPT['prompt'].format(recipe_info)
            json_format = NO_MORE_STEPS_PROMPT['json_format']
            #model = 'gpt-4'
        elif intent == 'finish_task':
            prompt = FINISH_TASK_PROMPT['prompt']
            json_format = FINISH_TASK_PROMPT['json_format']
            multi_output = True
            #model = 'gpt-4'
        elif intent == 'show_ingredients':
            prompt = SHOW_INGREDIENTS_PROMPT['prompt']
            json_format = SHOW_INGREDIENTS_PROMPT['json_format']
            multi_output = True
            model = 'gpt-4'
        elif intent == 'repeat':
            prompt = REPEAT_PROMPT['prompt']
            json_format = REPEAT_PROMPT['json_format']
            multi_output = True
            model = 'gpt-4'
        elif intent == 'deny':
            prompt = DENY_PROMPT['prompt'].format(args['bot'])
            json_format = DENY_PROMPT['json_format']
            model = 'gpt-4'
        elif intent == 'stop':
            prompt = STOP_PROMPT['prompt']
            json_format = STOP_PROMPT['json_format']
            model = 'gpt-4'
        elif intent == 'task_complete':
            prompt = TASK_COMPLETE_PROMPT['prompt']
            json_format = TASK_COMPLETE_PROMPT['json_format']
            model = 'gpt-4'
        elif 'system_response' in intent:
            if prev_intent in ['open_domain_qa', 'in_task_qa', 'show_ingredients']:
                model = 'gpt-4'
            if prev_intent == 'show_ingredients':
                # prompt = DISPLAY_INGREDIENTS_PROMPT['prompt'].format('\n'.join(args['recipe']['ingredients']))
                prompt = DISPLAY_INGREDIENTS_PROMPT['prompt'].format(self.get_dict_to_str_joined(args['recipe']['ingredients'], delim='\n'))
            elif prev_intent in ['open_domain_qa', 'deny', 'set_timer', 'chitchat', 'offense', 'legal_advice', 
                               'financial_advice', 'medical_advice', 'dangerous_task', 'personal_information', 
                               'suicide_attempt', 'subjective_qa']:
                prompt = SYSTEM_PROMPT['prompt'].format(args['user'])
            elif prev_intent in ['in_task_qa', 'show_ingredients']:
                steps_str = ', '.join([f"'{i+1}: {s}'" for i, s in enumerate(args['recipe']['steps'])])
                # recipe_info = f"title: {args['recipe']['title']}, description: {args['recipe']['description']}, ingredients: [{', '.join(args['recipe']['ingredients'])}], steps: [{steps_str}]"
                recipe_info = f"title: {args['recipe']['title']}, description: {args['recipe']['description']}, ingredients: [{self.get_dict_to_str_joined(args['recipe']['ingredients'])}], steps: [{steps_str}]"
                prompt = IN_TASK_SYSTEM_PROMPT['prompt'].format(args['step'], recipe_info, args['user'])
            elif prev_intent == 'repeat':
                prompt = SYSTEM_REPEAT_PROMPT['prompt'].format(args['bot'], args['user'])
        
        #print(f"\n*** prompt ***\n{prompt}\n***\n")

        if prompt is None:
            write_error(f'ERROR: {intent}')

        # response, used_tokens = chatgpt_api(prompt, model=model, temperature=temperature, max_retries=7)
        response, used_tokens = llm_api(prompt, model=model, temperature=temperature, max_retries=7)
            
        total_used_tokens[useapi] += used_tokens
        if response is None:
            write_error(f'ERROR: {prompt}')
            return None, total_used_tokens, None, prompt

        if json_format:
            try:
                response = json.loads(response)
            except:
                prompt = "fix the json below, expected format is {}, give only the correct json in your response nothing else:\n{}".format(json_format, response)
                # response, used_tokens = chatgpt_api(prompt, model='gpt-4', max_retries=7)
                response, used_tokens = llm_api(prompt, model='gpt-4', temperature=temperature, max_retries=7, api = gpt_4)
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
            options = response.split('\n')
            options = [r for r in options if r != '']
            response = random.choice(options)
        
        state = {'search_results': search_results,
                 'golden_result_position': golden_result_position,
                 'intent': returned_intent,
                 'step': step,
                 'suggestions': suggestions,
                 'model': model}

        return response, total_used_tokens, state, prompt

    def generate_conversation(self, task, max_length=40):
        num_steps = len(task['steps'])

        path_generator = TaskPathGenerator()
        path = path_generator.generate_path(max_length=max_length, num_steps=num_steps)
        path_length = len(path)

        conversation = []
        prev_intent = None
        total_used_tokens = {'gpt-3.5-turbo': 0, 'gpt-4': 0}

        results_page = 1
        current_step = 0
        search_results = []
        query = task['query']
        golden_result_position = None
        prev_bot_response = ''
        prev_user_response = ''

        for i, intent in enumerate(path):
            if intent == 'end':
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
                                                           args={'recipe': task, 
                                                                 'query': query,
                                                                 'page': results_page, 
                                                                 'step': current_step,
                                                                 'results': search_results,
                                                                 'golden_result_position': golden_result_position,
                                                                 'bot': prev_bot_response,
                                                                 'user': prev_user_response})
            if response is None:
                return conversation, total_used_tokens, task['id'], path
            
            if isinstance(response, str):
                response = {'text': response}
            
            if intent == 'more_results':
                results_page += 1
            elif intent in ['next_step', 'done_step', 'acknowledge_step', 'begin_task', 'acknowledge_task']:
                current_step += 1
            elif intent in ['search_recipe', 'suggest_recipe']:
                current_step = 0
                results_page = 1
            elif intent in ['show_results', 'show_suggestions'] and len(response['recipe_ids']) == 0:
                intent = 'no_results'

            intent = state['intent']
            prev_intent = intent
            golden_result_position = state['golden_result_position']
            if state['step'] != None:
                current_step = state['step']
            if state['suggestions'] != None:
                response['suggestions'] = state['suggestions']
            if state['search_results'] != None:
                search_results = state['search_results']
            if 'query' in response:
                query = response['query']

            response['role'] = role
            response['intent'] = intent
            response['model'] = state['model']
            response['prompt'] = prompt

            if intent in ['show_results', 'show_suggestions']:
                response['results'] = [r['id'] for r in search_results]
                response['results_str'] = '\n'.join([f"id: {j+1}, {d['title']}, {d['minutes']} minutes, rating: {d['rating']} ({d['ratingCount']}), {d['description']}" for j, d in enumerate(search_results)])
            elif intent in ['next_step', 'done_step', 'acknowledge_step', 'begin_task', 'acknowledge_task', 'goto_step']:
                response['step'] = current_step
            elif intent == 'select_i':
                response['selection'] = golden_result_position+1

            #print(response)
            conversation.append(response)

            if role == 'system':
                prev_bot_response = response['text']
            else:
                prev_user_response = response['text']
            
            total_used_tokens['gpt-3.5-turbo'] += used_tokens['gpt-3.5-turbo']
            total_used_tokens['gpt-4'] += used_tokens['gpt-4']
            
            if intent == 'no_results':
                break
        
        return conversation, total_used_tokens, task['id'], path
    
    
    def remove_urls(self, d) :
        ingrs = d['ingredients']
        ings_new = []
        for ing in ingrs :
            if "image" in ing:
                del ing['image']
            ings_new.append(ing)
        d['ingredients'] = ings_new

        steps = d['steps']
        steps_new = []
        for step in steps :
            if "image" in step :
                del step['image']
            if "video" in step :
                del step['video']
            steps_new.append(step)
        d['steps'] = steps_new

        return d



    def generate_conversations(self, limit=1):
        added_ids = set()

        '''
            uncomment following part only if you want to re-trigger and exclude the previously used seeds
        '''
        # with open("data/complete_conversations_llama_recipe.jsonl") as f:
        #     for line in f:
        #         d = json.loads(line.rstrip('\n'))
        #         added_ids.add(d['id'])
        
        
        
        recipes = []
        # get seed recipes 
        rel_path = "../../../"
        with open(f'{rel_path}data/recipe_seed_test_set.jsonl', 'r') as file:
            for line in file:
                d = json.loads(line)
                d = self.remove_urls(d)

                if d['id'] not in added_ids:
                    recipes.append(d)

        o = open(f'{rel_path}data/complete_conversations_llama_recipe.jsonl', 'a')
        total_used_tokens = {'gpt-3.5-turbo': 0, 'gpt-4': 0, useapi: 0}
        completed = 0
        
        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = []
            for recipe in recipes[:limit]:
                futures.append(executor.submit(self.generate_conversation, recipe))
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                conversation, used_tokens, recipe_id, path = future.result()
                with lock:
                    if len(conversation) > 0:
                        o.write(json.dumps({"id": recipe_id, "path": path, "conversation": conversation}) + "\n")
                        o.flush()
                total_used_tokens['gpt-3.5-turbo'] += used_tokens['gpt-3.5-turbo']
                total_used_tokens['gpt-4'] += used_tokens['gpt-4']
                completed += 1
        
        print(total_used_tokens)
        # estimated_cost = (total_used_tokens['gpt-3.5-turbo']/2*0.0015/1000 + total_used_tokens['gpt-3.5-turbo']/2*0.002/1000) + \
        #     (total_used_tokens['gpt-4']/2*0.03/1000 + total_used_tokens['gpt-4']/2*0.06/1000)
        # print("Estimated cost: ${:.2f}".format(estimated_cost))
        estimated_cost = (total_used_tokens[useapi]/2*0.9/1000000 + total_used_tokens[useapi]/2*1.8/1000000) + \
            (total_used_tokens[gpt_4]/2*0.03/1000 + total_used_tokens[gpt_4]/2*0.06/1000)
        print("Estimated cost: ${:.4f}".format(estimated_cost))
        estimate_cost_new_llm = (total_used_tokens[useapi]/2*0.7/1000000 + total_used_tokens[useapi]/2*0.9/1000000)
        print("Estimated cost of only new llm: ${:.4f}".format(estimate_cost_new_llm))

if __name__ == '__main__':
    generator = DataGenerator()
    # limit the number of conversations
    generator.generate_conversations(limit=10)

    