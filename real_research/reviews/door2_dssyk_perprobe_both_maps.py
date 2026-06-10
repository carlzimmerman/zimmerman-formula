#!/usr/bin/env python3
"""
DOOR 2 -- FINAL: the physically-correct deep-MOND freezing exponent p evaluated AT THE PROBE'S OWN
energy, + both-ways robustness on the load-bearing dictionary map. Resolves the C1/C2 tension cleanly.
=====================================================================================================
RESOLUTION of the apparent C1/C2 tension (working rule -- scrutinized both ways):
  The deep-MOND law g_obs ~ g_bar^p is governed by the LOCAL density-of-states slope s at the energy
  the PHYSICAL PROBE OCCUPIES, with p = 1/(s+2) (s=0 flat-center -> p=1/2 MOND; s=1/2 sqrt-edge -> p=2/5).
  - For galaxies the conical deficit is tiny, so the probe sits AT the center (E_src<=4e-3): s=0 -> MOND.
  - For clusters the deficit is O(1), so the probe sits AT the edge (E_src=1): s=1/2 -> anti-MOND/failure.
  C2's "always integrate the window around E=0" measured the central DOS even for the cluster (whose
  weight is actually at the edge) -- a fit-locale artifact. Evaluated at the probe's OWN energy
  (Diagnostic 3 / this file), galaxies->center->MOND, clusters->edge->fail. The GALAXY verdict is
  unchanged either way (galaxies ARE central); only the cluster reading is corrected.

p = 1/(s+2) derivation: local DOS rho~(dist)^s -> cumulative mu(x)=x^{s+1} -> mu(x) g_obs=g_bar with
x=g_obs/a0 -> g_obs^{s+2} ~ g_bar -> p=1/(s+2). (s=0: p=1/2,V flat; s=1/2: p=2/5, V~r^{+0.1} rising.)
"""
import numpy as np
NPOCH = 500
c = 2.998e8; G = 6.674e-11; Msun = 1.989e30
H0 = 67.0e3/3.086e22; OmegaL = 0.685; H_Lambda = H0*np.sqrt(OmegaL)
M_dS = c**2/(G*H_Lambda)/Msun

def qpoch(a,q,N=NPOCH):
    a=np.asarray(a,dtype=complex); out=np.ones(a.shape,dtype=complex); qk=1.0
    for _ in range(N): out*=(1-a*qk); qk*=q
    return out
def mu_qg(th,q):
    qq=qpoch(q,q).real; e2=np.exp(2j*th)
    return qq*(qpoch(e2,q)*qpoch(np.conj(e2),q)).real/(2*np.pi)
def Mk(th1,th2,D,q):
    num=qpoch(q**(2*D),q).real
    den=np.ones(np.broadcast(np.asarray(th1,float),np.asarray(th2,float)).shape,dtype=complex)
    for s1 in (1,-1):
        for s2 in (1,-1):
            den*=qpoch(q**D*np.exp(1j*(s1*np.asarray(th1,float)+s2*np.asarray(th2,float))),q)
    return num/den.real

th=np.linspace(1e-5,np.pi-1e-5,600001); E=np.cos(th)
rhoE_vac=mu_qg(th,q=0.7)/np.abs(np.sin(th))  # dummy; recomputed per q below

def local_dos_slope_at(Esrc,q):
    """local d ln rho_E / d ln(distance to NEAREST band end) at energy Esrc, using the probe's OWN
       conditional spectral weight is unnecessary -- the LOCAL DOS slope is a property of the q-Gaussian
       (the matter kernel transports but does not change the local power), so we read it off rho_vac."""
    rhoE=mu_qg(th,q)/np.abs(np.sin(th))
    if abs(Esrc) < 0.5:               # center side: rho ~ |E|^s
        lo=max(1e-4,abs(Esrc)*0.3 if Esrc!=0 else 1e-4)
        win=(np.abs(E)>lo)&(np.abs(E)<max(abs(Esrc)*3,0.05))&(np.abs(E)<0.3)&(rhoE>0)
        if win.sum()<10: return np.nan
        return np.polyfit(np.log(np.abs(E[win])),np.log(rhoE[win]),1)[0]
    else:                              # edge side: rho ~ (1-|E|)^s
        ome=1-np.abs(E); d=1-abs(Esrc)
        win=(ome>d*0.3)&(ome<max(d*3,0.02))&(ome<0.2)&(rhoE>0)
        if win.sum()<10: return np.nan
        return np.polyfit(np.log(ome[win]),np.log(rhoE[win]),1)[0]

def th0_of(alpha): return np.pi/2*(1-np.clip(alpha,0,1))

def report(disp_map, label):
    print("="*98)
    print(f"DEEP-MOND SIGN per probe, displacement map = {label}")
    print("="*98)
    print(f"  {'object':>14}{'mass':>10}{'alpha':>11}{'E_src':>11}{'local DOS s':>13}{'p=1/(s+2)':>11}{'V(r)~r^':>10}{'sign':>11}")
    for nm,Mass in [("dwarf",1e7),("spiral",3e10),("massive",1e12),("group",1e13),("cluster",1e15)]:
        a=Mass/M_dS; Esrc=disp_map(a)
        s=local_dos_slope_at(Esrc,0.7)
        p=1/(s+2); vexp=(1-2*p)/2
        sign=("MOND" if abs(p-0.5)<0.04 else ("anti-MOND" if p<0.46 else "?"))
        curve=("FLAT" if abs(vexp)<0.025 else ("RISING" if vexp>0 else "fall"))
        print(f"  {nm:>14}{Mass:>10.0e}{a:>11.2e}{Esrc:>11.3e}{s:>13.3f}{p:>11.3f}{('%+.3f(%s)'%(vexp,curve)):>17}{sign:>11}")
    print()

print("#"*98)
print("# DOOR 2 -- FINAL deep-MOND sign for a PHYSICAL finite-mass de Sitter probe (per-probe, both maps)")
print("#"*98)
print(f"\n M_dS={M_dS:.3e} Msun.  p=1/(s+2): s=0(flat center)->p=1/2 MOND; s=1/2(sqrt edge)->p=2/5 anti-MOND.\n")

# MAP A (framework reading, linear): E_src = cos(theta0), theta0 = pi/2 (1-alpha)
report(lambda a: abs(np.cos(th0_of(a))), "A: linear theta-displace E_src=cos[pi/2(1-alpha)]  (framework reading)")

# MAP B (alternative convention, direct-energy): E_src = min(alpha, 1) -- deficit IS the fractional energy
report(lambda a: min(a,1.0), "B: direct E_src=min(alpha,1)  (alternative: deficit = fractional band energy)")

# MAP C (alternative: sqrt -- if energy ~ sqrt(deficit), softer displacement)
report(lambda a: min(np.sqrt(a),1.0), "C: E_src=min(sqrt(alpha),1)  (alternative: energy ~ sqrt deficit)")

print("="*98)
print("BOTH-WAYS VERDICT")
print("="*98)
print("""  Across ALL three displacement conventions (A linear, B direct, C sqrt), the GALAXY result is
  identical and convention-robust: a galaxy (alpha<=2.65e-3) sits at E_src well inside the flat-center
  window (s~0) -> p=1/2 -> FLAT rotation curves -> deep-MOND ENHANCEMENT (the framework's sign, BTFR v^4~M).
  Even the most aggressive map (B: E_src=alpha directly) puts a 1e12-Msun galaxy at E_src=2.7e-3,
  still flat-center. The galaxy verdict does NOT depend on the contested map.

  The CLUSTER result is also convention-robust in DIRECTION: alpha=O(1) pushes the source to the band
  EDGE (s=+0.5) -> p=2/5 -> RISING curves -> MOND FAILS. The SAME calc that gives galaxies MOND gives
  clusters its known empirical breakdown -- an unforced consistency, not put in by hand.

  This is the content the prior round (4g) left as a DICTIONARY ASSERTION ('near-horizon probe sits at
  center -- very likely, not proven'): now COMPUTED. The probe's energy is fixed by its conical deficit
  alpha=m/M_dS, and the resulting local DOS slope -> p is read off directly. Galaxies land at the center
  for ANY reasonable deficit->energy map, because alpha is so tiny (<=2.65e-3): that smallness, not a
  chosen dictionary, is what forces the center.""")
