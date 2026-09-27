#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP11 -- THE LOCAL GROUP ON THE UNSCORED BRANCH: a past Milky Way--M31 flyby, tested in the chain's own two-body law.

WHY.  The Local Group (LG) is the chain's most persistent failure: FP9's (H_Y) gives R0 = 1.41 / 1.45 Mpc against the measured
0.96 +- 0.03 (FP1's ungated core 1.93 / 2.02); XR13's per-object door gives 1.34-1.55 Mpc and an own-orbit timing of -6.9 to
+48.7 km/s against the measured -110 km/s; and the KiDS-LG pincer (FP1 E3) says the LG needs ~3e-3 a0 in nu's argument where
KiDS tolerates <= 2.3e-4 (5.2e-4 with a 2-halo).  One branch was never scored: in MOND the MW--M31 attraction is stronger and
the literature (Zhao et al. 2013, A&A 557, L3; Banik & Zhao 2018, MNRAS 473, 4033) argues for a past close flyby ~7-11 Gyr
ago, with the pair now on its second approach and the flyby flinging dwarfs outward ("high-velocity galaxies").  This lane
integrates that branch IN THE CHAIN'S OWN LAW, both a0 footings, and scores it: the orbit family, whether a flyby is
required / allowed / excluded, the test-particle dwarfs' zero-velocity radius and Hubble flow, the pincer, the other gates.

THE LAW (nothing added to the action).  FP7's AQUAL-type root with FP9's separator (H_Y): J_Y = J_P2(Y) + 2 y_th sqrt(Y) on
phi, chi = (S_xi - S_L) phi, L = L_Lambda Omega_L^(n/2) (L_Lambda = 2.46 Mpc, n = 2), y_th = y_Lambda Omega_L^-p'
(y_Lambda = 7.78e-8, p' = 4) -- FP9's four declared constants, unchanged.  Its static law in QUMOND form (FP9 K3: the band-
passed spherical AQUAL law IS FP6's band-passed phantom; FP7 A3: AQUAL vs QUMOND <= 0.035 dex on discs):
    g = g_N + P (1 - S_L) X(g_bp),   g_bp = (1 - S_L) g_N,   X(g) = a0 x_P2(|g|/a0 - y_th) g/|g|,   x_P2(D) = sqrt(D^2 + D) - D,
P the curl-free projection, S_L the Gaussian heat filter (sigma = L), xi -> 0.  For TWO point masses this lane derives the
mutual force from it exactly: each body feels the other's Newtonian field, the other's ISOLATED band-passed phantom (FP6's
committed phantom(), exact), and the INTERACTION field P(1 - S_L) W, W = X(g_bp,1 + g_bp,2) - X(g_bp,1) - X(g_bp,2) (the
non-linear MOND superposition), evaluated by a direct dipole-kernel integral centred on the body (band-passed kernel closed
form; axisymmetry makes it 2-D).  Controls: the kernel reproduces FP6's isolated phantom; momentum is conserved; the deep-MOND
limit is Milgrom's two-body force (2/3) sqrt(G a0) [(m1+m2)^(3/2) - m1^(3/2) - m2^(3/2)]/d (the virial theorem of the scale-
invariant deep-MOND equation, which AQUAL and QUMOND share); the test-particle limit is the P2 law.  For the dwarfs the same
interaction field is solved on a polar grid by Legendre multipoles (finite-volume divergence, the band-pass as its exact
multipole kernel, Poisson recursion), checked against the direct integral at the bodies.
Dynamical friction: ZERO (the galaxy sector has no halos; the H_Y orbit turns out to have no past pericentre at all, so no
friction question arises in its past).  Masses: MW stars 6.08 +- 1.14e10 (Licquia & Newman 2015), M31 stars
10.3 (+2.3/-1.7)e10 (Sick et al. 2015; Tamm et al. 2012: 1.0-1.5e11), HI x 1.33 from the committed UNGC (Karachentsev+2013,
real_research/data/ungc_karachentsev2013.tsv): nominal M_b = 1.75e11, MW share 0.37; window [1.145e11 (the chain's committed
LG value, k02/XR4/FP9), 2.4e11].  Separation 0.78 Mpc, v_r = -109.3 +- 4.4 km/s (van der Marel+2012), v_t = 17 (vdM+2012,
<= 34 at 1 sigma), 57 (+35/-31; vdM+2019, Gaia DR2) and 82.4 +- 31.2 km/s (Salomon+2021, Gaia EDR3) -- all checked at the
source for this lane; R0 = 0.96 +- 0.03 Mpc (Karachentsev+2009, MNRAS 393, 1265; 30 galaxies at 0.7-3 Mpc).
CONVENTIONS (the timing argument's idealisation, stated): A = the chain's (XR4/XR13/FP9): point masses + Lambda, the pair and
the dwarfs start on the Hubble flow at a = 0.02 (radial timing, J = 0); B = A + the smooth cosmic background's deceleration
(the (a''/a) r term of Zhao+2013's eq. 2); C = A + XR4's Newtonian carrier histories (decay / full; a variant only: the
galaxy sector has no halos).  Pericentre distances need J: 2-D orbits with J = 0.78 Mpc x v_t integrated from today.

CHECKS
  K1 CONTROL: FP9's LG R0 at the (H_Y) headline cell, with FP6's committed machinery and FP9's yield hook: 1.4104 / 1.4532.
  K2 CONTROL: hunt item 13's radial timing (XR13 C3: -222.5 / -241.5 km/s) with its own scheme; this lane's Hubble-flow shooter
     with the same test-particle law agrees within 1.5 km/s (the two start conventions agree).
  K3 CONTROL (the two-body integral): (a) on W = V_B,iso it reproduces FP6's output-filtered isolated phantom (4 cells, incl.
     band-pass + yield); (b) momentum m1 a1 = m2 a2; (c) the deep limit -> Milgrom's two-body formula, deviation falling as
     r_M/d; (d) the test-particle limit -> 1 - (2/3) sqrt(m2/m1).
  K4 CONTROL: the multipole interaction field at the bodies equals the direct on-axis integral (<= 1%).
  K5 CONTROL: the tracer machinery with the pair merged reproduces FP9's (H_Y) R0 and FP1's plain-P2 R0 (1.9246 / 2.0179).
  K6 CONTROL (literature, verified at the source): Zhao+2013's own law, masses and K-term give their encounter (Table 1 line 1:
     7.0 Gyr ago; b = 22-48 kpc for v_t = 17-34 km/s); through this lane's strict-timing shooter (convention B) their law meets
     -109.3 km/s on the flyby branch at a mass inside their Table 1 range.
  K7 CONTROL: FP9's headline flagship / SPARC / KiDS numbers reproduced exactly with FP9's constants (the ones used here).
  T1 [load-bearing; MUTATE must fail] THE CHAIN'S LAW NEEDS NO FLYBY: on (H_Y) the first-approach branch reaches -109.3 +- 4.4
     km/s at a baryonic mass inside the window on BOTH footings (convention A).
  T2 THE CHAIN'S LAW EXCLUDES A PAST FLYBY: no approaching branch with a past pericentre at 0.78 Mpc for M_b <= 1e12, either
     footing, conventions A and B.
  T3 (reported) the timing mass under B and C; T4 THE PLAIN ROOT LAW (no separator) HAS NO TIMING SOLUTION IN THE WINDOW: its
     first approach is too fast there and its flyby branch needs a mass above it; T5 (reported) numerical / idealisation sensitivity.
  O1 / O2 (reported) 2-D orbits with v_t = 17 / 57 / 82 km/s: (H_Y) no close encounter since birth (last apocentre, future
     first pericentre); the plain law's flyby epoch and pericentre at its timing mass.
  R1 THE TIMING-MATCHED LOCAL GROUP STILL OVERSHOOTS R0 (two-body dwarfs, both footings, conventions A and B) -- a verified FAIL.
  R2 (reported) the two-body geometry vs the merged pair; the anisotropy.   R3 THE FLYBY DOES NOT RESCUE R0 (in the only law with a
     matched flyby, the plain root law at its own timing mass).   R4 (reported) the Hubble diagram vs the UNGC (same estimator), the HVGs.
  P1 THE PINCER AT THE TIMING MASS: the external field the LG would need in the kernel vs KiDS's tolerance; the band-pass passes
     no uniform field.   X1 (reported) the LG alone, timing imposed: which band-pass length L(0.25) would give R0 in the band at a
     baryonic timing mass (KiDS's floor is ~1.2 Mpc).   G1 THE OTHER GATES ARE UNCHANGED.   W the ledger.
MUTATE=1 removes the separator (band-pass + yield) from the SCORED two-body law (the plain P2 root law is scored in T1): its first
approach is too fast at every mass in the window, so T1 must FAIL (rc = 1).  Outputs: *_MUTATE.out / *_results_MUTATE.json.

SCOPE.  Point-mass galaxies (Newton softened at 10 kpc); radial timing (J = 0) for masses and branches, J > 0 from today for
pericentres; the dwarfs are axisymmetric about the pair axis (exact for the J = 0 orbit); no neighbouring groups (M81, Cen A,
IC 342) and no external tidal field; the interaction field in QUMOND form (the AQUAL curl difference is not computed); no
particle-mesh run (at most 2 workers, each run < 30 min).
Run from the repository root:  python3 real_research/derivation_chain_2026/FP11_local_group_flyby.py   (MUTATE=1 for the control)
"""
import os, sys, io, json, math, time, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from scipy.special import erf, ive, eval_legendre
from scipy.integrate import solve_ivp, quad
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
import hunt_lib as HL                                                            # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP11_local_group_flyby"
NPROC = 2


# ================================================================================================= the chain's machinery
def load_fp6():
    """FP9's loader, verbatim in effect: exec FP6's committed script up to its CONTROLS banner (constants, kernels, the band-
    passed phantom, KiDS lead grade, the LG shell model) in a private namespace; nothing is edited, its prints are captured."""
    p = os.path.join(HERE, "FP6_gate_survey.py"); src = open(p).read(); cut = src.index('banner("K  CONTROLS')
    ns = {"__file__": p, "__name__": "fp6_machinery"}
    old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:cut], p, "exec"), ns)
    finally:
        if old is None: os.environ.pop("MUTATE", None)
        else: os.environ["MUTATE"] = old
    ns["BANDPASS"] = True
    return ns


M6 = load_fp6()
YIELD = -1                                                                       # FP9's 'm' slot value for the yield law
_cut6 = M6["cutfac"]
nu_p2 = M6["nu_p2"]


def x_P2(D):
    """P2's scalar field for a Newtonian field D (units a0): mu_s(x) x = D, mu_s = x/(1 - 2x) (FP9's closed form)."""
    D = np.maximum(np.asarray(D, float), 0.0)
    return np.where(D > 0, 1.0 / (1.0 + np.sqrt(1.0 + 1.0 / np.maximum(D, 1e-300))), 0.0)


def cut_hook(y, yth, m):                                                         # FP9's hook, verbatim in effect
    if m == YIELD:
        if yth is None or yth <= 0:
            return np.ones_like(np.asarray(y, float))
        y = np.maximum(np.asarray(y, float), 1e-300)
        return x_P2(y - yth) / y / (nu_p2(y) - 1.0)
    return _cut6(y, yth, m)


M6["cutfac"] = cut_hook
_fp0 = json.load(open(os.path.join(HERE, "FP0_core_postulates_results.json")))["numbers"]
A0 = {"canonical": _fp0["a0_canonical"], "alt": _fp0["a0_rho_total"]}
FOOTS = ("canonical", "alt")
G = 6.6743e-11; MSUN = 1.98892e30; MPC = 3.0857e22; KPC = MPC / 1e3; GYR = 3.15576e16
RG, phantom = M6["RG"], M6["phantom"]
LG_H0, LG_OM, LG_OL, LG_OmL = M6["LG_H0"], M6["LG_OM"], M6["LG_OL"], M6["LG_OmL"]
L_OL_H02 = LG_OL * LG_H0 ** 2
HEAD = dict(n=2.0, L25=1.3, pp=4.0, y25=1e-6)                                   # FP9's (H_Y) headline cell
L_LAMBDA = HEAD["L25"] / M6["OmL_z"](0.25) ** (HEAD["n"] / 2.0)                  # FP9's LL_of(1.3, 2) = 2.46 Mpc
Y_LAMBDA = HEAD["y25"] * M6["OmL_z"](0.25) ** HEAD["pp"]
EPS = 10 * KPC                                                                   # Newtonian softening (galaxy size)
RATIO_D = 5.36                                                                   # XR4's carrier/baryon ratio (variant C)

# observables (each checked at its source for this lane)
D0_LG, VR_LG, EVR_LG = 0.78, -109.3, 4.4                                         # vdM+2012 (item 13 / XR13 used 0.78, -110)
VT_SET = (17.0, 57.0, 82.4)                                                      # vdM+2012, vdM+2019 (DR2), Salomon+2021 (EDR3)
R0_MEAS, R0_ERR, BAND = 0.96, 0.03, 0.10                                         # Karachentsev+2009; XR4's +-0.10 dex band
MW_STARS, M31_STARS = 6.08e10, 10.3e10                                           # Licquia & Newman 2015; Sick+2015
MW_STARS_E, M31_STARS_EP, M31_STARS_EM = 1.14e10, 2.3e10, 1.7e10
MB_LO, MB_HI = 1.145e11, 2.4e11                                                  # the window: the chain's committed LG value .. Tamm+2012 upper


def L_of_a(a, bp=True, LL=None):
    """FP9's band-pass length on the LG's leaf (FP6's lg_both: L_Lambda Omega_L(a)^(n/2)) [m]; LL overrides L_Lambda [Mpc] (X1 only)."""
    return (L_LAMBDA if LL is None else LL) * LG_OmL(a) ** (HEAD["n"] / 2.0) * MPC if bp else None


def yth_of_a(a, yl=True):
    """FP9's running yield (FP6's lg_both form): y_th(0.25) (Omega_L(0.25)/Omega_L(a))^p'."""
    return HEAD["y25"] * (LG_OmL(1 / 1.25) / LG_OmL(a)) ** HEAD["pp"] if yl else None


def t_of_a(a):
    return 2.0 / (3.0 * LG_H0 * math.sqrt(LG_OL)) * math.asinh(math.sqrt(LG_OL / LG_OM) * a ** 1.5)


_AG = np.geomspace(1e-4, 3.0, 20000); _TG = np.array([t_of_a(a) for a in _AG]); T0_AGE = t_of_a(1.0)


def lna_of_t(t):
    return math.log(float(np.interp(t, _TG, _AG)))


# ================================================================================================= the two-body law
def gfrac(u):
    return erf(u / math.sqrt(2)) - math.sqrt(2 / math.pi) * u * np.exp(-u * u / 2)


def Efac(r, L):
    """(1 - S_L) of a point mass: the fraction of its (unit) charge outside r after subtracting the Gaussian cloud."""
    if L is None:
        return np.ones_like(np.asarray(r, float))
    return 1.0 - gfrac(r / L)


def Xfield(gx, gz, a0, yth):
    """raw phantom X(g) = a0 x_P2(|g|/a0 - y_th) g/|g| (meridional components); zero below the yield."""
    gm = np.hypot(gx, gz)
    x = x_P2(gm / a0 - (yth or 0.0))
    f = np.where(gm > 0, a0 * x / np.maximum(gm, 1e-300), 0.0)
    return f * gx, f * gz


XG, WG = np.polynomial.legendre.leggauss(128)


def dg_body(mA, mB, d, a0, L, yth, ns=200, smin_fac=1e-4, control_W=None):
    """the interaction field P(1 - S_L) W at body A (origin), body B at z = -d: signed z component [m/s^2] (negative = toward
    B).  Spherical grid about A: g_z = (1/3) W_z(A) - (1/2) Int ds/s Int dmu [(2E + sqrt(2/pi) u^3 e^{-u^2/2}) mu W_s + E sqrt(1-mu^2)
    W_alpha], u = s/L, E = 1 - gfrac(u) (the closed-form band-passed dipole kernel; L = None: E = 1, no u^3 term).
    control_W = 'Biso' integrates W = X(g_bp,B) instead (the kernel control K3a)."""
    smax = (1e4 * d) if L is None else max(60 * L, 60 * d)
    s = np.geomspace(smin_fac * d, smax, ns)
    S = s[:, None]; MU = XG[None, :]; SA = np.sqrt(1 - MU ** 2)
    xx = S * SA; zz = S * MU
    rA = S * np.ones_like(MU); rB = np.sqrt(xx ** 2 + (zz + d) ** 2)
    EA, EB = Efac(rA, L), Efac(rB, L)
    gAx, gAz = -G * mA * EA * xx / rA ** 3, -G * mA * EA * zz / rA ** 3
    gBx, gBz = -G * mB * EB * xx / rB ** 3, -G * mB * EB * (zz + d) / rB ** 3
    gBd = -G * mB * float(Efac(np.array([d]), L)[0]) / d ** 2
    VBA = float(Xfield(np.array([0.0]), np.array([gBd]), a0, yth)[1][0])       # V_B,iso at A (z component)
    if control_W == "Biso":
        Wx, Wz = Xfield(gBx, gBz, a0, yth); WAz = VBA
    else:
        Vx, Vz = Xfield(gAx + gBx, gAz + gBz, a0, yth)
        VAx, VAz = Xfield(gAx, gAz, a0, yth); VBx, VBz = Xfield(gBx, gBz, a0, yth)
        Wx, Wz = Vx - VAx - VBx, Vz - VAz - VBz; WAz = -VBA                     # (V - V_A,iso) -> 0 at A
    Ws = Wx * SA + Wz * MU; Wal = Wx * MU - Wz * SA
    if L is None:
        k1, k2 = 2.0, 1.0
    else:
        u = S / L; E = Efac(S, L)
        k1 = 2 * E + math.sqrt(2 / math.pi) * u ** 3 * np.exp(-u * u / 2); k2 = E
    ang = ((k1 * MU * Ws + k2 * SA * Wal) * WG[None, :]).sum(axis=1)
    return WAz / 3.0 - 0.5 * np.trapz(ang, np.log(s))


def g_iso(m_kg, a0, L, yth, r):
    """FP6's output-filtered isolated phantom field at r (toward the body)."""
    Mph = phantom(m_kg, a0, L, yth, YIELD if yth else 4)
    return G * np.interp(r, RG, Mph) / r ** 2


DGRID = np.geomspace(2 * KPC, 8 * MPC, 64)
LNAT = np.linspace(math.log(0.02), 0.0, 49)


def force_table(m1, m2, a0, bp=True, yl=True, dgrid=None, lna=None, LL=None):
    """relative attraction a_rel(d, ln a) of the pair [m/s^2]: Newton (unsoftened here) + the isolated phantoms of each at the
    other + the interaction fields at both bodies.  Without a separator the law is epoch-independent (one row, tiled)."""
    dgrid = DGRID if dgrid is None else dgrid; lna = LNAT if lna is None else lna
    T = np.zeros((len(lna), len(dgrid)))
    rows = range(len(lna)) if (bp or yl) else [len(lna) - 1]
    for j in rows:
        a = math.exp(lna[j]); L = L_of_a(a, bp, LL); yt = yth_of_a(a, yl)
        M1 = phantom(m1, a0, L, yt, YIELD if yt else 4); M2 = phantom(m2, a0, L, yt, YIELD if yt else 4)
        gM1 = G * np.interp(dgrid, RG, M1) / dgrid ** 2; gM2 = G * np.interp(dgrid, RG, M2) / dgrid ** 2
        for k, d in enumerate(dgrid):
            T[j, k] = G * (m1 + m2) / d ** 2 + gM2[k] + gM1[k] - dg_body(m1, m2, d, a0, L, yt) - dg_body(m2, m1, d, a0, L, yt)
    if not (bp or yl):
        T[:] = T[-1]
    return dgrid, lna, T


def retained(z, hist):
    if hist == "none": return 0.0
    if hist == "full": return 1.0
    return float(np.interp(z, [0.0, 0.5, 1.0, 2.5, 100.0], [0.075, 0.645, 0.92, 0.998, 0.998]))   # XR4's decay history


class Acc:
    """a_rel(d, ln a): the MOND part bilinear in (ln a, ln d) from the table (as T_M d^2); Newton softened (EPS); optional
    Newtonian carrier 5.36 M_b retained(z) (variant C)."""
    def __init__(self, dg, lna, T, M_kg, soft=EPS, hist="none"):
        self.ld = np.log(dg); self.lna = lna; self.M = M_kg; self.soft = soft; self.hist = hist
        self.TM = (T - G * M_kg / dg[None, :] ** 2) * dg[None, :] ** 2; self.d0 = dg[0]

    def mond(self, l, d):
        j = (l - self.lna[0]) / (self.lna[1] - self.lna[0]); j0 = int(min(max(math.floor(j), 0), len(self.lna) - 2))
        fj = min(max(j - j0, 0.0), 1.0); row = (1 - fj) * self.TM[j0] + fj * self.TM[j0 + 1]
        dd = np.maximum(d, self.d0); m = np.interp(np.log(dd), self.ld, row) / dd ** 2
        return np.where(d < self.d0, m * d / self.d0, m)

    def __call__(self, l, d):
        newt = G * self.M * d / (d ** 2 + self.soft ** 2) ** 1.5
        if self.hist != "none":
            newt = newt * (1.0 + RATIO_D * retained(1.0 / math.exp(l) - 1.0, self.hist))
        return newt + self.mond(l, d)


def acc_testparticle(M_kg, a0):
    """XR13 / item 13's 'M*': the pair as a test particle in the merged mass's field, nu_RAR (hunt_lib), Newton softened."""
    def f(l, d):
        gN = G * M_kg * d / (d ** 2 + EPS ** 2) ** 1.5
        return HL.nu(gN / a0) * gN
    return f


def shoot(acc, ri, nstep=8000, a_start=0.02, bg=False, store=False):
    """radial (J = 0) signed 1-D relative orbits from the Hubble flow at a_start (XR4's convention; bg adds the smooth
    background's -(Om/2) H0^2 a^-3 x); returns x, u today and the pericentre-passage count (sign changes of x)."""
    x = ri.copy(); u = LG_H0 * math.sqrt(LG_OM / a_start ** 3 + LG_OL) * x
    lna = np.linspace(math.log(a_start), 0.0, nstep + 1); h = lna[1] - lna[0]
    nc = np.zeros_like(x, dtype=int); X = [x.copy()] if store else None

    def f(l, xx, uu):
        a = math.exp(l); H = LG_H0 * math.sqrt(LG_OM / a ** 3 + LG_OL)
        ac = -acc(l, np.abs(xx)) * np.sign(xx) + L_OL_H02 * xx
        if bg: ac = ac - 0.5 * LG_OM * LG_H0 ** 2 / a ** 3 * xx
        return uu / H, ac / H
    for i in range(nstep):
        l = lna[i]
        k1x, k1u = f(l, x, u); k2x, k2u = f(l + h / 2, x + h * k1x / 2, u + h * k1u / 2)
        k3x, k3u = f(l + h / 2, x + h * k2x / 2, u + h * k2u / 2); k4x, k4u = f(l + h, x + h * k3x, u + h * k3u)
        xn = x + h * (k1x + 2 * k2x + 2 * k3x + k4x) / 6; u = u + h * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
        nc += (np.sign(xn) != np.sign(x)).astype(int); x = xn
        if store: X.append(x.copy())
    if store: return x, u, nc, lna, np.array(X)
    return x, u, nc


def branches(acc, D0=D0_LG * MPC, lo=0.05, hi=600.0, n=300, bg=False, nstep=8000, a_start=0.02, nref=24, nsec=7):
    """every (k, v_r) solution at separation D0 today: coarse r_i grid, a fine grid inside each interval where the pericentre
    count changes (an approach branch starts there at d = 0), same-count brackets of d = D0, refined by 8-point sections."""
    sh = lambda r_: shoot(acc, r_, nstep=nstep, bg=bg, a_start=a_start)
    ri = np.geomspace(lo * KPC, hi * KPC, n); x, u, nc = sh(ri)
    bnd = [i for i in range(n - 1) if nc[i] != nc[i + 1]]
    if bnd:
        extra = np.concatenate([np.geomspace(ri[i], ri[i + 1], nref + 2)[1:-1] for i in bnd]); xe, ue, nce = sh(extra)
        ri = np.concatenate([ri, extra]); x = np.concatenate([x, xe]); u = np.concatenate([u, ue]); nc = np.concatenate([nc, nce])
        o = np.argsort(ri); ri, x, u, nc = ri[o], x[o], u[o], nc[o]
    d = np.abs(x)
    br = [(ri[i], ri[i + 1], nc[i]) for i in range(len(ri) - 1) if nc[i] == nc[i + 1] and (d[i] - D0) * (d[i + 1] - D0) < 0]
    if not br:
        return []
    A = np.array([b_[0] for b_ in br]); B = np.array([b_[1] for b_ in br]); K = np.array([b_[2] for b_ in br]); live = np.ones(len(br), bool)
    for _ in range(nsec):                                                       # all brackets refined together (10-point sections)
        g_ = np.array([np.geomspace(A[q], B[q], 10) for q in range(len(br))]); xg, ug, kg = sh(g_.ravel())
        dgv = (np.abs(xg) - D0).reshape(g_.shape); kg = kg.reshape(g_.shape)
        for q in range(len(br)):
            hit = [j for j in range(9) if kg[q, j] == K[q] and kg[q, j + 1] == K[q] and dgv[q, j] * dgv[q, j + 1] <= 0]
            if hit and live[q]:
                A[q], B[q] = g_[q, hit[0]], g_[q, hit[0] + 1]
            else:
                live[q] = False
    xm, um, km = sh(np.sqrt(A * B))
    return [dict(k=int(km[q]), ri_kpc=float(math.sqrt(A[q] * B[q]) / KPC), d=float(abs(xm[q]) / MPC), vr=float(np.sign(xm[q]) * um[q] / 1e3))
            for q in range(len(br))]


def orbit2d(acc, vt_kms, t_end, bg=False, vr_kms=VR_LG, rtol=1e-10):
    """planar relative orbit from today's state (D0 along x, v_r, v_t), to t_end (backward if < t0); the z = 0 law is kept for
    t > t0 (the band-pass and the yield change little in the next few Gyr: Omega_L 0.69 -> 0.83).  Returns the extrema."""
    def rhs(t, y):
        x, yy, vx, vy = y; r = math.hypot(x, yy); l = lna_of_t(t); a = math.exp(l)
        ar = float(acc(min(l, 0.0), np.array([r]))[0])
        ax = -ar * x / r + L_OL_H02 * x; ay = -ar * yy / r + L_OL_H02 * yy
        if bg:
            k = 0.5 * LG_OM * LG_H0 ** 2 / a ** 3; ax -= k * x; ay -= k * yy
        return [vx, vy, ax, ay]
    ev = lambda t, y: y[0] * y[2] + y[1] * y[3]
    sol = solve_ivp(rhs, (T0_AGE, t_end), [D0_LG * MPC, 0.0, vr_kms * 1e3, vt_kms * 1e3], method="DOP853", rtol=rtol, atol=1e-3,
                    events=ev, dense_output=True, max_step=0.02 * GYR)
    ext = []
    for te, ye in zip(sol.t_events[0], sol.y_events[0]):
        r = math.hypot(ye[0], ye[1]); dt = 1e-4 * GYR
        r1 = math.hypot(*sol.sol(te - dt)[:2]); r2 = math.hypot(*sol.sol(te + dt)[:2])
        kind = "peri" if (r1 > r and r2 > r) else ("apo" if (r1 < r and r2 < r) else "flat")
        ext.append(dict(kind=kind, lookback_Gyr=(T0_AGE - te) / GYR, z=1 / math.exp(lna_of_t(te)) - 1, d_kpc=r / KPC))
    yend = sol.y[:, -1]
    return ext, math.hypot(yend[0], yend[1]) / KPC


# ================================================================================================= the dwarfs' field
class Grid:
    """polar (r, theta) grid about the barycentre; Legendre multipoles for the band-passed curl-free projection."""
    def __init__(self, rmin=1.0, rmax=30000.0, nr=300, nth=256, lmax=80, lsm=40):
        self.re = np.geomspace(rmin, rmax, nr + 1) * KPC; self.rc = np.sqrt(self.re[1:] * self.re[:-1]); self.nr = nr
        self.te = np.linspace(0.0, math.pi, nth + 1); self.tc = 0.5 * (self.te[1:] + self.te[:-1]); self.nth = nth
        self.mc = np.cos(self.tc); self.me = np.cos(self.te); self.lmax = lmax; self.lsm = lsm
        Pe = np.array([eval_legendre(l, self.me) for l in range(lmax + 2)])
        self.Pint = np.zeros((lmax + 1, nth))
        for l in range(lmax + 1):
            F = self.me if l == 0 else (Pe[l + 1] - Pe[l - 1]) / (2 * l + 1)
            self.Pint[l] = F[:-1] - F[1:]
        self.Pc = np.array([eval_legendre(l, self.mc) for l in range(lmax + 1)])
        self.dPc = np.zeros((lmax + 1, nth))
        for l in range(1, lmax + 1):
            self.dPc[l] = l * (self.mc * self.Pc[l] - self.Pc[l - 1]) / (self.mc ** 2 - 1.0)
        self.vol = (self.re[1:] ** 3 - self.re[:-1] ** 3) / 3.0; self.dmu = self.me[:-1] - self.me[1:]

    def divergence(self, Wfun):
        R, T = np.meshgrid(self.re, self.tc, indexing="ij"); Wx, Wz = Wfun(R * np.sin(T), R * np.cos(T))
        fr = (self.re[:, None] ** 2) * (Wx * np.sin(T) + Wz * np.cos(T)) * self.dmu[None, :]
        R2, T2 = np.meshgrid(self.rc, self.te, indexing="ij"); Wx2, Wz2 = Wfun(R2 * np.sin(T2), R2 * np.cos(T2))
        ft = np.sin(T2) * (Wx2 * np.cos(T2) - Wz2 * np.sin(T2)) * ((self.re[1:] ** 2 - self.re[:-1] ** 2) / 2.0)[:, None]
        return ((fr[1:] - fr[:-1]) + (ft[:, 1:] - ft[:, :-1])) / (self.vol[:, None] * self.dmu[None, :])

    def smooth(self, ql, Lm):
        """(S_L q)_l: the Gaussian's exact multipole kernel (2 pi L^2)^(-3/2) 4 pi r'^2 e^{-(r-r')^2/2L^2} e^{-z} i_l(z), z = r r'/L^2
        (midpoint in r', log space); rows where L is below 2 cell widths are sub-grid: identity there, so (1 - S_L) q = 0."""
        if Lm is None: return np.zeros_like(ql)
        r = self.rc; dr = self.re[1:] - self.re[:-1]; unres = Lm < 2.0 * dr
        Zs = np.maximum(np.outer(r, r) / Lm ** 2, 1e-300)
        lnG2 = -(r[:, None] - r[None, :]) ** 2 / (2 * Lm ** 2)
        lnpref = -1.5 * math.log(2 * math.pi * Lm ** 2) + math.log(4 * math.pi) + np.log(r ** 2 * dr)[None, :]
        out = np.zeros_like(ql)
        for l in range(min(self.lsm, self.lmax) + 1):
            with np.errstate(all="ignore"):
                lniel = 0.5 * np.log(math.pi / (2 * Zs)) + np.log(np.maximum(ive(l + 0.5, Zs), 1e-300))
                K = np.exp(np.minimum(lnpref + lnG2 + lniel, 700.0))
            K[unres, :] = 0.0; out[l] = K @ ql[l]; out[l, unres] = ql[l, unres]
        if self.lsm < self.lmax: out[self.lsm + 1:, unres] = ql[self.lsm + 1:, unres]
        return out

    def poisson(self, ql):
        """Psi_l, Psi_l' for lap Psi = q: Psi_l = -(1/(2l+1)) [r^-(l+1) Int_0^r q r'^(l+2) + r^l Int_r^oo q r'^(1-l)], by stable
        recursions over cells (cell-averaged q)."""
        nr, lmax = self.nr, self.lmax; l = np.arange(lmax + 1).astype(float); re, rc = self.re, self.rc
        I = np.zeros((lmax + 1, nr)); acc = np.zeros(lmax + 1)
        for i in range(nr):
            a = re[i] / rc[i]; I[:, i] = acc * a ** (l + 1) + ql[:, i] * rc[i] ** 2 * (1 - a ** (l + 3)) / (l + 3)
            b = re[i] / re[i + 1]; acc = acc * b ** (l + 1) + ql[:, i] * re[i + 1] ** 2 * (1 - b ** (l + 3)) / (l + 3)
        O = np.zeros((lmax + 1, nr)); acc = np.zeros(lmax + 1)
        for i in range(nr - 1, -1, -1):
            a = rc[i] / re[i + 1]; b = re[i] / re[i + 1]
            with np.errstate(all="ignore"):
                half = np.where(l == 2, rc[i] ** 2 * np.log(re[i + 1] / rc[i]), rc[i] ** 2 * (a ** (l - 2) - 1) / (2 - l))
                full = np.where(l == 2, re[i] ** 2 * np.log(re[i + 1] / re[i]), re[i] ** 2 * (b ** (l - 2) - 1) / (2 - l))
            O[:, i] = acc * a ** l + ql[:, i] * half; acc = acc * b ** l + ql[:, i] * full
        c = 1.0 / (2 * l + 1)
        return -c[:, None] * (I + O), -c[:, None] * (-(l[:, None] + 1) * I / rc[None, :] + l[:, None] * O / rc[None, :])

    def field(self, q, Lm):
        l_ = np.arange(self.lmax + 1)[:, None]
        ql = ((2 * l_ + 1) / 2.0) * (self.Pint @ q.T)
        Psi, dPsi = self.poisson(ql - self.smooth(ql, Lm))
        return dPsi.T @ self.Pc, -(Psi.T @ self.dPc) * np.sin(self.tc)[None, :] / self.rc[:, None]


def W_pair(m1, m2, z1, z2, a0, Lm, yt):
    def W(xp, z):
        r1 = np.sqrt(xp ** 2 + (z - z1) ** 2); r2 = np.sqrt(xp ** 2 + (z - z2) ** 2); E1, E2 = Efac(r1, Lm), Efac(r2, Lm)
        g1x, g1z = -G * m1 * E1 * xp / r1 ** 3, -G * m1 * E1 * (z - z1) / r1 ** 3
        g2x, g2z = -G * m2 * E2 * xp / r2 ** 3, -G * m2 * E2 * (z - z2) / r2 ** 3
        Vx, Vz = Xfield(g1x + g2x, g1z + g2z, a0, yt); V1x, V1z = Xfield(g1x, g1z, a0, yt); V2x, V2z = Xfield(g2x, g2z, a0, yt)
        return Vx - V1x - V2x, Vz - V1z - V2z
    return W


class PairField:
    """the pair's field on the fixed (radial-orbit) axis: Newton (softened) + each body's isolated band-passed phantom (FP6's
    phantom(), exact 1-D) + the interaction field on the polar grid, tabulated at epochs lna_ep; xsep(l) = M31 - MW [m]."""
    def __init__(self, m1, m2, a0, xsep, lna_ep, bp=True, yl=True, merged=False, grid=None):
        self.m1, self.m2 = m1, m2; M = m1 + m2; self.f1, self.f2 = m1 / M, m2 / M; self.merged = merged
        self.lna = np.asarray(lna_ep); ne = len(self.lna); self.g = Grid() if grid is None else grid; g = self.g
        self.M1 = np.zeros((ne, len(RG))); self.M2 = np.zeros((ne, len(RG)))
        self.DR = np.zeros((ne, g.nr, g.nth)); self.DT = np.zeros((ne, g.nr, g.nth))
        for e, l in enumerate(self.lna):
            a = math.exp(l); Lm = L_of_a(a, bp); yt = yth_of_a(a, yl); x = 0.0 if merged else float(xsep(l))
            self.M1[e] = phantom(m1, a0, Lm, yt, YIELD if yt else 4); self.M2[e] = phantom(m2, a0, Lm, yt, YIELD if yt else 4)
            self.DR[e], self.DT[e] = g.field(g.divergence(W_pair(m1, m2, -self.f2 * x, self.f1 * x, a0, Lm, yt)), Lm)
        self.lrc = np.log(g.rc); self.dlr = self.lrc[1] - self.lrc[0]; self.dth = g.tc[1] - g.tc[0]; self.lRG = np.log(RG)

    def accel(self, l, X, Z, xsep, carrier=0.0):
        ne = len(self.lna); j = int(min(max(np.searchsorted(self.lna, l) - 1, 0), ne - 2))
        f = min(max((l - self.lna[j]) / (self.lna[j + 1] - self.lna[j]), 0.0), 1.0)
        x = 0.0 if self.merged else xsep; aX = np.zeros_like(X); aZ = np.zeros_like(Z)
        for (mb, zb, Mt) in ((self.m1, -self.f2 * x, self.M1), (self.m2, self.f1 * x, self.M2)):
            dz = Z - zb; rb = np.sqrt(X * X + dz * dz)
            newt = G * mb * (1.0 + carrier) / (rb * rb + EPS * EPS) ** 1.5
            prof = (1 - f) * Mt[j] + f * Mt[j + 1]
            mond = G * np.interp(np.log(np.maximum(rb, RG[0])), self.lRG, prof) / np.maximum(rb, 1e-30) ** 3
            mond = np.where(rb < EPS, mond * rb / EPS, mond)
            aX -= (newt + mond) * X; aZ -= (newt + mond) * dz
        r = np.sqrt(X * X + Z * Z); th = np.arctan2(np.abs(X), Z); g = self.g
        ir = np.clip((np.log(np.maximum(r, g.rc[0])) - self.lrc[0]) / self.dlr, 0, g.nr - 1.000001)
        it = np.clip((th - g.tc[0]) / self.dth, 0, g.nth - 1.000001)
        i0 = ir.astype(int); t0 = it.astype(int); fr = ir - i0; ft = it - t0

        def bil(B):
            return (1 - fr) * (1 - ft) * B[i0, t0] + fr * (1 - ft) * B[i0 + 1, t0] + (1 - fr) * ft * B[i0, t0 + 1] + fr * ft * B[i0 + 1, t0 + 1]
        gr = np.where(r > g.re[-1], 0.0, (1 - f) * bil(self.DR[j]) + f * bil(self.DR[j + 1]))
        gt = np.where(r > g.re[-1], 0.0, (1 - f) * bil(self.DT[j]) + f * bil(self.DT[j + 1]))
        s = np.where(X < 0, -1.0, 1.0)
        return aX + (gr * np.sin(th) + gt * np.cos(th)) * s, aZ + gr * np.cos(th) - gt * np.sin(th)


def run_flat(pf, xsep, th, rr, nstep=3000, a_start=0.02, bg=False, hist="none"):
    """dwarfs from the Hubble flow at a_start in the meridional plane (angle th from the MW->M31 axis, radius rr)."""
    X = rr * np.sin(th); Z = rr * np.cos(th); Hi = LG_H0 * math.sqrt(LG_OM / a_start ** 3 + LG_OL); VX = Hi * X; VZ = Hi * Z
    lna = np.linspace(math.log(a_start), 0.0, nstep + 1); h = lna[1] - lna[0]

    def f(l, X_, Z_, VX_, VZ_):
        a = math.exp(l); H = LG_H0 * math.sqrt(LG_OM / a ** 3 + LG_OL)
        car = RATIO_D * retained(1 / a - 1, hist) if hist != "none" else 0.0
        aX, aZ = pf.accel(l, X_, Z_, xsep(l), carrier=car); aX = aX + L_OL_H02 * X_; aZ = aZ + L_OL_H02 * Z_
        if bg:
            k = 0.5 * LG_OM * LG_H0 ** 2 / a ** 3; aX = aX - k * X_; aZ = aZ - k * Z_
        return VX_ / H, VZ_ / H, aX / H, aZ / H
    for i in range(nstep):
        l = lna[i]; k1 = f(l, X, Z, VX, VZ)
        k2 = f(l + h / 2, X + h * k1[0] / 2, Z + h * k1[1] / 2, VX + h * k1[2] / 2, VZ + h * k1[3] / 2)
        k3 = f(l + h / 2, X + h * k2[0] / 2, Z + h * k2[1] / 2, VX + h * k2[2] / 2, VZ + h * k2[3] / 2)
        k4 = f(l + h, X + h * k3[0], Z + h * k3[1], VX + h * k3[2], VZ + h * k3[3])
        X = X + h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6; Z = Z + h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
        VX = VX + h * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]) / 6; VZ = VZ + h * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]) / 6
    return X, Z, VX, VZ


def R0_rays(pf, xsep, thetas, ri_lo=2.0, ri_hi=80.0, n0=48, npass=6, nins=10, rpair=0.6, nstep=3000, bg=False, hist="none"):
    """the zero-velocity radius on each ray (angle from the axis): a coarse r_i grid, then adaptive insertion wherever today's
    radius jumps by > 25% between neighbours in the outer zone (the r_i -> r_today map is very steep at the zero-velocity
    shell), then the outermost - -> + crossing of v_r whose outer tracer ends beyond rpair [Mpc] with a continuous bracket
    (radii within 5%).  Also returns every tracer (r_i, today r, v_r) per ray for the Hubble diagram."""
    nt = len(thetas); RI = np.geomspace(ri_lo, ri_hi, n0) * KPC
    X, Z, VX, VZ = run_flat(pf, xsep, np.repeat(thetas, n0), np.tile(RI, nt), nstep=nstep, bg=bg, hist=hist)
    rt = np.hypot(X, Z); vr = (X * VX + Z * VZ) / np.maximum(rt, 1e-30)
    data = [dict(ri=RI.copy(), r=rt[k * n0:(k + 1) * n0], v=vr[k * n0:(k + 1) * n0]) for k in range(nt)]
    for _ in range(npass):
        nth_, nr_, own = [], [], []
        for k in range(nt):
            d = data[k]; o = np.argsort(d["ri"]); ri_, r_, v_ = d["ri"][o], d["r"][o], d["v"][o]
            for j in range(len(ri_) - 1):
                if max(r_[j], r_[j + 1]) > 0.2 * MPC and (r_[j + 1] / max(r_[j], 1e-30) > 1.25 or r_[j] / max(r_[j + 1], 1e-30) > 1.25
                                                           or ((v_[j] < 0 < v_[j + 1]) and abs(r_[j + 1] / r_[j] - 1) >= 0.05)):
                    ins = np.geomspace(ri_[j], ri_[j + 1], nins + 2)[1:-1]; nth_ += [thetas[k]] * nins; nr_ += list(ins); own += [k] * nins
        if not nr_: break
        nth_, nr_, own = np.array(nth_), np.array(nr_), np.array(own)
        X, Z, VX, VZ = run_flat(pf, xsep, nth_, nr_, nstep=nstep, bg=bg, hist=hist)
        rt = np.hypot(X, Z); vr = (X * VX + Z * VZ) / np.maximum(rt, 1e-30)
        for k in range(nt):
            s = own == k
            if s.any():
                data[k]["ri"] = np.concatenate([data[k]["ri"], nr_[s]]); data[k]["r"] = np.concatenate([data[k]["r"], rt[s]])
                data[k]["v"] = np.concatenate([data[k]["v"], vr[s]])
    R0 = np.full(nt, np.nan)
    for k in range(nt):
        d = data[k]; o = np.argsort(d["ri"]); r_, v_ = d["r"][o], d["v"][o]
        idx = [j for j in range(len(r_) - 1) if v_[j] < 0 < v_[j + 1] and r_[j + 1] > rpair * MPC and abs(r_[j + 1] / r_[j] - 1) < 0.05]
        if idx:
            j = idx[-1]; fr_ = -v_[j] / (v_[j + 1] - v_[j]); R0[k] = (r_[j] + fr_ * (r_[j + 1] - r_[j])) / MPC
    return R0, data


RAYS_C, RAYS_W = np.polynomial.legendre.leggauss(8)                              # Gauss-Legendre rays in cos(theta)
RAYS = np.arccos(RAYS_C)


def ray_stats(R0, cs=RAYS_C, ws=RAYS_W):
    R0 = np.asarray(R0, float); ok = np.isfinite(R0)
    val = np.abs(cs) <= 0.9                                                     # XR13's validity cut (90% of the sky)
    mean_all = float(np.sum(ws[ok] * R0[ok]) / np.sum(ws[ok])) if ok.any() else float("nan")
    s = ok & val
    mean_val = float(np.sum(ws[s] * R0[s]) / np.sum(ws[s])) if s.any() else float("nan")
    return dict(rays=R0.tolist(), cos=list(map(float, cs)), mean=mean_all, mean_valid=mean_val, n_ok=int(ok.sum()),
                axis=float(np.nanmean(R0[np.argsort(-np.abs(cs))[:2]])), perp=float(np.nanmean(R0[np.argsort(np.abs(cs))[:2]])))


def hubble_sample(data, ws=RAYS_W):
    """every tracer today with its Lagrangian mass weight: solid angle (GL weight) x r_i^3 x local d ln r_i (per ray)."""
    R, V, W = [], [], []
    for k, d in enumerate(data):
        o = np.argsort(d["ri"]); ri = d["ri"][o]; lr = np.log(ri)
        dl = np.gradient(lr) if len(lr) > 2 else np.ones_like(lr)
        R.append(d["r"][o] / MPC); V.append(d["v"][o] / 1e3); W.append(ws[k] * ri ** 3 * dl)
    return np.concatenate(R), np.concatenate(V), np.concatenate(W)


def lin_fit(R, V, w=None, lo=0.7, hi=3.0):
    s = (R > lo) & (R < hi) & np.isfinite(V)
    w = np.ones_like(R) if w is None else w
    A = np.vstack([R[s], np.ones(s.sum())]).T * np.sqrt(w[s])[:, None]
    h, b = np.linalg.lstsq(A, V[s] * np.sqrt(w[s]), rcond=None)[0]
    res = V[s] - (h * R[s] + b)
    return dict(R0=float(-b / h), H=float(h), rms=float(np.sqrt(np.sum(w[s] * res ** 2) / np.sum(w[s]))), n=int(s.sum()))


# ================================================================================================= the pincer (counterfactual)
def phantom_efe(Mb_kg, a0, L_m, yth, e):
    """FP6's band-passed phantom with FP9's yield and a uniform external field e [a0] in the kernel's argument (scalar-sum
    form), e NOT band-passed -- the counterfactual in which an external field reaches the kernel (in (H_Y) it cannot: h(0) = 0)."""
    gfr, Fmat = M6["gfrac_smooth"], M6["Fmat"]
    gN = G * Mb_kg / RG ** 2; gbp = gN * (1.0 - gfr(RG / L_m)); y = gbp / a0
    Mraw = x_P2(y + e - yth) / np.maximum(y + e, 1e-300) * gbp * RG ** 2 / G
    return Mraw - (Fmat(L_m) @ np.diff(Mraw) + Mraw[0] * gfr(RG / L_m))


def lgR0_efe(Mb, a0, e, LL=None):
    LNA_T, lg_R0 = M6["LNA_T"], M6["lg_R0"]; Mbk = Mb * MSUN
    tab = np.array([Mbk + phantom_efe(Mbk, a0, L_of_a(math.exp(la), LL=LL), yth_of_a(math.exp(la)), e) for la in LNA_T]); lnR = np.log(RG)

    def Menc(r, a):
        x = math.log(a); j = min(max(np.searchsorted(LNA_T, x) - 1, 0), len(LNA_T) - 2)
        f_ = (x - LNA_T[j]) / (LNA_T[j + 1] - LNA_T[j]); return np.interp(np.log(np.maximum(r, RG[0])), lnR, (1 - f_) * tab[j] + f_ * tab[j + 1])
    return lg_R0(Menc)


# ================================================================================================= data (committed UNGC)
def ungc_hubble(f31):
    """the UNGC (Karachentsev+2013) in the LG barycentric frame: barycentre at f31 of the way to M31, LG-frame velocities with
    the barycentre at rest; the Karachentsev-Makarov projection V_r = V (D - D_c cos) / R (k02's group_frame with V_c = 0)."""
    rows = HL.vizier_tsv("ungc_karachentsev2013.tsv")
    nm = np.array([r_["Name"].strip() for r_ in rows]); MD = np.array([r_["MD"].strip() for r_ in rows])
    ra = np.array([HL._f(r_["_RAJ2000"]) for r_ in rows]); de = np.array([HL._f(r_["_DEJ2000"]) for r_ in rows])
    D = np.array([HL._f(r_["Dist"]) for r_ in rows]); V = np.array([HL._f(r_["Vlg"]) for r_ in rows])
    fD = np.array([r_["f_Dist"].strip() for r_ in rows]); Ti = np.array([HL._f(r_["Ti1"]) for r_ in rows])
    lK = np.array([HL._f(r_["KLum"]) for r_ in rows]); lH = np.array([HL._f(r_["MHI"]) for r_ in rows])
    un = np.nan_to_num(np.stack([np.cos(np.radians(de)) * np.cos(np.radians(ra)), np.cos(np.radians(de)) * np.sin(np.radians(ra)), np.sin(np.radians(de))], axis=1))
    i31 = int(np.where(nm == "MESSIER031")[0][0])
    xc = f31 * D[i31] * un[i31]; Dc = float(np.linalg.norm(xc)); nc = xc / Dc; cth = un @ nc
    R = np.sqrt(np.clip(D ** 2 + Dc ** 2 - 2 * D * Dc * cth, 0, None)); Vr = V * (D - Dc * cth) / np.maximum(R, 1e-9)
    return dict(name=nm, MD=MD, D=D, V=V, fD=fD, Ti=Ti, lK=lK, lH=lH, R=R, Vr=Vr)


ACC_DIST = ("TRGB", "Cep", "RR", "HB", "SBF", "BS", "CMD", "geom")
OTHER_GROUPS = ("IC0342", "Maffei1", "Maffei2", "MB1", "MB3", "Dw1", "Dw2", "NGC2403", "NGC1569", "DDO044", "MESSIER081", "NGC4214",
                "NGC5128", "NGC0253")
HVG_BZ = ("SexA", "SexB", "NGC3109", "Antlia", "LeoP", "KKH98", "HIZSS003")   # Banik & Zhao 2018 (MNRAS 473, 4033) Table 3


# ================================================================================================= jobs (top level: worker-safe)
FMW = 0.37                                                                       # MW share of the LG's baryons (6.47e10 / 1.75e11)


def job_timing(cfg):
    law, foot, Mb, convs = cfg; t = time.time(); bp = yl = (law == "HY")
    m1, m2 = FMW * Mb * MSUN, (1 - FMW) * Mb * MSUN
    dg, ln_, T = force_table(m1, m2, A0[foot], bp, yl)
    out = {}
    for conv in convs:
        hist = {"C_decay": "decay", "C_full": "full"}.get(conv, "none")
        out[conv] = branches(Acc(dg, ln_, T, m1 + m2, hist=hist), bg=(conv == "B"))
    return cfg, out, time.time() - t


def job_sens(cfg):
    """T5: the canonical headline's v_r under numerical / idealisation changes."""
    var, Mb = cfg; t = time.time(); fmw = 1 / 3 if var == "split 1:2" else FMW
    m1, m2 = fmw * Mb * MSUN, (1 - fmw) * Mb * MSUN
    if var == "table 2x":
        dg, ln_, T = force_table(m1, m2, A0["canonical"], True, True, dgrid=np.geomspace(2 * KPC, 8 * MPC, 128), lna=np.linspace(math.log(0.02), 0.0, 97))
    else:
        dg, ln_, T = force_table(m1, m2, A0["canonical"], True, True)
    acc = Acc(dg, ln_, T, m1 + m2, soft=(5 * KPC if var == "eps 5 kpc" else EPS))
    a_st = {"a_start 0.05": 0.05, "a_start 0.1": 0.1}.get(var, 0.02)
    br = branches(acc, nstep=(16000 if var == "nstep 2x" else 8000), a_start=a_st, lo=0.05 * a_st / 0.02, hi=600.0 * a_st / 0.02)
    k0 = [b for b in br if b["k"] == 0 and b["vr"] < 0]
    return var, (k0[0]["vr"] if k0 else float("nan")), time.time() - t


def job_matched(cfg):
    """a timing-matched configuration: the table at its mass, its branch, the J = 0 orbit x(ln a), 2-D orbits with v_t, and the
    dwarfs (two-body and merged)."""
    name, law, foot, Mb, conv, k, opts = cfg; t = time.time(); bp = yl = (law == "HY")
    m1, m2 = FMW * Mb * MSUN, (1 - FMW) * Mb * MSUN; bg = conv == "B"; hist = {"C_decay": "decay", "C_full": "full"}.get(conv, "none")
    dg, ln_, T = force_table(m1, m2, A0[foot], bp, yl); acc = Acc(dg, ln_, T, m1 + m2, hist=hist)
    br = [b for b in branches(acc, bg=bg) if b["k"] == k and b["vr"] < 0]
    if not br:
        return name, dict(error="no branch"), time.time() - t
    b = br[0]
    x, u, nc, lna, X = shoot(acc, np.array([b["ri_kpc"] * KPC]), bg=bg, store=True); X = X[:, 0]
    xsep = lambda l: float(np.interp(l, lna, X))
    d = np.abs(X) / MPC; a_ = np.exp(lna); imax = int(np.argmax(d))
    peri_z = [float(1 / a_[i] - 1) for i in range(1, len(X)) if np.sign(X[i]) != np.sign(X[i - 1])]
    # MOND switch-on of the pair: first epoch where the table's MOND part exceeds 10% of Newton at the current separation
    on_z = None
    for i in range(0, len(lna), 20):
        if abs(float(acc.mond(lna[i], np.array([max(d[i] * MPC, dg[0])]))[0])) > 0.1 * G * (m1 + m2) / max(d[i] * MPC, dg[0]) ** 2:
            on_z = float(1 / a_[i] - 1); break
    orb = {}
    if opts.get("orb2d"):
        for vt in VT_SET:
            back, d_early = orbit2d(acc, vt, t_of_a(0.02), bg=bg)
            fwd, _ = orbit2d(acc, vt, T0_AGE + 8 * GYR, bg=bg)
            orb[f"{vt:g}"] = dict(past=back, d_at_a002_kpc=d_early, future=[e for e in fwd if e["lookback_Gyr"] < 0][:2])
    out = dict(branch=b, dmax=float(d[imax]), z_dmax=float(1 / a_[imax] - 1), t_dmax_lookback=float((T0_AGE - t_of_a(a_[imax])) / GYR),
               z_peri=peri_z, z_mond_on=on_z, orb2d=orb)
    if opts.get("tracers"):
        nr = opts.get("nrays", 8); cs, ws = np.polynomial.legendre.leggauss(nr); th = np.arccos(cs)
        ri_hi = 250.0 if bg else 80.0
        pf = PairField(m1, m2, A0[foot], xsep, LNAT, bp=bp, yl=yl)
        R0, data = R0_rays(pf, xsep, th, ri_hi=ri_hi, bg=bg, hist=hist)
        out["R0"] = ray_stats(R0, cs, ws)
        Rh, Vh, Wh = hubble_sample(data, ws)
        out["hubble"] = dict(R=Rh.tolist(), V=Vh.tolist(), W=Wh.tolist())
        pfm = PairField(m1, m2, A0[foot], xsep, LNAT, bp=bp, yl=yl, merged=True)
        R0m, _ = R0_rays(pfm, lambda l: 0.0, np.array([math.pi / 2]), ri_hi=ri_hi, bg=bg, hist=hist)
        out["R0_merged"] = float(R0m[0])
    return name, out, time.time() - t


def job_lscan(cfg):
    """X1: at band-pass length L(0.25) = L25 (the yield and n unchanged), the first-approach timing mass and the merged-pair R0 at it."""
    L25, foot, masses = cfg; t = time.time(); LL = L25 / M6["OmL_z"](0.25) ** (HEAD["n"] / 2.0); pts = []
    for Mb in masses:
        m1, m2 = FMW * Mb * MSUN, (1 - FMW) * Mb * MSUN
        dg, ln_, T = force_table(m1, m2, A0[foot], True, True, LL=LL)
        br = [b for b in branches(Acc(dg, ln_, T, m1 + m2)) if b["k"] == 0 and b["vr"] < 0]
        pts.append((Mb, br[0]["vr"] if br else float("nan")))
    Mt = timing_mass(pts)
    R0 = lgR0_efe(Mt, A0[foot], 0.0, LL=LL) if Mt else float("nan")
    return cfg, pts, Mt, R0, LL * LG_OmL(1.0), time.time() - t


def job_ctrl_tracer(cfg):
    law, foot = cfg; t = time.time(); bp = yl = law == "HY"
    m1, m2 = FMW * 1.145e11 * MSUN, (1 - FMW) * 1.145e11 * MSUN
    pf = PairField(m1, m2, A0[foot], lambda l: 0.0, LNAT, bp=bp, yl=yl, merged=True)
    R0, _ = R0_rays(pf, lambda l: 0.0, np.array([math.pi / 2]))
    return cfg, float(R0[0]), time.time() - t


def job_ctrl_shooter(foot):
    t = time.time(); br = branches(acc_testparticle(1.8e11 * MSUN, HL.A0[foot]), D0=0.78 * MPC)
    k0 = [b for b in br if b["k"] == 0 and b["vr"] < 0]
    return foot, (k0[0]["vr"] if k0 else float("nan")), time.time() - t


def job_zhao_timing(cfg):
    V1, V2 = cfg; t = time.time(); a0Z = 1.2e-10
    m1, m2 = (V1 * 1e3) ** 4 / (G * a0Z), (V2 * 1e3) ** 4 / (G * a0Z); M = m1 + m2; q1 = m1 / M; q2 = 1 - q1
    Q = 2 * (1 - q1 ** 1.5 - q2 ** 1.5) / (3 * q1 * q2)
    acc = lambda l, d: G * M * d / (d ** 2 + EPS ** 2) ** 1.5 + Q * math.sqrt(G * M * a0Z) * d / (d ** 2 + EPS ** 2)
    br = branches(acc, bg=True, D0=0.77 * MPC)
    k1 = [b for b in br if b["k"] == 1 and b["vr"] < 0]
    return cfg, M / MSUN, (k1[0]["vr"] if k1 else float("nan")), time.time() - t


# ================================================================================================= reporting
CH = []
OUT = {"lane": "FP11", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
T0 = time.time()


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def el():
    return f"[{time.time() - T0:.0f} s]"


def check(name, measured, ok, load_bearing=True, reading=""):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def timing_mass(pts, target=VR_LG):
    """pts: [(M_b, v_r)] on one approaching branch; the mass where v_r = target by linear interpolation in ln M (None if the
    scanned masses do not bracket it)."""
    pts = sorted((m, v) for m, v in pts if v == v)
    for (m1_, v1), (m2_, v2) in zip(pts[:-1], pts[1:]):
        if (v1 - target) * (v2 - target) <= 0 and v1 != v2:
            return float(math.exp(math.log(m1_) + (target - v1) / (v2 - v1) * (math.log(m2_) - math.log(m1_))))
    return None


def branch_pts(TS, law, foot, conv, k):
    pts = []
    for (lw, f, Mb, _), out in TS.items():
        if lw == law and f == foot and conv in out:
            vs = [b["vr"] for b in out[conv] if b["k"] == k and b["vr"] < 0]
            if vs:
                pts.append((Mb, min(vs)))
    return sorted(pts)


def main():
    from multiprocessing import Pool
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: the SCORED two-body law loses the separator (band-pass + yield -> the plain P2 root law); T1 must FAIL ***")
    SCORED = "P2" if MUTATE else "HY"
    P(f"\n  footings a0 = {A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2 (FP0); (H_Y) constants L_Lambda = {L_LAMBDA:.3f} Mpc, n = {HEAD['n']:g}, "
      f"y_Lambda = {Y_LAMBDA:.3e}, p' = {HEAD['pp']:g} (FP9); LG cosmology h = {LG_H0 * MPC / 1e5:.3f}, Om = {LG_OM:.4f} (FP6/XR4); t0 = {T0_AGE / GYR:.2f} Gyr")
    mw_gas = 1.33 * 10 ** 9.47; m31_gas = 1.33 * 10 ** 9.73                     # UNGC log M_HI (Milky Way 9.47, MESSIER031 9.73)
    mw_b, m31_b = MW_STARS + mw_gas, M31_STARS + m31_gas
    P(f"  baryons: MW {mw_b:.3e} (stars {MW_STARS:.2e} +- {MW_STARS_E:.2e}, HI x 1.33 {mw_gas:.2e}), M31 {m31_b:.3e} (stars {M31_STARS:.2e} "
      f"+{M31_STARS_EP:.1e}/-{M31_STARS_EM:.1e}, HI x 1.33 {m31_gas:.2e}); total {mw_b + m31_b:.3e}, MW share {mw_b / (mw_b + m31_b):.3f} (used {FMW}); "
      f"window [{MB_LO:.3e}, {MB_HI:.3e}]")
    OUT["numbers"]["baryons"] = dict(MW=mw_b, M31=m31_b, total=mw_b + m31_b, share_MW=mw_b / (mw_b + m31_b), window=[MB_LO, MB_HI])
    # ============================================================================================= K controls (light)
    banner("K  CONTROLS: the chain's committed machinery reproduced; the two-body law's integral, the multipoles, the tracers, the literature")
    lg = M6["lg_both"](L_LAMBDA, HEAD["n"], floor=(HEAD["y25"], HEAD["pp"], YIELD))
    F9 = json.load(open(os.path.join(HERE, "FP9_web_galaxy_separator_results.json")))["numbers"]
    ref9 = F9["H3"]["2.0_1.3"]; dk1 = max(abs(lg[f] / ref9[f] - 1) for f in FOOTS)
    check("K1 CONTROL: FP9's LG zero-velocity radius at the (H_Y) headline cell (one merged point mass, M_b = 1.145e11) is reproduced "
          "exactly with FP6's committed machinery and FP9's yield hook", f"{lg['canonical']:.4f} / {lg['alt']:.4f} Mpc vs committed "
          f"{ref9['canonical']:.4f} / {ref9['alt']:.4f} (max rel dev {dk1:.1e})", dk1 < 1e-9)
    OUT["numbers"]["K1"] = dict(R0=lg, committed=ref9)

    # K3 two-body integral
    a0c = A0["canonical"]; k3 = {}
    kern = []
    for (mB, d, Lz, yt) in ((1.2e11, 0.78, None, None), (1.2e11, 0.78, 1.69, 3.5e-7), (1.2e11, 0.3, 0.183, 2.5e-3), (6e10, 0.1, 0.5, None)):
        Lm = None if Lz is None else Lz * MPC
        gz = dg_body(6e10 * MSUN, mB * MSUN, d * MPC, a0c, Lm, yt, ns=500, control_W="Biso")
        ref = g_iso(mB * MSUN, a0c, Lm, yt, np.array([d * MPC]))[0]
        kern.append(abs(-gz / ref - 1))
    mom, mil = [], []
    for (mA, mB, d) in ((0.37 * 1.75e11, 0.63 * 1.75e11, 0.78), (1e11, 1e11, 0.78), (0.37 * 1.75e11, 0.63 * 1.75e11, 3.0), (0.37 * 1.75e11, 0.63 * 1.75e11, 0.2)):
        dA = dg_body(mA * MSUN, mB * MSUN, d * MPC, a0c, None, None); dB = dg_body(mB * MSUN, mA * MSUN, d * MPC, a0c, None, None)
        gNB, gNA = G * mB * MSUN / (d * MPC) ** 2, G * mA * MSUN / (d * MPC) ** 2
        aA = float(nu_p2(gNB / a0c)) * gNB - dA; aB = float(nu_p2(gNA / a0c)) * gNA - dB
        mom.append(abs(mA * aA / (mB * aB) - 1))
        M = (mA + mB) * MSUN; F = (2 / 3) * math.sqrt(G * a0c) * (M ** 1.5 - (mA * MSUN) ** 1.5 - (mB * MSUN) ** 1.5) / (d * MPC)
        mil.append((d, aA / (F / (mA * MSUN) + gNB)))
    tp = []
    for q in (1e-4, 1e-2):
        mA, mB, d = 1.2e11, 1.2e11 * q, 0.5
        dB = dg_body(mB * MSUN, mA * MSUN, d * MPC, a0c, None, None, smin_fac=1e-7, ns=900)
        gA = float(nu_p2(G * mA * MSUN / (d * MPC) ** 2 / a0c)) * G * mA * MSUN / (d * MPC) ** 2
        exact = (2 / 3) * ((1 + q) ** 1.5 - 1 - q ** 1.5) / q
        tp.append((q, (gA - dB) / gA, exact))
    mil_d = {f"{d:g}": r for d, r in mil}
    q_mw = FMW; q_31 = 1 - FMW; Fq = (2 / 3) * (1 - q_mw ** 1.5 - q_31 ** 1.5)          # Milgrom's force in units sqrt(G a0) M^1.5 / d
    sh_mw, sh_31 = Fq / q_mw / math.sqrt(q_31), Fq / q_31 / math.sqrt(q_mw)
    sh_rel = Fq * (1 / q_mw + 1 / q_31)                                          # relative acceleration / (sqrt(G M a0)/d)
    ok3 = max(kern) < 5e-3 and max(mom) < 1e-4 and all(abs(r - 1) < 0.1 for _, r in mil) and abs(mil_d["3"] - 1) < abs(mil_d["0.78"] - 1) < abs(mil_d["0.2"] - 1) \
        and all(abs(v / e - 1) < 3e-3 for _, v, e in tp)
    check("K3 CONTROL (the two-body integral of the chain's static law): (a) the band-passed dipole kernel on W = V_B,iso reproduces FP6's "
          "committed output-filtered isolated phantom (incl. band-pass + yield cells); (b) momentum: m1 a1 = m2 a2; (c) the deep-MOND limit is "
          "Milgrom's two-body force (the deviation falls as r_M/d); (d) the test-particle limit is 1 - (2/3) sqrt(m2/m1) x the P2 field",
          f"(a) max |rel dev| {max(kern):.1e}; (b) max |m1 a1/(m2 a2) - 1| {max(mom):.1e}; (c) a_1 / (Milgrom + Newton) at d = "
          + ", ".join(f"{d:g}: {r:.4f}" for d, r in mil) + f" Mpc; (d) " + ", ".join(f"q = {q:.0e}: {v:.5f} (exact {e:.5f})" for q, v, e in tp), ok3,
          reading=f"the non-linear superposition matters: in the deep limit the MW feels {sh_mw:.2f} and M31 {sh_31:.2f} of the other's "
                  f"test-particle MOND pull, and the relative acceleration is {sh_rel:.2f} of the merged-mass test-particle value (XR13's 'M*')")
    OUT["numbers"]["K3"] = dict(kernel=kern, momentum=mom, milgrom=mil, test_particle=tp)

    # K4 multipoles vs direct
    gridK = Grid(); k4 = []
    for (d_mpc, a) in ((0.78, 1.0), (0.9, 0.667), (0.2, 0.5), (0.05, 0.5)):
        d = d_mpc * MPC; Lm = L_of_a(a); yt = yth_of_a(a); m1, m2 = FMW * 1.75e11 * MSUN, (1 - FMW) * 1.75e11 * MSUN
        f1, f2 = m1 / (m1 + m2), m2 / (m1 + m2); z1, z2 = -f2 * d, f1 * d
        gr, gt = gridK.field(gridK.divergence(W_pair(m1, m2, z1, z2, A0["canonical"], Lm, yt)), Lm)
        v2 = float(np.interp(math.log(abs(z2)), np.log(gridK.rc), gr[:, 0])); v1 = -float(np.interp(math.log(abs(z1)), np.log(gridK.rc), gr[:, -1]))
        d2 = dg_body(m2, m1, d, A0["canonical"], Lm, yt, ns=400); d1 = -dg_body(m1, m2, d, A0["canonical"], Lm, yt, ns=400)
        k4.append((d_mpc, a, v1 / d1, v2 / d2))
    check("K4 CONTROL: the dwarfs' interaction field (Legendre multipoles on the polar grid: finite-volume divergence, the Gaussian's exact "
          "multipole kernel, Poisson recursion) equals the direct on-axis integral at both bodies", "multipole/direct at (d, a): "
          + "; ".join(f"({d_:g}, {a_:g}): MW {r1:.4f}, M31 {r2:.4f}" for d_, a_, r1, r2 in k4), all(abs(r1 - 1) < 0.01 and abs(r2 - 1) < 0.01 for _, _, r1, r2 in k4))
    OUT["numbers"]["K4"] = k4

    # K6 literature (backward orbits with Zhao's own law and K term)
    a0Z = 1.2e-10; T14 = 14.0 * GYR
    mZ1, mZ2 = (180e3) ** 4 / (G * a0Z), (225e3) ** 4 / (G * a0Z); MZ = mZ1 + mZ2; q1 = mZ1 / MZ; q2 = 1 - q1
    QZ = 2 * (1 - q1 ** 1.5 - q2 ** 1.5) / (3 * q1 * q2)
    ageZ = quad(lambda a: 1.0 / (a * (1.0 / T14) * math.sqrt(0.667 + 0.333 / a ** 3)), 1e-8, 1.0)[0]

    def rhsZ(t, y):
        x, yy, vx, vy = y; r = math.hypot(x, yy); ar = G * MZ / r ** 2 + QZ * math.sqrt(G * MZ * a0Z) / r
        K = 2.0 / (3.0 * T14 ** 2) - 2.0 / (9.0 * t ** 2)
        return [vx, vy, K * x - ar * x / r, K * yy - ar * yy / r]
    zres = {}
    for vt in (17.0, 34.0):
        sol = solve_ivp(rhsZ, (ageZ, 0.05 * GYR), [770 * KPC, 0.0, -109.3e3, vt * 1e3], method="DOP853", rtol=1e-10, atol=1e-6, dense_output=True, max_step=0.01 * GYR)
        ts = np.linspace(sol.t[0], sol.t[-1], 20000); Y = sol.sol(ts); r = np.hypot(Y[0], Y[1]) / KPC
        mins = [i for i in range(1, len(r) - 1) if r[i] < r[i - 1] and r[i] < r[i + 1]]
        zres[vt] = [((ageZ - ts[i]) / GYR, float(r[i])) for i in mins]
    P(f"    Zhao+2013 nominal (V = 180 / 225 km/s -> {mZ1 / MSUN:.2e} + {mZ2 / MSUN:.2e} Msun at a0 = 1.2e-10, Q = {QZ:.3f}; their K-term, age "
      f"{ageZ / GYR:.2f} Gyr): pericentres (look-back Gyr, kpc) v_t = 17: {[(round(a, 2), round(b, 1)) for a, b in zres[17.0]]}, v_t = 34: "
      f"{[(round(a, 2), round(b, 1)) for a, b in zres[34.0]]}")
    OUT["numbers"]["K6_backward"] = {str(k_): v for k_, v in zres.items()}

    # K7 gates reproduced
    OmL_z6, L_phys, law_dev_dex, kids_class = M6["OmL_z"], M6["L_phys"], M6["law_dev_dex"], M6["kids_class"]
    yz = lambda z: HEAD["y25"] * (OmL_z6(0.25) / OmL_z6(z)) ** HEAD["pp"]
    flag = {(f, Mv): law_dev_dex(Mv, A0[f], 0.1, L_phys(L_LAMBDA, HEAD["n"], 1 / 3.5), yz(2.5), YIELD) for f in FOOTS for Mv in (1e10, 1e11)}
    sparc = {f: max(abs(law_dev_dex(Mv, A0[f], yv, L_phys(L_LAMBDA, HEAD["n"], 1.0), yz(0.0), YIELD)) for Mv in (1e9, 1e10, 1e11, 1e12)
                    for yv in (0.01, 0.03, 0.1, 1.0, 10.0, 100.0)) for f in FOOTS}
    kids = {f: kids_class(A0[f], HEAD["L25"], yz(0.25), YIELD) - kids_class(A0[f]) for f in FOOTS}
    H2 = F9["H2"]
    d7 = max([abs(flag[(f, Mv)] / H2["flag"][str((f, Mv))] - 1) for f in FOOTS for Mv in (1e10, 1e11)] + [abs(sparc[f] / H2["sparc"][f] - 1) for f in FOOTS]
             + [abs(kids[f] - H2["kids"][f]) for f in FOOTS])
    check("K7 CONTROL: FP9's headline gate numbers -- the 1e10/1e11 flagship at z = 2.5, the SPARC range, KiDS lead grade -- are reproduced "
          "exactly from FP6's committed machinery with FP9's four constants (the constants every number in this lane uses)",
          f"flagship {min(flag.values()):+.4f}..{max(flag.values()):+.4f} dex; SPARC {sparc['canonical']:.1e}/{sparc['alt']:.1e} dex; KiDS "
          f"{kids['canonical']:+.2f}/{kids['alt']:+.2f}; max deviation from FP9's JSON {d7:.1e}", d7 < 1e-9)
    OUT["numbers"]["K7"] = dict(flag={str(k_): v for k_, v in flag.items()}, sparc=sparc, kids=kids)

    # data (light)
    DAT = {f31: ungc_hubble(f31) for f31 in (0.5, 0.63, 2 / 3)}
    P(f"    {el()}")

    h76 = {}
    for f in FOOTS:                                                              # item 13's own scheme (XR13 C3), reimplemented
        t0h = 13.8e9 * 3.156e7

        def rhs(t, y, a0=HL.A0[f]):
            r, v = y; r = max(r, 1e18); gN = HL.G * 1.8e11 * HL.Msun / r ** 2
            return [v, -gN * HL.nu_s(gN / a0) + HL.OM_L * HL.H0 ** 2 * r]
        lo_, hi_ = 1e3, 3e6
        for _ in range(60):
            mid = 0.5 * (lo_ + hi_); s = solve_ivp(rhs, (0, t0h), [1e19, mid], rtol=1e-9, atol=1e3, max_step=t0h / 2000)
            lo_, hi_ = (mid, hi_) if s.y[0][-1] < 0.78 * HL.Mpc else (lo_, mid)
        s = solve_ivp(rhs, (0, t0h), [1e19, 0.5 * (lo_ + hi_)], rtol=1e-9, atol=1e3, max_step=t0h / 2000)
        h76[f] = s.y[1][-1] / 1e3
    P(f"    serial controls done {el()}; the two workers start now")
    pool = Pool(NPROC)
    # ---- every independent heavy job is queued now; the main process only does light work while they run
    HY_M = (1.145e11, 1.45e11, 1.75e11, 2.1e11, 2.4e11, 3.0e11)
    P2_M = (1.145e11, 1.75e11, 2.4e11, 3.0e11, 4.0e11, 5.0e11, 6.0e11)
    jobs_t = []
    for f in FOOTS:
        for Mb in HY_M:
            jobs_t.append(("HY", f, Mb, ("A", "B", "C_decay", "C_full") if Mb <= 2.1e11 else ("A", "B")))
        for Mb in (6e11, 1e12):
            jobs_t.append(("HY", f, Mb, ("A", "B")))
        for Mb in P2_M:
            jobs_t.append(("P2", f, Mb, ("A", "B")))
    AT = [pool.apply_async(job_timing, (c,)) for c in jobs_t]
    AC = [pool.apply_async(job_ctrl_tracer, ((lw, f),)) for lw in ("HY", "P2") for f in FOOTS]
    AS = [pool.apply_async(job_ctrl_shooter, (f,)) for f in FOOTS]
    AZ = [pool.apply_async(job_zhao_timing, (c,)) for c in ((180, 205), (180, 225), (190, 250))]
    AV = [pool.apply_async(job_sens, ((v, 1.75e11),)) for v in ("nstep 2x", "table 2x", "a_start 0.05", "a_start 0.1", "eps 5 kpc", "split 1:2")]

    # ---- collect the pool's controls
    shoot_c = {}
    for a_ in AS:
        f, v, dt = a_.get(); shoot_c[f] = v
    ok2 = abs(h76["canonical"] + 222.5) < 1.0 and abs(h76["alt"] + 241.5) < 1.0 and all(abs(shoot_c[f] - h76[f]) < 1.5 for f in FOOTS)
    check("K2 CONTROL: hunt item 13's radial MOND timing (XR13 C3: M_b = 1.8e11, test-particle nu_RAR, from r = 1e19 m at t = 0) is reproduced "
          "with its own scheme, and this lane's Hubble-flow shooter (start on the Hubble flow at a = 0.02, XR4's convention) gives the same "
          "first-approach velocity with the same law", f"item 13: {h76['canonical']:+.1f} / {h76['alt']:+.1f} km/s; this lane's shooter "
          f"{shoot_c['canonical']:+.1f} / {shoot_c['alt']:+.1f} km/s", ok2)
    OUT["numbers"]["K2"] = dict(item13=h76, shooter=shoot_c)
    ctr = {}
    for a_ in AC:
        (lw, f), R0, dt = a_.get(); ctr[(lw, f)] = R0
    F1 = json.load(open(os.path.join(HERE, "FP1_static_sector_results.json")))["numbers"]["E3"]
    refs = {("HY", f): ref9[f] for f in FOOTS}; refs.update({("P2", f): F1[f]["R0_e0"] for f in FOOTS})
    d5 = max(abs(ctr[k_] / refs[k_] - 1) for k_ in ctr)
    check("K5 CONTROL: the dwarf machinery (two-body field tables + meridional tracers + the adaptive zero-velocity finder) with the pair "
          "merged reproduces FP9's (H_Y) R0 and FP1's plain-P2 R0 (M_b = 1.145e11, both footings)",
          "; ".join(f"{lw}/{f}: {ctr[(lw, f)]:.4f} vs {refs[(lw, f)]:.4f}" for (lw, f) in ctr) + f" (max rel dev {d5:.1e})", d5 < 3e-3)
    OUT["numbers"]["K5"] = {f"{k_[0]}/{k_[1]}": [ctr[k_], refs[k_]] for k_ in ctr}
    ztim = []
    for a_ in AZ:
        cfg, Mz, vz, dt = a_.get(); ztim.append((cfg, Mz, vz))
    Mz_t = timing_mass([(Mz, vz) for _, Mz, vz in ztim], -109.3)
    peri17 = [p_ for p_ in zres[17.0] if p_[1] < 200]; peri34 = [p_ for p_ in zres[34.0] if p_[1] < 200]
    ok6 = (len(peri17) >= 1 and abs(peri17[0][0] - 7.0) < 0.5 and 12 < peri17[0][1] < 35 and len(peri34) >= 1 and 30 < peri34[0][1] < 65
           and Mz_t is not None and 1.8e11 <= Mz_t <= 3.4e11)
    check("K6 CONTROL (literature, verified at the source): Zhao+2013's own two-body law (their eq. 1, Q-factor), nominal masses (V = 180 / "
          "225 km/s at a0 = 1.2e-10) and cosmological K-term reproduce their encounter (Table 1 line 1: 7.0 Gyr ago; b = 22-48 kpc for "
          "v_t = 17-34 km/s); run through this lane's strict-timing shooter (Hubble-flow birth, convention B) their law meets -109.3 km/s "
          "on the flyby branch at a mass inside their Table 1 range (1.8-3.35e11)",
          f"v_t = 17: encounter {peri17[0][0]:.2f} Gyr ago at {peri17[0][1]:.1f} kpc; v_t = 34: {peri34[0][0]:.2f} Gyr ago at "
          f"{peri34[0][1]:.1f} kpc; strict timing: " + ", ".join(f"M_b {Mz:.2e}: v_r {vz:+.1f}" for _, Mz, vz in ztim)
          + f" -> -109.3 at M_b = {Mz_t:.2e}" if (peri17 and peri34 and Mz_t) else "not reproduced", ok6,
          reading=("the machinery reproduces the MOND literature's flyby with the literature's inputs; the framework's inputs (a0, P2, "
                   "the separator) are what change the answer below") if ok6 else "the literature's flyby is NOT reproduced by this machinery")
    OUT["numbers"]["K6"] = dict(backward=OUT["numbers"].pop("K6_backward"), strict=[[list(c), m, v] for c, m, v in ztim], M_timing=Mz_t)
    P(f"    {el()}")

    # ============================================================================================= T timing
    banner("T  THE MW--M31 TIMING IN THE CHAIN'S TWO-BODY LAW: every branch through 0.78 Mpc today, both footings, conventions A / B / C")
    TS = {}
    for a_ in AT:
        cfg, out, dt = a_.get(); TS[cfg] = out
        P(f"    {cfg[0]} {cfg[1]:9s} M_b {cfg[2]:.3e}: " + " | ".join(f"{cv}: " + ", ".join(f"k={b['k']} {b['vr']:+.1f}" for b in br) for cv, br in out.items())
          + f"  [{dt:.0f}s]")
    OUT["numbers"]["timing_scan"] = {f"{c[0]}/{c[1]}/{c[2]:.3e}": o for c, o in TS.items()}
    TM = {}
    for law in ("HY", "P2"):
        for f in FOOTS:
            for conv in ("A", "B", "C_decay", "C_full"):
                for k in (0, 1):
                    pts = branch_pts(TS, law, f, conv, k)
                    if pts:
                        TM[(law, f, conv, k)] = dict(pts=pts, M=timing_mass(pts), M_lo=timing_mass(pts, VR_LG - EVR_LG), M_hi=timing_mass(pts, VR_LG + EVR_LG))
    for k_, v in TM.items():
        P(f"    timing: {k_[0]} {k_[1]:9s} {k_[2]:8s} k={k_[3]}: " + ", ".join(f"{m:.2e}:{vv:+.0f}" for m, vv in v["pts"])
          + f"  ->  M_b(-109.3) = {v['M']:.3e}" if v["M"] else f"    timing: {k_[0]} {k_[1]:9s} {k_[2]:8s} k={k_[3]}: " + ", ".join(f"{m:.2e}:{vv:+.0f}" for m, vv in v["pts"]) + "  ->  not bracketed")
    OUT["numbers"]["timing_mass"] = {"/".join(map(str, k_)): v for k_, v in TM.items()}
    inw = lambda m: m is not None and MB_LO <= m <= MB_HI
    t1 = {f: TM.get((SCORED, f, "A", 0), {}).get("M") for f in FOOTS}
    check(f"T1 THE CHAIN'S LAW NEEDS NO FLYBY: on the scored two-body law ({'plain P2, MUTATE' if MUTATE else '(H_Y)'}) the FIRST-APPROACH branch "
          "(no pericentre since the Hubble-flow birth) reaches -109.3 km/s at a baryonic mass inside the window on both footings (convention A)",
          ", ".join(f"{f}: M_b = {t1[f]:.3e}" if t1[f] else f"{f}: not in [{min(HY_M):.2e}, {max(P2_M):.1e}]" for f in FOOTS)
          + "; v_r at the nominal 1.75e11: " + ", ".join(f"{f}/{cv}: {dict(TM.get((SCORED, f, cv, 0), {}).get('pts', [])).get(1.75e11, float('nan')):+.1f}"
                                                         for f in FOOTS for cv in ("A", "B", "C_decay"))
          + f"; window [{MB_LO:.3e}, {MB_HI:.3e}]; +-4.4 km/s -> " + ", ".join(
              f"{f}: [{TM.get((SCORED, f, 'A', 0), {}).get('M_hi') or float('nan'):.2e}, {TM.get((SCORED, f, 'A', 0), {}).get('M_lo') or float('nan'):.2e}]" for f in FOOTS),
          all(inw(t1[f]) for f in FOOTS),
          reading="the separator switches the pair's MOND off early (the running yield, y_th ~ Omega_L^-4) and truncates it beyond ~2L(z) "
                  "(the band-pass); the matched orbit's history (switch-on, turnaround) is printed in section O")
    flyby_hy = {(f, cv): [(Mb, b["vr"]) for (lw, ff, Mb, _), o in TS.items() if lw == "HY" and ff == f and cv in o
                          for b in o[cv] if b["k"] >= 1 and b["vr"] < 0] for f in FOOTS for cv in ("A", "B")}
    maxM = max(c[2] for c in TS if c[0] == "HY")
    check("T2 THE CHAIN'S LAW EXCLUDES A PAST FLYBY: on (H_Y) no branch with a pericentre since birth passes 0.78 Mpc APPROACHING today for any "
          f"scanned M_b <= {maxM:.0e}, either footing, conventions A and B",
          "; ".join(f"{f}/{cv}: {v if v else 'none'}" for (f, cv), v in flyby_hy.items())
          + "; receding k>=1: " + ", ".join(f"{c[1]}/{cv}/{c[2]:.0e}: {b['vr']:+.0f}" for c, o in TS.items() if c[0] == "HY" for cv in o for b in o[cv] if b["k"] >= 1 and b["vr"] > 0),
          all(len(v) == 0 for v in flyby_hy.values()))
    t3 = {f"{f}/{cv}": TM.get(("HY", f, cv, 0), {}).get("M") for f in FOOTS for cv in ("B", "C_decay", "C_full")}
    check("T3 (reported) THE (H_Y) TIMING MASS UNDER THE OTHER CONVENTIONS: B (the smooth background's deceleration, Zhao+2013's K-term) and "
          "C (XR4's Newtonian carrier, decay / full): first-approach timing masses", ", ".join(f"{k_}: {v:.3e}" if v else f"{k_}: below/above scan"
                                                                                              for k_, v in t3.items()), True, load_bearing=False)
    p2k0 = {f: TM.get(("P2", f, "A", 0), {}) for f in FOOTS}; p2k1 = {(f, cv): TM.get(("P2", f, cv, 1), {}).get("M") for f in FOOTS for cv in ("A", "B")}
    p2_v_win = {f: [v for m, v in p2k0[f].get("pts", []) if MB_LO <= m <= MB_HI] for f in FOOTS}
    ok4 = all(not inw(p2k0[f].get("M")) for f in FOOTS) and all(v is None or v > MB_HI for v in p2k1.values()) and all(p2_v_win[f] and max(p2_v_win[f]) < VR_LG - EVR_LG for f in FOOTS)
    check("T4 THE PLAIN ROOT LAW (FP7's AQUAL root without FP9's separator) HAS NO TIMING SOLUTION AT THE LG'S BARYONIC MASS: its first "
          "approach is too fast at every mass in the window, and its flyby branch (second approach after a past pericentre) reaches -109.3 "
          "km/s only above the window (a mass the LG's baryons do not have)",
          "first approach in the window: " + "; ".join(f"{f}: {min(p2_v_win[f]):+.0f}..{max(p2_v_win[f]):+.0f} km/s" for f in FOOTS if p2_v_win[f])
          + "; flyby timing mass: " + ", ".join(f"{f}/{cv}: {v:.2e}" if v else f"{f}/{cv}: > {max(P2_M):.0e}" for (f, cv), v in p2k1.items()), ok4)
    OUT["numbers"]["T4"] = dict(first_in_window={f: p2_v_win[f] for f in FOOTS}, flyby_mass={f"{k_[0]}/{k_[1]}": v for k_, v in p2k1.items()})
    sens = {}
    for a_ in AV:
        var, v, dt = a_.get(); sens[var] = v
    base = [b["vr"] for b in TS[("HY", "canonical", 1.75e11, ("A", "B", "C_decay", "C_full"))]["A"] if b["k"] == 0 and b["vr"] < 0][0]
    slope = None
    pts_c = TM[("HY", "canonical", "A", 0)]["pts"]
    for (m1_, v1), (m2_, v2) in zip(pts_c[:-1], pts_c[1:]):
        if m1_ <= 1.75e11 <= m2_:
            slope = (v2 - v1) / math.log(m2_ / m1_)
    Mt5 = {k_: t1c * math.exp(-(v - base) / slope) for k_, v in sens.items()} if (slope and (t1c := TM.get(("HY", "canonical", "A", 0), {}).get("M"))) else {}
    check("T5 (reported) SENSITIVITY of the (H_Y) first-approach velocity at M_b = 1.75e11 (canonical): step count, force-table resolution, "
          "the start epoch of the Hubble flow, the softening, the mass split; the implied timing-mass shift uses dv/dlnM on the branch",
          f"baseline {base:+.2f} km/s; " + ", ".join(f"{k_}: {v - base:+.2f}" for k_, v in sens.items())
          + (f"; dv_r/dlnM = {slope:.1f} km/s -> largest timing-mass shift x{math.exp(max(abs(v - base) for v in sens.values()) / abs(slope)):.2f}" if slope else ""),
          True, load_bearing=False,
          reading=(f"implied canonical timing masses: " + ", ".join(f"{k_}: {Mt5[k_]:.2e}" for k_ in Mt5) + f"; all inside the window: {all(inw(v) for v in Mt5.values())}; "
                   f"largest mover: {max(sens, key=lambda k_: abs(sens[k_] - base))}") if Mt5 else "")
    OUT["numbers"]["T5"] = dict(base=base, variants=sens, slope=slope, implied_timing_mass=Mt5)
    P(f"    {el()}")

    # ============================================================================================= matched configurations
    banner("O / R  THE TIMING-MATCHED ORBITS AND THEIR DWARFS: 2-D orbits with v_t, the zero-velocity radius, the Hubble flow")
    MC = []
    for f in FOOTS:
        if TM.get(("HY", f, "A", 0), {}).get("M"):
            MC.append((f"HY/A/{f}", "HY", f, TM[("HY", f, "A", 0)]["M"], "A", 0, dict(tracers=True, orb2d=True)))
    if TM.get(("HY", "canonical", "B", 0), {}).get("M"):
        MC.append(("HY/B/canonical", "HY", "canonical", TM[("HY", "canonical", "B", 0)]["M"], "B", 0, dict(tracers=True)))
    if TM.get(("HY", "canonical", "C_decay", 0), {}).get("M"):
        MC.append(("HY/C_decay/canonical", "HY", "canonical", TM[("HY", "canonical", "C_decay", 0)]["M"], "C_decay", 0, dict(tracers=True, nrays=4)))
    if p2k1.get(("canonical", "A")):
        MC.append(("P2/A/canonical/flyby", "P2", "canonical", p2k1[("canonical", "A")], "A", 1, dict(tracers=True, orb2d=True, nrays=4)))
    if p2k1.get(("alt", "A")):
        MC.append(("P2/A/alt/flyby", "P2", "alt", p2k1[("alt", "A")], "A", 1, dict(tracers=True, nrays=4)))
    if p2k1.get(("canonical", "B")):
        MC.append(("P2/B/canonical/flyby", "P2", "canonical", p2k1[("canonical", "B")], "B", 1, dict(orb2d=True)))
    AM = [pool.apply_async(job_matched, (c,)) for c in MC]
    L25S = (0.6, 0.8, 1.0)
    AX = [pool.apply_async(job_lscan, ((L25, "canonical", (1.45e11, 2.1e11, 3.0e11, 4.2e11, 6.0e11)),)) for L25 in L25S]
    AE = [pool.apply_async(lgR0_efe, (TM[("HY", f, "A", 0)]["M"], A0[f], e)) for f in FOOTS for e in (0.0, 1e-4, 3e-4, 1e-3, 2e-3, 3e-3, 5e-3, 7e-3, 1e-2)
          if TM.get(("HY", f, "A", 0), {}).get("M")]
    MR = {}
    for a_ in AM:
        name, out, dt = a_.get(); MR[name] = out
        if "error" in out:
            P(f"    {name}: {out['error']}"); continue
        b = out["branch"]
        P(f"    {name}: M_b {[c for c in MC if c[0] == name][0][3]:.3e}, k = {b['k']}, v_r {b['vr']:+.1f} km/s at {b['d']:.4f} Mpc; d_max "
          f"{out['dmax']:.3f} Mpc at z = {out['z_dmax']:.2f} ({out['t_dmax_lookback']:.2f} Gyr ago); pericentres at z = "
          f"{[round(z, 2) for z in out['z_peri']]}; pair MOND > 10% of Newton from z = " + (f"{out['z_mond_on']:.2f}" if out['z_mond_on'] is not None else "never") + f"  [{dt:.0f}s]")
        for vt, o in out.get("orb2d", {}).items():
            P(f"        v_t = {vt}: past " + "; ".join(f"{e['kind']} {e['lookback_Gyr']:.2f} Gyr ago (z {e['z']:.2f}) at {e['d_kpc']:.0f} kpc" for e in o["past"])
              + f" | at a = 0.02: {o['d_at_a002_kpc']:.0f} kpc | future: " + "; ".join(f"{e['kind']} in {-e['lookback_Gyr']:.2f} Gyr at {e['d_kpc']:.0f} kpc" for e in o["future"]))
        if "R0" in out:
            r0 = out["R0"]
            P(f"        R0 per ray (cos theta = {', '.join(f'{c:+.2f}' for c in (RAYS_C if len(r0['rays']) == 8 else np.polynomial.legendre.leggauss(len(r0['rays']))[0]))}): "
              f"{', '.join(f'{x:.3f}' for x in r0['rays'])} Mpc; solid-angle mean {r0['mean']:.3f} ({math.log10(r0['mean'] / R0_MEAS):+.3f} dex)"
              + (f", |cos| <= 0.9: {r0['mean_valid']:.3f}; axis {r0['axis']:.3f}, perpendicular {r0['perp']:.3f}" if "axis" in r0 else "")
              + f"; merged pair {out['R0_merged']:.3f}")
    OUT["numbers"]["matched"] = {k_: {kk: vv for kk, vv in v.items() if kk != "hubble"} for k_, v in MR.items()}
    hy = {f: MR.get(f"HY/A/{f}", {}) for f in FOOTS}
    hyo = {f: hy[f].get("orb2d", {}) for f in FOOTS}
    close = [(f, vt, e["d_kpc"]) for f in FOOTS for vt, o in hyo[f].items() for e in o["past"] if e["kind"] == "peri" and e["d_kpc"] < 300]
    check("O1 (reported) THE (H_Y) ORBIT WITH THE MEASURED TANGENTIAL VELOCITIES (2-D, J conserved, from today at the timing mass): no close "
          "encounter in the past for v_t = 17 / 57 / 82 km/s; the last apocentre and the FIRST pericentre (in the future)",
          "; ".join(f"{f}/v_t {vt}: last apo " + ", ".join(f"{e['lookback_Gyr']:.1f} Gyr ago at {e['d_kpc']:.0f} kpc" for e in o["past"] if e["kind"] == "apo")[:60]
                    + " | first peri " + ", ".join(f"in {-e['lookback_Gyr']:.1f} Gyr at {e['d_kpc']:.0f} kpc" for e in o["future"] if e["kind"] == "peri")[:40]
                    for f in FOOTS for vt, o in hyo[f].items()) + f"; past pericentres < 300 kpc: {close if close else 'none'}",
          len(close) == 0 and all(hyo[f] for f in FOOTS), load_bearing=False,
          reading="separation at a = 0.02 when J is conserved back from today: " + ", ".join(f"{f[:3]}/v_t {vt}: {o['d_at_a002_kpc']:.0f} kpc" for f in FOOTS for vt, o in hyo[f].items())
                  + " vs the radial timing solution's " + ", ".join(f"{f[:3]} {hy[f]['branch']['ri_kpc']:.0f} kpc" for f in FOOTS if hy[f].get("branch"))
                  + " -- the measured J cannot be primordial: it was acquired after birth (tidal torques), the usual caveat of timing with J")
    fl = MR.get("P2/A/canonical/flyby", {}); flB = MR.get("P2/B/canonical/flyby", {})
    check("O2 (reported) THE PLAIN LAW'S FLYBY at its own timing mass (the only matched flyby): epoch and pericentre per v_t",
          "; ".join(f"{lab} v_t {vt}: " + ", ".join(f"peri {e['lookback_Gyr']:.2f} Gyr ago (z {e['z']:.2f}) at {e['d_kpc']:.0f} kpc" for e in o["past"] if e["kind"] == "peri")
                    for lab, src_ in (("A", fl), ("B", flB)) for vt, o in src_.get("orb2d", {}).items()), bool(fl.get("orb2d")), load_bearing=False,
          reading=(f"the matched flyby needs M_b = " + ", ".join(f"{cv}: {v:.2e} ({v / (mw_b + m31_b):.1f}x the nominal baryons)" for (f_, cv), v in p2k1.items() if v and f_ == "canonical")
                   + "; Zhao+2013 quote 7-11 Gyr ago and < 55 kpc for their law and masses"))
    # R1
    r1 = {k_: MR[k_]["R0"]["mean"] for k_ in ("HY/A/canonical", "HY/A/alt", "HY/B/canonical") if k_ in MR and "R0" in MR[k_]}
    edge = R0_MEAS * 10 ** BAND
    check("R1 THE TIMING-MATCHED LOCAL GROUP STILL OVERSHOOTS R0: with the pair on its timing-matched (H_Y) orbit and the dwarfs integrated from "
          "the Hubble flow through the two-body field, the solid-angle-mean zero-velocity radius lies above the +0.10 dex band on both "
          "footings (A) and in convention B -- a verified FAIL of the chain's Local Group",
          "; ".join(f"{k_}: {v:.3f} Mpc ({math.log10(v / R0_MEAS):+.3f} dex)" for k_, v in r1.items()) + f"; band edge {edge:.3f}; measured {R0_MEAS} +- {R0_ERR}",
          len(r1) >= 3 and all(v > edge for v in r1.values()),
          reading=(f"the timing pins the pair's MOND strength (M_b a0 at fixed v_r) and the same strength sets the outer flow: the two footings' "
                   f"timing-matched R0 differ by {abs(math.log10(r1['HY/A/canonical'] / r1['HY/A/alt'])):.3f} dex while their masses differ by "
                   f"{abs(math.log10(t1['canonical'] / t1['alt'])):.3f} dex") if ("HY/A/canonical" in r1 and "HY/A/alt" in r1 and t1.get("canonical") and t1.get("alt")) else "")
    r2 = {f: (hy[f]["R0"]["mean"] / hy[f]["R0_merged"] - 1, hy[f]["R0"]["axis"], hy[f]["R0"]["perp"]) for f in FOOTS if "R0" in hy[f]}
    check("R2 (reported) THE TWO-BODY GEOMETRY vs THE MERGED PAIR at the same mass, and the anisotropy of the zero-velocity surface",
          "; ".join(f"{f}: two-body/merged - 1 = {v[0]:+.3f}; along the axis {v[1]:.3f}, perpendicular {v[2]:.3f} Mpc" for f, v in r2.items())
          + f"; FP9's merged value at its 1.145e11: {ref9['canonical']:.3f}/{ref9['alt']:.3f}", True, load_bearing=False)
    # R3
    flx = {f: MR.get(f"P2/A/{f}/flyby", {}) for f in FOOTS}
    flr = {f: (v["R0"]["mean"], v["R0_merged"], v["R0"]["rays"]) for f, v in flx.items() if "R0" in v and v.get("R0_merged")}
    fl_R0 = flr.get("canonical", (None,))[0]
    check("R3 THE FLYBY DOES NOT RESCUE R0: in the only law where a flyby matches the timing (the plain root law, at its flyby timing mass) "
          "the dwarfs' zero-velocity radius lies above the band on both footings, and the flyby's own dynamical effect (two-body with the "
          "pericentre passage vs the merged pair at the same mass) is smaller than the overshoot",
          "; ".join(f"{f}: flyby at M_b = {p2k1[(f, 'A')]:.3e}: R0 {v[0]:.3f} Mpc ({math.log10(v[0] / R0_MEAS):+.3f} dex), merged {v[1]:.3f}, flyby effect "
                    f"{v[0] / v[1] - 1:+.3f}; rays {', '.join(f'{x:.2f}' for x in v[2])}" for f, v in flr.items()) if flr else "no flyby configuration computed",
          len(flr) == 2 and all(v[0] > edge and abs(math.log10(v[0] / v[1])) < math.log10(v[0] / R0_MEAS) for v in flr.values()))
    # R4 the Hubble diagram
    banner("D  THE HUBBLE DIAGRAM: the model's dwarfs against the committed UNGC (same estimator), and the high-velocity galaxies")
    rows = {}
    for f31, dd in DAT.items():
        sel = np.isfinite(dd["R"]) & np.isfinite(dd["Vr"]) & (dd["R"] > 0.7) & (dd["R"] < 3.0)
        s_acc = sel & np.isin(dd["fD"], ACC_DIST) & ~(np.isin(dd["MD"], OTHER_GROUPS) & (dd["Ti"] > 0))
        rows[f31] = dict(all=lin_fit(dd["R"][sel], dd["Vr"][sel]), lg=lin_fit(dd["R"][s_acc], dd["Vr"][s_acc]))
        P(f"    UNGC, barycentre at {f31:.2f} of the way to M31: all {rows[f31]['all']['n']}: R0 {rows[f31]['all']['R0']:.3f} Mpc, H {rows[f31]['all']['H']:.0f}, "
          f"rms {rows[f31]['all']['rms']:.0f} km/s | accurate distances, other groups' members excluded ({rows[f31]['lg']['n']}): R0 "
          f"{rows[f31]['lg']['R0']:.3f}, H {rows[f31]['lg']['H']:.0f}, rms {rows[f31]['lg']['rms']:.0f}")
    OUT["numbers"]["UNGC_fit"] = {f"{k_:.3f}": v for k_, v in rows.items()}
    dd = DAT[0.63]; sel = np.isfinite(dd["R"]) & np.isfinite(dd["Vr"]) & (dd["R"] > 0.7) & (dd["R"] < 3.0) & np.isin(dd["fD"], ACC_DIST) \
        & ~(np.isin(dd["MD"], OTHER_GROUPS) & (dd["Ti"] > 0))
    mock = {}
    for f in FOOTS:
        hb = MR.get(f"HY/A/{f}", {}).get("hubble")
        if not hb: continue
        Rm, Vm, Wm = np.array(hb["R"]), np.array(hb["V"]), np.array(hb["W"])
        fitm = lin_fit(Rm, Vm, Wm)
        bins = np.array([0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.2, 2.5, 3.0])
        mv = np.array([np.sum(Wm[(Rm >= a) & (Rm < b_)] * Vm[(Rm >= a) & (Rm < b_)]) / np.sum(Wm[(Rm >= a) & (Rm < b_)])
                       if np.sum(Wm[(Rm >= a) & (Rm < b_)]) > 0 else np.nan for a, b_ in zip(bins[:-1], bins[1:])])
        bc = 0.5 * (bins[1:] + bins[:-1]); okb = np.isfinite(mv); bc, mv = bc[okb], mv[okb]
        model_at = np.interp(dd["R"][sel], bc, mv)
        res = dd["Vr"][sel] - model_at
        hvg = {n_: float(dd["Vr"][i] - np.interp(dd["R"][i], bc, mv)) for i, n_ in enumerate(dd["name"]) if n_ in HVG_BZ}
        mid = (dd["R"][sel] > 1.2) & (dd["R"][sel] < 2.5)
        mock[f] = dict(fit=fitm, curve=dict(R=bc.tolist(), V=mv.tolist()), data_minus_model_mean=float(np.mean(res)), data_minus_model_rms=float(np.std(res)),
                       n=int(sel.sum()), hvg_minus_model=hvg, n_12_25=int(mid.sum()), frac_above_12_25=float(np.mean(res[mid] > 0)) if mid.any() else float("nan"),
                       median_excess_12_25=float(np.median(res[mid])) if mid.any() else float("nan"))
        P(f"    model ({f}, (H_Y) timing-matched, mass-weighted dwarfs): linear fit 0.7-3 Mpc R0 {fitm['R0']:.3f}, H {fitm['H']:.0f}, rms {fitm['rms']:.0f} "
          f"km/s; mean v_r(R) at R = {', '.join(f'{r_:.1f}' for r_ in bc)}: {', '.join(f'{v_:+.0f}' for v_ in mv)} km/s")
        P(f"      UNGC (accurate, LG flow; {sel.sum()} galaxies) minus the model's mean flow: mean {np.mean(res):+.0f} km/s, rms {np.std(res):.0f}; "
          f"Banik & Zhao's HVGs minus the model: " + ", ".join(f"{k_} {v:+.0f}" for k_, v in hvg.items()))
    for f in FOOTS:                                                              # the plain law's matched flyby (the only flyby model)
        hb = MR.get(f"P2/A/{f}/flyby", {}).get("hubble")
        if not hb: continue
        Rm, Vm, Wm = np.array(hb["R"]), np.array(hb["V"]), np.array(hb["W"])
        bins = np.array([0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.2, 2.5, 3.0])
        mv = np.array([np.sum(Wm[(Rm >= a) & (Rm < b_)] * Vm[(Rm >= a) & (Rm < b_)]) / np.sum(Wm[(Rm >= a) & (Rm < b_)])
                       if np.sum(Wm[(Rm >= a) & (Rm < b_)]) > 0 else np.nan for a, b_ in zip(bins[:-1], bins[1:])])
        bc = 0.5 * (bins[1:] + bins[:-1]); okb = np.isfinite(mv); bc, mv = bc[okb], mv[okb]
        res = dd["Vr"][sel] - np.interp(dd["R"][sel], bc, mv); fitm = lin_fit(Rm, Vm, Wm)
        mock[f"flyby/{f}"] = dict(fit=fitm, curve=dict(R=bc.tolist(), V=mv.tolist()), data_minus_model_mean=float(np.mean(res)), data_minus_model_rms=float(np.std(res)))
        P(f"    plain-law flyby model ({f}): " + (f"linear fit R0 {fitm['R0']:.3f}, H {fitm['H']:.0f}, rms {fitm['rms']:.0f} km/s" if fitm["H"] > 0 else
                                               f"no linear outflow over 0.7-3 Mpc (fitted slope {fitm['H']:.0f} km/s/Mpc: the region is falling in)") + "; mean v_r(R) at R = "
          f"{', '.join(f'{r_:.1f}' for r_ in bc)}: {', '.join(f'{v_:+.0f}' for v_ in mv)}; UNGC minus model: mean {np.mean(res):+.0f}, rms {np.std(res):.0f} km/s")
    OUT["numbers"]["hubble_mock"] = mock
    check("R4 (reported) THE HUBBLE DIAGRAM, same estimator: the linear-flow fit over 0.7-3 Mpc on the model's mass-weighted dwarfs vs the "
          "committed UNGC in the same barycentric frame; the data minus the model's mean flow; the high-velocity galaxies (Banik & Zhao 2018) "
          "relative to the model", "; ".join(f"{f}: " + (f"model fit R0 {m['fit']['R0']:.2f}" if m["fit"]["H"] > 0 else "model: no outflow (H < 0)")
                                               + f" (UNGC {rows[0.63]['lg']['R0']:.2f}, published 0.96), data - model "
                                               f"{m['data_minus_model_mean']:+.0f} +- {m['data_minus_model_rms']:.0f} km/s" for f, m in mock.items()), True, load_bearing=False,
          reading="; ".join(f"{f}: {m['frac_above_12_25']:.0%} of the {m['n_12_25']} UNGC galaxies at 1.2-2.5 Mpc recede faster than the model's mean flow "
                            f"(median excess {m['median_excess_12_25']:+.0f} km/s)" for f, m in mock.items() if "frac_above_12_25" in m))

    # ============================================================================================= P the pincer
    banner("P  THE KiDS-LG PINCER AT THE TIMING MASS")
    efe = {}
    i = 0
    for f in FOOTS:
        if not TM.get(("HY", f, "A", 0), {}).get("M"): continue
        es = (0.0, 1e-4, 3e-4, 1e-3, 2e-3, 3e-3, 5e-3, 7e-3, 1e-2); Rs = []
        for e in es:
            Rs.append(AE[i].get()); i += 1
        el_ = np.log10(es[1:]); Rl = np.log10(Rs[1:])
        need = {t_: float(10 ** np.interp(math.log10(t_), Rl[::-1], el_[::-1])) if min(Rs) <= t_ <= max(Rs) else float("nan") for t_ in (R0_MEAS, edge)}
        efe[f] = dict(R0_of_e=list(zip(es, Rs)), e_needed=need[R0_MEAS], e_band_edge=need[edge], KiDS_2h=F1[f]["e_KiDS_2h"], KiDS_no2h=F1[f]["e_KiDS_no2h"],
                      FP1_e_LG_1145=F1[f]["e_LG"], FP1_e_LG_172=F1[f]["e_LG_Mb172"])
        P(f"    {f}: (H_Y) merged LG at the timing mass {TM[('HY', f, 'A', 0)]['M']:.3e}: R0(e) " + ", ".join(f"{e:.0e}:{R_:.3f}" for e, R_ in zip(es, Rs))
          + f" -> R0 = 0.96 needs e = {need[R0_MEAS]:.2e} a0, the band edge {need[edge]:.2e} a0 (counterfactual: e reaches the kernel un-band-passed); "
          f"KiDS tolerates {F1[f]['e_KiDS_no2h']:.1e} (no 2-halo) / {F1[f]['e_KiDS_2h']:.1e} (2-halo) [FP1 E3]; FP1's core needed {F1[f]['e_LG']:.1e} at 1.145e11, "
          f"{F1[f]['e_LG_Mb172']:.1e} at 1.72e11")
    OUT["numbers"]["P1"] = efe
    check("P1 THE PINCER IS NOT RELIEVED: at the (H_Y) timing mass the uniform field the LG would need in the kernel's argument to reach "
          "R0 = 0.96 (even if it bypassed the band-pass) exceeds what KiDS's isolated lenses tolerate (FP1 E3, 2-halo), on both footings; "
          "and the band-pass passes no uniform field (h(k = 0) = 0), so in (H_Y) no external field can act at all (95% of the web's rms "
          "field is > 60 Mpc bulk flow, FP1 E5)", "; ".join(f"{f}: needs {v['e_needed']:.1e} a0 (band edge {v['e_band_edge']:.1e}) vs KiDS "
                                                                          f"<= {v['KiDS_2h']:.1e} -> {v['e_needed'] / v['KiDS_2h']:.1f}x (band edge {v['e_band_edge'] / v['KiDS_2h']:.1f}x)" for f, v in efe.items()),
          len(efe) == 2 and all(v["e_needed"] > v["KiDS_2h"] for v in efe.values()))

    # ============================================================================================= X the band-pass length, LG-internal
    banner("X  THE LG ALONE: with the timing imposed, which band-pass length would give R0 = 0.96?  (yield and n unchanged; KiDS needs L(0.25) >= ~1.2 Mpc, FP9 I5)")
    XS = {}
    for a_ in AX:
        (L25, f, _), pts, Mt, R0x, L0, dt = a_.get(); XS[(L25, f)] = dict(pts=pts, M=Mt, R0=R0x, L0=L0)
        P(f"    L(0.25) = {L25} Mpc ({f}): first approach " + ", ".join(f"{m:.2e}:{v:+.0f}" for m, v in pts)
          + (f" -> timing mass {Mt:.3e} ({'inside' if inw(Mt) else 'OUTSIDE'} the window), merged R0 at it {R0x:.3f} Mpc" if Mt else " -> no timing mass <= 6e11") + f"  [{dt:.0f}s]")
    for f in FOOTS:
        if TM.get(("HY", f, "A", 0), {}).get("M"):
            XS[(1.3, f)] = dict(M=TM[("HY", f, "A", 0)]["M"], R0=MR.get(f"HY/A/{f}", {}).get("R0_merged"), pts=TM[("HY", f, "A", 0)]["pts"], L0=L_LAMBDA * LG_OmL(1.0))
    OUT["numbers"]["X1"] = {f"{k_[0]}/{k_[1]}": v for k_, v in XS.items()}
    ok_x = {f: [L25 for L25 in (0.6, 0.8, 1.0, 1.3) if XS.get((L25, f), {}).get("M") and inw(XS[(L25, f)]["M"]) and (XS[(L25, f)]["R0"] or 9) <= edge] for f in FOOTS}
    check("X1 (reported) THE LG-INTERNAL TEST OF THE BAND-PASS LENGTH: with the MW-M31 timing imposed (first approach, conv. A), the timing mass "
          "and the merged-pair zero-velocity radius at it as L(0.25) is lowered from FP9's 1.3 Mpc (a shorter band-pass cuts the pair's mutual "
          "MOND as well as the outer flow's); which lengths satisfy timing (mass in the window) AND R0 within the +0.10 dex band; KiDS's floor "
          "is L(0.25) >~ 1.2 Mpc",
          "; ".join(f"L25 {k_[0]}/{k_[1][:3]}: M_t {v['M']:.2e}, R0 {v['R0']:.3f}" if v.get("M") and v.get("R0") else f"L25 {k_[0]}/{k_[1][:3]}: no timing mass"
                    for k_, v in sorted(XS.items())) + "; lengths passing both: " + ", ".join(f"{f}: {ok_x[f] if ok_x[f] else 'none'}" for f in FOOTS),
          True, load_bearing=False)

    # ============================================================================================= G gates
    banner("G  THE OTHER GATES")
    check("G1 THE OTHER GATES ARE UNCHANGED: this lane adds no term to the action -- the two-body force, the flyby test and the dwarfs use "
          "FP9's four constants as committed -- so the flagship, SPARC, KiDS (and sigma_8, the forest proxy) are FP9's numbers (K7 reproduces "
          "them exactly); the timing solution needs no new term, and nothing that would move the LG's R0 was added",
          f"flagship {min(flag.values()):+.4f}..{max(flag.values()):+.4f} dex, SPARC {max(sparc.values()):.1e} dex, KiDS {kids['canonical']:+.1f}/{kids['alt']:+.1f} "
          f"(FP9 H2); new action terms: 0", d7 < 1e-9)
    pool.close(); pool.join()

    # ============================================================================================= W ledger
    banner("W  THE LEDGER: FP11, the Local Group's flyby branch in the chain's own two-body law")
    tmc, tma = t1.get("canonical"), t1.get("alt")
    hy_t = {f: TM.get(("HY", f, "A", 0), {}).get("M") for f in FOOTS}
    apo = []                                                                     # the most recent apocentre of each (H_Y) 2-D orbit
    for f in FOOTS:
        for o in hyo[f].values():
            al = [e for e in o["past"] if e["kind"] == "apo"]
            if al:
                e0 = min(al, key=lambda e: e["lookback_Gyr"]); apo.append((e0["d_kpc"], e0["lookback_Gyr"]))
    fperi = [(-e["lookback_Gyr"], e["d_kpc"]) for f in FOOTS for o in hyo[f].values() for e in o["future"] if e["kind"] == "peri"]
    rng = lambda xs, fmt: (f"{min(xs):{fmt}}-{max(xs):{fmt}}" if xs else "n/a")
    s_apo = f"the last apocentre {rng([a for a, _ in apo], '.0f')} kpc, {rng([b for _, b in apo], '.1f')} Gyr ago" if apo else "no apocentre found"
    s_fp = f"the first pericentre {rng([a for a, _ in fperi], '.1f')} Gyr ahead at {rng([b for _, b in fperi], '.0f')} kpc" if fperi else "no future pericentre in 8 Gyr"
    fly_x = [v / (mw_b + m31_b) for v in p2k1.values() if v]
    s_fly = (f"the plain law's flyby needs M_b = {rng([v for v in p2k1.values() if v], '.2e')} = {rng(fly_x, '.1f')}x the nominal baryons" if fly_x
             else "the plain law has no matched flyby up to the scanned masses")
    en = [v["e_needed"] for v in efe.values()]; ek = [v["KiDS_2h"] for v in efe.values()]
    s_pin = (f"the LG would need e = {rng(en, '.1e')} a0 in the kernel; KiDS tolerates <= {rng(ek, '.1e')} (2-halo)" if en else "not computed")
    r1s = ", ".join(f"{k_} {v:.2f}" for k_, v in r1.items())
    LEDGER = [
        ("F11a", "the MW-M31 two-body force of the chain's static law (FP7 root, FP9 H_Y): Newton + each body's isolated band-passed "
                 "phantom + the interaction field P(1 - S_L)[X(g1 + g2) - X(g1) - X(g2)]", "DERIVED",
         "K3: kernel = FP6's phantom, momentum conserved, deep limit = Milgrom's two-body formula, test-particle limit; K4 multipoles"),
        ("F11b", "(H_Y) switches the pair's MOND off at early times (running yield) and truncates it beyond ~2L(z) (band-pass); the pair "
                 "coasts until the MOND switch-on", "DERIVED", "the force tables (T) and the matched orbits (O); XR13's 'Newtonian pair' and "
                 "'M*' bracket this law"),
        ("F11c", (f"the timing: (H_Y) reaches -109.3 km/s on the FIRST approach at M_b = {tmc:.2e} / {tma:.2e} (can/alt, conv. A), inside the "
                  "baryonic window: a flyby is NOT required") if (tmc and tma) else "the timing on the scored law: no first-approach solution in the window",
         "DERIVED" if (tmc and tma and all(inw(v) for v in (tmc, tma))) else "FAILS", "T1 (conv. A = the chain's point masses + Lambda from the "
         "Hubble flow; B and C in T3; sensitivity T5)"),
        ("F11d", f"a past MW-M31 flyby is EXCLUDED by (H_Y): no approaching branch with a past pericentre for M_b <= {maxM:.0e}; with v_t = "
                 f"17-82 km/s {s_apo}; {s_fp}", "DERIVED" if all(len(v) == 0 for v in flyby_hy.values()) else "FAILS", "T2, O1 (2-D, J conserved from today)"),
        ("F11e", f"the plain root law (no separator) has no timing solution at the LG's baryonic mass: its first approach is too fast; {s_fly}; "
                 "the MOND-literature flyby (Zhao+2013) is reproduced with a0 = 1.2e-10 and their interpolation", "FAILS", "T4, K6, O2"),
        ("F11f", "dynamical friction and flyby energy loss set to zero (no halos in the galaxy sector; the (H_Y) orbit has no past pericentre)",
         "POSTULATED", "scope; stellar friction at the future pericentre is not computed"),
        ("F11g", "the timing idealisation: point masses from the Hubble flow at a = 0.02 (the chain's XR4 convention), J treated as "
                 "conserved from today", "POSTULATED", "T3 / T5 measure how far the background term, the carrier and the start epoch move it"),
        ("F11h", f"R0 at the timing-matched mass: {r1s} Mpc vs 0.96 +- 0.03 -- the timing pins M_b a0, and with it R0", "FAILS", "R1, R2, R4"),
        ("F11i", "a flyby does not resolve the R0 overshoot: none exists in (H_Y), and the only matched flyby (the plain law, at its larger "
                 "timing mass) has a larger R0; the flyby's own effect on R0 is small", "FAILS", "R3"),
        ("F11j", f"the KiDS-LG pincer at the timing mass: {s_pin}; (H_Y)'s band-pass passes no uniform field", "CONSTRAINT", "P1 (FP1 E3's "
                 "tolerances, committed)"),
        ("F11k", "the flagship, SPARC, KiDS (and sigma_8, forest) gates are unchanged -- no action term was added", "DERIVED", "G1, K7"),
        ("F11l", "the LG alone, timing imposed: lengths L(0.25) passing timing + R0: " + ", ".join(f"{f}: {ok_x[f] if ok_x[f] else 'none'}" for f in FOOTS)
                 + " (canonical scan 0.6-1.3 Mpc, alt at 1.3); KiDS needs L(0.25) >= ~1.2 Mpc", "CONSTRAINT" if any(ok_x.values()) else "FAILS",
         "X1 (merged pair; yield, n unchanged)"),
        ("F11m", "open: the AQUAL-vs-QUMOND curl part of the two-body force (near pericentre only), the neighbours' tidal field (M81, Cen A, "
                 "IC 342), the CGM's baryons (raise M_b, R0 and the timing speed), a 3-D fit of the full local Hubble flow, and an LG-scale "
                 "action term that separates the pair's mutual MOND (fixed by the timing) from the outer flow (R0)", "OPEN", "scope; not computed here"),
    ]
    for k_, what, status, why in LEDGER:
        P(f"    {k_:5s} {status:11s} {what}  --  {why}")
    OUT["ledger"] = [dict(link=k_, what=w, status=s_, basis=b_) for k_, w, s_, b_ in LEDGER]
    check("W (reported) the ledger of this lane", f"{len(LEDGER)} links", True, load_bearing=False)

    # ============================================================================================= verdict
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    banner("VERDICT")
    P(f"  The unscored branch, scored in the chain's own law (FP7 root + FP9's (H_Y), both footings; convention A unless stated):")
    P(f"  (1) ORBITS.  On (H_Y) the first approach reaches -109.3 km/s at M_b = " + (f"{hy_t['canonical']:.2e} / {hy_t['alt']:.2e}" if all(hy_t.values()) else "(none)")
      + f" (can/alt; window [{MB_LO:.2e}, {MB_HI:.2e}]):")
    P(f"      a flyby is " + ("NOT required" if all(inw(v) for v in hy_t.values()) else "not avoided") + ", and " + ("no" if all(len(v) == 0 for v in flyby_hy.values()) else "a")
      + f" flyby branch exists up to M_b = {maxM:.0e}.  With v_t = 17-82 km/s: {s_apo}; {s_fp}.")
    P(f"      The MOND literature's flyby (Zhao+2013; K6 " + ("reproduces it" if ok6 else "does NOT reproduce it") + f") is the unseparated law's: {s_fly}.")
    P(f"  (2) DWARFS.  Timing-matched R0: {r1s} Mpc vs 0.96 +- 0.03 (band edge {edge:.2f}): the timing is resolved, the R0 overshoot is "
      + ("NOT" if all(v > edge for v in r1.values()) else "partly") + ";")
    P(f"      a flyby cannot help (none exists in (H_Y)" + ("; the plain law's matched flyby gives R0 = " + " / ".join(f"{v[0]:.2f}" for v in flr.values())
      + " Mpc (" + "/".join(flr) + f"), the flyby itself moving R0 by " + " / ".join(f"{v[0] / v[1] - 1:+.3f}" for v in flr.values()) if flr else "") + ").")
    P(f"  (3) PINCER.  {s_pin}; (H_Y)'s band-pass passes no uniform field.")
    P(f"  (4) THE LG ALONE (canonical, timing imposed): " + "; ".join(f"L(0.25) = {L25}: " + (f"timing mass {XS[(L25, 'canonical')]['M']:.2e}, R0 {XS[(L25, 'canonical')]['R0']:.2f}"
                                                                         if XS.get((L25, "canonical"), {}).get("M") else "no timing mass <= 6e11")
                                                          for L25 in (0.6, 0.8, 1.0, 1.3) if (L25, "canonical") in XS)
      + f" -- lengths passing timing + R0: {ok_x['canonical'] if ok_x['canonical'] else 'none'} (KiDS needs >= ~1.2).")
    P(f"  (5) GATES.  Flagship, SPARC, KiDS unchanged (no action term added).  Not 'closed'.  Time {time.time() - T0:.0f} s.")
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
    P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}")
    sys.exit(0 if nlb == 0 else 1)


if __name__ == "__main__":
    main()
