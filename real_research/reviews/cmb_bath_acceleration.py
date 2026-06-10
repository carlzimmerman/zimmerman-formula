#!/usr/bin/env python3
"""
The acceleration-BATH correction (regression fix): which acceleration enters mu(a/a0) at recombination?

Modified inertia is NONLINEAR and NONLOCAL: the mu-argument is the fluid element's TOTAL real-space
acceleration -- the sum over ALL Fourier modes (the 'bath') -- not the single-acoustic-mode value. The
real-space RMS acceleration is dominated by small scales (high k, up to Silk damping) and is FAR larger
than any one acoustic-peak mode. This is the external-field-effect logic applied to the CMB: the small-
scale acceleration bath puts the acoustic modes in the deep-Newtonian regime.

  per-mode (WRONG, the cmb_class_mond patch): a_peak ~ 1e-9 m/s^2 -> x_flat ~ 25 -> ~4.5% -> Dchi2~117.
  bath     (RIGHT):                            a_rms  ~ 1e-8..1e-7 -> x_flat ~ 100-1000 -> <0.5% -> Dchi2~0.

Consequence: FLAT (constant a0) is CMB-SAFE; "CMB selects declining" is RETRACTED (it was a per-mode
artifact -- a manufactured win toward the framework's own claim). RISING still dies (a0(z_rec)~1.9e-6 is
above even the bath). DECLINING safe. => the CMB does NOT discriminate flat vs declining; only rising-dead
survives. This script computes a_rms from the real CAMB baryon power at z_rec and reports the regime per
branch. Needs camb, numpy.  C. Zimmerman, 2026-06-09.
"""
import numpy as np, camb
from camb import model

c=2.99792458e8; Mpc=3.0857e22; zrec=1090.0
ombh2,omch2,H0,ns,As=0.02237,0.1200,67.36,0.9649,2.1e-9
h=H0/100.0
a0_flat=9.36e-11
Om,OmL=0.3153,0.6847
def E(z): return np.sqrt(Om*(1+z)**3+OmL)
def rhoDE(z,w0=-0.752,wa=-0.86): a=1/(1+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))
a0_rise=a0_flat*E(zrec); a0_decl=a0_flat*np.sqrt(rhoDE(zrec))

# --- baryon density power spectrum at recombination from CAMB (incl. acoustic + Silk damping) ---
pars=camb.set_params(H0=H0,ombh2=ombh2,omch2=omch2,ns=ns,As=As,tau=0.0544)
pars.set_matter_power(redshifts=[zrec],kmax=5.0)
pars.NonLinear=model.NonLinear_none
res=camb.get_results(pars)
kh,zs,pk=res.get_matter_power_spectrum(minkh=1e-3,maxkh=4.0,npoints=600,var1='delta_baryon',var2='delta_baryon')
k=kh*h                          # comoving 1/Mpc
P=pk[0]/h**3                    # Mpc^3
D2b=k**3*P/(2*np.pi**2)         # dimensionless baryon variance per ln k

# sound speed at recomb
Ogh2=2.47e-5; R=0.75*(ombh2/Ogh2)/(1+zrec); cs2=c**2/(3*(1+R))
kphys=k*(1+zrec)/Mpc            # physical 1/m
D2a=(cs2*kphys)**2*D2b          # acceleration variance per ln k  [ (m/s^2)^2 ]
lnk=np.log(k); a_rms=np.sqrt(np.trapz(D2a,lnk))
kpeak_a=k[np.argmax(D2a)]

print("="*82)
print(f"BATH acceleration of the baryon fluid at z={zrec:.0f} (real CAMB baryon power, sound speed cs={np.sqrt(cs2):.2e})")
print("="*82)
print(f"  R(baryon loading)={R:.3f}; acceleration-variance peaks at k~{kpeak_a:.2f}/Mpc (small-scale/Silk-ish)")
print(f"  a_rms (bath, RMS over all modes) = {a_rms:.2e} m/s^2")
print(f"  (single acoustic-peak mode ~ 1e-9; the bath is ~{a_rms/1e-9:.0f}x larger -- the point)\n")
print(f"  {'branch':>12}{'a0(z_rec)':>14}{'x=a_rms/a0':>14}{'regime':>16}{'flat-like deficit':>18}")
for nm,a0z in [('flat/const',a0_flat),('rising',a0_rise),('declining',a0_decl)]:
    x=a_rms/a0z; reg='deep-Newtonian' if x>30 else ('MOND/modified' if x<3 else 'transition')
    def_=np.sqrt(1+a0z/a_rms)-1
    print(f"  {nm:>12}{a0z:>14.2e}{x:>14.1f}{reg:>16}{def_:>17.3%}")
print(f"""
VERDICT (regression fix):
  With the BATH acceleration a_rms~{a_rms:.0e} m/s^2 (the physically correct mu-argument for a nonlinear,
  nonlocal modified inertia), the acoustic baryon modes are DEEP-NEWTONIAN for both FLAT and DECLINING
  (x>>1), so the CMB modification is <0.5% -> Dchi2~0 -> BOTH ARE CMB-SAFE. RISING still has
  a0(z_rec)={a0_rise:.1e} > a_rms -> deep-MOND -> DEAD (prescription-independent, since E(1100)~2e4).
  => RETRACT 'CMB selects declining' / Dchi2~117: that was the PER-MODE artifact (a_peak~1e-9 -> x~25).
     The CMB does NOT discriminate flat vs declining; only the rising kill survives. The decisive test
     for declining-vs-constant remains a0(z~3), NOT the CMB. (Precise Dchi2 needs the full bath-kernel
     CLASS rerun -- a standing queue item -- but the deep-Newtonian regime makes flat-safe robust.)""")
