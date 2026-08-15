#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t085_kernel_regression.py -- qwenlib pinned against 12 committed numbers (THE CANARY).

PASS: all 12 pins hold.  KILL: any pin off => qwenlib drifted; STOP ALL WORK, escalate.
Not a search.  Direction-of-risk: both (a drifted library corrupts every later task).
Pins' provenance: stage64 (tensor), Amendments 9/10 (asymptotes), stage59/61 (S values),
stage17 (a0(z) off-switch), the committed footings.  PREBUILT as kit infrastructure.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *
import numpy as np

check(abs(float(nu(1.0)) - 1.5820) < 2e-4, "P01 nu(1) = 1.5820")
check(abs(float(y_of_x(1.9)) - 1.2897) < 2e-4, "P02 y_of_x(1.9) = 1.2897")
n0, L0, bpar, bperp = response_tensor(1.9)
check(abs(n0 - 1.4732) < 2e-4 and abs(L0 - 0.3674) < 4e-4, "P03 tensor nu0/L0 = 1.4732/0.3674 [stage64]")
check(abs(bperp - 1.2598) < 2e-4, "P04 B_perp = 1.2598 [stage64]")
check(abs(np.sqrt(nu(y_of_x(1.9))) - 1.2138) < 2e-4, "P05 canonical asymptote 1.2138 [A9: 1.2139]")
x_alt = 1.9 * A0_CAN / A0_ALT
check(abs(np.sqrt(nu(y_of_x(x_alt))) - 1.2586) < 3e-4, "P06 alt asymptote 1.2586 [A9: 1.2592]")
check(abs(float(a0_local_ratio(1.47e4, NU0_HI)) - 0.5990) < 1e-3, "P07 S(dense, ceiling) = 0.5990 [stage59/61]")
check(abs(float(a0_local_ratio(1.47e4, NU0_LO)) - 0.9767) < 1e-3, "P08 S(dense, floor) = 0.9767 [stage59/61]")
check(0.0019 < float(np.sqrt(a0z_ratio_sq(1090, NU0_HI))) < 0.0023, "P09 a0(rec)/a0(0) ~ 0.002 at ceiling [stage17]")
check(0.0058 < float(np.sqrt(a0z_ratio_sq(1090, NU0_LO))) < 0.0062, "P10 a0(rec)/a0(0) ~ 0.006 at floor [stage17]")
check(abs(float(gobs_line(A0_CAN, A0_CAN)) / A0_CAN - 1.6180) < 2e-4, "P11 a0-line at y=1 = golden ratio 1.6180")
check(abs(A0_ALT / A0_CAN - 1.2048) < 2e-4 and Q0_LO == 0.0024 and Q0_HI == 0.0146,
      "P12 footing ratio 1.2048; pinned Q0 band (0.0024, 0.0146) present")

finish("t085")
