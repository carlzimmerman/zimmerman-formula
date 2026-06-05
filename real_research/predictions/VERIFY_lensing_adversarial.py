#!/usr/bin/env python3
"""
ADVERSARIAL INDEPENDENT VERIFICATION -- channel: GRAVITATIONAL LENSING.
Recompute every number from scratch. Do NOT reuse the original script's functions.
Check: (a) arithmetic, (b) physics/formula correctness, (c) real-data usage,
(d) error propagation soundness (not understated), (e) overclaims.
"""
import numpy as np

# ============================================================================
# CONSTANTS (mandated)
# ============================================================================
c    = 299792458.0          # m/s exact
G    = 6.67430e-11          # CODATA 2018
Msun = 1.98892e30           # kg
Mpc  = 3.0857e22            # m
rad2arcsec = 180.0 * 3600.0 / np.pi

# Planck 2018
H0     = 67.36              # km/s/Mpc
H0_e   = 0.54
OmL    = 0.6847
OmL_e  = 0.0073
Omm    = 0.3153
Omm_e  = 0.0073

# DESI DR2
w0, w0_e = -0.752, 0.057
wa, wa_e = -0.86,  0.22
corr     = -0.9

# MOND interpolating-function systematic band on a0
a0_simple = 9.1e-11
a0_rar    = 1.20e-10

print("="*100)
print("ADVERSARIAL VERIFICATION: gravitational lensing channel")
print("="*100)

# ============================================================================
# STEP 1: Lambda and framework a0 -- recompute independently
# ============================================================================
H0_si = H0 * 1e3 / Mpc                       # s^-1
Lam   = 3.0 * OmL * H0_si**2 / c**2          # m^-2
a0_fw = c**2 * np.sqrt(Lam / (32.0*np.pi))   # m/s^2

# cross-check the (c/2)sqrt(G rho_Lambda) form: rho_Lambda = Lambda c^2/(8 pi G)
rho_Lam = Lam * c**2 / (8.0*np.pi*G)
a0_alt  = 0.5*c*np.sqrt(G*rho_Lam)

print(f"\n[1] H0_si           = {H0_si:.6e} s^-1")
print(f"    Lambda          = {Lam:.6e} m^-2   (claim 1.089e-52)")
print(f"    a0_framework    = {a0_fw:.6e} m/s^2   (claim 9.3547e-11)")
print(f"    a0 via (c/2)sqrt(G rho_Lam) = {a0_alt:.6e}  (should match -> identity check)")
print(f"    rho_Lambda      = {rho_Lam:.6e} kg/m^3")

# ============================================================================
# STEP 2: statistical error on a0 from OmL, H0.  a0 ~ sqrt(OmL)*H0
#   => dln a0 = 0.5 dln OmL + dln H0  (independent quadrature)
# ============================================================================
rel_OmL = 0.5*OmL_e/OmL
rel_H0  = H0_e/H0
a0_rel  = np.sqrt(rel_OmL**2 + rel_H0**2)
a0_fw_e = a0_fw*a0_rel
print(f"\n[2] rel err from OmL = {rel_OmL*100:.4f}% ; from H0 = {rel_H0*100:.4f}%")
print(f"    a0 stat rel err = {a0_rel*100:.4f}%  -> a0 = ({a0_fw*1e11:.4f} +/- {a0_fw_e*1e11:.4f})e-11")
# verify by numerical partials (perturb OmL, H0)
def a0_of(OmL_v, H0_v):
    H0s = H0_v*1e3/Mpc
    L = 3.0*OmL_v*H0s**2/c**2
    return c**2*np.sqrt(L/(32*np.pi))
dOmL = (a0_of(OmL+1e-6, H0)-a0_of(OmL-1e-6,H0))/(2e-6)
dH0  = (a0_of(OmL, H0+1e-6)-a0_of(OmL,H0-1e-6))/(2e-6)
a0_e_numpartial = np.sqrt((dOmL*OmL_e)**2 + (dH0*H0_e)**2)
print(f"    cross-check numerical partials: a0_e = {a0_e_numpartial*1e11:.4f}e-11  (rel {a0_e_numpartial/a0_fw*100:.4f}%)")

# ============================================================================
# STEP 3: DERIVE the saturated deflection INDEPENDENTLY.
# Physics: weak-field deflection alpha = (2/c^2) * integral g_perp dl along LOS.
# Deep-MOND isolated point mass: g(r) = sqrt(G M a0)/r  (radial).
# g_perp at LOS coordinate l, impact parameter b:  r = sqrt(b^2+l^2),
#   g_perp = g(r) * (b/r) = sqrt(GMa0) * b / (b^2+l^2).
# integral_{-inf}^{inf} b/(b^2+l^2) dl = b * (1/b)[arctan(l/b)]_{-inf}^{inf}
#                                      = arctan(inf)-arctan(-inf) = pi.
# => alpha_inf = (2/c^2) sqrt(GMa0) * pi = 2 pi sqrt(GMa0)/c^2.   b CANCELS.
# ============================================================================
def alpha_inf(M_solar, a0):
    return 2.0*np.pi*np.sqrt(G*M_solar*Msun*a0)/c**2     # radians

# Symbolic check of the integral via scipy.integrate.quad with explicit b:
from scipy.integrate import quad
def los_integral(b):
    val,_ = quad(lambda l: b/(b**2+l**2), -np.inf, np.inf)
    return val
print(f"\n[3] LOS integral int b/(b^2+l^2) dl (should = pi = {np.pi:.6f}):")
for b in (1e15, 1e19, 1e21, 1e23):   # meters, wildly different b
    print(f"      b={b:.0e} m -> integral={los_integral(b):.10f}")

masses = [1e11, 1e13, 1e14]
print(f"\n    alpha_inf(z=0) with framework a0={a0_fw*1e11:.4f}e-11:")
claims_z0 = {1e11:0.5081, 1e13:5.0815, 1e14:16.069}
for M in masses:
    a_arcsec = alpha_inf(M, a0_fw)*rad2arcsec
    print(f"      M={M:.0e}: alpha_inf = {a_arcsec:.4f} arcsec   (claim {claims_z0[M]})")

# ============================================================================
# STEP 4: Numerically confirm b-INDEPENDENCE via a real finite LOS integral,
# using the same scheme the original used (finite range L = f*b).
# ============================================================================
print(f"\n[4] b-independence numeric test (finite range, trapezoid):")
def numeric_alpha(M_solar, a0, b_m, L_over_b=2000.0, npts=2_000_001):
    K = np.sqrt(G*M_solar*Msun*a0)
    L = L_over_b*b_m
    l = np.linspace(-L, L, npts)
    integ = np.trapz(b_m/(b_m**2+l**2), l)
    return (2.0/c**2)*K*integ
Mt = 1e13
analytic = alpha_inf(Mt, a0_fw)*rad2arcsec
ratios=[]
for b_kpc in (0.1,1.0,10.0,100.0,1000.0):
    b_m = b_kpc*Mpc/1000.0          # 1 kpc = Mpc/1000 meters
    num = numeric_alpha(Mt, a0_fw, b_m)*rad2arcsec
    ratios.append(num/analytic)
    print(f"      b={b_kpc:>7.1f} kpc -> num={num:.6f}  ratio={num/analytic:.10f}")
spread=max(ratios)-min(ratios)
# theoretical finite-range deficit: integral over [-L,L] = 2 arctan(L/b)/1 = 2 arctan(L_over_b)
# ratio = 2 arctan(L_over_b)/pi
theo_deficit = 1.0 - 2.0*np.arctan(2000.0)/np.pi
print(f"      spread across b = {spread:.3e} ; common deficit = {(1-np.mean(ratios))*100:.4f}%")
print(f"      predicted finite-range deficit 1-2arctan(2000)/pi = {theo_deficit*100:.4f}%  (should match)")

# ============================================================================
# STEP 5: EVOLUTION ratio.  a0(z) = a0(0) sqrt(rho_DE(z)/rho_DE0).
#   alpha ~ sqrt(a0) => alpha(z)/alpha(0) = sqrt(a0(z)/a0(0))
#                     = (rho_DE ratio)^(1/4).   CHECK exponent.
# ============================================================================
def rhoDE_ratio(z, w0_, wa_):
    a = 1.0/(1.0+z)
    return a**(-3.0*(1.0+w0_+wa_))*np.exp(-3.0*wa_*(1.0-a))
def amp_ratio(z, w0_, wa_):
    return rhoDE_ratio(z, w0_, wa_)**0.25

zs=[0.4,1.0,2.0,3.0]
claim_amp={0.4:1.0303,1.0:1.0044,2.0:0.9284,3.0:0.8585}
print(f"\n[5] amplitude ratio alpha(z)/alpha(0) = (rho_DE(z)/rho_DE0)^(1/4):")
for z in zs:
    rr=rhoDE_ratio(z,w0,wa)
    amp=rr**0.25
    print(f"      z={z}: rho_DE ratio={rr:.5f}  amp={amp:.5f}  (claim {claim_amp[z]})")

# ============================================================================
# STEP 6: Monte Carlo on (w0,wa) correlated, 200k draws, recompute sigmas/CIs.
# ============================================================================
print(f"\n[6] Monte Carlo evolution error (200k draws, corr={corr}):")
rng=np.random.default_rng(12345)   # different seed than original on purpose
N=200000
cov=np.array([[w0_e**2, corr*w0_e*wa_e],[corr*w0_e*wa_e, wa_e**2]])
draws=rng.multivariate_normal([w0,wa],cov,size=N)
W0s,WAs=draws[:,0],draws[:,1]
claim_sigma={0.4:0.0080,1.0:0.0140,2.0:0.0330,3.0:0.0497}
for z in zs:
    mc=rhoDE_ratio(z,W0s,WAs)**0.25
    lo,hi=np.percentile(mc,[16,84])
    print(f"      z={z}: sigma={mc.std():.4f} (claim {claim_sigma[z]})  68%CI[{lo:.4f},{hi:.4f}]  median={np.median(mc):.4f}")

# z=3 CI claim [0.8105,0.9092]
mc3=rhoDE_ratio(3.0,W0s,WAs)**0.25
print(f"      z=3 68%CI = [{np.percentile(mc3,16):.4f},{np.percentile(mc3,84):.4f}]  (claim [0.8105,0.9092])")

# Peak location
zgrid=np.linspace(0.0,1.5,3001)
amp_c=rhoDE_ratio(zgrid,w0,wa)**0.25
ipk=np.argmax(amp_c)
zpk=zgrid[ipk]; amppk=amp_c[ipk]
print(f"\n    peak (central): z_peak={zpk:.3f}  amp={amppk:.4f}  boost={(amppk-1)*100:+.2f}%  (claim z~0.41, +3%)")
# MC the peak
zpk_mc=np.empty(20000)
for i in range(20000):
    g=rhoDE_ratio(zgrid,W0s[i],WAs[i])
    zpk_mc[i]=zgrid[np.argmax(g)]
print(f"    z_peak MC 68%CI = [{np.percentile(zpk_mc,16):.3f},{np.percentile(zpk_mc,84):.3f}]  (claim [0.35,0.48])")
print(f"    fraction MC with interior peak (z>0) = {100*np.mean(zpk_mc>1e-6):.1f}%  (claim 100%)")

# ============================================================================
# STEP 7: Absolute alpha error budget at z=0 for 1e13.
#   stat (alpha) = 0.5 * a0_rel
#   syst (alpha) = 0.5 * (halfspan/mid) of a0 band, mapped onto alpha.
# Check the claim: stat +/-0.48%, syst +/-6.9%, alpha(1e13,z=0)=5.0815 +/-0.0245 +/-0.3492
# ============================================================================
stat_rel_alpha = 0.5*a0_rel
a0_mid = 0.5*(a0_simple+a0_rar)
a0_half = 0.5*(a0_rar-a0_simple)
sys_rel_alpha_mid = 0.5*(a0_half/a0_mid)   # half-span on alpha about midpoint
print(f"\n[7] absolute alpha error budget (1e13, z=0):")
a13 = alpha_inf(1e13,a0_fw)*rad2arcsec
e_stat=a13*stat_rel_alpha
e_sys =a13*sys_rel_alpha_mid
print(f"    stat rel(alpha)={stat_rel_alpha*100:.4f}%  (claim 0.48%) -> {e_stat:.4f}\"  (claim 0.0245)")
print(f"    syst rel(alpha)={sys_rel_alpha_mid*100:.4f}%  (claim 6.9%) -> {e_sys:.4f}\"  (claim 0.3492)")
print(f"    => alpha(1e13,z=0) = {a13:.4f} +/- {e_stat:.4f}(stat) +/- {e_sys:.4f}(syst)")

# alternative systematic mapping: alpha at framework a0 vs alpha at the two band ends
a13_lo = alpha_inf(1e13,a0_simple)*rad2arcsec
a13_hi = alpha_inf(1e13,a0_rar)*rad2arcsec
print(f"    alpha-band ends: simple-mu a0=9.1 -> {a13_lo:.4f}\" ; RAR a0=12 -> {a13_hi:.4f}\" ; framework -> {a13:.4f}\"")
print(f"    framework sits at fractional position { (a13-a13_lo)/(a13_hi-a13_lo)*100:.1f}% of the band")
print(f"    full alpha band half-span about its own midpoint = {0.5*(a13_hi-a13_lo)/(0.5*(a13_hi+a13_lo))*100:.2f}%")
print(f"    framework a0 is {(a0_fw-a0_rar)/a0_rar*100:.1f}% relative to McGaugh RAR anchor (claim ~-28%)")

# ============================================================================
# STEP 8: worked deliverable alpha(z=0.4 peak, 1e13)
# ============================================================================
a0_z04 = a0_fw*np.sqrt(rhoDE_ratio(0.4,w0,wa))
a_z04  = alpha_inf(1e13, a0_z04)*rad2arcsec
print(f"\n[8] alpha(z=0.4, 1e13) = {a_z04:.4f} arcsec  (claim 5.235)")
print(f"    a0(z=0.4) = {a0_z04*1e11:.4f}e-11")
# also using exact peak z
a0_zpk = a0_fw*np.sqrt(rhoDE_ratio(zpk,w0,wa))
a_zpk = alpha_inf(1e13,a0_zpk)*rad2arcsec
print(f"    at true peak z={zpk:.3f}: alpha={a_zpk:.4f}")

# ============================================================================
# STEP 9: which error dominates (absolute alpha)?
# ============================================================================
print(f"\n[9] dominance check (absolute alpha): stat={stat_rel_alpha*100:.3f}% syst={sys_rel_alpha_mid*100:.3f}% "
      f"ratio syst/stat = {sys_rel_alpha_mid/stat_rel_alpha:.1f}x")
print(f"    => systematic dominates absolute alpha (claim ~9x). For the RATIO the systematic cancels exactly,")
print(f"       so DESI w0/wa statistical is the only error there (grows 0.8% -> ~5% from z=0.4 to z=3).")

print("\n"+"="*100)
print("END VERIFICATION")
print("="*100)
