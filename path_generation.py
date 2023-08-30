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


class TaskPathGenerator:
    def __init__(self, ci_weight=0.1):
        """
        Initializes the TOD agent graph
        :param ci_weight: the probability weight of the common intents during in-task
        """
        self.common_intents = [
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

        self.start_intents = [('search_recipe', 0.5 * 0.7),
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

        self.in_task_intents = [('done_step', 0.32 * 0.9 * (1 - ci_weight)),
                                ('next_step', 0.32 * 0.9 * (1 - ci_weight)),
                                ('acknowledge_step', 0.33 * 0.9 * (1 - ci_weight)),
                                ('goto_step', 0.03 * 0.9 * (1 - ci_weight)),

                                ('in_task_qa', 0.7 * 0.1 * (1 - ci_weight)),
                                ('show_ingredients', 0.1 * 0.1 * (1 - ci_weight)),
                                ('repeat', 0.2 * 0.1 * (1 - ci_weight))
                                ]

        self.graph = {
            'stop': [],

            # from system states
            'start': self.start_intents,

            'show_results': [('select_i', 1 * 0.8 * (1 - ci_weight)),
                             ('more_results', 1 * 0.2 * (1 - ci_weight)),
                             ],
            
            'show_suggestions': [('select_i', 1 * 0.8 * (1 - ci_weight)),
                                 ('more_results', 1 * 0.2 * (1 - ci_weight)),
                                ],

            'option_selected': [('begin_task', 0.6 * (1 - ci_weight)),
                                ('show_ingredients_begin', 0.4 * (1 - ci_weight))
                                ] + self.common_intents,

            'started_task': self.in_task_intents + self.common_intents,

            'show_step': self.in_task_intents + self.common_intents,

            'no_more_steps': [('finish_task', 0.8 * (1 - ci_weight)), 
                              ('in_task_qa', 0.2 * (1 - ci_weight))] + self.common_intents,

            'task_complete': [('end', 1.0)],

            'system_response_begin': [('begin_task', 1.0)],

            'system_response': self.common_intents,
            'in_task_system_response': self.in_task_intents + self.common_intents,

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

    def generate_path(self, max_length=40, num_steps=4):
        """
        Generates a path of system-user states
        :param max_length: the maximum length of the path
        :param num_steps: the number of steps of given task (should be defined internally for suggest queries)
        :return: list of state names
        """
        search_intents = ['search_recipe', 'suggest_recipe', 'refine_query', 'search_task']
        system_intents = ['system_response', 'system_response_begin', 'in_task_system_response', 'show_results', 'show_suggestions', 
                          'option_selected', 'started_task', 'show_step', 'no_more_steps', 'task_complete']
        started_task = False
        finished_task = False
        selected_task = False
        issued_query = False
        shown_result_pages = 0
        current_node = 'start'
        walk = [current_node]
        current_step = 0

        for _ in range(max_length - 1):
            if current_node == 'end':
                break

            current_node_name = 'goto_step' if 'goto_step' in current_node else current_node
            if finished_task and current_node_name in system_intents and current_node_name != 'task_complete':
                current_node_name = 'no_more_steps'
            neighbors = self.graph[current_node_name]
            if not neighbors:
                break

            probabilities = [edge[1] * 100 for edge in neighbors]

            chosen_node, prob = random.choices(neighbors, weights=probabilities, k=1)[0]
            while chosen_node in search_intents and issued_query:
                chosen_node, prob = random.choices(neighbors, weights=probabilities, k=1)[0]
            current_node = chosen_node

            system_turn = current_node in system_intents

            if current_node == 'show_step':
                if current_step == num_steps:
                    current_node = 'no_more_steps'
                    finished_task = True
                else:
                    current_step += 1
            if current_node == 'more_results' and shown_result_pages == 2:
                current_node = 'select_i'
            elif current_node == 'show_results':
                shown_result_pages += 1
            elif current_node == 'goto_step':
                current_step = random.choice(list(set(range(num_steps)).difference({current_step})))
                current_node = f'goto_step_{current_step+1}'
            elif current_node == 'started_task':
                started_task = True
                current_step += 1
            elif current_node == 'option_selected':
                selected_task = True
            elif current_node in search_intents:
                started_task = False
                issued_query = True
            elif current_node == 'system_response' and started_task:
                current_node = 'in_task_system_response'
            elif not system_turn and selected_task and not started_task and random.random() > 0.3:
                current_node = random.choice(['begin_task', 'acknowledge_task'])
            elif not system_turn and not selected_task and random.random() > 0.3 and \
                    current_node not in ['select_i', 'more_results']:
                current_node = random.choice(['search_recipe', 'suggest_recipe'])

            walk.append(current_node)

        if walk[-1] != 'end':
            #walk.append('stop')
            walk.append('end')

        walk_final = []
        for w in walk:
            if w == 'show_ingredients_begin':
                w = 'show_ingredients'
            elif w == 'system_response_begin':
                w = 'system_response'
            walk_final.append(w)

        return walk_final


if __name__ == '__main__':
    cg = TaskPathGenerator()

    num_paths = 10

    paths = [cg.generate_path(max_length=30, num_steps=4) for _ in
             range(num_paths)]

    for p in paths[:20]:
        print(' -> '.join(p))

    plot_states_frequency(paths)
