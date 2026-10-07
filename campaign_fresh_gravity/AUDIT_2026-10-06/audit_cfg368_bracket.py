#!/usr/bin/env python3
"""Audit (read-only): CFG368's F2/F4 forms fail to solve only because the initial-vacuum bracket [-5, 10] is too narrow.
Re-uses CFG368's own solve/cpl/chi2 code (exec of its definitions) with a wider bracket. Usage: audit_cfg368_bracket.py FORM BRACKET p1,p2,..."""
import os, sys, numpy as np
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "CFG368_cold_de_flow_desi")
src = open(os.path.join(D, "cfg368_cold_de_flow.py")).read().split('s0 = solve("F1"')[0]
src = src.replace("lo, hi = -5.0, 10.0", "lo, hi = -BR, BR").replace('P(f"  chain', 'pass #')
form, BR, ps = sys.argv[1], float(sys.argv[2]), [float(v) for v in sys.argv[3].split(",")]
ns = {"__file__": os.path.join(D, "cfg368_cold_de_flow.py"), "__name__": "audit", "BR": BR}; exec(src, ns)
ch, chi2 = ns["chains"], ns["chi2"]; X0 = {k: chi2(*ch[k], -1.0, 0.0) for k in ch}
for p in ps:
    s = ns["solve"](form, p)
    if s is None: print(form, p, "unsolved"); continue
    c = ns["cpl"](s); d = {k: X0[k] - chi2(*ch[k], c[0], c[1]) for k in ch}
    print(f"{form} p {p:+.4f} rv_ini {s.y[0,0]:+.2e} (w0, wa) ({c[0]:+.3f}, {c[1]:+.3f}) Om_obs {c[2]:.3f}  dchi2 cmb/PP/U3/DY5 " + "/".join(f"{d[k]:+.2f}" for k in ch)
          + f"  preferred(all SN >= 4): {all(d[k] >= 4 for k in ('pantheonplus', 'union3', 'desy5'))}", flush=True)
