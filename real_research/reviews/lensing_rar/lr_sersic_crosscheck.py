#!/usr/bin/env python3
"""
LR cross-check — the SERSIC-INDEX split (Fig-8 Sersicbin_1/2 + covariance), the second independent morphology
axis in Brouwer+2021's release. Same machinery as lr_battery.py (the u-r split). Brouwer report the >=6sigma
for EACH split independently, so this is a genuine cross-check, not a re-test of the same selection:
Sersicbin_1 = low n (disky -> late), Sersicbin_2 = high n (spheroidal -> early), per the README bin ordering.
The Sersic threshold itself is recovered from the covariance bin-min values (as u-r=2.5 was).
Reruns: baseline split sigma, the conversion-differential erosion ladder (axis 1), the differential-gas
requirement (axis 2). Inline, no swarms.  C. Zimmerman, 2026-06-10.
"""
import numpy as np, os
from scipy import stats
from esd_conversion import nfw_C
G=6.674e-11; Msun=1.989e30; pc=3.086e16
D=os.path.join(os.path.dirname(__file__),'..','..','data','lensing_rar','brouwer2021_rar')
late=np.loadtxt(os.path.join(D,'Fig-8_RAR-KiDS-isolated_Sersicbin_1.txt'))    # low n  = late/disky
early=np.loadtxt(os.path.join(D,'Fig-8_RAR-KiDS-isolated_Sersicbin_2.txt'))   # high n = early/spheroidal
covraw=np.loadtxt(os.path.join(D,'Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt'))
gbar=late[:,0]; n=len(gbar)
assert np.allclose(late[:,0],early[:,0],rtol=1e-3), "g_bar grids differ"
ESD2g=4*G*(Msun/pc**2)
esd_l=late[:,1]/late[:,4]; esd_e=early[:,1]/early[:,4]
vals=np.unique(covraw[:,0]); print(f"Sersic-index bin edges from covariance (threshold recovered from data): {vals}")
cb={vals[0]:0, vals[1]:1}
rad=np.unique(covraw[:,2]); C30=np.zeros((2*n,2*n))
for m,nn,ri,rj,cv,_,bias in covraw:
    i=cb[m]*n+int(np.argmin(abs(rad-ri))); j=cb[nn]*n+int(np.argmin(abs(rad-rj))); C30[i,j]=cv/bias
Cll=C30[:n,:n]*ESD2g**2; Cee=C30[n:,n:]*ESD2g**2; Cel=C30[n:,:n]*ESD2g**2
ge0=esd_e*ESD2g; gl0=esd_l*ESD2g
def sigma_of(ge,gl,Ce,Cl,Cx):
    d=ge-gl; Cd=Ce+Cl-(Cx+Cx.T)
    chi2=d@np.linalg.solve(Cd,d); return chi2, stats.norm.isf(0.5*stats.chi2.sf(chi2,df=n))
chi2,sig=sigma_of(ge0,gl0,Cee,Cll,Cel)
above=np.sum(ge0>gl0)
print(f"\nBASELINE Sersic split (C=4 both): chi2={chi2:.1f} (dof={n}) -> {sig:.1f} sigma")
print(f"  early(high-n) ABOVE late(low-n) in {above}/{n} bins; mean dlog10(g_obs)={np.mean(np.log10(ge0/gl0)):.3f} dex")
print("\n=== AXIS 1 erosion ladder (conversion differential), Sersic split ===")
print("  C_early  C_late  dlogC(dex)  split_sigma")
for Ce_,Cl_,note in [(4.0,4.0,'baseline'),(nfw_C(10.),nfw_C(1.),'physical'),
                     (nfw_C(20.),nfw_C(0.5),'aggressive'),(np.pi,4.76,'extreme/implausible')]:
    fe,fl=Ce_/4.0,Cl_/4.0
    c2,s=sigma_of(ge0*fe,gl0*fl,Cee*fe*fe,Cll*fl*fl,Cel*fe*fl)
    print(f"  {Ce_:5.2f}   {Cl_:5.2f}   {np.log10(Ce_/Cl_):+6.3f}     {s:5.1f}   {note}")
print("\n=== AXIS 2: differential M_gas/M* to close (Sersic split) ===")
lge=np.log10(ge0); lgl=np.log10(gl0); lxb=np.log10(gbar)
order=np.argsort(lgl)
gbar_late_at=np.interp(lge,lgl[order],lxb[order])
f_req=10**(gbar_late_at-lxb)-1.0
good=np.isfinite(f_req)&(f_req>-0.9)
print(f"  mean vertical split = {np.mean(lge-lgl):.3f} dex; median required differential M_gas/M* = {np.median(f_req[good]):.2f}")
print("""
CROSS-CHECK READING: if the Sersic split reproduces the u-r split's magnitude (~0.26 dex, ~8-9 sigma baseline,
~5 sigma after the physical conversion differential), the early/late RAR split is INDEPENDENT of which morphology
proxy defines the classes -- the exposure is classification-robust. Divergence between the two axes would instead
localize the split in one proxy (a selection systematic). Either way reported.""")
