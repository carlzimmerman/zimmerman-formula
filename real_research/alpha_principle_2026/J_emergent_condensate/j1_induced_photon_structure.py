#!/usr/bin/env python3
"""J1 -- structure of a purely induced (emergent) photon: what sets alpha?

Pre-registration: J_PREREGISTRATION.md (H1). Units hbar = 1, Heaviside-Lorentz; c_photon and v are NOT assumed equal.

Claims verified symbolically (sympy):
  (i)   Weyl/Dirac species with common velocity v: after x = v x' the fermion action is Lorentz invariant, so the induced action is
        -(Z/4) F'F' with Z = e^2 N L /(12 pi^2), L = ln(Lambda^2/mu^2).  Back in physical coordinates: eps = Z/v, 1/mu_m = Z v, c_photon = v.
  (ii)  alpha_eff = e^2/(4 pi Z) = 3 pi/(N L): e and v drop out.  With a bare Maxwell term of equal velocity: 1/alpha = 1/alpha_0 + N L/(3 pi).
  (iii) The per-species coefficients 1/(12 pi^2) (Dirac), 1/(24 pi^2) (Weyl), 1/(48 pi^2) (complex scalar) from the Feynman-parameter integrals,
        and the agreement with lane C's d(1/alpha)/dln(mu) = -2 N/(3 pi).
  (iv)  N_eff = sum N_c q^2 for the SM charged fermions (exact Fractions): 8/3 per generation, 8 for three.

MUTATE control: run with argv `MUTATE` (exit code 1): the permittivity is taken as Z v instead of Z/v, which must break c_photon = v and the e,v cancellation.
"""
import sys
from fractions import Fraction
import sympy as sp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = 0
def check(name, cond):
    global fails
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails += 1

e, v, N, L, a0inv = sp.symbols('e v N L alpha0inv', positive=True)
Z = e**2 * N * L / (12 * sp.pi**2)

# (i) rescaling proof: E' = v E, B' = v^2 B, measure d^3x' = d^3x / v^3
E, B = sp.symbols('E B', positive=True)
Lprime = sp.Rational(1, 2) * Z * ((v * E)**2 - (v**2 * B)**2)          # Lorentz-invariant form in primed coordinates
Lphys = sp.expand(Lprime / v**3)                                         # per physical volume
eps = sp.simplify(Lphys.coeff(E, 2) * 2)
invmu = sp.simplify(-Lphys.coeff(B, 2) * 2)
if MUT:
    eps = Z * v; invmu = Z / v
print("eps =", eps, "; 1/mu_m =", invmu)
c_ph = sp.simplify(1 / sp.sqrt(eps * (1 / invmu)))
check("c_photon = v (induced photon moves at the fermion velocity)", sp.simplify(c_ph - v) == 0)

# (ii) alpha_eff: Coulomb V(r) = e^2/(4 pi eps r), coupling V r /(hbar c_photon)
alpha_eff = sp.simplify(e**2 / (4 * sp.pi * eps * c_ph))
target = 3 * sp.pi / (N * L)
check("alpha_eff = 3 pi /(N L)", sp.simplify(alpha_eff - target) == 0)
check("d alpha_eff / d e = 0 (microscopic charge drops out)", sp.simplify(sp.diff(alpha_eff, e)) == 0)
check("d alpha_eff / d v = 0 (velocity drops out)", sp.simplify(sp.diff(alpha_eff, v)) == 0)

# bare term of the same velocity: L = (1/2)(1/e0^2 + Z1)(E^2/v - v B^2) after rescaling A -> A/e
Z1 = N * L / (12 * sp.pi**2)
alpha_tot_inv = sp.simplify(4 * sp.pi * (a0inv / (4 * sp.pi) + Z1))
check("1/alpha = 1/alpha0 + N L/(3 pi) with a bare term", sp.simplify(alpha_tot_inv - (a0inv + N * L / (3 * sp.pi))) == 0)

# (iii) coefficients
x = sp.symbols('x')
dirac = sp.Rational(1, 2) / sp.pi**2 * sp.integrate(x * (1 - x), (x, 0, 1))
weyl = dirac / 2
scalar = sp.Rational(1, 16) / sp.pi**2 * sp.integrate((1 - 2 * x)**2, (x, 0, 1))
check("Dirac coefficient 1/(12 pi^2)", sp.simplify(dirac - 1 / (12 * sp.pi**2)) == 0)
check("Weyl coefficient 1/(24 pi^2)", sp.simplify(weyl - 1 / (24 * sp.pi**2)) == 0)
check("complex scalar coefficient 1/(48 pi^2)", sp.simplify(scalar - 1 / (48 * sp.pi**2)) == 0)
mu, Lam = sp.symbols('mu Lambda', positive=True)
lane_c = sp.simplify(sp.diff(N * sp.log(Lam**2 / mu**2) / (3 * sp.pi), mu) * mu)
check("d(1/alpha)/dln(mu) = -2 N/(3 pi) (agrees with lane C)", sp.simplify(lane_c + 2 * N / (3 * sp.pi)) == 0)

# (iv) SM charged-fermion N_eff (Dirac-equivalents, charges in units of e)
per_gen = Fraction(1) + 3 * Fraction(2, 3)**2 + 3 * Fraction(1, 3)**2
check("N_eff per generation = 8/3", per_gen == Fraction(8, 3))
check("N_eff (3 generations) = 8", 3 * per_gen == 8)
print("N_eff rescales with the unit of charge: unit e/3 -> x9 =", 9 * 3 * per_gen, "(the holonomy quantum is a physical choice)")

# inputs needed (report only)
Lreq = lambda Neff: 3 * sp.pi * sp.Float('137.035999177', 12) / Neff
for Neff in (1, sp.Rational(8, 3), 8):
    print("N_eff=%s: required ln(Lambda^2/mu^2) = %s -> Lambda/mu = 10^%s" % (Neff, sp.N(Lreq(Neff), 6), sp.N(Lreq(Neff) / 2 / sp.log(10), 5)))
print("SUMMARY: e and v cancel; inputs are N_eff and Lambda/mu only. fails =", fails)
sys.exit(1 if fails else 0)
