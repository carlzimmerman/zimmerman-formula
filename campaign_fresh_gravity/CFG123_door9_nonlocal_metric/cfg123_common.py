#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg123_common -- shared helpers for CFG123 (Door 9: Deser-Woodard / Maggiore-Mancarella nonlocal metric gravity).
Frozen criteria: CFG123_FROZEN_CRITERIA.md (committed e8b9fbcdf, unchanged).  kappa = 1/2 is FITTED.  Nothing here says the theory is closed.

Path independence: the repository root is ZF_REPO if set, else the nearest ancestor of this file that contains `campaign_fresh_gravity/`.
The repository is only READ (Bcommon, CFG7_common for r_ta); every output is written beside the script that produces it.

Units: SI for the cosmology/tie parts (c, G, H0), kpc-km/s-Msun for the galaxy parts (as CFG44 Bcommon).
"""
import os, sys, math, json, time
import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    z = os.environ.get("ZF_REPO")
    if z and os.path.isdir(os.path.join(z, "campaign_fresh_gravity")):
        return os.path.abspath(z)
    d = HERE
    for _ in range(8):
        if os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("cfg123: cannot locate the repository; set ZF_REPO to the repository root")


REPO = find_repo()
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG44_fluid_target"))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))

# ---------------------------------------------------------------------------------------------------- constants (SI)
C_SI = 299792458.0
G_SI = 6.67430e-11
MSUN = 1.98847e30
MPC = 3.0856775814913673e22
KPC = MPC / 1e3
H0_KMS_MPC = 67.36                                     # frozen: H0 = 67.36 km/s/Mpc
H0_SI = H0_KMS_MPC * 1e3 / MPC                         # 1/s
OM = 0.3153                                            # frozen: Omega_m = 0.3153
HH = 0.6736
OR_H2 = 4.15e-5                                        # Omega_r h^2 (photons + massless nu); declared, radiation is negligible at z<=1e3 checks
OR = OR_H2 / HH ** 2
OL_CANON = 0.6847                                      # the value a0 = 9.3603e-11 uses
A0_FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
KAPPA = 0.5
Z_STAR = 1090.0


def a0_from_tie(kappa=KAPPA, OL=OL_CANON, H0=H0_SI):
    """a0 = kappa c sqrt(G rho_Lambda) = kappa c H0 sqrt(3 Omega_Lambda / 8 pi)."""
    return kappa * C_SI * H0 * math.sqrt(3.0 * OL / (8.0 * math.pi))


# ---------------------------------------------------------------------------------------------------- the frozen G1 grid
MASSES = [1e9, 1e10, 1e11, 1e12]
XGRID = [0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 30.0]
H_EXP_KPC = 2.0                                       # CFG44 B1's exponential-sphere scale height (kpc), read from CFG44 B1 (COMPACT/DIFFUSE use h = 2.0)


def rM_m(M_sun, a0):
    return math.sqrt(G_SI * M_sun * MSUN / a0)


# ---------------------------------------------------------------------------------------------------- MUTATE plumbing
def mutate_mode():
    v = os.environ.get("MUTATE", "").strip().lower()
    return "" if v in ("", "0") else ("a" if v == "1" else v)


class Report:
    """same shape as the CFG48/CFG70 reports; check(load_bearing) counts toward the exit code."""

    def __init__(self, slug, mutate_tag=""):
        self.slug = slug + (("_MUTATE_" + mutate_tag) if mutate_tag else "")
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


def finish(R, mutate):
    """exit-code convention of the CFG lanes: the main run exits 0 iff every pre-registered claim holds (a falsified prediction exits 1 and is kept);
    a MUTATE run must exit 1 (the mutation must contradict at least one claim); if it exits 0 the control failed to bite and that is printed."""
    nf = R.write()
    if mutate:
        if nf == 0:
            R.P("  CONTROL FAILURE: the mutation did not contradict any load-bearing claim")
            return 0
        return 1
    return 0 if nf == 0 else 1


# ---------------------------------------------------------------------------------------------------- the RR background (H0 = 1 units)
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


def rr_rhs(x, y, lam, Om=OM, Or=OR):
    """localised RR background in x = ln a, units H0 = 1.  y = (U, U', S, S').  lam = m^2/H0^2.
    Friedmann constraint (E_00 of the localised action, derived in A1_localised_action.py):
       H^2 [3 - lam S - lam S' + (lam/6) S' U'] = 8 pi G rho + (lam/12) U^2 ,   8 pi G rho = 3 (Om a^-3 + Or a^-4)   (H0 = 1)
    scalar equations:  U'' + (3 + zeta) U' = 6 (zeta + 2),   S'' + (3 + zeta) S' = U / h^2,  zeta = H'/H, from d ln h^2 / dx of the constraint."""
    U, Up, S, Sp = y
    Mm = Om * math.exp(-3 * x)
    Rr = Or * math.exp(-4 * x)
    N = 3.0 * (Mm + Rr) + lam / 12.0 * U * U
    D = 3.0 - lam * S - lam * Sp + lam / 6.0 * Sp * Up
    h2 = N / D

    def g(z):
        Spp = -(3 + z) * Sp + U / h2
        Upp = -(3 + z) * Up + 6.0 * (z + 2.0)
        Np = -3.0 * (3 * Mm + 4 * Rr) + lam / 6.0 * U * Up
        Dp = -lam * Sp - lam * Spp + lam / 6.0 * (Spp * Up + Sp * Upp)
        return 0.5 * (Np / N - Dp / D) - z

    g0, g1 = g(0.0), g(1.0)
    z = -g0 / (g1 - g0)
    return [Up, -(3 + z) * Up + 6.0 * (z + 2.0), Sp, -(3 + z) * Sp + U / h2], h2, z


def rr_solve(lam, xi=math.log(1e-6), xf=0.0, dense=True, Om=OM, Or=OR):
    sol = solve_ivp(lambda x, y: rr_rhs(x, y, lam, Om, Or)[0], (xi, xf), [0.0, 0.0, 0.0, 0.0], method="DOP853",
                    rtol=1e-11, atol=1e-14, dense_output=dense)
    return sol


def h2_today(lam, Om=OM, Or=OR):
    sol = rr_solve(lam, dense=False, Om=Om, Or=Or)
    y = sol.y[:, -1]
    return rr_rhs(0.0, y, lam, Om, Or)[1]


def rr_fit_lambda(Om=OM, Or=OR):
    """m^2/H0^2 such that H(a=1) = H0: the one number that replaces Lambda (reading R-A)."""
    f = lambda lam: h2_today(lam, Om, Or) - 1.0
    lo, hi = 1e-3, 3.0
    return brentq(f, lo, hi, xtol=1e-13, rtol=1e-13)


def lcdm_h2(x, Om=OM, Or=OR):
    OLc = 1.0 - Om - Or
    return Om * np.exp(-3 * x) + Or * np.exp(-4 * x) + OLc


_BG = {}


def rr_background(Om=OM, Or=OR):
    """cached: (lam, sol) of the R-A background."""
    key = (Om, Or)
    if key not in _BG:
        lam = rr_fit_lambda(Om, Or)
        _BG[key] = (lam, rr_solve(lam, Om=Om, Or=Or))
    return _BG[key]
