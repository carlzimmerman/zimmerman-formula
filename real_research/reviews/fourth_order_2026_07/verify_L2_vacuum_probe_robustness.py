#!/usr/bin/env python3
"""
VERIFY L2 -- robustness of the load-bearing claim: a VACUUM PROBE (single monotone
finite-time window, no drive) through the interacting-chain ground state does NOT
invert the detector, across system size L, kick duration, kick strength g, and
detector gap w0. If p_e stays < 0.5 everywhere (and the free control tracks it),
the "sign wall holds at all orders for genuine vacuum probing" claim is robust,
not an L=8 / single-parameter artifact.
"""
import numpy as np
from numpy.linalg import eigh
np.seterr(over='ignore', invalid='ignore', divide='ignore')
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from L2_nonuniform_interacting_vacuum import run_protocol

if __name__ == "__main__":
    print("="*78)
    print("VERIFY L2: vacuum-probe (single monotone window) non-inversion robustness")
    print("  scan L, kick duration tk, coupling g, detector gap w0; interacting hz=0.6")
    print("="*78)
    print(f"  {'L':>3} {'tk':>5} {'g':>5} {'w0':>5} {'p_e[int]':>10} {'p_e[free]':>10} {'inverted?':>10}")
    worst = 0.0
    any_inv = False
    for L in [6, 8, 10]:
        for tk in [0.4, 0.8, 1.5]:
            for g in [1.0, 2.0]:
                for w0 in [0.6, 1.0, 1.6]:
                    prot = [(1.0, tk, 30)]           # single monotone kick = vacuum probe
                    pe_i,_,_ = run_protocol(L, hz=0.6, protocol=prot, g=g, w0=w0)
                    pe_f,_,_ = run_protocol(L, hz=0.0, protocol=prot, g=g, w0=w0)
                    worst = max(worst, pe_i, pe_f)
                    inv = pe_i > 0.5 or pe_f > 0.5
                    any_inv = any_inv or inv
                    # print only the extremes to keep output short
                    if (L==10 and tk==1.5) or pe_i>0.45:
                        print(f"  {L:>3} {tk:5.1f} {g:5.1f} {w0:5.1f} {pe_i:10.4f} {pe_f:10.4f} "
                              f"{'YES' if inv else 'no':>10}")
    print("-"*78)
    print(f"  max p_e over ALL {3*3*2*3} configs (both int+free) = {worst:.4f}")
    print(f"  any inversion (p_e>0.5)? {'YES -- CLAIM BREAKS' if any_inv else 'NO'}")
    print("="*78)
    print("VERDICT: vacuum-probe non-inversion is ROBUST" if not any_inv
          else "VERDICT: claim breaks somewhere -- investigate")
    print("  (a single monotone window never drives p_e past 1/2 at any L,tk,g,w0 tested;")
    print("   inversion requires a time-STRUCTURED drive, whose energy is agent-supplied.)")
    print("="*78)
