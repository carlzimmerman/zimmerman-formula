#!/usr/bin/env python3
"""
INDEPENDENT adversarial verification of channel 'highz-btfr'.
Recomputes everything from scratch with my own physics derivation, a DIFFERENT seed,
a DIFFERENT MC size, and an ANALYTIC (partial-derivative) cross-check of the error bars.
Nothing is reused from btfr_offset_ultra.py.
"""
import os
import numpy as np

# ---- constants (mandated) ----
C    = 299792458.0
G    = 6.67430e-11
MSUN = 1.98892e30
MPC  = 3.0857e22

# Planck 2018
H0_C, H0_E   = 67.36, 0.54
OML_C, OML_E = 0.6847, 0.0073
OMM_C, OMM_E = 0.3153, 0.0073
# DESI DR2
W0_C, W0_E = -0.752, 0.057
WA_C, WA_E = -0.86, 0.22
# mu systematic band
A0_SIMPLE, A0_RAR = 9.1e-11, 1.2e-10

ZGRID = [1.0, 2.0, 3.0, 4.0, 6.0]

# =====================================================================
# 1. ABSOLUTE ANCHOR  a0(0) = c^2 sqrt(Lambda/32pi), Lambda = 3 OmL H0^2/c^2
#    Independent algebra: a0 = c^2 * sqrt(3 OmL H0^2 / (32 pi c^2))
#                            = sqrt(3 OmL c^2 H0^2 / (32 pi))
#                            = c H0 sqrt(3 OmL / (32 pi))
#    Cross-check the (c/2) sqrt(G rho_Lambda) identity:
#      rho_Lambda = Lambda c^2/(8 pi G) = 3 OmL H0^2/(8 pi G)
#      (c/2) sqrt(G rho_Lambda) = (c/2) sqrt(3 OmL H0^2/(8 pi)) = c H0 sqrt(3 OmL/(32 pi)). identical. OK
# =====================================================================
def a0_anchor(omL, H0_kms):
    H0 = H0_kms * 1e3 / MPC          # s^-1
    return C * H0 * np.sqrt(3.0 * omL / (32.0 * np.pi))

a0_c = a0_anchor(OML_C, H0_C)
# independent route via Lambda explicitly
H0_si = H0_C * 1e3 / MPC
Lam = 3.0 * OML_C * H0_si**2 / C**2
a0_route2 = C**2 * np.sqrt(Lam / (32.0*np.pi))
# independent route via (c/2) sqrt(G rho_Lambda)
rho_Lam = Lam * C**2 / (8.0*np.pi*G)
a0_route3 = (C/2.0)*np.sqrt(G*rho_Lam)

print("="*78)
print("ANCHOR a0(0):")
print(f"  route1 c*H0*sqrt(3 OmL/32pi) = {a0_c:.6e}")
print(f"  route2 c^2 sqrt(Lambda/32pi) = {a0_route2:.6e}")
print(f"  route3 (c/2) sqrt(G rho_Lam) = {a0_route3:.6e}")
print(f"  claimed central 9.355e-11; reproduced {a0_c:.4e}")
print(f"  vs simple-mu {A0_SIMPLE:.2e}: {100*(a0_c-A0_SIMPLE)/A0_SIMPLE:+.1f}% ; "
      f"vs RAR {A0_RAR:.2e}: {100*(a0_c-A0_RAR)/A0_RAR:+.1f}%")

# =====================================================================
# 2. CORE PHYSICS  -- derive the offset independently.
#    BTFR: V_flat^4 = G M_bar a0   (deep-MOND).  At FIXED M_bar:
#      4 dlogV = dlog a0  => dlogV = (1/4) dlog10(a0)
#    a0(z) = a0(0) sqrt(rho_DE(z)/rho_DE0)  => dlog10 a0 = (1/2) log10(rho_DE ratio)
#    => dlogV(z) = (1/8) log10(rho_DE(z)/rho_DE0).  Matches claim.
#    CPL: rho_DE(a)/rho0 = a^{-3(1+w0+wa)} * exp(-3 wa (1-a)), a=1/(1+z).
# =====================================================================
def rho_ratio(z, w0, wa):
    a = 1.0/(1.0+z)
    return a**(-3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*(1.0-a))

def dlogV(z, w0, wa):
    return (1.0/8.0)*np.log10(rho_ratio(z, w0, wa))

# closed-form check of log10(rho_ratio):
# ln(rho_ratio) = -3(1+w0+wa) ln a - 3 wa (1-a)
# with a=1/(1+z): ln a = -ln(1+z), (1-a)= z/(1+z)
# => ln(rho_ratio) = 3(1+w0+wa) ln(1+z) - 3 wa z/(1+z)
def ln_rho_closed(z, w0, wa):
    return 3.0*(1.0+w0+wa)*np.log(1.0+z) - 3.0*wa*z/(1.0+z)

print("\n" + "="*78)
print("CENTRAL VALUES (independent), with closed-form ln(rho_ratio) cross-check:")
print(f"  {'z':>4}{'rho_ratio':>12}{'ln_closed-ln_direct':>22}{'dlogV[dex]':>14}{'dV[%]':>12}")
central = {}
for z in ZGRID:
    r = rho_ratio(z, W0_C, WA_C)
    chk = ln_rho_closed(z, W0_C, WA_C) - np.log(r)
    d = dlogV(z, W0_C, WA_C)
    dv = 100*(10**d - 1)
    central[z] = (r, d, dv)
    print(f"  {z:>4.0f}{r:>12.4f}{chk:>22.2e}{d:>14.4f}{dv:>12.2f}")

# =====================================================================
# 3. ERROR PROPAGATION
#    (a) Monte Carlo, independent seed + size.
#    (b) ANALYTIC partials cross-check:
#        dlogV = (1/(8 ln10)) * ln_rho ;  ln_rho = 3(1+w0+wa)L - 3 wa z/(1+z), L=ln(1+z)
#        d ln_rho/dw0 = 3 L
#        d ln_rho/dwa = 3 L - 3 z/(1+z) = 3[L - z/(1+z)]
#        sigma_dlogV^2 = (1/(8 ln10))^2 [ (3L)^2 sw0^2 + (3(L - z/(1+z)))^2 swa^2 ]
#    Verify the claim that OmL,H0,mu CANCEL: dlogV has no OmL/H0/mu dependence at all -> trivially exact.
# =====================================================================
LN10 = np.log(10.0)
rng = np.random.default_rng(777)          # DIFFERENT seed
NMC = 2_000_000                            # DIFFERENT (larger) size
w0s = rng.normal(W0_C, W0_E, NMC)
was = rng.normal(WA_C, WA_E, NMC)

print("\n" + "="*78)
print("ERROR BARS: Monte Carlo (seed=777, N=2e6) vs ANALYTIC partials")
print(f"  {'z':>4}{'MC sig_dlogV':>14}{'analytic':>12}{'MC sig_dV%':>14}{'claim sig_dV%':>14}{'claim sig_dex':>14}")
claim_dlv_sd = {1.0:0.0094, 2.0:0.0184, 3.0:0.0260, 4.0:0.0324, 6.0:0.0427}
claim_dv_sd  = {1.0:2.17,   2.0:4.09,   3.0:5.56,   4.0:6.69,   6.0:8.32}
err_check = {}
for z in ZGRID:
    L = np.log(1.0+z); zr = z/(1.0+z)
    s_an = (1.0/(8.0*LN10))*np.sqrt((3*L)**2*W0_E**2 + (3*(L-zr))**2*WA_E**2)
    dlv_s = dlogV(z, w0s, was)
    lo, hi = np.percentile(dlv_s, [16, 84])
    s_mc = 0.5*(hi-lo)
    dv_s = 100*(10**dlv_s - 1)
    dvlo, dvhi = np.percentile(dv_s, [16, 84])
    s_dv = 0.5*(dvhi-dvlo)
    err_check[z] = (s_mc, s_an, s_dv)
    print(f"  {z:>4.0f}{s_mc:>14.5f}{s_an:>12.5f}{s_dv:>14.3f}{claim_dv_sd[z]:>14.2f}{claim_dlv_sd[z]:>14.4f}")

# =====================================================================
# 4. ERROR DECOMPOSITION (w0-only, wa-only) -- check the 'wa dominates' claim
# =====================================================================
print("\n" + "="*78)
print("DECOMPOSITION (analytic): sigma_w0, sigma_wa, joint (dex). Check wa dominates.")
print(f"  {'z':>4}{'sig_w0':>12}{'sig_wa':>12}{'joint':>12}{'dominant':>10}")
for z in ZGRID:
    L = np.log(1.0+z); zr = z/(1.0+z)
    s_w0 = (1.0/(8.0*LN10))*abs(3*L)*W0_E
    s_wa = (1.0/(8.0*LN10))*abs(3*(L-zr))*WA_E
    s_jt = np.hypot(s_w0, s_wa)
    print(f"  {z:>4.0f}{s_w0:>12.5f}{s_wa:>12.5f}{s_jt:>12.5f}{('wa' if s_wa>s_w0 else 'w0'):>10}")

# =====================================================================
# 5. SIGN-CONTRAST claim: rising reading dlogV_tot = (1/4) log10 E(z) > 0 (opposite sign)
# =====================================================================
def Ez(z, omL, omM, w0, wa):
    return np.sqrt(omM*(1+z)**3 + omL*rho_ratio(z, w0, wa))
print("\n" + "="*78)
print("SIGN CONTRAST: framework dV vs rising-reading dV_tot=(1/4)log10 E(z)")
print(f"  {'z':>4}{'dV_DE%':>10}{'dV_tot%':>10}{'split%':>10}")
for z in ZGRID:
    dde = 100*(10**dlogV(z, W0_C, WA_C)-1)
    dto = 100*(10**(0.25*np.log10(Ez(z,OML_C,OMM_C,W0_C,WA_C)))-1)
    print(f"  {z:>4.0f}{dde:>10.2f}{dto:>10.2f}{dto-dde:>10.2f}")

# =====================================================================
# 6. HONEST SIGN SUBTLETY: where does rho_DE peak / cross 1?  (claim: peak z~0.405, cross z~1.06)
# =====================================================================
from scipy.optimize import brentq
zz = np.linspace(0, 3, 60001)
rr = rho_ratio(zz, W0_C, WA_C)
ipk = np.argmax(rr)
zpk = zz[ipk]
# crossing rho_ratio=1 for z>0:
f = lambda z: rho_ratio(z, W0_C, WA_C) - 1.0
zc = brentq(f, 0.5, 2.0)
print("\n" + "="*78)
print("SIGN SUBTLETY (DESI thawing): rho_DE peaks then crosses back below 1")
print(f"  peak at z = {zpk:.3f}, rho_ratio_peak = {rr[ipk]:.4f} ({100*(rr[ipk]-1):+.1f}% above today)")
print(f"  crosses rho_ratio=1 at z = {zc:.3f}  (claim peak~0.405, cross~1.06)")
print(f"  dV at z=0.4: {100*(10**dlogV(0.4,W0_C,WA_C)-1):+.2f}%  (claim +0.65%)")

# =====================================================================
# 7. REAL DATA: independently load + median z; compute measurability N(3sigma)
# =====================================================================
path = os.path.join(os.path.dirname(__file__), "..", "data", "kmos3d_ubler2017.csv")
arr = np.genfromtxt(path, delimiter=",", names=True)
zd = arr["z"]; logMb = arr["logMbar"]; V = arr["Vcirc_kms"]
good = np.isfinite(zd) & np.isfinite(logMb) & np.isfinite(V) & (V>0)
zd, logMb, V = zd[good], logMb[good], V[good]
print("\n" + "="*78)
print(f"REAL DATA: {len(zd)} disks, z=[{zd.min():.2f},{zd.max():.2f}], median z={np.median(zd):.2f}")
SIG_GAL = 0.05
for z in (1.4, 3.0, 6.0):
    s = abs(dlogV(z, W0_C, WA_C))
    N3 = (3*SIG_GAL/s)**2
    print(f"  z={z}: |dlogV|={s:.4f} dex, N(3sigma mean)={N3:.0f}")
print("  (claim: ~730 @z=1.4, ~21 @z=3, ~4 @z=6)")

# =====================================================================
# 8. signal-to-statistical-error at z=3 (claim: stat err ~75% of signal)
# =====================================================================
print("\n" + "="*78)
z=3.0
sig = abs(central[z][2])
err = err_check[z][2]
print(f"z=3 SIGNAL/STAT check: |dV|={sig:.2f}%, stat sigma={err:.2f}%, ratio sigma/signal={err/sig:.2f}")
print(f"  (claim: statistical error ~75% of central signal at z=3)")
