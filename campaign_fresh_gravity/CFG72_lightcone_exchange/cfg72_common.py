#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg72_common -- shared helpers for CFG72 (light-cone exchange).  The repository is only READ (CFG44 Bcommon, CFG7_common, CFG70's committed
results JSON); every output goes to this scratch directory.  Units: kpc, km/s, Msun; G = 4.30091727e-6 kpc (km/s)^2/Msun (Bcommon);
a0 = 9.3603e-11 m/s^2 canonical = 2888.3 (km/s)^2/kpc.  kappa = 1/2 is FITTED; nothing here fits anything.
"""
import os, sys, math, json, time
import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
CFG = os.path.join(REPO, "campaign_fresh_gravity")
sys.path.insert(0, os.path.join(CFG, "CFG44_fluid_target"))
sys.path.insert(0, CFG)
from Bcommon import (G, A0, A0_SI, KPC_M, OMEGA_C_OVER_B, point_mass, exp_sphere, freeman_disc, nu_p2)   # noqa: E402  read-only
import CFG7_common as C7                                                                               # noqa: E402  read-only

C_KMS = 299792.458
GYR_PER_KPC_KMS = KPC_M / 1e3 / 3.15576e16           # 1 kpc/(km/s) in Gyr (0.9778)
H0_KMS_KPC = 67.36 / 1e3
OM, HH, DELTA_TA48 = 0.3153, 0.6736, 11.81           # CFG48's convention
RHOC0_MPC = 2.775e11 * HH ** 2
CFG70_JSON = os.path.join(CFG, "CFG70_memory_kernel_exchange", "cfg70_memory_kernel_exchange_results.json")


def r_M_kpc(Mb):
    return math.sqrt(G * Mb / A0)


def r_ta48_kpc(Mb):
    Mcol = Mb * (1.0 + OMEGA_C_OVER_B)
    return 1e3 * (3.0 * Mcol / (4.0 * math.pi * OM * RHOC0_MPC * DELTA_TA48)) ** (1.0 / 3.0)


def r_ta_comm_kpc(Mb):
    """B's committed r_ta (CFG4's r_ta_law, kernel nu_mono, canonical footing, z = 0)."""
    return 1e3 * float(C7.r_ta_law(Mb, C7.A0["canonical"], C7.nu_mono, 1.0))


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
