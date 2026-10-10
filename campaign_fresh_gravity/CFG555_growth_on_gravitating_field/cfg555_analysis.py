#!/usr/bin/env python3
"""CFG555 analysis (FROZEN_CRITERIA.md): the CFG361 growth statistic (sigma8 ratio; max|P/P_S0 - 1| for k <= 1 h/Mpc; FAIL / GROWTH OK / TENSION)
re-applied to the GRAVITATING density (particles + e - comp) of every run behind PAPER45 and its confirmations, from the per-run caches written by
cfg555_compute.py (../_external_data/cfg555_work) and, for CFG530, from CFG530's own profile caches (built with the same captured-potential method).
  python3 cfg555_analysis.py                 -> cfg555_analysis.out / cfg555_results.json
  CFG555_MUTATE=1 python3 cfg555_analysis.py -> source switched off (delta_src := 0): must reproduce the lanes' particle numbers
                                                 -> cfg555_analysis_MUTATE.out / cfg555_results_MUTATE.json"""
import os, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W = os.path.join(EXT, "cfg555_work"); PROF530 = os.path.join(EXT, "cfg530_work", "profiles")
MUT = os.environ.get("CFG555_MUTATE", "0") == "1"
LINES, OUT = [], {"lane": "CFG555", "date": "2026-10-10", "mutate_source_off": MUT}
def P(s=""): print(s); LINES.append(s)
def cat(s8, pd): return "FAIL" if abs(s8 - 1) > 0.20 else ("GROWTH OK" if abs(s8 - 1) <= 0.05 and pd <= 0.10 else "TENSION")
def lj(p): return json.load(open(p))

def stat(k, Pr, s8r, k0, P0, s80):
    k = np.array(k); m = k <= 1.0; r = np.array(Pr)[m] / np.interp(k[m], np.array(k0), np.array(P0))
    i = int(np.argmax(np.abs(r - 1)))
    rf = np.array(Pr) / np.interp(k, np.array(k0), np.array(P0))
    at = {str(x): float(rf[int(np.argmin(np.abs(k - x)))]) for x in (0.5, 1.0, 2.0, 4.0) if x <= k.max() * 1.01}
    return dict(s8=s8r / s80, pdev=float(np.abs(r[i] - 1)), k_at=float(k[m][i]), r_at=at, verdict=cat(s8r / s80, float(np.abs(r[i] - 1))))

# ------------------------------------------------------------------------------------------------ committed lane numbers (particle-based)
C = lambda p: lj(os.path.join(CFG, p))
r424, r425, r426, r427 = (C(f"CFG42{i}_{n}/cfg42{i}_results.json") for i, n in ((4, "turnaround_catchment"), (5, "turnaround_catchment_confirm"),
                                                                                    (6, "zero_knob_de_and_alt_seeds"), (7, "zero_knob_inherited_settings")))
r439 = C("CFG439_zero_knob_alt_512/cfg439_results.json"); r460 = C("CFG460_zero_knob_512_second_seed/cfg460_results.json")
r518 = C("CFG518_depletion_consistent_growth/cfg518_results.json"); r527 = C("CFG527_law_respecting_engine/cfg527_results.json")
r530 = C("CFG530_fixed_box_convergence/cfg530_results.json")
g = lambda d, key: (d[key]["s8"], d[key]["pdev"])
LANE_RUNS = {   # lane -> [(cache name, committed (s8, pdev), counted as a pass by the lane?)]
    "CFG424": [("424_TAcan", g(r424, "TA-can"), True), ("424_TAalt", g(r424, "TA-alt"), True), ("424_MUTATE_nocomp", g(r424, "MUTATE (no compensation)"), False)],
    "CFG425": [("425_R1_can_s360", g(r425, "R1 256^3 seed 360"), True), ("425_R2_can_s361", g(r425, "R2 256^3 seed 361"), True),
               ("425_R3_can_512", g(r425, "R3 512^3 seed 359"), True)],
    "CFG426": [("426_D1_DEcan", g(r426, "D1 DE canonical 359"), True), ("426_D2_DEalt", g(r426, "D2 DE alt 359"), True),
               ("426_A1_alt_s360", g(r426, "A1 FLAT alt 360"), True), ("426_A2_alt_s361", g(r426, "A2 FLAT alt 361"), True)],
    "CFG427": [("427_E1_eps0.0385", g(r427, "E1 eps 0.0385"), True), ("427_E2_eps0.154", g(r427, "E2 eps 0.154"), True),
               ("427_G1_MIXB", g(r427, "G1 MIXB"), True), ("427_G2_HOT1", g(r427, "G2 HOT1"), True)],
    "CFG439": [("439_A_alt_512", g(r439, "A FLAT alt"), True), ("439_B_DEcan_512", g(r439, "B DE canonical"), True)],
    "CFG460": [("460_can_512_s360", (r460["s8"], r460["pdev"]), True)],
    "CFG518": [("518_DCcan", g(r518, "DC-can"), True), ("518_DCalt", g(r518, "DC-alt"), True), ("518_MUTATE_nocomp", g(r518, "MUTATE (no compensation)"), False),
               ("518_K1_fretone", g(r518, "K1 (f_ret = 1)"), False), ("518_DCcan_512", g(r518, "DC-can 512^3"), True)],
    "CFG527": [("527_LRcan_L200", g(r527["boxes"]["200"], "LR-can"), True), ("527_LRalt_L200", g(r527["boxes"]["200"], "LR-alt"), True),
               ("527_MUTB_nocomp_L200", g(r527["boxes"]["200"], "MUTATE B"), False)],
}
PAPER45 = ["424_TAcan", "424_TAalt", "425_R1_can_s360", "425_R2_can_s361", "426_A1_alt_s360", "426_A2_alt_s361", "426_D1_DEcan", "426_D2_DEalt",
           "427_E1_eps0.0385", "427_E2_eps0.154", "427_G1_MIXB", "427_G2_HOT1", "425_R3_can_512", "439_A_alt_512", "439_B_DEcan_512"]

# ------------------------------------------------------------------------------------------------ reproduction gates
def gates(d):
    sh = d["shared_diag"]; why, ok, f32 = [], True, True
    N3 = d["N"] ** 3
    for key in ("q_max", "e_mean", "e_sum"):
        if key in sh:
            a, b = sh[key]; rel = abs(a - b) / max(abs(b), 1e-30)
            ok1 = rel <= 1e-6; ok &= ok1; f32 &= rel <= 1e-4; why.append(f"{key} rel {rel:.1e}")
    if "n_catch" in sh:
        ok &= sh["n_catch"][0] == sh["n_catch"][1]; why.append(f"n_catch {sh['n_catch'][0]:.0f}/{sh['n_catch'][1]:.0f}")
    if "src_sum" in sh:
        esc = max(abs(sh["e_sum"][1]) if "e_sum" in sh else 0.0, N3 * abs(sh["e_mean"][1]) if "e_mean" in sh else 0.0)
        dd = abs(sh["src_sum"][0] - sh["src_sum"][1]); ok &= dd <= 1e-6 * esc; why.append(f"src_sum |d| {dd:.1e} (<= {1e-6 * esc:.1e})")
    rest = [abs(a - b) / max(abs(b), 1e-12) for k_, (a, b) in sh.items() if k_ not in ("q_max", "e_mean", "e_sum", "n_catch", "src_sum")]
    why.append(f"other diag max rel {max(rest) if rest else 0:.1e} ({len(rest)} keys, reported)")
    k = np.array(d["k"]); m = k <= 1.0
    r2 = float(np.max(np.abs(np.array(d["P_part"])[m] / np.array(d["P_part_json"])[m] - 1))); s2 = abs(d["s8_part"] / d["s8_part_json"] - 1)
    ok &= r2 <= 1e-4 and s2 <= 1e-5; why.append(f"R2 P rel {r2:.1e}, s8 rel {s2:.1e}")
    r3 = abs(d["mean_grav_minus_p"]); ok &= r3 <= 1e-6; why.append(f"R3 mean(grav-p) {r3:.1e}")
    sf = float(np.max(np.abs(np.array(d["P_part_splitfn"]) / np.array(d["P_part"]) - 1)))
    why.append(f"split-fn particle identity {sf:.1e}")
    return bool(ok), bool(f32), "; ".join(why)

P(__doc__.strip().splitlines()[0])
P("Statistic: CFG361 cuts (FAIL |s8-1| > 0.20; GROWTH OK |s8-1| <= 0.05 and max|P-1|(k<=1) <= 0.10; else TENSION), vs each lane's matched S0 JSON.")
P("MUTATE MODE: delta_src := 0 (source off) -- the 'gravitating' columns below are the particle field." if MUT else
  "Gravitating density delta_grav = -k^2 phi_k / (1.5 Om) from the engine's own forces on the saved z = 0 state (particles + (e - comp)/(1.5 Om)).")

# ------------------------------------------------------------------------------------------------ controls on the S0 capture path
s0c = lj(os.path.join(W, "cfg555_S0_359_N256.json"))
OUT["controls"] = dict(C2_s0_maxdiff_rel=s0c["s0_maxdiff_rel"], C2_inject_ratio_dev=s0c["C2_inject_ratio_dev"],
                       C1_syn_recovery_maxrel=s0c["C1_syn_recovery_maxrel"])
c1 = s0c["C1_syn_recovery_maxrel"] <= 1e-5; c2 = s0c["s0_maxdiff_rel"] <= 1e-4 and s0c["C2_inject_ratio_dev"] <= 1e-5
P(f"\nC1 synthetic source (P_syn = 0.05 P_S0, fixed amplitude) recovered bin by bin: max rel {s0c['C1_syn_recovery_maxrel']:.1e} (<= 1e-5) -> {'PASS' if c1 else 'FAIL'}")
P(f"C2 capture on S0: max|grav - p| / peak {s0c['s0_maxdiff_rel']:.1e} (<= 1e-4); (1 + 0.05) delta injected -> P ratio dev from 1.1025 {s0c['C2_inject_ratio_dev']:.1e} (<= 1e-5) -> {'PASS' if c2 else 'FAIL'}")
OUT["controls"].update(C1_pass=c1, C2_pass=c2)

# ------------------------------------------------------------------------------------------------ per run
RUN = {}
P("\nPer run (z = 0).  particle = the lanes' field; grav = the gravitating field.  C0 = |recomputed particle - committed| (s8 / max|P-1|).")
P(f"  {'run':24s} {'N':>4s} | {'part s8':>8s} {'max|P-1|':>8s} | {'grav s8':>8s} {'max|P-1|':>8s} {'k@max':>5s} {'verdict (grav)':>15s} | r_grav @0.5/1/2   | C0 d(s8)/d(P)    gates")
for lane, runs in LANE_RUNS.items():
    for name, (cs8, cpd), counted in runs:
        f = os.path.join(W, f"cfg555_{name}.json")
        if not os.path.exists(f):
            RUN[name] = dict(status="NOT EVALUABLE (cache missing; run cfg555_compute.py)"); P(f"  {name:24s} MISSING"); continue
        d = lj(f)
        if "missing" in d:
            RUN[name] = dict(status="NOT EVALUABLE (z = 0 state missing)", missing=d["missing"]); P(f"  {name:24s} z0 state MISSING"); continue
        s0 = lj(os.path.join(EXT, d["s0_base"] + ".json"))["snap"]["z0"]
        part = stat(d["k"], d["P_part"], d["s8_part"], s0["k"], s0["P"], s0["sigma8"])
        if MUT:
            grav = stat(d["k"], d["P_part"], d["s8_part"], s0["k"], s0["P"], s0["sigma8"])
        else:
            grav = stat(d["k"], d["P_grav"], d["s8_grav"], s0["k"], s0["P"], s0["sigma8"])
        split = stat(d["k"], d["P_grav_splitdeconv"], d["s8_grav_splitdeconv"], s0["k"], s0["P"], s0["sigma8"])
        ok, f32, why = gates(d)
        c0 = (abs(part["s8"] - cs8), abs(part["pdev"] - cpd)); c0ok = max(c0) <= 1e-4
        st = "EVALUATED" if ok else "NOT EVALUABLE (reproduction gate)"
        RUN[name] = dict(lane=lane, N=d["N"], foot=d["foot"], branch=d["branch"], mix=d["mix"], counted_as_pass=counted, committed=dict(s8=cs8, pdev=cpd),
                         particle=part, gravitating=grav, grav_split_deconv_reported=split, C0=dict(d_s8=c0[0], d_pdev=c0[1], pass_=c0ok),
                         gates_pass=ok, gates_f32=f32, gates=why, status=st, src_rms=d["src_rms"], s8_src_alone=d["s8_src"],
                         s8_src_over_s8_part=d["s8_src"] / d["s8_part"], shared_diag=d["shared_diag"])
        ra = grav["r_at"]
        P(f"  {name:24s} {d['N']:4d} | {part['s8']:8.4f} {part['pdev']:8.4f} | {grav['s8']:8.4f} {grav['pdev']:8.4f} {grav['k_at']:5.2f} {grav['verdict']:>15s} | "
          f"{ra.get('0.5', float('nan')):.3f}/{ra.get('1.0', float('nan')):.3f}/{ra.get('2.0', float('nan')):.3f} | {c0[0]:.1e}/{c0[1]:.1e} {'ok' if c0ok else 'FAIL'}  "
          f"{'PASS' if ok else 'FAIL'}")
        P(f"  {'':24s}      gates: {why}")
        P(f"  {'':24s}      reported: split-deconvolution grav s8 {split['s8']:.4f} max|P-1| {split['pdev']:.4f}; source alone sigma8 {d['s8_src']:.4f} "
          f"({d['s8_src'] / d['s8_part']:.3f} of particles)")

# ------------------------------------------------------------------------------------------------ CFG530 from its own caches
P("\nCFG530 (from CFG530's profile caches, built by cfg530_profiles.py with the CFG526 captured-potential method; S0 = the matched S0 cache at the same L, N)")
R530 = {}
def kcheck530(K):
    sh = K["shared"]; ok = True; why = []
    for key in ("e_sum", "q_max"):
        if key in sh:
            a, b = sh[key]; rel = abs(a - b) / max(abs(b), 1e-30); ok &= rel <= 1e-6; why.append(f"{key} rel {rel:.1e}")
    if "n_catch" in sh: ok &= sh["n_catch"][0] == sh["n_catch"][1]; why.append("n_catch eq" if sh["n_catch"][0] == sh["n_catch"][1] else "n_catch DIFF")
    if "src_sum" in sh and "e_sum" in sh:
        dd = abs(sh["src_sum"][0] - sh["src_sum"][1]); ok &= dd <= 1e-6 * abs(sh["e_sum"][1]); why.append(f"src_sum |d| {dd:.1e}")
    ok &= abs(K["mean_grav_minus_p"]) <= 1e-6 and K["pk_z0_check"] <= 1e-4
    why.append(f"mean(grav-p) {K['mean_grav_minus_p']:.1e}; P z0 check {K['pk_z0_check']:.1e}")
    return bool(ok), "; ".join(why)
for L in (100, 200):
    for N in (128, 256, 512):
        fs0 = os.path.join(PROF530, f"N{N}", f"cfg526_S0_L{L}.npz")
        if not os.path.exists(fs0): continue
        s0 = np.load(fs0); K0 = json.loads(str(s0["K"]))
        for run, foot in (("LRcan", "canonical"), ("LRalt", "alt")):
            f = os.path.join(PROF530, f"N{N}", f"cfg526_{run}_L{L}.npz")
            if not os.path.exists(f): continue
            d = np.load(f); K = json.loads(str(d["K"])); ok, why = kcheck530(K)
            k = d["kgrav"]; part = stat(k, d["ppart"], float(d["s8"]), s0["kgrav"], s0["ppart"], float(s0["s8"]))
            grav = part if MUT else stat(k, d["pgrav"], float(d["s8g"]), s0["kgrav"], s0["ppart"], float(s0["s8"]))
            cm = r530["runs"].get(f"{run}_L{L}_N{N}", {}); c0 = (abs(part["s8"] - cm.get("s8", np.nan)), abs(part["pdev"] - cm.get("pdev_k1", np.nan)))
            key = f"530_{run}_L{L}_N{N}"
            R530[key] = dict(L=L, N=N, foot=foot, particle=part, gravitating=grav, gates_pass=ok and K0["s0_maxdiff_rel"] <= 1e-4, gates=why,
                             C0=dict(d_s8=c0[0], d_pdev=c0[1], pass_=bool(max(c0) <= 1e-4)), committed=dict(s8=cm.get("s8"), pdev_k1=cm.get("pdev_k1")))
            P(f"  {key:24s} | part s8 {part['s8']:.4f} max|P-1| {part['pdev']:.4f} ({part['verdict']}) | grav s8 {grav['s8']:.4f} max|P-1| {grav['pdev']:.4f} "
              f"k {grav['k_at']:.2f} -> {grav['verdict']} | C0 {c0[0]:.1e}/{c0[1]:.1e} | {'PASS' if R530[key]['gates_pass'] else 'FAIL'} ({why})")
reb = RUN.get("530_LRcan_L200_N256_rebuild")
fr = os.path.join(W, "cfg555_530_LRcan_L200_N256_rebuild.json")
if os.path.exists(fr) and "530_LRcan_L200_N256" in R530:
    d = lj(fr); s0 = lj(os.path.join(EXT, d["s0_base"] + ".json"))["snap"]["z0"]
    gr = stat(d["k"], d["P_part"] if MUT else d["P_grav"], d["s8_part"] if MUT else d["s8_grav"], s0["k"], s0["P"], s0["sigma8"])
    dd = abs(gr["pdev"] - R530["530_LRcan_L200_N256"]["gravitating"]["pdev"]); idok = dd <= 1e-4
    OUT["cfg530_cache_identity"] = dict(rebuild=gr, cache=R530["530_LRcan_L200_N256"]["gravitating"], d_pdev=dd, pass_=idok)
    P(f"  independent rebuild of LRcan L200 N256 here vs the cache: max|P-1| {gr['pdev']:.5f} vs {R530['530_LRcan_L200_N256']['gravitating']['pdev']:.5f} "
      f"(|d| {dd:.1e} <= 1e-4) -> {'PASS' if idok else 'FAIL'}")
OUT["runs"] = RUN; OUT["cfg530"] = R530

# ------------------------------------------------------------------------------------------------ verdicts
P("\nVERDICTS (gravitating field; footings never pooled)")
LV = {}
def lane_verdict(names):
    rows = [(n, RUN[n]) for n in names]
    if any(not r.get("gates_pass") for _, r in rows if r.get("status", "").startswith("EVAL") or "gates_pass" in r) or \
       any(r.get("status", "").startswith("NOT EVALUABLE") for _, r in rows):
        bad = [n for n, r in rows if not r.get("gates_pass")]
        return "NOT EVALUABLE", bad
    fails = [n for n, r in rows if r["gravitating"]["verdict"] != "GROWTH OK"]
    return ("CLAIM FAILS ON GRAVITATING FIELD" if fails else "CLAIM HOLDS ON GRAVITATING FIELD"), fails
for lane, runs in LANE_RUNS.items():
    counted = [n for n, _, c in runs if c and n in RUN]
    v, lst = lane_verdict(counted)
    nums = {n: dict(s8=RUN[n]["gravitating"]["s8"], pdev=RUN[n]["gravitating"]["pdev"], verdict=RUN[n]["gravitating"]["verdict"]) for n in counted if "gravitating" in RUN[n]}
    others = {n: dict(s8=RUN[n]["gravitating"]["s8"], pdev=RUN[n]["gravitating"]["pdev"], verdict=RUN[n]["gravitating"]["verdict"])
              for n, _, c in runs if not c and "gravitating" in RUN.get(n, {})}
    LV[lane] = dict(verdict=v, failing_or_unevaluable=lst, counted_runs=nums, controls_reported=others)
    P(f"  {lane}: {v}" + (f"  ({', '.join(f'{n} s8 {nums[n]['s8']:.4f} max|P-1| {nums[n]['pdev']:.3f}' for n in lst if n in nums)})" if lst else "")
      + ("" if not others else "  | controls on grav: " + "; ".join(f"{n} {o['s8']:.4f}/{o['pdev']:.3f} {o['verdict']}" for n, o in others.items())))
# CFG530: its own claim was GROWTH OK only at 256^3 (CFG527's), already NOT CONFIRMED at 512^3 on particles
g530 = {f: [k for k, r in R530.items() if r["foot"] == f and r["L"] == 200] for f in ("canonical", "alt")}
v530 = {f: {k: (round(R530[k]["gravitating"]["s8"], 4), round(R530[k]["gravitating"]["pdev"], 3), R530[k]["gravitating"]["verdict"]) for k in ks} for f, ks in g530.items()}
allok530 = all(r["gates_pass"] for r in R530.values())
LV["CFG530"] = dict(verdict=("NOT EVALUABLE" if not allok530 else "CLAIM FAILS ON GRAVITATING FIELD" if any(R530[k]["gravitating"]["verdict"] != "GROWTH OK" for k in R530 if R530[k]["L"] == 200)
                             else "CLAIM HOLDS ON GRAVITATING FIELD"), L200=v530)
P(f"  CFG530 (L200, every N): {LV['CFG530']['verdict']}  " + json.dumps(v530))
pv, plst = lane_verdict(PAPER45)
worst = max(PAPER45, key=lambda n: RUN[n]["gravitating"]["pdev"] if "gravitating" in RUN[n] else -1)
P45 = dict(verdict=pv, failing_or_unevaluable=plst, n_runs=len(PAPER45), n_growth_ok=sum(RUN[n].get("gravitating", {}).get("verdict") == "GROWTH OK" for n in PAPER45),
           worst=dict(run=worst, **{k: RUN[worst]["gravitating"][k] for k in ("s8", "pdev", "k_at")}) if "gravitating" in RUN[worst] else None,
           range_256=dict(pdev=[min(RUN[n]["gravitating"]["pdev"] for n in PAPER45 if RUN[n].get("N") == 256), max(RUN[n]["gravitating"]["pdev"] for n in PAPER45 if RUN[n].get("N") == 256)],
                          s8=[min(RUN[n]["gravitating"]["s8"] for n in PAPER45 if RUN[n].get("N") == 256), max(RUN[n]["gravitating"]["s8"] for n in PAPER45 if RUN[n].get("N") == 256)]),
           at_512={n: dict(s8=RUN[n]["gravitating"]["s8"], pdev=RUN[n]["gravitating"]["pdev"]) for n in PAPER45 if RUN[n].get("N") == 512 and "gravitating" in RUN[n]},
           mutate_row=dict(s8=RUN["424_MUTATE_nocomp"]["gravitating"]["s8"], pdev=RUN["424_MUTATE_nocomp"]["gravitating"]["pdev"]))
P(f"\n  PAPER45 v2.0/v2.1 (15 rule runs): {pv}; GROWTH OK on the gravitating field in {P45['n_growth_ok']}/15; worst {worst} "
  f"s8 {P45['worst']['s8']:.4f} max|P-1| {P45['worst']['pdev']:.3f} (k {P45['worst']['k_at']:.2f})")
P(f"    256^3 range: s8 {P45['range_256']['s8'][0]:.4f}-{P45['range_256']['s8'][1]:.4f}, max|P-1| {P45['range_256']['pdev'][0]:.3f}-{P45['range_256']['pdev'][1]:.3f}; "
  "512^3: " + "; ".join(f"{n} {v['s8']:.4f}/{v['pdev']:.3f}" for n, v in P45["at_512"].items()))
P(f"    MUTATE row (no compensation) on grav: s8 {P45['mutate_row']['s8']:.4f} max|P-1| {P45['mutate_row']['pdev']:.3f}")
OUT["lane_verdicts"] = LV; OUT["PAPER45"] = P45
c0all = all(r["C0"]["pass_"] for r in RUN.values() if "C0" in r) and all(r["C0"]["pass_"] for r in R530.values())
OUT["C0_all_pass"] = c0all
P(f"\nC0 (source off reproduces every lane's committed particle numbers to <= 1e-4): {'PASS' if c0all else 'FAIL'}")
P("\nkappa = 1/2 FITTED; footings never pooled; cold energy MASS still required; not theory closed.")
sfx = "_MUTATE" if MUT else ""
open(os.path.join(HERE, f"cfg555_analysis{sfx}.out"), "w").write("\n".join(LINES) + "\n")
json.dump(OUT, open(os.path.join(HERE, f"cfg555_results{sfx}.json"), "w"), indent=1)
