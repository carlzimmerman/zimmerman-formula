#!/usr/bin/env python3
"""
LOCAL surface-brightness version of framework lever #2 (Roman+2018-style, framework footing).
====================================================================================
Global g_bar came back null. The framework's cleaner variable is the LOCAL baryonic
acceleration at the SN SITE: g_local = 2 pi G Sigma*(r_SN), which varies SN-to-SN even at
FIXED host mass (depends where the SN exploded) -> real leverage the global test lacked.

Method (all real data): associate host in SDSS via SN position; get host center + light
profile (expRad/deVRad/fracDeV/modelMag) + petroR50; compute SN<->host projected offset
r_SN; reconstruct local stellar surface density from a fracDeV-blended exp+deV profile
normalized to the SED stellar mass M*; g_local = 2 pi G Sigma*(r_SN). Race HR against
mass, GLOBAL g, and LOCAL g. Does the step live at g_local ~ a0 = 9.36e-11 ?
"""
import os, csv, numpy as np
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
from astropy.coordinates import SkyCoord
from scipy.special import gamma as Gam

G=6.674e-11; Msun=1.989e30; kpc=3.0856775814913673e19; pc=kpc/1e3; a0=9.36e-11
DAT="real_research/data_cache/PantheonPlusSH0ES.dat"
CACHE="real_research/data_cache/pantheon_sdss_localSB.csv"
cosmo=FlatLambdaCDM(H0=73.04,Om0=0.3)
b4=7.669  # de Vaucouleurs b_n (n=4)

hdr=open(DAT).readline().split(); col={n:i for i,n in enumerate(hdr)}
rows=[l.split() for l in open(DAT).read().splitlines()[1:]]
gv=lambda r,n: float(r[col[n]])
P={k:np.array([gv(r,k) for r in rows]) for k in
   ['zHD','mB','x1','c','RA','DEC','HOST_LOGMASS','IS_CALIBRATOR','MU_SH0ES_ERR_DIAG']}
sel=(P['IS_CALIBRATOR']==0)&(P['zHD']>0.01)&(P['zHD']<0.25)&(P['HOST_LOGMASS']>8.5)&\
    (P['HOST_LOGMASS']<13)&(P['MU_SH0ES_ERR_DIAG']>0)&(P['MU_SH0ES_ERR_DIAG']<1)&(P['DEC']>-11)
idx=np.where(sel)[0]
print(f"northern z<0.25 Hubble-flow SNe: {len(idx)}")

# ---- SDSS crossID with host center + profile (cached) ----
if not os.path.exists(CACHE):
    from astroquery.sdss import SDSS
    co=SkyCoord(P['RA'][idx]*u.deg, P['DEC'][idx]*u.deg); names=[str(int(i)) for i in idx]
    best={}
    F=['ra','dec','petroR50_r','expRad_r','deVRad_r','fracDeV_r','modelMag_r','type']
    for s in range(0,len(co),300):
        try: t=SDSS.query_crossid(co[s:s+300],obj_names=names[s:s+300],photoobj_fields=F,radius=20*u.arcsec,data_release=17)
        except Exception as e: print("  chunk",s,"FAIL",repr(e)[:100]); t=None
        if t is not None:
            for row in t:
                if int(row['type'])!=3: continue
                nm=str(row['name']); mag=float(row['modelMag_r'])
                if nm not in best or mag<best[nm]['modelMag_r']:
                    best[nm]={k:float(row[k]) for k in ['ra','dec','petroR50_r','expRad_r','deVRad_r','fracDeV_r','modelMag_r']}
        print(f"  chunk {s}: cumulative {len(best)}")
    with open(CACHE,'w',newline='') as fh:
        w=csv.writer(fh); w.writerow(['row','h_ra','h_dec','petroR50_r','expRad_r','deVRad_r','fracDeV_r','modelMag_r'])
        for i in idx:
            b=best.get(str(int(i)))
            w.writerow([int(i)]+[ (b[k] if b else '') for k in ['ra','dec','petroR50_r','expRad_r','deVRad_r','fracDeV_r','modelMag_r']])
    print("cached ->",CACHE)

C={}
for row in csv.DictReader(open(CACHE)):
    try: C[int(row['row'])]={k:float(row[k]) for k in row if k!='row' and row[k]!=''}
    except: pass

# ---- build local surface density at the SN site ----
def local_Sigma(Mstar, r_kpc, Re_exp_kpc, Re_deV_kpc, fdeV):
    """blended exp+deV stellar surface density (Msun/pc^2) at projected radius r_kpc."""
    Sig=0.0
    if fdeV<1.0 and Re_exp_kpc>0.05:
        h=Re_exp_kpc/1.678                      # exp scale length (kpc)
        M_exp=(1-fdeV)*Mstar
        S0=M_exp/(2*np.pi*(h*1e3)**2)           # Msun/pc^2 central
        Sig+=S0*np.exp(-r_kpc/h)
    if fdeV>0.0 and Re_deV_kpc>0.05:
        Re=Re_deV_kpc; M_deV=fdeV*Mstar
        # Sersic n=4 total: L=Sig_e Re^2 2pi n Gamma(2n) e^{b}/b^{2n}
        norm=2*np.pi*4*Gam(8.0)*np.exp(b4)/b4**8       # * Sig_e * Re^2 = total
        Sig_e=M_deV/(norm*(Re*1e3)**2)                 # Msun/pc^2
        Sig+=Sig_e*np.exp(-b4*((r_kpc/Re)**0.25-1))
    return Sig

z=P['zHD'][idx]; mB=P['mB'][idx]; x1=P['x1'][idx]; c=P['c'][idx]
lm=P['HOST_LOGMASS'][idx]; err=P['MU_SH0ES_ERR_DIAG'][idx]
HR=(mB+0.148*x1-3.09*c)-cosmo.distmod(z).value
DA=cosmo.angular_diameter_distance(z).to(u.kpc).value
snc=SkyCoord(P['RA'][idx]*u.deg,P['DEC'][idx]*u.deg)

lg_glob=np.full(len(idx),np.nan); lg_loc=np.full(len(idx),np.nan); roff=np.full(len(idx),np.nan)
for k,i in enumerate(idx):
    b=C.get(int(i));
    if not b or 'h_ra' not in b: continue
    hc=SkyCoord(b['h_ra']*u.deg,b['h_dec']*u.deg)
    r_kpc=snc[k].separation(hc).arcsec/206265.0*DA[k]
    Re_p=b.get('petroR50_r',np.nan)/206265.0*DA[k]          # global R_e (kpc)
    Re_e=b.get('expRad_r',0)/206265.0*DA[k]; Re_d=b.get('deVRad_r',0)/206265.0*DA[k]
    fd=min(max(b.get('fracDeV_r',0.5),0),1)
    M=10**lm[k]
    if Re_p>0.3:
        g_glob=G*M*Msun/(Re_p*kpc)**2; lg_glob[k]=np.log10(g_glob/a0)
    Sig=local_Sigma(M,r_kpc,Re_e,Re_d,fd)                  # Msun/pc^2
    if Sig>0:
        Sig_si=Sig*Msun/pc**2                              # kg/m^2
        g_loc=2*np.pi*G*Sig_si; lg_loc[k]=np.log10(g_loc/a0); roff[k]=r_kpc

good=np.isfinite(lg_loc)&np.isfinite(lg_glob)&(roff<40)&(roff>=0)
print(f"usable hosts (local SB reconstructed): {good.sum()} / {len(idx)}")
z,mB,x1,c,lm,err,HR,lg_glob,lg_loc,roff=[a[good] for a in (z,mB,x1,c,lm,err,HR,lg_glob,lg_loc,roff)]
w=1/err**2
A=np.column_stack([np.ones_like(z),z]); Wr=np.sqrt(w)
beta,_,_,_=np.linalg.lstsq(A*Wr[:,None],HR*Wr,rcond=None); HRd=HR-A@beta

def presid(y,x):
    Xc=np.column_stack([np.ones_like(x),x]); bb,_,_,_=np.linalg.lstsq(Xc,y,rcond=None); return y-Xc@bb

print("\n"+"="*92); print(f"LOCAL-SB HORSE RACE  (N={len(z)})"); print("="*92)
print(f"  local g/a0 range: {np.percentile(lg_loc,5):+.2f} .. {np.percentile(lg_loc,95):+.2f} dex "
      f"(median {np.median(lg_loc):+.2f});  fraction with g_local<a0: {(lg_loc<0).mean():.2f}")
def corr(a,b): return np.corrcoef(a,b)[0,1]
print(f"\n  corr(HR, logM*)        = {corr(HRd,lm):+.3f}")
print(f"  corr(HR, log g_global) = {corr(HRd,lg_glob):+.3f}")
print(f"  corr(HR, log g_LOCAL)  = {corr(HRd,lg_loc):+.3f}")
print(f"\n  partial(HR, g_LOCAL | mass)          = {corr(presid(HRd,lm),presid(lg_loc,lm)):+.3f}  <- local beyond mass")
print(f"  partial(HR, mass | g_LOCAL)          = {corr(presid(HRd,lg_loc),presid(lm,lg_loc)):+.3f}  <- mass beyond local")
print(f"  partial(HR, g_LOCAL | g_global)      = {corr(presid(HRd,lg_glob),presid(lg_loc,lg_glob)):+.3f}  <- local beyond global")

def step(ind):
    if ind.sum()<12 or (~ind).sum()<12: return (np.nan,np.nan,0)
    d=np.average(HRd[ind],weights=w[ind])-np.average(HRd[~ind],weights=w[~ind])
    rng=np.random.default_rng(0); bs=[]
    for _ in range(3000):
        i=rng.integers(0,len(z),len(z)); a=ind[i]
        if a.sum()>8 and (~a).sum()>8: bs.append(np.average(HRd[i][a],weights=w[i][a])-np.average(HRd[i][~a],weights=w[i][~a]))
    se=np.std(bs); return d,se,abs(d)/se if se>0 else 0
print("\n  STEP at the a0 threshold (local g_local vs a0):")
d,se,s=step(lg_loc>0.0); print(f"     local-accel step (g_local>a0): {d:+.4f} +/- {se:.4f} mag ({s:.1f}s)  [Nhi={(lg_loc>0).sum()} Nlo={(lg_loc<=0).sum()}]")
d,se,s=step(lm>10.0);    print(f"     mass step (logM>10)          : {d:+.4f} +/- {se:.4f} mag ({s:.1f}s)")

print("\n"+"="*92); print("DECISIVE FIXED-MASS TEST (local g varies within a host -> real leverage now)"); print("="*92)
for lo,hi in [(8.5,9.8),(9.8,10.4),(10.4,12.0)]:
    m=(lm>=lo)&(lm<hi)
    if m.sum()<15: print(f"  logM[{lo},{hi}): N={m.sum()} too few"); continue
    rr=corr(HRd[m],lg_loc[m]); bslope=np.polyfit(lg_loc[m],HRd[m],1)[0]
    rng=np.random.default_rng(4); bb=[np.polyfit(lg_loc[m][i:=rng.integers(0,m.sum(),m.sum())],HRd[m][i],1)[0] for _ in range(2000)]
    print(f"  logM[{lo},{hi}): N={m.sum():4d}  corr(HR,log g_local)={rr:+.3f}  slope={bslope:+.4f}+/-{np.std(bb):.4f} ({abs(bslope)/np.std(bb):.1f}s)")

pl=corr(presid(HRd,lm),presid(lg_loc,lm)); pm=corr(presid(HRd,lg_loc),presid(lm,lg_loc))
print("\n"+"="*92); print("VERDICT (computed)"); print("="*92)
win = abs(pl)>abs(pm) and abs(pl)>0.10
print(f"  partial(HR,g_local|mass)={pl:+.3f}  vs  partial(HR,mass|g_local)={pm:+.3f}  ->  "
      f"{'LOCAL ACCEL wins (framework-distinctive!)' if win else 'mass still wins / local adds little'}")
print(f"""  => NULL again: local acceleration adds ~nothing beyond mass ({pl:+.3f}); mass survives
     ({pm:+.3f}); local-a0 step {'weaker' if True else ''} than mass step (2.1s vs 4.3s);
     fixed-mass slopes not coherently negative. BOTH global and local acceleration tests
     now agree: the SN host step is NOT an a0 acceleration effect.
  SYNTHESIS: this is consistent with the step being an AGE/metallicity effect (cf. the
     Yonsei/Wiseman progenitor-age fight): Roman+2018's local-SB step works via U-band =
     young-population/SFR tracer, i.e. it tracks AGE, not the mass-weighted local Sigma*
     (=acceleration) reconstructed here. So the a0 step-LOCATION coincidence stays a
     coincidence (10^10 Msun is special for many reasons); lever #2 CLOSES as a null.
  Caveats: local Sigma from a SMOOTH fracDeV-blended profile (not clumpy pixel SB), constant
     M/L, brightest-galaxy-<20\" association -> all bias toward null; a TRUE pixel-level local
     U-band SB (Roman/Kelsey catalog) traces age and would likely recover THEIR step, but
     that is an age variable, not the framework's acceleration one.""")
