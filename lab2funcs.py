'''
Bryan Kennedy
ENME441
Lab 2 - Functions, Generators, and List Comprehension
Due 9/22/2025
'''

# Problem 1
def between(target, lower=0, upper=0.3):
    if target <= upper and target >= lower:
        return True
    else:
        return False


# Problem 2
def rangef(max, step):
    fmax = float(max)
    fstep = float(step)
    num = 0
    while num <= fmax:
        yield num
        num += fstep

print("Problem 2:", end=" ")
for i in rangef(5, 0.5):
    print(i, end=' ')
print()


# Problem 3
alist = list(rangef(1, 0.25))
print(f"Problem 3 initial: {alist}")

# 3a
import copy
alistInv = copy.deepcopy(alist)
alist += alistInv[::-1]  # ::-1 slices list in reverse
print(f"Problem 3a: {alist}")

# 3b
alist.sort(key=lambda x: between(x, 0, 0.3))
print(f"Problem 3b: {alist}")


# Problem 4
list4 = [i for i in range(0, 17) if i % 2 == 0 or i % 3 == 0]
print(f"Problem 4: {list4}")
