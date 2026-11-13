#!/usr/bin/env python3
"""EUC14 figures (reported; nothing graded here): every system SECURE at TA or TB in euc14_sources.csv, and the truth
lens.  Left: the mean prepared residual of the RGS000 (blue) and RGS180 (red) dithers in observed wavelength, with the
line's predicted position in each grism position (dashed).  Right: every usable dither shifted back by its own
predicted offset (k = 1) and averaged: a real arc line stacks at the midpoint (green).

Run:  python3 -I euc14_figs.py --data-dir <dir>      (writes figs/euc14_secure.png)
"""
import argparse, csv, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "EUC9_grism_spectra_source_redshifts"))
import euc14_core as C
import euc14_geom as GM
import euc14 as L

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "euc14_sources.csv"))) if "SECURE" in (r["class_TA"], r["class_TB"])]
    PA = GM.load_pa(a.data_dir)
    mer = {}
    for fn in os.listdir(os.path.join(a.data_dir, "nisp_tables")):
        if fn.startswith("mer_") and fn.endswith(".csv"):
            for r in csv.DictReader(open(os.path.join(a.data_dir, "nisp_tables", fn))): mer[int(r["object_id"])] = (float(r["ra"]), float(r["dec"]))
    fig, ax = plt.subplots(len(rows), 2, figsize=(11, 2.1 * len(rows)), squeeze=False)
    for i, r in enumerate(rows):
        oid = int(r["mer_object_id"]); raw = dict(np.load(os.path.join(a.data_dir, "nisp_spectra_dith", "%d.npz" % oid), allow_pickle=False))
        ra0, de0 = mer[oid]; U = GM.dither_dirs(raw, PA, L.CONV, ra0, de0)
        off = np.array([float(r["arc_east_arcsec"]), float(r["arc_north_arcsec"])]); pr = GM.proj(U, off)
        dl = C.dithers(raw); lam0, k = float(r["midpoint_A"]), float(r["k"])
        q = np.abs(C.WL - lam0) <= 300.0
        for g, col in zip(C.POS, ("tab:blue", "tab:red")):
            num = np.zeros(C.NPIX); den = np.zeros(C.NPIX); sh = []
            for j, d in enumerate(dl):
                if d is None or d["pos"] != g or not np.isfinite(pr[j]): continue
                num += d["r"] * d["w"]; den += d["w"]; sh.append(C.DISP * k * pr[j])
            m = np.where(den > 0, num / np.where(den > 0, den, 1.0), np.nan)
            ax[i, 0].step(C.WL[q], m[q], where="mid", color=col, lw=0.8)
            if sh: ax[i, 0].axvline(lam0 + float(np.mean(sh)), color=col, ls="--", lw=0.6)
        num = np.zeros(C.NPIX); den = np.zeros(C.NPIX)
        for j, d in enumerate(dl):
            if d is None or not np.isfinite(pr[j]): continue
            s = C.DISP * k * pr[j]
            num += np.interp(C.WL, C.WL - s, d["r"] * d["w"], left=0, right=0); den += np.interp(C.WL, C.WL - s, d["w"], left=0, right=0)
        m = np.where(den > 0, num / np.where(den > 0, den, 1.0), np.nan)
        ax[i, 1].step(C.WL[q], m[q], where="mid", color="k", lw=0.8); ax[i, 1].axvline(lam0, color="g", lw=0.6, ls=":")
        ax[i, 0].set_title("%s (%s%s) TA %s / TB %s: %s z_s = %s, k = %s, arc (E %s, N %s)\"" % (r["unique_identifier"][-7:], r["grade"], ", P" if r["in_P"] == "True" else "",
                          r["class_TA"], r["class_TB"], r["line"], r["z_s"], r["k"], r["arc_east_arcsec"], r["arc_north_arcsec"]), fontsize=7)
        ax[i, 1].set_title("dithers shifted back by their predicted offsets", fontsize=7)
        for c in (0, 1): ax[i, c].tick_params(labelsize=6)
    fig.tight_layout(); os.makedirs(os.path.join(HERE, "figs"), exist_ok=True)
    fig.savefig(os.path.join(HERE, "figs", "euc14_secure.png"), dpi=80)
    print("figs/euc14_secure.png: %d systems" % len(rows))

if __name__ == "__main__":
    main()
