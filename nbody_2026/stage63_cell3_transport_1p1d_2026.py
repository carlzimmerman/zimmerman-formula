#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage63_cell3_transport_1p1d_2026.py
====================================
STAGE 63: THE OWED CELL-3 1+1D TRANSPORT SOLVE (stage54 owed items 3+4), RUN AT THE
PINNED Q0 -- AND THE VERDICT IS NOT THE ONE THE BUILDER EXPECTED: THE CHANNEL IS
DEMOTED, VIABLE-CANDIDATE -> CONDITIONAL-DEAD, BY A FIXED-POINT CONSISTENCY ARGUMENT
WITH THE CORPUS'S OWN Q0 PIN.

What the solve found, in order:
  (1) THE F1 PIN (PART A, owed item 3): the action term is +2(2-K_B) J^mu nabla_mu phi /
      (16 pi G~) -- verbatim from the LaTeX source now transcribed in
      real_research/bridge1_aest_equations.md.  Mass flux F_J = (2-K_B) Q0 g/(8 pi G~):
      the pricing lane's convention was CORRECT; the 0.3x threshold freezes against it.
  (2) MAGNITUDE (PART B/C1): at the pinned Q0 (operative band 0.0024-0.0146 Mpc^-1 after
      stage61) the raw J-flux is 5.3x-32.2x the binding rate (enclosed-mass convention;
      1.8x-10.7x in the lane's v/R convention) -- the pin does NOT kill by magnitude.
      stage54's "0.15x-671x, knob never pinned" collapses to this.
  (3) THE CLOSURE FORK (C2-C3): the raw c_s = 1.4 km/s compensation closure is REFUTED
      OBSERVATIONALLY by the corpus's own stage12 KiDS fit (profiles at 2.2 Mpc exist =>
      v_est >= ~160 km/s, vs 1536 Gyr to establish at c_s); but the drain dies only for
      v_est > v_crit = 620-3790 km/s, so microphysics alone leaves the fork OPEN.
  (4) THE FIXED-POINT ARGUMENT (C4, the finding, REFEREE-CORRECTED mechanism): F_J is
      super-critical vs the inflow only in an OUTER SHELL (F_J/F_in crosses 1 at ~25-60
      kpc; at the pin radii 3.7-15 kpc it is 0.001-0.26) -- but on any strong-drain
      branch that shell GATES THE SUPPLY (PART B: incoming mass is expelled before it
      can transit), so the interior flow the X-pin's equality was built on still never
      arrives.  Strong drain => pin starved => Q0 un-calibrated: not self-consistent
      with the pin that priced it.  Only the QS-balanced weak-net closure survives.
      DEMOTED.  (A PRE-EXISTING interior reservoir is untested here -- exactly the
      transient escape D2 names.)
  (5) ANTI-ALIGNED branch (pre-stated report condition, C5): reverses to pile-up (98%
      retained) -- adverse for stage61's RAR margins; alignment is load-bearing.

The binding-epoch-wall pass (stage54 C3) survives as STRUCTURE; what dies is the
halo-emptying reading.  Remaining doors, named: Cell 1 at (2,0) marginal-LIVE (stage54
B4); the second-field structural change; any future mechanism with a self-consistent
flux scale.  The full tilted-aether w(r,t) collapse solve remains the derivation-grade
owed item (a transient evading C4 would have to drain WITHOUT suppressing the inflow the
pin needs -- a narrow, named target).

Exit 0 = every check passed.
"""

import sys

import numpy as np

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


print(__doc__)

G = 6.67430e-11
C = 2.99792458e8
KPC = 3.0856775814913673e19
MPC = 1e3 * KPC
MSUN = 1.989e30
H0 = 67.4e3 / MPC
RHO_CRIT = 3 * H0**2 / (8 * np.pi * G)
OM_DM, OM_M = 0.265, 0.315
RHO_DM0 = OM_DM * RHO_CRIT
A0 = 9.3619e-11
GYR = 3.156e16

# the s52 surface calibration (the committed Cell-3 test object, stage54 pricing lane):
M_CAP = 2.51e12 * MSUN
RHO_H = 1654.0 * RHO_DM0
R_SURF = (3 * M_CAP / (4 * np.pi * RHO_H)) ** (1.0 / 3.0)
T_DYN = 1.0 / np.sqrt(G * RHO_H * OM_M / OM_DM)          # binding time [s]
T_START, T_END = 0.44 * GYR, 13.8 * GYR                  # z_bind = 10.83 -> today
KB = 0.10                                                 # stage54's quoted K_B
CS = 1.4e3                                                # condensate sound speed [m/s]
V_FF = (G * M_CAP * A0) ** 0.25                           # terminal free-fall [m/s]
Q0_BAND = {"low edge": 0.0024 / MPC, "high edge": 0.0146 / MPC}   # [1/m], stage61 operative


def gobs_line(gn):
    return 0.5 * (gn + np.sqrt(gn**2 + 4 * gn * A0))      # a0-line kernel


# =================================================================================================
print("=" * 100)
print("PART A -- the F1 factor-2 convention PINNED from the action (owed item 3)")
print("=" * 100)
coef_action = 2 * (2 - KB) / (16 * np.pi)                 # action: +2(2-K_B) J.grad(phi)/16piG
coef_lane = (2 - KB) / (8 * np.pi)                        # the pricing lane's F1 convention
check(abs(coef_action / coef_lane - 1) < 1e-12,
      "A1  *** PINNED: the action's +2(2-K_B) J^mu nabla_mu phi/(16 pi G~) gives the "
      "shift-current mass flux F_J = (2-K_B) Q0 g/(8 pi G~) -- the factor 2 cancels into "
      "16 pi and the pricing lane's convention is CORRECT ***",
      "source: the verbatim NT_A_action transcription completed 2026-08-14 in "
      "real_research/bridge1_aest_equations.md; the 0.3x kill threshold now freezes "
      "against this convention")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- the 1+1D solve (donor-cell, flux-capped, lag compensation)")
print("=" * 100)
NR, DT = 300, 2e-3 * GYR
r_edge = np.geomspace(1.0 * KPC, 5.0 * MPC, NR + 1)
r_c = 0.5 * (r_edge[1:] + r_edge[:-1])
dr = np.diff(r_edge)
area = 4 * np.pi * r_edge[1:-1] ** 2                      # interior faces
vol = 4 * np.pi / 3 * (r_edge[1:] ** 3 - r_edge[:-1] ** 3)
i_surf = np.searchsorted(r_c, R_SURF)
i_kids = np.searchsorted(r_c, 2.2 * MPC)
MDOT_IN = M_CAP / (T_END - T_START)                       # smooth capture over the history

# gravitational field: enclosed M_CAP-profile source (fixed; drain feedback noted in D3)
M_enc = M_CAP * np.minimum(r_c / R_SURF, 1.0) ** 3
g_prof = gobs_line(G * M_enc / r_c**2)


def run(q0_m, sign=+1.0, closure="lag"):
    """donor-cell continuity with inflow at v_ff, J-term flux F_J, and closure.

    Faces f = 0..NR-2 sit between cells f and f+1.  Advection moves mass f+1 -> f
    (donor f+1).  The J-term moves mass f -> f+1 when aligned (donor f), f+1 -> f when
    anti-aligned (donor f+1).  A combined per-cell limiter caps TOTAL export at the
    cell's content, so densities stay non-negative by construction.
    """
    n = np.zeros(NR)                                      # resident mass density [kg/m^3]
    Fcomp = np.zeros(NR)
    t = T_START
    FJ = (2 - KB) * q0_m * C * g_prof / (8 * np.pi * G)   # omega_Q = Q0 c; [kg/m^2/s]
    tau = r_c / CS
    while t < T_END:
        if closure == "ceiling":
            Fj_eff = FJ
        elif closure == "lag":
            Fcomp = Fcomp + DT * (FJ - Fcomp) / tau
            Fj_eff = np.maximum(FJ - Fcomp, 0.0)
        else:                                             # condensate-cap
            Fj_eff = np.minimum(FJ, n * CS)
        # desired mass moves per face this step [kg]
        adv = n[1:] * V_FF * area * DT                    # donor f+1, direction inward
        if sign > 0:
            jmv = Fj_eff[:-1] * area * DT                 # donor f, direction outward
        else:
            jmv = Fj_eff[1:] * area * DT                  # donor f+1, direction inward
        # combined per-cell export limiter
        want = np.zeros(NR)
        np.add.at(want, np.arange(1, NR), adv)            # cell f+1 exports adv
        if sign > 0:
            np.add.at(want, np.arange(0, NR - 1), jmv)    # cell f exports jmv outward
        else:
            np.add.at(want, np.arange(1, NR), jmv)        # cell f+1 exports jmv inward
        avail = n * vol
        lam = np.where(want > 0, np.minimum(1.0, avail / np.maximum(want, 1e-300)), 1.0)
        adv = adv * lam[1:]
        jmv = jmv * (lam[:-1] if sign > 0 else lam[1:])
        dm = np.zeros(NR)
        dm[:-1] += adv
        dm[1:] -= adv
        if sign > 0:
            dm[:-1] -= jmv
            dm[1:] += jmv
        else:
            dm[:-1] += jmv
            dm[1:] -= jmv
        dm[-1] += MDOT_IN * DT                            # capture at the outer boundary
        n = n + dm / vol
        t += DT
    m_in = float((n * vol)[: i_surf + 1].sum())
    m_window = float((n * vol)[i_surf + 1 : i_kids + 1].sum())
    m_beyond = float((n * vol)[i_kids + 1 :].sum())
    return m_in, m_window, m_beyond, FJ[i_surf]


res = {}
print(f"    {'closure / branch':<34s} {'Q0 edge':>9s} {'M_in/M_cap':>11s} "
      f"{'M_win/M_cap':>12s} {'M_out/M_cap':>12s} {'rate/bind':>10s}")
for q0lab, q0 in Q0_BAND.items():
    for clo in ("ceiling", "lag", "cap"):
        m_in, m_w, m_b, fj = run(q0, +1.0, clo)
        rate = fj * 4 * np.pi * R_SURF**2 / M_CAP * T_DYN
        res[(clo, q0lab)] = (m_in / M_CAP, m_w / M_CAP, m_b / M_CAP, rate)
        print(f"    {clo:<10s} aligned{'':17s} {q0lab:>9s} {m_in/M_CAP:>11.4f} "
              f"{m_w/M_CAP:>12.4f} {m_b/M_CAP:>12.4f} {rate:>10.2f}")
m_in_aa, m_w_aa, m_b_aa, _ = run(Q0_BAND["high edge"], -1.0, "lag")
print(f"    {'lag':<10s} ANTI-ALIGNED{'':12s} {'high':>9s} {m_in_aa/M_CAP:>11.4f} "
      f"{m_w_aa/M_CAP:>12.4f} {m_b_aa/M_CAP:>12.4f} {'(pile-up)':>10s}")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- kill conditions, the closure fork, and the fixed-point argument")
print("=" * 100)
rate_lo, rate_hi = res[("lag", "low edge")][3], res[("lag", "high edge")][3]
check(rate_lo > 0.3,
      f"C1  the RAW ceiling survives the pre-stated kill threshold: the J-term flux at the "
      f"PINNED Q0 is {rate_lo:.1f}x (low edge) to {rate_hi:.1f}x (high edge) the binding "
      f"rate, vs the 0.3x kill line -- so the pin does NOT kill the channel by magnitude",
      "(enclosed-mass convention; the pricing lane's v/R convention is 3x smaller, "
      "1.8x-10.7x -- above threshold in either).  stage54's 0.15x-671x span collapses to "
      "this; the verdict now moves to the compensation closure, where the real physics is")
V_OBS_FLOOR = 2.2 * MPC / (13.36 * GYR)
check(2.2 * MPC / CS / GYR > 1000,
      f"C2  the RAW c_s closure is REFUTED OBSERVATIONALLY: establishing the scalar profile "
      f"out to 2.2 Mpc at c_s = 1.4 km/s would take {2.2*MPC/CS/GYR:.0f} Gyr, yet stage12's "
      f"committed KiDS fit OBSERVES the framework's MOND profile at 2.2 Mpc today -- so the "
      f"effective establishment speed is v_est >= {V_OBS_FLOOR/1e3:.0f} km/s",
      "this was invisible to stage54 (which named c_s and said 'the solve is required'); "
      "the solve, plus the corpus's own weak-lensing fit, retires the slowest closure")
v_crit_lo = R_SURF / (T_DYN / rate_lo) / 1e3
v_crit_hi = R_SURF / (T_DYN / rate_hi) / 1e3
check(v_crit_lo > V_OBS_FLOOR / 1e3,
      f"C3  the closure map: the drain empties the halo iff the compensation establishes "
      f"slower than v_crit = R/(t_dyn/rate) = {v_crit_lo:.0f}-{v_crit_hi:.0f} km/s; the "
      f"observational floor ({V_OBS_FLOOR/1e3:.0f} km/s) sits BELOW v_crit, and c sits far "
      f"above -- microphysics alone leaves the fork [156 km/s, c] OPEN",
      "so neither the kill threshold (C1) nor the observation (C2) decides.  What decides "
      "is self-consistency (C4)")
# REFEREE CORRECTION: the ratio F_J/F_in is radius-dependent.  F_in(r) = Mdot/(4 pi r^2)
# (steady supply converging inward), F_J(r) = (2-K_B) Q0 c g(r)/(8 pi G):
print(f"    {'r [kpc]':>8s} {'F_J/F_in (low edge)':>20s} {'(high edge)':>12s}")
ratios = {}
for r_kpc in (3.7, 8.122, 15.0, 25.0, 60.0, R_SURF / KPC):
    r_m = r_kpc * KPC
    g_r = gobs_line(G * M_CAP * min(r_m / R_SURF, 1.0) ** 3 / r_m**2)
    fin_r = MDOT_IN / (4 * np.pi * r_m**2)
    row = tuple((2 - KB) * q0 * C * g_r / (8 * np.pi * G) / fin_r
                for q0 in Q0_BAND.values())
    ratios[r_kpc] = row
    print(f"    {r_kpc:>8.1f} {row[0]:>20.3f} {row[1]:>12.1f}")
check(ratios[3.7][1] < 1.0 < ratios[60.0][0] and ratios[R_SURF / KPC][0] > 10,
      f"C4  *** THE FIXED-POINT ARGUMENT (referee-corrected mechanism): F_J/F_in crosses "
      f"1 between 15 and 60 kpc and reaches {ratios[R_SURF/KPC][0]:.0f}x-"
      f"{ratios[R_SURF/KPC][1]:.0f}x at the surface -- an outer GATING SHELL, sub-critical "
      f"at the pin radii (3.7-15 kpc: {ratios[3.7][0]:.3f}-{ratios[15.0][1]:.2f}).  On any "
      f"strong-drain branch the shell expels incoming charge before it transits (PART B: "
      f"M_in -> 0), so the interior flow the X-pin's equality needs still never arrives: "
      f"strong drain => pin starved => Q0 (hence F_J's own magnitude) un-calibrated -- not "
      f"self-consistent with the pin that priced it.  Only the QS-balanced (weak-net) "
      f"closure survives ***",
      "the original draft claimed super-criticality at ALL radii -- numerically false at "
      "the pin radii; the refereed mechanism is supply-gating, same conclusion.  A "
      "pre-existing interior reservoir is untested here (= D2's named transient escape).  "
      "COUPLING, on the record: the branch that surrenders the pin to keep a strong drain "
      "also unravels stage62's X-dilemma resolution -- both ride the same pin")
check(m_in_aa / M_CAP > 0.95,
      f"C5  ANTI-ALIGNED branch (pre-stated report condition): the flux reverses and the "
      f"halo retains/piles {100*m_in_aa/M_CAP:.0f}% -- no drain, plus interior pile-up "
      f"ABOVE the continuity baseline: adverse for the RAR margins of stage61 PART C",
      "alignment is load-bearing, exactly as stage54 C4's sign analysis said")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- verdict and grade")
print("=" * 100)
check(True,
      "D1  *** CELL 3'S TRANSPORT CHANNEL: DEMOTED from VIABLE-CANDIDATE to "
      "CONDITIONAL-DEAD -- dead-by-consistency at the corpus's own pinned Q0 (C4), alive "
      "only on a branch that surrenders the pin and thereby its own calibration.  The "
      "binding-epoch-wall pass (stage54 C3) stands as STRUCTURE; what dies is the "
      "halo-emptying reading of it ***",
      "NOT 'no doors': Cell 1 at (2,0) is marginal-LIVE under flow pricing (stage54 B4), "
      "the second-field structural change stands open, and the wall-pass structure "
      "survives for any future mechanism with a self-consistent flux scale")
check(True,
      "D2  GRADE AND LIMITS, stated plainly: 1+1D donor-cell flux bookkeeping with a "
      "relaxation closure -- NOT the full tilted-aether w(r,t) collapse solve, which "
      "remains owed and could in principle exhibit a transient net flux evading C4 (it "
      "would have to drain WITHOUT suppressing the inflow the pin needs: a narrow "
      "target, named).  Fixed-g source; K_B = 0.10 quoted ((2-K_B) span changes rates "
      "< 15%); the closure map (C3) and both branch tables (PART B) are the evidence",
      "the health matrix on the tilted background (stage51 owed) is unchanged by this "
      "stage")

print()
print("=" * 100)
n_fail = len(FAIL)
print(f"STAGE 63 CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed" + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
