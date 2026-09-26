#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L370 -- BOOSTED INFALL IN CLUSTER MERGERS: in the construction a cluster's baryons fall into a neighbour with the MOND
boost of their shared bound region, while its dark carrier falls in on plain Newtonian gravity.  Two merger tests:
(A) El Gordo's collision speed on Asencio, Banik & Kroupa's own yardstick; (B) the star-dark offsets of Harvey et al.'s
72 collisions.

WHY.  The idea under test: "boosted acceleration into the halo".  For baryons the construction already has it -- the MOND
kernel, switched on inside bound regions (L359) and reading only a region's own baryons (L361).  The carrier cannot have
it: whatever feels the boost must source it (reciprocity, L353 N2), and that universal coupling dies on X-COP
(L321/L345/L354 MUTATE).  So in a merger the two components fall differently.  This is the one place the construction's
split force law shows up in cluster DYNAMICS rather than statics.  MOND folklore says mergers favour modified gravity
(El Gordo and the Bullet collide fast; the record's FALSIFICATION_MATRIX row "El Gordo: natural (faster growth + boost)").
This lane computes what THIS construction actually does.

THE CONSTRUCTION'S MERGER PHYSICS (L353 + L359 + L361 + L357; nothing new is added):
  * a cluster = a real halo (carrier + gas + stars) plus the phantom of its region's baryons.  The region is the connected
    set where x~ = (3/2)(rho - rho_bar_m)/rho_crit(z) >= x_c0 E(z)^(2p) (L359 window cells) [CORRECTION 2026-09-26: the
    code masks on the ABSOLUTE density, (3/2) rho/rho_crit(z) >= x_c0 E(z)^(2p) (RealHalo.lensing and phantom_felt), and
    every result here and in its consumers (L371, L372, L373's Harvey stage) used that mask; L352, L377 and DE1 subtract
    the background, a shift of (3/2) Omega_m(z) in x~ (0.84 at z = 0.4) -- an operator difference, open item 1 of the
    2026-09-26 peer review].  The phantom field is
    P[f (nu(|g_w|/a0) - 1) g_w], with g_w the Newtonian field of the REGION's baryons (L361) and P the curl-free
    projection, so it is Gauss-cancelled at the region's edge;
  * baryons move in phi + f P; the carrier moves in phi (Newtonian from all matter).  Lensing = dynamics (L279), so weak
    lensing weighs real + phantom;
  * two clusters in separate regions attract as Newtonian REAL masses; once their regions merge, the combined baryons
    source one nonlinear phantom;
  * the carrier's core has decayed where the pre-decay density exceeds L357's vacuum-gated threshold (best strict cell
    p_v = 2, x_v0 = 2000, 'cleared'; variant 'cap', x_v0 = 1000; and an intact carrier).

METHOD.
 (A) El Gordo in Asencio+2023's convention (Kim+2021 lensing): M200 = 2.13e15 Msun, mass ratio 1.52, z = 0.87.
     * Each subcluster's real halo is solved so that real + phantom reproduces its lensing M200.  This is done in 1-D,
       which is exact in spherical symmetry; control C3 shows the grid reproduces it.
     * The pair force F(d) comes from a periodic-FFT QUMOND solve with region labelling (384^3 over 40 Mpc).  The
       Newtonian periodic images are removed with an Ewald point-mass correction, and the force is antisymmetrized.  The
       relative acceleration uses the REAL inertial masses.  LCDM: the same components (NFW dark matter + beta-model gas +
       stars) normalized to the lensing M200, all real and Newtonian -- with the kernel off the construction's intact variant
       is exactly this reference.
     * "The same collision" means the same relative speed at core contact, d_m = 0.5 Mpc (1 Mpc as a variant).
     * The speed the construction needs far out is mapped onto Asencio's statistic v~ = v(2R_T)/sqrt(G M/R_T), using
       its REAL virial masses and radii.  The mapping holds because the construction's z >~ 1 structure formation is
       LCDM's in real mass: the gated carrier is intact then (L357).
     * It is scored with Asencio+2023 Fig. 1 (chi against V_infall at M~ = 15.33, digitized) and with the mass
       dependence of Asencio+2021 Table A1 (the z = 1 quadratic; Models B and A as a bracket).
 (B) Harvey+2015 measured <delta_SI> = -5.8 +/- 8.2 kpc and <beta> = delta_SI/delta_SG = -0.04 +/- 0.07.
     * The configuration: a substructure (lensing M200 1e14 or 3e14) 400 kpc from a 1e15 main cluster at z = 0.4, its gas
       displaced by delta_SG = 60 or 120 kpc.
     * LCDM is the same substructure (NFW dark matter + stars + the displaced gas) with all mass real, normalized to the
       same lensing M200.
     * The lensing position (real + phantom) is measured three ways and compared with LCDM's: iterated centroids in
       apertures of 100 and 150 kpc (pre-declared), and the centre of a projected-NFW profile fitted to the convergence on
       the annulus 40-300 kpc -- the analogue of Harvey's Lenstool fits of NFW halos to the shear (added before the
       full-resolution run, after the coarse smoke test showed the apertures disagree).
     * The construction's EXCESS beta is the prediction, because Harvey's corrections null LCDM's own gas pull.  It is
       computed for an intact and for a core-decayed carrier.

CHECKS
  C1 the solver reproduces Milgrom's exact deep-MOND two-body force (2/3) sqrt(G a0) [(m1+m2)^1.5 - m1^1.5 - m2^1.5]/d
     within 5%, and conserves momentum within 5%.
  C2 the periodic-image correction (an Ewald sum): for two Gaussian blobs the corrected grid force equals their exact
     isolated mutual force within 1% at 4 and 8 Mpc.
  C3 the isolated construction cluster on the grid reproduces the 1-D lensing mass at R200 within 3%, and its phantom is
     Gauss-cancelled beyond the region's edge (|net phantom| < 2% of the baryons).
  A1 the phantom is part of what lensing weighs: El Gordo's REAL mass is < 0.9 of its lensing mass (both footings).
  A2 the split force law slows the infall: to collide as LCDM's pair does, the construction needs a larger v~ than LCDM
     at V_infall = 2500 km/s (every variant).
  A3 THE VERDICT on El Gordo, pre-declared as neutral: |chi_construction - chi_LCDM| < 0.5 at V_infall = 2500 km/s, all
     variants, both mass-slope models.  Neither the folklore win nor a new kill.
  B1 (control) LCDM's own gas pull on the lensing centroid in these configurations is a few kpc, the size of Harvey's
     correction (4.3 +/- 1.6 kpc).
  B2 intact carrier: the construction's excess beta lies within 2 sigma of Harvey's <beta> (-0.18 <= beta <= +0.10), all
     configurations.
  B3 core-decayed carrier (L357's cells): the same test.
  B4 (design pointer, reported) a carrier depleted UNIFORMLY to X-COP's 0.55: the same test.
  B5 with the Lenstool-like projected-NFW fit: the intact carrier within 2 sigma in every configuration.
  B6 with the Lenstool-like projected-NFW fit: the core-decayed carrier (L357's cells), the same test.
  B7 (reported) Harvey's number is a POPULATION mean: the configuration-averaged excess beta of each carrier, per estimator,
     in sigma from <beta> = -0.04 +/- 0.07 (the eight configurations are a crude stand-in for the 72 substructures).
MUTATE=1 switches the kernel off (nu = 1): the construction becomes LCDM with real = lensing mass.  A1 and A2 must fail
(rc = 1).

Run from the repository root:  python3 real_research/merger_infall_2026/L370_boosted_infall_mergers.py
"""
import os, sys, json, math, time, warnings
import numpy as np
import scipy.fft as sfft
from scipy import ndimage
from scipy.optimize import brentq
from scipy.interpolate import PchipInterpolator
from scipy.special import erfc, erfcinv
warnings.filterwarnings("ignore", category=RuntimeWarning)

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
FAST = os.environ.get("FAST", "0") == "1"                             # smoke test only (coarse grids); never committed
SLUG = "L370_boosted_infall_mergers" + ("_MUTATE" if MUTATE else "") + ("_FAST" if FAST else "")
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L370", "mutate": MUTATE, "checks": {}, "numbers": {}}
WK = 4                                                                # FFT threads (a parallel session shares the machine)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: kernel off (nu = 1) -- the construction reduces to LCDM with real = lensing mass; A1, A2 must FAIL ***")

# ------------------------------------------------------------------------------------------------ cosmology and units
h = 0.6736; omb, omc = 0.02237, 0.1200                                # L319's cosmology (Planck 2018)
Ob, Oc = omb / h ** 2, omc / h ** 2; Om = Ob + Oc; Orad = 4.18e-5 / h ** 2 * (1 + 0.2271 * 3.046); OL = 1 - Om - Orad
GK = 4.30091727e-6                                                    # kpc (km/s)^2 / Msun
GMPC = GK / 1e3                                                       # Mpc (km/s)^2 / Msun
KPC_M = 3.0856775814913673e19
RHOC0 = 277.5 * h ** 2                                                # Msun / kpc^3
Ez2 = lambda z: Om * (1 + z) ** 3 + OL
Om_z = lambda z: Om * (1 + z) ** 3 / Ez2(z)
OL_z = lambda z: OL / Ez2(z)
FOOT = {"canonical": 9.3619e-11, "alt": 1.1279e-10}                   # a0 [m/s^2], both footings always
A0K = {f: v * KPC_M / 1e6 for f, v in FOOT.items()}                   # (km/s)^2 / kpc


def c_dm14(Mh, z):                                                    # Dutton & Maccio 2014 (Planck), M in Msun/h (as L357)
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * np.log10(Mh / 1e12))


# ------------------------------------------------------------------------------------------------ the kernel (L340's, as L354)
def h_rar(y):
    y = np.asarray(y, float)
    return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)


Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P))
LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
DH = np.maximum(dh_rar(YG), 0.05 * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])


def nu_mono(y):                                                       # L340's monotone kernel
    if MUTATE:
        return np.ones_like(np.asarray(y, float))
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y


# ------------------------------------------------------------------------------------------------ the switch and the carrier gate
SWITCH = {"p1_x1.5": (1.0, 1.5), "p0.5_x2.5": (0.5, 2.5), "p2_x2.0": (2.0, 2.0)}     # L359 window cells (p, x_c0)
SW_DEF = "p1_x1.5"                                                    # L360's assembled construction
# ^ L370's OWN cell.  A consumer must pass its construction's cell explicitly and never inherit this default: L381 and
#   L373's first run inherited it against a p = 2, x_c0 = 2 mesh (2026-09-26).  Kept so committed consumers reproduce.
x_ceff = lambda z, sw: SWITCH[sw][1] * Ez2(z) ** SWITCH[sw][0]
GATE = {"cleared_2000": ("cleared", 2000.0), "cap_1000": ("cap", 1000.0), "intact": ("intact", None),
        "uniform_0.55": ("uniform", 0.55)}                            # L357 strict cells (p_v = 2); intact; X-COP's eps, uniform


def rho_thr(z, x_v0, p_v=2.0):                                       # L357: total-density threshold of the vacuum-gated decay
    x_eff = x_v0 * (OL / OL_z(z)) ** p_v
    return (Om_z(z) + 2.0 / 3.0 * x_eff) * RHOC0 * Ez2(z)


# ------------------------------------------------------------------------------------------------ 1-D spherical halos
RG = np.geomspace(0.05, 6e4, 9000)                                   # kpc


def cum_mass(rho):
    integ = 4 * math.pi * RG ** 2 * rho
    seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(RG)
    return np.concatenate([[integ[0] * RG[0] / 3.0], integ[0] * RG[0] / 3.0 + np.cumsum(seg)])


def taper(r, rt): return (rt ** 2 / (r ** 2 + rt ** 2)) ** 2             # Baltz-Marshall-Oguri n = 2 truncation
def s_nfw(r, rs): x = r / rs; return 1.0 / (x * (1 + x) ** 2)
def s_beta(r, rc): return 1.0 / (1 + (r / rc) ** 2)                    # beta = 2/3
def s_hern(r, a): x = r / a; return 1.0 / (x * (1 + x) ** 3)


def m_in(rho, R): return float(np.interp(R, RG, cum_mass(rho)))


class RealHalo:
    """The construction's real halo: carrier NFW + gas beta-model + stars (30% BCG Hernquist, 70% NFW-traced), normalized
    within the pre-decay R200; the carrier decayed where the pre-decay density exceeds the vacuum-gated threshold."""

    def __init__(self, M200, z, fgas, fstar, gate, c=None, rt_fac=2.5, rc_fac=0.12):
        self.M200, self.z = M200, z
        self.rhoc = RHOC0 * Ez2(z)
        self.R200 = (3 * M200 / (4 * math.pi * 200 * self.rhoc)) ** (1 / 3)
        self.c = float(c if c is not None else c_dm14(M200 * h, z))
        rs, rt = self.R200 / self.c, rt_fac * self.R200
        T = taper(RG, rt)
        nfw, gas, bcg = s_nfw(RG, rs) * T, s_beta(RG, rc_fac * self.R200) * T, s_hern(RG, 30.0) * T
        R = self.R200
        rho_c0 = (1 - fgas - fstar) * M200 * nfw / m_in(nfw, R)
        self.rho_g = fgas * M200 * gas / m_in(gas, R)
        self.rho_s = fstar * M200 * (0.3 * bcg / m_in(bcg, R) + 0.7 * nfw / m_in(nfw, R))
        pic, xv0 = GATE[gate]
        rho_pre = rho_c0 + self.rho_g + self.rho_s
        if pic == "cleared":
            self.rho_c = np.where(rho_pre >= rho_thr(z, xv0), 0.0, rho_c0)
        elif pic == "uniform":
            self.rho_c = xv0 * rho_c0
        elif pic == "cap":
            self.rho_c = np.where(rho_pre >= rho_thr(z, xv0), np.maximum(rho_thr(z, xv0) - self.rho_g - self.rho_s, 0.0), rho_c0)
        else:
            self.rho_c = rho_c0
        self.rho_b = self.rho_g + self.rho_s
        self.rho = self.rho_b + self.rho_c

    def lensing(self, a0, sw, kernel=True):
        """1-D (exact spherical) lensing profile: M_L(<r) = M_real(<r) + f (nu - 1) M_b(<r), region connected to the centre.
        kernel=False gives the LCDM reference (the same components, all real, Newtonian)."""
        Mb, Mr = cum_mass(self.rho_b), cum_mass(self.rho)
        gNb = GK * Mb / RG ** 2
        inside = (1.5 * self.rho / self.rhoc) >= x_ceff(self.z, sw)
        f = np.cumprod(inside).astype(float)                          # the region connected to the centre
        Mph = f * (nu_mono(gNb / a0) - 1.0) * Mb if kernel else 0.0 * Mb
        ML = Mr + Mph
        diff = ML - 200 * self.rhoc * 4 / 3 * math.pi * RG ** 3
        i = int(np.argmax((diff[:-1] > 0) & (diff[1:] <= 0)))
        R200L = RG[i] - diff[i] * (RG[i + 1] - RG[i]) / (diff[i + 1] - diff[i])
        edge = float(RG[int(np.argmin(f))]) if f.min() == 0 else float(RG[-1])
        return dict(M200L=float(np.interp(R200L, RG, ML)), R200L=float(R200L), edge=edge,
                    Mreal_R200L=float(np.interp(R200L, RG, Mr)), Mph_R200L=float(np.interp(R200L, RG, Mph)),
                    Mb_R200L=float(np.interp(R200L, RG, Mb)))


def solve_real(M200L, z, a0, sw, gate, fgas=0.125, fstar=0.015, c_fixed=None, kernel=True):
    """the real halo whose real + phantom has lensing M200 = M200L (kernel=False: the LCDM reference, same components)."""
    fn = lambda M: RealHalo(M, z, fgas, fstar, gate, c=c_fixed).lensing(a0, sw, kernel)["M200L"] - M200L
    M = brentq(fn, 0.2 * M200L, 3.0 * M200L, rtol=1e-6)
    H = RealHalo(M, z, fgas, fstar, gate, c=c_fixed)
    return H, H.lensing(a0, sw, kernel)


# ------------------------------------------------------------------------------------------------ the periodic grid
class Grid:
    def __init__(self, N, L):
        self.N, self.L, self.dx = N, L, L / N
        self.x = (np.arange(N) + 0.5) * self.dx - L / 2
        k = 2 * np.pi * sfft.fftfreq(N, d=self.dx); kz = 2 * np.pi * sfft.rfftfreq(N, d=self.dx)
        self.kx, self.ky, self.kz = k[:, None, None], k[None, :, None], kz[None, None, :]
        self.k2 = self.kx ** 2 + self.ky ** 2 + self.kz ** 2; self.k2[0, 0, 0] = 1.0
        self.dV = self.dx ** 3

    def field(self, rho):
        rk = sfft.rfftn(rho, workers=WK); phik = -4 * np.pi * GK * rk / self.k2; phik[0, 0, 0] = 0.0
        return [sfft.irfftn(-1j * kk * phik, s=rho.shape, workers=WK) for kk in (self.kx, self.ky, self.kz)]

    def project(self, F):
        Fk = [sfft.rfftn(f, workers=WK) for f in F]
        dot = (self.kx * Fk[0] + self.ky * Fk[1] + self.kz * Fk[2]) / self.k2; dot[0, 0, 0] = 0.0
        return [sfft.irfftn(kk * dot, s=F[0].shape, workers=WK) for kk in (self.kx, self.ky, self.kz)]

    def divergence(self, F):
        Fk = [sfft.rfftn(f, workers=WK) for f in F]
        return sfft.irfftn(1j * (self.kx * Fk[0] + self.ky * Fk[1] + self.kz * Fk[2]), s=F[0].shape, workers=WK)

    def paint(self, rho1d, centre=(0.0, 0.0, 0.0), sub=2, norm_mass=None):
        """cell-averaged density of a 1-D radial profile (sub-sampled); renormalized to the 1-D mass inside L/2."""
        N, dx = self.N, self.dx
        out = np.zeros((N, N, N))
        offs = (np.arange(sub) + 0.5) / sub - 0.5
        X = self.x[:, None, None]; Y = self.x[None, :, None]; Z = self.x[None, None, :]
        lr, lrho = np.log(RG), np.log(np.maximum(rho1d, 1e-300))
        for ox in offs:
            for oy in offs:
                for oz in offs:
                    r = np.sqrt((X + ox * dx - centre[0]) ** 2 + (Y + oy * dx - centre[1]) ** 2 + (Z + oz * dx - centre[2]) ** 2)
                    out += np.exp(np.interp(np.log(np.maximum(r, RG[0])), lr, lrho))
        out /= sub ** 3
        target = norm_mass if norm_mass is not None else float(np.interp(self.L / 2, RG, cum_mass(rho1d)))
        tot = out.sum() * self.dV
        return out * (target / tot) if tot > 0 else out


def phantom_felt(grid, rb, rreal, z, a0, sw, centres, want_rho=True):
    """L361: label the bound regions; each region's phantom from its OWN baryons; baryons feel their region's phantom.
    Returns the phantom field felt by baryons (3 arrays), the region labels at the given centre cells, and the phantom
    density (for lensing)."""
    mask = (1.5 * rreal / (RHOC0 * Ez2(z))) >= x_ceff(z, sw)
    lab, nlab = ndimage.label(mask)
    labs = sorted({int(lab[c]) for c in centres if lab[c] > 0})
    gfelt = [np.zeros_like(rb) for _ in range(3)]; rho_ph = np.zeros_like(rb)
    for L_ in labs:
        f = (lab == L_)
        gw = grid.field(rb * f)
        mag = np.sqrt(gw[0] ** 2 + gw[1] ** 2 + gw[2] ** 2)
        fac = f * (nu_mono(mag / a0) - 1.0)
        F = [fac * g_ for g_ in gw]
        del gw, mag
        gph = grid.project(F)
        for i in range(3):
            gfelt[i] += f * gph[i]
        if want_rho:
            rho_ph += -grid.divergence(gph) / (4 * math.pi * GK)
        del F, gph, f
    return gfelt, [int(lab[c]) for c in centres], rho_ph, nlab


# ============================================================================================================ C1
banner("C1  THE SOLVER against Milgrom's exact deep-MOND two-body force (a pure 1/sqrt(y) kernel inside a 4 Mpc region)")
G1 = Grid(160 if FAST else 256, 9000.0)
m1c, m2c, dc, bc, A0DM = 1e12, 0.5e12, 400.0, 40.0, 1e5
plum = lambda M, b: 3 * M / (4 * math.pi * b ** 3) * (1 + (RG / b) ** 2) ** -2.5
x1c, x2c = -dc * m2c / (m1c + m2c), dc * m1c / (m1c + m2c)
r1 = G1.paint(plum(m1c, bc), (x1c, 0, 0), norm_mass=m1c); r2 = G1.paint(plum(m2c, bc), (x2c, 0, 0), norm_mass=m2c)
gN = G1.field(r1 + r2)
reg = (G1.x[:, None, None] ** 2 + G1.x[None, :, None] ** 2 + G1.x[None, None, :] ** 2) <= 4000.0 ** 2
mag = np.sqrt(gN[0] ** 2 + gN[1] ** 2 + gN[2] ** 2)
fac = reg * (np.maximum(mag / A0DM, 1e-30) ** -0.5 - 1.0)
gph = G1.project([fac * g_ for g_ in gN])
F2 = float(((gN[0] + gph[0]) * r2).sum() * G1.dV); F1 = float(((gN[0] + gph[0]) * r1).sum() * G1.dV)
FM = (2 / 3) * math.sqrt(GK * A0DM) * ((m1c + m2c) ** 1.5 - m1c ** 1.5 - m2c ** 1.5) / dc
asym = abs(F1 + F2) / abs(F2)
P(f"    F on body 2 {F2:.4e}, on body 1 {F1:.4e}; Milgrom {FM:.4e}; ratio {abs(F2 - F1) / 2 / FM:.4f}; momentum defect {asym:.4f}")
OUT["numbers"]["C1"] = dict(ratio=abs(F2 - F1) / 2 / FM, momentum_defect=asym)
check("C1 the periodic-FFT QUMOND solver with a region mask reproduces Milgrom's exact deep-MOND two-body force within 5% "
      "and conserves momentum within 5%", f"ratio {abs(F2 - F1) / 2 / FM:.4f}, momentum defect {asym:.4f}",
      (abs(abs(F2 - F1) / 2 / FM - 1) < 0.05 or MUTATE) and asym < 0.05,
      "the nonlinear two-body MOND force (the 'two-body deficit' of deep MOND) is what the merged-region phantom must carry")
del G1, r1, r2, gN, reg, mag, fac, gph

# ============================================================================================================ (A) El Gordo
banner("A  EL GORDO (Kim+2021 lensing; Asencio+2023 convention): the real halos behind the lensing masses")
ZEG = 0.87
MTOT_A, RATIO_A, RT_A = 2.13e15, 1.52, 3030.0                       # Asencio+2023: M200, ratio, R_T (2R_T = 6.06 Mpc)
ML1, ML2 = MTOT_A * RATIO_A / (1 + RATIO_A), MTOT_A / (1 + RATIO_A)
VESC_A = math.sqrt(GMPC * MTOT_A / (RT_A / 1e3))                      # sqrt(G M / R_T), Asencio+2021 eq. 11
FIG1_V = np.array([1000.0, 1500.0, 2000.0, 2500.0, 3000.0])          # Asencio+2023 Fig. 1, solid red (El Gordo, survey region)
FIG1_CHI = np.array([3.03, 4.12, 4.70, 5.10, 5.38])                  # digitized from the rendered figure (+/- 0.05)
TA1 = {"B": (-786.14, 114.75, -4.16), "A": (-347.02, 54.41, -2.10)}   # Asencio+2021 Table A1/A2, z = 1 column
log10P_of_chi = lambda chi: math.log10(erfc(chi / math.sqrt(2)))
chi_of_log10P = lambda lp: math.sqrt(2) * erfcinv(10 ** lp) if lp > -300 else 40.0
LP_FIG = np.array([log10P_of_chi(c_) for c_ in FIG1_CHI]); VT_FIG = FIG1_V / VESC_A


def log10P_vt(vt):
    """Asencio's log10 P against v~ at M~ = 15.33; linear beyond the plotted range (flagged)."""
    if vt <= VT_FIG[-1]:
        return float(np.interp(vt, VT_FIG, LP_FIG))
    s = (LP_FIG[-1] - LP_FIG[-2]) / (VT_FIG[-1] - VT_FIG[-2])
    return float(LP_FIG[-1] + s * (vt - VT_FIG[-1]))


def log10P_vt_steep(vt):
    """the same, but beyond the plotted range continued as a Gaussian tail log10 P = A - B v~^2 through the last two points."""
    if vt <= VT_FIG[-1]:
        return float(np.interp(vt, VT_FIG, LP_FIG))
    B = (LP_FIG[-2] - LP_FIG[-1]) / (VT_FIG[-1] ** 2 - VT_FIG[-2] ** 2); A = LP_FIG[-1] + B * VT_FIG[-1] ** 2
    return float(A - B * vt ** 2)


Q = lambda Mt, m: TA1[m][0] + TA1[m][1] * Mt + TA1[m][2] * Mt ** 2
P(f"    Asencio yardstick: M = {MTOT_A:.3g} (M~ {math.log10(MTOT_A):.3f}), ratio {RATIO_A}, 2R_T = {2 * RT_A / 1e3:.2f} Mpc, "
  f"sqrt(GM/R_T) = {VESC_A:.0f} km/s; Fig. 1: " + ", ".join(f"{v:.0f}->{c:.2f}" for v, c in zip(FIG1_V, FIG1_CHI)))

EG = {}
for foot in FOOT:
    for sw in SWITCH:
        for gate in (("cleared_2000", "intact") if sw == SW_DEF else ("cleared_2000",)):
            key = (foot, sw, gate)
            H1, L1 = solve_real(ML1, ZEG, A0K[foot], sw, gate); H2, L2 = solve_real(ML2, ZEG, A0K[foot], sw, gate)
            EG[key] = dict(H=(H1, H2), L=(L1, L2))
            P(f"    {foot:9s} {sw:10s} {gate:12s}: real M200 {H1.M200:.3e} / {H2.M200:.3e} (real/lensing {H1.M200 / ML1:.3f} / "
              f"{H2.M200 / ML2:.3f}); at R200_L the phantom is {L1['Mph_R200L'] / L1['M200L']:.2f} / {L2['Mph_R200L'] / L2['M200L']:.2f} "
              f"of lensing; region edge {L1['edge'] / 1e3:.2f} / {L2['edge'] / 1e3:.2f} Mpc (R200_L {L1['R200L'] / 1e3:.2f} / "
              f"{L2['R200L'] / 1e3:.2f})")
frac_real = {k: (v["H"][0].M200 + v["H"][1].M200) / MTOT_A for k, v in EG.items()}
OUT["numbers"]["A_real_fraction"] = {"|".join(k): v for k, v in frac_real.items()}
check("A1 the phantom is part of what lensing weighs: El Gordo's REAL mass (baryons + carrier within the real R200s) is "
      "< 0.9 of its lensing mass on both footings", ", ".join(f"{'/'.join(k)} {v:.3f}" for k, v in frac_real.items()),
      all(v < 0.9 for v in frac_real.values()),
      "at z = 0.87 the baryons at R200 sit near 0.1 a0, so their phantom adds ~30-40% to what the shear measures")

# ---------------------------------------------------------------------------------------------------- the pair force
banner("A  THE PAIR FORCE F(d): QUMOND with region labelling (construction) against Newtonian lensing halos (LCDM)")
NG, LG = (160, 40000.0) if FAST else (384, 40000.0)
GR = Grid(NG, LG)
DX = GR.dx
D_LIST = np.array([0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 8.0]) * 1e3
D_CELLS = np.unique(np.round(D_LIST / DX).astype(int))
C0 = NG // 2                                                          # paintings are centred on the corner at index C0 - 1/2


def centre_cell(shift):                                               # the cell next to a painting's centre after a roll
    return (C0 + shift, C0, C0)


def ewald_gx(d, L, alpha=None, nr=3, nk=8):
    """x-acceleration on a unit mass at (d, 0, 0) from a unit mass at the origin, all periodic images and the
    neutralizing background of a cubic box of side L (Ewald sum; kpc, (km/s)^2/kpc)."""
    a = alpha if alpha is not None else 2.5 / L
    n = np.arange(-nr, nr + 1)
    NX, NY, NZ = np.meshgrid(n, n, n, indexing="ij")
    rx, ry, rz = d + NX * L, NY * L, NZ * L
    r = np.sqrt(rx ** 2 + ry ** 2 + rz ** 2)
    real = np.sum(rx / r ** 3 * (erfc(a * r) + 2 * a * r / math.sqrt(math.pi) * np.exp(-(a * r) ** 2)))
    m = np.arange(-nk, nk + 1)
    MX, MY, MZ = np.meshgrid(m, m, m, indexing="ij")
    kx, ky, kz = 2 * math.pi * MX / L, 2 * math.pi * MY / L, 2 * math.pi * MZ / L
    k2 = kx ** 2 + ky ** 2 + kz ** 2
    ok = k2 > 0
    recip = 4 * math.pi / L ** 3 * np.sum((kx[ok] / k2[ok]) * np.exp(-k2[ok] / (4 * a * a)) * np.sin(kx[ok] * d))
    return -GK * (real + recip)


def ewald_corr(n1, n2):
    """per unit (m1 m2): the isolated point-mass attraction G/d^2 minus the periodic one (images + background)."""
    d = (n1 + n2) * DX
    return GK / d ** 2 - (-ewald_gx(d, LG))


EWALD = {}
for n in D_CELLS:
    n1 = int(round(n * ML2 / (ML1 + ML2))); n2 = int(n - n1)
    EWALD[int(n)] = (n1, n2, ewald_corr(n1, n2))
P(f"    image correction (fraction of G/d^2): " + ", ".join(f"{n * DX / 1e3:.2f} Mpc {EWALD[int(n)][2] / (GK / (n * DX) ** 2):+.3f}" for n in D_CELLS))

# LCDM reference: the SAME components (NFW dark matter + beta-model gas + stars), all real and Newtonian, normalized to
# the lensing M200 -- so that with the kernel off (MUTATE) the construction's intact variant IS this reference
HL1, _ = solve_real(ML1, ZEG, A0K["canonical"], SW_DEF, "intact", kernel=False)
HL2, _ = solve_real(ML2, ZEG, A0K["canonical"], SW_DEF, "intact", kernel=False)
pL1, pL2 = GR.paint(HL1.rho), GR.paint(HL2.rho)
mL1, mL2 = pL1.sum() * GR.dV, pL2.sum() * GR.dV
AREL_L = {}
for n in D_CELLS:
    n1, n2, corr = EWALD[int(n)]
    a1, a2 = np.roll(pL1, -n1, axis=0), np.roll(pL2, n2, axis=0)
    g = GR.field(a1 + a2)
    F1x = float((g[0] * a1).sum() * GR.dV); F2x = float((g[0] * a2).sum() * GR.dV)
    Fatt = (F1x - F2x) / 2 + mL1 * mL2 * corr
    AREL_L[int(n)] = Fatt * (1 / mL1 + 1 / mL2)
del pL1, pL2
P(f"    LCDM (same components, all real; masses in box {mL1:.3e} / {mL2:.3e}): a_rel [(km/s)^2/kpc] " +
  ", ".join(f"{n * DX / 1e3:.2f}:{AREL_L[int(n)]:.1f}" for n in D_CELLS) + f"   [{time.time() - T0:.0f}s]")

AREL_C, AREL_CN, MERGE, MASS_C, ASYM = {}, {}, {}, {}, {}
_pc = {"key": None}
for key, v in sorted(EG.items(), key=lambda kv: (kv[0][0], kv[0][2], kv[0][1])):
    foot, sw, gate = key
    H1, H2 = v["H"]
    pk = (round(H1.M200 / 1e10), round(H2.M200 / 1e10), gate)
    if _pc["key"] != pk:
        _pc.clear(); _pc["key"] = pk
        _pc["arr"] = (GR.paint(H1.rho_b), GR.paint(H1.rho_c), GR.paint(H2.rho_b), GR.paint(H2.rho_c))
    b1, c1, b2, c2 = _pc["arr"]
    m1 = (b1.sum() + c1.sum()) * GR.dV; m2 = (b2.sum() + c2.sum()) * GR.dV
    MASS_C[key] = (m1, m2)
    ar, arn, mg, asy = {}, {}, {}, {}
    for n in D_CELLS:
        n1, n2, corr = EWALD[int(n)]
        B1, Cc1, B2, Cc2 = (np.roll(b1, -n1, axis=0), np.roll(c1, -n1, axis=0), np.roll(b2, n2, axis=0), np.roll(c2, n2, axis=0))
        rb = B1 + B2; rreal = rb + Cc1 + Cc2
        gN = GR.field(rreal)
        gfelt, labs, _, nlab = phantom_felt(GR, rb, rreal, ZEG, A0K[foot], sw, [centre_cell(-n1), centre_cell(n2)], want_rho=False)
        FN1 = float((gN[0] * (B1 + Cc1)).sum() * GR.dV); FN2 = float((gN[0] * (B2 + Cc2)).sum() * GR.dV)
        FP1 = float((gfelt[0] * B1).sum() * GR.dV); FP2 = float((gfelt[0] * B2).sum() * GR.dV)
        FattN = (FN1 - FN2) / 2 + m1 * m2 * corr
        Fatt = FattN + (FP1 - FP2) / 2
        ar[int(n)] = Fatt * (1 / m1 + 1 / m2); arn[int(n)] = FattN * (1 / m1 + 1 / m2)
        mg[int(n)] = (labs[0] == labs[1] and labs[0] > 0)
        asy[int(n)] = abs(FP1 + FP2) / max(abs(FP1 - FP2) / 2, 1e-30) if mg[int(n)] else 0.0
        del gN, gfelt, rb, rreal, B1, B2, Cc1, Cc2
    AREL_C[key], AREL_CN[key], MERGE[key], ASYM[key] = ar, arn, mg, asy
    P(f"    {foot:9s} {sw:10s} {gate:12s} (real masses in box {m1:.3e} / {m2:.3e}): a_rel/a_LCDM " +
      ", ".join(f"{n * DX / 1e3:.2f}:{ar[int(n)] / AREL_L[int(n)]:.3f}{'*' if mg[int(n)] else ''}" for n in D_CELLS) +
      f"   (* = regions merged; phantom-force momentum defect max {max(asy.values()):.3f})   [{time.time() - T0:.0f}s]")

_pc.clear()
# C2: the image correction itself, on a compact pair (the extended profiles overlap even at 8 Mpc, so they cannot test it)
sgP = 1.5 * DX                                                        # two Gaussian blobs: their mutual force is exact
gau = np.exp(-RG ** 2 / (2 * sgP ** 2)) / ((2 * math.pi) ** 1.5 * sgP ** 3)
p0 = GR.paint(gau, norm_mass=1.0)
F_gauss = lambda d: GK * (math.erf(d / (2 * sgP)) / d ** 2 - math.exp(-d ** 2 / (4 * sgP ** 2)) / (sgP * math.sqrt(math.pi) * d))
c2_rows = []
for dd in (4000.0, 8000.0):
    n = int(round(dd / DX)); n1 = n // 2; n2 = n - n1
    rho1, rho2 = np.roll(p0, -n1, axis=0), np.roll(p0, n2, axis=0)
    gP = GR.field(rho1)
    Fp = -float((gP[0] * rho2).sum() * GR.dV) + ewald_corr(n1, n2)
    c2_rows.append((n * DX, Fp / F_gauss(n * DX)))
    del rho1, rho2, gP
del p0
check("C2 the periodic-image correction: for two Gaussian blobs the corrected grid force equals their exact isolated mutual "
      "force within 1% at 4 and 8 Mpc", ", ".join(f"{d_ / 1e3:.1f} Mpc {r:.4f}" for d_, r in c2_rows),
      all(abs(r - 1) < 0.01 for _, r in c2_rows))
nfar = int(D_CELLS[-1]); dfar = nfar * DX
P(f"    (reported) extended profiles at {dfar / 1e3:.1f} Mpc against point masses of their box masses: LCDM "
  f"{AREL_L[nfar] / (GK * (mL1 + mL2) / dfar ** 2):.3f}; construction " + ", ".join(
    f"{'/'.join(k)} {AREL_C[k][nfar] / (GK * sum(MASS_C[k]) / dfar ** 2):.3f}" for k in EG) + "  (overlap of the outskirts)")

# C3: the isolated cluster on the grid reproduces the 1-D lensing mass, and Gauss cancellation
key0 = ("canonical", SW_DEF, "cleared_2000"); H1 = EG[key0]["H"][0]; L1 = EG[key0]["L"][0]
b1, c1 = GR.paint(H1.rho_b), GR.paint(H1.rho_c)
_, _, rph, _ = phantom_felt(GR, b1, b1 + c1, ZEG, A0K["canonical"], SW_DEF, [centre_cell(0)])
X2 = (GR.x[:, None, None] + DX / 2) ** 2 + (GR.x[None, :, None] + DX / 2) ** 2 + (GR.x[None, None, :] + DX / 2) ** 2
rr = np.sqrt(X2)
Mgrid = float(((b1 + c1 + rph) * (rr <= L1["R200L"])).sum() * GR.dV)
Mb_tot = float(b1.sum() * GR.dV); ph_out = float((rph * (rr <= L1["edge"] + 4 * DX)).sum() * GR.dV)
c3a = Mgrid / L1["M200L"] - 1; c3b = ph_out / Mb_tot
P(f"    isolated main subcluster (canonical, {SW_DEF}): grid lensing M(<R200_L) {Mgrid:.4e} vs 1-D {L1['M200L']:.4e} "
  f"({c3a:+.3f}); net phantom inside edge + 4 cells {ph_out:.3e} = {c3b:+.4f} of the baryons")
del b1, c1, rph, X2, rr
check("C3 the isolated construction cluster on the grid reproduces the 1-D lensing mass at R200 within 3%, and its phantom "
      "is Gauss-cancelled at the region's edge (|net phantom| < 2% of its baryons)", f"{c3a:+.3f}; {c3b:+.4f}",
      abs(c3a) < 0.03 and abs(c3b) < 0.02)

# ---------------------------------------------------------------------------------------------------- energy -> Asencio's statistic
banner("A  THE SAME COLLISION: the infall speed the construction needs far out, on Asencio's v~ statistic")


def a_of_d(tab, mtot_far, dcells):
    """relative acceleration as a function of d [kpc]: PCHIP in log-log on the grid, Newtonian point mass beyond."""
    ds = np.array([n * DX for n in dcells]); av = np.array([tab[int(n)] for n in dcells])
    f = PchipInterpolator(np.log(ds), np.log(av))
    return lambda d: np.where(d <= ds[-1], np.exp(f(np.log(np.clip(d, ds[0], ds[-1])))), GK * mtot_far / np.maximum(d, 1) ** 2)


def work(afun, da, db, n=4000):
    s = np.geomspace(da, db, n); a = afun(s)
    return float(np.sum(0.5 * (a[1:] + a[:-1]) * np.diff(s)))


V_A = [1000.0, 1500.0, 2000.0, 2300.0, 2500.0, 3000.0]
DM = {"d_m 0.5 Mpc": 500.0, "d_m 1 Mpc": 1000.0}
aL = a_of_d(AREL_L, mL1 + mL2, D_CELLS)
ROWS = []
for key in EG:
    H1, H2 = EG[key]["H"]
    m1, m2 = MASS_C[key]
    aC = a_of_d(AREL_C[key], m1 + m2, D_CELLS)
    RT_c = H1.R200 + H2.R200; M_c = H1.M200 + H2.M200
    vesc_c = math.sqrt(GK * M_c / RT_c)
    merged = [n * DX for n in D_CELLS if MERGE[key][int(n)]]
    d_merge = max(merged) if merged else 0.0
    d_s = max(2 * RT_c, d_merge + 1000.0)                             # a separation where the dynamics is Newtonian-real
    for dmk, dm in DM.items():
        for VA in V_A:
            Vm2 = VA ** 2 + 2 * work(aL, dm, 2 * RT_A)
            Vs2 = Vm2 - 2 * work(aC, dm, d_s)
            Veq2 = Vs2 + 2 * GK * M_c * (1 / (2 * RT_c) - 1 / d_s)     # Asencio's point-mass extrapolation to 2 R_T
            vt_c = math.sqrt(max(Veq2, 0.0)) / vesc_c
            vt_L = VA / VESC_A
            Mt_c = math.log10(M_c)
            rows = dict(key="/".join(key), dm=dmk, VA=VA, vt_L=vt_L, vt_c=vt_c, Mt_c=Mt_c, d_merge=d_merge,
                        chi_L=chi_of_log10P(log10P_vt(vt_L)))
            for m in TA1:
                lp = log10P_vt(vt_c) + (Q(Mt_c, m) - Q(math.log10(MTOT_A), m))
                rows[f"chi_c_{m}"] = chi_of_log10P(min(lp, 0.0))
                lps = log10P_vt_steep(vt_c) + (Q(Mt_c, m) - Q(math.log10(MTOT_A), m))
                rows[f"chi_c_{m}_steep"] = chi_of_log10P(min(lps, 0.0))
            rows["extrap"] = vt_c > VT_FIG[-1]
            ROWS.append(rows)
OUT["numbers"]["A_rows"] = ROWS
for r in ROWS:
    if r["VA"] in (1500.0, 2500.0) or (r["VA"] == 2300.0 and r["dm"] == "d_m 0.5 Mpc"):
        P(f"    {r['key']:34s} {r['dm']:11s} V_infall(LCDM) {r['VA']:.0f}: v~ LCDM {r['vt_L']:.3f} -> construction {r['vt_c']:.3f} "
          f"(M~ {r['Mt_c']:.3f}, regions merge at {r['d_merge'] / 1e3:.1f} Mpc){' [extrapolated]' if r['extrap'] else ''}; "
          f"chi LCDM {r['chi_L']:.2f} -> construction {r['chi_c_B']:.2f} (mass slope B) / {r['chi_c_A']:.2f} (A); "
          f"Gaussian tail {r['chi_c_B_steep']:.2f} / {r['chi_c_A_steep']:.2f}")
r2500 = [r for r in ROWS if r["VA"] == 2500.0]
check("A2 the split force law slows the infall: to collide as LCDM's pair does, the construction needs a larger v~ than LCDM "
      "at V_infall = 2500 km/s (every variant, both matching radii)",
      f"v~ LCDM {r2500[0]['vt_L']:.3f}; construction {min(r['vt_c'] for r in r2500):.3f}-{max(r['vt_c'] for r in r2500):.3f}",
      all(r["vt_c"] > r["vt_L"] * 1.02 for r in r2500),
      "the carrier -- most of the inertia -- feels only the real mass's Newtonian pull, and until the regions merge so does "
      "everything else")
dchi = [(r[f"chi_c_{m}"] - r["chi_L"]) for r in r2500 for m in TA1]
OUT["numbers"]["A3_dchi_2500"] = dict(min=min(dchi), max=max(dchi))
check("A3 THE VERDICT on El Gordo (pre-declared neutral): |chi_construction - chi_LCDM| < 0.5 at V_infall = 2500 km/s, "
      "every variant, both mass-slope models", f"Delta chi from {min(dchi):+.2f} to {max(dchi):+.2f}",
      max(abs(x) for x in dchi) < 0.5,
      "the phantom lowers El Gordo's real mass (fewer-sigma rarity) and the unboosted carrier raises the infall speed it "
      "needs (more-sigma); the pre-declared expectation was that the two nearly cancel")
dchi_s = [(r[f"chi_c_{m}_steep"] - r["chi_L"]) for r in r2500 for m in TA1]
OUT["numbers"]["A4_dchi_2500_steep"] = dict(min=min(dchi_s), max=max(dchi_s))
vt_max_jub = 1.69                                                     # Asencio+2021 Fig. 9: the largest v~ among the 1000 most massive pairs
check("A4 (reported) the same verdict with the v~ tail continued as a Gaussian (Asencio's Fig. 1 beyond 3000 km/s), and "
      "the construction's v~ against the largest v~ among Jubilee's 1000 most massive pairs (~1.69, Asencio+2021 Fig. 9)",
      f"Delta chi (Gaussian tail) {min(dchi_s):+.2f} to {max(dchi_s):+.2f}; construction v~ at 2500 km/s "
      f"{min(r['vt_c'] for r in r2500):.2f}-{max(r['vt_c'] for r in r2500):.2f} vs Jubilee's extreme ~{vt_max_jub}",
      True, "beyond v~ ~ 1.7 no LCDM-like pair exists to calibrate the tail: the verdict there is an extrapolation either way",
      load_bearing=False)

# ============================================================================================================ (B) Harvey
banner("B  HARVEY+2015: where the lensing peak sits when a substructure's gas is displaced (z = 0.4)")
ZH = 0.4
NH, LH = (160, 10000.0) if FAST else (400, 10000.0)
GH = Grid(NH, LH); DXH = GH.dx
XSUB = 400.0
HARV_BETA, HARV_ERR = -0.04, 0.07


def centroid(S, x0, y0, Rap, it=12):
    X = GH.x[:, None] + DXH / 2; Y = GH.x[None, :] + DXH / 2
    for _ in range(it):
        w = S * (((X - x0) ** 2 + (Y - y0) ** 2) <= Rap ** 2)
        x0, y0 = float((w * X).sum() / w.sum()), float((w * Y).sum() / w.sum())
    return x0, y0


def sig_nfw_shape(Xr):
    Xr = np.maximum(np.asarray(Xr, float), 1e-4); out = np.empty_like(Xr)
    lo, hi = Xr < 1 - 1e-6, Xr > 1 + 1e-6; mid = ~(lo | hi)
    xl, xh = Xr[lo], Xr[hi]
    out[lo] = (1 - 2 / np.sqrt(1 - xl ** 2) * np.arctanh(np.sqrt((1 - xl) / (1 + xl)))) / (xl ** 2 - 1)
    out[hi] = (1 - 2 / np.sqrt(xh ** 2 - 1) * np.arctan(np.sqrt((xh - 1) / (xh + 1)))) / (xh ** 2 - 1)
    out[mid] = 1.0 / 3.0
    return out


def nfw_fit_centre(S, x0, y0, r_in=40.0, r_out=300.0):
    """centre of a projected-NFW profile (plus a constant) least-squares fitted to the convergence map on the annulus
    r_in < R < r_out around the prior centre -- the analogue of a Lenstool NFW-halo fit to the shear."""
    from scipy.optimize import least_squares
    X = GH.x[:, None] + DXH / 2 + 0 * GH.x[None, :]; Y = GH.x[None, :] + DXH / 2 + 0 * GH.x[:, None]
    R0 = np.hypot(X - x0, Y - y0); sel = (R0 > r_in) & (R0 < r_out)
    xs, ys, ss_ = X[sel], Y[sel], S[sel]
    def res(p):
        R = np.hypot(xs - p[0], ys - p[1])
        return (math.exp(p[2]) * sig_nfw_shape(R / math.exp(p[3])) + p[4] - ss_) / max(float(np.median(np.abs(ss_))), 1e-30)
    A0 = float(np.interp(100.0, np.sort(R0[sel]), ss_[np.argsort(R0[sel])])) / float(sig_nfw_shape(np.array([100.0 / 150.0]))[0])
    sol = least_squares(res, [x0, y0, math.log(max(A0, 1e-30)), math.log(150.0), 0.0], x_scale=[10, 10, 1, 1, abs(A0) * 0.01 + 1e-30])
    return float(sol.x[0]), float(sol.x[1])


def paint_at(rho1d, cx, cy, norm):
    return GH.paint(rho1d, (cx - DXH / 2, cy - DXH / 2, -DXH / 2), norm_mass=norm)   # centred on cell corners at (cx, cy)


HB = []
foot_B = "canonical"
CONF = [(Msub, dSG, orient) for Msub in (1e14, 3e14) for dSG in (60.0, 120.0) for orient in ("perp", "toward_main")]
RES = {}
for (Msub, dSG, orient) in CONF:                                       # LCDM (linear): the substructure alone
    gx, gy = (XSUB, dSG) if orient == "perp" else (XSUB - dSG, 0.0)
    ux, uy = ((0.0, 1.0) if orient == "perp" else (-1.0, 0.0))
    HsL, _ = solve_real(Msub, ZH, A0K[foot_B], SW_DEF, "intact", fgas=0.10, fstar=0.02, kernel=False)
    SL = (paint_at(HsL.rho_c + HsL.rho_s, XSUB, 0.0, m_in(HsL.rho_c + HsL.rho_s, 1e9))
          + paint_at(HsL.rho_g, gx, gy, m_in(HsL.rho_g, 1e9))).sum(axis=2) * DXH
    # (LCDM: the same components, all real; linear, so the main cluster's own map is simply left out, as Harvey's
    #  multi-halo fit removes it)
    res = dict(Msub=Msub, dSG=dSG, orient=orient, gx=gx, gy=gy, ux=ux, uy=uy)
    for Rap in (100.0, 150.0):
        cxL, cyL = centroid(SL, XSUB, 0.0, Rap)
        res[f"LCDM_{Rap:.0f}"] = (cxL - XSUB) * ux + cyL * uy
    fxL, fyL = nfw_fit_centre(SL, XSUB, 0.0)
    res["LCDM_fit"] = (fxL - XSUB) * ux + fyL * uy
    RES[(Msub, dSG, orient)] = res
P(f"    LCDM substructure maps done   [{time.time() - T0:.0f}s]")
ic0 = NH // 2; icx = int(round((XSUB + LH / 2) / DXH))
for gate in GATE:
    Hm, _ = solve_real(1e15, ZH, A0K[foot_B], SW_DEF, gate)
    bm = paint_at(Hm.rho_b, 0.0, 0.0, m_in(Hm.rho_b, 1e9)); cm = paint_at(Hm.rho_c, 0.0, 0.0, m_in(Hm.rho_c, 1e9))
    _, _, rph, _ = phantom_felt(GH, bm, bm + cm, ZH, A0K[foot_B], SW_DEF, [(ic0, ic0, ic0)])
    SMAIN = (bm + cm + rph).sum(axis=2) * DXH                          # the main cluster alone (Harvey's multi-halo fit removes it)
    del rph
    for Msub in (1e14, 3e14):
        Hs, _ = solve_real(Msub, ZH, A0K[foot_B], SW_DEF, gate, fgas=0.10, fstar=0.02)
        ss = paint_at(Hs.rho_s, XSUB, 0.0, m_in(Hs.rho_s, 1e9)); cs = paint_at(Hs.rho_c, XSUB, 0.0, m_in(Hs.rho_c, 1e9))
        for (Ms_, dSG, orient) in CONF:
            if Ms_ != Msub:
                continue
            res = RES[(Msub, dSG, orient)]
            gs = paint_at(Hs.rho_g, res["gx"], res["gy"], m_in(Hs.rho_g, 1e9))
            rb = bm + ss + gs; rreal = rb + cm + cs
            gfelt, labs, rph, nlab = phantom_felt(GH, rb, rreal, ZH, A0K[foot_B], SW_DEF, [(ic0, ic0, ic0), (icx, ic0, ic0)])
            S = (rreal + rph).sum(axis=2) * DXH - SMAIN
            gN = GH.field(rreal)
            a_st = [float(((gN[i] + gfelt[i]) * ss).sum() / ss.sum()) for i in range(2)]
            a_ca = [float((gN[i] * cs).sum() / cs.sum()) for i in range(2)] if cs.sum() > 0 else [a_st[0], a_st[1]]
            da = math.hypot(a_st[0] - a_ca[0], a_st[1] - a_ca[1])
            R2 = ((GH.x[:, None, None] + DXH / 2 - XSUB) ** 2 + (GH.x[None, :, None] + DXH / 2) ** 2 + (GH.x[None, None, :] + DXH / 2) ** 2)
            rho50 = float(((rreal + rph) * (R2 <= 50.0 ** 2)).sum() * GH.dV) / (4 / 3 * math.pi * 50.0 ** 3)
            del R2
            for Rap in (100.0, 150.0):
                cxc, cyc = centroid(S, XSUB, 0.0, Rap)
                shift = (cxc - XSUB) * res["ux"] + cyc * res["uy"]
                res[f"{gate}_{Rap:.0f}"] = shift
                res[f"beta_{gate}_{Rap:.0f}"] = (shift - res[f"LCDM_{Rap:.0f}"]) / dSG
            fxc, fyc = nfw_fit_centre(S, XSUB, 0.0)
            res[f"{gate}_fit"] = (fxc - XSUB) * res["ux"] + fyc * res["uy"]
            res[f"beta_{gate}_fit"] = (res[f"{gate}_fit"] - res["LCDM_fit"]) / dSG
            res[f"dx_eq_{gate}"] = da / (4 / 3 * math.pi * GK * rho50)
            res[f"merged_{gate}"] = labs[0] == labs[1] and labs[0] > 0
            del gs, rb, rreal, gfelt, rph, gN
        del ss, cs
    del bm, cm, SMAIN
    P(f"    {gate} done   [{time.time() - T0:.0f}s]")
for (Msub, dSG, orient) in CONF:
    res = RES[(Msub, dSG, orient)]; HB.append(res)
    P(f"    sub {Msub:.0e} dSG {dSG:.0f} {orient:11s}: LCDM gas pull {res['LCDM_100']:+.1f}/{res['LCDM_150']:+.1f}/{res['LCDM_fit']:+.1f} kpc; "
      "excess beta (100 kpc / 150 kpc / NFW fit) "
      + "; ".join(f"{g_} {res[f'beta_{g_}_100']:+.3f}/{res[f'beta_{g_}_150']:+.3f}/{res[f'beta_{g_}_fit']:+.3f}" for g_ in GATE)
      + f"  (star-carrier equilibrium offset {res['dx_eq_intact']:.1f} kpc intact, {res['dx_eq_cleared_2000']:.1f} cleared)")
OUT["numbers"]["B_rows"] = HB
gp = [abs(r["LCDM_100"]) for r in HB] + [abs(r["LCDM_150"]) for r in HB]
check("B1 (control) LCDM's own gas pull on the lensing centroid is a few kpc in these configurations, the size of Harvey's "
      "correction (4.3 +/- 1.6 kpc on average)", f"{min(gp):.1f}-{max(gp):.1f} kpc", max(gp) < 15.0, load_bearing=False)
bI = [r[f"beta_intact_{a}"] for r in HB for a in (100, 150)]
check("B2 intact carrier: the construction's excess beta lies within 2 sigma of Harvey's <beta> = -0.04 +/- 0.07 "
      "(-0.18 <= beta <= +0.10) in every configuration", f"beta {min(bI):+.3f} to {max(bI):+.3f}",
      all(HARV_BETA - 2 * HARV_ERR <= b <= HARV_BETA + 2 * HARV_ERR for b in bI))
bD = {g_: [r[f"beta_{g_}_{a}"] for r in HB for a in (100, 150)] for g_ in ("cleared_2000", "cap_1000")}
check("B3 core-decayed carrier (L357's strict cells): the same test",
      "; ".join(f"{g_} beta {min(v):+.3f} to {max(v):+.3f}" for g_, v in bD.items()),
      all(HARV_BETA - 2 * HARV_ERR <= b <= HARV_BETA + 2 * HARV_ERR for v in bD.values() for b in v))

bU = [r[f"beta_uniform_0.55_{a}"] for r in HB for a in (100, 150)]
check("B4 (design pointer) a carrier depleted UNIFORMLY to X-COP's retained fraction 0.55 (rather than decayed in the core) "
      "passes the same test", f"beta {min(bU):+.3f} to {max(bU):+.3f}",
      all(HARV_BETA - 2 * HARV_ERR <= b <= HARV_BETA + 2 * HARV_ERR for b in bU), load_bearing=False)

bIf = [r["beta_intact_fit"] for r in HB]
check("B5 with the Lenstool-like projected-NFW fit (Harvey's estimator): the intact carrier's excess beta lies within 2 sigma "
      "of <beta> in every configuration", f"beta {min(bIf):+.3f} to {max(bIf):+.3f}",
      all(HARV_BETA - 2 * HARV_ERR <= b <= HARV_BETA + 2 * HARV_ERR for b in bIf))
bDf = {g_: [r[f"beta_{g_}_fit"] for r in HB] for g_ in ("cleared_2000", "cap_1000")}
check("B6 with the Lenstool-like projected-NFW fit: the core-decayed carrier (L357's strict cells), the same test",
      "; ".join(f"{g_} beta {min(v):+.3f} to {max(v):+.3f}" for g_, v in bDf.items()),
      all(HARV_BETA - 2 * HARV_ERR <= b <= HARV_BETA + 2 * HARV_ERR for v in bDf.values() for b in v))
OUT["numbers"]["B_mean_beta"] = {g_: {est: float(np.mean([r[f"beta_{g_}_{est}"] for r in HB])) for est in ("100", "150", "fit")}
                                 for g_ in GATE}
P("    configuration-averaged excess beta (100 / 150 / fit): " + "; ".join(
    f"{g_} " + "/".join(f"{OUT['numbers']['B_mean_beta'][g_][e]:+.3f}" for e in ("100", "150", "fit")) for g_ in GATE))
sig = {g_: {e: (OUT["numbers"]["B_mean_beta"][g_][e] - HARV_BETA) / HARV_ERR for e in ("100", "150", "fit")} for g_ in GATE}
OUT["numbers"]["B7_sigma"] = sig
check("B7 (reported) the population-mean comparison: configuration-averaged excess beta minus Harvey's <beta>, in sigma "
      "(100 kpc / 150 kpc / NFW fit)", "; ".join(f"{g_} " + "/".join(f"{sig[g_][e]:+.1f}" for e in ("100", "150", "fit"))
                                                for g_ in GATE), True,
      "every carrier pulls the lensing peak toward the displaced gas (the gas's phantom); the core-decayed carriers most",
      load_bearing=False)

# ============================================================================================================ verdict
banner("VERDICT")
n_ok = sum(1 for _, ok, _ in CH if ok); n_lb_fail = sum(1 for _, ok, lb in CH if (not ok) and lb)
P(f"  {n_ok}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}   [{time.time() - T0:.0f}s]")
with open(os.path.join(HERE, SLUG + "_results.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=float)
P(f"  wrote {SLUG}_results.json")
rc = 1 if n_lb_fail else 0
P(f"rc={rc}")
sys.exit(rc)
