#!/usr/bin/env python3
"""
SKEPTIC adversarial check on the aether_identification claim.
Goal: try HARDEST to show "coincidence-only" / "two separate frames".
Three attacks:
  ATTACK 1 (triviality): is C2/C3 forced for ANY rel-MOND vector, making the
           match non-diagnostic? Quantify what is trivial vs non-trivial.
  ATTACK 2 (divergence regime): find a regime where AeST's A_mu and the
           framework's u^mu MUST differ. If one exists and is physical,
           they are TWO frames, not one.
  ATTACK 3 (K(Q) pin circularity): is any proposed sqrt(Lambda)->I0 relation a
           real dS identity or a manufactured O(1)?
"""
import sympy as sp

print("="*78)
print("ATTACK 1 -- HOW MUCH OF THE C1/C2/C3 MATCH IS TRIVIAL?")
print("="*78)
print("""
 C1 (unit-timelike A^mu A_mu=-1): NOT trivial as a *match* but trivial as a
    *constraint* -- it is just normalization. ANY unit timelike vector satisfies
    it. So C1 carries ~0 bits of identification: it only says 'both are
    normalized timelike vectors', true of every observer 4-velocity. DISCOUNT.

 C2 (FLRW A_0=-N, A_i=0): on a HOMOGENEOUS+ISOTROPIC background, a unit timelike
    vector field respecting the symmetry is FORCED to be the comoving normal:
    A_i=0 by isotropy (no preferred spatial direction), A_0=-N by normalization.
    => C2 is FORCED for ANY symmetric rel-MOND aether. Non-diagnostic. DISCOUNT.
""")
# Demonstrate C2 is forced by symmetry: most general isotropy-respecting unit
# timelike vector on FLRW.
t = sp.symbols('t', real=True)
N = sp.Function('N')(t); a = sp.Function('a')(t)
A0 = sp.Function('A0')(t)
# isotropy => A_i=0 ; unit timelike with g^{00}=-1/N^2 :  g^{munu}A_mu A_nu=-1
unit = sp.Eq(-A0**2/N**2, -1)
sol = sp.solve(unit, A0)
print("  Most general isotropy-respecting unit-timelike A_mu on FLRW: A_i=0 forced,")
print("  A_0 solved from normalization =>", sol, " (=> A_0=-N is the past-directed root).")
print("  CONCLUSION: C2 is a SYMMETRY THEOREM, identical for framework AND AeST AND")
print("  EinsteinAether AND khronometric AND any covariant-MOND aether. 0 bits.\n")

print("="*78)
print("ATTACK 2 -- IS THERE A REGIME WHERE u^mu AND A_mu MUST DIVERGE?")
print("="*78)
print("""
 The non-trivial test: C3 / hypersurface-orthogonality OFF the symmetric
 background. AeST's A_mu is DYNAMICAL: its curl F_munu has a kinetic term
 (K_B/2)F^2, and a PROPAGATING transverse vector mode (omega^2=k^2+M^2). When
 that mode is EXCITED, F_ij != 0 -- A_mu acquires a TWIST and is NO LONGER
 hypersurface-orthogonal. The framework's u^mu = grad(cosmic time) is twist-free
 BY DEFINITION (it is a gradient) and can NEVER carry such a transverse mode.
 => In any process that excites the AeST vector mode (early-universe vector
 perturbations, vortical flows, the transverse polarization), AeST's A_mu and
 the framework's u^mu PHYSICALLY DIFFER. They coincide ONLY on the
 hypersurface-orthogonal (twist-free) SUBSET of AeST configurations.
""")
# Show: a gradient vector field can never have a transverse (curl) part.
x1,x2,x3 = sp.symbols('x1 x2 x3', real=True)
tau = sp.Function('tau')(x1,x2,x3)   # any scalar 'cosmic time' function
A_grad = [sp.diff(tau, v) for v in (x1,x2,x3)]
curl = [sp.simplify(sp.diff(A_grad[2],x2)-sp.diff(A_grad[1],x3)),
        sp.simplify(sp.diff(A_grad[0],x3)-sp.diff(A_grad[2],x1)),
        sp.simplify(sp.diff(A_grad[1],x1)-sp.diff(A_grad[0],x2))]
print("  curl(grad tau) =", curl, " -> identically 0 (a gradient frame has NO twist).")
print("  But AeST's A_mu has a curl kinetic term + propagating transverse mode, so")
print("  its physical config space is STRICTLY LARGER than {gradient frames}.")
print("  VERDICT ATTACK2: u^mu = a PROPER SUBSET (the twist-free sector) of A_mu's")
print("  config space. They are the SAME only where AeST's vector mode is unexcited")
print("  (FLRW bg + quasistatic). The identification is EXACT on that subset and")
print("  FAILS off it. This is the precise sense in which 'frame yes, field no'.\n")

print("="*78)
print("ATTACK 3 -- ANY sqrt(Lambda)->I0 RELATION: REAL dS IDENTITY OR MANUFACTURED?")
print("="*78)
import numpy as np
OmL=0.685; OmM=0.315; Omb=0.0493; Omdm=OmM-Omb
print(f"  Target Omega_dust = {Omdm:.4f}.  why-now ratio Omega_dust/Omega_DE={Omdm/OmL:.4f}")
print("  The decisive structural fact (NOT a numerology search): I0 is an")
print("  INTEGRATION CONSTANT of the shift-symmetric phi EOM. Lambda, a0, Z are")
print("  ACTION COUPLINGS. A theorem of ODE theory: the value of an integration")
print("  constant is set by BOUNDARY/INITIAL data, and is independent of the")
print("  equation's coefficients (the couplings). You can rescale I0 freely while")
print("  holding Lambda,a0,Z fixed and still solve the SAME EOM. Demonstrate:")
# toy: shift-symmetric EOM d/dt(a^3 dK/dQ)=0 => a^3 dK/dQ = I0 (const). I0 free.
print("    shift-symmetric EOM: d/dt(a^3 * K'(Q)) = 0  =>  a^3 K'(Q) = I0 = const.")
print("    For ANY value of I0 this is a valid solution; the couplings in K do NOT")
print("    fix I0. => rho_dust ∝ I0/a^3 has a FREE amplitude. Confirmed structurally.")
print("  Any claim 'sqrt(Lambda) pins I0' must inject an O(1) by hand =>")
print("  MANUFACTURED, not a dS identity. The de Sitter horizon length is ~10^3x the")
print("  empirical mu^-1, so even the geometric scale does not line up.")
print()
print("="*78)
print("SKEPTIC BOTTOM LINE")
print("="*78)
print("""  - C1,C2 carry ~0 identification bits (normalization + FLRW symmetry theorem).
  - The NON-trivial content is C3 *plus* the FORCING: the framework is COMPELLED
    (lensing no-go) to be preferred-frame and the dS-Unruh vacuum NAMES which
    frame (the cosmic/CMB one). That naming is what lifts this above coincidence:
    two independently-postulated frames need not agree on WHICH timelike
    direction; here the framework supplies an independent reason it is the
    cosmic-time gradient -- AeST's own quasistatic solution.
  - BUT u^mu is the TWIST-FREE SUBSET of AeST's A_mu config space; off that
    subset (excited vector mode) they differ. So 'same FRAME on the physical
    background, NOT the same dynamical FIELD'.
  - K(Q) amplitude pin: FALSE / manufactured. I0 is an integration constant,
    structurally orthogonal to the couplings Lambda,a0,Z. No dS identity ties
    them; the only 'hits' inject an O(1) by hand. NOT circular-but-true -- it is
    simply not pinned.""")
