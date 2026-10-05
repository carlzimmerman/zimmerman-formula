#!/usr/bin/env python3
"""CFG334 -- can unresolved binaries inflate Pal 3's single-epoch dispersion from Newton's 0.75 km/s to the measured 1.70?
Frozen: FROZEN_CRITERIA.md (f75660a81).  Run from the repository root; CFG334_MUTATE=1 sets f = 0 (separate outputs)."""
import os, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG334_MUTATE", "0") == "1"
SLUG = "cfg334_pal3_binaries" + ("_MUTATE" if MUTATE else "")
G = 6.674e-11; MSUN = 1.989e30; RSUN = 6.957e8; DAY = 86400.0; PC = 3.0857e16
N, SOBS, NDRAW, M1 = 22, 1.70, 20000, 0.8
rng = np.random.default_rng(334)
OUT, LOG, CH = {"lane": "CFG334", "frozen": "f75660a81", "mutate": MUTATE, "configs": {}, "checks": {}}, [], []


def P(s=""):
    print(s); LOG.append(s)


def check(name, val, ok):
    CH.append(bool(ok)); OUT["checks"][name] = {"ok": bool(ok), "measured": str(val)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def ml_sigma(v, e):
    """deconvolved Gaussian ML dispersion with known errors (rows = draws)."""
    s2 = np.maximum(v.var(axis=1) - (e ** 2).mean(axis=1), 1e-4)
    for _ in range(200):
        w = 1.0 / (s2[:, None] + e ** 2)
        mu = (w * v).sum(1) / w.sum(1)
        s2 = np.maximum(((w ** 2) * ((v - mu[:, None]) ** 2 - e ** 2)).sum(1) / (w ** 2).sum(1), 1e-4)
    return np.sqrt(s2)


def kepler_E(M, e):
    E = M.copy()
    for _ in range(40):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E


def binary_vlos(n):
    """line-of-sight velocity offset (km/s) of the luminous primary for n binaries (DM91 periods, flat q, thermal e)."""
    out = np.empty(n); filled = 0
    while filled < n:
        m = 4 * (n - filled) + 100
        logP = rng.normal(4.8, 2.3, m); Pd = 10 ** logP
        q = rng.uniform(0.1, 1.0, m); ecc = np.sqrt(rng.uniform(0, 1, m))
        Mt = M1 * (1 + q) * MSUN
        a = (G * Mt * (Pd * DAY) ** 2 / (4 * math.pi ** 2)) ** (1 / 3)
        ok = (a * (1 - ecc) >= 3 * 10 * RSUN) & (a < 0.1 * PC)
        Pd, q, ecc, a, Mt = Pd[ok], q[ok], ecc[ok], a[ok], Mt[ok]
        k = len(Pd)
        inc = np.arccos(rng.uniform(-1, 1, k)); om = rng.uniform(0, 2 * math.pi, k); Mn = rng.uniform(0, 2 * math.pi, k)
        E = kepler_E(Mn, ecc); nu = 2 * np.arctan2(np.sqrt(1 + ecc) * np.sin(E / 2), np.sqrt(1 - ecc) * np.cos(E / 2))
        K = (2 * math.pi * a / (Pd * DAY)) * (q / (1 + q)) * np.sin(inc) / np.sqrt(1 - ecc ** 2)
        v = K * (np.cos(nu + om) + ecc * np.cos(om)) / 1e3
        take = min(k, n - filled); out[filled:filled + take] = v[:take]; filled += take
    return out


def simulate(sint, e, f):
    v = rng.normal(0, sint, (NDRAW, N))
    isb = rng.uniform(0, 1, (NDRAW, N)) < f
    nb = int(isb.sum())
    if nb:
        v[isb] += binary_vlos(nb)
    err = np.full((NDRAW, N), e)
    if e > 0:
        v = v + rng.normal(0, 1, (NDRAW, N)) * e
    s = ml_sigma(v, np.maximum(err, 1e-6)) if e > 0 else v.std(axis=1, ddof=1)
    return s


P("CFG334: Pal 3 single-epoch binary inflation (N = 22, measured 1.70 km/s)")
P("\nControls")
s = simulate(0.75, 0.0, 0.0); check("C1 f=0, e=0 recovers sigma_int to 3%", f"median {np.median(s):.3f} vs 0.75", abs(np.median(s) / 0.75 - 1) < 0.03)
s = simulate(0.75, 1.0, 0.0); check("C2 f=0, e=1.0: ML deconvolution unbiased to 5% (median)", f"median {np.median(s):.3f} vs 0.75", abs(np.median(s) / 0.75 - 1) < 0.05)
a = (G * 1.6 * MSUN * (365.25 * DAY) ** 2 / (4 * math.pi ** 2)) ** (1 / 3); K = 2 * math.pi * a / (365.25 * DAY) * 0.5 / 1e3
check("C3 circular P=1 yr, q=1, M1=0.8: K = 15.6 km/s x sin i (analytic)", f"K = {K:.2f} km/s", abs(K - 15.6) < 0.3)

P("\nConfigurations: P(sigma_obs >= 1.70) and median sigma_obs")
fs = (0.0,) if MUTATE else (0.1, 0.3, 0.5)
for sint in (0.65, 0.75, 0.85):
    for e in (0.5, 1.0, 1.5):
        for f in fs:
            s = simulate(sint, e, f)
            p = float((s >= SOBS).mean()); med = float(np.median(s))
            key = f"sint{sint}_e{e}_f{f}"; OUT["configs"][key] = {"P": p, "median": med}
            P(f"  sigma_int {sint:.2f}  e {e:.1f}  f {f:.1f}:  P = {p:.4f}   median sigma_obs = {med:.3f}")

if MUTATE:
    p0 = OUT["configs"]["sint0.75_e1.0_f0.0"]["P"]
    check("MUTATE f=0: P at the primary falls far below the binary case (< 0.01)", f"P = {p0:.4f}", p0 < 0.01)
else:
    prim = OUT["configs"]["sint0.75_e1.0_f0.3"]["P"]
    any05 = any(v["P"] >= 0.05 for k, v in OUT["configs"].items())
    hi = any(v["P"] >= 0.05 for k, v in OUT["configs"].items() if k.endswith("f0.5") or "_e1.5_" in k)
    verdict = "BINARIES EXPLAIN" if prim >= 0.05 else ("PLAUSIBLE" if hi else "NOT")
    P(f"\nPrimary (sigma_int 0.75, e 1.0, f 0.3): P = {prim:.4f}\nVERDICT: {verdict}")
    OUT["verdict"] = verdict; OUT["primary_P"] = prim
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
raise SystemExit(0 if all(CH) else 1)
