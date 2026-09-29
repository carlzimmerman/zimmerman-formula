#!/usr/bin/env python3
"""p02_matching_scan.py -- which natural 'matching conditions' between a Schwarzschild black hole and de Sitter give Z^2 = 32 pi/3 ?

PRE-DECLARED MENU (fixed before any result was computed).  c = G = 1.  Two objects:
  BH : Schwarzschild, mass M,  r_s = 2M,  kappa = 1/(4M),  Z := 1/(a0 L) with a0 := kappa_BH  =>  Z = 4M/L
  dS : de Sitter,      radius L,  Lambda = 3/L^2,  kappa = 1/L
Each object carries a list of scalar quantities with a length-dimension d (the power of length).  A 'matching condition' equates one
BH quantity with one dS quantity of the SAME dimension; solving gives M/L, hence Z^2 = 16 M^2/L^2.  Every same-dimension pair is
tested (no pair is dropped or added after seeing results).  The question for each: is Z^2 exactly 32 pi/3 ?

The scan also records whether Z^2 contains pi, to test the claim that a pure-metric matching cannot produce the pi in 32 pi/3.
Controls: (C1) a deliberately wrong rho_Lambda (missing the 8 pi) must remove the exact hit; (C2) the scan must find the known
K_Sigma = rho_Lambda pair.  Exit 0 = the pre-declared scan ran and the controls behaved; the findings are the printed table.
"""
import itertools
import sys
import sympy as sp

pi = sp.pi
M, L = sp.symbols('M L', positive=True)

# (name, dimension d, expression) -- BH in terms of M, dS in terms of L.  Dimensions: powers of length (G = c = 1).
BH = [
    ("r_s = 2M",                          1, 2 * M),
    ("1/kappa = 4M",                      1, 4 * M),
    ("Misner mass M",                     1, M),
    ("kappa = 1/(4M)",                   -1, 1 / (4 * M)),
    ("static Euler charge int E4 dV3",   -1, 8 * pi / M),
    ("area A = 4 pi r_s^2",               2, 16 * pi * M**2),
    ("entropy S = A/4",                   2, 4 * pi * M**2),
    ("horizon Gauss curvature 1/r_s^2",  -2, 1 / (4 * M**2)),
    ("kappa^2",                          -2, 1 / (16 * M**2)),
    ("mean density 3/(8 pi r_s^2)",      -2, 3 / (32 * pi * M**2)),
    ("horizon Kretschmann = E4",         -4, 3 / (4 * M**4)),
    ("flat-ball volume 4 pi r_s^3/3",     3, 32 * pi * M**3 / 3),
]
DS = [
    ("L",                                 1, L),
    ("1/kappa = L",                       1, L),
    ("Misner mass L/2",                   1, L / 2),
    ("kappa = 1/L",                      -1, 1 / L),
    ("static Euler charge int E4 dV3",   -1, 32 * pi / L),
    ("area A = 4 pi L^2",                 2, 4 * pi * L**2),
    ("entropy S = pi L^2",                2, pi * L**2),
    ("horizon Gauss curvature 1/L^2",    -2, 1 / L**2),
    ("kappa^2 = Lambda/3",               -2, 1 / L**2),
    ("Lambda = 3/L^2",                   -2, 3 / L**2),
    ("Ricci scalar R = 12/L^2",          -2, 12 / L**2),
    ("rho_Lambda = Lambda/(8 pi)",       -2, 3 / (8 * pi * L**2)),
    ("static-patch volume 4 pi L^3/3",    3, 4 * pi * L**3 / 3),
    ("Kretschmann = E4 = 24/L^4",        -4, 24 / L**4),
]

def scan(bh, ds):
    rows = []
    for (nb, db, eb), (nd, dd, ed) in itertools.product(bh, ds):
        if db != dd:
            continue
        sol = sp.solve(sp.Eq(eb, ed), M)
        sol = [s for s in sol if s.is_positive]
        if not sol:
            continue
        Z2 = sp.simplify(16 * sol[0]**2 / L**2)
        rows.append((nb, nd, Z2, float(Z2), Z2.has(pi)))
    return rows

target = 32 * pi / 3
rows = scan(BH, DS)
print(f"pre-declared menu: {len(BH)} black-hole quantities x {len(DS)} de Sitter quantities; {len(rows)} same-dimension pairs\n")
print(f"  {'BH quantity':<34}{'= dS quantity':<34}{'Z^2':>16}{'Z^2 (num)':>11}  contains pi")
exact = []
for nb, nd, Z2, zf, hp in sorted(rows, key=lambda r: r[3]):
    hit = sp.simplify(Z2 - target) == 0
    if hit:
        exact.append((nb, nd))
    print(f"  {nb:<34}{nd:<34}{str(Z2):>16}{zf:>11.3f}  {'yes' if hp else 'no '}{'   <== EXACTLY 32 pi/3' if hit else ''}")

n_pi = sum(1 for r in rows if r[4])
print(f"\n  pairs whose Z^2 contains pi: {n_pi} of {len(rows)}")
print(f"  pairs giving EXACTLY Z^2 = 32 pi/3: {len(exact)}")
for nb, nd in exact:
    print(f"      {nb}   =   {nd}")
near = [(nb, nd, zf) for nb, nd, Z2, zf, hp in rows if abs(zf / float(target) - 1) < 0.10 and sp.simplify(Z2 - target) != 0]
print(f"  other pairs within 10% of 32 pi/3 (33.51): {len(near)}")
for nb, nd, zf in near:
    print(f"      {nb} = {nd}: Z^2 = {zf:.3f}")

# The structural claim: pairs whose BOTH sides are pi-free give a pi-free Z^2 (algebraic); a pi in Z^2 needs a pi on exactly one side.
print("\n  pi-content of the two sides vs pi in Z^2 (the structural claim):")
def has_pi(expr): return sp.sympify(expr).has(pi)
tally = {}
for (nb, db, eb), (nd, dd, ed) in itertools.product(BH, DS):
    if db != dd:
        continue
    sol = [s for s in sp.solve(sp.Eq(eb, ed), M) if s.is_positive]
    if not sol:
        continue
    key = (has_pi(eb), has_pi(ed), sp.simplify(16 * sol[0]**2 / L**2).has(pi))
    tally[key] = tally.get(key, 0) + 1
for (pb, pd, pz), n in sorted(tally.items()):
    print(f"      BH side has pi: {str(pb):<5} dS side has pi: {str(pd):<5} -> Z^2 has pi: {str(pz):<5}   ({n} pairs)")
claim_ok = all(pz == (pb != pd) or (pb and pd and not pz) or (pb and pd and pz) for (pb, pd, pz) in tally)
both_free_no_pi = all(not pz for (pb, pd, pz) in tally if (not pb and not pd))
one_side_pi = any(pz for (pb, pd, pz) in tally if pb != pd)

# ------------------------------------------------------------------ controls
print("\nControls")
DS_bad = [(n, d, (3 / L**2 / 8) if n.startswith("rho_Lambda") else e) for n, d, e in DS]     # rho_Lambda without the 1/pi
rows_bad = scan(BH, DS_bad)
exact_bad = [1 for nb, nd, Z2, zf, hp in rows_bad if sp.simplify(Z2 - target) == 0]
c1 = len(exact_bad) == 0
c2 = ("horizon Gauss curvature 1/r_s^2", "rho_Lambda = Lambda/(8 pi)") in exact
print(f"  C1  with rho_Lambda deliberately wrong (the 1/pi dropped) the exact hit disappears: {c1}")
print(f"  C2  the scan finds the known K_Sigma = rho_Lambda pair: {c2}")
print(f"  C3  both-sides-pi-free pairs never give a pi in Z^2: {both_free_no_pi};  a pi in Z^2 needs a pi on one side: {one_side_pi}")
sys.exit(0 if (c1 and c2 and both_free_no_pi) else 1)
