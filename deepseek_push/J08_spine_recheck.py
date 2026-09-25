#!/usr/bin/env python3
"""
J08 -- THE CHI2_1 SPINE: RECORD-CLOSING LIVE RE-CHECK (n = 2e6, ONE CLOUD)
2026-09-25.  Closes K01 finding F6 ("J08 -- ABSENT") by recording the spine
under its own identity.  This script performs the SINGLE allowed live leg:
the W KS table in 8 D-bins for one cloud (central, q=0).  The atom-mass and
hierarchy legs are NOT recomputed -- they exist in J09_two_component_law.out
(27/27, n = 6e5) and are traced, not re-run.

DEFINITION (the spine, verbatim from J09_two_component_law.py docstring):
  W := v^2/(2 ang) | (D, ang) ~ chi2_1
  -- W is INDEPENDENT of the whole path geometry (D, ang).

Check: in EVERY narrow D-bin of the continuous part (ang > 0), the KS
statistic of W against the chi2_1 CDF is <= 0.002 (the threshold J09c cites
for J08), with the p-value reported per bin.
"""
import json
import math
import sys

import numpy as np

sys.path.insert(0, "deepseek_push")
from J02_moment_hierarchy import simulate

N = 2_000_000
NBINS = 8


def chi2_1_cdf(x):
    # chi2_1 = Z^2, Z ~ N(0,1):  P(Z^2 <= x) = erf(sqrt(x/2)) for x >= 0
    x = np.maximum(x, 0.0)
    sq = np.sqrt(x / 2.0).ravel()
    out = np.empty(sq.shape, dtype=float)
    for i, v in enumerate(sq):
        out[i] = math.erf(v)
    return out.reshape(x.shape)


def ks_stat(w, cdf_fn=chi2_1_cdf):
    w = np.sort(w)
    n = len(w)
    c = cdf_fn(w)
    dplus = float(np.max((np.arange(1, n + 1)) / n - c)) if n else 0.0
    dminus = float(np.max(c - (np.arange(n)) / n)) if n else 0.0
    return max(dplus, dminus, 0.0)


def ks_pvalue(d, n):
    # Kolmogorov asymptotic: p = Q_KS((sqrt(n)+0.12+0.11/sqrt(n)) * d)
    lam = (math.sqrt(n) + 0.12 + 0.11 / math.sqrt(n)) * d
    lam = max(lam, 1e-12)
    s = 0.0
    j = 1
    while True:
        term = math.exp(-2.0 * j * j * lam * lam)
        s += ((-1.0) ** (j - 1)) * term
        if term < 1e-12 * s or j > 20000:
            break
        j += 1
    return min(1.0, max(0.0, 2.0 * s))


def run():
    seed = 20260925
    print(f"J08 spine live re-check: n={N}, central, tau0=1.0, q=0, seed={seed}")
    r = simulate(N, 1.0, 0.0, "central", seed=seed)
    D, v2, ang = r["D"], r["v2"], r["ang"]

    cont = ang > 0
    Dc, v2c, angc = D[cont], v2[cont], ang[cont]
    W = v2c / (2.0 * angc)

    A = float(np.mean(r["N"] == 0))
    predA = math.exp(-1.0 * (1.0 + 0.0 / 3.0))  # exp(-tau0 (1+q/3)), tau0=1, q=0
    overall = dict(n_cont=int(cont.sum()), n_atom=int((~cont).sum()),
                   A=A, pred_A=predA, resid_A=A - predA)

    # 8 D-bins from the CONTINUOUS part only (the atom spike must not absorb a
    # bin -- same convention as J09's B-check).
    pcts = [100.0 * k / NBINS for k in range(1, NBINS)]
    edges = np.concatenate([[0.0], np.percentile(Dc, pcts), [np.inf]])
    bins = []
    for k in range(NBINS):
        msk = (Dc >= edges[k]) & (Dc < edges[k + 1])
        w = W[msk]
        if len(w) == 0:
            bins.append(dict(bin=k, lo=float(edges[k]), hi=float(edges[k + 1]),
                             n=0, ks=None, p=None, mean_W=None))
            continue
        d = ks_stat(w)
        bins.append(dict(
            bin=k, lo=float(edges[k]), hi=float(edges[k + 1]),
            n=int(len(w)), ks=round(d, 6), p=round(ks_pvalue(d, len(w)), 6),
            mean_W=round(float(np.mean(w)), 4)))
    # overall continuous-part KS as a sanity row
    d_all = ks_stat(W)
    overall["ks"] = round(d_all, 6)
    overall["p"] = round(ks_pvalue(d_all, len(W)), 6)
    overall["mean_W"] = round(float(np.mean(W)), 4)
    overall["se_W"] = round(float(np.std(W, ddof=1) / np.sqrt(len(W))), 4)

    passed_bins = all((b["ks"] is not None and b["ks"] <= 0.002) for b in bins)
    verdict = "PASS" if passed_bins else "FAIL"
    for b in bins:
        flag = "PASS" if (b["ks"] is not None and b["ks"] <= 0.002) else "FAIL"
        print(f"  bin {b['bin']}: D in [{b['lo']:.4f}, {b['hi']:.4f})  n={b['n']}  "
              f"KS={b['ks']}  p={b['p']}  meanW={b['mean_W']}  [{flag}]")
    print(f"overall (cont part): KS={overall['ks']}  p={overall['p']}  "
          f"meanW={overall['mean_W']} +/- {overall['se_W']}  A={A:.6f} vs {predA:.6f} "
          f"(resid {A - predA:+.3e})")
    print(f"J08 SPINE RE-CHECK: {verdict} ({sum(1 for b in bins if b['ks'] is not None and b['ks'] <= 0.002)}/{NBINS} bins <= 0.002)")
    return 0 if passed_bins else 1


if __name__ == "__main__":
    sys.exit(run())