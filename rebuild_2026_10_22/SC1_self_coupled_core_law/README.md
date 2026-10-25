# SC1_self_coupled_core_law — RESULT: SC PASSES SPARC ONLY (both footings); clusters improve but not by the frozen 50%

Frozen criteria b5e95b9c9e (committed alone; no amendment). κ = ½ FITTED; footings never pooled; cold dark energy, not
matter; nothing here says the data favour the framework or ΛCDM; not "theory closed".

**Law graded.** LN1's T7 (Lean-certified) core law at fixed q = 1/3: X38's route-E Burkert halos with
Σ_i = Σ_a0 (σ_i/σ_ref)^(1/3).
- σ_ref = 70.50 km/s, the median SPARC V_last/√2, keeps the median galaxy at a₀/(2πG).
- Cluster σ comes from KT (median 517.12 km/s, K1); 220 clusters without a KT are filled by tercile.
- The cluster core surface density comes out 1.84 / 1.94 / 2.15 × Σ_a0 by KT tercile.

## Result (`sc1_core_law.out`)

| | canonical | alt |
|---|---|---|
| SPARC rms @ median Υ, background A (X38) | **0.0686 @ 0.75** (0.0795 @ 0.77) | **0.0636 @ 0.63** (0.0729 @ 0.60) |
| SPARC background B (X38) | 0.0683 @ 0.75 (0.0792 @ 0.76) | 0.0637 @ 0.60 (0.0729 @ 0.60) |
| MID T3 Z (X38) | +2.26 (+4.26) | +1.75 at h 0.672; fails at the other h (+3.80) |
| MID KT slope Z | +2.36 (+3.07) | +2.22 (+2.99) |
| OUTER M3 Z | +3.82 (+5.36) | +3.47 (+4.94) |
| OUTER M-all, MID T2 | now pass (were +2.36, +1.80) | pass |
| summed |Z| of X38's failing cells | 17.61 → **11.40** (−35%) | 14.26 → **9.11** (−36%) |
| new failures | none | none |
| **class** | **SC PASSES SPARC ONLY** | **SC PASSES SPARC ONLY** |

Checks 4/4: K0 (q = 0 reproduces X38 exactly) and K1. MUTATE (σ = σ_ref everywhere) reproduces X38 exactly; exit 1, as
frozen.

## What it means

- **The core law does better than a constant a₀ surface density everywhere it was graded.** SPARC improves by
  0.009–0.011 dex rms at the same Υ. That is the first improvement over X38 on SPARC. Every cluster cell moves toward the
  data, and none gets worse.
- **It is not enough for the heaviest clusters.** Three cells still fail: MID T3, the MID KT slope, and the gas-heaviest
  OUTER tercile.

## Reported only (not graded; q was fixed before the run and is not re-chosen here)

| variant | SPARC (A) can. / alt | still failing (canonical) | still failing (alt) |
|---|---|---|---|
| clusters at half the galaxy age (× √2) | unchanged | MID slope, OUT M3 (+3.19) | MID slope, OUT M3 (+2.87) |
| q = 1/4 | 0.0710 / 0.0655 | MID T3, slope, OUT M3 | same |
| q = 1/2 | **0.0646 / 0.0607** | MID slope (+1.93 at h 0.672), OUT M3 (+3.15) | **OUT M3 only (+2.83)** |

**Inside SPARC, rms falls steadily as q rises from 0 to 1/2.** So the galaxies themselves prefer a core surface density
that grows with σ. LN1's window premise "galaxies flat within ×2" was more conservative than SPARC needs.

## The decisive cross-check, disclosed in the criteria

A larger q lowers dwarf cores: Σ(σ ≈ 10 km/s) = 0.52 Σ_a0 at q = 1/3 and 0.38 Σ_a0 at q = 1/2. CD1's dwarfs need a median
of 0.53 (canonical) / 0.44 (alt) of the Σ_a0 cap. So the dwarfs pull q down while SPARC and clusters push it up, and one q
is either squeezed or ruled out.

The clean next lane, with frozen criteria:
1. Calibrate q once on SPARC alone (one constant, as X40 did).
2. Grade it out of sample on X30's clusters and on CD1's dwarfs at that q.
