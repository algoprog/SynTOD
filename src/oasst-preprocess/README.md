# Preprocessing

In this preprocessing process, we are trying to convert the data in the conversation format to a single text in oasst format in the jsonl. Here are the example.

```
{"text" : [the string of the whole dialogue]}
```

## How to run the script
To preprocess the initial data to the oasst format, you can run the command as the following: 

```
python convert_to_oasst.py \
    --output_file [output_file] \
    --seed_file [seed_file] \
    --conversation_file [conversation_file] \
    --mode [mode]
```

description : 

1. **output_file** : 
    the file path for the data in oasst format. Usually, it would be in the folder `data/[domain]/02_oasst/`, while `domain` is either `recipe` or `ecommmerce`
2. **seed_file** : 
    the file path for the recipe seed if the `domain` is `recipe`, otherwise this would be ignored. Generally, this file would be belonged to the folder `data/[domain]/00_seed/`.
3. **conversation_file** : 
    the file path for the conversation data in the original format (not the oasst format). Generally, this file belongs to the folder `data/[domain]/01_initial/`
4. **mode** : 
    the domain of the data we want to convert, it's either `recipe` or `ecommerce`
 