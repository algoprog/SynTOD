import json
from constants import *
import matplotlib.pyplot as plt
import statistics

# conversations_file = inventory_file # "data/conversations_final.jsonl" 

def print_dict(dict) :
    s = 0
    print("{")
    for key in dict :
        print(f"{key} : {dict[key]} , ")
        s+=dict[key]
    print("}")
    return s

def read_jsonl(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            json_obj = json.loads(line)
            data.append(json_obj)
    return data


# extracted_file =  "./data/extracted_final_ecom_conversations.jsonl" # final_ecom_conversation extracted_conversations_final_r_2
extracted_file = "data/ecom_conversations_test_set.jsonl"
# extracted_file = "data/recipe_conversations_test_set.jsonl"
# extracted_file = "data/recipe_conversations_v6.jsonl"


def get_data_source(filename) :
    if 'llama' in filename :
        return 'llama'
    elif 'mistral' in filename :
        return 'mistral'
    elif 'gemini' in filename :
        return 'gemini'
    

def create_combined_testset() :

    test_set_files_ecommerce = ['data/ecom_conversations_test_llama_short_desc_completed_entire.jsonl', 
                      'data/ecom_conversations_test_mistral_short_desc_completed_entire.jsonl', 
                      'data/ecom_conversations_test_gemini_completed.jsonl']
    test_set_files_recipe = ['data/complete_conversations_llama_recipe.jsonl', 
                        'data/conversations_mistral_recipe.jsonl', 
                        'data/conversations_gemini_recipe.jsonl']
    test_set_files = test_set_files_recipe
    # final_test_set_file = "data/ecom_conversations_test_set.jsonl"
    final_test_set_file = "data/recipe_conversations_test_set.jsonl"
    data = []
    for test_file in test_set_files :
        
        with open(test_file, 'r') as file:
            for line in file:
                json_obj = json.loads(line)
                json_obj['data_source'] = get_data_source(test_file)
                data.append(json_obj)
    
    with open(final_test_set_file, 'a') as file:
        for d in data:
            file.write(json.dumps(d))
            file.write("\n")



def build_histogram(data, inv_file = extracted_file) :

    # data = get_inventory_stats(inv_file=inv_file)

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
    plt.savefig(f"{inv_file.split('.')[0]}_intents_statistics.png")    

def plot_states_frequency(string_counts):
    
    strings = list(string_counts.keys())
    frequencies = list(string_counts.values())

    sorted_indices = sorted(range(len(frequencies)), key=lambda i: frequencies[i], reverse=True)
    sorted_strings = [strings[i] for i in sorted_indices]
    sorted_frequencies = [frequencies[i] for i in sorted_indices]
    sum_freq = sum(sorted_frequencies)
    max_freq = max(sorted_frequencies)
    sorted_frequencies = [ 100*(freq/max_freq) for freq in sorted_frequencies]

    plt.figure(figsize=(20, 10))
    plt.bar(sorted_strings, sorted_frequencies)
    plt.xlabel('Intents')
    plt.ylabel('Frequency')
    plt.title('Frequency of intents')
    plt.xticks(rotation='vertical')
    plt.subplots_adjust(bottom=0.25)
    plt.show()
    plt.savefig(f"plot_intents_frequency_training_conversations_ecom.png")



data = read_jsonl(extracted_file)

selected_results_stats = {
    1 : 0,
    2: 0,
    3: 0
}

# json_failure_intents = {}
json_failure_intents = {
# intents.suggest_product : 11 , 
# intents.show_results : 26 , 
# intents.shown_cart : 6 , 
# intents.search_product : 5 , 
# intents.show_comparison : 2 , 
# intents.open_domain_qa : 2 , 
# intents.user_clarifies : 9 , 
}

intents_counts = {
    intents.suggest_product : 0 , 
    intents.show_results : 0 , 
    intents.shown_cart : 0 , 
    intents.search_product : 0 , 
    intents.show_comparison : 0, 
    intents.open_domain_qa : 0 , 
    intents.user_clarifies : 0 ,
}
all_intents = {}

utterence_lengths = []
tokens = []
gpt_4tokens = []
user_tokens = []
system_tokens = []

for path in data :
    conversation = path['conversation']
    num_utterances = len(conversation)
    utterence_lengths.append(num_utterances)
    total_tokens = 0
    gpt_4_tok = 0

    for utterence in conversation :
        intent = utterence['intent']
        model = utterence['model']
        text_or_question = 'text'
        if 'question' in utterence.keys():
            text_or_question = 'question'
        if utterence['role'] == 'user' :
            # user_tokens.append(utterence['gtp_4_turbo'] + utterence['gpt-4'])
            user_tokens.append(len(utterence[text_or_question].split(" ")))
        else:
            # system_tokens.append(utterence['gtp_4_turbo'] + utterence['gpt-4'])
            system_tokens.append(len(utterence[text_or_question].split(" ")))
        # if utterence['gpt-4'] > 0 :
        #     if intent in json_failure_intents :
        #         json_failure_intents[intent] +=1
        #     else :
        #         json_failure_intents[intent] = 1

        total_tokens += utterence['gtp_4_turbo'] + utterence['gpt-4']
        # gpt_4_tok += utterence['gpt-4']

        # total_tokens += len(str(utterence).split(" "))

        # if intent == intents.show_results :
        #     if len(utterence['product_ids']) in selected_results_stats :
        #         selected_results_stats[len(utterence['product_ids'])] +=1
        #     else :
        #         selected_results_stats[len(utterence['product_ids'])] = 1
        # if intent in intents_counts :
        #     intents_counts[intent] +=1
        # if intent in all_intents :
        #     all_intents[intent] += 1
        # else :
        #     all_intents[intent] = 1
    

    tokens.append(total_tokens)
    gpt_4tokens.append(gpt_4_tok)


# print(selected_results_stats)
print(f"file: {extracted_file}")
print(f"Number conversations: {len(data)}")
# print(sum(utterence_lengths)/len(data))
# print(tokens/len(data))

print(f"Average conversation length: {statistics.mean(utterence_lengths)}")
print(f"Std. conversation length: {statistics.stdev(utterence_lengths)}")

print(f"Average conversation tokens: {statistics.mean(tokens)}") # tokens used in a conversation
print(f"Std. conversation tokens: {statistics.stdev(tokens)}")

print(f"Average user tokens: {statistics.mean(user_tokens)}")
print(f"Std. user tokens: {statistics.stdev(user_tokens)}")

print(f"Average system tokens: {statistics.mean(system_tokens)}")
print(f"Std. system tokens: {statistics.stdev(system_tokens)}")

# print(gpt_4tokens)
# print(json_failure_intents)
# s = print_dict(json_failure_intents)
print(sum(utterence_lengths))
# print(f"total : {s}")

# # print(intents_counts)

# plot_states_frequency(all_intents)


# create_combined_testset()
