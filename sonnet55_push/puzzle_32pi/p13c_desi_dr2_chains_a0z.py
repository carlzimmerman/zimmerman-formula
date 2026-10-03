"""p13c: p13b redone on the DESI DR2 MCMC chains, so the w0-wa correlation is included.
Prediction tested: if rho_DE is the a0 sector's vacuum energy, a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)) (CPL).

DATA (downloaded 2026-10-03 on the owner's explicit yes, ~327 MB, kept OUTSIDE the repo):
  source  https://data.desi.lbl.gov/public/papers/y3/bao-cosmo-params/cobaya/base_w_wa/
          desi-bao-all[_pantheonplus|_union3|_desy5sn]_planck2018-lowl-TT-clik_planck2018-lowl-EE-clik_
          planck-NPIPE-highl-CamSpec-TTTEEE_planck-act-dr6-lensing/chain.{1..4}.txt (+ chain.updated.yaml, chain.margestats)
  local   <parent of repo>/_external_data/desi_dr2_chains/{cmb,pantheonplus,union3,desy5}/ ; sha256 in
          p13c_desi_dr2_chains_SHA256SUMS.txt (copied here). Override the location with DESI_CHAINS=<dir>.
Burn-in: the first 30% of each chain is dropped (the GetDist convention DESI/Planck use); check A below
confirms the weighted w0, wa means and sds reproduce DESI's own chain.margestats (= Table 5) to within 0.01 / 15%.
Run: python3 p13c_desi_dr2_chains_a0z.py     MUTATE=1 -> wa sign flipped before the a0 calculation; checks must fail.
Writes p13c_desi_dr2_chains_a0z.csv (posterior quantiles of a0(z)/a0(0); small; committed).
"""
import os
import re
import sys
from pathlib import Path

import numpy as np

MUTATE = os.environ.get("MUTATE") == "1"
ROOT = Path(os.environ.get("DESI_CHAINS", Path(__file__).resolve().parents[3] / "_external_data" / "desi_dr2_chains"))
FITS = {"cmb": "DESI+CMB", "pantheonplus": "DESI+CMB+Pantheon+", "union3": "DESI+CMB+Union3", "desy5": "DESI+CMB+DESY5"}
BURN = 0.3
ZG = np.round(np.arange(0.0, 5.0001, 0.05), 2)

res = []


def check(name, ok):
    res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + name)


def load(key):
    w, w0, wa = [], [], []
    for i in range(1, 5):
        f = ROOT / key / f"chain.{i}.txt"
        cols = f.open().readline().lstrip("#").split()
        arr = np.loadtxt(f, usecols=[cols.index("weight"), cols.index("w"), cols.index("wa")])
        arr = arr[int(BURN * len(arr)):]
        w.append(arr[:, 0]); w0.append(arr[:, 1]); wa.append(arr[:, 2])
    return np.concatenate(w), np.concatenate(w0), np.concatenate(wa)


def margestats(key, par):
    for line in (ROOT / key / "chain.margestats").open():
        if line.split()[:1] == [par]:
            m = re.match(r"\s*\S+\s+(-?[\d.]+)\s*(?:\\pm\s*([\d.]+)|\^\{\+([\d.]+)\}_\{-([\d.]+)\})", line)
            mu = float(m.group(1))
            sd = float(m.group(2)) if m.group(2) else 0.5 * (float(m.group(3)) + float(m.group(4)))
            return mu, sd


def wq(x, w, q):
    i = np.argsort(x); cw = np.cumsum(w[i]); cw /= cw[-1]
    return np.interp(q, cw, x[i])


def a0r(z, w0, wa):
    return np.sqrt((1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z)))


rows = ["fit,z,q025,q16,q50,q84,q975"]
print(f"{'fit':20s} {'n_eff':>7s} {'corr(w0,wa)':>11s} {'a0(2.5)/a0(0): 16/50/84%':>26s} {'P(a0(2.5)<a0(0))':>16s} {'peak z (median)':>15s} {'peak height':>11s}")
for key, name in FITS.items():
    wt, w0, wa = load(key)
    if MUTATE:
        wa = -wa
    mu0, sd0 = np.average(w0, weights=wt), np.sqrt(np.cov(w0, aweights=wt))
    mua, sda = np.average(wa, weights=wt), np.sqrt(np.cov(wa, aweights=wt))
    (m0, s0), (ma, sa) = margestats(key, "w"), margestats(key, "wa")
    check(f"A {name}: chain w0 {mu0:.3f}+-{sd0:.3f}, wa {mua:.2f}+-{sda:.2f} reproduce DESI margestats (w0 {m0}+-{s0}, wa {ma}+-{sa})",
          abs(mu0 - m0) < 0.01 and abs(mua - ma) < 0.03 and abs(sd0 / s0 - 1) < 0.15 and abs(sda / sa - 1) < 0.15)
    rho = np.cov(w0, wa, aweights=wt)[0, 1] / (sd0 * sda)
    neff = wt.sum() ** 2 / (wt ** 2).sum()
    r25 = a0r(2.5, w0, wa)
    q16, q50, q84 = wq(r25, wt, [0.16, 0.5, 0.84])
    pfall = wt[r25 < 1].sum() / wt.sum()
    curves = a0r(ZG[None, :], w0[:, None], wa[:, None])
    zpk = ZG[np.argmax(curves, axis=1)]
    hpk = curves.max(axis=1)
    zpk50, hpk50 = wq(zpk, wt, 0.5), wq(hpk, wt, 0.5)
    print(f"{name:20s} {neff:7.0f} {rho:11.2f} {q16:8.3f} {q50:7.3f} {q84:7.3f}     {pfall:12.3f}     {zpk50:11.2f}     {hpk50:9.3f}")
    for j, z in enumerate(ZG):
        qs = wq(curves[:, j], wt, [0.025, 0.16, 0.5, 0.84, 0.975])
        rows.append(f"{name},{z:.2f}," + ",".join(f"{v:.4f}" for v in qs))
    check(f"B {name}: w0-wa strongly anticorrelated (rho = {rho:.2f}), so p13b's independent-error envelope was too wide",
          rho < -0.5)
    check(f"C {name}: a0(2.5)/a0(0) = {q50:.3f} (68%: {q16:.3f}-{q84:.3f}); 68% band excludes 'no change': {'YES' if q84 < 1 else 'NO'}",
          q50 < 1)
    check(f"D {name}: P(a0 at z=2.5 is below today) = {pfall:.3f}", pfall > 0.5)

out = Path(__file__).with_name("p13c_desi_dr2_chains_a0z.csv")
if not MUTATE:
    out.write_text("\n".join(rows) + "\n")
n = sum(res)
print(f"\n{n}/{len(res)} checks pass" + ("  [MUTATE=1: failures REQUIRED]" if MUTATE else ""))
sys.exit(0 if n == len(res) else 1)
