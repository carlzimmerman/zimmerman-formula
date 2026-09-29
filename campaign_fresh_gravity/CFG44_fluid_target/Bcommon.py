#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bcommon -- shared machinery for the attack-B lane (Gap 2: why does B's cold fluid take the density rho_c g = (a0/3) rhobar_b(<r)?).

Self-contained: nothing is imported from the repository (the kernels are re-implemented from FP1_static_sector.py / CFG4_common.py,
the definitions are cited in each script).  Units: kpc, km/s, Msun.  G = 4.30091727e-6 kpc (km/s)^2 / Msun.
a0 = 9.3603e-11 m/s^2 (canonical footing) -> 2888.3 (km/s)^2/kpc.   kappa = 1/2 is FITTED; nothing here fits anything.

Notation used everywhere:  u(r) = G M_tot(<r) = r^2 g_tot ; u_N(r) = G M_b(<r) = r^2 g_N ; w = u - u_N = G M_c(<r) (the cold fluid).
"""
import os, sys, math, json, time
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import i0, i1, k0, k1, gammainc

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
G = 4.30091727e-6
KPC_M = 3.0856775814913673e19
A0_SI = 9.3603e-11                      # canonical footing (CHARTER)
A0 = A0_SI * KPC_M / 1e6                # (km/s)^2/kpc
C_KMS = 299792.458
OMEGA_C_OVER_B = 0.1200 / 0.02237       # cosmic cold/baryon mass ratio (Omega_c h^2 FITTED as in LCDM)


# ------------------------------------------------------------------------------------------------------ kernels
def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


def _h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def _dh_rar(y, e=1e-6):
    return (_h_rar(y * (1 + e)) - _h_rar(y * (1 - e))) / (2 * y * e)


_Y_P = brentq(lambda y: float(_dh_rar(y)), 1.0, 5.0)
_H_P = float(_h_rar(_Y_P))
_LYG = np.linspace(-14, 14, 280001)
_YG = 10 ** _LYG
_DH = np.maximum(_dh_rar(_YG), 0.05 * _H_P / (_YG + _Y_P))
_HM = float(_h_rar(_YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (_DH[1:] + _DH[:-1]) * np.diff(_YG))])


def nu_mono(y):
    """the chain's monotone repair of nu_RAR, rebuilt exactly as FP1_static_sector.py / L340 build it."""
    y = np.maximum(np.asarray(y, float), 1e-14)
    return 1.0 + np.interp(np.log10(y), _LYG, _HM) / y


KERNELS = {"P2": nu_p2, "nu_mono": nu_mono}


def kappa_of_kernel(nu, y, e=1e-5):
    """kappa(y) = d[(nu-1) g_N]/d g_N at fixed r-geometry = (nu - 1) + y nu'(y)   (used in the reciprocity lane)."""
    y = np.asarray(y, float)
    dn = (nu(y * (1 + e)) - nu(y * (1 - e))) / (2 * y * e)
    return (nu(y) - 1.0) + y * dn


# ------------------------------------------------------------------------------------------------------ baryon profiles
class Profile:
    """spherical-equivalent baryons: u_N(r) = G M_b(<r) on a fine log grid (monotone), with total mass Mtot."""

    def __init__(self, name, Mtot, uN_func, rgrid=None, rho_func=None):
        self.name, self.Mtot = name, Mtot
        self.rg = np.geomspace(1e-5, 1e7, 24001) if rgrid is None else rgrid
        u = np.maximum.accumulate(np.maximum(np.asarray(uN_func(self.rg), float), 0.0))
        self.ug = u
        self._u = PchipInterpolator(np.log(self.rg), u, extrapolate=True)
        self._rho_func = rho_func

    def u(self, r):
        r = np.asarray(r, float)
        out = self._u(np.log(np.maximum(r, self.rg[0])))
        return np.where(r < self.rg[0], self.ug[0] * (r / self.rg[0]) ** 3, np.where(r > self.rg[-1], self.ug[-1], out))

    def du(self, r, e=1e-5):
        r = np.asarray(r, float)
        return (self.u(r * (1 + e)) - self.u(r * (1 - e))) / (2 * r * e)

    def rho_b(self, r):
        """baryon density M_b'/(4 pi r^2) (Msun/kpc^3)."""
        if self._rho_func is not None:
            return self._rho_func(np.asarray(r, float))
        return self.du(r) / (4 * math.pi * G * np.asarray(r, float) ** 2)

    def gN(self, r):
        return self.u(r) / np.asarray(r, float) ** 2


def point_mass(M):
    return Profile("point", M, lambda r: G * M * np.ones_like(r))


def plummer(M, a):
    return Profile(f"plummer(a={a})", M, lambda r: G * M * r ** 3 / (r * r + a * a) ** 1.5,
                   rho_func=lambda r: 3 * M / (4 * math.pi * a ** 3) * (1 + (r / a) ** 2) ** -2.5)


def hernquist(M, a):
    return Profile(f"hernquist(a={a})", M, lambda r: G * M * r ** 2 / (r + a) ** 2,
                   rho_func=lambda r: M * a / (2 * math.pi * r * (r + a) ** 3))


def exp_sphere(M, h):
    """3-D exponential sphere rho_b = rho_0 exp(-r/h), rho_0 = M/(8 pi h^3):  M_b(<r) = M P(3, s) = M [1 - (1 + s + s^2/2) e^{-s}], s = r/h."""
    return Profile(f"expsphere(h={h})", M, lambda r: G * M * gammainc(3.0, r / h),
                   rho_func=lambda r: M / (8 * math.pi * h ** 3) * np.exp(-r / h))


def freeman_disc(M, h):
    """the spherical-equivalent enclosed mass of a razor-thin Freeman exponential disc, u_N = r V_bar^2 (the SPARC convention),
    V^2 = 4 pi G Sigma0 h y^2 [I0(y)K0(y) - I1(y)K1(y)], y = r/2h, Sigma0 = M/(2 pi h^2); taken as its monotone envelope
    (CFG10's convention: r V^2 overshoots M slightly outside a few h; the running maximum removes negative densities)."""
    S0 = M / (2 * math.pi * h * h)

    def uN(r):
        y = np.maximum(r / (2 * h), 1e-9)
        with np.errstate(over="ignore", invalid="ignore"):
            V2 = 4 * math.pi * G * S0 * h * y * y * (i0(y) * k0(y) - i1(y) * k1(y))
        V2 = np.where(y > 300, G * M / (r), V2)
        return np.nan_to_num(r * V2)

    return Profile(f"freeman(h={h})", M, uN)


# ------------------------------------------------------------------------------------------------------ closures for the cold fluid
def cold_mass(prof, kind, a0=A0, r0=None, r1=None, w0=None, n=6001, a0_ode=None):
    """integrate the cold-fluid mass w(r) = G M_c(<r) for a closure, on a log grid.  kinds (all with u = u_N + w):
         'encl'   (CFG10 ii)   rho_c g = (a0/3) rhobar_b(<r)          w' = a0 r u_N / u
         'const'  (CFG9 S2)    constant charge C = a0 M_b,tot / 4 pi  w' = a0 r u_N(inf) / u
         'gauss'  (CFG10 i)    pressure Gauss law P = a0 g_N/(8 pi G) w' = (a0/2) r (2 u_N - r u_N') / u
       returns (r, w, u, u_N).  a0_ode: a0 used INSIDE the ODE (MUTATE controls double it)."""
    a = a0 if a0_ode is None else a0_ode
    r0 = 1e-3 * (prof.Mtot * G / a0) ** 0.5 if r0 is None else r0   # start deep inside r_M
    r1 = 1e4 * (prof.Mtot * G / a0) ** 0.5 if r1 is None else r1
    rg = np.geomspace(r0, r1, n)
    UT = prof.ug[-1]

    def rhs(s, y):
        r = math.exp(s)
        uN = float(prof.u(r))
        u = max(uN + y[0], 1e-3 * max(uN, 1e-30), 1e-300)
        if kind == "encl":
            dw = a * r * uN / u
        elif kind == "const":
            dw = a * r * UT / u
        elif kind == "gauss":
            duN = float(prof.du(r))
            dw = 0.5 * a * r * (2.0 * uN - r * duN) / u
        else:
            raise ValueError(kind)
        return [r * dw]

    if w0 is None:                                                     # start on the slow manifold: the algebraic P2 value at r0 (any O(1) offset relaxes at once)
        u0 = float(prof.u(r0))
        w0 = u0 * (math.sqrt(1.0 + a * r0 * r0 / u0) - 1.0) if u0 > 0 else 0.0
    sol = solve_ivp(rhs, (math.log(r0), math.log(r1)), [w0], t_eval=np.log(rg), rtol=1e-10, atol=1e-14, method="Radau")
    w = sol.y[0]
    return rg, w, prof.u(rg) + w, prof.u(rg)


def target_fields(prof, r0=None, r1=None, n=6001, a0=A0):
    """the target (T) with ANALYTIC logarithmic slopes: r, rho_c, g_tot, dln rho_c/dln r, u_N, w.
       rho_c = a0 u_N/(4 pi G r u)  =>  dln rho/dln r = r u_N'/u_N - 1 - r u'/u,  u' = u_N' + a0 r u_N/u."""
    rr, w, u, uN = cold_mass(prof, "encl", a0=a0, r0=r0, r1=r1, n=n)
    if prof._rho_func is not None:
        duN = 4 * math.pi * G * rr ** 2 * prof._rho_func(rr)
    else:
        duN = prof.du(rr)
    dw = a0 * rr * uN / u
    rho = a0 * uN / (4 * math.pi * G * rr * u)
    dln = rr * duN / uN - 1.0 - rr * (duN + dw) / u
    return dict(r=rr, rho=rho, g=u / rr ** 2, dln=dln, uN=uN, w=w, u=u, cs2=rr * (u / rr ** 2) / (-dln))


def law_u(prof, r, kernel, a0=A0):
    """u = G M_law(<r) = nu(g_N/a0) u_N   (the framework's law, algebraic)."""
    uN = prof.u(r)
    y = uN / (np.asarray(r, float) ** 2 * a0)
    return KERNELS[kernel](y) * uN


# ------------------------------------------------------------------------------------------------------ reporting
class Report:
    def __init__(self, slug, mutate):
        self.slug = slug + ("_MUTATE" if mutate else "")
        self.lines, self.checks, self.numbers, self.t0 = [], [], {}, time.time()

    def P(self, s=""):
        print(s, flush=True)
        self.lines.append(s)

    def banner(self, s):
        self.P("\n" + "=" * 118 + "\n" + s + "\n" + "=" * 118)

    def check(self, name, detail, ok, load_bearing=True):
        self.checks.append(dict(name=name, detail=detail, ok=bool(ok), load_bearing=load_bearing))
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")

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

        json.dump(clean(dict(slug=self.slug, load_bearing_failures=nf, checks=self.checks, numbers=self.numbers)),
                  open(os.path.join(HERE, self.slug + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, self.slug + ".out"), "w").write("\n".join(self.lines) + "\n")
        return nf
