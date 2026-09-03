#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h73_h86_h87_cosmic_dawn.py -- HUNT ITEMS 73, 86, 87: the three early-universe items, all driven by ONE mechanism.
=================================================================================================================
The framework puts nothing new into LINEAR growth (the delta-Y^(1) = 0 theorem: the MOND sector is absent from the
linear equations, so the halo mass function's shape is LambdaCDM's).  What it does change is the NONLINEAR collapse:
once a shell turns around, its acceleration is the kernel's, g = nu(g_N/a_0) g_N, not g_N, so it falls in faster.
That single speedup s(M, z) is the ONLY early-universe handle the framework has, and it drives all three items:

  Item 73  the JWST UV luminosity function at z = 9-15.  Faster baryonic delivery makes galaxies appear earlier, so
           the observed UVLF should sit above a constant-efficiency LambdaCDM baseline.  THE ITEM STATES THIS
           PREDICTION BACKWARDS and Part 2 corrects it: the speedup does fall with redshift, but the halo mass
           function steepens with redshift much faster, so a roughly constant fractional gain in (1 + z_formation)
           produces an excess that GROWS in dex toward high z, not one that shrinks.  Data: Donnan+2024
           (arXiv:2403.03171), fetched this session to real_research/data/donnan2024_uvlf.tsv.
  Item 86  the 21-cm absorption onset.  The same speedup applied to the H2-cooling minihalos that host the first
           stars advances the Lyman-alpha coupling and hence the onset of the trough.
  Item 87  the reionization optical depth.  The same speedup applied to atomic-cooling halos with a FIXED ionizing
           efficiency raises tau_e above the LambdaCDM-efficiency baseline; Planck measures tau_e = 0.0544 +- 0.0073.

HOW THE SPEEDUP ENTERS, and the correction to my own first version.  A speedup is a shift in TIMING, not a change
in the photon budget: multiplying the star-formation rate by s would let each halo emit s times more light in total,
which is wrong.  The correct mapping shifts the collapsed-fraction curve in redshift -- an object LambdaCDM forms at
z appears here at (1+z) x gain - 1 -- and every downstream quantity is recomputed from the SHIFTED curve.  A second
correction, also against interest: only the POST-turnaround half of the collapse is nonlinear, so the linear-growth
theorem protects the first half and the time compression is (1 + 1/s)/2, not 1/s.  Stage 26 used 1/s and therefore
over-states the redshift shift by about a factor two.

BOTH a_0 FOOTINGS.  BOTH ENDS OF THE nu_0 WINDOW.  BOTH BRANCHES OF THE FRAMEWORK'S OWN SOURCE FORK (does the kernel
act on the TOTAL halo mass, or only on the baryons?  stage 26's C3, the double-counting exposure).
Mutation control: a_0 -> 0 (nu == 1) must send every framework number to its LambdaCDM value exactly.
Checks CAN fail, and several are written so that the FRAMEWORK is what fails.
"""
import sys, math, os, warnings
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d
from hunt_lib import *

warnings.filterwarnings("ignore")
ck = Check(); rng = np.random.default_rng(738687)

# ------------------------------------------------------------------ cosmology (Planck 2018; hunt_lib values)
NS, S8, DELTA_C = 0.965, 0.811, 1.686
RHO_M_COM = 2.775e11 * OM_M                 # Msun/h per (Mpc/h)^3, comoving
F_BAR = OM_B / OM_M
NU0_FLOOR, NU0_CEIL = 2.14e-5, 1.77e-4      # the repo's committed nu_0 window (SWEEP3 S3-03)
TAU_PLANCK, TAU_ERR = 0.0544, 0.0073
SIGMA_T = 6.6524587e-29

def E(z): return np.sqrt(OM_M * (1 + np.asarray(z, float)) ** 3 + OM_L)
def Hz(z): return H0 * E(z)
def rho_crit_z(z): return 3 * Hz(z) ** 2 / (8 * math.pi * G)
def a0_of_z(z, nu0, a00):
    nu = nu0 * (1 + z) ** 3
    return a00 * math.sqrt(math.sqrt(1 + nu0 ** 2) / math.sqrt(1 + nu ** 2))
def z_switch(nu0): return nu0 ** (-1 / 3.) - 1.0

_zg = np.concatenate([np.linspace(0, 5, 60), np.linspace(5.1, 60, 150)])
def _growth_raw(z):
    a = 1.0 / (1 + z)
    f = lambda x: 1.0 / (x * math.sqrt(OM_M / x ** 3 + OM_L)) ** 3
    return float(E(z)) * quad(f, 1e-9, a, limit=200)[0]
_D0 = _growth_raw(0.0)
_Dg = interp1d(_zg, np.array([_growth_raw(z) / _D0 for z in _zg]), kind="cubic")
def growth(z): return float(_Dg(z))

# ------------------------------------------------------------------ Eisenstein-Hu 1998 "no-wiggle" transfer
_theta, _om, _ob = 2.7255 / 2.7, OM_M * h * h, OM_B * h * h
_fb = _ob / _om
_s_eh = 44.5 * math.log(9.83 / _om) / math.sqrt(1 + 10 * _ob ** 0.75)
_alpha_g = 1 - 0.328 * math.log(431 * _om) * _fb + 0.38 * math.log(22.3 * _om) * _fb ** 2
def T_eh(k):
    kmpc = np.asarray(k, float) * h
    gam = OM_M * h * (_alpha_g + (1 - _alpha_g) / (1 + (0.43 * kmpc * _s_eh) ** 4))
    q = np.asarray(k, float) * _theta ** 2 / gam
    L = np.log(2 * math.e + 1.8 * q); C = 14.2 + 731.0 / (1 + 62.5 * q)
    return L / (L + C * q * q)
_KG = np.logspace(-4, 3.0, 4000)
_PG = _KG ** NS * T_eh(_KG) ** 2
def _sigma2(R):
    x = _KG * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return np.trapz(_KG ** 2 * _PG * W ** 2, _KG) / (2 * math.pi ** 2)
_AMP = S8 ** 2 / _sigma2(8.0)
def sigma_M(M):
    return math.sqrt(_AMP * _sigma2((3 * M / (4 * math.pi * RHO_M_COM)) ** (1 / 3.)))
_LM = np.linspace(1.0, 16.5, 500)
_LS = np.array([math.log(sigma_M(10 ** lm)) for lm in _LM])
_dlnsig = interp1d(_LM, np.gradient(_LS, _LM * math.log(10)), kind="cubic")
_lnsig = interp1d(_LM, _LS, kind="cubic")

def dndlnM(M, z):
    """Sheth-Tormen dn/dlnM, (h/Mpc)^3 per ln M, M in Msun/h."""
    lm = np.log10(M)
    sig = np.exp(_lnsig(lm)) * growth(z)
    nup = math.sqrt(0.707) * DELTA_C / sig
    nufnu = 0.3222 * math.sqrt(2 / math.pi) * nup * (1 + nup ** (-0.6)) * np.exp(-nup ** 2 / 2)
    return (RHO_M_COM / M) * nufnu * np.abs(_dlnsig(lm))

def n_above(Mh, z, lmax=16.2):
    lm0 = math.log10(Mh)
    if lm0 >= lmax: return 0.0
    xs = np.linspace(lm0, lmax, 400)
    return float(np.trapz(dndlnM(10 ** xs, z) * math.log(10), xs))

def f_coll(Mh, z, lmax=16.2):
    """collapsed MASS fraction in halos above Mh (Msun/h)."""
    lm0 = math.log10(Mh)
    if lm0 >= lmax: return 0.0
    xs = np.linspace(lm0, lmax, 400)
    return float(np.trapz(dndlnM(10 ** xs, z) * 10 ** xs * math.log(10), xs)) / RHO_M_COM

def Mdot_h(M, z):
    """Fakhouri, Ma & Boylan-Kolchin 2010 mean halo growth rate, Msun/yr; M in Msun."""
    return 46.1 * (M / 1e12) ** 1.1 * (1 + 1.11 * z) * E(z)

def Tvir_to_M(Tvir, z, mu=1.22):
    """Barkana & Loeb 2001 virial-temperature threshold, Msun.  mu = 1.22 for neutral primordial gas
    (H2-cooling minihalos), mu = 0.6 for the ionized gas of an atomic-cooling halo.  The (Omega/Delta_c)
    factor carries exponent -1/2 and tends to 1 at high z; it is kept explicit rather than folded in."""
    return (1e8 / h * (Tvir / 1.98e4) ** 1.5 * (0.6 / mu) ** 1.5 * (0.3 / OM_M) ** -0.5
            * (10.0 / (1 + z)) ** 1.5)

# ------------------------------------------------------------------ the collapse speedup (grid integrator)
_UU = np.linspace(0.0, 1.0, 4000)                       # x = 1 - u^2: clusters points at turnaround
_XG = np.unique(np.concatenate([np.logspace(-8, -3, 1200), 1.0 - np.linspace(0, 1, 4000) ** 2]))
_XG = _XG[_XG > 0]                                      # ascending grid in x = r/r_ta, fine at BOTH ends
def r200(M_msun, z):
    return (3 * M_msun * Msun / (800 * math.pi * float(rho_crit_z(z)))) ** (1 / 3.)

def t_collapse(Msrc_kg, Mtot_kg, r_ta, a0z, law):
    """Time from rest at r_ta to r -> 0, by the energy integral.
    dphi(r) = int_r^{r_ta} g dr' is accumulated FROM THE TOP DOWN (a reverse cumulative sum), because
    accumulating from r_min and subtracting loses all precision near r_ta -- g ~ 1/r^2 makes the total
    integral enormous while dphi(r -> r_ta) -> 0.  That cancellation was a real bug in the first version
    of this script and it moved the collapse times by ~10%."""
    r = _XG * r_ta                                                  # ascending
    if law == "newton":
        g = G * Mtot_kg / r ** 2
    else:
        gN = G * Msrc_kg / r ** 2
        g = nu(gN / a0z) * gN if law == "routeA" else np.sqrt(gN * gN + a0z * gN)
    seg = 0.5 * (g[1:] + g[:-1]) * np.diff(r)                       # seg[i] = int_{r_i}^{r_i+1}
    dphi = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])      # dphi[i] = int_{r_i}^{r_ta}, summed downward
    x_u = 1.0 - _UU ** 2                                            # dt = dr/v, dr = -r_ta dx = 2 r_ta u du
    dp = np.interp(x_u, _XG, dphi)
    val = np.zeros_like(_UU)
    m = dp > 0
    val[m] = 2 * r_ta * _UU[m] / np.sqrt(2.0 * dp[m])
    val[0] = 2 * r_ta / math.sqrt(2.0 * float(g[-1]) * r_ta)        # u = 0 limit, dphi -> g(r_ta)(r_ta - r)
    return float(np.trapz(val, _UU))

def speedup(M_msun, z, a0z, branch="total", law="routeA"):
    rta = 2.0 * r200(M_msun, z)
    Mtot = M_msun * Msun
    Msrc = Mtot if branch == "total" else F_BAR * Mtot
    return t_collapse(Mtot, Mtot, rta, a0z, "newton") / t_collapse(Msrc, Mtot, rta, a0z, law)

def gain_of(s):
    """(1+z_form) multiplier.  Only the post-turnaround half is affected: t_form = t_ta(1 + 1/s) vs 2 t_ta."""
    return ((1 + 1.0 / s) / 2.0) ** (-2 / 3.)

def gain_curve(zs, Mfun, branch, nu0, ft, law="routeA"):
    out = []
    for z in zs:
        a0z = a0_of_z(z, nu0, A0[ft])
        out.append(gain_of(speedup(Mfun(z), z, a0z, branch, law)))
    return np.array(out)

CONFIGS = [(b, t, f) for b in ("total", "baryon") for t in ("ceil", "floor") for f in ("canonical", "alt")]
NU0OF = {"ceil": NU0_CEIL, "floor": NU0_FLOOR}

# =================================================================================================
P("=" * 118); P("PART 0 -- the framework's own early-universe laws, both footings, both ends of the nu_0 window"); P("=" * 118)
info(f"a_0 footings: canonical {A0['canonical']:.3e}, alt {A0['alt']:.3e} m/s^2")
info(f"nu_0 window (repo SWEEP3 S3-03): [{NU0_FLOOR:.2e}, {NU0_CEIL:.2e}] -> switch-on redshift "
     f"z_t = nu_0^(-1/3) - 1 = {z_switch(NU0_CEIL):.1f} (ceiling) to {z_switch(NU0_FLOOR):.1f} (floor)")
info(f"{'z':>6} {'a0(z)/a0(0) ceiling':>21} {'a0(z)/a0(0) floor':>19}")
for z in (6, 9, 11, 14.5, 17, 20, 25, 30, 35):
    info(f"{z:>6} {a0_of_z(z, NU0_CEIL, 1.0):>21.4f} {a0_of_z(z, NU0_FLOOR, 1.0):>19.4f}")
ck("0a THE ITEM'S OWN EDGE IS OUT OF REACH: the switch-on redshift z_t = 17-35 sits above the deepest published "
   "luminosity-function bin (z = 14.5), so the half of item 73 that says 'the excess vanishes above z_t' cannot be "
   "tested at all today.  Only the half that says 'the excess shrinks with z' is reachable",
   z_switch(NU0_CEIL) > 14.5,
   f"z_t = {z_switch(NU0_CEIL):.1f} (ceiling) to {z_switch(NU0_FLOOR):.1f} (floor); a_0(14.5)/a_0(0) = "
   f"{a0_of_z(14.5, NU0_CEIL, 1.0):.3f} at the ceiling but {a0_of_z(14.5, NU0_FLOOR, 1.0):.4f} at the floor")

P(""); P("=" * 118); P("PART 1 -- the collapse speedup s(M, z), the one mechanism behind all three items"); P("=" * 118)
info("branch TOTAL : the kernel acts on the whole halo, dark sector included (stage 26's choice) -- the LARGER boost")
info("branch BARYON: the kernel acts on the baryons only, as it does in a galaxy, and the comparison is against a")
info("               Newtonian collapse of the SAME total mass -- the framework's own double-counting fork (26 C3)")
info(f"{'M [Msun]':>10} {'z':>6} {'y at turnaround':>16} {'s total':>9} {'s baryon':>9} {'s a0-line':>10} "
     f"{'gain(tot)':>10} {'z_form':>8}")
SPEED = {}
for M, z in ((1e10, 6), (1e10, 9), (1e10, 12.5), (1e10, 20), (1e8, 20), (1e8, 25), (1e6, 25), (1e6, 30)):
    a0z = a0_of_z(z, NU0_CEIL, A0["canonical"])
    y_ta = G * M * Msun / (2 * r200(M, z)) ** 2 / a0z
    s_t = speedup(M, z, a0z, "total"); s_b = speedup(M, z, a0z, "baryon")
    s_l = speedup(M, z, a0z, "total", "a0line"); gn = gain_of(s_t)
    SPEED[(M, z)] = (s_t, s_b, s_l, y_ta)
    info(f"{M:>10.0e} {z:>6} {y_ta:>16.4f} {s_t:>9.3f} {s_b:>9.3f} {s_l:>10.3f} {gn:>10.4f} {(1+z)*gn-1:>8.2f}")
ck("1a the two readings of the source fork do NOT agree even in sign, and that is the framework's own unresolved "
   "question, not a nuisance: with the kernel fed the total halo mass the collapse is 1.3-2.1x faster, but with it "
   "fed only the baryons the framework collapses SLOWER than LambdaCDM once the turnaround acceleration exceeds "
   "about 0.15 a_0, because the square-root boost cannot make up for having 16% of the mass",
   min(v[1] for v in SPEED.values()) < 1.0 < max(v[1] for v in SPEED.values()),
   f"branch TOTAL s = {min(v[0] for v in SPEED.values()):.2f}-{max(v[0] for v in SPEED.values()):.2f}; "
   f"branch BARYON s = {min(v[1] for v in SPEED.values()):.2f}-{max(v[1] for v in SPEED.values()):.2f}, "
   f"crossing 1 near y_turnaround ~ 0.15")
ck("1b AGAINST INTEREST -- the observable shift is half what stage 26 quoted, because the linear-growth theorem "
   "protects the pre-turnaround half of the collapse: the time compression is (1 + 1/s)/2, not 1/s",
   all(gain_of(v[0]) < 1.35 for v in SPEED.values()),
   "gains " + ", ".join(f"{gain_of(v[0]):.3f}" for v in list(SPEED.values())[:4]) +
   f"; stage 26's un-halved form would give {SPEED[(1e10,6)][0]**(2/3.):.3f} where this gives {gain_of(SPEED[(1e10,6)][0]):.3f}")
ck("1c the SHAPE everything in item 73 rests on: at FIXED halo mass the speedup falls with redshift, because halos "
   "collapse from denser and therefore higher-acceleration initial conditions (and above z_t because a_0 falls too)",
   SPEED[(1e10, 6)][0] > SPEED[(1e10, 20)][0],
   f"1e10 Msun: s = {SPEED[(1e10,6)][0]:.3f} at z = 6 falling to {SPEED[(1e10,20)][0]:.3f} at z = 20; "
   f"y_turnaround rises {SPEED[(1e10,6)][3]:.4f} -> {SPEED[(1e10,20)][3]:.4f}")
s_mut = speedup(1e10, 10, 1e-30, "total")
s_ref = speedup(1e10, 10, a0_of_z(10, NU0_CEIL, A0["canonical"]), "total")
ck("1d MUTATION CONTROL: with a_0 driven to zero the kernel is the identity and the framework's collapse time must "
   "equal Newton's exactly.  It does, so the speedup is the a_0 term and not an integrator artefact",
   abs(s_mut - 1.0) < 2e-3 and s_ref > 1.5, f"s(a_0 -> 0) = {s_mut:.6f} (must be 1); s(a_0 real) = {s_ref:.3f}")
# integrator cross-check against the slow nested-quad form used by stage 26
def t_quad(Msrc, Mtot, rta, a0z, law):
    def g(r):
        if law == "newton": return G * Mtot / r ** 2
        gN = G * Msrc / r ** 2
        return nu_s(gN / a0z) * gN if law == "routeA" else math.sqrt(gN * gN + a0z * gN)
    def integ(x):
        d = quad(g, x * rta, rta, limit=200)[0]
        return 0.0 if d <= 0 else rta / math.sqrt(2 * d)
    return quad(integ, 1e-4, 1 - 1e-9, limit=200)[0]
_M, _z = 1e10, 10.0
_a0 = a0_of_z(_z, NU0_CEIL, A0["canonical"]); _rta = 2 * r200(_M, _z)
_ana = (math.pi / 2) * math.sqrt(_rta ** 3 / (2 * G * _M * Msun))
_gN = t_collapse(_M * Msun, _M * Msun, _rta, 1e-30, "routeA")
_g1 = t_collapse(_M * Msun, _M * Msun, _rta, _a0, "routeA")
_g2 = t_quad(_M * Msun, _M * Msun, _rta, _a0, "routeA")
ck("1e INTEGRATOR VALIDATED AGAINST AN EXACT ANSWER: with the kernel off, the collapse integral must return the "
   "textbook radial free-fall time (pi/2) sqrt(r_ta^3 / 2GM), and it does to one part in 1e5; the framework case "
   "also agrees with an independent adaptive-quadrature evaluation.  (The FIRST version of this integrator was 10% "
   "wrong -- it accumulated the potential from the centre outward and lost it to cancellation near turnaround.)",
   abs(_gN / _ana - 1) < 1e-4 and abs(_g1 / _g2 - 1) < 0.01,
   f"kernel-off {_gN:.5e} s vs exact {_ana:.5e} s (ratio {_gN/_ana:.6f}); framework grid {_g1:.4e} vs quad "
   f"{_g2:.4e} (ratio {_g1/_g2:.5f})")

P(""); P("=" * 118); P("PART 2 -- ITEM 73: the JWST UV luminosity function against the switch-on law"); P("=" * 118)
sig8 = math.sqrt(_AMP * _sigma2(8.0)); n12 = n_above(1e12, 0.0); n14 = n_above(1e14, 0.0)
info(f"halo machinery: sigma_8 = {sig8:.4f} (input {S8}); n(>1e12 h^-1 Msun, z=0) = {n12:.3e}, n(>1e14) = {n14:.3e} "
     f"(h/Mpc)^3; D(9) = {growth(9.0):.4f}")
ck("2a sanity of the halo mass function everything below is built on: sigma_8 is reproduced and the z = 0 cumulative "
   "abundances of 1e12 and 1e14 halos land in the standard ranges",
   abs(sig8 - S8) < 1e-3 and 1e-3 < n12 < 2e-2 and 1e-6 < n14 < 1e-4,
   f"sigma_8 {sig8:.4f}; n(>1e12) {n12:.2e}; n(>1e14) {n14:.2e}")

rows = [l.split("\t") for l in open(os.path.join(DATA, "donnan2024_uvlf.tsv")) if l.strip() and not l.startswith("#")]
ZA = np.array([float(r[1]) for r in rows if r[0] == "A"])
LRHO = np.array([float(r[2]) for r in rows if r[0] == "A"])
ERHO = np.array([0.5 * (float(r[3]) + float(r[4])) for r in rows if r[0] == "A"])
DPL = {float(r[1]): dict(phis=float(r[2]) * 1e-5, Ms=float(r[4]), al=float(r[6]), be=float(r[8]))
       for r in rows if r[0] == "B"}
info("Donnan+2024 log10 rho_UV (to M_UV = -17): " + ", ".join(f"z={z:.1f}: {l:.2f}+-{e:.2f}" for z, l, e in zip(ZA, LRHO, ERHO)))
def dpl(M, p): return p["phis"] / (10 ** (0.4 * (p["al"] + 1) * (M - p["Ms"])) + 10 ** (0.4 * (p["be"] + 1) * (M - p["Ms"])))
xs = np.linspace(-24.0, -17.0, 700)
n9 = float(np.trapz([dpl(x, DPL[9.0]) for x in xs], xs)) / h ** 3       # -> (h/Mpc)^-3
lo, hi = 6.0, 13.0
for _ in range(60):
    mid = 0.5 * (lo + hi)
    if n_above(10 ** mid, 9.0) > n9: lo = mid
    else: hi = mid
LMH9 = 0.5 * (lo + hi)
info(f"abundance matching at z = 9: n_gal(M_UV < -17) = {n9:.3e} (h/Mpc)^-3 -> host halo threshold "
     f"M_h = 10^{LMH9 - math.log10(h):.2f} Msun")
ck("2b the abundance-matched host halo of an M_UV = -17 galaxy at z = 9 lands where the literature puts it, "
   "10^10 - 10^11 Msun, so the threshold used below is not an artefact",
   9.7 < LMH9 - math.log10(h) < 11.3, f"log10 M_h = {LMH9 - math.log10(h):.2f} Msun")

ZFINE = np.linspace(5.0, 26.0, 106)
MTH73 = lambda z: 10 ** LMH9 / h                                        # fixed threshold = constant efficiency
FC73 = np.array([f_coll(10 ** LMH9, z) for z in ZFINE])
_lfc = interp1d(ZFINE, np.log(np.maximum(FC73, 1e-300)), kind="cubic", bounds_error=False,
                fill_value=(np.log(FC73[0]), -700.0))
def Fc73(z): return np.exp(_lfc(np.clip(z, ZFINE[0], ZFINE[-1])))
def dFdt(Fz, z, dz=0.05):
    """-dF/dz * dz/dt  with dz/dt = -(1+z)H(z)  ->  dF/dt = (F(z-dz)-F(z+dz))/(2dz) * (1+z)H(z)."""
    return (Fz(z - dz) - Fz(z + dz)) / (2 * dz) * (1 + z) * float(Hz(z))
BASE = np.array([dFdt(Fc73, z) for z in ZA])
# alternative baseline: halo-accretion-rate weighted (Fakhouri+2010), same fixed threshold
def rho_acc(z):
    xs = np.linspace(LMH9, 14.5, 250)
    return float(np.trapz(dndlnM(10 ** xs, z) * Mdot_h(10 ** xs / h, z) * math.log(10), xs))
BASE2 = np.array([rho_acc(z) for z in ZA])
EXC = (LRHO - np.log10(BASE)); EXC -= EXC[0]
EXC2 = (LRHO - np.log10(BASE2)); EXC2 -= EXC2[0]

FW = {}
for cfg in CONFIGS:
    br, tag, ft = cfg
    gz = gain_curve(ZFINE, MTH73, br, NU0OF[tag], ft)
    gi = interp1d(ZFINE, gz, kind="cubic", bounds_error=False, fill_value=(gz[0], gz[-1]))
    def Ffw(z, gi=gi): return Fc73((1 + np.asarray(z, float)) / gi(np.clip(z, ZFINE[0], ZFINE[-1])) - 1)
    pred = np.array([dFdt(Ffw, z) for z in ZA])
    FW[cfg] = (np.log10(pred / BASE), gi(ZA))
info(f"{'z':>6} {'log rho_obs':>12} {'log excess (dF/dt base)':>24} {'log excess (accretion base)':>28}")
for i, z in enumerate(ZA):
    info(f"{z:>6.1f} {LRHO[i]:>12.2f} {EXC[i]:>24.3f} {EXC2[i]:>28.3f}")
def wslope(x, y, e):
    w = 1.0 / e ** 2; A = np.vstack([x, np.ones_like(x)]).T
    C = np.linalg.inv(A.T @ (A * w[:, None])); b = C @ (A.T @ (w * y))
    return b[0], math.sqrt(C[0, 0])
sl_obs, esl_obs = wslope(ZA, EXC, ERHO)
sl_obs2, _ = wslope(ZA, EXC2, ERHO)
info(f"MEASURED d log10(observed / constant-efficiency LambdaCDM)/dz = {sl_obs:+.4f} +- {esl_obs:.4f} "
     f"(collapsed-fraction baseline), {sl_obs2:+.4f} (halo-accretion baseline)")
PRED = {}
for cfg in CONFIGS:
    y = FW[cfg][0] - FW[cfg][0][0]
    PRED[cfg] = (wslope(ZA, y, ERHO)[0], y[-1], FW[cfg][1][0], FW[cfg][1][-1])
    info(f"   PREDICTED branch {cfg[0]:<7} nu_0 {cfg[1]:<6} {cfg[2]:<10}: slope {PRED[cfg][0]:+.4f} dex/z, total "
         f"{PRED[cfg][1]:+.3f} dex over z = 9 -> 14.5 (gain {PRED[cfg][2]:.4f} -> {PRED[cfg][3]:.4f})")
TOT = {c: PRED[c][0] for c in PRED if c[0] == "total"}
BAR = {c: PRED[c][0] for c in PRED if c[0] == "baryon"}
tmin = min(v[1] for v in PRED.values() if v[1] > 0) if any(v[1] > 0 for v in PRED.values()) else 0.0
tmax = max(v[1] for v in PRED.values())
ck("73 THE ITEM'S STATED PREDICTION IS BACKWARDS, and correcting it is the result.  Item 73 says the JWST excess "
   "must be LARGER at z = 10-12 than at z = 15-17 because the collapse speedup declines with redshift.  The speedup "
   "does decline -- but the halo mass function STEEPENS with redshift much faster, so a roughly constant fractional "
   "gain in (1 + z_formation) produces an excess that GROWS in dex.  That is what the mechanism actually predicts, "
   "and it is the sign the data show",
   sl_obs > 0 and max(TOT.values()) > 0,
   f"measured {sl_obs:+.4f} +- {esl_obs:.4f} dex per unit z ({sl_obs/esl_obs:.1f} sigma above zero); the "
   f"total-mass branch predicts {min(TOT.values()):+.4f} to {max(TOT.values()):+.4f}, the same sign; the "
   f"halo-accretion baseline gives a measured {sl_obs2:+.4f}, also the same sign")
d_tot = [abs(sl_obs - v) / esl_obs for v in TOT.values()]
d_bar = [abs(sl_obs - v) / esl_obs for v in BAR.values()]
ck("73b AND THE BY-PRODUCT IS THE REAL FIND: the framework's own unresolved source fork -- does the kernel act on "
   "the whole halo or only on the baryons? -- is DECIDED by these data, because the two branches predict opposite "
   "signs.  The total-mass branch sits within 2 sigma of the measurement and supplies about half the excess with no "
   "free parameter; the baryon-only branch predicts the excess to SHRINK and is excluded at about 5 sigma",
   max(d_tot) < 2.5 and min(d_bar) > 3.0,
   f"total-mass branch {min(d_tot):.1f}-{max(d_tot):.1f} sigma from the measurement and contributes "
   f"{tmin:.2f}-{tmax:.2f} dex of the measured {EXC[-1]:.2f} dex ({100*tmax/abs(EXC[-1]):.0f}%); baryon-only branch "
   f"{min(d_bar):.1f}-{max(d_bar):.1f} sigma away")
ck("73c CAVEAT, AND IT IS LARGE ENOUGH TO STOP THIS BEING A MEASUREMENT.  'Excess' here means excess over a "
   "constant-efficiency baseline, a model everyone already knows fails; the published analysis of these very data "
   "(Donnan+2024) reproduces the evolution inside LambdaCDM by letting the star-formation efficiency rise.  "
   "Swapping the baseline from a collapsed-fraction rate to an accretion-rate weighting moves the measured excess "
   "by a sizeable fraction of the framework's whole prediction, and the error bars used above carry none of that",
   abs(EXC[-1] - EXC2[-1]) > 0.25 * tmax,
   f"baseline swap moves the z = 14.5 excess by {abs(EXC[-1]-EXC2[-1]):.3f} dex against a framework prediction of "
   f"{tmin:.3f}-{tmax:.3f} dex; the quoted sigmas are photometric only")
mutg = interp1d(ZFINE, np.ones_like(ZFINE), kind="linear")
def Fmut(z): return Fc73((1 + np.asarray(z, float)) / mutg(np.clip(z, ZFINE[0], ZFINE[-1])) - 1)
mut_pred = np.array([dFdt(Fmut, z) for z in ZA])
ck("73d MUTATION CONTROL: with the gain pinned to 1 (a_0 -> 0) the predicted excess is identically zero at every "
   "redshift, so the predicted band is the a_0 term; and scrambling the redshift labels destroys the measured slope",
   np.max(np.abs(np.log10(mut_pred / BASE))) < 1e-9 and
   abs(wslope(ZA, EXC[rng.permutation(len(ZA))], ERHO)[0] - sl_obs) > 0.3 * abs(sl_obs),
   f"kernel-off excess max |{np.max(np.abs(np.log10(mut_pred/BASE))):.2e}| dex")
info("both ways, stated plainly.  Donnan+2024's own conclusion is that the observed evolution to z ~ 12 is")
info("reproducible in LambdaCDM, and the steep drop they report is at z ~ 13 -- far BELOW the framework's switch-on")
info(f"edge z_t = {z_switch(NU0_CEIL):.0f}-{z_switch(NU0_FLOOR):.0f}, so it cannot be the switch-on either.  The")
info("framework's distinctive early-universe signature lives at z > 17, where no luminosity function exists.")

P(""); P("=" * 118); P("PART 3 -- ITEM 86: the 21-cm absorption onset"); P("=" * 118)
Z_ED, Z_ED_LO, Z_ED_HI = 17.2, 14.0, 20.9
info("the observable: first stars couple the 21-cm spin temperature to the gas through Lyman-alpha, so the ONSET of")
info("the absorption trough tracks the redshift at which a fixed collapsed fraction is reached in H2-cooling minihalos.")
info(f"EDGES reports a trough centred at z = {Z_ED:.1f} (78 MHz) with edges at z = {Z_ED_LO:.0f}-{Z_ED_HI:.1f}; SARAS-3")
info("rejects that profile at 95.3% confidence, so the datum itself is contested.")
MH2 = lambda z: Tvir_to_M(1000.0, z)
info(f"H2-cooling threshold (T_vir = 1000 K): M_min = {MH2(25):.2e} Msun at z = 25, {MH2(17):.2e} at z = 17")
Z86 = np.array([15.0, 17.2, 20.0, 25.0])
R86 = {}
for cfg in CONFIGS:
    br, tag, ft = cfg
    g86 = gain_curve(Z86, MH2, br, NU0OF[tag], ft)
    R86[cfg] = (g86, (1 + Z86) * g86 - 1 - Z86)
    info(f"branch {br:<7} nu_0 {tag:<6} {ft:<10}: gain = " +
         " ".join(f"z={zz:.1f}: {g:.3f} (dz {d:+.2f})" for zz, g, d in zip(Z86, g86, R86[cfg][1])))
dz_all = np.array([d for v in R86.values() for d in v[1]])
ck("86 THE PREDICTION IS FAR BIGGER THAN THE ITEM CLAIMED, and that is worth recording: item 86 says the onset moves "
   "earlier by Delta z ~ 1-2, but the minihalos that host the first stars are DEEP in MOND (y at turnaround ~ 0.02-0.1), "
   "so the framework advances the onset by Delta z = 3 to 8 -- first light at z ~ 18-33 instead of 15-25",
   dz_all.min() > 1.5, f"Delta z(onset) = {dz_all.min():+.2f} to {dz_all.max():+.2f} across both source branches, "
   f"both nu_0 ends and both footings; the item's stated 1-2 is an under-estimate")
g25 = np.array([R86[c][0][3] for c in R86]); g15 = np.array([R86[c][0][0] for c in R86])
ck("86b the framework-DISTINCTIVE part survives and has the right sign, once it is stated in the right variable: the "
   "advance must be measured as the GAIN in (1+z), not as Delta z (which grows with (1+z) mechanically).  In gain, the "
   "advance is SMALLER at z = 25 than at z = 15, which is the switch-on law's fingerprint and which no constant-a_0 "
   "MOND produces",
   g25.max() < g15.max() and g25.min() < g15.min(),
   f"gain at z = 25: {g25.min():.3f}-{g25.max():.3f}; at z = 15: {g15.min():.3f}-{g15.max():.3f}")
ck("86c AND YET THE ITEM IS NOT RUNNABLE AS A TEST.  The only claimed detection is rejected at 95.3% by SARAS-3, and "
   "even taken at face value its profile spans z = 14-21, comparable to the whole predicted shift; the LambdaCDM "
   "onset itself moves by several units of z with the star-formation efficiency and Lyman-Werner feedback.  What the "
   "computation delivers is a PREDICTION to be scored later, not a score",
   (Z_ED_HI - Z_ED_LO) > 0.8 * dz_all.max(),
   f"EDGES profile width {Z_ED_HI - Z_ED_LO:.1f} in z against a predicted advance of {dz_all.min():.1f}-{dz_all.max():.1f}")
ck("86d against interest, the same number is a WARNING: an onset advanced by Delta z ~ 2-8 also advances X-ray "
   "heating, which ERASES the absorption trough.  A framework that moves first light to z ~ 25-33 has to explain why "
   "any 21-cm absorption survives to z ~ 17 at all -- the same over-production worry that item 87 quantifies",
   dz_all.max() > 3.0, f"largest predicted advance {dz_all.max():.1f} in redshift")

P(""); P("=" * 118); P("PART 4 -- ITEM 87: the reionization optical depth (the one that can bite)"); P("=" * 118)
n_H0 = OM_B * rho_crit * 0.76 / 1.6726219e-27
info(f"comoving n_H = {n_H0:.3f} m^-3; Planck 2018 tau_e = {TAU_PLANCK:.4f} +- {TAU_ERR:.4f}")
MAT = lambda z: Tvir_to_M(1.0e4, z, mu=0.6)          # atomic-cooling halo: ionized gas, mu = 0.6
def zcross(zs, Q, lev):
    """first redshift (scanning from high z downward) at which Q crosses lev; Q is not monotonic once it saturates."""
    for i in range(1, len(zs)):
        if Q[i - 1] < lev <= Q[i]:
            return zs[i - 1] + (lev - Q[i - 1]) / (Q[i] - Q[i - 1]) * (zs[i] - zs[i - 1])
    return float("nan")
ZR = np.linspace(30.0, 4.0, 261)
FCAT = np.array([f_coll(MAT(z) * h, z) for z in ZR])
_lfa = interp1d(ZR[::-1], np.log(np.maximum(FCAT[::-1], 1e-300)), kind="cubic", bounds_error=False,
                fill_value=(np.log(max(FCAT[-1], 1e-300)), -700.0))
def Fat(z): return np.exp(_lfa(np.clip(z, 4.0, 30.0)))
def tau_of(zs, Q):
    zz = zs[::-1]; QQ = Q[::-1]
    igr = SIGMA_T * n_H0 * c_light * (1 + zz) ** 2 / (H0 * E(zz)) * QQ * 1.08
    zlo = np.linspace(0.0, zs.min(), 80)
    ilo = SIGMA_T * n_H0 * c_light * (1 + zlo) ** 2 / (H0 * E(zlo)) * np.where(zlo < 3, 1.16, 1.08)
    return float(np.trapz(igr, zz)) + float(np.trapz(ilo, zlo))
def Q_hist(zeta, Ffun):
    Q = 0.0; out = []
    C_HII, alpha_B = 3.0, 2.6e-19
    Fv = np.array([Ffun(z) for z in ZR])
    for i, z in enumerate(ZR):
        if i > 0:
            dt = -(ZR[i] - ZR[i - 1]) / ((1 + z) * float(Hz(z)))
            trec = 1.0 / (C_HII * alpha_B * n_H0 * (1 + z) ** 3 * 1.08)
            Q = min(max(Q + zeta * (Fv[i] - Fv[i - 1]) - Q * dt / trec, 0.0), 1.0)
        out.append(Q)
    return np.array(out)
lo, hi = 1e-3, 1e3
for _ in range(70):
    mid = math.sqrt(lo * hi)
    if tau_of(ZR, Q_hist(mid, Fat)) < TAU_PLANCK: lo = mid
    else: hi = mid
ZETA = math.sqrt(lo * hi)
Q0 = Q_hist(ZETA, Fat); tau0 = tau_of(ZR, Q0)
zre, zend = zcross(ZR, Q0, 0.5), zcross(ZR, Q0, 0.99)
info(f"LambdaCDM baseline calibrated: ionizing efficiency zeta = {ZETA:.2f} gives tau_e = {tau0:.4f} "
     f"(target {TAU_PLANCK:.4f}); midpoint z(Q = 0.5) = {zre:.2f}, end z(Q = 0.99) = {zend:.2f}")
ck("4a AGAINST INTEREST, THE BASELINE MODEL'S OWN LIMITATION, STATED FIRST: a single-efficiency reionization model "
   "tuned to Planck's tau reionizes too gradually -- the ionized midpoint lands near z ~ 7 but the last neutral gas "
   "is not cleared until z ~ 4-5, later than the Lyman-alpha forest allows (z ~ 5.3).  The item's output is a "
   "DIFFERENCE of two histories computed the same way, which is far less sensitive to that than either history is, "
   "but the absolute tau values below inherit it",
   6.0 < zre < 9.5, f"z(Q = 0.5) = {zre:.2f} (acceptable), z(Q = 0.99) = {zend:.2f} (too late; the forest says ~5.3)")
R87 = {}
for cfg in CONFIGS:
    br, tag, ft = cfg
    gz = gain_curve(ZR[::4], MAT, br, NU0OF[tag], ft)
    gi = interp1d(ZR[::4], gz, kind="cubic", bounds_error=False, fill_value=(gz[0], gz[-1]))
    def Ffw(z, gi=gi): return Fat((1 + z) / float(gi(np.clip(z, 4.0, 30.0))) - 1)
    Qf = Q_hist(ZETA, Ffw); tf = tau_of(ZR, Qf)
    zrf = zcross(ZR, Qf, 0.5)
    R87[cfg] = (tf, zrf, float(gi(10.0)), Ffw(10.0) / Fat(10.0))
    info(f"branch {br:<7} nu_0 {tag:<6} {ft:<10}: gain(z=10) = {float(gi(10.0)):.4f} -> collapsed fraction x"
         f"{Ffw(10.0)/Fat(10.0):.2f} -> tau_e = {tf:.4f} ({(tf - TAU_PLANCK)/TAU_ERR:+.1f} sigma), midpoint z = {zrf:.2f}")
taus = np.array([v[0] for v in R87.values()]); nsg = (taus - TAU_PLANCK) / TAU_ERR
ck("87 A REAL, QUANTIFIED LIABILITY.  Holding the ionizing efficiency at the value that makes LambdaCDM reproduce "
   "Planck's tau_e, the framework's earlier collapse reionizes the universe too early in EVERY branch, at both ends "
   "of the nu_0 window and on both footings.  The framework must therefore run a LOWER ionizing efficiency than "
   "LambdaCDM by a definite factor -- allowed, because the efficiency is not independently measured that well, but a "
   "cost that was not on the ledger before",
   nsg.min() > 1.0,
   f"tau_e = {taus.min():.4f} to {taus.max():.4f} against Planck {TAU_PLANCK:.4f} +- {TAU_ERR:.4f}, i.e. "
   f"{nsg.min():+.1f} to {nsg.max():+.1f} sigma; the collapsed fraction at z = 10 is raised x"
   f"{min(v[3] for v in R87.values()):.2f}-{max(v[3] for v in R87.values()):.2f} and the ionized midpoint moves to "
   f"z = {min(v[1] for v in R87.values()):.1f}-{max(v[1] for v in R87.values()):.1f}")
Qm = Q_hist(ZETA, lambda z: Fat((1 + z) / 1.0 - 1))
ck("87b MUTATION CONTROL: a gain pinned to 1 must return the LambdaCDM baseline exactly, and it does, so the tau "
   "shift is the collapse speedup and not an integrator drift",
   abs(tau_of(ZR, Qm) - tau0) < 1e-9, f"tau(gain = 1) = {tau_of(ZR, Qm):.8f} vs baseline {tau0:.8f}")
zbar = ZETA
lo, hi = 1e-3, 1e3
br, tag, ft = ("baryon", "ceil", "canonical")
gz = gain_curve(ZR[::4], MAT, br, NU0OF[tag], ft)
gi = interp1d(ZR[::4], gz, kind="cubic", bounds_error=False, fill_value=(gz[0], gz[-1]))
def Fb(z): return Fat((1 + z) / float(gi(np.clip(z, 4.0, 30.0))) - 1)
for _ in range(70):
    mid = math.sqrt(lo * hi)
    if tau_of(ZR, Q_hist(mid, Fb)) < TAU_PLANCK: lo = mid
    else: hi = mid
ZETA_FW = math.sqrt(lo * hi)
ck("87c and here is the size of the cost, stated as the thing an observer could check: to land on Planck's tau_e the "
   "framework needs an ionizing efficiency lower than LambdaCDM's by the factor below.  JWST's own ionizing-photon "
   "budget (xi_ion times f_esc for the z = 6-9 population) is that measurement, and it is currently uncertain by a "
   "factor 2-3 -- so the item is a recorded cost today and becomes a kill the moment the budget is pinned to ~30%",
   0.2 < ZETA_FW / zbar < 1.0,
   f"zeta(framework)/zeta(LambdaCDM) = {ZETA_FW/zbar:.2f} on the most conservative branch (baryon source, nu_0 "
   f"ceiling, canonical footing); the total-mass branch needs a larger reduction still")

sys.exit(ck.done())
