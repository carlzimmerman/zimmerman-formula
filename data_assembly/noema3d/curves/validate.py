#!/usr/bin/env python3
"""Validation of the NOEMA3D Fig. 5 digitisation (criteria of the calc thread's CFG214, 8340f3750).  Writes validation_report.json and validation_report.md.
V1  axis-calibration residuals (tick labels vs fitted linear map) and the pixel-to-kpc check (top axis vs bottom axis vs the angular scale of the cosmology).
V2  gate: model V at +-R_e,disk against Table 3 V_c(R_e,disk) within 5%.  The declared series is the model line reaching the largest |R| (input-side choice); V is the drawn observed
    line-of-sight velocity divided by sin(i) with i from paper-1 Table 1 (needed only to compare with V_c); a galaxy that fails is reported and excluded.
V3  C4: one full panel (G4_38065 velocity, the first panel of the figure by the declared rule) read twice by independent variants A and B; rms differences and tick residuals in km/s and kpc.
V4  outermost data radius per galaxy and series.  No acceleration, a0 or velocity ratio other than V2 is computed."""
import csv, json, os, math, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); rd = lambda f: list(csv.DictReader(open(os.path.join(H, f))))
cal, dat, mod, per = rd("noema3d_fig5_axis_calibration.csv"), rd("noema3d_fig5_data_markers.csv"), rd("noema3d_fig5_model_curves.csv"), {r["id"]: r for r in rd("../noema3d_per_galaxy.csv")}
datB, modB, calB = rd("noema3d_fig5_data_markers_variantB.csv"), rd("noema3d_fig5_model_curves_variantB.csv"), rd("noema3d_fig5_axis_calibration_variantB.csv")
rep = {}
# V1
v1 = {}
for ax in ("bottom_arcsec", "top_kpc", "left_km/s"):
    rr = [r for r in cal if r["axis"] == ax and r["ok"] == "1"]; res = [float(r["max_residual_value"]) for r in rr]; rel = [float(r["max_residual_value"]) / float(r["span"]) for r in rr if float(r["span"]) > 0]
    v1[ax] = dict(panels=len(rr), of=len([r for r in cal if r["axis"] == ax]), max_residual=round(max(res), 3), median_residual=round(float(np.median(res)), 4), max_residual_over_span=round(max(rel), 4))
try:
    from astropy.cosmology import Planck18
    have = True
except Exception: have = False
sc = {}
for g in per:
    z = float(per[g]["z"]); sl = {}
    for ax in ("bottom_arcsec", "top_kpc"):
        sl[ax] = {r["panel"]: float(r["slope_per_px"]) for r in cal if r["galaxy"] == g and r["axis"] == ax and r["ok"] == "1"}
    k = [sl["top_kpc"][p] / sl["bottom_arcsec"][p] for p in sl["top_kpc"] if p in sl["bottom_arcsec"]]
    sc[g] = dict(kpc_per_arcsec_from_axes=round(float(np.median(k)), 4), spread=round(float(np.ptp(k)), 4), cosmology=None if not have else round(float(Planck18.kpc_proper_per_arcmin(z).value / 60), 4))
v1["kpc_per_arcsec"] = sc; v1["cosmology_used_for_comparison"] = "astropy Planck18 (comparison only; the paper's own cosmology is not stated on the pages read)" if have else "astropy not available"; rep["V1"] = v1
# V2
def curve(g, series, panel="velocity"):
    r = [x for x in mod if x["galaxy"] == g and x["panel"] == panel and x["series"] == series and x["R_kpc"] not in ("", "None")]
    r.sort(key=lambda x: float(x["R_kpc"])); return np.array([float(x["R_kpc"]) for x in r]), np.array([float(x["value"]) for x in r]), np.array([int(x["gap_px_to_visible_line"]) for x in r])
v2 = {}
for g, p in per.items():
    ser = sorted({x["series"] for x in mod if x["galaxy"] == g and x["panel"] == "velocity"})
    if not ser: v2[g] = dict(status="no model curve extracted"); continue
    ext = {s: max(abs(curve(g, s)[0]).max(), 0) for s in ser if len(curve(g, s)[0]) > 5}; s0 = max(ext, key=ext.get)
    kx, vy, ip = curve(g, s0); Re = float(p["Re_disk_fixed_kpc"]); inc = float(p["incl_deg_P1"]); Vc = float(p["Vc_at_Re_disk_kms"]); si = math.sin(math.radians(inc)); vals = {}
    for sgn, nm in ((+1, "plus"), (-1, "minus")):
        R = sgn * Re
        if kx.min() <= R <= kx.max():
            j = int(np.searchsorted(kx, R)); gp = int(min(ip[max(j - 1, 0)], ip[min(j, len(ip) - 1)]))
            if gp > 15: vals[nm + "_no_visible_line_within_15px"] = dict(gap_px=gp); continue
            vals[nm] = dict(v_model=round(float(np.interp(R, kx, vy)), 2), v_over_sin_i=round(abs(float(np.interp(R, kx, vy))) / si, 1), gap_px_to_visible_line=gp)
    used = [v["v_over_sin_i"] for k_, v in vals.items() if "v_over_sin_i" in v]
    if not used: v2[g] = dict(series=s0, R_e_disk_kpc=Re, status="R_e,disk outside the drawn model extent", model_extent_kpc=[round(float(kx.min()), 2), round(float(kx.max()), 2)]); continue
    m = float(np.mean(used)); dev = (m - Vc) / Vc
    v2[g] = dict(series=s0, R_e_disk_kpc=Re, inclination_deg_table1=inc, Vc_table3=Vc, model_extent_kpc=[round(float(kx.min()), 2), round(float(kx.max()), 2)], sides=vals, V_model_deprojected_mean=round(m, 1), deviation_from_Vc=round(dev, 3), gate_5pct="PASS" if abs(dev) <= 0.05 else "FAIL (excluded)")
rep["V2"] = v2
# V3: panel G4_38065 velocity, variant A vs B
def markers(rows, g, panel="velocity"): return [r for r in rows if r["galaxy"] == g and r["panel"] == panel]
def compare(g, panel="velocity"):
    out = {}; A_, B_ = markers(dat, g, panel), markers(datB, g, panel)
    for s in sorted({r["series"] for r in A_}):
        a = [(float(r["px_x"]), float(r["px_y"]), float(r["R_kpc"]), float(r["value"])) for r in A_ if r["series"] == s]; b = [(float(r["px_x"]), float(r["px_y"]), float(r["R_kpc"]), float(r["value"])) for r in B_ if r["series"] == s]
        pairs = []
        for x in a:
            if not b: continue
            j = int(np.argmin([math.hypot(x[0] - y[0], x[1] - y[1]) for y in b])); d = math.hypot(x[0] - b[j][0], x[1] - b[j][1])
            if d < 6: pairs.append((x, b[j]))
        out[s] = dict(n_A=len(a), n_B=len(b), n_matched=len(pairs), rms_dR_kpc=round(float(np.sqrt(np.mean([(p[0][2] - p[1][2]) ** 2 for p in pairs]))), 4) if pairs else None, rms_dV_kms=round(float(np.sqrt(np.mean([(p[0][3] - p[1][3]) ** 2 for p in pairs]))), 3) if pairs else None,
                      max_dV_kms=round(float(max(abs(p[0][3] - p[1][3]) for p in pairs)), 3) if pairs else None)
    # model curves on the common R grid
    for s in sorted({r["series"] for r in mod if r["galaxy"] == g and r["panel"] == panel}):
        ra = [(float(r["R_kpc"]), float(r["value"])) for r in mod if r["galaxy"] == g and r["panel"] == panel and r["series"] == s]; rb = [(float(r["R_kpc"]), float(r["value"])) for r in modB if r["galaxy"] == g and r["panel"] == panel and r["series"] == s]
        if ra and rb:
            ra.sort(); rb.sort(); xa = np.array([p[0] for p in ra]); xb = np.array([p[0] for p in rb]); lo, hi = max(xa.min(), xb.min()), min(xa.max(), xb.max()); gx = np.linspace(lo, hi, 60)
            d = np.interp(gx, xa, [p[1] for p in ra]) - np.interp(gx, xb, [p[1] for p in rb]); out["model_" + s] = dict(rms_dV_kms=round(float(np.sqrt(np.mean(d ** 2))), 3), max_dV_kms=round(float(np.abs(d).max()), 3), grid_kpc=[round(float(lo), 2), round(float(hi), 2)])
    return out
g3 = "G4_38065"
v3 = dict(panel=f"{g3} velocity", markers_and_model=compare(g3))
for lab, cc in (("A", cal), ("B", calB)):
    v3["tick_residual_" + lab] = {r["axis"]: r["max_residual_value"] for r in cc if r["galaxy"] == g3 and r["panel"] == "velocity"}
rep["V3_C4"] = v3
# V4
v4 = {}
for g in per:
    v4[g] = {}
    for s in sorted({r["series"] for r in dat if r["galaxy"] == g and r["panel"] == "velocity"}):
        rr = [(float(r["R_arcsec"]), float(r["R_kpc"]), float(r["value"]), float(r["visible_fraction"])) for r in dat if r["galaxy"] == g and r["panel"] == "velocity" and r["series"] == s]
        pos = [x for x in rr if x[0] > 0]; neg = [x for x in rr if x[0] < 0]
        v4[g][s] = dict(n=len(rr), outer_plus=None if not pos else dict(R_arcsec=max(x[0] for x in pos), R_kpc=max(x[1] for x in pos)), outer_minus=None if not neg else dict(R_arcsec=min(x[0] for x in neg), R_kpc=min(x[1] for x in neg)))
rep["V4_outermost_data_radius"] = v4

# V2b: POST-HOC diagnostic (not the declared gate): the drawn model is the 1D profile of the beam-smeared 3D model cube, so the deviation at R_e,disk is listed for every series together with R_e,disk over the beam major axis
obs = rd("../noema3d_observations.csv")
diag = {}
for g, p in per.items():
    Re = float(p["Re_disk_fixed_kpc"]); si = math.sin(math.radians(float(p["incl_deg_P1"]))); Vc = float(p["Vc_at_Re_disk_kms"]); scl = sc[g]["kpc_per_arcsec_from_axes"]
    beams = [float(o["beam"].split("x")[0]) for o in obs if o["id"] == g]
    diag[g] = dict(beam_major_arcsec_table2=beams, beam_major_kpc=[round(b * scl, 1) for b in beams], Re_disk_over_largest_beam_major=round(Re / (max(beams) * scl), 2), series={})
    for s in sorted({x["series"] for x in mod if x["galaxy"] == g and x["panel"] == "velocity"}):
        kx, vy, ip = curve(g, s); dv = []
        for sgn in (+1, -1):
            R = sgn * Re
            if len(kx) > 5 and kx.min() <= R <= kx.max():
                j = int(np.searchsorted(kx, R)); 
                if min(ip[max(j - 1, 0)], ip[min(j, len(ip) - 1)]) <= 15: dv.append(abs(float(np.interp(R, kx, vy))) / si)
        if dv: diag[g]["series"][s] = dict(V_over_sin_i=round(float(np.mean(dv)), 1), deviation_from_Vc=round(float(np.mean(dv)) / Vc - 1, 3))
rep["V2b_posthoc_beam_diagnostic"] = diag
json.dump(rep, open(os.path.join(H, "validation_report.json"), "w"), indent=1)
print(json.dumps({k: rep[k] for k in ("V1", "V3_C4")}, indent=1)[:3500]); print(json.dumps(rep["V2"], indent=0)[:4500])
