import networkx as nx
import matplotlib.pyplot as plt
from constants import *
from ecom_path_skeleton import UniversalPaths, AltTaskPathGenerator


def visualizeGraph(graph) :
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes and edges from your graph definition
    for node, edges in graph.items():
        for edge, weight in edges:
            G.add_edge(node, edge) # , weight=weight

    # Define node positions for better layout
    # pos = nx.spring_layout(G, scale=0.05, iterations=10)
    pos = nx.kamada_kawai_layout(G, scale = 5, dim = 2)
    # pos = nx.nx_pydot.graphviz_layout(G, prog="dot") # , prog="dot"
    # pos = nx.nx_pydot.pydot_layout(G ) # , prog="dot"
    # pos = nx.circular_layout(G)
    # pos = nx.nx_pydot.graphviz_layout(G)
    # pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
    # pos = nx.planar_layout(G)
    
    # label_pos = {node:(coords[0], coords[1]-0.05) for node,coords in pos.items()}

    # Draw the graph # 
    # nx.draw(G, pos, with_labels=False)
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=10, font_color='black', font_weight='bold', arrowsize=8)
    # nx.draw_networkx_labels(G, label_pos)


    # Add edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, 'weight') # 
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    nx.write_gexf(G, 'data/ecom_graph_visualize.gexf', version="1.2draft")

    # Show the plot
    plt.show()


ci_weight  = 0.5





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



skeleton = AltTaskPathGenerator()

# visualizeGraph(recipe_graph)
visualizeGraph(skeleton.graph)
