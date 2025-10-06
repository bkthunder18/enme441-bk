#cd C:\Users\bryan\OneDrive\Documents\ENME441

#Must use f-string

''' 
Bryan Kennedy
ENME441
Lab 1
Taylor Series Expansion
'''

x = .5
sum = 0

# Problem 1
for k in range(1, 6):
    sum += ((-1)**(k-1)*(x-1)**k)/(k)

print(f"f(0.5) ~= {sum:.9f} with {k} terms")


k = 1
sum = 0
addition = 100

# Problem 2
while abs(addition) >= 1e-7:
	addition = ((-1)**(k-1)*(x-1)**k)/(k)
	sum += addition
	k += 1

print(f"f(0.5) ~= {sum:.9f} with {k} terms")