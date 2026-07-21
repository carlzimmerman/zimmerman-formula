#!/usr/bin/env python3
"""Minimal test suite for a0kit (run: python3 test_a0kit.py). -O-proof: raises, not assert."""
import a0kit as k, numpy as np
def check(cond,msg):
    if not cond: raise SystemExit(f"FAIL: {msg}")
def approx(a,b,r=1e-6): check(abs(a-b)<=r*abs(b), f"{a} != {b}")
# canonical a0 ~ 9.36e-11
approx(k.a0_from_lambda(), 9.3542e-11, 1e-3)
# Lambda <-> a0 round-trip
approx(k.lambda_from_a0(k.a0_from_lambda()), k.LAMBDA_PLANCK, 1e-3)
# a0-line invert round-trip
a0=k.A0_CANONICAL
approx(k.a0_line(k.g_obs(3e-11,a0),3e-11), a0, 1e-9)
# nu limits: y->inf Newtonian (~1), y->0 deep-MOND (nu>>1)
approx(k.nu(1e12), 1.0, 1e-6); check(k.nu(1e-4)>90, 'deep-MOND nu')
# flat DE => a0 constant
approx(k.a0_of_z(3, -1.0, 0.0)/a0, 1.0, 1e-9)
# evolving DE => decline
check(0.6 < k.a0_of_z(3,-0.84,-0.62)/a0 < 0.8, 'evolving-DE decline')
# BTFR positive, deep-MOND scaling V^4 ~ a0
approx(k.btfr_vflat(1e11*k.MSUN, 2*a0)/k.btfr_vflat(1e11*k.MSUN, a0), 2**0.25, 1e-9)
# both footings distinct, canonical < alt
f=k.footings(); check(f["canonical"] < f["alt"], "footings order")
# canonical hubble route: matches a0_from_lambda to ~1% at Planck-ALONE inputs (chain fork doc'd)
approx(k.a0_from_hubble(67.36, "canonical", Omega_L=0.6847), k.a0_from_lambda(), 3e-3)
# rho_de round-trip: (c/2)sqrt(G rho) == a0
approx((k.C/2)*np.sqrt(k.G*k.rho_de_from_a0(a0)), a0, 1e-12)
# footing typo must RAISE, never silently pick a footing
try:
    k.a0_from_hubble(67.66, "canonicl"); raise SystemExit("FAIL: typo footing did not raise")
except ValueError: pass
print("all a0kit tests PASS")
