#!/usr/bin/env python3
r"""
L38 -- what Type Ia supernovae actually say about this framework, end to end and adversarially
==============================================================================================
The framework's ONE distinctive surviving prediction is that the acceleration scale tracks the
dark-energy density,  a0 = kappa c sqrt(G rho),  and therefore evolves exactly as rho does:

    CANONICAL footing (rho = rho_Lambda):
        a0(z)/a0(0) = (1+z)^{(3/2)(1+w0+wa)} * exp[ -(3/2) wa z/(1+z) ]        [ CPL, exact ]
    ALT footing (rho = rho_total):
        a0(z)/a0(0) = E(z) = sqrt( Om (1+z)^3 + (1-Om) rho_DE(z)/rho_DE(0) )

Supernovae are the instrument that measures (w0, wa).  So SNe feed DIRECTLY into the framework's
own distinctive prediction, and that pipeline has never been run SN-only, end to end, with the
official covariance.  This lane runs it.

WHAT IS DELIBERATELY NOT HERE.  The SN host-mass-step lever is CLOSED.  It was tested twice --
globally (real_research/snia_hoststep_sizextmatch.py) and with reconstructed local surface density
at the SN site (real_research/snia_hoststep_localSB.py) -- and both returned null: the partial
correlation of Hubble residual with acceleration at fixed mass is +0.030 / -0.036 while mass
survives at -0.170 / -0.203.  The step is an age/metallicity effect and the a0 step-LOCATION
coincidence stays a coincidence.  Nothing below re-opens it.

DOCUMENTED FAILURE MODE THIS LANE MUST NOT REPEAT.  real_research/GEMINI_MANUFACTURED_WIN_a0z_
2026-07-20.md records an agent truncating the law at O(z), dropping the wa term, and extrapolating
a spurious monotone RISE to z ~ 1 to "confirm" a high-z measurement.  The exact closed form is used
everywhere below, and A5 reproduces the truncation as an explicit FAILURE so the guard is testable.

THE SECTIONS
  A  CONTROLS -- the machinery, before any claim rests on it.
  B  TARGET 1 -- the registered z ~ 2.5 Tully-Fisher prediction ("FLAT 0.00 dex vs LCDM +0.33 dex,
     one point at +/-0.13 dex, 20:1").  The zero point scales as a0^{1/4}; on the canonical footing
     with DESI's evolving dark energy a0(2.5)/a0(0) < 1.  Does "0.00" survive?
  C  TARGET 2 -- the SN-ONLY pipeline: fit (Om, w0, wa) from Pantheon+ with the official STAT+SYS
     covariance, propagate through the exact law, and produce a0(z) with a real band over 0 < z < 3.
  D  TARGET 3 -- the internal footing fork (rho_Lambda vs rho_total) across the supernova redshift
     range, and whether the SN-era a0 measurements already in the repo (MUSE-DARK III, MSA-3D) can
     separate the two branches.  (Recombination and BBN belong to lane L37 and are not touched.)
  E  TARGET 4 -- the unexplored angle: the gravitational-lensing magnification signal in SN Hubble
     residuals as a probe of a baryons-plus-kernel mass distribution.  Power calculation.
  F  BONUS -- the low-redshift Hubble-diagram scatter as a direct bound on the framework's
     peculiar-velocity field, which is a live framework question (hunt_2026/h85_bulk_flow_null.py).
  G  VERDICT.

BOTH FOOTINGS EVERYWHERE.  a0(0) = 9.3619e-11 (canonical, rho_Lambda) / 1.1279e-10 m s^-2 (alt,
rho_total).  The RATIO a0(z)/a0(0) is footing-independent WITHIN a branch; the two BRANCHES are
different functions of z, which is exactly what section D measures.

NEVER: "the data favour this framework over LCDM".  They do not, and the record forbids the claim.
"""
import os, sys, json, math
import numpy as np

# ------------------------------------------------------------------ the check harness (from L6)
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def P(s=""): print(s, flush=True)
def info(s): print("  " + s, flush=True)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rel(p): return p                                    # paths printed RELATIVE, never machine paths

np.random.seed(20260908)

# ------------------------------------------------------------------ constants and the two footings
C_LIGHT = 299792458.0
A0 = {"canonical (rho_Lambda)": 9.3619e-11, "alt (rho_total)": 1.1279e-10}
OM_FID, OL_FID = 0.315, 0.685

P("=" * 118)
P("L38 -- Type Ia supernovae re-examined for this framework: the a0(z) pipeline, SN-only, end to end")
P("=" * 118)
P("  a0(z)/a0(0) = (1+z)^{1.5(1+w0+wa)} exp[-1.5 wa z/(1+z)]   -- EXACT closed form, never truncated")
P(f"  footings: " + " / ".join(f"{k} = {v:.4e} m s^-2" for k, v in A0.items())
  + f"   (ratio {A0['alt (rho_total)']/A0['canonical (rho_Lambda)']:.4f} = 1/sqrt(Omega_Lambda))")
P("  host-mass-step lever: CLOSED (two null tests on the record); not re-opened anywhere below")
P("")

# ------------------------------------------------------------------ the laws
def rho_de_ratio(z, w0, wa):
    z = np.asarray(z, float)
    with np.errstate(over="ignore", invalid="ignore"):
        return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))

def a0_ratio_canonical(z, w0, wa):
    """a0(z)/a0(0) on the rho_Lambda footing -- the framework's canonical law."""
    return np.sqrt(rho_de_ratio(z, w0, wa))

def a0_ratio_alt(z, w0, wa, om=OM_FID):
    """a0(z)/a0(0) on the rho_total footing -- a0 proportional to H(z)."""
    z = np.asarray(z, float)
    return np.sqrt(om * (1 + z) ** 3 + (1 - om) * rho_de_ratio(z, w0, wa))

# ==================================================================================================
# S1.  DATA -- Pantheon+ with the official STAT+SYS covariance (read-only; owned by another lane)
# ==================================================================================================
import gzip, glob as _glob
CAND_DAT = ["real_research/data_cache/PantheonPlusSH0ES.dat",
            "prep_2026/sne_lambda/pantheonplus_full.dat",
            "qwen_claude_field_theory/closure_2026/supernova_reaudit_2026/release.dat"]
CAND_COV = ["qwen_claude_field_theory/closure_2026/supernova_reaudit_2026/PantheonPlusSH0ES_STAT_SYS.cov",
            "qwen_claude_field_theory/closure_2026/supernova_reaudit_2026/PantheonPlusSH0ES_STAT_SYS.cov.gz",
            "real_research/data_cache/PantheonPlusSH0ES_STAT_SYS.cov"]
DAT = next((p for p in CAND_DAT if os.path.exists(os.path.join(REPO, p))), None)
COV = next((p for p in CAND_COV if os.path.exists(os.path.join(REPO, p))), None)
if DAT is None or COV is None:
    sys.exit("L38 needs the Pantheon+ release table and its official STAT+SYS covariance; neither was found "
             "at any of the known in-repo paths.")

P("=" * 118); P("S1 -- data"); P("=" * 118)
TAB = np.genfromtxt(os.path.join(REPO, DAT), names=True, dtype=None, encoding=None)
info(f"Pantheon+ release table: {len(TAB)} light curves ({DAT})")
_same = [p for p in CAND_DAT if os.path.exists(os.path.join(REPO, p)) and
         open(os.path.join(REPO, p), "rb").read() == open(os.path.join(REPO, DAT), "rb").read()]
info(f"  byte-identical copies in the repo: {len(_same)} ({', '.join(_same)})")
_op = gzip.open if COV.endswith(".gz") else open
with _op(os.path.join(REPO, COV), "rt") as fh: raw = np.loadtxt(fh)
NCOV = int(raw[0]); COVM = raw[1:].reshape(NCOV, NCOV)
ASYM = float(np.max(abs(COVM - COVM.T))); COVM = (COVM + COVM.T) / 2
info(f"official STAT+SYS covariance {NCOV}x{NCOV} ({COV}), max asymmetry {ASYM:.1e} "
     f"(release rounding), symmetrised")

MASK = TAB["zHD"] > 0.01                                            # the official cosmology cut
Z = TAB["zHD"][MASK]; ZHEL = TAB["zHEL"][MASK]; MB = TAB["m_b_corr"][MASK]
CC = COVM[np.ix_(MASK, MASK)]
NSN = int(MASK.sum())
info(f"cosmology cut zHD > 0.01 -> N = {NSN}, z in [{Z.min():.4f}, {Z.max():.4f}]")
CINV = np.linalg.inv(CC); CINV = (CINV + CINV.T) / 2
ONE = np.ones(NSN); IO = CINV @ ONE; NORM = float(ONE @ IO)
assert np.all(np.isfinite(CINV))
info(f"C^-1 finite, condition number {np.linalg.cond(CC):.3e}; magnitude offset marginalised analytically")
P("")

# ---- the distance model (fast cumulative-trapezoid integrator; validated against 48-node GL in A1)
ZG = np.linspace(0.0, Z.max() * 1.0001, 4001); DZG = ZG[1] - ZG[0]
def mu_shape(om, w0, wa):
    """5 log10[(1+zHEL) * comoving distance in c/H0 units] -- H0 and M absorbed in the free offset."""
    with np.errstate(all="ignore"):
        e2 = om * (1 + ZG) ** 3 + (1 - om) * rho_de_ratio(ZG, w0, wa)
        if not np.all(np.isfinite(e2)) or np.min(e2) <= 0: return None
        inv = 1.0 / np.sqrt(e2)
        cum = np.concatenate([[0.0], np.cumsum((inv[1:] + inv[:-1]) / 2 * DZG)])
        dc = np.interp(Z, ZG, cum)
        if np.min(dc) <= 0: return None
        out = 5 * np.log10((1 + ZHEL) * dc)
    return out if np.all(np.isfinite(out)) else None

def chi2(om, w0, wa):
    p = mu_shape(om, w0, wa)
    if p is None: return 1e100
    r = MB - p; r = r - (IO @ r) / NORM
    return float(r @ (CINV @ r))

def chi2_batch(Pm):
    """Pm: (K,3) array of (om,w0,wa).  Batched -- one BLAS gemm for the whole block."""
    om = Pm[:, 0:1]; w0 = Pm[:, 1:2]; wa = Pm[:, 2:3]; zz = ZG[None, :]
    with np.errstate(all="ignore"):
        rho = (1 + zz) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * zz / (1 + zz))
        e2 = om * (1 + zz) ** 3 + (1 - om) * rho
        bad = (~np.isfinite(e2)) | (e2 <= 0)
        e2 = np.where(bad, 1.0, e2)
        cum = np.cumsum(np.concatenate([np.zeros((len(Pm), 1)),
                                        (1/np.sqrt(e2[:, 1:]) + 1/np.sqrt(e2[:, :-1])) / 2 * DZG], axis=1), axis=1)
    badrow = bad.any(axis=1)
    D = np.empty((len(Pm), NSN))
    for i in range(len(Pm)): D[i] = np.interp(Z, ZG, cum[i])
    with np.errstate(all="ignore"):
        M = 5 * np.log10((1 + ZHEL)[None, :] * D)
    badrow |= ~np.isfinite(M).all(axis=1)
    R = np.where(np.isfinite(M), MB[None, :] - M, 0.0)
    CR = CINV @ R.T
    R = R - ((ONE @ CR) / NORM)[:, None]
    out = np.einsum("kn,nk->k", R, CINV @ R.T)
    out[badrow] = 1e100
    return out

# ==================================================================================================
# A.  CONTROLS
# ==================================================================================================
P("=" * 118); P("A -- CONTROLS (nothing below is trusted unless these pass)"); P("=" * 118)

# ---- A1: independent-implementation control against 48-node Gauss-Legendre
from numpy.polynomial.legendre import leggauss
_nd, _wt = leggauss(48); _zz = Z[:, None] * (_nd + 1) / 2
def mu_gl(om, w0, wa):
    e2 = om * (1 + _zz) ** 3 + (1 - om) * rho_de_ratio(_zz, w0, wa)
    return 5 * np.log10((1 + ZHEL) * (Z / 2 * np.sum(_wt / np.sqrt(e2), axis=1)))
d1 = float(np.max(abs(mu_shape(0.33, -1.0, 0.0) - mu_gl(0.33, -1.0, 0.0))))
d2 = float(np.max(abs(mu_shape(0.30, -0.752, -0.86) - mu_gl(0.30, -0.752, -0.86))))
check("A1 the fast distance integrator matches an independent 48-node Gauss-Legendre quadrature "
      "(the convention used by the repo's own full-covariance audit) to better than 1e-4 mag on both a "
      "LCDM and a DESI-CPL cosmology",
      max(d1, d2) < 1e-4, f"max |dmu| = {d1:.2e} (LCDM), {d2:.2e} (CPL)")

# ---- A2: reproduce the published Pantheon+ SN-only constraint
from scipy.optimize import minimize_scalar, brentq, minimize
_f = minimize_scalar(lambda v: chi2(v, -1.0, 0.0), bounds=(0.05, 0.80), method="bounded",
                     options={"xatol": 1e-9})
OM_LCDM = float(_f.x); CHI2_LCDM = float(_f.fun)
_lo = brentq(lambda v: chi2(v, -1.0, 0.0) - CHI2_LCDM - 1, 0.05, OM_LCDM)
_hi = brentq(lambda v: chi2(v, -1.0, 0.0) - CHI2_LCDM - 1, OM_LCDM, 0.80)
SIG_OM = (_hi - _lo) / 2
OM_PUB, SIG_PUB = 0.334, 0.018                       # Brout et al. 2022 ApJ 938,110, Pantheon+ SN-only
pull = abs(OM_LCDM - OM_PUB) / math.hypot(SIG_OM, SIG_PUB)
info(f"flat LCDM, SN only: Omega_m = {OM_LCDM:.4f} +/- {SIG_OM:.4f} (chi2 = {CHI2_LCDM:.3f} / {NSN} SNe)")
info(f"published            Omega_m = {OM_PUB:.3f} +/- {SIG_PUB:.3f}  (Brout+2022, Pantheon+ SN-only)")
check("A2 the fitter reproduces the published Pantheon+ SN-only flat-LCDM constraint to well inside its "
      "quoted error",
      pull < 1.0 and abs(SIG_OM - SIG_PUB) < 0.006, f"pull {pull:.2f} sigma, sigma {SIG_OM:.4f} vs {SIG_PUB:.3f}")

# ---- A3: injection-recovery COVERAGE on synthetic data drawn from the real covariance.
#       Note the correct test here is COVERAGE, not point recovery: SN-only (w0,wa) is a long degenerate
#       ridge (that is section C's whole finding), so a "conditional" error bar with the other parameters
#       held fixed is meaningless.  We ask instead: does the profile-likelihood region contain the truth
#       at the advertised rate?
LCH = np.linalg.cholesky(CC)
TRUE = (0.30, -0.85, -0.60)
_gO = np.linspace(0.05, 0.60, 12); _gW = np.linspace(-2.2, 0.0, 20); _gA = np.linspace(-5.0, 3.0, 25)
_GO, _GW, _GA = np.meshgrid(_gO, _gW, _gA, indexing="ij")
_SEED = np.stack([_GO.ravel(), _GW.ravel(), _GA.ravel()], axis=1)
NREAL = 12
_cov68 = _cov95 = 0; _rec = []
_mb0 = MB.copy()
for k in range(NREAL):
    globals()["MB"] = mu_shape(*TRUE) + 19.30 + LCH @ np.random.normal(size=NSN)
    _c = chi2_batch(_SEED)
    _p0 = _SEED[np.argmin(_c)]
    best = min(float(minimize(lambda p: chi2(*p), s, method="Nelder-Mead",
                              options={"xatol": 1e-6, "fatol": 1e-6, "maxiter": 4000, "maxfev": 4000}).fun)
               for s in (_p0, np.array(TRUE), np.array([0.33, -1.0, 0.0])))
    r = minimize(lambda p: chi2(*p), _p0, method="Nelder-Mead",
                 options={"xatol": 1e-6, "fatol": 1e-6, "maxiter": 4000, "maxfev": 4000})
    ctrue = float(minimize_scalar(lambda v: chi2(v, TRUE[1], TRUE[2]), bounds=(0.02, 0.80),
                                  method="bounded").fun)
    d = ctrue - best
    _cov68 += (d <= 2.30); _cov95 += (d <= 5.99)
    _rec.append((r.x[1], r.x[2], d))
globals()["MB"] = _mb0
_rec = np.array(_rec)
info(f"injection (w0,wa) = ({TRUE[1]}, {TRUE[2]});  {NREAL} synthetic realisations drawn from the real "
     f"STAT+SYS covariance")
info(f"  recovered w0 median {np.median(_rec[:,0]):+.3f} (spread {np.std(_rec[:,0]):.3f}); "
     f"wa median {np.median(_rec[:,1]):+.3f} (spread {np.std(_rec[:,1]):.3f}) -- SN-only, so very wide")
info(f"  COVERAGE of the truth: {_cov68}/{NREAL} inside the 68% region (dchi2 <= 2.30), "
     f"{_cov95}/{NREAL} inside 95% (dchi2 <= 5.99); median dchi2 at the truth = {np.median(_rec[:,2]):.2f}")
check("A3 the cosmology fitter recovers injected (w0, wa) from synthetic supernova data generated with the "
      "real STAT+SYS covariance -- the profile-likelihood region covers the truth at the advertised rate",
      _cov95 >= NREAL - 2 and _cov68 >= NREAL // 2,
      f"68% coverage {_cov68}/{NREAL}, 95% coverage {_cov95}/{NREAL}")

# ---- A4: the exact law reproduces its own recorded behaviour
zb = np.linspace(0, 1, 200001); rb = a0_ratio_canonical(zb, -0.83, -0.75)
z_bump = float(zb[np.argmax(rb)]); bump = float(rb.max()); r3 = float(a0_ratio_canonical(3.0, -0.83, -0.75))
info(f"repo-canonical DESI-DR2-ish (w0,wa) = (-0.83,-0.75): bump peak z = {z_bump:.3f} at "
     f"{bump:.4f} (+{100*(bump-1):.1f}%), a0(3)/a0(0) = {r3:.4f}")
check("A4 the exact a0(z) law reproduces its own recorded behaviour -- a bump near z ~ 0.29 and 0.70 at "
      "z = 3 for the repo's DESI-DR2 parameters",
      abs(z_bump - 0.29) < 0.02 and abs(r3 - 0.70) < 0.01, f"z_bump {z_bump:.3f}, ratio(3) {r3:.4f}")

# ---- A5: the low-z expansion, and the documented failure mode reproduced AS a failure
def expand2(z, w0, wa):
    lin = 1.5 * (1 + w0); quad = 0.75 * (wa - (1 + w0)) + (9 / 8) * (1 + w0) ** 2
    return 1 + lin * z + quad * np.asarray(z, float) ** 2
def gemini_truncated(z, w0):  return 1 + 1.5 * (1 + w0) * np.asarray(z, float)
w0t, wat = -0.83, -0.75
zs = np.array([0.02, 0.05, 0.10])
err2 = np.max(abs(expand2(zs, w0t, wat) / a0_ratio_canonical(zs, w0t, wat) - 1) / zs ** 3)
zbad = np.array([0.5, 1.0, 1.5])
errG = np.max(abs(gemini_truncated(zbad, w0t) - a0_ratio_canonical(zbad, w0t, wat)))
info(f"O(z^2) expansion:  residual / z^3 bounded by {err2:.3f} over z <= 0.1 -> the claimed order holds")
info(f"the DOCUMENTED failure mode (linear, wa dropped) is off by up to {errG:.2f} in the ratio at "
     f"z = 0.5-1.5 -- i.e. it turns a decline into a +45% rise")
check("A5 the low-redshift expansion matches the exact law to the order claimed (O(z^2)), AND the "
      "documented manufactured-win truncation (linear, wa dropped) is reproduced as a large ERROR rather "
      "than being silently adopted",
      err2 < 5.0 and errG > 0.3, f"O(z^3) coefficient bound {err2:.2f}; truncation error {errG:.2f}")

# ---- A6: reproduce PAPER7's own number and identify which (w0,wa) fork produced it
DESI_DR2 = {   # arXiv:2503.14738 marginals, as frozen in prep_2026/a0z_crossscale/a0z_prediction_band_2026.py
    "DESI DR2 + CMB + Pantheon+": (-0.838, 0.055, -0.62, 0.22, -0.86),
    "DESI DR2 + CMB + DESY5":     (-0.752, 0.057, -0.86, 0.22, -0.86),
    "DESI DR2 + CMB + Union3":    (-0.667, 0.088, -1.09, 0.31, -0.87),
}
r25 = {k: float(a0_ratio_canonical(2.5, v[0], v[2])) for k, v in DESI_DR2.items()}
best_fork = min(r25, key=lambda k: abs(r25[k] - 0.82))
info("a0(2.5)/a0(0) by DESI DR2 combination: " + ", ".join(f"{k.split('+')[-1].strip()} {v:.4f}"
                                                           for k, v in r25.items()))
check("A6 PAPER7's stated a0(2.5)/a0(0) = 0.82 is reproduced exactly, and the (w0,wa) fork behind it is "
      "identified as DESI DR2 + CMB + Pantheon+",
      abs(r25[best_fork] - 0.82) < 0.005 and "Pantheon+" in best_fork,
      f"{best_fork} -> {r25[best_fork]:.4f}")
P("")

# ==================================================================================================
# B.  TARGET 1 -- the registered z ~ 2.5 Tully-Fisher prediction
# ==================================================================================================
P("=" * 118)
P("B -- TARGET 1: does the REGISTERED 'flat 0.00 dex at z ~ 2.5' survive evolving dark energy?")
P("=" * 118)
P("  the registered statistic (PAPER7, DOI 10.5281/zenodo.22563139; STANDING.md; README):")
P("    Delta_BTFR frozen against 0.00 dex (framework) and +0.33 dex (LCDM-native), one clean point at")
P("    +/-0.13 dex, quoted as 20:1 discrimination.")
P("")
P("  B1 -- SIGN CONVENTION.  In deep MOND V_f^4 = G a0 M_b exactly, so a change in a0 moves the zero")
P("        point.  Two conventions are in circulation and PAPER7 uses BOTH, in the same paragraph:")
sep_disp = None
Rn = 2.13                       # LCDM-native rise at z=2.5, Dutton-Maccio 2014 c(M,z), M = 1e12 Msun
w0p, s0p, wap, sap, rhop = DESI_DR2["DESI DR2 + CMB + Pantheon+"]
r_fw = float(a0_ratio_canonical(2.5, w0p, wap))
info(f"mass-side   Delta = log10 M_b - 4 log10 V_f - C0 = -log10[scale(z)/scale(0)]"
     f"  ->  framework {-math.log10(r_fw):+.3f},  LCDM-native {-math.log10(Rn):+.3f}")
info(f"vel.-side   Delta = 4 log10 V_f - log10 M_b - C0' = +log10[scale(z)/scale(0)]"
     f"  ->  framework {math.log10(r_fw):+.3f},  LCDM-native {math.log10(Rn):+.3f}")
info( "PAPER7's PROSE defines the mass-side form; its DISPLAYED numbers (0.00 / -0.09 / +0.33) are the")
info( "velocity-side one.  The SEPARATION is identical either way, so the 20:1 is unaffected, but an")
info( "observer who applies the prose formula and compares to '+0.33' would score the LCDM hypothesis")
info( "with the wrong sign.  This is a documentation hazard in a frozen pre-registration, not a physics")
info( "error; it should be fixed by an append-only amendment, not by editing the frozen text.")
check("B1 the two Delta_BTFR sign conventions give the SAME separation between the two hypotheses (so "
      "the 20:1 is convention-independent), while the registered central values are quoted in the "
      "velocity-side convention and the registered FORMULA is the mass-side one",
      abs(abs(math.log10(Rn) - math.log10(r_fw)) - abs(-math.log10(Rn) + math.log10(r_fw))) < 1e-12,
      f"separation {abs(math.log10(Rn)-math.log10(r_fw)):.3f} dex both ways")
P("")
P("  B2 -- the framework's OWN z = 2.5 prediction with the full (w0, wa) covariance propagated.")
P("        (all values below in the velocity-side convention, to match the registered numbers)")
info(f"{'(w0, wa) source':38s}{'a0(2.5)/a0(0)':>15}{'Delta_fw [dex]':>16}{'sigma [dex]':>13}{'provenance':>12}")
NMC = 400000
FORKS = []
for name, (w0, s0, wa, sa, rho) in DESI_DR2.items():
    cov2 = np.array([[s0 ** 2, rho * s0 * sa], [rho * s0 * sa, sa ** 2]])
    L2 = np.linalg.cholesky(cov2)
    smp = np.array([w0, wa])[:, None] + L2 @ np.random.normal(size=(2, NMC))
    d = np.log10(a0_ratio_canonical(2.5, smp[0], smp[1]))
    FORKS.append((name, float(a0_ratio_canonical(2.5, w0, wa)), float(np.log10(a0_ratio_canonical(2.5, w0, wa))),
                  float(np.std(d)), float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))))
    info(f"{name:38s}{FORKS[-1][1]:>15.4f}{FORKS[-1][2]:>16.3f}{FORKS[-1][3]:>13.3f}{'DR2 paper':>12}")
EXTRA = [("LCDM exactly (w = -1)", -1.00, 0.00, "the kill limit"),
         ("repo canonical DR2-ish", -0.83, -0.75, "repo"),
         ("DESI BAO+CMB only (SN-free)", -0.43, -1.70, "SN-free"),
         ("age-corrected BAO+CMB+P+ (Son25)", -0.45, -1.59, "SN-syst fork"),
         ("age-corrected BAO+CMB+DES5Y (Son25)", -0.34, -1.90, "SN-syst fork")]
for name, w0, wa, tag in EXTRA:
    rr = float(a0_ratio_canonical(2.5, w0, wa))
    info(f"{name:38s}{rr:>15.4f}{math.log10(rr):>16.3f}{'--':>13}   {tag}")
    FORKS.append((name, rr, math.log10(rr), np.nan, np.nan, np.nan))
evolving = [f for f in FORKS if "LCDM exactly" not in f[0]]
d_lo, d_hi = min(f[2] for f in evolving), max(f[2] for f in evolving)
sig_typ = float(np.nanmedian([f[3] for f in FORKS[:3]]))
P("")
info(f"EVERY evolving-dark-energy fork on the record puts the framework's z = 2.5 zero point at")
info(f"  Delta_fw = {d_hi:+.3f} to {d_lo:+.3f} dex, with a within-fork 1-sigma of ~{sig_typ:.3f} dex.")
info(f"  The registered central value 0.00 is recovered ONLY in the w = -1 limit.")
info(f"  |Delta_fw| is {abs(d_hi)/0.13*100:.0f}-{abs(d_lo)/0.13*100:.0f}% of the registered total measurement")
info(f"  budget of 0.13 dex -- i.e. it is NOT negligible against the measurement it is registered against.")
check("B2 the registered 'flat 0.00 dex' central value is UNCHANGED once evolving dark energy is "
      "propagated through the exact law with the full (w0, wa) covariance",
      abs(d_hi) < 0.02 and abs(d_lo) < 0.02,
      f"instead Delta_fw = {d_hi:+.3f} to {d_lo:+.3f} dex +/- {sig_typ:.3f}; the registered 0.00 holds only if w = -1")
P("")
P("  B3 -- the CROSS-TERM nobody has propagated: the LCDM-native rival's own scale contains E(z),")
P("        so the SAME (w0, wa) that move the framework also move the rival.  a0z_lcdm_native_")
P("        hypothesis_2026.py hardcodes E(z) at w = -1.")
h = 0.674
fNFW = lambda x: np.log(1 + x) - x / (1 + x)
def c_DM14(M, z):
    a = 0.520 + (0.905 - 0.520) * np.exp(-0.617 * np.asarray(z, float) ** 1.21); b = -0.101 + 0.026 * np.asarray(z, float)
    return 10 ** (a + b * np.log10(M * h / 1e12))
def lcdm_native(z, w0, wa, M=1e12):
    c0 = c_DM14(M, 0.0); cz = c_DM14(M, z)
    Ez = np.sqrt(OM_FID * (1 + np.asarray(z, float)) ** 3 + (1 - OM_FID) * rho_de_ratio(z, w0, wa))
    E0 = 1.0
    return (Ez / E0) ** (4 / 3) * (cz ** 2 / fNFW(cz)) / (c0 ** 2 / fNFW(c0))
Rn_L = float(lcdm_native(2.5, -1.0, 0.0)); Rn_D = float(lcdm_native(2.5, w0p, wap))
info(f"LCDM-native rise at z = 2.5:  w = -1 -> {Rn_L:.3f} ({math.log10(Rn_L):+.3f} dex);  "
     f"DESI DR2+P+ background -> {Rn_D:.3f} ({math.log10(Rn_D):+.3f} dex)")
info(f"the cross-term moves the RIVAL by only {abs(math.log10(Rn_D)-math.log10(Rn_L)):.4f} dex -- negligible "
     f"against 0.13.  (The concentration-mass relation's own w-dependence via the growth history is NOT")
info( " included; it is a second-order effect on c(M,z) and is flagged, not computed, here.)")
check("B3 the evolving-dark-energy cross-term in the LCDM-native rival is negligible against the "
      "registered 0.13 dex budget, so the +0.33 side of the registered statistic does NOT need revising",
      abs(math.log10(Rn_D) - math.log10(Rn_L)) < 0.02,
      f"rival shifts {math.log10(Rn_D)-math.log10(Rn_L):+.4f} dex; reproduces the registered {math.log10(Rn_L):+.2f}")
P("")
P("  B4 -- what the correction does to the registered 20:1.")
def odds(sep, sig): return math.exp(sep ** 2 / (2 * sig ** 2))
o_reg = odds(math.log10(Rn_L) - 0.0, 0.13)
sep_new = math.log10(Rn_D) - d_hi
o_new = odds(sep_new, math.hypot(0.13, sig_typ))
info(f"as registered (0.00 vs +{math.log10(Rn_L):.2f}, sigma 0.13):                   separation "
     f"{math.log10(Rn_L):.3f} dex -> {o_reg:.0f}:1")
info(f"corrected     ({d_hi:+.3f} vs +{math.log10(Rn_D):.2f}, sigma sqrt(0.13^2+{sig_typ:.3f}^2)):  separation "
     f"{sep_new:.3f} dex -> {o_new:.0f}:1")
info( "so the correction cuts BOTH ways and both must be reported: the registered CENTRAL VALUE is wrong")
info( "under every evolving-DE fork (it is a band, not a point), while the registered DISCRIMINATION")
info(f"against the LCDM-native rival is if anything better ({o_new:.0f}:1 rather than {o_reg:.0f}:1) because")
info( "the two predictions move apart.  The operational danger is the paper's own rule that 'a result")
info(f"inconsistent with both values counts against both': a true framework universe with DESI dark")
info(f"energy delivers {d_hi:+.3f} to {d_lo:+.3f} dex, and a measurement landing near {d_lo:+.2f} dex is")
info( "1.0 sigma from the registered 0.00 -- inside tolerance, but a deeper fork plus a 1-sigma downward")
info( "MEASUREMENT fluctuation of 0.13 dex reaches -0.26 dex, which that rule would score AGAINST the")
info( "framework although it is the framework's own prediction. The registered value needs an")
info( "append-only amendment stating the band, not a point.")
check("B4 the registered statistic can be applied as frozen without any risk of scoring the framework's "
      "OWN evolving-dark-energy prediction as a falsification of the framework",
      abs(d_lo) + sig_typ < 0.13,
      f"deepest fork {d_lo:+.3f} dex + 1 sigma {sig_typ:.3f} = {abs(d_lo)+sig_typ:.3f} dex vs the 0.13 dex budget")
P("")
P("  B5 -- WHERE THE BARE '0.00' IS ON THE RECORD (live grep, so this check is verifiable and can rot).")
DOCS = ["README.md", "STANDING.md",
        "qwen_claude_field_theory/papers_2026/PAPER7_a0z_decisive_measurement_2026.tex",
        "qwen_claude_field_theory/papers_2026/mnras_submission_2026/COVER_LETTER.md",
        "qwen_claude_field_theory/closure_2026/TEN_HARDEST_QUESTIONS_FOR_THE_LEAD_2026-09-04.md",
        "prep_2026/a0z_crossscale/FRAMEWORK_VS_LCDM_TEST_2026.md"]
bare, qualified, missing = [], [], []
for d in DOCS:
    fp = os.path.join(REPO, d)
    if not os.path.exists(fp): missing.append(d); continue
    for ln, line in enumerate(open(fp, encoding="utf-8", errors="replace"), 1):
        if "0.00" in line and "0.33" in line:
            q = ("0.09" in line) or ("DEC" in line)
            (qualified if q else bare).append(f"{d}:{ln}")
info(f"occurrences of the frozen pair (0.00 vs +0.33): {len(bare)+len(qualified)} in {len(DOCS)-len(missing)} documents")
info(f"  QUALIFIED with the DESI value (-0.09): {len(qualified)}  -> {', '.join(qualified) if qualified else 'none'}")
info(f"  BARE 0.00, no dark-energy caveat:      {len(bare)}  -> {', '.join(bare) if bare else 'none'}")
info( "  and NOWHERE, in any of them, is there an uncertainty on the framework's own value.")
check("B5 every place the registered pair (0.00 vs +0.33) appears on the record carries the evolving-"
      "dark-energy value alongside it",
      len(bare) == 0,
      f"{len(bare)} of {len(bare)+len(qualified)} occurrences quote a bare 0.00; the -0.09 survives in "
      f"{len(qualified)} of them and no occurrence anywhere carries an error bar")
P("")
P("  B6 -- the band an append-only amendment should register, combining the three DESI DR2 combinations")
P("        with equal weight (the combination choice is itself a systematic, so it is sampled, not picked):")
allsmp = []
for name, (w0, s0, wa, sa, rho) in DESI_DR2.items():
    L2 = np.linalg.cholesky(np.array([[s0 ** 2, rho * s0 * sa], [rho * s0 * sa, sa ** 2]]))
    s = np.array([w0, wa])[:, None] + L2 @ np.random.normal(size=(2, NMC // 3))
    allsmp.append(np.log10(a0_ratio_canonical(2.5, s[0], s[1])))
allsmp = np.concatenate(allsmp)
q16, q50, q84 = np.percentile(allsmp, [16, 50, 84])
info(f"  Delta_BTFR (framework, velocity-side convention) at z = 2.5 = {q50:+.3f} "
     f"[{q16:+.3f}, {q84:+.3f}] dex (68%), on DESI DR2 evolving dark energy")
info(f"                                                              =  0.000 exactly, if w = -1")
info(f"  Delta_BTFR (LCDM-native, Dutton-Maccio 2014)               = {math.log10(Rn_D):+.3f} dex")
info(f"  registered measurement budget 0.13 dex; the two hypotheses are {math.log10(Rn_D)-q50:.3f} dex apart")
info( "  RECOMMENDED (not applied here -- frozen files are untouchable and amendments are the user's call):")
info(f"    an append-only amendment registering the framework side as a BAND, 0.00 (w = -1) to "
     f"{q16:+.3f} dex")
info( "    (DESI DR2 1-sigma low), with the decision rule stated over the band rather than a point.")
P("")

# ==================================================================================================
# C.  TARGET 2 -- the SN-only pipeline
# ==================================================================================================
P("=" * 118)
P("C -- TARGET 2: the SN-ONLY pipeline.  (w0, wa) from Pantheon+ alone, propagated through the exact law")
P("=" * 118)
_r = minimize(lambda p: chi2(p[0], p[1], p[2]), [0.30, -0.90, 0.0], method="Nelder-Mead",
              options={"xatol": 1e-6, "fatol": 1e-6, "maxiter": 6000, "maxfev": 6000})
OMS = np.linspace(0.02, 0.72, 36); W0S = np.linspace(-2.6, 0.2, 57); WAS = np.linspace(-7.0, 4.0, 89)
Og, Wg, Ag = np.meshgrid(OMS, W0S, WAS, indexing="ij")
GP = np.stack([Og.ravel(), Wg.ravel(), Ag.ravel()], axis=1)
C2 = np.empty(len(GP)); B = 4000
for i in range(0, len(GP), B): C2[i:i + B] = chi2_batch(GP[i:i + B])
C2 = C2.reshape(Og.shape)
CBEST = float(min(C2.min(), _r.fun))
DCHI2_EVOL = CHI2_LCDM - CBEST
info(f"grid {C2.size:,} points over Omega_m in [{OMS[0]:.2f},{OMS[-1]:.2f}], w0 in [{W0S[0]:.1f},{W0S[-1]:.1f}], "
     f"wa in [{WAS[0]:.1f},{WAS[-1]:.1f}] (flat priors, box stated)")
ibest = np.unravel_index(np.argmin(C2), C2.shape)
info(f"SN-only best fit: Omega_m = {OMS[ibest[0]]:.2f}, w0 = {W0S[ibest[1]]:+.2f}, wa = {WAS[ibest[2]]:+.2f}, "
     f"chi2 = {CBEST:.3f}")
info(f"flat LCDM (w0 = -1, wa = 0):                              chi2 = {CHI2_LCDM:.3f}")
info(f"  -> Delta chi2 = {DCHI2_EVOL:.3f} for TWO extra parameters.  Expected by chance under LCDM: 2.0.")

# significance of "evolving" over "constant" from SNe alone
from scipy.stats import chi2 as chi2dist
p_evol = float(1 - chi2dist.cdf(max(DCHI2_EVOL, 0.0), 2))
sig_evol = float(math.sqrt(chi2dist.ppf(max(1 - p_evol, 1e-12), 1)))
info(f"  -> p = {p_evol:.2f} (2 d.o.f.) = {sig_evol:.2f} sigma.  Supernovae ALONE see no dark-energy evolution;")
info(f"     the improvement is SMALLER than the 2.0 expected from adding two free parameters to noise.")

# --- the SN-only a0(z) band: profile likelihood (prior-free) and marginal posterior (prior stated)
Wm, Am = np.meshgrid(W0S, WAS, indexing="ij")
PROFDE = C2.min(axis=0)                                     # profile over Omega_m
LIK = np.exp(-(C2 - CBEST) / 2.0); POST2 = LIK.sum(axis=0); POST2 /= POST2.sum()
def band_profile(zv, branch):
    """Profile-likelihood interval for the DERIVED 1-parameter quantity a0(z)/a0(0): the set of values
    attainable anywhere in the (Om,w0,wa) space with dchi2 <= 1.  Prior-free."""
    r = (a0_ratio_canonical(zv, Wm, Am) if branch == "canonical" else a0_ratio_alt(zv, Wm, Am)).ravel()
    d = (PROFDE - CBEST).ravel()
    sel = np.isfinite(r) & np.isfinite(d) & (d <= 1.0)
    return (float(r[sel].min()), float(r[sel].max())) if sel.any() else (np.nan, np.nan)
def band_marg(zv, branch, post):
    r = (a0_ratio_canonical(zv, Wm, Am) if branch == "canonical" else a0_ratio_alt(zv, Wm, Am)).ravel()
    p = post.ravel(); ok = np.isfinite(r)
    r, p = r[ok], p[ok]; o = np.argsort(r); r, p = r[o], p[o]; cp = np.cumsum(p) / p.sum()
    q = lambda f: float(np.interp(f, cp, r))
    return q(0.16), q(0.50), q(0.84), q(0.025), q(0.975)
P("")
P("  C2 -- the SN-ONLY a0(z) band, canonical (rho_Lambda) footing.  Two summaries, both reported:")
P(f"  {'z':>5} | {'profile dchi2<=1':>22} | {'marginal 68%':>22} | {'marginal 95%':>24} | {'median':>7}")
ZBAND = [0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
SN_BAND = {}
for zv in ZBAND:
    pl, ph = band_profile(zv, "canonical"); l68, med, h68, l95, h95 = band_marg(zv, "canonical", POST2)
    SN_BAND[zv] = dict(prof=(pl, ph), m68=(l68, h68), m95=(l95, h95), med=med)
    P(f"  {zv:5.2f} | [{pl:8.3f},{ph:9.3f}] | [{l68:8.3f},{h68:9.3f}] | [{l95:9.3f},{h95:10.3f}] | {med:7.3f}")
info(f"prior box: flat on Omega_m in [{OMS[0]:.2f},{OMS[-1]:.2f}], w0 in [{W0S[0]:.1f},{W0S[-1]:.1f}], "
     f"wa in [{WAS[0]:.1f},{WAS[-1]:.1f}].  The marginal band is PRIOR-DOMINATED (see C3b).")
P("")
# prior sensitivity
W0S2 = np.linspace(-1.6, -0.2, 57); WAS2 = np.linspace(-3.0, 2.0, 89)
Og2, Wg2, Ag2 = np.meshgrid(OMS, W0S2, WAS2, indexing="ij")
GP2 = np.stack([Og2.ravel(), Wg2.ravel(), Ag2.ravel()], axis=1)
C2b = np.empty(len(GP2))
for i in range(0, len(GP2), B): C2b[i:i + B] = chi2_batch(GP2[i:i + B])
C2b = C2b.reshape(Og2.shape)
LIK2 = np.exp(-(C2b - C2b.min()) / 2.0); POST2b = LIK2.sum(axis=0); POST2b /= POST2b.sum()
Wm2, Am2 = np.meshgrid(W0S2, WAS2, indexing="ij")
def band_marg2(zv):
    r = a0_ratio_canonical(zv, Wm2, Am2).ravel(); p = POST2b.ravel()
    o = np.argsort(r); r, p = r[o], p[o]; cp = np.cumsum(p) / p.sum()
    return float(np.interp(0.16, cp, r)), float(np.interp(0.5, cp, r)), float(np.interp(0.84, cp, r))
info("prior sensitivity (halved prior box, w0 in [-1.6,-0.2], wa in [-3,2]):")
for zv in (1.0, 2.5):
    a, b_, c_ = band_marg2(zv)
    info(f"  z = {zv}: 68% [{a:.3f}, {c_:.3f}] median {b_:.3f}   vs wide box "
         f"[{SN_BAND[zv]['m68'][0]:.3f}, {SN_BAND[zv]['m68'][1]:.3f}] median {SN_BAND[zv]['med']:.3f}")
info("the band moves by more than its own width when the prior box is halved -> the SN-only marginal band")
info("is a statement about the PRIOR, not about the supernovae.  The profile band is the honest one.")
P("")
P("  C2b -- the SAME band on the ALT (rho_total) footing, where a0(z) is proportional to H(z), plus the")
P("         ABSOLUTE a0(z) on both footings.  (The RATIO is footing-independent WITHIN a branch; the two")
P("         branches are different functions, which is what section D measures.)")
P(f"  {'z':>5} | {'canonical ratio, prof 1s':>26} | {'alt ratio, prof 1s':>22} | "
  f"{'a0(z) canonical [m/s^2]':>25} | {'a0(z) alt [m/s^2]':>21}")
for zv in ZBAND:
    pc = SN_BAND[zv]["prof"]; pa = band_profile(zv, "alt")
    ac = (pc[0] * A0["canonical (rho_Lambda)"], pc[1] * A0["canonical (rho_Lambda)"])
    aa = (pa[0] * A0["alt (rho_total)"], pa[1] * A0["alt (rho_total)"])
    P(f"  {zv:5.2f} | [{pc[0]:11.3f},{pc[1]:12.3f}] | [{pa[0]:9.3f},{pa[1]:10.3f}] | "
      f"[{ac[0]:9.2e},{ac[1]:10.2e}] | [{aa[0]:8.2e},{aa[1]:9.2e}]")
P("")
P("  C2c -- the SN-ONLY band against the BAO+CMB-driven values the record actually uses.")
info(f"{'z':>5} {'SN-only (this lane, prof 1s)':>32} {'DESI DR2+CMB+P+ (1s, propagated)':>36} "
     f"{'repo record (DR1 chains)':>26}")
REC = {3.0: (0.710, 0.594, 0.833)}                 # real_research/A0Z_DESI_CHAINS_RESULT_2026-06.md, DR1 chains
for zv in (1.0, 2.0, 2.5, 3.0):
    L2p = np.linalg.cholesky(np.array([[s0p ** 2, rhop * s0p * sap], [rhop * s0p * sap, sap ** 2]]))
    smp = np.array([w0p, wap])[:, None] + L2p @ np.random.normal(size=(2, 200000))
    rr = a0_ratio_canonical(zv, smp[0], smp[1])
    lo, hi = np.percentile(rr, [16, 84]); md = np.median(rr)
    pc = SN_BAND[zv]["prof"]
    rec = f"{REC[zv][0]:.3f} [{REC[zv][1]:.3f},{REC[zv][2]:.3f}]" if zv in REC else "--"
    info(f"{zv:5.2f} {'['+format(pc[0],'.3f')+', '+format(pc[1],'.3f')+']':>32} "
         f"{format(md,'.3f')+' ['+format(lo,'.3f')+', '+format(hi,'.3f')+']':>36} {rec:>26}")
info("the SN-only band is 10-40x wider than the band the record quotes.  The record's band is a BAO+CMB")
info("band that supernovae only help to close; it is not a supernova measurement of a0(z), and this lane")
info("finds no way to make it one.")
P("")
w_prof = SN_BAND[2.5]["prof"][1] - SN_BAND[2.5]["prof"][0]
covers1 = SN_BAND[2.5]["prof"][0] <= 1.0 <= SN_BAND[2.5]["prof"][1]
check("C3a supernovae ALONE can distinguish the framework's a0(z) from a constant, on the CANONICAL "
      "(rho_Lambda) footing",
      (not covers1) and DCHI2_EVOL > 6.0,
      f"Delta chi2 = {DCHI2_EVOL:.2f} for 2 parameters ({p_evol*100:.0f}% probability by chance); the SN-only "
      f"1-sigma profile band at z = 2.5 is [{SN_BAND[2.5]['prof'][0]:.2f}, {SN_BAND[2.5]['prof'][1]:.2f}], "
      f"width {w_prof:.2f}, and contains 1.000")
alt1 = band_profile(1.0, "alt"); alt25 = band_profile(2.5, "alt")
check("C3b the SAME question on the ALT (rho_total) footing -- and here the answer FLIPS: because that "
      "branch says a0 is proportional to H(z), the supernovae pin it directly and to a few per cent",
      alt1[0] > 1.0 and alt25[0] > 1.0,
      f"SN-only profile 1-sigma a0(z)/a0(0) = [{alt1[0]:.2f}, {alt1[1]:.2f}] at z = 1 and "
      f"[{alt25[0]:.2f}, {alt25[1]:.2f}] at z = 2.5, both excluding a constant by a wide margin")
info("Both footings, plainly, because the difference is the whole point: on the canonical footing the")
info("supernovae say nothing about a0(z), because the ratio depends only on the dark-energy sector they")
info("barely constrain.  On the alt footing they say a great deal -- but only because a0 proportional to")
info("H(z) is the Hubble diagram itself, so the 'prediction' carries no content the expansion history did")
info("not already have.  The alt footing converts supernovae from a spectator into a precision predictor,")
info("and section D asks whether the galaxies agree.")
P("")
P("  C4 -- where the record's constraint actually comes from.  Add ONLY a CMB-like matter-density prior")
P("        (Omega_m = 0.315 +/- 0.007) to the same supernovae:")
def chi2_prior(om, w0, wa): return chi2(om, w0, wa) + ((om - 0.315) / 0.007) ** 2
C2p = C2 + ((Og - 0.315) / 0.007) ** 2
CBESTp = float(C2p.min()); LIKp = np.exp(-(C2p - CBESTp) / 2.0); POSTp = LIKp.sum(axis=0); POSTp /= POSTp.sum()
PROFp = C2p.min(axis=0)
def band_profile_p(zv):
    r = a0_ratio_canonical(zv, Wm, Am).ravel(); d = (PROFp - CBESTp).ravel()
    sel = np.isfinite(r) & (d <= 1.0)
    return (float(r[sel].min()), float(r[sel].max())) if sel.any() else (np.nan, np.nan)
ip = np.unravel_index(np.argmin(C2p), C2p.shape)
d_lcdm_p = float(chi2_prior(0.315, -1.0, 0.0) - CBESTp)
info(f"SN + Om prior best fit: w0 = {W0S[ip[1]]:+.2f}, wa = {WAS[ip[2]]:+.2f}; Delta chi2 vs w = -1 is "
     f"{d_lcdm_p:.2f} for 2 parameters")
for zv in (1.0, 2.5, 3.0):
    a, b_ = band_profile_p(zv)
    info(f"  z = {zv}: profile 1-sigma a0(z)/a0(0) in [{a:.3f}, {b_:.3f}]  (SN-only was "
         f"[{SN_BAND[zv]['prof'][0]:.3f}, {SN_BAND[zv]['prof'][1]:.3f}])")
info("even with the matter density pinned to CMB precision the supernovae do not exclude a constant a0.")
info("The framework's a0(z) departure on the record is inherited from DESI's BAO geometry combined with")
info("the CMB, NOT from supernovae; the SNe contribute by breaking the (Om, w0, wa) degeneracy, not by")
info("detecting evolution themselves.  Stated against interest: this makes the whole distinctive")
info("prediction hostage to a BAO+CMB preference that supernovae, on their own, do not corroborate.")
P("")

# ==================================================================================================
# D.  TARGET 3 -- the two density footings across the supernova redshift range
# ==================================================================================================
P("=" * 118)
P("D -- TARGET 3: the rho_Lambda / rho_total footing fork inside the supernova redshift range")
P("=" * 118)
P("  The headline equation a0 = kappa c sqrt(G rho) is ambiguous in rho.  The two readings are NOT two")
P("  normalisations of one curve -- they are two DIFFERENT functions of redshift:")
info(f"z = 0:  a0 = {A0['canonical (rho_Lambda)']:.4e} (rho_Lambda) vs {A0['alt (rho_total)']:.4e} m/s^2 "
     f"(rho_total) -- a fixed {math.log10(A0['alt (rho_total)']/A0['canonical (rho_Lambda)']):.4f} dex offset")
info( "z > 0:  the canonical branch is bump-then-decline; the alt branch is a0 proportional to H(z), a")
info( "        monotone rise.  The separation grows without limit.")
P("")
P(f"  {'z':>5} | {'canonical a0(z)/a0(0)':>22} | {'alt a0(z)/a0(0)':>17} | {'separation [dex]':>17}")
SEP = {}
for zv in (0.33, 0.5, 0.9, 1.0, 1.44, 1.68, 2.0, 2.5, 3.0):
    rc = float(a0_ratio_canonical(zv, w0p, wap)); ra = float(a0_ratio_alt(zv, w0p, wap))
    SEP[zv] = math.log10(ra / rc)
    P(f"  {zv:5.2f} | {rc:22.4f} | {ra:17.4f} | {SEP[zv]:17.3f}")
info("(evaluated on DESI DR2 + CMB + Pantheon+; on w = -1 the canonical column is exactly 1.000 and the")
info(" separation is log10 E(z), 0.253 dex at z = 1 -- the fork is not a dark-energy artefact.)")
P("")
P("  D2 -- can the supernova-era a0 measurements already in the repo separate the two branches?")
P("")
info("MUSE-DARK III (Ciocan et al. 2026, A&A 709 L16): 79 galaxies, 0.33 < z < 1.44, a0(z) = a0(0)+a1 z,")
info("  a0(0) = 1.00 +/- 0.04, a1 = +1.59 (+0.11/-0.10) x 1e-10, a0(z~1) = 2.38 (+0.12/-0.10) x 1e-10,")
info("  intrinsic scatter 0.17 dex.  The authors state reconciliation to a constant a0 would need stellar")
info("  masses larger by +0.20 to +0.45 dex, which they say is NOT supported by their consistency checks.")
muse_z, muse_val, muse_err = 1.0, 2.38, 0.11
pred_c = float(a0_ratio_canonical(muse_z, w0p, wap)); pred_a = float(a0_ratio_alt(muse_z, w0p, wap))
sep_dex = math.log10(pred_a / pred_c)
sys_floor_lo, sys_floor_hi = 0.20, 0.45                                   # the authors' own M/L offsets
# a0 = V^4/(G M_b) in deep MOND -> d log a0 = -d log M_b, so an M/L offset propagates 1:1 in dex
info(f"  at z = 1 the two branches predict {pred_c:.3f} and {pred_a:.3f}, a separation of {sep_dex:.3f} dex.")
muse_dex_err = math.hypot(muse_err / muse_val, 0.04 / 1.00) / math.log(10)
info(f"  MUSE's own formal error on a0(z~1)/a0(0) is {muse_dex_err:.3f} dex (including its a0(0) error) -- "
     f"{abs(sep_dex)/muse_dex_err:.0f}x smaller than")
info(f"  the separation, so on FORMAL errors the branches are separable and BOTH are rejected (the data sit")
info(f"  at {math.log10(muse_val):.3f} dex, above both).  But in deep MOND a0 = V^4/(G M_b), so d log a0 =")
info(f"  -d log M_b exactly: the authors' own disowned-but-required M/L offset of {sys_floor_lo:.2f}-{sys_floor_hi:.2f} dex")
info(f"  propagates 1:1 and is {sys_floor_lo/abs(sep_dex):.1f}-{sys_floor_hi/abs(sep_dex):.1f}x the branch separation.")
info(f"  Adding the quoted 0.17 dex intrinsic scatter in quadrature, the systematic floor at z = 1 is")
floor1 = math.hypot(sys_floor_lo, 0.17); floor2 = math.hypot(sys_floor_hi, 0.17)
info(f"  {floor1:.2f}-{floor2:.2f} dex against a {abs(sep_dex):.2f} dex separation.")
P("")
info("MSA-3D (NIRSpec, this repo's inversion; 23 galaxies, 0.58 < z < 1.68): the raw a0-trend +2.1 splits")
info("  into +1.13 pure acceleration-selection and +1.00 from f_DM; controlling for g_obs the genuine")
info("  trend is +0.91 [+0.05, +1.63] per unit z in units of 1e-10, ~1.1 sigma from flat.")
z_lo, z_hi = 0.58, 1.68
sl_c = (float(a0_ratio_canonical(z_hi, w0p, wap)) - float(a0_ratio_canonical(z_lo, w0p, wap))) / (z_hi - z_lo)
sl_a = (float(a0_ratio_alt(z_hi, w0p, wap)) - float(a0_ratio_alt(z_lo, w0p, wap))) / (z_hi - z_lo)
sl_c /= float(a0_ratio_canonical(z_lo, w0p, wap)); sl_a /= float(a0_ratio_alt(z_lo, w0p, wap))
msa_sl, msa_err = 0.91, (1.63 - 0.05) / 2 / 1.0
info(f"  over its own 0.58 < z < 1.68 baseline the branches predict fractional slopes {sl_c:+.2f} (canonical)")
info(f"  and {sl_a:+.2f} (alt) per unit z: a {abs(sl_a-sl_c):.2f} separation against MSA-3D's controlled")
info(f"  uncertainty of +/-{msa_err:.2f} -> {abs(sl_a-sl_c)/msa_err:.1f} sigma.")
P("")
sep_z1 = abs(sep_dex)
can_sep = (floor1 < sep_z1) and (abs(sl_a - sl_c) / msa_err > 3.0)
check("D2 the supernova-era a0 measurements already in the repo (MUSE-DARK III, MSA-3D) can separate the "
      "rho_Lambda footing from the rho_total footing",
      can_sep,
      f"MUSE systematic floor {floor1:.2f}-{floor2:.2f} dex vs a {sep_z1:.2f} dex separation; MSA-3D "
      f"{abs(sl_a-sl_c)/msa_err:.1f} sigma on the slope. Formal errors say yes, the stated systematics say no.")
info("Direction stated: this is a FAIL on the systematics, not on the physics.  The branch separation at")
info("z = 1 is large (a factor 1.8); it is the a0 = V^4/(G M_b) readout that hands the stellar-mass")
info("systematic straight into the answer at 1:1.  A gas-dominated, rotation-dominated deep-MOND target")
info("with an independent gas mass -- i.e. exactly the z ~ 2.5 object already pre-registered -- separates")
info("the branches by 0.66 dex, five times the registered 0.13 dex budget.  The footing fork is the")
info("EASIEST thing that measurement decides, and it is not what the pre-registration scores.")
P("")
P("  D3 -- WHICH WAY DOES THE SUPERNOVA-ERA ARCHIVE LEAN?  'Cannot separate' is not 'says nothing', so")
P("        the direction is reported -- but it MUST be reported over the whole archive, not over the two")
P("        measurements the lane brief named.  A first pass here used only the two SLOPE measurements and")
P("        produced a clean lean toward the rejected footing.  That was one-sided and is withdrawn: the")
P("        repo's own committed placement script already puts SIX points on this fork, and the RATIO")
P("        points go the other way.  Corrected version below.")
muse_meas = math.log10(muse_val / 1.00)
pc1, pa1 = math.log10(float(a0_ratio_canonical(1.0, w0p, wap))), math.log10(float(a0_ratio_alt(1.0, w0p, wap)))
# verbatim from prep_2026/a0z_crossscale/highz_a0z_fork_placement_2026.py, run 2026-09-08 (exit 0).
# (name, currency, sigma-from-DECLINING/canonical, sigma-from-RISING/alt, which it favours)
PLACE = [("MSA-3D selection-corrected  z 0.58-1.68", "slope", 1.45, 0.32, "alt"),
         ("MUSE-DARK III / Ciocan     z 0.33-1.44", "slope", 4.10, 1.50, "alt"),
         ("MUSE-DARK II / Jeanneau    z ~ 0.9",     "ratio", 0.00, 1.10, "canonical/flat"),
         ("Ubler+17 KMOS3D            z ~ 0.9",     "ratio", 0.79, 0.48, "alt"),
         ("Ubler+17 KMOS3D            z ~ 2.3",     "ratio", 0.68, 1.05, "canonical/flat"),
         ("Amvrosiadis+25 DSFG        z ~ 2.4",     "ratio", 0.79, 1.40, "canonical/flat")]
info(f"{'point':42s}{'currency':>10}{'sigma from canonical':>22}{'sigma from alt':>16}{'nearer':>18}")
for n, cur, sc, sa, fav in PLACE:
    info(f"{n:42s}{cur:>10}{sc:>22.2f}{sa:>16.2f}{fav:>18}")
n_alt = sum(1 for p in PLACE if p[4] == "alt"); n_can = len(PLACE) - n_alt
slope_alt = all(p[4] == "alt" for p in PLACE if p[1] == "slope")
ratio_split = [p[4] for p in PLACE if p[1] == "ratio"]
info(f"(all six placements verbatim from the repo's own prep_2026/a0z_crossscale/"
     f"highz_a0z_fork_placement_2026.py,")
info(f" re-run 2026-09-08, exit 0.  Its own verdict on every one of them: UNDERPOWERED, excludes no branch.)")
info(f"tally: {n_alt} nearer the alt (rho_total) branch, {n_can} nearer canonical/flat; every point is "
     f"below 1.5 sigma except Ciocan's slope on inflated systematics (4.1 sigma from canonical).")
check("D3 the supernova-era a0 archive leans consistently toward ONE footing, so the fork can at least be "
      "given a direction",
      (n_alt == len(PLACE)) or (n_can == len(PLACE)),
      f"it does not: {n_alt} of {len(PLACE)} points sit nearer the alt branch and {n_can} nearer canonical, "
      f"and the split is BY MEASUREMENT CURRENCY -- both SLOPE points lean alt, and the ratio points are "
      f"{ratio_split.count('canonical/flat')}-{ratio_split.count('alt')} the other way")
info("What that pattern means, stated carefully and not over-read: a genuine a0(z) would move slope and")
info("ratio estimators together.  A redshift-dependent SYSTEMATIC in the slope estimators -- pressure")
info("support, beam smearing, or an M/L drift, all of which grow with z and all of which the systematics-")
info("floor script already prices -- would move the slopes and leave the ratios alone.  The observed split")
info("is the second pattern's signature, not the first's.  But every point is under 1.5 sigma, so this is")
info("an OBSERVATION about the archive's shape and not a measurement of anything.  The two slope points the")
info("lane brief named do lean toward the branch the record rejects (Ciocan 1.5 vs 4.1 sigma, MSA-3D 0.32")
info("vs 1.45 sigma); the repo's MUSE confrontation document already records the SIGN match and calls the")
info("rejected branch an undershoot.  Nothing here is new evidence for the rho_total footing, which the")
info("coefficient-footing audit rejects on independent z = 0 grounds.")
P("")
P("  D4 -- the CONSTRUCTIVE consequence: where the fork becomes decidable with today's systematics.")
FLOORP = os.path.join(REPO, "prep_2026/a0z_crossscale/highz_systematics_floor_results.json")
FLOORS = {}
if os.path.exists(FLOORP):
    try:
        _fj = json.load(open(FLOORP))["floors"]
        for k, v in _fj.items():
            if k.startswith("dwarf") and "|TODAY|" in k:
                FLOORS[float(k.split("|z")[-1])] = ("TODAY", float(v["glob"]))
            if k.startswith("dwarf") and "|FUTURE|" in k:
                FLOORS.setdefault(float(k.split("|z")[-1]), (None, None))
        _fu = {float(k.split("|z")[-1]): float(v["glob"]) for k, v in _fj.items()
               if k.startswith("dwarf") and "|FUTURE|" in k}
    except Exception:
        FLOORS, _fu = {}, {}
else:
    FLOORS, _fu = {}, {}
if FLOORS:
    info(f"{'z':>5} {'branch separation [dex]':>25} {'TODAY coherent floor [dex]':>28} "
         f"{'FUTURE floor [dex]':>20} {'decidable?':>12}")
    for zv in sorted(FLOORS):
        sep = math.log10(float(a0_ratio_alt(zv, w0p, wap)) / float(a0_ratio_canonical(zv, w0p, wap)))
        ft = math.log10(1 + FLOORS[zv][1]); ff = math.log10(1 + _fu.get(zv, np.nan))
        info(f"{zv:5.1f} {sep:>25.3f} {ft:>28.3f} {ff:>20.3f} "
             f"{('YES today' if sep > 2*ft else ('yes, future' if sep > 2*ff else 'no')):>12}")
    info("(coherent, non-averaging floor for a gas-dominated deep-MOND dwarf, read live from the repo's own")
    info(" prep_2026/a0z_crossscale/highz_systematics_floor_results.json; 'decidable' = separation > 2x floor)")
zdec = [zv for zv in sorted(FLOORS) if math.log10(float(a0_ratio_alt(zv, w0p, wap)) /
        float(a0_ratio_canonical(zv, w0p, wap))) > 2 * math.log10(1 + FLOORS[zv][1])]
check("D4 the rho_Lambda / rho_total footing fork is decidable somewhere inside the supernova redshift "
      "range with TODAY's coherent systematic floor",
      len(zdec) > 0,
      (f"yes, at z >= {min(zdec):.1f}: the branches are {math.log10(float(a0_ratio_alt(min(zdec),w0p,wap))/float(a0_ratio_canonical(min(zdec),w0p,wap))):.2f} dex apart "
       f"against a {math.log10(1+FLOORS[min(zdec)][1]):.2f} dex coherent floor" if zdec else
       "no z in the tabulated range clears twice the floor"))
info("This is the lane's one constructive output: the supernovae give the alt branch a sharp, few-per-cent")
info("prediction (C3b), the branches separate by 0.54-0.77 dex at z = 2-3, and that exceeds twice the")
info("repo's own coherent floor at z = 3 (and twice the FUTURE floor already at z = 2).  The SAME z ~ 2.5")
info("object already pre-registered for the 0.00-vs-+0.33 test settles the internal footing fork as a free")
info("by-product: 0.66 dex of separation against the registered 0.13 dex budget (5x), or against the")
info("generic uncurated-dwarf coherent floor of ~0.34 dex (2x).  Worth adding to the pre-registration's")
info("stated deliverables by amendment -- it costs no extra observing time.")
P("")

# ==================================================================================================
# E.  TARGET 4 -- the lensing-magnification angle
# ==================================================================================================
P("=" * 118)
P("E -- TARGET 4: the gravitational-lensing signal in supernova Hubble residuals")
P("=" * 118)
P("  In this framework there are no dark haloes: the lensing convergence toward a supernova is sourced by")
P("  baryons plus the kernel.  Pantheon+ models the lensing scatter as sigma_lens = A x 0.055 z mag with")
P("  A = 1 (Jonsson et al. 2010).  If A is measurable, the mass distribution is probed on Mpc scales.")
Zc = TAB["zHD"][MASK]; DIAG = TAB["m_b_corr_err_DIAG"][MASK]
RAWE = TAB["m_b_corr_err_RAW"][MASK]; VPE = TAB["m_b_corr_err_VPEC"][MASK]
EXTRA_V = DIAG ** 2 - RAWE ** 2 - VPE ** 2
info(f"error budget decomposition (medians): the non-fit, non-peculiar-velocity variance is "
     f"{np.median(EXTRA_V):.4f} mag^2")
info(f"  = an intrinsic/bias-correction floor of ~{math.sqrt(np.median(EXTRA_V)):.3f} mag; the lensing term "
     f"(0.055 z)^2 is {np.median((0.055*Zc[Zc>0.7])**2):.5f} mag^2 at z > 0.7")
for lo, hi in [(0.1, 0.4), (0.4, 0.7), (0.7, 1.2), (1.2, 2.3)]:
    s = (Zc >= lo) & (Zc < hi)
    if s.sum() == 0: continue
    frac = np.median((0.055 * Zc[s]) ** 2) / np.median(DIAG[s] ** 2)
    info(f"  z in [{lo},{hi}): N = {int(s.sum()):4d}, lensing is {100*frac:5.2f}% of the per-SN variance")
# --- the power calculation: profile likelihood on A with the intrinsic floor free
mu_best = mu_shape(OM_LCDM, -1.0, 0.0)
RES = MB - mu_best; RES = RES - (IO @ RES) / NORM
selE = Zc > 0.1
def nll(par, A):
    s_int = par[0]
    if s_int <= 0: return 1e9
    v = RAWE[selE] ** 2 + VPE[selE] ** 2 + s_int ** 2 + (A * 0.055 * Zc[selE]) ** 2
    return 0.5 * float(np.sum(RES[selE] ** 2 / v + np.log(v)))
from scipy.optimize import minimize_scalar as ms1
def prof_A(A):
    r = ms1(lambda s: nll([s], A), bounds=(0.01, 0.60), method="bounded", options={"xatol": 1e-7})
    return float(r.fun)
Agrid = np.linspace(0.0, 8.0, 401)
NLLg = np.array([prof_A(a) for a in Agrid])
iA = int(np.argmin(NLLg)); Ahat = float(Agrid[iA]); dl = 2 * (NLLg - NLLg[iA])
def cross(target):
    m = dl >= target
    up = Agrid[m & (Agrid > Ahat)]
    return float(up.min()) if len(up) else np.inf
A1s = cross(1.0); A2s = cross(4.0)
dl_at_0 = float(dl[0])
info(f"profile likelihood on the lensing amplitude A (intrinsic floor free, {int(selE.sum())} SNe at z > 0.1,")
info(f"  diagonal errors -- the covariance is a model for the MEAN, the scatter test is per-SN):")
SIG_A = (A2s - Ahat) / 2.0                                  # a 1-sigma-equivalent width on A
info(f"  A_hat = {Ahat:.2f} (at the physical boundary A >= 0);  1-sigma upper {A1s:.2f};  95% upper {A2s:.2f}.")
info(f"  Nominal A = 1 is disfavoured by Delta chi2 = {float(dl[np.argmin(abs(Agrid-1.0))]):.2f}; A = 0 by "
     f"Delta chi2 = {dl_at_0:.2f} ({math.sqrt(max(dl_at_0,0)):.1f} sigma).")
info(f"  i.e. Pantheon+ does not DETECT its own assumed lensing term: against a single constant intrinsic")
info(f"  floor the data prefer NO lensing scatter and put the nominal A = 1 right at the 95% boundary.")
info(f"  The 1-sigma-equivalent width on A is {SIG_A:.2f} -- the amplitude is simply not measured.")
info( "  (Read as a degeneracy, not a tension: Pantheon+'s own model uses a survey-dependent intrinsic")
info( "   floor and a redshift-dependent bias-correction scatter, both of which absorb a rising term.")
info( "   Allowing that freedom here would only WIDEN the interval on A, never narrow it.)")
# what difference would a baryons-plus-kernel convergence field make?
info("")
info("what would have to be resolved:  the kernel is calibrated to reproduce galaxy-galaxy lensing on")
info("  exactly these scales (the KiDS radial-acceleration test, 0.601 sigma on the record), so the")
info("  framework's convergence field is CONSTRUCTED to sit close to LCDM's where the data already are.")
info("  A generous allowance for the remaining difference -- all matter clumped with baryons instead of")
info("  85% of it in smooth haloes -- is a change in sigma_kappa of order tens of percent, i.e. |A-1| ~ 0.3.")
TARGET_A = 0.3
check("E2 the supernova lensing-magnification signal has ANY discriminating power between a baryons-plus-"
      "kernel convergence field and LCDM's",
      SIG_A < TARGET_A / 2,
      f"the effect to be resolved is |A-1| ~ {TARGET_A:.1f}; Pantheon+ measures A to +/-{SIG_A:.2f}, "
      f"{SIG_A/TARGET_A:.1f}x too coarse, and does not detect the lensing term itself "
      f"({math.sqrt(max(dl_at_0,0)):.1f} sigma from A = 0). Underpowered by a factor {SIG_A/(TARGET_A/2):.0f}; "
      f"stop here -- this is an honest power calculation, not a result")
P("")

# ==================================================================================================
# F.  BONUS -- the low-z Hubble-diagram scatter as a bound on the framework's velocity field
# ==================================================================================================
P("=" * 118)
P("F -- BONUS: the low-redshift Hubble-diagram scatter as a direct bound on the peculiar-velocity field")
P("=" * 118)
P("  This is the angle the repo's supernova work has never used.  hunt_2026/h85_bulk_flow_null.py records")
P("  that the framework's kernel, applied naively to the linear velocity field, boosts it by nu ~ 9 at the")
P("  Local Group acceleration -- while the framework's own relativistic completion carries a theorem")
P("  (delta Y^(1) = 0) that makes linear growth LCDM's.  Supernova magnitudes at z < 0.06 are dominated by")
P("  peculiar velocities, so the Hubble diagram bounds that boost independently of any reconstruction.")
P("")
selF = (Zc > 0.01) & (Zc < 0.06)
def nll_pec(par, Apec):
    s_int = par[0]
    if s_int <= 0: return 1e9
    v = RAWE[selF] ** 2 + (Apec * VPE[selF]) ** 2 + s_int ** 2
    return 0.5 * float(np.sum(RES[selF] ** 2 / v + np.log(v)))
Ag2 = np.linspace(0.0, 4.0, 401)
NLL2 = np.array([float(ms1(lambda s: nll_pec([s], a), bounds=(0.01, 0.60), method="bounded").fun) for a in Ag2])
j = int(np.argmin(NLL2)); Ap = float(Ag2[j]); dl2 = 2 * (NLL2 - NLL2[j])
up2 = Ag2[(dl2 >= 4.0) & (Ag2 > Ap)]; Ap95 = float(up2.min()) if len(up2) else np.inf
sig_v_assumed = 250.0
info(f"{int(selF.sum())} supernovae at 0.01 < z < 0.06; Pantheon+ assumes a residual peculiar-velocity")
info(f"  dispersion of {sig_v_assumed:.0f} km/s after its 2M++ correction.")
info(f"  fitted multiplier on that dispersion: A_pec = {Ap:.2f}, 95% upper limit {Ap95:.2f}")
info(f"  -> residual sigma_v < {Ap95*sig_v_assumed:.0f} km/s at 95%.")
NU_NAIVE = 9.0
_sint = float(ms1(lambda s: nll_pec([s], Ap), bounds=(0.01, 0.60), method="bounded").x)
info(f"  (fitted intrinsic floor at the same time: {_sint:.3f} mag)")
info(f"  a naive kernel boost of the velocity field by nu = {NU_NAIVE:.0f} would give sigma_v ~ "
     f"{NU_NAIVE*sig_v_assumed:.0f} km/s and a magnitude scatter of "
     f"{2.1715*NU_NAIVE*sig_v_assumed*1e3/(C_LIGHT*0.02):.2f} mag at z = 0.02 --")
info(f"  {NU_NAIVE/Ap95:.0f}x the supernova bound.")
info( "  why the 2M++ correction does not rescue the boosted case (stated explicitly, because it is the")
info( "  obvious objection): the correction is v_pred = beta x (reconstructed density), with beta")
info( "  calibrated in LCDM.  A kernel-boosted velocity-density relation has a LARGER true beta, so")
info(f"  applying the LCDM beta removes only ~1/nu of the flow and leaves ~{NU_NAIVE-1:.0f}x the LCDM residual --")
info( "  which is the quantity the Hubble-diagram scatter measures.  The bound therefore applies to the")
info( "  boosted world too; it is not an artefact of correcting the data with the null hypothesis.")
check("F1 the low-redshift supernova Hubble diagram is CONSISTENT with the framework's own linear-growth "
      "theorem (LCDM-like velocities) and independently EXCLUDES the naive kernel-boosted velocity field",
      Ap95 < 2.0 and Ap95 * sig_v_assumed < NU_NAIVE * sig_v_assumed / 3,
      f"sigma_v < {Ap95*sig_v_assumed:.0f} km/s vs {NU_NAIVE*sig_v_assumed:.0f} km/s for a naive nu = 9 boost; "
      f"the framework's OWN prediction (delta Y^(1) = 0 -> LCDM growth) passes, the naive reading does not")
info("Both ways, plainly: this is a PASS for the framework's own relativistic completion and a KILL for the")
info("naive modified-gravity reading of the velocity field.  It is a second, independent route to h85's")
info("null, using a dataset h85 never touched.  It is NOT evidence for the framework over LCDM -- LCDM")
info("makes the identical prediction and the test cannot separate them.")
P("")

# ==================================================================================================
# G.  VERDICT
# ==================================================================================================
P("=" * 118); P("G -- VERDICT"); P("=" * 118)
live_direct = (DCHI2_EVOL > 6.0) or can_sep or (SIG_A < TARGET_A / 2)
check("G1 supernova data, ON THEIR OWN, have live discriminating power for this framework -- i.e. some "
      "supernova measurement by itself can move a verdict on a0(z), on the footing fork, or on the kernel",
      live_direct,
      f"SN-only evolution {DCHI2_EVOL:.2f} chi2 for 2 params ({sig_evol:.2f} sigma); the SN-era a0 "
      f"measurements cannot separate the footings through their stated systematics; SN lensing is not "
      f"detected at all. On the canonical footing SNe enter as an INPUT to (w0, wa), never as a test.")
check("G2 supernovae nevertheless SHARPEN a framework prediction that another instrument can then decide "
      "-- the constructive half of the same finding",
      (alt1[0] > 1.5) and (len(zdec) > 0) and (sig_typ < 0.06),
      f"they pin the alt branch to a0(1)/a0(0) = [{alt1[0]:.2f}, {alt1[1]:.2f}] and the canonical branch's "
      f"z = 2.5 zero point to +/-{sig_typ:.3f} dex; the two branches separate by 0.66 dex at z = 2.5, which "
      f"the already-pre-registered object decides for free")
P("")
P("  the three-sentence verdict:")
P("  1. Supernovae are an INPUT to this framework, not a test of it: on their own they show no dark-energy")
P("     evolution at all (Delta chi2 = %.2f for two extra parameters, %.0f%% by chance, %.2f sigma), the" % (DCHI2_EVOL, p_evol * 100, sig_evol))
P("     canonical-footing SN-only a0(z) band at z = 2.5 is [%.2f, %.2f] -- consistent with constant and with" % (SN_BAND[2.5]["prof"][0], SN_BAND[2.5]["prof"][1]))
P("     almost anything else -- and the record's much tighter band is BAO+CMB geometry that supernovae only")
P("     help to close, so the framework's distinctive prediction is hostage to a preference the supernovae")
P("     do not corroborate on their own.")
P("  2. The one place supernovae bite hard is the REGISTERED prediction: the deep-MOND zero point goes as")
P("     a0^{1/4} and a0 tracks rho_DE, so 'flat 0.00 dex at z ~ 2.5' holds only in the w = -1 limit -- under")
P("     every evolving-dark-energy fork on the record the framework's own value is %+.3f to %+.3f dex with a" % (d_hi, d_lo))
P("     %.3f dex within-fork error (%.0f-%.0f%% of the registered 0.13 dex budget, and the deepest fork plus" % (sig_typ, abs(d_hi)/0.13*100, abs(d_lo)/0.13*100))
P("     one sigma reaches %.3f dex, past it), it appears bare in %d of %d places on the record, and it should" % (abs(d_lo)+sig_typ, len(bare), len(bare)+len(qualified)))
P("     be registered by append-only amendment as a BAND, %+.3f to 0.00 dex, not as a point." % q16)
P("  3. Nothing here favours this framework over LCDM and nothing here is a win: the supernova lensing angle")
P("     is dead on arrival (Pantheon+ does not detect its own lensing term, %.1f sigma, and is %.1fx too" % (math.sqrt(max(dl_at_0, 0)), SIG_A / TARGET_A))
P("     coarse for the effect), the supernova-era a0 archive is split %d-%d on the internal footing fork with" % (n_alt, n_can))
P("     the split falling along MEASUREMENT CURRENCY rather than redshift -- the signature of a z-dependent")
P("     systematic in the slope estimators, not of a0 evolution -- and the one clean new result, the low-z")
P("     Hubble diagram bounding any residual peculiar-velocity boost to under %.1fx, %.0fx below a naive" % (Ap95, NU_NAIVE / Ap95))
P("     kernel-boosted field, confirms the framework's own linear-growth theorem while making exactly the")
P("     same prediction as LCDM.")
P("")
P("=" * 118)
P(f"SUMMARY: {len(FAILS)} FAIL(s)")
for f in FAILS: P("  FAIL: " + f)
P("=" * 118)
