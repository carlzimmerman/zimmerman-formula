#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP23 -- GALAXY-GALAXY LENSING UNDER THE CHAIN'S CURRENT ACTION WITH THE WEB'S EXTERNAL FIELD IN THE KERNEL: KiDS-1000's
isolated lenses (Brouwer+21, lead grade) at z = 0.25 and 0.4; H_K1's z = 0.7 KiDS prediction re-derived in the adopted
reading; BOSS-CMASS-like lenses on both sides of H_K1's switch (z = 0.5, 0.65); LCDM on the same footing.

WHY.  FP22 (bfe9a2fe5) adopted reading (b): FK1 sits on the Einstein-frame metric g~, so baryons source and feel the phantom and
the dark component feels Newtonian gravity only; lensing sees 2 (Phi_N[delta_m] + chi[f_b delta_b]).  FP22 D2 flagged a risk
no committed KiDS model includes: the web's band-passed field enters the (nonlinear) kernel of an isolated lens (the EFE is
intrinsic to the kernel).  Its estimate -- the 3D rms of the band-passed baryonic field at z = 0.25 applied as a uniform field,
QUMOND monopole, fixed bin masses, FP18's projection -- was d chi^2 ~ +205-232 in (b), an upper-side estimate that did not
model B21's isolation.  This lane computes it: the field's distribution at isolated lenses, the AQUAL kernel's response
(the chain's J_P2 root is AQUAL-type), FP20's exact projection, B21 at lead grade, both footings.  It then takes H_K1's
redshift structure (the yield switches on at z = 0.635) to massive-galaxy lensing, where BOSS CMASS spans the switch.

THE ACTION (README "the action as it stands", 08548fc85): the separator H_K1 (FP19): chi = (S_xi - S_B) phi, B = L^2/2,
  L = L_Lambda Omega_L(<K>_h) (L_Lambda = 2.9 Mpc), J_Y = J_P2 + 2 y_th sqrt(Y), y_th = c_y max(0, 2q) 4 pi G rho_bar L/a0
  (c_y = 2), zero below z = 0.635; reading (b) (FP22): the phantom is sourced by f_b delta_b and felt by baryons.
  The static scalar equation (FP7/FP9: J_P2 is AQUAL-type):  div[ J'(|grad phi|) grad phi ] = 4 pi G (1 - S_B) rho_b,
  J'(u) = X/(1 - 2X), X = u/a0 (equivalently |grad phi| = a0 X_P2(y) in spherical symmetry, y = g_N,bp/a0), the force on
  baryons is -(1 - S_B) grad phi (the output filter).  With the yield: J' X = y - y_th (a Bingham threshold).

PART K -- CONTROLS.  K1 FP20's projector (its source parsed and exec'd, sha256 recorded) against the singular isothermal
  sphere, NFW (Wright & Brainerd) and a point mass at the 15 KiDS radii.  K2 THE BRIDGE: with the web's field switched off
  this lane's lead-grade scorer reproduces FP20b's exact-projector H_K1 numbers (all-matter reading; z = 0.25/0.4/0.7, both
  footings) -- the isolated-lens term is reading-independent (FP22 D1) -- and, with FP6's committed projector, FP19's
  committed numbers.  K3 the engine (FP22's two-fluid TF, exec'd read-only) reproduces FP22's committed band-passed field
  y25 (H_K1, both readings, both footings).  K4 this lane's QUMOND monopole reproduces FP22 D's committed web-field d chi^2
  (uniform rms field, fixed bin masses, FP18's projection) -- the harness against FP22's own number.
PART A -- THE AQUAL KERNEL.  An axisymmetric finite-volume solver on (ln r, theta) for a band-passed point lens in a uniform
  external D-field g_e (the web's band-passed Newtonian baryonic field; its scalar gradient u_e = a0 X_P2(g_e/a0)); Newton
  with a 3x3-coloured finite-difference Jacobian; inner Neumann boundary D.r = a_N.r at 2 r_M (the lens field >= 1/y_e of
  the external there), outer Dirichlet phi = -u_e z at 40 L.  The stacked lens sees the MONOPOLE of the phantom: by
  Gauss's law its enclosed mass is the flux of grad phi through spheres (exact), and the output filter (1 - S_B) commutes
  with the rotation average (isotropic kernel), so the committed FP6 filter acts on the monopole exactly.  A1 isolated limit
  (y_e -> 0) = the spherical P2 law; A2 the far-field EFE: the AQUAL/QUMOND monopole ratio against the analytic linearised
  value (AQUAL: (1/J'_e) arcsin(e)/(e sqrt(1 + L_e)), e^2 = L_e/(1 + L_e), L_e = 1/(1 - 2X_e); QUMOND: (2/3) X_e/y_e +
  (1/3) X'(y_e); pure deep MOND pi/4 vs 5/6); A3 grid convergence; A4 the AQUAL/QUMOND tables used below.
PART W -- THE WEB'S FIELD AT KiDS LENSES (reading (b), H_K1, the engine's own two-fluid growth, CLASS spectrum).
  W1 WHERE THE FIELD COMES FROM: the band-passed field at a point is g = Int d^3x G rho_b delta_b(x) x^/|x|^2 w(|x|),
     w(r) = 1 - gfrac(r/L) (exact: Int_0^oo w j_1(kr) dr = (1 - e^(-k^2 L^2/2))/k); its variance split by source radius
     at B21's isolation radius (3 Mpc proper) -- inside, outside, the cross term.
  W2 HOW ISOLATION CONDITIONS IT (the conditioning, stated): a Gaussian-random-field Monte Carlo of the SAME linear fields
     (the engine's delta_m, delta_b at z; 256^3, 96 Mpc comoving; exact normalisation checked against the engine's rms).  A lens
     of B21 bin b is a local maximum of delta_m smoothed (top hat) on its Lagrangian radius R_l(M_h) with delta >= 1.686,
     M_h from M* (B21's bin means, M_gal inverted with B21's Eq. 23) by Moster, Naab & White 2013 (MNRAS 428, 3121, Eq. 2 and
     Table 1); B21's isolation (no neighbour with M* > 0.1 M*_lens within 3 Mpc) becomes: no local maximum of delta_m on the
     neighbour threshold's Lagrangian radius above 1.686 within 3 Mpc proper (x (1+z) comoving) outside the lens's own patch;
     the EXTERNAL field is the band-passed field minus that of the lens's own Lagrangian patch (r < R_l, direct sum: it
     collapses into the lens).  Variants: threshold x3, x10 (looser), radius x0.7, x1.3; and "low-density environment" (the
     lowest 26% of the 3 Mpc top-hat density at lens peaks, B21's isolated fraction).
  W3 the distribution's shape against Maxwell (a linear field's |g| is chi_3-distributed).
PART D -- KiDS WITH THE WEB'S FIELD (B21 Fig. 3, full corrected covariance, M_b free per bin on FP6's grid, FP20's exact
  projector, gate d chi^2 <= +9 against the isolated P2 law, as FP13/FP19/FP20b): the stacked monopole averaged over the
  Maxwell distribution of each bin's conditioned field, AQUAL kernel (QUMOND reported).  D1 the field KiDS tolerates
  (uniform sigma, every bin); D2 THE VERDICT with the conditioned fields; D3 the brackets (unconditioned; the exterior-only
  bound; QUMOND); D4 the directions of the approximations.
PART Z -- H_K1's z = 0.7 PREDICTION in reading (b) with the exact projector: the isolated term (= FP20b) and with the web's
  field (the yield: QUMOND form, as the committed yield law; the web's own linear field is below y_th at z = 0.7).
PART C -- BOSS-CMASS-LIKE LENSES at z = 0.5, 0.6, 0.65, 0.7 (both sides of the switch), 0.1-30 Mpc proper: hosts from White+11's
  CMASS central HOD (ApJ 728, 126: log M_cut = 13.08, sigma = 0.98, h^-1 Msun; satellites omitted) on a Sheth-Tormen mass function
  from CLASS; LCDM = NFW (Duffy+08 c(M200c), truncated at r200) + b xi_lin beyond r200 (b from the same HOD); the chain = central
  stars (M* = 10^11.4, Hernquist) + hot gas (beta = 2/3, r_c = 0.07 r200, f_bar(<r200) = 0.157) + the phantom (H_K1's band-pass and
  yield at z, the web's unconditioned field as EFE, QUMOND form for the extended source) + the retained carrier (FP16's
  numbers["X"] group_ret_z05 at v_k = 575, NFW inside r200) + the escaped carrier (spread over FP16's reach, a 5 Mpc proper sphere)
  + the 2-halo term with the engine's per-mode lensing/matter ratio dL_chain/dm_LCDM (the same clustering; the linear web phantom).
  Brackets: f_bar 0.10 and 0.06, v_k 650, the escaped carrier removed, M* 10^11.2 / 10^11.6, no web phantom in the 2-halo term,
  hosts x2 (M_cut + 0.3 dex).  C1 the ratio chain/LCDM(R) and its decomposition; C2 the change across the switch, split into the
  part below it (0.6/0.5: L(z) shrinking) and across it (0.65/0.6); C3 against the literature (no CMASS lensing data on disk --
  quoted, see DATA); the LCDM control is the construction's own LCDM with the quoted deficit.
W  the ledger.

DATA.  B21 (Brouwer+2021, A&A 650, A113): real_research/data/lensing_rar/brouwer2021_rar (as FP18/FP20).  No BOSS CMASS / LOWZ
  lensing measurement is on disk (searched: grep -ril "cmass|leauthaud|amon" over *.py/*.txt/*.csv/*.json; only XR32's cosmic-shear
  rows and unrelated hits).  Quoted, not recomputed: Leauthaud et al. 2017, MNRAS 467, 3024 (arXiv:1611.08606), abstract: CMASS
  clustering with standard galaxy-halo models "robustly predicts a lensing signal that is 20-40% larger than observed"
  (CFHTLenS + CS82, 0.43 < z < 0.7); Amon et al. 2023, MNRAS 518, 477 (arXiv:2202.07440), abstract: for the Planck cosmology
  (S8 = 0.83) the lensing/clustering amplitude A = 0.79 (+-0.03, DES+KiDS; 0.84 +- 0.05 HSC) and the "Lensing" cosmology
  (S8 = 0.76) is consistent with A = 1.  Their per-redshift-bin values (CMASS 0.43-0.54 / 0.54-0.70) are in the paper's tables and
  figures, NOT on disk.  To test the switch directly: SDSS DR12 BOSS galaxy_DR12v5_CMASS_North.fits.gz (+ randoms) from
  data.sdss.org/sas/dr12/boss/lss/, crossed with the on-disk KiDS-1000 shear catalogue (KiDS_DR4.1_SOM_gold_WL_cat.fits) --
  fetching it needs the user's go.

MUTATE=1 switches the web's field OFF in every lens kernel (the committed KiDS models' omission): the checks asserting what the
field does (D2) must FAIL (rc = 1).  Outputs FP23_galaxy_lensing_web_field_MUTATE.out / _results_MUTATE.json.

READ-ONLY IMPORTS: FP22's module head (up to its PART A) exec'd with file writes refused (its machinery: FP9 -> FP6, FP13 state,
FP18, CLASS, the TF engine, H_K1); the hub's XR21_pm_core.py is loaded from its COMMITTED blob (b4bf5b2ae; the working copy
carries an uncommitted additive class) and XR21_common.py as committed; FP20's projector source parsed; FP16/FP20b/FP22's
committed results JSON read.  sha256 of each in the results JSON.  No particle-mesh run; at most two threads.

HISTORY (disclosed).  Exploratory scratch runs (not committed) came first: a QUMOND sensitivity scan (d chi^2 vs a uniform field),
the source-radius split W1, the Monte Carlo W2 (two set-up bugs fixed before any number was used: a missing N^(3/2) in the
field normalisation, caught by the engine-rms check, and a sign error in the grid field, caught by the patch subtraction), and
the AQUAL solver (a Picard/Kacanov iteration has a limit cycle for this J' -- replaced by Newton; the inner boundary moved from
0.3 to 2 r_M where J' is not stiff).  The check directions and bounds below were set after those scratch numbers: W1 (>= 0.85
of the variance inside 3 Mpc, counting half the cross term), W2 (isolation moves the external field by <= 20%), D2 (asserts the
FAIL), A1 (2% of the linearised far field).  Development runs of this script by section (FP23_ONLY, not committed) followed: after
the first C run printed chain/LCDM ~ 2 at 1 Mpc and a 35% fall at 3 Mpc between z = 0.5 and 0.65, C gained its decomposition,
the no-web-phantom, f_bar = 0.06 and hosts-x2 brackets and z = 0.6 (to separate the switch from the smooth L(z)); D4 (the
L_Lambda scan) was added then; W1's printed measure was aligned with its condition.  No check direction changed after a
development run; every C and D4 check is reported, not load-bearing.  The literature numbers were checked against the two
abstracts by a web search (no file fetched).
Run from the repository root:  python3 real_research/derivation_chain_2026/FP23_galaxy_lensing_web_field.py  (MUTATE=1 for the control)
"""
import os, sys, io, re, json, math, time, types, hashlib, subprocess, contextlib, builtins, warnings

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "2"
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
from scipy.special import erf, erfc, spherical_jn
from scipy.interpolate import RegularGridInterpolator
from scipy.ndimage import maximum_filter
from scipy.spatial import cKDTree
from scipy.stats import chi as chi_dist

warnings.filterwarnings("ignore")
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
XRD = os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26")
MUTATE = os.environ.get("MUTATE", "0") == "1"
WEB_ON = not MUTATE
ONLY = set(os.environ.get("FP23_ONLY", "").split(",")) - {""}         # development convenience; the record runs everything
SLUG = "FP23_galaxy_lensing_web_field"
OUT = {"lane": "FP23", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": [], "provenance": {}}
CH = []
T0 = time.time()
_trap = getattr(np, "trapezoid", None) or np.trapz
FOOTS = ("canonical", "alt")


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 116 + "\n" + t + "\n" + "=" * 116)


def el():
    return f"[{time.time() - T0:.0f} s]"


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}{'' if load_bearing else '  (reported, not load-bearing)'}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def want(sec):
    return not ONLY or sec in ONLY


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    if isinstance(o, np.ndarray):
        return [jclean(v) for v in o.tolist()]
    if isinstance(o, float) and not math.isfinite(o):
        return str(o)
    return o


P(__doc__.split("PART K")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the web's field is switched OFF in every lens kernel (the committed KiDS models' omission) -- D2 must FAIL ***")

# ================================================================================================= provenance + machinery
sha = lambda b: hashlib.sha256(b).hexdigest()
_open = builtins.open


def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"FP23 refuses to write {file} from an imported lane")
    return _open(file, mode, *a, **k)


PM_REV = "b4bf5b2ae"
_pm_src = subprocess.check_output(["git", "show", f"{PM_REV}:real_research/cross_thread_review_2026_09_26/XR21_pm_core.py"], cwd=REPO)
_pm = types.ModuleType("XR21_pm_core"); _pm.__file__ = os.path.join(XRD, "XR21_pm_core.py")
exec(compile(_pm_src.decode(), _pm.__file__, "exec"), _pm.__dict__)
sys.modules["XR21_pm_core"] = _pm
OUT["provenance"]["XR21_pm_core.py"] = {"sha256": sha(_pm_src), "source": f"git blob {PM_REV} (committed)",
                                       "working_copy_sha256": sha(open(os.path.join(XRD, "XR21_pm_core.py"), "rb").read())}
OUT["provenance"]["XR21_common.py"] = {"sha256": sha(open(os.path.join(XRD, "XR21_common.py"), "rb").read()), "status": "committed"}
P22 = os.path.join(HERE, "FP22_who_feels_mond.py")
_src22 = open(P22).read()
_cut22 = _src22.index("# ================================================================================================= PART A")
NS = {"__file__": P22, "__name__": "fp22_head", "open": _ro_open}
_old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(_src22[:_cut22], P22, "exec"), NS)
finally:
    os.environ["MUTATE"] = _old if _old is not None else "0"
OUT["provenance"]["FP22_head"] = {"sha256": sha(_src22[:_cut22].encode()), "file_sha256": sha(_src22.encode())}
P20 = os.path.join(HERE, "FP20_esd_projection_fix.py")
_src20 = open(P20).read()
_a20, _b20 = _src20.index("def shell_mats(edges, Rv):"), _src20.index("class M2Fix:")
NS20 = {"np": np, "math": math}
exec(compile(_src20[_a20:_b20], P20, "exec"), NS20)
ESDFix = NS20["ESDFix"]
OUT["provenance"]["FP20_projector"] = {"sha256": sha(_src20[_a20:_b20].encode()), "file_sha256": sha(_src20.encode())}
for fn in ("FP16_daughter_reaccretion_results.json", "FP20b_rescore_fp15_fp16_fp19_results.json", "FP22_who_feels_mond_results.json",
           "FP19_hs_repair_results.json"):
    OUT["provenance"][fn] = {"sha256": sha(open(os.path.join(HERE, fn), "rb").read())}
F16X = json.load(open(os.path.join(HERE, "FP16_daughter_reaccretion_results.json")))["numbers"]["X"]
F20b = json.load(open(os.path.join(HERE, "FP20b_rescore_fp15_fp16_fp19_results.json")))["numbers"]["R3_FP19"]["H1"]
F22D = json.load(open(os.path.join(HERE, "FP22_who_feels_mond_results.json")))["numbers"]["D"]

M6, ns9, F18 = NS["M6"], NS["ns9"], NS["F18"]
A0, FB, SEP, TF, KX, DX, ZS = NS["A0"], NS["FB"], NS["SEP_HK1"], NS["TF"], NS["KX"], NS["DX"], NS["ZS"]
CLS, h_, Om, H0, OmL_a, gfield, LL = NS["CLS"], NS["h_"], NS["Om"], NS["H0"], NS["OmL_a"], NS["gfield"], NS["HK1_LL"]
RR, RP, RG, MPCm, PCm, MS6, LM = M6["RR"], M6["RP"], M6["RG"], M6["MPCm"], M6["PCm"], M6["MS6"], M6["LM"]
_Rd, _Ed, _Sd, _Ci, G6, gfr, Fmat, YIELD = M6["_Rd"], M6["_Ed"], M6["_Sd"], M6["_Ci"], M6["G6"], M6["gfrac_smooth"], M6["Fmat"], ns9["YIELD"]
RHO_C0 = 3 * H0 ** 2 / (8 * math.pi * G6)                                      # kg/m^3
RHO_M0_MSUN = Om * RHO_C0 * MPCm ** 3 / MS6                                     # Msun/Mpc^3 (comoving)
KIDS_TOL = 9.0
P(f"\n  machinery: FP22 head exec'd read-only (XR21_pm_core from {PM_REV}, sha256 {OUT['provenance']['XR21_pm_core.py']['sha256'][:12]}...); "
  f"FP20's projector parsed (sha256 {OUT['provenance']['FP20_projector']['sha256'][:12]}...); a0 {A0['canonical']:.4e} / {A0['alt']:.4e}; "
  f"H_K1 L_Lambda {LL} Mpc; f_b {FB:.4f}   {el()}")


def Lm_of(z):
    return LL * OmL_a(1 / (1 + z)) * MPCm                                       # H_K1's L [m, proper]


def yth_of(z, f):
    return SEP[f].yth(1 / (1 + z))


# ================================================================================================= the engine runs (reading a, b; LCDM)
ZRUN = tuple(sorted(set(ZS) | {0.65}))
RUNS = {}
for f in FOOTS:
    for rd_, be_ in (("a", 0.0), ("b", 1.0)):
        RUNS[(f, rd_)] = TF(KX, be_, "real", SEP[f], A0[f], Tfac=1.0).run(DX, ZRUN)
REFL = TF(KX, 0.0, "lcdm", Tfac=1.0).run(DX, ZRUN)
SIGU = {(f, z): RUNS[(f, "b")][z]["y"] * A0[f] for f in FOOTS for z in (0.25, 0.4, 0.5, 0.6, 0.65, 0.7)}   # 3D rms [m/s^2]
P("  the web's band-passed baryonic field (reading b, H_K1, 3D rms / a0): " + "; ".join(
    f"{f[:3]} z {z}: {SIGU[(f, z)] / A0[f]:.3e}" for f in FOOTS for z in (0.25, 0.4, 0.5, 0.65, 0.7)) + f"   {el()}")
OUT["numbers"]["sigma_U"] = {f"{f}/{z}": SIGU[(f, z)] / A0[f] for f in FOOTS for z in (0.25, 0.4, 0.5, 0.65, 0.7)}

# ================================================================================================= the kernel: QUMOND tables, AQUAL solver
MU = np.linspace(-1, 1, 801)


def xP2(D):
    D = np.maximum(np.asarray(D, float), 0.0)
    return np.where(D > 0, 1.0 / (1.0 + np.sqrt(1.0 + 1.0 / np.maximum(D, 1e-300))), 0.0)


def F_mono(yb, ye, yth=0.0):
    """(1/2) Int dmu X(|y| - y_th)/|y| (y_b + y_e mu): the raw QUMOND monopole flux per a0 r^2 (y_b radial, y_e uniform)."""
    yb = np.asarray(yb, float)[..., None]
    yt = np.sqrt(np.maximum(yb ** 2 + ye ** 2 + 2 * yb * ye * MU, 0.0))
    return _trap(xP2(yt - yth) / np.maximum(yt, 1e-300) * (yb + ye * MU), MU, axis=-1) / 2.0


class FTable:
    """F(y_b, y_e): exact X(y_b - y_th) times the tabulated EFE ratio (y_th = 0), or F itself (y_th > 0: the field can re-open it)."""

    def __init__(self, yth=0.0, lyb=np.linspace(-14, 5, 761), lye=np.linspace(-8, -1, 141)):
        self.lyb, self.lye, self.yth = lyb, lye, yth
        tab = np.empty((len(lyb), len(lye)))
        for j, le in enumerate(lye):
            tab[:, j] = F_mono(10 ** lyb, 10 ** le, yth)
        f0 = F_mono(10 ** lyb, 0.0, yth)
        R = np.where(f0[:, None] > 0, tab / np.maximum(f0, 1e-300)[:, None], 0.0)
        self.itpR = RegularGridInterpolator((lyb, lye), R, bounds_error=False, fill_value=None)
        self.itpF = RegularGridInterpolator((lyb, lye), tab, bounds_error=False, fill_value=None)

    def __call__(self, yb, ye):
        yb = np.asarray(yb, float); out = np.zeros_like(yb); m = yb > 1e-14
        if ye <= 10 ** self.lye[0]:
            out[m] = xP2(yb[m] - self.yth); return out
        pts = np.column_stack([np.log10(np.minimum(yb[m], 10 ** self.lyb[-1])), np.full(int(m.sum()), min(math.log10(ye), self.lye[-1]))])
        out[m] = np.clip(self.itpF(pts), 0.0, None) if self.yth > 0 else xP2(yb[m]) * np.clip(self.itpR(pts), 0.0, None)
        return out


_FT = {}


def FT(yth):
    k = round(float(yth), 12)
    if k not in _FT:
        _FT[k] = FTable(k)
    return _FT[k]


TMX = np.linspace(0.0, 6.5, 66)[1:]                                               # Maxwell nodes: t = |g_e|/sigma_1
WMX = math.sqrt(2 / math.pi) * TMX ** 2 * np.exp(-TMX ** 2 / 2); WMX = WMX / WMX.sum()


def gfrac(x):
    x = np.asarray(x, float); return erf(x / math.sqrt(2)) - math.sqrt(2 / math.pi) * x * np.exp(-x * x / 2)


class AqualEFE:
    """AQUAL (J_P2) for a band-passed point lens in a uniform external D-field; dimensionless: r in Mpc, fields in a0."""

    def __init__(self, x_in, x_out, Ns=170, Nt=36):
        self.se = np.linspace(math.log(x_in), math.log(x_out), Ns + 1); self.sc = 0.5 * (self.se[1:] + self.se[:-1])
        self.re, self.rc = np.exp(self.se), np.exp(self.sc)
        self.te = np.linspace(0, math.pi, Nt + 1); self.tc = 0.5 * (self.te[1:] + self.te[:-1])
        self.mc = np.cos(self.tc); me = np.cos(self.te); self.dmu = me[:-1] - me[1:]
        self.Ns, self.Nt = Ns, Nt
        self.dsc, self.dtc, self.dr, self.sinf = np.diff(self.sc), np.diff(self.tc), np.diff(self.re), np.sin(self.te[1:-1])
        I = np.arange(Ns * Nt).reshape(Ns, Nt); self.I = I
        self.rows = np.concatenate([I[:-1, :].ravel(), I[1:, :].ravel(), I[:, :-1].ravel(), I[:, 1:].ravel(), I.ravel()])
        self.cols = np.concatenate([I[1:, :].ravel(), I[:-1, :].ravel(), I[:, 1:].ravel(), I[:, :-1].ravel(), I.ravel()])

    def setup(self, m, Ld, ye):
        self.m, self.Ld, self.ye = m, Ld, ye
        GMf = m * (1 - gfrac(self.re / Ld)) if Ld else np.full(len(self.re), m)  # g_bp r^2 at the s-edges
        self.ue = float(xP2(ye)) if ye > 0 else 0.0
        S = (GMf[1:] - GMf[:-1])[:, None] * self.dmu[None, :]
        S[0, :] += (GMf[0] / self.re[0] ** 2 - ye * self.mc) * self.re[0] ** 2 * self.dmu
        self.S, self.phi_bc = S, -self.ue * self.re[-1] * self.mc
        self.floor = 1e-3 * max(self.ue, 1e-12)

    def _Jp(self, X):
        X = np.clip(X, 0.0, 0.495); return np.maximum(X / (1 - 2 * X), self.floor)

    def assemble(self, phi):
        re, rc, Ns, Nt = self.re, self.rc, self.Ns, self.Nt
        dphr = (phi[1:, :] - phi[:-1, :]) / (re[1:-1, None] * self.dsc[:, None])
        gt = np.empty_like(phi)
        gt[:, 1:-1] = (phi[:, 2:] - phi[:, :-2]) / ((self.tc[2:] - self.tc[:-2])[None, :] * rc[:, None])
        gt[:, 0] = (phi[:, 1] - phi[:, 0]) / ((self.tc[1] - self.tc[0]) * rc); gt[:, -1] = (phi[:, -1] - phi[:, -2]) / ((self.tc[-1] - self.tc[-2]) * rc)
        Js = self._Jp(np.sqrt(dphr ** 2 + (0.5 * (gt[1:, :] * rc[1:, None] + gt[:-1, :] * rc[:-1, None]) / re[1:-1, None]) ** 2))
        dpht = (phi[:, 1:] - phi[:, :-1]) / (rc[:, None] * self.dtc[None, :])
        gr = np.empty_like(phi)
        gr[1:-1, :] = (phi[2:, :] - phi[:-2, :]) / ((self.sc[2:] - self.sc[:-2])[:, None] * rc[1:-1, None])
        gr[0, :] = (phi[1, :] - phi[0, :]) / (self.dsc[0] * rc[0]); gr[-1, :] = (phi[-1, :] - phi[-2, :]) / (self.dsc[-1] * rc[-1])
        Jt = self._Jp(np.sqrt(dpht ** 2 + (0.5 * (gr[:, 1:] + gr[:, :-1])) ** 2))
        dpho = (self.phi_bc - phi[-1, :]) / (re[-1] * (self.se[-1] - self.sc[-1]))
        Jo = self._Jp(np.sqrt(dpho ** 2 + (gt[-1, :] * rc[-1] / re[-1]) ** 2))
        As = Js * re[1:-1, None] * self.dmu[None, :] / self.dsc[:, None]
        At = Jt * self.sinf[None, :] * self.dr[:, None] / self.dtc[None, :]
        Ao = Jo * re[-1] * self.dmu / (self.se[-1] - self.sc[-1])
        diag = np.zeros((Ns, Nt)); diag[:-1, :] -= As; diag[1:, :] -= As; diag[:, :-1] -= At; diag[:, 1:] -= At; diag[-1, :] -= Ao
        b = self.S.copy(); b[-1, :] -= Ao * self.phi_bc
        vals = np.concatenate([As.ravel(), As.ravel(), At.ravel(), At.ravel(), diag.ravel()])
        return sps.csc_matrix((vals, (self.rows, self.cols)), shape=(Ns * Nt, Ns * Nt)), b.ravel()

    def residual(self, phi):
        A, b = self.assemble(phi); return A @ phi.ravel() - b

    def jacobian(self, x, r0):
        Ns, Nt, I = self.Ns, self.Nt, self.I
        ii, jj = np.meshgrid(np.arange(Ns), np.arange(Nt), indexing="ij")
        rows, cols, vals = [], [], []
        h = 1e-7 * max(1.0, float(np.max(np.abs(x))))
        for ci in range(3):
            for cj in range(3):
                e = np.zeros((Ns, Nt)); e[((ii % 3) == ci) & ((jj % 3) == cj)] = h
                dr = ((self.residual(x.reshape(Ns, Nt) + e) - r0) / h).reshape(Ns, Nt)
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        i2, j2 = ii + di, jj + dj
                        ok = (i2 >= 0) & (i2 < Ns) & (j2 >= 0) & (j2 < Nt) & ((i2 % 3) == ci) & ((j2 % 3) == cj)
                        rows.append(I[ok]); cols.append(I[i2[ok], j2[ok]]); vals.append(dr[ok])
        return sps.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(Ns * Nt, Ns * Nt))

    def solve(self, m, Ld, ye, tol=1e-10, npic=6, omega=0.5, maxnewt=30):
        self.setup(m, Ld, ye); Ns, Nt, rc = self.Ns, self.Nt, self.rc
        ur = xP2(m * (1 - (gfrac(rc / Ld) if Ld else 0.0)) / rc ** 2)
        phis = np.concatenate([[0.0], np.cumsum(0.5 * (ur[1:] + ur[:-1]) * np.diff(rc))]); phis -= phis[-1]
        phi = phis[:, None] - self.ue * rc[:, None] * self.mc[None, :]
        for _ in range(npic):                                                       # a few damped Picard steps (warm start)
            A, b = self.assemble(phi); phi = phi + omega * (spla.spsolve(A, b).reshape(Ns, Nt) - phi)
        scale = float(np.sum(np.abs(self.S))); x = phi.ravel().copy(); r = self.residual(x.reshape(Ns, Nt)); nr = float(np.linalg.norm(r))
        for _ in range(maxnewt):
            if nr / scale < tol:
                break
            dx = spla.spsolve(self.jacobian(x, r), -r)
            if not np.all(np.isfinite(dx)):
                A, b = self.assemble(x.reshape(Ns, Nt)); dx = spla.spsolve(A, b) - x
            lam = 1.0
            for _ in range(20):
                xn = x + lam * dx; rn = self.residual(xn.reshape(Ns, Nt)); nn = float(np.linalg.norm(rn))
                if nn < (1 - 1e-4 * lam) * nr:
                    break
                lam *= 0.5
            x, r, nr = xn, rn, nn
        self.phi, self.resid = x.reshape(Ns, Nt), nr / scale
        dphr = (self.phi[1:, :] - self.phi[:-1, :]) / (self.re[1:-1, None] * self.dsc[:, None])
        return 0.5 * np.sum(dphr * self.dmu[None, :], axis=1) * self.re[1:-1] ** 2   # enclosed raw phantom [a0 Mpc^2/G] at re[1:-1]


# ================================================================================================= the KiDS lead-grade scorer
FIX = ESDFix(RR, RP, PCm, MS6)
RPM = RP / MPCm


def esd_exact(M, Mb):
    return FIX(M, Mb)


def esd_committed(M, Mb):
    return M6["esd_of_M"](M, Mb)[1]


def kids_chi2(model_b, esd=esd_exact):
    """FP6's kids_chi2 (L341 F7): M_b free per bin on FP6's grid LM (diagonal selection), full corrected covariance; model_b(b, Mb_kg)
    -> the total enclosed mass on RR [kg] for bin b (a bin-dependent web field enters here)."""
    mods, best_lm = [], []
    for b in range(4):
        best = None
        for lm in LM:
            Mb = 10 ** lm * MS6
            mk = np.interp(_Rd[b], RPM, esd(model_b(b, Mb), Mb)); c_ = float(np.sum(((_Ed[b] - mk) / _Sd[b]) ** 2))
            if best is None or c_ < best[0]:
                best = (c_, mk, lm)
        mods.append(best[1]); best_lm.append(best[2])
    dv = np.concatenate(_Ed) - np.concatenate(mods)
    return float(dv @ _Ci @ dv), best_lm


def filtered(Mraw, L_m):
    """FP6's output filter (1 - S_L) on an enclosed-mass profile on RG (exact on the monopole: the kernel is isotropic)."""
    return Mraw - (Fmat(L_m) @ np.diff(Mraw) + Mraw[0] * gfr(RG / L_m))


def raw_q(Mb, a0, L_m, yth, sig3):
    """the Maxwell-averaged raw QUMOND monopole [kg] on RG of a band-passed point lens in the web's field (3D rms sig3)."""
    yb = G6 * Mb * (1 - (gfr(RG / L_m) if L_m else 0.0)) / RG ** 2 / a0
    tab = FT(yth)
    if not sig3 > 0:
        return tab(yb, 0.0) * a0 * RG ** 2 / G6
    s1 = sig3 / math.sqrt(3.0) / a0
    return sum(w * tab(yb, s1 * t) for t, w in zip(TMX, WMX)) * a0 * RG ** 2 / G6


AQT = {}                                                                          # (foot, z) -> {lm: (r [Mpc], log ye grid, R[ye, r])}
LYE = np.arange(-6.5, -2.49, 0.5)


def raw_aq(Mb, a0, L_m, sig3, key):
    """the Maxwell-averaged raw AQUAL monopole [kg] on RG: QUMOND x the solved AQUAL/QUMOND ratio (interpolated in log y_e)."""
    yb = G6 * Mb * (1 - gfr(RG / L_m)) / RG ** 2 / a0
    tab = FT(0.0)
    if not sig3 > 0:
        return tab(yb, 0.0) * a0 * RG ** 2 / G6
    lm = round(math.log10(Mb / MS6), 6)
    r_s, lye, Rm = AQT[key][lm]
    s1 = sig3 / math.sqrt(3.0) / a0
    lr = np.log(RG / MPCm); out = np.zeros_like(RG)
    for t, w in zip(TMX, WMX):
        ye = s1 * t
        if ye <= 10 ** lye[0]:
            Rr = np.ones_like(RG)
        else:
            x = min(math.log10(ye), lye[-1]); j = min(int(np.searchsorted(lye, x)), len(lye) - 1); j = max(j, 1)
            fr = (x - lye[j - 1]) / (lye[j] - lye[j - 1]); Rrow = (1 - fr) * Rm[j - 1] + fr * Rm[j]
            Rr = np.interp(lr, np.log(r_s), Rrow, left=1.0, right=Rrow[-1])
        out += w * tab(yb, ye) * Rr
    return out * a0 * RG ** 2 / G6


def sep_hk1(LLx, f):
    """H_K1 with another declared length (the tied yield carries L as well)."""
    hk = lambda a, k: 1.0 - np.exp(-0.5 * (k * h_ * LLx * OmL_a(a) / a) ** 2)
    yt = lambda a: 2.0 * max(0.0, NS["_two_q"](a)) * 1.5 * H0 ** 2 * (Om / a ** 3 + NS["Or"] / a ** 4) * LLx * OmL_a(a) * NS["Mpc"] / A0[f]
    return NS["Sep"](f"H_K1 (L_Lambda {LLx})", hk, yt, nconst=1)


def kids_web(f, z, sig_b, kernel="aqual", esd=esd_exact, LLx=None):
    """KiDS lead-grade chi^2 for lenses at z under H_K1 in reading (b) with the web's field of 3D rms sig_b[b] (m/s^2) per bin."""
    L_m, yth = Lm_of(z), yth_of(z, f); a0 = A0[f]
    if LLx is not None:
        L_m, yth, kernel = LLx * OmL_a(1 / (1 + z)) * MPCm, sep_hk1(LLx, f).yth(1 / (1 + z)), "qumond"
    cache = {}

    def model_b(b, Mb):
        s = float(sig_b[b]) if WEB_ON else 0.0
        k = (round(s, 22), round(math.log10(Mb / MS6), 6))
        if k not in cache:
            if kernel == "aqual" and yth <= 0:
                raw = raw_aq(Mb, a0, L_m, s, (f, z))
            else:
                raw = raw_q(Mb, a0, L_m, yth, s)
            cache[k] = Mb + np.interp(RR, RG, filtered(raw, L_m))
        return cache[k]
    return kids_chi2(model_b, esd)


KB = {f: kids_chi2(lambda b, Mb, f=f: Mb + np.interp(RR, RG, M6["phantom"](Mb, A0[f])))[0] for f in FOOTS}         # isolated P2
KB_C = {f: kids_chi2(lambda b, Mb, f=f: Mb + np.interp(RR, RG, M6["phantom"](Mb, A0[f])), esd_committed)[0] for f in FOOTS}
P(f"  KiDS reference (isolated P2, no band-pass): chi^2 {KB['canonical']:.2f} / {KB['alt']:.2f} (exact projector); "
  f"{KB_C['canonical']:.2f} / {KB_C['alt']:.2f} (FP6's committed)   {el()}")

# ================================================================================================= PART K
if want("K"):
    banner("K  CONTROLS: the projector, the bridge to FP20b/FP19, the engine vs FP22, the harness vs FP22 D")
    # K1 -- the analytic standard at the 15 KiDS radii
    VS = 200e3; KS = VS ** 2 / G6; RT = RR[-1]
    sis = FIX(KS * np.minimum(RR, RT), 0.0); RDm = _Rd[0] * MPCm
    sis_true = np.interp(_Rd[0], RPM, sis)
    RRF = np.geomspace(1e-5, 30.0, 16000) * MPCm; FIXF = ESDFix(RRF, RDm, PCm, MS6)
    sis_ref = FIXF(KS * np.minimum(RRF, RT), 0.0)
    Mpt = 1e11 * MS6; pt = np.interp(_Rd[0], RPM, FIX(np.full(len(RR), Mpt), Mpt)); pt_an = Mpt / (math.pi * RDm ** 2) * PCm ** 2 / MS6
    M200n, cn = 1e13 * MS6, 5.0
    rho_c = RHO_C0; r200 = (3 * M200n / (4 * math.pi * 200 * rho_c)) ** (1 / 3); rs = r200 / cn
    mfn = lambda x: np.log(1 + x) - x / (1 + x); rhos = M200n / (4 * math.pi * rs ** 3 * mfn(cn))
    Mn = lambda r: 4 * math.pi * rhos * rs ** 3 * mfn(np.asarray(r) / rs)

    def wb(R):                                                                 # Wright & Brainerd 2000, untruncated NFW Delta Sigma
        x = R / rs; out = np.empty_like(x)
        for i, xi in enumerate(x):
            if xi < 1:
                g = 8 * math.atanh(math.sqrt((1 - xi) / (1 + xi))) / (xi ** 2 * math.sqrt(1 - xi ** 2)) + 4 / xi ** 2 * math.log(xi / 2) - 2 / (xi ** 2 - 1) \
                    + 4 * math.atanh(math.sqrt((1 - xi) / (1 + xi))) / ((xi ** 2 - 1) * math.sqrt(1 - xi ** 2))
            else:
                g = 8 * math.atan(math.sqrt((xi - 1) / (1 + xi))) / (xi ** 2 * math.sqrt(xi ** 2 - 1)) + 4 / xi ** 2 * math.log(xi / 2) - 2 / (xi ** 2 - 1) \
                    + 4 * math.atan(math.sqrt((xi - 1) / (1 + xi))) / ((xi ** 2 - 1) ** 1.5)
            out[i] = rs * rhos * g
        return out * PCm ** 2 / MS6
    RRL = np.geomspace(1e-5, 3e3, 30000) * MPCm; FIXL = ESDFix(RRL, RDm, PCm, MS6)
    nfw_n = FIXL(Mn(RRL), 0.0); nfw_a = wb(RDm)
    d_sis = float(np.max(np.abs(sis_true / sis_ref - 1))); d_pt = float(np.max(np.abs(pt / pt_an - 1))); d_nfw = float(np.max(np.abs(nfw_n / nfw_a - 1)[_Rd[0] < 2.0]))
    check("K1 CONTROL: FP20's exact projector (source parsed) reproduces a point mass and an untruncated NFW (Wright & Brainerd 2000; "
          "R < 2 Mpc, grid to 3 Gpc) analytically, and the truncated SIS against a 16,000-shell reference, at the 15 KiDS radii, to < 0.2%",
          f"point mass {d_pt:.1e}, NFW {d_nfw:.1e}, SIS vs fine reference {d_sis:.1e}", max(d_pt, d_nfw, d_sis) < 2e-3)
    OUT["numbers"]["K1"] = dict(point=d_pt, nfw=d_nfw, sis=d_sis)

    # K2 -- the bridge
    br = {}
    for f in FOOTS:
        for z in (0.25, 0.4, 0.7):
            sig0 = [0.0] * 4
            ex = kids_web(f, z, sig0, kernel="qumond")[0] - KB[f]
            cm = kids_web(f, z, sig0, kernel="qumond", esd=esd_committed)[0] - KB_C[f]
            key = {0.25: "kids", 0.4: "kids@0.4", 0.7: "kids@0.7"}[z]
            br[(f, z)] = dict(exact=ex, committed=cm, fp20b=F20b[key]["after"][f], fp19=F20b[key]["before"][f])
    dev_b = max(abs(v["exact"] - v["fp20b"]) for v in br.values()); dev_c = max(abs(v["committed"] - v["fp19"]) for v in br.values())
    P("    web field off (= the committed lanes): " + "; ".join(f"{f[:3]} z {z}: {v['exact']:+.3f} (FP20b {v['fp20b']:+.3f}), committed projector "
                                                            f"{v['committed']:+.3f} (FP19 {v['fp19']:+.3f})" for (f, z), v in br.items()))
    check("K2 THE BRIDGE: with the web's field switched off, this lane's lead-grade scorer reproduces FP20b's exact-projector H_K1 KiDS "
          "numbers (z = 0.25/0.4/0.7, both footings; FP20b's all-matter re-run -- the isolated-lens term is the same in reading (b), FP22 D1) "
          "and, with FP6's committed projector, FP19's committed numbers",
          f"max |dev| exact vs FP20b {dev_b:.1e}; committed vs FP19 {dev_c:.1e}", dev_b < 0.01 and dev_c < 0.01)
    OUT["numbers"]["K2"] = {f"{f}/{z}": v for (f, z), v in br.items()}

    # K3 -- the engine vs FP22's committed band-passed field
    k3 = {(f, rd_): (RUNS[(f, rd_)][0.25]["y"] * A0[f], F22D["gext"][f"H_K1/{f}/{rd_}"]) for f in FOOTS for rd_ in ("a", "b")}
    d3 = max(abs(v[0] / v[1] - 1) for v in k3.values())
    check("K3 CONTROL: the engine (FP22's TF, exec'd read-only, CLASS spectrum) reproduces FP22's committed band-passed field at z = 0.25 "
          "(H_K1, readings (a) and (b), both footings)", "; ".join(f"{k_[0][:3]}/{k_[1]}: {v[0]:.4e} vs {v[1]:.4e}" for k_, v in k3.items())
          + f"; max rel dev {d3:.1e}", d3 < 1e-6)

    # K4 -- FP22 D's committed number through this lane's QUMOND monopole (uniform rms field, fixed masses, FP18's projection)
    def chi2_18(model):
        r_ = (model - F18.KE).ravel(); return float(r_ @ np.linalg.solve(F18.C60, r_))
    LGM, rgM = F18.LGM, RG / MPCm
    k4 = {}
    for f in FOOTS:
        L_m = LL * OmL_a(0.8) * MPCm; ge = F22D["gext"][f"H_K1/{f}/b"]
        mi, me = [], []
        for b in range(4):
            Mb = 10 ** F18.B21_MGAL[b] * LGM
            ph = np.maximum(M6["phantom"](Mb, A0[f], L_m, 0.0, YIELD), 0.0)
            gb_ = G6 * Mb * (1 - gfr(RG / L_m)) / RG ** 2 / A0[f]
            R_ = np.where(F_mono(gb_, 0.0) > 0, F_mono(gb_, ge / A0[f]) / np.maximum(F_mono(gb_, 0.0), 1e-300), 1.0)
            Mg12 = 10 ** F18.B21_MGAL[b] / 1e12
            mi.append(F18.esd_of(lambda r, ph=ph: Mg12 + np.interp(np.log(np.maximum(r, rgM[0])), np.log(rgM), ph / LGM / 1e12)))
            me.append(F18.esd_of(lambda r, ph=ph, R_=R_: Mg12 + np.interp(np.log(np.maximum(r, rgM[0])), np.log(rgM), ph * R_ / LGM / 1e12)))
        k4[f] = (chi2_18(np.array(me)) - chi2_18(np.array(mi)), F22D["kids"][f"H_K1/{f}"]["efe_b"] - F22D["kids"][f"H_K1/{f}"]["iso"])
    d4 = max(abs(v[0] - v[1]) for v in k4.values())
    check("K4 CONTROL: this lane's QUMOND monopole reproduces FP22 D's committed web-field cost in reading (b) with FP22's own recipe "
          "(3D rms as a uniform field, the filtered isolated phantom scaled by the raw ratio, B21's fixed bin masses, FP18's projection)",
          "; ".join(f"{f[:3]}: {v[0]:+.2f} vs FP22 {v[1]:+.2f}" for f, v in k4.items()) + f"; max |dev| {d4:.2f}", d4 < 0.5)
    OUT["numbers"]["K34"] = dict(K3={"/".join(k_): v for k_, v in k3.items()}, K4=k4)

# ================================================================================================= PART A
if want("A"):
    banner("A  THE AQUAL KERNEL: limits, the far-field EFE against the linearised solution, convergence, the tables")
    MPC = MPCm
    a0c = A0["canonical"]; Mt = 10 ** 10.57 * MS6; mt = G6 * Mt / (a0c * MPC ** 2); Lt = Lm_of(0.25) / MPC
    s_ = AqualEFE(2 * math.sqrt(mt), 40 * Lt); Ma = s_.solve(mt, Lt, 1e-9); r_ = s_.re[1:-1]
    Mq = F_mono(mt * (1 - gfrac(r_ / Lt)) / r_ ** 2, 1e-9) * r_ ** 2
    sel = (r_ < 3 * Lt)
    dA1 = float(np.max(np.abs(Ma - Mq)[sel]) / np.max(np.abs(Mq[sel])))
    # far field, unfiltered lens, several y_e
    ffr = {}
    for ye in (3e-5, 3e-4):
        re_ = math.sqrt(mt / ye); s2 = AqualEFE(2 * math.sqrt(mt), 3000 * re_, Ns=240, Nt=40); M2_ = s2.solve(mt, None, ye); rr2 = s2.re[1:-1]
        Mq2 = F_mono(mt / rr2 ** 2, ye) * rr2 ** 2
        k_ = int(np.argmin(np.abs(rr2 - 30 * re_))); num = M2_[k_] / Mq2[k_]
        Xe = float(xP2(ye)); Le = 1 / (1 - 2 * Xe); Jpe = Xe / (1 - 2 * Xe); e_ = math.sqrt(Le / (1 + Le))
        Afac = (1 / Jpe) * math.asin(e_) / (e_ * math.sqrt(1 + Le))
        dX = (float(xP2(ye * 1.0001)) - float(xP2(ye * 0.9999))) / (ye * 0.0002)
        Qfac = (2 / 3) * Xe / ye + (1 / 3) * dX
        ffr[ye] = dict(numeric=num, analytic=Afac / Qfac, resid=s2.resid)
    dA2 = max(abs(v["numeric"] / v["analytic"] - 1) for v in ffr.values())
    # grid convergence at a KiDS-like case
    s3a = AqualEFE(2 * math.sqrt(mt), 40 * Lt, Ns=170, Nt=36); Ma3 = s3a.solve(mt, Lt, 3e-4); ra3 = s3a.re[1:-1]
    s3b = AqualEFE(2 * math.sqrt(mt), 40 * Lt, Ns=300, Nt=60); Mb3 = s3b.solve(mt, Lt, 3e-4); rb3 = s3b.re[1:-1]
    xs = np.geomspace(0.05, 2.6, 12)
    dA3 = float(np.max(np.abs(np.interp(np.log(xs), np.log(ra3), Ma3) / np.interp(np.log(xs), np.log(rb3), Mb3) - 1)))
    P(f"    isolated limit: max |AQUAL - spherical P2| / max = {dA1:.1e}; far field (r = 30 r_e, unfiltered): " + "; ".join(
        f"y_e {ye:.0e}: AQUAL/QUMOND {v['numeric']:.4f} vs linearised {v['analytic']:.4f}" for ye, v in ffr.items())
      + f" (pure deep MOND (pi/4)/(5/6) = {math.pi / 4 / (5 / 6):.4f}); grid 170x36 vs 300x60: {dA3:.1e}   {el()}")
    check("A1 THE AQUAL SOLVER: the isolated limit reproduces the spherical P2 law (< 1e-3), the far-field EFE monopole matches the "
          "linearised AQUAL/QUMOND ratio (< 2%), and the monopole is grid-converged at the KiDS radii (< 0.5%)",
          f"isolated {dA1:.1e}; far field {dA2:.1e}; grid {dA3:.1e}", dA1 < 1e-3 and dA2 < 0.02 and dA3 < 5e-3)
    OUT["numbers"]["A1"] = dict(isolated=dA1, farfield={str(k_): v for k_, v in ffr.items()}, grid=dA3)
    # A4 -- the tables: every M_b of FP6's grid x y_e, both footings, z = 0.25, 0.4
    nbad, nsol, worst = 0, 0, 0.0
    for f in FOOTS:
        a0 = A0[f]
        for z in (0.25, 0.4):
            Ld = Lm_of(z) / MPC; tabs = {}
            for lm in LM:
                Mb = 10 ** lm * MS6; m = G6 * Mb / (a0 * MPC ** 2)
                sol = AqualEFE(2 * math.sqrt(m), 40 * Ld)
                rows = []
                for le in LYE:
                    ye = 10 ** le; Mr = sol.solve(m, Ld, ye); rs_ = sol.re[1:-1]
                    Mq_ = F_mono(m * (1 - gfrac(rs_ / Ld)) / rs_ ** 2, ye) * rs_ ** 2
                    rows.append(np.where(np.abs(Mq_) > 1e-12 * np.max(np.abs(Mq_)), Mr / np.where(Mq_ == 0, 1, Mq_), 1.0))
                    nsol += 1; nbad += int(sol.resid > 1e-6); worst = max(worst, sol.resid)
                tabs[round(lm, 6)] = (rs_, LYE, np.array(rows))
            AQT[(f, z)] = tabs
    P(f"    AQUAL/QUMOND tables: {nsol} solves (21 masses x {len(LYE)} fields x 2 footings x 2 epochs); unconverged (resid > 1e-6): {nbad}; "
      f"worst residual {worst:.1e}   {el()}")
    rep = AQT[("canonical", 0.25)][round(LM[8], 6)]
    P("    e.g. log M_b = %.1f, z = 0.25: AQUAL/QUMOND raw monopole at 0.1/0.5/1/2 Mpc for y_e = 1e-4.5 / 1e-3.5: " % LM[8]
      + " | ".join(" ".join(f"{np.interp(math.log(x), np.log(rep[0]), rep[2][j]):.3f}" for x in (0.1, 0.5, 1.0, 2.0)) for j in (4, 6)))
    check("A4 (reported) the AQUAL/QUMOND tables converged", f"{nsol - nbad}/{nsol} converged; worst residual {worst:.1e}", nbad == 0, load_bearing=False)

# ================================================================================================= PART W
MSTAR_B = []
for b in range(4):                                                               # B21's bin M* from the mean M_gal (B21 Eq. 23 inverted)
    lo, hi = 8.0, 11.5
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if F18.bos(mid) < F18.B21_MGAL[b] else (lo, mid)
    MSTAR_B.append(0.5 * (lo + hi))


def moster13_mstar(Mh, z):
    a = z / (1 + z); M1 = 10 ** (11.590 + 1.195 * a); N = 0.0351 - 0.0247 * a; be = 1.376 - 0.826 * a; ga = 0.608 + 0.329 * a
    return Mh * 2 * N / ((Mh / M1) ** (-be) + (Mh / M1) ** ga)


def mh_of_mstar(lms, z):
    lg = np.linspace(10.0, 15.5, 5501); return float(np.interp(lms, np.log10(moster13_mstar(10 ** lg, z)), lg))


def lag_radius(lMh):
    return (3 * 10 ** lMh / (4 * math.pi * RHO_M0_MSUN)) ** (1 / 3)               # comoving Mpc


class Box:
    """a periodic Gaussian realisation of the engine's linear delta_m, delta_b at z (numpy irfftn: <|D_k|^2> = N^6 P/V)."""

    def __init__(self, N, Lbox, Dm, Db, seed):
        self.N, self.Lb = N, Lbox
        k1 = 2 * math.pi * np.fft.fftfreq(N, d=Lbox / N); kz = 2 * math.pi * np.fft.rfftfreq(N, d=Lbox / N)
        self.kx, self.ky, self.kz = k1[:, None, None], k1[None, :, None], kz[None, None, :]
        self.k = np.sqrt(self.kx ** 2 + self.ky ** 2 + self.kz ** 2); kk = np.maximum(self.k, 1e-12)
        lk = np.log(KX * h_)
        Pm = 2 * math.pi ** 2 * np.exp(np.interp(np.log(kk), lk, np.log(np.maximum(Dm, 1e-300)))) ** 2 / kk ** 3
        Tb = np.exp(np.interp(np.log(kk), lk, np.log(np.maximum(Db, 1e-300) / np.maximum(Dm, 1e-300))))
        wk = np.fft.rfftn(np.random.default_rng(seed).standard_normal((N, N, N)))
        self.dmk = wk * np.sqrt(N ** 3 * Pm / Lbox ** 3); self.dmk[0, 0, 0] = 0.0
        self.dbk = self.dmk * Tb

    def smooth_th(self, R):
        x = self.k * R; W = np.where(x > 1e-6, 3 * (np.sin(x) - x * np.cos(x)) / np.maximum(x, 1e-6) ** 3, 1.0)
        return np.fft.irfftn(self.dmk * W, s=(self.N,) * 3)

    def db_x(self):
        return np.fft.irfftn(self.dbk, s=(self.N,) * 3)

    def bp_field(self, Lcom, rho_b, a):
        kk = np.maximum(self.k, 1e-12); hk = 1 - np.exp(-0.5 * (self.k * Lcom) ** 2); pref = 4 * math.pi * G6 * rho_b * a * MPCm
        out = []
        for kc in (self.kx, self.ky, self.kz):
            gk = 1j * kc / kk ** 2 * self.dbk * hk * pref; gk[0, 0, 0] = 0.0          # g = -grad Phi: toward overdensity
            out.append(np.fft.irfftn(gk, s=(self.N,) * 3))
        return np.stack(out, axis=-1)


def local_maxima(d, thr):
    return np.argwhere((d == maximum_filter(d, size=3, mode="wrap")) & (d >= thr))


ISO_VAR = ((1.0, 1.0), (3.0, 1.0), (10.0, 1.0), (1.0, 0.7), (1.0, 1.3))           # (threshold x, radius x); (1, 1) = B21's criterion
GN, GL = 256, 96.0
SEEDS = {"canonical": (20260927, 20260928), "alt": (20260929,)}
RB = {}                                                                          # (f, z) -> conditioned ratio per bin
MC = {}
if want("W") or want("D") or want("Z"):
    banner("W  THE WEB'S FIELD AT KiDS LENSES: where it comes from (W1), how B21's isolation conditions it (W2), its shape (W3)")
    # ---------------------------------------------------------------------------------------- W1
    w1 = {}
    for f in FOOTS:
        for z in (0.25, 0.4):
            a = 1 / (1 + z); r_ = RUNS[(f, "b")][z]; Gk = gfield(FB * r_["db"], a, KX); hk = SEP[f].hk(a, KX)
            Lp = Lm_of(z) / MPCm; kph = KX * h_ / a
            rr = np.concatenate([np.linspace(1e-4, 0.02, 50), np.geomspace(0.02, 60 * Lp, 4000)[1:]]); w = 1 - gfr(rr / Lp)
            Iin = np.array([_trap(w[rr <= 3.0] * spherical_jn(1, k * rr[rr <= 3.0]), rr[rr <= 3.0]) for k in kph])
            Itot = np.array([_trap(w * spherical_jn(1, k * rr), rr) for k in kph])
            lk = np.log(KX); Iout = Itot - Iin
            vt = _trap((Gk * hk) ** 2, lk); vin = _trap((Gk * kph * Iin) ** 2, lk); vout = _trap((Gk * kph * Iout) ** 2, lk)
            cov = _trap(Gk ** 2 * kph ** 2 * Iin * Iout, lk); rho = cov / math.sqrt(vin * vout)
            w1[(f, z)] = dict(sig=math.sqrt(vt) / A0[f], f_in=vin / vt, f_out=vout / vt, f_cov=2 * cov / vt, rho=rho,
                              sig_E=math.sqrt(vout * (1 - rho ** 2)) / A0[f], kernel_check=float(np.max(np.abs(kph * Itot - hk)[kph < 50])))
    P("    variance of the band-passed field by source radius (3 Mpc proper): " + "; ".join(
        f"{f[:3]} z {z}: inside {v['f_in']:.3f}, outside {v['f_out']:.4f}, cross {v['f_cov']:.3f} (rho {v['rho']:.2f}); exterior-only "
        f"conditional rms {v['sig_E']:.2e} a0 of {v['sig']:.2e}" for (f, z), v in w1.items()))
    OUT["numbers"]["W1"] = {f"{f}/{z}": v for (f, z), v in w1.items()}
    check("W1 DERIVED: THE BAND-PASS LOCALISES THE WEB'S FIELD -- >= 85% of the band-passed field's variance at a point is sourced within "
          "B21's 3 Mpc isolation radius (z = 0.25 and 0.4, both footings; the real-space kernel checked against the Fourier band-pass)",
          "; ".join(f"{f[:3]} z {z}: inside {v['f_in']:.3f} + half the cross term {0.5 * v['f_cov']:.3f} = {v['f_in'] + 0.5 * v['f_cov']:.3f}, "
                    f"outside {v['f_out']:.4f}; kernel check {v['kernel_check']:.0e}"
                    for (f, z), v in w1.items()),
          all(v["f_in"] + 0.5 * v["f_cov"] >= 0.85 and v["kernel_check"] < 1e-3 for v in w1.values()),
          reading="so B21's isolation is what decides -- if it removed the sources inside 3 Mpc, the field would drop to the exterior-only rms")

    # ---------------------------------------------------------------------------------------- W2
    for f in FOOTS:
        for z in (0.25, 0.4, 0.7):
            a = 1 / (1 + z); r_ = RUNS[(f, "b")][z]; Lcom = Lm_of(z) / MPCm / a; rho_b = FB * Om * RHO_C0 / a ** 3
            acc = {b: {"all": [], "var": {v: ([], []) for v in ISO_VAR}, "low": [], "rest": []} for b in range(4)}
            sU_box = []
            for seed in SEEDS[f]:
                box = Box(GN, GL, r_["dm"], r_["db"], seed)
                g = box.bp_field(Lcom, rho_b, a); gm = np.sqrt(np.sum(g ** 2, axis=-1)); db = box.db_x(); cell = GL / GN
                sU_box.append(math.sqrt(float(np.mean(gm ** 2))))
                d3 = box.smooth_th(3.0 / a); pk_cache = {}
                for b in range(4):
                    lMh = mh_of_mstar(MSTAR_B[b], z); Rl = lag_radius(lMh)
                    pk = local_maxima(box.smooth_th(Rl), 1.686)
                    n_ = int(Rl / cell) + 1
                    off = np.argwhere(np.ones((2 * n_ + 1,) * 3)) - n_; dist = np.linalg.norm(off * cell, axis=1); s_ = (dist > 0) & (dist < Rl)
                    off, dist = off[s_], dist[s_]
                    wgt = ((1 - gfr(dist / Lcom)) * G6 * rho_b * (cell * MPCm * a) ** 3 / (dist * MPCm * a) ** 2)[:, None] * (off / dist[:, None])
                    ge = np.empty(len(pk))
                    for i0 in range(0, len(pk), 256):
                        P_ = pk[i0:i0 + 256]; idx = (P_[:, None, :] + off[None, :, :]) % GN
                        dv = db[idx[..., 0], idx[..., 1], idx[..., 2]]
                        gin = np.einsum("pn,nc->pc", dv, wgt)
                        ge[i0:i0 + 256] = np.linalg.norm(g[P_[:, 0], P_[:, 1], P_[:, 2]] - gin, axis=1)
                    acc[b]["all"].append(ge)
                    env = d3[pk[:, 0], pk[:, 1], pk[:, 2]]; lo_ = env <= np.quantile(env, 0.26)
                    acc[b]["low"].append(ge[lo_]); acc[b]["rest"].append(ge[~lo_])
                    for (fm, fr) in ISO_VAR:
                        lMt = mh_of_mstar(MSTAR_B[b] - 1 + math.log10(fm), z); Rt = lag_radius(lMt)
                        kc = round(Rt, 4)
                        if kc not in pk_cache:
                            pk_cache[kc] = local_maxima(box.smooth_th(Rt), 1.686)
                        pt = pk_cache[kc]; tree = cKDTree(pt * cell, boxsize=GL); Riso = 3.0 / a * fr
                        lists = tree.query_ball_point(pk * cell, Riso)
                        nl = np.array([len(l_) for l_ in lists]); iso = np.ones(len(pk), bool)
                        if nl.sum() > 0:
                            pi_ = np.repeat(np.arange(len(pk)), nl); pj_ = np.concatenate([np.asarray(l_, int) for l_ in lists if len(l_)])
                            dd_ = np.linalg.norm(((pt[pj_] - pk[pi_] + GN / 2) % GN - GN / 2) * cell, axis=1)
                            iso[np.unique(pi_[dd_ > Rl])] = False                  # a neighbour peak outside the lens's own patch
                        acc[b]["var"][(fm, fr)][0].append(ge[iso]); acc[b]["var"][(fm, fr)][1].append(ge[~iso])
                del box, g, gm, db, d3
            sU = float(np.mean(sU_box))
            rms = lambda x: math.sqrt(float(np.mean(np.concatenate(x) ** 2))) / sU if sum(len(y) for y in x) > 0 else float("nan")
            res = {}
            for b in range(4):
                allg = np.concatenate(acc[b]["all"]); s1 = math.sqrt(float(np.mean(allg ** 2)) / 3)
                vv = {}
                for v in ISO_VAR:
                    ni = sum(len(y) for y in acc[b]["var"][v][0]); nt = ni + sum(len(y) for y in acc[b]["var"][v][1])
                    vv[v] = dict(n_iso=ni, frac=ni / max(nt, 1), iso=rms(acc[b]["var"][v][0]), non=rms(acc[b]["var"][v][1]))
                good = [vv[v]["iso"] for v in ISO_VAR if vv[v]["n_iso"] >= 50]
                res[b] = dict(n=len(allg), all=rms(acc[b]["all"]), var=vv, low=rms(acc[b]["low"]), rest=rms(acc[b]["rest"]),
                              fav=min(good) if good else rms(acc[b]["all"]), base=vv[(1.0, 1.0)]["iso"], base_n=vv[(1.0, 1.0)]["n_iso"],
                              p_low=float(np.mean(allg < 0.25 * sU)), p_low_maxwell=float(chi_dist.cdf(0.25 * sU / s1, 3)))
            MC[(f, z)] = dict(sU_box=sU / A0[f], sU_engine=SIGU[(f, z)] / A0[f], bins=res)
            RB[(f, z)] = [res[b]["fav"] for b in range(4)]
            P(f"    {f[:3]} z {z}: box rms {sU / A0[f]:.3e} a0 (engine {SIGU[(f, z)] / A0[f]:.3e}); external field at lens peaks / sigma_U per bin: "
              + " | ".join(f"b{b + 1} n {res[b]['n']}: all {res[b]['all']:.3f}, B21-crit iso {res[b]['base']:.3f} (n {res[b]['base_n']}), "
                           f"most favourable {res[b]['fav']:.3f}, low-density {res[b]['low']:.3f}" for b in range(4)) + f"   {el()}")
    OUT["numbers"]["W2"] = {f"{f}/{z}": dict(sU_box=v["sU_box"], sU_engine=v["sU_engine"],
                                            bins={str(b): dict(n=r_["n"], all=r_["all"], fav=r_["fav"], base=r_["base"], base_n=r_["base_n"],
                                                               low=r_["low"], rest=r_["rest"], p_low=r_["p_low"], p_low_maxwell=r_["p_low_maxwell"],
                                                               var={f"x{k_[0]:g}/Rx{k_[1]:g}": vv for k_, vv in r_["var"].items()})
                                                  for b, r_ in v["bins"].items()}) for (f, z), v in MC.items()}
    spread = []
    for (f, z), v in MC.items():
        for b, r_ in v["bins"].items():
            for k_, vv in r_["var"].items():
                if vv["n_iso"] >= 50:
                    spread.append(vv["iso"] / r_["all"])
            spread.append(r_["low"] / r_["all"])
    dnorm = max(abs(v["sU_box"] / v["sU_engine"] - 1) for v in MC.values())
    check("W2 DERIVED (linear theory, the conditioning stated in the docstring): B21's ISOLATION BARELY MOVES THE FIELD -- at lens peaks the "
          "external band-passed field (the lens's own Lagrangian patch removed) changes by <= 20% under every isolation variant with >= 50 "
          "isolated lenses (isolated fractions 0.1-100%) and under the low-density selection (Gaussian: a dipole is independent of a monopole); "
          "the box reproduces the engine's rms (< 1%)",
          f"isolated or low-density / all lens peaks: {min(spread):.3f}-{max(spread):.3f} over {len(spread)} cells; box/engine rms max dev {dnorm:.1e}",
          all(0.8 <= s <= 1.2 for s in spread) and dnorm < 0.01,
          reading="isolation removes neighbour PEAKS, not the smooth quasi-linear density slope at ~L that sources the band-passed field; "
                  "W1's 'inside 3 Mpc' is that slope, so the exterior-only rms is not what isolation delivers")
    pl = [(r_["p_low"], r_["p_low_maxwell"]) for v in MC.values() for r_ in v["bins"].values()]
    check("W3 (reported) the external field's distribution is Maxwellian (P(|g| < 0.25 sigma_U), Monte Carlo vs chi_3 at the same rms)",
          ", ".join(f"{p:.3f}/{q:.3f}" for p, q in pl), max(abs(p - q) for p, q in pl) < 0.02, load_bearing=False)

# ================================================================================================= PART D
DV = {}
if want("D"):
    banner("D  KiDS WITH THE WEB'S FIELD: the field KiDS tolerates (D1), the verdict with the conditioned field (D2), brackets (D3)")
    SC = (0.0, 1e-5, 2e-5, 3e-5, 5e-5, 7e-5, 1e-4, 1.5e-4, 2e-4, 3e-4, 4e-4)
    thr = {}
    for f in FOOTS:
        for z in (0.25, 0.4):
            row = [kids_web(f, z, [s * A0[f]] * 4)[0] - KB[f] for s in SC]
            cross = next((i for i in range(1, len(SC)) if row[i] > KIDS_TOL >= row[i - 1]), None)
            sstar = (SC[cross - 1] + (KIDS_TOL - row[cross - 1]) * (SC[cross] - SC[cross - 1]) / (row[cross] - row[cross - 1])) if cross else (float("inf") if row[-1] <= KIDS_TOL else 0.0)
            thr[(f, z)] = dict(scan=row, sigma_star=sstar)
            P(f"    {f[:3]} z {z}: d chi^2 vs a uniform web field (3D rms / a0) " + ", ".join(f"{s:.0e}: {v:+.1f}" for s, v in zip(SC, row))
              + f"  -> tolerated sigma* = {sstar:.2e} a0   {el()}")
    OUT["numbers"]["D1"] = {f"{f}/{z}": v for (f, z), v in thr.items()}
    check("D1 (reported) THE FIELD KiDS TOLERATES (AQUAL kernel, Maxwell-averaged, every bin the same rms): sigma* per footing and epoch",
          "; ".join(f"{f[:3]} z {z}: {v['sigma_star']:.2e} a0 ({v['sigma_star'] * A0[f]:.1e} m/s^2)" for (f, z), v in thr.items()), True,
          load_bearing=False)
    cases = {}
    for f in FOOTS:
        for z in (0.25, 0.4):
            sU = SIGU[(f, z)]
            fav = [RB[(f, z)][b] * sU for b in range(4)]
            base = [MC[(f, z)]["bins"][b]["base"] * sU for b in range(4)]
            allp = [MC[(f, z)]["bins"][b]["all"] * sU for b in range(4)]
            sE = OUT["numbers"]["W1"][f"{f}/{z}"]["sig_E"] * A0[f]
            c_ = {}
            c_["conditioned (most favourable isolation, AQUAL)"] = kids_web(f, z, fav)[0] - KB[f]
            c_["conditioned (B21 criterion, AQUAL)"] = kids_web(f, z, base)[0] - KB[f]
            c_["lens peaks, no isolation (AQUAL)"] = kids_web(f, z, allp)[0] - KB[f]
            c_["unconditioned random point (AQUAL)"] = kids_web(f, z, [sU] * 4)[0] - KB[f]
            c_["exterior-only bound (AQUAL)"] = kids_web(f, z, [sE] * 4)[0] - KB[f]
            c_["conditioned (most favourable, QUMOND)"] = kids_web(f, z, fav, kernel="qumond")[0] - KB[f]
            c_["web field off (= FP20b)"] = kids_web(f, z, [0.0] * 4, kernel="qumond")[0] - KB[f]
            eff = math.sqrt(sum(x ** 2 for x in fav) / 4) / A0[f]
            c_["s*"] = thr[(f, z)]["sigma_star"] / eff if eff > 0 else float("inf")
            cases[(f, z)] = c_
            P(f"    {f[:3]} z {z}: " + "; ".join(f"{k_} {v:+.1f}" for k_, v in c_.items() if k_ != "s*")
              + f"; the conditioned field must shrink x{1 / max(c_['s*'], 1e-9):.1f} to pass   {el()}")
    DV.update(cases)
    OUT["numbers"]["D2"] = {f"{f}/{z}": v for (f, z), v in cases.items()}
    key = "conditioned (most favourable isolation, AQUAL)"
    fails = {k_: v[key] > KIDS_TOL for k_, v in cases.items()}
    check("D2 KiDS FAILS WITH THE WEB'S FIELD (reading (b), H_K1): with the band-passed baryonic field at B21-like isolated lens peaks "
          "(the most favourable isolation variant per bin; Maxwell-averaged; AQUAL kernel; M_b free per bin; exact projector) d chi^2 exceeds "
          "the +9 gate at z = 0.25 and 0.4 on both footings",
          "; ".join(f"{f[:3]} z {z}: {v[key]:+.1f}" for (f, z), v in cases.items()), all(fails.values()),
          reading="the committed KiDS passes (FP13/FP19/FP20b) hold only with the web's field omitted from the kernel; the exterior-only "
                  "bound (every source inside 3 Mpc silenced) is the one reading that passes, and linear theory does not deliver it (W2)")
    check("D3 (reported) THE BRACKETS: unconditioned (FP22's upper side, now Maxwell/AQUAL/M_b-free) and the exterior-only lower bound; "
          "QUMOND vs AQUAL",
          "; ".join(f"{f[:3]} z {z}: random point {v['unconditioned random point (AQUAL)']:+.1f}, exterior-only {v['exterior-only bound (AQUAL)']:+.1f}, "
                    f"QUMOND {v['conditioned (most favourable, QUMOND)']:+.1f} vs AQUAL {v[key]:+.1f}" for (f, z), v in cases.items()), True,
          load_bearing=False)

    # D4 -- can the separator's one declared length rescue it?  (QUMOND kernel: the chain-favourable form; W2's ratios at 2.9 Mpc)
    d4 = {}
    for LLx in (2.0, 2.4, 2.8, 2.9, 3.5, 4.6):
        for f in FOOTS:
            rr_ = TF(KX, 1.0, "real", sep_hk1(LLx, f), A0[f], Tfac=1.0).run(DX, (0.25, 0.4))
            for z in (0.25, 0.4):
                sU = rr_[z]["y"] * A0[f]; fav = [RB[(f, z)][b] * sU for b in range(4)]
                d4[(LLx, f, z)] = dict(sigU=sU / A0[f], iso=kids_web(f, z, [0.0] * 4, LLx=LLx)[0] - KB[f], web=kids_web(f, z, fav, LLx=LLx)[0] - KB[f])
        P(f"    L_Lambda {LLx}: " + "; ".join(f"{f[:3]} z {z}: sigma_U {d4[(LLx, f, z)]['sigU']:.2e}, isolated {d4[(LLx, f, z)]['iso']:+.1f}, with the web "
                                           f"{d4[(LLx, f, z)]['web']:+.1f}" for f in FOOTS for z in (0.25, 0.4)) + f"   {el()}")
    OUT["numbers"]["D4"] = {f"{k_[0]}/{k_[1]}/{k_[2]}": v for k_, v in d4.items()}
    okL = [LLx for LLx in (2.0, 2.4, 2.8, 2.9, 3.5, 4.6) if all(d4[(LLx, f, z)]["web"] <= KIDS_TOL for f in FOOTS for z in (0.25, 0.4))]
    check("D4 (reported) THE SEPARATOR'S DECLARED LENGTH CANNOT RESCUE IT: L_Lambda = 2.0-4.6 Mpc (FP20b's window is [2.8, 4.6]) with the "
          "conditioned web field (QUMOND kernel, W2's 2.9-Mpc ratios): the lengths passing KiDS at z = 0.25 AND 0.4 on both footings",
          f"passing: {okL if okL else 'none'}", True, load_bearing=False)

# ================================================================================================= PART Z
if want("Z"):
    banner("Z  H_K1's z = 0.7 KiDS PREDICTION in reading (b), exact projector: the isolated term and the web's field (the yield on)")
    zz = {}
    for f in FOOTS:
        sU = SIGU[(f, 0.7)]; yth = yth_of(0.7, f)
        fav = [RB[(f, 0.7)][b] * sU for b in range(4)] if (f, 0.7) in RB else [sU] * 4
        zz[f] = dict(iso=kids_web(f, 0.7, [0.0] * 4, kernel="qumond")[0] - KB[f], web=kids_web(f, 0.7, fav, kernel="qumond")[0] - KB[f],
                     web_U=kids_web(f, 0.7, [sU] * 4, kernel="qumond")[0] - KB[f], yth=yth, sigU=sU / A0[f])
    P("    " + "; ".join(f"{f[:3]}: y_th(0.7) {v['yth']:.2e} vs the web's rms {v['sigU']:.2e}; isolated {v['iso']:+.1f}, with the conditioned web field "
                          f"{v['web']:+.1f} (unconditioned {v['web_U']:+.1f})" for f, v in zz.items()) + f"   {el()}")
    OUT["numbers"]["Z"] = zz
    check("Z1 (reported) THE z = 0.7 PREDICTION in reading (b) with the exact projector: the isolated term equals FP20b's (+500/+524; the "
          "reading does not touch it) and the web's field moves it (the kernel's argument |g_lens + g_web| can re-cross the yield)",
          "; ".join(f"{f[:3]}: {v['iso']:+.1f} -> {v['web']:+.1f}" for f, v in zz.items()), True, load_bearing=False)

# ================================================================================================= PART C
if want("C"):
    banner("C  BOSS-CMASS-LIKE LENSES ACROSS THE SWITCH (z = 0.5, 0.65): the chain (reading (b), H_K1) vs LCDM on the same footing")
    Rc = np.geomspace(0.1, 30.0, 36)                                             # proper Mpc
    RRc = np.geomspace(1e-4, 400.0, 6000) * MPCm
    FIXC = ESDFix(RRc, Rc * MPCm, PCm, MS6)
    rgc = RG
    # the HOD (White+11) on a Sheth-Tormen mass function from CLASS
    lMg = np.linspace(12.3, 15.3, 31); Mg = 10 ** lMg                            # Msun
    kkc = np.geomspace(1e-4, 50.0, 3000)                                         # 1/Mpc

    def pk_lin(z):
        return np.array([CLS.pk_lin(k, z) for k in kkc])

    def sigma_R(R, pk):
        x = kkc * R; W = np.where(x > 1e-6, 3 * (np.sin(x) - x * np.cos(x)) / np.maximum(x, 1e-6) ** 3, 1.0)
        return math.sqrt(_trap(kkc ** 3 * pk / (2 * math.pi ** 2) * W ** 2, np.log(kkc)))

    def st_weights(z, dlcut=0.0):
        pk = pk_lin(z); R = (3 * Mg / (4 * math.pi * RHO_M0_MSUN)) ** (1 / 3); sg = np.array([sigma_R(r, pk) for r in R])
        nu = 1.686 / sg; aa, pp, AA = 0.707, 0.3, 0.3222
        nuf = AA * np.sqrt(2 * aa * nu ** 2 / math.pi) * (1 + (aa * nu ** 2) ** (-pp)) * np.exp(-aa * nu ** 2 / 2)
        dlnnu = np.gradient(np.log(nu), np.log(Mg)); dndlnM = RHO_M0_MSUN / Mg * nuf * np.abs(dlnnu)
        bias = 1 + (aa * nu ** 2 - 1) / 1.686 + 2 * pp / (1.686 * (1 + (aa * nu ** 2) ** pp))
        Mcut = 10 ** (13.08 + dlcut) / h_; Ncen = 0.5 * erfc(np.log(Mcut / Mg) / (math.sqrt(2) * 0.98))
        w = dndlnM * Ncen; w = w / w.sum()
        return w, float(np.sum(w * bias)), pk

    def xi_of(r_com, dk, ratio=None):
        """xi(r) = Int Delta^2(k) R(k) j0(kr) dlnk on a linear k grid (Gaussian damping at 20/Mpc)."""
        kl = np.linspace(1e-4, 30.0, 60001); pkl = np.exp(np.interp(np.log(kl), np.log(kkc), np.log(dk)))
        rr_ = 1.0 if ratio is None else np.interp(np.log(kl), np.log(KX * h_), ratio)
        integ = kl ** 2 * pkl * rr_ * np.exp(-(kl / 20.0) ** 2) / (2 * math.pi ** 2)
        return np.array([_trap(integ * np.sinc(kl * r / math.pi), kl) for r in r_com])

    rx = np.geomspace(0.05, 300.0, 400)                                          # proper Mpc for xi
    ret = {v: (np.array([float(k_) for k_ in F16X[v]["group_ret_z05"]]), np.array(list(F16X[v]["group_ret_z05"].values()))) for v in ("575", "650")}

    def X_ret(M, vk):
        m_, x_ = ret[vk]; return float(np.exp(np.interp(math.log(M), np.log(m_), np.log(x_))))

    def nfw_M(r, M200, c, r200):
        rs = r200 / c; mf = lambda x: np.log(1 + x) - x / (1 + x)
        return M200 * mf(np.minimum(r, r200) / rs) / mf(c)

    def ph_ext(Mb_RG, a0, L_m, yth, sig3):
        """the phantom of an extended spherical baryon profile (enclosed mass on RG): band-pass, kernel with the web's field, output filter."""
        Mbp = Mb_RG - (Fmat(L_m) @ np.diff(Mb_RG) + Mb_RG[0] * gfr(RG / L_m))
        yb = np.maximum(G6 * Mbp / RG ** 2 / a0, 0.0); tab = FT(yth)
        if sig3 > 0 and WEB_ON:
            s1 = sig3 / math.sqrt(3) / a0; raw = sum(w * tab(yb, s1 * t) for t, w in zip(TMX, WMX))
        else:
            raw = tab(yb, 0.0)
        return filtered(raw * a0 * RG ** 2 / G6, L_m)

    def dsig(Mprof_RRc):
        return FIXC(Mprof_RRc, 0.0)

    cm = {}
    for z in (0.5, 0.6, 0.65, 0.7):
        a = 1 / (1 + z); w0_, bgal, pk = st_weights(z); w2_, bgal2, _ = st_weights(z, 0.3); dk = pk
        rho_m = Om * RHO_C0 / a ** 3; rho_cz = 3 * (H0 * NS["Ez"](a)) ** 2 / (8 * math.pi * G6)
        xi_l = xi_of(rx / a, pk)
        out_z, R2h = {}, {}
        for f in FOOTS:
            Rchain = RUNS[(f, "b")][z]["dL"] / REFL[z]["dm"]; xi_c = xi_of(rx / a, pk, Rchain)
            R2h[f] = [float(np.interp(math.log(k), np.log(KX), Rchain)) for k in (0.1, 0.3, 1.0, 3.0)]
            a0 = A0[f]; L_m, yth, sU = Lm_of(z), yth_of(z, f), SIGU[(f, z)]
            prof = {}
            for lab, lms, fbar, vk, esc, web2h, hx2 in (("central", 11.4, 0.157, "575", "spread", True, False),
                                                       ("low baryons", 11.4, 0.10, "575", "spread", True, False),
                                                       ("very low baryons", 11.4, 0.06, "575", "spread", True, False),
                                                       ("fast kick", 11.4, 0.157, "650", "spread", True, False),
                                                       ("escaped removed", 11.4, 0.157, "575", "removed", True, False),
                                                       ("M* 11.2", 11.2, 0.157, "575", "spread", True, False), ("M* 11.6", 11.6, 0.157, "575", "spread", True, False),
                                                       ("no web phantom in 2-halo", 11.4, 0.157, "575", "spread", False, False),
                                                       ("hosts x2 (M_cut +0.3 dex)", 11.4, 0.157, "575", "spread", True, True)):
                w_, bg_ = (w2_, bgal2) if hx2 else (w0_, bgal)
                dl_l, dl_c = np.zeros(len(Rc)), np.zeros(len(Rc))
                parts = {k_: np.zeros(len(Rc)) for k_ in ("baryons", "phantom", "carrier retained", "carrier escaped", "2-halo", "LCDM 1-halo", "LCDM 2-halo")}
                for Mh, wt in zip(Mg, w_):
                    if wt < 1e-5:
                        continue
                    r200 = (3 * Mh * MS6 / (4 * math.pi * 200 * rho_cz)) ** (1 / 3); c_ = 5.71 * (Mh * h_ / 2e12) ** (-0.084) * (1 + z) ** (-0.47)
                    r2 = rx * MPCm; x2h = r2 > r200
                    m2l = np.concatenate([[0.0], np.cumsum(0.5 * ((4 * math.pi * r2 ** 2 * rho_m * bg_ * xi_l * x2h)[1:] + (4 * math.pi * r2 ** 2 * rho_m * bg_ * xi_l * x2h)[:-1]) * np.diff(r2))])
                    m2c = np.concatenate([[0.0], np.cumsum(0.5 * ((4 * math.pi * r2 ** 2 * rho_m * bg_ * xi_c * x2h)[1:] + (4 * math.pi * r2 ** 2 * rho_m * bg_ * xi_c * x2h)[:-1]) * np.diff(r2))])
                    M2l = np.interp(RRc, r2, m2l, left=0.0); M2c = np.interp(RRc, r2, m2c if web2h else m2l, left=0.0)
                    Ml = nfw_M(RRc, Mh * MS6, c_, r200) + M2l
                    # the chain: stars (Hernquist, a = 5 kpc) + gas (beta = 2/3, r_c = 0.07 r200, to r200) + phantom + carrier
                    Ms = 10 ** lms * MS6; aH = 0.005 * MPCm
                    Mstar = lambda r: Ms * r ** 2 / (r + aH) ** 2
                    rcg = 0.07 * r200; Mgas_tot = max(fbar * Mh * MS6 - Ms, 0.0)
                    gshape = lambda r: (np.minimum(r, r200) / rcg - np.arctan(np.minimum(r, r200) / rcg)) / (r200 / rcg - math.atan(r200 / rcg))
                    Mbar = lambda r: Mstar(r) + Mgas_tot * gshape(r)
                    Mph = ph_ext(Mbar(RG), a0, L_m, yth, sU)
                    X = X_ret(Mh, vk); Mcar = (1 - FB) * Mh * MS6
                    Mret = X * nfw_M(RRc, Mcar, c_, r200)
                    Mesc = (1 - X) * Mcar * (np.minimum(RRc / (5.0 * MPCm), 1.0) ** 3 if esc == "spread" else 0.0 * RRc)
                    Mphc = np.interp(RRc, RG, Mph, right=Mph[-1])
                    Mc = Mbar(RRc) + Mphc + Mret + Mesc + M2c
                    dl_l += wt * dsig(Ml); dl_c += wt * dsig(Mc)
                    if lab == "central":
                        for k_, mm in (("baryons", Mbar(RRc)), ("phantom", Mphc), ("carrier retained", Mret), ("carrier escaped", Mesc), ("2-halo", M2c),
                                       ("LCDM 1-halo", nfw_M(RRc, Mh * MS6, c_, r200)), ("LCDM 2-halo", M2l)):
                            parts[k_] += wt * dsig(mm)
                norm = sum(wt for wt in w_ if wt >= 1e-5)
                prof[lab] = dict(lcdm=dl_l / norm, chain=dl_c / norm, ratio=dl_c / dl_l)
                if lab == "central":
                    prof[lab]["parts"] = {k_: v / norm for k_, v in parts.items()}
            out_z[f] = prof
        cm[z] = dict(bias=bgal, bias_x2=bgal2, prof=out_z, R2h=dict(k=[0.1, 0.3, 1.0, 3.0], ratio=R2h))
        P(f"    z {z}: CMASS-central bias {bgal:.2f} (hosts x2: {bgal2:.2f}; CMASS's measured b ~ 2); the chain's 2-halo lensing/matter per mode dL_chain/dm_LCDM at k = 0.1/0.3/1/3 h/Mpc: "
          + "; ".join(f"{f[:3]} " + ", ".join(f"{v:.3f}" for v in R2h[f]) for f in FOOTS) + f"   {el()}")
        for f in FOOTS:
            pr = out_z[f]
            P(f"      {f[:3]}: LCDM Delta Sigma at 0.1/0.3/1/3/10/30 Mpc: " + ", ".join(f"{np.interp(x, Rc, pr['central']['lcdm']):.2f}" for x in (0.1, 0.3, 1, 3, 10, 30))
              + " Msun/pc^2; chain/LCDM: " + " | ".join(f"{lab} " + " ".join(f"{np.interp(x, Rc, v['ratio']):.2f}" for x in (0.1, 0.3, 1, 3, 10, 30)) for lab, v in pr.items()))
            P("        the central case's parts (Msun/pc^2 at 0.1/0.3/1/3/10 Mpc): " + "; ".join(
                f"{k_} " + " ".join(f"{np.interp(x, Rc, v):.2f}" for x in (0.1, 0.3, 1, 3, 10)) for k_, v in pr["central"]["parts"].items()))
    OUT["numbers"]["C"] = {str(z): dict(bias=v["bias"], bias_x2=v["bias_x2"], R2h=v["R2h"], prof={f: {lab: dict(R=Rc, lcdm=pp["lcdm"], chain=pp["chain"], ratio=pp["ratio"], parts=pp.get("parts"))
                                                                                  for lab, pp in pr.items()} for f, pr in v["prof"].items()})
                           for z, v in cm.items()}
    # the jump across the switch
    jump = {f: {lab: cm[0.65]["prof"][f][lab]["ratio"] / cm[0.5]["prof"][f][lab]["ratio"] for lab in cm[0.5]["prof"][f]} for f in FOOTS}
    jump7 = {f: {lab: cm[0.7]["prof"][f][lab]["ratio"] / cm[0.5]["prof"][f][lab]["ratio"] for lab in cm[0.5]["prof"][f]} for f in FOOTS}
    jumpsw = {f: {lab: cm[0.65]["prof"][f][lab]["ratio"] / cm[0.6]["prof"][f][lab]["ratio"] for lab in cm[0.6]["prof"][f]} for f in FOOTS}
    OUT["numbers"]["C_jump"] = {f: {lab: dict(R=Rc, j065=v, j07=jump7[f][lab], j065_over_06=jumpsw[f][lab]) for lab, v in d_.items()} for f, d_ in jump.items()}
    P("    across the switch alone (ratio(0.65)/ratio(0.6), central, canonical) at 0.1/0.3/1/3/10 Mpc: "
      + " ".join(f"{np.interp(x, Rc, jumpsw['canonical']['central']):.3f}" for x in (0.1, 0.3, 1.0, 3.0, 10.0))
      + "; smooth part (ratio(0.6)/ratio(0.5)): " + " ".join(f"{np.interp(x, Rc, cm[0.6]['prof']['canonical']['central']['ratio'] / cm[0.5]['prof']['canonical']['central']['ratio']):.3f}"
                                                           for x in (0.1, 0.3, 1.0, 3.0, 10.0)))
    XR5 = (0.1, 0.3, 1.0, 3.0, 10.0)
    rng_ = {z: [float(np.min([np.interp(x, Rc, pp["ratio"]) for f in FOOTS for pp in cm[z]["prof"][f].values()])) for x in XR5] for z in cm}
    rng2 = {z: [float(np.max([np.interp(x, Rc, pp["ratio"]) for f in FOOTS for pp in cm[z]["prof"][f].values()])) for x in XR5] for z in cm}
    jr = [float(np.min([np.interp(x, Rc, v) for f in FOOTS for v in jump[f].values()])) for x in XR5]
    jR = [float(np.max([np.interp(x, Rc, v) for f in FOOTS for v in jump[f].values()])) for x in XR5]
    P("    chain/LCDM ranges over the brackets (0.1 / 0.3 / 1 / 3 / 10 Mpc): " + "; ".join(f"z {z}: " + ", ".join(f"{lo:.2f}-{hi:.2f}" for lo, hi in zip(rng_[z], rng2[z])) for z in cm)
      + "; ratio(0.65)/ratio(0.5): " + ", ".join(f"{lo:.3f}-{hi:.3f}" for lo, hi in zip(jr, jR)))
    OUT["numbers"]["C_summary"] = dict(ratio_min=rng_, ratio_max=rng2, jump_min=jr, jump_max=jR)
    obs = (1 / 1.4, 1 / 1.2)                                                    # Leauthaud+17: prediction 20-40% larger than observed
    check("C1 (reported) THE CMASS PREDICTION: chain/LCDM(R) at z = 0.5 and 0.65 (same hosts, same clustering), over the brackets",
          "; ".join(f"z {z}: " + ", ".join(f"{x} Mpc {lo:.2f}-{hi:.2f}" for x, lo, hi in zip(XR5, rng_[z], rng2[z])) for z in (0.5, 0.65)),
          True, load_bearing=False)
    swc = [float(np.interp(x, Rc, jumpsw["canonical"]["central"])) for x in XR5]
    smc = [float(np.interp(x, Rc, cm[0.6]["prof"]["canonical"]["central"]["ratio"] / cm[0.5]["prof"]["canonical"]["central"]["ratio"])) for x in XR5]
    OUT["numbers"]["C_switch"] = dict(R=XR5, across_switch_065_over_06=swc, smooth_06_over_05=smc)
    check("C2 (reported) THE SWITCH IN MASSIVE-GALAXY LENSING: ratio(0.65)/ratio(0.5) over the brackets, split into the part across the switch "
          "(0.65/0.6) and the smooth part below it (0.6/0.5, L = L_Lambda Omega_L(z) shrinking) -- central case, canonical",
          ", ".join(f"{x} Mpc {lo:.3f}-{hi:.3f}" for x, lo, hi in zip(XR5, jr, jR)) + "; across the switch " + " ".join(f"{v:.3f}" for v in swc)
          + "; smooth " + " ".join(f"{v:.3f}" for v in smc), True, load_bearing=False)
    inside = {z: [lo <= obs[1] and hi >= obs[0] for lo, hi in zip(rng_[z], rng2[z])] for z in (0.5, 0.65)}
    check("C3 (reported) AGAINST 'LENSING IS LOW' (quoted: observed/LCDM-predicted = 0.71-0.83 from Leauthaud+17's 20-40%; A = 0.79 from "
          "Amon+23 at Planck cosmology): does the chain's bracket reach the observed deficit at 0.1 / 1 / 10 Mpc?",
          "; ".join(f"z {z}: " + ", ".join(f"{x} Mpc {'yes' if ok else 'no'}" for x, ok in zip(XR5, inside[z])) for z in inside), True,
          load_bearing=False)

# ================================================================================================= W: the ledger
banner("W  THE LEDGER")
D2 = OUT["numbers"].get("D2", {}); W1n = OUT["numbers"].get("W1", {}); Zn = OUT["numbers"].get("Z", {}); Cs = OUT["numbers"].get("C_summary", {})


def _g(d, k, sub, fmt="{:+.1f}"):
    try:
        return fmt.format(d[k][sub])
    except Exception:
        return "n/a"


LEDGER = [
    ("F23a", "DERIVED", "the band-pass localises the web's field: " + (", ".join(f"{k}: {v['f_in'] + 0.5 * v['f_cov']:.2f}" for k, v in W1n.items()) if W1n else "n/a")
     + " of its variance is sourced within B21's 3 Mpc isolation radius", "W1 (reading (b), H_K1, the engine's growth, CLASS)"),
    ("F23b", "DERIVED", "in linear theory B21-like isolation leaves the external band-passed field at lens peaks within 20% of its value at all lens "
     "peaks (0.7-1.3 sigma_U by bin mass); a low-density selection leaves it unchanged (a dipole is independent of a monopole)",
     "W2 (Gaussian-field Monte Carlo; conditioning stated; Moster+13 SHMR for the Lagrangian scales)"),
    ("F23c", "FAILS" if not MUTATE else "OPEN", "KiDS (B21, lead grade, exact projector) with the web's field in the AQUAL kernel, reading (b), H_K1: "
     + ", ".join(f"{k}: {_g(D2, k, 'conditioned (most favourable isolation, AQUAL)')}" for k in D2) + " (gate +9); the committed passes need the field omitted",
     "D2 (web field in the kernel; MUTATE switches it off)"),
    ("F23d", "CONSTRAINT", "to pass, the field at isolated KiDS lenses must be below sigma* = " + (", ".join(f"{k}: {v['sigma_star']:.1e}" for k, v in OUT["numbers"].get("D1", {}).items()) or "n/a")
     + " a0, i.e. the linear conditioned field shrunk several-fold -- only the exterior-only bound (every source inside 3 Mpc silenced) does it",
     "D1, D3"),
    ("F23e", "CONSTRAINT", "H_K1's z = 0.7 KiDS prediction in reading (b), exact projector: isolated " + ", ".join(f"{f}: {_g(Zn, f, 'iso')}" for f in Zn)
     + "; with the web's field " + ", ".join(f"{f}: {_g(Zn, f, 'web')}" for f in Zn), "Z1 (a prediction; FP19's +496 was all-matter + the old projector)"),
    ("F23f", "DERIVED", "CMASS-like lenses: chain/LCDM at 0.1/0.3/1/3/10 Mpc (bracket ranges): " + ("; ".join(
        f"z = {z}: " + ", ".join(f"{lo:.2f}-{hi:.2f}" for lo, hi in zip(Cs["ratio_min"][z], Cs["ratio_max"][z])) for z in (0.5, 0.65, 0.7)) if Cs else "n/a")
     + ("; jump 0.65/0.5: " + ", ".join(f"{lo:.3f}-{hi:.3f}" for lo, hi in zip(Cs["jump_min"], Cs["jump_max"])) if Cs else ""),
     "C1/C2 (inputs: White+11 HOD, Sheth-Tormen, Duffy+08 c(M), beta-model gas, FP16's retention; QUMOND form for the extended source)"),
    ("F23g", "FAILS", "against the published CMASS lensing (quoted, not re-measured: Leauthaud+17's clustering-predicted signal 20-40% above the "
     "observed; Amon+23's A = 0.79 at Planck): the chain predicts " + (f"{min(Cs['ratio_min'][z][2] for z in (0.5, 0.65)):.2f}-"
                                                                      f"{max(Cs['ratio_max'][z][2] for z in (0.5, 0.65)):.2f}" if Cs else "n/a")
     + "x LCDM at R = 1 Mpc (the lens's own band-passed phantom, "
     "isothermal out to ~L, plus the web phantom's 2-halo term) where the data sit at 0.71-0.83x -- the wrong sign, " + (
         f"{min(Cs['ratio_min'][z][2] for z in (0.5, 0.65)) / 0.83:.1f}-{max(Cs['ratio_max'][z][2] for z in (0.5, 0.65)) / 0.71:.1f}x the observed; " if Cs else "")
     + "the deficit is not reproduced (a bump at ~1 Mpc and a trough at ~3 Mpc instead)", "C1, C3 (every bracket; the linear web phantom removed as well)"),
    ("F23i", "OPEN", "the direct test of H_K1's z-structure: no step at 0.635 for CMASS-like hosts (the yield's cut radius lies beyond L); a smooth "
     "~30% fall of Delta Sigma at 2-5 Mpc from z = 0.5 to 0.6 (L(z)) and ~10% more across the switch; needs CMASS lensing split by z: BOSS DR12 "
     "galaxy_DR12v5_CMASS_North x the on-disk KiDS-1000 shear catalogue", "C2 (fetching the BOSS catalogue needs the user's go)"),
    ("F23h", "POSTULATED", "the isolation conditioning's Lagrangian-peak proxy (Moster+13 SHMR, delta_c = 1.686 on top-hat scales, 3 Mpc proper)",
     "W2 variants bracket it; the verdict does not move across them"),
]
for k_, s_, w_, b_ in LEDGER:
    P(f"    {k_:6s} {s_:11s} {w_}  --  {b_}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, s_, w_, b_ in LEDGER]
check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)

# ================================================================================================= verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P("  KiDS with the web's field (reading (b), H_K1): see D2; the conditioning (W2) is the decisive derived step; CMASS across the switch: see C;"
  "\n  not 'closed'.  Time " + f"{time.time() - T0:.0f} s.")
_name = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(jclean(OUT), open(os.path.join(HERE, _name), "w"), indent=1)
P(f"\n  {len(CH) - n_fail}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {_name}")
sys.exit(0 if n_fail == 0 else 1)
