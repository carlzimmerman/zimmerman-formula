#!/usr/bin/env python3
"""
K_AUDIT (result) -- the TWO-CHANNEL count does NOT survive for a dust source under the framework's
own lensing=dynamics constraint. This is an OBSTRUCTION to the structural derivation of kappa=1/2,
found by internal consistency -- reported straight, both ways.

Background: kappa = 1/(2 cp) and the "2" is the source's static channel count (PD01). The count has
two candidate readings (PD01 D2, "the fork is open"):
  reading 1 = the metric's two static potentials  (G_00 -> Psi, G_kk -> Phi-Psi)
  reading 2 = the two branches of the gradient invariant (temporal / spatial)

Test both for the sources MOND actually governs: STATIC, PRESSURELESS (dust) galaxies.

Run: python3 opus_48_extended_research/kappa_audit_2026/K_AUDIT_two_channel_dust_obstruction.py (sympy)
"""
import sympy as sp

print("="*90)
print("Does the TWO-CHANNEL count hold for a static, pressureless (dust) source?")
print("="*90)

# ---- reading 1: the two metric potentials ----
x, y, z = sp.symbols('x y z', real=True)
r = sp.sqrt(x**2+y**2+z**2)
Phi = sp.Function('Phi'); Psi = sp.Function('Psi')
F = Phi(r); G = Psi(r)
lap = lambda f: sp.diff(f, x, 2)+sp.diff(f, y, 2)+sp.diff(f, z, 2)
G00 = 2*lap(G)               # channel A: sourced by rho
chanB_operand = F - G        # channel B operates on (Phi - Psi); G_kk = 2 lap(Phi-Psi)
print("\nREADING 1 -- the metric's two static Poisson sectors:")
print("   channel A (00): G_00 = 2 lap(Psi)         sourced by rho")
print("   channel B (kk): G_kk = 2 lap(Phi - Psi)   sourced by pressure / anisotropic stress")
print("   DUST: pressure = anisotropic stress = 0  -> channel B has no MATTER source.")
print("   FRAMEWORK'S OWN L279 (lensing=dynamics, gamma_PPN=1):  Phi = Psi.")
operandB_under_slip_free = chanB_operand.subs(Phi, Psi)   # Phi := Psi
print(f"   under Phi=Psi:  channel-B operand (Phi-Psi) = {sp.simplify(operandB_under_slip_free)}")
print("   => G_kk = 2 lap(0) = 0 identically. Channel B is UN-SOURCED. Independent channels = 1.")
print("   => reading-1 count for dust = 1  ->  slope 1  ->  kappa = 1/(1*cp) = 1,  NOT 1/2.")

# ---- reading 2: the two branches of the gradient invariant ----
t = sp.symbols('t', real=True)
phi = sp.Function('phi')
# covariant kinetic invariant X = -(d_t phi)^2 + (grad phi)^2 ; static -> d_t phi = 0
dphidt = sp.diff(phi(t), t)
print("\nREADING 2 -- the two branches (temporal/spatial) of the gradient invariant:")
print("   X = -(d_t phi)^2 + (grad phi)^2.  STATIC galaxy: d_t phi = 0.")
print("   => the temporal branch vanishes; only the spatial branch survives -> one branch.")
print("   => reading-2 count for a static source = 1 as well.")

print("\n" + "="*90)
print("OBSTRUCTION (both ways):")
print(" - EMPIRICALLY the count is 2 for dust: SPARC deep-MOND slope = 2 (kappa=1/2) on rotation-")
print("   supported (pressureless) galaxies. So the effective count IS 2 -- MEASURED.")
print(" - STRUCTURALLY neither candidate reading DELIVERS 2 for a static dust source: reading-1's")
print("   second channel is exactly zero under the framework's own Phi=Psi (L279); reading-2's")
print("   temporal branch is zero for a static field. Both predict count 1 -> kappa=1, contradicting")
print("   the measured kappa=1/2. So the 'kappa = channel count' derivation, as stated, gives the")
print("   WRONG count for exactly the sources MOND governs.")
print(" - THE ESCAPE (open, needs the full covariant action, NOT excluded here): the second channel")
print("   could be sourced by the framework's SCALAR anisotropic stress (T^phi_ij, not matter")
print("   pressure) -- but a scalar sourcing Phi-Psi generically produces gravitational SLIP")
print("   (Phi != Psi), colliding with L279's lensing=dynamics. Closing the two-channel count for")
print("   dust means exhibiting a mechanism that sources channel B WITHOUT breaking Phi=Psi. Until")
print("   that exists, the '2' for dust is EMPIRICALLY ANCHORED (SPARC slope), not derived.")
print("\nNET: kappa=1/2's '2' is measured, not structurally derived for the dust MOND governs; the")
print("naive channel readings fail under the framework's own constraints. Honest obstruction, recorded.")
assert sp.simplify(operandB_under_slip_free) == 0, "Phi=Psi should zero the channel-B operand"
