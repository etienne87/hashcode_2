import numpy as np
import os
import time
from read import read_file
import argparse


def score_lib(lib, days_left):
    #return 1-lib["sign_up_t"]
    if lib["num_books_in_lib"]<=0:
        return -99999999


    would_be_left = days_left - lib["sign_up_t"]
    nb_max_books = would_be_left * lib["ship_per_day"]
    if nb_max_books > lib["num_books_in_lib"]:
        score_lib = lib["score_in_lib"]
    else:
        sorted_list = sorted(lib["set_books_with_score"], key=lambda x: x[1])[::-1]
        score_lib = 0
        for i in range(nb_max_books):
            score_lib += sorted_list[i][1]


    return score_lib/lib["sign_up_t"]

#    return min(lib["ship_per_day"]*(days_left-lib["sign_up_t"]) * lib["score_in_lib"]/lib["num_books_in_lib"], lib["num_books_in_lib"]* lib["score_in_lib"]/lib["num_books_in_lib"])


def choose_library(libraries, days_left):
    id_max = None
    score_max = None
    for i, lib in enumerate(libraries):
        if not lib["taken"]:
            score = score_lib(lib, days_left)
            if score_max is None or score > score_max:
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
                lib["score_in_lib"] = lib["score_in_lib"] - books_score[book]

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
    if len(books_taken)==0:
        return "", []
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


        score_in_lib = 0

        for book in lib["book_ids"]:
            lib["set_books_with_score"].add((book, book_scores[book]))
            score_in_lib += book_scores[book]


        lib["score_in_lib"] = score_in_lib



    global_output = "{}\n".format(number_output_libs) + middle_output
    print("output_text", global_output)

    result_file = hard_code_path_to_input+"result/result_"+tab_input[id_input]

    with open(result_file, 'w') as file:
        file.write(global_output)





if __name__=="__main__":
    parser = argparse.ArgumentParser(description='book')

    parser.add_argument('--input_file_indice', type=int, default=1)

    args = parser.parse_args()

    id_input = args.input_file_indice
    main(id_input)




