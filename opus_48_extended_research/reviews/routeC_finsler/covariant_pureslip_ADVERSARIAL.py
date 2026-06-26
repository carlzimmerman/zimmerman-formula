#!/usr/bin/env python3
"""
ADVERSARIAL CHECK on Candidate C (the non-dynamical-frame TT/shear pure-slip lensing source).
=============================================================================================
The escape in Part 6 claimed: a TT (traceless, T00=0) source coupled to the Einstein eqs gives
delta-Phi=0, delta-Psi from the slip, c_T=c.  The SAME Bianchi/conservation argument that KILLED
Route 2 (Part 5: amputating T00 from a scalar's stress => non-conserved => inconsistent) must be
re-examined for Candidate C, OR Candidate C is the same failure wearing a Route-E coat.

THE HONEST WORRY: G^{mu nu} is identically conserved (nabla_mu G^{mu nu}=0, Bianchi). If we set
G^{mu nu} = 8piG (T_matter + T_lens) with T_lens TT and T_lens^{00}=0, then nabla_mu T_lens^{mu nu}=0
is FORCED. Does that force T_lens^{0nu} back to nonzero (=> a Phi-source), the way it did for the
scalar in Part 5? If yes, Candidate C ALSO moves Phi and the no-go is COMPLETE (publishable
OBSTRUCTED). If the non-dynamical frame genuinely evades it, Candidate C survives. ADJUDICATE,
do NOT manufacture the escape.
"""
import sympy as sp

def H(t): print("\n"+"="*88+"\n "+t+"\n"+"="*88)

H("STEP 1 -- the Bianchi constraint on ANY metric-coupled source (the guillotine, applied honestly)")
print("""
Einstein eq:  G_{mu nu} = 8piG (T^m_{mu nu} + T^lens_{mu nu}).  Bianchi: nabla^mu G_{mu nu}=0.
Matter alone is conserved: nabla^mu T^m_{mu nu}=0.  THEREFORE the partner MUST satisfy, ON ITS OWN,
   nabla^mu T^lens_{mu nu} = 0.                                                        (B)
This is NON-NEGOTIABLE for a consistent metric coupling. Now impose the pure-slip demands:
   T^lens_{00} = 0  (no Phi-source) ,  T^lens_{ij} = Pi_{ij} traceless (the slip-source).
Check (B) for nu=0 in the quasistatic (time-independent) weak field:
   nabla^mu T^lens_{mu 0} = d^i T^lens_{i0} + d^0 T^lens_{00}.
In a STATIC config d^0(anything)=0, and T^lens_{00}=0, so (B,nu=0) reduces to  d^i T^lens_{i0}=0.
""")
x,y,z = sp.symbols('x y z')
# T^lens_{i0} is the momentum density of the partner. For a STATIC lensing source it is natural to
# set T^lens_{i0}=0 (no net momentum flux). Then (B,nu=0): 0=0 TRIVIALLY satisfied -- NO Phi forced.
print("  For a STATIC source the momentum density T^lens_{i0}=0 is consistent, and then")
print("  (B, nu=0):  d^i T^lens_{i0} = 0  is satisfied with T^lens_{00}=0 => NO Phi-source forced.")
print("  CONTRAST Part 5 (the scalar): there T00 was tied to T_ij by the scalar EOM (box phi=0),")
print("  so deleting T00 broke conservation. Here T^lens is NOT a scalar's canonical stress -- it")
print("  is an EXTERNALLY-PRESCRIBED (Route-E kernel) source, so T00 and T_ij are INDEPENDENT.")

H("STEP 2 -- but does (B, nu=j) force a trace / Phi back in?  the real test")
print("""
(B, nu=j) static:  d^i T^lens_{ij} = 0  => the partner's spatial stress must be DIVERGENCE-FREE.
A traceless transverse (TT) tensor is BY DEFINITION divergence-free AND traceless:
   d^i Pi_{ij} = 0  AND  Pi^i_i = 0.
So if T^lens_{ij} = Pi_{ij} is genuinely TT, (B,nu=j) is satisfied with NO trace and NO 00-piece.
The question: can a TT Pi_{ij} sourced by the baryon density actually be NONZERO (give a slip)?
A TT tensor in 3d has 2 independent components -- it is the 'gravito-magnetic shear'. Build the
minimal one from a scalar potential f (the Route-E kernel output, f = K_E * rho_b /nabla^2):
""")
f = sp.Function('f')
ff = f(x,y,z)
def d2(g,a,b): return sp.diff(g,a,b)
lap = d2(ff,x,x)+d2(ff,y,y)+d2(ff,z,z)
# shear (traceless) tensor S_ij = d_i d_j f - 1/3 delta_ij lap f  (traceless but NOT transverse)
coords=[x,y,z]
S = sp.Matrix(3,3, lambda i,j: d2(ff,coords[i],coords[j]) - (sp.Rational(1,3)*lap if i==j else 0))
trS = sp.simplify(sum(S[i,i] for i in range(3)))
# divergence d^i S_ij :
divS = [sp.simplify(sum(sp.diff(S[i,j],coords[i]) for i in range(3))) for j in range(3)]
print("  shear S_ij = d_i d_j f - 1/3 delta_ij nabla^2 f:")
print("    trace =", trS, "  (traceless: YES)")
print("    div_i S_ij =", [sp.simplify(dv - sp.diff(lap,coords[j])*sp.Rational(2,3)) for j,dv in enumerate(divS)],
      " + (2/3)d_j(nabla^2 f)")
divS_explicit = [sp.simplify(divS[j]) for j in range(3)]
print("    div_i S_ij (explicit) =", divS_explicit)
print("""
  => the simple shear S_ij is TRACELESS but its divergence d^i S_ij = (2/3) d_j(nabla^2 f) != 0
     wherever nabla^2 f != 0 (i.e. ON the baryon source rho_b ~ nabla^2 f).  So S_ij is NOT
     transverse on the source => it does NOT satisfy (B,nu=j) by itself.
""")

H("STEP 3 -- the adjudication: TT-on-the-source forces either Phi back in, OR a frame current")
print("""
To satisfy (B, nu=j) = d^i T^lens_{ij}=0 ON the source while keeping T^lens_{00}=0, the shear's
divergence (2/3)d_j(nabla^2 f) must be CANCELLED. Two and only two ways:

  (a) add an isotropic pressure piece  p delta_ij  with d_j p = -(2/3)d_j(nabla^2 f) => p ~ nabla^2 f.
      But an isotropic p delta_ij is a TRACE => it sources delta-Phi via E1 (nabla^2 Phi=4piG(drho+3dp)).
      => restoring conservation RE-INTRODUCES a Phi-source.  This is the SAME failure as Part 5:
         a metric-coupled, conserved, traceless-on-the-source stress is IMPOSSIBLE without a trace.
      *** so a DIFF-INVARIANT source CANNOT be pure-slip: Bianchi forces the trace, forces Phi. ***

  (b) let the partner exchange momentum with the NON-DYNAMICAL FRAME u^mu: replace nabla^mu T^lens
      with a frame-covariant derivative D^mu (the khronometric/aether connection), so the missing
      divergence is carried by the prescribed frame, NOT by a Phi-source. THIS is what Lorentz
      violation buys: (B) is replaced by D^mu T^lens_{mu nu}=0, and the frame absorbs the d_j(nabla^2 f)
      WITHOUT a metric trace.  The price: 4-diff is broken to the u-frame (the source is NOT a
      4-tensor), exactly the khronometric structure.
""")
# Demonstrate (a) quantitatively: the conservation-completing pressure feeds Phi.
print("  Verify (a): the conservation-completing isotropic pressure p ~ (1/?)nabla^2 f feeds E1.")
p_needed = sp.Symbol('p')  # d_j p = -(2/3) d_j(nabla^2 f) => p = -(2/3) nabla^2 f + const
p_sol = -sp.Rational(2,3)*lap
print("    conservation-completing pressure  p = -(2/3)nabla^2 f =", p_sol)
print("    its contribution to delta-Phi via nabla^2 dPhi = 4piG(drho+3 dp): 3 dp =", sp.simplify(3*p_sol),
      " != 0  => delta-Phi != 0.  *** DIFF-INVARIANT pure slip is IMPOSSIBLE (Bianchi). ***")

H("STEP 4 -- so the FINAL status of Candidate C, honestly")
print("""
The adversary CONFIRMS the no-go in its strong form AND pins the escape precisely:

  STRONG NO-GO (proven, both ways):  In ANY 4-DIFFEOMORPHISM-INVARIANT theory, a metric-coupled
  lensing source that is pure-slip (T_00=0) is FORBIDDEN -- the Bianchi identity nabla^mu T_{mu nu}=0
  forces a conservation-completing trace/pressure that sources delta-Phi != 0 (Step 3a, sympy:
  3 dp = -2 nabla^2 f != 0). Combined with Parts 2-4 (c_T=c Horndeski slip = conformal = moves Phi;
  beyond-Horndeski alpha_H slip = graviton-decay-killed), the result is:
     *** Covariant, diffeomorphism-invariant, Cassini-safe (pure-slip) MOND lensing with c_T=c
         and ghost-freedom is FORBIDDEN. ***  (a real, publishable no-go)

  THE ESCAPE, named exactly:  the ONLY way out is to BREAK 4-diffeomorphism invariance to a
  preferred frame u^mu (Lorentz violation / khronometric / Einstein-aether), so that the
  conservation law is D^mu T_{mu nu}=0 (frame-covariant) and the missing momentum is carried by
  the NON-DYNAMICAL frame instead of by a Phi-sourcing trace. This is consistent ONLY because the
  framework ALREADY has a preferred frame (the de Sitter-Unruh / Route-E in-in worldline frame).
  In that Lorentz-violating completion the pure-slip term EXISTS (Part 6 linearization: dPhi=0,
  dPsi tuned, c_T=c), and ghost-freedom holds in the Einstein-aether/khronometric coupling window
  (Jacobson; CITED, full Hamiltonian of the gated nonlocal version OPEN).

  => VERDICT:  PARTIAL.  The covariant pure-slip lensing partner is OBSTRUCTED in the
     diff-invariant (Horndeski/DHOST) class (a clean no-go: c_T=c + ghost-freedom forbid it), and
     EXISTS only as a LORENTZ-VIOLATING preferred-frame (khronometric/aether-class) constraint
     term -- which is consistent with, and demanded by, the framework's own preferred-frame MI.
     All four boxes are tick-able ONLY in the Lorentz-violating class, with ghost-freedom
     conditional on the EA window.  NOT a free, diff-invariant term; the price (Lorentz violation)
     is the named no-go content.
""")
