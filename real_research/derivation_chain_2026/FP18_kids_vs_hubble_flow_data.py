#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP18 -- IS THE KiDS-VERSUS-R0 PINCER IN THE DATA ITSELF?  A data-only test, with no theory in between: can ONE static
spherical mass profile fit both KiDS-1000's isolated-lens lensing and the Local Volume's Hubble-flow zero-velocity radius?

WHY.  FP12 found the chain's law overshoots the zero-velocity radius R0 of the Local Group (LG), M81 and IC 342 by +0.20 dex
and the 14-group stack by +0.12-0.14 dex, while it fits KiDS's isolated lenses; cutting its phantom beyond ~0.3 Mpc to fix
R0 costs KiDS d chi^2 = +346.  If NO mass profile at all can fit both datasets, the pincer is a tension between two
datasets that every theory inherits (LCDM included), and it does not refute the chain's outer profile in particular.  If one
profile fits both, the pair refutes the chain's outer profile and describes the target its action must produce.

THE DATA (each read at its source for this lane; none quoted from memory)
  (a) Brouwer et al. 2021, A&A 650, A113 (arXiv:2106.11677; files real_research/data/lensing_rar/brouwer2021_rar, README
      read): Fig. 3's excess surface density Delta Sigma(R) of ISOLATED KiDS-bright lenses in four stellar-mass bins,
      log M*/(h70^-2 Msun) = [8.5, 10.3, 10.6, 10.8, 11.0], mean log M_gal (stars + cold gas) = 10.14, 10.57, 10.78, 10.96
      (Fig. 3 panel labels; Sect. 5.5); R = PROPER transverse separation (Sect. 3.1: "we compute Delta Sigma(R) as a function
      of proper transverse separation R"), 0.035-2.6 h70^-1 Mpc, 15 bins; ESD and covariance divided by the multiplicative
      bias (README); H0 = 70 (WMAP9: Om 0.2793); lenses 0.1 < z < 0.5, <z> = 0.25 (Sect. 3.3); isolation: no neighbour
      with > 10% of the lens's M* within 3 h70^-1 Mpc, M* < 1e11; App. A / Fig. A.3: photometric-redshift errors let
      non-isolated lenses in, so at
      R > 0.3 h70^-1 Mpc the ESD is ~30% above that of truly isolated galaxies (MICE); stellar masses carry a >= 0.2 dex
      systematic (Sects. 3.3, 5.2); M_gal = M* (1 + f_cold), log f_cold = -0.69 log M* + 6.63 (Boselli+14, their Eq. 23);
      early/late types differ (Sect. 5.4, Fig. 8; files Fig-8_*: colour split u - r = 2.5).  The binned covariance is
      stored in (m, n, i, j) order: a plain reshape is NOT positive definite (the record's 2026-09-03 correction,
      ccnl_clock_fix_2026.py; hunt_2026/h113 "bug pattern 4"); the corrected order is reshape(4,4,15,15).transpose(0,2,1,3).
  (b) Kashibadze & Karachentsev 2018, A&A 609, A11 (arXiv:1709.09420v2): R0 from a fit of their eq. (14),
      V(R) = H0 R - H0 R0 (R0/R)^(1/2), to galaxies around a group (barycentre frame, "minor attractor" velocities, free H0);
      the 14-group STACK (Table 7: 66 companions of 11 groups): R0 = 0.93 +- 0.02 Mpc, H0 = 85 +- 2, sigma_v = 57 km/s
      (Sect. 6); the LG (Table 4: 35 galaxies): adopted R0 = 0.91 +- 0.05 Mpc (barycentre scan, Table 5: 0.83-0.99);
      Table 8: the stack's R0 over centre/attractor choices, 0.71-1.03 Mpc; mass conversion eq. (4):
      M_T = 1.95e12 (R0/Mpc)^3 Msun (Planck: Om 0.315, OL 0.685, H0 67.3; WMAP: 2.12); their errors come from "a Monte
      Carlo ... assuming that distance errors ... ~5%" (Sect. 4).  Tables 4, 7 and 8 are transcribed below from the paper;
      Table 6 is FP12's transcription (KK18_T6).
  (c) FP12's other published R0 (read at source there): LG 0.96 +- 0.03 (Karachentsev+2009), M81 0.89 +- 0.05
      (Karachentsev & Kashibadze 2006), IC 342 0.90 +- 0.10 (Karachentsev 2005, Table 11), Cen A 1.40 +- 0.11
      (Karachentsev+2007); the groups' baryons (FP12 / k02, UNGC).
  (d) the record's reconstruction of B21's isolated lens sample (real_research/data/lensing_rar/lr_lenses.npz, built by
      real_research/reviews/lensing_rar/lr_esd_remeasure.py): per-bin red fractions (u - r split), used ONLY for the
      galaxy-type systematic, after K6 checks that it reproduces B21's bin mean masses.

CONVENTIONS (stated, as the published estimators use them)
  * The spherical-infall relation with Lambda is K&K 2018's eq. (4) (point mass + Lambda, the shell turning around today):
    M_T(<R0) = COEF R0^3.  COEF = 1.955e12 Msun Mpc^-3 is taken from the record's shell integrator (FP6 lg_R0: shells on
    the Hubble flow from a = 0.02, point mass + Lambda, Planck 2018), which K3 checks against K&K's 1.95e12.  For an
    extended profile the zero-velocity shell encloses a fixed (Lagrangian) mass, so R0 is the OUTERMOST radius where
    M_tot(<R) = COEF R^3 -- the published convention; the Eulerian readings (the profile acting at every epoch, or
    switched on late) are the D section's systematic.
  * M_tot = the lensing excess mass + the mean matter inside R (Planck, z = 0); lensing measures excess over the mean.
  * "Static": the proper-radius profile at the lenses' z ~ 0.25 is the profile at z = 0 (the epoch systematic prices it).
  * Matching: an LV system is compared with the KiDS profile at its central galaxy's M_gal (mapping (i): M* = 0.6 L_K from
    K&K Table 6 (their M* = L_K, FP12 K8), plus B21's own Boselli cold gas), interpolated linearly in log M_gal between
    the bin means (the covariance follows the same linear combination; no extrapolation beyond 10.14-10.96).  Mapping (ii)
    (the group's total baryons, FP12/k02) is reported.  (i) is the conservative one: companions only ADD mass.

THE TEST.  For each LV system, the joint statistic T = min over profiles [chi2_KiDS + chi2_R0] - min over profiles
  [chi2_KiDS], for (1) the FREE profile -- any non-negative spherical density (26 uniform shells, 0-10 Mpc: the family-
  agnostic answer; "relaxed" imposes only M(<R0) <= COEF R0^3 and is a rigorous LOWER bound on T, "full" imposes the exact
  outermost-crossing definition of R0), and (2) four parametric families: NFW (+ the galaxy; c free = LCDM's one-halo),
  NFW + two-halo (LCDM standard: Duffy+08 c(M), Tinker+10 bias, linear xi), truncated isothermal, the chain's baryons +
  phantom (FP9's (H_Y) at z = 0.25) with a free outer cut, a free piecewise power law.  The B section proves and applies the
  model-independent bound that drives everything: for any non-negative spherical excess density, Delta Sigma(R) <=
  M(<R)/(pi R^2), i.e. KiDS measures a LOWER bound M(<R) >= pi R^2 Delta Sigma(R) with no profile assumed.
  R0 ERRORS: the published estimator is re-run on the published tables (K4 reproduces K&K's stack fit); a bootstrap over
  galaxies gives the statistical error from the velocity scatter, which K&K's distance-only Monte Carlo omits; the
  "honest" error is the bootstrap and the quoted error in quadrature.  Both are reported; the rule uses the honest one.
  COMPARABILITY SYSTEMATICS (nuisances, priors declared here): galaxy type (the LV centrals are mostly spirals; KiDS's high-
  mass bins are mostly red): log t ~ N(log t_db, 0.08 dex) about the data-based late-type factor t_db (B21's blue/red
  contrast x the bins' red fractions x the system's late-type fraction); photometric-redshift isolation leakage at
  R > 0.3 Mpc: log l <= 0, half-normal 0.114 dex (= B21's 30%); the stellar-mass scale: N(0, 0.2 dex); the R0 method:
  N(0, 0.05 dex); the eq. (4) coefficient: N(0, 0.04 dex) (Planck 1.95 vs WMAP 2.12); epoch + h: N(0, 0.045 dex) on the
  lensing mass (static to +-10%, h 0.674-0.73).  All shared between systems.

RULE (fixed before this lane's committed run; it was designed after exploratory runs on the same data, so its priors are
  anchored to the published systematic sizes, not to any outcome).  The primary joint sample is K&K 2018's STACK and their
  LG (independent galaxy sets, one paper, one method), mapping (i), the full published radial range, the free profile with
  the exact R0 definition, honest R0 errors, dof = 2:
    COMPATIBLE   if T_nominal (no systematics) <= 5.99 (p >= 0.05): one profile fits both at face value.
    IN TENSION   if T_profiled (every comparability systematic profiled under its prior) > 11.83 (p < 0.0027, 3 sigma),
                 with the published KiDS covariance AND with it inflated by sqrt(chi2/dof) of the NFW fit.
    UNDECIDED    otherwise: the published data disagree but the comparability systematics can absorb it.
  Reported, not in the rule: every other system; mapping (ii); the quoted R0 errors; each systematic alone at its edge; the
  extreme corner (every flat systematic at its bound at once); R <= 0.3 Mpc only (B21's range for analytic models); a
  comoving reading; the direct Hubble-diagram test (the companions' velocities against the KiDS-implied flow); LCDM's own
  fit; the Eulerian dynamics readings.

CHECKS
  K1 CONTROL the Fig-3 covariance: the corrected (m,n,i,j) order is positive definite with diagonal = the published errors^2;
     the plain reshape is indefinite (the record's bug, exhibited).
  K2 CONTROL the ESD machinery: this lane's uniform-shell projection reproduces the analytic NFW Delta Sigma (Wright &
     Brainerd 2000) and the singular isothermal sphere's V^2/(4 G R) to < 1%.
  K2b (reported) side finding: FP6's committed esd_of_M (the record's KiDS 'lead grade' projection) under-projects the same SIS.
  K3 CONTROL the spherical-infall relation: the record's shell integrator gives M/R0^3 = K&K 2018 eq. (4)'s 1.95e12 (< 1%).
  K4 CONTROL the transcribed K&K Table 7 reproduces K&K's stack fit (eq. 14, free H0; their distance-only Monte Carlo):
     R0 = 0.93 +- 0.02-0.03, H0 = 85 +- 2 -- the published estimator runs here as published.
  K5 CONTROL the chain's phantom is FP9's: FP6's kids_class reproduces FP9/FP12's KiDS lead grade (-2.40 / -5.57).
  K6 CONTROL the record's isolated-lens reconstruction reproduces B21's four bin mean masses (<= 0.02 dex).
  K7 CONTROL the bound: Delta Sigma(R) <= M(<R)/(pi R^2) holds for 2000 random non-negative profiles; a mean-density void
     outside R (the most negative excess allowed) raises Delta Sigma at 1 Mpc by < 0.12 Msun/pc^2.
  E1 (reported) the R0 errors: bootstrap vs quoted, stack and LG; FP12's fit form is not K&K's eq. (14) (side finding).
  M  (printed) the matching: each system's KiDS analog (mappings (i)/(ii)), the gas and Upsilon_K choices, the type factors.
  B1 (reported) the bound: KiDS's model-independent M(<R) >= pi R^2 Delta Sigma against each system's COEF R0^3.
  F1 (reported) the free-profile T per system (relaxed and full; honest and quoted errors; mappings (i) and (ii)).
  F2 (reported) the family table (stack and LG): chi2_KiDS alone, the implied R0, the joint fit, d chi2_PG.
  S1, S2 (reported) the comparability systematics: one at a time; profiled; with the extreme corner, the inflated errors,
     R <= 0.3 Mpc, the comoving reading, isolated vs all lenses and the epoch (the chain's own growth) printed alongside.
  D1 (reported) the dynamics: Lagrangian vs Eulerian-static R0 of the KiDS best-fit profile; the latest switch-on epoch.
  H1 (reported) the direct Hubble diagram: the published companions' velocities (K&K Tables 7 and 4) against the KiDS-implied
     flow -- face value, the systematics' corners, profiled, with the local H free and held at the flow's own point-mass value.
  L1 (reported) LCDM's own fit to both.
  V1 [load-bearing; MUTATE must fail] THE PUBLISHED DATA DISAGREE AT FACE VALUE: T_nominal of the primary joint sample
     > 11.83 (p < 0.0027) with honest R0 errors.
  V2 (reported) THE VERDICT by the rule, and the per-system verdicts.   W the ledger.
MUTATE=1 shifts every published R0 by +0.3 dex -- the datasets' own face-value offset (KiDS-fitted profiles turn around at
~1.7-1.9 Mpc against 0.91-0.93): an injection that makes them agree, so the face-value disagreement must vanish, V1 FAILS
(rc = 1) and the verdict turns COMPATIBLE.  (A +0.2 dex shift was tried first: it leaves T = 11.3, 2.9 sigma -- V1 flips only
by a hair and the label stays UNDECIDED, too marginal for a control.)  Outputs: *_MUTATE.out / *_results_MUTATE.json.

SCOPE.  A data-only test: no action term, no chain constant is used except in the chain-shaped family (a shape family
with free mass and cut).  Spherical symmetry: exact for the stacked lensing (random orientations: the stack projects the
spherically averaged excess density) and Gauss's law for the monopole of the infall; the flow's non-sphericity is in the
R0-method prior.  No particle-mesh run (at most 2 workers, < 30 min).
Run from the repository root:  python3 real_research/derivation_chain_2026/FP18_kids_vs_hubble_flow_data.py  (MUTATE=1)
"""
import os, sys, io, json, math, time, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from scipy.optimize import lsq_linear, minimize, minimize_scalar, least_squares, brentq
from scipy.stats import chi2 as chi2_dist, norm as norm_dist
warnings.filterwarnings("ignore")
np.seterr(all="ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import FP12_local_volume_groups_r0 as F12                                     # FP12 -> FP11 -> FP6's machinery (not run)
F11, M6 = F12.F11, F12.M6

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP18_kids_vs_hubble_flow_data"
R0_SHIFT = 0.3 if MUTATE else 0.0                                                 # dex added to every published R0 (MUTATE)
T_LIM2, T_LIM1, T_OK2 = float(chi2_dist.isf(0.0027, 2)), float(chi2_dist.isf(0.0027, 1)), float(chi2_dist.isf(0.05, 2))
RNG_SEED = 20260927

# ================================================================================================= (a) Brouwer+2021 (KiDS-1000)
BDIR = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")


def b21_profile(fname):
    d = np.genfromtxt(os.path.join(BDIR, fname), comments="#")
    return d[:, 0], d[:, 1] / d[:, 4], d[:, 3] / d[:, 4]                          # ESD_t / bias, error / bias (README)


def b21_cov(fname, nb, npb):
    """(corrected, plain) covariance / bias: rows are stored (m, n, i, j) with j fastest (the record's correction)."""
    d = np.genfromtxt(os.path.join(BDIR, fname), comments="#"); v = d[:, 4] / d[:, 6]; n = nb * npb
    good = v.reshape(n, n) if nb == 1 else v.reshape(nb, nb, npb, npb).transpose(0, 2, 1, 3).reshape(n, n)
    return good, v.reshape(n, n)


_KR, _KE, _KS = [], [], []
for _b in range(1, 5):
    _r, _e, _s = b21_profile(f"Fig-3_Lensing-rotation-curves_Massbin-{_b}.txt"); _KR.append(_r); _KE.append(_e); _KS.append(_s)
RD = _KR[0]; KE = np.array(_KE); KS = np.array(_KS)
C60, C60_PLAIN = b21_cov("Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt", 4, 15)
B21_MGAL = np.array([10.14, 10.57, 10.78, 10.96])                                  # Fig. 3 / Sect. 5.5: log <M_gal>
B21_Z, B21_R_ISO, B21_LEAK, B21_MSYS = 0.25, 0.30, 1.30, 0.2                      # <z>; isolation-reliable radius; App. A; Sect. 5.2
B21_GBAR_ISO = 7.56e-14                                                           # App. A: g_gal at R = 0.3 Mpc for log M_gal = 10.69
B21_DELTA_QUOTED = 0.19                                                           # Sect. 5.4: colour split, R < 0.3 Mpc [dex]

# ================================================================================================= (b) Kashibadze & Karachentsev 2018
KK_COEF, KK_COEF_WMAP = 1.95, 2.12                                               # eq. (4) [1e12 Msun Mpc^-3]; WMAP variant
KK_STACK = dict(R0=0.93, e=0.02, H0=85.0, eH=2.0, sig=57.0)                       # Sect. 6, Fig. 5, Table 8 (BC, minor attractor)
KK_LG = dict(R0=0.91, e=0.05)                                                     # Sect. 4 (adopted; Table 5 scan 0.83-0.99)
KK_LG35 = dict(R0=0.95, e=0.03, H0=90.0, sig=42.0)                                # Sect. 4, Fig. 4 upper (35 galaxies)
KK_LG14 = dict(R0=0.85, e=0.03, H0=79.0, sig=23.0)                                # Sect. 4 (14 galaxies disturbed by MW/M31)
KK_T8 = {"MG minor": 0.83, "MG-norm minor": 0.71, "BC minor": 0.93, "BC-norm minor": 0.76,
         "MG major": 0.93, "MG-norm major": 0.76, "BC major": 1.03, "BC-norm major": 0.93}
KK_T6 = [(g, l1, l2, n) for (g, _a, l1, _d1, _b2, l2, _d2, n) in F12.KK18_T6]    # (group, lg L_K main, second, companions)
KK_EARLY = {"CenA/M83", "NGC3379"}                                                # E/S0 centrals (NGC 5128 S0/E; NGC 3379 E1)
# Table 7 (66 companions): main galaxy, name, R_C [Mpc], V_mi, V_ma [km/s] (barycentre frame)
KK_T7 = """M81 UGC04879 2.40 141 147|M81 UGC06456 1.26 -38 -86|M81 NGC3738 2.16 150 170|M81 UGC06757 1.37 51 42|M81 UGC07242 2.06 56 48
|M81 NGC4236 1.13 17 -15|M81 NGC4605 2.36 131 138|M81 DDO165 1.71 56 41|M81 UGC08245 1.54 14 -27|NGC5128 NGC3621 3.50 219 204
|NGC5128 ESO320-014 2.66 134 100|NGC5128 ESO379-007 2.07 129 111|NGC5128 ESO381-018 1.45 81 74|NGC5128 ESO381-020 1.47 55 39
|NGC5128 ESO443-009 1.97 124 119|NGC5128 KK182 1.80 66 62|NGC5128 ESO270-017 2.86 282 289|NGC5128 HIPASS_J1348-37 1.45 56 54
|NGC5128 HIPASS_J1351-47 1.80 20 -11|NGC5128 NGC5408 1.28 0 -25|NGC5128 ESO223-009 2.78 142 120|Maffei2 UGC01281 3.00 215 223
|Maffei2 KK17 2.97 220 238|Maffei2 NGC0784 3.25 240 254|Maffei2 KKH18 2.45 207 243|Maffei2 KKH34 1.80 110 106|N253 WLM 2.76 288 298
|N253 NGC0045 3.02 259 260|N253 PiscesA 3.49 278 292|N253 NGC0059 1.35 163 174|N253 DDO226 1.24 136 138|N253 UGCA438 1.76 178 221
|N4826 AGC749241 1.32 65 59|N4826 GR8 2.26 227 230|N4826 DDO187 2.34 202 207|N4736 NGC3741 1.47 105 95|N4736 DDO099 1.87 99 86
|N4736 UGCA281 1.48 30 12|N4736 DDO126 0.76 -64 -136|N4736 DDO125 1.80 92 90|N4736 Arp211 1.78 146 146|N4736 DDO147 1.42 -4 -13
|N4736 NGC5023 1.72 141 141|N4736 UGC08508 1.94 172 183|N4736 DDO181 1.44 73 59|N4736 DDO183 1.36 107 109|N4736 KK230 2.36 220 235
|N4736 DDO190 1.91 116 85|M101 LVJ1157+5638 3.00 190 215|M101 NGC4068 3.07 131 98|M101 MCG+09-20-131 2.82 161 167
|M101 UGC07298 3.14 149 136|M101 NGC4736 3.07 87 12|M101 NGC5204 2.44 49 40|M101 NGC5238 2.49 43 37|M101 KKH87 1.97 97 96
|M101 DDO194 1.29 15 -4|N4258 KK109 3.23 270 275|N4258 MCG+06-27-017 3.05 185 180|N4258 NGC4395 3.25 222 225
|N4258 NGC4707 1.38 -9 -66|N4258 NGC4861 3.17 371 464|N6744 IC4710 2.06 139 137|N6744 IC4870 1.00 4 -40|N2683 AGC182595 1.61 27 12
|N3379 DDO088 3.20 328 329"""
# Table 4 (35 galaxies around the LG): name, R_c [Mpc], V_cmi, V_cma [km/s], main disturber (barycentre at 0.43 Mpc)
KK_T4 = """WLM 0.83 -10 -7 M31|NGC404 2.53 205 205 Maffei2|KKs3 2.24 103 109 MWay|KKH37 3.17 217 221 M81|UGC4879 1.34 25 33 M31
|LeoA 0.93 -47 -53 MWay|SexB 1.71 94 101 MWay|NGC3109 1.73 94 96 Antlia|SexA 1.78 78 82 MWay|LeoP 1.95 120 128 MWay
|NGC3741 3.27 255 262 M81|DDO99 2.76 247 255 NGC4214|IC3104 2.73 159 162 NGC4945|DDO125 2.69 242 251 M81|DDO147 3.14 342 350 NGC4214
|GR8 2.48 128 132 MWay|UGC8508 2.66 176 184 M81|DDO181 3.19 278 285 NGC4736|DDO183 3.41 247 253 NGC4736|KKH86 2.93 198 202 NGC5128
|UGC8833 3.37 273 280 NGC4736|KK230 2.34 120 127 M81|DDO187 2.51 171 178 MWay|DDO190 2.88 258 267 M81|ESO274-01 3.20 327 329 NGC5128
|KKR25 1.84 126 137 M31|IC4662 2.87 131 135 NGC5128|NGC6789 3.28 153 156 M81|SagdIr 1.19 20 29 MWay|DDO210 0.98 12 22 MWay
|IC5152 2.08 70 77 NGC253|KK258 2.18 151 160 NGC253|Tucana 1.14 61 77 MWay|UGCA438 2.15 101 108 NGC55|KKH98 2.14 171 171 M31"""
T7 = [l.split() for l in KK_T7.replace("\n", "").split("|")]
T4 = [l.split() for l in KK_T4.replace("\n", "").split("|")]
T7_MAIN = {"M81": "M81", "NGC5128": "CenA/M83", "Maffei2": "Maffei2/IC342", "N253": "NGC253", "N4826": "NGC4826",
           "N4736": "NGC4736", "M101": "M101", "N4258": "NGC4258", "N6744": "NGC6744", "N2683": "NGC2683", "N3379": "NGC3379"}

# ================================================================================================= constants, cosmologies
UPS_K = 0.6                                                                       # K-band M/L on the Chabrier scale (k02 / FP12)
G_KMS = 4.30091e-9                                                                # G [Mpc (km/s)^2 / Msun]
H70, OM_W9, OB_W9, NS_W9, S8_W9 = 0.70, 0.2793, 0.0463, 0.972, 0.821               # B21's WMAP9 cosmology (Sect. 3)
RHOC_Z = 2.775e11 * H70 ** 2 * (OM_W9 * (1 + B21_Z) ** 3 + 1 - OM_W9) / 1e12      # rho_crit(z = 0.25) [1e12 Msun / Mpc^3]
RHOM_Z = 2.775e11 * H70 ** 2 * OM_W9 * (1 + B21_Z) ** 3 / 1e12                     # mean matter density, proper, z = 0.25
RHO0 = M6["LG_OM"] * 2.775e11 * M6["LG_h"] ** 2 / 1e12                            # Planck mean matter density at z = 0
LGM = M6["LG_Msun"]; LG_MPC = M6["LG_Mpc"]
A0C = F11.A0["canonical"]


def bos(lms):
    """B21's M_gal = M* (1 + f_cold), log f_cold = -0.69 log M* + 6.63 (their Eq. 23)."""
    return lms + math.log10(1 + 10 ** (-0.69 * lms + 6.63))


# ================================================================================================= profile machinery
def shell_kernel(Rv, e):
    """Delta Sigma [Msun/pc^2] at projected radii Rv [Mpc] per 1e12 Msun in each uniform-density shell (e[k], e[k+1])."""
    r1, r2 = e[:-1], e[1:]
    Rv = np.atleast_1d(Rv)[:, None]; rho = 1.0 / ((4 * np.pi / 3) * (r2 ** 3 - r1 ** 3))
    p = lambda x: np.clip(x, 0.0, None)
    Sig = 2 * rho * (np.sqrt(p(r2 ** 2 - Rv ** 2)) - np.sqrt(p(r1 ** 2 - Rv ** 2)))
    Mcyl = 1.0 - (4 * np.pi / 3) * rho * (p(r2 ** 2 - Rv ** 2) ** 1.5 - p(r1 ** 2 - Rv ** 2) ** 1.5)
    return Mcyl / (np.pi * Rv ** 2) - Sig


EC = np.concatenate([[0.0], np.geomspace(0.03, 10.0, 26)])                        # free profile: a core + 25 shells
EF = np.concatenate([[0.0], np.geomspace(0.004, 40.0, 200)])                      # parametric profiles
KC, KF = shell_kernel(RD, EC), shell_kernel(RD, EF)


def frac_in(R, e):
    return np.clip((R ** 3 - e[:-1] ** 3) / (e[1:] ** 3 - e[:-1] ** 3), 0.0, 1.0)


def shells_of(Mcum, e=EF):
    """shell masses [1e12 Msun] of a cumulative profile Mcum(r) (the central galaxy sits in the core shell)."""
    return np.diff(np.concatenate([[0.0], Mcum(e[1:])]))


def COEF_T(lc=0.0):
    return COEF_SI * 10 ** lc


def target_exc(R, lc=0.0, lsz=0.0):
    """the lensing excess mass [1e12 Msun] whose shell turns around at R today (eq. 4 minus the mean; epoch/h factor)."""
    return (COEF_T(lc) * R ** 3 - RHO0 * 4 * np.pi / 3 * R ** 3) / 10 ** lsz


def R0_of(Mcum, lc=0.0, lsz=0.0, lo=0.05, hi=12.0):
    """the zero-velocity radius of a static Lagrangian profile: the OUTERMOST R with 10^lsz M_exc(<R) + mean = COEF R^3."""
    Rg = np.geomspace(lo, hi, 500); f = Mcum(Rg) - target_exc(Rg, lc, lsz)
    idx = np.where((f[:-1] > 0) & (f[1:] <= 0))[0]
    if len(idx) == 0:
        return float("nan") if f[0] <= 0 else hi
    j = idx[-1]
    return float(brentq(lambda R: float(Mcum(np.array([R]))[0] - target_exc(R, lc, lsz)), Rg[j], Rg[j + 1], xtol=1e-6))


def bin_coeffs(logM):
    c = np.zeros(4); x = min(max(logM, B21_MGAL[0]), B21_MGAL[-1])
    j = int(min(max(np.searchsorted(B21_MGAL, x) - 1, 0), 2)); w = (x - B21_MGAL[j]) / (B21_MGAL[j + 1] - B21_MGAL[j])
    c[j] = 1 - w; c[j + 1] = w
    return c


def kids_for(targets, dM=0.0):
    """the KiDS profile for a system: a linear combination of the four bins (companion-weighted targets), and its covariance."""
    cv = sum(w * bin_coeffs(lm + dM) for lm, w in targets)
    d = sum(cv[b] * KE[b] for b in range(4))
    C = sum(cv[b] * cv[bb] * C60[b * 15:(b + 1) * 15, bb * 15:(bb + 1) * 15] for b in range(4) for bb in range(4))
    return d, C, cv


def mgal_of(cv):
    return float(np.log10(sum(cv[b] * 10 ** B21_MGAL[b] for b in range(4))))


def factors(t_in=1.0, t_out=1.0, ell=1.0):
    return np.where(RD > B21_R_ISO, t_out * ell, t_in)


def whit(C, idx):
    return np.linalg.inv(np.linalg.cholesky(C[np.ix_(idx, idx)]))


def bvls(A, y):
    return lsq_linear(A, y, bounds=(0, np.inf), method="bvls", tol=1e-12, max_iter=5000).x


def qp_full(A, y, Rt, lc, lsz, m_start):
    """min |A m - y|^2, m >= 0, M(<Rt) = target(Rt), M(<R) <= target(R) for R > Rt (Rt the OUTERMOST crossing)."""
    fi = frac_in(Rt, EC); Mt = target_exc(Rt, lc, lsz)
    Ro = np.array(sorted(set([R for R in EC[1:] if R > Rt * 1.001] + [Rt * f_ for f_ in (1.03, 1.08, 1.15, 1.3, 1.5)])))
    Fo = np.array([frac_in(R, EC) for R in Ro]); Uo = np.array([target_exc(R, lc, lsz) for R in Ro])
    x0 = np.clip(m_start, 0, None).copy(); s = fi @ x0
    if s > 0:
        x0 = x0 * min(1.0, Mt / s)
    r = minimize(lambda m: 0.5 * float(np.sum((A @ m - y) ** 2)), x0, jac=lambda m: A.T @ (A @ m - y), method="SLSQP",
                 bounds=[(0, None)] * len(x0), options=dict(maxiter=600, ftol=1e-12),
                 constraints=[dict(type="eq", fun=lambda m: fi @ m - Mt, jac=lambda m: fi),
                              dict(type="ineq", fun=lambda m: Uo - Fo @ m, jac=lambda m: -Fo)])
    m = np.clip(r.x, 0, None)
    viol = max(abs(fi @ m - Mt) / Mt, float(np.max(np.clip(Fo @ m - Uo, 0, None) / Uo)) if len(Uo) else 0.0)
    return float(np.sum((A @ m - y) ** 2)), m, viol


def T_free(d, C, R0, sR, lc=0.0, lsz=0.0, mask=None, full=False, Rkern=None, detail=False):
    """the family-agnostic joint statistic for one system: min_{m >= 0, R0_t} [chi2_K(m) + ((R0_t - R0)/sR)^2] - min chi2_K."""
    idx = np.arange(15) if mask is None else np.where(mask)[0]
    K = KC if Rkern is None else shell_kernel(Rkern, EC)
    W = whit(C, idx); A = W @ K[idx]; y = W @ d[idx]
    m0 = bvls(A, y); c0 = float(np.sum((A @ m0 - y) ** 2))

    def relaxed(Rt):
        f = frac_in(Rt, EC); Mt = target_exc(Rt, lc, lsz)
        if f @ m0 <= Mt:
            return c0, m0
        m = bvls(np.vstack([A, 1e3 * f / Mt]), np.concatenate([y, [1e3]]))
        return float(np.sum((A @ m - y) ** 2)), m
    grid = np.geomspace(max(0.3, R0 - 4 * sR) * 0.9, max(R0 + 6 * sR, 1.2 * R0) * 1.6, 44)
    rel = [(c - c0 + ((Rt - R0) / sR) ** 2, Rt, c - c0, m) for Rt in grid for c, m in [relaxed(Rt)]]
    j = int(np.argmin([r_[0] for r_ in rel])); Tr, Rtr, dkr, mr = rel[j]
    out = dict(T=Tr, R0t=Rtr, dK=dkr, c0=c0, m=mr, relaxed=True)
    if full:
        cache = {}

        def ffull(Rt):
            c, m, v = qp_full(A, y, Rt, lc, lsz, relaxed(Rt)[1]); cache[Rt] = (c, m, v)
            return c - c0 + ((Rt - R0) / sR) ** 2
        pts = np.unique(np.concatenate([grid[::4], np.geomspace(grid[max(j - 3, 0)], grid[min(j + 8, len(grid) - 1)], 9)]))
        vals = [ffull(Rt) for Rt in pts]; k = int(np.argmin(vals))
        a_, b_ = pts[max(k - 1, 0)], pts[min(k + 1, len(pts) - 1)]
        rr = minimize_scalar(ffull, bounds=(a_, b_), method="bounded", options=dict(xatol=2e-3))
        Tf, Rtf = (rr.fun, rr.x) if rr.fun < vals[k] else (vals[k], pts[k])
        c, m, v = cache.get(Rtf, qp_full(A, y, Rtf, lc, lsz, relaxed(Rtf)[1]))
        out.update(T=max(Tf, Tr), R0t=Rtf, dK=c - c0, m=m, relaxed=False, T_relaxed=Tr, viol=v)
    if detail:
        out["Mcum"] = lambda R, m_=out["m"]: np.array([frac_in(x, EC) @ m_ for x in np.atleast_1d(R)])
    return out


# ================================================================================================= parametric families
def nfw_Mcum(M200, c, Mgal):
    r200 = (3 * M200 / (4 * np.pi * 200 * RHOC_Z)) ** (1 / 3); rs = r200 / c; mc = math.log(1 + c) - c / (1 + c)
    return lambda r: Mgal + M200 * (np.log(1 + np.asarray(r) / rs) - (np.asarray(r) / rs) / (1 + np.asarray(r) / rs)) / mc


def nfw_ds(R, M200, c):
    """Wright & Brainerd (2000) NFW Delta Sigma [Msun/pc^2]; M200 [1e12 Msun] w.r.t. 200 rho_crit(z = 0.25)."""
    r200 = (3 * M200 / (4 * np.pi * 200 * RHOC_Z)) ** (1 / 3); rs = r200 / c
    dc = (200 / 3.) * c ** 3 / (math.log(1 + c) - c / (1 + c)); x = np.asarray(R, float) / rs; g = np.empty_like(x)
    for i, xi in enumerate(x):
        if xi < 1 - 1e-6:
            at = np.arctanh(math.sqrt((1 - xi) / (1 + xi)))
            g[i] = 8 * at / (xi ** 2 * math.sqrt(1 - xi ** 2)) + 4 / xi ** 2 * math.log(xi / 2) - 2 / (xi ** 2 - 1) + 4 * at / ((xi ** 2 - 1) * math.sqrt(1 - xi ** 2))
        elif xi < 1 + 1e-6:
            g[i] = 10 / 3. + 4 * math.log(0.5)
        else:
            at = np.arctan(math.sqrt((xi - 1) / (1 + xi)))
            g[i] = 8 * at / (xi ** 2 * math.sqrt(xi ** 2 - 1)) + 4 / xi ** 2 * math.log(xi / 2) - 2 / (xi ** 2 - 1) + 4 * at / ((xi ** 2 - 1) ** 1.5)
    return rs * dc * RHOC_Z * g


# ---- LCDM's two-halo term (B21's WMAP9; hunt_2026/h113's construction: EH98 no-wiggle, linear xi, Tinker+10 bias)
def _T_nw(k):
    h = H70; kh = k / h; th = 2.7255 / 2.7; Omh2 = OM_W9 * h * h; Obh2 = OB_W9 * h * h; fb = OB_W9 / OM_W9
    s = 44.5 * np.log(9.83 / Omh2) / np.sqrt(1 + 10 * Obh2 ** 0.75)
    al = 1 - 0.328 * np.log(431 * Omh2) * fb + 0.38 * np.log(22.3 * Omh2) * fb ** 2
    Gam = OM_W9 * h * (al + (1 - al) / (1 + (0.43 * kh * s) ** 4)); q = kh * th ** 2 / Gam
    L_ = np.log(2 * np.e + 1.8 * q); Cc = 14.2 + 731.0 / (1 + 62.5 * q)
    return L_ / (L_ + Cc * q * q)


_LK = np.linspace(math.log(1e-5), math.log(3e2), 5000); _KK = np.exp(_LK); _P0 = _KK ** NS_W9 * _T_nw(_KK) ** 2


def _sig(Rr, norm):
    x = _KK * Rr; Wt = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return math.sqrt(norm * np.trapz(_KK ** 3 * _P0 * Wt ** 2 / (2 * np.pi ** 2), _LK))


_NORM = (S8_W9 / _sig(8.0 / H70, 1.0)) ** 2


def _growth(z):
    f = lambda a: (OM_W9 / a + (1 - OM_W9) * a ** 2) ** -1.5
    a = 1 / (1 + z); g = np.linspace(1e-5, a, 4000); g1 = np.linspace(1e-5, 1.0, 4000)
    return (math.sqrt(OM_W9 / a ** 3 + 1 - OM_W9) * np.trapz(f(g), g)) / np.trapz(f(g1), g1)


_DZ = _growth(B21_Z)
_kk = np.exp(np.linspace(math.log(1e-4), math.log(1e2), 3000)); _Pk = _NORM * _kk ** NS_W9 * _T_nw(_kk) ** 2 * _DZ ** 2 * np.exp(-(_kk / 40.) ** 2)
_RXI = np.geomspace(1e-3, 200.0, 400)                                             # comoving [Mpc]
_XI = np.array([np.trapz(_kk ** 3 * _Pk * np.sinc(_kk * r / np.pi) / (2 * np.pi ** 2), np.log(_kk)) for r in _RXI])
RHOM0_COM = 2.775e11 * H70 ** 2 * OM_W9 / 1e12


def bias_tinker(M200):
    """Tinker+10 bias (Delta = 200), as hunt_2026/h113."""
    Rr = (3 * M200 * 1e12 / (4 * np.pi * RHOM0_COM * 1e12)) ** (1 / 3.); sM = _sig(Rr, _NORM) * _DZ
    y = math.log10(200.); dc = 1.686; nn = dc / sM
    A = 1.0 + 0.24 * y * math.exp(-(4 / y) ** 4); a = 0.44 * y - 0.88; Bb, bb = 0.183, 1.5
    Cc = 0.019 + 0.107 * y + 0.19 * math.exp(-(4 / y) ** 4); cc = 2.4
    return 1 - A * nn ** a / (nn ** a + dc ** a) + Bb * nn ** bb + Cc * nn ** cc


_RP2 = np.geomspace(1e-3, 60.0, 3000)                                             # proper [Mpc]
_M2H = np.concatenate([[0.0], np.cumsum(0.5 * np.diff(_RP2) * (4 * np.pi * _RP2[1:] ** 2 * np.interp(_RP2[1:] * (1 + B21_Z), _RXI, _XI)
                                                              + 4 * np.pi * _RP2[:-1] ** 2 * np.interp(_RP2[:-1] * (1 + B21_Z), _RXI, _XI)))]) * RHOM_Z


def m2h_cum(r, b):
    """the two-halo excess mass inside proper r [1e12 Msun]: b rho_m(z) int 4 pi r^2 xi_lin(r (1 + z)) dr."""
    return b * np.interp(np.asarray(r), _RP2, _M2H)


def duffy_c(M200):
    return 5.71 * (M200 * 1e12 * H70 / 2e12) ** -0.084 * (1 + B21_Z) ** -0.47


# ---- the chain's baryons + phantom (FP9's (H_Y) at z = 0.25; FP6's phantom), with a free outer cut
_PH_CACHE = {}


def chain_Mcum(Mb12, f_out, rc):
    key = round(math.log10(Mb12), 6)
    if key not in _PH_CACHE:
        ph = M6["phantom"](Mb12 * 1e12 * LGM, A0C, F11.HEAD["L25"] * F11.MPC, F11.HEAD["y25"], F11.YIELD) / LGM / 1e12
        _PH_CACHE[key] = np.maximum(ph, 0.0)
    ph = _PH_CACHE[key]; rg = M6["RG"] / F11.MPC

    def M(r):
        r = np.asarray(r, float)
        fr = f_out + (1 - f_out) / (1 + (r / rc) ** 4)
        return Mb12 + fr * np.interp(np.log(np.maximum(r, rg[0])), np.log(rg), ph)
    return M


# ---- free piecewise power law (B21 App. B's PPL form): log rho linear in log r between six nodes
PPL_NODES = np.array([0.02, 0.06, 0.2, 0.6, 2.0, 6.0])
_RPPL = np.geomspace(1e-3, 30.0, 1500)


def ppl_Mcum(lrho, Mgal):
    lr = np.log(PPL_NODES); lx = np.log(_RPPL)
    sl0 = (lrho[1] - lrho[0]) / (lr[1] - lr[0]); sl1 = (lrho[-1] - lrho[-2]) / (lr[-1] - lr[-2])
    lrho_x = np.interp(lx, lr, lrho)
    lrho_x = np.where(lx < lr[0], lrho[0] + min(sl0, 0.0) * (lx - lr[0]), lrho_x)
    lrho_x = np.where(lx > lr[-1], lrho[-1] + min(sl1, -1.5) * (lx - lr[-1]), lrho_x)
    rho = np.exp(lrho_x); dm = 4 * np.pi * _RPPL ** 3 * rho                        # d M / d ln r
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(lx))]) + 4 * np.pi / 3 * _RPPL[0] ** 3 * rho[0]
    return lambda r: Mgal + np.interp(np.asarray(r, float), _RPPL, cum)


def esd_of(Mcum):
    return KF @ shells_of(Mcum)


# ================================================================================================= reporting
CH = []
OUT = {"lane": "FP18", "mutate": MUTATE, "R0_shift_dex": R0_SHIFT, "checks": {}, "numbers": {}, "ledger": []}
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


def sig_of(T, dof):
    p = float(chi2_dist.sf(max(T, 0.0), dof))
    return p, (float(-norm_dist.ppf(p / 2)) if p > 0 else float("inf"))


# ================================================================================================= fits (families)
def chi2_K(model, d, Ci):
    r = d - model
    return float(r @ Ci @ r)


def fit_family(fam, d, C, Mgal12, R0=None, sR=None, lc=0.0, lsz=0.0):
    """best fit of a family to KiDS alone (R0 = None) or jointly with R0; returns dict(chiK, R0p, chiR, tot, p)."""
    Ci = np.linalg.inv(C)

    def build(p):
        if fam == "NFW":
            M200, c = 10 ** p[0], 10 ** p[1]
            if not (0.3 < c < 40): return None, None
            return nfw_ds(RD, M200, c) + Mgal12 / (np.pi * RD ** 2), nfw_Mcum(M200, c, Mgal12)
        if fam == "NFW+2h":
            M200 = 10 ** p[0]; c = duffy_c(M200); b = bias_tinker(M200); Mn = nfw_Mcum(M200, c, Mgal12)
            M = lambda r, Mn=Mn, b=b: Mn(r) + m2h_cum(r, b)
            return esd_of(M), M
        if fam == "TIS":
            V, rt = 10 ** p[0], 10 ** p[1]
            if not (0.005 < rt < 30): return None, None
            M = lambda r, V=V, rt=rt: Mgal12 + V ** 2 / (G_KMS * 1e12) * np.minimum(np.asarray(r, float), rt)
            return esd_of(M), M
        if fam == "chain+cut":
            Mb, fo, rc = 10 ** p[0], p[1], 10 ** p[2]
            if not (0.0 <= fo <= 1.5 and 0.05 < rc < 5.0 and 9.5 < p[0] + 12 < 12.0): return None, None
            M = chain_Mcum(Mb, fo, rc)
            return esd_of(M), M
        if fam == "PPL":
            M = ppl_Mcum(np.asarray(p), Mgal12)
            return esd_of(M), M
        raise ValueError(fam)

    def obj(p):
        mod, M = build(p)
        if mod is None: return 1e9
        c = chi2_K(mod, d, Ci)
        if R0 is None: return c
        R0p = R0_of(M, lc, lsz)
        return c + ((R0p - R0) / sR) ** 2 if R0p == R0p else 1e9
    starts = {"NFW": [[math.log10(x), math.log10(y)] for x in (1.0, 3.0, 8.0) for y in (1.5, 4.0)],
              "NFW+2h": [[math.log10(x)] for x in (0.5, 1.5, 4.0)],
              "TIS": [[math.log10(x), math.log10(y)] for x in (120.0, 180.0, 250.0) for y in (0.3, 1.0, 3.0)],
              "chain+cut": [[math.log10(x), fo, math.log10(rc)] for x in (0.06, 0.15) for fo in (1.0, 0.4) for rc in (0.3, 1.0)],
              "PPL": [list(np.log(np.array([1850.0, 205.0, 18.5, 2.06, 0.185, 0.021]) * s_)) for s_ in (0.3, 1.0, 3.0)]}[fam]
    best = None
    for x0 in starts:
        r = minimize(obj, x0, method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-4, maxiter=4000 if fam == "PPL" else 1500))
        if best is None or r.fun < best.fun:
            best = r
    r = minimize(obj, best.x, method="Nelder-Mead", options=dict(xatol=1e-5, fatol=1e-6, maxiter=4000))
    p = r.x if r.fun <= best.fun else best.x
    mod, M = build(p); cK = chi2_K(mod, d, Ci); R0p = R0_of(M, lc, lsz)
    return dict(p=[float(x) for x in p], chiK=cK, R0p=R0p, chiR=((R0p - R0) / sR) ** 2 if R0 is not None else None,
                tot=cK + (((R0p - R0) / sR) ** 2 if R0 is not None else 0.0), M=M, npar=len(p))


# ================================================================================================= main
def main():
    global COEF_SI
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P(f"\n  *** MUTATE=1: every published R0 is shifted by +{R0_SHIFT} dex (the face-value offset); V1 must FAIL, the verdict must turn COMPATIBLE ***")

    # ============================================================================================= K controls
    banner("K  CONTROLS: the covariance, the projection, the infall relation, K&K's fit, the chain's phantom, the lens sample, the bound")
    ev_g = np.linalg.eigvalsh((C60 + C60.T) / 2); ev_p = np.linalg.eigvalsh((C60_PLAIN + C60_PLAIN.T) / 2)
    dg = float(np.max(np.abs(np.sqrt(np.diag(C60)) / KS.ravel() - 1)))
    check("K1 CONTROL: the Fig-3 covariance in its (m,n,i,j) order is positive definite with diagonal = the published errors^2; "
          "the plain reshape is indefinite (the record's corrected bug, exhibited)",
          f"corrected: min eigenvalue {ev_g.min():+.3e}, max |sqrt(diag)/error - 1| = {dg:.1e}; plain reshape: min eigenvalue {ev_p.min():+.3e}",
          ev_g.min() > 0 and dg < 1e-3 and ev_p.min() < 0)
    # K2 projection
    dev = []
    for M200, c in ((0.5, 8.0), (3.0, 4.0), (10.0, 2.0)):
        a_ = nfw_ds(RD, M200, c); s_ = esd_of(nfw_Mcum(M200, c, 0.0)); dev.append(float(np.max(np.abs(s_ / a_ - 1))))
    ksis = 200.0 ** 2 / (G_KMS * 1e12)                                           # SIS, V = 200 km/s: Delta Sigma = V^2 / (4 G R)
    dsis = float(np.max(np.abs(esd_of(lambda r: ksis * np.minimum(np.asarray(r, float), 30.0)) / (ksis / (4 * RD)) - 1)))
    check("K2 CONTROL: this lane's uniform-shell projection reproduces the analytic NFW Delta Sigma (Wright & Brainerd 2000) and the "
          "singular isothermal sphere's V^2/(4 G R) at the 15 KiDS radii", f"NFW (M200 0.5/3/10e12, c 8/4/2): max dev {max(dev):.2e}; "
          f"SIS: max dev {dsis:.2e}", max(dev) < 0.01 and dsis < 0.01)
    RR, esd6 = M6["RR"], M6["esd_of_M"]
    Rq, dS = esd6(ksis * np.minimum(RR / F11.MPC, 30.0) * 1e12 * LGM, 0.0)
    b6 = np.interp(RD, Rq, dS) / (ksis / (4 * RD)) - 1
    check("K2b (reported) SIDE FINDING: FP6's committed esd_of_M (L341 F7's 'lead grade' Abel matrix, used by FP6/FP9/FP12's KiDS gates) "
          "UNDER-projects: on the same SIS it is low by tens of per cent inside 0.1 Mpc and by ~5-14% at 0.3-2.6 Mpc (a trapezoid over "
          "the Abel singularity plus the inner-mass approximation); this lane does not use it",
          ", ".join(f"R {R:.2f}: {v:+.1%}" for R, v in zip(RD[::2], b6[::2])), float(np.min(b6)) < -0.03, load_bearing=False)
    # K3 infall relation
    cf = [M / M6["lg_R0"](lambda r, a, M=M: M * 1e12 * LGM + 0.0 * r) ** 3 for M in (0.5, 1.57, 5.0)]
    COEF_SI = float(np.mean(cf))
    check("K3 CONTROL: the spherical-infall relation with Lambda -- the record's shell integrator (FP6 lg_R0: point mass + Lambda, "
          "Planck 2018, shells from the Hubble flow at a = 0.02) gives M/R0^3 equal to K&K 2018 eq. (4)'s 1.95e12 Msun/Mpc^3",
          f"M/R0^3 = {', '.join(f'{x:.4f}' for x in cf)} e12 (exactly self-similar); K&K eq. (4) 1.95 (Planck), 2.12 (WMAP); "
          f"deviation {COEF_SI / KK_COEF - 1:+.2%}", abs(COEF_SI / KK_COEF - 1) < 0.01 and np.ptp(cf) / COEF_SI < 1e-3)
    # K4 K&K's stack fit from Table 7
    Rc7 = np.array([float(r_[2]) for r_ in T7]); V7 = np.array([float(r_[3]) for r_ in T7])
    eq14 = lambda p, R: p[0] * R - p[0] * p[1] * np.sqrt(p[1] / R)
    s7 = least_squares(lambda p: eq14(p, Rc7) - V7, [80.0, 1.0]); sig7 = float(np.sqrt(np.sum((eq14(s7.x, Rc7) - V7) ** 2) / (len(V7) - 2)))
    rng = np.random.default_rng(RNG_SEED)
    mc = np.array([least_squares(lambda p, Rp=Rc7 * (1 + 0.05 * rng.standard_normal(len(Rc7))): eq14(p, Rp) - V7, [80.0, 1.0]).x
                   for _ in range(600)])
    bs = []
    for _ in range(1500):
        i_ = rng.integers(0, len(Rc7), len(Rc7)); bs.append(least_squares(lambda p: eq14(p, Rc7[i_]) - V7[i_], [80.0, 1.0]).x)
    bs = np.array(bs)
    fp12form = lambda p, R: p[0] * R * (1 - np.sqrt(abs(p[1]) / R))
    s12 = least_squares(lambda p: fp12form(p, Rc7) - V7, [80.0, 1.0])
    k4 = (abs(mc[:, 1].mean() - KK_STACK["R0"]) < 0.03 and mc[:, 1].std() < 0.035 and abs(mc[:, 0].mean() - KK_STACK["H0"]) < 3.0
          and abs(sig7 - KK_STACK["sig"]) < 4.0 and len(T7) == 66)
    check("K4 CONTROL: the transcribed K&K 2018 Table 7 (66 companions, barycentre frame, minor attractor) reproduces their stack "
          "fit with their eq. (14), V = H0 R - H0 R0 (R0/R)^(1/2), free H0, errors from their 5%-distance Monte Carlo",
          f"R0 = {s7.x[1]:.3f} (MC {mc[:, 1].mean():.3f} +- {mc[:, 1].std():.3f}), H0 = {s7.x[0]:.1f} (MC {mc[:, 0].mean():.1f} +- "
          f"{mc[:, 0].std():.1f}), sigma_v = {sig7:.1f} km/s vs published 0.93 +- 0.02, 85 +- 2, 57", k4)
    # K5 chain phantom = FP9's
    kb = M6["kids_class"](A0C); kc = M6["kids_class"](A0C, F11.HEAD["L25"], F11.HEAD["y25"], F11.YIELD) - kb
    ref = json.load(open(os.path.join(HERE, "FP12_local_volume_groups_r0_results.json")))["numbers"]["U"]["kids_f"]["canonical/1.0"]
    check("K5 CONTROL: the chain-shaped family uses FP9's (H_Y) phantom at z = 0.25 -- FP6's kids_class with FP9's constants "
          "reproduces FP9/FP12's committed KiDS lead grade", f"{kc:+.4f} vs FP12 {ref:+.4f} (canonical)", abs(kc - ref) < 1e-6)
    # K6 lens reconstruction
    lr = np.load(os.path.join(REPO, "real_research", "data", "lensing_rar", "lr_lenses.npz"))
    FRED, mg6 = [], []
    for i in range(4):
        s_ = (lr["logM"] >= (8.5, 10.3, 10.6, 10.8, 11.0)[i]) & (lr["logM"] < (8.5, 10.3, 10.6, 10.8, 11.0)[i + 1])
        FRED.append(float(np.mean(lr["typ"][s_] == 1))); mg6.append(float(np.log10(np.mean(lr["Mgal"][s_]))))
    dk6 = float(np.max(np.abs(np.array(mg6) - B21_MGAL)))
    check("K6 CONTROL: the record's reconstruction of B21's isolated lenses (lr_lenses.npz; its own isolation window and colour "
          "split) reproduces B21's four bin mean masses -- so its per-bin red fractions can price the galaxy-type systematic",
          f"log <M_gal> {', '.join(f'{x:.3f}' for x in mg6)} vs B21 {', '.join(f'{x:.2f}' for x in B21_MGAL)} (max dev {dk6:.3f}); "
          f"red fractions {', '.join(f'{x:.2f}' for x in FRED)}", dk6 <= 0.02, load_bearing=False)
    # K7 the bound
    rng2 = np.random.default_rng(RNG_SEED + 1); worst = -np.inf
    for _ in range(2000):
        m = rng2.exponential(1.0, len(EF) - 1) * (rng2.random(len(EF) - 1) < rng2.uniform(0.05, 0.9))
        ds = KF @ m; Min = np.array([frac_in(R, EF) @ m for R in RD]); worst = max(worst, float(np.max(ds * np.pi * RD ** 2 - Min)))
    void = np.zeros(len(EF) - 1); sel = EF[:-1] >= 1.0364
    void[sel] = -RHOM_Z * (4 * np.pi / 3) * (EF[1:][sel] ** 3 - EF[:-1][sel] ** 3) * (EF[1:][sel] < 20)
    dv = float((KF @ void)[np.argmin(np.abs(RD - 1.0365))])
    check("K7 CONTROL: the bound Delta Sigma(R) <= M(<R)/(pi R^2) holds for any non-negative spherical excess density (each shell "
          "outside R contributes -(M_s/pi R^2)(1-s)^2/(2s) <= 0, s = sqrt(1 - R^2/r_s^2)) -- 2000 random profiles; the most negative "
          "allowed outside (a complete void, excess = -rho_m, 1-20 Mpc) raises Delta Sigma(1.04 Mpc) by only",
          f"max[pi R^2 Delta Sigma - M(<R)] = {worst:+.2e} (1e12 Msun); void term {dv:+.3f} Msun/pc^2 (KiDS there: 1.3-3.2)",
          worst <= 1e-10 and 0 <= dv < 0.12)
    OUT["numbers"]["K"] = dict(eig_good=float(ev_g.min()), eig_plain=float(ev_p.min()), K2=dict(nfw=max(dev), sis=dsis, fp6_sis_bias=[float(x) for x in b6]), COEF_SI=COEF_SI, K4=dict(
        R0=float(s7.x[1]), H0=float(s7.x[0]), sig=sig7, mcR0=[float(mc[:, 1].mean()), float(mc[:, 1].std())]), K5=[kc, ref], K6=dict(
        mgal=mg6, fred=FRED), K7=[worst, dv])
    P(f"    {el()}")

    # ============================================================================================= E the R0 data and their errors
    banner("E  THE R0 DATA: the published estimator re-run on the published tables -- bootstrap vs quoted errors")
    Rc4 = np.array([float(r_[1]) for r_ in T4]); V4 = np.array([float(r_[2]) for r_ in T4]); MD4 = np.array([r_[4] for r_ in T4])
    m14 = np.isin(MD4, ["MWay", "M31"])
    s14 = least_squares(lambda p: eq14(p, Rc4[m14]) - V4[m14], [80.0, 1.0]); s35 = least_squares(lambda p: eq14(p, Rc4) - V4, [80.0, 1.0])
    b14, b35 = [], []
    ii14 = np.where(m14)[0]
    for _ in range(1500):
        i_ = rng.choice(ii14, len(ii14)); b14.append(least_squares(lambda p: eq14(p, Rc4[i_]) - V4[i_], [80.0, 1.0]).x[1])
        i_ = rng.integers(0, len(Rc4), len(Rc4)); b35.append(least_squares(lambda p: eq14(p, Rc4[i_]) - V4[i_], [80.0, 1.0]).x[1])
    sb7, sb14, sb35 = float(bs[:, 1].std()), float(np.std(b14)), float(np.std(b35))
    sig14 = float(np.sqrt(np.sum((eq14(s14.x, Rc4[m14]) - V4[m14]) ** 2) / (m14.sum() - 2)))
    sig35 = float(np.sqrt(np.sum((eq14(s35.x, Rc4) - V4) ** 2) / (len(V4) - 2)))
    SH = 10 ** R0_SHIFT
    HON = {"stack": math.hypot(sb7, KK_STACK["e"]), "LG": math.hypot(sb14, KK_LG["e"])}
    SYSTEMS = {  # key: (R0, sigma_quoted, sigma_honest, source)
        "stack": (KK_STACK["R0"] * SH, KK_STACK["e"] * SH, HON["stack"] * SH, "K&K 2018 stack (Table 7, BC minor)"),
        "LG": (KK_LG["R0"] * SH, KK_LG["e"] * SH, HON["LG"] * SH, "K&K 2018 LG (adopted)"),
        "LG_K09": (F12.MEAS["LG"][0][0] * SH, F12.MEAS["LG"][0][1] * SH, HON["LG"] * SH, "Karachentsev+2009"),
        "M81": (F12.MEAS["M81"][0][0] * SH, F12.MEAS["M81"][0][1] * SH, None, "Karachentsev & Kashibadze 2006"),
        "IC342": (F12.MEAS["IC342"][0][0] * SH, F12.MEAS["IC342"][0][1] * SH, None, "Karachentsev 2005 Tab.11"),
        "CenA": (F12.MEAS["CenA"][0][0] * SH, F12.MEAS["CenA"][0][1] * SH, None, "Karachentsev+2007"),
    }
    P(f"    stack (Table 7, 66): eq. 14 fit R0 {s7.x[1]:.3f}, H0 {s7.x[0]:.1f}, sigma_v {sig7:.1f}; bootstrap over companions "
      f"+-{sb7:.3f} (16-84: {np.percentile(bs[:, 1], 16):.3f}-{np.percentile(bs[:, 1], 84):.3f}); 5%-distance MC +-{mc[:, 1].std():.3f} (quoted +-0.02)")
    P(f"    LG (Table 4): 14 MW/M31-disturbed: R0 {s14.x[1]:.3f}, H0 {s14.x[0]:.1f}, sigma_v {sig14:.1f}, bootstrap +-{sb14:.3f} "
      f"(K&K quote 0.85 +- 0.03, H0 79, sigma 23); all 35: R0 {s35.x[1]:.3f}, H0 {s35.x[0]:.1f}, sigma_v {sig35:.1f}, bootstrap +-{sb35:.3f} "
      f"(K&K 0.95 +- 0.03, 90, 42); adopted 0.91 +- 0.05")
    P(f"    FP12's fit form V = H R [1 - (R0/R)^(1/2)] on the same Table 7: R0 {abs(s12.x[1]):.3f}, H {s12.x[0]:.0f} -- not K&K's eq. (14) "
      f"(which is V = H R [1 - (R0/R)^(3/2)]); FP12's R1/V5 'eq.14' numbers used it (non-load-bearing there)")
    P(f"    honest errors (bootstrap (+) quoted): stack +-{HON['stack']:.3f}, LG +-{HON['LG']:.3f} Mpc; M81 / IC 342 / Cen A: quoted only (no tables here)")
    for k_, (R0, sq, sh, src) in SYSTEMS.items():
        P(f"      {k_:7s} R0 = {R0:.3f}  quoted +-{sq:.3f}  honest {('+-%.3f' % sh) if sh else '   --'}   M_T(<R0) = {COEF_SI * R0 ** 3:.2f}e12   ({src})")
    check("E1 (reported) THE PUBLISHED R0 ERRORS OMIT THE VELOCITY SCATTER: K&K's quoted errors are reproduced by their distance-only "
          "Monte Carlo; the bootstrap over galaxies (the same estimator, the same tables) is 4-6x larger",
          f"stack: quoted 0.02, distance-MC {mc[:, 1].std():.3f}, bootstrap {sb7:.3f}; LG(14): quoted 0.03-0.05, bootstrap {sb14:.3f}; LG(35) "
          f"bootstrap {sb35:.3f}; FP12's fit form gives R0 {abs(s12.x[1]):.2f} on the stack (not eq. 14)", sb7 > 3 * KK_STACK["e"] and sb14 > 1.5 * KK_LG["e"], load_bearing=False,
          reading="the R0 values stand; their significance does not -- FP12's sigma for the LG / stack used the quoted errors")
    OUT["numbers"]["E"] = dict(stack=dict(R0=float(s7.x[1]), H0=float(s7.x[0]), sig=sig7, boot=sb7, mc=float(mc[:, 1].std())),
                               LG14=dict(R0=float(s14.x[1]), H0=float(s14.x[0]), sig=sig14, boot=sb14),
                               LG35=dict(R0=float(s35.x[1]), H0=float(s35.x[0]), sig=sig35, boot=sb35), honest=HON,
                               fp12_form_R0=float(abs(s12.x[1])), systems={k_: list(v[:3]) for k_, v in SYSTEMS.items()})
    P(f"    {el()}")

    # ============================================================================================= matching
    lu = math.log10(UPS_K); ntot = sum(n for *_, n in KK_T6)
    TARG = {"i": {}, "ii": {}}
    TARG["i"]["stack"] = [(bos(l1 + lu), n / ntot) for g, l1, l2, n in KK_T6 if n > 0]
    per = json.load(open(os.path.join(HERE, "FP12_local_volume_groups_r0_results.json")))["numbers"]["V"]["stack"]["canonical"]["per_group"]
    TARG["ii"]["stack"] = [(math.log10(per[g][0]), n / ntot) for g, l1, l2, n in KK_T6 if n > 0]
    cen = {"LG": 10.79, "LG_K09": 10.79, "M81": 10.95, "IC342": 10.86, "CenA": 10.89}      # K&K Table 6: M31, M81, Maffei 2, NGC 5128
    tot = {"LG": 1.145e11, "LG_K09": 1.145e11, "M81": F12.K02_OUT["M81"][2], "IC342": F12.K02_OUT["IC342"][2], "CenA": F12.K02_OUT["CenA"][2]}
    for k_ in cen:
        TARG["i"][k_] = [(bos(cen[k_] + lu), 1.0)]; TARG["ii"][k_] = [(math.log10(tot[k_]), 1.0)]
    FL = {"stack": sum(n for g, l1, l2, n in KK_T6 if g not in KK_EARLY) / ntot, "LG": 1.0, "LG_K09": 1.0, "M81": 1.0, "IC342": 1.0, "CenA": 0.0}
    # the type contrast (Fig. 8, colour split) and the late-type factors
    gb8, Eb, Sb = b21_profile("Fig-8_RAR-KiDS-isolated_Colorbin_1.txt"); _, Er, Sr = b21_profile("Fig-8_RAR-KiDS-isolated_Colorbin_2.txt")
    C8, _ = b21_cov("Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2, 15)

    def amp(E1, C1, E2, C2, C12, m):
        a = 1.0
        for _ in range(60):
            Cd = C1[np.ix_(m, m)] + a * a * C2[np.ix_(m, m)] - a * (C12[np.ix_(m, m)] + C12[np.ix_(m, m)].T)
            Ci = np.linalg.inv(Cd); x = E2[m]; yv = E1[m]; an = float(x @ Ci @ yv / (x @ Ci @ x))
            if abs(an - a) < 1e-9: break
            a = an
        return a, float(1 / math.sqrt(x @ Ci @ x))
    lo_g = gb8 < B21_GBAR_ISO
    DEL = {"in": amp(Eb, C8[:15, :15], Er, C8[15:, 15:], C8[:15, 15:], ~lo_g), "out": amp(Eb, C8[:15, :15], Er, C8[15:, 15:], C8[:15, 15:], lo_g)}

    def t_db(key, targets):
        cv = sum(w * bin_coeffs(lm) for lm, w in targets); fL = FL[key]; out = []
        for reg in ("in", "out"):
            dl = DEL[reg][0]
            out.append(sum(cv[b] * (fL * dl + (1 - fL)) / (FRED[b] + (1 - FRED[b]) * dl) for b in range(4)))
        return tuple(out)

    def t_extreme(key):
        return (DEL["in"][0], DEL["out"][0]) if FL[key] > 0.5 else (1.0, 1.0)
    OUT["numbers"]["matching"] = dict(targets={m_: {k_: v for k_, v in TARG[m_].items()} for m_ in TARG}, late_fraction=FL,
                                      delta_blue_red={k_: list(v) for k_, v in DEL.items()}, fred=FRED)
    banner("M  THE MATCHING: which KiDS lenses are the LV systems' analogs (the M* -> M_b mapping, gas, type)")
    gas_alt = []
    for (g, n1, l1, d1, n2, l2, d2, nc) in F12.KK18_T6:
        if nc == 0: continue
        i_ = F12.uidx(n1); hi_ = 1.33 * 10 ** F12.U_HI[i_] if (i_ is not None and np.isfinite(F12.U_HI[i_])) else 0.0
        gas_alt.append((g, bos(l1 + lu), math.log10(10 ** (l1 + lu) + hi_), nc))
    dgas = sum(nc * (a - b) for g, b, a, nc in gas_alt) / ntot
    for k_ in SYSTEMS:
        cvi, cvii = kids_for(TARG["i"][k_])[2], kids_for(TARG["ii"][k_])[2]
        P(f"    {k_:7s} mapping (i) central M_gal {mgal_of(cvi):.2f} (bins {', '.join(f'{c:.2f}' for c in cvi)}), (ii) group total "
          f"{mgal_of(cvii):.2f}; late-type fraction {FL[k_]:.2f}; t_db (R < / > 0.3 Mpc) {t_db(k_, TARG['i'][k_])[0]:.2f} / {t_db(k_, TARG['i'][k_])[1]:.2f}")
    P(f"    the stack's centrals, (i): " + ", ".join(f"{g} {b:.2f}" for g, b, a, nc in gas_alt) + f"; cold gas as B21 (Boselli) vs the UNGC's "
      f"1.33 M_HI: companion-weighted shift {dgas:+.3f} dex; Upsilon_K 0.5 / 1.0 instead of 0.6: {math.log10(0.5 / 0.6):+.3f} / {math.log10(1 / 0.6):+.3f} dex")
    P(f"    red fractions of B21-like isolated lenses per bin (K6): {', '.join(f'{x:.2f}' for x in FRED)}; B21's blue/red contrast (Fig. 8): "
      f"{DEL['in'][0]:.2f} (R < 0.3 Mpc), {DEL['out'][0]:.2f} (R > 0.3 Mpc)")
    OUT["numbers"]["matching"]["gas_shift_dex"] = dgas

    # ============================================================================================= B the bound
    banner("B  THE MODEL-INDEPENDENT BOUND: KiDS gives M(<R) >= pi R^2 Delta Sigma(R) for ANY non-negative spherical profile")
    P(f"    {'bin (log M_gal)':18s} " + " ".join(f"R={R:5.2f}" for R in RD[6:13]) + "   [1e12 Msun, +-1 sigma]")
    LB = {}
    for b in range(4):
        lbv = np.pi * RD ** 2 * KE[b]; le = np.pi * RD ** 2 * KS[b]; LB[b] = (lbv, le)
        P(f"    bin {b + 1} ({B21_MGAL[b]:.2f})      " + " ".join(f"{v:4.1f}+{e:3.1f}" for v, e in zip(lbv[6:13], le[6:13])))
    P("    the Hubble-flow systems: the TOTAL mass inside R0 (eq. 4) minus the mean = the most excess mass allowed inside R0:")
    for k_, (R0, sq, sh, src) in SYSTEMS.items():
        cvk = kids_for(TARG["i"][k_])[2]; lbk = sum(cvk[b] * LB[b][0] for b in range(4)); lek = np.sqrt(sum((cvk[b] * LB[b][1]) ** 2 for b in range(4)))
        inside = RD < R0; j = int(np.argmax(np.where(inside, (lbk - target_exc(R0)) / lek, -np.inf)))
        P(f"      {k_:7s} R0 {R0:.2f}: M_exc(<R0) <= {target_exc(R0):.2f}; KiDS at its M_gal {mgal_of(cvk):.2f} (mapping i) needs >= "
          f"{lbk[j]:.2f} +- {lek[j]:.2f} already inside R = {RD[j]:.2f} ({(lbk[j] - target_exc(R0)) / lek[j]:+.1f} sigma, one point)")
    b_stack = kids_for(TARG["i"]["stack"])[2]; lbs = sum(b_stack[b] * LB[b][0] for b in range(4))
    b1_ok = float(np.max(lbs[RD < SYSTEMS["stack"][0]])) > target_exc(SYSTEMS["stack"][0])
    check("B1 (reported) THE BOUND AGAINST THE FLOW: at face value KiDS's isolated lenses of the LV centrals' mass hold more excess mass "
          "inside ~0.5-0.8 Mpc than eq. (4) allows inside the whole R0 of the LV groups -- with no profile assumed",
          f"stack (M_gal {mgal_of(b_stack):.2f}): KiDS M(<0.56) >= {lbs[9]:.2f}, M(<0.76) >= {lbs[10]:.2f} vs <= {target_exc(SYSTEMS['stack'][0]):.2f} inside R0 = "
          f"{SYSTEMS['stack'][0]:.2f}; even bin 1 (M_gal 10.14): M(<0.76) >= {LB[0][0][10]:.2f} +- {LB[0][1][10]:.2f}", b1_ok, load_bearing=False)
    OUT["numbers"]["B"] = {f"bin{b + 1}": [list(LB[b][0]), list(LB[b][1])] for b in range(4)}
    P(f"    {el()}")

    # ============================================================================================= F1 free profile per system
    banner("F1  THE FREE PROFILE (any non-negative spherical density): the minimum joint penalty T, system by system")
    NOM = {}
    P(f"    {'system':8s} {'map':3s} {'R0':>5s} | {'T quoted (relaxed/full)':>24s} | {'T honest (relaxed/full)':>24s} | {'R0 the fit moves to':>20s} | KiDS M_gal")
    for k_ in ("stack", "LG", "LG_K09", "M81", "IC342", "CenA"):
        R0, sq, sh, src = SYSTEMS[k_]
        for mp in ("i", "ii"):
            d, C, cv = kids_for(TARG[mp][k_])
            tq = T_free(d, C, R0, sq, full=(mp == "i")); th = T_free(d, C, R0, sh, full=(mp == "i")) if sh else None
            NOM[(k_, mp)] = dict(q=tq, h=th)
            fmt = lambda o: (f"{o.get('T_relaxed', o['T']):9.1f} / " + (f"{o['T']:9.1f}" if not o["relaxed"] else f"{'--':>9s}")) if o else f"{'--':>21s}"
            P(f"    {k_:8s} {mp:3s} {R0:5.2f} | {fmt(tq)}   | {fmt(th)}   | {tq['R0t']:6.2f} / " + (f"{th['R0t']:5.2f}" if th else f"{'--':>5s}")
              + f"     | {mgal_of(cv):.2f}")
    Tj_nom = NOM[("stack", "i")]["h"]["T"] + NOM[("LG", "i")]["h"]["T"]
    check("F1 (reported) THE FREE PROFILE, SYSTEM BY SYSTEM: the least joint penalty any non-negative spherical profile pays for the "
          "KiDS profile of the system's central mass and its R0 (face value: no comparability systematics)",
          "; ".join(f"{k_}: {NOM[(k_, 'i')]['q']['T']:.0f} (quoted) / " + (f"{NOM[(k_, 'i')]['h']['T']:.0f} (honest)" if NOM[(k_, 'i')]['h'] else "--")
                    for k_ in ("stack", "LG", "LG_K09", "M81", "IC342", "CenA")) + f"; primary joint (stack + LG, honest) {Tj_nom:.1f}",
          True, load_bearing=False)
    OUT["numbers"]["F1"] = {f"{k_}/{mp}": dict(quoted=dict(T=v["q"]["T"], R0t=v["q"]["R0t"], T_relaxed=v["q"].get("T_relaxed")),
                                              honest=(dict(T=v["h"]["T"], R0t=v["h"]["R0t"], T_relaxed=v["h"].get("T_relaxed")) if v["h"] else None))
                           for (k_, mp), v in NOM.items()}
    P(f"    {el()}")

    # ============================================================================================= S systematics
    banner("S  THE COMPARABILITY SYSTEMATICS: one at a time, profiled under their priors, the extreme corner, the variants")
    PRI = dict(lt=0.08, ll=math.log10(B21_LEAK), dM=B21_MSYS, lr0=0.05, lc=0.04, lsz=0.045)

    def T_sys(key, p, sig_key="h", mapping="i", full=False, mask=None, infl=1.0, Rk=None, dscale=1.0):
        """one system's T at nuisances p = (lt, ll, dM, lr0, lc, lsz), without the prior penalty."""
        lt, ll, dM, lr0, lc, lsz = p; ll = min(ll, 0.0)
        R0, sq, sh, _ = SYSTEMS[key]; sR = sh if (sig_key == "h" and sh) else sq
        d, C, cv = kids_for(TARG[mapping][key], dM)
        ti, to = t_db(key, TARG[mapping][key])
        f = factors(ti * 10 ** lt, to * 10 ** lt, 10 ** ll) * dscale
        d, C = d * f, C * np.outer(f, f) * infl ** 2
        return T_free(d, C, R0 * 10 ** lr0, sR * 10 ** lr0, lc=lc, lsz=lsz, mask=mask, full=full, Rkern=Rk)["T"]

    def pen(p):
        lt, ll, dM, lr0, lc, lsz = p
        return (lt / PRI["lt"]) ** 2 + (min(ll, 0.0) / PRI["ll"]) ** 2 + (dM / PRI["dM"]) ** 2 + (lr0 / PRI["lr0"]) ** 2 + (lc / PRI["lc"]) ** 2 + (lsz / PRI["lsz"]) ** 2

    def T_nom_db(key, **kw):                                                     # the data-based type factor alone (the nuisances' centre)
        return T_sys(key, [0.0] * 6, **kw)

    def profile(keys, full=False, infl=None, mask=None, maxiter=500):
        infl = infl or {k_: 1.0 for k_ in keys}
        f = lambda p: sum(T_sys(k_, p, full=False, infl=infl[k_], mask=mask) for k_ in keys) + pen(p)
        best = None
        for x0 in ([-0.05, -0.05, -0.15, 0.04, 0.02, -0.02], [0.0, -0.1, -0.3, 0.07, 0.02, -0.02], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
            r = minimize(f, x0, method="Nelder-Mead", options=dict(xatol=2e-3, fatol=1e-2, maxiter=maxiter))
            if best is None or r.fun < best.fun: best = r
        out = dict(T_relaxed=float(best.fun), x=[float(v) for v in best.x], pen=float(pen(best.x)))
        if full:
            g = lambda p: sum(T_sys(k_, p, full=True, infl=infl[k_], mask=mask) for k_ in keys) + pen(p)
            v0 = g(best.x)
            r = minimize(g, best.x, method="Nelder-Mead", options=dict(xatol=3e-3, fatol=2e-2, maxiter=90, initial_simplex=np.array(
                [best.x] + [np.array(best.x) + np.eye(6)[i] * [0.03, 0.04, 0.08, 0.02, 0.02, 0.02][i] for i in range(6)])))
            out.update(T=float(min(v0, r.fun)), x=[float(v) for v in (r.x if r.fun < v0 else best.x)], T_at_relaxed_opt=float(v0))
            out["pen"] = float(pen(out["x"]))
        else:
            out["T"] = out["T_relaxed"]
        out["parts"] = {k_: float(T_sys(k_, out["x"], full=full, infl=infl[k_], mask=mask)) for k_ in keys}
        return out

    # the KiDS covariance inflation: sqrt(chi2/dof) of the NFW (LCDM one-halo) fit to each system's profile
    INFL = {}
    for k_ in SYSTEMS:
        d, C, cv = kids_for(TARG["i"][k_]); fr = fit_family("NFW", d, C, 10 ** mgal_of(cv) / 1e12)
        INFL[k_] = math.sqrt(max(1.0, fr["chiK"] / 13.0))
    P("    covariance inflation sqrt(chi2_NFW / 13): " + ", ".join(f"{k_} {v:.2f}" for k_, v in INFL.items()))
    P(f"    type contrast (B21 Fig. 8, colour, M*-matched): blue/red = {DEL['in'][0]:.3f} +- {DEL['in'][1]:.3f} (R < 0.3 Mpc; "
      f"{math.log10(DEL['in'][0]):+.3f} dex vs B21's quoted -{B21_DELTA_QUOTED}), {DEL['out'][0]:.3f} +- {DEL['out'][1]:.3f} (R > 0.3 Mpc)")
    P("    data-based late-type factor t_db (in/out) per system: " + ", ".join(f"{k_} {t_db(k_, TARG['i'][k_])[0]:.2f}/{t_db(k_, TARG['i'][k_])[1]:.2f}" for k_ in SYSTEMS))
    # isolation leakage: GAMA (spectroscopic) vs KiDS isolated, and isolated vs all lenses (Fig. 9 vs Fig. A.4)
    gbK, EK, SK = b21_profile("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt"); CK, _ = b21_cov("Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", 1, 15)
    _, EG, SG = b21_profile("Fig-4-C1_RAR-GAMA-isolated_Nobins.txt"); CG, _ = b21_cov("Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt", 1, 15)
    z0 = np.zeros((15, 15))
    gk_out = amp(EG, CG, EK, CK, z0, gbK < B21_GBAR_ISO); gk_in = amp(EG, CG, EK, CK, z0, gbK >= B21_GBAR_ISO)
    C9, _ = b21_cov("Fig-9_RAR-KiDS-isolated_Massbins_covmatrix.txt", 4, 15); CA4, _ = b21_cov("Fig-A4_RAR-KiDS-all_Massbins_covmatrix.txt", 4, 15)
    allv = []
    for b in range(4):
        g9, E9, _ = b21_profile(f"Fig-9_RAR-KiDS-isolated_Massbin-{b + 1}.txt"); _, EA, _ = b21_profile(f"Fig-A4_RAR-KiDS-all_Massbin-{b + 1}.txt")
        gcut = 6.674e-11 * 10 ** B21_MGAL[b] * 1.989e30 / (0.3 * 3.0857e22) ** 2
        allv.append(amp(EA, CA4[b * 15:(b + 1) * 15, b * 15:(b + 1) * 15], E9, C9[b * 15:(b + 1) * 15, b * 15:(b + 1) * 15], z0, g9 < gcut))
    P(f"    isolation: GAMA (spectroscopic) / KiDS (photometric) isolated ESD = {gk_out[0]:.2f} +- {gk_out[1]:.2f} at R > 0.3 Mpc, "
      f"{gk_in[0]:.2f} +- {gk_in[1]:.2f} inside (B21's MICE: 1/1.30 = 0.77 beyond 0.3)")
    P("    group-like environments: ALL lenses / isolated lenses (Fig. A.4 / Fig. 9, R > 0.3 Mpc): " + ", ".join(f"bin {b + 1} {a:.2f} +- {e:.2f}" for b, (a, e) in enumerate(allv))
      + " -- the LV groups have companions, so the isolated profile UNDER-states them (the direction that deepens the tension)")
    # one at a time (primary systems), relaxed
    EDGES = {"type: data-based": [0, 0, 0, 0, 0, 0], "type: extreme (all-red bins, all-spiral LV)": None, "leakage 1/1.3": [0, -PRI["ll"], 0, 0, 0, 0],
             "M* scale -0.2 dex": [0, 0, -0.2, 0, 0, 0], "R0 method +0.05 dex": [0, 0, 0, 0.05, 0, 0], "eq.4 coefficient +0.04 dex": [0, 0, 0, 0, 0.04, 0],
             "epoch/h -0.045 dex": [0, 0, 0, 0, 0, -0.045], "KiDS errors inflated": [0, 0, 0, 0, 0, 0]}
    ONE = {}
    for lab, p in EDGES.items():
        row = {}
        for k_ in ("stack", "LG"):
            if lab.startswith("type: extreme"):
                ti, to = t_db(k_, TARG["i"][k_]); te = t_extreme(k_)
                row[k_] = T_sys(k_, [0, 0, 0, 0, 0, 0], dscale=factors(te[0] / ti, te[1] / to))
            elif lab == "KiDS errors inflated":
                row[k_] = T_sys(k_, p, infl=INFL[k_])
            else:
                row[k_] = T_sys(k_, p)
        ONE[lab] = row
    base = {k_: NOM[(k_, "i")]["h"].get("T_relaxed", NOM[(k_, "i")]["h"]["T"]) for k_ in ("stack", "LG")}
    P("    one systematic at a time (relaxed T; honest R0 errors):  face value: " + ", ".join(f"{k_} {v:.1f}" for k_, v in base.items()))
    for lab, row in ONE.items():
        P(f"      {lab:48s}: " + ", ".join(f"{k_} {v:6.1f}" for k_, v in row.items()) + f"   joint {sum(row.values()):6.1f}")
    check("S1 (reported) EACH COMPARABILITY SYSTEMATIC ALONE (the data-based type factor applied, then one more at its edge): the "
          "primary joint T stays above 3 sigma under every single one", "; ".join(f"{lab}: {sum(row.values()):.1f}" for lab, row in ONE.items()),
          all(sum(row.values()) > T_LIM2 for row in ONE.values()), load_bearing=False)
    # profiled (the rule's statistic), published and inflated covariance
    PROF = profile(("stack", "LG"), full=True)
    P(f"    profiled (stack + LG, shared nuisances, full R0 definition): T = {PROF['T']:.2f} (relaxed {PROF['T_relaxed']:.2f}; prior penalty "
      f"{PROF['pen']:.2f}; parts {', '.join(f'{k_} {v:.2f}' for k_, v in PROF['parts'].items())})")
    P("      at: " + ", ".join(f"{n_} {v:+.3f}" for n_, v in zip(("log t", "log l", "dM", "log R0", "log coef", "log s_z"), PROF["x"]))
      + f"  (priors: {PRI['lt']}, half {PRI['ll']:.3f}, {PRI['dM']}, {PRI['lr0']}, {PRI['lc']}, {PRI['lsz']} dex)")
    PROFI = profile(("stack", "LG"), full=True, infl=INFL)
    P(f"    profiled with the inflated KiDS covariance: T = {PROFI['T']:.2f} (relaxed {PROFI['T_relaxed']:.2f}; penalty {PROFI['pen']:.2f})")

    def at_opt(key, p, infl=1.0):
        """the full-QP solution at nuisances p: its constraint violation, R0_t, and the R0 an NFW fit to the adjusted KiDS data implies."""
        lt, ll, dM, lr0, lc, lsz = p; ll = min(ll, 0.0); R0, sq, sh, _ = SYSTEMS[key]
        d, C, cv = kids_for(TARG["i"][key], dM); ti, to = t_db(key, TARG["i"][key]); f = factors(ti * 10 ** lt, to * 10 ** lt, 10 ** ll)
        o = T_free(d * f, C * np.outer(f, f) * infl ** 2, R0 * 10 ** lr0, sh * 10 ** lr0, lc=lc, lsz=lsz, full=True)
        fr = fit_family("NFW", d * f, C * np.outer(f, f), 10 ** mgal_of(cv) / 1e12, lc=lc, lsz=lsz)
        d0 = kids_for(TARG["i"][key])[0]; out_ = RD > B21_R_ISO
        adj = float(np.mean(np.log10(np.clip(d * f, 1e-6, None)[out_] / np.clip(d0, 1e-6, None)[out_])))
        return dict(viol=o.get("viol", 0.0), R0t=o["R0t"], R0_nfw=fr["R0p"], R0_obs=R0 * 10 ** lr0, adj_out=adj,
                    type_part=float(math.log10(to) + lt))
    OPT = {k_: at_opt(k_, PROF["x"]) for k_ in ("stack", "LG")}
    P("    at the profiled optimum: " + "; ".join(f"{k_}: the free profile's R0 {v['R0t']:.2f} (max constraint violation {v['viol']:.1e}); an NFW fit "
                                                 f"to the adjusted KiDS data implies R0 {v['R0_nfw']:.2f} vs the (shifted) flow's {v['R0_obs']:.2f}; the adjusted lensing beyond 0.3 Mpc "
                                                 f"is {v['adj_out']:+.2f} dex from the published bins (galaxy type {v['type_part']:+.2f})" for k_, v in OPT.items()))
    single = {k_: profile((k_,), full=True) for k_ in ("stack", "LG", "M81", "IC342", "CenA", "LG_K09")}
    P("    profiled per system (full; M81 / IC 342 / Cen A with their quoted errors): " + ", ".join(f"{k_} {v['T']:.1f}" for k_, v in single.items()))
    # extreme corner: type at the extreme, leakage at 1/1.3, others profiled
    def corner(keys):
        def f(q):
            dM, lr0, lc, lsz = q; tot_ = 0.0
            for k_ in keys:
                ti, to = t_db(k_, TARG["i"][k_]); te = t_extreme(k_)
                tot_ += T_sys(k_, [0, -PRI["ll"], dM, lr0, lc, lsz], dscale=factors(te[0] / ti, te[1] / to))
            return tot_ + (dM / PRI["dM"]) ** 2 + (lr0 / PRI["lr0"]) ** 2 + (lc / PRI["lc"]) ** 2 + (lsz / PRI["lsz"]) ** 2
        r = minimize(f, [-0.15, 0.05, 0.02, -0.02], method="Nelder-Mead", options=dict(xatol=2e-3, fatol=1e-2, maxiter=400))
        return float(r.fun), [float(v) for v in r.x]
    CORN = corner(("stack", "LG"))
    P(f"    extreme corner (type at blue/red, leakage at 1/1.3, the Gaussian ones profiled): T = {CORN[0]:.2f} at dM {CORN[1][0]:+.2f}, log R0 {CORN[1][1]:+.3f}")
    # R <= 0.3 only, comoving
    R03 = {k_: T_sys(k_, [0] * 6, mask=RD <= 0.31) for k_ in ("stack", "LG")}
    R03f = {k_: T_free(*kids_for(TARG["i"][k_])[:2], SYSTEMS[k_][0], SYSTEMS[k_][2], mask=RD <= 0.31)["T"] for k_ in ("stack", "LG")}
    R03q = {k_: T_free(*kids_for(TARG["i"][k_])[:2], SYSTEMS[k_][0], SYSTEMS[k_][1], mask=RD <= 0.31)["T"] for k_ in ("stack", "LG")}
    PR03 = profile(("stack", "LG"), full=False, mask=RD <= 0.31, maxiter=300)
    COM = {k_: T_free(*[x * (1 + B21_Z) ** 2 if i == 0 else x * (1 + B21_Z) ** 4 for i, x in enumerate(kids_for(TARG["i"][k_])[:2])],
                      SYSTEMS[k_][0], SYSTEMS[k_][2], Rkern=RD / (1 + B21_Z))["T"] for k_ in ("stack", "LG")}
    P(f"    R <= 0.3 Mpc only (B21's range for analytic models): face value {', '.join(f'{k_} {v:.1f}' for k_, v in R03f.items())} (quoted R0 errors: "
      f"{', '.join(f'{k_} {v:.1f}' for k_, v in R03q.items())}); with t_db {', '.join(f'{k_} {v:.1f}' for k_, v in R03.items())}; profiled joint {PR03['T']:.2f}")
    P(f"    comoving reading (B21 state proper): face value {', '.join(f'{k_} {v:.1f}' for k_, v in COM.items())} (vs proper {', '.join(f'{k_} {v:.1f}' for k_, v in base.items())})")
    # epoch: the chain's own growth of the outer mass from z = 0.25 to 0
    Mb = 10 ** mgal_of(kids_for(TARG["i"]["stack"])[2]) * LGM
    ph1 = M6["phantom"](Mb, A0C, F11.L_of_a(1.0), F11.yth_of_a(1.0), F11.YIELD); ph8 = M6["phantom"](Mb, A0C, F11.L_of_a(1 / 1.25), F11.yth_of_a(1 / 1.25), F11.YIELD)
    rg = M6["RG"] / F11.MPC; gr = {R: float(np.interp(R, rg, ph1) / np.interp(R, rg, ph8)) for R in (0.3, 0.56, 0.76, 1.0)}
    P("    epoch: the chain's own phantom grows from z = 0.25 to 0 by " + ", ".join(f"x{v:.2f} at {R} Mpc" for R, v in gr.items())
      + " -- growth, like LCDM's accretion, DEEPENS the tension; the static assumption is the conservative side")
    check("S2 (reported) THE SYSTEMATICS TOGETHER: profiled jointly under their priors they absorb most of the face-value disagreement",
          f"primary joint T: face value {Tj_nom:.1f} -> profiled {PROF['T']:.2f} (inflated {PROFI['T']:.2f}); extreme corner {CORN[0]:.2f}; "
          f"R <= 0.3 Mpc profiled {PR03['T']:.2f}; per system " + ", ".join(f"{k_} {v['T']:.1f}" for k_, v in single.items()),
          PROF["T"] < 0.25 * Tj_nom, load_bearing=False, reading=f"the nuisances at the optimum: type {PROF['x'][0]:+.2f} dex beyond t_db, leakage {min(PROF['x'][1], 0):+.2f}, "
                                            f"M* {PROF['x'][2]:+.2f}, R0 {PROF['x'][3]:+.3f}, coefficient {PROF['x'][4]:+.3f}, epoch {PROF['x'][5]:+.3f} dex -- "
                                            f"each within ~{max(abs(PROF['x'][2]) / PRI['dM'], abs(PROF['x'][3]) / PRI['lr0'], abs(PROF['x'][0]) / PRI['lt']):.1f} sigma, all in the same direction")
    OUT["numbers"]["S"] = dict(infl=INFL, delta=DEL, gama_over_kids=[gk_out, gk_in], all_over_iso=allv, one_at_a_time=ONE, base=base, at_optimum=OPT,
                               profiled={k_: v for k_, v in PROF.items()}, profiled_inflated={k_: v for k_, v in PROFI.items()},
                               single={k_: v for k_, v in single.items()}, corner=CORN, R03=R03, R03_face=R03f, R03_quoted=R03q, R03_profiled=PR03, comoving=COM, chain_growth=gr)
    P(f"    {el()}")

    # ============================================================================================= F2 families
    banner("F2  THE PROFILE FAMILIES (face value, mapping (i), honest R0 errors): KiDS alone, the implied R0, and the joint fit")
    FAM = {}
    P(f"    {'system':6s} {'profile':10s} | {'chi2_K alone':>12s} {'R0 implied':>10s} | {'joint chi2_K':>12s} {'chi2_R0':>8s} {'joint':>8s} | "
      f"{'d chi2_PG':>9s} {'p':>8s} | fits both?")
    for k_ in ("stack", "LG"):
        R0, sq, sh, _ = SYSTEMS[k_]; d, C, cv = kids_for(TARG["i"][k_]); Mg = 10 ** mgal_of(cv) / 1e12
        for fam in ("NFW", "NFW+2h", "TIS", "chain+cut", "PPL"):
            a_ = fit_family(fam, d, C, Mg); j_ = fit_family(fam, d, C, Mg, R0, sh)
            dPG = j_["tot"] - a_["chiK"]; pp = float(chi2_dist.sf(max(dPG, 0), 1))
            FAM[(k_, fam)] = dict(alone=dict(chiK=a_["chiK"], R0p=a_["R0p"], p=a_["p"]), joint=dict(chiK=j_["chiK"], chiR=j_["chiR"], tot=j_["tot"], R0p=j_["R0p"], p=j_["p"]),
                                 dPG=dPG, p=pp, npar=a_["npar"])
            P(f"    {k_:6s} {fam:10s} | {a_['chiK']:12.1f} {a_['R0p']:10.2f} | {j_['chiK']:12.1f} {j_['chiR']:8.1f} {j_['tot']:8.1f} | {dPG:9.1f} {pp:8.1e} | "
              f"{'yes' if pp > 0.05 else ('no (3 sigma)' if pp < 0.0027 else 'marginal')}")
        fr = NOM[(k_, "i")]["h"]
        P(f"    {k_:6s} {'free':10s} | {fr['c0']:12.1f} {'--':>10s} | {fr['c0'] + fr['dK']:12.1f} {((fr['R0t'] - R0) / sh) ** 2:8.1f} {fr['c0'] + fr['T']:8.1f} | "
          f"{fr['T']:9.1f} {float(chi2_dist.sf(fr['T'], 1)):8.1e} | {'yes' if chi2_dist.sf(fr['T'], 1) > 0.05 else 'no'}")
        FAM[(k_, "free")] = dict(dPG=fr["T"], p=float(chi2_dist.sf(fr["T"], 1)))
    check("F2 (reported) THE FAMILIES AT FACE VALUE: no family fits both the KiDS profile and the published R0 of the stack or the LG; "
          "each family's KiDS-alone fit implies an R0 well above the flow's", "; ".join(f"{k_[0]}/{k_[1]}: d chi2_PG {v['dPG']:.1f}" + (f" (R0 implied {v['alone']['R0p']:.2f})" if 'alone' in v else "")
                                                                                         for k_, v in FAM.items()), all(v["p"] < 0.05 for v in FAM.values()), load_bearing=False)
    OUT["numbers"]["F2"] = {f"{k_[0]}/{k_[1]}": v for k_, v in FAM.items()}
    P(f"    {el()}")

    # ============================================================================================= L LCDM
    banner("L  LCDM's OWN FIT TO BOTH (NFW + galaxy, c free; and the LCDM standard NFW + two-halo with Duffy c(M), Tinker bias)")
    lc_rows = []
    for k_ in ("stack", "LG"):
        for fam in ("NFW", "NFW+2h"):
            v = FAM[(k_, fam)]; a_ = v["alone"]
            m200 = 10 ** a_["p"][0]; cc = 10 ** a_["p"][1] if fam == "NFW" else duffy_c(m200)
            lc_rows.append(f"{k_}/{fam}: KiDS alone chi2 {a_['chiK']:.1f}/{15 - v['npar']} (M200 {m200:.2f}e12, c {cc:.2f}) -> R0 {a_['R0p']:.2f} vs {SYSTEMS[k_][0]:.2f} "
                           f"+- {SYSTEMS[k_][2]:.2f}; joint d chi2 {v['dPG']:.1f}")
            P("    " + lc_rows[-1])
    check("L1 (reported) LCDM INHERITS THE FACE-VALUE PINCER: its halos fitted to KiDS's isolated lenses turn around at R0 ~ 1.6-2 Mpc "
          "(Lagrangian infall), not at the LV's 0.9 Mpc; fitted jointly it pays the same penalty as the free profile", "; ".join(lc_rows),
          all(FAM[(k_, fam)]["alone"]["R0p"] > SYSTEMS[k_][0] + 2 * SYSTEMS[k_][2] for k_ in ("stack", "LG") for fam in ("NFW", "NFW+2h")), load_bearing=False)
    OUT["numbers"]["L"] = lc_rows
    P(f"    {el()}")

    # ============================================================================================= D dynamics
    banner("D  THE DYNAMICS READING: Lagrangian (the published convention) vs the profile acting at every epoch vs switched on late")
    k_ = "stack"; R0, sq, sh, _ = SYSTEMS[k_]; d, C, cv = kids_for(TARG["i"][k_]); Mg = 10 ** mgal_of(cv) / 1e12
    Mn = FAM[(k_, "NFW")]; pr = Mn["alone"]["p"]; Mcum = nfw_Mcum(10 ** pr[0], 10 ** pr[1], Mg)

    def eul(zon=None):
        aon = None if zon is None else 1 / (1 + zon)
        return M6["lg_R0"](lambda r, a: (Mcum(r / LG_MPC) if (aon is None or a >= aon) else Mg + 0.0 * r) * 1e12 * LGM)
    R_l = R0_of(Mcum); R_e = eul()
    try:
        zon = brentq(lambda z: eul(z) - R0, 0.0, 3.0, xtol=2e-3)
    except ValueError:
        zon = float("nan")
    P(f"    the stack's KiDS NFW profile: Lagrangian R0 {R_l:.2f}; Eulerian-static (the profile in place from a = 0.02) {R_e:.2f}; "
      f"R0 = {R0:.2f} needs the outer mass switched on only after z_on = {zon:.3f} (baryons alone before)")
    check("D1 (reported) THE DYNAMICS READING: an Eulerian (field) reading lowers R0 for the same present profile, but reaching the "
          "flow's R0 needs the outer mass to appear only at z < z_on, below KiDS's own lens epoch (0.1 < z < 0.5, <z> = 0.25)",
          f"Lagrangian {R_l:.2f}, Eulerian-static {R_e:.2f}, z_on {zon:.3f} (KiDS lenses at <z> = 0.25)", zon < B21_Z, load_bearing=False,
          reading="the one escape the data leave a non-Lagrangian theory: an outer pull that is weaker over the flow's history than "
                  "its lensing today (FP12 found z_on = 0.14-0.22 with the chain's own law)")
    OUT["numbers"]["D"] = dict(R0_lagr=R_l, R0_euler=R_e, z_on=zon)
    P(f"    {el()}")

    # ============================================================================================= H direct Hubble diagram
    banner("H  THE DIRECT HUBBLE DIAGRAM: the published companions' velocities against the flow the KiDS profile implies")
    grp_t = {g: bos(l1 + lu) for g, l1, l2, n in KK_T6}
    grp = sorted(set(T7_MAIN[r_[0]] for r_ in T7)); sel_g = {g: np.array([T7_MAIN[r_[0]] == g for r_ in T7]) for g in grp}
    DMG = np.array([-0.5, -0.35, -0.2, -0.1, 0.0, 0.1])
    NFWG = {}                                                                     # (group, dM) -> KiDS NFW mass at the radii, split at 0.3 Mpc
    for key_g, tlog, Rg in [(g, grp_t[g], Rc7[sel_g[g]]) for g in grp] + [("LG", mgal_of(kids_for(TARG["i"]["LG"])[2]), Rc4[m14])]:
        for dm in DMG:
            d, C, cv = kids_for([(tlog, 1.0)], dm); Mg_ = 10 ** mgal_of(cv) / 1e12; fr = fit_family("NFW", d, C, Mg_)
            Mf = nfw_Mcum(10 ** fr["p"][0], 10 ** fr["p"][1], Mg_); NFWG[(key_g, dm)] = (Mf(np.minimum(Rg, B21_R_ISO)), Mf(Rg))
    ttype = {g: (t_db("M81" if g not in KK_EARLY else "CenA", [(grp_t[g], 1.0)]), (DEL["in"][0], DEL["out"][0]) if g not in KK_EARLY else (1.0, 1.0)) for g in grp}
    ttype["LG"] = (t_db("LG", TARG["i"]["LG"]), (DEL["in"][0], DEL["out"][0]))

    def masses(key_g, dM, tin, tout):
        """the KiDS NFW mass at the companions' radii, the type/leakage factors applied inside / beyond 0.3 Mpc (dM interpolated)."""
        x = min(max(dM, DMG[0]), DMG[-1]); j = int(min(max(np.searchsorted(DMG, x) - 1, 0), len(DMG) - 2)); w = (x - DMG[j]) / (DMG[j + 1] - DMG[j])
        a_in, a_all = [(1 - w) * NFWG[(key_g, DMG[j])][i] + w * NFWG[(key_g, DMG[j + 1])][i] for i in (0, 1)]
        return tin * a_in + tout * (a_all - a_in)

    HFIX = {}                                                                    # None: H free; else the H each sample's own eq. 14 fit returns

    def flow_chi(Rg, Vg, sig, Mvals, lc=0.0, lsz=0.0, Hfix=None):
        """eq. (14) generalised to an extended Lagrangian profile: V = H R [1 - sqrt(M_tot(<R) / (COEF R^3))], H free (or fixed)."""
        br = 1 - np.sqrt((10 ** lsz * Mvals + RHO0 * 4 * np.pi / 3 * Rg ** 3) / (COEF_T(lc) * Rg ** 3))
        H = float(np.sum(Rg * br * Vg) / np.sum((Rg * br) ** 2)) if np.sum((Rg * br) ** 2) > 0 else 0.0
        H = min(max(H, 20.0), 400.0) if Hfix is None else Hfix
        return float(np.sum(((H * Rg * br - Vg) / sig) ** 2)), H

    def flow_all(p, mode=None):
        """stack (Table 7) + LG (Table 4, 14 galaxies) chi2 at nuisances p = (lt, ll, dM, lc, lsz); mode picks a fixed corner."""
        lt, ll, dM, lc, lsz = p; ll = min(ll, 0.0); Ms = np.zeros(len(T7)); out = {}
        for g in grp + ["LG"]:
            (tdi, tdo), (tei, teo) = ttype[g]
            if mode == "face": ti, to = 1.0, 1.0
            elif mode == "extreme": ti, to = tei, teo * (1 / B21_LEAK)
            else: ti, to = tdi * 10 ** lt, tdo * 10 ** lt * 10 ** ll
            mv = masses(g, dM, ti, to)
            if g == "LG": out["LG"] = flow_chi(Rc4[m14], V4[m14], sig14, mv, lc, lsz, HFIX.get("LG"))
            else: Ms[sel_g[g]] = mv
        out["stack"] = flow_chi(Rc7, V7, sig7, Ms, lc, lsz, HFIX.get("stack")); out["n_infall"] = int(np.sum((10 ** lsz * Ms + RHO0 * 4 * np.pi / 3 * Rc7 ** 3) > COEF_T(lc) * Rc7 ** 3))
        return out
    penH = lambda p: (p[0] / PRI["lt"]) ** 2 + (min(p[1], 0.0) / PRI["ll"]) ** 2 + (p[2] / PRI["dM"]) ** 2 + (p[3] / PRI["lc"]) ** 2 + (p[4] / PRI["lsz"]) ** 2
    c7 = float(np.sum(((eq14(s7.x, Rc7) - V7) / sig7) ** 2)); c14 = float(np.sum(((eq14(s14.x, Rc4[m14]) - V4[m14]) / sig14) ** 2))
    HROW = {}
    for lab, mode, p in (("face value", "face", [0, 0, 0, 0, 0]), ("type db", None, [0, 0, 0, 0, 0]),
                         ("type db + leakage 1/1.3", None, [0, -PRI["ll"], 0, 0, 0]), ("extreme type + leakage", "extreme", [0, 0, 0, 0, 0]),
                         ("extreme + M* -0.2 + epoch -0.045", "extreme", [0, 0, -0.2, 0, -0.045])):
        o = flow_all(p, mode); HROW[lab] = dict(stack=o["stack"][0] - c7, H_stack=o["stack"][1], LG=o["LG"][0] - c14, H_LG=o["LG"][1], n_infall=o["n_infall"],
                                               chi=o["stack"][0] + o["LG"][0])
    fH = lambda p: (lambda o: o["stack"][0] + o["LG"][0])(flow_all(p)) + penH(p)
    rH = min((minimize(fH, x0, method="Nelder-Mead", options=dict(xatol=2e-3, fatol=1e-2, maxiter=600)) for x0 in
              ([0, 0, 0, 0, 0], [-0.05, -0.1, -0.2, 0.02, -0.02], [-0.1, -0.12, -0.35, 0.03, -0.04])), key=lambda r: r.fun)
    oH = flow_all(rH.x); HROW["profiled"] = dict(stack=oH["stack"][0] - c7, H_stack=oH["stack"][1], LG=oH["LG"][0] - c14, H_LG=oH["LG"][1],
                                                n_infall=oH["n_infall"], chi=rH.fun, x=[float(v) for v in rH.x], pen=float(penH(rH.x)))
    HFIX.update(stack=float(s7.x[0]), LG=float(s14.x[0]))                       # hold H at the flow's own point-mass value
    rF = min((minimize(fH, x0, method="Nelder-Mead", options=dict(xatol=2e-3, fatol=1e-2, maxiter=600)) for x0 in
              ([0, 0, 0, 0, 0], [-0.1, -0.12, -0.35, 0.03, -0.04], [-0.2, -0.2, -0.6, 0.06, -0.08])), key=lambda r: r.fun)
    oF = flow_all(rF.x); HROW["profiled, H fixed"] = dict(stack=oF["stack"][0] - c7, H_stack=oF["stack"][1], LG=oF["LG"][0] - c14, H_LG=oF["LG"][1],
                                                         n_infall=oF["n_infall"], chi=rF.fun, x=[float(v) for v in rF.x], pen=float(penH(rF.x)))
    HFIX.clear()
    dofH = len(V7) - 1 + int(m14.sum()) - 1
    for lab, v in HROW.items():
        v["p_gof"] = float(chi2_dist.sf(v["chi"], dofH))
        P(f"    {lab:34s}: stack d chi2 {v['stack']:+7.1f} (H_loc {v['H_stack']:.0f}; {v['n_infall']}/66 predicted infalling), LG(14) d chi2 "
          f"{v['LG']:+7.1f} (H_loc {v['H_LG']:.0f}); goodness of fit chi2 {v['chi']:.1f}/{dofH} (p {v['p_gof']:.1e})")
    P(f"      eq. 14's own fits: chi2 {c7:.1f} + {c14:.1f} (sigma_v {sig7:.0f} / {sig14:.0f} km/s, the velocity errors used here); profiled at "
      + ", ".join(f"{n_} {x_:+.3f}" for n_, x_ in zip(("log t", "log l", "dM", "log coef", "log s_z"), rH.x)) + f" (penalty {HROW['profiled']['pen']:.1f}); "
      f"with H held at the flow's own point-mass value ({s7.x[0]:.0f} / {s14.x[0]:.0f}) at " + ", ".join(f"{n_} {x_:+.3f}" for n_, x_ in
      zip(("log t", "log l", "dM", "log coef", "log s_z"), rF.x)) + f" (penalty {HROW['profiled, H fixed']['pen']:.1f})")
    check("H1 (reported) THE VELOCITIES THEMSELVES, no R0 compression: the KiDS-implied flow (each companion's shell holding the KiDS mass "
          "of its group's centre, eq. 14 generalised, free local H) fails the published velocities at face value (p < 0.0027); with the "
          "systematics profiled it is " + ("still excluded" if HROW["profiled"]["p_gof"] < 0.0027 else "no longer excluded at 3 sigma"),
          "; ".join(f"{lab}: stack {v['stack']:+.0f}, LG {v['LG']:+.0f} (p {v['p_gof']:.0e})" for lab, v in HROW.items()),
          HROW["face value"]["p_gof"] < 0.0027, load_bearing=False,
          reading="caveats: sigma_v from the point-mass fit; coherent bulk flows of whole groups (K&K: the Local Void outflow) are not "
                  "modelled; the local H is free -- the KiDS flow wants H_loc ~ 110-140 km/s/Mpc, against the flow's own point-mass fits "
                  f"(86 / 85) and the global 67-73; held at 86 / 85 the profiled test gives p {HROW['profiled, H fixed']['p_gof']:.0e}; the type/leakage factors scale the "
                  "fitted NFW mass inside / beyond 0.3 Mpc (an approximation to refitting)")
    OUT["numbers"]["H"] = HROW
    P(f"    {el()}")

    # ============================================================================================= V verdict
    banner("V  THE VERDICT (the rule declared in the docstring)")
    v1 = Tj_nom > T_LIM2
    p_nom, s_nom = sig_of(Tj_nom, 2); p_pro, s_pro = sig_of(PROF["T"], 2); p_pri, s_pri = sig_of(PROFI["T"], 2)
    check("V1 THE PUBLISHED DATA DISAGREE AT FACE VALUE: no non-negative spherical profile fits KiDS's isolated lenses (at the LV "
          "centrals' masses) together with K&K 2018's stack and LG zero-velocity radii (honest errors) -- T_nominal > 11.83 (p < 0.0027)",
          f"T = {Tj_nom:.1f} (stack {NOM[('stack', 'i')]['h']['T']:.1f}, LG {NOM[('LG', 'i')]['h']['T']:.1f}; p {p_nom:.1e}, {s_nom:.1f} sigma); with "
          f"the quoted errors {NOM[('stack', 'i')]['q']['T'] + NOM[('LG', 'i')]['q']['T']:.0f}", v1)
    if Tj_nom <= T_OK2:
        VERD = "COMPATIBLE"
    elif PROF["T"] > T_LIM2 and PROFI["T"] > T_LIM2:
        VERD = "IN TENSION"
    else:
        VERD = "UNDECIDED"
    per_sys = {}
    T_OK1 = float(chi2_dist.isf(0.05, 1))
    for k_ in ("stack", "LG", "M81", "IC342", "CenA", "LG_K09"):
        tn = NOM[(k_, "i")]["h"]["T"] if NOM[(k_, "i")]["h"] else NOM[(k_, "i")]["q"]["T"]
        tp = single[k_]["T"] if k_ in single else float("nan")
        per_sys[k_] = ("COMPATIBLE" if tn <= T_OK1 else ("IN TENSION" if tp > T_LIM1 else "UNDECIDED"), tn, tp)
    check("V2 (reported) THE VERDICT BY THE DECLARED RULE, and per system (1 dof: compatible if T_nominal <= 3.84, in tension if "
          "T_profiled > 9)", f"primary (stack + LG): {VERD} -- T_nominal {Tj_nom:.1f} ({s_nom:.1f} sigma), T_profiled {PROF['T']:.2f} "
          f"({s_pro:.1f} sigma), inflated {PROFI['T']:.2f} ({s_pri:.1f} sigma); per system: " + ", ".join(f"{k_} {v[0]} ({v[1]:.0f} -> {v[2]:.1f})" for k_, v in per_sys.items()),
          True, load_bearing=False)
    OUT["numbers"]["V"] = dict(T_nominal=Tj_nom, T_profiled=PROF["T"], T_profiled_inflated=PROFI["T"], verdict=VERD, per_system=per_sys,
                               p=dict(nominal=p_nom, profiled=p_pro, inflated=p_pri))

    # ============================================================================================= W ledger
    banner("W  THE LEDGER: FP18, the KiDS-vs-Hubble-flow pincer as a data-only test")
    F12J = json.load(open(os.path.join(HERE, "FP12_local_volume_groups_r0_results.json")))["numbers"]
    ch_stack = (F12J["V"]["stack"]["canonical"]["true_w"], F12J["V"]["stack"]["alt"]["true_w"])
    ch_lg = (F12J["R1"]["LG_scored"]["canonical"], F12J["R1"]["LG_scored"]["alt"])
    kR0 = [FAM[(k_, f_)]["alone"]["R0p"] for k_ in ("stack", "LG") for f_ in ("NFW", "NFW+2h", "TIS", "chain+cut", "PPL")]
    hp, hf = HROW["profiled"], HROW["profiled, H fixed"]
    LEDGER = [
        ("F18a", "the model-independent bound: for any non-negative spherical excess density Delta Sigma(R) <= M(<R)/(pi R^2), so KiDS's "
                 f"stacked lenses give M(<R) >= pi R^2 Delta Sigma(R) with no profile assumed (voids outside R change it by < {dv:.2f} Msun/pc^2)",
         "DERIVED", "K7 (2000 random profiles), B1"),
        ("F18b", f"the published R0 errors omit the velocity scatter: K&K 2018's +-0.02 (stack) is their 5%-distance Monte Carlo (reproduced: "
                 f"+-{mc[:, 1].std():.3f}); the bootstrap of their own estimator on their own Table 7 gives +-{sb7:.2f} (LG, Table 4: +-{sb14:.2f}); "
                 f"FP12's fit form V = H R [1 - (R0/R)^(1/2)] is not K&K's eq. (14) (it returns R0 = {abs(s12.x[1]):.2f} on K&K's own table)",
         "CONSTRAINT", "K4, E1"),
        ("F18c", f"at face value NO static spherical profile fits KiDS's isolated lenses (at the LV centrals' masses) and the LV Hubble flow: "
                 f"T = {Tj_nom:.0f} (stack + LG, honest R0 errors; {NOM[('stack', 'i')]['q']['T'] + NOM[('LG', 'i')]['q']['T']:.0f} with the quoted "
                 f"ones); every family fails, LCDM's NFW(+2h) included (KiDS-fitted profiles turn around at R0 = {min(kR0):.2f}-{max(kR0):.2f} Mpc "
                 f"vs 0.91-0.93); the velocities themselves reject the KiDS-implied flow at p ~ {HROW['face value']['p_gof']:.0e}; within R <= 0.3 Mpc "
                 f"the two agree (T = {R03f['stack']:.1f} / {R03f['LG']:.1f}) -- the disagreement lives at 0.3-2.6 Mpc, where B21 flag photo-z isolation",
         "CONSTRAINT" if v1 else "DERIVED", "B1, F1, F2, L1, H1, S, V1"),
        ("F18d", f"the comparability systematics (galaxy type, photo-z isolation leakage, stellar-mass scale, R0 method, eq. 4 coefficient, "
                 f"epoch/h), profiled jointly under declared priors, bring the joint T to {PROF['T']:.1f} ({s_pro:.1f} sigma; inflated covariance "
                 f"{PROFI['T']:.1f}; extreme corner {CORN[0]:.1f}); each alone leaves it >= {min(sum(r_.values()) for r_ in ONE.values()):.0f} (S1); "
                 f"at the optimum M* {PROF['x'][2]:+.2f} dex, R0 {PROF['x'][3]:+.3f} dex, type {PROF['x'][0]:+.2f} dex beyond the data-based factor, "
                 f"leakage {min(PROF['x'][1], 0):+.2f} dex; the direct velocity test agrees (profiled p = {hp['p_gof']:.2f}) but only with a local "
                 f"H ~ {hp['H_stack']:.0f} km/s/Mpc -- held at the flow's own point-mass value it gives p = {hf['p_gof']:.0e}", "FITTED", "S1, S2, H1"),
        ("F18e", f"the verdict by the declared rule: {VERD}", "OPEN" if VERD == "UNDECIDED" else ("CONSTRAINT" if VERD == "IN TENSION" else "FAILS"), "V1, V2"),
        ("F18f", f"for the chain: at face value KiDS itself, read as a static Lagrangian profile, demands R0 = {min(kR0):.2f}-{max(kR0):.2f} Mpc "
                 f"for the stack / LG centrals -- above the chain's own {ch_stack[0]:.2f}/{ch_stack[1]:.2f} (stack) and {ch_lg[0]:.2f}/{ch_lg[1]:.2f} (LG) "
                 f"(FP12), so the chain's R0 overshoot is not a refutation of its outer profile by this pair; after the systematics the reconciled "
                 f"target is R0 ~ {min(v['R0_nfw'] for v in OPT.values()):.2f}-{max(v['R0_nfw'] for v in OPT.values()):.2f} Mpc with the LV centrals' "
                 f"lensing beyond 0.3 Mpc {min(v['adj_out'] for v in OPT.values()):+.2f} to {max(v['adj_out'] for v in OPT.values()):+.2f} dex from B21's "
                 f"published bins, of which {min(v['type_part'] for v in OPT.values()):+.2f} to {max(v['type_part'] for v in OPT.values()):+.2f} dex is the "
                 "measured spiral-vs-mixed (red/blue) difference at fixed M* -- a type dependence the chain's universal law does not produce; "
                 "the rest are measurement systematics that would move the chain's own KiDS target too", "CONSTRAINT", "F2, S, D1, FP12"),
        ("F18g", f"the escape for a field (non-Lagrangian) theory: an outer pull weaker over the flow's history than its lensing today; with "
                 f"the stack's KiDS profile (Lagrangian R0 {R_l:.2f}, Eulerian-static {R_e:.2f}) R0 = {SYSTEMS['stack'][0]:.2f} needs the outer "
                 f"mass to switch on only after z_on = {zon:.2f}, later than KiDS's own lenses (<z> = 0.25) -- the same z_on FP12 found for the chain",
         "CONSTRAINT", "D1, FP12 U2"),
        ("F18h", "open: the deciding measurement is like-for-like -- the lensing Delta Sigma(0.3-1.5 Mpc) of spectroscopically isolated SPIRAL "
                 "centrals at M_gal ~ 10^10.4-10.8 (the LV analogs; the record holds the KiDS-1000 shear catalogue and a re-measurement "
                 "pipeline, reviews/lensing_rar/lr_esd_remeasure.py), and on the flow side R0 with its bootstrap error plus a group bulk-flow "
                 "model for the companion velocities", "OPEN", "S, H1"),
        ("F18i", "the record's KiDS lead-grade projection (FP6 esd_of_M, used by FP6/FP9/FP11/FP12's KiDS numbers) under-projects: on a "
                 f"singular isothermal sphere it is {b6[0]:+.0%} at 35 kpc, {b6[7]:+.0%} at 0.3 Mpc, {b6[10]:+.0%} at 0.76 Mpc, {b6[14]:+.0%} at "
                 "2.6 Mpc (this lane's exact projection: < 0.5%); those lanes' KiDS chi2 are not re-scored here", "OPEN", "K2, K2b"),
    ]
    for k_, what, status, why in LEDGER:
        P(f"    {k_:5s} {status:11s} {what}  --  {why}")
    OUT["ledger"] = [dict(link=k_, what=w, status=s_, basis=b_) for k_, w, s_, b_ in LEDGER]
    check("W (reported) the ledger of this lane", f"{len(LEDGER)} links", True, load_bearing=False)

    # ============================================================================================= verdict block
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    banner("VERDICT")
    P(f"  Joint fit table (face value, mapping (i), honest R0 errors; d chi2_PG = joint minimum - KiDS-alone minimum, 1 dof):")
    P(f"    {'profile':10s} | {'chi2 KiDS (stack/LG)':>21s} | {'chi2 R0 (stack/LG)':>19s} | {'joint (stack/LG)':>17s} | {'d chi2_PG':>11s} | verdict")
    for fam in ("NFW", "NFW+2h", "TIS", "chain+cut", "PPL"):
        a, b = FAM[("stack", fam)], FAM[("LG", fam)]
        P(f"    {fam:10s} | {a['joint']['chiK']:9.1f} / {b['joint']['chiK']:9.1f} | {a['joint']['chiR']:8.1f} / {b['joint']['chiR']:8.1f} | "
          f"{a['joint']['tot']:7.1f} / {b['joint']['tot']:7.1f} | {a['dPG']:5.1f} / {b['dPG']:5.1f} | "
          + ("fits both" if min(a['p'], b['p']) > 0.05 else "cannot fit both"))
    P(f"    {'free':10s} | {'(any non-negative profile: minimum penalty)':>61s} | {FAM[('stack', 'free')]['dPG']:5.1f} / {FAM[('LG', 'free')]['dPG']:5.1f} | "
      + ("fits both" if min(FAM[('stack', 'free')]['p'], FAM[('LG', 'free')]['p']) > 0.05 else "cannot fit both"))
    P(f"  VERDICT (declared rule): {VERD}.  Face value T = {Tj_nom:.1f} ({s_nom:.1f} sigma, honest errors); systematics profiled T = "
      f"{PROF['T']:.2f} ({s_pro:.1f} sigma), inflated covariance {PROFI['T']:.2f}; extreme corner {CORN[0]:.2f}.")
    P(f"  Per system (1 dof): " + ", ".join(f"{k_} {v[0]} ({v[1]:.0f} -> {v[2]:.1f})" for k_, v in per_sys.items()) + ".  Within R <= 0.3 Mpc the "
      f"datasets agree at face value (T = {R03f['stack']:.1f} / {R03f['LG']:.1f}); the disagreement lives at 0.3-2.6 Mpc.")
    P(f"  The velocities without the R0 compression: face value p = {HROW['face value']['p_gof']:.0e}; profiled p = {HROW['profiled']['p_gof']:.2f} with a "
      f"free local H ({HROW['profiled']['H_stack']:.0f} / {HROW['profiled']['H_LG']:.0f} km/s/Mpc), p = {HROW['profiled, H fixed']['p_gof']:.3f} with H held "
      f"at the flow's own point-mass value.  LCDM (NFW c free): KiDS-fitted R0 {FAM[('stack', 'NFW')]['alone']['R0p']:.2f} / "
      f"{FAM[('LG', 'NFW')]['alone']['R0p']:.2f} Mpc -- the same face-value pincer.")
    P("  Not 'closed'.  Time " + f"{time.time() - T0:.0f} s.")
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))

    def enc(o):
        if isinstance(o, np.ndarray): return o.tolist()
        if isinstance(o, (np.floating, np.integer)): return float(o)
        if isinstance(o, (np.bool_,)): return bool(o)
        return str(o)

    def clean(o):
        if isinstance(o, dict):
            return {(k_ if isinstance(k_, str) else str(k_)): clean(v) for k_, v in o.items() if k_ not in ("M", "Mcum", "m")}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        return o
    json.dump(clean(OUT), open(fn, "w"), indent=1, default=enc)
    P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}")
    sys.exit(0 if nlb == 0 else 1)


COEF_SI = KK_COEF                                                                 # replaced by K3's integrator value in main()

if __name__ == "__main__":
    main()
