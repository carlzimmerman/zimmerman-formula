"""PRE-FREEZE synthetic calibration for W4-17 (planted worlds only; no real-data statistic is computed).
World A: exact simple-mu law at a0* for every SPARC galaxy (V_obs replaced), true Upsilon_d 0.5 -> all statistics ~0 at the true Upsilon.
World B: A plus a planted radial M/L gradient in the TRUE stellar mass (inner stars heavier: x(1 + (Rdisk/R)^0.5)), analysed with
constant Upsilon. Statistics vs analysis Upsilon in {0.5, 0.8}: Delta_g (gas-class minus star-class medians, p64 sample rule),
s (full-point WLS slope, W4-16), Delta_r (outer-half minus inner-half median log a0 by radius)."""
import contextlib, io, math, os, sys
import numpy as np
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
KPC = 3.0857e19; A0 = 0.5 * 2.99792458e8 * math.sqrt(6.67430e-11 * 0.685 * 8.533238720309458e-27)
GAL = [g for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2 and g["meta"]["Inc"] >= 30]
def world(grad):
    out = []
    for g in GAL:
        h = dict(g); R = g["R"] * KPC
        mult = (1 + np.sqrt(g["meta"]["Rdisk"] / np.clip(g["R"], 1e-3, None))) if grad else 1.0
        gb = (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + mult * (0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2)) * 1e6 / R
        m = gb > 0
        gt = np.where(m, gb * 0.5 * (1 + np.sqrt(1 + 4 * A0 / np.where(m, gb, 1.0))), 1e-12)
        h["Vobs"] = np.where(m, np.sqrt(gt * R) / 1e3, g["Vobs"]); out.append(h)
    return out
def stats(gals, U):
    dg, ss, dr = [], [], []
    for g in gals:
        R = g["R"] * KPC
        vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2; vs2f = 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
        gb = (vg2 + U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2) * 1e6 / R; go = (g["Vobs"] * 1e3) ** 2 / R
        v = (gb > 0) & (go > gb)
        if v.sum() < 8: continue
        la = np.full(len(gb), np.nan); la[v] = np.log10(go[v] * (go[v] - gb[v]) / gb[v])
        gm = (vg2 >= 0.7 * (vg2 + vs2f)) & v; sm = (vs2f >= 0.7 * (vg2 + vs2f)) & v
        if gm.sum() >= 3 and sm.sum() >= 3: dg.append(np.nanmedian(la[gm]) - np.nanmedian(la[sm]))
        x, y = np.log10(gb[v]), la[v]; ss.append(np.polyfit(x, y, 1)[0])
        rv = g["R"][v]; med = np.median(rv); dr.append(np.median(la[v][rv > med]) - np.median(la[v][rv <= med]))
    return np.median(dg) if dg else np.nan, len(dg), np.median(ss), np.median(dr)
for name, grad in (("A exact law", False), ("B planted radial M/L", True)):
    w = world(grad)
    for U in (0.5, 0.8):
        d, n, s, r = stats(w, U)
        print(f"{name:22s} Upsilon {U}: Delta_g {d:+.3f} (n {n}), s {s:+.3f}, Delta_r {r:+.3f}")

print("\nzero crossings Upsilon* (linear interpolation on the grid 0.3..1.4)")
UG = np.round(np.arange(0.3, 1.401, 0.1), 2)
def zero(vals):
    for i in range(len(UG) - 1):
        a, b = vals[i], vals[i + 1]
        if np.isfinite(a) and np.isfinite(b) and a * b <= 0:
            return UG[i] + (UG[i + 1] - UG[i]) * a / (a - b)
    return np.nan
for name, grad in (("A exact law", False), ("B planted radial M/L", True)):
    w = world(grad)
    rows = [stats(w, U) for U in UG]
    for lab, idx in (("Delta_g", 0), ("s", 2), ("Delta_r", 3)):
        print(f"  {name:22s} {lab:8s} Upsilon* = {zero([r[idx] for r in rows]):.3f}")
