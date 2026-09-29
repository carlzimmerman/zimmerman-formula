#!/usr/bin/env python3
"""Q2 -- SU(2) gauge coupling of the Salam-Sezgin S^2 vacuum from the 6D action on the Gibbons-Pope Pauli ansatz, and the fate of the 6D U(1).
Pre-registered in Q3_PREREGISTRATION.md (written before this script was run).  Tests H3 and H4.

Source (hep-th/0307052 eqs. 2.1, 2.3, 2.5): 6D bosonic action, overall 1/(2 kappa_6^2),
    L = R - (1/12) e^{phi_hat} H^2 - (1/4) e^{phi_hat/2} F^2 - 8 g^2 e^{-phi_hat/2},   (phi_hat = p constant on the vacuum)
    ds^2 = e^{-p/2}... in the PHYSICAL 6D frame used here:  eta_{mu nu} dx dx + R^2 [d theta^2 + sin^2 theta (d psi + 2 g A_mu dx^mu)^2],  R^2 = e^{p/2}/(8 g^2)
    F_hat = d A_hat,  A_hat = -(1/(2g)) cos(theta) (d psi + 2 g A),        (= (2g)^-1 Omega - d(mu_3 A^3), source 2.5)
    H_hat = -2 g F^3 ^ K_3^flat,  K_3^flat = (sin^2 theta/(8 g^2)) (d psi + 2 g A)   (source 2.5 with H_(3)=0; the unhatted e^a are the round S^2 of curvature 8 g^2)
Here a Cartan generator only (A^3 = A(x) dy); SU(2) covariance fixes the other two.

Run:   python3 q2_pauli_su2_coupling_and_u1.py            (real run, exits 0)
       python3 q2_pauli_su2_coupling_and_u1.py --mutate   (control: DROP the H_(3) term of the reduction, i.e. Einstein-Maxwell only as in lane F; must FAIL the
                                                           checks that the total kinetic coefficient equals the source's 4D coefficient and that alpha_SU2 = 2 l_P^2/R^2)
"""
import sys
import itertools
sys.dont_write_bytecode = True
import sympy as sp
import sympy.combinatorics

MUTATE = "--mutate" in sys.argv
CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


print("=" * 100)
print("Q2 SU(2) coupling of the Salam-Sezgin S^2 vacuum -- mode: " + ("MUTATE CONTROL (H_(3) term dropped)" if MUTATE else "REAL RUN"))
print("=" * 100)

t, x, y, z, th, ps = sp.symbols("t x y z theta psi", real=True)
g, p, Rr = sp.symbols("g p R", positive=True)
Ap = sp.symbols("Ap", real=True)                     # A'(x)
Af = sp.Function("A")(x)
coords = [t, x, y, z, th, ps]
E = sp.exp(p / 2)

# ---------------------------------------------------------------- B3: Killing vectors and normalisation (source 2.8-2.10)
print("\nB3  Killing vectors of the round S^2 (source 2.9) and generator normalisation")
phi_ = sp.symbols("phi_", real=True)
Kfun = {1: (-sp.sin(phi_), -sp.cot(th) * sp.cos(phi_)), 2: (sp.cos(phi_), -sp.cot(th) * sp.sin(phi_)), 3: (0, 1)}   # (theta, phi) components


def comm(Ka, Kb):
    out = []
    for m, cm in enumerate((th, phi_)):
        out.append(sp.simplify(sum(Ka[n] * sp.diff(Kb[m], (th, phi_)[n]) - Kb[n] * sp.diff(Ka[m], (th, phi_)[n]) for n in range(2))))
    return tuple(out)


ok_alg = True
for (i, j, k) in ((1, 2, 3), (2, 3, 1), (3, 1, 2)):
    cc = comm(Kfun[i], Kfun[j])
    ok_alg &= all(sp.simplify(cc[m] + Kfun[k][m]) == 0 for m in range(2))
check("B3a [K_i, K_j] = -eps_ijk K_k (source 2.9): T_i = -i K_i is a standard su(2) (T_3 = m on e^{i m psi}, structure constants eps)", ok_alg)
# K_3 from K^m = (1/8g^2) eps^{mn} d_n mu_3, sqrt(g_2) = sin(theta)/(8 g^2), mu_3 = cos(theta)
sqrtg2 = sp.sin(th) / (8 * g ** 2)
K3phi = sp.simplify((1 / (8 * g ** 2)) * (-1 / sqrtg2) * sp.diff(sp.cos(th), th))     # eps^{phi theta} = -1/sqrt(g)
check("B3b K_3 = (1/(8 g^2)) eps^{mn} d_n mu_3 with mu_3 = cos(theta) gives K_3 = d/d psi (source 2.8-2.9)", sp.simplify(K3phi - 1) == 0)
# A_KK = 2 g A in (dy + 2 g A K): F_KK^i = 2 g dA + (1/2)[structure const] (2 g)^2 A^A A = 2 g (dA + g eps A^A): so F^i = dA + g eps A^A (source) and g_YM(non-canonical) = 2 g
gg = sp.symbols("gg", positive=True)
check("B3c non-abelian term: (1/2)(2g)^2 = (2g)(g), so the source's F^i = dA^i + g eps A^A corresponds to standard coupling 2g (D = d - i (2g) A^i T_i)",
      sp.simplify(sp.Rational(1, 2) * (2 * gg) ** 2 - (2 * gg) * gg) == 0)

# ---------------------------------------------------------------- 6D metric, curvature, forms
print("\n6D physical-frame background: R^2 = e^{p/2}/(8 g^2), A^3 = A(x) dy")
gm = sp.zeros(6, 6)
gm[0, 0] = -1; gm[1, 1] = 1; gm[3, 3] = 1
gm[4, 4] = Rr ** 2
gm[5, 5] = Rr ** 2 * sp.sin(th) ** 2
gm[5, 2] = gm[2, 5] = 2 * g * Af * Rr ** 2 * sp.sin(th) ** 2
gm[2, 2] = 1 + 4 * g ** 2 * Af ** 2 * Rr ** 2 * sp.sin(th) ** 2
gi = gm.inv().applyfunc(sp.simplify)
Gam = [[[sum(gi[a, d] * (sp.diff(gm[d, b], coords[c]) + sp.diff(gm[d, c], coords[b]) - sp.diff(gm[b, c], coords[d])) for d in range(6)) / 2 for c in range(6)] for b in range(6)] for a in range(6)]


def Ric(b, c):
    r = 0
    for a in range(6):
        r += sp.diff(Gam[a][b][c], coords[a]) - sp.diff(Gam[a][b][a], coords[c])
        for d in range(6):
            r += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
    return r


R6 = sp.simplify(sum(gi[b, c] * Ric(b, c) for b in range(6) for c in range(6)))
dA = sp.diff(Af, x)


def to_Ap(expr):
    return sp.simplify(expr.subs(sp.Derivative(Af, (x, 2)), sp.Symbol("App")).subs(dA, Ap))


R6p = to_Ap(R6)
print(f"    6D Ricci scalar = {R6p}")
# one-form potential and field strength
Ahat = [0, 0, -sp.cos(th) * Af, 0, 0, -sp.cos(th) / (2 * g)]
Fh = sp.Matrix(6, 6, lambda a, b: sp.diff(Ahat[b], coords[a]) - sp.diff(Ahat[a], coords[b]))
# H = -2 g F^3 ^ K^flat = -(A' sin^2 theta /(4 g)) dx ^ dy ^ dpsi  (dy^dy = 0)
Hxyp = -(dA * sp.sin(th) ** 2) / (4 * g)
if MUTATE:
    Hxyp = 0 * Hxyp
Hc = {}
for perm in itertools.permutations([1, 2, 5]):
    sgn = sp.combinatorics.Permutation([[1, 2, 5].index(v) for v in perm]).signature()
    Hc[perm] = sgn * Hxyp


def Hcomp(a, b, c):
    return Hc.get((a, b, c), 0)


# ---- B2: Bianchi dH = (1/2) F^F  (source 2.13 with H_(3) = 0; tests my transcription of the ansatz)
print("\nB2  ansatz consistency: Bianchi identity  d H_hat = (1/2) F_hat ^ F_hat")
Hfull = {}
for perm in itertools.permutations([1, 2, 5]):
    sgn = sp.combinatorics.Permutation([[1, 2, 5].index(v) for v in perm]).signature()
    Hfull[perm] = sgn * (-(dA * sp.sin(th) ** 2) / (4 * g))          # always the UN-mutated ansatz for the identity test


def asym_sign(perm):
    return sp.combinatorics.Permutation(list(perm)).signature()


def dH(M, N, P, Q):
    idx = (M, N, P, Q)
    tot = 0
    for k in range(4):        # (dH)_{MNPQ} = d_M H_NPQ - d_N H_MPQ + d_P H_MNQ - d_Q H_MNP
        rest = tuple(idx[:k] + idx[k + 1:])
        tot += (-1) ** k * sp.diff(Hfull.get(rest, 0), coords[idx[k]])
    return tot


def FF(M, N, P, Q):     # (F^F)_{MNPQ} = 2 (F_MN F_PQ - F_MP F_NQ + F_MQ F_NP) ; (1/2) F^F = F_MN F_PQ - F_MP F_NQ + F_MQ F_NP
    return Fh[M, N] * Fh[P, Q] - Fh[M, P] * Fh[N, Q] + Fh[M, Q] * Fh[N, P]


bian_ok = True
for idx in itertools.combinations(range(6), 4):
    if sp.simplify(dH(*idx) - FF(*idx)) != 0:
        bian_ok = False
check("B2 Bianchi d H = (1/2) F ^ F holds identically on the ansatz for all 15 index sets", bian_ok)

# ---------------------------------------------------------------- B1: vacuum and B6: gauge invariance, quadratic coefficients
print("\nB1/B6  Lagrangian on the ansatz: vacuum value, dependence on A only through F, quadratic coefficients")
F2 = sum(gi[a, c] * gi[b, d] * Fh[a, b] * Fh[c, d] for a in range(6) for b in range(6) for c in range(6) for d in range(6))
F2p = to_Ap(F2)
H2 = 0
for (a, b, c) in Hc:
    for (d, e, f_) in Hc:
        H2 += gi[a, d] * gi[b, e] * gi[c, f_] * Hcomp(a, b, c) * Hcomp(d, e, f_)
H2p = to_Ap(H2)
Rsub = {Rr: sp.sqrt(E / (8 * g ** 2))}
LR = R6p
LF = -sp.Rational(1, 4) * E * F2p
LH = -sp.Rational(1, 12) * sp.exp(p) * H2p
LV = -8 * g ** 2 / E
Ltot = sp.simplify((LR + LF + LH + LV).subs(Rsub))
print(f"    L (physical frame, per unit volume element sqrt(-g)/(R^2 sin theta)) = {sp.simplify(Ltot)}")
L0 = sp.simplify(Ltot.subs(Ap, 0))
check("B1 vacuum: L(A'=0) = 0 (V = 0 at the Salam-Sezgin point; consistent with q1)", L0 == 0, f"[value {L0}]")
noA = all(sp.simplify(sp.diff(w, Af)) == 0 for w in (LR, LF, LH))
check("B6 the reduced Lagrangian depends on A only through F = A' (no bare A: gauge invariance of the ansatz)", noA)


def quad_coeff(expr):
    e = sp.expand(sp.simplify(expr.subs(Rsub)))
    return sp.simplify(e.coeff(Ap, 2)), sp.simplify(e.coeff(Ap, 1))


kR, lR = quad_coeff(LR); kF, lF = quad_coeff(LF); kH, lH = quad_coeff(LH)
check("B6b no term linear in A' in any piece", lR == 0 and lF == 0 and lH == 0)
# L_X quad = k_X Ap^2 ;  F_{mu nu}F^{mu nu} = 2 Ap^2 ;  L_X = -(1/4) c_X F_{mu nu}F^{mu nu}  ->  c_X = -2 k_X
cX = {k: sp.simplify(-2 * v) for k, v in (("metric", kR), ("F_(2)", kF), ("H_(3)", kH))}
Rsq = E / (8 * g ** 2)
CX = {}
for k, v in cX.items():
    CX[k] = sp.simplify(sp.integrate(sp.integrate(Rsq * sp.sin(th) * v, (th, 0, sp.pi)), (ps, 0, 2 * sp.pi)))
    print(f"    {k:7s}: c(theta) = {sp.simplify(v)};   C = int R^2 sin(theta) c dOmega = {CX[k]}")
Ctot = sp.simplify(sum(CX.values()))
Cpred = sp.pi * sp.exp(p) / (2 * g ** 2)            # source (2.17): -(1/2) e^{-phi} *F^F  with Vol(round S^2, R^2=1/(8g^2)) = pi/(2 g^2), phi = -p
check("B4a the three pieces are equal (metric : F_(2) : H_(3) = 1 : 1 : 1) in the un-mutated theory", sp.simplify(CX["metric"] - CX["F_(2)"]) == 0 and (MUTATE or sp.simplify(CX["metric"] - CX["H_(3)"]) == 0))
ctheta_tot = sp.simplify(sum(cX.values()))
check("B4c the theta-dependence of the total kinetic density cancels (c_tot(theta) = e^{p/2}, constant): the source's 'conspiracy' that makes the Pauli reduction consistent; it needs all three pieces",
      sp.simplify(sp.diff(ctheta_tot, th)) == 0)
check("B4b total kinetic coefficient C = pi e^{p}/(2 g^2) = Vol x (source 2.17 coefficient e^{-phi} with phi = -p): the 6D reduction reproduces the source's 4D action",
      sp.simplify(Ctot - Cpred) == 0, f"[C_total = {Ctot}, source-predicted = {Cpred}]")

# ---------------------------------------------------------------- B5: alpha_SU2 in units of l_P^2/R^2
print("\nB5  alpha_SU2 in terms of G_4 and R")
kap2 = sp.symbols("kappa2", positive=True)
# L_4 = (1/(2 kappa^2)) [ 4 pi R^2 R_4 - (1/4) C F_{mu nu}F^{mu nu} ];  G = kappa^2/(32 pi^2 R^2) ; A_c = A sqrt(C/(2 kappa^2)); T_3 couples to 2 g A^3
G4 = kap2 / (32 * sp.pi ** 2 * Rsq)
gYM2 = (2 * g) ** 2 * (2 * kap2) / Ctot
alpha_su2 = sp.simplify(gYM2 / (4 * sp.pi))
coeff = sp.simplify(alpha_su2 / (G4 / Rsq))
print(f"    alpha_SU2 = g_YM^2/(4 pi) = {alpha_su2};   G_4 = {sp.simplify(G4)};   alpha_SU2 / (l_P^2/R^2) = {coeff}")
Ctot_noH = sp.simplify(CX["metric"] + CX["F_(2)"])
coeff_noH = sp.simplify((((2 * g) ** 2 * (2 * kap2) / Ctot_noH) / (4 * sp.pi)) / (G4 / Rsq))
print(f"    without the H_(3) contribution (metric + F_(2) only, i.e. lane F / N1's Einstein-Maxwell-Lambda theory): alpha_SU2/(l_P^2/R^2) = {coeff_noH}")
check("B5a alpha_SU2 = 2 l_P^2/R^2 on the Salam-Sezgin vacuum (H_(3) included)", sp.simplify(coeff - 2) == 0)
check("B5b without H_(3) the same procedure returns lane F's / N1's 3 l_P^2/R^2 (cross-check of the method against F2 B3d and N1 I2c)", sp.simplify(coeff_noH - 3) == 0)
print(f"ALPHA_SU2_COEFF = {coeff}")
print(f"ALPHA_SU2_COEFF_NOH = {coeff_noH}")

# ---------------------------------------------------------------- B7: 6D photon l = 0 mode
print("\nB7  the 6D U(1) photon zero mode: Stueckelberg mass from H = dB + c_CS F ^ A")
a_ = sp.symbols("a", real=True)
qbg = 1 / (2 * g)                                   # F_hat_{theta psi} = sin(theta) q_bg
mass_table = {}
for cCS in (sp.Rational(1, 2), sp.Integer(1)):
    Hthpz = cCS * qbg * sp.sin(th) * a_             # H_{theta psi z} = c_CS F_{theta psi} a_z, unitary gauge B_{theta psi} = 0, constant a_z
    ginv = {th: 1 / Rsq, ps: 1 / (Rsq * sp.sin(th) ** 2), z: 1}
    H2u = 6 * Hthpz ** 2 * ginv[th] * ginv[ps] * ginv[z]
    LHa = sp.simplify(-sp.Rational(1, 12) * sp.exp(p) * H2u)                # = -rho a^2
    rho_ = sp.simplify(-LHa / a_ ** 2)
    # Proca: L = -(1/4) e^{p/2} f^2 - rho a^2 = -(1/4) e^{p/2}(f^2 + 4 m^2 a^2 ... ) -> m^2 = 2 rho / e^{p/2}
    m2 = sp.simplify(2 * rho_ / E)
    mass_table[cCS] = sp.simplify(m2 * Rsq)
    print(f"    c_CS = {cCS}: mass term -{rho_} a^2  ->  m^2 = {m2},  m^2 R^2 = {mass_table[cCS]}")
check("B7a the l = 0 photon acquires a mass ~ 1/R for either normalisation of the CS coupling (no massless U(1); its Stueckelberg partner is B_{theta psi})",
      all(v > 0 for v in mass_table.values()))
check("B7b m^2 R^2 = 1/2 (c_CS = 1/2, the source's H = dB + (1/2) F^A read naively) and 2 (c_CS = 1: the source's (5.9) 'Proca mass 4 g e^{phi0/2}')", mass_table[sp.Rational(1, 2)] == sp.Rational(1, 2) and mass_table[sp.Integer(1)] == 2)
print("    NOTE (statement, not a check): the source's (5.9) corresponds to c_CS = 1 (m^2 = 16 g^2 e^{phi0} in its 4D frame = 2/R^2 physical). My naive c_CS = 1/2 gives a factor 4 smaller m^2.")
print("    The difference is the treatment of the Chern-Simons term with the singular background potential (H = dB + (1/2)F^A shifts by dA ^ A_bg under a B redefinition, coefficient 1/2 -> 1); I did NOT resolve which the source used")
print("    beyond noting that (5.9) matches c_CS = 1. It does not matter for H4: the photon is massive in both, at the KK scale, so N1's alpha_U1 = N^2 l_P^2/(2R^2) massless-U(1) relation does not apply.")

n_ok = sum(1 for _, o in CHECKS if o)
print("\n" + "=" * 100)
print(f"CHECKS: {n_ok}/{len(CHECKS)} passed")
print("VERDICT (q2):")
print("  * H3 NOT reproduced: on the Salam-Sezgin vacuum alpha_SU2 = 2 l_P^2/R^2 (metric, F_(2) and H_(3) contribute equally), not lane F's 3 l_P^2/R^2 (Einstein-Maxwell-Lambda, no H_(3)).")
print("    The 6D reduction reproduces the source's 4D kinetic term exactly (B4b), so the factor is a property of the SUSY theory, not of my method.")
print("  * H4: the 6D U(1) photon is massive (Stueckelberg with B_{theta psi}); only the l = 0 photon was tested here (massive); the source's massless spectrum lists the SU(2) triplet only. N1's alpha_U1 relation has no massless U(1) to apply to.")
sys.exit(0 if n_ok == len(CHECKS) else 1)
