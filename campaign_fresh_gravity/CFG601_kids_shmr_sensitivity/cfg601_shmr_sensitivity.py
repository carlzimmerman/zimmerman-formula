#!/usr/bin/env python3
"""CFG601 (FROZEN_CRITERIA.md, committed alone first): KiDS verdict sensitivity to the SHMR (swap / scale / remove).
Machinery: ../CFG600_native_catchment_kids/cfg600_common.py (CFG531 harness, read-only).
Run: nice -n 10 python3 cfg601_shmr_sensitivity.py   (about 1 min with the cached CFG531 tables)"""
import os, sys, json, math
import numpy as np
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "CFG600_native_catchment_kids"))
import cfg600_common as K

LOG, CHK = [], {}
RES = {"lane": "CFG601", "script": "cfg601_shmr_sensitivity", "criteria": "FROZEN_CRITERIA.md",
       "settings": "kappa = 1/2 FITTED; footings never pooled; nu_mono; cold energy mass required; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(n, ok, msg):
    CHK[n] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {n}: {msg}")


def eps2(d, Cv, cp, idx, shmr, delta):
    """GLS amplitude of the own profile in bins idx; model of one SHMR; delta = rank-one SHMR term (or none)."""
    idx = np.asarray(idx)
    Em, om = cp["moster"]; Eb, ob = cp["behroozi"]
    mM, mB = Em + om, Eb + ob
    m, o = (mM, om) if shmr == "moster" else (mB, ob)
    dl = (mB - mM) if delta else np.zeros_like(mM)
    Ct = Cv[np.ix_(idx, idx)] / K.hart(len(idx)) + np.outer(dl[idx], dl[idx])
    W = np.linalg.inv(Ct); r = d[idx] - m[idx]
    F = float(o[idx] @ W @ o[idx]); e = float(o[idx] @ W @ r) / F
    return dict(eps=e, sig=F ** -0.5, Z=e * F ** 0.5, wvec=(W @ o[idx] / F).tolist())


def chi15(d, Cv, cp, shmr, delta):
    Em, om = cp["moster"]; Eb, ob = cp["behroozi"]
    mM, mB = Em + om, Eb + ob
    m = mM if shmr == "moster" else mB
    dl = (mB - mM) if delta else np.zeros_like(mM)
    Ct = Cv / K.hart(15) + np.outer(dl, dl)
    r = d - m; c2 = float(r @ np.linalg.solve(Ct, r))
    return c2, float(stats.chi2.sf(c2, 15))


F30 = K.F30
CL = {"all": F30, "early": F30 & K.EARLY, "late": F30 & ~K.EARLY}
DATA = {cls: K.esd_loo(mk) for cls, mk in CL.items()}
MEAS = K.MEAS["f30"]
scale = lambda k: {s: np.clip(k * MEAS[s], 0, 1) for s in K.SHMRS}
zero = {s: np.zeros_like(MEAS[s]) for s in K.SHMRS}
VARIANTS = {   # name -> (fE, fO, shmr, delta)
    "S0 base": (MEAS, MEAS, "moster", True),
    "S1 moster alone": (MEAS, MEAS, "moster", False),
    "S1 behroozi alone": (MEAS, MEAS, "behroozi", False),
    "S2 leak x0.5": (scale(0.5), scale(0.5), "moster", True),
    "S2 leak x1.5": (scale(1.5), scale(1.5), "moster", True),
    "S3 removed (bound)": (zero, zero, "moster", False),
    "MU1 leak x3": (scale(3.0), scale(3.0), "moster", True),
}
OUT = {}
for c in K.CONS:
    for foot in K.FOOTS:
        for vn, (fE, fO, shmr, delta) in VARIANTS.items():
            row = {}
            for cls, mk in CL.items():
                d, Cv, L = DATA[cls]
                Eg = K.Egrid(c, mk, fE, f"{vn}|{cls}")
                cp = K.cp_census(c, foot, mk, fE, fO, Eg)
                bands = {b: eps2(d, Cv, cp, ix, shmr, delta) for b, ix in K.BANDS.items()}
                mM = (cp["moster"][0] + cp["moster"][1]) if shmr == "moster" else (cp["behroozi"][0] + cp["behroozi"][1])
                loo = {b: ((L[:, ix] - mM[ix][None, :]) @ np.array(bands[b]["wvec"])).tolist() for b, ix in K.BANDS.items()}
                row[cls] = dict(bands={b: {k: v for k, v in x.items() if k != "wvec"} for b, x in bands.items()}, loo=loo)
                if cls == "all":
                    row["chi2_15"], row["p_15"] = chi15(d, Cv, cp, shmr, delta)
            # early-late K9 and CARRIED label (CFG531 rule)
            dv = np.array(row["early"]["loo"]["K9"]) - np.array(row["late"]["loo"]["K9"])
            vj = (K.NPATCH - 1) / K.NPATCH * np.sum((dv - dv.mean()) ** 2)
            vq = row["early"]["bands"]["K9"]["sig"] ** 2 + row["late"]["bands"]["K9"]["sig"] ** 2
            df = row["early"]["bands"]["K9"]["eps"] - row["late"]["bands"]["K9"]["eps"]
            ze, zl = row["early"]["bands"]["K9"]["Z"], row["late"]["bands"]["K9"]["Z"]
            car = ("CARRIED BY EARLY TYPES" if ze >= 3 and abs(zl) < 2 else "CARRIED BY LATE TYPES" if zl >= 3 and abs(ze) < 2
                   else "BOTH" if ze >= 2 and zl >= 2 else "MIXED/UNRESOLVED")
            row["split"] = dict(diff=df, sig=math.sqrt(max(vj, vq)), Z=df / math.sqrt(max(vj, vq)), carried=car)
            OUT[f"{c}|{foot}|{vn}"] = row
            a = row["all"]["bands"]
            P(f"[{c} {foot:9s}] {vn:20s} K-in {a['K-in']['eps']:+.3f}+-{a['K-in']['sig']:.3f} | K9 {a['K9']['eps']:+.3f}+-{a['K9']['sig']:.3f} (Z {a['K9']['Z']:+.1f}) | "
              f"census chi2 {row['chi2_15']:.1f} (p {row['p_15']:.1e}) | early-late {df:+.2f} (Z {row['split']['Z']:+.1f}) {car}")
RES["cells"] = {k: dict(chi2_15=v["chi2_15"], p_15=v["p_15"], split=v["split"], **{cl: v[cl]["bands"] for cl in CL}) for k, v in OUT.items()}

# ---------------------------------------------------------------- verdict (S1 and S2 only)
J531 = json.load(open(os.path.join(K.LANES, "CFG531_inner_halo_shortfall", "cfg531_kids_results.json")))
VER = {}
for foot in K.FOOTS:
    changed = []
    for c in K.CONS:
        b = OUT[f"{c}|{foot}|S0 base"]
        for vn in ("S1 moster alone", "S1 behroozi alone", "S2 leak x0.5", "S2 leak x1.5"):
            o = OUT[f"{c}|{foot}|{vn}"]
            if (o["all"]["bands"]["K9"]["Z"] >= 3) != (b["all"]["bands"]["K9"]["Z"] >= 3) or o["split"]["carried"] != b["split"]["carried"]:
                changed.append(f"{c}:{vn}")
    VER[foot] = "ROBUST TO THE SHMR" if not changed else "SENSITIVE (" + ", ".join(changed) + ")"
    rng = {q: [OUT[f"{c}|{foot}|{vn}"]["all"]["bands"]["K9"][q] for c in K.CONS for vn in ("S0 base", "S1 moster alone", "S1 behroozi alone", "S2 leak x0.5", "S2 leak x1.5")]
           for q in ("eps", "Z")}
    P(f"  VERDICT {foot}: {VER[foot]}; K9 eps over S0/S1/S2: {min(rng['eps']):+.3f} .. {max(rng['eps']):+.3f}; Z {min(rng['Z']):+.1f} .. {max(rng['Z']):+.1f}")
RES["verdict"] = VER

# CFG536 swap, from committed JSON only (not re-run)
J536 = json.load(open(os.path.join(K.LANES, "CFG536_kids_history_weighting_heldout", "cfg536_heldout_results.json")))
sw = {cell: dict(d_eps=v["K9"]["eps"], sig=v["K9"]["sig"], Z_moster=v["K9"]["Z"], Z_behroozi=v["K9"]["Z_behroozi"]) for cell, v in J536["heldout"]["frozen"].items()}
RES["cfg536_swap_from_json"] = sw
for k, v in sw.items():
    P(f"  CFG536 held-out early-late K9 {k}: d_eps {v['d_eps']:+.2f}+-{v['sig']:.2f}; Z moster {v['Z_moster']:+.2f} | Z behroozi {v['Z_behroozi']:+.2f} (committed JSON, not re-run)")

# ---------------------------------------------------------------- controls
k1 = max(abs(OUT[f"{c}|{foot}|S0 base"]["all"]["bands"]["K9"]["eps"] - J531["base"][f"{c}|{foot}|CENSUS"]["K9"]["eps"]) for c in K.CONS for foot in K.FOOTS)
check("K1 S0 reproduces CFG531 committed BASE K9 eps (census, 1e-6)", k1 < 1e-6, f"max |d| {k1:.1e}")
P("  (CARRIED labels at S0:", {f: OUT[f'A|{f}|S0 base']['split']['carried'] for f in K.FOOTS}, "; CFG531 committed 'c_reading':", J531.get("c_reading"), ")")
# MU1
mu1 = False
for foot in K.FOOTS:
    for c in K.CONS:
        b, m = OUT[f"{c}|{foot}|S0 base"], OUT[f"{c}|{foot}|MU1 leak x3"]
        if (m["all"]["bands"]["K9"]["Z"] >= 3) != (b["all"]["bands"]["K9"]["Z"] >= 3) or abs(m["chi2_15"] - b["chi2_15"]) >= 4:
            mu1 = True
check("MU1 leaked fraction x3 changes the K9 class or census chi2 (>= 4) on at least one cell", mu1,
      "; ".join(f"{c}|{f}: chi2 {OUT[f'{c}|{f}|S0 base']['chi2_15']:.1f} -> {OUT[f'{c}|{f}|MU1 leak x3']['chi2_15']:.1f}" for c in K.CONS for f in K.FOOTS))
mu2 = any(abs(OUT[f"{c}|{f}|S3 removed (bound)"]["all"]["bands"]["K9"]["eps"] - OUT[f"{c}|{f}|S0 base"]["all"]["bands"]["K9"]["eps"]) > OUT[f"{c}|{f}|S0 base"]["all"]["bands"]["K9"]["sig"]
          for c in K.CONS for f in K.FOOTS)
check("MU2 SHMR removed moves K9 eps by > 1 sigma on at least one cell", mu2,
      "; ".join(f"{c}|{f}: {OUT[f'{c}|{f}|S0 base']['all']['bands']['K9']['eps']:+.3f} -> {OUT[f'{c}|{f}|S3 removed (bound)']['all']['bands']['K9']['eps']:+.3f}" for c in K.CONS for f in K.FOOTS))
RES["checks"] = CHK
json.dump(RES, open(os.path.join(HERE, "cfg601_shmr_sensitivity_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg601_shmr_sensitivity.out"), "w").write("\n".join(LOG) + "\n")
P(f"{sum(v['ok'] for v in CHK.values())}/{len(CHK)} checks pass")
