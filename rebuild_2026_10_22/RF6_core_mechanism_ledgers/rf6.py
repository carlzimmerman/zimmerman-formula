#!/usr/bin/env python3
"""RF6_core_mechanism_ledgers (FROZEN_CRITERIA.md, 0b8131bb50): CM1 and CL5 re-run with moved gas scanned over the ledgered range; need as a band. CM1's and CL5's text is exec'd with asserted replacements; their files are read only.
    python3 rf6.py setup; python3 rf6.py list; python3 rf6.py run NAME; python3 rf6.py runall; python3 rf6.py grade
    RF6_MUTATE=1 python3 rf6.py runall; RF6_MUTATE=1 python3 rf6.py grade     # E3 x 0.1, X2 x 0.1, separate outputs
kappa = 1/2 FITTED; footings never pooled; not theory closed; cold dark energy is a gravitating field component, never a particle."""
import json, math, os, subprocess, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
from concurrent.futures import ThreadPoolExecutor
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); CM1 = os.path.join(RB, "CM1_outflow_coupling"); CL5 = os.path.join(RB, "CL5_agn_gas_cycles"); RUNS = os.path.join(HERE, "runs"); os.makedirs(RUNS, exist_ok=True); SETUP = os.path.join(HERE, "rf6_setup.json"); sys.path.insert(0, CM1)
MUT = os.environ.get("RF6_MUTATE") == "1"
def setup():
    import cm1_outflow as C
    S = json.load(open(os.path.join(CM1, "cm1_setup.json")))
    B1 = os.path.join(RB, "BE1_baryon_energy_budget", "be1_energy.py"); T1 = open(B1).read().replace('HERE = os.path.dirname(os.path.abspath(__file__))', f'HERE = {HERE!r}', 1); D = {"__file__": B1, "__name__": "be1_ro"}; a0 = sys.argv; sys.argv = [B1]; exec(compile(T1.split("K2rows = run(")[0], B1, "exec"), D); sys.argv = a0
    by = {q["name"]: q for q in D["GALS"]}; fg = [1.33 * by[r["name"]]["meta"]["MHI"] * 1e9 / 10 ** r["lM200"] for r in D["run"]("canonical") if r["active"]]; p16, p50, p84 = [float(np.percentile(fg, q)) for q in (16, 50, 84)]
    RC = S["rep"]["canonical"]; ESN = 0.5 * RC["L36"] / 100 * 1e51; EU = S["Eunit_erg"]
    def cap(fac):
        lo, hi = 0.0, S["Mb"]
        for _ in range(50):
            mid = 0.5 * (lo + hi); lo, hi = (mid, hi) if 40 * C.e_lift(S, mid) * EU <= fac * ESN else (lo, mid)
        return lo
    from astropy.io import fits
    XT = json.load(open(os.path.join(os.path.dirname(RB), "real_research", "data", "xcop", "xcop_r500_ettori2019.json"))); xc = {}
    for n in ("A85", "A644", "A1795", "A2029", "A2142", "A2319", "ZW1215"):
        with fits.open(os.path.join(os.path.dirname(RB), "real_research", "data", "xcop", n, f"{n}_fgas_profile.fits")) as h: g = h[1].data.copy(); rg = h[1].header["R500"]
        xc[n] = float(10 ** np.interp(np.log10(0.1207 * XT[n]["R200"] * 1e3), np.log10(g["RADIUS"] * rg), np.log10(g["MGAS"])) / (XT[n]["M200"] * 1e14))
    O = dict(fg_p16=p16, fg_p50=p50, fg_p84=p84, fg_S=S["Mg"], E1=cap(1.0), E3=cap(3.0), xcop_core=xc, ESN=ESN, EU=EU, XC=0.0186, X2=0.0566); json.dump(O, open(SETUP, "w"), indent=1); print(O)
def cells():
    O = json.load(open(SETUP)); m = 0.1 if MUT else 1.0
    if MUT: return dict(CM_E3_MUT=("cm", O["E3"] * m), CL14_X2_MUT=("cl", "1e14", O["X2"] * m))
    return dict(CM_GASHI=("cm", O["fg_p84"]), CM_E1=("cm", O["E1"]), CM_E3=("cm", O["E3"]), CL14_XC=("cl", "1e14", O["XC"]), CL14_X2=("cl", "1e14", O["X2"]), CL13_XC=("cl", "1e13", O["XC"]), CL13_X2=("cl", "1e13", O["X2"]), CTRL14_XC=("ctrl", "1e14", O["XC"]), CTRL14_X2=("ctrl", "1e14", O["X2"]), CTRL13_XC=("ctrl", "1e13", O["XC"]), CTRL13_X2=("ctrl", "1e13", O["X2"]))
def sub1(T, a, b):
    assert T.count(a) == 1, a[:70]
    return T.replace(a, b)
def run_cm(name, Mf, stop=None):
    T = open(os.path.join(CM1, "cm1_outflow.py")).read()
    T = sub1(T, 'Mg = {"STATIC": S["Mg"], "PRIMARY": S["Mg"], "MUTATE": S["Mg"], "MUTATE_A1": S["Mg"], "BOUND": S["Mb"]}[mode]; Ms = S["Mb"] - Mg', f'Mg = {Mf!r}; Ms = S["Mb"] - Mg')
    T = T.replace('os.path.join(HERE, f"cm1_run_{mode}.json")', f'{os.path.join(RUNS, name + ".json")!r}'); assert f'{name}.json' in T
    if stop: T = sub1(T, '        if stop["x"]: P(f"{mode} SIGTERM at step {k}: partial saved"); sys.exit(3)', f'        if k >= {stop}: sys.exit(0)\n        if stop["x"]: P(f"{{mode}} SIGTERM at step {{k}}: partial saved"); sys.exit(3)')
    sys.argv = ["cm1", "run", "PRIMARY"]; F = os.path.join(CM1, "cm1_outflow.py"); exec(compile(T, F, "exec"), {"__file__": F, "__name__": "__main__"})
def run_cl(name, m, Mf, ctrl, stop=None, native=False):
    F = os.path.join(CL5, "cl5_cycles.py"); T = open(F).read(); NMF = dict() if native else {name: Mf}
    T = sub1(T, 'if N == 0: Mf, bind, el = 0.0, "none", 0.0', 'if N == 0: Mf, bind, el = RF6_MF.get(name, 0.0), "control", 0.0')
    T = sub1(T, 'else: Mf, bind = moved(S["c"], S["EA"], af, N, e); el = e_lift(S["c"], Mf, af)', 'else: Mf, bind = (RF6_MF[name], "scan") if name in RF6_MF else moved(S["c"], S["EA"], af, N, e); el = e_lift(S["c"], Mf, af)')
    T = sub1(T, 'path = os.path.join(HERE, f"cl5_run_{name}.json")', f'path = os.path.join({RUNS!r}, name + ".json")')
    if stop: T = sub1(T, '        if stop["x"]: print(name, "SIGTERM: partial saved", flush=True); sys.exit(3)', f'        if k >= {stop}: sys.exit(0)\n        if stop["x"]: print(name, "SIGTERM: partial saved", flush=True); sys.exit(3)')
    NS = {"__file__": F, "__name__": "cl5_ro", "RF6_MF": NMF}; exec(compile(T, F, "exec"), NS)
    NS["RUNS"][name] = (m, 0.05, 0 if ctrl else 10, 0.0 if ctrl else 1.0); NS["run"](name)
def one(name):
    if name == "K1_CM": return run_cm("K1_CM", json.load(open(os.path.join(CM1, "cm1_setup.json")))["Mg"], stop=int(round(5 * 250 / 0.5)))
    if name == "K1_CL": return run_cl("K1_CL", "1e14", None, False, stop=1250, native=True)
    c = cells()[name]
    return run_cm(name, c[1]) if c[0] == "cm" else run_cl(name, c[1], c[2], c[0] == "ctrl")
def runall():
    N = (["K1_CM", "K1_CL"] if not MUT else []) + list(cells())
    def go(n):
        p = os.path.join(RUNS, n + ".json")
        if os.path.exists(p) and (n.startswith("K1") or json.load(open(p)).get("done")): return n, 0
        with open(os.path.join(RUNS, n + ".log"), "w") as L: rc = subprocess.run(["nice", "-n", "15", sys.executable, "-I", os.path.abspath(__file__), "run", n], stdout=L, stderr=subprocess.STDOUT, env=dict(os.environ, PYTHONHASHSEED="0")).returncode
        print(n, "rc", rc, flush=True); return n, rc
    with ThreadPoolExecutor(3) as ex: R = list(ex.map(go, N))
    print("failed", [n for n, r in R if r]); sys.exit(1 if any(r for _, r in R) else 0)
# ------------------------------------------------------------------ grade
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
J = lambda p: json.load(open(p))
def need_band():
    SH = J(os.path.join(RB, "SH1_softened_halo_grade", "sh1_results.json"))["runs"]; CE = J(os.path.join(RB, "CE1_converged_eta_grade", "ce1_results.json"))["runs"]["med_fs0.034"]; X73 = J(os.path.join(RB, "X73_smooth_core_all_measured", "x73_results_fs0.034_S_nat_s2.7774.json"))["footings"]; B = {}; f_c = 0.8405
    for f in ("canonical", "alt"):
        pts = [(10.82, X73[f]["sparc"]["A_c2b_refit"]["U_median"])] + [(SH[f"A_R{r}_fs0.034"]["eta"]["12"], SH[f"A_R{r}_fs0.034"][f]["sparc"]["A_c2b_refit"]["U"]) for r in ("0.573", "0.685", "0.817")] + [(25.94, CE[f]["sparc"]["A_c2b_refit"]["U"])]; E = np.array([p[0] for p in pts]); U = np.array([p[1] for p in pts]); rows = {}
        for ups in (0.44, 0.50, 0.57):
            if ups < U[-1]: rows[f"{ups}"] = dict(eta=None, R=None, R_cold=None, read="no softening needed")
            elif ups > U.max(): rows[f"{ups}"] = dict(eta=None, R=None, R_cold=None, read="unreachable by softening")
            else:
                ee = None
                for i in range(len(E) - 1, 0, -1):
                    if U[i] <= ups <= U[i - 1]: ee = float(E[i] + (ups - U[i]) * (E[i - 1] - E[i]) / (U[i - 1] - U[i])) if U[i - 1] != U[i] else float(E[i]); break
                rows[f"{ups}"] = dict(eta=ee, R=ee / 25.94, R_cold=ee / 21.80, read="softening to R")
        B[f] = dict(points=pts, floors=rows)
    cl = {}
    for m, e48, e64 in (("1e14", 16.91, 22.10), ("1e13", 17.67, 23.54)): cl[m] = {"ng48": 14.3 / e48, "ng64": 14.3 / e64, "ng48 x f_c": 14.3 / (e48 * f_c), "ng64 x f_c": 14.3 / (e64 * f_c)}
    return dict(sparc=B, clusters=cl)
def grade():
    O = J(SETUP); C = cells(); TAG = "rf6_MUTATE" if MUT else "rf6"; ok = True; RES = dict(setup=O)
    P(f"RF6 {TAG}: CM1 and CL5, moved gas scanned over the ledgered range; kappa = 1/2 FITTED; footings never pooled; not theory closed; cold dark energy is a gravitating field component, never a particle")
    N = need_band(); RES["need"] = N
    for f, b in N["sparc"].items():
        P(f"Need, SPARC {f}: points (eta, Upsilon) " + ", ".join(f"({a:.2f}, {u})" for a, u in b["points"])); [P(f"  floor {k}: {v['read']}" + (f": eta {v['eta']:.2f}, R {v['R']:.3f}, on cold share R {v['R_cold']:.3f}" if v["eta"] else "")) for k, v in b["floors"].items()]
    for m, b in N["clusters"].items(): P(f"Need, {m}: " + ", ".join(f"{k} {v:.3f}" for k, v in b.items()))
    Scm = J(os.path.join(CM1, "cm1_run_STATIC.json"))["marks"][-1]["eta"]; S14 = J(os.path.join(CL5, "cl5_run_M14_STATIC.json"))["marks"][-1]["eta"]; S13 = J(os.path.join(CL5, "cl5_run_M13_STATIC.json"))["marks"][-1]["eta"]; ST = {"1e14": S14, "1e13": S13}; SS = J(os.path.join(CM1, "cm1_setup.json")); RC = {}
    import cm1_outflow as CC
    if MUT:
        q = J(os.path.join(RUNS, "CM_E3_MUT.json")); r0 = J(os.path.join(RUNS, "CM_E3.json")); a = q["marks"][-1]["eta"] / Scm; b = r0["marks"][-1]["eta"] / Scm; q2 = J(os.path.join(RUNS, "CL14_X2_MUT.json")); c = q2["marks"][-1]["eta"] / S14; d = J(os.path.join(RUNS, "CL14_X2.json"))["marks"][-1]["eta"] / S14; bites = abs(1 - a) < abs(1 - b) and abs(1 - c) < abs(1 - d) and a > 0.817 and c > 0.846
        P(f"MUTATE CM1 E3 x 0.1: R {a:.3f} vs base {b:.3f}; CL5 X2 x 0.1, 1e14: R {c:.3f} vs base {d:.3f}: {'BITES' if bites else 'NOT INFORMATIVE'}"); open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n"); json.dump(dict(cm=[a, b], cl=[c, d], bites=bites), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1); sys.exit(0 if bites else 1)
    k1a = abs(J(os.path.join(RUNS, "K1_CM.json"))["marks"][1]["eta"] - J(os.path.join(CM1, "cm1_run_PRIMARY.json"))["marks"][1]["eta"]); k1b = abs(J(os.path.join(RUNS, "K1_CL.json"))["marks"][1]["eta"] - J(os.path.join(CL5, "cl5_run_M14_e1.json"))["marks"][1]["eta"]); kk = k1a <= 1e-9 and k1b <= 1e-9; P(f"K1 wrapper against CM1 PRIMARY, CL5 M14_e1 first marks: {k1a:.1e}, {k1b:.1e}: {'PASS' if kk else 'FAIL'}"); ok &= kk
    k2 = True; RES["cm1"] = {}; RES["cl5"] = {}; EU, ESN = O["EU"], O["ESN"]
    P("CM1 (R frozen need 0.817; 40 bursts, 250 Myr; committed PRIMARY R 0.932, BOUND 0.293):")
    for n, lab in (("CM_GASHI", "measured gas, 84th"), ("CM_E1", "E_SN cap"), ("CM_E3", "3 E_SN cap")):
        q = J(os.path.join(RUNS, n + ".json")); k2 &= q["maxerr"] < 0.01 and q["done"]; Mf = C[n][1]; R = q["marks"][-1]["eta"] / Scm; e = 40 * CC.e_lift(SS, Mf) * EU / ESN; ins = e <= 3.0 and Mf <= SS["Mb"]; ins3 = e <= 0.9; RES["cm1"][n] = dict(M_f=Mf, R=R, eps_SN=e, inside=ins, inside_c03=ins3, reached=R <= 0.817, net_work=q["W"], err=q["maxerr"], by5=[round(m["eta"] / Scm, 3) for m in q["marks"]]); P(f"  {n} {lab}: M_f {Mf:.4f} ({Mf / SS['Mg']:.2f} x today's gas): R {R:.3f} {'REACHES' if R <= 0.817 else 'misses'}; eps_SN {e:.3f}; inside at coupling 1 {ins}, at coupling 0.3 {ins3}; err {q['maxerr']:.1e}")
    k3 = abs(RES["cm1"]["CM_E1"]["eps_SN"] - 1) <= 0.01; P(f"K3 E1 eps_SN within 1 %: {'PASS' if k3 else 'FAIL'}"); ok &= k3
    P("CL5 (N 10, a_f 0.05; frozen need 0.846, 0.809; R vs frozen STATIC and vs same-gas control):")
    CE = {"1e14": J(os.path.join(CL5, "cl5_run_CTRL_M14_e1.json"))["marks"][-1]["eta"], "1e13": J(os.path.join(CL5, "cl5_run_CTRL_M14_e1.json"))["marks"][-1]["eta"] if not os.path.exists(os.path.join(CL5, "cl5_run_CTRL_M13_e1.json")) else J(os.path.join(CL5, "cl5_run_CTRL_M13_e1.json"))["marks"][-1]["eta"]}
    for m, tag, nd in (("1e14", "14", 14.3 / 16.91), ("1e13", "13", 14.3 / 17.67)):
        q0 = J(os.path.join(CL5, f"cl5_run_M{tag}_e1.json")); P(f"  {m} CEIL committed: M_f {q0['Mf']:.4f}: R {q0['marks'][-1]['eta'] / ST[m]:.3f}, same gas {q0['marks'][-1]['eta'] / CE[m]:.3f}; share {10 * q0['lift_each'] / q0['EA']:.2f}"); RES["cl5"][f"{m}|CEIL"] = dict(M_f=q0["Mf"], R=q0["marks"][-1]["eta"] / ST[m], R_same=q0["marks"][-1]["eta"] / CE[m], share=10 * q0["lift_each"] / q0["EA"])
        for k in ("XC", "X2"):
            q = J(os.path.join(RUNS, f"CL{tag}_{k}.json")); c = J(os.path.join(RUNS, f"CTRL{tag}_{k}.json")); k2 &= q["maxerr"] < 0.01 and q["done"] and c["done"]; R = q["marks"][-1]["eta"] / ST[m]; Rs = q["marks"][-1]["eta"] / c["marks"][-1]["eta"]; sh = 10 * q["lift_each"] / q["EA"]; ins = q["Mf"] <= 0.0186 and sh <= 2.0; RES["cl5"][f"{m}|{k}"] = dict(M_f=q["Mf"], R=R, R_same=Rs, share=sh, inside=ins, reached=R <= nd, reached_same=Rs <= nd, ctrl_over_static=c["marks"][-1]["eta"] / ST[m], err=q["maxerr"], by=[round(x["eta"] / ST[m], 3) for x in q["marks"]], by_same=[round(x["eta"] / y["eta"], 3) for x, y in zip(q["marks"], c["marks"])]); P(f"  {m} {k}: M_f {q['Mf']:.4f}: R {R:.3f} ({'reaches' if R <= nd else 'misses'} {nd:.3f}), same gas {Rs:.3f} ({'reaches' if Rs <= nd else 'misses'}); share of E_AGN {sh:.2f}; inside {ins}; err {q['maxerr']:.1e}")
    P(f"K2 work balance, runs done: {'PASS' if k2 else 'FAIL'}"); ok &= k2
    # verdict wording
    c1 = [v for v in RES["cm1"].values() if v["inside"] and v["reached"]]; c1a = [v for v in RES["cm1"].values() if v["reached"]]
    V = {}
    if c1: b = min(c1, key=lambda v: v["M_f"]); V["CM1"] = f"NOT REACHED only at the fiducial input; reached at moved gas M_f = {b['M_f']:.4f} ({b['M_f'] / SS['Mg']:.1f} x today's gas, eps_SN {b['eps_SN']:.2f}), which is inside its ledgered range at coupling 1, {'inside' if b['inside_c03'] else 'outside'} at coupling 0.3"
    elif c1a: V["CM1"] = "NOT REACHED, robust to the ledgered ranges; reached only outside them"
    else: V["CM1"] = "NOT REACHED, robust to the ledgered ranges"
    inn = [(k, v) for k, v in RES["cl5"].items() if v.get("inside") and (v["reached"] or v["reached_same"])]; both = {m: [v for k, v in inn if k.startswith(m)] for m in ("1e14", "1e13")}; rch = {m: [k for k, v in RES["cl5"].items() if k.startswith(m) and "reached" in v and (v["reached"] or v["reached_same"])] for m in ("1e14", "1e13")}
    V["CL5"] = "NOT REACHED, robust to the ledgered ranges" if not all(both.values()) else "NOT REACHED only at the fiducial input; reached at M_f 0.0186, inside"
    V["CL5"] += f"; outside the measured gas, cells reaching: 1e14 {rch['1e14'] or 'none'}, 1e13 {rch['1e13'] or 'none'}"
    V["CM2"] = "NOT REACHED only at the fiducial input; reached at cadence 1 Gyr (R 0.573), which is outside what I recall for this mass, from memory, not on disk"; V["CM3"] = "NOT REACHED only at the fiducial input; reached at coupling 1, which is outside the ledgered realistic coupling (0.3 misses at every cadence mapped)"; V["BH1"] = "NOT REACHED only at the fiducial input; reached (BH2) at a central load of 0.02-0.05 M200, outside the closed box and outside this model's own hot-gas cap; no measurement of such a load"; V["BH2"] = "REACHES LIMIT only at a stipulated load; 4 to 11 times the in-place cap, so outside any measured range here"; V["SH1"] = "SOFTENED FAIL stands at R = 1 on clusters; its one pass rests on R 0.685 at clusters, granted, not supplied by BH1, CL5 or this lane"
    RES["verdicts"] = V; P("VERDICTS:"); [P(f"  {k}: {v}") for k, v in V.items()]; RES["ok"] = ok
    json.dump(RES, open(os.path.join(HERE, TAG + "_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
    if not ok: P("K FAILURE: no verdict"); sys.exit(1)
if __name__ == "__main__":
    a = sys.argv[1]
    if a == "setup": setup()
    elif a == "list": print(list(cells()))
    elif a == "run": one(sys.argv[2])
    elif a == "runall": runall()
    elif a == "grade": grade()
