#!/usr/bin/env python3
"""
INDEPENDENT adversarial verification of the 'a0-scale' channel.
Recompute everything from scratch. No reuse of the original script's functions.
"""
import numpy as np
from math import pi, sqrt, exp

# ------------------------------------------------------------------
# Constants (mandated)
# ------------------------------------------------------------------
c    = 299792458.0       # m/s exact
G    = 6.67430e-11       # m^3 kg^-1 s^-2
Msun = 1.98892e30        # kg
Mpc  = 3.0857e22         # m

# Planck 2018
H0_kms      = 67.36
H0_kms_err  = 0.54
OmL         = 0.6847
OmL_err     = 0.0073
Om_m        = 0.3153
Om_m_err    = 0.0073

# DESI DR2 CPL
w0, w0_err = -0.752, 0.057
wa, wa_err = -0.86,  0.22

# Observed a0 endpoints
a0_RAR    = 1.20e-10
a0_simple = 9.1e-11

print("="*90)
print("INDEPENDENT RECOMPUTATION  --  a0 = c^2 sqrt(Lambda/32pi)")
print("="*90)

# ------------------------------------------------------------------
# Step 1: H0 in SI
# ------------------------------------------------------------------
H0 = H0_kms * 1.0e3 / Mpc          # s^-1
print(f"\nH0            = {H0:.6e} s^-1")
print(f"  cross-check: 67.36 km/s/Mpc -> 67.36e3/3.0857e22 = {67.36e3/3.0857e22:.6e}")

# ------------------------------------------------------------------
# Step 2: Lambda = 3 OmL H0^2 / c^2
# ------------------------------------------------------------------
Lam = 3.0 * OmL * H0**2 / c**2
print(f"\nLambda        = 3 * {OmL} * ({H0:.6e})^2 / ({c:.0f})^2")
print(f"              = {Lam:.6e} m^-2   (claim 1.0891e-52)")

# ------------------------------------------------------------------
# Step 3: a0 = c^2 sqrt(Lambda/32pi)
# ------------------------------------------------------------------
a0 = c**2 * sqrt(Lam / (32.0*pi))
print(f"\na0            = c^2 sqrt(Lambda/32pi)")
print(f"              = {c**2:.6e} * sqrt({Lam:.6e}/{32*pi:.6f})")
print(f"              = {a0:.6e} m/s^2   (claim 9.355e-11)")
print(f"              = {a0*1e10:.5f} e-10")

# ------------------------------------------------------------------
# Step 4: rho_Lambda = Lambda c^2 / (8 pi G)  and the (c/2)sqrt(G rho_L) identity
# ------------------------------------------------------------------
rho_L = Lam * c**2 / (8.0*pi*G)
print(f"\nrho_Lambda    = Lambda c^2/(8 pi G) = {rho_L:.6e} kg/m^3   (claim 5.835e-27)")
print(f"  H-atoms/m^3 (m_H=1.67262e-27) = {rho_L/1.67262e-27:.3f}   (claim 3.49)")
a0_alt = 0.5 * c * sqrt(G * rho_L)
print(f"\n(c/2)sqrt(G rho_L) = {a0_alt:.6e}   matches a0? {np.isclose(a0, a0_alt, rtol=1e-12)}")

# Algebraic proof that (c/2)sqrt(G rho_L) == c^2 sqrt(Lambda/32pi):
# (c/2)sqrt(G * Lam c^2/(8 pi G)) = (c/2) * c * sqrt(Lam/(8 pi)) = c^2/2 * sqrt(Lam/(8pi))
#   = c^2 sqrt(Lam/(4*8pi)) = c^2 sqrt(Lam/(32 pi)).  YES identical.
print("  algebra: (c/2)sqrt(G rho_L)=(c^2/2)sqrt(Lam/8pi)=c^2 sqrt(Lam/32pi)  [exact identity]")

# ------------------------------------------------------------------
# Step 5: cH_Lambda, H_Lambda, Z, kappa
# ------------------------------------------------------------------
H_Lam  = c * sqrt(Lam/3.0)
cH_Lam = c * H_Lam
print(f"\nH_Lambda      = c sqrt(Lambda/3) = {H_Lam:.6e} s^-1")
print(f"  check sqrt(OmL)*H0 = {sqrt(OmL)*H0:.6e}  (should equal H_Lambda) -> {np.isclose(H_Lam, sqrt(OmL)*H0)}")
print(f"cH_Lambda     = {cH_Lam:.6e} m/s^2   (claim 5.415e-10)")

Z = cH_Lam / a0
Z_analytic = sqrt(32.0*pi/3.0)
print(f"\nZ = cH_Lam/a0 = {Z:.6f}   analytic sqrt(32pi/3) = {Z_analytic:.6f}   (claim 5.7888)")
kappa = a0 / (c * sqrt(G*rho_L))
print(f"kappa         = a0/(c sqrt(G rho_L)) = {kappa:.6f}   (claim 0.50000)")

# ------------------------------------------------------------------
# Step 6: STATISTICAL error -- analytic partials
#   a0 ~ OmL^(1/2) * H0^(1)
# ------------------------------------------------------------------
rel_OmL = 0.5 * OmL_err / OmL
rel_H0  = 1.0 * H0_kms_err / H0_kms
rel_stat = sqrt(rel_OmL**2 + rel_H0**2)
print("\n" + "-"*90)
print("STATISTICAL (cosmological) error -- analytic")
print("-"*90)
print(f"  OmL term : (1/2)(0.0073/0.6847) = {rel_OmL*100:.4f}%   (claim 0.533%)")
print(f"  H0  term : (0.54/67.36)         = {rel_H0*100:.4f}%   (claim 0.802%)")
print(f"  quadrature                      = {rel_stat*100:.4f}%   (claim 0.96%)")
print(f"  abs: a0 = {a0*1e10:.4f} +/- {rel_stat*a0*1e10:.4f} e-10  (claim +/-0.0090e-10)")

# ------------------------------------------------------------------
# Step 7: Monte Carlo cross-check (independent RNG seed)
# ------------------------------------------------------------------
rng = np.random.default_rng(424242)
N = 4_000_000
oS = rng.normal(OmL, OmL_err, N)
hS = rng.normal(H0_kms, H0_kms_err, N)
oS = np.clip(oS, 1e-9, None)
HS = hS*1e3/Mpc
LamS = 3.0*oS*HS**2/c**2
a0S = c**2*np.sqrt(LamS/(32.0*pi))
print("\n" + "-"*90)
print(f"MONTE CARLO (N={N:,}, independent OmL,H0)")
print("-"*90)
print(f"  a0 mean = {a0S.mean():.6e}  std = {a0S.std(ddof=1):.6e}  = {a0S.std(ddof=1)/a0S.mean()*100:.4f}%")
print(f"  -> MC {a0S.std(ddof=1)/a0S.mean()*100:.4f}% vs analytic {rel_stat*100:.4f}%")

# Z and kappa MC (should be ~zero error)
cHLamS = c*c*np.sqrt(LamS/3.0)
ZS = cHLamS/a0S
print(f"  Z_MC = {ZS.mean():.6f} +/- {ZS.std(ddof=1):.2e}  (cosmo error should cancel)")

# ------------------------------------------------------------------
# Step 8: SYSTEMATIC (interpolating function)
# ------------------------------------------------------------------
sys_full_meanref = (a0_RAR - a0_simple)/(0.5*(a0_RAR+a0_simple))
sys_full_RARref  = (a0_RAR - a0_simple)/a0_RAR
sys_full_simpref = (a0_RAR - a0_simple)/a0_simple
print("\n" + "-"*90)
print("SYSTEMATIC (interpolating-function shape)")
print("-"*90)
print(f"  RAR=1.20e-10, simple-mu=9.1e-11")
print(f"  spread/mean   = {sys_full_meanref*100:.2f}%  (half {sys_full_meanref*50:.2f}%)  (claim ~24-31%, half 13.7%)")
print(f"  spread/RAR    = {sys_full_RARref*100:.2f}%")
print(f"  spread/simple = {sys_full_simpref*100:.2f}%")
print(f"  McGaugh's own RAR sys: 0.24/1.20 = {0.24/1.20*100:.1f}%  (claim 20%)")

# ------------------------------------------------------------------
# Step 9: framework vs observed
# ------------------------------------------------------------------
print("\n" + "-"*90)
print("FRAMEWORK a0 vs OBSERVED")
print("-"*90)
print(f"  a0_frame/a0_simple = {a0/a0_simple:.4f}  ({(a0/a0_simple-1)*100:+.2f}%)  (claim +2.8%)")
print(f"  a0_frame/a0_RAR    = {a0/a0_RAR:.4f}  ({(a0/a0_RAR-1)*100:+.2f}%)  (claim -22%)")
sig = rel_stat*a0
print(f"  offset vs simple = {(a0-a0_simple)/sig:+.1f} sigma_stat  (claim +2.8)")
print(f"  offset vs RAR    = {(a0-a0_RAR)/sig:+.1f} sigma_stat  (claim -29)")

# ------------------------------------------------------------------
# Step 10: empirical Z, kappa bands
# ------------------------------------------------------------------
print("\n" + "-"*90)
print("EMPIRICAL Z, kappa bands from observed a0")
print("-"*90)
Z_emp_lo = cH_Lam/a0_RAR     # larger a0 -> smaller Z
Z_emp_hi = cH_Lam/a0_simple
k_emp_lo = a0_simple/(c*sqrt(G*rho_L))
k_emp_hi = a0_RAR/(c*sqrt(G*rho_L))
print(f"  Z empirical: McGaugh {Z_emp_lo:.3f} .. simple-mu {Z_emp_hi:.3f}   (claim band [4.47,6.01])")
print(f"  kappa empirical: simple {k_emp_lo:.4f} .. McGaugh {k_emp_hi:.4f}   (claim [0.482,0.648])")
print(f"  framework Z={Z_analytic:.3f} in [4.2,6.0]? {4.2<=Z_analytic<=6.0}")
print(f"  framework kappa=0.5 in [0.48,0.69]? {0.48<=0.5<=0.69}")

# ------------------------------------------------------------------
# Step 11: a0(z) evolution from DESI CPL
#   rho_DE(a)/rho_DE0 = a^{-3(1+w0+wa)} exp(-3 wa (1-a)),  a0(z)/a0(0)=sqrt(ratio)
# ------------------------------------------------------------------
def rhoDE_ratio(z, W0, WA):
    a = 1.0/(1.0+z)
    return a**(-3.0*(1.0+W0+WA)) * np.exp(-3.0*WA*(1.0-a))

print("\n" + "-"*90)
print("a0(z) EVOLUTION (DESI w0,wa)  -- distinctive prediction")
print("-"*90)
w0S = rng.normal(w0, w0_err, N)
waS = rng.normal(wa, wa_err, N)
for z in [0.5,1.0,2.0,3.0]:
    rc = sqrt(rhoDE_ratio(z, w0, wa))
    rm = np.sqrt(rhoDE_ratio(z, w0S, waS))
    print(f"  z={z}: a0(z)/a0(0) = {rc:.4f} +/- {rm.std(ddof=1):.4f}  ({rm.std(ddof=1)/rc*100:.1f}%)")
z=3.0
rc3 = sqrt(rhoDE_ratio(3.0, w0, wa))
rm3 = np.sqrt(rhoDE_ratio(3.0, w0S, waS))
print(f"\n  z=3 ratio central = {rc3:.4f}   (claim 0.737)")
print(f"  z=3 ratio error   = {rm3.std(ddof=1):.4f}  ({rm3.std(ddof=1)/rc3*100:.1f}%)  (claim 25%, 0.186)")
a0z3 = a0 * rc3
print(f"  absolute a0(z=3)  = {a0z3*1e10:.4f} e-10   (claim 0.689e-10)")
# Note: w0+wa = -0.752-0.86 = -1.612, so 1+w0+wa = -0.612; exponent -3*(-0.612)= +1.836 on a
print(f"  (1+w0+wa) = {1+w0+wa:.4f}; -3(1+w0+wa) = {-3*(1+w0+wa):.4f}")

print("\n" + "="*90)
print("DONE")
print("="*90)
