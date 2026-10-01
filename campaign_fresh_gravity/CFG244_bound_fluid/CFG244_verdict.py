#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG244 verdict: reads the gate JSONs in the frozen ORDER (H, A, D), applies the STOP RULE (stop at the first binding FAIL; later gates only
as labelled post-hoc extras), and prints the gate table with the named failure.  Run: python3 CFG244_verdict.py (exit 0).
kappa = 1/2 FITTED; no dark-matter particle; the mass is required; nothing here is closure."""
import os, sys, json, math
sys.dont_write_bytecode = True
import CFG244_common as K
R = K.Report("CFG244_verdict"); P = R.P
H = json.load(open(os.path.join(K.HERE, "CFG244_H_satellites_results.json")))["numbers"]
A = json.load(open(os.path.join(K.HERE, "CFG244_A_infall_bound_results.json")))["numbers"]
Dp = os.path.join(K.HERE, "CFG244_D_distinctness_POSTHOC_results.json")
D = json.load(open(Dp))["numbers"] if os.path.exists(Dp) else None
P("CFG244 VERDICT (frozen order H, A, D; stop at the first binding FAIL)\n  repo: <repo>")
hc = H["final_outcome"]; hp = H["primary"]["outcome"]; hr = H["rar_kernel"]["outcome"]
P(f"\nGATE H: outcome class {hc} (P2 kernel {hp}; record RAR kernel {hr}).  H1/H3 would be binding FAILs; H2/H4 are PASS.")
h_binding = hc in ("H1", "H3")
P(f"  -> {'BINDING FAIL' if h_binding else 'PASS (non-binding): '+('the route is a different law from B at satellites' if hc=='H2' else 'AMBIGUOUS: the satellites do not separate the route from B')}; continue to Gate A")
gate = "STOPPED"
if not h_binding:
    a = A["A"]
    P(f"\nGATE A: A1 {'PASS' if a['A1_pass'] else 'FAIL'}, A2 {'PASS' if a['A2_pass'] else 'FAIL'}, A3 {'PASS' if a['A3_pass'] else 'FAIL'} -> {a['gate']}")
    b = A["binding"]
    P(f"  BINDING FAILURE: the bound cold mass's radial scale goes as M^p, p = {', '.join(f'{p:.3f}' for p in b['p_point'])} (q = 0.05, 0.1, 0.2), not 1/2; "
      f"R_s/r_M spread over 1e9-1e12 = {', '.join(f'{s:.2f}' for s in b['spread'])} against 1.22 allowed; C_bound/C_target = "
      f"{b['hl']['0.1|loc'][1][0]:.2f}-{b['hl']['0.1|loc'][1][1]:.2f} at x about 1.1 and {b['hl']['0.1|loc'][2][0]:.2f}-{b['hl']['0.1|loc'][2][1]:.2f} at x about 28 (q = 0.1)")
    gate = a["gate"]
    if gate == "FAIL":
        P("  STOP RULE: the lane stops here (a scoped no-go on the frozen class).  Gate D below is a labelled POST-HOC extra, not a verdict input.")
if D is not None:
    P(f"\nGATE D (POST-HOC extra, run after the stop): {D['verdict']}")
R.write()
