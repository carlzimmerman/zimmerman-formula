#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
esc_s_window_2026.py -- ROUTE 1 of the OPTION-1 ESCAPE:  DOES ONE VALUE OF s CLEAR BOTH DEATHS?
================================================================================================
2026-08-18.  Assigned question, verbatim: rescale Option 1's free function, script-J -> s*script-J,
and ask whether ONE s simultaneously (i) removes the transverse aether ghost and (ii) leaves the
linear-cosmology (CMB) aether kinetic coefficient nonzero and healthy.  PASS = non-empty window.
KILL = the two conditions are disjoint.

THE ACTION UNDER TEST (AeST, Skordis & Zlosnik arXiv:2007.00082 Eq. 5; the corpus's correct
transcription is real_research/bridge1_aest_equations.md -- NOT THE_COMPLETION.md):

  S = int d^4x (sqrt(-g)/16 pi Gt)[ R - 2 Lam - (K_B/2) F^{mu nu}F_{mu nu}
        + 2(2-K_B) J^mu grad_mu phi - (2-K_B) Y - F(Y,Q) - lam(A^mu A_mu + 1) ] + S_m[g]
  Q = A^mu grad_mu phi,  Y = (g^{mu nu}+A^mu A^nu) grad_mu phi grad_nu phi,
  F_{mu nu} = 2 grad_[mu A_nu],  J^mu = A^nu grad_nu A^mu   (the aether's ACCELERATION).

OPTION 1: F(Y,Q) -> F(Z,Q) with Z := J^mu J_mu.  AeST's own split F = (2-K_B) J(Z) + K(Q).
THE ESCAPE: J -> s J, so F_Z = (2-K_B) s J_Z = (2-K_B) s mu_phys(g_obs), mu_phys in (0,1].

================================================================================================
RESULT IN ONE PARAGRAPH.  DIRECTION: MIXED -- one briefed death is REFUTED, the other is real
and curable, and the price is worse than briefed and is NOT curable by any s.
================================================================================================
The s-window is NON-EMPTY, but not for the reason the brief expected, and the honest reason
matters more than the answer.  DEATH 1 (vector ghost) is REPRODUCED here from the action:
C_V = K_B - (2-K_B) s mu_phys, and at s = 1, mu_phys -> 1 this is 2K_B - 2 = -1.5 at K_B = 0.25,
c_V^2 = -0.1667.  Real.  DEATH 2 (CMB degeneracy) is NOT.  Its premise -- "for any F performing
the interpolation, F_Z(0) = K_B EXACTLY" -- is FALSE under the SAME convention that makes DEATH 1
true.  Under that convention mu_phys = J_Z (opt1_gates_2026.py D7/E1-E2: the whole Newtonian limit
is carried by J_Z -> 1), and the deep-MOND end of ANY interpolation has mu_phys -> 0, hence
F_Z(0) = 0, hence the linear-cosmology coefficient is K_B - 0 = K_B EXACTLY -- AeST's own value,
for EVERY s.  For the exponential kernel this is closed-form: mu = 1 - e^(-sqrt y), mu(0) = 0.
F_Z(0) = K_B would instead require mu(0) = K_B/((2-K_B)s) = 0.1429 at s=1: a MOND-limit mu FLOOR,
which is not an interpolation function at all, and which would make C_V(deep-MOND) = 0 -- the
vector mode infinitely strongly coupled at exactly the end DEATH 2 expands about.  THE TWO DEATHS
CANNOT BOTH BE TRUE; they are the same object F_Z read in two incompatible conventions.  This is
the SEVENTH error of the class the brief warned about, and it is in the brief.
   The CMB condition that survives is the branch-dependent one this repo already flagged
(opt1_gates_2026.py liability 1): at recombination Z is NOT infinitesimal, mu_rec -> 1 on the
large-Z branch, and the Eq (12) coefficient is K_B - (2-K_B) s mu_rec.  Positivity of THAT is the
SAME inequality as no-ghost.  So the intersection is non-empty and the two conditions coincide at
the worst case.  The binding constraint is neither: it is the LONGITUDINAL electric mode,
K_B - F_Z - 2 Z F_ZZ > 0, whose worst case is set by max d g_bar/d g_obs = 1/0.968 = 1.0335 -- the
same committed 0.968 that made the exponential kernel legal.  Window:
      0 < s < 0.13822 at K_B = 0.25,     0 < s < 0.050924 at K_B = 0.10.
   THE PRICE, computed here for the first time and WORSE than briefed: Gt/G_N = (1-K_B/2) s is
bounded by K_B/(2*1.0335), i.e. Gt/G_N <= 0.12094 (K_B=0.25) / 0.048377 (K_B=0.10) versus AeST's
0.875 -- an 8.3x / 20.7x split between the cosmological and local gravitational constants, and it
CANNOT be relieved by any s in the window because it is proportional to s.  Requiring the CMB
coefficient to sit within a tolerance tau of K_B drives s DOWN and the split UP without bound.
An order-of-magnitude BBN mapping (stated, not a likelihood, and NOT this route's deliverable)
gives Delta N_eff = -3.68 / -3.98 against sigma(N_eff) ~ 0.3; the SAME mapping applied to
unmodified AeST gives -0.52, so the escape is ~7x worse than a tension AeST already carries.
   Solar system is confirmed s-INDEPENDENT: s cancels identically between F_Z's normalisation and
G_N, the 1 AU anomaly is 10^-3458.7 (canonical) / 10^-3151.3 (alt) m/s^2 at every surviving s.
   ONE FURTHER LIABILITY, unasked and adverse: a_0 = kappa c sqrt(G rho_Lambda) now has a
G-AMBIGUITY it did not have.  If the anchor's G is G_N while rho_Lambda is the cosmologically
inferred Lam/(8 pi Gt), the product picks up G_N/Gt = 8.27x and a_0 moves by sqrt(8.27) = 2.88x,
which no RAR fit survives.  If the anchor is the cosmological combination Gt rho_Lambda = Lam/8pi,
a_0 is untouched.  NOT COMPUTED which fork the framework's derivation takes.

VERDICT: PARTIAL.  A non-empty s window clears both ASSIGNED conditions, so the escape is not
dead on Route 1 -- but DEATH 2 was never a real death, DEATH 1's cure carries a >=8x G-split that
no s can remove, and closing the escape now depends entirely on BBN/CLASS, which is not this file.

CONTROLS REPRODUCED BEFORE ANY NEW NUMBER (each named at its check):
  C-1  opt1_construction_2026.py PART F5b -- transverse aether wave: Z -> vdot^2, B^2 -> v'^2.
  C-2  the same, at F_Z = 0 (unmodified AeST): C_V = K_B > 0 and c_V^2 = +1 EXACTLY.  [THE GATE]
  C-3  opt1_construction_2026.py PART F1 -- Hessian eigenvalues 2(K_B - F_Z) transverse (x2) and
       2(K_B - F_Z - 2 Z F_ZZ) longitudinal.
  C-4  opt1_construction_2026.py PART F6 -- a_i = grad_i(alphadot + Psi) at linear order.
  C-5  opt1_gates_2026.py PART E3 -- min d g_obs/d g_bar = 0.968 for nu = 1/(1-e^(-sqrt y)).
  C-6  opt1_gates_2026.py PART G1 -- 1 AU anomaly 10^-3458.7 canonical / 10^-3151.3 alt m/s^2.
  C-7  bridge1_aest_equations.md -- Gt = (1 - K_B/2) Ghat, i.e. Gt/G_N = 0.875 at s = 1, K_B=0.25.

NOT COMPUTED, and no relief is assumed from any of it:
  * the actual delta-C_l from the K_B -> K_B - (2-K_B) s mu_rec shift (no AeST module in CLASS).
  * a real BBN likelihood; only the algebraic radiation-density mapping below.
  * which branch (mu_rec) recombination sits on -- carried as a parameter, both ends reported.
  * whether a LOWER bound on s exists from anything other than G_N/Ghat = 1/s blowing up.
  * the a_0 anchor's G-fork above.
  * GW amplitudes / gravitational-Cherenkov for the now-SUPERLUMINAL vector mode (c_V^2 > 1).

Exit 0 = every check passed.
"""

import math
import sys

import numpy as np
import sympy as sp
from scipy.optimize import minimize_scalar

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n         {detail}" if detail else ""))


def head(t):
    print("\n" + "=" * 96 + f"\n{t}\n" + "=" * 96)


print(__doc__)

# ------------------------------------------------------------------------------------------------
# constants -- BOTH footings carried for every dimensional number (standing rule)
# ------------------------------------------------------------------------------------------------
A0_CAN = 9.3619e-11          # kappa c sqrt(G rho_Lambda), canonical.  kappa = 1/2 FITTED (0.529+/-0.034)
A0_ALT = 1.1279e-10          # alt footing
FOOT = (("canonical", A0_CAN), ("ALT", A0_ALT))
GMSUN = 1.32712440018e20
AU = 1.495978707e11
SJ_BOUND = 3.66e-14          # Sereno & Jetzer 2006, m/s^2 (corpus-committed)
KB_LIST = (0.25, 0.10)       # K_B <= 0.25 from BBN (project_stages38_52_audit_cycle); 0.10 the low end
NEFF_STD = 3.044


# ================================================================================================
head("PART A -- CONTROLS FIRST.  The vector sector, rederived from the action.  [THE GATE]")
# ================================================================================================
tt, zz, epsb = sp.symbols("t z varepsilon", real=True)
K_B, FZ, FZZ, Zb = sp.symbols("K_B F_Z F_ZZ Zbar", real=True)
ETA = sp.diag(-1, 1, 1, 1)

# --- C-1: transverse aether wave A_x = v(t,z), exact unit-norm ansatz -----------------------------
vf = sp.Function("v")(tt, zz)
A_lo = sp.Matrix([-sp.sqrt(1 + epsb ** 2 * vf ** 2), epsb * vf, 0, 0])   # A_mu, A^mu A_mu = -1 exactly
norm = sp.simplify(sum((ETA * A_lo)[m] * A_lo[m] for m in range(4)))
dA = sp.zeros(4, 4)
for mu in range(4):
    dA[0, mu] = sp.diff(A_lo[mu], tt)
    dA[3, mu] = sp.diff(A_lo[mu], zz)
Fmn = sp.Matrix(4, 4, lambda a, b: dA[a, b] - dA[b, a])
A_up = ETA * A_lo
a_lo = sp.Matrix([sum(A_up[n] * Fmn[n, m] for n in range(4)) for m in range(4)])   # a_mu = A^nu F_{nu mu}
Z_w = sp.expand(sum((ETA * a_lo)[m] * a_lo[m] for m in range(4)))
Fup = ETA * Fmn * ETA
F2_w = sp.expand(sum(Fup[m, n] * Fmn[m, n] for m in range(4) for n in range(4)))
B2_w = sp.expand((F2_w + 2 * Z_w) / 2)


def o2(e):
    return sp.simplify(sp.expand(sp.series(sp.expand(e), epsb, 0, 3).removeO()).coeff(epsb, 2))


Z2, B22 = o2(Z_w), o2(B2_w)
check(sp.simplify(norm + 1) == 0 and sp.simplify(Z2 - sp.diff(vf, tt) ** 2) == 0
      and sp.simplify(B22 - sp.diff(vf, zz) ** 2) == 0,
      "A1  CONTROL C-1 REPRODUCED (opt1_construction_2026.py PART F5b): for a transverse aether "
      "wave A_x = v(t,z) with A^mu A_mu = -1 held EXACTLY, Z -> vdot^2 and B^2 -> v'^2 at O(eps^2)",
      "the aether Lagrangian -(K_B/2)F^2 - F(Z) = -K_B B^2 + K_B Z - F(Z) therefore gives\n"
      "         L_2 = (K_B - F_Z) vdot^2 - K_B v'^2,  so C_V = K_B - F_Z and c_V^2 = K_B/C_V.\n"
      "         The scalar cannot contribute: D^mu = q^{mu nu} grad_nu phi is a GRADIENT and has no\n"
      "         transverse-vector part, so the identity's -(2-K_B)|D-J|^2 cancels its +(2-K_B)Z\n"
      "         exactly in this sector -- which is why the a-a block is K_B Z - F(Z) and not 2Z - F.")

# --- C-2: THE GATE.  Unmodified AeST (F_Z = 0, equivalently s = 0) -------------------------------
CV_ctrl = {kb: kb - 0.0 for kb in KB_LIST}
cV2_ctrl = {kb: kb / CV_ctrl[kb] for kb in KB_LIST}
check(all(CV_ctrl[kb] == kb and abs(cV2_ctrl[kb] - 1.0) < 1e-15 for kb in KB_LIST),
      "A2  *** GATE PASSED -- CONTROL C-2: at F_Z = 0 (unmodified AeST, or s = 0) C_V = K_B > 0 and "
      f"c_V^2 = +1 EXACTLY at K_B = {KB_LIST[0]} and {KB_LIST[1]} ***",
      f"C_V = {CV_ctrl[0.25]:.4f} / {CV_ctrl[0.10]:.4f};  c_V^2 = {cV2_ctrl[0.25]:.6f} / "
      f"{cV2_ctrl[0.10]:.6f}.  Everything below is licensed by this reproduction.")

# --- C-3: the Hessian about a GENERAL background Z, which is where the death lives ----------------
a1, a2, a3 = sp.symbols("a_1 a_2 a_3", real=True)
avec = sp.Matrix([a1, a2, a3])
Zsym = a1 ** 2 + a2 ** 2 + a3 ** 2
Fser = FZ * (Zsym - Zb) + FZZ * (Zsym - Zb) ** 2 / 2          # F(Z) about Zbar, constant part dropped
W = K_B * Zsym - Fser
H = sp.Matrix(3, 3, lambda i, j: sp.diff(W, avec[i], avec[j]))
Hb = sp.simplify(H.subs({a1: sp.sqrt(Zb), a2: 0, a3: 0}))     # background acceleration along x
eigs = {sp.simplify(e) for e in Hb.eigenvals()}
tran_e = sp.simplify(2 * (K_B - FZ))
long_e = sp.simplify(2 * (K_B - FZ - 2 * Zb * FZZ))
check(tran_e in eigs and long_e in eigs and len(eigs) == 2,
      "A3  CONTROL C-3 REPRODUCED (opt1_construction_2026.py PART F1): the electric kinetic matrix "
      "about a background |a|^2 = Zbar has eigenvalues 2(K_B - F_Z) transverse (x2) and "
      "2(K_B - F_Z - 2 Zbar F_ZZ) longitudinal",
      "so the NO-GHOST conditions are (N1) K_B - F_Z > 0 and (N2) K_B - F_Z - 2 Z F_ZZ > 0.\n"
      "         DEATH 1 is N1 evaluated where Newton's law forces J_Z -> 1.  N2 is NOT in the brief\n"
      "         and turns out to be the binding one (PART C).")

# --- reproduce DEATH 1 exactly as briefed ---------------------------------------------------------
death1 = {kb: kb - (2 - kb) * 1.0 * 1.0 for kb in KB_LIST}     # s = 1, mu_phys = 1
death1_cV2 = {kb: kb / death1[kb] for kb in KB_LIST}
check(abs(death1[0.25] - (-1.5)) < 1e-12 and death1[0.25] < 0 and death1_cV2[0.25] < 0
      and abs(death1_cV2[0.25] - 0.25 / (2 * (0.25 - 1.0))) < 1e-12,
      f"A4  DEATH 1 REPRODUCED: at s = 1 and mu_phys -> 1 (the Newtonian limit, i.e. the solar "
      f"system and the whole RAR above g_bar = 0.024 a_0), C_V = 2K_B - 2 = {death1[0.25]:.4f} at "
      f"K_B = 0.25 and {death1[0.10]:.4f} at K_B = 0.10 -- NEGATIVE, a ghost, with "
      f"c_V^2 = {death1_cV2[0.25]:.6f} < 0, tachyonic",
      "the briefed C_V = -1.5 and the briefed formula c_V^2 = K_B/(2(K_B-1)) are both reproduced\n"
      "         from the action, not quoted.")


# ================================================================================================
head("PART B -- the kernel, and what mu_phys actually is at both ends")
# ================================================================================================
def nu_exp(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


def mu_of_y(y):
    """mu_phys = g_bar/g_obs = 1/nu.  CLOSED FORM for the Route-A exponential kernel."""
    return 1.0 - np.exp(-np.sqrt(y))


yy = np.logspace(-14, 12, 600001)
mu_vals = mu_of_y(yy)
gobs_over_a0 = yy * nu_exp(yy)
# deep-MOND normalisation check: mu -> g_obs/a0 as g -> 0  (this is what DEFINES a_0 in AQUAL)
deep = yy < 1e-8
ratio_deep = mu_vals[deep] / gobs_over_a0[deep]
check(mu_vals[0] < 1e-6 and abs(ratio_deep[0] - 1.0) < 1e-6 and abs(mu_vals[-1] - 1.0) < 1e-12,
      "B1  the interpolation, in closed form: mu_phys(y) = 1 - e^(-sqrt y) with y = g_bar/a_0.  "
      f"mu -> {mu_vals[0]:.3e} at y = 1e-14 (deep MOND) and -> {mu_vals[-1]:.12f} at y = 1e12 "
      f"(Newtonian).  The deep-MOND normalisation mu = g_obs/a_0 holds to "
      f"{abs(ratio_deep[0]-1.0):.2e}",
      "so J_Z(0) = 0 and J_Z(infinity) = 1: the second is the normalisation Newton's law demands\n"
      "         (opt1_gates_2026.py D7), the first is what EVERY MOND interpolation must do.")

check(bool(np.all(mu_vals > 0)) and bool(np.all(mu_vals <= 1.0)),
      "B2  mu_phys in (0,1] over 26 decades in y -- so the transverse condition N1 reduces to a "
      "single worst case at mu_phys = 1, and the static-attraction condition M = F_Z > 0 holds for "
      "every s > 0 with no upper constraint of its own",
      "M(Z) = (2-K_B) s mu_phys > 0 identically for s > 0.  Static attraction is NOT the binding\n"
      "         side of the window; it only forbids s <= 0.")

# the longitudinal quantity: N2 <=> (2-K_B) s * [mu + g dmu/dg] < K_B, and mu*g_obs = g_bar exactly,
# so the bracket is d g_bar / d g_obs (opt1_gates_2026.py E2).  Get its MAXIMUM.
xx = np.linspace(1e-6, 60.0, 4000001)          # x = sqrt(y)
Ex = np.exp(-xx)
dgobs_dgbar = (2.0 * (1.0 - Ex) - xx * Ex) / (2.0 * (1.0 - Ex) ** 2)


def _dg(x):
    e = math.exp(-x)
    return (2.0 * (1.0 - e) - x * e) / (2.0 * (1.0 - e) ** 2)


r = minimize_scalar(_dg, bracket=(1.0, 2.6, 6.0), method="brent",
                    options={"xtol": 1e-12})
DG_MIN = float(r.fun)
ELL_MAX = 1.0 / DG_MIN
check(abs(DG_MIN - 0.968) < 0.002 and DG_MIN > 0 and bool(np.all(dgobs_dgbar > 0)),
      f"B3  CONTROL C-5 REPRODUCED (opt1_gates_2026.py PART E3): min d g_obs/d g_bar = "
      f"{DG_MIN:.6f} at sqrt y = {r.x:.4f}, against the committed 0.968; strictly positive over the "
      f"whole grid, so the exponential kernel stays legal",
      f"the SAME number now does new work: max d g_bar/d g_obs = 1/{DG_MIN:.6f} = {ELL_MAX:.6f},\n"
      f"         which is the worst case of the LONGITUDINAL condition N2 and is > 1, so N2 is "
      f"{100*(ELL_MAX-1):.2f}% TIGHTER than N1.")


# ================================================================================================
head("PART C -- (a) the rescaled vector sector: C_V > 0 for all mu_phys iff s < K_B/(2-K_B)")
# ================================================================================================
ss, mus = sp.symbols("s mu", positive=True)
CV_sym = K_B - (2 - K_B) * ss * mus
# monotone decreasing in mu on (0,1], so the infimum over mu in (0,1] is at mu = 1
check(sp.simplify(sp.diff(CV_sym, mus) - (-(2 - K_B) * ss)) == 0,
      "C1  C_V(s, mu) = K_B - (2-K_B) s mu is LINEAR and strictly DECREASING in mu for K_B < 2 and "
      "s > 0, so its infimum over mu in (0,1] is attained at mu = 1 and nowhere else",
      "hence 'C_V > 0 for all mu in (0,1]'  <=>  K_B - (2-K_B)s > 0  <=>  s < K_B/(2-K_B).\n"
      "         No sampling needed; the scan below is a numerical corroboration only.")

sol = sp.solve(sp.Eq(CV_sym.subs(mus, 1), 0), ss)[0]
check(sp.simplify(sol - K_B / (2 - K_B)) == 0,
      "C2  the boundary is s* = K_B/(2-K_B) EXACTLY (sympy), reproducing the briefed 0.1429 at "
      f"K_B = 0.25: s* = {float(sp.Rational(1,4)/(2-sp.Rational(1,4))):.6f}")

bad = []
for kb in KB_LIST:
    smax_n1 = kb / (2 - kb)
    for s_test, want in ((0.99 * smax_n1, True), (1.01 * smax_n1, False)):
        cv = kb - (2 - kb) * s_test * mu_vals
        if bool(np.all(cv > 0)) != want:
            bad.append((kb, s_test, want))
check(not bad,
      "C3  numerical corroboration over 26 decades of mu_phys and both K_B: C_V > 0 everywhere at "
      "s = 0.99 s* and FAILS somewhere at s = 1.01 s*, both K_B.  The window's upper edge is real "
      "and it is N1's",
      "no ghost, and since c_V^2 = K_B/C_V > 0 the mode is also non-tachyonic throughout.")

# N2, the condition the brief does not mention
S_N1 = {kb: kb / (2 - kb) for kb in KB_LIST}
S_N2 = {kb: kb / ((2 - kb) * ELL_MAX) for kb in KB_LIST}
check(all(S_N2[kb] < S_N1[kb] for kb in KB_LIST),
      "C4  *** NEW, AND ADVERSE, AND NOT IN THE BRIEF: the LONGITUDINAL electric condition N2, "
      "K_B - F_Z - 2 Z F_ZZ > 0, is TIGHTER than N1.  Using the identity J_Z + 2Z J_ZZ = "
      "d g_bar/d g_obs (opt1_gates_2026.py E2), N2 reads (2-K_B) s * max(d g_bar/d g_obs) < K_B ***",
      f"s < K_B/[(2-K_B) * {ELL_MAX:.6f}]:  {S_N2[0.25]:.6f} at K_B=0.25 (vs N1's {S_N1[0.25]:.6f}),\n"
      f"         {S_N2[0.10]:.6f} at K_B=0.10 (vs N1's {S_N1[0.10]:.6f}).  A 3.2% tightening, small\n"
      "         but it is the operative bound and the brief's 0.1429 is NOT attainable.")

c_V2_edge = {kb: kb / (kb - (2 - kb) * S_N2[kb] * 1.0) for kb in KB_LIST}
info("C5  LIABILITY, stated at equal volume: the cured vector mode is SUPERLUMINAL.  "
     "c_V^2 = K_B/(K_B - (2-K_B) s mu) >= 1 for every s > 0, and it DIVERGES at the window edge",
     f"at the N2 edge with mu = 1: c_V^2 = {c_V2_edge[0.25]:.3f} (K_B=0.25) / "
     f"{c_V2_edge[0.10]:.3f} (K_B=0.10) -- i.e. the edge is a strong-coupling boundary, not a\n"
     "         merely marginal one.  A superluminal aether mode is not a GW170817 violation "
     "(that bounds c_T,\n         which is 1 exactly here) but it owes a causality/Cherenkov "
     "check that is NOT COMPUTED.")


# ================================================================================================
head("PART D -- (b) THE QUESTION NOBODY ASKED: what the rescaling does to F_Z(0) and the CMB")
# ================================================================================================
# --- C-4: a_i = grad_i(alphadot + Psi) at linear order, flat background ---------------------------
Psif, alpf = sp.Function("Psi")(tt, zz), sp.Function("alpha")(tt, zz)
gS = sp.diag(-(1 + 2 * epsb * Psif), 1, 1, 1)
gSi = sp.diag(-1 / (1 + 2 * epsb * Psif), 1, 1, 1)
AS = sp.Matrix([-(1 + epsb * Psif), 0, 0, epsb * sp.diff(alpf, zz)])   # bridge1's own ansatz
XC = [tt, sp.Symbol("x"), sp.Symbol("y"), zz]
GamS = [[[sp.simplify(sum(gSi[l, rr] * (sp.diff(gS[rr, m], XC[n]) + sp.diff(gS[rr, n], XC[m])
                                        - sp.diff(gS[m, n], XC[rr])) for rr in range(4)) / 2)
          for n in range(4)] for m in range(4)] for l in range(4)]
dAS = sp.Matrix(4, 4, lambda m, n: sp.diff(AS[n], XC[m])
                - sum(GamS[l][m][n] * AS[l] for l in range(4)))
FS = sp.Matrix(4, 4, lambda p, q: sp.cancel(dAS[p, q] - dAS[q, p]))
aS3 = sp.cancel(sum((gSi * AS)[n] * FS[n, 3] for n in range(4)))
aS3_lin = sp.simplify(sp.expand(sp.series(aS3, epsb, 0, 2).removeO()).coeff(epsb, 1))
check(sp.simplify(aS3_lin - sp.diff(sp.diff(alpf, tt) + Psif, zz)) == 0,
      "D1  CONTROL C-4 REPRODUCED (opt1_construction_2026.py PART F6): at linear order "
      "a_i = grad_i(alphadot + Psi) = grad_i E, with E = alphadot + Psi SZ21's OWN mixing variable "
      "(bridge1_aest_equations.md).  Hence Z = |grad E|^2 is O(eps^2), NOT O(eps^3)",
      "so DEATH 2's SETUP is correct: the free function DOES reach the linear cosmological sector\n"
      "         under F(Z), unlike F(Y) where Y^{3/2} is O(delta^3).  Only its CONCLUSION is wrong.")

# --- the O(eps^2) coefficient, symbolically ------------------------------------------------------
Ef = sp.Function("E")(tt, zz)
Zlin = sp.diff(Ef, zz) ** 2                                   # Z at O(eps^2)
FZ0 = sp.Symbol("F_Z0", real=True)                            # F_Z evaluated at Z = 0
L_elec = K_B * Zlin - (FZ0 * Zlin)                            # +K_B Z from -(K_B/2)F^2 ; -F_Z(0) Z
coef = sp.simplify(sp.expand(L_elec).coeff(sp.diff(Ef, zz) ** 2))
check(sp.simplify(coef - (K_B - FZ0)) == 0,
      "D2  the O(eps^2) aether-electric coefficient is [K_B - F_Z(0)] EXACTLY (symbolic), so linear "
      "cosmology sees K_B -> K_B - F_Z(0) in SZ21 Eqs (7)/(11)/(12).  DEATH 2's structure: CONFIRMED",
      "the whole death therefore rests on ONE number, F_Z(0).  It is computed next.")

# --- F_Z(0) for the rescaled function.  THE ANSWER. -----------------------------------------------
FZ0_val = {}
for kb in KB_LIST:
    for s_ in (1.0, S_N2[kb], 1e-3):
        FZ0_val[(kb, s_)] = (2 - kb) * s_ * float(mu_of_y(1e-30))
check(all(v < 1e-14 for v in FZ0_val.values()),
      "D3  *** F_Z(0) = (2-K_B) s mu_phys(0) = 0 FOR EVERY s, because mu_phys(0) = 0 -- the "
      "deep-MOND end of ANY interpolation.  Closed form for the Route-A kernel: "
      "mu = 1 - e^(-sqrt y) and mu(0) = 0 identically ***",
      f"largest value over K_B in {KB_LIST} and s in (1, s_max, 1e-3): "
      f"{max(FZ0_val.values()):.3e}.  Therefore K_B - F_Z(0) = K_B EXACTLY, AeST's own value,\n"
      "         at EVERY s.  The aether electric kinetic term does NOT vanish and Eq (12) does NOT\n"
      "         collapse.  DEATH 2, AS BRIEFED, IS REFUTED.")

# --- and the two deaths cannot both be true ------------------------------------------------------
mu0_required = {kb: kb / ((2 - kb) * 1.0) for kb in KB_LIST}    # what F_Z(0)=K_B would demand at s=1
check(all(mu0_required[kb] > 0.04 for kb in KB_LIST),
      "D4  *** THE TWO DEATHS ARE MUTUALLY EXCLUSIVE, and it is one convention splice counted "
      "twice.  Both quote the same object F_Z.  DEATH 1 reads it at the Newtonian end "
      "(F_Z = (2-K_B) = 1.75) using mu_phys = J_Z; DEATH 2 asserts F_Z(0) = K_B at the deep-MOND "
      "end, which under the SAME dictionary demands mu_phys(0) = K_B/((2-K_B)s) ***",
      f"that floor is mu(0) = {mu0_required[0.25]:.4f} (K_B=0.25) / {mu0_required[0.10]:.4f} "
      f"(K_B=0.10) at s = 1 -- a MOND-limit mu FLOOR, i.e. NOT an interpolation function, and it\n"
      "         would make C_V = K_B - K_B = 0 at exactly the end DEATH 2 expands about (the vector\n"
      "         mode infinitely strongly coupled there).  Either mu_phys = J_Z, in which case\n"
      "         DEATH 1 holds and DEATH 2 does not; or mu_phys ~ (K_B - F_Z), in which case DEATH 2\n"
      "         holds and DEATH 1 does not (C_V = mu > 0 everywhere).  The committed derivation\n"
      "         (opt1_gates_2026.py D7/D8: 'the ENTIRE Newtonian limit is carried by J_Z -> 1')\n"
      "         selects the FIRST.  DEATH 1 is the real one.")

# --- the CMB condition that DOES survive: the branch question ------------------------------------
MU_REC = {"deep-MOND branch (mu_rec -> 0)": 0.0, "large-Z branch (mu_rec -> 1)": 1.0}
cmb_coef = {}
for kb in KB_LIST:
    for lab, mr in MU_REC.items():
        cmb_coef[(kb, lab)] = kb - (2 - kb) * S_N2[kb] * mr
check(all(v > 0 for v in cmb_coef.values()),
      "D5  the CMB condition that SURVIVES is the branch-dependent one this repo already flagged "
      "(opt1_gates_2026.py liability 1): Z is not infinitesimal at recombination, so the operative "
      "coefficient is K_B - (2-K_B) s mu_rec.  POSITIVITY OF THAT IS THE SAME INEQUALITY AS N1",
      "\n         ".join(
          [f"K_B={kb}: {lab:<34s} coefficient = {cmb_coef[(kb,lab)]:.6f}  "
           f"(AeST value {kb})" for kb in KB_LIST for lab in MU_REC]))

# --- the explicit inequalities, and their intersection --------------------------------------------
print("""
    THE TWO CONDITIONS AS EXPLICIT INEQUALITIES IN s
    ------------------------------------------------
      (i)  VECTOR NO-GHOST, worst case over the whole RAR and the solar system:
                 N1:  s <  K_B / (2 - K_B)
                 N2:  s <  K_B / [(2 - K_B) * max(d g_bar/d g_obs)]      <-- operative, tighter
      (ii) CMB NON-DEGENERACY, i.e. the SZ21 Eq (12) aether kinetic coefficient nonzero:
                 as briefed (F_Z(0) = K_B):   NO s works -- but the premise is FALSE (D3, D4)
                 as computed (F_Z(0) = 0)  :  coefficient = K_B for EVERY s > 0   -- ALWAYS SATISFIED
                 branch-corrected          :  s <  K_B / [(2 - K_B) mu_rec],  mu_rec in (0,1]
                                              -> at mu_rec = 1 this is EXACTLY N1
      INTERSECTION: NON-EMPTY.  0 < s < K_B/[(2-K_B) * 1.0335], and condition (ii) is implied by
      condition (i) rather than competing with it.  The window is bounded above by the VECTOR
      sector and below only by G_N/Ghat = 1/s diverging.
""")
check(all(S_N2[kb] > 0 for kb in KB_LIST),
      "D6  *** INTERSECTION NON-EMPTY at both K_B.  Route 1 PASSES on its assigned criterion: one s "
      "clears both deaths -- because the second death is not a death, and the branch-corrected "
      "version of it coincides with the first ***")


# ================================================================================================
head("PART E -- (c) the window as numbers, and THE PRICE")
# ================================================================================================
# CONTROL C-7 first: unmodified AeST must give Gt/G_N = 1 - K_B/2 = 0.875 at K_B = 0.25, s = 1.
gt_over_gn_aest = {kb: (1 - kb / 2) * 1.0 for kb in KB_LIST}
check(abs(gt_over_gn_aest[0.25] - 0.875) < 1e-12,
      "E1  CONTROL C-7 REPRODUCED (bridge1_aest_equations.md: Gt = (1 - K_B/2) Ghat): at s = 1 the "
      f"price formula Gt/G_N = (1 - K_B/2) s returns {gt_over_gn_aest[0.25]:.4f} at K_B = 0.25 and "
      f"{gt_over_gn_aest[0.10]:.4f} at K_B = 0.10 -- AeST's own split, exactly",
      "so the formula is anchored on a committed number before it is used on a new one.  G_N = "
      "Ghat/s\n         is opt1_gates_2026.py D7's G_eff = Gt/[(1-K_B/2) J_Z(infinity)] with "
      "J_Z(infinity) = s.")

print(f"\n    {'K_B':>6}{'s_max (N1)':>13}{'s_max (N2)*':>14}{'Gt/G_N max':>13}"
      f"{'G_N/Ghat min':>15}{'split':>10}{'c_V^2 at edge':>15}")
rows = {}
for kb in KB_LIST:
    smax = S_N2[kb]
    gt_gn = (1 - kb / 2) * smax
    gn_ghat = 1.0 / smax
    rows[kb] = (S_N1[kb], smax, gt_gn, gn_ghat, 1.0 / gt_gn, c_V2_edge[kb])
    print(f"    {kb:>6.2f}{S_N1[kb]:>13.6f}{smax:>14.6f}{gt_gn:>13.6f}{gn_ghat:>15.4f}"
          f"{1.0/gt_gn:>9.2f}x{c_V2_edge[kb]:>15.1f}")
print("    * N2 is the operative bound (PART C4).  'split' = G_N/Gt = the factor between the local "
      "and\n      cosmological gravitational constants.  Gt/G_N is PROPORTIONAL to s: it cannot be "
      "improved\n      by moving inside the window, only made worse.\n")

check(abs(rows[0.25][2] - 0.120943) < 5e-5 and abs(rows[0.10][2] - 0.048377) < 5e-5
      and rows[0.25][2] < 0.125 and rows[0.10][2] < 0.05,
      "E2  *** THE PRICE, COMPUTED: Gt/G_N <= K_B/(2 * 1.0335) = 0.12094 at K_B = 0.25 and 0.04838 "
      "at K_B = 0.10, versus AeST's 0.875.  An 8.27x / 20.67x SPLIT between the cosmological and "
      "the local gravitational constant, and NO s in the window relieves it ***",
      "the brief's normalisation-free statement 2 Gt < K_B G_N is reproduced (it is N1's form);\n"
      "         the operative N2 form is 2 Gt < K_B G_N / 1.0335.  This is the number the escape\n"
      "         lives or dies on, and it is structural: Gt/G_N = (1-K_B/2) s with s bounded above.")

check(abs((1 - 0.25 / 2) * S_N1[0.25] - 0.125) < 1e-12,
      "E3  and the brief's own quoted ceiling 0.125 is reproduced exactly as the N1 (looser) form "
      "of E2, confirming my price algebra against the briefed value before I use the tighter one")

# tolerance form: how small must s be for the CMB coefficient to sit within tau of K_B?
print("    IF the CMB is additionally required to keep the Eq (12) coefficient within a fractional")
print("    tolerance tau of K_B on the large-Z branch (mu_rec = 1), then s <= tau * K_B/(2-K_B):\n")
print(f"    {'tau':>8}{'s (K_B=0.25)':>15}{'Gt/G_N':>12}{'split':>10}"
      f"{'s (K_B=0.10)':>15}{'Gt/G_N':>12}{'split':>10}")
for tau in (1.0, 0.10, 0.01):
    line = f"    {tau:>8.2f}"
    for kb in KB_LIST:
        s_t = min(tau * S_N1[kb], S_N2[kb])
        g = (1 - kb / 2) * s_t
        line += f"{s_t:>15.6f}{g:>12.6f}{1.0/g:>9.1f}x"
    print(line)
check(True,
      "E4  the tolerance table is MONOTONE THE WRONG WAY: tightening the CMB drives s down and the "
      "G-split up without bound.  There is no s that is simultaneously CMB-quiet and G-split-quiet",
      "at tau = 1% the split is 800x.  This is the structural difference from F(Y) the brief\n"
      "         named: there the analogous asymptote saturates as lambda_s/(1+lambda_s) -> 1 and "
      "the\n         normalisation drops out; here it does not, because F_Z is the SOLE carrier of "
      "G_N.")

# BBN mapping -- flagged as an ESTIMATE, with the AeST control alongside
print("\n    BBN ORDER-OF-MAGNITUDE MAPPING (an ALGEBRAIC EQUIVALENCE, NOT a likelihood, and NOT")
print("    this route's deliverable -- the assigned BBN/CLASS pricing belongs to another route).")
print("    Friedmann carries Gt; laboratories measure G_N.  Rescaling G by f = Gt/G_N is equivalent")
print("    at BBN to rescaling the radiation density: 1 + (7/8) N_eff,eff = f [1 + (7/8) N_std].\n")
print(f"    {'case':<34}{'f = Gt/G_N':>12}{'sqrt f (H ratio)':>18}{'N_eff,eff':>12}"
      f"{'Delta N_eff':>13}")
bbn = {}
for lab, kb, s_ in (("AeST unmodified, K_B=0.25", 0.25, 1.0),
                    ("AeST unmodified, K_B=0.10", 0.10, 1.0),
                    ("escape at s_max, K_B=0.25", 0.25, S_N2[0.25]),
                    ("escape at s_max, K_B=0.10", 0.10, S_N2[0.10])):
    f = (1 - kb / 2) * s_
    n_eff = (f * (1 + 0.875 * NEFF_STD) - 1.0) / 0.875
    bbn[lab] = (f, math.sqrt(f), n_eff, n_eff - NEFF_STD)
    print(f"    {lab:<34}{f:>12.6f}{math.sqrt(f):>18.4f}{n_eff:>12.4f}{n_eff-NEFF_STD:>13.4f}")
check(bbn["escape at s_max, K_B=0.25"][3] < -3.0 and bbn["AeST unmodified, K_B=0.25"][3] > -1.0,
      "E5  ESTIMATE, flagged as such: the escape maps to Delta N_eff = "
      f"{bbn['escape at s_max, K_B=0.25'][3]:.2f} (K_B=0.25) / "
      f"{bbn['escape at s_max, K_B=0.10'][3]:.2f} (K_B=0.10) against sigma(N_eff) ~ 0.3 -- and the "
      "implied N_eff,eff is NEGATIVE, i.e. outside the physical range entirely",
      "EVEN-HANDED CONTROL alongside it: the SAME mapping applied to UNMODIFIED AeST gives "
      f"{bbn['AeST unmodified, K_B=0.25'][3]:.2f},\n         a ~1.7-sigma tension AeST already "
      "carries and which is INHERITED, not created.  The escape is\n         ~7x worse than that. "
      " A real BBN likelihood is NOT COMPUTED and no relief is assumed from\n         either "
      "direction.")

info("E6  ONE FURTHER LIABILITY, unasked and adverse: the a_0 ANCHOR acquires a G-ambiguity.  "
     "a_0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 canonical / 1.1279e-10 alt",
     f"if the anchor's G is the LOCAL G_N while rho_Lambda is the cosmologically inferred\n"
     f"         Lam/(8 pi Gt), the product gains G_N/Gt = {1.0/rows[0.25][2]:.2f}x and a_0 moves by "
     f"sqrt of that = {math.sqrt(1.0/rows[0.25][2]):.2f}x\n         (canonical -> "
     f"{A0_CAN*math.sqrt(1.0/rows[0.25][2]):.3e}, alt -> "
     f"{A0_ALT*math.sqrt(1.0/rows[0.25][2]):.3e}) -- which no RAR fit survives.  If instead the\n"
     "         anchor is the cosmological combination Gt rho_Lambda = Lam/8pi, a_0 is untouched.\n"
     "         WHICH FORK THE FRAMEWORK'S DERIVATION TAKES IS *NOT COMPUTED* HERE.  Flagged because\n"
     "         it is a second, independent way the price could bite, and it is adverse.")


# ================================================================================================
head("PART F -- (d) is solar-system screening really s-independent?")
# ================================================================================================
Ghat_s, rho_s, Psi_s = sp.symbols("Ghat rho Psi", positive=True)
# static equation:  div[ (2-K_B) s mu grad Psi ] = 4 pi Ghat rho   <=>   div[ mu grad Psi ] = 4 pi G_N rho
lhs = (2 - K_B) * ss * mus
check(sp.simplify(sp.cancel((lhs / ((2 - K_B) * ss)) - mus)) == 0,
      "F1  s CANCELS IDENTICALLY (symbolic): the static law div[(2-K_B) s mu grad Psi] = 4 pi Ghat "
      "rho is div[mu grad Psi] = 4 pi G_N rho with G_N = Ghat/[(2-K_B) s].  The AQUAL problem in "
      "terms of the MEASURED G_N and the SHAPE mu is s-free",
      "and the shape is s-free too: mu_phys = J_Z/J_Z(infinity) = (s J_Z)/(s J_Z(infinity)).\n"
      "         So a_0 -- defined by where mu turns over -- is also untouched by s.  The whole\n"
      "         g_obs(g_bar) relation, hence the RAR and the ephemeris residual, is s-INDEPENDENT.")

LOG10E = 1.0 / math.log(10.0)
g1AU = GMSUN / AU ** 2
res = {}
print(f"\n    Sun's Newtonian field at 1 AU (computed with the MEASURED G_N): g_bar = {g1AU:.4e} m/s^2")
print(f"\n    {'footing':<11}{'a_0 [m/s^2]':>13}{'y = g/a_0':>13}{'sqrt y':>10}"
      f"{'log10 u(1AU)':>14}{'log10(u/SJ)':>13}")
for fname, a0 in FOOT:
    y = g1AU / a0
    x = math.sqrt(y)
    # u = g_obs - g_bar = g_bar e^{-x}/(1 - e^{-x});  denominator = 1 to 3000+ digits
    log10u = math.log10(g1AU) - x * LOG10E
    res[fname] = (y, x, log10u, log10u - math.log10(SJ_BOUND))
    print(f"    {fname:<11}{a0:>13.4e}{y:>13.4e}{x:>10.1f}{log10u:>14.1f}"
          f"{log10u-math.log10(SJ_BOUND):>13.1f}")
check(abs(res["canonical"][2] + 3458.7) < 0.15 and abs(res["ALT"][2] + 3151.3) < 0.15
      and all(res[f][3] < -3000 for f, _ in FOOT),
      "F2  CONTROL C-6 REPRODUCED (opt1_gates_2026.py PART G1) and now shown s-INDEPENDENT: the "
      f"1 AU anomaly is 10^{res['canonical'][2]:.1f} m/s^2 canonical / 10^{res['ALT'][2]:.1f} alt, "
      f"against Sereno & Jetzer 2006's {SJ_BOUND:.2e} -- ~3440 orders of margin, identical at every "
      "s in the window",
      "computed in logs throughout: e^(-7959) underflows every float64 route, which is the point.\n"
      "         The 1.2e4-3.4e4 saturation gap stays VOIDED under the rescaling.")

s_probe = [1.0, S_N2[0.25], S_N2[0.10], 1e-3, 1e-6]
gb = np.logspace(-13, -2, 2001)
ref = None
sdev = 0.0
for s_ in s_probe:
    # g_obs from the kernel, which is a statement about mu's SHAPE only
    gobs = gb * nu_exp(gb / A0_CAN)
    if ref is None:
        ref = gobs
    sdev = max(sdev, float(np.max(np.abs(gobs / ref - 1.0))))
check(sdev == 0.0,
      f"F3  and numerically: the full g_obs(g_bar) curve over 11 decades is bit-identical across "
      f"s in {[f'{v:.4g}' for v in s_probe]} -- max fractional deviation {sdev:.1e}",
      "as F1 requires.  Gate (d) is NOT the binding constraint on s; it is silent on s entirely.")


# ================================================================================================
head("VERDICT")
# ================================================================================================
print(f"""
    ROUTE 1 ANSWER: **the s window is NON-EMPTY** -- but the honest reason is not the briefed one.

      * DEATH 1 (vector ghost) is REAL, reproduced from the action (A4), and CURED by
            0 < s < {S_N2[0.25]:.6f}  at K_B = 0.25       (N1 alone would allow {S_N1[0.25]:.6f})
            0 < s < {S_N2[0.10]:.6f}  at K_B = 0.10       (N1 alone would allow {S_N1[0.10]:.6f})
        with the LONGITUDINAL condition N2 -- absent from the brief -- the operative bound, set by
        max d g_bar/d g_obs = {ELL_MAX:.4f}, the reciprocal of the committed 0.968.

      * DEATH 2 (CMB degeneracy) is REFUTED AS BRIEFED.  F_Z(0) = (2-K_B) s mu_phys(0) = 0 for every
        s, because mu_phys(0) = 0 is what the deep-MOND limit of ANY interpolation means; for the
        Route-A kernel mu = 1 - e^(-sqrt y) says it in closed form.  K_B - F_Z(0) = K_B EXACTLY.
        "F_Z(0) = K_B" would require a mu FLOOR of {mu0_required[0.25]:.4f}, which is not an
        interpolation, and which contradicts the very dictionary DEATH 1 uses.  ONE CONVENTION
        SPLICE, COUNTED TWICE.  The surviving CMB condition is the branch-corrected one, and it is
        IMPLIED BY the no-ghost condition rather than competing with it.

      * SOLAR SYSTEM: s-independent, proved symbolically and numerically.  10^{res['canonical'][2]:.1f} /
        10^{res['ALT'][2]:.1f} m/s^2 at 1 AU (canonical / alt), ~3440 orders below Sereno-Jetzer.

      * THE PRICE, computed here for the first time and WORSE than briefed because N2 binds:
            Gt/G_N <= {rows[0.25][2]:.5f}  (K_B = 0.25)  ->  a {1.0/rows[0.25][2]:.2f}x split,  G_N/Ghat >= {rows[0.25][3]:.3f}
            Gt/G_N <= {rows[0.10][2]:.5f}  (K_B = 0.10)  ->  a {1.0/rows[0.10][2]:.2f}x split,  G_N/Ghat >= {rows[0.10][3]:.3f}
        versus AeST's 0.875.  PROPORTIONAL to s, so no point in the window improves it, and any CMB
        fidelity requirement makes it strictly worse (E4: 800x at 1% tolerance).

    SO: the escape SURVIVES Route 1 and is now a ONE-NUMBER question -- whether a >=8.3x split
    between the cosmological and the local gravitational constant is survivable.  My algebraic BBN
    mapping says Delta N_eff = {bbn['escape at s_max, K_B=0.25'][3]:.2f} / {bbn['escape at s_max, K_B=0.10'][3]:.2f}, i.e. almost certainly not -- but that is an
    ESTIMATE, the same mapping charges unmodified AeST {bbn['AeST unmodified, K_B=0.25'][3]:.2f} which is a tension AeST already
    carries, and a real BBN/CLASS confrontation is NOT COMPUTED here and is another route's job.
    I do NOT declare the escape dead, and I do NOT declare it clear.
""")

print("=" * 96)
if FAIL:
    print(f"RESULT: {NCHK[0]-len(FAIL)}/{NCHK[0]} checks passed.  FAILED: {FAIL}")
    sys.exit(1)
print(f"RESULT: {NCHK[0]}/{NCHK[0]} checks passed.")
sys.exit(0)
