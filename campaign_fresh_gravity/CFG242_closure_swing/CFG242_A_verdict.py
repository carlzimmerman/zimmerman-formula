#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG242_A_verdict -- aggregation only (no physics): route A (L14a) gate table from the committed main results of the A scripts.  Never pooled with route B."""
import os, sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG242_common as C
HERE = C.HERE
def J(n):
    return json.load(open(os.path.join(HERE, f"CFG242_{n}.json")))
g0, g3, g4, g5, g1 = J("A_g0_legality"), J("A_g3_exchange"), J("A_g4_ledger"), J("A_g5_solar_stability"), J("A_g1_target")
L = []
def P(s=""):
    s = C.scrub(s); print(s); L.append(s)
P("ROUTE A (L14a): a causal ownership latch with a vacuum-funded exchange.  Cells cite their script.  MAIN = the frozen stop-rule verdicts; POST-HOC = a labelled continuation after the stop.")
P("")
P("arm A1 (strict; iota = 0, r = 1; kernel time free):")
P("  controls PASS (CFG242_A_controls.py) | G4 FAIL (tau_bar scanned, untied; CFG242_A_g4_ledger.py) -> STOP (frozen order puts G4 before G3) | G3 strict FAIL (reaction 22.5 g_law, energy 23-318 x orbital; CFG242_A_g3_exchange.py, evaluated anyway) | G5, G1, G2 NOT ADDRESSED")
P("arms A2 and A3 (funded; iota = 0 / inhibitor):")
v = g0["numbers"]["verdicts"]
P(f"  G0 legality (frozen E3): {v[[k for k in v][0]]['status']} -- {v[[k for k in v][0]]['why']}   -> STOP")
P("  G4, G3 funded, G5, G1, G2: NOT ADDRESSED in the MAIN run (stop rule at G0)")
P("Gate cells by script (each tagged MAIN or POST-HOC; POST-HOC = a labelled continuation after the stop, frozen equations with the E3 defect set aside, NOT a result of the frozen class):")
for src, nm in ((g4, "G4 (g4_ledger)"), (g3, "G3 (g3_exchange)"), (g5, "G5 (g5_solar_stability)"), (g1, "G1 (g1_target)")):
    for k, vv in src["numbers"].get("verdicts", {}).items():
        tag = "MAIN (arm A1, own gate)" if ("(main)" in k or "strict" in k) else ("MAIN (selectivity; G1 not addressed)" if "G1" in k else "POST-HOC")
        P(f"  [{tag}] {k}: {vv['status']} -- {vv['why']}")
P("")
P("BINDING FAILURE (route A, main): G0 legality, row B3: under the frozen latch equation E3 a bound shell after its own turnaround has n(t_ff) = %.3f and min n(t >= t_ff) = %.3f (line: >= 0.99 within one free-fall time and stays); the decay term acts whenever theta_b >= 0 (a static bound system has no memory); causality C1 (c_adv 0) and the mediator C2 pass, bound-only B1, B2, B4 pass." % (g0["numbers"]["B3"]["n_at_tff"], g0["numbers"]["B3"]["n_min_after_tff"]))
open(os.path.join(HERE, "CFG242_A_verdict.out"), "w").write("\n".join(L) + "\n")
json.dump(dict(route="A"), open(os.path.join(HERE, "CFG242_A_verdict.json"), "w"))
