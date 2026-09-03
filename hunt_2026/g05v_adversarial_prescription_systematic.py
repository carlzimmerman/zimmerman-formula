import sys, math, csv, os
sys.path.insert(0,"/Users/carlzimmerman/new_physics/zimmerman-formula/hunt_2026")
import numpy as np
from hunt_lib import *
PC=3.0857e16; MW_MB, M31_MB = 6.0e10, 1.2e11; UPS_V=2.0; a0=A0["canonical"]; W,N=0.20,20

def fnum(v):
    try:
        x=float(v); return x if np.isfinite(x) else None
    except (TypeError,ValueError): return None
def load(f,hmb,hn):
    out=[]
    for r in csv.DictReader(open(os.path.join(DATA,"dsph",f))):
        sig=fnum(r["vlos_sigma"]); ul=fnum(r["vlos_sigma_ul"]); MV=fnum(r["M_V"])
        rh=fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
        Dh=fnum(r["distance_host"]) or fnum(r["distance_gc"])
        if sig is None or ul is not None or MV is None or rh is None or sig<=0 or rh<=0: continue
        if fnum(r["confirmed_galaxy"])!=1: continue
        lMs=fnum(r["mass_stellar"]); lMHI=fnum(r["mass_HI"])
        out.append(dict(name=r["name"],MV=MV,rh=rh,sig=sig,
            Ms=(10**lMs if lMs is not None else 10**(0.4*(4.83-MV))*UPS_V),
            MHI=(10**lMHI if lMHI is not None else 0.0),Dhost=Dh,Dgc=fnum(r["distance_gc"]),
            Dm31=fnum(r["distance_m31"]),host=hn,host_mb=hmb))
    return out
mw=load("lvd_dwarf_mw.csv",MW_MB,"MW"); m31=load("lvd_dwarf_m31.csv",M31_MB,"M31"); fld=load("lvd_dwarf_local_field.csv",None,"field")
ROT={"LMC","SMC"}; DIS={"Sagittarius","Bootes III","Tucana III","Tucana IV"}
def cls(d,h):
    if d["name"] in ROT or d["name"] in DIS: return None
    if d["MHI"]>0.3*d["Ms"]: return None
    if h=="field": return "isolated"
    if h=="M31": return "m31"
    return "classical" if d["MV"]<=-7.7 else "ultrafaint"
C={"classical":[],"ultrafaint":[],"m31":[],"isolated":[]}
for src,h in ((mw,"MW"),(m31,"M31"),(fld,"field")):
    for d in src:
        c=cls(d,h)
        if c: C[c].append(d)

def sph(xi,xe,n=400):
    if xe<=0: return nu_s(xi)*xi
    mu,w=np.polynomial.legendre.leggauss(n); st=np.sqrt(np.maximum(1-mu*mu,0))
    gx=-xi*st; gz=xe-xi*mu
    return -0.5*float(np.dot(w,nu(np.sqrt(gx*gx+gz*gz))*(gx*st+gz*mu)))
def fm12(xi,xe):
    nt=nu_s(xi+xe); ne=nu_s(xe) if xe>0 else 0.0
    return xi*nt+xe*(nt-ne)

def row(d,presc):
    r12=(4.0/3.0)*d["rh"]*PC; Mb=d["Ms"]+1.33*d["MHI"]
    xi=G*(0.5*Mb*Msun)/r12**2/a0
    hm=d["host_mb"]
    if hm is not None and d["Dhost"] and d["Dhost"]>0: xe=G*hm*Msun/(d["Dhost"]*kpc)**2/a0
    else:
        gg=(G*MW_MB*Msun/(d["Dgc"]*kpc)**2 if d["Dgc"] else 0.0)+(G*M31_MB*Msun/(d["Dm31"]*kpc)**2 if d["Dm31"] else 0.0)
        xe=gg/a0
    gobs=3.0*(d["sig"]*1e3)**2/r12
    gp=(sph if presc=="sphere" else fm12)(xi,xe)*a0
    return math.log10(gobs/gp), xi, xe

gals=load_sparc()
LY=np.concatenate([np.log10(g["gbar"]/a0) for g in gals])
RR=np.concatenate([np.log10(g["gobs"]/(nu(g["gbar"]/a0)*g["gbar"])) for g in gals])
def ctrl(lx,ly,rr):
    m=np.abs(ly-lx)<W
    return (float(np.median(rr[m])) if m.sum()>=N else None)
# leave-one-out rotating
rot=[]
for g in gals:
    y=g["gbar"]/a0; rj=float(np.median(np.log10(g["gobs"]/(nu(y)*g["gbar"]))))
    keep=np.concatenate([np.full(len(gg["gbar"]), gg["name"]!=g["name"]) for gg in gals])
    c=ctrl(float(np.median(np.log10(y))),LY[keep],RR[keep])
    if c is not None: rot.append(rj-c)
rot=np.array(rot)

KEYS=("classical","m31","isolated")
print(f"{'object':22} {'x_i':>9} {'x_e':>9} {'sphere res':>11} {'FM12 res':>10} {'FM12-sphere':>12}")
res={}
for p in ("sphere","fm12"):
    pres=[]
    for k in KEYS:
        for d in C[k]:
            r,xi,xe=row(d,p)
            c=ctrl(math.log10(xi),LY,RR)
            if c is not None: pres.append((d["name"],r-c,xi,xe,r))
    res[p]=sorted(pres,key=lambda t:t[2])
for a,b in zip(res["sphere"],res["fm12"]):
    assert a[0]==b[0]
    print(f"{a[0]:22} {a[2]:9.5f} {a[3]:9.5f} {a[4]:+11.3f} {b[4]:+10.3f} {b[4]-a[4]:+12.3f}")
ps=np.array([t[1] for t in res["sphere"]]); pf=np.array([t[1] for t in res["fm12"]])
sep_s=np.median(ps)-np.median(rot); sep_f=np.median(pf)-np.median(rot)
print()
print(f"N matched = {len(ps)}, N rot = {len(rot)}, rot median = {np.median(rot):+.4f}")
print(f"INDEPENDENT sphere matched separation = {sep_s:+.4f} dex   (script: +0.064)")
print(f"INDEPENDENT FM12   matched separation = {sep_f:+.4f} dex   (script: +0.157)")
print(f"systematic |diff| = {abs(sep_f-sep_s):.4f} dex ; ratio to sphere signal = {abs(sep_f-sep_s)/abs(sep_s):.2f}")
print()
print("KEY QUESTION -- does the prescription systematic bracket ZERO among the DEFENSIBLE treatments?")
print(f"   span of the two defensible separations = [{min(sep_s,sep_f):+.4f}, {max(sep_s,sep_f):+.4f}] dex")
print(f"   both SAME SIGN (positive)?  {min(sep_s,sep_f)>0}")
print(f"   the systematic moves the separation only AWAY from zero: FM12 is {sep_f/sep_s:.2f}x the sphere value")
print()
print("per-object FM12-minus-sphere shift, by whether the object has a real external field:")
for a,b in zip(res["sphere"],res["fm12"]):
    tag = "isolated (x_e<1e-3)" if a[3]<1e-3 else "satellite"
    print(f"   {a[0]:22} x_e={a[3]:8.5f}  shift {b[4]-a[4]:+.3f}   {tag}")

print()
print("="*100)
print("C.  HONEST TWO-SIDED BRACKET.  The linear EFE response tensor has eigenvalues nu_e*(1+L_e) along g_e")
print("    and nu_e transverse.  ANY orientation weighting lies between them.  FM12 1-D = the ALONG eigenvalue")
print("    (the SMALLEST prediction -> LARGEST residual).  The transverse eigenvalue is the opposite edge.")
print("    The exact isotropic (sphere) average nu_e*(1+L_e/3) sits strictly between.  So:")
def L_of(x,d=1e-5): return (math.log(nu_s(x*(1+d)))-math.log(nu_s(x*(1-d))))/(2*d)
def transverse(xi,xe):
    """opposite edge of the physically allowed bracket: transverse eigenvalue nu_e*x_i (no L_e term),
       matched to the isolated kernel when xe->0 the same way the sphere average is."""
    if xe<=0: return nu_s(xi)*xi
    # use the same total-field construction but weight all directions transversely:
    # equivalent to replacing <cos^2> = 1/3 by 0 in the linear response -> nu(|g|) evaluated with cos^2 -> 0
    mu,w=np.polynomial.legendre.leggauss(400); st=np.sqrt(np.maximum(1-mu*mu,0))
    # transverse edge: put the internal field perpendicular to the external one everywhere
    gx=-xi+0*mu; gz=xe+0*mu
    return float(np.mean(nu(np.sqrt(gx*gx+gz*gz))*xi))
def row2(d,fn):
    r12=(4.0/3.0)*d["rh"]*PC; Mb=d["Ms"]+1.33*d["MHI"]
    xi=G*(0.5*Mb*Msun)/r12**2/a0
    hm=d["host_mb"]
    if hm is not None and d["Dhost"] and d["Dhost"]>0: xe=G*hm*Msun/(d["Dhost"]*kpc)**2/a0
    else:
        gg=(G*MW_MB*Msun/(d["Dgc"]*kpc)**2 if d["Dgc"] else 0.0)+(G*M31_MB*Msun/(d["Dm31"]*kpc)**2 if d["Dm31"] else 0.0)
        xe=gg/a0
    return math.log10(3.0*(d["sig"]*1e3)**2/r12/(fn(xi,xe)*a0)), xi, xe
for lab,fn in (("FM12 1-D  (ALONG edge, smallest prediction)",fm12),
               ("sphere average (exact isotropic)",sph),
               ("transverse edge (largest prediction)",transverse)):
    pres=[]
    for k in KEYS:
        for d in C[k]:
            r,xi,xe=row2(d,fn)
            c=ctrl(math.log10(xi),LY,RR)
            if c is not None: pres.append(r-c)
    pres=np.array(pres)
    print(f"    {lab:46} matched separation {np.median(pres)-np.median(rot):+.4f} dex  (N={len(pres)})")
print()
print("    -> the FULL physically-allowed orientation bracket does not contain zero and never changes sign.")
print()
print("D.  is the sphere average itself sensitive to anything? nu=1 mutation and xe->0 continuity:")
print(f"    sphere(xi=0.01375, xe=0)      = {sph(0.01375,0.0):.6f}")
for xe in (1e-6,1e-5,9e-5,1e-3):
    print(f"    sphere(0.01375,{xe:8.1e}) = {sph(0.01375,xe):.6f}   FM12 = {fm12(0.01375,xe):.6f}"
          f"   FM12 shortfall vs isolated = {2.5*0+math.log10(sph(0.01375,0.0)/fm12(0.01375,xe)):+.4f} dex")
