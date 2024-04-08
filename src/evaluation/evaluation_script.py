import json
import collections
from transformers import AutoTokenizer, AutoModelForCausalLM
import numpy as np
from tqdm import tqdm
from collections import defaultdict
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import os 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

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
ecommerce_intent = ['suggest_product', 'select_i', 'option_selected', 'add_to_cart',  'buy_cart', 'more_results', 'search_product', 'add_for_compare', 'open_domain_qa', 'show_cart', 'product_qa', 'acknowledge', 'remove_from_cart', 'repeat', 'generic_product_query', 'user_clarifies', 'delivery_address', 'show_attributes', 'chitchat', 'compare_products', 'remove_from_comparison']
recipe_intent = ['acknowledge_step', 'finish_task', 'done_step', 'acknowledge_task', 'option_selected', 'suggest_recipe', 'select_i', 'show_step', 'show_ingredients', 'show_suggestions', 'next_step', 'medical_advice', 'begin_task', 'search_recipe', 'more_results', 'in_task_qa', 'repeat', 'open_domain_qa', 'financial_advice', 'chitchat', 'subjective_qa', 'personal_information', 'offense', 'dangerous_task', 'legal_advice', 'set_timer', 'deny', 'goto_step', 'suicide_attempt']
nn = None
domain_intent = []

def helper_metrics(num_same, ref_len, hyp_len): 
    if hyp_len == 0 or ref_len == 0:
        return 0.0, 0.0, 0.0
    precision = 1.0 * num_same / hyp_len
    recall = 1.0 * num_same / ref_len
    if precision + recall > 0.0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0.0
    return precision, recall, f1
    
def calculate_slots(ref, hyp, slot, types):
    if slot not in hyp:
        return 0.0, 0.0, 0.0
    if types == "slot":
        if ref[slot] is None: 
            ref[slot] = ""
        if slot == "address" : # special case for data processing
            try:
                ref[slot] = ref[slot]['country'] if not isinstance(ref[slot], str) else ref[slot]
                hyp[slot] = hyp[slot]['country'] if not isinstance(hyp[slot], str) else hyp[slot]
            except:
                return 0.0, 0.0, 0.0
        elif slot == "query" and isinstance(ref[slot], list): # patch fix for suggestion
            ref[slot] = " ".join(ref[slot]) + " recipe"
        else:
            ref[slot] = ref[slot]
        try:
            ref_token = tokenizer.encode(ref[slot])
            hyp_token = tokenizer.encode(hyp[slot] if slot in hyp else "")
        except:
            return 0.0, 0.0, 0.0

        common = collections.Counter(ref_token) & collections.Counter(hyp_token)
        num_same = sum(common.values()) if len(hyp_token) !=0 else 0

        return helper_metrics(num_same, len(ref_token), len(hyp_token))

    elif types == "numerical":
        assert int(ref[slot]) == ref[slot], f"{ref[slot]} is not int :{type(ref[slot])}"
        if slot not in hyp:
            return 0.0, 0.0, 0.0
        return (1.0,1.0,1.0) if ref[slot] == hyp[slot] else (0.0,0.0,0.0)
    
    elif types == "numeric_list":
        if slot == "list_of_products" and len(ref[slot]) > 0 and not isinstance(ref[slot][0], str):
            ref_slot = [item["title"] for item in ref[slot]]
        else:
            ref_slot = ref[slot]

        num_same = len(set(ref_slot) & set(hyp[slot]))
        return helper_metrics(num_same, len(ref[slot]), len(hyp[slot]))

    elif types == "flatten_slot":
        ref_slots = set([str(list(item.keys())[0]) + " : " + str(list(item.values())[0]) for item in ref[slot]])
        hyp_slots = set([str(list(item.keys())[0]) + " : " + str(list(item.values())[0]) for item in hyp[slot]])
        num_same = len(ref_slots & hyp_slots)
        return helper_metrics(num_same, len(ref_slots), len(hyp_slots))
        

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

def flatten_list(array_list):
    return [item for nested_list in array_list for item in nested_list]

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues,
                          file_path='confusion_matrix.png',
                          ignore_none=True):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    fig, ax = plt.subplots(figsize=(18,20))
    if ignore_none:
        cm = cm[:-1, :-1]
        classes = classes[:-1]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        cm = np.nan_to_num(cm)
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    sns.heatmap(cm, annot=True, annot_kws={"fontsize":14}, fmt='.1f', ax=ax, cmap="YlGnBu")
    ax.set_title(title, size=18)
    ax.set_xlabel('Predicted label', size=16)
    ax.set_ylabel('True label', size=16)
    ax.xaxis.set_ticklabels(classes, rotation=90, fontsize=12)
    ax.yaxis.set_ticklabels(classes, rotation=0, fontsize=12)
    plt.show()
    fig.savefig(file_path)

def clean_intent(intent):
    merge_intent = {
        "acknowledge_task" : "begin_task",
        "done_step" : "next_step",
        "acknowledge_step" : "next_step",
    }
    global nn
    global domain_intent
    if (intent not in domain_intent):
        intent = nn.find_nearest(intent).replace(" ","_")
    if (intent in merge_intent):
        intent = merge_intent[intent]
    return intent

def clean_intent_list(intent_list):
    intent_list = [clean_intent(item) for item in intent_list]
    return intent_list

def ground_to_convlist(ground_text, data_type):
    history = []
    for ref in ground_text.split('###')[1:]:
        if ref.split(':')[0].strip() == 'HUMAN':
            history.append({"role" : "user", "content" : ref.split(":",1)[1].split("##")[0].strip()})
            history.append({"role" : "intent", "content" : ref.split("##")[1].strip()})
        elif ref.split(':')[0].strip() == 'RESULTS' and data_type == "graph":
            history.append({"role" : "retriever", "content" : ref.split(":",1)[1].strip()})
        elif ref.split(':')[0].strip() == 'SUGGESTIONS' and data_type == "graph":
            history.append({"role" : "suggestions", "content" : ref.split(":",1)[1].strip()})
        elif ref.split(':')[0].strip() == 'RECIPE' and data_type == "graph":
            history.append({"role" : "task", "content" : ref.split(":",1)[1].strip()})
        elif ref.split(':')[0].strip() == 'ASSISTANT':
            history.append({"role" : "system", "content" : ref.split(":",1)[1].strip()})
        else:
            assert False, f"ERROR: ref is {ref}"
    return history
    
class NearestNeighbor:
    def __init__(self, items, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.precompute(items)

    def precompute(self, items):
        items = [i.replace('_', ' ') for i in items]
        self.items = items
        self.embeddings = self.model.encode(items, convert_to_tensor=True)

    def find_nearest(self, query):
        if self.items is None or self.embeddings is None:
            raise Exception("You must run precompute() before find_nearest()")

        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cos_scores = cosine_similarity(
            query_embedding.cpu().reshape(1, -1), 
            self.embeddings.cpu().reshape(len(self.items), -1)
        )

        top_result = np.argmax(cos_scores)
        return self.items[top_result]

class MetricEvaluator:
    def __init__(self, evaluator_name = "default-eval"):
        self.name = evaluator_name
        self.intent_pred = []
        self.intent_true = []
        self.slot = defaultdict(list)
        self.current_intent_pred = []
        self.current_intent_true = []
        self.current_slot = defaultdict(list)
        self.omitted_intent = [
            "deny",
            "financial_advice",
            "legal_advice",
            "medical_advice",
            "offense",
            "repeat",
            "subjective_qa",
            "suicide_attempt",
            "personal_information"
        ]
        self.is_started = False

    def start_conversation(self):
        self.current_intent_pred = []
        self.current_intent_true = []
        self.current_slot = defaultdict(list)
        self.is_started = True

    def add_intent(self, ref_intent, hyp_intent):
        assert self.is_started, "The conversation has not started yet."
        cleaned_hyp_intent = clean_intent(hyp_intent)
        cleaned_ref_intent = clean_intent(ref_intent)
        if cleaned_ref_intent not in self.omitted_intent and cleaned_hyp_intent not in self.omitted_intent:
            self.current_intent_pred.append(cleaned_hyp_intent)
            self.current_intent_true.append(cleaned_ref_intent)

    def add_slot(self, intent, precision, recall, f1):
        assert self.is_started, "The conversation has not started yet."
        cleaned_intent = clean_intent(intent)
        if cleaned_intent not in self.omitted_intent:
            self.current_slot[cleaned_intent].append((precision, recall, f1))

    def end_conversation(self):
        self.intent_pred.append(self.current_intent_pred)
        self.intent_true.append(self.current_intent_true)
        for intent, values in self.current_slot.items():
            self.slot[intent].append(values)
        self.is_started = False
    
    def get_confusion_matrix(self, normalize=True):
        flatten_y_pred = flatten_list(self.intent_pred)
        flatten_y_true = flatten_list(self.intent_true)
        classes = [item for item in sorted(list(set(flatten_y_true + flatten_y_pred))) if item != "NONE"]
        classes += ["NONE"]
        y_pred = np.array(flatten_y_pred)
        y_true = np.array(flatten_y_true)
        cm = np.nan_to_num(confusion_matrix(y_true, y_pred, labels=classes))
        return cm, classes

    def _get_precision_recall_table(self):
        precision_table = defaultdict(list)
        recall_table = defaultdict(list)
        for true, pred in zip(self.intent_true, self.intent_pred):
            temp_precision_table = defaultdict(list)
            temp_recall_table = defaultdict(list)
            for item_true, item_pred in zip(true, pred):
                temp_precision_table[item_pred].append(1 if item_true == item_pred else 0)
                temp_recall_table[item_true].append(1 if item_true == item_pred else 0)
            for key, value in temp_precision_table.items():
                precision_table[key].append(np.mean(value))
            for key, value in temp_recall_table.items():
                recall_table[key].append(np.mean(value))
        return precision_table, recall_table

    def get_intent_metrics(self):
        metrics = {}
        details = {}
        flatten_y_pred = flatten_list(self.intent_pred)
        flatten_y_true = flatten_list(self.intent_true)
        acc_list = np.array([accuracy_score(true, pred) for true, pred in zip(self.intent_true, self.intent_pred) if len(true)> 0])
        # Generate precision and recall for each intent
        precision_table, recall_table = self._get_precision_recall_table()
        
        ## TODO: REVIEW ON THIS PART ##
        precision = np.mean([np.mean(item_list) for item_list in precision_table.values()])
        recall = np.mean([np.mean(item_list) for item_list in recall_table.values()])
        metrics["macro_intent_accuracy"] = acc_list.mean()
        metrics["macro_intent_precision"] = precision
        metrics["macro_intent_recall"] = recall
        metrics["macro_intent_f1"] = (2*precision*recall)/(precision + recall) if precision + recall > 0.0 else 0.0
        ## REVIEW END ##

        metrics["micro_intent_accuracy"] = accuracy_score(flatten_y_true, flatten_y_pred)
        metrics["micro_intent_precision"] = precision_score(flatten_y_true, flatten_y_pred, average="micro")
        metrics["micro_intent_recall"] = recall_score(flatten_y_true, flatten_y_pred, average="micro")
        metrics["micro_intent_f1"] = f1_score(flatten_y_true, flatten_y_pred, average="micro")

        ## TODO : DETAIL 
        macro_details = defaultdict(dict)
        for key, value in precision_table.items():
            macro_details[key]["precision"] = np.mean(value)
        for key, value in recall_table.items():
            macro_details[key]["recall"] = np.mean(value)
            if "precision" in macro_details[key]:
                p = macro_details[key]["precision"]
                r = macro_details[key]["recall"]
                macro_details[key]["f1"] = (2*p*r)/(p+r) if p + r > 0.0 else 0.0
        micro_details = defaultdict(dict)
        classes = list(set(flatten_y_pred + flatten_y_true))
        micro_intent_precision = precision_score(flatten_y_true, flatten_y_pred, labels=classes, average=None)
        micro_intent_recall = recall_score(flatten_y_true, flatten_y_pred, labels=classes, average=None)
        micro_intent_f1 = f1_score(flatten_y_true, flatten_y_pred, labels=classes, average=None)
        for i, intent in enumerate(classes):
            micro_details[intent]["precision"] = micro_intent_precision[i]
            micro_details[intent]["recall"] = micro_intent_recall[i]
            micro_details[intent]["f1"] = micro_intent_f1[i]
        details = {"macro" : macro_details, "micro" : micro_details}
        return metrics, details
    
    def get_slot_metrics(self):
        metrics = {}
        micro_list = []
        macro_list = []
        micro_details = defaultdict(dict)
        macro_details = defaultdict(dict)
        for key, values in self.slot.items():
            micro_precision, micro_recall, micro_f1 = np.mean(flatten_list(values), axis=0)
            macro_precision, macro_recall, macro_f1 = np.mean([np.mean(list_item, axis=0) for list_item in values], axis=0)
            micro_list += flatten_list(values)
            macro_list.append((macro_precision, macro_recall, macro_f1))
            micro_details[key] = {
                "precision" : micro_precision,
                "recall"    : micro_recall,
                "f1"        : micro_f1
            }
            macro_details[key] = {
                "precision" : macro_precision,
                "recall"    : macro_recall,
                "f1"        : macro_f1
            }
        details = {"macro" : macro_details, "micro": micro_details}
        macro_metrics = np.mean(macro_list, axis=0)
        if len(macro_list) > 0: 
            metrics["macro_slot_tagging_precision"] = macro_metrics[0]
            metrics["macro_slot_tagging_recall"] = macro_metrics[1]
            metrics["macro_slot_tagging_f1"] = macro_metrics[2]

        micro_metrics = np.mean(micro_list, axis=0)
        if len(micro_list) > 0:
            metrics["micro_slot_tagging_precision"] = micro_metrics[0]
            metrics["micro_slot_tagging_recall"] = micro_metrics[1]
            metrics["micro_slot_tagging_f1"] = micro_metrics[2]

        return metrics, details

class BatchEvaluator:
    def __init__(self, length_params = [10000]):
        self.length_params = length_params
        self.evaluators = [MetricEvaluator(f"length-{length}") if length >= 0 else MetricEvaluator("all") for length in length_params]
        self.current_length = 0

    def start_conversation(self):
        self.current_length = 0
        for evaluator in self.evaluators:
            evaluator.start_conversation()

    def add_intent(self, ref_intent, hyp_intent):
        for evaluator, length in zip(self.evaluators, self.length_params):
            if self.current_length == length or length < 0: 
                evaluator.add_intent(ref_intent, hyp_intent)

    def add_slot(self, intent, precision, recall, f1):
        for evaluator, length in zip(self.evaluators, self.length_params):
            if self.current_length == length or length < 0: 
                evaluator.add_slot(intent, precision, recall, f1)

    def step(self):
        self.current_length += 1

    def end_conversation(self):
        for evaluator in self.evaluators:
            evaluator.end_conversation()
    def dispatch(self):
        return self.evaluators
    


if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("--model")
    parser.add_argument("--eval_file")
    parser.add_argument("--output_dir")
    parser.add_argument("--domain")
    parser.add_argument("--type")
    args = parser.parse_args()
    if args.domain == "recipe":
        domain_intent = recipe_intent
        nn = NearestNeighbor(recipe_intent)
    else:
        domain_intent = ecommerce_intent
        nn = NearestNeighbor(ecommerce_intent)
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    batch_evaluator = BatchEvaluator([-1, 4, 8, 16, 20, 24, 28])
    writer = open(args.output_dir + "text_response.jsonl", "w")
    token_writer = open(args.output_dir + "token_length.jsonl", "w") 
    with open(args.eval_file, "r") as f:
        dialog_id = 0
        for line in tqdm(f.readlines()):
            obj = json.loads(line)
            ground_dialog = obj['ground_text']
            generated_dialog = obj['generated_text']
            ground_token_count = len(tokenizer.encode(ground_dialog))
            generated_token_count = len(tokenizer.encode(generated_dialog))
            if ground_token_count > 4096: 
                dialog_id += 1
                continue
            source = obj["source"]
            token_writer.write(json.dumps({"ground_token" : ground_token_count, "generated_token" : generated_token_count, "source": source, "ground_text" : ground_dialog, "generated_text" : generated_dialog}) + "\n")
            generated_text = generated_dialog.split('###')[0] + '###'
            turn_cnt = 0
            ref_history = ground_to_convlist(ground_dialog, args.type)
            hyp_history = ground_to_convlist(generated_dialog, args.type)
            batch_evaluator.start_conversation()
            for ref, hyp in zip(ref_history, hyp_history):
                if ref["role"] == "intent":
                    ref_slots = json.loads(ref["content"])
                    try:
                        hyp_slots = json.loads(hyp["content"])
                    except:
                        hyp_slots = {}
                    if "intent" in ref_slots and "intent" in hyp_slots:
                        batch_evaluator.add_intent(ref_slots["intent"], hyp_slots["intent"])
                    elif "intent" in ref_slots:
                        batch_evaluator.add_intent(ref_slots["intent"], "NONE")
                    elif "intent" in hyp_slots:
                        batch_evaluator.add_intent("NONE", hyp_slots["intent"])
                    if len(ref_slots) > 1:
                        precision, recall, f1 = calculate_metrics(ref_slots, hyp_slots)
                        batch_evaluator.add_slot(ref_slots["intent"], precision, recall, f1)
                elif ref["role"] == "system" or ref["role"] == "user":
                    batch_evaluator.step() 
                    if ref["role"] == "system": 
                        new_obj = {"dialog_id" : dialog_id, "source" : source,"history" : ref_history[:turn_cnt], "response" : hyp, "ground_truth" : ref}
                        writer.write(json.dumps(new_obj)+"\n")
                turn_cnt += 1
            batch_evaluator.end_conversation()
            dialog_id += 1  
    writer.close()


    for evaluator in batch_evaluator.dispatch():
        with open(args.output_dir + "metrics_" + evaluator.name + ".jsonl", "w") as f:
            cm, classes = evaluator.get_confusion_matrix()
            plot_confusion_matrix(cm, classes=classes, normalize=True ,file_path=args.output_dir + "confusion_matrix_" + evaluator.name + ".png" )
            intent_metrics, intent_details = evaluator.get_intent_metrics()
            slot_metrics, slot_details = evaluator.get_slot_metrics()
            f.write(json.dumps({"intent_metrics" : intent_metrics, "slot_metrics" : slot_metrics, "intent_details" : intent_details, "slot_details" : slot_details}))






