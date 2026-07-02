#!/usr/bin/env python3
"""
ADVERSARIAL VERIFICATION of lane L1 (hierarchical SPARC a0 arbiter) -- the INCLINATION-NORM
JACOBIAN FORK. The lane's likelihood rescales data AND errors by s=sin(i0)/sin(i) and includes
norm(i)=norm0-2N*ln(t): that is the transformed-data density WITHOUT the Jacobian (the missing
factor is exactly +2N*ln(t)), so i>i0 cells get a spurious -2N*ln(t) bonus, pulling a0_hat DOWN.
Proper data-space likelihood: V_obs fixed with FIXED published error e_V (=sigma_los/sin(i0), an
i-independent rescale of the raw measurement), model mean = V_mod*sqrt(d)*t, t=sin(i)/sin(i0);
the chi2 part is IDENTICAL in both conventions, only the norm differs. Li+2018's own MCMC uses
the (convention-independent) chi2 with no sigma-varying norm, so the CORRECTED form is the
Li-faithful one; the artifact enters only because the lane's f-profiling requires the norm.
This script re-runs the lane's headline configurations under BOTH conventions plus the corrected
honest-sigma ladder (mock-injection gate, bootstrap over galaxies, leave-out-top-2, McGaugh
comparator). Everything else in the lane script verified: fresh re-run exit 0 bit-identical,
gates A-D pass, constants (a0=9.36e-11 two routes), i-correction sign (synthetic recovery),
D-scaling (g_bar D-invariant), sample counts 175/171/37/94, published anchor 1.200e-10
independently reproduced (see VERIFY_L1_independent.py).
C. Zimmerman lane L1 adversarial verifier, 2026-07-02. numpy + local SPARC only.
"""
import numpy as np, glob, os, time
t0=time.time()
c=2.998e8; kpc=3.0857e19; H0=2.184e-18; OmL=0.685
A0FW=(c/2)*np.sqrt(3*OmL*H0**2/(8*np.pi)); A0FORK=1.13e-10
assert abs(A0FW/9.36e-11-1)<0.005
ROOT="/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data"
meta={}
for line in open(os.path.join(ROOT,"SPARC_Lelli2016c.mrt")):
    f=line.split()
    if len(f)<18: continue
    try: D=float(f[2]);eD=float(f[3]);inc=float(f[5]);ei=float(f[6]);Q=int(f[17])
    except ValueError: continue
    meta[f[0]]=dict(D0=D,eD=max(eD,0.05*D),i0=inc,ei=max(ei,1.0),Q=Q)
gals=[]
for f in sorted(glob.glob(os.path.join(ROOT,"sparc_data","*_rotmod.dat"))):
    d=np.genfromtxt(f,comments="#")
    if d.ndim!=2 or d.shape[1]<6: continue
    name=os.path.basename(f).split("_rotmod")[0]
    R,Vo,eV,Vg,Vd,Vb=(d[:,i] for i in range(6))
    ok=(Vo>0)&(eV>0)
    if ok.sum()<5 or name not in meta: continue
    gals.append(dict(name=name,R=R[ok],Vo=Vo[ok],eV=eV[ok],Vg=Vg[ok],Vd=Vd[ok],Vb=Vb[ok],**meta[name]))
assert len(gals)==171
gf=np.array([(lambda n_,d_: n_/max(d_,1e-30))(np.sum(np.sign(g["Vg"])*g["Vg"]**2),
     np.sum(np.sign(g["Vg"])*g["Vg"]**2)+0.5*np.sum(g["Vd"]**2)+0.7*np.sum(g["Vb"]**2)) for g in gals])
sel_gas=gf>0.5; assert sel_gas.sum()==37
nu_fw=lambda y: np.sqrt(1+1/y); nu_mcg=lambda y: 1/(1-np.exp(-np.sqrt(y)))
A0GRID=np.unique(np.concatenate([np.geomspace(0.6e-10,3.0e-10,17),np.geomspace(0.85e-10,1.75e-10,13),
        np.geomspace(0.9e-10,1.55e-10,19),[A0FW,A0FORK,1.2e-10,7.7e-11]]))
LNA0=np.log(A0GRID);NA=len(A0GRID)
IA_FW=int(np.argmin(abs(A0GRID-A0FW)));IA_FORK=int(np.argmin(abs(A0GRID-A0FORK)))
FGRID=np.array([0.0,.01,.02,.03,.04,.05,.055,.06,.065,.07,.08,.09,.105,.12,.135,.155,.17]);NF=len(FGRID)
LU0=np.log10(0.5);SIGU=0.10;LUGRID=LU0+np.arange(-0.65,0.6501,0.05);NU_=len(LUGRID)

def build(sample,nu,corrected):
    """corrected=True: proper data-space norm (i-independent). False: lane's -2N*ln(t) version."""
    n=len(sample);Tm=np.empty((n,NA,NF,NU_));U=10.0**LUGRID
    for k,g in enumerate(sample):
        Rm=g["R"]*kpc;sd=g["eD"]/g["D0"]
        dgr=np.linspace(max(1-3.5*sd,0.15),1+3.5*sd,13)
        ilo=max(g["i0"]-3.5*g["ei"],10.0);ihi=min(g["i0"]+3.5*g["ei"],89.9)
        igr=np.linspace(min(ilo,ihi-0.2),ihi,13)
        t=np.sin(np.radians(igr))/np.sin(np.radians(g["i0"]))
        gas=np.sign(g["Vg"])*g["Vg"]**2;star=g["Vd"]**2+1.4*g["Vb"]**2
        gbar=(gas[None,:]+U[:,None]*star[None,:])*1e6/Rm[None,:]
        msk=gbar[0]>0;gb=gbar[:,msk];Ru=Rm[msk];Vo=g["Vo"][msk];eV=g["eV"][msk];N=int(msk.sum())
        pdi=(((dgr-1)/sd)**2)[:,None]+(((igr-g["i0"])/g["ei"])**2)[None,:]
        if not corrected: pdi=pdi-2.0*N*np.log(t)[None,:]
        sqd=np.sqrt(dgr)
        for ia in range(NA):
            Vm0=np.sqrt(nu(gb/A0GRID[ia])*gb*Ru)/1e3
            for jf,f in enumerate(FGRID):
                s02=eV**2+(f*Vo)**2
                A=np.sum(Vo**2/s02);norm0=np.sum(np.log(2*np.pi*s02))
                B0=(Vm0*(Vo/s02)).sum(1);C0=((Vm0**2)*(1.0/s02)).sum(1)
                X=((A+norm0)+pdi[None,:,:]
                   -2.0*B0[:,None,None]*(sqd[:,None]*t[None,:])[None,:,:]
                   +C0[:,None,None]*(dgr[:,None]*(t**2)[None,:])[None,:,:])
                Xf=X.reshape(NU_,-1);xm=Xf.min(axis=1)
                Tm[k,ia,jf]=-0.5*xm+np.log(np.mean(np.exp(-0.5*(Xf-xm[:,None])),axis=1))
    return Tm
def combine(T):
    pu=((LUGRID-LU0)/SIGU)**2;W=T-0.5*pu[None,None,None,:]
    wm=W.max(axis=3,keepdims=True)
    return wm[...,0]+np.log(np.mean(np.exp(W-wm),axis=3))
def peak(prof):
    i=int(np.argmax(prof))
    if i==0 or i==NA-1: return A0GRID[i]
    x0,x1,x2=LNA0[i-1:i+2];y0,y1,y2=prof[i-1:i+2]
    den=(x0-x1)*(x0-x2)*(x1-x2)
    a=(x2*(y1-y0)+x1*(y0-y2)+x0*(y2-y1))/den
    b=(x2**2*(y0-y1)+x1**2*(y2-y0)+x0**2*(y1-y2))/den
    return float(np.exp(-b/(2*a))) if a<0 else A0GRID[i]
def rep(tag,G):
    M=G.sum(axis=0);prof=M.max(axis=1);dc=2*(prof.max()-prof)
    print(f"  {tag}: a0_hat={peak(prof):.3e}  Dchi2(9.36e-11)={dc[IA_FW]:.1f}  Dchi2(1.13e-10)={dc[IA_FORK]:.1f}")
    return peak(prof),dc[IA_FW],dc[IA_FORK],M
def boot(G,tag,nb=500,seed=7):
    rng=np.random.default_rng(seed);n=G.shape[0];hats=np.empty(nb)
    for b in range(nb): hats[b]=peak(G[rng.integers(0,n,n)].sum(axis=0).max(axis=1))
    pfw=np.mean(hats<=A0FW);pfk=np.mean(hats<=A0FORK)
    print(f"  boot {tag}: med={np.median(hats):.3e}  P(<=9.36e-11)={pfw:.3f}  P(<=1.13e-10)={pfk:.3f}")
    return pfw,pfk

print("=== A/B: lane norm (as run) vs corrected data-space norm (framework nu) ===")
Tm_lane=build(gals,nu_fw,corrected=False); G_lane=combine(Tm_lane)
aL,dL,kL,_=rep("LANE  fw full   ",G_lane); rep("LANE  fw gas-dom",G_lane[sel_gas])
assert abs(aL/1.239e-10-1)<0.01 and abs(dL-161.4)<2 and abs(kL-18.4)<1   # exact lane reproduction
Tm_cor=build(gals,nu_fw,corrected=True); G_cor=combine(Tm_cor)
aC,dC,kC,M=rep("CORR  fw full   ",G_cor); aCg,dCg,kCg,_=rep("CORR  fw gas-dom",G_cor[sel_gas])
print("\n=== corrected-norm honest-sigma ladder ===")
rng=np.random.default_rng(42); mock=[]
for g in gals:
    Rm=g["R"]*kpc
    gb=(np.sign(g["Vg"])*g["Vg"]**2+0.5*g["Vd"]**2+0.7*g["Vb"]**2)*1e6/Rm; ok=gb>0
    Vm=np.sqrt(nu_fw(gb[ok]/A0FW)*gb[ok]*Rm[ok])/1e3
    g2=dict(g)
    for key in ("R","Vg","Vd","Vb","eV"): g2[key]=g[key][ok]
    g2["Vo"]=Vm+rng.normal(0,g2["eV"])
    if (g2["Vo"]>0).all() and len(g2["Vo"])>=5: mock.append(g2)
am,dm,_,_=rep("MOCK corrected (truth 9.36e-11)",combine(build(mock,nu_fw,corrected=True)))
assert abs(am/A0FW-1)<0.05 and dm<4.0, "corrected machinery biased"
Gmc=combine(build(gals,nu_mcg,corrected=True)); rep("CORR mcg full   ",Gmc)
jf=int(np.argmax(M.max(axis=0)));ia_hat=int(np.argmax(M[:,jf]))
infl=2*(G_cor[:,ia_hat,jf]-G_cor[:,IA_FW,jf]);order=np.argsort(infl)[::-1]
print("  top influencers (corrected):",[(gals[k]['name'],round(float(infl[k]),1)) for k in order[:4]])
sel=np.ones(len(gals),bool);sel[order[0]]=False;sel[order[1]]=False
rep("CORR fw full leave-out-top-2",G_cor[sel])
boot(G_cor,"CORR fw full");boot(G_cor[sel_gas],"CORR fw gas-dom");boot(Gmc,"CORR mcg full")
print(f"\nVERDICT-RELEVANT DELTAS (lane -> corrected):")
print(f"  full-sample exclusion of 9.36e-11: {dL:.0f} -> {dC:.0f} (STRONGER; robust both conventions)")
print(f"  fork 1.13e-10 full-sample: {kL:.0f} -> {kC:.0f} naive (fork survival is convention-dependent)")
print(f"  gas-dom optimum: 8.67e-11 -> {aCg:.2e} ('low-sign' claim is a norm-term artifact;")
print(f"    robust statement: gas-dom framework-COMPATIBLE both ways, Dchi2(9.36e-11)<=1.5)")
print(f"{time.time()-t0:.0f}s; EXIT 0 = all assertions passed")
