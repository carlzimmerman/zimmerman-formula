# GH5_tsz_desi_centrals

**Question.** GH3/GH4 left the hot-gas extent NOT DECIDED on 88k KiDS isolated lenses. Does the gas around MW-mass centrals
extend past R_vir, using ~2.5× more DESI DR1 spectroscopic lenses already on disk? Criteria frozen first (11dc18546f).

## Verdict

**Frozen class, PRIMARY (CIB-deprojected, central, 206,422 lenses): MEASURED EXTENT PREFERRED, flagged CIB-SENSITIVE**
(Δχ² k1−k3 = −14.4; the standard map's class is NEITHER FITS).

**Read it as: no tSZ detection, not a measured gas extent.** The stack is consistent with zero (null χ² 7.2/7, p 0.41), and
null stacks of random positions give the same class (below). What the data do say is an upper limit: hot gas at 0.22 keV and
Zhang's normalisation out to 3 R_vir is disfavoured at about 2.7σ using the empirical error.

| Tier, CIB-deprojected | Lenses | Δχ² k1−k3 | A(k=1) | A(k=1.8) | A(k=3) | Class |
|---|---|---|---|---|---|---|
| **central** | 206,422 | −14.4 | 0.39 ± 0.76 | 0.07 ± 0.37 | −0.07 ± 0.28 | MEASURED EXTENT |
| clean (no heavier neighbour, 3 Mpc) | 82,038 | −3.5 | 1.54 ± 1.38 | 0.63 ± 0.75 | 0.16 ± 0.53 | NOT DECIDED |
| iso3 (B21-like) | 31,747 | +1.1 | 2.39 ± 2.42 | 1.51 ± 1.16 | 0.97 ± 0.73 | NOT DECIDED |
| passive | 134,129 | −8.4 | 0.49 ± 0.79 | 0.10 ± 0.44 | −0.05 ± 0.36 | MEASURED EXTENT |
| star-forming | 72,293 | −2.8 | 1.70 ± 1.43 | 0.65 ± 0.76 | 0.30 ± 0.49 | NEITHER FITS |
| COMP > 0.8 | 78,607 | −9.6 | −3.50 ± 1.33 | −1.57 ± 0.75 | −1.26 ± 0.50 | NEITHER FITS |

Errors are jackknife. Standard map, central: NEITHER FITS, χ² 56 / 77 / 89, central deficit −7.9 ± 1.3 × 10⁻⁸, the dust signature.

Central compensated y × 10⁸, x = [0, .5, 1, 1.8, 3, 5, 8, 12): −0.01 ± 1.36, −0.71 ± 1.18, −1.78 ± 1.06, −1.46 ± 0.98,
−0.66 ± 0.65, 0.23 ± 0.54, 0.32 ± 0.36.

## The null test decides how to read it (post-freeze, no verdict weight)

Eight stacks on random positions, scored on the central tier's models:

| | mean | scatter | range |
|---|---|---|---|
| A(k=3) | +0.05 | **0.39** | −0.54 to +0.58 |
| A(k=1) | +0.24 | 1.20 | −0.91 to +2.37 |
| Δχ² k1−k3 | **−9.0** | 6.7 | −21.6 to −2.8 |

1. **The frozen verdict rule is not a detection test at this depth.** No-signal stacks give Δχ² −3 to −22, and 5 of 8 pass
   the −4 threshold outright, so −14.4 is what empty sky gives. The k = 1 model is close to zero, so "prefers k = 1" here
   mostly means "prefers nothing". The rule was inherited from GH3 and this was not foreseen when it was frozen.
2. **Jackknife errors are too small by about 1.4** (0.39 vs 0.28 on A(k=3); the scatter itself is from only 8 stacks, so
   good to about 25 %).
3. **With the empirical error:** A(k=3) = −0.07 ± 0.39, so A = 1 is 2.7σ away. A(k=1.8) ≈ 0.07 ± 0.5 (scaled, not measured), so 1.8σ, not
   excluded. A(k=1) = 0.39 ± 1.2 is consistent with both 1 and 0: **even the gas Zhang detects inside R_vir is not seen.**
4. **KiDS vs DESI:** A(k=3) 1.26 ± 0.76 (GH4, same 1.4 scaling assumed) against −0.07 ± 0.39 differs by about 1.6σ, so this
   is not a clean contradiction. The samples overlap partly on the sky.

## Systematics found

- **Negative stacks.** Gas cannot make negative y. Star-forming lenses reach −4.4 ± 1.4 × 10⁻⁸ (null p 0.004); passive
  lenses are null (p 0.61). This fits fixed-SED CIB deprojection over-subtracting around dusty lenses. So A from star-forming
  lenses is biased low, and passive is the tier to trust.
- **COMP > 0.8 negative.** Post-freeze splits: passive lenses in it are null (p 0.26); the 20k southern part is strongly
  negative at the centre (−11 ± 5, 2σ); the 58k northern part is null. Mechanism not established.
- **Sky split:** north Δχ² −16.2, south −3.4; neither stack differs from zero.
- **Isolation trend.** A(k=3) rises −0.07 → 0.16 → 0.97 from central to iso3, within errors. GH2's question is about isolated
  lenses, and that tier is too small to answer it.

## For the theory

- **Route E's gas is not excluded.** Its need (GH2: k* ≈ 1.8) is about 1.8σ from these data as hot gas at 0.22 keV, and tSZ
  measures pressure: cooler gas at 1–3 R_vir, which route E's mass need would accept, is invisible here.
- The lean toward extended gas from GH3/GH4 did **not** grow with more data, which counts against it.
- The route's condition stays open. A mass-weighted, temperature-independent probe is what would settle it (kSZ, FRB
  dispersion); tSZ cannot.
- κ = ½ FITTED; c_f EXTERNAL; cold dark energy is a gravitating field component, never a particle; not theory closed;
  nothing here says the data favour the framework.

## Checks (all PASS)

K1 projection −6.5e-5; K2 reproduces GH4's compensated Y exactly (87,560 lenses); K3 geometry 7e-11 px; K4 central
fraction 0.701 (Zhang 0.68); MUTATE null χ² 9.8/7, p 0.20.

## Disclosures

- The null-seed test, the `diag_*` tiers, `GH5_SEED` and the `null_fits` output were added after the freeze and after seeing
  the PRIMARY result. Null seed 303 was rerun with the same draws as MUTATE.
- An interim commit (5267dfe298) was pushed mid-run at the owner's request; this README replaces its note.
- CIGALE stellar masses are not Zhang's; a mass offset is absorbed only in free A.
- DESI fibre incompleteness leaks satellites into every tier.
- GH4's README said a decision needs a deeper measurement; these deeper lenses were already on disk.

## Files

`FROZEN_CRITERIA.md`, `gh5_select.py`, `gh5_tsz_desi.py`, `run_all.sh`, `run_diag.sh`, `run_nullseeds.sh`,
`gh5_*.out`, `gh5_results_*.json`. Lens list in `_external_data/gh5_work/` (not committed).

Run: `./run_all.sh` (~45 min, one thread, peak RSS 1.8 GB).

**Sources:** ACT DR6.02 NILC (https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/act_dr6.02_nilc_info.html);
DESI DR1 LSS catalogues and CIGALE VAC (https://data.desi.lbl.gov/doc/releases/dr1/); Zhang et al. 2024, A&A 690, A267.

**Forward note (GH6_frb_dm_cgm):** FRB dispersion measures cannot take over from tSZ yet. The power gate failed (S far below 3), so no DM was read.
