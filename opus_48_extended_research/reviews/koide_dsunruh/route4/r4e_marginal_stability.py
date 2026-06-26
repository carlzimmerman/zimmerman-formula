#!/usr/bin/env python3
"""
ROUTE 4 (e) -- MARGINAL STABILITY / SPECIAL-GEOMETRY check (the last genuinely-distinct angle).

A fixed point can be selected NOT by being the min of a tuned potential, but by being a point
of MARGINAL STABILITY (a Hessian zero-mode, a second-order transition, a bifurcation), or a
point of SPECIAL GEOMETRY (where the orbit/stabilizer dimension jumps). These are DEFINITION-
FREE selectors: they don't need a 2/3 input, they are intrinsic features of the configuration
space. So: is r=sqrt2 (cos^2=1/2, theta=45deg) a special point of the flavor-vector geometry
in ANY of these intrinsic senses?

We check, sympy-exact, every intrinsic 'special' structure r could sit at:
  (1) Positivity boundary (smallest sqrt-mass -> 0): r boundary. Where is it? (=2, not sqrt2)
  (2) Orbit/stabilizer jump (enhanced symmetry): at which r does the S3 stabilizer enlarge?
  (3) Hessian degeneracy of |std|^2/|dem|^2 or of Q: is r=sqrt2 a marginal/critical point?
  (4) The 'democratic = standard length' self-dual point: special? (=sqrt2 but = the target,
      already shown a re-labeling in 4c)
  (5) Curvature/inflection of Q(r): any distinguished r?
The bar: an intrinsic special point at r=sqrt2 that is NOT 'equal partition' (which = the
target) would be a real lead. We expect: the intrinsic special points are r=0 (max symmetry),
r=1 (all-positive boundary for all phases), r=2 (one component vanishes / Q=1 max breaking) --
NONE at sqrt2.
"""
import sympy as sp
mp_dps = 40
import mpmath as mp
mp.mp.dps = mp_dps

print("="*80)
print("ROUTE 4(e) -- is r=sqrt2 an INTRINSIC special point (marginal stability/geometry)?")
print("="*80)

M, r, d = sp.symbols('M r delta', positive=True)
ks = [0,1,2]
sqrt_m = [M*(1 + r*sp.cos(2*sp.pi*k/3 + d)) for k in ks]

# ---------------------------------------------------------------------------
# (1) POSITIVITY boundaries. sqrt(m_i) >= 0 requires 1 + r cos(phi_k) >= 0.
#     - all-phase-positive (any delta): worst cos=-1 -> r<=1. Boundary r=1.
#     - one sqrt-mass exactly zero: 1 + r cos(phi)=0 for some sampled phase.
#       The Koide leptons have delta s.t. the smallest entry is small but >0.
#     Where does an entry vanish? At r=2, the entry with cos=-1/2 vanishes:1+2*(-1/2)=0.
# ---------------------------------------------------------------------------
print("\n(1) Positivity boundaries of the circulant:")
print("    all-phase-positive boundary: r=1 (worst cos=-1).")
# the delta=0 representative: entries 1+r*cos(0)=1+r, 1+r*cos(2pi/3)=1-r/2, 1+r*cos(4pi/3)=1-r/2
e0 = 1 + r*sp.cos(0); e1 = 1 + r*sp.cos(2*sp.pi/3); e2 = 1 + r*sp.cos(4*sp.pi/3)
print("    delta=0 entries:", sp.simplify(e0), sp.simplify(e1), sp.simplify(e2))
rz = sp.solve(sp.Eq(sp.simplify(e1), 0), r)
print("    smallest entry (1 - r/2) = 0  at r =", rz, "  -> r=2 (Q=1, one sqrt-mass vanishes).")
print("    => positivity special points: r=1 and r=2. NEITHER is sqrt2. r=sqrt2 sits BETWEEN,")
print("       an ordinary interior value, NOT a positivity boundary. (Confirms banked.)")

# ---------------------------------------------------------------------------
# (2) ORBIT / STABILIZER jump. The S3 (permutation) stabilizer of the sqrt-mass vector:
#     - generic v: trivial stabilizer.
#     - two entries equal: Z2 stabilizer (enhanced).
#     - all three equal (r=0): full S3.
#     At which r do two entries coincide (enhanced symmetry)? For delta=0, e1=e2 always
#     (two equal) -> that is a delta-CHOICE, not an r value. The r-driven coincidences:
#     e0=e1: 1+r = 1-r/2 -> r=0. So enhanced symmetry only at r=0. No jump at sqrt2.
# ---------------------------------------------------------------------------
print("\n(2) Stabilizer/orbit jump (enhanced permutation symmetry):")
print("    entries coincide (beyond the delta-forced pair) only at r=0 (full S3).")
sol_coinc = sp.solve(sp.Eq(sp.simplify(e0), sp.simplify(e1)), r)
print("    e0=e1 at r =", sol_coinc, " (=0). No symmetry-enhancement at r=sqrt2.")
print("    => the orbit dimension is constant for r in (0,2); r=sqrt2 is NOT a stabilizer jump.")

# ---------------------------------------------------------------------------
# (3) HESSIAN / marginal stability of the shape functionals. Q(r)=1/3+r^2/6 and the
#     partition ratio P(r)=r^2/2 are both smooth monotone with constant 2nd derivative ->
#     NO inflection, NO Hessian zero, NO marginal point anywhere. A bifurcation/2nd-order
#     transition needs a sign change in a 2nd derivative; there is none. r=sqrt2 is not
#     marginal in any intrinsic functional of the shape.
# ---------------------------------------------------------------------------
print("\n(3) Marginal stability / inflection of shape functionals:")
Q_r = sp.Rational(1,3) + r**2/6
P_r = r**2/2
print("    Q(r)=1/3+r^2/6:  Q'=", sp.diff(Q_r,r), " Q''=", sp.diff(Q_r,r,2), " (const>0, no inflection)")
print("    P(r)=r^2/2:      P'=", sp.diff(P_r,r), " P''=", sp.diff(P_r,r,2), " (const>0, no inflection)")
print("    => no Hessian zero-mode, no bifurcation, no 2nd-order transition at ANY r, incl sqrt2.")
print("       r=sqrt2 is NOT a point of marginal stability. (No definition-free selector here.)")

# ---------------------------------------------------------------------------
# (4) The democratic=standard 'self-dual' point r=sqrt2: IS special, but = equal partition
#     = cos^2=1/2 = the TARGET (logically identical to Q=2/3), already a re-labeling (4c).
#     The ONLY intrinsic sense in which sqrt2 is special is 'the two S3-reps carry equal
#     length' -- which is precisely the statement Q=2/3, not an independent selector.
# ---------------------------------------------------------------------------
print("\n(4) Self-dual point r=sqrt2 (|std|=|dem|): the ONE intrinsic specialness it has is")
print("    'equal length in trivial vs standard rep' == cos^2=1/2 == Q=2/3 (re-labeling, 4c).")
print("    It is NOT a positivity boundary, NOT a symmetry-enhancement, NOT a marginal/")
print("    bifurcation point. So NO definition-free intrinsic selector lands at sqrt2 except")
print("    the one that IS the target restated.")

# ---------------------------------------------------------------------------
# (5) SUMMARY TABLE of intrinsic special r values
# ---------------------------------------------------------------------------
print("\n(5) Intrinsic special r-values of the circulant flavor geometry:")
print("    r=0    : full S3 (democratic), Q=1/3   -- a real fixed point (max symmetry)")
print("    r=1    : all-phase positivity boundary, Q=1/2")
print("    r=2    : one sqrt-mass vanishes, Q=1    -- max breaking boundary")
print("    r=sqrt2: ONLY 'equal rep-length' (=the target Q=2/3); NOT a boundary/jump/marginal pt")
print("    => the genuine intrinsic fixed/critical points are r=0,1,2 -- NOT sqrt2.")

print("""
[VERDICT 4e] r=sqrt2 is NOT an intrinsic (definition-free) special point:
  - positivity boundaries are r=1 and r=2; r=sqrt2 is an ordinary interior value;
  - no stabilizer/orbit jump at sqrt2 (enhanced symmetry only at r=0);
  - no Hessian zero / inflection / bifurcation at any r (Q,P have constant +curvature);
  - the only sense sqrt2 is 'special' is |std|=|dem| = equal partition = the target Q=2/3
    restated (a re-labeling). No marginal-stability / special-geometry selector exists.
  Combined with 4a-d: the last door (variational/fixed-point/stability in the FLAVOR sector)
  is CLOSED. r=sqrt2 is a free modulus; every selector either smuggles 2/3 or is flavor-blind
  (cross-fermion falsified) with no derived lepton-specific ingredient (neutrinos colorless
  but non-Koide). NULL -- the honest expected result. SM mass sector stays WALLED.
""")
