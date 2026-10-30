#!/usr/bin/env python3
"""CM3_cadence_coupling_map: CM2's dynamics on a declared N x eps_c map plus seed/mass robustness.
    python3 cm3_map.py setup; python3 cm3_map.py run NAME; python3 cm3_map.py grade"""
import json, os, re, sys, textwrap
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); CM1 = os.path.join(REB, "CM1_outflow_coupling"); sys.path[:0] = [CM1, os.path.join(REB, "CM2_gas_rich_past")]
import cm1_outflow as C, cm2_gas_rich as C2
MAP = dict(N10e03=(10, 1000.0, 0.3), N10e01=(10, 1000.0, 0.1), N20e1=(20, 500.0, 1.0), N20e03=(20, 500.0, 0.3))
ROB = dict(SEED2=(10, 1000.0, 1.0), LO=(10, 1000.0, 1.0), HI=(10, 1000.0, 1.0))
STA = {f"STATIC_{k}": (10, 1000.0, 0.0) for k in ROB}
def vdir(v):
    d = os.path.join(HERE, f"ics_{v}"); os.makedirs(d, exist_ok=True); return d
def make_ics(v, S, seed):
    src = open(os.path.join(CM1, "cm1_outflow.py")).read(); body = src.split("    # cold density")[1].split("    xc = float(np.sort(r)[499])")[0]
    ns = dict(vars(C)); ns.update(S=S, c=S["c"], HERE=vdir(v), SEED=seed); exec(textwrap.dedent("    # cold density" + body), ns)
    r = np.linalg.norm(ns["pos"], axis=1); S["xc500"] = float(np.sort(r)[499]); json.dump(S, open(os.path.join(vdir(v), "cm1_setup.json"), "w"), indent=1)
def run(name):
    v = "BASE" if name in MAP else name.replace("STATIC_", ""); d = CM1 if v == "BASE" else vdir(v)
    S = json.load(open(os.path.join(d, "cm1_setup.json"))); C2.S, C2.CM1, C2.HERE = S, d, HERE
    C2.Mb, C2.Mg0, C2.a, C2.xc = S["Mb"], S["Mg"], S["a_star"], S["xc500"]; C2.Mstar = S["Mb"] - S["Mg"]
    C2.ESN = C2.ESN * C2.Mstar / (json.load(open(os.path.join(CM1, "cm1_setup.json")))["Mb"] - json.load(open(os.path.join(CM1, "cm1_setup.json")))["Mg"])
    C2.CFG = {**MAP, **ROB, **STA}; C2.run(name); os.replace(os.path.join(HERE, f"cm2_run_{name}.json"), os.path.join(HERE, f"cm3_run_{name}.json"))
def grade():
    L = lambda m: json.load(open(os.path.join(HERE, f"cm3_run_{m}.json"))); CM = os.path.join(REB, "CM2_gas_rich_past"); out = []
    def P(s): print(s, flush=True); out.append(s)
    P("CM3 cadence x coupling map (see FROZEN_CRITERIA.md); kappa = 1/2 FITTED; not theory closed; cold dark energy is a gravitating field, never a particle")
    es = json.load(open(os.path.join(CM1, "cm1_run_STATIC.json")))["marks"][-1]["eta"]; c2 = json.load(open(os.path.join(CM, "cm2_results.json")))
    k1 = all(np.array_equal(np.load(os.path.join(CM1, "cm1_ics.npz"))[k], np.load(os.path.join(vdir("K1"), "cm1_ics.npz"))[k]) for k in ("pos", "vel")); P(f"K1 regenerated seed 1 ICs identical: {'PASS' if k1 else 'FAIL'}")
    Rm = {}; k2 = k3 = done = True
    for m, (N, per, e) in {**MAP, **ROB}.items():
        q = L(m); ref = es if m in MAP else L(f"STATIC_{m}")["marks"][-1]["eta"]; Rm[m] = q["marks"][-1]["eta"] / ref; f = [s[0] for s in q["schedule"]]; eu = sum(q["lift_erg"]) / q["E_SN"]
        k2 &= q["maxerr"] < 0.01; k3 &= eu <= e * (1 + 1e-9); done &= q["done"]
        P(f"  {m}: N {N} eps_c {e}: R {Rm[m]:.3f} ({'reaches' if Rm[m] <= C.NEED else 'misses'}); moved mass first/last {f[0]:.4f}/{f[-1]:.4f}; eps_used {eu:.3f}; err {q['maxerr']:.1e}")
    P(f"K2 work balance: {'PASS' if k2 else 'FAIL'}; K3 energy cap: {'PASS' if k3 else 'FAIL'}; all runs done: {done}")
    a, b_, c_ = c2["R"]["C10"][-1], Rm["N10e03"], Rm["N10e01"]; mu = b_ >= a - 0.03 and c_ >= b_ - 0.03; P(f"MUTATE monotonic, N 10: eps 1 {a:.3f}, 0.3 {b_:.3f}, 0.1 {c_:.3f}: {'PASS' if mu else 'FAIL'}")
    ok = k1 and k2 and k3 and done; rob = "NOT DECIDED" if not ok else "ROBUST" if all(Rm[k] <= C.NEED for k in ROB) else "FRAGILE"
    P(f"VERDICT robustness (N 10, eps_c 1): SEED2 {Rm['SEED2']:.3f}, LO {Rm['LO']:.3f}, HI {Rm['HI']:.3f}: {rob}")
    open(os.path.join(HERE, "cm3.out"), "w").write("\n".join(out) + "\n"); json.dump(dict(R=Rm, robustness=rob, K1=k1, K2=k2, K3=k3, mutate=mu), open(os.path.join(HERE, "cm3_results.json"), "w"), indent=1)
if __name__ == "__main__":
    if sys.argv[1] == "setup":
        S0 = json.load(open(os.path.join(CM1, "cm1_setup.json"))); fb = json.load(open(os.path.join(HERE, "fb_percentiles.json")))
        make_ics("K1", dict(S0), 1); make_ics("SEED2", dict(S0), 2)
        for v in ("LO", "HI"):
            S = dict(S0); S["Mb"] = fb[v]; S["Mg"] = fb[v] * S0["Mg"] / S0["Mb"]; make_ics(v, S, 1)
    elif sys.argv[1] == "run": run(sys.argv[2])
    else: grade()
