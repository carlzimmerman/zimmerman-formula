# FB1_earth_flyby_anomaly — FROZEN CRITERIA (committed alone, before any script or graded number)

Written 2026-10-25 at the owner's request: "lets do the flyby anomaly again ... figure it out based on my framework".
κ = ½ FITTED. Footings canonical (a₀ = 9.3603e-11 m/s²) / alt (1.1312e-10), scored separately, never pooled. Cold dark
energy, not matter. Nothing here says the data favour the framework or GR. Not "theory closed".

Prior record: `ai_slop/research/unsolved_problems/pioneer_flyby_anomalies.py` (2026-06-01) said "MOND cannot explain
(g >> a₀ near Earth)" by inspection, with no kernel and no number. `qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_flyby_2026/`
(1c33c80f9c) is galaxy-scale EFD scattering and explicitly not the Earth flyby anomaly. FB1 is the first computed
readout.

## 0. What is graded

The observed Earth-flyby Δv∞ (Anderson et al. 2008, PRL 100, 091102, Table I; six flybys, transcribed in the script)
against the framework's own prediction for each flyby, from three readings, each reported separately:

- **R-S (primary): the screened theory** (doors push D7d; PAPER58): inside L★ a body's extra field is the hedgehog
  GM/L★² r̂. L★ ∈ {24, 28.9, 90} pc (CFG820 floor, native floor, upper end). The near-Earth extra field is Earth's
  own hedgehog plus the tidal part of the Sun's hedgehog across the flyby region (r ≤ 1e9 m).
- **R-M: the verdict kernel ν_mono = 1/(1 − e^(−√y))**, unscreened, with the total field never below g_sun(1 AU).
  ν − 1 is evaluated in log form (no underflow to a silent zero).
- **R-1 (reported only, Cassini-dead per E2): unscreened AQUAL ν1**, δg ≈ a₀ along the total field.

Prediction rule (fixed now, no fitting):
- A static field centred on Earth is conservative and spherically symmetric, so its Δv∞ is **exactly zero** (energy
  conservation in Earth's frame). This is stated, and then not relied on alone:
- a **bound** |Δv∞| ≤ max|δg| × T is computed with T = 2.0e6 s (±11.6 days, longer than any Table I fit arc), for every
  reading.

## 1. Classes (per footing; the verdict needs both footings to agree, else UNDECIDED)

| class | rule (primary reading R-S, all L★) |
|---|---|
| FB EXPLAINS | the prediction is within 2σ of every Table I Δv∞ |
| FB SILENT (= GR) | the bound is below 1e-3 × MESSENGER's σ (0.01 mm/s) for every flyby: the framework predicts no anomaly, so a real anomaly must come from outside it (or be a modelling systematic) |
| FB CONFLICTS | the bound reaches ≥ 0.01 mm/s and the prediction cannot match Table I within 2σ (the framework would put a signal into flyby tracking that is not seen) |

Reported only: the Anderson formula's own K = 2ωR/c (≈ 3.099e-6) and what a framework term would need to supply it (a
coupling to Earth's spin of order v_rot/c, which no reading here has); the post-2008 nulls (Rosetta II 2007, Rosetta III
2009, Juno 2013), where Anderson's formula predicted non-zero values and no anomaly was seen; R-1's bound.

## 2. Checks

- **K0** the transcription: Anderson's formula Δv = K v∞ (cos δ_in − cos δ_out) reproduces each Table I Δv∞ within
  max(3σ, 0.6 mm/s) for at least 5 of 6 flybys. If not, the table is mis-transcribed and the lane stops.
- **K1** Earth's hedgehog at L★ = 24 pc equals GM_E / L★² to 1e-12 relative.
- **K2** one thread, seconds.
- **MUTATE=1** (separate outputs): the prediction is replaced by Anderson's formula. The grader must then return
  FB EXPLAINS on the K0 flybys. MUTATE exits 1 if it does, 0 if not.

## 3. Disclosed before freezing

Hand estimate: Earth's hedgehog ≈ 4e14 / (7.4e17)² ≈ 7e-22 m/s², so the bound is about 1e-15 m/s, about 13 decades
under NEAR's 13.46 mm/s. Expected class: FB SILENT on both footings. That means the framework does not solve the flyby
anomaly. It also means flybys cannot hurt the framework, which matches the null flybys since 2007.
