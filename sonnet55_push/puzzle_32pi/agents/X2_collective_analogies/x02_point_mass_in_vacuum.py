#!/usr/bin/env python3
"""x02_point_mass_in_vacuum.py -- static point-mass potential in a medium of density rho_Lambda with p = -rho (Kottler / Schwarzschild-de Sitter),
and what a small non-zero response (rho + p != 0) would do.  c = 1.  Lambda = 8 pi G rho_Lambda.

Claims (each with a control that must FAIL):
 E1  SdS metric is an exact solution of G_mn + Lambda g_mn = 0 (r > 0);  control: wrong Lambda coefficient fails
 E2  O(M) part: d/d(eps) [G_mn + Lambda g_mn] = 0 for f_eps = 1 - Lambda r^2/3 - 2 eps G M/r.  The vacuum's exact linear response is the
     covariant contact term delta T_mn = -rho_Lambda h_mn (delta rho = delta p = 0): without it the linearised equation is violated by exactly -Lambda h_mn.
     ==> the point-mass field is  Phi = -GM/r - Lambda r^2/6  with the 1/r term UNMODIFIED (no screening, no anti-screening).
 E3  exact TOV: rho = const, p = -rho gives Phi' = (m + 4 pi r^3 p)/(r(r-2m)) consistent with m = M + (4 pi/3) rho r^3 and p' = -(rho+p) Phi' = 0 identically
 E4  the vacuum background field is -2 x the field the same density would have as dust: Phi_Lambda = -(4 pi/3) G rho r^2 vs +(2 pi/3) G rho r^2
 E5  small departure rho + p = eps rho != 0: hydrostatic response (c_s^2 delta rho = -(rho+p) phi) + Poisson gives (nabla^2 + k_J^2) phi = 4 pi G M delta^3,
     k_J^2 = 4 pi G (rho+p)/c_s^2 (the x01 result); Green's functions verified:  c_s^2 > 0: phi = -GM cos(kr)/r (anti-screening / Jeans swindle),
     c_s^2 < 0: phi = -GM exp(-m r)/r (Yukawa screening), and both reduce to -GM/r as (rho+p) -> 0
 E6  linear response => the force is exactly linear in M (d ln g / d ln M = 1); a MOND-like 1/r force has d ln g / d ln M = 1/2 (deep MOND) -- the far-field
     'envelope' of the anti-screened force IS a 1/r force (amplitude G M k) but oscillates in sign and is linear in M
 E7  inventory of the exact numbers fixed by p = -rho (no chosen input): rho+p = 0, (rho+3p)/rho = -2, c_s^2 = w = -1, H^2/(4 pi G rho) = 2/3
Exit 0 = all pass.
"""
import mpmath as mp
import sympy as sp
from common import Ledger

L = Ledger("x02")
ck, must = L.check, L.must_fail

t, r, th, ph = sp.symbols("t r theta phi", real=True)
G, M, Lam, eps = sp.symbols("G M Lambda epsilon", positive=True)
X = [t, r, th, ph]


def einstein_plus_lambda(gmat, lam):
    """G_mn + lam g_mn for a diagonal metric depending on (r, theta): Christoffels -> Ricci -> Einstein."""
    ginv = gmat.inv()
    n = 4
    Gam = [[[sum(ginv[i, l] * (sp.diff(gmat[l, j], X[kk]) + sp.diff(gmat[l, kk], X[j]) - sp.diff(gmat[j, kk], X[l])) for l in range(n)) / 2
             for kk in range(n)] for j in range(n)] for i in range(n)]
    def Riem(i, j, kk, l):     # R^i_{j k l}
        return (sp.diff(Gam[i][j][l], X[kk]) - sp.diff(Gam[i][j][kk], X[l])
                + sum(Gam[i][kk][m] * Gam[m][j][l] - Gam[i][l][m] * Gam[m][j][kk] for m in range(n)))
    Ric = sp.Matrix(n, n, lambda j, l: sum(Riem(i, j, i, l) for i in range(n)))
    Rs = sum(ginv[i, j] * Ric[i, j] for i in range(n) for j in range(n))
    return (Ric - Rs * gmat / 2 + lam * gmat).applyfunc(sp.simplify)


def metric(f):
    return sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th)**2)


print("E1  Schwarzschild-de Sitter (Kottler) is an exact vacuum + Lambda solution")
f0 = 1 - 2 * G * M / r - Lam * r**2 / 3
E_sds = einstein_plus_lambda(metric(f0), Lam)
ck("E1a  G_mn + Lambda g_mn = 0 for f = 1 - 2GM/r - Lambda r^2/3", E_sds == sp.zeros(4, 4))
f_bad = 1 - 2 * G * M / r - Lam * r**2 / 2
E_bad = einstein_plus_lambda(metric(f_bad), Lam)
must("E1b-mut  f = 1 - 2GM/r - Lambda r^2/2 is also a solution", E_bad == sp.zeros(4, 4))

print("\nE2  the O(M) part, and the vacuum's exact linear response")
feps = 1 - Lam * r**2 / 3 - 2 * eps * G * M / r
gam = metric(feps)
Efull = einstein_plus_lambda(gam, Lam)
dE = Efull.applyfunc(lambda e: sp.simplify(sp.diff(e, eps).subs(eps, 0)))
ck("E2a  d/d(eps)[G_mn + Lambda g_mn] = 0 at eps = 0 : the linear-in-M perturbation solves the vacuum + Lambda equations", dE == sp.zeros(4, 4))
# the same linearisation WITHOUT letting the vacuum stress co-vary with the metric (drop the Lambda h_mn term): residual is -Lambda h_mn
Efull_noresp = einstein_plus_lambda(gam, 0)
dE_noresp = Efull_noresp.applyfunc(lambda e: sp.simplify(sp.diff(e, eps).subs(eps, 0)))
h = (gam.applyfunc(lambda e: sp.diff(e, eps))).subs(eps, 0)
ck("E2b  delta G_mn = -Lambda h_mn exactly  (so the vacuum's linear response must be delta T_mn = -rho_Lambda h_mn, i.e. delta rho = delta p = 0)",
   (dE_noresp + Lam * h).applyfunc(sp.simplify) == sp.zeros(4, 4))
must("E2c-mut  delta G_mn = -(3/2) Lambda h_mn (a different vacuum susceptibility)", (dE_noresp + sp.Rational(3, 2) * Lam * h).applyfunc(sp.simplify) == sp.zeros(4, 4))
Phi_full = sp.simplify((f0 - 1) / 2)
ck("E2d  Phi = (f-1)/2 = -GM/r - Lambda r^2/6: the 1/r term carries coefficient exactly 1 (GM), independent of Lambda",
   sp.simplify(Phi_full - (-G * M / r - Lam * r**2 / 6)) == 0 and sp.simplify(sp.limit(-Phi_full * r, r, 0)) == G * M)

print("\nE3  exact TOV with rho = const, p = -rho")
rho = sp.symbols("rho", positive=True)
m_of_r = M * G + sp.Rational(4, 3) * sp.pi * rho * G * r**3      # geometric mass function G m
pp = -rho
Phi_p = (m_of_r + 4 * sp.pi * G * r**3 * pp) / (r * (r - 2 * m_of_r))
fS = 1 - 2 * m_of_r / r
ck("E3a  Phi' from TOV equals (1/2) d ln f/dr for f = 1 - 2 G m(r)/r  (consistent static metric)", sp.simplify(Phi_p - sp.diff(sp.log(fS), r) / 2) == 0)
ck("E3b  hydrostatic equation p' = -(rho+p) Phi' is satisfied identically (0 = 0): the pressure is unconstrained by the potential when rho + p = 0",
   sp.simplify(sp.diff(pp, r) + (rho + pp) * Phi_p) == 0)
ck("E3c  f = 1 - 2GM/r - (8 pi/3) G rho r^2 = SdS with Lambda = 8 pi G rho", sp.simplify(fS - (1 - 2 * G * M / r - (8 * sp.pi / 3) * G * rho * r**2)) == 0)

print("\nE4  background field of the vacuum vs. the same density as dust")
Phi_dust = sp.Rational(2, 3) * sp.pi * G * rho * r**2          # nabla^2 Phi = 4 pi G rho
Phi_vac = -sp.Rational(4, 3) * sp.pi * G * rho * r**2          # nabla^2 Phi = 4 pi G (rho + 3p) = -8 pi G rho
lap = lambda P: sp.simplify(sp.diff(r**2 * sp.diff(P, r), r) / r**2)
ck("E4a  laplacian Phi_dust = 4 pi G rho,  laplacian Phi_vac = -8 pi G rho", sp.simplify(lap(Phi_dust) - 4 * sp.pi * G * rho) == 0
   and sp.simplify(lap(Phi_vac) + 8 * sp.pi * G * rho) == 0)
ck("E4b  Phi_vac / Phi_dust = -2 = (rho+3p)/rho: the Newtonian 'Jeans swindle' background subtraction is exact and sign-reversed for the vacuum",
   sp.simplify(Phi_vac / Phi_dust + 2) == 0)

print("\nE5  small departure from p = -rho: hydrostatic + Poisson response")
kk, mm, Gm = sp.symbols("k m GM", positive=True)
phi_osc = -Gm * sp.cos(kk * r) / r
phi_yuk = -Gm * sp.exp(-mm * r) / r
lap_r = lambda P: sp.simplify(sp.diff(r**2 * sp.diff(P, r), r) / r**2)
ck("E5a  (nabla^2 + k^2)(-GM cos(kr)/r) = 0 for r > 0,  r^2 phi' -> +GM as r -> 0 (point source 4 pi G M delta^3)",
   sp.simplify(lap_r(phi_osc) + kk**2 * phi_osc) == 0 and sp.limit(r**2 * sp.diff(phi_osc, r), r, 0) == Gm)
ck("E5b  (nabla^2 - m^2)(-GM exp(-mr)/r) = 0 for r > 0,  r^2 phi' -> +GM as r -> 0",
   sp.simplify(lap_r(phi_yuk) - mm**2 * phi_yuk) == 0 and sp.limit(r**2 * sp.diff(phi_yuk, r), r, 0) == Gm)
must("E5c-mut  cos(kr) with the wrong sign, (nabla^2 - k^2), also solves it", sp.simplify(lap_r(phi_osc) - kk**2 * phi_osc) == 0)
ck("E5d  as k -> 0 (rho + p -> 0) or m -> 0 both potentials reduce to -GM/r", sp.limit(phi_osc, kk, 0) == -Gm / r and sp.limit(phi_yuk, mm, 0) == -Gm / r)
g_osc = sp.simplify(sp.diff(phi_osc, r))      # inward (attractive) magnitude g = +d phi/dr
g_yuk = sp.simplify(sp.diff(phi_yuk, r))
ck("E5e  forces: g_osc = GM[cos(kr)/r^2 + k sin(kr)/r],  g_yuk = GM (1 + m r) e^{-m r}/r^2",
   sp.simplify(g_osc - Gm * (sp.cos(kk * r) / r**2 + kk * sp.sin(kk * r) / r)) == 0 and sp.simplify(g_yuk - Gm * (1 + mm * r) * sp.exp(-mm * r) / r**2) == 0)
env = sp.simplify((g_osc * r / (Gm * kk)))
ck("E5f  anti-screened force: r g/(GM k) = sin(kr) + cos(kr)/(kr): a 1/r force with envelope amplitude G M k, oscillating in sign (zero mean)",
   sp.simplify(env - (sp.sin(kk * r) + sp.cos(kk * r) / (kk * r))) == 0)
rp, cs2s = sp.symbols("rho_plus_p cs2_abs", positive=True)          # rho + p > 0 ; |c_s^2|
# hydrostatic response: c_s^2 delta rho = -(rho+p) phi  (from grad delta p = -(rho+p) grad phi, delta p = c_s^2 delta rho); Poisson: lap phi = 4 pi G delta rho (r > 0)
drho_pos = -rp * phi_osc / cs2s                                       # c_s^2 = +|c_s^2|
drho_neg = -rp * phi_yuk / (-cs2s)                                    # c_s^2 = -|c_s^2|
res_pos = sp.simplify((lap_r(phi_osc) - 4 * sp.pi * G * drho_pos).subs(kk, sp.sqrt(4 * sp.pi * G * rp / cs2s)))
res_neg = sp.simplify((lap_r(phi_yuk) - 4 * sp.pi * G * drho_neg).subs(mm, sp.sqrt(4 * sp.pi * G * rp / cs2s)))
ck("E5g  Poisson + hydrostatic response is solved by phi_osc with k^2 = 4 pi G (rho+p)/c_s^2 (c_s^2 > 0) and by phi_yuk with m^2 = 4 pi G (rho+p)/|c_s^2| (c_s^2 < 0)",
   res_pos == 0 and res_neg == 0)
res_wrong = sp.simplify((lap_r(phi_osc) - 4 * sp.pi * G * drho_pos).subs(kk, sp.sqrt(4 * sp.pi * G * rp * 2 / cs2s)))
must("E5h-mut  k^2 = 8 pi G (rho+p)/c_s^2 also solves it", res_wrong == 0)

print("\nE6  mass scaling of the force: linear response vs MOND")
mp.mp.dps = 30
a0v, kv, rv = mp.mpf("0.7"), mp.mpf("1.3"), mp.mpf("5.0")


def gfun_osc(Mv):
    return Mv * (mp.cos(kv * rv) / rv**2 + kv * mp.sin(kv * rv) / rv)


def gfun_yuk(Mv):
    return Mv * (1 + kv * rv) * mp.e ** (-kv * rv) / rv**2


def gfun_dmond(Mv):
    return mp.sqrt(Mv * a0v) / rv


def slope(fn, Mv):
    return mp.diff(lambda x: mp.log(abs(fn(mp.e ** x))), mp.log(Mv))


ck("E6a  d ln g / d ln M = 1 for the anti-screened and Yukawa forces (linearity)", abs(slope(gfun_osc, mp.mpf(3)) - 1) < mp.mpf("1e-15") and abs(slope(gfun_yuk, mp.mpf(3)) - 1) < mp.mpf("1e-15"))
ck("E6b  d ln g / d ln M = 1/2 for deep MOND", abs(slope(gfun_dmond, mp.mpf(3)) - mp.mpf(1) / 2) < mp.mpf("1e-15"))
must("E6c-mut  the anti-screened force has slope 1/2", abs(slope(gfun_osc, mp.mpf(3)) - mp.mpf(1) / 2) < mp.mpf("1e-3"))
print("   ==> a linear-response medium gives v_flat^2 ~ M (baryonic Tully-Fisher slope 2); deep MOND has v^4 = G M a0 (slope 4).  a0 is a NONLINEARITY scale, not a susceptibility.")

print("\nE7  exact numbers fixed by p = -rho (nothing chosen)")
w = sp.symbols("w")
inv = {"rho + p": sp.simplify((1 + w).subs(w, -1)), "(rho+3p)/rho": (1 + 3 * w).subs(w, -1), "c_s^2 = w": w.subs(w, -1),
       "H^2/(4 pi G rho)": sp.simplify((sp.Rational(8, 3) * sp.pi / (4 * sp.pi)))}
for kx, vx in inv.items():
    print(f"   {kx:22s} = {vx}")
ck("E7a  the list is {0, -2, -1, 2/3}", [inv["rho + p"], inv["(rho+3p)/rho"], inv["c_s^2 = w"], inv["H^2/(4 pi G rho)"]] == [0, -2, -1, sp.Rational(2, 3)])
print("   The only response coefficient in the list that enters a static field equation with a length is (rho+p)/c_s^2 = 0 (k_J^2 = 0).  -2 sets the SIGN and size of the")
print("   Newton-Hooke background field (E4), not a length; -1 is a sound speed, not a length.  No exact number fixed by p = -rho produces a length, hence no 1/r force.")
L.finish()
