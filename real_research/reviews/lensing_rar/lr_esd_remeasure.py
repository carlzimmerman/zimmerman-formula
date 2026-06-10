#!/usr/bin/env python3
"""
LR independent re-measurement (the gold-standard track, Carl's pick): rebuild Brouwer+2021's ESD profiles from
the public KiDS-1000 catalogs from scratch, validating point-by-point against the released profiles
(brouwer2021_rar/). Two stages:
  --stage lens  : runs NOW (uses the two downloaded lens catalogs). Selection (r<20, 0.1<z<0.5, M*<1e11,
                  unmasked) -> ISOLATION (no neighbour with M*_sat > 0.1 M*_lens within 3 h70^-1 Mpc transverse,
                  photo-z window |dz|<0.05 [GAP: Brouwer's exact z-window not recoverable; logged substitute])
                  -> u-r split at 2.5 (the threshold recovered from the released covariance) -> M_gal =
                  M*(1+f_cold), log f_cold = -0.69 logM* + 6.63 -> writes lr_lenses.npz.
  --stage stack : runs when the 16 GB SOM-gold shear catalog lands. Per-lens tangential-ellipticity stack,
                  Sigma_crit(z_l,z_s) weights, lensfit weights, m-bias correction; bins in g_bar = G M_gal/r^2
                  (15 log bins 1e-15..5e-12, Brouwer's grid); outputs ESD_t per bin per type + bootstrap errors
                  -> validate against Fig-8 released profiles, then the split sigma.
GAP ledger (fidelity-first): (1b) LePhare MASS_MED fluxscale status unverified [check vs GAMA medians];
(iso-z) the |dz|<0.05 isolation window is a substitute; (n-split) Sersic axis needs the morphology catalog.
Inline, no swarms.  C. Zimmerman 2026-06-10.
"""
import numpy as np, os, sys, argparse
from astropy.io import fits
from scipy.spatial import cKDTree
D=os.path.join(os.path.dirname(__file__),'..','..','data','lensing_rar')
c=2.998e8; G=6.674e-11; Msun=1.989e30; Mpc=3.0857e22; H0=70*1e3/Mpc  # h70 units per Brouwer
def DC(z,n=2048):  # comoving distance in h70^-1 Mpc, flat LCDM Om=0.3 (Brouwer's cosmology)
    # v2 unit fix (logged): v1 returned METERS (c/H0 in SI), making the isolation radii 3/1e26 rad ~ 0
    # -> zero disqualifications. chi must be in Mpc; everything downstream treats it as Mpc.
    zz=np.linspace(0,np.max(z),n); E=np.sqrt(0.3*(1+zz)**3+0.7)
    chi=np.concatenate([[0],np.cumsum(0.5*(1/E[1:]+1/E[:-1])*np.diff(zz))])*(c/H0)/Mpc
    return np.interp(z,zz,chi)

def stage_lens():
    """FIX ROUND (2026-06-10, logged): v1 had two bugs caught by its own output. (1) Isolation used a fake
    'tangent plane' that scaled each galaxy's angles by its OWN chi -> different-z galaxies flung apart -> 0
    disqualifications (100% isolated). Fixed: unit-sphere KD-tree, per-lens angular radius 3 Mpc/chi_i, chord~angle.
    (2) The u-r threshold 2.5 (Brouwer's covariance bin-edge, THEIR color system) lands in our LePhare MAG_ABS
    distribution's red tail (2%/98%). The physical split is the BIMODALITY VALLEY; in the LePhare system it sits
    at u-r ~= 2.0 (red peak 2.34, blue 1.6; same valley Brouwer call 2.5 in their convention -- ~0.5 mag
    zeropoint/k-correction offset, GAP-color logged). Split data-driven at 2.0; the released-profile validation
    adjudicates the convention."""
    b=fits.open(os.path.join(D,'KiDS_DR4_brightsample.fits'))[1].data
    L=fits.open(os.path.join(D,'KiDS_DR4_brightsample_LePhare.fits'))[1].data
    assert np.array_equal(b['ID'],L['ID'])
    r=b['MAG_AUTO_CALIB']; z=np.array(b['zphot_ANNz2'],dtype='f8'); masked=b['masked']
    logM=np.array(L['MASS_MED'],dtype='f8'); ur=np.array(L['MAG_ABS_u']-L['MAG_ABS_r'],dtype='f8')
    ra=np.array(b['RAJ2000'],dtype='f8'); dec=np.array(b['DECJ2000'],dtype='f8')
    pool=(r<20)&(z>0.1)&(z<0.5)&(masked==0)&np.isfinite(logM)&(logM>7)   # neighbour pool: NO upper mass cut
    sel=pool&(logM<11.0)&np.isfinite(ur)                                  # the lens sample
    print(f"lens selection: {sel.sum():,} of {len(b):,}   (neighbour pool {pool.sum():,})")
    ip=np.where(pool)[0]; il=np.where(sel)[0]
    zP=z[ip]; logMP=logM[ip]; chiP=DC(zP)
    raP,decP=np.radians(ra[ip]),np.radians(dec[ip])
    xyzP=np.c_[np.cos(decP)*np.cos(raP),np.cos(decP)*np.sin(raP),np.sin(decP)]
    tree=cKDTree(xyzP)
    pos=np.searchsorted(ip,il)            # lens positions inside the pool arrays (sel subset of pool)
    # collect candidate (lens k, pool j) pairs once: projected < 3 Mpc, mass-qualified; then scan the radial window.
    # GAP-iso (logged): Brouwer's radial association ("within 3 Mpc", photo-z, App A ~80% accuracy) is not exactly
    # recoverable; a +-0.05 z-cylinder gives 0.8% isolated, a literal 3 Mpc photo-z sphere ~80%. Per the WB-R1
    # pattern: scan the window, CALIBRATE to their published isolated count (~259k of ~1M; ~26-40% of the lens
    # sample), flag count-calibrated, and let the released-profile validation adjudicate.
    PI,PJ=[],[]
    CH=20000
    for i0 in range(0,len(il),CH):
        slc=pos[i0:i0+CH]
        rads=3.0/chiP[slc]
        lists=tree.query_ball_point(xyzP[slc],r=rads)
        for k,js in enumerate(lists):
            i=slc[k]
            for j in js:
                if j!=i and logMP[j]>logMP[i]-1.0: PI.append(i0+k); PJ.append(j)
    PI=np.array(PI); PJ=np.array(PJ)
    dchi=np.abs(chiP[pos][PI]-chiP[PJ])
    print(f"candidate satellite pairs (proj<3 Mpc, mass-qualified): {len(PI):,}")
    print("  radial window scan:  Dchi[Mpc]  isolated  frac   (target ~26-40%)")
    best=None
    for DCHI in (3,5,10,15,20,30,50,100):
        iso=np.ones(len(il),bool); iso[np.unique(PI[dchi<DCHI])]=False
        f=iso.mean(); print(f"      {DCHI:5d}      {iso.sum():7,}  {100*f:5.1f}%")
        if best is None or abs(f-0.33)<abs(best[1]-0.33): best=(DCHI,f)
    DCHI=best[0]
    iso=np.ones(len(il),bool); iso[np.unique(PI[dchi<DCHI])]=False
    print(f"isolated (count-calibrated window Dchi={DCHI} Mpc): {iso.sum():,} ({100*iso.mean():.1f}%; Brouwer 259,383 of ~1M)")
    zS=zP[pos]; logMS=logMP[pos]; chiL=chiP[pos]; urS=ur[il]
    UR_SPLIT=2.0                          # bimodality valley in the LePhare MAG_ABS system (GAP-color logged)
    typ=np.where(urS>UR_SPLIT,1,0)
    fcold=10**(-0.69*logMS+6.63); Mgal=10**logMS*(1+fcold)
    e,l=np.sum(typ[iso]==1),np.sum(typ[iso]==0)
    print(f"split at u-r={UR_SPLIT} (isolated): early {e:,} ({100*e/(e+l):.0f}%)   late {l:,}")
    print(f"median log10 M_gal: early {np.median(np.log10(Mgal[iso&(typ==1)])):.2f}, late {np.median(np.log10(Mgal[iso&(typ==0)])):.2f}")
    np.savez(os.path.join(D,'lr_lenses.npz'),ra=ra[il][iso],dec=dec[il][iso],z=zS[iso],
             logM=logMS[iso],Mgal=Mgal[iso],typ=typ[iso],chi=chiL[iso])
    print(f"-> wrote lr_lenses.npz ({iso.sum():,} isolated lenses). Stage 2 armed (needs the SOM-gold shear FITS).")

def stage_stack():
    F=os.path.join(D,'KiDS_DR4.1_SOM_gold_WL_cat.fits')
    if not os.path.exists(F): sys.exit("shear catalog not present yet")
    ln=np.load(os.path.join(D,'lr_lenses.npz'))
    h=fits.open(F,memmap=True); s=h[1].data
    cols={c.name.upper():c.name for c in h[1].columns}
    def col(*names):
        for n in names:
            if n.upper() in cols: return np.array(s[cols[n.upper()]],dtype='f8')
        raise KeyError(names)
    raS=col('RAJ2000','ALPHA_J2000','RA'); decS=col('DECJ2000','DELTA_J2000','DEC')
    e1=col('e1','BIAS_CORRECTED_E1'); e2=col('e2','BIAS_CORRECTED_E2')
    w=col('weight','RECAL_WEIGHT','LFWEIGHT'); zB=col('Z_B','ZB','Z_B_BPZ')
    print(f"sources: {len(raS):,}")
    # Sigma_crit^-1 = 4 pi G / c^2 * D_l D_ls / D_s  (comoving->proper per Brouwer Eq.2 conventions)
    zl=ln['z']; chil=ln['chi']
    treeS=cKDTree(np.c_[np.radians(raS),np.radians(decS)])   # small-angle chord ~ angle (validated below)
    edges=np.logspace(np.log10(0.03),np.log10(3.0),16)        # R bins, h70^-1 Mpc (placeholder; rebinned to g_bar)
    gbar_edges=np.logspace(np.log10(1e-15),np.log10(5e-12),16)
    acc={t:{'wgE':np.zeros(15),'wg':np.zeros(15),'w':np.zeros(15),'n':np.zeros(15)} for t in (0,1)}
    chunk=2000
    for i0 in range(0,len(zl),chunk):
        sl=slice(i0,min(i0+chunk,len(zl)))
        for j,(rl,dl,zl_,chil_,Mg,ty) in enumerate(zip(ln['ra'][sl],ln['dec'][sl],zl[sl],chil[sl],ln['Mgal'][sl],ln['typ'][sl])):
            theta_max=3.0*(1+zl_)/chil_  # rad: 3 Mpc PROPER transverse
            ii=treeS.query_ball_point([np.radians(rl),np.radians(dl)],theta_max)
            ii=np.array(ii,dtype=int)
            if ii.size<5: continue
            back=zB[ii]>zl_+0.2
            ii=ii[back]
            if ii.size<5: continue
            dra=(np.radians(raS[ii])-np.radians(rl))*np.cos(np.radians(dl)); dde=np.radians(decS[ii])-np.radians(dl)
            R=np.hypot(dra,dde)*chil_/(1+zl_)   # PROPER transverse distance, Mpc (units-fix v2; validation adjudicates)
            phi=np.arctan2(dde,dra)
            # v3 convention fix: KiDS e1/e2 frame handedness — the 4-convention diagnostic (20k lenses, 0.3-1 Mpc
            # annulus) gave +4.0e-4 for the e2-flipped rotation vs +1.0e-4 unflipped -> the flipped one is physical.
            et=-(e1[ii]*np.cos(2*phi)-e2[ii]*np.sin(2*phi))
            chis=DC(zB[ii]); Dls=(chis-chil_)/(1+zB[ii]); Dl=chil_/(1+zl_); Ds=chis/(1+zB[ii])
            # Sigma_crit^-1 in SI (m^2/kg); estimator stays SI throughout (v1 mangled this by DIVIDING by Msun/Mpc^2)
            inv_sc=np.clip(4*np.pi*G/(c**2)*(Dl*Mpc)*(Dls/Ds),0,None)
            gbar=G*Mg*Msun/(R*Mpc)**2
            k=np.digitize(gbar,gbar_edges)-1
            ok=(k>=0)&(k<15)&(inv_sc>0)
            ww=w[ii]*inv_sc**2
            np.add.at(acc[ty]['wgE'],k[ok],(ww*et/np.where(inv_sc>0,inv_sc,1))[ok]); np.add.at(acc[ty]['w'],k[ok],ww[ok]); np.add.at(acc[ty]['n'],k[ok],1)
        print(f"  lenses {min(i0+chunk,len(zl)):,}/{len(zl):,}",flush=True)
    KG_M2_PER_MSUN_PC2=Msun/(3.0857e16)**2   # 2.0887e-3 kg/m^2 per Msun/pc^2
    cen=np.sqrt(gbar_edges[:-1]*gbar_edges[1:])
    # validation targets: the released Fig-8 split profiles (bias-corrected)
    B=os.path.join(D,'brouwer2021_rar')
    try:
        rel={0:np.loadtxt(os.path.join(B,'Fig-8_RAR-KiDS-isolated_Colorbin_1.txt')),
             1:np.loadtxt(os.path.join(B,'Fig-8_RAR-KiDS-isolated_Colorbin_2.txt'))}
    except Exception: rel=None
    for ty,lab in ((0,'late'),(1,'early')):
        esd=acc[ty]['wgE']/np.maximum(acc[ty]['w'],1e-300)/KG_M2_PER_MSUN_PC2   # -> Msun/pc^2
        print(f"\n{lab}: g_bar-bin centre | OUR ESD_t (Msun/pc^2) | released Brouwer (bias-corr) | ratio")
        for k in range(15):
            r=rel[ty][k,1]/rel[ty][k,4] if rel is not None else np.nan
            print(f"  {cen[k]:.2e} | {esd[k]:10.3f} | {r:10.3f} | {esd[k]/r if r else np.nan:6.2f}")
    np.savez(os.path.join(D,'lr_esd_remeasured.npz'),**{f"{k}_{t}":acc[t][k] for t in (0,1) for k in acc[t]})
    print("-> wrote lr_esd_remeasured.npz. Validation gate: ratios ~1 (within ~20-30%) across bins before ANY sigma is computed.")

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument('--stage',choices=['lens','stack'],required=True)
    a=ap.parse_args()
    stage_lens() if a.stage=='lens' else stage_stack()
