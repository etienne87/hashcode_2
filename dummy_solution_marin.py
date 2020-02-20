import argparse
import numpy as np
import os
from read import read_file

parser = argparse.ArgumentParser(description='book')

parser.add_argument('--input_file_indice', type=int)

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
print("list_time_registration_lib = ", list_time_registration_lib)
print("tab_score_book = ", tab_score_book)
print("tab_book_library = ", tab_book_library)

tab_indice_libraries_sorted_by_time_registration = np.argsort(list_time_registration_lib)

result_file = hard_code_path_to_input+"/result/result_"+tab_input[args.input_file_indice]

with open(result_file, 'w') as file:
    file.write(str(N_lib) + "\n")
    for indice_lib in tab_indice_libraries_sorted_by_time_registration:
        file.write(str(indice_lib) + " " + str(len(tab_book_library[indice_lib])) + "\n")
        tab_book_current_library = tab_book_library[indice_lib]
        tab_book_indice_current_library_sorted_by_score = np.argsort(-tab_score_book[tab_book_current_library])
        tab_book_current_library_sorted_by_score = tab_book_current_library[tab_book_indice_current_library_sorted_by_score]
        for book_indice in tab_book_current_library_sorted_by_score:
            file.write(str(book_indice) + " ")
        file.write("\n")

