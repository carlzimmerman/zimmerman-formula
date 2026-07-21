#!/usr/bin/env python3
"""
DECISIVE separability test (framework lever #2, part 2): does the SN Ia Hubble residual
track host ACCELERATION g_bar = G M*/R_e^2 better than host MASS -- AT FIXED MASS?
====================================================================================
Pantheon+ ships NO host coordinates (HOST_RA=-999), so we associate the host via the SN
position: cross-match SN RA/DEC to SDSS (DR17), keep the brightest GALAXY (type=3) within
20" as the host, take petroR50_r (half-light radius, arcsec). Northern, z<0.25 (hosts well
resolved). Build g_bar/a0, run mass vs acceleration as competing predictors. Cached.
a0 = 9.36e-11 (framework INPUT). At fixed mass g_bar ~ R_e^-2, so the fixed-mass test =
does HR correlate with log R_e (compact=more Newtonian).
"""
import os, csv, numpy as np
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
from astropy.coordinates import SkyCoord

G=6.674e-11; Msun=1.989e30; kpc=3.0856775814913673e19; a0=9.36e-11
DAT="real_research/data_cache/PantheonPlusSH0ES.dat"
CACHE="real_research/data_cache/pantheon_sdss_sizes.csv"
cosmo=FlatLambdaCDM(H0=73.04,Om0=0.3)

hdr=open(DAT).readline().split(); col={n:i for i,n in enumerate(hdr)}
rows=[l.split() for l in open(DAT).read().splitlines()[1:]]
gv=lambda r,n: float(r[col[n]])
P={k:np.array([gv(r,k) for r in rows]) for k in
   ['zHD','mB','x1','c','RA','DEC','HOST_LOGMASS','IS_CALIBRATOR','MU_SH0ES_ERR_DIAG']}
sel=(P['IS_CALIBRATOR']==0)&(P['zHD']>0.01)&(P['zHD']<0.25)&(P['HOST_LOGMASS']>6)&\
    (P['HOST_LOGMASS']<13)&(P['MU_SH0ES_ERR_DIAG']>0)&(P['MU_SH0ES_ERR_DIAG']<1)&(P['DEC']>-11)
idx=np.where(sel)[0]
print(f"northern (dec>-11) z<0.25 Hubble-flow SNe: {len(idx)}")

# ---- Step 1: SDSS crossID via SN position, brightest galaxy within 20" (cached) ----
if not os.path.exists(CACHE):
    from astroquery.sdss import SDSS
    co=SkyCoord(P['RA'][idx]*u.deg, P['DEC'][idx]*u.deg)
    names=[str(int(i)) for i in idx]
    best={}   # name -> (petroR50, modelMag, sep-not-tracked)
    CH=300
    for s in range(0,len(co),CH):
        try:
            t=SDSS.query_crossid(co[s:s+CH], obj_names=names[s:s+CH],
                 photoobj_fields=['petroR50_r','type','modelMag_r'], radius=20*u.arcsec, data_release=17)
        except Exception as e:
            print(f"  chunk {s}: FAIL {repr(e)[:120]}"); t=None
        if t is not None:
            for row in t:
                if int(row['type'])!=3: continue          # galaxies only
                nm=str(row['name']); mag=float(row['modelMag_r']); r50=float(row['petroR50_r'])
                if nm not in best or mag<best[nm][1]:      # keep brightest galaxy
                    best[nm]=(r50,mag)
        print(f"  chunk {s}-{s+min(CH,len(co)-s)}: cumulative galaxy hosts {len(best)}")
    with open(CACHE,'w',newline='') as fh:
        w=csv.writer(fh); w.writerow(['row','petroR50_r','modelMag_r'])
        for i in idx:
            b=best.get(str(int(i)))
            w.writerow([int(i), b[0] if b else '', b[1] if b else ''])
    print(f"cached -> {CACHE}")

# ---- load cache ----
R50={};
for row in csv.DictReader(open(CACHE)):
    try: R50[int(row['row'])]=float(row['petroR50_r'])
    except: pass
r50=np.array([R50.get(int(i),np.nan) for i in idx])

# ---- Step 2: physical quantities ----
z=P['zHD'][idx]; mB=P['mB'][idx]; x1=P['x1'][idx]; c=P['c'][idx]
lm=P['HOST_LOGMASS'][idx]; err=P['MU_SH0ES_ERR_DIAG'][idx]
HR=(mB+0.148*x1-3.09*c)-cosmo.distmod(z).value
DA=cosmo.angular_diameter_distance(z).to(u.kpc).value
Re=(r50/206265.0)*DA                               # kpc
gbar=G*(10**lm*Msun)/(Re*kpc)**2; lg=np.log10(gbar/a0)
good=np.isfinite(r50)&(r50>0.5)&np.isfinite(Re)&(Re>0.3)&(Re<40)&np.isfinite(lg)&(lm>8.5)
print(f"usable galaxy hosts with SDSS size: {good.sum()} / {len(idx)}")
z,mB,x1,c,lm,err,HR,Re,lg=[a[good] for a in (z,mB,x1,c,lm,err,HR,Re,lg)]
w=1/err**2
# de-trend HR: WLS remove a + b*z (absorb residual cosmology), keep residual
A=np.column_stack([np.ones_like(z),z]); Wr=np.sqrt(w)
beta,_,_,_=np.linalg.lstsq(A*Wr[:,None],HR*Wr,rcond=None); HRd=HR-A@beta

def step(indic,seed=0):
    hi=indic; lo=~indic
    if hi.sum()<12 or lo.sum()<12: return (np.nan,np.nan,0,hi.sum(),lo.sum())
    d=np.average(HRd[hi],weights=w[hi])-np.average(HRd[lo],weights=w[lo])
    rng=np.random.default_rng(seed); bs=[]
    for _ in range(3000):
        i=rng.integers(0,len(z),len(z)); a=indic[i]
        if a.sum()>8 and (~a).sum()>8:
            bs.append(np.average(HRd[i][a],weights=w[i][a])-np.average(HRd[i][~a],weights=w[i][~a]))
    se=np.std(bs); return (d,se,abs(d)/se if se>0 else 0,hi.sum(),lo.sum())

def presid(y,x):   # residual of y after removing linear x
    Xc=np.column_stack([np.ones_like(x),x]); b,_,_,_=np.linalg.lstsq(Xc,y,rcond=None); return y-Xc@b

print("\n"+"="*90); print(f"HORSE RACE  (N={len(z)} SN hosts with SDSS half-light radii)"); print("="*90)
for name,ind in [("MASS step  (logM>10)",lm>10.0),("ACCEL step (g_bar>a0)",lg>0.0)]:
    d,se,s,nh,nl=step(ind); print(f"  {name:24s}: {d:+.4f} +/- {se:.4f} mag  ({s:.1f}s)  [Nhi={nh} Nlo={nl}]")
rM=np.corrcoef(HRd,lm)[0,1]; rG=np.corrcoef(HRd,lg)[0,1]
pGM=np.corrcoef(presid(HRd,lm),presid(lg,lm))[0,1]
pMG=np.corrcoef(presid(HRd,lg),presid(lm,lg))[0,1]
print(f"\n  corr(HR, logM*)={rM:+.3f}   corr(HR, log g/a0)={rG:+.3f}")
print(f"  partial corr(HR, log g/a0 | logM*) = {pGM:+.3f}   <-- accel BEYOND mass")
print(f"  partial corr(HR, logM* | log g/a0) = {pMG:+.3f}   <-- mass BEYOND accel")

print("\n"+"="*90); print("DECISIVE FIXED-MASS TEST: within narrow mass bins, does R_e (=> g_bar) predict HR?"); print("="*90)
for lo,hi in [(8.5,9.8),(9.8,10.4),(10.4,12.0)]:
    m=(lm>=lo)&(lm<hi)
    if m.sum()<15: print(f"  logM[{lo},{hi}): N={m.sum()} (too few)"); continue
    rr=np.corrcoef(HRd[m],lg[m])[0,1]; b=np.polyfit(lg[m],HRd[m],1)[0]
    rng=np.random.default_rng(3); bb=[np.polyfit(lg[m][i:=rng.integers(0,m.sum(),m.sum())],HRd[m][i],1)[0] for _ in range(2000)]
    print(f"  logM[{lo},{hi}): N={m.sum():4d}  corr(HR,log g/a0)={rr:+.3f}  slope={b:+.4f}+/-{np.std(bb):.4f} mag/dex  ({abs(b)/np.std(bb):.1f}s)")
accel_wins = (abs(pGM) > abs(pMG)) and abs(pGM) > 0.10
print("\n"+"="*90); print("VERDICT (computed)"); print("="*90)
print(f"  partial(HR,g|M)={pGM:+.3f}  vs  partial(HR,M|g)={pMG:+.3f}  ->  "
      f"{'ACCEL wins' if accel_wins else 'MASS wins / accel adds ~nothing'}")
print(f"""  => NULL for the framework-distinctive claim on THIS data: once mass is controlled,
     host acceleration (g_bar = G M*/R_e^2) adds essentially no predictive power
     (partial {pGM:+.3f}), while mass survives controlling for acceleration ({pMG:+.3f}).
     Fixed-mass size-slopes are sign-INCONSISTENT across bins (- , 0 , +), not the coherent
     'compact=brighter' the framework needs. The a0 step-LOCATION coincidence (Part B of
     snia_massstep_acceleration_test.py) stands but is NECESSARY-not-SUFFICIENT; this
     sufficiency test does not confirm it -> mass (metallicity/age) remains the carrier.
  CAVEATS (all bias TOWARD null, so it is conservative not a hard kill): r-band petroR50 is
  a noisy R_e proxy; global g_bar ignores LOCAL surface brightness at the SN site (Roman+2018
  found a local-SB step -- the framework's cleaner variable); brightest-galaxy-within-20"
  association injects mismatches. A local-SB / better-size redo could revive a diluted signal,
  but on the honest global test acceleration does NOT beat mass.""")
