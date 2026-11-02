#!/usr/bin/env python3
"""UL1 part 1: c from raw z = 0 snapshots, own centre and fits; MW cold mass inside R0 on EM1. Reads ZN1's and LC1-paired snapshots only. kappa = 1/2 FITTED, unused; not theory closed."""
import glob, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
G = 4.30091e-9; Om, h = 0.2976016, 0.6856427
rhoc0 = 3 * (100 * h) ** 2 / (8 * math.pi * G)
mu = lambda y: np.log1p(y) - y / (1 + y)
def centre(x):
    c = np.median(x, 0); r = np.sqrt(((x - c) ** 2).sum(1)).max()
    for _ in range(40):
        s = ((x - c) ** 2).sum(1) < r * r
        if s.sum() < 200: break
        c = x[s].mean(0); r *= 0.85
    return c
def fitc(r, Menc, lo, hi, Rn):
    s = (r >= lo) & (r <= hi); r_ = r[s]; m_ = np.log(Menc[s]); idx = np.unique(np.geomspace(1, len(r_), 800).astype(int) - 1); r_, m_ = r_[idx], m_[idx]; cs = np.linspace(1, 40, 1561); M_R = float(np.interp(Rn, r, Menc))
    # shape-only over the range, normalised at Rn
    return float(cs[int(np.argmin([np.sum((np.log(mu(c * r_ / Rn) / mu(c)) + math.log(M_R) - m_) ** 2) for c in cs]))])
def one(d, Mb_list):
    A = np.load(os.path.join(d, "snap_z0.00.npz"), allow_pickle=False); x, m = A["x"], float(A["m"]); me = json.loads(str(A["meta"])); c = centre(x); r = np.sort(np.sqrt(((x - c) ** 2).sum(1))); M = np.arange(1, len(r) + 1) * m; dn = M / (4 / 3 * math.pi * r ** 3); eps = me["eps"]
    rho_m = me["Mf"] / (4 / 3 * math.pi * me["qM"] ** 3); R200 = float(r[np.where(dn >= 200 * rhoc0)[0].max()]); rvir = float(r[np.where(dn >= 18 * math.pi ** 2 * rho_m)[0].max()]); rconv = max(3 * eps, float(r[199]))
    c200 = fitc(r, M, max(3 * eps, 0.05 * R200), R200, R200); cnfw = fitc(r, M, rconv, rvir, rvir); M200 = float(np.interp(R200, r, M)); o = dict(R200=R200, rvir=rvir, eps=eps, rconv=rconv, c200=c200, c_nfw=cnfw, M200=M200, rho_m_over_rhoc=rho_m / rhoc0, r_c=lambda X: float(np.interp(X * R200, r, M)) / M200); return o
T = json.load(open(os.path.join(RB, "UR3_direct_weighing", "ur3_S_table.json")))["bg"]["A_c2b_refit"]
R = [one(d, None) for d in sorted(glob.glob(os.path.join(RB, "ZN1_zooms_to_z0", "runs", "M1e12_s?_ng64")))]
P(f"UL1 part 1. 1e12, ZN1 no-disc z = 0, {len(R)} seeds (the same no-disc runs LC1 paired). Own centre and fits; kappa = 1/2 FITTED, unused")
for k in ("R200", "rvir", "eps", "rconv", "c200", "c_nfw", "M200", "rho_m_over_rhoc"): v = [q[k] for q in R]; P(f"  {k:18s} median {np.median(v):.4g} range [{min(v):.4g}, {max(v):.4g}]")
rt = [q["c_nfw"] / q["c200"] for q in R]; P(f"  c_nfw/c200 median {np.median(rt):.3f} range [{min(rt):.3f}, {max(rt):.3f}]; r_vir/R200 {np.median([q['rvir'] / q['R200'] for q in R]):.3f}; exact NFW c200 7.5 with this r_vir ratio would give c_nfw {7.5 * np.median([q['rvir'] / q['R200'] for q in R]):.2f}")
# MW
Mb = float(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, os.path.join(RB, "UR3_direct_weighing")); import contextlib, io
s = open(os.path.join(RB, "UR3_direct_weighing", "ur3_mw.py")).read(); s = s[:s.index('g["MODE"].update(')]; NS = {"__file__": os.path.join(RB, "UR3_direct_weighing", "ur3_mw.py"), "__name__": "m"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(s, "ur3b", "exec"), NS)
MCM = NS["MCM"]; Mb = MCM["Mb"]; R0 = 8.178; lM = T["a"] + T["b"] * (math.log10(Mb) - 10); Mc = 10 ** lM; rc = 3 * (100 * T["h"]) ** 2 / (8 * math.pi * G) ; FC = (lambda r: r / (1 + r))(json.load(open(os.path.join(RB, "RET1_retention_replaces_em1", "ret1_results.json")))["RNAT"]); Rcold = (3 * Mc / (4 * math.pi * 200 * rc)) ** (1 / 3) * 1e3; Rtot = (3 * (Mc / FC) / (4 * math.pi * 200 * rc)) ** (1 / 3) * 1e3
nfw = lambda c, Rn: Mc * mu(c * R0 / Rn) / mu(c)
P(f"MW on EM1: M_b {Mb:.3e}, cold M200 {Mc:.3e}, cold share {FC:.3f}; R200 reading cold {Rcold:.1f} kpc, total {Rtot:.1f} kpc; R0 {R0} kpc, 3 eps {3 * np.median([q['eps'] for q in R]) * 1e3:.2f} kpc (scaled by R200 ratio, about {3 * np.median([q['eps'] for q in R]) / np.median([q['R200'] for q in R]) * Rtot:.2f})")
P(f"  UR3's row: NFW c 12.95 on R_cold: {nfw(12.95, Rcold):.3e}")
c = float(np.median([q["c200"] for q in R]))
for nm, Rn in (("cold", Rcold), ("total", Rtot)):
    v = [q["r_c"](R0 / Rn) * Mc for q in R]; P(f"  raw snapshots, m(x) at x = R0/R200_{nm} = {R0 / Rn:.4f}: M_cold(<R0) median {np.median(v):.3e} range [{min(v):.3e}, {max(v):.3e}]; NFW own c200 {c:.2f} on same R {nfw(c, Rn):.3e}")
dd = [abs(q["r_c"](R0 / Rtot) * Mc / nfw(12.95, Rcold) - 1) for q in R]; d = float(np.median(dd)); dc = float(np.median([abs(q["r_c"](R0 / Rcold) * Mc / nfw(12.95, Rcold) - 1) for q in R])); lab = "DEFINITION ERROR REAL" if np.median(rt) >= 1.3 and min(d, dc) >= 0.25 else "NOT ESTABLISHED"
P(f"Label: {lab}: c_nfw/c200 {np.median(rt):.2f} (line 1.3); |direct/UR3 row - 1| {dc:.2f} cold reading, {d:.2f} total reading (line 0.25)")
P(f"  Sensitivity: M_cold(<R0) for hand core is quoted by SP3 as 1.47e10.")
json.dump(dict(label=lab, c200=c, c_nfw=float(np.median([q["c_nfw"] for q in R])), ratio=float(np.median(rt))), open(os.path.join(HERE, "ul1_c.json"), "w"), indent=1); open(os.path.join(HERE, "ul1_c.out"), "w").write("\n".join(OUT) + "\n")
