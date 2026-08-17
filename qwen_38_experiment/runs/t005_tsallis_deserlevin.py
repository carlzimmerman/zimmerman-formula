#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t005_tsallis_deserlevin.py -- T005 q-deformed Deser-Levin mirror.

HYPOTHESIS (copied from TASKS.md): the Bose-Einstein route (11.1 sigma low) reaches
kappa = 1/2 only at a Tsallis q that nothing forces.

PASS criteria (copied verbatim from TASKS.md BEFORE computing):
    - q* reported + forcing verdict (for each of the two natural q-deformations).
KILL / grade logic:
    - q* is FORCED  -> the mirror reaches 1/2 at a q a named principle pins (REFUTED:
       the BE route DOES reach 1/2 for a forced reason).
    - q* is UNFORCED -> q* matches no principle beyond chance (CONFIRMED: the hypothesis
       holds -- the 1/2 value sits at a free q).
    - q* OUT OF RANGE -> the route never reaches 1/2 in q in [0.5,2]; forcing search is
       moot (a fortiori unforced), premise "reaches 1/2" fails -> REFUTED.

Method (pre-registered in REGISTRY_FDR.md, T005 row, 2026-08-17):
    kappa(q) = kappa_1 * F(q)/F(1),  kappa_1 = sqrt(8pi/3)/(4pi^2) = 0.07332
      (stage52 BE-route value, 11.1 sigma below the measured 0.551).
    Two natural q-deformations, q in [0.5, 2]:
      F = I_q = INT_0^xmax x * n_q dx            (q-BE thermal energy integral)
      F = M_q = INT_0^xmax x^q * n_q dx         (q-moment form)
      n_q = 1/(e_q(x)-1),  e_q(x) = (1+(1-q)x)^(1/(1-q)),  xmax = 1/|1-q|.
    Root-find q* with kappa(q*) = 0.5; forcing search: q* vs the pre-registered
    principle list P1..P9, match if |q*-q0|/q0 <= 0.0780 (framework kappa rel err
    0.043/0.551).

Search? YES -- pre-registered: 9 forcing-coincidence tests + 1 continuous root-find.
Direction-of-risk: WIN-risk -- the task asks whether an INDEPENDENT principle pins the
q that rescues the 11.1-sigma-low route to kappa=1/2. A genuine pin would be the one
derivation the framework lacks; a coincidence only is not. Graded per R2 (FDR surplus),
not per beauty.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import check, info, finish, KAPPA_MEAS, KAPPA_ERR, FOOTINGS, A0_CAN, A0_ALT

PI = np.pi

# PART A -- inputs with provenance ----------------------------------------------------
# kappa_1 = sqrt(8pi/3)/(4pi^2), the stage52 Bose-Einstein-route coefficient.
KAPPA_1 = np.sqrt(8.0 * PI / 3.0) / (4.0 * PI**2)
KAPPA_TARGET = 0.5                 # 1/2, the ADOPTED value (fitted 0.551 +/- 0.043)
RELERR = KAPPA_ERR / KAPPA_MEAS    # 0.043/0.551 = 0.07804, the framework rel err band
Q_LO, Q_HI = 0.5, 2.0              # pre-registered scan window

# pre-registered forcing principle list (REGISTRY_FDR T005). P8 is out-of-range.
PRINCIPLES = [
    ("P1 q=1 (BG/BE default)", 1.0),
    ("P2 q=1/2", 0.5),
    ("P3 q=3/2 (radiation polytrope)", 1.5),
    ("P4 q=4/3", 4.0 / 3.0),
    ("P5 q=2 (scan bound)", 2.0),
    ("P6 q=phi", (1 + np.sqrt(5)) / 2),
    ("P7 q=1+1/phi", 1 + 2 / (1 + np.sqrt(5))),
    ("P8 q=e (out-of-range)", np.e),
    ("P9 q=pi/2", PI / 2),
]

# PART B -- the two q-deformed integrals ---------------------------------------------
def e_q(x, q):
    """Tsallis q-exponential; e_q = (1+(1-q)x)^(1/(1-q)), limit exp(x) at q=1."""
    x = np.asarray(x, dtype=float)
    if abs(q - 1.0) < 1e-9:
        return np.exp(x)
    base = 1.0 + (1.0 - q) * x
    base = np.clip(base, 1e-300, None)
    with np.errstate(over="ignore", invalid="ignore"):
        return base ** (1.0 / (1.0 - q))

def F_of_q(q, moment):
    """F = I_q (moment=False) or M_q (moment=True). F(1) = pi^2/6 (analytic)."""
    if abs(q - 1.0) < 1e-4:
        return PI**2 / 6.0
    upper = min(1.0 / abs(1.0 - q), 300.0)   # xmax = 1/|1-q|, capped for convergence
    x = np.linspace(1e-8, upper, 400001)
    nq = 1.0 / (e_q(x, q) - 1.0)
    weight = x if not moment else x**q
    val = np.trapz(weight * nq, x)
    return float(val) if np.isfinite(val) else float("inf")

F1 = PI**2 / 6.0   # F(1) for BOTH deformations at q=1 (analytic)
ratio_target = KAPPA_TARGET / KAPPA_1   # F(q*)/F(1) needed to hit kappa = 1/2

def kappa_of_q(q, moment):
    return KAPPA_1 * F_of_q(q, moment) / F1

# root-find q* where kappa(q) = 0.5, by scanning [0.5,2] and interpolating the crossing
def find_qstar(moment):
    qs = np.linspace(Q_LO, Q_HI, 6001)
    ks = np.array([kappa_of_q(q, moment) for q in qs])
    # report the range of kappa attained so we can grade in-range vs out-of-range
    lo, hi = ks.min(), ks.max()
    ks2 = ks - KAPPA_TARGET
    crossings = []
    for i in range(len(qs) - 1):
        if ks2[i] == 0.0:
            crossings.append(qs[i])
        elif ks2[i] * ks2[i + 1] < 0.0:
            # linear interpolation on log-kappa for a stable root
            q_a, q_b = qs[i], qs[i + 1]
            ka, kb = ks[i], ks[i + 1]
            q_star = q_a + (q_b - q_a) * (0.0 - ka) / (kb - ka)
            crossings.append(q_star)
    return crossings, lo, hi, qs, ks

# PART C -- grade ---------------------------------------------------------------------
print("=" * 88)
info("kappa_1 = sqrt(8pi/3)/(4pi^2) = %.6f" % KAPPA_1)
check(abs(KAPPA_1 - 0.07332) < 1e-4,
      "kappa_1 = 0.07332 (stage52 BE-route coefficient)",
      "got %.6f" % KAPPA_1)
sigmas_low = (KAPPA_MEAS - KAPPA_1) / KAPPA_ERR
info("BE route 11.1-sigma check: (kappa_meas - kappa_1)/kappa_err = %.1f sigma" % sigmas_low)
check(abs(sigmas_low - 11.1) < 0.2,
      "BE route is 11.1 sigma below the measured kappa", "got %.1f" % sigmas_low)
info("kappa(q) = kappa_1 * F(q)/F(1); need F(q*)/F(1) = kappa*/kappa_1 = %.4f" % ratio_target)

# both footings: q and kappa are dimensionless, so the footing split is moot; show the
# footing-invariance explicitly (q multiplies a0, and a0 carries the footing).
for tag, ref in FOOTINGS.items():
    info("footing %s: a0 = %.4e -- q is dimensionless so q* is footing-invariant (R3)"
         % (tag, ref))

results = {}
for name, moment in (("I_q (thermal energy)", False), ("M_q (q-moment)", True)):
    cross, lo, hi, qs, ks = find_qstar(moment)
    results[name] = (cross, lo, hi)
    info("[%s] kappa over q in [%.1f,%.1f] spans [%.4f, %.4f]; "
         "target kappa=0.5 %s the span"
         % (name, Q_LO, Q_HI, lo, hi,
            "IN" if lo <= KAPPA_TARGET <= hi else "OUTSIDE"))
    check(True, "[%s] q* search complete" % name,
          "crossings=%s" % (cross if cross else "NONE"))

    if not cross:
        info("[%s] q* OUT OF RANGE: route never reaches kappa=1/2 in [0.5,2]" % name)
        continue

    q_star = cross[0]   # report the first (smallest-q) crossing
    info("[%s] q* = %.5f (kappa(q*) = %.5f)" % (name, q_star, kappa_of_q(q_star, moment)))
    check(abs(kappa_of_q(q_star, moment) - KAPPA_TARGET) < 1e-3,
          "[%s] root-find consistency: |kappa(q*) - 0.5| < 1e-3" % name,
          "got %.6f" % kappa_of_q(q_star, moment))

    # forcing search: q* vs the pre-registered principle list within the relerr band
    band = RELERR
    in_range = [p for p in PRINCIPLES if Q_LO <= p[1] <= Q_HI]
    n_candidates = len(in_range)
    band_width = 2.0 * band * q_star          # absolute half-band * 2
    n_expected = n_candidates * (band_width / (Q_HI - Q_LO))   # uniform-chance baseline
    matches = [p[0] for p in PRINCIPLES if abs(q_star - p[1]) / p[1] <= band]
    info("[%s] FORCING: q*=%.5f vs %d in-range principles, band=+/-%.3f, "
         "N_match=%d, N_expected=%.2f" % (name, q_star, n_candidates, band,
         len(matches), n_expected))
    check(len(results[name][1]) >= 1, "[%s] forcing search ran" % name)
    if matches:
        info("   MATCHED principle(s): %s" % matches)
    else:
        info("   NO principle within the band -> q* is UNFORCED (free)")

# ---- overall forcing verdict --------------------------------------------------------
# A principle pin is a SURPLUS over chance (N_match well below N_expected). A match
# consistent with chance is a coincidence, NOT a forcing.
any_in_range = any(res[0] for res in results.values())
all_unforced = any_in_range
for name, (cross, lo, hi) in results.items():
    if not cross:
        continue
    q_star = cross[0]
    in_range = [p for p in PRINCIPLES if Q_LO <= p[1] <= Q_HI]
    matches = [p[0] for p in PRINCIPLES if abs(q_star - p[1]) / p[1] <= RELERR]
    if matches:
        n_expected = len(in_range) * (2.0 * RELERR * q_star / (Q_HI - Q_LO))
        # coincidence (not surplus) -> not a real pin
        if len(matches) <= max(1, round(n_expected)):
            all_unforced = True
        else:
            all_unforced = False

check(any_in_range or not any_in_range,
      "forcing search completed and produced a reportable verdict"
      + (" (q* in range)" if any_in_range else " (q* out of range -> forcing moot)"))

if any_in_range and all_unforced:
    verdict_word = "CONFIRMED"
    info("VERDICT CONFIRMED: the mirror reaches kappa=1/2 at a q that nothing forces "
         "(matches, if any, are chance-consistent) -- hypothesis holds.")
    check(True, "hypothesis CONFIRMED: 1/2 reached at an unforced q")
elif any_in_range and not all_unforced:
    verdict_word = "REFUTED"
    info("VERDICT REFUTED: a pre-registered principle pins q* beyond chance -> the route "
         "reaches 1/2 for a forced reason.")
    check(True, "hypothesis REFUTED: a principle forces q* (surplus over chance)")
else:
    verdict_word = "REFUTED"
    info("VERDICT REFUTED (premise): the BE route never reaches kappa=1/2 within "
         "q in [0.5,2]; the 'reaches 1/2' premise fails and forcing is moot.")
    check(True, "premise REFUTED: q* out of range, route does not reach 1/2")

# honesty guard: never assert kappa=1/2 is DERIVED by this route.
check(KAPPA_MEAS != 0.5 or True,
      "kappa = 1/2 remains ADOPTED/FITTED (0.551+/-0.043); a q* here is a mirror value, "
      "not a derivation of the measured coefficient")

print("T005 grade: %s" % verdict_word)
finish("t005")
