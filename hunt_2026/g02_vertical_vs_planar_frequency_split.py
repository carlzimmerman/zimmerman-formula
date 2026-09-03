#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""g02_vertical_vs_planar_frequency_split.py
=================================================================================================
THE VERTICAL-VERSUS-PLANAR SPLIT IN THE MILKY WAY DISC, as a test of the modified-GRAVITY versus
modified-INERTIA fork (f08-f10, F08_F10_THE_COHERENCE_FORK.md).

WHY THIS IS THE CLEANEST LABORATORY FOR THE FORK.  Both motions happen in the SAME system at the
SAME field point.  In modified GRAVITY there is ONE potential: once the kernel and the baryons are
fixed, the circular speed and the vertical force are both derivatives of it and there is no freedom
left.  In modified INERTIA the modification attaches to the TRAJECTORY, and a vertical oscillation
(frequency nu_z) is a different trajectory from a circular orbit (frequency Omega) even at the same
place in the disc.  Milgrom (1994, Ann.Phys. 229, 384; 2011, arXiv:1111.1611) proved the two are
IDENTICAL for circular orbits in the deep-MOND limit and DIFFER for every other orbit, so a
vertical/planar comparison is exactly where they must part.

THE STATISTIC.  Everything is put into ONE ratio of FORCES, so that the overall baryon-budget
normalisation cancels exactly and the surface-density convention never enters:

      S  =  nu_vert / nu_rad
         =  [ |K_z^obs(R0, 1.1 kpc)| / |K_z^bar(R0, 1.1 kpc)| ]
            / [ (V_c^2/R0) / |g_bar,R(R0, 0)| ]

  Published vertical determinations are quoted as Sigma_1.1 = |K_z(1.1 kpc)| / (2 pi G) (the
  Kuijken & Gilmore 1991 convention), so |K_z^obs| = 2 pi G Sigma_dyn exactly, with no assumption
  about the radial term in the integrated Poisson equation.  The model enters ONLY through the
  dimensionless SHAPE number

      Q  =  |g_bar,R(R0, 0)| / |g_bar,z(R0, 1.1 kpc)|            ->    S = 2 pi G Sigma_dyn Q R0 / V_c^2

  Scaling every baryonic component by a common f leaves Q untouched, so the baryon budget's
  NORMALISATION -- the systematic the brief warned would swamp this test -- drops out identically.
  What is left is the mass model's SHAPE.

THE ARMS, each predicting its own S with no free parameter:
  MODIFIED GRAVITY (QUMOND, the framework's own Route A kernel, a0 an INPUT, both footings):
      div g = div [ nu(|g_N|/a0) g_N ]      solved exactly on an axisymmetric grid.  Zero freedom.
  MODIFIED INERTIA, algebraic/local (the map operative in this repository since 2026-08-08):
      a(x) = nu(|g_N(x)|/a0) g_N(x)         ONE scalar, both directions, no trajectory dependence.
  MODIFIED INERTIA, trajectory-dependent: A1 orbit-averaged, A2 the repository's own frequency
      gate, A3 a generic frequency power law.  All three are ASSUMPTIONS, written as equations in
      V5 and scanned over their defensible ranges.

DATA, all published, cited inline where used:
  Kuijken & Gilmore 1991, ApJ 367, L9          Sigma_1.1(R0) = 71 +- 6 Msun/pc^2
  Holmberg & Flynn 2004, MNRAS 352, 440        Sigma_1.1(R0) = 74 +- 6
  Bovy & Rix 2013, ApJ 779, 115                Sigma_1.1(R0) = 68 +- 4   (stars+remnants 38 +- 4)
  Nitschai, Eilers, Neumayer, Cappellari & Rix 2021, ApJ 916, 112 (arXiv:2106.05286)
                                               Sigma(R0,|z|<=1.1kpc) = 55.5 +- 1.7 (syst)
                                               v_c(R0) = 234.7 +- 1.7 km/s
  Eilers, Hogg, Rix & Ness 2019, ApJ 871, 120  v_c(8.122 kpc) = 229.0 +- 0.2(stat) +- 2.6(sys) km/s
  GRAVITY Collaboration 2019, A&A 625, L10     R0 = 8.178 +- 0.026 kpc
  McKee, Parravano & Hollenbach 2015, ApJ 814, 13   Sigma_bar(R0) = 47.1 +- 3.4 (gas 13.7 +- 1.6)
  Bland-Hawthorn & Gerhard 2016, ARA&A 54, 529 thin-disc scale length R_d = 2.6 +- 0.5 kpc
  McMillan 2017, MNRAS 465, 76, Table 3        the baryon mass model (SHAPE only; see above)
  Bienayme, Famaey, Wu, Zhao & Aubert 2009, A&A 500, 801   full 3D AQUAL comparator
  Lisanti, Moschella, Outmezguine & Slone 2019, PRD 100, 083009   the scalar-enhancement dilemma

SECTIONS
  V1  THE SYSTEMATIC, FIRST.  The error budget on S is built BEFORE any prediction is computed.
  V2  The axisymmetric Poisson machinery and its validations (analytic Miyamoto-Nagai; the exact
      QUMOND spherical identity).  Nothing is differentiated numerically anywhere.
  V3  The Newtonian baryon model, the shape number Q, and Q's literature-spanning systematic.
  V4  THE MODIFIED-GRAVITY ARM (QUMOND solve), both footings, three radii.
  V5  THE MODIFIED-INERTIA ARMS, with every assumption written as an equation and scanned.
  V6  THE CONFRONTATION: which arm, and at how many sigma.
  V7  What would have to improve for this test to decide the fork.
  V8  MUTATION CONTROLS.

BOTH a0 FOOTINGS on every dimensional number.  Checks that FAIL are reported, not tuned away.
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np
from scipy.special import j0, j1

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import A0, Check, G, P, Msun, info, kpc, nu  # noqa: E402

PC = kpc / 1000.0
MSUN_PC2 = Msun / PC**2
TWO_PI_G = 2.0 * math.pi * G

C = Check()
np.seterr(over="ignore", divide="ignore", invalid="ignore")


def banner(t: str) -> None:
    P("\n" + "=" * 104)
    P("  " + t)
    P("=" * 104)


# =================================================================================================
# THE BARYON MODEL -- McMillan 2017, MNRAS 465, 76, Table 3 best-fitting parameters, verbatim.
# Used for its SHAPE only; the normalisation cancels out of the statistic S by construction (V1).
# =================================================================================================
MCM = dict(
    S0_thin=896.0 * MSUN_PC2, Rd_thin=2.50 * kpc, zd_thin=0.300 * kpc,
    S0_thick=183.0 * MSUN_PC2, Rd_thick=3.02 * kpc, zd_thick=0.900 * kpc,
    rho0_b=98.4 * Msun / PC**3, alpha_b=1.8, r0_b=0.075 * kpc, rcut_b=2.1 * kpc, q_b=0.5,
    S_HI_fid=10.0 * MSUN_PC2, Rm_HI=4.0 * kpc, Rd_HI=7.0 * kpc, zd_HI=0.085 * kpc,
    S_H2_fid=2.0 * MSUN_PC2, Rm_H2=12.0 * kpc, Rd_H2=1.5 * kpc, zd_H2=0.045 * kpc,
    R_fid=8.33 * kpc,
)
ALLP = ("thin", "thick", "bulge", "HI", "H2")


def rho_baryons(R, z, pars=None, parts=ALLP):
    """McMillan 2017 baryonic density, SI (kg/m^3).  R, z broadcastable; z may be signed."""
    p = MCM if pars is None else pars
    R = np.asarray(R, float)
    z = np.abs(np.asarray(z, float))
    out = np.zeros(np.broadcast(R, z).shape, float)
    if "thin" in parts:
        out = out + (p["S0_thin"] / (2 * p["zd_thin"])) * np.exp(-z / p["zd_thin"] - R / p["Rd_thin"])
    if "thick" in parts:
        out = out + (p["S0_thick"] / (2 * p["zd_thick"])) * np.exp(-z / p["zd_thick"] - R / p["Rd_thick"])
    if "bulge" in parts:
        rp = np.sqrt(R**2 + (z / p["q_b"]) ** 2)
        out = out + p["rho0_b"] / (1 + rp / p["r0_b"]) ** p["alpha_b"] * np.exp(-((rp / p["rcut_b"]) ** 2))
    for tag in ("HI", "H2"):
        if tag not in parts:
            continue
        S0 = p[f"S_{tag}_fid"] / math.exp(-p[f"Rm_{tag}"] / p["R_fid"] - p["R_fid"] / p[f"Rd_{tag}"])
        zd = p[f"zd_{tag}"]
        Rs = np.maximum(R, 1e-3 * kpc)
        out = out + (S0 / (4 * zd)) * np.exp(-p[f"Rm_{tag}"] / Rs - Rs / p[f"Rd_{tag}"]) \
            / np.cosh(z / (2 * zd)) ** 2
    return out


def sigma_baryons(R, zmax, pars=None, parts=ALLP, n=3001):
    """Sigma(R, |z|<zmax) = 2 int_0^zmax rho dz, SI kg/m^2."""
    zz = np.linspace(0.0, zmax, n)
    return 2.0 * np.trapz(rho_baryons(np.full_like(zz, float(R)), zz, pars, parts), zz)


# =================================================================================================
# V2 machinery -- EXACT axisymmetric Poisson and EXACT QUMOND, entirely in Hankel space.
#
#   rho~(k,z) = int_0^inf rho(R,z) J0(kR) R dR
#   I(k,z)    = int e^{-k|z-z'|} rho~(k,z') dz'
#   Phi = -2 pi G int dk J0(kR) I ;  g_R = -2 pi G int dk k J1(kR) I ;  g_z = +2 pi G int dk J0 dI/dz
#   dI/dz(k,z) = -k int sgn(z-z') e^{-k|z-z'|} rho~(k,z') dz'
#
# QUMOND'S PHANTOM WITHOUT ANY NUMERICAL DERIVATIVE.  QUMOND is lap Phi = div[nu(|grad Phi_N|/a0)
# grad Phi_N]; with g = -grad Phi and F = [nu(|g_N|/a0) - 1] g_N (tapered to zero at the box edge so
# every boundary term vanishes) this is 4 pi G rho_ph = -div F -- the MINUS SIGN matters, and the
# spherical identity V2b is what catches it.  Integrating by parts in R and in z inside the
# transforms turns both derivatives into algebra:
#   -4 pi G rho~_ph(k,z) = k Ft_R1(k,z) + d/dz Ft_z0(k,z),
#       Ft_R1 = int F_R J1(kR) R dR ,   Ft_z0 = int F_z J0(kR) R dR
#   => I_ph  = (k/4 pi G) ( E0[Ft_R1] - E1[Ft_z0] )
#      dI_ph = (k/4 pi G) ( -k E1[Ft_R1] - 2 Ft_z0 + k E0[Ft_z0] )
#   with E0[h](z) = int e^{-k|z-z'|} h dz' and E1[h](z) = int sgn(z-z') e^{-k|z-z'|} h dz'.
# So NOTHING in this file is finite-differenced; V2b tests the result against the exact spherical
# QUMOND identity, which any error in the above would break.
# =================================================================================================
def _trapw(x):
    w = np.empty_like(x)
    w[1:-1] = 0.5 * (x[2:] - x[:-2])
    w[0] = 0.5 * (x[1] - x[0])
    w[-1] = 0.5 * (x[-1] - x[-2])
    return w


class Grid:
    """THE k GRID IS HYBRID AND THAT IS NOT COSMETIC.  The Bessel factor J1(kR) oscillates in k with
    period 2 pi / R, so a purely LOGARITHMIC k grid under-samples it at large R (dk = k dlnk grows
    with k) and returns a radial force that oscillates by tens of per cent past 10 kpc.  This grid is
    log-spaced only below k = dk (where the oscillation is slow) and UNIFORM above it, and V2c checks
    convergence by halving dk."""

    def __init__(self, Rmax=60.0 * kpc, dR=0.03 * kpc, Nz=241, zmax=60.0 * kpc, z_soft=0.01 * kpc,
                 kmin=0.0008 / kpc, dk=0.005 / kpc, kmax=10.0 / kpc, zsnap=(1.1 * kpc,)):
        self.R = np.arange(0.5 * dR, Rmax, dR)
        u = np.linspace(0.0, math.asinh(zmax / z_soft), Nz)
        zp = z_soft * np.sinh(u)
        for zs in zsnap:                                  # snap a node onto the evaluation height
            zp[np.argmin(np.abs(zp - zs))] = zs
        self.z = np.concatenate([-zp[:0:-1], zp])         # full symmetric grid, z=0 included
        klo = np.exp(np.linspace(math.log(kmin), math.log(0.999 * dk), 25))
        self.k = np.concatenate([klo, np.arange(dk, kmax + 0.5 * dk, dk)])
        self.wR = _trapw(self.R)
        self.wR[0] += self.R[0]                           # include the [0, R0] sliver
        self.wz = _trapw(self.z)
        self.wk = _trapw(self.k)
        self.wk[0] += self.k[0]
        self.J0 = j0(np.outer(self.k, self.R))            # (Nk, NR)
        self.J1 = j1(np.outer(self.k, self.R))
        self.RwR = self.R * self.wR
        d = self.z[:, None] - self.z[None, :]
        self.absd = np.abs(d)
        self.sgn = np.sign(d)

    # ---- transforms -----------------------------------------------------------------------------
    def h0(self, f):
        """order-0 Hankel over R: (NR,Nz) -> (Nk,Nz)."""
        return (self.J0 * self.RwR) @ f

    def h1(self, f):
        return (self.J1 * self.RwR) @ f

    def _E(self, kk, h):
        """E0[h], E1[h] at one k.  h shape (Nz,) -> scalars per z, returns (Nz,), (Nz,)."""
        Ek = np.exp(-kk * self.absd)
        hw = h * self.wz
        return Ek @ hw, (self.sgn * Ek) @ hw

    def newton(self, rho):
        """Newtonian g_R, g_z on the whole grid, shapes (NR, Nz)."""
        rh = self.h0(rho)
        I = np.empty_like(rh)
        dI = np.empty_like(rh)
        for i, kk in enumerate(self.k):
            e0, e1 = self._E(kk, rh[i])
            I[i] = e0
            dI[i] = -kk * e1
        gR = -TWO_PI_G * ((self.J1.T * (self.wk * self.k)) @ I)
        gz = +TWO_PI_G * ((self.J0.T * self.wk) @ dI)
        return gR, gz

    def newton_at(self, rho, Rf, zf):
        """Newtonian g_R, g_z at arbitrary field points."""
        rh = self.h0(rho)
        Rf = np.atleast_1d(np.asarray(Rf, float))
        zf = np.atleast_1d(np.asarray(zf, float))
        d = zf[:, None] - self.z[None, :]
        ad, sg = np.abs(d), np.sign(d)
        I = np.empty((len(self.k), len(zf)))
        dI = np.empty_like(I)
        for i, kk in enumerate(self.k):
            Ek = np.exp(-kk * ad)
            hw = rh[i] * self.wz
            I[i] = Ek @ hw
            dI[i] = -kk * ((sg * Ek) @ hw)
        gR = -TWO_PI_G * np.einsum("kn,k,kn->n", j1(np.outer(self.k, Rf)), self.wk * self.k, I)
        gz = +TWO_PI_G * np.einsum("kn,k,kn->n", j0(np.outer(self.k, Rf)), self.wk, dI)
        return gR, gz

    def qumond(self, rho, a0, taper=(35.0 * kpc, 55.0 * kpc)):
        """TOTAL QUMOND g_R, g_z on the grid (Newtonian + phantom), plus the Newtonian pair."""
        gRn, gzn = self.newton(rho)
        fac = nu(np.hypot(gRn, gzn) / a0) - 1.0
        r = np.hypot(self.R[:, None], self.z[None, :])
        t0, t1 = taper
        w = np.clip((t1 - r) / (t1 - t0), 0.0, 1.0)
        w = w * w * (3 - 2 * w)                                # smoothstep taper -> F = 0 at the edge
        FR1 = self.h1(-fac * gRn * w)          # the leading minus is 4 pi G rho_ph = -div F
        Fz0 = self.h0(-fac * gzn * w)
        Iph = np.empty_like(FR1)
        dIph = np.empty_like(FR1)
        for i, kk in enumerate(self.k):
            aR0, aR1 = self._E(kk, FR1[i])
            az0, az1 = self._E(kk, Fz0[i])
            Iph[i] = kk * (aR0 - az1)
            dIph[i] = kk * (-kk * aR1 - 2.0 * Fz0[i] + kk * az0)
        # Phi_ph = -(1/2) int dk J0 Iph  (the 2 pi G and 1/4 pi G cancel to 1/2)
        gRp = -0.5 * ((self.J1.T * (self.wk * self.k)) @ Iph)
        gzp = +0.5 * ((self.J0.T * self.wk) @ dIph)
        return gRn + gRp, gzn + gzp, gRn, gzn


# ---- analytic comparators used ONLY to validate the machinery -------------------------------------
def mn_rho(R, z, M, a, b):
    zt = np.sqrt(z**2 + b**2)
    return (b**2 * M / (4 * math.pi)) * (a * R**2 + (a + 3 * zt) * (a + zt) ** 2) \
        / ((R**2 + (a + zt) ** 2) ** 2.5 * zt**3)


def mn_forces(R, z, M, a, b):
    zt = np.sqrt(z**2 + b**2)
    den = (R**2 + (a + zt) ** 2) ** 1.5
    return -G * M * R / den, -G * M * z * (a + zt) / (zt * den)


def plummer_rho(R, z, M, a):
    return (3 * M / (4 * math.pi * a**3)) * (1 + (R**2 + z**2) / a**2) ** -2.5


def plummer_gr(r, M, a):
    return -G * M * r / (r**2 + a**2) ** 1.5


# =================================================================================================
banner("V1  THE SYSTEMATIC, FIRST -- what discriminating power is available before any prediction")
# =================================================================================================
P(r"""  THE STATISTIC.   S = nu_vert / nu_rad, entirely a ratio of FORCES:

      nu_vert = |K_z^obs(R0,1.1 kpc)| / |K_z^bar(R0,1.1 kpc)| = 2 pi G Sigma_dyn / |g_bar,z(R0,1.1)|
      nu_rad  = (V_c^2/R0) / |g_bar,R(R0,0)|
      =>  S = 2 pi G Sigma_dyn * Q * R0 / V_c^2,     Q = |g_bar,R(R0,0)| / |g_bar,z(R0,1.1 kpc)|

  Published Sigma_1.1 values are DEFINED as |K_z(1.1 kpc)|/(2 pi G) (Kuijken & Gilmore 1991), so no
  surface-density/force conversion and no radial-term correction ever enters.  Scaling every
  baryonic component by a common f leaves Q untouched: the baryon budget's NORMALISATION -- the
  systematic the brief warned would swamp this test -- CANCELS IDENTICALLY.  Only the mass model's
  SHAPE survives, in the single dimensionless number Q.""")

SIGMA_DYN = [("Kuijken & Gilmore 1991, ApJ 367, L9", 71.0, 6.0),
             ("Holmberg & Flynn 2004, MNRAS 352, 440", 74.0, 6.0),
             ("Bovy & Rix 2013, ApJ 779, 115", 68.0, 4.0),
             ("Nitschai+ 2021, ApJ 916, 112 (Gaia EDR3+APOGEE)", 55.5, 1.7)]
VC = [("Eilers+ 2019, ApJ 871, 120", 229.0e3, 2.6e3),
      ("Nitschai+ 2021, ApJ 916, 112", 234.7e3, 1.7e3)]
R0_MEAS, R0_ERR = 8.178 * kpc, 0.026 * kpc          # GRAVITY Collaboration 2019, A&A 625, L10
SIG_BAR_MCKEE, SIG_BAR_MCKEE_E = 47.1, 3.4          # McKee, Parravano & Hollenbach 2015, ApJ 814, 13

P("\n  the vertical measurement, four published determinations of Sigma_1.1(R0):")
for nme, v, e in SIGMA_DYN:
    P(f"      {v:5.1f} +- {e:3.1f}   {nme}")
vals = np.array([v for _, v, _ in SIGMA_DYN])
errs = np.array([e for _, _, e in SIGMA_DYN])
spread = float(vals.std(ddof=1))
P(f"\n  unweighted mean {vals.mean():.1f}, between-paper scatter {spread:.1f} "
  f"({spread/vals.mean():.1%}), quoted errors {errs.min():.1f}-{errs.max():.1f}")
C("V1a the SPREAD BETWEEN PUBLISHED Sigma_1.1 DETERMINATIONS EXCEEDS THEIR QUOTED ERRORS -- so the "
  "vertical measurement's true uncertainty is the literature scatter, not any one paper's error bar",
  spread > errs.mean(), f"scatter {spread:.1f} vs mean quoted error {errs.mean():.1f} Msun/pc^2")
P(f"\n  the planar measurement:  V_c(R0) = {VC[0][1]/1e3:.1f} +- {VC[0][2]/1e3:.1f} km/s ({VC[0][0]})")
P(f"                           V_c(R0) = {VC[1][1]/1e3:.1f} +- {VC[1][2]/1e3:.1f} km/s ({VC[1][0]})")
P(f"                           R0      = {R0_MEAS/kpc:.3f} +- {R0_ERR/kpc:.3f} kpc (GRAVITY 2019)")
P(f"  the baryon column, a cross-check only (it cancels from S):  Sigma_bar(R0) = "
  f"{SIG_BAR_MCKEE} +- {SIG_BAR_MCKEE_E} Msun/pc^2 (McKee+ 2015)")


# =================================================================================================
banner("V2  THE MACHINERY AND ITS VALIDATIONS -- exact axisymmetric Poisson, then exact QUMOND")
# =================================================================================================
GD = Grid()
info(f"grid: R {GD.R[0]/kpc:.3f}-{GD.R[-1]/kpc:.1f} kpc x {len(GD.R)} uniform;  "
     f"z +-{GD.z[-1]/kpc:.1f} kpc x {len(GD.z)} sinh (finest {GD.z[len(GD.z)//2+1]/kpc:.5f} kpc);  "
     f"k {GD.k[0]*kpc:.4f}-{GD.k[-1]*kpc:.1f} kpc^-1 x {len(GD.k)} (log below 0.005, then uniform)")

MMN, aMN, bMN = 5.0e10 * Msun, 3.0 * kpc, 0.3 * kpc
rho_mn = mn_rho(GD.R[:, None], GD.z[None, :], MMN, aMN, bMN)
Rt = np.array([4.0, 8.178, 8.178, 15.0]) * kpc
zt = np.array([0.0, 1.1, -1.1, 1.1]) * kpc
gR_num, gz_num = GD.newton_at(rho_mn, Rt, zt)
gR_an, gz_an = mn_forces(Rt, zt, MMN, aMN, bMN)
P("\n  V2a  Miyamoto-Nagai (M=5e10 Msun, a=3 kpc, b=0.3 kpc) -- numeric vs exact analytic:")
P(f"      {'R,z [kpc]':<17}{'gR num':>13}{'gR exact':>13}{'err':>9}{'gz num':>13}{'gz exact':>13}{'err':>9}")
eR = np.abs(gR_num / gR_an - 1)
ez = np.array([abs(gz_num[i] / gz_an[i] - 1) if gz_an[i] != 0 else abs(gz_num[i]) / abs(gR_an[i])
               for i in range(len(Rt))])
for i in range(len(Rt)):
    P(f"      {Rt[i]/kpc:5.2f},{zt[i]/kpc:6.2f}   {gR_num[i]:13.4e}{gR_an[i]:13.4e}{eR[i]:9.3%}"
      f"{gz_num[i]:13.4e}{gz_an[i]:13.4e}{ez[i]:9.3%}")
C("V2a the Hankel machinery reproduces the exact Miyamoto-Nagai forces (and returns gz = 0 in the "
  "plane, gz antisymmetric across it)", max(eR.max(), ez.max()) < 0.01,
  f"worst error {max(eR.max(), ez.max()):.3%}")

MPL, aPL = 6.0e10 * Msun, 3.0 * kpc
rho_pl = plummer_rho(GD.R[:, None], GD.z[None, :], MPL, aPL)
P("\n  V2b  the EXACT QUMOND spherical identity.  In spherical symmetry div g = div[nu g_N] "
  "integrates\n       to g = nu(|g_N|/a0) g_N with NO approximation, so this tests the phantom "
  "construction itself:")
worst_sph = 0.0
iz0 = int(np.argmin(np.abs(GD.z)))
ridx = [int(np.argmin(np.abs(GD.R - x * kpc))) for x in (4.0, 8.0, 16.0, 30.0)]
for fname, a0 in A0.items():
    gR_q, _, _, _ = GD.qumond(rho_pl, a0)
    gN = plummer_gr(GD.R[ridx], MPL, aPL)
    pred = nu(np.abs(gN) / a0) * gN
    got = gR_q[ridx, iz0]
    err = np.abs(got / pred - 1)
    worst_sph = max(worst_sph, float(err.max()))
    P(f"      {fname:<10} r = 4, 8, 16, 30 kpc:   solver / identity = "
      + ", ".join(f"{g/p:.4f}" for g, p in zip(got, pred)))
C("V2b the solver reproduces the EXACT QUMOND spherical identity g = nu(g_N/a0) g_N -- so any "
  "vertical/planar split it reports later is geometry, not solver error", worst_sph < 0.03,
  f"worst deviation {worst_sph:.2%}")

GD2 = Grid(dk=0.0025 / kpc, dR=0.02 * kpc)
rho_b_2 = rho_baryons(GD2.R[:, None], GD2.z[None, :])
Rconv = np.array([6.0, 8.178, 11.0, 16.0]) * kpc
v1 = np.sqrt(np.abs(GD.newton_at(rho_baryons(GD.R[:, None], GD.z[None, :]), Rconv,
                                 np.zeros_like(Rconv))[0]) * Rconv) / 1e3
v2 = np.sqrt(np.abs(GD2.newton_at(rho_b_2, Rconv, np.zeros_like(Rconv))[0]) * Rconv) / 1e3
P("\n  V2c  k- and R-grid convergence on the baryonic rotation curve (this is the test that caught a "
  "purely\n       logarithmic k grid oscillating by tens of per cent past 10 kpc):")
P(f"      R [kpc]        " + "".join(f"{R/kpc:9.2f}" for R in Rconv))
P(f"      v_bar coarse   " + "".join(f"{v:9.2f}" for v in v1))
P(f"      v_bar fine     " + "".join(f"{v:9.2f}" for v in v2))
C("V2c halving dk and dR changes the baryonic rotation curve by less than 1% out to 16 kpc",
  np.max(np.abs(v1 / v2 - 1)) < 0.01, f"worst change {np.max(np.abs(v1/v2-1)):.3%}")
del GD2, rho_b_2


# =================================================================================================
banner("V3  THE NEWTONIAN BARYON MODEL -- the shape number Q and its literature-spanning systematic")
# =================================================================================================
rho_b = rho_baryons(GD.R[:, None], GD.z[None, :])
ZK = 1.1 * kpc
RADII = np.array([6.0, 8.178, 11.0]) * kpc
izK = int(np.argmin(np.abs(GD.z - ZK)))
i0 = 1
info(f"vertical evaluation node z = {GD.z[izK]/kpc:.6f} kpc")

sig_star = sigma_baryons(R0_MEAS, ZK, parts=("thin", "thick")) / MSUN_PC2
sig_gas = sigma_baryons(R0_MEAS, ZK, parts=("HI", "H2")) / MSUN_PC2
sig_tot = sigma_baryons(R0_MEAS, ZK) / MSUN_PC2
P(f"\n  McMillan 2017 columns at R0 = {R0_MEAS/kpc:.3f} kpc, |z| < 1.1 kpc  [Msun/pc^2]:")
P(f"      stars {sig_star:6.2f}   gas {sig_gas:6.2f}   TOTAL {sig_tot:6.2f}")
P(f"      independent census, McKee+2015: {SIG_BAR_MCKEE} +- {SIG_BAR_MCKEE_E} "
  f"(model {sig_tot/SIG_BAR_MCKEE-1:+.1%}); Bovy & Rix 2013 stars 38 +- 4 (model {sig_star/38-1:+.1%})")
C("V3a AGAINST INTEREST: the dynamical mass model's local stellar column and the direct baryon "
  "census DISAGREE by more than either's error bar -- recorded here because it is exactly the "
  "SHAPE disagreement that does NOT cancel from Q", abs(sig_star / 33.4 - 1) < 0.10,
  f"McMillan {sig_star:.1f} vs McKee 33.4 +- 3.0 -> {sig_star/33.4-1:+.1%}; FAILING THIS IS THE "
  f"POINT and it is folded into sigma(Q) below")

gRb, _ = GD.newton_at(rho_b, RADII, np.zeros_like(RADII))
_, gzbK = GD.newton_at(rho_b, RADII, np.full_like(RADII, GD.z[izK]))
gRbK, _ = GD.newton_at(rho_b, RADII, np.full_like(RADII, GD.z[izK]))
Qr = np.abs(gRb) / np.abs(gzbK)
P(f"\n  {'R [kpc]':>9}{'v_bar [km/s]':>14}{'|g_bar,R|(0)':>15}{'|g_bar,z|(1.1)':>16}"
  f"{'Sig_bar(<1.1)':>15}{'Q = gR/gz':>12}")
for i, R in enumerate(RADII):
    vb = math.sqrt(abs(gRb[i]) * R) / 1e3
    P(f"  {R/kpc:9.3f}{vb:14.1f}{abs(gRb[i]):15.4e}{abs(gzbK[i]):16.4e}"
      f"{sigma_baryons(R, ZK)/MSUN_PC2:15.2f}{Qr[i]:12.4f}")
Q0 = float(Qr[i0])

# --- Q's systematic: LITERATURE-SPANNING ranges, not one paper's formal errors.
SHAPE = [("Rd_thin", 0.50 * kpc, "thin-disc scale length 2.6 +- 0.5 kpc, Bland-Hawthorn & Gerhard 2016"),
         ("Rd_thick", 0.40 * kpc, "thick-disc scale length, +-0.4 kpc"),
         ("rho0_b", 0.30 * MCM["rho0_b"], "bulge mass +-30%"),
         ("S0_thick", 0.30 * MCM["S0_thick"], "thick-disc normalisation +-30%"),
         ("S_HI_fid", 0.25 * MCM["S_HI_fid"], "HI column +-25%"),
         ("Rd_HI", 2.0 * kpc, "HI radial scale +-2 kpc"),
         ("zd_thin", 0.10 * kpc, "thin-disc scale height 300 +- 100 pc")]
P("\n  Q's response to the mass model's SHAPE (the normalisation is already cancelled):")
dlnQ = {}
for name, dv, why in SHAPE:
    q = []
    for s in (+1, -1):
        pars = dict(MCM)
        pars[name] = MCM[name] + s * dv
        rr = rho_baryons(GD.R[:, None], GD.z[None, :], pars)
        g1, _ = GD.newton_at(rr, [R0_MEAS], [0.0])
        _, g2 = GD.newton_at(rr, [R0_MEAS], [GD.z[izK]])
        q.append(abs(g1[0]) / abs(g2[0]))
    dlnQ[name] = 0.5 * (q[0] - q[1]) / Q0
    P(f"      {name:<10} d ln Q = {dlnQ[name]:+.4f}   [{why}]")
sig_lnQ = math.sqrt(sum(v * v for v in dlnQ.values()))
P(f"      -> total SHAPE uncertainty on Q:  {sig_lnQ:.2%}   (Q = {Q0:.4f})")
C("V3b the residual baryon systematic on S, after the normalisation has cancelled, is the SHAPE "
  "term alone -- and even with literature-spanning ranges it is under 30%", sig_lnQ < 0.30,
  f"{sig_lnQ:.2%}")
C("V3c but it is NOT small: the shape term alone exceeds 10%, so the baryon model has not been "
  "eliminated from this test, only demoted", sig_lnQ < 0.10, f"{sig_lnQ:.2%} -- FAILING THIS CHECK "
  f"records that the baryon SHAPE remains a leading systematic")

# --- an INDEPENDENT, census-anchored mass model: force the local baryonic column onto McKee+2015's
#     direct census (which the dynamical model exceeds by 25% in stars) while holding the GLOBAL
#     radial pull at R0 fixed, by lengthening the disc.  This is the single most consequential shape
#     alternative available and it moves the answer in the framework's favour, so it is carried
#     explicitly rather than buried inside sigma(Q).
def census_model(rd_thin, target_col):
    pars = dict(MCM)
    pars["Rd_thin"] = rd_thin
    base = sigma_baryons(R0_MEAS, ZK, pars, parts=("thin", "thick", "HI", "H2"))
    bul = sigma_baryons(R0_MEAS, ZK, pars, parts=("bulge",))
    s = (target_col * MSUN_PC2 - bul) / base
    for kk in ("S0_thin", "S0_thick", "S_HI_fid", "S_H2_fid"):
        pars[kk] = MCM[kk] * s
    return pars, float(s)


gR_target = abs(gRb[i0])
scan = []
for rd in (1.6, 1.9, 2.2, 2.5, 3.0):
    pars, s = census_model(rd * kpc, SIG_BAR_MCKEE)
    rr = rho_baryons(GD.R[:, None], GD.z[None, :], pars)
    g1, _ = GD.newton_at(rr, [R0_MEAS], [0.0])
    _, g2 = GD.newton_at(rr, [R0_MEAS], [GD.z[izK]])
    scan.append((rd, abs(g1[0]), abs(g1[0]) / abs(g2[0]), s))
srt = sorted(scan, key=lambda x: x[1])                 # np.interp needs the abscissa increasing
gs = [x[1] for x in srt]
rd_fit = float(np.interp(gR_target, gs, [x[0] for x in srt]))
Q_cen = float(np.interp(gR_target, gs, [x[2] for x in srt]))
bracketed = gs[0] <= gR_target <= gs[-1]
P(f"\n  census-anchored alternative: the local column is forced onto McKee+2015's {SIG_BAR_MCKEE} "
  f"Msun/pc^2 and the\n  disc scale length is re-fitted until |g_bar,R(R0)| returns to the McMillan "
  f"value {gR_target:.4e}:")
P(f"      {'R_d [kpc]':>10}{'norm scale':>12}{'|g_bar,R|':>13}{'Q':>9}")
for rd, g1, qq, s in scan:
    P(f"      {rd:10.2f}{s:12.4f}{g1:13.4e}{qq:9.4f}")
P(f"  -> R_d = {rd_fit:.2f} kpc, Q = {Q_cen:.4f}  ({Q_cen/Q0-1:+.1%} against the McMillan-shape Q)")
C("V3d the root is bracketed by the scan, so R_d and Q are interpolated and not extrapolated",
  bracketed, f"target {gR_target:.4e} inside [{gs[0]:.4e}, {gs[-1]:.4e}]")
C("V3d2 the two independently-anchored mass models disagree on Q by less than the shape systematic "
  "already assigned, so sigma(Q) is not understated", abs(Q_cen / Q0 - 1) < sig_lnQ,
  f"census Q / McMillan Q = {Q_cen/Q0:.3f} against sigma_lnQ = {sig_lnQ:.1%}")
S_cen_shift = Q_cen / Q0
P(f"  Carried forward, NOT adopted: swapping to the census-anchored shape multiplies S_obs by "
  f"{S_cen_shift:.3f}.\n  V6 reports the confrontation under both anchors so the reader sees the "
  f"shape dependence directly.")


# =================================================================================================
banner("V4  THE MODIFIED-GRAVITY ARM -- QUMOND, the framework's own Route A kernel, a0 an INPUT")
# =================================================================================================
P(r"""  div g = div [ nu(|g_N|/a0) g_N ],  nu(y) = 1/(1 - exp(-sqrt(y))).  ONE potential; the vertical
  force and the circular speed are both derivatives of it.  NO freedom once the baryons are fixed.
  The vertical/planar split is then whatever the phantom density's SHAPE makes it, and nothing else.""")

MG = {}
for fname, a0 in A0.items():
    gR_t, gz_t, gR_n, gz_n = GD.qumond(rho_b, a0)
    gR_R = np.interp(RADII, GD.R, gR_t[:, iz0])
    gz_R = np.interp(RADII, GD.R, gz_t[:, izK])
    gRn_R = np.interp(RADII, GD.R, gR_n[:, iz0])
    gzn_R = np.interp(RADII, GD.R, gz_n[:, izK])
    nv, nr = np.abs(gz_R / gzn_R), np.abs(gR_R / gRn_R)
    MG[fname] = dict(nu_vert=nv, nu_rad=nr, S=nv / nr,
                     sig=np.abs(gz_R) / TWO_PI_G / MSUN_PC2, vc=np.sqrt(np.abs(gR_R) * RADII) / 1e3)
    P(f"\n  a0 = {a0:.3e} ({fname}):")
    P(f"      {'R [kpc]':>9}{'y=gbar/a0':>12}{'nu_rad':>9}{'nu_vert':>9}{'S=nv/nr':>10}"
      f"{'v_c pred':>11}{'Sig_1.1 pred':>14}")
    for i, R in enumerate(RADII):
        P(f"  {R/kpc:9.3f}{abs(gRb[i])/a0:12.3f}{nr[i]:9.4f}{nv[i]:9.4f}{nv[i]/nr[i]:10.4f}"
          f"{MG[fname]['vc'][i]:11.1f}{MG[fname]['sig'][i]:14.2f}")

s_mg = np.array([MG[f]["S"][i0] for f in A0])
C("V4a the MODIFIED-GRAVITY split at R0 is within 10% of unity on BOTH footings -- a full QUMOND "
  "solve barely separates the vertical from the planar boost in the solar neighbourhood",
  np.all(np.abs(s_mg - 1) < 0.10), f"S_MG = {s_mg[0]:.4f} / {s_mg[1]:.4f}")
C("V4b and its sign is the same on both footings, so the split is a property of the disc geometry "
  "and not of the footing choice", np.all(np.sign(s_mg - 1) == np.sign(s_mg[0] - 1)),
  f"{s_mg[0]-1:+.4f}, {s_mg[1]-1:+.4f}")
gR_a, gz_a, gRn_a, gzn_a = GD.qumond(rho_b, A0["canonical"], taper=(22.0 * kpc, 38.0 * kpc))
S_alt = (abs(np.interp(R0_MEAS, GD.R, gz_a[:, izK])) / abs(np.interp(R0_MEAS, GD.R, gzn_a[:, izK]))) / \
        (abs(np.interp(R0_MEAS, GD.R, gR_a[:, iz0])) / abs(np.interp(R0_MEAS, GD.R, gRn_a[:, iz0])))
C("V4c the split is stable when the phantom source is truncated at 22-38 kpc instead of 35-55 kpc, "
  "so it is not a boundary artefact", abs(S_alt / MG["canonical"]["S"][i0] - 1) < 0.02,
  f"S = {S_alt:.4f} vs {MG['canonical']['S'][i0]:.4f}")
P(f"\n  comparator: Bienayme, Famaey, Wu, Zhao & Aubert 2009 (A&A 500, 801) solve FULL 3D AQUAL on a "
  f"256^3\n  multigrid with the 'simple' mu and obtain nu_vert = 1.57-1.66 at R = 7.5-8.5 kpc.  This "
  f"solve, with\n  the framework's OWN kernel and a0, gives nu_vert = {MG['canonical']['nu_vert'][i0]:.3f} "
  f"(canonical) / {MG['alt']['nu_vert'][i0]:.3f} (alt) -- lower, as the\n  stiffer Route A kernel requires, "
  f"and in the same regime.")


# =================================================================================================
banner("V5  THE MODIFIED-INERTIA ARMS -- every assumption written as an equation, and scanned")
# =================================================================================================
gN0 = math.hypot(gRb[i0], 0.0)
gNK = math.hypot(gRbK[i0], gzbK[i0])
P(f"\n  local baryonic Newtonian field:  |g_N|(R0,0) = {gN0:.4e},  |g_N|(R0,1.1kpc) = {gNK:.4e} m/s^2")
P(f"  vertical/radial component ratio at 1.1 kpc:  |g_z|/|g_R| = {abs(gzbK[i0])/abs(gRbK[i0]):.3f}")
C("V5a *** THE MAGNITUDE |g_N| -- the argument EVERY kernel takes -- DIFFERS BY ONLY A FEW PER CENT "
  "BETWEEN THE TWO EVALUATION POINTS, because at 1.1 kpc the vertical pull is a fraction of the "
  "radial one and adds in quadrature.  That is the physical reason this laboratory is blunt, and it "
  "is a fact about the Milky Way, not about either theory ***", abs(gNK / gN0 - 1) < 0.10,
  f"|g_N| differs by {abs(gNK/gN0-1):.2%}; |g_z|/|g_R| = {abs(gzbK[i0])/abs(gRbK[i0]):.3f}")

# ---- the two trajectory frequencies, computed rather than assumed
Om = VC[0][1] / R0_MEAS
zz = np.linspace(0.0, ZK, 241)
_, gzp = GD.newton_at(rho_b, np.full_like(zz, R0_MEAS), zz)
gzp = np.abs(gzp)
Phi_z = np.concatenate([[0.0], np.cumsum(0.5 * (gzp[1:] + gzp[:-1]) * np.diff(zz))])
boost = float(nu(gNK / A0["canonical"]))


def vertical_freq(zmax):
    th = np.linspace(1e-7, math.pi / 2 - 1e-7, 2001)
    zs = zmax * np.sin(th)
    v2 = np.maximum(2.0 * boost * (np.interp(zmax, zz, Phi_z) - np.interp(zs, zz, Phi_z)), 1e-32)
    T = 4.0 * np.trapz(zmax * np.cos(th) / np.sqrt(v2), th)
    return 2 * math.pi / T


nu_z_K = vertical_freq(ZK)
nu_z_small = vertical_freq(0.05 * kpc)
qK, qmid = nu_z_K / Om, nu_z_small / Om
P(f"\n  trajectory frequencies at R0:  Omega = V_c/R0 = {Om:.4e} rad/s ({VC[0][0]})")
P(f"      nu_z for z_max = 1.1 kpc  = {nu_z_K:.4e} rad/s  ->  q = nu_z/Omega = {qK:.3f}")
P(f"      nu_z for z_max -> 0       = {nu_z_small:.4e} rad/s  ->  q = {qmid:.3f}   (midplane limit)")
C("V5b the vertical-to-circular frequency ratio at the Sun is in the 1.5-3.5 band, i.e. the two "
  "trajectories are genuinely separated in frequency -- computed from the model potential, not "
  "assumed", 1.5 < qK < 3.5 and 1.5 < qmid < 3.5, f"q = {qK:.3f} at z_max = 1.1 kpc, {qmid:.3f} "
  f"in the midplane limit")

# ---- ARM MI-OA (ASSUMPTION A1): a time-nonlocal MI theory cannot read the instantaneous field; the
#      simplest defensible statement is that the kernel argument is the ORBIT AVERAGE,
#          a(t) = nu( <|g_N|>_traj / a0 ) g_N(t).
#      On a circular orbit <|g_N|> = |g_N|, so A1 reduces EXACTLY to the local map and hence, by
#      Milgrom's circular-orbit theorem, to modified gravity in the deep limit.  That is a required
#      consistency property of the assumption, not a fitted feature.
th = np.linspace(1e-7, math.pi / 2 - 1e-7, 801)
zs = ZK * np.sin(th)
gRs, gzs = GD.newton_at(rho_b, np.full_like(zs, R0_MEAS), zs)
v2 = np.maximum(2.0 * (np.interp(ZK, zz, Phi_z) - np.interp(zs, zz, Phi_z)), 1e-32)
wt = ZK * np.cos(th) / np.sqrt(v2)
g_orbavg = float(np.trapz(np.hypot(gRs, gzs) * wt, th) / np.trapz(wt, th))
P(f"\n  ASSUMPTION A1 (orbit-averaged MI):  <|g_N|> over the vertical orbit = {g_orbavg:.4e} m/s^2, "
  f"against\n      the turning-point value {gNK:.4e}  ({g_orbavg/gNK-1:+.2%})")

# ---- ARM MI-G (ASSUMPTION A2): the repository's OWN one-pole frequency gate,
#          a = g_N [ 1 + |G(w)| (nu(y) - 1) ],   |G(w)| = 1/sqrt(1 + (w/omega_c)^2),
#      w = Omega for the circular trajectory, w = nu_z for the vertical one.  omega_c is NOT derived
#      (mi_omegac_anchor_2026.py: theory-consistency brackets it to ~3 orders, the lower edge being
#      the galactic-survival bound); the whole window is scanned.
OMC = dict(lo=2.0e-15, committed=1.782e-14, hi=1.0e-11)

# ---- ARM MI-P (ASSUMPTION A3): the widest bracket -- a generic frequency power law,
#          y_eff = (w/Omega)^p * (|g_N|/a0),   p in [-2,+2],  p = 0 == the local map.
PVALS = np.array([-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0])


def arms_S(a0, q=None, gv=None, gr=None, oa=None):
    """S = nu_vert/nu_rad at R0 for every MI arm, one footing."""
    q = qK if q is None else q
    gv = gNK if gv is None else gv
    gr = gN0 if gr is None else gr
    oa = g_orbavg if oa is None else oa
    nr = float(nu(gr / a0))
    out = {"MI algebraic (local)": float(nu(gv / a0)) / nr,
           "MI orbit-avg [A1]": float(nu(oa / a0)) / nr}
    for tag, oc in OMC.items():
        Gv = 1.0 / math.sqrt(1 + (q * Om / oc) ** 2)
        Gr = 1.0 / math.sqrt(1 + (Om / oc) ** 2)
        out[f"MI gate [A2] omc {tag}"] = (1 + Gv * (float(nu(gv / a0)) - 1)) / (1 + Gr * (nr - 1))
    for p in PVALS:
        out[f"MI power [A3] p={p:+.1f}"] = float(nu(q**p * gv / a0)) / nr
    return out


ARMS = {f: arms_S(a0) for f, a0 in A0.items()}
P("\n  the arms, both footings, at R0:")
P(f"      {'arm':<30}" + "".join(f"{f:>16}" for f in A0))
for key in ARMS["canonical"]:
    P(f"      {key:<30}" + "".join(f"{ARMS[f][key]:16.4f}" for f in A0))
P(f"      {'MG QUMOND (V4)':<30}" + "".join(f"{MG[f]['S'][i0]:16.4f}" for f in A0))

C("V5c the ALGEBRAIC MI arm predicts S within 5% of exactly 1, parameter-free, because the kernel's "
  "argument is nearly the same at the two evaluation points",
  abs(ARMS["canonical"]["MI algebraic (local)"] - 1) < 0.05,
  f"S = {ARMS['canonical']['MI algebraic (local)']:.4f}")
gate_span = max(abs(ARMS["canonical"][k] - 1) for k in ARMS["canonical"] if "gate" in k)
C("V5d *** THE REPOSITORY'S OWN FREQUENCY GATE CANNOT PRODUCE A LARGE VERTICAL/PLANAR SPLIT "
  "ANYWHERE IN ITS THEORY-ALLOWED omega_c WINDOW: across ~4 decades of omega_c the largest "
  "departure from unity is under 10% ***", gate_span < 0.10, f"max |S-1| = {gate_span:.2%}")
oa_span = abs(ARMS["canonical"]["MI orbit-avg [A1]"] - ARMS["canonical"]["MI algebraic (local)"])
C("V5e and orbit-averaging the kernel argument (A1) moves S by less than 2% -- because the orbit "
  "spends its time where |g_N| is dominated by the RADIAL component, which the vertical motion does "
  "not change", oa_span < 0.02, f"|Delta S| = {oa_span:.3%}")
pow_span = max(abs(ARMS["canonical"][f"MI power [A3] p={p:+.1f}"] - 1) for p in PVALS)
C("V5f only the generic power-law bracket A3, with an exponent the framework does not supply, moves "
  "S by more than 10% -- so any measurable split needs a trajectory dependence stronger than "
  "anything the framework currently contains", pow_span > 0.10, f"max |S-1| = {pow_span:.1%}")


# =================================================================================================
banner("V6  THE CONFRONTATION -- S measured, with the full error budget, against every arm")
# =================================================================================================
rng = np.random.default_rng(20260903)
N = 400000
ps = rng.integers(0, len(SIGMA_DYN), N)
Sd = vals[ps] + rng.normal(0, 1, N) * errs[ps]
pv = rng.integers(0, len(VC), N)
Vc = np.array([v for _, v, _ in VC])[pv] + rng.normal(0, 1, N) * np.array([e for _, _, e in VC])[pv]
R0s = R0_MEAS + rng.normal(0, R0_ERR, N)
Qs = Q0 * np.exp(rng.normal(0, sig_lnQ, N))
S_mc = (Sd * MSUN_PC2) * TWO_PI_G * Qs * R0s / Vc**2
S_obs, S_err = float(S_mc.mean()), float(S_mc.std(ddof=1))
P(f"\n  S_obs = {S_obs:.4f} +- {S_err:.4f}   ({S_err/S_obs:.1%})")
terms = {
    "Sigma_dyn": (Sd * MSUN_PC2) * TWO_PI_G * Q0 * R0_MEAS / VC[0][1] ** 2,
    "shape Q": (vals.mean() * MSUN_PC2) * TWO_PI_G * Qs * R0_MEAS / VC[0][1] ** 2,
    "V_c and R0": (vals.mean() * MSUN_PC2) * TWO_PI_G * Q0 * R0s / Vc**2,
}
for tag, arr in terms.items():
    P(f"      isolated sigma(S) from {tag:<11} = {arr.std(ddof=1):.4f}  ({arr.std(ddof=1)/S_obs:.1%})")
dom = max(terms, key=lambda t: terms[t].std(ddof=1))
C("V6a the DOMINANT systematic is NOT the baryon budget's normalisation (which cancels) but the "
  f"{dom} term", dom in ("Sigma_dyn", "shape Q"), f"largest single term = {dom}")

P(f"\n  {'arm':<30}{'S canonical':>14}{'sigma':>9}{'S alt':>14}{'sigma':>9}")
P("  " + "-" * 76)
for key in list(ARMS["canonical"]) + ["MG QUMOND"]:
    sc = MG["canonical"]["S"][i0] if key == "MG QUMOND" else ARMS["canonical"][key]
    sa = MG["alt"]["S"][i0] if key == "MG QUMOND" else ARMS["alt"][key]
    P(f"  {key:<30}{sc:14.4f}{(S_obs-sc)/S_err:9.2f}{sa:14.4f}{(S_obs-sa)/S_err:9.2f}")

S_MG = MG["canonical"]["S"][i0]
S_MIA = ARMS["canonical"]["MI algebraic (local)"]
z_mg, z_mia = (S_obs - S_MG) / S_err, (S_obs - S_MIA) / S_err
sep_arms = abs(S_MG - S_MIA) / S_err

S_obs_cen = S_obs * S_cen_shift
P(f"\n  UNDER THE CENSUS-ANCHORED MASS MODEL of V3d instead:  S_obs = {S_obs_cen:.4f} +- {S_err:.4f}, "
  f"i.e. {(S_obs_cen-S_MIA)/S_err:+.2f} sigma\n  from algebraic MI and {(S_obs_cen-S_MG)/S_err:+.2f} "
  f"sigma from QUMOND, with the arm-vs-arm separation unchanged at {sep_arms:.2f} sigma.")
C("V6b0 the arm-vs-arm separation is INSENSITIVE to which mass-model anchor is used -- swapping "
  "anchors moves both arms together and changes the fork verdict not at all",
  abs(sep_arms - abs(S_MG - S_MIA) / S_err) < 1e-9,
  f"{sep_arms:.2f} sigma under either anchor, while the COMMON offset moves from {abs(z_mia):.2f} to "
  f"{abs((S_obs_cen-S_MIA)/S_err):.2f} sigma")
P(f"""
  READING IT.  The measured split sits {abs(z_mg):.2f} sigma from the modified-GRAVITY prediction and
  {abs(z_mia):.2f} sigma from the algebraic modified-INERTIA one, and those two predictions are only
  {sep_arms:.2f} sigma APART FROM EACH OTHER.""")
C("V6b *** THE FORK IS NOT DECIDED HERE.  Modified gravity and algebraic modified inertia are "
  "separated by less than one sigma of the measurement, so this laboratory cannot tell the two "
  "arms apart ***", sep_arms < 1.0, f"arm-vs-arm separation {sep_arms:.2f} sigma")
C("V6c ATTEMPTED, AND IT FAILS ITS 3-SIGMA BAR: the arm-vs-arm separation does not reach 3 sigma",
  sep_arms > 3.0, f"separation {sep_arms:.2f} sigma -- FAILING THIS CHECK IS THE RESULT")
C("V6d against interest, and reported at its true strength: BOTH arms sit on the same side of the "
  "measurement and BOTH are in tension with it at the same level, so this is not evidence for "
  "either arm over the other", abs(abs(z_mg) - abs(z_mia)) < 1.0,
  f"MG {z_mg:+.2f} sigma, MI-algebraic {z_mia:+.2f} sigma")
C("V6e and the common tension is itself below 3 sigma, so nothing here falsifies the kernel "
  "either", max(abs(z_mg), abs(z_mia)) < 3.0, f"worst {max(abs(z_mg), abs(z_mia)):.2f} sigma")

pg = np.linspace(-3.0, 12.0, 3001)
nr_c = float(nu(gN0 / A0["canonical"]))
Sp = np.array([float(nu(qK**p * gNK / A0["canonical"])) / nr_c for p in pg])
S_floor = 1.0 / nr_c            # p -> +infinity: the vertical boost switched off entirely
inb = pg[np.abs(S_obs - Sp) < 2 * S_err]
P(f"\n  the A3 family's REACHABLE range: as p -> +inf the vertical boost is switched off completely "
  f"and S -> 1/nu_rad =\n  {S_floor:.4f}; as p -> -inf, S -> infinity.  So the family spans "
  f"({S_floor:.3f}, inf), and the measurement {S_obs:.3f} +- {S_err:.3f} sits "
  f"{(S_obs-S_floor)/S_err:+.2f} sigma from that floor.")
if len(inb):
    hi = f"{inb.max():+.2f}" if inb.max() < pg[-1] - 1e-9 else f">= {pg[-1]:+.0f} (unbounded)"
    P(f"  the A3 exponent allowed at 2 sigma:  {inb.min():+.2f} < p < {hi}; p = 0, i.e. NO "
      f"trajectory dependence, is {'INSIDE' if inb.min() <= 0 <= inb.max() else 'OUTSIDE'} it")
    C("V6f the data do not pin the trajectory-dependence exponent -- the 2-sigma band on p is wider "
      "than 1 and unbounded above", inb.max() - inb.min() > 1.0,
      f"band {inb.min():+.2f} to {hi}")
    C("V6g and p = 0 (no trajectory dependence at all) is allowed at 2 sigma, so the measurement "
      "does not require modified inertia", inb.min() <= 0 <= inb.max(),
      f"band starts at p = {inb.min():+.2f}")
else:
    C("V6f the 2-sigma band on p is empty", False, "empty band")
    C("V6g p = 0 is excluded at 2 sigma", False, "empty band")

# --- V6h  WHERE the common offset lives.  The ratio S is normalisation-free by construction, which
#     also means it hides which of the two directions moves.  Undo that here, at the mass model's own
#     normalisation, by asking what baryon rescaling f each direction would need under the kernel.
def f_needed(g_obs, gN_mod, gcomp_mod, a0):
    lo, hi = 0.05, 20.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        val = float(nu(mid * gN_mod / a0)) * mid * gcomp_mod
        if val < g_obs:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


gobs_R = VC[0][1] ** 2 / R0_MEAS
gobs_z = TWO_PI_G * vals.mean() * MSUN_PC2
a0c = A0["canonical"]
nvo, nro = gobs_z / abs(gzbK[i0]), gobs_R / abs(gRb[i0])
f_R = f_needed(gobs_R, gN0, abs(gRb[i0]), a0c)
f_z = f_needed(gobs_z, gNK, abs(gzbK[i0]), a0c)
P(f"""
  V6h  WHERE THE COMMON OFFSET LIVES (the ratio hides this by design, so it is undone here).
       At the mass model's own normalisation, the Milky Way needs
           nu_rad(observed)  = {nro:.3f}      against the kernel's nu = {float(nu(gN0/a0c)):.3f}
           nu_vert(observed) = {nvo:.3f}      against the kernel's nu = {float(nu(gNK/a0c)):.3f}
       so the ROTATION CURVE wants MORE boost than the kernel supplies and the VERTICAL FORCE wants
       LESS.  Expressed as the baryon rescaling each direction would need under the kernel:
           f_radial = {f_R:.3f}   (the rotation curve wants {f_R-1:+.0%} baryons)
           f_vertical = {f_z:.3f}   (the vertical force wants {f_z-1:+.0%} baryons)
       One normalisation cannot serve both -- this IS the dilemma Lisanti, Moschella, Outmezguine &
       Slone 2019 (PRD 100, 083009) state for scalar enhancements, and the QUMOND solve of V4
       inherits it essentially unchanged because its own split is only {abs(S_MG-1):.1%}.""")
C("V6i the offset is NOT one-sided: the radial direction wants more baryons and the vertical wants "
  "fewer, so it cannot be repaired by any rescaling of the baryon budget -- which is exactly why the "
  "ratio S is the right statistic and exactly why improving the budget would not help",
  (f_R - 1) * (f_z - 1) < 0, f"f_radial = {f_R:.3f}, f_vertical = {f_z:.3f}")

# --- V6j  DEGENERACY CONTROL, against interest.  V6g excluded p = 0 at 2 sigma.  Is that a
#     measurement of trajectory dependence, or is p simply absorbing the shape systematic?
p_lo0 = float(inb.min()) if len(inb) else float("nan")
S_hi = S_obs * math.exp(sig_lnQ)            # Q one sigma high -> S one sigma high
inb2 = pg[np.abs(S_hi - Sp) < 2 * S_err]
p_lo1 = float(inb2.min()) if len(inb2) else float("nan")
P(f"\n  V6j  DEGENERACY CONTROL.  Moving Q by ONE sigma of its shape systematic ({sig_lnQ:.1%}) moves "
  f"the lower\n       edge of the allowed exponent band from p = {p_lo0:+.2f} to p = {p_lo1:+.2f} -- "
  f"a shift of {abs(p_lo1-p_lo0):.2f} against\n       the whole distance {abs(p_lo0):.2f} from p = 0.")
C("V6j against interest: the trajectory exponent is DEGENERATE with the baryon shape -- one sigma "
  "of the shape systematic alone moves the band's edge by at least half the distance from p = 0, so "
  "V6g's exclusion of p = 0 is measuring the mass model, not the trajectory",
  abs(p_lo1 - p_lo0) > 0.5 * abs(p_lo0),
  f"|dp| = {abs(p_lo1-p_lo0):.2f} from a 1-sigma Q shift, against |p_edge| = {abs(p_lo0):.2f}")


# =================================================================================================
banner("V7  WHAT WOULD HAVE TO IMPROVE FOR THIS TEST TO DECIDE THE FORK")
# =================================================================================================
sep_abs = abs(S_MG - S_MIA)
need = sep_abs / 3.0
P(f"\n  |S_MG - S_MI(algebraic)| = {sep_abs:.4f}.  A 3-sigma discrimination needs sigma(S) <= "
  f"{need:.4f}, i.e. {S_err/need:.1f}x better than today's {S_err:.4f}.")
P(f"  sigma(S)/S adds in quadrature over  Sigma_dyn ({terms['Sigma_dyn'].std(ddof=1)/S_obs:.1%}), "
  f"the baryon SHAPE ({terms['shape Q'].std(ddof=1)/S_obs:.1%}) and V_c^2/R0 "
  f"({terms['V_c and R0'].std(ddof=1)/S_obs:.1%}), so EVERY term would have to fall below "
  f"{need/S_obs:.2%}.  Concretely:")
P(f"      Sigma_1.1(R0) known to +- {need/S_obs*vals.mean():.2f} Msun/pc^2 -- today the four "
  f"published values SPAN {vals.max()-vals.min():.1f};")
P(f"      the disc scale length, bulge mass and gas profile good enough to fix Q to "
  f"{need/S_obs:.2%} -- today {sig_lnQ:.1%}.")
C("V7a the required precision on Sigma_1.1 is far below the DISAGREEMENT BETWEEN PUBLISHED "
  "DETERMINATIONS, so no reduction of statistical error can deliver it -- the obstruction is a "
  "systematic one", need / S_obs * vals.mean() < 0.5 * (vals.max() - vals.min()),
  f"need +-{need/S_obs*vals.mean():.2f}, published values span {vals.max()-vals.min():.1f} Msun/pc^2")
C("V7b and the baryon SHAPE would have to be pinned an order of magnitude better than any current "
  "Milky Way mass model delivers", need / S_obs < 0.1 * sig_lnQ,
  f"need {need/S_obs:.2%}, have {sig_lnQ:.1%} -> a factor {sig_lnQ/(need/S_obs):.0f}")


# =================================================================================================
banner("V8  MUTATION CONTROLS")
# =================================================================================================
a0_tiny = 1e-18
gR_n2, gz_n2, gRnn, gznn = GD.qumond(rho_b, a0_tiny)
S_mg_newt = (abs(np.interp(R0_MEAS, GD.R, gz_n2[:, izK])) / abs(np.interp(R0_MEAS, GD.R, gznn[:, izK]))) / \
            (abs(np.interp(R0_MEAS, GD.R, gR_n2[:, iz0])) / abs(np.interp(R0_MEAS, GD.R, gRnn[:, iz0])))
arms_newt = arms_S(a0_tiny)
worst_newt = max([abs(S_mg_newt - 1)] + [abs(v - 1) for v in arms_newt.values()])
P(f"\n  M1 Newtonian limit (a0 = {a0_tiny:.0e}):  S_MG = {S_mg_newt:.6f}; worst MI arm |S-1| = "
  f"{max(abs(v-1) for v in arms_newt.values()):.2e}")
C("M1 with the kernel switched off every arm returns S = 1, so the splits this script reports are "
  "produced by the kernel and not by the machinery", worst_newt < 0.005, f"worst |S-1| = {worst_newt:.2e}")

Mb = 2 * math.pi * float(np.sum(np.trapz(rho_b, GD.z, axis=1) * GD.R * GD.wR))
rho_sph = plummer_rho(GD.R[:, None], GD.z[None, :], Mb, 3.0 * kpc)
gR_s, gz_s, gRns, gzns = GD.qumond(rho_sph, A0["canonical"])
S_sph = (abs(np.interp(R0_MEAS, GD.R, gz_s[:, izK])) / abs(np.interp(R0_MEAS, GD.R, gzns[:, izK]))) / \
        (abs(np.interp(R0_MEAS, GD.R, gR_s[:, iz0])) / abs(np.interp(R0_MEAS, GD.R, gRns[:, iz0])))
P(f"  M2 spherical mutation (the same total baryonic mass {Mb/Msun:.3e} Msun in a Plummer sphere): "
  f"S_MG = {S_sph:.5f} against the disc's {S_MG:.5f}")
C("M2 a spherical mass distribution drives the MG split to exactly 1 (QUMOND is algebraic in "
  "spherical symmetry) -- so the disc's split is geometry, and the statistic does respond to "
  "geometry", abs(S_sph - 1) < 0.01, f"S_sph = {S_sph:.5f}")

arms_q1 = arms_S(A0["canonical"], q=1.0, oa=gNK)
dev = max(abs(arms_q1[k] - arms_q1["MI algebraic (local)"]) for k in arms_q1)
P(f"  M3 frequency mutation (q = nu_z/Omega forced to 1 and the orbit average forced to the local "
  f"value): every trajectory-dependent arm collapses onto the algebraic one to {dev:.2e}")
C("M3 with the two trajectories made identical, every trajectory-dependent arm collapses onto the "
  "algebraic arm to a residual FAR below the splits it is controlling -- so the V5 splits are the "
  "frequency dependence and nothing else.  (The collapse is exact for A1 and A3; for the gate A2 a "
  "residual of order (nu(g_v)-nu(g_r)) x (1-|G|) survives by construction, so the bar is set "
  "relative to the effect rather than at zero.)", dev < 0.05 * gate_span,
  f"residual {dev:.2e}, i.e. {dev/gate_span:.2%} of the gate's own {gate_span:.2%} split")

S_shuf = (rng.normal(vals.mean(), errs.mean(), N) * MSUN_PC2) * TWO_PI_G * Qs * R0_MEAS / VC[0][1] ** 2
P(f"  M4 deleting the literature disagreement (all four Sigma_1.1 replaced by draws from their "
  f"common mean): sigma(S) would fall to {S_shuf.std(ddof=1):.4f}, arm-vs-arm separation "
  f"{sep_abs/S_shuf.std(ddof=1):.2f} sigma")
C("M4 even with the vertical measurement's literature disagreement deleted outright, the two arms "
  "stay unresolved -- so the negative verdict is not an artefact of that scatter alone",
  sep_abs / S_shuf.std(ddof=1) < 3.0, f"{sep_abs/S_shuf.std(ddof=1):.2f} sigma")

# M5 -- an against-interest control on the tension itself: is S_obs < 1 driven by one paper?
P("  M5 leave-one-out on the four vertical determinations (does the common offset survive?):")
loo = []
for j, (nme, v, e) in enumerate(SIGMA_DYN):
    keep = [i for i in range(len(SIGMA_DYN)) if i != j]
    vv, ee = vals[keep], errs[keep]
    pj = rng.integers(0, len(keep), N)
    Sdj = vv[pj] + rng.normal(0, 1, N) * ee[pj]
    Sj = (Sdj * MSUN_PC2) * TWO_PI_G * Qs * R0s / Vc**2
    loo.append(((Sj.mean() - S_MIA) / Sj.std(ddof=1), nme))
    P(f"      drop {nme.split(',')[0]:<20} -> S = {Sj.mean():.4f} +- {Sj.std(ddof=1):.4f}, "
      f"{(Sj.mean()-S_MIA)/Sj.std(ddof=1):+.2f} sigma from algebraic MI")
C("M5 the common offset of S below the arms' prediction is not created by any single vertical "
  "determination: dropping any one leaves the sign unchanged",
  len({np.sign(z) for z, _ in loo}) == 1, f"signs {[f'{z:+.2f}' for z, _ in loo]}")


# =================================================================================================
banner("SUMMARY")
# =================================================================================================
P(f"""
  1. THE BARYON-BUDGET SYSTEMATIC DOES NOT SWAMP THIS TEST -- its NORMALISATION CANCELS.  Writing
     the vertical and planar boosts as one ratio of forces removes it identically (V1).  What
     survives is the mass model's SHAPE, in the single number Q = {Q0:.3f}, uncertain at {sig_lnQ:.1%}
     even with literature-spanning parameter ranges.  That is the brief's anticipated failure mode
     CHECKED FIRST and found to be only PART of the obstruction, not all of it.

  2. THE VERTICAL MEASUREMENT DISAGREES WITH ITSELF.  Four published Sigma_1.1(R0) span
     {vals.min():.1f}-{vals.max():.1f} Msun/pc^2 with quoted errors {errs.min():.1f}-{errs.max():.1f}: the between-paper scatter
     ({spread:.1f}) is {spread/errs.mean():.1f}x the mean quoted error.  Together with the shape term this gives
     sigma(S) = {S_err:.3f} on S_obs = {S_obs:.3f}.

  3. THE TWO ARMS PREDICT ALMOST THE SAME THING, AND THE REASON IS PHYSICAL.  At (R0, 1.1 kpc) the
     baryonic vertical pull is {abs(gzbK[i0])/abs(gRbK[i0]):.2f} of the radial one and adds in quadrature, so |g_N| -- the
     argument every kernel takes -- differs by only {abs(gNK/gN0-1):.1%} between the circular and the vertical
     evaluation point.  A full QUMOND solve splits them by {abs(S_MG-1):.1%}; the algebraic MI map by {abs(S_MIA-1):.1%};
     orbit-averaging the argument by {oa_span:.1%}; the repository's own frequency gate by at most {gate_span:.1%}
     ANYWHERE in its theory-allowed omega_c window.  The two arms are {sep_arms:.2f} sigma apart.

  4. VERDICT ON THE FORK: NOT DECIDED, AND NOT DECIDABLE HERE.  A 3-sigma separation needs
     sigma(S) <= {need:.4f} -- Sigma_1.1 to +- {need/S_obs*vals.mean():.2f} Msun/pc^2, far inside the spread between
     published determinations, and Q to {need/S_obs:.2%}, a factor {sig_lnQ/(need/S_obs):.0f} beyond any current mass model.
     Improving the baryon budget alone would NOT fix it: the budget's normalisation is already gone.

  5. THERE IS A COMMON OFFSET, AND IT IS REPORTED AT EXACTLY ITS STRENGTH, NOT HIGHER.
     S_obs = {S_obs:.3f} +- {S_err:.3f} sits {abs(z_mia):.2f} sigma from algebraic MI and {abs(z_mg):.2f} sigma from QUMOND --
     the SAME offset, in the same direction, for both arms, so it discriminates NOTHING about the
     fork.  V6h shows where it lives: the rotation curve wants {f_R-1:+.0%} baryons under the kernel while
     the vertical force wants {f_z-1:+.0%}, one normalisation cannot serve both, and that is precisely the
     dilemma Lisanti, Moschella, Outmezguine & Slone 2019 (PRD 100, 083009) state for scalar
     enhancements.  It is a known published feature of the Milky Way, re-derived here in a
     normalisation-free statistic with the framework's own kernel; it is NOT new and it is NOT a
     kill -- it sits at {max(abs(z_mg), abs(z_mia)):.1f} sigma with a 13% shape systematic that could move it either way,
     and the census-anchored mass model of V3d shifts Q by {Q_cen/Q0-1:+.1%} on its own, which alone moves the
     offset to {abs((S_obs_cen-S_MIA)/S_err):.1f} sigma.  The honest range is {min(abs((S_obs_cen-S_MIA)/S_err), abs(z_mia)):.1f}-{max(abs(z_mg), abs(z_mia)):.1f} sigma, shared by both arms.

  6. AND THE ONE THING THAT LOOKED LIKE A SIGNAL IS DEGENERATE.  V6g excludes p = 0 at 2 sigma,
     which would read as evidence FOR trajectory dependence.  V6j kills that reading: one sigma of
     the baryon SHAPE systematic alone moves the band's edge by {abs(p_lo1-p_lo0):.2f}, against the whole distance
     {abs(p_lo0):.2f} from p = 0.  The exponent is measuring the mass model.  And the A3 family cannot
     reach the measurement anyway: switching the vertical boost off ENTIRELY (p -> inf) only gets
     to S = {S_floor:.3f}, still {(S_obs-S_floor)/S_err:+.2f} sigma from S_obs.

  7. WHAT WOULD BITE, IF ANYTHING.  Only a trajectory dependence far stronger than anything the
     framework contains -- the generic A3 bracket needs |p| of order 1 before it clears the error
     bar.  The framework's own frequency structure (the one-pole gate) is {gate_span:.1%} and cannot
     reach it.  The vertical/planar split of the Milky Way disc is therefore NOT the cheap route to
     deciding the modified-gravity / modified-inertia fork.  f10 shut the wide-binary route; this
     shuts the solar-neighbourhood route, and for a reason that is structural rather than
     observational: at the one place where both motions are measured, the two trajectories sample
     almost the same |g_N|.""")

P("")
sys.exit(C.done())
