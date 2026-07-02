#!/usr/bin/env python3
"""ADVERSARIAL SPOT-CHECK of lane L6 (independent re-implementation, not a re-run).
Checks: (1) independent SPARC load + floor census; (2) the s-statistic distribution
(mean vs median vs empirical percentiles -- is 'max ~16% suppression' skew-inflated?);
(3) exclusion sigma with an alternative robust estimator; (4) MIGHTEE deep median;
(5) framework's OWN nu used (a0_eff estimator is the exact inversion)."""
import numpy as np, glob, os, re
from scipy import integrate, optimize

c=299792458.0; Mpc=3.0856775814913673e22; H0=67.4e3/Mpc; kpc=3.0857e19
a0_DW=c*H0/np.sqrt(30.0); a0_fw=c*H0*np.sqrt(3*0.685/(32*np.pi))
print(f"a0_DW={a0_DW:.4e}  a0_fw={a0_fw:.4e}")
assert abs(a0_fw-9.3624e-11)<2e-14 and abs(a0_DW-1.1956e-10)<2e-13

def make_B(Or,Om,OL):
    f=lambda u:(Or+0.5*Om*u-OL*u**4)/np.sqrt(Or+Om*u+OL*u**4)
    return lambda z:6*np.sqrt(30)*(1+z)**3*integrate.quad(f,0,1/(1+z),limit=400)[0]
Bs=[make_B(1e-4,0.300,0.700),make_B(1e-4,0.3089,1-1e-4-0.3089),make_B(9.2e-5,0.315,0.685)]
zc=[optimize.brentq(B,0.01,0.4) for B in Bs]
print(f"z_c: paper={zc[0]:.4f}  P15(Kim)={zc[1]:.4f}  P18={zc[2]:.4f}  (Kim+ paper: 0.0880)")
assert abs(zc[1]-0.0880)<0.002
floor_char=lambda z:0.5*a0_DW*min(abs(B(z)) for B in Bs)

DATA="/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
Ud=0.70; Ub=1.4*Ud
n_deep=n_below=0; s_gal=[]; off_gal=[]
for f in sorted(glob.glob(os.path.join(DATA,"*_rotmod.dat"))):
    m=re.search(r"Distance\s*=\s*([\d.]+)\s*Mpc",open(f).readline())
    if not m: continue
    z=H0*float(m.group(1))*Mpc/c
    try: d=np.genfromtxt(f,comments="#")
    except Exception: continue
    if d.ndim!=2 or d.shape[1]<6: continue
    R,Vo,eV,Vg,Vd,Vb=(d[:,i] for i in range(6))
    gb=(np.sign(Vg)*Vg**2+Ud*Vd**2+Ub*Vb**2)*1e6/(R*kpc); go=(Vo*1e3)**2/(R*kpc)
    ok=(gb>0)&(go>0)&np.isfinite(gb)&np.isfinite(go)&(Vo>0)
    gb,go=gb[ok],go[ok]
    deep=gb<0.1*a0_fw
    if not deep.any(): continue
    fl=floor_char(z); below=go[deep]<fl
    n_deep+=deep.sum(); n_below+=below.sum()
    if below.sum()>=2:
        gbb,gob=gb[deep][below],go[deep][below]
        s_gal.append(np.median((gob**2-gbb**2)/(a0_DW*gbb)))
        off_gal.append(np.median(np.log10(gob/gbb)))
s_gal=np.array(s_gal); off=np.array(off_gal); N=len(s_gal)
print(f"\nCENSUS (independent): deep={n_deep}, below charitable floor={n_below} ({100*n_below/n_deep:.1f}%), N_gal={N}")
mu,sd=off.mean(),off.std(ddof=1)
print(f"offset vs Newtonian: {mu:+.3f} +/- {sd/np.sqrt(N):.3f} dex -> {mu/(sd/np.sqrt(N)):.1f} sigma")
# robust alt: sign test -- how many galaxies have offset > 0?
npos=(off>0).sum()
from scipy import stats
print(f"sign test: {npos}/{N} galaxies ABOVE Newtonian; binomial p = {stats.binomtest(npos,N,0.5).pvalue:.2e}")
print(f"\ns distribution across galaxies (s = a0_eff/a0_DW on dead-branch points):")
q=np.percentile(s_gal,[5,25,50,75,95])
print(f"  mean={s_gal.mean():.3f}  median={np.median(s_gal):.3f}  p5={q[0]:.3f} p25={q[1]:.3f} p75={q[3]:.3f} p95={q[4]:.3f}")
print(f"  mean-based 95%LB = {s_gal.mean()-1.645*s_gal.std(ddof=1)/np.sqrt(N):.3f}")
# bootstrap the MEDIAN galaxy s (robust to skew)
rng=np.random.default_rng(7)
bm=np.array([np.median(rng.choice(s_gal,N)) for _ in range(4000)])
print(f"  bootstrap median-galaxy s: {np.median(s_gal):.3f} +/- {bm.std():.3f}; 95%LB(median) = {np.percentile(bm,5):.3f}")
print(f"  => skew check: mean {'>' if s_gal.mean()>np.median(s_gal) else '<'} median; "
      f"max-suppression via MEDIAN galaxy = {100*(1-np.percentile(bm,5)):.0f}% (headline used mean: ~16%)")
# framework nu inversion sanity: if g_obs = sqrt(gb^2+gb a0) exactly, (go^2-gb^2)/gb == a0
gbt=np.logspace(-13,-10,5); got=np.sqrt(gbt**2+gbt*a0_fw)
assert np.allclose((got**2-gbt**2)/gbt, a0_fw), "a0_eff estimator is NOT the exact framework-nu inversion"
print("\nframework-nu inversion: (go^2-gb^2)/gb recovers a0 EXACTLY on the framework's own locus -- OK")
# MIGHTEE deep median
MD="/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/next_doors_2026_07"
d=np.genfromtxt(os.path.join(MD,"mightee_rar_extracted.csv"),delimiter=",",comments="#")
gb,go=10**d[:,0],10**d[:,1]; deep=gb<0.1*a0_fw
a0m=(go[deep]**2-gb[deep]**2)/gb[deep]
print(f"MIGHTEE fiducial: {deep.sum()} deep pts, median a0_eff = {np.median(a0m):.3e} (lane: 1.71e-10)")
print("EXIT 0")
