# CS1_core_surface_density_atlas: the measured core surface density rises with σ (q ≈ 0.7, 0.25 dex scatter); the frozen class is NO SIMPLE LAW, set by the eRASS1 stacks

Criteria and assumption ledger: `FROZEN_CRITERIA.md` and `ASSUMPTION_LEDGER.md`, committed alone in 6f303e256b before
any script or number. There is no amendment.

Standing caveats:
- κ = ½ is FITTED.
- The two footings are scored separately and never pooled.
- Route E: Newtonian gravity, with cold dark energy = observed − baryons. Cold dark energy is a gravitating field
  component, not a particle.
- No ΛCDM input enters any measured Σ₀: no c(M), no c_f, no halo-mass function, no cosmic baryon fraction.
- Not "theory closed". Nothing here says the data favour the framework or ΛCDM.

Every number below is from `cs1_atlas.out` and `cs1_atlas_results.json`. The per-system table is `cs1_atlas.csv` and the
figure is `cs1_atlas.png`.

## What was done

Every system's own data were fitted by one method: a Burkert halo (isothermal core as a variant) fitted to observed −
baryons. This gives Σ₀ = ρ₀r₀ with a profile-likelihood interval.

| class | input | result |
|---|---|---|
| SPARC (175) | EM1 loader, Υ profiled per galaxy | 165 two-sided, 5 lower bounds, 1 upper, 4 unconstrained |
| Milky Way | Ou+24 minus GD1's McMillan baryons | two-sided |
| X-COP | 7 with stars; 5 more as an M★ = 0 variant | all two-sided |
| eRASS1 | 3 KT terciles | all two-sided, but wide (T1 ±0.6 dex) |
| dwarfs (88 of 89 with detected cold mass) and groups (63) | two-point / one-point data | **lower bounds only** (Burkert Σ_min = 0.6254 M/r₁₂², at r₀ = r₁₂/0.963), never quoted as measured Σ₀ |

**Σ₀ is a₀-free everywhere.** The eRASS1 terciles are measured relative to the footing's C* template, and that template
cancels between the measured and predicted ratio. So canonical and alt give identical Σ₀ and identical law fits. Only
the candidates' Σ_a₀ and q_f differ by footing.

## Verdict (frozen classes, both footings agree)

| read-out | canonical | alt |
|---|---|---|
| PRIMARY (176 two-sided points, σ 13–1179 km/s) | **NO SIMPLE LAW** | **NO SIMPLE LAW** |
| WHOLE-RANGE (plus 5 + 88 + 63 lower bounds, Tobit) | **NO SIMPLE LAW** | **NO SIMPLE LAW** |
| dwarfs vs the PRIMARY law | PARTIAL (8% of 88 exceed at 2σ) | PARTIAL (8%) |
| groups vs the PRIMARY law | CONSISTENT (0 of 63) | CONSISTENT |

**The best simple law is a single power law, and it wins decisively.**

    log Σ₀ [M☉ pc⁻²] = 2.223 + 0.692 log(σ / 70.5 km/s),   intrinsic scatter 0.249 dex

- The slope is q = 0.692 ± 0.060, an 11.6σ trend.
- On BIC it beats the flat floor by ΔBIC 92. The broken law gains nothing (ΔBIC +1.7, so the simpler model is taken).
- Floor + rise has its floor outside the data's range, so it is not selectable.
- Spearman ρ(Σ₀, σ) = +0.60 (p 2e-18). ρ(Σ₀, M_b) = +0.49. ρ(Σ₀, r₀) = +0.14 is not significant.

**Why the class is NO SIMPLE LAW anyway.** The frozen override fires on one class: the three eRASS1 terciles sit
−0.45 dex below the law. Using the sample standard error of three residuals, that is 5.1 se.

How fragile that override is:
- The three tercile points line up closely, so their sample standard error is small (0.088).
- If the standard error is built from their own measurement errors plus s_int, it becomes ≈ 0.26 dex, and the offset is
  ≈ 1.7σ. The class would then be SINGLE POWER LAW.
- The frozen rule is applied as coded before any number: sample standard error. So the verdict stands, but it rests on
  three stacked points with 1 degree of freedom each.

**X-COP sits 0.14 dex below the law at 3.4 se.** That is under the frozen 0.25 dex size threshold, so it does not
trigger the override.

**The two cluster sets disagree with each other:**
- X-COP: Σ₀ ≈ 10^2.94 at σ ≈ 1000 km/s;
- eRASS1: Σ₀ ≈ 10^2.2–2.6 at σ ≈ 440–700 km/s.

Their σ conventions also differ: V_c,HSE(R500)/√2 for X-COP, because no X-COP temperature is on disk, versus √(kT/0.6 m_p)
for eRASS1. And the eRASS1 fit is a stack with one shared x₀ = r₀/R500 (≈ 0.2). Part of the gap is likely convention, but
this lane does not separate it.

**WHOLE-RANGE.** Adding the bounds:
- The selected model is BROKEN, but with an unphysical slope of −16.7 below σ ≈ 18 km/s. That is a wall: the dwarf
  bounds sit above the power law's extrapolation, and the fit puts a near-vertical step there.
- The eRASS1 override also fires here, at −0.43 dex.
- Read plainly: **toward dwarf σ, Σ₀ stops falling as σ^0.7.**

## The candidates on the measured atlas

Residual = measured − candidate, in dex. Both χ² columns are over the 176 PRIMARY points.

| candidate (canonical; alt in brackets) | χ² (with s_int 0.25) | SPARC median | MW | X-COP median | eRASS1 median |
|---|---|---|---|---|---|
| X38 flat Σ_a₀ 107 (129) | 490 (402) | +0.21 (+0.13) | +0.62 (+0.54) | **+0.91 (+0.83)** | +0.40 (+0.32) |
| OS1 Σ_a₀ (σ/70.5)^0.892 (^0.748) | 268 (214) | +0.22 (+0.12) | +0.41 (+0.36) | −0.16 (−0.07) | −0.37 (−0.33) |
| X43 max(Σ_a₀, 14.83 Σ_coll), on its own M200 | 399 (335) | +0.21 (+0.13) | +0.62 (+0.54) | +0.22 (+0.22) | −0.17 (−0.17) |
| **CS1 measured power law** | **187** | +0.00 | +0.26 | −0.11 | −0.39 |

- **X38's flat floor is excluded as the law.** Σ₀ spans ~2 dex across SPARC → clusters and tracks σ. Clusters sit
  0.8–0.9 dex above Σ_a₀, the same "heavy cores" miss seen before.
- **OS1 has the right shape.** SPARC alone gives q = 0.882 here, matching OS1's canonical 0.892 from a completely
  different procedure: OS1 imposed the law and fitted rms; here each galaxy has a free Burkert halo.
  - With every class in, the slope comes out flatter, 0.69.
  - OS1's amplitude sits 0.1–0.2 dex below the SPARC median, because it was calibrated with EM1's M200 normalisation.
  - It is the best candidate on alt.
- **X43** fits the clusters better than X38 and does no better than X38 below its crossover.
- The measured law beats every candidate. No candidate reaches the s_int-limited χ² ≈ N.

## Where the Milky Way sits

The MW's own data (Ou+24 minus GD1's McMillan baryons) give:
- Σ₀ = 10^2.65 M☉ pc⁻², i.e. 4.2 Σ_a₀ canonical / 3.5 Σ_a₀ alt;
- r₀ = 5.2 kpc;
- χ² 7.4 / 35.

Against the candidates:
- **The CS1 law:** at the MW's σ = 122 km/s it predicts 10^2.39. The MW sits +0.26 dex above it, at z = +1.0 within the
  scatter. **The MW is an ordinary member of the measured relation.**
- **OS1:** the MW sits +0.41 / +0.36 dex above OS1's value at the same σ (2.24 / 2.29).
- **GD1's Eilers requirement** is ≈ 3.5 Σ_a₀ = 10^2.57 / 10^2.66. The MW's measured Σ₀ is right at it.

So GD1's 4–6σ V_c(R₀) miss is not the Milky Way being anomalous. It is OS1's amplitude together with its M200-fixed r₀
falling about 0.3–0.4 dex short for a σ ≈ 120 km/s system with the full scatter.

The stellar-scale band (S3's five values) moves the MW's Σ₀ over 10^2.58–2.75. A short disc (GD2) is not run here.

## Where the dwarfs sit

The dwarfs give only lower bounds: one cold mass at r₁₂ cannot fix (ρ₀, r₀).
- The median Σ_min is 10^1.76 at σ ≈ 6 km/s. That is 0.54 Σ_a₀ canonical (0.44 alt), so the bounds are **compatible
  with a flat floor near Σ_a₀**.
- It is +0.27 dex above the power law's extrapolation at that σ.
- Only 8% exceed the law at 2σ (PARTIAL). Because these are lower bounds, the true Σ₀ can only be higher.

Median Σ_min by X1 class:

| X1 class | median log Σ_min |
|---|---|
| M31 dE | 2.31 |
| M31 others | 1.99 |
| MW classical | 1.97 |
| LG field | 1.85 |
| MW ultra-faint | 1.74 |
| bright M31 | 1.62 |
| Crater II | 0.21 |
| Antlia II | 0.67 |

This is the record's dwarf blank seen from measured cores: below σ ≈ 20 km/s, the data do not continue σ^0.7. They hold
at or above ≈ 10^1.8.

The groups' Wolf bounds (median 10^1.11) are too weak to say anything: 0 of 63 exceed the law.

## Variants (reported only)

- **Isothermal core:** q = 0.85 (169 two-sided).
- **SPARC at Υ ≡ 0.50:** q = 0.72, s_int 0.24.
- **X-COP all 12, with M★ = 0 for 5:** median 10^2.82, against 10^2.94 for the primary 7.
- **eRASS1 h 0.686** at the h 0.672 best point: χ² 0.43 / 0.83 / 1.02 for 1 dof.

In both the isothermal and Υ ≡ 0.50 variants the power law beats flat by ΔBIC ≈ 100.

## Checks 7/7

| check | result |
|---|---|
| K0a | loader equals EM1 exactly; EM1 law rms 0.0541 / 0.0537 and Newtonian row 0.2528 reproduced |
| K0b | X-COP 42 rows equal the matched-clumping lane exactly |
| K0c | X38's halos reproduce X38's tercile cells exactly |
| K1 | closed forms vs quadrature |
| K2 | planted Σ₀ and r₀ recovered exactly; dwarf Σ_min analytic = brute force |
| K3 | input counts; SPARC median σ = 70.50 |
| K4 | 0.67 GB, one thread |

**MUTATE** (`CS1_MUTATE=1`): σ is shuffled across the PRIMARY systems. The slope goes to −0.03 / +0.00 (0.4σ / 0.0σ), and
ΔBIC(M0 − M1) = −5. **The control bites; exit 1, as frozen.**

The shuffled run is also NO SIMPLE LAW, via X-COP +0.59. That shows the override responds to the cluster classes
generically.

## Implementation choices fixed in the code before any graded number

- σ_logΣ is floored at 0.005 dex in the law fit.
- SPARC and cluster one-sided points enter the Tobit fit at their Δχ² = 1 end, with s_int only.
- The eRASS1 grid uses log Σ₀ steps of 0.1 and log x₀ steps of 0.1, with a cubic-spline profile on 0.01 steps. One dof
  per tercile.
- The X43 Σ_coll table is extrapolated log-linearly outside 10^11–10^15. Below the crossover the floor rules anyway.
- X1's Δ[Newton] differs slightly between footings (≈ 0.004 dex, from its binary correction). The dwarfs are therefore
  run per footing.

## Reading

**What the data say, in their own terms:**
- From σ ≈ 13 to ≈ 1200 km/s, the cold dark energy core surface density is not flat. It rises roughly as σ^0.7, with
  0.25 dex scatter.
- That makes OS1's direction right and X38's flat floor wrong as a universal law.
- The Milky Way is a normal member of that relation.
- The one class that does not sit on it is the eRASS1 stacks (−0.45 dex). The frozen rule turns that, fragilely, into
  NO SIMPLE LAW.
- Below σ ≈ 20 km/s the dwarf lower bounds sit at ≈ 10^1.8. That is above the power law and at or below Σ_a₀, which hints
  at a floor near a₀/(2πG) under a rise. Bounds alone cannot establish the floor.

**What would decide it:**
- per-cluster temperatures for X-COP, or a per-cluster rather than stacked eRASS1 fit, to put both cluster sets on one σ
  convention;
- dwarfs with resolved dispersion profiles, to turn the lower bounds into measurements.

## Files and run

- `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md`
- `cs1_atlas.py`
- `cs1_atlas.out`, `cs1_atlas_results.json`, `cs1_atlas.csv`, `cs1_atlas.png`
- the `_MUTATE` twins of the output and results files
- `cs1_x30_machinery*.log` (local only; `.log` is gitignored)

Run:

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 cs1_atlas.py                # ~31 min (eRASS1 grid), exit 0, 7/7
    CS1_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 cs1_atlas.py   # exit 1 = control bites

The committed run set `CS1_ERASS_CACHE` to a scratch folder. The normal run computed the eRASS1 χ² grids and saved them
there; MUTATE loaded the same grids. The numbers are identical either way.

The groups read Tian+2026 from `_external_data/vizier2026/J_A_A_710_L39.tsv`, which is outside git (as in P4). Nothing
was downloaded.
