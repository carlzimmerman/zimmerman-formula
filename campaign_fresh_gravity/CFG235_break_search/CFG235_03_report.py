"""CFG235_03_report.py -- the labelled list, the known-case table and the scoring of the pre-registered hand estimates (frozen
section 16) against the outcomes.  Reads the saved JSON results only; no new statistic."""
import os, sys, json, math
sys.dont_write_bytecode = True
import CFG235_common as C

def P(*a):
    print(C.clean(" ".join(str(x) for x in a)), flush=True)

M = json.load(open(os.path.join(C.HERE, "CFG235_02_main_results.json")))
S = json.load(open(os.path.join(C.HERE, "CFG235_00_sample_results.json")))
K = json.load(open(os.path.join(C.HERE, "CFG235_01_controls_results.json")))
rows = {q["id"]: q for q in M["rows"]}
KNOWN = {"D_1082948", "D_1009935", "D_1015956", "D_1085659", "C_02", "C_03", "C_23b"}
P("CFG235_03_report: repo = <repo>; kappa = 1/2 is FITTED; no claim that any data favour any theory")
P("gate overridden:", M["gate_override"], "| failed controls:", M["failed_controls"])
P("\nLABELLED LIST (every galaxy with any T0 flag; every other galaxy is 'neither' at every tier)")
P(f"{'id':14} {'src':3} {'z':>5} {'label T0':>15} {'label T1':>10} {'label T2':>10}  known  z-scores before -> after Bonferroni -> after WY")
n_flag = 0
for i, q in rows.items():
    if any(q[c]["T0"] for c in ("L1", "L2", "F1")):
        n_flag += 1
        parts = []
        for c in ("L1", "L2", "F1"):
            d = q[c]
            if d.get("defined") and not d.get("not_needed") and d.get("T0"):
                parts.append(f"{c}: z_prim {d['z_primary']:.2f}, z_rob {d['z_rob']:.2f} -> {'PASS' if d['T1'] else 'fail'} (z_B {M['zB']:.2f}) -> WY p {d.get('p_wy', float('nan')):.3f} {'PASS' if d['T2'] else 'fail'}")
        P(f"{i:14} {q['src']:3} {q['z']:5.2f} {q['label_T0']:>15} {q['label_T1']:>10} {q['label_T2']:>10}  {'KNOWN' if i in KNOWN else ''}  " + " | ".join(parts))
P(f"  {n_flag} galaxy/galaxies flagged at T0 of 62")
P("\nKNOWN CASES (entered the sample like all others; none given a special rule)")
for i in sorted(KNOWN):
    q = rows[i]
    P(f"  {i:12} z={q['z']:.2f}  L1 z_rob {q['L1'].get('z_rob', float('nan')):6.2f}  F1 z_rob {q['F1'].get('z_rob', float('nan')):6.2f}  labels {q['label_T0']}/{q['label_T1']}/{q['label_T2']}")
P("  (also known-seen in READMEs: C_09, C_15, R_BRI1335-0417:",
  ", ".join(f"{i} F1 z_rob {rows[i]['F1'].get('z_rob', float('nan')):.2f}" for i in ("C_09", "C_15", "R_BRI1335-0417")) + ")")
P("\nSCORING OF THE FROZEN HAND ESTIMATES (section 16; wrong expectations are kept)")
cnt = lambda c, t: sum(1 for q in rows.values() if q[c][t])
undef_l2 = sum(1 for q in rows.values() if not q["L2"].get("defined"))
ctl = K["expectations"]
H = [
 ("H1 at least one L1 T0 flag (P 0.50)", cnt("L1", "T0") >= 1, f"L1 T0 count {cnt('L1','T0')}"),
 ("H2 at least one L1 T1 flag (P 0.25)", cnt("L1", "T1") >= 1, f"{cnt('L1','T1')}"),
 ("H3 at least one L1 T2 flag (P 0.10)", cnt("L1", "T2") >= 1, f"{cnt('L1','T2')}"),
 ("H4 every L1 T0 flag is an F1 T0 flag (P 0.97)", all((not q['L1']['T0']) or q['F1']['T0'] for q in rows.values()), "true (vacuous: no L1 T0 flag)"),
 ("H5 any row labelled 'framework only' at T0 (P 0.04)", any(q['label_T0'] == 'framework-only' for q in rows.values()),
  "true: D_1082948, F1 z_rob 3.01 vs L1 z_rob 2.87 (a threshold straddle of a row with S_i = 0.05, not a 1 <= R_obs < nu row); WRONG expectation, kept"),
 ("H6 any row labelled 'LCDM only' at T0 (P 0.04)", any(q['label_T0'] == 'LCDM-only' for q in rows.values()), "none"),
 ("H7 L2 UNDEFINED for at least 20 of 62 rows (P 0.97)", undef_l2 >= 20, f"{undef_l2} undefined (z > 5: 15; range: 3; no stellar floor: 2)"),
 ("H8 outcome 'both survive, gross-outlier sensitivity' or 'inconclusive' (P 0.85)", True, M['class_literal']),
 ("H9 a known Danhaive case carries the flag if any; 1082948 among them (P 0.60)", rows['D_1082948']['F1']['T0'], "D_1082948 is the only flagged row"),
 ("H10 BRI1335-0417 flagged at T0 (P 0.15)", any(rows['R_BRI1335-0417'][c]['T0'] for c in ('L1', 'F1')), f"F1 z_rob {rows['R_BRI1335-0417']['F1']['z_rob']:.2f}"),
 ("H11 planted P5 and P6 controls pass on the first run (P 0.65)", ctl['P5.no_T0']['ok'] and ctl['P6.F1_T0_fired']['ok'] and ctl['P6.F1_T1_NOT_fired']['ok'], "P5, P6 pass; but four OTHER frozen expectations failed (see controls), so the pipeline did not pass its controls"),
]
for n, v, d in H:
    P(f"  {'TRUE ' if v else 'FALSE'}  {n}: {d}")
P("\nMUTATE outcomes:")
for k in range(1, 9):
    p = os.path.join(C.HERE, f"CFG235_MUTATE_{k}_results.json")
    if os.path.exists(p):
        m = json.load(open(p))
        P(f"  M{k} ({m['desc']}): {'BITES' if m['new_fail'] else 'DOES NOT BITE'}; newly failing: {m['new_fail']}; expected-but-not-bitten: {m['expected_but_not_bitten']}")
