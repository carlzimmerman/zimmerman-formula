# EUC4 (WIDE LENSES): FROZEN CRITERIA

Committed alone, before any EUC4 script exists and before any EUC4 number is computed. 2026-11-12.
Owner, 2026-11-12: "keep swinging while EUC3 runs".

κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt), never pooled. Not "theory closed". One-sided test: no
outcome favours the framework.

## 0. What this lane is

EUC1 (898cefb457) gave NO VERDICT on the whole sample P. Its exploratory map then showed where the excess sits: with
the source at infinity, the fraction of grade-A lenses needing more than 1.78 × Salpeter under law S was 0.31 for
Einstein radii of 1.3–1.7″, 0.62 for 1.7–2.5″ and 0.90 above 2.5″, against 0.03–0.07 below 1″. That split was made
after the numbers were seen, so it is a hypothesis, not a result.

Part A tests the hypothesis on lenses the map never used: the **grade-B** lenses, disjoint from P by construction.
Part B (exploratory) asks what the law itself would need in baryons outside the lens galaxy to make such lenses.

## 1. Data, model, statistic

Exactly EUC1's: the same two catalogue files (same hashes), the same cosmology, Sérsic deprojection, laws S and B,
projection, source at infinity (z_s = 1100), and `b` = log₁₀ of the stellar-mass boost the law needs. EUC1's code is
imported, not rewritten.

**Sample W_B (primary):** `lens_grade == 'B'`, `lens_model_success`, `final_sample`, no `large_system_warning`, EUC1's
five validity conditions, and `eclipse_effective_einstein_radius ≥ 1.7″`.
**Secondary:** the same with 1.3″ ≤ θ_E < 1.7″. **Complement (reported):** the same with θ_E < 1.0″.

**Statistic:** `f₂₅` = fraction with `b > 0.25`, law S, per footing, 95 % bootstrap interval (2,000 resamples, seed
20261112). Law B beside it.

**Words, per footing, on W_B:**
- **WIDE LENSES BREAK THE CEILING** if the lower bound of `f₂₅` ≥ 0.25;
- **NOT CONFIRMED** if the upper bound ≤ 0.10;
- **NO VERDICT** otherwise;
- **NOT EVALUABLE** if N < 30 or an instrument check fails.
The secondary bin gets the same words, labelled secondary.

**Seen before freezing (disclosed).** EUC1's map on grade A (the numbers above). EUC1's robustness run 7 on grades A+B
together (f₂₅ 0.164 / 0.145), from which grade B's overall fraction is about 0.17: so grade B as a whole looks like
grade A. No grade-B number by Einstein radius has been computed or read. A back-of-envelope estimate that a group's
baryons can raise the law's supply by several hundred M☉ pc⁻² (the reason for Part B).

## 2. Instrument checks (frozen)

- **E1** the imported machinery reproduces EUC1's primary numbers on P: `f₂₅` = 0.156 (canonical), 0.139 (alt) to 0.001.
  (EUC1's own checks K1–K4, K6 stand behind those numbers.)
- **E2** grade B and grade A are disjoint by identifier (count of shared identifiers = 0).
- **MUTATE** (`EUC4_MUTATE=newton`, a₀ → 10⁻³⁰): `f₂₅` on W_B must rise on both footings; exit 1; separate outputs.

## 3. Robustness (reported; cannot change the word)

`R_e × 0.80`; `n = 4`; SIE Einstein radius (with the 1.7″ cut applied to it); z_l < 1.0; `r_max = 300 kpc`; and the
threshold moved to 1.5″ and 2.0″.

## 4. What the words mean

- BREAK: the law, acting on the lens galaxy's catalogued stars alone, cannot make wide-separation lenses for any
  source redshift, with any IMF up to 1.78 × Salpeter. Such lenses then need either baryons outside the lens galaxy
  (group gas and neighbours, acted on by the same law) or gravitating density beyond the law's cold pull. Part B sizes
  the first.
- NOT CONFIRMED: EUC1's map split does not replicate; it was a fluctuation or a grade-A selection effect.

## 5. Part B (EXPLORATORY; no verdict; labelled as such)

For every lens of P and of grade B with θ_E ≥ 1.7″: add to the stars a spherical gas body, β-model with β = 2/3
(`ρ ∝ [1 + (r/r_c)²]⁻¹`), cut at 500 kpc, core radius `r_c` = 30 and 100 kpc (two runs). Solve for the gas mass inside
500 kpc, `M_g`, at which law S supplies the lens: (i) source at infinity, (ii) source at z_s = 3. Stars at the
catalogue's Salpeter mass, and at 1.174 × (A70's SLACS value). Reported: the distribution of `M_g` and of `M_g/M★`, and
the mean surface density the law's cold pull then supplies.

A reference range for the gas actually observed in X-ray groups with massive central galaxies (about 1–4 × 10¹² M☉
inside R₅₀₀, quoted from memory of the group scaling-relation literature, PROVISIONAL) is printed beside it for
orientation only. Part B makes no claim that these lenses sit in such groups: the catalogue has no environment
measure. It answers one question: is the gas mass the law would need of the order groups have, or far beyond it.

## 6. Not claimed

No statement about clusters. No measurement of a₀ or κ. No statement that any lens is or is not in a group.
