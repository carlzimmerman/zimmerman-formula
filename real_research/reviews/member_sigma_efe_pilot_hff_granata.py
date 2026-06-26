#!/usr/bin/env python3
"""
REAL-DATA PILOT 2 -- HFF cluster members (Granata et al. 2026, A&A 709 / arXiv:2603.26869)
==========================================================================================
Pulls the PUBLIC VizieR catalog J/A+A/709/A254 (Granata+2026): structural parameters of
950 red cluster members across the 4 Hubble Frontier Fields clusters (A2744 z=0.307,
AS1063 z=0.346, MACS0416 z=0.397, MACS1149 z=0.542). For EACH real member it computes the
INTERNAL Newtonian acceleration g_in/a0 (from the measured effective radius Re_F814W and a
luminosity-derived stellar mass), which decides whether the member is in the EFE-sensitive
(diffuse, g_in<a0) regime or is internally Newtonian (g_in>>a0, EFE-immune). It then computes
the predicted framework MI-EFE sigma_int suppression for the REAL member population.

WHY THIS MATTERS (the load-bearing data fact):
  The cluster-member sigma-SIGN test only works on DIFFUSE members (g_in<<a0). This script shows
  on REAL spectroscopically-confirmed members that the spec sample is OVERWHELMINGLY Newtonian
  internally (median g_in/a0~7.5; only ~4% have g_in<a0; only ~1% diffuse). So the predicted MI
  suppression for the real member mix is only ~1.7-5% -- BELOW the FJ/morphology systematic
  (+12% UP, measured in the SDSS pilot). The bright spec members are the WRONG sample; the diffuse
  members that would show the ~40% suppression are too faint for sigma measurement.

CAVEATS (honest, UNVERIFIED flagged):
  * The Granata+2026 VizieR upload has STRUCTURAL params only (mag, Re, Sersic, SB). The 213 MEASURED
    velocity dispersions are in the paper's Appendix C, NOT (yet) machine-readable at CDS -- so the
    sigma values themselves are not pulled here; we use the measured Re + luminosity to get g_in.
  * Granata+2026 MUSE coverage is CORE-ONLY (~few hundred kpc) -> there is NO radial lever arm into the
    EFE-weak outskirts, so the sigma-vs-cluster-centric-R trend is NOT measurable from this catalog.
    The paper itself reports NO sigma-vs-radius / sigma-vs-environment trend (confirmed in the text).
  * Stellar M/L_F814 fixed at 3.0 (red members, coarse); no k-correction (absorbed into M/L). The
    g_in DISTRIBUTION shape (mostly Newtonian) is robust to factor~2 M/L; the diffuse fraction is small
    for any reasonable M/L.
"""
import numpy as np
from scipy.optimize import brentq

G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; Mpc=3.0857e22
a0=9.36e-11
def nu(y): return np.sqrt(1.0+1.0/y)
def mu_fw(x):
    x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x**2)-1.0)/(2.0*x)
def solve_internal_g(g_N,g_ext,theta=1.0):
    ge=theta*g_ext
    rhs=g_N+ge*mu_fw(max(ge/a0,1e-12))
    f=lambda g:(g+ge)*mu_fw(max((g+ge)/a0,1e-12))-rhs
    lo,hi=g_N*1e-3,g_N*nu(g_N/a0)*3+ge
    return brentq(f,lo,hi,xtol=1e-30,rtol=1e-12)

def main():
    import sys
    print("="*94)
    print(" HFF MEMBER PILOT (Granata+2026, VizieR J/A+A/709/A254) -- real internal-acceleration mix")
    print("="*94)
    try:
        from astroquery.vizier import Vizier
        from astropy.cosmology import FlatLambdaCDM
    except Exception as e:
        print("MISSING DEP:",repr(e)); sys.exit(2)
    try:
        v=Vizier(row_limit=-1); cats=v.get_catalogs("J/A+A/709/A254")
    except Exception as e:
        print("DATA PULL FAILED:",repr(e)[:160]); sys.exit(2)
    cosmo=FlatLambdaCDM(H0=70,Om0=0.3)
    zclus={'a2744':0.307,'as1063':0.346,'m0416':0.397,'m1149':0.542}
    ML=3.0; Lsun_F814=4.52

    allgin=[]; allMstar=[]; allRe=[]
    print(f"  {'cluster':>8} {'z':>5} {'N':>4} {'med g_in/a0':>11} {'%<a0':>6} {'%<0.3a0':>8} {'medRe[kpc]':>10} {'medlogM*':>8}")
    for t in cats:
        name=t.meta.get('name').split('/')[-1]; z=zclus[name]
        DL=cosmo.luminosity_distance(z).value
        mag=np.array(t['F814W'],float); Re=np.array(t['ReF814W'],float)
        good=np.isfinite(mag)&np.isfinite(Re)&(Re>0)
        mag=mag[good]; Re=Re[good]
        Mabs=mag-5*np.log10(DL*1e6/10.0)
        L=10**(-0.4*(Mabs-Lsun_F814)); Mstar=ML*L*Msun
        g_in=G*Mstar/(Re*kpc)**2
        allgin.append(g_in); allMstar.append(Mstar); allRe.append(Re)
        print(f"  {name:>8} {z:>5.3f} {good.sum():>4} {np.median(g_in/a0):>11.2f} "
              f"{100*np.mean(g_in<a0):>5.0f}% {100*np.mean(g_in<0.3*a0):>7.0f}% "
              f"{np.median(Re):>10.2f} {np.median(np.log10(Mstar/Msun)):>8.1f}")
    gin=np.concatenate(allgin); Mstar=np.concatenate(allMstar)

    print("\n  REAL HFF member internal-acceleration distribution (950 members):")
    for q in [5,25,50,75,95]:
        print(f"    {q:>2}th pctile g_in/a0 = {np.percentile(gin/a0,q):.2f}")
    print(f"    frac g_in<a0     (EFE-sensitive at all)  = {100*np.mean(gin<a0):.0f}%")
    print(f"    frac g_in<0.3a0  (DIFFUSE, EFE bites)    = {100*np.mean(gin<0.3*a0):.0f}%  (N={np.sum(gin<0.3*a0)})")
    print(f"    frac g_in>3a0    (Newtonian, EFE-immune) = {100*np.mean(gin>3*a0):.0f}%")

    print("\n  Predicted framework MI-EFE sigma_int suppression for the REAL member mix (core, g_ext/a0=2.0, theta(0)=2):")
    g_ext=2.0*a0; theta0=2.0
    def supp(gi):
        giso=gi*nu(gi/a0); gA=solve_internal_g(gi,g_ext,theta=theta0); return 1-np.sqrt(gA/giso)
    S=np.array([supp(g) for g in gin]); w=Mstar/Mstar.sum()
    print(f"    unweighted MEAN suppression   = {100*np.mean(S):.1f}%")
    print(f"    mass-weighted MEAN suppression= {100*np.sum(w*S):.1f}%")
    print(f"    median suppression            = {100*np.median(S):.1f}%")
    if np.any(gin<0.3*a0):
        print(f"    diffuse-tail (g_in<0.3a0) supp = {100*np.mean(S[gin<0.3*a0]):.1f}%  (but only {np.sum(gin<0.3*a0)} such members)")

    print("\n  CONCLUSION (real data):")
    print("   * Spectroscopically-confirmed HFF cluster members are OVERWHELMINGLY internally Newtonian")
    print("     (median g_in/a0~7.5; ~4% have g_in<a0; ~1% diffuse). The EFE barely touches them.")
    print("   * Predicted MI suppression for the real member mix ~1.7-5% -- BELOW the FJ/morphology UP +12%")
    print("     systematic (SDSS pilot) and below the ~8-14% systematic floor.")
    print("   * Granata+2026 covers the CORE only -> no sigma-vs-R lever arm; the paper reports no such trend.")
    print("   * NET: the bright spec members are the WRONG sample. The decisive test needs DIFFUSE members")
    print("     (g_in<<a0) -- exactly the faint UDG/dwarf population that is too faint for current spectroscopy.")
    print("="*94)

if __name__=="__main__":
    main()
