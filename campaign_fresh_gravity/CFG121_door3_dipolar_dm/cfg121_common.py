#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg121_common -- shared machinery for CFG121 (Door 3: dipolar dark matter / gravitational polarisation), PHASE 2.
Frozen criteria: CFG121_FROZEN_CRITERIA.md (committed before any script).  Nothing in the repository is edited.

Path handling: REPO = $ZF_REPO if set, else the nearest ancestor of this file containing
campaign_fresh_gravity/CFG44_fluid_target/Bcommon.py.  If none is found the script prints what it needs and exits 2.
CFG44's Bcommon (kernels, exponential sphere, target ODE) and CFG48's Gcommon (r_ta constants) are imported READ-ONLY.

Units: kpc, km/s, Msun (G = 4.30091727e-6).  a0 = 9.3603e-11 m/s^2 canonical (2888.3 (km/s)^2/kpc); second footing 1.1312e-10.
kappa = 1/2 is FITTED.  Nothing here fits anything, and nothing says the data favour the framework.

DECLARATION (resolved BEFORE any number was seen): the frozen file said the exponential-sphere family is imported
from CFG44's Bcommon "(same scale-length law)".  Bcommon has exp_sphere(M, h) but NO law h(M).  The nearest committed
family is CFG50 D1's line: (M_b, h) = (1e9, 2), (1e10, 3), (1e11, 4), (1e12, 5) kpc.  This module uses h(M) = 2 + (log10 M - 9) kpc,
which reproduces exactly those four points; half-decade masses use the same line.  (Recorded as a gap in the frozen text.)
"""
import os, sys, math, json, time
import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    env = os.environ.get("ZF_REPO")
    cands = [env] if env else []
    p = HERE
    for _ in range(12):
        cands.append(p)
        p = os.path.dirname(p)
    for c in cands:
        if c and os.path.isfile(os.path.join(c, "campaign_fresh_gravity", "CFG44_fluid_target", "Bcommon.py")):
            return c
    print("cfg121: cannot find the repository.  Set ZF_REPO to the repo root (containing campaign_fresh_gravity/CFG44_fluid_target/Bcommon.py).")
    sys.exit(2)


REPO = find_repo()
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG44_fluid_target"))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG48_gap1_switch"))
import Bcommon as _B                                     # noqa: E402  (read-only)
from Bcommon import G, KPC_M, OMEGA_C_OVER_B, nu_p2, nu_mono, exp_sphere, target_fields   # noqa: E402
import Gcommon as _Gc                                    # noqa: E402  (read-only; r_ta constants)
sys.dont_write_bytecode = True

A0_SI = {"canonical": 9.3603e-11, "second": 1.1312e-10}
FOOT = os.environ.get("FOOTING", "canonical")
A0_SIV = A0_SI[FOOT]
A0 = A0_SIV * KPC_M / 1e6                                # (km/s)^2/kpc
MSUN_KG = 1.98841e30
MASSES = [1e9, 1e10, 1e11, 1e12]
MASSES_HALF = [3e9, 3e10, 3e11]
MUTATE = os.environ.get("MUTATE", "")


def h_of_M(M):
    return 2.0 + (math.log10(M) - 9.0)


def rM_of(M, a0=None):
    return math.sqrt(G * M / (A0 if a0 is None else a0))


def xgrid(n=121, lo=0.1, hi=30.0):
    return np.geomspace(lo, hi, n)


# ----------------------------------------------------------------------------------------------- kernels (nu(y), y = g_N/a0)
def nu_simple(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def nu_standard(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    z2 = 0.5 * (y * y + np.sqrt(y ** 4 + 4 * y * y))
    return np.sqrt(z2) / y


KERN = {"P2": nu_p2, "nu_mono": nu_mono, "simple": nu_simple, "standard": nu_standard}


def dnu(nu, y, e=1e-5):
    y = np.asarray(y, float)
    if nu is nu_p2:
        return -1.0 / (2.0 * y * y * nu_p2(y))
    return (nu(y * (1 + e)) - nu(y * (1 - e))) / (2 * y * e)


def hfun(nu, y):
    """h(y) = (nu-1) y = 4 pi G |Pi_eq| / a0   (polarisation in acceleration units, in units of a0)."""
    y = np.asarray(y, float)
    return (nu(y) - 1.0) * y


def dh(nu, y):
    """h'(y) = (nu - 1) + y nu'(y)."""
    return (nu(y) - 1.0) + np.asarray(y, float) * dnu(nu, y)


# ----------------------------------------------------------------------------------------------- baryons and target
def make_profile(M):
    return exp_sphere(M, h_of_M(M))


_TC = {}


def target_for(M, a0=None, xmax=200.0, n=8001):
    """CFG44's target for the exponential sphere of mass M (read-only Bcommon ODE).  Returns dict (r, rho, uN, w, u, g) on a log grid."""
    a0 = A0 if a0 is None else a0
    key = (M, a0, xmax, n)
    if key not in _TC:
        prof = make_profile(M)
        rM = rM_of(M, a0)
        f = target_fields(prof, r0=1e-3 * rM, r1=xmax * rM, n=n, a0=a0)
        f["prof"] = prof
        f["rM"] = rM
        _TC[key] = f
    return _TC[key]


def interp_log(rq, rg, yg):
    return np.exp(np.interp(np.log(rq), np.log(rg), np.log(np.maximum(yg, 1e-300))))


def target_at(M, x, a0=None):
    a0 = A0 if a0 is None else a0
    f = target_for(M, a0)
    r = np.asarray(x, float) * f["rM"]
    rho = interp_log(r, f["r"], f["rho"])
    w = np.interp(np.log(r), np.log(f["r"]), f["w"])
    uN = f["prof"].u(r)
    return dict(r=r, rho=rho, Mc=w / G, Mb=uN / G, uN=uN)


# ----------------------------------------------------------------------------------------------- pol model on exponential sphere
def pol_model(M, x, nu=None, a0=None):
    """bound charge of P = chi(g_b) g_b with 4 pi G chi = nu(g_b/a0) - 1, g_b = G M_b(<r)/r^2, spherical:
       M_pol = (nu-1) M_b ;  rho_pol = M_pol'/(4 pi r^2) (analytic in M_b', numeric in nu').  Returns r, Mb, Mpol, rho_pol, g_model, C_model."""
    a0 = A0 if a0 is None else a0
    nu = nu_p2 if nu is None else nu
    prof = make_profile(M)
    r = np.asarray(x, float) * rM_of(M, a0)
    uN = prof.u(r)
    Mb = uN / G
    rho_b = prof.rho_b(r)
    Mbp = 4 * math.pi * r ** 2 * rho_b
    y = uN / (r ** 2 * a0)
    dy = (G * Mbp / r ** 2 - 2 * uN / r ** 3) / a0
    Mpol = (nu(y) - 1.0) * Mb
    dMpol = (nu(y) - 1.0) * Mbp + Mb * dnu(nu, y) * dy
    rho_pol = dMpol / (4 * math.pi * r ** 2)
    g_model = G * (Mb + Mpol) / r ** 2
    C_model = rho_pol * r ** 3 * g_model
    C_tgt = a0 * Mb / (4 * math.pi)
    return dict(r=r, Mb=Mb, Mpol=Mpol, rho_pol=rho_pol, g_model=g_model, C_model=C_model, C_tgt=C_tgt, y=y, rho_b=rho_b, Mbp=Mbp)


# ----------------------------------------------------------------------------------------------- r_ta in both conventions
def r_ta_cfg48(M):
    return _Gc.r_ta_kpc(M)


def r_ta_committed(M, a0=None, nu=nu_p2):
    """the committed convention (CFG48_REFEREE section 5): r_ta where the law's own enclosed mass, phantom included, falls to
       Delta_ta * rho_bar_m.  Isolated point baryons, P2 (as in the referee's R7 table: 1151, 2047, 3639 kpc for 1e10, 1e11, 1e12)."""
    a0 = A0 if a0 is None else a0
    rho_m = _Gc.OM * _Gc.RHOC0_MPC / 1e9                 # Msun/kpc^3
    from scipy.optimize import brentq

    def f(r):
        y = G * M / (r * r * a0)
        Md = M * float(nu(y))
        return Md / (4.0 / 3.0 * math.pi * r ** 3) - _Gc.DELTA_TA * rho_m
    return brentq(f, 1.0, 1e5)


# ----------------------------------------------------------------------------------------------- report
class Report:
    def __init__(self, slug):
        mode = MUTATE
        self.slug = slug + (f"_MUTATE_{mode}" if mode else "") + ("" if FOOT == "canonical" else "_second")
        self.lines, self.checks, self.numbers, self.verdicts, self.t0 = [], [], {}, {}, time.time()

    def P(self, s=""):
        print(s, flush=True)
        self.lines.append(str(s))

    def banner(self, s):
        self.P("\n" + "=" * 118 + "\n" + s + "\n" + "=" * 118)

    def check(self, name, detail, ok, integrity=True):
        self.checks.append(dict(name=name, detail=str(detail), ok=bool(ok), integrity=integrity))
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if integrity else ' (result)'} {name}\n         {detail}")

    def verdict(self, gate, status, why):
        self.verdicts[gate] = dict(status=status, why=why)
        self.P(f"  >> {gate}: {status} -- {why}")

    def num(self, k, v):
        self.numbers[k] = v

    def finish(self, required_change=None):
        """rc: 0 = integrity ok (main run); 2 = integrity failed; MUTATE run: 1 iff the named headline cells changed as declared vs the main run."""
        integ_fail = [c for c in self.checks if c["integrity"] and not c["ok"]]

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

        rc = 0
        if MUTATE:
            base = self.slug.split("_MUTATE_")[0]
            bp = os.path.join(HERE, base + "_results.json")
            changed = {}
            if os.path.isfile(bp):
                bv = json.load(open(bp)).get("verdicts", {})
                for k, v in self.verdicts.items():
                    if k in bv and bv[k]["status"] != v["status"]:
                        changed[k] = (bv[k]["status"], v["status"])
            self.P(f"\n  MUTATE={MUTATE}: headline cells changed vs the main run: {changed}")
            need = required_change or []
            ok = bool(need) and all(k in changed for k in need)
            self.P(f"  required cells {need}: {'ALL CHANGED -> control works (exit 1)' if ok else 'NOT ALL CHANGED -> CONTROL FAILED (reported; exit 0)'}")
            self.numbers["control_changed"] = changed
            self.numbers["control_ok"] = ok
            rc = 1 if ok else 0
        elif integ_fail:
            rc = 2
        self.P(f"\n  integrity failures: {len(integ_fail)}   ({time.time() - self.t0:.0f} s)   exit {rc}")
        json.dump(clean(dict(slug=self.slug, footing=FOOT, mutate=MUTATE, integrity_failures=len(integ_fail), checks=self.checks,
                             verdicts=self.verdicts, numbers=self.numbers)), open(os.path.join(HERE, self.slug + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, self.slug + ".out"), "w").write("\n".join(self.lines) + "\n")
        sys.exit(rc)
