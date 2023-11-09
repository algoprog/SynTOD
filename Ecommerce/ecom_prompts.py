# System prompts

START_PROMPT = {
    "prompt": "Your name is MarunaSalesAssociate. You are a taskbot developed by CIIR at UMass Amherst, that helps with selling products present in an inventory. Write an intro prompt to the user, don't use emojis.",
    "json_format": None
}

SHOW_RESULTS_PROMPT = {
    "prompt": """Imagine you are a taskbot assistant that helps with selling products present in an inventory. Given the following product results info for the query '{}':
results: [
 
{}
]
Generate a compelling response that presents the results in the most appealing order based on the provided information. Encourage the user to select a product for options like adding it to the cart, comparing, or making a purchase. Highlight only the key details to capture the user's interest, avoiding excessive details. If a result is not directly related to the query, don't include it. In case no relevant results are available, provide a friendly response and suggest the user try a different query.

Use this format in your response, the text should include your full taskbot response:

{{"text": ..., "product_ids": [...]}}""",

    "json_format": "{\"text\": ..., \"product_ids\": [...]}"
}

SHOW_MORE_RESULTS_PROMPT = {
    "prompt": """Imagine you are a taskbot assistant that helps with selling products present in an inventory and already provided some results for a product suggestion. Given the following next product results info for the query '{}':
results: [    
{}
]
Generate an engaging response that summarizes these additional results in the best order based on the presented info. Encourage the user to select a product for options like adding it to the cart, comparing, or making a purchase.  Mention only the most important info to attract the user, not all the details. If one result is not directly relevant to the query, don't include it. If no results are provided or no relevant results are in the given list, give an appropriate response and tell the user to try something else.

Use this format in your response, the text should include your full taskbot response:

{{"text": ..., "product_ids": [...]}}""",

    "json_format": "{\"text\": ..., \"product_ids\": [...]}"
}

FIND_SUGGESTIONS_PROMPT = {
    "prompt": "Imagine you are a taskbot assistant that helps with selling products present in an inventory. Give {} most popular product name suggestions for the query '{}', one in each line, no quotes or enumeration.",
    "json_format": None
}

OPTION_SELECTED_PROMPT = {
    "prompt": """Imagine you are a taskbot assistant that helps with selling products present in an inventory and the user just selected the following product: 

title: {}
description: {}

Generate a captivating system response and provide options for the user, such as viewing the product's attributes, adding it to the cart, purchasing it, or adding it for comparison. Please provide only the text of the response.""",
    
    "json_format": None
}

# STARTED_TASK_PROMPT = {
#     "prompt": """Imagine you are a taskbot that helps with recipes and the user just confirmed to start the recipe '{}' he already selected previously. Don't congratulate him for the choice. Write an engaging system response for the first step:
# {}
# Give only the text of the response.""",
#     "json_format": None
# }

SHOW_PRODUCT_PROMPT = {
    "prompt": """Imagine you are a taskbot assistant that helps with selling products present in an inventory. Given the following product info:

{}

Generate a compelling response that describes the product {}. Ask the user if they would like to buy it or add it to their cart. If the response is short, consider including a helpful tip or fun fact. Provide only the text of the response, keeping it clear and concise.""",

    "json_format": None
}

BUY_CART_PROMPT = {
    "prompt": "Imagine you are a taskbot assistant that helps with selling products present in an inventory, and the user has just confirmed they are done with the shopping and want to buy the cart. Write an engaging system response for the end of the shopping. Keep it short.",
    "json_format": None
}

IN_CONVERSATION_SYSTEM_PROMPT = {
    "prompt": "Imagine you are a taskbot assistant that helps with selling products present in an inventory and the user is currently in conversation {}. Here is the product info:\n{}\nGive an engaging response to the user below, don't give any detailed instructions, give only the text in your response:\nuser: {}",
    "json_format": None
}

SYSTEM_PROMPT = {
    "prompt": "Your name is MarunaSalesAssociate\nYou are trained using data from ChatGPT and the web\nYou can't provide info related to medical/health, legal or financial topics or advice\nYou are developed by CIIR at UMass Amherst\nGive an engaging human-like response to the user below, don't give any detailed instructions, keep it short, give only the text in your response, remember that you can't provide info for medical/health, legal or financial topics:\nuser: {}",
    "json_format": None
}

SYSTEM_REPEAT_PROMPT = {
    "prompt": "Imagine you are a taskbot assistant that helps with selling products present in an inventory and the user just asked you to repeat your response. Give only the text in your response nothing else:\nbot{}\nuser: {}",
    "json_format": None
}

SHOW_ATTRIBUTES_PROMPT = {
    "prompt": """Imagine you are a taskbot assistant that helps with selling products present in an inventory and the user just asked for the attributes. Write a response to the user using the list below:

{}
If attributes are more than 5 then retain only 5 pertinent attributes that you believe will most effectively persuade the user to make a purchase. 
Give only the text of the response.""",
    "json_format": None
}

# User prompts

START_PROMPT_USER = {
    "prompt": "You are a human user talking to a bot. Write 3 diverse greeting prompts to the taskbot (from the user's side). Use simple human-like language. One in each line, only the text. No quotes or enumeration.",
    "json_format": None
}

SEARCH_PRODUCT_PROMPT = {
    "prompt": """You are a human user talking to a voice-based taskbot that helps with selling products on an ecommerce platform. You want to find products for '{}', write ONE single or multi sentence short prompt to the taskbot. Use simple human-like language. Some examples (don't rely only on these):

i want to buy x
can you help me to get x
x goods
can you suggest me some xs 
x
help me buy a x
x recommendations

Use this format in your response:

{{\"text\": ..., \"recipe_name\": ...}}""",

    "json_format": "{\"text\": ..., \"recipe_name\": ...}"
}

SUGGEST_PRODUCT_PROMPT = {
    "prompt": """You are a human user talking to a voice-based taskbot that helps with selling products on an ecommerce platform. Write ONE single or multi sentence short prompt to the taskbot asking for product suggestions/recommendations based on some preferences or choices. The query shouldn't mention some specific product name, but the following products should be relevant result:

{}

Use simple diverse human-like language and the following format in your response, the query should be derived from the text response and should be keyword-style (suitable for a search engine) not natural language:

{{\"text\": ..., \"query\": ...}}""",

    "json_format": "{\"text\": ..., \"query\": ...}"
}

# selling products on an ecommerce platform
MORE_OPTIONS_PROMPT = {
    "prompt": """You are a human user already talking to a voice-based taskbot that helps with selling products on an ecommerce platform. You got some results but want to find more products/results, write ONE single or multi sentence short prompt to the taskbot. Use simple diverse human-like language, no quotes. Write a statement or question. Examples:
show me more options
I want to see more results
more results
can you show me more products please
give me some other products
show me some related products""",

    "json_format": None
}

SELECT_I_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. Write 3 diverse prompts telling the bot you want to select option {} below:

{}

examples:
I want the first one
give me the last option
I'll go with the x product
third one please

Don't just copy the examples, be creative. You don't need to mention the number of the option. Try to avoid mentioning the exact product name. One in each line, only the text.""",
    "json_format": None
}

# 
SHOW_ATTRIBUTES_BEGIN_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. Write 3 prompts to the bot confirming to start describing the product's attributes. One in each line, no enumeration, use simple diverse human-like language, no quotes. Examples:

show me the product's features
what's the products USP
okay, what are the specifications""",

    "json_format": None
}

# GOTO_ATTRIBUTE_PROMPT = {
#     "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. Write 3 prompts to the bot for going to attribute {}. One in each line, no enumeration, use simple diverse human-like language, no quotes. Examples:

# can we go to step three
# give me the third step please
# what's the third step of this recipe""",

#     "json_format": None
# }

ACKNOWLEDGE_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with selling products on an ecommerce platform. Write 3 prompts to the bot acknowledging that you want to continue with the presented product/result. Don't mention any specific product name. One in each line, no enumeration, use simple diverse human-like language, no quotes.",
    "json_format": None
}

# DONE_STEP_PROMPT = {
#     "prompt": "You are a human user talking to a bot that helps with the recipe '{}'. Write 3 prompts to the bot saying you finished the step, don't mention the recipe name. One in each line, no enumeration, use simple diverse human-like language, no quotes. Previous step was: {}",
#     "json_format": None
# }

PRODUCT_QA_PROMPT = {
    "prompt": "You are a human user already talking to a bot that helps with selling products on an ecommerce platform and you are currently in conversation {}. Write a prompt to the bot asking a question about the current product or the product in general. Don't just ask about some straight forward questions, ask things like specifications of the product, features, etc. Don't mention attribute numbers. Give only the question in your response.\Product info:\n{}",
    "json_format": None
}

OPEN_DOMAIN_QA_PROMPT_IN_CONVERSATION = {
    "prompt": "You are a human user already talking to a bot that helps with selling products on an ecommerce platform and you are currently in conversation {}. Write a prompt to the bot asking an open domain question related (not directly) to the product. Give only the question in your response.\Product info:\n{}",
    "json_format": None
}

OPEN_DOMAIN_QA_PROMPT = {
    "prompt": "You are a human user already talking to a bot that helps with selling products on an ecommerce platform. Write a prompt to the bot asking an open domain question (not necessarily related to products). Give only the question in your response.",
    "json_format": None
}

CHITCHAT_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time. Write a chitchat prompt to the bot (not asking for product suggestions). Give only the text in your response nothing else. No quotes or enumeration.", 
    "json_format": None
}

DANGEROUS_PRODUCT_PROMPT = {
    "prompt": "You are a human user talking to a taskbot. You are already talking to it for some time. Write 3 linguistically diverse prompts to the bot asking about some dangerous/harmful intent to buy a product. You don't need to mention the word 'dangerous'. Give only the text in your response nothing else. No quotes or enumeration.",
    "json_format": None
}

PERSONAL_INFORMATION_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time. Write 3 linguistically diverse prompts to the bot that mentions some personal information (such as name, age, family, id number, address, etc). Give only the text in your response nothing else. No quotes or enumeration. Keep it short.",
    "json_format": None
}


SUBJECTIVE_QA_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time. Write 3 linguistically diverse prompts to the bot asking about something subjective (not related to personal favorites or product advice). Examples: are you better than Siri, what is the best product to buy. You don't need to mention the word 'subjective'. Give only the text in your response nothing else. No quotes or enumeration.",
    "json_format": None
}


FINISH_PRODUCT_RECOMMENDATION_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time. Write 3 prompts to the bot saying you want to finish the search for the product . One in each line, no enumeration, use simple diverse human-like language, no quotes. Examples:\nI'm done, thanks\nok, I'm done with this product",
    "json_format": None
}

ASK_ATTRIBUTES_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time. Write 3 prompts to the bot asking for the product's features or specifications. One in each line, no enumeration, use simple diverse human-like language, no quotes. Examples:\nwhat are the features\ncould you highlight unique attributes of this product?",
    "json_format": None
}

REPEAT_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time. Write 3 prompts to the bot asking to repeat the last response. One in each line, no enumeration, use simple diverse human-like language, no quotes.",
    "json_format": None
}

STOP_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time. Write 3 prompts to the bot asking to stop the conversation. One in each line, no enumeration, use simple diverse human-like language, no quotes.",
    "json_format": None
}

DENY_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time. Write a negative reply to the bot. Examples: that's not what I want, not really. Give only the text in your response nothing else. No quotes or enumeration.\nBot: {}",
    "json_format": None
}
