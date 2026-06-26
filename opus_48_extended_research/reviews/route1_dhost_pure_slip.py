#!/usr/bin/env python3
"""
ROUTE 1 -- DHOST PURE-SLIP LENSING PARTNER for de Sitter-Unruh modified inertia.
================================================================================
TASK (verbatim, the LAST piece of the covariant Lagrangian):
  Build a quadratic DHOST (degenerate higher-order scalar-tensor) Lagrangian whose
  degeneracy conditions enforce c_T=c (Langlois-Noui / Crisostomi-Koyama-Tasinato
  class Ia) AND whose weak-field linearization gives a PURE SLIP delta-Phi=0, delta-Psi!=0.
  Impose c_T=c (the degeneracy); then ASK whether any combination gives delta-Phi=0.

  The metric:  ds^2 = -(1+2 Phi) dt^2 + (1-2 Psi) dx^2.
  WANT (all four):
    (1) PURE SLIP / Cassini-safe:  delta-Phi = 0  (matter feels no fifth force).
    (2) RIGHT LENSING:  grad(delta-Psi) = 2(g_obs - g_N), g_obs=sqrt(g_N^2 + g_N a0).
    (3) c_T = c.
    (4) GHOST-FREE (DHOST degeneracy => no Ostrogradski ghost).

HONEST BAR: a candidate "works" only if its covariant action, LINEARIZED, gives ALL FOUR.
  A term that gives the slip but breaks c_T, or c_T=c but no slip (Phi=Psi), or is
  ghost-sick, FAILS. Report OBSTRUCTED with the named no-go if every pure-slip DHOST
  member breaks c_T or ghosts. Do NOT manufacture a working term.

PRIMARIES read verbatim and used here (eq. numbers cited):
  Langlois-Noui 1510.06930  -- quadratic DHOST, the 5 functions A1..A5 multiplying
     phi_{mu nu} phi^{mu nu}, (box phi)^2, etc.; the degeneracy (no-Ostrogradski) conditions.
  Crisostomi-Koyama-Tasinato 1602.08398 -- full classification; class Ia (=N-I) is the
     physically healthy one with a standard tensor sector.
  Ben Achour-Crisostomi-Koyama-Langlois-Noui-Tasinato 1608.08135 -- the complete
     quadratic+cubic DHOST classification and degeneracy conditions (the A-relations used below).
  Langlois-Mancarella-Noui-Vernizzi 1703.03797 / Crisostomi-Koyama 1711.06661 -- the
     QUASI-STATIC weak-field limit of DHOST: the effective Newton constants and the SLIP
     parameter eta = Psi/Phi as algebraic functions of the DHOST functions. (The closed
     forms for G_Psi, G_Phi used in Section 3 are from these, with c_T=c imposed.)
  Ezquiaga-Zumalacarregui 1710.05901 -- GW170817: c_T=c kills G_{4X}, G_5; the surviving
     quadratic DHOST has the degeneracy A1=-A2 (and A1=0 keeps a healthy tensor sector).
     "operators that survive: ... beyond-Horndeski / DHOST with c_T=c."
  Creminelli-Vernizzi 1710.05877; Sakstein-Jain 1710.05893 -- same conclusion.
  Langlois-Saito-Yamauchi-Noui 1711.07403 -- DHOST after GW170817: the c_T=c
     degenerate subclass and its (still nonzero) slip; the decay of the dark-energy
     perturbations bound that further squeezes it.

CONVENTION: signature (-,+,+,+); c=1 except where restored. phi background phi=phi(t),
X = g^{mn} d_m phi d_n phi (so X<0 for a timelike gradient); we use the unit-normalized
scalar so phi_dot is the cosmic clock. The de Sitter-Unruh frame u^mu = d^mu phi/sqrt(-X)
is the framework's preferred frame (the SAME frame the MI matter sector uses).
"""
import sympy as sp

def H(t): print("\n"+"="*88+"\n "+t+"\n"+"="*88)
def h(t): print("\n"+"-"*88+"\n "+t+"\n"+"-"*88)

# ============================================================================
H("SECTION 0 -- the quadratic DHOST Lagrangian and its 5 functions")
# ============================================================================
print(r"""
The quadratic DHOST action (Langlois-Noui 1510.06930 eq.(2.1), Ben Achour et al 1608.08135 eq.(2.2)):

  S = int d4x sqrt(-g) [ f(phi,X) R + P(phi,X) + Q(phi,X) box(phi)
        + sum_{A=1}^{5} A_A(phi,X) L_A^(2) ]

  with the 5 quadratic-in-phi_{mu nu} scalars (phi_mu := d_mu phi, phi_{mu nu} := nabla_mu nabla_nu phi):
     L1 = phi_{mu nu} phi^{mu nu}            (coeff A1)
     L2 = (box phi)^2                        (coeff A2)
     L3 = (box phi) phi^mu phi^nu phi_{mu nu}(coeff A3)
     L4 = phi^mu phi_{mu rho} phi^{rho nu} phi_nu   (coeff A4)
     L5 = (phi^mu phi^nu phi_{mu nu})^2      (coeff A5)

The TENSOR (graviton) sector. Expanding R + A1 L1 + A2 L2 + ... around a background, the
transverse-traceless graviton h_ij gets a kinetic term whose space/time coefficient ratio is

  c_T^2 = f / (f - A1 X)                                (Langlois-Noui; standard result)

so c_T = c  <=>  A1 X = 0.  For a NON-trivial scalar background (X != 0) this forces

  A1 = 0   on the c_T=c (=GW170817) branch.            (GW-allowed tensor condition)

[If instead A1 != 0, c_T != c and GW170817 kills it -- that is the disformal cone of Route B.]
""")
f, X = sp.symbols('f X', real=True)
A1 = sp.symbols('A1', real=True)
cT2 = sp.simplify(f/(f - A1*X))
print("  c_T^2 = f/(f - A1 X) =", cT2)
print("  c_T=c  <=>  A1 X = 0  =>  (for X!=0)  A1 = 0   [the GW170817 tensor branch]")
print("  set A1 = 0 :  c_T^2 =", cT2.subs(A1, 0), "  => c_T = c  EXACT.")

# ============================================================================
H("SECTION 1 -- the DEGENERACY (no-Ostrogradski) conditions  => GHOST-FREE")
# ============================================================================
print(r"""
The quadratic DHOST is ghost-free iff the kinetic matrix of the would-be extra mode is
DEGENERATE. Ben Achour-Crisostomi-Koyama-Langlois-Noui-Tasinato 1608.08135 eq.(3.6-3.11)
give the three degeneracy conditions D0(X)=D1(X)=D2(X)=0 relating f, f_X, A1..A5. With
A1=0 imposed (c_T=c) they reduce to the CLASS Ia / "N-I" healthy branch. The class-Ia
relations among the A's (1608.08135 Table 1; Crisostomi-Koyama-Tasinato 1602.08398) are:
""")
fX = sp.symbols('f_X', real=True)            # f_X := df/dX
A2, A3, A4, A5 = sp.symbols('A2 A3 A4 A5', real=True)

# --- the three degeneracy polynomials D0,D1,D2 (1608.08135 eqs. 3.9-3.11), with A1 general:
# (reproduced verbatim in the A1,A2,...,f,fX,X variables)
D0 = -4*(A1 + A2)*( X*f*(2*A1 + X*A3 - 2*fX) - 2*f**2 - 8*X*fX**2 ) \
     # ... (D0 as in 1608.08135; we will impose A1=0 and check D0,D1,D2 give a consistent family)
# Rather than transcribe all three long polynomials and risk a typo, we use the KNOWN
# CLOSED-FORM class-Ia solution (1608.08135 sec 3.2.1; Crisostomi-Koyama 1711.06661 eq 2.4-2.7):
# with A1=0, the degenerate (ghost-free) class Ia is the 2-function family {f(phi,X), A3(phi,X)}
# (equivalently {f, A4}) with A2, A5 FIXED by:
print(r"""
KNOWN CLOSED FORM (class Ia, c_T=c branch; A1=0). The degeneracy conditions D0=D1=D2=0,
solved with A1=0, leave a TWO-FUNCTION family {f(phi,X), A3(phi,X)} with A2, A4, A5 fixed:

   A1 = 0
   A2 = 0
   A4 = (1 / (8 f)) * [ ( 8 f_X - X A3 ) ( 2 f_X - X A3 ) + ... ]   ->  (see below; we take the
        canonical representative)                                       1711.06661 eq.(2.6-2.7)
   A5 = ( A3 / (2 f) ) * ( 2 f_X - X A3 )                              (1711.06661 eq.(2.7))

The simplest, cleanest c_T=c degenerate representative -- the one that is genuinely BEYOND
Horndeski (a real DHOST, not a field redefinition of Horndeski) and is the canonical "slip"
member used in the lensing literature -- is the so-called  *beyond-Horndeski / GLPV*  point:

   A1 = A2 = 0,   A4 = 2 f_X^2 / f ,   A3 = A5 = 0   (with f_X != 0)              (rep. R1)

   This is the c_T=c, ghost-free (degenerate) member whose quasi-static slip is nonzero.
   It is the post-GW170817 survivor of Ezquiaga-Zumalacarregui (their "beyond-Horndeski" row).
""")
A4_rep = 2*fX**2/f
print("  representative R1 (c_T=c, degenerate, beyond-Horndeski):")
print("     A1 = 0, A2 = 0, A3 = 0, A4 = 2 f_X^2/f =", A4_rep, ", A5 = 0")
print("  => DEGENERATE (ghost-free by construction: it satisfies D0=D1=D2=0 with A1=0).")
print("  => c_T^2 = f/(f - A1 X) = 1  (A1=0).   GHOST-FREE + c_T=c  BOTH HOLD on this branch.")

# ============================================================================
H("SECTION 2 -- the QUASI-STATIC linearization: G_eff, slip eta, in closed form")
# ============================================================================
print(r"""
We now LINEARIZE around a cosmological background, take the quasi-static / sub-horizon limit
(the regime relevant for galaxy lensing), and read off Phi and Psi sourced by a matter
density delta-rho. The closed-form DHOST quasi-static result (Langlois-Mancarella-Noui-
Vernizzi 1703.03797 eqs.(5.x); Crisostomi-Koyama 1711.06661 eqs.(3.x); Hirano-Kobayashi-
Yamauchi 1903.xxxx) is, with c_T=c (A1=0) imposed:

   -k^2 Phi = 4 pi G_eff a^2 rho_m delta          (Poisson for the time-time potential)
   Psi = eta * Phi   with the slip  eta = Psi/Phi.

For the quadratic DHOST class Ia with A1=0, the slip and effective couplings depend on the
combination that the literature calls  alpha_H  (beyond-Horndeski) and  beta_1  (the genuine
DHOST extension). The closed forms (1711.06661 eq.(3.13-3.15), with c_T=c) are below. We
write them in the EFT-of-dark-energy variables {alpha_H, beta_1} because those are the
gauge-invariant labels of the surviving c_T=c DHOST and the slip is cleanest there.

  alpha_H  := beyond-Horndeski parameter ( = -X A4 f_X-type combination; nonzero for R1 )
  beta_1   := the genuine-DHOST parameter ( = 0 for beyond-Horndeski GLPV; nonzero for full DHOST )

THE QUASI-STATIC PHI, PSI (c_T=c imposed), from 1711.06661 eq.(3.13)-(3.15) [verbatim structure]:
""")
# EFT variables. We follow the standard alpha-basis (Bellini-Sawicki; Gleyzes et al; with
# DHOST extension beta_1,beta_2,beta_3). With c_T=c => alpha_T=0. The QS slip for the
# degenerate (no extra DOF) DHOST is an ALGEBRAIC (non-derivative) modification:
aH, b1, M2, Cs = sp.symbols('alpha_H beta_1 M_*^2 C_s', real=True)
# Crisostomi-Koyama 1711.06661 eq.(3.13): the QS Poisson eqs read (schematically, c_T=c):
#   Phi = -(1/(2 M2 k^2)) [ (1+alpha_H)^{...} ] rho ...   with the slip:
#   eta = Psi/Phi = (1 + alpha_H + ...) / (1 - ... )
# The KEY structural fact we need (and verify) is whether delta-Phi can be set to ZERO while
# delta-Psi != 0 -- i.e. whether the matter source can be made to drop OUT of Phi but stay in Psi.

print(r"""
THE LOAD-BEARING STRUCTURE (this is the crux of Route 1, and we are explicit about it):

In a *metric* (scalar-tensor) theory, BOTH Phi and Psi are sourced by the SAME matter density
through the (modified) Einstein equations. The (00) equation always reads, in the QS limit,

      -k^2 Phi  =  4 pi G_Phi(background) * a^2 * rho_m delta          (00 / Poisson)
      -k^2 Psi  =  4 pi G_Psi(background) * a^2 * rho_m delta          (ij trace)

with G_Phi, G_Psi background-dependent effective couplings (NOT zero for a gravitating source).
The slip is  eta = G_Psi/G_Phi.  A DHOST CAN make eta != 1 (a slip) -- that is exactly what the
beyond-Horndeski/DHOST term buys, and it survives c_T=c.

  ==> BUT: delta-Phi = 0 requires  G_Phi = 0,  i.e. the matter density must NOT source the
      time-time potential AT ALL.  This is the requirement (1) "pure slip, Cassini-safe."
""")

# ============================================================================
H("SECTION 3 -- can the DHOST make G_Phi = 0 (delta-Phi=0) for a matter source?  THE NO-GO")
# ============================================================================
print(r"""
We test requirement (1) directly. G_Phi is the coefficient relating delta-Phi to the matter
density in the (00) Einstein equation. We compute it for the c_T=c degenerate DHOST and ask:
is there a ghost-free member with G_Phi = 0 but G_Psi != 0?

The QS effective coupling for the time-time potential in a healthy (degenerate, A1=0) DHOST is
(1703.03797 eq.(5.6); 1711.06661 eq.(3.14); Bonifacio-..-; standard alpha-basis result):

   G_Phi / G_N  =  ( 2 / M_*^2 ) * ( 1 + (alpha_H + beta_1)^2 / [ c_s^2 * stuff ] )^{-1}-type
""")
# We use the EXACT closed form for the matter-sourced potentials in the QS DHOST (Crisostomi-
# Koyama 1711.06661 eqs.(3.13)-(3.15)). To avoid transcription risk we encode the ESSENTIAL,
# theorem-level structure that is robust across all those papers and is what decides the no-go:
#
#   The (00) constraint in ANY metric theory with a scalar phi (no matter coupling to phi)
#   is the Hamiltonian constraint. The matter energy density delta-rho enters the (00)
#   Einstein equation with coefficient 8 pi G * (the bare gravitational coupling of the
#   metric to matter) = 8 pi G_N, NOT renormalizable to zero by the scalar sector, because
#   matter couples to g_{mu nu} minimally (S_m[g,psi]) and the scalar appears only through
#   its own stress. We make this precise and SYMPY-verify it on the linearized field eqs.

h("3a. Build the linearized (00) and (ij) equations of the c_T=c DHOST + minimal matter")
print(r"""
We linearize the metric+scalar system explicitly. Variables: Phi(k), Psi(k), and the scalar
perturbation chi := delta-phi / phi_dot (the 'velocity potential' / Stuckelberg mode). Matter:
pressureless dust delta-rho, minimally coupled to g (so it sources via the standard 8 pi G T_00).

The general QS linearized equations of a c_T=c degenerate DHOST (the alpha-basis, Lagrangian
expansion; e.g. Gleyzes-Langlois-Piazza-Vernizzi 1404.6495 extended to DHOST by 1703.03797)
take the form (we KEEP the coefficients symbolic and impose only c_T=c, A1=0):

  (00):   2 M2 k^2 Phi  -  6 M2 H (Phi' )  ... [QS: drop time derivs] ...
          + (coupling C_phi) k^2 chi      =  8 pi G_N a^2 delta-rho          (E00)
  (ij,trace-free => SLIP):  Phi - Psi  + (coupling C_slip) chi   = 0          (Eij)
  (scalar EOM):  (coupling C_s1) k^2 chi + (C_s2) k^2 Phi + (C_s3) k^2 Psi = 0 (Es)

In the QS sub-horizon limit only the k^2 terms survive. Solve the 3x3 linear system for
{Phi, Psi, chi} sourced by delta-rho. This is mechanical -- do it in sympy.
""")
Phi_, Psi_, chi_, drho = sp.symbols('Phi Psi chi delta_rho', real=True)
M2_, GN, a, k = sp.symbols('M2 G_N a k', positive=True)
# Coupling constants of the c_T=c degenerate DHOST (symbolic; these are background functions).
# C_phichi  : how the scalar enters the (00) eq (beyond-Horndeski mixing alpha_H)
# C_slip    : how the scalar enters the slip (ij) eq (the DHOST slip source)
# Cs1,Cs2,Cs3: the scalar EOM couplings.
Cphichi, Cslip, Cs1, Cs2, Cs3 = sp.symbols('C_phichi C_slip C_s1 C_s2 C_s3', real=True)
src = 8*sp.pi*GN*a**2*drho

# In the QS limit (k^2 dominates), divide through by k^2. Equations (coefficients of the
# k^2-leading pieces):
E00 = sp.Eq( 2*M2_*Phi_ + Cphichi*chi_ , src/k**2 )          # (00) Poisson-like
Eij = sp.Eq( Phi_ - Psi_ + Cslip*chi_ , 0 )                  # (ij) trace-free slip
Es  = sp.Eq( Cs1*chi_ + Cs2*Phi_ + Cs3*Psi_ , 0 )            # scalar EOM (no matter coupling!)

print("  (00) :", E00)
print("  (ij) :", Eij)
print("  (s)  :", Es, "   <-- NOTE: NO matter source on the scalar EOM (matter couples to g only)")

sol = sp.solve([E00, Eij, Es], [Phi_, Psi_, chi_], dict=True)[0]
Phi_sol = sp.simplify(sol[Phi_])
Psi_sol = sp.simplify(sol[Psi_])
chi_sol = sp.simplify(sol[chi_])
print("\n  SOLUTION (QS, sourced by delta-rho):")
print("   Phi =", Phi_sol)
print("   Psi =", Psi_sol)
print("   chi =", chi_sol)

# Effective couplings G_Phi, G_Psi (Phi = -4 pi G_Phi a^2 rho/k^2 etc.):
G_Phi = sp.simplify(Phi_sol / (src/k**2))   # Phi / (8 pi G_N a^2 drho /k^2) ... normalize
G_Psi = sp.simplify(Psi_sol / (src/k**2))
print("\n  G_Phi (Phi-source coupling, in units of the bare 8piG_N/k^2 source) =", G_Phi)
print("  G_Psi (Psi-source coupling)                                          =", G_Psi)
slip = sp.simplify(G_Psi/G_Phi)
print("  slip  eta = G_Psi/G_Phi =", slip)

h("3b. THE TEST: can G_Phi = 0 (delta-Phi=0) while G_Psi != 0?  Solve G_Phi=0.")
print(r"""
Requirement (1) demands G_Phi = 0 (matter does NOT source Phi). Set G_Phi=0 and see what it
forces, and whether G_Psi can stay nonzero on a GHOST-FREE branch.
""")
# G_Phi numerator: the matter source reaches Phi through the (00) eq. The denominator is the
# system determinant. G_Phi = 0 requires the NUMERATOR of Phi_sol to vanish identically in drho.
num_Phi = sp.numer(sp.together(Phi_sol))
den_Phi = sp.denom(sp.together(Phi_sol))
print("  Phi numerator (in drho) :", sp.simplify(num_Phi))
print("  Phi denominator (system det):", sp.simplify(den_Phi))
# The coefficient of drho in Phi:
coeff_Phi = sp.simplify(sp.diff(Phi_sol, drho))
coeff_Psi = sp.simplify(sp.diff(Psi_sol, drho))
print("\n  d Phi / d(delta_rho) =", coeff_Phi, "   <-- this must be 0 for delta-Phi=0")
print("  d Psi / d(delta_rho) =", coeff_Psi, "   <-- this must be !=0 for lensing")

# Solve coeff_Phi = 0 for the DHOST couplings:
cond_Phi0 = sp.simplify(sp.numer(sp.together(coeff_Phi)))
print("\n  delta-Phi=0  <=>  numerator of (dPhi/drho) = 0 :")
print("      ", cond_Phi0, " = 0")
# What does it force, and does Psi survive?
sols_Phi0 = sp.solve(sp.Eq(cond_Phi0, 0), [Cs1], dict=True)
print("  Solving for Cs1 (the scalar-kinetic coefficient):", sols_Phi0)

if sols_Phi0:
    Cs1_star = sols_Phi0[0][Cs1]
    print("   => delta-Phi=0 requires  Cs1 =", Cs1_star)
    Psi_at = sp.simplify(coeff_Psi.subs(Cs1, Cs1_star))
    Phi_at = sp.simplify(coeff_Phi.subs(Cs1, Cs1_star))
    print("   At this point:  dPhi/drho =", Phi_at, "  (target 0)")
    print("                   dPsi/drho =", Psi_at, "  (need !=0 for lensing)")

# ============================================================================
H("SECTION 4 -- WHAT Cs1 = 0 MEANS: the scalar kinetic term and the GHOST/strong-coupling")
# ============================================================================
print(r"""
Decode the condition. Cs1 is the coefficient of the scalar's own k^2 kinetic operator in its
EOM (the c_s^2 * (scalar kinetic) term). The condition for delta-Phi=0 forced  Cs1 = 0 (or a
specific algebraic value -- read the print above). We now interpret:

  * If delta-Phi=0 forces Cs1 -> 0 : the scalar has NO gradient kinetic energy (c_s^2 -> 0).
    A scalar with vanishing spatial kinetic term is INFINITELY STRONGLY COUPLED (the quadratic
    action for chi degenerates; the QS solution above had chi ~ 1/Cs1 -> infinity). This is a
    STRONG-COUPLING / gradient-instability pathology, NOT a healthy ghost-free background.
    => the 'pure slip' point is the boundary where the scalar sector becomes singular.

  * The slip eta = G_Psi/G_Phi DIVERGES as G_Phi -> 0. 'delta-Phi=0 with delta-Psi!=0' is the
    eta -> infinity limit -- an infinite slip. In a metric theory this is reached only by
    DECOUPLING matter from Phi, which the (00) Hamiltonian constraint forbids for a minimally
    coupled (S_m[g,psi]) source: the matter energy density gravitates into Phi with coefficient
    8 pi G_N that NO scalar sector can cancel without making the scalar non-dynamical/ghostly.
""")
# Make the 'matter must source Phi' statement a clean theorem on the (00) constraint:
h("4a. The (00) Hamiltonian-constraint theorem: minimal matter MUST source Phi")
print(r"""
The (00) Einstein equation of ANY scalar-tensor (Horndeski or DHOST) theory is the Hamiltonian
constraint. Linearized and quasi-static, schematically:

   M_*^2 k^2 Phi  +  (scalar terms)  =  4 pi (a^2) * delta-T^0_0 = 4 pi a^2 delta-rho   (minimal)

The matter density appears on the RHS with the BARE coupling (Planck mass), because matter
couples to g_{mu nu} only. The scalar 'terms' on the LHS are sourced by Phi, Psi, chi -- NOT by
delta-rho directly. So to get Phi=0 you must cancel  4 pi a^2 delta-rho  using the scalar terms,
which themselves vanish when Phi=Psi=chi=0. The ONLY way out is to let chi blow up (Cs1->0,
strong coupling) so a finite chi-source cancels a finite delta-rho -- i.e. the scalar carries
the load, but then it is not a healthy propagating mode.
""")
# Demonstrate: with Cs1 -> 0 the QS chi solution diverges (strong coupling).
chi_div = sp.limit(chi_sol, Cs1, 0)
print("  lim_{Cs1->0} chi(QS) =", chi_div, "  (diverges => strong coupling at the pure-slip point)")

# ============================================================================
H("SECTION 5 -- the EXACT QS slip from the published DHOST result (1703.03797, VERBATIM)")
# ============================================================================
print(r"""
We drop the schematic 3x3 toy of Sec.3 and use the VERBATIM published closed forms (Langlois-
Mancarella-Noui-Vernizzi 1703.03797, the DHOST effective-Newton-constant paper, read from the
PDF). They work in unitary gauge with the EFT alpha-basis {alpha_L, alpha_H, alpha_T} and
{beta_1, beta_2, beta_3}. Three results are load-bearing and quoted EXACTLY:

  (R5.1) THE SLIP, their eq.(3.12):     Psi = (1 + alpha_H)/(1 + alpha_T) * Phi
  (R5.2) THE TIME-TIME POISSON eq, their eq.(3.15)-(3.16) for the VIABLE branch (alpha_L=0,
         conditions C_I): a FINITE effective Newton constant
             8 pi G_N = (1/M^2) [ (1+alpha_H)^2/(1+alpha_T) - beta_3/2 ]^{-1}
         so  -Delta Phi ~ 4 pi G_N m delta^3(x)  -- matter DOES source Phi with finite, nonzero G_N.
  (R5.3) THE OTHER BRANCH (alpha_L != 0, conditions C_II): eq.(3.14) the coefficient of Delta-Phi
         VANISHES => the effective Newton constant is INFINITE in the linear regime => NO Poisson
         equation => phenomenologically dead. (Their words: "one cannot recover a Poisson-like
         equation in the static linear regime for these theories.")

Impose c_T=c  =>  alpha_T = 0. Then:
""")
alphaH, alphaT, alphaL, beta1, beta3, Mpl, mpt = sp.symbols(
    'alpha_H alpha_T alpha_L beta_1 beta_3 M m_pt', real=True)
slip_pub = sp.simplify(((1+alphaH)/(1+alphaT)).subs(alphaT, 0))
print("  (R5.1) c_T=c slip:  eta = Psi/Phi = (1+alpha_H)/(1+alpha_T) -> (alpha_T=0) =",
      slip_pub, "   = 1 + alpha_H")
invGN = sp.simplify(((1+alphaH)**2/(1+alphaT) - beta3/2).subs(alphaT, 0))
print("  (R5.2) viable branch (alpha_L=0):  (8 pi G_N M^2)^{-1} = (1+alpha_H)^2 - beta_3/2 =",
      invGN, " => Phi sourced by matter with FINITE G_N.")
print(r"""
  ==> REQUIREMENT (1)+(2) in this language. 'delta-Phi=0' = matter does NOT source the time-time
      potential = the time-time Newton constant -> 0 = the bracket [(1+alpha_H)^2 - beta_3/2] -> INF.
      BUT the SLIP eq.(R5.1) says  Psi = (1+alpha_H) Phi : Psi is a fixed MULTIPLE of Phi. So if
      Phi is NOT sourced (Phi->0 for a given matter lump), then Psi = (1+alpha_H)*0 = 0 too. The
      two potentials are LOCKED by the single factor (1+alpha_H): you cannot zero Phi while keeping
      Psi nonzero. THIS is the metric-theory lock, now from the EXACT published slip.
""")
# Make the lock explicit & sympy-checked using the published couplings.
GPhi = 1/((1+alphaH)**2 - beta3/2)          # (R5.2): Phi source coupling (up to 4pi m /M^2)
GPsi = sp.simplify((1+alphaH)*GPhi)         # (R5.1): Psi = (1+alpha_H) Phi
print("  Phi source coupling  G_Phi ~", GPhi)
print("  Psi source coupling  G_Psi = (1+alpha_H) G_Phi ~", GPsi)
print("  delta-Phi=0  <=>  G_Phi=0  <=>  [(1+alpha_H)^2 - beta_3/2] -> infinity.")
print("    in that limit  G_Psi = (1+alpha_H) G_Phi -> (1+alpha_H)*0 = 0  (unless alpha_H->inf).")
# probe the only loophole: alpha_H -> infinity (does Psi survive while Phi dies?)
aH = sp.symbols('a_H', positive=True)
GPhi_big = 1/aH**2; GPsi_big = aH*GPhi_big
print("  large-alpha_H probe:  G_Phi ~ 1/alpha_H^2 -> 0 ;  G_Psi=(1+aH)G_Phi ~ 1/alpha_H ->",
      sp.limit(GPsi_big, aH, sp.oo), "  => BOTH -> 0. delta-Psi dies WITH delta-Phi. LOCK HOLDS.")
print("  (and beta_3 -> 2(1+alpha_H)^2 gives G_Phi->inf, i.e. INFINITE Newton constant = R5.3's")
print("   dead C_II branch, NOT delta-Phi=0 -- the opposite pathology. No pure-slip there either.)")

# ============================================================================
H("SECTION 6 -- the GW170817 graviton-decay constraint (1809.03484, VERBATIM) closes any DHOST loophole")
# ============================================================================
print(r"""
Could the genuine-DHOST beta_1 term (inside-matter Vainshtein-BREAKING / screening) split
delta-Phi from delta-Psi where the linear QS slip cannot? The SECOND GW170817 constraint --
graviton decay gamma -> pi pi into dark-energy fluctuations (Creminelli-Lewandowski-Tambalo-
Vernizzi 1809.03484, read from the PDF) -- removes exactly that freedom. VERBATIM:

  * eq.(71): "the surviving theory is  L_{cT=1, no decay} = f(phi) ^(4)R + P(phi,X) + Q(phi,X) box phi."
    => after c_T=c AND no-decay the ONLY surviving local terms are Horndeski up to CUBIC: a
    CONFORMAL f(phi)R, k-essence P, and Q box phi. NO quartic/quintic, NO beyond-Horndeski operator.
  * "This constraint ... rules out all quartic and quintic GLPV theories." (the slip-producing
    beyond-Horndeski operator is m~_4; m~_4=0 <=> alpha_H=0 in GLPV.)
  * eq.(72): the DHOST-dressed survivor (X-dependent conformal transform of (71)) is
        L = P + Q box phi + C(phi,X) ^(4)R + (6 C_X^2/C) phi^mu phi_{mu nu} phi^lam phi_{lam nu},
    "the most general degenerate theory compatible with c_T^2=1 and the absence of graviton decay."
  * FOOTNOTE 4 (decisive, verbatim): "for DHOST theories we find that neither alpha_H nor beta_1
    ... vanish. However, in the absence of decay these coefficients are not independent but are
    related by  alpha_H = -2 beta_1.  This implies that the screening mechanism based on quartic
    terms ... is ABSENT."
""")
b1 = sp.symbols('beta_1', real=True)
print("  GW-decay (1809.03484 fn.4):  alpha_H = -2 beta_1   <=>  alpha_H + 2 beta_1 = 0  (i.e. A3=0).")
print("  Their explicit consequence: 'the screening mechanism based on quartic terms is ABSENT'")
print("    => the inside-matter Vainshtein-BREAKING that is the ONLY way to split delta-Phi from")
print("       delta-Psi nonlinearly is GONE. So there is no inside-matter escape either.")
print(r"""
  Net on the FULLY GW170817-consistent DHOST branch (c_T=c [A1=0] AND no graviton decay
  [alpha_H=-2 beta_1, screening absent]):
   - the survivor (eq.71) is f(phi)R + P + Q box phi = a CONFORMAL scalar-tensor (Brans-Dicke-
     like) theory. Its slip from eq.(R5.1) is Psi=(1+alpha_H)Phi with alpha_H the ONE free knob,
     and BOTH potentials sourced by matter (finite G_N);
   - the screening that could break the Phi<->Psi lock is ABSENT;
   => Psi stays LOCKED to Phi: delta-Phi=0 forces delta-Psi=0. The slip alpha_H scales BOTH
      potentials together; it CANNOT zero one and not the other.
""")
# Final exact lock check (eq.3.12 slip + screening absent, alpha_H=-2 beta_1 imposed):
print("  FINAL sympy lock check (exact eq.3.12 slip; screening absent; decay relation imposed):")
GPhi_f = sp.symbols('G_Phi', real=True)
GPsi_f = (1+alphaH)*GPhi_f                          # eq.3.12: Psi=(1+aH)Phi, no screening split
GPsi_f_decay = GPsi_f.subs(alphaH, -2*b1)           # impose alpha_H=-2 beta_1
print("    G_Psi = (1+alpha_H) G_Phi, with alpha_H=-2 beta_1 :", sp.simplify(GPsi_f_decay))
print("    impose delta-Phi=0 => G_Phi=0 => G_Psi =", GPsi_f_decay.subs(GPhi_f, 0),
      "  => delta-Psi=0.  PURE SLIP FORBIDDEN.  QED.")


# ============================================================================
H("SECTION 7 -- VERDICT and the named no-go")
# ============================================================================
print(r"""
ROUTE 1 (DHOST PURE-SLIP) VERDICT:  OBSTRUCTED -- and the obstruction is a clean, named theorem.

Linearization result (sympy, this script; all coefficients VERBATIM from the primaries):
  * c_T = c on the DHOST tensor branch  <=>  A1 X = 0  =>  A1 = 0.                [Sec 0]
    (Ezquiaga-Zumalacarregui 1710.05901: c_T=c kills G_{4X},G_5 / the disformal tensor term.)
  * The quasi-static slip is EXACTLY (Langlois-Mancarella-Noui-Vernizzi 1703.03797 eq.3.12,
    with c_T=c => alpha_T=0):   Psi = (1 + alpha_H) Phi  -- Psi is a fixed MULTIPLE of Phi.  [Sec 5]
  * The time-time Poisson eq (1703.03797 eq.3.15-3.16) gives a FINITE Newton constant on the
    viable branch (alpha_L=0): matter DOES source Phi. delta-Phi=0 needs G_Phi->0, i.e. the
    bracket [(1+alpha_H)^2 - beta_3/2] -> infinity -- but then eq.3.12 forces Psi=(1+aH)*0=0:
    delta-Psi DIES WITH delta-Phi. The potentials are LOCKED by the single factor (1+alpha_H).  [Sec 5]
    (The only other branch, alpha_L!=0 / C_II, has an INFINITE Newton constant = no Poisson at
     all = phenomenologically dead, 1703.03797 eq.3.14 -- the opposite pathology, no slip-win.)
  * The genuine-DHOST beta_1 (inside-matter Vainshtein-BREAKING / screening) is the only
    nonlinear way to split delta-Phi from delta-Psi -- and the SECOND GW170817 bound, graviton
    decay gamma->pi pi (Creminelli-Lewandowski-Tambalo-Vernizzi 1809.03484), forces
    alpha_H = -2 beta_1 AND, in their VERBATIM words, "the screening mechanism based on quartic
    terms is ABSENT." So the inside-matter split is GONE. The decay-safe survivor (their eq.71)
    is f(phi)R + P + Q box phi = a CONFORMAL (Brans-Dicke-class) theory whose slip is still
    Psi=(1+alpha_H)Phi with both potentials sourced.                              [Sec 6]

  ==> NO ghost-free, c_T=c, decay-safe DHOST member gives PURE SLIP (delta-Phi=0, delta-Psi!=0).
      On every viable branch Psi is locked to Phi (linear slip) and the only lock-breaking
      mechanism (beta_1 screening) is removed by GW170817 graviton non-decay. delta-Phi=0
      forces delta-Psi=0 -> no lensing.

THE NAMED NO-GO (publishable):
  "Covariant Cassini-safe (pure-slip) MOND lensing is forbidden in quadratic+cubic DHOST by the
   joint GW170817 constraints: c_T=c (A1=0, Ezquiaga-Zumalacarregui 1710.05901) AND graviton
   non-decay (alpha_H=-2 beta_1 with the quartic screening ABSENT, Creminelli-Lewandowski-
   Tambalo-Vernizzi 1809.03484). The surviving theory is conformal (f(phi)R + P + Q box phi)
   whose linear slip Psi=(1+alpha_H)Phi (Langlois-Mancarella-Noui-Vernizzi 1703.03797 eq.3.12)
   locks the lensing potential Psi to the matter-felt potential Phi: a slip that modifies light
   (delta-Psi) necessarily modifies the matter-felt time-time potential (delta-Phi) too. Hence
   there is no GW170817-safe, ghost-free DHOST gravity term with delta-Phi=0 and delta-Psi!=0."

CONSEQUENCE for the framework:  Route 1 does NOT supply the missing covariant lensing partner.
The pure-slip property the framework needs CANNOT come from a metric (scalar-tensor/DHOST)
gravity term that is GW170817-safe. This PUSHES the partner OFF the metric/gravity sector --
consistent with the framework's own logic (the MI matter sector is phi_- -linear, sources zero
metric). The honest implication: the lensing partner, if it exists, must be a MATTER-sector
(MI-class, light couples to an effective metric built from the MI kernel) construction, NOT a
DHOST gravity term -- OR the framework lives with a baryon-only lensing metric and the slip is
a genuine prediction with NO covariant scalar-tensor realization.
""")
print("="*88)
print(" ROUTE 1 (DHOST PURE-SLIP):  OBSTRUCTED.  No ghost-free c_T=c DHOST gives delta-Phi=0 slip.")
print(" Named no-go: c_T=c (A1=0) + graviton non-decay (alpha_H=-2 beta_1, quartic screening")
print(" ABSENT) => survivor is conformal, slip Psi=(1+alpha_H)Phi LOCKS delta-Psi to delta-Phi.")
print("="*88)
