import argparse
import numpy as np
import os
from read import read_file

def compute_score_library(lib_dict, tab_score_book, remaining_days, heuristic_on_day):
    sign_up_time = lib_dict['sign_up_t']
    shippable_per_day = lib_dict['ship_per_day']

    if sign_up_time >= remaining_days:
        return 0, []
    num_book_possible = (remaining_days - sign_up_time) * shippable_per_day

    #sort books
    tab_book_current_library = np.array(lib_dict['book_ids'])
    tab_book_indice_current_library_sorted_by_score = np.argsort(-tab_score_book[tab_book_current_library])
    tab_book_current_library_sorted_by_score = tab_book_current_library[tab_book_indice_current_library_sorted_by_score]

    total_score = np.sum(tab_score_book[tab_book_current_library_sorted_by_score[0:num_book_possible]])/(sign_up_time + heuristic_on_day)#- heuristic_on_day*sign_up_time
    return total_score, tab_book_current_library_sorted_by_score[0:num_book_possible]

parser = argparse.ArgumentParser(description='book')

parser.add_argument('--input_file_indice', type=int)
parser.add_argument('--heuristic', type=float)

args = parser.parse_args()

tab_input = ["a_example.txt",
"b_read_on.txt",
"c_incunabula.txt",
"d_tough_choices.txt",
"e_so_many_books.txt",
"f_libraries_of_the_world.txt",
             ]

hard_code_path_to_input = "/home/toromanoff/workspace/hashcode_2/input"
input_file = os.path.join(hard_code_path_to_input, tab_input[args.input_file_indice])

num_days, book_scores, libs = read_file(input_file)

N_book = len(book_scores)
N_lib = len(libs)
N_days = num_days
list_time_registration_lib = [lib['sign_up_t'] for lib in libs]
tab_score_book = np.array(book_scores)
tab_book_library = [np.array(lib['book_ids']) for lib in libs]

print("N_book = ", N_book)
print("N_lib = ", N_lib)
print("N_days = ", N_days)
# print("list_time_registration_lib = ", list_time_registration_lib)
# print("tab_score_book = ", tab_score_book)
# print("tab_book_library = ", tab_book_library)

tab_indice_libraries_sorted_by_time_registration = np.argsort(list_time_registration_lib)



remaining_days = N_days

tab_list_id_lib_still_possible = [i for i in range(N_lib)]


new_heuristic_tab = [10e6, 1e5]
day = 145
factor_for_day = day/N_days * new_heuristic_tab[1] + (N_days-day) * new_heuristic_tab[0]
heuristic_on_day = args.heuristic

result_file = hard_code_path_to_input+"/result/result_heur_"+str(heuristic_on_day)+"_"+tab_input[args.input_file_indice]

with open(result_file, 'w') as file:
    file.write(str(N_lib) + "\n")
    while len(tab_list_id_lib_still_possible) > 0:
        print("len(tab_list_id_lib_still_possible) = ", len(tab_list_id_lib_still_possible))
        chosen_lib = tab_list_id_lib_still_possible[0]
        max_score, chosen_book = compute_score_library(libs[chosen_lib], tab_score_book=tab_score_book, remaining_days=remaining_days, heuristic_on_day=heuristic_on_day)
        for indice_lib in tab_list_id_lib_still_possible:
            lib_dict = libs[indice_lib]
            current_score_lib, current_chosen_book = compute_score_library(lib_dict, tab_score_book=tab_score_book, remaining_days=remaining_days, heuristic_on_day=heuristic_on_day)
            if current_score_lib > max_score:
                max_score = current_score_lib
                chosen_lib = indice_lib
                chosen_book = current_chosen_book

        if len(chosen_book) > 0:
            file.write(str(chosen_lib) + " " + str(len(chosen_book)) + "\n")
            for book_indice in chosen_book:
                file.write(str(book_indice) + " ")
            file.write("\n")
        else:
            file.write(str(chosen_lib) + " " + str(1) + "\n")
            file.write(str(libs[chosen_lib]['book_ids'][0]) + " ")
            file.write("\n")
            print("we are not finding any lib to make point")
            assert max_score == 0

        remaining_days = remaining_days - libs[chosen_lib]['sign_up_t']
        tab_score_book[chosen_book] = 0
        tab_list_id_lib_still_possible.remove(chosen_lib)





