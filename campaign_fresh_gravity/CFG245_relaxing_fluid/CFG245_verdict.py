#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG245 verdict: reads the gate outputs in the frozen order (G0, T, C, A, E), applies the STOP RULE and prints which gate bound and the named failure.
Later gates are shown as POST-HOC extras (their file names carry _POSTHOC). Nothing here is closure; kappa = 1/2 stays FITTED; no dark-matter particle; the mass is required."""
import os, sys, json, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG245_common as K

R = K.Report("CFG245_verdict")


def load(slug):
    for suf in ("", "_POSTHOC"):
        p = os.path.join(K.HERE, slug + suf + "_results.json")
        if os.path.exists(p):
            return json.load(open(p)), slug + suf
    return None, None


def main():
    g0, n0 = load("CFG245_G0_target")
    t, nt = load("CFG245_T_timescale")
    c, nc = load("CFG245_C_clusters")
    a, na = load("CFG245_A_supply")
    e, ne = load("CFG245_E_ledger")
    R.banner("CFG245 VERDICT (frozen order G0, T, C, A, E; stop at the first binding FAIL)")
    if not all([g0, t]):
        R.P("  missing gate outputs: run the main scripts first")
        R.finish(); return 1
    ctl_ok = g0.get("controls_ok")
    R.P(f"  G0 controls (C-L1, C-L2): {'PASS' if ctl_ok else 'FAIL (lane UNDEFINED)'}; G0 outcomes: {g0['outcomes']}")
    first = None
    seq = [("T", t, nt), ("C", c, nc), ("A", a, na), ("E", e, ne)]
    for g, d, n in seq:
        if d is None:
            continue
        b = d.get("binding_fail")
        R.P(f"  Gate {g}: {'BINDING FAIL' if b else 'no binding FAIL'}   [{n}]")
        if b and first is None:
            first = g
    R.P("")
    R.P(f"  FIRST BINDING FAIL: Gate {first}")
    if first == "T":
        nm = t["numbers"]["T_G1"]
        R.P("  named failure: T-G1 -- Gamma*tau (favourable bracket tau = t_0) and residual fraction of the passive-infall deviation, per candidate:")
        for f in K.FOOTS:
            R.P("    " + f"{f:10s} " + "; ".join(f"{c_} Gamma*tau = {nm[f'{f}|{c_}']['gt']:.3f}, e = {nm[f'{f}|{c_}']['e']:.3f}" for c_ in K.CAND) +
                f"; Gamma*tau needed for the 10% line = {nm[f'{f}|G-H']['req_G1']:.2f} (= {nm[f'{f}|G-H']['req_G1']/(K.HL*K.T0):.2f} H_Lambda at tau = t_0)")
    posthoc = [g for g, d, n in seq if d is not None and g != first and first is not None and "_POSTHOC" in (n or "")]
    R.P(f"  post-hoc extras (labelled, no verdict depends on them): {', '.join(posthoc) if posthoc else 'none'}")
    allbind = [g for g, d, n in seq if d is not None and d.get("binding_fail")]
    R.P(f"  gates that WOULD bind on their own frozen lines: {', '.join(allbind) if allbind else 'none'}")
    R.finish(dict(first_binding=first, binding_gates=allbind))
    return 0


if __name__ == "__main__":
    sys.exit(main())
