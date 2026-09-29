#!/usr/bin/env python3
"""w1_3_dixon_fh -- Furey-Hughes (arXiv:2209.13016, 2210.10126): the Dixon algebra A = C x H x O (32 complex dimensions) as ONE generation with spin(10), g_sm, Y, Q, B-L.
Pre-registered F1-F6.  32 x 32 identities are checked in numpy complex128 (all entries are dyadic rationals or multiples of 1/sqrt3; tolerance 1e-12 printed);
lattice / anomaly statements are exact sympy.
Run (real):    python3 w1_3_dixon_fh.py          -> exit 0 if every check passes (2 otherwise)
Run (control): python3 w1_3_dixon_fh.py MUTATE   -> replaces s* by s in the hypercharge (a wrong idempotent); exit 1 if the control bites, 3 if it does not.
"""
import sys
sys.dont_write_bytecode = True
import itertools
import numpy as np
import sympy as sp
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import w1_lib as W

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
chk = W.Checks(MUT)
TOL = 1e-12
np.seterr(all="ignore")          # numpy 1.26 + macOS Accelerate emits spurious FP warnings in complex matmul; sanity-checked against einsum below
from fractions import Fraction
def rat(x):
    r = Fraction(float(x)).limit_denominator(48)
    assert abs(float(r) - float(x)) < 1e-8, (x, r)
    return sp.Rational(r.numerator, r.denominator)
_rng = np.random.default_rng(1)
_A = _rng.standard_normal((32, 32)) + 1j * _rng.standard_normal((32, 32))
_B = _rng.standard_normal((32, 32)) + 1j * _rng.standard_normal((32, 32))
chk("F0 matmul sanity: A @ B agrees with an einsum product to 1e-12 on random complex 32x32 matrices (guards against the spurious BLAS warnings being real)", np.max(np.abs(_A @ _B - np.einsum("ij,jk->ik", _A, _B))) < 1e-12)
c1 = 1j

# ------------------------------------------------------------------ the algebra A = C x H x O acting on itself (index mu*8 + nu)
LH, RH = W.quat_left_np()
LO = W.oct_left_np()
I4, I8, I32 = np.eye(4), np.eye(8), np.eye(32)
def LHq(a): return np.kron(LH[a], I8)            # left multiplication by eps_a (a=1..3)
def LOe(a): return np.kron(I4, LO[a])            # left multiplication by e_a (a=1..7)
def com(A, B): return A @ B - B @ A
def nrm(M): return float(np.max(np.abs(M)))

# generalised Pauli matrices, eq (10)
sig = {}
for j in range(1, 8):
    sig[j] = -(np.kron(LH[2], LO[j]))            # -(e_j eps_2 | 1)
sig[8] = -c1 * LHq(1)
sig[9] = -c1 * LHq(3)
sig[10] = -c1 * I32
sigbar = {c: (-sig[c] if c <= 9 else sig[c]) for c in sig}
def J(a, b):                                       # (1/2) sigma_[a sigma-bar_b]
    return 0.25 * (sig[a] @ sigbar[b] - sig[b] @ sigbar[a])
pairs = [(a, b) for a in range(1, 11) for b in range(a + 1, 11)]
Jg = {p: J(*p) for p in pairs}
def Jf(a, b):
    if a == b: return np.zeros((32, 32), complex)
    return Jg[(a, b)] if a < b else -Jg[(b, a)]

# ---------------- F1: so(10)
def so_dev(sign):
    dev = 0.0
    for (a, b) in pairs:
        for (c, d) in pairs:
            lhs = com(sign * Jf(a, b), sign * Jf(c, d))
            rhs = np.zeros((32, 32), complex)
            if b == c: rhs += sign * Jf(a, d)
            if a == c: rhs -= sign * Jf(b, d)
            if b == d: rhs -= sign * Jf(a, c)
            if a == d: rhs += sign * Jf(b, c)
            dev = max(dev, nrm(lhs - rhs))
    return dev
devs = {s: so_dev(s) for s in (+1, -1)}
best = min(devs, key=devs.get)
chk("F1a the 45 operators (1/2) sigma_[a sigma-bar_b] close into so(10): [K_ab,K_cd] = d_bc K_ad - d_ac K_bd - d_bd K_ac + d_ad K_bc for K = " + ("+J" if best == 1 else "-J"),
    devs[best] < TOL, f"(max deviation {devs[best]:.1e}; for the other sign {devs[-best]:.1e})")
# commutant dimension
rows = []
for p in pairs:
    Mx = Jg[p]
    rows.append(np.kron(Mx, I32) - np.kron(I32, Mx.T))
big = np.vstack(rows)
sv = np.linalg.svd(big, compute_uv=False)
dim_comm = int(np.sum(sv < 1e-9)) + max(0, 1024 - len(sv))
chk("F1b the commutant of so(10) in End(A) has complex dimension 4 (= 1 + right multiplication by C x H = sl(2,C) + 1 => 16 + 16, not 16 + 16*: End = M_2(C))", dim_comm == 4, f"nullity {dim_comm}")
# Cartan weights and chirality parity
Hc = [1j * Jf(2 * k - 1, 2 * k) for k in range(1, 6)]
chk("F1c the five operators i J_{2k-1,2k} commute (Cartan subalgebra of so(10))", all(nrm(com(Hc[i], Hc[j])) < TOL for i in range(5) for j in range(5)))
cvec = np.array([1.0, np.sqrt(2), np.sqrt(3), np.sqrt(5), np.sqrt(7)])
Mgen = sum(c * H for c, H in zip(cvec, Hc))
w, V = np.linalg.eigh((Mgen + Mgen.conj().T) / 2)
weights = []
for kcol in range(32):
    v = V[:, kcol]
    weights.append(tuple(round(float(np.real(v.conj() @ H @ v)) * 2) / 2 for H in Hc))
uw = sorted(set(weights))
parities = {sum(1 for x in wv if x < 0) % 2 for wv in uw}
chk("F1d the 32 weights are the 16 spinor weights (+-1/2)^5 of ONE chirality, each twice (16 + 16)", len(uw) == 16 and len(parities) == 1 and all(weights.count(wv) == 2 for wv in uw),
    f"distinct weights {len(uw)}, parity of minus signs {parities}")

# ---------------- SM generators
def e2(a, b): return LOe(a) @ LOe(b)
sqrt3 = np.sqrt(3.0)
iLam = {1: 0.5 * (e2(3, 4) - e2(1, 5)), 2: 0.5 * (e2(1, 4) + e2(3, 5)), 3: 0.5 * (e2(1, 3) - e2(4, 5)), 4: -0.5 * (e2(2, 5) + e2(4, 6)),
        5: 0.5 * (e2(2, 4) - e2(5, 6)), 6: -0.5 * (e2(1, 6) + e2(2, 3)), 7: -0.5 * (e2(1, 2) + e2(3, 6)), 8: -(1 / (2 * sqrt3)) * (e2(1, 3) + e2(4, 5) - 2 * e2(2, 6))}
Lam = {j: -c1 * iLam[j] for j in iLam}              # hermitian
s_ = 0.5 * (I32 + c1 * LOe(7))                      # s   = (1 + i e7)/2 (left multiplication)
sstar = 0.5 * (I32 - c1 * LOe(7))
if MUT:
    sY = s_                                          # MUTATE: the wrong idempotent in Y
else:
    sY = sstar
X = e2(1, 3) + e2(2, 6) + e2(4, 5)
tau = {k: (c1 / 2) * s_ @ LHq(k - 8) for k in (9, 10, 11)}     # tau_k = (i/2) s eps
T3L = (c1 / 2) * s_ @ LHq(3)                                    # hermitian T3 of su(2)_L
T3R = (c1 / 2) * sstar @ LHq(3)
Yop = -(c1 / 6) * X + (c1 / 2) * sY @ LHq(3)                    # eq (20)
Qop = -(c1 / 6) * X + (c1 / 2) * LHq(3)                         # eq (26)
BLop = -(c1 / 3) * X                                            # eq (22)
for nm, M in (("T3L", T3L), ("T3R", T3R), ("Y", Yop), ("Q", Qop), ("B-L", BLop)):
    assert nrm(M - M.conj().T) < TOL, nm + " not hermitian"
gens_sm = [iLam[j] for j in range(1, 9)] + [1j * tau[k] for k in (9, 10, 11)] + [1j * Yop]
G = np.array([np.concatenate([g.real.ravel(), g.imag.ravel()]) for g in gens_sm])
Jvec = np.array([np.concatenate([Jg[p].real.ravel(), Jg[p].imag.ravel()]) for p in pairs])
coef, res, rk, _ = np.linalg.lstsq(Jvec.T, G.T, rcond=None)
resid = np.max(np.abs(Jvec.T @ coef - G.T))
chk("F1e the 12 generators of g_sm (eqs 15,17,19) lie in the real span of the 45 so(10) generators", resid < 1e-10, f"(residual {resid:.1e})")
sc = np.array([[np.real(np.trace(Lam[i] @ Lam[j])) for j in range(1, 9)] for i in range(1, 9)])
ok_su3 = True
fs = {}
def setf(i, j, k, v):
    for (a, b, c), s in (((i, j, k), 1), ((j, k, i), 1), ((k, i, j), 1), ((j, i, k), -1), ((i, k, j), -1), ((k, j, i), -1)):
        fs[(a, b, c)] = s * v
for (i, j, k, v) in ((1, 2, 3, 1), (1, 4, 7, .5), (1, 5, 6, -.5), (2, 4, 6, .5), (2, 5, 7, .5), (3, 4, 5, .5), (3, 6, 7, -.5), (4, 5, 8, sqrt3 / 2), (6, 7, 8, sqrt3 / 2)):
    setf(i, j, k, v)
dev_f = 0.0
for i in range(1, 9):
    for j in range(1, 9):
        lhs = com(Lam[i] / 2, Lam[j] / 2)
        rhs = sum(1j * fs.get((i, j, k), 0) * Lam[k] / 2 for k in range(1, 9))
        dev_f = max(dev_f, nrm(lhs - rhs))
chk("F1f the colour generators of eq (16) close as su(3): [L_i/2, L_j/2] = i f_ijk L_k/2 (standard f_ijk)", dev_f < TOL, f"(max deviation {dev_f:.1e})")
tk = {k: (c1 / 2) * s_ @ LHq(k - 8) for k in (9, 10, 11)}
dev_su2 = max(nrm(com(tk[9], tk[10]) - 1j * tk[11]), nrm(com(tk[10], tk[11]) - 1j * tk[9]), nrm(com(tk[11], tk[9]) - 1j * tk[10]))
chk("F1g su(2)_L: T_k = (i/2) s eps_k obey [T_9,T_10] = i T_11 (cyclic) -- weak isospin with s a projector", dev_su2 < TOL, f"(deviation {dev_su2:.1e})")
chk("F1h g_su(3) and g_su(2)_L and Y commute with each other (direct sum): all cross commutators vanish",
    max(nrm(com(iLam[j], tau[k])) for j in iLam for k in tau) < TOL and max(nrm(com(iLam[j], Yop)) for j in iLam) < TOL and max(nrm(com(tau[k], Yop)) for k in tau) < TOL)
chk("F2a Q = T3L + Y as operators (eqs 20, 26)", nrm(Qop - T3L - Yop) < TOL, f"(deviation {nrm(Qop - T3L - Yop):.1e})")

# ---------------- F2: the 32 states of eq (30)
Hq = {"uu": [.5, 0, 0, .5j], "ud": [0, .5j, -.5, 0], "du": [0, .5j, .5, 0], "dd": [.5, 0, 0, -.5j]}
def ovec(d):
    v = np.zeros(8, complex)
    for k, x in d.items(): v[k] = x
    return v
Ov = {"l": ovec({0: .5, 7: .5j}), "l*": ovec({0: .5, 7: -.5j}),
      "q1": ovec({5: -.5, 4: .5j}), "q2": ovec({3: -.5, 1: .5j}), "q3": ovec({6: -.5, 2: .5j}),
      "q1*": ovec({5: -.5, 4: -.5j}), "q2*": ovec({3: -.5, 1: -.5j}), "q3*": ovec({6: -.5, 2: -.5j})}
def state(h, o): return np.kron(np.array(Hq[h], complex), Ov[o])
def lab(h, o):
    iso = {"uu": "up", "ud": "up", "du": "dn", "dd": "dn"}[h]
    if o == "l": return "V_L" if iso == "up" else "E_L"
    if o == "l*": return "E_R*" if iso == "up" else "V_R*"
    if o.startswith("q") and not o.endswith("*"): return "U_L" if iso == "up" else "D_L"
    return "D_R*" if iso == "up" else "U_R*"
SM = {"V_L": (.5, -.5, 0, -1), "E_L": (-.5, -.5, -1, -1), "E_R*": (0, 1, 1, 1), "V_R*": (0, 0, 0, 1),
      "U_L": (.5, 1 / 6, 2 / 3, 1 / 3), "D_L": (-.5, 1 / 6, -1 / 3, 1 / 3), "U_R*": (0, -2 / 3, -2 / 3, -1 / 3), "D_R*": (0, 1 / 3, 1 / 3, -1 / 3)}
def ev(M, v):
    lam = (v.conj() @ M @ v) / (v.conj() @ v)
    return lam, float(np.max(np.abs(M @ v - lam * v)))
C2 = sum((Lam[i] / 2) @ (Lam[i] / 2) for i in range(1, 9))
T8 = Lam[8] / 2
rows_tab = []
max_res = 0.0
allok = True
for h in Hq:
    for o in Ov:
        v = state(h, o)
        v = v / np.linalg.norm(v)
        vals = []
        for M in (T3L, Yop, Qop, BLop, C2, T8, Lam[3] / 2):
            lam, r = ev(M, v)
            max_res = max(max_res, r)
            vals.append(float(np.real(lam)))
        rows_tab.append((h, o, lab(h, o), vals))
chk("F2b all 32 basis states (eq 28-30) are simultaneous eigenvectors of T3L, Y, Q, B-L, colour Casimir, T8, T3c", max_res < 1e-10, f"(max residual {max_res:.1e})")
bad = []
for (h, o, l, vals) in rows_tab:
    exp = SM[l]
    got = tuple(vals[:4])
    if any(abs(a - b) > 1e-9 for a, b in zip(got, exp)):
        bad.append((l, h, o, got, exp))
chk("F2c (T3, Y, Q, B-L) of each of the 32 states equals the SM assignment of its label (V_L,E_L,U_L,D_L, and the conjugates of E_R,V_R,U_R,D_R)", not bad,
    "" if not bad else "first mismatches: " + str(bad[:3]))
print("      table: label, epsilon, octonion, (T3L, Y, Q, B-L, C2colour, T8, T3c)")
for (h, o, l, vals) in rows_tab:
    if o in ("l", "l*", "q1", "q1*"):
        print("       ", l.ljust(5), h, o.ljust(3), [round(x, 4) for x in vals])
# colour reps
def colour_rep(c2, t8s):
    if abs(c2) < 1e-9: return 0
    if abs(c2 - 4 / 3) < 1e-9:
        t = sorted(round(x, 6) for x in t8s)
        three = sorted(round(x, 6) for x in (1 / (2 * sqrt3), 1 / (2 * sqrt3), -1 / sqrt3))
        threebar = sorted(round(x, 6) for x in (-1 / (2 * sqrt3), -1 / (2 * sqrt3), 1 / sqrt3))
        return 1 if t == three else (-1 if t == threebar else None)
    return None
tri = {}
for l in SM:
    tb = None
    trip = [r for r in rows_tab if r[2] == l]
    # group the three colours (o = q1,q2,q3 or q1*,q2*,q3*) for a fixed epsilon
    if l in ("U_L", "D_L", "U_R*", "D_R*"):
        hset = {r[0] for r in trip}
        h0 = sorted(hset)[0]
        sub = [r for r in trip if r[0] == h0]
        tri[l] = colour_rep(sub[0][3][4], [r[3][5] for r in sub])
    else:
        tri[l] = colour_rep(trip[0][3][4], [trip[0][3][5]])
chk("F2d colour: leptons singlets, U_L,D_L in one triplet class t, U_R*, D_R* in the conjugate class -t", tri["V_L"] == tri["E_L"] == tri["E_R*"] == tri["V_R*"] == 0 and tri["U_L"] == tri["D_L"] == -tri["U_R*"] == -tri["D_R*"] and tri["U_L"] in (1, -1), str(tri))
sgn = tri["U_L"]                                   # +1 if the LH quark doublet is a 3 under these generators
y6 = {l: round(6 * SM[l][1]) for l in SM}
t2 = {l: (1 if l in ("V_L", "E_L", "U_L", "D_L") else 0) for l in SM}
ok2 = all((y6[l] - t2[l]) % 2 == 0 for l in SM)
ok3 = all(((y6[l] - sgn * tri[l]) % 3 == 0) for l in SM)
chk("F2e the Z6 quotient: 6Y = isospin-doublet (mod 2) and 6Y = +-triality (mod 3, one universal sign) on every state (so charge is quantised in units 1/6 of Y, 1/3 of Q)", ok2 and ok3, f"6Y = {y6}, universal sign {sgn}")

# ---------------- F3: complex-conjugation invariance
def fixed_dim(gens):
    Gm = np.array([g.imag.ravel() for g in gens])          # need sum c_k Im(g_k) = 0
    sv_ = np.linalg.svd(Gm, compute_uv=False)
    return len(gens) - int(np.sum(sv_ > 1e-10))
d_sm = fixed_dim(gens_sm)
d_so10 = fixed_dim([Jg[p] for p in pairs])
chk("F3a complex conjugation (entrywise in the basis eps_mu e_nu) fixes a 9-dimensional subalgebra of g_sm (12-dim)", d_sm == 9, f"dim {d_sm}")
chk("F3b the same conjugation fixes a 24-dimensional subalgebra of the whole so(10)_A (sigma_1..7 real, sigma_8..10 imaginary => so(7) + so(3))", d_so10 == 24, f"dim {d_so10}")
# is the fixed part of g_sm exactly su(3) + u(1)_Q ?
Gm = np.array([g.imag.ravel() for g in gens_sm])
u, s_v, vh = np.linalg.svd(Gm.T, full_matrices=True)
null = vh[np.sum(s_v > 1e-10):]
fixed_gen = [sum(c * g for c, g in zip(row, gens_sm)) for row in null]
def in_span(M, basis):
    Bm = np.array([np.concatenate([b.real.ravel(), b.imag.ravel()]) for b in basis])
    m = np.concatenate([M.real.ravel(), M.imag.ravel()])
    cf = np.linalg.lstsq(Bm.T, m, rcond=None)[0]
    return np.max(np.abs(Bm.T @ cf - m)) < 1e-9
target = [iLam[j] for j in range(1, 9)] + [1j * Qop]
chk("F3c that 9-dim fixed subalgebra is exactly su(3)_c + u(1)_Q (i Q = e13+e26+e45 over 6 - eps_3/2 is real)", all(in_span(g, target) for g in fixed_gen) and len(fixed_gen) == 9)
print("      F3 verdict: conjugation invariance picks su(3) + u(1)_Q OUT OF g_sm; it does not pick g_sm out of so(10) (fixed part of so(10) has dim 24).")

# ---------------- F4: what is fixed inside the Cartan plane span{T3R, B-L}
a_, b_, c_ = sp.symbols("a b c", real=True)
# multiplet table: for each distinct SM multiplet take T3L, T3R, B-L eigenvalues on a representative state
def ev_real(M, v): return round(float(np.real(ev(M, v / np.linalg.norm(v))[0])), 9)
T3Rv, BLv, T3Lv = {}, {}, {}
for (h, o, l, vals) in rows_tab:
    v = state(h, o)
    T3Rv[(l, h)] = rat(ev_real(T3R, v)); BLv[(l, h)] = rat(ev_real(BLop, v)); T3Lv[(l, h)] = rat(ev_real(T3L, v))
nonneutral = {}
for l in SM:
    hs = sorted({h for (h2, o2, l2, _) in rows_tab if l2 == l for h in [h2]})
    nonneutral[l] = [(T3Lv[(l, h)], T3Rv[(l, h)], BLv[(l, h)]) for h in hs][0]
print("      (T3L, T3R, B-L) per multiplet:", nonneutral)
# neutral-component requirement: in each isodoublet, one component has Q = T3L + a T3R + b (B-L)/2 = 0
Qfam = lambda t3l, t3r, bl, a, b: t3l + a * t3r + b * bl / 2
eqs = []
for l in ("V_L", "V_R*"):
    t3l, t3r, bl = nonneutral[l]
    eqs.append(sp.Eq(Qfam(t3l, t3r, bl, a_, b_), 0))
sol_ab = sp.solve(eqs, [a_, b_], dict=True)
chk("F4a demanding a NEUTRAL component in the left doublet (nu_L) and in the right doublet (nu_R): Q = T3L + a T3R + b (B-L)/2 gives (a,b) = (1,1) uniquely", sol_ab == [{a_: 1, b_: 1}], str(sol_ab))
print("      F4a statement: without that requirement every (a,b) is an equally consistent U(1); the algebra alone does not pick (1,1) -- nu neutrality is the physical input.")
real_part_ok = nrm((1j * (T3L + T3R)).imag) < TOL and nrm((1j * BLop).imag) < TOL
chk("F4b the operators i(T3L + T3R) = -eps_3/2 and i(B-L) are real matrices, so conjugation invariance leaves the relative weight of (B-L) in Q completely free", real_part_ok)
lat_c = []
for cc in [sp.Rational(p, 6) for p in range(-24, 25)]:
    qs_ = {Qfam(*nonneutral[l], a=1, b=cc) for l in SM}
    if all((q * 3).is_integer for q in qs_):
        lat_c.append(cc)
print("      values of c in (1/6)Z in [-4,4] for which all 8 multiplet charges lie in (1/3)Z:", [str(x) for x in lat_c])
chk("F4c the thirds-lattice requirement alone allows several c (it does not single out c = 1)", len(lat_c) > 1 and sp.Integer(1) in lat_c, f"{len(lat_c)} values")

# ---------------- F5: anomalies
YY = {l: a_ * nonneutral[l][1] + b_ * nonneutral[l][2] / 2 for l in SM}
mult = {  # (colour dim, iso dim) of each of the 6 LH Weyl multiplets, Y from the state with the given label
    "Q": (3, 2, ["U_L", "D_L"]), "U": (3, 1, ["U_R*"]), "D": (3, 1, ["D_R*"]), "L": (1, 2, ["V_L", "E_L"]), "E": (1, 1, ["E_R*"]), "N": (1, 1, ["V_R*"])}
yM = {k: sp.simplify(YY[v[2][0]]) for k, v in mult.items()}
def anomalies(y):
    e_su3 = 2 * y["Q"] + y["U"] + y["D"]
    e_su2 = 3 * y["Q"] + y["L"]
    e_grav = 6 * y["Q"] + 3 * y["U"] + 3 * y["D"] + 2 * y["L"] + y["E"] + y["N"]
    e_cub = 6 * y["Q"] ** 3 + 3 * y["U"] ** 3 + 3 * y["D"] ** 3 + 2 * y["L"] ** 3 + y["E"] ** 3 + y["N"] ** 3
    return [sp.simplify(e) for e in (e_su3, e_su2, e_grav, e_cub)]
an = anomalies(yM)
chk("F5a for EVERY (a,b) the family Y = a T3R + b (B-L)/2 is anomaly-free on this 16 (all four polynomials vanish identically): anomalies do not fix the Y direction", all(e == 0 for e in an), str(an))
ySM = {k: v.subs({a_: 1, b_: 1}) for k, v in yM.items()}
y6SM = {k: 6 * v for k, v in ySM.items()}
chk("F5b at (a,b) = (1,1): 6Y = Q:1, U:-4, D:2, L:-3, E:6, N:0 -- the branch B2 of lane G with (y_U,y_D) = 6 x (-4,2)/6", y6SM == {"Q": 1, "U": -4, "D": 2, "L": -3, "E": 6, "N": 0}, str(y6SM))
# swapped branch (y_U, y_D) = (2, -4)/6 (the other root of the cubic in lane G A1d): its singlet charges Q = Y
chargesA = sorted([ySM["U"], ySM["D"]])
chargesB = sorted([sp.Rational(2, 6), sp.Rational(-4, 6)])
chk("F5c the u<->d branch (y_U, y_D) = (2,-4)/6 gives the SAME set of singlet charges {-2/3,+1/3} as the algebra's (-4,2)/6: a relabelling of which singlet is called u, not a different charge spectrum", chargesA == chargesB, f"{chargesA} vs {chargesB}")

# ---------------- F6: normalisation
Tr = lambda M: float(np.real(np.trace(M))) / 2          # trace over the 16 (32 = 16 x spin 2)
tT3, tY, tQ, tBL, tT3R = Tr(T3L @ T3L), Tr(Yop @ Yop), Tr(Qop @ Qop), Tr(BLop @ BLop), Tr(T3R @ T3R)
chk("F6a Tr_16 Y^2 / Tr_16 T3L^2 = 5/3 (SU(5)/Spin(10) hypercharge normalisation)", abs(tY / tT3 - 5 / 3) < 1e-9, f"(Tr T3L^2 = {tT3:.4f}, Tr Y^2 = {tY:.4f}, Tr Q^2 = {tQ:.4f})")
chk("F6b sin^2 theta_W = Tr T3L^2 / Tr Q^2 = 3/8 and alpha_em = (3/8) alpha_G IF Spin(10) is gauged with one coupling", abs(tT3 / tQ - 3 / 8) < 1e-9, f"({tT3 / tQ:.6f})")
print("      F6 statement: the algebra A has End(A) = Cl(10) and every simple factor carries ONE free 1/g^2 (Schur); the 3/8 exists only if one imposes the single coupling of Spin(10).")
chk.finish("w1_3")
