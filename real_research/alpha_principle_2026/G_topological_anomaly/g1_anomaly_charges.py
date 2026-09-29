#!/usr/bin/env python3
"""G1 -- anomaly cancellation: what it fixes (ratios, integers) and what it leaves free (overall coupling). Pre-registered A1-A5.
Run: python3 g1_anomaly_charges.py [MUTATE]   (MUTATE: remove the electron singlet E; the SM charges must then FAIL A1; exits 1)"""
import sys
import sympy as sp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

def anomaly_eqs(y, Nc=3, with_nuR=False):
    """y: dict of hypercharges (left-handed Weyl: Q(Nc,2) U(Nc,1) D(Nc,1) L(1,2) E(1,1) [N(1,1)]).  Returns the 4 equations."""
    yQ, yU, yD, yL = y["Q"], y["U"], y["D"], y["L"]
    yE = y.get("E", 0); yN = y.get("N", 0)
    e_su3 = 2*yQ + yU + yD                                        # SU(Nc)^2 U(1): sum over colour-fund reps of index * y
    e_su2 = Nc*yQ + yL                                            # SU(2)^2 U(1)
    e_grav = 2*Nc*yQ + Nc*yU + Nc*yD + 2*yL + yE + yN             # grav^2 U(1)
    e_cub = 2*Nc*yQ**3 + Nc*yU**3 + Nc*yD**3 + 2*yL**3 + yE**3 + yN**3
    return [e_su3, e_su2, e_grav, e_cub]

# ---- A1: solve for the SM content (Nc = 3, no nu_R)
yQ, yU, yD, yL, yE = sp.symbols("yQ yU yD yL yE")
fields = {"Q": yQ, "U": yU, "D": yD, "L": yL, "E": yE}
if MUT:
    fields_m = dict(fields); fields_m["E"] = 0          # electron singlet removed
else:
    fields_m = fields
eqs = anomaly_eqs(fields_m, 3)
unk = [yQ, yU, yD, yL] + ([] if MUT else [yE])
sols = sp.solve(eqs, unk, dict=True)
print("raw sympy solution set:", sols)

# SM hypercharges (x6): Q 1/6 -> 1, u^c -2/3 -> -4, d^c +1/3 -> +2, L -1/2 -> -3, e^c +1 -> 6
sm = {"Q": 1, "U": -4, "D": 2, "L": -3, "E": 6}
sm_eqs = anomaly_eqs({k: sp.Integer(v) for k, v in sm.items() if not (MUT and k == "E")}, 3)
chk("A1a SM charges (x6) satisfy all 4 anomaly equations", all(sp.simplify(e) == 0 for e in sm_eqs), str(sm_eqs))

s, t = sp.symbols("s t")
B2a = {"Q": s, "U": -4*s, "D": 2*s, "L": -3*s, "E": 6*s}
B2b = {"Q": s, "U": 2*s, "D": -4*s, "L": -3*s, "E": 6*s}
B1 = {"Q": 0, "U": t, "D": -t, "L": 0, "E": 0}
ok_fam = True
for fam in (B1, B2a, B2b):
    ok_fam &= all(sp.simplify(e) == 0 for e in anomaly_eqs({k: sp.sympify(v) for k, v in fam.items()}, 3))
chk("A1b hand-derived families B1, B2(U,D), B2(D,U) satisfy the 4 equations identically in the free parameter", ok_fam)
if not MUT:
    # completeness: sympy's solution set must be exactly these families. Compare as sets of tuples after parametrising.
    got = set()
    for so in sols:
        tup = tuple(sp.simplify(so.get(v, v)) for v in (yQ, yU, yD, yL, yE))
        got.add(tup)
    # each sympy solution must lie in one of the 3 families (test by matching structure)
    def in_family(tup):
        q, u, d, l, e = tup
        # branch B1
        if sp.simplify(q) == 0 and sp.simplify(l) == 0 and sp.simplify(e) == 0 and sp.simplify(u + d) == 0:
            return True
        if q != 0:
            for (cu, cd) in ((-4, 2), (2, -4)):
                if all(sp.simplify(x) == 0 for x in (u - cu*q, d - cd*q, l + 3*q, e - 6*q)):
                    return True
        return False
    chk("A1c every sympy solution lies in {B1, B2a, B2b}", all(in_family(t_) for t_ in got), f"n_solutions={len(got)}")
    # and the number of DISCRETE components with y_Q != 0 is exactly 2 (from a direct algebraic elimination with yQ = 1)
    x = sp.symbols("x")
    p = sp.expand(anomaly_eqs({"Q": 1, "U": x, "D": -2 - x, "L": -3, "E": 6}, 3)[3])
    chk("A1d with y_Q = 1: cubic reduces to (x-2)(x+4) up to a constant, so exactly two discrete branches", sp.factor(p) in (sp.factor(-6*(x-2)*(x+4)), sp.factor(6*(x-2)*(x+4)), sp.factor(-3*(x-2)*(x+4)*2)) or sp.simplify(p / ((x-2)*(x+4))).is_number, sp.factor(p))
    print("      note: the second branch (U<->D swapped) is excluded by the Yukawa/Higgs structure, NOT by anomalies")

# ---- A2: homogeneity => overall normalization free
lam, g = sp.symbols("lambda g", positive=True)
ys = {k: sp.Symbol("y_" + k) for k in "QUDLE"}
E_all = anomaly_eqs(ys, 3)
scaled = anomaly_eqs({k: lam*v for k, v in ys.items()}, 3)
degs = [sp.simplify(sc / e) if e != 0 else None for sc, e in zip(scaled, E_all)]
chk("A2a anomaly polynomials are homogeneous: degrees (1,1,1,3)", degs == [lam, lam, lam, lam**3], str(degs))
gy = {k: g*v for k, v in ys.items()}                                 # matter couplings g*y_i
gy_scaled = {k: (g/lam)*(lam*v) for k, v in ys.items()}
chk("A2b (y -> lambda y, g -> g/lambda) leaves every matter coupling g y_i invariant", all(sp.simplify(gy[k] - gy_scaled[k]) == 0 for k in gy))
# the kinetic term (1/4g^2)F^2 with A -> A: equivalent to rescaling A; physical coupling of the minimal charged field: g*|y_min|
print("      consequence: anomalies fix y_i/y_Q only. The only invariant left is g*y_min, i.e. alpha itself. Free real parameters: 1; discrete choices: 1 (+ the u<->d branch).")

# ---- A3: Witten SU(2)
rows = []
ok_w = True
for Nc in range(1, 8):
    for Ng in range(1, 5):
        ndoublets = Nc*Ng + Ng
        rows.append((Nc, Ng, ndoublets % 2 == 0))
    ok_w &= all((3*Ng + Ng) % 2 == 0 for Ng in range(1, 20))
chk("A3a Witten SU(2): 4 N_g doublets, even for every N_g (Nc = 3)", ok_w)
print("      Witten condition (N_c+1) N_g even:  passes for (N_c, N_g) =", [(a, b) for a, b, c in rows if c][:14], "...")
chk("A3b Nc odd passes for every N_g; Nc even passes only for even N_g", all((c == ((Nc % 2 == 1) or (Ng % 2 == 0))) for Nc, Ng, c in rows))

# ---- A4: general N_c
Nc = sp.symbols("N_c", positive=True, integer=True)
x = sp.symbols("x")
yg = {"Q": 1, "L": -Nc, "E": 2*Nc, "U": x, "D": -2 - x}
eg = anomaly_eqs(yg, Nc)
chk("A4a linear equations at general N_c (y_Q=1) satisfied by y_L=-Nc, y_E=2Nc, y_U+y_D=-2", all(sp.simplify(eg[i]) == 0 for i in range(3)))
cub = sp.expand(eg[3])
roots = sp.solve(cub, x)
chk("A4b cubic gives y_U = -1 +- N_c", set(sp.simplify(r) for r in roots) == {-1 + Nc, -1 - Nc}, str(roots))
kappa = 1/(2*Nc)          # normalisation that makes the electron charge -1: Q_em = T3 + kappa*y
qu = sp.Rational(1, 2) + kappa*1
qd = -sp.Rational(1, 2) + kappa*1
qU = kappa*(-1 - Nc)
qD = kappa*(-1 + Nc)
chk("A4c q_u = 1/2 + 1/(2Nc), q_d = q_u - 1, u^c charge = -q_u, d^c charge = -q_d", sp.simplify(qU + qu) == 0 and sp.simplify(qD + qd) == 0 and sp.simplify(qu - qd - 1) == 0)
chk("A4d Nc = 3: q_u = 2/3, q_d = -1/3", qu.subs(Nc, 3) == sp.Rational(2, 3) and qd.subs(Nc, 3) == -sp.Rational(1, 3))
chk("A4e proton charge 2 q_u + q_d = 1 for every N_c (bound state (Nc+1)/2 u,(Nc-1)/2 d)", sp.simplify(((Nc+1)/2)*qu + ((Nc-1)/2)*qd - 1) == 0)
print("      the normalization 'electron = -1' is a CHOICE of unit; anomalies fix q_u/q_e = -(N_c+1)/(2N_c) etc., not the size of e.")

# ---- A5: with nu_R
a = sp.symbols("a0:6")   # yQ yU yD yL yE yN
lin = [2*a[0] + a[1] + a[2], 3*a[0] + a[3], 6*a[0] + 3*a[1] + 3*a[2] + 2*a[3] + a[4] + a[5]]
lin_sol = sp.solve(lin, [a[1], a[3], a[4]], dict=True)[0]      # express in terms of a0 (yQ), a2 (yD), a5 (yN)
sub = {a[1]: lin_sol[a[1]], a[3]: lin_sol[a[3]], a[4]: lin_sol[a[4]]}
cubic = sp.factor(sp.expand(sum(w*(v.subs(sub))**3 for w, v in zip((6, 3, 3, 2, 1, 1), a))))
print("      cubic on the 3-dim linear solution space (params yQ, yD, yN):", cubic)
chk("A5a the cubic is NOT identically zero on the 3-dim linear space (solution variety has dimension exactly 3-1 = 2)", cubic != 0)
Ysm = {"Q": 1, "U": -4, "D": 2, "L": -3, "E": 6, "N": 0}
BL = {"Q": 1, "U": -1, "D": -1, "L": -3, "E": 3, "N": 3}       # (B-L) x 3, left-handed Weyl convention: Q 1/3->1, u^c -1/3->-1, d^c ->-1, L -1 -> -3, e^c +1->3, nu^c +1->3
aa, bb = sp.symbols("aa bb")
comb = {k: aa*Ysm[k] + bb*BL[k] for k in Ysm}
chk("A5b span{Y, B-L} lies inside the solution variety for arbitrary (a,b): a 2-dim family, coupling ratio g_Y/g_{B-L} free", all(sp.simplify(e) == 0 for e in anomaly_eqs(comb, 3)))

nfail = sum(1 for _, ok in checks if not ok)
print(f"\nSUMMARY: {len(checks)-nfail}/{len(checks)} checks pass" + (" [MUTATE]" if MUT else ""))
sys.exit(1 if nfail else 0)
