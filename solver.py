import random
from generate_dictionary import get_words
sides = [["e","p","r"],["t","l","i"],["n","x","c"],["a","m","v"]]
flat_sides = [ x for xs in sides for x in xs ]
num_letters = len(flat_sides)

solutions = []
shortest_solution_len = 100
word_list = []

get_words(flat_sides)

#Generate dictionary from available letters
with open("words.txt", "r") as file:
    text = file.read()
    word_list = text.splitlines()

#Returns true if no consecutive letters are on the same 'side' of the box
def check_possibility(word, sides):
    for i in range(len(word)-1):
        for side in sides:
            if word[i] in side and word[i+1] in side:
                return False
    return True

#Returns a list of unique letters found in a word
def get_used(word):
    used = []
    for letter in word:
        if letter not in used:
            used.append(letter)
    return used

#Finds the first word in the solution using a given starting letters
#It maximizes the amount of unique letters in the word
#If a 'first word coverage' is defined (>0), that maximum is constrained to the value of 'first word coverage'
#Returns available_words (why are we using this again TODO? improve this?), best_words (keeps track of all best first words regardless of start letters),
#and max_used, the int that represents the number of unique letters all words in best_words have TODO:is this valuable for cross-first-letter tracking? i think yes?

def find_best_first_word(starting_letter, first_word_coverage, max_used, best_words, available_words):
    
    #Gathers all possible words
    first_letter = starting_letter
    for word in word_list:
        if word[0] is not first_letter: continue
        is_possible = check_possibility(word, sides)
        if is_possible:
            available_words.append(word)
    
    #Finds only those with greatest letter coverage or those equal to first_word_coverage
    #TODO: refactor logic slightly
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
    

#Returns a list of words that are valid after a certain prev_word
#All words maximize number of unused letters based on what's in the letter array cur_used
def find_next_word(prev_word, cur_used):
    best_words = []
    available_words = []

    max_leftover_letters_used = 0
    
    #TODO: make this its own seperate function
    first_letter = prev_word[-1]
    for word in word_list:
        if word[0] is not first_letter: continue
        is_possible = check_possibility(word, sides)
        if is_possible:
            available_words.append(word)
    
    #Counts the number of letters this word uses that the prev_word does not (new_letters_used_count)
    #TODO: refactor logic slightly again
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

#Recursive function to find a full solution chain
#Stops if finds a full solution or if hits number of max allowed iterations (defined in 'chains'; also represents length of solution in # of words)
def chain_words(chains, num_words, word, all_used_letters, full_solution):
    #TODO: make these not global pls
    global shortest_solution_len
    global solutions

    if len(all_used_letters) == num_letters:
        #print("Hurray! This is a complete solution.")
        if len(full_solution) < shortest_solution_len:
            solutions = []
            solutions.append(full_solution)
            shortest_solution_len = len(full_solution)
        elif len(full_solution) == shortest_solution_len:
            solutions.append(full_solution)
        return True
    elif chains == num_words:
        #Hit max number of allowed iterations, stopping
        return False
    else:
        used_letters = get_used(word) #TODO: can not run again?
        next_solutions = find_next_word(word, used_letters)
        #print(f"For word {word}, the next solutions are {next_solutions}")
        for next in next_solutions:
            total = get_used("".join(full_solution + [next]))
            #print(f"    solution {full_solution + [next]} uses {len(total)} / {num_letters}")
            all_used_letters = total
            chain_words(chains, num_words+1, next, all_used_letters, full_solution + [next])

#TODO maybe a poorly named function
#Given a first_word_coverage, finds maximum 
def get_solution(first_word_coverage, num_words_in_solution):
    max_used = first_word_coverage
    best_words = []
    available_words = []
    
    for letter in flat_sides:
        available_words, best_words, max_used = find_best_first_word(letter, first_word_coverage, max_used, best_words, available_words)

    best_words = list(dict.fromkeys(best_words))

    #This would print all the best second words that maximize the number of unique letters that are unused by the first word
    #print(f"{best_words} all use a maximum of {max_used} / {num_letters}.")

    for word in best_words:
       full_solution = []
       full_solution.append(word)
       all_used_letters = get_used(word)
       chain_words(num_words_in_solution, 1, word, all_used_letters, full_solution)

    #If we got this far, we need to try a different maximum number of unique letters used for the first word
    return False, max_used

#Finds max coverage of first word possible
#
success, max_coverage_available_first_word = get_solution(0, 3)

i = max_coverage_available_first_word - 1

while i >= 2:
    success, extra = get_solution(i, 3)
    if not success:
        i = i - 1
    else: 
        break

solutions = sorted(solutions, key=len)
print(f"All complete solutions with up to {3} words are: {solutions}")
