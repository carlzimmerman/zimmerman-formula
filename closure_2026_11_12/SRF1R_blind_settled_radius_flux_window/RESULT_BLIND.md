# SRF1R RESULT_BLIND: the settled-radius family with the forest graded at flux level

**As frozen: NO VERDICT / NO VERDICT (canonical / alt).** Known answer (d) fails. At f = 6, z 2.2, the linear-response
mean-flux retune is |eps| = 0.0135 / 0.0122, above the frozen line of 0.01 for f <= 6. Every other known answer passes
(a, b, c, e, f) and both mutations bite. The numbers below are therefore **ungraded**.

**Reading, ungraded (not the frozen label): the window would open at flux level, [1.004, 3.16] / [1.050, 3.21], with
f = 1 OUTSIDE.**
- f = 1 is outside because G4 fails there (SRH1's grade, +2.003 / +2.04 sigma). The forest itself passes f = 1 at flux
  level by a factor of about 500 (Delta chi^2_G 0.008 / 0.005).
- No computed bracket moves f = 1 across the gate or closes the window. The bracket set is incomplete: B1, B4 to B7, B9
  and B10 were not run, and the brackets that were run (B0, B2, B3, B8) reach only f = 3.
- **This would be a hit on a post hoc family, not a pass of form B.**
- The edge f_max sits where (d) starts to strain. f = 4 and above rest on the z 2.2 bin alone (AMENDMENT A3). The
  twelve-bin values are estimates through the matter-level ratio (A3).

TEST lane: it adopts nothing, relabels nothing (SRH1, FZS1 and SRH1R keep their labels) and registers nothing. The two
footings are graded separately and never pooled. Cold dark energy is a gravitating field component; no particle is
added. kappa = 1/2 is FITTED. **The settled-radius family is post hoc**: it was chosen after the forest failed at matter
level. Nothing here says the data favour the framework.

Commits: READING cc3d45432d, AMENDMENT A1 696d184fbf, A2 23c3b8956a, A3 f845b9632f, each committed alone before any flux
statistic. Nothing of SRF1 was opened before this file.

## What was computed

- **The family.** SRH1's settled layout is unchanged. The law's halo lies inside R_set = f R_fold (FLD1). Cold dark
  energy has the cold reference layout outside R_set, with the enclosed mass matched at R_set. FRZ1's halo model is
  inherited.
- **The construction.**
  - A 20 Mpc/h, 384^3 lognormal background with light haloes (below 10^10.8 Msun/h, Poisson, reference profiles).
  - Heavy haloes inserted one at a time, with importance weights, at 16 to 32 per 0.1 dex bin.
  - Why insertion: SRH1's change is carried by haloes above about 2e12 Msun/h (a design check before the freeze), and a
    20 Mpc/h box holds 0.2 haloes above 1e13 at z 2.2.
- **Gas physics:** FRZ3R's adopted values. FGPA with T0 1e4 K, gamma 1.5, pressure smoothing 79 comoving kpc, thermal
  broadening in 16 log-b classes, mean flux matched to Becker 2013 (PROVISIONAL inputs).
- **Graded statistic.** Delta chi^2_G = (flux Delta chi^2 of the construction) x K, with K = SRH1's matter Delta chi^2
  / the construction's matter Delta chi^2. Gate 4, 755 DESI DR1 P1D points.
- **Per A3,** flux was computed at the anchor bins z 2.2, 3.0 and 4.4 only. Twelve-bin values = anchor block x (matter
  twelve-bin / matter anchor block); for f = 4, 6 and inf, the z 2.2 bin x (matter twelve-bin / z 2.2 bin).

## Table per f (ungraded; footings separate)

Columns: SRH1 = the record's matter Delta chi^2; real = this construction's matter Delta chi^2; K; flux = this
construction's flux Delta chi^2 (twelve-bin estimate); soft = flux / matter, same fields; G = graded value; gate.

| f | canonical SRH1 / real / K | flux | soft | **G** | alt SRH1 / real / K | flux | soft | **G** |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 / 0 / - | 0 | - | 0 P | 0 / 0 / - | 0 | - | 0 P |
| 0.30 | 0.001 / 0.001 / 1.33 | 0.0000 | 2.9e-3 | 0.0000 P | 0.001 / 0.001 / 1.33 | 0.0000 | 5.3e-3 | 0.0000 P |
| 0.50 | 0.189 / 0.147 / 1.29 | 0.0002 | 1.7e-3 | 0.0003 P | 0.185 / 0.144 / 1.29 | 0.0002 | 1.6e-3 | 0.0003 P |
| 0.60 | 0.923 / 0.705 / 1.31 | 0.0008 | 1.1e-3 | 0.0010 P | 0.903 / 0.691 / 1.31 | 0.0006 | 9.4e-4 | 0.0008 P |
| 0.70 | 3.173 / 2.384 / 1.33 | 0.0012 | 5.1e-4 | 0.0016 P | 3.085 / 2.319 / 1.33 | 0.0011 | 4.6e-4 | 0.0014 P |
| 0.80 | 8.578 / 6.338 / 1.35 | 0.0018 | 2.9e-4 | 0.0025 P | 8.271 / 6.112 / 1.35 | 0.0014 | 2.3e-4 | 0.0019 P |
| 0.90 | 19.48 / 14.14 / 1.38 | 0.0029 | 2.1e-4 | 0.0040 P | 18.61 / 13.51 / 1.38 | 0.0023 | 1.7e-4 | 0.0031 P |
| **1.00** | **38.74 / 27.63 / 1.40** | **0.0057** | **2.1e-4** | **0.0081 P** | **36.66 / 26.11 / 1.40** | **0.0036** | **1.4e-4** | **0.0051 P** |
| 1.10 | 69.53 / 48.67 / 1.43 | 0.0100 | 2.1e-4 | 0.014 P | 65.15 / 45.49 / 1.43 | 0.0061 | 1.4e-4 | 0.009 P |
| 1.25 | 134.0 / 90.44 / 1.48 | 0.0208 | 2.3e-4 | 0.031 P | 102.9 / 68.62 / 1.50 | 0.0098 | 1.4e-4 | 0.015 P |
| 1.40 | 218.7 / 140.7 / 1.55 | 0.0353 | 2.5e-4 | 0.055 P | 149.6 / 95.28 / 1.57 | 0.0150 | 1.6e-4 | 0.024 P |
| 1.60 | 334.5 / 202.3 / 1.65 | 0.0523 | 2.6e-4 | 0.086 P | 213.2 / 128.4 / 1.66 | 0.0284 | 2.2e-4 | 0.047 P |
| 1.80 | 409.3 / 239.3 / 1.71 | 0.100 | 4.2e-4 | 0.171 P | 250.8 / 147.3 / 1.70 | 0.064 | 4.3e-4 | 0.108 P |
| 2.00 | 452.1 / 260.7 / 1.73 | 0.192 | 7.4e-4 | 0.333 P | 275.1 / 160.4 / 1.72 | 0.138 | 8.6e-4 | 0.236 P |
| 2.50 | 542.1 / 311.1 / 1.74 | 0.674 | 2.2e-3 | 1.17 P | 349.7 / 204.6 / 1.71 | 0.596 | 2.9e-3 | 1.02 P |
| 3.00 | 679.7 / 391.7 / 1.74 | 1.673 | 4.3e-3 | 2.90 P | 480.5 / 283.6 / 1.70 | 1.539 | 5.4e-3 | 2.61 P |
| 4.00 (z 2.2 est.) | 1192 / 684.9 / 1.74 | 12.44 | 1.8e-2 | 21.7 F | 1009 / 589.9 / 1.71 | 11.76 | 2.0e-2 | 20.1 F |
| 6.00 (z 2.2 est.) | 3393 / 1801 / 1.88 | 119.6 | 6.6e-2 | 225 F | 3359 / 1795 / 1.87 | 121.8 | 6.8e-2 | 228 F |
| inf (z 2.2 est.) | 9916 / 4500 / 2.20 | 773 | 0.17 | 1704 F | 9009 / 4307 / 2.09 | 732 | 0.17 | 1531 F |

SRH1's other grid points (0.35, 0.40, 0.45, 0.55, 0.65, 0.75; matter Delta chi^2 0.005 to 5.35) were not computed at
flux level. SRH1's 1.50 (matter 279.7 / not on this grid) lies between computed neighbours that pass.

| edge (ungraded) | canonical | alt |
|---|---|---|
| flux-level forest edge f_max (interpolated between 3.0 and 4.0, log Delta chi^2) | **3.16** | **3.21** |
| SRH1's matter-level edge | 0.722 | 0.725 |
| lensing G4 lower edge (SRH1) | 1.004 | 1.050 |
| window (G1 flux, G2, G3, G4) | [1.004, 3.16] | [1.050, 3.21] |
| window read with SRH1R (lensing cannot see f; lower edge G2's 0.391) | [0.391, 3.16] | [0.391, 3.21] |

**Per bin.** At f = 1 the z 2.2 bin carries almost everything: own-block flux Delta chi^2 0.0022 / 0.0014 at z 2.2,
1e-5 at z 3.0, 5e-10 at z 4.4. At f = 1, z 2.2, R_F - 1 is about 1e-4 at k_v 0.005 to 0.03 s/km, against matter-level
changes of 1 to 9 % at k 3 to 10 h/Mpc.

**Which haloes.** At f = 1 the flux change comes 24 / 30 % from haloes below 1e12, 71 / 65 % from 1e12 to 1e13 and 5 % from
above 1e13 (z 2.2, |Delta P| over k_v < 0.03 s/km).

**What softens it.** Saturation: mutation M1 (F = 1 - A tau) multiplies the z 2.2 flux Delta chi^2 by about 3e10. The
change lies inside R_set, deep in saturated gas (section 11 of READING). The softening is 1e-4 to 3e-4 for f <= 2; it rises
to 4e-3 at f = 3, 2e-2 at 4 and 0.17 at inf, as R_set reaches lower-density gas. That is where the edge comes from.

## Known answers

| | canonical | alt | line | verdict |
|---|---|---|---|---|
| (a) f = 0: R_F = 1 exactly in every part; Delta chi^2 0; DESI md5 | yes / 0 / ok | yes / 0 / ok | exact | PASS |
| (b) f = inf matter (unscaled, twelve bins) vs FRZ3R reading T | 4500 vs 5035 | 4307 vs 4377 | x / 2 | PASS |
| (b) f = inf flux (estimate, A3) vs reading T | 773 vs 363 (x 2.1) | 732 vs 425 (x 1.7) | x / 3 | PASS |
| (b) softening at inf vs reading T's | 0.172 vs 0.072 | 0.170 vs 0.097 | reported | - |
| (c0) SRH1's path recomputed (0 to inf, 18 points) | every value equal to 0.001, incl. 38.741 | incl. 36.658 | 0.01 | PASS |
| (c1) matter real / SRH1 at f = 1 | 0.713 | 0.712 | [0.25, 1.5] | PASS |
| (c2) K(f) / K(1), f 0.7 to 6 | 0.95 to 1.34 | 0.95 to 1.33 | [0.5, 2] | PASS |
| (d) mean flux of B | 1.7e-8 | 8.9e-9 | 1e-4 | pass |
| (d) max primary abs(eps), f <= 6 | **0.0135 at f = 6** (0.0013 at f = 4, 2.4e-4 at f = 3) | **0.0122 at f = 6** | 0.01 | **FAIL** |
| (e) seed scatter, z 2.2, seeds 0, 1; S / E at f = 1, 2, 3 | 0.11, 0.08, 0.08 | 0.14, 0.09, 0.08 | <= 1/3 | PASS |
| (f) confinement (z 3, f 1), mass at r_ta | 9.2e-7; 5.8e-16 | 9.2e-7; 6.1e-16 | 1e-6; 1e-9 | PASS |

Notes on these known answers:
- **(d) as frozen also read the mutation M1 parts.** There |eps| is 0.12 / 0.10, because a linear flux has no
  saturation. The primary alone already fails at f = 6, so the frozen reading does not depend on that ambiguity.
- **(d) is not about the edge.** The retune stays below 0.0014 at every f <= 4. My post hoc judgement: a second-order
  error of eps^2 (about 2e-4 relative) cannot move f = 6's Delta chi^2_G of about 225 across 4. The edge between 3 and 4
  is unaffected. That is a judgement, and the label stays NO VERDICT.
- **The carry at f = 1** ((R_paint - 1) / (R_cold - 1) at k 3 / 5 / 10): 0.58 / 0.76 / 0.96 at z 2.2 and 0.48 / 0.59 /
  0.84 at z 3.0. It is near 1 where the projection weighs most. K is about 1.4.
- **Haloes below 10^10.8 change nothing in this build.** In the halo model they carry 2 % of SRH1's f = 1 matter level
  (38.0 / 38.7 canonical).

## Mutations (`srf1r_grade_<foot>_MUTATE.json`)

- **M1, saturation removed.** z 2.2 flux Delta chi^2 0.0022 -> 6.0e7 at f = 1 and 0.046 -> 1.0e8 at f = 2 (canonical;
  alt similar): **bites**, and moves up, toward and far past the matter level. The linear flux goes negative in halo
  cores, so its size means nothing. Its direction is the point: saturation is what hides the change.
- **M2, R_set doubled at f = 1.** 0.0022 -> 0.046 (x 21) / 0.0014 -> 0.033 (x 24): **bites**.

## Brackets (z 2.2 ratio x the primary G; f 0.70 to 3.00; A3)

| bracket | canonical G at f 1 / 2 / 3 | alt G at f 1 / 2 / 3 | crosses? |
|---|---|---|---|
| B0 carry convention (unscaled flux) | 0.006 / 0.19 / 1.67 | 0.004 / 0.14 / 1.54 | no |
| B2 lambda_P x 2 | 0.012 / 0.10 / 0.67 | 0.011 / 0.08 / 0.64 | no |
| B3 lambda_P = 100 proper kpc | 0.000 / 0.03 / 0.65 | 0.000 / 0.02 / 0.62 | no |
| B8 clustered placement | 0.005 / 0.14 / 1.07 | 0.004 / 0.12 / 1.04 | no |
| B1, B4, B5, B6, B7, B9, B10 | not computed (time) | not computed | - |

Reading the brackets:
- No computed bracket puts f = 1 over the gate, and none closes the window. Their own edges lie above 3, the end of
  their f list.
- **FRAGILE is not printed, but the bracket set is incomplete.** Not run: half smoothing, gamma 1.2 and 1.6, the
  mean-flux brackets, resolution, and the temperature cap.
- Larger smoothing lowers the high-f values.

## What is left out

- Hydrodynamics, shock heating and hot halo gas: the FGPA's hot, dense cores carry the response here, and the
  temperature-cap bracket was not run. Also left out: collisional ionisation, self-shielding and damped systems,
  peculiar velocities and infall, UV and temperature fluctuations, metals, continuum.
- Halo positions are uncorrelated with the IGM in the primary (B8 only). Heavy haloes are isolated from each other.
- The heavy haloes' own reference contribution to the denominator was dropped (A1).
- The light haloes' change and the two-halo part of the change (3 %) are not included.
- The nine non-anchor DESI bins were not computed (A3). The twelve-bin numbers are estimates.
- One seed at z 3.0 and 4.4. The box has no power below its fundamental.
- FRZ1's halo model and SRH1's layout are taken as they are (PROVISIONAL).
- Lensing G4, rotation curves G2 and G3: SRH1's committed outputs, not re-graded.

## Disclosures

- **Pre-freeze design checks:** halo-model matter level and timing only, disclosed in READING section 1.
- **Three compute amendments**, each committed alone before any flux statistic. The first part took 20 minutes on a
  shared machine.
- **One part deadlocked** when a worker pool was forked after FFT threads (z 4.4 alt). It was rerun one footing per
  process; no number changed by that.
- **Seen before this file:** the FRZ3R folder's file names (READING section 0). Nothing of SRF1.

## Files

- `srf1r_tables.py`, `srf1r_cosmo.py`: stage 0. Tables are regenerated (216 MB, deleted after the run); `tables/cosmo.json`
  is kept.
- `srf1r_flux.py`: stage 1. Part files are in `parts/`.
- Queues: `run_all.sh`, `run_a3.sh`, `run_a3b.sh`.
- `srf1r_grade.py` -> `srf1r_grade_<foot>.json` / `.out` / `_MUTATE.json`.
- The console logs stay local.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
