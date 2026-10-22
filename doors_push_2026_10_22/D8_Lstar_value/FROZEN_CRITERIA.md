# D8_Lstar_value — FROZEN CRITERIA (written before any script or number of this lane)

Door: the microscopic value of the stiffness length L*. Rules: `doors_push_2026_10_22/BRIEF.md`.
κ = ½ is FITTED. Footings never pooled: canonical a0 = 9.36e-11, alt a0 = 1.13e-10 m/s² (BRIEF);
when CFG820's χ² is re-evaluated, its own footing values 9.3603e-11 / 1.1312e-10 are used (disclosed).
No dark-matter particle. Not "theory closed".

## Inputs (all read-only, from the record)

- DSF-21 A76 `a76_results.json` (c_s at 24 pc, ρ_c), A65 (L* = σ_c²/a0, coefficient 1).
- AG6D Part A identity c_s² = 2πG L*² ρ̄ (free cold medium, Γ = 2); AG6D C1 bound L*_IC:
  frozen scan `< 1 pc` (`ag6d_cutoff_results.json`), post-hoc 0.247 pc (`ag6d_cutoff_posthoc_results.json`).
- CFG820 cluster table (`campaign_fresh_gravity/CFG332_globulars_three_routes/cfg332_globulars_results.json`)
  and CFG820's estimator (copied verbatim into this lane's script, not imported: importing cfg820.py would
  rewrite its outputs).
- Thermal width σ_th = √(k_B T/(μ m_H)) at T = 1e4 K, μ = 1.22 (the record's premise; μ ∈ [0.60, 1.40] bracket).

## Part 1 — adjudication: are A76's L* = σ_c²/a0 and AG6D's EOS stiffness the same object?

- **K1 (same formula).** Recompute A76's c_s(24 pc) from AG6D's c_s² = 2πG L*² ρ̄ with A76's ρ_c.
  PASS iff |rel. diff| < 1e-3 against A76's stored value. PASS means A76's γ/c_s statement *is* the
  free-medium Γ = 2 EOS that AG6D C1 tests.
- **K2 (C1 applied to A76's reading).** σ_c,max = √(a0 · L*_IC) with the frozen L*_IC = 1 pc (conservative)
  and post-hoc 0.247 pc, both footings. PASS iff σ_th / σ_c,max(1 pc) ≥ 3 on both footings.
  PASS means: if L* = σ_c²/a0 is read as the free medium's EOS stiffness, the 10⁴ K value is excluded by
  the framework's own initial conditions. FAIL means the 10⁴ K reading survives C1.
- **K3 (σ_c is not the medium's sound speed).** At L* = σ_th²/a0: ratio σ_th / c_s(ρ̄_c) and the density
  ρ_eq = a0/(2πG L*) at which the Γ = 2 sound speed equals σ_c. PASS iff σ_th/c_s(ρ̄_c) ≥ 1e3 and
  ρ_eq/ρ̄_c ≥ 1e6 on both footings. PASS means the two relations coincide only at galactic densities,
  so A76's σ_c can only describe a tethered (bound) state, never the free medium.

## Part 2 — record check: is the 24 pc floor a measurement?

A76 states the 24 pc floor "is not a measurement" (the 10⁴ K width rounded) and "no datum on disk
excludes L* = 23.43 pc". A11's script cites the floor as `[EXT] CFG820` (a globular χ² bound).

- **K4 (reproduce CFG820).** Re-implemented CFG820 estimator on CFG820's grid gives L*_95 (primary,
  no Pal 3) within 0.5 % of 23.957 pc (canonical) and 24.721 pc (alt). Then a fine-grid root
  (Δχ² = 3.84 crossing) is reported.
- **C5 (classification, not pass/fail).** Δχ²_CFG820(L*_th) at μ = 1.22, T = 1e4 K, per footing.
  Δχ² > 3.84 ⇒ "thermal 10⁴ K / μ = 1.22 identification EXCLUDED at 95 % by the outer globulars on that
  footing" (and A76's "no datum excludes 23.43 pc" is wrong on that footing). Δχ² ≤ 3.84 ⇒ "allowed".
- **C6 (report).** The σ_c floor implied by CFG820: σ_min = √(a0 L*_95); T_min at μ = 1.22; μ_max at 1e4 K.

## Part 3 — is σ_c measurable on data on disk? (matching rule frozen here, before any search)

Search protocol: `_external_data/` and repo data directories, file names and ReadMe/header text only,
for per-galaxy **gas** velocity dispersions (HI second moment, HI line-width dispersion, Hα/warm-gas σ),
keywords `sigma`, `disp`, `mom2`, `velocity dispersion`, `sigma_HI`, `vdisp`. Stellar dispersions
(dSphs, GCs) are excluded: they are not σ_c. ALFALFA W50, SPARC errV, and rotation-curve errors are
excluded (A76 §3.1 already shows they are not σ_c).

**Matching rule.** For each galaxy i with a published gas dispersion σ_i: L*_pred,i = σ_i²/a0,
coefficient exactly 1, σ_i as published (thermal + turbulent; no μ assumption, no correction).
Statistic: sample median and 16–84 % range, per footing.
- median ∈ [L*_95(CFG820, footing), 90 pc] on that footing ⇒ CONSISTENT; the prediction is L* = median.
- median < L*_95 ⇒ TENSION with CFG820. median > 90 pc ⇒ TENSION with the A20 ceiling.
- 84/16 ratio of L*_pred > 2 ⇒ L* is not one constant under the tethered reading (report).
- no qualifying dataset ⇒ DATA-GATED; name the data that would be needed.

## Verdict rule

CRISP FINDING if K1–K3 pass (the tension is adjudicated with numbers) or C5 shows the record's
"no datum excludes" statement is wrong on at least one footing. RUNNABLE NOW if Part 3 finds data and
the matching rule runs. DATA-GATED if Part 3 finds none and Parts 1–2 add nothing. NOTHING NEW otherwise.

## Mutation

`D8_MUTATE=1`: use K = 8πG in the Γ = 2 relation (γ = 4πG L*²). K1 must fail (factor √2 in c_s).

## Compute

`OMP_NUM_THREADS=1 nice -n 10`, stdlib + numpy, seconds, no network, no downloads.

## AMENDMENT A1 — PRE-RESULT (written after the file/header inventory, before any σ value was read or any script run)

Part 3 inventory (file names and column headers only):
- **Qualifying, z ≈ 0, HI, per galaxy (PRIMARY):** `real_research/data/tidal_dwarfs/lelli2015_tdg.csv`
  (`sigma_HI_kms`, `e_sigma_HI_kms`; Lelli+2015 Table 7, 3D kinematic models of HI cubes; 6 tidal dwarfs).
  Cross-check transcription: `real_research/data/tdg/lelli2015_tdgs.csv` (independent transcription, if it carries σ).
- **Qualifying under the frozen text as written, but not σ_c by the record's own definition** (A65 §5 / A76 §9 define
  σ_c as the cold phase of a low-mass dwarf at z ≈ 0): ionised-gas σ0 of z ≈ 0.5–3 star-forming discs
  (`real_research/data/kmos3d_ubler2017.csv`, `kross_harrison2017.csv`, `rc100_nestorshachar2023_table3_CORRECTED.csv`,
  `msa3d_2026_rotation_curves.csv`, `data_assembly/high_z_tf_tables/simons2016_sigma.csv`). These are run with the
  identical frozen rule and reported as **SECONDARY (frozen-as-written)**; they carry no verdict weight.
- **Excluded by the frozen protocol:** stellar dispersions (dSph/UFD/GC tables, ATLAS3D, SLACS, SLUGGS, Walker 2023),
  global HI widths (ALFALFA, FASHI, xGASS, MIGHTEE), DiskMass `sigMod` (an extra error term, not a dispersion),
  GMC CO line widths (molecular clouds, not per-galaxy gas), McQuinn+22 (no σ column; V_cor − V_rot is a model
  correction, not a published σ), SPARC / LITTLE THINGS (no dispersion column; A76 §3.1).
- Caveat stated before the result: tidal dwarfs are young (< 1 orbit), gas-dominated, and their σ_HI comes from
  kpc-scale beams, not the 30–100 pc maps A76 §9 asks for. A PRIMARY result from them is a first look, not the
  measurement A76 specifies.
