"""FN3 grader (criteria s7, amendment A2): per-galaxy Delta -> per-third medians, slope, labels.

  python3 fn3_grade.py DRYRUN    grades K2' synthetic outputs (fn3_k2p.jsonl) to test the label logic; no real data.
  python3 fn3_grade.py <results.jsonl> <footing> <reading>    Stage 1 (after the owner's yes and the fits).

Labels, first match wins (criteria s7): NOT DECIDABLE (sigma_tot > 0.35 in a third, or < 12 valid fits);
BAND EXCLUDED, TOO LITTLE / TOO MUCH GRAVITY (Z_t > +3 / < -3 in any third); RISE REQUIRED (s/sigma_s > +3);
BAND CONSISTENT (all |Z_t| < 2 and |s/sigma_s| < 2); TENSION otherwise.
kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import sys

import numpy as np
from scipy import stats

import fn3_common as C

NBOOT, SEED = 10000, 20261104


def boot_median(x, rng):
    x = np.asarray(x, float)
    idx = rng.integers(0, len(x), size=(NBOOT, len(x)))
    return float(np.std(np.median(x[idx], axis=1)))


def boot_slope(z, d, rng):
    z, d = np.asarray(z, float), np.asarray(d, float)
    out = np.empty(NBOOT // 10)
    for b in range(len(out)):
        i = rng.integers(0, len(z), len(z))
        out[b] = stats.theilslopes(d[i], z[i])[0]
    return float(np.std(out))


def grade(rows, budget, footing):
    """rows: dicts with z, third, d (Delta), valid (bool)."""
    rng = np.random.default_rng(SEED)
    res = dict(thirds={})
    notdec = False
    Z = []
    for t in range(3):
        d = [r["d"] for r in rows if r["third"] == t and r["valid"]]
        cm = budget["thirds"][str(t)]["footings"][footing]["sigma_cm"]
        if len(d) < 12:
            notdec = True
            res["thirds"][t] = dict(N=len(d), note="fewer than 12 valid fits")
            continue
        med = float(np.median(d))
        sb = boot_median(d, rng)
        st = math.hypot(cm, sb)
        if st > 0.35:
            notdec = True
        z_t = med / st
        Z.append(z_t)
        res["thirds"][t] = dict(N=len(d), median=med, sigma_boot=sb, sigma_cm=cm, sigma_tot=st, Z=z_t)
    zz = [r["z"] for r in rows if r["valid"]]
    dd = [r["d"] for r in rows if r["valid"]]
    s = float(stats.theilslopes(dd, zz)[0])
    ssb = boot_slope(zz, dd, rng)
    sss = budget["slope"][footing]["sigma_s_sys"]
    sig_s = math.hypot(ssb, sss)
    res.update(slope=s, sigma_s_boot=ssb, sigma_s_sys=sss, sigma_s=sig_s, slope_Z=s / sig_s)
    if notdec:
        lab = "NOT DECIDABLE"
    elif any(z > 3 for z in Z):
        lab = "BAND EXCLUDED, TOO LITTLE GRAVITY"
    elif any(z < -3 for z in Z):
        lab = "BAND EXCLUDED, TOO MUCH GRAVITY"
    elif s / sig_s > 3:
        lab = "RISE REQUIRED"
    elif all(abs(z) < 2 for z in Z) and abs(s / sig_s) < 2:
        lab = "BAND CONSISTENT"
    else:
        lab = "TENSION"
    res["label"] = lab
    return res


def fmt(res, tag):
    out = [f"{tag}: {res['label']}"]
    for t, r in res["thirds"].items():
        if "median" in r:
            out.append(f"  third {t}: N {r['N']}, median Delta {r['median']:+.3f}, sigma_boot {r['sigma_boot']:.3f}, "
                       f"sigma_cm {r['sigma_cm']:.3f}, Z {r['Z']:+.2f}")
        else:
            out.append(f"  third {t}: N {r['N']} ({r['note']})")
    out.append(f"  slope {res['slope']:+.3f} per unit z, sigma_s {res['sigma_s']:.3f} (boot {res['sigma_s_boot']:.3f}, "
               f"sys {res['sigma_s_sys']:.3f}), s/sigma_s {res['slope_Z']:+.2f}")
    return out


def main():
    budget = json.load(open(os.path.join(C.HERE, "budget.json")))
    if len(sys.argv) > 1 and sys.argv[1] == "DRYRUN":
        recs = [json.loads(l) for l in open(os.path.join(C.HERE, "fn3_k2p.jsonl"))]
        lines = ["FN3 grader DRYRUN on K2' synthetics (no real data; tests the label logic only)"]
        for scen in ("flat", "rising"):
            rows = [dict(z=r["z"], third=r["third"], d=r["d_fit"], valid=True) for r in recs if r["scen"] == scen]
            for foot in C.A_FOOT:
                lines += fmt(grade(rows, budget, foot), f"{scen} scenario, {foot} budget")
        lines.append("kappa = 1/2 FITTED; not theory closed.")
        print("\n".join(lines))
        open(os.path.join(C.HERE, "fn3_grade_DRYRUN.out"), "w").write("\n".join(lines) + "\n")
        return
    path, foot, reading = sys.argv[1], sys.argv[2], sys.argv[3]
    recs = [json.loads(l) for l in open(path)]
    rows = [dict(z=r["z"], third=r["third"], d=r["d_fit"], valid=r.get("valid", True)) for r in recs if r.get("reading") == reading]
    res = grade(rows, budget, foot)
    print("\n".join(fmt(res, f"{foot} {reading}")))
    return res


if __name__ == "__main__":
    main()
