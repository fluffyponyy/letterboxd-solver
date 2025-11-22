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

## Solution Implementation

We know Letterboxed puzzles have 2-3 word solutions, so I only worked with chains of 2-3 words.

### When to stop?

