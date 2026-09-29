# -*- coding: utf-8 -*-
"""cfg172_common -- shared machinery for lane CFG172 (Door 11C).  Read-only import of CFG44's Bcommon (kernels, exponential sphere).
Repo root: env ZF_REPO, else walk up from this file looking for campaign_fresh_gravity/.  Printed as <repo>.  kappa = 1/2 is FITTED.
Units: kpc, km/s, Msun unless a name ends in _SI.  Nothing is scanned to make a gate pass."""
import os, sys, math, json, time
import numpy as np
from scipy.optimize import brentq

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    r = os.environ.get("ZF_REPO")
    if r and os.path.isdir(os.path.join(r, "campaign_fresh_gravity")):
        return os.path.abspath(r)
    d = HERE
    for _ in range(8):
        if os.path.isdir(os.path.join(d, "campaign_fresh_gravity", "CFG44_fluid_target")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("set ZF_REPO to the repository root")


REPO = find_repo()
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG44_fluid_target"))
import Bcommon as BC  # noqa: E402  (read-only)

G = BC.G                                  # kpc (km/s)^2 / Msun
KPC_M = BC.KPC_M
C_KMS = 299792.458
C_SI = 299792458.0
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOT = list(A0_SI)
A0 = {f: A0_SI[f] * KPC_M / 1e6 for f in FOOT}   # (km/s)^2/kpc
MASSES = [1e9, 3e9, 1e10, 3e10, 1e11, 3e11, 1e12]
H_EXP = 2.0                                # kpc
XGRID = np.logspace(-1, math.log10(30.0), 300)
OM, HH, OB_H2, OC_H2, OL = 0.3153, 0.6736, 0.02237, 0.1200, 0.6847
H0_SI = 100 * HH * 1e3 / 3.0856775814913673e22  # s^-1


def P(*a):
    print(*a, flush=True)


def rel(path):
    return "<repo>/" + os.path.relpath(path, REPO) if path.startswith(REPO) else os.path.basename(path)


def nu_p2(y):
    """CFG44's P2 (Bcommon): g = sqrt(g_N^2 + a0 g_N), nu = sqrt(1 + 1/y)."""
    return np.sqrt(1.0 + 1.0 / np.maximum(y, 1e-300))


def nu_simple(y):
    """the 'simple' function nu = 1/2 + sqrt(1/4 + 1/y) (the form quoted in the Door-11 brief; NOT CFG44's P2)."""
    return 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(y, 1e-300))


nu_mono = BC.nu_mono
KERNELS = {"P2": nu_p2, "nu_mono": nu_mono, "simple": nu_simple}


def q_of_yg(nu, yg):
    """q = 1 - mu, mu(y_g) = y_N/y_g with y_g = nu(y_N) y_N (algebraic law mu g = g_N), by inverting y_g(y_N)."""
    yg = np.atleast_1d(np.asarray(yg, float))
    out = np.empty_like(yg)
    for i, y in enumerate(yg):
        f = lambda ly: math.exp(ly) * float(nu(math.exp(ly))) - y
        yN = math.exp(brentq(f, -40, 40, xtol=1e-14))
        out[i] = 1.0 - yN / y
    return out


def M_enc_exp(M, r, h=H_EXP):
    s = np.asarray(r, float) / h
    return M * (1.0 - (1.0 + s + s * s / 2.0) * np.exp(-s))


def rho_exp(M, r, h=H_EXP):
    return M / (8 * math.pi * h ** 3) * np.exp(-np.asarray(r, float) / h)


def rM_kpc(M, a0):
    return math.sqrt(G * M / a0)


def profile_gN(M, prof, a0):
    """returns r (kpc), g_N (km/s)^2/kpc on the x-grid of the TOTAL mass M (x = r / r_M)."""
    r = XGRID * rM_kpc(M, a0)
    Menc = np.full_like(r, M) if prof == "point" else M_enc_exp(M, r)
    return r, G * Menc / r ** 2


class Run:
    def __init__(self, slug):
        self.slug = slug
        self.mut = os.environ.get("MUTATE", "")
        self.checks = []
        self.out = {"lane": slug, "mutate": self.mut, "checks": {}, "numbers": {}, "verdicts": {}}
        self.t0 = time.time()
        P(f"== {slug}  MUTATE={self.mut or 'off'}  repo=<repo>")

    def check(self, name, measured, ok, load_bearing=True):
        ok = bool(ok)
        self.checks.append((name, ok, load_bearing))
        self.out["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
        P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")

    def verdict(self, key, status, why):
        self.out["verdicts"][key] = {"status": status, "why": why}
        P(f"  >> {key}: {status}  ({why})")

    def finish(self, bite=None):
        """main: exit 1 iff any check failed.  MUTATE: exit 1 iff the named control bit (bite True)."""
        suffix = f"_MUTATE_{self.mut}" if self.mut else ""
        path = os.path.join(HERE, self.slug + suffix + "_results.json")
        self.out["runtime_s"] = round(time.time() - self.t0, 1)
        if self.mut:
            self.out["control_bit"] = bool(bite)
        json.dump(self.out, open(path, "w"), indent=1, default=str)
        nfail = sum(1 for _, ok, lb in self.checks if not ok)
        P(f"== {self.slug}: {len(self.checks)-nfail}/{len(self.checks)} checks pass; runtime {self.out['runtime_s']} s; wrote {os.path.basename(path)}")
        if self.mut:
            sys.exit(1 if bite else 0)
        sys.exit(1 if nfail else 0)
