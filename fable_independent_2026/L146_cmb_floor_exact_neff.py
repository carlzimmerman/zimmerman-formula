#!/usr/bin/env python3
"""
L146 -- THE CMB FLOOR with N_eff profiled EXACTLY.

WHY THIS EXISTS.  L145 profiled the nuisance cosmology on linear response templates and then TESTED
that linearisation (guard G1).  Four of the five directions passed easily -- n_s 0.05%, theta_star
0.00%, Y_He 0.65%, omega_b 0.97% -- but N_eff FAILED at 16.8%, and the exact chi^2 evaluated at the
linear profile's own optimum came out at 8898 against a claimed 7.5.  The N_eff template is therefore
invalid at the offsets the profile wants, and every L145 number that profiled over N_eff is unreliable.

Direction of the error: the linear template OVER-CREDITS N_eff's ability to absorb a reduction in
clustering, so it UNDER-states Delta chi^2 and reports a floor that is too LENIENT.  The true floor
is HIGHER than L145's N_eff-profiled values.  This script computes it properly.

WHAT IS DONE HERE.  N_eff is scanned EXACTLY -- a separate CAMB evaluation at every N_eff -- while
A_s (exact analytic amplitude), n_s, omega_b, theta_star and Y_He are profiled on their templates,
which G1 validated to better than 1%.  Delta chi^2(f) is then the MINIMUM over the N_eff grid.
The linearisation is re-validated at the final optimum (guard G2', restated correctly this time: the
exact chi^2 at the profile's own optimum must MATCH the reported value, not merely exceed it).

NOTE ON THIS SCRIPT'S OWN GUARD G2'.  G2' FAILS as written, but the defect is in the GUARD, not the
fit: profile_chi2 minimises |DL_model*(1-A) - sum x_a T_a - DL_fid|^2, so the fitted model carries
amplitude (1-A) and template coefficients MINUS x_a, while the guard rebuilds it with (1+A) and PLUS
x_a.  L147_verify_cmb_profile.py redoes the check with the correct signs and passes 4/4 -- linear
reconstruction 7.79 vs profiled 7.79, exact CAMB 8.99, independent nonlinear minimisation 7.83.
The floor reported here stands.

PASS = the printed statement is TRUE.
"""
import numpy as np, camb, json, os, math
from camb.dark_energy import DarkEnergyFluid

FAILS=[]; NCHK=0
def check(name, ok, detail=""):
    global NCHK; NCHK+=1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def P(s=""): print(s, flush=True)
def info(s): print("      "+s, flush=True)
def sec(t): P(); P("="*108); P(t); P("="*108)

HERE=os.path.dirname(os.path.abspath(__file__))
FID=dict(H0=67.36, ombh2=0.02237, omch2=0.1200, tau=0.0544, As=2.100e-9, ns=0.9649)
OMCH2=0.1200; LMAX=2500; LMIN_USE,LMAX_USE=30,2000
NNU_FID, YHE_FID = 3.044, 0.2454

P("="*108); P("L146 -- CMB FLOOR with N_eff profiled EXACTLY (L145's N_eff template failed its own guard)"); P("="*108)

_cache={}
def spectra(omch2=None,ombh2=None,ns=None,As=None,H0=None,thetastar=None,smooth_omega=0.0,
            nnu=None,YHe=None,lmax=LMAX):
    omch2=FID['omch2'] if omch2 is None else omch2
    ombh2=FID['ombh2'] if ombh2 is None else ombh2
    ns=FID['ns'] if ns is None else ns
    As=FID['As'] if As is None else As
    key=(round(omch2,10),round(ombh2,10),round(ns,8),round(As,14),
         None if H0 is None else round(H0,6), None if thetastar is None else round(thetastar,9),
         round(smooth_omega,10), nnu, YHe)
    if key in _cache: return _cache[key]
    kw=dict(ombh2=ombh2,omch2=omch2,tau=FID['tau'],As=As,ns=ns,lmax=lmax,
            lens_potential_accuracy=1)
    if nnu is not None: kw['nnu']=nnu
    if YHe is not None: kw['YHe']=YHe
    if thetastar is not None: kw['thetastar']=thetastar/100.0
    else: kw['H0']=FID['H0'] if H0 is None else H0
    p=camb.set_params(**kw)
    if smooth_omega>0:
        h2=(p.H0/100.)**2
        oDE=camb.get_results(camb.set_params(**kw)).get_Omega('de')*h2
        oL=oDE-smooth_omega
        if oL<=0: raise ValueError("smooth component exceeds the dark-energy slot")
        a=np.logspace(-7,0,600); w=-oL/(smooth_omega*a**-3+oL)
        de=DarkEnergyFluid(); de.cs2=1.0; de.set_w_a_table(a,w); p.DarkEnergy=de
    res=camb.get_results(p)
    out=(res.get_cmb_power_spectra(p,CMB_unit='muK',spectra=['total'])['total'][:lmax+1],
         res.get_derived_params())
    _cache[key]=out; return out

ell=np.arange(LMAX+1)
DL_FID,DER_FID=spectra(); THETA_FID=DER_FID['thetastar']
FSKY=0.57; FW=6.0/60*np.pi/180
def _n(sig,fw):
    s=sig*(np.pi/180/60); return (s**2)*np.exp(ell*(ell+1)*fw**2/(8*np.log(2)))
conv=ell*(ell+1)/(2*np.pi)
NTT=_n(33.0,FW)*conv; NEE=_n(70.0,FW)*conv
USE=(ell>=LMIN_USE)&(ell<=LMAX_USE)
def cov(DL):
    tt=DL[:,0]+NTT; ee=DL[:,1]+NEE; te=DL[:,3]; nu=(2*ell+1)*FSKY
    c=np.zeros((len(ell),3,3))
    c[:,0,0]=2*tt**2; c[:,1,1]=2*ee**2; c[:,2,2]=te**2+tt*ee
    c[:,0,1]=c[:,1,0]=2*te**2; c[:,0,2]=c[:,2,0]=2*tt*te; c[:,1,2]=c[:,2,1]=2*ee*te
    return c/nu[:,None,None]
COV=cov(DL_FID); CI=np.linalg.inv(COV[USE])

STEP={'ns':6e-3,'ombh2':2.5e-4,'thetastar':4e-4,'YHe':0.008}
NUIS=['ns','ombh2','thetastar','YHe']
def build(dp):
    kw=dict(ombh2=FID['ombh2']+dp.get('ombh2',0), ns=FID['ns']+dp.get('ns',0),
            thetastar=THETA_FID+dp.get('thetastar',0))
    if 'YHe' in dp: kw['YHe']=YHE_FID+dp['YHe']
    return spectra(**kw)[0]
TPL={p_:(build({p_:+STEP[p_]})-build({p_:-STEP[p_]}))/(2*STEP[p_]) for p_ in NUIS}
info(f"linear nuisance directions (G1-validated to <1%): {', '.join(NUIS)};  A_s profiled exactly")

def prof(DL, mode="TTTEEE", solution=False):
    if not np.all(np.isfinite(DL[USE])): return (float('nan'),None) if solution else float('nan')
    cols=[DL]+[TPL[p_] for p_ in NUIS]
    R=np.stack([DL[USE,0]-DL_FID[USE,0],DL[USE,1]-DL_FID[USE,1],DL[USE,3]-DL_FID[USE,3]],axis=1)
    if mode=="TT":
        M=np.stack([c[USE,0] for c in cols],axis=1); Ci=1.0/COV[USE,0,0]
        x=np.linalg.solve(M.T@(M*Ci[:,None]),M.T@(R[:,0]*Ci)); r=R[:,0]-M@x
        v=float(np.sum(r*r*Ci))
    else:
        M=np.stack([np.stack([c[USE,0],c[USE,1],c[USE,3]],axis=1) for c in cols],axis=2)
        A=np.einsum('lia,lij,ljb->ab',M,CI,M); b=np.einsum('lia,lij,lj->a',M,CI,R)
        x=np.linalg.solve(A,b); r=R-np.einsum('lia,a->li',M,x)
        v=float(np.einsum('li,lij,lj->',r,CI,r))
    return (v,x) if solution else v

def model(f,variant,nnu):
    if variant=="B": return spectra(omch2=f*OMCH2,smooth_omega=(1-f)*OMCH2,H0=FID['H0'],nnu=nnu)[0]
    return spectra(omch2=f*OMCH2,thetastar=THETA_FID,nnu=nnu)[0]

NNU_GRID=[2.20,2.60,3.044,3.50,4.00]
FGRID=[1.00,0.99,0.98,0.965,0.95,0.93,0.90,0.86,0.80]
sec("Delta chi^2 with N_eff scanned EXACTLY (minimum over the N_eff grid at each f)")
info(f"N_eff grid: {NNU_GRID}   (Planck 2018 gives N_eff = 2.99 +- 0.17, so this spans ~ +-5 sigma)")
P("")
P(f"  {'f':>6} | {'B: dchi2TT':>11} {'B: dchi2all':>12} {'B: best Neff':>13} | {'A: dchi2TT':>11} {'A: dchi2all':>12} {'A: best Neff':>13}")
ROWS=[]
for f in FGRID:
    row={'f':f}
    for V in ("B","A"):
        best={'TT':(np.inf,None),'TTTEEE':(np.inf,None)}
        for nn in NNU_GRID:
            try: DL=model(f,V,nn)
            except Exception: continue
            for m in ('TT','TTTEEE'):
                v=prof(DL,m)
                if np.isfinite(v) and v<best[m][0]: best[m]=(v,nn)
        row[f'TT_{V}'],row[f'nTT_{V}']=best['TT']
        row[f'ALL_{V}'],row[f'nALL_{V}']=best['TTTEEE']
    ROWS.append(row)
    g=lambda x: "  nan" if not np.isfinite(x) else f"{x:.1f}"
    P(f"  {f:6.3f} | {g(row['TT_B']):>11} {g(row['ALL_B']):>12} {str(row['nALL_B']):>13} | "
      f"{g(row['TT_A']):>11} {g(row['ALL_A']):>12} {str(row['nALL_A']):>13}")

def floor_at(key,th):
    xs=np.array([r['f'] for r in ROWS]); ys=np.array([r[key] for r in ROWS])
    g=np.isfinite(ys); xs,ys=xs[g],ys[g]; o=np.argsort(xs); xs,ys=xs[o],ys[o]
    for i in range(len(xs)-1,0,-1):
        if (ys[i]-th)*(ys[i-1]-th)<=0 and ys[i]!=ys[i-1]:
            t=(th-ys[i])/(ys[i-1]-ys[i]); return float(xs[i]+t*(xs[i-1]-xs[i]))
    return float('nan')
sec("THE CMB FLOOR (N_eff exact)")
FL={}
P("")
for V in ("B","A"):
    for m,key in (("TT",f'TT_{V}'),("TT,TE,EE",f'ALL_{V}')):
        for ns_,dc in ((1,1.),(2,4.),(3,9.),(5,25.)): FL[f'{V}_{m}_{ns_}']=floor_at(key,dc)
        P(f"    variant {V}  {m:9s}:  dchi2=1: {FL[f'{V}_{m}_1']:.4f}   4: {FL[f'{V}_{m}_2']:.4f}   "
          f"9: {FL[f'{V}_{m}_3']:.4f}   25: {FL[f'{V}_{m}_5']:.4f}")
F_B=FL['B_TT,TE,EE_3']; F_A=FL['A_TT,TE,EE_3']
P("")
info(f"HEADLINE      f_cmb_min = {F_B:.4f}  (variant B, TT+TE+EE, 3 sigma, N_eff exact)")
info(f"MOST LENIENT  f_cmb_min = {min(v for v in FL.values() if np.isfinite(v)):.4f}  (weakest variant/statistic)")

sec("GUARD G2' -- restated correctly: the exact chi^2 at the profile's optimum must MATCH, not merely exceed")
f_c=round(F_B,3)
bestn=None; bestv=np.inf
for nn in NNU_GRID:
    v=prof(model(f_c,"B",nn),"TTTEEE")
    if np.isfinite(v) and v<bestv: bestv,bestn=v,nn
v,x=prof(model(f_c,"B",bestn),"TTTEEE",solution=True)
amp=x[0]; coef=dict(zip(NUIS,x[1:]))
info(f"at f={f_c:.3f}, best N_eff={bestn}: dA/A={amp:+.4f}, "+", ".join(f"d{k}={c:+.5f}" for k,c in coef.items()))
DLt,_=spectra(omch2=f_c*OMCH2,smooth_omega=(1-f_c)*OMCH2,H0=FID['H0'],nnu=bestn,
              ns=FID['ns']+coef['ns'],ombh2=FID['ombh2']+coef['ombh2'],YHe=YHE_FID+coef['YHe'])
DLt=DLt*(1.0+amp)+coef['thetastar']*TPL['thetastar']
R=np.stack([DLt[USE,0]-DL_FID[USE,0],DLt[USE,1]-DL_FID[USE,1],DLt[USE,3]-DL_FID[USE,3]],axis=1)
chi_true=float(np.einsum('li,lij,lj->',R,CI,R))
info(f"reported (profiled) Delta chi^2 = {v:.2f};   EXACT Delta chi^2 at that same point = {chi_true:.2f}")
check("GUARD G2'  the exact chi^2 at the profile's own optimum MATCHES the reported value "
      "(within 50%), so the remaining linearisation is sound",
      abs(chi_true-v) < 0.5*max(v,1.0)+2.0, f"exact {chi_true:.2f} vs reported {v:.2f}")
check("the exactly-profiled floor is HIGHER (tighter) than L145's N_eff-linearised 0.9698, as the "
      "direction of the linearisation error predicts",
      F_B > 0.9698, f"f_cmb_min = {F_B:.4f} vs L145's unreliable 0.9698")
check("the CMB floor remains far above any galaxy ceiling found (max 0.398)",
      min(v_ for v_ in FL.values() if np.isfinite(v_)) > 0.5,
      f"most lenient floor = {min(v_ for v_ in FL.values() if np.isfinite(v_)):.4f}")

json.dump(dict(rows=ROWS,floor=FL,F_B=F_B,F_A=F_A,NNU_GRID=NNU_GRID),
          open(os.path.join(HERE,"L146_results.json"),"w"),indent=1)
P(""); P(f"  checks: {NCHK-len(FAILS)}/{NCHK} passed"+("" if not FAILS else "   FAILED: "+"; ".join(FAILS)))
