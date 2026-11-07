#!/usr/bin/env python3
"""QX7 iter_6 (criteria c302aa5804 + A1): iter_5's host-held dust with the measured external field capping every well.
    python3 qx7_iter6.py            # graded: qx7_iter6.json / .out
    python3 qx7_iter6.py --mutate   # K1, K2, MUTATE A-C: qx7_iter6_MUTATE.json / .out
Law in every host and in every prediction: g = g_law(g_N + g_Ne) - g_law(g_Ne) (1D EFE form), g_Ne = e_N * 1.2e-10.
iter_5's code (prelude, solver, gates, predictor) is executed from its own source; only the law function is swapped.
kappa = 1/2 FITTED; not theory closed. 1 thread."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = "--mutate" in sys.argv; TAG = "qx7_iter6_MUTATE" if MUT else "qx7_iter6"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
I5 = os.path.join(HERE, "..", "iter_5_host_hydrostatic", "qx7_iter5.py")
s5 = open(I5).read(); s5 = s5[:s5.index("# ---- K1:")]
argv0, sys.argv = sys.argv, [I5]
NS = {"__file__": os.path.abspath(I5), "__name__": "iter5_reused"}
exec(compile(s5, I5, "exec"), NS); sys.argv = argv0
A0, ST4, l0s_ = NS["A0"], NS["ST4"], None
GLAW0 = NS["glaw"]; I5J = json.load(open(os.path.join(HERE, "..", "iter_5_host_hydrostatic", "qx7_iter5.json")))
EN_PRIMARY = 0.0033; EN_BRACKET = {"noclu_median": 0.0004, "maxclu_p84": 0.0052, "x8_ceiling": 0.026}
STATE = {"gNe": 0.0}
def glaw_efe(gN, a0):
    ge = STATE["gNe"]
    return GLAW0(gN + ge, a0) - GLAW0(ge, a0)
NS["glaw"] = glaw_efe   # every iter_5 function looks up glaw in this namespace
def set_en(en):
    STATE["gNe"] = en * 1.2e-10; NS["CACHE"].clear()
    NS["BASE"] = {f: dict(L=NS["lens_mean"](a0, 1e9, NS["ISO"](0.0)), E=NS["ell_mean"](a0, 1e9, NS["ISO"](0.0))) for f, a0 in A0.items()}
lens_mean, ell_mean, gal_gates, predict, HOST, ISO = (NS[k] for k in ("lens_mean", "ell_mean", "gal_gates", "predict", "HOST", "ISO"))
def shift(l0):
    return {f: lens_mean(a0, l0, HOST) - NS["BASE"][f]["L"] for f, a0 in A0.items()}
RES = dict(tag=TAG, criteria="c302aa5804 + A1", e_N_primary=EN_PRIMARY, note="kappa = 1/2 FITTED; not theory closed")
P(f"QX7 iter6 {TAG}: EFE 1D form, e_N primary {EN_PRIMARY} (g_Ne {EN_PRIMARY * 1.2e-10:.3e})")
l0s = np.geomspace(1e-3, 1e2, 61)
if not MUT:
    set_en(EN_PRIMARY)
    # law + EFE baseline absolute misfit (clue, ungraded)
    RES["baseline_abs"] = {f: dict(KiDS_mean=NS["BASE"][f]["L"], ell_mean=NS["BASE"][f]["E"]) for f in A0}
    P("  law+EFE baseline (no dust): " + "; ".join(f"{f} KiDS mean {NS['BASE'][f]['L']:+.3f}, ellipticals {NS['BASE'][f]['E']:+.3f}" for f in A0)
      + f" | isolated law: KiDS {I5J['baselines']['canonical']['L']:+.3f} / {I5J['baselines']['alt']['L']:+.3f}")
    galok = {}
    for l0 in l0s:
        try: galok[float(l0)] = gal_gates(float(l0), HOST, NS["BASE"])
        except RuntimeError as ex: galok[float(l0)] = ("ERR", str(ex))
    l0_gal = [l0 for l0, g in galok.items() if g[0] is True and all(g)]
    nerr = sum(1 for g in galok.values() if g[0] == "ERR")
    P(f"  galaxy gates (EFE) pass for {len(l0_gal)}/61 lambda_0" + (f": {min(l0_gal):.3g}-{max(l0_gal):.3g} Mpc" if l0_gal else "") + f"; solver errors {nerr}")
    RES["galaxy_gates_by_lambda0"] = {f"{k:.4g}": list(v) for k, v in galok.items()}
    okset = {round(math.log(l0), 6) for l0 in l0_gal}
    window = [c for c in ST4["evaluated"] if c["dchi2"] <= NS["I2"].DCHI2_LINE and round(math.log(c["lambda_0"]), 6) in okset]
    P(f"  window: {len(window)} cells"); RES["window"] = window
    wl0 = sorted({c["lambda_0"] for c in ST4["window"]})
    RES["shift_iter4_window"] = {}
    for l0 in wl0:
        s = shift(l0); RES["shift_iter4_window"][f"{l0:.4g}"] = s
        P(f"   lambda_0 {l0:.3g}: KiDS shift " + ", ".join(f"{f} {v:+.3f}" for f, v in s.items()) + f"  (iter_5 isolated: see iter_5)")
    preds = {f"{l0:.4g}": predict(l0, HOST) for l0 in sorted(set(l0_gal) | set(wl0))}; RES["predictions"] = preds
    for k, pr in preds.items():
        P(f"   [clusters] lambda_0 {k}: " + "; ".join(f"{f} X {pr[f]['X_mean']:+.3f}/{pr[f]['X_rms']:.3f} groups {pr[f]['groups']['fst0']['n_pass']}/{pr[f]['groups']['fst1']['n_pass']}" for f in A0))
    if not window: lab = "FAIL (no window)"
    else:
        both = {f: sum(1 for c in window if preds[f"{c['lambda_0']:.4g}"][f]["X_pass"] and preds[f"{c['lambda_0']:.4g}"][f]["groups_strict"]) for f in A0}
        lab = ("PASS" if all(v > 0 for v in both.values()) else "FAIL (clusters)") + " [" + ", ".join(f"{f} {both[f]}/{len(window)}" for f in A0) + "]"
    RES["label"] = lab; P(f"  LABEL (primary e_N): {lab}")
    # bracket (reported only): KiDS shift and X-COP at the iter_4-window lambda_0
    RES["bracket"] = {}
    for nm, en in EN_BRACKET.items():
        set_en(en); row = {}
        for l0 in wl0:
            s = shift(l0); pr = predict(l0, HOST); row[f"{l0:.4g}"] = dict(shift=s, X={f: (pr[f]["X_mean"], pr[f]["X_rms"]) for f in A0})
        RES["bracket"][nm] = row
        best = min(row.items(), key=lambda kv: abs(kv[1]["shift"]["canonical"]))
        P(f"  [bracket {nm} e_N {en}] smallest |KiDS shift| in window: lambda_0 {best[0]} canonical {best[1]['shift']['canonical']:+.3f} alt {best[1]['shift']['alt']:+.3f}; X-COP there {best[1]['X']['canonical'][0]:+.3f}/{best[1]['X']['canonical'][1]:.3f}")
else:
    # K1: e_N = 0 reproduces iter_5
    set_en(0.0); s = shift(2.154); pr = predict(2.154, HOST)
    i5 = I5J["reported_clusters_iter4_window"]["2.154"]
    k1 = all(abs(pr[f]["X_mean"] - i5[f]["X_mean"]) <= 1e-4 for f in A0)
    RES["K1"] = dict(shift=s, X={f: pr[f]["X_mean"] for f in A0}, iter5={f: i5[f]["X_mean"] for f in A0}, pass_=bool(k1))
    P(f"  K1 (e_N 0 = iter_5): X-COP " + ", ".join(f"{f} {pr[f]['X_mean']:+.4f} vs {i5[f]['X_mean']:+.4f}" for f in A0) + f"; KiDS shift canonical {s['canonical']:+.4f} -> {'PASS' if k1 else 'FAIL'}")
    # K2: limits of the EFE form
    STATE["gNe"] = EN_PRIMARY * 1.2e-10; a0 = A0["canonical"]; ge = STATE["gNe"]
    lo = 1e-6 * ge; d = 1e-6 * ge
    slope = (GLAW0(ge + d, a0) - GLAW0(ge - d, a0)) / (2 * d)
    r_lo = glaw_efe(lo, a0) / (slope * lo); STATE["gNe"] = 1e-30; r_hi = glaw_efe(1e-9, a0) / GLAW0(1e-9, a0)
    k2 = abs(r_lo - 1) <= 1e-3 and abs(r_hi - 1) <= 1e-3; RES["K2"] = dict(low=r_lo, zero=r_hi, pass_=bool(k2))
    P(f"  K2 (EFE limits): g_N << g_Ne ratio {r_lo:.6f}; g_Ne -> 0 ratio {r_hi:.6f} -> {'PASS' if k2 else 'FAIL'}")
    set_en(EN_PRIMARY); s1 = shift(2.154); set_en(100 * EN_PRIMARY); s100 = shift(2.154)
    mA = all(abs(s100[f] - s1[f]) > 0.05 for f in A0); RES["MUTATE_A"] = dict(primary=s1, x100=s100, bites=bool(mA))
    P(f"  MUTATE A (e_N x100): KiDS shift canonical {s1['canonical']:+.3f} -> {s100['canonical']:+.3f}, alt {s1['alt']:+.3f} -> {s100['alt']:+.3f} -> {'BITES' if mA else 'NO BITE'}")
    set_en(EN_PRIMARY); g = gal_gates(1e-3, HOST, NS["BASE"]); mB = not (g[0] and g[1]); RES["MUTATE_B"] = dict(gates=list(g), bites=bool(mB))
    P(f"  MUTATE B (lambda_0 1e-3): {g} -> {'BITES' if mB else 'NO BITE'}")
    zero = lambda key, fM, Mt, lam0, a0: NS["dust"](key, fM, Mt, lam0, a0, fcap=0.0)[0]
    z0 = {f: lens_mean(a0, 2.154, zero) - NS["BASE"][f]["L"] for f, a0 in A0.items()}; mC = all(abs(v) < 1e-12 for v in z0.values())
    RES["MUTATE_C"] = dict(shift=z0, pass_=bool(mC)); P(f"  MUTATE C (f_cap 0): shift {z0} -> {'PASS' if mC else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
