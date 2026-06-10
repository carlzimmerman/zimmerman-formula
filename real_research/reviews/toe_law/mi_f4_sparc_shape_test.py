#!/usr/bin/env python3
"""
Trilemma calc #1c: does F4's SHAPE survive galaxy data? (MI_COUPLING_FAMILY.md named this the next bite.)
F4 (susceptibility coupling) derives mu_standard = x/sqrt(1+x^2); on circular orbits (rotation curves) modified
inertia gives mu(a/a0)*a = g_N EXACTLY, inverting to nu_std(y) = sqrt((y+sqrt(y^2+4))/(2y)), y = g_bar/a0.
Compare its SPARC RAR scatter against the McGaugh RAR function, the simple function, and the framework's own
emergent shape nu_fw = sqrt(1+1/y) -- same data, same Upsilon treatment (the only freedom; Upsilon_bul = 1.4 Ud),
each function gets its own best Upsilon (fair shape comparison; Upsilon and shape trade off).
CONVENTIONS (per the working rule -- metric choice is a known artifact source, so run BOTH ways):
  scatter reported UNWEIGHTED (the locked standard) AND error-weighted (the incumbent script's choice);
  a0 at BOTH the framework 9.36e-11 AND canonical MOND 1.2e-10.
PRE-REGISTERED reading: F4 SURVIVES if best scatter within 0.01 dex of the best rival at the same a0;
DEGRADED 0.01-0.02; DISFAVOURED >0.02. Knee check: nu(1) = 1.27 (std) vs 1.58 (RAR) vs 1.62 (simple) vs 1.41 (fw)
-- the standard function gives the weakest knee boost, so SPARC discriminates. Inline, no swarms. 2026-06-10.
"""
import numpy as np, glob, os
kpc=3.0857e19
DATA=os.path.join(os.path.dirname(__file__),"..","..","data","sparc_data")
rows=[]
for f in sorted(glob.glob(os.path.join(DATA,"*_rotmod.dat"))):
    try: d=np.genfromtxt(f,comments="#")
    except: continue
    if d.ndim!=2 or d.shape[1]<6: continue
    R,Vobs,eV,Vgas,Vdisk,Vbul=(d[:,i] for i in range(6))
    rows.append((R*kpc,Vobs,eV,Vgas,Vdisk,Vbul))
print(f"SPARC galaxies loaded: {len(rows)}")

def nu_fw(y):   return np.sqrt(1+1/y)
def nu_rar(y):  return 1.0/(1.0-np.exp(-np.sqrt(y)))
def nu_simple(y): return 0.5+np.sqrt(0.25+1/y)
def nu_std(y):  return np.sqrt((y+np.sqrt(y*y+4))/(2*y))     # F4: from mu = x/sqrt(1+x^2), exact inversion
FUNCS={'fw sqrt(1+1/y)':nu_fw,'McGaugh RAR':nu_rar,'simple':nu_simple,'F4 standard':nu_std}

def scatter(nu,Ud,a0):
    res,w=[],[]
    for Rm,Vobs,eV,Vgas,Vdisk,Vbul in rows:
        Vbar2=np.sign(Vgas)*Vgas**2 + Ud*Vdisk**2 + 1.4*Ud*Vbul**2
        gb=Vbar2*1e6/Rm; go=(Vobs*1e3)**2/Rm
        ok=(gb>0)&(go>0)&np.isfinite(gb)&np.isfinite(go)&(Vobs>0)
        r=np.log10(go[ok])-np.log10(nu(gb[ok]/a0)*gb[ok])
        fr=np.clip(eV[ok],1,None)/np.clip(Vobs[ok],1,None)
        res+=list(r); w+=list(1/fr**2)
    res,w=np.array(res),np.array(w)
    return np.sqrt(np.mean(res**2)), np.sqrt(np.sum(w*res**2)/np.sum(w))   # (unweighted, weighted)

Uds=np.linspace(0.3,1.2,46)
for a0,a0lab in [(9.36e-11,'framework 9.36e-11'),(1.2e-10,'canonical 1.2e-10')]:
    print(f"\n=== a0 = {a0lab} ===   (each function at its own best-Upsilon; dex)")
    print(f"  {'function':16s} {'best Ud':>8s} {'UNWEIGHTED':>11s} {'weighted':>9s}")
    best_unw={}
    for lab,nu in FUNCS.items():
        su=[scatter(nu,U,a0) for U in Uds]
        iu=int(np.argmin([s[0] for s in su]))
        best_unw[lab]=(Uds[iu],su[iu][0],su[iu][1])
        print(f"  {lab:16s} {Uds[iu]:8.2f} {su[iu][0]:11.4f} {su[iu][1]:9.4f}")
    rival=min((v[1] for k,v in best_unw.items() if k!='F4 standard'))
    d=best_unw['F4 standard'][1]-rival
    verdict='SURVIVES (<0.01)' if d<0.01 else ('DEGRADED (0.01-0.02)' if d<0.02 else 'DISFAVOURED (>0.02)')
    print(f"  -> F4 vs best rival: +{d:.4f} dex  => {verdict}")
print("""
READING per the pre-registered thresholds above; both metrics and both footings shown (artifact-robustness).
The F4 question is the SHAPE in the knee (its tail already passed Saturn); Upsilon freedom granted equally.""")
