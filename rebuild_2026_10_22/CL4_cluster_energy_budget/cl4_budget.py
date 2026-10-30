#!/usr/bin/env python3
"""CL4_cluster_energy_budget: BE1's E_req at cluster masses vs SN, AGN, infall budgets (BE1 loader, X74 read-only).
    python3 cl4_budget.py [--mutate]"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); MUT = "--mutate" in sys.argv
B1 = os.path.join(REB, "BE1_baryon_energy_budget", "be1_energy.py"); T1 = open(B1).read()
T1 = T1.replace('HERE = os.path.dirname(os.path.abspath(__file__))', f'HERE = {HERE!r}', 1).replace('MUT = "--mutate" in sys.argv', 'MUT = False', 1)
cut = "K2rows = run("; assert T1.count(cut) == 1
D = {"__file__": B1, "__name__": "be1_ro"}; argv0 = sys.argv; sys.argv = [B1]; exec(compile(T1.split(cut)[0], B1, "exec"), D); sys.argv = argv0
W_of, solve_r0, sigma_coll, eta_of, cf_of, SIG, BGS, GE, MSUNE, MPCE = (D[k] for k in ("W_of", "solve_r0", "sigma_coll", "eta_of", "cf_of", "SIG", "BGS", "GE", "MSUNE", "MPCE"))
ERG, C_ = 1e-7, 2.998e8; FG = 0.10 * (0.01 if MUT else 1.0); tag = "A_c2b_refit"; bg = BGS[tag]
rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def ereq(M, foot, eta_t):
    R = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); sc = sigma_coll(tag, M)[0] * MSUNE / D["PC2"]; ec = eta_of(cf_of(M))
    s0, s1 = max(SIG[foot], ec * sc), max(SIG[foot], eta_t * sc)
    return (W_of(s1, solve_r0(M * MSUNE, R, s1), R) - W_of(s0, solve_r0(M * MSUNE, R, s0), R)) / 2, ec, R
def srcs(M, fs, R):
    Ms = fs * FG * M; V2 = GE * M * MSUNE / R
    return dict(SN=Ms / 100 * 1e51 * ERG, AGN=0.1 * 0.005 * Ms * MSUNE * C_ ** 2, INFALL=Ms * MSUNE * V2)
P("CL4 cluster energy budget (see FROZEN_CRITERIA.md); inputs 0.10, 0.005, 0.1, 1/100 PROVISIONAL; kappa = 1/2 FITTED; not theory closed" + ("  [MUTATE M_gas x 0.01]" if MUT else ""))
k1 = all(abs(ereq(M, "canonical", eta_of(cf_of(M)))[0]) == 0 for M in (1e13, 1e14)); P(f"K1 eta_t = eta_conv gives E_req 0: {'PASS' if k1 else 'FAIL'}")
Rw = {}
for foot in ("canonical", "alt"):
    for eta_t in (14.3, 10.82):
        for M in (1e13, 1e14):
            E, ec, R = ereq(M, foot, eta_t)
            for fs in (0.034, 0.0615):
                e = {k: E / v for k, v in srcs(M, fs, R).items()}; Rw[f"{foot}|{eta_t}|{M:g}|{fs}"] = dict(E_req_erg=E / ERG, eta_conv=ec, eps=e)
                P(f"  [{foot}] target {eta_t} M {M:g} f* {fs}: eta_conv {ec:.2f}, E_req {E / ERG:.2e} erg; eps SN {e['SN']:.2f}, AGN {e['AGN']:.4f}, INFALL {e['INFALL']:.3f}")
cls = {}
for k in ("SN", "AGN", "INFALL"):
    w = max(v["eps"][k] for q, v in Rw.items() if q.startswith("canonical|14.3|")); cls[k] = dict(worst=w, cls="EXCLUDED" if w > 1 else "AMPLE" if w <= 0.01 else "SUFFICIENT IF COUPLED"); P(f"CLASS {k} (worst canonical, target 14.3): eps {w:.3f}: {cls[k]['cls']}")
res = dict(K1=k1, rows=Rw, classes=cls); tagf = "_MUTATE" if MUT else ""
if MUT:
    b = json.load(open(os.path.join(HERE, "cl4_results.json")))["rows"]; ok = all(abs(Rw[q]["eps"][k] / b[q]["eps"][k] / 100 - 1) < 0.01 for q in Rw for k in Rw[q]["eps"] if b[q]["eps"][k] != 0); P(f"MUTATE eps x 100: {'PASS' if ok else 'FAIL'}"); res["mutate"] = ok
else:
    be = json.load(open(os.path.join(REB, "BE1_baryon_energy_budget", "be1_results.json")))["runs"]["canonical_eta21.2"]["median"]
    new = float(np.median([r["eps"] for r in D["run"]("canonical") if r["active"]])); k2 = new == be; P(f"K2 BE1 median {new:.6f} vs committed {be:.6f}: {'PASS' if k2 else 'FAIL'}"); res["K2"] = k2
json.dump(res, open(os.path.join(HERE, f"cl4_results{tagf}.json"), "w"), indent=1); open(os.path.join(HERE, f"cl4{tagf}.out"), "w").write("\n".join(OUT) + "\n")
