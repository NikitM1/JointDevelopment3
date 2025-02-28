import random

def bullscows(guess: str, solution: str) -> tuple[int, int]:
    bulls=sum(guess[i]==solution[i] for i in range(min(len(guess),len(solution))))
    cows=max(len((set(guess)&set(solution)))-bulls,0)
    return (bulls, cows)

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    solution=words[random.randint(0, len(words))]
    askCount=0
    b=-1
    while b!=len(solution):
        guess=ask("Enter the word: ", words)
        b,c=bullscows(guess, solution)
        inform("Bulls: {}, Cows: {}", b, c)
        askCount+=1
    print("You found the solution in", askCount, "attempts. Well done!")
    return askCount

def ask(prompt: str, valid: list[str] = None) -> str:
    print(prompt, end='')
    guess=input()
    if valid==None: return guess
    while guess not in valid:
        print('You have to enter a valid word\n'+prompt, end='')
        guess=input()
    return guess

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))
    
#gameplay(ask, inform, ['песни', 'пляски'])