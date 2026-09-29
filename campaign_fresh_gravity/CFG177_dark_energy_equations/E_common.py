# -*- coding: utf-8 -*-
"""Shared helpers for CFG177 (the equations of the dark energy in the committed HT action, and its minimal dynamical promotion).

Conventions: signature (-,+,+,+); in the symbolic work c = 1 and M_P^2 = 1/(8 pi G); rho_vac = M_P^2 Lambda (the vacuum energy density);
eps = kappa^2/(8 pi); P_cap = eps M_P^2 Lambda = a0^2/(8 pi G) (CFG43's tie, POSTULATED there); kappa = 1/2 FITTED (never derived).
MUTATE env var selects a control mode (each script documents its own modes); outputs carry the mode in their names.
Every script writes <name>[_MUTATEk].out and <name>[_MUTATEk]_results.json next to itself and exits 1 if a load-bearing check fails.
Nothing here edits or writes outside this directory; CFG44's Bcommon is imported read-only (bytecode writing disabled first).
"""
import os
import sys
import json
import math
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = int(os.environ.get("MUTATE", "0"))

# SI constants and the program's footings (FP0 charter values, as in CFG43 A_common.py)
G_SI = 6.6743e-11
C_SI = 299792458.0
MSUN = 1.98847e30
KPC_M = 3.0856775814913673e19
AU_M = 1.495978707e11
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}      # m/s^2
RHO_L = 5.8424e-27                                     # kg/m^3 (rho_Lambda, canonical footing)
OMEGA_L = 0.6847
OMEGA_M = 0.3153
KAPPA = 0.5                                            # FITTED
EPS = KAPPA ** 2 / (8 * math.pi)
LAMBDA_SI = 8 * math.pi * G_SI * RHO_L / C_SI ** 2     # 1/m^2
H_LAMBDA = math.sqrt(8 * math.pi * G_SI * RHO_L / 3)   # 1/s  (H_Lambda = H0 sqrt(Omega_L))
H0 = H_LAMBDA / math.sqrt(OMEGA_L)
RHO_FOOT = {"canonical": RHO_L, "alt": RHO_L / OMEGA_L}   # the density each footing's a0 = kappa c sqrt(G rho) reads


class Run:
    def __init__(self, name):
        self.name = name
        tag = "" if MUTATE == 0 else "_MUTATE%d" % MUTATE
        self.stem = os.path.join(HERE, name + tag)
        self._f = open(self.stem + ".out", "w", encoding="utf-8")
        self.results = []
        self.numbers = {}
        self.fail_lb = 0
        self.t0 = time.time()

    def P(self, *a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        self._f.write(s + "\n")
        self._f.flush()

    def banner(self, t):
        self.P("")
        self.P("=" * 118)
        self.P(t)
        self.P("=" * 118)

    def check(self, tag, statement, measured, ok, reading="", load_bearing=True):
        ok = bool(ok)
        self.results.append(dict(tag=tag, ok=ok, load_bearing=load_bearing, statement=statement, measured=str(measured)))
        if (not ok) and load_bearing:
            self.fail_lb += 1
        st = "PASS" if ok else ("FAIL" if load_bearing else "FAIL(reported)")
        self.P("  [%s] %s %s" % (st, tag, statement))
        self.P("         measured: " + str(measured))
        if reading:
            self.P("         reading:  " + reading)

    def num(self, k, v):
        self.numbers[k] = v

    def finish(self):
        n = len(self.results)
        npass = sum(1 for r in self.results if r["ok"])
        self.P("")
        self.P("SUMMARY %s (MUTATE=%d): %d/%d checks pass; load-bearing failures = %d   (%.1f s)" % (
            self.name, MUTATE, npass, n, self.fail_lb, time.time() - self.t0))
        for r in self.results:
            if not r["ok"]:
                self.P("   failed: %s %s" % (r["tag"], "(load-bearing)" if r["load_bearing"] else "(reported)"))
        self._f.close()

        def clean(o):
            if isinstance(o, dict):
                return {str(k): clean(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)):
                return [clean(v) for v in o]
            try:
                import numpy as np
                if isinstance(o, np.generic):
                    o = o.item()
            except Exception:
                pass
            if isinstance(o, float):
                return o if math.isfinite(o) else str(o)
            return o if isinstance(o, (int, str, bool)) or o is None else str(o)

        json.dump(clean(dict(name=self.name, mutate=MUTATE, load_bearing_failures=self.fail_lb, checks=self.results,
                             numbers=self.numbers)), open(self.stem + "_results.json", "w"), indent=1)
        sys.exit(1 if self.fail_lb else 0)


def import_bcommon():
    """CFG44's Bcommon (read-only): P2 and nu_mono kernels, the exponential sphere. Bytecode writing is off (no __pycache__ there)."""
    sys.dont_write_bytecode = True
    p = os.path.join(os.path.dirname(HERE), "CFG44_fluid_target")
    if p not in sys.path:
        sys.path.insert(0, p)
    import Bcommon
    return Bcommon
