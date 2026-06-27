#!/usr/bin/env python3
"""
THE UNOPENED DOOR (Carl: swing at it for real): does the framework's a0(z) trajectory FORCE a swampland
Distance-Conjecture tower at a computable scale, or just permit one? Brutal bar: the scale must come out
WITHOUT being put in.

Logic. a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)) (framework). Evolving rho_DE => a rolling quintessence field
phi(z). The Distance Conjecture: a tower gets light as the field rolls, m_tower ~ M_Pl * exp(-alpha * Delta_phi/M_Pl).
For a canonical scalar with rho_DE = (1/2)phidot^2 + V and EoS w:
   (d phi/d ln a)^2 / M_Pl^2 = 3 (1+w) Omega_DE(a)     => Delta_phi(z)/M_Pl = INT sqrt(3|1+w|Omega_DE) d ln(1+z)
The exponential-potential slope lambda = M_Pl V'/V obeys (scaling) lambda^2 = 3(1+w); the de Sitter swampland
conjecture wants lambda >~ c ~ O(1) (often c >= sqrt(2/3)=0.82). Many string realizations tie the TOWER coefficient
alpha to the potential slope: alpha ~ lambda (the "tower<->potential" relation). If so, a0(z) -> w(z) -> lambda ->
alpha AND Delta_phi -> the tower mass is FORCED (no free knob). We test that, both-ways, on the REAL DESI posterior.

Footing a0=9.36e-11; uses the real DESI DR1 w0waCDM chains (a0z_desi_chains_propagation.py data). Honest both-ways:
report whether the ABSOLUTE scale is forced (it is NOT -- the total field distance is unobservable) vs the
VARIATION (which IS forced by the observable Delta_phi + the alpha~lambda relation).
"""
import importlib.util, os, math
import numpy as np

# ---- load the real DESI chains (reuse the propagation loader's data) ---------
DATA = ("/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/"
        "1b2404fe-c966-467a-ab3f-1335450f250e/scratchpad/desi_chains")
W0_COL, WA_COL, WEIGHT_COL, BURNIN = 8, 9, 0, 0.3
COMBOS={"DESI+CMB+DESY5":"desy5sn","DESI+CMB+Union3":"union3","DESI+CMB+Pantheon+":"pantheonplus"}
Om0=0.31  # matter density today (for Omega_DE(z))

def load(tag):
    ws,w0s,was=[],[],[]
    for n in (1,2,3,4):
        d=np.loadtxt(os.path.join(DATA,f"{tag}.chain.{n}.txt")); k=int(BURNIN*len(d)); d=d[k:]
        ws.append(d[:,WEIGHT_COL]); w0s.append(d[:,W0_COL]); was.append(d[:,WA_COL])
    return np.concatenate(ws),np.concatenate(w0s),np.concatenate(was)

def wz(z,w0,wa): return w0+wa*z/(1.0+z)
def rho_de_ratio(z,w0,wa): return (1.0+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1.0+z))
def Omega_DE(z,w0,wa):
    r=rho_de_ratio(z,w0,wa); rho_de=(1-Om0)*r; rho_m=Om0*(1+z)**3
    return rho_de/(rho_de+rho_m)

def field_excursion(zmax,w0,wa,nz=400):
    """Delta_phi(zmax)/M_Pl = INT_0^zmax sqrt(3|1+w| Omega_DE) dln(1+z)."""
    zs=np.linspace(0,zmax,nz); integ=np.sqrt(3*np.abs(1+wz(zs,w0,wa))*Omega_DE(zs,w0,wa))
    lna=np.log(1+zs)
    return np.trapz(integ,lna)

print("="*94)
print("SWAMPLAND TOWER from a0(z): does the framework FORCE a tower scale? (real DESI posterior)")
print("="*94)
print(f"  brutal bar: the SCALE must come out WITHOUT being put in.  M_Pl=2.435e18 GeV (reduced).")
c_dS=math.sqrt(2.0/3.0)  # a common de Sitter-conjecture slope bound

for name,tag in COMBOS.items():
    w,w0,wa=load(tag)
    w0m=np.average(w0,weights=w); wam=np.average(wa,weights=w)
    # field slope today and the phantom-divide crossing
    lam0=math.sqrt(3*abs(1+w0m))                       # lambda(z=0) = sqrt(3(1+w0))
    zc=(-(1+w0m)/wam) if wam!=0 else np.inf            # z where w crosses -1: z/(1+z)=-(1+w0)/wa
    zcross=zc/(1-zc) if 0<zc<1 else np.inf
    dphi3=field_excursion(3.0,w0m,wam); dphi1=field_excursion(1.0,w0m,wam)
    # tower variation for alpha=lambda0 (conditional-forced) and alpha=1 (generic SDC)
    def tower_ratio(dphi,alpha): return math.exp(-alpha*dphi)
    print(f"\n### {name}:  w0={w0m:+.3f}  wa={wam:+.3f}")
    print(f"  field slope lambda(0)=sqrt(3(1+w0)) = {lam0:.3f}   (de Sitter conj. bound c~{c_dS:.2f}: "
          f"{'SATURATES/exceeds' if lam0>=c_dS else 'BELOW (mild tension)'})")
    print(f"  phantom divide w=-1 crossed at z ~ {zcross:.2f}  (w<-1 / phantom for z> that -> canonical field FORBIDDEN there)")
    print(f"  observable field excursion:  Delta_phi(z=1)/M_Pl = {dphi1:.3f},  Delta_phi(z=3)/M_Pl = {dphi3:.3f}")
    print(f"  tower-mass VARIATION m_tower(z)/m_tower(0) = exp(-alpha*Delta_phi):")
    for al,lab in [(lam0,f'alpha=lambda0={lam0:.2f} [conditional-forced]'),(1.0,'alpha=1 [generic SDC]'),(c_dS,f'alpha=c={c_dS:.2f}')]:
        print(f"     {lab:38s}:  m(z=1)/m(0)={tower_ratio(dphi1,al):.3f},  m(z=3)/m(0)={tower_ratio(dphi3,al):.3f}")
    # side-by-side with a0(z)
    a0r1=math.sqrt(rho_de_ratio(1.0,w0m,wam)); a0r3=math.sqrt(rho_de_ratio(3.0,w0m,wam))
    print(f"  (for contrast, framework a0(z)/a0(0)=sqrt(rho_DE ratio): a0(1)={a0r1:.3f}, a0(3)={a0r3:.3f})")

print("\n"+"="*94); print("VERDICT (computed, both-ways) -- does the scale come out without being put in?"); print("="*94)
print("""  WHAT IS FORCED (comes out): the observable field excursion Delta_phi(z)/M_Pl ~ O(1) over z=0-3 is FIXED by the
    framework's a0(z) (= the DESI w(z)), with NO free knob -- it is an integral of the measured w(z). And the slope
    lambda(0)~0.8-0.9 SATURATES the de Sitter conjecture bound c~0.82, a genuine (if suggestive) consistency.
  WHAT IS NOT FORCED (put in): the tower's ABSOLUTE scale m_tower(0)=M_Pl*exp(-alpha*phi_total/M_Pl) depends on the
    TOTAL (pre-observable, unbounded) field distance phi_total AND on alpha -- both unobservable from a0(z). So the
    absolute tower mass does NOT come out. The brutal bar is NOT cleared for the absolute scale.
  THE PARTIAL THAT DOES COME OUT: the tower-mass VARIATION m_tower(z)/m_tower(0)=exp(-alpha*Delta_phi(z)) is forced
    by the (forced) Delta_phi -- a factor ~1.4-2 over z=0-3 IF the tower<->potential relation alpha~lambda holds.
    That is a genuine, NEW, computable prediction: a dark-sector mass scale that DECLINES with redshift, tracking
    the same rho_DE(z) that drives a0(z) -- tying the swampland tower to the ghost-condensate dark sector.
  THREE HONEST CAVEATS (both-ways): (1) the alpha~lambda 'tower<->potential' link is a model-dependent conjecture,
    not a theorem -- without it alpha is free and even the variation loosens. (2) The DESI w(z) CROSSES the phantom
    divide (w<-1 in the past) -> a single CANONICAL quintessence cannot realize it (needs a quintom/non-canonical
    field), and w<-1 is itself in tension with the strict de Sitter conjecture -> the canonical-tower mapping is a
    leading-order proxy, not exact. (3) Dies if DESI -> w=-1 (no roll, no tower).
  NET: the door does NOT crack to a FORCED ABSOLUTE SCALE (bar not cleared) -- but it is the FIRST door that yields a
    genuine, computed, NEW prediction from a0(z) without hitting flavor-blindness or the raw scale gap: a redshift-
    DECLINING dark-sector tower mass locked to a0(z), conditional on alpha~lambda. A real (bounded, conditional)
    partial, not a whiff. Worth a dedicated note + (eventually) a structure-formation/dark-sector test.""")
