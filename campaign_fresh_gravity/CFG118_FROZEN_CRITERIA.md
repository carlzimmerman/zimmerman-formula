# CFG118 — Door 6: spherical secondary infall of a cold fluid onto a baryon core (shell crossing). FROZEN CRITERIA

Written 2026-09-29, before any script or number of this lane. The menu of ten doors (closure_map/TEN_DOORS_GATES_2026-09-29.md, 5ef77ea09) was written knowing the target. The shared gates G1–G5 there are binding; this file adds lines but weakens none. A scoped no-go is a valid result.

## The question

Cold matter falls onto a baryon core in a ΛCDM background, and its shells cross. Does the violent relaxation that follows produce a cold density with CFG44's target C(r) ≡ ρ_c r³ g_tot = (a₀/4π) M_b(<r)?
- The pass line (G1) is within 10% over x = r/r_M in [0.1, 30], with r_M = √(GM_b/a₀) and a₀ at κ = ½ (canonical 9.36e-11 and alt 1.13e-10).
- It is checked for M_b = 10⁹, 10¹⁰, 10¹¹ and 10¹² M☉ with the same constants and initial-condition rules at every mass.

## The simulation (declared)

- **A 1-D spherical Lagrangian shell code** with N_s = 20,000 cold shells (5,000 in a resolution check). Newtonian gravity in physical coordinates:
  - each shell feels −G[M_b(<r) + M_c(<r)]/r² + (Λc²/3) r + j²/r³;
  - Planck18 background: H₀ = 67.4, Ω_m = 0.315, Ω_Λ = 0.685, Ω_b/Ω_m = 0.157;
  - shell crossing is allowed: enclosed masses are recomputed by sorting at every step;
  - a symplectic leapfrog runs with an adaptive step (a declared fraction of the local dynamical time).
- **Initial conditions (Bertschinger's secondary-infall set-up):**
  - at z_i = 100 the cold shells are uniformly spaced in enclosed mass at the cosmic cold density Ω_c ρ_crit(z_i);
  - they move with the Hubble flow, with no primordial perturbation other than the central baryon core, whose mass excess seeds the infall;
  - the shells extend to three times the z = 0 turnaround radius of the enclosed mass.
- **The baryon core** is present from z_i and static in physical coordinates, in two geometries: a point mass (softened at 10⁻³ r_M) and CFG44's exponential sphere with h = 2, 3, 4, 5 kpc. The baryons' assembly history is an untested hypothesis.
- **Angular momentum.** Purely radial orbits are singular at the centre, so each shell gets a specific angular momentum j. It is fixed at turnaround so that r_peri/r_ta equals a declared bracket value: 0.05, 0.1 or 0.2, the same at every mass. This is a bracket on an initial condition, not a fitted constant. The best bracket is not chosen after the fact; all three are reported.
- **The density at z = 0** is shells binned in log r and time-averaged over the last dynamical time at each radius.

## Checks

- **C1 CONTROL:** with no baryon core, the shells follow the background Hubble flow to 1e-6 relative at z = 0.
- **C2 CONTROL (physics):** Einstein–de Sitter background, Λ = 0, j at the smallest bracket and a point seed. The late-time inner cold profile approaches Bertschinger's self-similar ρ ∝ r^(−9/4) within ± 0.15 in log-slope over the self-similar range.
- **C3 CONTROL:** the 5,000-shell run reproduces the 20,000-shell ratio curves to 10% over x in [0.3, 30].
- **H1 [HEADLINE; MUTATE must change it]:** G1 holds: C_infall/C_target lies in [0.9, 1.1] over x in [0.1, 30] for every mass and both geometries, for at least one j bracket used at every mass.

## Reported rows

- **R1:** the ratio curves; the largest deviation per mass and geometry; the x range within 10%.
- **R2:** the mass scaling of the infall profile's radial scale (for example the radius where the log-slope is −2), against the target's r_M ∝ M_b^(1/2). The turnaround scale ∝ M^(1/3) is the declared expectation.
- **R3, G2–G5 as statements:**
  - G2: the cold fluid is CDM, so linear growth is ΛCDM's by construction.
  - G3: the interaction is ordinary Newtonian gravity, so reciprocity and energy hold.
  - G4: count any constant the result needs.
  - G5: CDM is well posed.
  - The door lives or dies on G1.

## MUTATE

MUTATE=1 evaluates G1 on the target's own ρ_c in place of the simulated density. H1 must then pass, so the MUTATE changes the headline. This checks that the evaluator can pass. The physics is validated by C1 and C2.

## Readings (declared)

- **H1 PASS:** collapse around a baryon core lands on the target at every mass. Such a result would need an independent re-derivation before anything else.
- **H1 FAIL:** a scoped no-go on G1: violent relaxation of CDM around baryons does not produce the target's a₀ scaling. R2 says whether the cause is the radial scale's mass scaling.
- **Untested (declared):**
  - non-spherical collapse, mergers and tidal torques;
  - baryonic feedback and a growing baryon core;
  - warm or self-interacting dark matter;
  - any angular-momentum distribution other than the three brackets.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
