#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG242_B_verdict -- aggregation only (no physics): route B (L13) gate table from the main results of the B scripts.  Never pooled with route A."""
import os, sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG242_common as C
HERE = C.HERE
def J(n):
    return json.load(open(os.path.join(HERE, f"CFG242_{n}.json")))
ctl, g5a, g4 = J("B_controls"), J("B_g5a_ghost"), J("B_g4_ledger")
L = []
def P(s=""):
    s = C.scrub(s); print(s); L.append(s)
f = g5a["numbers"]["flat"]
P("ROUTE B (L13): BIMOND with a lapse-free, preferred-foliation interaction.  Cells cite their script.  MAIN = the frozen stop-rule verdict.")
P("")
P(f"controls: {sum(1 for c in ctl['checks'] if c['ok'])}/{len(ctl['checks'])} PASS (CFG242_B_controls.py: EH gauge invariance, 4D class reproduces WF2/L70, 13c row reproduces CFG232's committed row)")
P("G5a flat space at mu/b = -1/4 (CFG242_B_g5a_ghost.py):")
for c in g5a["checks"]:
    P(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  ({c['detail']})")
P("  BACKGROUND (exact static MOND background): NOT ADDRESSED (stop rule)")
P(f"  verdict: {g5a['numbers']['verdicts'][[k for k in g5a['numbers']['verdicts']][0]]['status']}   -> STOP")
P("G4, G0 legality, G3, G5b, G1, G2: NOT ADDRESSED in the MAIN run (stop rule at G5a)")
P("POST-HOC continuation (labelled): G4 route B -- " + g4["numbers"]["verdicts"]["G4 route B (post-hoc continuation)"]["status"] + " (gamma/beta, mu/b and the direction are constants beyond kappa and Omega_c h^2)")
P("")
P(f"BINDING FAILURE (route B, main): G5a, cell HYPERBOLIC: at the frozen point mu/b = -1/4 the TT dispersion is omega^2 = c_T^2 kappa^2 with c_T^2 = {f['cT2']:g}: the system is d_t^2 h = 0 (a Jordan block, linear growth), not strongly hyperbolic; also DETERMINED fails (nullity {f['nullity']}: the relative time diffeo and the longitudinal spatial diffeo are unbroken at quadratic order, helicity-0 undetermined).")
open(os.path.join(HERE, "CFG242_B_verdict.out"), "w").write("\n".join(L) + "\n")
json.dump(dict(route="B"), open(os.path.join(HERE, "CFG242_B_verdict.json"), "w"))
