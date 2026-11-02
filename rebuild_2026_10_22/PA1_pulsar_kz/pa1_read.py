#!/usr/bin/env python3
"""PA1 part 3: labels on C1 rows (PROVISIONAL, web-read), forecast, non-potential-free reconstruction from Donlon+ 2025's fit parameters. python3 pa1_read.py [--inject]. --inject divides row errors by 20, must fire SEPARATES. Footings never pooled. kappa = 1/2 FITTED; not theory closed."""
import json, sys, math, numpy as np
INJ = "--inject" in sys.argv; G=4.30091e-6; KZU=2*math.pi*G*1e6; GY=1.02271; CONV=json.load(open("pa1_gap.json"))["mm_s_yr_per_K"]; R0=8.122
# rows: log10(alpha/Gyr^-2), +err, -err. All PROVISIONAL, from arXiv HTML pages via a summariser. Heights not readable per pulsar: chord compared over Z. kind chord: a_z = -alpha z over the sample; kind mid: local gradient.
ROWS=[("C21 alpha1 (14 PSR)",3.61,.13,.10,"chord"),("C21 alpha1,beta preferred",3.69,.19,.12,"chord"),("D24 alpha (24 PSR)",3.60,.06,.06,"chord"),("D24 alpha-beta",3.51,.13,.13,"chord"),("D24 anharmonic alpha1",3.51,.08,.08,"mid"),("D24 2alpha-beta alpha1",3.56,.11,.11,"mid"),("D24 local expansion da_z/dz",3.73,.08,.08,"mid")]
out=[]; res={}
def P(s): out.append(s); print(s)
P("All measured values PROVISIONAL (web-read). alpha in Gyr^-2. Chord alpha(z)=a_z/z.")
for f in ("canonical","alt"):
    d=json.load(open(f"pa1_profile_{f}.json")); Z=np.array(d["Z"]); C=d["cells"]
    A=np.array([c["KA"] for c in C]);Q=np.array([c["KQ"] for c in C]);R=np.array([c["KR"] for c in C]);N=np.array([c["KN"] for c in C])
    al=KZU/Z*GY**2
    P(f"\n[{f}] cells {len(C)} of {d['n_cells']} in-prior with form A v_c in line; recover at 1.1: max|A-cache| {max(abs(c['KA'][6]-c['cached_A']) for c in C):.3f}, Q {max(abs(c['KQ'][6]-c['cached_Q']) for c in C):.3f}, R {max(abs(c['KR'][6]-c['cached_R']) for c in C):.3f}; max res {max(c['res'] for c in C):.1e}")
    P(" z kpc | K_A med[min,max] | K_R med[min,max] | gap A-R min,med | log alpha_A med[min,max] | log alpha_R med[min,max] | gap mm/s/yr min | |Q/A-1|max")
    for j,z in enumerate(Z):
        g=A[:,j]-R[:,j]
        P(f" {z:.2f} | {np.median(A[:,j]):.1f}[{A[:,j].min():.1f},{A[:,j].max():.1f}] | {np.median(R[:,j]):.1f}[{R[:,j].min():.1f},{R[:,j].max():.1f}] | {g.min():.2f},{np.median(g):.2f} | {np.log10(np.median(A[:,j])*al[j]):.3f}[{np.log10(A[:,j].min()*al[j]):.3f},{np.log10(A[:,j].max()*al[j]):.3f}] | {np.log10(np.median(R[:,j])*al[j]):.3f}[{np.log10(R[:,j].min()*al[j]):.3f},{np.log10(R[:,j].max()*al[j]):.3f}] | {g.min()*CONV:.3f} | {np.max(np.abs(Q[:,j]/A[:,j]-1)):.4f}")
    res[f]={}
    allc=json.load(open(f"pa1_all_{f}.json")); AQ=np.array(allc["KQ"]); AR=np.array(allc["KR"]); P(f" all in-prior cells for labels: {allc['n']}, form Q for A (|Q/A-1| above), recover at 1.1 max {allc['max_recover']:.1e}")
    for nm,l,ep,em,kind in ROWS:
        v=10**l; sg=v*(10**max(ep,em)-1)
        if INJ: sg/=20
        ja=range(0,3) if kind=="mid" else range(1,7)
        best=0; xA=[];xR=[]
        for j in ja:
            gmin=(AQ[:,j]-AR[:,j]).min()*al[j]; best=max(best,gmin/sg)
            xA.append(min(abs(AQ[:,j]*al[j]-v))/sg if not ((AQ[:,j]*al[j]).min()<=v<=(AQ[:,j]*al[j]).max()) else 0.0); xR.append(min(abs(AR[:,j]*al[j]-v))/sg if not ((AR[:,j]*al[j]).min()<=v<=(AR[:,j]*al[j]).max()) else 0.0)
        lab="SEPARATES" if best>=3 else ("EXCLUDES" if min(xA)>=3 or min(xR)>=3 else "NO POWER")
        res[f][nm]=dict(label=lab,best_sep=best,minZ_A=min(xA),minZ_R=min(xR))
        P(f"  {nm}: {lab}; best gap/sigma over heights {best:.2f}; closest A {min(xA):.2f} sigma, R {min(xR):.2f} sigma, sigma {sg:.0f} Gyr^-2 on {v:.0f}")
    jc=6; gq=(A[:,jc]-R[:,jc])
    gcache=json.load(open("pa1_gap.json"))
    gmin=min(gcache[f"{f} {b} A v_c in line"]["gapA_min"] for b in ("B175","BV","BV2")); gmed=gcache[f"{f} BV2 A v_c in line"]["gapA_med"]; Amin=gcache[f"{f} BV2 A v_c in line"]["KA_min"]
    F=dict(gap_min=gmin,gap_med=gmed,KA_min=Amin,to_line=Amin-70.8)
    for k,x in (("gap_min",gmin),("gap_med",gmed),("KA_min-70.8",Amin-70.8)):
        s_K=x/3; s_mm=s_K*CONV; n=[(s0/(0.5*s_mm))**2 for s0 in (1.6,math.sqrt(2)*1.6)]
        F[k+"_sig"]=dict(sigma_K=s_K,sigma_mm_s_yr=s_mm,N_gauss=n[0],N_cauchy=n[1])
        P(f"  forecast {k} {x:.2f}: need sigma K {s_K:.2f} = {s_mm:.3f} mm/s/yr; N with xi 1.6, projection 0.5 (judgment): {n[0]:.0f} Gaussian, {n[1]:.0f} Lorentzian")
    res[f]["forecast"]=F
# NOT POTENTIAL-FREE: Donlon+ 2025 Table 1, disc + NFW r_s 15.6 normalised to rho_DM at R0. Newtonian functions as fit basis. Errors propagated without covariance: not a measurement of K.
P("\nNOT POTENTIAL-FREE reconstruction, K(R0, 1.1 kpc) from D25 parameters, symmetrised with halo offset. No label possible.")
def halo(z,rho,rs=15.6):
    x0=R0/rs; rhos=rho*1e9/(1/(x0*(1+x0)**2))
    def Mr(r): x=r/rs; return 4*math.pi*rhos*rs**3*(math.log(1+x)-x/(1+x))
    r=math.hypot(R0,z); return G*Mr(r)*z/r**3/KZU
def hsym(z,rho,o): return 0.5*(halo(z+o,rho)+halo(z-o,rho))
def exp_(rhob,h,z): return 2*rhob*1e3*h*(1-math.exp(-z/h))   # Msun/pc^2 with rho Msun/pc^3, h kpc
def iso(s,h,z): return s*s/h*math.tanh(z/h)/KZU
def mn(lm,a,b,z):
    M=10**lm; q=math.hypot(z,b); return G*M*z*(a+q)/(q*(R0**2+(a+q)**2)**1.5)/KZU
z=1.1; rec={}
def mc(fn,pars,n=20000):
    rng=np.random.default_rng(20261102); v=[fn(*[rng.normal(m,e) for m,e in pars]) for _ in range(n)]; return float(np.median(v)),float(np.std(v))
rec["exponential"]=mc(lambda r,h,dm,o:exp_(r-dm,h,z)+hsym(z,dm,o),[(0.130,0.009),(0.21,0.02),(0.010,0.002),(0.68,0.03)])
rec["isothermal"]=mc(lambda s,h,dm,o:iso(s,h,z)+hsym(z,dm,o),[(20.9,0.5),(0.32,0.04),(0.009,0.004),(0.69,0.08)])
rec["Miyamoto-Nagai"]=mc(lambda lm,a,b,dm,o:mn(lm,a,b,z)+hsym(z,dm,o),[(10.9,0.3),(3.1,0.8),(0.28,0.03),(0.010,0.002),(0.7,0.1)])
for k,(m,s) in rec.items(): P(f"  {k}: K(1.1) {m:.1f} +- {s:.1f} ({m*CONV:.2f} +- {s*CONV:.2f} mm/s/yr)")
res["reconstruction"]=rec
overall="CANNOT DECIDE" if not all(any(res[f][r[0]]["label"]!="NO POWER" for r in ROWS) for f in ("canonical","alt")) else "ROW FIRES"
P(f"\nOVERALL: {overall}"); res["overall"]=overall
tag="_INJECT" if INJ else ""
open(f"pa1_read{tag}.out","w").write("\n".join(out)+"\n"); json.dump(res,open(f"pa1_read{tag}.json","w"),indent=1,sort_keys=True)
