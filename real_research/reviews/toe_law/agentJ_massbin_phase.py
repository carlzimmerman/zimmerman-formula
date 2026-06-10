#!/usr/bin/env python3
"""
agentJ: the mass-binned lensing-RAR phase test (follow-up to agentH3 T4)
========================================================================
THE TEST (locked in agentJ_massbin_phase.md before results): if the ~9-sigma early/late lensing-RAR split is
PHASE-DRIVEN (condensate disruption keyed to HALO MASS: 68% of early halos above the B-K condensation boundary
vs 27% late, agentH3_typesplit.out), then the lensing-RAR offset at fixed g_bar must GROW MONOTONICALLY WITH
STELLAR MASS independent of type, because more massive halos sit above the condensation boundary more often.

DATA (all on disk, Brouwer+2021 released): Fig-9_RAR-KiDS-isolated_Massbin-{1,2,3,4}.txt + covmatrix
(real_research/data/lensing_rar/brouwer2021_rar/). Mass-bin edges log10 M* = [8.5,10.3,10.6,10.8,11.0]
(README Fig-3 description, verified). 15 g_bar bins per mass bin, IDENTICAL g_bar grid across the four bins
(verified at runtime) -> the offset TREND between mass bins is exactly independent of the reference curve.

COMPUTED:
 1. per-mass-bin mean vertical offset Dlog10(g_obs) vs (a) the framework nu=sqrt(1+1/y) at a0=9.36e-11,
    (b) regular-MOND conventions (a0=1.2e-10; McGaugh nu) per the #1 working rule, (c) bin-1 as empirical
    reference. Two estimators: unweighted mean-dex (repo convention; common valid set b=1..14 because bin-1
    has ESD<0 at b=15) and a full-covariance GLS amplitude in linear ESD space (all 15 points).
    Full 60x60 released covariance throughout (bias-corrected per README).
 2. TREND: GLS slope d(offset)/d(log10 M*) with the propagated 4x4 offset covariance; flat-vs-line Dchi2;
    pairwise monotonicity with errors.
 3. PHASE-CHAIN CONFRONTATION: the same SHMR/NFW machinery that produced the sign-matched type split
    (agentH3_typesplit.py / agentH_perclass_C.py, verbatim functions) run per MASS bin: predicted offsets,
    predicted bin-k-minus-bin-1 differences and ratios, predicted slope; condensation-boundary fraction per
    bin (B-K M ~ 1e12/h, arXiv:1507.01019 eq 18 context; BFK R_T, arXiv:1711.05748 near eq 25).
    GATE: the machinery must reproduce agentH3_typesplit's per-class numbers (med logM_h 12.36/11.86,
    frac-above 68%/27%) before any per-mass-bin number is trusted.
 4. THE BORING CONTROL (2-halo): at fixed g_bar, R = sqrt(G M_gal/g_bar) is ~2.6x larger for bin 4 than
    bin 1 -> more 2-halo. Two prongs: (i) restrict to bins where med R < r200 for ALL mass bins (1-halo-safe,
    the agentH_perclass_C windowing logic) and re-fit the slope; (ii) explicit linear-theory 2-halo estimate
    (EH98 no-wiggle P(k), arXiv:astro-ph/9709112 eqs 26-31, sigma8-normalized; Tinker+2010 Delta=200 bias,
    arXiv:1001.3162 Table 2; CPT growth) -> delta-g_2h per (massbin, g_bar bin), the 2-halo-induced offset
    trend, and the 2-halo-corrected measured slope (x0.5/x2 amplitude robustness).

PINNED RELATIONS: SHMR M13 arXiv:1205.5807 / B13 arXiv:1207.6105; c(M,z) D08 arXiv:0804.2486 /
DM14 arXiv:1402.7073; type-dep SHMR Mandelbaum+2016 arXiv:1509.06762 (variant); B-K condensation
arXiv:1507.01019; BFK R_T arXiv:1711.05748; EH98 astro-ph/9709112; Tinker bias arXiv:1001.3162.
Cosmology: Brouwer h=0.7, Om=0.3, OL=0.7. Window 0.03 < R < 3 h70^-1 Mpc (lr_published_pipeline.md).

VERDICT FORK (locked): PHASE-SUPPORTED (monotonic growth, magnitude consistent with the chain, survives the
2-halo control) / PHASE-NEUTRAL / PHASE-REFUTED (flat or non-monotonic where the chain demands growth -- full
weight against the H3 sign-match being phase-driven). Locked wording: this tests the real-lensing-mass class's
phase mechanism; it does not confirm any model. Agent J for C. Zimmerman, 2026-06-10. No git operations.
"""
import numpy as np, os
from scipy import stats

np.set_printoptions(suppress=True)
G=6.674e-11; Msun=1.989e30; pc=3.086e16; Mpc=3.0857e22
H0=70*1e3/Mpc; Om, OL, h = 0.3, 0.7, 0.7
rho_c0=3*H0**2/(8*np.pi*G)
ESD2g=4*G*(Msun/pc**2)                      # Brouwer eq 7: g_obs = 4 G ESD_t/bias (SIS C=4 convention)
HERE=os.path.dirname(os.path.abspath(__file__))
D=os.path.join(HERE,'..','..','data','lensing_rar')
B=os.path.join(D,'brouwer2021_rar')
P=print
LN10=np.log(10.0)
a0_FW=9.36e-11; a0_CAN=1.2e-10

def E2(z): return Om*(1+z)**3+OL
def rho_c(z): return rho_c0*E2(z)
def Delta_vir(z):
    d=Om*(1+z)**3/E2(z)-1.0
    return 18*np.pi**2+82*d-39*d**2

# ---------------- SHMRs + c(M,z) (verbatim from agentH_perclass_C.py / agentH3_typesplit.py) ----------------
def moster13_mstar(logMh,z):
    zf=z/(1+z)
    logM1=11.590+1.195*zf; N=0.0351-0.0247*zf; beta=1.376-0.826*zf; gam=0.608+0.329*zf
    r=10**(logMh-logM1)
    return logMh+np.log10(2*N/(r**-beta+r**gam))

def behroozi13_mstar(logMh,z):
    a=1/(1+z); nu=np.exp(-4*a**2)
    logM1 =11.514+(-1.793*(a-1)-0.251*z)*nu
    logeps=-1.777+(-0.006*(a-1)+0.000*z)*nu-0.119*(a-1)
    alpha =-1.412+(0.731*(a-1))*nu
    delta = 3.508+(2.608*(a-1)-0.043*z)*nu
    gamma = 0.316+(1.319*(a-1)+0.279*z)*nu
    def f(x):
        ex=np.clip(10**(-x),None,700.0)
        return -np.log10(10**(alpha*x)+1)+delta*(np.log10(1+np.exp(np.clip(x,None,700.0))))**gamma/(1+np.exp(ex))
    x=logMh-logM1
    return logeps+logM1+f(x)-f(0.0)

def invert_shmr(mstar_fn,logMs,z):
    grid=np.arange(10.0,15.5,0.005)
    znodes=np.round(np.arange(0.10,0.501,0.01),3)
    idx=np.clip(np.round((z-0.10)/0.01).astype(int),0,len(znodes)-1)
    out=np.empty_like(logMs)
    for k,zn in enumerate(znodes):
        m=idx==k
        if not m.any(): continue
        curve=mstar_fn(grid,zn)
        out[m]=np.interp(logMs[m],curve,grid)
    return out

def c_D08(M,z,kind='200',relaxed=False):
    piv=2e12/0.72
    if kind=='200': A,Bc,C=(6.71,-0.091,-0.44) if relaxed else (5.71,-0.084,-0.47)
    else:           A,Bc,C=(9.23,-0.090,-0.69) if relaxed else (7.85,-0.081,-0.71)
    return A*(M/piv)**Bc*(1+z)**C
def c_DM14(M,z,kind='200'):
    piv=1e12/0.671
    if kind=='200': a=0.520+(0.905-0.520)*np.exp(-0.617*z**1.21); b=-0.101+0.026*z
    else:           a=0.537+(1.025-0.537)*np.exp(-0.718*z**1.08); b=-0.097+0.024*z
    return 10**(a+b*np.log10(M/piv))

# =================== PART 0: data + gates ===================
P("="*104)
P("PART 0 -- data, covariance, gates")
P("="*104)
prof=[np.loadtxt(os.path.join(B,f'Fig-9_RAR-KiDS-isolated_Massbin-{k}.txt')) for k in (1,2,3,4)]
gbar=prof[0][:,0]; n=len(gbar); NB=4
for k in range(1,4):
    assert np.allclose(prof[k][:,0],gbar,rtol=1e-6), "g_bar grids differ between mass bins"
P(f"[gate] g_bar grid IDENTICAL across the 4 mass bins ({n} bins, {gbar[0]:.3e}..{gbar[-1]:.3e} m/s^2) -> "
  f"the mass-bin TREND is exactly independent of the reference curve (common per-bin subtraction).")
gobs=np.array([p[:,1]/p[:,4]*ESD2g for p in prof])           # (4,15)  g_obs = 4G ESD_t/bias
gerr=np.array([p[:,3]/p[:,4]*ESD2g for p in prof])
P(f"[note] bin-1 has {int(np.sum(prof[0][:,1]<=0))} non-positive ESD point (b=15, highest g_bar); "
  f"mean-dex estimator uses the common valid set b=1..14; GLS amplitude uses all 15.")

covraw=np.loadtxt(os.path.join(B,'Fig-9_RAR-KiDS-isolated_Massbins_covmatrix.txt'))
mvals=np.unique(covraw[:,0]); mi={v:i for i,v in enumerate(mvals)}
rad=np.unique(covraw[:,2]); assert len(rad)==n
C60=np.zeros((NB*n,NB*n))
for m,nn,ri,rj,cv,_,bias in covraw:
    i=mi[m]*n+int(np.argmin(abs(rad-ri))); j=mi[nn]*n+int(np.argmin(abs(rad-rj)))
    C60[i,j]=cv/bias
C60=0.5*(C60+C60.T)
Cg=C60*ESD2g**2
dg=np.sqrt(np.diag(Cg)).reshape(NB,n)
rel=np.abs(dg-gerr)/gerr
P(f"[gate] cov diagonal vs profile-file errors: max |sqrt(diag)-err|/err = {rel.max():.2e} "
  f"({'PASS' if rel.max()<0.02 else 'FAIL'})")
ev=np.linalg.eigvalsh(Cg)
P(f"[gate] covariance positive-definite: min eig = {ev[0]:.3e} ({'PASS' if ev[0]>0 else 'FAIL'})")

ln=np.load(os.path.join(D,'lr_lenses.npz'))
NL=len(ln['z'])
typ=ln['typ']; z=ln['z']; logMs=ln['logM'].copy(); Mgal=ln['Mgal'].copy()
P(f"[gate] lens catalog: {NL:,} isolated lenses ({'v4' if NL==181477 else 'NOT v4'}); med logM*={np.median(logMs):.3f}")
EDG=[8.5,10.3,10.6,10.8,11.0]
masks=[(logMs>=EDG[i])&(logMs<EDG[i+1]) for i in range(NB)]
medMs=np.array([np.median(logMs[m]) for m in masks])
medMg=np.array([np.median(np.log10(Mgal[m])) for m in masks])
medz =np.array([np.median(z[m]) for m in masks])
fearly=np.array([np.mean(typ[m]==1) for m in masks])
P(f"mass bins (edges {EDG}; {int(np.sum(logMs<8.5))} lenses below 8.5 excluded by edge):")
for k in range(NB):
    P(f"  bin{k+1}: N={masks[k].sum():6,}  med logM*={medMs[k]:.3f}  med logMgal={medMg[k]:.3f}  "
      f"med z={medz[k]:.3f}  frac early={fearly[k]:.2f}")
P(f"slope axis x = med logM* per bin: {np.round(medMs,3)} (span {medMs[-1]-medMs[0]:.2f} dex); "
  f"bin-midpoint robustness row carried in PART 2.")

# =================== PART 1: measured offsets ===================
P("\n"+"="*104)
P("PART 1 -- measured per-mass-bin offsets Dlog10 g_obs (full covariance)")
P("="*104)
def nu_fw(g,a0):  return np.sqrt(1.0+a0/g)                    # framework nu = sqrt(1+1/y)
def nu_mc(g,a0):  return 1.0/(1.0-np.exp(-np.sqrt(g/a0)))     # McGaugh/RAR nu
REFS={'framework nu, a0=9.36e-11':gbar*nu_fw(gbar,a0_FW),
      'framework nu, a0=1.20e-10':gbar*nu_fw(gbar,a0_CAN),
      'McGaugh nu,  a0=9.36e-11':gbar*nu_mc(gbar,a0_FW),
      'McGaugh nu,  a0=1.20e-10':gbar*nu_mc(gbar,a0_CAN)}
V=np.arange(n-1)                                              # common valid set b=1..14

def offsets_meandex(gref,Vset=V,gdat=None):
    gd=gobs if gdat is None else gdat
    Dk=np.log10(gd[:,Vset])-np.log10(gref[Vset])
    off=Dk.mean(axis=1)
    J=np.zeros((NB,NB*n))
    for k in range(NB): J[k,k*n+Vset]=1.0/(len(Vset)*LN10*gd[k,Vset])
    S=J@Cg@J.T
    return off,S

def offsets_gls(gref):
    A=np.zeros(NB); w=[]
    for k in range(NB):
        Ck=Cg[k*n:(k+1)*n,k*n:(k+1)*n]
        Wt=np.linalg.solve(Ck,gref)
        norm=Wt@gref
        A[k]=(Wt@gobs[k])/norm; w.append(Wt/norm)
    SA=np.zeros((NB,NB))
    for k in range(NB):
        for l in range(NB):
            SA[k,l]=w[k]@Cg[k*n:(k+1)*n,l*n:(l+1)*n]@w[l]
    off=np.log10(A); S=SA/np.outer(A,A)/LN10**2
    chi2=[ (gobs[k]-A[k]*gref)@np.linalg.solve(Cg[k*n:(k+1)*n,k*n:(k+1)*n],(gobs[k]-A[k]*gref)) for k in range(NB)]
    return off,S,np.array(chi2)

gref0=REFS['framework nu, a0=9.36e-11']
off_md,S_md=offsets_meandex(gref0)
off_gl,S_gl,chi2_gl=offsets_gls(gref0)
P("offsets vs the framework reference (mean-dex b=1..14 | GLS amplitude all 15, per-bin model chi2/dof):")
for k in range(NB):
    P(f"  bin{k+1} (med logM*={medMs[k]:.2f}): {off_md[k]:+.3f} +/- {np.sqrt(S_md[k,k]):.3f} dex   |   "
      f"{off_gl[k]:+.3f} +/- {np.sqrt(S_gl[k,k]):.3f} dex  (chi2/14={chi2_gl[k]/14:.1f})")
P("  [convention rows: same offsets under the other reference conventions -- per the #1 rule]")
for lab,gr in REFS.items():
    om,_=offsets_meandex(gr)
    P(f"    {lab}: offsets {np.round(om,3)}")
P("  [note] the GLS amplitude chi2/dof >> 1 flags that a single multiplicative amplitude is a poor model of the")
P("  full profile (the low-g_bar 2-halo upturn); mean-dex is the primary estimator (repo unweighted-dex convention).")

# bin-1 empirical reference
d_ref1=off_md-off_md[0]
e_ref1=np.array([np.sqrt(S_md[k,k]+S_md[0,0]-2*S_md[k,0]) for k in range(NB)])
P("\nbin-1 as empirical reference (mean-dex, correlated errors):")
for k in range(1,NB):
    P(f"  bin{k+1}-bin1: {d_ref1[k]:+.3f} +/- {e_ref1[k]:.3f} dex  ({d_ref1[k]/e_ref1[k]:+.1f} sigma)")

P("\nper-g_bar-bin detail (measured offset vs framework ref, dex):")
P(f"  {'g_bar':>9} {'bin1':>7} {'bin2':>7} {'bin3':>7} {'bin4':>7}")
for b in range(n):
    row=[(np.log10(gobs[k,b]/gref0[b]) if gobs[k,b]>0 else np.nan) for k in range(NB)]
    P(f"  {gbar[b]:>9.2e} "+" ".join(f"{r:+7.3f}" if np.isfinite(r) else "   neg." for r in row))

# =================== PART 2: trend test ===================
P("\n"+"="*104)
P("PART 2 -- the TREND test: slope d(offset)/d(log10 M*), full offset covariance")
P("="*104)
def gls_line(x,y,S):
    X=np.column_stack([np.ones(len(x)),x-x.mean()])
    Si=np.linalg.inv(S)
    cov=np.linalg.inv(X.T@Si@X)
    beta=cov@(X.T@Si@y)
    resid=y-X@beta
    chi2_line=resid@Si@resid
    # flat model
    w=Si.sum(); mu=(Si@y).sum()/w if False else (np.ones(len(x))@Si@y)/ (np.ones(len(x))@Si@np.ones(len(x)))
    r0=y-mu; chi2_flat=r0@Si@r0
    return beta[1],np.sqrt(cov[1,1]),chi2_flat,chi2_line

def report_slope(lab,x,off,S):
    s,es,c2f,c2l=gls_line(x,off,S)
    P(f"  {lab:58s} slope={s:+.3f} +/- {es:.3f} dex/dex ({s/es:+.1f} sigma); "
      f"chi2 flat->line {c2f:.1f}->{c2l:.1f} (Dchi2={c2f-c2l:.1f})")
    return s,es

P("primary (mean-dex offsets, framework ref; the slope is reference-independent -- verified below):")
s0,es0=report_slope("mean-dex, med-logM* axis",medMs,off_md,S_md)
for lab,gr in REFS.items():
    om,Sm=offsets_meandex(gr)
    s,_=gls_line(medMs,om,Sm)[:2]
    assert abs(s-s0)<1e-12
P(f"  [gate] slope under all 4 reference conventions identical to machine precision: PASS")
report_slope("GLS-amplitude offsets (weighting-convention row)",medMs,off_gl,S_gl)
mid=np.array([(EDG[i]+EDG[i+1])/2 for i in range(NB)])
report_slope("bin-midpoint x-axis (robustness)",mid,off_md,S_md)
report_slope("bin-index x-axis (rank robustness)",np.arange(1.,5.),off_md,S_md)

P("\npairwise monotonicity (mean-dex, correlated errors):")
mono=True
for k in range(1,NB):
    d=off_md[k]-off_md[k-1]; e=np.sqrt(S_md[k,k]+S_md[k-1,k-1]-2*S_md[k,k-1])
    P(f"  bin{k+1}-bin{k}: {d:+.3f} +/- {e:.3f} ({d/e:+.1f} sigma)")
    mono &= d>0
P(f"  monotonic increasing point estimates: {mono}")

P("\nmass-bin jackknife (drop one bin, mean-dex slope):")
for drop in range(NB):
    kk=[i for i in range(NB) if i!=drop]
    s,es=gls_line(medMs[kk],off_md[kk],S_md[np.ix_(kk,kk)])[:2]
    P(f"  drop bin{drop+1}: slope={s:+.3f} +/- {es:.3f} ({s/es:+.1f} sigma)")

# =================== PART 3: phase-chain confrontation ===================
P("\n"+"="*104)
P("PART 3 -- the phase chain, quantitatively (SHMR/NFW machinery of agentH3_typesplit, per MASS bin)")
P("="*104)
RMIN,RMAX=0.03,3.0
def halo_chain(shmr='M13',cM='D08',typedep=False,dlogMs=0.0,Mg=None):
    lm=logMs+dlogMs; Mg=Mgal if Mg is None else Mg
    if shmr=='M13': logMh=invert_shmr(moster13_mstar,lm,z); kind='200'
    else:           logMh=invert_shmr(behroozi13_mstar,lm,z); kind='vir'
    if typedep:
        F=10**np.interp(lm,[10.5,11.0],[np.log10(2.),np.log10(3.)])
        logMh=np.where(typ==1,logMh+np.log10(F),logMh)
    cfun=(lambda M,zz: c_D08(M,zz,kind)) if cM=='D08' else (lambda M,zz: c_DM14(M,zz,kind))
    cc=cfun(10**logMh,z); M=10**logMh*Msun
    Delta=200.0 if kind=='200' else Delta_vir(z)
    rD=(3*M/(4*np.pi*Delta*rho_c(z)))**(1/3)
    rs=rD/cc
    gfun=lambda u: np.log(1+u)-u/(1+u)
    medg=np.zeros((NB,n)); medR=np.zeros((NB,n)); Nwin=np.zeros((NB,n))
    for b in range(n):
        R=np.sqrt(G*Mg*Msun/gbar[b])
        win=(R/Mpc>RMIN)&(R/Mpc<RMAX)
        for k in range(NB):
            kk=win&masks[k]
            Nwin[k,b]=kk.sum()
            if kk.sum()<50: medg[k,b]=np.nan; medR[k,b]=np.nan; continue
            x=R[kk]/rs[kk]
            Mltr=M[kk]*gfun(x)/gfun(cc[kk])
            medg[k,b]=np.median(gbar[b]+G*Mltr/R[kk]**2)
            medR[k,b]=np.median(R[kk])/Mpc
    return medg,medR,Nwin,logMh,rD

P("[gate] reproduce agentH3_typesplit per-CLASS phase geography (M13xD08 type-blind):")
medg_p,medR_p,Nwin_p,logMh_p,rD_p=halo_chain('M13','D08',False)
Mcond=np.log10(1e12/0.7)
for t,lab,gate in ((1,'early','med logM_h=12.36 frac=68%'),(0,'late','med logM_h=11.86 frac=27%')):
    kk=typ==t
    P(f"  {lab}: med logM_h={np.median(logMh_p[kk]):.2f}; frac above boundary={np.mean(logMh_p[kk]>Mcond):.0%}"
      f"   [gate: {gate}]")

P("\nphase geography per MASS bin (M13xD08; B-K boundary logM_h > 12.15; BFK R_T, m=1eV sigma/m=0.01):")
fcond=np.zeros(NB); medMh=np.zeros(NB); r200med=np.zeros(NB)
for k in range(NB):
    mh=logMh_p[masks[k]]
    RT=310*((10**mh/1e12)**(1/7))*(0.01)**(2/7)
    r200=rD_p[masks[k]]/3.0857e19
    fcond[k]=np.mean(mh>Mcond); medMh[k]=np.median(mh); r200med[k]=np.median(r200)/1e3  # Mpc
    P(f"  bin{k+1} (med logM*={medMs[k]:.2f}): med logM_h={medMh[k]:.2f}; frac above boundary={fcond[k]:.0%}; "
      f"med R_T={np.median(RT):.0f} kpc; med r200={np.median(r200):.0f} kpc; core/r200={np.median(RT/r200):.2f}")
P(f"  -> the chain's premise: frac-above-boundary {'IS' if np.all(np.diff(fcond)>0) else 'is NOT'} monotonic "
  f"in M* ({', '.join(f'{f:.0%}' for f in fcond)}); the phase mechanism therefore DEMANDS a monotonic offset rise.")

def pred_offsets(medg,Vset=V):
    out=np.array([np.nanmean(np.log10(medg[k,Vset]/gref0[Vset])) for k in range(NB)])
    return out
P("\npredicted offsets (1-halo NFW; vs framework ref; mean over b=1..14) and bin-minus-bin1:")
P(f"  {'config':<38}{'bin1':>8}{'bin2':>8}{'bin3':>8}{'bin4':>8} | {'D21':>7}{'D31':>7}{'D41':>7} | {'slope':>7}")
CONFIGS=[('M13','D08',False,0.0,'M13 x D08, type-blind (primary)'),
         ('B13','DM14',False,0.0,'B13 x DM14, type-blind'),
         ('M13','D08',True ,0.0,'M13 x D08 + Mandelbaum16 type-dep'),
         ('M13','D08',False,-0.15,'M13 x D08, v3-like masses (-0.15)')]
pred_keep={}
for shmr,cM,td,dm,lab in CONFIGS:
    if dm!=0.0:
        lm3=logMs+dm; Mg3=10**lm3*(1+10**(-0.69*lm3+6.63))
        mg,mr,nw,_,_=halo_chain(shmr,cM,td,dm,Mg3)
    else:
        mg,mr,nw,_,_=(medg_p,medR_p,Nwin_p,None,None) if (shmr,cM,td)==('M13','D08',False) else halo_chain(shmr,cM,td)
    po=pred_offsets(mg)
    sl=np.polyfit(medMs,po,1)[0]
    pred_keep[lab]=(po,mg,mr)
    P(f"  {lab:<38}"+"".join(f"{o:>+8.3f}" for o in po)+" |"
      +"".join(f"{po[k]-po[0]:>+7.3f}" for k in (1,2,3))+f" |{sl:>+7.3f}")
P(f"  {'MEASURED (mean-dex)':<38}"+"".join(f"{o:>+8.3f}" for o in off_md)+" |"
  +"".join(f"{d_ref1[k]:>+7.3f}" for k in (1,2,3))+f" |{s0:>+7.3f}")
po=pred_keep['M13 x D08, type-blind (primary)'][0]
P("\npredicted vs measured bin-over-bin1 RATIOS (10^D, linear g_obs ratio at fixed g_bar):")
for k in (1,2,3):
    P(f"  bin{k+1}/bin1: predicted {10**(po[k]-po[0]):.2f}x (primary)  vs measured {10**d_ref1[k]:.2f}x "
      f"+/- {LN10*10**d_ref1[k]*e_ref1[k]:.2f}")
P("\nlinearized chain demand from the type split (agentH3: type-blind +0.119 dex across the 0.41-dex")
P(f"early-late med-M* gap -> ~+0.29 dex/dex): this dataset's 1.0-dex span demands ~+0.2..0.3 dex bin4-bin1")
P(f"if the offset is a pure function of M* through the halo chain; the direct per-bin prediction above is the")
P(f"exact version of that demand (primary D41={po[3]-po[0]:+.3f} dex).")

# =================== PART 4: the boring control (2-halo) ===================
P("\n"+"="*104)
P("PART 4 -- the 2-halo control")
P("="*104)
P("probe radii: med R (windowed, proper Mpc) per (mass bin, g_bar bin); 1-halo-safe = med R < med r200(bin):")
P(f"  {'g_bar':>9} | "+" | ".join(f"bin{k+1} R(safe)" for k in range(NB)))
safe=np.zeros((NB,n),bool)
for b in range(n):
    row=f"  {gbar[b]:>9.2e} | "
    for k in range(NB):
        safe[k,b]=medR_p[k,b]<r200med[k]
        row+=f"{medR_p[k,b]:7.3f}({'S' if safe[k,b] else '2h'}) | "
    P(row)
allsafe=np.where(safe.all(axis=0))[0]
P(f"  med r200 per bin (Mpc): {np.round(r200med,3)}; ALL-four-safe g_bar bins: {allsafe+1} (1-indexed)")

Vsafe=np.array([b for b in allsafe if b in set(V)])
off_s,S_s=offsets_meandex(gref0,Vsafe)
P(f"\n(i) 1-halo-safe subset (b in {Vsafe+1}): offsets "+", ".join(f"{o:+.3f}+/-{np.sqrt(S_s[k,k]):.3f}" for k,o in enumerate(off_s)))
ss,ess=report_slope("    1-halo-safe slope",medMs,off_s,S_s)
off_u,S_u=offsets_meandex(gref0,np.array([b for b in range(n-1) if b not in set(allsafe)]))
report_slope("    complement (2-halo-dominated bins) slope",medMs,off_u,S_u)

# ---- (ii) explicit linear-theory 2-halo estimate ----
# EH98 no-wiggle transfer (astro-ph/9709112 eqs 26,28-31), ns=0.965, sigma8-normalized; CPT growth;
# Tinker+2010 Delta=200 bias (arXiv:1001.3162 Table 2). Comoving->physical per Brouwer's proper-Mpc ESD.
ns_=0.965; sigma8=0.8; Tcmb=2.7255; th=Tcmb/2.7
om_=Om*h*h; ob_=0.0224
s_EH=44.5*np.log(9.83/om_)/np.sqrt(1+10*ob_**0.75)            # Mpc
aG=1-0.328*np.log(431*om_)*(ob_/om_)+0.38*np.log(22.3*om_)*(ob_/om_)**2
kk_=np.logspace(-4,3,6000)                                    # 1/Mpc
Geff=Om*h*(aG+(1-aG)/(1+(0.43*kk_*s_EH)**4))
q=kk_*th*th/(Geff*h)                                          # k[1/Mpc]/h / Gamma_eff
L0=np.log(2*np.e+1.8*q); C0=14.2+731.0/(1+62.5*q)
TEH=L0/(L0+C0*q*q)
D2=kk_**(3+ns_)*TEH**2*np.exp(-(kk_/500.0)**2)                # unnormalized Delta^2(k,z=0), UV-damped
lnk=np.log(kk_)
def WTH(x): return 3*(np.sin(x)-x*np.cos(x))/x**3
sig2_8=np.trapz(D2*WTH(kk_*8.0/h)**2,lnk)
D2*=sigma8**2/sig2_8
def sigma_R(R): return np.sqrt(np.trapz(D2*WTH(kk_*R)**2,lnk))
rr=np.logspace(-2,np.log10(300),400)
xi0=np.array([np.trapz(D2*np.sin(kk_*r)/(kk_*r),lnk) for r in rr])
i_r0=np.argmin(np.abs(xi0-1.0))
P(f"\n(ii) linear-theory module gates: sigma8={sigma8} (input); xi0(r)=1 at r={rr[i_r0]:.1f} Mpc "
  f"= {rr[i_r0]*h:.1f} Mpc/h [anchor ~5-6 Mpc/h]; ")
def Dgrow(zz):
    def gf(Omz,OLz): return 2.5*Omz/(Omz**(4/7)-OLz+(1+Omz/2)*(1+OLz/70))
    Omz=Om*(1+zz)**3/E2(zz); OLz=OL/E2(zz)
    return gf(Omz,OLz)/((1+zz)*gf(Om,OL))
# I(Rc) = int xi0 dchi  (comoving meters)
chi_g=np.linspace(0,100,2001)                                  # comoving Mpc
Rc_g=np.logspace(np.log10(0.005),np.log10(12),120)
I_g=np.array([2*np.trapz(np.interp(np.sqrt(Rc**2+chi_g**2),rr,xi0,right=0.0),chi_g)*Mpc for Rc in Rc_g])
Ibar=np.array([2/Rc_g[i]**2*np.trapz(I_g[:i+1]*Rc_g[:i+1],Rc_g[:i+1]) if i>0 else I_g[0] for i in range(len(Rc_g))])
def dSigma2h_phys(Rphys,zz,bias):                              # kg/m^2 (proper), at proper R [Mpc]
    Rc=Rphys*(1+zz)
    Ii=np.interp(Rc,Rc_g,I_g); Ib=np.interp(Rc,Rc_g,Ibar)
    return bias*Om*rho_c0*(1+zz)**2*Dgrow(zz)**2*(Ib-Ii)
delc=1.686; yT=np.log10(200.0)
AT=1.0+0.24*yT*np.exp(-(4/yT)**4); aT=0.44*yT-0.88; BT=0.183; bT=1.5
CT=0.019+0.107*yT+0.19*np.exp(-(4/yT)**4); cT=2.4
def tinker_bias(logMh_,zz):
    M=10**logMh_*Msun
    Rl=(3*M/(4*np.pi*Om*rho_c0))**(1/3)/Mpc                    # comoving Mpc (Lagrangian)
    nuv=delc/(sigma_R(Rl)*Dgrow(zz))
    return 1-AT*nuv**aT/(nuv**aT+delc**aT)+BT*nuv**bT+CT*nuv**cT
P(f"     b(nu=1)={1-AT/(1+1)+BT+CT:.3f}... computed b at med halo masses: "
  +", ".join(f"bin{k+1}: b({medMh[k]:.2f},z={medz[k]:.2f})={tinker_bias(medMh[k],medz[k]):.2f}" for k in range(NB)))
ds_anchor=dSigma2h_phys(1.0,0.3,1.0)/(Msun/pc**2)
P(f"     anchor: DeltaSigma_2h(R=1 Mpc proper, z=0.3, b=1) = {ds_anchor:.2f} Msun/pc^2 [expect O(1)]")

bias_k=np.array([tinker_bias(medMh[k],medz[k]) for k in range(NB)])
dg2h=np.zeros((NB,n))
for k in range(NB):
    for b in range(n):
        if np.isfinite(medR_p[k,b]):
            dg2h[k,b]=4*G*dSigma2h_phys(medR_p[k,b],medz[k],bias_k[k])
P("\n2-halo contamination delta-g/g_obs (per cent) per (mass bin, g_bar bin):")
P(f"  {'g_bar':>9} "+ " ".join(f"{'bin'+str(k+1):>7}" for k in range(NB)))
for b in range(n):
    P(f"  {gbar[b]:>9.2e} "+" ".join(f"{100*dg2h[k,b]/gobs[k,b]:>6.0f}%" if gobs[k,b]>0 else "   --  " for k in range(NB)))

# 2-halo-induced offset trend (on top of the 1-halo prediction) and corrected measured offsets
medg1=pred_keep['M13 x D08, type-blind (primary)'][1]
off2h_only=np.array([np.nanmean(np.log10((medg1[k,V]+dg2h[k,V])/medg1[k,V])) for k in range(NB)])
sl2h=np.polyfit(medMs,off2h_only,1)[0]
P(f"\n2-halo-INDUCED offset (mean over b=1..14, on top of 1-halo): "
  +", ".join(f"{o:+.3f}" for o in off2h_only)+f"  -> induced slope {sl2h:+.3f} dex/dex")
for fac,lab in ((1.0,'x1.0'),(0.5,'x0.5'),(2.0,'x2.0')):
    gcor=gobs-fac*dg2h
    okv=np.array([b for b in V if np.all(gcor[:,b]>0)])
    oc,Sc=offsets_meandex(gref0,okv,gcor)
    sc,esc=gls_line(medMs,oc,Sc)[:2]
    P(f"  2-halo-corrected measured slope ({lab} amplitude, {len(okv)} bins): {sc:+.3f} +/- {esc:.3f} "
      f"({sc/esc:+.1f} sigma); offsets "+", ".join(f"{o:+.3f}" for o in oc))

# predicted total (1-halo + 2-halo) vs measured, per bin
P("\npredicted TOTAL (1-halo + 2-halo) offsets vs measured (mean over b=1..14):")
ptot=np.array([np.nanmean(np.log10((medg1[k,V]+dg2h[k,V])/gref0[V])) for k in range(NB)])
P("  predicted total: "+", ".join(f"{o:+.3f}" for o in ptot)+f"  (slope {np.polyfit(medMs,ptot,1)[0]:+.3f})")
P("  measured       : "+", ".join(f"{o:+.3f}" for o in off_md)+f"  (slope {s0:+.3f} +/- {es0:.3f})")

# =================== VERDICT ===================
P("\n"+"="*104)
P("VERDICT INPUTS (fork locked in agentJ_massbin_phase.md)")
P("="*104)
P(f"  chain demand: fcond per bin {', '.join(f'{f:.0%}' for f in fcond)} (monotonic: {bool(np.all(np.diff(fcond)>0))}); "
  f"predicted D41={po[3]-po[0]:+.3f} dex (primary), slope {np.polyfit(medMs,po,1)[0]:+.3f} dex/dex")
P(f"  measured: offsets {np.round(off_md,3)}; slope {s0:+.3f} +/- {es0:.3f} ({s0/es0:+.1f} sigma); "
  f"monotonic point estimates: {mono}")
P(f"  bin4-bin1 measured {d_ref1[3]:+.3f} +/- {e_ref1[3]:.3f} vs chain {po[3]-po[0]:+.3f}")
P(f"  2-halo control: safe-subset slope {ss:+.3f} +/- {ess:.3f} ({ss/ess:+.1f} sigma); "
  f"2-halo-induced slope {sl2h:+.3f}")
P("  (verdict text in agentJ_massbin_phase.md -- locked wording: tests the real-lensing-mass class's phase")
P("   mechanism; does not confirm any model.)")
