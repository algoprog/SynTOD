# Evaluation

This folder contains evaluation script which would also be used during the validation with macro-F1 intent accuracy on the validation set. During the evaluation, we use the metrics such as intent accuracy, precision, recall, and f1 score with macro average and micro average. Moreover, to measure the slot tagging performance, we use slot precision, recall and f1 score for token matching.

## Run the script

To run the script, you need to run the script in the following format

```
python evaluation_script.py \
  --model [model name] \
  --eval_file [inference pair] \
  --output_dir [reports folder] \
  --domain [domain]
```

For each argument, the descriptions are the following : 
1. **model name** : 

This would be the LLM we used for generating text in this task.

2. **inference pair** : 

This would be the data in the folder data/03_inference_pair. The format of the data would be 
```
{"groundtruth" : [groundtruth text], "generated" : "generated_text"}
```
This file would be used to compare the groundtruth intent and slot to evaluate the performance of the model.

3. **reports folder** : 

After the evaluation is done, the script will generate multiple figures of confusion matrix, json of metrics and details metrics for each intent in this folder. Usually it would be in the reports folder with the name of the model .

4. **domain** : 

a domain of the data we are evaluating. It is either `recipe` or `ecommerce`.

5. **type** : 
The type of approach used for data generation. The possible options are `graph` or `nograph`