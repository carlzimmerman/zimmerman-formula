#!/usr/bin/env python3
"""BE1_baryon_energy_budget (criteria 6304ce4bb0): per SPARC galaxy, virial energy to soften the converged-cusp core
(CE1 eta) to the SPARC limit, vs the galaxy's supernova energy. X74 executed read-only (X76's loader), c_f table = CE1 median.
    python3 be1_energy.py [--mutate]"""
import json, math, os, sys
import numpy as np
from scipy.integrate import quad
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
MUT = "--mutate" in sys.argv
CE1T = os.path.join(REB, "CE1_converged_eta_grade", "CE1_med_fs0.034_cf_table.json")
X74F = os.path.join(REB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read()
END = '{"__file__": os.path.join(HERE, "x74_native_cf.py"), "__name__": "__main__"}'
assert TX.count(END) == 1; TX = TX.replace(END, "BE1NS")
os.environ.update(X74_CF=CE1T, X74_CFMULT="1", X73_FSTAR="0.034", X73_SLOPE="2.7774425603108597", PYTHONHASHSEED="0")
NS = {"__file__": os.path.join(HERE, "be1_base.py"), "__name__": "__main__"}
D = {"__file__": X74F, "__name__": "x74_ro", "BE1NS": NS}; argv0 = sys.argv
try: exec(compile(TX, X74F, "exec"), D)
except SystemExit: pass
sys.argv = argv0
GALS, B, solve_r0, sigma_coll, eta_of, SIG, BGS = (NS[k] for k in ("GALS", "B", "solve_r0", "sigma_coll", "eta_of", "SIG", "BGS"))
GE, MSUNE, MPCE, PC2 = NS["GE"], NS["MSUNE"], NS["MPCE"], NS["PC2"]; cf_of = NS["cf_of"]
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
ERG = 1e-7   # J per erg (GE is SI)
P("BE1 baryon energy budget (criteria 6304ce4bb0); kappa = 1/2 FITTED; footings never pooled; not theory closed" + ("  [MUTATE E_SN x 0.01]" if MUT else ""))
P(f"  cf table (CE1 median): {json.load(open(CE1T))['cf_by_mass']}")

def W_of(s, r0, R):
    """W = -G int_0^R M dM / r for the smooth core M(r) = pi s r0^2 B(r/r0)."""
    x = np.concatenate([[0.0], np.geomspace(1e-6 * R, R, 40001)])
    M = math.pi * s * r0 ** 2 * B(x / r0); dM = np.diff(M); rm = 0.5 * (x[1:] + x[:-1]); Mm = 0.5 * (M[1:] + M[:-1])
    return -GE * float(np.sum(Mm * dM / rm))
def W_phi(s, r0, R):
    """independent: W = (1/2) int rho Phi dV, Phi(r) = -G M(r)/r - G int_r^R dM'/r' (truncated at R)."""
    Mr = lambda r: math.pi * s * r0 ** 2 * float(B(r / r0)); rho = lambda r: s / r0 / (1 + (r / r0) ** 2) ** 1.5
    ext = lambda r: quad(lambda u: rho(u) * 4 * math.pi * u, r, R, epsrel=1e-11, limit=200)[0]
    return 0.5 * quad(lambda r: rho(r) * 4 * math.pi * r * r * (-GE * Mr(r) / r - GE * ext(r)), 0, R, epsrel=1e-9, limit=200)[0]
s_t, r0_t, R_t = SIG["canonical"], 3.0e19, 6.0e21
w1, w2 = W_of(s_t, r0_t, R_t), W_phi(s_t, r0_t, R_t); K1 = abs(w1 / w2 - 1) < 1e-6
P(f"K1 W (M dM / r) vs W (1/2 rho Phi): {w1:.9e} vs {w2:.9e}, rel {abs(w1 / w2 - 1):.1e}: {'PASS' if K1 else 'FAIL'}")

def run(foot, tag="A_c2b_refit", eta_t=21.2, k2=False):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); rows = []
    for q in GALS:
        lM = bg["a"] + bg["b"] * (q["lMb"] - 10); M200 = 10 ** lM; R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)
        scoll = sigma_coll(tag, M200)[0] * MSUNE / PC2; ec = eta_of(cf_of(M200))
        s_c = max(SIG[foot], ec * scoll); s_g = max(SIG[foot], (ec if k2 else eta_t) * scoll)
        if s_c <= SIG[foot]: rows.append(dict(name=q.get("name"), lM200=lM, active=False, eps=0.0)); continue
        Wc = W_of(s_c, solve_r0(M200 * MSUNE, R200, s_c), R200); Wg = W_of(s_g, solve_r0(M200 * MSUNE, R200, s_g), R200)
        Ereq = max(0.0, (Wg - Wc) / 2) if not k2 else (Wg - Wc) / 2
        Esn = (0.5 * q["L36"] / 100.0) * 1e51 * ERG * (0.01 if MUT else 1.0)
        rows.append(dict(name=q.get("name"), lM200=lM, active=True, Ereq_erg=Ereq / ERG, Esn_erg=Esn / ERG, eps=Ereq / Esn, ec=ec))
    return rows
K2rows = run("canonical", k2=True); K2 = all(r["eps"] == 0 for r in K2rows if r["active"])
P(f"K2 eta_t = eta_conv gives E_req = 0 for every active galaxy: {'PASS' if K2 else 'FAIL'}")
RES = dict(K1=K1, K2=K2, runs={})
for foot in ("canonical", "alt"):
    for eta_t in (21.2, 10.82):
        rows = run(foot, eta_t=eta_t); act = [r for r in rows if r["active"]]; e = np.array([r["eps"] for r in act]); lm = np.array([r["lM200"] for r in act])
        med = float(np.median(e)) if len(e) else float("nan")
        cls = "SN ENERGETICALLY EXCLUDED" if med > 1 else "SN ENERGY AMPLE" if med <= 0.01 else "SN ENERGY SUFFICIENT IF COUPLED"
        from scipy.stats import spearmanr
        rho = float(spearmanr(lm, e).correlation) if len(e) > 2 else float("nan")
        RES["runs"][f"{foot}_eta{eta_t}"] = dict(n_active=len(act), n=len(rows), median=med, p16=float(np.percentile(e, 16)), p84=float(np.percentile(e, 84)),
                                                 frac_over1=float(np.mean(e > 1)), spearman_M=rho, cls=cls, rows=rows)
        P(f"  [{foot}] target eta {eta_t}{' (PRIMARY)' if eta_t == 21.2 else ' (reported)'}: active {len(act)}/{len(rows)}; eps_req median {med:.4f} "
          f"[16-84% {np.percentile(e, 16):.4f}, {np.percentile(e, 84):.4f}], max {e.max():.3f}; eps > 1 in {np.mean(e > 1):.0%}; Spearman(M200) {rho:+.2f}: {cls}")
if MUT:
    base = json.load(open(os.path.join(HERE, "be1_results.json")))["runs"]["canonical_eta21.2"]["median"]
    r = RES["runs"]["canonical_eta21.2"]["median"] / base; P(f"MUTATE E_SN x 0.01: median eps x {r:.6f} (must be 100): {'PASS' if abs(r / 100 - 1) < 1e-9 else 'FAIL'}")
P("necessary condition only: no mechanism, no fitted efficiency; SN numbers PROVISIONAL (1 per 100 Msun, 1e51 erg)")
tag = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"be1_results{tag}.json"), "w"), indent=1); open(os.path.join(HERE, f"be1{tag}.out"), "w").write("\n".join(OUT) + "\n")
