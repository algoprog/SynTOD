import json
import collections
from transformers import AutoTokenizer, AutoModelForCausalLM
import numpy as np
from tqdm import tqdm
from collections import defaultdict
import argparse
tokenizer = None
misgen_conv = 0
misgen_flag = False
slot_types = {
    "query" : "slot", 
    "attributes_list" : "flatten_slot", 
    "selection" : "numerical", 
    "select_i": "numerical",
    "product_ids" : "numeric_list", 
    "product_name": "slot",
    "question" : "slot", 
    "topic":"slot", 
    "address" : "slot", 
    "list_of_products" : "numeric_list",
    "intent" : "intent"
}
def calculate_slots(ref, hyp, slot, types):
    if slot not in hyp:
        return 0.0, 0.0, 0.0
    if types == "slot":
        if slot == "address" and not isinstance(ref[slot], str): # special case for data processing
            ref_slot = ref[slot]['country']
        elif slot == "query" and ref[slot] is None:
            ref_slot = ""
        else:
            ref_slot = ref[slot]
        ref_token = tokenizer.encode(ref_slot)
        hyp_token = tokenizer.encode(hyp[slot] if slot in hyp else "")
        common = collections.Counter(ref_token) & collections.Counter(hyp_token)
        num_same = sum(common.values())
        if len(hyp_token) == 0:
            num_same = 0
        if num_same == 0:
            return 0.0, 0.0, 0.0
        precision = 1.0 * num_same / len(hyp_token)
        recall = 1.0 * num_same / len(ref_token)
        # f1
        if precision + recall > 0.0:
            f1 = 2 * precision * recall / (precision + recall)
        else:
            f1 = 0.0
        return precision, recall, f1
    elif types == "numerical":
        assert int(ref[slot]) == ref[slot], f"{ref[slot]} is not int :{type(ref[slot])}"
        if slot not in hyp:
            return 0.0, 0.0, 0.0
        if ref[slot] == hyp[slot]:
            return 1.0,1.0,1.0
        else:
            return 0.0, 0.0, 0.0
    elif types == "numeric_list":
        if slot == "list_of_products" and len(ref[slot]) > 0 and not isinstance(ref[slot][0], str):
            ref_slot = [item["title"] for item in ref[slot]]
        else:
            ref_slot = ref[slot]
        num_same = len(set(ref_slot) & set(hyp[slot]))
        if len(ref[slot]) == 0 or len(hyp[slot]) == 0:
            return 0.0, 0.0, 0.0
        precision = 1.0 * num_same / len(hyp[slot])
        recall = 1.0 * num_same / len(ref[slot])
        if precision + recall > 0.0:
            f1 = 2 * precision * recall / (precision + recall)
        else:
            f1 = 0.0
        return precision, recall, f1
    elif types == "flatten_slot":
        try:
            ref_slots = set([str(list(item.keys())[0]) + " : " + str(list(item.values())[0]) for item in ref[slot]])
            hyp_slots = set([str(list(item.keys())[0]) + " : " + str(list(item.values())[0]) for item in hyp[slot]])
        except:
            global misgen_flag
            misgen_flag = True
            print(ref)
            print(hyp)
            print()
            return 0.0, 0.0, 0.0
        num_same = len(ref_slots & hyp_slots)
        if len(hyp_slots) == 0 or len(ref_slots) == 0:
            return 0.0, 0.0, 0.0
        precision = 1.0 * num_same / len(hyp_slots)
        recall = 1.0 * num_same / len(ref_slots)
        if precision + recall > 0.0:
            f1 = 2 * precision * recall / (precision + recall)
        else:
            f1 = 0.0
        return precision, recall, f1

def calculate_metrics(ref, hyp):
    metrics = []
    for key,value in ref.items():
        if slot_types[key] == "intent":
            continue
        metrics.append(calculate_slots(ref, hyp, key, slot_types[key]))
    precisions = []
    recalls = []
    f1s = []
    for precision, recall, f1 in metrics:
        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)

    return np.mean(precisions), np.mean(recalls), np.mean(f1s) 

      
    
if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default='kimmypracha/llama-marunachef-v1-c1-a100-940')
    parser.add_argument("--eval_file",default="fine_tuned_generated_output_a100.jsonl")
    parser.add_argument("--output_file",default="slot_metrics_class.json")
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    with open(args.eval_file, "r") as f:
        precisions = defaultdict(list)
        recalls = defaultdict(list)
        f1s = defaultdict(list)
        intent_count = defaultdict(int)
        macro_acc = []
        micro_acc = []
        mp = defaultdict(list)
        mr = defaultdict(list)
        mf = defaultdict(list)
        global_intent_pred_precision = defaultdict(list)
        global_intent_pred_recall = defaultdict(list)
        global_intent_pred_f1 = defaultdict(list)
        micro_pred = defaultdict(list)
        micro_true = defaultdict(list)
        for line in tqdm(f.readlines()):
            misgen_flag = False
            obj = json.loads(line)
            ground_dialog = obj['ground_text']
            generated_dialog = obj['generated_text']
            generated_text = generated_dialog.split('###')[0] + '###'
            mac_acc = 0
            mac_cnt = 0
            pb = defaultdict(list)
            rb = defaultdict(list)
            fb = defaultdict(list)
            dialog_intent_pred = defaultdict(list)
            dialog_intent_true = defaultdict(list)
            for ref, hyp in zip(ground_dialog.split('###')[1:], generated_dialog.split('###')[1:]):
                # print(hyp)
                if ref.split(':')[0].strip() == 'HUMAN':
                    ref_slots = json.loads(ref.split('##')[1].strip())
                    try:
                        hyp_slots = json.loads(hyp.split('##')[1].strip())
                    except:
                        hyp_slots = {}
                    if "intent" in ref_slots:
                        intent_count[ref_slots["intent"]] += 1
                    if "intent" in hyp_slots:
                        acc = 1 if hyp_slots["intent"] == ref_slots["intent"] else 0
                        mac_acc += acc
                        mac_cnt += 1
                        micro_acc.append(acc)
                        dialog_intent_pred[hyp_slots["intent"]].append(acc)
                        dialog_intent_true[ref_slots["intent"]].append(acc)
                        micro_pred[hyp_slots["intent"]].append(acc)
                        micro_true[ref_slots["intent"]].append(acc)
                    elif "intent" in ref_slots:
                        acc = 0
                        mac_acc += acc
                        mac_cnt += 1
                        micro_acc.append(acc)
                        dialog_intent_pred["NONE"].append(acc)
                        dialog_intent_true[ref_slots["intent"]].append(acc)
                        micro_pred["NONE"].append(acc)
                        micro_true[ref_slots["intent"]].append(acc)
                    if len(ref_slots) > 1:
                        precision, recall, f1 = calculate_metrics(ref_slots, hyp_slots)
                        pb[ref_slots["intent"]].append(precision)
                        rb[ref_slots["intent"]].append(recall)
                        fb[ref_slots["intent"]].append(f1)

                    # if(abs(precision - recall) > 0.00001):
                    #     print(precision, recall)
            if mac_cnt > 0:
                macro_acc.append(mac_acc/mac_cnt)
            for k in pb:
                precisions[k]+= pb[k]
                if len(pb[k]) > 0:
                    mp[k].append(sum(pb[k])/len(pb[k]))
            for k in rb:
                recalls[k] += rb[k]
                if len(rb) > 0:
                    mr[k].append(sum(rb[k])/len(rb[k]))
            for k in fb:
                f1s[k] += fb[k]
                if len(fb[k]) > 0:
                    mf[k].append(sum(fb[k])/len(fb[k]))

            for k in dialog_intent_true.keys():
                pres = sum(dialog_intent_pred[k])/len(dialog_intent_pred[k]) if len(dialog_intent_pred[k]) > 0.0 else 0.0
                rec = sum(dialog_intent_true[k])/len(dialog_intent_true[k])
                if pres + rec > 0.0 :
                    f1 = 2 * pres * rec / (pres + rec)
                else:
                    f1 = 0.0
                global_intent_pred_precision[k].append(pres)
                global_intent_pred_recall[k].append(rec)
                global_intent_pred_f1[k].append(f1)
            if misgen_flag:
                misgen_conv += 1


            
            

    with open(args.output_file, "w") as f:
        # macro_data = {"intent_accuracy" : sum(macro_acc)/len(macro_acc), "precision"  : sum(mp)/len(mp), "recall" : sum(mr)/len(mr), "f1" : sum(mf)/len(mf)}
        # micro_data = {"intent_accuracy" : sum(micro_acc)/len(micro_acc), "precision" : np.array(precisions).mean(), "recall" : np.array(recalls).mean(), "f1" : np.array(f1s).mean()}
        macro_data = {}
        micro_data = {}
        macro_intent = {}
        micro_intent = {}
        for k in mp.keys():
            macro_data[k] = {"precision" : np.mean(mp[k]), "recall" : np.mean(mr[k]), "f1" : np.mean(mf[k])}
            micro_data[k] = {"precision" : np.mean(precisions[k]), "recall" : np.mean(recalls[k]), "f1": np.mean(f1s[k])}
        for k in micro_true.keys():
            macro_intent[k] = {"precision" : np.mean(global_intent_pred_precision[k]), "recall" : np.mean(global_intent_pred_recall[k]), "f1" : np.mean(global_intent_pred_f1[k])}
            micro_intent[k] = {"precision" : np.mean(micro_pred[k]), "recall" : np.mean(micro_true[k])}
            p = micro_intent[k]["precision"]
            r = micro_intent[k]["recall"]
            if p + r > 0.0:
                micro_intent[k]["f1"] = 2*p*r/(p+r)
            else:
                micro_intent[k]["f1"] = 0.0
        f.write(json.dumps({"slot_tagging" : {"macro_average" : macro_data, "micro_average" : micro_data},
                            "intent" : {"macro_accuracy" : np.mean(macro_acc), "micro_accuracy" : np.mean(micro_acc),
                            "macro_stats" : macro_intent, "micro_stats" : micro_intent}, "intent_count" : intent_count}))
    print()
    print("MISGEN:", misgen_conv)

