# W1_pmedium_3d_scaleup — ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY, plus PRESCRIBED (a test
input chosen by the parent lane, not data and not derived) and NUMERICAL (discretization or diagnostic convention).
No observational data enter this lane. Every row is inherited from SE-20261023 unless marked "this lane".

## A. The physics being evolved (inherited, unchanged)

| ingredient | class | source | used as |
|---|---|---|---|
| reduced preferred-frame action: cold + baryon particles, polarization P with W(P) = −\|P\| − ln(1 − \|P\|) (force P/(1−\|P\|)), scalar χ, mismatch e = δρ_c − ∇·P/A, h = e/χ, energy e²/(2χ), α(χ−1)²/2, d\|∇χ\|²/2, inertia η, b | FRAMEWORK-NATIVE (sol61 construction; not derived from the covariant v3 action) | SE `DERIVATION.md`; `expanding_polarization_2026_10_23` | the evolved system |
| η = .005, α = .005 (λ = 100), b = d = .125 (phase gap .2, phase speed 1) | FRAMEWORK-NATIVE choices (prescribed in the radiating_collapse lineage, not fitted here) | `radiating_collapse_2026_10_22/CONTRACT.md` L8; SE `model.py` | fixed constants |
| cold particles feel Φ + h, baryons feel Φ only | FRAMEWORK-NATIVE | SE `DERIVATION.md` | force law (the MUTATE removes h) |
| Newtonian periodic Poisson gravity ∇²Φ = A²(δρ_c + δρ_b) | standard GR weak-field (not MOND machinery) | SE `model.py` | gravity |
| no μ-function, no QUMOND/AQUAL operator, no EFE recipe | — (absence noted) | SE `model.py` | the AQUAL law of the BRIEF is not in this reduced action; any MOND-like behaviour must come from the medium. Not tested here. |
| unit system ℓ₀ = .4404221297174536 kpc, a₀, t₀ = √(ℓ₀/a₀), M₀ = a₀ℓ₀²/G | FRAMEWORK-NATIVE with κ = ½ FITTED (canonical a₀ = κc√(Gρ_DE)) | `radiating_collapse_2026_10_22/CONTRACT.md` L8 | the only place a₀ enters ⇒ both footings |
| canonical footing a₀ = 9.3603e-11 m/s² (SE's literal t₀ = .012074272908402984 Gyr, M₀ = 130257985.45037776 M☉) | FRAMEWORK-NATIVE, κ = ½ FITTED | SE `model.py` | canonical ladder |
| alt footing a₀ = 1.1312e-10 m/s², ℓ₀ fixed, t₀ and M₀ rescaled | FRAMEWORK-NATIVE (record alt value) | V1 lane record values; this lane's mapping | alt ladder (this lane) |
| ℓ₀ held fixed on the alt footing (not a₀-scaled) | PRESCRIBED (this lane's mapping choice; ℓ₀'s own origin is not traced here) | this lane | disclosed: another mapping would give another alt ladder |
| canonical core mass 1.0952264e7 M☉ (= .0840813 M₀) | FRAMEWORK-NATIVE, FITTED | `radiating_collapse_2026_10_22/RESULT.md` L9 | labels the box size only (box = 6π² × this mass); never a prediction |
| reference core radius .3214846542759978 kpc | FRAMEWORK-NATIVE (inherited canonical value) | SE `model.py` `groups()` | one aperture, unresolved at every grid here |

## B. Background and initial state (inherited)

| ingredient | class | source | used as |
|---|---|---|---|
| imposed Einstein–de Sitter background A = (t/t_i)^{2/3}, no Λ, no radiation, no evolved Friedmann constraint | ΛCDM-PROCESSED-adjacent simplification (GR matter-only background imposed) | SE `DERIVATION.md` | expansion |
| H₀ = 67.4 km/s/Mpc, Ω_m = .315 (Planck 2018 base-ΛCDM) | ΛCDM-PROCESSED | SE `SOURCES.md` | H_i and ρ̄_m for the EdS normalization; 67.4 lies inside the framework-native 67.2–68.6 (BRIEF), not re-derived here |
| baryon fraction f_b = 1/6.364 | ΛCDM-PROCESSED | SE `model.py` | species masses |
| pressureless baryons | PRESCRIBED simplification | SE `HANDOFF.md` | — |
| z_i = 1100, z_end = 10 | PRESCRIBED | SE `CONTRACT.md` | run span |
| quiet particle lattice + three orthogonal sinusoidal growing-dust displacements, amp .001 / .03, one wavelength per box | PRESCRIBED test seed (not a primordial spectrum) | SE `DERIVATION.md` | the seeds |
| field initial state = instantaneous minimum of the field energy at the given density; tangent velocities by ±ε = 1e-4 differences in ln A | FRAMEWORK-NATIVE prescription (low-excitation preparation, not a derived primordial state) | SE `DERIVATION.md` | initial P, χ, Q, V |
| L-BFGS-B maxiter 1000 → 20000 for n ≥ 32 | NUMERICAL (this lane; solver budget) | FROZEN_CRITERIA §3 | same minimizer, same residual gate |

## C. Discretization and integrator (inherited)

| ingredient | class | source |
|---|---|---|
| periodic box of comoving side L_com = 2πR_L, R_L from the nominal mass; n³ cells, n³ particles per species | NUMERICAL / PRESCRIBED | SE `DERIVATION.md` |
| TSC deposition with its exact derivative as the force (variational pairing); forward gradient, backward divergence | NUMERICAL | `fragment_radiation_2026_10_22/model.py` |
| canonical KDK with exact EdS drift integrals; dt = min(cfl √η / √(1 + 12/(A dx)²), .015/H) | NUMERICAL | SE `model.py` |
| field guards \|P\| < .985, χ > .1 (stop, never clip) | NUMERICAL | SE `model.py` |
| FoF link .2 × mean interparticle separation, ≥ 32 members | NUMERICAL convention (Davis et al. 1985 lineage; a candidate detector only) | SE `model.py` |

## D. This lane's measurement conventions

| ingredient | class | source |
|---|---|---|
| apertures 1.44 and 2.88 kpc (4 cells at 64³ and 32³ at z = 10) and .3215 kpc | NUMERICAL (chosen for resolvability, before any number) | FROZEN_CRITERIA §4 |
| centre: max-cell start, cold-particle mean within 1.44 kpc, iterated | NUMERICAL | FROZEN_CRITERIA §4 |
| isolated energy with Hubble-flow velocities and full-mass pairwise potential (standard halo-unbinding practice), ε = one physical cell, G = 1 code units | NUMERICAL (standard N-body diagnostic) | FROZEN_CRITERIA §6 |
| field energy of the region = SE's non-negative energy densities summed over cells inside R | FRAMEWORK-NATIVE definitions, NUMERICAL attribution (staggered faces to cell index) | FROZEN_CRITERIA §6 |
| 5% convergence threshold | inherited (SE's own spatial-peak criterion) | SE `summarize.py` |
| 25% stability and 25% agreement thresholds; 4-cells resolution rule (SE's own core requirement) | NUMERICAL (this lane, frozen before numbers) / inherited | FROZEN_CRITERIA §5–6 |

## E. What the original verdict rested on, and what this lane changes

SE-20261023's open items were: strong-seed peak not converged (8³–16³), late core radius unresolved, no isolated binding
certificate, runs bounded to ~300 s. This lane changes only resolution (32³–128³), speed/preemptibility and adds the
isolated certificate. It does not touch the open physics items SE lists (imposed EdS, no radiation, pressureless baryons,
initial-history dependence, single-mode seed, finite periodic box).
