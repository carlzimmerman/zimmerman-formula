#!/usr/bin/env python3
"""EUC16 figures (reported; nothing graded here; EUC15's figure script with EUC16's file names): every system SECURE at
TA or TB in euc16_sources.csv.  Left: the VIS box with the EUC16 arc (cross) and the 0.5 / 1.5 theta_E annulus.  Middle: the mean prepared
residual of the RGS000 (blue) and RGS180 (red) dithers, with each position's predicted line (dashed).  Right: every
usable dither shifted back by its own predicted offset and averaged (the midpoint in green).

Run:  python3 -I -B euc16_figs.py --data-dir <dir>      (writes figs/euc16_secure_*.png)
"""
import argparse, csv, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "closure_2026_11_12", "EUC14_predicted_split_source_redshifts"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "closure_2026_11_12", "EUC9_grism_spectra_source_redshifts"))
import euc14_core as C
import euc14_geom as GM
import euc14 as L

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from astropy.io import fits
    from astropy.wcs import WCS
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "euc16_sources.csv"))) if "SECURE" in (r["class_TA"], r["class_TB"])]
    PA = GM.load_pa(a.data_dir)
    mer = {}
    for fn in os.listdir(os.path.join(a.data_dir, "nisp_tables")):
        if fn.startswith("mer_") and fn.endswith(".csv"):
            for r in csv.DictReader(open(os.path.join(a.data_dir, "nisp_tables", fn))): mer[int(r["object_id"])] = (float(r["ra"]), float(r["dec"]))
    os.makedirs(os.path.join(HERE, "figs"), exist_ok=True)
    for pg in range(0, len(rows), 8):
        chunk = rows[pg:pg + 8]
        fig, ax = plt.subplots(len(chunk), 3, figsize=(13, 2.2 * len(chunk)), squeeze=False, gridspec_kw=dict(width_ratios=[1, 2.4, 2.4]))
        for i, r in enumerate(chunk):
            oid = int(r["mer_object_id"]); ra0, de0 = mer[oid]
            img = fits.getdata(os.path.join(a.data_dir, "euc15", "vis_boxes", "%d.fits" % oid)); w = WCS(fits.getheader(os.path.join(a.data_dir, "euc15", "vis_boxes", "%d.fits" % oid)))
            x0, y0 = w.all_world2pix(ra0, de0, 0); pix = 0.1
            off = np.array([float(r["arc_east_arcsec"]), float(r["arc_north_arcsec"])]); thE = float(r["theta_E_arcsec"])
            v = np.nanpercentile(img, [5, 99.5])
            ax[i, 0].imshow(img, origin="lower", cmap="gray", vmin=v[0], vmax=v[1])
            xa, ya = w.all_world2pix(ra0 + off[0] / 3600.0 / np.cos(np.radians(de0)), de0 + off[1] / 3600.0, 0)
            ax[i, 0].plot(xa, ya, "r+", ms=9)
            for f in (0.5, 1.5):
                t = np.linspace(0, 2 * np.pi, 100); ax[i, 0].plot(x0 + f * thE / pix * np.cos(t), y0 + f * thE / pix * np.sin(t), "c-", lw=0.4)
            ax[i, 0].set_xticks([]); ax[i, 0].set_yticks([])
            raw = dict(np.load(os.path.join(a.data_dir, "nisp_spectra_dith", "%d.npz" % oid), allow_pickle=False))
            U = GM.dither_dirs(raw, PA, L.CONV, ra0, de0); pr = GM.proj(U, off)
            dl = C.dithers(raw); lam0, k = float(r["midpoint_A"]), float(r["k"])
            q = np.abs(C.WL - lam0) <= 300.0
            for g, col in zip(C.POS, ("tab:blue", "tab:red")):
                num = np.zeros(C.NPIX); den = np.zeros(C.NPIX); sh = []
                for j, d in enumerate(dl):
                    if d is None or d["pos"] != g or not np.isfinite(pr[j]): continue
                    num += d["r"] * d["w"]; den += d["w"]; sh.append(C.DISP * k * pr[j])
                m = np.where(den > 0, num / np.where(den > 0, den, 1.0), np.nan)
                ax[i, 1].step(C.WL[q], m[q], where="mid", color=col, lw=0.8)
                if sh: ax[i, 1].axvline(lam0 + float(np.mean(sh)), color=col, ls="--", lw=0.6)
            num = np.zeros(C.NPIX); den = np.zeros(C.NPIX)
            for j, d in enumerate(dl):
                if d is None or not np.isfinite(pr[j]): continue
                s = C.DISP * k * pr[j]
                num += np.interp(C.WL, C.WL - s, d["r"] * d["w"], left=0, right=0); den += np.interp(C.WL, C.WL - s, d["w"], left=0, right=0)
            m = np.where(den > 0, num / np.where(den > 0, den, 1.0), np.nan)
            ax[i, 2].step(C.WL[q], m[q], where="mid", color="k", lw=0.8); ax[i, 2].axvline(lam0, color="g", lw=0.6, ls=":")
            ax[i, 1].set_title("%s (%s%s) TA %s / TB %s: %s z_s = %s, k = %s, arc (E %s, N %s)\", theta_E %.2f\"" % (r["unique_identifier"][-7:], r["grade"],
                               ", P" if r["in_P"] == "True" else "", r["class_TA"], r["class_TB"], r["line"], r["z_s"], r["k"], r["arc_east_arcsec"], r["arc_north_arcsec"], thE), fontsize=7)
            ax[i, 2].set_title("dithers shifted back by their predicted offsets", fontsize=7)
            for c in (1, 2): ax[i, c].tick_params(labelsize=6)
        fig.tight_layout(); fig.savefig(os.path.join(HERE, "figs", "euc16_secure_%02d.png" % (pg // 8)), dpi=75); plt.close(fig)
    print("figs/euc16_secure_*.png: %d systems" % len(rows))

if __name__ == "__main__":
    main()
