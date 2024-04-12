# Evaluation

This folder contains 2 evaluation scripts for state tracking and response relevance evaluation. For state tracking, we use the metrics such as intent accuracy, precision, recall, and f1 score with macro average and micro average. To measure the slot tagging performance, we use token-level slot precision, recall and f1 score. For response relevance evaluation, we include an example for evaluation using models that support the OpenAI inference API.

For state tracking, you can run the following:

```
python evaluation_states.py \
  --model [model name] \
  --eval_file [inference output jsonl file] \
  --output_dir [reports folder] \
  --domain [domain, recipe or ecommerce]
```

and for response relevance the following:

```
python evaluation_relevance.py \
  --eval_file [inference output jsonl file] \
  --output_filename [output text file that has a relevance label 0-2 in each line]
```
