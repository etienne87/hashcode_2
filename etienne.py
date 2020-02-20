import os, glob
from read import read_file



class Book:
    def __init__(self, id, score):
        self.id = id
        self.score = score

class Library:
    def __init__(self, N, T, M, books):
        self.num_books = N
        self.sign_up_time = T
        self.shippable_per_day = M
        self.books = sorted(books, key=lambda book:book.score, reverse=True)


def my_read(file):
    num_days, book_scores, libs = read_file(file)

    books = [Book(i, score) for i, score in enumerate(book_scores)]
    libraries = []
    for lib in libs:
        num_books_in_lib = lib['num_books_in_lib']
        sign_up_t = lib['sign_up_t']
        ship_per_day = lib['ship_per_day']
        book_ids = lib['book_ids']
        lib_books = [books[id] for id in book_ids]
        libraries.append(Library(num_books_in_lib, sign_up_t, ship_per_day, lib_books))

    return libraries, books, num_days


def compute_score(library, unscanned_books, remaining_days):
    remaining_days = remaining_days - library.sign_up_time
    if remaining_days <= 0:
        return 0, []

    #books_shippable = library.books.intersection(unscanned_books)
    num_shippable = remaining_days * library.shippable_per_day

    #select books that are not unscanned_books

    books_shippable = []
    for book in library.books:
        if unscanned_books[book.id]:
            books_shippable.append(book)

        if len(books_shippable) >= num_shippable:
            break

    total_score = sum([item.score for item in books_shippable])

    out_books_ids = [book.id for book in books_shippable]
    return total_score, out_books_ids



def print_scores(scores):
    print([item[1][0] for item in scores])

def optimize(libraries, all_books, days, verbose=True):
    id_libs = []
    n_books = []
    books_per_lib = []

    remaining_libs = [1 for _ in range(len(libraries))]
    unscanned_books = [1 for _ in range(len(all_books))]


    total_score = 0

    d = 0
    num_remaining_libs = len(libraries)
    while d < days and num_remaining_libs > 0:
        if verbose:
            print(d, '/', days, ' total score: ', total_score*1e-6)

        remaining_days = days-d

        scores = [(id,compute_score(lib, unscanned_books, remaining_days)) for id, lib in enumerate(libraries) if remaining_libs[id]]

        sorted_scores = sorted(scores, key=lambda lib:lib[1][0], reverse=True)

        best_lib_id = sorted_scores[0][0]
        best_lib_score, lib_book_ids = sorted_scores[0][1]

        if best_lib_score == 0:
            break

        total_score += best_lib_score

        id_libs.append(best_lib_id)
        n_books.append(len(lib_book_ids))
        books_per_lib.append(lib_book_ids)

        #remove days
        d += libraries[best_lib_id].sign_up_time
        #remove lib
        remaining_libs[best_lib_id] = 0
        num_remaining_libs -= 1
        #remove book
        for book_id in lib_book_ids:
            unscanned_books[book_id] = 0

    return total_score, id_libs, n_books, books_per_lib


def write_solution(result_file, id_libs, n_books, books_per_lib):
    with open(result_file, 'w') as file:
        file.write(str(len(id_libs)) + "\n")
        for i, indice_lib in enumerate(id_libs):
            nbooks = n_books[i]
            file.write(str(indice_lib) + " " + str(nbooks) + "\n")

            for book_indice in books_per_lib[i]:
                file.write(str(book_indice) + " ")
            file.write("\n")


def run():
    tab_input = ["a_example.txt",
                 "b_read_on.txt",
                 "c_incunabula.txt",
                 #"d_tough_choices.txt",
                 "e_so_many_books.txt",
                 "f_libraries_of_the_world.txt",
                 ]


    total_score = 0
    for file in tab_input:
        print(file)
        libraries, books, num_days = my_read("input/"+file)
        file_score, id_libs, n_books, books_per_lib = optimize(libraries, books, num_days)
        total_score += file_score

        print(file, ': file score: ', file_score*1e-6, ' total score: ', total_score*1e-6)

        result_file = "result/result_"+file
        write_solution(result_file, id_libs, n_books, books_per_lib)


    return total_score

if __name__ == '__main__':

    #run()

    #debug
    libraries, books, num_days = my_read('input/d_tough_choices.txt')
    optimize(libraries, books, num_days)
