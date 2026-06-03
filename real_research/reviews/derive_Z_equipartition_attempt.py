#!/usr/bin/env python3
"""
Can equipartition FORCE the 1/2 in a0 = (c/2) sqrt(G rho)?  An honest attempt.
=============================================================================
The 1/2 is the only undetermined factor in Z = 2 sqrt(8pi/3). The most rigorous
place a clean 1/2 lives is equipartition (E = 1/2 N kT). So we try to build a0 from
an equipartition argument on a holographic screen at the FREE-FALL scale (so that
sqrt(G rho) appears, not the horizon scale that gives Verlinde's ~6), and ask whether
the coefficient comes out 1/2. We do the algebra exactly and report what it gives --
even if it is the wrong number. (Manufacturing a 1/2 would be the numerology trap.)
"""
import numpy as np

c, G, hbar, Mpc = 2.99792458e8, 6.674e-11, 1.0546e-34, 3.0857e22
H0 = 67.4e3/Mpc
rho = 3*H0**2/(8*np.pi*G)                       # critical density
lP2 = G*hbar/c**3                               # Planck area
FRAMEWORK = 0.5                                 # the target coefficient: a0 = (1/2) c sqrt(Grho)


def a_from_screen(R, M):
    """Standard holographic equipartition: Mc^2 = (1/2) N kT, N=A/lP^2, kT=hbar a/(2 pi c).
    Returns the acceleration a it implies (this is Verlinde's route -> Newton)."""
    N = 4*np.pi*R**2/lP2
    # Mc^2 = (1/2) N kT = (1/2) N hbar a/(2 pi c)  ->  a = Mc^2 * 2 * 2 pi c/(N hbar)
    a = M*c**2 * 2 * (2*np.pi*c)/(N*hbar)
    return a


print("="*82)
print("ATTEMPT: equipartition on a free-fall-scale screen -> does the 1/2 appear?")
print("="*82)

# Sanity: the standard local screen must reproduce Newton a = GM/R^2.
R_test, M_test = 1e20, 1e40
a_newton_check = a_from_screen(R_test, M_test)
print(f"\n[check] standard screen reproduces Newton: a={a_newton_check:.3e} vs GM/R^2="
      f"{G*M_test/R_test**2:.3e}  ({'OK' if abs(a_newton_check/(G*M_test/R_test**2)-1)<1e-6 else 'FAIL'})")

# Free-fall screen: radius = free-fall light-crossing length, enclosing the MEAN density.
R_ff = c/np.sqrt(G*rho)                          # = c / sqrt(G rho)
M_ff = (4/3)*np.pi*R_ff**3*rho                   # mean density enclosed
a_ff = a_from_screen(R_ff, M_ff)                 # = GM/R^2 = (4pi/3) G rho R_ff
coeff = a_ff/(c*np.sqrt(G*rho))                  # a = coeff * c sqrt(G rho)

print(f"""
  Free-fall screen:  R = c/sqrt(G rho) = {R_ff:.3e} m,  M = (4/3)pi R^3 rho.
  Equipartition (the 1/2 is in Mc^2 = 1/2 N kT) + Unruh + holography gives a = GM/R^2:
     a = (4pi/3) c sqrt(G rho)  ->  coefficient = {coeff:.3f}   (= 4pi/3 = {4*np.pi/3:.3f})
  But the framework needs coefficient = 1/2 = {FRAMEWORK}.
     ratio  (got/target) = {coeff/FRAMEWORK:.3f}  = 8pi/3 = {8*np.pi/3:.3f}  <-- exactly the Friedmann factor.""")

# express both as Z = c H0 / a0
Z_ff = c*H0/a_ff
print(f"\n  In Z units:  this equipartition screen gives Z = cH0/a = {Z_ff:.2f}")
print(f"               (a0 = {a_ff:.2e} m/s^2 -- about 8x too BIG; ruled out).")
print(f"               the framework wants Z = 2 sqrt(8pi/3) = {2*np.sqrt(8*np.pi/3):.2f}.")

print("\n"+"="*82)
print("WHY IT DOES NOT CLOSE -- the honest tension")
print("="*82)
print(f"""  There are two clean equipartition setups, and NEITHER gives (c/2)sqrt(G rho):
    (A) screen at the de SITTER HORIZON (Verlinde):  right ballpark, Z ~ 6 -- but it is
        the ENTROPY route and outputs 6 (rational), not 2 sqrt(8pi/3)=5.79.
    (B) screen at the FREE-FALL scale (this attempt): gives the sqrt(G rho) FORM but the
        wrong coefficient 4pi/3 -> Z=0.69 (a0 ~8x too big).
  The framework's a0=(c/2)sqrt(G rho) sits BETWEEN: it uses the free-fall RATE (so the
  number is right) with a surface-gravity 1/2 (not the equipartition mass-energy budget).
  No single equipartition argument delivers that -- the 1/2 it produces is the one in
  Mc^2=1/2 N kT, which lands on Newton/Verlinde, not on a surface-gravity c^2/2R.

  RESULT: equipartition does NOT force the 1/2. I tried it exactly; it gives 4pi/3 on the
  free-fall screen and ~6 on the horizon. So the 1/2 in a0=(c/2)sqrt(G rho) remains a
  MOTIVATED POSIT (surface gravity / 'v=c/2 per free-fall time'), on exactly the same
  footing as Milgrom's 2pi and Verlinde's 6 -- none of which is derived either. I will
  not manufacture a closure; the honest statement is that this route is open.""")
print("="*82)
