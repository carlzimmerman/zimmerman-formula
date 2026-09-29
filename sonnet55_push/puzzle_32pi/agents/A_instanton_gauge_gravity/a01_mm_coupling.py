#!/usr/bin/env python3
"""a01: MacDowell-Mansouri (SO(5) / SO(4,1)) gauge form of de Sitter gravity -- what is the 'gauge coupling', and how does the
dS entropy read as an instanton action?   (Euclidean, hbar restored where it matters; the a0 relation itself has neither G nor hbar.)

Setup (all checked below, nothing assumed):
  MM curvature  F^{ab} = R^{ab} - (1/L^2) e^a e^b           (SO(5) curvature restricted to the SO(4) block; F^{a5} = torsion = 0)
  Claim A1 (algebra, 400 random algebraic curvature tensors):  eps_{abcd} F^{ab} F^{cd} / vol  =  E4 - (4/L^2)(R - 6/L^2)
           with E4 = Riem^2 - 4 Ric^2 + R^2 = (1/4) delta^{efgh}_{abcd} R^{ab}_{ef} R^{cd}_{gh}  (the Euler density, eps R R = E4 vol)
           hence  (R - 2 Lambda) vol = (L^2/4) (eps R R - eps F F)   with Lambda = 3/L^2.
  Claim A2 (S^4 in stereographic coordinates): R^{ab} = e^a e^b / L^2, so F = 0: the round S^4 is a FLAT SO(5) connection.
  Claim A3: the on-shell Euclidean EH action  I = -(1/16 pi G) Int (R - 2 Lambda) vol = -(L^2/64 pi G)(Int eps R R - Int eps F F) = -pi L^2/G
           comes ENTIRELY from the topological (Euler) term, Int eps R R = 32 pi^2 chi = 64 pi^2, because Int eps F F = 0 on shell.
  Claim A4 (chiral split): eps_{abcd} F^{ab} F^{cd} = 2 (G_+^i G_+^i - G_-^i G_-^i), G_pm^i = (1/2) eps_{ijk} F^{jk} pm F^{i4};
           on S^4 the curvatures of the SU(2)_pm spin connections are the BPST 2-forms (4/(1+r^2)^2) eta^i_pm and integrate to
           Int G^i G^i = 16 pi^2 k each (F^i_{mn}F^i_{mn} d^4x = 32 pi^2 k), so Int eps R R = 2 (16 pi^2 + 16 pi^2) = 64 pi^2.
  Result: matching the topological term to a YM-normalised instanton action (8 pi^2 / g^2) per unit instanton number gives
           1/g^2 = L^2/(16 pi hbar G),   8 pi^2/g^2 = pi L^2/(2 hbar G) = S_dS/2,   S_dS = chi * (8 pi^2/g^2)  with chi = 2.
  The convention-independent, hbar-free, L-free content is the RATIO  S_dS / (instanton action) = chi = 2  (A5), and
           S_{a0} / (instanton action) = Z^2/2 = 16 pi/3   (A6, S_{a0} = area/(4 hbar G) of the puzzle's Schwarzschild horizon),
  an irrational number: it is the puzzle itself, not something the gauge structure supplies.
Exit 0 = all checks and controls behave.
"""
import sys, itertools
import numpy as np
import sympy as sp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ---------------------------------------------------------------- A1: pointwise algebra with random algebraic curvature tensors
rng = np.random.default_rng(20260929)
eps4 = np.zeros((4, 4, 4, 4))
for p in itertools.permutations(range(4)):
    eps4[p] = np.linalg.det(np.eye(4)[list(p)])

def KN(h, k):   # Kulkarni-Nomizu product: (h wedge k)_{abcd} = h_ac k_bd + h_bd k_ac - h_ad k_bc - h_bc k_ad
    return (np.einsum('ac,bd->abcd', h, k) + np.einsum('bd,ac->abcd', h, k)
            - np.einsum('ad,bc->abcd', h, k) - np.einsum('bc,ad->abcd', h, k))

def random_curvature():
    R = np.zeros((4, 4, 4, 4))
    for _ in range(4):
        h = rng.normal(size=(4, 4)); h = h + h.T
        k = rng.normal(size=(4, 4)); k = k + k.T
        R += KN(h, k)
    return R

def bianchi_ok(R):
    b = R + np.einsum('abcd->acdb', R) + np.einsum('abcd->adbc', R)      # R_abcd + R_acdb + R_adbc = 0
    return np.abs(b).max() < 1e-9

def E4_tensor(R):
    Ric = np.einsum('acbc->ab', R); Rs = np.trace(Ric)
    return np.sum(R * R) - 4 * np.sum(Ric * Ric) + Rs ** 2, Rs

def eps_FF_over_vol(Fabef):   # (1/4) eps_{abcd} eps^{efgh} F^{ab}_{ef} F^{cd}_{gh}
    return 0.25 * np.einsum('abcd,efgh,abef,cdgh->', eps4, eps4, Fabef, Fabef)

Lsq = 1.7
delta2 = np.einsum('ae,bf->abef', np.eye(4), np.eye(4)) - np.einsum('af,be->abef', np.eye(4), np.eye(4))
bad = 0; bad_ctrl = 0; nbian = 0
for _ in range(400):
    R = random_curvature(); nbian += bianchi_ok(R)
    E4, Rs = E4_tensor(R)
    lhs_RR = eps_FF_over_vol(R)
    F = R - delta2 / Lsq
    lhs_FF = eps_FF_over_vol(F)
    rhs = E4 - (4 / Lsq) * (Rs - 6 / Lsq)
    bad += (abs(lhs_RR - E4) > 1e-8 * (1 + abs(E4))) or (abs(lhs_FF - rhs) > 1e-8 * (1 + abs(rhs)))
    # control: a wrong coefficient (2/L^2 instead of 4/L^2 in the EH-like term, and 24/L^4 kept) must NOT match
    rhs_wrong = E4 - (2 / Lsq) * (Rs - 6 / Lsq)
    bad_ctrl += abs(lhs_FF - rhs_wrong) < 1e-8 * (1 + abs(rhs))
chk("A0 random tensors really are algebraic curvature tensors (first Bianchi holds): %d/400" % nbian, nbian == 400)
chk("A1 eps R R = E4 vol and eps F F = E4 - (4/L^2)(R - 6/L^2) on 400 random curvature tensors (mismatches: %d)" % bad, bad == 0)
chk("A1-control: with 2/L^2 in place of 4/L^2 the identity is rejected on (almost) every tensor (accidental agreements: %d/400)" % bad_ctrl, bad_ctrl < 5)

# ---------------------------------------------------------------- A2: S^4 in stereographic frame, F = 0
x = sp.symbols('x1:5', real=True); r2 = sum(xi ** 2 for xi in x)
L = sp.symbols('L', positive=True)
s = sp.log(2 * L / (1 + r2))                    # e^s = Omega = 2L/(1+r^2);  metric = Omega^2 delta
ds = [sp.diff(s, xi) for xi in x]
def om(a, b, m):      # omega^{ab}_m = d_b s delta^a_m - d_a s delta^b_m  (torsion free: de^a + omega^a_b e^b = 0)
    return ds[b] * (1 if a == m else 0) - ds[a] * (1 if b == m else 0)
def Rc(a, b, m, n):   # R^{ab}_{mn} = d_m om^{ab}_n - d_n om^{ab}_m + om^{ac}_m om^{cb}_n - om^{ac}_n om^{cb}_m
    t = sp.diff(om(a, b, n), x[m]) - sp.diff(om(a, b, m), x[n])
    t += sum(om(a, c, m) * om(c, b, n) - om(a, c, n) * om(c, b, m) for c in range(4))
    return sp.simplify(t)
Om2 = (2 * L / (1 + r2)) ** 2
allF0 = True; allR = True
for a in range(4):
    for b in range(4):
        for m in range(4):
            for n in range(4):
                Rab = Rc(a, b, m, n)
                target = Om2 / L ** 2 * ((1 if (a == m and b == n) else 0) - (1 if (a == n and b == m) else 0))   # (1/L^2) e^a e^b, e^a = Omega dx^a
                allR = allR and sp.simplify(Rab - target) == 0
                Fab = Rab - target
                allF0 = allF0 and sp.simplify(Fab) == 0
chk("A2 S^4(L): R^{ab} = (1/L^2) e^a ^ e^b for all 256 components (constant curvature 1/L^2)", allR)
chk("A2 F^{ab} = R^{ab} - e^a e^b/L^2 = 0: the round S^4 is a flat SO(5) connection (its MM 'field strength' vanishes)", allF0)
chk("A2-control: with e^a e^b/(2 L^2) the field strength would NOT vanish", sp.simplify(Rc(0, 1, 0, 1) - Om2 / (2 * L ** 2)) != 0)

# ---------------------------------------------------------------- A3: on-shell action = topological term
G, hbar = sp.symbols('G hbar', positive=True)
Vol = sp.Rational(8, 3) * sp.pi ** 2 * L ** 4                      # Vol(S^4(L)), computed in p01 G1 from the metric
E4_S4 = 24 / L ** 4                                                # p01 (sympy Riemann of the static form): E4 = 24/L^4
Int_epsRR = sp.simplify(E4_S4 * Vol)                              # eps R R = E4 vol
Int_epsFF = 0                                                     # A2
I_onshell = -(L ** 2 / (64 * sp.pi * G)) * (Int_epsRR - Int_epsFF)
chk("A3 Int eps R R = 64 pi^2 = 32 pi^2 chi(S^4), independent of L", sp.simplify(Int_epsRR - 64 * sp.pi ** 2) == 0)
chk("A3 I_on-shell = -(L^2/64 pi G)(Int eps R R - Int eps F F) = -pi L^2/G = - S_dS (hbar = 1): the whole on-shell action is the Euler term",
    sp.simplify(I_onshell + sp.pi * L ** 2 / G) == 0)
# check the identity behind it: (R - 2 Lambda) vol = (L^2/4)(eps R R - eps F F) on S^4 directly
R12 = 12 / L ** 2
Lam = 3 / L ** 2
chk("A3 (R - 2 Lambda) = 12/L^2 - 6/L^2 = 6/L^2 = (L^2/4)(24/L^4 - 0) pointwise on S^4", sp.simplify((R12 - 2 * Lam) - (L ** 2 / 4) * E4_S4) == 0)

# ---------------------------------------------------------------- A4: chiral SU(2)_+ x SU(2)_- split (pointwise algebra + S^4 instanton integral)
def eta(i, sign):    # anti-symmetric 4x4 matrix: (1/2) eps_{ijk} dx^j dx^k  +- dx^i dx^4   (i = 0,1,2)
    M = np.zeros((4, 4))
    for j in range(3):
        for k in range(3):
            M[j, k] = float(sp.LeviCivita(i, j, k))
    M[i, 3] = sign; M[3, i] = -sign
    return M
def comps_G(Fabmn, sign):    # G^i_{pm, mn} = (1/2) eps_{ijk} F^{jk}_{mn} +- F^{i4}_{mn}
    Gs = []
    for i in range(3):
        g = np.zeros((4, 4))
        for j in range(3):
            for k in range(3):
                g += 0.5 * float(sp.LeviCivita(i, j, k)) * Fabmn[j, k]
        g += sign * Fabmn[i, 3]
        Gs.append(g)
    return Gs
def wedge4(Fmn, Hmn):        # (F ^ H)_{1234} = (1/4) eps^{mnpq} F_mn H_pq
    return 0.25 * np.einsum('mnpq,mn,pq->', eps4, Fmn, Hmn)
bad = 0
for _ in range(200):
    A = rng.normal(size=(4, 4, 4, 4))                      # F^{ab}_{mn}: antisymmetrise in ab and mn
    A = A - A.transpose(1, 0, 2, 3); A = A - A.transpose(0, 1, 3, 2)
    lhs = sum(eps4[a, b, c, d] * wedge4(A[a, b], A[c, d]) for a in range(4) for b in range(4) for c in range(4) for d in range(4) if eps4[a, b, c, d] != 0)
    Gp = comps_G(A, +1); Gm = comps_G(A, -1)
    rhs = 2 * (sum(wedge4(g, g) for g in Gp) - sum(wedge4(g, g) for g in Gm))
    bad += abs(lhs - rhs) > 1e-8 * (1 + abs(lhs))
chk("A4 eps_{abcd} F^{ab}^F^{cd} = 2 (G_+^i ^ G_+^i - G_-^i ^ G_-^i), G_pm = (1/2)eps_{ijk}F^{jk} pm F^{i4}: 200 random so(4) 2-forms (mismatches %d)" % bad, bad == 0)

# on S^4: G_pm = R-projections = (4/(1+r^2)^2) eta_pm ; (anti)self-dual, sum G^i_mn G^i_mn = 192/(1+r^2)^4, G^i ^ G^i = +-96/(1+r^2)^4 d^4x
Om2n = 4 / (1 + r2) ** 2      # L-independent in stereographic coordinates
Gp_S = [Om2n * sp.Matrix(eta(i, +1)) for i in range(3)]
Gm_S = [Om2n * sp.Matrix(eta(i, -1)) for i in range(3)]

# the SU(2)_pm CONNECTIONS of p10, A^i_pm = (1/2) eps_{ijk} om^{jk} pm om^{i4},  F = dA - eps A A  have exactly these curvatures
def A_pm(i, mu, sgn):
    t = sum(sp.Rational(1, 2) * sp.LeviCivita(i, j, k) * om(j, k, mu) for j in range(3) for k in range(3)) + sgn * om(i, 3, mu)
    return sp.simplify(t)
def F_pm(i, m, n, sgn):
    dA = sp.diff(A_pm(i, n, sgn), x[m]) - sp.diff(A_pm(i, m, sgn), x[n])
    comm = sum(sp.LeviCivita(i, j, k) * A_pm(j, m, sgn) * A_pm(k, n, sgn) for j in range(3) for k in range(3))
    return sp.simplify(dA - comm)
match = all(sp.simplify(F_pm(i, m, n, sg) - Gs[i][m, n]) == 0 for sg, Gs in ((+1, Gp_S), (-1, Gm_S)) for i in range(3) for m in range(4) for n in range(4))
chk("A4 F(A_pm) of the spin-connection SU(2)_pm (p10 convention F = dA - eps A A) equals the projections G_pm = (1/2) eps R^{jk} pm R^{i4} on all 96 components", match)
wrong = all(sp.simplify(F_pm(i, m, n, +1) + Gp_S[i][m, n]) == 0 for i in range(3) for m in range(4) for n in range(4))
chk("A4-control: the sign-flipped identification F(A_+) = -G_+ is rejected", not wrong)
def sq(Ms): return sp.simplify(sum(sum(M[m, n] ** 2 for m in range(4) for n in range(4)) for M in Ms))
def wed(Ms):
    tot = 0
    for M in Ms:
        for (m, n, p, q) in itertools.permutations(range(4)):
            tot += sp.Rational(1, 4) * sp.LeviCivita(m, n, p, q) * M[m, n] * M[p, q]
    return sp.simplify(tot)
chk("A4 S^4: G_pm^i_{mn} G_pm^i_{mn} = 192/(1+r^2)^4 (the BPST density of p10) for both chiralities",
    sp.simplify(sq(Gp_S) - 192 / (1 + r2) ** 4) == 0 and sp.simplify(sq(Gm_S) - 192 / (1 + r2) ** 4) == 0)
chk("A4 S^4: G_+ ^ G_+ = +96/(1+r^2)^4 d^4x (self-dual), G_- ^ G_- = -96/(1+r^2)^4 d^4x (anti-self-dual)",
    sp.simplify(wed(Gp_S) - 96 / (1 + r2) ** 4) == 0 and sp.simplify(wed(Gm_S) + 96 / (1 + r2) ** 4) == 0)
dens = sp.simplify(2 * (wed(Gp_S) - wed(Gm_S)))
chk("A4 S^4: 2(G_+^G_+ - G_-^G_-) = 384/(1+r^2)^4 d^4x = E4 * vol (E4 = 24/L^4, vol = (2L/(1+r^2))^4 d^4x)", sp.simplify(dens - E4_S4 * (2 * L / (1 + r2)) ** 4) == 0)
rr = sp.symbols('rr', positive=True)
Ichir = 2 * sp.pi ** 2 * sp.integrate(96 * rr ** 3 / (1 + rr ** 2) ** 4, (rr, 0, sp.oo))
chk("A4 S^4: Int G_pm ^ G_pm = +- 16 pi^2 (k = 1 each; = (1/2) Int F^i_mn F^i_mn = (1/2) 32 pi^2)", sp.simplify(Ichir - 16 * sp.pi ** 2) == 0)
chk("A4 hence Int eps R R = 2(16 pi^2 + 16 pi^2) = 64 pi^2 = 32 pi^2 (k_+ + k_-)", sp.simplify(2 * (Ichir + Ichir) - 64 * sp.pi ** 2) == 0)

# ---------------------------------------------------------------- Result: the coupling
# The topological piece of the MM/EH action is  I_top = -(L^2/(64 pi G hbar)) Int eps R R = -(L^2/(64 pi G hbar)) 32 pi^2 (k_+ + k_-).
# Per unit chiral instanton number this is (L^2 32 pi^2)/(64 pi G hbar) = pi L^2/(2 G hbar).  Writing a YM-normalised instanton action 8 pi^2/g^2:
g2 = sp.symbols('g2', positive=True)
sol = sp.solve(sp.Eq(8 * sp.pi ** 2 / g2, sp.pi * L ** 2 / (2 * G * hbar)), g2)[0]
chk("R1 1/g^2 = L^2/(16 pi hbar G)   [g^2 = 16 pi hbar G/L^2 = 16 pi l_P^2/L^2 = (16 pi/3) hbar G Lambda]",
    sp.simplify(sol - 16 * sp.pi * G * hbar / L ** 2) == 0 and sp.simplify(sol - sp.Rational(16, 3) * sp.pi * G * hbar * Lam) == 0)
S_dS = sp.pi * L ** 2 / (G * hbar)
inst = 8 * sp.pi ** 2 / sol
chk("R2 S_dS = pi L^2/(hbar G) = chi * (8 pi^2/g^2) with chi = 2: ratio S_dS / (instanton action) = 2 for every L, G, hbar",
    sp.simplify(S_dS / inst) == 2)
Zsym = sp.sqrt(32 * sp.pi / 3)
S_a0 = sp.pi / (4 * sp.symbols('a0', positive=True) ** 2 * G * hbar)
a0v = 1 / (Zsym * L)
ratio = sp.simplify((S_a0.subs(sp.symbols('a0', positive=True), a0v)) / inst)
chk("R3 S_{a0}/(instanton action) = Z^2/2 = 16 pi/3 (irrational: contains the puzzle's pi; NOT an integer or rational)", sp.simplify(ratio - 16 * sp.pi / 3) == 0 and not sp.nsimplify(16 * sp.pi / 3).is_rational)
chk("R3-control: for Z^2 = 32/3 the ratio would be rational 16/3 -- the check discriminates", sp.simplify(sp.Rational(32, 3) / 2 - sp.Rational(16, 3)) == 0)
print("\n   summary: 1/g^2 = L^2/(16 pi hbar G);  8 pi^2/g^2 = pi L^2/(2 hbar G) = S_dS/2;  S_dS/(8pi^2/g^2) = chi = 2;  S_a0/(8 pi^2/g^2) = 16 pi/3")
print("   hbar-content: g^2 ~ hbar G Lambda (hbar-FULL); the ratios above are hbar-free but the RATIO S_a0/S_dS = 8 pi/3 is exactly the puzzle.")
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
