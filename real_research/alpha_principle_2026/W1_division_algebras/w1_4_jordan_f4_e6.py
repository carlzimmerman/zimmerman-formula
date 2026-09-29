#!/usr/bin/env python3
"""w1_4_jordan_f4_e6 -- exceptional-Jordan-algebra constructions (Todorov-Dubois-Violette arXiv:1806.09450, Krasnov arXiv:1912.11282, Boyle arXiv:2006.16265):
F4 = Aut(J3(O)), E6 = Str(J3(O)); the SM group as an intersection / commutant; charges of the 26 and the 27; hypercharge uniqueness; embedding indices.  Pre-registered J1-J6.

Everything is exact integer / Fraction root-lattice arithmetic (no floating point).  Coordinates: F4 in R^4 (long roots +-e_i+-e_j, short roots +-e_i and (+-1,+-1,+-1,+-1)/2);
E6 in R^5 x R_psi with the metric (l, l') = l.l' + psi psi'/12 (roots: D5 roots at psi = 0, and the 32 spinor weights at psi = +-3).
Run (real):    python3 w1_4_jordan_f4_e6.py          -> exit 0 if every check passes (2 otherwise)
Run (control): python3 w1_4_jordan_f4_e6.py MUTATE   -> identifies colour with the SHORT A2 of F4 instead of the long one; exit 1 if the control bites, 3 if it does not.
"""
import sys
sys.dont_write_bytecode = True
import itertools
from fractions import Fraction as F
import sympy as sp
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import w1_lib as W

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
chk = W.Checks(MUT)
half = F(1, 2)

# ============================================================ F4
def dot(u, v): return sum(a * b for a, b in zip(u, v))
def add(u, v): return tuple(a + b for a, b in zip(u, v))
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def scal(c, u): return tuple(c * a for a in u)
def neg(u): return tuple(-a for a in u)
def refl(beta, alpha): return sub(beta, scal(2 * dot(beta, alpha) / dot(alpha, alpha), alpha))

E = [tuple(F(1) if i == j else F(0) for j in range(4)) for i in range(4)]
long_roots = [tuple(sg1 * (E[i][k]) + sg2 * (E[j][k]) for k in range(4)) for i in range(4) for j in range(i + 1, 4) for sg1 in (1, -1) for sg2 in (1, -1)]
short_roots = [scal(s, E[i]) for i in range(4) for s in (1, -1)] + [tuple(half * s for s in ss) for ss in itertools.product((1, -1), repeat=4)]
long_roots = [tuple(F(x) for x in r) for r in long_roots]
F4 = long_roots + short_roots
Fset = set(F4)
chk("J1a F4: 48 roots (24 long of norm^2 2, 24 short of norm^2 1)", len(F4) == 48 and len(set(F4)) == 48 and sum(1 for r in F4 if dot(r, r) == 2) == 24 and sum(1 for r in F4 if dot(r, r) == 1) == 24)
chk("J1b F4 is closed under all root reflections and 2(a,b)/(b,b) is an integer for all pairs (root system axioms); dim F4 = 48 + rank 4 = 52", all(refl(b, a) in Fset for a in F4 for b in F4) and all((2 * dot(a, b) / dot(b, b)).denominator == 1 for a in F4 for b in F4) and len(F4) + 4 == 52)
w26 = short_roots + [tuple(F(0) for _ in range(4))] * 2
chk("J1c the 26 of F4: weights = the 24 short roots + 2 zero weights, a single Weyl-orbit of minuscule-type weights closed under reflections", len(w26) == 26 and all(refl(w, a) in set(short_roots) | {(F(0),) * 4} for w in w26 for a in F4))

B4 = set(long_roots) | {scal(s, E[i]) for i in range(4) for s in (1, -1)}
# --- J2: all long A2 subsystems, their orthogonal short A2, and the intersection with B4 = Spin(9)
def span_sys(a, b):
    c = add(a, b)
    return frozenset([a, b, c, neg(a), neg(b), neg(c)])
A2long = set()
for a in long_roots:
    for b in long_roots:
        if dot(a, b) == -1:
            A2long.add(span_sys(a, b))
A2long = sorted(A2long, key=lambda s: sorted(s))
def orth(sys_):
    return frozenset(r for r in F4 if all(dot(r, x) == 0 for x in sys_))
stats = {}
ok_short_A2 = True
for A in A2long:
    C = orth(A)
    if len(C) != 6 or any(dot(r, r) != 1 for r in C):
        ok_short_A2 = False
    inter = (set(A) | set(C)) & B4
    nshort = sum(1 for r in inter if dot(r, r) == 1)
    nlong = sum(1 for r in inter if dot(r, r) == 2)
    stats[(nlong, nshort)] = stats.get((nlong, nshort), 0) + 1
chk("J2a every long A2 subsystem of F4 has an orthogonal complement in the root system which is a SHORT A2 (SU(3)_long x SU(3)_short)", ok_short_A2 and len(A2long) > 0, f"{len(A2long)} long A2 subsystems")
print("      J2 intersection (Spin(9) with SU(3)xSU(3)) by (long roots, short roots) : count of long-A2 choices:", stats)
chk("J2b (expectation REFUTED, see amendment 1) for every one of the long-A2 choices the orthogonal short A2 contains exactly one pair +-e_i of B4: the intersection is always A2 + A1 (+ a U(1)) = S(U(2) x U(3)) for every alignment that shares a maximal torus",
    stats == {(6, 2): len(A2long)}, str(stats))
print("      J2 scope: only subsystems sharing the maximal torus are enumerated (the Borel-de Siebenthal setting); non-toral relative positions of the two subgroups are not covered.")

# --- J3: aligned case
colour_long = not MUT
A0 = span_sys(sub(E[0], E[1]), sub(E[1], E[2]))                   # colour A2 (long): e_i - e_j, i,j <= 3
C0 = orth(A0)                                                     # short A2 orthogonal to it
assert A0 in set(A2long) and len(C0) == 6
if colour_long:
    colour, flavour = A0, C0
    su2_root = E[3]                                               # short root +e4 in B4 (the A1 of the intersection)
else:
    colour, flavour = C0, A0                                      # MUTATE: colour = the short A2
    su2_root = sub(E[0], E[1])                                    # a long root of the (now flavour) long A2
# hypercharge direction: orthogonal to colour and su2_root
Mrows = [list(r) for r in colour] + [list(su2_root)]
nullsp = sp.Matrix(Mrows).nullspace()
chk("J3a the centraliser of SU(3)_colour x SU(2) in the Cartan of F4 is ONE-dimensional: the hypercharge direction is unique up to scale", len(nullsp) == 1, f"nullspace dim {len(nullsp)}")
v = nullsp[0]
vY = tuple(F(int(sp.numer(x)), int(sp.denom(x))) for x in (v / max(abs(x) for x in v)))
print("      Y direction (unnormalised):", tuple(str(x) for x in vY))
# colour simple roots
if colour_long:
    a1c, a2c = sub(E[0], E[1]), sub(E[1], E[2])
else:
    # simple roots of the short A2 colour: pick two roots of C0 with dot = -1/2
    pairs = [(a, b) for a in colour for b in colour if dot(a, b) == -half]
    a1c, a2c = pairs[0]
def colour_labels(l):
    p = 2 * dot(l, a1c) / dot(a1c, a1c)
    q = 2 * dot(l, a2c) / dot(a2c, a2c)
    return int(p), int(q)
def dimsu3(p, q): return (p + 1) * (q + 1) * (p + q + 2) // 2
def T3of(l): return dot(l, su2_root) / dot(su2_root, su2_root)
# hypercharge scale: demand a neutral component in a colour-singlet isodoublet
def ysum(l): return dot(l, vY)
lept = [l for l in w26 if colour_labels(l) == (0, 0) and abs(T3of(l)) == half and ysum(l) != 0]
cands = set()
for l in lept:
    cands.add(-T3of(l) / ysum(l))
print("      scale c in Y = c (l . vY) which makes a lepton-doublet component neutral:", sorted(str(c) for c in cands))
chk("J3b the neutral-lepton requirement fixes |c| uniquely (the two signs are the charge-conjugate choice)", len(cands) > 0 and len({abs(x) for x in cands}) == 1, str(sorted(str(c) for c in cands)))
c_ = max(cands) if cands else F(1)
Y = lambda l: c_ * ysum(l)
Qch = lambda l: T3of(l) + Y(l)
def tri(l):
    p, q = colour_labels(l)
    return (p - q) % 3
def su2_peel(t3list):
    ts = sorted(t3list, reverse=True)
    out = []
    while ts:
        top = ts[0]
        for k in range(int(2 * top) + 1):
            ts.remove(top - k)
        out.append(int(2 * top) + 1)
    return sorted(out)
groups = {}
for l in w26:
    groups.setdefault((tri(l), Y(l)), []).append(T3of(l))
mult = []
for (t, y), t3s in groups.items():
    cd = 1 if t == 0 else 3
    per = []
    for x in sorted(set(t3s)):
        assert t3s.count(x) % cd == 0
        per += [x] * (t3s.count(x) // cd)
    for d in su2_peel(per):
        mult.append((cd, t, d, y))
mult.sort(key=lambda z: (z[1], z[2], z[3], z[0]))
print("      the 26 under SU(3) x SU(2) x U(1): (colour dim, triality, isospin dim, Y)")
for m_ in mult:
    print("       ", m_[0], "t=" + str(m_[1]), "iso", m_[2], "Y =", m_[3])
ref_abs = sorted([(3, 2, F(1, 6)), (3, 2, F(1, 6)), (3, 1, F(1, 3)), (3, 1, F(1, 3)), (1, 2, F(1, 2)), (1, 2, F(1, 2)), (1, 3, F(0)), (1, 1, F(0))])
got_abs = sorted((cd, d, abs(y)) for (cd, t, d, y) in mult)
okz = all((round(6 * y) - (d - 1)) % 2 == 0 for (cd, t, d, y) in mult)
ok3 = any(all((round(6 * y) - sg * t) % 3 == 0 for (cd, t, d, y) in mult) for sg in (1, -1))
chk("J3c the 26 decomposes as (3,2)_{1/6} + (3bar,2)_{-1/6} + (3,1)_{-1/3} + (3bar,1)_{+1/3} + (1,2)_{+-1/2} + (1,3)_0 + (1,1)_0: |Y| = 1/6 : 1/3 : 1/2 for quark doublet : quark singlet : lepton doublet, 6Y = isospin parity (mod 2) and 6Y = +-triality (mod 3, one universal sign)", got_abs == ref_abs and okz and ok3, str(got_abs))
# charges
qs = sorted(Qch(l) for l in w26)
print("      charges of the 26:", [str(q) for q in qs])
# vector-like: closed under l -> -l
chk("J3d the 26 is real: the weight multiset is symmetric under l -> -l, so it carries no gauge anomaly and NO chirality by itself (a chiral generation needs a further ingredient)", sorted(w26) == sorted(neg(l) for l in w26))
ch_triplet = [Qch(l) for l in w26 if colour_labels(l) == (0, 0) and abs(T3of(l)) == 1]
chk("J3e the 26 contains, besides quark- and lepton-like states, a colour-singlet ISOSPIN TRIPLET with charges +1, 0, -1 (a charged vector-like state with no SM partner)", sorted(ch_triplet) == [F(-1), F(1)], str([str(x) for x in ch_triplet]))
# Krasnov Spin(9): lepton / quark doublet charge ratio
lep_dbl = {Y(l) for l in w26 if colour_labels(l) == (0, 0) and abs(T3of(l)) == half}
qk_dbl = {Y(l) for l in w26 if colour_labels(l) != (0, 0) and abs(T3of(l)) == half}
sp9 = [l for l in w26 if all(abs(x) == half for x in l)]              # the 16 of Spin(9) inside the 26 (spinor weights)
ratio = {abs(y) / min(abs(z) for z in qk_dbl) for y in lep_dbl} if (qk_dbl and lep_dbl and all(z != 0 for z in qk_dbl)) else set()
chk("J6 Krasnov: on the 16 of Spin(9) (spinor weights) the doublets have hypercharges (3,2)_{1/6}, (1,2)_{-1/2}: ratio lepton : quark = N_c = 3 (traceless U(1) in SU(4) = diag(-3,1,1,1))", len(sp9) == 16 and ratio == {F(3)}, f"ratio {ratio}")
# ---- J5: embedding indices
def norm2_of_functional(fn_vec): return dot(fn_vec, fn_vec)
vT3 = scal(1 / dot(su2_root, su2_root), su2_root)                   # T3 = (l . alpha)/(alpha.alpha)
vc = scal(1 / dot(a1c, a1c), a1c)                                    # colour T3c
vYn = scal(c_, vY)
vQ = add(vT3, vYn)
alpha_over_G = lambda v_: 1 / (2 * dot(v_, v_))
a3, a2, aY, aem = alpha_over_G(vc), alpha_over_G(vT3), alpha_over_G(vYn), alpha_over_G(vQ)
sin2 = aY / (aY + a2)
print(f"      alpha_3 : alpha_2 : alpha_Y : alpha_em (in units of alpha_G) = {a3} : {a2} : {aY} : {aem};  sin^2 theta_W = {sin2}")
chk("J5a F4 with colour = long A2, SU(2) = short root: alpha_3 : alpha_2 : alpha_Y = 1 : 1/2 : 3/2 (embedding indices 1, 2, ..), sin^2 theta_W = 3/4, alpha_em = (3/8) alpha_G",
    (a3, a2, aY, sin2, aem) == (F(1), F(1, 2), F(3, 2), F(3, 4), F(3, 8)), f"{(str(a3), str(a2), str(aY), str(sin2), str(aem))}")

# ============================================================ E6
psi_norm = F(1, 12)
def mdot(u, v): return sum(a * b for a, b in zip(u[:5], v[:5])) + u[5] * v[5] * psi_norm
def mrefl(b, a):
    k = 2 * mdot(b, a) / mdot(a, a)
    return tuple(x - k * y for x, y in zip(b, a))
E5 = [tuple(F(1) if i == j else F(0) for j in range(5)) for i in range(5)]
d5 = []
for i in range(5):
    for j in range(i + 1, 5):
        for s1 in (1, -1):
            for s2 in (1, -1):
                r = [F(0)] * 6
                r[i], r[j] = F(s1), F(s2)
                d5.append(tuple(r))
sp16 = []
for ss in itertools.product((1, -1), repeat=5):
    nm = sum(1 for x in ss if x < 0)
    r = tuple(half * x for x in ss)
    sp16.append((r, nm % 2))
E6r = list(d5)
for r, par in sp16:
    E6r.append(r + (F(-3) if par == 0 else F(3),))
E6set = set(E6r)
chk("J1d E6: 72 roots (40 of D5 at psi = 0, 16 at psi = -3, 16bar at psi = +3), all of norm^2 2 in the metric l.l' + psi psi'/12", len(E6r) == 72 and len(E6set) == 72 and all(mdot(r, r) == 2 for r in E6r))
chk("J1e E6 root system axioms (closed under reflections, integrality) and dim E6 = 72 + 6 = 78", all(mrefl(b, a) in E6set for a in E6r for b in E6r) and all((2 * mdot(a, b) / mdot(b, b)).denominator == 1 for a in E6r for b in E6r) and len(E6r) + 6 == 78)
w27 = [tuple([F(0)] * 5 + [F(4)])] + [tuple(scal(s, e)) + (F(-2),) for e in E5 for s in (1, -1)] + [r + (F(1),) for r, par in sp16 if par == 0]
chk("J1f the 27 of E6 (1_4 + 10_-2 + 16_1): 27 weights, all of norm^2 4/3, minuscule ((w, root) in {-1,0,1}), closed under reflections", len(w27) == 27 and all(mdot(w, w) == F(4, 3) for w in w27) and all(mdot(w, a) in (-1, 0, 1) for w in w27 for a in E6r) and all(mrefl(w, a) in set(w27) for w in w27 for a in E6r))
# SM subalgebra inside E6: colour A2 = e_i - e_j (i,j<=3), su2 = e4 - e5
col_roots = [tuple(F(1) if k == i else (F(-1) if k == j else F(0)) for k in range(6)) for i in range(3) for j in range(3) if i != j]
su2r = tuple(F(1) if k == 3 else (F(-1) if k == 4 else F(0)) for k in range(6))
assert all(r in E6set for r in col_roots) and su2r in E6set
Mrows = [[a * (psi_norm if k == 5 else 1) for k, a in enumerate(r)] for r in col_roots + [su2r]]
null6 = sp.Matrix(Mrows).nullspace()
chk("J4a the centraliser of SU(3)_c x SU(2)_L in the Cartan of E6 is THREE-dimensional (hypercharge NOT unique in E6): U(1)_(123), U(1)_(45), U(1)_psi", len(null6) == 3, f"nullspace dim {len(null6)}")
# 16-multiplet analysis: Y = x1 (l1+l2+l3) + x2 (l4+l5) + x3 psi on the 16 (psi = 1)
sixteen = [w for w in w27 if w[5] == 1]
def cl_e6(l):
    a1, a2 = (1, -1, 0), (0, 1, -1)
    p = int(l[0] - l[1]); q = int(l[1] - l[2])
    return p, q
def T3e(l): return (l[3] - l[4]) / 2
# SM target multiset (colour class dim, isospin dim, Y) with both colour orientations
SMt = sorted([(3, 2, F(1, 6))] * 6 + [(3, 1, F(-2, 3))] * 3 + [(3, 1, F(1, 3))] * 3 + [(1, 2, F(-1, 2))] * 2 + [(1, 1, F(1))] + [(1, 1, F(0))])
# isospin dims of each state: doublet iff |l4 - l5| = 1
def iso_dim(l): return 2 if abs(l[3] - l[4]) == 1 else 1
def col_dim(l):
    p, q = cl_e6(l)
    return 1 if (p, q) == (0, 0) else 3
sols = []
grid = [F(k, 12) for k in range(-24, 25)]
sixt = [(col_dim(w), iso_dim(w), w[0] + w[1] + w[2], w[3] + w[4], (cl_e6(w)[0] - cl_e6(w)[1]) % 3) for w in sixteen]
def z6_ok(x1, x2):
    ys = [(cd, idm, x1 * y1 + x2 * y2, t) for (cd, idm, y1, y2, t) in sixt]
    ok2 = all((round(6 * y) - (idm - 1)) % 2 == 0 for (cd, idm, y, t) in ys)
    ok3 = any(all((round(6 * y) - sg * t) % 3 == 0 for (cd, idm, y, t) in ys) for sg in (1, -1))
    return ok2 and ok3
sols_multiset_only = []
for x1 in grid:
    for x2 in grid:
        vals = sorted((cd, idm, x1 * y1 + x2 * y2) for (cd, idm, y1, y2, t) in sixt)
        if vals == SMt or vals == sorted((cd, idm, -y) for (cd, idm, y) in SMt):
            sols_multiset_only.append((x1, x2))
            if z6_ok(x1, x2):
                sols.append((x1, x2))
print("      (x1, x2) with x3 = 0 reproducing the SM hypercharge multiset on the 16 (grid 1/12), multiset only:", [(str(a), str(b)) for a, b in sols_multiset_only])
print("      ... and also satisfying the Z6 correlation (6Y = isospin parity mod 2, 6Y = +-triality mod 3):", [(str(a), str(b)) for a, b in sols])
sum_y_zero = sum(t[2] for t in sixt) == 0 and sum(t[3] for t in sixt) == 0
def charge_multiset(a, b):
    Yf = lambda l: a * (l[0] + l[1] + l[2]) + b * (l[3] + l[4])
    return sorted(T3e(l) + Yf(l) for l in w27)
same_charges = all(charge_multiset(*sl) == charge_multiset(*sols[0]) or charge_multiset(*sl) == sorted(-q for q in charge_multiset(*sols[0])) for sl in sols)
chk("J4b demanding the SM hypercharges (with the Z6 correlation) on a 16 fixes |x1| = 1/3, |x2| = 1/2 and forces x3 = 0 (the 16 has zero mean of Y and psi = 1 is constant); the 4 sign choices are the overall charge conjugation and the u^c <-> d^c swap (lane G's branches) and give the same charge spectrum on the whole 27",
    len(sols) == 4 and all(abs(a) == F(1, 3) and abs(b) == half for a, b in sols) and sum_y_zero and same_charges, f"{len(sols)} solutions, traceless {sum_y_zero}, same charge multiset {same_charges}")
x1, x2 = sols[0] if sols[0][0] > 0 else sols[1]
vYe = (x1, x1, x1, x2, x2, F(0))                                    # as a covector on weights; the Cartan vector has psi component 12 x3 = 0
vT3e = (F(0), F(0), F(0), half, -half, F(0))
vce = (half, -half, F(0), F(0), F(0), F(0))
a2e = alpha_over_G(vT3e); aYe = alpha_over_G(vYe); a3e = alpha_over_G(vce)
sin2e = aYe / (aYe + a2e)
aeme = alpha_over_G(add(vT3e, vYe))
print(f"      E6 (SM charges on the 16): x1 = {x1}, x2 = {x2}; alpha_3 : alpha_2 : alpha_Y : alpha_em = {a3e} : {a2e} : {aYe} : {aeme}; sin^2 = {sin2e}")
chk("J4c with the SM charges imposed on the 16 the E6 (= Spin(10)) embedding gives sin^2 theta_W = 3/8 and alpha_em = (3/8) alpha_G (alpha_3 = alpha_2 = alpha_G)", (a3e, a2e, sin2e, aeme) == (F(1), F(1), F(3, 8), F(3, 8)), f"{(str(a3e), str(a2e), str(sin2e), str(aeme))}")
# the free family: sin^2 as a function of the U(1) direction (unconstrained by the SM charge requirement)
y1s, y2s, y3s = sp.symbols("y1 y2 y3", real=True)
vfam = (y1s, y1s, y1s, y2s, y2s, 12 * y3s)
nY = 3 * y1s ** 2 + 2 * y2s ** 2 + (12 * y3s) ** 2 * sp.Rational(1, 12)
sinfam = sp.simplify((1 / (2 * nY)) / ((1 / (2 * nY)) + sp.Rational(1, 1)))
print("      E6 family: sin^2 theta_W(y1,y2,y3) =", sinfam, "-- takes every value in (0,1) as the direction varies")
chk("J4d over the 3-dim commutant the sin^2 theta_W is NOT fixed by E6 (it is an unconstrained function of the U(1) direction; 3/8 is a point selected by the SM charges of the 16)", sinfam.has(y1s) and sinfam.has(y3s))
# 27 content at the SM direction
Ye = lambda l: x1 * (l[0] + l[1] + l[2]) + x2 * (l[3] + l[4])
def tri6(l): return (cl_e6(l)[0] - cl_e6(l)[1]) % 3
g27 = {}
for l in w27:
    g27.setdefault((tri6(l), Ye(l), l[5]), []).append(T3e(l))
print("      the 27 at the SM direction: (psi, colour dim, triality, isospin dim, Y)")
mult27 = []
for (t, y, psi), t3s in sorted(g27.items(), key=lambda z: (z[0][2], z[0][0], z[0][1])):
    cd = 1 if t == 0 else 3
    per = []
    for x in sorted(set(t3s)):
        assert t3s.count(x) % cd == 0
        per += [x] * (t3s.count(x) // cd)
    for d in su2_peel(per):
        mult27.append((psi, cd, t, d, y))
for m_ in mult27:
    print("       psi =", m_[0], " colour dim", m_[1], " t =", m_[2], " isospin dim", m_[3], " Y =", m_[4])
exotic_abs = sorted((cd, d, abs(y)) for (psi, cd, t, d, y) in mult27 if psi != 1)
chk("J4e the 27 = 16 + 10 + 1: besides the 16 (one SM generation incl. nu_R) it contains (3,1)_{-1/3} + (3bar,1)_{+1/3} + (1,2)_{+1/2} + (1,2)_{-1/2} + (1,1)_0, i.e. 11 states NOT in the SM, 8 of them electrically charged", exotic_abs == sorted([(3, 1, F(1, 3)), (3, 1, F(1, 3)), (1, 2, F(1, 2)), (1, 2, F(1, 2)), (1, 1, F(0))]) and sum(1 for l in w27 if l[5] != 1) == 11 and sum(1 for l in w27 if l[5] != 1 and T3e(l) + Ye(l) != 0) == 8, str(exotic_abs))
def anomaly_sums(mults):
    """mults: list of (colour dim, isospin dim, Y) LEFT-handed Weyl multiplets.  Returns the four anomaly polynomials SU(3)^2Y, SU(2)^2Y, grav^2 Y, Y^3."""
    return (sum(d * y for cd, d, y in mults if cd == 3), sum(cd * y for cd, d, y in mults if d == 2), sum(cd * d * y for cd, d, y in mults), sum(cd * d * y ** 3 for cd, d, y in mults))
m16 = [(cd, d, y) for (psi, cd, t, d, y) in mult27 if psi == 1]
m10 = [(cd, d, y) for (psi, cd, t, d, y) in mult27 if psi == -2]
m1 = [(cd, d, y) for (psi, cd, t, d, y) in mult27 if psi == 4]
m26 = [(cd, d, y) for (cd, t, d, y) in mult]
chk("J4f the E6 27 at the SM direction: the 16 alone is anomaly-free (all four polynomials vanish -- it is the anomaly-free SM generation with nu_R), the 10 and the 1 are separately vector-like anomaly-free; the F4 26 is real, hence anomaly-free with NO chirality",
    anomaly_sums(m16) == (0, 0, 0, 0) and anomaly_sums(m10) == (0, 0, 0, 0) and anomaly_sums(m1) == (0, 0, 0, 0) and anomaly_sums(m26) == (0, 0, 0, 0), str((anomaly_sums(m16), anomaly_sums(m10), anomaly_sums(m26))))
print("      J verdict: F4/E6 fix hypercharge RATIOS inside a representation (F4 uniquely; E6 only after matching the SM charges) and the colour/isospin index ratios (sin^2 = 3/4 for F4, 3/8 for E6); the coupling alpha_G stays free.")
chk.finish("w1_4")
