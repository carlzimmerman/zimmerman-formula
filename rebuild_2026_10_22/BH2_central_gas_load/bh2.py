#!/usr/bin/env python3
"""BH2_central_gas_load: a central gas load beyond BH1's closed box, lifted by black hole energy, gravity only (BH1 and CM1 machinery read-only).
    python3 bh2.py setup; python3 bh2.py run NAME; python3 bh2.py list; python3 bh2.py grade"""
import json, os, sys, textwrap
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); BH1 = os.path.join(REB, "BH1_cluster_bh_coupling"); sys.path.insert(0, BH1)
import bh1 as B
C = B.C; MST = B.FS * B.FG; LOADS = {"L02": 0.02, "L05": 0.05, "L10": 0.10}; TAB = 0.00615; LIM = {"14": 0.845, "13": 0.809}
def cells():
    c = {f"{l}_N{n}": (l, n, 1.0) for l in LOADS for n in (3, 10)}; c.update({f"{l}_STATIC": (l, 10, 0.0) for l in LOADS}); c.update(UNCAP=("L10", 10, None), MUTATE=("L05", 3, 0.01)); return c
GRID = cells()
def idir(m, l): d = os.path.join(HERE, f"ics_{m}_{l}"); os.makedirs(d, exist_ok=True); return d

def setup():
    src = open(os.path.join(REB, "CM1_outflow_coupling", "cm1_outflow.py")).read(); body = src.split("    # cold density")[1].split("    xc = float(np.sort(r)[499])")[0]
    old = 'Mb = S["Mb"]; a = S["a_star"]; Mt = Mc + hern_M(rg, Mb, a)'; assert body.count(old) == 1
    body = body.replace(old, 'Mt = Mc + hern_M(rg, MST + L, AS) + hern_M(rg, FG - L, AG)')
    for m in B.ETA:
        S1 = json.load(open(os.path.join(B.mdir(m), "setup.json")))
        for l, L in LOADS.items():
            S = dict(c=S1["c"], eta_c=S1["eta_c"]); ns = dict(vars(C)); ns.update(S=S, c=S1["c"], HERE=idir(m, l), SEED=1, MST=MST, L=L, FG=B.FG, AS=B.AS, AG=B.AG); exec(textwrap.dedent("    # cold density" + body), ns)
            r = np.linalg.norm(ns["pos"], axis=1); xc = float(np.sort(r)[499]); S.update(xc500=xc, eta_analytic=C.eta_a(C.a_fit_profile(C.M_nfw(S1["c"]), xc)), eta_t0=C.eta_p(ns["pos"], xc), L=L, M200=S1["M200"], R200_kpc=S1["R200_kpc"], Eunit_erg=S1["Eunit_erg"], E_BH_erg=S1["E_BH_erg"])
            json.dump(S, open(os.path.join(idir(m, l), "setup.json"), "w"), indent=1); print(m, l, S, flush=True)

def sched(L, N, eps, S):
    Mst, Mh = MST + L, B.FG - L; E = lambda f: B.lift(f, "G1", S, Mst, Mh) * S["Eunit_erg"]
    if eps == 0: return [(0.0, L)] * N
    if eps is None or E(L) <= eps * S["E_BH_erg"] / N: return [(L, L)] * N
    lo, hi = 0.0, L
    for _ in range(50):
        mid = 0.5 * (lo + hi); lo, hi = (mid, hi) if E(mid) <= eps * S["E_BH_erg"] / N else (lo, mid)
    return [(lo, L)] * N

def run(name):
    if name == "K1":
        d = B.mdir("14"); S = json.load(open(os.path.join(d, "setup.json"))); I = np.load(os.path.join(d, "cm1_ics.npz")); sch = B.schedule("G1", 3, 1.0, S, S["Eunit_erg"], S["E_BH_erg"])
        return B.integrate(I["pos"].copy(), I["vel"].copy(), float(I["mp"]), S["xc500"], "G1", 3, sch, MST, B.FG, B.AS, B.AG, B.TOT, os.path.join(HERE, "bh2_run_K1.json"), dict(name="K1"))
    m, cell = name.split("_", 1); l, N, eps = GRID[cell]; L = LOADS[l]; d = idir(m, l); S = json.load(open(os.path.join(d, "setup.json"))); I = np.load(os.path.join(d, "cm1_ics.npz")); sch = sched(L, N, eps, S)
    use = sum(B.lift(f, "G1", S, MST + L, B.FG - L) * S["Eunit_erg"] for f, _ in sch if f > 0)
    B.integrate(I["pos"].copy(), I["vel"].copy(), float(I["mp"]), S["xc500"], "G1", N, sch, MST + L, B.FG - L, B.AS, B.AG, B.TOT, os.path.join(HERE, f"bh2_run_{name}.json"), dict(name=name, L=L, N=N, eps=eps, E_used_erg=use, E_BH_erg=S["E_BH_erg"]))

def grade():
    out = []
    def P(s): print(s, flush=True); out.append(s)
    J = lambda n: json.load(open(os.path.join(HERE, f"bh2_run_{n}.json")))
    P("BH2 central gas load (see FROZEN_CRITERIA.md); upper-bound test, load not derived; inputs PROVISIONAL; kappa = 1/2 FITTED; not theory closed; cold dark energy is a gravitating field, never a particle")
    a = J("K1")["marks"][-1]["eta"]; b = json.load(open(os.path.join(BH1, "bh1_run_14_G1_N3.json")))["marks"][-1]["eta"]; k1 = abs(a / b - 1) < 1e-6; P(f"K1 eta {a:.6f} vs BH1 14_G1_N3 {b:.6f}: {'PASS' if k1 else 'FAIL'}")
    k2, k3, k4, k5, done = True, True, True, True, True; RES = {}; first = {}; mut = {}
    for m in B.ETA:
        RES[m] = {}; st = {}; first[m] = dict(limit=None, clean=None)
        for l in LOADS:
            S = json.load(open(os.path.join(idir(m, l), "setup.json"))); q = J(f"{m}_{l}_STATIC"); st[l] = q["marks"][-1]["eta"]; d = st[l] / q["marks"][0]["eta"]; k4 &= 0.97 <= d <= 1.03; k5 &= abs(S["eta_t0"] / S["eta_analytic"] - 1) <= 0.05; k2 &= q["maxerr"] < 0.01; done &= q["done"]
            P(f"[1e{m} {l}] L {S['L']:.2f} M200 = {S['L'] * S['M200']:.2e} Msun = {S['L'] / TAB:.1f} x closed box; x_c {S['xc500']:.4f}; eta t0 {S['eta_t0']:.2f} (analytic {S['eta_analytic']:.2f}); STATIC end {st[l]:.2f} (drift {d:.3f}); LIMIT R {LIM[m]}")
        for c, (l, N, e) in GRID.items():
            if c.endswith("STATIC"): continue
            q = J(f"{m}_{c}"); R = q["marks"][-1]["eta"] / st[l]; f = q["schedule"][0][0]; k2 &= q["maxerr"] < 0.01; done &= q["done"]
            if e is not None: k3 &= q["E_used_erg"] <= e * q["E_BH_erg"] * (1 + 1e-6) and f <= LOADS[l] * (1 + 1e-12)
            RES[m][c] = dict(R=R, moved=f, L=LOADS[l], E_over_EBH=q["E_used_erg"] / q["E_BH_erg"], err=q["maxerr"]); P(f"  {c}: R {R:.3f}; moved {f:.5f} M200 per burst; E/E_BH {RES[m][c]['E_over_EBH']:.3g}; err {q['maxerr']:.1e}")
        for l, L in LOADS.items():
            b = min(RES[m][f"{l}_N{n}"]["R"] for n in (3, 10))
            if first[m]["limit"] is None and b <= LIM[m]: first[m]["limit"] = L
            if first[m]["clean"] is None and b <= 0.685: first[m]["clean"] = L
        x, y = RES[m]["L05_N3"]["R"], RES[m]["MUTATE"]["R"]; mut[m] = "NOT INFORMATIVE" if abs(1 - x) < 0.03 else ("PASS" if abs(1 - y) < abs(1 - x) else "FAIL")
        P(f"  smallest L at LIMIT {first[m]['limit']}, at CLEAN {first[m]['clean']}; MUTATE eps 0.01 R {y:.3f} vs eps 1 R {x:.3f}: {mut[m]}")
    P(f"K2 work balance: {'PASS' if k2 else 'FAIL'}; K3 caps: {'PASS' if k3 else 'FAIL'}; K4 static drift: {'PASS' if k4 else 'FAIL'}; K5 t0 eta: {'PASS' if k5 else 'FAIL'}; all done: {done}")
    ok = k1 and k2 and k3 and k4 and k5 and done and "FAIL" not in mut.values()
    if not ok: v = "NOT DECIDED"
    elif all(first[m]["clean"] for m in B.ETA): v = f"REACHES CLEAN AT LOAD {max(first[m]['clean'] for m in B.ETA)}"
    elif all(first[m]["limit"] for m in B.ETA): v = f"REACHES LIMIT AT LOAD {max(first[m]['limit'] for m in B.ETA)}"
    else: v = "NOT REACHED AT ANY LOAD (" + ("energy-limited" if all(RES[m]["UNCAP"]["R"] <= LIM[m] for m in B.ETA) else "channel-limited") + ")"
    P(f"VERDICT: {v}")
    open(os.path.join(HERE, "bh2.out"), "w").write("\n".join(out) + "\n"); json.dump(dict(R=RES, first=first, verdict=v, K1=k1, K2=k2, K3=k3, K4=k4, K5=k5, mutate=mut), open(os.path.join(HERE, "bh2_results.json"), "w"), indent=1)

if __name__ == "__main__":
    a = sys.argv[1]
    if a == "setup": setup()
    elif a == "run": run(sys.argv[2])
    elif a == "list": print("\n".join(["K1"] + [f"{m}_{c}" for m in B.ETA for c in GRID]))
    else: grade()
