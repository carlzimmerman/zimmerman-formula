#!/usr/bin/env python3
"""ENSEMBLE_ATTRACTION.py -- the population test: is the vocabulary ATTRACTED to real SM
constants, or merely dense everywhere?

WHY THIS IS A DIFFERENT QUESTION. Every point test is dead. Retrodiction dies on the depth
ceiling (all PMNS D_max negative). Pre-registration dies on candidate density (15,000-26,000
reachable values per angle window, so the vocabulary predicts everything). Both failures share a
cause: they ask "can SOME expression hit THIS constant?", and in a dense set the answer is always
yes and never informative.

The population question is not about any expression. It asks whether the reachable SET is
structured with respect to real physics:

    do measured SM constants sit in DENSER regions of the value distribution than
    magnitude-matched RANDOM numbers do?

That is ONE hypothesis with ONE statistic. It does not care which formula lands where, so
density does not defeat it -- density is the null it is measured against. If the vocabulary is
merely dense, real constants and fake ones sit in equally dense regions and the test returns
nothing. If the germs encode something physical, real constants sit anomalously dense.

THE CONTROL IS THE WHOLE POINT, and it is what an earlier measurement of mine lacked. Reporting
"targets sit at 1.2x local density, 81st percentile" against a GLOBAL-UNIFORM null is close to
meaningless, because the value set spans 632 decades of ln|v| and is wildly non-uniform. The
correct null is MAGNITUDE-MATCHED: fake targets drawn to reproduce the real targets' own
distribution of |log10 value|, so the only thing that differs is whether the number is a real
measured constant.

PRE-REGISTERED DESIGN (fixed before running):
  * statistic: for each target t, rho(t) = number of distinct values within a fixed relative
    band of t (band = 1e-3 relative, chosen because it is far wider than any measurement window
    -- so the statistic is about the vocabulary's structure, NOT about matching);
    T = mean over the 19 fittable targets of log10 rho(t).
  * null: K = 2000 fake target sets, each of 19 numbers, drawn log-uniformly to match the real
    targets' log10-magnitude range; T computed identically.
  * p = fraction of null draws with T_null >= T_real. One-sided, because the hypothesis is
    ENRICHMENT.
  * verdict threshold: p < 0.05 is a signal worth pursuing; p >= 0.05 closes the population
    route as well. Stated before the number is seen.

WHAT A POSITIVE WOULD AND WOULD NOT MEAN. It would NOT produce a formula or derive a constant.
It would say the germ vocabulary is non-generically related to SM constants as a population,
which is a real and publishable structural claim and would justify further work. A negative
closes the last route the search programme has: the vocabulary would be indistinguishable from
random numbers of the same size.

Local-only. Exit 0 = ran. No hard-coded verdicts; outcome accepted either way.
"""
from __future__ import annotations
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

VALS_F64 = os.path.join(HERE, "results_grind", "depth_10", "values.f64")
OUT = os.path.join(HERE, "results_interlock", "ENSEMBLE_ATTRACTION.json")

BAND = 1e-3        # relative half-width of the density band (>> any measurement window)
K_NULL = 2000      # null draws
SEED = 20260729
ALPHA = 0.05       # pre-declared significance threshold

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")
    return cond

def banner(s):
    print("\n" + "=" * 98); print(s); print("=" * 98)


def local_density(sorted_vals, centres, band=BAND):
    """count of values within +/- band*|c| of each centre, via binary search."""
    c = np.asarray(centres, dtype=np.float64)
    lo = np.searchsorted(sorted_vals, c * (1.0 - band), side="left")
    hi = np.searchsorted(sorted_vals, c * (1.0 + band), side="right")
    return (hi - lo).astype(np.float64)


def main() -> int:
    banner("ENSEMBLE_ATTRACTION -- population test, magnitude-matched control")

    if not os.path.exists(VALS_F64):
        print(f"  ERROR: value array missing at {VALS_F64}")
        return 2

    from targets import pdg_constants as pdg
    import exhaust_parallel as EP
    ds = pdg.load()
    keys = [k for k in EP.sm_target_keys(include_holdout=False)]
    reals = np.array([float(ds[k].value) for k in keys], dtype=np.float64)
    check(len(keys) == 19, f"19 fittable targets, holdout excluded (got {len(keys)})")

    v = np.fromfile(VALS_F64, dtype=np.float64)
    v = v[np.isfinite(v) & (v > 0)]
    v.sort()
    print(f"  value set: {v.size:,} finite positive distinct values")
    print(f"  log10 range: [{math.log10(v[0]):.1f}, {math.log10(v[-1]):.1f}]  "
          f"({math.log10(v[-1]) - math.log10(v[0]):.0f} decades)")
    print(f"  band = +/-{BAND:.0e} relative (far wider than any measurement window, so this")
    print(f"  measures VOCABULARY STRUCTURE, not matching)")

    # -----------------------------------------------------------------------------------
    banner("S1. Real targets: local density")
    rho_real = local_density(v, reals)
    print(f"  {'target':<18}{'value':>16}{'log10':>9}{'rho in band':>13}")
    print("  " + "-" * 58)
    for k, val, r in zip(keys, reals, rho_real):
        print(f"  {k:<18}{val:>16.6g}{math.log10(abs(val)):>9.2f}{int(r):>13,}")
    # statistic: mean of log10(rho+1) -- +1 so zeros are admissible
    T_real = float(np.mean(np.log10(rho_real + 1.0)))
    print(f"\n  statistic T_real = mean log10(rho+1) = {T_real:.6f}")
    print(f"  (geometric-mean density ~ {10**T_real - 1:.1f} values per band)")

    # -----------------------------------------------------------------------------------
    banner("S2. Magnitude-matched null")
    lg = np.log10(np.abs(reals))
    lo_lg, hi_lg = lg.min(), lg.max()
    print(f"  real targets span log10 in [{lo_lg:.3f}, {hi_lg:.3f}]")
    print(f"  drawing {K_NULL:,} fake sets of {len(keys)} numbers, log-uniform in that range")
    rng = np.random.default_rng(SEED)
    T_null = np.empty(K_NULL, dtype=np.float64)
    for i in range(K_NULL):
        fake = 10.0 ** rng.uniform(lo_lg, hi_lg, size=len(keys))
        T_null[i] = np.mean(np.log10(local_density(v, fake) + 1.0))
    print(f"  T_null: mean {T_null.mean():.6f}  sd {T_null.std():.6f}  "
          f"min {T_null.min():.4f}  max {T_null.max():.4f}")

    p = float((T_null >= T_real).mean())
    z = float((T_real - T_null.mean()) / T_null.std()) if T_null.std() > 0 else float("nan")
    print(f"\n  T_real = {T_real:.6f}")
    print(f"  p(one-sided, T_null >= T_real) = {p:.4f}")
    print(f"  z = {z:+.2f}")

    # -----------------------------------------------------------------------------------
    banner("S3. Robustness: does the answer depend on the band?")
    print(f"  {'band':>10}{'T_real':>11}{'T_null mean':>13}{'z':>8}{'p':>9}")
    print("  " + "-" * 52)
    rob = {}
    for b in (1e-4, 1e-3, 1e-2, 1e-1):
        tr = float(np.mean(np.log10(local_density(v, reals, b) + 1.0)))
        tn = np.empty(400)
        rng2 = np.random.default_rng(SEED + 1)
        for i in range(400):
            fake = 10.0 ** rng2.uniform(lo_lg, hi_lg, size=len(keys))
            tn[i] = np.mean(np.log10(local_density(v, fake, b) + 1.0))
        pz = float((tn >= tr).mean())
        zz = float((tr - tn.mean()) / tn.std()) if tn.std() > 0 else float("nan")
        rob[f"{b:.0e}"] = dict(T_real=tr, T_null_mean=float(tn.mean()), z=zz, p=pz)
        print(f"  {b:>10.0e}{tr:>11.4f}{tn.mean():>13.4f}{zz:>+8.2f}{pz:>9.4f}")

    # -----------------------------------------------------------------------------------
    banner("VERDICT")
    signal = p < ALPHA
    consistent = all(r["p"] < ALPHA for r in rob.values()) or all(r["p"] >= ALPHA for r in rob.values())
    print(f"  pre-declared threshold: p < {ALPHA}")
    if signal:
        print(f"  p = {p:.4f} < {ALPHA}: the SM constants sit in ANOMALOUSLY DENSE regions of")
        print("  this vocabulary's reachable set, relative to magnitude-matched random numbers.")
        print("  READ THIS CAREFULLY: it does NOT derive any constant and produces no formula.")
        print("  It says the germ vocabulary is non-generically related to SM constants AS A")
        print("  POPULATION -- a structural claim, worth pursuing, and the first positive")
        print("  result this programme has produced.")
        print(f"  Band robustness: {'CONSISTENT across all bands' if consistent else 'BAND-DEPENDENT -- treat with suspicion'}")
    else:
        print(f"  p = {p:.4f} >= {ALPHA}: NO enrichment. Real SM constants sit in regions no")
        print("  denser than magnitude-matched random numbers do.")
        print("  This closes the POPULATION route as well, and it is the last route the search")
        print("  programme had. The vocabulary is statistically indistinguishable from random")
        print("  numbers of the same size, with respect to real physics constants.")
        print(f"  Band robustness: {'CONSISTENT across all bands' if consistent else 'band-dependent'}")
    print("\n  Note the earlier '1.2x enrichment, 81st percentile' figure was measured against a")
    print("  GLOBAL-UNIFORM null over a set spanning 632 decades, which is not a valid control.")
    print("  The magnitude-matched null above supersedes it.")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(dict(T_real=T_real, p=p, z=z, band=BAND, k_null=K_NULL,
                   n_values=int(v.size), targets=keys, robustness=rob,
                   signal=bool(signal), alpha=ALPHA), open(OUT, "w"), indent=1)
    print(f"\n  wrote {OUT}")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
