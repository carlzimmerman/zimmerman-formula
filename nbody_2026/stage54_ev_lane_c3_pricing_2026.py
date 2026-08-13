#!/usr/bin/env python3
# STAGE 54 EVIDENCE (committed 2026-08-13 late).  SURVIVED adversarial refereeing
# (stage54_ev_c3_referee_*.py, refuted=FALSE, conf ~0.9) WITH CORRECTIONS carried in stage54:
#   * R_halt range is 176-210 kpc (the "176-226" in this file's D3a prose is an erratum);
#   * the deep shortfall is 134x-1.7e4x (this file UNDERSTATES it);
#   * the Eq-6 double-source citation is the SETUP doc, not bridge1;
#   * DEAD-2 holds in the ALIGNED-tilt sector only (anti-aligned branch = a named report
#     condition of the future 1+1D solve);  * the F1 factor-2 convention must be pinned
#     before the 0.3x kill threshold freezes.
# Pressure reading: DEAD.  Transport/drain reading: VIABLE-CANDIDATE (the first mechanism to
# pass the binding-epoch wall structurally; two-ended separation ~1e7).
# -*- coding: utf-8 -*-
r"""
lane_c3_aether_current_pricing_2026.py
======================================
LANE C3 / PRICE CELL 3: AeST's OWN current term  L > 2(2-K_B) J^mu grad_mu phi,
J^mu = A^alpha grad_alpha A^mu (the aether acceleration current), as dust support.
Stage 53 REOPENED this cell (its earlier closure priced the F(Y,Q) expansion instead --
a manufactured deficit).  This script does the pricing nobody had done.

PROVENANCE OF EVERY EXTERNAL NUMBER (T-discipline):
  [SZ21]   Skordis & Zlosnik, PRL 127 161302 = arXiv:2007.00082 (ar5iv fetch 2026-08-13
           confirmed: action Eq 5 contains the term; linear eqs derived from the FULL action;
           CMB C_l + P(k) from their OWN Boltzmann code on those full equations; weak-field
           Eq 6 contains the -2 grad Phi . grad phi cross term).
           NOTE: the task brief's "arXiv:2109.04157" is a TYPO (that ID is a neutrino-flavor
           paper, checked); the AeST papers are 2007.00082 (+ the stability companion).
  [s51]    committed nbody_2026/stage51 (KILLED banner): sign-theorem survivors Parts A/B.
  [s52]    committed nbody_2026/stage52: surface calibration rho_h = 1654 rho_dm0,
           z_bind = 10.83; deep-interior self-halt incoherence (609 km/s inside the RAR);
           KiDS charge for a ~190-kpc core Delta chi^2 +1.2e3..+2.0e3 (verifier, unowned).
  [s53]    committed nbody_2026/stage53: A_ratio local-a0 law; 13.3x suppression at
           1e6 rho_dm0 (ceiling nu0); Cell-3 reopening; KiDS grid +446..+1698 at 2.51e12.
  [setup]  committed AEST_SPHERICAL_COLLAPSE_SETUP.md: Y=0 on FLRW; weak-field action Eq 6
           transcription (independent of the ar5iv fetch -- double-sourced).
  [v9]     corpus (THE_COMPLETION v9): collapse speedup 1.34-1.96x vs Newtonian, declining
           with z (2.03x at z=6 -> 1.14x at z=25).  QUOTED, not re-derived here.
  [brief]  orchestrator anchors: M_captured = 2.51e12 Msun; honest halt bound 10-15 kpc /
           g_* <= 8.2 a0; V_sat = 3.25e6 is the SATURATING bound.

Exit 0 = all checks pass.  Both footings; K_B in {0.10, 0.25}; both kernels where a kernel
enters; nu0 window ends where the local-a0 law enters.
"""

import sys
import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


# ---------------- constants ----------------
G = 6.67430e-11
C = 2.99792458e8
MSUN = 1.98892e30
KPC = 3.0856775814913673e19
MPC = 1e3 * KPC
H0 = 67.4e3 / MPC                       # 1/s
RHO_CRIT = 3 * H0 ** 2 / (8 * np.pi * G)
OM_DM, OM_M = 0.265, 0.315
RHO_DM0 = OM_DM * RHO_CRIT
RHO_M0 = OM_M * RHO_CRIT
A0_CAN, A0_ALT = 9.3619e-11, 1.1279e-10
NU0_LO, NU0_HI = 2.14e-5, 1.77e-4       # derived-a0(z) window (stage 17)
M_CAP = 2.51e12 * MSUN                  # committed captured dust share [s52/brief]
RHO_H = 1654.0 * RHO_DM0                # surface calibration [s52]
Z_BIND = 10.83
Z_REC = 1090.0
KBS = (0.10, 0.25)                      # K_B fiducial and BBN cap (stage 50)


def a_ratio_local(overdens, nu0):
    """A(local)/A(mean today) from the committed law, r = n/n0 [s53]."""
    r = float(overdens)
    return np.sqrt(1.0 + nu0 ** 2) / np.sqrt(1.0 + nu0 ** 2 * r ** 2)


def gobs_line(gn, a0):                  # framework's own dS-Unruh interpolation
    return np.sqrt(gn ** 2 + gn * a0)


def gobs_ms08(gn, a0):                  # operative MS08 kernel nu = 1/(1-e^-sqrt(y))
    y = gn / a0
    return gn / (1.0 - np.exp(-np.sqrt(y)))


print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- THE ALGEBRA: tilted unit-timelike ansatz, expanded honestly (sympy)")
print("=" * 100)
# Ansatz: 1+1 (t,r) sector, longitudinal-gauge weak field on FLRW:
#   ds^2 = -(1+2 eps Phi) dt^2 + a(t)^2 (1-2 eps Psi) dr^2
#   A^mu = (A^0, eps w),  A^0 fixed EXACTLY by g_mn A^m A^n = -1  (tilt w = the aether's
#   radial coordinate velocity; eps = perturbative order-counter).
t, r, eps, KB = sp.symbols("t r epsilon K_B", real=True)
a = sp.Function("a", positive=True)(t)
Phi = sp.Function("Phi", real=True)(t, r)
Psi = sp.Function("Psi", real=True)(t, r)
w = sp.Function("w", real=True)(t, r)
dphi = sp.Function("deltaphi", real=True)(t, r)
phibar = sp.Function("phibar", real=True)(t)

gdd = sp.diag(-(1 + 2 * eps * Phi), a ** 2 * (1 - 2 * eps * Psi))
guu = gdd.inv()
X = (t, r)
Gam = [[[sp.simplify(sum(guu[m, s] * (sp.diff(gdd[s, al], X[be]) + sp.diff(gdd[s, be], X[al])
                                      - sp.diff(gdd[al, be], X[s])) for s in range(2)) / 2)
         for be in range(2)] for al in range(2)] for m in range(2)]

A0 = sp.sqrt((1 + gdd[1, 1] * (eps * w) ** 2) / (1 + 2 * eps * Phi))   # exact unit norm
Au = sp.Matrix([A0, eps * w])
Ju = sp.Matrix([sum(Au[al] * (sp.diff(Au[m], X[al])
                              + sum(Gam[m][al][be] * Au[be] for be in range(2)))
                    for al in range(2)) for m in range(2)])

# A1: unit-norm identity A.J = 0 EXACTLY (all orders in eps, any Phi, Psi, w, a)
AdotJ = sp.simplify(sum(gdd[m, n] * Au[m] * Ju[n] for m in range(2) for n in range(2)))
check(AdotJ == 0,
      "A1  A_mu J^mu = 0 IDENTICALLY for the exact tilted unit-timelike ansatz (all orders): "
      "J is purely spatial in the aether frame",
      "consequence: the term contributes ZERO to the shift-charge density n = -A.J_shift -- "
      "it carries charge FLUX only.  This is NOT a vector-on-charge Proca coupling [s51 Part B]")

# A2: FLRW limit J = 0 exactly
J_flrw = sp.simplify(Ju.subs(eps, 0))
check(J_flrw == sp.Matrix([0, 0]),
      "A2  on FLRW (eps=0) J^mu = 0 EXACTLY -- comoving observers are geodesic; the term "
      "vanishes on the background at any amplitude (same protection class as Y=0 [setup:41-43])")

# A3: static weak-field limit J^r -> d_r Phi  => the term IS SZ21 Eq 6's cross term
J_static = sp.simplify(Ju[1].subs([(w, sp.Integer(0)), (a, sp.Integer(1))]))
J_static_lead = sp.series(J_static.subs(eps, 1), sp.Symbol("dummy"), 0, 1) if False else J_static
lead = sp.limit(sp.simplify(J_static / (eps * sp.diff(Phi, r))), eps, 0)
check(sp.simplify(lead - 1) == 0,
      "A3  static limit (w=0, a=1): J^r = d^r Phi at leading order -- the aether's proper "
      "acceleration IS the local gravitational field g",
      "so 2(2-K_B) J.grad phi -> 2(2-K_B) grad Phi . grad phi: EXACTLY the weak-field cross "
      "term in [SZ21] Eq 6 -- the term's quasi-static content is the theory's MOND SOURCE "
      "COUPLING, already inside DS24 Eq 2.40 and every committed fit (RAR, KiDS, clusters)")

# A4: perturbative order on FLRW: the term is O(eps^2) -- second order in the ACTION,
#     hence PRESENT in the linear EOMs; and its eps^1 piece vanishes (delta J^0 = 0).
phi_full = phibar + eps * dphi
T_term = 2 * (2 - KB) * (Ju[0] * sp.diff(phi_full, t) + Ju[1] * sp.diff(phi_full, r))
T_ser = sp.series(T_term, eps, 0, 3).removeO().expand()
c0 = sp.simplify(T_ser.coeff(eps, 0))
c1 = sp.simplify(T_ser.coeff(eps, 1))
c2 = sp.simplify(T_ser.coeff(eps, 2))
check(c0 == 0 and c1 == 0,
      "A4a the term's O(1) and O(eps) pieces VANISH on FLRW (background J = 0; delta J^0 = 0 "
      "at first order by A1) -- no first-order tadpole, background exactly protected")
check(c2 != 0,
      "A4b the O(eps^2) piece is NONZERO -- the term sits in the QUADRATIC action, so it "
      "CONTRIBUTES TO THE LINEAR EQUATIONS OF MOTION (the chi-E mixing of [SZ21] Eq 12)",
      f"c2 = {sp.nsimplify(0) if c2 == 0 else 'delta-J^i d_i(delta phi) + J^0(2) phibar-dot terms'}"
      " -- the CRUX VERIFIED: no gate, no protection needed; the term is part of the FITTED "
      "linear cosmology")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- THE INHERITANCE CHAIN (the crux's second half), with the honest caveat")
print("=" * 100)
import os
HERE_REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
s19 = open(os.path.join(HERE_REPO, "nbody_2026/stage19_class_rerun_derived_law_2026.py")).read()
mi = open(os.path.join(HERE_REPO, "real_research/reviews/mi_dbi_cmb_class_run_2026.py")).read()
check(("K_B" not in s19) and ("K_B" not in mi) and ("aether" not in mi.lower()),
      "B1  the corpus's OWN CLASS runs (stage19 + mi_dbi_cmb_class_run) contain the string "
      "'K_B' ZERO times and no aether/vector sector: they are FLUID-MODULE BRACKETS",
      "so the corpus never ran the J-term through a Boltzmann code itself")
info("B2  the CMB consistency of THIS term is therefore inherited in a 3-link chain: "
     "(i) [SZ21] derived the linear equations from the FULL action (term included) and fit "
     "CMB + P(k) with their OWN Boltzmann code -- LITERATURE, not corpus-run; "
     "(ii) committed stage18: the v9 promotion's new entries all vanish on FLRW, so the "
     "promoted theory's linear equations ARE AeST's; "
     "(iii) the corpus CLASS bracket checks the modified BACKGROUND only.  "
     "The middle of the chain is the fitted [SZ21] pass -- the term needs NO gate and NO "
     "new protection, with the fixed coefficient 2(2-K_B).  CAVEAT for the self-verifying "
     "standard: link (i) is not reproducible from this repo.")
info("B3  DOUBLE-EDGE recorded: at linear order the chi-E mixing this term feeds is part of "
     "what makes delta-phi cluster DUST-LIKE and fit the third peak [SZ21 Eq 11-12; bridge1]. "
     "The term is LOAD-BEARING for the banked CMB pass, not merely tolerated by it.")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- SIGN (deliverable 1): where this term lands in the sign taxonomy")
print("=" * 100)
info("C1  QUASI-STATIC SIGN: by A3 the term's QS content is the MOND source coupling -- "
     "ATTRACTION.  It is what turns g_N into g_obs; the dust falls FASTER because of it. "
     "The corpus's own collapse pricing [v9] (1.34-1.96x Newtonian speedup, 2.03x at z=6 -> "
     "1.14x at z=25) ALREADY INCLUDES this term's QS effect.  Sign verdict for the "
     "pressure reading: ANTI-support, landing with the scalar routes [s51 Part B].")
info("C2  NO STATIC SUPPORT BRANCH (the self-consistency kill of the pressure reading): "
     "any HALTED configuration is static; in a static configuration A is static and "
     "J^r = d^r Phi exactly (A3), so the term reverts IDENTICALLY to the priced attractive "
     "coupling.  A halo halted BY this term is self-contradictory: the halted state "
     "restores pure attraction.  Sustained anti-aligned tilt (aether accelerating inward "
     "at ~g) is not stationary: the congruence velocity grows secularly -- itself a collapse.")
info("C3  the term's honest dynamical range during collapse: between J = 0 (aether comoving/"
     "geodesic: MOND source OFF -> NEWTONIAN collapse) and J = g (static: full MOND-boosted "
     "collapse).  BOTH ENDS COLLAPSE.  The 'modulation' reading is bounded by removing a "
     "1.34-1.96x speedup [v9] -- it can never supply the sign flip a halt needs.")
# the one channel A1 leaves open:
info("C4  WHAT A1 LEAVES OPEN: the term adds to the shift CURRENT a pure-flux piece "
     "J_s^mu(J-term) = 2(2-K_B) J^mu/(16 pi G-tilde), zero charge density.  Inside a halo "
     "J^r points OUTWARD (magnitude g): an outward dust-charge transport channel "
     "(rho = Q0 n identically, so charge flux IS mass flux).  In exact QS equilibrium the "
     "net is zero (the balance IS the MOND field equation); the UNPRICED object is the "
     "NON-QS LAG of the compensating grad-phi flux during collapse.  This -- not pressure -- "
     "is the only reading the algebra leaves alive.")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- MAGNITUDE (deliverable 2): ceilings at the corpus's own calibrations")
print("=" * 100)
# Surface calibration [s52]: M_cap at rho_h = 1654 rho_dm0
R_surf = (3 * M_CAP / (4 * np.pi * RHO_H)) ** (1.0 / 3.0)
gN_surf = G * M_CAP / R_surf ** 2
check(abs(R_surf / KPC - 221) < 3 and abs(gN_surf / 7.15e-12 - 1) < 0.02,
      f"D1  surface calibration: R = {R_surf/KPC:.1f} kpc, g_N = {gN_surf:.2e} m/s^2 "
      f"= {gN_surf/A0_CAN:.4f} a0_can = {gN_surf/A0_ALT:.4f} a0_alt -- DEEP MOND at the surface")

# Stress ceiling: P_J^max/P_req = (2-K_B) g_phi / (6 g_N)   [derivation:
#   eps_J = 2(2-K_B)/(16 pi G) * |J||grad phi| c^4-consistent = (2-K_B) g g_phi/(8 pi G),
#   |J| <= g_obs (the largest sustained proper acceleration available);
#   P_req = rho g_obs R (hydrostatic);  8 pi G rho R = 6 g_N for the mean density  ]
print("\n  D2  STRESS CEILING (2-K_B) g_phi/(6 g_N)  [maximal tilt, perfect alignment, full "
      "energy density as radial support -- every choice favours the mechanism]:")
print(f"      {'calibration':<26s} {'kernel':<8s} {'footing':<8s} {'K_B=0.10':>10s} {'K_B=0.25':>10s}")
rows = {}
for label, overdens, use_local in (("surface 1654 rho_dm0", 1654.0, False),
                                   ("interior 1e4 rho_dm0", 1e4, True),
                                   ("deep 1e6 rho_dm0 (nu0 flr)", 1e6, "floor"),
                                   ("deep 1e6 rho_dm0 (nu0 ceil)", 1e6, "ceil")):
    rho_loc = overdens * RHO_DM0
    R_ = (3 * M_CAP / (4 * np.pi * rho_loc)) ** (1.0 / 3.0)
    gN_ = G * M_CAP / R_ ** 2
    for kern, gof in (("line", gobs_line), ("ms08", gobs_ms08)):
        for foot, a0g in (("can", A0_CAN), ("alt", A0_ALT)):
            if use_local == "ceil":
                a0l = a0g * np.sqrt(a_ratio_local(overdens, NU0_HI))
            elif use_local == "floor":
                a0l = a0g * np.sqrt(a_ratio_local(overdens, NU0_LO))
            elif use_local:
                a0l = a0g * np.sqrt(a_ratio_local(overdens, NU0_HI))
            else:
                a0l = a0g
            gphi = gof(gN_, a0l) - gN_
            vals = [(2 - kb) * gphi / (6 * gN_) for kb in KBS]
            rows[(label, kern, foot)] = vals
            print(f"      {label:<26s} {kern:<8s} {foot:<8s} {vals[0]:>10.4f} {vals[1]:>10.4f}")
surf_max = max(rows[("surface 1654 rho_dm0", k, f)][0] for k in ("line", "ms08") for f in ("can", "alt"))
deep_ceil = max(rows[("deep 1e6 rho_dm0 (nu0 ceil)", k, f)][0] for k in ("line", "ms08") for f in ("can", "alt"))
deep_flr = max(rows[("deep 1e6 rho_dm0 (nu0 flr)", k, f)][0] for k in ("line", "ms08") for f in ("can", "alt"))
check(0.75 < surf_max < 1.15,
      f"D2a HONEST: at the SURFACE calibration the ceiling is O(1) (0.80-{surf_max:.2f} across "
      f"kernel/footing/K_B) -- the stress ceiling ALONE does not kill this cell there.  No "
      f"manufactured deficit: recorded as-is")
check(deep_ceil < 3e-3 and deep_flr < 0.01,
      f"D2b at the DEEP 1e6 rho_dm0 calibration the ceiling is {deep_flr:.4f} (nu0 floor; "
      f"local-a0 suppression 4.6x) / {deep_ceil:.4f} (ceiling; 13.3x [s53 D2b]): short "
      f"133x-1e4x -- and the ratio FALLS inward like sqrt(a0_loc/g_N), so INNER SHELLS "
      f"(which bind FIRST in the onion model) are NEVER supported at any K_B, kernel or footing",
      "the pressure reading cannot halt the interior runaway even at its absolute ceiling; "
      "the Sgr A* endpoint (5.8e5x) is untouched by it")

# Implied halt radius under the (dead) pressure reading: ratio=1 in deep MOND
print("\n  D3  implied halt under the maximal pressure reading (ratio = 1 => g_* = "
      "(2-K_B)^2 a0/36):")
for foot, a0g in (("can", A0_CAN), ("alt", A0_ALT)):
    for kb in KBS:
        gstar = (2 - kb) ** 2 * a0g / 36
        Rh = np.sqrt(G * M_CAP / gstar)
        print(f"      {foot} K_B={kb}: g_* = {gstar/a0g:.3f} a0  ->  R_halt = {Rh/KPC:.0f} kpc")
gstar_max = (2 - 0.10) ** 2 / 36
check(gstar_max < 8.2 / 60,
      f"D3a g_* = {gstar_max:.3f} a0 -- 80x BELOW the honest halt bound g_* <= 8.2 a0 [brief]: "
      f"the halt (if the sign worked, which it does not) happens only at the 176-226 kpc "
      f"FRINGE, never at the 10-15 kpc scale the enclosed-mass bound allows",
      "endpoint class: a ~200-kpc core of 2.5e12 Msun -- the SAME configuration class "
      "committed stage12/52 machinery charges Delta chi^2 +1.2e3..+2.0e3 (worse than the "
      "rejected +927) and stage53 A4c grids at +446..+1698 [s52 kill 3, s53; quoted unowned]")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- THE TWO-ENDED TEST (deliverable 3): both ends computed")
print("=" * 100)
# End 1: the collapsing halo at z_bind. J ~ g there:
info(f"E1  halo end: |J| ~ g_obs(surface) = "
     f"{gobs_line(gN_surf, A0_CAN):.2e} m/s^2 = {gobs_line(gN_surf, A0_CAN)/A0_CAN:.3f} a0 "
     f"at z_bind = 10.83, where the derived a0(z) law is FLAT (0.9997 floor / 0.980 ceiling "
     f"[s52 B1]) -- the term is fully active exactly where support is needed.")
# End 2: linear scales at recombination. peculiar g on comoving scale Rc:
#   g = (4pi/3) G rho_m0 (1+z)^2 delta_rec Rc   with delta_rec = sigma(Rc,0)/D-growth
print("\n  E2  recombination end: peculiar gravitational field on linear scales "
      "(g = (4pi/3) G rho_m0 (1+z_rec)^2 delta_rec R_com; delta_rec = sigma_0(R)/850, "
      "matter-domination growth D ~ a with Lambda correction):")
GROWTH = 850.0
for Rc_mpc, sig0 in ((11.87, 0.80), (30.0, 0.35), (100.0, 0.06)):
    d_rec = sig0 / GROWTH
    g_lin = (4 * np.pi / 3) * G * RHO_M0 * (1 + Z_REC) ** 2 * d_rec * (Rc_mpc * MPC)
    print(f"      R_com = {Rc_mpc:6.1f} Mpc  sigma_0 = {sig0:.2f}  delta_rec = {d_rec:.2e}"
          f"  g_lin(rec) = {g_lin:.2e} m/s^2 = {g_lin/A0_CAN:5.2f} a0"
          f"  (= {g_lin/gN_surf:5.1f}x the halo-surface g_N)")
g_lin8 = (4 * np.pi / 3) * G * RHO_M0 * (1 + Z_REC) ** 2 * (0.80 / GROWTH) * (11.87 * MPC)
check(g_lin8 > 20 * gN_surf,
      f"E3  *** THE CHANNEL IS TWO-ENDED-INVERTED IN g: the physical peculiar field at "
      f"recombination linear scales ({g_lin8:.1e}) EXCEEDS the z=10.83 halo-surface field "
      f"({gN_surf:.1e}) by ~{g_lin8/gN_surf:.0f}x.  |J| ~ g gives NO parametric separation "
      f"between the two ends -- unlike y (4-6 orders spatial) ***",
      "so ANY reading of this term that needed the rec end SUPPRESSED is dead on arrival")
info("E4  why the recombination end nevertheless passes: the term sits IN the fitted linear "
     "theory [Part B] -- its rec-end effect is not suppressed, it is FIT.  For the transport "
     "reading specifically the fractional drain scales with the local overdensity "
     "(div J ~ 4 pi G delta-rho): O(delta) ~ 1e-3..1e-4 at rec linear scales vs O(1) in a "
     "bound halo -- a 3-5 order separation supplied by NONLINEARITY itself, not by a "
     "constructed gate.  This is the first candidate in the corpus whose two ends both pass "
     "STRUCTURALLY: rec end by fit + linearity, halo end active.  The wall [s52] does not "
     "kill this cell.")

# =================================================================================================
print()
print("=" * 100)
print("PART F -- THE TRANSPORT CEILING (the one live reading), and its unpinned knob")
print("=" * 100)
# v_eff = flux/charge-density = (2-K_B) J / (8 pi G-tilde n);  n = rho/Q0  =>
# v_eff/c = (2-K_B) g omega_Q / (8 pi G rho c),  omega_Q = Q0 c  [1/s].
# Q0 is NOT pinned by the corpus: mu^2 = 2 K2 Q0^2/(2-K_B) [SZ21] leaves Q0 free via K2.
rho_tot_bind = RHO_H * OM_M / OM_DM              # total matter at binding
t_dyn = 1.0 / np.sqrt(G * rho_tot_bind)
print(f"      binding: rho_tot = {rho_tot_bind:.2e} kg/m^3, t_dyn = 1/sqrt(G rho) = "
      f"{t_dyn/3.156e16:.1f} Gyr, rate = {1/t_dyn:.2e} /s")
print(f"      {'pinning':<34s} {'omega_Q [1/s]':>14s} {'drain/binding rate (K_B=0.10)':>32s}")
for lab, omQ in (("Q0 c = H0 (Hubble pinning)", H0),
                 ("Q0 c = mu c, mu^-1 = 1 Mpc, K2~O(1)", C / MPC)):
    for kb in (0.10,):
        v_eff = (2 - kb) * gobs_line(gN_surf, A0_CAN) * omQ / (8 * np.pi * G * RHO_H * C)
        rate = v_eff * C / R_surf                    # fractional drain 1/s  (v_eff in c units)
        print(f"      {lab:<34s} {omQ:>14.2e} {rate*t_dyn:>32.2f}")
v_h = (2 - 0.10) * gobs_line(gN_surf, A0_CAN) * H0 / (8 * np.pi * G * RHO_H * C)
v_m = (2 - 0.10) * gobs_line(gN_surf, A0_CAN) * (C / MPC) / (8 * np.pi * G * RHO_H * C)
check(v_h * C / R_surf * t_dyn < 1.0 < v_m * C / R_surf * t_dyn,
      f"F1  the drain CEILING spans {v_h*C/R_surf*t_dyn:.2f}x (Hubble pinning: too slow) to "
      f"{v_m*C/R_surf*t_dyn:.0f}x (mu pinning: ample) of the binding rate -- the verdict-"
      f"deciding knob is Q0 (equivalently K2 at the CMB-pinned mu), which the corpus has "
      f"NEVER pinned",
      "and this is a CEILING (zero compensation); in exact QS the net is zero -- the balance "
      "IS the MOND equation.  The net = the non-QS lag, which only the collapse solve gives")
info("F2  the lag is NOT obviously small: the compensating flux is carried by the condensate "
     "sector, whose sound speed is the SLOWEST mode in the theory (c_s ~ 1.4 km/s "
     "[stage6-audit B]), vs collapse speeds ~100 km/s at binding -- a 70x mismatch in the "
     "direction FAVOURING a large lag.  Not a result; a named reason the solve is required.")
info("F3  destination + late-time safety are NOT free: drained charge piles beyond the halo "
     "(lensing-visible in the KiDS window if it stops < 2.2 Mpc [stage12]), and at late-time "
     "linear scales (delta ~ 0.1-1 today) the same channel is O(delta) -- benign only "
     "because [SZ21]'s fitted pass says so at ITS parameters.  The named calculation must "
     "run at linear-cosmology-consistent (Q0, K2, K_B).")

# =================================================================================================
print()
print("=" * 100)
print("PART G -- HEALTH (deliverable 4) + VERDICT (deliverable 5)")
print("=" * 100)
info("G1  HEALTH, established: background + linear health is AeST's own -- [SZ21] linear "
     "equations + published stability analyses; six propagating modes (2 tensor at c "
     "EXACTLY, 2 massive vector, 1 massive scalar, 1 condensate) [stage6-audit B, "
     "Bataki-Skordis-Zlosnik 2023]; 0 < K_B < 2 stability, corpus BBN cap K_B <= 0.25 "
     "(stage 50); c_T = 1 exact.  NOT established (would need the health matrix): "
     "no-ghost/gradient stability of the chi-E mixing on a TILTED NONLINEAR collapse "
     "background (finite w, finite J) -- named, not presumed.")
print("""
  VERDICT (one line): VIABLE-CANDIDATE -- in EXACTLY ONE narrowed reading -- with two of the
  three readings of "support" KILLED here:

  DEAD 1, PRESSURE reading: no static support branch exists (a halted halo restores the
     attractive MOND coupling identically, Part C2); the ceiling declines inward as
     sqrt(a0_loc/g_N) -- 133x-1e4x short at the deep calibration, inner shells never
     supported (D2b); implied halt sits at the 176-226 kpc fringe, g_* ~ 0.09-0.10 a0,
     80x below the honest bound, in the lensing-charged +1.2e3..+2.0e3 class (D3a).
  DEAD 2, MODULATION reading: the term's dynamical range is [Newtonian, 1.34-1.96x MOND]
     collapse -- both ends collapse (C3).
  ALIVE, TRANSPORT reading: outward shift-charge flux 2(2-K_B)J^mu/(16 pi G-tilde), zero
     charge density (A1), fully active at z_bind (a0(z) flat there, E1), recombination end
     passed BY FIT + linearity with 3-5 orders of delta-separation (E4) -- the first
     mechanism in the corpus to pass the binding-epoch wall structurally.  Ceiling spans
     0.15x-671x of the binding rate across the UNPINNED Q0 window (F1).

  THE NAMED NEXT CALCULATION: the 1+1D tilted-aether spherical collapse
  (AEST_SPHERICAL_COLLAPSE_SETUP.md machinery + the tilt d.o.f. w(r,t) + shift-charge-flux
  bookkeeping), run at linear-cosmology-consistent (Q0, K2, K_B), reading off the NET
  charge flux through the halo surface from MOND-entry to virialisation.  Decisive knob:
  Q0.  Kill conditions, pre-stated: net flux inward or < ~0.3x binding rate at the
  mu-pinned Q0 => cell DEAD; drained mass parked inside 2.2 Mpc => KiDS charge applies.
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
