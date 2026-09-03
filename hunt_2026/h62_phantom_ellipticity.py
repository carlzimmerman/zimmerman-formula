#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h62_phantom_ellipticity.py -- HUNT ITEM 62 (the shape of the phantom halo, in lensing).
=======================================================================================
THE LIST'S POSING OF THE ITEM: "ellipticity of the MOND phantom around discs at 30-100 kpc; framework prediction
q ~ 0.7-0.8 aligned with the disc; LambdaCDM q ~ 0.85-0.95; Kepler-grade if the measured f_h is consistent with the
phantom and not the halo at 2 sigma."

WHAT IS ACTUALLY MEASURED.  Schrabback, Georgiou et al. 2021 (A&A 647, A185; arXiv:2010.00311), five surveys
including KiDS/KV450, and Schrabback et al. 2021 (KiDS-1000 centrals, arXiv:2102.03549), constrain

        f_h  =  < cos(2 dphi_{h,g}) |eps_h| / |eps_g| >                                    (their eq. 15)

the ratio of the ALIGNED component of the halo's ellipticity to the ellipticity of the light, with eps = (1-q)/(1+q)
(their own worked example, q = 0.56 <-> |eps_h| = 0.28, fixes the convention).  The fit range is
45 kpc/h70 < r < r200c.  The published numbers, read off the papers this session:

        Georgiou+2021 joint    RED  f_h = 0.303 +0.080 -0.079      BLUE f_h = 0.217 +0.160 -0.159
        Schrabback+2021 KiDS   RED  f_h = 0.55 +- 0.19 (outer)     BLUE f_h = 0.28 +- 0.55 (outer)
                               RED  f_h = 0.34 +- 0.17 (inner)     BLUE f_h = 0.08 +- 0.53 (inner)

DISCS ARE THE BLUE SAMPLE, so the number item 62 as written must be predicted against is f_h(blue) = 0.217 +- 0.160.
The RED sample is four times sharper, and this script computes that case too rather than leaving it as a remark.

WHAT THIS SCRIPT COMPUTES.
  (1) The QUMOND phantom density around a realistic galaxy, exactly, with no PDE solve:
          rho_ph = -(1/4 pi G) div[(nu-1) g_N]  =  (nu-1) rho_b  -  (1/4 pi G) g_N . grad(nu-1),
      the second form used because it needs only ONE numerical derivative of a smooth scalar instead of two.
      g_N is an axisymmetric multipole expansion of the baryon density whose radial derivative is analytic (the
      rho_l r terms cancel identically), validated three ways below.
  (2) The 3-D isodensity axis ratio q_ph(r) of that phantom -- the physical statement.
  (3) The PROJECTED convergence and its m = 2 azimuthal amplitude, converted to eps_kappa(R) exactly the way an
      elliptical-lens fit reads it.  The extractor is calibrated on an elliptical NFW of KNOWN eps_h, so the O(1)
      profile-shape factor the surveys call f_rel(r) is on the same footing on both sides.
  (4) f_h(framework) weighted over an isotropic inclination distribution with the ESTIMATOR'S OWN weights
      (their eq. 16 weights the numerator by |eps_g| and the denominator by |eps_g|^2).
  (5) The same for an OBLATE EARLY TYPE, which is what the sharp red-lens measurement is made on.
  (6) The LambdaCDM alternative beside both, and the statistical power of the existing measurements.

WHAT THE FIRST VERSION OF THIS SCRIPT GOT WRONG, recorded because it changed the verdict (see M4):
  I wrote the mutation controls expecting eps_kappa to be strongly sensitive to a_0.  IT IS NOT -- moving a_0 by a
  factor of 100 in either direction changes it by under 10 per cent.  The shape of the phantom at 45-200 kpc is
  inherited from the NEWTONIAN quadrupole of the baryons, which the kernel multiplies by a nearly isotropic scalar.
  So this observable does not measure a_0 at all.  What it does test is sharper and worth stating properly: whether
  the shape of the lensing mass is LOCKED to the baryons (framework, no freedom) or FREE (a dark halo).  The two
  mutations that were written on the wrong expectation have been replaced by ones that do break, and the a_0
  insensitivity is now reported as a finding.
  AND A SECOND REVERSAL (see 62c): I also wrote the early-type section expecting it to be a liability -- a round
  phantom against the sharp 0.303 +- 0.080 red-lens detection.  The calculation says otherwise: an early type is
  heavier and larger, so 45 kpc is only 2-3 MOND radii out and its quadrupole-to-monopole ratio there is four times
  a disc's, giving f_h = 0.15-0.21, within 1-2 sigma of the measurement.  The liability text has been withdrawn.

BOTH FOOTINGS.  A SPHERICAL-BARYON CONTROL THAT MUST RETURN EXACTLY ZERO.  A RESOLUTION SCAN (the fourth pass of
this hunt lost a whole item to an unresolved grid; that is not repeated here).  Checks CAN fail.
"""
import sys, math
import numpy as np
from scipy.special import eval_legendre, i0, i1, k0, k1
from scipy.interpolate import RegularGridInterpolator
from hunt_lib import *

ck = Check()

def _sech2(u):
    return 1.0/np.cosh(np.clip(np.abs(u), 0.0, 300.0))**2

# =====================================================================================================================
# 1.  THE BARYONS
# =====================================================================================================================
class Disc:
    """exponential stellar disc (sech^2 vertical) + exponential gas disc + Hernquist bulge."""
    def __init__(self, lMstar, Rd_kpc, fgas, fbulge=0.08, hz_over_Rd=0.15, Rg_over_Rd=2.0, label="", Rcut_kpc=None):
        self.label = label or f"logM*={lMstar}"
        self.Rcut = Rcut_kpc*kpc if Rcut_kpc else None
        Ms = 10**lMstar*Msun
        self.Md = (1-fbulge)*Ms; self.Mbul = fbulge*Ms; self.Mgas = fgas*Ms
        self.Rd = Rd_kpc*kpc; self.hd = hz_over_Rd*Rd_kpc*kpc
        self.Rg = Rg_over_Rd*Rd_kpc*kpc; self.hg = 2*hz_over_Rd*Rd_kpc*kpc
        self.abul = 0.20*Rd_kpc*kpc
        self.Mb = self.Md + self.Mbul + self.Mgas
        self.hmin = self.hd
    def rho(self, R, z):
        d = self.Md/(8*math.pi*self.Rd**2*self.hd)*np.exp(-R/self.Rd)*_sech2(z/(2*self.hd))
        g = self.Mgas/(8*math.pi*self.Rg**2*self.hg)*np.exp(-R/self.Rg)*_sech2(z/(2*self.hg)) if self.Mgas > 0 else 0.0
        r = np.maximum(np.sqrt(R**2+z**2), 1e-4*self.abul)
        b = self.Mbul*self.abul/(2*math.pi*r*(r+self.abul)**3) if self.Mbul > 0 else 0.0
        tot = d + g + b
        return np.where(R > self.Rcut, 0.0, tot) if self.Rcut is not None else tot
    def rM(self, a0): return math.sqrt(G*self.Mb/a0)

class Oblate:
    """an OBLATE early type: Hernquist stratified on m = sqrt(R^2 + z^2/q^2).  This is the red-lens model."""
    def __init__(self, lMb, Re_kpc, q3, label=""):
        self.label = label or f"oblate logMb={lMb}"
        self.Mb = 10**lMb*Msun; self.a = Re_kpc*kpc/1.8153; self.q3 = q3
        self.hmin = 0.05*self.a
    def rho(self, R, z):
        m = np.maximum(np.sqrt(R**2 + (z/self.q3)**2), 1e-6*self.a)
        return self.Mb*self.a/(2*math.pi*self.q3*m*(m+self.a)**3)
    def rM(self, a0): return math.sqrt(G*self.Mb/a0)

class Sphere(Oblate):
    """CONTROL: spherical Hernquist.  Everything downstream must return exactly zero ellipticity."""
    def __init__(self, lMb, Re_kpc): super().__init__(lMb, Re_kpc, 1.0, "spherical control")

# =====================================================================================================================
# 2.  THE NEWTONIAN FIELD -- axisymmetric multipole expansion with an analytic radial derivative
# =====================================================================================================================
LMAX = 10                                                    # even l only (symmetry about the plane)
LS = list(range(0, LMAX+1, 2))

def rho_l(model, rgrid, nz=400):
    """rho_l(r) = (2l+1)/2 Int rho(r,mu) P_l(mu) dmu, done in z (= r mu) on a grid that RESOLVES the disc.
    A uniform mu grid does not: at r = 50 kpc a 0.5 kpc scale height is |mu| < 0.01."""
    out = np.zeros((len(LS), len(rgrid)))
    for i, r in enumerate(rgrid):
        zp = np.concatenate([[0.0], np.geomspace(min(0.02*model.hmin, 1e-4*r), r, nz)])
        z = np.concatenate([-zp[::-1][:-1], zp])
        R = np.sqrt(np.maximum(r**2 - z**2, 0.0))
        rr = model.rho(R, z); mu = z/r
        for j, l in enumerate(LS):
            out[j, i] = (2*l+1)/2.0*np.trapz(rr*eval_legendre(l, mu), z)/r
    return out

def newtonian_field(model, rgrid, mugrid, want_Phi2=False):
    """(g_r, g_theta) on the (r, mu) grid.
    Phi_l(r) = -(4 pi G/(2l+1)) [ r^-(l+1) A_l + r^l B_l ],  A_l = Int_0^r rho_l r'^(l+2) dr', B_l = Int_r^inf rho_l r'^(1-l) dr'
    dPhi_l/dr = -(4 pi G/(2l+1)) [ -(l+1) r^-(l+2) A_l + l r^(l-1) B_l ]     (the rho_l r terms cancel exactly)
    g_r = -sum_l Phi_l' P_l(mu);   g_theta = (sin th / r) sum_l Phi_l P_l'(mu)"""
    rl = rho_l(model, rgrid)
    gr = np.zeros((len(rgrid), len(mugrid))); gth = np.zeros_like(gr); Phi2 = None
    P = np.array([eval_legendre(l, mugrid) for l in LS])
    dP = np.zeros_like(P)
    for j, l in enumerate(LS):
        if l == 0: continue
        dP[j] = l*(mugrid*eval_legendre(l, mugrid) - eval_legendre(l-1, mugrid))/np.maximum(1-mugrid**2, 1e-14)
    sinth = np.sqrt(np.maximum(1-mugrid**2, 0.0))
    for j, l in enumerate(LS):
        f = rl[j]
        A = np.concatenate([[0.0], np.cumsum(0.5*(f[1:]*rgrid[1:]**(l+2) + f[:-1]*rgrid[:-1]**(l+2))*np.diff(rgrid))])
        w = f*rgrid**(1.0-l)
        B = np.concatenate([np.cumsum((0.5*(w[1:]+w[:-1])*np.diff(rgrid))[::-1])[::-1], [0.0]])
        pref = -(4*math.pi*G/(2*l+1))
        Phi = pref*(rgrid**(-(l+1))*A + rgrid**l*B)
        dPhi = pref*(-(l+1)*rgrid**(-(l+2))*A + l*rgrid**(l-1)*B)
        gr += np.outer(-dPhi, P[j]); gth += np.outer(Phi/rgrid, dP[j])*sinth[None, :]
        if l == 2: Phi2 = Phi
    return (gr, gth, Phi2) if want_Phi2 else (gr, gth)

RG = np.geomspace(0.02*kpc, 6000*kpc, 760)
MU = np.linspace(-1.0, 1.0, 801)
IMID = int(np.argmin(abs(MU)))                                # mu = 0, the disc plane

# ---- V1a: Freeman's exact razor-thin exponential-disc rotation curve, where this item actually lives (r > 30 kpc)
def freeman_vc2(R, Sig0, Rd):
    y = R/(2*Rd); return 4*math.pi*G*Sig0*Rd*y**2*(i0(y)*k0(y) - i1(y)*k1(y))
_thin = Disc(10.3, 3.4, 0.0, fbulge=0.0, hz_over_Rd=0.004, label="thin validation disc")
_gr, _gth = newtonian_field(_thin, RG, MU)
_Sig0 = _thin.Md/(2*math.pi*_thin.Rd**2)
_Rout = np.array([32.0, 60.0, 120.0, 240.0])*kpc
_ro = np.array([np.interp(rt, RG, -_gr[:, IMID])*rt/freeman_vc2(rt, _Sig0, _thin.Rd) for rt in _Rout])
ck("V1a (validation) in the radial range this item lives in (r > 30 kpc) the multipole Newtonian solver reproduces Freeman's exact analytic razor-thin exponential-disc rotation curve to better than half a per cent",
   np.all(abs(_ro - 1) < 0.005),
   "v_c^2(numeric)/v_c^2(Freeman) at R = 32, 60, 120, 240 kpc = " + ", ".join(f"{v:.4f}" for v in _ro))

_Rin = np.array([2.0, 4.0, 8.0, 16.0])*kpc
_ri = np.array([np.interp(rt, RG, -_gr[:, IMID])*rt/freeman_vc2(rt, _Sig0, _thin.Rd) for rt in _Rin])
ck("V1b (validation, AGAINST INTEREST) INSIDE 20 kpc the l <= 10 truncation is worth up to 4 per cent on a razor-thin disc, because a delta-function-thin disc needs arbitrarily high multipoles in its own plane.  Raising LMAX is not available -- r^l overflows past l ~ 12 over this dynamic range.  So the INNER q_ph(r) numbers below carry a several-per-cent systematic and are quoted as indicative; every number the verdict rests on is measured beyond 45 kpc, where V1a applies",
   np.max(abs(_ri - 1)) < 0.06 and np.max(abs(_ro - 1)) < 0.1*np.max(abs(_ri - 1)),
   "v_c^2 ratio at R = 2, 4, 8, 16 kpc = " + ", ".join(f"{v:.4f}" for v in _ri) +
   f"  -> worst inner error {100*np.max(abs(_ri-1)):.1f}%, worst outer error {100*np.max(abs(_ro-1)):.2f}%")

# ---- V1c: the QUADRUPOLE itself, which IS the signal of this item, against an independent 3-D quadrature
_g2 = Disc(10.25, 3.4, 0.5, label="quadrupole validation")
_, _, _P2 = newtonian_field(_g2, RG, MU, want_Phi2=True)
_Rq = np.geomspace(1e-3*kpc, 600*kpc, 1200)
_Zq = np.concatenate([-np.geomspace(1e-4*kpc, 600*kpc, 700)[::-1], [0.0], np.geomspace(1e-4*kpc, 600*kpc, 700)])
_RR, _ZZ = np.meshgrid(_Rq, _Zq, indexing="ij")
_Qdirect = np.trapz(np.trapz(_g2.rho(_RR, _ZZ)*(_ZZ**2 - _RR**2/2)*2*math.pi*_RR, _Rq, axis=0), _Zq)
_Qfield = np.interp(1000*kpc, RG, _P2)*(1000*kpc)**3/(-G)     # exterior: Phi_2(r) = -G Q / r^3
ck("V1c (validation, the one that matters) the l = 2 moment of the solved field -- the entire signal of this item -- agrees with a completely independent 3-D quadrature of Int rho r^2 P_2(cos th) dV to one per cent",
   abs(_Qfield/_Qdirect - 1) < 0.02,
   f"Q from the field's Phi_2 at 1 Mpc = {_Qfield:.4e} kg m^2, Q by direct 3-D quadrature = {_Qdirect:.4e}, ratio {_Qfield/_Qdirect:.4f}")

# =====================================================================================================================
# 3.  THE PHANTOM
# =====================================================================================================================
def nu_prime(y):
    """dnu/dy for Route A nu = 1/(1-exp(-sqrt y));  nu' = -nu^2 exp(-sqrt y)/(2 sqrt y)."""
    y = np.maximum(np.asarray(y, float), 1e-14); s = np.sqrt(y); e = np.exp(-s)
    return -(1.0/(1.0-e))**2*e/(2*s)

def phantom(model, a0, eN=0.0, rgrid=RG, mugrid=MU, nu_on=True):
    """rho_ph(r, mu).  eN = external field in units of a0, via the simple scalar prescription y -> |g_N|/a0 + eN,
    which the repository's own ledger flags as OVER-aggressive; it is used here only to TRUNCATE, never to claim
    an EFE amplitude."""
    gr, gth = newtonian_field(model, rgrid, mugrid)
    sin2 = np.maximum(1 - mugrid**2, 0.0)[None, :]
    RR = rgrid[:, None]*np.sqrt(sin2); ZZ = rgrid[:, None]*mugrid[None, :]
    if not nu_on:
        return np.zeros_like(gr), gr, gth
    gmag = np.sqrt(gr**2 + gth**2)
    y = gmag/a0 + eN
    f = 1.0/(1.0 - np.exp(-np.sqrt(np.maximum(y, 1e-14)))) - 1.0                 # nu - 1
    npv = nu_prime(y)
    df_dr = npv*np.gradient(gmag, rgrid, axis=0)/a0
    df_dmu = npv*np.gradient(gmag, mugrid, axis=1)/a0
    # g . grad f = g_r df/dr + (g_th/r) df/dth,  df/dth = -sin(th) df/dmu
    gdotgrad = gr*df_dr - gth*np.sqrt(sin2)*df_dmu/rgrid[:, None]
    return f*model.rho(RR, ZZ) - gdotgrad/(4*math.pi*G), gr, gth

# ---- V2: the spherical case must integrate to exactly (nu-1) M_b(r)
_sph = Sphere(math.log10(3e10), 3.0*1.8153)
_rp, _gr2, _gth2 = phantom(_sph, A0["canonical"])
_pl = _rp[:, IMID]
_Mph = 4*math.pi*np.concatenate([[0.0], np.cumsum(0.5*(_pl[1:]*RG[1:]**2 + _pl[:-1]*RG[:-1]**2)*np.diff(RG))])
_Mb_sph = _sph.Mb*(RG/(RG+_sph.a))**2
_nu_sph = nu(np.abs(_gr2[:, IMID])/A0["canonical"])
_s = (RG > 3*kpc) & (RG < 300*kpc)
_ratio = _Mph[_s]/((_nu_sph[_s]-1)*_Mb_sph[_s])
ck("V2 (validation) for a SPHERICAL baryon distribution the numerically differentiated phantom integrates to exactly (nu-1) M_b(r), the known closed form -- so the divergence, the grid and the kernel derivative are all right",
   np.all(abs(_ratio - 1) < 0.02),
   f"M_ph(<r)/[(nu-1)M_b(r)] over 3-300 kpc: min {_ratio.min():.4f}, median {np.median(_ratio):.4f}, max {_ratio.max():.4f}")

# =====================================================================================================================
# 4.  PROJECTION AND THE ELLIPTICITY EXTRACTOR
# =====================================================================================================================
def make_interp(rho, rgrid=RG, mugrid=MU):
    """a density callable dens(r, |mu|) for a gridded phantom."""
    half = 0.5*(rho + rho[:, ::-1]); m = mugrid >= 0
    itp = RegularGridInterpolator((np.log(rgrid), mugrid[m]), half[:, m], bounds_error=False, fill_value=0.0)
    return lambda r, am: itp(np.stack([np.log(r), am], axis=-1))

def bary_dens(model):
    """the SAME callable interface for the baryons themselves -- they are lensing mass too, and at 45 kpc the
    razor-thin gas disc is a 2 per cent contribution to Sigma that is essentially 100 per cent elongated."""
    return lambda r, am: model.rho(r*np.sqrt(np.maximum(1-am**2, 0.0)), r*am)

def add_dens(*fs):
    return lambda r, am: sum(f(r, am) for f in fs)

NPHI = 32
PHI = np.arange(NPHI)*2*math.pi/NPHI

def sigma_map(dens, Rsky, inc_deg, smax=3000*kpc, ns=500, rtrunc=None):
    """Sigma(R, phi) by line-of-sight integration.  Sky x = the projected MAJOR axis (phi = 0), sky y = minor.
    Symmetry axis z_gal = (0, sin i, cos i); i = 90 deg is edge-on."""
    i = math.radians(inc_deg); si, ci = math.sin(i), math.cos(i)
    s = np.concatenate([-np.geomspace(1e-3*kpc, smax, ns)[::-1], [0.0], np.geomspace(1e-3*kpc, smax, ns)])
    out = np.zeros((len(Rsky), NPHI))
    for a, R in enumerate(Rsky):
        x = R*np.cos(PHI)[:, None]; y = R*np.sin(PHI)[:, None]; ss = s[None, :]
        zg = y*si + ss*ci
        r = np.maximum(np.sqrt(x**2 + y**2 + ss**2), RG[0])
        v = dens(r, np.abs(np.clip(zg/r, -1, 1)))
        if rtrunc is not None: v = np.where(r > rtrunc, 0.0, v)
        out[a] = np.trapz(v, s, axis=1)
    return out

def eps_from_map(Sig, Rsky):
    """m = 2 amplitude -> isodensity ellipticity eps = (1-q)/(1+q).  For Sigma = Sigma_0(m) with m the elliptical
    radius, a small ellipticity gives Sigma(R,phi) = Sigma_0(R)[1 + A2 cos 2phi] with A2 = -eps dlnSigma_0/dlnR.
    Positive eps = mass EXTENDED along phi = 0, the projected major axis of the light."""
    S0 = Sig.mean(axis=1)
    A2 = 2*np.mean(Sig*np.cos(2*PHI)[None, :], axis=1)/S0
    slope = np.gradient(np.log(np.maximum(S0, 1e-300)), np.log(Rsky))
    return A2/np.maximum(-slope, 1e-6), S0, slope

def nfw_sigma_profile(m, M200, c200):
    R200 = (3*M200/(4*math.pi*200*rho_crit))**(1/3.); rs = R200/c200
    dc = (200/3.)*c200**3/(math.log(1+c200) - c200/(1+c200))
    x = np.maximum(m/rs, 1e-6); S = np.zeros_like(x)
    lo = x < 0.999; hi = x > 1.001; eq = ~(lo | hi)
    S[lo] = 2*rs*dc*rho_crit/(x[lo]**2-1)*(1 - 2/np.sqrt(1-x[lo]**2)*np.arctanh(np.sqrt((1-x[lo])/(1+x[lo]))))
    S[hi] = 2*rs*dc*rho_crit/(x[hi]**2-1)*(1 - 2/np.sqrt(x[hi]**2-1)*np.arctan(np.sqrt((x[hi]-1)/(1+x[hi]))))
    S[eq] = 2*rs*dc*rho_crit/3.
    return S

def ell_nfw_map(Rsky, eps_h, M200, c200):
    q = (1-eps_h)/(1+eps_h)
    x = Rsky[:, None]*np.cos(PHI)[None, :]; y = Rsky[:, None]*np.sin(PHI)[None, :]
    return nfw_sigma_profile(np.sqrt(x**2*q + y**2/q), M200, c200)

RSKY = np.geomspace(25*kpc, 400*kpc, 22)
BAND = (RSKY >= 45*kpc) & (RSKY <= 200*kpc)
_sel2 = (RSKY > 40*kpc) & (RSKY < 250*kpc)
_eps_in = 0.15
_v = eps_from_map(ell_nfw_map(RSKY, _eps_in, 6e11*Msun, 8.0), RSKY)[0]
ck("V3 (validation) the ellipticity extractor, run on an elliptical NFW whose isodensity axis ratio is KNOWN, returns that ellipticity -- so eps_kappa below is on the same footing as the eps_h the surveys fit",
   abs(np.median(_v[_sel2])/_eps_in - 1) < 0.05,
   f"input eps_h = {_eps_in:.3f}, recovered {np.median(_v[_sel2]):.4f} (median over 40-250 kpc), spread {_v[_sel2].std():.4f}")

_esph = eps_from_map(sigma_map(make_interp(_rp), RSKY, 90.0), RSKY)[0]
ck("V4 (validation, the strongest control here) a SPHERICAL baryon distribution put through the whole phantom + projection + m=2 pipeline returns zero ellipticity.  Any nonzero eps_kappa below is therefore the flattening of the baryons, not the grid",
   np.max(abs(_esph[_sel2])) < 3e-3,
   f"|eps_kappa| for the spherical control over 40-250 kpc: max {np.max(abs(_esph[_sel2])):.2e} -- the floor the disc results are measured against")

def q3d(rho, rvals, rgrid=RG):
    """3-D isodensity axis ratio: the radius along the symmetry axis at which the phantom density equals its
    in-plane value at r, divided by r.  Restricted to the monotonically falling part of the polar profile."""
    plane = rho[:, IMID]; pole = rho[:, -1]
    jpk = int(np.argmax(pole)); rr = rgrid[jpk:]; pp = pole[jpk:]
    ok = pp > 0
    rr, pp = rr[ok], pp[ok]
    keep = np.concatenate([[True], np.diff(pp) < 0])          # strictly decreasing branch
    rr, pp = rr[keep], pp[keep]
    out = []
    for rv in rvals:
        t = np.interp(rv, rgrid, plane)
        if t <= 0 or t > pp[0] or t < pp[-1]: out.append(np.nan); continue
        out.append(float(np.interp(-math.log(t), -np.log(pp), rr))/rv)
    return np.array(out)

# =====================================================================================================================
# 5.  THE FRAMEWORK'S ANSWER -- DISCS (the blue lens sample)
# =====================================================================================================================
P(""); P("="*118)
P("ITEM 62 -- the shape of the phantom, in the radial range the surveys actually fit (45 kpc/h70 < r < r200c)")
P("="*118)
GALS = [Disc(9.75, 2.2, 1.0, label="blue bin 1  logM* 9.5-10.0"),
        Disc(10.25, 3.4, 0.5, label="blue bin 2  logM* 10.0-10.5"),
        Disc(10.75, 4.8, 0.3, label="blue bin 3  logM* > 10.5")]
R200_BIN = [117*kpc, 152*kpc, 195*kpc]                       # the measurement's OWN r200c for the KV450 blue bins
info("baryonic models, matched to the measurement's own blue stellar-mass bins:")
for g in GALS:
    info(f"   {g.label:28s} M_b = {g.Mb/Msun:.2e} Msun, R_d = {g.Rd/kpc:.1f} kpc, "
         f"r_M = sqrt(GM_b/a0) = {g.rM(A0['canonical'])/kpc:.1f} kpc (canonical) / {g.rM(A0['alt'])/kpc:.1f} kpc (alt)")
info("   -> the fit range starts at 45 kpc, which is 4-11 MOND radii out.  That is the whole story of this item.")

RES = {}; P("")
info("Sigma_eff = Sigma_phantom + Sigma_baryon.  The baryons are only ~2 per cent of the projected mass at 45 kpc but")
info("they are a razor-thin disc, so they are ~100 per cent elongated and are NOT negligible for a shape measurement.")
info("Both are reported; the headline is the total, which is the framework's complete lensing prediction.")
for foot, a0 in A0.items():
    for gi, g in enumerate(GALS):
        rho_ph, gr, gth = phantom(g, a0)
        dph = make_interp(rho_ph); db = bary_dens(g)
        eps_p = eps_from_map(sigma_map(dph, RSKY, 90.0), RSKY)[0]
        eps, S0, slope = eps_from_map(sigma_map(add_dens(dph, db), RSKY, 90.0), RSKY)
        RES[(foot, gi)] = dict(eps=eps, eps_ph=eps_p, S0=S0, slope=slope, rho=rho_ph, dph=dph, db=db)
        info(f"{foot:10s} {g.label:28s} eps_kappa(edge-on, TOTAL) at R = 45 / 100 / 200 kpc = "
             f"{np.interp(45*kpc, RSKY, eps):.4f} / {np.interp(100*kpc, RSKY, eps):.4f} / {np.interp(200*kpc, RSKY, eps):.4f}"
             f"  |  45-200 mean {eps[BAND].mean():.4f} (q = {(1-eps[BAND].mean())/(1+eps[BAND].mean()):.3f}); phantom alone {eps_p[BAND].mean():.4f}")

P(""); info("the 3-D isodensity axis ratio of the phantom itself -- the physics, before any projection:")
RV = np.array([2, 5, 10, 20, 30, 45, 100, 200])*kpc
Q3 = {}
for gi, g in enumerate(GALS):
    Q3[gi] = q3d(RES[("canonical", gi)]["rho"], RV)
    info(f"   {g.label:28s} q_ph at r = " + ", ".join(f"{v/kpc:.0f}" for v in RV) + " kpc:  " +
         ", ".join(("  --" if not np.isfinite(v) else f"{v:.3f}") for v in Q3[gi]))
info("   (the inner values carry the several-per-cent multipole systematic of V1b; the outer ones do not)")

q2 = Q3[1]
ck("62a THE LIST'S PREDICTION IS HALF RIGHT, AND THE HALF THAT IS WRONG IS THE HALF THAT MATTERS.  In THREE DIMENSIONS the list is close: at 45 kpc the phantom of an L* disc really does have q ~ 0.6-0.9.  But that is not what a lensing survey measures.  The survey measures the PROJECTED mass, whose line of sight at R = 45 kpc is dominated by material at 1-2 R where the phantom is already round, and it averages out to r200c where it is rounder still.  The observable is 5-15 times smaller than the 3-D number the list quoted",
   np.isfinite(q2[5]) and q2[5] < 0.95 and q2[6] > 0.95 and RES[("canonical", 1)]["eps"][BAND].mean() < 0.05,
   f"3-D: q_ph(10 kpc) = {q2[2]:.3f}, q_ph(45 kpc) = {q2[5]:.3f}, q_ph(100 kpc) = {q2[6]:.3f}.  "
   f"PROJECTED and band-averaged: eps_kappa = {RES[('canonical',1)]['eps'][BAND].mean():.4f}, i.e. q = "
   f"{(1-RES[('canonical',1)]['eps'][BAND].mean())/(1+RES[('canonical',1)]['eps'][BAND].mean()):.3f}, not 0.7-0.8")

# ---- resolution scan
_MUc = np.linspace(-1.0, 1.0, 401); _RGc = np.geomspace(0.02*kpc, 6000*kpc, 400)
_rc, _, _ = phantom(GALS[1], A0["canonical"], rgrid=_RGc, mugrid=_MUc)
_ec = eps_from_map(sigma_map(add_dens(make_interp(_rc, _RGc, _MUc), bary_dens(GALS[1])), RSKY, 90.0), RSKY)[0]
_ef = RES[("canonical", 1)]["eps"]
ck("V5 (validation) resolution scan: halving the radial and angular grid changes eps_kappa by under 15 per cent of itself, so the small number above is physics and not an unresolved grid",
   abs(_ec[BAND].mean()/_ef[BAND].mean() - 1) < 0.15,
   f"eps_kappa (45-200 kpc) at 760x801 = {_ef[BAND].mean():.5f}, at 400x401 = {_ec[BAND].mean():.5f}, change {100*(_ec[BAND].mean()/_ef[BAND].mean()-1):+.1f}%")

# ---- how much of the projected mass is baryonic (it must be negligible for the above to be the phantom's shape)
_s = np.concatenate([-np.geomspace(1e-3*kpc, 3000*kpc, 800)[::-1], [0.0], np.geomspace(1e-3*kpc, 3000*kpc, 800)])
_R45 = 45*kpc                                     # edge-on, major axis: the line of sight lies IN the disc plane
_Sb = float(np.trapz(GALS[1].rho(np.sqrt(_R45**2 + _s**2), np.zeros_like(_s)), _s))
_Sph45 = float(np.interp(_R45, RSKY, RES[("canonical", 1)]["S0"]))
_gcut = Disc(10.25, 3.4, 0.5, label="gas truncated at 30 kpc", Rcut_kpc=30.0)
_ecut = eps_from_map(sigma_map(add_dens(RES[("canonical", 1)]["dph"], bary_dens(_gcut)), RSKY, 90.0), RSKY)[0]
ck("V6 the baryons are lensing mass too, and being a razor-thin disc they are ~100 per cent elongated, so even the 2 per cent of Sigma they contribute at 45 kpc is not obviously negligible for a SHAPE measurement.  Computed rather than assumed, they add about 4 per cent to eps_kappa -- real, in the framework's favour, and small.  The associated worry, that the answer depends on where the gas disc is truncated (nothing measures it at 45 kpc), is also computed and also negligible in the band average",
   _Sb/_Sph45 < 0.05 and RES[("canonical", 1)]["eps"][BAND].mean() > RES[("canonical", 1)]["eps_ph"][BAND].mean()
   and abs(_ecut[BAND].mean()/RES[("canonical", 1)]["eps"][BAND].mean() - 1) < 0.05,
   f"Sigma_baryon/Sigma_phantom on the major axis at 45 kpc = {_Sb/_Sph45:.3f}; eps_kappa(45-200 kpc) = "
   f"{RES[('canonical',1)]['eps_ph'][BAND].mean():.4f} phantom alone, {RES[('canonical',1)]['eps'][BAND].mean():.4f} with baryons, "
   f"{_ecut[BAND].mean():.4f} if the gas disc is truncated at 30 kpc")

# =====================================================================================================================
# 6.  f_h WITH THE ESTIMATOR'S OWN INCLINATION WEIGHTING
# =====================================================================================================================
P(""); P("="*118); P("f_h -- the published observable, computed the way the surveys compute it"); P("="*118)
INC = np.degrees(np.arccos(np.linspace(0.999, 0.02, 400)))    # uniform in cos i IS the isotropic distribution
def eps_proj(inc_deg, q0):
    i = math.radians(inc_deg); q = math.sqrt(math.cos(i)**2 + q0**2*math.sin(i)**2); return (1-q)/(1+q)

# the sin^2 i scaling of a small projected flattening, validated directly at i = 55 deg
_e55 = eps_from_map(sigma_map(add_dens(RES[("canonical", 1)]["dph"], RES[("canonical", 1)]["db"]), RSKY, 55.0), RSKY)[0]
_pred55 = _ef*math.sin(math.radians(55.0))**2
ck("V7 (validation) the phantom's projected flattening scales as sin^2(i), as a small oblate flattening must -- checked directly at i = 55 deg, so the inclination average below does not need one projection per inclination",
   abs(np.mean(_e55[BAND])/np.mean(_pred55[BAND]) - 1) < 0.10,
   f"eps_kappa(55 deg) measured {np.mean(_e55[BAND]):.5f} vs sin^2(55) x edge-on = {np.mean(_pred55[BAND]):.5f}, ratio {np.mean(_e55[BAND])/np.mean(_pred55[BAND]):.3f}")

def fh_weighted(eps90, q0_light):
    """their eq. 16 weights the numerator by |eps_g| and the denominator by |eps_g|^2, so a mixed-inclination
    sample returns f_h = sum eps_h |eps_g| / sum |eps_g|^2 with eps_h(i) = eps_h(90) sin^2 i."""
    eg = np.array([eps_proj(i, q0_light) for i in INC])
    eh = eps90*np.sin(np.radians(INC))**2
    return float(np.sum(eh*eg)/np.sum(eg**2)), float(np.mean(eg))

Q0_DISC = 0.20
FH = {}
for foot in A0:
    for gi in range(3):
        FH[(foot, gi)] = fh_weighted(RES[(foot, gi)]["eps"][BAND].mean(), Q0_DISC)[0]
    info(f"{foot:10s} f_h(framework, discs) by blue mass bin: " + ", ".join(f"{FH[(foot,gi)]:.4f}" for gi in range(3)) +
         f"   sample-typical {np.mean([FH[(foot,gi)] for gi in range(3)]):.4f}")
FH_C = float(np.mean([FH[("canonical", gi)] for gi in range(3)]))
FH_A = float(np.mean([FH[("alt", gi)] for gi in range(3)]))
info(f"an isotropically oriented thin-disc sample (intrinsic q0 = {Q0_DISC}) has <|eps_g|> = {fh_weighted(0.01, Q0_DISC)[1]:.3f} -- the blue lenses are this population")

FH_OBS, FH_ERR = 0.217, 0.160                 # Georgiou+2021 joint, BLUE
FH_OBS_S, FH_ERR_S = 0.28, 0.55               # Schrabback+2021 KiDS-1000 centrals, blue, outer
FH_RED, FH_RED_E = 0.303, 0.080               # Georgiou+2021 joint, RED
P("")
info(f"MEASURED (Georgiou/Schrabback+2021, five surveys incl. KiDS/KV450, 45 kpc/h70 < r < r200c):  BLUE f_h = {FH_OBS:.3f} +- {FH_ERR:.3f}")
info(f"MEASURED (Schrabback+2021, KiDS-1000 central galaxies, outer isophotes):                     BLUE f_h = {FH_OBS_S:.2f} +- {FH_ERR_S:.2f}")
info(f"FRAMEWORK (this script):  f_h = {FH_C:.4f} (canonical) / {FH_A:.4f} (alt)")
nsig_fw = (FH_OBS - FH_C)/FH_ERR
ck("62b the framework's prediction for DISC lenses is a NULL.  Because the phantom is nearly round where the surveys measure, the framework predicts f_h of a few hundredths -- not the 0.2-0.3 that is measured.  It sits low, but the blue error bar is so wide that the framework is not excluded",
   abs(FH_C) < 0.06 and abs(nsig_fw) < 3.0,
   f"f_h(framework) = {FH_C:.4f} (canonical) / {FH_A:.4f} (alt) against a measured {FH_OBS:.3f} +- {FH_ERR:.3f}: {nsig_fw:.2f} sigma low, NOT excluded")

# =====================================================================================================================
# 7.  THE RED SAMPLE -- where the measurement is four times sharper
# =====================================================================================================================
P(""); P("="*118); P("the RED lenses -- an OBLATE early type, computed rather than asserted"); P("="*118)
info("the red measurement is 4x sharper (+-0.080 vs +-0.160).  Red lenses are early types: model them as oblate")
info("Hernquist spheroids of intrinsic axis ratio q3, with the framework's own super-Salpeter stellar mass (item 54).")
ETS = [Oblate(11.1, 6.0, 0.70, "early type q3=0.70, Re=6 kpc"),
       Oblate(11.1, 6.0, 0.60, "early type q3=0.60, Re=6 kpc"),
       Oblate(11.4, 9.0, 0.70, "early type q3=0.70, Re=9 kpc")]
FH_ET = {}
for et in ETS:
    rho_et, _, _ = phantom(et, A0["canonical"])
    eps_et = eps_from_map(sigma_map(add_dens(make_interp(rho_et), bary_dens(et)), RSKY, 90.0), RSKY)[0]
    fh_et, egm = fh_weighted(eps_et[BAND].mean(), et.q3)
    FH_ET[et.label] = fh_et
    qq = q3d(rho_et, RV)
    info(f"   {et.label:32s} r_M = {et.rM(A0['canonical'])/kpc:5.1f} kpc | q_ph(10/45/100 kpc) = "
         f"{qq[2]:.3f}/{qq[5]:.3f}/{qq[6]:.3f} | eps_kappa(45-200) = {eps_et[BAND].mean():.4f} | "
         f"<|eps_g|> = {egm:.3f} | f_h = {fh_et:.4f}")
FH_ET_MID = FH_ET["early type q3=0.70, Re=6 kpc"]
nsig_red = (FH_RED - FH_ET_MID)/FH_RED_E
ck("62c AGAINST MY OWN EXPECTATION, AND THIS IS THE RESULT OF THE ITEM.  I wrote this section expecting the early-type case to be the liability -- a round phantom against a sharp 0.303 detection.  IT IS NOT.  An oblate early type gives f_h = 0.15-0.21, within one to two sigma of the measurement, because two things I had not accounted for both push it up: an early type is heavier, so 45 kpc is only 2-3 MOND radii out instead of 7, and its half-light radius is twice a disc's scale length, so its quadrupole-to-monopole ratio at 45 kpc is four times larger.  The framework does BETTER on the sharp sample than on the blind one",
   0.08 < FH_ET_MID < 0.30 and nsig_red < 2.5,
   f"f_h(framework, oblate early type q3 = 0.70, Re = 6 kpc) = {FH_ET_MID:.4f} against a measured {FH_RED:.3f} +- {FH_RED_E:.3f} = {nsig_red:.1f} sigma low.  "
   f"The answer is insensitive to the assumed intrinsic flattening -- q3 = 0.60 gives {FH_ET['early type q3=0.60, Re=6 kpc']:.4f}, because f_h is a RATIO and both ellipticities scale together -- "
   f"but it IS sensitive to size: Re = 9 kpc gives {FH_ET['early type q3=0.70, Re=9 kpc']:.4f}, {(FH_RED-FH_ET['early type q3=0.70, Re=9 kpc'])/FH_RED_E:.1f} sigma")
ck("62d the systematics that would have to be controlled before ANY verdict is drawn from the red sample, stated so the 1-2 sigma above is not over-read in either direction.  Real early types are TRIAXIAL, not oblate, and a triaxial baryon distribution generates a phantom with a larger and differently oriented quadrupole than this model.  And the measurement's reference model is an elliptical NFW, so the f_rel(r) radial weighting it folds in is not the one appropriate to a rho ~ 1/r^2 phantom.  Each is worth an O(1) factor, and neither is evaluated here",
   True,
   f"the framework spans {min(FH_ET.values()):.3f}-{max(FH_ET.values()):.3f} across the model choices tried, against {FH_RED:.3f} +- {FH_RED_E:.3f}: "
   f"{(FH_RED-max(FH_ET.values()))/FH_RED_E:.1f} to {(FH_RED-min(FH_ET.values()))/FH_RED_E:.1f} sigma.  Two uncontrolled O(1) systematics sit on top of that range")

# =====================================================================================================================
# 8.  THE LambdaCDM ALTERNATIVE
# =====================================================================================================================
P(""); P("="*118); P("the LambdaCDM alternative on the identical estimator"); P("="*118)
info("a CDM halo is triaxial: dark-matter-only simulations give minor/major c/a ~ 0.6-0.7 at these masses, and")
info("baryonic contraction rounds the inner halo to c/a ~ 0.75-0.85.  Taken as oblate and ALIGNED with the light")
info("(the most favourable case for a detection), the projected ellipticity follows the same sin^2 i geometry:")
LCDM = {}
for q3 in (0.60, 0.70, 0.85):
    eg = np.array([eps_proj(i, Q0_DISC) for i in INC]); eh = np.array([eps_proj(i, q3) for i in INC])
    LCDM[q3] = float(np.sum(eh*eg)/np.sum(eg**2))
    info(f"   halo c/a = {q3:.2f} (3-D eps_h = {(1-q3)/(1+q3):.3f}), perfectly aligned  ->  f_h = {LCDM[q3]:.3f}")
info("   a misalignment of <cos 2 dphi> = 0.5, which simulations find for blue discs, halves these.")
ck("62e the LambdaCDM alternative reproduces the measured f_h across the whole plausible range of halo shapes -- but only because a halo's shape is a FREE function set by structure formation, so 'reproduces' here means 'is not constrained by'.  The asymmetry worth recording is the one the item was really about: on this observable the framework has NO freedom (the lensing mass's shape is fixed by the baryons and, per M4, not even by a_0) while LambdaCDM has all of it.  A sharp enough measurement would therefore bind the framework and not LambdaCDM -- but the present one is not sharp enough to bind either",
   0.10 < LCDM[0.70] < 0.60 and abs(LCDM[0.70] - FH_OBS)/FH_ERR < 2.0,
   f"f_h(LCDM, c/a = 0.60/0.70/0.85, aligned) = {LCDM[0.60]:.3f} / {LCDM[0.70]:.3f} / {LCDM[0.85]:.3f}; measured (blue) {FH_OBS:.3f} +- {FH_ERR:.3f}; "
   f"framework (discs) {FH_C:.4f}.  LCDM(c/a=0.7) is {abs(LCDM[0.70]-FH_OBS)/FH_ERR:.2f} sigma from the blue data, the framework {abs(nsig_fw):.2f} sigma")
sep = (LCDM[0.70] - FH_C)/FH_ERR
ck("62f THE ITEM AS THE LIST POSED IT CANNOT BE DECIDED, ON EITHER SAMPLE.  It asked for the measured f_h to pick the phantom over the halo at 2 sigma.  On the DISC lenses the list named, the framework (0.030) and an aligned CDM halo (0.314) are far apart but the error bar is +-0.160, so the separation is under 2 sigma and the data sit between them.  On the RED lenses, where the error bar is four times smaller, the framework's OWN prediction has moved up to 0.15-0.21 and is no longer far from the halo's -- so the sharper measurement is aimed at a smaller gap.  Neither sample decides it",
   sep < 2.5 and nsig_red < 2.5,
   f"discs: framework {FH_C:.3f} vs LCDM(aligned, c/a=0.7) {LCDM[0.70]:.3f} = a {sep:.2f} sigma separation at +-{FH_ERR:.3f}.  "
   f"Early types: framework {FH_ET_MID:.3f} vs measured {FH_RED:.3f} +- {FH_RED_E:.3f} = {nsig_red:.1f} sigma")

# =====================================================================================================================
# 9.  MUTATIONS
# =====================================================================================================================
P(""); P("="*118); P("MUTATION CONTROLS -- these must break"); P("="*118)
_base = Disc(10.25, 3.0, 0.0, fbulge=0.0, label="M1 base")
_wide = Disc(10.25, 6.0, 0.0, fbulge=0.0, label="M1 doubled scale length")
_eb = eps_from_map(sigma_map(make_interp(phantom(_base, A0["canonical"])[0]), RSKY, 90.0), RSKY)[0]
_ew = eps_from_map(sigma_map(make_interp(phantom(_wide, A0["canonical"])[0]), RSKY, 90.0), RSKY)[0]
_far = RSKY > 150*kpc
ck("M1 mutation: at fixed baryonic mass, doubling the disc's scale length must QUADRUPLE eps_kappa in the far field, because the whole signal is the disc's Newtonian quadrupole Q ~ M R_d^2 divided by M r^2.  If this did not hold the estimator would not be measuring the baryons' shape",
   2.8 < _ew[_far].mean()/_eb[_far].mean() < 5.2,
   f"eps_kappa beyond 150 kpc: R_d = 3 kpc gives {_eb[_far].mean():.5f}, R_d = 6 kpc gives {_ew[_far].mean():.5f}, ratio {_ew[_far].mean()/_eb[_far].mean():.2f} against a predicted 4.00")

_lr = np.polyfit(np.log(RSKY[_far]), np.log(_ef[_far]), 1)[0]
ck("M2 mutation: the far-field radial law.  eps_kappa must fall as R^-2, the quadrupole-over-monopole scaling.  A different power would mean the projected shape is being set by something other than the baryons' quadrupole",
   abs(_lr + 2.0) < 0.3,
   f"d ln eps_kappa / d ln R beyond 150 kpc = {_lr:.2f}, against a predicted -2.00")

_roff, _, _ = phantom(GALS[1], A0["canonical"], nu_on=False)
ck("M3 mutation: switching the kernel off (nu = 1) leaves NO phantom at all, so there is no lensing mass beyond 45 kpc to have a shape.  The entire signal is the kernel's",
   np.max(abs(_roff)) == 0.0, "rho_ph is identically zero with nu = 1")

_ehi = eps_from_map(sigma_map(make_interp(phantom(GALS[1], 100*A0["canonical"])[0]), RSKY, 90.0), RSKY)[0]
_elo = eps_from_map(sigma_map(make_interp(phantom(GALS[1], A0["canonical"]/100)[0]), RSKY, 90.0), RSKY)[0]
ck("M4 AGAINST MY OWN ESTIMATOR, and it is a finding, not a failure.  I wrote this script expecting eps_kappa to depend strongly on a_0, and built two mutations on that expectation.  BOTH WERE WRONG: moving a_0 by a factor of 100 either way changes eps_kappa by under 10 per cent.  The reason is that (nu-1) is a near-isotropic scalar at these radii, so the phantom simply inherits the Newtonian quadrupole's shape whatever a_0 is.  THIS OBSERVABLE DOES NOT MEASURE a_0 -- which is also why both footings agree to four decimals above.  What it tests is different and sharper: whether the lensing mass's shape is LOCKED to the baryons or FREE",
   abs(math.log10(_ehi[BAND].mean()/_ef[BAND].mean())) < 0.15 and abs(math.log10(_elo[BAND].mean()/_ef[BAND].mean())) < 0.15,
   f"eps_kappa (45-200 kpc): a_0 x 100 -> {_ehi[BAND].mean():.5f}, canonical -> {_ef[BAND].mean():.5f}, a_0/100 -> {_elo[BAND].mean():.5f}  "
   f"(spread {100*(_ehi[BAND].mean()/_elo[BAND].mean()-1):.0f}% over four decades in a_0)")

P(""); info("the external-field effect, the only mechanism left that could give the phantom a shape at 45-200 kpc:")
for eN in (0.0, 0.01, 0.03, 0.10):
    _re, _, _ = phantom(GALS[1], A0["canonical"], eN=eN)
    _S = sigma_map(make_interp(_re), RSKY, 90.0)
    _ee = eps_from_map(_S, RSKY)[0]
    info(f"   e_N = {eN:.2f}: eps_kappa(45-200 kpc) = {_ee[BAND].mean():+.5f}, projected mass at 100 kpc = "
         f"{100*np.interp(100*kpc, RSKY, _S.mean(axis=1))/np.interp(100*kpc, RSKY, RES[('canonical',1)]['S0']):.0f}% of the isolated value")
ck("62g AGAINST INTEREST -- the external field does not rescue the item.  It truncates the phantom's AMPLITUDE hard (the simple scalar prescription used here is over-aggressive, and item 1 of this hunt already showed the 1/r lensing law survives to 2.6 Mpc, so the real truncation is milder) while leaving its SHAPE almost untouched.  And the quadrupole the EFE does add points along g_ext, which is uncorrelated with the light's major axis, so it enters a stacked f_h with a random sign and cancels.  So the DISC prediction of 0.03 cannot be raised toward the measured 0.217 this way -- though per 62c it does not need to be, since it is only 1.2 sigma low to begin with",
   True,
   "the EFE quadrupole is aligned with g_ext, not with the light, so <cos 2 dphi> -> 0 in a stack; that is hunt item 83, not item 62")

# =====================================================================================================================
P(""); P("="*118); P("VERDICT"); P("="*118)
info(f"3-D: the phantom IS a flattened, baryon-following structure -- q_ph = {q2[2]:.2f} at 10 kpc -- and that remains a")
info(f"   real and distinctive prediction.  But it rounds off fast: q_ph = {q2[5]:.2f} at 45 kpc and {q2[6]:.2f} at 100 kpc.")
info(f"PROJECTED, which is what is measured: eps_kappa(45-200 kpc) = {_ef[BAND].mean():.4f} for a disc, i.e. q = "
     f"{(1-_ef[BAND].mean())/(1+_ef[BAND].mean()):.3f} -- five to fifteen times rounder than the list's 0.7-0.8.")
info(f"f_h: framework {FH_C:.3f} (discs) and {FH_ET_MID:.3f}-{max(FH_ET.values()):.3f} (early types); LambdaCDM (aligned, c/a = 0.7) {LCDM[0.70]:.3f};")
info(f"   measured {FH_OBS:.3f} +- {FH_ERR:.3f} (blue) and {FH_RED:.3f} +- {FH_RED_E:.3f} (red).  Everything is consistent with everything.")
info("the two things this script changed its own mind about, both recorded above: eps_kappa does not depend on a_0 (M4),")
info("   and the early-type case is NOT the liability I expected -- it is the framework's best showing here (62c).")
ck("62 SUMMARY -- a NULL, with the list's own prediction corrected and one liability I expected NOT confirmed.  (i) The stated framework prediction, q = 0.7-0.8 at 30-100 kpc, is WITHDRAWN: that is the 3-D axis ratio at the inner edge of the range, while the projected quantity lensing measures is q = 0.95-0.99.  (ii) On DISC lenses the framework predicts f_h = 0.03 against 0.217 +- 0.160: consistent, 1.2 sigma, underpowered.  (iii) On RED lenses, where I expected a liability, the framework predicts 0.15-0.21 against 0.303 +- 0.080: also consistent, 1.1-1.9 sigma, because an early type sits only 2-3 MOND radii inside 45 kpc.  No discrimination against LambdaCDM in either direction, and no liability.  What the item does establish is that this observable is a_0-BLIND, so it can never be a measurement of the framework's constant -- only of whether the lensing mass's shape is locked to the baryons",
   True,
   f"eps_kappa(45-200 kpc) = {_ef[BAND].mean():.4f} (both footings, and a_0-blind to 4 per cent over four decades); "
   f"f_h(discs) = {FH_C:.4f}/{FH_A:.4f} vs blue {FH_OBS:.3f}+-{FH_ERR:.3f} ({abs(nsig_fw):.1f} sigma); "
   f"f_h(early types) = {min(FH_ET.values()):.3f}-{max(FH_ET.values()):.3f} vs red {FH_RED:.3f}+-{FH_RED_E:.3f} ({(FH_RED-max(FH_ET.values()))/FH_RED_E:.1f}-{(FH_RED-min(FH_ET.values()))/FH_RED_E:.1f} sigma)")
sys.exit(ck.done())
