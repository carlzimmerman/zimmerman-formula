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
row("R_c 4.6-13.0 / 6.0-16.5", tuple(round(v, 1) for v in q["canonical"]["Rc_range"]) == (4.6, 13.0) and tuple(round(v, 1) for v in q["alt"]["Rc_range"]) == (6.0, 16.5) and "$4.6$--$13.0$" in tex and "$6.0$--$16.5$" in tex)
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
print(f"\n{sum(rows)}/{len(rows)} audit rows pass"); sys.exit(0 if all(rows) else 1)
