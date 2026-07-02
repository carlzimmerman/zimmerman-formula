#!/usr/bin/env python3
"""Marginalized-M/L RAR on the framework's OWN nu (the banked referee-proofing gap, run inline 2026-07-02).
Fixed-Upsilon 0.108 dex was convention-compatible; the referee question: marginalize Upsilon per galaxy with an
SPS prior -- does the a0 posterior still admit 9.36e-11, and what a0 does SPARC prefer on the framework's nu?
Likelihood: per-point gaussian in log g_obs, sigma_i from velocity errors (+ global sigma_int profiled per a0);
per-galaxy Upsilon_disk marginalized over a lognormal prior (mean 0.5, sigma_dex in {0.10, 0.15}); Ub=1.4*Ud."""
import numpy as np, glob, os
c=2.998e8; G=6.674e-11; kpc=3.0857e19
H0=2.184e-18; OmL=0.685; rho_L=OmL*3*H0**2/(8*np.pi*G); A0FW=(c/2)*np.sqrt(G*rho_L)
DATA=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","data","sparc_data")
gals=[]
for f in sorted(glob.glob(os.path.join(DATA,"*_rotmod.dat"))):
    d=np.genfromtxt(f,comments="#")
    if d.ndim!=2 or d.shape[1]<6: continue
    R,Vo,eV,Vg,Vd,Vb=(d[:,i] for i in range(6)); Rm=R*kpc
    ok=(Vo>0)&(eV>0)&np.isfinite(Vo)
    if ok.sum()<5: continue
    gals.append((Rm[ok],Vo[ok],eV[ok],Vg[ok],Vd[ok],Vb[ok]))
print(f"galaxies: {len(gals)}  | framework a0 = {A0FW:.3e}")
def gpred(gb,a0): return np.sqrt(gb**2+gb*a0)
UGRID=np.exp(np.linspace(np.log(0.15),np.log(1.6),41))
def neg2lnL(a0,sig_int,sig_prior_dex):
    lp=np.log(UGRID/0.5)/np.log(10.)
    prior=np.exp(-0.5*(lp/sig_prior_dex)**2); prior/=prior.sum()
    tot=0.
    for Rm,Vo,eV,Vg,Vd,Vb in gals:
        go=(Vo*1e3)**2/Rm; sig_pt=(2*eV/Vo/np.log(10.))
        s2=sig_pt**2+sig_int**2
        c2=np.empty(len(UGRID))
        for i,U in enumerate(UGRID):
            Vb2=np.sign(Vg)*Vg**2+U*Vd**2+1.4*U*Vb**2
            gb=Vb2*1e6/Rm
            m=gb>0
            if m.sum()<3: c2[i]=1e9; continue
            r=np.log10(go[m])-np.log10(gpred(gb[m],a0))
            c2[i]=np.sum(r**2/s2[m]+np.log(2*np.pi*s2[m]))
        c2min=c2.min()
        tot+=-2*np.log(np.sum(prior*np.exp(-0.5*(c2-c2min))))+c2min
    return tot
A0S=np.geomspace(0.5e-10,3.2e-10,17)
for sp in (0.10,0.15):
    best=[]
    for a0 in A0S:
        si_grid=[0.06,0.08,0.10,0.12,0.15]
        best.append(min(neg2lnL(a0,si,sp) for si in si_grid))
    best=np.array(best); best-=best.min()
    # gaussian-ish interval from delta chi2
    from numpy.polynomial import polynomial as P
    ia=np.argmin(best); a0hat=A0S[ia]
    within1=A0S[best<1]; lo,hi=within1.min(),within1.max()
    d_fw=best[np.argmin(abs(A0S-A0FW))]; d_can=best[np.argmin(abs(A0S-1.2e-10))]
    print(f"[prior sigma={sp:.2f} dex] a0_hat={a0hat:.2e}  1sig=[{lo:.2e},{hi:.2e}]  "
          f"Dchi2(9.36e-11)={d_fw:.1f} (~{np.sqrt(max(d_fw,0)):.1f}sig)  Dchi2(1.2e-10)={d_can:.1f} (~{np.sqrt(max(d_can,0)):.1f}sig)")
print("note: correlated-point caveat applies (per-point independence assumed); interpret sigma as indicative.")

# ---- PART 2 (correction): global M/L ZERO-POINT nuisance (the calibration systematic) ----
# A coherent Upsilon shift is ONE systematic, not 171 independent penalties (the lensing lane's lesson:
# 'fiducial-mass stat-sigmas are convention statements'). Profile a global zero-point delta (dex) with prior
# sigma_cal, on top of per-galaxy scatter. Also: the validation gate the quick pass skipped.
print("\n--- validation gate: fixed Upsilon=0.70, a0=9.36e-11, weighted rms (banked: 0.108 dex) ---")
res=[];w=[]
for Rm,Vo,eV,Vg,Vd,Vb in gals:
    Vb2=np.sign(Vg)*Vg**2+0.70*Vd**2+0.98*Vb**2
    gb=Vb2*1e6/Rm; go=(Vo*1e3)**2/Rm; m=gb>0
    r=np.log10(go[m])-np.log10(gpred(gb[m],A0FW)); fr=np.clip(eV[m],1,None)/np.clip(Vo[m],1,None)
    res+=list(r); w+=list(1/fr**2)
res=np.array(res);w=np.array(w)
print(f"  weighted rms = {np.sqrt(np.sum(w*res**2)/np.sum(w)):.3f} dex  (gate: ~0.108)")
print("\n--- PART 2: global zero-point profiled ---")
DGRID=np.linspace(-0.25,0.35,25)   # global log10-M/L offset around the 0.5 mean
def neg2lnL_global(a0,sig_int,sp,sig_cal):
    vals=[]
    for dlt in DGRID:
        lp=np.log(UGRID/(0.5*10**dlt))/np.log(10.)
        prior=np.exp(-0.5*(lp/sp)**2); prior/=prior.sum()
        tot=0.
        for Rm,Vo,eV,Vg,Vd,Vb in gals:
            go=(Vo*1e3)**2/Rm; sig_pt=(2*eV/Vo/np.log(10.)); s2=sig_pt**2+sig_int**2
            c2=np.empty(len(UGRID))
            for i,U in enumerate(UGRID):
                Vb2=np.sign(Vg)*Vg**2+U*Vd**2+1.4*U*Vb**2; gb=Vb2*1e6/Rm; m=gb>0
                if m.sum()<3: c2[i]=1e9; continue
                r=np.log10(go[m])-np.log10(gpred(gb[m],a0))
                c2[i]=np.sum(r**2/s2[m]+np.log(2*np.pi*s2[m]))
            cm=c2.min(); tot+=-2*np.log(np.sum(prior*np.exp(-0.5*(c2-cm))))+cm
        vals.append(tot+ (dlt/sig_cal)**2)          # the calibration prior, ONCE
    return min(vals)
for sig_cal in (0.05,0.10,0.15):
    n2_fw =min(neg2lnL_global(A0FW ,si,0.10,sig_cal) for si in (0.08,0.10,0.12))
    n2_can=min(neg2lnL_global(1.2e-10,si,0.10,sig_cal) for si in (0.08,0.10,0.12))
    d=n2_fw-n2_can
    print(f"  sigma_cal={sig_cal:.2f} dex:  Dchi2(9.36e-11 vs 1.2e-10) = {d:+.2f}  (~{np.sqrt(abs(d)):.1f} sigma-equiv, sign {'AGAINST' if d>0 else 'FOR'} 9.36e-11)")
print("\nVERDICT: compare to the lensing lane's profiled fork (Dchi2 <= +1.5 with the M/L prior).")
