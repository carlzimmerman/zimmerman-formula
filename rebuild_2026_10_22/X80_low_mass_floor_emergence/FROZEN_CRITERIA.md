# X80_low_mass_floor_emergence: FROZEN CRITERIA (committed alone, before any script, run or low-mass number)

**Question.** Does the a₀ floor of route E's core rule, ρ₀r₀ = max(a₀/2πG, η Σ_coll), emerge from native collapse at low
mass? Or must it be put in by hand? The owner said "Yes, queue them" (10-29). This follows X77 (direct native η, fa80ef5107).

**Standing:**
- κ = ½ FITTED. Footings never pooled. Not "theory closed".
- The zooms are Newtonian cold dark energy dust with no a₀ in the dynamics (X48's physics). So emergence here would mean
  that the collapse branch alone lands on a₀/2πG at dwarf masses. That would be a coincidence of scales tested natively,
  not a derivation of the floor or of κ.

**Already known (committed X48/X77 runs; physical ρ₀r₀ = η_S · 18π² ρ̄_m(z_f) · r_vir, median over seeds).** In M☉/pc²:

| Mass | Grid | ρ₀r₀ |
|---|---|---|
| 10¹² | ng 64 | 134.9 |
| 10¹³ | ng 48 | 167.1 |
| 10¹⁴ | ng 48 | 296.0 |

Σ_a0 = a₀/2πG = 106.85 (canonical) and 129.13 (alt).

## Runs (queued; start only after A5 logs "A5 done", so no overlap with A4/A5)

- `x48_zoom.py` unchanged, at M = 10¹⁰ and 10¹¹ M☉.
- Nine seeds (1–9) at ng 64, plus three seeds (1–3) at ng 48 for resolution.
- Same ε fraction, z_i, η_step and background as A3/A4.
- Run directories: `X48_native_cf_zoom/runs/M1e10_s*_ng*`, `M1e11_s*_ng*`.
- Preemptible (SIGTERM → checkpoint, exit 75, --resume).

## Measurement (X77's fit, unchanged)

- Smooth core ρ₀/(1+x²)^{3/2}, fitted over [r_conv, r_vir].
- **Primary:** physical Σ_core = ρ₀r₀ = η_S · 18π² ρ̄_m(z_f) · r_vir. This is the median over the ng 64 seeds, with a
  10 000-draw bootstrap 68 %.
- **Secondary:** η_S × X43's Σ_coll(M). X43's formula is evaluated directly at M, with X53's log-extrapolation reported
  beside it.
- R(M) = Σ_core / Σ_a0, per footing.

## Verdict (headline = canonical; label needs alt to agree, else FOOTING-SPLIT)

- **FLOOR EMERGES:** R(10¹⁰) and R(10¹¹) both lie in [0.71, 1.41] (±0.15 dex), AND |lg R(10¹⁰) − lg R(10¹¹)| ≤ 0.10.
- **FLOOR BY HAND (falls through):** R(10¹⁰) < 0.71.
- **NATIVE OVERSHOOT:** R(10¹⁰) > 1.41. The collapse branch alone would sit above the floor at dwarf masses.
- **PARTIAL:** anything else, e.g. in band but not flat, or in band at one mass only.
- **[NOISE-LIMITED]** is appended if the bootstrap 68 % of R(10¹⁰) spans two classes.
- **[RESOLUTION-DEPENDENT]** is appended if the median shifts by more than 20 % from ng 48 to ng 64 at either mass. The
  class is not changed.

## Also scored (reported, not graded)

Argon's smooth-max formula, frozen here:

c_f(M) = 4.46 [1 + (Σ_a0 / (η₀ Σ_coll))^{8/5}]^{1/2},  η₀ = (4/(3 B_S(1))) 4.46^{5/4} = 12.40.

| Mass | Its c_f | Its R (canonical) |
|---|---|---|
| 10¹⁰ | 14.3 | 1.07 |
| 10¹¹ | 9.6 | 1.16 |

It scores a HIT at a mass if the measured c_f-equivalent lies within ±15 %.

## Checks

- **K1:** the X80 script, run on the committed 10¹² ng 64 snapshots, reproduces X77's η median 20.8276 to 1e-6 and the
  134.9 above.
- **MUTATE:** inner fit bound × 0.8, as X77. It must move R(10¹⁰) by more than 5 %; otherwise the estimator is
  insensitive.
- A run that fails X77's fit flag is excluded and counted. If fewer than 6 of 9 ng 64 seeds survive at a mass, the
  verdict is UNDECIDED.
