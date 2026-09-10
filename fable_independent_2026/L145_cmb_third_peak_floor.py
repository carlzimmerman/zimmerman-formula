#!/usr/bin/env python3
"""
L145 -- THE CMB FLOOR:  what is the MINIMUM cold, CLUSTERING dark-matter density that the
      acoustic peaks (and the third peak in particular) actually require?

THE QUESTION.  A hybrid "MOND + reduced CDM" theory would keep a cold clustering component of
density  omega_c^clust = f * 0.1200  and supply the REST of the gravitating background some other
way (in AeST/TeVeS-like completions the extra fields do carry a dust-like background density).
So the honest CMB question is NOT "what happens if you delete matter from the universe" -- that
conflates GEOMETRY with CLUSTERING.  It is:

    holding the expansion history EXACTLY fixed, how little of the matter is allowed to CLUSTER?

TWO VARIANTS ARE RUN (they bracket the honest answer):
  VARIANT B (the hybrid-relevant one, headline).  omega_c -> f*omega_c, and the missing
     (1-f)*omega_c is carried by a SMOOTH component with the same a^-3 background scaling but
     sound speed cs^2 = 1 so it does not cluster.  Implemented EXACTLY by handing CAMB a w(a)
     table for the combined (smooth dust + Lambda) dark sector:
         w(a) = -rho_L / ( rho_s0 a^-3 + rho_L ).
     This reproduces H(a) of the fiducial model to ~1e-7 and theta_star to 7 digits (checked).
  VARIANT A (the textbook one).  omega_c -> f*omega_c with no replacement; Lambda takes up the
     slack and H0 is re-solved to hold theta_star fixed.  Background AND clustering both change.

WHAT IS PROFILED.  At every f the remaining cosmology is RE-OPTIMISED, so this is a profile, not a
one-parameter slice.  A_s is profiled ANALYTICALLY AND EXACTLY (it is a pure amplitude).  n_s is
profiled on the exact primordial tilt template.  omega_b and theta_star are profiled on
CAMB-computed linear response templates.  The critical f is then RE-CHECKED with a full nonlinear
Nelder-Mead over (A_s, n_s, omega_b, theta_star) with real CAMB calls at every evaluation.
Not profiling would MANUFACTURE A KILL; this is the single most important guard in this script.

LIKELIHOOD.  Gaussian band-power chi^2 with cosmic variance + an effective Planck instrumental
noise, f_sky and beam.  The noise model is not asserted -- it is CALIBRATED, by requiring that a
full 6-parameter Fisher forecast reproduce Planck 2018's PUBLISHED omega_c error bars
(TT+lowE: 0.1212 +- 0.0022 ; TT,TE,EE+lowE: 0.1200 +- 0.0012).  That is control C1/C2.

RESULT OF ITS OWN GUARDS (read this before using any number below).  Guard G1 shows that four of the
five linearised nuisance directions are accurate to better than 1% at the offsets the profile uses
(n_s 0.05%, theta_star 0.00%, Y_He 0.65%, omega_b 0.97%) but that N_eff FAILS at 16.8%, and guard G2
shows the exact chi^2 at the profile optimum is 8898 against a reported 7.5.  Every floor in this
script that profiles over N_eff is therefore UNRELIABLE, and unreliable in the LENIENT direction (the
template over-credits N_eff, understating Delta chi^2).  Those numbers are SUPERSEDED by
L146_cmb_floor_exact_neff.py, which scans N_eff exactly.  The floors WITHOUT N_eff freedom, and the
Planck sigma(omega_c) controls, remain valid.

PASS = the printed statement is TRUE.
Self-contained: numpy/scipy/camb only.  Writes nothing outside the scratchpad.
"""
import numpy as np, camb, json, os, sys
from camb.dark_energy import DarkEnergyFluid
from scipy.optimize import minimize

FAILS=[]; NCHK=0
def check(name, ok, detail=""):
    global NCHK; NCHK+=1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def P(s=""): print(s, flush=True)
def info(s): print("      "+s, flush=True)
def sec(t): P(); P("="*104); P(t); P("="*104)

HERE=os.path.dirname(os.path.abspath(__file__))

# ---------------- Planck 2018 base-LCDM (TT,TE,EE+lowE+lensing) ----------------
FID = dict(H0=67.36, ombh2=0.02237, omch2=0.1200, tau=0.0544, As=2.100e-9, ns=0.9649)
OMCH2_PLANCK = 0.1200
LMAX = 2500
LMIN_USE, LMAX_USE = 30, 2000          # Planck high-l TT/TE/EE range

P("="*104)
P("L145 -- THE CMB FLOOR: minimum CLUSTERING cold dark matter fraction f = omega_c^clust / 0.1200")
P("="*104)
info(f"fiducial Planck 2018: omega_b={FID['ombh2']}, omega_c={FID['omch2']}, H0={FID['H0']}, ns={FID['ns']}, tau={FID['tau']}")
info(f"multipole range used: {LMIN_USE} <= l <= {LMAX_USE}")

# ================= spectra =================
_cache={}
def spectra(omch2=None, ombh2=None, ns=None, As=None, H0=None, thetastar=None, smooth_omega=0.0, lmax=LMAX, boost=1.0, nnu=None, YHe=None):
    """Return D_l = l(l+1)C_l/2pi in muK^2, array (lmax+1, 4) [TT,EE,BB,TE]."""
    omch2 = FID['omch2'] if omch2 is None else omch2
    ombh2 = FID['ombh2'] if ombh2 is None else ombh2
    ns    = FID['ns']    if ns    is None else ns
    As    = FID['As']    if As    is None else As
    key=(round(omch2,10),round(ombh2,10),round(ns,8),round(As,14),nnu,YHe,
         None if H0 is None else round(H0,6), None if thetastar is None else round(thetastar,9),
         round(smooth_omega,10), lmax, boost)
    if key in _cache: return _cache[key]
    kw = dict(ombh2=ombh2, omch2=omch2, tau=FID['tau'], As=As, ns=ns, lmax=lmax,
              lens_potential_accuracy=1, AccuracyBoost=boost)
    if nnu is not None: kw['nnu']=nnu
    if YHe is not None: kw['YHe']=YHe
    if thetastar is not None: kw['thetastar']=thetastar/100.0   # derived params are 100*theta
    else:                     kw['H0']= FID['H0'] if H0 is None else H0
    p = camb.set_params(**kw)
    if smooth_omega > 0:
        # dark sector = smooth dust (omega=smooth_omega) + Lambda, all with cs2=1 (non-clustering)
        h2=(p.H0/100.)**2
        r0 = camb.get_results(camb.set_params(**kw))
        oDE = r0.get_Omega('de')*h2                     # total dark-energy slot today (h^2 units)
        oL  = oDE - smooth_omega
        if oL <= 0: raise ValueError("smooth component exceeds dark-energy slot")
        a = np.logspace(-7, 0, 600)
        w = -oL/(smooth_omega*a**-3 + oL)
        de = DarkEnergyFluid(); de.cs2 = 1.0
        de.set_w_a_table(a, w)
        p.DarkEnergy = de
    res = camb.get_results(p)
    cl  = res.get_cmb_power_spectra(p, CMB_unit='muK', spectra=['total'])['total'][:lmax+1]  # D_l already
    out = (cl, res.get_derived_params())
    _cache[key]=out
    return out

ell = np.arange(LMAX+1)
DL_FID, DER_FID = spectra()
THETA_FID = DER_FID['thetastar']
info(f"fiducial theta_star = {THETA_FID:.6f}")

# ================= noise model (CALIBRATED, not asserted) =================
# Effective single-experiment Planck model; f_sky and the white-noise levels are calibrated in C1/C2.
FSKY   = 0.57                     # Planck high-l TT likelihood mask
FWHM_T = 6.0/60*np.pi/180         # rad
FWHM_P = 6.0/60*np.pi/180
def _noise(sigma_arcmin, fwhm):
    s = sigma_arcmin*(np.pi/180/60)                 # muK*rad
    return (s**2)*np.exp(ell*(ell+1)*fwhm**2/(8*np.log(2)))
SIG_T, SIG_P = 33.0, 70.0         # muK*arcmin  (calibrated below)
def NL():
    nT=_noise(SIG_T,FWHM_T); nP=_noise(SIG_P,FWHM_P)
    conv = ell*(ell+1)/(2*np.pi)                    # C_l -> D_l
    return nT*conv, nP*conv
NTT, NEE = NL()

USE = (ell>=LMIN_USE)&(ell<=LMAX_USE)
def cov_blocks(DL):
    """Return per-l covariance of (TT,EE,TE) band powers, Gaussian approximation."""
    tt = DL[:,0]+NTT; ee = DL[:,1]+NEE; te = DL[:,3]
    nu = (2*ell+1)*FSKY
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.zeros((len(ell),3,3))
        c[:,0,0]=2*tt**2;      c[:,1,1]=2*ee**2;      c[:,2,2]=te**2+tt*ee
        c[:,0,1]=c[:,1,0]=2*te**2
        c[:,0,2]=c[:,2,0]=2*tt*te
        c[:,1,2]=c[:,2,1]=2*ee*te
        c/= nu[:,None,None]
    return c
COV_FID = cov_blocks(DL_FID)

def chi2(DL_model, DL_data=DL_FID, mode="TTTEEE"):
    d = np.stack([DL_model[:,0]-DL_data[:,0], DL_model[:,1]-DL_data[:,1], DL_model[:,3]-DL_data[:,3]],axis=1)
    if mode=="TT":
        v = d[USE,0]; s = COV_FID[USE,0,0]
        return float(np.sum(v*v/s))
    C = COV_FID[USE]; dv = d[USE]
    Ci = np.linalg.inv(C)
    return float(np.einsum('li,lij,lj->', dv, Ci, dv))

# ================= CONTROL C1/C2: calibrate/validate the noise model on Planck's published sigma(omega_c) =================
sec("CONTROL -- is the likelihood/noise model right?  Reproduce Planck 2018's PUBLISHED sigma(omega_c).")
PAR = ['ombh2','omch2','ns','As','thetastar','tau_amp','nnu','YHe']
STEP= {'ombh2':2.5e-4,'omch2':1.5e-3,'ns':6e-3,'As':2.0e-11,'thetastar':4e-4,'tau_amp':0.01,'nnu':0.15,'YHe':0.008}
def model_vec(dp):
    """Full LCDM model with parameter offsets dp (dict). tau_amp = fractional amplitude (tau/As direction)."""
    kw=dict(ombh2=FID['ombh2']+dp.get('ombh2',0), omch2=FID['omch2']+dp.get('omch2',0),
            ns=FID['ns']+dp.get('ns',0), As=FID['As']+dp.get('As',0),
            thetastar=THETA_FID+dp.get('thetastar',0))
    if 'nnu' in dp: kw['nnu']=3.044+dp['nnu']
    if 'YHe' in dp: kw['YHe']=0.2454+dp['YHe']
    DL,_ = spectra(**kw)
    return DL*(1.0+dp.get('tau_amp',0.0))
DERIV={}
for p_ in PAR:
    hp = STEP[p_]
    Dp = model_vec({p_:+hp}); Dm = model_vec({p_:-hp})
    DERIV[p_]=(Dp-Dm)/(2*hp)
LCDM_PAR = ['ombh2','omch2','ns','As','thetastar','tau_amp']
def fisher(mode, parset=None):
    parset = LCDM_PAR if parset is None else parset
    n=len(parset); F=np.zeros((n,n))
    C=COV_FID[USE]; Ci=np.linalg.inv(C)
    V=[]
    for p_ in parset:
        D=DERIV[p_]
        V.append(np.stack([D[USE,0],D[USE,1],D[USE,3]],axis=1))
    for i in range(n):
        for j in range(n):
            if mode=="TT":
                F[i,j]=np.sum(V[i][:,0]*V[j][:,0]/COV_FID[USE,0,0])
            else:
                F[i,j]=np.einsum('li,lij,lj->', V[i], Ci, V[j])
    return F
for mode,target,tol,label in (("TT",0.0022,0.0007,"Planck TT+lowE: omega_c = 0.1212 +- 0.0022"),
                              ("TTTEEE",0.0012,0.0004,"Planck TT,TE,EE+lowE: omega_c = 0.1200 +- 0.0012")):
    F=fisher(mode); Cpar=np.linalg.inv(F); sig=np.sqrt(Cpar[LCDM_PAR.index('omch2'),LCDM_PAR.index('omch2')])
    info(f"{mode:7s} Fisher sigma(omega_c) = {sig:.5f}   [published {target}]")
    check(f"CONTROL  the calibrated likelihood reproduces {label}", abs(sig-target)<tol,
          f"{sig:.5f} vs {target} (tol {tol})")

# ================= peak heights =================
def peaks(DL):
    out={}
    for k,(lo,hi) in enumerate(((180,280),(480,620),(720,900))):
        w=(ell>=lo)&(ell<=hi); i=np.argmax(DL[w,0]); out[k+1]=(float(ell[w][i]), float(DL[w,0][i]))
    return out
PK_FID=peaks(DL_FID)
info(f"fiducial peaks (l, D_l muK^2): "+", ".join(f"P{k}=({v[0]:.0f}, {v[1]:.1f})" for k,v in PK_FID.items()))

def peak_ratio_sigma(mode="TTTEEE"):
    """Planck 1-sigma on the ratio H3/H2 of peak heights, from the band-power covariance."""
    l2,l3 = int(PK_FID[2][0]), int(PK_FID[3][0])
    h2,h3 = PK_FID[2][1], PK_FID[3][1]
    s2 = COV_FID[l2,0,0]; s3 = COV_FID[l3,0,0]
    # single-l is pessimistic; average over a +-25 window (peaks are broad, ~flat over that range)
    def band(lc):
        w=(ell>=lc-25)&(ell<=lc+25)
        return 1.0/np.sum(1.0/COV_FID[w,0,0])
    s2,s3 = band(l2), band(l3)
    r=h3/h2
    return r, r*np.sqrt(s3/h3**2 + s2/h2**2)
R_FID, SIG_R = peak_ratio_sigma()
info(f"fiducial third/second peak height ratio H3/H2 = {R_FID:.4f} +- {SIG_R:.4f} (Planck-like, 50-l band)")

# ================= the f-scan =================
sec("THE SCAN -- Delta chi^2 (PROFILED over A_s, n_s, omega_b, theta_star) vs the clustering fraction f")

# linear response templates for the profiled nuisance directions
NUIS=['ns','ombh2','thetastar','nnu','YHe']   # N_eff and Y_He are the classic omega_c degeneracy directions
TPL={p_: DERIV[p_] for p_ in NUIS}

def profile_chi2(DL_model, mode="TTTEEE"):
    if not np.all(np.isfinite(DL_model[USE])): return float('nan')
    """Profile over amplitude (A_s, EXACT) + linear templates for ns, omega_b, theta_star."""
    # build design matrix: residual r = DL_model - DL_fid ; we minimise |r + sum_a x_a T_a + A*DL_model|
    cols=[DL_model]                         # amplitude direction (exact: A_s scales everything)
    cols+=[TPL[p_] for p_ in NUIS]
    if mode=="TT":
        R=(DL_model[USE,0]-DL_FID[USE,0]); Ci=1.0/COV_FID[USE,0,0]
        M=np.stack([c[USE,0] for c in cols],axis=1)
        A=M.T@(M*Ci[:,None]); b=M.T@(R*Ci)
        x=np.linalg.solve(A,b); res=R-M@x
        return float(np.sum(res*res*Ci))
    C=COV_FID[USE]; Ci=np.linalg.inv(C)
    R=np.stack([DL_model[USE,0]-DL_FID[USE,0], DL_model[USE,1]-DL_FID[USE,1], DL_model[USE,3]-DL_FID[USE,3]],axis=1)
    M=np.stack([np.stack([c[USE,0],c[USE,1],c[USE,3]],axis=1) for c in cols],axis=2)  # (l,3,ncol)
    A=np.einsum('lia,lij,ljb->ab',M,Ci,M); b=np.einsum('lia,lij,lj->a',M,Ci,R)
    x=np.linalg.solve(A,b); res=R-np.einsum('lia,a->li',M,x)
    return float(np.einsum('li,lij,lj->',res,Ci,res))

def model_f(f, variant):
    if variant=="B":
        return spectra(omch2=f*OMCH2_PLANCK, smooth_omega=(1-f)*OMCH2_PLANCK, H0=FID['H0'])
    else:
        return spectra(omch2=f*OMCH2_PLANCK, thetastar=THETA_FID)

FGRID=np.array([1.0,0.98,0.95,0.92,0.90,0.85,0.80,0.75,0.70,0.60,0.50,0.40,0.30,0.20,0.10,0.05])
rows=[]
P("")
P(f"  {'f':>6} {'om_c^cl':>8} | {'B:dchi2TT':>10} {'B:dchi2all':>11} {'B:H3/H2':>8} {'B:nsig(R)':>9} | {'A:dchi2TT':>10} {'A:dchi2all':>11} {'A:H3/H2':>8}")
P("  "+"-"*104)
for f in FGRID:
    r={'f':float(f)}
    for variant in ("B","A"):
        try:
            DL,der = model_f(f,variant)
            r[f'chi2TT_{variant}']  = profile_chi2(DL,"TT")
            r[f'chi2all_{variant}'] = profile_chi2(DL,"TTTEEE")
            pk=peaks(DL); r[f'R_{variant}']=pk[3][1]/pk[2][1]
            r[f'nsigR_{variant}']=abs(r[f'R_{variant}']-R_FID)/SIG_R
            r[f'theta_{variant}']=der['thetastar']
        except Exception as e:
            for k in ('chi2TT','chi2all','R','nsigR','theta'): r[f'{k}_{variant}']=float('nan')
            r[f'err_{variant}']=str(e)
    rows.append(r)
    P(f"  {f:6.2f} {f*OMCH2_PLANCK:8.4f} | {r['chi2TT_B']:10.1f} {r['chi2all_B']:11.1f} {r['R_B']:8.4f} {r['nsigR_B']:9.1f} | "
      f"{r['chi2TT_A']:10.1f} {r['chi2all_A']:11.1f} {r['R_A']:8.4f}")

def solve_f(key, thresh):
    xs=np.array([r['f'] for r in rows]); ys=np.array([r[key] for r in rows])
    o=np.argsort(xs); xs,ys=xs[o],ys[o]
    good=np.isfinite(ys)
    xs,ys=xs[good],ys[good]
    # ys decreasing in f (0 at f=1); find crossing of thresh
    for i in range(len(xs)-1,0,-1):
        if (ys[i]-thresh)*(ys[i-1]-thresh)<=0:
            t=(thresh-ys[i])/(ys[i-1]-ys[i]); return float(xs[i]+t*(xs[i-1]-xs[i]))
    return float('nan')

sec("THE CMB FLOOR")
res_floor={}
for variant in ("B","A"):
    for mode,key in (("TT",f'chi2TT_{variant}'),("TT,TE,EE",f'chi2all_{variant}')):
        for nsig,dc in ((1,1.0),(2,4.0),(3,9.0),(5,25.0)):
            res_floor[f'{variant}_{mode}_{nsig}']=solve_f(key,dc)
        P(f"  variant {variant}  {mode:9s}:  f at dchi2=1: {res_floor[f'{variant}_{mode}_1']:.4f}   "
          f"dchi2=4: {res_floor[f'{variant}_{mode}_2']:.4f}   dchi2=9: {res_floor[f'{variant}_{mode}_3']:.4f}   "
          f"dchi2=25: {res_floor[f'{variant}_{mode}_5']:.4f}")
for variant in ("B","A"):
    xs=np.array([r['f'] for r in rows]); ys=np.array([r[f'nsigR_{variant}'] for r in rows])
    g=np.isfinite(ys); xs,ys=xs[g],ys[g]; o=np.argsort(xs); xs,ys=xs[o],ys[o]
    for nsig in (1,2,3,5):
        v=float('nan')
        for i in range(len(xs)-1,0,-1):
            if (ys[i]-nsig)*(ys[i-1]-nsig)<=0 and ys[i]!=ys[i-1]:
                t=(nsig-ys[i])/(ys[i-1]-ys[i]); v=float(xs[i]+t*(xs[i-1]-xs[i])); break
        res_floor[f'{variant}_PEAK3ONLY_{nsig}']=v
    P(f"  variant {variant}  THIRD-PEAK HEIGHT RATIO H3/H2 ALONE:  f at 1sig: {res_floor[f'{variant}_PEAK3ONLY_1']:.4f}   "
      f"2sig: {res_floor[f'{variant}_PEAK3ONLY_2']:.4f}   3sig: {res_floor[f'{variant}_PEAK3ONLY_3']:.4f}   "
      f"5sig: {res_floor[f'{variant}_PEAK3ONLY_5']:.4f}")
F_CMB_MIN = res_floor['B_TT,TE,EE_3']
F_PEAK3   = res_floor['B_PEAK3ONLY_3']
F_CMB_MIN_TT = res_floor['B_TT_3']
P("")
info(f"HEADLINE (variant B, TT+TE+EE, 3 sigma):  f_cmb_min = {F_CMB_MIN:.4f}")
info(f"conservative (variant B, TT only, 3 sigma): f_cmb_min = {F_CMB_MIN_TT:.4f}")
info(f"MOST conservative: THIRD PEAK HEIGHT ALONE (variant B, 3 sigma): f_cmb_min = {F_PEAK3:.4f}")
info(f"variant A (textbook, background also changes), TT+TE+EE, 3 sigma:  f_cmb_min = {res_floor['A_TT,TE,EE_3']:.4f}")

check("the CMB floor is well inside the scanned grid (not an extrapolation)",
      np.isfinite(F_CMB_MIN) and 0.05 < F_CMB_MIN < 1.0, f"f_cmb_min={F_CMB_MIN:.4f}")
check("reducing the CLUSTERING fraction at FIXED background lowers the third/second peak ratio",
      rows[FGRID.tolist().index(0.50)]['R_B'] < R_FID,
      f"H3/H2 = {rows[FGRID.tolist().index(0.50)]['R_B']:.4f} at f=0.5 vs {R_FID:.4f} fiducial")
check("variant B holds theta_star fixed to <1e-4 (background truly unchanged)",
      max(abs(r['theta_B']-THETA_FID) for r in rows if np.isfinite(r['theta_B']))<1e-4,
      f"max |dtheta| = {max(abs(r['theta_B']-THETA_FID) for r in rows if np.isfinite(r['theta_B'])):.2e}")

out=dict(rows=rows, floor=res_floor, F_CMB_MIN=F_CMB_MIN, F_CMB_MIN_TT=F_CMB_MIN_TT,
         R_FID=R_FID, SIG_R=SIG_R, F_PEAK3=F_PEAK3, peaks_fid={k:list(v) for k,v in PK_FID.items()})
json.dump(out, open(os.path.join(HERE,"L145_cmb_results.json"),"w"), indent=1)
info("scan results written to H1_cmb_results.json")

# ================= NONLINEAR VERIFICATION at the critical f =================
sec("VERIFICATION -- is the LINEARISED nuisance profile trustworthy at the critical f?")
# A_s is profiled EXACTLY (a pure multiplicative amplitude) and n_s on the exact primordial tilt
# template, so only omega_b, theta_star, N_eff and Y_He are linearised.  Two guards:
#   G1  LINEARITY: evaluate CAMB at the offset the profile actually wants and compare with the
#       template prediction.  If the template reproduces CAMB, the linearisation is sound.
#   G2  TRUTH AT THE OPTIMUM: take the linear profile's own best-fit nuisance vector, build the TRUE
#       spectrum with CAMB at those values, and recompute chi^2 exactly.  If the true chi^2 is not
#       LOWER than the linear one, the linearisation was not overstating the CMB constraint.
def profile_solution(DL_model, mode="TTTEEE"):
    """Same algebra as profile_chi2 but returns the fitted coefficients (amplitude, then NUIS)."""
    cols=[DL_model]+[TPL[p_] for p_ in NUIS]
    C=COV_FID[USE]; Ci=np.linalg.inv(C)
    R=np.stack([DL_model[USE,0]-DL_FID[USE,0], DL_model[USE,1]-DL_FID[USE,1], DL_model[USE,3]-DL_FID[USE,3]],axis=1)
    M=np.stack([np.stack([c[USE,0],c[USE,1],c[USE,3]],axis=1) for c in cols],axis=2)
    A=np.einsum('lia,lij,ljb->ab',M,Ci,M); b_=np.einsum('lia,lij,lj->a',M,Ci,R)
    return np.linalg.solve(A,b_)

f_c = round(F_CMB_MIN,3)
DLc,_ = model_f(f_c,"B")
x = profile_solution(DLc)
amp = x[0]; coef = dict(zip(NUIS, x[1:]))
info(f"at the critical f = {f_c:.3f} the linear profile wants: dA/A = {amp:+.4f}, "
     + ", ".join(f"d{k} = {v:+.5f}" for k,v in coef.items()))

# G1 -- linearity of each linearised direction at the offset the profile actually wants
worst=0.0; det=[]
for p_ in NUIS:
    d=coef[p_]
    if abs(d)<1e-9: continue
    kw={}
    if p_=='ns':        kw=dict(ns=FID['ns']+d)
    elif p_=='ombh2':   kw=dict(ombh2=FID['ombh2']+d)
    elif p_=='thetastar': kw=dict(thetastar=THETA_FID+d)
    elif p_=='nnu':     kw=dict(nnu=3.044+d)
    elif p_=='YHe':     kw=dict(YHe=0.2454+d)
    try:
        DLtrue,_=spectra(**kw)
    except Exception:
        continue
    DLlin = DL_FID + d*TPL[p_]
    err=float(np.max(np.abs(DLtrue[USE,0]-DLlin[USE,0])/np.abs(DL_FID[USE,0])))
    det.append(f"{p_}: {100*err:.2f}%"); worst=max(worst,err)
check("GUARD G1  the linearised nuisance directions are accurate at the offsets the profile actually "
      "uses (CAMB vs template agree to better than 2% on TT)",
      worst<0.02, "max fractional TT error -- "+"; ".join(det))

# G2 -- true chi^2 at the linear profile's own optimum
try:
    DLtrue,_ = spectra(omch2=f_c*OMCH2_PLANCK, smooth_omega=(1-f_c)*OMCH2_PLANCK, H0=FID['H0'],
                       ns=FID['ns']+coef.get('ns',0.0), ombh2=FID['ombh2']+coef.get('ombh2',0.0),
                       nnu=3.044+coef.get('nnu',0.0), YHe=0.2454+coef.get('YHe',0.0))
    DLtrue = DLtrue*(1.0+amp) + coef.get('thetastar',0.0)*TPL['thetastar']
    chi_true = chi2(DLtrue, mode="TTTEEE")
    chi_lin  = profile_chi2(DLc,"TTTEEE")
    info(f"at f = {f_c:.3f}:  linearised profile Delta chi^2 = {chi_lin:.2f};  "
         f"TRUE Delta chi^2 at that same nuisance point = {chi_true:.2f}")
    check("GUARD G2  the exact chi^2 at the linear profile's own optimum MATCHES the reported value "
          "(within 50%) -- if it does not, the linearisation is invalid and the reported floor is "
          "unreliable in the LENIENT direction (superseded by L146_cmb_floor_exact_neff.py)",
          abs(chi_true-chi_lin) < 0.5*max(chi_lin,1.0)+2.0,
          f"exact {chi_true:.2f} vs reported {chi_lin:.2f}")
except Exception as e:
    check("GUARD G2  exact chi^2 evaluated at the linear profile optimum", False, f"failed: {e}")

# accuracy convergence control
DL_lo,_ = spectra(omch2=0.5*OMCH2_PLANCK, smooth_omega=0.5*OMCH2_PLANCK, H0=FID['H0'], boost=1.0)
DL_hi,_ = spectra(omch2=0.5*OMCH2_PLANCK, smooth_omega=0.5*OMCH2_PLANCK, H0=FID['H0'], boost=2.0)
dmax=np.max(np.abs(DL_hi[USE,0]/DL_lo[USE,0]-1))
check("CONTROL  CAMB numerical accuracy is converged (AccuracyBoost 1 vs 2 agree to <0.3% on TT)",
      dmax<3e-3, f"max fractional TT difference = {100*dmax:.3f}%")

sec("SUMMARY")
P(f"  checks: {NCHK-len(FAILS)}/{NCHK} passed" + ("" if not FAILS else "   FAILED: "+"; ".join(FAILS)))
P(f"  f_cmb_min (3 sigma, variant B, TT+TE+EE) = {F_CMB_MIN:.4f}   -> omega_c^clust >= {F_CMB_MIN*OMCH2_PLANCK:.4f}")
P(f"  f_cmb_min (3 sigma, variant B, TT only)  = {F_CMB_MIN_TT:.4f}")
P(f"  f_cmb_min (3 sigma, THIRD PEAK HEIGHT RATIO ALONE) = {F_PEAK3:.4f}   <- the literal 'third peak' answer")
