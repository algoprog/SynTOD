self.start_intents = [
                        ('search_product', 0.5 * 0.7),  # slots : product type , attribute list  - e.g color, specifications 
                        ('suggest_product', 0.5 * 0.7), # slots : product ,  attribute list
                        
                        
                        ('open_domain_qa', 0.2 * 0.3), # slots: topic, topic info?
                        ('chitchat', 0.1 * 0.3),       # 

                        ('offense', 0.7 / 8 * 0.3),    #
                        
                        ('dangerous_product', 0.7 / 8 * 0.3),  # slots:  ? product with dangerous intent in conversation
                        
                        ('suicide_attempt', 0.7 / 8 * 0.3), #
                        ('subjective_qa', 0.7 / 8 * 0.3)    # 
                        ]

self.in_task_intents = [
                        ('more_similar_products', 0.32 * 0.9 * (1 - ci_weight)),
                        
                        ('acknowledge', 0.33 * 0.9 * (1 - ci_weight)),
                        ('add_to_cart', 0.33 * 0.9 * (1 - ci_weight)), # slots: product name
                        ('remove_from_cart', 0.33 * 0.9 * (1 - ci_weight)), # slots: product name
                        ('user_preference', 0.33 * 0.9 * (1 - ci_weight)),  # slots: attributes list
                        ('buy_cart', 0.33 * 0.9 * (1 - ci_weight)),
                        ('delivery_location', 0.33 * 0.9 * (1 - ci_weight)), # slots: location 
                        
                        
                        ('compare_products', 0.5 * 0.7), # slots : products list 
                        
                        ('product_qa', 0.7 * 0.1 * (1 - ci_weight)), # slots : product and question 
                        ('show_attributes', 0.1 * 0.1 * (1 - ci_weight)), # slots: product
                        ('repeat', 0.2 * 0.1 * (1 - ci_weight))          # 
                        ]
'''
clarifing- > decide on no. of Qs.. 5 max, ask gpt to sort attributes based on how likely user will ask q about them
- user clarification
show_results
sys_resp


----
slots wrt intents  - 
'''