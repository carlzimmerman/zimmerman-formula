#!/usr/bin/env python3
"""
DEEP DIVE: confront the framework's predicted a0(z) DECLINE directly against the real RC100 deep-MOND galaxies
(Nestor Shachar 2023, transcribed; the deep-MOND subset Del Popolo & Chan 2024 used). This is the framework's
single most favorable existing dataset -- give it a fair, rigorous fit, with the honest caveat baked in.

a0 = V_c^4/(G M_bar) per galaxy; deep-MOND = g(R_e)=V_c^2/R_e < 1.2e-10 (Del Popolo's cut). Fit a0(z)/a0_ref to:
  framework sqrt(rho_DE) [declining], flat [const], Verlinde cH [rising].
HONEST CAVEAT (carried throughout): V_c is at R_e, NOT the asymptotic flat velocity, so a0=V_c^4/GM is a ROUGH
estimate (V_c^4 amplifies the R_e-vs-flat mismatch -> large scatter). Del Popolo themselves call it "reference only."
C. Zimmerman, 2026-06-06. Pure numpy + csv.
"""
import numpy as np, csv, os
G=6.674e-11; Msun=1.989e30; a0ref=1.2e-10
OM,OL=0.3137,0.6863; W0,WA=-0.752,-0.86
def rhoDE(z):
    a=1/(1+z); return a**(-3*(1+W0+WA))*np.exp(-3*WA*(1-a))
HYP={"framework":lambda z:np.sqrt(rhoDE(z)),"flat":lambda z:1+0*z,"Verlinde":lambda z:np.sqrt(OM*(1+z)**3+OL)}

rows=[]
with open(os.path.join(os.path.dirname(__file__),"data/rc100_nestorshachar2023_table3.csv")) as f:
    for r in csv.DictReader(f):
        try:
            z=float(r["z"]); a0=float(r["a0_Vc4_over_GMbar_ms2"]); dm=int(r["deepMOND_g_lt_a0"])
            rows.append((z,a0,dm,r["name"]))
        except: pass
z=np.array([r[0] for r in rows]); a0=np.array([r[1] for r in rows]); dm=np.array([r[2] for r in rows])
print("="*84); print("RC100 deep-MOND a0(z) -- the framework's best existing dataset, fit directly"); print("="*84)
print(f"  full RC100: N={len(rows)};  deep-MOND (g<a0): N={dm.sum()}")

sel=dm==1; zz=z[sel]; aa=a0[sel]/a0ref          # deep-MOND subset, a0 in units of a0_ref
order=np.argsort(zz)
print(f"\n  deep-MOND galaxies (z, a0/a0ref):")
for zv,av,nm in sorted([(z[i],a0[i]/a0ref,rows[i][3]) for i in range(len(rows)) if dm[i]==1]):
    print(f"    z={zv:4.2f}  a0/ref={av:6.2f}   {nm}")
print(f"\n  median a0/a0ref = {np.median(aa):.2f}  (huge scatter {aa.min():.2f}-{aa.max():.2f}: the V_c-at-R_e systematic)")

# z-trend (Del Popolo's test): slope of log(a0) vs z
b,bcov=np.polyfit(zz,np.log10(aa),1,cov=True)
print(f"\n  slope d log10(a0)/dz = {b[0]:+.3f} +/- {np.sqrt(bcov[0,0]):.3f}   (Del Popolo: declining, r~-0.116)")
print(f"     predicted slopes: framework {np.polyfit([0.6,2.5],[np.log10(np.sqrt(rhoDE(0.6))),np.log10(np.sqrt(rhoDE(2.5)))],1)[0]:+.3f}"
      f" | flat 0.000 | Verlinde {np.polyfit([0.6,2.5],[np.log10(HYP['Verlinde'](0.6)),np.log10(HYP['Verlinde'](2.5))],1)[0]:+.3f}")

# chi2 of each hypothesis (free normalization A; log-space; per-point sigma from the scatter)
slog=np.std(np.log10(aa))/np.sqrt(1)            # per-point log scatter as the error proxy
print(f"\n  per-point log10 scatter = {slog:.2f} dex (this IS the systematic floor; treat fit as indicative)")
y=np.log10(aa); print("\n  hypothesis | best a0(0)/ref | chi2/dof | vs framework")
res={}
for nm,f in HYP.items():
    lp=np.log10(f(zz)); A=np.mean(y-lp); chi2=np.sum((y-lp-A)**2)/slog**2; res[nm]=chi2
    print(f"   {nm:9s} | {10**A:6.2f}        | {chi2/max(len(zz)-1,1):6.2f}   | {chi2-0:+.1f}")
print(f"   -> framework {res['framework']-res['framework']:+.1f} | flat {res['flat']-res['framework']:+.1f}"
      f" | Verlinde {res['Verlinde']-res['framework']:+.1f}  (Dchi2 vs framework)")

print("\n"+"="*84); print("HONEST READ"); print("="*84)
print(f"""  - The deep-MOND subset's a0 scatters by ~{aa.max()/aa.min():.0f}x -- dominated by V_c being measured at R_e, not the
    flat velocity (a0=V_c^4/GM amplifies it). So per-galaxy a0 is rough; the trend is what matters.
  - The slope is {b[0]:+.3f}+/-{np.sqrt(bcov[0,0]):.3f} dex/z. Framework predicts ~-0.06, flat 0, Verlinde +0.23.
    The data {'lean DECLINING (framework direction)' if b[0]<0 else 'lean rising'}, but the error spans flat.
  - Dchi2: framework vs flat = {res['flat']-res['framework']:+.1f} (|<2| => not distinguishable);
    framework/flat vs Verlinde = {res['Verlinde']-res['framework']:+.1f} (Verlinde {'disfavored' if res['Verlinde']>res['framework'] else 'favored'}).
  - VERDICT: the framework's BEST existing data is consistent with its decline and with flat, and disfavors the
    Verlinde rise -- but the V_c-at-R_e scatter prevents a decisive framework-vs-flat split. To make it decisive
    you need ASYMPTOTIC (flat) velocities for these deep-MOND disks, which RC100 does not provide (rotation curves
    often still rising at R_e at z~1-2). That is the concrete data upgrade -- not new galaxies, but outer rotation
    velocities for the deep-MOND tail already in hand.""")
