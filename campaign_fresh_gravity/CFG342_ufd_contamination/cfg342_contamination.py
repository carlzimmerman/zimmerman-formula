#!/usr/bin/env python3
"""CFG342 -- could an unaccounted per-star velocity-error floor explain the UFD excess?  (frozen (see git log))
Run from the repository root; CFG342_MUTATE=1 shuffles sigma_obs across systems (separate outputs)."""
import os, csv, math, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("CFG342_MUTATE", "0") == "1"; SLUG = "cfg342_contamination" + ("_MUTATE" if MUTATE else "")
G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LOG, CH, OUT = [], [], {"lane": "CFG342", "frozen": "(see git log)", "mutate": MUTATE, "checks": {}}
rng = np.random.default_rng(341)


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
    y = max(y, 1e-12); return 1.0 / (1.0 - math.exp(-math.sqrt(y)))


def sig_law(d, a0):
    Mb = 2.0 * d["LV"] + 1.33 * d["MHI"]; r = (4 / 3) * d["rh"] * PC
    gN = G * 0.5 * Mb * MSUN / r ** 2
    return math.sqrt(gN * nu(gN / a0) * r / 3.0) / 1e3


R, U = [], []
for r in csv.DictReader(open(os.path.join(REPO, "real_research/data/dsph/lvd_dwarf_mw.csv"))):
    MV, sig, ul = fnum(r["M_V"]), fnum(r["vlos_sigma"]), fnum(r["vlos_sigma_ul"])
    rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"]); Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
    if MV is None or MV <= -7.7 or rh is None or Dh is None:
        continue
    d = dict(name=r["name"], LV=10 ** (0.4 * (4.83 - MV)), rh=rh, MHI=(10 ** fnum(r["mass_HI"]) if fnum(r["mass_HI"]) is not None else 0.0))
    if sig is not None and ul is None and sig > 0:
        d["sig"] = sig; R.append(d)
    elif ul is not None:
        d["sig"] = ul; U.append(d)
if MUTATE:
    s = rng.permutation([d["sig"] for d in R])
    for d, x in zip(R, s):
        d["sig"] = float(x)
P(f"CFG342: {len(R)} resolved UFDs + {len(U)} upper limits")


def cneed(so, sl, W):
    den = W * W / 3.0 - sl * sl
    return max(so * so - sl * sl, 0.0) / den if den > 0 else float("inf")


check("C1 sigma_obs = sigma_law gives c_need = 0", cneed(2.0, 2.0, 30.0), cneed(2.0, 2.0, 30.0) == 0.0)
so_mix = math.sqrt(0.9 * 2.0 ** 2 + 0.1 * 30.0 ** 2 / 3.0)
check("C2 synthetic mix c = 0.10, W = 30 recovered", f"{cneed(so_mix, 2.0, 30.0):.6f}", abs(cneed(so_mix, 2.0, 30.0) - 0.10) < 1e-9)
for foot, a0 in A0.items():
    P(f"\n--- footing {foot} ---")
    OUT[foot] = {}
    for lab, Wf in (("W=max(3sig,10)", lambda s: max(3 * s, 10.0)), ("W=5sig", lambda s: 5 * s)):
        c = np.array([cneed(d["sig"], sig_law(d, a0), Wf(d["sig"])) for d in R])
        P(f"  {lab:15s}: median c_need {np.median(c):.1%}; UFDs with c_need <= 5%: {np.mean(c <= 0.05):.0%}; <= 15%: {np.mean(c <= 0.15):.0%}")
        OUT[foot][lab] = {"median": float(np.median(c)), "le5": float(np.mean(c <= 0.05)), "le15": float(np.mean(c <= 0.15))}
if not MUTATE:
    m = max(OUT[f]["W=max(3sig,10)"]["median"] for f in A0)
    verdict = "EXPLAINS" if m <= 0.05 else ("PLAUSIBLE" if m <= 0.15 else "NOT")
    P(f"\nVERDICT: {verdict}"); OUT["verdict"] = verdict
else:
    real = json.load(open(os.path.join(HERE, "cfg342_contamination_results.json")))
    a, b = real["canonical"]["W=max(3sig,10)"]["median"], OUT["canonical"]["W=max(3sig,10)"]["median"]
    check("MUTATE shuffled sigma: c_need distribution changes", f"{a:.3f} -> {b:.3f}", abs(a - b) > 1e-6)
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
raise SystemExit(0 if all(CH) else 1)
