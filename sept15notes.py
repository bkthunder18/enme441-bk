'''
Here are some notes from enme441 on sept 15
We (should) start with the rasberry pis next week on monday

iterators via generators
-next(f), function f will run until reaching 'yield'
-yield returns a value for the current iteration

"for _ in range(10):" the _ is a placeholder, for situations where you dont care about what the loop variable is
encouraged to try using generator functions
functions that leverage "yield"

chatgpt tidbit
Useful for Infinite or Unbounded Sequences
Why: You cant store an infinite sequence in memory, but you can generate values as needed.
How: Perfect for streams like sensor data, event logs, or math sequences.

iter() function
-takes an iterable obj as an argument, returns an iterator based on that object
-allows us to manually iterate over the values in the original iterable

global vs local variables - no notes needed


def add(x,y):
    return x + y

one = 1
two = 2
thing = add(one, two)

print(f'{thing}')


'''
