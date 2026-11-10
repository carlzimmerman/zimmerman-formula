#!/usr/bin/env python3
"""DT1 design arithmetic (a design note's numbers, NOT a graded lane: no criteria, no label).

The clock's dust term L_K(Q) enters through one function  n(x) = K L_K'(1 + x),  x = Q - 1  (n = 4 pi G rho_dust / c^2, in Mpc^-2).
Facts used (QX17 / TPA1 / MK1's rows, for the quadratic case; here for a general n):
  background      n(xbar(a)) = n0 / a^3                         (conserved charge)
  equation of state  w ~ (1/n) int_0^xbar n dx,   c_s^2 ~ n / n'        (x << 1)
  Jeans           k_J^2 (physical) = 4 pi G rho / c_s^2 = n'(xbar)      (quadratic: k_J = mu_K, MK1 row 2)
  static clock    x = xbar_inf + phi,  phi = |Phi| / c^2,  so a well of depth phi holds dust  n(xbar_inf + phi).
Families:  Q  quadratic  n = mu^2 x;   E  exponential  n = n0 exp((x - xbar0) / xT)  (an isothermal clock: w = c_s^2 = xT).
All numbers here are hand-level design arithmetic. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__)); LOG = open(os.path.join(HERE, "dt1_design.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.write(s + "\n")
c = 299792.458                                  # km/s
H0 = 70.0; Oc = 0.26
n0 = 1.5 * (H0 / c) ** 2 * Oc                   # 4 pi G rho_c0 / c^2 = (3/2) Omega_c (H0/c)^2, Mpc^-2
G = 6.674e-11; Msun = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22; cSI = 2.998e8
rho0 = n0 / Mpc ** 2 * cSI ** 2 / (4 * math.pi * G)          # kg/m^3
rho0_sun = rho0 * kpc ** 3 / Msun                           # Msun / kpc^3
P(f"n0 = {n0:.4e} Mpc^-2  (MK1 row 1: I0/2 = 2.018e-08);  mean cold density today {rho0:.3e} kg/m^3 = {rho0_sun:.1f} Msun/kpc^3")
ZS = (0.0, 3.0, 30.0, 1100.0, 3400.0)
NEED = {0.0: None, 3.0: 5.0, 30.0: 1.0, 1100.0: 0.3, 3400.0: 0.3}   # comoving k (1/Mpc) the dust should still cluster at; hand targets
WELLS = (("dwarf", 1e-7), ("Sun's place in the Milky Way", 2e-6), ("deepest spiral", 4e-6), ("group", 8e-6), ("cluster core", 3e-5))

def report(name, n_of, slope_of, xbar_of, w_of):
    P(f"\n== {name}")
    for z in ZS:
        nb = n0 * (1 + z) ** 3; xb = xbar_of(nb); kJ = math.sqrt(slope_of(xb)); kc = kJ / (1 + z)
        need = NEED[z]; ok = "" if need is None else ("  ok" if kc >= need else f"  SHORT of {need}")
        P(f"  z {z:6.0f}: offset {xb:.3e}; w {w_of(xb):.2e}; c_s {math.sqrt(n_of(xb) / slope_of(xb)) * c:8.1f} km/s; Jeans k {kJ:.3g} /Mpc physical = {kc:.3g} comoving (length {2 * math.pi / kc:.3g} Mpc comoving){ok}")
    xb0 = xbar_of(n0)
    for wname, phi in WELLS:
        ns = n_of(xb0 + phi); m30 = (ns - n0) / n0 * rho0_sun * (4 / 3) * math.pi * 30 ** 3
        P(f"  well {wname:30s} depth {phi:.0e}: dust {ns / n0:10.3g} x mean; if uniform inside 30 kpc that is {m30:.3g} Msun")

# Q: the quadratic at the record's CMB line (MK1 row 1) and at QX2's cluster value
for mu in (198.25, 1.778):
    report(f"quadratic, mu_K {mu} per Mpc", lambda x, mu=mu: mu * mu * x, lambda x, mu=mu: mu * mu, lambda n, mu=mu: n / (mu * mu), lambda x: x / 2)
# E: exponential (isothermal clock), xT = c_s^2 / c^2
for cs in (350.0, 500.0, 1000.0):
    xT = (cs / c) ** 2
    report(f"exponential, c_s {cs:.0f} km/s (xT {xT:.2e})", lambda x, xT=xT: n0 * math.exp(x / xT), lambda x, xT=xT: n0 * math.exp(x / xT) / xT,
           lambda n, xT=xT: xT * math.log(n / n0), lambda x, xT=xT: xT)

# the trade-off lemma, in numbers: cold on forest scales AND galaxies empty
ka = 20.0; na, nb = 27 * n0, 216 * n0; phig = 4e-6
width = (nb - na) / ka ** 2; flat = (na - n0) / phig
P(f"\nTRADE-OFF (any n): if the dust is to cluster at k >= {ka:.0f} /Mpc physical while the background passes from {na / n0:.0f} to {nb / n0:.0f} x today's mean (z 2 to 5),")
P(f"  that stretch of n spans a clock offset of at most {width:.2e}; every well deeper than (offset of the z = 2 background) + {width:.1e} then holds at least {nb / n0:.0f} x the mean.")
P(f"  To keep wells of depth {phig:.0e} (the deepest spirals) below it, n must be flat between today's mean and the z = 2 density: slope <= {flat:.3g} Mpc^-2,")
P(f"  i.e. a Jeans length of at least {2 * math.pi / math.sqrt(flat):.1f} Mpc (physical) for z < 2. The quadratic at the CMB line has slope {198.25 ** 2:.3g}: it floods every well.")
P("\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.")
