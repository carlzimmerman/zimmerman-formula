# FN4a_ic1613_cube_model: FROZEN CRITERIA (committed alone, before any script, download or number of this lane)

Item 4 of the finish push, row group IC 1613. This is the council's CW7 ("fit the cube, not the curve"), taken under an FN4 id. κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. Footings never pooled: canonical a0 9.3603e-11, alt 1.1312e-10 m/s².

**Gate: the owner's yes for the downloads below.** Nothing runs before that.

## Question
Is IC 1613's E −0.593 (Z −7.9; RT1) a property of the galaxy, or of a one-dimensional tilted-ring curve on a slow, lopsided, holed HI disc? The record's grades all rest on Oh+15's curve at a fixed i of 48°, or on an inclination alone (RT1, FD1, IN1, IN2, RF2, UX4). UX4 found the answer is "inclination or nothing". This lane fits the law to the HI cube itself, in data space, with the inclination free and with pressure support and non-circular motions allowed.

## Data
| Item | File | Source | Status |
|---|---|---|---|
| HI cube, natural weighting (primary) | `IC1613_NA_ICL001.FITS` | http://things.cv.nrao.edu/littlethings/ic1613/HI/ | download, owner's yes; size not obtained (host timed out 2026-11-04) |
| HI cube, robust 0.5 (resolution check) | `IC1613_R_ICL001.FITS` | same | same |
| moment 0, 1, 2 | `IC1613_NA_X0_P_R.FITS`, `IC1613_NA_XMOM1.FITS`, `IC1613_NA_XMOM2.FITS` | same | same |
| V and B images, calibration | `ic1613v.fits` (10,082,880 B), `ic1613b.fits` (10,082,880 B), `ic1613_ubvcalib.txt` (1,881 B) | https://science.nrao.edu/science/surveys/littlethings/data/ic1613/ | download, owner's yes |
| Oh+15 tables | Table 1 and 2, rotation curves | `../_external_data/little_things_oh2015/` | on disk |
| MUSE stellar values (i 36 ± 11 / 32 ± 11; σ, v profiles as printed) | TeX | `_external_data/ic1613_muse2024/` | on disk |
| Stellar mass, distance | SED M★ 2.88e7 (IN1, primary); 1.9e8 (X1 / LVD, bracket); D 0.73 Mpc (UNGC, Cepheid) | record | on disk |

Each download is logged with URL, time, bytes and sha256 in a `FETCH_LOG.md` in its own folder under `_external_data/fn4a_ic1613_2026_11/`.

## Models, all fitted to the same cube
- **M_free** (empirical benchmark): rotation free in rings one beam wide, dispersion σ(R) free, geometry (centre, v_sys, PA, i) free.
- **M_law**: rotation from the law's in-plane field of the baryon maps, no rotation freedom. Gas = 1.33 × the moment-0 map (primary-beam corrected). Stars = the V-band map with M/L_V from B−V (Bell & de Jong 2001), scaled so the total is the stated M★. Thin disc, scale height 0.2 kpc (0.1 and 0.3 as a bracket). Newtonian field by 2D FFT on the map grid. The law is the record's (RQ3 `candidates/law.py`), applied to the azimuthally averaged in-plane Newtonian field. Pressure support: v_rot² = v_c² + σ² d ln(Σ_gas σ²)/d ln R. Free: i (15–60°), PA, centre, v_sys, σ(R). Both footings.
- **M_law+nc**: M_law plus harmonic non-circular terms m = 1 and m = 2 (radial and tangential, each at most 20 km/s per ring).
- **M_N**: as M_law with ν ≡ 1 (Newtonian baryons). A control.
- The Local Group external field is left out: CZ1 Part D puts it at 3.4e-4 a0.

The χ² is taken on a beam-sampled grid (one voxel per beam area per independent channel) inside the HI mask, with the noise from emission-free channels. k = number of extra parameters of M_free over M_law (its ring velocities).

## Labels (frozen), per footing
- **LAW FITS THE CUBE**: χ²(M_law or M_law+nc) − χ²(M_free) ≤ χ²₀.₉₅(k), at a fitted i inside the independent geometric range 24.5–45.8° (RF2's 16th percentile of the optical isophote row to the 84th of the HI-footprint row).
- **LAW FITS ONLY BELOW 24.5°**: the same Δχ² line met only at i < 24.5°.
- **GENUINE OVER-PREDICTION**: the line fails at every i in 15–60°, with and without the non-circular terms.
- **NOT EVALUABLE**: a stage-0 check fails, or M_free itself has χ²_red > 1.5 on the beam grid.

The 24.5–45.8° range and the χ²₀.₉₅ line are fixed here and are not moved after a result.

## Known answers and checks
- **S0a** the HI mass from moment 0 is within 10 % of Oh+15's tabulated gas mass (divided by their helium factor), at the same distance.
- **S0b** a tilted-ring fit at Oh+15's geometry (i 48°, their PA) gives V(R_max = 2.71 kpc) within 2 km/s of their 16.9 km/s.
- **KA1** a mock cube built with the law (IC 1613's baryon maps, i 35°, σ 9 km/s, the cube's beam, channels and noise) is labelled LAW FITS THE CUBE, with i recovered within ±5°.
- **KA2** the same mock with rotation at 0.505 × the law's (the record's E −0.593 in acceleration) is labelled GENUINE OVER-PREDICTION.
- **KA3** M_N fits worse than M_free by more than χ²₀.₉₅(k) on the real cube (Newton must fail; LITTLE THINGS dwarfs are not Newtonian on their baryons).
- **MUTATE** (`FN4A_MUTATE=1`): the velocity axis is shuffled channel by channel. M_free must then fail its χ²_red line, so the label reads NOT EVALUABLE, exit 1.
- Rerun byte-identical JSON.

## Reported beside the label (no line)
The law's predicted m = 2 amplitude from the non-axisymmetric maps against M_law+nc's fitted amplitude; E_σ (IN1's stellar-σ tracer) at the cube's fitted inclination; the robust-cube result; the 1.9e8 M★ bracket.

## Compute
One thread, `python3 -I`, `nice`. The cube is cropped to the HI mask and binned to about a third of a beam; RSS target under 1 GB. No 3DBarolo (a pip install would be a download); the ring model is written here and checked by KA1–KA2.

## What this lane cannot say
One galaxy. A pass means the law is consistent with IC 1613's cube at an allowed inclination. It does not mean the law is right. A fail strengthens row 6; it does not exclude the law.
