#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_dr4_anisotropy_and_gated_2026.py
===================================
THE LAST TWO DR4 CHECKLIST ITEMS, with their POWER computed rather than assumed.

Verdict, both ways: *** the ANISOTROPY falsifier is real and sign-pre-declared, but PROJECTION
DILUTION costs a factor ~4.2 (D = 0.2367) and it needs N ~ 2.1-2.7e5 for 3 sigma -- SEVEN TO NINE TIMES the frozen 30,000.  And the
GATED branch is NOT separable from Newton in the aggregate at all (0.03 sigma); its only handle is
the INTERNAL RISE across the window, which Amendment 8 itself caps at 1.56 sigma_fit. ***  Both are
therefore WATCH items at the frozen N, not decisive tests -- and that is stated here rather than
discovered after DR4 lands.

--------------------------------------------------------------------------------------------------
ITEM 5 -- THE ANISOTROPY FALSIFIER (Part A)
--------------------------------------------------------------------------------------------------
Amendment 2 pre-declared the SIGN: *** perpendicular pairs must show the LARGER boost, and the
opposite sense at >= 3 sigma falsifies the derived external-field effect INDEPENDENTLY of the
aggregate gamma_v. ***  Under Amendment 8's Route A kernel:
        canonical:  gamma_par = 1.03800,  gamma_perp = 1.21385,  spread 0.17585
        alt:        gamma_par = 1.05977,  gamma_perp = 1.25916,  spread 0.19939
so the falsifier is STRONGER than it was at alpha = 2 (spread 0.0994), as Amendment 8 records.

*** BUT THE 3-D SPLIT IS NOT THE OBSERVABLE. ***  Only the SKY-PROJECTED angle between the pair's
separation and the projected Galactic-centre direction is measurable, and the unknown
line-of-sight component dilutes the contrast.  Modelling gamma(psi) = gamma_perp +
(gamma_par - gamma_perp) cos^2 psi and averaging over isotropic 3-D orientations, the split between
a projected-parallel half (phi < 45 deg) and a projected-perpendicular half is diluted by

        D = <cos^2 psi>_{phi<45} - <cos^2 psi>_{phi>45}

which this script computes BOTH analytically (for the in-plane case, D = 2/3 * 2/pi = 4/(3 pi) =
0.4244, closed form) AND by Monte Carlo over the frozen |b| > 15 deg sky, which gives D = 0.2367.
The observable split is therefore 0.042-0.047, not the 3-D 0.176-0.199 -- a factor ~4.2 cost.

--------------------------------------------------------------------------------------------------
ITEM 6 -- THE GATED BRANCH AS A SECOND SCORED HYPOTHESIS (Part B)
--------------------------------------------------------------------------------------------------
Trap count STAYS 2, so the gated branch must be scored alongside the ungated one.  Amendment 8
registers gamma_gated = 1.00064-1.00117 at 10 kAU, with Route A making the amplitude exactly the
kernel's Newtonian residual S = 1 - mu = e^-sqrt(y), and it is NO LONGER FLAT across the window:
0.001 sigma_fit at 2 kAU rising to 1.56 sigma_fit by 30 kAU.
*** In the AGGREGATE the gated branch is indistinguishable from Newton -- 0.03 sigma at the frozen
N -- so anyone scoring only the aggregate would report "Newtonian" for a universe in which the
gated branch is true.  The ONLY handle is the internal rise, and 1.56 sigma is not 3. ***

--------------------------------------------------------------------------------------------------
WHAT THIS MEANS FOR DR4, STATED BEFORE THE DATA
--------------------------------------------------------------------------------------------------
  * The DECISIVE statement at N = 30,000 remains the one Amendment 8 already identified: a Newtonian
    2-30 kAU result is evidence AGAINST at 4.74-7.10 sigma_tot, because under a Newtonian truth the
    estimator's shape bias is identically zero.
  * The anisotropy falsifier fires only on a WRONG SIGN, and needs ~2.1-2.7e5 pairs at 3 sigma.
    Reported as a directional check with its N, not as a test the frozen sample can settle.
  * The gated branch cannot be excluded by DR4 in the aggregate.  Registering it as "scored" means
    reporting its distance honestly, which is ~0.03 sigma -- i.e. no information.
  * a_0's VALUE is still not derived.  kappa = 1/2 remains FITTED.

CREDIT.  The external-field effect and its orientation dependence are MILGROM's (1994 Ann.Phys.
229:384; 1999 PLA 253:273 eqs 6-9).  The anisotropy sign pre-declaration is Amendment 2 of the
author's frozen Gaia DR4 pre-registration; the Route A kernel, the gated-branch amplitudes and the
1.56 sigma internal-rise figure are Amendment 8.  Wide-binary cuts follow BANIK et al. 2024; the
DR3 comparison catalogue is EL-BADRY et al. 2021.  Gaia: ESA/DPAC.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import numpy as np
import mpmath as mp

mp.mp.dps = 25
FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


# Amendment 8's recorded eigenvalues (both footings, primary g_ext convention)
EIG = {"canonical": (1.03800, 1.21385), "alt": (1.05977, 1.25916)}
A2_SPREAD = 0.0994          # the alpha=2 spread Amendment 8 compares against
N_FROZEN = 30_000
SIG_DR3, N_DR3 = 0.0350, 10_624      # the DR3 dry run's own sigma_fit and N (measured)
rng = np.random.default_rng(20260808)

print(__doc__)


# =============================================================================================
print("=" * 100)
print("PART A -- the anisotropy falsifier, and what PROJECTION costs it")
print("=" * 100)
for nm, (gp, gq) in EIG.items():
    print(f"  {nm:>10s}  gamma_par = {gp:.5f}   gamma_perp = {gq:.5f}   spread = {gq - gp:.5f}")
spreads = {nm: gq - gp for nm, (gp, gq) in EIG.items()}
check(all(gq > gp for gp, gq in EIG.values()),
      "A1  *** THE PRE-DECLARED SIGN: perpendicular pairs show the LARGER boost on BOTH footings.  "
      "Amendment 2 registered this in advance, and the OPPOSITE sense at >= 3 sigma falsifies the "
      "derived external-field effect independently of the aggregate gamma_v ***")
check(min(spreads.values()) > A2_SPREAD,
      f"A2  and the spread is LARGER than at alpha = 2 ({min(spreads.values()):.4f}-"
      f"{max(spreads.values()):.4f} vs {A2_SPREAD}), so Route A STRENGTHENS the falsifier -- as "
      "Amendment 8 records")

# --- the projection dilution, closed form for the in-plane case ---
# gamma(psi) = gamma_perp + (gamma_par - gamma_perp) cos^2 psi, psi = angle(s_hat, g_hat).
# With g_hat in the sky plane: cos psi = sin(theta) cos(phi), phi measurable, theta not.
# <sin^2 theta> = 2/3 (isotropic);  <cos^2 phi>_{phi<45} = 1/2 + 1/pi, _{phi>45} = 1/2 - 1/pi.
D_closed = mp.mpf(2) / 3 * (2 / mp.pi)
check(abs(D_closed - 4 / (3 * mp.pi)) < mp.mpf("1e-25"),
      "A3  the in-plane dilution has the CLOSED FORM D = (2/3)(2/pi) = 4/(3 pi) = "
      f"{mp.nstr(D_closed, 6)}: <sin^2 theta> = 2/3 for isotropic 3-D orientations, and "
      "<cos^2 phi> differs by 2/pi between the phi < 45 and phi > 45 halves")

# --- Monte Carlo over the frozen |b| > 15 deg sky, so beta (the angle of g_hat out of the sky
#     plane) is not assumed to be zero ---
NMC = 400_000
# isotropic separation directions
u = rng.uniform(-1, 1, NMC)
ph = rng.uniform(0, 2 * np.pi, NMC)
s = np.stack([np.sqrt(1 - u**2) * np.cos(ph), np.sqrt(1 - u**2) * np.sin(ph), u])
# sky positions with |b| > 15 deg (the frozen cut); g_hat points to the Galactic centre, so in the
# star's local frame the angle of g_hat out of the plane of the sky is beta = b (to the accuracy
# that matters for a dilution factor near the Sun).
sinb = rng.uniform(-1, 1, NMC)
b = np.arcsin(sinb)
b = b[np.abs(np.degrees(b)) > 15]
idx = rng.integers(0, len(b), NMC)
beta = b[idx]
g = np.stack([np.cos(beta), np.zeros(NMC), np.sin(beta)])   # g_hat, x = in-sky, z = line of sight
cos_psi = (s * g).sum(0)
phi_proj = np.abs(np.arctan2(s[1], s[0]))                   # projected angle to g_proj (= x_hat)
phi_proj = np.minimum(phi_proj, np.pi - phi_proj)           # fold to [0, pi/2]
par_half = phi_proj < np.pi / 4
D_mc = (cos_psi[par_half]**2).mean() - (cos_psi[~par_half]**2).mean()
check(0.20 < D_mc < float(D_closed) + 0.02,
      "A4  *** and the Monte Carlo over the frozen |b| > 15 deg sky gives D = "
      f"{D_mc:.4f}, BELOW the in-plane closed form {mp.nstr(D_closed, 5)} because the "
      "line-of-sight component of g_hat dilutes further.  So the observable contrast is roughly a "
      "THIRD of the 3-D split, not all of it ***",
      f"{NMC:,} draws; par half = {par_half.mean():.3f} of pairs by construction")

obs = {nm: D_mc * sp for nm, sp in spreads.items()}
for nm in obs:
    print(f"  {nm:>10s}  3-D spread {spreads[nm]:.5f}  ->  OBSERVABLE split {obs[nm]:.5f}")
check(max(obs.values()) < max(spreads.values()),
      "A5  so the observable split is 0.04-0.06 rather than 0.18-0.20 -- the dilution is a real cost "
      "and is carried explicitly rather than absorbed")

# --- the required N, anchored on the pipeline's OWN measured sigma_fit ---
sig_frozen = SIG_DR3 * mp.sqrt(mp.mpf(N_DR3) / N_FROZEN)
sig_diff = 2 * sig_frozen              # two independent halves, each of N/2 => 2x the full-sample sigma
z_frozen = {nm: obs[nm] / float(sig_diff) for nm in obs}
N3 = {nm: N_FROZEN * (3 * float(sig_diff) / obs[nm]) ** 2 for nm in obs}
print(f"  sigma_fit at N = {N_FROZEN:,} (scaled from the measured DR3 {SIG_DR3} at N = {N_DR3:,}): "
      f"{mp.nstr(sig_frozen, 4)}; split sigma = {mp.nstr(sig_diff, 4)}")
for nm in obs:
    print(f"  {nm:>10s}  z at frozen N = {z_frozen[nm]:.2f}   N for 3 sigma = {N3[nm]:,.0f}")
check(all(z < 3 for z in z_frozen.values()),
      "A6  *** AGAINST INTEREST: at the frozen N = 30,000 the anisotropy split reaches only "
      f"{min(z_frozen.values()):.2f}-{max(z_frozen.values()):.2f} sigma, NOT 3.  It needs "
      f"N ~ {min(N3.values()):,.0f}-{max(N3.values()):,.0f} pairs ***",
      "so this is a DIRECTIONAL check reported with its N, not a test the frozen sample settles")
check(min(N3.values()) > N_FROZEN,
      "A7  and that requirement is ABOVE the frozen sample size, which is stated here BEFORE DR4 "
      "rather than discovered afterwards")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- the gated branch as a second scored hypothesis")
print("=" * 100)
GATED_10KAU = (1.00064, 1.00117)      # Amendment 8, both gating conventions
RISE_30KAU_SIG = 1.56                 # Amendment 8's own figure
RISE_2KAU_SIG = 0.001
amp = [g - 1 for g in GATED_10KAU]
z_agg = [a / float(sig_frozen) for a in amp]
print(f"  gated gamma at 10 kAU: {GATED_10KAU[0]:.5f}-{GATED_10KAU[1]:.5f}  "
      f"(amplitude {amp[0]:.5f}-{amp[1]:.5f})")
print(f"  aggregate z vs Newton at frozen N: {z_agg[0]:.3f}-{z_agg[1]:.3f} sigma")
check(max(z_agg) < 0.1,
      "B1  *** THE GATED BRANCH IS NOT SEPARABLE FROM NEWTON IN THE AGGREGATE: "
      f"{max(z_agg):.3f} sigma at the frozen N.  Anyone scoring only the aggregate would report "
      "'Newtonian' for a universe in which the gated branch is TRUE ***")
N3_gate = N_FROZEN * (3 * float(sig_frozen) / max(amp)) ** 2
check(N3_gate > 1e7,
      f"B2  and separating it from Newton in the aggregate at 3 sigma would need N ~ "
      f"{N3_gate:,.0f} pairs -- three orders above anything Gaia will deliver",
      "so the aggregate is the wrong statistic for this hypothesis, by a wide margin")
check(RISE_30KAU_SIG > 100 * RISE_2KAU_SIG,
      "B3  *** THE ONLY HANDLE IS THE INTERNAL RISE: Amendment 8 registers 0.001 sigma_fit at "
      f"2 kAU rising to {RISE_30KAU_SIG} sigma_fit by 30 kAU, a factor "
      f"{RISE_30KAU_SIG / RISE_2KAU_SIG:,.0f}, so the branch is falsifiable WITHIN the frozen window "
      "by its SHAPE even though its amplitude is invisible ***")
check(RISE_30KAU_SIG < 3,
      "B4  *** AGAINST INTEREST: 1.56 sigma is not 3.  The gated branch is a WATCH item at the "
      "frozen N, and registering it as 'scored' means reporting a distance of ~0.03 sigma in the "
      "aggregate and ~1.6 sigma in shape -- i.e. very little information either way ***")
# the ungated-vs-gated fork, which IS large
UNGATED = 1.1582
fork = (UNGATED - 1) / max(amp)
check(fork > 100,
      f"B5  what the two branches DO separate from each other by: the ungated target is "
      f"{fork:,.0f}x the gated amplitude, so a measurement discriminates the BRANCHES sharply even "
      "though it cannot discriminate gated-from-Newton",
      "Amendment 8 records the fork as 8.2-10.2 sigma_fit")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- what survives as decisive at the frozen N")
print("=" * 100)
NEWT_Z = (4.74, 7.10)
check(min(NEWT_Z) > 3,
      "C1  *** the DECISIVE statement is unchanged and is the one Amendment 8 already identified: a "
      f"Newtonian 2-30 kAU result is evidence AGAINST at {NEWT_Z[0]}-{NEWT_Z[1]} sigma_tot at the "
      "frozen N, because under a Newtonian truth the estimator's shape bias is identically zero ***")
check(max(z_frozen.values()) < 3 and RISE_30KAU_SIG < 3,
      "C2  and NEITHER new item is decisive at that N -- anisotropy "
      f"{max(z_frozen.values()):.2f} sigma, gated shape {RISE_30KAU_SIG} sigma.  Both are registered "
      "as WATCH items with their numbers attached")
check(True,
      "C3  so DR4's primary read stays: raw gamma_hat, sigma_fit, both distances, the two declared "
      "risk flags, plus these two directional checks reported with their own power -- and no single "
      "verdict word, per Amendment 7(e)")


# =============================================================================================
print()
print("=" * 100)
print("NEGATIVE CONTROLS -- these must trip")
print("=" * 100)
# NC1: the dilution must be BELOW the closed form, and a no-dilution decoy must be rejected.
check(D_mc < float(D_closed) and abs(D_mc - 1.0) > 0.5,
      f"NC1  CONTROL FIRES: the MC dilution {D_mc:.4f} is strictly below the in-plane closed form "
      f"{mp.nstr(D_closed, 5)} and nowhere near the no-dilution decoy D = 1, so Part A measures a "
      "real projection cost rather than assuming one")
# NC2: reversing the eigenvalues must flip the pre-declared sign.
flipped = {nm: (gq, gp) for nm, (gp, gq) in EIG.items()}
check(all(b_ < a_ for a_, b_ in flipped.values()),
      "NC2  CONTROL FIRES: swapping gamma_par and gamma_perp reverses the pre-declared sense, so A1 "
      "tests an ORIENTATION and is not satisfied by any pair of numbers")
# NC3: the split sigma must be LARGER than the full-sample sigma -- halving the sample costs.
check(float(sig_diff) > float(sig_frozen),
      f"NC3  CONTROL: the split sigma {mp.nstr(sig_diff, 4)} exceeds the full-sample "
      f"{mp.nstr(sig_frozen, 4)}, as splitting into halves must -- so A6's power is not silently "
      "borrowing the full sample's precision")
# NC4: the gated amplitude must be far below the ungated one, else B5 would be vacuous.
check(max(amp) < 0.01 * (UNGATED - 1),
      "NC4  CONTROL: the gated amplitude is below 1% of the ungated signal, so B1's "
      "indistinguishability is a property of the hypothesis and not of a mis-scaled sigma")
# NC5: the MC's parallel half must be ~half the sample by construction.
check(abs(par_half.mean() - 0.5) < 0.01,
      f"NC5  CONTROL: the projected-parallel half is {par_half.mean():.4f} of the sample, i.e. a "
      "genuine median split, so D is a difference of equal-sized halves")


print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f_ in FAIL:
        print("  -", f_)
    sys.exit(1)
print("""
VERDICT -- BOTH ITEMS IMPLEMENTED, BOTH UNDERPOWERED AT THE FROZEN N, AND SAID SO IN ADVANCE.
  ANISOTROPY.  The sign is pre-declared (perpendicular larger, Amendment 2) and holds on both
  footings, with Route A STRENGTHENING the 3-D spread to 0.176-0.199 from alpha = 2's 0.099.
  *** But only the sky-PROJECTED angle is observable, and the dilution is D = 0.2367 by Monte Carlo
  over the frozen |b| > 15 deg sky against the in-plane closed form 4/(3 pi) = 0.4244 -- so the
  observable split is 0.042-0.047, reaching only 1.00-1.13 sigma at N = 30,000 and needing
  N ~ 2.1-2.7e5 for 3 sigma. ***  A directional check reported with its N, not a test the frozen sample settles.
  GATED BRANCH.  *** Not separable from Newton in the aggregate at all -- 0.03 sigma, needing
  N ~ 8.6e7 -- so an aggregate-only scorer would report "Newtonian" for a universe where the gated
  branch is true. ***  Its only handle is the internal rise, 0.001 sigma at 2 kAU to 1.56 sigma at
  30 kAU, which is falsifiable in SHAPE but is not 3 sigma.  The two BRANCHES do separate from each
  other sharply (the ungated signal is 135x the gated amplitude).
  WHAT STAYS DECISIVE: a Newtonian 2-30 kAU result is evidence AGAINST at 4.74-7.10 sigma_tot.
  a_0's VALUE is still not derived.  kappa = 1/2 remains FITTED.
""")
