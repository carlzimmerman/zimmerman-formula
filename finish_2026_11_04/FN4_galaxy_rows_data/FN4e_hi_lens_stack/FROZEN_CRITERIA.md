# FN4e_hi_lens_stack: FROZEN CRITERIA (committed alone, before any script or number of this lane)

The council's CY6 ("lens on gas"), taken under an FN4 id, for the KiDS lensing row. κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. Footings never pooled: canonical a0 9.3603e-11, alt 1.1312e-10 m/s². **No download: the lens catalogues and the KiDS-1000 shear catalogue are on disk.**

## Question
Can a lensing a0 be measured from gas-dominated lenses, where stellar M/L hardly enters? The KiDS gap (about 0.09 dex, LE1; it stands on the rebuilt sample, FN4c) splits by colour (CW6), so colour-blind inputs can't fix both classes. Gas-rich lenses carry the smallest M/L lever.

## Inputs (on disk)
- ALFALFA α.100 (Haynes+18), `../_external_data/alfalfa_sdss/a100.code12.table2.190808.csv`; stellar masses from Durbala+20 (`durbala2020-table2.21-Sep-2020.fits.gz`).
- FASHI DR2 (`_external_data/fashi_dr2_2026_10_18/fashi_dr2.csv`), stellar masses only where its ALFALFA match gives them.
- KiDS-1000 SOM-gold shear catalogue (`../_external_data/kids_lensing_zsplit/`, 17.7 GB) and its n(z) tarball.
- DESI DR1 BGS (`../_external_data/desi_dr1_bgs/`, 5.19 GB) for spectroscopic neighbours where it overlaps.

## Stage 0: power (runs now)
- Lenses: HI detections with f_gas = 1.33 M_HI / (1.33 M_HI + M★) > 0.6, inside the KiDS-1000 source footprint (HEALPix nside 512 cells holding sources).
- Isolation, B21-style: no neighbour with M★ > 0.1 M★,lens (M_b for the HI lens) within 3 Mpc proper and |Δcz| < 1000 km/s, from DESI BGS and the HI catalogue itself; lenses outside BGS coverage are counted separately, not called isolated.
- Forecast σ(log a0) for the stack by Fisher, from each lens's law-predicted ΔΣ(R) (M_b = M★ + 1.33 M_HI, R 0.03–1 Mpc proper), the source counts behind it in the catalogue (Z_B > z_l + 0.2, as B21), σ_e per component from the catalogue's weighted ellipticity spread, Σ_crit from the sources' Z_B. In the deep regime ΔΣ ∝ √a0, so σ(log a0) = 2 σ(log A) for the stack amplitude A.
- **Line, frozen:** stage 1 runs only if σ(log a0) ≤ 0.05 dex on both footings (the footings differ by 0.082 dex). Otherwise the label is **STOP: NOT ENOUGH POWER**, with the count and σ reported.

## Stage 1 (only if stage 0 passes)
The stacked ΔΣ around the isolated gas-dominated lenses from the shear catalogue, random points subtracted, m-bias corrected, B21's conversion g_obs = 4 G ΔΣ, against the law on each footing with HI-based baryons and FN4b's external field where computable. Labels: **LAW FITS** (|Z| ≤ 2 on the amplitude), **LAW SHORT** (Z > 2), **LAW OVER** (Z < −2); and **FOOTING SEPARATED** only if the two footings differ by more than 3σ in the amplitude fit, else **FOOTING UNDECIDED**. Stage 1's own known answers and MUTATE (random lens positions must give a stack consistent with zero at 2σ) are part of this freeze.

## Known answers and checks (stage 0)
- **K1** the α.100 table has 31,502 rows (Haynes+18's count).
- **K2** the KiDS-1000 source footprint from the catalogue's own positions is within 5 % of 777 deg² (the KiDS-1000 effective area, PROVISIONAL from memory; reported if it misses, and the forecast then uses the measured area).
- **K3** the Fisher machinery recovers a planted case: 100 SIS lenses (σ_v 100 km/s) on a noise-only mock give a forecast S/N within 10 % of the analytic value.
- **MUTATE** (`FN4E_MUTATE=1`): lens RA rotated by 180°. The in-footprint count must fall by more than 50 %; exit 1.
- Rerun byte-identical JSON.

## Compute
One thread, `python3 -I`, `nice`. The shear catalogue is read with header-only metadata and raw chunked reads (FN4c's reader), RSS target under 1 GB.
