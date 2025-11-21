import nltk #consider: different libary for better wordlist
from nltk.corpus import words

word_list = words.words()  # list of English words
def get_words(available_letters):
    filtered = []
    for w in word_list:
        valid = True
        if len(w) < 3: continue
        for letter in w:
            if letter not in available_letters: valid = False

        if valid:
            filtered.append(w)
    
    filename = "words.txt"

    with open(filename, "w") as file:
        file.write("\n".join(filtered))

    print(f"Saving to {filename} with {len(filtered)} possible words.")

