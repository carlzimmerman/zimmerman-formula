#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP21 -- WEAK LENSING AROUND SPECTROSCOPICALLY ISOLATED SPIRALS OF LOCAL-VOLUME MASS.  A MEASUREMENT, favouring no theory:
the excess surface density Delta Sigma(R) at 0.03-3 Mpc around galaxies with SPECTROSCOPIC redshifts in the KiDS-1000
footprint, whose masses are defined exactly as the Local Volume (LV) centrals' masses are, compared with (a) the published
mixed-type KiDS isolated-lens bins (Brouwer+21, B21) at the same mass and (b) the mass the LV groups' zero-velocity radii
R0 allow.  It decides whether FP18's KiDS-versus-Hubble-flow pincer is real -- or says what sample would decide it.

WHY.  FP18 (09990b398): at face value no mass profile fits both B21's isolated lenses at the LV centrals' mass and the LV
groups' R0 (T = 102, 9.8 sigma); six comparability systematics profiled under priors bring it to 2.3 sigma (UNDECIDED).
Reconciliation needs the lensing of SPIRALS beyond 0.3 Mpc ~0.5 dex below B21's mixed-type bins (the measured blue/red
contrast supplies -0.18 to -0.25 dex of it), plus R0 +0.08 dex.  The three largest systematics -- the stellar-mass scale
(B21's LePhare M* vs the LV's 0.6 L_K), photometric isolation leakage beyond 0.3 Mpc, and galaxy type -- are properties of
the LENS SAMPLE.  A lens sample with spectroscopic redshifts, K-band masses and type labels removes or measures each.

THE DATA (each read at its source for this lane; none quoted from memory)
  (a) SOURCES: KiDS-1000 SOM-gold weak-lensing catalogue (Giblin+21; real_research/data/lensing_rar/KiDS_DR4.1_SOM_gold_WL_cat
      .fits, 21,262,011 rows, 833-byte records; streamed column-wise, ~35 s): RAJ2000, DECJ2000, e1, e2, weight, Z_B, MASK.
  (b) LENSES: 2M++ (Lavaux & Hudson 2011, MNRAS 416, 2840; VizieR J/MNRAS/416/2840, the record's gext_vectors_2026/data/raw/
      2mpp_vizier.tsv, 72,973 rows): a redshift compilation (2MRS + 6dFGS + SDSS + literature) complete to K2M++ <= 12.5 in the
      SDSS (flag M1) and 6dFGS (flag M2) regions -- BOTH KiDS regions are inside them (2,173 of the 2,176 2M++ galaxies in the
      KiDS footprint carry M1 or M2).  Columns: Ks (isophotal, extinction-corrected), Vcmb, completeness c11.5 / c12.5, Ref
      ("none" = no measured redshift, velocity assigned by 2M++).  THIS IS THE ONLY SPECTROSCOPIC CATALOGUE ON DISK THAT
      COVERS THE KiDS FOOTPRINT: GAMA DR4 and SDSS DR7 are not in the record; fetching them needs the user's go.
  (c) MAGNITUDE SYSTEM: 2MRS (Huchra+12; real_research/data/2mrs_catalog.csv) extinction-corrected TOTAL Ks (Ktmag).  2M++'s
      Ks is isophotal: median K2M++ - Ktot = +0.24 mag, rising with K; the calibration uses K2M++ <= 11.75 only (the 2MRS limit
      Ktot < 11.75 truncates the offset distribution above that).
  (d) TYPE LABELS: ALFALFA a100 HI detections (Haynes+18, positions/velocities from Durbala+20 Table 1: real_research/data/
      alfalfa_sdss_durbala2020_t1.tsv) = gas-rich = LATE; the 6dFGS Fundamental-Plane sample (Campbell+14: fp_6dfgs_campbell
      2014.tsv; its RAJ2000 column is in HOURS despite the 'deg' label -- detected and converted) = spectroscopic EARLY types;
      KiDS-bright LePhare rest-frame u - r (Bilicki+21; KiDS_DR4_brightsample*_LePhare.fits) for the rest.  CAVEAT, measured in
      T1: at z ~ 0.026 the KiDS GAaP aperture (~2") samples the central ~1 kpc, i.e. the BULGE of a nearby spiral, so the colour
      is a weak type indicator here; the cut is calibrated on the labels (below), never on the lensing.
  (e) THE LV SIDE (FP18, committed): R0 = 0.93 (stack) / 0.91 (LG) Mpc with FP18's HONEST errors (bootstrap (+) quoted:
      0.117 / 0.111, read from FP18_kids_vs_hubble_flow_data_results.json); eq. (4) M_T = COEF R0^3 with COEF from the record's
      shell integrator (1.9553e12, FP18 K3); the LV centrals' M_gal targets (FP18 mapping (i)); UNGC (Karachentsev+13) to check
      the L_K formula; B21 Fig-3 profiles + (m,n,i,j)-ordered covariance through FP18's loaders.
  (f) PIPELINE VALIDATION: the record's photometric reconstruction of B21's isolated lenses (lr_lenses.npz; FP18 K6: it
      reproduces B21's four bin mean masses to <= 0.013 dex), bins 2 (10.3 <= log M* < 10.6) and 3 (10.6-10.8).

CONVENTIONS (stated)
  * Cosmology B21's (WMAP9 flat, Om 0.2793, h = 0.7; h70 units); R = PROPER transverse separation (B21 Sect. 3.1); Sigma_crit
    from D_l D_ls / D_s with the source's Z_B; sources Z_B > z_l + 0.2 (B21); weights w_ls = w_s Sigma_crit^-2; Delta Sigma =
    sum w_ls e_t Sigma_crit / sum w_ls.  Tangential ellipticity e_t = e1 cos 2PA + e2 sin 2PA (PA east of north, exact spherical
    geometry) -- identical to the record's validated handedness (lr_esd_remeasure v3: e_t = -(e1 cos 2phi - e2 sin 2phi),
    phi from +RA); e_x the 45-degree component (null test).  60 fine log bins 0.03-3 Mpc (4 per B21 bin; B21's 15 bins reused).
  * Lens mass = FP18's mapping (i) EXACTLY: log L_K = 0.4 (3.28 - M_K), M_K = K_tot - 5 log10(d_L/10 pc) + 6 log10(1+z)
    (Kochanek+01 K-correction), d_L from Vcmb; M* = 0.6 L_K (FP18's Upsilon_K); M_gal = M* (1 + f_cold) with B21's Boselli
    f_cold.  K4 checks the L_K formula against UNGC's own L_K (the source of K&K's LV-central masses).  So the stellar-mass-
    scale systematic (FP18's largest nuisance, -0.28 dex at the profiled optimum) is ABSENT by construction; the lenses are at
    z ~ 0.026, so the epoch systematic is absent too.  Lens redshift z >= 0.01 (Vcmb >= 3000 km/s: peculiar velocities <= 10%
    of the distance, apertures <= 4 deg).  Target 10.4 <= log M_gal <= 10.8 (the LV centrals, mapping (i): 10.40-10.82).
  * Type: LATE = ALFALFA-detected (30", |dV| <= 300 km/s, heliocentric) and not 6dF-FP, or (no label and GAaP u - r < 2.35);
    EARLY = 6dF-FP (10", |dV| <= 300) and not HI-detected, or (no label and u - r >= 2.50); otherwise ambiguous/unknown.  The
    cuts are FIXED from the label calibration (T1: 0/28 FP early types have u - r < 2.35 at the target mass; 64-77% of HI-rich
    spirals have u - r < 2.3-2.4) before any lensing was run with them.
  * ISOLATION (spectroscopic; the whole-sky 2M++ is the neighbour pool, complete for "brighter than the lens" because the lens
    itself is above the flux limit): PRIMARY = no 2M++ galaxy brighter in total Ks within projected proper R_p <= 3 Mpc and
    |dVcmb| <= 500 km/s (~2 group velocity dispersions; B21's own 3-Mpc radius).  Variants: the redshift-space 3-Mpc sphere
    sqrt(R_p^2 + (dV/H0)^2) <= 3 Mpc (B21's GAMA-like definition), +-1000 / +-2000 km/s, and "group centrals" (brightest within
    R_p <= 1.0 / 1.5 Mpc, +-500): by the shell theorem of FP18 K7 a brighter galaxy OUTSIDE R adds nothing positive to the
    stacked Delta Sigma(< R), so the group-central samples are the like-for-like lensing analogs of R0 (the flow measures the
    group's mass inside R0 ~ 0.93 Mpc).  Leakage is tested three ways (L1).
CORRECTIONS (all applied; each printed)
  * additive c: the weighted mean e1, e2 subtracted per KiDS region (N/S) x tomographic bin (Z_B edges 0.1/.3/.5/.7/.9/1.2);
  * multiplicative m: divided by B21's released (1+K) = 0.98531 (read from the Fig-3 files: the same value the comparison bins
    carry);
  * photo-z dilution: a declared model p(z_true | Z_B) = 0.9 N(Z_B, 0.06 (1 + Z_B)) + 0.1 n_all(z) gives f = <Sigma_crit^-1
    (z_true)> / Sigma_crit^-1(Z_B) per pair; Delta Sigma is divided by the weighted mean f (~1% at z_l ~ 0.026; larger at z_l ~
    0.3, where K6 tests it against B21);
  * boost: B(R) = [sum_L w_ls / N_L] / [sum_R w_rs / N_R] against randoms re-weighted to the lens redshift distribution; the
    lens signal is multiplied by max(B, 1): B > 1 is dilution by lens-associated sources, B < 1 is obscuration by the bright
    lenses' own masks (no shear bias) -- raw-B and no-boost variants are reported;
  * random points: 12,000 uniform in the footprint (HEALPix nside 256 source-density mask), redshifts drawn from the lens
    candidates, subtracted after the same corrections.
COVARIANCE.  Jackknife over 40 equal-area sky patches (20 RA stripes in KiDS-N, 20 in KiDS-S), leave-one-patch-out of lenses
  AND randoms (the full estimator, boost included, recomputed each time), over the patches that hold the sample's lenses;
  Hartlap-corrected wherever inverted.  Shape-noise-only errors are printed beside it.
COMPARISONS.  (a) B21 mixed-type at the same mass: FP18's kids_for over the sample's lensing-weighted M_gal distribution,
  its covariance from the corrected C60; the amplitude A = band(sample) / band(mixed) over the BAND = B21 bins 8-13 (R 0.26-1.62
  Mpc) with the sample's own pair weights.  (b) the flow: the two R0 combined (independent galaxy sets: 0.93 +- 0.117,
  0.91 +- 0.111 -> 0.920 +- 0.080); the rigorous envelope Delta Sigma(R) <= M_max(<R)/(pi R^2) with M_max = COEF R0^3 - mean
  inside R0 and the outermost-crossing cap beyond (FP18 B, K7; exact, any non-negative profile); the NFW-family envelope
  (profiles turning around at R0, projected with FP18's uniform-shell kernel, < 0.5% vs analytic; FP6's esd_of_M is NOT used);
  the joint free-profile statistic T = min over profiles [chi2_lens + chi2_R0] - min [chi2_lens] (FP18's T_free, full R0
  definition) on 6 wide bins with the pair-weight-averaged shell kernel, mass-matched to the LV centrals by B21's mass trend.
RULE (fixed before this lane's committed run; designed after EXPLORATORY prototype runs on the same data, which showed: only
  ~10-15% of target-mass 2M++ galaxies are the brightest within 3 Mpc; the unselected target-mass stack sits ~2x above B21's
  isolated bins at 0.5-1.4 Mpc; the pipeline reproduces B21's bins 2/3 at 1.06-1.08 before corrections).  A development run
  of this script (reduced randoms) then showed: the honest jackknife error at z ~ 0.026 is ~2x shape noise (0.3-1.6 Mpc is
  ~1 deg, where cosmic-shear noise equals shape noise and is shared by clustered lenses), so the target-mass stack alone is a
  ~3-sigma detection -- the load-bearing DETECTION control D1 was therefore moved to the full 2M++ candidate stack (same
  threshold; the target-mass S/N is reported as D1b); the null tests use the exact Hotelling T^2 -> F test (a Hartlap chi^2 is
  anticonservative in the tail for 40 patches); A_rec scales the WHOLE mixed profile (scaling only R > 0.26 Mpc cannot reach
  compatibility, because B21's inner lensing already fixes the mass).  The first COMMITTED run then failed K6 as first declared
  (every correction applied: bin 3 at 1.28 +- 0.10, outside [0.80, 1.20]; bin 2 at 1.00): the excess sits entirely inside
  0.3 Mpc (1.65 there, 1.04 beyond) and is the BOOST correction -- against uniform randoms the photometric bin-3 lenses show
  B = 1.15-1.23 inside 0.3 Mpc, which is largely an artefact (those lenses are selected unmasked, while uniform randoms fall in
  the footprint's masked holes, ~19% of it: 957 deg^2 of pixels vs KiDS's ~777 deg^2 effective area), and B21's published bins
  match the pipeline WITHOUT it.  So K6 is now the like-for-like validation (B21's convention: no boost); the first-declared
  form is kept, reported, as K6b, and it still fails.  For the 2M++ lenses B <= 1 in the band (obscuration by their own
  masks), so max(B, 1) never acts there and no 2M++ number changes.  The verdict rule below is unchanged.  PRIMARY: the LATE-
  type, primary-isolated, target-mass sample; T with the combined R0, dof 1; A over the band.
    RECONCILED   if T <= 3.84 (p >= 0.05) AND (1 - A) / sigma_A >= 2: spiral lensing is measurably below the mixed level and
                 meets the flow.
    PINCER REAL  if T > 9.0 (3 sigma): no profile fits the spirals' lensing and the flow together (A is quoted beside it).
    UNDECIDED    otherwise -- and the sample size that would decide is computed: N such that A = 1 and A = A_rec (the
                 face-value reconciliation amplitude, from T on B21's own precision) differ by 3 sigma.
  Reported, not in the rule: all-type / early-type / group-central / window variants; the non-isolated sample; the Z_B > 0.5,
  MASK == 0, raw-boost and no-boost variants; the FP18-style two-system T (dof 2); the model-independent mass bound.

CHECKS
  K1 CONTROL the source catalogue and the null: 21,262,011 sources, |c| < 2e-3 per region x bin; the cross-shear Delta Sigma_x
     of the full 2M++ footprint stack is consistent with zero (jackknife Hotelling T^2 -> F, p > 0.001).
  K2 CONTROL the projection: FP18's uniform-shell kernel reproduces analytic NFW (Wright & Brainerd) and SIS Delta Sigma < 1%.
  K3 CONTROL this lane's T implementation (arbitrary kernel) reproduces FP18's T_free on FP18's own stack input, and FP18's
     committed 51.9.
  K4 CONTROL the mass scale: the L_K formula reproduces UNGC's log L_K (median |d| < 0.02 dex).
  K5 CONTROL randoms: the random-point Delta Sigma is consistent with zero (jackknife Hotelling T^2 -> F, p > 0.001).
  K6 CONTROL the pipeline, with B21's convention (c, m, dilution model, randoms; no boost correction), reproduces B21's published
     Fig-3 bins 2 and 3 in R from the record's photometric reconstruction: amplitude within [0.80, 1.20] for both.
  K6b (reported) the same with the measured boost applied (K6 as first declared) -- it fails for bin 3; the boost per radius.
  T1 (reported) the type-cut calibration on the labels.   L1 (reported) the isolation leakage tests.
  D1 [load-bearing; MUTATE must fail] the full 2M++ candidate stack (all masses, all environments) DETECTS lensing: S/N > 4 over
     0.03-1.62 Mpc (jackknife).   D1b (reported) the same for the target-mass stack alone.
  D2 (reported) the primary table: Delta Sigma(R) +- jackknife (shape noise), S/N per bin.   D3 (reported) every variant.
  C1 (reported) vs B21 mixed at the same mass.   C2 (reported) vs the R0 envelope and the mass bound.   C3 (reported) T.
  V1 (reported) the verdict by the rule.   V2 (reported) the sample size that would decide.   W the ledger.
MUTATE=1 moves every 2M++ lens to a random footprint position (same redshift, mass, type and isolation flags) before the
stack: the detection must vanish, D1 FAILS (rc = 1).  Outputs *_MUTATE.out / *_results_MUTATE.json.  (FP21_CACHE=<path.npz>
caches the streamed source columns outside the repository; FP21_DEV=1 cuts the randoms and validation lenses for
development only -- the committed outputs use neither.)

SCOPE.  A measurement: no action term and no chain constant enters.  No particle-mesh run; one process, < 15 min, ~4 GB.
Run from the repository root:  python3 real_research/derivation_chain_2026/FP21_isolated_spiral_lensing.py  (MUTATE=1)
"""
import os, sys, io, json, math, time, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
import healpy as hp
from astropy.io import fits
from scipy.spatial import cKDTree
from scipy.optimize import minimize_scalar, brentq
from scipy.stats import chi2 as chi2_dist, norm as norm_dist, f as f_dist
warnings.filterwarnings("ignore")
np.seterr(all="ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import FP18_kids_vs_hubble_flow_data as F18                                  # FP18's loaders, projection, T machinery (not run)

MUTATE = os.environ.get("MUTATE", "0") == "1"
DEV = os.environ.get("FP21_DEV", "0") == "1"
SLUG = "FP21_isolated_spiral_lensing"
RNG_SEED = 20260927

# ================================================================================================= files
DLR = os.path.join(REPO, "real_research", "data", "lensing_rar")
DDA = os.path.join(REPO, "real_research", "data")
F_SHEAR = os.path.join(DLR, "KiDS_DR4.1_SOM_gold_WL_cat.fits")
F_BRIGHT, F_LEPH = os.path.join(DLR, "KiDS_DR4_brightsample.fits"), os.path.join(DLR, "KiDS_DR4_brightsample_LePhare.fits")
F_LRL = os.path.join(DLR, "lr_lenses.npz")
F_2MPP = os.path.join(REPO, "gext_vectors_2026", "data", "raw", "2mpp_vizier.tsv")
F_2MRS = os.path.join(DDA, "2mrs_catalog.csv")
F_ALF = os.path.join(DDA, "alfalfa_sdss_durbala2020_t1.tsv")
F_FP6 = os.path.join(DDA, "fp_6dfgs_campbell2014.tsv")
F_UNGC = os.path.join(DDA, "ungc_karachentsev2013.tsv")
F_FP18J = os.path.join(HERE, "FP18_kids_vs_hubble_flow_data_results.json")
F_B21 = os.path.join(DLR, "brouwer2021_rar")

# ================================================================================================= constants
C_KMS, H0, OM = 299792.458, 70.0, F18.OM_W9                                      # B21's WMAP9, h70 units
G_PC = 4.30091e-3                                                                # G [pc (km/s)^2 / Msun]
SIGC = 4 * math.pi * G_PC / C_KMS ** 2 * 1e6                                     # Sigma_crit^-1 [pc^2/Msun] = SIGC D_l[Mpc] D_ls/D_s
MK_SUN, UPS_K = 3.28, F18.UPS_K
R_MIN, R_MAX, NF = 0.03, 3.0, 60
DLOGF = math.log(R_MAX / R_MIN) / NF
B21_BINS = [list(range(4 * b, 4 * b + 4)) for b in range(15)]                    # fine -> B21's 15 bins (same edges)
WIDE_B = [[0, 1, 2, 3], [4, 5, 6], [7, 8], [9, 10], [11, 12], [13, 14]]           # wide bins (groups of B21 bins) for T
WIDE = [sum((B21_BINS[b] for b in g), []) for g in WIDE_B]
BAND_B = [7, 8, 9, 10, 11, 12]                                                   # B21 bins 8-13: R 0.257-1.624 Mpc
BAND = sum((B21_BINS[b] for b in BAND_B), [])
DET = sum((B21_BINS[b] for b in range(13)), [])                                  # 0.03-1.624 Mpc (detection scalar)
EDGE15 = R_MIN * (R_MAX / R_MIN) ** (np.arange(16) / 15.0)
M_LO, M_HI, Z_MIN = 10.4, 10.8, 0.01
ISO_R, ISO_DV = 3.0, 500.0
UR_LATE, UR_EARLY = 2.35, 2.50
ZB_CUT, PZ_SIG, PZ_OUT = 0.2, 0.06, 0.10
NSIDE, NPH = 256, 20                                                             # footprint map; patches per KiDS region
N_RAND = 3000 if DEV else 12000
NVAL = 15000 if DEV else None
ZBE = np.array([0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.05, 0.06, 0.08, 0.13])   # random re-weighting bins
DIP_RA, DIP_DE, DIP_V = 167.942, -6.944, 369.82                                  # CMB dipole apex (Planck 2018), km/s
NACC = 12   # accumulators: 0 W, 1 S_t, 2 S_x, 3 V_t, 4 V_x, 5 S_R, 6 N, 7 S_f, 8 W(Z_B>0.5), 9 S_t(Z_B>0.5), 10 W(MASK=0), 11 S_t(MASK=0)
T_OK1, T_LIM1 = float(chi2_dist.isf(0.05, 1)), 9.0

# ================================================================================================= reporting
CH = []
OUT = {"lane": "FP21", "mutate": MUTATE, "dev": DEV, "checks": {}, "numbers": {}, "ledger": []}
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


# ================================================================================================= cosmology, catalogues
_ZG = np.linspace(0.0, 3.0, 30001)
_EZ = np.sqrt(OM * (1 + _ZG) ** 3 + 1 - OM)
_CHI = np.concatenate([[0.0], np.cumsum(0.5 * (1 / _EZ[1:] + 1 / _EZ[:-1]) * np.diff(_ZG))]) * C_KMS / H0


def chi_of(z):
    return np.interp(z, _ZG, _CHI)


def DA(z):
    return chi_of(z) / (1 + np.asarray(z))


def dL(z):
    return chi_of(z) * (1 + np.asarray(z))


def uvec(ra, dec):
    r, d = np.radians(ra), np.radians(dec)
    return np.c_[np.cos(d) * np.cos(r), np.cos(d) * np.sin(r), np.sin(d)]


def read_tsv(fn):
    rows = [l.rstrip("\n").split("\t") for l in open(fn) if l.strip() and not l.startswith("#")]
    hdr = [h.strip() for h in rows[0]]
    return hdr, [r for r in rows[3:] if len(r) == len(hdr)]


def tcol(hdr, data, key, f=float):
    i = hdr.index(key); out = []
    for r in data:
        try:
            out.append(f(r[i].strip()))
        except ValueError:
            out.append(np.nan)
    return np.array(out)


def bos_v(lms):
    return lms + np.log10(1 + 10 ** (-0.69 * lms + 6.63))                        # B21's M_gal = M* (1 + f_cold), Boselli


def load_sources():
    cache = os.environ.get("FP21_CACHE", "")
    if cache and os.path.exists(cache):
        z = np.load(cache)
        return {k: z[k] for k in z.files}
    with fits.open(F_SHEAR, memmap=True) as h:
        off = h.fileinfo(1)["datLoc"]; dt = h[1].data.dtype; n = int(h[1].header["NAXIS2"])
    mm = np.memmap(F_SHEAR, dtype=dt, mode="r", offset=off, shape=(n,))
    names = {"ra": "RAJ2000", "dec": "DECJ2000", "e1": "e1", "e2": "e2", "w": "weight", "zb": "Z_B", "mask": "MASK"}
    out = {k: np.empty(n, dtype=("f8" if k in ("ra", "dec") else ("i4" if k == "mask" else "f4"))) for k in names}
    for i0 in range(0, n, 1_000_000):
        blk = np.array(mm[i0:i0 + 1_000_000])
        for k, c in names.items():
            out[k][i0:i0 + 1_000_000] = blk[c]
    del mm
    if cache:
        np.savez(cache, **out)
    return out


# ================================================================================================= photo-z dilution model
def dilution_table(zb_all, w_all):
    """f(z_l, Z_B) = <Sigma_crit^-1(z_true)>_{p(z|Z_B)} / Sigma_crit^-1(Z_B); p = 0.9 Gaussian(0.06(1+Z_B)) + 0.1 n_all."""
    zlg = np.arange(0.0, 0.7001, 0.002); zbg = np.round(np.arange(0.10, 1.2001, 0.01), 2)
    zt = np.linspace(0.0, 3.0, 3001); chit = chi_of(zt)
    h, _ = np.histogram(zb_all, bins=np.append(zbg - 0.005, zbg[-1] + 0.005), weights=w_all)
    G = np.array([np.exp(-0.5 * ((zt - zb) / (PZ_SIG * (1 + zb))) ** 2) for zb in zbg])
    G /= np.trapz(G, zt, axis=1)[:, None]
    nall = (h[:, None] * G).sum(0); nall /= np.trapz(nall, zt)
    Pz = (1 - PZ_OUT) * G + PZ_OUT * nall[None, :]
    F = np.ones((len(zlg), len(zbg)))
    for i, zl in enumerate(zlg):
        chl = float(chi_of(zl)); eff = np.where(chit > chl, 1 - chl / np.maximum(chit, 1e-9), 0.0)
        pt = np.where(chi_of(zbg) > chl, 1 - chl / chi_of(zbg), 0.0)
        num = np.trapz(Pz * eff[None, :], zt, axis=1)
        F[i] = np.where(pt > 0, num / np.where(pt > 0, pt, 1.0), 1.0)
    return zlg, zbg, F


# ================================================================================================= the stacker
def stack(SRC, ra_l, dec_l, z_l, slot=None, nslot=None, label=""):
    """per-object (slot None) or per-slot accumulators (NACC, NF) of the tangential-shear estimator; all pairs in 0.03-3 Mpc."""
    n = len(ra_l); acc = np.zeros(((n if slot is None else nslot), NACC, NF))
    lr, ld = np.radians(np.asarray(ra_l, float)), np.radians(np.asarray(dec_l, float))
    tree, zb, FT = SRC["tree"], SRC["zb"], SRC["FTAB"]
    t1 = time.time()
    for i in range(n):
        zl = float(z_l[i]); chl = float(chi_of(zl)); Dl = chl / (1 + zl); th = min(R_MAX / Dl, 3.0)
        cl_, sl_ = math.cos(ld[i]), math.sin(ld[i])
        idx = np.asarray(tree.query_ball_point((cl_ * math.cos(lr[i]), cl_ * math.sin(lr[i]), sl_), 2 * math.sin(th / 2)), dtype=np.int64)
        if idx.size == 0:
            continue
        idx = idx[zb[idx] > zl + ZB_CUT]
        if idx.size == 0:
            continue
        da = SRC["rar"][idx] - lr[i]; cd = SRC["cdec"][idx]; sd = SRC["sdec"][idx]
        hav = np.sin(0.5 * (SRC["decr"][idx] - ld[i])) ** 2 + cl_ * cd * np.sin(0.5 * da) ** 2
        R = Dl * 2 * np.arcsin(np.sqrt(np.clip(hav, 0.0, 1.0)))
        k = np.floor(np.log(np.maximum(R, 1e-12) / R_MIN) / DLOGF).astype(np.int64)
        ok = (k >= 0) & (k < NF) & (R > 0)
        if not ok.any():
            continue
        idx, R, k, da, cd, sd = idx[ok], R[ok], k[ok], da[ok], cd[ok], sd[ok]
        pa = np.arctan2(np.sin(da) * cd, cl_ * sd - sl_ * cd * np.cos(da))
        c2, s2 = np.cos(2 * pa), np.sin(2 * pa)
        e1 = SRC["e1"][idx].astype(np.float64); e2 = SRC["e2"][idx].astype(np.float64)
        et = e1 * c2 + e2 * s2; ex = -e1 * s2 + e2 * c2
        isc = SIGC * Dl * np.clip(1 - chl / SRC["chis"][idx], 0.0, None)
        g = isc > 0
        if not g.all():
            idx, R, k, et, ex, isc = idx[g], R[g], k[g], et[g], ex[g], isc[g]
        ws = SRC["w"][idx].astype(np.float64); wl = ws * isc ** 2; sc = 1.0 / isc
        izl = min(int(round(zl / 0.002)), FT.shape[0] - 1)
        fd = FT[izl][np.clip(np.rint((zb[idx] - 0.10) / 0.01).astype(np.int64), 0, FT.shape[1] - 1)]
        hi = zb[idx] > 0.5; m0 = SRC["mask"][idx] == 0
        a = acc[i if slot is None else slot[i]]
        wse, wsx = wl * sc * et, wl * sc * ex
        a[0] += np.bincount(k, wl, NF); a[1] += np.bincount(k, wse, NF); a[2] += np.bincount(k, wsx, NF)
        a[3] += np.bincount(k, wse ** 2, NF); a[4] += np.bincount(k, wsx ** 2, NF); a[5] += np.bincount(k, wl * R, NF)
        a[6] += np.bincount(k, None, NF); a[7] += np.bincount(k, wl * fd, NF)
        a[8] += np.bincount(k[hi], wl[hi], NF); a[9] += np.bincount(k[hi], wse[hi], NF)
        a[10] += np.bincount(k[m0], wl[m0], NF); a[11] += np.bincount(k[m0], wse[m0], NF)
    P(f"    stacked {label}: {n:,} centres in {time.time() - t1:.0f} s")
    return acc


# ================================================================================================= the estimator
ONEPK = None                                                                     # B21's (1+K), read in main()


def est(L, nL, Rr, groups, cols=(0, 1), fcol=7, boost="max1", dil=True):
    """corrected, random-subtracted Delta Sigma per group of fine bins.  L: summed lens accumulators; Rr: per-lens-equivalent
    random sums (z re-weighted); boost applied per fine bin to the lens signal."""
    WL, SL, WR, SR = L[cols[0]], L[cols[1]], Rr[cols[0]], Rr[cols[1]]
    B = (WL / max(nL, 1)) / np.where(WR > 0, WR, np.nan); B = np.nan_to_num(B, nan=1.0)
    Bu = np.ones(NF) if boost == "none" else (B if boost == "raw" else np.maximum(B, 1.0))
    out = []
    for g in groups:
        wl, wr = WL[g].sum(), WR[g].sum()
        if wl <= 0 or wr <= 0:
            out.append(np.nan); continue
        dl, dr = (Bu[g] * SL[g]).sum() / wl, SR[g].sum() / wr
        if dil:
            dl /= L[fcol][g].sum() / wl; dr /= Rr[fcol][g].sum() / wr
        out.append((dl - dr) / ONEPK)
    return np.array(out)


class Sample:
    """a lens sample: per-object accumulators + patches + redshifts, with randoms per (patch, z-bin)."""

    def __init__(self, A, patch, z, AR, NRz):
        self.A, self.patch, self.z, self.AR, self.NRz = A, patch, z, AR, NRz
        self.zi = np.clip(np.searchsorted(ZBE, z, side="right") - 1, 0, len(ZBE) - 2)

    def sums(self, excl=None):
        keep = np.ones(len(self.z), bool) if excl is None else self.patch != excl
        L = self.A[keep].sum(0); nL = int(keep.sum())
        hz = np.bincount(self.zi[keep], minlength=len(ZBE) - 1).astype(float); hz /= max(hz.sum(), 1)
        ARk = self.AR.sum(0) - (0 if excl is None else self.AR[excl]); NRk = self.NRz.sum(0) - (0 if excl is None else self.NRz[excl])
        Rr = sum(hz[j] * ARk[j] / NRk[j] for j in range(len(hz)) if hz[j] > 0 and NRk[j] > 0)
        return L, nL, Rr

    def profile(self, groups, **kw):
        L, nL, Rr = self.sums()
        full = est(L, nL, Rr, groups, **kw)
        pts = np.unique(self.patch); loo = np.array([est(*self.sums(k), groups, **kw) for k in pts])
        n = len(pts); C = (n - 1) / n * (loo - loo.mean(0)).T @ (loo - loo.mean(0))
        return full, C, n

    def shape_noise(self, groups, cols=(0, 3)):
        L = self.A.sum(0)
        return np.array([math.sqrt(L[cols[1]][g].sum()) / L[cols[0]][g].sum() / ONEPK if L[cols[0]][g].sum() > 0 else np.nan for g in groups])

    def meanR(self, groups):
        L = self.A.sum(0)
        return np.array([L[5][g].sum() / L[0][g].sum() for g in groups])

    def weights(self, groups):
        L = self.A.sum(0)
        return np.array([L[0][g].sum() for g in groups])


class PatchSample(Sample):
    """a sample accumulated per patch (validation lenses), with its own randoms per patch (same z distribution)."""

    def __init__(self, AP, nP, ARP, nRP):
        self.AP, self.nP, self.ARP, self.nRP = AP, nP, ARP, nRP

    def sums(self, excl=None):
        keep = np.ones(len(self.nP), bool)
        if excl is not None:
            keep[excl] = False
        L = self.AP[keep].sum(0); nL = int(self.nP[keep].sum()); Rr = self.ARP[keep].sum(0) / max(self.nRP[keep].sum(), 1)
        return L, nL, Rr

    def profile(self, groups, **kw):
        L, nL, Rr = self.sums()
        full = est(L, nL, Rr, groups, **kw)
        pts = np.where(self.nP > 0)[0]; loo = np.array([est(*self.sums(k), groups, **kw) for k in pts])
        n = len(pts); C = (n - 1) / n * (loo - loo.mean(0)).T @ (loo - loo.mean(0))
        return full, C, n

    def shape_noise(self, groups, cols=(0, 3)):
        L = self.AP.sum(0)
        return np.array([math.sqrt(L[cols[1]][g].sum()) / L[cols[0]][g].sum() / ONEPK for g in groups])

    def meanR(self, groups):
        L = self.AP.sum(0)
        return np.array([L[5][g].sum() / L[0][g].sum() for g in groups])


def hartlap(n, p):
    return (n - p - 2) / (n - 1) if n > p + 2 else float("nan")


def chi2_zero(d, C, n):
    h = hartlap(n, len(d))
    return float(h * d @ np.linalg.solve(C, d)), h


def hotelling(d, C, n):
    """null test of d = 0 with a jackknife covariance C (= S/n for n resamples): T^2 = d C^-1 d, (n - p)/(p (n - 1)) T^2 ~ F(p, n - p)."""
    p = len(d)
    if n <= p:
        return float("nan"), float("nan")
    T2 = float(d @ np.linalg.solve(C, d))
    return T2, float(f_dist.sf((n - p) / (p * (n - 1)) * T2, p, n - p))


def amp_gls(d, C, t, Ct):
    """GLS amplitude of d against the template t (covariances C, Ct), iterated as FP18's amp()."""
    a = 1.0
    for _ in range(60):
        Ci = np.linalg.inv(C + a * a * Ct); an = float(t @ Ci @ d / (t @ Ci @ t))
        if abs(an - a) < 1e-10:
            break
        a = an
    return a, float(1 / math.sqrt(t @ np.linalg.inv(C + a * a * Ct) @ t))


# ================================================================================================= the free-profile statistic
def T_free_K(d, C, K, R0, sR, lc=0.0, lsz=0.0, full=True):
    """FP18's T_free with an arbitrary kernel K (n_data x FP18.EC shells): min_{m >= 0, R0t} [chi2(m) + ((R0t - R0)/sR)^2] - min chi2."""
    W = np.linalg.inv(np.linalg.cholesky(C)); A = W @ K; y = W @ d
    m0 = F18.bvls(A, y); c0 = float(np.sum((A @ m0 - y) ** 2)); EC = F18.EC

    def relaxed(Rt):
        f = F18.frac_in(Rt, EC); Mt = F18.target_exc(Rt, lc, lsz)
        if f @ m0 <= Mt:
            return c0, m0
        m = F18.bvls(np.vstack([A, 1e3 * f / Mt]), np.concatenate([y, [1e3]]))
        return float(np.sum((A @ m - y) ** 2)), m
    grid = np.geomspace(max(0.3, R0 - 4 * sR) * 0.9, max(R0 + 6 * sR, 1.2 * R0) * 1.6, 44)
    rel = [(c - c0 + ((Rt - R0) / sR) ** 2, Rt, c - c0, m) for Rt in grid for c, m in [relaxed(Rt)]]
    j = int(np.argmin([r_[0] for r_ in rel])); Tr, Rtr, dkr, mr = rel[j]
    out = dict(T=Tr, R0t=Rtr, dK=dkr, c0=c0, relaxed=True)
    if full:
        cache = {}

        def ffull(Rt):
            c, m, v = F18.qp_full(A, y, Rt, lc, lsz, relaxed(Rt)[1]); cache[Rt] = (c, m, v)
            return c - c0 + ((Rt - R0) / sR) ** 2
        pts = np.unique(np.concatenate([grid[::4], np.geomspace(grid[max(j - 3, 0)], grid[min(j + 8, len(grid) - 1)], 9)]))
        vals = [ffull(Rt) for Rt in pts]; k = int(np.argmin(vals))
        a_, b_ = pts[max(k - 1, 0)], pts[min(k + 1, len(pts) - 1)]
        rr = minimize_scalar(ffull, bounds=(a_, b_), method="bounded", options=dict(xatol=2e-3))
        Tf, Rtf = (rr.fun, rr.x) if rr.fun < vals[k] else (vals[k], pts[k])
        c, m, v = cache.get(Rtf, F18.qp_full(A, y, Rtf, lc, lsz, relaxed(Rtf)[1]))
        out.update(T=max(Tf, Tr), R0t=Rtf, dK=c - c0, relaxed=False, T_relaxed=Tr, viol=v)
    return out


# ================================================================================================= main
def main():
    global ONEPK
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: every 2M++ lens is moved to a random footprint position before the stack; D1 must FAIL ***")
    if DEV:
        P("\n  *** FP21_DEV=1: reduced randoms / validation lenses (development only) ***")
    rng = np.random.default_rng(RNG_SEED)
    # m-bias: B21's released (1+K)
    b21f = np.genfromtxt(os.path.join(F_B21, "Fig-3_Lensing-rotation-curves_Massbin-3.txt"), comments="#")
    ONEPK = float(b21f[0, 4]); assert np.allclose(b21f[:, 4], ONEPK)
    F18J = json.load(open(F_FP18J))["numbers"]
    HON = F18J["E"]["honest"]
    cf = [M / F18.M6["lg_R0"](lambda r, a, M=M: M * 1e12 * F18.LGM + 0.0 * r) ** 3 for M in (0.5, 1.57, 5.0)]
    F18.COEF_SI = float(np.mean(cf))                                             # FP18 K3's integrator value

    # ============================================================================================= sources
    banner("A  THE DATA: sources, footprint, corrections' inputs")
    SRC = load_sources(); NS_ = len(SRC["ra"])
    P(f"    sources: {NS_:,} (KiDS-1000 SOM-gold)  {el()}")
    reg = (SRC["dec"] < -15).astype(np.int8); tb = np.digitize(SRC["zb"], [0.3, 0.5, 0.7, 0.9]); CC = {}
    for r_ in (0, 1):
        for t_ in range(5):
            s = (reg == r_) & (tb == t_)
            c1 = float(np.average(SRC["e1"][s], weights=SRC["w"][s])); c2 = float(np.average(SRC["e2"][s], weights=SRC["w"][s]))
            SRC["e1"][s] -= c1; SRC["e2"][s] -= c2; CC[f"{'NS'[r_]}{t_ + 1}"] = (c1, c2)
    del reg, tb
    pix = hp.ang2pix(NSIDE, SRC["ra"], SRC["dec"], lonlat=True); cnt = np.bincount(pix, minlength=hp.nside2npix(NSIDE)); del pix
    GOOD = cnt > 0.3 * np.median(cnt[cnt > 0]); AREA = float(GOOD.sum() * hp.nside2pixarea(NSIDE, degrees=True))
    gp = np.where(GOOD)[0]; gra, gde = hp.pix2ang(NSIDE, gp, lonlat=True); south = gde < -15
    gru = np.where(south, (gra + 180.0) % 360.0, gra); PQ = {}
    for s_, m in ((0, ~south), (1, south)):
        q = np.quantile(gru[m], np.linspace(0, 1, NPH + 1)); q[0] -= 1e-6; q[-1] += 1e-6; PQ[s_] = q

    def patch_of(ra_, dec_):
        ra_, dec_ = np.atleast_1d(ra_), np.atleast_1d(dec_); s_ = (dec_ < -15).astype(int)
        ru = np.where(s_ == 1, (ra_ + 180.0) % 360.0, ra_); out = np.empty(len(ra_), dtype=np.int64)
        for k_ in (0, 1):
            m = s_ == k_
            out[m] = k_ * NPH + np.clip(np.searchsorted(PQ[k_], ru[m], side="right") - 1, 0, NPH - 1)
        return out

    def rand_pos(n, rs):
        ras, des, got = [], [], 0
        lo, hi_ = math.sin(math.radians(-40.0)), math.sin(math.radians(6.0))
        while got < n:
            ra_ = rs.uniform(0, 360, 400000); de_ = np.degrees(np.arcsin(rs.uniform(lo, hi_, 400000)))
            ok = GOOD[hp.ang2pix(NSIDE, ra_, de_, lonlat=True)]; ras.append(ra_[ok]); des.append(de_[ok]); got += int(ok.sum())
        return np.concatenate(ras)[:n], np.concatenate(des)[:n]
    SRC["rar"] = np.radians(SRC["ra"]); SRC["decr"] = np.radians(SRC["dec"]); SRC["cdec"] = np.cos(SRC["decr"]); SRC["sdec"] = np.sin(SRC["decr"])
    SRC["chis"] = chi_of(SRC["zb"].astype(np.float64))
    SRC["tree"] = cKDTree(np.c_[SRC["cdec"] * np.cos(SRC["rar"]), SRC["cdec"] * np.sin(SRC["rar"]), SRC["sdec"]])
    zlg, zbg, FTAB = dilution_table(SRC["zb"], SRC["w"]); SRC["FTAB"] = FTAB
    P(f"    footprint (HEALPix {NSIDE}, > 30% of median source density): {AREA:.0f} deg^2; c-terms subtracted: "
      + ", ".join(f"{k_} ({v[0]:+.1e}, {v[1]:+.1e})" for k_, v in CC.items()))
    P(f"    m-correction: B21's (1+K) = {ONEPK:.5f}; photo-z dilution model f(z_l, Z_B) at Z_B = 0.3 / 0.7: z_l 0.026 -> "
      f"{FTAB[13, 20]:.4f} / {FTAB[13, 60]:.4f}; z_l 0.30 -> {FTAB[150, 50]:.4f} (Z_B 0.6) / {FTAB[150, 60]:.4f}  {el()}")

    # ============================================================================================= the 2M++ lens catalogue
    h_, d_ = read_tsv(F_2MPP)
    K2 = tcol(h_, d_, "Ksmag"); V = tcol(h_, d_, "Vcmb"); c125 = tcol(h_, d_, "c12.5"); M1 = tcol(h_, d_, "M1"); M2 = tcol(h_, d_, "M2")
    RA = tcol(h_, d_, "_RA"); DE = tcol(h_, d_, "_DE"); REF = np.array([r[h_.index("Ref")].strip() for r in d_])
    okc = np.isfinite(K2) & np.isfinite(V) & np.isfinite(RA) & np.isfinite(DE)
    K2, V, c125, M1, M2, RA, DE, REF = K2[okc], V[okc], c125[okc], M1[okc], M2[okc], RA[okc], DE[okc], REF[okc]
    X2 = uvec(RA, DE); T2 = cKDTree(X2)
    m2 = np.genfromtxt(F_2MRS, delimiter=",", names=True)
    dd2, jj2 = cKDTree(uvec(m2["RAJ2000"], m2["DEJ2000"])).query(X2); in2 = dd2 < np.radians(5 / 3600)
    dk = K2[in2] - m2["Ktmag"][jj2[in2]]; kk = K2[in2]
    kbe = np.arange(6.0, 11.76, 0.25); kbc, kbm = [], []
    for a_ in kbe[:-1]:
        s = (kk >= a_) & (kk < a_ + 0.25)
        if s.sum() >= 30:
            kbc.append(a_ + 0.125); kbm.append(float(np.median(dk[s])))
    KOFF_FAINT = float(np.median(dk[(kk >= 11.0) & (kk < 11.75)]))
    koff = lambda k: np.where(k > 11.75, KOFF_FAINT, np.interp(k, kbc, kbm))
    KT = K2 - koff(K2); KT[in2] = m2["Ktmag"][jj2[in2]]
    Z = V / C_KMS
    MKa = KT - 5 * np.log10(np.maximum(dL(np.maximum(Z, 1e-4)), 1e-3) * 1e5) + 6.0 * np.log10(1 + np.maximum(Z, 0))
    LMS = 0.4 * (MK_SUN - MKa) + math.log10(UPS_K); LMG = bos_v(LMS)
    inF = GOOD[hp.ang2pix(NSIDE, RA, DE, lonlat=True)]
    CAND = np.where(inF & (Z >= Z_MIN))[0]                                        # lens candidates (all masses)
    NCAND = len(CAND)
    # ---- type labels
    ha, da_ = read_tsv(F_ALF); ara, ade, av = tcol(ha, da_, "RAJ2000"), tcol(ha, da_, "DEJ2000"), tcol(ha, da_, "RVel")
    okA = np.isfinite(ara) & np.isfinite(ade) & np.isfinite(av); ara, ade, av = ara[okA], ade[okA], av[okA]
    cosd = uvec(RA, DE) @ uvec(np.array([DIP_RA]), np.array([DIP_DE]))[0]; VH = V - DIP_V * cosd
    dA_, jA = cKDTree(uvec(ara, ade)).query(X2); HI = (dA_ < np.radians(30 / 3600)) & (np.abs(av[jA] - VH) <= 300)
    hf, df_ = read_tsv(F_FP6); fra, fde, fcz = tcol(hf, df_, "RAJ2000"), tcol(hf, df_, "DEJ2000"), tcol(hf, df_, "cz")
    FP_HOURS = bool(np.nanmax(fra) <= 24.0)
    if FP_HOURS:
        fra = fra * 15.0
    dF_, jF = cKDTree(uvec(fra, fde)).query(X2); FPE = (dF_ < np.radians(10 / 3600)) & (np.abs(fcz[jF] - V) <= 300)
    with fits.open(F_BRIGHT) as hb, fits.open(F_LEPH) as hl:
        bra, bde = np.array(hb[1].data["RAJ2000"], float), np.array(hb[1].data["DECJ2000"], float)
        bur = np.array(hl[1].data["MAG_ABS_u"], float) - np.array(hl[1].data["MAG_ABS_r"], float)
    dB, jB = cKDTree(uvec(bra, bde)).query(X2[CAND]); UR = np.full(len(RA), np.nan)
    mB = dB < np.radians(5 / 3600); UR[CAND[mB]] = bur[jB[mB]]; del bra, bde, bur
    hasc = np.isfinite(UR)
    LATE = (HI & ~FPE) | (~HI & ~FPE & hasc & (UR < UR_LATE))
    EARLY = (FPE & ~HI) | (~HI & ~FPE & hasc & (UR >= UR_EARLY))

    # ---- isolation
    def isolation(ii, Rp, dV, mode="cyl"):
        flag = np.ones(len(ii), bool); nb = np.zeros(len(ii), int)
        for n_, i in enumerate(ii):
            Da = float(DA(Z[i])); th = Rp / Da
            js = np.asarray(T2.query_ball_point(X2[i], 2 * math.sin(th / 2)), dtype=np.int64); js = js[js != i]
            dv = np.abs(V[js] - V[i])
            if mode == "cyl":
                mm = dv <= dV
            else:
                rp = Da * np.arccos(np.clip(X2[js] @ X2[i], -1, 1)); mm = np.hypot(rp, dv / H0) <= Rp
            nb[n_] = int(np.sum(KT[js[mm]] < KT[i])); flag[n_] = nb[n_] == 0
        return flag, nb
    ISO = {}
    for key, (Rp, dV, mode) in {"3Mpc/500": (3.0, 500.0, "cyl"), "3Mpc sphere": (3.0, 0.0, "sph"), "3Mpc/1000": (3.0, 1000.0, "cyl"),
                                "3Mpc/2000": (3.0, 2000.0, "cyl"), "1.5Mpc/500": (1.5, 500.0, "cyl"), "1Mpc/500": (1.0, 500.0, "cyl")}.items():
        ISO[key] = isolation(CAND, Rp, dV, mode)
    P(f"    2M++: {len(RA):,} rows; in the footprint with z >= {Z_MIN}: {NCAND:,}; K offset (2MRS matches {in2.sum():,}): "
      f"{', '.join(f'{c_:.2f}:{m_:+.3f}' for c_, m_ in zip(kbc[::3], kbm[::3]))}; K2M++ > 11.75: {KOFF_FAINT:+.3f}  {el()}")

    # ============================================================================================= the stacks
    banner("B  THE STACKS (per-lens accumulators; randoms per patch x redshift bin; the photometric validation sample)")
    lra, lde, lz = RA[CAND].copy(), DE[CAND].copy(), Z[CAND]
    if MUTATE:
        lra, lde = rand_pos(NCAND, np.random.default_rng(RNG_SEED + 99))
    A_L = stack(SRC, lra, lde, lz, label="2M++ lens candidates" + (" (MUTATED positions)" if MUTATE else ""))
    PL = patch_of(lra, lde)
    rra, rde = rand_pos(N_RAND, rng); rz = rng.choice(lz, N_RAND)
    rp_ = patch_of(rra, rde); rzi = np.clip(np.searchsorted(ZBE, rz, side="right") - 1, 0, len(ZBE) - 2)
    slot = rp_ * (len(ZBE) - 1) + rzi
    A_R = stack(SRC, rra, rde, rz, slot=slot, nslot=2 * NPH * (len(ZBE) - 1), label="randoms").reshape(2 * NPH, len(ZBE) - 1, NACC, NF)
    NRz = np.bincount(slot, minlength=2 * NPH * (len(ZBE) - 1)).reshape(2 * NPH, len(ZBE) - 1).astype(float)
    LRL = np.load(F_LRL); VAL = {}
    for b_, (lo, hi_) in ((2, (10.3, 10.6)), (3, (10.6, 10.8))):
        s = np.where((LRL["logM"] >= lo) & (LRL["logM"] < hi_))[0]
        if NVAL:
            s = rng.choice(s, NVAL, replace=False)
        vra, vde, vz = LRL["ra"][s], LRL["dec"][s], LRL["z"][s]; vp = patch_of(vra, vde)
        AV = stack(SRC, vra, vde, vz, slot=vp, nslot=2 * NPH, label=f"B21-bin-{b_} photometric lenses")
        wra, wde = rand_pos(len(s), rng); wz = rng.choice(vz, len(s)); wp = patch_of(wra, wde)
        AVR = stack(SRC, wra, wde, wz, slot=wp, nslot=2 * NPH, label=f"bin-{b_} randoms")
        VAL[b_] = PatchSample(AV, np.bincount(vp, minlength=2 * NPH).astype(float), AVR, np.bincount(wp, minlength=2 * NPH).astype(float))
        VAL[b_].n = len(s); VAL[b_].lmg = float(np.log10(np.mean(LRL["Mgal"][s])))
    P(f"    {el()}")

    def sample(mask):
        ii = np.where(mask)[0]
        return Sample(A_L[ii], PL[ii], lz[ii], A_R, NRz), ii

    # ============================================================================================= K controls
    banner("K  CONTROLS: sources and the null, the projection, the T machinery, the mass scale, randoms, the pipeline vs B21")
    ALL, _ = sample(np.ones(NCAND, bool))
    x15, Cx15, nx = ALL.profile(B21_BINS, cols=(0, 2)); cx, hx = chi2_zero(x15, Cx15, nx); T2x, px = hotelling(x15, Cx15, nx)
    maxc = max(max(abs(v[0]), abs(v[1])) for v in CC.values())
    check("K1 CONTROL: the source catalogue and the cross-shear null -- 21,262,011 SOM-gold sources, additive terms small, and the "
          "45-degree (cross) Delta Sigma_x of the full 2M++ footprint stack consistent with zero (jackknife, Hartlap)",
          f"N = {NS_:,}; max |c| = {maxc:.1e}; cross Hotelling T^2 = {T2x:.1f} (15 bins, {nx} patches), p = {px:.3f} (Hartlap chi2 "
          f"{cx:.1f}/15, p {float(chi2_dist.sf(cx, 15)):.3f}); Delta Sigma_x: " + ", ".join(f"{v:+.2f}" for v in x15),
          NS_ == 21262011 and maxc < 2e-3 and px > 1e-3)
    dev = []
    for M200, c in ((0.5, 8.0), (3.0, 4.0), (10.0, 2.0)):
        dev.append(float(np.max(np.abs(F18.esd_of(F18.nfw_Mcum(M200, c, 0.0)) / F18.nfw_ds(F18.RD, M200, c) - 1))))
    ksis = 200.0 ** 2 / (F18.G_KMS * 1e12)
    dsis = float(np.max(np.abs(F18.esd_of(lambda r: ksis * np.minimum(np.asarray(r, float), 30.0)) / (ksis / (4 * F18.RD)) - 1)))
    check("K2 CONTROL: the projection -- FP18's uniform-shell kernel (used for every envelope and T here) reproduces the analytic "
          "NFW Delta Sigma (Wright & Brainerd 2000) and the SIS V^2/(4 G R) at B21's radii; FP6's esd_of_M is not used",
          f"NFW max dev {max(dev):.2e}; SIS max dev {dsis:.2e}", max(dev) < 0.01 and dsis < 0.01)
    tst = F18J["matching"]["targets"]["i"]["stack"]
    dS, CS, _ = F18.kids_for([tuple(t) for t in tst])
    Tf18 = F18.T_free(dS, CS, 0.93, HON["stack"], full=True); Tmine = T_free_K(dS, CS, F18.KC, 0.93, HON["stack"], full=True)
    Tcom = F18J["F1"]["stack/i"]["honest"]["T"]
    check("K3 CONTROL: this lane's free-profile T (any kernel) reproduces FP18's T_free on FP18's own stack input (B21 at the stack's "
          "M_gal, R0 0.93 +- 0.117, full definition) and FP18's committed value",
          f"T = {Tmine['T']:.4f} (this lane) vs {Tf18['T']:.4f} (FP18's function) vs {Tcom:.4f} (FP18 committed)",
          abs(Tmine["T"] - Tf18["T"]) < 1e-6 * max(1.0, Tf18["T"]) and abs(Tmine["T"] - Tcom) < 0.5)
    hu, du = read_tsv(F_UNGC); uK, uD, uL = tcol(hu, du, "Kmag"), tcol(hu, du, "Dist"), tcol(hu, du, "KLum")
    ou = np.isfinite(uK) & np.isfinite(uD) & np.isfinite(uL) & (uD > 0)
    dlu = 0.4 * (MK_SUN - (uK[ou] - 5 * np.log10(uD[ou] * 1e5))) - uL[ou]
    check("K4 CONTROL: the mass scale -- the L_K formula used for the lenses (M_K,sun = 3.28) reproduces UNGC's own log L_K (the "
          "source of K&K's LV-central masses, FP18 mapping (i)); the 2M++ isophotal Ks is put on 2MRS's total-magnitude system",
          f"UNGC: n = {ou.sum()}, median d = {np.median(dlu):+.4f} dex, MAD {np.median(np.abs(dlu - np.median(dlu))):.4f}; 2M++ - 2MRS "
          f"total: {np.median(dk):+.3f} mag overall ({in2.sum():,} matches), calibrated per 0.25 mag for K2M++ <= 11.75",
          abs(np.median(dlu)) < 0.02)
    Rr_all = sum(A_R[:, j].sum(0) / NRz[:, j].sum() for j in range(len(ZBE) - 1) if NRz[:, j].sum() > 0) / (len(ZBE) - 1)
    rloo, rpts = [], np.unique(rp_)
    for k_ in rpts:
        ARk = A_R.sum(0) - A_R[k_]; NRk = NRz.sum(0) - NRz[k_]
        Rk = sum(ARk[j] / NRk[j] for j in range(len(ZBE) - 1) if NRk[j] > 0) / (len(ZBE) - 1)
        rloo.append([Rk[1][g].sum() / Rk[0][g].sum() / ONEPK for g in B21_BINS])
    rloo = np.array(rloo); nr_ = len(rpts); Cr = (nr_ - 1) / nr_ * (rloo - rloo.mean(0)).T @ (rloo - rloo.mean(0))
    r15 = np.array([Rr_all[1][g].sum() / Rr_all[0][g].sum() / ONEPK for g in B21_BINS])
    cr, hr = chi2_zero(r15, Cr, nr_); T2r, pr = hotelling(r15, Cr, nr_)
    check("K5 CONTROL: random points -- the Delta Sigma around 12,000 random footprint points (redshifts from the lenses) is "
          "consistent with zero (jackknife, Hartlap); it is subtracted from every lens profile",
          f"Hotelling T^2 = {T2r:.1f} (15 bins, {nr_} patches), p = {pr:.3f} (Hartlap chi2 {cr:.1f}/15); values at 0.3-1.4 Mpc: "
          + ", ".join(f"{v:+.2f} +- {math.sqrt(Cr[i, i]):.2f}" for i, v in enumerate(r15) if 7 <= i <= 12),
          pr > 1e-3)
    VR = {}
    for b_ in (2, 3):
        Bd = np.genfromtxt(os.path.join(F_B21, f"Fig-3_Lensing-rotation-curves_Massbin-{b_}.txt"), comments="#")
        bd = Bd[:, 1] / Bd[:, 4]; Cb = F18.C60[(b_ - 1) * 15:b_ * 15, (b_ - 1) * 15:b_ * 15]
        dv_, Cv_, nv_ = VAL[b_].profile(B21_BINS, boost="none"); a_, sa_ = amp_gls(dv_, Cv_ / hartlap(nv_, 15), bd, Cb)
        dvn, Cvn, _ = VAL[b_].profile(B21_BINS, boost="none", dil=False); an_, _ = amp_gls(dvn, Cvn / hartlap(nv_, 15), bd, Cb)
        dvb, Cvb, _ = VAL[b_].profile(B21_BINS); ab_, sab_ = amp_gls(dvb, Cvb / hartlap(nv_, 15), bd, Cb)
        rr_ = dv_ - bd; c2v = float(rr_ @ np.linalg.solve(Cv_ / hartlap(nv_, 15) + Cb, rr_))
        f15, nf_, rf_ = VAL[b_].sums(); fdl = np.array([f15[7][g].sum() / f15[0][g].sum() for g in B21_BINS])
        bst = np.array([(f15[0][g].sum() / nf_) / rf_[0][g].sum() for g in B21_BINS])
        inn = np.arange(15) < 7; wi = 1 / np.diag(Cb)
        a_in = [float(np.sum((wi * x_ * bd)[m_]) / np.sum((wi * bd * bd)[m_])) for x_ in (dv_, dvb) for m_ in (inn, ~inn)]
        VR[b_] = dict(A=a_, sA=sa_, A_nodil=an_, A_boost=ab_, sA_boost=sab_, chi2=c2v, p=float(chi2_dist.sf(c2v, 15)), n=VAL[b_].n,
                      lmg=VAL[b_].lmg, d=dv_, err=np.sqrt(np.diag(Cv_)), b21=bd, b21e=np.sqrt(np.diag(Cb)), fdil=fdl, npatch=nv_,
                      boost=bst, split=a_in)
    for b_ in (2, 3):
        v_ = VR[b_]
        P(f"    B21 bin {b_} (record's reconstruction, {v_['n']:,} lenses, log <M_gal> {v_['lmg']:.2f}): R | this pipeline +- jk | B21 +- err")
        P("      " + " | ".join(f"{F18.RD[i]:.2f}: {v_['d'][i]:5.1f}+-{v_['err'][i]:4.1f} / {v_['b21'][i]:5.1f}+-{v_['b21e'][i]:3.1f}" for i in range(0, 15, 2)))
        P(f"      amplitude (B21's convention: no boost) {v_['A']:.3f} +- {v_['sA']:.3f} (point-Z_B, no dilution correction: {v_['A_nodil']:.3f}); "
          f"chi2 vs B21 (summed covariances, lenient: the same sources) {v_['chi2']:.1f}/15, p {v_['p']:.2f}; mean dilution factor "
          f"{np.mean(v_['fdil']):.3f}; with the measured boost {v_['A_boost']:.3f} +- {v_['sA_boost']:.3f}")
    check("K6 CONTROL: the pipeline with B21's convention (c, m, dilution model, randoms subtracted; no boost correction) reproduces "
          "B21's published Fig-3 Delta Sigma(R) of mass bins 2 and 3 from the record's photometric reconstruction of B21's isolated "
          "lenses: amplitude within [0.80, 1.20]",
          f"bin 2: {VR[2]['A']:.3f} +- {VR[2]['sA']:.3f}; bin 3: {VR[3]['A']:.3f} +- {VR[3]['sA']:.3f} (without the dilution model "
          f"{VR[2]['A_nodil']:.3f} / {VR[3]['A_nodil']:.3f})", all(0.80 <= VR[b_]["A"] <= 1.20 for b_ in (2, 3)))
    check("K6b (reported) K6 AS FIRST DECLARED, with the measured boost applied: fails for bin 3; the excess is inside 0.3 Mpc, where "
          "the boost against uniform randoms is large -- confounded by the photometric lenses' mask selection (see the docstring)",
          f"bin 2: {VR[2]['A_boost']:.3f} +- {VR[2]['sA_boost']:.3f}; bin 3: {VR[3]['A_boost']:.3f} +- {VR[3]['sA_boost']:.3f}; inner (< 0.3 Mpc) / "
          f"outer amplitude, no boost vs boost: bin 2 {VR[2]['split'][0]:.2f}/{VR[2]['split'][1]:.2f} vs {VR[2]['split'][2]:.2f}/{VR[2]['split'][3]:.2f}, "
          f"bin 3 {VR[3]['split'][0]:.2f}/{VR[3]['split'][1]:.2f} vs {VR[3]['split'][2]:.2f}/{VR[3]['split'][3]:.2f}; bin-3 boost per B21 bin: "
          + " ".join(f"{x:.2f}" for x in VR[3]["boost"]), all(0.80 <= VR[b_]["A_boost"] <= 1.20 for b_ in (2, 3)), load_bearing=False)
    OUT["numbers"]["K"] = dict(n_src=NS_, c_terms=CC, cross=dict(T2=T2x, p=px, chi2_hartlap=cx, d=x15), K2=dict(nfw=max(dev), sis=dsis),
                               K3=dict(mine=Tmine["T"], fp18=Tf18["T"], committed=Tcom), K4=dict(ungc_med=float(np.median(dlu)),
                               k_off=float(np.median(dk)), kbc=kbc, kbm=kbm, koff_faint=KOFF_FAINT), randoms=dict(chi2=cr, p=pr, d=r15),
                               validation={str(b_): {k_: v_ for k_, v_ in VR[b_].items()} for b_ in VR}, COEF_SI=F18.COEF_SI, onepK=ONEPK,
                               randoms_T2=T2r)
    P(f"    {el()}")

    # ============================================================================================= S the sample
    banner("S  THE SAMPLE: 2M++ in KiDS-1000, the mass mapping, the type labels, the isolation and its leakage")
    lmg = LMG[CAND]; TM = (lmg >= M_LO) & (lmg <= M_HI)
    late, early = LATE[CAND], EARLY[CAND]; hi_, fp_, ur_ = HI[CAND], FPE[CAND], UR[CAND]
    iso0 = ISO["3Mpc/500"][0]
    PRIM = TM & late & iso0
    P(f"    candidates (footprint, z >= {Z_MIN}): {NCAND:,} (KiDS-N {np.sum(DE[CAND] > -15):,}, KiDS-S {np.sum(DE[CAND] < -15):,}); "
      f"target mass {M_LO}-{M_HI}: {TM.sum()} (log <M_gal> {np.log10(np.mean(10 ** lmg[TM])):.2f}; z 5/50/95%: "
      f"{', '.join(f'{x:.4f}' for x in np.percentile(lz[TM], [5, 50, 95]))})")
    P(f"    labels at the target mass: HI-detected {np.sum(TM & hi_)}, 6dF-FP {np.sum(TM & fp_)}, KiDS colour {np.sum(TM & np.isfinite(ur_))}; "
      f"LATE {np.sum(TM & late)}, EARLY {np.sum(TM & early)}, ambiguous/unknown {np.sum(TM & ~late & ~early)}")
    urc = lambda m, c: float(np.mean(ur_[m & np.isfinite(ur_)] < c)) if np.sum(m & np.isfinite(ur_)) else float("nan")
    ALFA_FOOT = (DE[CAND] > 0) & (DE[CAND] < 36) & (RA[CAND] > 112.5) & (RA[CAND] < 247.5)
    cal = {c: (urc(TM & fp_, c), urc(TM & hi_, c), urc(TM & ALFA_FOOT & ~hi_, c)) for c in (2.2, 2.3, 2.35, 2.4, 2.5)}
    check("T1 (reported) THE TYPE CUT, calibrated on the labels only: fraction with GAaP u - r below the cut among spectroscopic early "
          "types (6dF-FP), HI-rich spirals (ALFALFA) and ALFALFA-footprint non-detections, at the target mass",
          "; ".join(f"u-r<{c}: FP {v[0]:.2f}, HI {v[1]:.2f}, non-det {v[2]:.2f}" for c, v in cal.items())
          + f"; FP u-r quantiles 10/50/90: {', '.join(f'{x:.2f}' for x in np.nanpercentile(ur_[TM & fp_], [10, 50, 90]))}",
          True, load_bearing=False, reading="the cut 2.35 admits no FP early type and ~70% of HI-rich spirals; at z ~ 0.026 the GAaP "
                                            "colour is a bulge colour, so the LATE sample is spiral-ENRICHED, not a morphological sample")
    P("    isolation (2M++ neighbour brighter in total Ks), target-mass counts all / LATE / EARLY:")
    for k_, (fl, nb) in ISO.items():
        P(f"      {k_:12s}: {np.sum(TM & fl):4d} / {np.sum(TM & late & fl):4d} / {np.sum(TM & early & fl):4d}")
    fl0 = ISO["3Mpc/500"][0]; lk1 = float(np.mean(~ISO["3Mpc/1000"][0][TM & fl0])); lk2 = float(np.mean(~ISO["3Mpc/2000"][0][TM & fl0]))
    npr = []
    for i in CAND[TM & fl0]:
        th = 3.0 / float(DA(Z[i])); js = np.asarray(T2.query_ball_point(X2[i], 2 * math.sin(th / 2)), dtype=np.int64)
        npr.append(int(np.sum((REF[js] == "none") & (np.abs(V[js] - V[i]) <= 500))))
    comp = float(np.nanmean(np.where(c125[CAND[TM & fl0]] > 0, c125[CAND[TM & fl0]], np.nan)))
    OUT["numbers"]["S"] = dict(n_cand=NCAND, n_target=int(TM.sum()), n_late=int(np.sum(TM & late)), n_early=int(np.sum(TM & early)),
                               n_primary=int(PRIM.sum()), iso_counts={k_: [int(np.sum(TM & fl)), int(np.sum(TM & late & fl)), int(np.sum(TM & early & fl))]
                                                                      for k_, (fl, nb) in ISO.items()}, type_cal={str(c): v for c, v in cal.items()},
                               leak=dict(frac_nb_500_1000=lk1, frac_nb_500_2000=lk2, clones_within=int(np.sum(npr)), completeness=comp))
    P(f"    {el()}")

    # ============================================================================================= D the measurement
    banner("D  THE MEASUREMENT: Delta Sigma(R) with every correction; jackknife covariance; S/N per bin")
    dA_, CA_, nA_ = ALL.profile([DET]); snA = float(dA_[0] / math.sqrt(CA_[0, 0]))
    check("D1 THE FULL 2M++ CANDIDATE STACK (all masses, environments and types; z >= 0.01) DETECTS weak lensing around the "
          "spectroscopic lenses: S/N of the single-bin Delta Sigma over 0.03-1.62 Mpc > 4 (jackknife)",
          f"N = {NCAND:,}, Delta Sigma = {dA_[0]:.2f} +- {math.sqrt(CA_[0, 0]):.2f} Msun/pc^2 (S/N {snA:.1f}; {nA_} patches)", snA > 4.0)
    TMS, _ = sample(TM)
    dT, CT, nT = TMS.profile([DET]); snT = float(dT[0] / math.sqrt(CT[0, 0])); snT_sn = float(dT[0] / TMS.shape_noise([DET])[0])
    check("D1b (reported) THE TARGET-MASS STACK ALONE (10.4-10.8, all environments and types): its detection S/N, jackknife vs "
          "shape noise only", f"N = {TM.sum()}, Delta Sigma = {dT[0]:.2f} +- {math.sqrt(CT[0, 0]):.2f} (S/N {snT:.1f}; shape noise only "
          f"{snT_sn:.1f}; {nT} patches)", True, load_bearing=False,
          reading="at z ~ 0.026 the 0.3-1.6 Mpc annuli span ~1 deg: cosmic-shear noise, shared by clustered lenses, doubles the error")
    SAMPLES = {
        "PRIMARY late, 3Mpc/500": TM & late & fl0,
        "all types, 3Mpc/500": TM & fl0,
        "early, 3Mpc/500": TM & early & fl0,
        "late, 3Mpc sphere": TM & late & ISO["3Mpc sphere"][0],
        "late, 3Mpc/1000": TM & late & ISO["3Mpc/1000"][0],
        "late, 1.5Mpc/500 (group centrals)": TM & late & ISO["1.5Mpc/500"][0],
        "late, 1Mpc/500 (group centrals)": TM & late & ISO["1Mpc/500"][0],
        "all types, 1Mpc/500 (group centrals)": TM & ISO["1Mpc/500"][0],
        "all late (no isolation)": TM & late,
        "NON-isolated, all types": TM & ~fl0,
        "all target mass": TM,
    }
    # the LV targets (FP18 mapping (i)), combined with the R0 inverse-variance weights
    wS, wG = 1 / HON["stack"] ** 2, 1 / HON["LG"] ** 2
    R0C = (0.93 * wS + 0.91 * wG) / (wS + wG); sR0C = 1 / math.sqrt(wS + wG)
    TLV = [(t[0], t[1] * wS / (wS + wG)) for t in F18J["matching"]["targets"]["i"]["stack"]] + \
          [(t[0], t[1] * wG / (wS + wG)) for t in F18J["matching"]["targets"]["i"]["LG"]]
    dLV, CLV, cvLV = F18.kids_for(TLV)
    RES = {}
    for name, msk in SAMPLES.items():
        S_, ii = sample(msk)
        if len(ii) < 3:
            RES[name] = None; continue
        d15, C15, n15 = S_.profile(B21_BINS); sn15 = S_.shape_noise(B21_BINS); R15 = S_.meanR(B21_BINS)
        d6, C6, n6 = S_.profile(WIDE); dB_, CB_, nB_ = S_.profile([BAND])
        W15 = S_.weights(B21_BINS); wb = W15[BAND_B] / W15[BAND_B].sum()
        bw = np.array([S_.A[k_, 0][BAND].sum() for k_ in range(len(ii))]); tg = [(float(lmg[ii][k_]), float(bw[k_] / bw.sum())) for k_ in range(len(ii))]
        dM, CM, cvM = F18.kids_for(tg)
        bandM = float(wb @ dM[BAND_B]); sbandM = float(math.sqrt(wb @ CM[np.ix_(BAND_B, BAND_B)] @ wb))
        bandLV = float(wb @ dLV[BAND_B]); fmass = bandLV / bandM
        A_ = float(dB_[0] / bandM); sA_ = float(math.sqrt(CB_[0, 0] + A_ ** 2 * sbandM ** 2) / bandM)
        var = {}
        for vk, kw in (("Z_B>0.5", dict(cols=(8, 9), dil=False)), ("MASK=0", dict(cols=(10, 11), dil=False)), ("raw boost", dict(boost="raw")),
                       ("no boost", dict(boost="none")), ("no dilution", dict(dil=False))):
            dv_, Cv_, _ = S_.profile([BAND], **kw); var[vk] = (float(dv_[0]), float(math.sqrt(Cv_[0, 0])))
        x15, Cx_, nx_ = S_.profile(B21_BINS, cols=(0, 2)); _, cxx = hotelling(x15, Cx_, nx_)
        L_, nL_, Rr_ = S_.sums()
        Bst = (L_[0] / nL_) / np.where(Rr_[0] > 0, Rr_[0], np.nan)
        RES[name] = dict(n=len(ii), npatch=n15, d15=d15, C15=C15, sn15=sn15, R15=R15, d6=d6, C6=C6, n6=n6, band=float(dB_[0]),
                         sband=float(math.sqrt(CB_[0, 0])), bandM=bandM, sbandM=sbandM, fmass=fmass, A=A_, sA=sA_, var=var, dM=dM, CM=CM,
                         wb=wb, lmg=float(np.log10(np.sum(10 ** lmg[ii] * bw / bw.sum()))), cross_chi2=cxx,
                         boost=[float(np.nanmean(Bst[g])) for g in B21_BINS], fdil=[float(L_[7][g].sum() / L_[0][g].sum()) for g in B21_BINS],
                         zmed=float(np.median(lz[ii])), S=S_)
    pr_ = RES["PRIMARY late, 3Mpc/500"]
    P(f"    PRIMARY: LATE, isolated (no brighter 2M++ galaxy within 3 Mpc and +-500 km/s), 10.4 <= log M_gal <= 10.8: N = {pr_['n']} "
      f"(lensing-weighted log M_gal {pr_['lmg']:.2f}, median z {pr_['zmed']:.4f}; {pr_['npatch']} jackknife patches)")
    xs = pr_["S"].profile(B21_BINS, cols=(0, 2))[0]
    P("      R [Mpc] | Delta Sigma +- jk (shape noise) | S/N  | Delta Sigma_x | boost | dilution f | B21 mixed at the same mass")
    for i in range(15):
        e_ = math.sqrt(pr_["C15"][i, i])
        P(f"      {pr_['R15'][i]:6.3f} | {pr_['d15'][i]:8.2f} +- {e_:6.2f} ({pr_['sn15'][i]:6.2f}) | {pr_['d15'][i] / e_:+5.1f} | "
          f"{xs[i]:+6.2f} | {pr_['boost'][i]:5.3f} | {pr_['fdil'][i]:6.4f} | {pr_['dM'][i]:6.2f} +- {math.sqrt(pr_['CM'][i, i]):4.2f}")
    check("D2 (reported) THE PRIMARY PROFILE: Delta Sigma(R) of spectroscopically isolated LATE-type 2M++ galaxies of LV-central mass, "
          "per B21 radial bin, with jackknife errors and S/N", "; ".join(f"R {pr_['R15'][i]:.2f}: {pr_['d15'][i]:+.1f} +- "
                                                                          f"{math.sqrt(pr_['C15'][i, i]):.1f} (x {xs[i]:+.1f})" for i in range(15)),
          True, load_bearing=False, reading=f"band (0.26-1.62 Mpc) {pr_['band']:.2f} +- {pr_['sband']:.2f} Msun/pc^2 (S/N {pr_['band'] / pr_['sband']:.1f}); "
                                            f"cross-shear null p = {pr_['cross_chi2']:.2f} (Hotelling)")
    P("    every sample (band = one bin over 0.26-1.62 Mpc, jackknife; A = band / B21 mixed at the sample's mass):")
    P(f"      {'sample':38s} {'N':>4s} {'log M':>6s} | {'band':>6s} +- {'err':>5s} | {'B21 mix':>7s} | {'A':>6s} +- {'sA':>5s} | Z_B>0.5 | MASK=0 | raw B | no B")
    for name, r in RES.items():
        if r is None:
            P(f"      {name:38s} (fewer than 3 lenses)"); continue
        P(f"      {name:38s} {r['n']:4d} {r['lmg']:6.2f} | {r['band']:6.2f} +- {r['sband']:5.2f} | {r['bandM']:7.2f} | {r['A']:6.2f} +- {r['sA']:5.2f} | "
          f"{r['var']['Z_B>0.5'][0]:6.2f} | {r['var']['MASK=0'][0]:6.2f} | {r['var']['raw boost'][0]:5.2f} | {r['var']['no boost'][0]:5.2f}")
    check("D3 (reported) EVERY VARIANT: the band Delta Sigma for the isolation windows, the group-central radii, the types, the "
          "non-isolated sample, and the source-selection / boost / dilution variants",
          "; ".join(f"{k_}: {r['band']:.2f} +- {r['sband']:.2f} (N {r['n']})" for k_, r in RES.items() if r is not None), True, load_bearing=False)
    lk_rows = [(k_, RES[k_]["band"], RES[k_]["sband"]) for k_ in ("late, 3Mpc sphere", "PRIMARY late, 3Mpc/500", "late, 3Mpc/1000") if RES[k_]]
    check("L1 (reported) ISOLATION LEAKAGE: (i) the fraction of primary-isolated target-mass lenses with a brighter 2M++ galaxy at "
          "500 < |dV| <= 1000 / 2000 km/s inside 3 Mpc (an upper bound on velocity leakage), (ii) 2M++ velocity-assigned ('none') "
          "galaxies near them, (iii) the 2M++ K <= 12.5 completeness there, (iv) the lensing's response to the window",
          f"(i) {lk1:.2f} / {lk2:.2f}; (ii) {int(np.sum(npr))} within 3 Mpc / +-500 km/s of {int(np.sum(TM & fl0))} lenses; (iii) mean c12.5 "
          f"{comp:.3f}; (iv) late-type band: " + ", ".join(f"{k_} {b:.2f} +- {s:.2f}" for k_, b, s in lk_rows), True, load_bearing=False,
          reading="a brighter neighbour is complete to K 12.5 whenever the lens is in 2M++, so the leakage is velocity leakage only")
    P(f"    {el()}")

    # ============================================================================================= C comparisons
    banner("C  THE COMPARISONS: B21 mixed-type at the same mass; the mass the LV groups' R0 allows; the joint free-profile T")
    Rb = F18.RD
    Mmax = lambda R, R0: np.where(R <= R0, F18.target_exc(R0), F18.target_exc(R))
    env15 = Mmax(Rb, R0C) / (np.pi * Rb ** 2)
    Mg12 = 10 ** F18.mgal_of(cvLV) / 1e12
    nfw_env = []
    for c in np.geomspace(1.0, 30.0, 30):
        f = lambda lm: F18.R0_of(F18.nfw_Mcum(10 ** lm, c, Mg12)) - R0C
        try:
            lm = brentq(f, -2.0, 1.5, xtol=1e-6)
        except ValueError:
            continue
        nfw_env.append((c, 10 ** lm, F18.esd_of(F18.nfw_Mcum(10 ** lm, c, Mg12))))
    nfw_max = np.max(np.array([e_[2] for e_ in nfw_env]), axis=0)
    nfw_c = {round(c, 1): e_ for c, m_, e_ in nfw_env}
    ctyp = min(nfw_env, key=lambda t: abs(t[0] - 8.0))
    wbp = pr_["wb"]
    band_env, band_nfw, band_nfw8 = float(wbp @ env15[BAND_B]), float(wbp @ nfw_max[BAND_B]), float(wbp @ ctyp[2][BAND_B])
    P(f"    the flow: R0 = {R0C:.3f} +- {sR0C:.3f} Mpc (stack 0.93 +- {HON['stack']:.3f} and LG 0.91 +- {HON['LG']:.3f} combined); "
      f"M_exc(<R0) <= {F18.target_exc(R0C):.2f}e12 Msun (eq. 4, COEF {F18.COEF_SI:.4f}e12, minus the mean)")
    P(f"    the LV centrals' mass (mapping (i), stack + LG): log M_gal {F18.mgal_of(cvLV):.2f}; B21 mixed there, band {wbp @ dLV[BAND_B]:.2f}")
    P("      R [Mpc] | rigorous envelope | NFW envelope (c 1-30) | NFW c~8 | B21 mixed (LV mass) | PRIMARY x mass-match")
    for i in range(15):
        P(f"      {Rb[i]:6.3f} | {env15[i]:8.2f} | {nfw_max[i]:8.2f} | {ctyp[2][i]:6.2f} | {dLV[i]:7.2f} +- {math.sqrt(CLV[i, i]):4.2f} | "
          f"{pr_['d15'][i] * pr_['fmass']:7.2f} +- {math.sqrt(pr_['C15'][i, i]) * pr_['fmass']:5.2f}")
    # A_rec: the face-value reconciliation amplitude on B21's own precision -- the WHOLE mixed profile at the LV mass scaled by A
    # (scaling only R > 0.26 Mpc cannot reach compatibility: B21's inner lensing already fixes the mass; T(A_out -> 0) stays large)
    def T_of_A(a, outer_only=False):
        d_ = np.where(np.arange(15) >= 7, a * dLV, dLV) if outer_only else a * dLV
        return T_free_K(d_, CLV, F18.KC, R0C, sR0C, full=True)["T"]
    T1_ = T_of_A(1.0)
    try:
        A_REC = brentq(lambda a: T_of_A(a) - T_OK1, 0.01, 1.0, xtol=2e-3) if T1_ > T_OK1 else 1.0
    except ValueError:
        A_REC = float("nan")
    T_OUT = {a: T_of_A(a, True) for a in (0.1, 0.3, 0.5)}
    # the joint T for every sample (mass-matched, 6 wide bins, pair-weight-averaged shell kernel)
    TJ = {}
    for name, r in RES.items():
        if r is None:
            continue
        S_ = r["S"]; L_ = S_.A.sum(0); Rf = L_[5] / np.where(L_[0] > 0, L_[0], np.nan); Kf = F18.shell_kernel(np.nan_to_num(Rf, nan=1.0), F18.EC)
        K6 = np.array([(L_[0][g][:, None] * Kf[g]).sum(0) / L_[0][g].sum() for g in WIDE])
        h6 = hartlap(r["n6"], 6)
        if not np.isfinite(h6) or h6 <= 0:
            TJ[name] = None; continue
        dm, Cm = r["d6"] * r["fmass"], r["C6"] * r["fmass"] ** 2 / h6
        try:
            tj = T_free_K(dm, Cm, K6, R0C, sR0C, full=True)
            ts = T_free_K(dm, Cm, K6, 0.93, HON["stack"], full=True)["T"] + T_free_K(dm, Cm, K6, 0.91, HON["LG"], full=True)["T"]
            tu = T_free_K(r["d6"], r["C6"] / h6, K6, R0C, sR0C, full=True)["T"]
        except np.linalg.LinAlgError:
            TJ[name] = None; continue
        lb = np.pi * r["R15"] ** 2 * r["d15"] * r["fmass"]; slb = np.pi * r["R15"] ** 2 * np.sqrt(np.diag(r["C15"])) * r["fmass"]
        inR = r["R15"] <= R0C; zlb = (lb - F18.target_exc(R0C)) / slb
        TJ[name] = dict(T=tj["T"], R0t=tj["R0t"], T2sys=ts, T_unmatched=tu, h6=h6, zlb_max=float(np.max(zlb[inR])),
                        lb=lb, slb=slb, band_m=r["band"] * r["fmass"], sband_m=r["sband"] * r["fmass"])
    P("    per sample (mass-matched to the LV centrals by B21's mass trend; T on 6 wide bins, Hartlap; dof 1 with the combined R0):")
    P(f"      {'sample':38s} {'fmass':>5s} | {'band':>6s} +- {'err':>5s} | env: rigorous {band_env:.2f}, NFW {band_nfw:.2f}, c8 {band_nfw8:.2f} | "
      f"{'T':>6s} {'(2-sys)':>7s} | max z of pi R^2 dS above the cap")
    for name, t in TJ.items():
        if t is None:
            P(f"      {name:38s} (covariance not invertible)"); continue
        r = RES[name]
        P(f"      {name:38s} {r['fmass']:5.2f} | {t['band_m']:6.2f} +- {t['sband_m']:5.2f} | z vs rigorous {(t['band_m'] - band_env) / t['sband_m']:+5.1f}, "
          f"vs NFW {(t['band_m'] - band_nfw) / t['sband_m']:+5.1f}, vs mixed {(t['band_m'] - wbp @ dLV[BAND_B]) / t['sband_m']:+5.1f} | "
          f"{t['T']:6.2f} {t['T2sys']:7.2f} | {t['zlb_max']:+5.1f}")
    check("C1 (reported) VS THE PUBLISHED MIXED-TYPE BINS AT THE SAME MASS: the amplitude A of the band Delta Sigma relative to B21's "
          "isolated mixed-type lenses interpolated to each sample's lensing-weighted M_gal",
          "; ".join(f"{k_}: A = {r['A']:.2f} +- {r['sA']:.2f}" for k_, r in RES.items() if r is not None), True, load_bearing=False,
          reading=f"FP18's reconciliation needs ~0.29-0.33 beyond 0.3 Mpc (profiled optimum); B21's measured blue/red contrast there is 0.50")
    check("C2 (reported) VS THE FLOW: the band Delta Sigma the combined R0 allows -- rigorous (any non-negative profile), the NFW family "
          "(any c), a c ~ 8 NFW -- and the model-independent mass bound pi R^2 Delta Sigma(R) against the cap M_exc(<R0)",
          f"allowed band: rigorous <= {band_env:.2f}, NFW <= {band_nfw:.2f}, c~8 {band_nfw8:.2f}; B21 mixed at the LV mass {wbp @ dLV[BAND_B]:.2f}; "
          f"PRIMARY (mass-matched) {TJ['PRIMARY late, 3Mpc/500']['band_m']:.2f} +- {TJ['PRIMARY late, 3Mpc/500']['sband_m']:.2f}"
          if TJ.get("PRIMARY late, 3Mpc/500") else "primary T unavailable", True, load_bearing=False)
    check("C3 (reported) THE JOINT FREE-PROFILE STATISTIC T (FP18's, full R0 definition) with each sample's lensing and the combined R0; "
          "and A_rec, the largest fraction of the mixed-type profile (all radii) that B21-precision data at the LV mass could show and "
          "still meet the flow at p = 0.05", f"A_rec = {A_REC:.3f} (T at A = 1: {T1_:.1f}; scaling only R > 0.26 Mpc by 0.1 / 0.3 / 0.5: T = "
          f"{T_OUT[0.1]:.1f} / {T_OUT[0.3]:.1f} / {T_OUT[0.5]:.1f}); " + "; ".join(f"{k_}: T {t['T']:.2f}" for k_, t in TJ.items() if t is not None),
          True, load_bearing=False)
    OUT["numbers"]["C"] = dict(R0C=R0C, sR0C=sR0C, band_env=band_env, band_nfw=band_nfw, band_nfw8=band_nfw8, env15=env15, nfw_max=nfw_max,
                               dLV=dLV, lmg_LV=float(F18.mgal_of(cvLV)), A_rec=A_REC, T_at_A1=T1_, T_outer_only={str(k_): v for k_, v in T_OUT.items()},
                               samples={k_: (None if t is None else {kk: v for kk, v in t.items()}) for k_, t in TJ.items()})
    P(f"    {el()}")

    # ============================================================================================= V verdict and forecast
    banner("V  THE VERDICT (the rule declared in the docstring) AND THE SAMPLE THAT WOULD DECIDE")
    ANALOG = [k_ for k_ in SAMPLES if k_ not in ("all late (no isolation)", "NON-isolated, all types", "all target mass")]
    tp = TJ.get("PRIMARY late, 3Mpc/500")
    if tp is None:
        VERD, Tp = "UNDECIDED", float("nan")
    else:
        Tp = tp["T"]
        if Tp <= T_OK1 and (1 - pr_["A"]) / pr_["sA"] >= 2.0:
            VERD = "RECONCILED"
        elif Tp > T_LIM1:
            VERD = "PINCER REAL"
        else:
            VERD = "UNDECIDED"
    pT, sT = sig_of(Tp, 1)
    per_verd = {}
    for k_, t in TJ.items():
        if t is None:
            continue
        r = RES[k_]
        per_verd[k_] = ("RECONCILED" if (t["T"] <= T_OK1 and (1 - r["A"]) / r["sA"] >= 2.0) else ("PINCER REAL" if t["T"] > T_LIM1 else "UNDECIDED")) \
            + ("" if k_ in ANALOG else " (not an LV analog: no isolation)")
    check("V1 (reported) THE VERDICT BY THE DECLARED RULE on the primary sample, and the same rule on every variant",
          f"PRIMARY: {VERD} -- T = {Tp:.2f} (p {pT:.2f}, {sT:.1f} sigma), A = {pr_['A']:.2f} +- {pr_['sA']:.2f} ((1 - A)/sigma_A = "
          f"{(1 - pr_['A']) / pr_['sA']:+.1f}); " + "; ".join(f"{k_}: {v}" for k_, v in per_verd.items()), True, load_bearing=False)
    # forecast: A = 1 vs A = A_rec at 3 sigma
    N0, sA0 = pr_["n"], pr_["sA"]
    need = (1.0 - A_REC) / 3.0
    N3 = int(math.ceil(N0 * (sA0 / need) ** 2)) if np.isfinite(A_REC) and A_REC < 1 else None
    N2 = int(math.ceil(N0 * (sA0 / ((1.0 - A_REC) / 2.0)) ** 2)) if N3 else None
    # per-lens band variance: 2M++ spirals (z ~ 0.026) vs the photometric KiDS-bright lenses (z ~ 0.3)
    v2 = pr_["sband"] ** 2 * pr_["n"] / pr_["bandM"] ** 2
    vv = {}
    for b_ in (2, 3):
        dvb, Cvb, _ = VAL[b_].profile([BAND]); vv[b_] = Cvb[0, 0] * VAL[b_].n / float(dvb[0]) ** 2
    ratio = float(np.mean([vv[2], vv[3]]) / v2)
    tall = RES["all target mass"]
    P(f"    the primary's amplitude error sigma_A = {sA0:.2f} from N = {N0}; deciding A = 1 vs A_rec = {A_REC:.2f} at 3 sigma needs sigma_A "
      f"<= {need:.3f}: N ~ {N3} late-type isolated centrals at z ~ 0.026 (2 sigma: {N2}); the fractional per-lens variance of a KiDS-"
      f"bright photometric lens at z ~ 0.3 is {ratio:.1f}x that of a 2M++ lens, so ~{int(N3 * ratio) if N3 else None} spectroscopic isolated "
      f"spirals at z ~ 0.1-0.4 (GAMA/SDSS-like) would do the same; 2M++ holds {int(np.sum(TM & late))} late-type target-mass galaxies "
      f"in the whole KiDS-1000 footprint ({int(TM.sum())} of all types) -- the on-disk data CANNOT decide it")
    check("V2 (reported) THE SAMPLE THAT WOULD DECIDE: the number of spectroscopically isolated late-type centrals at LV-central mass "
          "that separates the mixed level (A = 1) from the face-value reconciliation level (A_rec) at 3 sigma",
          f"N_3sigma ~ {N3} at z ~ 0.026 (2M++-like; {N2} for 2 sigma), ~{int(N3 * ratio) if N3 else None} at z ~ 0.3 (KiDS-bright-like per-lens "
          f"noise); available here {N0}", True, load_bearing=False)
    OUT["numbers"]["V"] = dict(verdict=VERD, T=Tp, p=pT, A=pr_["A"], sA=pr_["sA"], per_sample=per_verd, N3=N3, N2=N2, var_ratio=ratio,
                               A_rec=A_REC, n_primary=N0)
    OUT["numbers"]["D"] = {k_: (None if r is None else {kk: v for kk, v in r.items() if kk not in ("S", "C15", "C6", "CM")}) for k_, r in RES.items()}
    OUT["numbers"]["D"]["primary_C15"] = pr_["C15"]

    # ============================================================================================= W ledger
    banner("W  THE LEDGER: FP21, weak lensing of spectroscopically isolated spirals of LV-central mass")
    iso_all = RES["all types, 3Mpc/500"]; non = RES["NON-isolated, all types"]; gc = RES["all types, 1Mpc/500 (group centrals)"]
    zrec = [(RES[k_]["A"] - 0.3) / RES[k_]["sA"] for k_ in ANALOG if RES.get(k_) and not k_.startswith("early")]
    chain_meaning = {"RECONCILED": ("FAILS", "the spirals' lensing and the flow agree with each other and not with the chain's universal (type-blind) outer "
                                              "profile, which fits B21's mixed bins and predicts R0 = 1.24-1.53 Mpc (FP12)"),
                     "PINCER REAL": ("CONSTRAINT", "the two datasets disagree with each other for every static profile, so the chain's R0 overshoot "
                                                   "is not a refutation of its outer profile in particular (FP18 F18f stands)"),
                     "UNDECIDED": ("OPEN", "nothing moves: FP18's standing holds -- the chain's R0 = 1.24-1.53 Mpc overshoot of the LV is neither "
                                           "confirmed as a law-specific failure nor excused as a data-data pincer; the chain's universal law "
                                           "cannot produce a type dependence, so a future RECONCILED would FAIL it")}[VERD]
    lcdm_meaning = {"RECONCILED": "LCDM accommodates it: at fixed M* late-type centrals live in less massive halos, and its KiDS-fitted R0 falls with them",
                    "PINCER REAL": "LCDM inherits the pincer: its NFW(+2h) halos fitted to KiDS turn around at 1.65-2.26 Mpc (FP18 L1)",
                    "UNDECIDED": "unchanged: LCDM's KiDS-fitted halos turn around at 1.65-2.26 Mpc (FP18 L1); a type split in halo mass at fixed M* "
                                 "is standard LCDM, so a future RECONCILED would be comfortable for it"}[VERD]
    LEDGER = [
        ("F21a", f"the like-for-like lens sample exists and is small: 2M++ (spectroscopic, K <= 12.5, complete in both KiDS regions) holds "
                 f"{NCAND:,} galaxies in the KiDS-1000 footprint (z >= {Z_MIN}), {int(TM.sum())} at 10.4 <= log M_gal <= 10.8 with the LV "
                 f"centrals' own mass mapping (0.6 L_K + Boselli gas; UNGC L_K reproduced to {np.median(dlu):+.3f} dex), {int(np.sum(TM & late))} "
                 f"LATE-labelled; only {int(np.sum(TM & fl0))} are the brightest within 3 Mpc / +-500 km/s, {N0} of them LATE (the primary)",
         "CONSTRAINT", "K4, S, T1"),
        ("F21b", f"the pipeline (exact spherical geometry, c, m = B21's 1+K, dilution model, randoms, jackknife) reproduces B21's published "
                 f"bins 2 / 3 from the record's photometric reconstruction at A = {VR[2]['A']:.2f} +- {VR[2]['sA']:.2f} / {VR[3]['A']:.2f} +- "
                 f"{VR[3]['sA']:.2f} with B21's convention (no boost); applying the boost measured against uniform randoms gives "
                 f"{VR[2]['A_boost']:.2f} / {VR[3]['A_boost']:.2f} (K6 as first declared FAILS for bin 3) -- that boost is confounded by the "
                 f"lens samples' mask selection, and is inactive for the 2M++ lenses (B <= 1 in the band); cross-shear and random nulls pass",
         "CONSTRAINT", "K1, K5, K6, K6b"),
        ("F21c", f"the measurement: the primary sample's Delta Sigma over 0.26-1.62 Mpc is {pr_['band']:.2f} +- {pr_['sband']:.2f} Msun/pc^2 "
                 f"(S/N {pr_['band'] / pr_['sband']:.1f}), A = {pr_['A']:.2f} +- {pr_['sA']:.2f} of B21's mixed-type isolated lenses at the same "
                 f"mass; all types isolated A = {iso_all['A']:.2f} +- {iso_all['sA']:.2f}; group centrals (1 Mpc) A = {gc['A']:.2f} +- {gc['sA']:.2f}",
         "CONSTRAINT", "D1, D2, D3, C1"),
        ("F21d", f"against the flow (R0 = {R0C:.3f} +- {sR0C:.3f} Mpc): the band Delta Sigma allowed is <= {band_env:.2f} (rigorous, any profile) / "
                 f"{band_nfw:.2f} (any NFW); the primary's mass-matched band is {tp['band_m']:.2f} +- {tp['sband_m']:.2f}; the joint free-profile "
                 f"T = {Tp:.2f} (p {pT:.2f}); at B21's precision the flow tolerates at most A_rec = {A_REC:.2f} of the mixed-type profile (all radii "
                 f"scaled) at face value -- FP18's -0.5 dex reconciliation, recovered independently"
         if tp else "the primary's T could not be computed", "CONSTRAINT", "C2, C3"),
        ("F21e", f"the verdict by the declared rule: {VERD}", "OPEN" if VERD == "UNDECIDED" else "CONSTRAINT", "V1"),
        ("F21f", f"FP18's comparability systematics tested directly (L_K masses as the LV's, spectroscopic isolation, z ~ 0): no sample is "
                 f"measurably BELOW B21's mixed level -- isolated all types A = {iso_all['A']:.2f} +- {iso_all['sA']:.2f}, group centrals "
                 f"{gc['A']:.2f} +- {gc['sA']:.2f}, the primary {pr_['A']:.2f} +- {pr_['sA']:.2f}, non-isolated {non['A']:.2f} +- {non['sA']:.2f} (isolated "
                 f"and non-isolated do not differ measurably); FP18's reconciled level A ~ 0.3 lies {min(zrec):.1f}-{max(zrec):.1f} sigma below the "
                 f"isolated samples -- a lean against reconciliation, not a result", "CONSTRAINT", "D3, C1"),
        ("F21g", f"for the chain's universal law (R0 = 1.24-1.53 Mpc for the stack / LG, FP12; no type dependence possible): {chain_meaning[1]}",
         chain_meaning[0], "V1, FP12, FP18"),
        ("F21h", f"for LCDM: {lcdm_meaning}", "OPEN" if VERD == "UNDECIDED" else "CONSTRAINT", "V1, FP18 L1"),
        ("F21i", f"what would decide it: ~{N3} spectroscopically isolated late-type centrals at LV-central mass at z ~ 0.03 (3 sigma between "
                 f"A = 1 and A_rec = {A_REC:.2f}), or ~{int(N3 * ratio) if N3 else None} at z ~ 0.1-0.4; the on-disk 2M++ holds {N0}; GAMA DR4 (G09/G12/G15/G23, "
                 f"r < 19.65) or SDSS DR7 spectroscopy over KiDS-N is the next step, and fetching it needs the user's go", "OPEN", "V2"),
        ("F21j", f"the type cut is FITTED to labels, not to lensing: GAaP u - r < {UR_LATE} (no 6dF-FP early type below it; ~70% of HI-rich "
                 f"spirals) -- at z ~ 0.026 it is a bulge colour, so LATE is spiral-enriched, not morphological", "FITTED", "T1"),
    ]
    for k_, what, status, why in LEDGER:
        P(f"    {k_:5s} {status:11s} {what}  --  {why}")
    OUT["ledger"] = [dict(link=k_, what=w, status=s_, basis=b_) for k_, w, s_, b_ in LEDGER]
    check("W (reported) the ledger of this lane", f"{len(LEDGER)} links", True, load_bearing=False)

    # ============================================================================================= verdict block
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    banner("VERDICT")
    P(f"  PRIMARY (LATE, isolated 3 Mpc / +-500 km/s, 10.4-10.8, N = {N0}): band Delta Sigma(0.26-1.62 Mpc) = {pr_['band']:.2f} +- {pr_['sband']:.2f} "
      f"Msun/pc^2; A = {pr_['A']:.2f} +- {pr_['sA']:.2f} of B21's mixed bins at the same mass; the flow allows <= {band_env:.2f} (rigorous) / "
      f"{band_nfw:.2f} (NFW); T = {Tp:.2f}.")
    P(f"  VERDICT (declared rule): {VERD}.  Sample that would decide at 3 sigma: ~{N3} such centrals at z ~ 0.03 or ~{int(N3 * ratio) if N3 else None} at "
      f"z ~ 0.3; the whole KiDS-1000 footprint holds {int(np.sum(TM & late))} LATE target-mass 2M++ galaxies.")
    P(f"  No isolated sample is measurably below the mixed level (all types {iso_all['A']:.2f} +- {iso_all['sA']:.2f}; group centrals "
      f"{gc['A']:.2f} +- {gc['sA']:.2f}; non-isolated {non['A']:.2f} +- {non['sA']:.2f}); FP18's reconciled level A ~ 0.3 lies "
      f"{min(zrec):.1f}-{max(zrec):.1f} sigma below the isolated samples -- a lean, not a result.")
    P("  Not 'closed'.  Time " + f"{time.time() - T0:.0f} s.")
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))

    def enc(o):
        if isinstance(o, np.ndarray): return o.tolist()
        if isinstance(o, (np.floating, np.integer)): return float(o)
        if isinstance(o, (np.bool_,)): return bool(o)
        return str(o)
    json.dump(OUT, open(fn, "w"), indent=1, default=enc)
    P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}")
    sys.exit(0 if nlb == 0 else 1)


if __name__ == "__main__":
    main()
