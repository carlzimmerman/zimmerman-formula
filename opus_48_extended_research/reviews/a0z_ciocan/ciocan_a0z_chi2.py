#!/usr/bin/env python3
"""
chi^2 / sigma-exclusion of THREE a0(z) branches against Ciocan et al. (MUSE-DARK III,
A&A 709 L16, arXiv:2604.22613) binned a0(z), under THREE treatments:

  (a) RAW                       -- absolute a0(z) = 9.36e-11 x branch-ratio vs the binned points
  (b) NORMALIZATION-MARGINALIZED-- minimize chi^2 over a free a0(z=0) amplitude (SHAPE-only test);
                                   this is the FAIR test under the framework's quarantine
                                   (a0(0) is a multiplicative INPUT, never derived).
  (c) SYSTEMATIC-MARGINALIZED   -- additionally absorb the Magneticum LCDM-assembly apparent-a0
                                   drift (Mayer+2023) as a nuisance EVERY model inherits, AND fold
                                   the un-budgeted pressure-support / M-L systematic into the errors.

Branches (a0(z)/a0(0) ratios; a0(0)_framework = 9.36e-11 m/s^2):
  - FRAMEWORK declining  : a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)) on DESI w0wa (NON-MONOTONIC:
                           +6% bump @z~0.4 then decline). Values banked in FRONT_A0Z_DESI_2026-06-20.
  - FLAT                 : a0(z)/a0(0) = 1 at all z  (constant-a0 MOND / LCDM).
  - RISING-cH (rival)    : a0(z)/a0(0) = E(z) = sqrt(Om(1+z)^3 + OL),  Om=0.31.

Both-ways (Carl #1 rule): report sigma in EACH treatment honestly. Do NOT manufacture
'non-diagnostic' by over-marginalizing; do NOT high-priest a real slope tension away.

QUARANTINE: a0/Z/kappa never derived; a0(0) is an INPUT -> treatment (b) (free amplitude,
SHAPE-only) is the honest fair test of the framework's distinctive content.
"""
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import chi2 as chi2dist
from scipy.stats import norm

# -----------------------------------------------------------------------------
# 1. CIOCAN BINNED DATA  (all a0 in 1e-10 m/s^2)
#    Endpoint bins (z~0.45, z~1.15) are VERBATIM from the text; the two middle bins are
#    RECONSTRUCTED by interpolating along the paper's own straight a0(z)=1.0+1.59z law.
#    Per-bin errors = intrinsic scatter / sqrt(N~20), floored conservatively.
# -----------------------------------------------------------------------------
z_bins   = np.array([0.45, 0.65, 0.90, 1.15])
a0_bins  = np.array([1.99, 2.20, 2.45, 2.71])     # measured a0 (1e-10)
err_bins = np.array([0.13, 0.17, 0.22, 0.27])     # per-bin 1-sigma (1e-10)

# Robust paper-quoted objects (used for the SLOPE-level cross-check):
a1_paper      = 1.59    # da0/dz (1e-10 per unit z), VERBATIM
a1_paper_err  = 0.054   # 1-sigma from 95% CI (+0.11/-0.10) -> ~0.054
a0_int_paper  = 1.00    # intercept a0(0) (1e-10), VERBATIM
a0_z1_paper   = 2.38    # a0 at z~1 (1e-10), VERBATIM

# -----------------------------------------------------------------------------
# 2. BRANCH RATIO MODELS  r(z) = a0(z)/a0(0)
# -----------------------------------------------------------------------------
a0_framework_abs = 0.936   # framework a0(0) in 1e-10 m/s^2  (= 9.36e-11)

# FRAMEWORK declining sqrt(rho_DE) branch -- banked DESI w0=-0.752, wa=-0.86 values.
# Non-monotonic: +6% bump @z~0.4 then decline. Interpolate the banked anchor points.
fw_z   = np.array([0.0, 0.40, 1.0, 2.0, 3.0])
fw_r   = np.array([1.0, 1.0615, 1.01, 0.86, 0.737])
def r_framework(z):
    return np.interp(z, fw_z, fw_r)

# FLAT
def r_flat(z):
    return np.ones_like(np.atleast_1d(z)).astype(float)

# RISING-cH / E(z)
Om, OL = 0.31, 0.69
def r_rising(z):
    return np.sqrt(Om*(1+z)**3 + OL)

# MUSE self-model (1 + 1.59 z) / 1.0   -- a sanity reference (should give chi2 ~ 0 at raw)
def r_muse(z):
    return (a0_int_paper + a1_paper*z) / a0_int_paper

branches = {
    "framework_declining": (r_framework, a0_framework_abs),
    "flat":                (r_flat,      a0_framework_abs),
    "rising_cH":           (r_rising,    a0_framework_abs),
    "MUSE_self":           (r_muse,      a0_int_paper),     # reference only
}

# -----------------------------------------------------------------------------
# 3. MAGNETICUM LCDM-ASSEMBLY DRIFT TEMPLATE  (Mayer+2023, arXiv:2206.04333)
#    Apparent-a0 rise in a LCDM sim with NO fundamental a0: ~x3 from z=0 to z=2.3,
#    modeled as E(z)^p with p=0.89 calibrated to that x3.  Over the MUSE data range
#    its effective slope is ~+0.80/z -- itself ~15sigma BELOW MUSE's +1.59.
# -----------------------------------------------------------------------------
p_mag = 0.89
def r_magneticum(z):
    return (Om*(1+z)**3 + OL)**(p_mag/2.0)   # E(z)^p

# -----------------------------------------------------------------------------
# 4. chi^2 MACHINERY
# -----------------------------------------------------------------------------
def chi2_raw(rfun, A_abs):
    """ (a) RAW: model a0(z) = A_abs * r(z), fixed amplitude. """
    model = A_abs * rfun(z_bins)
    return np.sum(((a0_bins - model)/err_bins)**2)

def chi2_marg_amplitude(rfun, extra_template=None, err=None):
    """
    Minimize chi^2 over a free linear amplitude A (and, if extra_template given, a free
    coefficient B on the nuisance template added IN QUADRATURE-LINEAR to the model ratio).
    Returns (chi2_min, dof, A_best).
    With a free amplitude only -> tests SHAPE only.  This is a linear least squares:
        model_i = A * base_i  (+ B*templ_i)  -> solve normal equations.
    """
    if err is None:
        err = err_bins
    base = rfun(z_bins)
    w = 1.0/err**2
    if extra_template is None:
        # 1-parameter linear fit: a0_i = A*base_i
        A = np.sum(w*a0_bins*base)/np.sum(w*base*base)
        model = A*base
        chi2v = np.sum(w*(a0_bins-model)**2)
        dof = len(z_bins) - 1
        return chi2v, dof, A
    else:
        templ = extra_template(z_bins)
        # 2-parameter linear fit: a0_i = A*base_i + B*templ_i
        S11 = np.sum(w*base*base); S12 = np.sum(w*base*templ); S22 = np.sum(w*templ*templ)
        b1  = np.sum(w*a0_bins*base); b2 = np.sum(w*a0_bins*templ)
        det = S11*S22 - S12*S12
        A = ( S22*b1 - S12*b2)/det
        B = (-S12*b1 + S11*b2)/det
        model = A*base + B*templ
        chi2v = np.sum(w*(a0_bins-model)**2)
        dof = len(z_bins) - 2
        return chi2v, dof, (A, B)

def chi2_to_sigma(chi2v, dof):
    """ Convert a chi^2 with dof to an equivalent one-sided Gaussian sigma via the
    survival-function p-value (two-sided -> one-tail). """
    if dof <= 0:
        return 0.0, 1.0
    p = chi2dist.sf(chi2v, dof)          # prob of chi2 >= observed
    p = max(p, 1e-300)
    sigma = norm.isf(p/2.0)              # two-sided -> sigma
    return sigma, p

# -----------------------------------------------------------------------------
# 5. RUN ALL TREATMENTS
# -----------------------------------------------------------------------------
print("="*86)
print("CIOCAN (MUSE-DARK III) a0(z) -- chi^2 / sigma-exclusion of THREE branches")
print("binned points (1e-10):", list(zip(z_bins, a0_bins, err_bins)))
print("="*86)

results = {}
for name, (rfun, A_abs) in branches.items():
    # (a) RAW
    c_raw = chi2_raw(rfun, A_abs)
    dof_raw = len(z_bins)                       # fixed abs amplitude, 0 free params
    s_raw, p_raw = chi2_to_sigma(c_raw, dof_raw)

    # (b) NORMALIZATION-MARGINALIZED (free amplitude, SHAPE-only)
    c_b, dof_b, A_b = chi2_marg_amplitude(rfun)
    s_b, p_b = chi2_to_sigma(c_b, dof_b)

    # (c) SYSTEMATIC-MARGINALIZED: free amplitude + free Magneticum-drift template,
    #     AND inflate errors by the un-budgeted pressure-support/M-L systematic.
    #     Systematic floor: full-sample scatter 0.17 dex ~ 39% -> add ~0.30 (1e-10) per
    #     bin in quadrature as the un-error-budgeted floor (conservative, both-ways).
    sys_floor = 0.17*np.log(10) * (A_abs*rfun(z_bins))   # 0.17 dex fractional -> abs (1e-10)
    err_sys = np.sqrt(err_bins**2 + (0.5*sys_floor)**2)  # half the dex-floor, quadrature
    c_c, dof_c, AB_c = chi2_marg_amplitude(rfun, extra_template=r_magneticum, err=err_sys)
    s_c, p_c = chi2_to_sigma(c_c, dof_c)

    results[name] = dict(raw=(c_raw,dof_raw,s_raw), normm=(c_b,dof_b,s_b,A_b),
                         sysm=(c_c,dof_c,s_c))
    print(f"\n--- {name} ---")
    print(f"  (a) RAW            : chi2={c_raw:7.2f} / {dof_raw} dof  -> {s_raw:5.2f} sigma  (A fixed={A_abs:.3f})")
    print(f"  (b) NORM-MARG SHAPE: chi2={c_b:7.2f} / {dof_b} dof  -> {s_b:5.2f} sigma  (A_best={A_b:.3f} e-10)")
    print(f"  (c) SYST-MARG      : chi2={c_c:7.2f} / {dof_c} dof  -> {s_c:5.2f} sigma")

# -----------------------------------------------------------------------------
# 6. SLOPE-LEVEL CROSS-CHECK (the robust, paper-quoted object)
#    Compare each branch's effective slope da0/dz over the data range (with A free,
#    so it is the SHAPE slope) to the paper's a1 = 1.59 +/- 0.054.
#    da0/dz_branch = A_best * d r(z)/dz  (linearized over 0.45..1.15).
# -----------------------------------------------------------------------------
print("\n" + "="*86)
print("SLOPE-LEVEL CROSS-CHECK vs paper a1 = 1.59 +/- {:.3f} (1e-10 /z)".format(a1_paper_err))
print("(slope from the free-amplitude SHAPE fit, linearized over z=0.45..1.15)")
print("="*86)
zlo, zhi = z_bins[0], z_bins[-1]
for name, (rfun, A_abs) in branches.items():
    if name == "MUSE_self":
        continue
    _, _, A_b = chi2_marg_amplitude(rfun)
    slope = A_b * (rfun(np.array([zhi]))[0] - rfun(np.array([zlo]))[0]) / (zhi - zlo)
    nsig_slope = abs(slope - a1_paper)/a1_paper_err
    print(f"  {name:20s}: SHAPE slope={slope:+6.3f}/z  vs 1.59 -> {nsig_slope:5.1f} sigma (formal stat err)")

# -----------------------------------------------------------------------------
# 7. SLOPE WITH SYSTEMATIC ERROR ON a1  (both-ways: the paper's a1 carries an
#    un-budgeted pressure-support/M-L + LCDM-assembly systematic).
#    Magneticum LCDM-apparent slope over the range = +0.80/z. Treat the SHARED LCDM
#    drift as a systematic floor on a1: the framework only needs to disagree with the
#    part of the slope NOT explained by LCDM-assembly.
# -----------------------------------------------------------------------------
print("\n" + "="*86)
print("BOTH-WAYS: slope tension with the LCDM-assembly systematic folded in")
print("="*86)
slope_mag = r_magneticum(np.array([zhi]))[0] - r_magneticum(np.array([zlo]))[0]
slope_mag /= (zhi - zlo)
slope_mag_abs = slope_mag * (a0_int_paper)  # in 1e-10 /z scale (apparent-a0 units ~1)
print(f"  Magneticum LCDM-apparent SHAPE slope over data range ~ {slope_mag:+.3f}/z (ratio units)")
print(f"  => MUSE +1.59 is steeper than even the LCDM forward-model; the EXCESS over LCDM")
print(f"     is the only part any fundamental-a0 model must explain.")
# residual slope MUSE must-explain after removing LCDM-apparent part (scaled to a0(0)=1):
resid_slope = a1_paper - slope_mag*a0_int_paper
# systematic error on a1: combine stat (0.054) with a generous LCDM-template-spread systematic.
# Magneticum itself is "x3 to z=2.3" with model-spread; take ~50% of its slope as the sys uncertainty.
a1_sys = 0.5*abs(slope_mag*a0_int_paper)
a1_err_tot = np.sqrt(a1_paper_err**2 + a1_sys**2)
print(f"  residual slope MUSE must explain beyond LCDM ~ {resid_slope:+.3f}/z")
print(f"  total a1 error (stat (+) LCDM-template sys) ~ {a1_err_tot:.3f}/z")
for name, (rfun, A_abs) in branches.items():
    if name == "MUSE_self":
        continue
    _, _, A_b = chi2_marg_amplitude(rfun)
    slope = A_b * (rfun(np.array([zhi]))[0] - rfun(np.array([zlo]))[0]) / (zhi - zlo)
    nsig = abs(slope - a1_paper)/a1_err_tot
    print(f"  {name:20s}: SHAPE slope={slope:+6.3f}/z vs 1.59 with sys -> {nsig:5.1f} sigma")

# -----------------------------------------------------------------------------
# 8. HEADLINE SUMMARY for the framework's flat/declining shape
# -----------------------------------------------------------------------------
print("\n" + "="*86)
print("HEADLINE -- framework's flat/declining branch exclusion in EACH treatment")
print("="*86)
for nm in ["framework_declining", "flat"]:
    r = results[nm]
    print(f"  {nm:20s}:  RAW {r['raw'][2]:5.2f}s | NORM-MARG {r['normm'][2]:5.2f}s | SYST-MARG {r['sysm'][2]:5.2f}s")
print("\nRISING-cH rival (for reference):")
r = results["rising_cH"]
print(f"  {'rising_cH':20s}:  RAW {r['raw'][2]:5.2f}s | NORM-MARG {r['normm'][2]:5.2f}s | SYST-MARG {r['sysm'][2]:5.2f}s")
print("\nMUSE_self reference (should be ~0 raw):")
r = results["MUSE_self"]
print(f"  {'MUSE_self':20s}:  RAW {r['raw'][2]:5.2f}s | NORM-MARG {r['normm'][2]:5.2f}s")
