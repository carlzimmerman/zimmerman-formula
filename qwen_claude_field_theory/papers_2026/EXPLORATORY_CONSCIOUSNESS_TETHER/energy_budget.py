"""Energy budget for Reading 1 of the exploratory consciousness-tether essay.

Dark energy in one Hubble volume vs. all human brains (and the biosphere) over the age of the universe.
"""
import math

c = 2.998e8            # m/s
G = 6.674e-11          # m^3 kg^-1 s^-2
H0 = 67.4e3 / 3.086e22  # 1/s
OMEGA_DE = 0.685
AGE_S = 13.8e9 * 3.156e7

rho_crit = 3 * H0**2 / (8 * math.pi * G)
u_de = OMEGA_DE * rho_crit * c**2
R_h = c / H0
E_de = u_de * 4 / 3 * math.pi * R_h**3

E_brains = 20.0 * 8e9 * AGE_S
E_bio = 1e14 * AGE_S

print(f"u_DE           = {u_de:.2e} J/m^3")
print(f"Hubble radius  = {R_h:.3e} m")
print(f"E_DE (Hubble)  = {E_de:.2e} J")
print(f"E brains       = {E_brains:.2e} J  ratio {E_de / E_brains:.1e}")
print(f"E biosphere    = {E_bio:.2e} J  ratio {E_de / E_bio:.1e}")
print(f"c H0 / 2 pi    = {c * H0 / (2 * math.pi):.3e} m/s^2")
