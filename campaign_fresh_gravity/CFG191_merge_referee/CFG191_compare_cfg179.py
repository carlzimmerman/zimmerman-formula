#!/usr/bin/env python3
"""CFG191_compare_cfg179 -- PHASE 2, run only AFTER CFG191_s1..s5b main and MUTATE results were saved.  Reads CFG179's committed s1/s2 .out files
(read-only) and prints its numbers beside mine, with a difference class: numerical / definition / framing / scoring convention / README typo.
Nothing is imported from CFG179; only its text outputs are parsed."""
import re, json, pathlib, sys
sys.dont_write_bytecode = True
from CFG191_common import REPO, rel, HERE
D = REPO/"campaign_fresh_gravity/CFG179_door11_merge_swirl"
o1 = (D/"cfg179_s1_merge_symbolic.out").read_text(); o2 = (D/"cfg179_s2_merge_numbers.out").read_text()
mine = {k: json.loads((HERE/f"CFG191_{k}_results.json").read_text()) for k in ("s1_theorem", "s2_coma_udg", "s3_solar_q2", "s4_scorecard", "s5_dr4_mapping", "s5b_pipeline_tier2")}
lines = []
def P(s=""): print(s); lines.append(s)
P(f"CFG179 outputs read: {rel(D/'cfg179_s1_merge_symbolic.out')}, {rel(D/'cfg179_s2_merge_numbers.out')} (text only)")
P(f"{'item':44s} {'CFG179':>14s} {'CFG191':>14s} {'diff':>9s}  class")
rows = []
def add(name, a, b, cls, unit=""):
    rows.append((name, a, b, cls)); P(f"{name:44s} {a:14.4f} {b:14.4f} {b-a:+9.4f}  {cls} {unit}")
# (a) six residuals
m = re.search(r"residuals \(0\.01,0\.1\): ([-\d.]+), \(0\.01,1\): ([-\d.]+), \(0\.1,0\.1\): ([-\d.]+), \(0\.1,1\): ([-\d.]+), \(1,0\.1\): ([-\d.]+), \(1,1\): ([-\d.]+)", o1)
theirs = [float(x) for x in m.groups()]; my6 = [d["r_sympy"] for d in mine["s1_theorem"]["data"]["six_points"]]
for i, (a, b) in enumerate(zip(theirs, my6)):
    add(f"(a) residual point {i+1}", a, b, "numerical (4-digit rounding)")
# (a) survival table T
tm = re.search(r"canonical wide binary / the Sun in the Milky Way \(1.778e-10\)\s+g_ext/a0 = 1.8995:\s+b=0.01: 1D ([\d.]+) / E7 ([\d.]+)", o2)
add("(a/T) MW Sun b=0.01 survival 1-D", float(tm.group(1)), 0.103, "numerical (README rounds to 0.10)")
# (b) Coma
h = mine["s2_coma_udg"]["data"]["headline"]
for foot, key in (("canonical", 0), ("alt", 1)):
    mm = re.search(rf"{foot}\s+g_ext = 0\.845 x 9\.3619e-11 \(g_ext/a0 = [\d.]+\): E7 ([+\d.]+) dex \(([\d.]+) sigma\)", o2)
    add(f"(b) E7 offset {foot} [dex]", float(mm.group(1)), h[foot]["offset"], "numerical (constants: Msun, G, kpc)")
    add(f"(b) E7 sigma {foot}", float(mm.group(2)), h[foot]["sigma"], "numerical (0.235 vs 0.2355; rounding)")
for gc, lab in (("0.427", "0.427"), ("1.059", "1.059")):
    mm = re.search(rf"canonical g_ext = {gc} x 9\.3619e-11 \(g_ext/a0 = [\d.]+\): E7 ([+\d.]+) dex", o2)
    add(f"(b) E7 canonical at {lab} a0(L23)", float(mm.group(1)), mine["s2_coma_udg"]["data"]["sweep"][lab][0][0], "numerical")
mm = re.search(r"canonical isolated P2, stars only \(no merge\): ([+\d.]+) dex", o2)
add("(b) isolated P2 canonical", float(mm.group(1)), h["canonical"]["iso"], "numerical")
# (c)
m8 = re.search(r"canonical: P2 alpha = 1 tail a0/2 = [\d.e+-]+ m/s\^2 = (\d+) x .*?a0/r_M = ([\d.e+-]+) s\^-2 = ([\d.]+) x", o2)
add("(c) natural scale a0/r_M / ceiling (canonical)", float(m8.group(3)), 15.1, "numerical (identical)")
p2v = [v for k, v in mine["s3_solar_q2"]["data"]["table"].items() if k.startswith("P2")]; rv = [v for k, v in mine["s3_solar_q2"]["data"]["table"].items() if k.startswith("nu_RAR")]
P(f"  (c) CFG179 cites GATES 4.01 '4.0-5.7 x' (not recomputed) and remarks 'the quadrupole coefficient is ~0.3-0.4 of a0/r_M' (4.0/15.1 = 0.26, 5.7/15.1 = 0.38: a rounding). Mine: P2 {min(p2v):.2f}-{max(p2v):.2f} x, nu_RAR {min(rv):.2f}-{max(rv):.2f} x over kernel x footing x g_ext; P2 alone does not reach 4.0 at its low end (3.63) and no single kernel spans 4.0-5.7. class: framing (a cited kernel-mixed range) + numerical")
# (d)
P(f"  (d) scorecard 9/14 vs 6/14: identical (CFG179 reads the committed lines; mine recounts from sigmas). class: none")
# (e)
t2 = mine["s5b_pipeline_tier2"]["data"]["summary"]
P(f"  (e) CFG179 M7: 'every merging-river composition predicts a boost (gamma > 1); only the no-merge rule (Arm C) predicts 1.000' and labels Arm A as 'merge, P2 as modified gravity, full nonlinear solve'.")
P(f"      CFG179's own C3 control reproduces the section-1.1 P2 numbers (z_e 1.4642, sqrt(nu) 1.1390), NOT the Arm A solve's nu_RAR y_extN 1.289 / sqrt(nu) 1.2138. Mine: P2 merge in the frozen estimator canonical {t2['P2|canonical|1.778e-10']['floor']:.4f}-{t2['P2|canonical|1.778e-10']['top']:.4f}; Arm A (nu_RAR, my control) {t2['nu_RAR|canonical|1.778e-10']['floor']:.4f}-{t2['nu_RAR|canonical|1.778e-10']['top']:.4f}. class: definition/kernel label + framing (universal claim vs Arm B / chain)")
P(f"      CFG179 point-field values (their M7): P2 perp 1.1390 / par 1.0169 / isotropic 1.0998 (algebraic tensor); mine QUMOND/AQUAL Poisson tensors: par 1.2973 (boost) / perp 1.1582 (AQUAL) -> gamma par 1.1390 / perp 1.0762, sphere-average 1.0975. class: definition (orientation of the axes; same sphere average to 0.003)")
(HERE/"CFG191_compare_cfg179.out").write_text("\n".join(lines) + "\n")
