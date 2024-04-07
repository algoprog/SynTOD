# Inference

We are trying to generate the dialog text which would be used to evaluate the performance of the large language model in task-oriented dialogue. 

## How to run
To run the script for inference, you can use the command as the following : 

```
python inference_script.py \
  --model [model_name]
  --output_file [output_file] \
  --test_file [test_file]
```

The script could be explained as the following :  

1. **model_name** : 
The fine-tuned model that would be used for inference. 
2. **output_file** : 
the output file that would contains pairs of groundtruth dialogue and generated dialogue. Usually, it would be stored in `data/[domain]/03_inference_pair/`, while `domain` could be either `recipe` or `ecommerce`.
3. **test_file** : 
The file contains groundtruth dialogues for the model to generate from and compare to.  Usually, it would be stored in `data/[domain]/02_oasst/`, while `domain` could be either `recipe` or `ecommerce`