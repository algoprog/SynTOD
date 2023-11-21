import random
import logging

import matplotlib.pyplot as plt
from constants import *

import csv

logging.getLogger().setLevel(logging.INFO)


def plot_states_frequency(list_of_lists):
    string_counts = {}

    for lst in list_of_lists:
        unique_strings = set(lst)
        for string in unique_strings:
            if string in string_counts:
                string_counts[string] += 1
            else:
                string_counts[string] = 1

    strings = list(string_counts.keys())
    frequencies = list(string_counts.values())

    sorted_indices = sorted(range(len(frequencies)), key=lambda i: frequencies[i], reverse=True)
    sorted_strings = [strings[i] for i in sorted_indices]
    sorted_frequencies = [frequencies[i] for i in sorted_indices]
    max_freq = max(sorted_frequencies)
    sorted_frequencies = [100 * freq / max_freq for freq in sorted_frequencies]

    plt.figure(figsize=(20, 10))
    plt.bar(sorted_strings, sorted_frequencies)
    plt.xlabel('States')
    plt.ylabel('Frequency')
    plt.title('Frequency of states')
    plt.xticks(rotation='vertical')
    plt.subplots_adjust(bottom=0.25)
    plt.show()
    plt.savefig("plot_states_frequency.png")


class TaskPathGenerator:
    def __init__(self, ci_weight=0.1):
        """
        Initializes the TOD agent graph
        :param ci_weight: the probability weight of the common intents during in-task
        """
        # user intents 
        ecomm_start_intents = [
                                    
                                    (intents.search_product, 0.25),  
                                    (intents.suggest_product, 0.23), 
                                    (intents.open_domain_qa, 0.20),  
                                    (intents.chitchat, 0.07),
                                    (intents.subjective_qa, 0.05),
                                    (intents.dangerous_product, 0.03), 
                                    (intents.generic_product_query, 0.07)
                                    ]

        ecomm_in_conversation_intents = [
                                        (intents.more_results, 0.25 * 0.7 * (1 - ci_weight)),
                                        
                                        
                                        (intents.acknowledge, 0.10 * 0.7 * (1 - ci_weight)),
                                        # (intents.add_to_cart, 0.30 * 0.7 * (1 - ci_weight)),   
                                        (intents.refine_query, 0.15 * 0.7 * (1 - ci_weight)),  
                                        (intents.buy_cart, 0.15 * 0.7 * (1 - ci_weight)),   
                                        (intents.delivery_address, 0.05 * 0.7 * (1 - ci_weight)), 
                                        
                                        (intents.product_qa, 0.7 * 0.15 * (1 - ci_weight)), 
                                        (intents.show_attributes, 0.1 * 0.15 * (1 - ci_weight)),  
                                        (intents.repeat, 0.2 * 0.15 * (1 - ci_weight)), 
                                        
                                        (intents.compare_products, 0.55 * 0.15 * (1 - ci_weight)),   
                                        # (intents.add_for_compare, 0.45 * 0.15 * (1 - ci_weight)),   
                    
                                        ]

        ecom_intents_after_selection = [(intents.product_info, 0.2 * (1 - ci_weight)),
                                        (intents.show_attributes, 0.25 * (1 - ci_weight)),
                                        (intents.add_to_cart, 0.3 * (1 - ci_weight)),
                                        (intents.add_for_compare, 0.20 * (1 - ci_weight)),		
                                        (intents.delivery_address, 0.05 * (1 - ci_weight))
                                        ]

        self.graph = {
                    intents.stop: [],

                    # from system states
                    intents.start: ecomm_start_intents,                  

                    intents.show_results: [(intents.select_i, 1.0 * 0.8 * (1 - ci_weight)),
                                    (intents.more_results, 1.0 * 0.15 * (1 - ci_weight)),
                                    (intents.refine_query, 1.0 * 0.05 * (1 - ci_weight) )
                                    ],

                    intents.clarifying_questions : [(intents.no_more_clarifying_questions, 0.3), (intents.clarifying_questions, 0.7)],

                    intents.no_more_clarifying_questions : [(intents.show_results, 1.0)],

                    intents.shown_cart : [(intents.acknowledge, 0.1), (intents.buy_cart, 0.4), (intents.select_i, 0.20), (intents.select_i_remove_from_cart, 0.30)],

                    intents.select_i_remove_from_cart : [(intents.remove_from_cart, 1.0)],
                    


                    intents.shown_attributes: ecomm_in_conversation_intents,

                    intents.show_comparison : [(intents.select_i , ci_weight * 0.40), (intents.select_i_remove_from_compare, ci_weight*0.60) ] + ecomm_in_conversation_intents,

                    intents.select_i_remove_from_compare : [(intents.remove_from_compare,1.0)],
                    

                    intents.option_selected: ecom_intents_after_selection,

                    intents.system_response: ecomm_start_intents,

                    intents.in_conversation_system_response: ecomm_in_conversation_intents,
                    
                    # intents.show_suggestions : [(intents.select_i, 1 * 0.8 * (1 - ci_weight)),
                    #                     (intents.more_results, 1 * 0.15 * (1 - ci_weight)),
                    #                     (intents.refine_query, 1.0 * 0.05 * (1 - ci_weight)),
                    #                     ],
                    intents.product_info : [
                                        (intents.add_to_cart, 0.5 * (1 - ci_weight)),
                                        (intents.add_for_compare, 0.4 * (1 - ci_weight)),
                                        (intents.acknowledge, 0.1*(1-ci_weight))
                                        ],

                    intents.system_response_cart_removal : [(intents.acknowledge, 0.3),(intents.suggest_product, 0.7)],
                    intents.system_response_added_to_cart : [(intents.acknowledge,0.3), (intents.suggest_product, 0.5), (intents.buy_cart, 0.2)],
                    intents.system_response_add_for_compare : [(intents.compare_products, 0.7)] + ecomm_in_conversation_intents,
                    intents.system_response_remove_from_compare : [(intents.compare_products, 0.7)] + ecomm_in_conversation_intents,
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
                    

        #############################################################################################################

                    intents.delivery_address: ecomm_in_conversation_intents, 
                    
                    
                    intents.product_qa: [(intents.select_i, 0.7)] + ecomm_in_conversation_intents, 
                    
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
                    
                    intents.dangerous_product: [(intents.system_response, 1.0)],
                    
                    intents.subjective_qa: [(intents.system_response, 1.0)]
                }
    def generate_path(self, max_length=40, num_clari=5):
        """
        Generates a path of system-user states
        :param max_length: the maximum length of the path
        :param num_clari: the max number of clarification questions in a conversation
        :return: list of state names
        """
        search_intents = [

                        intents.search_product, 
                        intents.suggest_product,
                        intents.refine_query
                          
                          ]
        system_intents = [

                        intents.start,
                        intents.show_results,
                        intents.clarifying_questions,
                        intents.no_more_clarifying_questions,
                        intents.shown_cart,
                        intents.select_i_remove_from_cart,
                        intents.shown_attributes,
                        intents.show_comparison ,
                        intents.select_i_remove_from_compare ,
                        intents.option_selected,
                        intents.system_response,
                        intents.in_conversation_system_response,
                        # intents.show_suggestions,
                        intents.system_response_cart_removal ,
                        intents.system_response_added_to_cart,
                        intents.system_response_add_for_compare ,
                        intents.system_response_remove_from_compare   

                        ]
        started_conversation = False
        finished_product_recommendation = False
        
        selected_product = False
        issued_query = False
        shown_result_pages = 0
        current_node = 'start'
        walk = [current_node]
        
        clarifying_question_number = 0
        
        for _ in range(max_length - 1):
            if current_node == intents.stop:
                break
            
            current_node_name = current_node


            neighbors = self.graph[current_node_name]
            if not neighbors:
                break

            probabilities = [edge[1] * 100 for edge in neighbors]
            s = 0
            for p in probabilities :
                s +=p
            probabilities = [p/s for p in probabilities]
            
            chosen_node, prob = random.choices(neighbors, weights=probabilities, k=1)[0]
            i = 0
            while chosen_node in search_intents and issued_query:
                chosen_node, prob = random.choices(neighbors, weights=probabilities, k=1)[0]
                i +=1
                if(i ==10) :
                    print(f"stuck here!! - current_node_name : {current_node_name} , neighbours: {neighbors}")
            current_node = chosen_node

            system_turn = current_node in system_intents

            
            if current_node == intents.clarifying_questions:
                '''
                    Limit the number of consecutive clarifying questions
                '''
                if clarifying_question_number >= num_clari:
                    current_node = intents.no_more_clarifying_questions
                    clarifying_question_number = 0
                else:
                    clarifying_question_number += 1
            
            if current_node == intents.more_results and shown_result_pages >= 2:
                '''
                    Limit user asking for more results more than twice .. including first one
                    - To avoid endless loops 
                ''' 
                current_node = intents.select_i
            elif current_node == intents.show_results:
                shown_result_pages += 1
            
            
            elif current_node == intents.start:
                started_conversation = True
                
            elif current_node == intents.option_selected:
                selected_product = True
            elif current_node in search_intents:
                started_conversation = False
                issued_query = True
            elif current_node == intents.system_response and started_conversation:
                current_node = intents.in_conversation_system_response
            
            elif not system_turn and selected_product and not started_conversation and random.random() > 0.7:
                '''
                    Product is selected after the query results are shown
                    Will make the user to jump on a different search or just continue 
                '''
                current_node = random.choice([intents.start, intents.acknowledge])
            
            elif not system_turn and not selected_product and random.random() > 0.3 and \
                    current_node not in [intents.select_i, intents.more_results]:
                '''
                    Avoid path to get stuck
                '''
                current_node = random.choice([intents.search_product, intents.suggest_product])

            walk.append(current_node)

        if walk[-1] != 'stop':
            walk.append('stop')

        return walk


if __name__ == '__main__':
    cg = TaskPathGenerator()

    num_paths = 100

    path = cg.generate_path(max_length=30, num_clari=4)

    paths = [cg.generate_path(max_length=30, num_clari=4) for _ in
             range(num_paths)]

    
    file_name = 'generated_paths.csv'

    # Open the file in write mode and use 'csv.writer' to write the data
    with open(file_name, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        
        # Write each row to the CSV file
        for p in paths:
            csv_writer.writerow(p)

    plot_states_frequency(paths)



'''
calrif q only after generic product query 
add generic product q intent
ask chat gpt how many to gen for a query (cq)


'''