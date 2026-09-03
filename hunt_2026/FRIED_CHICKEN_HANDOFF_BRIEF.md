# FRIED CHICKEN — handoff brief for an independent agent (2026-09-03)

Paste this whole file as the opening prompt. It is self-contained. Everything it cites is committed in
`github.com/carlzimmerman/zimmerman-formula` and runnable.

---

## THE GOAL, in one sentence

Produce a **full relativistic completion of the de Sitter–MOND framework** — a single covariant action that
reproduces the framework's galactic kernel exactly, passes every solar-system, gravitational-wave and cosmological
gate, and predicts the cluster and pressure-supported-system behaviour — **OR** prove rigorously that no such
action exists under stated assumptions. Outcome A is a theory. Outcome B is a no-go theorem. Both are wins.
Anything in between (a candidate that "mostly works") is a loss and must be labelled as such.

## THE FRAMEWORK you are completing (non-negotiable inputs)

- Acceleration scale: **a₀ = ½ c √(G ρ_DE) = c² √(Λ/32π)**. Two numerical footings, use BOTH in every test:
  canonical 9.36e-11 m/s², alternative 1.13e-10 m/s². The ½ is FITTED to SPARC, not derived. Never claim it derived.
- Galactic kernel (Route A): **ν(y) = 1/(1 − e^{−√y})**, y = g_bar/a₀. Equivalently μ(x) = 1 − e^{−x}.
  Field equation used empirically: QUMOND, ∇·g = ∇·[ν(|g_N|/a₀) g_N].
- Where it works: 147–175 SPARC rotating discs at 0.06 dex; Milky Way rotation curve; vertical force; Renzo's rule.
- Where it fails (THE LIABILITY TABLE, `hunt_2026/THE_LIABILITY_TABLE.md`): every pressure-supported system —
  clusters need ×2–3 more at R500 (core g≈20a₀ Newtonian, no kernel can touch it), groups, ellipticals, dwarf
  spheroidals, UDGs, globular clusters. External-field slope measured +0.08±0.05 vs modified-gravity prediction
  −0.09: a SIGN disagreement at 3.7σ.

## THE 13 GATES — all must pass from ONE action (`qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md`)

 1. Reproduces μ(y) = 1 − e^{−y} EXACTLY in the quasi-static weak-field limit (not "MOND-like").
 2. Degrees of freedom: N_grav = 2 tensor (+ at most one healthy clock scalar). HONEST FORM (gate 2′): every DOF
    explicit, counted by a Dirac/Hamiltonian analysis, and healthy (no ghost, no gradient instability, no tachyon).
 3. Φ = Ψ (no gravitational slip) DERIVED, not imposed. Lensing must equal dynamics.
 4. Full PPN derived: γ = β = 1, α₁ = α₂ = α₃ = 0, ξ = 0. Cassini: |γ−1| < 2.3e-5. Pulsar: |α₃| < 4e-20.
 5. ∇_μ T^{μν} = 0 as a Noether identity of the action, not assumed.
 6. Tensor speed c_T = c to 1e-15 (GW170817). NO tunable escape.
 7. Stability at every background: Minkowski, de Sitter, FLRW, galactic. Specifically NO instantaneous channel
    (no ω-independent 1/k² propagator) — this is the wall that kills constraint-based MOND.
 8. Expanding FLRW background with acceleration, obtained dynamically, not by freezing a deceleration parameter.
 9. Controlled y → 0 (deep-MOND) limit: no divergence, no discontinuity in the field equations.
10. Newton's G derived as the high-acceleration limit, not a separate input.
11. ONE metric that both matter and light couple to.
12. The exponential law: the MOND-generating function is G(y) = y² + 2(1+y)e^{−y} − 2, i.e. the correction ADDED
    to the Einstein term is F_M(y) = 2[(1+y)e^{−y} − 1]. Do NOT add the full G(y) — Einstein already supplies y².
13. a₀ = c²√(Λ/32π) may be taken as INPUT. Any claim to DERIVE it must be a theorem with a committed proof.

## WHAT IS ALREADY DEAD — do not rebuild these (every kill is a committed script, rc=0)

**The LOCAL NO-GO THEOREM** (`FRIED_CHICKEN_VERDICT_2026-09-01.md`, assumptions A1–A7, A2 = locality is
load-bearing). Every local carrier of the MOND force beyond the two tensor polarisations dies:
- Algebraic / elliptic metric constraint → instantaneous (gate 7).
- Frame-free F(X) scalar → anisotropic-stress slip (gate 3).
- Clock scalar + R_nn or K → c_T ≠ c (gate 6; λ ≈ −2e-7 in every MOND zone, GW170817 excluded 1e7–1e9×).
- Clock + a_μ (khronometric) → radial gradient instability for a₀ < a < 38a₀, uncurable (gate 7).
- Spatial-curvature couplings → c_T (gate 6).
- Y ≡ 0 clock; DBI clock + rotated MMG; DHOST → each fails a named gate.
- Clock + second scalar → N = 2+2 (gate 2).
- Vector / Einstein-aether (AeST and its c₂,c₄ generalization) → PPN: α₁ = −4c₁₄ − 4(2−K_B)/(J_Y+1). The term
  that MAKES MOND gives an irreducible negative α₁; α₁ = 0 costs a spin-1 ghost. Solar screening loophole dead.
- Second metric / bimetric → N = 7 DOF (gate 2) plus Boulware–Deser ghost.
- **CDE-L4C strict-2-DOF (the furthest any 2-DOF MOND got):** killed at α₃ = O(1), excluded ~1e19×.
  **THE PINCER, mechanism exposed:** N_grav = 2 ⇔ MOND via a second-class constraint ⇔ instantaneous
  propagator ⇔ α₃ = O(1). You cannot have N_grav = 2 AND α₃ = 0 for a MOND theory. α₃ = 0 needs a retarded
  propagating carrier, which is exactly the scalar graviton that N_grav = 2 removes.
- v9 DBI dark sector → dead (pin is DBI-specific per SZ21). CCNL clock → fixable clock but DEAD on lensing for
  any clock inside one metric. Two-sector (dark field on a second metric) → CMB physical-scale theorem + forest.
- Nonlocal spin-2 subclasses: projected kernel keeps the ghost; c_T² = 1/(1−ξ̄) kills 2e9× over GW170817.
- ANY dark component for the cluster residual — hot, cold, or mixed (`hunt_2026/f04–f07`): structure caps the
  hot fraction ≤ 3.75%, the framework's own galaxies require ≥ 30–80%. Structural, so a third component
  does not help.
- Pure modified inertia (rapidity-gap action) → excluded 21σ. (See "the open fork" below — the CLASS is not dead.)

## WHAT IS OPEN — the only places a theory can still live

**(A) MOND + a dark field that IS dark energy.** The universal dark-field theorem says gate 2-as-written ∧ gate 3
is unsatisfiable, so the honest target is gate 2′ with one explicit, counted, healthy dark scalar whose
background IS ρ_DE (this is where a₀ = ½c√(Gρ_DE) comes from physically). AeST is the template and AeST's PPN is
dead, so this needs a NEW action whose MOND-generating coupling does not feed α₁. Cluster lever: potential depth
|Φ| orders clusters ~20× above galaxies; a +μ²Φ Helmholtz term is "real, 28–100% of the core residual,
galaxy- and Cassini-safe" but PHASE-TUNED. Decisive un-run calculation: does the phase pin DYNAMICALLY in a
time-dependent spherical field solve (potential flow, NOT a PM N-body)?

**(B) Field-dependent nonlocal spin-2.** The one residual door of the local theorem. Known obstructions:
localization adds DOF; conservation is not Euler–Lagrange. A candidate must show both are evaded, not assumed.

**(C) THE NEW FORK (2026-09-03, `hunt_2026/F08_G06_*`): modified INERTIA vs modified GRAVITY.** Every system
the framework fits is rotation-supported; every failure is pressure-supported, across 11 decades of mass.
Milgrom proved the two arms coincide for circular orbits and differ for all others. The repo has run ONLY the
modified-gravity arm. Status: 1.73σ hint on 8 dwarf spheroidals (the hard ceiling); globular clusters
(confound-free, no dark matter possible) lean the OTHER way — framework OVER-predicts them by 0.3 dex even with
the EFE on, and the EFE is required to keep it that close. Rotating galaxies can NEVER decide this fork
(proved: what they test is a circular-orbit identity). The cheap wide-binary eccentricity test is SHUT (slope
reverses sign with the eccentricity population). Modified inertia has NO relativistic completion; if you build
one it must be time-nonlocal, and it must explain why globular clusters are Newtonian inside the MW field.

## THE EMPIRICAL GATES a candidate must ALSO clear (data, not theory)

- SPARC RAR 0.06 dex; both a₀ footings.
- Cassini |γ−1| < 2.3e-5; pulsar α₃; LLR/ephemerides for anomalous solar-system acceleration (repo has ~50
  scripts, grep "cassini" — cite, don't redo).
- GW170817 c_T.
- CMB: any dark field must reproduce the acoustic peaks at physical scales (the two-sector kill).
- Lyman-α forest: dark component cold at z~3 (the matching theorem: a galaxy well today IS the background at
  (1+z)³ = δ).
- KiDS-1000 galaxy-galaxy lensing (Brouwer+2021): accreted charge multiplies the 100 kpc–1 Mpc signal by 3–20;
  excluded Δχ² ≥ 100. Covariance MUST be reshaped (m,n,i,j) → transpose(0,2,1,3) or it is not positive-definite.
- Bulk flow β = 0.447 (ΛCDM 0.440): the framework's linear regime measured Newtonian.
- Cluster residual at R500; core g ≈ 20a₀ Newtonian.
- External-field slope: measured +0.08 ± 0.047 (a candidate predicting −0.09 is 3.7σ dead on this alone).
- The decisive future test: deep-MOND BTFR zero-point at z ≈ 2.5 to ±0.13 dex. Framework predicts FLAT (a₀
  constant because Λ is constant); ΛCDM's emergent scale predicts +0.33 dex. Gaia DR4 (Dec 2026) wide-binary band
  frozen at γ_v = 1.1614–1.1814 (canonical) — do NOT touch `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md`.

## WORKING RULES — violating any of these makes the work worthless

1. Test the framework ON ITS OWN TERMS. Verify a "fails" AS HARD AS a "works." Never manufacture a deficit OR a
   win. A negative result is a fine result; say it plainly.
2. EVERY load-bearing claim = a committed, runnable script with numbered checks that CAN FAIL, at least one
   MUTATION CONTROL (shuffle / switch-off / wrong-sign) proving the machinery isn't producing the answer, and
   BOTH a₀ footings. A script exiting nonzero with honest failures beats one that passes by construction.
3. Verify BEFORE announcing. Announce at TRUE strength (1.7σ is "a hint," never "a result").
4. Bug patterns that have bitten this programme repeatedly — check every result against ALL of them:
   total mass used where enclosed mass belongs; spherical formula applied to a disc (the virial coefficient
   is 2/3 for spheres, 0.82 for discs); aperture centred on a local minimum/saddle; covariance reshaped wrong;
   trivial correlation from a joint-fit degeneracy; a "residual" whose SIGN tracks a branch of your own
   prescription rather than the data; a mutation control run once on 15 rows (use ≥ 20000 permutations).
5. NEVER say "theory closed" or "no open doors." Say "every local route closed." NEVER say the data favour
   this framework over ΛCDM. NEVER cite κ = ½ as derived. NEVER cite the de Sitter–Unruh argument for κ (it
   forces a₀ = 2cH_Λ, excluded 15.6σ).
6. If literature values are needed, cite author+year inline. If a number cannot be found, mark the check
   NOT-RUN. Fabricated data is a catastrophe; "blocked, here is the pipeline and the exact input needed" is fine.
7. No personal names or personal framing in any committed file or commit message.

## HOW TO START

Read, in order: `STANDING.md`; `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md`;
`FRIED_CHICKEN_VERDICT_2026-09-01.md`; `hunt_2026/THE_LIABILITY_TABLE.md`; `hunt_2026/F08_F10_THE_COHERENCE_FORK.md`.
Then pick ONE of doors (A), (B), (C). State your assumptions as numbered A1…An before writing an action. Build
the smallest action that could possibly pass gate 1, and run it through gates 7, 6, 4 FIRST (in that order —
that is where everything dies). Only if it survives those three do the rest matter. Report the first decisive
failure by gate number, or the full pass with every gate's script.
