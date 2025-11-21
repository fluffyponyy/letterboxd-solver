#Closed solution; has a word list, does not have to input letters one by one and check if valid word
#Open solution; no word list given, must enter letters one by one and verify validity

import random
from generate_dictionary import get_words

sides = [["d","f","w"],["y","e","u"],["o","c","i"],["a","v","s"]]
#sides = [["a","b"],["e","r"],["s","t"]]
flat_sides = [ x for xs in sides for x in xs ]
letters_used = []

#min size of a solution set is 1
solutions = {}
word_list = []

available_words = []

max_used = 0
best_words = []

get_words(flat_sides)
num_letters = len(flat_sides)

with open("words.txt", "r") as file:
    text = file.read()
    word_list = text.splitlines()

min_len = 3

def check_possibility(word, sides):
    for i in range(len(word)-1):
        for side in sides:
            if word[i] in side and word[i+1] in side: #if on same side
                return False
    return True

def get_used(word):
    used = []
    for letter in word:
        if letter not in used:
            used.append(letter)
    return used


def find_best_first_word(starting_letter, first_word_coverage):
    global max_used
    global best_words

    first_letter = starting_letter
    for word in word_list:
        if word[0] is not first_letter: continue
        is_possible = check_possibility(word, sides)
        if is_possible:
            available_words.append(word)
    

    for word in available_words:
        num_used = len(get_used(word))
        if num_used == first_word_coverage: ##changed from num_used > max_used
            #best_words = []
            max_used = num_used
            best_words.append(word)
        # elif num_used == max_used:
        #     best_words.append(word)

def find_next_word(prev_word, cur_used):
    best_words = []
    available_words = []
    num_cur_used = len(cur_used)
    
    first_letter = prev_word[-1]
    for word in word_list:
        if word[0] is not first_letter: continue
        is_possible = check_possibility(word, sides)
        if is_possible:
            available_words.append(word)
        
    for word in available_words:
        num_used = len(get_used(word+prev_word))
        if num_used > num_cur_used:
            best_words = []
            num_cur_used = num_used
            best_words.append(word)
        elif num_used == num_cur_used:
            best_words.append(word)
    return best_words

def try_solution(first_word_coverage, num_words_in_solution):
    for letter in flat_sides:
        find_best_first_word(letter, first_word_coverage)


    print(f"{best_words} all use a maximum of {max_used} / {num_letters}.")

    for word in best_words:
        for i in range(num_words_in_solution-1):    
            used = max_used
            used_letters = get_used(word) #running again nbut doesnt really matter
            next_solutions = find_next_word(word, used_letters)
            print(f"For word {word}, the next solutions are {next_solutions}")
            for next in next_solutions:
                total = get_used(word+next)
                print(f"    solution {word}, {next} uses {len(total)} / {num_letters}")
                if total == num_letters:
                    print("Hurray! This is a complete solution.")
                    return True
                else:
                    #TODO: need to make sure can do a third word
    print("Not a complete solution. Restarting...")
    return False


max_available = 8
i = max_available

while i >= 3:
    success = try_solution(i, 2)
    if not success:
        i - 1
    else:
        exit()

print("No success with 2 words. Attempting 3...")

while i >= 3:
    success = try_solution(i, 3)
    if not success:
        i - 1
    else:
        exit()