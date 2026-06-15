#!/usr/bin/env python3
"""Figure data + key numbers for EFE_dsunruh_paper.tex -- the framework's OWN dS-Unruh interpolation
nu(y)=sqrt(1+1/y) (=> g_obs=sqrt(g^2+g*a0)) used for BOTH the isolated RAR and the EFE, a0=9.36e-11.
Corrects the simple-mu the original EFE_paper.tex used for the EFE. C. Zimmerman / Opus 4.8, 2026-06-14."""
import numpy as np
def nu(y): y=np.maximum(y,1e-30); return np.sqrt(1.0+1.0/y)        # a0=1 units
def gobs_iso(gb): return np.sqrt(gb**2+gb)
def gobs_efe(gN,ge): return np.sqrt((gN+ge)**2+(gN+ge))-np.sqrt(ge**2+ge) if ge>0 else gobs_iso(gN)
c=2.99792458e8; G=6.674e-11; H0=2.184e-18; OmL=0.6847
rho_DE=OmL*3*H0**2/(8*np.pi*G); a0=0.5*c*np.sqrt(G*rho_DE)
eMW=(233e3)**2/(8.178*3.0857e19)/a0
print(f"a0={a0:.4e}  g_ext(MW)={eMW:.3f} a0")
def comp(ge):
    n=nu(ge); Le=-0.5/(1.0+ge); return n, n*(1+Le), (2/3)*n+(1/3)*n*(1+Le)
t,r,i=comp(eMW)
print(f"wide-binary cap: transverse={t:.3f} radial={r:.3f} orbit-avg={i:.3f}  v/vN-1={np.sqrt(i)-1:+.1%}")
print("(simple-mu would give 1.32; standard-mu 1.08 -- both NORMAL MOND, not the framework's dS-Unruh)")
