#!/usr/bin/env python3
r"""
ADVERSARIAL VERIFIER for lane D3_unsettled_observable.
Independent re-derivation, from scratch, of the load-bearing chain:
 (1) Crater II orbit timing (Kepler, Pace+22 MW+LMC peri/apo, corpus M_MW power law)
 (2) memory-weighted relational sigma excess, kernel band theta0 = sqrt2 .. 2
 (3) chL sigma-level mapping from the framework's OWN nu: g_obs=sqrt(g_bar^2+g_bar a0)
 (4) the n=1 Luo-tail value  -> EXPOSES a factor-2 print bug propagated to the verdict
 (5) headline-vs-script consistency: chM-only vs TOTAL(=chM+chL envelope) for the
     named systems -> EXPOSES envelope-as-central-value double count
 (6) footing fork both ways.
Exit 0 = my numbers; assertions state what the LANE claimed vs what is CORRECT.
"""
import math

G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; pc=3.0857e16
yr=3.1557e7; Gyr=1e9*yr; Mpc=1e3*kpc; c=2.99792458e8
H0=67.4e3/Mpc; HL=H0*math.sqrt(0.685); Z=math.sqrt(32*math.pi/3)
A0=c*HL/Z; A0A=c*H0/Z; TAU=0.45*Gyr
assert abs(A0-9.36e-11)<2e-13 and abs(A0A-1.13e-10)<2e-12   # footing anchors OK

# ---- (1) Crater II orbit, independent implementation ----
AL=math.log(7.0/4.0)/math.log(2.0)                 # corpus M(50)=4e11, M(100)=7e11
M=lambda r: 4e11*Msun*(r/(50*kpc))**AL
om=lambda r: math.sqrt(G*M(r)/r**3)
sig,rh,dist,rp,ra=2.7e3,1066*pc,117.5*kpc,24*kpc,138.1*kpc
w_in=sig/rh
a=(rp+ra)/2; e=(ra-rp)/(ra+rp)
T=2*math.pi*math.sqrt(a**3/(G*M(a)))
E=math.acos(max(min((1-dist/a)/e,1),-1))
t=(T/(2*math.pi))*(E-e*math.sin(E))                # outbound branch (DR4 caveat carried)
y_cur=om(dist)/w_in; y_per=om(rp)/w_in
print(f"CraterII: T={T/Gyr:.2f} Gyr  t_since_peri={t/Gyr:.2f} Gyr  phase={t/T:.2f}  "
      f"y_cur={y_cur:.2f}  y_peri={y_per:.2f}")
assert abs(y_cur-0.57)<0.02 and abs(y_per-3.28)<0.06 and abs(t/Gyr-0.77)<0.03  # lane numbers REPRODUCED

# ---- (2) kernel band relational excess (corpus convention fboost=sqrt(th0/th), verified
#          against real_research/reviews/dwarf_sigma_yeff_joint_pilot.py line 30) ----
w=math.exp(-t/TAU); ye=y_cur+(y_per-y_cur)*w
fb2=lambda y: math.sqrt(1+(math.sqrt(2)-1)*y*y)    # theta0=sqrt2
fbr=lambda y: math.sqrt(1+y*y)                     # theta0=2
lo=fb2(ye)/fb2(y_cur)-1; hi=fbr(ye)/fbr(y_cur)-1
print(f"  w={w:.3f} y_eff={ye:.2f}  chM relational excess = +{lo*100:.1f}% .. +{hi*100:.1f}%")
assert abs(lo-0.136)<0.005 and abs(hi-0.265)<0.01  # lane's +13.6..26.5% CONFIRMED
# sign convention: fboost INCREASES with y (framework MI-EFE enhancement; matches
# corpus pilot AND the banked wide-binary MI-EFE gamma~1.05-1.10 direction). Post-peri
# (y_eff>y_cur) => EXCESS; first-infall (y_eff<y_cur) => DEFICIT. Sign table STANDS.
yc_i=0.9; ye_i=yc_i+(0.1-yc_i)*0.7
assert fb2(ye_i)/fb2(yc_i)-1 < -0.05               # infall deficit sign CONFIRMED

# ---- (3) chL sigma mapping from the framework's own nu ----
# g_obs^2=g_bar^2+g_bar*a0 -> dln g_obs/dln a0 = 1/(2(1+x)); sigma^2~g_obs*r ->
# dln sigma/dln a0 = 1/(4(1+x)) -> deep-MOND factor 1/4. CONFIRMED symbolically:
x=1e-6; num=(math.sqrt(x**2+x*1.001)/math.sqrt(x**2+x)-1)/0.001
assert abs(num-0.5)<1e-3                            # dln g/dln a0 -> 1/2 deep MOND; x1/2 more for sigma

# ---- (4) the factor-2 bug: chL(n=1) ----
chL=lambda n: 0.25/(2*math.pi*n)
print(f"  chL(n=0.5)={chL(0.5)*100:.1f}%  chL(n=1)={chL(1)*100:.1f}%  chL(n=2)={chL(2)*100:.1f}%  "
      f"chL(n=10)={chL(10)*100:.2f}%")
assert abs(chL(1)-0.0398)<1e-4                      # CORRECT n=1 value = 4.0%
# The lane's verdict says 'chL 2.0% (n=1)': that is chL(n=2). D3_amplitude line 123
# prints (1/(4*pi))*0.25 labeled (n=1) -- a FACTOR-2 slip in a print (the loop above
# it is correct). Effect: the tail band should read 0.4..4.0% (n=1..10), not 0.4..2%.
assert abs(chL(2)-0.0199)<1e-4                      # the printed '2.0%' is the n=2 value
N=lambda s,err: math.ceil(2*(3*err/s)**2)
print(f"  chL-alone N/arm at corrected n=1 signal 4%, err 5%: {N(0.04,0.05)} "
      f"(lane quoted 113-2813 for 0.4-2%)")
assert N(0.04,0.05)<=29                             # detectability of the n~1 envelope is ~5x better than stated
# ...but chL is a ONE-SIDED UPPER ENVELOPE (positivity-locked, coherence discount <=x2):
# a null does NOT falsify; 'underpowered as a standalone DISCRIMINATOR' survives, the
# 450-2813/arm framing does not apply at the n~1-2 handover.

# ---- (5) headline vs script TOTAL: envelope double-count ----
n_cr=t/T                                            # lane resets chL clock at peri: n=0.27
tot_lo=lo+chL(n_cr); tot_hi=hi+chL(n_cr)
print(f"  named-systems script TOTAL for CraterII = +{tot_lo*100:.1f}..{tot_hi*100:.1f}% "
      f"(chL(n={n_cr:.2f})={chL(n_cr)*100:.1f}% added as a CENTRAL value)")
assert tot_lo>0.27                                  # script prints +28..41%, lane headline says +14-27%
# VERDICT on (5): the lane HEADLINE (+14-27% = chM only) and its OWN committed script
# (+28-41% TOTAL) disagree. The headline is the more defensible number: adding a <=
# envelope, extrapolated to n<1 (laneB quotes 1/(2 pi n) AT ~10 orbits; at n=0.16 it
# exceeds 100%), as a central value manufactures signal. Same issue: Antlia II
# (+3.4-6.7% claimed vs +13.7-17.0% printed), cluster spread (6-13% banked vs 18-25%
# printed), Leo I 'null ~0' (chM~0 but script TOTAL +3.4% via the no-reset clock).

# ---- (6) footing fork ----
for a0,tag in [(A0,"canonical"),(A0A,"alt")]:
    xx=sig**2/rh/a0
    print(f"  [{tag}] CraterII x=g_in/a0={xx:.4f} (deep-MOND carrier)  chM band a0-FREE")
    assert xx<0.01
# ---- (7) decay-timescale discriminator degeneracy (attack on discrimination row 2) ----
# Post-tidal-shock revirialization decays on ~few internal crossing times t_cross=rh/sigma.
# For the diffuse carriers this is STRUCTURALLY ~tau_mem: carriers need y~O(1), i.e.
# omega_in ~ omega_ext(peri), and tau_mem=0.45 Gyr ~ 1/omega_in for CraterII-class:
t_cross=rh/sig
print(f"  CraterII t_cross=rh/sigma={t_cross/Gyr:.2f} Gyr vs tau_mem=0.45 Gyr -> ratio {t_cross/TAU:.2f}")
assert 0.7<t_cross/TAU<1.2   # degenerate within ~15-30%: 'tides = NO decay' row is WRONG for shocks;
# post-shock sigma excess DOES relax, on nearly the SAME clock. The exp-decay discriminator is
# NOT clean on diffuse carriers; the first-infall SIGN FLIP (deficit) remains the clean one.
print("VERIFIER PASSED: chM chain + signs + footings REPRODUCED; chL n=1 factor-2, "
      "envelope-in-TOTAL double count, and decay-clock tidal degeneracy CONFIRMED")
