# System prompts

START_PROMPT = {
    "prompt": "Your name is MarunaChef. You are a taskbot that helps with recipes developed by CIIR at UMass Amherst. Write an intro prompt to the user, don't use emojis.",
    "json_format": None
}

SHOW_RESULTS_PROMPT = {
    "prompt": """Imagine you are a taskbot assistant that helps with recipes. Given the following recipe results info for the query '{}':
results: [
 
{}
]
Generate an engaging response that summarizes the results in the best order based on the presented info, and asks the user to select one or show more options. Mention only the most important info to attract the user, not all the details. If a result is not directly relevant to the query, don't include it. If no results are provided or no relevant results are in the given list, give an appropriate response and tell the user to try something else.

Use this format in your response, the text should include your full taskbot response:

{{"text": ..., "recipe_ids": [...]}}""",

    "json_format": "{\"text\": ..., \"recipe_ids\": [...]}"
}

SHOW_MORE_RESULTS_PROMPT = {
    "prompt": """Imagine you are a taskbot assistant that helps with recipes and already provided some results. Given the following next recipe results info for the query '{}':
results: [    
{}
]
Generate an engaging response that summarizes these additional results in the best order based on the presented info, and asks the user to select one or show more options. Mention only the most important info to attract the user, not all the details. If one result is not directly relevant to the query, don't include it. If no results are provided or no relevant results are in the given list, give an appropriate response and tell the user to try something else.

Use this format in your response, the text should include your full taskbot response:

{{"text": ..., "recipe_ids": [...]}}""",

    "json_format": "{\"text\": ..., \"recipe_ids\": [...]}"
}

FIND_SUGGESTIONS_PROMPT = {
    "prompt": "Imagine you are a taskbot assistant that helps with recipes. Give {} most popular recipe title suggestions for the query '{}', one in each line, no quotes or enumeration.",
    "json_format": None
}

OPTION_SELECTED_PROMPT = {
    "prompt": """Imagine you are a taskbot that helps with recipes and the user just selected the following recipe: 

title: {}
description: {}

Write an engaging system response, ask the user if they want to see the required ingredients and when they are ready to start with the first step. Give only the text of the response.""",
    
    "json_format": None
}

STARTED_TASK_PROMPT = {
    "prompt": """Imagine you are a taskbot that helps with recipes and the user just confirmed to start the recipe '{}' he already selected previously. Don't congratulate him for the choice. Write an engaging system response for the first step:
{}
Give only the text of the response.""",
    "json_format": None
}

SHOW_STEP_PROMPT = {
    "prompt": """Imagine you are a taskbot that helps with recipes. Given the following recipe info:

{}

generate an engaging response describing step {}, and ask when they are ready to continue. If step is short, also give a tip or fun fact. Give only the text of the response. Keep it SHORT and simple and not overwhelming.""",

    "json_format": None
}

NO_MORE_STEPS_PROMPT = {
    "prompt": "Imagine you are a taskbot that helps with recipes and the user just finished the last step of the recipe. Write an engaging system response for the end of the recipe, also asking if they have any more questions for the recipe. Keep it SHORT.\nRecipe info:\n{}",
    "json_format": None
}

TASK_COMPLETE_PROMPT = {
    "prompt": "Imagine you are a taskbot that helps with recipes and the user just confirmed they are done with the recipe. Write an engaging system response for the end of the recipe. Keep it short.",
    "json_format": None
}

IN_TASK_SYSTEM_PROMPT = {
    "prompt": "Imagine you are a taskbot that helps with recipes and the user is currently in step {}. Here is the recipe info:\n{}\nGive an engaging response to the user below, don't give any detailed instructions, give only the text in your response:\nuser: {}",
    "json_format": None
}

SYSTEM_PROMPT = {
    "prompt": "Your name is MarunaChef\nYou are trained using data from ChatGPT and the web\nYou can't provide info related to medical/health, legal or financial topics or advice\nYou are developed by CIIR at UMass Amherst\nGive an engaging human-like response to the user below, don't give any detailed instructions, keep it short, give only the text in your response, remember that you can't provide info for medical/health, legal or financial topics:\nuser: {}",
    "json_format": None
}

SYSTEM_REPEAT_PROMPT = {
    "prompt": "Imagine you are a taskbot that helps with recipes and the user just asked you to repeat your response. Give only the text in your response nothing else:\nbot{}\nuser: {}",
    "json_format": None
}

DISPLAY_INGREDIENTS_PROMPT = {
    "prompt": """Imagine you are a taskbot that helps with recipes and the user just asked for the ingredients. Write a response to the user using the list below:

{}

Give only the text of the response.""",
    "json_format": None
}

# User prompts

START_PROMPT_USER = {
    "prompt": "You are a human user talking to a bot. Write 3 diverse greeting prompts to the taskbot (from the user's side). Use simple human-like language. One in each line, only the text. No quotes or enumeration.",
    "json_format": None
}

SEARCH_RECIPE_PROMPT = {
    "prompt": """You are a human user talking to a voice-based taskbot that helps with recipes. You want to find recipes for '{}', write ONE single or multi sentence short prompt to the taskbot. Use simple human-like language. Some examples (don't rely only on these):

i want to make x
can you help me cook x
x recipes
can you suggest me some x recipes
x
help me bake some x
x recommendations

Use this format in your response:

{{\"text\": ..., \"recipe_name\": ...}}""",

    "json_format": "{\"text\": ..., \"recipe_name\": ...}"
}

SUGGEST_RECIPE_PROMPT = {
    "prompt": """You are a human user talking to a voice-based taskbot that helps with recipes. Write ONE single or multi sentence short prompt to the taskbot asking for recipe suggestions/recommendations based on some preferences or occasion/circumstances. The query shouldn't mention some specific recipe name, but the following recipe should be relevant result:

{}

Use simple diverse human-like language and the following format in your response, the query should be derived from the text response and should be keyword-style (suitable for a search engine) not natural language:

{{\"text\": ..., \"query\": ...}}""",

    "json_format": "{\"text\": ..., \"query\": ...}"
}

MORE_OPTIONS_PROMPT = {
    "prompt": """You are a human user already talking to a voice-based taskbot that helps with recipes. You got some results but want to find more recipes/results/options, write ONE single or multi sentence short prompt to the taskbot. Use simple diverse human-like language, no quotes. Write a statement or question. Examples:
show me more options
I want to see more results
more results
can you show me more recipes please
give me some different recipes""",

    "json_format": None
}

SELECT_I_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with recipes. Write 3 diverse prompts telling the bot you want to select option {} below:

{}

examples:
I want the first one
give me the last option
I'll go with the x recipe
third one please

Don't just copy the examples, be creative. You don't need to mention the number of the option. Try to avoid mentioning the exact recipe name. One in each line, only the text.""",
    "json_format": None
}

BEGIN_TASK_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with recipes. Write 3 prompts to the bot confirming to start the recipe. One in each line, no enumeration, use simple diverse human-like language, no quotes. Examples:

let's start cooking
i'm ready
okay, give me the first step""",

    "json_format": None
}

GOTO_STEP_PROMPT = {
    "prompt": """You are a human user talking to a bot that helps with recipes. Write 3 prompts to the bot for going to step {}. One in each line, no enumeration, use simple diverse human-like language, no quotes. Examples:

can we go to step three
give me the third step please
what's the third step of this recipe""",

    "json_format": None
}

ACKNOWLEDGE_TASK_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with recipes. Write 3 prompts to the bot acknowledging that you want to continue with the presented recipe/result. Don't mention any specific recipe name. One in each line, no enumeration, use simple diverse human-like language, no quotes.",
    "json_format": None
}

ACKNOWLEDGE_STEP_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with the recipe '{}'. Write 3 prompts to the bot acknowledging that the step is done, don't mention the recipe name. One in each line, no enumeration, use simple diverse human-like language, no quotes. Previous step was: {}",
    "json_format": None
}

NEXT_STEP_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with the recipe '{}'. Write 3 prompts to the bot asking for the next step, don't mention the recipe name. One in each line, no enumeration, use simple diverse human-like language, no quotes. Previous step was: {}",
    "json_format": None
}

DONE_STEP_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with the recipe '{}'. Write 3 prompts to the bot saying you finished the step, don't mention the recipe name. One in each line, no enumeration, use simple diverse human-like language, no quotes. Previous step was: {}",
    "json_format": None
}

IN_TASK_QA_PROMPT = {
    "prompt": "You are a human user already talking to a bot that helps with recipes and you are currently in step {}. Write a prompt to the bot asking a question about the current step or the recipe in general. Don't just ask about next step, ask things like process, timing, ingredients, tools, etc. Don't mention step numbers. Give only the question in your response.\nRecipe info:\n{}",
    "json_format": None
}

OPEN_DOMAIN_QA_PROMPT_IN_TASK = {
    "prompt": "You are a human user already talking to a bot that helps with recipes and you are currently in step {}. Write a prompt to the bot asking an open domain question related (not directly) to the recipe. Give only the question in your response.\nRecipe info:\n{}",
    "json_format": None
}

OPEN_DOMAIN_QA_PROMPT = {
    "prompt": "You are a human user already talking to a bot that helps with recipes. Write a prompt to the bot asking an open domain question (not necessarily related to recipes). Give only the question in your response.",
    "json_format": None
}

CHITCHAT_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with recipes. You are already talking to it for some time. Write a chitchat prompt to the bot (not asking for recipe suggestions). Give only the text in your response nothing else. No quotes or enumeration.", 
    "json_format": None
}

OFFENSE_PROMPT = {
    "prompt": "You are a human user talking to a taskbot. You are already talking to it for some time. Write 3 linguistically diverse offensive prompts to the bot, but don't use any obvious swear words. Give only the text in your response nothing else. No quotes or enumeration.",
    "json_format": None
}

LEGAL_ADVICE_PROMPT = {
    "prompt": "You are a human user talking to a taskbot. You are already talking to it for some time. Write 3 linguistically diverse prompts to the bot asking for some legal advice. You don't need to mention the word 'legal'. Give only the text in your response nothing else. No quotes or enumeration.",
    "json_format": None
}

FINANCIAL_ADVICE_PROMPT = {
    "prompt": "You are a human user talking to a taskbot. You are already talking to it for some time. Write 3 linguistically diverse prompts to the bot asking for some financial advice. You don't need to mention the word 'financial'. Give only the text in your response nothing else. No quotes or enumeration.",
    "json_format": None
}

MEDICAL_ADVICE_PROMPT = {
    "prompt": "You are a human user talking to a taskbot. You are already talking to it for some time. Write 3 linguistically diverse prompts to the bot asking for some medical advice. You don't need to mention the word 'medical'. Give only the text in your response nothing else. No quotes or enumeration.",
    "json_format": None
}

DANGEROUS_TASK_PROMPT = {
    "prompt": "You are a human user talking to a taskbot. You are already talking to it for some time. Write 3 linguistically diverse prompts to the bot asking about some dangerous/harmful task. You don't need to mention the word 'dangerous'. Give only the text in your response nothing else. No quotes or enumeration.",
    "json_format": None
}

PERSONAL_INFORMATION_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with recipes. You are already talking to it for some time. Write 3 linguistically diverse prompts to the bot that mentions some personal information (such as name, age, family, id number, address, etc). Give only the text in your response nothing else. No quotes or enumeration. Keep it short.",
    "json_format": None
}

SUICIDE_ATTEMPT_PROMPT = {
    "prompt": "Based on the following examples, write 3 more diverse. No quotes or enumeration. Keep it short. Examples:\nlife is so pointless\nI feel like swallowing these pills\nI'm gonna throw myself off a bridge",
    "json_format": None
}

SUBJECTIVE_QA_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with recipes. You are already talking to it for some time. Write 3 linguistically diverse prompts to the bot asking about something subjective (not related to personal favorites or recipe advice). Examples: are you better than Siri, what is the best recipe. You don't need to mention the word 'subjective'. Give only the text in your response nothing else. No quotes or enumeration.",
    "json_format": None
}

SET_TIMER_PROMPT_1 = {
    "prompt": "You are a human user talking to a bot that helps with recipes. You are already talking to it for some time. Write a prompt to the bot for setting a timer for some amount of time. Pick a random duration in seconds. Use the following format in your response, the text should also include the duration, the duration field should have this format H:M:S: {\"text\": ..., \"duration\": ...}",
    "json_format": "\{\"text\":..., \"duration\":...\}"
}

SET_TIMER_PROMPT_2 = {
    "prompt": "You are a human user talking to a bot that helps with recipes. You are already talking to it for some time. Write a prompt to the bot for setting a timer for some amount of time. Pick a random duration in hours & minutes. Use the following format in your response, the text should also include the duration, the duration field should have this format H:M:S: {\"text\": ..., \"duration\": ...}",
    "json_format": "\{\"text\":..., \"duration\":...\}"
}

SET_TIMER_PROMPT_3 = {
    "prompt": "You are a human user talking to a bot that helps with recipes. You are already talking to it for some time. Write a prompt to the bot for setting a timer for some amount of time. Pick a random duration in minutes & seconds. Use the following format in your response, the text should also include the duration, the duration field should have this format H:M:S: {\"text\": ..., \"duration\": ...}",
    "json_format": "\{\"text\":..., \"duration\":...\}"
}

FINISH_TASK_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with recipes. You are already talking to it for some time. Write 3 prompts to the bot saying you want to finish the task/recipe. One in each line, no enumeration, use simple diverse human-like language, no quotes. Examples:\nI'm done, thanks\nok, I'm done with this recipe",
    "json_format": None
}

SHOW_INGREDIENTS_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with recipes. You are already talking to it for some time. Write 3 prompts to the bot asking for the ingredients. One in each line, no enumeration, use simple diverse human-like language, no quotes. Examples:\nwhat are the ingredients\nwhat do I need to cook this",
    "json_format": None
}

REPEAT_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with recipes. You are already talking to it for some time. Write 3 prompts to the bot asking to repeat the last response. One in each line, no enumeration, use simple diverse human-like language, no quotes.",
    "json_format": None
}

STOP_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with recipes. You are already talking to it for some time. Write 3 prompts to the bot asking to stop the conversation. One in each line, no enumeration, use simple diverse human-like language, no quotes.",
    "json_format": None
}

DENY_PROMPT = {
    "prompt": "You are a human user talking to a bot that helps with recipes. You are already talking to it for some time. Write a negative reply to the bot. Examples: that's not what I want, not really. Give only the text in your response nothing else. No quotes or enumeration.\nBot: {}",
    "json_format": None
}
