# CFG561 FROZEN CRITERIA: do isolated KiDS lenses inside cosmic voids lens differently from matched lenses outside?

Frozen and committed before any script exists and before any lensing number for a void or outside subsample has been computed.
The only things looked at so far: the void catalogue's own columns (1,228 voids; 103 with centres in the KiDS-N box,
centre z 0.22–0.66, R_eff median 42 Mpc/h) and the lens file's column layout. κ = ½ is fitted, never derived. Both a₀
footings (9.3603e-11 / 1.1312e-10 m/s²) are irrelevant to this pure-data measurement; the verdict map below is a sign test,
not a footing-dependent prediction. No dark-matter particle; the framework's cold mass is still required (amount free).

## Question (council Session 13, rank 1)

At fixed M*, z and colour, do isolated KiDS-1000 lenses inside cosmic voids lens differently from matched lenses outside,
in the 1-halo bins (K1) and in the outer bins (KO)? Three pictures, three signs:

- **settling** (law-shaped cold fluid with a supply limit): a void lens's catchment is starved → LOWER outer lensing (Δ_KO < 0);
- **law as a force without an external-field effect** (foil; already excluded by wide binaries): the weakest external field →
  HIGHER lensing (Δ > 0);
- **ΛCDM**: small difference at fixed M* (assembly bias), declared |Δ| ≲ 0.1 dex, sign uncertain.
  Caveat stated now: in ΛCDM the 2-halo term of a void galaxy is also expected to be lower (smaller large-scale density
  around it), so a negative outer Δ is not by itself unique to settling; only its size could separate them. This lane does
  not model that; the verdict map is frozen as given by the task.

## Data

- Lenses: `real_research/data/lensing_rar/cfg110_perlens.npz` (WG, WW per lens per g_bar bin, 181,477 × 15), `lr_lenses.npz`
  (ra, dec, z = zphot_ANNz2, logM, typ = u − r > 2), `lr_esd_jackknife.npz` (50 June patches), exactly as CFG446.
  ESD = Σ WG / Σ WW / KG, KG = 1.989e30 / (3.0857e16)².
- Bins: K1 = g_bar bins 8–14 (1-halo, as CFG88/446); KO = bins 0–7 (outer: at log M* = 10.5 these are R ≈ 0.22–2.1 Mpc;
  the radius of a g_bar bin scales as M*^½, identical between void and matched-outside samples because they are M*-matched).
- Voids: Mao et al. 2017, ApJ 835, 161, BOSS DR12 ZOBOV void catalogue (CDS J/ApJ/835/161, table1.dat, fetched 2026-10-08;
  FETCH_LOG.md). Centres = weighted centres; radius R_eff in Mpc/h comoving; z 0.2–0.7. Only BOSS North overlaps KiDS-N
  (no void has Dec < −20, so KiDS-S has no coverage and is excluded).
- Neighbour pool for the positive control: CFG446's pool (KiDS DR4 bright sample, MAG_AUTO_CALIB < 20, 0.1 < zphot < 0.5,
  masked == 0, finite log M* > 7).

## Analysis set (frozen)

- Lenses with Dec > −15 (KiDS-N) and 0.22 ≤ z_l ≤ 0.50 (the void catalogue's redshift coverage; lenses at z < 0.22 cannot be
  certified outside a void and are excluded). Assumption declared: KiDS-N lies inside the BOSS North footprint; mask holes
  are not modelled.
- Distances: flat ΛCDM Ω_m = 0.3089, H0 = 100 h (comoving Mpc/h), used only to place lenses relative to voids.

## Void membership (photo-z handled by integration)

- Photo-z error σ_z = 0.02 (1 + z_l), Gaussian (outliers not modelled; declared).
- For each lens and void: r_p = D_C(z_void) × angular separation. If r_p < R_void, the void's line-of-sight chord is
  χ ∈ [D_C(z_v) − h, D_C(z_v) + h], h = √(R_void² − r_p²), converted to [z1, z2]; p = Φ((z2 − z_l)/σ_z) − Φ((z1 − z_l)/σ_z).
  Else p = 0. A lens's p_void = max over voids. Primary R_void = R_eff.
- **VOID sample:** p_void ≥ 0.25. **OUTSIDE sample:** p_void < 0.02. Lenses in between are excluded.
- Purity reported: p̄_V = mean p_void over VOID, p̄_O over OUTSIDE.

## Matching (frozen)

- Cells: log M* 0.1 dex from 8.5 to 11.0 (clipped to the edge bins) × z_l 0.025 from 0.22 to 0.50 × colour (typ 0/1).
  OUTSIDE lenses are reweighted cell by cell to reproduce the VOID sample's histogram; VOID cells with no OUTSIDE lens are
  dropped from the VOID sample (fraction reported).

## Statistic (frozen)

- For bin set K ∈ {K1, KO}: Δ_K = log10[ (Σ_V WG / Σ_V WW) / (Σ_O w WG / Σ_O w WW) ] pooled over the bins of K (the CFG446
  R-TRACE form), V unweighted, O with matching weights w.
- Errors: delete-one jackknife over the 50 June patches; variance factor (n − 1)/n with n = number of patches holding
  analysis-set lenses.
- Purity-corrected Δ (for the NULL bound only): Δ_c = log10[1 + (10^Δ − 1)/(p̄_V − p̄_O)], σ_c by the same transformation of
  the jackknife replicates.

## Verdict map (outer bins KO are the headline; K1 reported with the same map)

- **SETTLING-SIGN** if Δ_KO < 0 at > 3σ.
- **FORCE-SIGN** if Δ_KO > 0 at > 3σ.
- **NULL (ΛCDM-consistent)** if |Δ_KO| < 2σ AND the purity-corrected 2σ bound (|Δ_c| + 2σ_c) < 0.1 dex.
- **NON-DISCRIMINATING** otherwise (including 2–3σ, or a null that cannot bound 0.1 dex).
- Power (printed before any Δ): the expected σ_Δ from 100 random subsets of the analysis set with the VOID sample's size,
  matched the same way (C5); power to see a 0.1 dex outer offset at 3σ quoted as P = Φ(0.1 (p̄_V − p̄_O)/σ − 3) (diluted).

## Controls (load-bearing unless marked)

- **C1:** the per-lens sums reproduce CFG88's full-sample K1 early-minus-late D (1e-6 rel) and its zero-model Hartlap χ²
  35.0418/7 (1e-6 rel) — CFG446's C1, copied.
- **C2:** lens ↔ bright-sample exact position match (CFG446's C2), needed for the pool.
- **C3 (positive control / tracer):** void lenses sit in emptier surroundings. T = log10[mean N_V / mean_w N_O], N = pool
  galaxies within a projected 8 Mpc/h comoving radius and |Δz| < 2 × 0.018 (1 + z_l) of the lens (lens itself excluded),
  same matching weights, same jackknife. PASS if T < 0 at > 3σ.
- **C4 (random voids):** 20 random catalogues — each void keeps its z and R_eff, its centre is redrawn uniformly in
  RA 128–240°, Dec −4 to +4 (KiDS-N box) — through the identical pipeline. PASS if the mean of Δ_KO/σ and of Δ_K1/σ over the
  20 is within ±3/√20 · 1.5 of 0 and no single |z| exceeds 3.5. (Random voids may still land on real underdensities by chance;
  that is what the spread measures.)
- **C5 (null calibration, reported):** the std of Δ/σ over the 100 random subsets in [0.7, 1.3].
- **Sensitivity rows (reported only, never the verdict):** R_void = 0.5 R_eff (deep cores, p ≥ 0.25); VOID threshold
  p ≥ 0.5; p-weighted VOID sample (all p ≥ 0.02, weight p); early and late types separately.

## MUTATE (must FAIL, exit 1)

MUTATE=1 shuffles p_void among the analysis-set lenses (seed 561) before the samples are drawn. The tracer C3 (void lenses'
neighbour deficit at > 3σ) must then FAIL → exit 1. Δ_KO and Δ_K1 are printed and should return to null.

## What the verdicts can and cannot mean

A SETTLING-SIGN verdict is necessary for the settling picture but not sufficient against ΛCDM (see the caveat above);
a FORCE-SIGN verdict would conflict with the wide-binary exclusion and would be reported as a data anomaly; NULL bounds the
void effect at fixed M* below 0.1 dex. Nothing here can say the data favour the framework over ΛCDM. Not theory closed.
