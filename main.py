from itertools import chain, product
from typing import List, Set, Tuple
from trie import Trie

def hop(current: Tuple[str], sides: Set[Tuple[str]], candidates: Set[str], buffer: str="", iter: int=0):
    """Recursively bounce around the letter box, consulting the word trie to validate guesses."""
    if iter == 20:
        print("maximum depth reached")
        return False
    # is the current buffer a member of the NYT word list? if so, it's a candidate
    if trie.search(buffer):
        candidates.add(buffer)
    # is the current buffer a *prefix* of a member of the NYT word list?
    #       - if so it's a candidate, but keep digging!
    #       - example: "arm" is a prefix of "armor", we'd want to find both instead of stopping at "arm"
    if trie.startsWith(buffer):
        for side in sides - {current}:
            for letter in side:
                # recursively hop through each side of the letter box
                hop(side, sides, candidates, buffer + letter, iter+1)
    return

def join_sides(*sides):
    return ''.join(chain(*sides))

def no_common_letters(first: str, second: str):
    """Return True if the two strings share no common letters, otherwise False."""
    return all(letter not in second for letter in first)

def guess_coverage(guesses: Tuple[str, ...], sides: Set[Tuple[str, ...]]):
    """Return the ratio of *possible* letters that are covered by the provided guesses."""
    possible_letters = join_sides(*sides)
    guess_letters = join_sides(*guesses)
    count = sum([letter in guess_letters for letter in possible_letters])
    return (count / len(possible_letters)) * 100

def is_viable_guess(guesses: Tuple):
    return all(pair[0][-1] == pair[1][0] for pair in zip(guesses[:-1], guesses[1:]))

if __name__ == '__main__':
    with open("words.txt", 'r') as f:
        words = {word.strip() for word in f.readlines() if len(word.strip()) > 2}
        trie = Trie(words)

    sides = {tuple(c for c in s) for s in ["pim", "eot", "cna", "yul"]}
    
    candidates: Set[str] = set()

    for start in sides:
        hop(start, sides, candidates)
    
    # Through a ton of list transformations, come up with a list of optimal guesses ordered by length
    sorted_candidates = sorted(candidates, key=lambda x: guess_coverage(tuple(x), sides), reverse=True)
    viable_pairs = filter(is_viable_guess, product(sorted_candidates, sorted_candidates))
    pairs_by_highest_coverage = sorted(viable_pairs, key=lambda x: guess_coverage(x, sides), reverse=True)
    max_coverage = guess_coverage(pairs_by_highest_coverage[0], sides)
    only_optimal_guesses = [guess for guess in pairs_by_highest_coverage if guess_coverage(guess, sides) == max_coverage]
    optimal_shortest_first = sorted(only_optimal_guesses, key=lambda x: sum([len(guess) for guess in x]), reverse=False)

    print(f"{'Top 10 Optimal Guesses:':^30}")
    print('-'*30)
    
    for pair in optimal_shortest_first[:10]:
        print(f"{guess_coverage(pair, sides):<.1f}%: {pair}")