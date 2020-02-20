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
        self.book_ids = set(books)

def my_read(file):
    num_days, book_scores, libs = read_file(file)

    books = [Book(i, score) for i, score in enumerate(book_scores)]
    libraries = []
    for lib in libs:
        num_books_in_lib = lib['num_books_in_lib']
        sign_up_t = lib['sign_up_t']
        ship_per_day = lib['ship_per_day']
        book_ids = lib['book_ids']
        lib_books = books[book_ids]
        #convert to books
        libraries.append(Library(num_books_in_lib, sign_up_t, ship_per_day, lib_books))

    return libraries, books, num_days


def compute_score(library, unscanned_books, remaining_days):
    if library.sign_up_time > remaining_days:
        return 0
    books_shippable = unscanned_books.difference(unscanned_books)
    num_shippable = remaining_days * library.shippable_per_day

    #sort books
    books_shippable = list(books_shippable)
    best_books = sorted(books_shippable, key=lambda book:book.score)[:num_shippable]

    total_score = [item.score for item in best_books]
    return total_score, best_books


def optimize(libraries, all_books, days):
    d = 0
    while d < days:
        pass





if __name__ == '__main__':

    libraries, books = my_read('input/a_example.txt')