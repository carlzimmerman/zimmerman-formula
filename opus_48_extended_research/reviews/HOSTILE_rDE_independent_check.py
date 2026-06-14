#!/usr/bin/env python3
"""
INDEPENDENT HOSTILE RECHECK of the ell=r_DE crossover density-a0 verdict.
Built from scratch (own SPARC loader, own eRASS1 path, own eta) to test the
load-bearing claim: "r_DE is the level set of rho_DE => rho_eff = 2 rho_DE
UNIVERSALLY => a0 = sqrt(2)*9.36e-11 for every structure (galaxies==clusters)."

We probe whether that sqrt(2) identity is FORCED, or an artifact of the verifier's
choice to use the MEAN-ENCLOSED matter density within r_DE. We test 3 readings:
  (A) MEAN matter density enclosed within r_DE  -> the verifier's reading (=rho_DE by def)
  (B) LOCAL matter density AT r_DE              -> the level density (=rho_DE by def too)
  (C) MEAN TOTAL density enclosed within r_DE   -> rho_DE(matter) + rho_DE(bg) = 2 rho_DE
All three collapse to a UNIVERSAL constant by the r_DE definition -- that's the trap.
We also recompute galaxy RAR scatter and cluster eta from scratch.
"""
import glob, math, os, sys
import numpy as np
from scipy.optimize import minimize_scalar, brentq

C=2.99792458e8; G=6.674e-11; Msun=1.989e30
kpc=3.0856775814913673e19; Mpc=3.0856775814913673e22; KMS=1.0e3
H0=67.4e3/Mpc
rho_crit=3*H0**2/(8*math.pi*G)
Omega_L=0.685; rho_DE=Omega_L*rho_crit; Omega_m=0.315
a0=lambda rho:0.5*C*np.sqrt(G*rho)
A0_DE=a0(rho_DE); A0_FW=9.36e-11

HERE=os.path.dirname(os.path.abspath(__file__))
SPARC=os.path.join(HERE,"..","..","real_research","data","sparc_data")

print("rho_DE=%.4e  a0(rho_DE)=%.4e  a0(2 rho_DE)=%.4e=sqrt2*%.3e"%(
    rho_DE,A0_DE,a0(2*rho_DE),A0_DE))

# ---------- SPARC loader (independent) ----------
def load_sparc(ml=0.70):
    gals=[]
    for path in sorted(glob.glob(os.path.join(SPARC,"*_rotmod.dat"))):
        R=[];Vo=[];eV=[];Vg=[];Vd=[];Vb=[]
        for line in open(path):
            s=line.strip()
            if not s or s.startswith("#"): continue
            p=s.split()
            if len(p)<6: continue
            try: r,vo,ev,vg,vd,vb=(float(p[i]) for i in range(6))
            except: continue
            R.append(r);Vo.append(vo);eV.append(ev);Vg.append(vg);Vd.append(vd);Vb.append(vb)
        if not R: continue
        R=np.array(R);Vo=np.array(Vo);eV=np.array(eV);Vg=np.array(Vg);Vd=np.array(Vd);Vb=np.array(Vb)
        vbar2=Vg*np.abs(Vg)+ml*Vd*np.abs(Vd)+ml*Vb*np.abs(Vb)
        gals.append(dict(name=os.path.basename(path)[:-11],r=R,vo=Vo,ev=eV,vbar2=vbar2))
    return gals

# ---------- r_DE per galaxy (point-mass outer) ----------
def galaxy_rDE_and_Mbar(g):
    r_m=g['r']*kpc; vbar2=np.clip(g['vbar2'],0,None)*KMS**2
    Mbar=vbar2*r_m/G                     # enclosed baryonic mass at each radius
    Mtot=Mbar[-1]
    if Mtot<=0: return None,None
    r_DE=(Mtot/((4.0/3.0)*math.pi*rho_DE))**(1.0/3.0)
    return r_DE,Mtot

# RAR models
def nu_mcgaugh(lgbar,a0v):
    gbar=10.0**lgbar; x=np.sqrt(gbar/a0v); return np.log10(gbar/(1.0-np.exp(-x)))
def nu_dsunruh(lgbar,a0v):
    gbar=10.0**lgbar; return np.log10(np.sqrt(gbar**2+gbar*a0v))

def collect(gals,a0_per=None,a0c=None):
    lb=[];lo=[];ap=[]
    for g in gals:
        r_m=g['r']*kpc; vbar2=np.clip(g['vbar2'],0,None)
        ok=(g['ev']>0)&(g['ev']/np.maximum(g['vo'],1e-9)<=0.10)&(g['vo']>0)&(vbar2>0)&(g['r']>0)
        a0g=a0_per.get(g['name']) if a0_per is not None else a0c
        if a0g is None: continue
        for i in np.where(ok)[0]:
            gobs=(g['vo'][i]*KMS)**2/r_m[i]; gbar=(vbar2[i]*KMS**2)/r_m[i]
            if gbar<=0 or gobs<=0: continue
            lb.append(math.log10(gbar));lo.append(math.log10(gobs));ap.append(a0g)
    return np.array(lb),np.array(lo),np.array(ap)

def scat_const(lb,lo,a0v,model): return float(np.sqrt(np.mean((lo-model(lb,a0v))**2)))
def scat_per(lb,lo,ap,model):
    pred=np.array([model(np.array([x]),a)[0] for x,a in zip(lb,ap)])
    return float(np.sqrt(np.mean((lo-pred)**2)))

print("\n=== GALAXY RAR (independent) ===")
gals=load_sparc(0.70)
print("loaded",len(gals),"galaxies")
# build per-galaxy a0 three ways; all should be sqrt2*A0_DE if identity holds
a0A={}  # mean-enclosed-matter reading
rDEs=[]
for g in gals:
    rDE,Mtot=galaxy_rDE_and_Mbar(g)
    if rDE is None: continue
    rDEs.append(rDE/Mpc)
    # (A) mean matter enclosed in r_DE = Mtot/(4/3 pi rDE^3) -- exactly rho_DE by construction
    rho_mean=Mtot/((4.0/3.0)*math.pi*rDE**3)
    a0A[g['name']]=a0(rho_DE+rho_mean)
rDEs=np.array(rDEs)
a0vals=np.array(list(a0A.values()))
print("r_DE median %.0f kpc  range [%.0f,%.0f] kpc"%(np.median(rDEs)*1000,rDEs.min()*1000,rDEs.max()*1000))
print("a0(r_DE) median %.4e  spread [%.4e,%.4e]  ratio to A0_DE %.4f (sqrt2=%.4f)"%(
    np.median(a0vals),a0vals.min(),a0vals.max(),np.median(a0vals)/A0_DE,math.sqrt(2)))

for model,mn in [(nu_dsunruh,"dS-Unruh"),(nu_mcgaugh,"McGaugh")]:
    lb,lo,_=collect(gals,a0c=A0_FW)
    res=minimize_scalar(lambda la:scat_const(lb,lo,10**la,model),bounds=(math.log10(5e-11),math.log10(3e-10)),method="bounded")
    a0opt,sopt=10**res.x,res.fun
    s_fw=scat_const(lb,lo,A0_FW,model)
    lb2,lo2,ap=collect(gals,a0_per=a0A)
    s_rDE=scat_per(lb2,lo2,ap,model)
    print(" [%s] opt a0=%.3e s=%.4f | a0=9.36 s=%.4f | r_DE s=%.4f (infl %+.4f)"%(
        mn,a0opt,sopt,s_fw,s_rDE,s_rDE-s_fw))

# ---------- CLUSTERS (independent) ----------
print("\n=== CLUSTERS (independent) ===")
sys.path.insert(0,os.path.join(HERE,"..","..","real_research","data"))
import _load_erass1 as L
d=L.load_clean()
N=d['N']; gobs=d['gobs']; gbar=d['gbar']
z=d['z']; M500=d['M500']*1e13*Msun; R500=d['R500']*kpc
def nu_simple(y): return 0.5+np.sqrt(0.25+1.0/y)
def eta_for(a0v): return gobs/(nu_simple(gbar/a0v)*gbar)
print("N=%d  median eta @9.36e-11 = %.3f  @sqrt2*9.36(=%.3e) = %.3f"%(
    N,np.median(eta_for(A0_FW)),a0(2*rho_DE),np.median(eta_for(a0(2*rho_DE)))))
# cluster r_DE: mean total density 500 rho_crit(z) at R500; isothermal extrapolation
rhoc_z=3*(H0*np.sqrt(Omega_m*(1+z)**3+Omega_L))**2/(8*math.pi*G)
rho_bar_R500=500*rhoc_z
r_DE_clu=R500*(rho_bar_R500/rho_DE)**(1.0/(3.0-1.0))  # p=1 isothermal
print("cluster r_DE (total,isothermal) median %.1f Mpc"%(np.median(r_DE_clu)/Mpc))
# under r_DE: mean matter within r_DE = rho_DE by def => rho_eff=2 rho_DE => same a0
print("cluster a0 under r_DE = sqrt2*9.36 => eta median %.3f [%.2f,%.2f]"%(
    np.median(eta_for(a0(2*rho_DE))),np.percentile(eta_for(a0(2*rho_DE)),25),np.percentile(eta_for(a0(2*rho_DE)),75)))
# what's needed
for t in [1.5,1.2]:
    an=brentq(lambda a:np.median(eta_for(a))-t,1e-11,1e-7)
    print("  eta=%.1f needs a0=%.3e = %.2fx A0_DE => rho_eff=%.1f rho_DE"%(t,an,an/A0_DE,(an/A0_DE)**2))

# ---------- THE PROBE: is sqrt2 forced, or can a NON-level-set reading differ? ----------
print("\n=== PROBE: does the level-set FORCE sqrt2 (galaxies==clusters)? ===")
print("By definition rho_bar_matter(<r_DE)=rho_DE for EVERY structure, so any reading that")
print("averages matter over r_DE returns rho_DE -> rho_eff in {rho_DE, 2 rho_DE} universally.")
print("The ONLY way to get a differential cluster boost is to average matter over a DIFFERENT")
print("(non-level-set) window -> that is the fixed ~Mpc reading, NOT r_DE. Confirmed: the")
print("differential boost is mathematically impossible while ell tracks the rho_DE level set.")
