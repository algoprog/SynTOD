import random
import logging

import matplotlib.pyplot as plt
from constants import *
from ecom_path_skeleton import UniversalPaths, AltTaskPathGenerator

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
    sum_freq = sum(sorted_frequencies)
    max_freq = max(sorted_frequencies)
    sorted_frequencies = [ freq  for freq in sorted_frequencies]

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
    def __init__(self, graph , ci_weight=0.1):
        self.graph = graph
    

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
        
        selected_product = False
        issued_query = False
        shown_result_pages = 0
        current_node = 'start'
        walk = [current_node]
        
        clarifying_question_number = 0
        products_in_compare_list = 0
        products_in_cart = 0

        
        for _ in range(max_length - 1):
            if current_node == intents.stop:
                break
            
            current_node_name = current_node

            if current_node == intents.add_for_compare :
                products_in_compare_list +=1
            if current_node == intents.select_i_remove_from_compare :
                products_in_compare_list -=1
                if(products_in_compare_list < 0) :
                    products_in_compare_list = 0
            if current_node == intents.add_to_cart :
                products_in_cart +=1
            if current_node == intents.select_i_remove_from_cart :
                products_in_cart -=1


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
                    print(f"stuck at search!! - current_node_name : {current_node_name} , neighbours: {neighbors}")
            
            while chosen_node in [intents.compare_products, intents.select_i_remove_from_compare ] and products_in_compare_list < 2:
                chosen_node, prob = random.choices(neighbors, weights=probabilities, k=1)[0]
                i +=1
                if(i%10 ==0) :
                    print(f"stuck at compare!! - current_node_name : {current_node_name} , neighbours: {neighbors}")
            
            
            while chosen_node in [intents.buy_cart, intents.select_i_remove_from_cart] and products_in_cart < 1:
                chosen_node, prob = random.choices(neighbors, weights=probabilities, k=1)[0]
                i +=1
                if(i ==10) :
                    print(f"stuck at cart!! - current_node_name : {current_node_name} , neighbours: {neighbors}")
            
            
            while chosen_node == intents.buy_cart and products_in_cart < 1:
                chosen_node, prob = random.choices(neighbors, weights=probabilities, k=1)[0]
                i +=1
                if(i ==10) :
                    print(f"stuck at cart!! - current_node_name : {current_node_name} , neighbours: {neighbors}")
            
            
            
            
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
    
    def get_path_from_file(self, pos, filename) :
        '''
        pos is indexed from 0
        '''
        walks = []
        walk = []
        with open(filename, newline='') as csvfile:
            # Create a CSV reader
            csv_reader = csv.reader(csvfile)
            
            # Iterate through each row in the CSV file
            for row in csv_reader:
                # 'row' variable contains each row as a list
                # print(row)  # Or perform any operations with the row list
                walks.append(row)
        walk = walks[pos]
        return walk


if __name__ == '__main__':

    # skeleton = UniversalPaths()
    skeleton = AltTaskPathGenerator()
    cg = TaskPathGenerator(graph = skeleton.graph)

    num_paths = 100

    # path = cg.generate_path(max_length=30, num_clari=4)

    paths = [cg.generate_path(max_length=40, num_clari=4) for _ in
             range(num_paths)]

    
    file_name = 'generated_paths_alt.csv'

    # paths = [ cg.get_path_from_file(pos, file_name) for pos in range(num_paths) ]

    # Open the file in write mode and use 'csv.writer' to write the data
    with open(file_name, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        
        # Write each row to the CSV file
        for p in paths:
            csv_writer.writerow(p)

    # # plot_states_frequency(paths)
    # selected_paths = [0,2,3,5,6,8,10,18,21,39]
    # for pos in selected_paths :
    #     print(paths[pos])

    # for p in paths[:20]:
    #     print(' -> '.join(p))

    plot_states_frequency(paths)



'''
calrif q only after generic product query 
add generic product q intent
ask chat gpt how many to gen for a query (cq)





# need to handle aux state trackers 
        # not used any more!!!
        elif intent == intents.remove_from_compare:
            prdt = other_product
            if prdt == None:
                prdt = aux_compare[compare_i]
            product_info_oth = self.product_to_string(prdt)
            # compare_i -=1
            last_shown_options_string = args['last_shown_options_string']
            if last_shown_options_string == None :
                last_shown_options_string = args['bot']
            prompt = REMOVE_FROM_COMPARE_PROMPT['prompt'].format(prdt,last_shown_options_string)
            
            if 'compare_list' in args.keys() :
                compare_list = args['compare_list']
                compare_list.remove(prdt)
                other_product = prdt
            
            # model = gpt_4
        # need to handle aux state trackers 
        # not used any more!!!
        elif intent == intents.remove_from_cart:
            prdt = other_product
            if prdt == None: # or prdt not in aux_cart
                prdt = aux_cart[cart_i]
            # cart_i -=1
            product_info = self.product_to_string(prdt)
            last_shown_options_string = args['last_shown_options_string']
            if last_shown_options_string == None :
                last_shown_options_string = args['bot']
            prompt = REMOVE_FROM_CART_PROMPT['prompt'].format(prdt,last_shown_options_string)
            
            if 'cart' in args.keys():
                cart = args['cart']
                cart.remove(prdt)
                other_product = prdt
'''