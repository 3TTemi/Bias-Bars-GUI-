KEY_WOMEN = "W"
KEY_MEN = "M"

def convert_rating_to_index(rating):
 
    if rating < 2.5:
        return 0
    elif rating >= 2.5 and rating <= 3.5:
        return 1
    else:
        return 2

def add_data_for_word(word_data, word, gender, rating):
 

    if(word not in word_data):
        word_data[word] = {KEY_WOMEN: [0, 0, 0], KEY_MEN: [0, 0, 0]}
    if gender == KEY_MEN:
        if convert_rating_to_index(rating) == 0:
            word_data[word][KEY_MEN][0] += 1
        elif convert_rating_to_index(rating) == 1:
            word_data[word][KEY_MEN][1] += 1
        elif convert_rating_to_index(rating) == 2:
            word_data[word][KEY_MEN][2] += 1
    elif gender == KEY_WOMEN:
        if convert_rating_to_index(rating) == 0:
            word_data[word][KEY_WOMEN][0] += 1
        elif convert_rating_to_index(rating) == 1:
            word_data[word][KEY_WOMEN][1] += 1
        elif convert_rating_to_index(rating) == 2:
            word_data[word][KEY_WOMEN][2] += 1

def read_file(filename):
 
    word_data = {}

    with open(filename) as f:
        next(f)
        for line in f:
            review_list = line.split(',')
            word_list = review_list[2].split()
            for word in word_list:
                add_data_for_word(word_data, word, review_list[1], float(review_list[0]))

    return word_data

def search_words(word_data, target):
 
    match_words = []
    target = target.lower()

    keys = word_data.keys()
    for key in keys:
        if target in key.lower():
            match_words.append(key)

    return match_words

def print_words(word_data):

    for key, value in sorted(word_data.items()):
        print(key, end=" ")
        for gender, counts in sorted(value.items()):
            print(gender, counts, end=" ")
        print("")

def main():
    import sys
    args = sys.argv[1:]

    if len(args) == 0: return

    filename = args[0]


    target = ''
    if len(args) >= 2 and args[0] == '-search':
        target = args[1]
        filename = args[2]  

    word_data = read_file(filename)

    if len(target) > 0:
        search_results = search_words(word_data, target)
        for word in search_results:
            print(word)
    else:
        print_words(word_data)


if __name__ == '__main__':
    main()