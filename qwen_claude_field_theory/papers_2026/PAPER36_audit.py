#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PAPER36 audit: every number the note quotes, re-read from the committed outputs.  Exit 0 only if every quoted value matches its
source at the precision quoted.  Run: python3 PAPER36_audit.py"""
import os, sys, json, re, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFG = os.path.join(REPO, "campaign_fresh_gravity")
J = lambda f: json.load(open(os.path.join(CFG, f)))["numbers"]
ROWS = []


def q(label, quoted, value, tol):
    ROWS.append((label, quoted, value, abs(quoted - value) <= tol))


# CFG4 / CFG19
q("SPARC nu_mono canonical rms 0.100", 0.100, J("CFG4_galaxy_law_results.json")["H2"]["canonical|nu_mono"]["rms"], 0.0005)
q("X-COP identity ratio 0.946", 0.946, J("CFG4_clusters_results.json")["H2"]["canonical|nu_mono"]["id_ratio"], 0.0005)
b19 = J("CFG19_harness_rescore_results.json")["B_rescored"]; q("harness 42 of 48", 42, b19["npass"], 0); q("harness total 48", 48, b19["ntot"], 0)
# CFG34 groups
c34 = J("CFG34_groups_and_the_ladder_under_b_results.json")
q("groups R500 ratio 1.41 canonical", 1.41, 10 ** c34["RES"]["canonical|R500"]["med"], 0.005)
q("groups R500 ratio 1.33 alt", 1.33, 10 ** c34["RES"]["alt|R500"]["med"], 0.005)
q("groups R500 1.8 sigma canonical", 1.8, c34["RES"]["canonical|R500"]["z"], 0.05)
q("groups R500 1.5 sigma alt", 1.5, c34["RES"]["alt|R500"]["z"], 0.05)
q("groups R2500 ratio 1.88", 1.88, 10 ** c34["RES"]["canonical|R2500"]["med"], 0.005)
q("groups R2500 2.6 sigma", 2.6, c34["RES"]["canonical|R2500"]["z"], 0.05)
q("groups rho -0.958", -0.958, c34["H3"]["rho"], 0.0005)
q("groups p 7e-18 (order)", -17.1, math.log10(c34["H3"]["p"]), 0.1)
# CFG32 X-ray ellipticals under the law
c32 = J("CFG32_xray_ellipticals_under_b_results.json")["RES"]
q("X-ray ellipticals factor 1.91 canonical", 1.91, 10 ** c32["canonical"]["base"]["mean"], 0.005)
q("X-ray ellipticals factor 1.79 alt", 1.79, 10 ** c32["alt"]["base"]["mean"], 0.005)
q("X-ray ellipticals 1.7 sigma", 1.7, c32["canonical"]["z"], 0.05); q("X-ray ellipticals 1.6 sigma alt", 1.6, c32["alt"]["z"], 0.05)
q("X-ray ellipticals law +0.28", 0.28, c32["canonical"]["base"]["mean"], 0.005)
# CFG35 colour-blind
c35 = J("CFG35_cold_mass_conservation_results.json")
q("CFG35 ellipticals -0.013", -0.013, c35["RES"]["canonical"]["mean"], 0.0005); q("CFG35 ellipticals -0.024 alt", -0.024, c35["RES"]["alt"]["mean"], 0.0005)
q("CFG35 spirals up to +0.30 dex", 0.30, c35["SPARC"]["max_dlogv"], 0.005)
w35 = c35["SPARC"]["worst"][0]; ROWS.append(("CFG35 worst spiral is UGC 2885", 1, int(w35[0] == "UGC02885"), w35[0] == "UGC02885"))
# CFG36 colour split
c36 = J("CFG36_colour_split_collapse_results.json")
q("CFG36 ellipticals +0.125", 0.125, c36["RES"]["canonical"]["mean"], 0.0005); q("CFG36 ellipticals +0.122 alt", 0.122, c36["RES"]["alt"]["mean"], 0.0005)
q("CFG36 ellipticals 1.0 sigma", 1.0, c36["RES"]["canonical"]["z"], 0.05)
w36 = c36["SPARC"]["worst"][0]; q("UGC 2487 +0.14 dex", 0.14, w36[2], 0.005)
ROWS.append(("CFG36 worst is UGC 2487", 1, int(w36[0] == "UGC02487"), w36[0] == "UGC02487"))
n_fex_e = sum(x > 0 for x in c36["RES"]["canonical"]["fex"]); q("CFG36 ellipticals with f_ex > 0: 6 of 7", 6, n_fex_e, 0)
# CFG37 passive disks
c37 = J("CFG37_passive_disks_results.json")["RES"]["canonical|law"]
q("passive disks +0.026", 0.026, c37["mean"], 0.0005); q("passive disks +-0.085", 0.085, c37["tot"], 0.0005); q("passive disks 0.3 sigma", 0.3, c37["z"], 0.05)
# CFG38 SLUGGS
c38 = J("CFG38_sluggs_massive_passive_results.json")
r38 = c38["RES"]["canonical"]
q("SLUGGS law +0.080", 0.080, r38["law_mean"], 0.0005); q("SLUGGS law +-0.024", 0.024, r38["law_err"], 0.0005)
q("SLUGGS law 3.3 sigma", 3.3, r38["law_mean"] / r38["law_err"], 0.05)
q("SLUGGS rule +0.007", 0.007, r38["rule_mean"], 0.0005); q("SLUGGS rule +-0.017", 0.017, r38["rule_err"], 0.0005)
q("SLUGGS rule 0.4 sigma", 0.4, r38["rule_mean"] / r38["rule_err"], 0.05)
q("SLUGGS debris in 10 of 19", 10, sum(x > 0 for x in r38["fex"]), 0); q("SLUGGS 19 galaxies", 19, len(r38["fex"]), 0)
lr = np.array(c38["R2_lcdm_red"]); q("LCDM same halos -0.037", -0.037, float(lr.mean()), 0.0005)
q("LCDM same halos +-0.017", 0.017, float(lr.std(ddof=1) / math.sqrt(len(lr))), 0.0005)
o38 = open(os.path.join(CFG, "CFG38_sluggs_massive_passive.out")).read()
m87 = re.search(r"NGC4486\s+log M\*\s+[0-9.]+: law ([+-][0-9.]+) -> rule ([+-][0-9.]+)", o38)
q("M87 law +0.28", 0.28, float(m87.group(1)), 0.005); q("M87 rule +0.08", 0.08, float(m87.group(2)), 0.005)
# CFG39 harness
c39 = J("CFG39_harness_with_rule_results.json")
q("SPARC rms 0.1003", 0.1003, c39["sparc"]["rms0"], 0.00005); q("SPARC rms 0.1012 with the rule", 0.1012, c39["sparc"]["rms1"], 0.00005)
q("budget leftover at most 0.007", 0.007, max(v["leftover"] for k, v in c39["budget"].items() if k.endswith("|len")), 0.0005)
ROWS.append(("KiDS lens bins carry no debris", 1, int(all(x[1] == 0 for x in c39["kids_fex_red"])), all(x[1] == 0 for x in c39["kids_fex_red"])))
# the data files exist with provenance
for fn in ("mandelbaum2016_lbg_halo_mass.tsv", "denheijer2015_etg_hi_tfr.tsv"):
    txt = open(os.path.join(REPO, "real_research", "data", fn)).read()
    ROWS.append((f"{fn} carries provenance (sha256)", 1, int("sha256" in txt), "sha256" in txt))

bad = [r for r in ROWS if not r[3]]
for lab, qv, v, ok in ROWS:
    print(f"  [{'ok ' if ok else 'BAD'}] {lab:48s} quoted {qv!s:>8}  source {v!s:.10}")
print(f"\n{len(ROWS) - len(bad)}/{len(ROWS)} quoted values match their committed sources")
sys.exit(1 if bad else 0)
