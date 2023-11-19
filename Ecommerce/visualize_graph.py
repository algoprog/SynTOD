import networkx as nx
import matplotlib.pyplot as plt
from constants import *



def visualizeGraph(graph) :
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes and edges from your graph definition
    for node, edges in graph.items():
        for edge, weight in edges:
            G.add_edge(node, edge) # , weight=weight

    # Define node positions for better layout
    pos = nx.spring_layout(G)

    # Draw the graph # 
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=10, font_color='black', font_weight='bold', arrowsize=20)

    # Add edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, 'weight') # 
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    # Show the plot
    plt.show()


ci_weight  = 0.5

#############################################################################################################

# # user intents 
# ecomm_start_intents = [
                              
#                               (intents.search_product, 0.25),  # slots : product type , attribute list  - e.g color, specifications 
#                               (intents.suggest_product, 0.23), # slots : product ,  attribute list
#                               (intents.open_domain_qa, 0.20),  # slots: topic, topic info?
#                               (intents.chitchat, 0.07),
#                               (intents.subjective_qa, 0.05),
#                               (intents.dangerous_product, 0.03), # slots:  ? product with dangerous intent in conversation
#                               (intents.generic_product_query, 0.07)
#                               ]

# ecomm_in_conversation_intents = [
#                                 (intents.more_results, 0.20 * 0.7 * (1 - ci_weight)),
                                
                                
#                                 (intents.acknowledge, 0.05 * 0.7 * (1 - ci_weight)),
#                                 (intents.add_to_cart, 0.25 * 0.7 * (1 - ci_weight)),   # slots: product id
#                                 (intents.remove_from_cart, 0.15 * 0.7 * (1 - ci_weight)),  # slots: product id
#                                 (intents.user_preference, 0.15 * 0.7 * (1 - ci_weight)),  # slots: attributes list - use relevant attributes - use chatgpt 
#                                 (intents.buy_cart, 0.15 * 0.7 * (1 - ci_weight)),   
#                                 (intents.delivery_address, 0.05 * 0.7 * (1 - ci_weight)), # slots: address [city state pin code]
                                
#                                 (intents.product_qa, 0.7 * 0.15 * (1 - ci_weight)), # slots : product id and question 
#                                 (intents.show_attributes, 0.1 * 0.15 * (1 - ci_weight)),  # slots: productid rename intent: show_attributes:-> summarize_product
#                                 (intents.repeat, 0.2 * 0.15 * (1 - ci_weight)), 
                                
#                                 (intents.compare_products, 0.5 * 0.15 * (1 - ci_weight)),   # slots : products list of ids 
#                                 (intents.add_for_compare, 0.30 * 0.15 * (1 - ci_weight)),   # slots: product id
#                                 (intents.remove_from_compare, 0.20 * 0.15 * (1 - ci_weight)),  # slots: product id
                                
#                                 ]

# ecom_intents_after_selection = [(intents.product_qa, 0.2 * (1 - ci_weight)),
#                                 (intents.show_attributes, 0.2 * (1 - ci_weight)),
#                                 (intents.add_to_cart, 0.2 * (1 - ci_weight)),
#                                 (intents.add_for_compare, 0.15 * (1 - ci_weight)),		
#                                 (intents.remove_from_cart, 0.15 * (1 - ci_weight)),
#                                 (intents.remove_from_compare, 0.05 * (1 - ci_weight)),
#                                 (intents.delivery_address, 0.05 * (1 - ci_weight))
#                                 ]

# graph_ecomm = {
#             intents.stop: [],

#             # from system states
#             intents.start: ecomm_start_intents,                  

#             intents.show_results: [(intents.select_i, 1.0 * 0.8 * (1 - ci_weight)),
#                              (intents.more_results, 1.0 * 0.15 * (1 - ci_weight)),
#                              (intents.user_preference, 1.0 * 0.05 * (1 - ci_weight) )
#                              ],

#             intents.clarifying_questions : [(intents.no_more_clarifying_questions, 0.3), (intents.clarifying_questions, 0.7)],

#             intents.no_more_clarifying_questions : [(intents.refine_query, 1.0)],

#             intents.shown_cart : [(intents.acknowledge, 0.3), (intents.buy_cart, 0.4), (intents.select_i, 0.3)],
            


#             intents.shown_attributes: ecomm_in_conversation_intents,

#             intents.show_comparison : [(intents.select_i , 0.5)] + ecomm_in_conversation_intents,

            
            

#             intents.option_selected: ecom_intents_after_selection,

#             intents.system_response: ecomm_start_intents,

#             intents.in_conversation_system_response: ecomm_in_conversation_intents,
            
#             intents.show_suggestions : [(intents.select_i, 1 * 0.8 * (1 - ci_weight)),
#                                  (intents.more_results, 1 * 0.15 * (1 - ci_weight)),
#                                  (intents.user_preference, 1.0 * 0.05 * (1 - ci_weight)),
#                                 ],

#             intents.system_response_cart_removal : [(intents.acknowledge, 0.3),(intents.suggest_product, 0.7)],
#             intents.system_response_added_to_cart : [(intents.acknowledge,0.3), (intents.suggest_product, 0.5), (intents.buy_cart, 0.2)],
#             intents.system_response_add_for_compare : [(intents.compare_products, 0.7)] + ecomm_in_conversation_intents,
#             intents.system_response_remove_from_compare : [(intents.compare_products, 0.7)] + ecomm_in_conversation_intents,
#             # from user states

#             intents.started_conversation : [(intents.start, 1.0)],
            
            
#             intents.suggest_product: [(intents.show_suggestions, 1.0)],
#             intents.user_preference : [(intents.refine_query,1.0)],
#             intents.show_attributes: [(intents.shown_attributes, 1.0)],
#             intents.generic_product_query:[(intents.clarifying_questions, 1.0 )],  
            
#             intents.search_product:[(intents.show_results, 1.0 )],  # slots : product type , attribute list  - e.g color, specifications 
            
#             intents.add_to_cart: [(intents.system_response_added_to_cart, 1.0)],   # slots: product id
#             intents.show_cart : [(intents.shown_cart, 1.0)] ,
#             intents.bought_cart : [(intents.stop, 0.9), (intents.suggest_product, 0.1)],

#             intents.remove_from_cart: [(intents.system_response_cart_removal, 1.0)],  # slots: product id
            
#             intents.buy_cart: [(intents.bought_cart, 1.0)],   

#             intents.compare_products: [(intents.show_comparison, 1.0)],   # slots : products list of ids 
            

# #############################################################################################################

#             intents.delivery_address: ecomm_in_conversation_intents, # slots: address [city state pin code] # can't we treat this as an attribute?
            
            
            
#             intents.product_qa: [(intents.select_i, 0.7)] + ecomm_in_conversation_intents, # slots : product id and question 
            
            
#             intents.add_for_compare : [(intents.system_response_add_for_compare, 1.0)] ,   # slots: product id
            
#             intents.remove_from_compare : [(intents.system_response_remove_from_compare, 1.0)],  # slots: product id
            
# #############################################################################################################
     

#             intents.refine_query: [(intents.show_results, 1.0)],
#             intents.more_results: [(intents.show_results, 1.0)],

            
#             intents.acknowledge: [(intents.in_conversation_system_response, 1.0)],  # ? 

#             intents.open_domain_qa: [(intents.system_response, 1.0)],
            
#             intents.select_i: [(intents.option_selected, 1.0)],   # ? 

            
            
            
#             intents.repeat: [(intents.system_response, 1.0)],
#             intents.deny: [(intents.system_response, 1.0)],
            
#             intents.chitchat: [(intents.system_response, 1.0)],
            
#             intents.dangerous_product: [(intents.system_response, 1.0)],
            
#             intents.subjective_qa: [(intents.system_response, 1.0)]
#         }




common_intents = [
            #('search_recipe', 0.2 * 0.05 * ci_weight),
            #('suggest_recipe', 0.2 * 0.05 * ci_weight),
            #('refine_query', 0.1 * 0.05 * ci_weight),
            #('search_task', 0.5 * 0.05 * ci_weight),

            ('open_domain_qa', 0.4 * 1.0 * ci_weight),
            ('chitchat', 0.2 * 1.0 * ci_weight),
            ('set_timer', 0.05 * 1.0 * ci_weight),
            ('deny', 0.05 * 1.0 * ci_weight),

            ('offense', 0.3 / 8 * 1.0 * ci_weight),
            #('nsfw', 0.2 / 11 * 1.0 * ci_weight),
            #('illegal_action', 0.2 / 10 * 1.0 * ci_weight),
            #('unhealthy_action', 0.2 / 10 * 1.0 * ci_weight),
            ('legal_advice', 0.3 / 8 * 1.0 * ci_weight),
            ('financial_advice', 0.3 / 8 * 1.0 * ci_weight),
            ('medical_advice', 0.3 / 8 * 1.0 * ci_weight),
            ('dangerous_task', 0.3 / 8 * 1.0 * ci_weight),
            ('personal_information', 0.3 / 8 * 1.0 * ci_weight),
            ('suicide_attempt', 0.3 / 8 * 1.0 * ci_weight),
            ('subjective_qa', 0.3 / 8 * 1.0 * ci_weight)
        ]


start_intents = [('search_recipe', 0.5 * 0.7),
                              ('suggest_recipe', 0.5 * 0.7),
                              #('search_task', 0.5 * 0.7),

                              ('open_domain_qa', 0.2 * 0.3),
                              ('chitchat', 0.1 * 0.3),

                              ('offense', 0.7 / 8 * 0.3),
                              #('nsfw', 0.7 / 11 * 0.3),
                              #('illegal_action', 0.7 / 11 * 0.3),
                              #('unhealthy_action', 0.7 / 11 * 0.3),
                              ('legal_advice', 0.7 / 8 * 0.3),
                              ('financial_advice', 0.7 / 8 * 0.3),
                              ('medical_advice', 0.7 / 8 * 0.3),
                              ('dangerous_task', 0.7 / 8 * 0.3),
                              ('personal_information', 0.7 / 8 * 0.3),
                              ('suicide_attempt', 0.7 / 8 * 0.3),
                              ('subjective_qa', 0.7 / 8 * 0.3)
                              ]

in_task_intents = [('done_step', 0.32 * 0.9 * (1 - ci_weight)),
                                ('next_step', 0.32 * 0.9 * (1 - ci_weight)),
                                ('acknowledge_step', 0.33 * 0.9 * (1 - ci_weight)),
                                ('goto_step', 0.03 * 0.9 * (1 - ci_weight)),

                                ('in_task_qa', 0.7 * 0.1 * (1 - ci_weight)),
                                ('show_ingredients', 0.1 * 0.1 * (1 - ci_weight)),
                                ('repeat', 0.2 * 0.1 * (1 - ci_weight))
                                ]

recipe_graph = {
            'stop': [],

            # from system states
            'start': start_intents,

            'show_results': [('select_i', 1 * 0.8 * (1 - ci_weight)),
                             ('more_results', 1 * 0.2 * (1 - ci_weight)),
                             ],
            
            'show_suggestions': [('select_i', 1 * 0.8 * (1 - ci_weight)),
                                 ('more_results', 1 * 0.2 * (1 - ci_weight)),
                                ],

            'option_selected': [('begin_task', 0.6 * (1 - ci_weight)),
                                ('show_ingredients_begin', 0.4 * (1 - ci_weight))
                                ] + common_intents,

            'started_task': in_task_intents + common_intents,

            'show_step': in_task_intents + common_intents,

            'no_more_steps': [('finish_task', 0.8 * (1 - ci_weight)), 
                              ('in_task_qa', 0.2 * (1 - ci_weight))] + common_intents,

            'task_complete': [('end', 1.0)],

            'system_response_begin': [('begin_task', 1.0)],

            'system_response': common_intents,
            'in_task_system_response': in_task_intents + common_intents,

            # from user states
            'finish_task': [('task_complete', 1.0)],
            'search_recipe': [('show_results', 1.0)],
            'search_task': [('show_results', 1.0)],
            'suggest_recipe': [('show_suggestions', 1.0)],
            'refine_query': [('show_results', 1.0)],
            'more_results': [('show_results', 1.0)],

            'begin_task': [('started_task', 1.0)],
            'acknowledge_task': [('started_task', 1.0)],

            'open_domain_qa': [('system_response', 1.0)],
            'in_task_qa': [('system_response', 1.0)],
            'select_i': [('option_selected', 1.0)],

            'done_step': [('show_step', 1.0)],
            'next_step': [('show_step', 1.0)],
            'acknowledge_step': [('show_step', 1.0)],
            'goto_step': [('show_step', 1.0)],

            'task_overview': [('system_response', 1.0)],
            'show_ingredients': [('system_response', 1.0)],
            'show_ingredients_begin': [('system_response_begin', 1.0)],
            'show_image': [('system_response', 1.0)],
            'show_video': [('system_response', 1.0)],
            'repeat': [('system_response', 1.0)],
            'deny': [('system_response', 1.0)],
            'set_timer': [('system_response', 1.0)],
            'chitchat': [('system_response', 1.0)],
            'offense': [('system_response', 1.0)],
            'nsfw': [('system_response', 1.0)],
            'illegal_action': [('system_response', 1.0)],
            'unhealthy_action': [('system_response', 1.0)],
            'legal_advice': [('system_response', 1.0)],
            'financial_advice': [('system_response', 1.0)],
            'medical_advice': [('system_response', 1.0)],
            'dangerous_task': [('system_response', 1.0)],
            'personal_information': [('system_response', 1.0)],
            'suicide_attempt': [('system_response', 1.0)],
            'subjective_qa': [('system_response', 1.0)]
        }



# visualizeGraph(recipe_graph)
# visualizeGraph(graph_ecomm)
