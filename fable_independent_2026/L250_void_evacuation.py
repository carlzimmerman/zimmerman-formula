#!/usr/bin/env python3
"""L250 -- COSMIC VOIDS: the maximally-MOND environment, and what the kernel does to it.

WHY VOIDS.  A void interior is the lowest-acceleration place in the universe that contains any
matter at all.  The outward peculiar acceleration at the edge of a spherical under-density is
g = (4/3) pi G rho_m |delta| R, and for the observed void population (R ~ 10-50 Mpc/h, central
delta ~ -0.8) that is 1e-13 to 1e-12 m/s^2 -- two to three orders of magnitude BELOW a_0.  So a
MOND-like kernel is in its maximally-enhanced regime throughout a void's life, while in LCDM a void
is merely under-dense.  Enhanced outward gravity evacuates a void faster and further: EMPTIER voids,
LARGER voids, MORE of them.  That is a generic, sharp, and (in this repo) largely unrun prediction.

WHAT THIS REPO ALREADY HAS (established here before anything new is claimed; see PRIOR ART below):
  * nbody_2026/stage53_route_a_prime_closure_2026.py PART C -- the KBC/local-hole front.  C2 branch
    (ii) already records "every rms 12-Mpc void evacuates to delta = -0.993" under Haslbauer's
    MOND-on prescription, and C1 shows the kernel selects on ACCELERATION not scale (ratio 1.175).
  * hunt_2026/k01_acceleration_census.py -- ONE literature scalar, "cosmic void wall (R ~ 15 Mpc)
    g_int/a_0 ~ 0.003", tagged "framework's linear regime is Newtonian (item 85)".
  * hunt_2026/h76_h13_h36_h63.py item 63 -- void-versus-wall galaxies, an EXTERNAL-FIELD test on
    rotation-curve outer slopes.  Different physics; not void evacuation.
So a void lane EXISTS, at one scale, as a by-product of the KBC front.  WHAT IS UNRUN, and what this
script does, is the confrontation of the evacuation with the OBSERVED void population: the -0.993 was
never compared with a measured void profile, never computed across the observed size range, never
given a size-function direction, and never tested against the external field that real voids sit in.

THE ONE HONEST FORK THAT GOVERNS EVERYTHING BELOW.  stage53 C2 records two branches:
  (i)  the framework's OWN covariant cosmology (AeST): delta-Y^(1) = 0 on FRW, so the promoted MOND
       term is O(delta phi^3) and the linear enhancement is EXACTLY 1 -- voids evolve as in LCDM and
       there is NO void prediction at all.
  (ii) "MOND-on" (Haslbauer's prescription): nu applied to the peculiar acceleration.  This is the
       branch that produces a void signal -- and it is ALREADY excluded on other grounds in the same
       file (over-delivers 18.3-28x on the KBC amplitude; sigma_8 -> 1.38).
This script computes branch (ii) properly and says so.  It does NOT claim a new kill.

THE MODEL.  Exact split of the spherical-shell equation into background plus peculiar piece.  With
M fixed at the background mass of comoving Lagrangian radius R_L, x = r/(a R_L) = (1+delta)^(-1/3):
        x'' + (2 + dlnH/dN) x' + (Omega_m(a)/2) (x^-2 - x) nu(|A|/a_0) = 0,   N = ln a
        |A| = (Omega_m(a) H^2 / 2) |x^-2 - x| a R_L      (the Newtonian peculiar acceleration)
nu = 1 gives back the exact Newtonian shell equation and, linearised, the standard growth equation.
Validated against the textbook void shell-crossing pair (delta_L, delta_nl) = (-2.717, -0.7947).

LITERATURE VALUES USED (cited as literature, not fitted here):
  Planck 2018 VI: Omega_m = 0.315, Omega_b = 0.0493, h = 0.674, n_s = 0.965, sigma_8 = 0.811.
  Blumenthal, da Costa, Goldwirth, Lecar & Piran 1992; Sheth & van de Weygaert 2004 MNRAS 350, 517:
    EdS void shell crossing at linear delta_v = -2.717, non-linear delta = -0.7947.
  Sheth & van de Weygaert 2004: void size function carries exp(-delta_v^2 / 2 sigma^2(R_L)).
  Hamaus, Sutter & Wandelt 2014 PRL 112, 251302; Ricciardelli, Quilis & Planelles 2014 MNRAS 440,
    601; Nadathur et al. 2015 MNRAS 449, 3997; Hamaus et al. 2016 JCAP 11, 018: stacked void density
    profiles, central contrast ~ -0.8 in tracer density for large voids.
  Bardeen, Bond, Kaiser & Szalay 1986 + Sugiyama 1995 shape correction: the transfer function.
  Carrick, Turnbull, Lavaux & Hudson 2015 MNRAS 450, 317: the 2M++ reconstructed density field
    (real_research/data/twompp_density.npy, 257^3, Galactic Cartesian Mpc/h, spacing 400/256,
    Local Group at cell [128,128,128], K-band luminosity-weighted bias b = 1.2).  GITIGNORED -- if
    absent the two data-backed parts announce themselves as SKIPPED and register no check.

Checks state measurement and threshold separately; the FAIL is the finding; no literal-True
conditions.  Both a_0 footings throughout."""
import os, sys, json, math, warnings
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

warnings.filterwarnings("ignore")
np.seterr(all="ignore")

G, MPC = 6.674e-11, 3.0857e22
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
OM, OB, HL, NS, S8 = 0.315, 0.0493, 0.674, 0.965, 0.811
OL = 1.0 - OM
H0 = 100.0 * HL * 1e3 / MPC                       # s^-1
RHO_CRIT = 3.0 * H0**2 / (8.0 * math.pi * G)      # kg/m^3
RHO_M = OM * RHO_CRIT
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "real_research", "data")
TWOMPP = os.path.join(DATA, "twompp_density.npy")
CH, OUT = [], {}


def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)


def skip(n, why):
    print(f"  [SKIP] {n}\n           ({why} -- NO check registered, the count below is reduced)", flush=True)


# ---- literature constants, named so they can never be mistaken for a local fit -------------------
DL_SHELLCROSS_EDS = -2.717      # Blumenthal+1992 / Sheth & van de Weygaert 2004
DNL_SHELLCROSS = -0.7947        # the same event, non-linear contrast
B_2MPP = 1.2                    # Carrick+2015 K-band luminosity-weighted galaxy bias
OBS_MEAN_FLOOR = 0.10           # generous floor on residual matter fraction 1+delta_bar, see V5
OBS_MEAN_CEIL = 0.50            # generous ceiling on the same

print(__doc__.split("\n")[0]); print()
print("PRIOR ART IN THIS REPO (stated before anything new is claimed):")
print("    nbody_2026/stage53_route_a_prime_closure_2026.py PART C -- KBC front; C2(ii) already has")
print("      'every rms 12-Mpc void evacuates to delta = -0.993'; C1 ratio 1.175; C3 a_0(z) FLAT")
print("      where the void lives, so constant a_0 is justified to <= 4.5% even from z_i = 1000.")
print("    hunt_2026/k01_acceleration_census.py -- one literature scalar, g_int/a_0 ~ 0.003 at 15 Mpc.")
print("    hunt_2026/h76_h13_h36_h63.py item 63 -- void-vs-wall EFE on rotation curves, different front.")
print("    UNRUN, and done here: the confrontation with the OBSERVED void population.\n")


# =================================================================================================
# kernels, background, linear theory
# =================================================================================================
def nu_RAR(y):
    """the framework's kernel (memory f23: THE_COMPLETION's kernel IS nu_RAR)"""
    return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(y, 1e-300))))


def nu_simple(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt((1.0 + np.sqrt(1.0 + 4.0 / y**2)) / 2.0)


def E(a):   return math.sqrt(OM * a**-3 + OL)             # H/H0
def Om_a(a): return OM * a**-3 / (OM * a**-3 + OL)
def dlnH_dN(a): return -1.5 * Om_a(a)


def growth_D(a):
    """LCDM linear growth factor, normalised D(1) = 1."""
    f = lambda ap: 1.0 / (ap * E(ap))**3
    num = E(a) * quad(f, 1e-8, a, limit=200)[0]
    den = E(1.0) * quad(f, 1e-8, 1.0, limit=200)[0]
    return num / den


# BBKS + Sugiyama shape, normalised to sigma_8 -- the standard CMB-anchored linear amplitude
KGRID = np.logspace(-4.0, 2.0, 6000)                      # h/Mpc
GAM = OM * HL * math.exp(-OB - math.sqrt(2.0 * HL) * OB / OM)
_q = KGRID / GAM
_T = (np.log(1.0 + 2.34 * _q) / (2.34 * _q)) * (1.0 + 3.89 * _q + (16.1 * _q)**2
                                                + (5.46 * _q)**3 + (6.71 * _q)**4)**-0.25
_PK = KGRID**NS * _T**2


def _sig_raw(R):
    x = KGRID * R
    W = 3.0 * (np.sin(x) - x * np.cos(x)) / x**3
    return math.sqrt(np.trapz(_PK * W**2 * KGRID**2, KGRID) / (2.0 * math.pi**2))


_SNORM = S8 / _sig_raw(8.0)
def sigma_L(R_mpch):
    """linear rms top-hat contrast, extrapolated to z = 0 with LCDM growth.  R in Mpc/h."""
    return _SNORM * _sig_raw(R_mpch)


# =================================================================================================
# V1 -- how deep into the MOND regime a void actually sits
# =================================================================================================
print("=" * 112)
print("V1 -- the acceleration census of voids, analytic, across the OBSERVED size range")
print("=" * 112)
print("    g(R) = (4/3) pi G rho_m |delta| R at the edge of a spherical under-density")
print(f"    rho_m = {RHO_M:.4e} kg/m^3 (Planck 2018 Omega_m = {OM}, h = {HL})")

R_OBS = [10.0, 15.0, 20.0, 30.0, 50.0]                    # Mpc/h, the observed void radius range
DELTA_OBS = 0.8                                           # |delta| at the observed void centre
g_of = lambda R_mpch, ad: (4.0 * math.pi / 3.0) * G * RHO_M * ad * (R_mpch / HL) * MPC
print(f"\n    {'R (Mpc/h)':>10s} {'g (m/s^2)':>12s} {'y = g/a0 can':>14s} {'nu can':>8s} "
      f"{'y alt':>10s} {'nu alt':>8s}")
ymax = 0.0
for R in R_OBS:
    g = g_of(R, DELTA_OBS)
    yc, ya = g / A0["canonical"], g / A0["alt"]
    ymax = max(ymax, yc, ya)
    print(f"    {R:10.0f} {g:12.3e} {yc:14.5f} {float(nu_RAR(yc)):8.2f} {ya:10.5f} {float(nu_RAR(ya)):8.2f}")
    OUT[f"v1_g_R{int(R)}"] = float(g); OUT[f"v1_y_can_R{int(R)}"] = float(yc)
    OUT[f"v1_nu_can_R{int(R)}"] = float(nu_RAR(yc)); OUT[f"v1_nu_alt_R{int(R)}"] = float(nu_RAR(ya))
OUT["v1_ymax"] = float(ymax)
SPARC_OUTER_Y = 0.02          # k01_acceleration_census.out: SPARC outermost median g_bar/a_0
nu_sparc = float(nu_RAR(SPARC_OUTER_Y))
print(f"\n    for comparison, the deepest point the RAR is actually measured at: SPARC outermost")
print(f"    median g_bar/a_0 = {SPARC_OUTER_Y} (k01_acceleration_census.out), nu = {nu_sparc:.2f}")
print(f"    NOTE the direction: g grows with R at fixed delta, so the LARGEST voids are the")
print(f"    SHALLOWEST in MOND terms and the smallest voids are the most enhanced.")
check("V1 [EVERY OBSERVED VOID SIZE IS DEEPER IN THE MOND REGIME THAN ANYWHERE THE RAR IS MEASURED] "
      "the edge acceleration of a spherical under-density with the observed central contrast is "
      "computed across the observed radius range on both footings and the largest resulting y = g/a_0 "
      "is compared with the deep-MOND threshold y < 0.1 (nu > 4.1)",
      ymax < 0.1,
      f"the worst case over R = 10-50 Mpc/h and both footings is y = {ymax:.4f}, threshold 0.1; the "
      f"kernel boost runs nu = {OUT['v1_nu_can_R50']:.1f} to {OUT['v1_nu_can_R10']:.1f} (canonical), "
      f"against nu = {nu_sparc:.1f} at the deepest point SPARC reaches. Voids are the maximally-MOND "
      "environment, and this confirms k01's single literature scalar across the whole size range")


# =================================================================================================
# V2 -- the same number, measured on a real reconstructed density field
# =================================================================================================
print("\n" + "=" * 112)
print("V2 -- real local voids: internal accelerations measured on the 2M++ reconstruction")
print("=" * 112)
SP, NG, CEN = 400.0 / 256.0, 257, 128
voids, have_2mpp = [], os.path.exists(TWOMPP)
if not have_2mpp:
    skip("V2 [real voids]", "the 2M++ field is gitignored and absent from this checkout")
else:
    from scipy.ndimage import gaussian_filter
    cube = np.load(TWOMPP)
    print(f"    Carrick+2015 2M++ loaded: {cube.shape}, delta_g in [{cube.min():.2f}, {cube.max():.2f}], "
          f"mean {cube.mean():+.5f}, cell {SP:.4f} Mpc/h")
    print(f"    converting tracer to matter with the paper's own bias b = {B_2MPP}: delta_m = delta_g / b")
    dm = cube / B_2MPP
    ax = (np.arange(NG) - CEN) * SP
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    Rr = np.sqrt(X**2 + Y**2 + Z**2)
    sm = gaussian_filter(dm, sigma=8.0 / SP, mode="nearest")      # 8 Mpc/h, a void-scale filter
    RELIABLE = 120.0                                              # Mpc/h, the trusted reconstruction zone
    cand = np.argsort(np.where(Rr < RELIABLE, sm, 1e9).ravel())
    picked = []
    for idx in cand:
        i, j, k = np.unravel_index(idx, sm.shape)
        p = np.array([ax[i], ax[j], ax[k]])
        if all(np.linalg.norm(p - q) > 25.0 for q in picked):
            picked.append(p)
        if len(picked) >= 12:
            break
    # a coarse copy for the external-field sum (the external field is a large-scale quantity)
    ds = dm[:256, :256, :256].reshape(128, 2, 128, 2, 128, 2).mean(axis=(1, 3, 5))
    axc = (np.arange(128) * 2 + 0.5 - CEN) * SP
    Xc, Yc, Zc = np.meshgrid(axc, axc, axc, indexing="ij")
    DVc = (2 * SP / HL * MPC)**3                                  # coarse cell volume, m^3
    R_PROBE = 15.0
    print(f"\n    {'void':>5s} {'l(deg)':>8s} {'b(deg)':>8s} {'d(Mpc/h)':>9s} {'dbar(<15)':>10s} "
          f"{'g_int/a0':>10s} {'g_ext/a0':>10s} {'ext/int':>8s}")
    for n_, p in enumerate(picked, 1):
        d3 = np.sqrt((X - p[0])**2 + (Y - p[1])**2 + (Z - p[2])**2)
        inside = d3 < R_PROBE
        dbar = float(dm[inside].mean())
        g_int = (4.0 * math.pi / 3.0) * G * RHO_M * abs(dbar) * (R_PROBE / HL) * MPC
        dxc, dyc, dzc = Xc - p[0], Yc - p[1], Zc - p[2]
        rc = np.sqrt(dxc**2 + dyc**2 + dzc**2)
        msk = (rc > R_PROBE) & (rc < 150.0)
        w = G * RHO_M * DVc * ds[msk] / ((rc[msk] / HL * MPC)**3)
        gv = np.array([np.sum(w * dxc[msk] / HL * MPC), np.sum(w * dyc[msk] / HL * MPC),
                       np.sum(w * dzc[msk] / HL * MPC)])
        g_ext = float(np.linalg.norm(gv))
        dd = float(np.linalg.norm(p))
        lo = math.degrees(math.atan2(p[1], p[0])) % 360.0
        ba = math.degrees(math.asin(np.clip(p[2] / max(dd, 1e-9), -1, 1)))
        voids.append(dict(l=lo, b=ba, d=dd, dbar=dbar, g_int=g_int, g_ext=g_ext))
        print(f"    {n_:5d} {lo:8.1f} {ba:8.1f} {dd:9.1f} {dbar:10.3f} "
              f"{g_int/A0['canonical']:10.5f} {g_ext/A0['canonical']:10.5f} {g_ext/max(g_int,1e-30):8.2f}")
    yint = np.array([v["g_int"] for v in voids]) / A0["canonical"]
    yext = np.array([v["g_ext"] for v in voids]) / A0["canonical"]
    OUT["v2_n"] = len(voids)
    OUT["v2_median_dbar"] = float(np.median([v["dbar"] for v in voids]))
    OUT["v2_median_yint_can"] = float(np.median(yint))
    OUT["v2_median_yint_alt"] = float(np.median(np.array([v["g_int"] for v in voids]) / A0["alt"]))
    OUT["v2_median_ratio_ext_int"] = float(np.median(yext / np.maximum(yint, 1e-30)))
    OUT["v2_voids"] = voids
    print(f"\n    medians over {len(voids)} voids: delta_bar(<15 Mpc/h) = {OUT['v2_median_dbar']:+.3f}, "
          f"g_int/a_0 = {OUT['v2_median_yint_can']:.5f} (canonical) / {OUT['v2_median_yint_alt']:.5f} (alt)")
    print(f"    the reconstruction is smoothed at ~4 Mpc/h and linear-theory based, so delta_bar here is")
    print(f"    a LOWER bound on the true depth and g_int correspondingly an UPPER bound -- the true")
    print(f"    voids are deeper in MOND than this measurement says, not shallower")
    check("V2 [REAL LOCAL VOIDS SIT WHERE V1 SAYS THEY DO -- THE CENSUS SCALAR IS CONFIRMED ON DATA] "
          "the mean matter contrast inside 15 Mpc/h of the twelve deepest local under-densities in the "
          "2M++ reconstruction is measured, converted to an internal acceleration, and the median is "
          "compared with the deep-MOND threshold y < 0.1",
          OUT["v2_median_yint_can"] < 0.1 and OUT["v2_median_yint_alt"] < 0.1,
          f"median g_int/a_0 = {OUT['v2_median_yint_can']:.5f} (canonical) / "
          f"{OUT['v2_median_yint_alt']:.5f} (alt) against threshold 0.1, on a median measured contrast "
          f"delta_bar = {OUT['v2_median_dbar']:+.3f}. k01's single scalar 0.003 is confirmed to within a "
          "factor of a few on real data; the external field these voids sit in is carried to V7")


# =================================================================================================
# V3 -- the spherical void integrator, and its two controls
# =================================================================================================
print("\n" + "=" * 112)
print("V3 -- the spherical under-density integrator and its controls")
print("=" * 112)


def evolve(delta_i, R_L_mpch, a0=None, kern=nu_RAR, a_i=1.0/101.0, eds=False,
           a0_of_a=None, y_ext=0.0):
    """integrate the shell equation from a_i to a = 1.  a0 = None -> Newtonian (nu == 1).
    y_ext is a constant external-field term added inside nu (quasi-linear EFE, V7)."""
    R_L = R_L_mpch / HL * MPC                                    # comoving metres
    def Ea(a):  return 1.0 if eds else E(a)
    def Oma(a): return 1.0 if eds else Om_a(a)
    def dlh(a): return -1.5 if eds else dlnH_dN(a)

    def rhs(N, u):
        a = math.exp(N); x, xp = u
        x = max(x, 1e-8)
        s = x**-2 - x
        if a0 is None:
            nu = 1.0
        else:
            a0e = a0 if a0_of_a is None else a0_of_a(a)
            A = 0.5 * Oma(a) * (H0 * Ea(a))**2 * abs(s) * a * R_L
            nu = float(kern(A / a0e + y_ext))
        return [xp, -(2.0 + dlh(a)) * xp - 0.5 * Oma(a) * s * nu]

    f_i = 1.0 if eds else Om_a(a_i)**0.55
    x_i = (1.0 + delta_i)**(-1.0 / 3.0)
    xp_i = -(1.0 / 3.0) * (1.0 + delta_i)**(-4.0 / 3.0) * f_i * delta_i
    sol = solve_ivp(rhs, (math.log(a_i), 0.0), [x_i, xp_i], rtol=1e-10, atol=1e-12,
                    method="DOP853", dense_output=True)
    if not sol.success:
        return float("nan"), float("nan")
    xf = float(sol.y[0, -1])
    # epoch of shell crossing, taken at the standard non-linear contrast
    zsc = float("nan")
    Ns = np.linspace(math.log(a_i), 0.0, 4000)
    dser = sol.sol(Ns)[0]**-3 - 1.0
    hit = np.where(dser <= DNL_SHELLCROSS)[0]
    if len(hit):
        zsc = 1.0 / math.exp(Ns[hit[0]]) - 1.0
    return xf**-3 - 1.0, zsc



def root_dv(RL, a0=None, a_i=1.0/101.0, lo=-0.4, hi=-1e-4):
    """the initial contrast at which a shell reaches the shell-crossing contrast by a = 1.  The kernel
    branch evacuates so fast that a seed of 1e-6 can already be past shell crossing, so the bracket is
    found adaptively: the shallow end is walked toward zero until the shell has NOT yet crossed, the deep
    end toward -1 until it has."""
    f = lambda d: evolve(d, RL, a0=a0, a_i=a_i)[0] - DNL_SHELLCROSS
    fh = f(hi)
    while fh <= 0.0 and hi < -0.5 * SEED_FLOOR:   # walk the shallow end toward zero while it has already crossed
        hi *= 0.1; fh = f(hi)
    if fh <= 0.0:
        # even a seed at SEED_FLOOR has crossed by a = 1: the barrier is not resolvable, only bounded.
        # (Below ~1e-16 the initial shell radius rounds to exactly 1, the peculiar field is exactly zero and
        #  the kernel is singular there, so the floor is kept three decades above that.)
        # Returned value is an UPPER BOUND on |delta_i| and is recorded as such.
        BOUND_HITS.append((RL, a0, hi))
        return hi
    fl = f(lo)
    while fl >= 0.0 and lo > -0.99:
        lo = max(-0.99, 2.0 * lo); fl = f(lo)
    if not (fl < 0.0 < fh):
        return float("nan")
    return brentq(f, lo, hi, xtol=1e-14)
BOUND_HITS = []
SEED_FLOOR = 1e-13                    # the shallowest seed the barrier walk tries (see root_dv)

# control A: EdS must reproduce the textbook shell-crossing pair
A_I = 1.0 / 101.0
di_eds = DL_SHELLCROSS_EDS * (A_I / 1.0)                 # EdS: D propto a, so delta_i = delta_L * a_i
d_eds, _ = evolve(di_eds, 15.0, a0=None, eds=True)
err_eds = abs(d_eds / DNL_SHELLCROSS - 1.0)
OUT["v3_eds_delta"] = float(d_eds); OUT["v3_eds_relerr"] = float(err_eds)
print(f"    control A (EdS): linear delta_L = {DL_SHELLCROSS_EDS} (Blumenthal+1992 / SvdW2004) integrates")
print(f"                     to delta_nl = {d_eds:.5f}; the literature value is {DNL_SHELLCROSS}, "
      f"relative error {err_eds:.2e}")
# control B: a tiny under-density must reproduce LCDM linear growth
D_I, D_0 = growth_D(A_I), growth_D(1.0)
tiny = -1e-5
d_lin, _ = evolve(tiny, 15.0, a0=None)
pred_lin = tiny * D_0 / D_I
err_lin = abs(d_lin / pred_lin - 1.0)
OUT["v3_lin_relerr"] = float(err_lin)
print(f"    control B (LCDM linear): delta_i = {tiny:.0e} at z = 100 integrates to {d_lin:.6e}; linear")
print(f"                     theory with D(1)/D(a_i) = {D_0/D_I:.4f} predicts {pred_lin:.6e}, "
      f"relative error {err_lin:.2e}")
check("V3 [THE INTEGRATOR IS CORRECT] the same code is run in two regimes with a known answer: the "
      "Einstein-de Sitter void shell-crossing pair from the literature, and the linear-growth limit "
      "computed independently by quadrature; both must agree to better than 1 per cent",
      err_eds < 0.01 and err_lin < 0.01,
      f"EdS shell crossing reproduced to {err_eds:.2e} and LCDM linear growth to {err_lin:.2e}, "
      "threshold 1e-2 on each. The Newtonian limit of the kernel branch is therefore the correct "
      "spherical evolution and every comparison below is differential on one verified integrator")


# =================================================================================================
# V4 -- the evacuation differential: same initial condition, Newtonian versus kernel
# =================================================================================================
print("\n" + "=" * 112)
print("V4 -- the evacuation, calibrated so the NEWTONIAN branch lands on the observed void")
print("=" * 112)
print("    method: for each Lagrangian radius, solve for the initial contrast delta_i at z = 100 that")
print("    makes the NEWTONIAN branch reach the observed non-linear contrast -0.7947 at z = 0, then run")
print("    the KERNEL branch from THE SAME delta_i.  Apples to apples; no free parameter is left over.")

R_LAG = [8.0, 12.0, 15.0, 20.0, 30.0]                    # Mpc/h Lagrangian; Eulerian = R_L (1+d)^(-1/3)
calib = {}
for RL in R_LAG:
    di = root_dv(RL, a0=None)
    calib[RL] = di
    OUT[f"v4_delta_i_R{int(RL)}"] = float(di)
print(f"\n    {'R_L':>6s} {'delta_i(z=100)':>15s} {'delta_L0':>10s} | {'branch':>10s} "
      f"{'delta(z=0)':>11s} {'1+delta':>9s} {'z_shellcross':>13s}")
rows_v4 = []
for RL in R_LAG:
    di = calib[RL]
    dN, zN = evolve(di, RL, a0=None)
    print(f"    {RL:6.0f} {di:15.6e} {di*D_0/D_I:10.3f} | {'Newtonian':>10s} {dN:11.5f} "
          f"{1+dN:9.4f} {zN:13.2f}")
    for tag, a0 in A0.items():
        dM, zM = evolve(di, RL, a0=a0)
        ratio = (1.0 + dN) / max(1.0 + dM, 1e-12)
        rows_v4.append(dict(R_L=RL, footing=tag, delta_N=dN, delta_M=dM, ratio=ratio, z_sc=zM))
        OUT[f"v4_deltaM_{tag}_R{int(RL)}"] = float(dM); OUT[f"v4_ratio_{tag}_R{int(RL)}"] = float(ratio)
        OUT[f"v4_zsc_{tag}_R{int(RL)}"] = float(zM)
        print(f"    {'':6s} {'':15s} {'':10s} | {'kernel ' + tag[:3]:>10s} {dM:11.5f} {1+dM:9.4f} "
              f"{zM:13.2f}   residual matter {ratio:.1f}x less than Newtonian")
OUT["v4_rows"] = rows_v4
ratios = [r["ratio"] for r in rows_v4]
OUT["v4_ratio_min"] = float(min(ratios)); OUT["v4_ratio_max"] = float(max(ratios))
print(f"\n    across all radii and both footings the kernel leaves between {min(ratios):.1f}x and "
      f"{max(ratios):.1f}x less residual matter")
print(f"    the kernel branch reaches shell crossing at z = "
      f"{min(r['z_sc'] for r in rows_v4):.1f} to {max(r['z_sc'] for r in rows_v4):.1f}, against "
      f"z = 0 for the Newtonian branch by construction")
check("V4 [THE FRONT HAS TEETH -- THE TWO BRANCHES ARE NOT DEGENERATE] with the initial condition "
      "fixed by the Newtonian branch matching the observed void, the kernel branch is run from the "
      "same initial condition and the residual matter fraction 1+delta is compared; a ratio above 3 "
      "means the prediction is separable from LCDM by any measurement of void emptiness",
      min(ratios) > 3.0,
      f"the kernel leaves {min(ratios):.1f}x to {max(ratios):.1f}x less residual matter than Newtonian "
      f"from an identical initial under-density, and drives shell crossing forward from z = 0 to "
      f"z = {min(r['z_sc'] for r in rows_v4):.1f}-{max(r['z_sc'] for r in rows_v4):.1f}. Against the "
      "threshold 3 this is a large, separable effect -- IN BRANCH (ii) ONLY; branch (i) is Newtonian "
      "by construction and predicts the Newtonian column exactly")


# =================================================================================================
# V5 -- the confrontation with observed void density profiles
# =================================================================================================
print("\n" + "=" * 112)
print("V5 -- confrontation with the observed void density profile")
print("=" * 112)
print("    THE THRESHOLD, STATED SEPARATELY AND BEFORE THE MEASUREMENT.  Stacked void profiles")
print("    (Hamaus+2014 PRL 112 251302; Ricciardelli+2014 MNRAS 440 601; Nadathur+2015 MNRAS 449")
print("    3997; Hamaus+2016 JCAP 11 018) find central TRACER contrast about -0.8 for large voids;")
print("    the MEAN interior matter contrast that corresponds to is shallower than the central value")
print("    and carries tracer-bias and void-finder systematics in both directions.  The envelope")
print(f"    adopted here is deliberately GENEROUS to the framework: residual matter fraction")
print(f"    1+delta_bar between {OBS_MEAN_FLOOR} and {OBS_MEAN_CEIL} (i.e. delta_bar between "
      f"{OBS_MEAN_FLOOR-1:.2f} and {OBS_MEAN_CEIL-1:.2f}).")
print("    A branch is in tension only if it falls BELOW the floor, i.e. empties voids further than")
print("    the most extreme reading of the data allows.")
resid_M = {f"{r['footing']}_R{int(r['R_L'])}": 1.0 + r["delta_M"] for r in rows_v4}
worst_M = max(resid_M.values())                                   # the LEAST-emptied kernel case
best_M = min(resid_M.values())
OUT["v5_resid_kernel_max"] = float(worst_M); OUT["v5_resid_kernel_min"] = float(best_M)
OUT["v5_resid_newtonian"] = float(1.0 + DNL_SHELLCROSS)
print(f"\n    Newtonian branch  : 1+delta_bar = {1+DNL_SHELLCROSS:.4f}  -- inside the envelope BY "
      "CONSTRUCTION (it was calibrated there)")
print(f"    kernel branch (ii): 1+delta_bar = {best_M:.5f} to {worst_M:.5f} across radii and footings")
print(f"    the kernel therefore leaves {(1+DNL_SHELLCROSS)/worst_M:.0f}x to "
      f"{(1+DNL_SHELLCROSS)/best_M:.0f}x less matter in a void than the observations accommodate")
check("V5 [THE KERNEL BRANCH OVER-EMPTIES VOIDS PAST THE MOST GENEROUS READING OF THE DATA] the "
      "residual matter fraction the kernel branch leaves inside a void is compared with a floor set "
      "in advance from the published stacked void profiles and deliberately widened in the "
      "framework's favour; falling below that floor in EVERY case is the tension",
      worst_M < OBS_MEAN_FLOOR,
      f"the least-emptied kernel case over all radii and both footings is 1+delta_bar = {worst_M:.5f}, "
      f"against the generous floor {OBS_MEAN_FLOOR}: a factor {OBS_MEAN_FLOOR/worst_M:.0f} below it, "
      f"and a factor {(1+DNL_SHELLCROSS)/worst_M:.0f} below the calibrated Newtonian value. This "
      "reproduces and generalises stage53 C2(ii)'s single number -0.993 across the observed size "
      "range. IT IS NOT A KILL: see V8, and note the kernel branch is past shell crossing (V4) where "
      "the top-hat is an extrapolation, so the DIRECTION is robust and the VALUE is not")


# =================================================================================================
# V6 -- the void size function: direction and rough magnitude
# =================================================================================================
print("\n" + "=" * 112)
print("V6 -- the void size function: which way, and roughly how much")
print("=" * 112)
print("    Sheth & van de Weygaert 2004 MNRAS 350 517: the void multiplicity carries the factor")
print("    exp(-delta_v^2 / 2 sigma^2(R_L)), delta_v the LINEAR contrast at which the void reaches")
print("    shell crossing.  A kernel that evacuates faster reaches shell crossing from a SHALLOWER")
print("    initial under-density, so |delta_v| falls and the exponential rises: MORE voids, LARGER.")
print("    sigma(R) is BBKS+Sugiyama normalised to sigma_8 = 0.811 -- the CMB-anchored linear")
print("    amplitude, which both branches share at z = 100.")
print(f"\n    {'R_L':>6s} {'sigma_L(R_L)':>13s} {'dv Newton':>11s} {'dv kernel can':>14s} "
      f"{'dv kernel alt':>14s} {'N_M/N_N can':>13s} {'alt':>12s}")
dvN_ref = None
for RL in R_LAG:
    sg = sigma_L(RL)
    dvN_i = root_dv(RL, a0=None)
    dvN = dvN_i * D_0 / D_I
    if dvN_ref is None:
        dvN_ref = dvN
    line = [f"    {RL:6.0f} {sg:13.4f} {dvN:11.3f}"]
    boosts = {}
    for tag, a0 in A0.items():
        dvM_i = root_dv(RL, a0=a0)
        dvM = dvM_i * D_0 / D_I
        boosts[tag] = math.exp((dvN**2 - dvM**2) / (2.0 * sg**2))
        line.append(f"{dvM:14.3f}")
        OUT[f"v6_dv_{tag}_R{int(RL)}"] = float(dvM); OUT[f"v6_boost_{tag}_R{int(RL)}"] = float(boosts[tag])
    OUT[f"v6_dvN_R{int(RL)}"] = float(dvN); OUT[f"v6_sigma_R{int(RL)}"] = float(sg)
    print("".join(line) + f" {boosts['canonical']:13.3e} {boosts['alt']:12.3e}")
dv_ratio = max(abs(OUT[f"v6_dv_{t}_R{int(R)}"]) / abs(OUT[f"v6_dvN_R{int(R)}"])
               for t in A0 for R in R_LAG)
if BOUND_HITS:
    bound_lin = max(abs(hh) for _, _, hh in BOUND_HITS) * D_0 / D_I
    print(f"\n    NOTE: for {len(BOUND_HITS)} kernel-branch cases no seed as shallow as |delta_i| = {SEED_FLOOR:.0e} at z = 100")
    print(f"    avoids shell crossing by z = 0 (the deep-MOND enhancement nu ~ (a_0/g)^(1/2) diverges as the")
    print(f"    peculiar field vanishes), so the kernel barrier |delta_v| is an UPPER BOUND (< {bound_lin:.0e} in linear")
    print(f"    z = 0 units) and the exponential factor N_M/N_N is a LOWER BOUND, not a value.")
    OUT["v6_kernel_barrier_upper_bound_linear"] = float(bound_lin)
print(f"\n    the kernel barrier is shallower than the Newtonian one at every radius and both footings;")
print(f"    the largest ratio |delta_v,kernel| / |delta_v,Newton| is {dv_ratio:.3f}")
print("    THE MAGNITUDE IS NOT A PREDICTION.  The exponential is the LEADING factor only, sigma(R_L)")
print("    enters squared in a denominator, and the SvdW barrier is itself a spherical construction.")
print("    Only the SIGN and the ordering are defensible from this calculation.")
check("V6 [THE SIZE FUNCTION MOVES THE SAME WAY AT EVERY RADIUS: MORE AND LARGER VOIDS] the linear "
      "shell-crossing barrier is computed for both branches on the same integrator and the same "
      "CMB-anchored sigma(R); the kernel barrier must be shallower than the Newtonian barrier at "
      "every radius and both footings for the direction to be a clean prediction rather than a "
      "radius-dependent mixture",
      dv_ratio < 1.0,
      f"the deepest kernel barrier is {dv_ratio:.3f} of the Newtonian one, threshold 1.0 -- shallower "
      f"everywhere. The exponential factor that follows runs "
      f"{min(OUT[f'v6_boost_{t}_R{int(R)}'] for t in A0 for R in R_LAG):.1e} to "
      f"{max(OUT[f'v6_boost_{t}_R{int(R)}'] for t in A0 for R in R_LAG):.1e}, which is quoted as a "
      "DIRECTION with an order of magnitude and must never be quoted as a predicted abundance")


# =================================================================================================
# V7 -- the external field real voids actually sit in
# =================================================================================================
print("\n" + "=" * 112)
print("V7 -- does the external field rescue it?  The one escape a MOND kernel always has")
print("=" * 112)
print("    A void is not isolated.  If the external field of surrounding structure exceeds the void's")
print("    own internal field, the kernel is evaluated at the external value and the internal boost")
print("    collapses.  This is the standard EFE escape and it must be tested, not assumed away.")
if not voids:
    skip("V7 [the EFE quench]", "needs the 2M++ field, which is absent")
else:
    rat = OUT["v2_median_ratio_ext_int"]
    print(f"    measured on the twelve real voids of V2: median g_ext / g_int = {rat:.2f}")
    print(f"    (range {min(v['g_ext']/max(v['g_int'],1e-30) for v in voids):.2f} to "
          f"{max(v['g_ext']/max(v['g_int'],1e-30) for v in voids):.2f})")
    print("    ASSUMPTION, stated: this ratio is held constant over the void's history.  In linear")
    print("    theory both fields scale as a^-1 so the ratio is constant; once the void goes non-linear")
    print("    its own field saturates while the external one keeps growing, so the true late-time")
    print("    ratio is LARGER and the quench applied here is the CONSERVATIVE one.")
    print(f"\n    {'R_L':>6s} {'footing':>10s} {'y_int(z=0)':>11s} {'y_ext used':>11s} "
          f"{'1+delta free':>13s} {'1+delta EFE':>12s}")
    surv = []
    for RL in (12.0, 20.0):
        di = calib[RL]
        for tag, a0 in A0.items():
            g0 = g_of(RL * (1 + DNL_SHELLCROSS)**(-1.0/3.0), abs(DNL_SHELLCROSS))
            yq = rat * g0 / a0
            dF, _ = evolve(di, RL, a0=a0)
            dE, _ = evolve(di, RL, a0=a0, y_ext=yq)
            surv.append(1.0 + dE)
            OUT[f"v7_resid_efe_{tag}_R{int(RL)}"] = float(1.0 + dE)
            print(f"    {RL:6.0f} {tag:>10s} {g0/a0:11.5f} {yq:11.5f} {1+dF:13.5f} {1+dE:12.5f}")
    OUT["v7_resid_efe_max"] = float(max(surv))
    print(f"\n    the EFE quench raises the residual matter fraction to at most {max(surv):.5f}, still "
          f"a factor {OBS_MEAN_FLOOR/max(surv):.0f} below the generous floor {OBS_MEAN_FLOOR}")
    check("V7 [THE EXTERNAL FIELD DOES NOT RESCUE THE OVER-EMPTYING] the external-to-internal field "
          "ratio measured on real local voids is fed back into the kernel as a quasi-linear "
          "external-field term and the evacuation re-run; the over-emptying survives only if the "
          "residual matter fraction stays below the same floor used in V5",
          max(surv) < OBS_MEAN_FLOOR,
          f"with the measured median quench g_ext/g_int = {rat:.2f} applied throughout, the largest "
          f"residual fraction reached is {max(surv):.5f} against the floor {OBS_MEAN_FLOOR}. The "
          "external field real voids sit in is far too weak to switch the kernel off, because the "
          "void's own field and its surroundings' field are BOTH far below a_0 -- which is the whole "
          "point of the environment. The EFE escape that rescues wide binaries and dwarf satellites "
          "is not available here")


# =================================================================================================
# V8 -- the honest limitation, quantified
# =================================================================================================
print("\n" + "=" * 112)
print("V8 -- what this calculation cannot decide, quantified rather than asserted")
print("=" * 112)
print("    STATED PROMINENTLY.  (1) A spherical top-hat is a crude model of a void: real voids are")
print("    aspherical, contain substructure, and the kernel branch is PAST SHELL CROSSING for most of")
print("    its evolution (V4), where the top-hat is an extrapolation and not a solution.  (2) Void")
print("    statistics depend strongly on the tracer and on the void-finder definition: watershed,")
print("    spherical-underdensity and ZOBOV/VIDE finders return different central contrasts on the")
print("    same field, and tracer bias converts between galaxy and matter contrast with an uncertainty")
print("    that is itself density dependent.  NO KILL IS CLAIMED FROM A SPHERICAL MODEL.")
print("    (3) The governing fork: the framework's OWN covariant cosmology has linear enhancement")
print("    EXACTLY 1 (stage53 C2(i), item 85), in which case the Newtonian column IS the framework's")
print("    prediction and this entire front is empty.\n")
print("    what IS testable here is how far the branch-(ii) answer moves under the modelling choices")
print("    that are actually free:")
variants = {}
for RL in (12.0, 20.0):
    di = calib[RL]
    for tag, a0 in A0.items():
        variants[f"nu_RAR {tag} R{int(RL)}"] = 1.0 + evolve(di, RL, a0=a0)[0]
        variants[f"nu_simple {tag} R{int(RL)}"] = 1.0 + evolve(di, RL, a0=a0, kern=nu_simple)[0]
        variants[f"a0~H(z) rival {tag} R{int(RL)}"] = 1.0 + evolve(
            di, RL, a0=a0, a0_of_a=lambda a, _a0=a0: _a0 * E(a))[0]
    variants[f"z_i = 30 canonical R{int(RL)}"] = 1.0 + evolve(
        root_dv(RL, a0=None, a_i=1/31.),
        RL, a0=A0["canonical"], a_i=1/31.)[0]
for k_, v_ in sorted(variants.items(), key=lambda t: -t[1]):
    print(f"      {k_:32s} 1+delta_bar = {v_:.5f}")
OUT["v8_variants"] = {k_: float(v_) for k_, v_ in variants.items()}
spread_hi = max(variants.values())
OUT["v8_spread_hi"] = float(spread_hi); OUT["v8_spread_lo"] = float(min(variants.values()))
print(f"\n    the whole spread is {min(variants.values()):.5f} to {spread_hi:.5f}; the floor is "
      f"{OBS_MEAN_FLOOR}")
check("V8 [THE DIRECTION SURVIVES EVERY MODELLING CHOICE THAT IS ACTUALLY FREE, WHICH IS NOT THE "
      "SAME AS SURVIVING THE MODEL] both kernels, both footings, two Lagrangian radii, two starting "
      "redshifts and the rival a_0 proportional to H(z) branch are run and the full spread of the "
      "residual matter fraction is compared with the same floor; the direction is robust only if the "
      "entire spread stays on one side of it",
      spread_hi < OBS_MEAN_FLOOR,
      f"the whole spread {min(variants.values()):.5f} to {spread_hi:.5f} lies below the floor "
      f"{OBS_MEAN_FLOOR}, so no choice among kernel, footing, radius, starting redshift or a_0(z) "
      "branch reverses the sign. The rival a_0 proportional to H(z) branch makes the over-emptying "
      "WORSE, not better, because a larger a_0 at early times pushes the void DEEPER into the MOND "
      "regime. What this does NOT establish is that the spherical model itself is adequate, and that "
      "is the limitation that actually binds")

print("\n" + "=" * 112)
print("WHAT THIS FRONT IS WORTH")
print("=" * 112)
print("    Branch (ii) 'MOND-on' makes a large, sign-definite, environment-proof prediction: voids")
print("    empty to a residual matter fraction of order 1e-2 or less, reach shell crossing at")
print(f"    z ~ {max(r['z_sc'] for r in rows_v4):.0f}, and the size function is pushed to more and larger voids.  That is")
print("    in the wrong direction against every published void profile, and V7 shows the external")
print("    field cannot switch it off.  But branch (ii) was ALREADY excluded in this repo on the")
print("    KBC amplitude and on sigma_8 -> 1.38 (stage53 C2), so this is an INDEPENDENT CONFIRMATION")
print("    of a known failure, not a new kill.")
print("    Branch (i), the framework's own covariant cosmology, has linear enhancement exactly 1 and")
print("    therefore predicts the Newtonian column -- no void signal at all.")
print("    NET: cosmic voids are NOT a live discriminating front for this framework as it stands.")
print("    They become one only if a covariant completion is found whose cosmological perturbations")
print("    carry a MOND enhancement, and then voids would be among the sharpest tests available,")
print("    because V7 shows the usual external-field escape is closed there.")

json.dump(OUT, open(os.path.join(HERE, "L250_results.json"), "w"), indent=1)
print(f"\nL250 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
sys.exit(0 if all(CH) else 1)
