#!/usr/bin/env python3
"""QX7 iter_7 (criteria c302aa5804 + A1): iter_4 Jeans-switch retention + a phase-mixed remnant tracing the host's hot gas.
    python3 qx7_iter7.py   # writes qx7_iter7.json / .out (graded SHAPE label, reported galaxy gates, K1, K2, MUTATE A-C)
Plain law per footing. iter_5's code (loaders, host profiles, gates, predictor) is executed from its own source.
kappa = 1/2 FITTED; not theory closed. 1 thread."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); TAG = "qx7_iter7"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
I5 = os.path.join(HERE, "..", "iter_5_host_hydrostatic", "qx7_iter5.py")
s5 = open(I5).read(); s5 = s5[:s5.index("# ---- K1:")]
argv0, sys.argv = sys.argv, [I5]
NS = {"__file__": os.path.abspath(I5), "__name__": "iter5_reused"}
exec(compile(s5, I5, "exec"), NS); sys.argv = argv0
A0, ST4, XC, KPC, MS, MPC, R, FCAP, r_ta0 = (NS[k] for k in ("A0", "ST4", "XC", "KPC", "MS", "MPC", "R", "FCAP", "r_ta0"))
lens_mean, ell_mean, gal_gates, predict, ISO, BASE, pl_profile, XPROF = (NS[k] for k in ("lens_mean", "ell_mean", "gal_gates", "predict", "ISO", "BASE", "pl_profile", "XPROF"))
I2 = NS["I2"]; DATA = NS["DATA"]
# X-COP gas-only profiles (the remnant's shape), normalised at Mb_last's radius
XGAS = {}
for name in sorted({z["name"] for z in XC}):
    with fits.open(os.path.join(DATA, "xcop", name, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = h[1].header["R500"]
    gr = np.array(gas["RADIUS"], float) * rg500; gM = np.array(gas["MGAS"], float); ok = np.isfinite(gM) & (gM > 0) & (gr > 0)
    fg = pl_profile(gr[ok], gM[ok]); tl = next(z["Mb_last"] for z in XC if z["name"] == name)[1]; Gt = float(fg(tl))
    XGAS[name] = lambda r, fg=fg, tl=tl * KPC, Gt=Gt: np.where(np.asarray(r) > tl, 1.0, fg(np.asarray(r, float) / KPC) / Gt)

def provider(fcap=FCAP, retain="switch", shape="gas"):
    def prov(key, fM, Mt, lam0, a0):
        keep = (lam0 / 2 < r_ta0(Mt)) if retain == "switch" else True
        if not keep or fcap == 0: return lambda r: 0.0 * np.asarray(r, float)
        Md = fcap * R * Mt
        if key[0] == "X":
            if shape == "gas": return lambda r, n=key[1]: Md * XGAS[n](r)
            fx, Ml = XPROF[key[1]]; return lambda r, fx=fx, Ml=Ml: Md * fx(np.asarray(r, float)) / Ml
        if key[0] in ("G", "E"): return lambda r, fM=fM: Md * np.minimum(np.asarray(fM(r), float) / Mt, 1.0)
        return lambda r: Md + 0.0 * np.asarray(r, float)     # point-mass hosts (KiDS, G5): all dust inside r
    return prov
TRACE = provider()
RES = dict(tag=TAG, criteria="c302aa5804 + A1", note="kappa = 1/2 FITTED; not theory closed. Galaxy gates are BY ASSUMPTION (A1).")
P(f"QX7 iter7: switch retention + gas-tracing remnant; f_cap {FCAP}, R {R:.3f}")

# K1: isolated core provider = iter_4 at 2.154 (as iter_5 MUTATE A)
I4 = ST4["cluster_vs_lambda0_galaxyok"]; k = min(I4, key=lambda s: abs(math.log(float(s) / 2.154))); pk = predict(float(k), ISO())
K1 = all(abs(pk[f]["X_mean"] - I4[k][f]["X_mean"]) <= 2e-3 and abs(pk[f]["X_rms"] - I4[k][f]["X_rms"]) <= 2e-3 for f in A0)
P(f"  K1 (iter_4 core): " + ", ".join(f"{f} {pk[f]['X_mean']:+.4f}/{pk[f]['X_rms']:.4f} vs {I4[k][f]['X_mean']:+.4f}/{I4[k][f]['X_rms']:.4f}" for f in A0) + f" -> {'PASS' if K1 else 'FAIL'}")
# K2: everyone keeps, baryon tracing = QX29 B1 (-0.003 / -0.027)
p2 = predict(2.154, provider(retain="all", shape="baryon")); K2 = abs(p2["canonical"]["X_mean"] + 0.003) <= 0.01 and abs(p2["alt"]["X_mean"] + 0.027) <= 0.01
P(f"  K2 (QX29 B1 reproduction): X-COP {p2['canonical']['X_mean']:+.4f}/{p2['canonical']['X_rms']:.3f}, {p2['alt']['X_mean']:+.4f}/{p2['alt']['X_rms']:.3f} vs -0.003/0.082, -0.027/0.087 -> {'PASS' if K2 else 'MISS (disclosed)'}")
RES.update(K1=dict(pass_=bool(K1)), K2=dict(mine=(p2["canonical"]["X_mean"], p2["alt"]["X_mean"]), pass_=bool(K2)))

wl0 = sorted({c["lambda_0"] for c in ST4["window"]}); rows = {}
for l0 in wl0:
    g = gal_gates(l0, TRACE, BASE); pr = predict(l0, TRACE); pb = predict(l0, provider(shape="baryon"))
    eD = {f: ell_mean(a0, l0, TRACE) - BASE[f]["E"] for f, a0 in A0.items()}
    eabs = {f: ell_mean(a0, l0, TRACE) for f, a0 in A0.items()}
    nE = sum(1 for e in NS["EL"] if l0 / 2 < r_ta0(e["Mbar"](1e9)))
    shp = all(pr[f]["X_pass"] and pr[f]["groups_strict"] for f in A0) and g[2]
    rows[f"{l0:.4g}"] = dict(gates_by_assumption=list(g)[:2], G7=g[2], ell_shift=eD, ell_abs=eabs, n_ell_retain=nE, gas=pr, baryon_reported=pb, shape_pass=bool(shp))
    P(f"   lambda_0 {l0:.3g}: ellipticals keeping dust {nE}/7, G7 shift " + ", ".join(f"{f} {eD[f]:+.3f}" for f in A0)
      + " | gas-traced X-COP " + "; ".join(f"{f} {pr[f]['X_mean']:+.3f}/{pr[f]['X_rms']:.3f} groups {pr[f]['groups']['fst0']['n_pass']}/{pr[f]['groups']['fst1']['n_pass']}" for f in A0)
      + " | baryon-traced X-COP " + "; ".join(f"{f} {pb[f]['X_mean']:+.3f}/{pb[f]['X_rms']:.3f}" for f in A0) + f" -> {'SHAPE PASS' if shp else 'shape fail'}")
RES["rows"] = rows
okl = [k for k, v in rows.items() if v["shape_pass"]]
win = [c for c in ST4["window"] if f"{c['lambda_0']:.4g}" in okl]
lab = (f"SHAPE PASS (scoped, CONDITIONAL on the pressureless remnant and on iter_4's refuted retention) at lambda_0 {okl}, {len(win)} window cells" if okl else "SHAPE FAIL")
# MUTATEs
mA = predict(2.154, provider(fcap=0.0)); okA = abs(mA["canonical"]["X_mean"] - 0.4675) <= 1e-3 and abs(mA["alt"]["X_mean"] - 0.4345) <= 1e-3
g = gal_gates(1e-3, TRACE, BASE); okB = not (g[0] and g[1])
mv = {f: predict(2.154, provider(fcap=0.3 * FCAP))[f]["X_mean"] - predict(2.154, TRACE)[f]["X_mean"] for f in A0}; okC = all(abs(v) > 0.1 for v in mv.values())
P(f"  MUTATE A (f_cap 0): {mA['canonical']['X_mean']:+.4f} / {mA['alt']['X_mean']:+.4f} -> {'PASS' if okA else 'FAIL'}; MUTATE B (lambda_0 1e-3): {g} -> {'BITES' if okB else 'NO BITE'}; "
  f"MUTATE C (f_cap x0.3): move " + ", ".join(f"{f} {v:+.3f}" for f, v in mv.items()) + f" -> {'BITES' if okC else 'NO BITE'}")
RES.update(MUTATE_A=bool(okA), MUTATE_B=dict(gates=list(g), bites=bool(okB)), MUTATE_C=dict(move=mv, bites=bool(okC)))
if not (K1 and okA and okB and okC): lab = "NO VERDICT (control failed) | numbers read " + lab
RES["label"] = lab; P(f"  LABEL: {lab}")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
