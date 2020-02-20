import os, glob
from input import read_file
#from compute_score import compute_score


#def optimize(data):
#    return ans, total

"""
def run_all(dir):
    filenames = glob.glob(dir + "/*.in")
    print(filenames)
    for filename in filenames:
        max_slices, slices = read_file(filename)
        total_pizza_types = len(slices)
        ans, total = optimize_max_slices(slices, max_slices)
        print("problem: ", os.path.basename(filename), ": ", total, max_slices, max_slices - total)
        score = compute_score(max_slices, total_pizza_types, slices, len(ans), ans)
        total += score
    return total
"""

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


def compute_score(library, unscanned_books, remaining_days):
    if library.sign_up_time > remaining_days:
        return 0
    books_shippable = unscanned_books.difference(unscanned_books)
    num_shippable = remaining_days * library.shippable_per_day

    #sort books
    books_shippable = list(books_shippable)
    books_sorted = sorted(books_shippable, key=lambda book:book.score)[:num_shippable]

    total_score = [item.score for item in books_sorted]
    return total_score







if __name__ == '__main__':
    # max_slices, slices = read_file('input/d_also_big.in')
    # total_pizza_types = len(slices)
    # ans, total = optimize_max_slices(slices, max_slices)
    # print(total, max_slices, max_slices-total)
    # score = compute_score(max_slices, total_pizza_types, slices, len(ans), ans)
    # print(score)

    #score = run_all('input')

    print('total score: ', score)