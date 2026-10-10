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

# ---- v2.2 correction: every rule run re-measured on the GRAVITATING density (CFG555)
G = j("CFG555_growth_on_gravitating_field/cfg555_results.json"); GR = G["runs"]
f4 = lambda x: f"{x:.4f}"; f3 = lambda x: f"{x:.3f}"
ctab = [("$256^3$, canonical &", "424_TAcan"), ("$256^3$, alternative &", "424_TAalt"),
        ("$256^3$, realisation 2 (canonical) &", "425_R1_can_s360"), ("$256^3$, realisation 3 (canonical) &", "425_R2_can_s361"),
        ("$256^3$, realisation 2 (alternative) &", "426_A1_alt_s360"), ("$256^3$, realisation 3 (alternative) &", "426_A2_alt_s361"),
        ("$256^3$, $a_0$ tracking dark energy (canonical) &", "426_D1_DEcan"), ("$256^3$, $a_0$ tracking dark energy (alternative) &", "426_D2_DEalt"),
        ("$256^3$, switch width halved &", "427_E1_eps0.0385"), ("$256^3$, switch width doubled &", "427_E2_eps0.154"),
        ("$256^3$, other gas filter (1) &", "427_G1_MIXB"), ("$256^3$, other gas filter (2) &", "427_G2_HOT1"),
        ("\\textbf{, canonical} &", "425_R3_can_512"), ("$512^3$, alternative &", "439_A_alt_512"),
        ("$512^3$, $a_0$ tracking dark energy &", "439_B_DEcan_512"), ("$512^3$, realisation 2 (canonical) &", "460_can_512_s360"),
        ("control: mass conservation switched off ($256^3$) &", "424_MUTATE_nocomp")]
for lab, k in ctab:
    r = GR[k]; p, g = r["particle"], r["gravitating"]
    gs = f"{f4(g['s8'])} / {f3(g['pdev'])}"
    if k.endswith("512") or k.startswith("460"): gs = "\\textbf{" + gs + "}"
    line = f"{lab} {f4(p['s8'])} / {f3(p['pdev'])} & {gs}\\\\"
    ok = r["status"] == "EVALUATED" and r["gates_pass"] and r["C0"]["pass_"] and line in tex
    ok = ok and (g["verdict"] == "GROWTH OK") == (r["N"] == 256 and r["counted_as_pass"])
    row(f"CFG555 {k}: particle {f4(p['s8'])}/{f3(p['pdev'])}, gravitating {f4(g['s8'])}/{f3(g['pdev'])} ({g['verdict']})", ok)
P45 = G["PAPER45"]; r256 = P45["range_256"]
row("CFG555 PAPER45 verdict FAILS, 12 of 15, failing = the three 512^3 runs", P45["verdict"] == "CLAIM FAILS ON GRAVITATING FIELD" and P45["n_runs"] == 15 and P45["n_growth_ok"] == 12
    and sorted(P45["failing_or_unevaluable"]) == ["425_R3_can_512", "439_A_alt_512", "439_B_DEcan_512"] and "12 of 15 pass" in tex)
row("CFG555 256^3 gravitating range 0.063-0.082, s8 1.014-1.019", (f3(r256["pdev"][0]), f3(r256["pdev"][1]), f"{r256['s8'][0]:.3f}", f"{r256['s8'][1]:.3f}") == ("0.063", "0.082", "1.014", "1.019")
    and "$\\max|P-1|=0.063$--$0.082$, $\\sigma_8$ ratio $1.014$--$1.019$" in tex and "$6.3$--$8.2\\%$ at $256^3$" in tex)
k512 = ["425_R3_can_512", "439_A_alt_512", "439_B_DEcan_512", "460_can_512_s360"]
pd = [GR[k]["gravitating"]["pdev"] for k in k512]; s8 = [GR[k]["gravitating"]["s8"] for k in k512]
row("CFG555 all four 512^3 runs fail: 0.163-0.193 (16-19%), s8 +3-5% and inside the 5% cut", all(GR[k]["gravitating"]["verdict"] == "TENSION" for k in k512) and all(GR[k]["particle"]["verdict"] == "GROWTH OK" for k in k512)
    and (f3(min(pd)), f3(max(pd))) == ("0.163", "0.193") and (round(min(pd) * 100), round(max(pd) * 100)) == (16, 19) and all(0.03 <= s - 1 <= 0.05 for s in s8)
    and "$0.163$--$0.193$ against $0.10$" in tex and "$16$--$19\\%$ at $512^3$ ($\\sigma_8$ $+3$--$5\\%$)" in tex and "$\\sigma_8$ stays inside its $5\\%$ cut" in tex)
r1 = [GR[k]["gravitating"]["r_at"]["1.0"] for k in k512]
row("CFG555 512^3 gravitating 13-20% below control at k = 1", (round((1 - max(r1)) * 100), round((1 - min(r1)) * 100)) == (13, 20) and "$13$--$20\\%$ below the control at $k=1" in tex)
row("CFG555 particle numbers reproduced to < 1e-7 (C0) and controls C1/C2 pass", G["C0_all_pass"] and G["controls"]["C1_pass"] and G["controls"]["C2_pass"]
    and all(max(abs(GR[k]["particle"]["s8"] - GR[k]["committed"]["s8"]), abs(GR[k]["particle"]["pdev"] - GR[k]["committed"]["pdev"])) < 1e-7 for k in GR) and "better than $10^{-7}$" in tex)
c460 = j("CFG460_zero_knob_512_second_seed/cfg460_results.json")
row("CFG460 second 512^3 realisation: committed particle 1.0037 / 0.040 (GROWTH OK) = CFG555 particle", (f4(c460["s8"]), f3(c460["pdev"]), c460["cut"]) == ("1.0037", "0.040", "GROWTH OK")
    and abs(c460["s8"] - GR["460_can_512_s360"]["particle"]["s8"]) < 1e-7 and abs(c460["pdev"] - GR["460_can_512_s360"]["particle"]["pdev"]) < 1e-7)
row("v2.2 version line + scope note (comparison rows not re-measured)", "version 2.2" in tex and "Correction (2026-10-10)" in tex and "they were not re-measured" in tex and "Fixes Structure Growth" not in tex
    and "is therefore not fixed by this rule" in tex)
# ---- v2.2 kernel wording: nu_mono (engine) vs 1/(1-exp(-sqrt y)), recomputed from the engine source
_src = open(os.path.join(C, "CFG424_turnaround_catchment", "cfg424_pm.py")).read()
_ns = {"np": __import__("numpy"), "math": math}; from scipy.optimize import brentq as _bq; _ns["brentq"] = _bq
exec(_src[_src.index("def h_rar"):_src.index("# ---------------------------------------------------------------- linear theory")], _ns)
import numpy as _np
_nu = lambda y: 1 / (1 - _np.exp(-_np.sqrt(y)))
_lo = _np.logspace(-3, _np.log10(2.5), 400); _hi = _np.linspace(10, 30, 2001); _all = _np.logspace(-3, 4, 7001)
_d = lambda y: _ns["nu_mono"](y) / _nu(y) - 1
_ye = (1 / 5.85) ** 2
row("kernel: Y_P 2.54; nu_mono = analytic for y <= 2.5 (<2e-4) and at the edge y~0.03; max diff 2.4% (y=10-30, also global)",
    round(_ns["Y_P"], 2) == 2.54 and _np.abs(_d(_lo)).max() < 2e-4 and abs(_d(_ye)) < 1e-6 and round(_d(_hi).max() * 100, 1) == 2.4 and _d(_all).max() <= _d(_hi).max() + 1e-6
    and "\\nu_{\\rm mono}$ (equal to $1/(1-e^{-\\sqrt y})$ for $y\\lesssim2.5$" in tex and "$\\le2.4\\%$ at $y=10$--$30$" in tex and "$y\\approx0.03$" in tex)
print(f"\n{sum(rows)}/{len(rows)} audit rows pass"); sys.exit(0 if all(rows) else 1)
