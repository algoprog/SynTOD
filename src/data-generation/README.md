## data-generation ##
This part proides code for generating synthetic conversations. We have provided a framework on how to generate conversations using a transition graph in two domains. 
Because of the nature of random walk and non-zero temperaure used in prompting LLMs the output might different on multiple runs of these script.


## Ecommerce ##

This folder contains scripts for generating Ecommerce conversations.
You will need to change the API key values and use the appropriate file names before running any script.


Following important files are present in this folder:
1. constants.py: Defines all the intents which are nodes of a transition, also defines all seed files and global constants.
2. ecom_datagen_with_seeds.py: Script to generate conversations using only gpt-4 and gpt-4-1106-preview LLMs. The script uses a transition graph to create random walks and aligns sampled seeds as per the random walk generated and generates conversations by prompting gpt-4 and gpt-4-1106-preview LLMs using the information from seeds, context and appropriate prompt. Read the script to look for places to provide appropriate api key.
3. ecom_graph_multiple_llms.py: Script to generate conversations using multiple LLMs. The script uses a transition graph to create random walks and aligns sampled seeds as per the random walk generated and generates conversations by prompting an LLM using the information from seeds, context and appropriate prompt. Read the script to look for places to provide appropriate api key and to select required LLM. This script was used to create test data.
4. ecom_no_graph_conversation_generation.py: Script to generate conversations using a single prompt and few sampled product seeds.
Other files are just helper files which help in creating a product seed inventory, to get conversation statistics, or to visualize a graph, or to create a transition graph.

To run these files:
First change the working directory and then run them after updating the required fields.
```
cd src\data-generation\Ecommerce\
python ecom_datagen_with_seeds.py
python ecom_graph_multiple_llms.py
python ecom_no_graph_conversation_generation.py

```



## Recipe ##

This folder contains scripts for generating Recipe conversations.
You will need to change the API key values and use the appropriate file names before running any script.


Following important files are present in this folder:

2. datagen.py: Script to generate conversations using only gpt-4 LLM. The script uses a transition graph to create random walks and generates conversations by prompting gpt-4 and gpt-4 turbo LLMs using the information from the seed, context and appropriate prompt. Read the script to look for places to provide appropriate api key.
3. ecom_graph_multiple_llms.py: Script to generate conversations using multiple LLMs. The script uses a transition graph to create random walks and generates conversations by prompting an LLM using the information from seeds, context and appropriate prompt. Read the script to look for places to provide appropriate api key and to select required LLM. This script was used to create test data.

Other files are just helper files  to create a transition graph, random path, define prompts, retriever.

To run these files:
First change the working directory and then run them after updating the required fields.
```
cd src\data-generation\Recipe\
python datagen.py
python datagen_multiple_llm.py

```

