#!/usr/bin/env python3
"""CFG397: M/L-free a0 rung from SPARC gas-dominated points (criteria FROZEN_CRITERIA.md). Run: python3 cfg397_gas_rung.py [--mutate]"""
import os, sys, json, math, io, contextlib
import numpy as np
from scipy.optimize import minimize_scalar
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
OUT = []
def P(s=""): print(s); OUT.append(str(s))
KPC = 3.0857e19
GAL = [g for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2]
def sel_points(g):
    vg = 0 * g["Vgas"] if MUT else g["Vgas"]
    vg2 = np.sign(vg) * vg ** 2
    vb2 = vg2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    return (vg2 >= 0.7 * vb2) & (vb2 > 0) & (g["Vobs"] > 0)
def arrays(gs, U):
    out = []
    for g in gs:
        m = sel_points(g); R = g["R"][m] * KPC
        vg = 0 * g["Vgas"][m] if MUT else g["Vgas"][m]
        b = (np.sign(vg) * vg ** 2 + U * g["Vdisk"][m] ** 2 + 1.4 * U * g["Vbul"][m] ** 2) * 1e6 / R
        o = (g["Vobs"][m] * 1e3) ** 2 / R
        w = 1 / (np.clip(g["eV"][m], 1, None) / np.clip(g["Vobs"][m], 1, None)) ** 2
        ok = (b > 0) & (o > 0)
        out.append((b[ok], o[ok], w[ok]))
    return out
def fit(parts):
    gb = np.concatenate([p[0] for p in parts]); go = np.concatenate([p[1] for p in parts]); w = np.concatenate([p[2] for p in parts])
    lgo, lgb = np.log10(go), np.log10(gb)
    f = lambda la: np.sum(w * (lgo - lgb - np.log10(C.nu_mono(gb / 10 ** la))) ** 2)
    return minimize_scalar(f, bounds=(-10.8, -9.3), method="bounded", options={"xatol": 1e-5}).x
use = [g for g in GAL if sel_points(g).sum() >= 3]
P(f"CFG397 gas-dominated rung{' [MUTATE: gas dropped]' if MUT else ''}: {len(use)} galaxies with >= 3 gas-dominated points (of {len(GAL)} Q<=2)")
if len(use) == 0:
    P("MUTATE: empty selection detected -> exit 1"); open(os.path.join(HERE, f"cfg397_gas_rung{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1)
classes = {"A all": (1, 2, 3, 4, 5), "B ladder (TRGB/Cep/SNe)": (2, 3, 5), "C Hubble flow": (1,)}
res = {}
for nm, fd in classes.items():
    gs = [g for g in use if g["meta"]["fD"] in fd]
    parts = arrays(gs, 0.5); la = fit(parts)
    rng = np.random.default_rng(7)
    bs = [fit([parts[i] for i in rng.integers(0, len(parts), len(parts))]) for _ in range(500)]
    res[nm] = dict(n=len(gs), log_a0=float(la), sd=float(np.std(bs)), npts=int(sum(len(p[0]) for p in parts)))
    P(f"  {nm:24s} N gal {len(gs):3d} pts {res[nm]['npts']:4d}: a0 = {10**la:.3e} (log {la:+.3f} +- {np.std(bs):.3f})")
k1 = {U: float(fit(arrays(use, U))) for U in (0.3, 0.5, 0.7)}
dk = k1[0.7] - k1[0.5]; k1ok = abs(dk) <= 0.05
P(f"K1 Upsilon-insensitivity: log a0 at Upsilon 0.3/0.5/0.7 = {k1[0.3]:+.3f}/{k1[0.5]:+.3f}/{k1[0.7]:+.3f}; 0.5->0.7 shift {dk:+.3f} -> {'PASS' if k1ok else 'FAIL'}")
B = res["B ladder (TRGB/Cep/SNe)"]
est = B["sd"] <= 0.05 and k1ok
P(f"RUNG {'ESTABLISHED' if est else 'NOT ESTABLISHED'} (anchor sd {B['sd']:.3f}, K1 {'pass' if k1ok else 'fail'})")
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10), ("PAPER43 gas-point", 8.3e-11)):
    d = B["log_a0"] - math.log10(a0)
    P(f"  anchor vs {foot:18s} {a0:.3e}: {d:+.3f} dex ({d / B['sd']:+.2f} sigma) -> {'consistent' if abs(d) < 2 * B['sd'] else 'differs'}")
c301 = json.load(open(os.path.join(LANES, "CFG301_mightee_hi_catalogue_width_chain", "cfg301_stageB_results.json")))
s = json.dumps(c301); i = s.find('"(ii) gas-dominated (M_gas > M*)": {')
sub = json.loads(s[i + len('"(ii) gas-dominated (M_gas > M*)": '):].split(', "recipe"')[0] + "}")
P(f"  CFG301 MeerKAT (ii) gas-dominated BTFR (reported): N {sub['n']}, median a0 {sub['median']:.3e} (log {math.log10(sub['median']):+.3f}); anchor minus it {B['log_a0'] - math.log10(sub['median']):+.3f} dex")
C_ = res["C Hubble flow"]; dfl = C_["log_a0"] - B["log_a0"]
P(f"  flow - ladder (gas-only) = {dfl:+.3f} +- {math.hypot(C_['sd'], B['sd']):.3f} dex")
json.dump(dict(res=res, K1=k1, established=est, cfg301_gas=sub["median"]), open(os.path.join(HERE, f"cfg397_gas_rung{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg397_gas_rung{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0)
