#!/usr/bin/env python3
"""
CIRCULARITY AUDIT, computational part.
Resolve the v <-> theta <-> E map of 2312.04097, and check the TWO
independent placements against each other:

  (P1) Conical-deficit map (2312.04097):  pi*v = pi - 2*theta,  v ~ p*alpha,
       alpha = 2pi(1 - sqrt(1-8GM)) ~ 8 pi G M  (small M).
       Energy: E = E0 cos(theta).  v=1 is stated to be the EDGE (max energy).

  (P2) Chord-number map (my independent rederivation):
       n=0 -> spectral CENTER (E~0);  n->inf -> spectral EDGE.

The audit question: where does the de Sitter VACUUM (empty static patch) sit,
and is that placement DERIVED from the chord algebra or ASSUMED by choosing a
dictionary?
"""
import numpy as np
import sympy as sp

print("="*78)
print("STEP 1: v <-> theta <-> E from 2312.04097's own relation pi v = pi - 2 theta")
print("="*78)
v, th = sp.symbols('v theta', positive=True)
# pi v = pi - 2 theta  =>  theta = (pi/2)(1 - v)
theta_of_v = sp.pi/2 * (1 - v)
print(f"  theta(v) = (pi/2)(1 - v)")
for vv in [0, sp.Rational(1,2), 1]:
    th_val = theta_of_v.subs(v, vv)
    E_over_E0 = sp.cos(th_val)
    print(f"   v={vv}:  theta={th_val} = {float(th_val):.4f} rad,  E/E0=cos(theta)={float(E_over_E0):+.4f}")
print("""
  READ-OFF of P1:
    v=0  -> theta=pi/2 -> E/E0 = cos(pi/2) = 0   => SPECTRAL CENTER (E=0)
    v=1  -> theta=0    -> E/E0 = cos(0)    = 1   => SPECTRAL EDGE (max energy)
  So in 2312.04097's parametrization:
    EMPTY dS (M=0 => alpha=0 => v=0) sits at the SPECTRAL CENTER E=0.
    FINITE backreaction (alpha>0 => v>0) MIGRATES toward v=1 = the EDGE.
  This is INTERNALLY CONSISTENT with the verbatim quote
  'states with finite backreaction migrate toward v=1 ... the edge'.
""")

print("="*78)
print("STEP 2: Numbers -- where does a galaxy's conical deficit land, p=1 vs p->inf")
print("="*78)
c = 2.998e8; G_N = 6.674e-11; Msun = 1.989e30
a0 = 9.36e-11
Z = np.sqrt(32*np.pi/3)
H_Lambda = a0 * Z / c
M_dS = c**2 / (G_N * H_Lambda)
print(f"  a0={a0:.3e}, Z={Z:.4f}, H_Lambda={H_Lambda:.3e} /s")
print(f"  M_dS = c^2/(G H_Lambda) = {M_dS:.3e} kg = {M_dS/Msun:.3e} Msun")
def alpha_of_M(Mkg):
    arg = 1 - 8*G_N*Mkg/(c**2) * (H_Lambda/c)*0 # placeholder; use small-M closed form below
    return None
# small-M: alpha/2pi = M/M_dS  (consistent with finder)
print(f"\n  {'object':>12}{'M(Msun)':>10}{'alpha/2pi=M/MdS':>18}{'v(p=1)':>12}{'E/E0(p=1)':>12}{'v(p=1e6)':>12}")
for nm,Ms in [("spiral",3e10),("MW",1e11),("massive",1e12),("cluster",1e15)]:
    Mkg=Ms*Msun
    a2pi = Mkg/M_dS
    alpha = 2*np.pi*a2pi
    v_p1 = 1.0*alpha
    E_p1 = np.sin(0.5*np.pi*min(v_p1,1.0))  # E/E0 = cos(theta)=cos((pi/2)(1-v))=sin((pi/2)v)
    v_pbig = min(1e6*alpha, 1.0)
    print(f"  {nm:>12}{Ms:>10.0e}{a2pi:>18.3e}{v_p1:>12.3e}{E_p1:>12.3e}{v_pbig:>12.3e}")
print("""
  => At p=1: galaxies E/E0 ~ 1e-6..1e-3 (CENTER). At p=1e6: v->1 (EDGE).
     p-dependent and undetermined -- EXACTLY the finder's Axis-2 result.
""")

print("="*78)
print("STEP 3: THE SMUGGLE TEST -- does 'singlet escapes deep into bulk' = spectral center?")
print("="*78)
print("""  Two facts now in hand:
   FACT A (2401.08555, verbatim): singlets 'escape the near horizon region and
           propagate DEEP INTO THE BULK' (toward the pode). 'Deep into the bulk'
           = large geodesic length from the horizon = LARGE chord number n.
   FACT B (my Step-2 rederivation, triple-verified): LARGE chord number n
           -> spectral EDGE (RMS|E|/E0 -> 0.707, peak|E/E0| -> 1).
           Small chord number n~0 (near the horizon) -> spectral CENTER E=0.

  THEREFORE: 'escape deep into the bulk pode' (spatial center) maps to the
  spectral EDGE, NOT the spectral center E=0. The horizon (n~0) is the spectral
  center. So 'the singlet escapes to the (spatial) center -> (spectral) center
  -> MOND' CONFLATES two opposite ends. It is a NON-SEQUITUR.

  CROSS-CHECK with P1 (conical deficit): empty dS (the deep, unexcited static
  patch with NO backreaction) is M=0 => v=0 => theta=pi/2 => E=0 = CENTER.
  But that is the EMPTY patch (zero chord excitation), i.e. n~0 again -- the
  near-horizon vacuum, NOT a 'deep bulk particle'. A finite-mass object that
  actually sits deep in the bulk has alpha>0 => v>0 => migrates to the EDGE.
  CONSISTENT with FACT B: the only thing at the spectral center is the EMPTY
  (n~0) limit; anything with finite backreaction/finite depth is off-center.
""")

print("="*78)
print("STEP 4: WHERE IS THE PLACEMENT DERIVED vs ASSUMED?")
print("="*78)
print("""  The map chord-number<->energy (P2) IS derived from the chord algebra
  (tridiagonal H, b_n=sqrt([n]_q)) -- I rederived it independently. That part
  is a THEOREM of the algebra.

  But it only tells you 'which chord number <-> which energy'. To get a
  PHYSICS sign you must ALSO say WHICH chord number the de Sitter VACUUM / the
  deep-MOND galaxy probe occupies. THAT identification (vacuum = n=0 = center,
  per Narovlansky-Verlinde; vs vacuum = near-edge semiclassical, per Okuyama)
  is the ASSUMED dictionary input. The chord algebra does NOT pick it.

  Confinement (2401.08555) was supposed to DERIVE this placement dynamically.
  But 2401.08555 makes NO statement linking deconfinement to E=0 (verbatim
  WebFetch confirmed). It only decides SPATIAL escape. And spatial-deep-bulk
  = spectral-EDGE (Fact B). So confinement does NOT supply the missing
  placement; if read literally it points the deep-bulk singlet to the EDGE.

  => The spectral placement enters as an ASSUMPTION (the N-V-vs-Okuyama
     dictionary choice), NOT a derivation. Both the center reading and the
     edge reading trace back to that assumed input. CONTESTED-TERMINAL.
""")
