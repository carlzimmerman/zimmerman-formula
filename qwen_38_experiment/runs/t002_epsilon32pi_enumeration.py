#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t002 -- eps_tot = 1/(32*pi): is it special among le-3-factor products of natural horizon fractions?

HYPOTHESIS (verbatim from TASKS.md T002):
   the required eps_tot is not special among <=3-factor products of natural horizon fractions.

Method: pre-register the space {1/n*pi, m/n*pi : n in 2..64 powers of 2, m in 1,3};
count products hitting 1/(32*pi) within the kappa measurement window (+-7.8% -> +-15.6% on eps).
PASS: report N_match vs N_expected.   KILL: none (NULL is informative).

Search? YES -- trial count + baseline pre-registered in REGISTRY_FDR.md on 2026-08-17 (row T002).
Direction-of-risk: DEFICIT-risk -- a crowded window (N_match >> 1, consistent with chance)
undermines the "the framework uniquely derived 1/(32*pi)" narrative; a unique hit (N_match==1)
would be the WIN-side. Per R2 we grade the deficit as rigorously as the win.
"""
import sys, os, math
from itertools import combinations_with_replacement
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import check, info, finish, KAPPA_MEAS, KAPPA_ERR

# ---- PART A: pre-stated inputs (provenance: TASKS.md T002 text) ----------------------
TARGET = 1.0 / (32.0 * math.pi)          # eps_tot = 1/(32*pi) = 0.009947
REL_KAPPA = KAPPA_ERR / KAPPA_MEAS        # 0.043/0.551 = 7.8%
HALF = 2.0 * REL_KAPPA                    # +-7.8% on kappa -> +-15.6% on eps (eps ~ kappa^2)
N_MATCH_TARGET = None

# factor space B = {1/(n*pi), 3/(n*pi): n in powers of 2, 2..64}
POWERS = [2 ** k for k in range(1, 7)]    # 2,4,8,16,32,64
MVALS  = [1, 3]
B = [float(m) / (n * math.pi) for n in POWERS for m in MVALS]
assert len(B) == 12, len(B)

# ---- PART B: enumerate <=3-factor multisets (with repetition, order-independent) ------
from itertools import chain
multisets = []
for k in (1, 2, 3):
    multisets += list(combinations_with_replacement(B, k))
n_combos = len(multisets)
# distinct product VALUES (round to kill fp noise; ~1e-12 rel)
vals = sorted({round(math.prod(t), 15) for t in multisets})
n_distinct = len(vals)

# ---- window about the real target -----------------------------------------------------
lo, hi = TARGET * (1.0 - HALF), TARGET * (1.0 + HALF)
def in_window(v):
    return lo <= v <= hi

match_vals = sorted(v for v in vals if in_window(v))
N_match = len(match_vals)
N_match_combos = sum(1 for t in multisets if lo <= math.prod(t) <= hi)

# ---- PART C: chance baseline -- 120 log-spaced pseudo-targets over full product range --
import numpy as np
logmin, logmax = math.log(vals[0]), math.log(vals[-1])
pseudo = [math.exp(logmin + (logmax - logmin) * i / 119.0) for i in range(120)]
counts = []
for p in pseudo:
    plo, phi = p * (1.0 - HALF), p * (1.0 + HALF)
    counts.append(sum(1 for v in vals if plo <= v <= phi))
N_expected = float(np.mean(counts))
N_exp_std  = float(np.std(counts, ddof=1))
frac_any   = sum(1 for c in counts if c >= 1) / len(counts)   # P(a random window is non-empty)

# ---- internal consistency checks ------------------------------------------------------
check(abs((TARGET - 1.0/(32*math.pi))) < 1e-15, "target == 1/(32*pi)")
check(abs(REL_KAPPA - 0.043/0.551) < 1e-9, "kappa rel err == 7.8%")
check(abs(HALF - 0.156) < 5e-3, "eps window ~15.6% (=2x 7.804% kappa rel err, HALF=0.15608)")
check(n_combos == 12 + 78 + 364, f"multiset count 12+78+364=454, got {n_combos}")
check(round(TARGET,15) in {round(v,15) for v in vals}, "1/(32*pi) is itself a 1-factor product (trivial hit present)")

# ---- report ---------------------------------------------------------------------------
print(f"target eps_tot = 1/(32*pi) = {TARGET:.6e}")
print(f"window +-15.6% -> [{lo:.6e}, {hi:.6e}]")
print(f"factor space |B| = {len(B)}; distinct products = {n_distinct}; multisets(<=3) = {n_combos}")
print(f"N_match (distinct values in window) = {N_match}; N_match (combinations) = {N_match_combos}")
for v in match_vals:
    # label the hit
    label = "1/(32*pi) [k=1]" if abs(v - 1/(32*math.pi)) < 1e-12 else \
            "3/(32*pi^2) [k=2]" if abs(v - 3/(32*math.pi**2)) < 1e-12 else \
            "9/(32*pi^3) [k=3]" if abs(v - 9/(32*math.pi**3)) < 1e-12 else f"{v:.6e} [other]"
    info(f"hit {label} = {v:.6e}  (rel { (v/TARGET-1)*100:+.2f}% )")
print(f"N_expected (mean over 120 log-spaced pseudo-targets) = {N_expected:.3f} +/- {N_exp_std:.3f}")
print(f"P(random window non-empty) = {frac_any:.3f};  surplus = N_match - N_expected = {N_match-N_expected:+.3f}")
print(f"VERDICT-GUIDE: N_match={N_match} vs N_expected={N_expected:.2f}; "
      + ("crowded/not-special if N_match>=N_expected" if N_match >= N_expected else
         "sparser than typical -> leans special"))

finish("t002")
