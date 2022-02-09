#test
import os, sys, glob, math, tqdm, time, copy, collections, heapq, argparse, random
from read import read_file


DYNAMIC_OCC=1

def select_intersection(books, unscanned_books, num_shippable, early_stop=1):
    books_shippable = [-1]
    for i in range(len(books)):
        book = books[i]
        if unscanned_books[book.id]:
            books_shippable.append(i)

        if len(books_shippable) >= num_shippable and early_stop:
            break
    return books_shippable[1:]

class Book(object):
    def __init__(self, id, score, occ):
        self.id = id
        self.score = score
        self.occ = occ

    def weighted_score(self):
        return self.score/math.log(1+self.occ)
      
      

class Library:
    def __init__(self, N, T, M, books):
        self.num_books = N
        self.sign_up_time = T
        self.shippable_per_day = M
        self.books = sorted(books, key=lambda book:book.score, reverse=True)

        #self.book_id_to_num = {item.id:i for i,item in enumerate(self.books)}


    def shippable(self, remaining_days):
        return min(self.num_books, (remaining_days-self.sign_up_time)*self.shippable_per_day)

    def really_shippable(self, remaining_days, unscanned_books):
        max_num_shippable = self.shippable(remaining_days)
        books_shippable = select_intersection(self.books, unscanned_books, max_num_shippable)
        return len(books_shippable)

    def score_shippable(self, remaining_days, unscanned_books=None):
        num_shippable = self.shippable(remaining_days)

        if unscanned_books is None:
            score = sum([item.score for item in self.books[:num_shippable]])
        else:
            books_shippable = select_intersection(self.books, unscanned_books, num_shippable)
            score = sum([self.books[item].score for item in books_shippable])

        return score
        
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


def make_book_to_lib(libraries):
    book_to_lib = collections.defaultdict(set)
    for lib_id, lib in enumerate(libraries):
        for book in lib.books:
            book_to_lib[book.id].add(lib_id)
    return book_to_lib

def my_read(file):
    num_days, book_scores, libs = read_file(file)
    book_occ = book_occurences(libs, len(book_scores))
    mean_book_occ = sum(book_occ)
    book_occ = [item/mean_book_occ for item in book_occ]
    books = [Book(i, score, book_occ[i]) for i, score in enumerate(book_scores)]

    # check = [1 for _ in range(len(books))]
    libraries = []
    for lib in libs:
        num_books_in_lib = lib['num_books_in_lib']
        sign_up_t = lib['sign_up_t']
        ship_per_day = lib['ship_per_day']
        book_ids = lib['book_ids']
        lib_books = [books[id] for id in book_ids]
        # for book_id in book_ids:
        #     check[book_id] = 0
        libraries.append(Library(num_books_in_lib, sign_up_t, ship_per_day, lib_books))

    # some books are found in no library
    # checksum = sum(check) 
    # assert checksum == 0

    return libraries, books, num_days





def compute_score(library, unscanned_books, remaining_days, total_days, occ=None):
    remaining_days_after = remaining_days - library.sign_up_time
    if remaining_days_after < 0:
        return 0, 0, []

    num_shippable = remaining_days_after * library.shippable_per_day

    # if DYNAMIC_OCC:
    #     for i in range(len(library.books)):
    #         library.books[i].occ = occ[library.books[i].id]
        #library.sort_by_occ()


    books_shippable = select_intersection(library.books, unscanned_books, num_shippable)
    

    total_score = sum([library.books[item].score for item in books_shippable])
    out_books_ids = [library.books[item].id for item in books_shippable]

    ratio = max(0.7, remaining_days/total_days * 1.4)

    if DYNAMIC_OCC:
        weighted_score = 0
        for idx in books_shippable:
            weighted_score += library.books[idx].score / math.log(1+occ[library.books[idx].id])
            
        # weighted_score = sum([library.books[item].weighted_score() for item in books_shippable])
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

    def update(self, libraries, book2lib, best_lib_id, lib_book_ids, lib_score):
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

            # for libid in book2lib[book_id]:
            #     lib = libraries[libid]
            #     book_num = lib.book_id_to_num[book_id]
            #     lib.books[book_num].occ = self.book_occ[book_id]

            

        self.total_score += lib_score
        self.hashkey = int("".join([str(item) for item in self.remaining_libs]))

    def __hash__(self):
        return self.hashkey


def get_mu_std(array):
    mean = sum(array)/len(array)
    std = math.sqrt(sum([(item-mean)**2 for item in array])/len(array))
    return mean, std

def optimize_beam(libraries, all_books, days, k=2, d=3, n=2, pruning=False, verbose=0):
    book_occ = book_occurences_v2(libraries, len(all_books))

    book2lib = make_book_to_lib(libraries)
    num_remaining_libs = len(libraries)
    beam = [Solution(len(all_books), len(libraries), days, book_occ)]

    # print some stats
    sign_up_times = [lib.sign_up_time for lib in libraries]
    shipping_speeds = [lib.shippable_per_day for lib in libraries]


    sign_up_mean, sign_up_std = get_mu_std(sign_up_times)
    shipping_speed_mean, shipping_speed_std = get_mu_std(shipping_speeds)
    print('sign up time: avg: ', sign_up_mean)
    print('sign up time: var: ', sign_up_std)
    print('shipping speed: avg: ', shipping_speed_mean)
    print('shipping speed: var: ', shipping_speed_std)

 
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
                    nusol.update(libraries, book2lib, best_lib_id, lib_book_ids, lib_score)
                    if pruning:
                        hash_key = nusol.__hash__()
                        if hash_key in beam_hash:
                            other = beam_hash[hash_key]
                            beam_hash[hash_key] = nusol if nusol.total_score > other.total_score else other
                        else:
                            beam_hash[hash_key] = nusol 
                    else:
                        all_solutions.append(nusol)
        
        if pruning:
            all_solutions = beam_hash.values()

        if len(all_solutions) and iter%d==0:
            all_solutions = heapq.nlargest(n, all_solutions, key=lambda item:item.total_score/item.days) 

            # num = len(all_solutions)
            # step = max(1, num//n)
            # all_solutions = all_solutions[:num:step]

    
            print('current best: ', all_solutions[0].total_score*1e-6, ' @', beam[0].days, '/', days, ' num sol: ', len(all_solutions))
     
        iter += 1
        
        beam = all_solutions

    total_score, id_libs, n_books, books_per_lib = best_sol.total_score, best_sol.id_libs, best_sol.n_books, best_sol.books_per_lib

    
    return total_score, id_libs, n_books, books_per_lib


def optimize_d(libraries, all_books, days):
    #for D it is a pure knapsack! (as sign up & ship_per_day is all the same)

    sign_up_times = [lib.sign_up_time for lib in libraries]
    shipping_speeds = [lib.shippable_per_day for lib in libraries]
    num_books_per_lib = [len(lib.books) for lib in libraries]

    sign_up_mean, sign_up_std = get_mu_std(sign_up_times)
    shipping_speed_mean, shipping_speed_std = get_mu_std(shipping_speeds)
    num_books_mean, num_books_std = get_mu_std(num_books_per_lib)
    print('sign up time: avg: ', sign_up_mean)
    print('sign up time: var: ', sign_up_std)
    print('shipping speed: avg: ', shipping_speed_mean)
    print('shipping speed: var: ', shipping_speed_std)
    print('num books per lib: avg: ', num_books_mean)
    print('num books per lib: var: ', num_books_std)

    print('can we sign up every lib: ', sum(sign_up_times), '/', days)

    nbooks = len(all_books)
    book_to_lib = collections.defaultdict(set)

    book_to_best_lib = {}

    for lib_id, lib in enumerate(libraries):
        for book in lib.books:
            book_to_lib[book.id].add(lib_id)


    for book in all_books:
        libs = list(book_to_lib[book.id])
        
        if len(libs) == 0:
            book_to_best_lib[book.id] = 1e-5
            continue

        #max
        libs = sorted(libs, key=lambda item:libraries[item].score_shippable(days) )
        best_lib = libs[0]

        book_to_best_lib[book.id] = libraries[best_lib].score_shippable(days)


    books = sorted(all_books, key=lambda item:item.score/book_to_best_lib[item.id], reverse=True)
    #books = sorted(all_books, key=lambda item:item.score, reverse=True) 

    libs_taken = set()

    id_libs = []
    books_per_lib = collections.defaultdict(list) #lib id: books


    unscanned_books = [1 for _ in range(len(all_books))]
    lib_id_to_ship = {}
    total_score = 0
    remaining_days = days

    #quite fast, could consider knapsack
    for i, book in enumerate(books):

        book_libs = book_to_lib[book.id]
        
        inter =  list(book_libs.intersection(libs_taken))


        book_placed=False
        if len(inter): #lib has been reserved already
            lib_taken = None
            for lib in inter:
                remaining_books = lib_id_to_ship[lib] 
                if remaining_books > 0:
                    lib_taken = lib
            
            if lib_taken is not None:
                books_per_lib[lib_taken].append(book.id)
                total_score += book.score
                unscanned_books[book.id] = 0     
                lib_id_to_ship[lib_taken] -= 1
                book_placed=True
            else:
                book_placed=False

        if remaining_days > 0 and not book_placed:
            #choose best lib according to sign_up time

            #don't choose among already taken libs!
            libs = list(book_libs.difference(libs_taken))

           
            libs = sorted(libs, key=lambda item:libraries[item].score_shippable(remaining_days, unscanned_books), reverse=True)
            best_lib = None
            for item in libs:
                if libraries[item].sign_up_time > remaining_days:
                    continue
                else:
                    best_lib = item
                    break
            
            if best_lib is None:
                continue

            lib_id_to_ship[best_lib] = libraries[best_lib].really_shippable(remaining_days, unscanned_books) - 1
            libs_taken.add(best_lib)
            id_libs.append(best_lib)
            books_per_lib[best_lib].append(book.id)
            remaining_days -= libraries[best_lib].sign_up_time

            total_score += book.score
 
            unscanned_books[book.id] = 0

    print('num days: ', remaining_days)
    print('still to ship: ', sum(lib_id_to_ship.values()))

    possible_total_score = 0
    for i, book in enumerate(books):
        if unscanned_books[book.id] == 0:
            continue
        #print(book.score)
        book_libs = book_to_lib[book.id]
        inter =  list(book_libs.intersection(libs_taken))
        if len(inter):
            possible_total_score += book.score
    
    print('possible: ', possible_total_score)



    books_per_lib = [books_per_lib[item] for item in id_libs]
    n_books = [len(item) for item in books_per_lib]

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
        5039449,
        5056623,
        5345656
    ]

    tab_input = [tab_input[id] for id in tabs]
    current_scores = [myteam_leaderboard[id]*1e-6 for id in tabs]

    total_to_beat = sum(current_scores)

    #opt_fun = lambda x, y, z: optimize_by_books(x,y,z)
    opt_fun = lambda x,y,z: optimize_beam(x,y,z,k=k,n=n,d=d)

    if len(tabs) == 1 and tabs[0] == 3:
        opt_fun = lambda x,y,z: optimize_d(x,y,z)

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
