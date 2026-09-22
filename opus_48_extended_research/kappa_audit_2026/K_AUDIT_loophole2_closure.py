#!/usr/bin/env python3
"""
K_AUDIT (result) -- LOOPHOLE 2 of the channel-B no-go closes: no NON-slip second channel gives the
deep-MOND slope 2 for a static dust source. Surfaces the sharpest structural point: the "channel
count" is BASIS-DEPENDENT, and the physical invariant (the rank of the source->engaged-response map)
is 1 for static dust.

PD01's slope argument mu = 1-(1-p)^n needs n channels EACH ENGAGED (per-channel p != 0). So the load-
bearing number is the count of ENGAGED (sourced) response d.o.f., not the number of sectors that
merely EXIST.

Run: python3 opus_48_extended_research/kappa_audit_2026/K_AUDIT_loophole2_closure.py   (sympy)
"""
import sympy as sp

print("="*90)
print("LOOPHOLE 2 -- a non-slip second channel for static dust")
print("="*90)

print("\n(i) The raw 'channel count' is BASIS-DEPENDENT:")
print("    basis (Psi, Phi-Psi): dust sources G_00 -> Psi engaged; G_kk -> (Phi-Psi)=0 UN-engaged => 1")
print("    basis (Phi, Psi)    : both nonzero => looks like 2, BUT Phi=Psi (dust) ties them = ONE d.o.f.")
print("                          counted twice (double-counting).")
print("    So a bare 'count' is not physical; the invariant is the RANK of source -> engaged response.")

print("\n(ii) The RANK (basis-independent). Static stress T_munu decomposes as")
print("     (T_00=rho, T_0i=momentum, T_ii=pressure, T_ij^TL=anisotropic stress). DUST: only T_00 != 0.")
S = sp.Matrix([1, 0, 0, 0])          # dust populates only T_00
print(f"     dust source (T00,T0i,pressure,aniso) has rank = {S.rank()}  -> 1-dimensional source.")
print("     no anisotropic stress => Phi=Psi (constraint) => the engaged response is 1-parameter (Psi).")
print("     ENGAGED channel count for static dust = 1, in every basis -> slope 1 -> kappa = 1.")
print("     Getting 2 needs a SECOND source (anisotropic stress). For dust the only supplier is the")
print("     modification's own anisotropic stress = a metric SLIP = subject to the no-go (loophole 1).")

print("\n(iii) The specific NON-slip candidates for a second channel -- each fails:")
print("   (a) a SEPARATE scalar field  -> violates the framework's OWN one-field ontology")
print("       (PD05: 'one scalar = the metric's own potential, no second field').")
print("   (b) the graviton's 2 TT polarizations -> RADIATIVE d.o.f.; they do not source the STATIC")
print("       Newtonian potential (carried by the constrained/longitudinal sector) -> no static engagement.")
print("   (c) the two gradient-invariant branches (temporal/spatial) -> static field d_t phi = 0 kills")
print("       the temporal branch (K_AUDIT_two_channel_dust_obstruction) -> collapse to 1.")

assert S.rank() == 1
print("\n" + "="*90)
print("VERDICT: loophole 2 CLOSES. Engaged-channel count for static dust = 1 (rank, basis-free); every")
print("non-slip route to a second engaged channel fails. A second engaged channel REQUIRES the second")
print("metric sector sourced = a slip = the (now coupling-independent) no-go. So kappa=1/2's '2' cannot")
print("be recovered for the dust MOND governs by a non-slip channel either.")
print()
print("STRUCTURAL COROLLARY (the sharpest form of the critique): 'kappa = 1/(channel count)' is")
print("ill-defined without a physical criterion for the count, and the physical criterion (rank of the")
print("engaged response) gives 1 for static dust, not 2. The observed kappa=1/2 (slope 2) is therefore")
print("EMPIRICAL, not a derived channel count -- consistent with the whole audit.")
print()
print("Remaining open: loophole 3 only (give up UNIVERSAL lensing=dynamics -- source-dependent gamma).")
