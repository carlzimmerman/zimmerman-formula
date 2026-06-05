#!/usr/bin/env python3
"""
LEDGER MASTER NUMBERS — independent recomputation of every headline value that
goes into the ULTRA-PRECISION PREDICTIONS LEDGER.

Recomputes from the mandated constants only. Asserts nothing not computed here.
Cross-checks the VERIFIER's recomputed values for each channel.

Scope of THIS script (the cross-channel spine that every channel shares):
  - a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_Lambda), Lambda = 3 OmL H0^2/c^2
  - Z = c H_Lambda / a0  (pure number sqrt(32pi/3)); kappa = 1/2
  - statistical (cosmological) error on a0 from H0, OmL (analytic + Monte Carlo)
  - mu interpolating-function SYSTEMATIC band (simple-mu vs McGaugh RAR)
  - a0(z) evolution via DESI CPL rho_DE(z), and the channel exponents that ride it
  - the per-channel headline ratios/offsets (all coefficient-free, share the same lever)
The per-channel data fits (SPARC scatter, eRASS1 eta, dSph sigmas) are produced by
the channel scripts and are quoted from the VERIFIER; here we reproduce the analytic
spine and the evolution numbers, which is what the ledger table is keyed on.
"""

import numpy as np
np.seterr(over='ignore', invalid='ignore', divide='ignore')  # tame extreme-tail w0/wa draws in MC

# ----------------------------------------------------------------------
# MANDATED CONSTANTS (exact list)
# ----------------------------------------------------------------------
c     = 299792458.0          # m/s (exact)
G     = 6.67430e-11          # CODATA 2018
Msun  = 1.98892e30           # kg
Mpc   = 3.0857e22            # m
AU    = 1.495978707e11       # m

# Planck 2018
H0_kms   = 67.36             # km/s/Mpc
H0_err   = 0.54
OmL      = 0.6847
OmL_err  = 0.0073
OmM      = 0.3153
OmM_err  = 0.0073

# DESI DR2 CPL dark energy
w0, w0_err = -0.752, 0.057
wa, wa_err = -0.86,  0.22

# MOND interpolating-function anchors (the systematic)
a0_simplemu = 9.1e-11        # simple-mu fit
a0_RAR      = 1.20e-10       # McGaugh RAR

pi = np.pi

def H0_SI(H0_kms_val):
    return H0_kms_val * 1.0e3 / Mpc   # s^-1

# ----------------------------------------------------------------------
# 1. THE SCALE: a0, Lambda, rho_Lambda, cH_Lambda, Z, kappa
# ----------------------------------------------------------------------
def a0_from_cosmo(H0_kms_val, OmL_val):
    H0 = H0_SI(H0_kms_val)
    Lam = 3.0 * OmL_val * H0**2 / c**2          # Lambda [m^-2]
    a0  = c**2 * np.sqrt(Lam / (32.0 * pi))
    return a0, Lam, H0

a0_0, Lambda, H0 = a0_from_cosmo(H0_kms, OmL)
rho_Lambda = Lambda * c**2 / (8.0 * pi * G)     # kg/m^3
n_H        = rho_Lambda / 1.6726219e-27          # H-atoms / m^3
H_Lambda   = c * np.sqrt(Lambda / 3.0)           # = sqrt(Lambda/3)*c  -> cH_Lambda below
cH_Lambda  = c * H_Lambda
# identity check: (c/2) sqrt(G rho_Lambda)
a0_alt = 0.5 * c * np.sqrt(G * rho_Lambda)
Z      = cH_Lambda / a0_0
kappa  = a0_0 / (c * np.sqrt(G * rho_Lambda))    # should be exactly 1/2
Z_exact = np.sqrt(32.0 * pi / 3.0)

print("="*72)
print("1. SCALE / COEFFICIENT")
print("="*72)
print(f"Lambda          = {Lambda:.5e} m^-2")
print(f"rho_Lambda      = {rho_Lambda:.5e} kg/m^3   ({n_H:.2f} H-atoms/m^3)")
print(f"cH_Lambda       = {cH_Lambda:.5e} m/s^2")
print(f"a0 (c^2 form)   = {a0_0:.5e} m/s^2  = {a0_0*1e10:.4f}e-10")
print(f"a0 ((c/2) form) = {a0_alt:.5e} m/s^2   [identity match: {np.isclose(a0_0,a0_alt)}]")
print(f"Z = cH_Lambda/a0 = {Z:.6f}   (exact sqrt(32pi/3) = {Z_exact:.6f})")
print(f"kappa            = {kappa:.6f}   (exact 1/2)")

# ----------------------------------------------------------------------
# 2. STATISTICAL (cosmological) error on a0:  a0 ~ OmL^(1/2) H0^(1)
# ----------------------------------------------------------------------
# analytic partials (independent OmL, H0 — as in the channel scripts)
rel_H0  = 1.0 * (H0_err / H0_kms)          # exponent 1 on H0
rel_OmL = 0.5 * (OmL_err / OmL)            # exponent 1/2 on OmL
rel_a0  = np.hypot(rel_H0, rel_OmL)

# Monte Carlo cross-check
rng = np.random.default_rng(20260605)
N = 4_000_000
H0s  = rng.normal(H0_kms, H0_err, N)
OmLs = rng.normal(OmL,    OmL_err, N)
a0_mc = np.array([])  # avoid building huge; vectorize:
H0_si_mc = H0s*1e3/Mpc
Lam_mc   = 3.0*OmLs*H0_si_mc**2/c**2
a0_samp  = c**2*np.sqrt(Lam_mc/(32*pi))
rel_a0_mc = a0_samp.std()/a0_samp.mean()

# correlated case (Planck base-LCDM OmL,H0 are POSITIVELY correlated; verifier note)
# analytic: var(rel) = relH0^2 + relOmL^2 + 2 rho relH0 relOmL  (a0 ~ H0^1 OmL^1/2)
rel_a0_corr05 = np.sqrt(rel_H0**2 + rel_OmL**2 + 2*0.5*rel_H0*rel_OmL)
rel_a0_corr1  = np.sqrt(rel_H0**2 + rel_OmL**2 + 2*1.0*rel_H0*rel_OmL)

print("\n" + "="*72)
print("2. STATISTICAL (cosmological) error on a0")
print("="*72)
print(f"H0 term       = {rel_H0*100:.3f}%")
print(f"OmL term      = {rel_OmL*100:.3f}%")
print(f"quadrature    = {rel_a0*100:.3f}%   (independent)")
print(f"Monte Carlo   = {rel_a0_mc*100:.3f}%   (N={N:,})")
print(f"a0 abs err    = +/- {a0_0*rel_a0*1e10:.4f}e-10 m/s^2")
print(f"  [if OmL,H0 correlated rho=+0.5: {rel_a0_corr05*100:.3f}%; rho=+1: {rel_a0_corr1*100:.3f}%]")

# ----------------------------------------------------------------------
# 3. mu interpolating-function SYSTEMATIC band
# ----------------------------------------------------------------------
# referenced to McGaugh RAR; full span; geometric-mean band
sys_vs_RAR   = abs(a0_simplemu - a0_RAR)/a0_RAR          # 'McGaugh own RAR systematic' style
full_span    = (a0_RAR - a0_simplemu)/a0_simplemu        # referenced to simple-mu
geo_mean     = np.sqrt(a0_simplemu * a0_RAR)
half_span_geo= 0.5*(a0_RAR - a0_simplemu)/geo_mean       # +/- about geo mean
gap_fw_to_RAR= (a0_0 - a0_RAR)/a0_RAR                     # framework below RAR
gap_fw_simple= (a0_0 - a0_simplemu)/a0_simplemu
# sigma_stat distance of framework from each anchor
sig = a0_0*rel_a0
n_sig_simple = (a0_0 - a0_simplemu)/sig
n_sig_RAR    = (a0_0 - a0_RAR)/sig

print("\n" + "="*72)
print("3. mu SYSTEMATIC band (simple-mu 9.1e-11 vs McGaugh RAR 1.2e-10)")
print("="*72)
print(f"|simple-RAR|/RAR        = {sys_vs_RAR*100:.1f}%   (McGaugh-referenced)")
print(f"(RAR-simple)/simple     = {full_span*100:.1f}%   (full span, simple-referenced)")
print(f"geo-mean a0             = {geo_mean*1e10:.4f}e-10")
print(f"half-span about geomean = +/-{half_span_geo*100:.2f}%")
print(f"framework vs RAR        = {gap_fw_to_RAR*100:+.1f}%  ({n_sig_RAR:+.1f} sigma_stat)")
print(f"framework vs simple-mu  = {gap_fw_simple*100:+.1f}%  ({n_sig_simple:+.1f} sigma_stat)")

# ----------------------------------------------------------------------
# 4. a0(z) EVOLUTION via DESI CPL, and the channel exponents
# ----------------------------------------------------------------------
def rho_DE_ratio(z, w0v, wav):
    a = 1.0/(1.0+z)
    return a**(-3.0*(1.0+w0v+wav)) * np.exp(-3.0*wav*(1.0-a))

def a0_ratio(z, w0v, wav):           # a0(z)/a0(0) = sqrt(rho_DE ratio)
    return np.sqrt(rho_DE_ratio(z, w0v, wav))

# central evolution
zs = [0.3, 0.4, 1, 2, 3, 4, 5, 6]
print("\n" + "="*72)
print("4. a0(z) EVOLUTION (DESI CPL central w0,wa) and channel exponents")
print("="*72)
print("Exponents on rho_DE(z)/rho_DE0 for each observable:")
print("  a0(z)        : 1/2   (a0 ~ sqrt rho_DE)")
print("  V_flat/BTFR  : 1/8   (V ~ a0^1/4)")
print("  sigma_dSph   : 1/8   (sigma ~ a0^1/4)")
print("  D mass-disc  : 1/4   (deep-MOND D ~ sqrt a0)")
print("  alpha_lens   : 1/4   (alpha ~ sqrt a0)")
print("  e_N EFE      : -1/2  (e_N ~ 1/a0)")
print()
hdr = f"{'z':>4} | {'rhoDE':>8} | {'a0(z)/a0(0)':>11} | {'dlogV(dex)':>10} | {'dV%':>7} | {'D ratio':>8} | {'sig ratio':>9} | {'eN ratio':>8}"
print(hdr); print("-"*len(hdr))
for z in zs:
    r  = rho_DE_ratio(z, w0, wa)
    a0r= np.sqrt(r)
    dlogV = (1.0/8.0)*np.log10(r)
    dVpc  = (10**dlogV - 1.0)*100
    Dr    = r**0.25
    sigr  = r**0.125
    eNr   = 1.0/a0r
    print(f"{z:>4} | {r:>8.4f} | {a0r:>11.4f} | {dlogV:>+10.4f} | {dVpc:>+7.2f} | {Dr:>8.4f} | {sigr:>9.4f} | {eNr:>8.4f}")

# evolution errors by Monte Carlo over DESI w0,wa
def evo_mc(z, exponent_on_rho, rho_corr, Nmc=400000, seed=777):
    r = np.random.default_rng(seed)
    # correlated draws via Cholesky; clamp |rho|<1 to keep cov positive-definite
    rc = np.clip(rho_corr, -0.999999, 0.999999)
    cov = np.array([[w0_err**2, rc*w0_err*wa_err],
                    [rc*w0_err*wa_err, wa_err**2]])
    Lc = np.linalg.cholesky(cov)
    zz = r.standard_normal((2, Nmc))
    d  = Lc @ zz
    w0s = w0 + d[0]; was = wa + d[1]
    rr = rho_DE_ratio(z, w0s, was)
    val = rr**exponent_on_rho
    return val

print("\nEvolution 1-sigma errors (Monte Carlo, DESI w0,wa):")
print("  (a0(z)/a0(0) uses exponent 1/2; dlogV exponent 1/8 in dex space)")
for rho_corr, tag in [(-0.9, "corr=-0.9 (DESI anti-corr)"), (0.0, "independent")]:
    print(f"  -- {tag} --")
    for z in [1,2,3,4,5,6]:
        a0r_s = evo_mc(z, 0.5, rho_corr)
        # dlogV distribution
        rr_s  = evo_mc(z, 1.0, rho_corr)
        dlogV_s = (1.0/8.0)*np.log10(rr_s)
        dV_s    = (10**dlogV_s - 1.0)
        print(f"    z={z}: a0ratio={a0r_s.mean():.4f}+/-{a0r_s.std():.4f} ({a0r_s.std()/a0r_s.mean()*100:.1f}%) | "
              f"dlogV={dlogV_s.mean():+.4f}+/-{dlogV_s.std():.4f} dex | dV={dV_s.mean()*100:+.2f}+/-{dV_s.std()*100:.2f}%")

# z=3 headline a0 evolution % and a0(z=3) absolute
r3 = rho_DE_ratio(3, w0, wa)
a0_z3 = a0_0*np.sqrt(r3)
a0r3_s = evo_mc(3, 0.5, 0.0)  # independent (matches the 25% quoted in a0-scale channel)
print(f"\na0(z=3)/a0(0) = {np.sqrt(r3):.4f} +/- {a0r3_s.std():.4f}  ({a0r3_s.std()/a0r3_s.mean()*100:.1f}%, independent w0/wa)")
print(f"a0(z=3) abs   = {a0_z3*1e10:.4f}e-10 m/s^2")

# peak redshift of rho_DE (thawing DE rises then falls)
zz = np.linspace(0, 2, 20001)
rr = rho_DE_ratio(zz, w0, wa)
zpk = zz[np.argmax(rr)]
cross1 = zz[np.argmin(np.abs(rr-1.0)[zz>0.1])+np.argmax(zz>0.1)]
print(f"\nrho_DE peaks at z = {zpk:.3f}  (ratio {rr.max():.4f}, i.e. +{(rr.max()-1)*100:.1f}% over today)")
print(f"rho_DE crosses back to 1 near z ~ {1.0/(1.0): .0f} ... (search):")
# find crossing for z>zpk
mask = zz>zpk
idx = np.argmin(np.abs(rr[mask]-1.0))
print(f"   rho_DE = 1 again at z ~ {zz[mask][idx]:.3f}")

# ----------------------------------------------------------------------
# 5. CHANNEL-SPECIFIC ABSOLUTE NUMBERS that derive purely from a0 (z=0)
# ----------------------------------------------------------------------
print("\n" + "="*72)
print("5. CHANNEL ABSOLUTE NUMBERS from a0(z=0) [framework a0]")
print("="*72)

# --- lensing saturated deflection alpha_inf = 2 pi sqrt(G M a0)/c^2 ---
def alpha_inf_arcsec(M_Msun, a0v):
    M = M_Msun*Msun
    rad = 2.0*pi*np.sqrt(G*M*a0v)/c**2
    return np.degrees(rad)*3600.0
for M in [1e11, 1e13, 1e14]:
    print(f"  lensing alpha_inf({M:.0e} Msun) = {alpha_inf_arcsec(M, a0_0):.4f} arcsec  (framework a0)")
print(f"  lensing alpha_inf(1e13, z=0.4 peak) = {alpha_inf_arcsec(1e13, a0_0)*rr.max()**0.5:.4f} arcsec (approx, ratio sqrt(rhoDE peak))")
# alpha statistical & systematic (alpha ~ sqrt a0)
alpha_stat = 0.5*rel_a0
alpha_sys  = 0.5*half_span_geo
print(f"  alpha statistical = +/-{alpha_stat*100:.2f}%  ; alpha mu-systematic = +/-{alpha_sys*100:.2f}% (half-span)")

# --- wide binary transition separation s_t = sqrt(G M / a0) ---
def s_t_AU(M_Msun, a0v):
    M = M_Msun*Msun
    return np.sqrt(G*M/a0v)/AU
M_wb = 1.5
print(f"\n  wide-binary s_t(1.5 Msun) = {s_t_AU(M_wb, a0_0):.1f} AU  (framework a0)")
print(f"     s_t band [RAR..simple] = [{s_t_AU(M_wb, a0_RAR):.0f}, {s_t_AU(M_wb, a0_simplemu):.0f}] AU")
print(f"     s_t stat err = +/-{0.5*rel_a0*s_t_AU(M_wb,a0_0):.0f} AU ({0.5*rel_a0*100:.2f}%)  [s_t ~ a0^-1/2]")
# geometric-mean identity prefactor
rS  = 2*G*(M_wb*Msun)/c**2
rhz = c/np.sqrt(Lambda/3.0)/np.sqrt(1.0)  # rough horizon scale c/H_Lambda
pref= np.sqrt(G*(M_wb*Msun)/a0_0)/np.sqrt(rS*(c/ H_Lambda))
print(f"     prefactor (2 sqrt(3 OmL/32pi))^-1/2 = {(2*np.sqrt(3*OmL/(32*pi)))**-0.5:.6f}")

# --- dwarf isolated deep-MOND sigma = (4 G M a0 / 81)^(1/4) ; coefficient check ---
print(f"\n  dwarf isolated coeff (4/81)^(1/4) = {(4.0/81.0)**0.25:.4f}  (Milgrom isolated)")
print(f"  dwarf EFE coeff (2/9)             = {2.0/9.0:.4f}")

# ----------------------------------------------------------------------
# 6. FORECAST: the decisive beta test, stat-only Fisher sanity
# ----------------------------------------------------------------------
print("\n" + "="*72)
print("6. FORECAST beta (a0~rho_DE^(beta/2)); stat-only Fisher sanity")
print("="*72)
# observable offset O(z) = (1/8) log10(rho_DE ratio) * beta ; dO/dbeta = (1/8) log10(ratio)
# per-galaxy scatter sigma_g = 0.06 dex
sig_g = 0.06
for z, Nfor in [(3, 83), (3, 30), (5, 24), (5, 9), (3.5, 60)]:
    r = rho_DE_ratio(z, w0, wa)
    dOdb = (1.0/8.0)*np.log10(r)          # dex per unit beta
    sig_beta = sig_g/np.sqrt(Nfor)/abs(dOdb)
    print(f"  z={z}, N={Nfor}: |dO/dbeta|={abs(dOdb):.4f} dex, sigma(beta)_stat={sig_beta:.3f} -> {1.0/sig_beta:.2f} sigma (beta=1 vs 0)")

print("\nDONE. All numbers above computed from the mandated constants in this script.")
