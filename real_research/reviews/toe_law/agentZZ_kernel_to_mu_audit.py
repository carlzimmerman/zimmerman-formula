#!/usr/bin/env python3
"""
agentZZ_kernel_to_mu_audit.py  --  THE HONEST AUDIT (both ways)

The construction in agentZZ_inin_worldline_pillar1.py VERIFIED everything that
is a CONSEQUENCE of mu_fw. The make-or-break question for "Pillar 1 as a concrete
action" is the one step that was NOT verified there:

   Does the dS influence-functional kernel (Deser-Levin chord, Galley physical
   limit) DERIVE the interpolation function mu_fw(x)=(sqrt(1+4x^2)-1)/(2x),
   or is mu_fw inserted by hand?

This is the crux. A linear (Gaussian/Caldeira-Leggett) influence functional is
LINEAR in the worldline coordinate after the physical limit -> it gives a
LINEAR friction/inertia correction  m_eff = m(1 + const), NOT a nonlinear
mu(a/a0). So a STANDARD FV influence functional can only give a LINEAR (constant)
inertia renormalization, never the nonlinear MOND interpolation. The nonlinearity
has to come from somewhere. Audit exactly where.
"""
import sympy as sp

print("="*78)
print("AUDIT: can the Gaussian dS influence functional give NONLINEAR mu_fw?")
print("="*78)

# ---------------------------------------------------------------------------
# A linear (Gaussian) influence functional in the physical limit yields an
# EOM of the form  m xddot + int dt' gamma(t-t') xdot(t') = F.  In frequency
# space that is  [ -m w^2 - i w gamma~(w) ] x~(w) = F~.  For a CONSTANT-acc /
# adiabatic (low-w) bath this is a LINEAR, FREQUENCY-LOCAL renormalization of
# m:  m -> m_eff = m + (real const).  It CANNOT produce a dependence on the
# AMPLITUDE |a| -- i.e. it cannot give mu(|a|/a0). Show this explicitly.
# ---------------------------------------------------------------------------
m, w, gam, t, a, a0 = sp.symbols('m omega gamma t a a0', positive=True)
x_w, F_w = sp.symbols('x_w F_w')
# linear-response EOM in frequency space (gamma~ = const adiabatic limit):
lhs = (-m*w**2 - sp.I*w*gam)*x_w
print("Linear FV EOM (freq space):  (-m w^2 - i w gamma~) x~ = F~")
print("  => m_eff(w) = m + i gamma~/w :  a LINEAR, amplitude-INDEPENDENT shift.")
print("  => NO dependence on |a|/a0.  A purely Gaussian dS influence functional")
print("     CANNOT by itself produce the nonlinear mu_fw(|a|/a0).")

print("""
WHERE THE NONLINEARITY MUST COME FROM (honest):
  mu_fw(x) = (sqrt(1+4x^2)-1)/(2x) is nonlinear in a. To get it from the
  worldline picture you need ONE of:
   (a) a NONLINEAR coupling g(a) to the bath (the coupling itself depends on
       the instantaneous acceleration via T_eff(a)), OR
   (b) a SELF-CONSISTENT / non-Gaussian resummation where the bath temperature
       T_eff = (1/2pi)sqrt(a^2 + (cH)^2) feeds back on the response (the
       'thermal mass' depends on a), OR
   (c) the mu_fw is POSTULATED as the modified-inertia response built on T_eff,
       and the worldline action only supplies its FORM (a^2 + (cH)^2 under a
       sqrt) plus the active/nonlocal/preferred-frame STRUCTURE.
  Option (c) is what the framework actually has. The honest status: the
  worldline construction DERIVES the STRUCTURE (sqrt(a^2+(cH)^2) floor, the
  active kernel, the preferred frame, the v^4 law in the deep limit) but
  IMPORTS the specific algebraic mu_fw -- it is not forced by the Gaussian
  influence functional alone.
""")

# ---------------------------------------------------------------------------
# Check the ONE thing the kernel DOES force without importing mu_fw: the
# combination sqrt(a^2 + (cH)^2). The Deser-Levin a5 = sqrt(a^2+H^2) is the
# UNIQUE invariant the worldline bath supplies (the 5-acceleration). Show that
# the deep-MOND scale a0 emerges as the acceleration where the H-floor takes
# over -- this IS forced (it is the a -> 0 limit of a5).
# ---------------------------------------------------------------------------
print("-"*78)
print("WHAT IS FORCED (no mu_fw imported): the sqrt(a^2+(cH)^2) floor & a0~cH")
print("-"*78)
c, H, Lam = sp.symbols('c H Lambda', positive=True)
a5 = sp.sqrt(a**2 + (c*H)**2)
print("DL 5-acceleration / bath invariant:  a5 =", a5)
print("  a -> 0 :  a5 -> cH  (the pure-dS floor; sets the MOND scale a0 ~ cH).")
print("  This floor IS forced by the bath (Deser-Levin Eq.8). The PROPORTIONALITY")
print("  a0 = c^2 sqrt(Lambda/32pi) (the sqrt(1/32pi) = the kernel normalization)")
print("  is the '√π wall' content -- forced in FORM (a0 ~ sqrt(Lambda)) but the")
print("  exact 1/sqrt(32pi) is the un-forced coefficient (prior corpus result).")

print("\n"+"="*78)
print("HONEST VERDICT ON PILLAR 1 (this step):")
print("="*78)
print("""
DERIVED by the worldline in-in action (forced):
  - the doubled in-in action + FV influence functional STRUCTURE (Galley Eq.5)
  - the bath = KMS-thermal at sqrt(a^2+(cH)^2) (Deser-Levin Eq.8) -- the FLOOR
  - the kernel is ACTIVE (time-antisymmetric, nonlocal) -- no passive/local home
  - a preferred frame u^mu (the dS-bath rest frame, unit-timelike)
  - deep-limit v^4 = G M a0 GIVEN the deep-MOND mu -> a/a0

IMPORTED (not forced by the Gaussian influence functional):
  - the SPECIFIC algebraic mu_fw(x)=(sqrt(1+4x^2)-1)/(2x). A linear (Gaussian)
    FV functional gives only a LINEAR inertia shift; the nonlinear mu_fw needs a
    nonlinear/self-consistent coupling that the framework POSTULATES (built on
    T_eff), not derives. This is the SAME '8th non-closure / coefficient' gap the
    prior corpus already found -- the worldline integral is REAL as a MECHANISM
    but does not FORCE the coefficient/interpolation.

NET (this step):  Pillar 1 is constructed as a concrete action with the right
STRUCTURE and verified limits, but the nonlinear interpolation is imported, not
derived. STATUS = STRUCTURE DERIVED / INTERPOLATION IMPORTED.
""")
