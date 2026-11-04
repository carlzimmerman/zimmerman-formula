# FN4b_lg_external_field: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Item 4 of the finish push, row group "Local Group dwarfs and ultra-faints" (and IC 1613 as a field dwarf). κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. Footings never pooled: canonical a0 9.3603e-11, alt 1.1312e-10 m/s². **No download: every input is on disk.**

## Question
The law-rule ledger lists as open: "Local Group external field from a new estimator (UNGC plus Milky Way and M31): not built." NV2 found no external-field estimate for the Local Group dwarfs, the ultra-faints or IC 1613. This lane builds one from a catalogue and asks two things.
1. **Sign test.** Within each class, do the law's residuals trend with the catalogue field the way an external-field effect would (residual falling as the field rises)?
2. **Size.** Does replacing the host-only field with the whole catalogue's field move any class median by a graded amount?

## Inputs (all on disk)
- Catalogue: UNGC, Karachentsev+13, `real_research/data/ungc_karachentsev2013.tsv` (869 galaxies). Baryons M_b = 0.6 L_K + 1.33 M_HI, the convention CZ1 used for M31. Bracket Υ_K 0.3 and 1.0.
- Milky Way: point mass 7.0e10 M☉ at the Galactic centre (KT15's frozen value, as CZ1). M31: from UNGC as above (`MESSIER031`).
- Systems and residuals: `rebuild_2026_10_22/X1_hosted_recount/x1_per_system.csv` (name, host, class, M_V, r_h, σ, and the residual Δ of the isolated law, column `Delta[iso AQUAL L*0]`, per footing). Positions and distances from LVD, `real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv`, matched by name.
- Galactocentric positions with astropy (`Galactocentric`, R₀ 8.178 kpc), as CZ1.

## Estimator
For each system: g_Ne = |Σ over Milky Way, M31 and every other UNGC galaxy of G M_b d̂ / d²| (Newtonian vector sum). The system itself is excluded: any UNGC row within 0.1° and |ΔD|/D < 0.25 of it. The host (Milky Way or M31) is kept in the total and also reported separately. y_e = g_Ne / a0, per footing.

## Tests and labels (frozen), per footing
- **T1 sign test**, per class (X1's classes; individual-class rows by host): Spearman ρ between Δ and log y_e, p from 10,000 permutations (fixed seed).
  - **EFE-SIGNED TREND**: ρ < 0 with p < 0.01.
  - **OPPOSITE TREND**: ρ > 0 with p < 0.01.
  - **NO TREND**: otherwise.
- **T2 size**, per system: the shift in the record's corrected one-zone form (CZ1 Part D), ΔE = log ν(√(y_N² + y_host²)) − log ν(√(y_N² + y_e²)), with y_N = G(M_b/2)/r½² / a0, r½ = (4/3) r_h, M_b from X1's log M★ (plus 1.33 M_HI where LVD gives it). Per class, the median ΔE against the class error σ_c = |median Δ / Z| from LW1's plain-law table (MW ultra-faint, MW classical, bright M31, M31 others, LG field). A class LW1 does not list (X1's M31 dE, 3 systems) uses σ_c = 1.2533 × sd / √n of its X1 Δ values. "|Z| crosses 2" uses Z = median Δ / σ_c before and after.
  - **FIELD MOVES A ROW**: some class median moves by at least σ_c, or its |Z| crosses 2.
  - **FIELD MOVES NOTHING**: otherwise.
- **NOT EVALUABLE**: any of K1–K4 fails.

## Known answers and checks
- **K1** with the Milky Way and M31 only, IC 1613's y_e reproduces CZ1 Part D (3.4e-4 canonical, 2.8e-4 alt, from `cz1.json`) to 1e-6 relative.
- **K2** planted catalogue: one 1e11 M☉ point at 1 Mpc gives G M/d² to 1e-12 relative; a symmetric ring of 12 equal masses gives zero net field at its centre to 1e-12 of one member's field.
- **K3** self-exclusion: a planted duplicate of a system is excluded; the count of excluded rows is reported.
- **K4** every X1 system gets a position (LVD match); unmatched names are listed and the check fails if more than 5 % are unmatched.
- **MUTATE** (`FN4B_MUTATE=1`): every UNGC distance × 0.5. K1 must fail, exit 1.
- Rerun byte-identical JSON.

## Reported beside the labels (no line)
The median non-host fraction of the field per class; the three galaxies that dominate each field dwarf's sum; the Υ_K 0.3 and 1.0 brackets; UX4's host-field slope (−0.05 ± 0.20 per dex, prediction −0.75) set beside T1's.

## Expectation, written before running
The non-host field should be a small fraction of the host's for satellites, and about 1e-4 to 1e-3 a0 for the field dwarfs, far below their internal y_N (about 0.01–0.03). So T2 should read FIELD MOVES NOTHING. T1 has about 15 field dwarfs and low power.

## Compute
One thread, `python3 -I`, `nice`; seconds; RSS well under 1 GB.
