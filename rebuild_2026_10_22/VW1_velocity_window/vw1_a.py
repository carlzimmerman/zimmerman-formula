#!/usr/bin/env python3
"""VW1 Stage A: slowest v0 massive discs allow, by HF1's own profile (R4) and solver, read-only. Criteria: FROZEN_CRITERIA.md. VW1_MUTATE=1: f_hi x 16, separate outputs.
kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); HF = os.path.join(os.path.dirname(HERE), "HF1_hybrid_fermion"); sys.path.insert(0, HF); sys.dont_write_bytecode = True
sys.argv = ["hf1_g23.py"]
import hf1_g23 as H
import numpy as np
from scipy.integrate import quad
MUT = os.environ.get("VW1_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
FM = H.FM; FAIR = 5.2715; HJ, CL, EV = FM.H_J, FM.C_L, FM.EV; RHOC_H2 = 1.8784e-26
MG = np.geomspace(1.0, 300.0, 25)
def Qof(m, gf=2.0): return (m * EV / CL ** 2) ** 4 * (gf / 2) / HJ ** 3
FD_I = 8 * math.pi * quad(lambda x: x * x / (math.exp(x) + 1), 0, 200)[0]
SHAPES = dict(FD=lambda r, Q: 3.15137 * (r / (FD_I * Q)) ** (1 / 3), Maxwell=lambda r, Q: 1.59577 * (r / ((2 * math.pi) ** 1.5 * Q)) ** (1 / 3), TopHat=lambda r, Q: 0.75 * (r / (4 * math.pi / 3 * Q)) ** (1 / 3))
def ratios(g, a0):
    VB2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + .5 * g["Vdisk"] ** 2 + .7 * g["Vbul"] ** 2; gb = VB2 * 1e6 / g["R"]; gb = np.maximum(gb, 1e-30)[None, :]
    Mbl = float(gb[0, -1] * g["R"][-1] ** 2 / H.GF); out = []
    for m in MG:
        Mfr = H.gal_model(g, gb, np.array([0.5]), FAIR, float(m), a0)[1]; out.append(float(Mfr[0, -1]) / Mbl)
    return np.array(out)
def m_at(rt, lim):
    """m where the ratio crosses lim, log interpolated; inf if the cap never binds, 0 if it's over at the lowest m."""
    if rt[-1] <= lim: return math.inf
    if rt[0] >= lim: return 0.0
    i = int(np.argmax(rt >= lim)); a, b = math.log(max(rt[i - 1], 1e-300)), math.log(rt[i]); t = (math.log(lim) - a) / (b - a); return float(math.exp(math.log(MG[i - 1]) + t * math.log(MG[i] / MG[i - 1])))
def main():
    out = []
    def P(s=""): print(s, flush=True); out.append(str(s))
    P("VW1 Stage A, criteria in FROZEN_CRITERIA.md" + ("  [MUTATE f_hi x 16]" if MUT else "")); G = [g for g in H.SP.load_gal() if g["lgMb"] >= 10 and g["Q"] < 3 and g["Inc"] >= 30 and float(g["gas_ok"] if "gas_ok" in g else 1)]
    res = dict(n=len(G), checks={}, feet={})
    ck = res["checks"]; ck["K_integral"] = dict(val=FD_I, expect=45.3, passed=abs(FD_I / (8 * math.pi * 1.8030857) - 1) < 1e-4)
    g0 = G[0]; rt0 = ratios(g0, H.A0["canonical"]); mp = 17.3; VB2 = np.sign(g0["Vgas"]) * g0["Vgas"] ** 2 + .5 * g0["Vdisk"] ** 2 + .7 * g0["Vbul"] ** 2; gb0 = np.maximum(VB2 * 1e6 / g0["R"], 1e-30)[None, :]
    lim0 = float(H.gal_model(g0, gb0, np.array([0.5]), FAIR, mp, H.A0["canonical"])[1][0, -1]) / float(gb0[0, -1] * g0["R"][-1] ** 2 / H.GF); mr = m_at(rt0, lim0); ck["K_planted"] = dict(planted=mp, recovered=mr, Q_ratio=(mr / mp) ** 4, passed=abs((mr / mp) ** 4 - 1) <= 0.01 if math.isfinite(mr) else False)
    for ft in H.FEET:
        rows = {g["name"]: ratios(g, H.A0[ft]) for g in G}; R = dict(lim={})
        for fh in (0.1, 0.2, 0.4):
            fe = fh * (16 if MUT else 1); lim = fe * FAIR; ms = {n: m_at(r, lim) for n, r in rows.items()}; a = np.array(sorted(ms.values())); Q = np.array([Qof(x) if math.isfinite(x) else math.inf for x in a])
            q = {p: float(np.percentile(a, p, method="nearest")) for p in (16, 50, 84)}; v = {}
            for wf in (0.11, 0.13, 0.15):
                for sh, fn in SHAPES.items():
                    for p, mm in q.items():
                        v[f"{sh}_w{wf}_p{p}"] = fn(wf * RHOC_H2, Qof(mm)) / 1e3 if (mm > 0 and math.isfinite(mm)) else None
            R["lim"][str(fh)] = dict(m_16_50_84=q, n_never_binds=int(np.isinf(a).sum()), n_over_at_1eV=int((a == 0).sum()), v0_km_s=v, per_gal={k: (x if math.isfinite(x) else None) for k, x in ms.items()})
            P(f"{ft} f_hi {fe:g}: n {len(a)}, m at equality 16/50/84 %: {q[16]:.2f} {q[50]:.2f} {q[84]:.2f} eV; never binds {int(np.isinf(a).sum())}; v_min(FD, w 0.13) 84/50/16 of m -> " + " ".join("n/a" if v[f"FD_w0.13_p{p}"] is None else f"{v[f'FD_w0.13_p{p}']:.2f}" for p in (84, 50, 16)) + " km/s")
            P(f"     shapes at median, w 0.13: " + " ".join(f"{s} {v[f'{s}_w0.13_p50']:.2f}" if v[f"{s}_w0.13_p50"] is not None else f"{s} n/a" for s in SHAPES) + "; w 0.11, 0.15 FD: " + " ".join(str(None if v[f'FD_w{w}_p50'] is None else round(v[f'FD_w{w}_p50'], 2)) for w in (0.11, 0.15)))
        res["feet"][ft] = R
    P("checks: " + ", ".join(f"{k} {v['passed']}" for k, v in ck.items())); P("kappa = 1/2 FITTED. Not theory closed.")
    json.dump(res, open(os.path.join(HERE, f"vw1_a{TAG}.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"vw1_a{TAG}.out"), "w").write("\n".join(out) + "\n")
main()
