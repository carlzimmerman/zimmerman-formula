# condensate_dust_2026 — the dark mass as a state of the framework's own field

This directory tests the record's no-particle reading of the dark sector. In that reading (the ghost-condensate thread), the cold dark mass is not a particle species. It is the framework's own scalar sitting slightly above its condensate minimum, with the excess diluting as cold dust. Linear cosmology cannot tell this from a particle: the CMB constrains a fluid. The nonlinear universe can. Halos, Bullet and Harvey all need cold streams of dark mass to pass through each other.

## L374 — the condensate's dust through shell crossing (one dimension)

`L374_condensate_dust_shell_crossing.py`: 5/7 checks pass, rc = 1.
- **R1 fails:** the pre-declared hypothesis is falsified.
- **C1 fails:** for a physical reason, explained below.

`MUTATE=1` replaces the condensate by a linear complex field with the same dispersion and self-interaction. It passes 6/6, rc = 0, which makes it the inverted control.

**The question.** The candidate fix for the mode reading's caustic problem is the condensate's own k⁴ term. That term gives its ripples a k² dispersion, the same property that lets fuzzy dark matter pass through itself by interference. Does it work?

**The field.** φ = t + π, with P(X) quadratic about its minimum and the ghost condensate's (□φ)² term. In the weak-field, non-relativistic limit in one dimension, with dust density ρ ∝ X − X₀ and v = −∂ₓπ:

- ∂ₜρ + ∂ₓ(ρv) = β ∂ₓ³v  (the shift charge; β is the k⁴ term)
- ∂ₜv + v∂ₓv = −∂ₓΦ − ε∂ₓρ  (ε is the condensate's warmth)

This is a dispersive γ = 2 fluid. Its linear waves obey ω² = ερk² + εβk⁴, so D = √(εβ) plays the role of ħ/2m. Negative ρ means the condensate has fallen below its minimum, where c_s² < 0.

**The test.** A cold converging flow in a periodic box, run free-streaming and self-gravitating, coarse-grained on L/50.
- **Target:** an exact collisionless N-body answer.
- **Positive control:** Schrödinger–Poisson at the same D.
- **Negative control:** the pressureless fluid.
- **Scan:** warmth W = ερ̄/v₀² from 0.1 to 10⁻⁴, and de Broglie length L/100 and L/200.

| warmth W | condensate: first below its minimum | condensate: breaks down | linear complex field (MUTATE) |
|---|---|---|---|
| 0.1 | 1.11–1.16 t_sc | free: survives, but collides like a fluid (21.5% of the mass misplaced); gravity: 1.52–1.53 t_sc | the same fluid (21.5% / 23.9% misplaced) |
| 0.01 | 1.02–1.05 t_sc | 1.16–1.37 t_sc | tracks with gravity; free 6.4–6.6% (misses) |
| 0.001 | 0.94–0.98 t_sc | 1.08–1.19 t_sc | **tracks** (≤ 1.4%) |
| 0.0001 | 0.81–0.91 t_sc | 0.98–1.15 t_sc | **tracks** (≤ 1.0%) |

Schrödinger–Poisson tracks the collisionless answer to ≤ 1.0% at L/100 and ≤ 0.5% at L/200. The pressureless fluid follows the exact single-stream solution (central density 20.000 at 0.95 t_sc) and then diverges.

**What happens.**
- Every cold condensate cell falls below its minimum within ~20% of shell crossing and runs away. The colder the cell, the earlier this happens. Halving the de Broglie length barely moves the times.
- Energy is conserved to ≤ 1.2 × 10⁻⁶ until the runaway. Doubling the grid and halving the time step reproduce the crossing time exactly and the breakdown time to 2 × 10⁻⁵, so the breakdown belongs to the equations, not the numerics.
- The warmest cell survives free streaming only as a fluid: the streams stop and pile up instead of passing through.
- With the same warmth and dispersion, the linear complex field passes. So the failure lies in the form of the condensate's dispersion. A single real field is hydrodynamics; interference needs a linear wave field.

**C1, recorded as failed.** C1 was pre-declared as a single-stream control. It fails only in the coldest cells, and for a physical reason. At fixed dispersion, the k⁴ coefficient β = D²/ε grows as the condensate cools, and it bends the large-scale flow before any crossing. The pre-crossing deviation scales exactly as D²/W:
- it drops ×4.0 when λ halves;
- it rises ×9.9 when W drops tenfold.

At cosmological parameters this pre-crossing effect is negligible, but the breakdown at crossing is not.

**Reading.** The minimal ghost condensate cannot be the collisionless dark mass:
- cold, it breaks down at the first stream crossing;
- warm enough to be held up by pressure, it collides like a fluid.

The one field that passes is a linear wave field. Physically, that is wave (fuzzy) dark matter, whose quanta are light bosons. The record's open item "caustic-quenched dust" is not answered by the condensate's own k⁴ term.

**Limits.**
- One dimension, a static background, and the non-relativistic weak-field limit.
- The minimal action only: quadratic P about the minimum and the (□φ)² term. The ghost condensate's cubic operator and other completions are not tested.
- The scanned warmth is far above the CMB's bound on the dust, but the trend runs the wrong way for the condensate (colder breaks earlier).

## L382 — the fuzzy wave field in the particle-mesh box

`L382_fuzzy_field_in_the_box.py`: 5/5 checks pass, rc = 0. `MUTATE=1` sets the allowed masses to 10⁻²⁴ eV. The box then sees the wave field and R1 flips (rc = 1).

**The question.** L374 found that only a linear wave field (fuzzy dark matter) passes through itself. What does such a field do in the record's particle-mesh box: 100 Mpc/h, 256³ mesh, 580 kpc cells?

**What can differ.** A wave field differs from collisionless dust in only two ways:
- its initial power is suppressed below its Jeans scale (the Hu–Barkana–Gruzinov transfer);
- below its de Broglie length it interferes and forms solitonic cores.

Above that length it moves as collisionless dust, which was L374's positive control. The Lyman-α forest bounds the boson mass: m ≳ 2 × 10⁻²¹ eV (Iršič et al. 2017), and m ≳ 2 × 10⁻²⁰ eV (Rogers & Peiris 2021).

**On the box's own mesh and spectrum:**

| boson mass | initial variance | σ₈ | worst mesh shell | forest-range 1D power | de Broglie length (200 / 700 km/s) | solitonic core (10¹² / 10¹⁴ M☉) |
|---|---|---|---|---|---|---|
| 10⁻²² eV (forest-excluded) | −21% | 1 − 10⁻⁶ | 0.00 (the corner) | ≥ 0.85 | 600 / 170 pc | 160 / 35 pc |
| 2 × 10⁻²¹ eV | −1.3 × 10⁻⁴ | unchanged | 0.991 (the corner) | ≥ 0.9999 | 30 / 9 pc | 8 / 1.7 pc |
| 2 × 10⁻²⁰ eV | unchanged | unchanged | 1.000 | 1.0000 | 3 / 0.9 pc | 0.8 / 0.2 pc |

**Reading.** At every mass the forest allows, the box and its gates cannot tell the wave field from the collisionless carrier:
- the initial conditions differ by at most 10⁻⁴ in variance;
- every wave effect sits at ≲ 30 pc, against 580 kpc cells and Harvey's 100 kpc aperture.

So the record's box runs, L373 included, are the wave field's runs as they stand. The decay modes read as the field's momentum being redistributed, which is the same thing in the classical limit. The box would see the wave field only at ~10⁻²² eV, which the forest already excludes as all of the dark mass.

On the gates the box checks, a forest-allowed wave field is just the collisionless carrier, so the galaxy clearing (mode G) is still needed. Its solitonic cores in galaxies (≲ 8 pc) are far too small to matter to the MOND regime.

**Limits.**
- Linear transfer and sub-mesh scales only; no wave-resolving zoom simulation.
- The solitonic core scaling is Schive et al. 2014's, at z = 0.
