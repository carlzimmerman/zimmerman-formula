#!/usr/bin/env python3
"""cfg250_common -- shared machinery for lane CFG250 (a mass-free a0 estimator from rotation-curve SHAPE).

Nothing here is a result.  It holds:
  * a0 on the two footings and the kernels P2 / nu_mono, imported READ-ONLY from campaign_fresh_gravity/CFG4_common.py
    (kappa = 1/2 is FITTED; a0 canonical 9.3603e-11, alt 1.1312e-10 m/s^2);
  * Phi(y) = y nu(y), its inverse, and the point-mass slope s(y) = 1 - 2 dlnPhi/dlny with its inverse y(s), as log-grid tables;
  * E(z) = sqrt(Om (1+z)^3 + 1 - Om), Om = 0.315 (the rival reading a0 x E(z));
  * the in-plane Newtonian field of a razor-thin exponential disc (Freeman 1970), per unit mass;
  * Kretschmer et al. 2021's alpha(x) as quoted verbatim in CFG160 (x = R/R_e - 1, clipped to [0, 4]);
  * a tee that writes a script's own .out (MUTATE=1 -> *_MUTATE.out) plus a results JSON.
No measured KURVS velocity or dispersion is read by this module.
"""
import os
import sys
import json
import math
import builtins

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from scipy.special import i0e, i1e, k0e, k1e

LANE = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.dirname(LANE)
REPO = os.path.dirname(CFGDIR)
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
sys.path.insert(0, CFGDIR)
import CFG4_common as C4                                          # noqa: E402  (read-only import: constants and kernels)

MUTATE = os.environ.get("MUTATE", "0") == "1"
G_SI = C4.G_SI
MSUN = C4.MSUN
KPC = C4.KPC
A0 = dict(C4.A0)                                                  # {'canonical': 9.3603e-11, 'alt': 1.1312e-10}
OM = 0.315
KERNELS = {"P2": C4.nu_p2, "nu_mono": C4.nu_mono}


def E(z, om=OM):
    return np.sqrt(om * (1.0 + np.asarray(z, float)) ** 3 + 1.0 - om)


# ------------------------------------------------------------------------------------------------ Phi, s(y) tables
class Kernel:
    """Phi(y) = y nu(y); s(y) = 1 - 2 dlnPhi/dlny (the point-mass log-slope of V_c^2); inverses by log-grid interpolation."""

    def __init__(self, name, lo=-9.0, hi=9.0, n=18001):
        self.name = name
        nu = KERNELS[name]
        self.lny = np.linspace(lo * math.log(10), hi * math.log(10), n)
        y = np.exp(self.lny)
        self.lnPhi = np.log(y * nu(y))
        if name == "P2":                                          # exact closed forms for P2
            self.dlnPhi = (2 * y + 1) / (2 * (y + 1))
        else:
            self.dlnPhi = np.gradient(self.lnPhi, self.lny)
        self.s = 1.0 - 2.0 * self.dlnPhi
        self.phi_monotone = bool(np.all(np.diff(self.lnPhi) > 0))
        ds = np.diff(self.s)
        self.s_monotone = bool(np.all(ds < 0))
        self.s_max_increase = float(np.max(ds)) if ds.size else 0.0

    def Phi(self, y):
        y = np.asarray(y, float)
        if self.name == "P2":
            return np.sqrt(y * y + y)
        return y * KERNELS[self.name](y)

    def Phi_inv(self, t):
        """y such that Phi(y) = t (t > 0)."""
        t = np.asarray(t, float)
        if self.name == "P2":
            return 0.5 * (np.sqrt(1.0 + 4.0 * t * t) - 1.0)
        return np.exp(np.interp(np.log(np.maximum(t, 1e-300)), self.lnPhi, self.lny))

    def s_of_y(self, y):
        y = np.asarray(y, float)
        if self.name == "P2":
            return -y / (1.0 + y)
        return np.interp(np.log(y), self.lny, self.s)

    def y_of_s(self, s):
        """inverse of s(y) on (-1, 0); returns nan outside the domain (s >= 0: y -> 0, a0 lower limit; s <= -1: y -> inf, upper limit)."""
        s = np.asarray(s, float)
        if self.name == "P2":
            with np.errstate(divide="ignore", invalid="ignore"):
                y = -s / (1.0 + s)
            return np.where((s < 0) & (s > -1), y, np.nan)
        # s decreases with y: interpolate on the reversed arrays
        ss, ly = self.s[::-1], self.lny[::-1]
        out = np.exp(np.interp(s, ss, ly))
        return np.where((s < ss.max()) & (s > ss.min()), out, np.nan)

    def D_of_y(self, y):
        """D(y) = dlnPhi/dlny (1/2 in deep MOND, 1 in Newton)."""
        y = np.asarray(y, float)
        if self.name == "P2":
            return (2 * y + 1) / (2 * (y + 1))
        return np.interp(np.log(y), self.lny, self.dlnPhi)

    def y_of_D(self, D):
        """inverse of D(y); nan outside (D_min, D_max).  The shape-aware estimator: at a radius where the baryons' Newtonian
        log-slope of V_N^2 is s_N, the observed slope s gives D = (1 - s)/(1 - s_N) (s_N = -1 recovers the point mass)."""
        D = np.asarray(D, float)
        if self.name == "P2":
            with np.errstate(divide="ignore", invalid="ignore"):
                y = (2 * D - 1) / (2 * (1 - D))
            return np.where((D > 0.5) & (D < 1.0), y, np.nan)
        m = self.lny < math.log(1e8)
        dd, ly = self.dlnPhi[m], self.lny[m]
        out = np.exp(np.interp(D, dd, ly))
        return np.where((D > dd.min()) & (D < dd.max()), out, np.nan)


# ------------------------------------------------------------------------------------------------ thin exponential disc
def g_disc_unit(R_kpc, Rd_kpc):
    """in-plane Newtonian acceleration (m/s^2) of a razor-thin exponential disc of UNIT mass (1 Msun) at R (Freeman 1970):
    V^2 = (2 G M / R_d) y^2 [I0 K0 - I1 K1], y = R / (2 R_d); g = V^2 / R."""
    R = np.maximum(np.asarray(R_kpc, float), 1e-6)
    y = R / (2.0 * Rd_kpc)
    br = i0e(y) * k0e(y) - i1e(y) * k1e(y)                        # the exponential scalings cancel in each product
    V2 = 2.0 * G_SI * MSUN / (Rd_kpc * KPC) * y * y * br
    return V2 / (R * KPC)


def g_point_unit(R_kpc):
    R = np.maximum(np.asarray(R_kpc, float), 1e-6)
    return G_SI * MSUN / (R * KPC) ** 2


def g_sphere_unit(R_kpc, Rd_kpc):
    """the 'spherical shortcut' used by CFG140: G M(<R)/R^2 with the thin disc's enclosed mass fraction."""
    R = np.maximum(np.asarray(R_kpc, float), 1e-6)
    q = R / Rd_kpc
    return G_SI * MSUN * (1.0 - np.exp(-q) * (1.0 + q)) / (R * KPC) ** 2


def gN_baryons(R_kpc, Mstar, mu, Rd, Rgas_over_Rd=2.0, geom="disc"):
    """stars (exponential, R_d) + gas (exponential, Rgas_over_Rd x R_d, mass mu x M*)."""
    if geom == "disc":
        return Mstar * g_disc_unit(R_kpc, Rd) + mu * Mstar * g_disc_unit(R_kpc, Rgas_over_Rd * Rd)
    if geom == "sphere":
        return Mstar * g_sphere_unit(R_kpc, Rd) + mu * Mstar * g_sphere_unit(R_kpc, Rgas_over_Rd * Rd)
    if geom == "point":
        return (1.0 + mu) * Mstar * g_point_unit(R_kpc)
    raise ValueError(geom)


def shape_unit(R_kpc, Rd, mu, Rgas_over_Rd=2.0):
    """the baryonic field SHAPE (per unit total mass): what the disc-shape estimator assumes; normalisation-free."""
    return (g_disc_unit(R_kpc, Rd) + mu * g_disc_unit(R_kpc, Rgas_over_Rd * Rd)) / (1.0 + mu)


# ------------------------------------------------------------------------------------------------ pressure support
def alpha_k21(x):
    """Kretschmer et al. 2021 Table 1 (gas, disc), as quoted verbatim in CFG160: alpha = -0.146 x^2 + 1.204 x + 1.475,
    x = R/R_e - 1, clipped to the fitted range [0, 4]."""
    x = np.clip(np.asarray(x, float), 0.0, 4.0)
    return -0.146 * x * x + 1.204 * x + 1.475


def pressure_term(R_kpc, sigma_kms, Rd, presc, Reff=None):
    """the asymmetric-drift term added to V^2 (km/s)^2 for a constant sigma: 'k<num>' -> k sigma^2 R/R_d;
    'K21x<scale>' -> scale x alpha(R/R_eff - 1) sigma^2; 'none' -> 0."""
    R = np.asarray(R_kpc, float)
    if presc == "none":
        return np.zeros_like(R)
    if presc.startswith("k"):
        return float(presc[1:]) * sigma_kms ** 2 * R / Rd
    if presc.startswith("K21x"):
        Re = 1.68 * Rd if Reff is None else Reff
        return float(presc[4:]) * alpha_k21(R / Re - 1.0) * sigma_kms ** 2
    raise ValueError(presc)


# ------------------------------------------------------------------------------------------------ output harness
class Tee:
    def __init__(self, slug):
        suf = "_MUTATE" if MUTATE else ""
        self.out_path = os.path.join(LANE, f"{slug}{suf}.out")
        self.json_path = os.path.join(LANE, f"{slug}{suf}_results.json")
        self._f = builtins.open(self.out_path, "w", encoding="utf-8")
        self._stdout = sys.stdout
        sys.stdout = self
        self.checks = []
        self.numbers = {}

    def write(self, t):
        self._stdout.write(t)
        self._f.write(t)

    def flush(self):
        self._stdout.flush()
        self._f.flush()

    def banner(self, t):
        print("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)

    def check(self, name, measured, ok, load_bearing=True):
        ok = bool(ok)
        self.checks.append({"name": name, "measured": str(measured), "ok": ok, "load_bearing": load_bearing})
        print(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
        return ok

    def finish(self):
        nlb = sum(1 for c in self.checks if c["load_bearing"] and not c["ok"])
        npass = sum(1 for c in self.checks if c["ok"])
        with builtins.open(self.json_path, "w", encoding="utf-8") as fh:
            json.dump({"mutate": MUTATE, "checks": self.checks, "numbers": _jclean(self.numbers)}, fh, indent=1)
        print(f"\n  {npass}/{len(self.checks)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(self.json_path)}")
        rc = 1 if nlb else 0
        print(f"rc = {rc}")
        sys.stdout = self._stdout
        self._f.close()
        return rc


def _jclean(o):
    if isinstance(o, dict):
        return {str(k): _jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jclean(v) for v in o]
    if isinstance(o, np.ndarray):
        return _jclean(o.tolist())
    if isinstance(o, (np.floating, float)):
        o = float(o)
        return o if math.isfinite(o) else str(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o
