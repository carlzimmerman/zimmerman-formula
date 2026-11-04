# FN4f_mw_thick_share_apogee: FROZEN CRITERIA (committed alone, before any download, script or number of this lane)

Item 4 of the finish push, row group "Milky Way vertical force". κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. Footings never pooled: canonical a0 9.3603e-11, alt 1.1312e-10 m/s².

**Data, owner-approved 2026-11-04 (relayed by the lead with names and sizes):** `allStar-dr17-synspec_rev1.fits` (3,970,621,440 B, https://data.sdss.org/sas/dr17/apogee/spectro/aspcap/dr17/synspec_rev1/) and `apogee_astroNN-DR17.fits` (647,328,960 B, https://data.sdss.org/sas/dr17/env/APOGEE_ASTRO_NN/), into `../_external_data/apogee_dr17_2026_11/` with a FETCH_LOG. **APOGEE's selection function is not on disk and is not fetched.** The owner approved knowing a rigorous share needs it.

## Question
Does a measured thick-disc share put the law's Milky Way cells inside or outside what the data allow?

The cells on record and the local thick share of the stellar column each carries:
| Cells | Thick share | Law's result on record |
|---|---|---|
| X5's 175-cell box (LW1 forms A and R; part of KT13) | 0.2633 (McMillan17's thin share 0.736733, `x5_grid_canonical.out`) | form R: 1 canonical and 6 alt in-prior cells pass UR3's gate; form A INFEASIBLE |
| UX5 / KT13 boxes BV, BV2 | 0.12, 0.26, 0.35 | form Q (the plain law, every kernel): 0 cells pass at any share |
| KT18 / KT22 (filter, context only; CZ5 rules out every filter on Cassini) | 0.12, 0.16, 0.20 | alt passes at 0.20 only |

Star counts give 0.12 ± 0.04 (BH&G16) and a chemical split gives 0.264 (Lian+22), both PROVISIONAL web lookups. The definitions differ.

## Stage A: the share, without a selection function
- **Sample:** `EXTRATARG == 0` (main survey only), ASPCAPFLAG without STAR_BAD, SNR ≥ 70, 1.0 ≤ LOGG ≤ 3.5, 3900 ≤ TEFF ≤ 5500 K, finite FE_H and MG_FE with zero flags, −1.0 ≤ [Fe/H] ≤ +0.5. astroNN `weighted_dist` with fractional error ≤ 0.2. The astroNN rows are joined to allStar on APOGEE_ID, TELESCOPE and FIELD, all three equal.
- **Geometry:** R, z from (l, b, d), with R₀ 8.122 kpc (the record's) and z☉ 20.8 pc. Solar cylinder 7.122 ≤ R ≤ 9.122 kpc.
- **The split:** high-α lies above a line in [Mg/Fe] against [Fe/H]. The line comes from the trough of the [Mg/Fe] distribution (Gaussian KDE, bandwidth 0.02 dex, minimum between 0.05 and 0.25) in 0.1-dex [Fe/H] bins from −0.9 to +0.1, solar-cylinder stars with |z| ≤ 2.5 kpc, fitted as a straight line.
- **Estimator:** the selection is taken as chemistry-blind at fixed position, so the count ratio r(z) = N_hi/N_lo in |z| bins of 0.2 kpc over 0.2–2.5 kpc measures the density ratio of giants. Fit ln r = ln r₀ − κ|z| (weighted least squares, binomial errors), κ = 1/h_hi − 1/h_lo. With the thin scale height h_lo fixed (primary 0.30 kpc), h_hi = 1/(κ + 1/h_lo). The giant-number share is s_N = r₀ h_hi / (r₀ h_hi + h_lo). The mass share is s = s_N c / (s_N c + 1 − s_N), with c the ratio of stellar mass per selected giant, high-α to low-α. Primary c = 1.
- **Statistical error:** 300 bootstrap resamples of stars (fixed seed); σ_stat is their standard deviation.
- **Systematic band (frozen here, from having no selection function and no isochrones):** the envelope over these variants:
  - h_lo 0.25, 0.30, 0.35 kpc (the record's box);
  - c 0.7, 1.0, 1.4 (population-dependent giant counts and the colour cut, which favours metal-rich giants; a declared range, PROVISIONAL, not derived);
  - the split line, the trough fit and the trough ± 0.02 dex;
  - the |z| fit ranges 0.2–2.5 and 0.4–2.0 kpc;
  - distances × 0.9 and × 1.1.
  
  **Band B = [min over variants of (s − 2σ_stat), max over variants of (s + 2σ_stat)].**

## Stage B: placing the cells
- **If 0.2633 ∈ B:** form R's passing in-prior cells sit at an allowed share.
- **Otherwise:** form R is re-solved at the lower edge, the centre and the upper edge of B on X5's 175-cell box, both footings. This uses LW1's `cell()` Newton branch (Newton solve, then the round rule; the AQUAL branch is skipped), copied with attribution. The thin share is set to 1 − s. Cells are counted on UR3's gate (L1 v_c, L2a χ²_Kz, L2b K_z(R₀), L3 Ou) and LW1's in-prior tags.
- Forms A and Q are not re-solved: on record they pass nowhere at any share from 0.12 to 0.35.

## Labels (frozen), per footing
- **CELLS INSIDE:** at least one in-prior form R cell passes UR3's gate at a share inside B.
- **CELLS OUTSIDE:** no in-prior form R cell passes at any share inside B (the record's 0.2633 cells outside B, and no pass at B's edges or centre).
- **NOT MEASURABLE:** B is wider than 0.15, so it spans both the star-count and the chemical shares and cannot place the cells. Also NOT MEASURABLE if any known answer below fails.

Reported beside the label in every case: s with σ_stat, B, h_hi, the split line; and the fact that forms A and Q fail at every share on record.

## Known answers
- **KA1 planted sample:** two exponential populations (h_lo 0.30, h_hi 0.90 kpc, true share 0.20), a chemistry-blind selection in |z|, and Poisson counts at the real sample's size. The estimator recovers the share within 0.01 and h_hi within 0.05 kpc.
- **KA2 the bimodality:** the fitted trough at [Fe/H] −0.3 lies between [Mg/Fe] 0.10 and 0.22 (the APOGEE α-bimodality, PROVISIONAL).
- **KA3 the thick scale height:** the primary h_hi lies in 0.54–1.26 kpc, BH&G16's 0.9 ± 0.18 kpc at 2σ (PROVISIONAL, from memory).
- **KA4 join:** at least 99 % of allStar rows join to astroNN rows one to one.
- **Stage B check:** at share 0.2633, the copied Newton branch reproduces LW1's form R in-prior pass counts (1 canonical, 6 alt) exactly.
- **MUTATE** (`FN4F_MUTATE=1`): [Mg/Fe] is shuffled among the sample's stars. κ must collapse, so h_hi falls out of KA3's range; the label reads NOT MEASURABLE and the run exits 1.
- Rerun byte-identical JSON.

## Compute
One thread, `python3 -I`, `nice`. The FITS tables are read by column in raw chunks (header-only metadata, as FN4c's reader), RSS target under 1 GB. The data folder holds only the two approved files and the log. Scripts stay in this lane.

## What this lane cannot say
Without the selection function this is a chemistry-blind-selection estimate with a declared band, not Lian+22's or Mackereth+17's measurement. A chemical thick disc is not the geometric thick component of the record's model; they are compared as shares of the local stellar column. Form R has no field equation behind it (LW1).
