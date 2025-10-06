import numpy as np

x = 30.0
y = 0.001
E = 32e3
nd = 1.25

# Define A and discriminant
A = (x**3 / 3.0) - (30.0 * x**2)
disc = A**2 + 0.004 * x * y

# Quadratic roots for I
Iplus  = (A + np.sqrt(disc)) / (2.0 * E * y)
Iminus = (A - np.sqrt(disc)) / (2.0 * E * y)

# Pick the physically valid (positive) solution
I = Iplus if Iplus > 0 else Iminus

print(f'Iplus = {Iplus}, Iminus = {Iminus}')
print(f'Chosen I = {I}')

# Diameter calculation
d = ((64.0 * I) / np.pi) ** 0.25
dmin = d * nd

print(f'd = {d}, dmin = {dmin}')
