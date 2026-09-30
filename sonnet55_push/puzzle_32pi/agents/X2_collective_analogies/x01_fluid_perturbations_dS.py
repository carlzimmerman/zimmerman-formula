#!/usr/bin/env python3
"""x01_fluid_perturbations_dS.py -- linearised dynamics of a perfect fluid (w, c_s^2) on de Sitter / dust + vacuum, and what the
vacuum's own 'Jeans-like' rates are.  c = 1.  Lambda := 8 pi G rho_Lambda.  Held-fixed variable: G rho_Lambda.

Sub-horizon (k >> aH) conformal-Newtonian-gauge fluid equations (Ma-Bertschinger form with rest-frame sound speed c_s^2,
non-adiabatic terms O(H^2/k^2) dropped; psi = phi, Poisson k^2 psi = -4 pi G a^2 rho delta):
    delta' = -(1+w) theta - 3 calH (c_s^2 - w) delta
    theta' = -calH (1 - 3 c_s^2) theta + c_s^2 k^2 delta/(1+w) + k^2 psi
Written with the momentum variable v := (1+w) theta (regular at w = -1):
    delta' = -v - 3 calH (c_s^2 - w) delta
    v'     = -calH (1 - 3 c_s^2) v + c_s^2 k^2 delta - (1+w) S delta ,        S := 4 pi G a^2 rho_X
Claims (each with a control that must FAIL):
 B1  second-order form delta'' + A delta' + B delta = 0 derived symbolically; known limits: dust, radiation (Hu-Sugiyama form)
 B2  clustering-dark-energy exact solution delta_X/delta_m = (1+w)/(1-3w) for c_s = 0 in matter domination (the (1+w) factor is the one in the
     abstract of arXiv:1101.1026, opened; the ratio itself is derived here from the equations)
 B3  GRAVITY (G, i.e. S) ENTERS a fluid's own perturbation dynamics ONLY through (1+w): d(det M)/dS = -(1+w) -> 0 at w = -1.
     The frozen (calH -> 0) dispersion is omega^2 = c_s^2 k^2 - 4 pi G a^2 (rho + p), k_J^2 = 4 pi G (rho+p)/c_s^2.
 B4  the vacuum w = -1 given c_s^2 = -1 (delta p = -delta rho): gradient instability at every k with rate |k|; given c_s^2 = +1: oscillation at k; no G-scale
 C1  Heath's growth integral solves the dust-in-(dust+Lambda) equation: the vacuum enters ONLY through H; dS limit rates {0, -2H}
 C2  local exponents of a dust component in dS: s = -H + sqrt(H^2 + 4 pi G rho_c), H^2 = (2/3)(4 pi G rho_Lambda): the only place where
     (4 pi G rho_Lambda, 4 pi G rho_c) combine; s/H = -1 + sqrt(1 + 3 X/2), X = rho_c/rho_Lambda (free ratio)
 D1  vacuum active mass: 4 pi G (rho + 3p) = -8 pi G rho_Lambda = -Lambda   (NOT -2 Lambda), i.e. g_Lambda = +H^2 r (Newton-Hooke), from the metric
 D2  Einstein-static-universe (dust + Lambda) instability rate = sqrt(Lambda) at 4 pi G rho_c = Lambda (rho_c = 2 rho_Lambda)
 D3  menu consistency: menu entries V1 (H_Lambda), V2 (sqrt Lambda), V4 (omega_J), V5, V6 written in units of s = sqrt(G rho_Lambda)
Exit 0 = all pass.
"""
import mpmath as mp
import sympy as sp
from common import Ledger

L = Ledger("x01")
ck, must = L.check, L.must_fail

# ------------------------------------------------------------------------------------------------
print("\nB1  second-order equation from the first-order (delta, v) system")
calH, calHp, k, w, cs2, S, Sm = sp.symbols("calH calHp k w cs2 S S_m", real=True)
d, dp = sp.symbols("d dp")           # delta, delta'


def second_order(coupling_factor):
    """delta'' = -v' - 3 calH' (cs2-w) delta - 3 calH (cs2-w) delta'  with v eliminated. coupling_factor multiplies S in v'."""
    v = -dp - 3 * calH * (cs2 - w) * d
    vp = -calH * (1 - 3 * cs2) * v + cs2 * k**2 * d - coupling_factor * S * d
    ddp = -vp - 3 * calHp * (cs2 - w) * d - 3 * calH * (cs2 - w) * dp
    ddp = sp.expand(ddp)
    A = sp.simplify(-ddp.coeff(dp, 1))
    B = sp.simplify(-ddp.coeff(d, 1))
    return A, B


A, B = second_order(1 + w)
print("   A =", sp.factor(A))
print("   B =", sp.factor(B))
ck("B1a  adiabatic (cs2 = w): A = calH(1-3w),  B = w k^2 - (1+w) S",
   sp.simplify(A.subs(cs2, w) - calH * (1 - 3 * w)) == 0 and sp.simplify(B.subs(cs2, w) - (w * k**2 - (1 + w) * S)) == 0)
ck("B1b  dust (w = cs2 = 0): delta'' + calH delta' - S delta = 0",
   sp.simplify(A.subs({w: 0, cs2: 0}) - calH) == 0 and sp.simplify(B.subs({w: 0, cs2: 0}) + S) == 0)
ck("B1c  radiation (w = cs2 = 1/3): delta'' + (k^2/3) delta - (4/3) S delta = 0  (the Hu-Sugiyama form, S = 4 pi G a^2 rho)",
   sp.simplify(A.subs({w: sp.Rational(1, 3), cs2: sp.Rational(1, 3)})) == 0
   and sp.simplify(B.subs({w: sp.Rational(1, 3), cs2: sp.Rational(1, 3)}) - (k**2 / 3 - sp.Rational(4, 3) * S)) == 0)
Am, Bm = second_order(1)     # MUTATION: gravity coupling without the (1+w) factor
must("B1c-mut  radiation with the coupling S instead of (1+w) S gives B = k^2/3 - S  (must NOT equal the correct k^2/3 - (4/3) S)",
     sp.simplify(Bm.subs({w: sp.Rational(1, 3), cs2: sp.Rational(1, 3)}) - (k**2 / 3 - sp.Rational(4, 3) * S)) == 0)

# ------------------------------------------------------------------------------------------------
print("\nB2  clustering (c_s = 0) fluid with constant w in an Einstein-de Sitter background: exact solution delta_X = C delta_m")
eta = sp.symbols("eta", positive=True)
C = sp.symbols("C")
a_eta = eta**2                           # a proportional to eta^2 (matter domination); only calH = 2/eta matters
calH_eta = 2 / eta
delta_m = eta**2                         # growing mode delta_m proportional to a
S_m = sp.Rational(3, 2) * calH_eta**2    # 4 pi G a^2 rho_m = (3/2) calH^2
ck("B2a  dust growing mode delta_m ~ a solves delta'' + calH delta' - (3/2) calH^2 delta = 0",
   sp.simplify(sp.diff(delta_m, eta, 2) + calH_eta * sp.diff(delta_m, eta) - S_m * delta_m) == 0)
delta_X = C * delta_m
vX = -(sp.diff(delta_X, eta) + 3 * calH_eta * (0 - w) * delta_X)          # v from delta' eq with cs2 = 0
eq_v = sp.diff(vX, eta) - (-calH_eta * (1 - 0) * vX + 0 - (1 + w) * S_m * delta_m)   # v' equation (X is a test fluid; potential from dust)
Csol = sp.solve(sp.simplify(eq_v / eta), C)
print("   solving v' equation for C:", Csol)
ck("B2b  C = (1+w)/(1-3w)", len(Csol) == 1 and sp.simplify(Csol[0] - (1 + w) / (1 - 3 * w)) == 0)
Csol_mut = sp.solve(sp.simplify((sp.diff(-(sp.diff(C * delta_m, eta) + 3 * calH_eta * (0 - w) * C * delta_m), eta)
                                 - (-calH_eta * (-(sp.diff(C * delta_m, eta) + 3 * calH_eta * (0 - w) * C * delta_m))
                                    - S_m * delta_m)) / eta), C)      # MUTATION: no (1+w) in the coupling
print("   mutated coupling (no (1+w)) gives C =", Csol_mut)
must("B2c-mut  with the coupling lacking (1+w) the ratio would not vanish at w = -1; the mutated C must differ from (1+w)/(1-3w)",
     len(Csol_mut) == 1 and sp.simplify(Csol_mut[0] - (1 + w) / (1 - 3 * w)) == 0)
ck("B2d  w = 0 gives C = 1 (dust follows dust) and w = -1 gives C = 0 (the vacuum does not cluster)",
   sp.simplify(Csol[0].subs(w, 0) - 1) == 0 and sp.simplify(Csol[0].subs(w, -1)) == 0)

# ------------------------------------------------------------------------------------------------
print("\nB3  where does gravity enter?  matrix M of (delta, v):  d/deta (delta, v) = M (delta, v)")
M = sp.Matrix([[-3 * calH * (cs2 - w), -1], [cs2 * k**2 - (1 + w) * S, -calH * (1 - 3 * cs2)]])
detM = sp.expand(M.det())
ck("B3a  d(det M)/dS = -(1+w)", sp.simplify(sp.diff(detM, S) + (1 + w)) == 0)
ck("B3b  at w = -1 the whole matrix is independent of S (= 4 pi G a^2 rho): the vacuum's own perturbations feel no self-gravity",
   sp.simplify(sp.diff(M.subs(w, -1), S)) == sp.zeros(2, 2))
Mm = sp.Matrix([[-3 * calH * (cs2 - w), -1], [cs2 * k**2 - S, -calH * (1 - 3 * cs2)]])
must("B3b-mut  mutated coupling (no (1+w)) would keep S in the vacuum matrix", sp.simplify(sp.diff(Mm.subs(w, -1), S)) == sp.zeros(2, 2))
om2 = sp.simplify(detM.subs(calH, 0))
ck("B3c  frozen (calH -> 0) dispersion omega^2 = det M = c_s^2 k^2 - (1+w) S", sp.simplify(om2 - (cs2 * k**2 - (1 + w) * S)) == 0)
kJ2 = sp.solve(sp.Eq(om2, 0), k**2)[0]
ck("B3d  marginal wavenumber k_J^2 = (1+w) S / c_s^2 = 4 pi G a^2 (rho+p)/c_s^2", sp.simplify(kJ2 - (1 + w) * S / cs2) == 0)
print("   ==> k_J^2 = 4 pi G (rho+p)/c_s^2 :  the 'gravitational plasma frequency' of a fluid is 4 pi G (rho+p), not 4 pi G rho.")
print("       For the vacuum rho + p = 0 EXACTLY: no Jeans frequency, no Jeans/Debye length; 4 pi G rho_Lambda is not an eigenfrequency of anything in the vacuum.")

# ------------------------------------------------------------------------------------------------
print("\nB4  the vacuum as a fluid: (w = -1) with a chosen sound speed; no rate involves G")
lam = sp.symbols("lam")
for cs2v, name in [(-1, "c_s^2 = -1 (delta p = -delta rho, the barotropic vacuum)"), (1, "c_s^2 = +1 (k-essence-like)")]:
    Mv = M.subs({w: -1, cs2: cs2v, calH: 0})
    ev = sp.solve(sp.Eq(Mv.charpoly(lam).as_expr(), 0), lam)
    print(f"   {name}: eigenvalues at calH -> 0:", ev)
ev_m1 = sp.solve(sp.Eq(M.subs({w: -1, cs2: -1, calH: 0}).charpoly(lam).as_expr(), 0), lam)
ev_p1 = sp.solve(sp.Eq(M.subs({w: -1, cs2: 1, calH: 0}).charpoly(lam).as_expr(), 0), lam)
ck("B4a  c_s^2 = -1: eigenvalues +-k (real: exponential growth at EVERY wavenumber, ill-posed; no acceleration scale)",
   sorted([sp.simplify(e**2 - k**2) for e in ev_m1]) == [0, 0])
ck("B4b  c_s^2 = +1: eigenvalues +-i k (oscillation, no G, no scale)", sorted([sp.simplify(e**2 + k**2) for e in ev_p1]) == [0, 0])
ck("B4c  neither contains S (G rho)", all(not e.has(S) for e in ev_m1 + ev_p1))

# ------------------------------------------------------------------------------------------------
print("\nC1  Heath growth integral: dust in dust + Lambda; the vacuum enters only through H(a)")
mp.mp.dps = 30
a_, Isym = sp.symbols("a_ I_", positive=True)
Om = sp.Rational(3, 10)
E = sp.sqrt(Om * a_**-3 + (1 - Om))
Ip = 1 / (a_ * E) ** 3


def tot(expr):                                   # total derivative with dI/da = 1/(aE)^3
    return sp.diff(expr, a_) + sp.diff(expr, Isym) * Ip


Dg = sp.Rational(5, 2) * Om * E * Isym
resid = tot(tot(Dg)) + (3 / a_ + sp.diff(E, a_) / E) * tot(Dg) - sp.Rational(3, 2) * Om / (a_**5 * E**2) * Dg
resid_mut = tot(tot(Dg)) + (3 / a_ + sp.diff(E, a_) / E) * tot(Dg) - 1 * Om / (a_**5 * E**2) * Dg
resid_f = sp.lambdify((a_, Isym), resid, "mpmath")
resid_mut_f = sp.lambdify((a_, Isym), resid_mut, "mpmath")
Ef = sp.lambdify(a_, E, "mpmath")
worst, worst_mut = mp.mpf(0), mp.mpf(0)
for av in [mp.mpf("0.1"), mp.mpf("0.4"), mp.mpf("0.9"), mp.mpf("1.7")]:
    Iv = mp.quad(lambda x: 1 / (x * Ef(x)) ** 3, [0, av])
    worst = max(worst, abs(resid_f(av, Iv)))
    worst_mut = max(worst_mut, abs(resid_mut_f(av, Iv)))
print(f"   max |residual| (correct 3/2 coefficient) = {mp.nstr(worst, 3)};  with 1 instead of 3/2: {mp.nstr(worst_mut, 3)}")
ck("C1a  Heath D(a) = (5/2) Om H(a) int da/(aH)^3 satisfies D'' + (3/a + E'/E) D' - (3/2) Om a^-5 E^-2 D = 0 (|res| < 1e-20)", worst < mp.mpf("1e-20"))
must("C1b-mut  the same D with coefficient 1 instead of 3/2 has residual < 1e-3", worst_mut < mp.mpf("1e-3"))
Hh = sp.symbols("Hh", positive=True)
tt = sp.symbols("t")
ck("C1c  pure dS (Om -> 0, H const): delta'' + 2H delta' = 0 has exponents {0, -2H}: growth frozen (delta = const, e^{-2Ht})",
   sorted(sp.solve(sp.symbols("s") ** 2 + 2 * Hh * sp.symbols("s"), sp.symbols("s"))) == sorted([0, -2 * Hh]))

print("\nC2  local exponents of a dust component in dust + vacuum: delta'' + 2H delta' - 4 pi G rho_c delta = 0 (frozen coefficients)")
s = sp.symbols("s")
Gr_L = sp.symbols("Grho_L", positive=True)         # G rho_Lambda
Xr = sp.symbols("X", positive=True)                # rho_c / rho_Lambda
H2 = sp.Rational(8, 3) * sp.pi * Gr_L              # H_Lambda^2 = (8 pi/3) G rho_Lambda
four_pi_Grho_c = 4 * sp.pi * Gr_L * Xr
sols = sp.solve(s**2 + 2 * sp.sqrt(H2) * s - four_pi_Grho_c, s)
sp_plus = [e for e in sols if sp.simplify(e.subs({Xr: 1, Gr_L: 1})) > 0][0]
ck("C2a  s+/H = -1 + sqrt(1 + 3X/2)  with X = rho_c/rho_Lambda", sp.simplify(sp_plus / sp.sqrt(H2) - (-1 + sp.sqrt(1 + sp.Rational(3, 2) * Xr))) == 0)
ck("C2b  X = 0: s+ = 0 (frozen); X = 2: s+ = H exactly (rate H); X -> large: s+ -> sqrt(4 pi G rho_c)",
   sp.simplify((sp_plus / sp.sqrt(H2)).subs(Xr, 0)) == 0 and sp.simplify((sp_plus / sp.sqrt(H2)).subs(Xr, 2)) == 1
   and sp.limit(sp_plus / sp.sqrt(four_pi_Grho_c), Xr, sp.oo) == 1)
print("   ==> the exponent depends on the free ratio X = rho_c/rho_Lambda; there is no X-independent combination of 4 pi G rho_c and 4 pi G rho_Lambda that is a rate.")
print("       For X = 2 (rho_c = 2 rho_Lambda: mean density at the zero-gravity radius) s+ = H_Lambda = sqrt(8 pi/3) sqrt(G rho_Lambda) = 5.79 a0.")

# ------------------------------------------------------------------------------------------------
print("\nD1  active gravitational mass of the vacuum and Newton-Hooke acceleration")
rho, p, G, Lam, r_, t_, th_, ph_ = sp.symbols("rho p G Lambda r t theta phi", positive=True)
Lam_expr = 8 * sp.pi * G * rho                     # Lambda = 8 pi G rho_Lambda
src = 4 * sp.pi * G * (rho + 3 * (-rho))
ck("D1a  4 pi G (rho + 3p) at p = -rho equals -8 pi G rho_Lambda = -Lambda   (the task's '-2 Lambda' is a slip: it would need Lambda = 4 pi G rho)",
   sp.simplify(src + Lam_expr) == 0)
must("D1a-mut  4 pi G (rho+3p) = -2 Lambda with Lambda = 8 pi G rho", sp.simplify(src + 2 * Lam_expr) == 0)
Hs = sp.sqrt(Lam_expr / 3)
f = 1 - Hs**2 * r_**2                                # static patch g_tt = -f
Phi = sp.simplify((f - 1) / 2)                       # g_tt = -(1+2Phi) = -f  ->  Phi = -H^2 r^2/2
gvec = sp.simplify(-sp.diff(Phi, r_))                # acceleration = -dPhi/dr
ck("D1b  static patch: Phi = -H^2 r^2/2, acceleration g = +H^2 r (repulsive, Newton-Hooke), H^2 = Lambda/3 = 8 pi G rho_Lambda/3",
   sp.simplify(gvec - Hs**2 * r_) == 0)
lap = sp.simplify(sp.diff(r_**2 * sp.diff(Phi, r_), r_) / r_**2)
ck("D1c  Poisson: laplacian Phi = -3 H^2 = -Lambda = 4 pi G (rho + 3p) at p = -rho", sp.simplify(lap + Lam_expr) == 0)

print("\nD2  Einstein static universe (dust + Lambda) instability rate")
aa, a0E, rc0 = sp.symbols("aa a0E rc0", positive=True)
Lam_s = sp.symbols("Lam_s", positive=True)
addot = -sp.Rational(4, 3) * sp.pi * G * rc0 * a0E**3 / aa**2 + Lam_s * aa / 3     # d^2a/dt^2 = -(4 pi G/3) rho_c a + Lambda a/3, rho_c = rc0 (a0E/a)^3
static_cond = sp.solve(sp.Eq(addot.subs(aa, a0E), 0), rc0)[0]                        # 4 pi G rho_c = Lambda
ck("D2a  static condition 4 pi G rho_c = Lambda  (rho_c = 2 rho_Lambda)", sp.simplify(static_cond * 4 * sp.pi * G - Lam_s) == 0)
rate2 = sp.simplify(sp.diff(addot, aa).subs(aa, a0E).subs(rc0, static_cond) )
ck("D2b  linearised d^2 (delta a)/dt^2 = Lambda delta a: instability rate sqrt(Lambda)  (Eddington)", sp.simplify(rate2 - Lam_s) == 0)
print("   note: only the homogeneous mode of the static universe; Kiessling's justification of the Jeans swindle (astro-ph/9910247, abstract opened)")
print("   uses a static universe with a cosmological constant; that the matching relation is Lambda = 4 pi G rho_c is derived here, not read from that abstract.")

# ------------------------------------------------------------------------------------------------
print("\nD4  where sqrt(2 Lambda) (menu V3, task-listed) lives: the Nariai limit of Schwarzschild-de Sitter (G = 1)")
rN_, MN_ = 1 / sp.sqrt(Lam_s), 1 / (3 * sp.sqrt(Lam_s))
Msym, xx = sp.symbols("Msym xx", positive=True)
fN = 1 - 2 * Msym / r_ - Lam_s * r_**2 / 3
ck("D4a  Nariai point: f(r_N) = f'(r_N) = 0 at r_N = 1/sqrt(Lambda), M_N = 1/(3 sqrt(Lambda)); f''(r_N) = -2 Lambda",
   sp.simplify(fN.subs({Msym: MN_, r_: rN_})) == 0 and sp.simplify(sp.diff(fN, r_).subs({Msym: MN_, r_: rN_})) == 0
   and sp.simplify(sp.diff(fN, r_, 2).subs({Msym: MN_, r_: rN_}) + 2 * Lam_s) == 0)
# Kantowski-Sachs side (f < 0, r is time): dr/dtau = sqrt(-f)  =>  d^2 r/dtau^2 = -f'(r)/2  ; linearise about r_N
ks_rate2 = sp.simplify(-sp.diff(fN, r_, 2).subs({Msym: MN_, r_: rN_}) / 2)
ck("D4b  KS linearisation d^2(delta r)/dtau^2 = -(f''/2) delta r = Lambda delta r: growth rate sqrt(Lambda) (= menu V2, not V3)", sp.simplify(ks_rate2 - Lam_s) == 0)
must("D4b-mut  growth rate^2 = 2 Lambda", sp.simplify(ks_rate2 - 2 * Lam_s) == 0)
# dS2 side (f > 0): F = f near r_N is F = eps0 - Lambda x^2 ; the static solution delta r = x of the radius fluctuation obeys  box x = (F x')' = F' = -2 Lambda x
eps0 = sp.symbols("eps0", positive=True)
Fdes = eps0 - Lam_s * xx**2
box_x = sp.diff(Fdes * sp.diff(xx, xx), xx)
ck("D4c  on dS_2 (F = eps0 - Lambda x^2, curvature radius 1/sqrt(Lambda)) the static radius perturbation delta r = x obeys box(delta r) = -2 Lambda delta r: tachyon |m| = sqrt(2 Lambda) (= menu V3)",
   sp.simplify(box_x + 2 * Lam_s * xx) == 0)
must("D4c-mut  box(delta r) = -Lambda delta r", sp.simplify(box_x + Lam_s * xx) == 0)
print("   ==> sqrt(2 Lambda) is the tachyonic MASS of the Nariai radius mode (m^2 = -2 Lambda on dS_2); its growth RATE is sqrt(Lambda) (dS_2: Delta(1-Delta) = m^2/H_2^2 = -2 => growing exponent H_2 = sqrt(Lambda)).")
print("      Both are algebraic multiples of H_Lambda: V2 = sqrt(3) H_Lambda, V3 = sqrt(6) H_Lambda.")

print("\nD3  menu entries in units of s = sqrt(G rho_Lambda)")
sdim = sp.symbols("sdim", positive=True)
Lam_u = 8 * sp.pi                                     # Lambda / s^2
menu_check = {
    "V1 H_Lambda": sp.sqrt(Lam_u / 3),
    "V2 sqrt(Lambda)": sp.sqrt(Lam_u),
    "V4 omega_J": sp.sqrt(4 * sp.pi),
    "V5 sqrt(4 pi/3)": sp.sqrt(4 * sp.pi / 3),
    "V6 1/t_ff": sp.sqrt(32 / (3 * sp.pi)),
}
ck("D3a  V1 = sqrt(8 pi/3) s, V2 = sqrt(8 pi) s, V4 = 2 sqrt(pi) s (as used in x04)",
   sp.simplify(menu_check["V1 H_Lambda"] - sp.sqrt(8 * sp.pi / 3)) == 0 and sp.simplify(menu_check["V2 sqrt(Lambda)"] - 2 * sp.sqrt(2 * sp.pi)) == 0
   and sp.simplify(menu_check["V4 omega_J"] - 2 * sp.sqrt(sp.pi)) == 0)
tff_alt = (sp.pi / 2) / sp.sqrt(8 * sp.pi / 3)        # t_ff = (pi/2)/sqrt(8 pi G rho/3)
ck("D3b  1/t_ff: sqrt(3 pi/(32 G rho)) = (pi/2)/sqrt(8 pi G rho/3) (both forms in the task agree)",
   sp.simplify(1 / tff_alt - sp.sqrt(32 / (3 * sp.pi))) == 0)
ck("D3c  omega_J^2 = (3/2) H_Lambda^2 exactly (the 4 pi G rho_Lambda 'plasma rate' is 3/2 of the dS Hubble rate squared)",
   sp.simplify(menu_check["V4 omega_J"] ** 2 - sp.Rational(3, 2) * menu_check["V1 H_Lambda"] ** 2) == 0)

print("\nSUMMARY (x01)")
print("  * fluid with (w, c_s^2): k_J^2 = 4 pi G (rho+p)/c_s^2;  vacuum: rho + p = 0 => no self-gravity in its own perturbations (B3b).")
print("  * vacuum enters dust dynamics only through H (C1); local dust exponent s = -H + sqrt(H^2 + 4 pi G rho_c) (C2).")
print("  * every genuine rate of this linear system is an algebraic number times H_Lambda (for algebraic w, c_s^2, X) or, for X free, a chosen input.")
L.finish()
