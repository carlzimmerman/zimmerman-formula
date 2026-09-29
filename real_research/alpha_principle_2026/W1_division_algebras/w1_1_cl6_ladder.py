#!/usr/bin/env python3
"""w1_1_cl6_ladder -- Furey (arXiv:1603.04078): the complex-octonion ladder system, Q = N/3, SU(3)_c; what is fixed, what is free.  Pre-registered L1-L6.

Exact sympy arithmetic on 8 x 8 matrices over Q(i, sqrt3).
Run (real):    python3 w1_1_cl6_ladder.py          -> exit 0 if every check passes (2 otherwise)
Run (control): python3 w1_1_cl6_ladder.py MUTATE   -> corrupts the octonion table (sign of the triple 5,6,1); exit 1 if the control bites, 3 if it does not.
"""
import sys
sys.dont_write_bytecode = True
import itertools
from fractions import Fraction
import sympy as sp
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import w1_lib as W

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
chk = W.Checks(MUT)
I = sp.I
Lm = W.oct_left_sp(corrupt=MUT)                # Lm[a] = left multiplication by e_a (real 8x8)
E8 = sp.eye(8)
Z8 = sp.zeros(8)

# ---------------- L1: table sanity
ok_cl = all(sp.simplify(Lm[a] * Lm[b] + Lm[b] * Lm[a] - (-2 * (1 if a == b else 0)) * E8) == Z8 for a in range(1, 8) for b in range(1, 8))
chk("L1a L_a L_b + L_b L_a = -2 delta_ab for a,b = 1..7 (alternativity: the octonion left multiplications generate a Clifford algebra)", ok_cl)
# norm multiplicativity through the identity L_a^T L_a = 1 and antisymmetry
chk("L1b every L_a (a = 1..7) is real antisymmetric with L_a^2 = -1", all(Lm[a].T == -Lm[a] and Lm[a] * Lm[a] == -E8 for a in range(1, 8)))
# e7 = e1(e2(e3(e4(e5(e6 f))))) claimed in Furey 1910.08395 eq (4)
vol = Lm[1] * Lm[2] * Lm[3] * Lm[4] * Lm[5] * Lm[6]
chk("L1c L_e1 L_e2 L_e3 L_e4 L_e5 L_e6 = L_e7 (e7 is redundant as a left-action map)", vol == Lm[7], "(product of the six left maps vs L_e7)")

# ---------------- L2: ladder operators
a1 = (-Lm[5] + I * Lm[4]) / 2
a2 = (-Lm[3] + I * Lm[1]) / 2
a3 = (-Lm[6] + I * Lm[2]) / 2
al = [a1, a2, a3]
ad = [(Lm[5] + I * Lm[4]) / 2, (Lm[3] + I * Lm[1]) / 2, (Lm[6] + I * Lm[2]) / 2]     # alpha_i^dagger as written in the paper
acomm = lambda A, B: (A * B + B * A).applyfunc(sp.expand)
ok_low = all(acomm(al[i], al[j]) == Z8 for i in range(3) for j in range(3))
ok_up = all(acomm(ad[i], ad[j]) == Z8 for i in range(3) for j in range(3))
ok_mix = all(acomm(al[i], ad[j]) == (E8 if i == j else Z8) for i in range(3) for j in range(3))
chk("L2a {alpha_i, alpha_j} = 0 (eq 3)", ok_low)
chk("L2b {alpha_i^dag, alpha_j^dag} = 0 (eq 4)", ok_up)
chk("L2c {alpha_i, alpha_j^dag} = delta_ij (eq 5)", ok_mix)
chk("L2d the paper's dagger (i -> -i, e_n -> -e_n, order reversed) equals the matrix conjugate transpose", all(ad[i] == al[i].H for i in range(3)))

# ---------------- L3: vacuum, number operator, charges, SU(3)
om = a1 * a2 * a3
omd = ad[2] * ad[1] * ad[0]
P0 = (om * omd).applyfunc(sp.expand)
chk("L3a omega omega^dag is a rank-one projector (P^2 = P, tr = 1)", (P0 * P0 - P0).applyfunc(sp.expand) == Z8 and sp.simplify(P0.trace()) == 1, f"rank {P0.rank()}")
chk("L3b alpha_i omega omega^dag = 0 for all i (vacuum; eq 12)", all((al[i] * P0).applyfunc(sp.expand) == Z8 for i in range(3)))
N = sum((ad[i] * al[i] for i in range(3)), Z8).applyfunc(sp.expand)
ev = sorted(sum(([k] * m for k, m in N.eigenvals().items()), []))
chk("L3c N = sum alpha_i^dag alpha_i has eigenvalues {0,1,1,1,2,2,2,3}", ev == [0, 1, 1, 1, 2, 2, 2, 3], str(ev))
Q = N / 3
qs =sorted(sum(([k] * m for k, m in Q.eigenvals().items()), []))
chk("L3d Q = N/3 spectrum", qs == [0, sp.Rational(1, 3), sp.Rational(1, 3), sp.Rational(1, 3), sp.Rational(2, 3), sp.Rational(2, 3), sp.Rational(2, 3), 1], str(qs))

Ad = ad  # shorthand
Lam = [None,
       (-Ad[1] * al[0] - Ad[0] * al[1]),
       (I * Ad[1] * al[0] - I * Ad[0] * al[1]),
       (Ad[1] * al[1] - Ad[0] * al[0]),
       (-Ad[0] * al[2] - Ad[2] * al[0]),
       (-I * Ad[0] * al[2] + I * Ad[2] * al[0]),
       (-Ad[2] * al[1] - Ad[1] * al[2]),
       (I * Ad[2] * al[1] - I * Ad[1] * al[2]),
       (-(Ad[0] * al[0] + Ad[1] * al[1] - 2 * Ad[2] * al[2]) / sp.sqrt(3))]
Lam = [None] + [M.applyfunc(sp.expand) for M in Lam[1:]]
half = sp.Rational(1, 2)
fs = {}
def setf(i, j, k, v):
    for (a, b, c), s in (((i, j, k), 1), ((j, k, i), 1), ((k, i, j), 1), ((j, i, k), -1), ((i, k, j), -1), ((k, j, i), -1)):
        fs[(a, b, c)] = s * v
s3 = sp.sqrt(3)
for (i, j, k, v) in ((1, 2, 3, 1), (1, 4, 7, half), (1, 5, 6, -half), (2, 4, 6, half), (2, 5, 7, half), (3, 4, 5, half), (3, 6, 7, -half), (4, 5, 8, s3 / 2), (6, 7, 8, s3 / 2)):
    setf(i, j, k, v)
def comm(A, B): return (A * B - B * A).applyfunc(sp.expand)
ok_su3 = True
for i in range(1, 9):
    for j in range(1, 9):
        lhs = comm(Lam[i] / 2, Lam[j] / 2)
        rhs = sum((I * fs.get((i, j, k), 0) * Lam[k] / 2 for k in range(1, 9)), Z8).applyfunc(sp.expand)
        if (lhs - rhs).applyfunc(sp.simplify) != Z8:
            ok_su3 = False
chk("L3e the eight Lambda_i of Furey eq (16) satisfy [L_i/2, L_j/2] = i f_ijk L_k/2 with the standard su(3) structure constants", ok_su3)
chk("L3f [Lambda_i, Q] = 0 for all i", all(comm(Lam[i], Q) == Z8 for i in range(1, 9)))
C2 = sum(((Lam[i] / 2) * (Lam[i] / 2) for i in range(1, 9)), Z8).applyfunc(sp.expand)
# decompose V = C^8 by (N, Casimir, T8 spectrum)
T8 = Lam[8] / 2
rows = []
for n in range(4):
    proj = sp.Matrix(sp.zeros(8))
    # eigenspace of N with eigenvalue n
    ns = (N - n * E8).nullspace()
    if not ns: continue
    B = sp.Matrix.hstack(*ns)
    c2 = sp.simplify((B.pinv() * C2 * B)[0, 0]) if B.shape[1] else None
    t8 = sorted(sp.simplify(x) for x in sum(([k] * m for k, m in (B.pinv() * T8 * B).eigenvals().items()), []))
    rows.append((n, B.shape[1], c2, t8))
    print(f"      N = {n}: dim {B.shape[1]}, Casimir C2 = {c2}, T8 spectrum {t8}")
three = sorted([-1 / (2 * s3), -1 / (2 * s3), 1 / s3], key=lambda x: float(x))
threebar = sorted([1 / (2 * s3), 1 / (2 * s3), -1 / s3], key=lambda x: float(x))
def rep_of(c2, t8):
    if c2 == 0: return "1"
    if sp.simplify(c2 - sp.Rational(4, 3)) == 0:
        if all(sp.simplify(a - b) == 0 for a, b in zip(t8, sorted(three, key=lambda x: float(x)))): return "3"
        if all(sp.simplify(a - b) == 0 for a, b in zip(t8, sorted(threebar, key=lambda x: float(x)))): return "3bar"
    return "?"
# T8 of the fundamental 3 = diag(1/(2 sqrt3), 1/(2 sqrt3), -1/sqrt3); our three/threebar lists are sorted versions
three_true = sorted([1 / (2 * s3), 1 / (2 * s3), -1 / s3], key=lambda x: float(x))
threebar_true = sorted([-1 / (2 * s3), -1 / (2 * s3), 1 / s3], key=lambda x: float(x))
def rep_of2(c2, t8):
    if sp.simplify(c2) == 0: return "1"
    if sp.simplify(c2 - sp.Rational(4, 3)) == 0:
        tt = [sp.simplify(x) for x in t8]
        if all(sp.simplify(a - b) == 0 for a, b in zip(tt, three_true)): return "3"
        if all(sp.simplify(a - b) == 0 for a, b in zip(tt, threebar_true)): return "3bar"
    return "?"
content = {n: rep_of2(c2, t8) for (n, d, c2, t8) in rows}
chk("L3g the eight states are 1 (N=0, Q=0) + 3bar (N=1, Q=1/3) + 3 (N=2, Q=2/3) + 1 (N=3, Q=1)", content == {0: "1", 1: "3bar", 2: "3", 3: "1"}, str(content))

# ---------------- L4: what is fixed
E = {(i, j): (ad[i] * al[j]).applyfunc(sp.expand) for i in range(3) for j in range(3)}
herm = []
for i in range(3):
    herm.append(E[(i, i)])
for i in range(3):
    for j in range(i + 1, 3):
        herm.append((E[(i, j)] + E[(j, i)]).applyfunc(sp.expand))
        herm.append((I * (E[(i, j)] - E[(j, i)])).applyfunc(sp.expand))
def as_real_vec(M):
    v = []
    for x in M:
        v.append(sp.re(sp.expand(x))); v.append(sp.im(sp.expand(x)))
    return v
Mh = sp.Matrix([as_real_vec(M) for M in herm])
chk("L4a the 9 hermitian operators alpha^dag_i h_ij alpha_j are real-linearly independent (dim of their real span = 9 = dim u(3))", Mh.rank() == 9, f"rank {Mh.rank()}")
Mhq = sp.Matrix([as_real_vec(M) for M in herm + [Q]])
Mhc = sp.Matrix([as_real_vec(M) for M in herm + [sp.Rational(-7, 5) * N, 11 * N]])
chk("L4b Q_c = c N lies in that span for EVERY real c (adding Q, -7N/5, 11N does not raise the rank)", Mhq.rank() == 9 and Mhc.rank() == 9)
# SM correlation: charge mod 1 = - triality / 3.  N=1 is 3bar (triality -1), N=2 is 3 (triality +1), N=0,3 singlets.
tri = {0: 0, 1: -1, 2: 1, 3: 0}
def ok_c(c):
    return all(((c * n + sp.Rational(tri[n], 3)) % 1) == 0 for n in range(4))
cs = [sp.Rational(p, 12) for p in range(-48, 49)]
good = [c for c in cs if ok_c(c)]
expected = [c for c in cs if ((c - sp.Rational(1, 3)) % 1) == 0]
chk("L4c the SM correlation (Q mod 1 = -triality/3 on all 8 states) holds exactly for c in 1/3 + Z (scan of 97 multiples of 1/12)", good == expected, f"good = {[str(c) for c in good]}")
chk("L4d the smallest |c| among them is 1/3 (the unit in which the fully excited state e+ has charge 1)", min(good, key=abs) == sp.Rational(1, 3))
print("      L4 verdict: the algebra generates u(3) = su(3) + R N; the coefficient of N (hence the unit of charge, i.e. c) is FREE in the algebra;")
print("      c = 1/3 is selected by the SM correlation between charge and colour triality (input), giving charge RATIOS 0 : 1/3 : 2/3 : 1.")

# ---------------- L5: so(6) content
gens6 = [(I * Lm[a] * Lm[b]).applyfunc(sp.expand) for a in range(1, 7) for b in range(a + 1, 7)]
M15 = sp.Matrix([as_real_vec(M) for M in gens6])
chk("L5a the 15 hermitian bivector operators i L_a L_b (a<b<=6) are real-linearly independent and traceless (spin(6) = su(4))", M15.rank() == 15 and all(sp.simplify(M.trace()) == 0 for M in gens6))
Nc_ = (N - sp.Rational(3, 2) * E8).applyfunc(sp.expand)
M16 = sp.Matrix([as_real_vec(M) for M in gens6 + [Nc_]])
M16q = sp.Matrix([as_real_vec(M) for M in gens6 + [Q]])
chk("L5b N - 3/2 (hence (B-L) = 2(N-3/2)/3) lies in the real span of the 15 bivectors", M16.rank() == 15)
chk("L5c Q = N/3 does NOT lie in that span (tr Q = 4)", M16q.rank() == 16 and sp.simplify(Q.trace()) == 4, f"rank {M16q.rank()}, tr Q = {Q.trace()}")
BL = (2 * (N - sp.Rational(3, 2) * E8) / 3).applyfunc(sp.expand)
chk("L5d Q = (B-L)/2 + 1/2 on the whole 8: the constant 1/2 (= T3R on the ideal, Pati-Salam Q = T3R + (B-L)/2) is not generated by Cl(6)", (Q - BL / 2 - E8 / 2).applyfunc(sp.expand) == Z8)

# ---------------- L6: N_c
n = sp.symbols("n", positive=True)
q_anom_u = sp.Rational(1, 2) + 1 / (2 * n)              # lane G A4c: charge of u (colour-fundamental of SU(n)) for N_c = n, electron = -1
q_fock_dbar = 1 / n                                     # charge of N=1 state of Q = N/n
q_fock_u = (n - 1) / n                                  # charge of N = n-1 state
sol = sp.solve(sp.Eq(q_anom_u, q_fock_u), n)
sol2 = sp.solve(sp.Eq(q_anom_u - 1, -q_fock_dbar), n)
chk("L6a the Fock charge (n-1)/n of the N = n-1 state equals the anomaly-free up-quark charge 1/2 + 1/(2n) only at n = 3", sol == [3], str(sol))
chk("L6b the Fock charge -1/n of the (conjugate) N=1 state equals the anomaly-free down-quark charge 1/(2n) - 1/2 only at n = 3", sol2 == [3], str(sol2))
print("      L6c (statement, not a check): n = number of ladder operators = (dim O - 2)/2 = 3, i.e. O = C + C^3 (Todorov-Dubois-Violette Sec 2); N_c = 3 is a property of the octonions,")
print("      fixed when O is chosen among the Hurwitz algebras of dimension 1, 2, 4, 8; none of the papers offers a dynamical reason for choosing O.")
print("      L6 verdict: given O, N_c = 3 and thirds follow; nothing in the algebra sets the size of the unit charge e (the coupling).")
chk.finish("w1_1")
