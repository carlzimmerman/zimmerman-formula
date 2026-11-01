#!/usr/bin/env python3
"""FG1 (FROZEN_CRITERIA.md, 3b2fae101a): the 11-line by 4-candidate scorecard. Reads only; writes fg1.out, fg1_results.json (MUTATE twin:
fg1_MUTATE.out, fg1_results_MUTATE.json, reads the law tail with nu = 1, K3 must fail, exit 1).
Run: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I fg1_read.py     FG1_MUTATE=1 for the twin.
kappa = 1/2 FITTED; T LOCATED, not derived; cold dark energy, never a particle; not theory closed; nothing here says the data favour the framework."""
import json, os, re, sys

H = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(H)
MUT = os.environ.get("FG1_MUTATE") == "1"; SFX = "_MUTATE" if MUT else ""
OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)
def J(*p): return json.load(open(os.path.join(RB, *p)))
def T(*p): return open(os.path.join(RB, *p)).read()
FG = "FG1_final_grade"; FEET = ("canonical", "alt"); BG = ("A_c2b_refit", "B_cfg886_bg"); checks = []
def chk(k, ok, msg): checks.append((k, bool(ok))); P(f"{k} {msg}: {'PASS' if ok else 'FAIL'}")
def sline(u, rms): return 0.50 <= u <= 0.80 and rms <= 0.110

if not os.path.exists(os.path.join(H, "fg1_harness_results.json")) :
    print("FG1 harness not finished: no table"); sys.exit(2)
HR = J(FG, "fg1_harness_results.json"); C3, C4 = HR["C3"], HR["C4"]
NR3 = J("NR3_ur1_on_nr2", "nr3_MEDIAN_results.json")["runs"]; E0, EB = NR3["EM1|off"], NR3["EM1|blum"]
ZN = J("ZN4_cluster_resolution", "zn4_results.json")["runs"]; Z005 = ZN["f* 0.034, gas +0.005"]; Z005b = ZN["f* 0.0615, gas +0.005"]; Z111 = ZN["f* 0.034, X-COP's gas"]; Z111b = ZN["f* 0.0615, X-COP's gas"]
TL = J(FG, f"fg1law_{'MUTATE' if MUT else 'RUN'}_results.json")
DM = J("UR3_direct_weighing", "ur3_diskmass.json"); MW = J("UR3_direct_weighing", "ur3_mw.json")["rows"]
FCK = J("FC1_cold_share_native_eta", "x79_rule", "x79_kids_grade_native.json")["footings"]
ND = J("ND1_native_dwarfs", "nd1_ceiling_results.json")["grades"]["native free M200 (PRIMARY)"]["cls"]
BS = J("BS1_basin_switch", "bs1_basin_switch_results.json")["primary"]; RF2 = J("RF2_ic1613_inclination_footing", "rf2_ic1613_results.json")["verdict"]

def keys(z):
    bad = sorted({k for h in z["cells"] for k, c in z["cells"][h].items() if abs(c["Z"]) > 2}); w = max(((abs(c["Z"]), k, h, c["Z"]) for h in z["cells"] for k, c in z["cells"][h].items()))
    return dict(n=15 - len(bad), bad=bad, worst=w[1], worst_h=w[2], worst_Z=w[3])
K005, K005b, K111, K111b = keys(Z005), keys(Z005b), keys(Z111), keys(Z111b)
XPASS = lambda x: abs(x["mean"]) <= 0.05 and x["rms"] <= 0.10
def cell(status, val, tag, note=""): return dict(status=status, value=val, tag=tag, note=note)
PASS, FAIL, NG = "PASS", "FAIL", "NOT GRADED"
RT = {}

# --- C1: NR2 MEDIAN + EM1, clusters ZN4 at GS4's +0.005
def sp(r): s = r["sparc"]; return s[BG[0]], s[BG[1]]
a, b = sp(E0); ku = keys(Z005)
c1 = dict(
 S=cell(PASS if a["line"] and b["line"] else FAIL, f"U {a['U']:.2f}/{b['U']:.2f}, rms {a['rms']:.4f}/{b['rms']:.4f}", "[NR2]", "no a0, footings coincide"),
 Tl=cell(PASS if abs(a["tilt"]) <= .15 and abs(b["tilt"]) <= .15 else FAIL, f"{a['tilt']:+.2f}/{b['tilt']:+.2f}", "[NR2]"),
 LT=cell(PASS if all(abs(E0["lt"][t]) <= .10 for t in BG) else FAIL, f"{E0['lt'][BG[0]]:+.3f}/{E0['lt'][BG[1]]:+.3f}", "[NR2]"),
 G=cell(PASS if E0["groups"]["verdict"] == "CONSISTENT" else FAIL, f"Z {E0['groups']['Z']:+.2f}", "[NR2]"),
 K=cell(PASS if K005["n"] == 15 else FAIL, f"{K005['n']} of 15, over 2: {', '.join(K005['bad'])}; worst {K005['worst']} {K005['worst_Z']:+.2f}", "[READ ZN4]", f"f* 0.0615: {K005b['n']} of 15, {K005b['worst']} {K005b['worst_Z']:+.2f}"),
 X=cell(PASS if XPASS(Z005["xcop"]) else FAIL, f"mean {Z005['xcop']['mean']:+.3f}, rms {Z005['xcop']['rms']:.3f}", "[READ ZN4]", f"N's smooth core on the NR3 path reads {E0['xcop']['mean']:+.3f}, {E0['xcop']['rms']:.3f}: a different profile, not this cell"),
 Ln=cell(FAIL if FCK["canonical"]["verdict"] == "LAW" else PASS, f"class {FCK['canonical']['verdict']}, dchi2(H2H-L2H) {FCK['canonical']['all']['dchi2']:+.1f}, alt {FCK['alt']['all']['dchi2']:+.1f}", "[READ FC1]", "not on NR2"),
 Dw=cell(PASS if all(abs(v["Z"]) < 2 for v in ND.values()) else FAIL, "; ".join(f"{k} {v['Z']:+.2f}" for k, v in ND.items()), "[READ ND1]", "ND1's primary core row, free M200, z_f"),
 MW=cell(FAIL, f"{MW['A_c2b_refit|d0|off']['cls']}, {MW['A_c2b_refit|d0|off']['n_all']} cell", "[READ UR3]", "UR3's table is NR1 PRIMARY, not NR2. Wide priors only isn't a pass"),
 DM=cell(PASS if .9 <= DM["1.5 hR|off"]["r"] <= 1.1 else FAIL, f"r {DM['1.5 hR|off']['r']:.3f}, Upsilon_K {DM['1.5 hR|off']['Y']:.3f}, target 0.90-1.10", "[READ UR3]"),
 IC=cell(FAIL, "E -0.474 (Z -6.3)", "[READ ND1]", "RF2: disfavoured, not excluded; depends on inclination"))
# --- C2: NR3 MEDIAN EM1|blum
a, b = sp(EB); kb = EB["keys"]; wb = max(((abs(z), k, h, z) for h, zz in kb["Z"].items() for k, z in zz.items()))
c2 = dict(
 S=cell(PASS if a["line"] and b["line"] else FAIL, f"U {a['U']:.2f}/{b['U']:.2f}, rms {a['rms']:.4f}/{b['rms']:.4f}", "[NR2]", "rms clears; Upsilon doesn't"),
 Tl=cell(PASS if abs(a["tilt"]) <= .15 and abs(b["tilt"]) <= .15 else FAIL, f"{a['tilt']:+.2f}/{b['tilt']:+.2f}", "[NR2]"),
 LT=cell(PASS if all(abs(EB["lt"][t]) <= .10 for t in BG) else FAIL, f"{EB['lt'][BG[0]]:+.3f}/{EB['lt'][BG[1]]:+.3f}", "[NR2]"),
 G=cell(PASS if EB["groups"]["verdict"] == "CONSISTENT" else FAIL, f"Z {EB['groups']['Z']:+.2f}", "[NR2]"),
 K=cell(PASS if kb["n"] == 15 else FAIL, f"{kb['n']} of 15, over 2: {', '.join(kb['bad'])}; worst {wb[1]} {wb[3]:+.2f}; G-OUT-M3 {kb['Z']['h0672']['G-OUT-M3']:+.2f}", "[NR2]", "NR3's row: smooth core + response on eRASS1's gas, one template. ZN4's shape with a response not computed on record"),
 X=cell(PASS if XPASS(EB["xcop"]) else FAIL, f"mean {EB['xcop']['mean']:+.3f}, rms {EB['xcop']['rms']:.3f}", "[NR2]", "NR3's row and the same line; ZN4's own profile with a response isn't on record"),
 Ln=cell(FAIL if FCK["canonical"]["verdict"] == "LAW" else PASS, f"class {FCK['canonical']['verdict']}, dchi2(H2H-L2H) {FCK['canonical']['all']['dchi2']:+.1f}, alt {FCK['alt']['all']['dchi2']:+.1f}", "[READ FC1]", "not on NR2, no response in FC1"),
 Dw=cell(NG, "no lane has it", "[no lane on record]"),
 MW=cell(FAIL, f"{MW['A_c2b_refit|d0|blum']['cls']}, {MW['A_c2b_refit|d0|blum']['n_all']} cells", "[READ UR3]", f"Gnedin, the alternate: {MW['A_c2b_refit|d0|gnedin']['cls']}. UR3's table is NR1 PRIMARY. Its stress test: this weighs inner cold mass, not the response"),
 DM=cell(PASS if .9 <= DM["1.5 hR|blum"]["r"] <= 1.1 else FAIL, f"r {DM['1.5 hR|blum']['r']:.3f}, Upsilon_K {DM['1.5 hR|blum']['Y']:.3f}, n {DM['1.5 hR|blum']['n']}", "[READ UR3]", "Fragile: CFG577's Jeans integral raises r 5-7 %, to about 1.13, outside; Upsilon_K 0.287 is below SPARC's line"),
 IC=cell(NG, "no lane has it", "[no lane on record]"))
# --- C3, C4 harness rows
def hS(g): s = g["sparc"]; return s[BG[0]], s[BG[1]]
def hcell_S(R, f, tag, note=""): a, b = hS(R[f]); return cell(PASS if a["line"] and b["line"] else FAIL, f"U {a['U']:.2f}/{b['U']:.2f}, rms {a['rms']:.4f}/{b['rms']:.4f}", tag, note)
def hcell_G(R, f, tag, note=""): g = R[f]["groups"]; return cell(PASS if g["verdict"] == "CONSISTENT" else FAIL, f"Z {g['Z']:+.2f}", tag, note)
def hcell_Ln(R, f, tag, note=""):
    l = R[f]["lensing"]; return cell(PASS if l["d_LF_L"] <= 9 and l["d_LF_H"] < 0 else FAIL, f"ENV2H-L2H {l['d_LF_L']:+.1f}, ENV2H-H2H {l['d_LF_H']:+.1f}", tag, note)
def hcell_Dw(R, f, tag, note=""): d = R[f]["dwarfs"]; return cell(PASS if all(abs(v["Z"]) < 2 for v in d.values()) else FAIL, "; ".join(f"{k} {v['Z']:+.2f}" for k, v in d.items()), tag, note)
def lawT(f): return TL[f]
def tl_cell(f, tag, note=""):
    a, b = lawT(f)[BG[0]], lawT(f)[BG[1]]; return cell(PASS if abs(a["tilt"]) <= .15 and abs(b["tilt"]) <= .15 else FAIL, f"{a['tilt']:+.2f}/{b['tilt']:+.2f}", tag, note)
def lt_cell(f, tag, note=""):
    a, b = lawT(f)[BG[0]], lawT(f)[BG[1]]; return cell(PASS if abs(a["lt"]) <= .10 and abs(b["lt"]) <= .10 else FAIL, f"{a['lt']:+.3f}/{b['lt']:+.3f}", tag, note)
HN = "LEE1 harness at L 7.082 (NR2's 10^14), S9 shape, X43's floor kept: disclosed departure"
APX = "law on all systems; ignores the 9 of 175 SPARC galaxies above T (5.1 %)"
def build_c3(f):
    return dict(S=hcell_S(C3, f, "[NR2]", HN), Tl=tl_cell(f, "[NR2]", APX), LT=lt_cell(f, "[NR2]", APX), G=hcell_G(C3, f, "[NR2]", HN),
      K=cell(FAIL, f"{K005['n']} of 15, over 2: {', '.join(K005['bad'])}; worst {K005['worst']} {K005['worst_Z']:+.2f}", "[READ ZN4]", "the harness's own cluster row isn't this cell"),
      X=cell(PASS if XPASS(Z005["xcop"]) else FAIL, f"mean {Z005['xcop']['mean']:+.3f}, rms {Z005['xcop']['rms']:.3f}", "[READ ZN4]"),
      Ln=hcell_Ln(C3, f, "[NR2]", HN), Dw=hcell_Dw(C3, f, "[NR2]", "satellites on route E, flag independent of T and L"),
      MW=cell(FAIL, f"{BS['mw'][f]['cls']}, {BS['mw'][f]['n_L1_L2a_L2b']} cells on 3 lines, 3 on all four", "[READ BS1, its own L 4.0]", "Wide priors only isn't a pass; R_d 1.93 short disc"),
      DM=cell(NG, "r 1.250 (alt 1.212) CFG576, 1.342 CFG577; neither in 0.90-1.10", "[READ CFG576/577, numbers only]", "those lanes' own gates failed, frozen INCONCLUSIVE, so no verdict is read from them; the round rule is the law on these discs"),
      IC=cell(FAIL, f"E {BS['dwarfs'][f]['flags']['IC 1613']['E']:+.3f} (Z {BS['dwarfs'][f]['flags']['IC 1613']['Z']:+.2f})", "[READ BS1, its own L 4.0]", "RF2's class: " + RF2[f]))
def build_c4(f):
    k = C4[f]["clusters"]; bad = [n for n, c in k.items() if not c["ok"]]; w = max(((abs(c["Z"]), n, c["Z"]) for n, c in k.items()))
    return dict(S=hcell_S(C4, f, "[NR2]", "LEE1 harness, mode law"), Tl=tl_cell(f, "[NR2]"), LT=lt_cell(f, "[NR2]"), G=hcell_G(C4, f, "[NR2]", "LEE1 harness, mode law; no eta"),
      K=cell(PASS if not bad else FAIL, f"{15 - len(bad)} of 15, over 2 in either h: {', '.join(bad)}; worst at h 0.672 {w[1]} {w[2]:+.2f}", "[NR2]", "harness template: f* 0.20, no gas tail, older than the measured chain of C1-C3"),
      X=cell(NG, "the harness doesn't carry X-COP. CS2's law on record: -0.151, 0.205", "[READ HO1, numbers only]"),
      Ln=hcell_Ln(C4, f, "[NR2]", "L2H and ENV2H coincide in law mode, so the first number is zero by construction"), Dw=hcell_Dw(C4, f, "[NR2]", "plain nu(g_N), no external-field term in X51's path"),
      MW=cell(FAIL, "FEASIBLE (wide priors only), 7 of 175 cells (alt 4); passing cells K_z +4.7 to +6.6 sigma against Bovy & Rix", "[READ X5, not RF1]", "SOURCE SWAP, disclosed: the criteria name RF1, which has no row for the law (only OS1 and native N); X5 is v3's AQUAL. Wide priors only isn't a pass"),
      DM=cell(NG, "r 1.250 (alt 1.212) CFG576, 1.342 CFG577; neither in 0.90-1.10", "[READ CFG576/577, numbers only]", "those lanes' own gates failed, frozen INCONCLUSIVE, so no verdict is read from them"),
      IC=cell(FAIL, "E -0.593 (Z -7.9); RF2's class: " + RF2[f], "[READ ND1, RF2]", "disfavoured, not excluded"))
TABLE = dict(C1=c1, C2=c2, C3=dict(canonical=build_c3("canonical"), alt=build_c3("alt")), C4=dict(canonical=build_c4("canonical"), alt=build_c4("alt")))
LINES = ("S", "Tl", "LT", "G", "K", "X", "Ln", "Dw", "MW", "DM", "IC")

P("FG1_final_grade: scorecard, frozen criteria 3b2fae101a. kappa = 1/2 FITTED; T LOCATED; footings never pooled; not theory closed")
P("\n=== Checks")
# K1: C1, C2 cells against NR3's committed summary and README row, and the line recomputed
d = 0.0
for r in (E0, EB):
    for t in BG: d = max(d, abs(float(r["sparc"][t]["line"]) - float(sline(r["sparc"][t]["U"], r["sparc"][t]["rms"]))))
rd = T("NR3_ur1_on_nr2", "README.md"); lit = ["0.75/0.76", "0.0690", "+0.59", "+1.47", "+0.153", "0.35/0.36", "0.0670", "+0.17", "+1.50", "+0.116", "−0.097, 0.146"]; miss = [x for x in lit if x not in rd]
chk("K1", d <= 1e-6 and not miss, f"C1, C2 read straight from NR3 MEDIAN; line recomputed |d| {d:.0e}; README row literals missing {miss}")
# K2
dl = max(abs(C4[f]["sparc"][BG[0]]["rms"] - r) for f, r in (("canonical", 0.0541), ("alt", 0.0537)))
chk("K2", HR["k0"] and dl <= 1e-3, f"LEE1 Step-0 K0a, K0b, K0c, K2a, K2b pass; law rms within {dl:.1e} of EM1 LAW 0.0541 / 0.0537")
# K3
d3 = max(abs(TL[f][t]["U"] - HR["C4_U"][f][t]) for f in FEET for t in BG)
chk("K3", d3 <= 0.02, f"law tail's median Upsilon against the harness's law, max |d| {d3:.3f} (line 0.02)")
# K4: literals of READ cells in their own sources
LITS = [("ND1_native_dwarfs/nd1_ab.out", "IC 1613 -0.474 (-6.3"), ("X5_mw_joint_baryons/README.md", "7 of 175 cells"), ("X5_mw_joint_baryons/README.md", "+4.7 to +6.6σ"), ("HO1_xcop_hotgas_heldout/README.md", "CS2 law −0.151 / 0.205"),
        ("ND1_native_dwarfs/README.md", "−0.593 (−7.9)"), ("../campaign_fresh_gravity/CFG576_diskmass_sigz/README.md", "1.250 [1.205, 1.291]"), ("../campaign_fresh_gravity/CFG576_diskmass_sigz/README.md", "1.212 [1.167, 1.265]"),
        ("../campaign_fresh_gravity/CFG577_diskmass_grid/README.md", "1.342 [1.272, 1.377]"), ("BS1_basin_switch/README.md", "| cells passing L1 + L2a + L2b | **13** | 13 |"), ("BS1_basin_switch/README.md", "| cells passing all four | 3 "), ("UR3_direct_weighing/README.md", "CFG577's Jeans integral raises r 5–7 %"), ("LEE1_look_elsewhere/README.md", "MW ultra-faints Z +5.22")]
miss4 = [l for p, l in LITS if l not in T(*p.split("/"))]
jsonk = [BS["dwarfs"]["canonical"]["flags"]["IC 1613"]["Z"], FCK["canonical"]["all"]["dchi2"], DM["1.5 hR|off"]["r"], DM["1.5 hR|blum"]["r"], Z005["xcop"]["mean"]]
chk("K4", not miss4 and all(isinstance(x, float) for x in jsonk), f"{len(LITS)} literals and {len(jsonk)} JSON keys in their source files; missing {miss4}")
# K0 diagnosis, restated by machine
ofo, lao, ono = (T(FG, n) for n in ("x62_x43copy_off_a2.out", "x62_x43copy_law_a2.out", "x62_x43copy_on_shpS9_L7.082_T12.3_B.out"))
ofj, laj, onj = (J(FG, n)["checks"] for n in ("x62_x43copy_off_a2_results.json", "x62_x43copy_law_a2_results.json", "x62_x43copy_on_shpS9_L7.082_T12.3_B_results.json"))
nz = T("NZ1_zoom_core_radius", "nz1_one_template.out")
src = T("X43_collapse_core_floor", "x43_collapse_core.py")
dg = dict(
  off_passes_both=ofj["K0"] and ofj["K0x38"] and "SPARC 0.0795 (0.0795), OUTER 0.697 (0.697): PASS" in ofo,
  law_k0x38_is_law="SPARC 0.0541 (0.0795), OUTER 0.999 (0.697): FAIL" in lao and laj["K0"] and not laj["K0x38"],
  on_k0x38_is_law="SPARC 0.0541 (0.0795), OUTER 0.999 (0.697): FAIL" in ono and not onj["K0x38"],
  flag_false_code="if not rule: return s, False" in src,
  on_x30_is_tail="X30 OUTER / MID 0.7801 / 1.6387: FAIL" in ono and "f* 0.20, tail to r_ta" in nz and "KT_all 0.7801" in nz,
  other_checks_pass=all(onj[k] for k in onj if k not in ("K0", "K0x38")) and all(laj[k] for k in laj if k != "K0x38"))
chk("K0-diagnosis", all(dg.values()), "X43's K0x38 is the law branch in harness mode, K0's X30 half is GS1's tail: " + ", ".join(f"{k} {v}" for k, v in dg.items()))
allok = all(ok for _, ok in checks)
if not allok:
    P("\nA CHECK FAILED: NO VERDICT"); RT["verdict"] = "NO VERDICT, check failed"
    open(os.path.join(H, f"fg1{SFX}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(dict(checks=dict(checks), verdict=RT["verdict"]), open(os.path.join(H, f"fg1_results{SFX}.json"), "w"), indent=1, sort_keys=True); sys.exit(1)

P("\n=== Table, canonical primary. C1, C2 have no a0: footings coincide")
def rows(lab, tb):
    P(f"\n--- {lab}")
    for l in LINES: c = tb[l]; P(f"  {l:3s} {c['status']:10s} {c['value']}  {c['tag']}" + (f"  | {c['note']}" if c["note"] else ""))
rows("C1 native N, no response", c1); rows("C2 N + Blumenthal response", c2); rows("C3 basin split, canonical", TABLE["C3"]["canonical"]); rows("C3 basin split, alt (reported, not pooled)", TABLE["C3"]["alt"]); rows("C4 the law alone, canonical", TABLE["C4"]["canonical"]); rows("C4 the law alone, alt (reported, not pooled)", TABLE["C4"]["alt"])
def verdict(tb):
    f = [l for l in LINES if tb[l]["status"] == FAIL]; n = [l for l in LINES if tb[l]["status"] == NG]
    return dict(verdict="FAILS" if f else "PASSES EVERY GRADED LINE", failed=f, not_graded=n)
V = dict(C1=verdict(c1), C2=verdict(c2), C3=verdict(TABLE["C3"]["canonical"]), C4=verdict(TABLE["C4"]["canonical"]), C3_alt=verdict(TABLE["C3"]["alt"]), C4_alt=verdict(TABLE["C4"]["alt"]))
P("\n=== Verdict per candidate")
for k in V: P(f"  {k}: {V[k]['verdict']}; failed {V[k]['failed']}; NOT GRADED {V[k]['not_graded']}")
surv = V["C1"]["verdict"] != "FAILS" or V["C2"]["verdict"] != "FAILS"
gc = K111["n"] == 15 and K111b["n"] == 15
ov = "ROUTE E SURVIVES" if surv else "ROUTE E DOES NOT SURVIVE ON MEASURED DATA"
P(f"\nOVERALL: {ov}" + (" [GAS-CONDITIONAL]" if gc else ""))
P(f"  Tag: K at +0.111 is 15 of 15 on ZN4 (G-OUT-M3 worst {K111['worst_Z']:+.2f}, f* 0.0615 {K111b['worst_Z']:+.2f}), so C1's and C3's K failure disappears. It rescues K only: C1 still fails {[l for l in V['C1']['failed'] if l != 'K']}, C3 {[l for l in V['C3']['failed'] if l != 'K']}. The verdict stays on GS4's +0.005.")
P("  No candidate is declared best by counting lines; the lines are not independent.")
RT.update(checks=dict(checks), k0_diagnosis=dg, table=TABLE, verdicts=V, overall=ov, gas_conditional=gc, keys=dict(k005=K005, k005_fs0615=K005b, k111=K111, k111_fs0615=K111b))
P("\nkappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.")
open(os.path.join(H, f"fg1{SFX}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RT, open(os.path.join(H, f"fg1_results{SFX}.json"), "w"), indent=1, sort_keys=True, default=float); sys.exit(0)
