'''
Bryan Kennedy
ENME441
Lab 3 - Mastermind Game
'''
import random as ran

#generate random goal code
goal = [0,0,0,0]
for i in range(0,4):
    goal[i] = ran.randint(1,6)

#print instructions
print("Guess a sequence of 4 values from 1-6")
print("  ○ = one element is in the code but in the wrong place")
print("  ● = one element is in the code and in the correct place")
print()

#inputs/outputs
for turn in range(1, 12+1):
    while True:
        guess_str = input(f"Guess {turn} of 12: ").strip()
        if len(guess_str) == 4 and all(ch in '123456' for ch in guess_str):
            break
        print('Error - invalid input. Please enter exactly 4 digits (1-6).')

    guess = [int(ch) for ch in guess_str]

    result_symbols = []
    unused_goal = goal[:]
    unused_guess = guess[:]

    # exact matches 
    for i in range(4):
        if guess[i] == goal[i]:
            result_symbols.append('●')
            unused_goal[i] = 0
            unused_guess[i] = -1

    # wrong position matches
    for i in range(4):
        if unused_guess[i] != -1:
            for j in range(4):
                if unused_guess[i] == unused_goal[j]:
                    result_symbols.append('○')
                    unused_goal[j] = 0
                    break

    if result_symbols:
        print('Result: ', ''.join(result_symbols))
    else:
        print('Result: ')

    win = result_symbols == ['●'] * 4

    if win:
        print("Correct - you win!")
        break
else:
    print(f"You lose. The correct sequence was: {''.join(str(d) for d in goal)}")

