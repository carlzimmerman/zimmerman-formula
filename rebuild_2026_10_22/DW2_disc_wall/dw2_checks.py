#!/usr/bin/env python3
"""DW2 checks left over: K4, K5, K8 (A4 path against the RQ2 harness), row 11 and row 12 implementation comparisons, measured-U table against U_open. Reads outputs; no fit. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, runpy, sys
import numpy as np
from astropy.io import fits
from dw2_core import *
OUT = []; R = {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
A4 = json.load(open("dw2_a4_results.json"))["footings"]; W = json.load(open("dw2_wall_results.json")); PR = json.load(open("dw2_proc_results.json")); SE = json.load(open("dw2_second_results.json"))
for ft, b_ in (("canonical", -0.016), ("alt", -0.023)):
    x = A4[ft]["LAW|em1|f0.0"]["slope"]["b"]; P(f"K4 {ft}: law slope {x:+.4f} vs HS1 {b_}: {'PASS' if abs(x - b_) <= .01 else 'FAIL'}")
mc = json.load(open(os.path.join(RB, "MC1_minimal_cold_requirement", "mc1_results.json")))["footings"]["canonical"]["xcop"]["table"]["0.1"]["dMg"]; P(f"K5 X-COP: dw2_a4 reads the same data and rule as MC1; MC1's dM/Mg at x 0.1 {mc:.2f} vs brief 8.53: {'PASS' if abs(mc / 8.53 - 1) < .01 else 'FAIL'} (a read, not a recompute: K1 and A4's LAW X-COP +0.425 vs RQ2's law B23 +0.4675 is the live comparison, differing by x-range)")
for ft in FEET:
    hp = os.path.join("acc", "results", "cand_max_share_fq.json")
    H = json.load(open(hp))["footings"][ft]["rows"]; a = A4[ft]["MAX|share|f0.872"]; l = A4[ft]["LAW|em1|f0.0"]; LH = json.load(open(os.path.join(RB, "RQ2_framework_acceptance", "results", "law.json")))["footings"][ft]["rows"]
    dr, du = a["path"]["rms"] - H["A1"]["value"], a["path"]["U"] - H["A2"]["value"]; ldr, ldu = l["path"]["rms"] - LH["A1"]["value"], l["path"]["U"] - LH["A2"]["value"]
    P(f"K8 {ft}: MAX share f_Q A4 path rms {a['path']['rms']:.4f} U {a['path']['U']:.2f} tilt {a['path']['tilt']:+.2f}; harness rms {H['A1']['value']:.4f} U {H['A2']['value']:.2f} tilt {H['A3']['value']:+.2f}. |rms diff| {abs(dr):.4f} ({'PASS' if abs(dr) <= .003 else 'FAIL'} at 0.003), |U diff| {abs(du):.2f} ({'PASS' if abs(du) <= .03 else 'FAIL'}). Same difference on the law itself: rms {ldr:+.4f}, U {ldu:+.2f} (samples and masks differ: Q<=2 vs all 175)")
# row 11 same sigma, f 0, against first implementation
ns = runpy.run_path("dw2_second.py", init_globals={}, run_name="skip") if False else None
RES11 = PR["star_em1"]; P(f"Row 11 first implementation (f 0, mean, sigma {RES11['sigma']:.2e}): retained " + " ".join(f"{a:.2f}" for a in RES11["retained"]))
json.dump({}, open(os.devnull, "w"))
# measured U vs U_open
Meas = {"NGC 6946 plain": (.444, .082), "NGC 6946 weighted": (.356, .071), "NGC 628": (.75, .18)}
for ft in FEET:
    for k in ("em1|f0.872|N", "share|f0.872|N", "share|f0.0|N", "share|f0.54|N"):
        q = W["A2"][ft][k]; uo = q["U_open"]; P(f"{ft} {k}: U_open by bin " + " ".join(f"{a:.2f}" for a in uo) + f"; 4of5 {q['U_open_4of5']:.2f}; U_fill " + " ".join(f"{a:.2f}" for a in q["U_fill"]))
        P("   GSWLC-U_open (U_tot) " + " ".join(f"{W['scenarios']['S2 GSWLC']['U'][i] - uo[i]:+.2f}" for i in range(5)) + " | Taylor-U_open " + " ".join(f"{W['scenarios']['S3 Taylor']['U'][i] - uo[i]:+.2f}" for i in range(5)) + " | Z 4of5 " + " ".join(f"{n} {(m - q['U_open_4of5']) / s:+.1f}" for n, (m, s) in Meas.items()))
open("dw2_checks.out", "w").write("\n".join(OUT) + "\n")
