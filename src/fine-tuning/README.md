# Fine tuning 
We fine-tuned the LLM with QLoRA approach. The scripts that we used is in `fine-tune.sh`. Here are the parameters that we changed during the experiment. 

1. **model_name_or_path** : 
The model that we will use to fine-tune.
2. **output_dir** :  
the output folder for the adapter model, which would be used to merge later on with the base model. Therefore, the output folder can be anywhere.
3. **lora_r** and **lora_alpha**: 
These two hyperparameters are the hyperparameters we did experiments with.
4. **dataset** : 
the path of the data we will fine-tune on the LLM. The format of the data would be in oasst format, which is the single text prompt containing the whole conversation.
5. **run_name** : 
The name of run when we save the log in wandb during fine-tuning.

## How to run the script 

First configure the arguments that we specified above. And then run the following command. 

```
sh fine-tune.sh
```

and then, merge the model with the following script
```
sh merge.sh
```

Note : There might be an issue regarding uploading the model to huggingface with those script, you can use the huggingface-cli to upload the model directly after that on the merged model. 