#!/usr/bin/env python3
"""X77_direct_core_surface_density (criteria 21f010353f): fit the smooth-core shape to each finished X48 zoom halo with
X48's own measure() range/objective and read eta_native = rho0 r0 / (18 pi^2 rho_m r_vir) = (4/3) a^2 / B_S(a).
    python3 x77_direct_eta.py [--mutate]"""
import glob, json, math, os, sys
import numpy as np
from scipy.integrate import quad
HERE = os.path.dirname(os.path.abspath(__file__)); X48 = os.path.join(os.path.dirname(HERE), "X48_native_cf_zoom")
sys.path.insert(0, X48); import x48_analyze as XA
MUT = "--mutate" in sys.argv
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
BS = lambda x: 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
BB = lambda x: np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)          # Burkert: M(<x r0) = pi rho0 r0^3 BB(x)
AG = np.geomspace(0.5, 60.0, 2001)
def fit(x, m, rho_m, eps):
    o = XA.measure(x, m, rho_m, eps)
    if "rconv" not in o or o["flag"] in ("unresolved", "too few bins", "no virial radius"): return o, None
    c = XA.centre(x, m); r = np.sort(np.sqrt(((x - c) ** 2).sum(1)))
    if MUT:
        q = r < o["rvir"] / 4; r = np.sort(np.where(q, 0.8 * r, r))
    Menc = np.arange(1, len(r) + 1) * m; rv, rc = o["rvir"], o["rconv"]
    sel = (r >= rc) & (r <= rv); y = np.log(Menc[sel] / Menc[sel][-1]); u = r[sel] / rv
    res = {}
    for nm, B in (("S", BS), ("B", BB)):
        a = min(AG, key=lambda aa: float(np.sum((np.log(B(aa * u) / B(aa)) - y) ** 2)))
        res[nm] = dict(a=float(a), eta=float(4 / 3 * a * a / B(a)))
    return o, res
# K2: formula vs direct integration (smooth core, a = 6)
a = 6.0; Mv = 1.0; rv = 1.0; r0 = rv / a
I = quad(lambda r: 4 * math.pi * r * r / (1 + (r / r0) ** 2) ** 1.5, 0, rv, epsabs=1e-14, epsrel=1e-13)[0]
rho0 = Mv / I; eta_int = rho0 * r0 / (3 * Mv / (4 * math.pi * rv ** 3) * rv)
k2 = abs(eta_int / (4 / 3 * a * a / BS(a)) - 1) < 1e-10
P(f"K2 eta formula vs integral (a=6): {eta_int:.12f} vs {4/3*a*a/BS(a):.12f}: {'PASS' if k2 else 'FAIL'}")
# K1: synthetic smooth core a = 6 (inverse-CDF sampling) and synthetic NFW c = 4 (X48's K3)
rng = np.random.default_rng(1); N = 20000; rr = np.geomspace(1e-4, 1, 20001); cdf = BS(6 * rr) / BS(6.0)
rs = np.interp(rng.random(N), cdf, rr); v = rng.standard_normal((N, 3)); v /= np.linalg.norm(v, axis=1)[:, None]
xs = rs[:, None] * v; ms = 1.0 / N; rho_t = 1.0 / (4 / 3 * math.pi) / (18 * math.pi ** 2)
_, rS = fit(xs, ms, rho_t, 1e-4)
k1 = rS is not None and abs(rS["S"]["a"] / 6 - 1) < 0.05
P(f"K1 synthetic smooth core a=6: fitted a {rS['S']['a'] if rS else float('nan'):.3f}, eta {rS['S']['eta'] if rS else float('nan'):.3f}: {'PASS' if k1 else 'FAIL'}")
xn = XA.synthetic_nfw(4.0, 12000, 1); _, rN = fit(xn, 1 / 12000, (1.0) / (4 / 3 * math.pi) / (18 * math.pi ** 2), 1e-4)
P(f"  synthetic NFW c=4 -> smooth-core eta {rN['S']['eta']:.2f} (a {rN['S']['a']:.2f}); Burkert eta {rN['B']['eta']:.2f}  [reference: rule eta_S(c_f 4) = 10.82, X43 Burkert 14.83]")
R = dict(K1=k1, K2=k2, nfw4=rN, runs={})
for d in sorted(glob.glob(os.path.join(X48, "runs", "*"))):
    sn = os.path.join(d, "snap_zf.npz")
    if not os.path.exists(sn): continue
    Z = np.load(sn); x, m = Z["x"], float(Z["m"]); meta = json.loads(str(Z["meta"]))
    rho_mz = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + meta["zf"]) ** 3
    o, res = fit(x, m, rho_mz, meta["eps"])
    if res is None: R["runs"][os.path.basename(d)] = dict(flag=o.get("flag")); continue
    rf = (3 * meta["Mf"] / (4 * math.pi * 18 * math.pi ** 2 * rho_mz)) ** (1 / 3)
    Mv = float((np.sqrt(((x - XA.centre(x, m)) ** 2).sum(1)) <= o["rvir"]).sum() * m)
    eta_rf = res["S"]["eta"] * (Mv / meta["Mf"]) * (rf / o["rvir"]) ** -2 * 1.0   # rho0 r0 / (Delta rho_m r_f)
    eta_rf = (res["S"]["eta"] * (3 * Mv / (4 * math.pi * o["rvir"] ** 2))) / (3 * meta["Mf"] / (4 * math.pi * rf ** 2))
    R["runs"][os.path.basename(d)] = dict(M=meta["M"], seed=meta["seed"], ng=meta["ng"], rvir=o["rvir"], rf=rf, Mv_over_Mf=Mv / meta["Mf"],
                                         S=res["S"], B=res["B"], eta_rf=eta_rf, cf_X48=o.get("cf"), c_nfw=o.get("c_nfw_fit"))
LIM = {12.0: 21.2, 13.0: 14.3, 14.0: 14.3}
P("\nper mass/grid: nine-seed median eta_native (smooth core) [68% boot], Burkert median, eta with r_f, eta-equivalent c_f")
SUM = {}
for M in (1e12, 1e13, 1e14):
    for ng in (38, 48, 64):
        rows = [v for v in R["runs"].values() if v.get("M") == M and v.get("ng") == ng]
        if not rows: continue
        e = np.array([v["S"]["eta"] for v in rows]); b = np.array([v["B"]["eta"] for v in rows]); erf = np.array([v["eta_rf"] for v in rows])
        g = np.random.default_rng(20261026); bt = np.median(e[g.integers(0, len(e), (10000, len(e)))], axis=1)
        med = float(np.median(e)); lo, hi = np.percentile(bt, [16, 84]); ceq = 4 * (med / 10.82) ** 0.8
        SUM[f"{M:.0e}_ng{ng}"] = dict(n=len(rows), eta_med=med, boot68=[float(lo), float(hi)], burk_med=float(np.median(b)),
                                     eta_rf_med=float(np.median(erf)), cf_equiv=ceq, per_seed=sorted(e.tolist()))
        P(f"  M {M:.0e} ng {ng} (n {len(rows)}): eta_S {med:.2f} [{lo:.2f}, {hi:.2f}]  Burkert {np.median(b):.2f}  eta(r_f) {np.median(erf):.2f}  c_f-equiv {ceq:.2f}  limit {LIM[math.log10(M)]}")
R["summary"] = SUM
P("\nGRADE (smooth core)")
g12 = SUM.get("1e+12_ng64"); verdict = {}
for key, lim in (("1e+12_ng64", 21.2), ("1e+13_ng48", 14.3), ("1e+14_ng48", 14.3), ("1e+13_ng64", 14.3), ("1e+14_ng64", 14.3)):
    if key not in SUM: continue
    s = SUM[key]; lab = "INSIDE WINDOW" if s["eta_med"] <= lim else f"OVER x{s['eta_med'] / lim:.2f}"
    verdict[key] = lab; P(f"  {key}: median {s['eta_med']:.2f} vs limit {lim}: {lab}")
if "1e+12_ng48" in SUM and g12:
    sh = g12["eta_med"] / SUM["1e+12_ng48"]["eta_med"] - 1
    R["resolution_1e12"] = sh; P(f"  1e12 ng48 -> ng64 shift {sh:+.1%}: {'RESOLUTION-DEPENDENT' if abs(sh) > 0.2 else 'within 20%'}")
R["verdict"] = verdict
tag = "_MUTATE" if MUT else ""
open(os.path.join(HERE, f"x77{tag}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(R, open(os.path.join(HERE, f"x77_results{tag}.json"), "w"), indent=1, default=float)
sys.exit(0 if (k1 and k2) else 1)
