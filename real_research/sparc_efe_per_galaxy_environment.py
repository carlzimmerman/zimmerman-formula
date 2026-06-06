#!/usr/bin/env python3
"""
THE CLINCHING EFE TEST (the prior in-house test said it couldn't do this for lack of per-galaxy g_ext --
the environment table now supplies it). Framework-internal, NO dark matter.

The External Field Effect is the ONE MOND signature LambdaCDM cannot fake: a UNIFORM external field is
invisible to internal dynamics under Newton+DM (the Strong Equivalence Principle), but MOND/modified-inertia
is nonlinear, so a stronger external field SUPPRESSES the internal MOND boost -> the outer rotation curve
dips BELOW the RAR. The smoking gun: galaxies in DENSER environments (stronger g_ext) should sit MORE below
the RAR at low g_bar. Outer-kinematic systematics (warps, beam smearing) do NOT correlate with environment,
so a correlation with environment isolates the EFE.

We compute, per SPARC galaxy: the mean RAR residual in the EFE-sensitive (low-g_bar) regime, and correlate
it with the environmental field proxy (2MRS/2M++ overdensity, host halo mass). PREDICTION: negative slope at
low g_bar, and NO correlation at high g_bar (Newtonian -> EFE-insensitive) = the internal control.
C. Zimmerman, 2026-06-06. numpy + SPARC + environment table.
"""
import numpy as np, glob, os, csv
kpc=3.0857e19; MLd,MLb=0.5,0.7; a0=1.2e-10
HERE=os.path.dirname(__file__); DATA=os.path.join(HERE,"data","sparc_data")
def g_RAR(gb): return np.sqrt(gb**2+gb*a0)          # framework emergent shape (no DM)

# per-galaxy (g_bar, g_obs)
gal={}
for f in sorted(glob.glob(os.path.join(DATA,"*_rotmod.dat"))):
    nm=os.path.basename(f).replace("_rotmod.dat","")
    try: d=np.genfromtxt(f,comments="#")
    except: continue
    if d.ndim!=2 or d.shape[1]<6: continue
    R,Vobs,eV,Vgas,Vdisk,Vbul=(d[:,i] for i in range(6)); Rm=R*kpc
    Vbar2=np.sign(Vgas)*Vgas**2+MLd*Vdisk**2+MLb*Vbul**2
    gb=Vbar2*1e6/Rm; go=(Vobs*1e3)**2/Rm
    ok=(gb>0)&(go>0)&np.isfinite(gb)&np.isfinite(go)&(Vobs>0)
    if ok.sum()>=3: gal[nm]=(gb[ok],go[ok])

# environment table
env={}
with open(os.path.join(HERE,"data","sparc_a0_environment_table.csv")) as fh:
    for r in csv.DictReader(fh):
        try: env[r["name"]]=dict(onepd=float(r["onepd_2mrs"]),onepd2=float(r.get("onepd_2mpp",r["onepd_2mrs"])),
                                 logMh=float(r["logMhalo_host"]))
        except: pass

def residuals(gb,go,lo,hi):                          # mean log RAR residual for g_bar in [lo,hi]
    m=(gb>=lo)&(gb<hi)
    return np.mean(np.log10(go[m])-np.log10(g_RAR(gb[m]))) if m.sum() else np.nan

def corr(xs,ys):
    xs,ys=np.array(xs),np.array(ys); ok=np.isfinite(xs)&np.isfinite(ys); xs,ys=xs[ok],ys[ok]
    n=len(xs)
    rx,ry=np.argsort(np.argsort(xs)).astype(float),np.argsort(np.argsort(ys)).astype(float) # Spearman
    rs=np.corrcoef(rx,ry)[0,1]; t=rs*np.sqrt((n-2)/(1-rs**2)) if abs(rs)<1 else np.inf
    from math import erf
    p=2*(1-0.5*(1+erf(abs(t)/np.sqrt(2))))           # ~normal approx
    return n,rs,p

matched=[nm for nm in gal if nm in env]
print("="*88); print(f"PER-GALAXY EFE TEST: outer-RAR suppression vs environment  ({len(matched)} matched galaxies)"); print("="*88)

for label,(lo,hi),efe in [("EFE-sensitive  g_bar<3e-11 (deep-MOND)",(0,3e-11),True),
                          ("transition    3e-11<g_bar<3e-10",(3e-11,3e-10),False),
                          ("Newtonian      g_bar>3e-10 (CONTROL)",(3e-10,1e-7),False)]:
    res=[residuals(*gal[nm],lo,hi) for nm in matched]
    od =[np.log10(max(env[nm]["onepd"],1e-3)) for nm in matched]      # log(1+delta), 2MRS
    n,rs,p=corr(od,res)
    pred = "predict NEGATIVE (EFE suppresses)" if efe else "predict ~ZERO (EFE-insensitive)"
    flag = ("<-- EFE SIGNAL" if (efe and rs<0 and p<0.05) else
            ("<-- control OK (null)" if (not efe and p>0.05) else ""))
    print(f"\n  [{label}]")
    print(f"    residual vs log(1+delta_2MRS):  N={n}, Spearman r={rs:+.3f}, p={p:.3f}   [{pred}] {flag}")

# headline: the EFE-sensitive correlation vs both environment proxies
print("\n"+"="*88); print("HEADLINE (EFE-sensitive regime, g_bar<3e-11)"); print("="*88)
resL=[residuals(*gal[nm],0,3e-11) for nm in matched]
for proxy,key in [("2MRS overdensity log(1+d)","onepd"),("2M++ overdensity log(1+d)","onepd2"),("host halo logMhalo","logMh")]:
    xv=[np.log10(max(env[nm][key],1e-3)) if key!="logMh" else env[nm][key] for nm in matched]
    n,rs,p=corr(xv,resL)
    print(f"  outer-RAR residual vs {proxy:28s}: N={n}, r={rs:+.3f}, p={p:.3f}"
          f"  {'<-- EFE (suppressed in dense env)' if rs<0 and p<0.05 else ''}")
print("""
  READING IT: the EFE predicts galaxies in DENSER environments / more massive hosts (stronger g_ext) sit
  MORE BELOW the RAR at low g_bar (suppressed internal MOND boost), with NO such trend at high g_bar. A
  negative low-g_bar correlation that VANISHES in the Newtonian control is the EFE -- and it cannot be an
  outer-kinematic artifact, because warps/beam-smearing do not know about the cosmic web. This is the
  per-galaxy test the prior in-house EFE script lacked. No dark matter enters anywhere.""")
