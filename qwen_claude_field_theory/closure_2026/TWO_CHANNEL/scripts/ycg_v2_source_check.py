#!/usr/bin/env python3
r"""YCG-v2 decisive check: WHICH variation gives the MOND divergence, and what sources it?
Action piece: N sqrt(h) J(Y),  Y = c^4 D_i q D^i q,  h_ij = e^{4q} hbar_ij,  Psi = 2c^2 q.
"""
import sympy as sp
print("="*78)
print("(1) Which variation produces D_i[mu D^i Psi] ?")
print("="*78)
print("""  delta/delta N  [N sqrt h J(Y)] = sqrt h J(Y)
        -> a POTENTIAL term in H_perp. No divergence structure. NOT the MOND operator.
  delta/delta q  [N sqrt h J(Y)] = -2 D_i[ N sqrt h J_Y c^4 D^i q ]
        -> HAS the divergence structure. With J_Y = mu and Psi=2c^2 q:
           = -D_i[ mu D^i Psi ] * (normalization)   <== THE MOND OPERATOR LIVES HERE""")
print("  => the MOND equation is the q-EQUATION, not the lapse equation.\n")

print("="*78)
print("(2) What sources the q-equation under MINIMAL coupling?")
print("="*78)
print("""  S_m = S_m[g_munu, psi_m],  h_ij = e^{4q} hbar_ij.
  delta S_m/delta q = (delta S_m/delta h_ij)(delta h_ij/delta q)
                    = (-(1/2) sqrt h T^ij)(4 h_ij) = -2 sqrt h T^i_i
  => the q-equation is sourced by the TRACE OF THE SPATIAL STRESS T^i_i, NOT by rho.""")
print("""
  For the matter that makes galaxies -- pressureless dust (stars, gas, cold baryons):
        T^munu = rho u^mu u^nu   =>   T^ij = rho v^i v^j ~ rho v^2  =>  T^i_i ~ rho v^2/c^2 -> 0
  Numerically for a galaxy: v/c ~ 7e-4, so T^i_i/rho c^2 ~ v^2/c^2 ~ 5e-7.""")
v,c = 220e3, 2.998e8
print(f"  Milky Way: (v/c)^2 = {(v/c)**2:.2e}  <== the MOND source is suppressed by THIS factor")
print("""
  => D_i[mu(|DPsi|/a0) D^i Psi] = 4 pi G * (T^i_i) ~ 4 pi G rho (v/c)^2,  NOT 4 pi G rho.
  The MOND equation is sourced ~5e-7 too weakly. Rotation curves stay Newtonian.""")

print("\n"+"="*78)
print("VERDICT — YCG-v2")
print("="*78)
print(r"""
The Cotton-squared V_TT ~ C Delta^-2 C IS a genuine contribution: it supplies an independent
k^2 tensor gradient, escaping the CGD c_T=0 no-go. Credit where due. But it repairs a sector
YCG never broke (YCG keeps Einstein's TT term anyway), and it does not touch the actual killer.

THE KILLER (structural, minimal coupling):
  The MOND divergence operator D_i[mu D^i Psi] arises from the q-VARIATION.
  Under minimal coupling the q-variation is sourced by the spatial stress trace T^i_i,
  because q is the conformal factor of the SPATIAL metric: delta h_ij/delta q = 4 h_ij.
  Pressureless baryons have T^i_i ~ rho v^2/c^2 ~ 5e-7 rho.
  => The MOND equation has essentially NO SOURCE for the matter that makes galaxies.

This is HORN 2 of the two-channel trilemma (MOND inert), reached by a different route --
and it is the SAME obstruction, in its cleanest form yet:

  rho_b (energy density)   lives in the LAPSE variation  (delta S_m/delta N)
  T^i_i (stress trace)     lives in the CONFORMAL variation (delta S_m/delta q)

  Putting MOND on q gives it the wrong source. Putting MOND on N gives MMG (gamma_PPN=0).
  THAT is the duality, now proven twice by independent arguments.

The honest open door remains what it was: the q-equation would work if matter coupled
non-minimally (forbidden), or if T^i_i were not suppressed (relativistic matter only --
which is not what galaxies are made of).
""")
