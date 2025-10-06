Fy = 1
Fz = 2
d1 = 20
d2 = 10
a = 10
b = 10
c = 10
beta = .25
x = 18

Tfp = 5.333
Tbp = 1.333
Rayp = 2.833
Razp = -1


#q3
Mz = -(x-a)*Tfp - (x-a)*Tbp + Rayp*x
My = Razp * x

print(f'My = {My}\nMz = {Mz}')