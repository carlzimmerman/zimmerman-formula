#!/usr/bin/env python3
"""
L150 -- HOW ROBUST IS THE GALAXY CEILING?  Every halo-modelling variant, every observational criterion.

A first pass at this asserted that the BTFR ceiling was insensitive to halo profile and concentration.
THAT WAS FALSE and the checks caught it.  This script therefore does not assert insensitivity; it
MEASURES the ceiling separately for every variant and reports the spread, including the variants that
weaken the constraint to nothing.

VARIANTS (halo modelling freedom a hybrid could legitimately claim):
   mass convention  AM = M200 = f * abundance-matched(M_star)   [ratio strongly MASS DEPENDENT]
                    CS = M200 = f * (omega_c/omega_b) * M_b     [ratio MASS INDEPENDENT]
   profile          NFW (cuspy -- what collisionless cold dark matter actually makes)
                    Burkert (cored -- maximal concession)
   concentration    Dutton-Maccio 2014, and that relation scaled by 0.5 and 2.0

OBSERVATIONAL CRITERIA (a variant is excluded if ANY of them excludes it):
   BTFR  |residual trend| > 3 sigma of the observed BTFR slope (3.85 +- 0.09, Lelli+2016)
   RAR   halo-injected scatter sigma_add > 0.06 dex (the observed intrinsic-scatter budget)
   a0 is refit at every f over a range including a0 -> 0, so no criterion is evaluated at a frozen a0.

The a0-COLLAPSE is reported alongside but NOT counted as an observational exclusion: it is an
interpretive statement about whether the theory is still MOND, not a measurement.

PASS = the printed statement is TRUE.  Self-contained; reads only committed repo data.
"""
import numpy as np, os, glob, math, json
from scipy.optimize import minimize_scalar

FAILS=[]; NCHK=0
def check(name, ok, detail=""):
    global NCHK; NCHK+=1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def P(s=""): print(s, flush=True)
def info(s): print("      "+s, flush=True)
def sec(t): P(); P("="*112); P(t); P("="*112)

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DATA=os.path.join(REPO,"real_research","data")
HERE=os.path.dirname(os.path.abspath(__file__))
G=6.674e-11; MSUN=1.989e30; kpc=3.0857e19
UPS_D0,UPS_B=0.5,0.7; H0_kms=67.36; h=H0_kms/100.
RHO_CRIT=3*(H0_kms*1e3/(1e3*kpc))**2/(8*np.pi*G)
COSMIC_RATIO=0.1200/0.02237
TREND_1SIG=0.09/3.85**2          # allowed |d log10 V / d log10 M_b| from slope 3.85 +- 0.09
SIG_ADD_MAX=0.06                 # dex, observed RAR intrinsic-scatter budget

P("="*112); P("L150 -- ROBUSTNESS OF THE GALAXY CEILING ACROSS ALL HALO-MODELLING VARIANTS"); P("="*112)
info(f"BTFR 3-sigma trend threshold = {3*TREND_1SIG:.4f} dex/dex;  RAR threshold sigma_add = {SIG_ADD_MAX} dex")

def moster_mstar(lg):
    M=10**lg; M1=10**11.59; N,be,ga=0.0351,1.376,0.608
    return M*2*N/((M/M1)**(-be)+(M/M1)**ga)
_lg=np.linspace(8.0,15.5,2000); _ms=np.log10(np.array([moster_mstar(x) for x in _lg]))
def M200_AM(Ms): return 10**np.interp(np.log10(np.maximum(Ms,1e4)),_ms,_lg)
def c200(M): return 10**(0.905-0.101*np.log10(np.maximum(M,1e6)*h/1e12))
def r200_of(M): return (3*M*MSUN/(4*np.pi*200*RHO_CRIT))**(1/3.)
def g_NFW(r,M,c):
    rs=r200_of(M)/c; x=r/rs; mu=lambda t: np.log(1+t)-t/(1+t)
    return G*(M*mu(x)/mu(c))*MSUN/r**2
def g_BURK(r,M,c):
    r0=r200_of(M)/c; x=r/r0
    m=lambda t: 0.5*np.log(1+t**2)+np.log(1+t)-np.arctan(t)
    return G*M*MSUN*(m(x)/m(c))/r**2
def nu_RAR(gb,a0):
    y=np.maximum(gb,1e-300)/a0
    return np.where(y>1e-12, gb/(-np.expm1(-np.sqrt(y))), np.sqrt(a0*np.maximum(gb,0)))

def read_master():
    lines=open(os.path.join(DATA,"SPARC_Lelli2016c.mrt"),encoding="latin-1").read().splitlines()
    last=max(i for i,l in enumerate(lines) if l.startswith("-----")); rows={}; nf=[]
    for line in lines[last+1:]:
        if not line.strip(): continue
        f=line.split(); nf.append(len(f))
        try: rows[f[0]]=dict(L36=float(f[7]),MHI=float(f[13]),Vflat=float(f[15]),Q=int(f[17]))
        except (ValueError,IndexError): continue
    return rows,nf
MASTER,_nf=read_master()
check("CONTROL  SPARC master table parses cleanly (175 rows, 19 fields each)",
      len(_nf)==175 and set(_nf)=={19}, f"{len(_nf)} rows, fields {sorted(set(_nf))}")
GAL=[]
for fn in sorted(glob.glob(os.path.join(DATA,"sparc_data","*_rotmod.dat"))):
    name=os.path.basename(fn).replace("_rotmod.dat","")
    if name not in MASTER: continue
    m=MASTER[name]
    try: d=np.loadtxt(fn,comments="#")
    except Exception: continue
    if d.ndim!=2 or d.shape[1]<6: continue
    r=d[:,0]*kpc; Vo=d[:,1]*1e3; eV=d[:,2]*1e3
    Vg=d[:,3]*1e3; Vd=d[:,4]*1e3; Vb=d[:,5]*1e3
    Vb2=Vg*np.abs(Vg)+UPS_D0*Vd*np.abs(Vd)+UPS_B*Vb*np.abs(Vb)
    msk=(r>0)&(Vo>0)&(Vb2>0)&(eV/np.maximum(Vo,1)<0.10)
    if msk.sum()<3: continue
    GAL.append(dict(name=name,r=r[msk],gb=Vb2[msk]/r[msk],go=Vo[msk]**2/r[msk],
                    L36=m["L36"],MHI=m["MHI"],Vflat=m["Vflat"],Q=m["Q"]))
def mstar(g): return UPS_D0*g["L36"]*1e9
def mb(g): return mstar(g)+1.33*g["MHI"]*1e9
BT=[g for g in GAL if np.isfinite(g["Vflat"]) and g["Vflat"]>10 and g["Q"]<3]
info(f"SPARC: {len(GAL)} galaxies; BTFR subsample {len(BT)}")

def ghalo(g,f,conv,prof,cfac):
    if f<=0: return np.zeros_like(g["r"])
    M=f*(M200_AM(mstar(g)) if conv=="AM" else COSMIC_RATIO*mb(g))
    c=max(c200(M)*cfac,1.0)
    return (g_NFW if prof=="NFW" else g_BURK)(g["r"],M,c)

def analyse(f,conv,prof,cfac):
    def ss(la0):
        a0=10**la0; t=0.0
        for g in GAL:
            rr=np.log10(g["go"]/nu_RAR(g["gb"]+ghalo(g,f,conv,prof,cfac),a0)); t+=float(np.sum(rr*rr))
        return t
    r=minimize_scalar(ss,bounds=(-13.5,-9.3),method='bounded',options=dict(xatol=1e-4))
    a0=10**r.x; n=sum(len(g["r"]) for g in GAL); rms=math.sqrt(ss(r.x)/n)
    lres=[];lmbv=[]
    for g in BT:
        i=int(np.argmax(g["r"]))
        gt=g["gb"][i]+ghalo(g,f,conv,prof,cfac)[i]
        Vp=math.sqrt(nu_RAR(np.array([gt]),a0)[0]*g["r"][i])
        lres.append(math.log10(g["Vflat"]*1e3/Vp)); lmbv.append(math.log10(mb(g)))
    lres=np.array(lres); lmbv=np.array(lmbv)
    A=np.vstack([lmbv-np.mean(lmbv),np.ones_like(lmbv)]).T
    sl,_=np.linalg.lstsq(A,lres,rcond=None)[0]
    return dict(a0=a0,rms=rms,trend=float(sl))

FG=[0.0,0.005,0.01,0.02,0.03,0.05,0.075,0.10,0.15,0.25,0.40,0.60,0.80,1.00]
VARIANTS=[("AM","NFW",1.0,"AM / NFW / c(M) standard   [the CDM-appropriate case]"),
          ("AM","NFW",0.5,"AM / NFW / c x 0.5"),
          ("AM","NFW",2.0,"AM / NFW / c x 2.0"),
          ("AM","Burkert",1.0,"AM / Burkert cored / c(M)"),
          ("CS","NFW",1.0,"CS / NFW / c(M)          [mass-INDEPENDENT ratio]"),
          ("CS","Burkert",1.0,"CS / Burkert / c(M)      [mass-INDEPENDENT ratio]")]

def cross(fs,ys,thresh):
    for i in range(1,len(fs)):
        if (ys[i]-thresh)*(ys[i-1]-thresh)<=0 and ys[i]!=ys[i-1]:
            t=(thresh-ys[i-1])/(ys[i]-ys[i-1]); return float(fs[i-1]+t*(fs[i]-fs[i-1]))
    return float('inf')

sec("CEILING PER VARIANT")
RES={}
for conv,prof,cfac,lab in VARIANTS:
    rows=[analyse(f,conv,prof,cfac) for f in FG]
    tr=[abs(r['trend']) for r in rows]
    add=[math.sqrt(max(0.0,r['rms']**2-rows[0]['rms']**2)) for r in rows]
    a0r=[r['a0']/rows[0]['a0'] for r in rows]
    cB=cross(FG,tr,3*TREND_1SIG); cR=cross(FG,add,SIG_ADD_MAX)
    ca=cross(FG,[-x for x in a0r],-0.5)          # a0 falls below half its f=0 value
    RES[lab]=dict(btfr=cB,rar=cR,a0=ca,obs=min(cB,cR),
                  trend_max=max(tr),add_max=max(add),a0_min=min(a0r))
    P("")
    P(f"  {lab}")
    P(f"    {'f':>7} {'|trend|':>9} {'/3sig':>7} {'sigma_add':>10} {'a0/a0(0)':>9}")
    for f,t,a,ar in zip(FG,tr,add,a0r):
        P(f"    {f:7.3f} {t:9.4f} {t/(3*TREND_1SIG):7.2f} {a:10.4f} {ar:9.4f}")
    fmt=lambda v: "  none  " if not np.isfinite(v) else f"{v:8.4f}"
    P(f"    -> BTFR 3sig ceiling {fmt(cB)}   RAR ceiling {fmt(cR)}   "
      f"OBSERVATIONAL ceiling {fmt(min(cB,cR))}   (a0 halves at f={fmt(ca)})")

sec("SUMMARY -- the galaxy ceiling and how far modelling freedom can push it")
P("")
P(f"  {'variant':>56} {'BTFR':>9} {'RAR':>9} {'ceiling':>9}")
for lab,v in RES.items():
    fmt=lambda x: "none" if not np.isfinite(x) else f"{x:.4f}"
    P(f"  {lab:>56} {fmt(v['btfr']):>9} {fmt(v['rar']):>9} {fmt(v['obs']):>9}")
AM_var={k:v for k,v in RES.items() if k.startswith("AM")}
CS_var={k:v for k,v in RES.items() if k.startswith("CS")}
F_AM_MAX=max(v['obs'] for v in AM_var.values())
F_AM_STD=RES["AM / NFW / c(M) standard   [the CDM-appropriate case]"]['obs']
P("")
info(f"CDM-appropriate variant (AM, cuspy NFW, standard c-M):  f_gal_max = {F_AM_STD:.4f}")
info(f"Most lenient MASS-DEPENDENT (AM) variant:               f_gal_max = "
     +("NO CEILING" if not np.isfinite(F_AM_MAX) else f"{F_AM_MAX:.4f}"))
info(f"Mass-INDEPENDENT (CS) variants:                         f_gal_max = "
     +("NO CEILING at any f<=1" if all(not np.isfinite(v['obs']) for v in CS_var.values())
       else f"{max(v['obs'] for v in CS_var.values()):.4f}"))

check("with an abundance-matched CUSPY (CDM-appropriate) halo the BTFR excludes f above ~0.1",
      0.03 < F_AM_STD < 0.25, f"f_gal_max = {F_AM_STD:.4f}")
check("HONEST LIMIT: a CORED halo weakens the BTFR test -- its trend never reaches 3 sigma, so the "
      "cored variant's ceiling comes from the RAR instead, and is looser",
      not np.isfinite(RES["AM / Burkert cored / c(M)"]['btfr']),
      f"cored BTFR max trend = {RES['AM / Burkert cored / c(M)']['trend_max']/(3*TREND_1SIG):.2f} x the 3-sigma threshold")
check("HONEST LIMIT: halo concentration matters -- the BTFR ceiling moves by more than a factor of 2 "
      "when c(M) is scaled between 0.5 and 2",
      max(RES['AM / NFW / c x 0.5']['btfr'],RES['AM / NFW / c x 2.0']['btfr'])/
      max(min(RES['AM / NFW / c x 0.5']['btfr'],RES['AM / NFW / c x 2.0']['btfr']),1e-9) > 2.0,
      f"c x0.5 -> {RES['AM / NFW / c x 0.5']['btfr']:.4f}, c x2.0 -> {RES['AM / NFW / c x 2.0']['btfr']:.4f}")
check("THE DOOR: with a MASS-INDEPENDENT halo/baryon ratio NO observational criterion excludes any f "
      "up to and including f=1 -- the galaxy ceiling disappears entirely",
      all(not np.isfinite(v['obs']) for v in CS_var.values()),
      "CS variants: "+", ".join(f"{k.split('/')[1].strip()}: "
      +("none" if not np.isfinite(v['obs']) else f"{v['obs']:.3f}") for k,v in CS_var.items()))
check("and the contrast is real: the mass-DEPENDENT variant at f=1 tilts the BTFR far beyond 3 sigma "
      "while the mass-INDEPENDENT one does not",
      RES["AM / NFW / c(M) standard   [the CDM-appropriate case]"]['trend_max'] > 3*TREND_1SIG
      and all(v['trend_max'] < 3*TREND_1SIG for v in CS_var.values()),
      f"AM max trend {RES['AM / NFW / c(M) standard   [the CDM-appropriate case]']['trend_max']/TREND_1SIG:.1f} sigma vs "
      f"CS max {max(v['trend_max'] for v in CS_var.values())/TREND_1SIG:.1f} sigma")

sec("WHAT THIS MEANS")
P(f"""
   The galaxy ceiling is NOT a bound on how much cold matter a galaxy may contain.  It is a bound on
   how that amount SCALES WITH GALAXY MASS.

     - If the cold component's galactic abundance tracks the cosmological one (abundance matching:
       halo/baryon ~ 1000 in dwarfs, ~30 at L*), it tilts the baryonic Tully-Fisher relation and is
       bounded at f = {F_AM_STD:.3f} for the cuspy halos that collisionless cold dark matter actually makes,
       and at f = {F_AM_MAX:.3f} for the most permissive mass-dependent variant tested.

     - If instead every galaxy carries the SAME multiple of its baryonic mass, the whole effect is
       absorbed by refitting a0 and NO galaxy criterion bounds f at all, up to f = 1.

   So the gap between galaxies and the CMB is held open by ONE assumption: that a cold, clustering
   component is distributed among galaxies the way cold dark matter is.  A hybrid must break exactly
   that -- it needs cold matter that clusters at z ~ 1100 (for the third peak) but whose z = 0
   galactic abundance is a mass-INDEPENDENT multiple of the baryons, i.e. depleted from dwarf haloes
   by a factor of order 100 relative to abundance matching.  Collisionless cold matter has no known
   way to do this: it does not feel feedback.  That is the door, and it is narrow -- but it is a
   DYNAMICAL question, not a parameter choice, and these data do not close it.
""")
json.dump({k:{kk:(None if not np.isfinite(vv) else vv) if isinstance(vv,float) else vv
              for kk,vv in v.items()} for k,v in RES.items()},
          open(os.path.join(HERE,"L150_results.json"),"w"),indent=1)
P(f"  checks: {NCHK-len(FAILS)}/{NCHK} passed"+("" if not FAILS else "   FAILED: "+"; ".join(FAILS)))
