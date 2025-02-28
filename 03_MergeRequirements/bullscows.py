import random

def bullscows(guess: str, solution: str) -> tuple[int, int]:
    bulls=sum(guess[i]==solution[i] for i in range(min(len(guess),len(solution))))
    cows=max(len((set(guess)&set(solution)))-bulls,0)
    return (bulls, cows)

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    solution=words[random.random]
    asksCount=0
    b=-1
    while b!=len(solution):
        guess=ask("Enter the word: ", words)
        b,c=bullscows(guess, solution)
        inform("Bulls: {}, Cows: {}", b, c)
        askCount+=1
    #print("You found the solution in", askCount, "attempts. Well done!")
    return askCount

def ask(*args): pass

def inform(*args): pass