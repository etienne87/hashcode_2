import numpy as np
import os
import time
from read import read_file



def score_lib(lib, days_left):
    return min(lib["ship_per_day"]*(days_left-lib["sign_up_t"]), lib["num_books_in_lib"])


def choose_library(libraries, days_left):
    id_max = 0
    score_max = 0
    for i, lib in enumerate(libraries):
        score = score_lib(lib, days_left)
        if score > score_max:
            id_max = i
            score_max = score

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
    output_text = "{}\n".format(lib["id"])
    count_before_end = 0
    for (book, score) in sorted_list[::-1]:
        if count_before_end >nb_max_books:
            break
        output_text += "{} ".format(book)
    output_text = output_text[:-1] + "\n"
    return output_text


def main():
    B = 100

    scanned_books = np.zeros(B)


    num_days, book_scores, libs = read_file('input/a_example.txt')


    days_left = num_days

    for id_lib, lib in enumerate(libs):
        lib["set_books"] = set(lib["book_ids"])
        lib["id"] = id_lib
        lib["set_books_with_score"] = set()
        for book in lib["book_ids"]:
            lib["set_books_with_score"].add((book, book_scores[book]))


    id_best_lib = choose_library(libs)
    
    output_test = choose_books_for_lib(libs)




    print("test")


    print("before", libs)

    libs = update_libs(libs, [1,2,3,4,5], book_scores)


    print("after", libs)








if __name__=="__main__":
    main()




