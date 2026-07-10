#!/usr/bin/env python3
"""
THE BRANCH-B DECIDER: point-level SPARC fit at FIXED a0 for the sharp-screened medium
response that passes the Cassini Q2 gate. Desmond+2024's 8.7-sigma RAR-vs-Q2 penalty was
at FITTED a0 with their hierarchical likelihood; the framework's question is at FIXED
a0 = 9.36e-11 (canonical; alt 1.13e-10) with the framework's own protocol (Upsilon refit,
weighted point-level rms over all SPARC points). PRE-COMMITTED RULE (stated before running):
  ALIVE        if the sharp screen's full weighted rms is within ~0.010 dex of framework-nu
  DEAD         if it exceeds reg-MOND's 0.122 dex (a Desmond-sized transition penalty)
  CONDITIONAL  in between (state the number; the transition bins carry the verdict)
Pipeline verbatim from laneA_family_scan.py (validated: reproduces the banked 0.108 @ 0.70).
"""
import numpy as np, glob, os, sys
kpc=3.086e19; A0C=9.36e-11; A0A=1.13e-10
DATADIR="/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
def load_sparc():
    Rl,Vol,eVl,Vg2l,Vd2l,Vb2l=[],[],[],[],[],[]
    for f in sorted(glob.glob(os.path.join(DATADIR,"*_rotmod.dat"))):
        try: d=np.genfromtxt(f,comments="#")
        except Exception: continue
        if d.ndim!=2 or d.shape[1]<6: continue
        R,Vobs,eV,Vgas,Vdisk,Vbul=(d[:,i] for i in range(6))
        Rl.append(R*kpc);Vol.append(Vobs);eVl.append(eV)
        Vg2l.append(np.sign(Vgas)*Vgas**2);Vd2l.append(Vdisk**2);Vb2l.append(Vbul**2)
    return (np.concatenate(Rl),np.concatenate(Vol),np.concatenate(eVl),
            np.concatenate(Vg2l),np.concatenate(Vd2l),np.concatenate(Vb2l))
Rm,Vobs,eV,Vg2,Vd2,Vb2=load_sparc()
gobs=(Vobs*1e3)**2/Rm
w=1.0/np.clip(eV,1,None)**2*np.clip(Vobs,1,None)**2
UGRID=np.arange(0.30,1.2001,0.025)
def fit(boost,a0):
    best=(None,1e9,None,None)
    for Ud in UGRID:
        gb=(Vg2+Ud*Vd2+1.4*Ud*Vb2)*1e6/Rm
        ok=(gb>0)&(gobs>0)&np.isfinite(gb)&(Vobs>0)
        gp=gb[ok]*(1.0+boost(gb[ok]/a0))
        r=np.log10(gobs[ok])-np.log10(gp)
        rms=np.sqrt(np.sum(w[ok]*r**2)/np.sum(w[ok]))
        if rms<best[1]: best=(Ud,rms,r,gb[ok]/a0)
    Ud,rms,r,y=best; meds={}
    for ys in (0.1,0.5,1.0,2.0,6.0):
        m=np.abs(np.log10(y/ys))<0.15
        meds[ys]=(np.median(r[m]) if m.sum()>=8 else np.nan, int(m.sum()))
    return Ud,rms,meds
nu_fw=lambda y: np.sqrt(1.0+1.0/np.maximum(y,1e-12))
F_fw =lambda y: nu_fw(y)-1.0
def F_delta(y,d,amp=0.9822):                       # sharp Desmond delta-family, 0.982-anchored
    y=np.maximum(y,1e-12)
    return amp*((1.0-np.exp(-y**(d/2.0)))**(-1.0/d)-1.0)
def F_pow(y,p,yt,n,amp=0.9822):                    # sharp power screen
    y=np.maximum(y,1e-12)
    return amp*y**-0.5*(1.0+(y/yt)**n)**(-(p-0.5)/n)
print("="*88)
print("BRANCH-B DECIDER: point-level SPARC (175 gal, %d pts) at FIXED a0, Upsilon refit"%len(Rm))
print("="*88)
for tag,a0 in (("CANONICAL 9.36e-11",A0C),("ALT 1.13e-10",A0A)):
    Uf,rf,mf=fit(F_fw,a0)
    print(f"\n--- {tag}:  framework-nu benchmark  rms={rf:.4f} dex @ Ups={Uf:.2f} "
          f"(banked 0.108 @ 0.70)"+("  [BENCH OK]" if abs(rf-0.108)<0.012 else "  [BENCH DRIFT]"))
    if a0==A0C: assert abs(rf-0.108)<0.012 and abs(Uf-0.70)<0.10, "pipeline broken"
    rows=[("delta d=4",lambda y:F_delta(y,4)),("delta d=5",lambda y:F_delta(y,5)),
          ("delta d=6",lambda y:F_delta(y,6)),("delta d=8",lambda y:F_delta(y,8)),
          ("pow p=6 yt=1 n=2",lambda y:F_pow(y,6,1.0,2)),
          ("pow p=8 yt=0.5 n=2",lambda y:F_pow(y,8,0.5,2)),
          ("pow p=8 yt=1 n=2",lambda y:F_pow(y,8,1.0,2)),
          ("pow p=8 yt=1.5 n=2",lambda y:F_pow(y,8,1.5,2))]
    print(f"  {'member':>20} {'Ups':>5} {'rms':>7} {'drms':>7}  med(y=0.5) med(y=1) med(y=2)  verdict")
    for name,Fb in rows:
        U,r,m=fit(Fb,a0); d=r-rf
        v="ALIVE" if d<=0.010 else ("DEAD" if r>0.122 else "COND")
        flag=" Ups>0.8!" if U>0.8+1e-9 else ""
        print(f"  {name:>20} {U:>5.2f} {r:>7.4f} {d:>+7.4f}   {m[0.5][0]:+8.3f} {m[1.0][0]:+8.3f} {m[2.0][0]:+8.3f}  {v}{flag}")
print("\n"+"="*88)
print("FINITE-y LENSING-NORM CHECK (does the d=6 screen erode the 0.982 deep match where")
print("galaxy-galaxy lensing actually measures, y~0.03-0.3?)  ratio = F_d6 / (0.982 y^-1/2):")
for ys in (0.01,0.03,0.1,0.2,0.3,0.5):
    ratio=F_delta(np.array([ys]),6)[0]/(0.9822*ys**-0.5)
    print(f"   y={ys:<5}: ratio={ratio:.4f}  ({np.log10(ratio):+.3f} dex)")
print(" (Brouwer+2021 lensing band ~0.05-0.1 dex; erosion above that at measured y = a real cost)")
print("="*88); print("exit 0")
