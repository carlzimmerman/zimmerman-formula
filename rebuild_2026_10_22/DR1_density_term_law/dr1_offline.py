#!/usr/bin/env python3
"""DR1 offline (FROZEN_CRITERIA.md): SPARC, X-COP rows, LITTLE THINGS bracket, from SL1's cache, read only. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, pickle, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
C = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))
MUT = sys.argv[1] if len(sys.argv) > 1 else None   # zero | three
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
UPS = C["UPS"]; A0 = C["const"]["A0"]; G = C["const"]["GE"]; MS = C["const"]["MSUNE"]; MPC = C["const"]["MPCE"]; GALS = C["gals"]
def combine(gb, gs, a0, rd):
    if rd == "R1": return 0.5 * gb + np.sqrt(0.25 * gb ** 2 + a0 * gs)
    if rd == "R2": return gb + np.sqrt(a0 * gs)
    return np.sqrt(gb ** 2 + a0 * gs)
def sfac(S): return np.zeros_like(S) if MUT == "zero" else (np.full_like(S, 3.0) if MUT == "three" else S)
def sparc_gs(q, c):
    """g_s on (npts, nups). (4 pi G r/3) rho_b = (1/(3r)) d(r^2 g_b)/dr, floored at rho_b = 0."""
    R, GB = q["Rm"], q["GB"]
    if c == 0: return GB.copy()
    if MUT == "zero": return GB.copy()
    if MUT == "three": return GB * (1 + c)
    dM = np.gradient(R[:, None] ** 2 * GB, R, axis=0) if len(R) >= 2 else np.zeros_like(GB)
    return GB + c * np.maximum(dM, 0.0) / (3 * R[:, None])
def fit_one(q, lg):
    OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lg, 0.0); Wm = np.where(OK, W[:, None], 0.0)
    wr2 = (Wm * r * r).sum(0); ws = Wm.sum(0); i = int(np.argmin(wr2 / np.maximum(ws, 1e-300))); return wr2[i], ws[i], i
BIN = ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400))
def sparc(f, c, rd):
    a0 = A0[f]; rows = []; U = {}
    for q in GALS:
        gb = np.maximum(q["GB"], 1e-300); gs = np.maximum(sparc_gs(q, c), 1e-300); g = combine(gb, gs, a0, rd); w, s, i = fit_one(q, np.log10(g)); rows.append((w, s)); U[q["name"]] = float(UPS[i])
    rms = math.sqrt(sum(r[0] for r in rows) / sum(r[1] for r in rows)); u = np.array([U[q["name"]] for q in GALS]); v = np.array([q["vf"] for q in GALS]); Q = np.array([q["Q"] <= 2 and q["inc"] >= 30 for q in GALS]); um = float(np.median(u))
    return dict(rms=rms, U=um, line=bool(rms <= 0.110 and 0.5 <= um <= 0.8), tilt=float(np.median(u[Q & (v > 0) & (v < 100)]) - np.median(u[Q & (v > 150)])), bins={f"{a}-{b}": float(np.median(u[Q & (v >= a) & (v < b)])) for a, b in BIN}, chi2=float(sum(r[0] for r in rows)), n=float(sum(r[1] for r in rows)))
# HS1's slope at 2 R_d
TB = {}
for l in open(os.path.join(RB, "..", "real_research", "data", "SPARC_Lelli2016c.mrt")):
    p = l.split()
    if len(p) < 18: continue
    try: TB[p[0]] = dict(sb=float(p[10]), rd=float(p[11]), vf=float(p[15]), Q=int(p[17]), inc=float(p[5]))
    except ValueError: pass
def hs1(f, c, rd):
    iu = int(np.argmin(abs(UPS - 0.5))); x = []; y = []; a0 = A0[f]; KPC = MPC / 1e3
    for q in GALS:
        t = TB.get(q["name"])
        if not t or not (60 <= t["vf"] < 120) or t["Q"] > 2 or t["inc"] < 30 or t["sb"] <= 0: continue
        ok = q["OK"][:, iu]; Rk = q["Rm"] / KPC; R2 = 2 * t["rd"]
        if ok.sum() < 2 or R2 < Rk[ok].min() or R2 > Rk[ok].max(): continue
        gb = np.maximum(q["GB"][:, iu], 1e-300); gs = np.maximum(sparc_gs(q, c)[:, iu], 1e-300); g = combine(gb, gs, a0, rd); Vm = np.sqrt(np.maximum(g * q["Rm"], 0)) / 1e3; Vo = np.sqrt(q["GO"] * q["Rm"]) / 1e3
        x.append(math.log10(t["sb"])); y.append(float(np.interp(math.log(R2), np.log(Rk[ok]), Vm[ok] / Vo[ok] - 1)))
    x = np.array(x); y = np.array(y); xx = x - x.mean(); sl = lambda a, b: float(((a - a.mean()) * (b - b.mean())).sum() / ((a - a.mean()) ** 2).sum()); r = np.random.default_rng(1); bs = []
    for _ in range(2000):
        k = r.integers(0, len(x), len(x)); bs.append(sl(x[k], y[k]))
    return dict(slope=sl(x, y), se=float((np.percentile(bs, 84) - np.percentile(bs, 16)) / 2), n=len(x), mean=float(y.mean()))
# X-COP rows
def xcop(f, c, rd):
    a0 = A0[f]; D = []; bx = {}; Sr = []; Ss = []; by = {}
    for r in C["xcop"]["canonical"]["rows"]: by.setdefault(r["cluster"], []).append(r)
    for nm, rs in by.items():
        rs = sorted(rs, key=lambda z: z["r_kpc"]); rr = np.array([z["r_kpc"] for z in rs]) * 1e3 * MPC / 1e6; Mb = np.array([z["Mb_Msun"] for z in rs]) * MS; Mh = np.array([z["MHSE_Msun"] for z in rs]) * MS
        S = sfac(np.maximum(np.gradient(np.log(Mb), np.log(rr)), 0.0)); gb = G * Mb / rr ** 2; g = combine(gb, gb * (1 + c * S / 3), a0, rd); Ml = g * rr ** 2 / G; go = G * Mh / rr ** 2
        for k, z in enumerate(rs):
            if z["x"] > 0.75: continue
            v = math.log10(Mh[k] / Ml[k]); D.append(v); bx.setdefault(f"{z['x']:g}", []).append(v); Sr.append(3 * (go[k] * (go[k] - gb[k]) / (a0 * gb[k]) - 1)); Ss.append(float(S[k]))
    d = np.array(D); return dict(mean=float(d.mean()), rms=float(np.sqrt((d ** 2).mean())), n=len(d), by_x={k: float(np.mean(v)) for k, v in bx.items()}, PASS=bool(abs(d.mean()) <= 0.05 and np.sqrt((d ** 2).mean()) <= 0.10), S_med=float(np.median(Ss)), S_req_med=float(np.median(Sr)), S_req_frac_over3=float(np.mean(np.array(Sr) > 3)), S_by_row=None)
def lt(f, S):
    a0 = A0[f]; E = []
    for r in C["lt"]:
        Rm = r["R"] * MPC / 1e3; gb = G * 10 ** r["logMb"] * MS / Rm ** 2; E.append(math.log10((r["V"] * 1e3) ** 2 / Rm) - math.log10(combine(gb, gb * (1 + S / 3), a0, "R1")))
    return float(np.median(E))
def last_S():
    iu = int(np.argmin(abs(UPS - 0.5))); o = []
    for q in GALS:
        ok = q["OK"][:, iu]
        if ok.sum() < 3: continue
        M = q["Rm"] ** 2 * q["GB"][:, iu]; dM = np.gradient(M, q["Rm"]) * q["Rm"] / np.maximum(M, 1e-300); o.append(max(float(dM[ok][-1]), 0.0))
    return float(np.median(o))
R = dict(sparc={}, xcop={}, hs1={}, lt={}); ROWS = [("R1", 0), ("R1", 1), ("R1", 3), ("R2", 0), ("R2", 1), ("R3", 0), ("R3", 1), ("R3", 3)]
for rd, c in ROWS:
    k = f"{rd}|c{c}"; R["sparc"][k] = {f: sparc(f, c, rd) for f in ("canonical", "alt")}; R["xcop"][k] = {f: xcop(f, c, rd) for f in ("canonical", "alt")}; R["hs1"][k] = hs1("canonical", c, rd)
    s = R["sparc"][k]; x = R["xcop"][k]["canonical"]; h = R["hs1"][k]
    P(f"{k}: SPARC can rms {s['canonical']['rms']:.4f} U {s['canonical']['U']:.2f} tilt {s['canonical']['tilt']:+.2f} line {s['canonical']['line']}; alt rms {s['alt']['rms']:.4f} U {s['alt']['U']:.2f} tilt {s['alt']['tilt']:+.2f} line {s['alt']['line']}; bins {[round(v, 2) for v in s['canonical']['bins'].values()]}; chi {s['canonical']['chi2']:.1f}; HS1 {h['slope']:+.3f}+-{h['se']:.3f} n{h['n']}; X-COP can mean {x['mean']:+.3f} rms {x['rms']:.3f} alt {R['xcop'][k]['alt']['mean']:+.3f} by x {x['by_x']} S {x['S_med']:.2f} S_req {x['S_req_med']:.1f} frac>3 {x['S_req_frac_over3']:.2f}")
R["lt"] = {f"S{s}": lt("canonical", s) for s in (0, 1, 3)}; R["last_S_median"] = last_S(); P(f"LITTLE THINGS bracket, not graded: {R['lt']}; median S at SPARC's last point, Upsilon 0.5 (R_max still inside gas?): {R['last_S_median']:.2f}")
# checks
if MUT is None:
    s0 = R["sparc"]["R1|c0"]; k1 = max(abs(s0["canonical"]["rms"] - 0.054087447879939264), abs(s0["alt"]["rms"] - 0.05371798965550355)); k1u = s0["canonical"]["U"] == 0.52 and s0["alt"]["U"] == 0.44
    k3 = abs(R["lt"]["S0"] + 0.025); gb = np.array([1e-11, 1e-10, 1e-9]); k4a = float(np.max(np.abs(combine(gb, gb * 2, 1e-10, "R1") - (0.5 * gb + np.sqrt(0.25 * gb ** 2 + 2e-10 * gb))))); k4b = float(np.max(np.abs(combine(gb, gb, 1e-10, "R1") - gb * (0.5 + np.sqrt(0.25 + 1e-10 / gb)))))
    hj = json.load(open(os.path.join(RB, "HS1_hsb_lsb_residual_slope", "hs1_results.json"))); k6 = R["sparc"]["R3|c3"]["canonical"]["chi2"] > R["sparc"]["R3|c0"]["canonical"]["chi2"]
    P(f"K1 {k1:.1e} U {k1u}; K3 {k3:.4f}; K4 {k4a:.1e} {k4b:.1e}; K6 c3 worse than c0 on R3 {k6} (chi {R['sparc']['R3|c0']['canonical']['chi2']:.0f} -> {R['sparc']['R3|c3']['canonical']['chi2']:.0f}); HS1 keys {list(hj)[:12]}")
    R["checks"] = dict(K1=k1, K1U=k1u, K3=k3, K4=[k4a, k4b], K6=bool(k6))
tag = f"_MUTATE_{MUT}" if MUT else ""
json.dump(R, open(os.path.join(HERE, f"dr1_offline{tag}.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"dr1_offline{tag}.out"), "w").write("\n".join(OUT) + "\n")
