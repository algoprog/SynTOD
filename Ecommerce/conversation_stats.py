import json
from constants import *
import matplotlib.pyplot as plt

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


extracted_file =  "./data/extracted_final_ecom_conversations.jsonl" # final_ecom_conversation extracted_conversations_final_r_2

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
    sorted_frequencies = [ freq/max_freq for freq in sorted_frequencies]

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

for path in data :
    conversation = path['conversation']
    num_utterances = len(conversation)
    utterence_lengths.append(num_utterances)
    total_tokens = 0
    gpt_4_tok = 0

    for utterence in conversation :
        intent = utterence['intent']
        model = utterence['model']
        if utterence['gpt-4'] > 0 :
            if intent in json_failure_intents :
                json_failure_intents[intent] +=1
            else :
                json_failure_intents[intent] = 1
        total_tokens += utterence['gtp_4_turbo'] + utterence['gpt-4']
        gpt_4_tok += utterence['gpt-4']

        if intent == intents.show_results :
            if len(utterence['product_ids']) in selected_results_stats :
                selected_results_stats[len(utterence['product_ids'])] +=1
            else :
                selected_results_stats[len(utterence['product_ids'])] = 1
        if intent in intents_counts :
            intents_counts[intent] +=1
        if intent in all_intents :
            all_intents[intent] += 1
        else :
            all_intents[intent] = 1
    

    tokens.append(total_tokens)
    gpt_4tokens.append(gpt_4_tok)


print(selected_results_stats)
print(sum(utterence_lengths)/len(data))
# print(tokens)
# print(gpt_4tokens)
# print(json_failure_intents)
# s = print_dict(json_failure_intents)
print(sum(utterence_lengths))
# print(f"total : {s}")

# print(intents_counts)

plot_states_frequency(all_intents)
