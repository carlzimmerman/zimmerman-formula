#!/usr/bin/env python3
"""
SKEPTIC AUDIT of ciocan_a0z_chi2.py.  Both-ways.  Tests the load-bearing claims:
  - is the NORM-marginalized (shape-only) test the FAIR one?  (yes -- a0(0) is an INPUT)
  - does MUSE's rising SLOPE survive marginalizing the offset?  what sigma?
  - is the Magneticum nuisance applied honestly?
  - are the binned errors + 30sigma claim using REAL errors?
  - re-run the load-bearing chi^2 for the DECLINING branch under treatment (b).

VERIFIED-FROM-PAPER (WebFetch arXiv:2604.22613 abstract + A&A full text aa59230-26):
  intercept a0(0) = 1.0 +0.04/-0.04   (1e-10)   VERBATIM
  slope     a1    = 1.59 +0.11/-0.10  (1e-10/z) VERBATIM  -> 1-sig ~ 0.105, NOT 0.054
  a0(z~1)         = 2.38 +/- 0.1                 VERBATIM
  lowest-z bin a0 ~ 1.99 ; highest-z bin a0 ~ 2.71   VERBATIM (endpoints)
  four QUANTILE z bins (~equal N => N~20 each); scatter 0.13 dex (low z) -> 0.19 dex (high z)
  "~30 sigma" = OVERALL trend across all points, NOT the slope error
                (a1/sig_a1 = 1.59/0.105 = 15.1 sigma is the honest slope significance)
  Figure-read middle bins (AI vision, imprecise): ~2.33 (z~0.68), ~2.52 (z~0.92)
                -- the script used a STRAIGHT-LAW reconstruction 2.20, 2.45 (slightly LOWER).
"""
import numpy as np
from scipy.stats import chi2 as chi2dist, norm

# ---------------------------------------------------------------- data variants
z_bins  = np.array([0.45, 0.65, 0.90, 1.15])     # quantile bin centers (approx)
# (A) script's straight-law reconstruction
a0_straight = np.array([1.99, 2.20, 2.45, 2.71])
# (B) figure-read (convex-ish) -- endpoints same, middles HIGHER
a0_figread  = np.array([1.99, 2.33, 2.52, 2.71])
err_bins = np.array([0.13, 0.17, 0.22, 0.27])    # script's per-bin 1-sig (scatter/sqrt(N))

# paper-quoted robust objects
a1_paper, a1_err_paper = 1.59, 0.105    # VERBATIM (+0.11/-0.10 -> ~0.105)
a0int_paper, a0int_err = 1.00, 0.04     # VERBATIM

# ---------------------------------------------------------------- branch ratios
fw_z = np.array([0.0,0.40,1.0,2.0,3.0]); fw_r = np.array([1.0,1.0615,1.01,0.86,0.737])
r_framework = lambda z: np.interp(z, fw_z, fw_r)
r_flat      = lambda z: np.ones_like(np.atleast_1d(z), dtype=float)
Om, OL = 0.31, 0.69
r_rising    = lambda z: np.sqrt(Om*(1+z)**3 + OL)
r_mag       = lambda z: (Om*(1+z)**3 + OL)**(0.89/2.0)

def sig(chi2v, dof):
    if dof <= 0: return 0.0
    p = max(chi2dist.sf(chi2v, dof), 1e-300)
    return norm.isf(p/2.0)

def normmarg(rfun, a0, err):
    """free-amplitude (shape-only) chi2; analytic 1-param LSQ."""
    b = rfun(z_bins); w = 1/err**2
    A = np.sum(w*a0*b)/np.sum(w*b*b)
    c = np.sum(w*(a0-A*b)**2)
    return c, len(z_bins)-1, A, sig(c, len(z_bins)-1)

print("="*88)
print("PART 1 -- NORM-MARGINALIZED (shape-only) chi2, BOTH data variants, REAL errors")
print("="*88)
for label, a0 in [("straight-law (script)", a0_straight), ("figure-read (convex)", a0_figread)]:
    print(f"\n  data = {label}:  {list(a0)}")
    for nm, rf in [("framework_declining",r_framework),("flat",r_flat),("rising_cH",r_rising)]:
        c, d, A, s = normmarg(rf, a0, err_bins)
        print(f"    {nm:20s}: chi2={c:6.2f}/{d}  A_best={A:5.3f}  -> {s:4.2f} sigma")

print("\n" + "="*88)
print("PART 2 -- ERROR-ASSUMPTION SENSITIVITY (the most arbitrary script choice)")
print("  per-bin err = intrinsic-scatter-dex / sqrt(N).  Vary N and the dex floor.")
print("="*88)
# scatter per bin in dex (paper: 0.13 low z -> 0.19 high z), converted to fractional abs err
scat_dex = np.array([0.13,0.145,0.165,0.19])
for Nbin in [10, 20, 30]:
    err_se = scat_dex*np.log(10) * a0_straight / np.sqrt(Nbin)   # std error of mean per bin
    c,d,A,s = normmarg(r_framework, a0_straight, err_se)
    cf,_,Af,sf = normmarg(r_flat, a0_straight, err_se)
    print(f"  N/bin={Nbin:2d}: declining {s:4.2f}s (A={A:.2f}) | flat {sf:4.2f}s   [median err~{np.median(err_se):.3f}]")

print("\n" + "="*88)
print("PART 3 -- SLOPE-ONLY test with the PAPER'S REAL a1 error (0.105, not 0.054)")
print("  This is the cleanest shape test: framework SHAPE-slope vs a1=1.59 +/- 0.105.")
print("="*88)
zlo, zhi = z_bins[0], z_bins[-1]
for nm, rf in [("framework_declining",r_framework),("flat",r_flat),("rising_cH",r_rising)]:
    _,_,A,_ = normmarg(rf, a0_straight, err_bins)
    slope = A*(rf(np.array([zhi]))[0]-rf(np.array([zlo]))[0])/(zhi-zlo)
    print(f"  {nm:20s}: shape-slope={slope:+6.3f}/z | vs 1.59+/-0.105 -> {abs(slope-a1_paper)/a1_err_paper:4.1f} sigma")
print("  NOTE: flat predicts slope=0 EXACTLY -> a1=1.59/0.105 = 15.1 sigma is the")
print("        irreducible slope significance on the paper's OWN stat error (no recon).")

print("\n" + "="*88)
print("PART 4 -- IS THE MAGNETICUM NUISANCE HONEST?  (over-subtraction check)")
print("="*88)
slope_mag = (r_mag(np.array([zhi]))[0]-r_mag(np.array([zlo]))[0])/(zhi-zlo)
print(f"  Magneticum E(z)^0.89 shape-slope over data range = {slope_mag:+.3f}/z (ratio units)")
print(f"  As fraction of MUSE's +1.59/z slope (norm to a0(0)~2 abs): {slope_mag*2.1/a1_paper*100:4.0f}%")
print("  -> the template, scaled to the data's OWN amplitude (~2.1e-10), supplies a LARGE")
print("     fraction of the rise.  At a0(0)~1 it supplies ~50%.  The (c) result is")
print("     amplitude-sensitive: with a FREE amplitude AND a free Magneticum coeff on only")
print("     4 points (2 dof), the fit has enough freedom to absorb almost ANY smooth shape")
print("     -> chi2~0 is partly OVER-FITTING, not purely physical absorption.")
# Demonstrate the overfitting: 2 free params on 4 points with a monotonic template
b = r_framework(z_bins); t = r_mag(z_bins); w = 1/err_bins**2
S11=np.sum(w*b*b);S12=np.sum(w*b*t);S22=np.sum(w*t*t);b1=np.sum(w*a0_straight*b);b2=np.sum(w*a0_straight*t)
det=S11*S22-S12*S12; A=(S22*b1-S12*b2)/det; B=(-S12*b1+S11*b2)/det
print(f"  2-param fit (decl base + mag templ): A={A:+.2f}, B={B:+.2f}  (B can go NEGATIVE/large -> sign of overfit)")

print("\n" + "="*88)
print("PART 5 -- HONEST BOTTOM LINE (declining branch, the load-bearing number)")
print("="*88)
c,d,A,s = normmarg(r_framework, a0_straight, err_bins)
cf,_,_,sf = normmarg(r_framework, a0_figread, err_bins)
print(f"  NORM-MARG (shape-only, straight-law data, the script's number): {s:.2f} sigma")
print(f"  NORM-MARG (shape-only, figure-read data, middles higher):       {sf:.2f} sigma")
print(f"  SLOPE-only on paper's REAL a1 error (flat branch, no recon):    {a1_paper/a1_err_paper:.1f} sigma")
print(f"  -> The honest shape tension is ~2-3 sigma on binned points (recon-dependent),")
print(f"     but the slope a1=1.59 differs from flat's 0 at 15 sigma on the paper's OWN")
print(f"     statistical error.  The COLLAPSE to ~2 sigma requires the per-bin errors to be")
print(f"     ~2x larger than scatter/sqrt(N~20) implies.  See Part 2.")
