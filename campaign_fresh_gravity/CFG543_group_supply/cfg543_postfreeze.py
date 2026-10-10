#!/usr/bin/env python3
"""CFG543 POST-FREEZE diagnostics (2026-10-09; written after the primary was seen; NO verdict weight).
1. Containment supply (5.364 M_cat / 0.10) WITH hot gas h x M_cat inside R500 (h = the NGC 4936 anchor 1.72, and a scan 0..4):
   where between P2 (h = 0) and P1 (census-internal h, median 4) does the class mean cross zero?
2. Residual trend with log M_cat for C0 / P2 / P3 (CFG540 found massive, high-f_ret groups above the law even without the edge).
Imports cfg543_group_supply read-only (its config_masses is wrapped here, not edited).
"""
import os, json, math
os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np
import cfg543_group_supply as M

HERE = M.HERE
OUT = []


def log(s=""):
    print(s); OUT.append(s)


_orig = M.config_masses


def cm(lM, cfg):
    if cfg["kind"] == "P2H":
        Mc = 10 ** lM
        return Mc, cfg["h"] * Mc, M.COLD_PER_B * Mc / 0.10, 0.10
    return _orig(lM, cfg)


M.config_masses = cm


def main():
    rows = M.read_groups()
    M.GEO = M.gas_geometry(M.lovisari())
    prim = json.load(open(os.path.join(HERE, "cfg543_results.json")))
    h2 = prim["D"]["NGC4936_ratio"]
    lM = np.array([o["lM"] for o in rows])
    res = {}
    log("CFG543 POST-FREEZE (no verdict weight)")
    for fk, a0 in M.FOOT.items():
        r = {}
        log(f"\n=== {fk} ===")
        D, s, st = M.run(rows, a0, dict(kind="P2H", h=h2))
        r["P2_plus_H2"] = st
        log(f"  containment supply + NGC4936-anchored hot gas (h = {h2:.2f} inside R500): mean {st['mean']:+.3f} Z {st['Z']:+.2f} -> {st['label']}")
        sc = {}
        for h in (0.0, 0.25, 0.5, 1.0, 1.72, 2.5, 4.0):
            D, _, _ = M.run(rows, a0, dict(kind="P2H", h=h), need_s=False)
            sc[str(h)] = float(D.mean())
        hs = np.array([float(k) for k in sc]); ms = np.array(list(sc.values()))
        hz = float(np.interp(0.0, ms[::-1], hs[::-1])) if ms.min() < 0 < ms.max() else None
        r["h_scan"] = sc; r["h_null"] = hz
        log("  h scan (containment supply): " + ", ".join(f"h {k} {v:+.3f}" for k, v in sc.items()) + f"; mean crosses 0 at h ~ {hz}")
        for nm in ("C0", "P2", "P3", "P1"):
            Dn = np.array(prim["footings"][fk]["configs"][nm]["Delta"])
            sl = float(np.polyfit(lM, Dn, 1)[0])
            r[f"slope_{nm}"] = sl
            hi = lM >= np.median(lM)
            log(f"  {nm}: dDelta/dlogM_cat {sl:+.3f}; mean upper-half mass {Dn[hi].mean():+.3f}, lower half {Dn[~hi].mean():+.3f}")
        res[fk] = r
    json.dump(res, open(os.path.join(HERE, "cfg543_postfreeze_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg543_postfreeze.out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
