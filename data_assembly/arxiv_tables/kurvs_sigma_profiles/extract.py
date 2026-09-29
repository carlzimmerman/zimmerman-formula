#!/usr/bin/env python3
"""Extract the observed H-alpha velocity-dispersion profiles sigma_obs(R) of the 22 KURVS-CDFS galaxies from the paper's VECTOR figures.

Source: the four appendix/figure PDFs of arXiv:2305.04382 (Puglisi+2023), byte-for-byte in raw_small/ (sha256 in manifest.json;
originals in ~/new_physics/_external_data/arxiv_src/2305.04382/).  Each page has rows of panels; the rightmost panel of each row is
"Dispersion profile": sigma_obs [km/s] against Radius [kpc], extracted by the authors from the sigma_obs map ALONG THE KINEMATIC MAJOR AXIS.
The PDFs store every marker, error bar, sigma_0 line and tick as exact vector geometry and all tick labels as text, so nothing is read by eye:
the axes are calibrated from the major ticks and their labels and each marker / error bar is converted directly.
Paper caption (arXiv TeX, quoted in README): white-filled circles = pixels clipped for sky-line contamination or broad components;
dotted vertical lines = HST half-light radius R_50; horizontal dotted line = OBSERVED sigma_0, solid line = beam-smearing-CORRECTED sigma_0,
grey band = 1-sigma error of sigma_0.  The plotted sigma_obs profile itself is the OBSERVED profile (not beam-smearing corrected).
Validation: the corrected sigma_0 line and its band are compared with the paper's Table (kurvs2023_kinematics.csv); the outermost radius is
compared with R_Halpha,max of the same table.  No g, V_c, pressure-support or test statistic is computed here.
Usage: python3 extract.py
"""
import csv, hashlib, json, os, re
import fitz
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.join(HERE, "..")
SRC = os.path.join(HERE, "raw_small") + "/"      # byte-for-byte copies of the arXiv source figures
PDFS = ["KURVS_11_to_16_vsigma_sorted_dataset.pdf", "KURVS_10_to_8_vsigma_sorted_dataset.pdf",
        "KURVS_13_to_6_vsigma_sorted_dataset.pdf", "KURVS_19_to_20_vsigma_sorted_dataset.pdf"]
LOG = []


def log(m):
    print(m); LOG.append(m)


def check(c, m):
    log(("PASS  " if c else "FAIL  ") + m)
    if not c:
        open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
        raise SystemExit("check failed: " + m)


def rnd(c):
    return None if c is None else tuple(round(v, 2) for v in c)


BLUE = (0.27, 0.51, 0.71)
WHITE = (1.0, 1.0, 1.0)
rows_out, line_out, cal_out = [], [], []
manifest = {}

for pdf in PDFS:
    path = SRC + pdf
    manifest[pdf] = hashlib.sha256(open(path, "rb").read()).hexdigest()
    page = fitz.open(path)[0]
    dr = page.get_drawings()
    words = page.get_text("words")

    # ------------------------------------------------ panel frames (one closed polyline per panel, black 0.8, no fill)
    frames = []
    for x in dr:
        r = x["rect"]
        if x.get("color") is None and rnd(x.get("fill")) == (1, 1, 1) and 250 < r.width < 330 and 100 < r.height < 170:
            frames.append((r.x0, r.y0, r.x1, r.y1))          # white panel background of each plot
    frames = sorted(set((round(a, 1), round(b, 1), round(c, 1), round(d, 1)) for a, b, c, d in frames), key=lambda f: (round(f[1]), f[0]))
    # merge the two near-identical backgrounds per panel (RC 309 wide, sigma 312 wide): keep one per (row, column) by x0
    uniq = []
    for f in frames:
        if not any(abs(f[0] - g[0]) < 8 and abs(f[1] - g[1]) < 8 for g in uniq):
            uniq.append(f)
    frames = uniq
    ys = sorted(set(round(f[1] / 20) for f in frames))
    check(len(frames) == 2 * len(ys), f"{pdf}: {len(frames)} frames = 2 per row over {len(ys)} rows")
    sig = [max([f for f in frames if round(f[1] / 20) == y], key=lambda f: f[0]) for y in ys]   # rightmost = dispersion profile

    # ------------------------------------------------ titles: "<n> cdfs <id>"
    titles = []
    for w in words:
        if w[4] in ("cdfs", "GS4"):
            same = sorted([ww for ww in words if abs(ww[1] - w[1]) < 1.5 and w[0] - 40 < ww[0] < w[0] + 90], key=lambda ww: ww[0])
            txt = [ww[4] for ww in same]
            i = txt.index(w[4])
            titles.append((w[1], int(txt[i - 1]), int(txt[i + 1]), w[4]))
    check(len(titles) == len(sig), f"{pdf}: one title per row ({len(titles)})")

    # ------------------------------------------------ x calibration from the bottom row: major ticks + labels
    fb = sig[-1]
    maj = []
    for x in dr:
        if rnd(x.get("color")) == (0, 0, 0) and abs((x.get("width") or 0) - 0.8) < 1e-6 and x.get("fill") is not None:
            for it in x["items"]:
                if it[0] == "l" and abs(it[1].x - it[2].x) < 0.01 and abs(abs(it[1].y - it[2].y) - 3.5) < 0.2:
                    if abs(min(it[1].y, it[2].y) - fb[3]) < 4 or abs(max(it[1].y, it[2].y) - fb[3]) < 4:
                        maj.append(it[1].x)
    maj = sorted(set(round(v, 2) for v in maj if fb[0] - 1 <= v <= fb[2] + 1))
    lab = [w for w in words if fb[0] - 8 <= (w[0] + w[2]) / 2 <= fb[2] + 8 and fb[3] < (w[1] + w[3]) / 2 < fb[3] + 35 and re.fullmatch(r"\d+", w[4])]
    check(len(maj) >= 4 and len(lab) == len(maj), f"{pdf}: x major ticks {len(maj)} = tick labels {len(lab)}")
    zero = [w for w in lab if w[4] == "0"]
    check(len(zero) == 1, f"{pdf}: exactly one '0' x label")
    x0lab = (zero[0][0] + zero[0][2]) / 2
    xv, xp = [], []
    for w in lab:
        cx = (w[0] + w[2]) / 2
        t = min(maj, key=lambda m: abs(m - cx))
        sgn = -1 if cx < x0lab - 2 else 1
        xv.append(sgn * float(w[4])); xp.append(t)
    A = np.polyfit(xp, xv, 1)
    res = np.array(xv) - np.polyval(A, xp)
    check(np.max(np.abs(res)) < 0.05 and abs(np.polyval(A, x0lab)) < 0.3, f"{pdf}: x calibration residual <= {np.max(np.abs(res)):.3f} kpc, {len(xv)} ticks")
    cal_out.append(dict(pdf=pdf, axis="x", slope_kpc_per_pt=A[0], intercept=A[1], n_ticks=len(xv), max_resid=float(np.max(np.abs(res)))))

    def X(px):
        return float(np.polyval(A, px))

    for k, f in enumerate(sig):
        kid = [t for t in titles if f[1] - 12 < t[0] < f[3]]
        check(len(kid) == 1, f"{pdf}: row {k} has one title")
        kurvs_id, cdfs_id = kid[0][1], f"{kid[0][3]}_{kid[0][2]}"

        # ---- y calibration from left major ticks and labels of this panel
        yt = []
        for x in dr:
            if rnd(x.get("color")) == (0, 0, 0) and abs((x.get("width") or 0) - 0.8) < 1e-6 and x.get("fill") is not None:
                for it in x["items"]:
                    if it[0] == "l" and abs(it[1].y - it[2].y) < 0.01 and abs(abs(it[1].x - it[2].x) - 3.5) < 0.2:
                        if abs(min(it[1].x, it[2].x) - f[0]) < 1 and f[1] - 1 <= it[1].y <= f[3] + 1:
                            yt.append(it[1].y)
        yt = sorted(set(round(v, 2) for v in yt))
        yl = [w for w in words if f[0] - 45 < w[2] <= f[0] - 1 and f[1] - 4 < (w[1] + w[3]) / 2 < f[3] + 4 and re.fullmatch(r"\d+", w[4])]
        check(len(yt) == len(yl) and len(yt) >= 2, f"{pdf} KURVS-{kurvs_id}: y major ticks {len(yt)} = labels {len(yl)}")
        yv, yp = [], []
        for w in yl:
            cy = (w[1] + w[3]) / 2
            t = min(yt, key=lambda m: abs(m - cy))
            yv.append(float(w[4])); yp.append(t)
        B = np.polyfit(yp, yv, 1)
        ry = np.array(yv) - np.polyval(B, yp)
        check(np.max(np.abs(ry)) < 0.6, f"{pdf} KURVS-{kurvs_id}: y calibration residual {np.max(np.abs(ry)):.3f} km/s over {len(yv)} ticks")
        cal_out.append(dict(pdf=pdf, axis=f"y KURVS-{kurvs_id}", slope_kms_per_pt=B[0], intercept=B[1], n_ticks=len(yv), max_resid=float(np.max(np.abs(ry)))))

        def Y(py):
            return float(np.polyval(B, py))

        def inside(r, pad=1.0):
            return r.x0 >= f[0] - pad and r.x1 <= f[2] + pad and r.y0 >= f[1] - pad and r.y1 <= f[3] + pad

        # ---- markers (blue = kept, white = clipped) and error bars
        marks, bars, hl, vl, band = [], [], [], [], []
        for x in dr:
            r = x["rect"]
            col, fil, w_ = rnd(x.get("color")), rnd(x.get("fill")), round(x.get("width") or 0, 2)
            kinds = set(i[0] for i in x["items"])
            is_bar = kinds == {"l"} and col == (0, 0, 0) and fil is None and w_ == 1.5
            if is_bar:
                if not (f[0] - 1 <= r.x0 and r.x1 <= f[2] + 1 and r.y1 >= f[1] - 1 and r.y0 <= f[3] + 1):
                    continue
            elif not inside(r):
                continue
            if kinds == {"c"} and col == (0, 0, 0) and fil in (BLUE, WHITE) and 5 < r.width < 8:
                marks.append(dict(x=(r.x0 + r.x1) / 2, y=(r.y0 + r.y1) / 2, clipped=int(fil == WHITE)))
            elif kinds == {"l"} and col == (0, 0, 0) and fil is None and w_ == 1.5:
                for it in x["items"]:
                    if abs(it[1].x - it[2].x) < 0.01:
                        bars.append((it[1].x, min(it[1].y, it[2].y), max(it[1].y, it[2].y)))
            elif kinds == {"l"} and col is not None and col[0] == col[1] == col[2] and 0.35 < col[0] < 0.45 and w_ == 1.5:
                dash = "dotted" if x.get("dashes") and "5.55" in x["dashes"] else "solid"
                for it in x["items"]:
                    hl.append((dash, it[1].y))
            elif kinds == {"l"} and col == (0.5, 0.5, 0.5) and fil == (0.5, 0.5, 0.5) and w_ == 1.0:
                band.append((r.y0, r.y1))
            elif kinds == {"l"} and col is not None and col[0] == col[1] == col[2] and w_ == 3.0 and abs(col[0] - 0.75) < 0.02:
                vl.append(x["items"][0][1].x)
        check(len(marks) >= 15, f"{pdf} KURVS-{kurvs_id}: {len(marks)} markers")
        check(len(hl) == 2 and len(band) == 1, f"{pdf} KURVS-{kurvs_id}: two sigma_0 lines and one band ({hl}, {len(band)})")

        marks.sort(key=lambda m: m["x"])
        # every error bar belongs to the marker at the same x
        used = set()
        for m in marks:
            cand = [(abs(b[0] - m["x"]), i) for i, b in enumerate(bars) if abs(b[0] - m["x"]) < 0.3 and i not in used]
            if cand:
                i = min(cand)[1]; used.add(i); b = bars[i]
                m["bar"] = (b[1], b[2])
            else:
                m["bar"] = None
        # a marker is at the panel edge if its bar touches the frame (clipped by the axis range)
        for m in marks:
            sig_v = Y(m["y"])
            if m["bar"] is None:
                lo = hi = None; edge = 0; beyond = 0
            else:
                hi_v, lo_v = Y(m["bar"][0]), Y(m["bar"][1])     # smaller pixel-y is larger value
                hi, lo = hi_v - sig_v, sig_v - lo_v
                edge = int(m["bar"][0] <= f[1] + 0.6 or m["bar"][1] >= f[3] - 0.6)
                beyond = int(m["bar"][0] < f[1] - 0.6 or m["bar"][1] > f[3] + 0.6)
            rows_out.append(dict(kurvs_id=kurvs_id, cdfs_id=cdfs_id, R_kpc=round(X(m["x"]), 3), sigma_obs_kms=round(sig_v, 2),
                                 err_up_kms="" if hi is None else round(hi, 2), err_lo_kms="" if lo is None else round(lo, 2),
                                 clipped_white_marker=m["clipped"], errbar_touches_axis_edge=edge, errbar_extends_beyond_axis=beyond, has_errbar=int(m["bar"] is not None),
                                 source_pdf=pdf))
        for d_, py in hl:
            line_out.append(dict(kurvs_id=kurvs_id, cdfs_id=cdfs_id, kind=f"sigma0_{'observed' if d_ == 'dotted' else 'beam_corrected'}_line", value_kms=round(Y(py), 2), source_pdf=pdf))
        line_out.append(dict(kurvs_id=kurvs_id, cdfs_id=cdfs_id, kind="sigma0_band_lo", value_kms=round(Y(band[0][1]), 2), source_pdf=pdf))
        line_out.append(dict(kurvs_id=kurvs_id, cdfs_id=cdfs_id, kind="sigma0_band_hi", value_kms=round(Y(band[0][0]), 2), source_pdf=pdf))
        for v in vl:
            line_out.append(dict(kurvs_id=kurvs_id, cdfs_id=cdfs_id, kind="R50_dotted_vertical_kpc", value_kms=round(X(v), 3), source_pdf=pdf))
        log(f"      KURVS-{kurvs_id} ({cdfs_id}): {len(marks)} markers, {sum(m['clipped'] for m in marks)} clipped, {sum(m['bar'] is None for m in marks)} without a bar")

integ = {int(r["kurvs_id"]): r["candels_id"] for r in csv.DictReader(open(os.path.join(TAB, "kurvs2023_integrated.csv")))}
idm = {r["kurvs_id"]: r["cdfs_id"] for r in rows_out}
check(all(idm[k].lower() == integ[k].lower() or idm[k].replace("GS4_", "gs4_").lower() == integ[k].lower() for k in idm), "figure titles' catalogue IDs match kurvs2023_integrated.csv for all 22")
ids = sorted(set(r["kurvs_id"] for r in rows_out))
check(ids == list(range(1, 23)), f"all 22 KURVS ids present (got {ids})")

# ---------------------------------------------------------------- validation against the paper's own table
kin = list(csv.DictReader(open(os.path.join(TAB, "kurvs2023_kinematics.csv"))))
log(f"      kurvs2023_kinematics.csv columns: {list(kin[0].keys())}")
tab = {int(r[[k for k in r if k.lower().startswith("kurvs") or k.lower() == "id"][0]]): r for r in kin}
sig_col = [k for k in kin[0] if k.lower().replace("_", "").startswith("sigma0") and "err" not in k.lower() and "lo" not in k.lower() and "hi" not in k.lower()]
rmax_col = [k for k in kin[0] if "max" in k.lower() and "ha" in k.lower().replace("α", "a")]
log(f"      table columns used: sigma0={sig_col} Rmax={rmax_col}")
worst = 0.0
for kid in range(1, 23):
    lines = {r["kind"]: r["value_kms"] for r in line_out if r["kurvs_id"] == kid}
    if sig_col and kid in tab:
        try:
            t = float(tab[kid][sig_col[0]])
            worst = max(worst, abs(lines["sigma0_beam_corrected_line"] - t))
        except (ValueError, KeyError):
            pass
check(worst < 1.5, f"corrected sigma_0 line agrees with the paper's Table sigma_0 within {worst:.2f} km/s for all rows that parse")

fields = ["kurvs_id", "cdfs_id", "R_kpc", "sigma_obs_kms", "err_up_kms", "err_lo_kms", "clipped_white_marker", "errbar_touches_axis_edge", "errbar_extends_beyond_axis", "has_errbar", "source_pdf"]
rows_out.sort(key=lambda r: (r["kurvs_id"], r["R_kpc"]))
with open(os.path.join(HERE, "kurvs_sigma_profiles.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows_out)
with open(os.path.join(HERE, "kurvs_sigma_reference_lines.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["kurvs_id", "cdfs_id", "kind", "value_kms", "source_pdf"]); w.writeheader()
    w.writerows(sorted(line_out, key=lambda r: (r["kurvs_id"], r["kind"])))
json.dump(dict(source_pdf_sha256=manifest, calibrations=cal_out), open(os.path.join(HERE, "manifest.json"), "w"), indent=1, default=float)
log(f"wrote {len(rows_out)} profile points for 22 galaxies")
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")

# ---------------------------------------------------------------- per-galaxy coverage summary (radii only) + band check + QA plot
summ = []
bandbad = 0.0
for kid in range(1, 23):
    pts = [r for r in rows_out if r["kurvs_id"] == kid]
    keep = [r for r in pts if not r["clipped_white_marker"]]
    pos = [r["R_kpc"] for r in keep if r["R_kpc"] > 0]
    neg = [-r["R_kpc"] for r in keep if r["R_kpc"] < 0]
    lines = {r["kind"]: r["value_kms"] for r in line_out if r["kurvs_id"] == kid}
    t = tab[kid]
    try:
        e = float(t["e_sigma0"])
        bandbad = max(bandbad, abs((lines["sigma0_band_hi"] - lines["sigma0_band_lo"]) / 2 - e))
    except ValueError:
        pass
    summ.append(dict(kurvs_id=kid, cdfs_id=pts[0]["cdfs_id"], n_points=len(pts), n_clipped_white=len(pts) - len(keep),
                     R_max_positive_side_kpc=round(max(pos), 3) if pos else "", R_max_negative_side_kpc=round(max(neg), 3) if neg else "",
                     R_max_any_side_kpc=round(max(pos + neg), 3), R_halpha_max_table_kpc=t["R_halpha_max_kpc"],
                     R_max_including_clipped_kpc=round(max(abs(r["R_kpc"]) for r in pts), 3),
                     n_pts_beyond_half_table_Rmax=sum(1 for r in keep if abs(r["R_kpc"]) >= 0.5 * float(t["R_halpha_max_kpc"])),
                     flag_star_in_table=t["flag_star"]))
check(bandbad < 1.5, f"sigma_0 grey band half-width agrees with the paper's Table error within {bandbad:.2f} km/s")
with open(os.path.join(HERE, "kurvs_sigma_coverage.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(summ[0].keys())); w.writeheader(); w.writerows(summ)
worst_r = max(abs(s["R_max_any_side_kpc"] - float(s["R_halpha_max_table_kpc"])) for s in summ)
log(f"      |R_max(any side, unclipped) - R_Halpha,max(table)| worst = {worst_r:.2f} kpc (informational)")
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axs = plt.subplots(5, 5, figsize=(20, 16)); axs = axs.ravel()
    for kid in range(1, 23):
        a = axs[kid - 1]; pts = [r for r in rows_out if r["kurvs_id"] == kid]
        for r in pts:
            a.errorbar(r["R_kpc"], r["sigma_obs_kms"], yerr=[[r["err_lo_kms"]], [r["err_up_kms"]]], fmt="o", ms=3,
                       color="k", mfc="w" if r["clipped_white_marker"] else "steelblue", lw=0.8)
        L = {r["kind"]: r["value_kms"] for r in line_out if r["kurvs_id"] == kid}
        a.axhline(L["sigma0_beam_corrected_line"], color="grey"); a.axhline(L["sigma0_observed_line"], color="grey", ls=":")
        a.set_title(f"KURVS-{kid}", fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "qa_replot.png"), dpi=60)
except Exception as ex:
    log(f"      QA plot skipped: {ex}")
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
