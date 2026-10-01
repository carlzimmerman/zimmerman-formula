#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG242_A_g1_target -- route A (L14a), G1 and the SELECTIVITY control (frozen plan sections 4.1-4.2, gate order 6).

Under the stop rule G1 is NOT ADDRESSED for every arm of route A as a gate: A1 stopped at G4 (strict arm), A2 and A3 at G0.  What is run here is the ONE frozen
item that is independent of the stop: the selectivity control (MA7), because the frozen file states that Class A cannot pass G1 as P-derived BY CONSTRUCTION
(the exchange target theta^T is SUPPLIED).  Control: the class's static equilibrium (r = 0: theta -> n theta^T(q), E2 at late time) is handed (a) the CFG70 pressure-slaved
P2 target and (b) Verlinde's M_D shape (C_V/C_target = (1 + x)/x, CFG117); if the class reproduces BOTH to rounding it reproduces whatever it is handed: a restatement.
MA7 replaces the target by Verlinde's shape in the 'P2 selected' cell: the cell is False in the main run (restatement) and stays False under MA7: the control does NOT bite
(a declared control failure, kept): the main cell is already the restatement verdict.
"""
import os, sys, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import CFG242_common as C
R = C.Run("CFG242_A_g1_target")
P = R.P
P(__doc__.strip())
x = np.geomspace(0.1, 30, 200)
P2_target = 0.75 * x ** 2 / np.sqrt(1 + x ** 2)
Verl_target = P2_target * (1 + x) / x
def equilibrium(target):
    # late-time static limit of E2 with r = 0: theta = n * thT (exact: r + c(theta - n thT) = 0)
    return 1.0 * target
errP = np.max(np.abs(equilibrium(P2_target) / P2_target - 1))
errV = np.max(np.abs(equilibrium(Verl_target) / Verl_target - 1))
P(f"    max relative deviation of the class's static equilibrium from the target it is handed: P2 {errP:.1e}, Verlinde-shaped {errV:.1e}")
selective = (errP < 1e-6) and (errV > 1e-2)       # selective iff it reproduces P2 but NOT the Verlinde shape
R.check("G1 selectivity: the class reproduces P2 but not a Verlinde-shaped target handed to it ('P2 selected')" + (" [MA7: Verlinde target]" if R.mutate == "MA7" else ""),
        selective, f"errors {errP:.1e} / {errV:.1e}: it reproduces both, so G1 cannot be P-derived for class A", kind="result")
R.verdict("G1 arms A1, A2, A3", "NOT ADDRESSED", "stop rule; and P-derived is impossible by construction (target supplied): any G1 pass would be P-declared / p*")
base = R.main_cells()
if R.mutate == "MA7":
    R.finish([base.get("G1 selectivity: the class reproduces P2 but not a Verlinde-shaped target handed to it ('P2 selected')") is True and selective])
else:
    R.finish()
