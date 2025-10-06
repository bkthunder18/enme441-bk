import numpy as np
import matplotlib.pyplot as plt

# parameters
E = 30e6          # psi
nu = 0.30
G = E/(2*(1+nu))  # psi
c = 10/9          # circular section (use your value if different)

r = np.linspace(1, 20, 400)  # L/d range

Phi_b = (64/(3*np.pi)) * r**3
Phi_total = Phi_b + (E/G) * (4*c/np.pi) * r
pct_error = 100 * ((E/G) * (4*c/np.pi) * r) / Phi_total

# Example: plot normalized deflection vs L/d
plt.figure(1)
plt.plot(r, Phi_b, label='Bending only')
plt.plot(r, Phi_total, label='Bending + Shear')
plt.xlabel('L/d')
plt.ylabel('Deflection')
plt.legend(); plt.grid(True); plt.title('Deflection vs L/d')

# Example: percent error curve
plt.figure(2)
plt.plot(r, pct_error)
plt.xlabel('L/d'); plt.ylabel('% error (omit shear)')
plt.grid(True); plt.title('Percent error vs L/d')
plt.show()
