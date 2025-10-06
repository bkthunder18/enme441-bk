Fy = 1
Fz = 2
d1 = 20
d2 = 10
a = 3
b = 7
c = 12
beta = .75



#q2
Tf = (d1 * Fz) / (d2 * (1-beta))
Tb = beta * Tf
Ray = (Tf*b + Tb*b - Fy*c) / (a + b)


print(f'Ray = {Ray}')