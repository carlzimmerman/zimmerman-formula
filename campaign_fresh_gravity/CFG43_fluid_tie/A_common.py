# -*- coding: utf-8 -*-
"""Shared helpers for the attack_A scripts (Gap 3: a0-Lambda tie acting on the fluid's stress cap).

Conventions (all scripts):  c = 1;  Mp2 = 1/(8 pi G);  rho_Lambda = Mp2 * Lambda;  kappa = 1/2 is FITTED (never derived);
eps = kappa^2/(8 pi);  P_cap = a0^2/(8 pi G) = eps * Mp2 * Lambda = (kappa^2/8 pi) rho_Lambda c^2.
MUTATE env var: 0 (default), 1 (multiplier replaced by a dynamical scalar), 2 (tie dropped: cap independent of Lambda).
Every script writes its own .out next to itself (name carries the MUTATE mode) and exits rc=1 if a load-bearing check failed.
"""
import os
import sys
import math

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = int(os.environ.get("MUTATE", "0"))

# footings from the program's charter (FP0): canonical / alt a0 in m/s^2; rho_Lambda in kg/m^3
G_SI = 6.6743e-11
C_SI = 299792458.0
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
RHO_L = 5.8424e-27
KAPPA = 0.5                      # FITTED
EPS = KAPPA ** 2 / (8 * math.pi)
MSUN = 1.98847e30
PC = 3.0856775814913673e16       # m
MPC = 3.0856775814913673e22
MSUN_PC3 = MSUN / PC ** 3
MSUN_PC2 = MSUN / PC ** 2


class Run:
    def __init__(self, name):
        self.name = name
        tag = "" if MUTATE == 0 else "_MUTATE%d" % MUTATE
        self.path = os.path.join(HERE, name + tag + ".out")
        self._f = open(self.path, "w", encoding="utf-8")
        self.results = []
        self.fail_lb = 0

    def P(self, *a):
        s = " ".join(str(x) for x in a)
        print(s)
        self._f.write(s + "\n")
        self._f.flush()

    def banner(self, t):
        self.P("")
        self.P("=" * 118)
        self.P(t)
        self.P("=" * 118)

    def check(self, tag, statement, measured, ok, reading="", load_bearing=True, label=""):
        ok = bool(ok)
        self.results.append((tag, ok, load_bearing))
        if (not ok) and load_bearing:
            self.fail_lb += 1
        st = "PASS" if ok else ("FAIL" if load_bearing else "FAIL(reported)")
        self.P("  [%s] %s%s" % (st, tag + " ", ("[" + label + "] ") if label else "") + statement)
        self.P("         measured: " + str(measured))
        if reading:
            self.P("         reading:  " + reading)

    def finish(self):
        n = len(self.results)
        npass = sum(1 for r in self.results if r[1])
        self.P("")
        self.P("SUMMARY %s (MUTATE=%d): %d/%d checks pass; load-bearing failures = %d" % (self.name, MUTATE, npass, n, self.fail_lb))
        for tag, ok, lb in self.results:
            if not ok:
                self.P("   failed: %s %s" % (tag, "(load-bearing)" if lb else "(reported)"))
        self._f.close()
        sys.exit(1 if self.fail_lb else 0)
