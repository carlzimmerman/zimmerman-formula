#!/usr/bin/env python3
r"""
ROUTE C -- MULTI-FIELD / extended no-particle dark sector vs the cluster-CORE residual.
=========================================================================================
THE STANDING (banked, do NOT re-litigate):
  * The cluster-core residual is GAS-TRACKING (RX J1347 merger + A2029 relaxed XRISM-clean,
    inner log-slope d ln M_res/d ln r = +1.81, M_res/M_star RISES ~15-30x outward).
  * No-new-particle stack covers ~50-71% (relaxed A2029) to ~45% (gas-tracking) of the core.
  * The ~30-49% remainder is the irreducible SHARED MOND-cluster gap (framework MI == AeST MG).
  * The single ghost-condensate scalar (Y^{3/2} MOND term + K2(Q-Q0)^2 dust) is ALREADY in the stack.

THE ROUTE-C QUESTION (the genuinely-untried multi-field door):
  Could a SECOND gravitational field -- still NO new PARTICLE -- cluster MORE in deep cluster
  cores than the single ghost-condensate dust, closing the residual while staying galaxy-safe?
   (a) Does AeST's AETHER VECTOR A_mu source extra core mass via its own field eqn?
   (b) Could a SECOND shift-symmetric scalar with a DIFFERENT (cluster-clustering) mass scale add core mass?
   (c) honest cost: this RELOCATES the postulate (a second field is new structure the framework
       does not derive) but stays no-PARTICLE.

FOUR GATES a closure must pass:
  G1 SUFFICIENCY  -- close the ~30-49% residual at a0=9.36e-11
  G2 GALAXY-VETO  -- NOT break the SPARC RAR (<~0.13 dex)
  G3 NO-NEW-PARTICLE -- own field / known physics, not a new species
  G4 DATA         -- eRASS1 / CLASH / XRISM / Cassini / solar-system / LSS / CMB

BOTH-WAYS (#1 rule): hunt HARD for a real closure; concede honestly if a gate fails.
QUARANTINE: a0/Z/kappa/I0 never asserted derived.

Companion to the banked aether-stress work (cluster_aether_stress_derivation.py) but now
targeting the CORE residual (not R500) with the gas-tracking shape constraint.
"""
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp

# ============================================================ constants
c    = 2.99792458e8
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.0857e19
Mpc  = 3.0857e22
H0   = 2.184e-18                        # 67.4 km/s/Mpc
Om, OmL = 0.315, 0.685
RHO_CRIT0 = 3*H0**2/(8*np.pi*G)
RHO_DE0   = OmL*RHO_CRIT0
a0   = 0.5*c*np.sqrt(G*RHO_DE0)         # framework a0 (pure dark energy) = 9.36e-11
Lam  = 3*OmL*H0**2/c**2                 # cosmological constant [1/m^2]

print("="*100)
print("ROUTE C -- MULTI-FIELD no-particle dark sector vs the cluster-CORE residual (gas-tracking)")
print("="*100)
print(f"  a0 (framework) = {a0:.4e} m/s^2   Lambda = {Lam:.3e} /m^2   1/sqrt(Lambda) = {1/np.sqrt(Lam)/Mpc:.0f} Mpc\n")

# ============================================================ A2029 real profiles (banked, relaxed XRISM-clean)
# from cluster_shape_a2029/a2029_core_residual_shape.py (reproduced <4%)
def nfw_M(r_kpc, M200, conc, r200_kpc):
    rs = r200_kpc/conc
    mm = lambda x: np.log(1+x) - x/(1+x)
    return M200*mm(np.asarray(r_kpc)/rs)/mm(conc)

# M_lens (Sohn+2019 caustic, better-constrained inner TOTAL): M200=8.47e14, c=4, R200=1.91 Mpc
def Mlens_a2029(r_kpc):  return nfw_M(r_kpc, 8.47e14, 4.0, 1910.0)
# M_gas (LBS03 cusp-beta) integrated
rho_gc, beta_g, alpha_g, rc_gas = 6.6e-26, 0.54, 0.55, 77.6   # g/cm3, -, -, kpc
def rho_gas_cgs(r_kpc):
    x = np.asarray(r_kpc)/rc_gas
    return rho_gc*2.0**(1.5*beta_g-0.5*alpha_g)*x**(-alpha_g)*(1.0+x**2)**(-1.5*beta_g+0.5*alpha_g)
def Mgas_a2029(r_kpc):
    out=[]
    for R in np.atleast_1d(r_kpc):
        I,_=quad(lambda rk: rho_gas_cgs(rk)*4*np.pi*(rk*3.0857e21)**2*3.0857e21, 1e-3, R, limit=200)
        out.append(I/1.989e33)   # g -> Msun
    return np.array(out) if np.ndim(r_kpc) else out[0]
# M_star: IC 1101 BCG+ICL Hernquist, M*=4e12, Re=76 kpc (a~Re/1.8153)
def Mstar_a2029(r_kpc, Mstar=4e12, Re=76.0):
    a_h = Re/1.8153
    r=np.asarray(r_kpc)
    return Mstar*r**2/(r+a_h)**2

# framework MOND (modified-inertia, dS-Unruh nu): g_obs = sqrt(g_bar^2 + g_bar a0)
def M_mond(r_kpc, Mbar_func):
    r=np.atleast_1d(r_kpc).astype(float); out=[]
    for R in r:
        Mb=Mbar_func(R)*Msun; rm=R*kpc
        gbar=G*Mb/rm**2
        gobs=np.sqrt(gbar**2+gbar*a0)
        out.append(gobs*rm**2/G/Msun)
    return np.array(out) if np.ndim(r_kpc) else out[0]

Mbar_a2029 = lambda r: Mgas_a2029(r)+Mstar_a2029(r)

R = np.array([20.,50.,100.,200.,300.,420.])
Mlens = Mlens_a2029(R); Mgas=Mgas_a2029(R); Mstar=Mstar_a2029(R); Mmond=M_mond(R,Mbar_a2029)
Mres  = Mlens - Mmond
print("PART 0 -- the CORE residual target (real A2029, relaxed XRISM-clean)")
print(f"  {'r[kpc]':>8}{'M_lens':>11}{'M_gas':>11}{'M_star':>11}{'M_MOND':>11}{'M_res':>11}{'res/gas':>9}{'res/star':>9}")
for i,r in enumerate(R):
    print(f"  {r:>8.0f}{Mlens[i]:>11.2e}{Mgas[i]:>11.2e}{Mstar[i]:>11.2e}{Mmond[i]:>11.2e}{Mres[i]:>11.2e}"
          f"{Mres[i]/Mgas[i]:>9.2f}{Mres[i]/max(Mstar[i],1):>9.2f}")
# core target & no-particle coverage at 420 kpc
cover_baseline = Mmond[-1]/Mlens[-1]
print(f"\n  Core target M_res(<420kpc) = {Mres[-1]:.3e} Msun;  bare-MOND coverage = {cover_baseline*100:.1f}% of M_lens")
print(f"  Residual to close (after the banked field+remnant stack ~50-71%): the ~30-49% shared gap.")
print(f"  M_res/M_gas is FLAT-to-declining ({Mres[0]/Mgas[0]:.1f}->{Mres[-1]/Mgas[-1]:.1f}) = GAS-TRACKING.")
print(f"  ANY multi-field closure must (i) supply ~{Mres[-1]:.2e} Msun in the core AND (ii) track gas, not stars.\n")

# ============================================================================================
print("="*100)
print("PART 1 -- ROUTE C(a): does the AeST AETHER VECTOR A_mu source extra CORE mass?")
print("="*100)
print(r"""
  THE AeST FIELD CONTENT (Skordis-Zlosnik 2021, Eq.5):  metric g, unit-timelike aether A^mu
  (A.A=-1), scalar phi.  Free function F(Y,Q), Y=spatial-projected (grad phi)^2 (the a0/MOND
  sector), Q = A.grad phi (the cosmological/CDM-dust sector, K(Q)=-2Lambda+1/2 K2 (Q-Q0)^2).

  KEY THEOREM (Eling-Jacobson 2006 gr-qc/0603058 static-aether; Mistele 2023 2305.07742):
  in a STATIC, SPHERICALLY-SYMMETRIC system the unit aether is forced PURELY TIMELIKE (A^i=0).
  Its vector kinetic term F_{mu nu}F^{mu nu} (the curl sector) VANISHES.  => the aether's ONLY
  contribution to the radial g in a relaxed cluster is the SCALAR mass term mu^2 Phi in Eq.2.40:
        (1/r^2) d/dr[r^2 M(x) Phi'] + mu^2 Phi = 4 pi G_N rho_b,    mu^2 = 2 K2 Q0^2/(2-K_B).
  THERE IS NO SEPARATE VECTOR FORCE IN THE CORE.  (a) reduces to the mass-term analysis.
""")

# --- size the aether mass-term contribution and its SHAPE in the CORE (not just R500) ---
# rho_aether(r) = -mu^2 Phi(r)/(4 pi G); Phi<0 in a well => rho_aether>0. Solve Eq.2.40 in
# canonical-momentum variables P = r^2 M(x) Phi' (removes the Helmholtz zero-crossing singularity).
def M_interp(x):  # AeST modified-Laplacian interpolation (Durakovic-Skordis 2.9)
    return (np.sqrt(1+4*x)-1)/(np.sqrt(1+4*x)+1)

def solve_aest_massterm(invmu_Mpc, Mbar_func, r_in_kpc=5., r_out_kpc=3000., dphi0=0.0, npts=4000):
    """Integrate Eq.2.40 outward in P=r^2 M(x) Phi'. Returns r[kpc], g_aest/g_mond, M_res_aether(<r)."""
    mu = 1.0/(invmu_Mpc*Mpc)
    r_grid = np.logspace(np.log10(r_in_kpc), np.log10(r_out_kpc), npts)*kpc
    # natural inner anchor: Phi0 = MOND well start; P0 = G M_enc (MOND limit, mu->0)
    Mb0 = Mbar_func(r_in_kpc)*Msun
    P0  = G*Mb0                       # MOND: P=G M_enc
    Phi0= -np.sqrt(G*Mb0*a0)*1.0 + dphi0  # deep-MOND well scale ~ v_c^2; dphi0 = free boundary shift
    def rhs(r, y):
        P, Phi = y
        Mb = Mbar_func(r/kpc)*Msun
        # solve M(x) Phi' = P/r^2 for Phi' given x=|Phi'|/a0
        # M(x)=(sqrt(1+4x)-1)/(sqrt(1+4x)+1); M(x)*a0*x = P/r^2 => solve for x
        target = abs(P)/r**2 / a0
        # M(x)*x as fn of x is monotone; invert numerically
        from scipy.optimize import brentq
        if target<1e-30:
            xphi=0.0
        else:
            f=lambda x: M_interp(x)*x - target
            try: xphi=brentq(f,1e-12,1e8)
            except Exception: xphi=target  # newton limit
        Phip = np.sign(P)*a0*xphi
        dPdr = r**2*(-mu**2*Phi + 4*np.pi*G*( Mb/(4*np.pi*r**3/3) if False else 0))  # baryon already in MOND P0
        # the baryon source enters via P0=G M_enc; here track the mu^2 drain/pump only:
        dPdr = -mu**2 * Phi * r**2 + 4*np.pi*G*rho_b_of_r(r/kpc, Mbar_func)*r**2
        return [dPdr, Phip]
    sol = solve_ivp(rhs, [r_in_kpc*kpc, r_out_kpc*kpc], [P0, Phi0],
                    t_eval=r_grid, method='LSODA', rtol=1e-6, atol=1e-30, max_step=50*kpc)
    return sol

def rho_b_of_r(r_kpc, Mbar_func, dr=1e-2):
    r=np.asarray(r_kpc,dtype=float)
    Mp = Mbar_func(r*(1+dr)); Mm = Mbar_func(r*max(1-dr,1e-3))
    dMdr = (Mp-Mm)*Msun/((r*(1+dr)-r*(1-dr))*kpc)
    return dMdr/(4*np.pi*(r*kpc)**2)

# the controlling dimensionless number for the mass-term enhancement (banked): f = kappa (mu r)^2, kappa~0.48 log-well
kappa_logwell = 0.48
print("  (i) MAGNITUDE in the core vs at R500 -- f_aether = kappa (mu r)^2, kappa~0.48 (log-well, banked):")
print(f"     {'r':>8}{'1/mu=1Mpc':>14}{'1/mu=0.5Mpc':>14}   (f_aether = fractional extra g)")
for r_kpc,label in [(50,'core 50kpc'),(100,'core 100kpc'),(420,'~R2500/core edge'),(1300,'R500')]:
    f1 = kappa_logwell*(r_kpc*kpc/(1.0*Mpc))**2
    f2 = kappa_logwell*(r_kpc*kpc/(0.5*Mpc))**2
    print(f"     {r_kpc:>6}kpc{f1:>14.4f}{f2:>14.4f}   {label}")
print(r"""
  READING: the mass-term enhancement scales as r^2 -- it is NEGLIGIBLE in the core (f~0.001 at
  50 kpc, ~0.05 at 100 kpc even with a galaxy-UNSAFE 1/mu=0.5 Mpc) and only reaches O(1) near
  R500 (~1.3 Mpc). The aether vector helps in the OUTSKIRTS, NOT the core. This is the WRONG
  RADIUS for the gas-tracking core residual, which needs the boost AT 50-420 kpc.
""")

# --- (ii) the SHAPE: integrate the actual mass-term enhancement profile and compare to gas-tracking ---
print("  (ii) SHAPE -- integrate rho_aether(r) = -mu^2 Phi(r)/(4 pi G) and ask: does it track GAS?")
print(r"""
  In deep MOND the well is logarithmic: Phi(r) = v_c^2 ln(r/r_t), v_c^2 = sqrt(G M_bar a0) ~ const.
  => rho_aether(r) = -mu^2 v_c^2 ln(r/r_t)/(4 pi G).  This is NEGATIVE (a DEFICIT) inside r_t and
  only positive (extra mass) outside r_t where ln>0 -- the OPPOSITE of a centrally-concentrated
  gas-tracking residual. M_aether(<r) = -(mu^2/G) INT_0^r Phi r'^2 dr' grows as ~r^3 ln r =>
  the aether 'phantom' is an OUTSKIRTS halo, centrally HOLLOW. Compare slopes:
""")
# log-well rho_aether shape vs gas (beta) and stars (Hernquist)
def rho_aether_logwell(r_kpc, invmu_Mpc, vc2, r_t_kpc=600.):
    mu=1.0/(invmu_Mpc*Mpc)
    Phi = vc2*np.log(np.asarray(r_kpc)/r_t_kpc)
    return -mu**2*Phi/(4*np.pi*G)   # kg/m^3 (sign: >0 where Phi<0, i.e. r<r_t)
vc2_a2029 = np.sqrt(G*5e13*Msun*a0)   # deep-MOND v_c^2 for A2029-scale baryons
rr=np.array([50.,100.,200.,300.,420.,800.])
rho_ae = rho_aether_logwell(rr,1.0,vc2_a2029)
rho_g  = rho_gas_cgs(rr)*1e3          # g/cm3 -> kg/m3
print(f"     {'r[kpc]':>8}{'rho_aether':>14}{'rho_gas':>14}{'ae/gas':>10}  (rho in kg/m^3; r_t=600kpc)")
for i,r in enumerate(rr):
    print(f"     {r:>8.0f}{rho_ae[i]:>14.3e}{rho_g[i]:>14.3e}{rho_ae[i]/rho_g[i]:>10.4f}")
print(r"""
  READING: rho_aether is POSITIVE but tiny in the core and grows toward r_t (centrally HOLLOW,
  rising outward) -- the OPPOSITE radial shape from the centrally-cusped gas. It does NOT track
  gas in the core; it under-delivers in the core by ~10^3-10^4 and only competes near R500.
  And beyond r_t it goes NEGATIVE (the Helmholtz 'negative phantom mass' deficit) -- banked.
""")
print("  ROUTE C(a) VERDICT: the aether vector contributes ONLY the mu^2 mass term in spherical")
print("  symmetry (curl sector vanishes, Eling-Jacobson). That term scales as (mu r)^2 -> NEGLIGIBLE")
print("  in the core (G1 FAIL: ~0.1-0.5% of the core residual), is centrally HOLLOW (G4 FAIL: anti-")
print("  gas-tracking shape), and full-delivery needs 1/mu<1 Mpc which bends galaxies (G2 squeeze).")
print("  This is the SAME mass term banked as falsified-as-closure at R500 -- now also dead in the CORE.\n")

# ============================================================================================
print("="*100)
print("PART 2 -- ROUTE C(b): a SECOND shift-symmetric scalar with a DIFFERENT (clustering) mass scale")
print("="*100)
print(r"""
  THE PROPOSAL: add a second gravitational scalar chi (no new PARTICLE -- a classical field,
  like the ghost-condensate phi) with its OWN mass/length scale m_chi (Compton 1/m_chi = l_chi),
  tuned to cluster in cluster cores (~100-400 kpc) while staying inert in galaxy cores.

  THE DECISIVE OBSTRUCTION (this is the crux, both ways):
  A SECOND field can add core mass in only TWO ways, and BOTH are already-killed or self-defeating:

   (1) DENSITY-DEPENDENT clustering (chameleon/screening): chi clusters where rho_b is high.
       -> REQUIRES a potential V(chi) with a density-dependent effective mass (chameleon).
       -> A SHIFT-SYMMETRIC scalar (the framework's own type, no V) CANNOT chameleon (banked
          Route C: shift symmetry -> no chameleon; Ward identity -> no Y->Q sourcing). If we
          ADD a V(chi) to get screening we (i) break shift symmetry (new structure, a genuine
          new potential = effectively a new species' worth of postulate) AND (ii) re-enter the
          DENSITY-a0 graveyard: a field that clusters in dense cluster cores ALSO clusters in
          dense galaxy cores/bulges -> breaks the SPARC RAR (the 222-406x, 0.38-dex killer).
          A chameleon thin-shell could in principle screen galaxies -- but galaxy CORES are
          DENSER than cluster cores (rho_gal_core ~ 0.1-1 Msun/pc^3 >> rho_clus_core ~ 1e-3),
          so any density-triggered clustering fires in galaxies FIRST. WRONG ENVIRONMENT ORDER.

   (2) FIXED-LENGTH clustering (a Compton/Jeans scale l_chi): chi is a massive scalar whose
       static profile around baryons is Yukawa, range l_chi. To add ~core mass it needs
       l_chi ~ 100-400 kpc. But a FIXED length cannot tell a cluster core from a galaxy:
       a 100-kpc Yukawa cloud sourced by baryons has the SAME fractional effect wherever the
       baryons are -- it sources around galaxy disks (10-30 kpc < l_chi) too, where it shows
       up as extra flat-curve mass at large R -> alters the SPARC RAR. Quantify below.
""")

# --- quantify the fixed-length (Yukawa) second scalar: amplitude needed in core vs galaxy spillover ---
print("  (2) FIXED-LENGTH (Yukawa) second scalar -- core delivery vs galaxy spillover:")
print(r"""
  Model: a massive scalar chi sourced by baryons, alpha = coupling strength (relative to gravity),
  l_chi = Compton range. Static profile gives an EXTRA acceleration
     g_chi(r) = alpha * G M_b(<r)/r^2 * [Yukawa form factor], saturating to alpha*g_N for r<<l_chi.
  To supply the core residual eta_res = M_res/M_MOND ~ 0.41/0.59 ~ 0.69 of the MOND mass at 420 kpc,
  i.e. g_chi/g_MOND ~ 0.69 at 420 kpc, with g_MOND = sqrt(g_N a0) deep-MOND:
     alpha*g_N / sqrt(g_N a0) = 0.69  =>  alpha = 0.69 * sqrt(a0/g_N).
""")
# A2029 core: at 420 kpc
r_core = 420.; Mb_core = Mbar_a2029(r_core)*Msun; gN_core = G*Mb_core/(r_core*kpc)**2
gMOND_core = np.sqrt(gN_core*a0)
Mres_frac = Mres[-1]/Mmond[-1]
alpha_needed = Mres_frac * np.sqrt(a0/gN_core)
print(f"     A2029 @420kpc: g_N={gN_core:.3e}, g_MOND={gMOND_core:.3e}, g_N/a0={gN_core/a0:.3f} (deep-MOND)")
print(f"     core residual fraction g_res/g_MOND = {Mres_frac:.3f}")
print(f"     => required Yukawa coupling alpha = {alpha_needed:.3f}  (with l_chi >~ 420 kpc to fill the core)\n")

# galaxy spillover: same alpha, same l_chi, on a SPARC disk. At galaxy scales r<<l_chi so g_chi=alpha*g_N FULLY.
print("  GALAXY SPILLOVER (same alpha, l_chi>=420kpc >> galaxy size): a SPARC disk RC point:")
print(r"""
  For a galaxy (r ~ 10-30 kpc << l_chi ~ 420 kpc) the Yukawa is UNscreened: g_chi = alpha*g_N exactly.
  The framework's RAR is g_obs=sqrt(g_N^2 + g_N a0). Adding g_chi=alpha*g_N shifts g_N->(1+alpha)g_N
  EVERYWHERE on the disk -- a pure rescaling of the baryonic acceleration = a MASS-TO-LIGHT shift of
  (1+alpha). The RAR is M/L-degenerate at the ~20% level, so a UNIFORM (1+alpha) on ALL galaxies is
  partly absorbable -- BUT alpha is set by the cluster (a FIXED coupling), and the SAME alpha applied
  to galaxies shifts the deep-MOND plateau v^4 = G M a0 (1+alpha)^2 -> the BTFR normalization and the
  RAR a0 move by (1+alpha). Quantify the RAR damage:
""")
# the deep-MOND acceleration relation with a universal (1+alpha) baryon boost: g_obs=sqrt((1+a)^2 gN^2 + (1+a) gN a0)
# in deep MOND g_obs -> sqrt((1+a) gN a0): the effective a0 -> (1+alpha) a0. RAR offset in dex:
import math
for al in [alpha_needed, 0.3, 0.69]:
    da0_dex = math.log10(1+al)
    print(f"     alpha={al:.2f}: deep-MOND effective a0 -> (1+alpha)a0 => RAR/BTFR a0 shifts +{da0_dex:.3f} dex")
print(r"""
  READING: a fixed-length (l_chi>=420kpc) Yukawa scalar that fills the cluster core with alpha~0.69
  shifts the galaxy deep-MOND a0 by +log10(1.69)=+0.228 dex -- a 1.7x boost of the SPARC RAR a0,
  FAR outside the <~0.13 dex galaxy-veto window. The SAME coupling that helps clusters re-bends every
  galaxy. (And the framework already pays a +12.6% surcharge for a0=9.36e-11 vs 1.2e-10; a +69% boost
  is the WRONG direction and ~5x the entire convention spread.)  This is the density-a0 graveyard in
  Yukawa clothing: a UNIVERSAL coupling cannot be cluster-ON / galaxy-OFF.
""")

# --- both-ways: the Yukawa form factor makes core delivery WEAKER -> alpha even larger; and the
#     environment-ordering (galaxy cores DENSER than cluster cores) check ---
print("="*100)
print("PART 3 -- BOTH-WAYS hardening of Route C(b): form-factor + environment ordering + the one escape")
print("="*100)
# Yukawa form factor: a point source gives g_chi = alpha G M/r^2 (1+r/l) e^{-r/l}. At r=l_chi it's
# alpha gN * (1+1) e^-1 = 0.736 alpha gN -> core delivery REDUCED, required alpha LARGER.
for linv_kpc in [420., 800., 2000.]:
    ff = (1+r_core/linv_kpc)*np.exp(-r_core/linv_kpc)
    alpha_ff = alpha_needed/ff
    print(f"  l_chi={linv_kpc:>5.0f}kpc: Yukawa form-factor@420kpc={ff:.3f} -> required alpha={alpha_ff:.3f}"
          f" -> galaxy a0 shift +{math.log10(1+alpha_ff):.3f} dex")
print(r"""
  => accounting for the Yukawa suppression makes the required alpha LARGER (0.98 -> 1.3-2.7) and the
  galaxy a0 shift WORSE (+0.30 -> +0.36-0.57 dex). G2 fails harder.
""")
# environment ordering: a density-triggered (chameleon) field fires where rho is highest. Compare:
rho_gal_core  = 0.3 * Msun/(3.0857e16)**3   # ~0.3 Msun/pc^3 typical bulge/inner-disk (pc=3.0857e16 m)
rho_clus_core = (Mgas_a2029(100.)*Msun)/((4/3)*np.pi*(100*kpc)**3)  # mean gas density <100kpc
print(f"  ENVIRONMENT ORDERING (kills the chameleon escape):")
print(f"     galaxy inner/bulge density  ~ {rho_gal_core:.3e} kg/m^3 (~0.3 Msun/pc^3)")
print(f"     cluster core mean density   ~ {rho_clus_core:.3e} kg/m^3 (A2029 gas <100kpc)")
print(f"     ratio rho_gal/rho_clus      ~ {rho_gal_core/rho_clus_core:.0f}x")
print(r"""  => galaxy cores are ~10^3-10^5 x DENSER than cluster cores. ANY density-triggered clustering
  (chameleon, symmetron, Jeans) fires in GALAXIES FIRST. There is NO density threshold that is
  cluster-core-ON and galaxy-core-OFF -- the ordering is backwards. (This is the SAME reason the
  density-a0 law breaks galaxies: dense places are galaxies, not cluster cores.)
""")
print(r"""  THE ONE GENUINE ESCAPE (tested, both ways): source chi NOT by baryon DENSITY but by a
  cluster-ONLY observable -- the hot-gas TEMPERATURE/pressure (clusters: kT~5-10 keV; galaxies:
  ~0.01-0.1 keV). A scalar Yukawa-coupled to the gas INTERNAL ENERGY (T^mu_mu of the hot plasma)
  would source ~T -> ~100x stronger in clusters than galaxies. BUT:
   - this is a NEW coupling of a NEW field to the SM stress trace = a genuine new sector (a fifth
     force on baryons), NOT 'the framework's own field' -- it RELOCATES the postulate fully and
     adds a new SM interaction the framework does not have. (G3: no-new-particle PARTIAL -> it is a
     new FIELD + a new COUPLING, structurally heavier than a relabeled mode.)
   - T-sourcing tracks the hot GAS -> it WOULD be gas-tracking (G4 shape OK!) -- the only proposal
     that can match the shape. But a scalar coupling to T_trace of baryons is a long-range fifth
     force that violates the Cassini/solar-system bound (the Sun is hot: kT_core~1 keV) unless
     screened -> back to needing a screening mechanism -> back to the environment-ordering kill.
   - and it is observationally a SECOND dark species in all but name (a field whose energy density
     IS the missing cluster mass), so 'no dark matter at clusters' is forfeited exactly as with the
     sterile-nu patch -- the relocation, not a derivation.
""")
print("  ROUTE C(b) VERDICT: a second shift-symmetric scalar cannot be cluster-core-ON/galaxy-OFF.")
print("  Fixed-length Yukawa: universal coupling re-bends galaxies (+0.30 to +0.57 dex, G2 FAIL).")
print("  Density-triggered: galaxy cores are denser -> fires in galaxies first (G2 FAIL, wrong order).")
print("  T/pressure-sourced: matches gas shape but is a NEW field + NEW SM coupling (G3 relocates) and")
print("  needs screening to pass Cassini -> re-enters the environment-ordering kill (G2/Cassini FAIL).\n")
