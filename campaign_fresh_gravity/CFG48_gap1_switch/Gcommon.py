#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gcommon -- shared machinery for CFG48 (Gap 1: the switch as a legal action term).  Nothing in the repository is edited.

Units: kpc, km/s, Msun (G = 4.30091727e-6 kpc (km/s)^2/Msun), as in CFG44's Bcommon (imported read-only for G, a0 and the kernels).
a0 = 9.3603e-11 m/s^2 canonical footing = 2888.3 (km/s)^2/kpc.  kappa = 1/2 is FITTED; nothing here fits anything.
Cosmology for r_ta (CFG4's convention): flat, Omega_m = 0.3153, h = 0.6736, z = 0, Delta_ta = 11.81 (mean total-matter overdensity at
turnaround), collapse mass M_col = M_b (1 + Omega_c/Omega_b), the cosmic share (T4/T5).
"""
import os, sys, math, json, time, io, contextlib
import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG44_fluid_target"))
from Bcommon import G, A0, A0_SI, KPC_M, OMEGA_C_OVER_B, nu_p2, nu_mono  # noqa: E402  (read-only import)

OM, HH, DELTA_TA = 0.3153, 0.6736, 11.81
RHOC0_MPC = 2.775e11 * HH ** 2            # Msun / Mpc^3 (critical density today)
FB_COSMIC = 1.0 / (1.0 + OMEGA_C_OVER_B)  # Omega_b / (Omega_b + Omega_c)


def r_ta_kpc(Mb):
    """turnaround radius of the collapse mass M_col = M_b (1 + Omega_c/Omega_b)."""
    Mcol = Mb * (1.0 + OMEGA_C_OVER_B)
    rho_m = OM * RHOC0_MPC
    return 1e3 * (3.0 * Mcol / (4.0 * math.pi * rho_m * DELTA_TA)) ** (1.0 / 3.0)


def r_M_kpc(Mb, a0=A0):
    return math.sqrt(G * Mb / a0)


def P2_dyn_mass(Mb, r, a0=A0):
    """M_dyn(<r) of the point-mass P2 law: g = sqrt(g_N^2 + a0 g_N)  =>  M_dyn = M_b sqrt(1 + (r/r_M)^2)."""
    return Mb * np.sqrt(1.0 + (np.asarray(r, float) / r_M_kpc(Mb, a0)) ** 2)


class Report:
    def __init__(self, slug, mutate):
        self.slug = slug + ("_MUTATE" if mutate else "")
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
        """gate-level status against GATES_FROZEN.md (PASS / FAIL / PARTIAL / OPEN); NOT an exit code."""
        self.verdicts[gate] = dict(status=status, why=why)
        self.P(f"  >> GATE {gate}: {status} -- {why}")

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
            if isinstance(o, (np.integer,)):
                return int(o)
            if isinstance(o, (np.bool_, bool)):
                return bool(o)
            return o if isinstance(o, (int, str)) or o is None else str(o)

        json.dump(clean(dict(slug=self.slug, load_bearing_failures=nf, checks=self.checks, verdicts=self.verdicts, numbers=self.numbers)),
                  open(os.path.join(HERE, self.slug + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, self.slug + ".out"), "w").write("\n".join(self.lines) + "\n")
        return nf


def load_de12():
    """DE12's constants, gate step Wd and transition(), loaded UNEDITED from the committed source (its MUTATE switch forced off, output muted).
    Returns a dict with G, Hz, CS, MS, KPC, Wd, transition, ZS, MBS and the raw namespace."""
    p = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
    src = open(p).read()
    cut = src.split('banner("C1  CONTROL')[0]
    cut = cut.replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
    tail = src.split("# ============================================================================================ the transitions")[1]
    tail = tail.split('banner("C2  CONTROL')[0]
    ns = {"__name__": "de12_loaded", "__file__": p}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(cut + "\n" + tail, p, "exec"), ns)
    return ns
