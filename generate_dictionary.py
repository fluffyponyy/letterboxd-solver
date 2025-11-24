from wordfreq import zipf_frequency
from wordfreq import top_n_list

words = top_n_list("en", 200000)
word_list = [w for w in words if zipf_frequency(w, "en") >= 1.8]

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

