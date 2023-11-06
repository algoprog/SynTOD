import random
import logging

import matplotlib.pyplot as plt

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
        # self.common_intents = [

        # ]

        self.start_intents = [
                              
                                
                              ('search_product', 0.25),  # slots : product type , attribute list  - e.g color, specifications 
                              ('suggest_product', 0.25), # slots : product ,  attribute list
                              ('open_domain_qa', 0.20),  # slots: topic, topic info?
                              ('chitchat', 0.10),
                              ('subjective_qa', 0.05),
                              ('offense', 0.05),
                              ('dangerous_product', 0.05), # slots:  ? product with dangerous intent in conversation
                              ('suicide_attempt', 0.05)
                              ]


        self.in_conversation_intents = [
                                ('more_results', 0.20 * 0.7 * (1 - ci_weight)),
                                
                                
                                ('acknowledge', 0.05 * 0.7 * (1 - ci_weight)),
                                ('add_to_cart', 0.25 * 0.7 * (1 - ci_weight)),   # slots: product id
                                ('remove_from_cart', 0.15 * 0.7 * (1 - ci_weight)),  # slots: product id
                                ('user_preference', 0.15 * 0.7 * (1 - ci_weight)),  # slots: attributes list - use relevant attributes - use chatgpt 
                                ('buy_cart', 0.15 * 0.7 * (1 - ci_weight)),   
                                ('delivery_address', 0.05 * 0.7 * (1 - ci_weight)), # slots: address [city state pin code]
                                
                                ('product_qa', 0.7 * 0.15 * (1 - ci_weight)), # slots : product id and question 
                                ('show_attributes', 0.1 * 0.15 * (1 - ci_weight)),  # slots: productid rename intent: show_attributes:-> summarize_product
                                ('repeat', 0.2 * 0.15 * (1 - ci_weight)), 
                                
                                ('compare_products', 0.5 * 0.15 * (1 - ci_weight)),   # slots : products list of ids 
                                ('add_for_compare', 0.30 * 0.15 * (1 - ci_weight)),   # slots: product id
                                ('remove_from_compare', 0.20 * 0.15 * (1 - ci_weight)),  # slots: product id
                                
                                ]

        self.graph = {
            'stop': [],

            # from system states
            'start': self.start_intents,
            'started_conversation' : [('start', 1.0)],
            'buy_cart' : [('conversation_complete',1.0)],
            'user_preference' : [('refine_query',1.0)],

                              

            'show_results': [('select_i', 1.0 * 0.8 * (1 - ci_weight)),
                             ('more_results', 1.0 * 0.15 * (1 - ci_weight)),
                             ('user_preference', 1.0 * 0.05 * (1 - ci_weight) )
                             ],

            'clarifying_questions' : [('no_more_clarifying_questions', 0.3), ('clarifying_questions', 0.7)],

            'no_more_clarifying_questions' : [('refine_query', 1.0)],
            
            'show_suggestions': [('select_i', 1 * 0.8 * (1 - ci_weight)),
                                 ('more_results', 1 * 0.15 * (1 - ci_weight)),
                                 ('user_preference', 1.0 * 0.05 * (1 - ci_weight)),
                                ],
            'show_attributes_begin': [('system_response', 1.0)],
            

            'option_selected': [('product_qa', 0.2 * (1 - ci_weight)),
                                ('show_attributes_begin', 0.2 * (1 - ci_weight)),
                                ('add_to_cart', 0.2 * (1 - ci_weight)),
                                ('add_for_compare', 0.15 * (1 - ci_weight)),		
                                ('remove_from_cart', 0.15 * (1 - ci_weight)),
                                ('remove_from_compare', 0.05 * (1 - ci_weight)),
                                ('delivery_address', 0.05 * (1 - ci_weight))
                                ],

            'conversation_complete': [('end', 1.0)],

            'system_response': self.start_intents,

            'in_conversation_system_response': self.in_conversation_intents,
            'generic_product_query':[('clarifying_questions', 1.0 * (1 - ci_weight))],  
            
            # misc states starting
                                
            'search_product':[('show_results', 1.0 * (1 - ci_weight))],  # slots : product type , attribute list  - e.g color, specifications 
            'suggest_product': [], # slots : product ,  attribute list
            
            # misc states in conversation
            'more_similar_products': [],
            
            'add_to_cart': self.in_conversation_intents,   # slots: product id
            'show_cart' : [('acknowledge', 0.3), ('buy_cart', 0.4), ('select_i', 0.3)] ,
            'remove_from_cart': [('acknowledge', 0.3),('suggest_product', 0.7)],  # slots: product id
            
            'buy_cart': [('acknowledge', 0.3),('stop', 0.7)],   
            'delivery_address': self.in_conversation_intents, # slots: address [city state pin code]
            
            
            'compare_products': [('select_i', 0.5)] + self.in_conversation_intents,   # slots : products list of ids 
            # remove_from_compare	more_results	add_to_cart	product_qa	self.in_conversation_intents
            
            'product_qa': [('select_i', 0.7)] + self.in_conversation_intents, # slots : product id and question 
            
            
            'add_for_compare' : [('compare_products', 0.7)] + self.in_conversation_intents,   # slots: product id
            'remove_from_compare' : [('compare_products', 0.7)] + self.in_conversation_intents,  # slots: product id
            
            # from user states
            'product_recommendation_complete': [('conversation_complete', 0.1)] + self.in_conversation_intents, # more product suggestions?
            # product_recommendation_complete
            'suggest_product': [('show_results', 1.0)],

            'refine_query': [('show_results', 1.0)],
            'more_results': [('show_results', 1.0)],

            
            'acknowledge': [('in_conversation_system_response', 1.0)],  # ? 

            'open_domain_qa': [('system_response', 1.0)],
            
            'select_i': [('option_selected', 1.0)],   # ? 

            
            'show_attributes': [('system_response', 1.0)],
            
            
            'repeat': [('system_response', 1.0)],
            'deny': [('system_response', 1.0)],
            
            'chitchat': [('system_response', 1.0)],
            'offense': [('system_response', 1.0)],
            
            'nsfw': [('system_response', 1.0)], # ? 
            
            'dangerous_product': [('system_response', 1.0)],
            'personal_information': [('system_response', 1.0)],
            'suicide_attempt': [('system_response', 1.0)],
            'subjective_qa': [('system_response', 1.0)]
        }

    def generate_path(self, max_length=40, num_clari=5):
        """
        Generates a path of system-user states
        :param max_length: the maximum length of the path
        :param num_clari: the max number of clarification questions in a conversation
        :return: list of state names
        """
        search_intents = ['search_product', 'suggest_product']
        system_intents = ['system_response', 'in_conversation_system_response', 'show_results', 'show_suggestions', 
                          'option_selected', 'started_conversation', 'product_recommendation_complete']
        started_conversation = False
        finished_product_recommendation = False
        
        selected_product = False
        issued_query = False
        shown_result_pages = 0
        current_node = 'start'
        walk = [current_node]
        
        clarifying_question_number = 0
        
        for _ in range(max_length - 1):
            if current_node == 'end':
                break
            
            current_node_name = current_node


            # current_node_name = 'goto_step' if 'goto_step' in current_node else current_node # ?
            if finished_product_recommendation and current_node_name in system_intents and current_node_name != 'conversation_complete':
                current_node_name = 'product_recommended'
            neighbors = self.graph[current_node_name]
            if not neighbors:
                break

            probabilities = [edge[1] * 100 for edge in neighbors]
            # if current_node_name == 'user_preference':
            #     print(f"here")

            chosen_node, prob = random.choices(neighbors, weights=probabilities, k=1)[0]
            i = 0
            while chosen_node in search_intents and issued_query:
                chosen_node, prob = random.choices(neighbors, weights=probabilities, k=1)[0]
                i +=1
                if(i ==10) :
                    print(f"stuck here!! - current_node_name : {current_node_name} , neighbours: {neighbors}")
            current_node = chosen_node

            system_turn = current_node in system_intents

            if current_node == 'clarifying_questions':
                if clarifying_question_number == num_clari:
                    current_node = 'no_more_clarifying_questions'
                    clarifying_question_number = 0
                else:
                    clarifying_question_number += 1
            
            if current_node == 'more_results' and shown_result_pages == 2:
                current_node = 'select_i'
            elif current_node == 'show_results':
                shown_result_pages += 1
            
            
            elif current_node == 'started_conversation':
                started_conversation = True
                
            elif current_node == 'option_selected':
                selected_product = True
            elif current_node in search_intents:
                started_conversation = False
                issued_query = True
            elif current_node == 'system_response' and started_conversation:
                current_node = 'in_conversation_system_response'
            elif not system_turn and selected_product and not started_conversation and random.random() > 0.3:
                current_node = random.choice(['started_conversation', 'acknowledge'])
            elif not system_turn and not selected_product and random.random() > 0.3 and \
                    current_node not in ['select_i', 'more_results']:
                current_node = random.choice(['search_product', 'suggest_product'])

            walk.append(current_node)

        if walk[-1] != 'end':
            #walk.append('stop')
            walk.append('end')

        walk_final = []
        for w in walk:
            if w == 'show_attributes_begin':
                w = 'show_attributes'
            # if w == 'system_response_begin':
            #     w = 'system_response'
            walk_final.append(w)

        return walk_final


if __name__ == '__main__':
    cg = TaskPathGenerator()

    num_paths = 50

    paths = [cg.generate_path(max_length=30, num_clari=4) for _ in
             range(num_paths)]

    for p in paths[:20]:
        print(' -> '.join(p))

    plot_states_frequency(paths)



'''
calrif q only after generic product query 
add generic product q intent
ask chat gpt how many to gen for a query (cq)


'''