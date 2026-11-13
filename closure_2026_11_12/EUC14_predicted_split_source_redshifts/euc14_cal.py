#!/usr/bin/env python3
"""EUC14 field calibration of the dispersion direction and scale (no lens or grade-X object is used).

Each calibrator is a pair (A, B) of catalogued field objects 0.8 to 2.5 arcsec apart, more than 30 arcsec from every
ECLIPSE system, where B's own spectrum carries a strong compact line at lambda_B (Euclid's catalogue).  Where B falls
inside A's extraction, B's line appears in A's dither spectra at  lambda_B + DISP * k * (D . u_i),  D = B - A, k = 1.

For every convention (C0 in 0, 90, 180, 270 deg; tilt sign +1, -1 or 0) the line is fitted in A's dithers with the
midpoint held within 30 A of lambda_B and the scale k free in [-2, 2]:
  - D(conv)  = the best d2 at k = 1 (the prediction), and whether it reaches S/N 6;
  - k_hat    = the k of the best d2 over all k.
The convention is the one with the most calibrators detected at k = 1 (S/N >= 6); then the scale is checked: the
median k_hat of calibrators detected anywhere in k (S/N >= 8) must be within 0.15 of 1.

Run:  python3 -I euc14_cal.py --data-dir <dir>      (writes euc14_cal.out / euc14_cal_results.json)
"""
import argparse, csv, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "EUC9_grism_spectra_source_redshifts"))
import euc14_core as C
import euc14_geom as GM

LAM_WIN = 30.0
SN_DET, SN_SCALE = 6.0, 8.0
OUT = []
def P(s=""):
    if QUIET[0]: return
    print(s); OUT.append(s)

def fit_pair(raw, dl, S, U, off, lam_b):
    pr = GM.proj(U, off)
    lam0 = C.LAM0[np.abs(C.LAM0 - lam_b) <= LAM_WIN]
    if len(lam0) == 0: return None
    best = dict(d2=0.0); k1 = dict(d2=0.0)
    j1 = int(np.argmin(np.abs(C.KGRID - 1.0)))
    for s in C.SIG_PAIR:
        sc = C.scan(dl, S, pr, s, lam0=lam0)
        d2 = np.where(sc["F"] > 0, sc["d2"], 0.0)
        a, b = np.unravel_index(int(np.argmax(d2)), d2.shape)
        if d2[a, b] > best["d2"]: best = dict(d2=float(d2[a, b]), k=float(C.KGRID[a]), lam0=float(lam0[b]), sig=s,
                                              sn000=float(sc["sn_pos"][C.POS[0]][a, b]), sn180=float(sc["sn_pos"][C.POS[1]][a, b]))
        b1 = int(np.argmax(d2[j1]))
        if d2[j1, b1] > k1["d2"]: k1 = dict(d2=float(d2[j1, b1]), lam0=float(lam0[b1]), sig=s)
    h = float(np.nanmedian(np.abs(pr))) if np.any(np.isfinite(pr)) else float("nan")
    return dict(best=best, k1=k1, h=h)

QUIET = [False]
def summary(data_dir):
    """the calibration recomputed (for the lane's check C1); prints nothing, writes nothing"""
    QUIET[0] = True
    try: return compute(data_dir, write=False)
    finally: QUIET[0] = False

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    compute(a.data_dir, write=True)

def compute(data_dir, write):
    odir = os.path.join(data_dir, "euc14"); cdir = os.path.join(odir, "cal_spectra")
    PA = GM.load_pa(data_dir)
    pairs = list(csv.DictReader(open(os.path.join(odir, "cal_pairs.csv"))))                  # first list (by line S/N; fetch stopped at 72)
    for p in pairs: p["list"] = "first"
    for p in csv.DictReader(open(os.path.join(odir, "cal_pairs_aligned.csv"))): p["list"] = "aligned"; pairs.append(p)
    P("EUC14 field calibration: %d calibrator pairs selected; position angles for %d pointings" % (len(pairs), len(PA)))
    R = []
    for p in pairs:
        fn = os.path.join(cdir, "%s.npz" % p["a_id"])
        if not os.path.exists(fn): continue
        raw = dict(np.load(fn, allow_pickle=False)); dl = C.dithers(raw)
        if not any(d is not None and d["pos"] == C.POS[0] for d in dl) or not any(d is not None and d["pos"] == C.POS[1] for d in dl): continue
        S = C.sums(dl, C.SIG_PAIR)
        ra, de = float(p["a_ra"]), float(p["a_dec"])
        off = GM.tan_offset(float(p["b_ra"]), float(p["b_dec"]), ra, de)
        row = dict(a=p["a_id"], b=p["b_id"], list=p["list"], sep=float(p["sep"]), lam_b=float(p["lam_b"]), snr_b=float(p["snr_b"]), off=off.tolist(),
                   ndith=len(dl), npa=0, conv={})
        for conv in GM.CONVS:
            U = GM.dither_dirs(raw, PA, conv, ra, de); row["npa"] = int(np.sum(np.isfinite(U[:, 0])))
            r = fit_pair(raw, dl, S, U, off, row["lam_b"])
            if r: row["conv"]["%g,%g" % conv] = r
        R.append(row)
    P("calibrators with a usable dither in each grism position: %d (first list %d, aligned list %d)" % (len(R), sum(r["list"] == "first" for r in R), sum(r["list"] == "aligned" for r in R)))
    # ---------------------------------------------------------------- convention
    tab = []
    for conv in GM.CONVS:
        key = "%g,%g" % conv
        det = [r for r in R if key in r["conv"] and r["conv"][key]["k1"]["d2"] >= SN_DET ** 2]
        tot = sum(min(r["conv"][key]["k1"]["d2"], 400.0) for r in R if key in r["conv"])
        tab.append((len(det), tot, conv))
        P("  convention C0 = %3.0f deg, tilt sign %+.0f: detected at k = 1 (S/N >= %.0f) in %3d; sum of d2 (each capped at 400) %.0f"
          % (conv[0], conv[1], SN_DET, len(det), tot))
    tab.sort(key=lambda t: (-t[0], -t[1])); win = tab[0][2]; key = "%g,%g" % win
    other = [t for t in tab if t[2][0] != win[0]]                     # the best convention with another C0
    nxt = other[0][0] if other else 0
    P("  -> convention C0 = %.0f deg, tilt sign %+.0f (best other C0: %d detections; the tilt sign is weakly determined)" % (win[0], win[1], nxt))
    # ---------------------------------------------------------------- scale
    det = [r for r in R if key in r["conv"] and r["conv"][key]["best"]["d2"] >= SN_SCALE ** 2 and r["conv"][key]["h"] >= 0.5]
    ks = np.array([r["conv"][key]["best"]["k"] for r in det])
    if len(ks):
        med = float(np.median(ks)); mad = float(1.4826 * np.median(np.abs(ks - med)))
        dl0 = np.array([r["conv"][key]["best"]["lam0"] - r["lam_b"] for r in det])
        P("  scale: %d calibrators detected anywhere in k at S/N >= %.0f with predicted half-split >= 0.5 arcsec: median k_hat %.3f, robust sigma %.3f;"
          " fraction with |k_hat - 1| <= 0.3: %.2f; k_hat < 0: %d" % (len(ks), SN_SCALE, med, mad, float(np.mean(np.abs(ks - 1) <= 0.3)), int(np.sum(ks < 0))))
        P("         midpoint minus catalogue lambda_B: median %+.1f A, robust sigma %.1f A" % (float(np.median(dl0)), float(1.4826 * np.median(np.abs(dl0 - np.median(dl0))))))
        for r in sorted(det, key=lambda r: -r["conv"][key]["best"]["d2"]):
            b = r["conv"][key]["best"]
            P("    A %s  sep %.2f  offset (E %+.2f, N %+.2f)  h %.2f\"  lam_B %.0f  k_hat %+.2f  S/N %.1f (RGS000 %.1f, RGS180 %.1f)  S/N at k=1 %.1f"
              % (r["a"], r["sep"], r["off"][0], r["off"][1], r["conv"][key]["h"], r["lam_b"], b["k"], math.sqrt(b["d2"]), b["sn000"], b["sn180"],
                 math.sqrt(r["conv"][key]["k1"]["d2"])))
    else:
        med = mad = float("nan")
    ok = len(ks) >= 5 and abs(med - 1.0) <= 0.15 and tab[0][0] >= 5 and tab[0][0] >= 2 * max(nxt, 1)
    P("  CALIBRATION %s" % ("PASSES" if ok else "FAILS"))
    res = dict(convention=list(win), n_detected=tab[0][0], next_detected=nxt, k_median=med, k_sigma=mad, n_scale=int(len(ks)), passes=bool(ok),
               table=[(t[0], t[1], list(t[2])) for t in tab])
    if write:
        json.dump(dict(res, rows=R), open(os.path.join(HERE, "euc14_cal_results.json"), "w"), indent=1, default=float)
        open(os.path.join(HERE, "euc14_cal.out"), "w").write("\n".join(OUT) + "\n")
    return res

if __name__ == "__main__":
    main()
