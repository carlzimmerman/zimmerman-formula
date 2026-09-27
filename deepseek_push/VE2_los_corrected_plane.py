#!/usr/bin/env python3
"""VE2 -- LOS-corrected discriminator plane (Z5-wave; owns VE2_*). VE1 completion.
VE1 banked corr_los(eps) = eps^p with p = -0.1061 (central) / -0.1307 (volume),
measured at i=90 only. This lane tests the corrected window across the FULL
inclination plane: fresh MC q=0, tau0=1, eps{1.0,0.7,0.5,0.3} x i{20,40,60,90} x
{central,volume}, n=4e5, Pool(8), fresh seeds (V02 seed_for + 911000), via
V02_inclination.one_cell loaded-not-transcribed. Gates pre-registered in
Z5-WAVE_BRIEF.md (P0, G1, G2, G3); house rules 1-10; leaf lane does NOT commit.
"""
import json, math, os, sys, time
from multiprocessing import Pool
from V02_inclination import one_cell, seed_for

HERE = os.path.dirname(os.path.abspath(__file__))
N = 400000
EPSES = (1.0, 0.7, 0.5, 0.3)
IANG = (20.0, 40.0, 60.0, 90.0)
RES = {"title": "VE2 LOS-corrected discriminator plane (VE1 completion)",
       "pre_registration": "Z5-WAVE_BRIEF.md VE2 gates"}
_T0 = time.time()

def finish(rc):
    RES["elapsed_s"] = round(time.time() - _T0, 1)
    RES["exit"] = rc
    with open(os.path.join(HERE, "VE2_results.json"), "w") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps({k: RES.get(k) for k in
                      ("verdict", "P0_parity", "G1_i90_repair", "G2_plane_order",
                       "G3_U_separation")}, indent=1))
    print("elapsed %ss; exit %s" % (RES["elapsed_s"], rc))
    sys.exit(rc)

def main():
    v02 = json.load(open(os.path.join(HERE, "V02_results.json")))
    ve1 = json.load(open(os.path.join(HERE, "VE1_results.json")))
    tabs = v02["measurements"]["U_los_tables_q0"]
    P = {s: ve1["K1_exponents"][s]["p_eps03"] for s in ("central", "volume")}

    specs = []
    for src in ("central", "volume"):
        for eps in EPSES:
            for i in IANG:
                specs.append(dict(tag="VE2_%s_%s_%d" % (src, eps, int(i)), n=N, q=0.0,
                                  src=src, eps=eps, i=i,
                                  seed=seed_for(eps, i, 0.0, src) + 911000))
    with Pool(8) as ex:
        rows = ex.map(one_cell, specs)
    fr = {(r["src"], r["eps"], r["i"]): r for r in rows}

    # P0 parity at (0.5, 90)
    pmax = 0.0
    for src in ("central", "volume"):
        st = tabs[src]["0.5"]["90"]
        f = fr[(src, 0.5, 90.0)]
        z = abs(f["R_lo"] - st["R"]) / math.sqrt(f["seR_lo"] ** 2 + st["se_R"] ** 2)
        pmax = max(pmax, z)
    RES["P0_parity"] = {"max_z": pmax, "pass": bool(pmax < 3.0)}
    if pmax >= 3.0:
        RES["verdict"] = "FAIL P0 machinery parity (z=%.2f)" % pmax
        finish(1)

    # G1: i=90 repair at fresh statistics
    g1 = {"ok": True, "rows": {}}
    for src in ("central", "volume"):
        anch = fr[(src, 1.0, 90.0)]
        for eps in (0.3, 0.5, 0.7):
            f = fr[(src, eps, 90.0)]
            rc_ = f["R_lo"] / (eps ** P[src])
            se = f["seR_lo"] / (eps ** P[src])
            sig = math.sqrt(se ** 2 + anch["seR_lo"] ** 2)
            z = abs(rc_ - anch["R_lo"]) / sig
            g1["rows"]["%s_%s" % (src, eps)] = z
            if z > 3.0:
                g1["ok"] = False
    RES["G1_i90_repair"] = g1

    # G2: full-plane ordering (same-i anchor)
    g2 = {"ok": True, "worst_z": None, "offenders": []}
    for src in ("central", "volume"):
        for i in IANG:
            anch = fr[(src, 1.0, i)]
            for eps in (0.3, 0.5, 0.7):
                f = fr[(src, eps, i)]
                rc_ = f["R_lo"] / (eps ** P[src])
                sig = math.sqrt((f["seR_lo"] / (eps ** P[src])) ** 2
                                + anch["seR_lo"] ** 2)
                z = (anch["R_lo"] - rc_) / sig
                g2["worst_z"] = z if g2["worst_z"] is None else max(g2["worst_z"], z)
                if z > 3.0:
                    g2["ok"] = False
                    g2["offenders"].append("%s eps=%s i=%d z=%.2f" % (src, eps, i, z))
    RES["G2_plane_order"] = g2

    # G3: U separation central-vs-volume at every (eps, i)
    g3 = {"ok": True, "min_z": None, "rows": {}}
    for eps in EPSES:
        for i in IANG:
            c, v = fr[("central", eps, i)], fr[("volume", eps, i)]
            z = abs(c["U_lo"] - v["U_lo"]) / math.sqrt(c["seU_lo"] ** 2
                                                       + v["seU_lo"] ** 2)
            g3["rows"]["%s_%d" % (eps, int(i))] = z
            g3["min_z"] = z if g3["min_z"] is None else min(g3["min_z"], z)
            if z < 3.0:
                g3["ok"] = False
    RES["G3_U_separation"] = g3

    ok = g1["ok"] and g2["ok"] and g3["ok"]
    RES["verdict"] = ("LOS-CORRECTED PLANE HOLDS: corr_los repairs i=90 at fresh stats "
                      "(G1), no ordering inversion anywhere on the (eps, i) plane (G2 "
                      "worst z = %.2f), U separation >= 3 sigma everywhere (G3 min z = "
                      "%.1f)" % (g2["worst_z"], g3["min_z"]) if ok else
                      "HONEST FAIL (recorded): G1=%s G2=%s G3=%s offenders=%s"
                      % (g1["ok"], g2["ok"], g3["ok"], g2["offenders"][:6]))
    finish(0 if ok else 1)

if __name__ == "__main__":
    main()
