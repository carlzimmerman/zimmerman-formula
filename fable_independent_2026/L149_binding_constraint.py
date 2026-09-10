#!/usr/bin/env python3
"""
L149 -- WHICH GALAXY-SCALE CONSTRAINT IS ACTUALLY BINDING, and the a0-COLLAPSE diagnostic.

L148 found something that changes the shape of the question.  When a0 is honestly refit at every CDM
fraction f (as it must be, or the kill is manufactured), the RAR SCATTER criterion does NOT produce a
sharp ceiling: the best-fit a0 slides continuously toward ZERO as f rises, and the model morphs
smoothly from MOND into mean-relation LCDM, whose RAR scatter is only modestly worse.  So "the RAR
scatter" alone cannot close the question.  This script asks what does.

FOUR CANDIDATE CONSTRAINTS, all with a0 refit on SPARC at every f:
  (1) THE a0-COLLAPSE.  a0 is the theory's fundamental constant, not a nuisance.  At what f has the
      refit a0 fallen so far that the modification is no longer doing the galactic work?  This is
      reported as a CONTINUOUS curve (no threshold asserted), plus the f at which a0 drops below
      1/1.25, 1/1.5, 1/2, 1/4 and 1/10 of its f=0 value.
  (2) THE BTFR.  A mass-DEPENDENT halo/baryon ratio tilts and broadens the baryonic Tully-Fisher
      relation.  Observed (Lelli+2016, Vflat sample): slope 3.85 +- 0.09, intrinsic scatter
      <= 0.10 dex in M_b (= 0.026 dex in V).  The residual TREND is the sharp statistic.
  (3) THE MILKY WAY.  V_c(R0) = 233 +- 3 km/s (Eilers+2019 / GRAVITY R0 = 8.178 kpc) and the
      vertical force Sigma(|z|<1.1 kpc) = 71 +- 6 Msun/pc^2 (Kuijken-Gilmore / Bovy-Rix).
  (4) DWARF SPHEROIDALS.  The eight classical Milky Way dSphs from the committed Local Volume
      Database, with the external field effect.  Reported with explicit humility: this repository's
      own standing is that 8 classical dSphs is the sample ceiling and such tests reach ~1.7 sigma.

PASS = the printed statement is TRUE.  Self-contained; reads only committed repo data.
"""
import numpy as np, os, glob, csv, math, json
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

G=6.674e-11; MSUN=1.989e30; kpc=3.0857e19; PC=kpc/1000.
A0={"canonical":9.3619e-11,"alt":1.1279e-10}
UPS_D0,UPS_B=0.5,0.7
H0_kms=67.36; h=H0_kms/100.
RHO_CRIT=3*(H0_kms*1e3/(1e3*kpc))**2/(8*np.pi*G)
OMB,OMC=0.02237,0.1200; COSMIC_RATIO=OMC/OMB

P("="*112); P("L149 -- WHICH GALAXY CONSTRAINT BINDS?  plus the a0-collapse diagnostic"); P("="*112)

# ---------------- halos ----------------
def moster_mstar(lg):
    M=10**lg; M1=10**11.59; N,be,ga=0.0351,1.376,0.608
    return M*2*N/((M/M1)**(-be)+(M/M1)**ga)
_lg=np.linspace(8.0,15.5,2000); _ms=np.log10(np.array([moster_mstar(x) for x in _lg]))
def M200_AM(Ms): return 10**np.interp(np.log10(np.maximum(Ms,1e4)),_ms,_lg)
def c200(M): return 10**(0.905-0.101*np.log10(np.maximum(M,1e6)*h/1e12))
def r200_of(M): return (3*M*MSUN/(4*np.pi*200*RHO_CRIT))**(1/3.)
def Menc_NFW(r,M,c):
    rs=r200_of(M)/c; x=r/rs; mu=lambda t: np.log(1+t)-t/(1+t)
    return M*mu(x)/mu(c)
def g_NFW(r,M,c): return G*Menc_NFW(r,M,c)*MSUN/r**2
def nu_RAR(gb,a0):
    y=np.maximum(gb,1e-300)/a0
    return np.where(y>1e-12, gb/(-np.expm1(-np.sqrt(y))), np.sqrt(a0*np.maximum(gb,0)))

# ---------------- SPARC master table ----------------
# The published byte-by-byte spec is offset by one byte in this file copy, so fixed-width slicing is
# WRONG here.  Whitespace splitting is unambiguous instead: every data row splits into exactly 19
# fields (checked below), so no two columns can have merged.  Field order is the published one:
#   0 name  1 T  2 D  3 e_D  4 f_D  5 Inc  6 e_Inc  7 L[3.6]  8 e_L  9 Reff  10 SBeff  11 Rdisk
#   12 SBdisk  13 MHI  14 RHI  15 Vflat  16 e_Vflat  17 Q  18 Ref
def read_master():
    lines=open(os.path.join(DATA,"SPARC_Lelli2016c.mrt"),encoding="latin-1").read().splitlines()
    last=max(i for i,l in enumerate(lines) if l.startswith("-----"))
    rows={}; nf=[]
    for line in lines[last+1:]:
        if not line.strip(): continue
        f=line.split(); nf.append(len(f))
        try: rows[f[0]]=dict(D=float(f[2]),inc=float(f[5]),L36=float(f[7]),MHI=float(f[13]),
                             Vflat=float(f[15]),eVflat=float(f[16]),Q=int(f[17]))
        except (ValueError,IndexError): continue
    return rows,nf
MASTER,_nf=read_master()
check("CONTROL  every SPARC master row splits into exactly 19 whitespace fields, so no columns merged "
      "(the published byte offsets are shifted by one in this file copy and must NOT be used)",
      len(_nf)==175 and set(_nf)=={19} and len(MASTER)==175,
      f"{len(_nf)} rows, field counts {sorted(set(_nf))}, {len(MASTER)} parsed")
_vf=[m['Vflat'] for m in MASTER.values() if m['Vflat']>0]
check("CONTROL  parsed Vflat values are physical (10-400 km/s covers dwarfs through giant spirals) "
      "for the galaxies that have one",
      len(_vf)>100 and min(_vf)>=10 and max(_vf)<=400,
      f"{len(_vf)} with Vflat>0, range {min(_vf):.1f}-{max(_vf):.1f} km/s")

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
    GAL.append(dict(name=name,r=r[msk],Vo=Vo[msk],
                    g_gas=(Vg[msk]*np.abs(Vg[msk]))/r[msk],
                    g_dsk=(Vd[msk]*np.abs(Vd[msk]))/r[msk],
                    g_bul=(Vb[msk]*np.abs(Vb[msk]))/r[msk],
                    go=Vo[msk]**2/r[msk],
                    L36=m["L36"],MHI=m["MHI"],Vflat=m["Vflat"],eVflat=m["eVflat"],Q=m["Q"]))
info(f"SPARC: {len(GAL)} galaxies")
def gbar_of(g): return g["g_gas"]+UPS_D0*g["g_dsk"]+UPS_B*g["g_bul"]
def mstar_of(g): return UPS_D0*g["L36"]*1e9
def mgas_of(g):  return 1.33*g["MHI"]*1e9
def mb_of(g):    return mstar_of(g)+mgas_of(g)
def ghalo_of(g,f,conv="AM"):
    if f<=0: return np.zeros_like(g["r"])
    M=f*(M200_AM(mstar_of(g)) if conv=="AM" else COSMIC_RATIO*mb_of(g))
    return g_NFW(g["r"],M,c200(M))

# ---------------- refit a0 on SPARC at each f ----------------
def fit_a0(f,conv="AM"):
    def ss(la0):
        a0=10**la0; t=0.0
        for g in GAL:
            gt=gbar_of(g)+ghalo_of(g,f,conv)
            rr=np.log10(g["go"]/nu_RAR(gt,a0)); t+=float(np.sum(rr*rr))
        return t
    r=minimize_scalar(ss,bounds=(-13.5,-9.3),method='bounded',options=dict(xatol=1e-4))
    a0=10**r.x; n=sum(len(g["r"]) for g in GAL)
    return a0, math.sqrt(ss(r.x)/n)

sec("(1) THE a0-COLLAPSE -- how fast does the theory's fundamental constant have to be given up?")
FG=np.array([0.0,0.002,0.005,0.01,0.02,0.03,0.05,0.075,0.10,0.15,0.25,0.50,0.75,1.00])
A0F={}; P("")
P(f"    {'f':>7} {'a0_fit (m/s^2)':>15} {'a0(f)/a0(0)':>12} {'rms(dex)':>9}")
for f in FG:
    a0,rms=fit_a0(f); A0F[float(f)]=(a0,rms)
    P(f"    {f:7.3f} {a0:15.4e} {a0/A0F[0.0][0]:12.4f} {rms:9.4f}")
A0_0=A0F[0.0][0]
def f_where_a0_below(frac):
    xs=np.array(sorted(A0F)); ys=np.array([A0F[x][0]/A0_0 for x in xs])
    for i in range(1,len(xs)):
        if ys[i]<=frac<=ys[i-1] and ys[i]!=ys[i-1]:
            t=(frac-ys[i-1])/(ys[i]-ys[i-1]); return float(xs[i-1]+t*(xs[i]-xs[i-1]))
    return float('nan')
P("")
A0CEIL={}
for lab,frac in (("within 25% (a0>=0.80 a0_0)",0.80),("within a factor 1.5",1/1.5),
                 ("within a factor 2",0.5),("within a factor 4",0.25),("within a factor 10",0.10)):
    A0CEIL[lab]=f_where_a0_below(frac)
    info(f"a0 stays {lab:30s} -> f <= {A0CEIL[lab]:.4f}")
check("the refit a0 falls MONOTONICALLY with f (the CDM component really is replacing the modification)",
      all(A0F[float(FG[i])][0] <= A0F[float(FG[i-1])][0]+1e-13 for i in range(1,len(FG))),
      f"a0/a0_0 from 1.000 at f=0 to {A0F[1.0][0]/A0_0:.4f} at f=1")
check("at FULL CDM (f=1) the modification is switched off: refit a0 below 5% of its f=0 value",
      A0F[1.0][0]/A0_0 < 0.05, f"a0(f=1)/a0(0) = {A0F[1.0][0]/A0_0:.4f}")

sec("(2) THE BTFR -- slope and scatter (a mass-DEPENDENT halo ratio tilts the relation)")
BT=[g for g in GAL if np.isfinite(g["Vflat"]) and g["Vflat"]>20 and g["Q"]<3]
info(f"BTFR sample: {len(BT)} galaxies with a measured Vflat and quality flag Q<3")
def btfr_stats(f,conv="AM"):
    a0,_=fit_a0(f,conv); lres=[]; lmb=[]
    for g in BT:
        i=int(np.argmax(g["r"]))                       # outermost measured radius
        gt=gbar_of(g)[i]+ghalo_of(g,f,conv)[i]
        Vp=math.sqrt(nu_RAR(np.array([gt]),a0)[0]*g["r"][i])
        lres.append(math.log10(g["Vflat"]*1e3/Vp)); lmb.append(math.log10(mb_of(g)))
    lres=np.array(lres); lmb=np.array(lmb)
    A=np.vstack([lmb-np.mean(lmb),np.ones_like(lmb)]).T
    slope,icept=np.linalg.lstsq(A,lres,rcond=None)[0]
    resid=lres-A@np.array([slope,icept])
    # 1-sigma on the fitted trend
    se=float(np.sqrt(np.sum(resid**2)/(len(lres)-2)/np.sum((lmb-np.mean(lmb))**2)))
    return dict(a0=a0,scatter=float(np.std(lres)),trend=float(slope),trend_se=se,
                scatter_about_trend=float(np.std(resid)))
# Observed BTFR: slope 3.85 +- 0.09 => allowed residual trend |d logV / d log M_b| = 0.09/3.85^2
TREND_1SIG = 0.09/3.85**2
V_SCAT_OBS = 0.10/3.85                                   # 0.10 dex in M_b -> dex in V
info(f"observed allowances: residual trend |d log10 V / d log10 M_b| <= {TREND_1SIG:.4f} (1 sigma, from slope 3.85+-0.09)")
info(f"                     BTFR scatter in log10 V <= {V_SCAT_OBS:.4f} dex (from 0.10 dex in M_b)")
P("")
P(f"    {'f':>7} {'scatter(logV)':>14} {'trend':>9} {'trend/1sig':>11} {'scat/obs':>9}")
BTR={}
for f in FG:
    s=btfr_stats(f); BTR[float(f)]=s
    P(f"    {f:7.3f} {s['scatter']:14.4f} {s['trend']:+9.4f} {abs(s['trend'])/TREND_1SIG:11.2f} {s['scatter']/V_SCAT_OBS:9.2f}")
def f_where(key,thresh,d):
    xs=np.array(sorted(d)); ys=np.array([abs(d[x][key]) for x in xs])
    for i in range(1,len(xs)):
        if (ys[i]-thresh)*(ys[i-1]-thresh)<=0 and ys[i]!=ys[i-1]:
            t=(thresh-ys[i-1])/(ys[i]-ys[i-1]); return float(xs[i-1]+t*(xs[i]-xs[i-1]))
    return float('nan')
F_BTFR_TREND_3S=f_where('trend',3*TREND_1SIG,BTR)
F_BTFR_SCAT   =f_where('scatter',math.hypot(BTR[0.0]['scatter'],V_SCAT_OBS),BTR)
info("")
info(f"BTFR residual-trend ceiling (3 sigma on the observed slope): f <= {F_BTFR_TREND_3S:.4f}")
info(f"BTFR scatter ceiling (injected scatter = observed allowance): f <= {F_BTFR_SCAT:.4f}")
check("the halo TILTS the BTFR (a nonzero residual trend appears and grows with f), which is the "
      "mechanism that makes the BTFR a sharper probe than the RAR scatter",
      abs(BTR[0.25]['trend'])>abs(BTR[0.0]['trend']),
      f"trend {BTR[0.0]['trend']:+.4f} at f=0 -> {BTR[0.25]['trend']:+.4f} at f=0.25")

sec("(3) THE MILKY WAY -- circular speed at R0 and the vertical force")
R0=8.178*kpc; VC_OBS,VC_ERR=233e3,3e3
MB_MW,MB_MW_ERR=6.0e10,0.6e10                  # stars ~5e10 + gas ~1e10, 10% systematic
SIG_Z_OBS,SIG_Z_ERR=71.0,6.0                   # Msun/pc^2 within |z|<1.1 kpc
info(f"M_b(MW) = {MB_MW:.2e} +- {MB_MW_ERR:.1e} Msun; V_c(R0={R0/kpc:.3f} kpc) = {VC_OBS/1e3:.0f} +- {VC_ERR/1e3:.0f} km/s")
M200_MW=M200_AM(5.0e10)
info(f"abundance-matched Milky Way halo: M200 = {M200_MW:.3e} Msun, c = {c200(M200_MW):.2f}, r200 = {r200_of(M200_MW)/kpc:.0f} kpc")
P("")
P(f"    {'f':>7} {'V_c(R0) km/s':>13} {'n_sigma(Vc)':>12} {'Sigma_1.1 Msun/pc2':>19} {'n_sigma(Sig)':>13}")
MWR={}
for f in FG:
    a0,_=fit_a0(f)
    gb=G*MB_MW*MSUN/R0**2
    gh=g_NFW(R0,f*M200_MW,c200(f*M200_MW)) if f>0 else 0.0
    Vc=math.sqrt(nu_RAR(np.array([gb+gh]),a0)[0]*R0)
    # vertical: Newton-equivalent surface density that the model's total gravity implies at |z|<1.1 kpc
    # Sigma_eff = g_z/(2 pi G); use the MOND-boosted local column plus the halo's own contribution
    boost=nu_RAR(np.array([gb+gh]),a0)[0]/(gb+gh)
    SIG_BAR=47.0                                     # Msun/pc^2 baryonic column (Bovy-Rix)
    rho_h=((Menc_NFW(R0*1.0001,f*M200_MW,c200(f*M200_MW))-Menc_NFW(R0,f*M200_MW,c200(f*M200_MW)))
           /(4*np.pi*R0**2*(0.0001*R0))) if f>0 else 0.0            # Msun per m^3
    Sig_h=2*rho_h*(1.1*kpc)*PC**2                                    # -> Msun per pc^2
    Sig=boost*SIG_BAR+Sig_h
    nV=abs(Vc-VC_OBS)/math.hypot(VC_ERR, 0.5*VC_OBS*MB_MW_ERR/MB_MW)
    nS=abs(Sig-SIG_Z_OBS)/SIG_Z_ERR
    MWR[float(f)]=dict(Vc=Vc/1e3,nV=nV,Sig=Sig,nS=nS)
    P(f"    {f:7.3f} {Vc/1e3:13.1f} {nV:12.2f} {Sig:19.1f} {nS:13.2f}")
F_MW=f_where('nV',3.0,MWR)
info(f"Milky Way V_c ceiling (3 sigma, M_b systematic included): f <= {F_MW if np.isfinite(F_MW) else float('nan'):.4f}"
     if np.isfinite(F_MW) else "Milky Way V_c ceiling (3 sigma): NOT REACHED anywhere on the grid -- the MW does not bind")

sec("(4) DWARF SPHEROIDALS -- the eight classical Milky Way dSphs (Local Volume Database)")
def fnum(v):
    try:
        x=float(v); return x if np.isfinite(x) else None
    except (TypeError,ValueError): return None
CLASSIC8={"Draco","Sculptor","Fornax","Carina","Sextans","Leo I","Leo II","Ursa Minor"}
MW_MB=6.0e10; UPS_V=2.0
d8=[]
for r_ in csv.DictReader(open(os.path.join(DATA,"dsph","lvd_dwarf_mw.csv"))):
    if r_["name"] not in CLASSIC8: continue
    sig=fnum(r_["vlos_sigma"]); rh=fnum(r_["rhalf_sph_physical"]) or fnum(r_["rhalf_physical"])
    MV=fnum(r_["M_V"]); lMs=fnum(r_["mass_stellar"]); lMHI=fnum(r_["mass_HI"])
    Dgc=fnum(r_["distance_gc"])
    em=fnum(r_["vlos_sigma_em"]) or 0.2*sig; ep=fnum(r_["vlos_sigma_ep"]) or 0.2*sig
    if sig is None or rh is None or Dgc is None: continue
    d8.append(dict(name=r_["name"],sig=sig,esig=0.5*(em+ep),rh=rh,Dgc=Dgc,
                   Ms=(10**lMs if lMs is not None else 10**(0.4*(4.83-MV))*UPS_V),
                   MHI=(10**lMHI if lMHI is not None else 0.0)))
info(f"recovered {len(d8)} of the 8 classical dSphs from the committed LVD table")
check("CONTROL  all eight classical Milky Way dSphs are recovered from the committed catalogue",
      len(d8)==8, f"{len(d8)}/8")
def dsph_resid(f,a0):
    out=[]
    for d in d8:
        r12=(4.0/3.0)*d["rh"]*PC
        Mb=d["Ms"]+1.33*d["MHI"]
        gi=G*(0.5*Mb*MSUN)/r12**2
        if f>0:
            M2=f*M200_AM(d["Ms"]); gi+=g_NFW(r12,M2,c200(M2))
        ge=G*MW_MB*MSUN/(d["Dgc"]*kpc)**2                 # external field of the Milky Way
        gp=nu_RAR(np.array([gi+ge]),a0)[0]*gi/(gi+ge)      # EFE-suppressed 1-D prescription
        gobs=3.0*(d["sig"]*1e3)**2/r12
        eobs=2*d["esig"]/d["sig"]/math.log(10)
        out.append((d["name"],math.log10(gobs/gp),eobs))
    return out
P("")
P(f"    {'f':>7} {'mean resid (dex)':>17} {'rms (dex)':>10} {'chi2/8':>8}")
DS={}
for f in FG:
    a0,_=fit_a0(f); rr=dsph_resid(f,a0)
    v=np.array([x[1] for x in rr]); e=np.array([x[2] for x in rr])
    e=np.sqrt(e**2+0.15**2)                               # 0.15 dex modelling systematic
    DS[float(f)]=dict(mean=float(np.mean(v)),rms=float(np.sqrt(np.mean(v**2))),
                      chi2=float(np.sum((v/e)**2)/len(v)))
    P(f"    {f:7.3f} {DS[float(f)]['mean']:+17.4f} {DS[float(f)]['rms']:10.4f} {DS[float(f)]['chi2']:8.2f}")
info("NOTE (repository standing): 8 classical dSphs is the sample ceiling; such tests reach ~1.7 sigma.")
info("The dSph column is reported for completeness and is NOT used to set any headline number.")

sec("VERDICT -- which constraint binds?")
cands=[("a0 stays within a factor 2 of its measured value",A0CEIL["within a factor 2"]),
       ("BTFR residual trend within 3 sigma of the observed slope",F_BTFR_TREND_3S),
       ("BTFR scatter within the observed allowance",F_BTFR_SCAT),
       ("Milky Way V_c(R0) within 3 sigma",F_MW)]
P("")
for lab,v in cands:
    P(f"    f <= {v:8.4f}   {lab}" if np.isfinite(v) else f"    f <= {'  ---':>8}   {lab}   (never violated on the grid: does NOT bind)")
fin=[(l,v) for l,v in cands if np.isfinite(v)]
BIND=min(fin,key=lambda t:t[1]) if fin else (None,float('nan'))
P("")
info(f"BINDING CONSTRAINT: {BIND[0]}  ->  f_gal_max = {BIND[1]:.4f}")
json.dump(dict(a0_curve={str(k):list(v) for k,v in A0F.items()}, a0_ceilings=A0CEIL,
               btfr={str(k):v for k,v in BTR.items()}, mw={str(k):v for k,v in MWR.items()},
               dsph={str(k):v for k,v in DS.items()},
               F_BTFR_TREND_3S=F_BTFR_TREND_3S,F_BTFR_SCAT=F_BTFR_SCAT,F_MW=F_MW,
               binding=[BIND[0],BIND[1]]),
          open(os.path.join(HERE,"L149_results.json"),"w"),indent=1)
P(""); P(f"  checks: {NCHK-len(FAILS)}/{NCHK} passed"+("" if not FAILS else "   FAILED: "+"; ".join(FAILS)))
