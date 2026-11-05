#!/usr/bin/env python3
"""FA1 gate 1 for I1, the tidal-isotropy selector zeta = rho_b / rho_bar_b. Criteria FROZEN_CRITERIA.md (d7c4be8f4c).
  python3 fa1_zeta.py              -> fa1_results.json, fa1.out
  FA1_MUTATE=1 python3 fa1_zeta.py -> fa1_results_MUTATE.json, fa1_MUTATE.out  (SPARC zeta x 0.1; must read SEPARATES)
Reads SPARC rotmod (CRG1 inputs), X-COP FITS (as RQ3), UX6's Plummer Bullet model. Selector only; no dust model.
kappa = 1/2 FITTED; not theory closed. Adopts nothing; the cold sector stays retired."""
import os, sys, json, math, glob
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
try: os.nice(19)
except OSError: pass
import numpy as np
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
MUT = os.environ.get("FA1_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"fa1{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n")
A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); FEET = ("canonical", "alt")
G_SI, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
F_MAX = (0.110 ** 2 - 0.069 ** 2) / 0.40 ** 2
CHECKS = {}
def check(n, ok, d):
    CHECKS[n] = bool(ok); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {d}")

# ---------- selector
def zeta_profile(r, M):
    """reading A on tabulated (r, M): (d ln M / d ln r)/3 by np.gradient in ln r. NaN where M <= 0."""
    r = np.asarray(r, float); M = np.asarray(M, float); z = np.full(r.shape, np.nan); ok = M > 0
    if ok.sum() >= 3:
        lr, lm = np.log(r[ok]), np.log(M[ok]); z[ok] = np.gradient(lm, lr) / 3.0
    return z
def zeta_tensor(T):
    """zeta from a 3x3 tidal tensor; 0 where tr T <= 0"""
    tr = np.trace(T)
    if tr <= 0: return 0.0
    TF = T - tr / 3.0 * np.eye(3); n = math.sqrt(float((TF * TF).sum()))
    return 1.0 / (1.0 + 3.0 / math.sqrt(6.0) * n / tr)
def plummer_hess(M, a, c, p):
    d = np.asarray(p, float) - np.asarray(c, float); s2 = float(d @ d) + a * a
    return M * (np.eye(3) / s2 ** 1.5 - 3.0 * np.outer(d, d) / s2 ** 2.5)   # G = 1; zeta is a ratio

# ---------- checks K0, K1
say("=" * 80); say(f"FA1 gate 1, I1 tidal isotropy. MUTATE={MUT}. f_max = {F_MAX:.4f}")
def law(g, a): return g * (0.5 + np.sqrt(0.25 + a / g))
def cand(gb, a, F=0.0, gd=0.0): return law(gb, a) + F * gd
gb = np.geomspace(1e-14, 1e-6, 200)
for f in FEET:
    d = float(np.max(np.abs(cand(gb, A0[f], 0.0, gb * 7.0) / law(gb, A0[f]) - 1)))
    check(f"K0 F=0 reproduces the law, {f}", d < 1e-12, f"max rel {d:.1e}")
Mp, ap = 1.0, 1.0; worst = 0.0
for rr in (0.1, 0.3, 1.0, 2.0, 5.0, 20.0):
    zt = zeta_tensor(plummer_hess(Mp, ap, (0, 0, 0), (rr / math.sqrt(3),) * 3)); za = ap ** 2 / (rr ** 2 + ap ** 2); worst = max(worst, abs(zt - za))
check("K1 Plummer Hessian zeta = analytic (dlnM/dlnr)/3", worst < 1e-6, f"max diff {worst:.1e}")
rt = np.geomspace(1, 100, 60)
z_uni = zeta_profile(rt, rt ** 3); z_iso = zeta_profile(rt, rt); z_pt = zeta_tensor(plummer_hess(1.0, 1e-3, (0, 0, 0), (1e3, 0, 0)))
check("K1 uniform sphere -> 1", np.nanmax(np.abs(z_uni - 1)) < 1e-9, f"{np.nanmax(np.abs(z_uni - 1)):.1e}")
check("K1 rho ~ r^-2 -> 1/3", np.nanmax(np.abs(z_iso - 1 / 3)) < 1e-3, f"{np.nanmax(np.abs(z_iso - 1 / 3)):.1e}")
check("K1 point mass far -> 0", z_pt < 1e-6, f"{z_pt:.1e}")

# ---------- X-COP, reading A
from astropy.io import fits
D = os.path.join(REPO, "real_research", "data", "xcop"); XC = []
def li(r, m, t): return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan
for name in sorted(os.listdir(D)):
    p = os.path.join(D, name)
    if not (os.path.isdir(p) and os.path.exists(os.path.join(p, f"{name}_mstar.fits"))): continue
    with fits.open(os.path.join(p, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
    with fits.open(os.path.join(p, f"{name}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
    with fits.open(os.path.join(p, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    for x in (.1, .2, .3, .5, .7):
        r = x * r5; ms = []
        for q in (r / 1.1, r, r * 1.1):
            mg, mst = li(ga["RADIUS"] * rg, ga["MGAS"], q), li(st["RADIUS"], st["MSTAR"], q); ms.append(mg + mst)
        mh = li(hm["RADIUS"], hm["M_FORW"], r)
        if np.all(np.isfinite(ms + [mh])):
            z = (math.log(ms[2]) - math.log(ms[0])) / (2 * math.log(1.1)) / 3.0
            XC.append(dict(n=name, x=x, r_kpc=r * 1e3, zeta=z, Mb=ms[1], gb=G_SI * ms[1] * MSUN / (r * 1e3 * KPC) ** 2))
zx = np.array([c["zeta"] for c in XC]); zc = float(np.percentile(zx, 5))
say(f"X-COP rows {len(XC)} in {len({c['n'] for c in XC})} clusters. zeta: min {zx.min():.3f}, 5th pct (zeta_c) {zc:.3f}, median {np.median(zx):.3f}, max {zx.max():.3f}")
for x in (.1, .2, .3, .5, .7):
    s = zx[[c["x"] == x for c in XC]]; say(f"  x = {x}: n {len(s)}, median zeta {np.median(s):.3f}, range {s.min():.3f}-{s.max():.3f}")

# ---------- SPARC, reading A
files = sorted(glob.glob(os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "sparc", "rotmod", "*_rotmod.dat")))
SP = []
for fpath in files:
    a = np.loadtxt(fpath, comments="#", ndmin=2); SP.append((os.path.basename(fpath).replace("_rotmod.dat", ""), a[:, 0], a[:, 3], a[:, 4], a[:, 5]))
def sparc_rows(Y, a0):
    zs, gbs, names, drop = [], [], [], 0
    for name, R, Vg, Vd, Vb in SP:
        V2 = np.sign(Vg) * Vg ** 2 + Y * Vd ** 2 + 1.4 * Y * Vb ** 2; M = V2 * R           # units cancel in the log slope
        z = zeta_profile(R, M); gbv = V2 * 1e6 / (R * KPC)
        if MUT: z = z * 0.1
        ok = np.isfinite(z) & (gbv > 0); drop += int((~ok).sum()); sel = ok & (gbv < a0)
        zs.append(z[sel]); gbs.append(gbv[sel]); names += [name] * int(sel.sum())
    return np.concatenate(zs), np.concatenate(gbs), np.array(names), drop
RES = dict(criteria="d7c4be8f4c", mutate=MUT, f_max=F_MAX, zeta_c=zc, xcop=dict(n=len(XC), zeta_min=float(zx.min()), zeta_median=float(np.median(zx)), zeta_max=float(zx.max()), rows=[{k: (round(v, 6) if isinstance(v, float) else v) for k, v in c.items() if k != "gb"} for c in XC]), footings={})
for f in FEET:
    o = {}
    for Y in (0.5, 0.3, 0.7):
        z, g_, nm, drop = sparc_rows(Y, A0[f]); hit = z >= zc; gal = sorted(set(nm)); galhit = sorted(set(nm[hit]))
        o[f"Y{Y}"] = dict(n_pts=int(len(z)), n_gal=len(gal), dropped=drop, f_SP=float(hit.mean()), n_hit=int(hit.sum()), gal_frac=len(galhit) / len(gal), zeta_median=float(np.median(z)), zeta_p95=float(np.percentile(z, 95)))
    fs = [o[k]["f_SP"] for k in ("Y0.5", "Y0.3", "Y0.7")]
    lab = "SEPARATES" if all(v <= F_MAX for v in fs) else ("DOES NOT SEPARATE" if all(v > F_MAX for v in fs) else "UNDECIDED")
    o["G-SEP"] = lab; RES["footings"][f] = o
    say(f"[{f}] SPARC g_b < a0: " + "; ".join(f"Y {k[1:]}: n {o[k]['n_pts']} pts / {o[k]['n_gal']} gal, f_SP {o[k]['f_SP']:.3f} ({o[k]['n_hit']}), galaxies hit {o[k]['gal_frac']:.2f}, median zeta {o[k]['zeta_median']:.3f}" for k in ("Y0.5", "Y0.3", "Y0.7")))
    say(f"[{f}] G-SEP: {lab} (line f <= {F_MAX:.3f})")

# ---------- reading B, thin-disc midplane
TB = np.diag([0.0, 0.0, 1.0]); zB = zeta_tensor(TB); RES["reading_B_midplane_zeta"] = zB
say(f"Reading B: thin-disc midplane zeta = {zB:.4f}; zeta_c {zc:.3f}: {'ABOVE (disc-volume dust would weigh)' if zB >= zc else 'below'}; effect size NOT COMPUTED")

# ---------- Bullet, UX6's Plummer model (kpc, Msun)
GAS = [(2.0e14, 565.0, 190.0, 90.0), (1.5e13, 505.0, 525.0, 120.0), (1.5e13, 90.0, 670.0, 170.0), (-6.8e12, 70.0, 670.0, 170.0)]
GAL = [(1.196e13, 470.0, 0.0, 0.0), (4.0e12, 245.0, 820.0, 220.0)]
PTS = dict(BCG1=(0.0, 0.0), BCG3=(820.0, 220.0), GASM=(190.0, 90.0), GASB=(670.0, 170.0))
def zb(x, y): return zeta_tensor(sum(plummer_hess(M, a, (cx, cy, 0.0), (x, y, 0.0)) for M, a, cx, cy in GAS + GAL))
def zb_disc(x0, y0, R=100.0, n=24):
    v = [zb(x0 + rr * math.cos(t), y0 + rr * math.sin(t)) for rr in np.linspace(0, R, n + 1)[1:] for t in np.linspace(0, 2 * math.pi, n, endpoint=False)]
    w = [rr for rr in np.linspace(0, R, n + 1)[1:] for _ in range(n)]
    return float(np.average(v, weights=w))
bu = {k: dict(point=zb(*p), disc100=zb_disc(*p)) for k, p in PTS.items()}
okB = bu["BCG1"]["point"] >= zc and bu["BCG3"]["point"] >= zc
wrong = any(bu[b]["point"] < zc and bu[gp]["point"] >= zc for b, gp in (("BCG1", "GASM"), ("BCG3", "GASB")))
lb = "WEIGHT ALLOWED AT GALAXIES" if okB else ("WRONG SIGN" if wrong else "NO SIGN")
RES["bullet"] = dict(points=bu, label=lb)
say("Bullet zeta (point, mean over 100 kpc): " + "; ".join(f"{k} {v['point']:.3f}, {v['disc100']:.3f}" for k, v in bu.items()) + f" -> G-BUL {lb}")

# ---------- Q2, Saturn's orbit
GMs = 1.32712440018e20; r = 9.5826 * 149597870700.0; rho = 0.1 * MSUN / (3.0857e16) ** 3
zq = 1.0 / (1.0 + 3.0 / math.sqrt(6.0) * math.sqrt(6.0) * GMs / r ** 3 / (4 * math.pi * G_SI * rho))
RES["Q2"] = dict(zeta_saturn=zq, label="INHERITS (dust off; Q2 rests on the MOND part)" if zq < zc else "DUST ON AT SATURN")
say(f"Q2: zeta at Saturn {zq:.2e} -> {RES['Q2']['label']}")

# ---------- labels
RES["checks"] = CHECKS; allok = all(CHECKS.values())
gs = [RES["footings"][f]["G-SEP"] for f in FEET]
if not allok: lane = "NO CLEAN LABEL (a check failed)"
elif all(g == "DOES NOT SEPARATE" for g in gs): lane = "I1 KILLED AT GATE 1"
elif all(g == "SEPARATES" for g in gs) and lb != "WRONG SIGN": lane = "I1 ALIVE AT GATE 1"
elif gs[0] != gs[1]: lane = "FOOTING-SPLIT"
else: lane = "UNDECIDED"
RES["lane_label"] = lane; say(f"LANE: {lane}" + (" [MUTATE twin]" if MUT else ""))
json.dump(RES, open(os.path.join(HERE, f"fa1_results{TAG}.json"), "w"), indent=1, sort_keys=True)
OUT.close()
