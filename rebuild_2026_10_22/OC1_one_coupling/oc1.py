#!/usr/bin/env python3
"""OC1 (FROZEN_CRITERIA.md): one coupling of baryonic dissipation against core energy needs. Energy bookkeeping only. python3 oc1.py [--mutate]
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import contextlib, io, json, math, os, sys
import numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); MUT = "--mutate" in sys.argv; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
CD = os.path.join(REB, "CL4_cluster_energy_budget"); T = open(os.path.join(CD, "cl4_budget.py")).read(); T = T[:T.index('P("CL4 cluster energy budget')].replace('HERE = os.path.dirname(os.path.abspath(__file__))', f'HERE = {HERE!r}', 1).replace('MUT = "--mutate" in sys.argv', 'MUT = False', 1)
NS = {"__file__": os.path.join(CD, "cl4_budget.py"), "__name__": "cl4_ro"}; A0 = sys.argv; sys.argv = ["x"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(T, "cl4", "exec"), NS)
sys.argv = A0; os.chdir(HERE); ereq, srcs = NS["ereq"], NS["srcs"]; W_of, solve_r0, sigma_coll, SIG, MSUNE, GE, ERG = (NS[k] for k in ("W_of", "solve_r0", "sigma_coll", "SIG", "MSUNE", "GE", "ERG")); PC2 = NS["D"]["PC2"]; rc = NS["rc"]; tag = NS["tag"]
A4 = {1e13: 23.54, 1e14: 22.10}
def ereq_a4(M, foot, et):
    R = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); sc = sigma_coll(tag, M)[0] * MSUNE / PC2; s0, s1 = max(SIG[foot], A4[M] * sc), max(SIG[foot], et * sc); return (W_of(s1, solve_r0(M * MSUNE, R, s1), R) - W_of(s0, solve_r0(M * MSUNE, R, s0), R)) / 2, R
BE = json.load(open(os.path.join(REB, "BE1_baryon_energy_budget", "be1_results.json")))["runs"]; CN = json.load(open(os.path.join(REB, "CN1_contraction_on_cold_share", "cn1_energy.json")))
Rk = (lambda f: CN[f]["rows"]) if "rows" in CN.get("canonical", {}) else None
BHSN = (0.1 * 0.005 * 1.98847e30 * 2.998e8 ** 2 / 1e-7) / (1e51 / 100); P(f"E_BH/E_SN per M*, CL4's inputs: {BHSN:.1f}"); 
if MUT: BHSN = 0.0
ok = True; w = max(ereq(M, "canonical", 14.3)[0] / srcs(M, fs, ereq(M, "canonical", 14.3)[2])[k] for M in (1e13, 1e14) for fs in (.034, .0615) for k in ("AGN",)); e = abs(w / 0.0751 - 1) <= 1e-2; ws = max(ereq(M, "canonical", 14.3)[0] / srcs(M, fs, ereq(M, "canonical", 14.3)[2])["SN"] for M in (1e13, 1e14) for fs in (.034, .0615)); e2 = abs(ws / 6.71 - 1) <= 1e-2; ok &= e and e2; P(f"K1 CL4 worst eps_AGN {w:.4f}, eps_SN {ws:.3f} (table 3 digits): {'PASS' if e and e2 else 'FAIL'}")
ok2 = abs(BE["canonical_eta21.2"]["median"] - 0.0171) < 1e-3; ok &= ok2; P(f"K2 BE1 median {BE['canonical_eta21.2']['median']:.4f}: {'PASS' if ok2 else 'FAIL'}; CN1 keys {list(CN)[:3]}")
sy = np.full(20, 0.05); ok3 = np.std(np.log10(sy)) <= .3 and abs(np.median(sy) - .05) < 1e-12; ok &= ok3; P(f"K3 constant eps: {'PASS' if ok3 else 'FAIL'}")
if not ok: P("K FAILED: no verdict"); open(os.path.join(HERE, "oc1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1)
RES = {}
for foot in ("canonical", "alt"):
    rows = BE[f"{foot}_eta21.2"]["rows"]; b = {r["name"]: r for r in rows if r.get("active")}; zero = sum(1 for r in rows if not r.get("active") or r.get("Ereq_erg", 0) <= 0); c = {r["name"]: r for r in CN[foot]["rows"]}; shared = sorted(set(b) & set(c)); P(f"[{foot}] SPARC rows {len(rows)}; BE1 active {len(b)}, CN1 {len(c)}, shared {len(shared)}, zero need {zero}")
    JOB = {"soften": ({n: b[n]["Ereq_erg"] for n in b}, {n: b[n]["Esn_erg"] for n in b}, {n: b[n]["lM200"] for n in b}), "undo": ({n: c[n]["Ereq_erg"] for n in c}, {n: c[n]["Esn_erg"] for n in c}, {n: c[n]["lM200"] for n in c}), "both": ({n: b[n]["Ereq_erg"] + c[n]["Ereq_erg"] for n in shared}, {n: b[n]["Esn_erg"] for n in shared}, {n: b[n]["lM200"] for n in shared})}
    CLU = {}
    for et in (14.3, 10.82):
        for M in (1e13, 1e14):
            E, R = ereq_a4(M, foot, et); E0 = ereq(M, foot, et)[0]
            for fs in (.034, .0615):
                s = srcs(M, fs, R); CLU[(et, M, fs)] = dict(E=E, E0=E0, SN=s["SN"], AGN=s["AGN"])
    P("  cluster need A4 eta: " + "; ".join(f"t {et} M {M:g}: {CLU[(et, M, .034)]['E'] / ERG:.2e} erg (CL4 eta {CLU[(et, M, .034)]['E0'] / ERG:.2e})" for et in (14.3, 10.82) for M in (1e13, 1e14)))
    for rd, gdiv, cdiv in (("1 one coupling", lambda s: s * (1 + BHSN), lambda q: q["SN"] * (1 + BHSN)), ("2 two sources", lambda s: s, lambda q: q["AGN"])):
        vc = {k: q["E"] / cdiv(q) for k, q in CLU.items()}; v14 = [v for k, v in vc.items() if k[0] == 14.3]; cmin, cmax = min(vc.values()), max(vc.values()); cg = float(np.exp(np.mean(np.log(v14))))
        for job, (Eq, Es, LM) in JOB.items():
            n = [k for k in Eq if Eq[k] > 0]; e = np.array([Eq[k] / gdiv(Es[k]) for k in n]); lm = np.array([LM[k] for k in n]); rms = float(np.std(np.log10(e))); rho = float(spearmanr(e, lm)[0]); p = np.percentile(e, [16, 50, 84]); g1 = rms <= .30 and abs(rho) <= .30; g2 = p[0] <= cmax and cmin <= p[2]; g3 = max(p[1] / cg, cg / p[1]) <= 2
            RES[f"{foot}|{rd}|{job}"] = dict(n=len(n), p16=p[0], med=p[1], p84=p[2], rms=rms, rho=rho, cmin=cmin, cmax=cmax, cgm=cg, CONST=bool(g1), OVERLAP=bool(g2), RATIO=bool(g3)); P(f"  R{rd} {job}: n {len(n)}, eps {p[1]:.4g} [{p[0]:.4g}, {p[2]:.4g}], rms {rms:.2f} dex, rho {rho:+.2f}; clusters [{cmin:.4g}, {cmax:.4g}], gm {cg:.4g}, ratio {max(p[1] / cg, cg / p[1]):.1f}: CONST {g1} OVERLAP {g2} RATIO {g3}")
            if job == "both":
                bins = np.digitize(lm, [11, 11.5, 12]); P("    by lM200 <11, 11-11.5, 11.5-12, >12: " + ", ".join(f"{np.median(e[bins == i]):.3g} (n {(bins == i).sum()})" if (bins == i).any() else "-" for i in range(4)))
                wg = (p[0] / 1.8, p[2] / 0.6); wc = (cmin / (10 ** .3 if rd.startswith("2") else 1.8), cmax / (10 ** -.3 if rd.startswith("2") else .6)); P(f"    with bands, reported only: gal [{wg[0]:.4g}, {wg[1]:.4g}], cl [{wc[0]:.4g}, {wc[1]:.4g}], overlap {wg[0] <= wc[1] and wc[0] <= wg[1]}")
    g = lambda r, k: RES[f"{foot}|{r}|both"][k]; R1, R2 = "1 one coupling", "2 two sources"; a = all(g(R1, k) for k in ("CONST", "OVERLAP", "RATIO")); bb = all(g(R2, k) for k in ("CONST", "OVERLAP", "RATIO")); o1, o2 = g(R1, "OVERLAP"), g(R2, "OVERLAP"); C = "ONE COUPLING" if a else "ONE COUPLING [TWO SOURCES]" if bb else f"INTERVALS OVERLAP ONLY (reading {'1' if o1 else ''}{'2' if o2 else ''})" if o1 or o2 else "NO ONE COUPLING"; RES[f"{foot}|class"] = C; P(f"  VERDICT [{foot}]: {C}")
P("dwarfs, sign only: S_min 46-64 (SN1) against native S 44.2 at 1e10, 79.1 at 1e11 (X80): heating lowers S, so not needed at 1e11 and the wrong sign at 1e10")
TAGF = "oc1_MUTATE" if MUT else "oc1"; json.dump(RES, open(os.path.join(HERE, TAGF + "_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, TAGF + ".out"), "w").write("\n".join(OUT) + "\n")
