# Audit — FM-000004 "Spatially Nonlocal F+ Screened Preferred-Frame with Decoupled Propagator"
**VERDICT: KILL at G8 (P7 strong-coupling collision). CONDITIONAL on the natural reading of its coupling.**

## Claim under audit
"The vector A_μ carries a fixed Maxwell kinetic term, so the finite propagating mode has a kinetic
normalization NOT inherited from the screened preferred-frame response — separating α~e^{−y} screening
from the propagator normalization." (kinetic_normalization_source: "independent")

## Why it fails (audit_decoupled_propagator.py, sympy-exact)
1. **Maxwell is identically blind to the longitudinal mode.** F_{μν}[A=∂φ] ≡ 0 (verified). The −¼F²
   term gives ZERO kinetic term to the u-longitudinal polarization.
2. **The preferred-frame physics lives in that longitudinal mode.** The 2 transverse Maxwell modes are
   frame-blind spectators — they carry no α₁, α₂, and no u-dependent lensing. What produces the
   preferred-frame MOND effect is the u-longitudinal/temporal polarization.
3. **Integrating out A₀** in (−¼F² + ½M²(y)A²) gives the longitudinal kinetic coefficient exactly
   **K_long = M²k²/(2(M²+k²)) → M²/2 in the short-wavelength regime.** With the screened coupling
   acting as the field-dependent mass M²(y)=e^{−y}, **K_long → e^{−y}/2 → 0** as y→∞ (Solar System).
4. **So the mode carrying the physics is normalized by the SCREENED coupling, not by Maxwell.**
   Canonical σ̂=√K_long·σ ~ M σ; every vertex g→g/M ~ g e^{y/2}. Λ_sc ∝ M(y)=e^{−y/2} → 0.

**The "independent finite propagator" is true only for the transverse spectators. The longitudinal
carrier collapses exactly where α₁,α₂ are screened — P7 intact.** Same wall as AeST (α₂), and as the
GW170817-collapsed khronometric endpoint (KM-X1). Adding a Maxwell vector does not dodge P7; it just
relocates the collision to the vector's longitudinal mode.

## Honest scope
CONDITIONAL on the screened chi–A_μ order-φ² preferred-frame term acting as a field-dependent vector
mass on the u-projection — the natural reading of the declared architecture. If the intended coupling
is a *gauge-invariant current* coupling e^{−y}∂_μχ·A^μ instead (no vector mass), then A stays exactly
Maxwell (2 healthy DOF) but then it carries NO preferred-frame effect at all (a conserved-current
coupling produces no α₁,α₂) — so it fails the lensing/DC-001 escape it was built for. Either branch
fails: massive→P7 strong coupling; massless→no preferred-frame lensing. That fork is the real kill.
