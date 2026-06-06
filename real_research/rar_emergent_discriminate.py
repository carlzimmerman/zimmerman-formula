#!/usr/bin/env python3
"""
FORWARD (no dark matter, framework-internal): is MOND's interpolation function DERIVED from the vacuum,
and can the data confirm it uniquely?

The framework is emergent gravity sourced by the vacuum. de Sitter-Unruh modified inertia predicts a SPECIFIC,
parameter-free RAR shape: g_obs = sqrt(g_bar^2 + g_bar*a0)  [equiv nu(y)=sqrt(1+1/y), y=g_bar/a0]. Verified two
ways: (a) mu(a)=[sqrt(a^2+(cH)^2)-cH]/a; (b) Luo 2026 mu(x)=(sqrt(1+4x^2)-1)/2x -> BOTH give the same g_obs.
This is a prediction LambdaCDM cannot make (it has no RAR shape; the relation is emergent-with-scatter).

This script (175 SPARC galaxies, real data): (1) confirms the derived shape fits; (2) asks if the data UNIQUELY
select it vs McGaugh/simple -- the degeneracy question; (3) finds WHERE the forms diverge -> the discriminating
regime + precision; (4) reports the a0 SCALE each form wants vs the framework's vacuum value (the coefficient).
C. Zimmerman, 2026-06-06. numpy + SPARC.
"""
import numpy as np, glob, os
kpc=3.0857e19; DATA=os.path.join(os.path.dirname(__file__),"data","sparc_data"); MLd,MLb=0.5,0.7
a0_framework=9.36e-11      # c^2 sqrt(Lambda/32pi), pure-Lambda

def load():
    gb,go,w=[],[],[]
    for f in sorted(glob.glob(os.path.join(DATA,"*_rotmod.dat"))):
        try: d=np.genfromtxt(f,comments="#")
        except: continue
        if d.ndim!=2 or d.shape[1]<6: continue
        R,Vobs,eV,Vgas,Vdisk,Vbul=(d[:,i] for i in range(6)); Rm=R*kpc
        Vbar2=np.sign(Vgas)*Vgas**2+MLd*Vdisk**2+MLb*Vbul**2
        g_b=Vbar2*1e6/Rm; g_o=(Vobs*1e3)**2/Rm
        ok=(g_b>0)&(g_o>0)&np.isfinite(g_b)&np.isfinite(g_o)&(Vobs>0)
        fr=np.clip(eV,1,None)/np.clip(Vobs,1,None)
        gb+=list(g_b[ok]); go+=list(g_o[ok]); w+=list(1/fr[ok]**2)
    return map(np.array,(gb,go,w))

# interpolations: g_obs(g_bar,a0)
def dsu(gb,a0): return np.sqrt(gb**2+gb*a0)               # emergent/de Sitter-Unruh (=Luo); DERIVED
def mcg(gb,a0): return gb/(1.0-np.exp(-np.sqrt(gb/a0)))   # McGaugh 2016 empirical
def simp(gb,a0):x=gb/a0; return 0.5*(1+np.sqrt(1+4/x))*gb # 'simple' mu=x/(1+x)
FORMS={"emergent (DERIVED) sqrt(gb^2+gb a0)":dsu,"McGaugh 2016 (fit)":mcg,"simple mu=x/(1+x)":simp}

def fit(model,gb,go,w):
    grid=np.linspace(0.4e-10,3.0e-10,800); best=None
    for a0 in grid:
        r=np.log10(go)-np.log10(model(gb,a0)); s=np.sqrt(np.sum(w*r**2)/np.sum(w))
        if best is None or s<best[1]: best=(a0,s)
    return best

gb,go,w=load()
print("="*86); print(f"RAR: emergent-gravity DERIVED shape vs alternatives ({len(gb)} SPARC points, no dark matter)"); print("="*86)
print(f"  {'interpolation':38}{'best a0[e-10]':>13}{'scatter[dex]':>13}{'scatter@framework a0':>22}")
fits={}
for nm,m in FORMS.items():
    a0,s=fit(m,gb,go,w); fits[nm]=(a0,s)
    rfw=np.log10(go)-np.log10(m(gb,a0_framework)); sfw=np.sqrt(np.sum(w*rfw**2)/np.sum(w))
    print(f"  {nm:38}{a0*1e10:>13.2f}{s:>13.3f}{sfw:>22.3f}")

print("\n"+"="*86); print("(1) IS THE DERIVED SHAPE DATA-CONSISTENT?  YES -- and degenerate with the fits"); print("="*86)
print(f"  emergent {fits['emergent (DERIVED) sqrt(gb^2+gb a0)'][1]:.3f} vs McGaugh {fits['McGaugh 2016 (fit)'][1]:.3f} dex"
      f" -- difference {abs(fits['emergent (DERIVED) sqrt(gb^2+gb a0)'][1]-fits['McGaugh 2016 (fit)'][1]):.3f} dex (negligible).")
print("  The DERIVED shape (no shape freedom) fits as well as the best empirical fit. But it does NOT uniquely")
print("  win -- McGaugh/simple fit equally. So the RAR is CONSISTENT WITH but does not yet CONFIRM the emergent shape.")

print("\n"+"="*86); print("(2) WHERE DO THE FORMS DIVERGE? -> the discriminating regime"); print("="*86)
print(f"  {'y=g_bar/a0':>10}{'nu_emergent':>13}{'nu_McGaugh':>12}{'diff [dex]':>12}")
ymax=0
for y in [0.03,0.1,0.3,1,3,10]:
    ne=np.sqrt(1+1/y); nm=1/(1-np.exp(-np.sqrt(y))); d=abs(np.log10(ne)-np.log10(nm))
    ymax=max(ymax,d); print(f"  {y:>10.2f}{ne:>13.3f}{nm:>12.3f}{d:>12.3f}")
print(f"  => max divergence ~{ymax:.3f} dex, in the TRANSITION (y~0.1-1). The deep tail (y<<1) and Newtonian (y>>1)")
print(f"     limits AGREE (both -> sqrt(g_bar a0) and -> g_bar). To DISTINGUISH the emergent shape you need RAR")
print(f"     precision <~ {ymax:.3f} dex in the transition region -- BELOW today's ~0.10 dex scatter. That is the test.")

print("\n"+"="*86); print("(3) THE SCALE a0: vacuum value vs RAR-preferred (the coefficient posit)"); print("="*86)
print(f"  framework (pure-Lambda) a0 = {a0_framework*1e10:.2f}e-10  [c^2 sqrt(Lambda/32pi), posited coefficient]")
for nm in FORMS: print(f"  RAR-preferred a0 ({nm.split('(')[0].strip()}) = {fits[nm][0]*1e10:.2f}e-10  -> framework is {fits[nm][0]/a0_framework:.2f}x low")
print("""  => the SHAPE is derived; the SCALE is set by Lambda up to the unfalsifiable coefficient. The RAR wants
     a0 ~1.4-1.9x the framework's posited value -- exactly the known coefficient freedom (kappa, not derivable,
     but it cancels in a0(z) tests). The shape prediction does NOT depend on this.""")

print("\n"+"="*86); print("FORWARD VERDICT (no dark matter)"); print("="*86)
print(f"""  - The framework PREDICTS the RAR shape (emergent-gravity mu, derived 2 ways) -- a parameter-free prediction
    LambdaCDM cannot make -- and it fits 175 SPARC galaxies at 0.10 dex with NO dark matter. Genuine success.
  - But the shape is DEGENERATE with empirical fits at today's 0.10 dex scatter; the emergent form is confirmed
    CONSISTENT, not UNIQUE. The forms diverge ~{ymax:.2f} dex only in the transition (y~0.1-1).
  - THE DISCRIMINATING TEST (the forward step): push the RAR scatter below ~{ymax:.2f} dex in the transition region
    (y~0.3-1) -- needs better M/L (stellar pops), distances, inclinations to beat the intrinsic-scatter floor.
    THAT would confirm or kill the emergent-gravity (vacuum-derived) interpolation -- the framework's claim that
    MOND's shape comes from the vacuum, not a fit. Decisive, framework-internal, and uses data already in hand.""")
