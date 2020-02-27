import os, sys, glob, math, tqdm, time, copy, collections, heapq, argparse
from read import read_file

DYNAMIC_OCC=0

class Book:
    def __init__(self, id, score, occ):
        self.id = id
        self.score = score
        self.occ = occ

    def weighted_score(self):
        return self.score*math.sqrt(self.occ)
      
      

class Library:
    def __init__(self, N, T, M, books):
        self.num_books = N
        self.sign_up_time = T
        self.shippable_per_day = M
        self.books = sorted(books, key=lambda book:book.score, reverse=True)
    
    def sort_by_occ(self):
        self.books = sorted(self.books, key=lambda book:book.weighted_score(), reverse=True)


def book_occurences(libraries, N):
    M = len(libraries)
    book_occ = [0 for i in range(N)]
    for row, lib in enumerate(libraries):
        book_ids = lib['book_ids']
        for id in book_ids:
            book_occ[id] += 1
    return book_occ

def book_occurences_v2(libraries, N):
    M = len(libraries)
    book_occ = [0 for i in range(N)]
    for row, lib in enumerate(libraries):
        for book in lib.books:
            book_occ[book.id] += 1
    return book_occ



def my_read(file):
    num_days, book_scores, libs = read_file(file)
    book_occ = book_occurences(libs, len(book_scores))
    mean_book_occ = sum(book_occ)
    book_occ = [item/mean_book_occ for item in book_occ]
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


def compute_score(library, unscanned_books, remaining_days, total_days, occ=None):
    remaining_days_after = remaining_days - library.sign_up_time
    if remaining_days_after < 0:
        return 0, 0, []

    num_shippable = remaining_days_after * library.shippable_per_day

    if DYNAMIC_OCC:
        for i in range(len(library.books)):
            library.books[i].occ = occ[library.books[i].id]
        #library.sort_by_occ()


    books_shippable = select_intersection(library.books, unscanned_books, num_shippable)
    
    total_score = sum([item.score for item in books_shippable])
    
    out_books_ids = [book.id for book in books_shippable]

    ratio = max(0.7, remaining_days/total_days * 1.45)

    if DYNAMIC_OCC:
        weighted_score = sum([item.weighted_score() for item in books_shippable])
        weighted_score = weighted_score / math.pow(library.sign_up_time, ratio) 
    else:
        weighted_score = total_score / math.pow(library.sign_up_time, ratio) 

   
    return weighted_score, total_score, out_books_ids





class Solution:
    def __init__(self, nbooks, nlibs, total_days, book_occ):
        self.id_libs = []
        self.books_per_lib = []
        self.n_books = []
        self.total_score = 0
        self.days = 0
        self.total_days = total_days
        self.unscanned_books = [1 for _ in range(nbooks)]
        self.remaining_libs = [1 for _ in range(nlibs)]
        self.num_remaining_libs = nlibs
        self.book_occ = book_occ 
        self.hashkey = int("".join([str(item) for item in self.remaining_libs]))

    def get_scores(self, libraries):
        remaining_days = self.total_days - self.days
        scores = [[id, *compute_score(lib, self.unscanned_books, remaining_days, self.total_days, self.book_occ)] for id, lib in enumerate(libraries) if self.remaining_libs[id]]
        return scores

    def update(self, libraries, best_lib_id, lib_book_ids, lib_score):
        #add libs
        self.id_libs.append(best_lib_id)
        self.n_books.append(len(lib_book_ids))
        self.books_per_lib.append(lib_book_ids)
        #remove days
        assert (self.days + libraries[best_lib_id].sign_up_time) <= self.total_days
        self.days += libraries[best_lib_id].sign_up_time
        #remove lib
        self.remaining_libs[best_lib_id] = 0
        self.num_remaining_libs -= 1
        #remove book from unscanned_books array
        for book_id in lib_book_ids:
            self.unscanned_books[book_id] = 0
            self.book_occ[book_id] -= 1
        self.total_score += lib_score
        self.hashkey = int("".join([str(item) for item in self.remaining_libs]))

    def __hash__(self):
        return self.hashkey

    def reorder(self, libraries):
        libs = [libraries[id] for id in self.id_libs]
        libs = sorted(libs, key=lambda lib:lib.sign_up_time)
        #recompute score


def select_topk(libs, k):
    return heapq.nlargest(libs, k)


def optimize_beam(libraries, all_books, days, k=2, d=3, n=2, pruning=False, verbose=0):
    book_occ = book_occurences_v2(libraries, len(all_books))

    num_remaining_libs = len(libraries)
    beam = [Solution(len(all_books), len(libraries), days, book_occ)]

    # print some stats
    sign_up_times = [lib.sign_up_time for lib in libraries]
    sign_up_mean = sum(sign_up_times)/len(sign_up_times)
    sign_up_std = math.sqrt(sum([(item-sign_up_mean)**2 for item in sign_up_times])/len(sign_up_times))
    print('sign up time: avg: ', sign_up_mean)
    print('sign up time: var: ', sign_up_std)
    #best possible score?
    max_score = 0
    for book in all_books:
        max_score += book.score
    print('max score: ', max_score*1e-6)

 
    best_sol = None
    iter = 0
    

    #pbar = tqdm.tqdm(total=days)

    while len(beam):
        all_solutions = []

        beam_hash = {}
        for sol in beam:
            if sol.days == days:
                if best_sol is None or sol.total_score >= best_sol.total_score:
                    best_sol = sol
                    print(best_sol.total_score)
                continue

            scores = sol.get_scores(libraries)
            scores = heapq.nlargest(k, scores, key=lambda lib:lib[1])

            #if zero score add solution!
            all_zero = sum([item[1] for item in scores]) == 0
            if all_zero:
                if best_sol is None or sol.total_score > best_sol.total_score:
                    best_sol = sol
                    print(best_sol.total_score)
                continue    

            for score in scores:
                nusol = copy.deepcopy(sol)
                best_lib_id, heuristic_score, lib_score, lib_book_ids = score

                if heuristic_score > 0:
                    nusol.update(libraries, best_lib_id, lib_book_ids, lib_score)
                    if pruning:
                        hash_key = nusol.__hash__()
                        if hash_key in beam_hash:
                            other = beam_hash[hash_key]
                            beam_hash[hash_key] = nusol if nusol.total_score > other.total_score else other
                        else:
                            beam_hash[hash_key] = nusol 
                            all_solutions.append(nusol)
                    else:
                        all_solutions.append(nusol)
            

        if len(all_solutions) and iter%d==0:
            all_solutions = heapq.nlargest(n, all_solutions, key=lambda item:item.total_score/item.days)

            print('current best: ', all_solutions[0].total_score*1e-6, ' @', beam[0].days, '/', days)
     
        iter += 1
        
        beam = all_solutions

    total_score, id_libs, n_books, books_per_lib = best_sol.total_score, best_sol.id_libs, best_sol.n_books, best_sol.books_per_lib

    
    return total_score, id_libs, n_books, books_per_lib



#optimize greedy
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

    while d <= days and num_remaining_libs >= 0:
        if verbose:
            print(d, '/', days, ' total score: ', total_score*1e-6)

        remaining_days = days-d

        #id, heuristic, total_score, book_ids
        scores = [[id, *compute_score(lib, unscanned_books, remaining_days, days)] for id, lib in enumerate(libraries) if remaining_libs[id]]
        sorted_scores = sorted(scores, key=lambda lib:lib[1], reverse=True)
        best_lib_id = sorted_scores[0][0]
        best_lib_id, _, best_lib_score, lib_book_ids = sorted_scores[0]


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
         
        
        pbar.update(max(d/days, num_remaining_libs/len(libraries)))

    print('days: ', d,'/', days)
    print('libs: ', len(id_libs), '/', len(libraries))
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


def run(tabs=[0,1,2,3,4,5], k=1, n=1, d=1):
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
        5056623,
        5345656
    ]

    tab_input = [tab_input[id] for id in tabs]
    current_scores = [myteam_leaderboard[id]*1e-6 for id in tabs]

    total_to_beat = sum(current_scores)

    #opt_fun = lambda x, y, z: optimize(x,y,z)
    opt_fun = lambda x,y,z: optimize_beam(x,y,z,k=k,n=n,d=d)

    total_score = 0
    for i, file in enumerate(tab_input):
        print(file)
        libraries, books, num_days = my_read("input/"+file)
        file_score, id_libs, n_books, books_per_lib = opt_fun(libraries, books, num_days)
        total_score += file_score

        print(file, ': file score: ', file_score*1e-6, '/', current_scores[i], ' total score: ', total_score*1e-6, '/', total_to_beat)

        if file_score*1e-6 > current_scores[i]:
            print(file, ': beaten!')

        result_file = "result/result_"+file
        write_solution(result_file, id_libs, n_books, books_per_lib)


    return total_score



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='book')

    parser.add_argument('--tabs',
                      nargs='+',
                      type=int,
                      dest='list',
                      default=[0,1,2,3,4,5],
                      help='tab list',
                      required=True)
    
    parser.add_argument('--k',
                      type=int,
                      default=1,
                      help='beam growth')
    parser.add_argument('--d',
                      type=int,
                      default=1,
                      help='beam depth')
    parser.add_argument('--n',
                      type=int,
                      default=1,
                      help='beam size after selection')
    args = parser.parse_args()
    
    tabs = args.list

    print('run on: ', tabs)
    print('beam size: ', args.k, args.d, args.n)

    start = time.time()
    run(tabs, args.k, args.n, args.d)

    print('program took: ', time.time()-start)