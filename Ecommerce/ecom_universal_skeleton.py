from constants import *


class UniversalPaths:
    def __init__(self):
        """
        Initializes the TOD agent graph
        :param ci_weight: the probability weight of the common intents during in-task
        """
        # user intents 
        ecomm_start_intents = [
                                    
                                    (intents.search_product, 0.2),  
                                    (intents.suggest_product, 0.2), 
                                    (intents.open_domain_qa, 0.15),  
                                    (intents.chitchat, 0.15),
                                    (intents.subjective_qa, 0.15),
                                    (intents.generic_product_query, 0.15)
                                    ]

        ecomm_in_conversation_intents = [
                                        (intents.more_results, 0.30),
                                        (intents.acknowledge, 0.10),
                                        (intents.refine_query, 0.25 ),  
                                        (intents.buy_cart, 0.15 ),   
                                        (intents.delivery_address, 0.05 ), 
                                        (intents.show_attributes, 0.1 ),  
                                        (intents.repeat, 0.05), 
                                        ]
        ecomm_in_conversation_intents_after_compare_selection = [
                                        (intents.acknowledge, 0.10  ),
                                        (intents.refine_query, 0.25  ),  
                                        (intents.buy_cart, 0.10  ),   
                                        (intents.delivery_address, 0.05  ), 
                                        (intents.product_qa, 0.25  ), 
                                        (intents.repeat, 0.05  ), 
                                        (intents.add_to_cart, 0.20),
                                        ]
        ecomm_in_conversation_intents_after_cart_selection = [
            (intents.refine_query, 0.25  ),
        ]
        ecomm_in_conversation_intents_after_attributes = [
                                        (intents.more_results, 0.30 ),
                                        
                                        
                                        (intents.acknowledge, 0.10 ),
                                        (intents.add_to_cart, 0.05),   
                                        (intents.refine_query, 0.15 ),  
                                        (intents.buy_cart, 0.15 ),   
                                        (intents.delivery_address, 0.05 ), 
                                        
                                        (intents.repeat, 0.2 ), 
                                        
                                        ]
        ecomm_in_conversation_intents_after_compare = [
                                        (intents.more_results, 0.40),
                                        (intents.acknowledge, 0.10),
                                        (intents.refine_query, 0.30  ),  
                                        (intents.buy_cart, 0.15  ),   
                                        (intents.delivery_address, 0.05 ), 
                                        
                                        ]

        ecom_intents_after_selection = [
                                        (intents.product_qa, 0.25 ), 
                                        (intents.show_attributes, 0.10),
                                        (intents.add_to_cart, 0.3),
                                        (intents.add_for_compare, 0.20 ),		
                                        (intents.delivery_address, 0.15 ),
                                        ]

        self.graph = {
                    intents.stop: [],

                    # from system states
                    intents.start: ecomm_start_intents,                  

                    intents.show_results: [(intents.select_i,  0.8 ),
                                    (intents.more_results,  0.15),
                                    (intents.refine_query, 0.05)
                                    ],

                    intents.clarifying_questions : [(intents.no_more_clarifying_questions, 0.3), (intents.clarifying_questions, 0.7)],

                    intents.no_more_clarifying_questions : [(intents.show_results, 1.0)],

                    intents.shown_cart : [(intents.select_i_remove_from_cart, 0.30),(intents.acknowledge, 0.1), (intents.buy_cart, 0.4), (intents.refine_query, 0.25  )] ,
                    intents.select_i_remove_from_cart : [(intents.remove_from_cart, 1.0)],
                    


                    intents.shown_attributes: ecomm_in_conversation_intents_after_attributes,

                    intents.show_comparison : [ (intents.select_i_remove_from_compare, 0.60) ] + self.adjust_by_weight(ecomm_in_conversation_intents_after_compare_selection, 0.4),

                    intents.select_i_remove_from_compare : [(intents.remove_from_compare,1.0)],
                    

                    intents.option_selected: ecom_intents_after_selection,

                    intents.system_response: ecomm_start_intents,

                    intents.in_conversation_system_response: ecomm_in_conversation_intents,
                    
                    intents.product_qa_system_response : [(intents.add_to_cart, 0.4 ),
                                        (intents.add_for_compare, 0.5),
                                        (intents.acknowledge, 0.1 )],

                    intents.system_response_cart_removal : [(intents.acknowledge, 0.3),(intents.suggest_product, 0.7)],
                    intents.system_response_added_to_cart : [(intents.acknowledge,0.05), (intents.show_cart, 0.35) ,  (intents.suggest_product, 0.4), (intents.buy_cart, 0.2)],
                    intents.system_response_add_for_compare : [(intents.compare_products, 0.7)] + self.adjust_by_weight(ecomm_in_conversation_intents_after_compare, 0.3),
                    intents.system_response_remove_from_compare : [(intents.search_product, 0.5), (intents.suggest_product, 0.3), (intents.compare_products, 0.2)] ,
                    # from user states

                    # intents.started_conversation : [(intents.start, 1.0)],
                    
                    
                    intents.suggest_product: [(intents.show_results, 1.0)],
                    
                    intents.show_attributes: [(intents.shown_attributes, 1.0)],
                    intents.generic_product_query:[(intents.clarifying_questions, 1.0 )],  
                    
                    intents.search_product:[(intents.show_results, 1.0 )],  
                    
                    intents.add_to_cart: [(intents.system_response_added_to_cart, 1.0)],   
                    intents.show_cart : [(intents.shown_cart, 1.0)] ,
                    intents.bought_cart : [(intents.stop, 0.9), (intents.suggest_product, 0.1)],

                    intents.remove_from_cart: [(intents.system_response_cart_removal, 1.0)],  
                    
                    intents.buy_cart: [(intents.bought_cart, 1.0)],   

                    intents.compare_products: [(intents.show_comparison, 1.0)],  

                    intents.delivery_check : ecomm_in_conversation_intents, 

                    
        #############################################################################################################

                    intents.delivery_address: [(intents.delivery_check, 1.0)],
                    
                    
                    intents.product_qa: [(intents.product_qa_system_response, 1.0)], 
                    
                    intents.add_for_compare : [(intents.system_response_add_for_compare, 1.0)] ,  
                    
                    intents.remove_from_compare : [(intents.system_response_remove_from_compare, 1.0)],  

                    
        #############################################################################################################
            

                    intents.refine_query: [(intents.show_results, 1.0)],
                    intents.more_results: [(intents.show_results, 1.0)],

                    
                    intents.acknowledge: [(intents.in_conversation_system_response, 1.0)],  # ? 

                    intents.open_domain_qa: [(intents.system_response, 1.0)],
                    
                    intents.select_i: [(intents.option_selected, 1.0)],   # ? 

                    
                    
                    
                    intents.repeat: [(intents.system_response, 1.0)],
                    intents.deny: [(intents.system_response, 1.0)],
                    
                    intents.chitchat: [(intents.system_response, 1.0)],
                    
                    # intents.dangerous_product: [(intents.system_response, 1.0)],
                    
                    intents.subjective_qa: [(intents.system_response, 1.0)]
                }
    
    def adjust_by_weight(self, intents_list, wt =1.0) :
        li = []

        for intent in intents_list :
            li.append((intent[0], intent[1]*wt))
        
        return li


