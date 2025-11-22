#Closed solution; has a word list, does not have to input letters one by one and check if valid word
#Open solution; no word list given, must enter letters one by one and verify validity

import random
from generate_dictionary import get_words
sides = [["e","p","r"],["t","l","i"],["n","x","c"],["a","m","v"]]
#sides = [["a","b"],["e","r"],["s","t"]]
flat_sides = [ x for xs in sides for x in xs ]

letters_used = []

#min size of a solution set is 1
solutions = []
word_list = []

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


def find_best_first_word(starting_letter, first_word_coverage, max_used, best_words, available_words):

    first_letter = starting_letter
    for word in word_list:
        if word[0] is not first_letter: continue
        is_possible = check_possibility(word, sides)
        if is_possible:
            available_words.append(word)
    

    for word in available_words:
        num_used = len(get_used(word))
        if first_word_coverage == 0:
            if num_used > max_used:
                best_words = []
                max_used = num_used
                best_words.append(word)
            elif num_used == max_used:
                best_words.append(word)
        else:
            if num_used == first_word_coverage:
                max_used = num_used
                best_words.append(word)

    return available_words, best_words, max_used
    

def find_next_word(prev_word, cur_used):
    best_words = []
    available_words = []

    max_leftover_letters_used = 0
    
    first_letter = prev_word[-1]
    for word in word_list:
        if word[0] is not first_letter: continue
        is_possible = check_possibility(word, sides)
        if is_possible:
            available_words.append(word)
        
    for word in available_words:
        letters_used = get_used(word)
        new_letters_used_count = 0
        for letter in letters_used:
            if letter not in cur_used:
                new_letters_used_count+=1
        if new_letters_used_count > max_leftover_letters_used:
            best_words = []
            max_leftover_letters_used = new_letters_used_count
            best_words.append(word)
        elif new_letters_used_count == max_leftover_letters_used:
            best_words.append(word)
    return best_words

def chain_words(chains, num_words, word, all_used_letters, full_solution):

    if len(all_used_letters) == num_letters:
        print("Hurray! This is a complete solution.")
        solutions.append(full_solution)
        return True
    elif chains == num_words:
        return False
    else:
        used_letters = get_used(word) #running again nbut doesnt really matter
        next_solutions = find_next_word(word, used_letters)
        #print(f"For word {word}, the next solutions are {next_solutions}")
        for next in next_solutions:
            total = get_used("".join(full_solution + [next]))
            #print(f"    solution {full_solution + [next]} uses {len(total)} / {num_letters}")
            all_used_letters = total
            chain_words(chains, num_words+1, next, all_used_letters, full_solution + [next])

def try_solution(first_word_coverage, num_words_in_solution):
    max_used = first_word_coverage
    best_words = []
    available_words = []
    
    for letter in flat_sides:
        available_words, best_words, max_used = find_best_first_word(letter, first_word_coverage, max_used, best_words, available_words)

    best_words = list(dict.fromkeys(best_words))
    print(f"{best_words} all use a maximum of {max_used} / {num_letters}.")

    for word in best_words:
       full_solution = []
       full_solution.append(word)
       all_used_letters = get_used(word)
       chain_words(num_words_in_solution, 1, word, all_used_letters, full_solution)

    print("Not a complete solution. Restarting...")
    return False, max_used

success, max_coverage_available_first_word = try_solution(0, 3)

i = max_coverage_available_first_word - 1

while i >= 2:
    success, extra = try_solution(i, 3)
    if not success:
        i = i - 1
    else: 
        break

solutions = sorted(solutions, key=len)
print(f"All complete solutions with up to {3} words are: {solutions}")
