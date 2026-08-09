#!/usr/bin/env python3
"""
MECHANISM 2: can the AeST Q-sector's conserved SHIFT CHARGE cluster gravitationally?

Question assigned: the dust AMOUNT I_0 is a conserved shift charge (already established,
robustly free).  This script asks about its SPATIAL DISTRIBUTION: does the charge density
get advected and concentrated under the collapse of ordinary matter, and what fractional
CDM-level clustering xi does that imply in a galaxy and in a cluster?

Framework premises used (NOT re-derived here):
  a0 = kappa c sqrt(G rho_Lambda) = c H_Lambda / Z = 9.3619e-11 m/s^2, kappa = 1/2,
  Route A kernel nu(y) = 1/(1 - exp(-sqrt(y))), y = g_bar/a0.
  Relativistic completion: AeST (Skordis & Zlosnik 2021, PRL 127:161302), free function
  Fcal(Y,Q), Q = A^mu grad_mu phi, Y = q^{mu nu} grad_mu phi grad_nu phi.
  Q-sector = ghost condensate (Arkani-Hamed, Cheng, Luty, Mukohyama 2004, JHEP 0405:074).

LOAD-BEARING RESULTS (each printed with its own numbers below):
  B1  shift symmetry phi -> phi + c gives j^mu; charge density n = Fcal_Q/(8 pi G),
      flux from the Y-sector; FRW conservation gives n ~ a^-3 (the dust).
  B2  ANY smooth K(Q) with a minimum of order N gives a BAROTROPIC fluid p = K_poly rho^gamma
      with gamma = N/(N-1) EXACTLY.  N=2 (generic quadratic) => gamma = 2.
  B3  the Jeans wavenumber is k_J = sqrt(4 pi G rho)/c_s ~ rho^{(2-gamma)/2}.
      gamma = 2 is the unique DENSITY-INDEPENDENT case, k_J = mu; the self-gravitating
      equilibrium is the n=1 Lane-Emden polytrope of MASS-INDEPENDENT radius R = pi/mu,
      and that equation IS the AeST quasistatic Helmholtz term.  Compression-proof.
  B4  fuzzy dark matter has k_J ~ rho^{1/4} (compression makes it cluster).  The ghost
      condensate at gamma = 2 does not.  This is the real structural difference.
  B5  the k^4 branch is irrelevant above ~millimetres; the k^2 polytropic term supersedes it.
  B6  hydrostatic response rho_c(|Phi|) and the resulting xi.
  B7  gamma = 2 normalised on clusters: mu^-1 = 1.4-2.1 Mpc, xi_gal ~ 1e-5.  Then the CMB
      cannot cluster:  fails by ~1e9 in c_s^2.
  B8  gamma = 2 normalised on the CMB: mu^-1 <~ 0.1 kpc, and then xi_gal >> 1 -- an
      overshoot WORSE than the context's item-4 estimate.
  B9  scan over N: the ONLY window is N >~ 4 (K vanishing quartically or faster at its
      minimum), optimum at N = 4 (gamma = 4/3).  Even there the implied matter-power-
      spectrum cutoff sits at k_crit ~ 0.1-0.2 Mpc^-1, i.e. inside the linear data.
  B10 timescales: t_sound/t_dyn = mu R exactly; a CDM-level condensate overdensity in a
      galaxy is over-pressured and re-expands in ~(mu R) dynamical times.
"""
import numpy as np
import sympy as sp

# ---------------- constants (SI unless stated) ----------------
G      = 6.67430e-11
c      = 2.99792458e8
Mpc    = 3.0856776e22
kpc    = 3.0856776e19
pc     = 3.0856776e16
Msun   = 1.98892e30
H0     = 67.4e3/Mpc
rho_cr = 3*H0**2/(8*np.pi*G)
Om_m, Om_dm, Om_L, Om_r = 0.315, 0.265, 0.685, 9.24e-5
rho_dm0 = Om_dm*rho_cr
hbar_eVs, hbarc_eVm = 6.582119569e-16, 1.9733e-7
MPl_red_eV = 2.435e27

def hdr(s): print("\n" + "="*78 + "\n" + s + "\n" + "="*78)

# =====================================================================
hdr("BLOCK 1 -- shift symmetry, Noether current, conserved charge")
# =====================================================================
print("""
  phi enters Fcal(Y,Q) ONLY through grad phi   (Q = A.grad phi, Y = q^{ab} grad_a phi grad_b phi),
  so the action has the EXACT global symmetry  phi -> phi + const.
  Noether current (AeST normalisation: Fcal sits inside the 1/16 pi G bracket, so the
  Skordis-Zlosnik relation 8 pi G rho_0 = Q_0 I_0 fixes the 8 pi G):

      j^mu = -sqrt(-g)/(8 pi G) * [ Fcal_Q A^mu  +  2 Fcal_Y q^{mu nu} grad_nu phi ]
      grad_mu ( Fcal_Q A^mu + 2 Fcal_Y q^{mu nu} grad_nu phi ) = 0      (EXACT)

  charge density in the aether frame:  n = Fcal_Q /(8 pi G)          [aether-parallel piece]
  charge FLUX                       :  f^i = 2 Fcal_Y q^{i nu} grad_nu phi /(8 pi G)
                                           = n v^i  with  v^i = 2 Fcal_Y grad^i phi / Fcal_Q

  ==> the shift charge IS advected: it obeys d_t n + div(n v) = 0.  There is no structural
      exemption from concentration.  But v^i is a GRADIENT: the flow is IRROTATIONAL and
      SINGLE-VALUED.  No multistreaming, no velocity dispersion, hence no violent relaxation.
      The only equilibrium available is HYDROSTATIC, supported by p(rho).  That is the whole
      difference from CDM, and it is a difference of support mechanism, not of advectability.
""")
t, a = sp.symbols('t a', positive=True)
Qs = sp.Function('Q')(t); af = sp.Function('a')(t); K = sp.Function('K')
phi = sp.Function('phi')(t)
L = af**3 * (-K(sp.diff(phi, t)))                 # homogeneous: Y = 0, Q = phidot
eom = sp.simplify(sp.diff(sp.diff(L, sp.diff(phi, t)), t))
print("  homogeneous EOM  d/dt[ a^3 K'(Qdot) ] =", sp.simplify(eom), " ==> a^3 K'(Q) = I_0 = const")
print("  so  n = K'(Q)/(8 pi G) = I_0/(8 pi G a^3)  ~ a^-3   : DUST, amount = the shift charge.")

# =====================================================================
hdr("BLOCK 2 -- K(Q) with an order-N minimum  ==>  p = K_poly rho^gamma, gamma = N/(N-1)")
# =====================================================================
eps, N = sp.symbols('varepsilon N', positive=True)
Kf = eps**N                                        # K = (Q - Q0)^N up to normalisation, Q0 = 1
Kp = sp.diff(Kf, eps)
rho_s = sp.simplify((1+eps)*Kp - Kf)               # rho = (Q Fcal_Q - Fcal)/(8 pi G), Q0 = 1
p_s   = Kf                                         # p   = Fcal /(8 pi G)
rho_lead = sp.simplify(sp.series(rho_s, eps, 0, N+1).removeO())
print("  rho(eps) =", sp.expand(rho_s), "   leading:", N, "* eps^(N-1)")
print("  p(eps)   =", p_s)
gam = sp.simplify(sp.log(p_s)/sp.log(N*eps**(N-1)))
print("  eliminating eps at leading order:  p ~ rho^gamma with gamma = N/(N-1)")
for Nv in [2,3,4,5,6,8,100]:
    print(f"    N = {Nv:4d}  ->  gamma = {Nv/(Nv-1):.4f}   (polytrope index n = 1/(gamma-1) = {Nv-1})")
print("""
  N = 2 is the GENERIC case (any smooth K with K''(Q0) != 0), and it reproduces ACLMW 2007
  eq 3.15 exactly:  p = rho^2/(2 M^4)  with  M^4 = Q0^2 K''(Q0),  equivalently
  mu^2 = 4 pi G M^4 / c^4 x c^2 ... in the SI form used below:  p = 2 pi G rho^2 / mu^2,
  c_s^2 = 4 pi G rho / mu^2,  w = p/(rho c^2) = 2 pi G rho/(mu^2 c^2) = eps/2.
  Sanity: with K = mu^2 (Q-1)^2 (Blanchet & Skordis 2024 eq 2.7) rho = mu^2 eps c^2/(4 pi G).
""")

# =====================================================================
hdr("BLOCK 3 -- Jeans scale;  gamma = 2 is the unique compression-proof case")
# =====================================================================
print("""
  barotropic p = K_poly rho^gamma  =>  c_s^2 = gamma K_poly rho^(gamma-1)
      k_J = sqrt(4 pi G rho)/c_s  ~  rho^{(2-gamma)/2}
  gamma = 2  =>  k_J INDEPENDENT of rho.  With K_poly = 2 pi G/mu^2:  k_J = mu exactly.
  Self-gravitating equilibrium (hydrostatic + Poisson) for gamma = 2:
      grad(2 K rho) = -grad Phi ,  lap Phi = 4 pi G rho   =>  lap rho + (2 pi G/K) rho = 0
      =>  lap rho + mu^2 rho = 0   (HELMHOLTZ)  =>  rho = rho_0 sin(mu r)/(mu r),
      first zero at mu R = pi  =>  R_TF = pi/mu, INDEPENDENT OF MASS.
  IDENTITY worth logging: that is literally the AeST quasistatic equation
      lap Phi + mu^2 Phi = 4 pi G rho_b        (Durakovic & Skordis 2024 eq 2.33)
  with rho_c = -mu^2 Phi/(4 pi G) (= Mistele+2023 eq 2).  So AeST's 'mass term' IS the
  n=1 polytropic self-gravity of the shift charge in hydrostatic equilibrium.  The
  Durakovic-Skordis ASSUMPTION 'Q -> Q0 up to small fluctuations' is exactly the statement
  that the shift charge is hydrostatic rather than virialised.
""")
r = sp.symbols('r', positive=True); mu_s = sp.symbols('mu', positive=True)
prof = sp.sin(mu_s*r)/(mu_s*r)
lap = sp.simplify(sp.diff(r**2*sp.diff(prof, r), r)/r**2)
print("  check Lane-Emden n=1: lap[sin(mu r)/(mu r)] + mu^2 [.] =", sp.simplify(lap + mu_s**2*prof))
for mui_Mpc in [0.22e-3, 1.0, 1.55, 2.0]:
    mu = 1.0/(mui_Mpc*Mpc)
    print(f"    mu^-1 = {mui_Mpc:9.5f} Mpc  ->  lambda_J = 2pi/mu = {2*np.pi/mu/Mpc:9.4f} Mpc,"
          f"  R_TF = pi/mu = {np.pi/mu/Mpc:9.4f} Mpc")

# =====================================================================
hdr("BLOCK 4 -- head-on comparison with FUZZY dark matter")
# =====================================================================
print("""
  FDM is also a coherent scalar with irrotational potential flow, and it DOES cluster.
  Why: its support is the QUANTUM pressure, effective c_s^2(k) = hbar^2 k^2/(4 m^2), which is
  INDEPENDENT of rho.  Hence k_J = (16 pi G rho m^2/hbar^2)^{1/4} ~ rho^{1/4}: compression
  RAISES k_J, the Jeans scale SHRINKS, and collapse runs away (solitons + CDM-like envelope).
  The ghost condensate off its minimum is NOT that fluid.  Its support is a SELF-INTERACTION,
  p ~ rho^2 -- i.e. it is BEC/self-interacting scalar dark matter in the THOMAS-FERMI limit,
  for which the mass-independent radius R = pi sqrt(K/(2 pi G)) is textbook
  (Goodman 2000 New Astron 5:103; Peebles 2000 ApJ 534:L127; Boehmer & Harko 2007 JCAP 06:025;
   Chavanis 2011 PRD 84:043531; Rindler-Daller & Shapiro 2012 MNRAS 422:135).
  k_J ~ rho^{(2-gamma)/2}:  gamma=2 -> rho^0 (compression-proof), gamma=3/2 -> rho^{1/4}
  (EXACTLY the FDM scaling), gamma->1 -> rho^{1/2} (isothermal, clusters most easily).
  So the FDM counterexample transfers only for gamma <= 3/2, and NOT at the generic gamma = 2.
""")
# effective FDM mass that reproduces the pure k^4 branch, for the record
M_nat_eV = ((Om_L*rho_cr)*c**2/1.602176634e-19*hbarc_eVm**3)**0.25
m_eff_eV = M_nat_eV/2.0
lam_dB = 2*np.pi*hbar_eVs*c**2/(m_eff_eV*2.0e5)     # hbar/(m v), v = 200 km/s
print(f"  If one insisted on the pure k^4 branch: omega = c k^2/k_M matches FDM omega = hbar k^2/2m")
print(f"  with m_eff c^2 = M/2.  At the natural M = rho_L^1/4 = {M_nat_eV*1e3:.3f} meV that is")
print(f"  m_eff = {m_eff_eV:.4e} eV, {m_eff_eV/2e-20:.2e} x the Lyman-alpha FDM floor 2e-20 eV")
print(f"  (Rogers & Peiris 2021 PRL 126:071302), de Broglie wavelength at 200 km/s = {lam_dB:.2f} m.")
print("  AGAINST INTEREST: on the k^4 branch alone the condensate is FDM with a metre-scale")
print("  de Broglie wavelength, i.e. indistinguishable from CDM.  Item 2 of the brief is right.")

# =====================================================================
hdr("BLOCK 5 -- the k^4 branch is superseded by the k^2 branch above ~millimetres")
# =====================================================================
print("""
  full dispersion of a condensate DISPLACED off the minimum (rho != 0 <=> eps != 0 <=> Fcal_Q != 0):
      omega^2 = c_s^2 k^2 + c^2 k^4/k_M^2 - 4 pi G rho ,      c_s^2 = gamma K_poly rho^(gamma-1)
  crossover k_x = k_M c_s/c.  Below is k_x for the mu^-1 that clusters require (Block 7).
""")
def M_from_mu(mu_inv_m):
    """ACLMW/AeST map M^2 = sqrt(2) mu MPl (c=hbar=1); returns M in eV."""
    mu_eV = (1.0/mu_inv_m)*hbarc_eVm
    return np.sqrt(np.sqrt(2)*mu_eV*MPl_red_eV)
for mui_Mpc, eps_lab, epsv in [(1.55, "cluster eps ~ |Phi|/c^2", 2.0e-5),
                               (1.55, "galaxy  eps ~ |Phi|/c^2", 5.4e-7)]:
    M_eV = M_from_mu(mui_Mpc*Mpc); kM = M_eV/hbarc_eVm
    kx = kM*np.sqrt(epsv)
    print(f"  mu^-1={mui_Mpc} Mpc -> M={M_eV:.4f} eV, k_M={kM:.3e} 1/m ; {eps_lab}={epsv:.2e}"
          f" -> k_x={kx:.3e} 1/m, lambda_x={2*np.pi/kx*1e3:.3f} mm")
print("  ==> the k^4 term matters only below ~millimetres.  It is NOT the operative physics at")
print("      galaxy or cluster scales.  CORRECTION TO THE BRIEF'S ITEMS 1-3: the leading")
print("      dispersion is k^2, not k^4, whenever rho != 0, because rho != 0 means Fcal_Q != 0")
print("      means the gradient term is present.  Item 3's 'in LINEAR theory xi = 1' does NOT")
print("      follow from the k^4 Jeans scale.")

# =====================================================================
hdr("BLOCK 6 -- systems, potentials, and the hydrostatic response rho_c(|Phi|)")
# =====================================================================
def system(M500_Msun=None, R_m=None, vc=None, label=""):
    if vc is None:
        vc = np.sqrt(G*M500_Msun*Msun/R_m)
    rho_dyn = 3*vc**2/(4*np.pi*G*R_m**2)     # mean dynamical density inside R
    return dict(label=label, R=R_m, vc=vc, rho_dyn=rho_dyn)

A_LOG = 1.0     # |Phi| = A_LOG * vc^2 ; A_LOG = 1 fiducial, 2.3 variant reported below
CLU = system(M500_Msun=5.0e14, R_m=1.2*Mpc, label="cluster M500=5e14, R500=1.2 Mpc")
GAL20  = system(vc=220e3, R_m=20*kpc,  label="MW-like spiral, R = 20 kpc")
GAL100 = system(vc=220e3, R_m=100*kpc, label="MW-like spiral, R = 100 kpc")
DWARF  = system(vc=40e3,  R_m=5*kpc,   label="LSB dwarf, vc=40 km/s, R = 5 kpc")
for s in [CLU, GAL20, GAL100, DWARF]:
    print(f"  {s['label']:42s} vc={s['vc']/1e3:7.1f} km/s  |Phi|/c^2={A_LOG*s['vc']**2/c**2:.3e}"
          f"  rho_dyn={s['rho_dyn']:.4e} kg/m^3")
print("""
  hydrostatic equilibrium of a barotrope in an external+self potential of depth |Phi|
  (zero point at rho -> 0):   gamma K_poly rho^(gamma-1)/(gamma-1) = |Phi|
      =>  rho_c = [ (gamma-1)|Phi| / (gamma K_poly) ]^{1/(gamma-1)}   ~  |Phi|^{1/(gamma-1)}
  xi(R) == rho_c/rho_dyn.  For gamma = 2 this is exactly Mistele+2023 eq 2 / the AeST
  Helmholtz response rho_c = mu^2|Phi|/(4 pi G), i.e. xi = A (mu R)^2/3.
""")
def rho_c_of(Phi, gamma, Kp_):
    return ((gamma-1)*Phi/(gamma*Kp_))**(1.0/(gamma-1))
def Kp_from_target(Phi, gamma, rho_target):
    return (gamma-1)*Phi/(gamma*rho_target**(gamma-1))

# =====================================================================
hdr("BLOCK 7 -- gamma = 2 branch NORMALISED ON CLUSTERS")
# =====================================================================
print("  demand xi(R500) = 0.11 / 0.20 / 0.26 (the self-consistent cluster requirement)\n")
Phi_clu = A_LOG*CLU['vc']**2
for xi_t in [0.11, 0.20, 0.26]:
    rho_t = xi_t*CLU['rho_dyn']
    mu2 = 4*np.pi*G*rho_t/Phi_clu
    mu  = np.sqrt(mu2); mui = 1.0/mu
    print(f"  xi(R500)={xi_t:.2f}: mu = {mu:.4e} 1/m, mu^-1 = {mui/Mpc:.4f} Mpc, "
          f"lambda_J = {2*np.pi*mui/Mpc:.3f} Mpc")
    for s in [GAL20, GAL100, DWARF]:
        rc = mu2*A_LOG*s['vc']**2/(4*np.pi*G)
        print(f"        xi({s['label']:34s}) = {rc/s['rho_dyn']:.4e}   [(mu R)^2/3 ="
              f" {(mu*s['R'])**2/3:.4e}]")
    # cosmological failure: can k = 0.2 Mpc^-1 cluster from horizon entry?
    kcom = 0.2/Mpc
    def Ha(av): return H0*np.sqrt(Om_r*av**-4 + Om_m*av**-3 + Om_L)
    aa = np.logspace(-7, 0, 20000)
    ienter = np.argmin(np.abs(kcom - aa*Ha(aa)/c))
    a_ent = aa[ienter]
    rho_e = rho_dm0/a_ent**3
    cs2_e = 4*np.pi*G*rho_e/mu2
    print(f"        k=0.2 Mpc^-1 enters horizon at a = {a_ent:.3e} (z={1/a_ent-1:.3e});"
          f" rho_dm = {rho_e:.3e} kg/m^3")
    print(f"        c_s^2/c^2 there = {cs2_e/c**2:.4e}   (need <~ 1.6e-2 for GDM w-bounds and"
          f" for k_J > k/a)  -> FAILS by {cs2_e/c**2/1.64e-2:.3e}")
    print(f"        w = eps/2 at recombination a=1/1101: {0.5*4*np.pi*G*(rho_dm0*1101**3)/mu2/c**2:.3e}")
    print()
print("""  AGAINST INTEREST: this is Blanchet & Skordis 2024 (JCAP 11:040) section 4.3.1 in the
  variable that controls xi.  Their own statement: 'the exact functional dependence for K
  chosen in (4.12) cannot be in simultaneous harmony with observations of galaxies and with
  cosmology.'  I reproduce their mu^-1 <~ 0.22 kpc below and the conflict is ~1e3 in mu^-1,
  ~1e6-1e9 in xi.""")
# reproduce Blanchet-Skordis 0.22 kpc: eps(a=1e-5) = 1
for a_star, eps_max, tag in [(1e-5, 1.0, "c_ad^2 <= 1 at a = 1e-5 (Blanchet-Skordis)"),
                             (1e-4, 2*0.0164, "w <= 0.0164 at a = 1e-4 (Kopp+2018 GDM)")]:
    eps0 = eps_max*a_star**3
    mu2 = 4*np.pi*G*rho_dm0/(eps0*c**2)
    print(f"  {tag}:  eps_0 <= {eps0:.3e}  ->  mu^-1 <= {1/np.sqrt(mu2)/pc:.4g} pc")

# =====================================================================
hdr("BLOCK 8 -- gamma = 2 branch NORMALISED ON COSMOLOGY: xi >> 1 in galaxies")
# =====================================================================
for mui_pc in [55.0, 224.0, 1000.0]:
    mu2 = (1.0/(mui_pc*pc))**2
    print(f"  mu^-1 = {mui_pc:7.1f} pc :")
    for s in [GAL20, GAL100, DWARF, CLU]:
        rc = mu2*A_LOG*s['vc']**2/(4*np.pi*G)
        print(f"      xi({s['label']:42s}) = {rc/s['rho_dyn']:.4e}")
print("""  ==> on the branch cosmology allows, the condensate does not merely reach CDM level, it
      OVERSHOOTS CDM by 1e2-1e5, and the AeST potential turns oscillatory on sub-kpc scales
      (r_C = (r_M/mu^2)^{1/3}; Verwayen, Skordis & Boehm 2024 MNRAS 531:272 give r_C = 156 kpc
      at mu = 1 Mpc^-1 and 33.6 kpc at 10 Mpc^-1 -- here mu >= 4.5e3 Mpc^-1).  This is
      Mistele, McGaugh & Hossenfelder 2023 (A&A 676:A100) Table 1 in the same variable.
      The brief's item-4 overshoot (2.06x-4.42x) UNDERSTATES this branch by orders.""")

# =====================================================================
hdr("BLOCK 9 -- scan over N: is there any K that works?")
# =====================================================================
print("""  For each N (K ~ (Q-Q0)^N, gamma = N/(N-1)) normalise K_poly on xi(R500) = 0.20, then ask
  for the largest COMOVING k that is Jeans-unstable at EVERY epoch a in [a_enter, 1]:
      k_crit = min_a [ a k_J(a) ],  k_J(a) = sqrt(4 pi G rho_dm(a))/c_s(rho_dm(a))
  and report xi at galaxy radii.  Requirement: k_crit >~ 0.3 Mpc^-1 (BOSS/SDSS linear P(k)
  reaches k ~ 0.2 h/Mpc = 0.3 Mpc^-1); CMB damping tail wants at least 0.2 Mpc^-1.
""")
aa = np.logspace(-6.5, 0, 4000)
def k_crit_and_xi(Nv, xi_clu=0.20, A=A_LOG):
    gamma = Nv/(Nv-1.0)
    Phi_c = A*CLU['vc']**2
    Kp_ = Kp_from_target(Phi_c, gamma, xi_clu*CLU['rho_dyn'])
    rho_a = rho_dm0/aa**3
    cs2 = gamma*Kp_*rho_a**(gamma-1)
    kJ = np.sqrt(4*np.pi*G*rho_a)/np.sqrt(cs2)
    kcrit = np.min(aa*kJ)*Mpc                       # comoving Mpc^-1
    out = {}
    for s in [GAL20, GAL100, DWARF]:
        rc = rho_c_of(A*s['vc']**2, gamma, Kp_)
        out[s['label']] = rc/s['rho_dyn']
    # over-pressure test: c_s at CDM-level density in the galaxy vs escape speed
    cs_cdm = np.sqrt(gamma*Kp_*GAL20['rho_dyn']**(gamma-1))
    cs_cdm_clu = np.sqrt(gamma*Kp_*CLU['rho_dyn']**(gamma-1))
    return gamma, kcrit, out, cs_cdm, cs_cdm_clu
from scipy.integrate import solve_ivp
def Hofa(av): return H0*np.sqrt(Om_r*av**-4 + Om_m*av**-3 + Om_L)
def dlnH_dlna(av):
    num = -4*Om_r*av**-4 - 3*Om_m*av**-3
    return 0.5*num/(Om_r*av**-4 + Om_m*av**-3 + Om_L)

def growth_transfer(Nv, k_Mpc, xi_clu=0.20, A=A_LOG, a_i=1e-6):
    """Linear growth of the Q-sector density contrast WITH its own pressure:
         d''(x) + (2 + dlnH/dlna) d'(x) + [c_s^2 k^2/(a^2 H^2) - 4 pi G rho_dm/H^2] d = 0
       x = ln a.  Returns T(k) = delta_k(a=1)/delta_{k->0}(a=1) with identical ICs."""
    gamma = Nv/(Nv-1.0)
    Kp_ = Kp_from_target(A*CLU['vc']**2, gamma, xi_clu*CLU['rho_dyn'])
    kk = k_Mpc/Mpc
    def rhs(x, y, kv):
        av = np.exp(x); H = Hofa(av); rho = rho_dm0*av**-3
        cs2 = gamma*Kp_*rho**(gamma-1)
        d, dp = y
        return [dp, -(2 + dlnH_dlna(av))*dp - (cs2*kv**2/(av**2*H**2) - 4*np.pi*G*rho/H**2)*d]
    xs = (np.log(a_i), 0.0)
    sol_k = solve_ivp(rhs, xs, [1.0, 0.0], args=(kk,), rtol=1e-9, atol=1e-14, method='LSODA')
    sol_0 = solve_ivp(rhs, xs, [1.0, 0.0], args=(1e-6/Mpc,), rtol=1e-9, atol=1e-14, method='LSODA')
    return sol_k.y[0, -1]/sol_0.y[0, -1]

def k_at_T(Nv, Tgoal, xi_clu=0.20, A=A_LOG):
    lo, hi = 1e-3, 30.0
    if growth_transfer(Nv, lo, xi_clu, A) < Tgoal: return np.nan
    for _ in range(45):
        mid = np.sqrt(lo*hi)
        if growth_transfer(Nv, mid, xi_clu, A) > Tgoal: lo = mid
        else: hi = mid
    return np.sqrt(lo*hi)

print(f"  {'N':>5} {'gamma':>7} {'k_crit':>9} {'k(T=0.9)':>9} {'k(T=0.5)':>9} {'xi(20kpc)':>11} "
      f"{'xi(100kpc)':>11} {'cs@CDMgal/vc':>13} {'cs@CDMclu/vc':>13}")
rows = []
for Nv in [2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 8, 12, 20, 50]:
    gamma, kcrit, out, csg, csc = k_crit_and_xi(Nv)
    k90 = k_at_T(Nv, 0.9); k50 = k_at_T(Nv, 0.5)
    rows.append(dict(N=Nv, gamma=gamma, kcrit=kcrit, k90=k90, k50=k50, xi=out,
                     rg=csg/GAL20['vc'], rc=csc/CLU['vc']))
    print(f"  {Nv:5.1f} {gamma:7.4f} {kcrit:9.3e} {k90:9.4f} {k50:9.4f} {out[GAL20['label']]:11.3e} "
          f"{out[GAL100['label']]:11.3e} {csg/GAL20['vc']:13.2f} {csc/CLU['vc']:13.2f}")
print("""
  TWO INDEPENDENT REQUIREMENTS, and they pinch from opposite sides:
   (i) COSMOLOGY: k(T=0.9) must exceed ~0.3 Mpc^-1 (SDSS/BOSS linear P(k) reach 0.2 h/Mpc).
  (ii) GALAXY DRAIN: the hydrostatic xi is the attractor only if excess charge can actually
       flow out, i.e. c_s at CDM-level galaxy density must EXCEED v_c comfortably (ratio >~ 3,
       drain time <~ t_dyn/3).  Large N fails this: the hydrostatic xi ~ 1e-80 is an
       unphysical extrapolation of an isothermal-limit formula there.""")
ok = [r for r in rows if r['rg'] >= 3.0]
print(f"\n  N passing the drain test (c_s/v_c >= 3 in a MW-like galaxy): "
      f"{[r['N'] for r in ok]}")
if ok:
    b = max(ok, key=lambda r: r['k90'])
    print(f"  best k(T=0.9) inside that window: N = {b['N']} (gamma = {b['gamma']:.4f}), "
          f"k(T=0.9) = {b['k90']:.4f} Mpc^-1  (lambda = {2*np.pi/b['k90']:.1f} Mpc),"
          f" k(T=0.5) = {b['k50']:.4f} Mpc^-1")
    print(f"  SHORTFALL vs the 0.3 Mpc^-1 requirement: factor {0.3/b['k90']:.2f} in k")
print("\n  sensitivity of the N = 4 case:")
for xi_clu in [0.11, 0.20, 0.26, 0.50, 1.00]:
    g_, kc_, o_, csg_, _ = k_crit_and_xi(4.0, xi_clu=xi_clu)
    print(f"    xi(R500)={xi_clu:.2f} -> k(T=0.9) = {k_at_T(4.0,0.9,xi_clu=xi_clu):.4f} Mpc^-1, "
          f"xi(20kpc) = {o_[GAL20['label']]:.3e}, c_s/v_c(gal) = {csg_/GAL20['vc']:.2f}")
for A in [1.0, 2.3, 4.6]:
    g_, kc_, o_, csg_, _ = k_crit_and_xi(4.0, A=A)
    print(f"    |Phi|={A:.1f} vc^2  -> k(T=0.9) = {k_at_T(4.0,0.9,A=A):.4f} Mpc^-1, "
          f"xi(20kpc) = {o_[GAL20['label']]:.3e}, c_s/v_c(gal) = {csg_/GAL20['vc']:.2f}")
print("""
  READ-OFF:  N = 2 (generic, any K with K''(Q0) != 0) is dead both ways (Blocks 7-8).
  A window opens only for 3.5 <~ N <~ 9, i.e. K must vanish at least QUARTICALLY at its
  minimum (K''(Q0) = K'''(Q0) ~ 0).  The shift symmetry does NOT protect that; it is a
  tuning, and it is a DIFFERENT shape from the rescue Blanchet & Skordis floated (large
  K3 ~ 1e5 / K4 ~ 1e6 WITH K2 present).  In that window xi(galaxy) ~ 1e-13 - 1e-6 (RAR and
  galaxy weak lensing untouched, which also answers Mistele+2023's weak-lensing challenge)
  and xi(R500) = 0.11-0.26 by construction -- but the Q-sector transfer function turns over
  at k ~ 0.1-0.2 Mpc^-1, i.e. lambda ~ 30-60 Mpc, INSIDE the SDSS/BOSS linear range.""")

# =====================================================================
hdr("BLOCK 10 -- timescales: is the suppression dynamically REALISED?")
# =====================================================================
print("""
  identity for gamma = 2: with the condensate at CDM level rho = rho_dyn = 3 vc^2/(4 pi G R^2),
      c_s^2 = 4 pi G rho/mu^2 = 3 vc^2/(mu R)^2  =>  c_s/vc = sqrt(3)/(mu R)
      t_sound/t_dyn = (R/c_s)/(R/(sqrt(3) vc)) = mu R
  so for R << 1/mu a CDM-level condensate overdensity is SUPERSONICALLY over-pressured and
  re-expands in mu R dynamical times.  The suppression is not a linear-theory statement; it is
  dynamically enforced.  This also partially answers ACLMW 2007 sec 3.5 ('It is possible that
  the pressure resolves the caustics ... inside galaxy halos ... we will not consider that
  here') -- MY INFERENCE, not theirs.
""")
mu = 1.0/(1.55*Mpc)
for s in [GAL20, GAL100, CLU]:
    cs = np.sqrt(4*np.pi*G*s['rho_dyn']/mu**2)
    print(f"  {s['label']:42s}: mu R = {mu*s['R']:.4f}, c_s(at CDM level) = {cs/1e3:9.1f} km/s"
          f"  vs vc = {s['vc']/1e3:7.1f} km/s   -> {'EXPELLED' if cs>s['vc'] else 'BOUND'}")
print("\n  same test on the best non-generic branch N = 4:")
g4, kc4, o4, csg4, csc4 = k_crit_and_xi(4.0)
print(f"    galaxy  20 kpc: c_s(at CDM level) = {csg4/1e3:8.1f} km/s vs vc = 220.0 km/s -> "
      f"{'EXPELLED' if csg4>GAL20['vc'] else 'BOUND'}")
print(f"    cluster R500  : c_s(at CDM level) = {csc4/1e3:8.1f} km/s vs vc = {CLU['vc']/1e3:.1f} km/s -> "
      f"{'EXPELLED' if csc4>CLU['vc'] else 'BOUND'}")

# =====================================================================
hdr("BLOCK 11 -- the decisive, K-shape-independent version of the trade")
# =====================================================================
print("""
  Drop the cluster demand entirely (leave the framework's cluster front open) and impose ONLY
  the thing the no-dark-matter-in-halos reading actually needs:
      the shift charge must be EXPELLED from galaxies,  c_s(rho_dyn,gal) = F v_c,gal, F >~ 1.4
  Normalise K_poly on THAT and ask what it costs at the CMB/LSS end.  Because c_s^2 ~ rho^(g-1)
  and a^2H^2 ~ a^-1 in the matter era, kappa = c_s^2 k^2/(a^2 H^2) ~ a^{1-3(g-1)}: the
  suppression is time-independent exactly at gamma = 4/3 (N=4), which is therefore the OPTIMUM
  -- for gamma < 4/3 the binding epoch is today, for gamma > 4/3 it is the early universe.
""")
def norm_on_galaxy(Nv, F):
    gamma = Nv/(Nv-1.0)
    cs2_gal = (F*GAL20['vc'])**2
    Kp_ = cs2_gal/(gamma*GAL20['rho_dyn']**(gamma-1))
    return gamma, Kp_
def transfer_from_Kp(gamma, Kp_, k_Mpc, a_i=1e-6):
    kk = k_Mpc/Mpc
    def rhs(x, y, kv):
        av = np.exp(x); H = Hofa(av); rho = rho_dm0*av**-3
        cs2 = gamma*Kp_*rho**(gamma-1)
        d, dp = y
        return [dp, -(2 + dlnH_dlna(av))*dp - (cs2*kv**2/(av**2*H**2) - 4*np.pi*G*rho/H**2)*d]
    s1 = solve_ivp(rhs, (np.log(a_i), 0.0), [1.,0.], args=(kk,), rtol=1e-9, atol=1e-14, method='LSODA')
    s0 = solve_ivp(rhs, (np.log(a_i), 0.0), [1.,0.], args=(1e-6/Mpc,), rtol=1e-9, atol=1e-14, method='LSODA')
    return s1.y[0,-1]/s0.y[0,-1]
def k_at_T_gal(Nv, F, Tgoal):
    gamma, Kp_ = norm_on_galaxy(Nv, F)
    lo, hi = 1e-4, 50.0
    if transfer_from_Kp(gamma, Kp_, lo) < Tgoal: return np.nan
    for _ in range(45):
        mid = np.sqrt(lo*hi)
        if transfer_from_Kp(gamma, Kp_, mid) > Tgoal: lo = mid
        else: hi = mid
    return np.sqrt(lo*hi)
print(f"  {'F':>5} {'N':>5} {'gamma':>7} {'k(T=0.9)':>10} {'k(T=0.5)':>10} {'lam(T=.9)':>10} "
      f"{'xi(R500)':>10} {'xi(20kpc)':>11} {'shortfall':>10}")
bestall = None
for F in [1.0, 1.414, 3.0]:
    for Nv in [3, 3.5, 4, 4.5, 5, 6, 8]:
        gamma, Kp_ = norm_on_galaxy(Nv, F)
        k9 = k_at_T_gal(Nv, F, 0.9); k5 = k_at_T_gal(Nv, F, 0.5)
        xic = rho_c_of(A_LOG*CLU['vc']**2, gamma, Kp_)/CLU['rho_dyn']
        xig = rho_c_of(A_LOG*GAL20['vc']**2, gamma, Kp_)/GAL20['rho_dyn']
        print(f"  {F:5.2f} {Nv:5.1f} {gamma:7.4f} {k9:10.4f} {k5:10.4f} {2*np.pi/k9:10.1f} "
              f"{xic:10.3e} {xig:11.3e} {0.3/k9:10.2f}")
        if bestall is None or k9 > bestall[0]: bestall = (k9, F, Nv, xic, xig)
print(f"\n  ABSOLUTE BEST over the whole barotropic class (F >= 1.0, any N):"
      f"  k(T=0.9) = {bestall[0]:.4f} Mpc^-1 at F={bestall[1]}, N={bestall[2]}")
print(f"     -> lambda(T=0.9) = {2*np.pi/bestall[0]:.1f} Mpc, shortfall vs 0.3 Mpc^-1 ="
      f" factor {0.3/bestall[0]:.2f} in k; and it delivers only xi(R500) = {bestall[3]:.3e}")
print("""
  READ-OFF -- THE HARD RESULT.  Expelling the shift charge from galaxies REQUIRES a dark
  sector with c_s >~ 200-700 km/s at galactic densities.  Any barotrope with that property is
  too WARM to be CDM at LSS scales: the best case anywhere in the class suppresses the Q-sector
  transfer function by >10% already at k ~ 0.1-0.2 Mpc^-1, and if you additionally demand
  xi(R500) = 0.11-0.26 the cutoff moves to k ~ 0.02-0.03 Mpc^-1 (lambda ~ 200-300 Mpc).
  There is no barotropic shift-charge fluid that is simultaneously absent from galaxies,
  present at 11-26% in clusters, and CDM-like for the CMB.  The framework's own cluster
  requirement and the CMB fit that motivated AeST pull the SAME single knob in opposite
  directions -- this is Blanchet & Skordis 2024 sec 4.3.1 and Mistele+2023 Table 1, now
  derived from the shift charge's OWN equation of state and extended to arbitrary K shape.""")

# =====================================================================
hdr("BLOCK 12 -- PARETO FRONT: best LSS behaviour compatible with the framework's cluster need")
# =====================================================================
print("""  Impose BOTH framework requirements at once and maximise the LSS reach:
      (i)  xi(R500) = target (0.11 / 0.20 / 0.26)                  [clusters need this]
      (ii) c_s(rho_dyn,gal)/v_c,gal >= 1.4 (>= escape speed)        [galaxies must drain]
  and report the largest k that still grows to within 10% of the CDM answer.
""")
for xi_t in [0.11, 0.20, 0.26]:
    bestrow = None
    for Nv in [4, 5, 6, 8, 10, 12, 16, 20, 24, 28, 34, 40]:
        gamma, kcrit, out, csg, csc = k_crit_and_xi(Nv, xi_clu=xi_t)
        if csg/GAL20['vc'] < 1.4: continue
        k9 = k_at_T(Nv, 0.9, xi_clu=xi_t)
        if bestrow is None or k9 > bestrow[1]: bestrow = (Nv, k9, csg/GAL20['vc'], out)
    Nv, k9, rg, out = bestrow
    print(f"  xi(R500)={xi_t:.2f}: best N = {Nv} (gamma={Nv/(Nv-1):.4f}), drain ratio = {rg:.2f},"
          f"  k(T=0.9) = {k9:.4f} Mpc^-1  (lambda = {2*np.pi/k9:.0f} Mpc)")
    print(f"                 xi(20 kpc) = {out[GAL20['label']]:.3e},"
          f" SHORTFALL vs 0.3 Mpc^-1 = factor {0.3/k9:.2f} in k")
print("""
  ==> NO member of the barotropic shift-charge class clears the LSS bar.  Best case anywhere:
      the Q-sector transfer function is already 10% low at k ~ 0.08-0.09 Mpc^-1 (lambda ~ 70-80
      Mpc), where the CMB and galaxy clustering are measured to sub-percent accuracy.  The
      GENERIC member (quadratic K, N=2) misses by ~1e9 in c_s^2.  And the winning N ~ 20-24
      means K ~ (Q-Q0)^20, i.e. the first NINETEEN derivatives of K vanish at the minimum.""")

hdr("SUMMARY")
print("""
  1. The shift charge IS advected and CAN concentrate: d_t n + div(n v) = 0 with
     v^i = 2 Fcal_Y grad^i phi/Fcal_Q.  There is no structural exemption from concentration.
  2. But the flow is irrotational and single-valued: it cannot VIRIALISE in the CDM sense
     (no multistreaming, no velocity dispersion, no violent relaxation).  Its only equilibrium
     is HYDROSTATIC, supported by p = K_poly rho^gamma, gamma = N/(N-1) for an order-N
     minimum of K.  ANSWER TO THE FDM COUNTEREXAMPLE: FDM has k_J ~ rho^{1/4} (compression
     shrinks its Jeans scale, so it clusters); the generic N=2 shift charge has k_J = mu,
     rho-INDEPENDENT, compression-proof.  The correct analogue is not fuzzy DM but BEC /
     self-interacting scalar DM in the Thomas-Fermi limit, radius R = pi/mu, mass-independent.
  3. That yields a REAL, quantitative suppression law:  xi(R) = A (mu R)^2 / 3.  Numbers with
     mu^-1 fixed by xi(R500) = 0.11-0.26  ->  mu^-1 = 1.36-2.09 Mpc:
        xi(20 kpc) = 3.1e-5 - 7.2e-5 ;  xi(100 kpc) = 7.6e-4 - 1.8e-3 ;  xi(dwarf) ~ 2-5e-6.
     The SPARC RAR would be untouched, and Mistele+2023's weak-lensing challenge answered.
     It is also DYNAMICALLY enforced (t_sound/t_dyn = mu R exactly), not merely a linear
     statement, which independently VALIDATES Durakovic & Skordis's Q -> Q0 assumption.
  4. IT DOES NOT SURVIVE THE PARAMETER COUNT.  Same mu, opposite demands:
        clusters  -> mu^-1 = 1.4-2.1 Mpc
        cosmology -> mu^-1 <~ 0.055-1.28 kpc  (c_s^2/c^2 at a=1.1e-5 fails by 1.7e9-4.0e9;
                                               w at recombination = 25-59)
     On the cosmology-allowed branch xi(20 kpc) = 1.3e2 - 4.4e4 and xi(R500) = 4.8e5 - 1.6e8:
     the shift charge does not merely reach CDM level, it OVERSHOOTS CDM by 2-5 orders.
     The brief's item-4 overshoot (2.06x-4.42x) UNDERSTATES this branch badly.
  5. AND THE FAILURE IS NOT SPECIFIC TO THE QUADRATIC K.  Scanning the whole power-law class
     K ~ (Q-Q0)^N, the best point that delivers xi(R500) = 0.11-0.26 AND lets galaxies drain
     at >= escape speed is N ~ 24 (gamma = 1.044), and even there the Q-sector transfer
     function is 10% low already at k = 0.090 Mpc^-1 (lambda ~ 70 Mpc) -- a factor 3.3
     shortfall in k against the ~0.3 Mpc^-1 the CMB and galaxy clustering demand.
  6. WHAT IS STILL OPEN (do not read this as closed):
     (a) my closure is BAROTROPIC, p = p(rho).  The Pareto failure is a statement about
         MONOTONE c_s^2(rho).  A K with an INFLECTION, giving c_s^2(rho) PEAKED near galactic
         densities (~1e-22 kg/m^3) and small at BOTH ~1e-27 (mean today) and ~1e-12 (a=1e-5),
         evades every bound computed here.  No one has constructed or excluded such a K; it is
         unmotivated by any symmetry but it is not forbidden.  THIS IS THE LIVE DOOR.
     (b) I neglected Y-Q cross terms in Fcal.  Fcal(Y,Q) is not separable in general and a
         cross term gives anisotropic stress, i.e. a non-barotropic closure.  Never computed.
     (c) if the flow DOES form caustics (ACLMW 2007 sec 3.2), the coarse-grained closure
         acquires a velocity dispersion instead of a pressure -- but that pushes toward MORE
         CDM-like clustering, i.e. against interest.
""")
