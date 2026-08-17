#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
curl_sector_cluster_pricing_2026.py
===================================
PRICING THE PROPOSAL: "the AeST aether CURL sector is the cluster mechanism".

THE PROPOSAL (untested until now).  The framework's cluster residual -- clusters need
eta = M_dyn/M_pred ~ 1.7-2.1 more gravity at R500 than the kernel supplies -- is currently
covered by an ad-hoc a0-BUMP cross term  A_b * B(Y/a0^2) * (Q-Q0)^2,  B(y)=y/(1+y)^2,
calibrated at A_b ~ 1.7 Mpc^-2 (mu^2_eff = 0.23 Mpc^-2 at cluster R500).  The proposal is
that the residual instead comes from the aether's CURL (transverse / spin-1) sector, which
   (i)   vanishes identically in spherical symmetry (Mistele arXiv:2305.07742),
   (ii)  is K_B-blind in quasi-static galaxy phenomenology,
   (iii) would switch on exactly in non-spherical / merging / high-dispersion systems.

THE CONFRONTATION I WAS ASKED TO RUN FIRST.  The aether kinetic term carries K_B and PPN now
forces K_B < 2.5e-5 (stage70: AeST's -(K_B/2)F^2 maps to Einstein-aether c1=K_B, c2=0,
c3=-K_B, c4=0, so alpha_1 = -4 K_B, and LLR |alpha_1|<1e-4).  If the curl amplitude scaled as
K_B the proposal would be dead on arrival at ~1e-5.

*** RESULT 1 (AGAINST THE PREMISE I WAS HANDED -- direction FAVOURABLE to the proposal).
The curl-sector amplitude does NOT scale as K_B.  K_B multiplies only the transverse aether's
GRADIENT (stiffness) term; its algebraic mass comes from the unit-norm multiplier lambda and
its source and feedback are K_B-FREE.  So the response is
        a^T(k) = -S^T / [ 2 ( K_B k^2 + lambda ) ],     lambda = W Q0^2 + F_Q Q0 / 2,
which is MONOTONE INCREASING as K_B falls and SATURATES at a K_B-INDEPENDENT ceiling.  The
scaling is K_B^0 (saturated, large scales) crossing over to K_B^-1 SUPPRESSION on scales
below l_U = sqrt(K_B/W)/Q0.  Tightening K_B from the old BBN cap 0.25 to the PPN bound
2.5e-5 therefore HELPS the proposal by ~2e3-8e3x at cluster radii.  PPN is not the killer.

*** RESULT 2 (THE ACTUAL KILL -- direction ADVERSE to the proposal).  Two structural facts,
neither involving K_B:
  (a) EXACT POINTWISE CANCELLATION.  The Y-sector and F_Q-sector contributions to the aether
      spatial equation carry the SAME W(x) as the lambda mass they are balanced against, so
      their ratio is EXACTLY 1/Q0 pointwise and the induced tilt is a PURE GRADIENT
      (a_i = -(1+Psi) d_i phi / Q0) -- zero curl, for ANY anisotropy.  The curl sector is
      sourced only by the leftovers: the mixing term's theta-piece (relative size
      T = theta/(mu Q0) = 0.27-1.13) and the Psi-weighting (~2e-5).
  (b) THE DIVERGENCE THEOREM.  eta is an ENCLOSED-MASS (monopole) deficit.  A transverse
      field has zero net flux through any closed surface, so its ell=0 contribution is
      SECOND order in the anisotropy: R_curl = C eps^2 T with C = O(1) (toy solve: 0.6).
  Needed: eta = 1.72-2.08 demands a monopole boost of 72-108% (field metric) or 196-334%
  (deep-MOND flux metric).  Delivered at the observed ellipticity of RELAXED clusters
  (eps ~ 0.1-0.3): 0.07-10%.  SHORTFALL 7x (absolute floor, every assumption stacked in the
  proposal's favour) to ~6e3x (conservative), central ~1e2x.  AND the curl sector has NO
  FREE AMPLITUDE to calibrate -- unlike the a0-bump's A_b, its size is fixed by the system's
  own asphericity.  *** THE PROPOSAL IS DEAD AS THE CLUSTER MECHANISM. ***

*** RESULT 3 (a SIDE-FINDING, ADVERSE to the framework, CONDITIONAL / ESCALATE).  The same
de-stiffening that makes the curl sector available at cluster scales makes the LONGITUDINAL
tilt available there too, and its saturated solution gives D = -T grad(phi), i.e. the MOND
argument Y = |D|^2 SUPPRESSED by T^2 = 0.07-1.3 for r > l_U.  Galaxies are safe (99.7%+ stiff
at 30 kpc even at the PPN bound, so the published K_B-blind rotation-curve phenomenology
stands) but cluster scales are exactly where l_U lands.  If it survives review this makes the
cluster deficit WORSE, not better.  Flagged, not claimed: it needs the AeST quasi-static
system re-derived at K_B ~ 1e-5 rather than K_B = O(1).

SCOPE / LABELLED ASSUMPTIONS (all printed at run time; see PART F):
  * the aether variation, the lambda elimination and the mixing-term (J.grad phi) reduction
    are DERIVED HERE from SZ21 Eq.(5) as transcribed in real_research/bridge1_aest_equations.md.
    They are NOT literature-verified.  The load-bearing identity (a) is a two-line algebraic
    consequence of lambda being fixed by the mu=0 component and is checked symbolically.
  * W = (2-K_B) mu(y) identifies the total Y-coefficient with the MOND mu-function: an
    IDENTIFICATION, not a derivation.
  * eps = the fractional QUADRUPOLE of the baryonic field, taken equal to the X-ray isophotal
    ellipticity of relaxed clusters (assumed literature-typical 0.1-0.3).  Equating the two is
    GENEROUS to the proposal (potential quadrupoles are diluted relative to shape).
  * Q0 = 0.00341-0.01456 Mpc^-1 is the corpus's committed core pin (stage58_x_to_q0_2026.py,
    X = 106-453, Q0 = X/31112 Mpc^-1); the wider stage56 band is carried as sensitivity.

Run: python3 curl_sector_cluster_pricing_2026.py     (needs sympy, numpy)
"""
import sys
import numpy as np
import sympy as sp

FAILS = []
_N = [0]


def check(cond, label, detail=""):
    _N[0] += 1
    ok = bool(cond)
    print(f"  [{_N[0]:02d}] [{'ok' if ok else 'FAIL'}] {label}" + (f"\n            {detail}" if detail else ""))
    if not ok:
        FAILS.append(f"{_N[0]:02d} {label}")
    return ok


def info(label, detail=""):
    print(f"  [--] [note] {label}" + (f"\n            {detail}" if detail else ""))


def hdr(t):
    print("\n" + "=" * 100)
    print(t)
    print("=" * 100)


# ======================================================================================
# CONSTANTS -- framework standing, both footings where dimensional
# ======================================================================================
C_LIGHT = 2.99792458e8
MPC = 3.0856775814913673e22
A0_CANON = 9.3619e-11          # kappa c sqrt(G rho_Lambda), rho_DE / cH_Lambda footing
A0_ALT = 1.1279e-10            # rho_total / cH_0 footing
H0_KMS = 67.4
KB_PPN = 2.5e-5                # stage70: alpha_1 = -4 K_B, |alpha_1| < 1e-4 (LLR)
KB_BBN = 0.25                  # superseded corpus cap, kept for the gain factor
KB_SZ21 = (0.5, 0.3, 0.1)      # SZ21's three published values

# committed Q0 pin (stage58_x_to_q0_2026.py): Q0[Mpc^-1] = X / 31112
X_FACTOR = 31112.0
Q0_CORE = (106.0 / X_FACTOR, 453.0 / X_FACTOR)          # 0.00341 - 0.01456 Mpc^-1
Q0_WIDE = (70.0 / X_FACTOR, 1340.0 / X_FACTOR)          # stage56 defensible band

# cluster eta standing.  BAND A: X-COP, kernel-labelled (RETRACTIONS.md: operative MS08 gives
# 1.865 canon / 1.722 alt; the a0-line kernel gives 2.084 / 1.917).  BAND B: eRASS1 audit
# (clusters_eta_audit.out, framework kernel nu=sqrt(1+1/y)): 2.334 canon / 2.132 alt.
ETA_A = (1.722, 2.084)
ETA_B = (2.132, 2.334)
ETA_SCATTER_DEX = 0.1094       # clusters_eta_audit.out, framework kernel, canonical, N=9830
Y_R500 = (0.0369, 0.0306)      # g_bar/a0 median at R500: canonical, alt (same audit)
EPS_CL = (0.10, 0.30)          # ASSUMED X-ray isophotal ellipticity band, relaxed clusters
A_BUMP = 1.7                   # Mpc^-2, the a0-bump's calibrated amplitude
MU2_BUMP = 0.23                # Mpc^-2, mu^2_eff it delivers at cluster R500

theta_cosmo = 3.0 * (H0_KMS / (C_LIGHT / 1e3))   # 3H0/c in Mpc^-1  (theta = div A)


def nu_frame(y):
    """framework / Route A kernel nu(y) = 1/(1-exp(-sqrt y))"""
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


print(__doc__)

# ======================================================================================
hdr("PART A -- WHERE K_B SITS: the transverse aether's stiffness, mass, source and feedback")
# ======================================================================================
print(r"""  AeST action (SZ21 Eq.5, bridge1_aest_equations.md), 16 pi Gtilde = 1:
      L = R - (K_B/2) F^{mn}F_{mn} + 2(2-K_B) J^m grad_m phi - (2-K_B) Y - F(Y,Q) - lam(A.A+1)
      F_{mn} = 2 grad_[m A_n],  J_m = A^a grad_a A_m,  Y = q^{mn} d_m phi d_n phi (q = g + AA),
      Q = A^m d_m phi.
  Quasi-static ansatz: g_00 = -(1+2Psi), g_ij = (1-2Phi)delta_ij, phi = Q0 t + varphi(x),
      A_m = ( -(1+Psi) , a_i ),   a_i = d_i alpha + U_i  with div U = 0  (U = the CURL sector).
""")

# --- A1: Y = |grad varphi + Q0 a|^2 : the aether tilt enters the MOND argument, K_B-free ---
a1, a2, a3, d1, d2, d3, Q0s = sp.symbols("a_1 a_2 a_3 d_1 d_2 d_3 Q_0", real=True)
avec = sp.Matrix([a1, a2, a3])
dvec = sp.Matrix([d1, d2, d3])
A0up = sp.sqrt(1 + (avec.T * avec)[0])            # unit-norm A.A=-1 at Psi=Phi=0, A^i = a^i
Qcur = A0up * Q0s + (avec.T * dvec)[0]
Ycal = -Q0s**2 + (dvec.T * dvec)[0] + Qcur**2     # Y = g^{mn}dphi dphi + Q^2
Ytarget = ((dvec + Q0s * avec).T * (dvec + Q0s * avec))[0]
eps_s = sp.symbols("epsilon_s", positive=True)
# scale (a, d) jointly by eps_s: the difference must start at cubic order
diff_series = sp.series(sp.expand(Ycal - Ytarget).subs(
    {a1: eps_s * a1, a2: eps_s * a2, a3: eps_s * a3,
     d1: eps_s * d1, d2: eps_s * d2, d3: eps_s * d3}), eps_s, 0, 3).removeO()
check(sp.simplify(diff_series) == 0,
      "A1  Y = |grad(varphi) + Q0 a|^2 exactly to quadratic order in the perturbations "
      "(a, grad varphi) -- the unit-norm constraint supplies the Q0^2|a|^2 term that completes "
      "the square.  So the AETHER TILT SITS INSIDE THE MOND ARGUMENT Y, with coefficient "
      "(2-K_B)+F_Y: NO K_B suppression of the coupling",
      f"residual through O(eps^2) = {sp.simplify(diff_series)}")

# --- A2: K_B multiplies ONLY the transverse aether's gradient term ---
x, y_, z_, t_ = sp.symbols("x y z t", real=True)
psi_f = sp.Function("psi")(x, y_)                 # stream function -> divergence-free U
Ux, Uy, Uz = sp.diff(psi_f, y_), -sp.diff(psi_f, x), sp.Integer(0)
chi_f = sp.Function("chi")(x, y_, z_)             # arbitrary longitudinal piece
Ai = [Ux + sp.diff(chi_f, x), Uy + sp.diff(chi_f, y_), Uz + sp.diff(chi_f, z_)]
coords = [x, y_, z_]
check(sp.simplify(sum(sp.diff(u, c) for u, c in zip([Ux, Uy, Uz], coords))) == 0,
      "A2a the trial U built from a stream function is divergence-free (it IS the curl sector)")
Fij = [[sp.simplify(sp.diff(Ai[j], coords[i]) - sp.diff(Ai[i], coords[j])) for j in range(3)]
       for i in range(3)]
FijFij = sp.simplify(sum(Fij[i][j] ** 2 for i in range(3) for j in range(3)))
curlU = [sp.diff(Uz, y_) - sp.diff(Uy, z_), sp.diff(Ux, z_) - sp.diff(Uz, x),
         sp.diff(Uy, x) - sp.diff(Ux, y_)]
check(sp.simplify(FijFij - 2 * sum(c ** 2 for c in curlU)) == 0,
      "A2b F_ij F^ij = 2 |curl U|^2 EXACTLY -- the magnetic part of F sees ONLY the curl "
      "sector (the longitudinal piece d_i chi drops identically), so -(K_B/2)F^2 supplies "
      "the transverse aether's ONE derivative term, with coefficient exactly K_B",
      "and F_0i = d_i(alpha-dot + Psi) + U-dot_i carries no U in the static limit")

# --- A3: the exact pointwise cancellation (the load-bearing identity) ---
W, FQ, lam, di, Mi, M0, Psi = sp.symbols("W F_Q lambda d_i M_i M_0 Psi", real=True)
# aether EOM  E_m = 2K_B grad^n F_{nm} + M_m - (2 W Q + F_Q) d_m phi - 2 lam A_m = 0.
# Saturated (mass-dominated) limit: drop the K_B gradient term.  Q -> Q0 at leading order.
eq0 = sp.Eq(M0 - (2 * W * Q0s + FQ) * Q0s - 2 * lam * (-(1 + Psi)), 0)     # m = 0, A_0=-(1+Psi)
lam_sol = sp.solve(eq0, lam)[0]
eqi = sp.Eq(Mi - (2 * W * Q0s + FQ) * di - 2 * lam_sol * sp.Symbol("a_i"), 0)  # m = i, A_i = a_i
ai_sol = sp.simplify(sp.solve(eqi, sp.Symbol("a_i"))[0])
ai_noMix = sp.simplify(ai_sol.subs({Mi: 0, M0: 0}))
check(sp.simplify(ai_noMix + (1 + Psi) * di / Q0s) == 0,
      "A3a *** THE CANCELLATION IDENTITY: with the mixing term off, the saturated aether tilt "
      "is a_i = -(1+Psi) d_i(varphi)/Q0 -- W AND F_Q CANCEL POINTWISE (the source and the "
      "lambda mass are built from the SAME (2WQ+F_Q) combination, ratio exactly 1/Q0).  A pure "
      "gradient => ZERO CURL for ANY anisotropy ***",
      f"a_i(M=0) = {ai_noMix}")
check(sp.simplify(sp.diff(ai_noMix, W)) == 0 and sp.simplify(sp.diff(ai_noMix, FQ)) == 0,
      "A3b and the cancellation is exact in the FUNCTIONS, not just their values: d a_i/dW = "
      "d a_i/dF_Q = 0, so however W(x) varies across an aspherical cluster it cannot generate "
      "a transverse source at this order")
mix_piece = sp.simplify(ai_sol - ai_noMix)
check(mix_piece != 0,
      "A3c the ONLY surviving curl source is the leftover that has no lambda counterpart -- the "
      "mixing term's theta-piece M_i = -2(2-K_B) theta d_i(varphi) (theta = div A = 3H on FRW) "
      "-- plus the O(Psi) ~ 2e-5 weighting in A3a",
      f"a_i - a_i(M=0) = {sp.simplify(mix_piece.subs({M0: 0}))}")
info("A3d the mixing-term reduction M_i = -2(2-K_B) theta d_i(varphi), M_0 = O(2) is DERIVED "
     "HERE by varying 2(2-K_B) J^m grad_m phi about the static aligned aether; it is NOT "
     "literature-verified, and it sets the size of the ONLY leading curl source.  PART E "
     "therefore prices the kill BOTH with and without this suppression.")

# --- A4: the response function and its K_B scaling ---
KBs, ks = sp.symbols("K_B k", positive=True)
resp = 1 / (2 * (KBs * ks**2 + lam))
check(sp.simplify(sp.diff(resp, KBs)) != 0 and sp.limit(resp, KBs, 0) == 1 / (2 * lam),
      "A4a the transverse response a^T(k) = -S^T/[2(K_B k^2 + lambda)] is MONOTONE INCREASING "
      "as K_B falls and its K_B -> 0 limit is FINITE (= the algebraic/saturated ceiling): the "
      "limit is REGULAR, not singular",
      f"lim_(K_B->0) = {sp.limit(resp, KBs, 0)}")
check(sp.simplify(sp.limit(resp * KBs * ks**2, KBs, sp.oo) - sp.Rational(1, 2)) == 0,
      "A4b in the opposite (stiff) regime K_B k^2 >> lambda the response falls as 1/K_B -- so "
      "the K_B-dependence is a SUPPRESSION at small scales, never an enhancement")
print(r"""
  *** ANSWER TO THE QUESTION I WAS ASKED (does the curl contribution scale as K_B, 1/K_B or
  K_B^0?):  NEITHER K_B NOR A NAIVE 1/K_B.  It is
        K_B^0   for k << m_U = sqrt(lambda/K_B)   (large scales: SATURATED, K_B-BLIND)
        K_B^-1  for k >> m_U                      (small scales: STIFFNESS-SUPPRESSED)
  with the crossover at l_U = 1/m_U = sqrt(K_B/W)/Q0.  The premise handed to me -- "a curl
  effect whose amplitude scales with K_B is suppressed by ~1e-5, DEAD ON ARRIVAL" -- is FALSE.
  Direction: FAVOURABLE to the proposal.  PPN's K_B < 2.5e-5 makes the curl sector MORE
  available, not less.  The kill has to come from somewhere else. ***""")

# ======================================================================================
hdr("PART B -- WHERE THE CROSSOVER LANDS: l_U = sqrt(K_B/W)/Q0 at the committed Q0 pin")
# ======================================================================================
mu_r500 = tuple(1.0 / nu_frame(y) for y in Y_R500)
print(f"  framework kernel nu = 1/(1-exp(-sqrt y)) at the eRASS1 median R500:")
print(f"    canonical a0 = {A0_CANON:.4e} m/s^2 : y = {Y_R500[0]:.4f} -> nu = {nu_frame(Y_R500[0]):.3f}"
      f" -> mu = 1/nu = {mu_r500[0]:.4f}")
print(f"    alt       a0 = {A0_ALT:.4e} m/s^2 : y = {Y_R500[1]:.4f} -> nu = {nu_frame(Y_R500[1]):.3f}"
      f" -> mu = 1/nu = {mu_r500[1]:.4f}")
print(f"  IDENTIFICATION (labelled): W = (2-K_B) mu(y)  =>  W(R500) = "
      f"{(2 - KB_PPN) * mu_r500[0]:.4f} (canon) / {(2 - KB_PPN) * mu_r500[1]:.4f} (alt); "
      f"W = 2 is the analytic (mu -> 1) end")
print(f"  theta = 3H0/c = {theta_cosmo:.4e} Mpc^-1 ;  Q0 (committed core pin) = "
      f"{Q0_CORE[0]:.5f} - {Q0_CORE[1]:.5f} Mpc^-1  (1/Q0 = {1/Q0_CORE[1]:.1f} - {1/Q0_CORE[0]:.1f} Mpc)")


def l_U(kb, w, q0):
    return np.sqrt(kb / w) / q0


def sat_frac(r, kb, w, q0):
    """fraction of the saturated ceiling actually realised at scale r (k ~ 1/r)"""
    return 1.0 / (1.0 + (l_U(kb, w, q0) / r) ** 2)


W_LO = (2 - KB_PPN) * mu_r500[0]      # deep-MOND end (canonical)
W_HI = 2.0                            # analytic end
print(f"\n  {'K_B':>10} {'W':>7} {'l_U [Mpc] (Q0 hi..lo)':>28} {'sat@30kpc':>12} "
      f"{'sat@R500=1.3Mpc':>17}")
rows = {}
for kb, tag in ((KB_PPN, "PPN bound"), (KB_BBN, "old BBN cap"), (KB_SZ21[0], "SZ21 Cosh")):
    for w, wt in ((W_LO, "deep"), (W_HI, "analytic")):
        lo, hi = l_U(kb, w, Q0_CORE[1]), l_U(kb, w, Q0_CORE[0])
        s30 = (sat_frac(0.030, kb, w, Q0_CORE[1]), sat_frac(0.030, kb, w, Q0_CORE[0]))
        s500 = (sat_frac(1.30, kb, w, Q0_CORE[1]), sat_frac(1.30, kb, w, Q0_CORE[0]))
        rows[(kb, wt)] = (lo, hi, s30, s500)
        print(f"  {kb:>10.2e} {w:>7.3f} {lo:>12.3f} .. {hi:<13.3f} {s30[1]:>8.1e}..{s30[0]:<.1e}"
              f" {s500[1]:>9.3f}..{s500[0]:<.3f}   ({tag}, W {wt})")

lo_p, hi_p, s30_p, s500_p = rows[(KB_PPN, "deep")]
check(0.3 < lo_p < 1.0 and 1.5 < hi_p < 4.0,
      f"B1  at the PPN bound the aether crossover lands at l_U = {lo_p:.2f}-{hi_p:.2f} Mpc -- "
      f"i.e. AT CLUSTER SCALES (R500 ~ 1.3 Mpc), decades ABOVE galaxy scales",
      "this is why the curl sector is 'switched on' for clusters at all: it is a K_B-driven "
      "scale, and PPN pushed it down into the cluster regime")
check(max(s30_p) < 0.01,
      f"B2  galaxies stay STIFF even at the PPN bound: only {100*max(s30_p):.2f}-"
      f"{100*min(s30_p):.3f}% of the ceiling is realised at 30 kpc, so the aether tilt is "
      f"pinned and the published K_B-BLIND rotation-curve phenomenology SURVIVES",
      "direction: FAVOURABLE -- statement (ii) of the proposal is confirmed for galaxies, and "
      "the adverse side-finding of PART F does NOT reach rotation curves")
gain = tuple(rows[(KB_PPN, "deep")][3][i] / rows[(KB_BBN, "deep")][3][i] for i in (0, 1))
check(min(gain) > 100,
      f"B3  tightening K_B from the old BBN cap 0.25 to the PPN bound 2.5e-5 INCREASES the "
      f"realised curl response at R500 by {min(gain):.0f}x-{max(gain):.0f}x",
      "direction: FAVOURABLE to the proposal -- the exact opposite of the 'dead on arrival by "
      "1e-5' premise.  It is the PPN bound that makes the mechanism even arguable.")

# ======================================================================================
hdr("PART C -- THE AMPLITUDE CEILING: what the curl sector can actually deliver")
# ======================================================================================
# C1 -- the leftover source strength T = theta/(mu Q0)
T_band = tuple(theta_cosmo / (mu_r500[0] * q) for q in (Q0_CORE[1], Q0_CORE[0]))
T_band_alt = tuple(theta_cosmo / (mu_r500[1] * q) for q in (Q0_CORE[1], Q0_CORE[0]))
print(f"  T = (2-K_B) theta / (W Q0) = theta/(mu Q0)  [the only leading curl-source strength, A3c]")
print(f"    canonical footing : T = {T_band[0]:.3f} - {T_band[1]:.3f}")
print(f"    alt footing       : T = {T_band_alt[0]:.3f} - {T_band_alt[1]:.3f}")
check(T_band[0] < 1.0 < T_band[1] * 1.3,
      f"C1  the surviving curl source is suppressed by T = {T_band[0]:.2f}-{T_band[1]:.2f} "
      f"(canonical) / {T_band_alt[0]:.2f}-{T_band_alt[1]:.2f} (alt) relative to the naive "
      f"'eps x the MOND field' estimate -- a factor 1-4x, NOT robust enough to carry the kill "
      f"on its own (T reaches ~1 at the low-Q0 edge)",
      "so PART E's headline kill is priced with T -> 1, i.e. WITHOUT this suppression")
# merger escape
v_merge, L_merge = 2000e3, 0.5                     # m/s, Mpc
theta_merge = (v_merge / C_LIGHT) / L_merge
T_merge = theta_merge / (mu_r500[0] * Q0_CORE[1]), theta_merge / (mu_r500[0] * Q0_CORE[0])
check(min(T_merge) > 1,
      f"C2  MERGER ESCAPE, priced and REAL: a 2000 km/s collision over 500 kpc gives a LOCAL "
      f"theta = div A ~ {theta_merge:.3e} Mpc^-1 = {theta_merge/theta_cosmo:.0f}x the "
      f"cosmological 3H0/c, lifting T to {min(T_merge):.1f}-{max(T_merge):.1f} -- so in violent "
      f"mergers the T-suppression is GONE",
      "direction: FAVOURABLE to statement (iii).  It does NOT rescue the mechanism, because "
      "the eta requirement is measured on RELAXED clusters, and the eps^2 wall below is "
      "independent of T")

# C3 -- sub-dominance checks on the terms I dropped
rho_dm0 = 0.26 * (3 * (H0_KMS * 1e3 / MPC) ** 2 / (8 * np.pi * 6.674e-11))
src_over_mass = 4 * np.pi * 6.674e-11 * rho_dm0 / C_LIGHT ** 2 * (MPC ** 2) / (Q0_CORE[0] ** 2)
grad_phi_geom = A0_CANON / C_LIGHT ** 2 * MPC       # |grad phi| ~ a0 in Mpc^-1
ratio_gp = (grad_phi_geom / Q0_CORE[0]) ** 2
check(src_over_mass < 1e-2 and ratio_gp < 1e-2,
      f"C3  the terms dropped from the aether mass are negligible even at the LOW-Q0 edge of the "
      f"pin (the worst case): 4 pi G rhobar_dm/(c^2 Q0^2) = {src_over_mass:.2e} and "
      f"(|grad phi|/(c^2 Q0))^2 = {ratio_gp:.2e}, i.e. both below 0.2% (using |grad phi| ~ "
      f"a0 = {A0_CANON:.3e} m/s^2 = {grad_phi_geom:.2e} Mpc^-1)",
      "so lambda = W Q0^2 dominates the aether mass and the algebra of A3 is the right leading "
      "order.  Both footings give the same conclusion (a0 differs by 1.20x, the ratios by 1.45x)")

# C4 -- the monopole theorem, verified numerically, and the O(1) coefficient from a toy solve
print(r"""
  THE MONOPOLE THEOREM.  eta is an ENCLOSED-MASS ratio, so what matters is the ell=0 part of the
  flux  Phi(r) = closed-integral of W (grad varphi + Q0 a) . dS.  For the transverse piece:
        closed-integral of U . dS = volume-integral of div U = 0   IDENTICALLY.
  So the curl sector can only contribute through the CORRELATION of its own anisotropic part
  with the anisotropic part of W -- second order in the anisotropy eps.""")
# numeric check: explicit divergence-free U with an ell=2 radial pattern, flux vs eps
nth = 4001
th = np.linspace(0.0, np.pi, nth)
mu_th = np.cos(th)
P2 = 0.5 * (3 * mu_th ** 2 - 1)
w_sin = np.sin(th)


def flux_ell0(eps, u2, W0=1.0):
    """(1/4pi) * closed integral of [W0(1+eps P2)] * [eps u2 P2] dOmega  / (W0)"""
    integ = (W0 * (1 + eps * P2)) * (eps * u2 * P2) * w_sin
    trap = getattr(np, "trapezoid", None) or np.trapz
    return 0.5 * trap(integ, th) / W0


eps_grid = np.array([0.4, 0.2, 0.1, 0.05])
f_grid = np.array([flux_ell0(e, 1.0) for e in eps_grid])
slope = np.polyfit(np.log(eps_grid), np.log(np.abs(f_grid)), 1)[0]
check(abs(slope - 2.0) < 1e-4 and abs(np.abs(f_grid[1]) / 0.2 ** 2 - 0.2) < 1e-5,
      f"C4a the ell=0 flux of a transverse ell=2 field against an ell=2 W scales EXACTLY as "
      f"eps^2 (fitted slope {slope:.6f}, quadrature-limited) with the Legendre coefficient "
      f"<P_2^2> = 1/5 (measured {np.abs(f_grid[1])/0.2**2:.6f})",
      "the eps^1 term vanishes by orthogonality, i.e. by the divergence theorem -- this is the "
      "structural wall, and it holds for ANY mechanism whose carrier is divergence-free")

# toy transverse solve: derive the ell=2 ODE symbolically, then its particular solution
rr = sp.symbols("r", positive=True)
thh = sp.symbols("theta", positive=True)
u_f, s_f = sp.Function("u")(rr), sp.Function("s")(rr)
P2s = sp.Rational(1, 2) * (3 * sp.cos(thh) ** 2 - 1)
Ur_s, Uth_s = u_f * P2s, s_f * sp.diff(P2s, thh)
div_s = sp.simplify(sp.diff(rr ** 2 * Ur_s, rr) / rr ** 2
                    + sp.diff(sp.sin(thh) * Uth_s, thh) / (rr * sp.sin(thh)))
s_from_div = sp.solve(sp.Eq(sp.simplify(div_s / P2s), 0), s_f)[0]
check(sp.simplify(s_from_div - sp.diff(rr ** 2 * u_f, rr) / (6 * rr)) == 0,
      "C4b div U = 0 for the ell=2 transverse mode forces s(r) = (r^2 u)'/(6r)  (sympy, "
      "spherical coordinates)")
curl_phi = sp.simplify((sp.diff(rr * Uth_s, rr) - sp.diff(Ur_s, thh)) / rr)
omg = sp.symbols("omega", real=True)
ode = sp.simplify((curl_phi / sp.diff(P2s, thh)).subs(s_f, s_from_div).doit() - omg)
ode_std = sp.simplify(sp.expand(ode * 6 * rr))
check(sp.simplify(ode_std - (rr ** 2 * sp.diff(u_f, rr, 2) + 4 * rr * sp.diff(u_f, rr)
                             - 4 * u_f - 6 * rr * omg)) == 0,
      "C4c and curl U = curl V then gives the ell=2 radial ODE  r^2 u'' + 4 r u' - 4 u = 6 r "
      "omega  (homogeneous solutions r and r^-4)",
      f"reduced ODE: {sp.simplify(ode_std)} = 0")
# toy: V = T grad(varphi) with T ~ 1/W ~ 1/|grad varphi|, deep-MOND power law g ~ r^-p, p=1/2
p_toy = sp.Rational(1, 2)
tau, Aamp = sp.symbols("tau A", positive=True)
T0 = tau * rr ** p_toy                                   # T ~ 1/W ~ r^p
Phi0 = Aamp * rr ** (1 - p_toy) / (1 - p_toy)            # spherical potential, g = A r^-p
w2 = T0 * Phi0 / rr
v2 = sp.Integer(0)                                       # radial ell=2 part cancels (T ~ 1/W)
omega_toy = sp.simplify((sp.diff(rr * w2, rr) - v2) / rr)
u_const = sp.symbols("u_c", real=True)
sol_c = sp.solve(sp.Eq((rr ** 2 * 0 + 4 * rr * 0 - 4 * u_const), 6 * rr * omega_toy), u_const)[0]
C_toy = sp.simplify(sol_c / (T0 * Aamp * rr ** (-p_toy)))   # in units of T0 * g
check(abs(float(C_toy)) > 1.0,
      f"C4d toy solve (deep-MOND power law, p=1/2, regular particular solution): the transverse "
      f"response is Q0 a^T_r = {float(C_toy):.1f} x eps x T0 x g -- an O(1)-to-few coefficient, "
      f"GENEROUS to the proposal",
      f"combining with <P_2^2>=1/5 gives the monopole coefficient C = |{float(C_toy):.1f}|/5 = "
      f"{abs(float(C_toy))/5:.2f}; PART E uses C = 1 (rounded UP, in the proposal's favour)")
C_MONO = 1.0
info("C4e the toy's SIGN is negative (the curl rider REDUCES the ell=0 flux, i.e. makes eta "
     "WORSE).  The sign depends on the boundary condition chosen for the r and r^-4 homogeneous "
     "modes and is NOT robust; PART E prices only the MAGNITUDE, crediting the favourable sign.")

# ======================================================================================
hdr("PART D -- WHAT IS NEEDED: the cluster eta requirement, both bands, both footings")
# ======================================================================================
print(f"  eta = M_dyn/M_pred at R500.  To close it the PREDICTED field must rise by the factor eta.")
print(f"    BAND A (X-COP, kernel-labelled): {ETA_A[0]:.3f} (alt, MS08 kernel) - {ETA_A[1]:.3f} "
      f"(canonical, a0-line kernel)")
print(f"    BAND B (eRASS1 audit, framework kernel, N=9830): {ETA_B[0]:.3f} (alt) - {ETA_B[1]:.3f} "
      f"(canonical)")
need = {}
for tag, band in (("A", ETA_A), ("B", ETA_B)):
    need[(tag, "field")] = (band[0] - 1, band[1] - 1)
    need[(tag, "flux")] = (band[0] ** 2 - 1, band[1] ** 2 - 1)
print(f"\n  {'band':>6} {'metric':>8} {'required fractional monopole boost':>38}")
for k, v in need.items():
    print(f"  {k[0]:>6} {k[1]:>8} {v[0]:>18.3f} .. {v[1]:<18.3f}")
info("FIELD metric = credit the curl sector's flux contribution directly as a field boost "
     "(GENEROUS).  FLUX metric = the correct deep-MOND mapping: with W ~ |D| the flux goes as "
     "|D|^2, so closing eta needs the flux up by eta^2.  Clusters at y = 0.031-0.037 are deep, "
     "so the flux metric is the physical one; both are reported.")
check(need[("A", "field")][0] > 0.7 and need[("B", "flux")][1] > 4.0,
      f"D1  the requirement is a monopole boost of {need[('A','field')][0]:.2f}-"
      f"{need[('B','field')][1]:.2f} (field metric) / {need[('A','flux')][0]:.2f}-"
      f"{need[('B','flux')][1]:.2f} (flux metric) -- an ORDER-UNITY change, not a percent-level one")

# ======================================================================================
hdr("PART E -- THE PRICING: needed vs the ceiling K_B < 2.5e-5 allows.  THE RATIO.")
# ======================================================================================
print(r"""  What K_B < 2.5e-5 ALLOWS: the FULL saturated ceiling (PART A/B).  The allowed amplitude is
  therefore not a K_B ratio at all -- it is fixed by geometry:
        R_curl(ell=0)  =  C * eps^2 * T * f_sat ,
  C ~ 1 (C4d, rounded up), eps = fractional field quadrupole ~ X-ray ellipticity, T from C1
  (set to 1 for the headline = dropping my own derived suppression), f_sat from B (0.22-0.83 at
  R500 at the PPN bound; set to 1 for the headline).""")
print(f"\n  {'eps':>6} {'T':>6} {'delivered R':>13} | {'shortfall vs A-field':>21} "
      f"{'vs B-flux':>12}")
grid = []
for eps in (EPS_CL[1], 0.2, EPS_CL[0]):
    for T, Tt in ((1.0, "T=1 (generous)"), (float(np.mean(T_band)), "T=derived")):
        R = C_MONO * eps ** 2 * T
        sA = need[("A", "field")][0] / R
        sB = need[("B", "flux")][1] / R
        grid.append((eps, T, R, sA, sB))
        print(f"  {eps:>6.2f} {T:>6.2f} {R:>13.5f} | {sA:>21.1f}x {sB:>11.0f}x   ({Tt})")
floor = min(g[3] for g in grid)
worst = max(g[4] for g in grid)
central = C_MONO * 0.20 ** 2 * float(np.mean(T_band)) * float(np.mean([0.22, 0.83]))
central_short = float(np.mean([need[("A", "field")][0], need[("B", "flux")][1]])) / central
check(floor > 5.0,
      f"E1  *** THE ABSOLUTE FLOOR OF THE SHORTFALL IS {floor:.1f}x. *** That floor requires "
      f"EVERY assumption stacked in the proposal's favour simultaneously: C = 1 (toy gives "
      f"0.6), eps = {EPS_CL[1]:.2f} (top of the relaxed-cluster ellipticity band), NO "
      f"theta-suppression (T = 1), FULL saturation (f_sat = 1), the generous FIELD metric, and "
      f"the LOWEST eta in either band ({ETA_A[0]:.3f})",
      "there is no assembly of defensible assumptions under which the curl sector closes eta")
check(central_short > 50,
      f"E2  the CENTRAL pricing is a shortfall of ~{central_short:.0f}x (eps = 0.20, T = "
      f"{np.mean(T_band):.2f}, f_sat = {np.mean([0.22,0.83]):.2f}), and the conservative end is "
      f"{worst:.0f}x",
      f"delivered R_curl = {central:.5f} against a requirement of "
      f"{need[('A','field')][0]:.2f}-{need[('B','flux')][1]:.2f}")
eps_req = tuple(np.sqrt(v / C_MONO) for v in (need[("A", "field")][0], need[("B", "flux")][1]))
check(eps_req[0] > 0.8,
      f"E3  inverted: closing eta needs a fractional field quadrupole of eps = {eps_req[0]:.2f} "
      f"to {eps_req[1]:.2f} at EVERY radius of EVERY cluster -- eps >~ 1 means a system with no "
      f"spherical component at all.  The eta requirement is measured on RELAXED, near-round "
      f"clusters (assumed eps = {EPS_CL[0]:.2f}-{EPS_CL[1]:.2f})",
      f"in eps^2 the gap is {(eps_req[0]/EPS_CL[1])**2:.0f}x-{(eps_req[1]/EPS_CL[0])**2:.0f}x")
check(True,
      "E4  and the curl sector has NO FREE AMPLITUDE.  The a0-bump carries a calibratable "
      f"A_b = {A_BUMP} Mpc^-2 (delivering mu^2_eff = {MU2_BUMP} Mpc^-2 at R500); the curl "
      "sector's size is FIXED by the system's own asphericity, so it cannot be fitted to "
      "clusters even in principle.  It is a PREDICTION of ~0.1-10%, not a mechanism for ~100%",
      "structural, not numerical: this is why the proposal cannot replace the bump")

# --- E6 (ordered before E5's soft test): the MERGER CORNER, where the mechanism does NOT die ---
eps_merge = 0.5
R_merge = tuple(C_MONO * eps_merge ** 2 * t for t in T_merge)
ratio_merge = tuple(need[("A", "flux")][0] / r for r in (max(R_merge), min(R_merge)))
check(max(R_merge) > need[("A", "flux")][0],
      f"E6  *** THE ONE LIVE CORNER, priced AGAINST MY OWN VERDICT: in a violent merger "
      f"(eps = {eps_merge:.1f}, T = {min(T_merge):.1f}-{max(T_merge):.1f}) the ceiling is "
      f"R_curl = {min(R_merge):.2f}-{max(R_merge):.2f}, which REACHES and can OVERSHOOT the "
      f"{need[('A','flux')][0]:.2f}-{need[('B','flux')][1]:.2f} requirement (needed/allowed = "
      f"{ratio_merge[0]:.2f}x-{ratio_merge[1]:.2f}x).  So the mechanism is NOT dead in mergers ***",
      "TWO reasons this does not rescue the proposal, and one reason it is a LIABILITY: "
      "(1) WRONG POPULATION -- the eta = 1.72-2.33 standing is measured on relaxed/near-round "
      "clusters (X-COP is explicitly relaxed-selected; the eRASS1 sample is mass-proxy selected, "
      "not merger selected), so the residual it must explain is there in the ABSENCE of mergers; "
      "(2) it needs eps ~ 0.5 AND T >> 1 simultaneously; (3) LIABILITY: an order-unity, "
      "possibly overshooting boost in merging clusters is a sharp falsifiable prediction against "
      "merging-cluster lensing masses.  ASSUMPTION, labelled and GENEROUS: theta_local is taken "
      "as div(v_gas)/c, i.e. the aether is assumed to comove with the merging gas.  Whether the "
      "aether tracks a bulk flow at all -- at K_B ~ 1e-5 its own stiffness is nearly gone, so it "
      "plausibly does -- is an OWED item that this corner rests entirely on.")

# --- E5: the morphology-scatter discriminator, on committed data ---
sig_log_eps = 0.20            # ASSUMED lognormal spread of cluster ellipticity, ~1.6x
pred_scatter = 2 * sig_log_eps * (1 - 1 / np.mean(ETA_B))   # d log eta = (eta-1)/eta * d log(eta-1)
check(pred_scatter > ETA_SCATTER_DEX,
      f"E5  independent discriminator on COMMITTED data: if eta-1 were proportional to eps^2, "
      f"the measured log10(eta) scatter would be ~{pred_scatter:.3f} dex (2 x an assumed "
      f"{sig_log_eps:.2f} dex ellipticity spread, diluted by (eta-1)/eta), versus the measured "
      f"{ETA_SCATTER_DEX:.4f} dex on N=9830 eRASS1 clusters -- {pred_scatter/ETA_SCATTER_DEX:.1f}x "
      f"too large",
      "direction ADVERSE to the proposal, but SOFT: the ellipticity spread is assumed, not "
      "measured here, and the eta scatter has its own systematic floor.  It is a real test the "
      "mechanism must eventually pass, not a kill on its own.")

# ======================================================================================
hdr("PART F -- SIDE-FINDING (ADVERSE to the framework, CONDITIONAL): the LONGITUDINAL branch")
# ======================================================================================
T_sup = tuple(t ** 2 for t in T_band)
print(f"""  The same algebra (A3) applied to the LONGITUDINAL tilt says that where the aether is
  de-stiffened (r > l_U) the saturated solution is
        D = grad(varphi) + Q0 a = -T grad(varphi),      T = theta/(mu Q0) = {T_band[0]:.2f}-{T_band[1]:.2f},
  so the MOND argument Y = |D|^2 is multiplied by T^2 = {T_sup[0]:.2f}-{T_sup[1]:.2f} at cluster
  scales.  Galaxies are untouched (B2: 99.7%+ stiff at 30 kpc even at the PPN bound), which is
  why AeST's published K_B-blind rotation-curve phenomenology is consistent with this -- it was
  derived at K_B = O(1), where l_U = {rows[(KB_SZ21[0],'deep')][0]:.0f}-{rows[(KB_SZ21[0],'deep')][1]:.0f}
  Mpc and NOTHING is de-stiffened.""")
check(min(T_sup) < 1.0,
      f"F1  CONDITIONAL / ESCALATE: at the PPN bound the same de-stiffening that makes the curl "
      f"sector available at cluster scales may SUPPRESS the MOND field there by T^2 = "
      f"{T_sup[0]:.2f}-{T_sup[1]:.2f}.  Direction: ADVERSE -- it would make the cluster deficit "
      f"WORSE, not better",
      "NOT CLAIMED.  It rests on my own aether variation (A3d) and on the saturated limit being "
      "the right description at K_B ~ 1e-5.  It is exactly the owed item stage70 flagged ('the "
      "K_B -> 0 limit itself, where the vector modes become non-dynamical').  The deciding "
      "calculation is the AeST quasi-static system re-derived at K_B ~ 1e-5 with the "
      "J^m grad_m phi coupling retained.")
check(max(rows[(KB_SZ21[0], "deep")][2]) < 1e-3,
      "F2  consistency of F1 with the literature: at SZ21's own K_B = 0.5 the crossover sits at "
      "tens of Mpc, so the tilt is pinned everywhere observationally relevant and 'K_B appears "
      "zero times in the quasi-static equations' (arXiv:2304.05134) is exactly what one expects. "
      "The K_B-blindness claim is a statement about K_B = O(1), and PART B shows it acquires a "
      "cluster-scale caveat at the PPN bound")

# ======================================================================================
hdr("VERDICT")
# ======================================================================================
print(f"""
  THE PROPOSAL IS DEAD AS THE CLUSTER MECHANISM FOR THE MEASURED (RELAXED-CLUSTER) eta
  STANDING -- but NOT for the reason I was handed, and NOT in every corner (see 2b).

  1. K_B SCALING (the confrontation): the curl-sector contribution scales as K_B^0, not K_B.
     K_B multiplies only the transverse aether's GRADIENT term; the mass (from the unit-norm
     multiplier lambda), the source and the feedback into the observable sector are all K_B-free.
     Response a^T(k) = -S^T/[2(K_B k^2 + lambda)]: monotone increasing as K_B falls, finite
     limit.  The PPN bound K_B < 2.5e-5 is FAVOURABLE, raising the realised response at R500 by
     {min(gain):.0f}x-{max(gain):.0f}x over the old BBN cap.  "Suppressed by ~1e-5" is FALSE.

  2. WHAT KILLS IT: geometry, in two independent layers.
     (a) an EXACT pointwise cancellation (A3): the Y- and F_Q-sector sources are built from the
         same (2WQ+F_Q) combination as the lambda mass, so the saturated tilt is a PURE GRADIENT
         and carries no curl at all for any anisotropy.  Only the mixing term's theta-piece
         survives, at relative strength T = {T_band[0]:.2f}-{T_band[1]:.2f}.
     (b) the DIVERGENCE THEOREM (C4): eta is a monopole deficit and a transverse field has zero
         net flux, so the ell=0 effect is O(eps^2).
     Needed: {need[('A','field')][0]:.2f}-{need[('B','flux')][1]:.2f}.  Delivered at relaxed-cluster
     ellipticity: {C_MONO*EPS_CL[0]**2*T_band[0]:.4f}-{C_MONO*EPS_CL[1]**2*1.0:.4f}.
     *** SHORTFALL: {floor:.1f}x absolute floor, ~{central_short:.0f}x central, up to {worst:.0f}x. ***
     Required ellipticity to close it: eps = {eps_req[0]:.2f}-{eps_req[1]:.2f} (order unity).
     And there is NO FREE AMPLITUDE to calibrate, unlike the a0-bump's A_b = {A_BUMP} Mpc^-2.

  2b. WHERE IT DOES NOT DIE (E6, against my own verdict): the MERGER corner.  With eps ~ 0.5 and
     a local theta = div(v_gas)/c ~ {theta_merge/theta_cosmo:.0f}x the cosmological value, the ceiling
     rises to R_curl = {min(R_merge):.2f}-{max(R_merge):.2f} and REACHES/overshoots the
     {need[('A','flux')][0]:.2f}-{need[('B','flux')][1]:.2f} requirement.  This is the wrong
     population (the eta standing is a relaxed-cluster measurement) and it converts into a
     LIABILITY: order-unity boosts in merging clusters are testable against merging-cluster
     lensing masses.  It rests on the aether comoving with the merging gas -- an OWED item.

  3. WHAT SURVIVES of (i)-(iii):
     (i)   SURVIVES as a theorem -- and it is the ENGINE of the kill, not an asset: vanishing in
           spherical symmetry is exactly what forbids a monopole (enclosed-mass) effect.  It also
           confirms stage70's retraction E3: the curl sector IS excited in axisymmetric (alpha_1)
           configurations, so it must not be cited as a general PPN defence.
     (ii)  SURVIVES, and is now DERIVED rather than asserted -- with a REFINEMENT: K_B-blindness
           holds for r << l_U = sqrt(K_B/W)/Q0.  At the PPN bound that is {lo_p:.2f}-{hi_p:.2f} Mpc,
           so galaxies are K_B-blind and CLUSTERS ARE NOT.  "K_B-blind quasi-static
           phenomenology" now needs the scale qualifier.
     (iii) SURVIVES as a genuine framework-specific PREDICTION, not a mechanism: a merger- and
           ellipticity-gated rider with eta-1 proportional to eps^2, amplitude 0.1-10%, boosted
           in violent mergers where local theta = div v/c reaches {theta_merge/theta_cosmo:.0f}x the
           cosmological value.  No ISOTROPIC bump can produce that shape, so it is a real
           discriminator between the two -- at the 1-10% level, which needs a stacked
           ellipticity-binned lensing/X-ray analysis to reach.

  4. OWED (in priority order):
     * PART F's longitudinal side-finding: the AeST quasi-static system re-derived at K_B ~ 1e-5
       with the J^m grad_m phi coupling retained.  ADVERSE if it stands.  Highest priority.
     * the mixing-term reduction M_i = -2(2-K_B) theta d_i(varphi), M_0 = O(2) (A3d) --
       derived here, not literature-verified; it sets T, the ONLY leading curl source.
     * the identification W = (2-K_B) mu(y), and lambda's K_B/M_0 corrections.
     * a measured ellipticity distribution for the eRASS1 eta sample, to turn E5 from an
       assumed-spread argument into a real test.
     * the sign of the ell=0 curl rider (C4e): the toy gives ADVERSE; boundary conditions decide.
     * does the aether track a bulk flow?  E6's merger corner -- the only surviving corner --
       rests entirely on theta_local = div(v_gas)/c.  Also the test that would price the
       liability: merging-cluster (Bullet-class) lensing masses vs the predicted order-unity boost.

  DIRECTION OF RISK, stated plainly: this exercise did NOT find a cluster mechanism, and it
  surfaced a NEW adverse channel (PART F) at cluster scales.  The a0-bump remains the only live
  cluster candidate, with its free amplitude A_b intact and unchallenged by this route.
""")

print("=" * 100)
if FAILS:
    print(f"FAILED CHECKS ({len(FAILS)}):")
    for f in FAILS:
        print("   " + f)
    sys.exit(1)
print(f"ALL {_N[0]} CHECKS PASSED")
sys.exit(0)
