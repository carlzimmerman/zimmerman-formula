#!/usr/bin/env python3
"""OE1 Part C and K4 (FROZEN_CRITERIA.md): what the particles do from 1 to 6 R200: slope, rho/rho_mean, infall share, the sphere's edge; direct particle Delta-Sigma against M(<r) through an Abel projection. Reads snapshots only. kappa = 1/2 FITTED; not theory closed."""
import glob, json, math, os, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(H); OUT = []; RES = {}
def P(s): print(s, flush=True); OUT.append(s)
G = 4.30091e-9; Om, h = 0.2976016, 0.6856427; H0 = 100 * h
def rho_c(z): return 3 * H0 ** 2 * (Om * (1 + z) ** 3 + 1 - Om) / (8 * math.pi * G)
def rho_m(z): return 3 * H0 ** 2 * Om * (1 + z) ** 3 / (8 * math.pi * G)
XB = np.geomspace(0.7, 12.0, 25); XC = np.sqrt(XB[1:] * XB[:-1])
def centre(x, m):
    c = np.median(x, 0)
    for rad in (3.0, 1.5, 0.8, 0.4, 0.2):
        k = ((x - c) ** 2).sum(1) < rad ** 2
        if k.sum() > 50: c = x[k].mean(0)
    return c
def prof(f, z):
    Z = np.load(f, allow_pickle=False); x, m = Z["x"], float(Z["m"]); v = Z["v"] if "v" in Z.files else None; c = centre(x, m); d = x - c; r = np.sqrt((d * d).sum(1)); o = np.argsort(r); rs = r[o]; Me = np.arange(1, len(r) + 1) * m; den = Me / (4 / 3 * math.pi * rs ** 3); thr = 200 * rho_c(z); i = np.where(den >= thr)[0].max(); R2 = rs[i] * (den[i] / thr) ** (1 / 3); M2 = thr * 4 / 3 * math.pi * R2 ** 3
    Nb, _ = np.histogram(r / R2, XB); vol = 4 / 3 * math.pi * R2 ** 3 * np.diff(XB ** 3); rho = Nb * m / vol
    fin = np.full(len(XC), np.nan); vrm = np.full(len(XC), np.nan)
    if v is not None:
        kq = r < R2; vm = v[kq].mean(0); vr = ((v - vm) * d).sum(1) / np.maximum(r, 1e-9) + (H0 * math.sqrt(Om * (1 + z) ** 3 + 1 - Om) * r * 0)
        for b in range(len(XC)):
            k = (r / R2 >= XB[b]) & (r / R2 < XB[b + 1])
            if k.sum() > 5: fin[b] = np.mean(vr[k] < 0); vrm[b] = np.mean(vr[k])
    return dict(R2=R2, M2=M2, rho=rho, N=Nb, fin=fin, vrm=vrm, rmax=rs[int(0.999 * len(rs))], r90=rs[int(0.9 * len(rs))], Mtot=len(r) * m, d=d, m=m, rs=rs, Me=Me)
def ds_direct(p, Rs):
    d, m = p["d"], p["m"]; out = []
    for ax in range(3):
        R = np.sqrt((np.delete(d, ax, 1) ** 2).sum(1)); out.append([(np.sum(R < a) * m / (math.pi * a ** 2)) - np.sum((R >= a * 0.95) & (R < a * 1.05)) * m / (math.pi * a ** 2 * (1.05 ** 2 - 0.95 ** 2)) for a in Rs])
    return np.mean(out, 0)
def ds_abel(p, Rs, rcut=None):
    rs = p["rs"][::200]; Me = p["Me"][::200]; rc = np.geomspace(rs[1], rs[-1], 400); M = np.interp(rc, rs, Me)
    if rcut is not None: M = np.minimum(M, np.interp(rcut, rc, M))
    rho = np.gradient(M, rc) / (4 * math.pi * rc ** 2); out = []
    def Sig(a):
        l = np.geomspace(1e-3, np.sqrt(max(rc[-1] ** 2 - a ** 2, 1e-6)), 1500); return 2 * np.trapz(np.interp(np.sqrt(a ** 2 + l ** 2), rc, rho, right=0) * l, np.log(l))
    RR = np.geomspace(0.01, max(Rs) * 1.06, 160); SS = np.array([Sig(a) for a in RR])
    for a in Rs:
        k = RR <= a; me = (np.interp(0.01, rc, M) + 2 * math.pi * np.trapz(SS[k] * RR[k] ** 2, np.log(RR[k]))) / (math.pi * a ** 2); out.append(me - np.interp(a, RR, SS))
    return np.array(out)
SETS = {"1e13": sorted(glob.glob(os.path.join(RB, "ZN1_zooms_to_z0", "runs", "M1e13_s?_ng64"))), "1e14": sorted(glob.glob(os.path.join(RB, "ZN4_cluster_resolution", "runs", "M1e14_s?_ng80"))), "1e15": sorted(glob.glob(os.path.join(RB, "ZN4_cluster_resolution", "runs", "M1e15_s?_ng80"))), "1e12": sorted(glob.glob(os.path.join(RB, "ZN1_zooms_to_z0", "runs", "M1e12_s?_ng64")))}
P("OE1 particles: stack medians at each x; slope = -d ln rho/d ln r; kappa = 1/2 FITTED; not theory closed")
for M_, ds in SETS.items():
    for zs, z in (("0.00", 0.0), ("0.25", 0.25)):
        rows = [prof(os.path.join(d, f"snap_z{zs}.npz"), z) for d in ds if os.path.exists(os.path.join(d, f"snap_z{zs}.npz"))]
        if not rows: continue
        rho = np.median([q["rho"] for q in rows], 0); sl = -np.gradient(np.log(np.maximum(rho, 1e-30)), np.log(XC)); slm = np.array([-np.gradient(np.log(np.maximum(q["rho"], 1e-30)), np.log(XC)) for q in rows]); fin = np.nanmedian([q["fin"] for q in rows], 0); rm = rho_m(z); i1, i2 = np.searchsorted(XC, 1.4), np.searchsorted(XC, 2.0) - 1; ok = XC <= 6; im = np.argmax(sl[ok]); wide = float(np.log(np.interp(1.4, XC, rho) / np.interp(2.4, XC, rho)) / np.log(2.4 / 1.4)); xsph = np.median([q["rmax"] / q["R2"] for q in rows]); x90 = np.median([q["r90"] / q["R2"] for q in rows]); cliff = float(sl[i1:i2 + 1].max())
        RES[f"{M_}|{zs}"] = dict(n=len(rows), x=XC.tolist(), slope=sl.tolist(), rho_over_mean=(rho / rm).tolist(), fin=fin.tolist(), x90=float(x90), x999=float(xsph), R200=float(np.median([q["R2"] for q in rows])), M_tot_over_M200=float(np.median([q["Mtot"] / q["M2"] for q in rows])), slope_max_14_20=cliff, slope_seed_max_14_20=float(np.max(slm[:, i1:i2 + 1])), steepest_x=float(XC[ok][im]), steepest=float(sl[ok][im]), mean_slope_14_24=wide)
        P(f"{M_} z {zs} n {len(rows)}: R200 {RES[f'{M_}|{zs}']['R200']:.3f}; x90 {x90:.2f}, x99.9 {xsph:.2f}; M_tot/M200 {RES[f'{M_}|{zs}']['M_tot_over_M200']:.2f}; slope 1.4-2 R200 stack max {cliff:.2f} (any seed {RES[f'{M_}|{zs}']['slope_seed_max_14_20']:.2f}); steepest inside 6 R200 {sl[ok][im]:.2f} at x {XC[ok][im]:.2f}; mean slope 1.4-2.4 R200 {wide:.2f}")
        for xx in (1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0):
            j = np.argmin(abs(XC - xx)); P(f"   x {XC[j]:.2f}: slope {sl[j]:+.2f}, rho/rho_mean {rho[j] / rm:.2f}, shell N med {np.median([q['N'][j] for q in rows]):.0f}, share v_r<0 {fin[j]:.2f}")
# VB1
for tag, rs_ in (("A", "rs1.5"), ("B", "rs2.0")):
    p = prof(os.path.join(RB, "VB1_vacuum_boundary", "runs", f"M1e14_s1_ng48_{rs_}", "snap_z0.00.npz"), 0.0); rm = rho_m(0); sl = -np.gradient(np.log(np.maximum(p["rho"], 1e-30)), np.log(XC)); P(f"VB1 {tag} {rs_}: R200 {p['R2']:.3f}; M_tot/M200 {p['Mtot'] / p['M2']:.2f}; x99.9 {p['rmax'] / p['R2']:.2f}"); P("   " + "; ".join(f"x {XC[j]:.2f} slope {sl[j]:+.2f} rho/mean {p['rho'][j] / rm:.2f} in {p['fin'][j]:.2f}" for j in range(4, 22, 3)))
    RES[f"VB1{tag}"] = dict(x=XC.tolist(), slope=sl.tolist(), rho_over_mean=(p["rho"] / rm).tolist(), fin=p["fin"].tolist(), tot=p["Mtot"] / p["M2"])
# K4
bad = []; P("K4 direct particles (3 axes) against M(<r) through Abel, no cut, both own run; R in R200 units 1.2, 1.6, 2.0, 2.4; then a cut at x 4 and x 7 through the same Abel")
for M_, d in (("1e14", SETS["1e14"][0]), ("1e15", SETS["1e15"][0])):
    p = prof(os.path.join(d, "snap_z0.25.npz"), 0.25); Rs = np.array([1.2, 1.6, 2.0, 2.4]) * p["R2"]; a = ds_direct(p, Rs); b = ds_abel(p, Rs); c4 = ds_abel(p, Rs, 4 * p["R2"]); c7 = ds_abel(p, Rs, 7 * p["R2"]); rt = b / a; bad += [abs(rt - 1).max()]; P(f"  {M_}: direct {np.round(a / 1e12, 2)}, Abel {np.round(b / 1e12, 2)} M/pc^2; ratio {np.round(rt, 3)}; cut at 4 / none {np.round(c4 / b, 3)}; cut at 7 / none {np.round(c7 / b, 3)}"); RES[f"K4{M_}"] = dict(ratio=rt.tolist(), c4=(c4 / b).tolist(), c7=(c7 / b).tolist())
RES["K4"] = float(max(bad)); P(f"K4 {'PASS' if max(bad) <= 0.05 else 'FAIL (stated, not a stop)'}: max |ratio - 1| {max(bad):.3f}")
json.dump(RES, open(os.path.join(H, "oe1_particles.json"), "w")); open(os.path.join(H, "oe1_particles.out"), "w").write("\n".join(OUT) + "\n")
