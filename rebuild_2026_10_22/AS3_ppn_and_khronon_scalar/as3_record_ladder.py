#!/usr/bin/env python3
"""AS3: what the record's ladder (aest_j10/wf3_base_aest_eta_K_solve.py) solves, on its own action L2dc_v2.pkl rebuilt from route2_v2_build.py (a copy run in scratch, record untouched).
Path of the pickle in argv[1]. Prints whether O(w^0) has a free direction, what fixes it, and whether the ladder's solution solves the exact system at finite w. No timing."""
import pickle, sys, sympy as sp

L = pickle.load(open(sys.argv[1], "rb"))
KB, Q0, K2, JY = sp.symbols("K_B Q_0 K_2 J_Y", real=True)
wb = sp.symbols("w_b", positive=True); w1, w2, w3 = sp.symbols("w1 w2 w3", real=True)
GT, LAM, kx = sp.symbols("G_t Lambda k_x", real=True)
S = sp.Symbol
names = ["Psi", "Phi", "B2", "B3", "s22", "s23", "a1", "a2", "a3", "chi"]
K_ = [S(n + "k") for n in names]; B_ = [S(n + "b") for n in names]; Rk = S("rhok")
print("L2 free symbols:", sorted(str(s) for s in L.free_symbols))
sub = {GT: 1, LAM: 0, kx: 1, KB: sp.Rational(1, 5), K2: 10, Q0: sp.Rational(2, 5), JY: 1}
eq = {b: sp.expand(sp.diff(L, b).subs(sub)) for b in B_}
out = {}
M0 = sp.Matrix([[eq[b].coeff(wb, 0).subs({w1: 0, w2: 0, w3: 0}).coeff(k) for k in K_] for b in B_])
print("O(w^0) block rank", M0.rank(), "of", len(K_), "; null space:", [list(v.T) for v in M0.nullspace()])
# longitudinal flow: w1 only, the source at rest in these coordinates, aether moving along k
for lab, wv in (("w along k (w1)", {w1: 1, w2: 0, w3: 0}), ("w perp k (w2)", {w1: 0, w2: 1, w3: 0})):
    E = [eq[b].subs(wv) for b in B_]
    A, c = sp.linear_eq_to_matrix(E, K_)
    wnum = sp.Rational(1, 10)
    An = A.subs(wb, wnum); cn = c.subs(wb, wnum)
    rA = An.rank(); print(lab, "at w_b = 1/10, truncated to O(w^2): rank", rA, "augmented", An.row_join(cn).rank())
    # order by order
    A0, A1, A2 = [A.applyfunc(lambda e: sp.expand(e).coeff(wb, o)) for o in (0, 1, 2)]
    c0 = c.applyfunc(lambda e: sp.expand(e).coeff(wb, 0))
    z0 = sp.symbols("z0:10"); z1 = sp.symbols("y0:10")
    v0, v1 = sp.Matrix(z0), sp.Matrix(z1)
    so = sp.solve(list(A0 * v0 - c0) + list(A0 * v1 + A1 * v0 - c.applyfunc(lambda e: sp.expand(e).coeff(wb, 1))), list(z0) + list(z1), dict=True)
    print("  orders 0 and 1 solvable:", bool(so))
    if so:
        s = so[0]
        print("  Psi0/rho", s.get(z0[0], "free"), " a1 at O(0):", s.get(z0[6], "free"), " chi at O(0):", s.get(z0[9], "free"))

print("\nRecord's L2 at w = 0, k = 1, K_B = 1/5, J_Y = 1, Q0 = 2/5, K2 = 10: coefficient of bra*ket")
vals = {wb: 0, GT: 1, LAM: 0, kx: 1, KB: sp.Rational(1, 5), JY: 1, Q0: sp.Rational(2, 5), K2: 10}
L0 = sp.expand(L.subs(vals))
A1k, A1b, Ck, Cb, Pk, Pb = S("a1k"), S("a1b"), S("chik"), S("chib"), S("Psik"), S("Psib")
tab = {}
for b_, k_ in ((Pb, Ck), (Pb, A1k), (Cb, Ck), (Cb, A1k), (A1b, Ck), (A1b, A1k), (Pb, Pk)):
    tab[str(b_) + "*" + str(k_)] = sp.nsimplify(L0.coeff(b_).coeff(k_))
    print(" ", b_, k_, tab[str(b_) + "*" + str(k_)])
c_ = sp.Rational(9, 5); Wv = 2; qv = sp.Rational(2, 5)
print("Covariant form 2c a.V - c W V^2, a_1 = i k Psi, V_1 = i k chi + Q0 a1: u = chi + Q0 a1/(i k) is the only combination.")
print("  so Psib*a1k / Psib*chik must be Q0/(i k) =", qv / sp.I, "; record:", sp.nsimplify(tab["Psib*a1k"] / tab["Psib*chik"]) if tab["Psib*chik"] != 0 else None)
print("  and chib*a1k / chib*chik must be", qv / sp.I, "; record:", sp.nsimplify(tab["chib*a1k"] / tab["chib*chik"]))
print("  and a1b*a1k / a1b*chik must be", qv / sp.I, "; record:", sp.nsimplify(tab["a1b*a1k"] / tab["a1b*chik"]))
