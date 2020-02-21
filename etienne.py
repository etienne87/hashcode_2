import os, glob, math, tqdm, time
from read import read_file


class Book:
    def __init__(self, id, score, occ=0):
        self.id = id
        self.score = score

        #bullshit score using number of occurences of same book
        self.weighted_score = score / (1+occ)

class Library:
    def __init__(self, N, T, M, books):
        self.num_books = N
        self.sign_up_time = T
        self.shippable_per_day = M
        self.books = sorted(books, key=lambda book:book.score, reverse=True)
      

def book_occurences(libraries, N):
    M = len(libraries)
    book_occ = [0 for i in range(N)]
    for row, lib in enumerate(libraries):
        book_ids = lib['book_ids']
        for id in book_ids:
            book_occ[id] += 1
    return book_occ


def my_read(file):
    num_days, book_scores, libs = read_file(file)
    book_occ = book_occurences(libs, len(book_scores))
    books = [Book(i, score, book_occ[i]) for i, score in enumerate(book_scores)]
    libraries = []
    for lib in libs:
        num_books_in_lib = lib['num_books_in_lib']
        sign_up_t = lib['sign_up_t']
        ship_per_day = lib['ship_per_day']
        book_ids = lib['book_ids']
        lib_books = [books[id] for id in book_ids]
        libraries.append(Library(num_books_in_lib, sign_up_t, ship_per_day, lib_books))

    return libraries, books, num_days

def select_intersection(books, unscanned_books, num_shippable, early_stop=1):
    books_shippable = []
    for i in range(len(books)):
        book = books[i]
        if unscanned_books[book.id]:
            books_shippable.append(book)

        if len(books_shippable) >= num_shippable and early_stop:
            break
    return books_shippable


def compute_score(library, unscanned_books, remaining_days, total_days):
    remaining_days = remaining_days - library.sign_up_time
    if remaining_days <= 0:
        return 0, 0, []

    num_shippable = remaining_days * library.shippable_per_day

    books_shippable = select_intersection(library.books, unscanned_books, num_shippable)
 
    total_score = sum([item.score for item in books_shippable])

    out_books_ids = [book.id for book in books_shippable]

    # for this to be true, you need to confirm that N libs with signup_time/N exist
    # so if 
    weighted_score = total_score / library.sign_up_time


    return weighted_score, total_score, out_books_ids


def optimize(libraries, all_books, days, verbose=0):
    id_libs = []
    n_books = []
    books_per_lib = []

    remaining_libs = [1 for _ in range(len(libraries))]
    unscanned_books = [1 for _ in range(len(all_books))]
   
    total_score = 0

  
    d = 0
    num_remaining_libs = len(libraries)
    pbar = tqdm.tqdm(total=days)

    while d < days and num_remaining_libs > 0:
        if verbose:
            print(d, '/', days, ' total score: ', total_score*1e-6)

        remaining_days = days-d

        start = time.time()
        scores = [(id,compute_score(lib, unscanned_books, remaining_days, days)) for id, lib in enumerate(libraries) if remaining_libs[id]]
        #print('compute scores: ', time.time()-start)

       
        start = time.time()
        sorted_scores = sorted(scores, key=lambda lib:lib[1][0], reverse=True)
        #print('sorting: ', time.time()-start)


        best_lib_id = sorted_scores[0][0]
        weighed_score, best_lib_score, lib_book_ids = sorted_scores[0][1]

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
        #remove book from unscanned_books array
        for book_id in lib_book_ids:
            unscanned_books[book_id] = 0

        pbar.update(1)

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


def run(tabs=[0,1,2,3,4,5]):
    tab_input = ["a_example.txt",
                 "b_read_on.txt",
                 "c_incunabula.txt",
                 "d_tough_choices.txt",
                 "e_so_many_books.txt",
                 "f_libraries_of_the_world.txt",
    ]

    myteam_leaderboard = [
        21, 
        5822900,
        5690378,
        5028530,
        5043567,
        5345656
    ]

    tab_input = [tab_input[id] for id in tabs]
    current_scores = [myteam_leaderboard[id]*1e-6 for id in tabs]

    total_to_beat = sum(current_scores)

    total_score = 0
    for i, file in enumerate(tab_input):
        print(file)
        libraries, books, num_days = my_read("input/"+file)
        file_score, id_libs, n_books, books_per_lib = optimize(libraries, books, num_days)
        total_score += file_score

        print(file, ': file score: ', file_score*1e-6, '/', current_scores[i], ' total score: ', total_score*1e-6, '/', total_to_beat)

        if file_score*1e-6 > current_scores[i]:
            print(file, ': beaten!')

        result_file = "result/result_"+file
        write_solution(result_file, id_libs, n_books, books_per_lib)


    return total_score

def run_d():
    file = 'd_tough_choices.txt'
    libraries, books, num_days = my_read("input/"+file)
    file_score, id_libs, n_books, books_per_lib = optimize(libraries, books, num_days, 1)
    result_file = "result/result_" + file
    write_solution(result_file, id_libs, n_books, books_per_lib)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='book')

    parser.add_argument('--tabs',
                      nargs='+',
                      type=int,
                      dest='list',
                      default=[0,1,2,3,4,5],
                      help='<Required> Set flag',
                      required=True)
    args = parser.parse_args()
    
    tabs = args.list

    print('run on: ', tabs)

    start = time.time()
    run(tabs)

    print('program took: ', time.time()-start)