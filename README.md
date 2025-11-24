# letterboxed-solver

Personal algorithm for finding all most optimal solutions for a NYT Letterboxed puzzle.

## Problem Description

Given a list of letters split into 4 buckets, find the shortest chain of valid words that **use all given letters** where no two consecutive letters come from the same bucket.

### Definitions

**Open** solution: a solution that does not know if a word is a valid dictionary word until it submits it to the game.

**Closed** solution: a solution that has access to a full dictionary of valid words. My work implements a closed solution.

**Most optimal solution** is defined as a solution with the fewest amount of words possible.

**Chain**: a series of words where each subsequent word begins with the last letter of the previous word.

**Valid word**: a word within the game's dictionary. Since NYT Games has never released their Letterboxed dictionary, I use a custom one.

**Coverage**: the number of unique letters used by a word.

## Solution Implementation

We know Letterboxed puzzles have 1-2 word solutions, so my solution assumes a solution can be found within a chain of 3 (although this can be modified).
I allow it to go up to 3 in case my dictionary does not include an essential word in NYT's dictionary.

An example puzzle and dictionary are included; the letters are "yob - trd - als - ing", and the given NYT solution is "blog, grandiosity".

### Dictionary

I used the `wordfreq` library to pull the $200000$ most frequent English words, just as a base vocabulary, and then filter to all words with a ZipF frequency above $1.8$. This still does not include all words the NYT uses, such as "dewlap", and it might include inappropriate words that they blacklist. One could also try and scrape the website to gain access to the game's dictionary, but I wanted my solution to be unreliant on external information.

### Process

It begins by finding the subset of best possible starting words; that is, all words with the greatest coverage. Then it tries to chain it to every next best possible word; that is, all
words that cover the greatest amount of unused letters. It does this until either finding a solution, or hitting a pre-defined limit on chain length. It then progressively decreases the coverage of the first word until it hits 2 and repeats the above process each time.

## An Open Solution?

An open solution means submitting words to the black box of Letterboxed blind. One could start by generating all possible words under or equal to a certain arbitrary length, checking their validity against the black box, generating a dictionary from this and then applying the closed solution.

If we select an arbitrary word legnth of 14, this results in a total of

$12 \* 9^2 + 12 \* 9^3 + ... + 12 \* 9^13 = 12 \sum\_{k=2}^{13} 9^{k} = 34, 315, 188, 682, 320 $

34 trillion options. Maybe not, unless you pair it with an existing dictionary to guide your search.
