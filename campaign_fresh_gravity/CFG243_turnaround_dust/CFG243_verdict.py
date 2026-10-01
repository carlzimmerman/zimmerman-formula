#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG243_verdict -- applies the frozen stop rule to the committed JSONs and prints the gate table.  The frozen order is COSMIC -> G0 -> AMOUNT -> HIERARCHY -> G3/G4; the lane
STOPS at the first binding FAIL.  Results from scripts with `_posthoc` in the name are printed in a separate, labelled block and are never part of the verdict.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG243_common as C

R = C.Run("CFG243_verdict")
P = R.P
P(__doc__.strip())


def load(slug):
    p = os.path.join(C.HERE, f"{slug}_results.json")
    return json.load(open(p)) if os.path.exists(p) else None


ctl = load("CFG243_controls")
cos = load("CFG243_cosmic")
R.banner("controls")
if ctl is None:
    P("  CFG243_controls_results.json missing: NOT RUN")
else:
    bad = [c["name"] for c in ctl["checks"] if c["kind"] == "control" and not c["ok"]]
    P(f"  {len(ctl['checks'])} controls, {len(bad)} failed: {bad if bad else 'none'}")
R.banner("frozen verdict (stop rule)")
binding = None
if cos is not None:
    cells = {c["name"]: c for c in cos["checks"] if c["kind"] == "result"}
    c1 = cells["C1 COSMIC: Omega_dust h^2 at the evaluation epoch >= 0.5 x requirement"]
    c1b = cells["C1b COSMIC: the shortfall is NOT an order of magnitude or more (the binding FAIL if this fails)"]
    P(f"  COSMIC C1: {'PASS' if c1['ok'] else 'FAIL'}   ({c1['detail']})")
    P(f"  COSMIC C1b (order-of-magnitude shortfall = the binding FAIL if it fails): {'PASS' if c1b['ok'] else 'FAIL'}")
    if not c1["ok"] and not c1b["ok"]:
        binding = "COSMIC"
nums = cos["numbers"] if cos else {}
if binding:
    om = nums.get("omega_dust_h2", {})
    lr = nums.get("log10_ratio_1100", {})
    P(f"\n  BINDING FAIL: {binding}.  A scoped no-go on the frozen class (a pressureless conserved dust created once at theta_b = 0 by a local causal source, funded by the vacuum), under the declared estimator.")
    for k in om:
        P(f"    M_min = {k[1:]}: Omega_dust h^2 at z = 1100 = 0.1200 x 10^{lr[k]:.1f} (line 0.060; total 0.1200); z = 10: {om[k]['10']:.4f}; z = 2.5: {om[k]['2.5']:.4f}; z = 0: {om[k]['0']:.4f}")
    P("  The lane stops here: G0, AMOUNT, HIERARCHY and G3/G4 are NOT part of the frozen verdict.")
else:
    P("  no binding FAIL found in COSMIC (unexpected for the frozen estimate): every later gate would be run in order")

R.banner("gate table (frozen cells; post-hoc cells labelled and never part of the verdict)")
rows = [("COSMIC", "CFG243_cosmic.py", "FAIL (binding)" if binding else "see above"),
        ("G0 legality", "CFG243_g0_legality_posthoc.py", None),
        ("AMOUNT", "CFG243_amount_posthoc.py", None),
        ("HIERARCHY", "CFG243_hierarchy_posthoc.py", None),
        ("G3/G4", "CFG243_g3g4_ledger_posthoc.py", None)]
for name, script, cell in rows:
    if cell is not None:
        P(f"  {name:12s} {cell:22s} [{script}]  (FROZEN verdict)")
        continue
    slug = script.replace(".py", "")
    j = load(slug)
    if j is None:
        P(f"  {name:12s} {'NOT ADDRESSED (frozen: stopped)':22s} [{script} not run]")
        continue
    v = list(j["numbers"].get("verdicts", {}).values())
    P(f"  {name:12s} {('POST-HOC ' + v[0]['status']) if v else 'POST-HOC (no verdict)':22s} [{script}]  {v[0]['why'] if v else ''}")
P(f"  {'G5':12s} {'NOT ADDRESSED':22s} [outside the frozen order: well-posedness and Solar System]")
P(f"  {'G2 (growth)':12s} {'NOT ADDRESSED':22s} [outside the frozen order: perturbation-level growth to k = 30/Mpc]")
R.finish()
