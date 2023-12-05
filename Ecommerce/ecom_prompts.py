# System prompts

START_PROMPT = {
    "prompt": "Your name is Maruna Shopper. You are a taskbot developed by CIIR at UMass Amherst, that helps with selling products present in a product catalog. Write an intro prompt to the user, don't use emojis, keep it short.",
    "json_format": None
}

SHOW_RESULTS_PROMPT = {
    "prompt": """Imagine you are a shopping assistant that helps with selling products present in an inventory. Given the following product results info for the query '{}':
results: [
 
{}
]
Generate a compelling response that presents all the results in the most appealing order based on the provided information. Encourage the user to select a product for options like adding it to the cart, or adding for compare, or making a purchase. Highlight only the key details to capture the user's interest, avoiding excessive details. If a result is not directly related to the query, don't include it. In case no relevant results are available, provide a friendly response and suggest the user try a different query.
Put the product titles in '*' bold formatting, always use enumeration instead of bullet points.
Include all enumerated product ids present in results.
Use following format in your response, the text should include your full taskbot response:

{{"text": ..., "product_ids": [...]}}""",

    "json_format": "{\"text\": ..., \"product_ids\": [...]}"
}

SHOW_MORE_RESULTS_PROMPT = {
    "prompt": """Imagine you are a shopping assistant that helps with selling products present in an inventory and already provided some results for a product suggestion. Given the following next product results info for the query '{}':
results: [    
{}
]
Generate an engaging response that summarizes all of these additional results in the best order based on the presented info. Encourage the user to select a product for options like adding it to the cart, comparing, or making a purchase.  Mention only the most important info to attract the user, not all the details. If one result is not directly relevant to the query, don't include it. If no results are provided or no relevant results are in the given list, give an appropriate response and tell the user to try something else.
Put the product titles in '*' bold formatting, always use enumeration instead of bullet points.
Include all enumerated product ids present in results.
Use following format in your response, the text should include your full taskbot response:

{{"text": ..., "product_ids": [...]}}""",

    "json_format": "{\"text\": ..., \"product_ids\": [...]}"
}

FIND_SUGGESTIONS_PROMPT = {
    "prompt": "Imagine you are a shopping assistant that helps with selling products present in an inventory. Give {} most popular product name suggestions for the query '{}', one in each line, no quotes or enumeration.",
    "json_format": None
}

OPTION_SELECTED_PROMPT = {
    "prompt": """Imagine you are a shopping assistant that helps with selling products present in an inventory and the user just selected the following product: 

title: {}
description: {}

Generate a concise system response and provide options for the user, such as viewing the product's attributes, adding it to the cart, purchasing it, or adding it for comparison. Please provide only the text of the response.""",
    
    "json_format": None
}



SHOW_PRODUCT_PROMPT = {
    "prompt": """Imagine you are a shopping assistant that helps with selling products present in an inventory. Given the following product info:

{}
And last user utterance : {}

Put the product title in '*' bold formatting.
Generate a compelling response that describes the product or answers users question if asked. You may highlight most relevant feature in the given product information. Ask the user if they would like to buy it or add it to their cart. Provide only the text of the response, keeping it clear.""",

    "json_format": None
}

BOUGHT_CART_PROMPT = {
    "prompt": "Imagine you are a shopping assistant that helps with selling products present in an inventory, and the user has just confirmed they are done with the shopping and want to buy the cart. Write an engaging system response for the end of the shopping experience. Keep it short.",
    "json_format": None
}

IN_CONVERSATION_SYSTEM_PROMPT = {
    "prompt": """Imagine you are a shopping assistant that helps with selling products present in an inventory and the user is currently in conversation. Here is the product info:\n{}\nGive an engaging response to the user below, don't give any detailed instructions, give only the text in your response, you can ask user to type the need:\nuser: {}
    Do not ask following things from user: Payment information, shipping address, quantity to buy, any button to click.
    """,
    "json_format": None
}

SYSTEM_PROMPT = {
    "prompt": "Your name is MarunaSalesAssociate\nYou are trained using data from ChatGPT and the web\nYou can't provide info related to medical/health, legal or financial topics or advice\nYou are developed by CIIR at UMass Amherst\nGive an engaging human-like response to the user below, don't give any detailed instructions, keep it short, give only the text in your response, remember that you can't provide info for medical/health, legal or financial topics:\nuser: {}",
    "json_format": None
}

SYSTEM_REPEAT_PROMPT = {
    "prompt": "Imagine you are a shopping assistant that helps with selling products present in an inventory and the user just asked you to repeat your response. Give only the text in your response nothing else:\nbot{}\nuser: {}",
    "json_format": None
}

SHOWN_ATTRIBUTES_PROMPT = {
    "prompt": """Imagine you are a shopping assistant that helps with selling products on an ecommerce platform and the user just asked for the attributes. Write a response to the user using the list below:

{}
If attributes are more than 5 then retain only 5 pertinent attributes that you believe will most effectively persuade the user to make a purchase. 
Give only the text of the response.""",
    "json_format": None
}

SHOWN_CART_PROMPT = {
    "prompt": """Imagine you are a shopping assistant that helps with selling products on an ecommerce platform and the user just asked for showing shopping cart list done till now. Write a response to the user using the list below:

{}
Put the product titles in '*' bold formatting, always use enumeration instead of bullet points. Summarize the cart contents concisely.
Use this format in your response, the text should include your full taskbot response:

{{"text": ..., "product_ids": [...]}}.""",
    "json_format": "{\"text\": ..., \"product_ids\": [...]}"
}

SHOW_COMPARISON_PROMPT = {
    "prompt": """Imagine you are a shopping assistant that helps with selling products on an ecommerce platform and the user just asked for comparison between products. Write a response summarizing differences between products to the user using the product list below:

{}
Put the product titles in '*' bold formatting. 
Use this format in your response, the text should include your full taskbot response:

{{"text": ..., "product_ids": [...]}}.""",
    "json_format": "{\"text\": ..., \"product_ids\": [...]}"
}

ASK_CLARIFICATION_PROMPT = {
    "prompt": """Imagine you are a shopping assistant that helps with selling products on an ecommerce platform and the user just asked for a generic product suggestion. Write a response asking clarification from the user to be more specific or provide details for the suggestion:
Use following conversation to construct Clarification question:
{}

Examples (do not use these examples):
User: I want to buy a shirt
Clarifications: What color are looking for? Any specific brands you are interested in?

Give only the text of the response.""",
    "json_format": None
}

CHECK_DELIVERY_PROMPT = {
    "prompt" : """ Imagine you are a shopping assistant that helps with selling products on an ecommerce platform and the user just asked whether given product is available for delivery in {}. 
    According to the product catalog, the product {} is available in following locations : {}
    Write a response to the user whether the product could be delivered or not.

    Give only the text of the response.""",
    "json_format" : None
}


# User prompts

START_PROMPT_USER = {
    "prompt": "You are a human user talking to a bot. Write 3 diverse greeting prompts to the taskbot (from the user's side). Use simple human-like language. One in each line, only the text. No quotes or enumeration.",
    "json_format": None
}


SEARCH_PRODUCT_PROMPT = {
    "prompt": """You are a human user talking to a taskbot that helps with selling products on an ecommerce platform. You want to find products for '{}', write ONE single or multi sentence short prompt to the taskbot. Use simple human-like language. Some examples (don't rely only on these):

i want to buy x
can you help me to get x which is of brand d and size y
x goods
can you suggest me some xs 
x
help me buy a x
x recommendations

Give slots for query, product_name, and list of attributes
Give query too in the response, the query should be derived from the text response and should be keyword-style (suitable for a search engine) not natural language
List of attributes should be derived from the text in response and should be like [(color:c),(brand: b)], keep at max 4 most relevant attributes, every text may not have these attributes mentioned, in that case use a blank list []
Use this format in your response:

{{\"text\": ..., \"product_name\": ...,  \"query\": ..., \"attributes_list\":...}}""",

    "json_format": "{\"text\": ..., \"product_name\": ..., \"query\": ..., \"attributes_list\":...}"
}

SUGGEST_PRODUCT_PROMPT = {
    "prompt": """You are a human user talking to a voice-based taskbot that helps with selling products on an ecommerce platform. Write ONE single or multi sentence short prompt to the taskbot asking for product suggestions/recommendations based on some preferences or choices. The query shouldn't mention the product name, but the following products should be relevant result:

{}
Give slots for query, and list of attributes (attributes_list)

Use simple diverse human-like language and the following format in your response, the query should be derived from the text response and should be keyword-style (suitable for a search engine) not natural language:
List of attributes should be derived from the text in response and should be like [(color:c),(brand: b)], keep at max 4 most relevant attributes, every text may not have these attributes mentioned, in that case use a blank list []
Use this format in your response:

{{\"text\": ..., \"query\": ..., \"attributes_list\":...}}""",

    "json_format": "{\"text\": ..., \"query\": ..., \"attributes_list\":...}"
}



# selling products on an ecommerce platform
MORE_OPTIONS_PROMPT = {
    "prompt": """You are a human user already talking to a taskbot that helps with selling products on an ecommerce platform. You got some results but want to find more products/results, write ONE single or multi sentence short prompt to the taskbot. Use simple diverse human-like language, no quotes. Write a statement or question. Examples:
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

Don't just copy the examples, be creative. You don't need to mention the number of the option always. 
Try to avoid mentioning the exact product name and do not ask to add to cart or for compare just give the prompts for selection of the option. 
One in each line, only the text.""",
    "json_format": None
}

# 
SHOW_ATTRIBUTES_BEGIN_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. Write a 3 prompts to the bot confirming to start describing the product's attributes for product {}. One in each line, no enumeration, use simple diverse human-like language, no quotes. Examples:
No enumeration
text : 
show me the product's features
what's the products USP
okay, what are the specifications
could you highlight unique attributes of this product?

Use following format in the response: 
{{\"text\":..., \"title\":..., \"product_id\" :... }}

""",

    "json_format": "{\"text\":..., \"title\":..., \"product_id\" :... }"
}


SHOW_CART_PROMPT = {
    "prompt": "You are a human user already talking to a bot that helps with selling products on an ecommerce platform. Write a prompt to the bot asking it to show cart (probable list of products human user has marked to buy). Give only the question in your response.",
    "json_format": None
}

ACKNOWLEDGE_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with selling products on an ecommerce platform. Write 3 prompts to the bot acknowledging that you want to continue with the presented product/result / conversation. Don't mention any specific product name. One in each line, no enumeration, use simple diverse human-like language, no quotes.",
    "json_format": None
}


PRODUCT_QA_PROMPT = {
    "prompt": """You are a human user already talking to a bot that helps with selling products on an ecommerce platform and you are currently in conversation. Write a prompt to the bot asking a question about the current product or the product in general. Don't just ask about some very straight forward question like whats the product name, ask things like specifications of the product, features, etc. Don't mention attribute numbers.\Product info:\n{},
    Use following format in the response: 
    {{\"question\": ..., \"title\": ..., \"product_id\": ...}}""",
    "json_format" : "{\"question\": ..., \"title\": ..., \"product_id\": ...}"
}

OPEN_DOMAIN_QA_PROMPT_IN_CONVERSATION = {
    "prompt": "You are a human user already talking to a bot that helps with selling products on an ecommerce platform and you are currently in conversation {}. Write a prompt to the bot asking an open domain question related (not directly) to the product. Give only the question in your response.\Product info:\n{}",
    "json_format": None
}

OPEN_DOMAIN_QA_PROMPT = {
    "prompt": """You are a human user already talking to a bot that helps with selling products on an ecommerce platform. Write a prompt to the bot asking an open domain question (not necessarily related to products). Give only question and general topic asked in the question. \n Use this format in your response: 
    {{\"question\": ..., \"topic\": ...}}""",
    "json_format": "{\"question\": ..., \"topic\": ...}"
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

BUY_CART_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time and have added few items in cart. Write a response to ask bot to buy the cart. Examples: I would like to buy, proceed for checkout, I'm ready to make the purchase. Give only the text in your response nothing else. No quotes or enumeration.\nBot: {}",
    "json_format": None
}

ADD_TO_CART_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time and currently discussing about a product {}. 
    Write a response to ask the bot to add this product to the shopping cart. 
    Response should not be very short like: add to cart. 
    If the product's name is lengthy, utilize distinct and recognizable words from its name for reference, in such a case choose product name length such that it fits the flow of conversation.

    
    Examples: Add x to the cart, Put it in the cart.\nBot: {}
    
    
    Use following format in the response:

    {{\"text\": ..., \"title\": ..., \"product_id\":...}}
    
    """,
    "json_format": "{\"text\": ..., \"title\": ..., \"product_id\":...}"
}

REMOVE_FROM_CART_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time and currently discussing about a product {} which is in your shopping cart. 
    Write a response to ask the bot to remove this product from the shopping cart. 
    Response should not be very short like: remove. 
    If the product's name is lengthy, utilize distinct and recognizable words from its name for reference, in such a case choose product name length such that it fits the flow of conversation.

    Examples: Take x out from the cart, remove x .\nBot: {}
    
    
    Use following format in the response:

    {{\"text\": ..., \"title\": ..., \"product_id\":...}}
    
    """,
    "json_format": "{\"text\": ..., \"title\": ..., \"product_id\":...}"
}

ADD_TO_CART_REFERENTIAL_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time and currently discussing about a product {}. 
    Write a response to ask the bot to add this product to the shopping cart. 
    Do not directly state the name of this product while asking to add to cart, 
    you can use contextual cues or references like : add second one to the cart
    Response should not be very short like: add to cart. 
    If the product's name is lengthy, utilize distinct and recognizable words from its name for reference, in such a case choose product name length such that it fits the flow of conversation.

    
    Examples: Add x to the cart, Add last one to the cart.\nBot: {}
    
    
    Use following format in the response:

    {{\"text\": ..., \"title\": ..., \"product_id\":...}}
    
    """,
    "json_format": "{\"text\": ..., \"title\": ..., \"product_id\":...}"
}

REMOVE_FROM_CART_REFERENTIAL_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time and currently discussing about a product {} which is in your shopping cart. 
    Write a response to ask the bot to remove this product from the shopping cart. 
    Do not directly state the name of this product while asking to remove from the cart, 
    you can use contextual cues or references like : remove second one from the cart
    Response should not be very short like: remove 
    If the product's name is lengthy, utilize distinct and recognizable words from its name for reference, in such a case choose product name length such that it fits the flow of conversation.

    Examples: Take last one from the cart, remove x .\nBot: {}
    
    
    Use following format in the response:

    {{\"text\": ..., \"title\": ..., \"product_id\":...}}
    
    """,
    "json_format": "{\"text\": ..., \"title\": ..., \"product_id\":...}"
}


USER_PREFERENCE_PROMPT = {
    "prompt": """You are a human user talking to a voice-based taskbot that helps with selling products on an ecommerce platform. Write ONE single or multi sentence short prompt to the taskbot asking for product recommendations based on some new preferences or choices. The query shouldn't mention some specific product name, but the following products should be relevant result:

{}

Use simple diverse human-like language and the following format in your response, the query should be derived from the text response and should be keyword-style (suitable for a search engine) not natural language, also attributes_list should be a list of relevant key value pairs with key as name of attribute and value as it's specification:

{{\"text\": ..., \"query\": ..., \"attributes_list\":...}}""",

    "json_format": "{\"text\": ..., \"query\": ..., \"attributes_list\":...}"
}


COMPARE_PRODUCTS_PROMPT = {
    "prompt": """You are a human user talking to a voice-based taskbot that helps with selling products on an ecommerce platform and you are already in a conversation which has a list of products for comparison. Write ONE single or multi sentence short prompt to the taskbot asking for comparisons between the products. You can ask bot to compare entire list or for few product comparison. Following products are present in the compare list :

{}

Use simple diverse human-like language and the following format in your response, the query should be derived from the text response and should be keyword-style (suitable for a search engine) not natural language:
List of products is the list of title of products for comparison: 
{{\"text\": ..., \"query\": ..., \"list_of_products\":...}}""",

    "json_format": "{\"text\": ..., \"query\": ..., \"list_of_products\":...}"
}

ADD_FOR_COMPARE_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time and currently discussing about a product {}. 
    Craft a response requesting the bot to include this product in the comparison list.
    Response should not be very short like compare or add compare. 
    If the product's name is lengthy, utilize distinct and recognizable words from its name for reference, in such a case choose product name length such that it fits the flow of conversation.

    Some Examples: Add x to the compare list, Put x for comparison.
    No quotes or enumeration.\nBot: {}
    
    
    Use following format in the response:

    {{\"text\": ..., \"title\": ..., \"product_id\":...}}
    
    """,
    "json_format": "{\"text\": ..., \"title\": ..., \"product_id\":...}"
}

REMOVE_FROM_COMPARE_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time and currently discussing about a product {} which is in your compare list. Write a response to ask the bot to remove this product from the compare list, response should not be very short. 
    
    If the product's name is lengthy, utilize distinct and recognizable words from its name for reference, in such a case choose product name length such that it fits the flow of conversation.

    Expected Examples: Do not use x for comparison, remove x\n
    
    Bot: {},
    
    Use following format in the response:

    {{\"text\": ..., \"title\": ..., \"product_id\":...}}
    
    """,
    "json_format": "{\"text\": ..., \"title\": ..., \"product_id\":...}"
}

ADD_FOR_COMPARE_REFERENTIAL_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time and currently discussing about a product {}. 
    Craft a response requesting the bot to include this product in the comparison list.
    Do not directly state the name of this product while asking to compare, 
    you can use contextual cues or references like : add second one for compare.
    Response should not be very short like: add for compare. 
    If the product's name is lengthy, utilize distinct and recognizable words from its name for reference, in such a case choose product name length such that it fits the flow of conversation.

    
    Examples: Add x to compare, Add last one for comparing.\nBot: {}
    
    
    Use following format in the response:

    {{\"text\": ..., \"title\": ..., \"product_id\":...}}
    
    """,
    "json_format": "{\"text\": ..., \"title\": ..., \"product_id\":...}"
}

REMOVE_FROM_COMPARE_REFERENTIAL_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time and currently discussing about a product {} which is in your shopping cart. 
    Write a response to ask the bot to remove this product from the compare list.
    Do not directly state the name of this product while asking to remove from the cart, 
    you can use contextual cues or references like : remove second one from the cart
    Response should not be very short like: remove 
    If the product's name is lengthy, utilize distinct and recognizable words from its name for reference, in such a case choose product name length such that it fits the flow of conversation.

    Examples: Take last one from the cart, remove x .\nBot: {}
    
    
    Use following format in the response:

    {{\"text\": ..., \"title\": ..., \"product_id\":...}}
    
    """,
    "json_format": "{\"text\": ..., \"title\": ..., \"product_id\":...}"
}

USER_GENERIC_PRODUCT_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. Write a generic product prompt to the bot. Prompt should not be specific as bot should ask you few clarifying questions in return which will lead to Product : {}. Examples I need a laptop, show me a shirt, I am shopping for xmas gift.  Give only the text in your response nothing else. No quotes or enumeration.""", 
    "json_format": None
}
USER_CLARIFIES_AFTER_CLARIFICATION_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. 
    Write a generic product prompt to the bot refering to the clarification bot has asked. 
    Prompt should not be very specific as bot should ask you a clarifying question back in return which will lead to Product : {}. 
    Current conversation : \n{}
    Examples I need a laptop with 16gb RAM, show me a yellow shirt, I am shopping for xmas clothing.
    
    Give slots for query, and list of attributes (attributes_list)

    Use simple diverse human-like language and the following format in your response, the query should be derived from the text response and should be keyword-style (suitable for a search engine) not natural language:
    List of attributes should be derived from the text in response and should be like [(color:c),(brand: b)], keep at max 4 most relevant attributes, every text may not have these attributes mentioned, in that case use a blank list []
    Use this format in your response:

    {{\"text\": ..., \"query\": ..., \"attributes_list\":...}}""",

    "json_format": "{\"text\": ..., \"query\": ..., \"attributes_list\":...}"
}
CHECK_DELIVERY_AVAILABILITY_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with selling products on an ecommerce platform. You are already talking to it for some time and currently discussing about a product {}. Write a response to ask the bot to check whether it could be delivered in {}. Examples: Is it available for delivery in country x, Could it be delivered to x. \nBot: {}
    You must mention the name of country in text 
    Use following format in the response just keep name of country in the address:
    {{\"text\":..., \"address\":...}}
    
    """,
    "json_format": "{\"text\":..., \"address\":...}"
}

USER_PRODUCT_INFORMATION_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with selling products on an ecommerce platform. Write a prompt to the bot which asks to describe the product: {}. Question should be short and in a natural language flow. Give only text in your response nothing else.  No quotes or enumeration. \nBot: {}", 
    "json_format": None
}