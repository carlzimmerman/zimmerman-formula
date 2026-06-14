#!/usr/bin/env python3
"""
ROUTE B -- LSS / TURNAROUND MATCHING: does the PHYSICAL turnaround/cosmological
background fix the free Helmholtz boundary constant chi_out to a UNIVERSAL value,
and does that value give eta(R500) ~ 2.15 across clusters?
================================================================================
Framework (C. Zimmerman): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2, realized
covariantly by AeST (Skordis-Zlosnik 2021). a0 and the coefficient are QUARANTINED
(NOT asserted derived). mu is the free CMB-pinned AeST constant; 1/mu = 1 Mpc, held
identically galaxies<->clusters.

THE QUESTION (Route B, independent of Route A's "minimize the outer envelope" BC):
  The +mu^2 Helmholtz operator leaves a FREE boundary constant chi_out
  (Verwayen-Skordis-Boehm 2024, MNRAS 531 272; their chi_hat_out = chi(r0)/sqrt(G_N M a0),
   Eq. 18-20). Route A killed it by minimizing the outer oscillation (=> deficit).
  Route B asks a DIFFERENT, physical question: a cluster is NOT isolated to r=inf.
  It detaches from the Hubble flow at the TURNAROUND radius r_ta (few Mpc). Beyond
  r_ta the field is the surrounding LARGE-SCALE-STRUCTURE / COSMOLOGICAL BACKGROUND
  AeST scalar, NOT a decaying isolated tail. So the physical boundary condition is
     Phi_bar(r_ta) = Phi_bg(z_formation)   [match to the cosmological background]
  NOT Phi(inf)->0. Does THIS matching select a UNIVERSAL chi_out -> eta~2.15?

THE COSMOLOGICAL BACKGROUND (Durakovic-Skordis 2024, arXiv:2312.00889, exact eqns):
  * The AeST scalar: phi = Q0 t + varphi          (their 2.14)
  * Cosmological shift charge Q evolves with redshift like DUST:
        Q = Q0 + I0 (1+z)^3 + ...                 (their p.5; energy density ~(1+z)^3)
    I0 = initial displacement of Q from its minimum Q0; sets Omega_AeST.
  * The MASS is set by Q0 at the MINIMUM:
        mu^2 = 2 K2 Q0^2 / (2 - K_B)              (their 2.18)
    => mu is a CONSTANT (Q0 = const = minimum), CMB/cosmo-pinned. 1/mu = 1 Mpc.
  * Weak-field cluster eqn (their 2.20, 2.25, 2.33):
        Laplacian(Phi_bar) + mu^2 Phi = 4 pi G rho_b ,  Phi_bar = Phi - chi
  Cosmologically rho_b -> rho_mean(z), and the mass term mu^2 Phi balances the cosmic
  source. The HOMOGENEOUS (spatially-flat) cosmological particular solution is
        Phi_bg(z) = 4 pi G rho_AeST(z) / mu^2     [Laplacian=0 on the homogeneous bg]
  i.e. the value the cluster field MUST approach as r -> r_ta is set by COSMOLOGY,
  the same prescription for every cluster (modulo formation redshift z_f).

WHAT THIS SCRIPT COMPUTES (all from first principles, run python):
  1. The cosmological background AeST scalar potential Phi_bg(z) from rho_AeST(z)
     and mu (the dust-like (1+z)^3 condensate). -> the universal chi_out candidate.
  2. The turnaround radius r_ta(M500) from spherical collapse (lambda_ta) and from
     the AeST/MOND deep-MOND collapse.
  3. Integrate the FULL nonlinear AeST EOM inward from r_ta with the matched
     boundary value Phi_bar(r_ta)=Phi_bg, and read eta(R500).
  4. eta(M500) trend: is it FLAT (cosmological-BC signature) or scattered (tune)?
  5. HONESTY: does the matching value have any residual per-cluster freedom? Is the
     chi_out it selects the SAME for all clusters? Both-ways: also report what the
     turnaround match gives if z_f varies cluster-to-cluster.

Companion to Route A (cluster_aest_shooting_solver.py). INDEPENDENT physics + BC.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# ----------------------------------------------------------------- constants
c    = 2.99792458e8
G_N  = 6.674e-11
Msun = 1.989e30
kpc  = 3.0857e19
Mpc  = 3.0857e22
a0   = 9.36e-11            # framework a0 (quarantined, not derived)
Lam  = 1.106e-52          # Lambda [1/m^2] (Planck 2018: ~1.1e-52)
H0   = 67.4*1e3/Mpc       # 1/s
Om, OL = 0.315, 0.685

# AeST mass scale: 1/mu = 1 Mpc, CMB-pinned, identical galaxies<->clusters
inv_mu_Mpc = 1.0
mu = 1.0/(inv_mu_Mpc*Mpc)
mu2 = mu*mu

print("="*84)
print("ROUTE B -- TURNAROUND / LSS MATCHING: does cosmology fix chi_out universally?")
print("="*84)
print(f"a0={a0:.3e} m/s^2 | 1/mu={inv_mu_Mpc} Mpc (mu={mu:.3e} 1/m) | "
      f"H0={H0*Mpc/1e3:.1f} km/s/Mpc")

# =========================================================================
# STEP 1. THE COSMOLOGICAL BACKGROUND AeST SCALAR POTENTIAL Phi_bg(z)
# =========================================================================
# The AeST condensate (Durakovic-Skordis p.5) is DUST-LIKE: its energy density
# scales (1+z)^3, set by the displacement I0 of Q from Q0. In the LCDM-matching
# AeST cosmology, this condensate PLAYS THE ROLE OF (part of) the matter/DM budget.
# At the BACKGROUND level the cluster eqn  Lap(Phi_bar)+mu^2 Phi = 4 pi G rho
# has the spatially-homogeneous solution (Lap=0):
#         Phi_bg(z) = 4 pi G rho_source(z) / mu^2
# where rho_source is the cosmic mean density that the mass term balances.
#
# WHICH rho? The mass term mu^2 Phi in AeST is the cosmological condensate; the
# self-consistent statement is that on the homogeneous background the SAME mass
# term that gives mu^2 Phi must reproduce the condensate's gravitational source.
# Two physically-motivated choices, computed BOTH WAYS (honesty):
#   (a) rho = rho_mean,m(z) = Om rho_crit0 (1+z)^3  (the dust the condensate mimics)
#   (b) rho = rho_Lambda  = OL rho_crit0            (the DE floor; framework's a0 root)
print("\n" + "-"*84)
print("STEP 1: cosmological background potential Phi_bg(z) = 4 pi G rho(z)/mu^2")
print("-"*84)
rho_crit0 = 3*H0**2/(8*np.pi*G_N)
print(f"rho_crit0 = {rho_crit0:.4e} kg/m^3")

def Phi_bg(z, which='matter'):
    """Homogeneous cosmological background AeST potential [ (m/s)^2 ]."""
    if which == 'matter':
        rho = Om*rho_crit0*(1+z)**3          # dust the AeST condensate mimics
    elif which == 'lambda':
        rho = OL*rho_crit0                   # DE floor (constant)
    elif which == 'total':
        rho = rho_crit0*(Om*(1+z)**3 + OL)   # total
    return 4*np.pi*G_N*rho/mu2

for z in [0.0, 0.3, 0.5, 1.0]:
    pm = Phi_bg(z,'matter'); pl = Phi_bg(z,'lambda')
    print(f"  z={z:.1f}:  Phi_bg(matter)={pm:.4e} (m/s)^2 = ({np.sqrt(abs(pm)):.0f} m/s)^2 |"
          f"  Phi_bg(Lambda)={pl:.4e} = ({np.sqrt(abs(pl)):.0f} m/s)^2")

# Compare to the MOND potential scale at R500: Phi_MOND ~ (sqrt(G M a0))^... ~ (1500 km/s)^2
PhiMOND_scale = (1500e3)**2
print(f"  [scale check] |Phi_MOND(R500)| ~ ({np.sqrt(PhiMOND_scale)/1e3:.0f} km/s)^2 "
      f"= {PhiMOND_scale:.3e} (m/s)^2  (the depth chi_out must be compared against)")

# =========================================================================
# STEP 2. THE TURNAROUND RADIUS r_ta(M500) FROM SPHERICAL COLLAPSE
# =========================================================================
# Spherical collapse: a perturbation turns around at r_ta then virializes at
# r_vir ~ r_ta/2. In LCDM, r_ta ~ (3 M / (4 pi rho_ta))^(1/3) with the turnaround
# overdensity. A robust, model-light estimate: the turnaround radius is where the
# enclosed mean density = the turnaround density ~ (3pi/4)^2-ish * rho_mean, OR
# equivalently r_ta is a few * R500. We use the standard result r_ta ~ 3-5 R200 ~
# 4-6 R500 and ALSO an absolute spherical-collapse estimate.
print("\n" + "-"*84)
print("STEP 2: turnaround radius r_ta(M500) from spherical collapse")
print("-"*84)
z_obs = 0.3
Hz = H0*np.sqrt(Om*(1+z_obs)**3 + OL)
rho_crit_z = 3*Hz**2/(8*np.pi*G_N)
def R500_of(M500):
    return (M500/((4.0/3.0)*np.pi*500.0*rho_crit_z))**(1.0/3.0)

# Turnaround: at turnaround the structure has mean overdensity Delta_ta ~ 5.55*(1+z)
# (LCDM) relative to critical; the classic EdS value is (3pi/4)^2*... Use the
# standard turnaround overdensity ~ 11 x rho_crit (the LCDM late-time value),
# enclosing the SAME mass M_ta ~ M_collapsed. Equivalent: r_ta where mean density
# = Delta_ta rho_crit.  Also: spherical collapse gives r_ta = 2 r_vir (EdS), and
# r_vir ~ R200 ~ 1.5 R500, so r_ta ~ 3 R500 as an independent cross-check.
Delta_ta = 11.0     # turnaround mean overdensity wrt rho_crit (LCDM late-time)
def r_ta_of(M500):
    # M inside r_ta ~ the collapsing mass (take ~ 2 M500 for the larger turnaround sphere
    # accreted mass; we test sensitivity below). Use M_ta = M500 conservatively first.
    return (M500/((4.0/3.0)*np.pi*Delta_ta*rho_crit_z))**(1.0/3.0)

masses = [1e14, 3e14, 5e14, 1e15]
print(f"  z_obs={z_obs}, Delta_ta={Delta_ta} x rho_crit(z):")
print(f"  {'M500[Msun]':>12s} {'R500[Mpc]':>10s} {'r_ta[Mpc]':>10s} {'r_ta/R500':>10s} "
      f"{'(mu r_ta)^2':>12s}")
clusters=[]
for M in masses:
    M500=M*Msun; R500=R500_of(M500); rta=r_ta_of(M500)
    clusters.append((M,M500,R500,rta))
    print(f"  {M:>12.0e} {R500/Mpc:>10.3f} {rta/Mpc:>10.3f} {rta/R500:>10.2f} "
          f"{(mu*rta)**2:>12.2f}")

# =========================================================================
# 3. BARYONS (same beta-model+BCG as Route A, for an apples-to-apples eta)
# =========================================================================
class Cluster:
    def __init__(self, M500, R500, f_gas500=0.125, f_star500=0.012,
                 rc_over_R500=0.18, beta=2.0/3.0, a_star_kpc=30.0):
        self.M500=M500; self.R500=R500; self.beta=beta
        self.rc=rc_over_R500*R500; self.a_star=a_star_kpc*kpc
        self.M_star=f_star500*M500
        rr=np.linspace(0.0,R500,40000)
        Ig=np.trapz(4*np.pi*rr**2*(1+(rr/self.rc)**2)**(-1.5*beta),rr)
        self.rho_g0=f_gas500*M500/Ig
    def rho_b(self,r): return self.rho_g0*(1+(r/self.rc)**2)**(-1.5*self.beta)
    def M_gas(self,r):
        rr=np.linspace(0.0,r,4000)
        return np.trapz(4*np.pi*rr**2*self.rho_g0*(1+(rr/self.rc)**2)**(-1.5*self.beta),rr)
    def M_star_lt(self,r): return self.M_star*r**2/(r+self.a_star)**2
    def M_bar(self,r): return self.M_gas(r)+self.M_star_lt(r)
    def g_bar(self,r): return G_N*self.M_bar(r)/r**2

# ---- AeST interpolation + exact flux inversion (identical to Route A) -------
def Mfunc(x):
    s=np.sqrt(1+4*x); return (s-1)/(s+1)
def u_from_flux(F,r):
    if r==0.0: return 0.0
    f=abs(F)/(a0*r*r); u=a0*(np.sqrt(f)+f); return np.sign(F)*u
def g_MOND(cl,r):
    gN=G_N*cl.M_bar(r)/r**2; f=gN/a0; x=f+np.sqrt(f); return a0*x

# =========================================================================
# 4. INTEGRATE THE FULL NONLINEAR EOM with the TURNAROUND-MATCHED BC
#    Integrate INWARD from r_ta (where Phi_bar = Phi_bg, the cosmological match)
#    to R500 and read eta. Phase-space state y=[Phi, F], F=r^2 M(x) Phi'.
#    BC at r_ta: Phi(r_ta) = Phi_bg(z), F(r_ta) = G_N M_bar(<r_ta) (flux continuity:
#    the localized baryon flux; the cosmological mean is subtracted as the bg).
# =========================================================================
def _Mbar_to(cl,r):
    return cl.M_bar(r)
def rhs(r,y,rho_b_func):
    Phi,F=y; u=u_from_flux(F,r)
    return [u, r*r*(4*np.pi*G_N*rho_b_func(r)-mu2*Phi)]

def integrate_inward(cl, r_ta, Phi_ta, r_inner):
    """Integrate (Phi,F) INWARD from r_ta with Phi(r_ta)=Phi_ta (cosmological match)
    and F(r_ta)=G_N M_bar(<r_ta). Returns dense solution."""
    F_ta = G_N*cl.M_bar(r_ta)
    sol=solve_ivp(rhs,[r_ta,r_inner],[Phi_ta,F_ta],args=(cl.rho_b,),
                  t_eval=np.linspace(r_ta,r_inner,4000),rtol=1e-10,atol=1e-12,
                  method='DOP853',dense_output=True,max_step=(r_ta-r_inner)/2000.0)
    return sol
def g_AeST(sol,r):
    Phi,F=sol.sol(r); return abs(u_from_flux(F,r))

print("\n" + "="*84)
print("STEP 3-4: integrate INWARD from r_ta with Phi_bar(r_ta)=Phi_bg(z); read eta(R500)")
print("="*84)

def run_match(which_bg, z_match, label):
    print(f"\n--- MATCH = Phi_bg({which_bg}, z={z_match}) = "
          f"{Phi_bg(z_match,which_bg):.4e} (m/s)^2   [{label}] ---")
    print(f"  {'M500':>10s} {'R500[Mpc]':>10s} {'r_ta[Mpc]':>9s} {'Phi_ta':>12s} "
          f"{'g_MOND':>11s} {'g_AeST':>11s} {'eta(R500)':>10s}")
    etas=[]; lgM=[]
    Pta = Phi_bg(z_match, which_bg)   # the SAME background value for all clusters
    # NOTE: the cluster field at r_ta is Phi = Phi_bar + chi; the matched quantity is
    # the gauge-invariant background. The localized solution sits on TOP of Phi_bg.
    # We seed Phi(r_ta)=Phi_bg (sign convention: condensate is a potential WELL? It
    # is a positive 4 pi G rho/mu^2 -> we test the sign both ways below).
    for (M,M500,R500,rta) in clusters:
        cl=Cluster(M500,R500,f_gas500=0.09+0.06*(np.log10(M)-14.0),f_star500=0.012)
        sol=integrate_inward(cl,rta,Pta,0.05*Mpc)
        gM=g_MOND(cl,R500); gA=g_AeST(sol,R500); eta=gA/gM
        etas.append(eta); lgM.append(np.log10(M))
        print(f"  {M:>10.0e} {R500/Mpc:>10.3f} {rta/Mpc:>9.3f} {Pta:>12.3e} "
              f"{gM:>11.4e} {gA:>11.4e} {eta:>10.4f}")
    slope=np.polyfit(lgM,etas,1)[0]
    print(f"  d eta/d log10(M500) = {slope:+.3f}   (eRASS1: flat ~ -0.03; target eta~2.15)")
    print(f"  mean eta(R500) = {np.mean(etas):.3f}, spread = {np.ptp(etas):.3f}")
    return etas, slope

# Run BOTH WAYS: matter-condensate match and Lambda-floor match, at z_match=z_obs
e_m, s_m = run_match('matter', 0.3, 'AeST dust-condensate background (rho_m, declining inward irrelevant)')
e_l, s_l = run_match('lambda', 0.3, 'Lambda/DE floor background (constant)')
e_t, s_t = run_match('total' , 0.3, 'total cosmic background')

# negative sign (potential well) both-ways
print("\n--- SIGN both-ways: match to a NEGATIVE bg (condensate as a potential well) ---")
def run_match_signed(which_bg, z_match, sgn):
    Pta = sgn*Phi_bg(z_match, which_bg)
    etas=[]
    for (M,M500,R500,rta) in clusters:
        cl=Cluster(M500,R500,f_gas500=0.09+0.06*(np.log10(M)-14.0))
        sol=integrate_inward(cl,rta,Pta,0.05*Mpc)
        etas.append(g_AeST(sol,R500)/g_MOND(cl,R500))
    return etas
for sgn,tag in [(+1,'+ (over-density potential)'),(-1,'- (potential well)')]:
    em=run_match_signed('matter',0.3,sgn)
    print(f"  sign {tag:28s}: eta(R500) = "
          f"[{', '.join(f'{e:.3f}' for e in em)}]  mean={np.mean(em):.3f}")

# =========================================================================
# 5. THE UNIVERSALITY / TUNE TEST -- is chi_out hidden-free per cluster?
# =========================================================================
print("\n" + "="*84)
print("STEP 5: UNIVERSALITY TEST -- is the matched chi_out one prescription, or a knob?")
print("="*84)
# The matching value Phi_bg(z) depends ONLY on z (cosmology), NOT on M500 or any
# per-cluster property. So IF the physics is "match Phi at r_ta to Phi_bg(z)", chi_out
# is UNIVERSAL (one z->one value). The only cluster-to-cluster freedom is z_formation.
# Quantify: how much does eta(R500) move as z_match (formation) ranges 0.2-1.0?
print("  Sensitivity of eta(R500) [5e14 cluster] to z_match (formation redshift):")
M,M500,R500,rta = clusters[2]
cl=Cluster(M500,R500,f_gas500=0.12)
print(f"  {'z_match':>8s} {'Phi_bg(m)':>12s} {'eta(R500)':>10s}")
for zm in [0.2,0.3,0.5,0.7,1.0]:
    Pta=Phi_bg(zm,'matter')
    sol=integrate_inward(cl,rta,Pta,0.05*Mpc)
    print(f"  {zm:>8.2f} {Pta:>12.3e} {g_AeST(sol,R500)/g_MOND(cl,R500):>10.4f}")

# What chi_out (in MOND-potential units, like Verwayen chi_hat_out) does the match
# correspond to? Compare Phi_bg to sqrt(G M a0) per cluster.
print("\n  The matched value in Verwayen's normalized units chi_hat_out=chi/sqrt(G M a0):")
print(f"  {'M500':>10s} {'sqrt(GMa0)':>12s} {'Phi_bg(m,.3)':>13s} {'chi_hat_out':>12s} "
      f"{'Delta vs max~0':>13s}")
for (M,M500,R500,rta) in clusters:
    cl=Cluster(M500,R500)
    norm=np.sqrt(G_N*cl.M_bar(R500)*a0)
    chi_hat=Phi_bg(0.3,'matter')/norm
    print(f"  {M:>10.0e} {norm:>12.3e} {Phi_bg(0.3,'matter'):>13.3e} {chi_hat:>12.4f} "
          f"{chi_hat:>13.4f}")
print("  -> if chi_hat_out is the SAME O(0.001) for all M500, it is NOT Verwayen's")
print("     O(1) free constant Delta -- it is a fixed, COSMOLOGICALLY TINY value.")

# =========================================================================
# 6. THE DECISIVE NUMBER: is Phi_bg big enough to matter vs the MOND depth?
# =========================================================================
print("\n" + "="*84)
print("STEP 6: THE DECISIVE RATIO  Phi_bg / |Phi_MOND(R500)|  (does the BC even bite?)")
print("="*84)
M,M500,R500,rta = clusters[2]
cl=Cluster(M500,R500,f_gas500=0.12)
# MOND potential depth at R500 (integrate g_MOND from R500 outward to r_ta ~ where it
# would asymptote): |Phi_MOND| ~ g_MOND(R500)*R500 * ln factor ~ v_c^2 ln(...)
vc2 = g_MOND(cl,R500)*R500     # ~ circular-velocity-squared scale
print(f"  5e14 cluster: g_MOND(R500)={g_MOND(cl,R500):.3e}, "
      f"v_c^2~g*R500={vc2:.3e} (m/s)^2 = ({np.sqrt(vc2)/1e3:.0f} km/s)^2")
for zm,wb in [(0.3,'matter'),(0.3,'lambda'),(0.3,'total')]:
    P=Phi_bg(zm,wb)
    print(f"  Phi_bg({wb},z={zm})/v_c^2 = {P/vc2:.3e}  "
      f"(Phi_bg={P:.3e}, {'NEGLIGIBLE -> BC barely bites' if abs(P/vc2)<0.05 else 'O(1) -> BC bites'})")

print("\n" + "="*84)
print("END ROUTE B SOLVE. Verdict block printed by wrapper / written to the .md")
print("="*84)
