#!/usr/bin/env python3
"""CFG599 library (criteria FROZEN_CRITERIA.md, 8a10775bd).  Re-uses CFG597's grid, hydro, Poisson, CIC and round-phantom
routines read-only (imported from ../CFG597_merger_settling_stopwatch/cfg597_lib.py) and adds:
  - Progenitor599: CFG597's progenitor plus the sub's cool core (M-3b: f_cc = 0.15 of the sub's gas as a Plummer a = 50 kpc
    cloud truncated at 300 kpc; the rest of the gas on the grid), with the phantom of the baryons INCLUDING the core;
  - the mass-conserving bilinear projection of grid gas (O-1) and the shrinking-circle peak estimator (O-2).
Units kpc, Gyr, Msun.  kappa = 1/2 is fitted; the cold energy's mass is required (an input); no particle species."""
import os, sys, math
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.ndimage import map_coordinates
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG597_merger_settling_stopwatch"))
import cfg597_lib as L597                      # read-only re-use
from cfg597_lib import (G, KMS, A0, A0_SI, GAMMA, nu_mono, r200_of, Grid, prim, cons, hydro_step, hydro_dt,  # noqa: F401
                        cumtrapz_sph, phantom_mass, sample_radial, phantom_profile_from_mass)

F_CC = 0.15          # cool-core fraction of the SUB's gas (M-3b)
A_CC = 50.0          # Plummer scale, kpc
R_CC_T = 300.0       # cloud truncation, kpc


class Progenitor599:
    """Spherical progenitor (CFG597 M-3/M-4 case L) with an optional cool-core cloud (M-3b)."""

    def __init__(self, M200, foot, swap=False, cloud=False, nr=4000, rmax=8000.0):
        self.M200 = M200; self.r200 = r200_of(M200); self.rt = min(self.r200, 1200.0)
        self.Mb = M200 / 6.73
        fg, fs = (0.13, 0.87) if swap else (0.87, 0.13)
        self.Mgas_all, self.Mst = fg * self.Mb, fs * self.Mb
        self.cloud = cloud
        self.Mcc = F_CC * self.Mgas_all if cloud else 0.0
        self.Mgas = self.Mgas_all - self.Mcc                      # grid part
        self.a0 = A0[foot]
        r = np.concatenate([[0.0], np.geomspace(0.5, rmax, nr)]); self.r = r
        rc = 0.1 * self.r200
        sh = (1 + (r / rc) ** 2) ** -1.0 * np.where(r < self.rt, 1.0, (np.maximum(r, 1e-3) / self.rt) ** -8.0)
        Mg = cumtrapz_sph(r, sh)
        self.rho_g0 = self.Mgas / Mg[-1]
        self.rho_g = self.rho_g0 * sh; self.Mg = self.rho_g0 * Mg
        # cool core (Plummer, truncated)
        if cloud:
            pl = (1 + (r / A_CC) ** 2) ** -2.5 * (r < R_CC_T)
            Mp = cumtrapz_sph(r, pl)
            self.rho_cc = self.Mcc * pl / Mp[-1]; self.Mcc_r = self.Mcc * Mp / Mp[-1]
        else:
            self.rho_cc = 0 * r; self.Mcc_r = 0 * r
        self.Sigma_cc = self.Mcc / (math.pi * A_CC ** 2) if cloud else None
        rs = self.r200 / 4.0
        nfw = np.where(r < self.rt, 1.0 / (np.maximum(r, 1e-3) / rs * (1 + r / rs) ** 2), 0.0)
        Mn = cumtrapz_sph(r, nfw)
        self.nfw_shape = nfw / Mn[-1]; self.Mnfw_unit = Mn / Mn[-1]
        self.rho_s = self.Mst * self.nfw_shape; self.Ms = self.Mst * self.Mnfw_unit
        self.Mbar = self.Mg + self.Ms + self.Mcc_r
        Mph = phantom_mass(r, self.Mbar, self.a0)
        Mph_t = np.interp(self.rt, r, Mph)
        self.Mph = np.where(r < self.rt, Mph, Mph_t)
        self.rho_ph = np.gradient(self.Mph, r) / (4 * math.pi * np.maximum(r, 1e-3) ** 2)
        self.rho_ph[r >= self.rt] = 0.0
        self.Mph_tot = Mph_t
        self.Mtot = self.Mbar + self.Mph
        gN = G * self.Mtot / np.maximum(r, 1e-3) ** 2
        integrand = self.rho_g * gN
        P = np.zeros_like(r)
        P[-1] = self.rho_g[-1] * 0.5 * G * self.Mtot[-1] / r[-1]
        for k in range(len(r) - 2, -1, -1):
            P[k] = P[k + 1] + 0.5 * (integrand[k] + integrand[k + 1]) * (r[k + 1] - r[k])
        self.P = P
        # case-L only in this lane (M-4)
        self.rho_u = 0 * r; self.Mu = 0 * r; self.Mu_tot = 0.0; self.u_frac = 0.0

    def jeans_sigma2(self, rho):
        r = self.r
        gN = G * self.Mtot / np.maximum(r, 1e-3) ** 2
        f = rho * gN
        I = np.zeros_like(r)
        for k in range(len(r) - 2, -1, -1):
            I[k] = I[k + 1] + 0.5 * (f[k] + f[k + 1]) * (r[k + 1] - r[k])
        return np.where(rho > 0, I / np.maximum(rho, 1e-300), 0.0)


# ------------------------------------------------------------------------------------------------ O-1 projection
def project_grid_bilinear(F3, g, Xp, Yp):
    """sum a 3-D density along z on the 50-kpc grid, bilinearly interpolate the column density onto pixel centres (Xp, Yp
    1-D arrays) and renormalise to the exact column mass. Returns a surface density (Msun/kpc^2) on the pixel grid."""
    S = F3.sum(2) * g.dx                                   # column density at coarse cell centres
    Mtot = S.sum() * g.dx ** 2
    u = (Xp - g.lo[0]) / g.dx - 0.5; v = (Yp - g.lo[1]) / g.dx - 0.5
    UU, VV = np.meshgrid(u, v, indexing="ij")
    out = map_coordinates(S, [UU.ravel(), VV.ravel()], order=1, mode="nearest").reshape(UU.shape)
    px = Xp[1] - Xp[0]
    s = out.sum() * px * px
    if s > 0 and Mtot > 0:
        out *= Mtot / s
    return out


# ------------------------------------------------------------------------------------------------ O-2 shrinking circle
def shrink_peak(X, Y, S, start, R0=300.0, Rmin=50.0, fac=0.85, tol=0.1, itmax=200):
    """shrinking-circle peak: centre <- mass-weighted centroid within R; R <- max(fac R, Rmin); iterate at Rmin to |dc| < tol."""
    c = np.array(start, float); R = R0
    for _ in range(itmax):
        w = S * (((X - c[0]) ** 2 + (Y - c[1]) ** 2) <= R * R)
        sw = w.sum()
        if sw <= 0:
            return c, False
        cn = np.array([(w * X).sum() / sw, (w * Y).sum() / sw])
        dc = np.hypot(*(cn - c)); c = cn
        if R > Rmin:
            R = max(fac * R, Rmin)
        elif dc < tol:
            return c, True
    return c, False


def massweighted_start(X, Y, S, centre, Rw=600.0):
    w = S * (((X - centre[0]) ** 2 + (Y - centre[1]) ** 2) <= Rw * Rw)
    sw = w.sum()
    if sw <= 0:
        return np.array(centre, float)
    return np.array([(w * X).sum() / sw, (w * Y).sum() / sw])
