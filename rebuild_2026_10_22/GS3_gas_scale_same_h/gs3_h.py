#!/usr/bin/env python3
"""GS3 step 1: each catalogue's h from M500 = 500 rho_c(z) 4 pi/3 R500^3; offset at one h. kappa = 1/2 FITTED; not theory closed."""
import glob, json, math, os
import numpy as np
from astropy.io import fits
from scipy.optimize import least_squares
HERE=os.path.dirname(os.path.abspath(__file__)); RB=os.path.dirname(HERE); DATA=os.path.join(os.path.dirname(RB),"real_research","data"); G=4.30091e-9; OUT=[]
def P(s): print(s,flush=True); OUT.append(s)
def E2h2(M,Rmpc): return M/(500*4*math.pi/3*Rmpc**3)*8*math.pi*G/3/1e4   # h^2 E^2
def fit(z,y):
    f=lambda p:np.log(p[0]**2*(p[1]*(1+z)**3+1-p[1]))-np.log(y); r=least_squares(lambda p:f(p),[0.7,0.3],loss="soft_l1",f_scale=0.01)
    hf=np.exp(0.5*np.median(np.log(y/(0.3*(1+z)**3+0.7)))); return r.x[0],r.x[1],float(hf),float(np.std(f(r.x)))
zs=np.array([.05,.2,.5]); k2=abs(fit(zs,0.68**2*(.31*(1+zs)**3+.69))[0]-.68)<=1e-4; P(f"K2 synthetic h 0.68 recovered: {k2}")
E=fits.open(os.path.join(DATA,"erass1cl_primary_v3.2.fits"))[1].data; z=np.array(E["BEST_Z"],float); M=np.array(E["M500"],float)*1e13; R=np.array(E["R500"],float)/1e3; s=np.isfinite(z)&(z>0.01)&(M>0)&(R>0); hE,oE,hE3,sc=fit(z[s],E2h2(M[s],R[s])); P(f"eRASS1 n {s.sum()}: h {hE:.4f}, Omega_m {oE:.4f}; at Om 0.3 h {hE3:.4f}; scatter in ln(h^2E^2) {sc:.4f}")
zz,yy,nm=[],[],[]
for d in sorted(glob.glob(os.path.join(DATA,"xcop","*"))):
    n=os.path.basename(d); f=os.path.join(d,f"{n}_hydro_mass.fits")
    if not os.path.exists(f): continue
    H=fits.open(f)[1]; h=H.header; rr=H.data; c=rr.columns.names; Mk=[k for k in c if k.upper().startswith("M_FORW") or k.upper().startswith("MASS") or k.upper()=="M"][0]; Rk=[k for k in c if k.upper().startswith("R")][0]; r=np.array(rr[Rk],float); m=np.array(rr[Mk],float)
    r5=h["R500"]; rk=r*r5 if r.max()<20 else r; M5=float(np.exp(np.interp(math.log(r5),np.log(rk),np.log(m)))); M5=M5*1e14 if M5<1e4 else M5; zz.append(h["REDSHIFT"]); yy.append(E2h2(M5,r5/1e3)); nm.append(n)
    if len(nm)==1: P(f"  X-COP columns {c}; {n} M500 {M5:.3e}, R500 {r5}")
zz,yy=np.array(zz),np.array(yy); hX=np.exp(.5*np.median(np.log(yy/(.3*(1+zz)**3+.7)))); hsc=float(np.std(.5*np.log(yy/(.3*(1+zz)**3+.7)))); P(f"X-COP n {len(zz)}: h at Om 0.3 {hX:.4f}, scatter {hsc:.4f}")
und=abs(sc)>0.02
I=json.load(open(os.path.join(RB,"RF3_cluster_keys_hse_free","rf3_inputs.json")))["XF"]; rows=I["rows"]; P("RF3 rows "+str(list(rows[0].keys()))); SM=[r["name"] if "name" in r else r.get("xcop") for r in rows]
d0=np.array([r["dex_at_eRASS_R500"] for r in rows]); med0=float(np.median(d0)); se=float(np.std(d0,ddof=1)/math.sqrt(len(d0))); hXse=hsc/math.sqrt(len(zz)); idX=hXse<=0.005; P(f"RF3's offset rows {np.round(d0,3).tolist()}, median {med0:+.3f}, SE {se:.3f}; eRASS1 h identified to {sc/2:.4f}; X-COP h SE {hXse:.4f}: {'identified' if idX else 'NOT identified to 0.005'}")
P(f"Reported: X-COP at 0.70 (its stated convention) leaves {med0:+.3f}; at this measured {hX:.4f}, mass x q^2.5 and radius x q, about {med0+2.5*math.log10(hX/hE):+.3f}. Z = 2 on G-OUT-M3 at +0.093 (RF3).")
med=med0
json.dump(dict(hE=hE,oE=oE,hE3=hE3,hX=hX,offset=med,se=se,rows=d0.tolist(),k2=bool(k2),x_identified=bool(idX)),open(os.path.join(HERE,"gs3_h.json"),"w"),indent=1); open(os.path.join(HERE,"gs3_h.out"),"w").write("\n".join(OUT)+"\n")
