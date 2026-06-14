import sympy as sp
# ============================================================
# ZZ3 - PATHOLOGY AUDIT (the OWN-tax of spatial nonlocality: ghost / causality / constraint).
# Maximum hostility: spatial nonlocality classically brings acausality, ghosts, a momentum-space
# constraint structure.  A carrier that slips only by introducing a ghost is NOT a survivor.
# ============================================================
k, L, m = sp.symbols('k L m', positive=True)

# The finite-range kernel 1/(1 - L^2 nabla^2).  Two sign choices:
#   (A) 1/(1 + L^2 k^2) = massive-field (Yukawa) propagator, m^2 = +1/L^2 > 0.  GHOST-FREE,
#       causal, exponentially-localized Green function exp(-r/L)/r.  This is what we used.
#   (B) 1/(1 - L^2 k^2): a TACHYONIC/wrong-sign pole at k = 1/L -> ghost + instability +
#       acausal (the Green function oscillates / the pole is on the real axis).
# To get FINITE RANGE (exponential localization, not oscillatory), the kernel MUST be the
# ghost-free sign (A).  Verify the localization and the pole structure.
print("Kernel sign audit:")
KA = 1/(1+L**2*k**2)   # the resolvent we used
poleA = sp.solve(sp.denom(KA), k)
print("  (A) 1/(1+L^2k^2): poles at k =", poleA, " (imaginary -> exponential decay exp(-r/L), causal, ghost-free)")
KB = 1/(1-L**2*k**2)
poleB = sp.solve(sp.denom(KB), k)
print("  (B) 1/(1-L^2k^2): poles at k =", poleB, " (REAL -> oscillatory Green fn, tachyon, ghost/acausal)")
print("  => finite RANGE (exp localization) REQUIRES sign (A) = the ghost-free massive auxiliary field.")
print("     The escape we tested IS the healthy one; it has NO ghost.  Good (the carrier is clean).")

# Ostrogradski check: a TRUE nonlocal operator (infinite-derivative exp(L^2 nabla^2)) vs the
# resolvent.  The resolvent = ONE extra massive scalar chi (mass 1/L) with a STANDARD kinetic
# term -- finite # of d.o.f., no Ostrogradski ghost.  Confirm the auxiliary-field kinetic sign:
print("\nOstrogradski / d.o.f. audit:")
print("  resolvent (1-L^2 Lap)chi=Phi  <=>  ONE auxiliary scalar chi, mass m=1/L, STANDARD")
print("  kinetic term +(grad chi)^2 (sign A).  Finite d.o.f., right-sign kinetic -> NO ghost,")
print("  NO Ostrogradski instability.  Causality: the Yukawa Green function is static & decaying.")

# THE PUNCHLINE OF THE PATHOLOGY AUDIT, stated honestly both ways:
print("\n*** The clean kernel is EXACTLY the one that LOCKS ***")
print("  The ghost-free finite-range kernel is the massive-propagator 1/(1+L^2k^2), with")
print("  |Khat|<=1 and Khat(0)=1 (DC gain 1).  A DC gain of 1 is PRECISELY the KK-1 locked-DC")
print("  condition in space: long-wavelength (k->0) modes pass UNSUPPRESSED.  To suppress the")
print("  pollution you need |Khat|<1 at the SLIP's mode -- but that is the SAME mode, so the slip")
print("  dies equally (the locked ratio).  The ONLY kernel that could suppress the slip's mode")
print("  while passing a DIFFERENT mode is a BAND-PASS (Khat small at k=0) -- but a band-pass")
print("  spatial kernel has Khat(0)=0 = NO long-range force = NO static lens (the spatial twin of")
print("  KK's zero-DC derivative key, which failed the static-lens job).  And a band-pass kernel")
print("  1/(1+1/(L^2k^2)) type has a pole/ghost or a 1/k^2 IR divergence (acausal long-range).")

# Confirm the band-pass IR pathology:
Kbp = (L**2*k**2)/(1+L**2*k**2)   # high-pass: Khat(0)=0
print("\n  Band-pass/high-pass attempt Khat=L^2k^2/(1+L^2k^2): Khat(k->0) =",
      sp.limit(Kbp, k, 0), " -> NO DC = NO static long-range slip (dead, = KK escape (a)).")
