import json
from tqdm import tqdm
if __name__ == "__main__" :
    writer = open("textgen/marunashop-gemini.jsonl", "w")

    with open("ecommerce/marunashop-v2-gemini.jsonl", "r") as f:
        precisions = []
        recalls = []
        f1s = []
        history = []
        dialog_id = 0
        for line in tqdm(f.readlines()):
            obj = json.loads(line)
            ground_dialog = obj['ground_text']
            generated_dialog = obj['generated_text']
            generated_text = generated_dialog.split('###')[0] + '###'
            for ref, hyp in zip(ground_dialog.split('###')[1:], generated_dialog.split('###')[1:]):
                # print(hyp)
                if ref.split(':')[0].strip() == 'HUMAN':
                    history.append({"role" : "user", "content" : ref.split(":",1)[1].split("##")[0].strip()})
                    history.append({"role" : "intent", "content" : ref.split("##")[1].strip()})
                elif ref.split(':')[0].strip() == 'RESULTS':
                    history.append({"role" : "retriever", "content" : ref.split(":",1)[1].strip()})
                elif ref.split(':')[0].strip() == 'SUGGESTIONS':
                    history.append({"role" : "suggestions", "content" : ref.split(":",1)[1].strip()})
                elif ref.split(':')[0].strip() == 'RECIPE':
                    history.append({"role" : "task", "content" : ref.split(":",1)[1].strip()})
                elif ref.split(':')[0].strip() == 'ASSISTANT':
                    new_obj = {"dialog_id" : dialog_id, "history" : history, "response" : {"role" : "system" , "content" : hyp.split(":",1)[1].strip()}, "ground_truth" : {"role" : "system", "content" : ref.split(":",1)[1].strip()}}
                    writer.write(json.dumps(new_obj) + "\n")
                    history.append({"role" : "system", "content" : ref.split(":",1)[1].strip()})
            dialog_id += 1
    writer.close()


