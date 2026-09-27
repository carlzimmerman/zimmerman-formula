#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FL2 -- V0'S DARK SLOT WITH FK1'S KICK POTENTIAL: the field-side checks (kernel invisibility, the khronon's equation with
the gated conversion as a source, CV3's rule, the criterion-B fold condition, and which piece may carry the gate).

FK1 (c2e1fa119, real_research/dark_fluid_kick_2026/) builds the kick inside FL1's field.  One complex scalar,
  V = m^2 |Phi|^2 + eps Re(Phi^2) + lambda(K) (Im Phi^2)^2,     Phi = (phi_H + i phi_L)/sqrt 2,   lambda ~ K^(-2q), q = 1.75.
eps splits the two real components (m_H^2 - m_L^2 = 2 eps).  The cold fluid is the heavy one.  The pure cross term
lambda phi_H^2 phi_L^2 converts heavy pairs into light pairs that leave back to back at v_k.  Its coupling carries the
vacuum gate through the khronon's K.  FK1 hands two checks to the V0 writer: the khronon's equation with the lambda'(K)
source, and whether the cross coupling keeps FL1 F2's kernel invisibility.  The review session adds three more: CV3's rule
(the gate must not re-enter the constraint Hessian), the criterion-B fold condition with both components multistreaming,
and a plain statement of the field content.

WHAT THIS LANE CHECKS
  V1 [kernel invisibility, sympy] both non-relativistic components in V0's static action, coupled as FL1 F2's dark slot,
     with the heavy one's rest-energy offset and the cross term's slow part.  Each obeys
     i psi_j,t = -lap psi_j/2m_j + m_j (Phi + lam/2) psi_j + dU/dpsi_j*, and lap u = 4 pi G (rho_b + m_H n_H + m_L n_L).
     The potential carries no metric field, so on shell (CV3 carrier_blind) the fluid feels and sources only u.
  V2 [the slow part of the cross term, sympy] the fast-phase average of phi_H^2 phi_L^2 is
     [4 n_H n_L + 2 Re(psi_H^2 psi_L*^2 e^(-2i d))]/(4 m_H m_L).  That reproduces FK1 K5: cross lambda/m^2, pair G/n =
     lambda/2m^2.  Its value is g_c (6 a^2 + 2 b^2) >= 0 with a + i b = psi_H psi_L*, and it vanishes in both pure states:
     the gated energy is non-negative and transient.
  V3 [the khronon's equation with the lambda'(K) source, sympy] adding -lambda(K) E_int to CV4's term,
     -(c_2 S/2)(delta K)^2 with S K^2 = 3 rho_c c^2, varying the khronon gives lap[dL/d(delta K)] = 0.  So
     x (1 + x)^(2q+1) = x0 = 2q E_int/(3 c_2 rho_c c^2) for x = delta K/K (a harmonic part vanishes at infinity).  The
     second variation's (delta K)^2 coefficient is c_2 S/2 + q(2q+1) E_int/K^2 > 0 whenever E_int >= 0.  Because V2's
     energy is >= 0, the gate stiffens the khronon and cannot destabilise it.
  V4 [the numbers] x at conversion.  Inputs: FK1's trigger couplings (read from its committed JSON), the energy fraction
     (3/4) G_t/mc^2 x E^(1/2), conversion at the trigger density (1 + delta_t) Omega_d rho_c0 E^4 (FK1 N2, q = 1.75),
     delta_t in {5, 25}, c_2 in {1e-4, 1e-3, 2.9e-3, 7.3e-3}, z = 0 ... 10.  Pass when max x < 0.1 for z <= 4.  The
     force from the non-CMC part, relative to gravity, is reported alongside.
  V5 [CV3's rule, sympy] order the Hessian as (multipliers, constrained, khronon + fluid).  Its determinant is
     (-1)^n det(M)^2 det(Z) for ANY constrained block X and constrained-khronon block Y.  The K-gated term depends only on
     (tau, psi), so its entries sit in Z and never in a multiplier row.  Checks: the explicit block inverse, det A =
     -det(M)^2, a zero Schur correction, five exact random 8x8 tests, and V0's 5x5 instance a^2 b^2 Z.
  V6 [criterion B, numeric] each component is a three-stream superposition with its generic vortex lattice.  At a node,
     |v| r -> const (|v| ~ 1/r, circulation 2 pi hbar/m): the fluid's velocity is singular.  The density, momentum
     density, stress and E_int stay finite and continuous through it.  The khronon is sourced by that smooth stress and
     answers E_int algebraically (V3), so its leaves never fold.  A dust khronon (u^mu ~ grad tau) would need grad tau
     = v.
  V7 [which piece may carry a region gate] at a 1e11 Msun edge (z = 0.25, CV3's conventions, w = 0.25), the gate force
     -4 pi G C B W' puts a potential B W'_max/rho_th at the edge.  For the conversion this is
     <= (3/4)(G_t/mc^2) c^2 (rho_d/rho_th) W'_max.  For the splitting it is (eps/2m^2) c^2 (rho_d/rho_th) W'_max.
     Pass when the design's gated piece stays below 0.05 v_f^2.
  (4) [reported] the dark slot's field content, each item marked derived, declared or fitted.
  MUTATE=1 gates the SPLITTING, eps(K), instead of the conversion.  Its K-dependent energy is (eps/2m)(n_H - n_L):
  sign-indefinite and present wherever the fluid is.  V3, V4 and V7 must FAIL.  rc = 1.

SCOPE.  The khronon response is CV4's quasi-static, linear, lambda-term-dominated equation (alpha_c enters only through
time derivatives), with the gate expanded around K = 3H.  The conversion is taken to happen at the trigger density, which
holds while regions cross the threshold slowly compared with the conversion.  FK1's G_t is its z = 0 background estimate
with O(1) factors; its z-scaling G_t ~ H^(1/2) follows from FK1 K4.  Nothing here re-scores retention, Harvey, X-COP or
the flagship.

Run from the repository root:  python3 real_research/dark_fluid_2026/FL2_dark_slot_with_the_kick.py
"""
import os, sys, json, math, time, random, warnings
import numpy as np
import sympy as sp
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "FL2", "FL2_dark_slot_with_the_kick"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the splitting eps(K) carries the gate instead of the conversion; V3, V4 and V7 must FAIL ***")

# FK1's committed numbers (read, not re-run)
FK1 = json.load(open(os.path.join(ROOT, "real_research", "dark_fluid_kick_2026", "FK1_kick_as_phase_change_results.json")))
GT = {k_: v_["G_over_mc2"] for k_, v_ in FK1["numbers"]["N3"].items()}           # trigger pair coupling G_t/mc^2 at z = 0
EPS_M2 = {float(k_): v_ for k_, v_ in FK1["numbers"]["K2"]["eps_over_m2"].items()} # eps/m^2 by v_k
Q_GATE = FK1["numbers"]["N2"]["q_linear_gate"]                                    # 1.75
P(f"\n  FK1 inputs: G_t/mc^2 = {GT}; eps/m^2(600 km/s) = {EPS_M2[600.0]:.4e}; q = {Q_GATE}")

# ============================================================================================ V1 kernel invisibility
banner("V1  KERNEL INVISIBILITY: both components in V0's static action, coupled as FL1 F2's dark slot")
x, t = sp.symbols("x t", real=True)
G_, mH, mL, a0_, c1, d1, m2_, fg, Dl, gc = sp.symbols("G m_H m_L a0 c1 d1 m2 f Delta g_c", positive=True)
Phi, u, v, lam, w, Psi = [sp.Function(n)(t, x) for n in ("Phi", "u", "v", "lam", "w", "Psi")]
aH, bH, aL, bL = [sp.Function(n)(t, x) for n in ("aH", "bH", "aL", "bL")]
rb = sp.Function("rho_b")(t, x)
qc = lambda s_: c1 * s_ ** sp.Rational(3, 2) + d1 * sp.log(1 + s_)
dx = lambda F, n=1: sp.diff(F, x, n)
EPG = 8 * sp.pi * G_
nH, nL = aH ** 2 + bH ** 2, aL ** 2 + bL ** 2
rho_d = mH * nH + mL * nL
psH, psL = aH + sp.I * bH, aL + sp.I * bL
# slow part of lambda phi_H^2 phi_L^2 in the frame where psi_H carries the offset Delta: g_x n_H n_L + g_c (psi_H^2 psi_L*^2 + cc)
U_int = 4 * gc * nH * nL + gc * sp.expand(psH ** 2 * sp.conjugate(psL) ** 2 + sp.conjugate(psH) ** 2 * psL ** 2)
U_int = sp.expand(U_int.subs({sp.conjugate(aH): aH, sp.conjugate(bH): bH, sp.conjugate(aL): aL, sp.conjugate(bL): bL}))
U_loc = Dl * nH + U_int
kin = lambda a_, b_, m_: (b_ * sp.diff(a_, t) - a_ * sp.diff(b_, t)) - (dx(a_) ** 2 + dx(b_) ** 2) / (2 * m_)
L_fluid = kin(aH, bH, mH) + kin(aL, bL, mL) - U_loc
M2 = m2_ * (1 - fg)
L_V0 = (-(rb + rho_d) * Phi - (2 * dx(Phi) * dx(u) - dx(u) ** 2) / EPG
        + a0_ ** 2 * fg * qc(dx(w) ** 2 / a0_ ** 2) / EPG
        + Psi * (dx(w, 2) - M2 * w - fg * (dx(u, 2) - dx(v, 2))) / EPG
        + lam * (dx(v, 2) - 4 * sp.pi * G_ * rho_d) / EPG
        - M2 * w ** 2 / EPG)
L_tot = L_V0 + L_fluid
Vc = Phi + lam / 2
res = []
for (a_, b_, m_) in ((aH, bH, mH), (aL, bL, mL)):
    ELa = sp.euler_equations(L_tot, [a_], [t, x])[0].lhs
    ELb = sp.euler_equations(L_tot, [b_], [t, x])[0].lhs
    ta = -2 * sp.diff(b_, t) + dx(a_, 2) / m_ - 2 * m_ * Vc * a_ - sp.diff(U_loc, a_)
    tb = 2 * sp.diff(a_, t) + dx(b_, 2) / m_ - 2 * m_ * Vc * b_ - sp.diff(U_loc, b_)
    res += [sp.simplify(ELa - ta), sp.simplify(ELb - tb)]
ELPhi = sp.euler_equations(L_tot, [Phi], [t, x])[0].lhs * EPG
lap_u_ok = sp.simplify(ELPhi - (2 * dx(u, 2) - EPG * (rb + rho_d))) == 0
metric_free = not (U_loc.free_symbols | set(U_loc.atoms(sp.Function))) & {Phi, u, v, lam, w, Psi}
P(f"    residuals against i psi_j,t = -lap psi_j/2m_j + m_j (Phi + lam/2) psi_j + dU/dpsi_j*: {res}")
P(f"    lap u = 4 pi G (rho_b + m_H n_H + m_L n_L): {lap_u_ok};  the fluid's potential contains no V0 field: {metric_free}")
OUT["numbers"]["V1"] = {"residuals": [str(r_) for r_ in res], "lap_u": lap_u_ok, "metric_free": metric_free}
check("V1 both components obey Schrodinger equations with m_j (Phi + lam/2) and lap u = 4 pi G (rho_b + m_H n_H + m_L n_L); "
      "the splitting and the cross term carry no metric field, so on shell (CV3 carrier_blind: Phi + lam/2 = u) the fluid "
      "feels and sources only the Newtonian potential of all matter",
      f"residuals {res}; lap u {lap_u_ok}; potential metric-free {metric_free}",
      all(r_ == 0 for r_ in res) and lap_u_ok and metric_free,
      "FK1's potential keeps FL1 F2's kernel invisibility: L353's reciprocity holds for the two-component fluid, whatever "
      "its composition; the conversion energy gravitates only through rho_d at relative order G_t/mc^2 ~ 1e-9, like a pressure")

# ============================================================================================ V2 the slow cross term
banner("V2  THE SLOW PART OF THE CROSS TERM: FK1 K5 reproduced; its energy is >= 0 and transient")
pH_, pL_, cpH_, cpL_, Es, Ds = sp.symbols("pH pL cpH cpL E D")
phH = (pH_ / Es + cpH_ * Es) / sp.sqrt(2 * mH)                       # e^(-i s) = 1/E, fast phase s
phL = (pL_ * Ds / Es + cpL_ * Es / Ds) / sp.sqrt(2 * mL)             # psi_L's phase lags by the slow d (D = e^(i d))
avg = sp.Poly(sp.expand(phH ** 2 * phL ** 2 * Es ** 4), Es).coeff_monomial(Es ** 4)
targ = (4 * pH_ * cpH_ * pL_ * cpL_ + pH_ ** 2 * cpL_ ** 2 / Ds ** 2 + cpH_ ** 2 * pL_ ** 2 * Ds ** 2) / (4 * mH * mL)
avg_ok = sp.simplify(avg - targ) == 0
x1, y1, x2, y2 = sp.symbols("x1 y1 x2 y2", real=True)
PH, PL = x1 + sp.I * y1, x2 + sp.I * y2
wv = sp.expand(PH * sp.conjugate(PL))
Eint_over_gc = sp.expand(4 * PH * sp.conjugate(PH) * PL * sp.conjugate(PL) + PH ** 2 * sp.conjugate(PL) ** 2
                         + sp.conjugate(PH) ** 2 * PL ** 2)
sq_ok = sp.simplify(Eint_over_gc - (6 * sp.re(wv) ** 2 + 2 * sp.im(wv) ** 2)) == 0
pure_zero = Eint_over_gc.subs({x2: 0, y2: 0}) == 0 and Eint_over_gc.subs({x1: 0, y1: 0}) == 0
P(f"    <phi_H^2 phi_L^2>_fast = [4 n_H n_L + psi_H^2 psi_L*^2 e^(-2id) + cc]/(4 m_H m_L): {avg_ok}")
P(f"    so lambda <..> = g_x n_H n_L + g_c (psi_H^2 psi_L*^2 + cc) with g_x = lambda/m_H m_L, g_c = lambda/4 m_H m_L, pair "
  f"G/n = 2 g_c = lambda/2m^2 (FK1 K5: {FK1['numbers']['K5']['lam(ImPhi^2)^2']})")
P(f"    E_int/g_c = 6 a^2 + 2 b^2 with a + i b = psi_H psi_L*: {sq_ok};  zero in both pure states: {pure_zero}")
OUT["numbers"]["V2"] = {"average": avg_ok, "square_form": sq_ok, "zero_in_pure_states": pure_zero}
check("V2 the fast-phase average of phi_H^2 phi_L^2 gives FK1's couplings (cross lambda/m^2, pair G/n = lambda/2m^2), and the "
      "conversion energy is g_c (6 a^2 + 2 b^2) >= 0, zero in both pure states", f"average {avg_ok}; square form {sq_ok}; "
      f"pure states {pure_zero}", avg_ok and sq_ok and pure_zero,
      "the gated energy lives only where both components coexist (during the conversion) and is never negative")

# ============================================================================================ V3 the khronon with the source
banner("V3  THE KHRONON'S EQUATION WITH THE lambda'(K) SOURCE (CV4's quasi-static lambda-term + the gated energy)")
y_, z_ = sp.symbols("y z", real=True)
aS = sp.symbols("a", positive=True)
c2s, S_, K0, E0, qg = sp.symbols("c_2 S K_0 E_0 q", positive=True)
pi_ = sp.Function("pi")(t, x, y_, z_)
dK = -(sp.diff(pi_, x, 2) + sp.diff(pi_, y_, 2) + sp.diff(pi_, z_, 2)) / aS ** 2        # CV4: the pi-part of delta K
xK = sp.symbols("xK")
gate_expand = sp.series((1 + xK) ** (-2 * qg), xK, 0, 3).removeO()                    # lambda(K)/lambda(K0), 2nd order
L_K = -(c2s * S_ / 2) * dK ** 2 - E0 * gate_expand.subs(xK, dK / K0)
EL = sp.euler_equations(L_K, [pi_], [t, x, y_, z_])[0].lhs
dLd = sp.diff(-(c2s * S_ / 2) * xK ** 2 * K0 ** 2 - E0 * gate_expand, xK) / K0          # dL/d(delta K), delta K = K0 xK
dLd_pi = dLd.subs(xK, dK / K0)
lapf = lambda F: sp.diff(F, x, 2) + sp.diff(F, y_, 2) + sp.diff(F, z_, 2)
form_ok = any(sp.simplify(sp.expand(EL - sgn * lapf(dLd_pi) / aS ** 2)) == 0 for sgn in (1, -1))
xs_lin = sp.solve(sp.Eq(dLd, 0), xK)[0]                                                 # linear response
x_lin_target = 2 * qg * E0 / (c2s * S_ * K0 ** 2 + 2 * qg * (2 * qg + 1) * E0)
lin_ok = sp.simplify(xs_lin - x_lin_target) == 0
stiff = sp.simplify(-sp.diff(-(c2s * S_ / 2) * xK ** 2 * K0 ** 2 - E0 * gate_expand, xK, 2) / K0 ** 2 / 2)
stiff_ok = sp.simplify(stiff - (c2s * S_ / 2 + qg * (2 * qg + 1) * E0 / K0 ** 2)) == 0
# the exact response for lambda ~ K^(-2q) (no expansion): dL/dx = 0  <=>  x (1 + x)^(2q+1) = 2 q E0/(c2 S K0^2)
xp = sp.symbols("x_p", positive=True)
dL_exact = sp.diff(-(c2s * S_ / 2) * xp ** 2 * K0 ** 2 - E0 * (1 + xp) ** (-2 * qg), xp)
exact_ok = sp.simplify(dL_exact * (1 + xp) ** (2 * qg + 1) / (c2s * S_ * K0 ** 2)
                       + xp * (1 + xp) ** (2 * qg + 1) - 2 * qg * E0 / (c2s * S_ * K0 ** 2)) == 0
# units: I_V0's prefactor c^3/16 pi G per d^4x (x0 = ct) makes -(c_2 S/2)(delta K)^2 with S = c^4/(8 pi G), K0 = 3H/c
cc_, GG_, HH_ = sp.symbols("c G_N H", positive=True)
SK2 = sp.simplify((cc_ ** 4 / (8 * sp.pi * GG_)) * (3 * HH_ / cc_) ** 2)
units_ok = sp.simplify(SK2 - 3 * (3 * HH_ ** 2 / (8 * sp.pi * GG_)) * cc_ ** 2) == 0      # = 3 rho_c c^2
sign_design = "E_int = g_c (6 a^2 + 2 b^2) >= 0 (V2)"
if MUTATE:
    # the splitting's K-dependent energy (eps/2m)(n_H - n_L): negative once the light component dominates
    E_gated = sp.Rational(1, 2) * (sp.Symbol("n_H", nonnegative=True) - sp.Symbol("n_L", nonnegative=True))
    E_min_sign = E_gated.subs({sp.Symbol("n_H", nonnegative=True): 0, sp.Symbol("n_L", nonnegative=True): 1})
    sign_design = "(eps/2m)(n_H - n_L): -eps/2m at n_H = 0, n_L = 1"
    nonneg = E_min_sign >= 0
else:
    nonneg = sq_ok                                                                       # V2: E_int = g_c(6a^2 + 2b^2)
P(f"    Euler-Lagrange in pi = lap[dL/d(delta K)]/a^2 (up to sign): {form_ok}  -> dL/d(delta K) = harmonic -> 0 at infinity")
P(f"    linear response delta K/K = {sp.factor(xs_lin)}: {lin_ok};  exact x (1+x)^(2q+1) = 2q E0/(c2 S K0^2): {exact_ok}")
P(f"    S K0^2 = (c^4/8 pi G)(3H/c)^2 = 3 rho_c c^2: {units_ok}")
P(f"    second variation (delta K)^2 coefficient = {stiff}: {stiff_ok};  gated energy {sign_design}: non-negative {nonneg}")
OUT["numbers"]["V3"] = {"EL_form": form_ok, "x_lin": str(sp.factor(xs_lin)), "exact": exact_ok, "units": units_ok,
                        "stiffness": str(stiff), "gated_energy_nonnegative": bool(nonneg)}
check("V3 with the gated term the khronon's quasi-static equation is lap[dL/d(delta K)] = 0: delta K/K solves x (1+x)^(2q+1) = "
      "2q E/(3 c_2 rho_c c^2), and the second variation's coefficient c_2 S/2 + q(2q+1) E/K^2 is positive because the gated "
      "energy is non-negative", f"EL form {form_ok}; linear response {lin_ok}; exact response {exact_ok}; units {units_ok}; "
      f"stiffness {stiff_ok}; gated energy non-negative {bool(nonneg)}",
      form_ok and lin_ok and exact_ok and units_ok and stiff_ok and bool(nonneg),
      "a convex gate (lambda ~ K^(-2q)) times a non-negative energy adds stiffness to the khronon: FK1's K-gate cannot "
      "destabilise it; a gate on the splitting could (its energy changes sign)")

# ============================================================================================ V4 the numbers
banner("V4  THE NUMBERS: the self-consistent shift delta K/K at conversion (FK1's trigger couplings)")
H0K, OM, OL = 0.0674, 0.3153, 0.6847                             # km/s/kpc, the record's cosmology (CV3/CV4)
OMEGA_D = 0.264                                                  # the dark fluid's mean share (Planck omega_c = 0.120)
E_ = lambda zz: math.sqrt(OM * (1 + zz) ** 3 + OL)
C2S = (1e-4, 1e-3, 2.9e-3, 7.3e-3)                               # KM1's lower edge, Planck caps (L350-L352), L340's window
ZS = (0.0, 1.0, 2.5, 4.0, 10.0)


def solve_x(x0, qq):
    lo, hi = 0.0, max(1.0, x0)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid * (1 + mid) ** (2 * qq + 1) < x0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


rows4, worst4, worst10 = [], 0.0, 0.0
e_split = EPS_M2[600.0] / 2                                      # (eps/2m^2): the splitting's K-dependent energy fraction
for mkey, gt0 in GT.items():
    for dt in (5.0, 25.0):
        for c2v in C2S:
            for zz in ZS:
                Ez = E_(zz)
                rho_over_rhoc = (1 + dt) * OMEGA_D * Ez ** 2          # rho_t(z)/rho_c(z), rho_t ~ E^4 (FK1 N2, q = 1.75)
                if MUTATE:
                    e_g = e_split                                     # persistent, wherever the fluid is (here: at rho_t)
                else:
                    e_g = 0.75 * gt0 * Ez ** 0.5                      # E_int <= (3/4) hbar G n, G_t ~ H^(1/2)
                x0 = 2 * Q_GATE * e_g * rho_over_rhoc / (3 * c2v)
                xs_ = solve_x(x0, Q_GATE)
                rows4.append({"m": mkey, "delta_t": dt, "c2": c2v, "z": zz, "e": e_g, "x0": x0, "x": xs_,
                              "lambda_factor": (1 + xs_) ** (-2 * Q_GATE)})
                if zz <= 4.0:
                    worst4 = max(worst4, xs_)
                else:
                    worst10 = max(worst10, xs_)
for r_ in rows4:
    if r_["delta_t"] == 25.0 and r_["m"] == "2e-19" and r_["c2"] in (1e-4, 1e-3):
        P(f"    m = {r_['m']} eV, delta_t = 25, c_2 = {r_['c2']:.0e}, z = {r_['z']:>4}: e = {r_['e']:.2e}, x0 = {r_['x0']:.2e}, "
          f"delta K/K = {r_['x']:.2e}, coupling factor {r_['lambda_factor']:.3f}")
force_ratio = 2 * Q_GATE * worst4 * (0.75 * GT["2e-19"] * E_(4.0) ** 0.5) * (299792.458 ** 2) / 200.0 ** 2
P(f"    worst delta K/K at z <= 4: {worst4:.3e};  at z = 10: {worst10:.3e}")
P(f"    the non-CMC gate's force on the fluid relative to gravity (v_c = 200 km/s), worst z <= 4: {force_ratio:.1e}")
OUT["numbers"]["V4"] = {"rows": rows4, "worst_z_le_4": worst4, "worst_z_10": worst10, "force_ratio": force_ratio}
check("V4 at conversion the gated energy shifts the khronon's K by < 10% for z <= 4 at every m of FK1's list, delta_t in "
      "{5, 25} and c_2 >= 1e-4: the leaves stay CMC to that accuracy and the K-gate stays force-free",
      f"max delta K/K (z <= 4) = {worst4:.2e}; at z = 10 {worst10:.2e}; relative gate force {force_ratio:.1e}",
      worst4 < 0.1,
      "the shift is set by G_t/mc^2 x rho_t/rho_c / c_2 (~1e-9 x 7E^2 / c_2), small because the conversion energy is "
      "transient and lives at the trigger density; at z ~ 10 with c_2 = 1e-4 it reaches ~0.2 and self-quenches the "
      "coupling by ~(1+x)^(-2q) (reported)")

# ============================================================================================ V5 CV3's rule
banner("V5  CV3'S RULE: the K-gated term cannot re-enter the constraint block")
Ms = sp.Matrix(3, 3, sp.symbols("M0:9"))
xs = sp.symbols("X0:6"); Xm = sp.Matrix([[xs[0], xs[1], xs[2]], [xs[1], xs[3], xs[4]], [xs[2], xs[4], xs[5]]])
Ym = sp.Matrix(3, 2, sp.symbols("Y0:6"))
zs = sp.symbols("Z0:3"); Zm = sp.Matrix([[zs[0], zs[1]], [zs[1], zs[2]]])
Z33, Z32 = sp.zeros(3, 3), sp.zeros(3, 2)
Hfull = sp.BlockMatrix([[Z33, Ms, Z32], [Ms.T, Xm, Ym], [Z32.T, Ym.T, Zm]]).as_explicit()
Am = sp.BlockMatrix([[Z33, Ms], [Ms.T, Xm]]).as_explicit()
Minv = Ms.inv()
Ainv = sp.BlockMatrix([[-Minv.T * Xm * Minv, Minv.T], [Minv, Z33]]).as_explicit()
inv_ok = sp.simplify(Am * Ainv - sp.eye(6)) == sp.zeros(6, 6)
Bm = sp.Matrix.vstack(Z32, Ym)
schur0 = sp.simplify(Bm.T * Ainv * Bm) == sp.zeros(2, 2)
detA_ok = sp.expand(Am.det(method="berkowitz") + Ms.det() ** 2) == 0
random.seed(3)
rand_ok = True
for _ in range(5):
    sub = {s_: sp.Rational(random.randint(-9, 9), random.randint(1, 5)) for s_ in list(Ms) + list(xs) + list(Ym) + list(zs)}
    rand_ok &= Hfull.subs(sub).det() == -(Ms.subs(sub).det()) ** 2 * Zm.subs(sub).det()
a_s, b_s, c_s, X11, X12, X22, Y1, Y2, Zs = sp.symbols("a b c X11 X12 X22 Y1 Y2 Z")
H5 = sp.Matrix([[0, a_s, 0, 0, 0], [a_s, X11, c_s, X12, Y1], [0, c_s, 0, b_s, 0], [0, X12, b_s, X22, Y2], [0, Y1, 0, Y2, Zs]])
det5 = sp.factor(H5.det())
# the gated term's fields: -lambda(K(tau)) E(psi) touches only (tau, psi)
tau_s, psi_s = sp.symbols("tau psi")
lamf, Ef = sp.Function("lambda_g"), sp.Function("E_int")
Lc = -lamf(K0 - tau_s) * Ef(psi_s)
touch = Lc.free_symbols & {sp.Symbol(n_) for n_ in ("Phi", "Psi", "lam", "u", "w", "v")}
P(f"    explicit block inverse {inv_ok}; Schur correction zero {schur0}; det A = -det(M)^2 {detA_ok}; 5 exact 8x8 tests {rand_ok}")
P(f"    V0's instance (Phi, u, Psi, w, tau): det = {det5};  the gated term touches multipliers/constrained fields: {touch or 'none'}")
OUT["numbers"]["V5"] = {"inverse": inv_ok, "schur_zero": schur0, "detA": detA_ok, "random": bool(rand_ok), "det5": str(det5)}
check("V5 with the multipliers linear and coupled only to constrained fields, det H = (-1)^n det(M)^2 det(Z) for any X and "
      "Y; the K-gated conversion depends only on the khronon and the fluid, so its entries sit in Z and the constraint block "
      "is untouched", f"inverse {inv_ok}; Schur {schur0}; det A {detA_ok}; random {bool(rand_ok)}; 5x5 {det5}",
      inv_ok and schur0 and detA_ok and rand_ok and sp.expand(det5 - a_s ** 2 * b_s ** 2 * Zs) == 0 and not touch,
      "the K-gate obeys CV3's rule by construction; whether Z itself stays positive is V3 (it gains + q(2q+1) E/K^2)")

# ============================================================================================ V6 criterion B
banner("V6  CRITERION B: both components multistreaming -- singular fluid velocity, smooth stress, unfolded leaves")
WAVES = {"H": ([(4.0, 0.0), (-2.0, 3.3), (-2.1, -3.2)], [0.0, 1.1, 2.3], [1.0, 0.9, 0.8], 1.0),
         "L": ([(3.1, 1.2), (-1.0, -3.0), (-2.4, 1.9)], [0.4, 2.0, 5.1], [1.0, 0.7, 0.85], 1.0 - 2.0e-6)}


def fields(key, X, Y):
    ks, ph, A, _ = WAVES[key]
    p = sum(Aj * np.exp(1j * (kx * X + ky * Y + pj)) for Aj, (kx, ky), pj in zip(A, ks, ph))
    px = sum(1j * kx * Aj * np.exp(1j * (kx * X + ky * Y + pj)) for Aj, (kx, ky), pj in zip(A, ks, ph))
    py = sum(1j * ky * Aj * np.exp(1j * (kx * X + ky * Y + pj)) for Aj, (kx, ky), pj in zip(A, ks, ph))
    return p, px, py


def node_of(key):
    xx, yy = np.meshgrid(np.linspace(0, 3, 601), np.linspace(0, 3, 601))
    n_ = np.abs(fields(key, xx, yy)[0]) ** 2
    i_ = np.unravel_index(n_.argmin(), n_.shape); zv = np.array([xx[i_], yy[i_]])
    for _ in range(60):
        p, px, py = fields(key, *zv)
        Jm = np.array([[px.real, py.real], [px.imag, py.imag]])
        zv = zv - np.linalg.solve(Jm, np.array([p.real, p.imag]))
    return zv


def local(zv, r_):
    out = []
    for th in np.linspace(0, 2 * np.pi, 64, endpoint=False):
        X, Y = zv[0] + r_ * np.cos(th), zv[1] + r_ * np.sin(th)
        comp = {k_: fields(k_, X, Y) for k_ in ("H", "L")}
        rho = sum(WAVES[k_][3] * abs(comp[k_][0]) ** 2 for k_ in comp)
        stress = sum((abs(comp[k_][1]) ** 2 + abs(comp[k_][2]) ** 2) / WAVES[k_][3] for k_ in comp)
        wv_ = comp["H"][0] * np.conj(comp["L"][0])
        eint = 6 * wv_.real ** 2 + 2 * wv_.imag ** 2
        out.append((rho, stress, eint, th, X, Y))
    return out


V6 = {}
for key in ("H", "L"):
    zv = node_of(key)
    m_ = WAVES[key][3]
    vr, circ, stress_rng = [], [], []
    for r_ in (1e-2, 1e-3, 1e-4, 1e-5):
        vals, cvals = [], 0.0
        ths = np.linspace(0, 2 * np.pi, 256, endpoint=False)
        for th in ths:
            X, Y = zv[0] + r_ * np.cos(th), zv[1] + r_ * np.sin(th)
            p, px, py = fields(key, X, Y)
            nn = abs(p) ** 2
            vx, vy = np.imag(np.conj(p) * px) / (m_ * nn), np.imag(np.conj(p) * py) / (m_ * nn)
            vals.append(math.hypot(vx, vy) * r_)
            cvals += (-vx * math.sin(th) + vy * math.cos(th)) * r_ * (2 * np.pi / len(ths))
        loc = local(zv, r_)
        vr.append(max(vals)); circ.append(cvals * m_ / (2 * np.pi))
        stress_rng.append((min(l_[1] for l_ in loc), max(l_[1] for l_ in loc), max(l_[2] for l_ in loc)))
    V6[key] = {"node": zv.tolist(), "max_v_r": vr, "winding": circ, "stress": stress_rng}
    P(f"    psi_{key} node at {zv.round(4).tolist()}: max|v| r at r = 1e-2..1e-5: {[round(v_, 4) for v_ in vr]}; circulation "
      f"m/(2 pi hbar) x loop = {[round(c_, 4) for c_ in circ]}")
    P(f"      total stress |grad psi|^2/m range on the loops: {[(round(a_, 3), round(b_, 3)) for a_, b_, _ in stress_rng]}; "
      f"max E_int/g_c {[round(c_, 3) for _, _, c_ in stress_rng]}")
v_div = all(abs(V6[k_]["max_v_r"][-1] / V6[k_]["max_v_r"][-2] - 1) < 0.01 for k_ in V6)   # |v| r -> const: |v| ~ 1/r
wind_ok = all(abs(abs(V6[k_]["winding"][-1]) - 1) < 1e-3 for k_ in V6)
stress_cont = all(abs(V6[k_]["stress"][-1][1] - V6[k_]["stress"][-1][0]) < 1e-3 * V6[k_]["stress"][-1][1] for k_ in V6)
OUT["numbers"]["V6"] = V6
check("V6 at a node of either multistreaming component the fluid velocity diverges (|v| r -> const, one quantum of "
      "circulation), while the density, stress and conversion energy stay finite and continuous through it",
      f"|v| r converged {v_div}; winding +-1 {wind_ok}; stress continuous at r = 1e-5 {stress_cont}",
      v_div and wind_ok and stress_cont,
      "the khronon is sourced by the smooth stress and answers E_int algebraically (V3): its leaves never fold; a dust "
      "khronon (grad tau = v) would inherit the 1/r singularity and the multiple values -- the fold criterion B forbids")

# ============================================================================================ V7 which piece may carry a region gate
banner("V7  WHICH PIECE MAY CARRY A REGION GATE: the gate force's edge potential at a 1e11 Msun edge (z = 0.25)")
GKs = 4.30091e-6; A0K = 9.3619e-11 * 3.0856775814913673e19 / 1e6; CK2 = 299792.458 ** 2
rho_c0 = 3 * H0K ** 2 / (8 * math.pi * GKs)
W_WIDTH, ZZ = 0.25, 0.25
rho_th = (2.0 / 3.0) * 2.5 * E_(ZZ) ** 4 * rho_c0                # CV3's threshold at x_c0 = 2.5, linear gate
vf = (GKs * 1e11 * A0K) ** 0.25
r_e = vf / math.sqrt(4 * math.pi * GKs * rho_th)
g_ = lambda s_: np.where(s_ > 0, np.exp(-1.0 / np.maximum(s_, 1e-300)), 0.0)
tt = np.linspace(1e-4, 1 - 1e-4, 200001)
Wp_max = float(np.gradient(g_(tt) / (g_(tt) + g_(1 - tt)), tt).max()) / (2 * W_WIDTH)
e_conv = 0.75 * GT["2e-19"] * E_(ZZ) ** 0.5                     # the conversion's largest energy fraction (lightest m)
rows7 = {}
for lab, e_g in (("conversion", e_conv), ("splitting", e_split)):
    for rr in (0.3, 1.0):
        phi_e = e_g * CK2 * rr * Wp_max
        rows7[f"{lab}_{rr}"] = {"edge_potential_kms2": phi_e, "over_vf2": phi_e / vf ** 2}
        P(f"    {lab:>10}, rho_d/rho_th = {rr}: edge potential {phi_e:.3e} (km/s)^2 = {phi_e / vf ** 2:.2e} v_f^2 "
          f"(v_f = {vf:.1f} km/s, r_e = {r_e:.0f} kpc, W'_max = {Wp_max:.3f})")
design = "splitting" if MUTATE else "conversion"
ratio_light = e_split / e_conv
ratio_heavy = e_split / (0.75 * min(GT.values()) * E_(ZZ) ** 0.5)
P(f"    the splitting's energy fraction over the conversion's at z = 0.25: {ratio_light:.0f}x (m = 2e-19 eV) to "
  f"{ratio_heavy:.1e}x (m = 1e-10 eV)")
OUT["numbers"]["V7"] = {"rows": rows7, "r_e_kpc": r_e, "vf": vf, "Wp_max": Wp_max, "design": design,
                        "split_over_conv": [ratio_light, ratio_heavy]}
check(f"V7 the design's gated piece ({design}) exerts less than 0.05 v_f^2 at a region edge even if region-gated; the other "
      "piece is reported", f"{design}: {rows7[design + '_1.0']['over_vf2']:.2e} v_f^2 at rho_d = rho_th; conversion "
      f"{rows7['conversion_1.0']['over_vf2']:.2e}, splitting {rows7['splitting_1.0']['over_vf2']:.2e}",
      rows7[design + "_1.0"]["over_vf2"] < 0.05,
      "the splitting's rest energy (eps/2m^2 = 1e-6 of mc^2, i.e. v_k^2/4) is far too large to carry any gate -- region "
      "(an edge wall ~10 v_f^2) or K (V4's MUTATE); the conversion's energy is ~1e-9 of mc^2, so it can carry either, "
      "and FK1's K-gate is the force-free choice")

# ============================================================================================ (4) the plain statement
banner("(4)  THE DARK SLOT'S FIELD CONTENT, SAID PLAINLY")
content = [
    ("Phi: one complex scalar = two real fields phi_H, phi_L", "declared (new field content; FL1 F1: V0 has no room for it)"),
    ("m", "declared (>= 2-5e-19 eV, L383); the fluid's mass is still required"),
    ("eps (eps/m^2 = v_k^2/(2c^2 - v_k^2) = 1.84-2.35e-6)", "fitted to L388's kick window 575-650 km/s (FK1 K2)"),
    ("lambda(K) = lambda_0 (K/K_0)^(-2q), pure cross term (Im Phi^2)^2", "declared; lambda_0 set by the trigger, q = 1.75 "
     "matched to the linear gate (FK1 N2); force-free and khronon-stiffening (V3-V5)"),
    ("initial misalignment near phi_H (within ~14 deg) and its amplitude", "declared (the amount, free like I0; FK1)"),
    ("Z2 x Z2, kernel invisibility, pair-only conversion at v_k", "derived from the declared potential (FK1 K2, V1, V2)"),
]
for item, mark in content:
    P(f"    {item:<72} {mark}")
P("    Its quanta, if quantised, would be bosons of masses m_H and m_L; at occupations ~1e77 per de Broglie cell (FL1 F6) it is")
P("    a classical field, not a gas of particles.  With eps != 0 the U(1) is broken: the amount is the non-relativistic number")
P("    n_H + n_L (an adiabatic invariant the conversion conserves), set by the misalignment amplitude, not a U(1) charge.")
OUT["numbers"]["content"] = content
check("(4) reported: one complex scalar with one explicit U(1)-breaking constant eps (fitted to the kick window), a declared "
      "mass, a declared gated cross coupling and a declared initial condition", "listed", True, load_bearing=False)

banner("VERDICT")
P(f"""  FK1's kick potential fits V0's dark slot without touching the gravity sector.  The two components couple to V0 exactly
  as FL1's one did: the Newtonian potential of all matter, kernel-invisible for any composition (V1).  The gated cross
  term's energy is non-negative and lives only while both components coexist (V2).  Through the khronon's K it therefore
  adds stiffness rather than removing it (V3).  It shifts K by at most {worst4:.1e} at conversion for z <= 4 and c_2 >= 1e-4
  (V4).  Its Hessian entries never reach a multiplier row (V5).  A multistreaming two-component fluid has a singular
  velocity but a smooth stress, so the leaves do not fold (V6).  The splitting itself cannot carry a gate: its rest
  energy is {ratio_light:.0f}x (m = 2e-19 eV) to {ratio_heavy:.0e}x (1e-10 eV) the conversion's, and it changes sign
  (V7, MUTATE).
  Declared, not derived: m, eps (fitted to the kick window), lambda_0, q and the initial misalignment.  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
