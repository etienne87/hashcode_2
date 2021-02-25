def read_file(filename):
    with open(filename, 'r') as f:
        num_books, num_libs, num_days = f.readline().split(' ')
        book_scores = f.readline().split(' ')
        book_scores = [int(item) for item in book_scores]
        libs = []
        for i in range(int(num_libs)):
            num_books_in_lib, sign_up_t, ship_per_day = f.readline().split(' ')
            book_ids = f.readline().split(' ')
            book_ids = [int(item) for item in book_ids]
            libs.append({
                'num_books_in_lib': int(num_books_in_lib),
                'sign_up_t': int(sign_up_t),
                'ship_per_day': int(ship_per_day),
                'book_ids': book_ids
            })
        return int(num_days), book_scores, libs


if __name__ == '__main__':
    num_days, book_scores, libs = read_file('input/a_example.txt')
    print(num_days)
    print(book_scores)
    print(libs)