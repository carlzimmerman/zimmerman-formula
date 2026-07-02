#!/usr/bin/env python3
"""PRE-REGISTERED (RUN_NEXT_DOORS_RESULTS_2026-07): joint global (a0, Upsilon_3.6) SPARC refit on the framework's OWN nu,
with the MIGHTEE-measured Upsilon prior vs the SPS standard, both footing forks, reg-MOND comparator, and THE DECISIVE
CUT: gas-dominated SPARC galaxies (Upsilon-insensitive -> their a0 preference is prior-free). Both-ways: if the anchor
collapses under a realistic Upsilon prior AND the gas-dominated subsample independently wants high a0, the coefficient
miss is real; if gas-dominated galaxies sit near 9.36e-11, B3's residue is quarantined to population Upsilon."""
import numpy as np, glob, os
c=2.998e8; G=6.674e-11; kpc=3.0857e19
H0=2.184e-18; OmL=0.685; A0FW=(c/2)*np.sqrt(G*OmL*3*H0**2/(8*np.pi*G))
DATA=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","data","sparc_data")
gals=[]
for f in sorted(glob.glob(os.path.join(DATA,"*_rotmod.dat"))):
    d=np.genfromtxt(f,comments="#")
    if d.ndim!=2 or d.shape[1]<6: continue
    R,Vo,eV,Vg,Vd,Vb=(d[:,i] for i in range(6)); ok=(Vo>0)&(eV>0)
    if ok.sum()<5: continue
    gals.append(tuple(x[ok] for x in (R*kpc,Vo,eV,Vg,Vd,Vb)))
def gasfrac(g,U):
    Rm,Vo,eV,Vg,Vd,Vb=g
    num=np.sum(np.sign(Vg)*Vg**2); den=num+U*np.sum(Vd**2)+1.4*U*np.sum(Vb**2)
    return num/max(den,1e-30)
def nu_fw(y): return np.sqrt(1+1/y)
def nu_mcg(y): return 1/(1-np.exp(-np.sqrt(y)))
def m2ll(sub,a0,U,nu,si):
    tot=0.;n=0
    for Rm,Vo,eV,Vg,Vd,Vb in sub:
        go=(Vo*1e3)**2/Rm; s2=(2*eV/Vo/np.log(10.))**2+si**2
        gb=(np.sign(Vg)*Vg**2+U*Vd**2+1.4*U*Vb**2)*1e6/Rm; m=gb>0
        if m.sum()<3: continue
        r=np.log10(go[m])-np.log10(nu(gb[m]/a0)*gb[m])
        tot+=np.sum(r**2/s2[m]+np.log(2*np.pi*s2[m])); n+=m.sum()
    return tot,n
A0S=np.geomspace(0.6e-10,3.2e-10,21); US=np.geomspace(0.12,1.3,31); SIS=[0.06,0.08,0.10,0.12,0.15]
def surface(sub):
    S=np.empty((len(A0S),len(US)))
    for i,a0 in enumerate(A0S):
        for j,U in enumerate(US):
            S[i,j]=min(m2ll(sub,a0,U,nu_fw,si)[0] for si in SIS)
    return S
def report(tag,S,prior=None):
    P=S.copy()
    if prior:
        U0,sd=prior
        P=P+((np.log10(US/U0)/sd)**2)[None,:]
    prof=P.min(axis=1); prof-=prof.min()
    ia=np.argmin(prof); w1=A0S[prof<1]
    ja=np.argmin(P[ia]); d_fw=prof[np.argmin(abs(A0S-A0FW))]; d_fork=prof[np.argmin(abs(A0S-1.13e-10))]
    print(f"  {tag:<38} a0_hat={A0S[ia]:.2e} [{w1.min():.2e},{w1.max():.2e}]  U_hat={US[ja]:.2f}  "
          f"Dchi2(9.36e-11)={d_fw:6.1f}  Dchi2(1.13e-10)={d_fork:6.1f}")
print(f"galaxies={len(gals)}  A0FW={A0FW:.3e}   (correlated-point caveat: Dchi2 indicative, not gaussian sigma)")
S_all=surface(gals)
print("\n--- FULL SPARC, framework nu, global (a0,Upsilon) ---")
report("unconstrained (profile U)",S_all)
report("SPS prior U=0.50 (0.10 dex)",S_all,(0.50,0.10))
report("MIGHTEE prior U=0.27 (0.10 dex)",S_all,(0.27,0.10))
report("MIGHTEE prior U=0.36 (0.10 dex)",S_all,(0.36,0.10))
for Ufix in (0.27,0.36,0.70):
    j=np.argmin(abs(US-Ufix)); col=S_all[:,j]-S_all[:,j].min(); ia=np.argmin(col)
    print(f"  hard-fix U={US[j]:.2f}: a0_hat={A0S[ia]:.2e}  Dchi2(9.36e-11)={col[np.argmin(abs(A0S-A0FW))]:.1f}")
# THE DECISIVE CUT (at reference U=0.5 for classification; gas frac > 0.5 vs < 0.3)
gf=[gasfrac(g,0.5) for g in gals]
gasdom=[g for g,f in zip(gals,gf) if f>0.5]; stardom=[g for g,f in zip(gals,gf) if f<0.3]
print(f"\n--- THE DECISIVE CUT: gas-dominated N={len(gasdom)} (Upsilon-insensitive) vs star-dominated N={len(stardom)} ---")
report("GAS-DOMINATED, unconstrained",surface(gasdom))
report("STAR-DOMINATED, unconstrained",surface(stardom))
# comparator: reg-MOND (McGaugh nu) full sample for context
Sm=np.empty((len(A0S),len(US)))
for i,a0 in enumerate(A0S):
    for j,U in enumerate(US): Sm[i,j]=min(m2ll(gals,a0,U,nu_mcg,si)[0] for si in SIS)
prof=Sm.min(axis=1);prof-=prof.min();ia=np.argmin(prof)
print(f"\n  comparator reg-MOND(McGaugh nu): a0_hat={A0S[ia]:.2e}  best -2lnL diff (fw-mcg) = {S_all.min()-Sm.min():+.1f} (shape, full sample)")
