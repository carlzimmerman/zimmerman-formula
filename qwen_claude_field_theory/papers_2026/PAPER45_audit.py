"""PAPER45 audit: numbers in the .tex against committed outputs."""
import json, os, sys, math
H = os.path.dirname(os.path.abspath(__file__)); C = os.path.join(H, "..", "..", "campaign_fresh_gravity"); D = os.path.join(H, "..", "..", "deepseek_push", "openai_math_cross_analysis_2026-10")
tex = open(os.path.join(H, "PAPER45_supply_edge_note_2026.tex")).read(); j = lambda p: json.load(open(os.path.join(C, p))); rows = []
def row(n, ok): rows.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
r = j("CFG361_pm_growth_T5_bookkeeping/cfg361_pm_growth_T5_results.json")["numbers"]["ratios"]
row("T5 1.2049 / 1.2573", round(r["T5_FLAT_canonical_N256"]["z0"]["sig8"], 4) == 1.2049 and round(r["T5_FLAT_alt_N256"]["z0"]["sig8"], 4) == 1.2573 and "1.2049 / 1.2573" in tex)
b = j("CFG410_filament_share_of_excess/cfg410_results.json")
row("BASE 1.0193/1.0243, 0.153/0.193", (round(b["canonical"]["BASE"]["s8"], 4), round(b["alt"]["BASE"]["s8"], 4), round(b["canonical"]["BASE"]["pdev"], 3), round(b["alt"]["BASE"]["pdev"], 3)) == (1.0193, 1.0243, 0.153, 0.193) and "1.0193 / 1.0243 & 0.153 / 0.193" in tex and "+15.3\\%$/$+19.3\\%" in tex)
h = j("CFG411_overnight_convergence/cfg411_results.json")["b"]
row("512 1.0226 / 0.174 (+17.4%)", round(h["hi"]["s8"], 4) == 1.0226 and round(h["hi"]["pdev"], 3) == 0.174 and "1.0226 & 0.174" in tex and "+17.4\\%" in tex)
d = j("CFG412_filament_blind_switch/cfg412_diag_results.json")
row("0.805 inside host spheres (~81%)", round(d["canonical_D2"]["covered_by_resolved_host(>=2 cells)"], 3) == 0.805 and "0.805" in tex and "81\\%" in tex)
row("KiDS-safe removal 13-19% (CFG412 README)", "13–19%" in open(os.path.join(C, "CFG412_filament_blind_switch", "README.md")).read() or "13-19" in open(os.path.join(C, "CFG412_filament_blind_switch", "README.md")).read())
q = j("CFG418_lensing_cold_ratio/cfg418_rc.json")
row("x_best 0.48 / 0.53", round(q["canonical"]["x_best"], 2) == 0.48 and round(q["alt"]["x_best"], 2) == 0.53 and "$x=0.48$" in tex and "$0.53$" in tex)
g = j("CFG413_on_radius_kids_vs_growth/cfg413_growth_results.json")
row("S(0.4) 0.83", round(g["canonical"]["rows"]["2.0"]["0.4"]["S"], 2) == 0.83 and "0.83 of the excess" in tex)
p = j("CFG415_shared_catchments_and_sqrtMb/precheck_supply_edge_hosts.json")
xs = [v["x_median"] for f in p for v in p[f].values()]
row("resolved-host x_edge 0.24-0.33", round(min(xs), 2) == 0.24 and round(max(xs), 2) == 0.33 and "0.24$--$0.33" in tex)
row("5.850 r_t exact (f_ret = 1)", abs(1 / math.log(1 + 1 / 5.364) - 5.850) < 5e-4 and "5.850" in tex)
sys.path.insert(0, os.path.join(C, "CFG100_kids_mass_rederivation")); os.environ.setdefault("ZF_REPO", os.path.join(H, "..", ".."))
import cfg100_lib as Lb
xe = [(5.364 / f) * math.sqrt(4.30091e-9 * 10 ** m / Lb.A0["canonical"]) / Lb.r_ta_law(10 ** m, Lb.A0["canonical"], 0.0) for m in (10.5, 10.8, 11.0, 11.3) for f in (0.07, 0.10)]
row("KiDS-lens x_edge 0.24-0.54 (canonical; recomputed with cfg100_lib)", round(min(xe), 2) == 0.24 and round(max(xe), 2) == 0.54 and "0.24$--$0.54" in tex)

# ---- v2.0 rows: the zero-knob rule (CFG424-427, CFG425, CFG439) and the 512^3 comparison edges (CFG414, CFG416)
def rr(rel, dig): return lambda x: round(x, dig)
c424 = j("CFG424_turnaround_catchment/cfg424_results.json")
row("CFG424 can/alt 1.0033/1.0031, 0.027/0.029; MUTATE 1.0326/0.154", (round(c424["TA-can"]["s8"], 4), round(c424["TA-alt"]["s8"], 4), round(c424["TA-can"]["pdev"], 3), round(c424["TA-alt"]["pdev"], 3), round(c424["MUTATE (no compensation)"]["s8"], 4), round(c424["MUTATE (no compensation)"]["pdev"], 3)) == (1.0033, 1.0031, 0.027, 0.029, 1.0326, 0.154)
    and "1.0033 / 1.0031 & 0.027 / 0.029" in tex and "1.0326 & 0.154" in tex and "15.4\\%" in tex)
c425 = j("CFG425_turnaround_catchment_confirm/cfg425_results.json")
R1, R2, R3 = c425["R1 256^3 seed 360"], c425["R2 256^3 seed 361"], c425["R3 512^3 seed 359"]
row("CFG425 R1/R2 1.0024/1.0026, 0.022/0.017; R3 1.0045 / 0.033", (round(R1["s8"], 4), round(R2["s8"], 4), round(R1["pdev"], 3), round(R2["pdev"], 3), round(R3["s8"], 4), round(R3["pdev"], 3)) == (1.0024, 1.0026, 0.022, 0.017, 1.0045, 0.033)
    and "1.0024 / 1.0026 & 0.022 / 0.017" in tex and "\\textbf{1.0045} & \\textbf{0.033}" in tex and "$3.3\\%$" in tex)
c426 = j("CFG426_zero_knob_de_and_alt_seeds/cfg426_results.json")
row("CFG426 DE 1.0035/1.0032, 0.029/0.030; alt seeds 1.0023/1.0030, 0.025/0.023", (round(c426["D1 DE canonical 359"]["s8"], 4), round(c426["D2 DE alt 359"]["s8"], 4), round(c426["D1 DE canonical 359"]["pdev"], 3), round(c426["D2 DE alt 359"]["pdev"], 3),
    round(c426["A1 FLAT alt 360"]["s8"], 4), round(c426["A2 FLAT alt 361"]["s8"], 4), round(c426["A1 FLAT alt 360"]["pdev"], 3), round(c426["A2 FLAT alt 361"]["pdev"], 3)) == (1.0035, 1.0032, 0.029, 0.030, 1.0023, 1.0030, 0.025, 0.023)
    and "1.0035 / 1.0032 & 0.029 / 0.030" in tex and "1.0023 / 1.0030 & 0.025 / 0.023" in tex)
c427 = j("CFG427_zero_knob_inherited_settings/cfg427_results.json")
row("CFG427 eps 1.0033/1.0033 0.027/0.027; filters 1.0027/1.0038 0.026/0.031", (round(c427["E1 eps 0.0385"]["s8"], 4), round(c427["E2 eps 0.154"]["s8"], 4), round(c427["E1 eps 0.0385"]["pdev"], 3), round(c427["E2 eps 0.154"]["pdev"], 3),
    round(c427["G1 MIXB"]["s8"], 4), round(c427["G2 HOT1"]["s8"], 4), round(c427["G1 MIXB"]["pdev"], 3), round(c427["G2 HOT1"]["pdev"], 3)) == (1.0033, 1.0033, 0.027, 0.027, 1.0027, 1.0038, 0.026, 0.031)
    and "1.0033 / 1.0033 & 0.027 / 0.027" in tex and "1.0027 / 1.0038 & 0.026 / 0.031" in tex)
c439 = j("CFG439_zero_knob_alt_512/cfg439_results.json")
row("CFG439 512 alt 1.0054/0.040, DE 1.0045/0.033", (round(c439["A FLAT alt"]["s8"], 4), round(c439["A FLAT alt"]["pdev"], 3), round(c439["B DE canonical"]["s8"], 4), round(c439["B DE canonical"]["pdev"], 3)) == (1.0054, 0.040, 1.0045, 0.033)
    and "1.0054 & 0.040" in tex and "1.0045 & 0.033" in tex and "$0.6\\%$" in tex and "Lambda$CDM-equivalent" in tex and "convergence is not established" in tex)
allr = [c424["TA-can"], c424["TA-alt"], R1, R2, R3] + [c426[k] for k in c426 if k != "verdict"] + [c427[k] for k in c427 if k != "verdict"] + [c439["A FLAT alt"], c439["B DE canonical"]]
row("15 of 15 runs of the rule GROWTH OK, all sigma8 within 0.6%", len(allr) == 15 and all(r["verdict"] == "GROWTH OK" and abs(r["s8"] - 1) <= 0.006 for r in allr) and "15 of 15" in tex)
c414 = j("CFG414_confined_switch_512/cfg414_results.json"); c416 = j("CFG416_supply_edge_confinement_512/cfg416_results.json")
row("CFG414 512 1.0046/1.0059, 0.080/0.0996; CFG416 1.0072/1.0073, 0.092/0.1009", (round(c414["canonical"]["s8"], 4), round(c414["alt"]["s8"], 4), round(c414["canonical"]["pdev"], 3), round(c414["alt"]["pdev"], 4),
    round(c416["canonical"]["s8"], 4), round(c416["alt"]["s8"], 4), round(c416["canonical"]["pdev"], 3), round(c416["alt"]["pdev"], 4)) == (1.0046, 1.0059, 0.080, 0.0996, 1.0072, 1.0073, 0.092, 0.1009)
    and "1.0046 / 1.0059 & 0.080 / 0.0996" in tex and "1.0072 / 1.0073 & 0.092 / 0.1009" in tex)
W = os.path.join(H, "..", "..", "..", "_external_data", "cfg424_work")
if os.path.isdir(W):
    qm = lambda f: json.load(open(os.path.join(W, f)))["snap"]["z0"]["q_max"]
    q256 = max(qm(f) for f in os.listdir(W) if f.endswith("N256.json") and "_TA_MIXA" in f and "NOCOMP" not in f)
    q512 = max(qm(f) for f in os.listdir(W) if f.endswith("N512.json") and "_TA_MIXA" in f)
    row("max catchment draw 30% (256^3) / 57% (512^3) [work files]", round(q256 * 100) == 30 and round(q512 * 100) == 57 and "30\\% at $256^3$ and 57\\% at $512^3$" in tex)
row("edge 5.85 r_M = 1/ln(1/(1-f_b)) with engine f_b", abs(1 / math.log(1 / (1 - 0.02237 / (0.02237 + 0.1200))) - 5.85) < 5e-3 and "5.85\\,r_M" in tex)
print(f"\n{sum(rows)}/{len(rows)} audit rows pass"); sys.exit(0 if all(rows) else 1)
