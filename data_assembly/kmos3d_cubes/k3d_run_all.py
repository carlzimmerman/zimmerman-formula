#!/usr/bin/env python3
"""Fit all KMOS3D cubes with catalogue Z >= 1.9 on disk, as fixed in FROZEN_CRITERIA_2026-09-30.md. usage: python3 k3d_run_all.py [main|alt]  (alt = C3 variant: q0=0.1, PA starts offset by 22.5 deg)"""
import sys, os, time, numpy as np, pandas as pd
from multiprocessing import Pool
import k3d_fit as K
D = "/Users/carlzimmerman/new_physics/_external_data/kmos3d/cubes/"
cat = pd.read_csv("../kmos3d_phibss/kmos3d_catalog.csv")
MODE = sys.argv[1] if len(sys.argv) > 1 else "main"
REDO = len(sys.argv) > 2 and sys.argv[2] == "redo"   # re-run only the rows that errored in the first pass (code fixes for missing SPEC_RES / position outside the cube)
def run(row):
    row = pd.Series(row); out = dict(ID=row.ID, FILE=row.FILE, Z=row.Z, OBSBAND=row.OBSBAND)
    sn = row.HAFIT_FLUX_HA / row.HAFIT_FLUX_HA_ERR if np.isfinite(row.HAFIT_FLUX_HA) and np.isfinite(row.HAFIT_FLUX_HA_ERR) and row.HAFIT_FLUX_HA_ERR > 0 else np.nan
    out["cat_SN"] = sn; out["quality"] = "highSN" if sn >= 10 else "lowSN"
    need = [row.RHALF, row.Q, row.SPEC_RES, row.RA, row.DEC]
    if not all(np.isfinite(need)) or row.RHALF <= 0: out["status"] = "no catalogue size/axis ratio/resolution"; return out
    try:
        t = time.time(); q0 = 0.2 if MODE == "main" else 0.1
        cube = K.Cube(D + row.FILE, row.Z, row.RA, row.DEC, row.RHALF, row.Q, row.SPEC_RES, q0=q0)
        if len(cube.win) < 30 or cube.ok.sum() < 500: out["status"] = "too few usable channels/pixels"; return out
        f0 = 1e-3 * (row.HAFIT_FLUX_HA if np.isfinite(row.HAFIT_FLUX_HA) and row.HAFIT_FLUX_HA > 0 else 5.0) * (row.HAFIT_FLUX_AP_CORR if np.isfinite(row.HAFIT_FLUX_AP_CORR) else 1.0)
        r = K.fit(cube, f0, pa_offset=0.0 if MODE == "main" else 22.5); out.update(K.summarize(cube, r)); out["status"] = "ok"; out["secs"] = time.time() - t
        out["badchi"] = bool(out["chi2r"] > 3); out["catalog_HAFIT_SIG"] = row.HAFIT_SIG
    except Exception as e: out["status"] = "error: %s" % e
    return out
if __name__ == "__main__":
    s = cat[(cat.Z >= 1.9) & cat.FILE.apply(lambda f: os.path.exists(D + f))].reset_index(drop=True)
    if REDO:
        prev = pd.read_csv(f"k3d_fits_{MODE}.csv"); bad = set(prev[prev.status != "ok"].ID); s = s[s.ID.isin(bad)].reset_index(drop=True)
    print("galaxies to fit:", len(s), "mode", MODE, "redo" if REDO else "", flush=True)
    with Pool(14) as p: res = p.map(run, [r.to_dict() for _, r in s.iterrows()], chunksize=1)
    df = pd.DataFrame(res)
    if REDO:
        prev = pd.read_csv(f"k3d_fits_{MODE}.csv"); prev = prev[~prev.ID.isin(df.ID)]; df = pd.concat([prev, df], ignore_index=True); df.to_csv(f"k3d_fits_{MODE}_final.csv", index=False)
    else: df.to_csv(f"k3d_fits_{MODE}.csv", index=False)
    print(df.status.value_counts().to_dict())
