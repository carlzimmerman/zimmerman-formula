#!/usr/bin/env python3
"""
INDEPENDENT HOSTILE REGRADE of the dS-Unruh horizon density-a0 (ell_desitter_unruh_horizon).
============================================================================================
Built from scratch (own SPARC loader, own eRASS1 path, own eta + RAR) to verify the verdict:
  - ell = r_AH = c/H_local genuinely DERIVED (the local apparent-horizon radius)?
  - galaxy RAR scatter under density-a0 stays ~0.13-0.15 dex (does NOT inflate)?
  - cluster eta under the self-consistent horizon density-a0?
  - is the cluster-profile/turnaround choice driving the result, or is it robust?
  - does any 1-2 Mpc ell OVER-close (eta<1)? what ell actually hits 1.2-1.5?
Quarantine: a0/Z are POSITED, never asserted derived. ell tested for derived-vs-tuned.
"""
import os, glob, math
import numpy as np

# ---- SI constants (independent) ----
c    = 2.99792458e8
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.0856775814913673e19
Mpc  = 3.0856775814913673e22
H0   = 67.4e3/Mpc
rho_crit = 3*H0**2/(8*np.pi*G)
Omega_L  = 0.685
rho_DE   = Omega_L*rho_crit
a0_of    = lambda rho: 0.5*c*np.sqrt(G*rho)
A0_DE    = a0_of(rho_DE)
A0_CRIT  = a0_of(rho_crit)

print("="*88)
print("INDEPENDENT REGRADE -- dS-Unruh horizon density-a0")
print("="*88)
print(f"rho_crit={rho_crit:.3e}  rho_DE={rho_DE:.3e}  kg/m^3")
print(f"a0(rho_DE)   = {A0_DE:.4e}  (framework anchor 9.36e-11, POSITED)")
print(f"a0(rho_crit) = {A0_CRIT:.4e}  (rho_total cosmic footing 1.13e-10)")

# =========================================================================
# CHECK A -- is ell=c/H_local genuinely the apparent-horizon radius? (algebra)
# In FRW the apparent horizon is r_AH = c / sqrt(H^2 + k c^2/a^2). Flat (k=0):
#   r_AH = c/H. With H^2 = (8 pi G/3) rho (Friedmann), r_AH = c/sqrt((8piG/3)rho).
# Also a0 = (c/2) sqrt(G rho) = (c/2) sqrt(3/(8pi)) * sqrt((8piG/3)rho) = (c/2)*sqrt(3/8pi)*H.
# So a0 = 0.5*sqrt(3/(8pi)) * c H = 0.1727 c H  -> a0 ~ c H up to an O(1) factor. CONFIRM both.
# =========================================================================
def r_AH(rho):
    H = np.sqrt((8*np.pi*G/3.0)*rho)
    return c/H
# verify a0 = (c/2)sqrt(3/8pi) * H_local identity
for rho in (rho_DE, rho_crit, 500*rho_crit):
    H = np.sqrt((8*np.pi*G/3.0)*rho)
    a0_direct = 0.5*c*np.sqrt(G*rho)
    a0_viaH   = 0.5*np.sqrt(3.0/(8*np.pi))*c*H
    print(f"  CHECK A: rho={rho:.2e}  a0=(c/2)sqrt(Grho)={a0_direct:.4e}  "
          f"(c/2)sqrt(3/8pi)cH={a0_viaH:.4e}  ratio={a0_direct/a0_viaH:.6f}  r_AH={r_AH(rho)/Mpc:.2f} Mpc")
print("  -> ell=c/H_local IS the flat-FRW apparent horizon (k=0); a0=0.1727 cH_local exactly. DERIVED scale.")

# =========================================================================
# CHECK B -- the DERIVED ell numerics: how big at each density?
# =========================================================================
print("\nCHECK B -- derived ell=r_AH at representative densities:")
for nm, rho in [("rho_DE floor", rho_DE), ("rho_crit", rho_crit),
                ("200 rho_crit (virial)", 200*rho_crit), ("500 rho_crit (R500)", 500*rho_crit),
                ("galaxy disk 1e-21", 1e-21), ("2e7 rho_crit", 2e7*rho_crit)]:
    print(f"    {nm:24}: ell=r_AH={r_AH(rho)/Mpc:11.4g} Mpc  a0={a0_of(rho):.3e} ({a0_of(rho)/A0_DE:.2f}x)")

# =========================================================================
# CHECK C -- GALAXY RAR (own loader). a0_eff per point from self-consistent horizon smoothing.
# =========================================================================
HERE  = os.path.dirname(os.path.abspath(__file__))
SPARC = os.path.join(HERE, "..", "..", "real_research", "data", "sparc_data")

def load_sparc(ml=0.70):
    gals=[]
    for path in sorted(glob.glob(os.path.join(SPARC, "*_rotmod.dat"))):
        rows=[]
        for line in open(path):
            s=line.strip()
            if not s or s.startswith("#"): continue
            p=s.split()
            if len(p)<6: continue
            try: r,vo,ev,vg,vd,vb=(float(p[i]) for i in range(6))
            except ValueError: continue
            rows.append((r,vo,ev,vg,vd,vb))
        if not rows: continue
        a=np.array(rows)
        R=a[:,0]*kpc; Vo=a[:,1]*1e3; eV=a[:,2]; Vg=a[:,3]*1e3; Vd=a[:,4]*1e3; Vb=a[:,5]*1e3
        Vbar2=Vg*np.abs(Vg)+ml*Vd*np.abs(Vd)+ml*Vb*np.abs(Vb)
        gbar=Vbar2/R; gobs=Vo**2/R
        Menc=np.maximum(Vbar2,0.0)*R/G
        gals.append(dict(R=R,gbar=gbar,gobs=gobs,Menc=Menc,everr=a[:,2],vobs=a[:,1]))
    return gals

def gal_Menc(gal):
    R,Menc=gal["R"],gal["Menc"]; Mtot=Menc[-1]
    def f(r):
        if r<=0: return 0.0
        if r<=R[0]: return Menc[0]*(r/R[0])**3
        if r>=R[-1]: return Mtot
        return float(np.interp(r,R,Menc))
    return f

def sc_a0(Menc_f, r_probe, n=300):
    """self-consistent: ell=r_AH(rho_t), rho_t=rho_DE + Menc(max(ell,r_probe))/vol."""
    rho_t=rho_DE
    for _ in range(n):
        ell=r_AH(rho_t); R=max(ell,r_probe)
        rho_m=Menc_f(R)/((4/3)*np.pi*R**3)
        rn=rho_DE+rho_m
        if abs(rn-rho_t)<=1e-9*rho_t: rho_t=rn; break
        rho_t=rn
    return a0_of(rho_t), r_AH(rho_t), rho_t

def rar_scatter(gb, go, a0_arr):
    x=np.sqrt(gb/a0_arr)
    pred=np.log10(gb/(1-np.exp(-x)))
    return float(np.sqrt(np.mean((np.log10(go)-pred)**2)))

print("\nCHECK C -- GALAXY RAR (own loader, real 175 SPARC):")
for ML in (0.70, 0.50):
    gals=load_sparc(ML)
    gb,go,a0d=[],[],[]
    for gal in gals:
        Mf=gal_Menc(gal)
        for i in range(len(gal["R"])):
            r,vo,ev=gal["R"][i],gal["vobs"][i],gal["everr"][i]
            if r<=0 or vo<=0 or ev<=0 or ev/vo>0.10: continue
            if gal["gbar"][i]<=0 or gal["gobs"][i]<=0: continue
            ae,_,_=sc_a0(Mf,r)
            gb.append(gal["gbar"][i]); go.append(gal["gobs"][i]); a0d.append(ae)
    gb,go,a0d=np.array(gb),np.array(go),np.array(a0d)
    s_DE  = rar_scatter(gb,go,np.full_like(gb,A0_DE))
    s_den = rar_scatter(gb,go,a0d)
    print(f"  Ups={ML}: N={len(gb)} pts | const a0(rho_DE) scatter={s_DE:.4f} dex | "
          f"density-a0 scatter={s_den:.4f} dex | inflation={s_den-s_DE:+.4f} | "
          f"a0_eff/a0_DE=[{a0d.min()/A0_DE:.4f},{a0d.max()/A0_DE:.4f}]")

# =========================================================================
# CHECK D -- CLUSTERS (own eRASS1 load) self-consistent horizon density-a0 + sensitivity to profile.
# =========================================================================
import sys
sys.path.insert(0, os.path.join(HERE, "..", "..", "real_research", "data"))
from _load_erass1 import load_clean
d=load_clean()
gbar=d["gbar"]; gobs=d["gobs"]; M500=d["M500"]*1e13*Msun; R500=d["R500"]*kpc; N=d["N"]
nu=lambda y:0.5*(1+np.sqrt(1+4/y))
def eta_const(a0v): return gobs/(nu(gbar/a0v)*gbar)

print(f"\nCHECK D -- CLUSTERS real eRASS1 N={N}, median z={np.median(d['z']):.3f}, "
      f"median M500={np.median(d['M500'])*1e13:.2e}, median R500={np.median(d['R500']):.0f} kpc")
print(f"  baseline eta: a0(rho_DE)={np.median(eta_const(A0_DE)):.3f}  a0=1.2e-10={np.median(eta_const(1.2e-10)):.3f}")

def cl_Menc(M500_kg, R500_m, r_ta_factor=5.0, rho_bg=rho_crit):
    r_ta=r_ta_factor*R500_m; M_ta=M500_kg*(r_ta/R500_m)
    def f(r):
        if r<=r_ta: return M500_kg*(r/R500_m)
        return M_ta+rho_bg*(4/3)*np.pi*(r**3-r_ta**3)
    return f

# self-consistent horizon eta, AND sensitivity to turnaround factor (does the choice drive it?)
for taf in (3.0, 5.0, 10.0):
    a0c=[]
    for i in range(N):
        Mf=cl_Menc(M500[i],R500[i],r_ta_factor=taf)
        ae,_,_=sc_a0(Mf,R500[i])
        a0c.append(ae)
    a0c=np.array(a0c)
    eta=gobs/(nu(gbar/a0c)*gbar)
    print(f"  self-consistent horizon (turnaround={taf:g}xR500): ell_median={np.median([r_AH(0)*0]) if False else '':}"
          f"eta={np.median(eta):.3f} [IQR {np.percentile(eta,25):.2f}-{np.percentile(eta,75):.2f}] "
          f"a0boost_med={np.median(a0c)/A0_DE:.3f}x over-closed={100*(eta<1).mean():.1f}%")

# =========================================================================
# CHECK E -- the fixed-ell scan (which ell threads both?) -- own implementation
# =========================================================================
print("\nCHECK E -- FIXED-ell scan (tuned): cluster eta + galaxy RAR scatter")
gals70=load_sparc(0.70)
# precompute galaxy RAR cloud once
gcloud=[]
for gal in gals70:
    Mtot=gal["Menc"][-1]
    for i in range(len(gal["R"])):
        r,vo,ev=gal["R"][i],gal["vobs"][i],gal["everr"][i]
        if r<=0 or vo<=0 or ev<=0 or ev/vo>0.10: continue
        if gal["gbar"][i]<=0 or gal["gobs"][i]<=0: continue
        gcloud.append((gal["gbar"][i],gal["gobs"][i],Mtot))
gcloud=np.array(gcloud)
for ellMpc in (1.0,1.5,2.0,3.0,6.0,8.0,10.0):
    ell=ellMpc*Mpc
    # cluster
    a0cl=[]
    for i in range(N):
        Mf=cl_Menc(M500[i],R500[i])
        R=max(ell,R500[i]); rho_m=Mf(R)/((4/3)*np.pi*R**3)
        a0cl.append(a0_of(rho_DE+rho_m))
    a0cl=np.array(a0cl); eta=gobs/(nu(gbar/a0cl)*gbar)
    # galaxy
    rho_g=gcloud[:,2]/((4/3)*np.pi*ell**3)
    a0g=a0_of(rho_DE+rho_g)
    s=rar_scatter(gcloud[:,0],gcloud[:,1],a0g)
    print(f"  ell={ellMpc:5.1f} Mpc: cluster eta={np.median(eta):.3f} (over-closed {100*(eta<1).mean():4.0f}%) | "
          f"galaxy RAR={s:.4f} dex (gal a0 boost x{np.median(a0g)/A0_DE:.3f})")

print("\n" + "="*88)
print("DONE -- compare to verdict's 0.1471/0.1537 dex, eta 1.75, and the 6-10 Mpc tuned window.")
print("="*88)
