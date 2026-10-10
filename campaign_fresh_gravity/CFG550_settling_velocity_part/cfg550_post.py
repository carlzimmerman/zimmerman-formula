#!/usr/bin/env python3
"""CFG550 post-freeze diagnostics (dated 2026-10-10): no label depends on this script.
(1) the derived target T_ph(r) near the centre in each cell (the cluster phantom is ~0 inside r_M, so T_ph = P/rho_ph diverges);
(2) when the cluster a1/c runs' relaxation energy blows up (from cfg550_results.json series);
(3) the MW-only reading of every frozen item (the cluster cells excluded), so the MW verdict is shown not to hinge on the blow-up.
Run: nice -n 10 python3 cfg550_post.py
"""
import os, json, math, importlib.util
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("c550", os.path.join(HERE, "cfg550.py")); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
J = json.load(open(os.path.join(HERE, "cfg550_results.json")))
out, res = [], {}
def log(s): print(s); out.append(s)
for k in ("MW_can", "MW_alt", "cluster_can", "cluster_alt"):
    s, f = k.split("_"); c = M.T544.make_cell(s, f); pr = M.law_profiles(c)
    pts = [0.002, 0.01, 0.03, 0.05, 0.1, 0.2]
    T = {str(r): float(np.interp(r, pr["r"], pr["T"])) for r in pts}
    res[k] = dict(T_ph_at=T, r_M_over_rstar=c["Mb"], T_ph_max_inside_rta=float(pr["T"][(pr["r"] >= M.RMIN) & (pr["r"] <= c["rta"])].max()))
    log(f"{k}: r_M/r_* {c['Mb']:.4f}; T_ph/V_f^2 at r/r_* {T}; max inside r_ta {res[k]['T_ph_max_inside_rta']:.3e}")
for nm, o in J["runs"].items():
    if nm.startswith("cluster") and ("|a1_" in nm or "|c_" in nm):
        ser = o["series"]
        tb = next((x["t"] for x in ser if abs(x["relax_in"]) > 10), None)
        res.setdefault("blowup_t_Gyr", {})[nm] = tb
        log(f"{nm}: relaxation input first exceeds 10 V_f^2 M_cat at t = {tb} Gyr")
R = J["routes"]; mw = ("MW_can", "MW_alt")
for md in ("a1", "c"):
    r = R[md]
    d = dict(G550_B={k: r["G550_B"][k] for k in mw}, G550_C={k: r["G550_C"][k] for k in mw},
             D_B={k: J["runs"][f"{k}|{md}_B"]["final"]["D"] for k in mw}, logXJ_B={k: J["runs"][f"{k}|{md}_B"]["final"]["logXJ"] for k in mw},
             overfill_P={k: r["overfill_P"][k] for k in mw},
             edge={kk: v for kk, v in r["edge_dln_r99"].items() if kk.split("|")[0] in mw},
             energy={k: dict(B_net=r["energy"][k]["B_net"], C_whole=r["energy"][k]["C_whole_history"], B_relax_in_rate=r["energy"][k]["B_relax_in_rate_last2"]) for k in mw},
             F_rise_max={nm: v[0] for nm, v in r["lyapunov_numeric_rises"].items() if nm.split("|")[0] in mw})
    res[f"MW_only_{md}"] = d
    log(f"MW-only {md}: {d}")
json.dump(res, open(os.path.join(HERE, "cfg550_post.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg550_post.out"), "w").write("\n".join(out) + "\n")
