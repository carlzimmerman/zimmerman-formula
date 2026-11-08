#!/usr/bin/env python3
"""KR2 grader (FROZEN_CRITERIA.md 92c1ced823): assembles parts/{battery,sparc,kids,lens}.json into kr2.json / kr2.out and the
MUTATE readout kr2_MUTATE.json / kr2_MUTATE.out. Label per footing (never pooled) from the frozen rule (section 5).
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, json, math

HERE = os.path.dirname(os.path.abspath(__file__)); PARTS = os.path.join(HERE, "parts")
FOOTS = ("canonical", "alt")
J = {k: json.load(open(os.path.join(PARTS, f"{k}.json"))) for k in ("battery", "sparc", "kids", "lens")}
OUT, MOUT = [], []
def P(s=""): print(s); OUT.append(str(s))
def M(s=""): print(s); MOUT.append(str(s))
def fmt(w): return "empty" if not w else (f"{{{w[0]:.4g}}}" if len(w) == 1 else f"[{w[0]:.4g}, {w[-1]:.4g}] ({len(w)} grid pts)")
ORDER = ("C1", "C2", "C3", "C5", "C6", "C7")
NAMES = dict(C1="SPARC clean", C2="X-COP core (KQ1 lines, NA2 per-bin)", C3="groups (UA1 interval)", C4="Bullet", C5="KiDS G6 with kSZ gas (KX1)",
             C6="hosts inside R500 (NC4)", C7="CMB lensing, corrected kernel (static)")

# ------------------------------------------------------------------ KA
ka = {}
B, S, K, L = J["battery"], J["sparc"], J["kids"], J["lens"]
ka["KA1_F1A_R"] = True
ka["KQ1_prefix_KA1-5"] = bool(B["KQ1_prefix_KA"]["ok"]); ka["KA7_battery"] = bool(B["KA7_battery"]["pass_"]); ka["KA6c_solvers"] = bool(K["KA6c"]["pass_"])
for f in FOOTS:
    for k, v in B[f]["KA"].items(): ka[f"{k}_{f}"] = bool(v["pass_"])
    ka[f"KA2_{f}"] = bool(S[f]["KA2"]["pass_"]); ka[f"KA7_sparc_{f}"] = bool(S[f]["KA7"]["pass_"])
    for k, v in K[f]["KA"].items(): ka[f"{k}_{f}"] = bool(v["pass_"])
    ka[f"KA8_{f}"] = bool(L[f]["KA8"]["pass_"])
KA_OK = all(ka.values())

# ------------------------------------------------------------------ MUTATE
mu_ = {}
for f in FOOTS:
    mu_[f"M1_Xcop_cusp_and_C2_{f}"] = bool(B[f]["M1"]["bites"])
    mu_[f"M1_C1_{f}"] = bool(S[f]["M1"]["bites"])
    mu_[f"M1_C5_{f}"] = bool(K[f]["M1"]["bites"])
    mu_[f"M2_C2_fails_at_f0_{f}"] = bool(B[f]["M2"]["bites"])
    mu_[f"M2_law_numbers_{f}"] = bool(B[f]["KA"]["KA3"]["pass_"] and B[f]["KA"]["KA5"]["pass_"] and S[f]["KA2"]["pass_"] and K[f]["KA"]["KA4"]["pass_"])
    mu_[f"M3_planted_core_holds_{f}"] = bool(B[f]["M3"]["holds"])
MUT_OK = all(mu_.values())

# ------------------------------------------------------------------ windows
GRID = [r["mu"] for r in B["canonical"]["grid"]]
def col_ok(f, col, var="R_B"):
    if col == "C1": return [r[var]["C1"] for r in S[f]["grid"]]
    if col == "C2": return [r[var]["C2"]["C2"] for r in B[f]["grid"]]
    if col == "C3": return [r[var]["C3"]["C3"] for r in B[f]["grid"]]
    if col == "C5": return [r[var]["C5"] for r in K[f]["grid"]]
    if col == "C6": return [r[var]["C2"]["C6"] for r in B[f]["grid"]]
    if col == "C7": return [r["C7_static"] for r in L[f]["grid"]]
def errs(f):
    n = sum(r["R_B"]["solver_errors"] for r in S[f]["grid"]) + sum(r["R_B"]["solver_errors"] for r in B[f]["grid"])
    ne = sum(1 for r in S[f]["grid"] if r["R_B"]["rule"] == "NOT EVALUABLE")
    return n, ne
RES = dict(lane="KR2", criteria="92c1ced823", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", grid=GRID, KA=ka, KA_all=KA_OK, MUTATE=mu_, MUTATE_all=MUT_OK, footings={})
P("KR2: the present-day mu_K window for the action's K(Q) dust (cold dark energy) at the CMB's amount. Criteria 92c1ced823.")
P(f"KA all: {'PASS' if KA_OK else 'FAIL'} ({sum(ka.values())}/{len(ka)}); MUTATE all bite / hold: {MUT_OK}")
for f in FOOTS:
    ok = {c: col_ok(f, c) for c in ORDER}; W = {c: [m for m, o in zip(GRID, ok[c]) if o] for c in ORDER}
    run = set(GRID); first = None; trace = []
    for c in ORDER:
        run &= set(W[c]); trace.append((c, sorted(run)))
        if not run and first is None: first = c
    today = sorted(set(GRID).intersection(*[set(W[c]) for c in ("C1", "C2", "C3", "C5", "C6")]))
    tfirst = None; rr = set(GRID)
    for c in ("C1", "C2", "C3", "C5", "C6"):
        rr &= set(W[c])
        if not rr and tfirst is None: tfirst = c
    allw = sorted(run)
    empty_own = [c for c in ORDER if not W[c]]
    disjoint = [(a, b) for i, a in enumerate(ORDER) for b in ORDER[i + 1:] if W[a] and W[b] and not set(W[a]) & set(W[b])]
    zr = {f"{r['mu']:.6g}": r["z_run_max"] for r in L[f]["grid"]}
    ne, nn = errs(f)
    if not (KA_OK and MUT_OK) or ne > 0: lab = "NO VERDICT"
    elif allw: lab = f"PASS (window {fmt(allw)})"
    else: lab = f"FAIL (empty at {first})"
    WA = {c: [m for m, o in zip(GRID, col_ok(f, c, "R_A")) if o] for c in ORDER if c != "C7"}
    WF = {c: [m for m, o in zip(GRID, col_ok(f, c, "fcapR_B")) if o] for c in ORDER if c != "C7"}
    RES["footings"][f] = dict(label=lab, windows=W, running=[dict(after=c, window=w) for c, w in trace], first_empty=first, window_all=allw,
                              today_window=today, today_first_empty=tfirst, empty_on_own=empty_own, disjoint_pairs=disjoint,
                              z_run_max=zr, z_run_max_on_today=[zr[f"{m:.6g}"] for m in today], solver_errors=ne, C1_not_evaluable_cells=nn,
                              reading_A_windows=WA, fcapR_B_windows=WF, C4="NOT EVALUABLE (RSS: DB1/UX6 child 1.19-1.48 GB)")
    P(""); P(f"=== {f}: LABEL {lab}")
    for c in ("C1", "C2", "C3", "C4", "C5", "C6", "C7"):
        if c == "C4": P(f"  C4 {NAMES[c]}: NOT EVALUABLE (RSS line; DB1/UX6 machinery 1.19-1.48 GB)"); continue
        P(f"  {c} {NAMES[c]}: window {fmt(W[c])}" + (f" | reading A {fmt(WA[c])} | f_cap R {fmt(WF[c])}" if c != "C7" else ""))
    P("  running intersection: " + "; ".join(f"after {c}: {fmt(w)}" for c, w in trace))
    P(f"  first column that empties it: {first}; empty on their own: {empty_own}; disjoint pairs: {disjoint}")
    P(f"  TODAY window (C1-C3, C5, C6; hand-off to KR1): {fmt(today)}" + (f"; first empty at {tfirst}" if not today else ""))
    P("  C7-run z_run,max by mu: " + ", ".join(f"{k}:{v}" for k, v in zr.items()))
    P(f"  solver errors in graded cells {ne}; C1 NOT EVALUABLE cells {nn}")
M("KR2 MUTATE readout (criteria 92c1ced823)")
for f in FOOTS:
    m1 = B[f]["M1"]; M(f"[{f}] M1 mu_B {m1['mu']:.4e}: X-COP at KD1 capture {m1['mean']:.6f} / {m1['rms']:.6f} vs KD1 {m1['kd1_mean']:.6f} / {m1['kd1_rms']:.6f}; "
                     f"max r_1/2 {m1['max_r_half_kpc']:.2e} kpc; C2 at R {'PASS' if m1['C2_at_R_label'] else 'FAIL'} -> {'BITES' if m1['bites'] else 'NO BITE'}")
    s1 = S[f]["M1"]; M(f"[{f}] M1 C1 at R: {'PASS' if s1['C1'] else 'FAIL'} (rule {s1['rule']}, rms {s1['rms']:.4f}, U {s1['U_median']:.2f}, over cap {s1['n_over_cap']}) -> {'BITES' if s1['bites'] else 'NO BITE'}")
    k1 = K[f]["M1"]; M(f"[{f}] M1 C5 at R: {'PASS' if k1['C5_at_R'] else 'FAIL'} z {', '.join('%+.2f' % z for z in k1['z_R'])}; f_cap R vs HY1 point |dz| {k1['d_vs_HY1']:.1e} -> {'BITES' if k1['bites'] else 'NO BITE'}")
    M(f"[{f}] M1 C7 static at mu_B: dchi2 {L[f]['M1']['dchi2']:.4f} (reported)")
    m2 = B[f]["M2"]; M(f"[{f}] M2 f 0: X-COP mean {m2['mean']:.6f}, C2 {'PASS' if m2['C2_at_f0'] else 'FAIL'}; SPARC rms {S[f]['KA2']['rms']:.8f}; KiDS max|d| {K[f]['KA']['KA4']['maxd']:.1e}; groups step {B[f]['KA']['KA5']['step']} -> {'BITES' if m2['bites'] else 'NO BITE'}")
    m3 = B[f]["M3"]; M(f"[{f}] M3 planted core: rms {m3['rms']:.4f}, L3 {m3['L3']}, L4 {m3['L4']} -> {'HOLDS' if m3['holds'] else 'FAILS'}")
M(f"MUTATE all: {MUT_OK}")
P(""); P("Adopts nothing. kappa = 1/2 FITTED; not theory closed."); M("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, "kr2.json"), "w"), indent=1)
open(os.path.join(HERE, "kr2.out"), "w").write("\n".join(OUT) + "\n")
json.dump(dict(MUTATE=mu_, battery={f: dict(M1=B[f]["M1"], M2=B[f]["M2"], M3=B[f]["M3"]) for f in FOOTS}, sparc={f: S[f]["M1"] for f in FOOTS},
               kids={f: K[f]["M1"] for f in FOOTS}, lens={f: L[f]["M1"] for f in FOOTS}, all=MUT_OK, note=RES["note"]),
          open(os.path.join(HERE, "kr2_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, "kr2_MUTATE.out"), "w").write("\n".join(MOUT) + "\n")
