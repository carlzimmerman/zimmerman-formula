"""CFG502 environment-model library (FROZEN_CRITERIA.md section 2, cacadd50d). LCDM-equivalent halo model; nothing fitted to lensing.

Units: physical Mpc and Msun (the record's units, h = 0.6736); colossus is called in comoving Mpc/h and Msun/h and converted.
Imports cfg495_lenslib read-only (inverse Moster, Duffy NFW, delta_ta, the shell projector).
"""
import os, sys, math
import numpy as np
from scipy.special import sici, jv
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(LANES, "CFG495_drawdown_shell"))
import cfg495_lenslib as LL                                                  # noqa: E402  (read-only import)
from colossus.cosmology import cosmology                                     # noqa: E402
from colossus.lss import mass_function, bias                                 # noqa: E402

H = LL.H; OM = LL.OM; RHOC0 = LL.RHOC0; G_MPC = LL.G_MPC
COSMO = cosmology.setCosmology("cfg502", params=dict(flat=True, H0=100 * H, Om0=OM, Ob0=0.02237 / H ** 2,
                                                      sigma8=0.8111, ns=0.9649), persistence="")
SIG_SHMR = 0.15
M1_OVER_MMIN = 17.0


def rho_m(z):                     # physical Msun / Mpc^3
    return OM * RHOC0 * (1 + z) ** 3


# ------------------------------------------------------------------ halo mass function and bias (M in Msun, physical units)
LMH = np.arange(10.5, 15.8001, 0.01)
MH = 10 ** LMH


def dndlnM(z):
    """Mpc^-3 per ln M on LMH."""
    return mass_function.massFunction(MH * H, z, mdef="200c", model="tinker08", q_out="dndlnM") * H ** 3


def bias_T10(M, z):
    return bias.haloBias(np.asarray(M, float) * H, z=z, mdef="200c", model="tinker10")


def moster_vec(lMh, z):
    return np.array([LL.moster_ms(x, z) for x in np.atleast_1d(lMh)])


def Mmin(lMs, z):
    return 10 ** LL.inv_moster(lMs, z)


def Nsat_gt(lMt, z, M=MH):
    mm = Mmin(lMt, z)
    return np.maximum(M - mm, 0.0) / (M1_OVER_MMIN * mm)


class HOD:
    """HOD pieces at one z, cached."""
    def __init__(self, z):
        self.z = z
        self.n = dndlnM(z)
        self.fM = moster_vec(LMH, z)
        self.b = bias_T10(MH, z)

    def cen_w(self, lMs):           # P(M | cen, M*) x phi_c, per ln M
        g = np.exp(-0.5 * ((lMs - self.fM) / SIG_SHMR) ** 2) / (SIG_SHMR * math.sqrt(2 * math.pi))
        return self.n * g

    def sat_w(self, lMs, d=0.01):   # -dN_sat(>M*|M)/dlog M* x n, per ln M
        dn = (Nsat_gt(lMs - d, self.z) - Nsat_gt(lMs + d, self.z)) / (2 * d)
        return self.n * np.maximum(dn, 0.0)

    def pieces(self, lMs, pW, lMlim, isolate=True):
        """returns dict: f_par, f_W, b_c, b_h, host weights (per LMH, normalised), passage means."""
        wc = self.cen_w(lMs); ws = self.sat_w(lMs)
        lnstep = math.log(10) * 0.01
        phic = wc.sum() * lnstep; phis = ws.sum() * lnstep
        fpar = phis / (phis + phic)
        lMt = max(lMs - 1.0, lMlim)
        Nq = Nsat_gt(lMt, self.z)
        if isolate:
            Pc = np.exp(-pW * Nq); Ps = (1 - pW) * np.exp(-pW * Nq)
        else:
            Pc = np.ones_like(MH); Ps = np.ones_like(MH)
        wcp = wc * Pc; wsp = ws * Ps
        Pc_m = wcp.sum() / wc.sum(); Ps_m = wsp.sum() / ws.sum()
        fW = fpar * Ps_m / (fpar * Ps_m + (1 - fpar) * Pc_m)
        hw = wsp / wsp.sum()
        cw = wcp / wcp.sum()
        return dict(f_par=fpar, f_W=fW, b_c=float((cw * self.b).sum()), b_h=float((hw * self.b).sum()), host_w=hw, cen_w=cw,
                    Pc_mean=Pc_m, Ps_mean=Ps_m, lMh_cen_mean=float((cw * LMH).sum()), lMh_host_mean=float((hw * LMH).sum()),
                    lMh_host_median=float(LMH[np.searchsorted(np.cumsum(hw), 0.5)]), Nq_host_mean=float((hw * Nq).sum()),
                    Nq_cen_mean=float((cw * Nq).sum()))


# ------------------------------------------------------------------ truncated NFW in Fourier space; offset host term (Hankel)
def nfw_params(M200, z):
    Menc, rho, c, r200 = LL.nfw(M200, z)
    return c, r200


def u_nfw(k, c, r200):
    """normalised Fourier transform of an NFW truncated at r200 (k in 1/Mpc physical)."""
    rs = r200 / c
    x = np.asarray(k, float) * rs
    si1, ci1 = sici((1 + c) * x); si0, ci0 = sici(x)
    mc = math.log(1 + c) - c / (1 + c)
    return (np.sin(x) * (si1 - si0) - np.sin(c * x) / ((1 + c) * x) + np.cos(x) * (ci1 - ci0)) / mc


KH = np.geomspace(1e-4, 3e3, 60000)                    # 1/Mpc physical


def hankel_J2(Fk, R):
    """Int k dk / (2 pi) F(k) J2(k R)  for R array [Mpc]; F on KH."""
    R = np.atleast_1d(R)
    out = np.empty(len(R))
    lk = np.log(KH)
    for i, r in enumerate(R):
        integ = KH * KH * Fk * jv(2, KH * r) / (2 * math.pi)
        out[i] = np.trapz(integ, lk)
    return out


def ds_offset_host(M200, z, R, centred=False):
    """Msun/Mpc^2: truncated-NFW host seen from satellites distributed like the host (u_s = u_h); centred=True: u_s = 1."""
    c, r200 = nfw_params(M200, z)
    uh = u_nfw(KH, c, r200)
    us = np.ones_like(uh) if centred else uh
    return M200 * hankel_J2(uh * us, R)


def ds_nfw_trunc_real(M200, z, R):
    """centred truncated NFW via the record's shell projector (control C4)."""
    Menc, rho, c, r200 = LL.nfw(M200, z)
    r = np.geomspace(1e-5, r200, 4000)
    return LL.dsigma(R, r, Menc(r))


def P2D_proj_frac(M200, z, R1):
    """fraction of a truncated-NFW (host) satellite population within projected radius R1 of the centre."""
    c, r200 = nfw_params(M200, z)
    r = np.geomspace(1e-5, r200, 3000)
    Menc, rho, _, _ = LL.nfw(M200, z)
    Mr = Menc(r)
    Mcyl = LL.dsigma(np.array([R1]), r, Mr)                 # not used directly; compute projected mass explicitly below
    # projected mass inside R1 = M(<R1) + mass of shells r > R1 inside the cylinder
    R = R1
    r1 = r[:-1]; r2 = r[1:]; m = np.diff(Mr); dr = np.diff(r)
    a1 = np.maximum(r1, R); a2 = np.maximum(r2, R)
    F = lambda x: np.sqrt(np.maximum(x * x - R * R, 0.0)) - R * np.arccos(np.minimum(R / x, 1.0))
    Mc = Mr[-1] - (m / dr * (F(a2) - F(a1))).sum()
    return float(Mc / Mr[-1])


# ------------------------------------------------------------------ two-halo shape outside r_ta, and the mean-density hole
def xi_lin_phys(r, z):
    rc = np.asarray(r, float) * (1 + z) * H                  # comoving Mpc/h
    return COSMO.correlationFunction(rc, z)


def T2h_shape(R, z, rta, rmax=200.0, n=2500, exclude=True):
    """DeltaSigma [Msun/Mpc^2] of rho_bar xi_lin on r > r_ta (exclude) or on r > 5e-3 Mpc (no exclusion), per unit bias."""
    r0 = rta if exclude else 5e-3
    r = np.geomspace(r0, rmax, n)
    rm = np.sqrt(r[1:] * r[:-1])
    dM = 4 * math.pi * rm ** 2 * rho_m(z) * xi_lin_phys(rm, z) * np.diff(r)
    M = np.concatenate([[0.0], np.cumsum(dM)])
    return LL.dsigma(R, r, M)


def hole(R, z, rta):
    r = np.geomspace(1e-5, rta, 2000)
    return -LL.dsigma(R, r, 4 * math.pi / 3 * r ** 3 * rho_m(z))


def T2h_hankel_noexcl(R, z):
    """b = 1, no exclusion: rho_bar Int k dk/(2pi) P_phys(k) J2(kR) (control C3)."""
    kc = KH / ((1 + z) * H)                                  # comoving h/Mpc
    P = COSMO.matterPowerSpectrum(np.clip(kc, 1e-5, 1e3), z) / H ** 3 / (1 + z) ** 3
    P = np.where(kc < 1e3, P, 0.0)
    return rho_m(z) * hankel_J2(P, R)


def w_p_lin(R1, z, pimax=300.0):
    """Int_{R<R1} d^2R Int dpi xi_lin  [Mpc^4 ... -> count factor], physical Mpc: returns Int over disc of w_p(R)."""
    Rg = np.linspace(1e-3, R1, 60); pig = np.linspace(-pimax, pimax, 4001)
    rr = np.sqrt(Rg[:, None] ** 2 + pig[None, :] ** 2)
    xi = xi_lin_phys(rr.ravel(), z).reshape(rr.shape)
    wp = np.trapz(xi, pig, axis=1)
    return float(np.trapz(2 * math.pi * Rg * wp, Rg))


def r_ta_lcdm(lMs, z):
    """LCDM-equivalent r_ta (cfg495 lens_model's definition) and M200c of the lens."""
    M200 = 10 ** LL.inv_moster(lMs, z)
    Menc, rho, c, r200 = LL.nfw(M200, z)
    rho_ta = OM * RHOC0 * (1 + z) ** 3 * LL.dta(z)
    rta = math.exp(brentq(lambda lr: math.log(float(Menc(math.exp(lr)))) - math.log(4 * math.pi / 3 * math.exp(3 * lr) * rho_ta),
                          math.log(r200 * 0.5), math.log(r200 * 50)))
    return rta, M200
