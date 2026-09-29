#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg70_common -- shared helpers for CFG70 (memory-kernel exchange).  Nothing in the repository is edited; the repository is only READ
(Gcommon/Bcommon for cross-checks, CFG7_common for B's committed r_ta).  Outputs go to this scratch directory.

Units: kpc, km/s, Msun; G = 4.30091727e-6 kpc (km/s)^2/Msun (Bcommon); a0 = 9.3603e-11 m/s^2 (canonical) = 2888.3 (km/s)^2/kpc.
kappa = 1/2 is FITTED; nothing here fits anything.
"""
import os, sys, math, json, time
import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

G = 4.30091727e-6
KPC_M = 3.0856775814913673e19
A0_SI = 9.3603e-11
A0 = A0_SI * KPC_M / 1e6                      # (km/s)^2/kpc
C_KMS = 299792.458
GYR_PER_KPC_KMS = KPC_M / 1e3 / 3.15576e16    # 1 kpc/(km/s) in Gyr (0.9778)
H0_KMS_KPC = 67.36 / 1e3                      # (km/s)/kpc (h = 0.6736, CFG48/CFG4)
OMEGA_C_OVER_B = 0.1200 / 0.02237
OM, HH, DELTA_TA48 = 0.3153, 0.6736, 11.81    # CFG48's convention (Gcommon)
RHOC0_MPC = 2.775e11 * HH ** 2


def r_M_kpc(Mb):
    return math.sqrt(G * Mb / A0)


def r_ta48_kpc(Mb):
    """CFG48's r_ta (Gcommon.r_ta_kpc): turnaround radius of the cosmic-share collapse mass M_b(1 + Omega_c/Omega_b)."""
    Mcol = Mb * (1.0 + OMEGA_C_OVER_B)
    return 1e3 * (3.0 * Mcol / (4.0 * math.pi * OM * RHOC0_MPC * DELTA_TA48)) ** (1.0 / 3.0)


class Report:
    def __init__(self, slug, mutate_tag):
        self.slug = slug + (("_MUTATE" + (("_" + mutate_tag) if mutate_tag not in ("", "1") else "")) if mutate_tag else "")
        self.lines, self.checks, self.numbers, self.verdicts, self.t0 = [], [], {}, {}, time.time()

    def P(self, s=""):
        print(s, flush=True)
        self.lines.append(str(s))

    def banner(self, s):
        self.P("\n" + "=" * 118 + "\n" + s + "\n" + "=" * 118)

    def check(self, name, detail, ok, load_bearing=True):
        self.checks.append(dict(name=name, detail=str(detail), ok=bool(ok), load_bearing=load_bearing))
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")

    def verdict(self, gate, status, why):
        self.verdicts[gate] = dict(status=status, why=why)
        self.P(f"  >> {gate}: {status} -- {why}")

    def num(self, k, v):
        self.numbers[k] = v

    def write(self):
        lb = [c for c in self.checks if c["load_bearing"]]
        nf = sum(not c["ok"] for c in lb)
        self.P(f"\n  {sum(c['ok'] for c in self.checks)}/{len(self.checks)} checks pass; load-bearing failures: {nf}   ({time.time() - self.t0:.0f} s)")

        def clean(o):
            if isinstance(o, dict):
                return {str(k): clean(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)):
                return [clean(v) for v in o]
            if isinstance(o, (np.floating, float)):
                return float(o) if np.isfinite(o) else str(o)
            if isinstance(o, np.integer):
                return int(o)
            if isinstance(o, (np.bool_, bool)):
                return bool(o)
            if isinstance(o, np.ndarray):
                return clean(o.tolist())
            return o if isinstance(o, (int, str)) or o is None else str(o)

        json.dump(clean(dict(slug=self.slug, load_bearing_failures=nf, checks=self.checks, verdicts=self.verdicts, numbers=self.numbers)),
                  open(os.path.join(HERE, self.slug + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, self.slug + ".out"), "w").write("\n".join(self.lines) + "\n")
        return nf
