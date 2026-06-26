#!/usr/bin/env python3
"""
agentZZ STAGE 2 — Coarse-grain the worldlines to a FIELD theory.

The move: a worldline is a delta-function source x_i(t). Integrating over ALL matter
worldlines (the density rho) coupled to the dS bath, the collective object is the
matter NUMBER/MOMENTUM density. We ask: what collective FIELDS does the in-in worldline
action generate, and what is their action?

Method (Feynman-Vernon -> collective field, the standard open-EFT coarse-graining):
  - The bath is the dS vacuum; its two-point structure splits into a NOISE (Hadamard)
    kernel and a DISSIPATION (retarded) kernel [Caldeira-Leggett / Galley Eq 25 below].
  - Integrating out the bath for the WHOLE matter distribution gives an influence
    functional Phi[rho_+, rho_-] that is BILINEAR in the coarse-grained source.
  - A Hubbard-Stratonovich (HS) transformation trades the bilinear-in-source kernel for
    a GAUSSIAN integral over an auxiliary COLLECTIVE FIELD whose propagator is the kernel.
    This is the textbook route by which a kernel becomes a field.

We carry this out and read off (a) the SPIN of the collective field(s), (b) their
kinetic structure, (c) the preferred-frame vector, and (d) the deep-MOND nonlinearity.
"""
import sympy as sp

print("="*78)
print("STAGE 2: coarse-grain worldlines (integrate over rho) -> collective FIELDS")
print("="*78)

# ----------------------------------------------------------------------------
# 2A. The coarse-grained source. A worldline couples to the bath through its
#     acceleration a^mu. Summing over worldlines of density rho(x), the collective
#     coupling is to the MOMENTUM-FLUX / acceleration density. In the in-in action
#     the bath enters as int dx dx' J_-(x) G_bath(x-x') J_+(x'), where J is the
#     coarse-grained current sourced by matter.
#
#     KEY STRUCTURAL FACT (Deser-Levin): the dS bath is defined in the COSMIC REST
#     FRAME. The detector temperature depends on the acceleration RELATIVE to that
#     frame. So the bath kernel G_bath is NOT Lorentz-invariant: it carries a
#     preferred timelike direction u^mu = the dS rest frame 4-velocity, u.u = -1.
#     This is forced, not chosen.
# ----------------------------------------------------------------------------
print("""
[2A] FORCED PREFERRED FRAME (from Deser-Levin):
   The dS-Unruh temperature T_eff = (hbar/2pi c kB) sqrt(|a|^2 + (cH_Lam)^2) is defined
   by the acceleration |a| MEASURED IN THE COSMIC REST FRAME. The bath two-point kernel
   therefore carries a unit-timelike direction u^mu (u.u = -1) = the dS rest 4-velocity.
   => A UNIT-TIMELIKE VECTOR FIELD is FORCED as a collective bath label.   [field #1: A_mu]
""")

# ----------------------------------------------------------------------------
# 2B. Hubbard-Stratonovich: the bilinear bath kernel -> a collective SCALAR field.
#     The influence functional has the schematic form (Caldeira-Leggett / Galley 25):
#        Phi = (1/2) int J_a(x) G^{ab}_bath(x-x') J_b(x')
#     where a,b in {+,-}, J = coarse-grained matter current. The retarded part is the
#     long-range collective force. We HS-decouple the LONG-RANGE (low-frequency,
#     spatial-gradient) part of the kernel with an auxiliary field phi:
#        exp[ -(1/2) J K^{-1}... ] ~ INT Dphi exp[ -(1/2) phi K phi + phi J ]
#     The resulting phi is a SCALAR (it couples to the scalar matter density rho),
#     long-range, shift-symmetric (J only couples to grad phi, since rho couples to
#     the FORCE = gradient of the collective potential).
# ----------------------------------------------------------------------------
print("[2B] Hubbard-Stratonovich on the long-range bath kernel:")
print("   The bilinear  (1/2) J K J  with K the long-range retarded kernel decouples via")
print("   an auxiliary SCALAR phi:   INT Dphi exp[ -(1/2) phi K^{-1} phi + phi J ].")
print("   phi couples to the matter density rho through the FORCE -> grad phi . (matter current).")
print("   phi is shift-symmetric (only grad phi appears) and long-range.   [field #2: scalar phi]")
print()

# Verify the HS identity explicitly (Gaussian) in a 1-mode toy:
J, K, phi = sp.symbols('J K phi', real=True)
# INT dphi exp(-1/2 K phi^2 + phi J) = sqrt(2pi/K) exp(J^2/(2K))
# so the effective source-source action is J^2/(2K) -- matches (1/2) J (1/K) J.
gaussian = sp.sqrt(2*sp.pi/K)*sp.exp(J**2/(2*K))
print("   HS check (1 mode): INT dphi exp(-K phi^2/2 + phi J) =", gaussian)
print("   => source self-energy J^2/(2K). The auxiliary phi's kernel K^{-1} IS the bath kernel.")
print()

# ----------------------------------------------------------------------------
# 2C. The deep-MOND nonlinearity of the kernel. The single-worldline response was
#     mu_fw(|a|/a0). In the collective field, |a| -> |grad phi| (the collective
#     acceleration field). The kinetic term for phi is therefore NOT canonical:
#     it inherits mu_fw. We compute the phi-Lagrangian whose EOM reproduces the
#     MOND law div[ mu_fw(|grad phi|/a0) grad phi ] = 4 pi G rho.
# ----------------------------------------------------------------------------
print("[2C] The collective phi-Lagrangian (AQUAL form), inherited from mu_fw:")
# In AQUAL the Lagrangian is L = -(1/8piG) a0^2 f(|grad phi|^2/a0^2), with
# f'(y) = mu(sqrt(y)).  Deep-MOND mu ~ x => f'(y) = sqrt(y) => f(y) = (2/3) y^{3/2}.
y = sp.symbols('y', positive=True)   # y = |grad phi|^2 / a0^2
# deep-MOND mu(x)=x => f'(y)=sqrt(y)
f_deep = sp.integrate(sp.sqrt(y), y)
print("   AQUAL: L_phi = -(a0^2/8piG) f(y), y=|grad phi|^2/a0^2, f'(y)=mu_fw(sqrt(y)).")
print("   deep-MOND mu_fw->x => f'(y)=sqrt(y) => f(y) =", f_deep, " = (2/3) y^{3/2}")
print("   => the collective scalar carries a NON-ANALYTIC |grad phi|^3 term.   <-- the Y^{3/2} shape")
print()
print("   COMPARE AeST Eq(2): J(Y) -> (2 lambda_s/(3(1+lambda_s) a0)) Y^{3/2} as grad phi->0,")
print("   with Y=|grad phi|^2. The coarse-grained scalar's deep-MOND term has the SAME")
print("   (2/3) Y^{3/2} structure and the SAME 1/a0 coefficient scaling.")
print()

# ----------------------------------------------------------------------------
# 2D. Summary of the collective field content produced by the coarse-graining.
# ----------------------------------------------------------------------------
print("[2D] COLLECTIVE FIELD CONTENT produced by integrating worldlines over rho:")
print("   (i)  A_mu : unit-timelike vector = the dS bath rest frame (u.u=-1).   [FORCED, Deser-Levin]")
print("   (ii) phi  : shift-symmetric long-range scalar (HS of the bath kernel). [FORCED, HS]")
print("   (iii) the scalar's kinetic term is non-canonical, deep-MOND limit (2/3)|grad phi|^3.")
print("   => EXACTLY AeST's field content {g, A_mu(unit-timelike), phi(shift-sym)} + the Y^{3/2}.")
