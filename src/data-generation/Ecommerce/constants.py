'''
REQUIRED: update appropriate open_ai keys , proper file paths and useapi

'''

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
inventory_with_locations_file = '../../../data/final_product_catalog_added_locations_v0.jsonl'
inventory_file_original_with_description = "../../../data/4k_final_valid_product_catalog.jsonl" #'data/final_valid_product_catalog_v0_with_description.jsonl'

# inventory_file = 'data/final_valid_product_catalog.jsonl'
# inventory_with_locations_file = 'data/final_valid_product_catalog_added_locations_v0.jsonl'
inventory_file_extra = '../../../data/final_valid_product_catalog_extra.jsonl'

combined_inventory_file = '../../../data/combined_valid_product_catalog.jsonl'

inventory_file_4k = "../../../data/4k_final_valid_product_catalog.jsonl" # 'data/4k_valid_product_catalog.jsonl'
inventory_file_train = '../../../data/4k_valid_product_catalog_train.jsonl'
inventory_file_test = '../../../data/4k_valid_product_catalog_test.jsonl'
inventory_100_file_test = '../../../data/4k_valid_100_product_catalog_test.jsonl'

locations = [ "United States", "United Kingdom", "South Africa", "Australia", "India", "Thailand", "Greece", "Bangladesh", "China", "Canada", "Mexico", "France", "Germany", "Japan", "South Korea"]

# provide appropriate openai_key
openai_key = ''

inventory_file = inventory_file_train 
# provide appropriate llm name 
useapi = 'mistral'

class Intents:
    # register all intents here 

    

    def __init__(self) -> None:
        
        # Prompts Present


        # User
        '''
        User Prompt For searching a specific product
        '''
        self.search_product = 'search_product'
        '''
        User Prompt Asking about some product
        '''
        self.suggest_product = 'suggest_product'
        '''
        User Prompt selecting a product from the display
        '''
        self.select_i = 'select_i'
        '''
        User Prompt selecting a product from the cart display and asking to remove the product
        '''
        self.select_i_remove_from_cart = 'select_i_remove_from_cart'
        '''
        User Prompt selecting a product from the compare display and asking to remove the product
        '''
        self.select_i_remove_from_compare = 'select_i_remove_from_compare'
        '''
        User Prompt asking to describe general features of a product
        '''
        self.show_attributes = 'show_attributes'
        '''
        User Prompt acknowledging the reply from taskbot
        '''
        self.acknowledge = 'acknowledge'
        '''
        User Prompt asking open domain questions or questions which require some web search
        '''
        self.open_domain_qa = 'open_domain_qa'
        '''
        User Prompt not loaded with any intent
        '''
        self.chitchat = 'chitchat'
        '''
        User Prompt asking bot about a product on a subjective question
        '''
        self.subjective_qa = 'subjective_qa'
        '''
        User Prompt asking to repeat the revious response from bot
        '''
        self.repeat = 'repeat'
        '''
        User Prompt denying to bot
        '''
        self.deny = 'deny'
        '''
        Prompt to the conversation
        '''
        self.stop = 'stop'
        # self.dangerous_product = 'dangerous_product' # not used


        # User and untracked 
        '''
        User Prompt starting the conversation
        '''
        self.user_start = 'user_start'
        '''
        User Prompt asking to show the cart
        '''
        self.show_cart = 'show_cart'
        '''
        User Prompt asking to buy products present in the cart
        '''
        self.buy_cart = 'buy_cart'
        '''
        User Prompt asking to add a product to the cart
        '''
        self.add_to_cart = 'add_to_cart'
        '''
        User Prompt asking to remove a product from the cart
        '''
        self.remove_from_cart = 'remove_from_cart'
        # self.user_preference = 'user_preference'  # refine query works better for this 
        self.refine_query = 'refine_query' # not required as clarifying questions takes care of it 
        
        '''
        User Prompt asking to compare products in compare list
        '''
        self.compare_products = 'compare_products'
        '''
        User Prompt asking to add product in compare list
        '''
        self.add_for_compare = 'add_for_compare'
        '''
        User Prompt asking to remove products from compare list
        '''
        self.remove_from_compare = 'remove_from_compare'
        '''
        User Prompt asking a very generic product search requests (bot needs more details to start the search)
        '''
        self.generic_product_query = 'generic_product_query'
        '''
        User Prompt asking questions related to a product
        '''
        self.product_qa = 'product_qa'
        '''
        User Prompt asking availability of a product in certain country
        '''
        self.delivery_address = 'delivery_address'
        # self.desc_product = 'describe_product'
        '''
        User Prompt clarifying bot's question regarding a product.
        '''
        self.user_clarifies = 'user_clarifies'

        '''
        User Prompt asking bot to present more results
        '''
        self.more_results = 'more_results'
        


        # system
        '''
        System Prompt to start conversation
        '''
        self.start = 'start'

        '''
        System Prompt showing search results
        '''
        self.show_results = 'show_results' # clubbed with show suggestions
        '''
        System Prompt specifying the product selected by user
        '''
        self.option_selected = 'option_selected'
        '''
        System Prompt showing summary of a product's attributes
        '''
        self.shown_attributes = 'shown_attributes'
        '''
        System Prompt showing search results
        '''
        self.show_suggestions = 'show_suggestions'
        # self.product_info = 'product_info'
        self.delivery_check = 'delivery_check'
        

        # undecided and untracked 

        self.more_options = 'more_options' # ? not used 
        '''
        System Prompt sumarizing the shopping cart
        '''
        self.shown_cart = 'shown_cart'
        '''
        System Prompt stating completion of buying products in a cart
        '''
        self.bought_cart = 'bought_cart'
        '''
        System Prompt comparing the products present in the compare list
        '''
        self.show_comparison = 'show_comparison'
        '''
        System Prompt asking user some clarification questions for refining the product search
        '''
        self.clarifying_questions = 'clarifying_questions'
        
        # not needed
        self.no_more_clarifying_questions = 'no_more_clarifying_questions' #  not needed

        '''
        System Prompt responding to the user
        '''
        self.system_response = 'system_response'


        self.started_conversation = 'started_conversation' # remove ? 
        self.no_results = 'no_results'

        
        
        # No need of prompts for following states: string in string => intent in intent!! 
        # all have single prompt where conv is provided : IN_CONVERSATION_SYSTEM_PROMPT
        '''
        System Prompt which reply to user's question regarding a product
        '''
        self.product_qa_system_response = 'product_qa_system_response'
        '''
        System Prompt comfirming user about removal of a product from cart
        '''
        self.system_response_cart_removal = 'system_response_cart_removal'
        '''
        System Prompt comfirming user about adding a product to the cart
        '''
        self.system_response_added_to_cart = 'system_response_added_to_cart'
        '''
        System Prompt comfirming user about adding a product to the compare list
        '''
        self.system_response_add_for_compare = 'system_response_add_for_compare'
        '''
        System Prompt comfirming user about removal of a product from the compare list
        '''
        self.system_response_remove_from_compare = 'system_response_remove_from_compare'
        
        '''
        System Prompt responding to a general user utterance based on context
        '''
        self.in_conversation_system_response = 'in_conversation_system_response'
        

        
        
        
        
        
        

intents = Intents()



slots_map = {
intents.delivery_address : {"text":"", "address": ""}, # address is just the country name 
intents.select_i_remove_from_compare : {"text": "", "title": "", "product_id":""},
intents.add_for_compare :  {"text": "", "title": "", "product_id":""},
intents.compare_products : {"text": "", "query": "", "list_of_products":""},
intents.refine_query : {"text": "", "query": "", "attributes_list":"" },
intents.select_i_remove_from_cart : {"text": "", "title": "", "product_id":""} , 
intents.add_to_cart : {"text": "", "title": "", "product_id":""} ,
intents.open_domain_qa : {"question": "", "topic": ""},
intents.product_qa : {"question": "", "title": "", "product_id":""},
intents.show_attributes : {"text": "", "title" : "", "product_id" : "" },
intents.search_product: {"text": "", "product_name": "", "query": "", "attributes_list":""}, 
intents.suggest_product : {"text": "", "query": "", "attributes_list":""},

intents.show_results : {"text": "", "product_ids": ["", ""]},
intents.more_results :  {"text": "", "product_ids": ["", ""]},


}

