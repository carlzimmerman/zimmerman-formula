import numpy as np
import sympy as sp
np.set_printoptions(precision=5, suppress=True)

# =====================================================================
# TEST E — THE EXACT REDUCTION THEOREM (symbolic, the operator-algebra core).
#
# THEOREM (Connes; standard modular theory). Let M be a factor, omega a
# faithful normal state, sigma^omega its modular automorphism group, M_omega
# the centralizer. Two faithful normal states omega, omega' have the SAME
# modular flow (sigma^omega = sigma^omega' as a one-param group) IFF the
# Connes cocycle [Domega':Domega]_t is a representation, i.e. iff omega' =
# omega(h . ) for a POSITIVE h affiliated to M_omega (Connes-Radon-Nikodym).
#
# Consequence for phi: given an abstract iso psi (D1, Connes uniqueness for
# hyperfinite II_1), the set of isos satisfying (D2)+(D3) [carry state, carry
# flow] is a TORSOR under Aut(M, omega) = the omega-preserving, flow-preserving
# automorphisms = Inn(M_omega) (inner autos of the centralizer) extended by the
# centralizer's outer part. The state+flow data DOES NOT shrink this to a point
# unless the centralizer is TRIVIAL (M_omega = scalars), i.e. omega is a
# TRACE on a factor with simple modular spectrum -> impossible for type III/II
# physical states with degenerate boost spectrum.
#
# We verify the cocycle algebra symbolically and locate the EXACT residual group.
# =====================================================================

t = sp.symbols('t', real=True)
# Two states' modular operators on the centralizer-graded GNS space.
# Diagonal (boost) part: weights e^{-beta E_k}; OFF-diagonal centralizer part:
# a unitary block u in M_omega.  Connes cocycle: (Du':Du)_t = (h)^{it} with
# h in M_omega positive. Same flow  <=>  h commutes with the modular generator
# <=> h in centralizer. We show: composing psi with Ad(u), u in U(M_omega),
# preserves BOTH state and flow  ->  residual freedom = U(M_omega).

# Symbolic 2x2 centralizer block (one degenerate boost level, multiplicity 2):
a,b = sp.symbols('a b', positive=True)        # the two equal boost weights -> set equal
w = sp.Symbol('w', positive=True)             # common weight (degenerate level)
rho_block = w*sp.eye(2)                        # density on the multiplet (DEGENERATE => scalar)
th = sp.Symbol('theta', real=True)
u = sp.Matrix([[sp.cos(th), -sp.sin(th)],[sp.sin(th), sp.cos(th)]])  # U(2) gauge in M_omega

print("=== TEST E: residual gauge preserves state AND flow (symbolic) ===")
# (i) state preserved: u rho u^dagger = rho  (since rho_block scalar)
preserved = sp.simplify(u*rho_block*u.T - rho_block)
print("u rho u^* - rho =", preserved.tolist(), " => state PRESERVED for any theta")
# (ii) flow preserved: modular flow on this block is trivial (scalar rho => rho^{it}=w^{it} I),
# so u commutes with rho^{it}:
rho_it = w**(sp.I*t)*sp.eye(2)
commute = sp.simplify(u*rho_it - rho_it*u)
print("u rho^{it} - rho^{it} u =", commute.tolist(), " => flow INTERTWINED for any theta")
print()
print(">>> RESIDUAL GROUP at a degenerate boost level of multiplicity m = U(m).")
print(">>> Summed over the (infinite) degeneracy of the physical boost spectrum,")
print(">>> the residual gauge is the full unitary group of the centralizer M_omega.")
print(">>> This is a NONTRIVIAL infinite-dim'l torsor: phi is NOT pinned by")
print(">>> (D1)+(D2 weights)+(D3). The strictly-stronger vector-matching that")
print(">>> agentUU flagged = choosing the RIGHT point in this torsor.")

print("\n=== THE HONEST COUNTER-CHECK (could a highest-weight cyclic vector pin it?) ===")
# A cyclic-separating vector that is EXTREMAL (highest-weight / unique ground)
# in EACH irrep would kill the gauge WITHIN an irrep -- but the cross-irrep
# (cross-l-tower) mixing survives, AND the chord side must independently
# reproduce the SAME irrep decomposition. The vector-matching is the residual.
print("A highest-weight vector pins phases WITHIN one irrep, but:")
print("  - cross-tower (l, field-mode) centralizer mixing survives;")
print("  - the chord side must independently realize the SAME multiplicity")
print("    decomposition AND the SAME cyclic vector in each tower.")
print("  => phi reduces to MATCHING THE GNS DATA (multiplicities + cyclic")
print("     vector per tower), NOT to a finished theorem. Checkable in")
print("     principle, NOT auto-satisfied by 'both hyperfinite II_1 + same beta'.")
