#!/usr/bin/env python3
"""Driver: digitise the velocity, dispersion and flux panels of the NOEMA3D Fig. 5 for all 10 galaxies and write CSVs.  Usage: run_all.py [outdir] [--variant B]
Variant B is an independent second read (different colour tolerance, opening radius, template thresholds) used for the C4 duplicate-read control."""
import sys, os, json, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import *
OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.path.dirname(os.path.abspath(__file__))
VAR = "B" if "--variant" in sys.argv else "A"
P = dict(A=dict(tol=45, min_own=0.62, max_bg=0.03, open_r=5), B=dict(tol=38, min_own=0.66, max_bg=0.02, open_r=4))[VAR]
PANELS = ["velocity", "dispersion", "flux"]; UNITS = {"velocity": "km/s", "dispersion": "km/s", "flux": "normalised"}
MANUAL = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "manual_axis_labels.json"))) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "manual_axis_labels.json")) else {}
def pix2val(poly, p): return float(np.polyval(poly, p))
def cal_for(name, panel, side, fr):
    key = f"{name}|{PANELS[panel]}|{side}"
    if key in MANUAL:                                            # printed labels transcribed by eye: {"labels": [values...]} matched to detected ticks in order
        tk = ticks(fr, side); v = MANUAL[key]["labels"]
        if len(tk) == len(v):
            p = np.polyfit(tk, v, 1); return dict(poly=p, max_resid=float(np.abs(np.array(v) - np.polyval(p, tk)).max()), n=len(v), n_tokens=len(v), span=float(max(v) - min(v)), source="manual")
    c = axis_cal(fr, side)
    if c: c["source"] = "ocr"
    return c
rows_data, rows_model, rows_cal, rows_leg = [], [], [], []
os.makedirs(os.path.join(OUT, "overlays_" + VAR), exist_ok=True)
for col in (0, 1):
    for row in range(5):
        name = NAMES[col][row]; frv = frame(col, row, 0); SWATCH.clear(); boxes, ent = legend_info(frv); sw = dict(SWATCH)
        cmap = {}
        for grp, lab, cn, cnt in ent:
            if cn: cmap.setdefault(grp, {})[lab] = cn
        # colour -> label: from the Data group when present (data series), else from the Model group; the label of the third colour is inferred by elimination
        lab_of = {}
        for grp in ("Model", "Data"):
            for lab, cn in cmap.get(grp, {}).items(): lab_of.setdefault(cn, lab)
        present = [c for c in COLOURS if c in lab_of]
        alllabs = [lab for grp, lab, cn, cnt in ent if grp == "Data"]
        miss = [l for l in alllabs if l not in lab_of.values()]
        if miss and len(present) < len(set(alllabs)):
            free = [c for c in COLOURS if c not in lab_of and c in ("red", "blue", "green")][:1]
            if free: lab_of[free[0]] = miss[0]; present.append(free[0])
        FIX = {'robustl': 'robust1', 'robusto.1': 'robust0.1', 'robustO.1': 'robust0.1', 'tappered': 'tapered'}
        lab_of = {c: FIX.get(l, l) for c, l in lab_of.items()}
        for grp, lab, cn, cnt in ent: rows_leg.append(dict(galaxy=name, group=grp, label=lab, colour=cn, swatch_px=cnt, marker_size_px=None if cn not in sw else round(sw[cn], 2)))
        # pass 1: calibrations and independent template scans in the three panels
        P3 = {}
        for panel in range(3):
            fr = frame(col, row, panel); x0, x1, y0, y1 = interior(fr); sub = A[y0:y1, x0:x1]
            cb, ct, cl = cal_for(name, panel, "bottom", fr), cal_for(name, panel, "top", fr), cal_for(name, panel, "left", fr)
            for side, c in (("bottom_arcsec", cb), ("top_kpc", ct), ("left_" + UNITS[PANELS[panel]], cl)):
                rows_cal.append(dict(galaxy=name, panel=PANELS[panel], axis=side, ok=int(c is not None), n_ticks_used=None if c is None else c["n"], n_tokens=None if c is None else c["n_tokens"], span=None if c is None else round(c["span"], 4),
                                     max_residual_value=None if c is None else round(c["max_resid"], 4), slope_per_px=None if c is None else float(c["poly"][0]), source=None if c is None else c["source"]))
            excl = [(b[0] - x0, b[1] - x0, b[2] - y0, b[3] - y0) for b in boxes] if panel == 0 else []
            P3[panel] = dict(fr=fr, sub=sub, x0=x0, y0=y0, cb=cb, ct=ct, cl=cl, excl=excl, found={})
            if cb is None or cl is None: continue
            for cn in COLOURS:
                if cn not in lab_of: continue
                size = sw.get(cn) or 7.0
                P3[panel]["found"][cn] = (scan_markers(sub, cn, size, excl, min_own=P["min_own"], max_bg=P["max_bg"], tol=P["tol"]), size)
        # pass 2: the three panels share the radial bins of each series; a bin is kept if found in >= 2 panels (or fully visible in one), and is re-fitted at that x in the panels that missed it
        for cn in [c for c in COLOURS if c in lab_of]:
            cand = []
            for panel in range(3):
                pp = P3[panel]
                if pp["cb"] is None or cn not in pp["found"]: continue
                for m in pp["found"][cn][0]: cand.append((pix2val(pp["cb"]["poly"], m["rx"] + pp["x0"]), panel, m["vis"]))
            if not cand: continue
            scale = abs(P3[0]["cb"]["poly"][0]) if P3[0]["cb"] is not None else 0.005
            cand.sort(); clusters_ = []
            for xv, pnl, vis in cand:
                if clusters_ and abs(xv - np.mean([c[0] for c in clusters_[-1]])) < 3.5 * scale: clusters_[-1].append((xv, pnl, vis))
                else: clusters_.append([(xv, pnl, vis)])
            bins = [float(np.median([c[0] for c in cl_])) for cl_ in clusters_ if len({c[1] for c in cl_}) >= 2 or max(c[2] for c in cl_) >= 0.9]
            for panel in range(3):
                pp = P3[panel]
                if pp["cb"] is None or cn not in pp["found"]: continue
                sm, size = pp["found"][cn]; sub = pp["sub"]; new_sm = []
                for bx in bins:
                    px = (bx - pp["cb"]["poly"][1]) / pp["cb"]["poly"][0] - pp["x0"]
                    near = [m for m in sm if abs(m["rx"] - px) < 3.5]
                    if near: mm = dict(min(near, key=lambda m: abs(m["rx"] - px))); mm["recovered"] = 0
                    else:
                        r_ = scan_markers(sub, cn, size, pp["excl"], min_own=0.30, max_bg=P["max_bg"] * 1.5, tol=P["tol"])
                        near = [m for m in r_ if abs(m["rx"] - px) < 2.5]
                        if not near: continue
                        mm = dict(min(near, key=lambda m: abs(m["rx"] - px))); mm["recovered"] = 1
                    mm["bin_arcsec"] = bx; new_sm.append(mm)
                pp["found"][cn] = (new_sm, size)
        # pass 3: rows
        for panel in range(3):
            pp = P3[panel]; sub, x0, y0, cb, ct, cl = pp["sub"], pp["x0"], pp["y0"], pp["cb"], pp["ct"], pp["cl"]
            if cb is None or cl is None: continue
            found = pp["found"]; foot = np.zeros(sub.shape[:2], bool)
            for cn, (sm, size) in found.items():
                for m in sm: foot |= template(SHAPE[cn], size + 2.5, m["rx"], m["ry"], *sub.shape[:2])
            for cn, (sm, size) in found.items():
                for m in sm:
                    up, dn = error_bar(sub, cn, m["rx"], m["ry"], size, tol=P["tol"]); xa = pix2val(cb["poly"], m["rx"] + x0); yv = pix2val(cl["poly"], m["ry"] + y0)
                    yu = pix2val(cl["poly"], up + y0); yd = pix2val(cl["poly"], dn + y0)
                    rows_data.append(dict(galaxy=name, panel=PANELS[panel], series=lab_of[cn], colour=cn, R_arcsec=round(xa, 4), R_kpc=None if ct is None else round(pix2val(ct["poly"], m["rx"] + x0), 3), value=round(yv, 3),
                                          err_up=round(abs(yu - yv), 3), err_down=round(abs(yd - yv), 3), visible_fraction=round(m["vis"], 2), recovered_at_shared_bin=m["recovered"], px_x=round(m["rx"] + x0, 1), px_y=round(m["ry"] + y0, 1)))
            for cn in found:
                lx, ly, lf = trace_line(sub, cn, foot, pp["excl"], tol=P["tol"])
                if len(lx) < 10: continue
                mx = [m["rx"] for m in found[cn][0]]; lo = int(min(lx.min(), min(mx))) if mx else int(lx.min()); hi = int(max(lx.max(), max(mx))) if mx else int(lx.max())
                grid = np.arange(lo, hi + 1, 4); yy = np.interp(grid, lx, ly); gap = np.array([np.min(np.abs(lx - g)) for g in grid])
                for g, y, gp in zip(grid, yy, gap):
                    rows_model.append(dict(galaxy=name, panel=PANELS[panel], series=lab_of[cn], colour=cn, R_arcsec=round(pix2val(cb["poly"], g + x0), 4), R_kpc=None if ct is None else round(pix2val(ct["poly"], g + x0), 3),
                                           value=round(pix2val(cl["poly"], y + y0), 3), interpolated=int(gp > 3), gap_px_to_visible_line=int(gp), px_x=g + x0, px_y=round(float(y) + y0, 1)))
            img = sub.copy().astype("uint8")
            for cn, (sm, size) in found.items():
                for m in sm: cv2.drawMarker(img, (int(round(m["rx"])), int(round(m["ry"]))), (0, 0, 0) if not m["recovered"] else (255, 0, 255), cv2.MARKER_CROSS, 12, 1)
            Image.fromarray(img).save(os.path.join(OUT, "overlays_" + VAR, f"{name}_{PANELS[panel]}.png"))
def w(fn, rows):
    with open(os.path.join(OUT, fn), "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)
sfx = "" if VAR == "A" else "_variantB"
w(f"noema3d_fig5_data_markers{sfx}.csv", rows_data); w(f"noema3d_fig5_model_curves{sfx}.csv", rows_model); w(f"noema3d_fig5_axis_calibration{sfx}.csv", rows_cal); w(f"noema3d_fig5_legends{sfx}.csv", rows_leg)
print("data rows", len(rows_data), "model rows", len(rows_model))
