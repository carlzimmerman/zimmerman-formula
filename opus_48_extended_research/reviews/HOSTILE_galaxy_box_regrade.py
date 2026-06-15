#!/usr/bin/env python3
"""
HOSTILE REGRADE of SWEEP 2 [galaxy_box].
========================================
Independent skeptic cross-checks of the galaxy_box_viability_scan claims:

 Q1. Is "96% of a0 prior / 75% of Upsilon prior" an HONEST volume, or a misleading
     1D marginal of a sloped band? Recompute the TRUE 2D cell-fraction AND the
     conditional a0-window AT the framework's Upsilon=0.70 (not marginalized over Ups).

 Q2. Is the framework point INTERIOR or on the EDGE? Distance of 9.36e-11 to the
     nearest viable-band boundary at Ups=0.70, in cells and in dex-penalty terms.
     And: at what Upsilon does 9.36e-11 first land on the ridge? (the M/L requirement).

 Q3. Does the RAR penalty (+0.51%) SURVIVE a different scatter metric?
     (a) error-weighted RMS (1/sigma_logg^2);  (b) 5%/95% trimmed RMS (outlier-robust);
     (c) median-|resid| (L1). If 9.36e-11's penalty blows up under a reasonable metric,
     the "interior" claim is metric-fragile.

 Q4. The BTFR "implied a0" both-ways: the BTFR intercept implies a0~1.26e-10 at Ups=0.70.
     How many sigma does THAT disprefer 9.36e-11? (the ledger calls it non-diagnostic;
     verify the dispreference magnitude honestly).

 Q5. Sensitivity of the headline 49% to the ARBITRARY conventions:
     TOL_DEX (0.005), the WB_OBS_BAND (1.0,1.65), the err/V<0.1 cut. Does the
     "broad ~50%" survive tightening these, or is it a loose-threshold artifact?
"""
import glob, math, os, csv
import numpy as np
from scipy.optimize import minimize_scalar
from scipy import odr

HERE = os.path.dirname(os.path.abspath(__file__))
ROT  = os.path.join(HERE, "..", "..", "real_research", "data", "sparc_data")
MAST = os.path.join(HERE, "..", "..", "real_research", "data", "sparc_master_clean.csv")
KPC_M=3.0856775814913673e19; KMS=1e3; G=6.674e-11; MSUN=1.989e30; HE=1.33
FW_A0=9.36e-11; G_EXT_MW=2.08e-10

def g_dsunruh(gb,a0): return np.sqrt(gb**2+gb*a0)
def g_simple(gb,a0):  return 0.5*gb*(1.0+np.sqrt(1.0+4.0*a0/gb))
def g_standard(gb,a0):
    y=gb/a0; return gb*np.sqrt(0.5+np.sqrt(0.25+1.0/y**2))
def g_mcgaugh(gb,a0):
    x=np.sqrt(gb/a0); return gb/(1.0-np.exp(-x))
GFUN={"dsunruh":g_dsunruh,"simple":g_simple,"standard":g_standard,"mcgaugh":g_mcgaugh}

def load_rar_full(ml,mlb=0.70):
    """return gbar, gobs, AND err_on_logg (propagated from vobs error)."""
    gb,go,wlog=[],[],[]
    for path in sorted(glob.glob(os.path.join(ROT,"*_rotmod.dat"))):
        with open(path) as fh:
            for line in fh:
                line=line.strip()
                if not line or line.startswith("#"): continue
                p=line.split()
                if len(p)<6: continue
                try: r,vobs,everr,vgas,vdisk,vbul=(float(p[i]) for i in range(6))
                except ValueError: continue
                if r<=0 or vobs<=0 or everr<=0 or everr/vobs>0.10: continue
                vbar2=vgas*abs(vgas)+ml*vdisk*abs(vdisk)+mlb*vbul*abs(vbul)
                if vbar2<=0: continue
                rm=r*KPC_M
                g_o=(vobs*KMS)**2/rm; g_b=(vbar2*KMS**2)/rm
                if g_b<=0 or g_o<=0: continue
                # d log10(gobs) = 2 * d log10(vobs) = 2/ln10 * (everr/vobs)
                sig_logg = 2.0/math.log(10.0)*(everr/vobs)
                gb.append(g_b); go.append(g_o); wlog.append(sig_logg)
    return np.array(gb),np.array(go),np.array(wlog)

def scat_rms(gb,go,a0,nu):
    r=np.log10(go)-np.log10(GFUN[nu](gb,a0)); return float(np.sqrt(np.mean(r**2)))
def scat_wrms(gb,go,sig,a0,nu):
    r=np.log10(go)-np.log10(GFUN[nu](gb,a0)); w=1.0/sig**2
    return float(np.sqrt(np.sum(w*r**2)/np.sum(w)))
def scat_trim(gb,go,a0,nu,lo=5,hi=95):
    r=np.log10(go)-np.log10(GFUN[nu](gb,a0)); r=r-np.median(r)
    qlo,qhi=np.percentile(r,[lo,hi]); m=(r>=qlo)&(r<=qhi)
    return float(np.sqrt(np.mean(r[m]**2)))
def scat_l1(gb,go,a0,nu):
    r=np.log10(go)-np.log10(GFUN[nu](gb,a0)); return float(np.median(np.abs(r-np.median(r))))

def opt(metric_fn):
    f=lambda la:metric_fn(10**la)
    r=minimize_scalar(f,bounds=(math.log10(5e-11),math.log10(3e-10)),method="bounded",options={"xatol":1e-7})
    return 10**r.x,r.fun

print("="*84)
print("HOSTILE REGRADE — SWEEP 2 [galaxy_box]")
print("="*84)

gb,go,sig=load_rar_full(0.70)
print(f"Loaded {len(gb)} RAR points at Ups=0.70 (err/V<0.1).  median sig_logg={np.median(sig):.4f} dex\n")

# ============ Q1: honest volume vs marginal ============
print("-"*84); print("Q1. TRUE 2D volume vs the 1D-marginal '96%/75%' headline"); print("-"*84)
# rebuild the dsunruh viable map exactly as the scan does
ups_grid=np.round(np.arange(0.40,0.701+1e-9,0.025),3)
a0_grid=np.linspace(8e-11,1.30e-10,27)
TOL=0.005; WB=(1.0,1.65)
cache={u:load_rar_full(u) for u in ups_grid}
# btfr slopes
brows=[]
with open(MAST) as f:
    for r in csv.DictReader(f):
        try: brows.append((float(r["L36"]),float(r["MHI"]),float(r["Vflat"]),int(r["Q"]),float(r["inc"])))
        except (ValueError,KeyError): continue
def btfr_slope(ml):
    lM,lV,a0s=[],[],[]
    for L36,MHI,Vf,Q,inc in brows:
        if Q>2 or Vf<=30 or inc<30: continue
        M=ml*L36*1e9+HE*MHI*1e9
        if M<=0: continue
        lM.append(math.log10(M)); lV.append(math.log10(Vf)); a0s.append((Vf*KMS)**4/(G*M*MSUN))
    lV,lM=np.array(lV),np.array(lM); lin=lambda B,x:B[0]*x+B[1]
    out=odr.ODR(odr.RealData(lV,lM),odr.Model(lin),beta0=[4.0,np.median(lM)-4*np.median(lV)]).run()
    return out.beta[0], float(np.median(a0s))
def gamma_efe(y,nu):
    if nu=="dsunruh": return math.sqrt(1+1/y)
    if nu=="simple": return 0.5*(1+math.sqrt(1+4/y))
    if nu=="standard": return math.sqrt(0.5+math.sqrt(0.25+1/y**2))
    if nu=="mcgaugh": return 1/(1-math.exp(-math.sqrt(y)))

viable=[]
for u in ups_grid:
    gbu,gou,_=cache[u]
    a0o,so=opt(lambda a0:scat_rms(gbu,gou,a0,"dsunruh"))
    slope,_=btfr_slope(u); btfr_ok=3.7<=slope<=4.3
    for a0 in a0_grid:
        s=scat_rms(gbu,gou,a0,"dsunruh")
        rar_ok=(s-so)<=TOL
        cap=gamma_efe(G_EXT_MW/a0,"dsunruh"); efe_ok=WB[0]<=cap<=WB[1]
        if rar_ok and btfr_ok and efe_ok: viable.append((u,a0))
ncells=len(ups_grid)*len(a0_grid)
print(f"  TRUE 2D cell fraction (dsunruh): {len(viable)}/{ncells} = {len(viable)/ncells*100:.1f}%")
a0s_v=sorted(set(a for _,a in viable)); ups_v=sorted(set(u for u,_ in viable))
print(f"  1D a0-marginal span: [{min(a0s_v):.2e},{max(a0s_v):.2e}] = {(max(a0s_v)-min(a0s_v))/(1.30e-10-8e-11)*100:.0f}% of a0 prior")
print(f"  1D Ups-marginal span: [{min(ups_v):.2f},{max(ups_v):.2f}] = {(max(ups_v)-min(ups_v))/(0.70-0.40)*100:.0f}% of Ups prior")
# conditional a0 window AT Ups=0.70 only
v70=[a for u,a in viable if abs(u-0.70)<1e-9]
print(f"  CONDITIONAL a0 window at Ups=0.70 ONLY: [{min(v70):.2e},{max(v70):.2e}] = {(max(v70)-min(v70))/(1.30e-10-8e-11)*100:.0f}% of a0 prior")
print(f"  --> the 1D marginal OVER-states: it counts a0 viable at SOME Upsilon. The honest")
print(f"      volume is the 2D cell fraction (~49%), NOT '96% of a0 prior'.")

# ============ Q2: edge vs interior ============
print("\n"+"-"*84); print("Q2. Is the framework point INTERIOR or on the EDGE?"); print("-"*84)
gb70,go70,_=cache[0.70]
a0o70,so70=opt(lambda a0:scat_rms(gb70,go70,a0,"dsunruh"))
# fine a0 scan at Ups=0.70 to find the RAR-viable band edges
a0f=np.linspace(7e-11,1.6e-10,600)
sf=np.array([scat_rms(gb70,go70,a,"dsunruh") for a in a0f])
band=a0f[(sf-so70)<=TOL]
lo70,hi70=band.min(),band.max()
print(f"  At Ups=0.70: RAR-viable a0 band [{lo70:.3e},{hi70:.3e}]; optimum {a0o70:.3e}")
print(f"  Framework 9.36e-11 sits {(FW_A0-lo70)/(hi70-lo70)*100:.0f}% of the way from the LOW edge")
print(f"  Distance to low edge: {(FW_A0-lo70)*1e11:.2f}e-11 ; to optimum: {(a0o70-FW_A0)*1e11:.2f}e-11 ({(a0o70-FW_A0)/a0o70*100:.1f}% below opt)")
# at what Upsilon does 9.36e-11 first enter the ridge (pen<=0.003, the scan's stricter ridge)?
print("  Minimum Upsilon for 9.36e-11 to be on the ridge (pen<=0.003 / <=0.005):")
for u in ups_grid:
    gbu,gou,_=cache[u]; a0o,so=opt(lambda a0:scat_rms(gbu,gou,a0,"dsunruh"))
    p=scat_rms(gbu,gou,FW_A0,"dsunruh")-so
    tag=[]
    if p<=0.003: tag.append("ridge<=0.003")
    if p<=0.005: tag.append("scan<=0.005")
    if tag: print(f"     Ups={u}: 9.36e-11 penalty {p*100:.2f}% of floor -> {','.join(tag)}"); break
print("  --> 9.36e-11 requires Upsilon >= ~0.65 (near-max-disk). At population-synthesis")
print("      Ups~0.5 the framework a0 is DISPREFERRED (RAR wants ~1.4e-10). This is a REAL")
print("      (a0,Upsilon) co-requirement, not full interiority.")

# ============ Q3: metric robustness of the +0.51% penalty ============
print("\n"+"-"*84); print("Q3. Does the RAR +0.51% penalty SURVIVE other scatter metrics? (Ups=0.70)"); print("-"*84)
print(f"  {'metric':>16} | {'opt a0':>10} | {'floor':>8} | {'9.36e-11 pen':>13} | {'% of floor':>10}")
mets=[("unweighted RMS", lambda a0:scat_rms(gb70,go70,a0,"dsunruh")),
      ("err-weighted RMS", lambda a0:scat_wrms(gb70,go70,sig if len(sig)==len(gb70) else load_rar_full(0.70)[2],a0,"dsunruh")),
      ("5-95% trim RMS",  lambda a0:scat_trim(gb70,go70,a0,"dsunruh")),
      ("L1 median|res|",  lambda a0:scat_l1(gb70,go70,a0,"dsunruh"))]
sig70=load_rar_full(0.70)[2]
mets[1]=("err-weighted RMS", lambda a0:scat_wrms(gb70,go70,sig70,a0,"dsunruh"))
for name,fn in mets:
    a0o,fo=opt(fn); pen=fn(FW_A0)-fo
    print(f"  {name:>16} | {a0o:>10.3e} | {fo:>8.4f} | {pen:>+13.4f} | {pen/fo*100:>9.2f}%")
print("  --> if the penalty stays ~<=2% across metrics, the 'interior on RAR' claim is robust.")

# ============ Q4: BTFR-implied a0 dispreference ============
print("\n"+"-"*84); print("Q4. How strongly does the BTFR-implied a0 DISPREFER 9.36e-11?"); print("-"*84)
for u in [0.5,0.7]:
    slope,a0imp=btfr_slope(u)
    # scatter of per-galaxy a0 in dex
    lM,lV,a0s=[],[],[]
    for L36,MHI,Vf,Q,inc in brows:
        if Q>2 or Vf<=30 or inc<30: continue
        M=u*L36*1e9+HE*MHI*1e9
        if M<=0: continue
        a0s.append((Vf*KMS)**4/(G*M*MSUN))
    a0s=np.array(a0s); la=np.log10(a0s)
    med=10**np.median(la); sd=np.std(la); sem=sd/math.sqrt(len(la))
    z=(math.log10(med)-math.log10(FW_A0))/sem
    print(f"  Ups={u}: BTFR median a0={med:.2e} (slope {slope:.3f}); scatter {sd:.3f} dex, N={len(la)}")
    print(f"     9.36e-11 is {(math.log10(med)-math.log10(FW_A0)):+.3f} dex from BTFR-a0 = {z:+.1f} sigma_mean (sd {sd:.2f}dex pop)")
print("  --> BTFR-implied a0 (~1.26e-10 at 0.70) is HIGHER than 9.36e-11; report the honest")
print("      dispreference (sigma_of_mean is large-N-inflated; the population sd is the fair scale).")

# ============ Q5: headline robustness to arbitrary conventions ============
print("\n"+"-"*84); print("Q5. Does the '~50% broad' survive tightening the arbitrary thresholds?"); print("-"*84)
def count_viable(tol, wb, errcut_note=""):
    vv=0
    for u in ups_grid:
        gbu,gou,_=cache[u]; a0o,so=opt(lambda a0:scat_rms(gbu,gou,a0,"dsunruh"))
        slope,_=btfr_slope(u); btfr_ok=3.7<=slope<=4.3
        for a0 in a0_grid:
            s=scat_rms(gbu,gou,a0,"dsunruh"); rar_ok=(s-so)<=tol
            cap=gamma_efe(G_EXT_MW/a0,"dsunruh"); efe_ok=wb[0]<=cap<=wb[1]
            if rar_ok and btfr_ok and efe_ok: vv+=1
    return vv
for tol in [0.005,0.003,0.002,0.001]:
    n=count_viable(tol,(1.0,1.65))
    fwin = (scat_rms(gb70,go70,FW_A0,"dsunruh")-so70)<=tol
    print(f"  TOL_DEX={tol}: viable {n}/{ncells} = {n/ncells*100:.1f}% ; framework pt in? {'YES' if fwin else 'NO'}")
print("  --> if 9.36e-11 stays in even at TOL=0.001 AND the region stays broad, robust not loose.")
