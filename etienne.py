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
        return 0

    #books_shippable = library.books.intersection(unscanned_books)
    num_shippable = remaining_days * library.shippable_per_day

    #select books
    books_shippable = []
    for book in library.books:
        if unscanned_books[book.id]:
            books_shippable.append(book)

        if len(books_shippable) >= num_shippable:
            break

    total_score = sum([item.score for item in books_shippable])
    return total_score, books_shippable

def print_scores(scores):
    print([item[1][0] for item in scores])

def optimize(libraries, all_books, days):

    id_libs = []
    n_books = []
    books_per_lib = []

    signed_up_libs = []
    remaining_libs = [i for i in range(len(libraries))]
    unscanned_books = [1 for i in range(len(all_books))]

    total_score = 0

    d = 0
    while d < days:
        remaining_days = days-d

        scores = [(i,compute_score(lib, unscanned_books, remaining_days)) for i, lib in enumerate(libraries) if remaining_libs[i]]

        sorted_scores = sorted(scores, key=lambda lib:lib[1][0], reverse=True)

        best_lib_id, lib_score, lib_books = sorted_scores[0]

        total_score += lib_score

        signed_up_libs.append(best_lib_id)
        n_books.append(len(lib_books))
        books_per_lib.append(lib_books)

        #remove lib
        remaining_libs[best_lib_id] = 0
        #remove book
        for book in lib_books:
            unscanned_books[book.id] = 0

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


if __name__ == '__main__':

    libraries, books, num_days = my_read('input/a_example.txt')
    optimize(libraries, books, num_days)
