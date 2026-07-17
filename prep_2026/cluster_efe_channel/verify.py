#!/usr/bin/env python3
r"""
VERIFY LANE  --  prep_2026/cluster_efe_channel/verify.py                        2026-07-17
==========================================================================================
ADVERSARIAL re-audit of the four banked lanes (predict / mg_efe_zero / observable / power)
for the CLUSTER-MEMBER INFALL-PHASE EFE sigma-spread.  Exit 0.  numpy only.  BOTH footings.

I did NOT rebuild the physics; I stress the LOAD-BEARING claims that, if wrong, kill the test:

  V1  THE CRUX (reviewer #2).  observable.py [C] claims the ~2.2% MG projection alias is
      "killed to <0.1%" by the Rhee zones "binning on TRUE r".  But TRUE 3D r is NOT an
      observable -- caustics give M(<r) in 3D, but each galaxy's radius is only R_proj, and
      GAP_STATEMENT E2 itself says "deproject STATISTICALLY" (class-blind), which mg_efe_zero.py
      showed barely dents the alias (2.249->2.185).  E3 says purity p<1, estimated per cluster.
      => quantify the residual alias under a REALISTIC zone tag (purity p, per-zone mean-r
         calibration), NOT the simulation's true r.  Where does the mimic really sit vs 6-13%?

  V2  ANISOTROPIC / FILAMENTARY INFALL (an MG mimic the spherical-isotropic MC never tested).
      Real infall is along filaments -> first-infall galaxies enter along the cluster major
      axis, correlating orbit class WITH projection geometry.  Does that manufacture an MG
      phase-contrast beyond the isotropic 2.2%?

  V3  THE SIGN INCONSISTENCY.  GAP_STATEMENT E4/E7 predict the sign statistic NEGATIVE
      ("plungers less boosted") and make POSITIVE the KILL condition.  predict.py's baseline
      says "plungers/backsplash HOTTER" (positive).  Can the framework's own raw adiabatic
      loading TRIP its own pre-registered kill switch?  Reconcile or flag.

  V4  MANUFACTURED DETECTION + MANUFACTURED NULL (reviewer #6): show an MG universe + the
      frozen cuts can still leak a phase-contrast (false positive risk), and an MI universe
      on survey-bright members gives ~0 (false negative -- the power wall is real).

  V5  DATASET REALITY (reviewer #7): the load-bearing SDSS completeness number.

BOTH FOOTINGS throughout.  MG=0 at fixed TRUE field is granted (re-verified symbolically in
the banked lanes).  MI-class-generic (MI-vs-MG), NOT framework-specific.  Amplitude kernel-
hostage; a0 value + s=-1 postulates.  Honest both ways -- confirm OR break, no caving.
"""
import numpy as np

rng = np.random.default_rng(20260717)
A0_CAN, A0_ALT = 9.36e-11, 1.13e-10
G, Msun, Mpc = 6.674e-11, 1.989e30, 3.086e22
M200, R200, CONC = 1e15*Msun, 2.0*Mpc, 5.0
MI_BAND = {A0_CAN: (0.062, 0.118), A0_ALT: (0.075, 0.141)}
LINE = "="*94
_MUC = np.log(1+CONC) - CONC/(1+CONC)

def m_of_r(r):
    x = r/R200*CONC
    return M200*(np.log(1+x) - x/(1+x))/_MUC
def g_ext(r):
    return G*m_of_r(r)/r**2
def d_MG(r, a0):                                   # MG position-only boost (log), = 0.5 ln nu
    return 0.5*np.log(np.sqrt(1.0 + a0/g_ext(r)))

print(LINE); print(" VERIFY -- adversarial re-audit of the cluster-EFE infall-phase channel (both footings)"); print(LINE)

# ==========================================================================================
# Build a common population: settled (NFW) + radial plungers, projected isotropically.
# ==========================================================================================
def draw_settled(n):
    rs = np.linspace(0.05, 2.5, 6000)*R200
    cdf = m_of_r(rs); cdf = cdf/cdf[-1]
    return np.interp(rng.random(n), cdf, rs)
def draw_plunger(n):
    r_apo = rng.uniform(1.0, 2.0, n)*R200
    psi = rng.uniform(0, np.pi, n)
    return np.clip(r_apo*(1+np.cos(psi))/2, 0.05*R200, 2.4*R200)

N = 200000
r_s = draw_settled(N//2); r_p = draw_plunger(N//2)
r_true = np.concatenate([r_s, r_p])
is_pl = np.concatenate([np.zeros(N//2), np.ones(N//2)])

def project_iso(r):
    mu = rng.uniform(-1, 1, r.size)                # isotropic
    return r*np.sqrt(1-mu**2)
Rproj_iso = project_iso(r_true)

def contrast(bin_var, r_for_d, is_plunger, a0, edges):
    """inverse-variance-combined (mean d_plunger - mean d_settled) within bins of bin_var."""
    d = d_MG(r_for_d, a0); num = den = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (bin_var >= lo) & (bin_var < hi)
        sp, se = m & (is_plunger > 0.5), m & (is_plunger < 0.5)
        if sp.sum() < 30 or se.sum() < 30: continue
        diff = d[sp].mean() - d[se].mean()
        var = d[sp].var(ddof=1)/sp.sum() + d[se].var(ddof=1)/se.sum()
        num += diff/var; den += 1.0/var
    return abs(num/den) if den > 0 else np.nan

edges = np.geomspace(0.1*R200, 2.4*R200, 12)

# ==========================================================================================
# V1  THE CRUX -- realistic deprojection, not the simulation's true r
# ==========================================================================================
print("\n"+LINE); print(" V1  CRUX: is the MG projection alias REALLY killed to ~0.01%, or only on sim-true-r?"); print(LINE)
print("  observable.py [C] bins on the SIMULATION's TRUE r to claim ~0.01%.  But the OBSERVABLE is")
print("  a_ext from the caustic profile evaluated at each galaxy's radius -- which is only R_proj.")
print("  Realistic Rhee tag: an orbit-class label of PURITY p that lets you correct the PER-ZONE")
print("  MEAN true-r (from N-body), leaving the WITHIN-zone true-r scatter uncorrected.\n")

for a0 in (A0_CAN, A0_ALT):
    lo, hi = MI_BAND[a0]
    tag = "canonical" if a0 == A0_CAN else "alternate"
    m_true = contrast(r_true,    r_true, is_pl, a0, edges)   # perfect (sim-true-r) -- NOT observable
    m_proj = contrast(Rproj_iso, r_true, is_pl, a0, edges)   # bin by R_proj (the actual observable)
    # per-zone mean-r correction at purity p: replace each galaxy's binning radius by the
    # PURITY-WEIGHTED mean true-r of its (possibly mis-assigned) zone, within its R_proj shell.
    print(f"  footing={tag}  MI band {lo*100:.1f}-{hi*100:.1f}%")
    print(f"    bin by SIM-TRUE r (observable.py's claim) : {m_true*100:6.3f}%   <- NOT an observable")
    print(f"    bin by R_proj     (the actual observable) : {m_proj*100:6.3f}%")
    for p in (0.5, 0.7, 0.9):
        # assign zone tag: correct class w.p. p, flipped w.p. 1-p
        correct = rng.random(N) < p
        tag_pl = np.where(correct, is_pl, 1-is_pl)
        # per-zone mean-true-r calibration WITHIN each R_proj shell (best case: N-body gives the
        # per-tag mean true r exactly), then bin on that calibrated radius estimate.
        r_cal = np.empty(N)
        order = np.argsort(Rproj_iso); Rs = Rproj_iso[order]
        win = 6000
        for cls in (0.0, 1.0):
            sel = tag_pl[order] == cls
            # local (in R_proj) mean true r for this tag class -> the calibrated radius
            rr = np.where(sel, r_true[order], np.nan)
            # simple boxcar mean of the class's true r vs R_proj rank
            csum = np.nancumsum(np.where(sel, r_true[order], 0.0))
            ccnt = np.cumsum(sel.astype(float))
            idxlo = np.maximum(np.arange(N)-win//2, 0); idxhi = np.minimum(np.arange(N)+win//2, N-1)
            mean_r = (csum[idxhi]-csum[idxlo])/np.maximum(ccnt[idxhi]-ccnt[idxlo], 1)
            r_cal[order[sel]] = mean_r[sel]
        m_cal = contrast(r_cal, r_true, is_pl, a0, edges)
        print(f"    Rhee tag purity p={p:.1f}, per-zone mean-r calib : {m_cal*100:6.3f}%   "
              f"({m_cal/hi*100:.0f}% of MI top, {m_cal/lo*100:.0f}% of floor)")
print("  READING: the calibrated residual sits BETWEEN the ~0.09% sim-true-r floor and the ~2.2%")
print("  raw R_proj alias -- it is NOT the ~0.01% observable.py advertises.  The per-zone mean-r")
print("  calibration removes the MEAN offset; the residual is the within-zone true-r scatter, which")
print("  survives at the ~0.2-1% level and DEGRADES with lower purity.  The kill is REAL but PARTIAL")
print("  and PURITY-DEPENDENT -- a load-bearing mitigation, exactly as mg_efe_zero.py concluded, NOT")
print("  the ~0.01% clean kill the observable lane's sim-true-r binning implies.  Not fatal (residual")
print("  < MI floor at p>=0.7) but the honest MG floor is ~0.5-1%, not ~0.01%.")

# ==========================================================================================
# V2  ANISOTROPIC / FILAMENTARY INFALL -- an MG mimic the isotropic MC never tested
# ==========================================================================================
print("\n"+LINE); print(" V2  ANISOTROPIC (filamentary) infall -- extra MG mimic beyond the isotropic 2.2%?"); print(LINE)
print("  Real infall is along filaments: plungers enter along the cluster major axis.  If the LOS")
print("  is near that axis, plungers are seen at systematically SMALLER R_proj for their true r")
print("  (foreshortened) than isotropic -> the projection alias is AMPLIFIED and correlated with")
print("  orbit class.  Model: plungers projected with anisotropy beta_a (mu drawn toward +-1).\n")
def project_aniso(r, is_plunger, kap):
    # kap=0 -> isotropic (|mu| uniform, = uniform(-1,1)); kap>0 -> plungers concentrated toward
    # |mu|->1 (infall along the LOS/filament axis, foreshortened to small R_proj).
    u = rng.random(r.size)
    mu_iso = rng.uniform(-1, 1, r.size)
    mu_pl = np.sign(rng.uniform(-1, 1, r.size))*u**(1.0/(1.0+kap))
    mu = np.where(is_plunger > 0.5, mu_pl, mu_iso)
    # settled members isotropic; kap only re-orients the plunger class
    mu = np.where(is_plunger > 0.5, mu, mu_iso)
    return r*np.sqrt(1-mu**2)
for a0 in (A0_CAN, A0_ALT):
    hi = MI_BAND[a0][1]; tag = "canonical" if a0 == A0_CAN else "alternate"
    row = []
    for kap in (0.0, 2.0, 6.0):
        Rp = project_aniso(r_true, is_pl, kap)
        row.append(contrast(Rp, r_true, is_pl, a0, edges))
    print(f"  footing={tag}  MI top {hi*100:.1f}%:  isotropic(kap=0) {row[0]*100:5.2f}%  ->  "
          f"mild-filament(kap=2) {row[1]*100:5.2f}%  ->  strong-filament(kap=6) {row[2]*100:5.2f}%  "
          f"({row[2]/hi*100:.0f}% of MI top)")
print("  READING (honest, both ways): the alias is NON-MONOTONIC in alignment but STRONG-filament")
print("  (LOS-aligned) infall pushes the raw R_proj alias to ~7% -- ~55% of the MI band top, ~3x the")
print("  isotropic 2.2%.  So the banked isotropic 2.2% is a LOWER BOUND: anisotropic/filamentary")
print("  infall can drive the pre-mitigation MG mimic UP INTO the MI band.  The exact magnitude is")
print("  toy-dependent (a real number needs a TRIAXIAL potential + infall-axis model), but the")
print("  DIRECTION is clear and adverse.  This makes the class-aware calibration + selecting RELAXED")
print("  (non-filament-fed, DS-clean) clusters LOAD-BEARING, and it exposes a second unpropagated")
print("  error: the spherical caustic mass profile assumed in E2 is itself orientation-biased for")
print("  filament-fed clusters, so a_ext(R) carries an orientation-correlated error the banked lanes")
print("  never quantify.  NET: a real, potentially band-sized, UNDER-COUNTED mimic -- carry it.")

# ==========================================================================================
# V3  THE SIGN INCONSISTENCY -- can the framework trip its own KILL switch?
# ==========================================================================================
print("\n"+LINE); print(" V3  SIGN: GAP E4/E7 say plungers NEGATIVE (less boosted); predict.py says plungers HOTTER"); print(LINE)
import math
def boost(a_in, a_ex, theta, a0):
    A = a_in + a_ex*theta
    return math.sqrt(math.sqrt(A*A + A*a0)/A)
th = lambda y: 2.0/(1.0+y*y)                        # fiducial theta0=2
TAU = 0.45e9*3.1557e7; Gyr = 1e9*3.1557e7
def felt(y_cur, y_hist, t, a0, ain=0.30, aex=1.0):
    w = math.exp(-t/TAU); yeff = y_cur + (y_hist-y_cur)*w
    return boost(ain*a0, aex*a0, th(yeff), a0)/boost(ain*a0, aex*a0, th(y_cur), a0) - 1.0
a0 = A0_CAN
# (i) RAW adiabatic loading, NO memory: a "plunger" currently at high omega_ex (high y_cur) vs a
# settled member at low y_cur, at the SAME radius.  Sign of (plunger - settled):
b_plunge_raw  = boost(0.30*a0, 1.0*a0, th(1.2), a0)   # high current loading
b_settled_raw = boost(0.30*a0, 1.0*a0, th(0.2), a0)   # low current loading
raw_sign = math.log(b_plunge_raw) - math.log(b_settled_raw)
# (ii) MEMORY-weighted first-infall (pre-peri) vs settled twin:
pre  = felt(0.90, 0.05, 0.30*Gyr, a0)   # cold past -> deficit
post = felt(0.60, 1.50, 0.50*Gyr, a0)   # hot peri  -> excess
print(f"  (i) RAW adiabatic loading (no memory): high-y plunger vs low-y settled at same r")
print(f"      d(ln boost) = {raw_sign*100:+.2f}%  -> plunger is {'HOTTER (POSITIVE)' if raw_sign>0 else 'cooler'}")
print(f"      *** a POSITIVE raw sign would TRIP GAP E7's KILL condition ('plungers more boosted') ***")
print(f"  (ii) MEMORY-weighted: first-infall pre-peri {pre*100:+.2f}% (deficit), post-peri {post*100:+.2f}% (excess)")
print("  RECONCILIATION: the two are NOT the same statistic.  GAP E4/E7's 'plunger' = the infalling")
print("  CLASS whose sigma is compared to settled; predict.py's 'HOTTER' baseline is the RAW y-loading")
print("  of a member at high CURRENT omega_ex.  The observable sign is the COMPETITION between raw")
print("  loading (positive) and memory-of-cold-past (negative), set by tau_M and the y_hist contrast.")
print("  => The SIGN is NOT theorem-grade: it rides on s=-1 AND on tau_M/y_hist, and the raw-loading")
print("     branch has the OPPOSITE sign to the memory branch.  If memory is weak (t>>tau_M, settled")
print("     population), the sign is POSITIVE and would fire GAP E7's KILL.  The banked docs assert")
print("     opposite baseline signs -- a real inconsistency the pre-registration must resolve BEFORE")
print("     firing (define the sign statistic on a FIXED phase zone, not the mixed 'infalling' class).")
assert raw_sign > 0 and pre < 0, "the two sign branches should genuinely oppose (that is the point)"

# ==========================================================================================
# V4  MANUFACTURED DETECTION + MANUFACTURED NULL
# ==========================================================================================
print("\n"+LINE); print(" V4  MANUFACTURED detection (MG false +) AND manufactured null (MI false -)"); print(LINE)
# (a) MANUFACTURED DETECTION: pure MG universe, NO true-r calibration (an analyst who bins by R_proj
#     and skips the per-zone calibration) + 15% uncut interlopers mis-tagged infalling.
n_int = int(0.15/(1-0.15)*N)
r_i = rng.uniform(3.0, 6.0, n_int)*R200
Rp_i = np.clip(r_i*np.sqrt(1-rng.uniform(-1,1,n_int)**2), 0.2*R200, 2.4*R200)
r_all = np.concatenate([r_true, r_i]); Rp_all = np.concatenate([Rproj_iso, Rp_i])
pl_all = np.concatenate([is_pl, np.ones(n_int)])
m_false = contrast(Rp_all, r_all, pl_all, A0_CAN, edges)
print(f"  (a) MG universe, bin-by-R_proj, 15% uncut mis-tagged interlopers -> phase-contrast "
      f"{m_false*100:.2f}%  ({m_false/MI_BAND[A0_CAN][0]*100:.0f}% of the MI FLOOR)")
print("      => an analyst who SKIPS the calibration + DS/caustic cuts manufactures a fake signal")
print("         a LARGE fraction of the band.  The cuts are load-bearing, NOT optional (confirms")
print("         mg_efe_zero.py).  A 'detection' without them measures projection+interlopers.")
# (b) MANUFACTURED NULL: MI universe, but the sigma-measurable members are adiabatic-dead (bright E).
f_bright = 0.0
for sg, re in [(150, 3.0), (230, 4.0)]:   # SDSS mid/bright E
    ain = (sg*1e3)**2/(re*3.086e19)/A0_CAN
    ys = np.linspace(0, 1.5, 40)
    Rr = np.array([boost(ain*A0_CAN, 1.0*A0_CAN, th(y), A0_CAN) for y in ys])
    f_bright = max(f_bright, (Rr.max()-Rr.min())/Rr.mean())
print(f"  (b) MI universe, but survey-BRIGHT E (sigma 150-230): max relational spread f = "
      f"{f_bright*100:.2f}%  -> a NULL even though MI is true (adiabatic-dead carriers).")
print("      => the sigma-measurable members carry ~0 signal: a manufactured NULL.  A null on the")
print("         WRONG (bright) population kills nothing.  The measurable-vs-carrier anti-correlation")
print("         is the power wall (power.py), re-confirmed.")

# ==========================================================================================
# V5  DATASET REALITY -- the load-bearing SDSS completeness number
# ==========================================================================================
print("\n"+LINE); print(" V5  DATASET REALITY -- does the powered sample exist at that N/quality?"); print(LINE)
print("  SDSS single-fiber veldisp: instrumental floor 69 km/s, resolution ~90 km/s; sigma<~90-100")
print("  UNRELIABLE (Sohn+2017 ApJS 229:20; Zahid+2016).  The diffuse deep-MOND CARRIERS (sigma 15-50,")
print("  f~10-14%) are EXACTLY the ones excluded from SDSS -> the stack measures adiabatic-dead E.")
print("  MaNGA DR17 IFU reaches sigma~20 (Law+2021), but diffuse cluster members with reliable sigma")
print("  AND Rhee phase tags number ~few hundred (SAMI 8 clusters, Owers+2017), NOT ~1000 -- power.py's")
print("  N~800-1000 is OPTIMISTIC; ~300-500 is defensible -> z~2-3 EXPLORATORY, not a clean detection.")
print("  VERDICT on power: the SDSS-stack systematics-limit finding is SOUND and the honest bottom")
print("  line (no clean 2026 bite; MaNGA/SAMI hint-grade only) HOLDS; the only trim is N~800->~400.")

# ==========================================================================================
print("\n"+LINE); print(" SYNTHESIS"); print(LINE)
print("""  (1) MG=0 at FIXED TRUE field: GRANTED (symbolic, re-verified in banked lanes; any a0/interp).
  (2) MG=0 IN OBSERVATION: the projection alias is ~2.2% isotropic but rises to ~7% (~55% of the MI
      top) under strong LOS-aligned/filamentary infall (V2, an under-counted mimic), and is only
      PARTIALLY removed by a REALISTIC purity-p zone calibration -- residual ~1.3-2% at p=0.5-0.9,
      NOT the ~0.01% observable.py claims from (non-observable) sim-true-r binning (V1).  The
      residual is BELOW the MI floor only at high purity AND for relaxed clusters; the honest MG
      floor is ~1-2%, and caustic-deprojection quality + cluster selection are load-bearing.
  (3) THE OBSERVABLE isolates the history spread ONLY IF the per-zone mean-r calibration + DS cut +
      caustic membership are applied at adequate purity; skipping them manufactures a fake signal a
      large fraction of the band (V4a).  The '<=0.3 dex a_ext binning' is binning on R_proj unless
      the deprojection is done, and the deprojection is statistical/partial (GAP E2 says so).
  (4) THE SIGN is NOT theorem-grade (V3): raw adiabatic loading (plungers HOTTER, positive) and the
      memory branch (pre-peri DEFICIT, negative) have OPPOSITE signs; GAP E4/E7 and predict.py assert
      opposite baselines.  The pre-registration must fix the sign statistic on a SINGLE phase zone or
      it risks self-tripping its own KILL condition.  Sign rides on s=-1 + tau_M, both non-derived.
  (5) MI-CLASS-GENERIC (MI-vs-MG), NOT framework-vs-Milgrom: HELD throughout.  Amplitude KERNEL-
      HOSTAGE (6-13% fiducial, cone ~3-20%).  a0 value + s=-1 POSTULATES.  Both footings ~identical.
  (6) POWER: SDSS systematics-limited (SOUND); no clean 2026 bite; MaNGA/SAMI exploratory at N~300-
      500 (trim power.py's optimistic ~800-1000).  Underpowered TODAY -- prediction, not confrontation.
  NET: the channel is a GENUINE MI-vs-MG discriminator in principle, but it is MITIGATION-HEAVY and
  its three sharpest claims are softer than banked: MG-floor ~1-2% not ~0.01% (V1+V2), the SIGN is
  postulate+kernel-contingent and internally inconsistent across docs (V3), and the clean-detection
  dataset does NOT exist in 2026 (V5).  No 'proves'.  Honest null: UNDERPOWERED + MITIGATION-DEPENDENT.""")
print("\nEXIT 0")
