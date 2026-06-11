#!/usr/bin/env python3
"""
agentZ: THE SECOND-VARIABLE HUNT — which lens property, BEYOND type and g_bar, drives the lensing-RAR offset?
Our own data end to end: lr_lenses.npz (v4, 181,477 isolated lenses) x KiDS DR4.1 SOM-gold shear (21.3M sources),
the agentK jackknife-stack pattern (50 sky patches), with ONE structural change: the per-lens accumulation cell is
(patch, TYPE x M*bin x ZBIN x DENSITY[3 definitions], g_bar bin) instead of (patch, type, g_bar bin), so EVERY
marginal, the full matrix offset(type, M*, z, density), and every pre-registered robustness swap come from a single
pass over the shear catalog (additivity of the estimator sums).

Context this closes: agentW Part 2 gate (c) — the lens-only slip partner "must carry a second variable, smooth in
halo mass (agentJ: sharp staircase refuted 7.3 sigma; smooth 1-halo-safe trend +0.122+-0.062 dex/dex)". This run
IDENTIFIES the second variable empirically, in our own measurement. Measurement only; no mechanism advocacy.

== PRE-REGISTERED DESIGN (locked before the stack ran) =====================================================
g_bar binning: accumulate the FULL 15 Brouwer bins (costless — the digitize is per source either way); analyze in
3 SUPER-BINS of 5 fine bins each, chosen for S/N per cell (a single fine bin at ~5k-lens matrix cells is 30-80%
noise -> log() undefined on negative draws; 5-bin amplitude fits are 6-16%). The super-bins map onto physics
(median lens, R = sqrt(G Mgal/g_bar)):
  SB1 = bins 0-4    g_bar 1e-15..1.7e-14    R ~ 0.62-2.6 Mpc   2-HALO-DOMINATED (environment lives here trivially)
  SB2 = bins 5-9    g_bar 1.7e-14..2.9e-13  R ~ 0.15-0.62 Mpc  transition
  SB3 = bins 10-14  g_bar 2.9e-13..5e-12    R <~ 0.15 Mpc      1-HALO-SAFE (= agentJ's clean bins 10-14, R < r200)
Offset statistic: per (cell, super-bin), GLS amplitude A of the cell's 5 fine-bin ESD against the FULL-SAMPLE
template T_b (diagonal weights T_b^2/var_jk,b frozen from a first jackknife pass); offset = log10 A. This is the
banked mean-Delta-log statistic made robust to noisy fine bins. Errors: 50-patch leave-one-out jackknife of the
COMPLETE statistic (template and cell re-measured per replica -> shared-patch/shared-template correlations
propagate). Combined-SB offset: 1/sigma^2-frozen-weighted mean of the three SB offsets.
Centroid guard: coarse bins admit a within-bin g_bar-distribution systematic (different Mgal mixes sample a fine
bin's interior differently; ESD log-slope ~0.3-0.7 -> a delta-dex centroid shift mimics ~0.5*delta offset). We
accumulate sum(w*log10 g_bar) per (patch,cell,bin) and report offsets RAW and CENTROID-CORRECTED
(E_b -> E_b * 10^(-s_b*(ell_b(cell)-ell_b(full))), s_b = template log-log slope). Both ways, by rule.
VARIABLES (per lens, all from our own catalogs):
  M*    : per-type terciles of logM* (catalog logM, +0.15 fluxscale system). The cell grid uses the 5 ABSOLUTE bins
          cut at the union of both types' tercile edges, so per-type terciles AND fixed-absolute-M* strata are both
          exact unions of accumulator cells.
  z     : two bins at the global lens median.
  DENSITY: the isolation-pipeline machinery (lr_esd_remeasure stage-lens KD-tree conventions, verbatim: unit-sphere
          chord ~ angle, transverse d = chord*chi_lens, comoving) counting pool neighbours in the 3-10 Mpc annulus
          with |Delta chi| < 10 Mpc (the count-calibrated isolation window). Inside 3 Mpc the isolated sample has
          ZERO mass-qualified neighbours BY CONSTRUCTION — reproducing that zero is the stage gate (GATE C).
          PRIMARY count: neighbours above an ADAPTIVE completeness floor = P20 of the pool's logM in the lens's
          dz=0.02 slice (the r<20 flux limit makes any fixed floor z-incomplete).
          VARIANTS (carried as real accumulator axes, not proxies): fixed floor logM>10.0; mass-qualified
          (logM_nb > logM_lens - 1, the isolation rule's own qualification).
          Density bin = TERCILE OF THE COUNT WITHIN THE LENS'S dz=0.02 z-SLICE (rank-normalization kills the
          survey-depth and photo-z-dilution z-trends by construction; integer ties broken by seeded jitter
          U(0,0.5), rng 20260610). Photo-z scatter MISASSIGNS some neighbours -> DILUTES a real density signal
          toward null; so a positive density verdict is conservative, and a NULL one carries the dilution caveat
          plus a z-lo-restricted row.
ACCUMULATOR: 540 cells = type(2) x absM*(5) x z(2) x dens_ad(3) x dens_10(3) x dens_q(3); every analysis object
is a re-marginalization. Cell sums are tiny; S/N lives in the merged analysis cells (>=~5k lenses).
VALIDATION GATES (all must pass before any sub-split is interpreted):
  GATE A (machine): summing cells reproduces the banked agentK accumulators lr_esd_jackknife.npz per
          (patch,type,bin) to allclose rtol 1e-8 (FP reordering only).
  GATE B (banked numbers): the agentK analysis re-run on the marginalized accumulators reproduces, at printed
          precision: chi2(early-late)=126.0 raw -> 9.1 sigma; Hartlap(0.673) 84.8 -> 6.8 SIGMA HEADLINE;
          mean +0.209 dex; 14/15 bins; diag 7.1 sigma; 25-patch 24.6/13.1; per-class-vs-released 1.3/0.4 sigma.
  GATE C (density machinery): zero mass-qualified neighbours within 3 Mpc & |dchi|<10 for all 181,477 lenses.
PRE-REGISTERED READINGS (decision rules; sigma = jackknife):
  Stratified contrast Delta_V (per type t, per SB and combined): Mantel-Haenszel-style sum over strata of the
  OTHER two variables, harmonic-N_eff weights, strata with min(N)<1000 dropped (count printed).
  DRIVER(V):  |Delta_comb| >= 3 sigma AND sign(SB3)==sign(comb) AND |Delta_SB3| >= 1.5 sigma_SB3.
              (The SB3 condition is the 2-HALO GUARD: environment/clustering moves SB1 trivially; an RAR-level
              second variable must move the 1-halo-safe bins.)
  TREND(V):   1.5-3 sigma combined (reported, no driver claim; agentJ-consistency noted for M*).
  NULL(V):    < 1.5 sigma.
  Readings: DENSITY-DRIVEN / MASS-DRIVEN = DRIVER(dens)/DRIVER(M*) in either type; MIXED = DRIVERs among >=2
  DISTINCT variables; TYPE-IRREDUCIBLE = no DRIVER among {M*, z, dens} while the stratified TYPE contrast at fixed
  (absolute-M* bin, z, density) stays >= 3 sigma. A claimed DRIVER must additionally survive (>=2 sigma, same
  sign): the centroid-correction toggle; the density-definition swaps (for dens; real re-marginalizations here);
  the agentH conversion column (for M*: per-cell <nfw_C(x)> differential, M13 SHMR x D08 c(M,z) — the banked
  primary chain — added to the ESD contrast to form the g_obs-level contrast).
============================================================================================================
m-bias caveat (inherited from agentK, stated up front): raw lensfit e1/e2, no (1+K) correction -> all ESDs ~1.5%
low vs the released convention; CONSTANT and cell-shared -> cancels in every offset and contrast here.
Inline, no swarms. agentZ for C. Zimmerman, 2026-06-10/11. No git operations.
"""
import numpy as np, os, sys, argparse
from scipy import stats
from scipy.spatial import cKDTree

HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
from agentK_jackknife_stack import assign_patches, DC, NPATCH   # identical patches + comoving distance
from esd_conversion import nfw_C                                 # validated C(x): C(2)=4.000 anchor

D=os.path.join(HERE,'..','..','data','lensing_rar')
c_=2.998e8; G=6.674e-11; Msun=1.989e30; Mpc=3.0857e22; H0=70*1e3/Mpc; Om,OL=0.3,0.7
F_DENS=os.path.join(D,'agentZ_density.npz'); F_STACK=os.path.join(D,'agentZ_stack.npz')
NCELL=540   # cell = t*270 + m5*54 + iz*27 + d_ad*9 + d_10*3 + d_q
SBS={'SB1':list(range(0,5)),'SB2':list(range(5,10)),'SB3':list(range(10,15))}
SBORD=['SB1','SB2','SB3']

def cell_decode():
    cell=np.arange(NCELL)
    return cell//270,(cell//54)%5,(cell//27)%2,(cell//9)%3,(cell//3)%3,cell%3   # CT,CM,CZ,CDad,CD10,CDq

# ============================== STAGE 1: DENSITY ==============================
def stage_density():
    print("="*100); print("STAGE density — neighbour counts (3-10 Mpc annulus, |dchi|<10 Mpc) + cell assignment")
    print("="*100,flush=True)
    from astropy.io import fits
    b=fits.open(os.path.join(D,'KiDS_DR4_brightsample.fits'))[1].data
    L=fits.open(os.path.join(D,'KiDS_DR4_brightsample_LePhare.fits'))[1].data
    assert np.array_equal(b['ID'],L['ID'])
    r=b['MAG_AUTO_CALIB']; zb=np.array(b['zphot_ANNz2'],dtype='f8'); masked=b['masked']
    FLUXSCALE_DEX=0.15                                  # v4 system (lr_esd_remeasure.py)
    logM=np.array(L['MASS_MED'],dtype='f8')+FLUXSCALE_DEX
    ra=np.array(b['RAJ2000'],dtype='f8'); dec=np.array(b['DECJ2000'],dtype='f8')
    pool=(r<20)&(zb>0.1)&(zb<0.5)&(masked==0)&np.isfinite(logM)&(logM>7)    # stage-lens pool, verbatim
    print(f"pool (v4 fluxscale system): {pool.sum():,} of {len(b):,}")
    ip=np.where(pool)[0]
    zP=zb[ip]; logMP=logM[ip]; chiP=DC(zP)
    raP,decP=np.radians(ra[ip]),np.radians(dec[ip])
    xyzP=np.c_[np.cos(decP)*np.cos(raP),np.cos(decP)*np.sin(raP),np.sin(decP)]
    tree=cKDTree(xyzP)
    ln=np.load(os.path.join(D,'lr_lenses.npz'))
    NL=len(ln['z']); assert NL==181477, f"expected v4 catalog (181,477), got {NL}"
    raL,decL=np.radians(np.array(ln['ra'],'f8')),np.radians(np.array(ln['dec'],'f8'))
    xyzL=np.c_[np.cos(decL)*np.cos(raL),np.cos(decL)*np.sin(raL),np.sin(decL)]
    # --- exact match of each lens back to its pool row (self-exclusion + field cross-check) ---
    dist,selfidx=tree.query(xyzL,k=1)
    ok=(dist<1e-9)&(np.abs(logMP[selfidx]-ln['logM'])<1e-8)&(np.abs(chiP[selfidx]-ln['chi'])<1e-6)
    print(f"lens->pool exact match: {ok.sum():,}/{NL:,} (max pos dev {dist.max():.2e} rad, "
          f"max dlogM {np.abs(logMP[selfidx]-ln['logM']).max():.2e}, max dchi {np.abs(chiP[selfidx]-ln['chi']).max():.2e} Mpc)")
    assert ok.all(), "lens catalog does not match regenerated pool — pool reconstruction differs, STOP"
    # --- adaptive completeness floor per dz=0.02 slice: P20 of POOL logM in the slice ---
    edges_z=np.round(np.arange(0.10,0.501,0.02),3); nsl=len(edges_z)-1
    slP=np.clip(np.searchsorted(edges_z,zP,side='right')-1,0,nsl-1)
    floor_sl=np.array([np.percentile(logMP[slP==s],20) if (slP==s).sum()>100 else 10.0 for s in range(nsl)])
    zL=np.array(ln['z'],'f8'); chiL=np.array(ln['chi'],'f8'); logML=np.array(ln['logM'],'f8')
    slL=np.clip(np.searchsorted(edges_z,zL,side='right')-1,0,nsl-1)
    floorL=floor_sl[slL]
    print("z-slice completeness floors (P20 of pool logM): "
          +", ".join(f"{edges_z[s]:.2f}:{floor_sl[s]:.2f}" for s in range(nsl)))
    # --- neighbour counts ---
    n_ad=np.zeros(NL,np.int32); n_10=np.zeros(NL,np.int32); n_q=np.zeros(NL,np.int32); n_inner=np.zeros(NL,np.int32)
    CH=10000
    for i0 in range(0,NL,CH):
        sl=slice(i0,min(i0+CH,NL))
        rads=10.0/chiL[sl]                                   # chord ~ angle, the stage-lens convention
        lists=tree.query_ball_point(xyzL[sl],r=rads)
        for k,js in enumerate(lists):
            i=i0+k
            js=np.asarray(js,dtype=int); js=js[js!=selfidx[i]]
            if js.size==0: continue
            js=js[np.abs(chiP[js]-chiL[i])<10.0]             # the count-calibrated isolation window
            if js.size==0: continue
            dt=np.linalg.norm(xyzP[js]-xyzL[i],axis=1)*chiL[i]   # transverse comoving Mpc (chord*chi)
            q=logMP[js]>logML[i]-1.0
            n_inner[i]=int(np.sum((dt<=3.0)&q))              # GATE C: must be 0 (isolation criterion)
            ann=(dt>3.0)&(dt<10.0)
            n_q[i] =int(np.sum(ann&q))
            n_10[i]=int(np.sum(ann&(logMP[js]>10.0)))
            n_ad[i]=int(np.sum(ann&(logMP[js]>floorL[i])))
        if (i0//CH)%5==0 or i0+CH>=NL: print(f"  lenses {min(i0+CH,NL):,}/{NL:,}",flush=True)
    viol=int(np.sum(n_inner>0))
    print(f"\nGATE C (isolation reproduction): lenses with a mass-qualified neighbour at d_t<=3 Mpc, |dchi|<10: {viol}")
    if viol>0:
        bad=np.where(n_inner>0)[0][:5]
        for i in bad: print(f"  VIOLATION lens {i}: n_inner={n_inner[i]} (logM*={logML[i]:.2f}, z={zL[i]:.3f})")
        sys.exit("GATE C FAILED — density machinery does not reproduce the isolation pipeline. STOP.")
    print("GATE C PASSED — the density machinery reproduces the isolation criterion exactly (0 of 181,477).")
    # --- density terciles within z-slice (rank-normalized), jittered ties ---
    rng=np.random.default_rng(20260610)
    def terciles_in_slice(cnt):
        v=cnt+rng.uniform(0,0.5,NL); idn=np.zeros(NL,np.int8)
        for s in range(nsl):
            m=slL==s
            if m.sum()<30: continue
            qq=np.quantile(v[m],[1/3,2/3]); idn[m]=np.digitize(v[m],qq).astype(np.int8)
        return idn
    idn_ad=terciles_in_slice(n_ad); idn_10=terciles_in_slice(n_10); idn_q=terciles_in_slice(n_q)
    print("\ncount distributions (P16/50/84) by z-slice (PRIMARY=adaptive | fixed10 | qualified) + zero-frac(ad):")
    for s in range(0,nsl,2):
        m=slL==s
        if m.sum()<100: continue
        pa=np.percentile(n_ad[m],[16,50,84]); p1=np.percentile(n_10[m],[16,50,84]); pq=np.percentile(n_q[m],[16,50,84])
        print(f"  z {edges_z[s]:.2f}-{edges_z[s+1]:.2f} (N={m.sum():6,}): ad {pa[0]:4.0f}/{pa[1]:4.0f}/{pa[2]:4.0f} | "
              f"f10 {p1[0]:4.0f}/{p1[1]:4.0f}/{p1[2]:4.0f} | q {pq[0]:4.0f}/{pq[1]:4.0f}/{pq[2]:4.0f} | "
              f"zero(ad) {100*np.mean(n_ad[m]==0):4.1f}%")
    print(f"  variant label agreement vs primary: fixed10 {100*np.mean(idn_10==idn_ad):.1f}%, "
          f"qualified {100*np.mean(idn_q==idn_ad):.1f}%")
    # --- M* per-type terciles -> absolute 5-bin grid; z median ---
    typ=np.array(ln['typ'],int)
    ed={}
    for t in (0,1): ed[t]=np.percentile(logML[typ==t],[100/3,200/3])
    abs_edges=np.sort(np.concatenate([ed[0],ed[1]]))
    im5=np.digitize(logML,abs_edges).astype(np.int8)         # 0..4
    iterc=np.where(logML<np.where(typ==1,ed[1][0],ed[0][0]),0,
           np.where(logML<np.where(typ==1,ed[1][1],ed[0][1]),1,2)).astype(np.int8)
    zmed=float(np.median(zL)); iz=(zL>=zmed).astype(np.int8)
    print(f"\nM* tercile edges: late {ed[0][0]:.3f}/{ed[0][1]:.3f}  early {ed[1][0]:.3f}/{ed[1][1]:.3f}")
    print(f"absolute 5-bin edges: {np.round(abs_edges,3)};  z median split at {zmed:.4f}")
    cell=(typ*270+im5.astype(int)*54+iz.astype(int)*27+idn_ad.astype(int)*9
          +idn_10.astype(int)*3+idn_q.astype(int)).astype(np.int16)
    Ncell=np.bincount(cell,minlength=NCELL)
    print(f"\n540-cell accumulator grid: occupied {int(np.sum(Ncell>0))}/540")
    print("analysis-cell occupancy, primary 36-matrix granularity (t, M* tercile, z, dens_ad):")
    for t,lab in ((1,'early'),(0,'late')):
        for k in range(3):
            ns=[int(np.sum((typ==t)&(iterc==k)&(iz==z_)&(idn_ad==dd))) for z_ in range(2) for dd in range(3)]
            print(f"  {lab} terc{k}: "+" ".join(f"{x:6,}" for x in ns)+f"   (min {min(ns):,})")
    # --- entanglement diagnostics ---
    print("\nentanglement (Spearman):")
    for t,lab in ((1,'early'),(0,'late')):
        m=typ==t
        print(f"  {lab}: rho(n_ad,logM*)={stats.spearmanr(n_ad[m],logML[m]).statistic:+.3f}  "
              f"rho(idn_ad,logM*)={stats.spearmanr(idn_ad[m],logML[m]).statistic:+.3f}  "
              f"rho(idn_ad,z)={stats.spearmanr(idn_ad[m],zL[m]).statistic:+.3f}")
    for k in range(3):
        m=idn_ad==k
        print(f"  dens tercile {k}: early fraction {100*np.mean(typ[m]==1):.1f}%   "
              f"med logM* early {np.median(logML[m&(typ==1)]):.3f} late {np.median(logML[m&(typ==0)]):.3f}")
    np.savez(F_DENS,n_ad=n_ad,n_10=n_10,n_q=n_q,floorL=floorL,slL=slL,idn_ad=idn_ad,idn_10=idn_10,idn_q=idn_q,
             im5=im5,iterc=iterc,iz=iz,cell=cell,typ=typ,logM=logML,Mgal=np.array(ln['Mgal'],'f8'),z=zL,
             abs_edges=abs_edges,ed_late=ed[0],ed_early=ed[1],zmed=zmed,edges_z=edges_z,floor_sl=floor_sl,Ncell=Ncell)
    print(f"\n-> wrote {F_DENS}",flush=True)

# ============================== STAGE 2: STACK ==============================
def stage_stack():
    print("="*100); print("STAGE stack — single pass, accumulators per (50 patches, 540 cells, 15 g_bar bins)")
    print("="*100,flush=True)
    from astropy.io import fits
    F=os.path.join(D,'KiDS_DR4.1_SOM_gold_WL_cat.fits')
    if not os.path.exists(F): sys.exit("shear catalog not present")
    ln=np.load(os.path.join(D,'lr_lenses.npz')); dn=np.load(F_DENS)
    cell=dn['cell']; assert len(cell)==len(ln['z'])
    patch=assign_patches(np.array(ln['ra'],dtype='f8'),np.array(ln['dec'],dtype='f8'))
    cnt=np.bincount(patch,minlength=NPATCH)
    print(f"patches: {NPATCH}; lens counts min/med/max = {cnt.min()}/{int(np.median(cnt))}/{cnt.max()}",flush=True)
    h=fits.open(F,memmap=True); s=h[1].data
    cols={cc.name.upper():cc.name for cc in h[1].columns}
    def col(*names):
        for nm in names:
            if nm.upper() in cols: return np.array(s[cols[nm.upper()]],dtype='f8')
        raise KeyError(names)
    raS=col('RAJ2000','ALPHA_J2000','RA'); decS=col('DECJ2000','DELTA_J2000','DEC')
    e1=col('e1','BIAS_CORRECTED_E1'); e2=col('e2','BIAS_CORRECTED_E2')
    w=col('weight','RECAL_WEIGHT','LFWEIGHT'); zB=col('Z_B','ZB','Z_B_BPZ')
    print(f"sources: {len(raS):,}",flush=True)
    zl=ln['z']; chil=ln['chi']
    treeS=cKDTree(np.c_[np.radians(raS),np.radians(decS)])   # agentK verbatim: small-angle chord ~ angle
    gbar_edges=np.logspace(np.log10(1e-15),np.log10(5e-12),16)
    wgE=np.zeros((NPATCH,NCELL,15)); W=np.zeros((NPATCH,NCELL,15)); NN=np.zeros((NPATCH,NCELL,15))
    WLG=np.zeros((NPATCH,NCELL,15))                          # sum w*inv_sc^2*log10(gbar): per-bin centroids
    chunk=2000
    for i0 in range(0,len(zl),chunk):
        sl=slice(i0,min(i0+chunk,len(zl)))
        for j,(rl,dl,zl_,chil_,Mg,ce,pa) in enumerate(zip(ln['ra'][sl],ln['dec'][sl],zl[sl],chil[sl],
                                                          ln['Mgal'][sl],cell[sl],patch[sl])):
            ce=int(ce); pa=int(pa)
            theta_max=3.0*(1+zl_)/chil_                      # 3 Mpc PROPER transverse (agentK verbatim)
            ii=treeS.query_ball_point([np.radians(rl),np.radians(dl)],theta_max)
            ii=np.array(ii,dtype=int)
            if ii.size<5: continue
            back=zB[ii]>zl_+0.2
            ii=ii[back]
            if ii.size<5: continue
            dra=(np.radians(raS[ii])-np.radians(rl))*np.cos(np.radians(dl)); dde=np.radians(decS[ii])-np.radians(dl)
            R=np.hypot(dra,dde)*chil_/(1+zl_)
            phi=np.arctan2(dde,dra)
            et=-(e1[ii]*np.cos(2*phi)-e2[ii]*np.sin(2*phi))
            chis=DC(zB[ii]); Dls=(chis-chil_)/(1+zB[ii]); Dl=chil_/(1+zl_); Ds=chis/(1+zB[ii])
            inv_sc=np.clip(4*np.pi*G/(c_**2)*(Dl*Mpc)*(Dls/Ds),0,None)
            gbar=G*Mg*Msun/(R*Mpc)**2
            k=np.digitize(gbar,gbar_edges)-1
            ok=(k>=0)&(k<15)&(inv_sc>0)
            ww=w[ii]*inv_sc**2
            A_g,A_w,A_n,A_l=wgE[pa,ce],W[pa,ce],NN[pa,ce],WLG[pa,ce]
            np.add.at(A_g,k[ok],(ww*et/np.where(inv_sc>0,inv_sc,1))[ok])
            np.add.at(A_w,k[ok],ww[ok]); np.add.at(A_n,k[ok],1)
            np.add.at(A_l,k[ok],(ww*np.log10(np.where(gbar>0,gbar,1)))[ok])
        if (i0//chunk)%10==0 or i0+chunk>=len(zl):
            print(f"  lenses {min(i0+chunk,len(zl)):,}/{len(zl):,}",flush=True)
    np.savez(F_STACK,wgE=wgE,W=W,NN=NN,WLG=WLG,gbar_edges=gbar_edges,patch=patch)
    print(f"-> wrote {F_STACK}",flush=True)

# ============================== STAGE 3: ANALYZE ==============================
def stage_analyze():
    print("="*100)
    print("STAGE analyze — gates first, then the matrix. PRE-REGISTERED RULES (locked in the module header):")
    print("  offset = log10 GLS-amplitude vs full-sample template per super-bin; 50-patch jackknife of everything;")
    print("  stratified extreme-bin contrasts, harmonic-N weights, strata with min(N)<1000 dropped;")
    print("  DRIVER: |comb|>=3sig AND sign(SB3)==sign(comb) AND |SB3|>=1.5sig  (SB3 = the 2-halo guard);")
    print("  TREND 1.5-3sig; NULL <1.5sig; TYPE-IRREDUCIBLE if no driver but stratified type contrast >=3sig;")
    print("  DRIVER robustness: centroid toggle; density-definition re-marginalizations; agentH conversion column.")
    print("="*100,flush=True)
    zs=np.load(F_STACK); dn=np.load(F_DENS)
    wgE,W,NN,WLG=zs['wgE'],zs['W'],zs['NN'],zs['WLG']; gbar_edges=zs['gbar_edges']
    cen=np.sqrt(gbar_edges[:-1]*gbar_edges[1:]); n=15; N=NPATCH
    KG=Msun/(3.0857e16)**2
    CT,CM,CZ,CDad,CD10,CDq=cell_decode()
    DAX={'ad':CDad,'10':CD10,'q':CDq}
    typ=dn['typ']; logML=dn['logM']; MgalL=dn['Mgal']; zL=dn['z']
    cellL=dn['cell']; Ncell=np.bincount(cellL,minlength=NCELL)
    ed={0:dn['ed_late'],1:dn['ed_early']}
    mids=np.concatenate([[dn['abs_edges'][0]-0.5],0.5*(dn['abs_edges'][1:]+dn['abs_edges'][:-1]),
                         [dn['abs_edges'][-1]+0.5]])
    TS={t:{k:[m for m in range(5) if (0 if mids[m]<ed[t][0] else (1 if mids[m]<ed[t][1] else 2))==k]
           for k in range(3)} for t in (0,1)}
    print(f"per-type tercile -> absolute-bin sets: late {TS[0]}  early {TS[1]}")
    # ---------------- GATE A ----------------
    print("\n=== GATE A: cell-summed accumulators vs banked lr_esd_jackknife.npz (rtol 1e-8) ===")
    old=np.load(os.path.join(D,'lr_esd_jackknife.npz'))
    mine={'wgE':np.zeros((N,2,n)),'W':np.zeros((N,2,n)),'NN':np.zeros((N,2,n))}
    for t in (0,1):
        m=np.where(CT==t)[0]
        mine['wgE'][:,t]=wgE[:,m].sum(1); mine['W'][:,t]=W[:,m].sum(1); mine['NN'][:,t]=NN[:,m].sum(1)
    okA=True
    for key in ('wgE','W','NN'):
        a,b=mine[key],old[key]
        dev=np.max(np.abs(a-b)/np.maximum(np.abs(b),1e-300))
        okk=np.allclose(a,b,rtol=1e-8,atol=0); okA&=okk
        print(f"  {key}: max rel dev {dev:.2e}  -> {'PASS' if okk else 'FAIL'}")
    if not okA: sys.exit("GATE A FAILED — the cell-granular stack does not reproduce the banked accumulators. STOP.")
    print("GATE A PASSED.")
    # ---------------- GATE B ----------------
    print("\n=== GATE B: banked split statistics from the marginalized accumulators ===")
    tot_g=mine['wgE'].sum(0); tot_w=mine['W'].sum(0)
    esd=tot_g/np.maximum(tot_w,1e-300)/KG
    loo=(tot_g[None]-mine['wgE'])/np.maximum(tot_w[None]-mine['W'],1e-300)/KG
    sig=lambda c2,df=n: stats.norm.isf(0.5*stats.chi2.sf(c2,df=df))
    B=os.path.join(D,'brouwer2021_rar')
    late=np.loadtxt(os.path.join(B,'Fig-8_RAR-KiDS-isolated_Colorbin_1.txt'))
    early=np.loadtxt(os.path.join(B,'Fig-8_RAR-KiDS-isolated_Colorbin_2.txt'))
    rel={0:late[:,1]/late[:,4],1:early[:,1]/early[:,4]}
    covraw=np.loadtxt(os.path.join(B,'Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt'))
    rad=np.unique(covraw[:,2]); cb={0.0:0,2.5:1}
    C30r=np.zeros((2*n,2*n))
    for m_,nn_,ri,rj,cv,_,bias in covraw:
        i=cb[m_]*n+int(np.argmin(abs(rad-ri))); jx=cb[nn_]*n+int(np.argmin(abs(rad-rj))); C30r[i,jx]=cv/bias
    X=np.concatenate([loo[:,0,:],loo[:,1,:]],axis=1); Rm=X-X.mean(0)
    C30=(N-1)/N*(Rm.T@Rm)
    checks=[]
    for ty,lab,bank in ((0,'late',1.3),(1,'early',0.4)):
        dlt=esd[ty]-rel[ty]
        Csum=C30[ty*n:(ty+1)*n,ty*n:(ty+1)*n]+C30r[ty*n:(ty+1)*n,ty*n:(ty+1)*n]
        s=sig(float(dlt@np.linalg.solve(Csum,dlt)))
        checks.append((f"{lab} vs released (fullcov)",f"{s:.1f}s",f"{bank}s",abs(s-bank)<=0.051))
    d=esd[1]-esd[0]
    Dp=loo[:,1,:]-loo[:,0,:]; Rd=Dp-Dp.mean(0)
    Cd=(N-1)/N*(Rd.T@Rd)
    chi2=float(d@np.linalg.solve(Cd,d)); hart=(N-n-2)/(N-1); chi2h=hart*chi2
    nup=int(np.sum(d>0)); mdex=float(np.mean(np.log10(esd[1]/esd[0])))
    chi2diag=float(np.sum(d**2/np.diag(Cd)))
    g25=np.add.reduceat(mine['wgE'],np.arange(0,N,2),axis=0); w25=np.add.reduceat(mine['W'],np.arange(0,N,2),axis=0)
    loo25=(tot_g[None]-g25)/np.maximum(tot_w[None]-w25,1e-300)/KG
    Dp25=loo25[:,1,:]-loo25[:,0,:]; Rd25=Dp25-Dp25.mean(0)
    Cd25=(25-1)/25*(Rd25.T@Rd25)
    chi2_25=float(d@np.linalg.solve(Cd25,d)); h25=(25-n-2)/(25-1)
    checks+=[("early>late bins",f"{nup}/15","14/15",nup==14),
             ("mean dlog10(ESD)",f"{mdex:+.3f}","+0.209",abs(mdex-0.209)<0.002),
             ("chi2 raw",f"{chi2:.1f} ({sig(chi2):.1f}s)","126.0 (9.1s)",abs(chi2-126.0)<0.5),
             ("Hartlap HEADLINE",f"{chi2h:.1f} ({sig(chi2h):.1f}s)","84.8 (6.8s)",abs(chi2h-84.8)<0.5),
             ("diag-only",f"{sig(chi2diag):.1f}s","7.1s",abs(sig(chi2diag)-7.1)<=0.051),
             ("25-patch raw/Hartlap",f"{sig(chi2_25):.1f}/{sig(h25*chi2_25):.1f}s","24.6/13.1s",
              abs(sig(chi2_25)-24.6)<=0.051 and abs(sig(h25*chi2_25)-13.1)<=0.051)]
    allok=True
    for lab,got,bank,okk in checks:
        allok&=okk; print(f"  {lab:28s} {got:>20s}   banked {bank:>14s}   {'OK' if okk else 'MISMATCH'}")
    if not allok: sys.exit("GATE B FAILED — banked numbers not reproduced. No sub-split is interpreted. STOP.")
    print("GATE B PASSED — the banked 6.8-sigma split reproduces; sub-splits may now be interpreted.")
    # ---------------- offset machinery ----------------
    _sub={}
    def subset(cells):
        key=tuple(sorted(cells))
        if key not in _sub:
            ix=list(key)
            g=wgE[:,ix,:].sum(1); w_=W[:,ix,:].sum(1)
            tg=g.sum(0); tw=w_.sum(0)
            E=tg/np.maximum(tw,1e-300)/KG
            lo=(tg[None]-g)/np.maximum(tw[None]-w_,1e-300)/KG
            lg=WLG[:,ix,:].sum(1).sum(0)/np.maximum(tw,1e-300)
            _sub[key]=(E,lo,tw,lg)
        return _sub[key]
    ALL=tuple(range(NCELL))
    Tfull,Tloo,Wfull,LGfull=subset(ALL)
    lcen=np.log10(cen)
    s_b=np.gradient(np.log10(Tfull),lcen)            # template log-log slope (centroid correction)
    print("\ntemplate (full sample) per fine bin: ESD, log-log slope, weighted-centroid offset from bin centre:")
    print("  bin  g_bar      ESD       slope   <log g>-log g_cen")
    for b_ in range(n):
        print(f"  {b_:3d}  {cen[b_]:.2e}  {Tfull[b_]:8.3f}  {s_b[b_]:+.3f}    {LGfull[b_]-lcen[b_]:+.4f}")
    _off={}
    def offset(cells,sb,corrected=False):
        """offset (log10 amplitude vs full template) over SBS[sb]; returns (off, off_p[50], sigma)."""
        key=(tuple(sorted(cells)),sb,corrected)
        if key in _off: return _off[key]
        E,lo,tw,lg=subset(cells)
        bb=[b_ for b_ in SBS[sb] if tw[b_]>0]
        var=(N-1)/N*((lo-lo.mean(0))**2).sum(0)
        E=E.copy(); lo=lo.copy()
        if corrected:
            sh=10**np.clip(-s_b*(lg-LGfull),-1,1); E=E*sh; lo=lo*sh[None,:]
        wb=np.array([Tfull[b_]**2/max(var[b_],1e-300) for b_ in bb])
        A=float(np.sum(wb*E[bb]/Tfull[bb])/np.sum(wb))
        Ap=np.array([np.sum(wb*lo[p,bb]/Tloo[p,bb])/np.sum(wb) for p in range(N)])
        if A<=0 or np.any(Ap<=0) or len(bb)==0:
            _off[key]=(np.nan,np.full(N,np.nan),np.nan); return _off[key]
        off=float(np.log10(A)); offp=np.log10(Ap)
        sg=float(np.sqrt((N-1)/N*np.sum((offp-offp.mean())**2)))
        _off[key]=(off,offp,sg); return _off[key]
    def comb(cells,corrected=False):
        os_=[offset(cells,sb,corrected) for sb in SBORD]
        if any(np.isnan(o[0]) for o in os_): return (np.nan,np.full(N,np.nan),np.nan)
        u=np.array([1/max(o[2],1e-300)**2 for o in os_])
        off=float(np.sum(u*np.array([o[0] for o in os_]))/u.sum())
        offp=np.sum(u[:,None]*np.array([o[1] for o in os_]),axis=0)/u.sum()
        sg=float(np.sqrt((N-1)/N*np.sum((offp-offp.mean())**2)))
        return off,offp,sg
    def jsig(statp):
        return float(np.sqrt((N-1)/N*np.sum((statp-np.mean(statp))**2)))
    def cells_of(t=None,m5=None,iz_=None,terc=None,dens=None,densdef='ad'):
        m=np.ones(NCELL,bool)
        if t is not None: m&=CT==t
        if m5 is not None: m&=np.isin(CM,np.atleast_1d(m5))
        if terc is not None: m&=np.isin(CM,TS[t][terc])
        if iz_ is not None: m&=CZ==iz_
        if dens is not None: m&=DAX[densdef]==dens
        return tuple(np.where(m)[0])
    NC=lambda cells: int(Ncell[list(cells)].sum())
    # ---------------- agentH conversion chain (M13 x D08 primary) ----------------
    def moster13_mstar(logMh,zz):
        zf=zz/(1+zz)
        logM1=11.590+1.195*zf; Nn=0.0351-0.0247*zf; beta=1.376-0.826*zf; gam=0.608+0.329*zf
        r_=10**(logMh-logM1); return logMh+np.log10(2*Nn/(r_**-beta+r_**gam))
    grid=np.arange(10.0,15.5,0.005); znodes=np.round(np.arange(0.10,0.501,0.01),3)
    idxz=np.clip(np.round((zL-0.10)/0.01).astype(int),0,len(znodes)-1)
    logMh=np.empty_like(logML)
    for kz,zn in enumerate(znodes):
        m=idxz==kz
        if m.any(): logMh[m]=np.interp(logML[m],moster13_mstar(grid,zn),grid)
    rho_c0=3*H0**2/(8*np.pi*G)
    cD08=5.71*((10**logMh)/(2e12/0.72))**-0.084*(1+zL)**-0.47
    rD=(3*10**logMh*Msun/(4*np.pi*200.0*rho_c0*(Om*(1+zL)**3+OL)))**(1/3)/Mpc
    rsL=rD/cD08
    _C={}
    def Cvec(lensmask):
        key=lensmask.tobytes()
        if key not in _C:
            out=np.zeros(n)
            for b_ in range(n):
                R=np.sqrt(G*MgalL[lensmask]*Msun/cen[b_])/Mpc
                m=(R>0.03)&(R<3.0)
                out[b_]=np.mean(nfw_C(R[m]/rsL[lensmask][m])) if m.sum()>10 else np.nan
            _C[key]=out
        return _C[key]
    Cfull=Cvec(np.ones(len(logML),bool))
    def dlogC(lensmask,sb): return float(np.nanmean(np.log10(Cvec(lensmask)/Cfull)[SBS[sb]]))
    def lensmask_of(cells): return np.isin(cellL,list(cells))
    # ---------------- bridge: type marginals ----------------
    print("\n=== type marginals (bridge to the banked battery; offsets vs full-sample template, dex) ===")
    tt={}
    for t,lab in ((1,'early'),(0,'late')):
        cl=cells_of(t=t); row=[]
        for sb in SBORD:
            o=offset(cl,sb); row.append(f"{o[0]:+.3f}+-{o[2]:.3f}")
        oc=comb(cl); tt[t]=oc
        print(f"  {lab:6s} (N={NC(cl):7,})  "+"   ".join(row)+f"   comb {oc[0]:+.3f}+-{oc[2]:.3f}")
    dspp=tt[1][1]-tt[0][1]; dsp=tt[1][0]-tt[0][0]
    print(f"  split (early-late) combined: {dsp:+.3f} +- {jsig(dspp):.3f} dex ({abs(dsp)/jsig(dspp):.1f} sigma in"
          f" amplitude form; banked 15-bin chi2 form: +0.209 dex, 6.8 sigma)")
    for sb in SBORD:
        oe=offset(cells_of(t=1),sb); ol=offset(cells_of(t=0),sb)
        ddp=oe[1]-ol[1]; dd=oe[0]-ol[0]
        print(f"    split per {sb}: {dd:+.3f} +- {jsig(ddp):.3f} dex  ({abs(dd)/jsig(ddp):.1f} sigma)")
    # ---------------- 1-D marginals per type ----------------
    print("\n=== 1-D marginals per type (offsets vs template; SB1 | SB2 | SB3 | combined) ===")
    res1d={}
    for t,lab in ((1,'early'),(0,'late')):
        print(f"-- {lab} --")
        for V,nb in (('M*',3),('z',2),('dens',3)):
            offs=[]
            for k in range(nb):
                cl=cells_of(t=t,terc=k) if V=='M*' else (cells_of(t=t,iz_=k) if V=='z' else cells_of(t=t,dens=k))
                row=[offset(cl,sb) for sb in SBORD]; oc=comb(cl); offs.append((cl,row,oc))
                msk=lensmask_of(cl)
                med=np.median(logML[msk]) if V=='M*' else (np.median(zL[msk]) if V=='z' else np.median(dn['n_ad'][msk]))
                print(f"  {V:4s} bin {k} (N={NC(cl):7,}, med {med:7.3f}): "
                      +" | ".join(f"{r[0]:+.3f}+-{r[2]:.3f}" for r in row)+f" | comb {oc[0]:+.3f}+-{oc[2]:.3f}")
            res1d[(t,V)]=offs
            ddp=offs[-1][2][1]-offs[0][2][1]; dd=offs[-1][2][0]-offs[0][2][0]; sgg=jsig(ddp)
            print(f"    extreme-bin Delta (UNstratified, comb): {dd:+.3f} +- {sgg:.3f}  ({dd/max(sgg,1e-300):+.1f} sigma)")
        offs=res1d[(t,'M*')]
        x=np.array([np.median(logML[lensmask_of(o[0])]) for o in offs])
        for tag,pick in (('comb',lambda o:o[2]),('SB3',lambda o:o[1][2])):
            y=np.array([pick(o)[0] for o in offs]); yp=np.array([pick(o)[1] for o in offs])
            wq=np.array([1/max(pick(o)[2],1e-300)**2 for o in offs])
            xb=np.sum(wq*x)/wq.sum(); den=np.sum(wq*(x-xb)**2)
            sl=float(np.sum(wq*(x-xb)*y)/den); slp=np.sum(wq[:,None]*(x-xb)[:,None]*yp,axis=0)/den
            print(f"    M* slope ({tag}): {sl:+.3f} +- {jsig(slp):.3f} dex/dex"
                  +("   [agentJ 1-halo-safe banked: +0.122+-0.062]" if tag=='SB3' else ""))
    # ---------------- the 36-row matrix ----------------
    print("\n=== THE MATRIX offset(type, M* tercile, z, density tercile): combined-SB and SB3 (jackknife errs) ===")
    print("  type Mterc z dens      N        comb              SB3")
    for t in (1,0):
        for k in range(3):
            for z_ in range(2):
                for dd_ in range(3):
                    cl=cells_of(t=t,terc=k,iz_=z_,dens=dd_)
                    oc=comb(cl); o3=offset(cl,'SB3')
                    print(f"  {'E' if t else 'L'}    {k}     {z_} {dd_}    {NC(cl):7,}   "
                          f"{oc[0]:+.3f}+-{oc[2]:.3f}    {o3[0]:+.3f}+-{o3[2]:.3f}")
    # ---------------- stratified contrasts ----------------
    print("\n=== STRATIFIED CONTRASTS — variable V extreme bins at FIXED other two (+ type at fixed all three) ===")
    print("Delta_V = sum_strata n_eff*(off_hi-off_lo)/sum n_eff; n_eff harmonic; strata min(N)>=1000 kept")
    MINN=1000
    def strat(t,V,corrected=False,densdef='ad',zlo_only=False):
        strata=[]
        if V=='type':
            for m5 in range(5):
                for z_ in range(2):
                    for dd_ in range(3):
                        strata.append((cells_of(t=1,m5=m5,iz_=z_,dens=dd_,densdef=densdef),
                                       cells_of(t=0,m5=m5,iz_=z_,dens=dd_,densdef=densdef)))
        elif V=='M*':
            for z_ in ([0] if zlo_only else [0,1]):
                for dd_ in range(3):
                    strata.append((cells_of(t=t,terc=2,iz_=z_,dens=dd_,densdef=densdef),
                                   cells_of(t=t,terc=0,iz_=z_,dens=dd_,densdef=densdef)))
        elif V=='dens':
            for z_ in ([0] if zlo_only else [0,1]):
                for k in range(3):
                    strata.append((cells_of(t=t,terc=k,iz_=z_,dens=2,densdef=densdef),
                                   cells_of(t=t,terc=k,iz_=z_,dens=0,densdef=densdef)))
        elif V=='z':
            for k in range(3):
                for dd_ in range(3):
                    strata.append((cells_of(t=t,terc=k,iz_=1,dens=dd_,densdef=densdef),
                                   cells_of(t=t,terc=k,iz_=0,dens=dd_,densdef=densdef)))
        kept=[];drop=0
        for hi,lo_ in strata:
            Nh,Nl=NC(hi),NC(lo_)
            if min(Nh,Nl)<MINN: drop+=1; continue
            kept.append((hi,lo_,2/(1/Nh+1/Nl)))
        out={}
        for sb in SBORD+['comb']:
            num=0.;nump=np.zeros(N);den=0.
            for hi,lo_,ne in kept:
                oh=comb(hi,corrected) if sb=='comb' else offset(hi,sb,corrected)
                ol=comb(lo_,corrected) if sb=='comb' else offset(lo_,sb,corrected)
                if np.isnan(oh[0]) or np.isnan(ol[0]): continue
                num+=ne*(oh[0]-ol[0]); nump+=ne*(oh[1]-ol[1]); den+=ne
            if den==0: out[sb]=(np.nan,np.full(N,np.nan),np.nan); continue
            Dv=num/den; Dp_=nump/den
            out[sb]=(Dv,Dp_,jsig(Dp_))
        out['nstrat']=len(kept); out['drop']=drop
        return out
    CONTRASTS={}
    print(f"\n  {'V':5s} {'type':5s} {'SB1':>15s} {'SB2':>15s} {'SB3':>15s} {'COMB':>15s}   strata  [signif]")
    for t,lab in ((1,'early'),(0,'late')):
        for V in ('M*','z','dens'):
            r_=strat(t,V); CONTRASTS[(V,t)]=r_
            cs=" ".join(f"{r_[sb][0]:+.3f}+-{r_[sb][2]:.3f}" for sb in SBORD+['comb'])
            sg3=abs(r_['SB3'][0])/max(r_['SB3'][2],1e-300); sgc=abs(r_['comb'][0])/max(r_['comb'][2],1e-300)
            print(f"  {V:5s} {lab:5s} "+cs+f"   {r_['nstrat']}/{r_['drop']}   [SB3 {sg3:.1f}s, comb {sgc:.1f}s]")
    rT=strat(None,'type'); CONTRASTS[('type',None)]=rT
    cs=" ".join(f"{rT[sb][0]:+.3f}+-{rT[sb][2]:.3f}" for sb in SBORD+['comb'])
    print(f"  {'type':5s} {'both':5s} "+cs+f"   {rT['nstrat']}/{rT['drop']}"
          f"   [SB3 {abs(rT['SB3'][0])/max(rT['SB3'][2],1e-300):.1f}s, comb {abs(rT['comb'][0])/max(rT['comb'][2],1e-300):.1f}s]")
    # ---------------- robustness (pre-registered) ----------------
    print("\n=== ROBUSTNESS ===")
    print("(i) centroid-CORRECTED contrasts (within-fine-bin g_bar-distribution systematic removed):")
    for t,lab in ((1,'early'),(0,'late')):
        for V in ('M*','z','dens'):
            r_=strat(t,V,corrected=True)
            print(f"  {V:5s} {lab:5s} SB3 {r_['SB3'][0]:+.3f}+-{r_['SB3'][2]:.3f}   comb {r_['comb'][0]:+.3f}+-{r_['comb'][2]:.3f}")
    rTc=strat(None,'type',corrected=True)
    print(f"  type  both  SB3 {rTc['SB3'][0]:+.3f}+-{rTc['SB3'][2]:.3f}   comb {rTc['comb'][0]:+.3f}+-{rTc['comb'][2]:.3f}")
    print("\n(ii) density-definition swaps (REAL re-marginalizations of the same stack):")
    for densdef,lab2 in (('10','fixed logM>10'),('q','mass-qualified')):
        for t,lab in ((1,'early'),(0,'late')):
            r_=strat(t,'dens',densdef=densdef)
            print(f"  dens[{lab2:14s}] {lab:5s} SB3 {r_['SB3'][0]:+.3f}+-{r_['SB3'][2]:.3f}   "
                  f"comb {r_['comb'][0]:+.3f}+-{r_['comb'][2]:.3f}   ({r_['nstrat']}/{r_['drop']} strata)")
    print("\n(iii) z-lo-restricted density contrast (photo-z dilution guard; strata = M* terciles at z-lo):")
    for t,lab in ((1,'early'),(0,'late')):
        r_=strat(t,'dens',zlo_only=True)
        print(f"  dens {lab}: SB3 {r_['SB3'][0]:+.3f}+-{r_['SB3'][2]:.3f}   comb {r_['comb'][0]:+.3f}+-{r_['comb'][2]:.3f}"
              f"   ({r_['nstrat']} strata)")
    print("\n(iv) agentH conversion column (M13 x D08 <nfw_C(x)>; g_obs contrast = ESD contrast + dlogC_hi-lo):")
    for t,lab in ((1,'early'),(0,'late')):
        mh=lensmask_of(cells_of(t=t,terc=2)); ml=lensmask_of(cells_of(t=t,terc=0))
        d3=dlogC(mh,'SB3')-dlogC(ml,'SB3'); dc=float(np.mean([dlogC(mh,sb)-dlogC(ml,sb) for sb in SBORD]))
        r_=CONTRASTS[('M*',t)]
        print(f"  M* hi-lo {lab}: dlogC SB3 {d3:+.4f}, SB-mean {dc:+.4f}  -> g_obs-level contrast "
              f"SB3 {r_['SB3'][0]+d3:+.3f}, comb {r_['comb'][0]+dc:+.3f}")
    mh=lensmask_of(cells_of(t=1)); ml=lensmask_of(cells_of(t=0))
    print(f"  type (early-late): dlogC SB3 {dlogC(mh,'SB3')-dlogC(ml,'SB3'):+.4f} "
          f"(agentH banked 15-bin mean +0.0008 — sanity)")
    for t,lab in ((1,'early'),(0,'late')):
        mh=lensmask_of(cells_of(t=t,dens=2)); ml=lensmask_of(cells_of(t=t,dens=0))
        print(f"  dens hi-lo {lab}: dlogC SB3 {dlogC(mh,'SB3')-dlogC(ml,'SB3'):+.4f} (expected ~0)")
    # ---------------- VERDICT ----------------
    print("\n"+"="*100)
    print("PRE-REGISTERED VERDICT LOGIC (header rules, applied mechanically):")
    labels={}
    for (V,t),r_ in CONTRASTS.items():
        if V=='type': continue
        sgc=abs(r_['comb'][0])/max(r_['comb'][2],1e-300); sg3=abs(r_['SB3'][0])/max(r_['SB3'][2],1e-300)
        samesign=np.sign(r_['SB3'][0])==np.sign(r_['comb'][0])
        lab='DRIVER' if (sgc>=3 and samesign and sg3>=1.5) else ('TREND' if sgc>=1.5 else 'NULL')
        labels[(V,t)]=lab
        print(f"  {V:5s} {'early' if t else 'late ':5s}: comb {r_['comb'][0]:+.3f} ({sgc:.1f}s), "
              f"SB3 {r_['SB3'][0]:+.3f} ({sg3:.1f}s), same-sign={samesign} -> {lab}")
    sgT=abs(rT['comb'][0])/max(rT['comb'][2],1e-300)
    print(f"  type (fixed absM*,z,dens): comb {rT['comb'][0]:+.3f} ({sgT:.1f}s), "
          f"SB3 {rT['SB3'][0]:+.3f} ({abs(rT['SB3'][0])/max(rT['SB3'][2],1e-300):.1f}s)")
    drivers=[k for k,v in labels.items() if v=='DRIVER']
    if len(drivers)==0:
        reading='TYPE-IRREDUCIBLE (type contrast >=3s at fixed strata, no other driver)' if sgT>=3 else \
                'NO-DRIVER (and the stratified type contrast itself is below 3 sigma)'
    elif len(set(dd[0] for dd in drivers))>=2:
        reading='MIXED: '+", ".join(f"{V}({'E' if t else 'L'})" for V,t in drivers)
    else:
        reading={'dens':'DENSITY-DRIVEN','M*':'MASS-DRIVEN','z':'REDSHIFT/EVOLUTION-DRIVEN'}[drivers[0][0]]+ \
                ' ('+",".join('E' if t else 'L' for _,t in drivers)+')'
    print(f"\n  READING: {reading}")
    print("  (Robustness qualifications and both-ways caveats are weighed in the memo, not silently here.)")
    np.savez(os.path.join(D,'agentZ_matrix.npz'),
             **{f"c_{V.replace('*','s')}_{t}_{sb}":np.array([r_[sb][0],r_[sb][2]])
                for (V,t),r_ in CONTRASTS.items() if V!='type' for sb in SBORD+['comb']})
    print("\nDONE.",flush=True)

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument('--stage',choices=['density','stack','analyze'],required=True)
    a=ap.parse_args()
    {'density':stage_density,'stack':stage_stack,'analyze':stage_analyze}[a.stage]()
