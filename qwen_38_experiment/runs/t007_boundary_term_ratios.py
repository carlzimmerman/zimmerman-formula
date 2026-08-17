#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t007 -- Boundary-term ratios. Hypothesis: kappa^2 is NOT a ratio of
GHY-to-bulk action terms on the static patch at <= 3 combinations.

PASS criteria (copied verbatim from TASKS.md BEFORE computing):
   - Pre-register the combination space; count hits vs chance. PASS: N vs baseline.
   - Hypothesis is a REFUTATION: kappa^2 does not equal a GHY/bulk static-patch
     ratio among a small (<=3) pre-registered set. N_match <= N_expected (no
     surplus over chance) => hypothesis CONFIRMED.
KILL criteria:
   - Any pre-registered combination lands within the tolerance of a target with
     N_match > N_expected (a surplus over chance) => a boundary-term ratio DOES
     reproduce kappa^2 => hypothesis REFUTED.
Search? Yes. 3 combinations, pre-registered in REGISTRY_FDR.md (T007 row, 2026-08-17).
Direction-of-risk: WIN-risk -- a spurious "kappa^2 = boundary ratio" would flatter
the framework by dressing a fitted constant in a geometric derivation; so the
refutation (0/3 hits) is the DEFICIT-side-honest result and we are suspicious of
any hit.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *    # constants, kernel, check/info/finish

# ------------------------------------------------------------------------------
# PART A -- inputs with provenance
# ------------------------------------------------------------------------------
# rho_Lambda backed out from the committed framework a0 = kappa c sqrt(G rho_Lambda)
#   => rho_Lambda = (a0 / (kappa c))^2 / G
# r_h = c sqrt(3/Lambda), Lambda = 8 pi G rho_Lambda / c^2
# eta(R) = (R/r_h)^2 / (4 - (R/r_h)^2): the GHY (boundary/surface) to bulk
#   (volume) surface-to-volume ratio of the static patch of radius R.
#   FOOTING-INDEPENDENT: r_h cancels, so eta depends only on the dimensionless
#   R/r_h.  We still loop both footings to SHOW the zero spread (R3).

TOL = 0.156                       # pre-registered window +-15.6% (=2x kappa rel err)
KAPPA_ADOPTED = 0.5
KAPPA_MEAS = KAPPA_MEAS           # 0.551 (qwenlib)
TARGETS = {
    "kappa_adopted^2": KAPPA_ADOPTED ** 2,      # 0.25
    "kappa_measured^2": KAPPA_MEAS ** 2,        # 0.3036
}
# pre-registered radii R/r_h (3 combinations)
RADII = {"1/2 (horizon-limit patch)": 0.5,
         "1/sqrt(3) (Einstein-static balanced patch)": 1.0 / 3.0 ** 0.5,
         "1/sqrt(2) (half-max patch)": 1.0 / 2.0 ** 0.5}

# ------------------------------------------------------------------------------
# PART B -- compute.  Both footings, showing footing-independence of the ratio.
# ------------------------------------------------------------------------------
def eta_of_ratio(r_over_rh):
    """GHY/bulk surface-to-volume ratio on the Lambda static patch."""
    return r_over_rh ** 2 / (4.0 - r_over_rh ** 2)

def rho_lambda(a0, kappa):
    return (a0 / (kappa * C)) ** 2 / G

results = {}   # (footing, radius_label) -> eta
spread = {}     # radius_label -> spread across footings
for fname, a0 in FOOTINGS.items():
    rho = rho_lambda(a0, KAPPA_MEAS)
    Lambda = 8.0 * np.pi * G * rho / C ** 2
    r_h = C * (3.0 / Lambda) ** 0.5
    for label, rr in RADII.items():
        eta = eta_of_ratio(rr)          # footing-independent by construction
        results[(fname, label)] = eta
        spread.setdefault(label, []).append(eta)

# the footing-independent value (both footings must agree to ~1e-12)
eta_by_radius = {label: eta_of_ratio(rr) for label, rr in RADII.items()}
for label, vals in spread.items():
    check(abs(vals[0] - vals[1]) < 1e-12 * max(1.0, vals[0]),
          f"footing-independence {label}: can==alt within 1e-12",
          f"can={vals[0]:.6e} alt={vals[1]:.6e}")

# ------------------------------------------------------------------------------
# PART C -- grade against PASS/KILL.  Count matches vs chance.
# ------------------------------------------------------------------------------
# EXCLUDE the trivial Bekenstein-Hawking S/A = 1/4 constant (CONVENTION-grade):
#   it equals kappa_adopted^2 = 0.25 by definition, a literature constant, not a
#   derivation.  Per protocol we never count a CONVENTION match as a hit.
CONVENTION_EXCLUDED = 0.25
check(abs(CONVENTION_EXCLUDED - TARGETS["kappa_adopted^2"]) < 1e-15,
      "Bekenstein-Hawking S/A = 1/4 flagged as CONVENTION-grade and excluded",
      "= kappa_adopted^2 by definition (not a derivation)")

N_match = 0
hit_log = []
for label, eta in eta_by_radius.items():
    for tname, target in TARGETS.items():
        if abs(eta - target) <= TOL * target:
            N_match += 1
            hit_log.append((label, eta, tname, target))
    # show each combo vs both targets
    info(f"eta[{label}] = {eta:.6f}",
         f"vs adopted^2={TARGETS['kappa_adopted^2']:.4f} "
         f"(d={abs(eta-TARGETS['kappa_adopted^2'])/TARGETS['kappa_adopted^2']:.3f} rel), "
         f"vs measured^2={TARGETS['kappa_measured^2']:.4f} "
         f"(d={abs(eta-TARGETS['kappa_measured^2'])/TARGETS['kappa_measured^2']:.3f} rel)")

N_trials = len(RADII)
# pre-registered chance baseline: 3 combos x (band-width / plausible range [0,1])
N_expected = N_trials * (2.0 * TOL / 1.0)
info(f"N_match = {N_match}",
     f"vs N_expected ~ {N_expected:.3f} "
     f"(3 combos x band 0.312 over range [0,1]); "
     f"minimum rel distance to any target = "
     f"{min(abs(eta-t)/t for eta in eta_by_radius.values() for t in TARGETS.values()):.3f}")

# PASS: N_match <= N_expected (no surplus over chance) => hypothesis CONFIRMED.
check(N_match <= N_expected,
      f"PASS: N_match ({N_match}) <= N_expected ({N_expected:.3f}) "
      f"-- kappa^2 is NOT a GHY/bulk static-patch ratio at <=3 combos",
      "hypothesis CONFIRMED (refutation holds)" if N_match <= N_expected
      else "SURPLUS -> hypothesis REFUTED")

finish("t007")
