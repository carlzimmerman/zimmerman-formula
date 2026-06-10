#!/usr/bin/env python3
"""
agentK: spatial-jackknife re-stack — gives the v4 independent re-measurement (lr_esd_remeasure.py) ERROR BARS
and OUR OWN early/late split significance, closing the re-measurement gate.

Copy of lr_esd_remeasure.py stage_stack (v4: 21.3M SOM-gold sources x ~181k isolated lenses, 15 g_bar bins per
type, validated vs Brouwer's released Fig-8 profiles) with ONE structural change: each LENS is assigned to one
of 50 equal-count sky patches (25 RA-quantile stripes in KiDS-N [dec>-15] + 25 in KiDS-S, RA unwrapped through
0 in the south; stripe width >~3 deg >> theta_max ~0.5 deg, so a lens's sources live almost entirely "in" its
patch) and the estimator sums (wgE, w, n) accumulate PER (patch, type, g_bar bin) in the same single pass.
Sources are shared across patch borders — that is FINE for a lens-jackknife (the resampled unit is the lens).

Analysis: leave-one-patch-out ESD per (type, bin) -> full 30x30 jackknife covariance (late 0-14, early 15-29,
the same ordering as lr_battery.py's released-covariance C30) ->
 (a) per-bin ESD with jackknife errors vs the released bias-corrected profiles+errors = validation-gate verdict
     per class (late: noise or residual systematic?);
 (b) OUR OWN split significance: chi2 of (early-late) with the full jackknife covariance of the DIFFERENCE
     (jackknifed directly, so the early-late cross-block is in), Hartlap-corrected for N_jk=50, p=15 —
     the analog of the released-profile 8.8 sigma (lr_battery.out).

m-bias caveat (stated up front): the released profiles are (1+K)-corrected, 1+K=0.98531 for BOTH classes ->
released values sit +1.49% above raw; our stack applies NO m-correction (raw lensfit e1/e2), so our ESD is
~1.5% LOW vs the released convention. Constant, multiplicative, far below the jackknife errors, and it CANCELS
in the early-late split (same K both classes).
Inline, no swarms.  agentK 2026-06-10.
"""
import numpy as np, os, sys
from astropy.io import fits
from scipy import stats
from scipy.spatial import cKDTree
D=os.path.join(os.path.dirname(__file__),'..','..','data','lensing_rar')
c=2.998e8; G=6.674e-11; Msun=1.989e30; Mpc=3.0857e22; H0=70*1e3/Mpc  # h70 units per Brouwer
NPATCH=50
OUT=os.path.join(D,'lr_esd_jackknife.npz')
def DC(z,n=2048):  # comoving distance in h70^-1 Mpc, flat LCDM Om=0.3 (Brouwer's cosmology) — v4 verbatim
    zz=np.linspace(0,np.max(z),n); E=np.sqrt(0.3*(1+zz)**3+0.7)
    chi=np.concatenate([[0],np.cumsum(0.5*(1/E[1:]+1/E[:-1])*np.diff(zz))])*(c/H0)/Mpc
    return np.interp(z,zz,chi)

def assign_patches(ra,dec,npatch=NPATCH):
    """50 equal-lens-count sky patches: 25 RA-quantile stripes per KiDS region (N: dec>-15; S: RA unwrapped)."""
    south=dec<-15.0
    ra_u=np.where(south,(ra+180.0)%360.0,ra)      # KiDS-S wraps through RA=0 -> shift to a contiguous range
    patch=np.zeros(len(ra),dtype=np.int64); off=0
    for m in (~south,south):
        npr=npatch//2
        q=np.quantile(ra_u[m],np.linspace(0,1,npr+1)); q[0]-=1e-6; q[-1]+=1e-6
        patch[m]=off+np.clip(np.searchsorted(q,ra_u[m],side='right')-1,0,npr-1)
        off+=npr
    return patch

def stage_stack():
    F=os.path.join(D,'KiDS_DR4.1_SOM_gold_WL_cat.fits')
    if not os.path.exists(F): sys.exit("shear catalog not present")
    ln=np.load(os.path.join(D,'lr_lenses.npz'))
    patch=assign_patches(np.array(ln['ra'],dtype='f8'),np.array(ln['dec'],dtype='f8'))
    cnt=np.bincount(patch,minlength=NPATCH)
    print(f"patches: {NPATCH} (25 N + 25 S RA-quantile stripes); lens counts min/med/max = "
          f"{cnt.min()}/{int(np.median(cnt))}/{cnt.max()}",flush=True)
    h=fits.open(F,memmap=True); s=h[1].data
    cols={cc.name.upper():cc.name for cc in h[1].columns}
    def col(*names):
        for n in names:
            if n.upper() in cols: return np.array(s[cols[n.upper()]],dtype='f8')
        raise KeyError(names)
    raS=col('RAJ2000','ALPHA_J2000','RA'); decS=col('DECJ2000','DELTA_J2000','DEC')
    e1=col('e1','BIAS_CORRECTED_E1'); e2=col('e2','BIAS_CORRECTED_E2')
    w=col('weight','RECAL_WEIGHT','LFWEIGHT'); zB=col('Z_B','ZB','Z_B_BPZ')
    print(f"sources: {len(raS):,}",flush=True)
    zl=ln['z']; chil=ln['chi']
    treeS=cKDTree(np.c_[np.radians(raS),np.radians(decS)])   # v4 verbatim: small-angle chord ~ angle
    gbar_edges=np.logspace(np.log10(1e-15),np.log10(5e-12),16)
    wgE=np.zeros((NPATCH,2,15)); W=np.zeros((NPATCH,2,15)); NN=np.zeros((NPATCH,2,15))
    chunk=2000
    for i0 in range(0,len(zl),chunk):
        sl=slice(i0,min(i0+chunk,len(zl)))
        for j,(rl,dl,zl_,chil_,Mg,ty,pa) in enumerate(zip(ln['ra'][sl],ln['dec'][sl],zl[sl],chil[sl],
                                                          ln['Mgal'][sl],ln['typ'][sl],patch[sl])):
            ty=int(ty); pa=int(pa)
            theta_max=3.0*(1+zl_)/chil_  # rad: 3 Mpc PROPER transverse
            ii=treeS.query_ball_point([np.radians(rl),np.radians(dl)],theta_max)
            ii=np.array(ii,dtype=int)
            if ii.size<5: continue
            back=zB[ii]>zl_+0.2
            ii=ii[back]
            if ii.size<5: continue
            dra=(np.radians(raS[ii])-np.radians(rl))*np.cos(np.radians(dl)); dde=np.radians(decS[ii])-np.radians(dl)
            R=np.hypot(dra,dde)*chil_/(1+zl_)   # PROPER transverse distance, Mpc
            phi=np.arctan2(dde,dra)
            et=-(e1[ii]*np.cos(2*phi)-e2[ii]*np.sin(2*phi))   # v3 handedness fix, verbatim
            chis=DC(zB[ii]); Dls=(chis-chil_)/(1+zB[ii]); Dl=chil_/(1+zl_); Ds=chis/(1+zB[ii])
            inv_sc=np.clip(4*np.pi*G/(c**2)*(Dl*Mpc)*(Dls/Ds),0,None)
            gbar=G*Mg*Msun/(R*Mpc)**2
            k=np.digitize(gbar,gbar_edges)-1
            ok=(k>=0)&(k<15)&(inv_sc>0)
            ww=w[ii]*inv_sc**2
            A_g,A_w,A_n=wgE[pa,ty],W[pa,ty],NN[pa,ty]     # views into the (patch,type,bin) accumulators
            np.add.at(A_g,k[ok],(ww*et/np.where(inv_sc>0,inv_sc,1))[ok])
            np.add.at(A_w,k[ok],ww[ok]); np.add.at(A_n,k[ok],1)
        if (i0//chunk)%10==0 or i0+chunk>=len(zl):
            print(f"  lenses {min(i0+chunk,len(zl)):,}/{len(zl):,}",flush=True)
    np.savez(OUT,wgE=wgE,W=W,NN=NN,patch=patch,gbar_edges=gbar_edges)
    print(f"-> wrote {OUT}",flush=True)
    return wgE,W,NN,gbar_edges

def analyze(wgE,W,NN,gbar_edges):
    KG=Msun/(3.0857e16)**2   # kg/m^2 per Msun/pc^2
    cen=np.sqrt(gbar_edges[:-1]*gbar_edges[1:]); n=15; N=NPATCH
    tot_g=wgE.sum(0); tot_w=W.sum(0)
    esd=tot_g/np.maximum(tot_w,1e-300)/KG                                   # (2,15)  ty: 0=late, 1=early
    loo=(tot_g[None]-wgE)/np.maximum(tot_w[None]-W,1e-300)/KG               # (50,2,15) leave-one-patch-out
    # full 30x30 jackknife covariance, ordering = [late 0-14, early 15-29] (matches lr_battery C30)
    X=np.concatenate([loo[:,0,:],loo[:,1,:]],axis=1); Rm=X-X.mean(0)
    C30=(N-1)/N*(Rm.T@Rm)
    err=np.sqrt(np.diag(C30)); err_l,err_e=err[:n],err[n:]
    # released bias-corrected profiles + their covariance (for the validation gate)
    B=os.path.join(D,'brouwer2021_rar')
    late=np.loadtxt(os.path.join(B,'Fig-8_RAR-KiDS-isolated_Colorbin_1.txt'))
    early=np.loadtxt(os.path.join(B,'Fig-8_RAR-KiDS-isolated_Colorbin_2.txt'))
    rel={0:late[:,1]/late[:,4],1:early[:,1]/early[:,4]}
    rerr={0:late[:,3]/late[:,4],1:early[:,3]/early[:,4]}
    covraw=np.loadtxt(os.path.join(B,'Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt'))
    rad=np.unique(covraw[:,2]); cb={0.0:0,2.5:1}
    C30r=np.zeros((2*n,2*n))
    for m,nn_,ri,rj,cv,_,bias in covraw:
        i=cb[m]*n+int(np.argmin(abs(rad-ri))); jx=cb[nn_]*n+int(np.argmin(abs(rad-rj))); C30r[i,jx]=cv/bias
    sig=lambda c2,df=n: stats.norm.isf(0.5*stats.chi2.sf(c2,df=df))
    print("\n=== (a) VALIDATION GATE: our ESD +/- jackknife err  vs  released bias-corrected +/- err ===")
    print("m-bias caveat: ours is raw (no 1/(1+K)); released uses 1+K=0.98531 -> ours sits ~1.5% LOW by"
          "\nconvention alone. Constant and multiplicative; ignored below (it is <<1 jackknife sigma per bin).")
    for ty,lab in ((0,'late'),(1,'early')):
        ours=esd[ty]; oerr=err[ty*n:(ty+1)*n]
        dlt=ours-rel[ty]; comb=np.sqrt(oerr**2+rerr[ty]**2)
        pulls=dlt/comb; chi2d=float(np.sum(pulls**2))
        Csum=C30[ty*n:(ty+1)*n,ty*n:(ty+1)*n]+C30r[ty*n:(ty+1)*n,ty*n:(ty+1)*n]
        chi2f=float(dlt@np.linalg.solve(Csum,dlt))
        print(f"\n{lab}: g_bar | OURS +/- jk_err | RELEASED +/- err | ratio | pull")
        for k in range(n):
            print(f"  {cen[k]:.2e} | {ours[k]:8.3f} +/- {oerr[k]:6.3f} | {rel[ty][k]:8.3f} +/- {rerr[ty][k]:6.3f}"
                  f" | {ours[k]/rel[ty][k]:5.2f} | {pulls[k]:+5.2f}")
        print(f"  {lab} vs released: chi2_diag={chi2d:.1f} (df=15, p={stats.chi2.sf(chi2d,15):.3f},"
              f" {sig(chi2d):.1f} sigma) ; chi2_fullcov={chi2f:.1f} ({sig(chi2f):.1f} sigma)")
        print(f"  [caveat BOTH WAYS: same survey data -> ours & released are CORRELATED; quadrature/full-sum"
              f"\n   errors OVERSTATE the difference error, so these pulls are LENIENT on consistency. But sample"
              f"\n   differences (isolation window, colour split 2.0-LePhare vs 2.5-Brouwer, +0.15dex fluxscale)"
              f"\n   produce COHERENT offsets, which is what the full-cov chi2 is sensitive to.]")
    # ---- (b) OUR OWN split significance: jackknife the (early-late) difference directly ----
    print("\n=== (b) OUR OWN early/late split significance (jackknife covariance of the difference) ===")
    d=esd[1]-esd[0]
    Dp=loo[:,1,:]-loo[:,0,:]; Rd=Dp-Dp.mean(0)
    Cd=(N-1)/N*(Rd.T@Rd)
    chi2=float(d@np.linalg.solve(Cd,d))
    hart=(N-n-2)/(N-1)
    chi2h=hart*chi2
    print(f"  early ABOVE late in {int(np.sum(d>0))}/15 bins; mean dlog10(ESD) = {np.mean(np.log10(esd[1]/esd[0])):+.3f} dex"
          f"  (released-profile battery: 15/15, +0.261 dex)")
    print(f"  chi2(early-late | full 15x15 jackknife Cd) = {chi2:.1f} (df=15) -> {sig(chi2):.1f} sigma  [raw]")
    print(f"  Hartlap-corrected (N_jk={N}, p=15: factor {hart:.3f}): chi2={chi2h:.1f} -> {sig(chi2h):.1f} sigma  [HEADLINE]")
    # diagonal-only reference (no off-diagonal information)
    chi2diag=float(np.sum(d**2/np.diag(Cd)))
    print(f"  diagonal-only reference: chi2={chi2diag:.1f} -> {sig(chi2diag):.1f} sigma")
    # robustness: 25-patch jackknife (merge adjacent stripe pairs)
    g25=np.add.reduceat(wgE,np.arange(0,N,2),axis=0); w25=np.add.reduceat(W,np.arange(0,N,2),axis=0)
    loo25=(tot_g[None]-g25)/np.maximum(tot_w[None]-w25,1e-300)/KG
    Dp25=loo25[:,1,:]-loo25[:,0,:]; Rd25=Dp25-Dp25.mean(0)
    Cd25=(25-1)/25*(Rd25.T@Rd25)
    chi2_25=float(d@np.linalg.solve(Cd25,d)); h25=(25-n-2)/(25-1)
    print(f"  robustness, 25 merged patches: raw {sig(chi2_25):.1f} sigma; Hartlap({h25:.3f}) "
          f"{sig(h25*chi2_25):.1f} sigma")
    # comparison line
    print(f"\n  released-profile analog (lr_battery.out): chi2=119.9 -> 8.8 sigma (their cov, their sample)")
    print(f"  expected dilutions in OURS vs theirs: 181,477 vs 259,383 isolated lenses (x0.70 -> sigma x~0.84);")
    print(f"  jackknife cov includes cosmic variance + shape noise (analytic cov is shape-noise-led); colour")
    print(f"  split at the LePhare valley 2.0 (53/47 early/late) vs Brouwer 2.5 (their convention); isolation")
    print(f"  Dchi=10 Mpc count-calibrated window. All four DILUTE; quantified in agentK_remeasure_errors.md.")
    np.savez(os.path.join(D,'lr_esd_jackknife_analysis.npz'),esd=esd,loo=loo,C30=C30,Cd=Cd,err=err,
             gbar_cen=cen,d=d,chi2=chi2,chi2_hartlap=chi2h)
    print(f"-> wrote lr_esd_jackknife_analysis.npz")

if __name__=="__main__":
    if os.path.exists(OUT) and '--force' not in sys.argv:
        print(f"reusing {OUT} (pass --force to re-stack)")
        z=np.load(OUT); wgE,W,NN,ge=z['wgE'],z['W'],z['NN'],z['gbar_edges']
    else:
        wgE,W,NN,ge=stage_stack()
    analyze(wgE,W,NN,ge)
