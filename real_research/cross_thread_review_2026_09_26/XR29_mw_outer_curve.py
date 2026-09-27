#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR29_mw_outer_curve.py -- THE MILKY WAY'S OUTER ROTATION CURVE IN THE DERIVATION CHAIN'S LAW: does the chain's static law
reproduce the Gaia-era circular-velocity curves out to 25-30 kpc, including the decline that some analyses read as Keplerian
and present as evidence against MOND?  Independent cross-thread review (2026-09-27).  Read-only on every other file: the
record's Milky Way AQUAL code (real_research/reviews/mi_aqual_mcmillan2017_2026.py, run whole and captured as a control;
mi_aqual_mond_refit_2026.py, its definitions exec'd), FP7's dual (flux) Kacanov solver (its source slice exec'd), FP11's two-body
machinery (exec'd with __name__ != '__main__', and through it FP6's band-pass), FP0's footings and the committed data files.

WHY.  The record's vertical-force front (mi_aqual_mcmillan2017_2026 6fb320dda, mi_aqual_mond_refit_2026 dd0230dbf) found that a
full AQUAL solve with the alpha = 2 ('standard') kernel on McMillan 2017's baryons gets the local vertical force right and the
Eilers et al. 2019 slope right, and misses only the circular-speed normalisation (v_c(R0) 192-199 vs 233 km/s): a baryon-budget
problem.  That kernel is not the chain's.  The chain's static law is FP7's AQUAL-type root with the P2 primitive; it has never
been run on the Milky Way.  Since then Gaia DR3 curves (Zhou+2023, Jiao+2023, Ou+2024) extend to 25-27 kpc and show a steeper
decline; Jiao+2023 call it Keplerian (vc ~ R^-0.47 +- 0.15 beyond 19 kpc) and Coquery & Blanchard 2025 (A&A 703, A88) conclude
from it that MOND needs a0 < 0.53e-10 m/s^2 (95%).  This lane asks the chain's own law, with a0 fixed by P1 on both footings.

THE LAW (FP7, nothing added; per 1/16 pi G, c = 1).  Static weak field: Phi = Phi_N + chi, chi = S phi, and
      div[ mu_s(|grad phi|/a0) grad phi ] = 4 pi G (S rho),   mu_s(x) = x/(1 - 2x)   (J_P2' = mu_s: P2 exactly for spheres),
  solved in its dual (flux) form: grad phi = w(|F|/a0) F, div F = 4 pi G rho, curl(w F) = 0, w = sqrt(1 + 1/s) - 1 (FP7 A3's
  Kacanov solver on the axisymmetric (R, z >= 0) grid).  S = S_xi - S_L: the heat filter at xi (FP1/FP7 floor 0.024-0.032 pc; the
  chain's window 0.024-~100 pc, FP14/FP17) and FP9's band-pass at L (H_Y: L(0) = 2.4615 Omega_L(0) = 1.690 Mpc; FP13's H_S cell
  L(0) = 2.879 Mpc, pending FP19) with H_Y's yield y_th(0) = 3.5e-7.  The two filters and M31's surviving field are evaluated as
  corrections (F, E below) with the chain's own machinery (FP6's phantom(), FP11's two-body QUMOND-form fields, XR27's reduction).
  The footings (FP0): a0 = 9.3603e-11 (canonical) and 1.1312e-10 m/s^2 (alt); kappa = 1/2 FITTED (Z = kappa = 5.7888).

DATA (each published table read or transcribed with its source; errors as published, systematics as the authors state them):
  E19  Eilers, Hogg, Rix & Ness 2019, ApJ 871, 120, Table 1 (38 pts, 5.27-24.82 kpc; committed real_research/data/mw_rc_eilers2019_
       table1.tsv).  Systematics (their Sect. 5.2, Fig. 4): '2-5% out to R ~ 20 kpc', rising beyond; <~ 3% at R0; slope +-0.46.
       Used: a smoothed by-eye envelope of Fig. 4's total (2-3% to 14 kpc, 4% at 16, 6% at 19, 12% from 22 kpc).
  Z23  Zhou, Li, Huang & Zhang 2023, ApJ 946, 73 (arXiv:2212.10393), Table 4 (34 pts, 5.24-24.00 kpc), transcribed here from the
       arXiv PDF; errors statistical ('systematics not included', Fig. 11).  Systematics (Sect. 4.2.2, Fig. 12): each source
       <~ 1%, the tracer scale length 1.0-1.5% at 25 kpc, cross term 'slightly larger' beyond 18 kpc; v_c(R0) sys 1.36 km/s, slope
       sys 0.07.  Used: envelope 1% to 15 kpc, 1.5% at 18, 2% at 20, 3% at 24 kpc.
  J23  Jiao, Hammer, Wang et al. 2023, A&A 678, A208 (arXiv:2309.00048v4), Table 3 (18 pts, 9.5-26.5 kpc), transcribed here and
       checked against both the arXiv HTML and the PDF; the tabulated sigma ALREADY includes systematics in quadrature (their
       Sect. 2.2.5, Eq. 4: cross term, disc scale length, density profile, sample split).  R0 = 8.34 kpc.
  O24  Ou, Eilers, Necib & Frebel 2024, MNRAS 528, 693 (arXiv:2303.12838), Table 1 (37 pts, 6.27-27.31 kpc; committed
       real_research/data/mw_rc_ou2024_table1.tsv).  Systematics (Sect. 4, Fig. 5): '1% to 5% up to R = 22 kpc, ... total 2-4%',
       beyond 22 kpc 'reaching over 15%'.  Used: a by-eye envelope of Fig. 5's total (3% at 6.3, 2.2% to 13, 3% at 16, 3.6% at
       19, 2.6% at 21, 4% at 22, 15% from 22.7 kpc; Jiao+2023 fn. 4 digitised the same figure, 0.14 where off-chart).
  B22  Bird et al. 2022, MNRAS 516, 731: M(<52 kpc) = 4.1 +- 1.2 (+- 0.6 sys) e11, M(<73 kpc) = 4.3 +- 0.95 (+- 0.6) e11 Msun
       (committed real_research/data/mw_halo_bird2022_jeans.txt): the 30-100 kpc check.
  Critiques carried as context, not as data: Koop et al. 2024 (A&A 692, A50: Jeans-inferred outer curves can be off by up to
  15%, likely ~10% for the MW); Melchiorri & Ruchika 2026 (arXiv:2608.10189, review of the Keplerian-decline debate).

BARYONS (Msun, kpc; the stellar part is scaled by f_* in the fits, gas fixed by 21-cm/CO, CGM separate):
  McM17   McMillan 2017 Table 3 (the record's mass model, taken from its own exec'd constants and verified point-by-point):
          M_* = 5.45e10, gas 1.19e10.
  McM17r  the record's refit cell f_M = 1.30, f_R = 0.90 (mi_aqual_mond_refit_2026's densities(), verified): M_* = 5.70e10.
  Cau20   Cautun et al. 2020, MNRAS 494, 4291, Tables 1-2 (contracted-halo best fit: bulge rho0 = 103, thin 731 Msun/pc^2 / 2.63 kpc,
          thick 101 / 3.80, McMillan's gas): M_* = 5.04e10; with its CGM (rho ~ r^-1.46, 6.4e10 inside R200 = 218 kpc) as
          Cau20+CGM (the CGM range is 0 .. Cautun's).
  Cau20N  Cautun et al. 2020's NFW-halo column (thin 1070 / 2.43, thick 113 / 3.88, bulge 101): M_* = 5.97e10.
  B2      de Salas et al. 2019's B2 as tabulated by Ou+2024 Table 2 and used by Jiao+2023 and Coquery & Blanchard 2025: disc
          3.65e10 (2.35, 0.14), Hernquist bulge 1.55e10 (0.70), HI 8.2e9 (18.24, 0.52), H2 1.3e9 (2.57, 0.08), dust 7.0e7 + 2.2e5.
  Censuses compared with: McMillan 2017 M_* = 5.43 +- 0.57e10; Cautun 2020 5.04 (+0.43/-0.52)e10; Licquia & Newman 2015 (ApJ
  806, 96) 6.08 +- 1.14e10; Bland-Hawthorn & Gerhard 2016 (ARA&A 54, 529) 5 +- 1e10.

CHECKS (controls first; load-bearing unless marked 'reported')
  K1 CONTROL (the record): mi_aqual_mcmillan2017_2026.py run whole with its own code reproduces its committed numbers exactly
     (v_c(R0) 191.9 / 196.1 / 197.6 km/s, Sigma_dyn 71.4 / 74.8 / 76.0, Newtonian v_c(R0) 177.0, simple-kernel 222.7 / 96.5), and
     mi_aqual_mond_refit_2026.py's own observables()/slope_of() give the committed prior-respecting cell (1.30, 0.90): v_c 198.6,
     Sigma_dyn 75.2, slope -1.14 km/s/kpc.
  K2 CONTROL (the chain's solver): FP7's source slice, exec'd, reproduces FP7's committed Plummer control (AQUAL/QUMOND 8.1e-5 dex,
     AQUAL/algebraic 1.6e-4 dex) to 1e-6 relative.
  K3 CONTROL (pure Newton): the grid's Newtonian midplane curve reproduces an independent semi-analytic one (Hankel transform for
     the discs, homoeoid integral for the spheroidal bulge, closed forms for Hernquist and the CGM) to <= 0.3% at 5-100 kpc for
     every baryon model, and McM17's v_N(8.21 kpc) reproduces the record's 177.0 km/s to 0.3 km/s; this lane's McM17 and McM17r
     densities equal the record's own functions to 1e-10.
  K4 CONTROL (numerics): the scan grid agrees with a finer grid (x2 cells per axis) to <= 0.3% at 5-100 kpc, and the cubic
     interpolation in f_* agrees with a direct solve at a fitted f_* to <= 0.2%.
  K5 CONTROL (FP11): the MW-centred interaction field at the Milky Way equals FP11's direct dipole-kernel integral dg_body to
     <= 1e-3 (FP11 K4's control, re-centred).
  F1 the heat filter (xi = 0.03 pc) changes v_c by < 1e-3 at 5-30 kpc: the double filter's leading term xi^2 d^2 g/dz^2 is
     evaluated on the solved field and validated against a direct vertically double-filtered solve at xi = 100 pc.
  F2 the band-pass (H_Y L(0) = 1.690 Mpc, H_S 2.879 Mpc) and H_Y's yield change v_c by < 1e-3 at 5-30 kpc (FP6's phantom()).
  E1 M31 (1.10e11 Msun of baryons, range 0.72-1.51e11, 0.78 Mpc): the surviving fractions of its field at the MW are reported,
     and its tidal + non-linear (EFE) perturbation of the MW's radial field changes v_c by < 1e-3 at 5-30 kpc on the data's
     azimuths (both footings); at 50-100 kpc it is reported and applied.
  T1 [load-bearing; MUTATE must fail] THE LAW SUPPLIES THE OUTER FORCE: fitted to each Gaia curve's points at R >= 15 kpc with the
     McM17 shape, the chain's law needs a stellar mass below 2x McMillan's census (1.09e11 Msun) on both footings (Newton needs
     ~3x).
  S, D, N, X (reported): the scan tables; chi^2 of every curve at the census baryons and at the fitted f_*; the mass each curve
     requires; the decline tests (outer chi^2, the MOND floor at the lowest census mass, the outer power-law slope); the
     LambdaCDM NFW control; a free-a0 DIAGNOSTIC (algebraic P2; a0 is NOT free in the chain) to confront Coquery & Blanchard 2025.
  H1-H8 (reported, pre-declared), and the verdict.

PRE-DECLARED HYPOTHESES (written before any data fit ran; the only runs before them were solver timings, grid/iteration
convergence, one census-baryon McM17 curve and FP11's M31 fields -- disclosed in XR29_README.md; reported as they fall, never
re-worded after the run):
  H1 NORMALISATION: at the census baryons (f_* = 1) the chain's law under-predicts every Gaia curve at 5-12 kpc by >= 15 km/s on
     both footings, for McM17, Cau20 and B2 -- the record's baryon-budget shortfall persists under P2, smaller than alpha = 2's.
  H2 REQUIRED MASS: fitted to each whole curve, the chain's law needs M_* ~ 7-9e10 (canonical) / 6-8e10 (alt) with the McM17 shape:
     > 2 sigma above McMillan's and Cautun's censuses, within ~2 sigma of Licquia & Newman 2015 on the alt footing.
  H3 THE DECLINE: at the whole-curve fitted mass the outer points (R >= 19 kpc) of E19, Z23, J23 and O24 are reproduced within the
     published budgets (p(chi^2_outer) >= 0.01 each), because the law's curve for a concentrated baryonic galaxy itself falls
     from ~230 km/s at R0 toward (G M_b a0)^(1/4) ~ 175-190 km/s; the model's outer power-law slope is shallower than Jiao's
     -0.47 +- 0.15 and Ou's -0.56 (+0.23 -0.22) by 1.5-2.5 sigma -- a tension, not an exclusion.
  H4 THE FLOOR: no point beyond 19 kpc lies more than 2 sigma below the chain's curve for the LOWEST census stellar mass
     (M_* = 3.0e10, Bland-Hawthorn & Gerhard's 2-sigma floor): the decline does not fall below what the allowed baryons give.
  H5 FILTERS AND M31: xi, L and M31 change v_c by < 1e-3 at 5-30 kpc; M31's band-passed field survives at > 90% at the MW but, being
     nearly uniform, perturbs v_c at 100 kpc by < 2%.
  H6 LambdaCDM CONTROL: baryons + NFW with free (M200, c) fit every curve (chi^2/N <= 1 with systematics), but the curves with the
     steep decline (J23, O24) need c above the Dutton & Maccio 2014 c(M) relation by > 2 sigma (0.11 dex).
  H7 MUTATE (a0 -> 0): the law becomes Newton on baryons; T1 fails (the outer curve needs >= 2x the census stellar mass).
  H8 BEYOND 30 kpc: at the whole-curve fitted mass, with the CGM range 0 .. Cautun's, the chain's law is within 1.5 sigma of
     Bird+2022's M(<52 kpc) and M(<73 kpc) (random + 15% systematic).
DECISION RULES (pre-declared).  'REPRODUCES THE DECLINE' if for every Gaia curve, on at least one footing and baryon shape, the
  outer points at the whole-curve fitted mass have p(chi^2_outer) >= 0.01 (published budget), and no outer point lies > 2 sigma
  below the floor curve (H4).  'FAILS THE DECLINE' if any curve has an outer point > 2 sigma below the floor, or p < 0.01 on every
  shape and footing.  The baryon budget is judged separately: 'CONSISTENT' if some shape/footing needs M_* within 2 sigma of
  Licquia & Newman 2015; 'TENSION' otherwise.
MUTATE=1 sets a0 = 0 in the chain's law (the exact limit: |grad phi| < a0/2 by FP7 A2's saturation, so the scalar's force
  vanishes and the law is Newton on baryons): T1 must FAIL (rc = 1).  Outputs XR29_mw_outer_curve_MUTATE.out /
  XR29_mw_outer_curve_results_MUTATE.json.

SCOPE.  Axisymmetric (R, z) solves of the chain's two-field AQUAL law; the filters and M31 as computed corrections (QUMOND form for
the band-pass and the two-body field, as FP9/FP11/XR27 state the law); the data taken as published (steady-state axisymmetric
Jeans curves; the tabulated radii use each paper's own R0); no bar, spiral arms, warp or LMC-induced disequilibrium in the model
(the LMC's static field is estimated and reported, not applied); the NFW control is the standard LambdaCDM fit (Newtonian
baryons + a spherical NFW), not a contracted halo.  At most 3 worker processes; the main run takes ~10-15 minutes.
Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR29_mw_outer_curve.py   (MUTATE=1 first)
"""
import os, sys, io, json, math, time, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spl
from scipy.integrate import quad
from scipy.special import j0, j1, i0, i1, k0, k1
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar, minimize, brentq
from scipy.stats import chi2 as CHI2
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("XR29_REPO_ROOT", os.path.abspath(os.path.join(HERE, "..", "..")))   # the override is for out-of-tree tests only
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
REVIEWS = os.path.join(REPO, "real_research", "reviews")
DATA = os.path.join(REPO, "real_research", "data")
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR29_mw_outer_curve"
NPROC = 3
T0 = time.time()

# ================================================================================================= units and the chain's inputs
G = 6.67430e-11; MSUN = 1.98892e30; KPC = 3.0856775814913673e19; PC = KPC / 1e3
GK = G * MSUN / KPC / 1e6                                                    # G in (km/s)^2 kpc / Msun
_fp0 = json.load(open(os.path.join(CHAIN, "FP0_core_postulates_results.json")))["numbers"]
A0 = {"canonical": _fp0["a0_canonical"], "alt": _fp0["a0_rho_total"]}      # 9.3603e-11 / 1.1312e-10 (FP0)
FOOTS = ("canonical", "alt")
A0_LAW = {f: (0.0 if MUTATE else A0[f]) for f in FOOTS}                     # MUTATE: a0 -> 0 in the chain's law
XI_PC = 0.03                                                                 # the heat filter's length (FP1/FP7 floors 0.024-0.032 pc)
L_HS0_MPC = 2.879                                                            # FP13's committed H_S cell at z = 0 (XR27's reading)
H0_KMS = 67.4                                                                # FP0's H0 (NFW control's rho_crit and c(M))
RHO_CRIT = 3 * (H0_KMS * 1e3 / (KPC * 1e3)) ** 2 / (8 * math.pi * G) * KPC ** 3 / MSUN   # Msun / kpc^3

# ================================================================================================= FP7's solver (read-only slice)
_FP7P = os.path.join(CHAIN, "FP7_aqual_type_repair.py")
_fp7src = open(_FP7P).read()
NS7 = {"np": np, "sps": sps, "spl": spl, "math": math, "quad": quad}
exec(compile(_fp7src[_fp7src.index("wP2 = lambda s:"):_fp7src.index("HZ = 0.1")], "FP7_aqual_type_repair.py[A3 slice]", "exec"), NS7)
faces, Cyl, axisym_run = NS7["faces"], NS7["Cyl"], NS7["axisym_run"]
GRIDS = {"scan": ((0.02, 1.06, 1000.0), (0.005, 1.07, 1000.0)),            # kpc: (first cell, growth, extent) in R and in z
         "fine": ((0.02, 1.03, 1000.0), (0.005, 1.035, 1000.0))}

# ================================================================================================= baryon models (Msun, kpc)
# ("expexp", Sigma0 [Msun/kpc^2], Rd, zd)          rho = Sigma0/(2 zd) exp(-R/Rd - |z|/zd)
# ("gas", Sigma0, Rm, Rd, zd)                      rho = Sigma0/(4 zd) exp(-Rm/R - R/Rd) sech^2(z/(2 zd))       (McMillan 2017 Eq. 4)
# ("mcmbulge", rho0 [Msun/kpc^3], alpha, r0, rcut, q)  rho = rho0 (1 + m/r0)^-alpha exp(-(m/rcut)^2), m^2 = R^2 + (z/q)^2
# ("hernquist", M, a)                              rho = M a / (2 pi r (r + a)^3)
# ("cgm", M(<R200), R200, beta)                    rho ~ r^beta inside R200 (Cautun 2020 Eq. 5-6), truncated at R200
_SIG_HI_MCM = 10e6 / math.exp(-4.0 / 8.33 - 8.33 / 7.0)                     # McMillan's back-out from Sigma(8.33 kpc) = 10, 2
_SIG_H2_MCM = 2e6 / math.exp(-12.0 / 8.33 - 8.33 / 1.5)
_MCM_GAS = [("gas", _SIG_HI_MCM, 4.0, 7.0, 0.085), ("gas", _SIG_H2_MCM, 12.0, 1.5, 0.045)]
_CAU_GAS = [("gas", 53e6, 4.0, 7.0, 0.085), ("gas", 2200e6, 12.0, 1.5, 0.045)]   # Cautun 2020 Table 1 (as printed)
_EE = lambda M, Rd, zd: ("expexp", M / (2 * math.pi * Rd ** 2), Rd, zd)          # B2's double exponential by total mass
MODELS = {
    "McM17": dict(star=[("expexp", 896e6, 2.50, 0.300), ("expexp", 183e6, 3.02, 0.900), ("mcmbulge", 98.4e9, 1.8, 0.075, 2.1, 0.5)],
                  gas=_MCM_GAS, cgm=[], label="McMillan 2017 (the record's mass model)"),
    "McM17r": dict(star=[("expexp", 896e6 * 1.30, 2.50 * 0.90, 0.300), ("expexp", 183e6 * 1.30, 3.02 * 0.90, 0.900),
                         ("mcmbulge", 98.4e9, 1.8, 0.075, 2.1, 0.5)],
                   gas=_MCM_GAS, cgm=[], label="the record's prior-respecting refit cell (f_M 1.30, f_R 0.90)"),
    "Cau20": dict(star=[("expexp", 731e6, 2.63, 0.300), ("expexp", 101e6, 3.80, 0.900), ("mcmbulge", 103e9, 1.8, 0.075, 2.1, 0.5)],
                  gas=_CAU_GAS, cgm=[], label="Cautun et al. 2020 (contracted-halo fit), no CGM"),
    "Cau20+CGM": dict(star=[("expexp", 731e6, 2.63, 0.300), ("expexp", 101e6, 3.80, 0.900), ("mcmbulge", 103e9, 1.8, 0.075, 2.1, 0.5)],
                      gas=_CAU_GAS, cgm=[("cgm", 6.4e10, 218.0, -1.46)], label="Cautun et al. 2020 with its CGM (6.4e10 inside 218 kpc)"),
    "Cau20N": dict(star=[("expexp", 1070e6, 2.43, 0.300), ("expexp", 113e6, 3.88, 0.900), ("mcmbulge", 101e9, 1.8, 0.075, 2.1, 0.5)],
                   gas=_CAU_GAS, cgm=[], label="Cautun et al. 2020, NFW-halo column"),
    "B2": dict(star=[_EE(3.65e10, 2.35, 0.14), ("hernquist", 1.55e10, 0.70)],
               gas=[_EE(8.2e9, 18.24, 0.52), _EE(1.3e9, 2.57, 0.08), _EE(7.0e7, 5.00, 0.10), _EE(2.2e5, 3.30, 0.09)], cgm=[],
               label="de Salas+2019 B2 (Ou+2024 Table 2; Jiao+2023; Coquery & Blanchard 2025)"),
}
FSTAR = (0.5, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.1, 2.4)                      # the stellar-mass factors scanned


def _sech2(x):
    e = np.exp(-2.0 * np.abs(x)); return 4.0 * e / (1.0 + e) ** 2


def comp_rho(c, R, z):
    """density [Msun/kpc^3] of one component at (R, z) [kpc]."""
    k = c[0]
    if k == "expexp":
        _, S0, Rd, zd = c; return S0 / (2 * zd) * np.exp(-R / Rd - np.abs(z) / zd)
    if k == "gas":
        _, S0, Rm, Rd, zd = c; Rs = np.maximum(R, 1e-6)
        return S0 / (4 * zd) * np.exp(-Rm / Rs - Rs / Rd) * _sech2(z / (2 * zd))
    if k == "mcmbulge":
        _, r0h, al, r0, rc, q = c; m = np.maximum(np.sqrt(R * R + (z / q) ** 2), 1e-7)
        return r0h / (1 + m / r0) ** al * np.exp(-(m / rc) ** 2)
    if k == "hernquist":
        _, M, a = c; r = np.maximum(np.sqrt(R * R + z * z), 1e-7); return M * a / (2 * math.pi * r * (r + a) ** 3)
    if k == "cgm":
        _, M2, R2, be = c; r = np.maximum(np.sqrt(R * R + z * z), 1e-4)
        return np.where(r <= R2, (3 + be) * M2 / (4 * math.pi * R2 ** (3 + be)) * r ** be, 0.0)
    raise ValueError(k)


def comp_mass(c):
    k = c[0]
    if k == "expexp":
        return 2 * math.pi * c[1] * c[2] ** 2
    if k == "gas":
        _, S0, Rm, Rd, zd = c
        return 2 * math.pi * S0 * quad(lambda R: math.exp(-Rm / R - R / Rd) * R if R > 0 else 0.0, 0, 60 * Rd + 10 * Rm, limit=400)[0]
    if k == "mcmbulge":
        _, r0h, al, r0, rc, q = c
        return 4 * math.pi * q * quad(lambda m: r0h / (1 + m / r0) ** al * math.exp(-(m / rc) ** 2) * m * m, 0, 20 * rc, limit=400)[0]
    if k == "hernquist":
        return c[1]
    if k == "cgm":
        return c[1]
    raise ValueError(k)


def model_parts(key, fstar=1.0, cgm_scale=1.0):
    m = MODELS[key]
    comps = [("star", c, fstar) for c in m["star"]] + [("gas", c, 1.0) for c in m["gas"]] + [("cgm", c, cgm_scale) for c in m["cgm"]]
    return comps


def model_rho(key, fstar=1.0, cgm_scale=1.0):
    parts = model_parts(key, fstar, cgm_scale)
    return lambda R, z: sum(w * comp_rho(c, R, z) for _, c, w in parts)


def model_masses(key, fstar=1.0, cgm_scale=1.0):
    ms = {"star": 0.0, "gas": 0.0, "cgm": 0.0}
    for grp, c, w in model_parts(key, fstar, cgm_scale):
        ms[grp] += w * comp_mass(c)
    return ms


# ================================================================================================= one axisymmetric solve
def newton_only(rho_hat, M_hat, Rf, zf):
    """Newton on FP7's grid with FP7's own Cyl methods (the a0 -> 0 limit of the chain's law; no scalar)."""
    c = Cyl(Rf, zf); R, Z = np.meshgrid(c.Rc, c.zc, indexing="ij")
    src = 4 * math.pi * rho_hat(R, Z).ravel() * c.vol
    bRN, bzN = -M_hat / c.rbR, -M_hat / c.rbz
    PhiN = c.poisson(src, bRN, bzN); gNR, _ = c.grad(PhiN, bRN, bzN)
    k0_ = np.arange(c.nR - 1) * c.nz; gN = -gNR[k0_]
    return dict(R=c.Rf[1:c.nR], gN=gN, gQ=gN, gA=gN, galg=gN, it=0, change=0.0, curl=0.0, cells=(c.nR, c.nz))


def solve_task(task):
    """(model, footing, f_*, cgm_scale, grid) -> the midplane curves [km/s] of the chain's law (AQUAL), its QUMOND and algebraic
    forms, and Newton, on the grid's R faces.  Units inside: kpc, a0 = 1, G = 1 (FP7's), M_u = a0 kpc^2 / G."""
    key, foot, fs, cs, grid = task
    t = time.time()
    a0u = A0[foot]; Mu = a0u * KPC ** 2 / G / MSUN                          # Msun per dimensionless mass unit
    rho = model_rho(key, fs, cs); ms = model_masses(key, fs, cs); Mt = sum(ms.values())
    rho_hat = lambda R, Z: rho(R, Z) / Mu
    Rf, zf = faces(*GRIDS[grid][0]), faces(*GRIDS[grid][1])
    o = axisym_run(rho_hat, Mt / Mu, Rf, zf) if A0_LAW[foot] > 0 else newton_only(rho_hat, Mt / Mu, Rf, zf)
    v = lambda g: np.sqrt(np.abs(g) * a0u * o["R"] * KPC) / 1e3
    return task, dict(R=o["R"], vN=v(o["gN"]), vA=v(o["gA"]), vQ=v(o["gQ"]), valg=v(o["galg"]), it=int(o["it"]),
                      change=float(o["change"]), curl=float(o["curl"]), cells=o["cells"], masses=ms, secs=time.time() - t)


def run_fields(rho_hat, M_hat, Rf, zf, itmax=260):
    """axisym_run's steps (FP7) returning the 2-D scalar-force field too: used only by the heat-filter test F1."""
    c = Cyl(Rf, zf); R, Z = np.meshgrid(c.Rc, c.zc, indexing="ij")
    src = 4 * math.pi * rho_hat(R, Z).ravel() * c.vol
    bRN, bzN = -M_hat / c.rbR, -M_hat / c.rbz
    PhiN = c.poisson(src, bRN, bzN); gNR, gNz = c.grad(PhiN, bRN, bzN)
    s = c.dual(gNR, gNz, itmax=itmax)
    gphiR = (s["wR"] * s["FR"]).reshape(c.nR, c.nz)                         # the scalar's radial force on the R faces x z centres
    return c, -gNR.reshape(c.nR, c.nz), -gphiR, s


# ================================================================================================= semi-analytic Newton (K3)
_U = np.linspace(0.0, 40.0, 40001); _SU = 1.0 / np.cosh(_U) ** 2
_SK_CACHE = {}


def _Zexp(k, zd):
    return 1.0 / (1.0 + k * zd)


def _Zsech2(k, zd):
    out = np.empty_like(k)
    for i in range(0, len(k), 2000):
        out[i:i + 2000] = np.trapz(_SU[None, :] * np.exp(-np.outer(2 * k[i:i + 2000] * zd, _U)), _U, axis=1)
    return out


def _S_gas(S0, Rm, Rd, k):
    key = (S0, Rm, Rd, len(k), float(k[-1]))
    if key not in _SK_CACHE:
        Rg = np.linspace(0.0, 150.0, 30001)[1:]; w = S0 * np.exp(-Rm / Rg - Rg / Rd) * Rg * (Rg[1] - Rg[0])
        out = np.empty_like(k)
        for i in range(0, len(k), 400):
            out[i:i + 400] = j0(np.outer(k[i:i + 400], Rg)) @ w
        _SK_CACHE[key] = out
    return _SK_CACHE[key]


def gR_semi(c, Rs):
    """midplane inward radial force [(km/s)^2/kpc] of one component, independent of the grid."""
    k_ = c[0]; Rs = np.atleast_1d(np.asarray(Rs, float))
    if k_ == "expexp":
        _, S0, Rd, zd = c; k = np.linspace(1e-6, 60.0, 24000); S = S0 * Rd ** 2 / (1 + (k * Rd) ** 2) ** 1.5; Z = _Zexp(k, zd)
        return np.array([2 * math.pi * GK * np.trapz(k * j1(k * R) * S * Z, k) for R in Rs])
    if k_ == "gas":
        _, S0, Rm, Rd, zd = c; k = np.linspace(1e-6, 40.0, 12000); S = _S_gas(S0, Rm, Rd, k); Z = _Zsech2(k, zd)
        return np.array([2 * math.pi * GK * np.trapz(k * j1(k * R) * S * Z, k) for R in Rs])
    if k_ == "mcmbulge":
        _, r0h, al, r0, rc, q = c; e2 = 1 - q * q
        f = lambda m: r0h / (1 + m / r0) ** al * math.exp(-(m / rc) ** 2)
        return np.array([4 * math.pi * GK * q / R * quad(lambda m: f(m) * m * m / math.sqrt(R * R - m * m * e2), 0, R, limit=400)[0]
                         for R in Rs])
    if k_ == "hernquist":
        _, M, a = c; return GK * M / (Rs + a) ** 2
    if k_ == "cgm":
        _, M2, R2, be = c; return GK * M2 * np.minimum(Rs / R2, 1.0) ** (3 + be) / Rs ** 2
    raise ValueError(k_)


def vN_semi(key, Rs, fstar=1.0, cgm_scale=1.0):
    return np.sqrt(sum(w * gR_semi(c, Rs) for _, c, w in model_parts(key, fstar, cgm_scale)) * np.asarray(Rs))


# ================================================================================================= the data
def _tsv(name):
    rows = [l.split("\t") for l in open(os.path.join(DATA, name)) if l.strip() and not l.startswith("#")]
    return rows[0], np.array([[float(x) for x in r] for r in rows[1:]])


# Zhou, Li, Huang & Zhang 2023, ApJ 946, 73 (arXiv:2212.10393), Table 4: R [kpc], V_c [km/s], sigma_Vc [km/s] (statistical), N stars
Z23_TABLE = """5.24 225.10 0.69 845; 5.74 233.53 0.68 692; 6.25 234.3 0.62 704; 6.77 233.17 0.60 759; 7.23 236.19 0.45 1061;
7.83 236.00 0.29 2288; 8.21 233.19 0.26 2550; 8.78 233.15 0.22 3281; 9.26 232.15 0.17 4583; 9.75 231.24 0.16 5061;
10.25 230.34 0.17 4881; 10.75 230.54 0.18 4564; 11.25 229.11 0.19 4005; 11.75 227.48 0.20 3431; 12.24 226.69 0.25 2844;
12.74 225.56 0.27 2312; 13.25 224.90 0.27 2116; 13.74 223.57 0.31 1825; 14.23 221.10 0.40 1362; 14.74 220.19 0.43 987;
15.23 219.59 0.50 801; 15.74 217.36 0.68 563; 16.24 216.61 0.74 446; 16.74 217.28 0.87 308; 17.23 216.25 1.02 257;
17.74 213.81 1.15 163; 18.35 217.53 1.45 207; 18.90 212.10 1.58 97; 19.50 210.46 1.32 162; 20.41 206.69 1.71 85;
21.28 207.71 1.69 93; 22.39 203.72 2.01 46; 23.16 205.20 2.50 20; 24.00 200.64 4.94 10"""
# Jiao, Hammer, Wang et al. 2023, A&A 678, A208 (arXiv:2309.00048v4), Table 3: R [kpc], V_c [km/s], sigma_Vc [km/s] (stat + sys)
J23_TABLE = """9.5 221.75 3.17; 10.5 223.32 3.02; 11.5 220.72 3.47; 12.5 222.92 3.19; 13.5 224.16 3.48; 14.5 221.60 4.20;
15.5 218.79 4.75; 16.5 216.38 4.96; 17.5 213.48 6.13; 18.5 209.17 4.42; 19.5 206.25 4.63; 20.5 202.54 4.40; 21.5 197.56 4.62;
22.5 197.00 3.81; 23.5 191.62 12.95; 24.5 187.12 8.06; 25.5 181.44 19.58; 26.5 175.68 24.68"""


def _parse(tab):
    return np.array([[float(x) for x in r.split()] for r in tab.replace("\n", " ").split(";") if r.strip()])


def load_data():
    D = {}
    _, e = _tsv("mw_rc_eilers2019_table1.tsv")                             # R, v, sig_minus, sig_plus
    D["E19"] = dict(R=e[:, 0], v=e[:, 1], s=0.5 * (e[:, 2] + e[:, 3]),
                    sysf=np.interp(e[:, 0], [5.0, 6.0, 14.0, 16.0, 19.0, 22.0, 30.0], [0.030, 0.020, 0.022, 0.040, 0.060, 0.120, 0.120]),
                    sys_in_s=False, R0=8.122, cite="Eilers+2019 (ApJ 871, 120) Table 1",
                    corr=dict(norm=0.025, slope=0.46), slope_pub=(-1.7, 0.1, 0.46))
    _, o = _tsv("mw_rc_ou2024_table1.tsv")                                 # R, v, sig_plus, sig_minus, N
    D["O24"] = dict(R=o[:, 0], v=o[:, 1], s=0.5 * (o[:, 2] + o[:, 3]),
                    sysf=np.interp(o[:, 0], [6.27, 7.0, 13.0, 16.0, 19.0, 21.0, 22.0, 22.7, 30.0],
                                   [0.030, 0.022, 0.023, 0.030, 0.036, 0.026, 0.040, 0.150, 0.150]),
                    sys_in_s=False, R0=8.178, cite="Ou+2024 (MNRAS 528, 693) Table 1", corr=None,
                    slope_pub=(-2.22, 0.20, 0.0), gamma_pub=(-0.56, 0.225))
    z = _parse(Z23_TABLE)
    D["Z23"] = dict(R=z[:, 0], v=z[:, 1], s=z[:, 2],
                    sysf=np.interp(z[:, 0], [5.0, 15.0, 18.0, 20.0, 24.0], [0.010, 0.010, 0.015, 0.020, 0.030]),
                    sys_in_s=False, R0=8.21, cite="Zhou+2023 (ApJ 946, 73) Table 4", corr=dict(norm=1.36 / 234.04, slope=0.07),
                    slope_pub=(-1.83, 0.02, 0.07))
    j = _parse(J23_TABLE)
    D["J23"] = dict(R=j[:, 0], v=j[:, 1], s=j[:, 2], sysf=np.zeros(len(j)), sys_in_s=True, R0=8.34,
                    cite="Jiao+2023 (A&A 678, A208) Table 3", corr=None, slope_pub=(-2.18, 0.23, 0.0), gamma_pub=(-0.47, 0.15))
    for k, d in D.items():
        d["stot"] = np.sqrt(d["s"] ** 2 + (d["sysf"] * d["v"]) ** 2)
    return D


def load_bird():
    txt = {}
    for l in open(os.path.join(DATA, "mw_halo_bird2022_jeans.txt")):
        if l.strip() and not l.startswith("#"):
            p = l.split(); txt[p[0]] = float(p[1])
    return [dict(tag="BHB", r=txt["JEANS_BHB_r_kpc"], M=txt["JEANS_BHB_M_e11"] * 1e11, er=txt["JEANS_BHB_Mrand_e11"] * 1e11,
                 es=txt["JEANS_BHB_Msys_e11"] * 1e11),
            dict(tag="KG", r=txt["JEANS_KG_r_kpc"], M=txt["JEANS_KG_M_e11"] * 1e11, er=txt["JEANS_KG_Mrand_e11"] * 1e11,
                 es=txt["JEANS_KG_Msys_e11"] * 1e11)]


CENSUS = {"McMillan17": (5.43e10, 0.57e10, 0.57e10), "Cautun20": (5.04e10, 0.43e10, 0.52e10),
          "LicquiaNewman15": (6.08e10, 1.14e10, 1.14e10), "BHGerhard16": (5.0e10, 1.0e10, 1.0e10)}
MSTAR_FLOOR = 3.0e10                                                         # Bland-Hawthorn & Gerhard 5e10 - 2 sigma


# ================================================================================================= statistics
def chi2_diag(vm, d, which="tot"):
    s = d["stot"] if which == "tot" else d["s"]
    return float(np.sum(((vm - d["v"]) / s) ** 2))


def chi2_corr(vm, d):
    """stat + a common fractional normalisation (+ a slope where published) + the diagonal excess of the per-point budget."""
    if d["corr"] is None:
        return float("nan")
    r = vm - d["v"]; n = d["corr"]["norm"]; b = d["corr"]["slope"]
    C = np.diag(d["s"] ** 2) + np.outer(n * d["v"], n * d["v"]) + np.outer(b * (d["R"] - d["R0"]), b * (d["R"] - d["R0"]))
    C += np.diag(np.maximum((d["sysf"] * d["v"]) ** 2 - (n * d["v"]) ** 2, 0.0))
    return float(r @ np.linalg.solve(C, r))


def pval(c2, n):
    return float(CHI2.sf(c2, n)) if n > 0 else float("nan")


def wslope(R, v, s):
    """weighted least-squares straight line; returns (slope, error)."""
    w = 1 / s ** 2; A = np.vstack([np.ones_like(R), R]).T
    Cm = np.linalg.inv(A.T @ (A * w[:, None])); p = Cm @ (A.T @ (w * v))
    return float(p[1]), float(math.sqrt(Cm[1, 1]))


def wgamma(R, v, s):
    """power-law index of v = A R^gamma by weighted least squares in log space (sigma_ln v = s/v)."""
    return wslope(np.log(R), np.log(v), s / v)


# ================================================================================================= reporting
class _Tee:
    def __init__(self, fh): self.fh = fh; self.so = sys.__stdout__
    def write(self, s): self.so.write(s); self.fh.write(s)
    def flush(self): self.so.flush(); self.fh.flush()


CH = []
OUT = {"lane": "XR29 (Milky Way outer rotation curve in the chain's law)", "mutate": MUTATE, "checks": {}, "numbers": {}}


def P(*a):
    print(*a, flush=True)


def check(name, measured, ok, load_bearing=True, reading=""):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 118); P(t); P("=" * 118)


def el():
    return f"[{time.time() - T0:.0f} s]"


def exec_ro(path, name, cut=None):
    """exec a committed script (whole, or up to the marker `cut`) in a private namespace, stdout captured, MUTATE forced to 0;
    a sys.exit() at its end is caught.  Returns (namespace, captured stdout, exit code)."""
    src = open(path).read()
    if cut is not None:
        src = src[:src.index(cut)]
    ns = {"__file__": path, "__name__": name}; buf = io.StringIO(); rc = None
    old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    try:
        with contextlib.redirect_stdout(buf):
            try:
                exec(compile(src, os.path.basename(path), "exec"), ns)
            except SystemExit as e:
                rc = e.code
    finally:
        if old is None: os.environ.pop("MUTATE", None)
        else: os.environ["MUTATE"] = old
    return ns, buf.getvalue(), rc


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return [jsonable(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    return o


# ================================================================================================= main
def main():
    from multiprocessing import Pool
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: a0 -> 0 in the chain's law (the scalar's force vanishes; Newton on baryons): T1 must FAIL (rc = 1) ***")
    P(f"\n  inputs: a0 = {A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2 (FP0); law a0 = {A0_LAW['canonical']:.4e} / {A0_LAW['alt']:.4e}; "
      f"xi = {XI_PC} pc; H_S L(0) = {L_HS0_MPC} Mpc; rho_crit (H0 = {H0_KMS}) = {RHO_CRIT:.1f} Msun/kpc^3")
    D = load_data(); BIRD = load_bird()
    for k, d in D.items():
        P(f"    {k}: {d['cite']}: {len(d['R'])} points, {d['R'][0]:.2f}-{d['R'][-1]:.2f} kpc; median stat {np.median(d['s']):.2f} km/s, "
          f"sys {('in sigma' if d['sys_in_s'] else f'{d[chr(115)+chr(121)+chr(115)+chr(102)].min():.1%}-{d[chr(115)+chr(121)+chr(115)+chr(102)].max():.1%}')}")
    pool = Pool(NPROC)

    # ------------------------------------------------------------------------------------------ K1 the record's own code
    banner("K1  CONTROL: the record's Milky Way AQUAL numbers, reproduced with its own code")
    NSR, outR, rcR = exec_ro(os.path.join(REVIEWS, "mi_aqual_mcmillan2017_2026.py"), "rec_mcm17")
    res = NSR["res"]
    got1 = dict(vc_can=res["canon 9.36e-11"]["vc"] / 1e3, sd_can=res["canon 9.36e-11"]["sd"], vc_alt=res["alt 1.13e-10"]["vc"] / 1e3,
                sd_alt=res["alt 1.13e-10"]["sd"], vc_12=res["a0=1.2e-10 CTRL"]["vc"] / 1e3, sd_12=res["a0=1.2e-10 CTRL"]["sd"],
                vN=NSR["vcN"] / 1e3, vc_simple=NSR["vc_s"] / 1e3, sd_simple=NSR["sd_s"])
    want1 = dict(vc_can=191.9, sd_can=71.4, vc_alt=196.1, sd_alt=74.8, vc_12=197.6, sd_12=76.0, vN=177.0, vc_simple=222.7, sd_simple=96.5)
    ok1 = all(abs(round(got1[k], 1) - want1[k]) < 1e-9 for k in want1) and rcR in (0, None)
    P("    mi_aqual_mcmillan2017_2026.py (run whole, captured; exit code %s):" % rcR)
    for k in want1:
        P(f"      {k:<10} {got1[k]:9.3f}   committed {want1[k]:7.1f}")
    NSF, _, _ = exec_ro(os.path.join(REVIEWS, "mi_aqual_mond_refit_2026.py"), "rec_refit", cut='banner("F1')
    srcF = open(os.path.join(REVIEWS, "mi_aqual_mond_refit_2026.py")).read()
    exec(compile(srcF[srcF.index("def slope_of"):srcF.index("MODELS = {")], "mi_aqual_mond_refit_2026.py[slope_of]", "exec"), NSF)
    oq = NSF["observables"](1.30, 0.90, NSF["A0"]["canon"], NSF["mu_a2"])
    _, slq = NSF["slope_of"](1.30, 0.90, NSF["A0"]["canon"], NSF["mu_a2"])
    got2 = dict(vc=oq["vc"] / 1e3, sd=oq["sd"], slope=slq, mstar=oq["mstar"], sigstar=oq["sigstar"])
    want2 = dict(vc=198.6, sd=75.2, slope=-1.14)
    ok2 = abs(round(got2["vc"], 1) - 198.6) < 1e-9 and abs(round(got2["sd"], 1) - 75.2) < 1e-9 and abs(round(got2["slope"], 2) + 1.14) < 1e-9
    P(f"    mi_aqual_mond_refit_2026.py, cell (1.30, 0.90) canonical: v_c {got2['vc']:.3f} (committed 198.6), Sigma_dyn {got2['sd']:.3f} "
      f"(75.2), slope {got2['slope']:+.4f} (-1.14), M_* {got2['mstar']:.3e}, Sigma_* {got2['sigstar']:.2f}")
    OUT["numbers"]["K1"] = dict(mcmillan2017=got1, refit_cell=got2)
    check("K1 CONTROL: the record's committed Milky Way AQUAL numbers are reproduced EXACTLY (to their printed precision) by its own "
          "code: McMillan 2017 v_c(R0) 191.9 / 196.1 / 197.6, Sigma_dyn 71.4 / 74.8 / 76.0, Newton 177.0, simple 222.7 / 96.5; the "
          "refit cell (1.30, 0.90): 198.6 km/s, 75.2 Msun/pc^2, slope -1.14",
          "; ".join(f"{k} {got1[k]:.1f}" for k in want1) + f"; refit {got2['vc']:.1f} / {got2['sd']:.1f} / {got2['slope']:+.2f}",
          ok1 and ok2, reading="the alpha = 2 kernel of that front is the record's, not the chain's; the chain's P2 is solved below")

    # the record's baryons, as this lane encodes them, must BE the record's functions
    Rt = np.array([0.3, 1.0, 3.0, 5.0, 8.21, 12.0, 20.0, 30.0]); zt = np.array([0.0, 0.05, 0.3, 1.1, 3.0])
    RR_, ZZ_ = np.meshgrid(Rt, zt, indexing="ij")
    rec_rho = NSR["rho_baryon"](RR_ * KPC, ZZ_ * KPC) / (MSUN / KPC ** 3)
    my_rho = model_rho("McM17")(RR_, ZZ_)
    comp = NSF["densities"](1.30, 0.90)[0]
    rec_rho_r = sum(f(RR_ * KPC, ZZ_ * KPC) for f in comp.values()) / (MSUN / KPC ** 3)
    my_rho_r = model_rho("McM17r")(RR_, ZZ_)
    dev_rho = max(float(np.max(np.abs(my_rho / rec_rho - 1))), float(np.max(np.abs(my_rho_r / rec_rho_r - 1))))
    P(f"    this lane's McM17 / McM17r densities vs the record's own functions (40 points each): max |relative difference| {dev_rho:.1e}")

    # ------------------------------------------------------------------------------------------ K2 FP7's solver
    banner("K2  CONTROL: FP7's dual Kacanov solver (exec'd slice) reproduces FP7's committed Plummer control")
    Mpl = 3.0
    pl = axisym_run(lambda R, Z: 3 * Mpl / (4 * math.pi) * (1 + R ** 2 + Z ** 2) ** -2.5, Mpl, faces(0.02, 1.04, 300.0), faces(0.02, 1.04, 300.0))
    selp = (pl["R"] > 0.1) & (pl["R"] < 30)
    pl_AQ = float(np.max(np.abs(np.log10(pl["gA"][selp] / pl["gQ"][selp])))); pl_Aa = float(np.max(np.abs(np.log10(pl["gA"][selp] / pl["galg"][selp]))))
    ref = json.load(open(os.path.join(CHAIN, "FP7_aqual_type_repair_results.json")))["numbers"]["A3"]["plummer"]
    dK2 = max(abs(pl_AQ / ref["AQ"] - 1), abs(pl_Aa / ref["Aalg"] - 1))
    check("K2 CONTROL: FP7's solver slice reproduces FP7's committed Plummer control (the spherical law is P2 exactly) to 1e-6",
          f"AQUAL/QUMOND {pl_AQ:.6e} (committed {ref['AQ']:.6e}), AQUAL/algebraic {pl_Aa:.6e} (committed {ref['Aalg']:.6e}); max rel. diff {dK2:.1e}",
          dK2 < 1e-6)

    # ------------------------------------------------------------------------------------------ the scan (parallel)
    banner(f"S  THE SCAN: the chain's law on every baryon model, both footings, f_* in {FSTAR}   {el()}")
    tasks = [(k, f, fs, 1.0, "scan") for k in MODELS for f in FOOTS for fs in FSTAR]
    tasks_fine = [("McM17", "canonical", 1.0, 1.0, "fine"), ("McM17", "canonical", 1.6, 1.0, "fine"), ("B2", "alt", 1.4, 1.0, "fine"),
                  ("Cau20+CGM", "canonical", 1.4, 1.0, "fine")]
    SC = {}
    for tk, r in pool.imap_unordered(solve_task, tasks + tasks_fine, chunksize=1):
        SC[tk] = r
    worst_it = max(r["it"] for r in SC.values()); worst_curl = max(r["curl"] for r in SC.values())
    P(f"    {len(SC)} solves done {el()}; cells {SC[tasks[0]]['cells']} (scan) / {SC[tasks_fine[0]]['cells']} (fine); Kacanov iterations <= {worst_it}, "
      f"curl residual <= {worst_curl:.1e}; mean {np.mean([r['secs'] for r in SC.values()]):.1f} s per solve")
    Rg = SC[tasks[0]]["R"]
    MS = {k: model_masses(k) for k in MODELS}
    for k in MODELS:
        P(f"    {k:<10} {MODELS[k]['label']}: M_* {MS[k]['star']:.3e}, gas {MS[k]['gas']:.3e}, CGM {MS[k]['cgm']:.3e} Msun")
    P(f"\n    census curves (f_* = 1), the chain's law (AQUAL) [Newton] in km/s:")
    Rshow = (5.0, 8.2, 10.0, 15.0, 20.0, 25.0, 30.0, 50.0, 100.0)
    P("    " + f"{'model':<11}{'footing':<10}" + "".join(f"{r_:>13.1f}" for r_ in Rshow))
    for k in MODELS:
        for f in FOOTS:
            r = SC[(k, f, 1.0, 1.0, "scan")]
            P("    " + f"{k:<11}{f:<10}" + "".join(f"{np.interp(r_, Rg, r['vA']):7.1f} [{np.interp(r_, Rg, r['vN']):4.0f}]" for r_ in Rshow))

    # ------------------------------------------------------------------------------------------ K3 Newton
    banner(f"K3  CONTROL: pure Newton -- the grid reproduces the semi-analytic baryonic curve   {el()}")
    Rk3 = np.array([5.0, 8.21, 10.0, 15.0, 20.0, 25.0, 30.0, 50.0, 100.0])
    worst3 = 0.0; K3 = {}
    for k in MODELS:
        vs = vN_semi(k, Rk3); vg = np.interp(Rk3, Rg, SC[(k, "canonical", 1.0, 1.0, "scan")]["vN"])
        dv = float(np.max(np.abs(vg / vs - 1))); worst3 = max(worst3, dv); K3[k] = dict(semi=vs, grid=vg, maxdev=dv)
        P(f"    {k:<10} semi-analytic " + " ".join(f"{x:6.1f}" for x in vs) + f"   max |grid/semi - 1| = {dv:.1e}")
    vN_R0 = float(np.interp(8.21, Rg, SC[("McM17", "canonical", 1.0, 1.0, "scan")]["vN"]))
    OUT["numbers"]["K3"] = dict(R=Rk3, models=K3, vN_R0_McM17=vN_R0)
    check("K3 CONTROL: pure Newton -- the grid's midplane curve equals the independent semi-analytic baryonic curve (Hankel discs, "
          "homoeoid bulge, closed-form Hernquist/CGM) to <= 0.3% at 5-100 kpc for every model; McM17's v_N(8.21) equals the record's "
          "177.0 km/s to 0.3 km/s; this lane's McMillan densities equal the record's functions to 1e-10",
          f"worst |grid/semi - 1| {worst3:.1e}; v_N(8.21) {vN_R0:.2f} km/s; density match {dev_rho:.1e}",
          worst3 < 3e-3 and abs(vN_R0 - 177.0) < 0.3 and dev_rho < 1e-10)

    # ------------------------------------------------------------------------------------------ K4 numerics
    banner("K4  CONTROL: grid convergence and the interpolation in f_*")
    worst4 = 0.0
    for tf in tasks_fine:
        rf = SC[tf]; rs_ = SC[(tf[0], tf[1], tf[2], tf[3], "scan")]
        sel = (Rg >= 5) & (Rg <= 100)
        dv = float(np.max(np.abs(np.interp(Rg[sel], rf["R"], rf["vA"]) / rs_["vA"][sel] - 1))); worst4 = max(worst4, dv)
        P(f"    {tf[0]} {tf[1]} f_* {tf[2]}: fine vs scan grid max |dv/v| over 5-100 kpc = {dv:.1e}")
    OUT["numbers"]["K4_grid"] = worst4

    SPL = {}
    for k in MODELS:
        for f in FOOTS:
            V2 = np.array([SC[(k, f, fs, 1.0, "scan")]["vA"] ** 2 for fs in FSTAR]); VN2 = np.array([SC[(k, f, fs, 1.0, "scan")]["vN"] ** 2 for fs in FSTAR])
            SPL[(k, f)] = (CubicSpline(FSTAR, V2, axis=0), VN2)

    def v_model(k, f, fs, R, newton=False):
        """the model curve at radii R for stellar factor fs: AQUAL spline (inside the scan) or, for Newton (and for the MUTATE law),
        the exact linearity v_N^2 = v_gas^2 + f_* v_*^2 (any f_* >= 0)."""
        if newton or A0_LAW[f] == 0:
            VN2 = SPL[(k, f)][1]; vst2 = (VN2[-1] - VN2[0]) / (FSTAR[-1] - FSTAR[0]); vg2 = VN2[0] - FSTAR[0] * vst2
            return np.sqrt(np.maximum(np.interp(R, Rg, vg2 + fs * vst2), 0.0))
        return np.sqrt(np.maximum(np.interp(R, Rg, SPL[(k, f)][0](min(max(fs, FSTAR[0]), FSTAR[-1]))), 0.0))

    # ------------------------------------------------------------------------------------------ E  M31 (and the LMC, reported)
    banner(f"E  M31's PARTIALLY SURVIVING FIELD (FP11's two-body machinery, MW-centred), and the LMC (reported)   {el()}")
    F11, _, _ = exec_ro(os.path.join(CHAIN, "FP11_local_group_flyby.py"), "fp11_ro")
    L0 = F11["L_of_a"](1.0); yt0 = F11["yth_of_a"](1.0); MPCm = F11["MPC"]
    P(f"    H_Y at z = 0 (FP11's L_of_a, yth_of_a): L = {L0 / MPCm:.4f} Mpc, y_th = {yt0:.3e}")
    lb = {"M31": (121.1744, -21.5729, 780.0), "LMC": (280.4652, -32.8884, 49.59)}
    R0SUN = 8.178

    def gc_unit(l, b, d):
        v = np.array([d * math.cos(math.radians(b)) * math.cos(math.radians(l)) - R0SUN, d * math.cos(math.radians(b)) * math.sin(math.radians(l)),
                      d * math.sin(math.radians(b))])
        return v / np.linalg.norm(v), float(np.linalg.norm(v))

    phis = np.radians(np.linspace(-30, 30, 13)); ehat = np.stack([-np.cos(phis), np.sin(phis), np.zeros_like(phis)], axis=1)
    phia = np.radians(np.arange(0, 360, 10)); ehat_all = np.stack([-np.cos(phia), np.sin(phia), np.zeros_like(phia)], axis=1)
    Mmw = sum(MS["McM17"].values())
    EFE = {}

    def pert_table(body, m2, foot):
        """(1/g_MW) x the internal radial perturbation (inward +) at the MW's midplane radii Rg: Sun-side wedge mean, disc-azimuth mean,
        sphere mean; tidal part of the body's own field (Newton + filtered isolated phantom) + the interaction field minus its centre value."""
        a0 = A0[foot]; u, d = gc_unit(*lb[body]); d_m = d * KPC; m1 = Mmw * MSUN; m2k = m2 * MSUN
        g = F11["Grid"](rmin=0.5, rmax=30000.0, nr=360, nth=256, lmax=80, lsm=40)
        W = F11["W_pair"](m1, m2k, 0.0, -d_m, a0, L0, yt0)
        DR, DT = g.field(g.divergence(W), L0)
        gz0 = float(np.mean(DR[0] * np.cos(g.tc) - DT[0] * np.sin(g.tc)))
        dgb = float(F11["dg_body"](m1, m2k, d_m, a0, L0, yt0))
        lr = np.log(g.rc)

        def interp_DR(r, th):
            ir = np.clip((np.log(r) - lr[0]) / (lr[1] - lr[0]), 0, g.nr - 1.000001); it = np.clip((th - g.tc[0]) / (g.tc[1] - g.tc[0]), 0, g.nth - 1.000001)
            i0_, t0_ = int(ir), int(it); fr, ft = ir - i0_, it - t0_
            return ((1 - fr) * (1 - ft) * DR[i0_, t0_] + fr * (1 - ft) * DR[i0_ + 1, t0_] + (1 - fr) * ft * DR[i0_, t0_ + 1] + fr * ft * DR[i0_ + 1, t0_ + 1])

        Mph2 = F11["phantom"](m2k, a0, L0, yt0, F11["YIELD"]); RG6 = F11["RG"]              # FP11's g_iso profile, computed once

        def body_acc(xv, zv):
            rb = math.hypot(xv, zv + d_m); gm = G * (m2k + float(np.interp(rb, RG6, Mph2))) / rb ** 2; return -gm * xv / rb, -gm * (zv + d_m) / rb
        ax0, az0 = body_acc(0.0, 0.0)

        def dr_out(r_kpc, cth):
            th = math.acos(max(-1.0, min(1.0, cth))); r = r_kpc * KPC; xv, zv = r * math.sin(th), r * math.cos(th)
            ax, az = body_acc(xv, zv)
            return ((ax - ax0) * math.sin(th) + (az - az0) * math.cos(th)) + (interp_DR(r, th) - gz0 * math.cos(th))
        gA_mw = SC[("McM17", foot, 1.0, 1.0, "scan")]["vA"] ** 2 / Rg * 1e6 / KPC       # m/s^2 (inward) on the R faces
        out = {"sun": np.zeros_like(Rg), "disc": np.zeros_like(Rg), "sphere": np.zeros_like(Rg)}
        mu_s = np.linspace(-1, 1, 41)
        for i, R_ in enumerate(Rg):
            if R_ < 1.0 or R_ > 300.0:
                continue
            out["sun"][i] = -np.mean([dr_out(R_, -float(e @ u)) for e in ehat]) / gA_mw[i]
            out["disc"][i] = -np.mean([dr_out(R_, -float(e @ u)) for e in ehat_all]) / gA_mw[i]
            out["sphere"][i] = -np.trapz([dr_out(R_, m_) for m_ in mu_s], mu_s) / 2 / gA_mw[i]
        return out, dict(gz0=gz0, dgb=dgb, d=d)

    if MUTATE:
        P("    (MUTATE: a0 = 0 -- no scalar, no phantom, no external-field effect; M31 enters only through Newton's tides, which are not "
          "part of the scored test)")
        for f in FOOTS:
            EFE[("M31", f)] = {"sun": np.zeros_like(Rg), "disc": np.zeros_like(Rg), "sphere": np.zeros_like(Rg)}
        k5ok, worstE = True, 0.0
    else:
        k5dev = 0.0
        for f in FOOTS:
            a0 = A0[f]; u, d = gc_unit(*lb["M31"]); dm = d * KPC
            Ef = float(F11["Efac"](np.array([dm]), L0)[0])
            for m31 in (0.72e11, 1.10e11, 1.51e11):
                gN31 = G * m31 * MSUN / dm ** 2; gph_f = float(F11["g_iso"](m31 * MSUN, a0, L0, yt0, dm)); gph_u = float(F11["g_iso"](m31 * MSUN, a0, None, None, dm))
                P(f"    {f:<9} M31 {m31:.2e} at {d:.0f} kpc (Galactocentric): Newtonian field {gN31 / a0:.3e} a0 survives the band-pass at "
                  f"{Ef:.4f}; its isolated phantom at the MW {gph_f / a0:.3e} a0 = {gph_f / gph_u:.3f} of the unfiltered {gph_u / a0:.3e} a0")
                tab, info = pert_table("M31", m31, f)
                EFE[("M31", f, m31)] = tab
                k5dev = max(k5dev, abs(info["gz0"] / info["dgb"] - 1))
                if m31 == 1.10e11:
                    EFE[("M31", f)] = tab
                    OUT["numbers"].setdefault("E_M31", {})[f] = dict(Efac=Ef, phantom_ratio=gph_f / gph_u, gN_over_a0=gN31 / a0,
                                                                     phantom_over_a0=gph_f / a0, centre_grid=info["gz0"], centre_dg_body=info["dgb"])
            P(f"      interaction field at the MW centre: grid {info['gz0'] / a0:+.4e} a0 vs FP11's dg_body {info['dgb'] / a0:+.4e} a0")
        sel530 = (Rg >= 5) & (Rg <= 30)
        worstE = max(0.5 * float(np.max(np.abs(EFE[k_]["sun"][sel530]))) for k_ in EFE if len(k_) == 3)          # |dv/v| on the data's azimuths
        worstEdisc = max(float(np.max(np.abs(EFE[k_]["disc"][sel530]))) for k_ in EFE if len(k_) == 3)         # |dg/g|, disc mean (reported)
        P(f"    worst over footings and M31 masses at 5-30 kpc: |dv/v| on the Sun-side wedge {worstE:.1e}; |dg/g| disc mean {worstEdisc:.1e}")
        P("    M31's fractional change of the inward radial field (x 1e-4), nominal 1.10e11:")
        P("      " + f"{'R':>6}" + "".join(f"{f[:3] + ' sun':>11}{f[:3] + ' disc':>11}{f[:3] + ' sph':>11}" for f in FOOTS))
        for r_ in (5, 8.2, 15, 20, 25, 30, 50, 73, 100):
            P("      " + f"{r_:6.1f}" + "".join(f"{1e4 * np.interp(r_, Rg, EFE[('M31', f)][w_]):11.2f}" for f in FOOTS for w_ in ("sun", "disc", "sphere")))
        k5ok = k5dev < 1e-3
        OUT["numbers"]["E_M31_worst_5_30"] = worstE
        # the LMC: reported only (non-equilibrium; not applied)
        for f in FOOTS:
            tabL, infoL = pert_table("LMC", 3.2e9, f)
            EFE[("LMC", f)] = tabL
            P(f"    LMC (reported, NOT applied; baryons 3.2e9 Msun at {infoL['d']:.1f} kpc, static fields): fractional change of the inward field, "
              f"{f}: Sun-side " + ", ".join(f"{r_:g} kpc {np.interp(r_, Rg, tabL['sun']):+.1e}" for r_ in (8.2, 15, 20, 25, 30)) +
              "; disc mean " + ", ".join(f"{r_:g} kpc {np.interp(r_, Rg, tabL['disc']):+.1e}" for r_ in (8.2, 20, 30)))
            OUT["numbers"].setdefault("E_LMC", {})[f] = dict(R=[8.2, 15, 20, 25, 30], sun=[float(np.interp(r_, Rg, tabL["sun"])) for r_ in (8.2, 15, 20, 25, 30)])
    check("K5 CONTROL (FP11): the MW-centred interaction field at the Milky Way equals FP11's direct dipole-kernel integral dg_body to 1e-3",
          "n/a at a0 = 0 (MUTATE)" if MUTATE else f"max |grid/dg_body - 1| over footings and M31 masses {k5dev:.1e}", k5ok)
    check("E1 M31's surviving field changes v_c by < 1e-3 at 5-30 kpc on the data's azimuths (the Sun-side +-30 deg wedge; both footings, "
          "M31 baryons 0.72-1.51e11)", "n/a at a0 = 0 (MUTATE)" if MUTATE else f"worst |delta v/v| {worstE:.1e} (disc-mean |delta g/g| {worstEdisc:.1e}, reported)",
          MUTATE or worstE < 1e-3, load_bearing=not MUTATE,
          reading="M31's field survives the band-pass almost whole (it lies inside L), but across the inner Galaxy it is uniform to "
                  "~r/d: what is left is tidal and a weak non-linear (EFE) term")

    def corr_fac(f, R, which="sun"):
        return np.sqrt(1.0 + np.interp(R, Rg, EFE[("M31", f)][which]))

    # ------------------------------------------------------------------------------------------ F filters
    banner(f"F  THE FILTERS: the heat filter (xi) and the band-pass (L), with H_Y's yield   {el()}")
    worstF1 = 0.0; F1info = {}
    if MUTATE:
        P("    (MUTATE: a0 = 0 -- the filters act only on the scalar, which is absent)")
    else:
        for f in FOOTS:
            a0u = A0[f]; Mu = a0u * KPC ** 2 / G / MSUN; rho = model_rho("McM17"); Mt = sum(MS["McM17"].values())
            Rf, zf = faces(*GRIDS["scan"][0]), faces(*GRIDS["scan"][1])
            c, gNt, gP, s = run_fields(lambda R, Z: rho(R, Z) / Mu, Mt / Mu, Rf, zf)
            z0, z1 = c.zc[0], c.zc[1]
            d2 = 2 * (gP[:, 1] - gP[:, 0]) / (z1 ** 2 - z0 ** 2)                  # d^2 g_phi,R / dz^2 at the midplane (even in z) [a0/kpc^2]
            gtot0 = gNt[:, 0] + gP[:, 0]
            Rfc = c.Rf[1:]
            sel = (Rfc >= 5) & (Rfc <= 30)
            ratio_per_kpc2 = np.abs(d2[sel] / gtot0[sel])                            # |delta g / g| per xi^2 [kpc^-2]
            est_xi = float(np.max(ratio_per_kpc2)) * (XI_PC / 1e3) ** 2
            # the direct double-filtered solve at xi = 100 pc (vertical Gaussian on the source and on the output)
            xt = 0.1; gh_x, gh_w = np.polynomial.hermite_e.hermegauss(24); gh_w = gh_w / gh_w.sum()
            rho_s = lambda R, Z: sum(w_ * rho(R, Z - xt * u_) for u_, w_ in zip(gh_x, gh_w)) / Mu
            c2, gN2, gP2, s2 = run_fields(rho_s, Mt / Mu, Rf, zf)
            zc = c2.zc; zsym = np.concatenate([-zc[::-1], zc])
            gPs0 = np.array([np.sum(gh_w * np.interp(xt * gh_x, zsym, np.concatenate([gP2[i, ::-1], gP2[i]]))) for i in range(c2.nR)])
            dgdir = (gNt[:, 0] + gPs0) - gtot0                                        # the law: Newton unfiltered, the scalar double-filtered
            pred = -xt ** 2 * d2 * 0.5 * 2                                            # xi^2 d2 (leading order of sigma^2 = e^{-xi^2 k^2})
            dirr = np.abs(dgdir[sel] / gtot0[sel]); prr = np.abs(pred[sel] / gtot0[sel])
            worstF1 = max(worstF1, est_xi)
            F1info[f] = dict(estimate_xi003=est_xi, direct_100pc_max=float(np.max(dirr)), taylor_100pc_max=float(np.max(prr)),
                             xi_for_1e3_pc=float(1e3 * math.sqrt(1e-3 / np.max(ratio_per_kpc2))))
            P(f"    {f}: leading term |xi^2 d2g/dz2| / g at xi = {XI_PC} pc: <= {est_xi:.1e} over 5-30 kpc (reaches 1e-3 only at xi = "
              f"{F1info[f]['xi_for_1e3_pc']:.0f} pc); direct double-filtered solve at xi = 100 pc: max |dg/g| {F1info[f]['direct_100pc_max']:.1e} "
              f"vs the leading-order estimate {F1info[f]['taylor_100pc_max']:.1e}")
        OUT["numbers"]["F1"] = F1info
    check("F1 the heat filter at xi = 0.03 pc changes the midplane force by < 1e-3 at 5-30 kpc (leading term evaluated on the solved field, "
          "validated in order of magnitude by a direct double-filtered solve at xi = 100 pc)",
          "n/a at a0 = 0 (MUTATE)" if MUTATE else "; ".join(f"{f}: {v['estimate_xi003']:.1e} (100 pc direct {v['direct_100pc_max']:.1e} vs estimate "
                                                           f"{v['taylor_100pc_max']:.1e})" for f, v in F1info.items()),
          MUTATE or (worstF1 < 1e-3 and all(v["direct_100pc_max"] < 5 * v["taylor_100pc_max"] + 1e-4 for v in F1info.values())),
          reading=("" if MUTATE else f"at xi = 100 pc (FP14's galaxy ceiling) the direct solve moves the force by <= "
                   f"{max(v['direct_100pc_max'] for v in F1info.values()):.1e} (the leading-order estimate is conservative by ~"
                   f"{max(v['taylor_100pc_max'] / v['direct_100pc_max'] for v in F1info.values()):.0f}x): the rotation curve does not constrain xi "
                   f"anywhere in the chain's window"))
    worstF2 = 0.0; F2info = {}
    if not MUTATE:
        phantom = F11["phantom"]; RG6 = F11["RG"]; YIELD = F11["YIELD"]
        for f in FOOTS:
            a0 = A0[f]; Mk = sum(MS["McM17"].values()) * MSUN
            base = phantom(Mk, a0, None, None, 4)
            for lab, Lm, yt, mm in (("H_Y", L0, yt0, YIELD), ("H_S", L_HS0_MPC * MPCm, None, 4)):
                Mph = phantom(Mk, a0, Lm, yt, mm)
                rr = np.array([5, 8.2, 10, 15, 20, 25, 30, 50, 100]) * KPC
                rat = (Mk + np.interp(rr, RG6, Mph)) / (Mk + np.interp(rr, RG6, base)) - 1
                F2info[f"{f}/{lab}"] = rat
                worstF2 = max(worstF2, float(np.max(np.abs(rat[:7]))))
                P(f"    {f} {lab} (L = {Lm / MPCm:.3f} Mpc, y_th = {yt}): fractional change of g at 5, 8.2, 10, 15, 20, 25, 30, 50, 100 kpc: "
                  + ", ".join(f"{x:+.1e}" for x in rat))
        OUT["numbers"]["F2"] = F2info
    check("F2 the band-pass (H_Y L(0) = 1.690 Mpc; H_S 2.879 Mpc) and H_Y's yield change g by < 1e-3 at 5-30 kpc (FP6's phantom())",
          "n/a at a0 = 0 (MUTATE)" if MUTATE else f"worst |delta g/g| at 5-30 kpc {worstF2:.1e}", MUTATE or worstF2 < 1e-3)

    # ------------------------------------------------------------------------------------------ D the data
    banner(f"D  THE DATA: chi^2 at the census baryons, the fitted stellar mass, and the decline   {el()}")
    FITS = {}

    def fit_f(k, f, d, sel, which="tot", newton=False, corr=False):
        def c2(fs):
            vm = v_model(k, f, fs, d["R"][sel], newton) * corr_fac(f, d["R"][sel])
            dd = {kk: (vv[sel] if isinstance(vv, np.ndarray) and len(vv) == len(d["R"]) else vv) for kk, vv in d.items()}
            return chi2_corr(vm, dd) if corr else chi2_diag(vm, dd, which)
        lo, hi = (0.0, 12.0) if (newton or A0_LAW[f] == 0) else (FSTAR[0], FSTAR[-1])
        grid = np.linspace(lo, hi, 241); cg = np.array([c2(x) for x in grid]); j = int(np.argmin(cg))
        a_, b_ = grid[max(j - 1, 0)], grid[min(j + 1, len(grid) - 1)]
        r = minimize_scalar(c2, bounds=(a_, b_), method="bounded", options={"xatol": 1e-5})
        fb, cb = float(r.x), float(r.fun)

        def side(sgn):                                  # the Delta chi^2 = 1 edge: geometric steps out, then brentq
            x, st = fb, 1e-4
            while True:
                xn = x + sgn * st
                if xn <= lo or xn >= hi:
                    return lo if sgn < 0 else hi
                if c2(xn) > cb + 1.0:
                    return brentq(lambda t: c2(t) - cb - 1.0, min(x, xn), max(x, xn), xtol=1e-7)
                x, st = xn, st * 1.6
        edge = (fb <= lo + 1e-3) or (fb >= hi - 1e-3)
        return dict(f=fb, chi2=cb, lo=float(side(-1)), hi=float(side(+1)), edge=edge, n=int(sel.sum()))

    rows = []
    for dk, d in D.items():
        allp = np.ones(len(d["R"]), bool); outp = d["R"] >= 19.0; o15 = d["R"] >= 15.0; o13 = d["R"] >= 13.0
        for k in MODELS:
            for f in FOOTS:
                vm1 = v_model(k, f, 1.0, d["R"]) * corr_fac(f, d["R"])
                c_cen = chi2_diag(vm1, d); c_cen_stat = chi2_diag(vm1, d, "stat") if not d["sys_in_s"] else float("nan")
                inner = (d["R"] >= 5) & (d["R"] <= 12)
                dv_in = float(np.mean(vm1[inner] - d["v"][inner])) if inner.any() else float("nan")
                fa = fit_f(k, f, d, allp); fo = fit_f(k, f, d, outp); f15 = fit_f(k, f, d, o15); f13 = fit_f(k, f, d, o13)
                fc = fit_f(k, f, d, allp, corr=True) if d["corr"] is not None else None
                vmb = v_model(k, f, fa["f"], d["R"]) * corr_fac(f, d["R"])
                c_out = chi2_diag(vmb[outp], {kk: (vv[outp] if isinstance(vv, np.ndarray) and len(vv) == len(d["R"]) else vv) for kk, vv in d.items()})
                ffl = MSTAR_FLOOR / MS[k]["star"]
                vfl = v_model(k, f, ffl, d["R"]) * corr_fac(f, d["R"])
                zfl = float(np.min(((d["v"] - vfl) / d["stot"])[outp])) if outp.any() else float("nan")
                g_mod = wgamma(d["R"][outp], vmb[outp], d["stot"][outp])[0] if outp.sum() >= 3 else float("nan")
                g_dat, g_err = wgamma(d["R"][outp], d["v"][outp], d["stot"][outp]) if outp.sum() >= 3 else (float("nan"), float("nan"))
                sl_mod = wslope(d["R"], vmb, d["stot"])[0]; sl_dat, sl_err = wslope(d["R"], d["v"], d["stot"])
                gas_cgm = MS[k]["gas"] + MS[k]["cgm"]
                c_all_stat = chi2_diag(vmb, d, "stat") if not d["sys_in_s"] else float("nan")
                c_out_stat = float(np.sum(((vmb[outp] - d["v"][outp]) / d["s"][outp]) ** 2)) if not d["sys_in_s"] else float("nan")
                row = dict(data=dk, model=k, foot=f, N=len(d["R"]), chi2_census=c_cen, chi2_census_stat=c_cen_stat, dv_inner_census=dv_in,
                           chi2_all_stat=c_all_stat, chi2_outer_stat_at_all=c_out_stat, f_13=f13, Mstar_13=f13["f"] * MS[k]["star"],
                           p_13=pval(f13["chi2"], f13["n"] - 1),
                           f_all=fa, Mstar_all=fa["f"] * MS[k]["star"], Mb_all=fa["f"] * MS[k]["star"] + gas_cgm,
                           Mstar_all_lo=fa["lo"] * MS[k]["star"], Mstar_all_hi=fa["hi"] * MS[k]["star"],
                           chi2_all=fa["chi2"], p_all=pval(fa["chi2"], fa["n"] - 1),
                           chi2_outer_at_all=c_out, N_outer=int(outp.sum()), p_outer_at_all=pval(c_out, int(outp.sum())),
                           f_outer=fo, Mstar_outer=fo["f"] * MS[k]["star"], f_15=f15, Mstar_15=f15["f"] * MS[k]["star"],
                           f_corr=fc, floor_min_z=zfl, gamma_model=g_mod, gamma_data=g_dat, gamma_data_err=g_err,
                           slope_model=sl_mod, slope_data=sl_dat, slope_data_err=sl_err)
                rows.append(row); FITS[(dk, k, f)] = row
    OUT["numbers"]["fits"] = rows
    P("    per curve / model / footing -- chi^2 (stat (+) sys, the published budget) at the census baryons; the fitted f_* (M_*) and its chi^2;")
    P("    the outer points (R >= 19 kpc) at that fit; the outer-only fitted M_*; the floor (lowest census M_* = 3.0e10) margin; the")
    P("    outer power-law index (model vs data, same weights); dv = model - data at 5-12 kpc for the census baryons [km/s]")
    hdr = (f"    {'curve':<5}{'model':<10}{'foot':<6}{'N':>3}{'chi2@cen':>9}{'dv5-12':>8}{'f_*':>6}{'M_* [1e10]':>15}{'chi2':>7}{'p':>7}"
           f"{'out:chi2/N':>11}{'p':>7}{'M_*(R>=19)':>11}{'M_*(R>=15)':>11}{'floor z':>8}{'gam mod':>8}{'gam dat':>12}")
    P(hdr)
    for r in rows:
        fa = r["f_all"]
        P(f"    {r['data']:<5}{r['model']:<10}{r['foot'][:5]:<6}{r['N']:>3}{r['chi2_census']:>9.1f}{r['dv_inner_census']:>8.1f}{fa['f']:>6.2f}"
          f"{r['Mstar_all'] / 1e10:>7.2f} ({r['Mstar_all_lo'] / 1e10:.2f}-{r['Mstar_all_hi'] / 1e10:.2f}){'*' if fa['edge'] else ''}"
          f"{r['chi2_all']:>7.1f}{r['p_all']:>7.3f}{r['chi2_outer_at_all']:>7.1f}/{r['N_outer']:<3d}{r['p_outer_at_all']:>7.3f}"
          f"{r['Mstar_outer'] / 1e10:>9.2f}{'*' if r['f_outer']['edge'] else ' '}{r['Mstar_15'] / 1e10:>9.2f}{'*' if r['f_15']['edge'] else ' '}"
          f"{r['floor_min_z']:>8.2f}{r['gamma_model']:>8.3f}{r['gamma_data']:>7.3f}+-{r['gamma_data_err']:.3f}")
    P("    (* = at the edge of the scanned f_* range)")
    P("\n    the correlated-systematics variant (stat + a common normalisation + the published slope systematic + the per-point excess):")
    for r in rows:
        if r["f_corr"] is not None and r["model"] in ("McM17", "B2", "Cau20+CGM"):
            P(f"      {r['data']} {r['model']:<10} {r['foot']:<9}: f_* {r['f_corr']['f']:.2f} (M_* {r['f_corr']['f'] * MS[r['model']]['star'] / 1e10:.2f}e10), "
              f"chi2 {r['f_corr']['chi2']:.1f} / {r['f_corr']['n'] - 1}")
    for dk in ("J23", "O24"):
        P(f"    published outer power-law index (v ~ R^gamma, R > 19 kpc): {dk} {D[dk]['gamma_pub'][0]:+.2f} +- {D[dk]['gamma_pub'][1]:.2f} "
          f"(this lane's weighted fit of the same table: {FITS[(dk, 'McM17', 'canonical')]['gamma_data']:+.3f} +- {FITS[(dk, 'McM17', 'canonical')]['gamma_data_err']:.3f})")
    P("\n    published linear slopes (5-25 kpc) vs the chain's law at the fitted mass (same radii and weights):")
    for dk, d in D.items():
        for f in FOOTS:
            r = FITS[(dk, "McM17", f)]
            P(f"      {dk} {f:<9}: data slope {r['slope_data']:+.2f} +- {r['slope_data_err']:.2f} (published {d['slope_pub'][0]:+.2f} +- {d['slope_pub'][1]:.2f} "
              f"(+- {d['slope_pub'][2]:.2f} sys)); McM17 model {r['slope_model']:+.2f}; B2 model {FITS[(dk, 'B2', f)]['slope_model']:+.2f}")

    # ------------------------------------------------------------------------------------------ C predicted against measured
    banner(f"C  PREDICTED AGAINST MEASURED (McM17 shape; census f_* = 1 and each curve's whole-curve fit; M31 applied)   {el()}")
    CUR = {}
    for dk, d in D.items():
        fa = {f: FITS[(dk, "McM17", f)]["f_all"]["f"] for f in FOOTS}
        cols = {}
        for f in FOOTS:
            cols[f"{f}/census"] = v_model("McM17", f, 1.0, d["R"]) * corr_fac(f, d["R"])
            cols[f"{f}/fit"] = v_model("McM17", f, fa[f], d["R"]) * corr_fac(f, d["R"])
        CUR[dk] = dict(R=d["R"], v=d["v"], s_stat=d["s"], s_tot=d["stot"], f_fit=fa, **cols)
        st = "; ".join(f"{f}: chi2 (stat (+) sys) {FITS[(dk, 'McM17', f)]['chi2_census']:.1f} at census, {FITS[(dk, 'McM17', f)]['chi2_all']:.1f} at the fit; "
                        f"stat only {FITS[(dk, 'McM17', f)]['chi2_census_stat']:.0f} / {FITS[(dk, 'McM17', f)]['chi2_all_stat']:.0f}" for f in FOOTS)
        P(f"    {dk}: {d['cite']}; N = {len(d['R'])}; fitted f_* canonical {fa['canonical']:.3f}, alt {fa['alt']:.3f}")
        P(f"      {st}" + ("  (stat only: n/a, the table's sigma includes systematics)" if d["sys_in_s"] else ""))
        P(f"      {'R':>6}{'v_obs':>8}{'s_stat':>7}{'s_tot':>7}{'can cen':>9}{'can fit':>9}{'(z)':>6}{'alt cen':>9}{'alt fit':>9}{'(z)':>6}")
        for i in range(len(d["R"])):
            zc_ = (cols["canonical/fit"][i] - d["v"][i]) / d["stot"][i]; za_ = (cols["alt/fit"][i] - d["v"][i]) / d["stot"][i]
            P(f"      {d['R'][i]:6.2f}{d['v'][i]:8.2f}{d['s'][i]:7.2f}{d['stot'][i]:7.2f}{cols['canonical/census'][i]:9.1f}{cols['canonical/fit'][i]:9.1f}"
              f"{zc_:+6.1f}{cols['alt/census'][i]:9.1f}{cols['alt/fit'][i]:9.1f}{za_:+6.1f}")
    OUT["numbers"]["C_curves_McM17"] = CUR
    P("\n    the outer points (R >= 19 kpc) at the whole-curve fit with STATISTICAL errors only (no systematics), McM17 / best shape:")
    for dk, d in D.items():
        if d["sys_in_s"]:
            P(f"      {dk}: n/a (the table's sigma includes systematics)"); continue
        bst = min((FITS[(dk, k, f)]["chi2_outer_stat_at_all"], k, f) for k in MODELS for f in FOOTS)
        P(f"      {dk}: McM17 canonical {FITS[(dk, 'McM17', 'canonical')]['chi2_outer_stat_at_all']:.1f} / alt {FITS[(dk, 'McM17', 'alt')]['chi2_outer_stat_at_all']:.1f} "
          f"for {FITS[(dk, 'McM17', 'canonical')]['N_outer']} points (p {pval(FITS[(dk, 'McM17', 'canonical')]['chi2_outer_stat_at_all'], FITS[(dk, 'McM17', 'canonical')]['N_outer']):.3f} / "
          f"{pval(FITS[(dk, 'McM17', 'alt')]['chi2_outer_stat_at_all'], FITS[(dk, 'McM17', 'alt')]['N_outer']):.3f}); best {bst[1]} {bst[2]} {bst[0]:.1f} "
          f"(p {pval(bst[0], FITS[(dk, 'McM17', 'canonical')]['N_outer']):.3f})")
    P("\n    DECLINE-ONLY FITS (R >= 13 kpc, f_* free, a0 FIXED by the footing; Coquery & Blanchard 2025 fitted J23 at r > ~13 kpc with a0 free):")
    for dk in D:
        P(f"      {dk}: " + "; ".join(f"{k} {f[:3]} M_* {FITS[(dk, k, f)]['Mstar_13'] / 1e10:.2f}e10 chi2 {FITS[(dk, k, f)]['f_13']['chi2']:.1f}/"
                                   f"{FITS[(dk, k, f)]['f_13']['n'] - 1} (p {FITS[(dk, k, f)]['p_13']:.3f})" for k in ('McM17', 'Cau20', 'B2') for f in FOOTS))
    Rp = np.array([5.0, 8.2, 10, 15, 20, 25, 30, 40, 50, 73, 100])
    P("    the predicted curve at 5-100 kpc [km/s] at each curve's fitted mass (McM17 shape, M31 applied on the Sun-side wedge):")
    for dk in D:
        for f in FOOTS:
            fs = FITS[(dk, "McM17", f)]["f_all"]["f"]; vv = v_model("McM17", f, fs, Rp) * corr_fac(f, Rp)
            OUT["numbers"].setdefault("C_pred_5_100", {})[f"{dk}/{f}"] = dict(R=Rp, v=vv, Mstar=fs * MS["McM17"]["star"])
            P(f"      {dk} {f:<9} M_* {fs * MS['McM17']['star'] / 1e10:.2f}e10: " + " ".join(f"{r_:g}:{x:.1f}" for r_, x in zip(Rp, vv)))

    # ------------------------------------------------------------------------------------------ T1 (load-bearing; MUTATE flips it)
    t1 = {f"{dk}/{f}": FITS[(dk, "McM17", f)]["Mstar_15"] for dk in D for f in FOOTS}
    t1_edge = any(FITS[(dk, "McM17", f)]["f_15"]["edge"] for dk in D for f in FOOTS)
    t1ok = all(v < 2 * CENSUS["McMillan17"][0] for v in t1.values()) and not t1_edge
    check("T1 THE LAW SUPPLIES THE OUTER FORCE: fitted to each Gaia curve's points at R >= 15 kpc (McM17 shape, gas fixed), the chain's law "
          "needs a stellar mass below 2x McMillan's census (1.09e11 Msun) on both footings",
          ", ".join(f"{k_} {v_ / 1e10:.2f}e10" for k_, v_ in t1.items()) + (" (edge hit)" if t1_edge else ""), t1ok,
          reading="Newton on the same baryons needs ~3x (the MUTATE); the chain's law needs the amounts printed")

    # ------------------------------------------------------------------------------------------ X  the free-a0 diagnostic
    banner(f"X  DIAGNOSTIC (not the theory: P1 fixes a0): which a0 would the curves' SHAPE pick, algebraic P2 on each model's Newtonian field   {el()}")
    XD = {}
    if not MUTATE:
        for dk, d in D.items():
            for k in ("McM17", "B2"):
                for sub, sel in (("all", np.ones(len(d["R"]), bool)), ("R>=13", d["R"] >= 13.0)):
                    VN2 = SPL[(k, "canonical")][1]; vst2 = (VN2[-1] - VN2[0]) / (FSTAR[-1] - FSTAR[0]); vg2 = VN2[0] - FSTAR[0] * vst2
                    R_ = d["R"][sel]

                    def c2a(p):
                        fs, la = p
                        if fs <= 0: return 1e12
                        gN = np.interp(R_, Rg, vg2 + fs * vst2) / R_ * 1e6 / KPC; a0 = 10 ** la
                        vv = np.sqrt(gN * np.sqrt(1 + a0 / gN) * R_ * KPC) / 1e3
                        return float(np.sum(((vv - d["v"][sel]) / d["stot"][sel]) ** 2))
                    best = None
                    for fs0 in (0.8, 1.2, 1.8, 2.6):
                        for la0 in (-11.5, -10.5, -10.0, -9.6):
                            rr = minimize(c2a, [fs0, la0], method="Nelder-Mead", options={"xatol": 1e-5, "fatol": 1e-6, "maxiter": 4000})
                            if best is None or rr.fun < best.fun: best = rr
                    fsb, lab_ = best.x
                    prof = {}
                    for la in np.linspace(-13, -9.3, 75):
                        prof[la] = minimize_scalar(lambda fs: c2a([fs, la]), bounds=(0.05, 8.0), method="bounded").fun
                    las = np.array(list(prof.keys())); cps = np.array(list(prof.values()))
                    ok95 = las[cps <= best.fun + 3.84]
                    c_can = minimize_scalar(lambda fs: c2a([fs, math.log10(A0["canonical"])]), bounds=(0.05, 8.0), method="bounded").fun
                    c_alt = minimize_scalar(lambda fs: c2a([fs, math.log10(A0["alt"])]), bounds=(0.05, 8.0), method="bounded").fun
                    XD[(dk, k, sub)] = dict(a0_best=10 ** lab_, f_best=fsb, chi2_best=float(best.fun), a0_95=(10 ** ok95.min(), 10 ** ok95.max()),
                                            dchi2_canonical=c_can - float(best.fun), dchi2_alt=c_alt - float(best.fun), n=int(sel.sum()))
                    P(f"    {dk} {k:<6} {sub:<6}: best a0 {10 ** lab_:.2e} (f_* {fsb:.2f}, chi2 {best.fun:.1f}/{sel.sum() - 2}); 95% a0 range "
                      f"{10 ** ok95.min():.1e}-{10 ** ok95.max():.1e}; the chain's canonical / alt cost dchi2 = {c_can - best.fun:+.2f} / {c_alt - best.fun:+.2f}")
        OUT["numbers"]["X_free_a0"] = [dict(key=list(k_), **v_) for k_, v_ in XD.items()]
    else:
        P("    (MUTATE: skipped)")

    # ------------------------------------------------------------------------------------------ N LambdaCDM control
    banner(f"N  THE LambdaCDM CONTROL: Newtonian baryons (census) + a spherical NFW, fitted to each curve   {el()}")
    hlit = H0_KMS / 100.0

    def v_nfw(R, M200, c):
        R200 = (3 * M200 / (4 * math.pi * 200 * RHO_CRIT)) ** (1 / 3); rs = R200 / c; x = R / rs
        mfun = lambda t: np.log1p(t) - t / (1 + t)
        return np.sqrt(GK * M200 * mfun(x) / mfun(c) / R)

    def c_dm14(M200):
        return 10 ** (0.905 - 0.101 * math.log10(M200 * hlit / 1e12))

    NF = {}
    for dk, d in D.items():
        for k in ("McM17", "Cau20", "B2"):
            vb = v_model(k, "canonical", 1.0, d["R"], newton=True)

            def c2n(p, cfix=False):
                lm, lc = p
                if not (10.0 < lm < 13.5): return 1e12
                c = c_dm14(10 ** lm) if cfix else 10 ** lc
                if not (1.0 < c < 200.0): return 1e12
                vv = np.sqrt(vb ** 2 + v_nfw(d["R"], 10 ** lm, c) ** 2)
                return float(np.sum(((vv - d["v"]) / d["stot"]) ** 2))
            best = None
            for lm0 in (11.3, 11.8, 12.2):
                for lc0 in (0.8, 1.2, 1.6):
                    rr = minimize(c2n, [lm0, lc0], method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-7, "maxiter": 4000})
                    if best is None or rr.fun < best.fun: best = rr
            r1 = minimize_scalar(lambda lm: c2n([lm, 0.0], True), bounds=(10.5, 13.3), method="bounded")
            lm, lc = best.x; zc = (lc - math.log10(c_dm14(10 ** lm))) / 0.11
            NF[(dk, k)] = dict(M200=10 ** lm, c=10 ** lc, chi2=float(best.fun), N=len(d["R"]), c_dm14=c_dm14(10 ** lm), c_sigma=zc,
                               M200_cfix=10 ** float(r1.x), chi2_cfix=float(r1.fun))
            P(f"    {dk} + {k:<6}: free (M200, c) -> M200 {10 ** lm:.2e}, c {10 ** lc:5.1f} (c(M) {c_dm14(10 ** lm):.1f}: {zc:+.1f} sigma at 0.11 dex), "
              f"chi2 {best.fun:6.1f}/{len(d['R']) - 2}  |  c on c(M): M200 {10 ** float(r1.x):.2e}, chi2 {r1.fun:6.1f}/{len(d['R']) - 1}")
    OUT["numbers"]["N_nfw"] = [dict(key=list(k_), **v_) for k_, v_ in NF.items()]

    # ------------------------------------------------------------------------------------------ B beyond 30 kpc
    banner(f"B  BEYOND 30 kpc: Bird et al. 2022's enclosed masses vs the chain's law at the whole-curve fitted mass   {el()}")
    BB = {}
    for dk in D:
        for k in ("McM17", "Cau20", "Cau20+CGM", "B2"):
            for f in FOOTS:
                fs = FITS[(dk, k, f)]["f_all"]["f"]; zs = []
                for b in BIRD:
                    v = float(v_model(k, f, fs, np.array([b["r"]]))[0] * corr_fac(f, np.array([b["r"]]), "sphere")[0])
                    Mm = v ** 2 * b["r"] / GK; zs.append((Mm - b["M"]) / math.hypot(b["er"], b["es"]))
                BB[(dk, k, f)] = zs
    for k in ("McM17", "Cau20", "Cau20+CGM", "B2"):
        P(f"    {k:<10}: z = (model - Bird) / sigma at 52 / 73 kpc, per curve's fitted mass: " +
          "; ".join(f"{dk}/{f[:3]} {BB[(dk, k, f)][0]:+.1f} {BB[(dk, k, f)][1]:+.1f}" for dk in D for f in FOOTS))
    OUT["numbers"]["B_bird"] = [dict(key=list(k_), z=v_) for k_, v_ in BB.items()]

    # ------------------------------------------------------------------------------------------ K4 part 2: the f_* interpolation
    banner(f"K4b  the cubic interpolation in f_* against direct solves at fitted values   {el()}")
    chk = [("McM17", "canonical", FITS[("O24", "McM17", "canonical")]["f_all"]["f"]), ("B2", "alt", FITS[("J23", "B2", "alt")]["f_all"]["f"])]
    chk = [(k, f, round(min(max(fs, FSTAR[0]), FSTAR[-1]), 4)) for k, f, fs in chk]
    worst4b = 0.0
    for tk, r in pool.imap_unordered(solve_task, [(k, f, fs, 1.0, "scan") for k, f, fs in chk]):
        sel = (Rg >= 5) & (Rg <= 100)
        dv = float(np.max(np.abs(v_model(tk[0], tk[1], tk[2], Rg[sel]) / r["vA"][sel] - 1))); worst4b = max(worst4b, dv)
        P(f"    {tk[0]} {tk[1]} f_* {tk[2]}: spline vs direct max |dv/v| over 5-100 kpc = {dv:.1e}")
    pool.close(); pool.join()
    OUT["numbers"]["K4_spline"] = worst4b
    check("K4 CONTROL: the scan grid agrees with a finer grid to <= 0.3% at 5-100 kpc, and the cubic interpolation in f_* agrees with a "
          "direct solve at fitted values to <= 0.2%", f"grid {worst4:.1e}; interpolation {worst4b:.1e}", worst4 < 3e-3 and worst4b < 2e-3)

    # ------------------------------------------------------------------------------------------ H the pre-declared hypotheses
    banner("H  THE PRE-DECLARED HYPOTHESES, as they fall")
    G_ = lambda dk, k, f: FITS[(dk, k, f)]
    h1v = {f"{dk}/{k}/{f}": G_(dk, k, f)["dv_inner_census"] for dk in D for k in ("McM17", "Cau20", "B2") for f in FOOTS}
    h1 = all(v <= -15.0 for v in h1v.values() if np.isfinite(v))
    check("H1 (reported, pre-declared) NORMALISATION: at the census baryons the law is >= 15 km/s low at 5-12 kpc for McM17, Cau20, B2, "
          "both footings, every curve", f"mean model - data at 5-12 kpc: {min(h1v.values()):+.1f} .. {max(h1v.values()):+.1f} km/s", h1, load_bearing=False)
    ms_can = [G_(dk, "McM17", "canonical")["Mstar_all"] for dk in D]; ms_alt = [G_(dk, "McM17", "alt")["Mstar_all"] for dk in D]
    zc_mcm = [(m - CENSUS["McMillan17"][0]) / math.hypot(CENSUS["McMillan17"][1], 0.5 * (G_(dk, "McM17", f)["Mstar_all_hi"] - G_(dk, "McM17", f)["Mstar_all_lo"]))
              for dk in D for f, m in zip(("canonical",), [G_(dk, "McM17", "canonical")["Mstar_all"]])]
    zl_alt = [(G_(dk, "McM17", "alt")["Mstar_all"] - CENSUS["LicquiaNewman15"][0]) / CENSUS["LicquiaNewman15"][1] for dk in D]
    h2 = all(7e10 <= m <= 9e10 for m in ms_can) and all(6e10 <= m <= 8e10 for m in ms_alt) and all(z > 2 for z in zc_mcm) and all(z < 2 for z in zl_alt)
    check("H2 (reported, pre-declared) REQUIRED MASS: whole-curve fits need M_* 7-9e10 (canonical) / 6-8e10 (alt) with the McM17 shape; > 2 sigma "
          "above McMillan's census; within 2 sigma of Licquia & Newman on the alt footing",
          f"canonical {', '.join(f'{m / 1e10:.2f}' for m in ms_can)}e10; alt {', '.join(f'{m / 1e10:.2f}' for m in ms_alt)}e10 (E19, O24, Z23, J23 order: "
          f"{list(D)}); vs McMillan (canonical) {', '.join(f'{z:+.1f}' for z in zc_mcm)} sigma; alt vs Licquia & Newman {', '.join(f'{z:+.1f}' for z in zl_alt)} sigma",
          h2, load_bearing=False)
    decl = {dk: max(G_(dk, k, f)["p_outer_at_all"] for k in MODELS for f in FOOTS) for dk in D}
    gam_t = {dk: [(G_(dk, "McM17", f)["gamma_model"] - G_(dk, "McM17", f)["gamma_data"]) / G_(dk, "McM17", f)["gamma_data_err"] for f in FOOTS] for dk in D}
    h3 = all(v >= 0.01 for v in decl.values()) and all(1.5 <= min(gam_t[dk]) and max(gam_t[dk]) <= 2.5 for dk in ("J23", "O24"))
    check("H3 (reported, pre-declared) THE DECLINE: the outer points (R >= 19 kpc) are reproduced at the whole-curve fit (p >= 0.01 on the best "
          "shape/footing for every curve), and the model's outer slope is shallower than J23's / O24's by 1.5-2.5 sigma",
          "best p_outer: " + ", ".join(f"{dk} {v:.3f}" for dk, v in decl.items()) + "; (model - data) outer index in sigma (McM17, can/alt): "
          + ", ".join(f"{dk} {gam_t[dk][0]:+.1f}/{gam_t[dk][1]:+.1f}" for dk in D), h3, load_bearing=False)
    flo = {dk: min(G_(dk, k, f)["floor_min_z"] for k in MODELS for f in FOOTS) for dk in D}
    flo_best = {dk: max(G_(dk, k, f)["floor_min_z"] for k in MODELS for f in FOOTS) for dk in D}
    h4 = all(v >= -2.0 for v in flo_best.values())
    check("H4 (reported, pre-declared) THE FLOOR: no outer point lies > 2 sigma below the law's curve at the lowest census stellar mass "
          "(3.0e10), on the most favourable shape/footing", "most negative (data - floor)/sigma, best shape: " + ", ".join(f"{dk} {v:+.2f}" for dk, v in flo_best.items())
          + "; worst shape: " + ", ".join(f"{dk} {v:+.2f}" for dk, v in flo.items()), h4, load_bearing=False)
    if not MUTATE:
        e100 = max(abs(float(np.interp(100.0, Rg, EFE[("M31", f)][w_]))) for f in FOOTS for w_ in ("sun", "disc", "sphere"))
        h5 = worstF1 < 1e-3 and worstF2 < 1e-3 and worstE < 1e-3 and min(OUT["numbers"]["E_M31"][f]["Efac"] for f in FOOTS) > 0.9 and e100 < 0.02
        check("H5 (reported, pre-declared) FILTERS AND M31: < 1e-3 at 5-30 kpc; M31's field survives at > 90%; < 2% at 100 kpc",
              f"xi {worstF1:.1e}, L {worstF2:.1e}, M31 {worstE:.1e}; surviving Newtonian fraction {OUT['numbers']['E_M31']['canonical']['Efac']:.3f}; at 100 kpc {e100:.1e}",
              h5, load_bearing=False)
    csig = {dk: max(NF[(dk, k)]["c_sigma"] for k in ("McM17", "Cau20", "B2")) for dk in D}
    h6 = all(min(NF[(dk, k)]["chi2"] / NF[(dk, k)]["N"] for k in ("McM17", "Cau20", "B2")) <= 1.0 for dk in D) and all(
        min(NF[(dk, k)]["c_sigma"] for k in ("McM17", "Cau20", "B2")) > 2 for dk in ("J23", "O24"))
    check("H6 (reported, pre-declared) LambdaCDM CONTROL: NFW + baryons fit every curve at chi^2/N <= 1 (free M200, c), with c > 2 sigma above "
          "c(M) for J23 and O24", "; ".join(f"{dk}: best chi2/N {min(NF[(dk, k)]['chi2'] / NF[(dk, k)]['N'] for k in ('McM17', 'Cau20', 'B2')):.2f}, "
                                              f"c offsets " + "/".join(f"{NF[(dk, k)]['c_sigma']:+.1f}" for k in ("McM17", "Cau20", "B2")) for dk in D), h6, load_bearing=False)
    check("H7 (reported, pre-declared) MUTATE: with a0 -> 0 T1 fails", "this is the MUTATE run" if MUTATE else "see the MUTATE run (T1 above passes here)",
          (not t1ok) if MUTATE else True, load_bearing=False)
    bz = [abs(z) for dk in D for f in FOOTS for k in ("McM17", "Cau20+CGM") for z in BB[(dk, k, f)]]
    bz_best = {dk: min(max(abs(z) for z in BB[(dk, k, f)]) for k in ("McM17", "Cau20", "Cau20+CGM", "B2") for f in FOOTS) for dk in D}
    h8 = all(v <= 1.5 for v in bz_best.values())
    check("H8 (reported, pre-declared) BEYOND 30 kpc: within 1.5 sigma of Bird+2022 at 52 and 73 kpc (CGM range 0 .. Cautun's)",
          "best |z| per curve's fitted mass: " + ", ".join(f"{dk} {v:.2f}" for dk, v in bz_best.items()) + f"; all McM17/Cau20+CGM |z| <= {max(bz):.2f}",
          h8, load_bearing=False)

    # ------------------------------------------------------------------------------------------ V the verdict
    banner("V  THE VERDICT (pre-declared decision rules)")
    repro = all(decl[dk] >= 0.01 for dk in D) and all(flo_best[dk] >= -2.0 for dk in D)
    fails = any(flo_best[dk] < -2.0 for dk in D) or any(decl[dk] < 0.01 for dk in D)
    zLN = {f"{dk}/{k}/{f}": (G_(dk, k, f)["Mstar_all"] - CENSUS["LicquiaNewman15"][0]) / CENSUS["LicquiaNewman15"][1] for dk in D for k in MODELS for f in FOOTS}
    budget = "CONSISTENT" if min(abs(v) for v in zLN.values()) <= 2.0 else "TENSION"
    budget_per_curve = {dk: min(abs(zLN[f"{dk}/{k}/{f}"]) for k in MODELS for f in FOOTS) for dk in D}
    verdict = "REPRODUCES THE DECLINE" if repro else ("FAILS THE DECLINE" if fails else "UNDECIDED")
    OUT["verdict"] = dict(decline=verdict, budget=budget, best_p_outer=decl, floor_best=flo_best, budget_min_sigma_LN=budget_per_curve)
    P(f"    decline: {verdict} -- best p(chi^2_outer) per curve {', '.join(f'{dk} {v:.3f}' for dk, v in decl.items())}; floor margins "
      f"{', '.join(f'{dk} {v:+.2f}' for dk, v in flo_best.items())} sigma")
    P(f"    baryon budget: {budget} -- the closest shape/footing to Licquia & Newman 2015 per curve: "
      f"{', '.join(f'{dk} {v:.1f} sigma' for dk, v in budget_per_curve.items())}")

    nlb = sum(1 for _, ok, lb_ in CH if lb_ and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(jsonable(OUT), open(fn, "w"), indent=1)
    P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   {el()}")
    return 1 if nlb else 0


if __name__ == "__main__":
    _OUTF = open(os.path.join(HERE, SLUG + ("_MUTATE.out" if MUTATE else ".out")), "w")
    sys.stdout = _Tee(_OUTF)
    rc = main()
    sys.stdout.flush()
    sys.exit(rc)
