#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP12 -- THE ZERO-VELOCITY RADIUS R0 OF THE LOCAL VOLUME GROUPS: is the Local Group's R0 overshoot universal (the law's outer
profile) or the Local Group's own (its environment)?

WHY.  FP11 closed the Local Group's (LG) timing with baryons only on the first approach, but its zero-velocity radius still
overshoots: R0 = 1.53 / 1.52 Mpc (can/alt; timing-matched, two-body) against 0.96 +- 0.03 (+0.20 dex).  The timing fixes
M_b a0, which sets R0, so the footings agree; shortening the band-pass kills the timing (FP11 X1).  One system cannot say
WHY.  If every nearby group overshoots by ~0.2 dex the fault is the law's OUTER profile (g << a0 at 0.3-1.5 Mpc, where the
band-pass and the kernel's deep-MOND tail act); if only the LG does, it is the LG's environment.  This lane computes R0 in the
chain's own law for the four groups the record's k02 lane measured from the UNGC -- M81, Cen A, M83, IC 342 -- confronts
them with the published zero-velocity radii (each checked at its source for this lane), and decides.

THE LAW (nothing added to the action).  FP7's AQUAL root with FP9's separator (H_Y) and FP9's four declared constants,
unchanged: L_Lambda = 2.46 Mpc, n = 2, y_Lambda = 7.78e-8, p' = 4.  An isolated group is a merged point mass at the centre of
its own Hubble flow (the XR4 / FP9 / FP11 convention: the dwarfs start on the Hubble flow at a = 0.02, point masses + Lambda);
its dwarfs are test particles in the static (H_Y) field: FP6's band-passed phantom with FP9's yield.  FP11's tracer machinery
(PairField merged + R0_rays: dwarfs integrated from the Hubble flow through the group's field) and FP6's shell integrator
(lg_R0 = FP11's lgR0_efe at e = 0) are the same computation (K5); the fast one carries the variants.  A binary group's two-body
geometry moves R0 by +0.016 (FP11 R2, the LG pair at 0.78 Mpc); no neighbour tides.

INPUTS (each read at its source for this lane; none quoted from memory).
  Zero-velocity radii R0 [Mpc]:
    Local Group    0.96 +- 0.03   Karachentsev et al. 2009, MNRAS 393, 1265 (FP11's reference, checked there)
                   0.94 +- 0.10   Karachentsev 2005, AJ 129, 178 (arXiv:astro-ph/0410065v1), Table 11, column "M.Way/M31"
                   0.91 +- 0.05   Kashibadze & Karachentsev 2018, A&A 609, A11 (arXiv:1709.09420v2), abstract and Sect. 4
    M81 group      0.89 +- 0.05   Karachentsev & Kashibadze 2006, Astrophysics 49, 3 (arXiv:astro-ph/0509207), abstract
                   1.05 +- 0.07   Karachentsev 2005, Table 11, "M81/N2403"
    Cen A group    1.40 +- 0.11   Karachentsev et al. 2007, AJ 133, 504 (arXiv:astro-ph/0603091), abstract
                   1.26 +- 0.15   Karachentsev 2005, Table 11, "CenA/M83"
    M83 group      none           no separate published R0 was found: K05 fits Cen A and M83 as one complex, and K+2007's
                                  abstract gives M83 only an orbital/virial mass; the record's k02 UNGC fit (0.49 +- 1.38) is
                                  not a measurement (S1) -> UNSCORED; its model R0 is stated as a prediction
    IC 342 group   0.90 +- 0.10   Karachentsev 2005, Table 11, "IC342/Maff"
    14-group stack 0.93 +- 0.02   Kashibadze & Karachentsev 2018, Table 8 (barycentre, minor attractor; their eq. 14 fit,
                                  V = H R [1 - (R0/R)^(1/2)]); the same table spans 0.71-1.03 over centre / infall models; the
                                  same paper's LG (same method): 0.91 +- 0.05
  Baryonic masses: the record's k02 inputs, re-derived here from the committed UNGC (Karachentsev+2013,
    real_research/data/ungc_karachentsev2013.tsv): 0.6 L_K + 1.33 M_HI of every catalogue galaxy inside k02's measured R0
    (the Milky Way's stars 6.1e10, k02's value).  Band: Upsilon_K in {0.5, 0.6, 1.0} (K&K 2018's stellar masses equal L_K,
    K8), aperture 0.7-1.5 Mpc (0.8 for IC 342, which keeps Maffei 1/2, as K05's "IC342/Maff" complex does), and x1.4 at the
    top for unseen warm/hot gas (FP11's LG window, 2.4e11 / 1.75e11).  The LG: FP11's timing masses 1.652e11 / 1.367e11
    (can/alt).  The stack: K&K 2018 Table 6 (stellar masses of the two leading galaxies per group) weighted by Table 7's
    companion counts (66 galaxies around 11 groups), converted to Upsilon_K = 0.6 with K8's implied Upsilon.

CHECKS (the decision rule is declared here, before any number is computed).
  RULE.  A system's overshoot is delta = log10(R0_model / R0_measured), R0_model the model's true zero-velocity radius at the
  nominal baryonic mass (the LG: FP11's timing-matched two-body R0).  It OVERSHOOTS if delta > +0.10 dex on both footings
  (the chain's band, XR4 / FP11); it FITS if |delta| <= 0.10 on both.  Scored: the LG, M81, Cen A, IC 342 (M83 has no
  published R0).  UNIVERSAL = the LG and every scored external group overshoot; LG-ONLY = the LG overshoots and every scored
  external group fits; MIXED = anything else.  Primary set: the first R0 listed per group; robustness: K05's homogeneous set,
  the model's own linear-fit and eq.-14 estimators, the mass-band edges, and LG-relative offsets (estimator-cancelling).
  K1 CONTROL: FP9's LG R0 at the (H_Y) headline cell (1.4104 / 1.4532) with FP6's lg_both and with this lane's law function.
  K2 CONTROL: FP11's LG R0 re-run with FP11's own job at its timing masses: two-body 1.5297 / 1.5222, merged 1.5054 / 1.5003.
  K3 CONTROL: FP11's P1 merged R0 at the timing mass (1.50543 / 1.49970) with this lane's law function.
  K4 CONTROL: k02's measured R0 (+- bootstrap) and baryonic masses re-derived exactly from the committed UNGC (5 groups).
  K5 CONTROL: FP11's tracer machinery (PairField merged + R0_rays) = the shell integrator per group, both footings (<= 3e-3).
  K6 CONTROL: the plain-P2 root law's merged LG R0 at 1.145e11 reproduces FP1 E3 (1.9246 / 2.0179): the MUTATE law.
  K7 CONTROL: FP9's gate numbers (flagship, SPARC, KiDS) reproduced exactly: the constants used here are FP9's.
  K8 (reported) K&K 2018's stellar masses against the UNGC's L_K (the implied Upsilon_K).
  K9 CONTROL: FP11's force table + first-approach shooter at FP11's timing mass return FP11's -109.27 / -109.21 km/s.
  S1 (reported) the record's UNGC R0 of the external groups are not measurements: k02's own estimator moves by more than its
     bootstrap error under window / distance-quality changes (the record's XR4 N2 and k_dimensional K3.2 found the same).
  M1 (reported) the baryonic masses and their band.   R1 (reported) the model's R0 per group, both footings, three estimators.
  V1 [load-bearing] NOT LG-ONLY: M81 and IC 342 overshoot on both footings (primary set), and so does the 14-group stack.
  V2 [load-bearing; MUTATE must fail] CEN A FITS: |delta| <= 0.10 on both footings, with and without M83's baryons.
  V3 (reported) the verdict by the rule, and its robustness.   V4 (reported) mean and scatter of delta; common-offset chi^2;
     LG-relative offsets.   V5 (reported) the stack and the LG in one paper, one estimator (K&K 2018).
  U1 [load-bearing] THE CHAIN'S OWN KNOBS CANNOT DO THE UNIVERSAL FIX: the band-pass length L(0.25) or the yield y_th(0.25)
     that brings the typical group to its measured R0 costs KiDS d chi^2 > +9 on both footings.
  U2 (reported) the required outer-profile change: the factor f on the phantom beyond 0.3 Mpc, or the switch-on epoch z_on;
     its KiDS cost; SPARC outskirts at the actual outermost SPARC radii; the LG timing under it (the internal pincer).
  U3 [load-bearing] NO UNIVERSAL OUTER PROFILE FITS CEN A AND THE REST: the f each needs does not overlap.
  E1 (reported) the environment: what could separate Cen A from the others.   G1 THE OTHER GATES ARE UNCHANGED.   W the ledger.
MUTATE=1 scores the unseparated law (FP7's plain P2 root: no band-pass, no yield) instead of (H_Y): every group's R0 rises to
~1.8-2.0 Mpc, Cen A overshoots too, so V2 must FAIL (rc = 1) and the verdict turns UNIVERSAL.  Outputs: *_MUTATE.out /
*_results_MUTATE.json.  The controls and the U section always use (H_Y): they are statements about the separator.

SCOPE.  Merged point-mass groups (binary geometry <= +0.016, FP11 R2), no neighbour tides, radial Hubble-flow tracers from
a = 0.02; the published R0 come from different estimators (the lane carries the model's own estimator spread and the
estimator-cancelling LG-relative offsets); no particle-mesh run (at most 2 workers, each run < 30 min).
Run from the repository root:  python3 real_research/derivation_chain_2026/FP12_local_volume_groups_r0.py   (MUTATE=1 for the control)
"""
import os, sys, io, json, math, time, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from scipy.optimize import brentq, least_squares
from scipy.stats import chi2 as chi2_dist
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
with contextlib.redirect_stdout(io.StringIO()):
    import FP11_local_group_flyby as F11                                         # FP11's machinery (its main() is not run)
import hunt_lib as HL                                                            # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP12_local_volume_groups_r0"
NPROC = 2
SCORED = "P2" if MUTATE else "HY"

M6 = F11.M6
A0, FOOTS = F11.A0, F11.FOOTS
G, MSUN, MPC, KPC = F11.G, F11.MSUN, F11.MPC, F11.KPC
YIELD, HEAD = F11.YIELD, F11.HEAD
LNA_T, lg_R0, phantom, RG = M6["LNA_T"], M6["lg_R0"], M6["phantom"], M6["RG"]
LG_G, LG_Mpc, LG_H0, LG_OM, LG_OL, LG_OmL = M6["LG_G"], M6["LG_Mpc"], M6["LG_H0"], M6["LG_OM"], M6["LG_OL"], M6["LG_OmL"]
OmL_z = M6["OmL_z"]
BAND = 0.10                                                                      # the chain's +-0.10 dex band (XR4 / FP11)
RS_FIX = 0.3                                                                     # [Mpc] the inner edge of the 'outer profile'

F11J = json.load(open(os.path.join(HERE, "FP11_local_group_flyby_results.json")))["numbers"]
F9J = json.load(open(os.path.join(HERE, "FP9_web_galaxy_separator_results.json")))["numbers"]
F1J = json.load(open(os.path.join(HERE, "FP1_static_sector_results.json")))["numbers"]["E3"]
MT_LG = {f: F11J["timing_mass"][f"HY/{f}/A/0"]["M"] for f in FOOTS}              # FP11's first-approach timing masses

# ================================================================================================= the literature (read at source)
K09, K05, KK06, K07, KK18 = ("Karachentsev+2009 MNRAS 393 1265", "Karachentsev 2005 AJ 129 178 Tab.11", "Karachentsev & Kashibadze "
                             "2006 Ap 49 3", "Karachentsev+2007 AJ 133 504", "Kashibadze & Karachentsev 2018 A&A 609 A11")
MEAS = {                                                                         # key: (primary, K05 homogeneous set); (R0, err, source)
    "LG": ((0.96, 0.03, K09), (0.94, 0.10, K05 + " M.Way/M31")),
    "M81": ((0.89, 0.05, KK06), (1.05, 0.07, K05 + " M81/N2403")),
    "CenA": ((1.40, 0.11, K07), (1.26, 0.15, K05 + " CenA/M83")),
    "M83": (None, None),
    "IC342": ((0.90, 0.10, K05 + " IC342/Maff"), (0.90, 0.10, K05 + " IC342/Maff")),
}
KK18_LG, KK18_STACK, KK18_RANGE = (0.91, 0.05), (0.93, 0.02), (0.71, 1.03)       # abstract / Sect. 4; Table 8 (BC, minor); Table 8 span
KK18_T6 = [  # (group, main, lg M*, D_MW, second, lg M*, D_MW, companions in Table 7): K&K 2018 Table 6 and Table 7
    ("M81", "MESSIER081", 10.95, 3.70, "MESSIER082", 10.59, 3.61, 9),
    ("CenA/M83", "NGC5128", 10.89, 3.68, "NGC5236", 10.86, 4.90, 12),
    ("Maffei2/IC342", "Maffei2", 10.86, 3.48, "IC0342", 10.60, 3.28, 5),
    ("NGC253", "NGC0253", 10.98, 3.70, "NGC0247", 9.50, 3.72, 6),
    ("NGC4826", "NGC4826", 10.49, 4.41, "DDO154", 7.59, 4.04, 3),
    ("NGC4736", "NGC4736", 10.56, 4.41, "NGC4449", 9.68, 4.27, 13),
    ("M101", "MESSIER101", 10.79, 6.95, "NGC5474", 9.21, 6.98, 9),
    ("NGC4258", "NGC4258", 10.92, 7.66, "NGC4242", 9.47, 7.9, 5),
    ("NGC5055", "NGC5055", 11.00, 9.04, "NGC4460", 9.66, 9.59, 0),
    ("NGC4594", "NGC4594", 11.30, 9.30, "NGC4597", 9.48, 10.1, 0),
    ("NGC6744", "NGC6744", 10.91, 9.51, "NGC6684", 10.39, 8.7, 2),
    ("NGC3115", "NGC3115", 10.95, 9.68, "PGC4078671", 7.95, 9.38, 0),
    ("NGC2683", "NGC2683", 10.81, 9.82, "KK69", 7.27, 9.16, 1),
    ("NGC3379", "NGC3379", 10.92, 11.32, "NGC3368", 10.83, 10.42, 1),
]
KK18_LGROW = ("LG", "MESSIER031", 10.79, 0.78, "MilkyWay", 10.70, 0.01, 0)
K05_T10_SGZ = {"LG": 0.00, "M31": 0.07, "M81": 0.04, "CenA": -0.33, "M83": 0.08, "IC342": 0.02, "Maffei": 0.08}   # K05 Table 10 [Mpc]
K05_T11_MtLB = {"LG": 12, "M81": 28, "CenA": 37, "IC342": 18}                  # K05 Table 11, M_t / L_B
MT_LCDM = {"LG": (1.29e12, 0.14e12, KK06), "M81": (1.03e12, 0.17e12, KK06), "CenA": (6.0e12, 1.4e12, K07)}   # published M_T(<R0)
BENISTY26 = (6.36e12, 1.30e12, "Benisty, Libeskind & Makarov 2026, A&A 707, L10 (arXiv:2602.11268)")          # Cen A/M83 timing mass

# ================================================================================================= the law, the shells, the estimators
def LL_of(L25, n):
    """L_Lambda from the band-pass length at z = 0.25 (FP9's LL_of; FP11's L_LAMBDA at the headline)."""
    return L25 / OmL_z(0.25) ** (n / 2.0)


def law_rows(Mb_msun, foot, law, L25=None, y25=None, n=None, pp=None, fp=None, a0=None):
    """The group's enclosed phantom mass on FP6's grid RG at FP6's epochs LNA_T: (H_Y) = FP6's phantom() with FP9's yield hook,
    L(a) = L_Lambda Omega_L(a)^(n/2), y_th(a) = y_th(0.25) (Omega_L(0.25)/Omega_L(a))^p' (FP11's L_of_a / yth_of_a); 'P2' = the
    plain root law.  fp(r) multiplies the phantom (the U section's outer-profile change).  a0 defaults to FP11's footings (FP0's
    JSON); K1 passes FP6's rounded constants to reproduce FP6's lg_both bit for bit."""
    L25 = HEAD["L25"] if L25 is None else L25; y25 = HEAD["y25"] if y25 is None else y25
    n = HEAD["n"] if n is None else n; pp = HEAD["pp"] if pp is None else pp
    a0 = A0[foot] if a0 is None else a0; Mbk = Mb_msun * MSUN; LL = LL_of(L25, n); rows = []
    for la in LNA_T:
        a = math.exp(la)
        if law == "HY":
            Mph = phantom(Mbk, a0, LL * LG_OmL(a) ** (n / 2.0) * MPC, y25 * (LG_OmL(1 / 1.25) / LG_OmL(a)) ** pp, YIELD)
        else:
            Mph = phantom(Mbk, a0, None, None, 4)
        rows.append(Mph if fp is None else Mph * fp(RG))
    return Mbk, np.array(rows)


def make_menc(Mbk, rows, zon=None):
    """M(<r, a) interpolated in ln a between FP6's epochs (FP6's lg_both / FP11's lgR0_efe); zon: phantom off before z_on."""
    lnR = np.log(RG); aon = None if zon is None else 1.0 / (1.0 + zon)

    def Menc(r, a):
        x = math.log(a); j = min(max(np.searchsorted(LNA_T, x) - 1, 0), len(LNA_T) - 2)
        f_ = (x - LNA_T[j]) / (LNA_T[j + 1] - LNA_T[j])
        ph = np.interp(np.log(np.maximum(r, RG[0])), lnR, (1 - f_) * rows[j] + f_ * rows[j + 1])
        return Mbk + (0.0 * ph if (aon is not None and a < aon) else ph)
    return Menc


def R0_true(Mb_msun, foot, law=None, zon=None, **kw):
    """The true zero-velocity radius today [Mpc]: FP6's committed shell bisection lg_R0 on the law's enclosed mass."""
    Mbk, rows = law_rows(Mb_msun, foot, SCORED if law is None else law, **kw)
    return lg_R0(make_menc(Mbk, rows, zon))


def shells(Menc, ri, n_steps=2000, a_start=0.02):
    """FP6 lg_R0's own integrator (FP6_gate_survey.py:397-411), verbatim in effect: radial shells from the Hubble flow at
    a_start, point mass + Lambda; returns today's radius [m] and radial velocity [m/s]."""
    r = ri.copy(); uu = LG_H0 * math.sqrt(LG_OM / a_start ** 3 + LG_OL) * r
    dead = np.zeros_like(r, dtype=bool); lna = np.linspace(math.log(a_start), 0.0, n_steps + 1); h_ = lna[1] - lna[0]

    def accf(l, rr):
        a = math.exp(l); H = LG_H0 * math.sqrt(LG_OM / a ** 3 + LG_OL); rr = np.maximum(rr, 1e-6 * LG_Mpc)
        return -LG_G * Menc(rr, a) / rr ** 2 + LG_OL * LG_H0 ** 2 * rr, H
    for i in range(n_steps):
        l = lna[i]
        a1, H1 = accf(l, r); k1r, k1u = uu / H1, a1 / H1
        a2, H2 = accf(l + h_ / 2, r + h_ * k1r / 2); k2r, k2u = (uu + h_ * k1u / 2) / H2, a2 / H2
        a3, H3 = accf(l + h_ / 2, r + h_ * k2r / 2); k3r, k3u = (uu + h_ * k2u / 2) / H3, a3 / H3
        a4, H4 = accf(l + h_, r + h_ * k3r); k4r, k4u = (uu + h_ * k3u) / H4, a4 / H4
        r = r + h_ * (k1r + 2 * k2r + 2 * k3r + k4r) / 6; uu = uu + h_ * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
        dead |= r <= 1e-5 * LG_Mpc; r = np.where(dead, 1e-5 * LG_Mpc, r); uu = np.where(dead, -1.0, uu)
    return r, uu


RI_TR = np.geomspace(5.0, 120.0, 4000) * KPC                                     # tracer radii at a = 0.02 (physical): today's
#                                                                                  0.1-25 Mpc, >= 150 shells in the fit windows
#                                                                                  (converged to 1e-3 against 3000 / 1500 shells)


def hubble_diagram(Mb_msun, foot, law=None, **kw):
    """The model's Hubble diagram: today's (R [Mpc], V [km/s]) of the shells, Lagrangian mass weights (uniform initial density,
    equal d ln r_i: w = r_i^3), and the zero crossing of V found on the dense tracer grid."""
    Mbk, rows = law_rows(Mb_msun, foot, SCORED if law is None else law, **kw)
    r, u = shells(make_menc(Mbk, rows), RI_TR.copy())
    R, V, w = r / LG_Mpc, u / 1e3, RI_TR ** 3
    live = r > 1.0001e-5 * LG_Mpc
    idx = [j for j in range(len(R) - 1) if live[j] and V[j] < 0 < V[j + 1] and R[j + 1] > 0.3]
    Rz = float("nan")
    if idx:
        j = idx[-1]; Rz = float(R[j] + (-V[j] / (V[j + 1] - V[j])) * (R[j + 1] - R[j]))
    return dict(R=R, V=V, w=w, live=live, R_zero=Rz)


def fit_lin(R, V, w, live, lo=0.7, hi=3.0):
    """k02 / Karachentsev+2009 / FP11 R4's estimator: V = H (R - R0), weighted least squares over lo < R < hi."""
    s = live & (R > lo) & (R < hi)
    A = np.vstack([R[s], np.ones(s.sum())]).T * np.sqrt(w[s])[:, None]
    h, b = np.linalg.lstsq(A, V[s] * np.sqrt(w[s]), rcond=None)[0]
    return float(-b / h), float(h)


def fit_eq14(R, V, w, live, lo=0.7, hi=3.5):
    """K&K 2018's eq. 14 estimator: V = H R [1 - (R0/R)^(1/2)] (their R < 3.5 Mpc), weighted least squares."""
    s = live & (R > lo) & (R < hi); ww = w[s] / w[s].mean()
    sol = least_squares(lambda p: (V[s] - p[0] * R[s] * (1 - np.sqrt(abs(p[1]) / R[s]))) * np.sqrt(ww), [80.0, 1.0])
    return float(abs(sol.x[1])), float(sol.x[0])


def estimators(Mb_msun, foot, law=None, **kw):
    hd = hubble_diagram(Mb_msun, foot, law, **kw)
    lin, H = fit_lin(hd["R"], hd["V"], hd["w"], hd["live"]); e14, H14 = fit_eq14(hd["R"], hd["V"], hd["w"], hd["live"])
    return dict(true=R0_true(Mb_msun, foot, law, **kw), zero_tracer=hd["R_zero"], lin=lin, H_lin=H, eq14=e14, H_eq14=H14), hd


def fprof(f, rs=RS_FIX):
    """the outer-profile change of the U section: the phantom multiplied by f beyond ~rs (a smooth step in r^4)."""
    return lambda r: f + (1.0 - f) / (1.0 + (np.asarray(r, float) / (rs * MPC)) ** 4)


# ================================================================================================= the committed UNGC (k02's pipeline)
_rows = HL.vizier_tsv("ungc_karachentsev2013.tsv")
U_NAME = np.array([r_["Name"].strip() for r_ in _rows])
U_KEY = np.char.replace(np.char.upper(U_NAME), " ", "")
U_RA = np.array([HL._f(r_["_RAJ2000"]) for r_ in _rows]); U_DE = np.array([HL._f(r_["_DEJ2000"]) for r_ in _rows])
U_D = np.array([HL._f(r_["Dist"]) for r_ in _rows]); U_V = np.array([HL._f(r_["Vlg"]) for r_ in _rows])
U_LK = np.array([HL._f(r_["KLum"]) for r_ in _rows]); U_HI = np.array([HL._f(r_["MHI"]) for r_ in _rows])
U_FD = np.array([r_["f_Dist"].strip() for r_ in _rows])
U_UNIT = np.stack([np.cos(np.radians(U_DE)) * np.cos(np.radians(U_RA)), np.cos(np.radians(U_DE)) * np.sin(np.radians(U_RA)),
                   np.sin(np.radians(U_DE))], axis=1)
ACC_DIST = ("TRGB", "Cep", "RR", "HB", "SBF", "BS", "CMD", "geom")
GROUPS = (("LG", "Local Group", "MilkyWay"), ("M81", "M81 group", "MESSIER081"), ("CenA", "Cen A group", "NGC5128"),
          ("M83", "M83 group", "NGC5236"), ("IC342", "IC 342 group", "IC0342"))
EXT = ("M81", "CenA", "M83", "IC342")
SCORED_EXT = ("M81", "CenA", "IC342")
K02_OUT = {"LG": (1.176, 0.106, 1.145e11), "M81": (1.033, 0.165, 9.621e10), "CenA": (0.614, 0.234, 9.025e10),     # hunt_2026/
           "M83": (0.488, 1.375, 5.764e10), "IC342": (0.925, 0.118, 1.034e11)}                                    # k02_lambda_edge_zvs.out


def uidx(key):
    i = np.where(U_KEY == key.upper())[0]
    return int(i[0]) if len(i) else None


def group_frame(i_c, dmax=4.0):
    """k02's group_frame (hunt_2026/k02_lambda_edge_zvs.py:183-191), verbatim in effect."""
    Dc, Vc, nc = U_D[i_c], U_V[i_c], U_UNIT[i_c]
    with np.errstate(all="ignore"):
        cth = U_UNIT @ nc
        R = np.sqrt(np.clip(U_D ** 2 + Dc ** 2 - 2 * U_D * Dc * cth, 0, None))
        Vr = (U_V * (U_D - Dc * cth) + Vc * (Dc - U_D * cth)) / R
    ok = np.isfinite(R) & np.isfinite(Vr) & (R > 0.0) & (R < dmax) & (np.arange(len(U_D)) != i_c)
    return R, Vr, ok


def fit_R0_k02(R, Vr, ok, rlo, rhi, boot=True):
    """k02's fit_R0 (k02_lambda_edge_zvs.py:194-210), verbatim in effect (the same bootstrap seed)."""
    m = ok & (R > rlo) & (R < rhi)
    if m.sum() < 8:
        return float("nan"), float("nan"), int(m.sum()), float("nan")
    A = np.vstack([R[m], np.ones(m.sum())]).T; h, b = np.linalg.lstsq(A, Vr[m], rcond=None)[0]; R0 = -b / h
    if not boot:
        return float(R0), float("nan"), int(m.sum()), float(h)
    rng = np.random.default_rng(20260903); bs = []; idx = np.where(m)[0]
    for _ in range(2000):
        s = rng.choice(idx, len(idx), replace=True); A2 = np.vstack([R[s], np.ones(len(s))]).T
        hh, bb = np.linalg.lstsq(A2, Vr[s], rcond=None)[0]
        if hh > 0: bs.append(-bb / hh)
    return float(R0), (float(np.std(bs)) if bs else float("nan")), int(m.sum()), float(h)


def baryons(R, ok, rcut, i_c, anchor, ups=0.6):
    """k02's baryonic_mass + its centre terms (k02_lambda_edge_zvs.py:213-248): ups L_K + 1.33 M_HI inside rcut."""
    m = ok & (R < rcut)
    Ms = np.nansum(ups * 10.0 ** U_LK[m][np.isfinite(U_LK[m])]); Mg = 1.33 * np.nansum(10.0 ** U_HI[m][np.isfinite(U_HI[m])])
    if anchor == "MilkyWay":
        Ms += 6.1e10; Mg += 1.33 * 10.0 ** U_HI[i_c]
    else:
        Ms += ups * 10.0 ** U_LK[i_c] if np.isfinite(U_LK[i_c]) else 0.0
        Mg += 1.33 * 10.0 ** U_HI[i_c] if np.isfinite(U_HI[i_c]) else 0.0
    return float(Ms), float(Mg)


def read_sparc():
    """(name, r_last [kpc], M_b [Msun]) for SPARC (Lelli+2016, committed): the last rotation-curve radius of each rotmod file;
    M_b = 0.5 L[3.6] + 1.33 M_HI (Table 1; the record's standard Upsilon_[3.6] = 0.5)."""
    p = os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt"); out = []
    lines = open(p, encoding="latin-1").read().splitlines()
    start = max(i for i, l in enumerate(lines) if l.startswith("-----")) + 1
    for l in lines[start:]:
        t = l.split()
        if len(t) < 17: continue
        f_ = os.path.join(REPO, "real_research", "data", "sparc_data", t[0] + "_rotmod.dat")
        if not os.path.exists(f_): continue
        rr = [float(x.split()[0]) for x in open(f_) if x.strip() and not x.startswith("#")]
        out.append((t[0], max(rr), 0.5 * float(t[7]) * 1e9 + 1.33 * float(t[13]) * 1e9))
    return out


# ================================================================================================= pool jobs (top level: worker-safe)
def job_tracer(cfg):
    """FP11's tracer machinery for one group: the merged pair's field (PairField, merged) and the zero-velocity finder."""
    key, foot, Mb, law = cfg; t = time.time(); bp = yl = (law == "HY")
    m1, m2 = F11.FMW * Mb * MSUN, (1 - F11.FMW) * Mb * MSUN
    pf = F11.PairField(m1, m2, A0[foot], lambda l: 0.0, F11.LNAT, bp=bp, yl=yl, merged=True)
    R0, _ = F11.R0_rays(pf, lambda l: 0.0, np.array([math.pi / 2]))
    return cfg, float(R0[0]), time.time() - t


def job_lg(foot):
    """FP11's own timing-matched configuration (job_matched, convention A, tracers) at FP11's committed timing mass."""
    t = time.time()
    name, out, dt = F11.job_matched((f"HY/A/{foot}", "HY", foot, MT_LG[foot], "A", 0, dict(tracers=True)))
    return foot, dict(R0=out["R0"]["mean"], rays=out["R0"]["rays"], merged=out["R0_merged"], vr=out["branch"]["vr"]), time.time() - t


def job_timing_f(cfg):
    """the MW-M31 first-approach v_r in FP11's two-body law with the pair's mutual MOND part scaled by the outer profile f(d)."""
    foot, Mb, fsc = cfg; t = time.time()
    m1, m2 = F11.FMW * Mb * MSUN, (1 - F11.FMW) * Mb * MSUN
    dg, ln_, T = F11.force_table(m1, m2, A0[foot], True, True)
    Nw = G * (m1 + m2) / dg[None, :] ** 2; out = {}
    for lab, TT in (("unscaled", T), ("scaled", Nw + fprof(fsc)(dg)[None, :] * (T - Nw))):
        br = [b for b in F11.branches(F11.Acc(dg, ln_, TT, m1 + m2)) if b["k"] == 0 and b["vr"] < 0]
        out[lab] = br[0]["vr"] if br else float("nan")
    return cfg, out, time.time() - t


# ================================================================================================= reporting
CH = []
OUT = {"lane": "FP12", "mutate": MUTATE, "scored_law": SCORED, "checks": {}, "numbers": {}, "ledger": []}
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


def dex(a, b):
    return math.log10(a / b)


def sig_dex(R, e):
    return e / (R * math.log(10))


def label(deltas):
    """the declared rule: deltas = {system: (delta_can, delta_alt)} with 'LG' among them."""
    cls = {}
    for k_, (dc, da) in deltas.items():
        cls[k_] = "over" if (dc > BAND and da > BAND) else ("fits" if (abs(dc) <= BAND and abs(da) <= BAND) else "between")
    ext = [cls[k_] for k_ in deltas if k_ != "LG"]
    if cls.get("LG") == "over" and all(c == "over" for c in ext):
        return "UNIVERSAL", cls
    if cls.get("LG") == "over" and all(c == "fits" for c in ext):
        return "LG-ONLY", cls
    return "MIXED", cls


def interp_mass(pts, target=F11.VR_LG):
    return F11.timing_mass(pts, target)


def main():
    from multiprocessing import Pool
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: the SCORED law is the unseparated plain P2 root (no band-pass, no yield); V2 must FAIL ***")
    P(f"\n  footings a0 = {A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2 (FP0); (H_Y) L_Lambda = {F11.L_LAMBDA:.3f} Mpc, n = {HEAD['n']:g}, "
      f"y_Lambda = {F11.Y_LAMBDA:.3e}, p' = {HEAD['pp']:g} (FP9); scored law: {'plain P2 (MUTATE)' if MUTATE else '(H_Y)'}; "
      f"FP11 LG timing masses {MT_LG['canonical']:.4e} / {MT_LG['alt']:.4e}")

    # ---------------------------------------------------------------------------------------- queue the heavy jobs
    pool = Pool(NPROC)
    AL = [pool.apply_async(job_lg, (f,)) for f in FOOTS]
    # the nominal k02 masses (re-derived below exactly; the committed values are used to queue now, K4 checks they agree)
    AT = [pool.apply_async(job_tracer, ((g, f, K02_OUT[g][2], SCORED),)) for g in EXT for f in FOOTS]
    FT = 0.30                                                                    # the typical f the universal fix needs (U2)
    TM_SCAN = {f: (MT_LG[f], 4.0e11, 1.0e12, 2.5e12) for f in FOOTS}
    AF = [pool.apply_async(job_timing_f, ((f, Mb, FT),)) for f in FOOTS for Mb in TM_SCAN[f]]

    # ============================================================================================= K controls (light)
    banner("K  CONTROLS: FP9's and FP11's committed numbers, k02's measurement, the MUTATE law, FP9's gates")
    lg = M6["lg_both"](F11.L_LAMBDA, HEAD["n"], floor=(HEAD["y25"], HEAD["pp"], YIELD)); ref9 = F9J["H3"]["2.0_1.3"]
    mine = {f: R0_true(1.145e11 * M6["LG_Msun"] / MSUN, f, "HY", a0=M6["A0"][f]) for f in FOOTS}
    dk1 = max(max(abs(lg[f] / ref9[f] - 1), abs(mine[f] / ref9[f] - 1)) for f in FOOTS)
    check("K1 CONTROL: FP9's LG zero-velocity radius at the (H_Y) headline cell (merged, M_b = 1.145e11) is reproduced exactly by FP6's "
          "lg_both and by this lane's law function", f"lg_both {lg['canonical']:.6f} / {lg['alt']:.6f}; this lane {mine['canonical']:.6f} / "
          f"{mine['alt']:.6f}; committed {ref9['canonical']:.6f} / {ref9['alt']:.6f} (max rel dev {dk1:.1e})", dk1 < 1e-9)
    p1 = {f: R0_true(MT_LG[f], f, "HY") for f in FOOTS}; ref11 = {f: F11J["P1"][f]["R0_of_e"][0][1] for f in FOOTS}
    dk3 = max(abs(p1[f] / ref11[f] - 1) for f in FOOTS)
    check("K3 CONTROL: FP11's P1 merged-LG R0 at the timing mass (e = 0) is reproduced by this lane's law function",
          f"{p1['canonical']:.6f} / {p1['alt']:.6f} vs committed {ref11['canonical']:.6f} / {ref11['alt']:.6f} (max rel dev {dk3:.1e})", dk3 < 1e-9)
    p2 = {f: R0_true(1.145e11, f, "P2") for f in FOOTS}; ref1 = {f: F1J[f]["R0_e0"] for f in FOOTS}
    dk6 = max(abs(p2[f] / ref1[f] - 1) for f in FOOTS)
    check("K6 CONTROL: the unseparated plain-P2 root law (MUTATE's law) gives FP1 E3's merged LG R0 at M_b = 1.145e11",
          f"{p2['canonical']:.4f} / {p2['alt']:.4f} vs FP1 {ref1['canonical']:.4f} / {ref1['alt']:.4f} (max rel dev {dk6:.1e}; FP11 K5's tolerance 3e-3)", dk6 < 3e-3)
    # K7: FP9's gates with FP9's constants (as FP11 K7)
    L_phys, law_dev_dex, kids_class = M6["L_phys"], M6["law_dev_dex"], M6["kids_class"]
    yz = lambda z, y25=HEAD["y25"], pp=HEAD["pp"]: y25 * (OmL_z(0.25) / OmL_z(z)) ** pp
    flag = {(f, Mv): law_dev_dex(Mv, A0[f], 0.1, L_phys(F11.L_LAMBDA, HEAD["n"], 1 / 3.5), yz(2.5), YIELD) for f in FOOTS for Mv in (1e10, 1e11)}

    def sparc_gate(f, L25=HEAD["L25"], y25=HEAD["y25"]):
        return max(abs(law_dev_dex(Mv, A0[f], yv, L_phys(LL_of(L25, HEAD["n"]), HEAD["n"], 1.0), yz(0.0, y25), YIELD))
                   for Mv in (1e9, 1e10, 1e11, 1e12) for yv in (0.01, 0.03, 0.1, 1.0, 10.0, 100.0))
    sparc = {f: sparc_gate(f) for f in FOOTS}
    KB = {f: kids_class(A0[f]) for f in FOOTS}
    kids = {f: kids_class(A0[f], HEAD["L25"], yz(0.25), YIELD) - KB[f] for f in FOOTS}
    H2 = F9J["H2"]
    d7 = max([abs(flag[(f, Mv)] / H2["flag"][str((f, Mv))] - 1) for f in FOOTS for Mv in (1e10, 1e11)] + [abs(sparc[f] / H2["sparc"][f] - 1) for f in FOOTS]
             + [abs(kids[f] - H2["kids"][f]) for f in FOOTS])
    check("K7 CONTROL: FP9's headline gate numbers (the 1e10/1e11 flagship at z = 2.5, the SPARC range, the KiDS lead grade) are "
          "reproduced exactly with FP9's four constants -- the constants every (H_Y) number in this lane uses",
          f"flagship {min(flag.values()):+.4f}..{max(flag.values()):+.4f} dex; SPARC {sparc['canonical']:.1e}/{sparc['alt']:.1e} dex; "
          f"KiDS {kids['canonical']:+.2f}/{kids['alt']:+.2f}; max deviation from FP9's JSON {d7:.1e}", d7 < 1e-9)
    OUT["numbers"]["K"] = dict(K1=dict(lg_both=lg, mine=mine, committed=ref9), K3=dict(mine=p1, committed=ref11), K6=dict(mine=p2, FP1=ref1),
                               K7=dict(flag={str(k_): v for k_, v in flag.items()}, sparc=sparc, kids=kids))

    # K4 + S1: k02's measurement re-derived, and its stability
    meas02, stab, mass = {}, {}, {}
    for key, gname, anchor in GROUPS:
        i_c = uidx(anchor); R, Vr, ok = group_frame(i_c)
        R0, eR0, N, h = fit_R0_k02(R, Vr, ok, 0.7, 3.0)
        Ms, Mg = baryons(R, ok, R0, i_c, anchor)
        meas02[key] = dict(R0=R0, eR0=eR0, N=N, H=h, Ms=Ms, Mg=Mg, Mb=Ms + Mg)
        var = {}
        for lab, (lo, hi, acc) in {"0.7-2.5": (0.7, 2.5, False), "0.5-3.0": (0.5, 3.0, False), "0.7-3.5": (0.7, 3.5, False),
                                   "1.0-3.0": (1.0, 3.0, False), "accurate D": (0.7, 3.0, True)}.items():
            var[lab] = fit_R0_k02(R, Vr, ok & (np.isin(U_FD, ACC_DIST) if acc else True), lo, hi, boot=False)[0]
        vv = [R0] + list(var.values())
        stab[key] = dict(variants=var, spread=float(max(vv) - min(vv)), unstable=bool((max(vv) - min(vv)) > 2 * eR0 or min(vv) <= 0))
        # the mass band: Upsilon_K x aperture x unseen gas (IC 342's aperture >= 0.8 Mpc keeps Maffei 1/2)
        grid = []
        if key != "LG":
            for ups in (0.5, 0.6, 1.0):
                for ap in ((0.8, 1.0, 1.5) if key == "IC342" else (0.7, 1.0, 1.5)):
                    for cgm in (1.0, 1.4):
                        ms_, mg_ = baryons(R, ok, ap, i_c, anchor, ups); grid.append((ms_ + mg_) * cgm)
        mass[key] = dict(nominal=Ms + Mg, lo=min(grid) if grid else None, hi=max(grid) if grid else None)
    iCen = uidx("NGC5128"); Rc_, _, okc_ = group_frame(iCen)
    ms_, mg_ = baryons(Rc_, okc_, 1.6, iCen, "NGC5128")                          # the Cen A/M83 complex: M83 sits 1.5 Mpc out
    mass["CenA+M83"] = dict(nominal=ms_ + mg_)
    dk4 = max(max(abs(meas02[k_]["R0"] - K02_OUT[k_][0]), abs(meas02[k_]["eR0"] - K02_OUT[k_][1]), abs(meas02[k_]["Mb"] / K02_OUT[k_][2] - 1))
              for k_ in K02_OUT)                                                 # k02 prints 3 decimals / 4 digits
    check("K4 CONTROL: the record's k02 measurement (UNGC, k02's group frame, linear fit 0.7-3 Mpc, bootstrap seed 20260903) and its "
          "baryonic masses (0.6 L_K + 1.33 M_HI inside the measured R0) are re-derived exactly from the committed catalogue",
          "; ".join(f"{k_}: R0 {meas02[k_]['R0']:.3f} +- {meas02[k_]['eR0']:.3f} (k02 {K02_OUT[k_][0]} +- {K02_OUT[k_][1]}), M_b {meas02[k_]['Mb']:.4e} "
                    f"(k02 {K02_OUT[k_][2]:.3e})" for k_ in K02_OUT) + f"; max |dev| {dk4:.1e}", dk4 < 1.5e-3)
    check("S1 (reported) THE RECORD'S UNGC R0 OF THE EXTERNAL GROUPS ARE NOT MEASUREMENTS: k02's own estimator moves by more than twice "
          "its bootstrap error (or through zero) when the fit window or the distance quality changes, for every external group (the "
          "record's XR4 N2 and k_dimensional K3.2/K3.3 found the same: ~100 km/s flow scatter around groups at 3-5 Mpc) -- the "
          "confrontation below uses the published R0, read at source",
          "; ".join(f"{k_}: " + ", ".join(f"{lab} {v:.2f}" for lab, v in stab[k_]["variants"].items()) + f" (spread {stab[k_]['spread']:.2f} vs "
                    f"2 sigma_boot {2 * meas02[k_]['eR0']:.2f}: {'UNSTABLE' if stab[k_]['unstable'] else 'stable'})" for k_ in K02_OUT),
          True, load_bearing=False, reading=f"external groups unstable: {[k_ for k_ in EXT if stab[k_]['unstable']]}; the LG's k02 value is "
                                            f"MW-centred (1.18 vs the barycentric 0.96-1.05 of FP11 R4)")
    OUT["numbers"]["K4_S1"] = dict(k02=meas02, stability=stab)

    # K8: K&K 2018's stellar masses vs the UNGC's L_K
    ups_imp = []
    for row in KK18_T6 + [KK18_LGROW]:
        for (nm, lm, dkk) in ((row[1], row[2], row[3]), (row[4], row[5], row[6])):
            i = uidx(nm)
            if i is not None and np.isfinite(U_LK[i]) and U_D[i] > 0.1:
                ups_imp.append((nm, 10 ** (lm - U_LK[i]) / (dkk / U_D[i]) ** 2))
    ui = np.array([u for _, u in ups_imp]); UPS_KK = float(np.median(ui))
    out_nm = max(ups_imp, key=lambda x: x[1])[0]
    out_in_stack = any(out_nm in (r_[1], r_[4]) and r_[7] > 0 for r_ in KK18_T6)
    check("K8 (reported) K&K 2018's stellar masses (Table 6) against the committed UNGC's L_K at the same distance: the implied "
          "Upsilon_K of the stack's masses (used to put the stack on k02's Upsilon_K = 0.6)",
          f"{len(ui)} galaxies: median {UPS_KK:.3f}, range {ui.min():.2f}-{ui.max():.2f} (" + ", ".join(f"{n_} {u:.2f}" for n_, u in ups_imp[:8])
          + f", ...; the largest, {out_nm}, is {'IN' if out_in_stack else 'not in'} a group with stacked companions)", True, load_bearing=False)
    OUT["numbers"]["K8"] = dict(median=UPS_KK, values=ups_imp)
    P(f"    {el()}")

    # ============================================================================================= M masses, R model R0
    banner("M / R  THE BARYONS AND THE CHAIN'S ZERO-VELOCITY RADII (the scored law; both footings; three estimators)")
    for k_ in EXT:
        P(f"    {k_:6s} M_b nominal (k02) {mass[k_]['nominal']:.3e}  band [{mass[k_]['lo']:.3e}, {mass[k_]['hi']:.3e}]  (Upsilon_K 0.5/0.6/1.0 x "
          f"aperture {'0.8' if k_ == 'IC342' else '0.7'}-1.5 Mpc x unseen gas 1-1.4)")
    P(f"    CenA+M83 (every UNGC galaxy within 1.6 Mpc of Cen A, which reaches M83 at "
      f"{float(group_frame(uidx('NGC5128'))[0][uidx('NGC5236')]):.2f} Mpc): {mass['CenA+M83']['nominal']:.3e}")
    P(f"    LG: FP11's timing masses {MT_LG['canonical']:.3e} / {MT_LG['alt']:.3e} (can/alt); k02's 1.145e11")
    check("M1 (reported) THE BARYONIC MASSES: k02's accounting re-derived (nominal) and the band (Upsilon_K 0.5-1.0, aperture 0.7-1.5 "
          "Mpc, x1.4 unseen gas); R0 moves as M_b^0.19 in (H_Y), so the band is worth +-0.04-0.05 dex on R0",
          "; ".join(f"{k_}: {mass[k_]['nominal']:.2e} [{mass[k_]['lo']:.2e}, {mass[k_]['hi']:.2e}]" for k_ in EXT)
          + f"; CenA+M83 {mass['CenA+M83']['nominal']:.2e}", True, load_bearing=False)
    OUT["numbers"]["M1"] = mass

    MOD = {}
    for k_ in EXT:
        for f in FOOTS:
            est, hd = estimators(mass[k_]["nominal"], f)
            MOD[(k_, f)] = dict(est=est, lo=R0_true(mass[k_]["lo"], f), hi=R0_true(mass[k_]["hi"], f), hd=hd)
    for f in FOOTS:
        est, hd = estimators(mass["CenA+M83"]["nominal"], f); MOD[("CenA+M83", f)] = dict(est=est, hd=hd)
        est, hd = estimators(MT_LG[f], f); MOD[("LG", f)] = dict(est=est, hd=hd)
        est, _ = estimators(1.145e11, f); MOD[("LG@k02", f)] = dict(est=est)
    # the LG row: FP11's two-body timing-matched R0 (re-run, K2) for (H_Y); the merged law at FP11's masses for the MUTATE law
    LGR = {}
    for a_ in AL:
        f, v, dt = a_.get(); LGR[f] = v; P(f"    FP11 job_matched HY/A/{f}: two-body R0 {v['R0']:.4f}, merged {v['merged']:.4f}, v_r {v['vr']:+.2f}  [{dt:.0f}s]")
    ref2 = {f: (F11J["matched"][f"HY/A/{f}"]["R0"]["mean"], F11J["matched"][f"HY/A/{f}"]["R0_merged"]) for f in FOOTS}
    dk2 = max(max(abs(LGR[f]["R0"] / ref2[f][0] - 1), abs(LGR[f]["merged"] / ref2[f][1] - 1)) for f in FOOTS)
    check("K2 CONTROL: FP11's Local Group R0 is reproduced by re-running FP11's own timing-matched job (convention A, two-body tracers, "
          "8 rays) at its committed timing masses -- the LG row of this lane IS FP11's",
          f"two-body {LGR['canonical']['R0']:.6f} / {LGR['alt']['R0']:.6f} vs committed {ref2['canonical'][0]:.6f} / {ref2['alt'][0]:.6f}; merged "
          f"{LGR['canonical']['merged']:.6f} / {LGR['alt']['merged']:.6f} vs {ref2['canonical'][1]:.6f} / {ref2['alt'][1]:.6f} (max rel dev {dk2:.1e})", dk2 < 1e-6)
    LG_MODEL = {f: (LGR[f]["R0"] if SCORED == "HY" else MOD[("LG", f)]["est"]["true"]) for f in FOOTS}
    # K5: FP11's tracer machinery vs the shell integrator, every group, both footings
    TR = {}
    for a_ in AT:
        (g, f, Mb, law), R0t, dt = a_.get(); TR[(g, f)] = R0t
    dk5 = max(abs(TR[(g, f)] / R0_true(K02_OUT[g][2], f) - 1) for g in EXT for f in FOOTS)
    check("K5 CONTROL: FP11's tracer machinery (dwarfs from the Hubble flow through the group's field: PairField merged + R0_rays) "
          "equals the shell integrator's R0 for every group on both footings at k02's masses (the scored law)",
          "; ".join(f"{g}/{f[:3]}: tracers {TR[(g, f)]:.4f} vs shells {R0_true(K02_OUT[g][2], f):.4f}" for g in EXT for f in FOOTS) + f" (max rel dev {dk5:.1e})",
          dk5 < 3e-3)
    OUT["numbers"]["K2_K5"] = dict(LG=LGR, committed=ref2, tracer={f"{g}/{f}": v for (g, f), v in TR.items()})
    P("")
    P(f"    {'group':9s} {'M_b':>9s} | {'R0 true can/alt':>16s} | {'band (mass) can':>16s} | {'lin-fit can/alt':>15s} | {'eq.14 can/alt':>14s} | "
      f"{'H_lin':>8s} | tracer zero")
    rows_R1 = {}
    for k_ in EXT + ("CenA+M83",):
        e_c, e_a = MOD[(k_, "canonical")]["est"], MOD[(k_, "alt")]["est"]
        bd = f"{MOD[(k_, 'canonical')]['lo']:.3f}-{MOD[(k_, 'canonical')]['hi']:.3f}" if "lo" in MOD[(k_, "canonical")] else "-"
        P(f"    {k_:9s} {mass[k_]['nominal']:9.3e} | {e_c['true']:7.3f} / {e_a['true']:6.3f} | {bd:>16s} | {e_c['lin']:6.3f} / {e_a['lin']:6.3f} | "
          f"{e_c['eq14']:5.3f} / {e_a['eq14']:5.3f} | {e_c['H_lin']:3.0f}/{e_a['H_lin']:3.0f} | {e_c['zero_tracer']:.3f}")
        rows_R1[k_] = dict(can=e_c, alt=e_a)
    for k_ in ("LG", "LG@k02"):
        e_c, e_a = MOD[(k_, "canonical")]["est"], MOD[(k_, "alt")]["est"]
        P(f"    {k_:9s} {'timing' if k_ == 'LG' else '1.145e11':>9s} | {e_c['true']:7.3f} / {e_a['true']:6.3f} | {'(merged)':>16s} | {e_c['lin']:6.3f} / {e_a['lin']:6.3f} | "
          f"{e_c['eq14']:5.3f} / {e_a['eq14']:5.3f} | {e_c['H_lin']:3.0f}/{e_a['H_lin']:3.0f} | {e_c['zero_tracer']:.3f}")
        rows_R1[k_] = dict(can=e_c, alt=e_a)
    P(f"    LG (two-body, FP11, timing-matched): {LGR['canonical']['R0']:.3f} / {LGR['alt']['R0']:.3f} -- the scored LG row" if SCORED == "HY" else
      f"    LG (MUTATE: plain law, merged at FP11's timing masses): {LG_MODEL['canonical']:.3f} / {LG_MODEL['alt']:.3f} -- the scored LG row")
    slope = {f: dex(R0_true(3e11, f), R0_true(3e10, f)) for f in FOOTS}
    est_off = {e_: [dex(rows_R1[k_][c_][e_], rows_R1[k_][c_]["true"]) for k_ in rows_R1 for c_ in ("can", "alt")] for e_ in ("lin", "eq14", "zero_tracer")}
    rng_R = [MOD[(k_, f)][b_] for k_ in EXT for f in FOOTS for b_ in ("lo", "hi")] + [MOD[(k_, f)]["est"]["true"] for k_ in EXT for f in FOOTS]
    rng_M = [mass[k_][b_] for k_ in EXT for b_ in ("lo", "hi")]
    lead = "the band-pass flattens the deep-MOND 1/4 slope" if SCORED == "HY" else "the unseparated law keeps the deep-MOND slope"
    check("R1 (reported) THE CHAIN'S ZERO-VELOCITY RADII of the four groups: true zero-velocity radius (headline), the linear fit over "
          "0.7-3 Mpc (k02 / FP11 R4's estimator) and K&K 2018's eq. 14 over 0.7-3.5 Mpc on the model's own mass-weighted shells; the "
          "mass slope", "; ".join(f"{k_}: {rows_R1[k_]['can']['true']:.3f}/{rows_R1[k_]['alt']['true']:.3f} (lin {rows_R1[k_]['can']['lin']:.3f}, eq14 "
                                    f"{rows_R1[k_]['can']['eq14']:.3f})" for k_ in EXT) + f"; d log R0/d log M_b = {slope['canonical']:.3f} / {slope['alt']:.3f} "
          f"(3e10-3e11)", True, load_bearing=False,
          reading=f"{lead} (d log R0/d log M_b = {slope['canonical']:.2f}), so every group of {min(rng_M):.1e}-{max(rng_M):.1e} baryons (the "
                  f"mass bands) sits at {min(rng_R):.2f}-{max(rng_R):.2f} Mpc on either footing; on the "
                  f"model's own flow the estimators read, relative to the true zero-velocity radius: linear fit "
                  f"{min(est_off['lin']):+.3f}..{max(est_off['lin']):+.3f} dex, eq. 14 {min(est_off['eq14']):+.3f}..{max(est_off['eq14']):+.3f} dex "
                  f"(the dense-shell zero crossing {min(est_off['zero_tracer']):+.4f}..{max(est_off['zero_tracer']):+.4f}: the shells are lg_R0's) -- "
                  f"the estimator systematic V3 carries")
    OUT["numbers"]["R1_estimator_offsets"] = est_off
    OUT["numbers"]["R1"] = dict(rows=rows_R1, slope=slope, LG_scored=LG_MODEL)
    P(f"    {el()}")

    # ============================================================================================= V the verdict
    banner("V  THE CONFRONTATION AND THE VERDICT (the rule declared in the docstring)")

    def deltas(setix, est="true", mkey="nominal", cen_complex=False):
        out = {}
        for k_ in ("LG",) + SCORED_EXT:
            m_ = MEAS[k_][setix]
            if k_ == "LG":
                mod = {f: (LG_MODEL[f] if est == "true" else MOD[("LG", f)]["est"][est]) for f in FOOTS}
            else:
                src = "CenA+M83" if (k_ == "CenA" and cen_complex) else k_
                if mkey == "nominal" or src == "CenA+M83":
                    mod = {f: MOD[(src, f)]["est"][est] for f in FOOTS}
                else:
                    mod = {f: MOD[(src, f)][mkey] for f in FOOTS}
            out[k_] = (dex(mod["canonical"], m_[0]), dex(mod["alt"], m_[0]))
        return out
    D0 = deltas(0)
    P(f"    {'system':8s} {'R0 measured':>14s}  {'source':42s} {'model can/alt':>14s} {'delta can/alt [dex]':>20s} {'sigma':>6s} {'n sigma':>7s}")
    SIG = {}
    for k_ in ("LG",) + SCORED_EXT:
        R_, e_, s_ = MEAS[k_][0]
        mc = LG_MODEL["canonical"] if k_ == "LG" else MOD[(k_, "canonical")]["est"]["true"]
        ma = LG_MODEL["alt"] if k_ == "LG" else MOD[(k_, "alt")]["est"]["true"]
        smod = 0.006 if k_ == "LG" else 0.5 * dex(MOD[(k_, "canonical")]["hi"], MOD[(k_, "canonical")]["lo"])
        SIG[k_] = math.hypot(sig_dex(R_, e_), smod)
        P(f"    {k_:8s} {R_:6.2f} +- {e_:4.2f}  {s_:42s} {mc:6.3f}/{ma:6.3f} {D0[k_][0]:+9.3f} / {D0[k_][1]:+7.3f} {SIG[k_]:6.3f} {D0[k_][0] / SIG[k_]:+7.1f}")
    dcen = {f: dex(MOD[("CenA+M83", f)]["est"]["true"], MEAS["CenA"][0][0]) for f in FOOTS}
    P(f"    CenA with M83's baryons merged: model {MOD[('CenA+M83', 'canonical')]['est']['true']:.3f}/{MOD[('CenA+M83', 'alt')]['est']['true']:.3f} -> "
      f"delta {dcen['canonical']:+.3f} / {dcen['alt']:+.3f}")
    m83 = (MOD[("M83", "canonical")]["est"]["true"], MOD[("M83", "alt")]["est"]["true"])
    P(f"    M83 (UNSCORED: no published R0; k02's UNGC fit {meas02['M83']['R0']:.2f} +- {meas02['M83']['eR0']:.2f}): the chain PREDICTS R0 = {m83[0]:.2f} / "
      f"{m83[1]:.2f} Mpc (mass band {MOD[('M83', 'canonical')]['lo']:.2f}-{MOD[('M83', 'canonical')]['hi']:.2f})")
    # the stack (K&K 2018): companion-weighted model
    stk = []
    for row in KK18_T6:
        g, n1, l1, d1, n2, l2, d2, nc = row
        if nc == 0: continue
        gas = sum(1.33 * 10 ** U_HI[i] for i in (uidx(n1), uidx(n2)) if i is not None and np.isfinite(U_HI[i]))
        stk.append((g, nc, (0.6 / UPS_KK) * (10 ** l1 + 10 ** l2) + gas))
    iM31, iMW = uidx("MESSIER031"), uidx("MilkyWay")
    Mlg_kk = (0.6 / UPS_KK) * (10 ** 10.79 + 10 ** 10.70) + 1.33 * (10 ** U_HI[iM31] + 10 ** U_HI[iMW])
    STK = {}
    for f in FOOTS:
        est = [(g, nc, Mb, estimators(Mb, f)) for g, nc, Mb in stk]
        wn = np.array([nc for _, nc, _, _ in est], float)
        true_w = float(np.sum(wn * np.array([e[0]["true"] for *_, e in est])) / wn.sum())
        Rp, Vp, Wp, Lp = [], [], [], []
        for (g, nc, Mb, (e, hd)) in est:
            s = hd["live"] & (hd["R"] > 0.7) & (hd["R"] < 3.5)
            Rp.append(hd["R"]); Vp.append(hd["V"]); Wp.append(hd["w"] * nc / hd["w"][s].sum()); Lp.append(hd["live"])
        e14p = fit_eq14(np.concatenate(Rp), np.concatenate(Vp), np.concatenate(Wp), np.concatenate(Lp))[0]
        lgk, _ = estimators(Mlg_kk, f)
        STK[f] = dict(true_w=true_w, eq14_pooled=e14p, per_group={g: (Mb, e["true"], e["eq14"]) for g, nc, Mb, (e, hd) in est},
                      LG_kk=dict(M=Mlg_kk, true=lgk["true"], eq14=lgk["eq14"]))
    dstk = {f: dex(STK[f]["true_w"], KK18_STACK[0]) for f in FOOTS}
    P(f"    stack of 14 LV groups (K&K 2018, 66 companions of 11 groups): model (companion-weighted true R0) {STK['canonical']['true_w']:.3f} / "
      f"{STK['alt']['true_w']:.3f} vs {KK18_STACK[0]} +- {KK18_STACK[1]} -> delta {dstk['canonical']:+.3f} / {dstk['alt']:+.3f}; per group (can): "
      + ", ".join(f"{g} {v[0]:.2e}: {v[1]:.2f}" for g, v in STK["canonical"]["per_group"].items()))
    ov = lambda d: d[0] > BAND and d[1] > BAND
    v1 = ov(D0["M81"]) and ov(D0["IC342"]) and all(dstk[f] > BAND for f in FOOTS)
    check("V1 NOT LG-ONLY: M81 and IC 342 overshoot their published R0 beyond +0.10 dex on both footings (primary set), and so does "
          "the 14-group stack of K&K 2018 -- the overshoot is not the Local Group's alone",
          f"M81 {D0['M81'][0]:+.3f}/{D0['M81'][1]:+.3f}, IC 342 {D0['IC342'][0]:+.3f}/{D0['IC342'][1]:+.3f}, stack {dstk['canonical']:+.3f}/{dstk['alt']:+.3f}; "
          f"LG {D0['LG'][0]:+.3f}/{D0['LG'][1]:+.3f} dex", v1,
          reading=f"significance with quoted errors + the mass band: M81 {D0['M81'][0] / SIG['M81']:.1f} sigma, IC 342 {D0['IC342'][0] / SIG['IC342']:.1f} sigma, "
                  f"LG {D0['LG'][0] / SIG['LG']:.1f} sigma (canonical)")
    fit_c = lambda d: abs(d[0]) <= BAND and abs(d[1]) <= BAND
    v2 = fit_c(D0["CenA"]) and fit_c((dcen["canonical"], dcen["alt"]))
    check("V2 CEN A FITS: the chain's law matches Cen A's published R0 within +-0.10 dex on both footings, with and without M83's "
          "baryons merged into the group", f"Cen A alone {D0['CenA'][0]:+.3f} / {D0['CenA'][1]:+.3f}; with M83 {dcen['canonical']:+.3f} / {dcen['alt']:+.3f} dex "
          f"(R0 = {MEAS['CenA'][0][0]} +- {MEAS['CenA'][0][1]}, {MEAS['CenA'][0][2]})", v2,
          reading=("the one group whose measured R0 is as large as the chain's: in LCDM terms Cen A is the heavy one (M_T(<R0) = 6.0e12 "
                   "vs 1.3e12 for the LG and 1.0e12 for M81, same method family)") if v2 else "Cen A overshoots under the scored law")
    # V3 robustness of the label
    LAB = {}
    LAB["primary / true R0 / nominal mass"] = label(D0)
    LAB["K05 homogeneous set (Cen A with M83 merged)"] = label(deltas(1, cen_complex=True))
    LAB["K05 homogeneous set (Cen A alone)"] = label(deltas(1))
    LAB["primary / model lin-fit R0"] = label(deltas(0, est="lin"))
    LAB["primary / model eq.14 R0"] = label(deltas(0, est="eq14"))
    LAB["primary / mass band low"] = label(deltas(0, mkey="lo"))
    LAB["primary / mass band high"] = label(deltas(0, mkey="hi"))
    VERD = LAB["primary / true R0 / nominal mass"][0]
    for k_, (lab, cls) in LAB.items():
        P(f"    rule on {k_:44s}: {lab:9s}  " + ", ".join(f"{s_}: {c_}" for s_, c_ in cls.items()))
    check("V3 (reported) THE VERDICT BY THE DECLARED RULE, and its robustness to the R0 set, the model's estimator and the mass band",
          f"primary: {VERD}; " + "; ".join(f"{k_}: {v[0]}" for k_, v in LAB.items() if k_ != "primary / true R0 / nominal mass"),
          True, load_bearing=False)
    # V4 mean / scatter; common offset; LG-relative (K05's one table)
    V4 = {}
    for f_i, f in enumerate(FOOTS):
        ds = np.array([D0[k_][f_i] for k_ in ("LG",) + SCORED_EXT]); ss = np.array([SIG[k_] for k_ in ("LG",) + SCORED_EXT])
        wc = 1 / ss ** 2; dc = float(np.sum(wc * ds) / np.sum(wc)); c2 = float(np.sum((ds - dc) ** 2 * wc))
        ds3 = ds[[0, 1, 3]]; ss3 = ss[[0, 1, 3]]; w3 = 1 / ss3 ** 2; dc3 = float(np.sum(w3 * ds3) / np.sum(w3)); c23 = float(np.sum((ds3 - dc3) ** 2 * w3))
        V4[f] = dict(mean=float(ds.mean()), scatter=float(ds.std(ddof=1)), common=dc, chi2=c2, p=float(chi2_dist.sf(c2, len(ds) - 1)),
                     common_noCenA=dc3, chi2_noCenA=c23, p_noCenA=float(chi2_dist.sf(c23, 2)))
    D1 = deltas(1); D1c = deltas(1, cen_complex=True)
    rel = {k_: (D1[k_][0] - D1["LG"][0], D1[k_][1] - D1["LG"][1]) for k_ in SCORED_EXT}
    rel_c = (D1c["CenA"][0] - D1c["LG"][0], D1c["CenA"][1] - D1c["LG"][1])
    check("V4 (reported) THE OVERSHOOT'S MEAN AND SCATTER over the scored systems (LG, M81, Cen A, IC 342; primary set), a common-"
          "offset chi^2 with and without Cen A, and the LG-relative offsets in K05's single table (one author, one method: the "
          "estimator cancels)", "; ".join(f"{f}: mean {V4[f]['mean']:+.3f}, scatter {V4[f]['scatter']:.3f} dex; common offset {V4[f]['common']:+.3f} "
                                          f"(chi^2 {V4[f]['chi2']:.1f}/3, p {V4[f]['p']:.1e}); without Cen A {V4[f]['common_noCenA']:+.3f} (chi^2 "
                                          f"{V4[f]['chi2_noCenA']:.2f}/2, p {V4[f]['p_noCenA']:.2f})" for f in FOOTS)
          + "; K05 LG-relative delta - delta_LG (can/alt): " + ", ".join(f"{k_} {v[0]:+.3f}/{v[1]:+.3f}" for k_, v in rel.items())
          + f", CenA+M83 {rel_c[0]:+.3f}/{rel_c[1]:+.3f}", True, load_bearing=False,
          reading="LG-relative ~0 = the group shares the LG's overshoot (universal); ~ -delta_LG (-0.2) = it does not (LG-only)")
    # V5 the stack and the LG in one paper, one estimator
    rel_stk = {f: dex(STK[f]["eq14_pooled"], STK[f]["LG_kk"]["eq14"]) - dex(KK18_STACK[0], KK18_LG[0]) for f in FOOTS}
    d14 = {f: (dex(STK[f]["eq14_pooled"], KK18_STACK[0]), dex(STK[f]["LG_kk"]["eq14"], KK18_LG[0])) for f in FOOTS}
    check("V5 (reported) THE STACK AND THE LG IN ONE PAPER, ONE ESTIMATOR (K&K 2018: eq. 14, barycentre, minor attractor): the model's "
          "own eq.-14 R0 for the companion-weighted stack and for the LG (K&K's stellar masses on Upsilon_K = 0.6), their offsets, and "
          "the stack-minus-LG offset (estimator and paper systematics cancel)",
          "; ".join(f"{f}: stack eq14 {STK[f]['eq14_pooled']:.3f} vs {KK18_STACK[0]} ({d14[f][0]:+.3f}), LG eq14 {STK[f]['LG_kk']['eq14']:.3f} (M_b "
                    f"{STK[f]['LG_kk']['M']:.2e}) vs {KK18_LG[0]} ({d14[f][1]:+.3f}); stack - LG {rel_stk[f]:+.3f} dex" for f in FOOTS)
          + f"; K&K's own centre/model span {KK18_RANGE[0]}-{KK18_RANGE[1]} Mpc = {dex(KK18_RANGE[1], KK18_STACK[0]):+.3f}/{dex(KK18_RANGE[0], KK18_STACK[0]):+.3f} dex",
          True, load_bearing=False)
    OUT["numbers"]["V"] = dict(delta_primary=D0, sigma=SIG, cenA_with_M83=dcen, M83_prediction=m83, stack=STK, delta_stack=dstk,
                               labels={k_: v[0] for k_, v in LAB.items()}, classes={k_: v[1] for k_, v in LAB.items()}, V4=V4,
                               K05_LG_relative=rel, K05_LG_relative_CenA_M83=rel_c, KK18_stack_minus_LG=rel_stk, KK18_eq14=d14, verdict=VERD)
    P(f"    {el()}")

    # ============================================================================================= U the universal fix
    banner("U  IF THE OVERSHOOT WERE UNIVERSAL: what outer-profile change would remove it, and can the chain's action supply it? ((H_Y))")
    targets = {"M81": (mass["M81"]["nominal"], MEAS["M81"][0]), "IC342": (mass["IC342"]["nominal"], MEAS["IC342"][0]),
               "LG@k02": (1.145e11, MEAS["LG"][0]), "stack": (float(np.median([Mb for _, _, Mb in stk])), (KK18_STACK[0], KK18_STACK[1], KK18)),
               "CenA": (mass["CenA"]["nominal"], MEAS["CenA"][0]), "CenA(K05)": (mass["CenA+M83"]["nominal"], MEAS["CenA"][1])}
    KN = {}
    Mtyp = targets["stack"][0]
    for f in FOOTS:
        try:
            L_star = brentq(lambda L_: R0_true(Mtyp, f, "HY", L25=L_) - KK18_STACK[0], 0.25, HEAD["L25"], xtol=2e-3)
        except ValueError:
            L_star = float("nan")
        try:
            ly_star = brentq(lambda ly: R0_true(Mtyp, f, "HY", y25=10 ** ly) - KK18_STACK[0], -6.0, -2.0, xtol=2e-3); y_star = 10 ** ly_star
        except ValueError:
            y_star = float("nan")
        KN[f] = dict(L25=L_star, y25=y_star,
                     kids_L=(kids_class(A0[f], L_star, yz(0.25), YIELD) - KB[f]) if L_star == L_star else float("nan"),
                     kids_y=(kids_class(A0[f], HEAD["L25"], yz(0.25, y_star), YIELD) - KB[f]) if y_star == y_star else float("nan"),
                     sparc_L=sparc_gate(f, L25=L_star) if L_star == L_star else float("nan"),
                     sparc_y=sparc_gate(f, y25=y_star) if y_star == y_star else float("nan"))
    u1 = all(KN[f]["kids_L"] > 9.0 and KN[f]["kids_y"] > 9.0 for f in FOOTS)
    check("U1 THE CHAIN'S OWN KNOBS CANNOT DO THE UNIVERSAL FIX: the band-pass length L(0.25) (n fixed) or the yield y_th(0.25) (p' "
          "fixed) that brings the typical group (the stack's median M_b) to the stack's R0 = 0.93 costs KiDS d chi^2 > +9 on both "
          "footings (FP9's gate) -- and FP11 X1 found no L(0.25) that keeps the MW-M31 timing in the window at R0 ~ 1",
          "; ".join(f"{f}: L(0.25) {KN[f]['L25']:.3f} Mpc -> KiDS {KN[f]['kids_L']:+.0f}, SPARC {KN[f]['sparc_L']:.1e} dex | y_th(0.25) {KN[f]['y25']:.2e} -> "
                    f"KiDS {KN[f]['kids_y']:+.0f}, SPARC {KN[f]['sparc_y']:.1e} dex" for f in FOOTS) + f" (headline: L 1.3, y 1e-6; KiDS allows +9; M_typ {Mtyp:.2e})",
          u1, reading="both knobs act on the same 0.3-1.5 Mpc phantom that KiDS's isolated lenses measure at z ~ 0.25; on FP9's SPARC gate "
                      "grid (tolerance 0.01 dex, which reaches 0.39 Mpc at its 1e12 / y = 0.01 corner) the band-pass knob gives "
                      + ", ".join(f"{KN[f]['sparc_L']:.3f}" for f in FOOTS) + " and the yield knob " + ", ".join(f"{KN[f]['sparc_y']:.3f}" for f in FOOTS)
                      + " dex (" + ("the L knob also breaks SPARC's corner" if any(KN[f]["sparc_L"] > 0.01 for f in FOOTS) else "SPARC holds") + ")")
    # U2 the generic change
    FN, ZN = {}, {}
    for lab, (Mb, (Rm, em, src)) in targets.items():
        for f in FOOTS:
            def fneed(Rt):
                try:
                    return brentq(lambda x: R0_true(Mb, f, "HY", fp=fprof(x)) - Rt, 0.02, 3.0, xtol=2e-3)
                except ValueError:
                    return float("nan")
            FN[(lab, f)] = (fneed(Rm), fneed(Rm - em), fneed(Rm + em))
            try:
                ZN[(lab, f)] = brentq(lambda z: R0_true(Mb, f, "HY", zon=z) - Rm, 0.005, 3.0, xtol=2e-3)
            except ValueError:
                ZN[(lab, f)] = float("nan")
    for lab in targets:
        P(f"    {lab:10s} target R0 {targets[lab][1][0]:.2f} +- {targets[lab][1][1]:.2f}: f needed (r > {RS_FIX} Mpc) can {FN[(lab, 'canonical')][0]:.3f} "
          f"[{FN[(lab, 'canonical')][1]:.3f}, {FN[(lab, 'canonical')][2]:.3f}], alt {FN[(lab, 'alt')][0]:.3f}; phantom switched on only after z_on = "
          f"{ZN[(lab, 'canonical')]:.3f} / {ZN[(lab, 'alt')]:.3f}" + ("  (no switch-off needed: the unmodified law already reaches it)" if ZN[(lab, 'canonical')] != ZN[(lab, 'canonical')] else ""))
    RR = M6["RR"]; kids_chi2 = M6["kids_chi2"]

    def kids_f(f, fsc):
        def Mf(Mb):
            return Mb + np.interp(RR, RG, phantom(Mb, A0[f], HEAD["L25"] * MPC, yz(0.25), YIELD) * fprof(fsc)(RG))
        return kids_chi2(Mf) - KB[f]
    kf = {(f, x): kids_f(f, x) for f in FOOTS for x in (1.0, FT, 0.5, 0.8)}
    SP = read_sparc()

    def sparc_f(f, fsc):
        worst = (0.0, None)
        for name_, rl, Mb in SP:
            r = rl * KPC; ph = phantom(Mb * MSUN, A0[f], F11.L_of_a(1.0), F11.yth_of_a(1.0), YIELD)
            gph = G * np.interp(r, RG, ph) / r ** 2; gN = G * Mb * MSUN / r ** 2
            dv = math.log10((gN + fprof(fsc)(r) * gph) / (gN + gph))
            if abs(dv) > abs(worst[0]): worst = (dv, name_)
        return worst
    spf = {f: sparc_f(f, FT) for f in FOOTS}
    # the timing under f = FT (pool)
    TF = {f: [] for f in FOOTS}
    for a_ in AF:
        (f, Mb, fsc), vr, dt = a_.get(); TF[f].append((Mb, vr))
    ok9 = {f: [v for Mb, v in TF[f] if Mb == MT_LG[f]][0]["unscaled"] for f in FOOTS}
    ref9v = {f: F11J["matched"][f"HY/A/{f}"]["branch"]["vr"] for f in FOOTS}
    check("K9 CONTROL: FP11's two-body force table and first-approach shooter at FP11's timing mass return FP11's committed v_r (the "
          "machinery the timing cost below uses)", f"{ok9['canonical']:+.4f} / {ok9['alt']:+.4f} vs {ref9v['canonical']:+.4f} / {ref9v['alt']:+.4f} km/s",
          all(abs(ok9[f] - ref9v[f]) < 0.05 for f in FOOTS))
    TMF = {}
    for f in FOOTS:
        pts = sorted((Mb, v["scaled"]) for Mb, v in TF[f]); Mt = interp_mass(pts)
        TMF[f] = dict(pts=pts, M=Mt, R0=(R0_true(Mt, f, "HY", fp=fprof(FT)) if Mt else float("nan")))
        P(f"    timing with f = {FT} ({f}): first-approach v_r " + ", ".join(f"{Mb:.2e}: {v:+.1f}" for Mb, v in pts)
          + (f" -> timing mass {Mt:.3e} (window [{F11.MB_LO:.3e}, {F11.MB_HI:.3e}]); merged R0 at it with f = {FT}: {TMF[f]['R0']:.3f} Mpc" if Mt else " -> not bracketed"))
    check("U2 (reported) THE REQUIRED OUTER-PROFILE CHANGE: the factor f on the phantom beyond ~0.3 Mpc (all epochs) or the latest "
          "switch-on epoch z_on that brings each group to its measured R0; the KiDS cost of f; SPARC's outermost points; the MW-M31 "
          "timing under it (FP11's two-body law with its mutual MOND part scaled the same way)",
          "; ".join(f"{lab}: f {FN[(lab, 'canonical')][0]:.2f}/{FN[(lab, 'alt')][0]:.2f}, z_on {ZN[(lab, 'canonical')]:.2f}" for lab in targets)
          + "; KiDS d chi^2 at f = " + ", ".join(f"{x}: {kf[('canonical', x)]:+.0f}/{kf[('alt', x)]:+.0f}" for x in (FT, 0.5, 0.8, 1.0))
          + f"; SPARC's outermost points at f = {FT}: worst {spf['canonical'][0]:+.1e} dex ({spf['canonical'][1]}) / {spf['alt'][0]:+.1e}"
          + "; LG timing mass at f = " + f"{FT}: " + ", ".join((f"{f[:3]} {TMF[f]['M']:.2e} (R0 there {TMF[f]['R0']:.2f})" if TMF[f]["M"] else f"{f[:3]} > {max(TM_SCAN[f]):.1e}") for f in FOOTS),
          True, load_bearing=False,
          reading="the typical group needs ~70% of its outer phantom removed at every epoch, or no phantom before z ~ 0.1-0.2; KiDS's "
                  "isolated lenses at z ~ 0.25 see the full phantom out to ~1 Mpc, and the MW-M31 pair (0.3-1 Mpc apart for the last "
                  "~8 Gyr) loses the same pull, so its timing mass leaves the baryonic window -- FP11's internal pincer, now on the "
                  "outer profile itself")
    # U3 no universal f
    ivl = lambda lab, f: (min(x for x in FN[(lab, f)] if x == x), max(x for x in FN[(lab, f)] if x == x))
    rest = ("M81", "IC342", "LG@k02", "stack")
    u3 = all(ivl("CenA", f)[0] > max(ivl(lab, f)[1] for lab in rest) for f in FOOTS)
    check("U3 NO UNIVERSAL OUTER PROFILE FITS CEN A AND THE REST: the phantom factor f that Cen A needs (its R0 +- 1 sigma) does not "
          "overlap the f the LG, M81, IC 342 and the stack need, on both footings -- in a baryon-only law with one outer profile, the "
          "groups' R0 are not a function of M_b alone",
          "; ".join(f"{f}: Cen A [{ivl('CenA', f)[0]:.2f}, {ivl('CenA', f)[1]:.2f}] vs the rest up to {max(ivl(lab, f)[1] for lab in rest):.2f} "
                    f"(M81 [{ivl('M81', f)[0]:.2f}, {ivl('M81', f)[1]:.2f}], IC 342 [{ivl('IC342', f)[0]:.2f}, {ivl('IC342', f)[1]:.2f}], LG [{ivl('LG@k02', f)[0]:.2f}, "
                    f"{ivl('LG@k02', f)[1]:.2f}], stack [{ivl('stack', f)[0]:.2f}, {ivl('stack', f)[1]:.2f}])" for f in FOOTS)
          + f"; K05's Cen A/M83 (1.26 +- 0.15, M83 merged): [{ivl('CenA(K05)', 'canonical')[0]:.2f}, {ivl('CenA(K05)', 'canonical')[1]:.2f}]", u3)
    OUT["numbers"]["U"] = dict(knobs=KN, f_needed={f"{k_[0]}/{k_[1]}": v for k_, v in FN.items()}, z_on={f"{k_[0]}/{k_[1]}": v for k_, v in ZN.items()},
                               kids_f={f"{k_[0]}/{k_[1]}": v for k_, v in kf.items()}, sparc_f=spf, timing_f=TMF, f_typ=FT, M_typ=Mtyp)
    P(f"    {el()}")

    # ============================================================================================= E environment
    banner("E  THE ENVIRONMENT: what could separate Cen A from the LG, M81, IC 342 and the stack?")
    sepCM = float(group_frame(uidx("NGC5128"))[0][uidx("NGC5236")])
    Rchain_eq = {f: 1.95e12 * rows_R1["M81"]["can" if f == "canonical" else "alt"]["true"] ** 3 for f in FOOTS}
    P(f"    (a) Cen A and M83 form an LG-analog binary: {BENISTY26[2]} find them infalling toward each other, timing mass "
      f"{BENISTY26[0]:.2e} +- {BENISTY26[1]:.1e}; in the committed UNGC M83 lies {sepCM:.2f} Mpc from Cen A, i.e. AT Cen A's zero-velocity "
      f"surface (1.40 +- 0.11): Cen A's R0 is read in the joint field of a pair; merging M83's baryons moves the model by "
      f"{dex(MOD[('CenA+M83', 'canonical')]['est']['true'], MOD[('CenA', 'canonical')]['est']['true']):+.3f} dex (V2 holds either way)")
    P(f"    (b) LCDM reads Cen A as the heavy one: M_T(<R0) = {MT_LCDM['CenA'][0]:.1e} ({K07}) vs LG {MT_LCDM['LG'][0]:.2e} and M81 "
      f"{MT_LCDM['M81'][0]:.2e} ({KK06}); K05 Table 11 M_t/L_B: " + ", ".join(f"{k_} {v}" for k_, v in K05_T11_MtLB.items())
      + f".  The chain's R0 for ~1e11 of baryons ({rows_R1['M81']['can']['true']:.2f} Mpc) is, in K&K 2018's eq. 4 (Planck), the R0 of M_T = "
      f"{Rchain_eq['canonical']:.1e} = {Rchain_eq['canonical'] / MT_LCDM['CenA'][0]:.1f}x Cen A's measured M_T and "
      f"{Rchain_eq['canonical'] / MT_LCDM['LG'][0]:.1f}x the LG's: the chain gives EVERY group of ~1e11 baryons the dynamical mass of a Cen A-class group")
    P(f"    (c) position: K05 Table 10 SGZ [Mpc]: " + ", ".join(f"{k_} {v:+.2f}" for k_, v in K05_T10_SGZ.items())
      + " -- Cen A lies 0.33 Mpc below the Local Sheet, the others in it")
    P("    (d) the external field cannot be the lever in (H_Y): its band-pass passes no uniform field (h(k = 0) = 0; FP11 P1), and a "
      "neighbour 3-4 Mpc away is nearly uniform across a 1 Mpc infall region; a non-uniform (tidal) field survives the band-pass only "
      "on scales <~ L(0) = 1.7 Mpc")
    check("E1 (reported) THE ENVIRONMENT: the LG is not special among the groups that overshoot (M81 and IC 342 sit in the Local Sheet "
          "as the LG does, K05 SGZ +0.04 / +0.02 Mpc, and each is paired with a massive companion as the LG is: M82 and Maffei 2, "
          "K&K 2018 lg M* 10.59 and 10.86), so the LG's own environment is not the cause; what distinguishes Cen A is its binary "
          "with M83 at its zero-velocity surface, its off-sheet position, and its large LCDM mass -- an ingredient the baryon-only law "
          "does not carry", f"Cen A-M83 {sepCM:.2f} Mpc; SGZ Cen A {K05_T10_SGZ['CenA']:+.2f} vs {K05_T10_SGZ['M81']:+.2f}/{K05_T10_SGZ['IC342']:+.2f}/"
          f"{K05_T10_SGZ['LG']:+.2f}; M_T/L_B Cen A {K05_T11_MtLB['CenA']} vs {K05_T11_MtLB['LG']}/{K05_T11_MtLB['M81']}/{K05_T11_MtLB['IC342']}",
          True, load_bearing=False)
    OUT["numbers"]["E"] = dict(sep_CenA_M83=sepCM, chain_equivalent_MT=Rchain_eq, SGZ=K05_T10_SGZ, MtLB=K05_T11_MtLB)

    # ============================================================================================= G gates
    banner("G  THE OTHER GATES")
    check("G1 THE OTHER GATES ARE UNCHANGED: this lane adds no term to the action -- every (H_Y) number uses FP9's four constants as "
          "committed (K7 reproduces FP9's flagship, SPARC and KiDS exactly); the U section's changes are diagnostics, not adopted",
          f"flagship {min(flag.values()):+.4f}..{max(flag.values()):+.4f} dex, SPARC {max(sparc.values()):.1e} dex, KiDS {kids['canonical']:+.1f}/{kids['alt']:+.1f}; "
          f"new action terms: 0", d7 < 1e-9)
    pool.close(); pool.join()

    # ============================================================================================= W ledger
    banner("W  THE LEDGER: FP12, the zero-velocity radii of the Local Volume groups in the chain's law")
    f2 = lambda d: f"{d[0]:+.2f}/{d[1]:+.2f}"
    LEDGER = [
        ("F12a", f"the chain's R0 of an isolated group ({'(H_Y)' if SCORED == 'HY' else 'plain P2, MUTATE'}): M81 {rows_R1['M81']['can']['true']:.2f}/{rows_R1['M81']['alt']['true']:.2f}, "
                 f"Cen A {rows_R1['CenA']['can']['true']:.2f}/{rows_R1['CenA']['alt']['true']:.2f}, M83 {rows_R1['M83']['can']['true']:.2f}/{rows_R1['M83']['alt']['true']:.2f}, "
                 f"IC 342 {rows_R1['IC342']['can']['true']:.2f}/{rows_R1['IC342']['alt']['true']:.2f} Mpc (can/alt) at k02's baryons; d log R0/d log M_b = "
                 f"{slope['canonical']:.2f}", "DERIVED", "R1, K5 (FP11's tracer machinery = FP6's shells), K1-K3 (FP9/FP11 reproduced)"),
        ("F12b", "the groups as merged point masses on their own Hubble flow from a = 0.02, no neighbour tides; binary geometry <= +0.016 "
                 "(FP11 R2); baryons = k02's UNGC accounting (0.6 L_K + 1.33 M_HI) with a band (Upsilon_K 0.5-1.0, aperture 0.7-1.5 Mpc, "
                 "x1.4 unseen gas)", "POSTULATED", "M1, K4 (k02 re-derived), K8"),
        ("F12c", "the record's UNGC R0 of M81, Cen A, M83 and IC 342 (k02) are not measurements: they move by more than twice their "
                 "bootstrap error under window / distance-quality changes; the published R0 (read at source) carry the test",
         "CONSTRAINT", "S1 (and the record's XR4 N2, k_dimensional K3.2/K3.3)"),
        ("F12d", f"the overshoot is NOT the Local Group's alone: M81 {f2(D0['M81'])}, IC 342 {f2(D0['IC342'])}, the 14-group stack "
                 f"{dstk['canonical']:+.2f}/{dstk['alt']:+.2f} dex, like the LG's {f2(D0['LG'])} (FP11); LG, M81 and IC 342 share one offset "
                 f"({V4['canonical']['common_noCenA']:+.3f}, chi^2 p = {V4['canonical']['p_noCenA']:.2f}); with K&K 2018's own eq.-14 estimator on the model "
                 f"the stack reads {d14['canonical'][0]:+.2f}/{d14['alt'][0]:+.2f} and the same paper's LG {d14['canonical'][1]:+.2f}/{d14['alt'][1]:+.2f} dex "
                 f"(stack minus LG {rel_stk['canonical']:+.3f})", "FAILS" if v1 else "DERIVED", "V1, V4, V5"),
        ("F12e", (f"Cen A is matched: {f2(D0['CenA'])} dex alone, {dcen['canonical']:+.2f}/{dcen['alt']:+.2f} with M83's baryons -- the one group "
                  "whose measured R0 is as large as the chain's") if v2 else
                 (f"Cen A is NOT matched by the scored law: {f2(D0['CenA'])} dex alone, {dcen['canonical']:+.2f}/{dcen['alt']:+.2f} with M83's "
                  "baryons (outside the +-0.10 band)"), "DERIVED" if v2 else "FAILS", "V2"),
        ("F12f", f"the verdict by the declared rule: {VERD} (mean delta {V4['canonical']['mean']:+.3f}/{V4['alt']['mean']:+.3f}, scatter "
                 f"{V4['canonical']['scatter']:.3f}/{V4['alt']['scatter']:.3f} dex over LG, M81, Cen A, IC 342; common offset without Cen A "
                 f"{V4['canonical']['common_noCenA']:+.3f}, chi^2 p = {V4['canonical']['p_noCenA']:.2f}; with it p = {V4['canonical']['p']:.1e})",
         "FAILS", "V3, V4 (robustness: " + ", ".join(sorted(set(v[0] for v in LAB.values()))) + ")"),
        ("F12g", f"the universal fix needs the phantom beyond ~0.3 Mpc cut to f = {min(FN[(l_, 'canonical')][0] for l_ in rest):.2f}-{max(FN[(l_, 'canonical')][0] for l_ in rest):.2f} "
                 f"(all epochs), or no phantom before z_on = {min(ZN[(l_, 'canonical')] for l_ in rest):.2f}-{max(ZN[(l_, 'canonical')] for l_ in rest):.2f}; KiDS "
                 f"d chi^2 at f = {FT}: {kf[('canonical', FT)]:+.0f}/{kf[('alt', FT)]:+.0f} (<= +9 allowed); SPARC's outer points move <= {abs(spf['canonical'][0]):.0e} dex",
         "CONSTRAINT", "U2"),
        ("F12h", f"no action-level term of the chain supplies it: L(0.25) -> {KN['canonical']['L25']:.2f} Mpc costs KiDS {KN['canonical']['kids_L']:+.0f} (and FP9's "
                 f"SPARC gate {KN['canonical']['sparc_L']:.3f} dex vs 0.01), y_th(0.25) -> {KN['canonical']['y25']:.1e} costs KiDS {KN['canonical']['kids_y']:+.0f} "
                 f"(can); with f = {FT} the MW-M31 timing mass becomes "
                 + ", ".join((f"{TMF[f]['M']:.2e}" if TMF[f]["M"] else f"> {max(TM_SCAN[f]):.0e}") for f in FOOTS) + f" (window <= {F11.MB_HI:.1e})",
         "FAILS", "U1, U2, FP11 X1"),
        ("F12i", f"no universal outer profile fits Cen A and the rest: Cen A needs f in [{ivl('CenA', 'canonical')[0]:.2f}, {ivl('CenA', 'canonical')[1]:.2f}], "
                 f"the others <= {max(ivl(l_, 'canonical')[1] for l_ in rest):.2f}; the measured R0 are not a function of M_b alone", "FAILS" if u3 else "OPEN", "U3"),
        ("F12j", f"open: M83 has no published R0 (the chain predicts {m83[0]:.2f}/{m83[1]:.2f} Mpc); one estimator (eq. 14) refit around every "
                 "group from the same catalogue; a two-body Cen A/M83 model (an LG analog); what separates Cen A (its binary, its "
                 "off-sheet position, its mass budget); an action term that weakens the time-integrated pull on infall regions ~3x "
                 "while KiDS's isolated lenses keep the full phantom", "OPEN", "scope; not computed here"),
    ]
    for k_, what, status, why in LEDGER:
        P(f"    {k_:5s} {status:11s} {what}  --  {why}")
    OUT["ledger"] = [dict(link=k_, what=w, status=s_, basis=b_) for k_, w, s_, b_ in LEDGER]
    check("W (reported) the ledger of this lane", f"{len(LEDGER)} links", True, load_bearing=False)

    # ============================================================================================= verdict
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    banner("VERDICT")
    P(f"  The Local Volume groups in the chain's law ({'(H_Y), FP9 constants' if SCORED == 'HY' else 'plain P2 root, MUTATE'}; both footings; true zero-velocity radius):")
    P(f"    {'group':8s} {'M_b [Msun]':>11s} {'model R0 can/alt':>17s} {'measured R0':>18s} {'overshoot can/alt [dex]':>24s}")
    P(f"    {'LG':8s} {MT_LG['canonical']:11.3e} {LG_MODEL['canonical']:8.3f} / {LG_MODEL['alt']:5.3f} {MEAS['LG'][0][0]:9.2f} +- {MEAS['LG'][0][1]:.2f} "
      f"{D0['LG'][0]:+13.3f} / {D0['LG'][1]:+.3f}   (FP11)")
    for k_ in EXT:
        mm = MEAS[k_][0]
        if mm:
            P(f"    {k_:8s} {mass[k_]['nominal']:11.3e} {rows_R1[k_]['can']['true']:8.3f} / {rows_R1[k_]['alt']['true']:5.3f} {mm[0]:9.2f} +- {mm[1]:.2f} "
              f"{D0[k_][0]:+13.3f} / {D0[k_][1]:+.3f}")
        else:
            P(f"    {k_:8s} {mass[k_]['nominal']:11.3e} {rows_R1[k_]['can']['true']:8.3f} / {rows_R1[k_]['alt']['true']:5.3f} {'(none published)':>18s} {'unscored':>24s}")
    P(f"    {'stack':8s} {Mtyp:11.3e} {STK['canonical']['true_w']:8.3f} / {STK['alt']['true_w']:5.3f} {KK18_STACK[0]:9.2f} +- {KK18_STACK[1]:.2f} "
      f"{dstk['canonical']:+13.3f} / {dstk['alt']:+.3f}   (14 groups, K&K 2018)")
    P(f"  VERDICT (declared rule): {VERD}.  Mean {V4['canonical']['mean']:+.3f} / {V4['alt']['mean']:+.3f} dex, scatter {V4['canonical']['scatter']:.3f} / "
      f"{V4['alt']['scatter']:.3f} over LG, M81, Cen A, IC 342.")
    s_v1 = "NOT the LG's alone (M81, IC 342 and the stack share it)" if v1 else "not shared by M81, IC 342 and the stack"
    s_v2 = "it is not universal either (Cen A fits)" if v2 else "every scored group overshoots (Cen A too)"
    P(f"    The overshoot is {s_v1}; {s_v2}.  Relative to the LG in K05's one table: " + ", ".join(f"{k_} {v[0]:+.2f}" for k_, v in rel.items()) + ".")
    fr_ = [FN[(l_, "canonical")][0] for l_ in rest]
    cen_under = [-dex(R0_true(mass["CenA"]["nominal"], "canonical", "HY", fp=fprof(x)), MEAS["CenA"][0][0]) for x in (min(fr_), max(fr_))]
    P(f"    A universal fix needs f = {min(fr_):.2f}-{max(fr_):.2f} on the phantom beyond 0.3 Mpc (LG, M81, IC 342, stack; can); the chain's knobs cost "
      f"KiDS {KN['canonical']['kids_L']:+.0f} (L) / {KN['canonical']['kids_y']:+.0f} (y_th); the generic cut (f = {FT}) costs KiDS {kf[('canonical', FT)]:+.0f} and "
      + (f"forces an LG timing mass {TMF['canonical']['M']:.1e} (R0 there {TMF['canonical']['R0']:.2f} Mpc)" if TMF["canonical"]["M"] else "leaves the LG timing unbracketed"))
    P(f"    and it would leave Cen A {min(cen_under):.2f}-{max(cen_under):.2f} dex BELOW its measured R0.  Not 'closed'.  Time {time.time() - T0:.0f} s.")
    OUT["numbers"]["verdict_fix"] = dict(f_range=[min(fr_), max(fr_)], cenA_undershoot=cen_under)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))

    def enc(o):
        if isinstance(o, np.ndarray): return o.tolist()
        if isinstance(o, (np.floating, np.integer)): return float(o)
        if isinstance(o, (np.bool_,)): return bool(o)
        return str(o)

    def clean(o):
        if isinstance(o, dict):
            return {(k_ if isinstance(k_, str) else str(k_)): clean(v) for k_, v in o.items() if k_ not in ("hd",)}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        return o
    json.dump(clean(OUT), open(fn, "w"), indent=1, default=enc)
    P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}")
    sys.exit(0 if nlb == 0 else 1)


if __name__ == "__main__":
    main()
