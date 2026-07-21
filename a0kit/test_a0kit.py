#!/usr/bin/env python3
"""Minimal test suite for a0kit (run: python3 test_a0kit.py)."""
import a0kit as k, numpy as np
def approx(a,b,r=1e-6): assert abs(a-b)<=r*abs(b), f"{a} != {b}"
# canonical a0 ~ 9.36e-11
approx(k.a0_from_lambda(), 9.3542e-11, 1e-3)
# Lambda <-> a0 round-trip
approx(k.lambda_from_a0(k.a0_from_lambda()), k.LAMBDA_PLANCK, 1e-3)
# a0-line invert round-trip
a0=k.A0_CANONICAL
approx(k.a0_line(k.g_obs(3e-11,a0),3e-11), a0, 1e-9)
# nu limits: y->inf Newtonian (~1), y->0 deep-MOND (nu>>1)
approx(k.nu(1e12), 1.0, 1e-6); assert k.nu(1e-4)>90
# flat DE => a0 constant
approx(k.a0_of_z(3, -1.0, 0.0)/a0, 1.0, 1e-9)
# evolving DE => decline
assert 0.6 < k.a0_of_z(3,-0.84,-0.62)/a0 < 0.8
# BTFR positive, deep-MOND scaling V^4 ~ a0
approx(k.btfr_vflat(1e11*k.MSUN, 2*a0)/k.btfr_vflat(1e11*k.MSUN, a0), 2**0.25, 1e-9)
# both footings distinct, canonical < alt
f=k.footings(); assert f["canonical"] < f["alt"]
print("all a0kit tests PASS")
