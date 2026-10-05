"""p17: try to DERIVE G rho_Lambda r_s^2 = c^2 (the puzzle; r_s = Schwarzschild radius with surface gravity a0).
G = c = 1. Black hole: M = r/2, surface gravity kappa = 1/(2r). Vacuum: density rho, pressure p = -rho.
Each row is a physical condition linking the hole to the vacuum; sympy solves it for k = rho r^2. The puzzle needs k = 1.
POST-HOC menu, written knowing the target (as p02); it tests whether any standard condition gives 1, not a false-positive rate.

Run: python3 p17_natural_conditions.py  |  MUTATE=1: the target becomes 3/(8 pi) (row C1's value), so check A must fail
"""
import os, sys
import sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
rho, r = sp.symbols("rho r", positive=True)
pi = sp.pi
M, kap = r / 2, 1 / (2 * r)
H2 = 8 * pi * rho / 3                     # Friedmann / de Sitter H^2 for the vacuum
gL = 4 * pi / 3 * (rho + 3 * (-rho)) * r  # Newtonian-limit vacuum field at r (rho+3p = -2 rho): magnitude 8 pi rho r/3, outward
rows = {
 "C1 vacuum ball of radius r is its own black hole (escape speed c)":      sp.Eq(2 * (4 * pi / 3 * rho * r**3) / r, 1),
 "C2 vacuum energy inside r equals the hole's mass":                        sp.Eq(4 * pi / 3 * rho * r**3, M),
 "C3 vacuum repulsion at r equals the hole's surface gravity":              sp.Eq(-gL, kap),
 "C4 vacuum potential |Phi_L(r)| = (4pi/3) rho r^2 equals the hole's GM/r": sp.Eq(4 * pi / 3 * rho * r**2, M / r),
 "C5 vacuum pressure force on the horizon equals F_max = 1/4":             sp.Eq(rho * 4 * pi * r**2, sp.Rational(1, 4)),
 "C6 Hubble radius of the vacuum equals r":                                  sp.Eq(H2 * r**2, 1),
 "C7 de Sitter horizon area equals the hole's area (equal entropies)":      sp.Eq(4 * pi * 3 / (8 * pi * rho), 4 * pi * r**2),
 "C8 vacuum free-fall time equals light-crossing time of r":                sp.Eq(3 * pi / (32 * rho), r**2),
 "C9 Komar (rho+3p) mass of the vacuum inside r equals M":                  sp.Eq(2 * rho * 4 * pi / 3 * r**3, M),
 "C10 horizon Gauss curvature 1/r^2 equals vacuum 4D Ricci R = 4 Lambda":   sp.Eq(1 / r**2, 4 * 8 * pi * rho),
 "C11 hole's tidal field 2M/r^3 equals vacuum tidal field H^2":             sp.Eq(2 * M / r**3, H2),
 "C12 BH mean density 3/(8 pi r^2) equals rho":                             sp.Eq(3 / (8 * pi * r**2), rho),
 "C13 vacuum energy in the shell A*r (= 4 pi r^3) equals the hole's mass":  sp.Eq(rho * 4 * pi * r**3, M),
}
target = 3 / (8 * pi) if MUTATE else sp.Integer(1)
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
hits = []
for name, eq in rows.items():
    k = sp.simplify(sp.solve(eq, rho)[0] * r**2)
    ratio = sp.nsimplify(sp.simplify(k / target))
    pipow = sp.degree(sp.numer(sp.together(k)), pi) - sp.degree(sp.denom(sp.together(k)), pi)
    print(f"{name:74s} rho r^2 = {str(k):10s} ({float(k):.4f})  pi^{int(pipow):+d}   x target: {float(k/target):.4f}")
    if sp.simplify(k - target) == 0: hits.append(name)
print(f"\ntarget rho r^2 = {target}; rows that hit it: {hits or 'none'}")
check("A no standard condition gives rho r^2 = 1 exactly", not hits)
ks = [sp.simplify(sp.solve(e, rho)[0] * r**2) for e in rows.values()]
check("B every row carries exactly one net power of pi (pi^+1 or pi^-1), so none can be the pi-free 1",
      all(abs(sp.degree(sp.numer(sp.together(k)), pi) - sp.degree(sp.denom(sp.together(k)), pi)) == 1 for k in ks))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
