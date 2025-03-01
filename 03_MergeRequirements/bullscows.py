import random
import sys
import urllib.request

DEFAULT_LENGTH=5

def bullscows(guess: str, solution: str) -> tuple[int, int]:
    bulls=sum(guess[i]==solution[i] for i in range(min(len(guess),len(solution))))
    cows=sum(min(guess.count(letter),solution.count(letter)) for letter in set(guess)&set(solution))-bulls
    return (bulls, cows)

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    solution=words[random.randint(0, len(words)-1)]
    askCount=0
    b=-1
    while b!=len(solution):
        guess=ask("Enter the word: ", words)
        b,c=bullscows(guess, solution)
        inform("Bulls: {}, Cows: {}", b, c)
        askCount+=1
    return askCount

def ask(prompt: str, valid: list[str] = None) -> str:
    print(prompt, end='')
    guess=input().lower()
    if not valid: return guess
    while guess not in valid:
        print('You have to enter a valid word\n'+prompt, end='')
        guess=input().lower()
    return guess

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))

def main():
    
    def setLength() -> int:
        try:
            length=int(sys.argv[2])
        except:
            length=DEFAULT_LENGTH
            print("Set default length value", length)   
        return length
    
    def getData(link: str) -> set[str]:
        if link.startswith('http'):
            filling=urllib.request.urlopen(link).read().decode('utf-8')
        else:
            filling=open(link).read()
        data={word.strip().lower() for word in filling.split()}-{''}
        return data
    
    def getWordlist(length: int) -> list[str]:
        data=getData(sys.argv[1])
        words=[word for word in data if len(word)==length]
        if not words:
            print("No words of length", length, "found in provided file. \
All submitted words of any length will be taken into account")
            words=list(data)
        return words
    
    if len(sys.argv) < 2:
        print("Usage: python -m bullscows <wordlist-link> [words-length]")
        return
    
    length=setLength()
    words=getWordlist(length)
    askCount = gameplay(ask, inform, words)
    print("You found the solution in", askCount, "attempts. Well done!")


if __name__ == "__main__":
    try: main()
    except: print('\nGame stopped. See you soon!')