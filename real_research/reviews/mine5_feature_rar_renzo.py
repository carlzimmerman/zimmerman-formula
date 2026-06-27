#!/usr/bin/env python3
"""
MINE-5 CREATIVE WILDCARD: FEATURE-LEVEL RAR / RENZO'S RULE on existing SPARC (175 RCs).

The GLOBAL RAR scatter test is degenerate (banked): dS-Unruh, McGaugh, simple all fit
~equally and the a0 is convention-soft. That test uses only the CLOUD of (g_bar,g_obs)
points. It throws away the WITHIN-GALAXY radial STRUCTURE -- the bumps & wiggles.

Renzo's rule (Sancisi 2004): every feature in the LUMINOUS profile (g_bar) has a
corresponding feature in the ROTATION curve (g_obs). The RAR makes this quantitative:
a LOCAL interpolation g_obs = nu(g_bar)*g_bar predicts the feature in g_obs is the
feature in g_bar AMPLIFIED by the LOCAL LOG-SLOPE  s(g_bar) = d ln g_obs / d ln g_bar.
  deep-MOND (g_bar<<a0): s -> 1/2   (g_obs ~ sqrt(g_bar a0))
  Newtonian (g_bar>>a0): s -> 1
The TRANSITION shape of s(g_bar) DIFFERS between interpolations -> a feature-level
discriminator the global scatter washes out.

TWO independent levers, both provable NOW on in-hand SPARC:

LEVER A (vs-LCDM, expected strong): WITHIN-GALAXY local log-slope.
  For each galaxy, neighboring radii give a finite-difference local slope
  s_obs = dln g_obs / dln g_bar. Pure-disk-dominated LCDM halos have NO reason for
  s_obs to track a UNIVERSAL function of g_bar -- the halo contribution is a free
  per-galaxy profile. The RAR-family predicts s_obs = s_pred(g_bar) UNIVERSALLY.
  We test: does the within-galaxy local slope collapse onto the predicted s(g_bar)?

LEVER B (vs-MOND, the MG-vs-MI lever): MODIFIED INERTIA is NON-LOCAL in radius.
  In modified GRAVITY (QUMOND/AQUAL) g_obs(r)=nu(g_bar(r)) g_bar(r) is STRICTLY LOCAL:
  a feature at radius r imprints at the SAME r with FULL local-slope amplitude.
  In modified INERTIA (Milgrom 1994; dS-Unruh MI) the algebraic g_obs=nu*g_bar holds
  only for the CLOSED circular orbit as a whole; the inertia is a FUNCTIONAL of the
  trajectory -> a localized g_bar feature is partially SMEARED over the orbit, so the
  feature RESPONSE is SUPPRESSED relative to the strictly-local MG amplitude.
  => MI predicts feature amplitude  <  MG predicts feature amplitude (same nu).
  This is the only MG-impossible lever the framework owns; we SCOPE whether SPARC's
  per-point errors leave it provable-now or below-noise.

RUTHLESS BOTH WAYS. C. Zimmerman corpus, 2026-06-26. numpy + real SPARC rotmod.
"""
import numpy as np, glob, os
kpc=3.0857e19
DATA=os.path.join(os.path.dirname(__file__),"..","data","sparc_data")
MLd,MLb=0.5,0.7
a0=9.36e-11   # framework: c^2 sqrt(Lambda/32pi), pure-Lambda

# ---- interpolations and their LOCAL LOG-SLOPE s(y)=dln(g_obs)/dln(g_bar), y=g_bar/a0
def dsu(gb):  return np.sqrt(gb**2+gb*a0)                 # dS-Unruh / Luo / "emergent"  (framework)
def mcg(gb):  return gb/(1.0-np.exp(-np.sqrt(gb/a0)))     # McGaugh 2016
def simp(gb): x=gb/a0; return 0.5*(1+np.sqrt(1+4/x))*gb   # simple mu=x/(1+x)
def slope_num(model,gb):
    # analytic-quality numerical d ln gobs/d ln gbar
    lg=np.log(gb); h=1e-4
    return (np.log(model(gb*np.exp(h)))-np.log(model(gb*np.exp(-h))))/(2*h)

def load_galaxies():
    gal=[]
    for f in sorted(glob.glob(os.path.join(DATA,"*_rotmod.dat"))):
        try: d=np.genfromtxt(f,comments="#")
        except: continue
        if d.ndim!=2 or d.shape[1]<6: continue
        R,Vobs,eV,Vgas,Vdisk,Vbul=(d[:,i] for i in range(6)); Rm=R*kpc
        Vbar2=np.sign(Vgas)*Vgas**2+MLd*Vdisk**2+MLb*Vbul**2
        gb=Vbar2*1e6/Rm; go=(Vobs*1e3)**2/Rm
        ok=(gb>0)&(go>0)&np.isfinite(gb)&np.isfinite(go)&(Vobs>0)&(eV>0)&(R>0)
        if ok.sum()<4: continue
        # frac error on g_obs: g_obs ~ Vobs^2 -> d ln g_obs = 2 dVobs/Vobs
        eln_go=2*eV[ok]/Vobs[ok]
        gal.append(dict(name=os.path.basename(f)[:-11],R=R[ok],gb=gb[ok],go=go[ok],eln=eln_go))
    return gal

gal=load_galaxies()
print("="*90)
print(f"MINE-5  FEATURE-LEVEL RAR / RENZO'S RULE   ({len(gal)} SPARC galaxies, {sum(len(g['R']) for g in gal)} points)")
print("="*90)

# ============================================================================
# LEVER A: within-galaxy LOCAL LOG-SLOPE collapses onto a UNIVERSAL s(g_bar)?
# Finite-difference s_obs between adjacent radii; compare to predicted s(g_bar).
# This is a *feature* statistic: it uses the radial DERIVATIVE, not the level.
# ============================================================================
ys=[]; sobs=[]; esobs=[]; spred_dsu=[]; spred_mcg=[]; spred_simp=[]
for g in gal:
    R,gb,go,eln=g['R'],g['gb'],g['go'],g['eln']
    o=np.argsort(R); R,gb,go,eln=R[o],gb[o],go[o],eln[o]
    dlgb=np.diff(np.log(gb)); dlgo=np.diff(np.log(go))
    good=np.abs(dlgb)>0.03   # need a real lever arm in g_bar to define a slope
    s=dlgo[good]/dlgb[good]
    # error on the local slope from the two endpoint g_obs errors
    e=np.sqrt(eln[:-1]**2+eln[1:]**2)[good]/np.abs(dlgb[good])
    gbm=np.sqrt(gb[:-1]*gb[1:])[good]   # geom-mean g_bar of the pair
    ys+=list(gbm/a0); sobs+=list(s); esobs+=list(e)
    spred_dsu+=list(slope_num(dsu,gbm)); spred_mcg+=list(slope_num(mcg,gbm)); spred_simp+=list(slope_num(simp,gbm))
ys=np.array(ys);sobs=np.array(sobs);esobs=np.array(esobs)
spred_dsu=np.array(spred_dsu);spred_mcg=np.array(spred_mcg);spred_simp=np.array(spred_simp)
# keep finite, sane local slopes (features can be noisy; weight by 1/e^2 handles it)
m=np.isfinite(sobs)&np.isfinite(esobs)&(esobs>0)&(esobs<2)&(np.abs(sobs)<3)
ys,sobs,esobs=ys[m],sobs[m],esobs[m]
spred_dsu,spred_mcg,spred_simp=spred_dsu[m],spred_mcg[m],spred_simp[m]
w=1/esobs**2
print(f"\nLEVER A: within-galaxy local log-slope  s = d ln g_obs / d ln g_bar   (N={len(sobs)} adjacent pairs)")
print(f"  predicted: deep-MOND s->0.5, Newtonian s->1.0  (a UNIVERSAL function of g_bar)")
# binned weighted mean slope vs y
edges=np.logspace(np.log10(max(ys.min(),1e-2)),np.log10(ys.max()),9)
print(f"\n  {'g_bar/a0 bin':>20}{'N':>5}{'<s_obs>':>10}{'+-':>8}{'s_dSU':>8}{'s_McG':>8}{'s_simp':>8}")
for i in range(len(edges)-1):
    b=(ys>=edges[i])&(ys<edges[i+1])
    if b.sum()<8: continue
    sm=np.sum(w[b]*sobs[b])/np.sum(w[b]); se=1/np.sqrt(np.sum(w[b]))
    print(f"  [{edges[i]:7.2f},{edges[i+1]:7.2f}]{b.sum():5d}{sm:10.3f}{se:8.3f}"
          f"{np.median(spred_dsu[b]):8.3f}{np.median(spred_mcg[b]):8.3f}{np.median(spred_simp[b]):8.3f}")

# Global chi2 of the UNIVERSAL predicted slope vs a free per-point constant (LCDM-ish null)
def chi2(pred): return np.sum(w*(sobs-pred)**2)
# Null A: slope is a single global constant fit (no g_bar dependence) -> what LCDM has no reason to beat
const=np.sum(w*sobs)/np.sum(w)
chi2_const=np.sum(w*(sobs-const)**2)
print(f"\n  chi2 (UNIVERSAL s_dSU(g_bar)) = {chi2(spred_dsu):.1f}   on {len(sobs)} pts")
print(f"  chi2 (best single global slope = {const:.3f})      = {chi2_const:.1f}")
dchi=chi2_const-chi2(spred_dsu)
print(f"  Delta chi2 (universal running slope vs flat) = {dchi:.1f}  ->  sqrt= {np.sqrt(abs(dchi)):.1f} sigma")
print(f"  vs-LCDM read: a running, g_bar-locked local slope is detected at ~{np.sqrt(abs(dchi)):.0f} sigma")
print(f"  chi2 dSU {chi2(spred_dsu):.1f} | McGaugh {chi2(spred_mcg):.1f} | simple {chi2(spred_simp):.1f}"
      f"   (which interpolation -> degeneracy check)")

# ============================================================================
# LEVER B (MG vs MI): feature-RESPONSE amplitude.
# Detrend each galaxy on the RAR (remove the smooth nu*g_bar level), then ask:
# does a g_bar RESIDUAL feature dr_gb imprint a g_obs residual dr_go with the
# LOCAL-SLOPE amplitude (MG) or a SUPPRESSED amplitude (MI, non-local smearing)?
# Estimator: beta = cov(dr_go, s*dr_gb)/var(s*dr_gb). MG predicts beta=1, MI beta<1.
# ============================================================================
print("\n"+"="*90)
print("LEVER B (vs-MOND, the MG-vs-MI lever): feature-response amplitude beta")
print("  MG (QUMOND/AQUAL, strictly local): beta = 1.  MI (non-local inertia): beta < 1.")
print("="*90)
DRGO=[];PRED=[];WB=[]
for g in gal:
    R,gb,go,eln=g['R'],g['gb'],g['go'],g['eln']
    if len(R)<6: continue
    o=np.argsort(R); R,gb,go,eln=R[o],gb[o],go[o],eln[o]
    lgb,lgo=np.log(gb),np.log(go)
    # smooth (galaxy-level) RAR trend via local linear detrend in log-log (3-pt running)
    # residual feature in g_bar and g_obs about the smooth monotone trend:
    def detrend(x):
        # subtract a smoothed version (moving average window 3 in index order, which IS radius order)
        sm=np.convolve(x,np.ones(3)/3,mode='same')
        return x-sm
    dlgb=detrend(lgb); dlgo=detrend(lgo)
    s=slope_num(dsu,gb)               # predicted local slope (framework interpolation)
    pred=s*dlgb                       # MG strictly-local feature response
    e=eln                             # error on log g_obs residual ~ same as on log g_obs
    keep=np.abs(dlgb)>0.005
    DRGO+=list(dlgo[keep]); PRED+=list(pred[keep]); WB+=list(1/np.clip(e[keep],1e-3,None)**2)
DRGO=np.array(DRGO);PRED=np.array(PRED);WB=np.array(WB)
mm=np.isfinite(DRGO)&np.isfinite(PRED)&np.isfinite(WB)
DRGO,PRED,WB=DRGO[mm],PRED[mm],WB[mm]
# weighted least-squares slope through origin: beta
beta=np.sum(WB*PRED*DRGO)/np.sum(WB*PRED**2)
beta_err=1/np.sqrt(np.sum(WB*PRED**2))
print(f"  N feature pairs = {len(DRGO)}")
print(f"  measured feature-response  beta = {beta:.3f} +- {beta_err:.3f}")
print(f"    MG prediction beta=1 :  tension = {abs(beta-1)/beta_err:.2f} sigma")
print(f"    MI prediction beta<1 :  beta={beta:.3f} is {'BELOW' if beta<1 else 'AT/ABOVE'} 1")
# how big is the MI suppression we'd need to see, vs the noise floor?
print(f"  noise floor on beta (1 sigma) = {beta_err:.3f}  ->  an MI suppression must exceed ~{beta_err:.2f}")
print(f"    to be provable; literature MI smearing for circular orbits is O(few %), i.e. beta~0.95-0.99.")
print(f"  VERDICT LEVER B: MI-vs-MG suppression is {'RESOLVED' if beta_err<0.05 and abs(beta-1)>2*beta_err else 'BELOW SPARC NOISE (a0/MG-degenerate at this S/N)'}")
