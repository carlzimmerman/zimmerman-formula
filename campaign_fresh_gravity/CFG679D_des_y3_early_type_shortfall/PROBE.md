# CFG679D probe: DES Y3 public catalogues, layout and byte budget (no lensing number computed)

Lane purpose: does the KiDS-1000 inner-halo shortfall of isolated early types (CFG529 / CFG531, ε ≈ +0.5 at 52–98 kpc) replicate
in DES Y3? This file records what the probe found before any criteria or measurement. Owner approved the DES Y3 download on
2026-10-12; budget ≤ 30 GB. κ = ½ is fitted; cold energy's mass still required; not theory closed.

Lane id: the requested directory name `CFG679_...` collides with the committed `CFG679_mechanism_contract` (same block, 8b77a75fc /
41ad7a730 / 11629ff57). This directory uses `CFG679D` until the block owner assigns a number.

## Files and layout (from `cfg679_probe.py` / `cfg679_probe.out`, HDF5 metadata by HTTP range requests)

| file | size | what this lane needs | layout found |
|---|---|---|---|
| `stellar_mass/DESY3_stellar_mass_catalog.hdf5` | 2.85 GB | ra, dec, z, mstar (lenses and isolation pool) | 10 contiguous little-endian 8-byte columns, 35,653,240 rows; also coadd_obj_id, zsam, msam, nn_weight, zbin, mbin. **No colour, no magnitude.** Rows are ordered by (zbin, mbin); z starts at 0.20 (zbin 1 = 0.20–0.40, zbin 2 = 0.40–0.55 seen); log M* bins start near 9.56 |
| `y3kp_cats/DESY3_metacal_v03-004.h5` | 312 GB | unsheared ra, dec, e_1, e_2, weight (+ R11, R22 on a subsample) | `catalog/{unsheared, sheared_1p, sheared_1m, sheared_2p, sheared_2m}/<col>`; every column probed is 399,263,026 rows, 8-byte float, chunks of 1,000,000 rows, **uncompressed** (one chunk = 8 MB = one range request) |
| `y3kp_cats/DESY3_indexcat.h5` | 27.3 GB | `index/select_bin1..4` (fiducial selection + tomographic bin) | not reached (probe stopped, see throughput) |
| `y3kp_cats/DESY3_GOLD_2_2.1.h5` | 62.6 GB | g, r, i magnitudes of the lenses (r < 20 cut, colour split) | `catalog/gold/...`, `masks`; columns not reached |
| `datavectors/2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits` | 28 MB | source n(z), 4 bins | downloaded (sha256 in `_external_data/cfg679_des/`); mean z of bins 1–4: 0.336, 0.521, 0.741, 0.936 |

## Byte budget (full footprint, the only plan with power to return the KiDS-SPECIFIC label)

| item | bytes |
|---|---|
| stellar-mass ra, dec, z, mstar | 1.14 GB |
| metacal unsheared ra, dec, e_1, e_2, weight (5 × 3.19 GB) | 16.0 GB |
| index select_bin1..4 (≈100 M int64) | ≤ 0.8 GB |
| R11, R22 on 20 random chunks | 0.32 GB |
| GOLD g, r, i for the colour split (3.2 GB each if 8-byte, 1.6 GB if 4-byte) | 4.8–9.6 GB |
| GOLD coadd_object_id, only if GOLD rows are not aligned with metacal rows | +3.2 GB |
| **total** | **23–31 GB** (≤ 30 GB only if GOLD is row-aligned or 4-byte) |

Dropping `weight` (unit weights) saves 3.2 GB. A half-footprint subset halves the source part.

Expected power (scaling from the KiDS f30 early-type K-in error, 0.19 with CFG531's estimator, by area 4143 vs ~1000 deg²
and source density 5.6 vs ~6.2 arcmin⁻²; rough, before any DES number): σ(ε, early, K-in) ≈ 0.10–0.12 full footprint, ≈ 0.15
half footprint. With KiDS at ε ≈ 0.54 ± 0.19, a half-footprint DES cannot reach the frozen "KiDS-SPECIFIC" bar (needs ε_DES within
1σ of 0 AND ≥ 2σ_comb below KiDS, i.e. ε_DES ≲ 0.0); only the full footprint can.

## Throughput (the blocking finding)

Measured 2026-10-12/13 from this machine, `desdr-server.ncsa.illinois.edu`:
- Single request, small file region: 0.6–1.3 MB/s when the server responds.
- Large files (metacal, GOLD, sompz): time-to-first-byte from 0.5 s to 84 s; several 1–32 MB range requests returned **0 bytes in
  110–300 s**; a HEAD request on the metacal file hung > 30 min once.
- Parallel streams do not add: 3 × 32 MB in parallel gave 0.30 + 0.15 + 0 MB/s.
- `cfg679_download.py sm` (stellar-mass columns, 8 MB pieces, 2 threads): 15 pieces (120 MB) in the first 6 min, then **no piece for
  10+ min** (stall); session average ≈ 0.1–0.2 MB/s.
- HDF5 metadata look-ups on the metacal file take ~4 min per dataset (random small reads).

At the sustained 0.1–0.6 MB/s observed, the 23–31 GB plan needs **~12–85 hours** of downloading; at the 2.5 MB/s noted on 10-09 it
would have been ~3 h. The full plan is within the byte budget but not within a working session at the current server rate.
