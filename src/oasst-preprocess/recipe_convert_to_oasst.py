import json
import random

random.seed(43)

o_train = open('train_nograph_v8.jsonl', 'w+')

intents_list = [
    # Recipe Related
    'search_recipe', 'suggest_recipe', 'more_results', 'select', 'show_ingredients',

    # Task Management
    'begin', 'next_step', 'goto_step', 'finish',
    # 'repeat',
    
    # Question-Answering
    'open_domain_qa', 'in_task_qa', 
    # 'subjective_qa', 
    
    # Inappropriate
    # 'financial_advice', 'medical_advice', 'legal_advice', 'offense', 'dangerous_task',
    
    # Miscellaneous
    'chitchat', 'set_timer'
]
intents = ', '.join(intents_list)

LLM_PROMPT = f"Conversation between human and AI that helps with recipes, allowed user intents are; {intents}:"
USER_PREFIX = " ### HUMAN: "
SYSTEM_PREFIX = " ### ASSISTANT: "
SUGGESTIONS_PREFIX = " ### SUGGESTIONS: "
RESULTS_PREFIX = " ### RESULTS: "
RECIPE_PREFIX = " ### RECIPE: "
SEPARATOR = " ## "
HISTORY_SIZE = -1

def get_metadata(utterance):
    metadata = {"intent": utterance['intent']} if 'intent' in utterance else {}
    if 'selection' in utterance:
        metadata['selection'] = utterance['selection']
    if 'query' in utterance:
        metadata['query'] = utterance['query']
    if 'recipe_name' in utterance:
        metadata['query'] = utterance['recipe_name']
    metadata = json.dumps(metadata)
    return metadata

data = []
max_len = 0

recipes = {}
with open("data/corpus.jsonl") as f:
    for line in f:
        d = json.loads(line.rstrip('\n'))
        recipes[d['id']] = d

conversations = []
with open("/project/pi_hzamani_umass_edu/chris/convtod/data/recipe_nograph_2.jsonl") as f:
    for line in f:
        d = json.loads(line.rstrip('\n'))
        conversations.append(d)
# print("ORG: ", len(conversations))
# # select 10% of conversations randomly and put them in separate list:
# #random.shuffle(conversations)
# num_conversations = len(conversations)
# num_conversations_ms_split = int(num_conversations * 0.1)
# num_conversations_ms_split += 1 if num_conversations_ms_split % 2 == 1 else 0
# conversations_ms_split = conversations[:num_conversations_ms_split]
# conversations = conversations[num_conversations_ms_split:]

# conversations_ms = conversations_ms_split[:len(conversations_ms_split)//2]
# conversations_ms_pool = conversations_ms_split[len(conversations_ms_split)//2:]

# conversations_ms_final = []
# pool_idx = 0

# for conv in conversations_ms:
#     final_conv = []
#     reached_injection_point = False
#     found_search_intent_pool = False
#     inject_idx = -1
#     cnt = 0
#     for i, utter in enumerate(conv['conversation']):
#         if 'intent' in utter and utter['intent'] in ['search_recipe', 'suggest_recipe']:
#             if i < len(conv['conversation'])//2:
#                 upper_bound = (len(conv['conversation'])//2) - 1
#                 inject_idx = i + random.randint(4 if upper_bound > 4 else 1, upper_bound)
#             else:
#                 upper_bound = len(conv['conversation']) - i - 1
#                 inject_idx = i + random.randint(4 if upper_bound > 4 else 1, upper_bound)
#             #print(f"inject_idx: {inject_idx}")
        
#         if i == inject_idx:
#             if ('role' in utter and utter['role'] == 'user') or ('user' in utter):
#                 reached_injection_point = True
#             else:
#                 inject_idx += 1

#         if not reached_injection_point:
#             final_conv.append(utter)
#             #print(f"adding (original) utterance: {utter['text']}")
#         else:
#             if pool_idx >= len(conversations_ms_pool):
#                 break
#             pool_conv = conversations_ms_pool[pool_idx]
#             pool_idx += 1
#             for utter_pool in pool_conv['conversation']:
#                 if 'intent' in utter_pool and utter_pool['intent'] in ['search_recipe', 'suggest_recipe']:
#                     found_search_intent_pool = True
#                 if found_search_intent_pool:
#                     #print(f"adding (pool) utterance: {utter_pool['text']}")
#                     final_conv.append(utter_pool)
#             break

#     if found_search_intent_pool:
#         conv['id'] = conversations_ms_pool[pool_idx-1]['id']         
    
#     conv['conversation'] = final_conv
#     conversations_ms_final.append(conv)

# o = open('temp.jsonl', 'w+')
# for utter in conversations_ms_final[0]['conversation']:
#     o.write(json.dumps(utter) + '\n')

# exit()
# print("LEN:", len(conversations_ms_final), len(conversations))
# conversations = conversations_ms_final + conversations
random.shuffle(conversations)

for d in conversations:
    recipe = recipes[d['id']]
    history = []
    current_step = 'not started'
    recipe_info = ''
    skip_next = False
    add_next = 0

    for i, utterance in enumerate(d['conversation']):
        if skip_next:
            skip_next = False
            continue
        if  'intent' in utterance and  utterance['intent'] in [
            "deny",
            "financial_advice",
            "legal_advice",
            "medical_advice",
            "offense",
            "repeat",
            "subjective_qa",
            "suicide_attempt",
            "personal_information",
            "dangerous_task"
        ]:
            skip_next = True
            continue

        metadata = ''
        utterance['text'] = utterance['text'].strip()

        if 'intent' in utterance and utterance['intent'] == 'option_selected':
            steps_str = ', '.join([f"'{i+1}: {s['text']}'" for i, s in enumerate(recipe['steps'])])
            ingredients = [item['ingredient'] for item in recipe['ingredients']]
            info = f"title: {recipe['title']}, description: {recipe['description']}, ingredients: [{', '.join(ingredients)}], steps: [{steps_str}]"
            recipe_info = f"{RECIPE_PREFIX}{info}"
            history.append(recipe_info)

        if 'step' in utterance:
            current_step = utterance['step']

        prefix = SYSTEM_PREFIX if utterance['role'] == 'system' else USER_PREFIX
        
        results_info = ''
        if 'intent' in utterance and utterance['intent'] in ['show_results', 'show_suggestions']:
            if utterance['intent'] == 'show_suggestions':
                suggestions_str = '\n'.join(utterance['suggestions'])
                results_info += f"{SUGGESTIONS_PREFIX}{suggestions_str}"
            metadata = json.dumps({"selected_ids": utterance['recipe_ids']})
            results_info += f"{RESULTS_PREFIX}{utterance['results_str']}"
        
        if i+1 < len(d['conversation']) and 'intent' in d['conversation'][i+1] and d['conversation'][i+1]['intent'] == 'select':
            metadata_str = f"{SEPARATOR}{metadata}" if metadata != '' else ''
            next_metadata = get_metadata(d['conversation'][i+1])
            history.append(f"{results_info}{prefix}{utterance['text']}{metadata_str}{USER_PREFIX}{d['conversation'][i+1]['text']}{SEPARATOR}{next_metadata}")
            skip_next = True
        else:
            history.append(f"{results_info}{prefix}{utterance['text']}")

        if utterance['role'] == 'user':
            metadata = get_metadata(utterance)
        
        if metadata != '':
            history[-1] += f"{SEPARATOR}{metadata}"
    
    text = ''.join(history)
    example = f"{LLM_PROMPT}{text}"
    data.append(example)
    max_len = max(max_len, len(example.split()))

for i, d in enumerate(data):
    o_train.write(json.dumps({"text": d}) + '\n')

print(max_len)