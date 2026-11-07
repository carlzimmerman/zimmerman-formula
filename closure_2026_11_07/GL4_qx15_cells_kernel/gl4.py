#!/usr/bin/env python3
"""GL4 (FROZEN_CRITERIA.md 626564bed8): QX15's cells C1-C4 and P1 re-read with the Limber k^-4 restored.
Builds QX15 do_cells' source exactly (same string patches) plus weight x (chi/(L+1/2))^n; n 0 record, n 4 corrected,
n 2 MUTATE. Grades with QX15's own objective (read-only import). Usage: gl4.py [MUTATE]. One thread.
kappa = 1/2 FITTED; not theory closed. Footings never pooled. Adopts nothing."""
import os, sys, json, time, importlib.util, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
Q15D = os.path.join(REPO, "closure_2026_11_06", "QX15_cmb_primary_likelihood")
sys.path.insert(0, Q15D)
import qx15 as Q                                          # read-only; its __main__ block does not run
NOTE = "kappa = 1/2 FITTED; not theory closed"
MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def J(n): return json.load(open(os.path.join(Q15D, "parts", n)))
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9   # bytes on macOS
CELLS = ("C1", "C2", "C3", "C4"); FEET = ("canonical", "alt")
KEYS = ["omega_b", "omega_d", "lnAs1e10", "n_s", "tau"]


def build_cells(npows):
    """QX15 do_cells, verbatim patches, plus the exponent patch. Returns {n: {cell: (S_clamped, Lcov, S_raw)}}."""
    spec = importlib.util.spec_from_file_location("qx10_i1", os.path.join(REPO, "closure_2026_11_06/QX10_window_hardening/iter_1_primary_cmb/qx10_i1.py"))
    M10 = importlib.util.module_from_spec(spec); spec.loader.exec_module(M10)
    import inspect
    src = inspect.getsource(M10.jcheck)
    assert "Ls = np.arange(2, 2501)" in src and "S = Sfull(Rr)" in src
    src = src.replace("Ls = np.arange(2, 2501)", "Ls = np.arange(2, 7001)")
    old = "S = np.ones(len(Ls)); ok = den > 0; S[ok] = num[ok] / den[ok]; return S"
    assert old in src
    src = src.replace(old, "S = np.ones(len(Ls)); ok = den > 0; S[ok] = num[ok] / den[ok]; COV['last'] = full; return S")
    src = src.replace("        num = np.zeros(len(Ls)); den = np.zeros(len(Ls))",
                      "        num = np.zeros(len(Ls)); den = np.zeros(len(Ls)); full = np.ones(len(Ls), bool)")
    src = src.replace("kk = (Ls + 0.5) / chi[j]; m = (kk >= kgrid[0]) & (kk <= kgrid[-1])",
                      "kk = (Ls + 0.5) / chi[j]; m = (kk >= kgrid[0]) & (kk <= kgrid[-1]); full &= m | (w[j] == 0)")
    src = src.replace("Rr = solve_gen(kJ) / N3[\"ref\"]; S = Sfull(Rr)", "Rr = solve_gen(kJ) / N3[\"ref\"]; S = Sfull(Rr); SOUT[cname] = (S.copy(), COV['last'].copy())")
    src = src.replace('json.dump(res, open(os.path.join(HERE, "jcheck.json"), "w"), indent=1)', "return res")
    # GL4's one extra patch: the lensing-potential k^-4 with exponent NPOW (0 = record)
    old_w = "num[m] += w[j] * Pj * Rj ** 2 / chi[j] ** 2; den[m] += w[j] * Pj / chi[j] ** 2"
    assert src.count(old_w) == 1
    src = src.replace(old_w, "ex = (chi[j] / (Ls[m] + 0.5)) ** NPOW; num[m] += w[j] * Pj * Rj ** 2 / chi[j] ** 2 * ex; den[m] += w[j] * Pj / chi[j] ** 2 * ex")
    Ls = np.arange(2, 7001); allS = {}
    for n in npows:
        ns = M10.__dict__; SOUT = {}; COV = {}; ns["SOUT"] = SOUT; ns["COV"] = COV; ns["NPOW"] = n
        exec(compile(src, "qx10_jcheck_extended_gl4", "exec"), ns)
        ns["jcheck"]()
        allS[n] = {}
        for c, (S, full) in SOUT.items():
            Lcov = int(Ls[full].max()) if full.any() else 2
            S2 = S.copy(); S2[Ls > Lcov] = S[Ls == Lcov][0]
            allS[n][c] = (S2, Lcov, S)
        P(f"S built n={n}: " + "; ".join(f"{c} Lcov {v[1]} S_min {v[0].min():.6f} max|1-S| {np.abs(1 - v[0]).max():.3e}" for c, v in allS[n].items()) + f"  (RSS {rss():.2f} GB)")
    return Ls, allS


def chi2_at(foot, theta, S, x0nuis=None):
    """QX15's objective at one theta (fresh make_obj; nuisance profile started at x0nuis)."""
    f, st, cache = Q.make_obj(foot, "main", S=S)
    if x0nuis is not None: st["x0"] = x0nuis
    v = f(np.array(theta, float))
    return float(v), st


def nuis_of(rec):
    return {"Pcut": np.array(rec["grade"]["Pcut"]["nuis"]), "A": np.array(rec["grade"]["A"]["nuis"])}


def main():
    t0 = time.time()
    rec = json.load(open(os.path.join(Q15D, "qx15.json")))
    npows = (2,) if MUT else (0, 4)
    Ls, allS = build_cells(npows)
    res = dict(note=NOTE, criteria="626564bed8", mutate=MUT, S={}, footings={})
    for n in npows:
        res["S"][str(n)] = {c: dict(L_full_coverage=v[1], S_min=float(v[0].min()), S_max=float(v[0].max()),
                                    max_abs_1mS=float(np.abs(1 - v[0]).max()), S_L100=float(v[0][98]), S_L400=float(v[0][398]),
                                    S_L917=float(v[0][915]), max_abs_1mS_L2500=float(np.abs(1 - v[2][:2499]).max()))
                            for c, v in allS[n].items()}
    if not MUT:
        Z = np.load(os.path.join(Q15D, "parts", "cellS.npz")); meta = J("cellS_meta.json")
        ka0 = {c: dict(max_abs_d=float(np.abs(allS[0][c][0] - Z[c]).max()), Lcov=allS[0][c][1], Lcov_rec=meta[c]["L_full_coverage"]) for c in CELLS}
        ka0_ok = all(v["max_abs_d"] <= 1e-12 and v["Lcov"] == v["Lcov_rec"] for v in ka0.values())
        res["KA0"] = dict(cells=ka0, pass_=ka0_ok)
        P(f"KA0 (n=0 vs cellS.npz): " + "; ".join(f"{c} max|d| {v['max_abs_d']:.1e} Lcov {v['Lcov']}/{v['Lcov_rec']}" for c, v in ka0.items()) + f" -> {'PASS' if ka0_ok else 'FAIL'}")
        ka2 = {c: res["S"]["4"][c]["max_abs_1mS_L2500"] for c in CELLS}
        res["KA2"] = dict(n4_max_abs_1mS_L2500=ka2, pass_=all(v <= 1e-3 for v in ka2.values()))
        P(f"KA2 (n=4 max|1-S| at L<=2500, GL1 L9 <= 1.8e-5): {ka2} -> {'PASS' if res['KA2']['pass_'] else 'FAIL'}")
    Lgrid = Ls
    for foot in FEET:
        F = {}; R = rec["footings"][foot]
        base = J(f"fit_{foot}_main.json"); th0 = [base["theta"][k] for k in KEYS]; chi_main = base["chi2_PA"]
        x0m = nuis_of(base)
        if not MUT:
            v, _ = chi2_at(foot, th0, None, x0m)
            F["KA1_main"] = dict(chi2=v, rec=chi_main, d=v - chi_main)
            P(f"{foot} KA1 main: chi2 {v:.6f} vs {chi_main:.6f} (d {v - chi_main:+.2e})  [{time.time() - t0:.0f} s, RSS {rss():.2f} GB]")
            F["KA1_cells"] = {}
            for c in CELLS + ("P1",):
                r = J(f"cell_{foot}_{c}.json"); th = [r["theta"][k] for k in KEYS]
                S = (Lgrid, np.full(len(Lgrid), 0.5)) if c == "P1" else (Lgrid, allS[0][c][0])
                v, _ = chi2_at(foot, th, S, nuis_of(r))
                F["KA1_cells"][c] = dict(chi2=v, rec=r["chi2_PA"], d=v - r["chi2_PA"], delta_rec=r["delta_cell"], delta_repro=v - chi_main)
                P(f"{foot} KA1 {c}: chi2 {v:.6f} vs {r['chi2_PA']:.6f} (d {v - r['chi2_PA']:+.2e}); Delta_cell {v - chi_main:+.4f} vs record {r['delta_cell']:+.4f}  [{time.time() - t0:.0f} s]")
        n = 2 if MUT else 4
        F["cells"] = {}
        for c in CELLS:
            S = (Lgrid, allS[n][c][0])
            d0, _ = chi2_at(foot, th0, S, x0m); d0 -= chi_main
            row = dict(n=n, Delta_0=d0, refit=None)
            if not MUT and d0 > 4:
                f, st, cache = Q.make_obj(foot, "main", S=S)
                Q.nm(f, np.array(th0), np.array([1.5e-4, 0.004, 0.02, 0.008, 0.008]), 150)
                row["refit"] = dict(delta=st["best"][0] - chi_main, theta=dict(zip(KEYS, st["best"][1])), nfev=len(cache))
            dl = row["refit"]["delta"] if row["refit"] else d0
            row["Delta"] = dl; row["label"] = Q.Lc(dl) if R["P1"]["bites"] else "NO VERDICT (P1 no power)"
            old = R["cells"][c]; row["record"] = dict(delta=old["delta_cell"], label=old["label"])
            row["verdict"] = None if MUT else ("HOLDS" if row["label"] == old["label"] else "MOVES")
            F["cells"][c] = row
            P(f"{foot} {c} n={n}: Delta_0 {d0:+.4f}" + (f", refit {row['refit']['delta']:+.4f}" if row["refit"] else "") +
              f" -> {row['label']}; record {old['delta_cell']:+.2f} {old['label']}" + ("" if MUT else f" => {row['verdict']}") + f"  [{time.time() - t0:.0f} s]")
        if not MUT:
            F["P1"] = dict(record=R["P1"], reading="kernel-free (flat S = 0.5); HOLDS by construction", verdict="HOLDS")
        res["footings"][foot] = F
    if MUT:
        g = json.load(open(os.path.join(HERE, "gl4.json")))
        diffS = {c: dict(vs_n0=float(np.abs(allS[2][c][0] - np.load(os.path.join(Q15D, "parts", "cellS.npz"))[c]).max())) for c in CELLS}
        bites_any = False
        for foot in FEET:
            for c in CELLS:
                d4 = g["footings"][foot]["cells"][c]["Delta_0"]; d2 = res["footings"][foot]["cells"][c]["Delta_0"]
                res["footings"][foot]["cells"][c]["Delta_0_n4"] = d4
                if abs(d2 - d4) > 0.01: bites_any = True
        for c in CELLS:
            s4min = g["S"]["4"][c]["S_min"]; diffS[c]["Smin_n2"] = res["S"]["2"][c]["S_min"]; diffS[c]["Smin_n4"] = s4min
        res["M1"] = dict(S_diff=diffS, S_differs=all(v["vs_n0"] > 1e-3 for v in diffS.values()) and all(abs(v["Smin_n2"] - v["Smin_n4"]) > 1e-3 for v in diffS.values()),
                         Delta_differs_from_n4=bites_any)
        res["M1"]["bites"] = res["M1"]["S_differs"] and bites_any
        P(f"M1 (n=2): S differs from n0 and n4: {res['M1']['S_differs']}; Delta_0 differs from n4: {bites_any} -> {'BITES' if res['M1']['bites'] else 'DOES NOT BITE'}")
    res["peak_RSS_GB"] = rss(); res["runtime_s"] = time.time() - t0
    P(f"peak RSS {rss():.2f} GB; {time.time() - t0:.0f} s. {NOTE}")
    tag = "gl4_MUTATE" if MUT else "gl4"
    json.dump(res, open(os.path.join(HERE, tag + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
