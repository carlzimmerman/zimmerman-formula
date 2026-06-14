#!/usr/bin/env python3
"""
ROUTE A -- COSMOLOGICAL-BACKGROUND MATCHING: what does cosmology fix chi_out to?
================================================================================
Framework (C. Zimmerman): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2, realized
covariantly by AeST (Skordis-Zlosnik 2021 PRL 127 161302). a0/Z QUARANTINED (never
asserted derived). mu = free CMB-pinned AeST constant.

THE PROBLEM THIS SETTLES.
  The cluster scalar perturbation obeys an INHOMOGENEOUS HELMHOLTZ equation
     (1/r^2) d/dr[ r^2 M(x) Phi' ] + mu^2 Phi = 4 pi G_N rho_b(r)        (Durakovic-Skordis 2.40)
  whose +mu^2 sign makes the homogeneous solutions OSCILLATORY [A cos(mu r)+B sin(mu r)]/r,
  BOTH decaying as 1/r. So Phi(inf)->0 is NON-SELECTIVE: it does NOT pin the solution. The
  surviving free constant is Verwayen-Skordis-Zlosnik 2024's chi_hat_out (their boundary
  value of the gravitational potential). The cluster RAR peak eta "depends on the boundary
  value of the gravitational potential" (Durakovic-Skordis 2024 explicitly). chi_out IS the
  whole game.

  This is NOT free per cluster IF physics fixes it. ROUTE A's claim: the cluster scalar
  perturbation must MATCH the evolving COSMOLOGICAL BACKGROUND AeST scalar field at the
  cluster edge (the radius where the overdensity meets the mean cosmic field). That matching
  value is set by COSMOLOGY -- the SAME prescription for every cluster at a given z.

THE DERIVATION (Route A), in five linked steps, all run below:
  STEP 1.  Cosmological AeST background phi_bg(z): the shift-current charge Q0(z) and the
           self-consistent mass mu^2 = 2 K2 Q0^2/(2-K_B). The scalar drives the dark-energy
           mimicry, so its background "potential" amplitude is the cosmological DE potential
           well, ~ the Newtonian potential of the mean density inside the matching radius.
  STEP 2.  The MATCHING CONDITION. The weak-field scalar perturbation Phi is defined RELATIVE
           to the cosmological mean. At the cluster EDGE r_ta (turnaround), the cluster field
           must continuously match the background cosmological field. The boundary value the
           perturbation takes there is chi_out = -[ Phi_cosmo(r_ta) ] = the background-field
           potential the cluster sits IN, evaluated at the matching radius.
  STEP 3.  Compute Phi_cosmo(r_ta). Two physically-equivalent handles, both run:
           (A) the cosmological-constant / DE potential well: Phi_Lambda(r) = -(1/6) Lambda c^2 r^2
               (the de Sitter background potential the AeST scalar mimics), evaluated at r_ta;
           (B) the mean-matter Newtonian potential at turnaround:
               Phi_mean(r_ta) = -(1/2) (4 pi/3) G rho_m(z) r_ta^2  (the field of the cosmic mean
               the cluster decoupled from). These agree to O(1) because at turnaround
               rho_collapse ~ rho_mean and r_ta is the de Sitter / matter crossover.
  STEP 4.  The turnaround radius r_ta(M500, z): set by the spherical-collapse / Lambda
           turnaround condition (the radius where the cluster's mean enclosed density equals
           the turnaround density ~ a few x rho_crit). r_ta ~ (3-5) R500 -- the SAME multiple
           for all clusters (a structural, not per-object, number).
  STEP 5.  chi_out at z~0.3, and IS IT UNIVERSAL? Report chi_out, its (mu r_ta) phase, and the
           per-cluster spread. Then FEED chi_out back into the full nonlinear shooting solver
           and read eta(R500). Both ways: does the cosmologically-fixed chi_out give 2.15, the
           deficit, or smuggle a per-cluster knob?

QUARANTINE: a0/Z never asserted derived. mu the free CMB-pinned constant (1/mu=1 Mpc).
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

# ----------------------------------------------------------------- constants (SI)
c    = 2.99792458e8
G_N  = 6.674e-11
Msun = 1.989e30
kpc  = 3.0857e19
Mpc  = 3.0857e22
a0   = 9.36e-11
H0   = 67.4e3/Mpc                  # 1/s
Om, OL = 0.315, 0.685
# Lambda from a0 = c^2 sqrt(Lambda/32 pi)  =>  Lambda = 32 pi (a0/c^2)^2
Lambda = 32.0*np.pi*(a0/c**2)**2   # 1/m^2
# cross-check Lambda also from OL: Lambda_OL = 3 OL H0^2/c^2
Lambda_OL = 3.0*OL*H0**2/c**2

print("="*92)
print("ROUTE A -- COSMOLOGICAL-BACKGROUND MATCHING: what fixes chi_out?")
print("="*92)
print(f"  a0           = {a0:.3e} m/s^2  (framework, quarantined)")
print(f"  Lambda(a0)   = {Lambda:.3e} 1/m^2   [from a0=c^2 sqrt(Lambda/32pi)]")
print(f"  Lambda(OL)   = {Lambda_OL:.3e} 1/m^2   [from 3 OL H0^2/c^2]  ratio={Lambda/Lambda_OL:.3f}")
print(f"  1/mu (CMB-pinned) = 1.00 Mpc ; mu = {1.0/Mpc:.3e} 1/m")

# =====================================================================================
# STEP 1.  COSMOLOGICAL AeST BACKGROUND phi_bg(z), shift charge Q0(z), self-consistent mu
# =====================================================================================
print("\n" + "="*92)
print("STEP 1 -- cosmological AeST background: phi_bg(z), Q0(z), self-consistent mu^2=2K2 Q0^2/(2-K_B)")
print("="*92)
print(r"""
  AeST scalar has a SHIFT symmetry phi -> phi + const => a conserved shift current J^mu,
  whose background time-component is the shift charge Q ≡ J^0. In FLRW the homogeneous scalar
  rolls as phi_bg(t) with phidot_bg = Q0 set by this charge (Skordis-Zlosnik 2021 eq for the
  shift charge; Verwayen-Skordis-Zlosnik 2024 sec 2). The DARK-ENERGY MIMICRY branch is the
  one where the scalar's stress-energy acts as Lambda: its energy density is ~ rho_DE, i.e.
       rho_phi,bg ~ rho_DE = Lambda c^2/(8 pi G) = OL rho_crit,0.
  The mass term is mu^2 = 2 K2 Q0^2/(2-K_B): mu is SET BY the same background charge Q0 that
  drives the DE mimicry. We do NOT need {K2,K_B,Q0} separately -- AeST FIXES the combination
  via the CMB to 1/mu ~ 1 Mpc (the only banked constraint). The KEY background OUTPUT we need
  is not Q0 itself but the background scalar POTENTIAL AMPLITUDE, i.e. the depth of the
  cosmological gravitational potential well the cluster perturbation must match.
""")
# The background DE potential the AeST scalar mimics is the de Sitter potential.
# In the Newtonian gauge a constant-Lambda background gives Phi_bg(r) = -(1/6) Lambda c^2 r^2
# (the de Sitter / repulsive potential), the SAME quadratic the AeST scalar reproduces.
rho_DE   = Lambda_OL*c**2/(8.0*np.pi*G_N)        # kg/m^3  (use OL-Lambda for rho_crit consistency)
rho_DE_a0= Lambda*c**2/(8.0*np.pi*G_N)
rho_crit0= 3.0*H0**2/(8.0*np.pi*G_N)
print(f"  rho_crit,0   = {rho_crit0:.3e} kg/m^3")
print(f"  rho_DE(OL)   = {rho_DE:.3e} kg/m^3   (= OL rho_crit,0, check OL={rho_DE/rho_crit0:.3f})")
print(f"  rho_DE(a0)   = {rho_DE_a0:.3e} kg/m^3 (from Lambda(a0); ratio to OL-version {rho_DE_a0/rho_DE:.3f})")
# the background scalar's coherence scale is 1/mu (CMB-pinned) -- this is ALSO the scale over
# which the cosmological scalar potential is correlated. The DE potential well over a region
# of size L has depth ~ (1/6) Lambda c^2 L^2.

# =====================================================================================
# STEP 4 (compute first; STEP 2/3 use it).  TURNAROUND RADIUS r_ta(M500, z)
# =====================================================================================
print("\n" + "="*92)
print("STEP 4 -- turnaround radius r_ta(M500,z): where the cluster overdensity meets the mean field")
print("="*92)
print(r"""
  The matching radius is the cluster EDGE = the turnaround radius r_ta, where the infalling
  shell decouples from the Hubble flow and the cluster mean density equals the turnaround
  overdensity. Spherical collapse with Lambda: at turnaround the mean enclosed density is
       rho_ta = zeta * rho_m(z),  zeta ~ 5.6 (EdS) ... ~ few (Lambda-modified),
  and the collapsed virial radius R500 sits well inside. Equivalently r_ta is fixed by
       M500 = (4/3) pi r_ta^3 * Delta_ta * rho_crit(z),  Delta_ta ~ 5-6 x Om (vs 500 for R500).
  The RATIO r_ta/R500 = (500/Delta_ta_crit)^{1/3} is the SAME for all clusters (structural).
""")
z   = 0.3
Ez2 = Om*(1+z)**3 + OL
Hz  = H0*np.sqrt(Ez2)
rho_crit_z = 3.0*Hz**2/(8.0*np.pi*G_N)
rho_m_z    = Om*(1+z)**3*rho_crit0
# turnaround overdensity wrt rho_crit(z): EdS gives ~5.55*Om(z) ... use the standard
# Delta_ta ~ 5.5 * rho_m = 5.5*Om(z)*rho_crit_z; Om(z):
Omz = Om*(1+z)**3/Ez2
Delta_ta_crit = 5.55*Omz       # turnaround density / rho_crit(z) (spherical collapse w/ Lambda ~ 4-6)
def R500_of(M500):
    return (M500/((4.0/3.0)*np.pi*500.0*rho_crit_z))**(1.0/3.0)
def r_ta_of(M500):
    return (M500/((4.0/3.0)*np.pi*Delta_ta_crit*rho_crit_z))**(1.0/3.0)
ratio_ta = (500.0/Delta_ta_crit)**(1.0/3.0)
print(f"  z={z}: E(z)^2={Ez2:.3f}, Om(z)={Omz:.3f}, rho_crit(z)={rho_crit_z:.3e}, rho_m(z)={rho_m_z:.3e}")
print(f"  Delta_ta/rho_crit(z) = {Delta_ta_crit:.2f}  ->  r_ta/R500 = (500/Delta_ta)^(1/3) = {ratio_ta:.2f} (SAME for all M)")
masses = [1e14, 3e14, 5e14, 1e15]
print(f"\n  {'M500[Msun]':>12} {'R500[Mpc]':>10} {'r_ta[Mpc]':>10} {'r_ta/R500':>10} {'(mu r_ta)':>10} {'(mu r_ta)^2':>12}")
mu = 1.0/Mpc
for M in masses:
    M500 = M*Msun; R5 = R500_of(M500); rta = r_ta_of(M500)
    print(f"  {M:>12.0e} {R5/Mpc:>10.3f} {rta/Mpc:>10.3f} {rta/R5:>10.3f} {mu*rta:>10.3f} {(mu*rta)**2:>12.3f}")

# =====================================================================================
# STEP 2-3.  THE MATCHING CONDITION + chi_out = -Phi_cosmo(r_ta)
# =====================================================================================
print("\n" + "="*92)
print("STEP 2-3 -- matching condition: chi_out = background cosmological scalar potential at r_ta")
print("="*92)
print(r"""
  MATCHING. The weak-field scalar potential Phi entering the cluster RAR is measured RELATIVE
  to the cosmological mean. At the cluster edge r_ta the perturbation field must join smoothly
  onto the cosmological background scalar -- the same field whose stress-energy is the DE the
  AeST scalar mimics. So the surviving Helmholtz constant chi_out is NOT zero; it equals the
  background cosmological scalar potential at the matching radius:
        chi_out = Phi_cosmo(r_ta).
  Two equivalent estimators of Phi_cosmo(r_ta) (both run; they bracket the answer):
    (A) de Sitter / DE background potential:  Phi_Lambda(r) = -(1/6) Lambda c^2 r^2
        (the repulsive cosmological-constant potential the scalar reproduces).
    (B) mean-matter Newtonian potential the cluster decoupled from:
        Phi_mean(r_ta) = -(1/2)(4pi/3) G rho_m(z) r_ta^2  (the cosmic-mean well at turnaround).
  At turnaround these coincide up to O(1): rho_collapse(r_ta) ~ rho_m(z), and r_ta is the
  Lambda/matter crossover, so |Phi_Lambda(r_ta)| ~ |Phi_mean(r_ta)|. The SAME prescription,
  set by {Lambda, rho_m(z), r_ta/R500} -- all cosmological, none per-cluster.
""")
def Phi_Lambda(r):     # de Sitter background potential the scalar mimics
    return -(1.0/6.0)*Lambda*c**2*r**2
def Phi_Lambda_a0(r):
    return -(1.0/6.0)*Lambda*c**2*r**2     # Lambda already from a0 path? we used Lambda(a0)=Lambda above
def Phi_mean(r):       # mean-matter Newtonian potential at radius r (cosmic mean at z)
    return -0.5*(4.0*np.pi/3.0)*G_N*rho_m_z*r**2
# NOTE: Lambda defined above is Lambda(a0). For the DE potential the physically-mimicked one
# is the cosmological Lambda_OL; compute BOTH and bracket.
def Phi_Lambda_OL(r):
    return -(1.0/6.0)*Lambda_OL*c**2*r**2

print(f"  {'M500[Msun]':>12} {'r_ta[Mpc]':>9} {'-PhiLam(a0)':>13} {'-PhiLam(OL)':>13} {'-Phi_mean':>13} {'[(km/s)^2 units]':>2}")
chi_table = {}
for M in masses:
    M500 = M*Msun; rta = r_ta_of(M500)
    pL_a0 = -Phi_Lambda(rta); pL_OL = -Phi_Lambda_OL(rta); pM = -Phi_mean(rta)
    chi_table[M] = dict(rta=rta, PhiLam_a0=Phi_Lambda(rta), PhiLam_OL=Phi_Lambda_OL(rta),
                        Phi_mean=Phi_mean(rta))
    print(f"  {M:>12.0e} {rta/Mpc:>9.3f} {pL_a0/1e6:>13.3e} {pL_OL/1e6:>13.3e} {pM/1e6:>13.3e}")
print("   (units: (m/s)^2 /1e6 = (km/s)^2.  |Phi| ~ (10^3 km/s)^2 = 1e12 (m/s)^2 = cluster well depth)")

# reference cluster well depth for scale: a 5e14 cluster's MOND potential ~ v_c^2 ~ (1000 km/s)^2
v_c2_ref = (1000e3)**2
print(f"\n  Reference cluster potential depth v_c^2 ~ (1000 km/s)^2 = {v_c2_ref:.3e} (m/s)^2")
for M in [5e14]:
    d = chi_table[M]
    print(f"  5e14: -Phi_Lambda(OL)(r_ta) = {-d['PhiLam_OL']:.3e} (m/s)^2 = {-d['PhiLam_OL']/v_c2_ref:.4f} v_c^2")
    print(f"        -Phi_mean(r_ta)       = {-d['Phi_mean']:.3e} (m/s)^2 = {-d['Phi_mean']/v_c2_ref:.4f} v_c^2")

# =====================================================================================
# STEP 5a.  IS chi_out UNIVERSAL?  (does it hide a per-cluster knob?)
# =====================================================================================
print("\n" + "="*92)
print("STEP 5a -- universality test: chi_out's M500 dependence (knob in disguise?)")
print("="*92)
print(r"""
  chi_out = Phi_cosmo(r_ta) and r_ta ~ M500^{1/3} (since M500 = (4/3)pi Delta rho_crit r_ta^3).
  So Phi_cosmo(r_ta) ~ r_ta^2 ~ M500^{2/3}: chi_out is NOT a single number -- it SCALES with
  cluster mass. That is the honest catch. BUT it is a FIXED FUNCTION of M500 (one prescription:
  chi_out(M500) = -(1/6)Lambda c^2 r_ta(M500)^2), NOT a free per-object parameter. The question
  for closure is whether THIS fixed mass-scaling gives the FLAT eta~2.15 eRASS1 sees, or the
  wrong trend.
""")
lgM = np.log10(masses)
chi_OL  = np.array([-chi_table[M]['PhiLam_OL'] for M in masses])
chi_mean= np.array([-chi_table[M]['Phi_mean'] for M in masses])
sl_OL  = np.polyfit(lgM, np.log10(chi_OL), 1)[0]
sl_mn  = np.polyfit(lgM, np.log10(chi_mean),1)[0]
print(f"  d log10(chi_out) / d log10(M500)  =  {sl_OL:.3f} (DE)   {sl_mn:.3f} (mean)   [expect 2/3={2/3:.3f}]")
print("  => chi_out RISES with M500 as M^(2/3). It is a UNIVERSAL FUNCTION, not a per-cluster tune,")
print("     but it is mass-DEPENDENT. eRASS1 eta is FLAT in M500 -- this scaling is a testable hook.")

# =====================================================================================
# STEP 5b.  FEED chi_out INTO THE FULL NONLINEAR SOLVER -> eta(R500)
# =====================================================================================
print("\n" + "="*92)
print("STEP 5b -- feed cosmologically-fixed chi_out into the full nonlinear Helmholtz solver -> eta(R500)")
print("="*92)

def Mfunc(x):
    s = np.sqrt(1.0+4.0*x); return (s-1.0)/(s+1.0)
def u_from_flux(F, r):
    if r == 0.0: return 0.0
    f = abs(F)/(a0*r*r); u = a0*(np.sqrt(f)+f); return np.sign(F)*u

class Cluster:
    def __init__(self, M500, R500, f_gas500=0.125, f_star500=0.012,
                 rc_over_R500=0.18, beta=2.0/3.0, a_star_kpc=30.0):
        self.M500=M500; self.R500=R500; self.beta=beta; self.rc=rc_over_R500*R500
        self.a_star=a_star_kpc*kpc; self.M_star=f_star500*M500
        Ig=self._gas_shape_mass(R500); self.rho_g0=f_gas500*M500/Ig
    def _gas_shape_mass(self,R):
        rr=np.linspace(0.0,R,40000)
        return np.trapz(4*np.pi*rr**2*(1+(rr/self.rc)**2)**(-1.5*self.beta), rr)
    def rho_b(self,r): return self.rho_g0*(1+(r/self.rc)**2)**(-1.5*self.beta)
    def M_gas(self,r):
        rr=np.linspace(0.0,r,4000)
        return np.trapz(4*np.pi*rr**2*self.rho_g0*(1+(rr/self.rc)**2)**(-1.5*self.beta), rr)
    def M_star_lt(self,r): return self.M_star*r**2/(r+self.a_star)**2
    def M_bar(self,r): return self.M_gas(r)+self.M_star_lt(r)
    def g_bar(self,r): return G_N*self.M_bar(r)/r**2

def rhs(r,y,mu2,rho_b_func):
    Phi,F=y; u=u_from_flux(F,r)
    return [u, r*r*(4*np.pi*G_N*rho_b_func(r)-mu2*Phi)]
def _Mbar_func(rho_b_func,r):
    rr=np.linspace(0.0,r,2000)
    return np.trapz(4*np.pi*rr**2*np.array([rho_b_func(x) for x in rr]), rr)
def integrate_outward(Phi_c,mu,rho_b_func,r0,r_max,n_eval=4000):
    mu2=mu*mu; F0=G_N*_Mbar_func(rho_b_func,r0)
    r_eval=np.linspace(r0,r_max,n_eval)
    return solve_ivp(rhs,[r0,r_max],[Phi_c,F0],args=(mu2,rho_b_func),t_eval=r_eval,
                     rtol=1e-10,atol=1e-12,method='DOP853',dense_output=True,
                     max_step=(r_max-r0)/2000.0)
def g_MOND(cl,r):
    gN=G_N*cl.M_bar(r)/r**2; f=gN/a0; return a0*(f+np.sqrt(f))
def g_AeST(sol,r):
    Phi,F=sol.sol(r); return abs(u_from_flux(F,r))

def shoot_to_chiout(mu, cl, chi_out, r0=2.0*kpc, r_max=None,
                    Phic_lo_log=9.0, Phic_hi_log=13.5):
    """
    PHYSICAL BC = the COSMOLOGICAL MATCHING value chi_out imposed at r_ta:
       Phi(r_ta) = chi_out   (the background-fixed boundary value).
    We shoot the central Phi_c so that the integrated Phi(r_ta) equals chi_out. This is the
    Route-A boundary condition (replaces the degenerate envelope-min/Phi(inf)->0). chi_out is
    NEGATIVE (a potential well); we bisect on Phi(r_ta)-chi_out.
    Integrate only to ~1.2*r_ta (no need for 30 Mpc -- the BC is AT r_ta).
    """
    r_ta = r_ta_of(cl.M500)
    r_end = 1.15*r_ta
    rho = cl.rho_b
    F0 = G_N*_Mbar_func(rho, r0)
    mu2 = mu*mu
    def Phi_at_rta(log10_absPhic):
        Phi_c = -10.0**log10_absPhic
        sol = solve_ivp(rhs,[r0,r_end],[Phi_c,F0],args=(mu2,rho),
                        rtol=1e-9,atol=1e-11,method='DOP853',dense_output=True,
                        max_step=(r_end-r0)/1500.0)
        if not sol.success: return None
        return sol.sol(r_ta)[0]
    los, his = Phic_lo_log, Phic_hi_log
    target = chi_out
    g = lambda L: (Phi_at_rta(L) - target)
    Ls = np.linspace(los, his, 24); gs = np.array([ (lambda v: np.nan if v is None else v-target)(Phi_at_rta(L)) for L in Ls])
    root = None
    for i in range(len(Ls)-1):
        if np.isfinite(gs[i]) and np.isfinite(gs[i+1]) and gs[i]*gs[i+1] < 0:
            root = brentq(g, Ls[i], Ls[i+1], xtol=1e-4); break
    if root is None:
        res = minimize_scalar(lambda L: abs(g(L)) if np.isfinite(g(L) or np.nan) else 1e300,
                              bounds=(los,his), method='bounded', options={'xatol':1e-4})
        root = res.x
    Phi_c = -10.0**root
    sol = solve_ivp(rhs,[r0,r_end],[Phi_c,F0],args=(mu2,rho),
                    rtol=1e-9,atol=1e-11,method='DOP853',dense_output=True,
                    max_step=(r_end-r0)/3000.0)
    return sol, Phi_c, r_ta

print("  Imposing Phi(r_ta) = chi_out = Phi_cosmo(r_ta), for each estimator of chi_out:")
print(f"\n  {'M500':>10} {'chi_out_used':>14} {'estimator':>10} {'g_bar/a0':>9} {'eta(R500)':>10}")
results_eta = {}
for est_name, est_func in [('DE/Lambda', Phi_Lambda_OL), ('mean', Phi_mean)]:
    etas=[]
    for M in masses:
        M500=M*Msun; R5=R500_of(M500); cl=Cluster(M500,R5,
              f_gas500=0.09+0.06*(np.log10(M)-14.0)/1.0, f_star500=0.012)
        rta=r_ta_of(M500); chi_out=est_func(rta)
        sol,Phi_c,_=shoot_to_chiout(mu, cl, chi_out)
        if sol is None:
            print(f"  {M:>10.0e} {chi_out/1e6:>13.3e}k {est_name:>10}  -- solve failed"); etas.append(np.nan); continue
        eta=g_AeST(sol,R5)/g_MOND(cl,R5); etas.append(eta)
        print(f"  {M:>10.0e} {chi_out:>14.3e} {est_name:>10} {cl.g_bar(R5)/a0:>9.3f} {eta:>10.4f}")
    results_eta[est_name]=np.array(etas)
    sl=np.polyfit(lgM, np.array(etas), 1)[0]
    print(f"     -> d eta/d log10(M500) = {sl:+.3f}  (eRASS1: ~flat at eta~2.15, slope~-0.03)")

# =====================================================================================
# STEP 5c.  BOTH WAYS -- what chi_out would 2.15 require, vs what cosmology gives
# =====================================================================================
print("\n" + "="*92)
print("STEP 5c -- BOTH WAYS: the chi_out that 2.15 NEEDS vs the chi_out cosmology DELIVERS")
print("="*92)
# For the 5e14 cluster, scan chi_out and read eta(R500); find chi_out giving eta=2.15.
M=5e14; M500=M*Msun; R5=R500_of(M500)
cl=Cluster(M500,R5,f_gas500=0.09+0.06*(np.log10(M)-14.0)/1.0,f_star500=0.012)
rta=r_ta_of(M500)
chi_cosmo_OL = Phi_Lambda_OL(rta)
chi_cosmo_mn = Phi_mean(rta)
print(f"  5e14: r_ta={rta/Mpc:.2f} Mpc; cosmology gives chi_out(DE)={chi_cosmo_OL:.3e}, chi_out(mean)={chi_cosmo_mn:.3e}")
print(f"\n  scanning chi_out -> eta(R500):")
print(f"  {'chi_out [(m/s)^2]':>20} {'chi_out/v_c^2':>14} {'eta(R500)':>10}")
scan_vals = -np.array([1e9,1e10,3e10,1e11,3e11,1e12,3e12,1e13])
eta_scan=[]
for ch in scan_vals:
    sol,_,_=shoot_to_chiout(mu, cl, ch)
    if sol is None: eta_scan.append(np.nan); continue
    e=g_AeST(sol,R5)/g_MOND(cl,R5); eta_scan.append(e)
    print(f"  {ch:>20.3e} {ch/v_c2_ref:>14.4f} {e:>10.4f}")
eta_scan=np.array(eta_scan)
# find chi_out for eta=2.15 by interpolation where monotone
print(f"\n  cosmological chi_out (DE)   = {chi_cosmo_OL:.3e} = {chi_cosmo_OL/v_c2_ref:.4f} v_c^2")
print(f"  cosmological chi_out (mean) = {chi_cosmo_mn:.3e} = {chi_cosmo_mn/v_c2_ref:.4f} v_c^2")
# eta at the cosmological chi_out:
for nm,ch in [('DE',chi_cosmo_OL),('mean',chi_cosmo_mn)]:
    sol,_,_=shoot_to_chiout(mu, cl, ch)
    e=g_AeST(sol,R5)/g_MOND(cl,R5) if sol is not None else np.nan
    print(f"  => eta(R500) at cosmological chi_out({nm}) = {e:.4f}")

print("\n" + "="*92)
print("END ROUTE A SOLVE. Verdict assembled by the wrapper.")
print("="*92)
