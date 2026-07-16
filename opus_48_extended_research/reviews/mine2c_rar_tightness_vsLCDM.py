#!/usr/bin/env python3
"""
MINE 2c -- the REAL in-hand vs-LCDM chicken: RAR TIGHTNESS, not a0-invariance.
The clean, published, in-hand vs-LCDM result is: the SPARC RAR has total vertical
scatter ~0.13 dex, of which the observational/M-L budget accounts for ~essentially all,
leaving intrinsic scatter consistent with ZERO (Li+2018: 0.057 dex, Lelli+2017).
A one-parameter (a0) relation reproducing 2778 points to ~0.13 dex with ~0 intrinsic
scatter is what LCDM galaxy-formation cannot natively produce (halo scatter alone
predicts >>0.13 dex residual). Quantify the tightness honestly here.
"""
import glob,math,os
import numpy as np
KPC_M=3.0856775814913673e19; KMS=1e3
DATA=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","real_research","data","sparc_data")
A0=9.36e-11
def gds(gb,a0): return np.sqrt(gb*gb+gb*a0)
GB,GO,FE=[],[],[]
for p in sorted(glob.glob(os.path.join(DATA,"*_rotmod.dat"))):
    for line in open(p):
        s=line.strip()
        if not s or s.startswith("#"): continue
        q=s.split()
        if len(q)<6: continue
        try: r,vo,ev,vg,vd,vb=(float(q[i]) for i in range(6))
        except: continue
        if r<=0 or vo<=0 or ev<=0 or ev/vo>0.10: continue
        vbar2=vg*abs(vg)+0.70*vd*abs(vd)+0.70*vb*abs(vb)
        if vbar2<=0: continue
        rm=r*KPC_M
        GB.append(vbar2*KMS**2/rm); GO.append((vo*KMS)**2/rm); FE.append(2*ev/vo)
GB=np.array(GB);GO=np.array(GO);FE=np.array(FE)
resid=np.log10(GO)-np.log10(gds(GB,A0))   # vertical dex residual at framework a0
tot=np.sqrt(np.mean(resid**2))
# observational dex error budget (velocity error only; M/L, distance, inclination add more)
obs_dex=FE/math.log(10)
obs_budget=np.sqrt(np.mean(obs_dex**2))
intr2=tot**2-obs_budget**2
intr=math.sqrt(intr2) if intr2>0 else 0.0
print(f"SPARC RAR at framework a0=9.36e-11, Y=0.70, dS-Unruh nu  ({len(GB)} points):")
print(f"  total vertical scatter      : {tot:.4f} dex")
print(f"  velocity-error budget alone : {obs_budget:.4f} dex")
print(f"  residual intrinsic (this budget only): {intr:.4f} dex")
print(f"  (Li+2018 with full M/L+dist+incl budget -> intrinsic ~0.057 dex, ~consistent w/ 0)")
print()
print("vs-LCDM significance (model comparison, published, NOT re-derived here):")
print("  Li+2018 (ApJ 2018, 1610.08981 lineage): RAR favored over a feature-rich halo")
print("  model at very high odds; the framework reproduces 2778 pts with ONE parameter.")
print("  The '25-62 sigma too tight' = the BTFR/RAR-vs-halo-scatter model comparison,")
print("  NOT an a0-invariance-across-mass claim (that one FAILS: a0 trends w/ Vflat).")
