#!/usr/bin/env python3
"""Digitise the ALPAKA I rotation-curve figure (Fig. 'vrot', arXiv:2303.16227) and validate it against the paper's tables.

The figure is a raster PNG (937 x 1020) with 19 disks in 5 columns. For each disk there is a velocity panel (pink ring
markers with a 1-sigma band) above a dispersion panel (teal markers and band).  Method:
  1. Axis label VALUES are transcribed by eye from 2.6x crops of the figure (table AXES below); OCR was tried and abandoned as
     unreliable.  Label POSITIONS are detected automatically (dark-pixel clusters under/above each axis).
  2. Each axis is a linear map fitted to its labelled ticks (x axes start at 0 at the left frame edge; y axes at 0 at the
     bottom frame edge); the fit residual is checked.
  3. Ring markers are found by colour, converted to (R arcsec, R kpc, V, sigma).  The band at each marker column gives the
     plotted 1-sigma interval.  The dashed grey line is the optical R_e where the paper drew it.
  4. Validation against the paper's own numbers: (a) R in kpc over R in arcsec must equal the angular scale at the galaxy's
     redshift (flat LCDM, H0 = 70, Om = 0.3, tolerance 6%); (b) max digitised V vs the table's V_max; (c) mean of the last two V
     vs the table's V_ext; (d) sigma likewise where the table gives a value.
Nothing is fitted.  Usage: python3 digitise.py
"""
import csv, os
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.join(HERE, "..")
LOG = []


def log(m):
    print(m); LOG.append(m)


COLS = [(60, 193), (240, 373), (420, 553), (600, 733), (779, 913)]
ROWS = [46, 289, 532, 775]
IDS = [[1, 2, 3, 6, 7], [8, 9, 11, 12, 13], [15, 18, 19, 20, 22], [23, 24, 25, 28]]
VH = 97
# labelled tick VALUES read from the figure, per disk: top axis (kpc), bottom axis (arcsec), velocity axis, dispersion axis.
# Horizontal: left to right, starting with the 0 at the frame edge.  Vertical: bottom to top, excluding the 0 at the frame bottom.
AXES = {
    1: ([0, 2.5, 5.0], [0, 0.4, 0.8], [80, 160], [8, 16]),
    2: ([0, 1, 2], [0, 0.15, 0.30], [100, 200], [10, 20]),
    3: ([0, 0.8, 1.6], [0, 0.08, 0.16, 0.24], [200, 400], [30, 60]),
    6: ([0, 1.5, 3.0], [0, 0.15, 0.30], [150, 300], [25, 50]),
    7: ([0, 2, 4], [0, 0.2, 0.4, 0.6], [150, 300], [25, 50]),
    8: ([0, 2.5, 5.0], [0, 0.3, 0.6], [200, 400], [40, 80]),
    9: ([0, 2, 4], [0, 0.2, 0.4], [150, 300], [25, 50]),
    11: ([0, 2.5, 5.0], [0, 0.25, 0.50], [200, 400], [20, 40]),
    12: ([0, 2.5, 5.0], [0, 0.25, 0.50, 0.75], [150, 300], [25, 50]),
    13: ([0, 1.5, 3.0], [0, 0.15, 0.30, 0.45], [150, 300], [20, 40]),
    15: ([0, 0.8, 1.6], [0, 0.08, 0.16, 0.24], [200, 400], [80, 160]),
    18: ([0, 2, 4], [0, 0.25, 0.50], [250, 500], [30, 60]),
    19: ([0, 1.5, 3.0], [0, 0.2, 0.4], [150, 300], [25, 50]),
    20: ([0, 2, 4], [0, 0.2, 0.4], [150, 300], [30, 60]),
    22: ([0, 0.8, 1.6], [0, 0.08, 0.16, 0.24], [200, 400], [30, 60]),
    23: ([0, 2.5, 5.0], [0, 0.3, 0.6, 0.9], [200, 400], [20, 40]),
    24: ([0, 1.5, 3.0], [0, 0.2, 0.4], [150, 300], [20, 40]),
    25: ([0, 2, 4], [0, 0.2, 0.4, 0.6], [150, 300], [30, 60]),
    28: ([0, 2, 4], [0, 0.25, 0.50], [200, 400], [150, 300]),
}

im = cv2.imread(os.path.join(HERE, "vrot_2303.16227.png"), cv2.IMREAD_UNCHANGED)
alpha = im[:, :, 3].astype(float) / 255.0
rgb = (im[:, :, :3].astype(float) * alpha[:, :, None] + 255 * (1 - alpha[:, :, None])).astype(np.uint8)
gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)


def clusters(mask1d, gap):
    idx = np.where(mask1d)[0]
    if len(idx) == 0:
        return []
    cl = [[idx[0], idx[0]]]
    for k in idx[1:]:
        if k - cl[-1][1] <= gap:
            cl[-1][1] = k
        else:
            cl.append([k, k])
    return cl


def horiz_calibration(x0, x1, ya, yb, values, name):
    strip = gray[ya:yb, x0 - 22:x1 + 22] < 150
    cl = [c for c in clusters(strip.any(axis=0), 9) if c[1] - c[0] >= 1]
    cx = [(c[0] + c[1]) / 2.0 + x0 - 22 for c in cl]
    cx = [x for x in cx if x0 - 8 <= x <= x1 + 12]                       # labels centred on ticks inside or at the frame edge
    if len(cx) != len(values):
        raise RuntimeError(f"{name}: found {len(cx)} label clusters at {[round(x, 1) for x in cx]} for {len(values)} values")
    b, a0 = np.polyfit(values, cx, 1)                                    # px = a0 + b*value
    resid = float(np.abs(np.array(cx) - (a0 + b * np.array(values))).max())
    edge = float(abs(a0 - x0))
    if resid > 2.0 or edge > 3.0:
        raise RuntimeError(f"{name}: calibration poor (residual {resid:.2f} px, zero {edge:.1f} px from the frame edge)")
    return a0, b, resid, edge


def vert_calibration(x0, ytop, ybot, values, name):
    """values bottom->top, excluding the 0 at ybot (frame bottom)."""
    strip = gray[ytop + 3:ybot - 5, x0 - 32:x0 - 5] < 150
    cl = [c for c in clusters(strip.any(axis=1), 2) if c[1] - c[0] >= 4]
    cy = [(c[0] + c[1]) / 2.0 + ytop + 3 for c in cl]
    cy = sorted(cy, reverse=True)                                        # bottom to top
    if len(cy) != len(values):
        raise RuntimeError(f"{name}: found {len(cy)} label clusters at {[round(y, 1) for y in cy]} for {len(values)} values")
    px = [ybot] + cy
    vv = [0.0] + list(values)
    b, a0 = np.polyfit(vv, px, 1)
    resid = float(np.abs(np.array(px) - (a0 + b * np.array(vv))).max())
    if resid > 2.0:
        raise RuntimeError(f"{name}: calibration poor (residual {resid:.2f} px)")
    return a0, b, resid


def markers(mask):
    # closing first: a dashed grey R_e line can cross a marker and split it
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    er = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    n, lab, st, cen = cv2.connectedComponentsWithStats(er)
    return sorted([tuple(cen[i]) for i in range(1, n) if st[i, cv2.CC_STAT_AREA] >= 6], key=lambda c: c[0])


def band(x, y0, y1, ymark, kind):
    col = rgb[y0:y1, int(round(x))].astype(int)
    ok = (col[:, 2] - col[:, 1] > 8) if kind == "pink" else ((col[:, 1] - col[:, 2] > 3) | ((col[:, 1] > col[:, 2]) & (col[:, 0] > 200) & (col[:, 1] < 235)))
    ym = int(round(ymark)) - y0
    if not (0 <= ym < len(ok)):
        return np.nan, np.nan
    lo = hi = ym
    while lo > 0 and ok[lo - 1]:
        lo -= 1
    while hi < len(ok) - 1 and ok[hi + 1]:
        hi += 1
    return lo + y0, hi + y0


def ang_scale_kpc_per_arcsec(z, H0=70.0, Om=0.3, n=4000):
    c = 299792.458
    zz = np.linspace(0, z, n); E = np.sqrt(Om * (1 + zz) ** 3 + (1 - Om))
    dc = c / H0 * np.trapz(1 / E, zz)                                # Mpc
    da = dc / (1 + z)
    return da * 1000.0 * np.pi / 180.0 / 3600.0                          # kpc per arcsec


# sample redshifts and table velocities from the parsed tables
sample = {int(r["id"]): float(r["z"]) for r in csv.DictReader(open(os.path.join(TAB, "alpaka1_sample.csv")))}
kin = {int(r["id"]): r for r in csv.DictReader(open(os.path.join(TAB, "alpaka1_kinematics.csv")))}

pts, cal, dbg = [], [], rgb.copy()
pink = ((hsv[:, :, 1] > 115) & (hsv[:, :, 2] > 170) & ((hsv[:, :, 0] < 12) | (hsv[:, :, 0] > 170))).astype(np.uint8)
teal = ((hsv[:, :, 1] > 70) & (hsv[:, :, 2] < 170) & (hsv[:, :, 0] > 70) & (hsv[:, :, 0] < 100)).astype(np.uint8)
for r, yt in enumerate(ROWS):
    for c, gid in enumerate(IDS[r]):
        x0, x1 = COLS[c]
        yv0, yv1 = yt, yt + VH
        ys0, ys1 = yv1, yt + 2 * VH
        top_v, bot_v, vv, sv = AXES[gid]
        tx = horiz_calibration(x0, x1, yv0 - 19, yv0 - 7, top_v, f"ID{gid} top")
        bx = horiz_calibration(x0, x1, ys1 + 5, ys1 + (22 if r < 3 else 27), bot_v, f"ID{gid} bottom")
        vy = vert_calibration(x0, yv0, yv1, vv, f"ID{gid} V")
        sy = vert_calibration(x0, ys0, ys1, sv, f"ID{gid} sigma")
        inv = lambda cal_, px: (px - cal_[0]) / cal_[1]
        pm = [(x + x0 + 1, y + yv0 + 1) for x, y in markers(pink[yv0 + 1:yv1, x0 + 1:x1])]
        tm = [(x + x0 + 1, y + ys0 + 1) for x, y in markers(teal[ys0 + 1:ys1, x0 + 1:x1])]
        sub = gray[yv0 + 2:yv1 - 1, x0 + 3:x1 - 2].astype(int)
        cnt = ((sub > 60) & (sub < 175)).sum(axis=0)
        cand = np.where(cnt > 0.35 * sub.shape[0])[0]
        dash = float(np.mean(cand)) + x0 + 3 if len(cand) else None
        for k, (x, y) in enumerate(pm):
            lo, hi = band(x, yv0 + 1, yv1, y, "pink")
            pts.append([gid, k + 1, "V", inv(bx, x), inv(tx, x), inv(vy, y), inv(vy, hi) if np.isfinite(hi) else np.nan,
                        inv(vy, lo) if np.isfinite(lo) else np.nan, round(x, 1), round(y, 1)])
            cv2.circle(dbg, (int(x), int(y)), 7, (255, 0, 0), 1)
        for k, (x, y) in enumerate(tm):
            lo, hi = band(x, ys0 + 1, ys1, y, "teal")
            pts.append([gid, k + 1, "sigma", inv(bx, x), inv(tx, x), inv(sy, y), inv(sy, hi) if np.isfinite(hi) else np.nan,
                        inv(sy, lo) if np.isfinite(lo) else np.nan, round(x, 1), round(y, 1)])
            cv2.circle(dbg, (int(x), int(y)), 7, (0, 0, 255), 1)
        cal.append(dict(id=gid, n_v=len(pm), n_s=len(tm), bx=bx, tx=tx, vy=vy, sy=sy,
                        dash_arcsec=inv(bx, dash) if dash else np.nan, dash_kpc=inv(tx, dash) if dash else np.nan))
cv2.imwrite(os.path.join(HERE, "debug_overlay.png"), dbg)

# ---------------------------------------------------------------- write points
with open(os.path.join(HERE, "alpaka1_vrot_digitised.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "ring", "panel", "R_arcsec", "R_kpc", "value_kms", "band_hi_kms", "band_lo_kms", "px_x", "px_y"])
    for p in pts:
        w.writerow([p[0], p[1], p[2]] + [("%.4f" % v if isinstance(v, float) and np.isfinite(v) else ("" if isinstance(v, float) else v)) for v in p[3:]])

# ---------------------------------------------------------------- validation
bad = []
by = {}
for p in pts:
    by.setdefault((p[0], p[2]), []).append(p)
rows = []
for cdict in cal:
    gid = cdict["id"]
    V = sorted(by[(gid, "V")], key=lambda p: p[3]); S = sorted(by[(gid, "sigma")], key=lambda p: p[3])
    Rk = np.array([p[4] for p in V]); Ra = np.array([p[3] for p in V]); Vv = np.array([p[5] for p in V])
    scale_digit = float(np.mean(Rk / Ra)); scale_true = ang_scale_kpc_per_arcsec(sample[gid])
    tv = kin[gid]
    vmax_t = float(tv["vmax_kms"]); vext_t = float(tv["vext_kms"])
    vmax_d = float(Vv.max()); vext_d = float(np.mean(Vv[-2:]))
    sig_ok = ""
    if S and tv["sigma_ext_kms"]:
        se_t = float(tv["sigma_ext_kms"]); se_d = float(np.mean([p[5] for p in S][-2:])); sig_ok = f"{se_d:.1f} vs {se_t:.1f}"
    rows.append([gid, sample[gid], len(V), len(S), float(Ra.max()), float(Rk.max()), scale_digit, scale_true, vmax_d, vmax_t, vext_d, vext_t,
                 cdict["dash_arcsec"], cdict["dash_kpc"], sig_ok])
    tol = []
    if abs(scale_digit / scale_true - 1) > 0.06: tol.append(f"kpc/arcsec {scale_digit:.2f} vs cosmology {scale_true:.2f}")
    if abs(vmax_d / vmax_t - 1) > 0.05: tol.append(f"Vmax {vmax_d:.0f} vs {vmax_t:.0f}")
    if abs(vext_d / vext_t - 1) > 0.05: tol.append(f"Vext {vext_d:.0f} vs {vext_t:.0f}")
    if tol: bad.append((gid, tol))
with open(os.path.join(HERE, "alpaka1_vrot_validation.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "z", "n_V_rings", "n_sigma_rings", "R_ext_arcsec", "R_ext_kpc", "kpc_per_arcsec_digitised", "kpc_per_arcsec_cosmology",
                "Vmax_digitised", "Vmax_table", "Vext_digitised_mean_last2", "Vext_table", "dashed_line_Re_arcsec", "dashed_line_Re_kpc",
                "sigma_ext_digitised_vs_table"])
    for rw in rows:
        w.writerow([("%.4f" % v if isinstance(v, float) and np.isfinite(v) else ("" if isinstance(v, float) else v)) for v in rw])
nmismatch = [rw[0] for rw in rows if rw[2] != rw[3]]
log(f"velocity and dispersion panels carry the same number of rings for every disk: {'PASS' if not nmismatch else 'FAIL ' + str(nmismatch)}")
dv = np.array([abs(rw[8] / rw[9] - 1) for rw in rows]); de = np.array([abs(rw[10] / rw[11] - 1) for rw in rows])
ds = np.array([abs(rw[6] / rw[7] - 1) for rw in rows])
log(f"accuracy against the paper's own table (19 disks): |Vmax dev| median {np.median(dv)*100:.1f}% max {dv.max()*100:.1f}%; "
    f"|Vext dev| median {np.median(de)*100:.1f}% max {de.max()*100:.1f}%; kpc/arcsec vs cosmology median {np.median(ds)*100:.1f}% max {ds.max()*100:.1f}%")
log(f"digitised {len(pts)} markers on {len(cal)} disks; validation failures (>6% scale, >5% Vmax or Vext): {len(bad)}")
# outer-radius summary
A0 = 1.2e-10; KPC = 3.0857e19
with open(os.path.join(HERE, "alpaka1_outer_summary.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "z", "n_rings", "R_ext_arcsec", "R_ext_kpc", "Vext_kms_table", "Re_arcsec_dashed_line", "Re_kpc_dashed_line",
                "R_ext_over_Re", "Vext2_over_Rext_over_a0"])
    for rw in rows:
        gid = rw[0]; rext_a, rext_k = rw[4], rw[5]; vext = float(kin[gid]["vext_kms"])
        re_a, re_k = rw[12], rw[13]
        gobs = (vext * 1e3) ** 2 / (rext_k * KPC) / A0
        w.writerow([gid, rw[1], rw[2], "%.4f" % rext_a, "%.3f" % rext_k, "%.0f" % vext,
                    "%.4f" % re_a if np.isfinite(re_a) else "", "%.3f" % re_k if np.isfinite(re_k) else "",
                    "%.2f" % (rext_a / re_a) if np.isfinite(re_a) else "", "%.1f" % gobs])
log("wrote alpaka1_outer_summary.csv (R_ext/R_e only where the paper drew R_e; V^2/R_ext over a0 is a rough total-acceleration estimate, NOT g_bar)")
for g_, t_ in bad:
    log(f"  ID{g_}: {t_}")
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
