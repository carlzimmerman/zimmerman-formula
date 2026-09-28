#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG27 -- CLOSING THE EDGE THREAD: is the cold-budget-vs-KiDS tension an exclusion of the target law, or smaller than what the KiDS
machinery demonstrably does to standard halos?

WHAT THIS IS.  A bookkeeping lane on committed numbers only.  Every input is read from a committed results file, and the outcome was
known when this script was written; it records the closing rule and its result, and tests nothing new.

THE RULE (declared here).  A model-vs-data tension measured with a machinery counts as an EXCLUSION only if it exceeds the spread
that machinery demonstrably produces for STANDARD physics under reasonable modelling choices.  The spread S is taken as the SMALLEST
of the standard-halo spreads the record measured on KiDS's isolated lenses (the most conservative choice -- it makes an exclusion as
easy as possible):
  S_NFW   = chi^2(NFW, Duffy+08 c, best truncation)  - chi^2(NFW, c x 0.7, best truncation)        CFG23 / CFG23_diagnostics V3
  S_sph0  = chi^2(spherical-infall standard halo, A = 0, best)       - the same best NFW chi^2     CFG25
  S_sphb  = chi^2(spherical-infall standard halo, A <= b_Tinker, best) - the same best NFW chi^2   CFG25
The tension: KiDS's cost at the cold budget's edge against KiDS's own best (CFG24: turned-around associations, the framework's own
T3 level; the Milky-Way erratum applied), all four footing/kernel rows, and the generous linking (reported).

  C1  CONTROL  the committed inputs are read back and are finite.
  H1  [HEADLINE; MUTATE must fail] the canonical budget-vs-KiDS cost (both kernels) is below S: the edge thread closes as NOT
      DECIDABLE with this machinery (not an exclusion).  Known when written: yes.
  R1  (reported) the alt rows; the ratio cost / S; each spread separately.
MUTATE=1: S is set to 0 (a machinery with no demonstrated spread) -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG27_edge_thread_closure.py   (MUTATE=1 for the control; < 1 s)
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG27_edge_thread_closure", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the machinery's spread set to 0 -- H1 must FAIL ***")

J = lambda f: json.load(open(os.path.join(HERE, f)))["numbers"]
c23 = J("CFG23_lcdm_control_results.json")
c23d = J("CFG23_diagnostics_results.json")
c24 = J("CFG24_budget_associations_results.json")
c25 = J("CFG25_fg016_lcdm_control_results.json")

chi_duffy = c23["fit"]["chi2_best"]                                                    # NFW, Duffy c, best x_t
v3 = c23d["V3"]
best_nfw_key = min(v3, key=v3.get)
chi_best_nfw = v3[best_nfw_key]
chi_sph0 = c25["summary"]["best_A0"]["chi2"]
chi_sphb = c25["summary"]["best_capped"]["chi2"]
fw_best = c23["fit"]["framework_best"]["canonical|P2"]
S_NFW, S_sph0, S_sphb = chi_duffy - chi_best_nfw, chi_sph0 - chi_best_nfw, chi_sphb - chi_best_nfw
S = 0.0 if MUTATE else min(S_NFW, S_sph0, S_sphb)
COST = {k.replace("op|", ""): v["associations"]["kids_cost"] for k, v in c24["edges"].items() if k.startswith("op|")}
GEN = {k.replace("op|", ""): v["generous"]["kids_cost"] for k, v in c24["edges"].items() if k.startswith("op|")}

R.banner("C1  CONTROL: the committed inputs")
vals = [chi_duffy, chi_best_nfw, chi_sph0, chi_sphb, fw_best] + list(COST.values()) + list(GEN.values())
P(f"    NFW Duffy c (CFG23): {chi_duffy:.2f}; best NFW variant (CFG23_diagnostics V3, {best_nfw_key}): {chi_best_nfw:.2f}; spherical "
  f"infall standard halo (CFG25): {chi_sph0:.2f} (A = 0) / {chi_sphb:.2f} (A <= b); the framework's best (CFG21): {fw_best:.2f}")
check("C1 CONTROL: every committed input is read back and finite", f"{len(vals)} values", all(math.isfinite(v) for v in vals))

R.banner("THE RULE APPLIED")
P(f"    spreads: S_NFW {S_NFW:.1f}; S_sph (A = 0) {S_sph0:.1f}; S_sph (A <= b) {S_sphb:.1f} -> S = {S:.1f} (the smallest)")
for k in COST:
    P(f"    {k:18s}: budget-vs-KiDS cost {COST[k]:.1f} (generous linking {GEN[k]:.1f}); cost / S = {COST[k] / S if S > 0 else float('inf'):.2f}")
h1 = all(COST[f"canonical|{kn}"] < S for kn in ("P2", "nu_mono"))
check("H1 [HEADLINE] the canonical budget-vs-KiDS cost (both kernels) is below the machinery's smallest demonstrated standard-halo "
      "spread: the edge thread closes as NOT DECIDABLE with this machinery" + ("  [MUTATE: S = 0]" if MUTATE else ""),
      "; ".join(f"{kn}: {COST[f'canonical|{kn}']:.1f} vs S {S:.1f}" for kn in ("P2", "nu_mono")), h1)
check("R1 (reported) the alt rows against the same S", "; ".join(f"{kn}: {COST[f'alt|{kn}']:.1f}" for kn in ("P2", "nu_mono")) +
      f" vs S {S:.1f}", all(COST[f"alt|{kn}"] < S for kn in ("P2", "nu_mono")), load_bearing=False)
R.num("closure", dict(S=S, S_NFW=S_NFW, S_sph_A0=S_sph0, S_sph_capped=S_sphb, cost=COST, cost_generous=GEN, best_nfw=best_nfw_key,
                      verdict=("NOT DECIDABLE with this machinery" if h1 else "EXCLUSION-LEVEL")))
nf = R.write()
sys.exit(1 if nf else 0)
