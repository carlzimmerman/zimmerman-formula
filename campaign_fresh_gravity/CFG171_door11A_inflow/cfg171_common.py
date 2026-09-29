#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg171_common -- shared machinery for CFG171 (door 11A, the radial-inflow CONTROL reading of the owner's flowing Lambda-vacuum).

Frozen criteria: FROZEN_QUESTION.md (written before any script).  Nothing in the repository outside this directory is edited.
CFG44's Bcommon is imported READ-ONLY for G, a0 (canonical), the kernels (P2 = sqrt(1 + 1/y), nu_mono) and the baryon profiles.

Units for galaxy work: kpc, km/s, Msun, G = 4.30091727e-6 kpc (km/s)^2/Msun (Bcommon).  SI for the Solar System.
kappa = 1/2 is FITTED.  The Lambda tie per footing: H_foot = Z a0/c, Z = sqrt(32 pi/3) = 5.7888 (identical to kappa = 1/2);
canonical a0 = 9.3603e-11 m/s^2 -> H_Lambda; alt a0 = 1.1312e-10 -> H_0 (rho_total / c H_0 footing).  Nothing is fitted.
"""
import os, sys, math, json, time
import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG44_fluid_target"))
import Bcommon as B  # noqa: E402  (read-only import)

G = B.G                     # kpc (km/s)^2 / Msun
KPC_M = B.KPC_M
C_KMS = 299792.458
C_SI = 299792458.0
G_SI = 6.67430e-11
MSUN_KG = 1.98847e30
Z = math.sqrt(32.0 * math.pi / 3.0)                           # = c H_Lambda / a0 at kappa = 1/2
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}        # CFG7_common.A0_SI (both footings)
KAPPA = 0.5                                                   # FITTED


def a0_kpc(foot):
    """a0 in (km/s)^2/kpc."""
    return A0_SI[foot] * KPC_M / 1e6


def H_si(foot):
    """the footing's Lambda-tied expansion rate, H = Z a0 / c  (s^-1)."""
    return Z * A0_SI[foot] / C_SI


def H_kpc(foot):
    """H in km/s/kpc."""
    return H_si(foot) * KPC_M / 1e3


def rho_lambda_si(foot):
    """rho_Lambda (kg/m^3) = 3 H^2/(8 pi G) with the footing's H."""
    return 3.0 * H_si(foot) ** 2 / (8.0 * math.pi * G_SI)


def rho_lambda_kpc(foot):
    """rho_Lambda in Msun/kpc^3."""
    return rho_lambda_si(foot) * KPC_M ** 3 / MSUN_KG


def r_M(Mb, foot="canonical"):
    return math.sqrt(G * Mb / a0_kpc(foot))


# ---------------------------------------------------------------------------------------------------------------- kernels
def nu_p2(y):
    return B.nu_p2(y)


def nu_mono(y):
    return B.nu_mono(y)


def nu_simple(y):
    """the 'simple' nu = 1/2 + sqrt(1/4 + 1/y) (the DOOR11 file's parenthetical; reported, never scored)."""
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def nu_alpha2(y):
    """alpha = 2 kernel of the n-family, nu = [(1 + sqrt(1 + 4/y^2))/2]^(1/2)  (MUTATE control for G5 only)."""
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y ** 2)))


KERNELS = {"P2": nu_p2, "nu_mono": nu_mono, "simple": nu_simple, "alpha2": nu_alpha2}

HEXP = {1e9: 2.0, 1e10: 3.0, 1e11: 4.0, 1e12: 5.0}           # CFG118's exponential-sphere scale lengths (kpc)
MASSES = (1e9, 1e10, 1e11, 1e12)


def profiles(Mb, foot="canonical"):
    """point mass, exp sphere (CFG118 h, primary) and exp sphere (h = 0.5 r_M, CFG124, secondary)."""
    return {"point": B.point_mass(Mb), "exp_hCFG118": B.exp_sphere(Mb, HEXP[Mb]), "exp_h0.5rM": B.exp_sphere(Mb, 0.5 * r_M(Mb, foot))}


# ---------------------------------------------------------------------------------------------------------------- report
class Report:
    def __init__(self, slug, mode):
        self.slug = slug + ("" if mode is None else f"_MUTATE_{mode}")
        self.mode = mode
        self.lines, self.checks, self.numbers, self.t0 = [], [], {}, time.time()

    def P(self, s=""):
        print(s, flush=True)
        self.lines.append(str(s))

    def banner(self, s):
        self.P("\n" + "=" * 118 + "\n" + s + "\n" + "=" * 118)

    def check(self, name, detail, ok, load_bearing=True):
        self.checks.append(dict(name=name, detail=str(detail), ok=bool(ok), load_bearing=load_bearing))
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")

    def num(self, k, v):
        self.numbers[k] = v

    def write(self):
        lb = [c for c in self.checks if c["load_bearing"]]
        nf = sum(not c["ok"] for c in lb)
        self.P(f"\n  {sum(c['ok'] for c in self.checks)}/{len(self.checks)} checks pass; load-bearing failures: {nf}   ({time.time() - self.t0:.1f} s)")

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

        json.dump(clean(dict(slug=self.slug, mode=self.mode, load_bearing_failures=nf, checks=self.checks, numbers=self.numbers)),
                  open(os.path.join(HERE, self.slug + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, self.slug + ".out"), "w").write("\n".join(self.lines) + "\n")
        return nf


def parse_mode(argv, allowed):
    """--mutate <mode> ; returns None for the main run."""
    if "--mutate" in argv:
        i = argv.index("--mutate")
        m = argv[i + 1] if i + 1 < len(argv) else allowed[0]
        if m not in allowed:
            raise SystemExit(f"unknown mutate mode {m}; allowed {allowed}")
        return m
    return None
