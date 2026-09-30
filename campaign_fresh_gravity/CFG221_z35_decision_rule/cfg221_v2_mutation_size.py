#!/usr/bin/env python3
"""CFG221 v2 POST HOC (written after v2's MUTATE control C3 was seen to FAIL; reported only; no v3 is iterated): how large an injected D multiplier does v2's primary-cell rule need before it stops
reading FLAT-SEPARATED in the noise-free flat-truth mock?  The frozen C3 injected D x 1.5 (+0.176 dex); the marginalised calibration prior (sigma_dust = 0.30 dex on the gas mass) already lets the
gas offset absorb a shift of that size, so the rule's silence there is the calibration prior at work, not an arithmetic fault.  Here D x 1.5, 2, 3, 5 and 10 (+0.18, +0.30, +0.48, +0.70, +1.00 dex)
are injected into the noise-free flat-truth mock at each N and v2's and v1's verdicts are reported (B = 10,000 for v2; v1 at its frozen B = 500).
Run: python3 campaign_fresh_gravity/CFG221_z35_decision_rule/cfg221_v2_mutation_size.py
"""
import os, sys, json
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg221_decision_rule as M
import cfg221_v2 as V

rng = np.random.default_rng(221 + 55)
out = [__doc__.split("Run:")[0].strip(), ""]
out.append(f"{'N':>3s}  " + "  ".join(f"D x {f:<4g}".rjust(24) for f in (1.5, 2, 3, 5, 10)))
out.append("     (each cell: v2 primary-cell status flat/rival -> v2 verdict | v1 verdict)")
for N in V.NG2:
    cells = []
    for f in (1.5, 2, 3, 5, 10):
        mock = M.gen_mock(M.BASE, N, "FLAT", 0.0, 0.0, rng, noise=False)
        mock["gobs"] = mock["gobs"] * f
        v2, _, _, res = V.rule2(mock, "FLAT", "H(z)", V.B2, rng, robust=False)
        v1, _, _ = M.rule(mock, "FLAT", "H(z)", M.NB, rng)
        cells.append(f"{res[(V.PRIM, 'FLAT')][:3]}/{res[(V.PRIM, 'H(z)')][:3]} -> {v2:4s} | {v1:4s}")
    out.append(f"{N:3d}  " + "  ".join(c.rjust(24) for c in cells))
print("\n".join(out))
open(os.path.join(HERE, "cfg221_v2_mutation_size.out"), "w").write("\n".join(out) + "\n")
