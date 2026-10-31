# RF2_ic1613_inclination_footing: assumption ledger (committed with FROZEN_CRITERIA.md, before any script or number)

Classes as X5. PROVISIONAL = not read from the primary paper.

| ingredient | class | source | note |
|---|---|---|---|
| Law ν = ½ + √(¼ + 1/y), a₀ 9.3603e-11 / 1.1312e-10 | FRAMEWORK-NATIVE (κ fitted); kernel as IN1 | IN1 | |
| σ_los 10.8, r_h 1439.78 pc | SURVEY-CALIBRATION | X1 / LVD (Kirby+14, Higgs+21) | |
| v_rot,★ 13 km/s | LITERATURE-INPUT | UNGC vAmp, FD1, IN1 | |
| HI V_rot 16.9 at 2.71 kpc, i 48 | SURVEY-CALIBRATION (Oh+15 Table 2, tex on disk) | RT1, `_external_data/little_things_oh2015/src/ms.tex` | |
| M★ 2.88e7, M_gas 5.93e7 | LITERATURE-INPUT (Oh+15 SED); SED M/L | same | largest lever; X1's 1.9e8 reported |
| Disc estimator q_σ 0.4–0.8 | modelling choice, IN1 | IN1 | |
| s 0.0792, 0.075 | record (HO3, RT1) | IN1 | not independently re-derived |
| Taibi+24 36 ± 11, 32 ± 11, ε 0.20 ± 0.05, PA 90 ± 1, PA_HI 72 ± 2 | LITERATURE-INPUT, read from TeX on disk | `_external_data/ic1613_muse2024/src/ic1613_accepted.tex`, tarball sha256 in IN2 | 36 uses Read+16's asymmetric-drift form; not a mass model |
| ε 0.20 ± 0.05, PA 90.49 ± 1.02, r_h 7.57′ | SURVEY-CALIBRATION (star counts) | LVD csv, Higgs+21 | same origin as Taibi's row, one row |
| Lake & Skillman 1989 38 ± 5 | LITERATURE-INPUT, **PROVISIONAL, second-hand** | via Taibi+24 | |
| Read+16 39 ± 2, 15° | **ΛCDM-PROCESSED** (mass-model fit) | via Taibi+24 | BRACKET |
| Collins & Read 2022 ~20° | LITERATURE-INPUT, **circular** (BTFR imposed) | via Taibi+24 | BRACKET |
| Oh+15 PA 73.7, i 48 ± 0 | SURVEY-CALIBRATION (tilted ring, i fixed) | ms.tex Table 1 | |
| Oh+15 Fig. A.55 panel (a) | RAW-rendered (published figure raster; intensities lost) | `deepseek_push/G114_data/oh2015/HI_Spitzer_data_PV_ic1613.pdf` | no FITS on disk |
| e_int 0.10; q₀ 0–0.6 | declared, PROVISIONAL, unsourced on disk | this lane | always shown as a range |
| Flat prior in cos i | declared, as Taibi+24 | | |
| Truncated normal for quoted ± | declared. `INDEPENDENT_PUSH_2026-10-28` notes published errors do not validate a Gaussian angle posterior | | |

Not done: mass model, new data, moment-0 FITS (needs the owner's OK). IN1's falsifier is not changed.
