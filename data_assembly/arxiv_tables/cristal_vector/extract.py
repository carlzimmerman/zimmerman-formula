#!/usr/bin/env python3
"""Extract the model velocity profiles of the 14 ALMA-CRISTAL disks from the paper's VECTOR figure.

Source: figs/mass_profile_v4.pdf of arXiv:2507.11600 (copied here, sha256 in manifest).  Each of the 14 panels shows, against R in
kpc: V_circ,bary (green), V_circ,DM (yellow), V_circ,tot (orange) with an asymmetric-drift correction, f_DM(<R) = V_DM^2/V_tot^2 (grey, right
axis), the intrinsic sigma_0 (red dashed), the disk effective radius (grey dashed vertical), the folded 1D observed profile (circles with
error bars) and the same profile extracted from the DysmalPy model cubes (squares).
The PDF stores every curve as a polyline of exact vertices and all tick labels as text, so nothing is read by eye: axes are calibrated from
the major ticks and their labels and every curve vertex is converted directly.
Validation against the paper's own table (cristal2025_dynamics.csv): sigma_0, R_e,disk, f_DM(R_e).
Usage: python3 extract.py
"""
import collections, csv, os, re
import fitz
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.join(HERE, "..")
LOG = []


def log(m):
    print(m); LOG.append(m)


def check(c, m):
    log(("PASS  " if c else "FAIL  ") + m)
    if not c:
        open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
        raise SystemExit("check failed: " + m)


doc = fitz.open(os.path.join(HERE, "mass_profile_v4_2507.11600.pdf"))
page = doc[0]
dr = page.get_drawings()
words = page.get_text("words")

# ---------------------------------------------------------------- panels
frames = []
for x in dr:
    for it in x["items"]:
        if it[0] == "re":
            r = it[1]
            if 270 < r.width < 290 and 170 < r.height < 185:
                frames.append((r.x0, r.y0, r.x1, r.y1))
frames = sorted(set((round(a, 1), round(b, 1), round(c, 1), round(d, 1)) for a, b, c, d in frames), key=lambda f: (round(f[1]), f[0]))
check(len(frames) == 14, f"14 panel frames found (got {len(frames)})")


def in_frame(pt, f, pad=0.0):
    return f[0] - pad <= pt[0] <= f[2] + pad and f[1] - pad <= pt[1] <= f[3] + pad


names = {}
for w in words:
    if w[4].startswith("CRISTAL"):
        cx, cy = (w[0] + w[2]) / 2, (w[1] + w[3]) / 2
        for k, f in enumerate(frames):
            if in_frame((cx, cy), f):
                names[k] = w[4].replace("−", "-").replace("CRISTAL-", "")
check(len(names) == 14, f"every panel has a CRISTAL title ({names})")

# ---------------------------------------------------------------- ticks
def seg_lines(color=None, fill=None, width=None):
    out = []
    for x in dr:
        if color is not None and x.get("color") != color:
            continue
        if fill is not None and x.get("fill") != fill:
            continue
        if width is not None and abs((x.get("width") or 0) - width) > 1e-6:
            continue
        for it in x["items"]:
            if it[0] == "l":
                out.append((it[1].x, it[1].y, it[2].x, it[2].y))
    return out


black_lines = seg_lines(color=(0.0, 0.0, 0.0))
htick = [s for s in black_lines if abs(s[1] - s[3]) < 0.01 and 9 < abs(s[0] - s[2]) < 11]     # horizontal major ticks
vtick = [s for s in black_lines if abs(s[0] - s[2]) < 0.01 and 9 < abs(s[1] - s[3]) < 11]     # vertical major ticks


def num(s):
    s = s.replace("−", "-")
    return float(s) if re.fullmatch(r"-?\d+(\.\d+)?", s) else None


def fit(pairs, name, tol=0.35):
    px = np.array([p for p, v in pairs]); vv = np.array([v for p, v in pairs])
    b, a = np.polyfit(px, vv, 1)
    resid = float(np.abs(a + b * px - vv).max()) / max(abs(vv).max(), 1e-9)
    px_resid = float(np.abs((vv - a) / b - px).max())
    check(len(pairs) >= 2 and px_resid < tol, f"{name}: linear axis from {len(pairs)} labelled ticks, residual {px_resid:.3f} pt")
    return a, b


cal = {}
for k, f in enumerate(frames):
    x0, y0, x1, y1 = f
    # left axis (V, km/s)
    lab = [((w[1] + w[3]) / 2, num(w[4])) for w in words if x0 - 48 < (w[0] + w[2]) / 2 < x0 - 1 and y0 - 4 < (w[1] + w[3]) / 2 < y1 + 4 and num(w[4]) is not None]
    ticks_y = [s[1] for s in htick if x0 - 0.8 < min(s[0], s[2]) < x0 + 0.8 and y0 - 0.6 < s[1] < y1 + 0.6]
    pairs = []
    for yc, v in lab:
        cand = [t for t in ticks_y if abs(t - yc) < 4.0]
        if v == 0 and abs(yc - y1) > 3.0:
            continue                                   # the 0 label of the panel above sits on this panel's top edge
        pairs.append((min(cand, key=lambda t: abs(t - yc)) if cand else (y1 if v == 0 else None), v))
    pairs = sorted(set((round(p, 2), v) for p, v in pairs if p is not None))
    ay, by = fit(pairs, f"{names[k]} left axis")
    # right axis (f_DM)
    labr = [((w[1] + w[3]) / 2, num(w[4])) for w in words if x1 + 1 < (w[0] + w[2]) / 2 < x1 + 50 and y0 - 4 < (w[1] + w[3]) / 2 < y1 + 4 and num(w[4]) is not None]
    ticks_r = [s[1] for s in htick if x1 - 0.8 < max(s[0], s[2]) < x1 + 0.8 and y0 - 0.6 < s[1] < y1 + 0.6]
    pr = []
    for yc, v in labr:
        cand = [t for t in ticks_r if abs(t - yc) < 4.0]
        if v == 0 and abs(yc - y1) > 3.0:
            continue
        pr.append((min(cand, key=lambda t: abs(t - yc)) if cand else (y1 if v == 0 else None), v))
    pr = sorted(set((round(p, 2), v) for p, v in pr if p is not None))
    ar, br = fit(pr, f"{names[k]} right axis (f_DM)")
    cal[k] = dict(ay=ay, by=by, ar=ar, br=br)

# x axis: the lowest panel of each column carries the labels
cols = sorted(set(f[0] for f in frames))
xcal = {}
for c in cols:
    col_frames = [f for f in frames if f[0] == c]
    low = max(col_frames, key=lambda f: f[1])
    x0, y0, x1, y1 = low
    lab = [((w[0] + w[2]) / 2, num(w[4])) for w in words if y1 < (w[1] + w[3]) / 2 < y1 + 28 and x0 - 6 < (w[0] + w[2]) / 2 < x1 + 6 and num(w[4]) is not None]
    tx = [s[0] for s in vtick if y1 - 10.6 < min(s[1], s[3]) < y1 + 0.6 and x0 - 0.8 < s[0] < x1 + 0.8]
    pairs = []
    for xc, v in lab:
        cand = [t for t in tx if abs(t - xc) < 4.0]
        if cand:
            pairs.append((min(cand, key=lambda t: abs(t - xc)), v))
    a, b = fit(pairs, f"x axis of the column at x0 = {c}")
    xcal[c] = (a, b)
    check(abs(a + b * x0) < 0.05, f"x = 0 kpc sits at the left frame edge for the column at x0 = {c} (R at the edge = {a + b * x0:.3f} kpc)")
scales = [xcal[c][1] for c in cols]
check(max(scales) / min(scales) - 1 < 0.002, f"the three columns share one x scale (kpc per pt {scales})")


def R_of(px, col):
    a, b = xcal[col]
    return a + b * px


# ---------------------------------------------------------------- curves
def color_of(x):
    c = x.get("color")
    return tuple(round(v, 2) for v in c) if c else None


def polyline(x):
    pts = []
    for it in x["items"]:
        if it[0] == "l":
            if not pts:
                pts.append((it[1].x, it[1].y))
            pts.append((it[2].x, it[2].y))
    return pts


STYLE = {"V_bary": (0.21, 0.45, 0.39), "V_DM": (0.88, 0.69, 0.07), "V_tot": (0.84, 0.47, 0.23)}
curves = {k: {} for k in range(14)}
for x in dr:
    c = color_of(x)
    if x.get("type") != "s":
        continue
    pts = polyline(x)
    if len(pts) < 10:
        continue
    for nm, col in STYLE.items():
        if c == col:
            for k, f in enumerate(frames):
                if abs(pts[0][0] - f[0]) < 1.0 and f[1] - 0.5 <= min(p[1] for p in pts) and max(p[1] for p in pts) <= f[3] + 0.5:
                    curves[k][nm] = pts
    if c == (0.5, 0.5, 0.5) and abs((x.get("width") or 0) - 1.0) < 1e-6 and str(x.get("dashes")).startswith("[]"):
        for k, f in enumerate(frames):
            if abs(pts[0][0] - f[0]) < 5.0 and f[1] - 0.5 <= min(p[1] for p in pts) and max(p[1] for p in pts) <= f[3] + 0.5:
                curves[k]["f_DM"] = pts
for k in range(14):
    check(set(curves[k]) == {"V_bary", "V_DM", "V_tot", "f_DM"}, f"{names[k]}: all four curves found ({sorted(curves[k])})")

rows_c = []
for k, f in enumerate(frames):
    ay, by, ar, br = cal[k]["ay"], cal[k]["by"], cal[k]["ar"], cal[k]["br"]
    for nm, pts in curves[k].items():
        for (px, py) in pts:
            v = (ar + br * py) if nm == "f_DM" else (ay + by * py)
            rows_c.append([names[k], nm, R_of(px, f[0]), v])
with open(os.path.join(HERE, "cristal_curves.csv"), "w", newline="") as fo:
    w = csv.writer(fo); w.writerow(["id", "curve", "R_kpc", "value"])
    for r in rows_c:
        w.writerow([r[0], r[1], "%.4f" % r[2], "%.4f" % r[3]])

# ---------------------------------------------------------------- scalars: sigma0, R_e, shaded band
scal = {}
last_panel = None
for x in dr:
    c = color_of(x)
    if x.get("type") == "s" and c == (0.78, 0.35, 0.28):
        pts = polyline(x)
        for k, f in enumerate(frames):
            if pts and in_frame(pts[0], f, 1.0) and abs(pts[0][1] - pts[-1][1]) < 0.01:
                scal.setdefault(k, {})["sigma0"] = cal[k]["ay"] + cal[k]["by"] * pts[0][1]
                last_panel = k
    if x.get("type") == "s" and c == (0.5, 0.5, 0.5) and str(x.get("dashes")).startswith("[ 3.7"):
        # the R_e line is a full-height axvline whose stored vertices run beyond the panel (clipped when drawn); it is drawn right after
        # the sigma_0 line of its own panel, so it belongs to that panel; its x must lie inside that panel's x range
        pts = polyline(x)
        f = frames[last_panel]
        check(f[0] <= pts[0][0] <= f[2], f"R_e line of panel {names[last_panel]} lies inside the panel's x range")
        scal.setdefault(last_panel, {})["R_e"] = R_of(pts[0][0], f[0])
    if x.get("type") == "fs" and c == (0.5, 0.5, 0.5) and x.get("fill") == (0.5, 0.5, 0.5):
        r = x["rect"]
        for k, f in enumerate(frames):
            if in_frame(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2), f):
                scal.setdefault(k, {}).setdefault("grey_band_R_max", R_of(r.x1, f[0]))
check(all({"sigma0", "R_e"} <= set(scal.get(k, {})) for k in range(14)), "sigma_0 line and R_e line found in every panel")

# ---------------------------------------------------------------- data and model points
circles = []
for x in dr:
    if x.get("type") == "s" and color_of(x) == (0.0, 0.0, 0.0) and len(x["items"]) == 8 and x["items"][0][0] == "c":
        r = x["rect"]
        if 14 < r.width < 16 and 14 < r.height < 16:
            circles.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
squares = []
for x in dr:
    if color_of(x) == (0.86, 0.08, 0.24) and x.get("type") == "s" and x["items"][0][0] == "re":
        r = x["rect"]
        squares.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
caps_v = [((s[0]), (s[1] + s[3]) / 2) for s in black_lines if abs(s[0] - s[2]) < 0.01 and abs(abs(s[1] - s[3]) - 6) < 0.05]   # vertical caps: x error ends
caps_h = [((s[0] + s[2]) / 2, s[1]) for s in black_lines if abs(s[1] - s[3]) < 0.01 and abs(abs(s[0] - s[2]) - 6) < 0.05]     # horizontal caps: y error ends
rows_p = []
legend_words = [((w[0] + w[2]) / 2, (w[1] + w[3]) / 2) for w in words if w[4] in ("Model", "Data")]


def is_legend_marker(cx, cy):
    """the legend symbols sit just left of the words 'Model' and 'Data'"""
    return any(0 < wx - cx < 45 and abs(wy - cy) < 9 for wx, wy in legend_words)


circles = [c for c in circles if not is_legend_marker(*c)]
squares = [s for s in squares if not is_legend_marker(*s)]
for kind, pts_ in (("data", circles), ("model", squares)):
    for (cx, cy) in pts_:
        for k, f in enumerate(frames):
            if in_frame((cx, cy), f, 6.0):
                ay, by = cal[k]["ay"], cal[k]["by"]
                xe = sorted(p[0] for p in caps_v if abs(p[1] - cy) < 0.6 and abs(p[0] - cx) < 90)
                ye = sorted(p[1] for p in caps_h if abs(p[0] - cx) < 0.6 and abs(p[1] - cy) < 120)
                # keep the two caps nearest the centre on each side
                xl = [v for v in xe if v < cx - 0.5]; xr = [v for v in xe if v > cx + 0.5]
                yl = [v for v in ye if v < cy - 0.5]; yr = [v for v in ye if v > cy + 0.5]
                rows_p.append([names[k], kind, R_of(cx, f[0]), ay + by * cy,
                               R_of(max(xl), f[0]) if xl and kind == "data" else np.nan, R_of(min(xr), f[0]) if xr and kind == "data" else np.nan,
                               ay + by * max(yl) if yl and kind == "data" else np.nan, ay + by * min(yr) if yr and kind == "data" else np.nan])
                break
with open(os.path.join(HERE, "cristal_points.csv"), "w", newline="") as fo:
    w = csv.writer(fo); w.writerow(["id", "kind", "R_kpc", "V_kms", "R_lo_kpc", "R_hi_kpc", "V_hi_kms", "V_lo_kms"])
    for r in sorted(rows_p, key=lambda r: (r[0], r[1], r[2])):
        w.writerow([r[0], r[1]] + ["%.4f" % v if np.isfinite(v) else "" for v in r[2:]])

nd_ = sum(1 for r in rows_p if r[1] == "data"); nm_ = sum(1 for r in rows_p if r[1] == "model")
check(nd_ == nm_, f"{nd_} observed-profile markers and {nm_} model-cube markers on 14 panels (equal after removing the legend symbols)")

# ---------------------------------------------------------------- validation
dyn = {r["id"]: r for r in csv.DictReader(open(os.path.join(TAB, "cristal2025_dynamics.csv")))}
alias = {"10a": "10a-E"}


def curve_xy(k, cn):
    f = frames[k]
    a, b = (cal[k]["ar"], cal[k]["br"]) if cn == "f_DM" else (cal[k]["ay"], cal[k]["by"])
    xy = sorted((R_of(p[0], f[0]), a + b * p[1]) for p in curves[k][cn])
    return np.array([q[0] for q in xy]), np.array([q[1] for q in xy])


# (1) internal consistency, independent of the paper's table: f_DM(<R) drawn on the RIGHT axis must equal (V_DM/V_tot)^2 from the LEFT axis
worst_int = 0.0
for k in range(14):
    Rf, Ff = curve_xy(k, "f_DM"); Rd, Vd = curve_xy(k, "V_DM"); Rt, Vt = curve_xy(k, "V_tot")
    Rg = np.linspace(max(Rf.min(), Rd.min(), Rt.min()) + 0.05, 8.0, 40)
    fdm = np.interp(Rg, Rf, Ff); rat = (np.interp(Rg, Rd, Vd) / np.interp(Rg, Rt, Vt)) ** 2
    worst_int = max(worst_int, float(np.abs(fdm - rat).max()))
check(worst_int < 0.02, f"internal consistency: f_DM curve (right axis) equals (V_DM/V_tot)^2 (left axis) to within {worst_int:.4f} over 0.15-8 kpc for all 14 panels")
worst_q = 0.0
# (2) V_tot is the quadrature sum of V_bary and V_DM
for k in range(14):
    Rb, Vb = curve_xy(k, "V_bary"); Rd, Vd = curve_xy(k, "V_DM"); Rt, Vt = curve_xy(k, "V_tot")
    Rg = np.linspace(0.3, 8.0, 40)
    worst_q = max(worst_q, float(np.abs(np.sqrt(np.interp(Rg, Rb, Vb) ** 2 + np.interp(Rg, Rd, Vd) ** 2) / np.interp(Rg, Rt, Vt) - 1).max()))
check(worst_q < 0.02, f"V_tot equals the quadrature sum of V_bary and V_DM to within {worst_q*100:.2f}% over 0.3-8 kpc for all 14 panels")

# (3) figure versus the paper's dynamical-model table (posterior medians with errors); the figure shows one model per galaxy
rows_v = []; exact = []
for k in range(14):
    nm = names[k]; t = dyn[alias.get(nm, nm)]
    ts, tr, tf = float(t["sigma0_kms"]), float(t["Re_disk_kpc"]), float(t["fDM_Re"])
    sig, re_ = scal[k]["sigma0"], scal[k]["R_e"]
    Rf, Ff = curve_xy(k, "f_DM")
    f_at_fig = float(np.interp(re_, Rf, Ff)); f_at_tab = float(np.interp(tr, Rf, Ff))

    def nsig(fig, tab, eh, el):
        e = eh if fig > tab else el
        return (fig - tab) / e if e and np.isfinite(e) and e > 0 else np.nan
    zs = nsig(sig, ts, float(t["sigma0_kms_errhi"]), float(t["sigma0_kms_errlo"]))
    zr = nsig(re_, tr, float(t["Re_disk_kpc_errhi"]), float(t["Re_disk_kpc_errlo"]))
    zf = nsig(f_at_tab, tf, float(t["fDM_Re_errhi"]), float(t["fDM_Re_errlo"]))
    rows_v.append([nm, ts, sig, tr, re_, tf, f_at_fig, f_at_tab, zs, zr, zf])
    if abs(sig / ts - 1) < 0.005 and abs(re_ - tr) < 0.06:      # the table prints R_e to 0.1 kpc
        exact.append(nm)
with open(os.path.join(HERE, "cristal_validation.csv"), "w", newline="") as fo:
    w = csv.writer(fo)
    w.writerow(["id", "sigma0_table", "sigma0_figure", "Re_table_kpc", "Re_figure_line_kpc", "fDM_Re_table", "fDM_figure_at_its_own_Re", "fDM_figure_at_table_Re",
                "sigma0_dev_in_table_sigmas", "Re_dev_in_table_sigmas", "fDM_dev_in_table_sigmas"])
    for r in rows_v:
        w.writerow([r[0]] + ["%.3f" % v if np.isfinite(v) else "" for v in r[1:]])
check(len(exact) >= 5, f"figure and table agree exactly (sigma_0 within 0.5%, R_e within the table's 0.1 kpc rounding) for {len(exact)} disks: {exact}")
dev = [r for r in rows_v if not (r[0] in exact)]
log("figure vs table for the other %d disks (deviation in units of the table's quoted 1-sigma): " % len(dev) + "; ".join(
    f"{r[0]}: sigma0 {r[8]:+.1f}, R_e {r[9]:+.1f}, fDM {r[10]:+.1f}" for r in dev))
log("the figure draws one model per galaxy while the table lists posterior medians, so a difference is expected; a difference beyond the quoted error "
    "(|deviation| > 1) means the drawn model and the tabulated median disagree")

# ---------------------------------------------------------------- outer summary at the outermost observed marker and at the table's R_out
A0 = 1.2e-10; KPC = 3.0857e19
outer = []
for k in range(14):
    nm = names[k]; t = dyn[alias.get(nm, nm)]
    dpts = [r for r in rows_p if r[0] == nm and r[1] == "data"]
    Rdata = max(r[2] for r in dpts)
    Rtab = float(t["Rout_over_Re"]) * float(t["Re_disk_kpc"])
    for label, R in (("outermost_data_marker", Rdata), ("table_Rout", Rtab)):
        Rb, Vb = curve_xy(k, "V_bary"); Rd, Vd = curve_xy(k, "V_DM"); Rt, Vt = curve_xy(k, "V_tot")
        vb, vd, vt = float(np.interp(R, Rb, Vb)), float(np.interp(R, Rd, Vd)), float(np.interp(R, Rt, Vt))
        gb = (vb * 1e3) ** 2 / (R * KPC) / A0; gt = (vt * 1e3) ** 2 / (R * KPC) / A0
        outer.append([nm, label, R, vb, vd, vt, gb, gt, float(t["sigma0_kms"]), float(t["Vrot_Re_kms"])])
with open(os.path.join(HERE, "cristal_outer_summary.csv"), "w", newline="") as fo:
    w = csv.writer(fo)
    w.writerow(["id", "radius_definition", "R_kpc", "Vbary_kms", "VDM_kms", "Vtot_kms", "gbar_over_a0", "gtot_over_a0", "sigma0_table_kms", "Vrot_Re_table_kms"])
    for r in outer:
        w.writerow([r[0], r[1]] + ["%.3f" % v for v in r[2:]])
og = [r for r in outer if r[1] == "outermost_data_marker"]
log("g_bar / a0 = V_bary^2 / R / a0 at the outermost OBSERVED marker (model curve, 14 disks): " + ", ".join(f"{r[0]} {r[6]:.2f}" for r in og))
log("g_tot / a0 = V_tot^2 / R / a0 there (asymmetric-drift-corrected model circular velocity): " + ", ".join(f"{r[0]} {r[7]:.2f}" for r in og))
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
