"""CFG503 environment-model library. COPY of CFG502's cfg502_envlib.py (cacadd50d / 4dac09899), unchanged below the marked line except
that the SHMR is a parameter (Moster+13 primary = the record's; Behroozi+13 alternative), plus three additions declared in CFG503
FROZEN_CRITERIA.md (f56e146a1): CAMB halofit xi_NL with the Tinker+05 radial bias zeta, the Behroozi+13 SHMR, and the Jacobi tidal radius.
LCDM-equivalent halo model; nothing fitted to lensing.

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
# ---- CFG503 addition: SHMR registry (filled below the CFG502 copy)
SHMR_MS = {}
SHMR_INV = {}
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


def moster_vec(lMh, z, shmr="moster"):
    return np.array([SHMR_MS[shmr](x, z) for x in np.atleast_1d(lMh)])


def Mmin(lMs, z, shmr="moster"):
    return 10 ** SHMR_INV[shmr](lMs, z)


def Nsat_gt(lMt, z, M=MH, shmr="moster"):
    mm = Mmin(lMt, z, shmr)
    return np.maximum(M - mm, 0.0) / (M1_OVER_MMIN * mm)


class HOD:
    """HOD pieces at one z, cached."""
    def __init__(self, z, shmr="moster"):
        self.z = z; self.shmr = shmr
        self.n = dndlnM(z)
        self.fM = moster_vec(LMH, z, shmr)
        self.b = bias_T10(MH, z)

    def cen_w(self, lMs):           # P(M | cen, M*) x phi_c, per ln M
        g = np.exp(-0.5 * ((lMs - self.fM) / SIG_SHMR) ** 2) / (SIG_SHMR * math.sqrt(2 * math.pi))
        return self.n * g

    def sat_w(self, lMs, d=0.01):   # -dN_sat(>M*|M)/dlog M* x n, per ln M
        dn = (Nsat_gt(lMs - d, self.z, shmr=self.shmr) - Nsat_gt(lMs + d, self.z, shmr=self.shmr)) / (2 * d)
        return self.n * np.maximum(dn, 0.0)

    def pieces(self, lMs, pW, lMlim, isolate=True):
        """returns dict: f_par, f_W, b_c, b_h, host weights (per LMH, normalised), passage means."""
        wc = self.cen_w(lMs); ws = self.sat_w(lMs)
        lnstep = math.log(10) * 0.01
        phic = wc.sum() * lnstep; phis = ws.sum() * lnstep
        fpar = phis / (phis + phic)
        lMt = max(lMs - 1.0, lMlim)
        Nq = Nsat_gt(lMt, self.z, shmr=self.shmr)
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


def r_ta_lcdm(lMs, z, shmr="moster"):
    """LCDM-equivalent r_ta (cfg495 lens_model's definition) and M200c of the lens."""
    M200 = 10 ** SHMR_INV[shmr](lMs, z)
    Menc, rho, c, r200 = LL.nfw(M200, z)
    rho_ta = OM * RHOC0 * (1 + z) ** 3 * LL.dta(z)
    rta = math.exp(brentq(lambda lr: math.log(float(Menc(math.exp(lr)))) - math.log(4 * math.pi / 3 * math.exp(3 * lr) * rho_ta),
                          math.log(r200 * 0.5), math.log(r200 * 50)))
    return rta, M200


# ====================================================================================================================================
# CFG503 additions (FROZEN_CRITERIA.md sections 2-4)
# ====================================================================================================================================
from scipy.integrate import quad as _quad

SHMR_MS["moster"] = LL.moster_ms
SHMR_INV["moster"] = LL.inv_moster


def delta_vir_BN(z):
    """Bryan & Norman 1998 Delta_vir w.r.t. the critical density."""
    Omz = OM * (1 + z) ** 3 / LL.Ez2(z)
    x = Omz - 1
    return 18 * math.pi ** 2 + 82 * x - 39 * x * x


def mvir_from_m200c(M200, z):
    """Mvir (Bryan-Norman) of the record's Duffy NFW of mass M200c."""
    Menc, rho, c, r200 = LL.nfw(M200, z)
    rhov = delta_vir_BN(z) * RHOC0 * LL.Ez2(z)
    f = lambda lr: math.log(float(Menc(math.exp(lr)))) - math.log(4 * math.pi / 3 * math.exp(3 * lr) * rhov)
    rv = math.exp(brentq(f, math.log(r200 * 0.5), math.log(r200 * 3.0)))
    return float(Menc(rv))


def behroozi_ms_vir(lMvir, z):
    """Behroozi, Wechsler & Conroy 2013 eqs. 3-4, best-fit z-dependent parameters (U, recalled)."""
    a = 1.0 / (1 + z); nu = math.exp(-4 * a * a)
    leps = -1.777 + (-0.006 * (a - 1) + 0.0 * z) * nu - 0.119 * (a - 1)
    lM1 = 11.514 + (-1.793 * (a - 1) - 0.251 * z) * nu
    al = -1.412 + (0.731 * (a - 1)) * nu
    de = 3.508 + (2.608 * (a - 1) - 0.043 * z) * nu
    ga = 0.316 + (1.319 * (a - 1) + 0.279 * z) * nu
    f = lambda x: -math.log10(10 ** (al * x) + 1) + de * (math.log10(1 + math.exp(x))) ** ga / (1 + math.exp(10 ** (-x)))
    return leps + lM1 + f(lMvir - lM1) - f(0.0)


def behroozi_ms(lM200c, z):
    return behroozi_ms_vir(math.log10(mvir_from_m200c(10 ** lM200c, z)), z)


def inv_behroozi(lMs, z):
    return brentq(lambda x: behroozi_ms(x, z) - lMs, 9.0, 16.0)


SHMR_MS["behroozi"] = behroozi_ms
SHMR_INV["behroozi"] = inv_behroozi


# ---------------------------------------------------------------- CAMB halofit (Takahashi+12) xi_NL and the Tinker+05 zeta
class CambXi:
    """xi(r_comoving [Mpc/h], z) for 'nl' (halofit Takahashi) and 'lin' (CAMB linear), tabulated on given z values."""
    def __init__(self, zs, kmax_camb=200.0):
        import camb
        pars = camb.CAMBparams()
        pars.set_cosmology(H0=100 * H, ombh2=0.02237, omch2=0.1200, mnu=0.06, omk=0.0)
        pars.InitPower.set_params(As=2.1e-9, ns=0.9649)
        pars.set_matter_power(redshifts=[0.0], kmax=10.0)
        r = camb.get_results(pars)
        s8 = float(r.get_sigma8_0())
        pars.InitPower.set_params(As=2.1e-9 * (0.8111 / s8) ** 2, ns=0.9649)
        pars.NonLinearModel.set_params(halofit_version="takahashi")
        self.sigma8 = {}
        zs = sorted(set(float(z) for z in zs))
        self.zs = np.array(zs)
        self.P = {}
        for nl in (False, True):
            pk = camb.get_matter_power_interpolator(pars, nonlinear=nl, hubble_units=True, k_hunit=True, kmax=kmax_camb,
                                                    zmin=0.0, zmax=max(zs) + 0.05, nz_step=4)
            self.P[nl] = pk
        res = camb.get_results(pars)
        self.sigma8_0 = float(res.get_sigma8_0())
        self.kmax = kmax_camb
        self.RG = np.geomspace(0.01, 400.0, 420)            # comoving Mpc/h
        self.tab = {}
        for nl in (False, True):
            for z in zs:
                self.tab[(nl, z)] = self._xi_table(nl, z)

    def Pk(self, nl, z, k):
        """P [(Mpc/h)^3] at k [h/Mpc]; beyond kmax extended with the local log-slope (0.75-1.0 kmax); taper exp(-(k/300)^2)."""
        k = np.atleast_1d(np.asarray(k, float))
        pk = self.P[nl]
        kin = np.clip(k, 1e-5, self.kmax)
        P = pk.P(z, kin)
        k1, k2 = 0.75 * self.kmax, self.kmax
        sl = math.log(float(pk.P(z, k2)) / float(pk.P(z, k1))) / math.log(k2 / k1)
        P = np.where(k > self.kmax, float(pk.P(z, k2)) * (k / k2) ** sl, P)
        return P * np.exp(-(k / 300.0) ** 2)

    def _xi_table(self, nl, z):
        lk = np.linspace(math.log(1e-5), math.log(3000.0), 6000)
        kk = np.exp(lk)
        lP = np.log(self.Pk(nl, z, kk))
        from scipy.interpolate import CubicSpline
        sp = CubicSpline(lk, lP)
        edges = [1e-5, 1e-3, 1e-2, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 3000.0]
        out = np.zeros(len(self.RG))
        for i, r in enumerate(self.RG):
            tot = 0.0
            for a, b in zip(edges[:-1], edges[1:]):
                f = lambda k: k * math.exp(float(sp(math.log(k))))
                tot += _quad(f, a, b, weight="sin", wvar=r, limit=400)[0]
            out[i] = tot / (2 * math.pi ** 2 * r)
        return out

    def xi(self, nl, rc, z):
        """linear interpolation in log r between tabulated z (exact at the table z)."""
        rc = np.asarray(rc, float)
        j = int(np.argmin(np.abs(self.zs - z)))
        if abs(self.zs[j] - z) > 1e-9:
            raise ValueError("z not tabulated")
        return np.interp(np.log(rc), np.log(self.RG), self.tab[(nl, float(self.zs[j]))])


def zeta_T05(xi_nl):
    """Tinker+05 eq. B7 radial (scale-dependent) halo bias (U, recalled)."""
    x = np.asarray(xi_nl, float)
    return (1 + 1.17 * x) ** 1.49 / (1 + 0.69 * x) ** 2.09


def T2h_shape_gen(R, z, rta, xi_fn, rmax=200.0, n=2500, exclude=True):
    """as CFG502's T2h_shape but with a supplied xi_fn(r_phys [Mpc], z) -> xi_hm / b."""
    r0 = rta if exclude else 5e-3
    r = np.geomspace(r0, rmax, n)
    rm = np.sqrt(r[1:] * r[:-1])
    dM = 4 * math.pi * rm ** 2 * rho_m(z) * xi_fn(rm, z) * np.diff(r)
    M = np.concatenate([[0.0], np.cumsum(dM)])
    return LL.dsigma(R, r, M)


def T2h_hankel_noexcl_P(R, z, Pfun_h):
    """b = 1, no exclusion, rho_bar Int k dk/(2pi) P_phys(k) J2(kR) for a supplied P(k [h/Mpc]) [(Mpc/h)^3] (control C3n)."""
    kc = KH / ((1 + z) * H)
    P = Pfun_h(np.clip(kc, 1e-5, 3e3)) / H ** 3 / (1 + z) ** 3
    P = np.where(kc < 3e3, P, 0.0)
    return rho_m(z) * hankel_J2(P, R)


# ---------------------------------------------------------------- tidal stripping (Jacobi radius, circular orbit)
ND = 20


def host_D_and_A(lMh, z):
    """D quantiles (enclosed-mass fractions (i + 0.5)/ND of the host NFW truncated at r200) and A = M_h(<D)(3 - dlnM/dlnr)/D^3."""
    Menc, rho, c, r200 = LL.nfw(10 ** lMh, z)
    rr = np.geomspace(1e-5 * r200, r200, 4000)
    fr = Menc(rr) / Menc(r200)
    q = (np.arange(ND) + 0.5) / ND
    D = np.exp(np.interp(q, fr, np.log(rr)))
    MD = Menc(D)
    s = 4 * math.pi * D ** 3 * rho(D) / MD
    return D, MD * (3 - s) / D ** 3


def tidal_rt(lMsat, z, rta_sat, A):
    """r_t solving m(<r_t)/r_t^3 = A for the satellite's Duffy NFW (M200c = 10**lMsat); capped at rta_sat (returned as inf)."""
    Menc, rho, c, r200 = LL.nfw(10 ** lMsat, z)
    rr = np.geomspace(1e-6, rta_sat, 3000)
    lmb = np.log(Menc(rr) / rr ** 3)                         # decreasing
    la = np.log(np.asarray(A, float))
    rt = np.exp(np.interp(-la, -lmb, np.log(rr)))
    return np.where(la < lmb[-1], np.inf, rt)
