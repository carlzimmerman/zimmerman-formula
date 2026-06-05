#!/usr/bin/env python3
"""
NEW (conditional) PREDICTION, COMPUTED: everpresent-Lambda (Das-Nasiri-Yazdi 2024, arXiv:2304.03819)
-> a definite, falsifiable a0(z) law and a0-vs-distance trend, via the framework a0 = c^2 sqrt(Lambda/32pi).

CONTEXT / honesty: the repo previously logged the everpresent-Lambda SIGN FLIP (<Lambda>=0, Lambda
fluctuates +/- ~H^2, flips sign ~every Hubble time) purely as an OBSTRUCTION: a0 ~ sqrt(Lambda) is
imaginary for Lambda<0. That no-go stands and is the honest headline: a literal marriage of the two is
forbidden. This script extracts the only CONSTRUCTIVE residue: CONDITIONED on the positive-Lambda epoch
we observe, the model's own quantified amplitude/inhomogeneity (eqs 3.6-3.12: |Lambda(x)| ~ alpha/sqrt(V(x)),
V(x)=past-lightcone 4-volume) makes a SHARP prediction for how a0 should vary with redshift and distance.
That prediction is COMPUTED here and compared to the framework's other a0(z) readings and to the RAR data.

PRIMARY SOURCES (quoted):
  * Das, Nasiri, Yazdi 2024 (arXiv:2304.03819): dLambda = 4pi (l_p/l_cs)^2 / sqrt(V) (eq 3.6);
    delta-Lambda ~ H^2 (eq 3.7); <Lambda>=0; Lambda(x) per past-lightcone volume V(x) (eq 3.12);
    sign flips ~ every Hubble time.
  * Framework: a0 = (c^2/sqrt(32pi)) sqrt(Lambda)  =>  a0 prop sqrt(Lambda)  =>  da0/a0 = (1/2) dLambda/Lambda.
  * Li, Lelli, McGaugh 2018 (arXiv:1803.00022): "no credible indication of variation in the critical
    acceleration scale"; intrinsic scatter ~0.057 dex, NO trend with any galaxy property.

RESULT (verified):
  (1) Conditioned on Lambda>0, the a0 magnitude envelope is a0(z) = a0(0) (V0/V(z))^(1/4) -- a FOURTH,
      distinct a0(z) law, the STEEPEST riser: 2.3x / 4.1x / 6.2x at z=1/2/3 (vs cH(z)=E(z): 1.8/3.0/4.6;
      vs const-Lambda null: 1.0; vs DESI-falling: 1.01/0.86/0.74). Low-z slope ~1.0 dex per decade in (1+z).
  (2) Over SPARC's distance range (3-130 Mpc) this is a MONOTONIC ~0.012 dex trend with distance -- below
      today's 0.057 dex bound (so not yet excluded) BUT a TREND, which the data say is absent. So:
      everpresent-Lambda is DISFAVORED-but-alive at low z, and SHARPLY testable at the z~1-3 BTFR frontier.
  (3) Plus a second signature: zero-mean sign-flipping Lambda => a fraction of high-z galaxies should show
      Lambda<0 = NO MOND (wrong sign). The observed RAR is universal and one-signed -> further disfavors it.

Needs numpy.
"""
import numpy as np

c, Mpc = 2.99792458e8, 3.0857e22
H0 = 67.4e3/Mpc
Om, OmL = 0.315, 0.685
Lam0 = 3*OmL*H0**2/c**2

def E(z): return np.sqrt(Om*(1+z)**3 + OmL)

def lc_vol(z_obs, N=400000):
    """Past-lightcone proper 4-volume of a comoving observer at redshift z_obs (LCDM).
    dV4 = (4pi/3) a^4 r_com^3 d(eta);  validated: chi(0)=14.4 Gpc, matches the particle horizon."""
    a_obs = 1.0/(1.0+z_obs)
    a = np.linspace(1e-7, a_obs, N); zg = 1.0/a - 1.0
    integ = 1.0/(a**2 * H0 * E(zg))
    eta = np.concatenate([[0], np.cumsum((integ[1:]+integ[:-1])/2*np.diff(a))])
    r = c*(eta[-1]-eta)
    return np.trapz((4*np.pi/3.0)*a**4*r**3, eta)

def main():
    print("#"*94)
    print("# Everpresent-Lambda -> a0(z): a conditional, computed, falsifiable prediction")
    print("#"*94)
    a0_fw = c**2*np.sqrt(Lam0/(32*np.pi))
    print(f"  Lambda_0={Lam0:.3e} m^-2;  a0(framework floor)={a0_fw:.3e} m/s^2 (repo 9.36e-11).\n")

    print("="*94); print("(1) THE NO-GO (honest headline): sign flip forbids a literal marriage"); print("="*94)
    print("  DNY: <Lambda>=0, Lambda=+/-dLambda~H^2, sign flips ~every Hubble time. a0~sqrt(Lambda) is")
    print("  imaginary for Lambda<0 -> the two cannot both be fundamental. CONFLICT stands.\n")

    print("="*94); print("(2) THE CONSTRUCTIVE RESIDUE: conditioned on Lambda>0, a definite a0(z) law"); print("="*94)
    V0 = lc_vol(0.0)
    print(f"  {'z':>5}{'EP-L (V0/Vz)^1/4':>18}{'cH(z)=E(z)':>13}{'const null':>12}{'EP-L/E(z)':>12}")
    for z in (0.0,0.5,1.0,2.0,3.0,4.0,6.0):
        epl=(V0/lc_vol(z))**0.25
        print(f"  {z:>5.1f}{epl:>18.4f}{E(z):>13.4f}{1.0:>12.4f}{epl/E(z):>12.4f}")
    zt=np.array([0.005,0.01,0.02,0.04]); rt=np.array([(V0/lc_vol(z))**0.25 for z in zt])
    slope=np.polyfit(np.log10(1+zt),np.log10(rt),1)[0]
    print(f"  low-z slope d(log10 a0)/d(log10(1+z)) = {slope:.3f} dex/decade. DISTINCT, steepest riser.\n")

    print("="*94); print("(3) THE LOW-z TEST: a0-vs-distance trend across SPARC vs the 0.057 dex bound"); print("="*94)
    d_Mpc=np.array([3.,10.,30.,50.,80.,130.]); zr=H0*(d_Mpc*Mpc)/c
    rr=np.array([(V0/lc_vol(z))**0.25 for z in zr])
    print(f"  {'d[Mpc]':>8}{'z':>9}{'a0/a0(0)':>11}{'dex':>9}")
    for d,z,r in zip(d_Mpc,zr,rr): print(f"  {d:>8.0f}{z:>9.5f}{r:>11.5f}{np.log10(r):>9.4f}")
    print(f"  predicted spread over SPARC = {np.log10(rr.max()/rr.min()):.4f} dex (a TREND with distance).")
    print(f"  observed: ~0.057 dex scatter, NO trend ('single effective force law', Li-Lelli-McGaugh 2018).")
    print(f"  => survives in amplitude today, but the predicted TREND is the falsifier: FLAT (const-Lambda)")
    print(f"     vs RISING ~{slope:.1f} dex/decade (everpresent-Lambda). Decisive at z~1-3 (2.3x-6.2x).")
    print("#"*94)

if __name__ == "__main__":
    main()
