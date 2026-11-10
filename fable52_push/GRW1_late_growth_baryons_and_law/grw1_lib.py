#!/usr/bin/env python3
"""GRW1 engine: two-fluid linear growth (baryons + the cold component) from z_start with the a0 law under the frozen
treatments of FROZEN_CRITERIA.md section 1 (criteria 11c19a2c5f). TEST lane, quarantined; adopts nothing.
kappa = 1/2 FITTED; not theory closed. One thread.

Treatments ('tr'):
  'off'   law off: clock coefficient 1 - q^2 (Jeans), Poisson source baryons + clock.
  'TA'    the action's linear theory: delta_d = delta_N/(1 + c q^2), c = (1/(1+x))(1 - x mu^2/(1+x)), x = A_rms/a0 (self-consistent).
  'TAmax' TA with c = 1 everywhere (bound).
  'TS'    static law, total field as external field: source B (Om_b d_b + Om_c d_d), B = 1/(mu_e (1 + L_e mu^2)), x = g_rms/a0.
State per mode (k, mu): [delta_b, D_b, delta_c, D_c], D = d delta / d ln a. delta_c is delta_N (TA, TAmax, off) or delta_d (TS).
"""
import os, sys, math, json, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
from classy import Class

C_KMS = 299792.458
MPC_M = 3.0856775814913673e22
KB, MP = 1.380649e-23, 1.67262192e-27
OB, OD, H0, NS, AS = 0.0215, 0.11958060485606123, 65.0, 0.95, 2.0e-9
h = H0 / 100.0
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
ZSTART = 700.0
KGRID = np.geomspace(1e-3, 10.0, 64)
_t, _w = np.polynomial.legendre.leggauss(12)            # 12 nodes on [-1, 1]; the integrands are even in mu -> 6 nodes on [0, 1]
MU = _t[_t > 0]; WMU = _w[_t > 0]                       # sum WMU = 1: the average over [0, 1]
ZOUT = np.unique(np.round(np.concatenate([np.linspace(0.0, 7.0, 141), np.geomspace(7.0, ZSTART, 61), [0.295, 0.51, 0.706, 0.919]]), 10))
T_IGM, G_IGM, MU_IGM = 1.5e4, 1.5, 0.59
CS_PRIMARY = [1000.0, 1495.0, 2117.0, 3000.0, 4481.0]
CS_DT1 = [350.0, 500.0, 707.0]
_lnk = np.log(KGRID); WK = np.zeros_like(_lnk); _d = np.diff(_lnk); WK[:-1] += 0.5 * _d; WK[1:] += 0.5 * _d   # trapezoid in ln k
DR2 = AS * (KGRID / 0.05) ** (NS - 1.0)                 # Delta_R^2(k)


def run_class(cs=None, zmax=1000.0):
    """cs None: the cold reference (CDM). cs in km/s: the exponential term as CLASS's fluid (criteria 1.4)."""
    p = {"output": "mPk,mTk", "h": h, "omega_b": OB, "A_s": AS, "n_s": NS, "tau_reio": 0.06, "N_ur": 3.046, "T_cmb": 2.7255,
         "P_k_max_1/Mpc": 12.0, "z_max_pk": zmax}
    if cs is None:
        p["omega_cdm"] = OD
    else:
        xT = (cs / C_KMS) ** 2
        p.update({"omega_cdm": 1e-8, "Omega_fld": OD / h ** 2, "w0_fld": -1e-10, "wa_fld": 0.0, "cs2_fld": xT, "use_ppf": "no"})
    M = Class(); M.set(p); M.compute(); return M


class Background:
    """CLASS background + thermodynamics for one model. H in 1/Mpc (CLASS units)."""
    def __init__(self, M, zstart=ZSTART):
        self.M = M
        lna = np.linspace(math.log(1 / (1 + max(zstart, 900.0))) - 0.05, 0.0, 4001)
        lnH = np.log([M.Hubble(1 / math.exp(x) - 1) for x in lna])
        self.spH = CubicSpline(lna, lnH); self.spdH = self.spH.derivative()
        self.H0c = M.Hubble(0.0); self.ob0 = OB / h ** 2; self.oc0 = OD / h ** 2; self.og0 = M.Omega_g()
        th = M.get_thermodynamics()
        z = th["z"][::-1]; self.tz = z
        self.cb2 = np.maximum(th["c_b^2"][::-1], 0.0)
        self.kap = th["kappa' [Mpc^-1]"][::-1]
        self.zre = M.get_current_derived_parameters(["z_reio"])["z_reio"]
        self.cIGM = G_IGM * KB * T_IGM / (MU_IGM * MP) / (C_KMS * 1e3) ** 2
    def at(self, lna):
        a = math.exp(lna); z = 1 / a - 1; H = math.exp(float(self.spH(lna))); dl = float(self.spdH(lna))
        E2 = (H / self.H0c) ** 2
        Ob = self.ob0 * a ** -3 / E2; Oc = self.oc0 * a ** -3 / E2
        wre = 0.5 * (1 - math.tanh((z - self.zre) / 0.5))
        cb2 = float(np.interp(z, self.tz, self.cb2)) + wre * self.cIGM
        R43 = (4.0 / 3.0) * self.og0 * (1 + z) / self.ob0
        drag = R43 * float(np.interp(z, self.tz, self.kap)) / (a * H)
        return a, z, H, dl, Ob, Oc, cb2, drag


class EdS:
    """Einstein-de Sitter test background for KA3: baryon fraction f, no pressure, no drag; q^2 given directly."""
    def __init__(self, f): self.f = f
    def at(self, lna):
        a = math.exp(lna); return a, 1 / a - 1, 1.0, -1.5, self.f, 1 - self.f, 0.0, 0.0


def transfer_ic(M, zs, cold_key):
    """synchronous-gauge delta_b, delta_c at zs and d/d ln a by central difference (criteria 1.5), on KGRID."""
    def tr(z):
        T = M.get_transfer(z); k = T["k (h/Mpc)"] * h
        return (np.interp(_lnk, np.log(k), T["d_b"]), np.interp(_lnk, np.log(k), T[cold_key]))
    eps = 1e-3; a = 1 / (1 + zs)
    b0, c0 = tr(zs); bp, cp = tr(1 / (a * math.exp(eps)) - 1); bm, cm = tr(1 / (a * math.exp(-eps)) - 1)
    return b0, (bp - bm) / (2 * eps), c0, (cp - cm) / (2 * eps)


def cfac(x):
    """c(mu) of T-A at external field x (criteria 1.3)."""
    return (1.0 / (1.0 + x)) * (1.0 - x * MU ** 2 / (1.0 + x))


def Bfac(x):
    """T-S boost B(mu) = 1/(mu_e (1 + L_e mu^2))."""
    me = x / (1.0 + x); Le = 1.0 / (1.0 + x)
    return 1.0 / (me * (1.0 + Le * MU ** 2))


class Run:
    """one integration: background bg, treatment tr, a0 (m/s^2), cs(z) in km/s, initial state (4 arrays on KGRID)."""
    def __init__(self, bg, tr, a0, csz, ic, kgrid=KGRID, q2fix=None, cfix=None):
        self.bg, self.tr, self.a0, self.csz = bg, tr, a0, csz
        self.k = np.asarray(kgrid, float)[:, None]; self.nk = len(kgrid); self.nm = len(MU)
        self.q2fix, self.cfix = q2fix, cfix
        self.wkr = (WK * DR2)[:, None] * WMU[None, :] if len(kgrid) == len(KGRID) else None
        self.y0 = np.concatenate([np.repeat(np.asarray(v, float)[:, None], self.nm, axis=1).ravel() for v in ic])
        self.xlog = []
    def q2(self, lna, a, H, Oc):
        if self.q2fix is not None: return np.full((self.nk, 1), self.q2fix)
        cs = self.csz(1 / a - 1) / C_KMS
        return (self.k / (a * H) * cs) ** 2 / (1.5 * Oc)
    def xsolve(self, lna, a, H, Ob, Oc, db, dc, q2):
        """self-consistent external field x for TA / TS (criteria 1.3)."""
        if self.tr == "TA":
            cs = self.csz(1 / a - 1) * 1e3
            if cs == 0.0 or self.wkr is None: return 0.0
            kph = self.k / (a * MPC_M)
            def A2(x): return float(np.sum(self.wkr * (cs ** 2 * kph * dc / (1.0 + cfac(x)[None, :] * q2)) ** 2))
            Ahi = math.sqrt(A2(1e30))
            if Ahi == 0.0: return 0.0
            return brentq(lambda x: x - math.sqrt(A2(x)) / self.a0, 0.0, Ahi / self.a0 + 1.0, xtol=1e-14, rtol=1e-10)
        if self.tr == "TS":
            Hs = H * C_KMS * 1e3 / MPC_M; km = self.k / MPC_M; Om = Ob + Oc
            G = 1.5 * Hs ** 2 * a * (Ob * db + Oc * dc) / km                  # Newtonian field per mode (m/s^2, per unit R)
            g2N = self.wkr * G ** 2
            def g(x): return math.sqrt(float(np.sum(g2N * Bfac(x)[None, :] ** 2)))
            xN = math.sqrt(float(np.sum(g2N))) / self.a0
            if xN == 0.0: return 1e30
            return brentq(lambda x: x - g(x) / self.a0, 1e-14, xN + 1.0, xtol=1e-16, rtol=1e-11)
        return None
    def rhs(self, lna, y):
        a, z, H, dl, Ob, Oc, cb2, drag = self.bg.at(lna)
        Y = y.reshape(4, self.nk, self.nm); db, Db, dc, Dc = Y
        q2 = self.q2(lna, a, H, Oc)
        kaH2 = (self.k / (a * H)) ** 2
        tr = self.tr
        if tr == "smooth":                                     # KA3(a) only: the clock held smooth
            src = Ob * db; dDc = np.zeros_like(Dc)
        elif tr == "off":
            src = Ob * db + Oc * dc; coefc = 1.0 - q2
            dDc = -(2 + dl) * Dc + 1.5 * (Ob * db + Oc * dc * coefc)
        elif tr in ("TA", "TAmax"):
            if self.cfix is not None: c = np.full(self.nm, self.cfix)
            elif tr == "TAmax": c = np.ones(self.nm)
            else: c = cfac(self.xsolve(lna, a, H, Ob, Oc, db, dc, q2))
            src = Ob * db + Oc * dc; coefc = 1.0 - q2 / (1.0 + c[None, :] * q2)
            dDc = -(2 + dl) * Dc + 1.5 * (Ob * db + Oc * dc * coefc)
        elif tr == "TS":
            B = Bfac(self.xsolve(lna, a, H, Ob, Oc, db, dc, q2))[None, :]
            src = B * (Ob * db + Oc * dc)
            dDc = -(2 + dl) * Dc + 1.5 * src - 1.5 * Oc * q2 * dc
        else:
            raise ValueError(tr)
        dDb = -(2 + dl + drag) * Db + 1.5 * src - kaH2 * cb2 * db
        return np.concatenate([Db.ravel(), dDb.ravel(), Dc.ravel(), dDc.ravel()])
    def solve(self, zout=ZOUT, lna0=None, rtol=1e-7, atol=1e-10):
        lna0 = math.log(1 / (1 + ZSTART)) if lna0 is None else lna0
        te = np.sort(np.log(1 / (1 + np.asarray(zout, float))))
        te = te[te >= lna0 - 1e-12]
        so = solve_ivp(self.rhs, (lna0, float(te[-1])), self.y0, t_eval=te, method="DOP853", rtol=rtol, atol=atol)
        if not so.success: raise RuntimeError(so.message)
        self.nfev = so.nfev
        Y = so.y.reshape(4, self.nk, self.nm, -1)
        zz = 1 / np.exp(so.t) - 1
        xs = []
        if self.tr in ("TA", "TS"):
            for j, t in enumerate(so.t):
                a, z, H, dl, Ob, Oc, cb2, drag = self.bg.at(t)
                xs.append(self.xsolve(t, a, H, Ob, Oc, Y[0, :, :, j], Y[2, :, :, j], self.q2(t, a, H, Oc)))
        return dict(z=zz, db=Y[0], Db=Y[1], dc=Y[2], Dc=Y[3], x=np.array(xs) if xs else None, nfev=so.nfev)


def const_cs(cs):
    return lambda z: cs


def step_cs(cs, zw):
    return lambda z: (cs if z <= zw else 0.0)


def lens_delta(out, tr, a0=None, bg=None):
    """delta the lensing sees, per (k, mu, z); TS includes the boost B (needs x)."""
    wb, wc = OB / (OB + OD), OD / (OB + OD)
    d = wb * out["db"] + wc * out["dc"]
    if tr == "TS":
        B = np.stack([Bfac(x) for x in out["x"]], axis=-1)[None, :, :]
        d = d * B
    return d


def muavg2(arr):
    """mu-average of |arr|^2 over axis 1 (arr: k, mu, z)."""
    return np.einsum("m,kmz->kz", WMU, arr ** 2)
