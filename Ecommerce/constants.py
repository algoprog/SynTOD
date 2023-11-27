from ecom_prompts import *

prompt = 'prompt'
json_format = 'json_format'

product_name = 'product'
recipe = 'recipe'
popo = product_name
attributes = 'attributes'
title = 'title'
rating = 'overall'
ratingCount = 'vote'

# openai_keys = ['']
openai_key = ''

class Intents:
    # register all intents here

    '''
    untracked intents
    
    no_results
    
    
    '''

    def __init__(self) -> None:
        
        # Prompts Present


        # User
        self.search_product = 'search_product'
        self.suggest_product = 'suggest_product'
        self.select_i = 'select_i'
        self.select_i_remove_from_cart = 'select_i_remove_from_cart'
        self.select_i_remove_from_compare = 'select_i_remove_from_compare'
        self.show_attributes = 'show_attributes'
        self.acknowledge = 'acknowledge'
        self.open_domain_qa = 'open_domain_qa'
        self.chitchat = 'chitchat'
        self.subjective_qa = 'subjective_qa'
        self.repeat = 'repeat'
        self.deny = 'deny'
        self.stop = 'stop'
        self.dangerous_product = 'dangerous_product' # not used


        # User and untracked 
        self.user_start = 'user_start'
        self.show_cart = 'show_cart'
        self.buy_cart = 'buy_cart'
        self.add_to_cart = 'add_to_cart'
        self.remove_from_cart = 'remove_from_cart'
        # self.user_preference = 'user_preference'  # refine query works better for this 
        self.refine_query = 'refine_query'
        
        self.compare_products = 'compare_products'
        self.add_for_compare = 'add_for_compare'
        self.remove_from_compare = 'remove_from_compare'
        self.generic_product_query = 'generic_product_query'
        self.product_qa = 'product_qa'
        self.delivery_address = 'delivery_address'


        # system
        self.start = 'start'

        self.more_results = 'more_results'
        self.show_results = 'show_results'
        self.option_selected = 'option_selected'
        self.shown_attributes = 'shown_attributes'
        self.show_suggestions = 'show_suggestions'
        self.product_info = 'product_info'
        

        # undecided and untracked 

        self.more_options = 'more_options' # ?
        self.shown_cart = 'shown_cart'
        self.bought_cart = 'bought_cart'
        self.show_comparison = 'show_comparison'
        self.clarifying_questions = 'clarifying_questions'
        self.no_more_clarifying_questions = 'no_more_clarifying_questions' # no need of prompt
        self.system_response = 'system_response'

        self.started_conversation = 'started_conversation' # remove ? 
        self.no_results = 'no_results'


        # No need of prompts for following states: string in string => intent in intent!! 
        # all have single prompt where conv is provided : IN_CONVERSATION_SYSTEM_PROMPT

        self.system_response_cart_removal = 'system_response_cart_removal'
        self.system_response_added_to_cart = 'system_response_added_to_cart'
        self.system_response_add_for_compare = 'system_response_add_for_compare'
        self.system_response_remove_from_compare = 'system_response_remove_from_compare'
        self.in_conversation_system_response = 'in_conversation_system_response'
        
        
        
        
        

intents = Intents()


# intents_map = {

#     # system
#     intents.start : START_PROMPT,
#     intents.show_results:SHOW_RESULTS_PROMPT,
#     f"show_{intents.more_results}" : SHOW_MORE_RESULTS_PROMPT,
#     intents.option_selected : OPTION_SELECTED_PROMPT,
#     intents.shown_attributes : SHOWN_ATTRIBUTES_PROMPT,
#     intents.show_suggestions : FIND_SUGGESTIONS_PROMPT,
#     intents.system_response : SYSTEM_PROMPT,
#     intents.in_conversation_system_response : IN_CONVERSATION_SYSTEM_PROMPT,
#     f"prev_intent_{intents.repeat}" : SYSTEM_REPEAT_PROMPT,
#     intents.more_results : MORE_OPTIONS_PROMPT,
#     intents.shown_cart : SHOWN_CART_PROMPT,
#     intents.show_comparison : SHOW_COMPARISON_PROMPT,
#     intents.bought_cart : BOUGHT_CART_PROMPT,
#     intents.clarifying_questions : ASK_CLARIFICATION_PROMPT,
    
#     intents.no_more_clarifying_questions : IN_CONVERSATION_SYSTEM_PROMPT, # no need of prompt
    
#     intents.product_info : SHOW_PRODUCT_PROMPT,
    
    
    
    
#     intents.no_results : 'no_results',



#     # user
#     intents.user_start : START_PROMPT_USER,
#     intents.search_product : SEARCH_PRODUCT_PROMPT,
#     intents.suggest_product : SUGGEST_PRODUCT_PROMPT,
#     intents.more_results : MORE_OPTIONS_PROMPT,
#     intents.select_i : SELECT_I_PROMPT,
#     intents.acknowledge : ACKNOWLEDGE_PROMPT,
#     intents.open_domain_qa : OPEN_DOMAIN_QA_PROMPT,
#     intents.chitchat : CHITCHAT_PROMPT,
#     intents.subjective_qa : SUBJECTIVE_QA_PROMPT,
#     intents.user_start : START_PROMPT_USER,
#     intents.repeat : REPEAT_PROMPT,
#     intents.deny : DENY_PROMPT,
#     intents.stop : STOP_PROMPT,
#     intents.show_cart : SHOW_CART_PROMPT,
#     intents.buy_cart : BUY_CART_PROMPT,
#     intents.remove_from_cart : REMOVE_FROM_CART_PROMPT,
#     intents.remove_from_compare : REMOVE_FROM_COMPARE_PROMPT,
#     intents.add_to_cart : ADD_TO_CART_PROMPT,
#     intents.add_for_compare : ADD_FOR_COMPARE_PROMPT,
#     intents.compare_products : COMPARE_PRODUCTS_PROMPT,
#     intents.generic_product_query : USER_GENERIC_PRODUCT_PROMPT,
#     intents.product_qa : PRODUCT_QA_PROMPT,
#     intents.delivery_address : CHECK_DELIVERY_AVAILABILITY_PROMPT,
#     intents.refine_query : USER_PREFERENCE_PROMPT,
#     intents.show_attributes : SHOW_ATTRIBUTES_BEGIN_PROMPT,
#     intents.show_attributes : ASK_ATTRIBUTES_PROMPT,

# }

slots_map = {
intents.delivery_address : {"text":"", "address": ""},
intents.remove_from_compare : {"text": "", "title": "", "product_id":""},
intents.add_for_compare :  {"text": "", "title": "", "product_id":""},
intents.compare_products : {"text": "", "query": "", "list_of_products":""},
intents.refine_query : {"text": "", "query": "", "attributes_list":"" },
intents.remove_from_cart : {"text": "", "title": "", "product_id":""} , 
intents.add_to_cart : {"text": "", "title": "", "product_id":""} ,
intents.open_domain_qa : {"question": "", "topic": ""},
intents.product_qa : {"question": "", "title": "", "product_id":""},
intents.show_attributes : {"text": "", "title" : "", "product_id" : "" },
intents.search_product: {"text": "", "product_name": "", "query": "", "attributes_list":""}, 
intents.suggest_product : {"text": "", "query": "", "attributes_list":""},

intents.show_results : {"text": "", "product_ids": ["", ""]},
intents.more_results :  {"text": "", "product_ids": ["", ""]},


}

