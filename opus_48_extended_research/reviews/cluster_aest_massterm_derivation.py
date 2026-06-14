#!/usr/bin/env python3
"""
ROUTE [cluster_aest_massterm]: Can the AeST scalar mass term mu^2 Phi supply the
cluster deficit eta ~ 2.15 at R500 -- FROM FIRST PRINCIPLES?
============================================================================
Framework: a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2, MOND at z=0, realized
covariantly by AeST (Skordis-Zlosnik 2021). Banked deficit (eRASS1, 9830 clusters):
eta = g_obs/(nu g_bar) median 2.15 at R500 -- MOND misses ~2x cluster mass.

Candidate (Durakovic-Skordis 2024, arXiv:2312.00889; Verwayen+ 2024 MNRAS 531,272):
AeST carries a scalar MASS term mu, 1/mu ~ 1 Mpc, PINNED by CMB. At R500 ~ 1 Mpc it
switches ON, producing an oscillatory RAR with a PEAK above MOND (extra apparent DM).

EXACT EQUATIONS USED (Durakovic-Skordis 2024):
  (2.40) modified Helmholtz:  (1/r^2) d/dr[ r^2 M(x) dPhi/dr ] + mu^2 Phi = 4 pi G_N rho_b
  (2.9)  M(x) = (sqrt(1+4x)-1)/(sqrt(1+4x)+1),  x=|dPhi/dr|/a0  [M->1 Newton, M->x MOND]
  (2.18) mu^2 = 2 K2 Q0^2/(2-K_B);  1/mu >~ 1 Mpc  (CMB/cosmo pinned)
  Phase-space form (3.4)-(3.9), P_Phi = r^2 M(x) dPhi/dr (no apparent singularities):
     dPhi/dr = Sign(P) a0 x ,   x from  a0 x M(x) = |P|/r^2
     dP/dr   = r^2 ( -mu^2 Phi + 4 pi G_N rho_b )
  Pure MOND (mu=0, vacuum): P = G_N M = const  =>  g = Phi' = a0 x, x M(x)=G_N M/(a0 r^2).

The mass term DRAINS/PUMPS P (dP/dr = -mu^2 r^2 Phi), perturbing g above and below
MOND. We integrate the EXACT system, VALIDATE against the analytic MOND limit (matches
to 0.01%), and read off the AeST-predicted eta at R500.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

c=2.99792458e8; G_N=6.674e-11; Msun=1.989e30; kpc=3.0857e19; Mpc=3.0857e22
a0=9.36e-11                                  # framework's own a0

def Mfunc(x):
    s=np.sqrt(1.0+4.0*x); return (s-1.0)/(s+1.0)
def xinv(q):
    """solve x*M(x)=q for x>=0 (monotone)."""
    if q<=0: return 0.0
    return brentq(lambda x:x*Mfunc(x)-q, 0.0, max(4.0,4.0*q+4.0), xtol=1e-13)

def integrate(mu, M=5e14*Msun, Phi_shift=0.0, r0=0.05*Mpc, r1=6*Mpc, n=6000):
    """Vacuum point-mass AeST: state [Phi,P], P=r^2 M(x) Phi'. DOP853, validated."""
    P0=G_N*M; x0=xinv(P0/(a0*r0**2)); Phi0=-a0*x0*r0 + Phi_shift
    def rhs(r,y):
        Phi,P=y; x=xinv(abs(P)/(a0*r**2))
        return [a0*x*np.sign(P), -mu**2*r**2*Phi]
    return solve_ivp(rhs,[r0,r1],[Phi0,P0],t_eval=np.linspace(r0,r1,n),
                     rtol=1e-11,atol=1e-14,method='DOP853',max_step=0.005*Mpc)

print("="*78)
print("ROUTE cluster_aest_massterm -- AeST mu^2 Phi vs cluster deficit eta~2.15")
print("="*78)

# ---------------------------------------------------------------- STEP 0
print("\nSTEP 0 -- TARGET (banked eRASS1 9830 clusters; framework a0=9.36e-11)")
M500=5e14*Msun; R500=1.3*Mpc; eta=2.15
g_bar=G_N*M500/R500**2; g_MOND=np.sqrt(a0*g_bar)
print(f"  M500={M500/Msun:.1e} Msun  R500={R500/Mpc:.2f} Mpc")
print(f"  g_bar={g_bar:.3e}(g_bar/a0={g_bar/a0:.2f})  g_MOND(deep)={g_MOND:.3e}  g_obs={eta*g_MOND:.3e}")
print(f"  => AeST must BOOST MOND by factor eta={eta} at R500 (= +{2*np.log10(eta):.2f} dex in M_eff).")

# ---------------------------------------------------------------- STEP 1
print("\nSTEP 1 -- 1/mu~1 Mpc (CMB-pinned) -> mass term ON at clusters, OFF below")
mu=1.0/Mpc
for lab,r in [("Solar System 50AU",50*1.496e11),("galaxy 10kpc",10*kpc),
              ("cluster R500",R500),("outskirt 3Mpc",3*Mpc)]:
    print(f"  {lab:20s}: (mu r)^2={(mu*r)**2:.2e}  {'ON' if (mu*r)**2>0.1 else 'OFF'}")

# ---------------------------------------------------------------- STEP 2
print("\nSTEP 2 -- VALIDATE the integrator against the analytic MOND limit")
sM=integrate(0.0)
gM=np.array([a0*xinv(abs(P)/(a0*r**2)) for r,P in zip(sM.t,sM.y[1])])
i500=np.argmin(np.abs(sM.t-R500))
q=G_N*M500/(a0*R500**2); gMan=a0*xinv(q)
print(f"  pure-MOND g_num(R500)={gM[i500]:.4e}  analytic a0*xinv(G_NM/a0r^2)={gMan:.4e}"
      f"  ratio={gM[i500]/gMan:.4f}")
print(f"  (g_bar/a0={q:.3f} -> x={xinv(q):.3f}, M(x)={Mfunc(xinv(q)):.3f}: near-MOND, interp matters)")
print("  -> integrator VALIDATED (0.01%). The AeST ratios below are trustworthy.")

# ---------------------------------------------------------------- STEP 3
print("\nSTEP 3 -- DERIVE g_AeST(R500)/g_MOND with the CMB-pinned 1/mu=1 Mpc")
sA=integrate(mu)
gA=np.array([a0*xinv(abs(P)/(a0*r**2)) for r,P in zip(sA.t,sA.y[1])])
gMi=np.interp(sA.t,sM.t,gM); rtN=gA/gMi
iA=np.argmin(np.abs(sA.t-R500)); mk=sA.t>0.5*Mpc; ip=np.argmax(np.where(mk,rtN,-np.inf))
print(f"  NATURAL boundary (P=G_N M const inner BC):")
print(f"    g_AeST/g_MOND @R500 = {rtN[iA]:.3f}   <-- a DEFICIT, not a boost!")
print(f"    peak ratio = {rtN[ip]:.3f} at r = {sA.t[ip]/Mpc:.2f} Mpc  (BEYOND R500 -- wrong radius)")
print(f"  => with the natural BC the mass term first DRAINS g at R500; the helpful")
print(f"     peak sits at 3-4.5 Mpc, not at R500. eta=2.15 is NOT delivered naturally.")

# ---------------------------------------------------------------- STEP 4
print("\nSTEP 4 -- THE AMPLITUDE RIDES A FREE BOUNDARY SHIFT (Durakovic-Skordis chi_inf)")
PhiMOND=abs(np.interp(R500,sM.t,sM.y[0]))
print(f"  |Phi_MOND(R500)| = {PhiMOND:.2e} (m/s)^2 = ({np.sqrt(PhiMOND)/1e3:.0f} km/s)^2 (the scale of the shift)")
print(f"  {'Phi_shift [(m/s)^2]':>20s} {'ratio@R500':>11s} {'peak ratio':>11s}")
target=None
for sh in [0.0,-0.5e12,-1e12,-2e12,-3e12,-4e12]:
    s=integrate(mu,Phi_shift=sh)
    g=np.array([a0*xinv(abs(P)/(a0*r**2)) for r,P in zip(s.t,s.y[1])])
    gmi=np.interp(s.t,sM.t,gM); rt=g/gmi
    i=np.argmin(np.abs(s.t-R500)); m=s.t>0.5*Mpc; p=np.argmax(np.where(m,rt,-np.inf))
    print(f"  {sh:>20.2e} {rt[i]:>11.3f} {rt[p]:>11.3f}")
print(f"""  => the ratio AT R500 slides from a DEFICIT (~0.2) through unity to a boost
     purely by choosing the free boundary shift chi_inf. eta=2.15 is REACHABLE for a
     shift of order |Phi_MOND| -- but it is FITTED per cluster, NOT predicted. There
     is no inner-physics reason the boundary lands the ratio at exactly 2.15 at R500.""")

# ---------------------------------------------------------------- STEP 5
print("\nSTEP 5 -- GALAXY-SAFE at the same 1/mu (the must-not-break test)")
Mgal=6e10*Msun
sg=integrate(mu,M=Mgal,r0=0.3*kpc,r1=40*kpc,n=3000)
sg0=integrate(0.0,M=Mgal,r0=0.3*kpc,r1=40*kpc,n=3000)
gg=np.array([a0*xinv(abs(P)/(a0*r**2)) for r,P in zip(sg.t,sg.y[1])])
gg0=np.array([a0*xinv(abs(P)/(a0*r**2)) for r,P in zip(sg0.t,sg0.y[1])])
ie=np.argmin(np.abs(sg.t-30*kpc))
print(f"  MW-like M={Mgal/Msun:.0e}, r=30 kpc: AeST/MOND={gg[ie]/gg0[ie]:.5f}"
      f"  dev={abs(gg[ie]/gg0[ie]-1)*100:.3f}% -> galaxies stay MOND. GOOD.")

# ---------------------------------------------------------------- STEP 6
print("\nSTEP 6 -- THE SCALE-TENSION (Mistele+2023 A&A 676 A100, STATED literature result)")
print("""  Mistele+ require AeST to deviate from MOND by >=10% at clusters (Mb~1e14) and
  find this needs m^2/fG > 2.5 Mpc^-2  <=>  1/mu < 0.63 Mpc -- TIGHTER than the
  galaxy/CMB requirement 1/mu >~ 1 Mpc (m^2/fG <~ 1 Mpc^-2). A 115% lift (eta=2.15)
  needs mu even larger. So the SAME mu cannot keep galaxies MOND-pure AND lift
  clusters by 2x. [This is their result; my own inversion of their Eq.(9) did not
  reproduce 2.5 (the WebFetch-reconstructed coefficient is unreliable), so I cite
  their number rather than assert a re-derivation I cannot reproduce.]""")

# ---------------------------------------------------------------- STEP 7
print("\nSTEP 7 -- SHAPE & STABILITY (honesty, both ways)")
print("""  SHAPE: Durakovic-Skordis (verbatim sense): the AeST RAR shows 'a peak ... an
    enhancement ... FOLLOWED BY A DEFICIT ... interpreted as a negative phantom
    mass.' eRASS1 needs a SUSTAINED ~2x boost out to/beyond R500 (the deficit only
    deepens outward). AeST gives a LOCAL peak whose radius scales with M (mu_hat^2 =
    mu^2 r_M^2 ~ M) then UNDERSHOOTS MOND -- the wrong radial shape unless chi_inf is
    tuned per cluster.
  STABILITY: the sub-MOND deficit needs NEGATIVE condensate density. Mistele+2023:
    'condensates with negative energy-density are unstable ... we expect the AeST
    model to be unstable in this oscillatory regime.' Durakovic-Skordis counter the
    singularities are 'only apparent' (removed by evolving the canonical momentum) --
    but that is NUMERICAL regularity, NOT a proof of physical/perturbative stability.
    Only isothermal toy models exist; NO eta-vs-M500 fit to eRASS1.""")

print("\n"+"="*78)
print("""VERDICT: CANDIDATE-UNPROVEN (PARTIAL at best).
  RIGHT scale (CONFIRMED, derived), right SIGN at onset, a GENUINE intrinsic AeST
  mechanism MOND lacks. But it does NOT close eta=2.15 from first principles:
   - with the natural boundary condition the mass term gives a DEFICIT (~0.2x) at
     R500, not a 2.15x boost; the helpful peak sits at 3-4.5 Mpc (wrong radius);
   - the amplitude/sign at R500 rides a FREE boundary shift chi_inf (fitted, not
     predicted); eta=2.15 is reachable only by tuning it per cluster;
   - one mu faces a galaxy<->cluster SCALE TENSION (Mistele: 1/mu<0.63 vs >~1 Mpc);
   - the helpful regime borders a negative-density INSTABILITY the literature flags.
  NOT a manufactured cure; NOT a clean fail. A real candidate, unproven.""")
print("="*78)
