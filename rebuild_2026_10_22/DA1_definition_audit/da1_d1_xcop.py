#!/usr/bin/env python3
"""DA1 D1 part 1, from raw files before GS4/SM1 code is opened. eRASS1 primary catalogue vs X-COP's own Mgas(r): implied fiducial, then same-name offsets at each aperture. kappa = 1/2 FITTED; not theory closed."""
import json, os, re, sys, hashlib
import numpy as np
from astropy.io import fits
HERE=os.path.dirname(os.path.abspath(__file__)); DATA=os.path.join(HERE,'..','..','real_research','data'); OUT=[]
MODE=sys.argv[1] if len(sys.argv)>1 else 'PRIMARY'
def P(s): print(s); OUT.append(str(s))
d=fits.open(os.path.join(DATA,'erass1cl_primary_v3.2.fits'))[1].data
P('eRASS1 sha256 '+hashlib.sha256(open(os.path.join(DATA,'erass1cl_primary_v3.2.fits'),'rb').read()).hexdigest())
z=d['BEST_Z'];M=d['M500']*1e13;R=d['R500']; s=np.isfinite(M)&(M>0)&(R>0)
G=4.30091e-6; E=(8*np.pi*G/3*M[s]/(4/3*np.pi*500*R[s]**3))*1e6; A=np.vstack([(1+z[s])**3,np.ones(s.sum())]).T; c=np.linalg.lstsq(A,E,rcond=None)[0]
fid=dict(H0=float(np.sqrt(c.sum())),Om=float(c[0]/c.sum())); P(f"Catalogue M500, R500 and z imply H0 {fid['H0']:.3f}, Om {fid['Om']:.4f}, frac resid {np.std(E/(A@c)-1):.4f}, n {s.sum()}")
names=[n.strip() for n in d['MATCH_NAME']]; ra=d['RA'];dec=d['DEC']
Xdir=os.path.join(DATA,'xcop'); CL=sorted(x for x in os.listdir(Xdir) if os.path.isdir(os.path.join(Xdir,x)))
C=json.load(open(os.path.join(Xdir,'xcop_r500_ettori2019.json')))
POS={'A85':(10.46,-9.30),'A644':(124.36,-7.51),'A1644':(194.30,-17.41),'A1795':(207.22,26.59),'A2029':(227.73,5.74),'A2142':(239.58,27.23),'A2255':(258.13,64.06),'A2319':(290.30,43.95),'A3158':(55.72,-53.63),'A3266':(67.80,-61.44),'RXC1825':(276.35,30.44),'ZW1215':(184.42,3.66)}
rows=[]
for k in CL:
    r0,d0=POS[k]; sep=np.hypot((ra-r0)*np.cos(np.radians(d0)),dec-d0)*60; i=int(np.argmin(sep)); zc=C[k]['z'] if k in C else None
    if sep[i]>10: P(f"{k}: no eRASS1 row within 10' (nearest {sep[i]:.1f}')"); continue
    H=fits.open(os.path.join(Xdir,k,f'{k}_fgas_profile.fits'))[1]; f=H.data; x=f['RADIUS']; Mg=f['MGAS']; Rg=float(H.header['R500']); Rx=C[k]['R500']*1e3 if k in C else None
    if Rx is None: P(f"{k}: no R500 in Ettori table"); continue
    Rcat=float(R[i]); Mcat=float(d['MGAS500'][i])*1e11
    if not (Mcat>0 and Rcat>0 and abs(z[i]-zc)<0.01): P(f"{k}: row {names[i]!r} sep {sep[i]:.1f}' z {z[i]:.4f} vs {zc}, Mgas {Mcat}: rejected"); continue
    Mx=lambda rr: float(np.exp(np.interp(np.log(rr/Rg),np.log(x),np.log(Mg))))  # RADIUS is in units of this file's own header R500
    if MODE=='MUTATE_h': Mcat_u=Mcat*(0.7/1.0)**2.5   # planted: h^-5/2 scaling applied one-sidedly to the catalogue
    else: Mcat_u=Mcat
    rows.append(dict(name=k,match=names[i],sep_arcmin=float(sep[i]),z_cat=float(z[i]),z_x=zc,R500_cat=Rcat,R500_x=Rx,Mgas_cat=Mcat_u,Mgas_x_own=Mx(Rx),Mgas_x_at_cat=Mx(Rcat),off_own=float(np.log10(Mx(Rx)/Mcat_u)),off_same_aperture=float(np.log10(Mx(Rcat)/Mcat_u)),L=float(d['MGAS500_L'][i]),H=float(d['MGAS500_H'][i]),kT=float(d['KT'][i]),M500_cat=float(M[i]),M500_x=C[k]['M500']*1e14))
for r in rows: P(f"{r['name']:8s} [{r['match'][:16]:16s}] sep {r['sep_arcmin']:.1f}' z {r['z_cat']:.4f}/{r['z_x']} R500 cat {r['R500_cat']:.0f} X {r['R500_x']:.0f} kpc; M500 cat {r['M500_cat']:.2e} X {r['M500_x']:.2e}; Mgas cat {r['Mgas_cat']:.3e}; X at own R500 {r['Mgas_x_own']:.3e}, at cat R500 {r['Mgas_x_at_cat']:.3e}; off own {r['off_own']:+.3f}, same aperture {r['off_same_aperture']:+.3f}")
o=np.array([r['off_own'] for r in rows]); a=np.array([r['off_same_aperture'] for r in rows])
P(f"n {len(rows)}: median offset, own apertures {np.median(o):+.3f} (std {o.std(ddof=1):.3f}); same aperture (cat R500) {np.median(a):+.3f} (std {a.std(ddof=1):.3f}), mean {a.mean():+.3f}")
# conventions from the two papers
P(f"Convention: eRASS1 rho_gas/(m_p n_e) = 1.18; X-COP = 0.61*(1+1/1.17) = {0.61*(1+1/1.17):.4f}; X-COP lower by {np.log10(1.18/(0.61*(1+1/1.17))):.4f} dex for the same n_e")
json.dump(dict(fid=fid,rows=rows,median_own=float(np.median(o)),median_same=float(np.median(a)),conv_dex=float(np.log10(1.18/(0.61*(1+1/1.17))))),open(os.path.join(HERE,f'da1_d1_xcop_{MODE}.json'),'w'),indent=1)
open(os.path.join(HERE,f'da1_d1_xcop_{MODE}.out'),'w').write('\n'.join(OUT)+'\n')
