#!/usr/bin/env python3
"""Extract the observed Halpha rotation curves v_obs(R) of the 22 KURVS-CDFS galaxies from the paper's VECTOR figures (arXiv:2305.04382, Puglisi+2023).

Same four figure PDFs and method as ../kurvs_sigma_profiles/extract.py (byte-for-byte copies in ../kurvs_sigma_profiles/raw_small/, sha256 in its manifest.json):
in each row the LEFT panel is "Rotation curve" (v_obs [km/s] vs Radius [kpc], along the kinematic major axis, plotted so that the velocity gradient is positive).
Extracted per galaxy: every marker (blue = kept, white = clipped by the authors), its error bar, the best-fit exponential-disc (Freeman) model curve as a polyline, and the R50 dotted verticals.
The plotted velocity is the OBSERVED line-of-sight velocity: not inclination-corrected, not beam-smearing corrected, no pressure-support correction.
Controls (see checks.txt): the y-axis is calibrated from the panel's own tick labels (sign from position relative to the '0' label); the model curve is compared with the tabulated
V at the last point (Table B1 column 3, inclination-corrected) after dividing by sin i_SFR from Table 1.  No physics is computed here.
"""
import csv, hashlib, json, math, os, re
import fitz
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.join(HERE, "..")
SRC = os.path.join(TAB, "kurvs_sigma_profiles", "raw_small") + "/"
PDFS = ["KURVS_11_to_16_vsigma_sorted_dataset.pdf", "KURVS_10_to_8_vsigma_sorted_dataset.pdf",
        "KURVS_13_to_6_vsigma_sorted_dataset.pdf", "KURVS_19_to_20_vsigma_sorted_dataset.pdf"]
LOG = []


def check(c, m):
    LOG.append(("PASS  " if c else "FAIL  ") + m); print(LOG[-1])
    if not c:
        open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n"); raise SystemExit(m)


def rnd(c):
    return None if c is None else tuple(round(v, 2) for v in c)


BLUE, WHITE = (0.27, 0.51, 0.71), (1.0, 1.0, 1.0)
pts_out, curve_out, ref_out, cal_out = [], [], [], []
for pdf in PDFS:
    page = fitz.open(SRC + pdf)[0]
    dr = page.get_drawings(); words = page.get_text("words")
    frames = []
    for x in dr:
        r = x["rect"]
        if x.get("color") is None and rnd(x.get("fill")) == (1, 1, 1) and 250 < r.width < 330 and 100 < r.height < 170:
            frames.append((r.x0, r.y0, r.x1, r.y1))
    frames = sorted(set((round(a, 1), round(b, 1), round(c, 1), round(d, 1)) for a, b, c, d in frames), key=lambda f: (round(f[1]), f[0]))
    uniq = []
    for f in frames:
        if not any(abs(f[0] - g[0]) < 8 and abs(f[1] - g[1]) < 8 for g in uniq):
            uniq.append(f)
    frames = uniq
    ys = sorted(set(round(f[1] / 20) for f in frames))
    rc = [min([f for f in frames if round(f[1] / 20) == y], key=lambda f: f[0]) for y in ys]        # leftmost of each row's pair = rotation curve
    titles = []
    for w in words:
        if w[4] in ("cdfs", "GS4"):
            same = sorted([ww for ww in words if abs(ww[1] - w[1]) < 1.5 and w[0] - 40 < ww[0] < w[0] + 90], key=lambda ww: ww[0])
            txt = [ww[4] for ww in same]; i = txt.index(w[4]); titles.append((w[1], int(txt[i - 1])))
    check(len(rc) == len(titles), f"{pdf}: {len(rc)} rotation-curve panels = {len(titles)} titles")

    fb = rc[-1]
    maj = []
    for x in dr:
        if rnd(x.get("color")) == (0, 0, 0) and abs((x.get("width") or 0) - 0.8) < 1e-6 and x.get("fill") is not None:
            for it in x["items"]:
                if it[0] == "l" and abs(it[1].x - it[2].x) < 0.01 and abs(abs(it[1].y - it[2].y) - 3.5) < 0.2:
                    if (abs(min(it[1].y, it[2].y) - fb[3]) < 4 or abs(max(it[1].y, it[2].y) - fb[3]) < 4) and fb[0] - 1 <= it[1].x <= fb[2] + 1:
                        maj.append(it[1].x)
    maj = sorted(set(round(v, 2) for v in maj))
    lab = [w for w in words if fb[0] - 8 <= (w[0] + w[2]) / 2 <= fb[2] + 8 and fb[3] < (w[1] + w[3]) / 2 < fb[3] + 35 and re.fullmatch(r"\d+", w[4])]
    check(len(maj) >= 4 and len(lab) == len(maj), f"{pdf}: RC x major ticks {len(maj)} = labels {len(lab)}")
    zero = [w for w in lab if w[4] == "0"]; check(len(zero) == 1, f"{pdf}: one '0' x label")
    x0 = (zero[0][0] + zero[0][2]) / 2
    xv, xp = [], []
    for w in lab:
        cx = (w[0] + w[2]) / 2; t = min(maj, key=lambda m: abs(m - cx)); xv.append((-1 if cx < x0 - 2 else 1) * float(w[4])); xp.append(t)
    A = np.polyfit(xp, xv, 1); rx = np.array(xv) - np.polyval(A, xp)
    check(np.max(np.abs(rx)) < 0.05, f"{pdf}: RC x calibration residual {np.max(np.abs(rx)):.3f} kpc over {len(xv)} ticks")
    cal_out.append(dict(pdf=pdf, axis="x", slope=A[0], intercept=A[1], n_ticks=len(xv), max_resid=float(np.max(np.abs(rx)))))
    X = lambda px: float(np.polyval(A, px))

    for k, f in enumerate(rc):
        kid = [t for t in titles if f[1] - 12 < t[0] < f[3]]; check(len(kid) == 1, f"{pdf}: row {k} title")
        kurvs_id = kid[0][1]
        yt = []
        for x in dr:
            if rnd(x.get("color")) == (0, 0, 0) and abs((x.get("width") or 0) - 0.8) < 1e-6 and x.get("fill") is not None:
                for it in x["items"]:
                    if it[0] == "l" and abs(it[1].y - it[2].y) < 0.01 and abs(abs(it[1].x - it[2].x) - 3.5) < 0.2:
                        if abs(min(it[1].x, it[2].x) - f[0]) < 1 and f[1] - 1 <= it[1].y <= f[3] + 1:
                            yt.append(it[1].y)
        yt = sorted(set(round(v, 2) for v in yt))
        yl = [w for w in words if f[0] - 34 <= w[0] and w[2] <= f[0] - 1 and f[1] - 4 < (w[1] + w[3]) / 2 < f[3] + 4 and re.fullmatch(r"\d+", w[4])]
        check(len(yt) == len(yl) and len(yt) >= 3, f"KURVS-{kurvs_id}: RC y ticks {len(yt)} = labels {len(yl)}")
        z0 = [w for w in yl if w[4] == "0"]; check(len(z0) == 1, f"KURVS-{kurvs_id}: one '0' y label")
        y0c = (z0[0][1] + z0[0][3]) / 2
        yv, yp = [], []
        for w in yl:
            cy = (w[1] + w[3]) / 2; t = min(yt, key=lambda m: abs(m - cy))
            sign = 0 if w[4] == "0" else (1 if cy < y0c - 2 else -1)          # above the '0' label = positive
            yv.append(sign * float(w[4])); yp.append(t)
        B = np.polyfit(yp, yv, 1); ry = np.array(yv) - np.polyval(B, yp)
        check(np.max(np.abs(ry)) < 0.6, f"KURVS-{kurvs_id}: RC y calibration residual {np.max(np.abs(ry)):.3f} km/s over {len(yv)} ticks")
        cal_out.append(dict(pdf=pdf, axis=f"y KURVS-{kurvs_id}", slope=B[0], intercept=B[1], n_ticks=len(yv), max_resid=float(np.max(np.abs(ry)))))
        Y = lambda py: float(np.polyval(B, py))

        def inside(r, pad=1.0):
            return r.x0 >= f[0] - pad and r.x1 <= f[2] + pad and r.y0 >= f[1] - pad and r.y1 <= f[3] + pad

        marks, bars, vl, curve = [], [], [], None
        for x in dr:
            r = x["rect"]; col, fil, w_ = rnd(x.get("color")), rnd(x.get("fill")), round(x.get("width") or 0, 2); kinds = set(i[0] for i in x["items"])
            if kinds == {"l"} and col is not None and col[0] == col[1] == col[2] and 0.35 < col[0] < 0.45 and w_ == 2.0 and len(x["items"]) > 20:
                if f[1] - 60 <= r.y0 and r.y1 <= f[3] + 60 and r.x0 <= f[2] and r.x1 >= f[0]:                 # the model polyline of this row (extends beyond the frame)
                    if abs((r.y0 + r.y1) / 2 - (f[1] + f[3]) / 2) < 110: curve = x
                continue
            if kinds == {"l"} and col == (0, 0, 0) and fil is None and w_ == 1.5:
                if f[0] - 1 <= r.x0 and r.x1 <= f[2] + 1 and r.y1 >= f[1] - 1 and r.y0 <= f[3] + 1:
                    for it in x["items"]:
                        if abs(it[1].x - it[2].x) < 0.01: bars.append((it[1].x, min(it[1].y, it[2].y), max(it[1].y, it[2].y)))
                continue
            if not inside(r): continue
            if kinds == {"c"} and col == (0, 0, 0) and fil in (BLUE, WHITE) and 5 < r.width < 8:
                marks.append(dict(x=(r.x0 + r.x1) / 2, y=(r.y0 + r.y1) / 2, clipped=int(fil == WHITE)))
            elif kinds == {"l"} and col is not None and col[0] == col[1] == col[2] and w_ == 3.0 and abs(col[0] - 0.75) < 0.02:
                vl.append(x["items"][0][1].x)
        check(len(marks) >= 15, f"KURVS-{kurvs_id}: {len(marks)} RC markers")
        check(curve is not None, f"KURVS-{kurvs_id}: model polyline found")
        marks.sort(key=lambda m: m["x"]); used = set()
        for m in marks:
            cand = [(abs(b[0] - m["x"]), i) for i, b in enumerate(bars) if abs(b[0] - m["x"]) < 0.3 and i not in used]
            if cand:
                i = min(cand)[1]; used.add(i); m["bar"] = (bars[i][1], bars[i][2])
            else:
                m["bar"] = None
        for m in marks:
            v = Y(m["y"])
            if m["bar"] is None: up = lo = None; edge = beyond = 0
            else:
                up, lo = Y(m["bar"][0]) - v, v - Y(m["bar"][1])
                edge = int(m["bar"][0] <= f[1] + 0.6 or m["bar"][1] >= f[3] - 0.6); beyond = int(m["bar"][0] < f[1] - 0.6 or m["bar"][1] > f[3] + 0.6)
            pts_out.append(dict(kurvs_id=kurvs_id, R_kpc=round(X(m["x"]), 3), v_obs_kms=round(v, 2), err_up_kms="" if up is None else round(up, 2), err_lo_kms="" if lo is None else round(lo, 2),
                                clipped_white_marker=m["clipped"], errbar_touches_axis_edge=edge, errbar_extends_beyond_axis=beyond, has_errbar=int(m["bar"] is not None), source_pdf=pdf))
        vs = []
        for it in curve["items"]:
            vs.append((it[1].x, it[1].y))
        vs.append((curve["items"][-1][2].x, curve["items"][-1][2].y))
        vs = [(X(px), Y(py)) for px, py in vs if f[0] - 0.5 <= px <= f[2] + 0.5]
        check(len(vs) >= 20, f"KURVS-{kurvs_id}: {len(vs)} model-curve vertices inside the panel")
        for R, v in vs: curve_out.append(dict(kurvs_id=kurvs_id, R_kpc=round(R, 3), v_model_obs_kms=round(v, 2), source_pdf=pdf))
        for v in vl: ref_out.append(dict(kurvs_id=kurvs_id, kind="R50_dotted_vertical_kpc", value=round(X(v), 3)))
        print(f"      KURVS-{kurvs_id}: {len(marks)} markers ({sum(m['clipped'] for m in marks)} clipped), {sum(m['bar'] is None for m in marks)} without a bar, model vertices {len(vs)}")

ids = sorted(set(r["kurvs_id"] for r in pts_out)); check(ids == list(range(1, 23)), f"all 22 KURVS ids present (got {ids})")

# ---------------------------------------------------------------- control against the paper's tables
vel = {int(r["kurvs_id"]): r for r in csv.DictReader(open(os.path.join(TAB, "kurvs2023_velocities_at_radii.csv")))}
inc = {int(r["kurvs_id"]): float(r["inc_sfr_deg"]) for r in csv.DictReader(open(os.path.join(TAB, "kurvs2023_integrated.csv")))}
rows = []
for kid in range(1, 23):
    cv = [(c["R_kpc"], c["v_model_obs_kms"]) for c in curve_out if c["kurvs_id"] == kid]
    R, V = np.array([c[0] for c in cv]), np.array([c[1] for c in cv])
    Rmax = float(vel[kid]["R_halpha_max_kpc"]); v_tab = float(vel[kid]["v_at_last_point_kms"]); e_tab = float(vel[kid]["e_v_last"])
    # the tabulated "velocity at the maximal extent" is positive; take the model magnitude on the side that is positive, at |R| = Rmax
    vpos = float(np.interp(Rmax, R, V)) if R.min() <= Rmax <= R.max() else float("nan")
    vneg = float(np.interp(-Rmax, R, V)) if R.min() <= -Rmax <= R.max() else float("nan")
    s = math.sin(math.radians(inc[kid]))
    rows.append(dict(kurvs_id=kid, R_max_table_kpc=Rmax, v_table_last_kms=v_tab, e_v_table=e_tab, inc_sfr_deg=inc[kid], model_v_at_plus_Rmax_obs=round(vpos, 2), model_v_at_minus_Rmax_obs=round(vneg, 2),
                     model_over_sini_plus=round(vpos / s, 2), model_over_sini_minus=round(abs(vneg) / s, 2)))
with open(os.path.join(HERE, "kurvs_rc_control_vs_table.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
ok = [r for r in rows if not math.isnan(r["model_over_sini_plus"])]
ratio = [max(r["model_over_sini_plus"], r["model_over_sini_minus"]) / r["v_table_last_kms"] for r in ok if r["v_table_last_kms"] > 15 and not math.isnan(r["model_over_sini_minus"])]
LOG.append(f"control vs Table B1 col 3: model(R_max)/sin i / tabulated V(R_max): median {np.median(ratio):.3f}, min {min(ratio):.3f}, max {max(ratio):.3f} over {len(ratio)} galaxies with V > 15 km/s"); print(LOG[-1])

fields = ["kurvs_id", "R_kpc", "v_obs_kms", "err_up_kms", "err_lo_kms", "clipped_white_marker", "errbar_touches_axis_edge", "errbar_extends_beyond_axis", "has_errbar", "source_pdf"]
pts_out.sort(key=lambda r: (r["kurvs_id"], r["R_kpc"]))
with open(os.path.join(HERE, "kurvs_rc_points.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(pts_out)
with open(os.path.join(HERE, "kurvs_rc_model_curves.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["kurvs_id", "R_kpc", "v_model_obs_kms", "source_pdf"]); w.writeheader(); w.writerows(sorted(curve_out, key=lambda r: (r["kurvs_id"], r["R_kpc"])))
with open(os.path.join(HERE, "kurvs_rc_reference_lines.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["kurvs_id", "kind", "value"]); w.writeheader(); w.writerows(sorted(ref_out, key=lambda r: (r["kurvs_id"], r["kind"], r["value"])))
json.dump(dict(calibrations=cal_out, source_pdfs="see ../kurvs_sigma_profiles/manifest.json"), open(os.path.join(HERE, "manifest.json"), "w"), indent=1, default=float)
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axs = plt.subplots(5, 5, figsize=(20, 16)); axs = axs.ravel()
    for kid in range(1, 23):
        a = axs[kid - 1]
        for r in [p for p in pts_out if p["kurvs_id"] == kid]:
            a.errorbar(r["R_kpc"], r["v_obs_kms"], yerr=[[r["err_lo_kms"] or 0], [r["err_up_kms"] or 0]], fmt="o", ms=3, color="k", mfc="w" if r["clipped_white_marker"] else "steelblue", lw=0.8)
        c = [x for x in curve_out if x["kurvs_id"] == kid]; a.plot([x["R_kpc"] for x in c], [x["v_model_obs_kms"] for x in c], color="grey"); a.set_title(f"KURVS-{kid}", fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "qa_replot.png"), dpi=60)
except Exception as ex:
    LOG.append(f"QA plot skipped: {ex}")
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
