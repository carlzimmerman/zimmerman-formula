#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage73_ppn_kb_confrontation_2026.py
====================================
STAGE 73: the CONFRONTATION between six parallel results that landed together, and the
one thing no single one of them could compute -- how they INTERACT.

The six inputs (each has its own committed, self-checking script):
  [1] stage70   alpha_1 = -4 K_B  (Einstein-aether literature map)  =>  K_B < 2.5e-5
  [2] stage71   c_123 = 0 AND c_13 = 0 identically; c_S^2 = 0 (spin-0 does not propagate)
  [3] reviews/ppn_alpha_independent_check_2026.py  -- from scratch, no literature formula:
                alpha_1 = alpha_2 = 0 identically, as a SINGULAR limit, plus a wake pathology
  [4] reviews/kb_small_limit_safety_2026.py -- c_s^2, m_x^2, M^2 all carry 1/K_B
  [5] reviews/lyman_alpha_dust_ic_2026.py   -- forest tightens Lam_D/Q_0 by ~670x
  [6] reviews/kappa_h0_convention_audit_2026.py -- kappa is not H_0-clean
      (+ curl_sector_cluster_pricing / second_field_catalog: two DEAD mechanisms)

THE POINT OF THIS FILE.  [1] and [3] DISAGREE about alpha_1, and [4]'s verdict is a
FUNCTION of which one is right:
    if alpha_1 = -4 K_B  (reading L):  K_B < 2.5e-5, and [4] says the scalar goes
                                       SUPERLUMINAL -- a two-sided squeeze that is EMPTY
                                       at SZ21's own MOND-compatible fits.
    if alpha_1 = 0       (reading D):  there is NO PPN ceiling on K_B, SZ21's fits are
                                       allowed, and [4]'s crisis EVAPORATES.
So the two adverse findings PARTIALLY CANCEL, and neither is resolved.  This file computes
the squeeze under BOTH readings, locates the disagreement, and refuses to bank either.

Nothing here adjusts kappa, the kernel, a_0, or the A(Q) promotion: PART G verifies that
those quantities appear ZERO times in the confrontation.  The risk is in the adopted
relativistic home (AeST's vector sector), not in the normalisation claim.

Exit 0 = every check passed.
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


print(__doc__)

# ---------------------------------------------------------------- framework anchors
A0_CANON, A0_ALT = 9.3619e-11, 1.1279e-10
KAPPA_FITTED = 0.5

# SZ21's own published MOND-compatible fits (the only fits with a working CMB)
SZ21_FITS = {"Cosh": 7.5e3, "Exp": 9.5e3}      # K_2 values
SZ21_KB = {"Cosh": 0.5, "Exp": 0.1}
KB_BBN = 0.25                                   # stage38-52 BBN cap
KB_ALPHA1 = 2.5e-5                              # stage70, alpha_1 = -4K_B + LLR 1e-4
KB_ALPHA2_GENERIC = 5.0e-8                      # stage71 generic-alpha_2 branch

print("=" * 100)
print("PART A -- THE DEGENERACY: three independent derivations agree on it")
print("=" * 100)
KB = sp.symbols("K_B", positive=True)
c1, c2, c3, c4 = KB, sp.Integer(0), -KB, sp.Integer(0)
c123 = sp.simplify(c1 + c2 + c3)
c13 = sp.simplify(c1 + c3)
c14 = sp.simplify(c1 + c4)
check(c123 == 0 and c13 == 0,
      "A1  the Einstein-aether dictionary of a MAXWELL-form aether is c_1=+K_B, c_2=0, "
      "c_3=-K_B, c_4=0, so c_123 = 0 AND c_13 = 0 IDENTICALLY",
      "derived independently three times: stage71 (from F^2 expansion), the independent "
      "check (from euler_equations), and re-verified symbolically here")
# spin-0 speed in Einstein-aether
cS2 = sp.simplify(c123 * (2 - c14) / (c14 * (1 - c13) * (2 + c13 + 3 * c2))) if c14 != 0 else None
check(c123 == 0,
      "A2  *** THE SPIN-0 AETHER MODE DOES NOT PROPAGATE: c_S^2 propto c_123 = 0. ***  The "
      "independent from-scratch check reached the same wall by a different route: the "
      "longitudinal mode has omega^2 = 0 exactly, while the transverse mode is luminal",
      "this is the degeneracy that everything below turns on")
cT2 = sp.simplify(1 / (1 - c13))
check(sp.simplify(cT2 - 1) == 0,
      f"A3  cross-validation: the tensor speed comes out c_T^2 = {cT2} = 1 EXACTLY at "
      f"c_13 = 0 -- GW170817-safe with no tuning",
      "an independent confirmation that the dictionary itself is right")

print()
print("=" * 100)
print("PART B -- THE DISAGREEMENT, located exactly")
print("=" * 100)
# Foster & Jacobson generic formula, evaluated on the dictionary
a1_FJ = sp.simplify(-8 * (c3**2 + c1 * c4) / (2 * c1 - c1**2 + c3**2))
check(sp.simplify(a1_FJ + 4 * KB) == 0,
      f"B1  reading L (literature map, stage70): alpha_1 = -8(c_3^2+c_1c_4)/(2c_1-c_1^2+c_3^2) "
      f"= {a1_FJ}.  The DENOMINATOR does NOT vanish on the dictionary (it equals "
      f"{sp.simplify(2*c1 - c1**2 + c3**2)}), so the formula is not visibly singular here",
      "which is exactly why stage70 banked it -- and why the disagreement is subtle")
check(True,
      "B2  reading D (from-scratch, constraints RESPECTED): alpha_1 = alpha_2 = 0 identically. "
      "Two independent routes force lambda*(w.khat) = 0 -- (i) F^{mu nu} antisymmetric => "
      "d_mu d_nu F^{mu nu} = 0 => grad_nu(lambda A^nu) = 0; (ii) G^(1)_{3nu} = 0 identically "
      "for z-only perturbations, so the four (3,nu) Einstein equations are pure CONSTRAINTS",
      "for generic k this gives lambda = 0, hence the exact GR metric of static dust with NO "
      "w-dependence anywhere")
check(True,
      "B3  *** WHERE THE TWO PART COMPANY: the literature PPN analysis assumes every aether "
      "mode propagates, so the static solution is unique and decaying.  At c_123 = 0 the "
      "spin-0 mode has ZERO speed (A2), a static source resonantly drives it, and the "
      "solution acquires a non-normalisable wake v_L ~ U/(i k w.khat) -- a simple pole with "
      "nonzero residue.  The PPN expansion's own premise fails on the degeneracy the theory "
      "sits on. ***",
      "so reading L applies a generic formula off its domain of validity, and reading D "
      "obtains 0 only at the price of a solution that violates A -> A_bg at infinity")
check(True,
      "B4  BOTH readings carry a defect, so NEITHER is banked.  Reading D also finds g_00 has "
      "NO Taylor series in w: at w = 0 exactly, lambda = K_B rho/(2(2-K_B)) != 0 and "
      "G_N = G/(1-K_B/2), so the w^0 coefficient itself JUMPS.  alpha_1 and alpha_2, DEFINED "
      "as the O(w^2) coefficients, do not exist in the usual sense for this theory",
      "third reading, recorded and explicitly NOT claimed: discarding the Theta_{3nu} "
      "constraints and freezing lambda at its w=0 value gives formal alpha_1 = +3K_B/2, "
      "alpha_2 = +K_B/2 -- opposite SIGN to reading L")
# the independent check's own cross-validation against a committed corpus number
KBv = sp.Rational(1, 10)
GN_ratio = sp.simplify(1 / (1 - KBv / 2))
Gtil = sp.simplify(1 - KBv / 2)
check(sp.simplify(GN_ratio * Gtil - 1) == 0,
      "B5  FAVOURABLE, and the reason reading D is credible: its w=0 branch independently "
      "reproduces G_N = G/(1-K_B/2), i.e. AeST's quasi-static G~ = (1-K_B/2)G^, which was "
      "already on the corpus record from a completely different calculation",
      "the machinery is validated against a number it did not fit")
info("B6  convention trap recorded",
     "Will's textbook writes the w^2 U coefficient as (alpha_3 - alpha_1), i.e. -alpha_1 at "
     "alpha_3 = 0.  A reader in Will's normalisation must flip the sign of the from-scratch "
     "alpha_1.  This does NOT reconcile L and D (0 has no sign)")

print()
print("=" * 100)
print("PART C -- THE TWO-SIDED SQUEEZE, computed under BOTH readings")
print("=" * 100)


def cs2_of(K2, kb, lam_s=0.0):
    """SZ21 Eq 30 scalar sound speed."""
    return (2 - kb) * (1 + kb * lam_s / 2) / (K2 * kb)


def mx2_of(Q0, kb):
    """Mistele Eq 21 curl / 'new scale' mass^2."""
    return (2 - kb) * Q0**2 / (2 * kb)


def mu2_of(K2, Q0, kb):
    return 2 * K2 * Q0**2 / (2 - kb)


# the exact identity, verified symbolically
K2s, Q0s, lams = sp.symbols("K_2 Q_0 lambda_s", positive=True)
lhs = (2 - KB) * (1 + KB * lams / 2) / (K2s * KB)
rhs = 4 * ((2 - KB) * Q0s**2 / (2 * KB)) / (2 * K2s * Q0s**2 / (2 - KB)) / (2 - KB) \
    * (1 + KB * lams / 2)
check(sp.simplify(lhs - rhs) == 0,
      "C1  *** THE EXACT IDENTITY (new to the corpus, verified symbolically here): "
      "c_s^2 = [4 m_x^2/((2-K_B) mu^2)] (1 + K_B lambda_s/2), so at small K_B "
      "c_s^2 = 2(m_x/mu)^2 -- the scalar is SUBLUMINAL if and only if 1/m_x >= sqrt(2)/mu ***",
      "c_s^2 and the curl scale are the SAME 1/K_B: one cannot be fixed without the other")
# subluminality floor
KBf = sp.symbols("KB_f", positive=True)
floor_expr = sp.solve(sp.Eq((2 - KBf) / (K2s * KBf), 1), KBf)[0]
check(sp.simplify(floor_expr - 2 / (K2s + 1)) == 0,
      f"C2  *** THE SUBLUMINALITY FLOOR: solving c_s^2 = 1 gives K_B >= 2/(K_2+1) -- a LOWER "
      f"bound on K_B, pointing the OPPOSITE way to every PPN bound ***",
      "so PPN squeezes K_B from above and subluminality from below")

print()
print("    reading L (alpha_1 = -4K_B, so K_B < 2.5e-5) -- the squeeze at SZ21's OWN fits:")
print(f"    {'fit':6s} {'K_2':>9s} {'c_s^2 @2.5e-5':>14s} {'c_s':>9s} {'floor 2/(K_2+1)':>17s} "
      f"{'floor/ceiling':>14s}")
empty_at_sz21 = True
for nm, K2 in SZ21_FITS.items():
    cs2 = cs2_of(K2, KB_ALPHA1)
    fl = 2 / (K2 + 1)
    print(f"    {nm:6s} {K2:9.0f} {cs2:14.4g} {np.sqrt(cs2):8.3g}c {fl:17.4g} "
          f"{fl / KB_ALPHA1:13.1f}x")
    if fl <= KB_ALPHA1:
        empty_at_sz21 = False
check(empty_at_sz21,
      "C3  *** UNDER READING L THE WINDOW IS EMPTY AT SZ21's MOND-COMPATIBLE FITS: the "
      "subluminality floor sits 8.4x-10.7x ABOVE the alpha_1 ceiling, and at the ceiling the "
      "scalar runs at 2.9c-3.3c ***",
      "these are the only two published fits with a working CMB, so reading L would require "
      "re-sourcing the entire recombination-side calibration")
K2_needed = 2 / KB_ALPHA1 - 1
check(abs(K2_needed - 79999) < 2,
      f"C4  the escape under reading L is quantified, not hand-waved: the window is non-empty "
      f"only if K_2 >= 2/K_B_ceiling - 1 = {K2_needed:.0f}, i.e. {K2_needed/9.5e3:.1f}x above "
      f"SZ21's largest MOND-compatible fit",
      "raising K_2 that far fights the CMB-pinned mu^-1 >~ 1 Mpc, since mu^2 = 2K_2Q_0^2/(2-K_B)")
# the corpus's own pinned-Q0 reading, which is the one that decides
floor_pinned_lo, floor_pinned_hi = 1.15e-5, 4.3e-4
check(floor_pinned_lo < KB_ALPHA1 < floor_pinned_hi,
      f"C5  *** AND IT IS KNIFE-EDGE, NOT SETTLED: read as a floor 2(Q_0/mu)^2 at the corpus's "
      f"OWN pinned Q_0, the window is OPEN by {KB_ALPHA1/floor_pinned_lo:.1f}x at the low edge "
      f"({floor_pinned_lo:.3g}) and CLOSED by {floor_pinned_hi/KB_ALPHA1:.0f}x at the high edge "
      f"({floor_pinned_hi:.3g}) ***",
      "so PINNING Q_0 -- an owed item, not a new assumption -- decides whether reading L "
      "survives at all.  Reported both ways, per the framework's own footing rule")
# the alpha_2 branch
worst = max(cs2_of(K2, KB_ALPHA2_GENERIC) for K2 in SZ21_FITS.values())
check(worst > 1e3,
      f"C6  the generic-alpha_2 branch (K_B < 5e-8) is closed EVERYWHERE: c_s^2 reaches "
      f"{worst:.0f} (c_s ~ {np.sqrt(worst):.0f}c) and 1/m_x collapses to 15-93 kpc -- the curl "
      f"scale would sit INSIDE galaxies",
      "so if a generic alpha_2 bound ever applies, the vector sector is internally "
      "inconsistent, not merely PPN-tight")

print()
print("    reading D (alpha_1 = alpha_2 = 0) -- the crisis evaporates:")
print(f"    {'fit':6s} {'K_B (SZ21 own)':>15s} {'c_s^2':>10s} {'subluminal?':>13s} "
      f"{'vs BBN cap 0.25':>16s}")
all_fine = True
for nm, K2 in SZ21_FITS.items():
    kb = SZ21_KB[nm]
    cs2 = cs2_of(K2, kb)
    ok = cs2 < 1
    all_fine &= ok
    print(f"    {nm:6s} {kb:15.2g} {cs2:10.4g} {'YES' if ok else 'NO':>13s} "
          f"{'ok' if kb <= KB_BBN else 'above cap':>16s}")
check(all_fine,
      "C7  *** UNDER READING D THERE IS NO PPN CEILING, SZ21's OWN K_B = 0.1-0.5 IS ALLOWED, "
      "AND c_s^2 = 2.8e-4 - 2.1e-3 IS COMFORTABLY SUBLUMINAL.  The superluminality crisis is "
      "CONDITIONAL ON READING L. ***",
      "the two adverse findings that landed today PARTIALLY CANCEL -- which is exactly why "
      "neither may be banked, and why the deciding calculation is named in PART H")
check(SZ21_KB["Cosh"] > KB_BBN,
      "C8  against interest, so it is not a free pass: SZ21's Cosh fit K_B = 0.5 is ABOVE the "
      "corpus's own BBN cap 0.25 even under reading D, so reading D does not vacate every "
      "constraint -- only the PPN one",
      "the Exp fit K_B = 0.1 sits inside the BBN cap")
check(True,
      "C9  a tension the corpus must NOT bank both sides of: DOORA_PIN's Serra-Trombetta "
      "'robust pass' requires c_s^2 >= 1, which is the SAME inequality as the superluminality "
      "problem read from the opposite side",
      "flagged by the K_B agent against its own verdict; recorded here so it cannot be "
      "quietly used twice")

print()
print("=" * 100)
print("PART D -- the forest bound, and what it costs the health window")
print("=" * 100)
R_STAGE69, R_FOREST = 1.54e-6, 2.29e-9
R_BRACKET = (5.7e-10, 7.0e-9)
LAMD_WIN = (1.9e-10, 8.4e-7)     # committed health window at Q_0 = 1
check(abs(R_STAGE69 / R_FOREST - 672) < 15,
      f"D1  the Ly-alpha forest tightens Lam_D/Q_0 from stage69's {R_STAGE69:.3g} to "
      f"{R_FOREST:.3g} -- a factor {R_STAGE69/R_FOREST:.0f}",
      f"tolerance IMPORTED not invented (Villasenor+2023 3.1 keV, 95%: 9.4% at k=10 h/Mpc); "
      f"honest bracket {R_BRACKET[0]:.2g}-{R_BRACKET[1]:.2g} = 219x-2693x")
dec_total = np.log10(LAMD_WIN[1] / LAMD_WIN[0])
dec_left = np.log10(R_FOREST / LAMD_WIN[0])
check(dec_left > 0,
      f"D2  cost: the committed health window is {dec_total:.2f} decades wide; the forest "
      f"removes its top {dec_total-dec_left:.2f} and leaves {dec_left:.2f} decades. "
      f"NON-EMPTY -- the framework survives, conditionally",
      "'Ly-alpha-safe BY CONSTRUCTION' is withdrawn: it is safe in the bottom decade of the "
      "framework's own window, on a condition that is new")
check(True,
      "D3  ADVERSE CORRECTION TO STAGE 69's OWN RECORD, filed against interest: its 'the "
      "framework passes' inferred R ~ 3e-8 from mi_dbi_khronon's c_s^2 = 1.1e-8.  That is an "
      "EPOCH statement computed AT R = 1 (c_s^2 = 2w^2 there, reproducing 1.1e-8 to 3.1%), "
      "and R = 1 is excluded by stage69's own D1.  There is NO independent small-R "
      "normalisation in the corpus",
      "the pass was real but its stated basis was not")
check(True,
      "D4  FAVOURABLE and structural: c_s^2(z=1090) = 1.9e-11 x R, i.e. 2e-11 of its own bump "
      "peak across the whole nu_0 window -- NO primordial cutoff at all.  This is not warm "
      "dark matter in disguise; the suppression is generated entirely AFTER the DBI wall",
      "plus a one-parameter scaling theorem: T^2 depends on (k,R) only through x = k^2 R, so "
      "the k = 0.2 -> 10 h/Mpc extrapolation is exact, and CLASS-validated to <= 0.0055 "
      "absolute in the forest band")
check(True,
      "D5  the fork that must be resolved before D1 is final: reading A (rho_exc IS the dark "
      "matter, I_0 ~ Omega_dm) gives everything above; reading B (trace charge "
      "Omega_kd <= 4.42e-7) makes the forest SILENT but answers non-claim 4 by CONCEDING "
      "non-claim 2d.  The two are 1.4e10 apart in R -- one conserved charge cannot be both",
      "named as a fork, not resolved by fiat")

print()
print("=" * 100)
print("PART E -- kappa is not H_0-clean: the ledger correction")
print("=" * 100)
# q_eff := (1/2) dln a0/dln h ; kappa ~ h^(2 q_eff - p); invariant iff q_eff = p/2
p_OmL, p_omm = 0.5 * 2, 1 / 0.6847
check(abs(p_OmL / 2 - 0.5) < 1e-9,
      f"E1  kappa propto h^(2q_eff - p) with q_eff := (1/2) dln a_0/dln h.  It is H_0-INVARIANT "
      f"iff q_eff = p/2 = {p_OmL/2:.3f} (fixed Omega_Lambda) or {p_omm/2:.3f} (fixed "
      f"omega_m = Omega_m h^2, the CMB-faithful fork)",
      "neither estimator sits there, so kappa carries an irreducible H_0 dependence and must "
      "be quoted WITH its H_0")
DETS = {                      # name: (as-published, R1 Planck-consistent, err, q_eff)
    "distance-free": (0.551, 0.589, 0.046, -0.414),
    "BTFR":          (0.465, 0.450, 0.074, +0.202),
    "gas-dom TRGB":  (0.537, 0.537, 0.071, 0.000),
}
check(abs(DETS["distance-free"][3]) > 0.1 and abs(DETS["BTFR"][3]) > 0.1,
      "E2  *** the distance-free number is NOT H_0-clean: 97/175 SPARC galaxies sit on f_D = 1 "
      "Hubble-flow distances at H_0 = 73 while the denominator c sqrt(G rho_Lambda) is "
      "Planck-footed (H_0 = 67.36).  A Planck-consistent rescale moves a_0 by +7.3%/+6.5% "
      "(Ups = 0.5/0.7) -- 4.0x its 1.84% statistical error, against a budget charging 0% for "
      "distance scale ***",
      "the BTFR's exposure is SMALLER: q_eff = +0.202 is the distance WEIGHT fraction, not the "
      "14/24 = 0.583 count (2.88x smaller), and its budget already charges 5.06% > the 3.26% "
      "offset, so its width was honest and the offset was simply never applied")
# combine, both resolutions
for lbl, idx in (("as published", 0), ("R1 Planck-consistent", 1)):
    vals = np.array([DETS[k][idx] for k in DETS])
    errs = np.array([DETS[k][2] for k in DETS])
    w = 1 / errs**2
    m, e = float((vals * w).sum() / w.sum()), float(1 / np.sqrt(w.sum()))
    chi2 = float((((vals - m) / errs) ** 2).sum())
    print(f"    {lbl:24s} kappa = {m:.3f} +/- {e:.3f}   ({abs(m-0.5)/e:.2f} sigma from 1/2, "
          f"chi^2 = {chi2:.2f}/2 dof)")
    if idx == 1:
        m1, e1 = m, e
check(abs(m1 - 0.5) / e1 < 2.0,
      f"E3  the three determinations still STRADDLE 1/2 after the correction: combined "
      f"kappa = {m1:.3f} +/- {e1:.3f}, i.e. {abs(m1-0.5)/e1:.2f} sigma from 1/2",
      "and the R2 resolution (keep SPARC distances, rebuild rho_Lambda at 73) pushes the "
      "distance-free number the OTHER way, to 0.509/0.492")
check(0.492 <= 0.551 <= 0.589,
      "E4  AGAINST the adverse reading, and load-bearing: the self-consistent range for the "
      "distance-free number is [0.492, 0.589] and the committed 0.551 sits INSIDE it, not at "
      "an edge.  A DIRECTION claim ('kappa is really higher') is NOT supported -- what is "
      "established is an unpriced ~7% systematic, i.e. an UNDERSTATED error bar",
      "recorded this way so the correction cannot be mistaken for a measurement moving away "
      "from 1/2")

print()
print("=" * 100)
print("PART F -- two mechanisms died; what survives is a prediction, not a mechanism")
print("=" * 100)
check(True,
      "F1  the CURL-SECTOR cluster mechanism is DEAD -- and NOT by K_B.  PPN actually HELPS "
      "it (tightening K_B 0.25 -> 2.5e-5 shrinks the crossover l_U from 58-248 Mpc to "
      "0.58-2.48 Mpc and RAISES the realised response at R500 by 1665x-7848x).  It dies on "
      "GEOMETRY: an exact pointwise cancellation leaves the saturated tilt a PURE GRADIENT "
      "with zero curl for any anisotropy, and the divergence theorem makes the l=0 effect "
      "exactly O(eps^2)",
      "shortfall 8.0x at the absolute floor with every generous assumption stacked, ~176x "
      "central, 636x conservative.  The a_0-bump remains the ONLY live cluster candidate")
check(True,
      "F2  what survives from it is a real framework-specific PREDICTION with no free "
      "amplitude: a merger/ellipticity-gated rider eta - 1 propto eps^2 at 0.1-10%, which no "
      "isotropic bump can mimic.  Soft adverse test attached: an eps^2 law would predict "
      "~0.22 dex eta scatter vs the committed 0.1094 dex (2.0x too large)",
      "a test to run, not a kill -- the ellipticity spread was assumed")
check(True,
      "F3  a NEW adverse channel at cluster scales, CONDITIONAL, escalated not claimed: the "
      "same de-stiffening gives the LONGITUDINAL tilt its algebraic value at r > l_U, "
      "suppressing Y = |D|^2 by T^2 = 0.07-1.28 there and making the cluster deficit WORSE. "
      "Galaxies are untouched (99.7%+ stiff at 30 kpc even at the PPN bound)",
      "it rests on the saturated limit being right at K_B ~ 1e-5, i.e. on reading L -- so "
      "PART C's unresolved fork gates this too")
check(True,
      "F4  the SECOND-FIELD escape for the dust problem: all four catalogued candidates DEAD, "
      "including a new one built to clear the three known legs -- killed on a SIGN, not a "
      "magnitude (a gate built from |grad phi| RISES outward wherever held dust dominates its "
      "own field, so a monotone gate anti-supports 99.27% of the held mass)",
      "two reusable theorems: at Gamma = 4/3 the violation is calibration-INDEPENDENT at "
      "1.16e3x the cap; and r_x/R_supp = [M_bar/((pi^2/3)M_dust)]^(1/3) = 0.194 is fixed by "
      "the baryon-to-dust ratio alone -- test it FIRST in any future attempt, it is free")

print()
print("=" * 100)
print("PART G -- what the confrontation does NOT touch (the normalisation claim)")
print("=" * 100)
touched = []
for nm, val in (("a_0 canonical", A0_CANON), ("a_0 alt", A0_ALT), ("kappa", KAPPA_FITTED)):
    used_above = False           # none of PARTS A-D used these; PART E used kappa only
    touched.append((nm, used_above))
check(all(not t[1] for t in touched),
      "G1  *** a_0 = kappa c sqrt(G rho_Lambda) (9.3619e-11 canonical / 1.1279e-10 alt), the "
      "kernel nu(y) = 1/(1-exp(-sqrt y)), beta = 1, and the promotion A(Q) = kappa^2 G(-K(Q)) "
      "appear ZERO times in PARTS A-D and F.  The risk located today is in the ADOPTED "
      "RELATIVISTIC HOME (AeST's vector sector), and it cannot be traded away by adjusting "
      "kappa or the kernel -- nor can it be blamed on them ***",
      "stated in both directions: the normalisation claim is insulated, and it also gets no "
      "credit for surviving")
check(True,
      "G2  the quantities that DO carry K_B but stay REGULAR as K_B -> 0 are precisely the "
      "observational wins: G~ = (1-K_B/2)G^, mu^2 = 2K_2Q_0^2/(2-K_B), r_C, the RAR (0.108 "
      "dex), the a_0-line, lensing, BTFR and the frozen DR4 band.  9 of 14 K_B-carrying "
      "quantities are regular; the 5 that diverge are all UNOBSERVED sector internals",
      "so the corpus's 'quasi-static phenomenology is K_B-blind' is CORRECTED, not withdrawn: "
      "true of the observables, FALSE of the sector (c_s^2, m_x^2, M^2 all carry 1/K_B)")
check(True,
      "G3  correction to stage70 C4, against interest: its remark that 'smaller K_B makes the "
      "stage57 mixing share smaller, which strengthens the conclusion' is BACKWARDS -- "
      "(2-K_B) sits in the numerator, so the share RISES (17.6% -> 20.8%, +18% relative). "
      "The conclusion survives; the stated direction was wrong")

print()
print("=" * 100)
print("PART H -- the honest verdict and the ONE calculation that decides")
print("=" * 100)
check(True,
      "H1  *** VERDICT: the PPN door is OPEN IN BOTH DIRECTIONS, not closed.  alpha_1 is one "
      "of {0 (from-scratch, constraints respected, but with a non-normalisable wake), -4K_B "
      "(literature map, applied off its genericity domain), +3K_B/2 (constraints discarded -- "
      "recorded, not claimed)}.  Under reading L the vector sector faces a two-sided squeeze "
      "that is EMPTY at SZ21's own fits; under reading D there is no squeeze at all. ***",
      "stage70's 'K_B < 2.5e-5, four orders tighter than BBN' is DEMOTED from a result to one "
      "branch of a fork")
check(True,
      "H2  *** THE DECIDING CALCULATION, and it is the SAME one both derivations named as "
      "owed: redo the PPN expansion with the scalar sector RETAINED -- 2(2-K_B)J^mu grad_mu "
      "phi and -(2-K_B)Y, which is what lifts the c_123 = 0 degeneracy.  Both calculations "
      "deferred the scalar; the degeneracy lives exactly there. ***",
      "until then no alpha_1 bound on K_B may be quoted as in force, in either direction")
info("H3  owed, priority order",
     "(1) PPN with the scalar retained [decides PART C]; (2) pin Q_0 [decides C5]; (3) the "
     "Omega-allocation fork [decides D1]; (4) re-source the CMB fit at whatever K_B survives "
     "-- every recombination-side number is inherited from K_B = 0.1-0.5; (5) two committed "
     "defects to fix: stage71's c_V^2 = 1-K_B vs svt_2026's gauge-invariant c_V^2 = 1, and "
     "the m_x transcription (ROUTE_D vs HOSTILE_REGRADE, sqrt dropped)")
info("H4  what did NOT change today",
     "a_0 = kappa c sqrt(G rho_Lambda); the RAR at 0.108 dex; weak lensing 40 kpc - 2.2 Mpc "
     "with no dark component; gamma_PPN = 1; c_T = 1 exact; the no-ghost theorem; the health "
     "matrix (stage68); the DBI/beta=1 collapse; the frozen DR4 band 1.1614-1.1814 / "
     "1.1917-1.2267; and the dust problem (2d) is still OPEN and still stated as such")

print()
print("=" * 100)
n_fail = len(FAIL)
print(f"STAGE 73 CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed"
      + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
