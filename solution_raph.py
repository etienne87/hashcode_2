import numpy as np
import os
import time
from read import read_file
import argparse


def score_lib(lib, days_left):
    return min(lib["ship_per_day"]*(days_left-lib["sign_up_t"]), lib["num_books_in_lib"])


def choose_library(libraries, days_left):
    id_max = None
    score_max = 0
    for i, lib in enumerate(libraries):
        if not lib["taken"]:
            score = score_lib(lib, days_left)
            if score > score_max:
                id_max = i
                score_max = score
    if id_max is not None:
        libraries[id_max]["taken"] = 1
    return id_max



def update_libs(libraries, books_taken, books_score):
    for lib in libraries:
        for book in books_taken:
            if book in lib["set_books"]:
                lib["num_books_in_lib"] -= 1
                lib["set_books"].remove(book)
                lib["set_books_with_score"].remove((book, books_score[book]))
    return libraries


def choose_books_for_lib(lib, days_left):
    sorted_list = sorted(lib["set_books_with_score"], key=lambda x: x[1])

    nb_max_books = days_left * lib["ship_per_day"]
    output_text = "{} ".format(lib["id"])
    middle_text = ""
    count_before_end = 0
    books_taken = []
    for (book, score) in sorted_list[::-1]:
        if count_before_end >nb_max_books:
            break
        middle_text += "{} ".format(book)
        books_taken += [book]
    output_text += str(len(books_taken)) + "\n"
    output_text += middle_text[:-1] + "\n"
    return output_text, books_taken


def main(id_input):
    B = 100

    scanned_books = np.zeros(B)

    hard_code_path_to_input = "/home/raphael/PycharmProjects/hashcode_2/input/"
    tab_input = ["a_example.txt",
                 "b_read_on.txt",
                 "c_incunabula.txt",
                 "d_tough_choices.txt",
                 "e_so_many_books.txt",
                 "f_libraries_of_the_world.txt",
                 ]

    num_days, book_scores, libs = read_file(hard_code_path_to_input + tab_input[id_input])


    days_left = num_days


    for id_lib, lib in enumerate(libs):
        lib["set_books"] = set(lib["book_ids"])
        lib["id"] = id_lib
        lib["set_books_with_score"] = set()
        lib["taken"]=0
        for book in lib["book_ids"]:
            lib["set_books_with_score"].add((book, book_scores[book]))


    STOP = False

    number_output_libs = 0

    global_output = ""
    middle_output = ""
    while not STOP and days_left > 0:
        print(days_left)
        id_best_lib = choose_library(libs, days_left=days_left)
        if id_best_lib is None:
            print("no more libs available")
            break

        lib_chosen = libs[id_best_lib]
        days_left -= lib_chosen["sign_up_t"]
        output_text, books_taken = choose_books_for_lib(lib_chosen, days_left)

        number_output_libs += 1

        #print("before", libs)

        libs = update_libs(libs, books_taken, book_scores)

        middle_output += output_text


    #print("after", libs)


    global_output = "{}\n".format(number_output_libs) + middle_output
    print("output_text", global_output)

    result_file = hard_code_path_to_input+"result/result_"+tab_input[id_input]

    with open(result_file, 'w') as file:
        file.write(global_output)





if __name__=="__main__":
    parser = argparse.ArgumentParser(description='book')

    parser.add_argument('--input_file_indice', type=int, default=3)

    args = parser.parse_args()

    id_input = args.input_file_indice
    main(id_input)




