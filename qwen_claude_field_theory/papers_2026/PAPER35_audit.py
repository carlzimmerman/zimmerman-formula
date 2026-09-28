#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PAPER35 audit: every number the note quotes, re-read from the committed outputs (and the frozen pre-registration text).
Exit 0 only if every quoted value matches its source at the precision quoted.  Run: python3 PAPER35_audit.py"""
import os, sys, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFG = os.path.join(REPO, "campaign_fresh_gravity")
J = lambda f: json.load(open(os.path.join(CFG, f)))["numbers"]
ROWS = []


def q(label, quoted, value, tol):
    ok = abs(quoted - value) <= tol
    ROWS.append((label, quoted, value, ok))


# SPARC (CFG4_galaxy_law H2)
h2 = J("CFG4_galaxy_law_results.json")["H2"]
q("SPARC rms nu_mono canonical 0.100", 0.100, h2["canonical|nu_mono"]["rms"], 0.0005)
q("SPARC rms nu_mono alt 0.099", 0.099, h2["alt|nu_mono"]["rms"], 0.0005)
q("SPARC rms P2 canonical 0.108", 0.108, h2["canonical|P2"]["rms"], 0.0005)
q("SPARC rms P2 alt 0.104", 0.104, h2["alt|P2"]["rms"], 0.0005)
# FG001 gate table (canonical / alt), fg001 vs rival
G = J("CFG7_hierarchy_fg001_results.json")["GATES"]
for key, fq, rq in (("G4 MW classical dSphs", (1.1, 0.7), (3.5, 3.3)), ("G5 M31 dwarfs (LVD)", (2.6, 2.2), (6.0, 5.7)),
                    ("G6 M31 dwarfs (Collins+13)", (2.5, 2.3), (5.8, 5.6)), ("G7 MW ultra-faints", (8.0, 7.5), (13.2, 12.8))):
    for i, f in enumerate(("canonical", "alt")):
        q(f"FG001 {key} {f}", fq[i], G[key][f]["fg001"], 0.05)
        q(f"rival {key} {f}", rq[i], G[key][f]["rival"], 0.05)
for key, fq, rq in (("G8 LV dwarfs' host statistic", 1.7, 3.9), ("G9 cluster-infall BTFR slope", 0.1, 2.4),
                    ("G10 cluster-infall BTFR zero point", 1.3, 0.8), ("G11 NGC 1052-DF2", 0.0, 2.9), ("G12 NGC 1052-DF4", 0.8, 1.5),
                    ("G13 Chae D1 (143 galaxies)", 4.1, 0.8), ("G14 Chae D2 (90 galaxies)", 4.3, 0.0)):
    q(f"FG001 {key} canonical", fq, G[key]["canonical"]["fg001"], 0.05)
    q(f"rival {key} canonical", rq, G[key]["canonical"]["rival"], 0.05)
q("rival G11 NGC 1052-DF2 alt 3.1", 3.1, G["G11 NGC 1052-DF2"]["alt"]["rival"], 0.05)
F7 = J("CFG7_hierarchy_fg001_results.json")
q("FG001 score 9 of 14 (canonical)", 9, F7["SCORE"]["canonical"][0], 0); q("rival score 6 of 14 (canonical)", 6, F7["SCORE"]["canonical"][1], 0)
q("FG001 score 9 of 14 (alt)", 9, F7["SCORE"]["alt"][0], 0); q("FG001 total gates 14", 14, len(F7["GATES"]), 0)
tides = [v["tide"] for v in F7["H1"].values()]; ratios = [v["ratio"] for v in F7["H1"].values()]
q("MW phantom tide at the Sun low 1.6e-31", 1.6e-31, min(tides), 0.05e-31); q("... high 2.6e-31", 2.6e-31, max(tides), 0.05e-31)
q("Cassini margin low 2e4", 2e4, min(ratios), 0.5e4); q("Cassini margin high 3e4", 3e4, max(ratios), 0.5e4)
# CFG18 infall baryons (non-detections as zero)
R18 = J("CFG18_satellite_infall_gas_results.json")["RES"]
for key, quoted in (("m31|zero|canonical", 1.6), ("m31|zero|alt", 1.2), ("col|zero|canonical", 1.4), ("col|zero|alt", 1.2),
                    ("cls|zero|canonical", 0.4), ("cls|zero|alt", 0.1), ("ufd|zero|canonical", 7.4)):
    q(f"CFG18 {key} z", quoted, R18[key]["z"], 0.05)
b = J("CFG19_harness_rescore_results.json")["B_rescored"]
q("CFG19 harness 42 of 48 (npass)", 42, b["npass"], 0); q("CFG19 harness ntot 48", 48, b["ntot"], 0)
# CFG8 Chae refit
S8 = J("CFG8_chae_kernel_results.json")["STAT"]
q("CFG8 P2 canonical 1.7 sigma", 1.7, S8["V4"]["z_lo"], 0.05); q("CFG8 nu_mono canonical 2.2 sigma", 2.2, S8["V6"]["z_lo"], 0.05)
q("CFG8 alt lower 2.7 sigma (P2)", 2.7, S8["V5"]["z_lo"], 0.05); q("CFG8 alt upper 3.0 sigma (nu_mono)", 3.0, S8["V7"]["z_lo"], 0.05)
# CFG9, CFG14
q("CFG9 theorem max deviation 9e-8", 9e-8, J("CFG9_local_virial_results.json")["D1"]["max_dev"], 0.5e-8)
D14 = J("CFG14_shape_calibration_results.json")["dist"]
q("CFG14 P2 canonical p ~ 0.03", 0.03, D14["canonical|P2|A"]["p_two_sided"], 0.005)
q("CFG14 P2 alt p low 0.03", 0.03, min(D14["alt|P2|A"]["p_two_sided"], D14["alt|P2|B"]["p_two_sided"]), 0.005)
q("CFG14 P2 alt p high 0.13", 0.13, max(D14["alt|P2|A"]["p_two_sided"], D14["alt|P2|B"]["p_two_sided"]), 0.005)
# CFG21
R21 = J("CFG21_kids_lg_joint_results.json")["RES"]
kmins = [v["kids_min"] for v in R21.values()]
q("CFG21 KiDS best -35 (least negative)", -35, max(kmins), 0.5); q("CFG21 KiDS best -38 (most negative)", -38, min(kmins), 0.5)
q("CFG21 KiDS best x_e 0.62", 0.62, R21["canonical|P2|1.145e+11"]["kids_best_x"], 0.005)
q("CFG21 framework T 26.2 (P2)", 26.2, R21["canonical|P2|1.145e+11"]["T_min"], 0.05)
q("CFG21 framework T 27.8 (nu_mono)", 27.8, R21["canonical|nu_mono|1.145e+11"]["T_min"], 0.05)
# CFG23 (+ diagnostics)
f23 = J("CFG23_lcdm_control_results.json")["fit"]
q("CFG23 Duffy-c NFW chi^2 174", 174, f23["chi2_best"], 0.5); q("CFG23 framework best 104.7", 104.7, f23["framework_best"]["canonical|P2"], 0.05)
v3 = J("CFG23_diagnostics_results.json")["V3"]
q("CFG23d best NFW variant 99.3", 99.3, min(v3.values()), 0.05)
Ts = [v["T"] for v in f23["joint"].values()]; R0s = [v["R0"] for v in f23["joint"].values()]
q("CFG23 LCDM T low 24.5", 24.5, min(Ts), 0.05); q("CFG23 LCDM T high 72.5", 72.5, max(Ts), 0.05)
q("CFG23 LCDM R0 low 1.5", 1.5, min(R0s), 0.05); q("CFG23 LCDM R0 high 1.9", 1.9, max(R0s), 0.05)
q("CFG23d projection vs analytic 3e-4", 3e-4, J("CFG23_diagnostics_results.json")["V1"]["max_rel"], 0.5e-4)
# CFG24, CFG25, CFG27
E = J("CFG24_budget_associations_results.json")["edges"]
q("CFG24 edge canonical P2 0.390", 0.390, E["op|canonical|P2"]["associations"]["edge"], 0.0005)
q("CFG24 edge alt P2 0.336", 0.336, E["op|alt|P2"]["associations"]["edge"], 0.0005)
q("CFG24 cost P2 29.4", 29.4, E["op|canonical|P2"]["associations"]["kids_cost"], 0.05)
q("CFG24 cost nu_mono 32.9", 32.9, E["op|canonical|nu_mono"]["associations"]["kids_cost"], 0.05)
q("CFG24 cost alt low 45", 45, E["op|alt|P2"]["associations"]["kids_cost"], 0.5)
q("CFG24 cost alt high 49", 49, E["op|alt|nu_mono"]["associations"]["kids_cost"], 0.5)
s25 = J("CFG25_fg016_lcdm_control_results.json")["summary"]
q("CFG25 spherical-infall standard halo 149", 149, s25["best_capped"]["chi2"], 0.5); q("CFG25 ... 173", 173, s25["best_A0"]["chi2"], 0.5)
q("CFG27 smallest spread 50.2", 50.2, J("CFG27_edge_thread_closure_results.json")["closure"]["S"], 0.05)
# k05
k5 = json.load(open(os.path.join(REPO, "kappa_closure", "k05_is_32pi_special_results.json")))["numbers"]["S3"]["combined"]
q("k05 combined kappa 0.530", 0.530, k5[0], 0.0005); q("k05 combined sigma 0.037", 0.037, k5[1], 0.0005)
# FP18 (the zero-velocity radius used by CFG20-CFG23)
fp18 = open(os.path.join(REPO, "real_research", "derivation_chain_2026", "FP18_kids_vs_hubble_flow_data.out")).read()
m = re.search(r"stack\s+R0 = ([0-9.]+)\s+quoted \+-([0-9.]+)\s+honest \+-([0-9.]+)", fp18)
q("FP18 stack R0 0.93", 0.93, float(m.group(1)), 0.005); q("FP18 honest error 0.12", 0.12, float(m.group(3)), 0.005)
# the frozen pre-registration text (Amendments 13 and 14)
pre = open(os.path.join(REPO, "prep_2026", "gaia_dr4_prep", "PREREGISTRATION_DR4.md")).read()
for s in ("1.084", "1.1614–1.1814", "1.1917–1.2267", "1.0725", "1.0900", "1.157", "1.174", "5.8σ_tot / 6.8σ_tot", "1.23",
          "1.6–2.6e-31", "2–3 × 10⁴"):
    ROWS.append((f"pre-registration text contains '{s}'", 1, int(s in pre), s in pre))
# DR3 validation of the catalogue chain
val = open(os.path.join(REPO, "prep_2026", "gaia_dr4_prep", "catalog_builder", "README.md")).read()
ROWS.append(("catalogue README: 99.40% El-Badry pairs recovered", 1, int("99.40%" in val), "99.40%" in val))

bad = [r for r in ROWS if not r[3]]
for lab, qv, v, ok in ROWS:
    print(f"  [{'ok ' if ok else 'BAD'}] {lab:60s} quoted {qv!s:>8}  source {v!s:.10}")
print(f"\n{len(ROWS) - len(bad)}/{len(ROWS)} quoted values match their committed sources")
sys.exit(1 if bad else 0)
