#!/usr/bin/env python3
"""
AeST |Phi|-BOUNDARY CLUSTER DOOR -- SETUP + DERIVATION VERIFY (the DS24 deferred step).
=======================================================================================
This is the SETUP/DERIVE leg: it encodes the EXACT weak-field AeST equations extracted
verbatim from the three source papers, verifies the deep-MOND limit symbolically, and
characterizes the "boundary value of the gravitational potential" mechanism that
Durakovic-Skordis 2024 flagged as "the potential of AeST to address the shortcomings of
MOND in galaxy clusters" and explicitly DEFERRED ("going beyond the isothermal case").

Framework (C. Zimmerman): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2 (INPUT, quarantined,
never derived). The dark sector IS AeST (Skordis-Zlosnik 2021). The AeST constants
{K_2 -> mu, K_B, lambda_s, a0} are FREE inputs; a0 is imported from the framework, the
mass mu is CMB-pinned (1/mu ~ 1 Mpc), lambda_s sets the screening.

=========================== THE EXACT FIELD EQUATIONS ===========================
Source 1 -- Durakovic & Skordis 2024, arXiv:2312.00889, JCAP 04 (2024) 040
            "Towards galaxy cluster models in AeST: isothermal spheres and curiosities"
Source 2 -- Blanchet & Skordis 2024, arXiv:2404.06584, JCAP 11 (2024) 040
            "Relativistic Khronon Theory ..." (the SAME weak-field structure)
Source 3 -- Skordis & Zlosnik 2021, arXiv:2007.00082, PRL 127 161302 (the AeST action)

THE SINGLE REDUCED WEAK-FIELD EQUATION (DS24 Eq 2.33 / spherical Eq 2.40):

      div[ M(x) grad Phi ] + mu_t^2 Phi = 4 pi G_N rho_b ,      x = |grad Phi| / a0

  spherical:  (1/r^2) d/dr[ r^2 M(x) Phi' ] + mu_t^2 Phi = 4 pi G_N rho_b(r)

  - M(x) is the MOND interpolation (DS24 Eq 2.39, simple-mu / lambda_s->inf choice):
        M(x) = ( -1 + sqrt(1+4x) ) / ( 1 + sqrt(1+4x) )
        limits:  M->1 (Newton, x>>1) ;  M->x (deep-MOND, x<<1)
  - mu_t^2 = (1+beta0) mu^2  (DS24 Eq 2.35), beta0 = 1/lambda_s (Eq 2.36).
        This is the NEW AeST term ABSENT from AQUAL/Bekenstein-Milgrom. Its SIGN is
        +mu^2 -> a MODIFIED HELMHOLTZ operator (oscillatory homogeneous solutions).

EQUIVALENT (Blanchet-Skordis 2024 Eq 3.21-3.23): div[(1+J_Y) grad phi] + mu^2 phi = 4piG rho,
  with f(y) = 1 + J_Y(Y) the MOND function (Eq 3.22), y = |grad phi|/a0, Y = a0^2 y^2/c^4,
  and the FREE FUNCTION in the deep-MOND limit (Eq 3.23):
        J(Y) = Lambda - Y + (2 c^2 / 3 a0) Y^{3/2} + O(Y^2)
  => J_Y = -1 + (c^2/a0) sqrt(Y) ,  f(y) = 1 + J_Y = (c^2/a0) sqrt(Y) = y   (deep-MOND).
  So 1+J_Y (BS24) == M(x) (DS24) are the SAME interpolation; same +mu^2 mass term.
  a0 enters in EXACTLY ONE place: the coefficient of the forced Y^{3/2} term. The
  framework plugs a0 = 9.36e-11 into that one slot. (Lambda is the additive constant of J,
  orthogonal to a0; Lambda ~ a0^2/c^4, BS24 Eq just below 3.7.)

================= THE BOUNDARY-Phi MECHANISM (the load-bearing physics) =================
WHY there is a |Phi|-boundary dependence AT ALL:
  Pure AQUAL/MOND  div[M(x) grad Phi] = 4piG rho  is SHIFT-INVARIANT: Phi -> Phi + const
  leaves it unchanged (only grad Phi appears). The absolute zero-point of Phi is unphysical.
  The AeST mass term +mu^2 * Phi BREAKS that shift symmetry: Phi appears UNDIFFERENTIATED.
  => the ABSOLUTE VALUE of Phi (its boundary/asymptotic level) is now PHYSICAL and feeds
     back into the source as an effective mass density -mu^2 Phi / (4 pi G).

WHAT the "boundary value of the gravitational potential" IS, precisely (DS24):
  - In the VACUUM/extended-source case it is the shift  Delta Phi  (DS24 Eq 2.42, Fig 7).
  - In the ISOTHERMAL (cluster) case it is the asymptotic constant  chi_infty  (DS24 Sec 3.5,
    Fig 7 right; Appendix B.2 iterates the inner BC until Phi(r->large) -> chi_infty).
  Because the operator is HELMHOLTZ (+mu^2), the homogeneous solutions are oscillatory
  [C1 cos(mu r) + C2 sin(mu r)]/r, BOTH decaying as 1/r, so Phi(inf)->0 does NOT select a
  unique solution: a one-parameter family survives, parametrized by chi_infty.

WHY it ENHANCES CLUSTERS (DS24 abstract + conclusion, verbatim):
  "the AeST RAR ... can display a peak, an enhancement with respect to the MOND RAR, at an
   acceleration range determined by [1] the value of the AeST weak-field mass parameter,
   [2] the mass of the system, and [3] THE BOUNDARY VALUE OF THE GRAVITATIONAL POTENTIAL.
   For lower accelerations, the AeST RAR drops below the MOND expectation, as if there is a
   negative mass density."  AND:  "The peak is made larger by a MORE NEGATIVE shift of the
   potential." (Sec 3.5)  AND the deferral: "a full quantitative comparison with observations
   will require GOING BEYOND THE ISOTHERMAL CASE ... left for future work." (conclusion)

  => More negative boundary |Phi| (deeper well) -> the -mu^2 Phi effective source is MORE
     POSITIVE (extra phantom mass) over the core -> a RAR PEAK above MOND. Clusters sit in a
     deeper integrated potential than galaxies, so a boundary-|Phi|-keyed term ranks clusters
     above galaxies -- the one scalar where clusters beat galaxies (potential DEPTH).

THE CRUX FOR THE PAPER (what the full non-isothermal solve must decide):
  Is chi_infty (a) PINNED by physics (cosmological matching) to a value that gives the cluster
  peak WITHOUT a per-cluster tune AND WITHOUT breaking galaxies, or (b) a free per-object knob
  (then it is descriptive, not predictive). DS24 leave chi_infty free; the framework footing
  asks whether a0=Lambda + the cosmological background fix it. (Prior corpus work --
  CLUSTER_AEST_MASSTERM_BVP_implB, cluster_chi_out_cosmological_matching -- found the mass-term
  +mu^2 route under a NON-tuned/cosmological chi gives a DEFICIT, not the +2 boost, and that
  galaxy-safety needs a smaller mu than clusters: the Mistele 2023 squeeze. This SETUP encodes
  the exact equations for the full non-isothermal numeric solve to re-decide on the framework's
  own a0 with REAL baryon profiles.)
"""
import sympy as sp
import numpy as np

print("="*88)
print("AeST |Phi|-BOUNDARY CLUSTER DOOR -- SETUP + DERIVATION VERIFY")
print("="*88)

# ----------------------------------------------------------------------------------
# 1. DEEP-MOND LIMIT -- both interpolation forms, symbolic (must be EXACT).
# ----------------------------------------------------------------------------------
print("\n[1] DEEP-MOND LIMIT (symbolic, sympy)")
x, Y, a0s, c, y = sp.symbols('x Y a0 c y', positive=True)
Lam = sp.symbols('Lambda')

# DS24 Eq 2.39 interpolation M(x)
M = (-1 + sp.sqrt(1 + 4*x)) / (1 + sp.sqrt(1 + 4*x))
M_deep = sp.series(M, x, 0, 2).removeO()
M_newt = sp.limit(M, x, sp.oo)
print(f"  DS24 (2.39)  M(x) = {M}")
print(f"               M(x->0)  = {M_deep}   (deep-MOND: M->x  OK)")
print(f"               M(x->oo) = {M_newt}   (Newton:   M->1  OK)")

# BS24 Eq 3.23 free function J(Y) and f(y)=1+J_Y
J = Lam - Y + (2*c**2/(3*a0s)) * Y**sp.Rational(3, 2)
JY = sp.diff(J, Y)
f_y = sp.simplify((1 + JY).subs(Y, a0s**2 * y**2 / c**4))
print(f"\n  BS24 (3.23)  J(Y) = Lambda - Y + (2c^2/3a0) Y^(3/2)")
print(f"               J_Y  = {sp.simplify(JY)}")
print(f"               f(y) = 1 + J_Y = {f_y}   (deep-MOND interpolation f(y)=y  OK)")
deep_ok = (sp.simplify(M_deep - x) == 0) and (M_newt == 1) and (sp.simplify(f_y - y) == 0)
print(f"\n  DEEP-MOND CHECK: M->x, M->1, (1+J_Y)->y  ALL EXACT?  {deep_ok}")
print("  => BS24's (1+J_Y) and DS24's M(x) are the SAME forced sqrt-law MOND interpolation;")
print("     a0 sits in the single forced Y^(3/2) coefficient -> framework plugs 9.36e-11 there.")

# Force law check: deep-MOND  M(x) Phi' = g_bar  =>  x Phi' ... |g|=sqrt(g_bar a0)
print("\n  Force-law: deep-MOND div[M grad Phi]=4piG rho with M->x=|gradPhi|/a0 gives")
print("             |grad Phi|^2/a0 ~ g_N  =>  g_obs = sqrt(g_N a0)  == framework dS-Unruh MI.")

# ----------------------------------------------------------------------------------
# 2. SHIFT-SYMMETRY BREAKING -- why the boundary value of Phi is physical.
# ----------------------------------------------------------------------------------
print("\n[2] BOUNDARY-Phi MECHANISM: shift-symmetry breaking by the +mu^2 Phi term (symbolic)")
r = sp.symbols('r', positive=True)
Phi = sp.Function('Phi')
mu_t, GN, rho = sp.symbols('mu_t G_N rho', positive=True)
const = sp.symbols('C')  # a constant shift Phi -> Phi + C

# Pure AQUAL operator (no mass term): only grad Phi appears -> shift invariant.
# Helmholtz/AeST operator: + mu_t^2 Phi -> NOT shift invariant.
Phi_op_mass = mu_t**2 * Phi(r)
Phi_shift   = mu_t**2 * (Phi(r) + const)
delta = sp.simplify(Phi_shift - Phi_op_mass)
print(f"  AQUAL term div[M grad Phi]: depends ONLY on grad Phi  -> shift Phi->Phi+C invariant.")
print(f"  AeST mass term  mu_t^2 Phi: shift Phi->Phi+C changes it by  {delta}  (NOT invariant).")
print(f"  => the boundary/asymptotic level of Phi (Delta Phi / chi_infty) is PHYSICAL.")
print(f"  => effective extra source density = -mu_t^2 Phi/(4 pi G):  deeper (more negative) Phi")
print(f"     -> more POSITIVE phantom density over the core -> RAR PEAK above MOND.")

# ----------------------------------------------------------------------------------
# 3. PARAMETERS + framework values (numeric, SI).
# ----------------------------------------------------------------------------------
print("\n[3] PARAMETERS (AeST free inputs + framework a0)")
c_si   = 2.99792458e8
G_N    = 6.674e-11
Mpc    = 3.0857e22
kpc    = 3.0857e19
a0_fw  = 9.36e-11                       # framework input, quarantined
H0     = 67.4e3 / Mpc
OL     = 0.685
Lam_OL = 3.0 * OL * H0**2 / c_si**2     # 1/m^2
Lam_a0 = 32.0 * np.pi * (a0_fw / c_si**2)**2
inv_mu = 1.0 * Mpc                      # CMB-pinned 1/mu ~ 1 Mpc (BS24 Eq 3.25: mu^-1 >~ 1 Mpc)
mu_val = 1.0 / inv_mu
print(f"  a0   (framework input)   = {a0_fw:.4e} m/s^2   [a0 = c^2 sqrt(Lambda/32pi); QUARANTINED]")
print(f"  Lambda(from a0)          = {Lam_a0:.4e} 1/m^2")
print(f"  Lambda(from Omega_L)     = {Lam_OL:.4e} 1/m^2   (ratio {Lam_a0/Lam_OL:.3f})")
print(f"  mu   (CMB-pinned, FREE)  = {mu_val:.4e} 1/m   (1/mu = {inv_mu/Mpc:.2f} Mpc)")
print(f"  lambda_s (screening, FREE): simple-mu limit lambda_s->inf => beta0=0, M=Eq(2.39).")
print(f"  AeST adopts a0=1.2e-10 phenomenologically; framework imports 9.36e-11 (-22%, RAR-band).")

# ----------------------------------------------------------------------------------
# 4. POTENTIAL-DEPTH ORDERING (why clusters can beat galaxies on this lever) -- order check.
# ----------------------------------------------------------------------------------
print("\n[4] POTENTIAL-DEPTH ORDERING (order-of-magnitude scaffold for the full solve)")
# integrated baryonic depth |Phi_bar|/c^2 ~ (1/c^2) * v_c^2 for a system of circular speed v_c
def depth_over_c2(vc_kms):
    return (vc_kms*1e3)**2 / c_si**2
print(f"  |Phi_bar|/c^2 ~ v_c^2/c^2 :")
for name, vc in [("Solar System (local Sun, v~30 km/s orbit)", 30),
                 ("deep SPARC disk      (v_c ~ 250 km/s)", 250),
                 ("rich cluster A2029   (v_c ~ 1000 km/s)", 1000)]:
    print(f"     {name:42s}: {depth_over_c2(vc):.3e}")
print("  => cluster integrated depth ~16x a big galaxy's, ~1e3x the Sun's local orbital depth.")
print("     This is the ONE scalar where clusters out-rank galaxies (density orders backwards).")
print("     The naive LOCAL |Phi|/c^2 coupling gives only ~0.003% (cluster 1.1e-5) -- TOO SMALL.")
print("     The QUESTION for the full solve: does the NONLINEAR chi_infty/Helmholtz boundary")
print("     mechanism deliver MORE than this naive local coupling, AND stay galaxy+Cassini safe?")

# ----------------------------------------------------------------------------------
# 5. THE EQUATIONS TO SOLVE NUMERICALLY (handed to the solve leg).
# ----------------------------------------------------------------------------------
print("\n[5] EQUATIONS FOR THE FULL NON-ISOTHERMAL SOLVE (the deferred DS24 step)")
print("""  Two-component (DS24 Eq 2.43-2.44, non-singular form), spherical, REAL baryon rho_b(r):
      (1/r^2) d/dr[ r^2 (Phi' - chi') ] + mu_t^2 Phi = 4 pi G_N rho_b(r)
      beta(x) * chi' = Phi'      ,   x = |Phi'|/a0 ,  beta = 1 + J_Y = f(y)
  OR the Hamiltonian canonical-momentum form (DS24 Sec 3, removes the |Phi'|=0 singularities):
      evolve P_Phi (canonical momentum) instead of Phi -- smooth through oscillation nodes.
  Boundary: inner regularity at r0 (P_Phi(r0)=G_N M_bar(r0)); OUTER value Phi(r->R_match)=chi_infty.
  chi_infty is the lever: (a) cosmological-matching (turnaround, Lambda/mean-field) -> test if
  it gives the cluster peak with NO per-cluster tune; (b) free -> descriptive only.
  SOLVE for: (a) rich cluster M500=1e15 real gas(beta-model)+stars(Hernquist), embedded chi_infty;
             (b) SPARC-like disk (shallow Phi) -- galaxy-veto: RAR shift must stay < 0.05 dex;
             (c) Solar System (deep local g>>a0, shallow integrated Phi) -- Cassini.
  Report: effective boost eta(R500)=g_AeST/g_MOND, galaxy RAR scatter shift, Cassini |gamma-1|,
          and magnitude vs the naive ~0.003% local |Phi|/c^2.""")

print("\n" + "="*88)
print("SETUP VERIFY COMPLETE.  Deep-MOND EXACT:", deep_ok,
      " | shift-breaking confirmed | params loaded | equations staged for the full solve.")
print("="*88)
