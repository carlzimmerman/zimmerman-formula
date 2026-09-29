#!/usr/bin/env python3
"""N4 -- Nesti-Percacci graviweak unification (arXiv:0706.3307): is the weak coupling tied to G, Lambda?
Action AS PRINTED:  S_R1 = (g1/16 pi) Int R theta theta eps  [Palatini, eq (24)],  torsion term a1 (25),  cosmological term lambda Int theta^4 eps (32),
S_R2 = (1/g2^2) Int (r R + (r^2) theta theta) eps (28).  Broken phase <theta> = M e (18):
  (27): (g1/16 pi) M^2 R + 4 a1 M^2 Theta^2 + 10 K^2,  M_Pl^2 = g1 M^2;   (32): lambda M^4 Int |e| + ...;   (29): (1/g2^2)[-R_munu^j R^{j munu} - W^2 - K^2].
CHECKS
 (a) observables G = 1/(g1 M^2) [M_Pl^2 = g1 M^2 with the 16 pi in the action], vacuum-energy Lambda = 8 pi G lambda M^4 = 8 pi lambda M^2/g1, weak coupling g_W^2 = c_norm g2^2 (c_norm a pure convention number):
     the Jacobian of (G, Lambda, g_W^2) with respect to (g1, g2, M, lambda) has rank 3 -> no relation among G, Lambda, g_W (FREE).
 (b) coefficient ratios: coefficient(R_munu^2) : coefficient(W^2) : coefficient(K^2) = 1 : 1 : 1 (all = 1/g2^2, printed statement after (29)).  Group-theory basis: the SO(4,C)~SL2+ x SL2- adjoint has
     exactly 2 invariant symmetric bilinear forms (one per factor); the Z2 exchange (their eq (16) is the unique Z2-invariant epsilon) leaves exactly 1: a single 1/g2^2.
 (c) 0909.4537 (SO(3,11) chirality): UNSCRIPTED source reading -- the text has no bosonic action; the authors state the bosonic/gauge terms are an omission.
Run:    python3 n4_graviweak_nesti_percacci.py           (exit 0)
MUTATE: python3 n4_graviweak_nesti_percacci.py MUTATE   (asserts the dimension of the invariant forms is 1 WITHOUT the Z2 exchange; must FAIL -> exit 1)
"""
import sys
import sympy as sp
from itertools import combinations

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(n, ok, m=""):
    print(("[PASS] " if ok else "[FAIL] ") + n + " " + m)
    if not ok:
        fails.append(n)

# (a) Jacobian
g1, g2, M, lam, cn = sp.symbols('g1 g2 M lambda c_norm', positive=True)
G = 1 / (g1 * M**2)
Lam = 8 * sp.pi * G * lam * M**4
gW2 = cn * g2**2
J = sp.Matrix([[sp.diff(f, v) for v in (g1, g2, M, lam)] for f in (G, Lam, gW2)])
rk = J.rank()
chk("rank d(G, Lambda, g_W^2)/d(g1, g2, M, lambda) = 3: the three observables are independent functions of the action's coefficients", rk == 3, "rank = %d" % rk)
# explicit statement: at fixed G and Lambda, g_W^2 can be anything
sol = sp.solve([sp.Eq(G, sp.Symbol('Gobs')), sp.Eq(Lam, sp.Symbol('Lobs'))], [g1, lam], dict=True)
chk("G and Lambda can be held at any values while g2 (hence g_W^2) is varied freely", len(sol) == 1 and sp.diff(sol[0][g1], g2) == 0 and sp.diff(sol[0][lam], g2) == 0)

# (b) invariant forms on so(4)
def E(i, j):
    m = sp.zeros(4); m[i, j] = 1; m[j, i] = -1; return m
basis = [E(i, j) for i, j in combinations(range(4), 2)]
def coords(X):
    return sp.Matrix([X[i, j] for i, j in combinations(range(4), 2)])
def ad(Z):
    return sp.Matrix.hstack(*[coords(Z * b - b * Z) for b in basis])
q = sp.symbols('q0:21')
Q = sp.zeros(6, 6); k = 0
for i in range(6):
    for j in range(i, 6):
        Q[i, j] = q[k]; Q[j, i] = q[k]; k += 1
eqs = []
for Z in basis:
    A = ad(Z)
    eqs += list(A.T * Q + Q * A)
solQ = sp.solve(eqs, list(q), dict=True)[0]
free = [x for x in q if x not in solQ]
dim_inv = len(free)
chk("dimension of ad-invariant symmetric bilinear forms on so(4) = 2 (one per simple factor of SO(4,C) = SL2+ x SL2-)", dim_inv == 2, "free parameters = %d" % dim_inv)
# Z2: reflection R = diag(-1,1,1,1) acts on so(4) by conjugation and exchanges the self-dual and anti-self-dual factors
R = sp.diag(-1, 1, 1, 1)
P = sp.Matrix.hstack(*[coords(R * b * R.inv()) for b in basis])
Qgen = Q.subs(solQ)
eqsZ = list(P.T * Qgen * P - Qgen)
solZ = sp.solve(eqsZ, [x for x in free], dict=True)
Q2 = Qgen.subs(solZ[0]) if solZ else Qgen
free2 = sorted(Q2.free_symbols & set(q), key=str)
dim_Z2 = len(free2)
if MUT:
    chk("(MUTATED) dimension of invariant forms is 1 without the Z2 exchange", dim_inv == 1, "dim = %d" % dim_inv)
else:
    chk("after the Z2 exchange (reflection swaps SL2+ and SL2-) exactly 1 invariant form remains: a single coupling 1/g2^2", dim_Z2 == 1, "free parameters = %d" % dim_Z2)
# self-dual / anti-self-dual split check: the two invariant forms are the Killing forms of the two ideals
Lp = [(E(0, 1) + E(2, 3)), (E(0, 2) - E(1, 3)), (E(0, 3) + E(1, 2))]
Lm = [(E(0, 1) - E(2, 3)), (E(0, 2) + E(1, 3)), (E(0, 3) - E(1, 2))]
zero_cross = all((a * b - b * a) == sp.zeros(4) for a in Lp for b in Lm)
chk("self-dual and anti-self-dual so(4) generators commute (two commuting sl2 ideals)", zero_cross)
print("   ratio statement: coefficients of (R_munu^j)^2, (W^j)^2, (K^j)^2 in (29) are all 1/g2^2 (printed); overall 1/g2^2 is NOT constrained by any relation to G = 1/(g1 M^2) or Lambda.")
print("   (c) UNSCRIPTED: arXiv:0909.4537 prints only the fermion action (kinetic form (10)-(11) style); the bosonic part incl. gauge terms is stated to be omitted -> no coefficient to inherit (UNDEFINED).")
print("READING: graviweak unification = FREE for the coupling; the only forced structure is the 1:1:1 ratio of the curvature-squared coefficients, overall 1/g2^2 free (MIXED inside the higher-derivative sector).")
print("SUMMARY: fails =", fails)
sys.exit(1 if fails else 0)
