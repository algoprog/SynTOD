
prompt = 'prompt'
json_format = 'json_format'

product = 'product'
recipe = 'recipe'
popo = product
attributes = 'attributes'
title = 'title'
rating = 'overall'
ratingCount = 'vote'

openai_keys = ['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']

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
        self.dangerous_product = 'dangerous_product'


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
        

        # undecided and untracked 

        self.more_options = 'more_options' # ?
        self.shown_cart = 'shown_cart'
        self.bought_cart = 'bought_cart'
        self.show_comparison = 'show_comparison'
        self.clarifying_questions = 'clarifying_questions'
        self.no_more_clarifying_questions = 'no_more_clarifying_questions' # no need of prompt
        self.system_response = 'system_response'


        # No need of prompts for following states:

        self.system_response_cart_removal = 'system_response_cart_removal'
        self.system_response_added_to_cart = 'system_response_added_to_cart'
        self.system_response_add_for_compare = 'system_response_add_for_compare'
        self.system_response_remove_from_compare = 'system_response_remove_from_compare'
        self.started_conversation = 'started_conversation' # remove ? 
        self.in_conversation_system_response = 'in_conversation_system_response'
        
        
        

intents = Intents()


