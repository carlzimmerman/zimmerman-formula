#!/usr/bin/env python3
"""CFG341 -- could an unaccounted per-star velocity-error floor explain the UFD excess?  (frozen c246b01a0)
Run from the repository root; CFG341_MUTATE=1 shuffles sigma_obs across systems (separate outputs)."""
import os, csv, math, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("CFG341_MUTATE", "0") == "1"; SLUG = "cfg341_error_floor" + ("_MUTATE" if MUTATE else "")
G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LOG, CH, OUT = [], [], {"lane": "CFG341", "frozen": "c246b01a0", "mutate": MUTATE, "checks": {}}
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
P(f"CFG341: {len(R)} resolved UFDs + {len(U)} upper limits")


def corr(s, f):
    return math.sqrt(s * s - f * f) if s > f else 0.1


def km_median(x, xu):
    """median with upper limits treated as values at their limits (lower bound on the true median shift: limits only push down)."""
    return float(np.median(np.concatenate([x, xu])))


for foot, a0 in A0.items():
    P(f"\n--- footing {foot} ---")
    fneed = np.array([math.sqrt(max(d["sig"] ** 2 - sig_law(d, a0) ** 2, 0.0)) for d in R])
    P(f"  f_need: median {np.median(fneed):.2f} km/s; <= 1.0 km/s: {np.mean(fneed <= 1.0):.0%}; <= 2.0 km/s: {np.mean(fneed <= 2.0):.0%}")
    OUT[foot] = {"f_need_median": float(np.median(fneed)), "frac_le1": float(np.mean(fneed <= 1.0)), "frac_le2": float(np.mean(fneed <= 2.0))}
    for f in (0.0, 1.0, 2.0):
        x = np.array([math.log10(corr(d["sig"], f) / sig_law(d, a0)) for d in R])
        xu = np.array([math.log10(corr(d["sig"], f) / sig_law(d, a0)) for d in U])
        med = km_median(x, xu)
        bs = [np.median(rng.choice(x, len(x))) for _ in range(4000)]
        err = math.hypot(float(np.std(bs)), 0.077); z = med / err
        mr = float(np.median(x))
        P(f"  hidden floor f = {f:.1f} km/s: median offset (resolved) {mr:+.3f}, with limits {med:+.3f} +- {err:.3f}  ({z:+.2f} sigma)")
        OUT[foot][f"f{f}"] = {"median_resolved": mr, "median_all": med, "err": err, "z": z}

if not MUTATE:
    c1 = OUT["canonical"]["f0.0"]["median_resolved"]
    check("C1 f = 0 reproduces the measured-only median offset +0.354 (canonical) to 0.005 dex", f"{c1:+.4f}", abs(c1 - 0.354) < 0.005)
    ex = all(abs(OUT[f]["f1.0"]["z"]) < 2 for f in A0); ext = all(abs(OUT[f]["f2.0"]["z"]) < 2 for f in A0)
    verdict = "EXPLAINS" if ex else ("ONLY AT EXTREME" if ext else "NOT")
    P(f"\nVERDICT: {verdict}"); OUT["verdict"] = verdict
else:
    real = json.load(open(os.path.join(HERE, "cfg341_error_floor_results.json")))
    a, b = real["canonical"]["f_need_median"], OUT["canonical"]["f_need_median"]
    check("MUTATE shuffled sigma: f_need distribution changes", f"median {a:.2f} -> {b:.2f}", abs(a - b) > 1e-6)
P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
raise SystemExit(0 if all(CH) else 1)
