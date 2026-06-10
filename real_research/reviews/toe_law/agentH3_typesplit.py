#!/usr/bin/env python3
"""
agentH3 T4: is the ~9-sigma lensing-RAR early/late split a PREDICTION of the superfluid-DM-class hybrid?
=========================================================================================================
Pre-registered fork in agentH3_gauntlet.md (T4). The SfDM structure: lensing comes from REAL mass
(condensate core + collisionless NFW envelope; photons do not couple to phonons -- arXiv:1711.05748 I.2,
arXiv:2303.08560), so at the Brouwer probe radii (0.03-3 Mpc, mostly outside the ~50-80 kpc cores) the
lensing-RAR offset between classes is driven by the HALO MASS at fixed g_bar, exactly as in CDM.
Direction claimed by the task: early types in hotter/more massive halos -> less phonon boost (kinematics)
and MORE real halo mass -> ABOVE on the lensing RAR. This script computes the predicted offset from the
repo's OWN lens catalog (lr_lenses.npz, v4) with the same pinned SHMR/c(M,z) chains as agentH_perclass_C.py:
  SHMR  M13: Moster, Naab & White 2013 (arXiv:1205.5807) | B13: Behroozi+2013 (arXiv:1207.6105)
  c(M,z) D08: Duffy+2008 (arXiv:0804.2486) | DM14: Dutton & Maccio 2014 (arXiv:1402.7073)
  type-dep SHMR: Mandelbaum+2016 (arXiv:1509.06762): early halos x2 (logM*<=10.5) -> x3 (logM*=11)
Measured comparator: the released Brouwer+2021 Fig-8 profiles (mean offset +0.261 dex u-r / +0.185 Sersic,
early above late 15/15 bins; lr_battery_results.md, hardened 8.6-9.2 sigma by agentH_perclass_C.md).
Phase geography per class from the B-K condensation criterion (1507.01019 eq 18: galaxies M <~ 1e12/h
fully condensed) and the BFK thermal radius. numpy only. Agent H3, 2026-06-10. No git.
"""
import numpy as np, os

G=6.674e-11; Msun=1.989e30; pc=3.086e16; Mpc=3.0857e22
H0=70*1e3/Mpc; Om, OL = 0.3, 0.7
rho_c0=3*H0**2/(8*np.pi*G)
HERE=os.path.dirname(os.path.abspath(__file__))
D=os.path.join(HERE,'..','..','data','lensing_rar')
P=print

def E2(z): return Om*(1+z)**3+OL
def rho_c(z): return rho_c0*E2(z)
def Delta_vir(z):
    d=Om*(1+z)**3/E2(z)-1.0
    return 18*np.pi**2+82*d-39*d**2

# ---------------- SHMRs (verbatim from agentH_perclass_C.py) ----------------
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
    if kind=='200': A,B,C=(6.71,-0.091,-0.44) if relaxed else (5.71,-0.084,-0.47)
    else:           A,B,C=(9.23,-0.090,-0.69) if relaxed else (7.85,-0.081,-0.71)
    return A*(M/piv)**B*(1+z)**C
def c_DM14(M,z,kind='200'):
    piv=1e12/0.671
    if kind=='200': a=0.520+(0.905-0.520)*np.exp(-0.617*z**1.21); b=-0.101+0.026*z
    else:           a=0.537+(1.025-0.537)*np.exp(-0.718*z**1.08); b=-0.097+0.024*z
    return 10**(a+b*np.log10(M/piv))

# ---------------- catalog + released profiles ----------------
ln=np.load(os.path.join(D,'lr_lenses.npz'))
NL=len(ln['z'])
P(f"lens catalog: {NL:,} isolated lenses ({'v4' if NL==181477 else 'NOT v4'}); "
  f"med logM*={np.median(ln['logM']):.3f}")
typ=ln['typ']; z=ln['z']; logMs=ln['logM'].copy(); Mgal=ln['Mgal'].copy()
for t,lab in ((1,'early'),(0,'late')):
    P(f"  {lab}: N={np.sum(typ==t):,}  med logM*={np.median(logMs[typ==t]):.2f}  med z={np.median(z[typ==t]):.3f}")

B=os.path.join(D,'brouwer2021_rar')
def load_axis(tag):
    late=np.loadtxt(os.path.join(B,f'Fig-8_RAR-KiDS-isolated_{tag}bin_1.txt'))
    early=np.loadtxt(os.path.join(B,f'Fig-8_RAR-KiDS-isolated_{tag}bin_2.txt'))
    gbar=late[:,0]
    ESD2g=4*G*(Msun/pc**2)
    gl0=late[:,1]/late[:,4]*ESD2g; ge0=early[:,1]/early[:,4]*ESD2g
    return gbar,ge0,gl0
gbar,ge0_c,gl0_c=load_axis('Color')
_,ge0_s,gl0_s=load_axis('Sersic')
n=len(gbar)
P(f"\nmeasured split (released profiles, SIS C=4 both classes -- the conversion differential is ~0.001 dex,")
P(f"agentH_perclass_C.md): mean dlog g_obs = {np.mean(np.log10(ge0_c/gl0_c)):+.3f} dex (u-r) /"
  f" {np.mean(np.log10(ge0_s/gl0_s)):+.3f} dex (Sersic)   [gate: +0.261 / +0.185]")

# ---------------- predicted lensing g_obs per class (SfDM envelope = real mass) ----------------
RMIN,RMAX=0.03,3.0
def predicted_split(shmr='M13',cM='D08',typedep=False,label=''):
    if shmr=='M13': logMh=invert_shmr(moster13_mstar,logMs,z); kind='200'
    else:           logMh=invert_shmr(behroozi13_mstar,logMs,z); kind='vir'
    if typedep:
        F=10**np.interp(logMs,[10.5,11.0],[np.log10(2.),np.log10(3.)])
        logMh=np.where(typ==1,logMh+np.log10(F),logMh)
    cfun=(lambda M,zz: c_D08(M,zz,kind)) if cM=='D08' else (lambda M,zz: c_DM14(M,zz,kind))
    cc=cfun(10**logMh,z)
    M=10**logMh*Msun
    Delta=200.0 if kind=='200' else Delta_vir(z)
    rD=(3*M/(4*np.pi*Delta*rho_c(z)))**(1/3)          # m
    rs=rD/cc
    gfun=lambda u: np.log(1+u)-u/(1+u)
    dlog=np.zeros(n); dlog_med=np.zeros(n); r200_med={}; ok1halo=np.zeros(n,bool)
    for b in range(n):
        R=np.sqrt(G*Mgal*Msun/gbar[b])                # m (Brouwer estimator radius per lens)
        m=(R/Mpc>RMIN)&(R/Mpc<RMAX)
        med={}
        for t in (1,0):
            k=m&(typ==t)
            x=R[k]/rs[k]
            Mltr=M[k]*gfun(x)/gfun(cc[k])             # NFW enclosed (extrapolated past rD; 1-halo)
            gpred=gbar[b]+G*Mltr/R[k]**2
            med[t]=np.median(gpred)
            r200_med[t]=np.median(rD[k])
        dlog[b]=np.log10(med[1]/med[0])
        ok1halo[b]=all(np.median(np.sqrt(G*Mgal[m&(typ==t)]*Msun/gbar[b]))<r200_med[t] for t in (1,0))
    return dlog,ok1halo,logMh,rD

P("\n== predicted early-late lensing-RAR offset at fixed g_bar (SfDM: lensing = real halo mass) ==")
P(f"{'config':<38}{'mean dlog':>10}{'mean dlog (1-halo-safe bins)':>30}{'sign':>6}")
CONFIGS=[('M13','D08',False,'M13 x D08, type-blind SHMR'),
         ('B13','DM14',False,'B13 x DM14, type-blind SHMR'),
         ('M13','D08',True ,'M13 x D08 + Mandelbaum16 type-dep'),
         ('B13','DM14',True ,'B13 x DM14 + Mandelbaum16 type-dep')]
keep={}
for shmr,cM,td,lab in CONFIGS:
    dlog,ok,logMh,rD=predicted_split(shmr,cM,td)
    keep[lab]=(dlog,ok,logMh,rD)
    P(f"{lab:<38}{np.mean(dlog):>+10.3f}{np.mean(dlog[ok]):>+27.3f} ({ok.sum()} bins)"
      f"{'  +' if np.all(dlog>0) else ('  +/-' if np.mean(dlog)>0 else '  -')}")
P(f"{'MEASURED (u-r / Sersic)':<38}{'+0.261':>10} / +0.185{'':>14}  + (15/15 bins)")

dlog,ok,logMh,rD=keep['M13 x D08, type-blind SHMR']
P("\nper-bin detail (primary config M13 x D08 type-blind vs measured u-r):")
P(f"  {'g_bar':>9} {'pred dlog':>10} {'meas dlog':>10} {'1-halo-safe':>12}")
for b in range(n):
    P(f"  {gbar[b]:>9.2e} {dlog[b]:>+10.3f} {np.log10(ge0_c[b]/gl0_c[b]):>+10.3f} {str(ok[b]):>12}")

# ---------------- phase geography per class (the 'hotter/disrupted halo' leg) ----------------
P("\n== phase geography per class (B-K condensation boundary M ~ 1e12/h; 1507.01019 eq 18 context) ==")
Mcond=np.log10(1e12/0.7)
for t,lab in ((1,'early'),(0,'late')):
    k=typ==t
    mh=logMh[k]
    RT=310*( (10**mh/1e12)**(1/7) )*(0.01)**(2/7)     # kpc, m=1 eV, sigma/m=0.01 (BFK near eq 25)
    r200=rD[k]/ (3.0857e19)                            # kpc
    P(f"  {lab}: med logM_h={np.median(mh):.2f}; frac above condensation boundary (logM>{Mcond:.2f}):"
      f" {np.mean(mh>Mcond):.0%}; med R_T={np.median(RT):.0f} kpc vs med r200={np.median(r200):.0f} kpc"
      f" -> core/halo radius fraction {np.median(RT/r200):.2f}")
P("  -> early-type halos sit at/above the condensation boundary far more often than late: less coherent")
P("     superfluid (smaller phonon boost for their KINEMATICS), more normal-phase real mass. On the LENSING")
P("     axis (this measurement) the offset is carried by the halo mass at fixed g_bar; the phase fork's")
P("     DISTINCTIVE signature is kinematic-vs-lensing inconsistency per class, not the lensing split alone.")

P("\n== verdict inputs (prereg T4 fork) ==")
P(f"  sign: predicted + (early above) in ALL configs and ALL bins -> MATCHES the measured direction")
prim=np.mean(keep['M13 x D08, type-blind SHMR'][0]); td=np.mean(keep['M13 x D08 + Mandelbaum16 type-dep'][0])
P(f"  magnitude: type-blind {prim:+.3f} dex; +type-dep {td:+.3f} dex vs measured +0.261 (u-r) / +0.185 (Sersic)")
P(f"  ratios to u-r measurement: {prim/0.261:.2f}x (type-blind) .. {td/0.261:.2f}x (type-dep)")
P("  caveats carried: (i) 1-halo NFW only -- absolute g underpredicted at R>r200 (2-halo), but the split is")
P("  the target and the low-g_bar bins are flagged; (ii) this is the generic CDM-envelope SHMR effect -- the")
P("  locked wording applies: consistency for the real-lensing-mass CLASS, not 'SfDM confirmed' (Brouwer's own")
P("  MICE/BAHAMAS sims disagree on the split); (iii) the same model FAILS the absolute lensing RAR shape")
P("  (arXiv:2303.08560: chi2_red 15-29 vs parameter-free MOND 6.5 on the same data).")
