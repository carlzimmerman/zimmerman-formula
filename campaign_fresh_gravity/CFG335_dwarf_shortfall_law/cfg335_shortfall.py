#!/usr/bin/env python3
"""CFG335 -- empirical law for the dwarfs' extra-mass requirement under the law (frozen 4167d42db).
Run from the repository root; CFG335_MUTATE=1 shuffles sigma_obs across systems (separate outputs)."""
import os, csv, math, json
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "real_research", "data", "dsph")
MUTATE = os.environ.get("CFG335_MUTATE", "0") == "1"; SLUG = "cfg335_shortfall" + ("_MUTATE" if MUTATE else "")
G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LOG, CH, OUT = [], [], {"lane": "CFG335", "frozen": "4167d42db", "mutate": MUTATE, "checks": {}, "fits": {}}
rng = np.random.default_rng(335)


def P(s=""):
    print(s); LOG.append(s)


def check(n, v, ok):
    CH.append(bool(ok)); OUT["checks"][n] = {"ok": bool(ok), "measured": str(v)}; P(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def nu(y):
    y = max(y, 1e-14); return 1.0 / (1.0 - math.exp(-math.sqrt(y)))


def sig_of_M(M, r, a0):          # M = mass inside r (Msun), r in m -> sigma km/s
    gN = G * M * MSUN / r ** 2; return math.sqrt(gN * nu(gN / a0) * r / 3.0) / 1e3


def M_need(sig, r, a0):
    return brentq(lambda lm: sig_of_M(10 ** lm, r, a0) - sig, -6, 14, xtol=1e-13)


rows = []
for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"), ("lvd_dwarf_local_field.csv", "field")):
    for r in csv.DictReader(open(os.path.join(DATA, fn))):
        MV, sig, ul = fnum(r.get("M_V")), fnum(r.get("vlos_sigma")), fnum(r.get("vlos_sigma_ul"))
        rh = fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))
        if MV is None or rh is None or sig is None or ul is not None or sig <= 0:
            continue
        hi = fnum(r.get("mass_HI")); MHI = 10 ** hi if hi is not None else 0.0
        Mb = 2.0 * 10 ** (0.4 * (4.83 - MV)) + 1.33 * MHI
        rows.append(dict(name=r["name"], host=host, Mb=Mb, rh=rh, sig=sig))
P(f"CFG335: {len(rows)} resolved dwarfs (MW {sum(d['host']=='MW' for d in rows)}, M31 {sum(d['host']=='M31' for d in rows)}, field {sum(d['host']=='field' for d in rows)})")
if MUTATE:
    s = rng.permutation([d["sig"] for d in rows])
    for d, x in zip(rows, s):
        d["sig"] = float(x)

d0 = rows[0]; r0 = (4 / 3) * d0["rh"] * PC
Mn = M_need(d0["sig"], r0, A0["canonical"])
check("C1 invert then re-predict returns sigma_obs to 1e-8", abs(sig_of_M(10 ** Mn, r0, A0["canonical"]) - d0["sig"]), abs(sig_of_M(10 ** Mn, r0, A0["canonical"]) - d0["sig"]) < 1e-8)
sp = sig_of_M(d0["Mb"] / 2, r0, A0["canonical"]); Mz = M_need(sp, r0, A0["canonical"])
check("C2 sigma_obs = law prediction gives Delta M = 0 to 1e-8 (relative)", abs(10 ** Mz / (d0["Mb"] / 2) - 1), abs(10 ** Mz / (d0["Mb"] / 2) - 1) < 1e-8)


def fit(x, y):
    A = np.vstack([x, np.ones_like(x)]).T; c, *_ = np.linalg.lstsq(A, y, rcond=None); res = y - A @ c
    bs = []
    for _ in range(2000):
        i = rng.integers(0, len(x), len(x)); cc, *_ = np.linalg.lstsq(A[i], y[i], rcond=None); bs.append(cc[0])
    return float(c[0]), float(np.std(bs)), float(c[1]), float(np.std(res, ddof=2))


for foot, a0 in A0.items():
    P(f"\n--- footing {foot} ---")
    for d in rows:
        r = (4 / 3) * d["rh"] * PC; d["Mneed"] = 10 ** M_need(d["sig"], r, a0); d["dM"] = d["Mneed"] - d["Mb"] / 2
    pos = [d for d in rows if d["dM"] > 0]; neg = [d for d in rows if d["dM"] <= 0]
    P(f"  shortfall > 0: {len(pos)}; law already sufficient (Delta M <= 0): {len(neg)}")
    lM = np.log10([d["Mb"] for d in pos]); lr = np.log10([d["rh"] for d in pos]); ldM = np.log10([d["dM"] for d in pos])
    F = {}
    F["F1 logdM vs logMb"] = fit(lM, ldM); F["F2 logdM vs logrh"] = fit(lr, ldM)
    F["F3 constant dM"] = (0.0, 0.0, float(ldM.mean()), float(ldM.std(ddof=1)))
    F["F4 log(dM/Mb) vs logMb"] = fit(lM, ldM - lM)
    for k, (s, es, c, sc) in F.items():
        P(f"  {k:24s}: slope {s:+.3f} +- {es:.3f}  intercept {c:+.3f}  scatter {sc:.3f} dex")
    host = {}
    for h in ("MW", "M31", "field"):
        sub = [d for d in pos if d["host"] == h]
        if len(sub) >= 5:
            host[h] = fit(np.log10([d["Mb"] for d in sub]), np.log10([d["dM"] for d in sub]))
            P(f"    F1 host {h:5s} (N={len(sub)}): slope {host[h][0]:+.3f} +- {host[h][1]:.3f} intercept {host[h][2]:+.3f} scatter {host[h][3]:.3f}")
    best = min(F, key=lambda k: F[k][3]); sc3 = F["F3 constant dM"][3]
    lawlike = {}
    for k in ("F1 logdM vs logMb", "F2 logdM vs logrh", "F4 log(dM/Mb) vs logMb"):
        s, es, c, sc = F[k]
        slopes = [v for v in host.values()]
        hostok = all(abs(v[0] - s) < 2 * math.hypot(v[1], es) for v in slopes) if slopes else False
        lawlike[k] = bool(sc <= 0.25 and (sc3 - sc >= 0.05 or sc3 <= 0.25) and hostok)
    lawlike["F3 constant dM"] = bool(sc3 <= 0.25)
    OUT["fits"][foot] = {"F": F, "host_F1": host, "lawlike": lawlike, "n_pos": len(pos), "n_neg": len(neg),
                         "neg_names": [d["name"] for d in neg], "median_logdM": float(np.median(ldM))}
    P(f"  law-like: {lawlike}")

if MUTATE:
    import json as _j
    real = _j.load(open(os.path.join(HERE, "cfg335_shortfall_results.json")))
    a = real["fits"]["canonical"]["F"]["F1 logdM vs logMb"][3]; b = OUT["fits"]["canonical"]["F"]["F1 logdM vs logMb"][3]
    check("MUTATE shuffled sigma: F1 scatter grows", f"{a:.3f} -> {b:.3f}", b > a)
else:
    ll = [k for k in OUT["fits"]["canonical"]["lawlike"] if OUT["fits"]["canonical"]["lawlike"][k] and OUT["fits"]["alt"]["lawlike"][k]]
    verdict = ("LAW-LIKE: " + ", ".join(ll)) if ll else "NO SIMPLE LAW"
    P(f"\nVERDICT: {verdict}"); OUT["verdict"] = verdict
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
raise SystemExit(0 if all(CH) else 1)
