#!/usr/bin/env python3
r"""
ROUTE A -- THE CIRCULARITY CHECK (the load-bearing honesty test).
=================================================================
The first pass keyed the boost on the cluster's TOTAL |Phi| (NFW including the residual
mass we are trying to EXPLAIN). That is potentially CIRCULAR: a modified-inertia / modified-
gravity law can only respond to the BARYONIC source (g_bar), because the residual mass does
not exist as a source -- it IS the thing the boost must manufacture. So the fair, non-circular
footing keys the boost on the BARYONIC potential depth |Phi_bar|/c^2 (from g_bar only).

  => Recompute the cluster-core |Phi_bar|/c^2 from BARYONS ONLY (gas+stars), and the
     galaxy |Phi_bar|/c^2 from baryons only, and re-measure the CONTRAST and whether a
     |Phi_bar|-keyed law still closes the core without breaking galaxies.

This is the make-or-break: if the contrast SURVIVES on baryonic Phi, Route A is a genuine
candidate; if it COLLAPSES (because cluster baryonic Phi ~ galaxy baryonic Phi), the first
pass was a circular mirage and Route A fails G1/G3 honestly.

Also: the deep-MOND self-consistency -- in deep MOND the TRUE potential is the MONDian
(boosted) one, |Phi| ~ v_flat^2 ln(r) which is LARGER than baryonic. Which Phi does the
"inertia" see? Both ways.
"""
import numpy as np, glob, os
from scipy.integrate import quad
G=6.674e-11; c=2.998e8; Msun=1.989e30; kpc=3.0857e19
Msun_g=1.989e33; kpc_cm=3.0857e21; a0=9.36e-11
HERE=os.path.dirname(__file__)
SPARC=os.path.join(HERE,"..","..","..","real_research","data","sparc_data")

print("="*94)
print(" ROUTE A -- CIRCULARITY CHECK: key on BARYONIC |Phi|/c^2, not total (honest footing)")
print("="*94)

# ---------- A2029 BARYONIC potential depth (gas+stars only) ----------
rho_gc=6.6e-26;beta_g=0.54;alpha_g=0.55;rc_gas=77.6
def rho_gas(r):
    x=np.asarray(r)/rc_gas
    return rho_gc*2.0**(1.5*beta_g-0.5*alpha_g)*x**(-alpha_g)*(1+x**2)**(-1.5*beta_g+0.5*alpha_g)
def Mgas(r_kpc):
    def one(rr):
        v,_=quad(lambda rp:4*np.pi*(rp*kpc_cm)**2*rho_gas(rp)*kpc_cm,1e-3,rr,limit=200);return v/Msun_g
    return np.array([one(r) for r in np.atleast_1d(r_kpc)])
_sr=np.array([50.,100.,200.,500.]);_sp=np.array([1.2e12,3.0e12,3.4e12,3.8e12])
def Mstar(r):
    out=np.exp(np.interp(np.log(np.atleast_1d(r)),np.log(_sr),np.log(_sp),left=np.log(_sp[0]),right=np.log(_sp[-1])))
    out=np.where(np.atleast_1d(r)<50.,_sp[0]*(np.atleast_1d(r)/50.)**1.5,out);return out
def Mbar_A2029(r): return Mgas(r)+Mstar(r)
# baryonic potential depth from M_bar(<r): |Phi_bar(r)|/c^2 = [G M_bar(<r)/r + int_r^inf G M_bar/r'^2 dr']/c^2
def phi_bar_depth(M_of_r,r_kpc,r_out=3000.):
    inner=G*(M_of_r(r_kpc)[0] if np.ndim(M_of_r(r_kpc))>0 else M_of_r(r_kpc))*Msun/(r_kpc*kpc)
    def integ(rp):
        m=M_of_r(rp); m=m[0] if np.ndim(m)>0 else m
        return G*m*Msun/((rp*kpc)**2)*kpc
    outer,_=quad(integ,r_kpc,r_out,limit=200)
    return (inner+outer)/c**2

R=np.array([20.,50.,100.,200.,300.,500.])
phi_bar=np.array([phi_bar_depth(Mbar_A2029,r) for r in R])
# total (NFW) for comparison
def nfw_M(r,M200,cn,r200): rs=r200/cn; m=lambda x:np.log(1+x)-x/(1+x); return M200*m(np.asarray(r)/rs)/m(cn)
A2029_tot=lambda r: nfw_M(r,8.47e14,4.0,1910.0)
def phi_tot_depth(r_kpc,r_out=5000.):
    inner=G*A2029_tot(r_kpc)*Msun/(r_kpc*kpc)
    outer,_=quad(lambda rp:G*A2029_tot(rp)*Msun/((rp*kpc)**2)*kpc,r_kpc,r_out,limit=200)
    return (inner+outer)/c**2
phi_tot=np.array([phi_tot_depth(r) for r in R])
print("\n[A] A2029 baryonic vs total potential depth:")
print(f"    {'r(kpc)':>7} {'|Phi_bar|/c^2':>14} {'|Phi_tot|/c^2':>14} {'ratio bar/tot':>14}")
for i,r in enumerate(R):
    print(f"    {r:7.0f} {phi_bar[i]:14.3e} {phi_tot[i]:14.3e} {phi_bar[i]/phi_tot[i]:14.3f}")
print(f"    -> baryonic depth is ~{np.mean(phi_bar/phi_tot):.2f}x the total (gas+stars are ~13% of mass,")
print(f"       but the gas is extended so |Phi_bar| is a sizeable fraction of |Phi_tot|).")

# ---------- SPARC baryonic potential depth (already baryonic) ----------
def load_sparc():
    out=[]
    for f in sorted(glob.glob(os.path.join(SPARC,"*_rotmod.dat"))):
        try: dat=np.loadtxt(f,comments="#")
        except Exception: continue
        if dat.ndim!=2 or dat.shape[1]<7: continue
        Rk=dat[:,0];Vobs=dat[:,1];Vgas=dat[:,3];Vdisk=dat[:,4];Vbul=dat[:,5]
        Ups=0.70
        Vbar2=Vgas*np.abs(Vgas)+Ups*Vdisk*np.abs(Vdisk)+1.4*Ups*Vbul*np.abs(Vbul)
        Vbar2=np.clip(Vbar2,0,None)
        Rm=Rk*kpc; gbar=Vbar2*1e6/Rm; gobs=(Vobs*1e3)**2/Rm
        m=(Rk>0)&(gbar>0)&(gobs>0)&np.isfinite(gbar)&np.isfinite(gobs)
        if m.sum()<3: continue
        Rs=Rm[m];gb=gbar[m];o=np.argsort(Rs);Rs=Rs[o];gb=gb[o]
        phi=np.zeros_like(Rs)
        for k in range(len(Rs)):
            seg=sum(0.5*(gb[j]+gb[j+1])*(Rs[j+1]-Rs[j]) for j in range(k,len(Rs)-1))
            Vb2=gb[-1]*Rs[-1]; tail=Vb2*np.log(10.0)
            phi[k]=(seg+tail)/c**2
        out.append((gb,gobs[m][o],phi))
    return out
rows=load_sparc()
phi_sparc=np.concatenate([r[2] for r in rows])
gbar_s=np.concatenate([r[0] for r in rows]); gobs_s=np.concatenate([r[1] for r in rows])
print(f"\n[B] SPARC baryonic |Phi_bar|/c^2: median={np.median(phi_sparc):.2e} max={phi_sparc.max():.2e}")
print(f"    cluster-core baryonic |Phi_bar|/c^2 (A2029 @200 kpc) = {phi_bar[3]:.2e}")
contrast_bar=phi_bar[3]/phi_sparc.max()
print(f"    *** BARYONIC core/deepest-disk CONTRAST = {contrast_bar:.2f}x ***")
print(f"        (was {7.69e-5/4.81e-6:.1f}x on TOTAL Phi -- did keying on baryons collapse it?)")

# ---------- does a |Phi_bar|-keyed law still close the core AND pass SPARC? ----------
def M_mond_b(Mbar_M,r,a0eff):
    rm=r*kpc;Mb=Mbar_M*Msun;gb=G*Mb/rm**2
    return np.sqrt(gb**2+gb*a0eff)*rm**2/G/Msun
Mbar=np.array([Mbar_A2029(r)[0] if np.ndim(Mbar_A2029(r))>0 else Mbar_A2029(r) for r in R])
tot=A2029_tot(R)
from scipy.optimize import brentq
def cover(amp,p):
    a0e=a0*(1+amp*phi_bar**p)
    return M_mond_b(Mbar,R,a0e)/tot
print("\n[C] |Phi_bar|-keyed law: tune amp at 200 kpc, read full-profile coverage + SPARC veto:")
def nu(g,a0_): return np.sqrt(g**2+g*a0_)
def rar(a0e_s):
    res=np.log10(gobs_s)-np.log10(nu(gbar_s,a0e_s))
    return 1.4826*np.median(np.abs(res-np.median(res)))
floor=rar(a0*np.ones_like(gbar_s))
print(f"    SPARC RAR floor: {floor:.4f} dex")
print(f"    {'p':>3} {'amp':>12} {'cov@20':>8} {'cov@200':>8} {'cov@500':>8} {'medSPARCboost':>14} {'maxSPARCboost':>14} {'RAR dex':>9} {'G2':>6}")
for p in [1,2,3]:
    f=lambda amp: cover(amp,p)[3]-1.0
    try: amp=brentq(f,1e1,1e30)
    except Exception: amp=np.nan
    cov=cover(amp,p)
    a0e_s=a0*(1+amp*phi_sparc**p)
    sc=rar(a0e_s)
    g2="PASS" if sc<floor+0.02 else "BREAK"
    print(f"    {p:>3} {amp:12.3e} {cov[0]*100:6.1f}% {cov[3]*100:6.1f}% {cov[5]*100:6.1f}% "
          f"{np.median(a0e_s/a0):14.3f} {np.max(a0e_s/a0):14.3f} {sc:9.4f} {g2:>6}")

print("\n"+"="*94)
print(" CIRCULARITY VERDICT")
print("="*94)
print(f"  baryonic core/deepest-disk |Phi| contrast = {contrast_bar:.2f}x (vs {7.69e-5/4.81e-6:.1f}x on total Phi)")
print(f"  If the contrast SURVIVES on baryonic Phi and the law still closes+passes -> Route A is real.")
print(f"  If it COLLAPSES (cluster baryonic Phi ~ galaxy) -> the first pass was circular, G1/G3 fail.")
