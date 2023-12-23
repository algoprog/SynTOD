import json
import threading


lock = threading.Lock()


def read_jsonl(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            json_obj = json.loads(line)
            data.append(json_obj)
    return data


def visualize_conv(conversation, visualized_file) :

    with open(visualized_file, 'w') as file:
            # Write a line to the file
            file.write("This is a synthetic conversation.\n")

    for utterance in conversation :
        if 'text' in utterance :
            uttr = utterance['text']
        else :
            uttr = utterance['question']
        role = utterance['role']
        with open(visualized_file, 'a') as file:
            # Write a line to the file
            file.write(f"{role} : {uttr}")
            file.write("\n\n")


filename = "./data/extracted_conversations_final.jsonl"
data = read_jsonl(filename)


select_conversations = [18,19] # line 18 and 19

for conv_number in select_conversations :
    conv = data[conv_number]['conversation']
    visualized_file = f"./data/visualized_conversation_{conv_number}.txt"

    
    visualize_conv(conv, visualized_file)