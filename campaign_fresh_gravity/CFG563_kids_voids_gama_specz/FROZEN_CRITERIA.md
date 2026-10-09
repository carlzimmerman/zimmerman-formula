# CFG563 FROZEN CRITERIA: CFG561's void test redone with GAMA spectroscopic redshifts and a GAMA environment catalogue

Frozen and committed before any script exists and before any lensing number for a void or outside subsample has been computed.
κ = ½ is fitted, never derived. Both a₀ footings (9.3603e-11 / 1.1312e-10 m/s²) do not enter this pure-data sign test.
No dark-matter particle; the framework's cold mass is still required (amount free). Not theory closed.

## What was looked at before freezing (environment and positions only, no lensing)

- GAMA DR4 tables fetched from Data Central TAP (FETCH_LOG.md): Alpaslan et al. 2014 filament catalogue (`FilGalsv02`
  29,247, `TendrilGalsv02` 14,544, `VoidGalsv02` 1,677 galaxies) and Eardley et al. 2015 geometric environments
  (`GalaxiesClassifiedv01`, 117,556 galaxies, 0.04 < z < 0.263, GeoS4 / GeoS10 = 0 void, 1 sheet, 2 filament, 3 knot).
  CFG471's `G3CGalv10.csv` reused read-only (sha256 051950e1…f6ad9f8 verified against CFG471's FETCH_LOG).
- Counts only: 20,542 KiDS isolated lenses match a G3CGal galaxy within 1.5″ (all fields). Among matched lenses with an
  Eardley class: GeoS4 void 2,086, sheet 3,244, filament 2,509, knot 391. Alpaslan classes: void 160, tendril 1,002,
  filament 1,287.

## Departure from the task's preference (disclosed, decided on counts only)

The task preferred Alpaslan et al. 2014. Its "void" class (galaxies in neither filaments nor tendrils) holds only 160
matched lenses, which cannot measure anything. The headline therefore uses the other published GAMA large-scale-structure
catalogue on Data Central, Eardley et al. 2015 (tidal-tensor classification, 4 Mpc/h smoothing, GeoS4). Alpaslan's
classification is kept as a reported sensitivity row. No void finder of my own is run.

## Question and predictions (as CFG561)

At fixed M*, z and colour, do isolated KiDS lenses in GAMA voids lens differently from matched lenses outside, in the outer
bins (KO = g_bar bins 0–7, headline) and the 1-halo bins (K1 = 8–14)?

- **settling** (law-shaped cold fluid with a supply limit): starved catchment → LOWER outer lensing (Δ_KO < 0);
- **law as a force without an external-field effect** (foil; already excluded by wide binaries): HIGHER lensing (Δ > 0);
- **ΛCDM**: small difference at fixed M* (assembly bias), |Δ| ≲ 0.1 dex. Caveat kept from CFG561: in ΛCDM the 2-halo term
  around a void galaxy is also lower, so a negative outer Δ does not single out settling; only its size could, and this lane
  does not model that.

## Data and analysis set (frozen)

- Lenses and ESD: `real_research/data/lensing_rar/cfg110_perlens.npz` (WG, WW), `lr_lenses.npz` (ra, dec, z = photo-z,
  logM, typ), `lr_esd_jackknife.npz` (June patches), exactly as CFG561. ESD = Σ WG / Σ WW. The per-lens sums were built with
  the photo-z and are not recomputed; the spectroscopic z is used only for environment, matching and the C3 tracer (declared).
- Footprint: CFG471's GAMA boxes (RA 129–141, Dec −2..3; RA 174–186, Dec −3..2; RA 211.5–223.5, Dec −2..3).
- Cross-match: nearest G3CGalv10 galaxy within 1.5″ (CFG471's radius). Lens kept if |z_spec − z_phot| < 0.1(1 + z_spec)
  (drops catastrophic photo-z, whose ESD radii are wrong), and if its CATAID has an Eardley class with NQ > 2.
- **VOID:** GeoS4 = 0. **OUTSIDE:** GeoS4 ∈ {1, 2, 3}. Purity is taken as 1 on both sides (spectroscopic classification;
  so the purity-corrected Δ equals Δ).

## Matching (frozen)

Cells: KiDS log M* 0.1 dex from 8.5 to 11.0 (clipped) × z_spec 0.025 from 0.04 to 0.265 × colour (typ). OUTSIDE reweighted
cell by cell to VOID's histogram; VOID cells with no OUTSIDE lens dropped (fraction reported).

## Statistic and errors (frozen)

- Δ_K = log10[(Σ_V WG / Σ_V WW) / (Σ_O w WG / Σ_O w WW)] pooled over the bins of K (CFG561's form).
- Errors: delete-one jackknife over the June patches that hold analysis-set lenses (12 expected, as CFG471), factor (n−1)/n.
  Reported sensitivity: CFG471's 36 sub-patches (each patch split in three by lens-RA terciles).

## Power (printed before any void number)

100 random analysis-set subsets of the VOID size, matched the same way: expected σ_Δ (median) for KO and K1, and
P(3σ | true 0.1 dex) = Φ(0.1/σ − 3). If P < 0.5 the lane is declared UNDERPOWERED for a 0.1 dex effect before scoring;
the NULL verdict needs σ < 0.05 dex, so it is expected to be out of reach.

## Verdict map (KO headline; K1 reported with the same map)

- **SETTLING-SIGN** if Δ_KO < 0 at > 3σ.
- **FORCE-SIGN** if Δ_KO > 0 at > 3σ.
- **NULL (ΛCDM-consistent)** if |Δ_KO| < 2σ AND |Δ_KO| + 2σ < 0.1 dex.
- **NON-DISCRIMINATING** otherwise (including 2–3σ, or a null that cannot bound 0.1 dex).

## Controls

- **C1a (load-bearing):** CFG561's C1 copied: the per-lens sums reproduce CFG88's full-sample K1 early-minus-late D
  (1e-6 rel) and its zero-model Hartlap χ² 35.0418/7 (1e-6 rel).
- **C1b (load-bearing):** the same split restricted to the GAMA footprint: the pooled K1 early/late log ratio of all
  footprint lenses agrees with the full-sample value within 3σ (footprint jackknife).
- **C2 (load-bearing):** chance-match rate (lens positions shifted +60″ in Dec) < 2% of the real rate (CFG471's C2).
- **C3 (positive control, load-bearing, must pass):** T = log10[mean N_V / mean_w N_O], N = G3CGalv10 galaxies within a
  projected 8 Mpc/h comoving radius and |c Δz| / (1 + z) < 1000 km/s of the lens (lens itself excluded), same weights,
  same jackknife. PASS if T < 0 at > 3σ. (The Eardley flag is itself built from GAMA galaxy density, so this checks that the
  flag-to-lens pipeline works, not that voids exist; stated now.)
- **C5 (reported):** std of Δ/σ over the 100 power subsets in [0.7, 1.3].
- **Sensitivity rows (reported only, never the verdict):** GeoS10 void; VOID vs sheet + filament only (knots dropped);
  early only; late only; Alpaslan VoidGals vs FilGals + TendrilGals; headline with the 36 sub-patch jackknife.

## MUTATE (must FAIL, exit 1)

MUTATE=1 shuffles the VOID/OUTSIDE flag among analysis-set lenses (seed 563). C3 must then fail → exit 1; Δ_KO and Δ_K1 are
printed and should be null.

## What the verdicts can and cannot mean

SETTLING-SIGN is necessary for settling but not sufficient against ΛCDM (2-halo caveat). FORCE-SIGN would conflict with the
wide-binary exclusion and be reported as a data anomaly. Nothing here can say the data favour the framework over ΛCDM.
