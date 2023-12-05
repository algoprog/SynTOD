from constants import *

from ecom_universal_skeleton import UniversalPaths


class AltTaskPathGenerator(UniversalPaths) :
    def __init__(self):
        
        # user intents 
        ecomm_start_intents = [
            (intents.search_product, 0.3),  
            (intents.suggest_product, 0.3), 
            (intents.open_domain_qa, 0.30),
            (intents.chitchat, 0.10)  
            ]

        ecomm_in_conversation_intents = [
                                        (intents.more_results, 0.30),
                                        # (intents.acknowledge, 0.10),
                                        (intents.refine_query, 0.35 ),  
                                        (intents.buy_cart, 0.15 ),   
                                        (intents.delivery_address, 0.05 ), 
                                        (intents.show_attributes, 0.1 ),  
                                        (intents.repeat, 0.05), 
                                        ]
        ecomm_in_conversation_intents_after_compare_selection = [
                                        (intents.acknowledge, 0.05  ),
                                        (intents.refine_query, 0.25  ),  
                                        (intents.buy_cart, 0.15  ),   
                                        (intents.product_qa, 0.35  ), 
                                        (intents.add_to_cart, 0.20),
                                        ]
        
        ecomm_in_conversation_intents_after_attributes = [
                                        (intents.more_results, 0.15 ),
                                        (intents.acknowledge, 0.10 ),
                                        (intents.add_to_cart, 0.15),   
                                        (intents.refine_query, 0.15 ),  
                                        (intents.buy_cart, 0.15 ),   
                                        (intents.delivery_address, 0.10 ), 
                                        (intents.repeat, 0.2 ), 
                                        ]
        ecomm_in_conversation_intents_after_compare = [
                                        (intents.suggest_product, 0.40),
                                        (intents.search_product, 0.30),
                                        (intents.refine_query, 0.30),  
                                        ]

        ecom_intents_after_selection = [
                                        (intents.product_qa, 0.3 ), 
                                        (intents.add_to_cart, 0.3),
                                        (intents.add_for_compare, 0.3 ),		
                                        (intents.delivery_address, 0.1 ),
                                        ]

        self.graph = {
                    intents.stop: [],

                    # from system states
                    intents.start: ecomm_start_intents,                  

                    intents.show_results: [(intents.select_i,  0.8 ),
                                    (intents.more_results,  0.15),
                                    (intents.refine_query, 0.05)
                                    ],

                    intents.shown_cart : [(intents.select_i_remove_from_cart, 0.30),(intents.acknowledge, 0.1), (intents.buy_cart, 0.4), (intents.refine_query, 0.25  )] ,
                    
                    intents.shown_attributes: ecomm_in_conversation_intents_after_attributes,

                    intents.show_comparison : [ (intents.select_i_remove_from_compare, 0.65) ] + self.adjust_by_weight(ecomm_in_conversation_intents_after_compare_selection, 0.35),


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

                    intents.suggest_product: [(intents.show_results, 1.0)],
                    
                    intents.show_attributes: [(intents.shown_attributes, 1.0)],
                    
                    intents.search_product:[(intents.show_results, 1.0 )],  
                    
                    intents.add_to_cart: [(intents.system_response_added_to_cart, 1.0)],   
                    intents.show_cart : [(intents.shown_cart, 1.0)] ,
                    intents.bought_cart : [(intents.stop, 0.9), (intents.suggest_product, 0.1)],

                    intents.select_i_remove_from_cart: [(intents.system_response_cart_removal, 1.0)],  
                    
                    intents.buy_cart: [(intents.bought_cart, 1.0)],   

                    intents.compare_products: [(intents.show_comparison, 1.0)],  

                    intents.delivery_check : ecomm_in_conversation_intents, 

                    
        #############################################################################################################

                    intents.delivery_address: [(intents.delivery_check, 1.0)],
                    
                    
                    intents.product_qa: [(intents.product_qa_system_response, 1.0)], 
                    
                    intents.add_for_compare : [(intents.system_response_add_for_compare, 1.0)] ,  
                    
                    intents.select_i_remove_from_compare : [(intents.system_response_remove_from_compare, 1.0)],  

                    
        #############################################################################################################
            

                    intents.refine_query: [(intents.show_results, 1.0)],
                    intents.more_results: [(intents.show_results, 1.0)],

                    
                    intents.acknowledge: [(intents.in_conversation_system_response, 1.0)],  # ? 

                    intents.open_domain_qa: [(intents.system_response, 1.0)],
                    
                    intents.select_i: [(intents.option_selected, 1.0)],   # ? 

                    
                    
                    
                    intents.repeat: [(intents.system_response, 1.0)],
                    intents.chitchat: [(intents.system_response, 1.0)],
                    
                }
