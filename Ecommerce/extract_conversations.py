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

def write_jsonl(file_path, entry):
    with open(file_path, 'a') as file:
        json.dump(entry, file)
        file.write('\n')



filename = "./data/complete_conversations_llama_test_100.jsonl"
extracted_file = "./data/extracted_ecom_conversations_llama_test_100.jsonl"
data = read_jsonl(filename)

for conversation in data :
    del conversation['aux_cart']
    del conversation['aux_compare']
    
    write_jsonl(extracted_file, conversation)
