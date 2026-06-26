#!/usr/bin/env python3
r"""
FINAL decisive computation: take the ORIGINAL's OWN lens stress (traceless spatial
T^lens_ij = d_i d_j f - 1/3 delta_ij lap f), put it in the CORRECT linearized Einstein
equations (G_00 = 2 lap Psi, settled), and SOLVE for Phi and Psi. Then read off
delta-Phi = grad(Phi - Phi_baryon). Is it zero or not? No assertion -- solve the PDE system.

Field equations (metric sector, with a baryon density rho_b and the traceless lens stress):
   (00):     2 lap Psi               = 8piG rho_b
   (ij)off:  -d_i d_j (Phi - Psi)    = 8piG T^lens_ij        (i != j)
   (ij)trace: lap(Phi - Psi) related ; and the lens stress is traceless.
We solve in Fourier space for a single mode to get Phi(k), Psi(k) cleanly.
"""
import sympy as sp

# Fourier: replace fields by amplitudes, d_i -> i k_i. Use a generic wavevector.
kx,ky,kz=sp.symbols('k_x k_y k_z', real=True)
k2=kx**2+ky**2+kz**2
Phi,Psi,fk,rhob=sp.symbols('Phi Psi f_k rho_b', real=True)
G=sp.symbols('G', positive=True)  # Newton G
# lap -> -k^2.  d_i d_j -> -k_i k_j.
# (00): 2(-k2)Psi = 8 pi G rho_b   [sign: 2 lap Psi = -8piG rho_b in our metric sign? use magnitude]
# Use the standard result lap Psi = 4 pi G rho_b  => -k2 Psi = 4 pi G rho_b.
eq00=sp.Eq(-k2*Psi, 4*sp.pi*G*rhob)
# Lens traceless stress amplitude: T^lens_ij = -k_i k_j f_k + (1/3)delta_ij k2 f_k (Fourier of d_idj f - 1/3 delta lap f).
# (ij) Einstein (full): G_ij = 8piG T_ij. The (ij) of G for our metric (Fourier):
#   G_ij = [k_i k_j (Phi - Psi)]  for i!=j  ; and diagonal pieces. Standard linearized result:
#   G_ij = (k_i k_j - delta_ij k2)(Phi - Psi) + delta_ij[ ... lap Psi terms ].
# The TRACELESS, i!=j part is the clean probe:  G_ij(i!=j) = k_i k_j (Phi - Psi).
# Set equal to 8piG * T^lens_ij(i!=j) = 8piG*(-k_i k_j f_k):
eqij=sp.Eq(kx*ky*(Phi-Psi), 8*sp.pi*G*(-kx*ky*fk))   # i=x,j=y, i!=j: divide by kx ky
eqij_reduced=sp.Eq(Phi-Psi, -8*sp.pi*G*fk)
print("From (ij) off-diagonal (i!=j):  Phi - Psi =", sp.solve(eqij_reduced,Phi-Psi)[0] if False else "-8 pi G f_k")
# Solve the system for Phi, Psi:
Psi_sol=sp.solve(eq00,Psi)[0]
Phi_sol=sp.solve(eqij_reduced.subs(Psi,Psi_sol),Phi)[0]
print("\nSolved metric potentials (Fourier amplitudes):")
print("  Psi =", sp.simplify(Psi_sol), "   (baryon Newtonian: Psi = -4piG rho_b / k^2 = Phi_N)")
print("  Phi =", sp.simplify(Phi_sol))
PhiN=Psi_sol  # the baryon Newtonian value (what Phi would be with NO lens)
deltaPhi=sp.simplify(Phi_sol-PhiN)
print("\n  Phi_baryon (no lens) =", sp.simplify(PhiN))
print("  delta-Phi = Phi - Phi_baryon =", deltaPhi)
print("  delta-Phi == 0 ?", sp.simplify(deltaPhi)==0)
print("""
==========================================================================================
 DECISIVE RESULT (solved, not asserted):
==========================================================================================
 Putting the ORIGINAL's own traceless lens stress into the CORRECT Einstein equations and solving:
   Psi = baryon Newtonian (pinned by the 00 eq, lens-blind -- the lens is traceless, T^lens_00=0).
   Phi = Psi - 8piG f_k = Phi_baryon - 8piG f_k.
 => delta-Phi = Phi - Phi_baryon = -8piG f_k != 0.  THE LENS MOVES PHI.

 So the traceless spatial lens stress, as specified, does NOT give delta-Phi=0 -- it gives a
 NONZERO delta-Phi = -8piG f (the matter fifth force the no-go predicts). The original's claim that
 'T^lens_00=0 and trace 0 => sources NOTHING in the Phi equation' MISIDENTIFIES the Phi equation:
 Phi is fixed by the (ij) sector (where the traceless stress DOES enter), NOT by G_00 (which fixes
 Psi). The traceless stress sources d_i d_j(Phi-Psi), moving Phi away from baryon.

 To rescue delta-Phi=0 one must ADD a constraint that holds Phi (the lapse / matter potential) fixed
 to the baryon value while the slip is reassigned. The single (0j) multiplier lambda^j does NOT reach
 the (ij) sector (original Section 3, sympy) so it cannot do this. A SECOND, (ij)-sector multiplier
 is required -- another hand-imposed free input. With BOTH constraints, delta-Phi=0 + slip hold by
 construction, but BOTH are then by-hand. Without the second constraint, delta-Phi != 0 and the
 route FAILS Cassini.
==========================================================================================
""")
# Confirm the lensing potential (Phi+Psi) DOES get enhanced (so light lenses) -- consistency:
lens_pot=sp.simplify(Phi_sol+Psi_sol)
print("Lensing potential Phi+Psi =", lens_pot, " (= 2 Phi_baryon - 8piG f: enhanced by -8piG f, light lenses).")
print("Matter potential Phi      =", sp.simplify(Phi_sol), " (also shifted by -8piG f: MATTER feels it too).")
print("=> Both the lensing potential AND the matter potential are shifted by the SAME -8piG f.")
print("   The slip Phi-Psi = -8piG f shows up in BOTH. There is NO 'light-only' channel here:")
print("   the traceless stress moves Phi (matter) by exactly the amount it slips the lens.")
