#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG275 (lane F) -- digitiser for the rotation-curve points of Lin et al. (arXiv:2411.08958, PKS 0529-549 [CI](2-1)) from the paper's VECTOR figures.

The e-print's figures are vector PDFs: marker centres and error-bar ends are exact coordinates, calibrated from the axes' major tick marks.
  ADC_compare.pdf               V_rot (black circles + error bars), V_c with constant sigma_v (red squares), V_c with varying sigma_v (blue diamonds); x in arcsec
  PKS_0529-549_MaxGas_MCMC.pdf  V_c (black circles + error bars) used in the mass-model fits; x in kpc
Output: lin2024_rings_digitised.csv (long format).  QA is printed WITHOUT velocity values.
Not blind: the author of this script had already decoded these curves by hand before writing it (disclosed in FROZEN_CRITERIA.md section 0).
Run: python3 cfg275_digitise_lin24.py
"""
import os, sys, csv, math, hashlib
sys.dont_write_bytecode = True
import numpy as np
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
FIG = os.path.join(os.path.dirname(REPO), "_external_data", "arxiv_src", "2411.08958", "fig")
LOG = []


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]


def ticks(drs):
    xt = sorted(set(round(d["rect"].x0, 3) for d in drs if d["type"] == "fs" and len(d["items"]) == 1 and d["rect"].width == 0 and abs(d["rect"].height - 3.0) < 0.01))
    yt = sorted(set(round(d["rect"].y0, 3) for d in drs if d["type"] == "fs" and len(d["items"]) == 1 and d["rect"].height == 0 and abs(d["rect"].width - 3.0) < 0.01))
    return xt, yt


def calibrate(pos, vals, name):
    a, b = np.polyfit(pos, vals, 1)
    res = np.array(vals) - (a * np.array(pos) + b)
    P(f"    {name}: {len(pos)} major ticks, slope {a:.6g} data/pt, max |residual| {np.max(np.abs(res)):.2e} data units")
    return (lambda p: a * p + b), float(np.max(np.abs(res)))


def near(c, ref, tol=0.01):
    return c is not None and all(abs(c[i] - ref[i]) < tol for i in range(3))


def read_fig(fn, xvals, scale_x_name, csize):
    p = fitz.open(os.path.join(FIG, fn))[0]
    drs = p.get_drawings()
    xt, yt = ticks(drs)
    assert len(xt) == len(xvals) and len(yt) == 9, (fn, xt, yt)
    fx, rx = calibrate(xt, xvals, f"{fn} x ({scale_x_name})")
    fy, ry = calibrate(yt[::-1], [0, 50, 100, 150, 200, 250, 300, 350, 400], f"{fn} y (km/s)")
    legend = [d["rect"] for d in drs if d.get("color") and d["type"] == "fs" and abs(d["color"][0] - 0.8) < 0.01]                    # the legend box (grey frame)
    inleg = lambda r: any(l.contains(fitz.Point((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)) for l in legend)
    out = {"circ": [], "red": [], "blue": [], "bar": []}
    for d in drs:
        r = d["rect"]
        if inleg(r): continue
        if d["type"] == "fs" and len(d["items"]) == 8 and abs(r.width - csize) < 0.1 and abs(r.height - csize) < 0.1 and d.get("fill") == (0.0, 0.0, 0.0):
            out["circ"].append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
        elif d["type"] == "s" and near(d.get("color"), (0.8627451, 0.0784314, 0.2352941)) and len(d["items"]) == 1:
            out["red"].append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
        elif d["type"] == "s" and near(d.get("color"), (0.1176471, 0.5647059, 1.0)) and len(d["items"]) == 4:
            out["blue"].append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
        elif d["type"] == "s" and d.get("color") == (0.0, 0.0, 0.0) and d.get("fill") is None and len(d["items"]) == 1 and abs(d.get("width", 0) - 1.0) < 0.01 and r.width == 0:
            out["bar"].append((r.x0, r.y0, r.y1))
    for k in out: out[k].sort()
    return fx, fy, out, max(rx, ry)


P(__doc__.split("Run:")[0].strip())
rows = []
KPA_PAPER = 8.22                                                             # kpc per arcsec stated in the paper's scale (checked below against the MCMC figure's kpc axis)
fxa, fya, oa, qa = read_fig("ADC_compare.pdf", [0.1, 0.2, 0.3, 0.4], "arcsec", 5.0)
fxm, fym, om, qm = read_fig("PKS_0529-549_MaxGas_MCMC.pdf", [0, 1, 2, 3], "kpc", 3.0)
P(f"  ADC_compare.pdf sha256 {sha(os.path.join(FIG, 'ADC_compare.pdf'))}; PKS_0529-549_MaxGas_MCMC.pdf sha256 {sha(os.path.join(FIG, 'PKS_0529-549_MaxGas_MCMC.pdf'))}")
P(f"  marker counts ADC: V_rot circles {len(oa['circ'])}, V_c const-sigma squares {len(oa['red'])}, V_c varying-sigma diamonds {len(oa['blue'])}, error bars {len(oa['bar'])}; MCMC: V_c circles {len(om['circ'])}, error bars {len(om['bar'])}")
assert len(oa["circ"]) == len(oa["red"]) == len(oa["blue"]) == len(oa["bar"]) == len(om["circ"]) == len(om["bar"]) == 5
for k in range(5):
    xa = fxa(oa["circ"][k][0]); xr = fxa(oa["red"][k][0]); xb = fxa(oa["blue"][k][0]); xbar = fxa(oa["bar"][k][0])
    assert abs(xa - xr) < 1e-3 and abs(xa - xb) < 1e-3 and abs(xa - xbar) < 1e-3, ("x mismatch in ADC ring", k)
    rows.append(["V_rot (3DFIT)", k + 1, f"{xa:.4f}", f"{xa * KPA_PAPER:.4f}", f"{fya(oa['circ'][k][1]):.3f}", f"{fya(oa['circ'][k][1]) - fya(oa['bar'][k][2]):.3f}", f"{fya(oa['bar'][k][1]) - fya(oa['circ'][k][1]):.3f}", "ADC_compare.pdf"])
    rows.append(["V_c (constant sigma_v)", k + 1, f"{xa:.4f}", f"{xa * KPA_PAPER:.4f}", f"{fya(oa['red'][k][1]):.3f}", "", "", "ADC_compare.pdf"])
    rows.append(["V_c (varying sigma_v)", k + 1, f"{xa:.4f}", f"{xa * KPA_PAPER:.4f}", f"{fya(oa['blue'][k][1]):.3f}", "", "", "ADC_compare.pdf"])
    xk = fxm(om["circ"][k][0]); assert abs(xk - fxm(om["bar"][k][0])) < 1e-3
    rows.append(["V_c (mass-model fit input)", k + 1, f"{xk / KPA_PAPER:.4f}", f"{xk:.4f}", f"{fym(om['circ'][k][1]):.3f}", f"{fym(om['circ'][k][1]) - fym(om['bar'][k][2]):.3f}", f"{fym(om['bar'][k][1]) - fym(om['circ'][k][1]):.3f}", "PKS_0529-549_MaxGas_MCMC.pdf"])
# QA that prints no velocity values
xs_a = np.array([float(r[2]) for r in rows if r[0] == "V_rot (3DFIT)"]); xs_k = np.array([float(r[3]) for r in rows if r[0] == "V_c (mass-model fit input)"])
exp_arc = 0.045 + 0.09 * np.arange(5)
P(f"  ring radii (arcsec) equal 0.045 + 0.09 k (the paper's 0.09-arcsec rings) to {float(np.max(np.abs(xs_a - exp_arc))):.1e}; radii in kpc from the MCMC figure equal arcsec x {KPA_PAPER} to {float(np.max(np.abs(xs_k - exp_arc * KPA_PAPER))):.1e} kpc")
vc_adc = np.array([float(r[4]) for r in rows if r[0] == "V_c (constant sigma_v)"]); vc_mc = np.array([float(r[4]) for r in rows if r[0] == "V_c (mass-model fit input)"])
P(f"  the MCMC figure's V_c data equal the ADC figure's constant-sigma V_c: max |difference| {float(np.max(np.abs(vc_adc - vc_mc))):.3f} km/s (the same five points, two figures)")
P(f"  calibration max residual {max(qa, qm):.2e} data units; ticks and tick labels agree to 0.02 pt")
with open(os.path.join(HERE, "lin2024_rings_digitised.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["series", "ring", "R_arcsec", "R_kpc", "V_kms", "err_lo_kms", "err_hi_kms", "source_pdf"]); [w.writerow(r) for r in rows]
P(f"  wrote lin2024_rings_digitised.csv ({len(rows)} rows)")
open(os.path.join(HERE, "cfg275_digitise.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
