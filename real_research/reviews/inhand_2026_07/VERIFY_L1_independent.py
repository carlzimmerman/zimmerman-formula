#!/usr/bin/env python3
"""ADVERSARIAL VERIFIER for lane L1 -- fully independent re-derivation (own loader, own
likelihood code; nothing imported from the lane script). Spot-checks:
  V1. constants: a0 = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z = 9.36e-11 (both routes)
  V2. sign of the inclination correction (synthetic recovery test)
  V3. published-config anchor: McGaugh nu, U=0.5, D=D0, i=i0, f=0 -> a0_hat ~1.2e-10
  V4. full-sample framework-nu optimum direction (simple config, U=0.5, f profiled)
  V5. gas-dominated cut (framework nu, U=0.5 fixed, f=0 and f profiled): optimum vs 9.36e-11
  V6. sample counts: 175 rotmod files, 171 base, 37 gas-dom, 94 star-dom
"""
import numpy as np, glob, os

c=2.998e8; G=6.674e-11; kpc=3.0857e19; H0=2.184e-18; OmL=0.685
# V1 -- two independent routes to a0
Lam = 3*OmL*H0**2/c**2                      # m^-2, Lambda = 3 Omega_L H0^2 / c^2
a0_route1 = c**2*np.sqrt(Lam/(32*np.pi))
HLam = H0*np.sqrt(OmL); Z = np.sqrt(32*np.pi/3)
a0_route2 = c*HLam/Z
print(f"V1: a0 route1(c^2 sqrt(L/32pi))={a0_route1:.4e}  route2(cH_L/Z)={a0_route2:.4e}")
assert abs(a0_route1/9.36e-11-1)<0.005 and abs(a0_route2/a0_route1-1)<1e-12
A0FW = a0_route1

# V2 -- inclination sign: published V_obs assumed i0; if true inc is i, V_true = V_obs*sin(i0)/sin(i)
# synthetic: true rotation 100 km/s, true i=60deg -> V_los=100*sin(60); catalog wrongly used i0=45
Vlos = 100*np.sin(np.radians(60)); Vpub = Vlos/np.sin(np.radians(45))
Vcorr = Vpub*np.sin(np.radians(45))/np.sin(np.radians(60))
print(f"V2: published(45deg)={Vpub:.2f} -> corrected at true 60deg = {Vcorr:.2f} (must be 100)")
assert abs(Vcorr-100)<1e-9

# own loader
ROOT="/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data"
gals=[]
files = sorted(glob.glob(os.path.join(ROOT,"sparc_data","*_rotmod.dat")))
for f in files:
    d=np.genfromtxt(f,comments="#")
    if d.ndim!=2 or d.shape[1]<6: continue
    R,Vo,eV,Vg,Vd,Vb = d[:,0],d[:,1],d[:,2],d[:,3],d[:,4],d[:,5]
    ok=(Vo>0)&(eV>0)
    if ok.sum()<5: continue
    gals.append(dict(name=os.path.basename(f).split("_rotmod")[0],
                     R=R[ok],Vo=Vo[ok],eV=eV[ok],Vg=Vg[ok],Vd=Vd[ok],Vb=Vb[ok]))
print(f"V6: rotmod files={len(files)}  base sample N={len(gals)}")
assert len(files)==175 and len(gals)==171

def gasfrac(g,U=0.5):
    num=np.sum(np.sign(g["Vg"])*g["Vg"]**2)
    return num/max(num+U*np.sum(g["Vd"]**2)+1.4*U*np.sum(g["Vb"]**2),1e-30)
gf=np.array([gasfrac(g) for g in gals])
print(f"V6: gas-dom N={(gf>0.5).sum()}  star-dom N={(gf<0.3).sum()}")
assert (gf>0.5).sum()==37 and (gf<0.3).sum()==94

nu_fw  = lambda y: np.sqrt(1+1/y)
nu_mcg = lambda y: 1/(1-np.exp(-np.sqrt(y)))

def fit(sub, nu, U=0.5, fgrid=(0.0,)):
    """velocity-space -2lnL, nuisances fixed at catalog (D=D0,i=i0), global f profiled"""
    a0s=np.geomspace(0.5e-10,3.5e-10,141)
    tot=np.zeros((len(a0s),len(fgrid)))
    for g in sub:
        Rm=g["R"]*kpc
        gb=(np.sign(g["Vg"])*g["Vg"]**2+U*g["Vd"]**2+1.4*U*g["Vb"]**2)*1e6/Rm
        m=gb>0
        if m.sum()<3: continue
        Rm,Vo,eV,gb=Rm[m],g["Vo"][m],g["eV"][m],gb[m]
        for ja,a0 in enumerate(a0s):
            Vm=np.sqrt(nu(gb/a0)*gb*Rm)/1e3
            for jf,f in enumerate(fgrid):
                s2=eV**2+(f*Vo)**2
                tot[ja,jf]+=np.sum((Vo-Vm)**2/s2+np.log(2*np.pi*s2))
    prof=tot.min(axis=1); i=int(np.argmin(prof))
    dfw =prof[np.argmin(abs(a0s-A0FW))]-prof[i]
    dfk =prof[np.argmin(abs(a0s-1.13e-10))]-prof[i]
    return a0s[i],dfw,dfk

FG=(0.0,0.02,0.04,0.055,0.06,0.07,0.08,0.10,0.12,0.15)
a,dfw,dfk = fit(gals,nu_mcg,0.5,(0.0,))
print(f"V3: McGaugh nu, U=0.5, D0/i0 fixed, f=0 (published config): a0_hat={a:.3e} "
      f"(lane 1.198e-10; McGaugh/Li published ~1.2e-10)")
assert 1.1e-10<a<1.3e-10
a,dfw,dfk = fit(gals,nu_fw,0.5,FG)
print(f"V4: framework nu, full, U=0.5 fixed, f profiled: a0_hat={a:.3e}  "
      f"Dchi2(9.36e-11)={dfw:.0f}  Dchi2(1.13e-10)={dfk:.0f}  (direction: optimum ABOVE 9.36e-11)")
assert a>A0FW
sub=[g for g,s in zip(gals,gf>0.5) if s]
a1,d1,k1 = fit(sub,nu_fw,0.5,(0.0,))
a2,d2,k2 = fit(sub,nu_fw,0.5,FG)
print(f"V5: framework nu, GAS-DOM, U=0.5: f=0 -> a0_hat={a1:.3e} Dchi2(fw)={d1:.1f}; "
      f"f profiled -> a0_hat={a2:.3e} Dchi2(fw)={d2:.1f} Dchi2(fork)={k2:.1f} (direction: optimum BELOW 9.36e-11)")
assert a2<A0FW
print("ALL INDEPENDENT CHECKS PASS")
