# Covariant push (started 2026-10-22): shared brief

## Why this push exists

The doors push (`doors_push_2026_10_22/`, PAPER58, DOI 10.5281/zenodo.23577784) left one surviving candidate,
the **screened theory**: PAPER49's one-field action whose L★ → 0 limit is AQUAL with μ = x/(1+x) (doors E2),
plus a stiffness γ = K L★²/2 with L★ in roughly [20, 90] pc (E4: M/L-dominated), and a collisionless cold-energy
medium. It passes Cassini by 10⁷–10⁹ (D7d) and is the only version that passes Cassini and the galactic law together.

What it lacks is the part that makes a theory complete: **a covariant, well-posed action whose cosmology is
derived, not borrowed.** Every cosmological input so far (ρ_Λ, H₀, Ω_c/Ω_b) has come from Planck's ΛCDM fit
(doors E1). The record's parent no-gos (D9, D9b, E5) cover theories that enforce "phantom = cold medium" as a
Gauss identity. They do not cover the one relativistic MOND-type theory known in the literature to fit the CMB
and matter power spectrum: **AeST** (Skordis & Złośnik, PRL 127, 161302 (2021), arXiv:2007.00082), a
vector + scalar theory whose extra sector behaves as pressureless dust in cosmology. The record touched AeST
only as a one-line "door remnant" (`campaign_fresh_gravity/CFG242_FROZEN_CRITERIA.md`, L12).

## Rules (all lanes; in addition to `doors_push_2026_10_22/BRIEF.md` and `BRIEF_E_AUDIT.md`, which apply)

1. **No new posits to fix a failed test.** A lane may only (a) derive, (b) compute, (c) prove a no-go, or
   (d) state exactly which premise is missing. Adding a free function or constant is allowed only if the lane
   says so in its verdict line and counts it.
2. **Never "derived" for anything that rests on a premise.** Every claim is tagged DERIVED (from stated premises,
   listed), COMPUTED, POSTULATED, FITTED or OPEN.
3. **Literature facts are external inputs.** Cite them (arXiv id, equation number) and verify from a source on disk or
   from the paper text; never from memory alone. If a fact cannot be verified without new downloads, say so and stop
   at that point (no downloads without the owner's OK).
4. **Raw-data rule** (owner, 10-10): verdicts compare raw data with the theory's own prediction; no ΛCDM or
   standard-MOND machinery as a hidden ingredient.
5. **Compute budget:** a CFG960 1024³ job may be running. Every run: `OMP_NUM_THREADS=1 nice -n 10`, < 1 GB RSS,
   minutes. sympy-heavy work is fine within that.
6. Frozen criteria committed alone first; checks + `--mutate`; pathspec commits of your lane only; never push.
   Lane dirs: `covariant_push_2026_10_22/<lane>/`.

## Lanes (wave 1)

| lane | question |
|---|---|
| C1_aest_embedding | Is the screened theory's static sector (AQUAL μ = x/(1+x) + stiffness γ + clock term + cold medium) a limit of an AeST-type action? If yes, which AeST free function F and which parameters; if no, the exact obstruction. |
| C2_aest_cosmology | What does the AeST-type completion predict for the background and linear perturbations (does the extra sector act as cold dust with the right abundance; what sets it), and what tooling and raw data on disk would a native CMB/P(k) confrontation need? |
| C3_scale_map | Do AeST's own scales (its mass/"MOND switch" term) map onto L★, and onto the screened theory's predictions (Cassini, wide binaries, globulars)? Is L★ then derived, fitted, or a new constant? |
