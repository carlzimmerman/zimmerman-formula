#!/usr/bin/env python3
"""
WB-F Correction 1: the super-escape contamination discriminator is THEORY-LADEN.
The f_triple inference (wb_deprojection_mc.py) counted ANY vtilde > sqrt(2) as unbound -> contamination.
But sqrt(2) is the NEWTONIAN escape ratio. Under the framework's own EFE-suppressed MOND dynamics bound pairs
extend further: v_esc/v_c >~ 1.42 (parallel to the external field), 1.65 (perpendicular), ~1.55 (angle-averaged).
So in the MOND branch a slice of the "super-escape demand" (sqrt(2) < vtilde < 1.65) is BOUND -> boost, not triples.
Rerun the triple-demand at each threshold and show f_triple shifts DOWN in the MOND branch => the contamination
discriminator differs between the Newtonian and MOND hypotheses BY CONSTRUCTION. Inline, no swarms. 2026-06-10.
"""
import numpy as np, warnings, os; warnings.filterwarnings('ignore')
from astropy.io import fits
rng=np.random.default_rng(20260610)
G=6.674e-11;Msun=1.989e30;AU=1.496e11;a0=9.36e-11
F=os.path.join(os.path.dirname(__file__),'all_columns_catalog.fits.gz')
C=['ra1','dec1','parallax1','parallax2','parallax_error1','parallax_error2','pmra1','pmra2','pmdec1','pmdec2',
   'pmra_error1','pmra_error2','pmdec_error1','pmdec_error2','ruwe1','ruwe2','ipd_frac_multi_peak1',
   'ipd_frac_multi_peak2','phot_g_mean_mag1','phot_g_mean_mag2','sep_AU']
with fits.open(F,memmap=True) as h:
    d=h[1].data; D={k:np.array(d[k],dtype='f8') for k in C}
aN,dN=np.radians(192.85948),np.radians(27.12825); ra,dec=np.radians(D['ra1']),np.radians(D['dec1'])
bg=np.degrees(np.arcsin(np.sin(dec)*np.sin(dN)+np.cos(dec)*np.cos(dN)*np.cos(ra-aN)))
d1=1000/D['parallax1'];d2=1000/D['parallax2'];dist=0.5*(d1+d2);skAU=D['sep_AU']/1e3
sd1=1000*D['parallax_error1']/D['parallax1']**2;sd2=1000*D['parallax_error2']/D['parallax2']**2;sdd=np.hypot(sd1,sd2)
MG1=D['phot_g_mean_mag1']-5*np.log10(dist/10);MG2=D['phot_g_mean_mag2']-5*np.log10(dist/10)
xg=np.linspace(-1.46,0.99,4000);MGg=4.887-5.693*xg+0.4164*xg**2+0.9611*xg**3;o=np.argsort(MGg)
mfn=lambda MG:np.exp(np.interp(np.clip(MG,0.6,11.1),MGg[o],xg[o]));Mtot=mfn(MG1)+mfn(MG2)
s=D['sep_AU']*AU;dpm=np.hypot(D['pmra1']-D['pmra2'],D['pmdec1']-D['pmdec2'])
vN=np.sqrt(G*Mtot*Msun/s)/1e3;vsky=4.74*dpm*(dist/1000);vt=vsky/vN;x=np.log10(G*Mtot*Msun/s**2/a0)
sdpm=np.sqrt(((D['pmra1']-D['pmra2'])*np.hypot(D['pmra_error1'],D['pmra_error2']))**2
            +((D['pmdec1']-D['pmdec2'])*np.hypot(D['pmdec_error1'],D['pmdec_error2']))**2)/np.maximum(dpm,1e-6)
svt=np.sqrt((4.74*dist/1000*sdpm)**2+(4.74*dpm/1000*sdd)**2)/vN
sel=((np.abs(bg)>15)&(D['phot_g_mean_mag1']<17)&(D['phot_g_mean_mag2']<17)&(dist<250)&(D['ruwe1']<1.2)&(D['ruwe2']<1.2)
   &(skAU>2)&(skAU<30)&(D['ipd_frac_multi_peak1']<=2)&(D['ipd_frac_multi_peak2']<=2)
   &(Mtot>0.464)&(Mtot<4.31)&(vt<=5)&(np.abs(d1-d2)<np.minimum(4*sdd,8)))
deep=sel&(x<-0.5)&np.isfinite(vt)
vtd=vt[deep]; svd=np.clip(svt[deep],1e-3,2.0); Nd=deep.sum()
print(f"Banik-exact deep bins (g_N/a0<0.3): N={Nd}")

def kepler(M,e):
    E=M.copy()
    for _ in range(40): E-=(E-e*np.sin(E)-M)/(1-e*np.cos(E))
    return E
def newton_vt(n,alpha=1.5):                  # scale-free Newtonian vtilde (super-thermal e), matched calibration
    e=rng.uniform(0,1,n)**(1/(alpha+1)); Me=rng.uniform(0,2*np.pi,n); w=rng.uniform(0,2*np.pi,n); ci=rng.uniform(-1,1,n)
    E=kepler(Me,e); cE,sE=np.cos(E),np.sin(E); q=np.sqrt(1-e*e); r_a=1-e*cE
    px,py=cE-e,q*sE; vx,vy=-sE/r_a,q*cE/r_a
    a1p=px*np.cos(w)-py*np.sin(w);a2p=px*np.sin(w)+py*np.cos(w)
    a1v=vx*np.cos(w)-vy*np.sin(w);a2v=vx*np.sin(w)+vy*np.cos(w)
    return np.sqrt(a1v**2+(a2v*ci)**2)*np.sqrt(np.sqrt(a1p**2+(a2p*ci)**2))

def model_se(ftrip,T,K=200):                 # MC super-escape fraction above threshold T, with contamination ftrip
    base=newton_vt(Nd*K); sig=np.repeat(svd,K)
    phi=rng.uniform(0,2*np.pi,Nd*K)
    o=np.hypot(base*np.cos(phi)+rng.normal(0,1,Nd*K)*sig, base*np.sin(phi)+rng.normal(0,1,Nd*K)*sig)
    tri=rng.uniform(0,1,Nd*K)<ftrip; o=np.where(tri,o+np.abs(rng.normal(0,1,Nd*K)),o)
    return np.mean(o>T)

THR={'sqrt2 = 1.414 (NEWTON escape)':np.sqrt(2),'1.55 (MOND, angle-avg)':1.55,'1.65 (MOND, perpendicular)':1.65}
print("\n  threshold T            | data super-esc | f_triple needed to match (Newton-MC intrinsic + triples)")
for lab,T in THR.items():
    dse=np.mean(vtd>T)
    # solve for f_triple: sweep and pick the closest
    fs=np.linspace(0,0.30,31); diffs=[abs(model_se(f,T)-dse) for f in fs]; fbest=fs[int(np.argmin(diffs))]
    print(f"  {lab:24s} |     {dse:.3f}      |   f_triple = {fbest:.2f}")
print("""
READING (Correction 1 -- both-ways, including against Fable's own expectation):
 * Data super-escape DROPS with threshold: 0.098 (sqrt2) -> 0.078 (1.55) -> 0.070 (1.65). The ~0.028 of deep
   pairs in the sqrt(2)<vtilde<1.65 window are real and RECLASSIFIABLE.
 * BUT the inferred f_triple is ~FLAT (0.19-0.20), NOT lower as predicted -- because raising the threshold also
   lowers each triple's super-escape contribution above it, and the two effects cancel. Reported as found.
 * The genuine theory-ladenness is the RECLASSIFICATION, not an f_triple shift: the sqrt(2)-1.65 window is
   'unbound contamination' under Newton but 'boosted-bound orbits' under the framework's EFE-suppressed MOND
   (v_esc/v_c: 1.42 parallel, 1.65 perp, ~1.55 angle-avg). The SAME pairs are junk in one hypothesis and signal
   in the other, by construction.
 * => The contamination discriminator is HYPOTHESIS-DEPENDENT. Verdict UNCHANGED (the deep excess is still
   absorbable as contamination under Newton), but the 'absorbed by contamination' framing is itself
   Newton-laden; under the MOND hypothesis those pairs are the predicted population. Degeneracy DEEPENED. The
   synthesis must say this -- a referee would otherwise say it for us.""")
