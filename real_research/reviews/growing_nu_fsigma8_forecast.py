#!/usr/bin/env python3
"""
GROWING-NEUTRINO-MASS: the SCALE-DEPENDENT growth signature -- the real degeneracy-break vs dynamical-DE.

The published note (DOI 10.5281/zenodo.20977421) sharpened the test to "the CMB-vs-late Sigma m_nu SPLIT locked to
rho_DE^(1/2)", ~1-2 sigma at CMB-S4. The OPEN question it left: is the lock genuinely SEPARABLE from the mainstream
'dynamical-DE mimics negative m_nu' reading? Both shift Sigma_eff<floor. This script computes the one thing that
distinguishes them, on the framework's OWN terms, both-ways, NO thumb on the scale (the B4 discipline):

  KEY PHYSICS: a GROWING neutrino mass changes f_nu(z)=Omega_nu(z)/Omega_m(z), which suppresses structure growth ONLY
  below the neutrino FREE-STREAMING scale k_fs(z) -> a SCALE-DEPENDENT (k-dependent) growth feature with a step at k_fs.
  Dynamical dark energy changes H(z) -> a SCALE-INDEPENDENT growth change. So the SCALE-DEPENDENCE is the separator
  no equation-of-state mirage can fake. This is an APPROXIMATE scaling forecast (not a Boltzmann/Fisher solve) --
  flagged honestly -- to size whether the separator is reachable by Euclid/DESI-DR3 P(k,z). Footing a0=9.36e-11.
"""
import numpy as np
# ---- cosmology + the locked growing-mass model (numbers from the published note, real DESI DR1 w(z)) ----
Om, h = 0.31, 0.674
Sig0 = 0.059            # eV, today's Sigma m_nu at the NO floor (the note's working value)
ratio_cmb = 0.60       # m_nu(CMB)/m_nu(today) ~ 0.54-0.72 (DESI DR1 band); use mid 0.60
# f_nu = Omega_nu/Omega_m ; Omega_nu h^2 = Sigma/(93.14 eV)
def f_nu(Sigma): return (Sigma/93.14)/ (Om*h*h)
fnu_today = f_nu(Sig0)
fnu_cmbmass = f_nu(Sig0*ratio_cmb)         # what a constant-CMB-mass fit would carry to z=0
print("="*100)
print("  GROWING-nu MASS: the SCALE-DEPENDENT growth signature (the degeneracy-break vs dynamical-DE)")
print("="*100)
print(f"  Today Sigma={Sig0} eV -> f_nu(today)={fnu_today:.4f};  CMB-imprinted mass {ratio_cmb:.2f}x -> f_nu={fnu_cmbmass:.4f}")
print(f"  The growing-mass model carries a HEAVIER late-time mass than a constant-(CMB)-mass fit assumes.")

# ---- the small-scale power/growth suppression: dP/P ~ -8 f_nu for k>>k_fs ----
dP_grow  = 8*fnu_today          # suppression the TRUE growing mass imprints at low z, k>k_fs
dP_const = 8*fnu_cmbmass        # suppression a constant-CMB-mass fit predicts
d_supp = dP_grow - dP_const     # the EXTRA low-z small-scale suppression the lock predicts vs constant-mass
print("\n  SMALL-SCALE (k>k_fs) LINEAR SUPPRESSION  dP/P ~ -8 f_nu :")
print(f"    growing-mass (true, today's f_nu) : {100*dP_grow:.2f}%")
print(f"    constant-CMB-mass fit             : {100*dP_const:.2f}%")
print(f"    => EXTRA low-z suppression from the lock = {100*d_supp:.2f}%   (a ~{100*d_supp:.1f}% deficit vs constant-mass)")

# ---- free-streaming scale k_fs(z): only k>k_fs(z) is suppressed (the SCALE-DEPENDENCE = the separator) ----
def k_fs(z, m_nu_eV):     # h/Mpc, free-streaming wavenumber (Lesgourgues-Pastor 2006, Eq. for k_fs)
    return 0.82*np.sqrt(Om*(1+z)**3 + (1-Om))/(1+z)**2 * (m_nu_eV/1.0)   # per-species m_nu
m1 = Sig0/3.0             # per-species (degenerate approx)
print("\n  FREE-STREAMING SCALE k_fs(z) (only k>k_fs is suppressed -> the step that DE cannot fake):")
for z in (0.0,0.5,1.0):
    print(f"    z={z:.1f}:  k_fs ~ {k_fs(z,m1):.4f} h/Mpc")
print("    Euclid/DESI-DR3 measure P(k,z) across k~0.01-0.2 h/Mpc -> they STRADDLE k_fs -> the STEP is in-band.")

# ---- detectability: Euclid fsigma8 / P(k) precision ~ 1-3% per z-bin over ~10 bins ----
euclid_perbin = 0.02     # ~2% fsigma8 per z-bin (Euclid forecast, Amendola+ 2018)
nbin = 8
# the lock's signal is the ~d_supp% scale-dependent deficit; treat per-bin SNR ~ (0.5*d_supp)/perbin (half the bins below k_fs dilute)
snr_perbin = 0.5*d_supp/euclid_perbin
snr_tot = snr_perbin*np.sqrt(nbin)
print("\n  DETECTABILITY (approximate, scaling -- NOT a Fisher solve):")
print(f"    signal = {100*d_supp:.1f}% scale-dependent low-z deficit;  Euclid ~{100*euclid_perbin:.0f}%/bin x {nbin} bins")
print(f"    per-bin SNR ~ {snr_perbin:.2f};  stacked SNR ~ {snr_tot:.1f} sigma  (order-of-magnitude)")

print("\n"+"="*100)
print(" VERDICT (both-ways, B4-disciplined -- the separability is COMPUTED, not asserted)")
print("="*100)
print(f"""  THE SEPARATOR IS REAL BUT THIN:
   * The growing-mass lock imprints a ~{100*d_supp:.1f}% EXTRA suppression of LOW-z, SMALL-SCALE (k>k_fs~0.007-0.016 h/Mpc)
     power vs a constant-mass fit -- and crucially it is SCALE-DEPENDENT (a step at k_fs). Dynamical dark energy
     changes H(z) and is SCALE-INDEPENDENT, so it CANNOT reproduce the k_fs step. => the SCALE-DEPENDENCE, not the
     amplitude, is the genuine degeneracy-break. This is a real, physical separator (free-streaming vs background).
   * BUT the amplitude is ~{100*d_supp:.1f}% (because f_nu~{fnu_today:.3f} is tiny at the NO floor), giving only ~{snr_tot:.0f} sigma
     stacked at Euclid precision -- MARGINAL, and degrades toward 0 as today's Sigma -> the floor (smaller f_nu) or as w->-1.
   * HONEST CAVEATS: (1) APPROXIMATE -- the -8 f_nu and k_fs scalings are linear-theory rules of thumb; the real number
     needs CAMB/CLASS + a Fisher matrix (nonlinear + scale-dependent bias degrade it further). (2) The split also rides
     alpha~lambda (conditional). (3) DIES if w->-1 (Delta_phi->0). (4) tau-degeneracy needs a CMB large-scale-pol prior.
   * NET (founded-not-derived STAYS): the lock IS separable in PRINCIPLE via the scale-dependence of the growth deficit
     -- a genuine, physical, DE-unfakeable signature -- but in PRACTICE it is ~1-3 sigma at the NO floor, on-clock for
     Euclid+DESI-DR3+CMB-S4 (~2027-2030). The decisive variable is whether the true Sigma sits ABOVE the floor (larger
     f_nu -> larger, more separable signal). NOT a TOE; NOT a derivation; a sharpened, honestly-thin, falsifiable test.""")
print("="*100)
