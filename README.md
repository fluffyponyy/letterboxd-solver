# letterboxed-solver (WIP)

Personal algorithm for finding all most optimal solutions for a Letterboxed puzzle.

## Problem Description

Given a list of letters split into 4 buckets, find the shortest chain of valid words that **use all given letters** where no two consecutive letters come from the same bucket.

Two possible solutions to this problem include an "**open**" and a "**closed**" solution.

### Definitions

**Open** solution: a solution that does not know if a word is a valid dictionary word until it submits it to the game.

**Closed** solution: a solution that has access to a full dictionary of valid words. My work implements a closed solution.

**Most optimal solution** is defined as a solution with the fewest amount of words possible.

**Chain**: a series of words where each subsequent word begins with the last letter of the previous word.

**Valid word**: a word within the game's dictionary. Since NYT Games has never released their Letterboxed dictionary, I use a custom one.

**Coverage**: the number of unique letters used by a word.

## Solution Implementation

We know Letterboxed puzzles have 2-3 word solutions, so I only worked with chains of 2-3 words.

### Dictionary

I used the `wordfreq` library to pull the $100000$ most frequent English words, just as a base vocabulary, and then filter to all words with a ZipF frequency above $2.5$. This still does not include all words the NYT uses, such as "schmutz".

### Process

### Correctness

## An Open Solution?

An open solution means submitting words to the black box of Letterboxd blind. One could start by generating all possible words under or equal to a certain arbitrary length, checking their validity against the black box, generating a dictionary from this and then applying the closed solution.

If we select an arbitrary word legnth of 14, this results in a total of

$12 \* 9^2 + 12 \* 9^3 + ... + 12 \* 9^13 = 12 \sum\_{k=2}^{13} 9^{k} = 34 315 188 682 320 $

34 trillion options. Maybe not.
