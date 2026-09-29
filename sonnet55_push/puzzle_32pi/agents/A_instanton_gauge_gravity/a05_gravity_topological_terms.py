#!/usr/bin/env python3
"""a05: gravitational topological terms -- does any carry a dimensionful coupling that could set an acceleration?  (c = 1, hbar restored via l_P^2 = hbar G.)

Terms examined and what is computed:
  P1  Euler / Gauss-Bonnet:  (alpha/(16 pi hbar G)) Int E4.  alpha has dimension length^2 and is a FREE coupling in EGB gravity.  In the MM (SO(5)) form the
      Euler coefficient is not free: it is fixed to L^2/(64 pi G) by requiring the action to equal EH; the MM curvature vanishes only for ell = L (P2).
  P2  The MM action with an independent radius ell in F = R - e e/ell^2, evaluated on S^4(L):  eps F F/vol = (24/L^4)(1 - L^2/ell^2)^2 and
      I_MM(ell) = (pi/G)(ell^2 - L^2)^2/ell^2: zero and stationary ONLY at ell = L.  The dS connection selects ell = L, not ell = Z L.
  P3  Pontryagin / signature: R R~ = 0 on S^4 (conformally flat; tr F_{SO(5)}^2 = 0 for every ell); the Euler number chi(S^4) = 2 comes entirely from the scalar
      curvature term R^2/24 (W = 0): chi = Lambda^2 V_4/(12 pi^2) with V_4 = 24 pi^2/Lambda^2.
  P4  Nieh-Yan / Holst: the NY 4-form vanishes for torsion-free e (first Bianchi: eps^{abcd} R_{abcd} = 0), so the Holst term 1/gamma is dimensionless AND inert.
  P5  Gravitational instantons have size moduli: Eguchi-Hanson  ds^2 = dr^2/f + (r^2/4)(sigma_1^2 + sigma_2^2 + f sigma_3^2), f = 1 - a^4/r^4:  Riem^2 = 384 a^8/r^12,
      Int E4 = 48 pi^2 and Int R R~ = -+ 48 pi^2 for EVERY a: the size a is a free length that no topological charge fixes.
  P6  The only quantisation available: the chiral instanton action per unit charge is S_dS/2 (a01); single-valuedness of exp(i k S_dS/2) under a unit large gauge
      transformation needs K = S_dS/(4 pi) = L^2/(4 hbar G) = 3/(4 hbar G Lambda) in Z.  This agrees with the published Chern-Simons-Kodama integrality condition
      kappa = 3/(4 G Lambda beta), beta = Immirzi parameter (arXiv gr-qc/0504010, opened; note that paper's 'a_0' is a PLANCK area, not the MOND scale) and with theta = 12 pi^2/(Lambda l_Pl^2)
      mod 2 pi of arXiv 2506.14886 (opened).  It quantises 1/(hbar G Lambda) = 1/Pi_2: Lambda in Planck units; a0 does not appear.
Exit 0 = all checks and controls behave.
"""
import sys, itertools
import numpy as np
import sympy as sp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

L, ell, G, hb, Lam = sp.symbols('L ell G hbar Lambda', positive=True)

# ---------------------------------------------------------------- P2: MM action with an independent radius ell on S^4(L)
E4 = 24 / L ** 4; R = 12 / L ** 2
epsFF = E4 - (4 / ell ** 2) * (R - 6 / ell ** 2)            # a01 identity with L -> ell in F
chk("P2 eps F_ell F_ell / vol on S^4(L) = (24/L^4)(1 - L^2/ell^2)^2", sp.simplify(epsFF - (24 / L ** 4) * (1 - L ** 2 / ell ** 2) ** 2) == 0)
Vol = sp.Rational(8, 3) * sp.pi ** 2 * L ** 4
I_MM = sp.simplify((ell ** 2 / (64 * sp.pi * G)) * epsFF * Vol)
chk("P2 I_MM(ell) = (ell^2/(64 pi G)) Int eps F F = (pi/G)(ell^2 - L^2)^2/ell^2", sp.simplify(I_MM - sp.pi * (ell ** 2 - L ** 2) ** 2 / (G * ell ** 2)) == 0)
crit = sp.solve(sp.diff(I_MM, ell), ell)
chk("P2 the only stationary point of I_MM(ell) is ell = L (where it vanishes): the MM connection selects the dS radius, nothing at ell = Z L", crit == [L] and sp.simplify(I_MM.subs(ell, L)) == 0)
Zs = sp.sqrt(32 * sp.pi / 3)
print("   cost of using ell = Z L on S^4(L): I_MM = %s * (pi L^2/G)" % sp.nsimplify(sp.simplify(I_MM.subs(ell, Zs * L) / (sp.pi * L ** 2 / G))))
chk("P2-control: at ell = Z L the action is NOT stationary", sp.simplify(sp.diff(I_MM, ell).subs(ell, Zs * L)) != 0)

# ---------------------------------------------------------------- P3: Euler number of the Euclidean dS is the R^2/24 term
Rsc = 4 * Lam
V4 = 24 * sp.pi ** 2 / Lam ** 2
chi = sp.simplify((1 / (8 * sp.pi ** 2)) * (Rsc ** 2 / 24) * V4)      # W = 0, Ric_0 = 0 on S^4
chk("P3 chi(S^4) = (1/8 pi^2) Int (|W|^2 - |Ric_0|^2/2 + R^2/24) = Lambda^2 V_4/(12 pi^2) = 2 with W = Ric_0 = 0, R = 4 Lambda, V_4 = 24 pi^2/Lambda^2",
    sp.simplify(chi - 2) == 0 and sp.simplify(Lam ** 2 * V4 / (12 * sp.pi ** 2) - 2) == 0)
chk("P3 V_4(S^4(L)) = (8 pi^2/3) L^4 = 24 pi^2/Lambda^2 for Lambda = 3/L^2", sp.simplify((sp.Rational(8, 3) * sp.pi ** 2 * L ** 4).subs(L, sp.sqrt(3 / Lam)) - V4) == 0)

# ---------------------------------------------------------------- P4: Nieh-Yan is inert for torsion-free e
rng = np.random.default_rng(7)
eps4 = np.zeros((4, 4, 4, 4))
for p in itertools.permutations(range(4)):
    eps4[p] = np.linalg.det(np.eye(4)[list(p)])
def KN(h, k):
    return (np.einsum('ac,bd->abcd', h, k) + np.einsum('bd,ac->abcd', h, k) - np.einsum('ad,bc->abcd', h, k) - np.einsum('bc,ad->abcd', h, k))
def randR():
    Rr = np.zeros((4, 4, 4, 4))
    for _ in range(4):
        h = rng.normal(size=(4, 4)); h = h + h.T
        k = rng.normal(size=(4, 4)); k = k + k.T
        Rr += KN(h, k)
    return Rr
ny = max(abs(np.einsum('abcd,abcd->', eps4, randR())) for _ in range(300))
chk("P4 e^a e^b R_ab (the torsion-free part of the Nieh-Yan 4-form) ~ eps^{abcd} R_{abcd} = 0 on 300 random curvature tensors (max %.1e): first Bianchi" % ny, ny < 1e-9)
Rbad = randR() + 0.1 * rng.normal(size=(4, 4, 4, 4))
chk("P4-control: a tensor violating the first Bianchi identity gives eps^{abcd} R_{abcd} != 0", abs(np.einsum('abcd,abcd->', eps4, Rbad)) > 1e-3)

# ---------------------------------------------------------------- P5: Eguchi-Hanson, size a is a free modulus
r, th, ph, ps, a = sp.symbols('r theta phi psi a', positive=True)
X = [r, th, ph, ps]
f = 1 - a ** 4 / r ** 4
g = sp.zeros(4, 4)
g[0, 0] = 1 / f
g[1, 1] = r ** 2 / 4
g[2, 2] = r ** 2 / 4 * (sp.sin(th) ** 2 + f * sp.cos(th) ** 2)
g[2, 3] = g[3, 2] = r ** 2 / 4 * f * sp.cos(th)
g[3, 3] = r ** 2 / 4 * f
sqrtg = r ** 3 * sp.sin(th) / 8
chk("P5 det g = r^6 sin^2(theta)/64, i.e. sqrt(g) = r^3 sin(theta)/8 (independent of a)", sp.simplify(g.det() - sqrtg ** 2) == 0)
ginv = g.inv()
Gam = [[[sum(ginv[i, l] * (sp.diff(g[l, j], X[k]) + sp.diff(g[l, k], X[j]) - sp.diff(g[j, k], X[l])) for l in range(4)) / 2 for k in range(4)] for j in range(4)] for i in range(4)]
def Rm(i, j, k, l):
    return sp.diff(Gam[i][j][l], X[k]) - sp.diff(Gam[i][j][k], X[l]) + sum(Gam[i][k][m] * Gam[m][j][l] - Gam[i][l][m] * Gam[m][j][k] for m in range(4))
Rup = [[[[Rm(i, j, k, l) for l in range(4)] for k in range(4)] for j in range(4)] for i in range(4)]
pt = {r: sp.Rational(23, 10), th: sp.Rational(7, 10), a: sp.Rational(3, 2)}
pt2 = {r: sp.Rational(41, 10), th: sp.Rational(11, 10), a: sp.Rational(3, 2)}
def numeric_curv(pt_):
    Rn = np.array([[[[float(Rup[i][j][k][l].subs(pt_)) for l in range(4)] for k in range(4)] for j in range(4)] for i in range(4)])
    gn = np.array(g.subs(pt_).tolist(), dtype=float); gin = np.linalg.inv(gn)
    Rl = np.einsum('im,mjkl->ijkl', gn, Rn)                              # R_{ijkl}
    Ric = np.einsum('ijil->jl', Rn)
    Rs = np.einsum('jl,jl->', gin, Ric)
    Rl_up = np.einsum('ijkl,ia,jb,kc,ld->abcd', Rl, gin, gin, gin, gin)
    riem2 = np.einsum('ijkl,ijkl->', Rl, Rl_up)
    ric2 = np.einsum('ij,kl,ik,jl->', Ric, Ric, gin, gin)
    sg = float(sqrtg.subs(pt_))
    epsL = eps4 / sg                                                      # tensor epsilon_{abcd} (all lower); eps^{abcd} via inverse metric below
    # (1/2) eps^{mnpq} R_{mn}^{ab} R_{pq ab}, eps^{mnpq} = eps4/sqrt(g)
    Rmix = np.einsum('mnab,ac,bd->mncd', Rl, gin, gin)                    # R_{mn}^{cd}
    pont = 0.5 * np.einsum('mnpq,mncd,pqcd->', eps4, Rmix, Rl) / sg
    return riem2, ric2, Rs, pont
rr = []
for p_ in (pt, pt2):
    riem2, ric2, Rs, pont = numeric_curv(p_)
    exact = 384 * float(p_[a]) ** 8 / float(p_[r]) ** 12
    rr.append((riem2, ric2, Rs, pont, exact))
    print("   EH at r=%.1f: Riem^2 = %.8g (384 a^8/r^12 = %.8g), Ric^2 = %.1e, R = %.1e, R R~ = %.8g" % (float(p_[r]), riem2, exact, ric2, Rs, pont))
chk("P5 Eguchi-Hanson is Ricci flat and Riem^2 = 384 a^8/r^12 at two points (E4 = Riem^2)", all(abs(x[0] - x[4]) < 1e-9 * x[4] and abs(x[1]) < 1e-9 and abs(x[2]) < 1e-9 for x in rr))
chk("P5 Pontryagin density R R~ = -+ Riem^2 (Weyl self-dual/anti-self-dual, sign = orientation) at two points", all(abs(abs(x[3]) - x[4]) < 1e-8 * x[4] for x in rr))
angvol = 8 * sp.pi ** 2               # int sin(theta) dtheta dphi dpsi over theta in [0,pi], phi in [0,2pi], psi in [0,2pi) (Z_2 quotient)
IE = sp.simplify(angvol / 8 * sp.integrate(384 * a ** 8 * r ** 3 / r ** 12, (r, a, sp.oo)))
chk("P5 Int E4 = 48 pi^2 = 32 pi^2 (3/2) for EVERY a (chi = 2 = 3/2 + 1/2 with the Z_2 boundary term): the size a is scale-free, like rho on S^4", sp.simplify(IE - 48 * sp.pi ** 2) == 0 and sp.diff(IE, a) == 0)
IEwrong = sp.simplify(angvol / 8 * sp.integrate(384 * a ** 8 * r ** 3 / r ** 11, (r, a, sp.oo)))
chk("P5-control: with a wrong radial power (r^-11 instead of r^-12) the integral depends on a (test can fail)", sp.diff(IEwrong, a) != 0)

# ---------------------------------------------------------------- P6: the level K
K = L ** 2 / (4 * hb * G)
S_dS = sp.pi * L ** 2 / (hb * G)
chk("P6 chiral instanton action per unit charge = S_dS/2 = 2 pi K  =>  K = S_dS/(4 pi) = L^2/(4 hbar G) = 3/(4 hbar G Lambda)  (Lambda = 3/L^2)",
    sp.simplify(S_dS / 2 - 2 * sp.pi * K) == 0 and sp.simplify(K.subs(L, sp.sqrt(3 / Lam)) - 3 / (4 * hb * G * Lam)) == 0)
Pi2 = hb * G * Lam
chk("P6 K = 3/(4 Pi_2) depends on Pi_2 = hbar G Lambda only; observed Pi_2 ~ 3e-122 gives K ~ 3e121 (lattice spacing 1/K ~ 3e-122 in Pi_2 units)",
    sp.simplify(K.subs(L, sp.sqrt(3 / Lam)) - sp.Rational(3, 4) / Pi2) == 0 and 3 / (4 * 2.87e-122) > 1e121)
chk("P6-control: with a wrong per-unit-charge action S_dS/3 the level would differ from 3/(4 hbar G Lambda) (the check can fail)",
    sp.simplify((S_dS / 3) / (2 * sp.pi) - K) != 0)
print("\n   dimension table (c = 1; [length] = 1/acceleration):  alpha_EGB: length^2 (free);  ell in F = R - e e/ell^2: length (fixed to L by stationarity, P2);")
print("   theta_E, theta_P (Euler/Pontryagin), 1/gamma (Holst/Nieh-Yan; inert for T = 0): dimensionless;  K = 3/(4 hbar G Lambda): dimensionless, Planck units.  a0 appears in none.")
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
