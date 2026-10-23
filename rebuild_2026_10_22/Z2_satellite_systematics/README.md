# Z2_satellite_systematics: how much of the dwarf-satellite excess is real?

## Verdict: CRISP FINDING

1. **The excess is real.** No pre-declared systematic removes it. In every clean subset, every flavor stays above its
   prediction. Tides are not implicated for any flavor.
2. **T1's host-field trend is a luminosity proxy.** Faint ultra-faints are found only near the Milky Way. With M_V in the
   regression, the slope at ε = 0 falls from +0.76 ± 0.26 to +0.02 ± 0.20 (alt +0.84 → +0.02). M_V's own slope is
   +0.27 ± 0.05 dex per mag.
3. **What is left of the trend tests the external-field effect (EFE).** At fixed M_V the data are flat in host field:
   −0.05 ± 0.19 dex per dex. v3 static predicts −0.55. AQUAL with its EFE predicts −0.76.

κ = ½ is FITTED. Footings are canonical / alt (9.3603e-11 / 1.1312e-10 m/s²), never pooled. The extra mass is cold
energy, not a particle. Not "theory closed". Nothing here says the data favour the framework.

**Checks: 8/8 PASS.** `--mutate` replaces the data by a pure tidal artefact. It fails K1–K3 (5/8, exit 1), fires TIDES
IMPLICATED for every flavor (partial z +3 to +13), and turns V3S and MOND NOT ROBUST (alt V3S: TOO FEW).

## Clean-subset excess (frozen lines; bootstrap median of log g_obs/g_pred ± sd)

| flavor | all systems | clean (C1–C4) | f_sys (68 %) | class | C2–C4 only (N 19) | W in clean |
|---|---|---|---|---|---|---|
| v3 static (V3S), canonical | +1.332 ± 0.148 | +0.900 ± 0.213 (N 6) | 0.32 [0.14, 0.49] | **ROBUST** | +1.169 ± 0.146 | +0.53 ± 0.20 |
| v3 static (V3S), alt | +1.302 ± 0.146 | +0.787 ± 0.235 (N 5) | 0.40 [0.20, 0.55] | TOO FEW (N < 6) | +1.162 ± 0.150 | +0.44 ± 0.21 |
| v3 dust-free (V3D, U1 B0), canonical | +2.006 ± 0.113 | +1.925 ± 0.239 (N 2) | 0.04 [−0.05, 0.15] | TOO FEW | **+1.880 ± 0.097, ROBUST** | +1.55 ± 0.24 |
| v3 dust-free (V3D), alt | +1.993 ± 0.110 | +1.928 ± 0.227 (N 2) | 0.03 [−0.06, 0.14] | TOO FEW | **+1.885 ± 0.100, ROBUST** | +1.55 ± 0.23 |
| AQUAL + EFE, L★ = 0 (MOND), canonical | +1.137 ± 0.151 | +0.693 ± 0.150 (N 7) | 0.39 [0.24, 0.53] | **ROBUST** | +0.952 ± 0.154 | +0.36 ± 0.15 |
| AQUAL + EFE (MOND), alt | +1.078 ± 0.152 | +0.711 ± 0.157 (N 8) | 0.34 [0.15, 0.49] | **ROBUST** | +0.917 ± 0.159 | +0.39 ± 0.15 |
| isolated AQUAL (ISO), canonical | +0.557 ± 0.099 | +0.465 ± 0.110 (N 14) | 0.16 [−0.01, 0.32] | **ROBUST** | +0.450 ± 0.094 | +0.24 ± 0.12 |
| isolated AQUAL (ISO), alt | +0.498 ± 0.099 | +0.424 ± 0.108 (N 14) | 0.15 [−0.05, 0.33] | **ROBUST** | +0.409 ± 0.097 | +0.19 ± 0.12 |

- **Clean (frozen):**
  - C1: r₁₂/r_t < 0.5 at a PM-based pericentre, with the flavor's own mass, in S1's own MW field;
  - C2: ellipticity < 0.5;
  - C3: no velocity gradient;
  - C4: N★ ≥ 10.
- **The v3-static clean set** is Eridanus II, Leo IV, Leo V, Pegasus III, Pegasus IV and Leo T. M31 satellites have no
  PMs on disk, so they cannot pass C1.
- **STRICT** (tidally safe even with baryons only) leaves only Eridanus II and Leo V. That is TOO FEW for every flavor.
- **95 % intervals of f_sys:** V3S [−0.00, 0.65] / [−0.00, 0.72]; MOND [0.10, 0.69] / [−0.00, 0.64];
  ISO [−0.27, 0.50] / [−0.39, 0.52].
- **The f_sys of V3S and MOND is mostly host-field selection (A1, post-result).** C1 keeps distant satellites. The full
  sample's own x_e regression predicts the clean set's drop:
  - V3S: +0.39 predicted vs +0.35 observed. That leaves −0.04 ± 0.19 for the systematics, or +0.30 ± 0.19 with M_V also
    controlled.
  - MOND: +0.06 ± 0.17 / +0.35 ± 0.19 left.
  - V3D: −0.10 ± 0.16 / −0.03 ± 0.24 left. ISO: +0.04 ± 0.11 / +0.07 ± 0.11 left.
  - **So no flavor shows a systematics share that differs from zero by 2 sd.**
- **Robustness of the clean set (A1).** The v3-static clean Δ is stable at +0.89 to +0.92 under the E_lo / E_hi host and
  the 84th-percentile orbit. N drops to 4 under E_hi and under q₈₄.

## Per-test results (canonical; alt is the same class everywhere; full table in `z2_satellite_systematics.out`)

| test | v3 static | v3 dust-free | AQUAL + EFE | isolated AQUAL |
|---|---|---|---|---|
| (a) partial slope on host tidal density at pericentre, internal density controlled | +0.16 ± 0.15 (z +1.0) | −0.05 ± 0.11 (−0.4) | +0.18 ± 0.15 (+1.2) | −0.09 ± 0.09 (−0.9) |
| (a) PM satellites exposed (q ≥ 1) / safe (q < 0.5), of 33 | 6 / 12 | **17 / 3** | 6 / 13 | 2 / 27 |
| (b) ellipticity < 0.5 minus ≥ 0.5 | −0.16 ± 0.42 | −0.02 ± 0.36 | −0.16 ± 0.42 | +0.04 ± 0.28 |
| (c) N★ ≥ 10 minus < 10 | −0.40 ± 0.26 | −0.35 ± 0.20 | −0.44 ± 0.28 | −0.24 ± 0.18 |
| (d) UFD minus classical-luminosity (38 vs 7) | +0.96 ± 0.31 | +0.60 ± 0.28 | +0.78 ± 0.30 | +0.44 ± 0.33 |
| (e) slope on log x_e (all 45) | +1.10 ± 0.21 | +0.41 ± 0.19 | +1.16 ± 0.19 | +0.28 ± 0.17 |

- **(a) Tides:** not implicated for any flavor on either footing.
  - Under v3's dust-free mass (stars only), half the PM satellites (17 / 33) have r₁₂ beyond the King radius at
    pericentre. Their excess does not depend on q.
- **(b) Velocity gradients:** 6 systems have ≥ 10 Walker 2023 members (Boötes I, Crater II, Hydrus I, Reticulum II,
  Tucana II, Ursa Major II). None is flagged; the closest is Hydrus I (p = 0.031).
  - The test has power: an injected 10 km/s/kpc gradient on Crater II's 78 members is recovered at p = 4e-29, and the
    false-flag rate is 1.0 %.
- **(c) Member counts:** this is the largest single systematic. Systems with fewer than 10 members carry +0.24 to
  +0.44 dex more excess (1.4–1.7 sd). Its per-test fraction is 0.06–0.18.
- **(d) Luminosity:** the classical-luminosity systems in this sample sit near the isolated law: ISO +0.17 ± 0.31,
  V3S +0.48 ± 0.27. They are 5 M31 dSphs, Crater II and Leo T.

## Task 1: why T1 sees a trend and CFG838/839 did not

**Frozen factor grid** (`z2_satellite_systematics.out`): T1's cell is the 45 satellites of E3, the v3 residual at
ε = 0, log x_e and OLS. Its slope is +0.761 ± 0.257 (z 3.0, Spearman p 0.007).

| single change toward CFG838 | slope (canonical) | removes the trend? |
|---|---|---|
| **sample → CFG838's 24 satellites** | −0.19 ± 0.27 (ρ −0.00) | **yes** |
| **variable → CFG838's tidal parameter T (today)** | +0.02 ± 0.15 | **yes** |
| **variable → T at the PM pericentre** | −0.31 ± 0.15 | **yes (wrong sign for tides)** |
| variable → host distance (sign flipped) | +0.83 ± 0.25 | no: distance and field are the same signal |
| statistic → Spearman | ρ +0.40, p 0.007 | no |
| residual → Newton / isolated AQUAL | +0.41 ± 0.19 / +0.28 ± 0.17 | weakened, not removed |

- **The two samples barely overlap.** CFG838 tested the classical and bright M31 dSphs. E3 is 38 ultra-faints plus 7
  brighter systems. Only 5 systems are in both: CVn II, Leo IV, Hercules, And XI and And XIII.
- **CFG838's T is dominated by the dwarf's own structure.** T = |dg_host/dD| r₁₂ / g_int, and r₁₂/g_int spans far more
  than the host field does.
- **On CFG838's own sample, nothing tracks anything.** Every residual and variable gives |z| < 1, including CFG828's Δ
  (−0.14 ± 0.20).
- **The record already pointed this way:**
  - CFG838 reported ρ(Δ, g_host/g_int,N) +0.34 as the internal-field (g_bar) signal;
  - CFG875 found that its host-distance trend rides on the faint ultra-faints (M_V ≤ −6: k = 0.00 ± 0.13).
- **Reproduced first:**
  - CFG838's ρ (−0.001, −0.017) and CFG839's ρ (+0.077), from their committed rows;
  - CFG839's Draco orbit, 53.4 / 120.0 kpc, with this lane's orbit code.

**V3 (frozen): T1's trend is a PROXY (M_V) on both footings.**
- **The luminosity control kills it.** With M_V added, b_xe drops to +0.02 ± 0.20. log y₀ does not kill it
  (+0.78 ± 0.28, T1's A3). log Λ comes close (+0.20 ± 0.19).
- **The trend is not a single system.** Jackknife slopes span [+0.65, +0.86], and the Theil–Sen slope is +0.75.
- **The permutation control does not track.** With x_e shuffled, the partial slope is −0.14 ± 0.14.
- **The raw data trend is the same proxy.** For the Newton residual it is also PROXY (M_V): b_xe −0.05 ± 0.19 with M_V
  controlled.
- **Where a prediction contains the EFE, the trend survives M_V control.** v3 static gives +0.49 ± 0.18 and
  AQUAL + EFE gives +0.71 ± 0.19, both TRACKS HOST FIELD. Both predictions fall with x_e; the data do not.

## What this means for each flavor

- **v3 static:** a real excess, with two parts.
  - **(i) The EFE is too strong.** The predicted −0.55 dex/dex fall with host field is absent: the data give
    −0.05 ± 0.19, about 2.5 σ apart.
  - **(ii) An excess remains even in weak fields.** The distant, tidally safe satellites sit +0.79 to +0.90 above v3
    (x_e 0.02–0.11).
  - Neither part is tides, ellipticity, gradients or member counts.
- **v3 dust-free dynamics (U1):** +1.9 dex stays: STRUCTURAL stands.
  - Under its own stars-only mass, half the MW ultra-faints would be inside-out tidally exposed at pericentre. Their
    excess ignores that.
  - A dust-free v3 therefore has to explain why exposed and safe satellites look alike.
- **Plain AQUAL with its EFE (MOND):** +0.69 / +0.71 remains in the clean subset. Its EFE slope is contradicted at
  about 3.6 σ by the same fixed-luminosity test.
- **Isolated AQUAL (no EFE):** +0.47 / +0.42 remains. With worst-clean data it falls to +0.24 ± 0.12 / +0.19 ± 0.12.
  - This is the smallest gap and closest to the systematics floor.
  - Its trend with host field is a pure luminosity proxy.
- **The excess is concentrated in the faintest systems.** It rises 0.12–0.27 dex per magnitude fainter, at fixed host
  field. Fewer members (C4) account for part of that. The rest cannot be split between binaries and physics with these
  data.

## Checks (`z2_satellite_systematics.out`)

| check | what | result |
|---|---|---|
| K1 | E3 reproduced with own code | Newton +2.014 / +2.007; law +0.561 / +0.510 (max diff 0.009) |
| K2 | S1 reproduced | V3S +1.333 / +1.303, MOND +1.138 / +1.076, ISO +0.554 / +0.499. Per-system logG and U1's B0 exact (0.0) |
| K3 | T1 reproduced | slope +0.7607 / +0.8382; A3 +0.7792 / +0.8526 (exact) |
| K4 | CFG838/839 statistics and CFG839's Draco orbit reproduced | |
| K5 | turning points vs a 5-Gyr leapfrog in S1's field | 0.0000 |
| K6 | King radius | 3e-15 |
| K7 | gradient test power and size | |
| K8 | peak RSS | 0.53 GB |

Runtime: 577 s cold (tables), 212 s with the cached tables. One thread, nice 15, no downloads.

## What this does not show

- **Orbits:** static spherical MW, no LMC, no orbital decay. LMC-associated systems (Car II/III, Hor I, Hyi I, Ret II)
  have approximate pericentres.
- **Tidal mass:** extended beyond r₁₂ with the present boost. For EFE flavors the pericentric boost is smaller, so q is
  understated.
- **Clean subsets** are MW-only (no M31 PMs on disk) and small (2–14 systems).
- **Gradients** are testable for only 6 systems. Member counts use the N_eff = ½(σ/δσ)² proxy where no count is on disk
  (22 of 45 systems).
- **Missing data:**
  - stream associations and velocity gradients from DEIMOS / IMACS / GMOS per-star data;
  - published UFD velocity-gradient measurements (per-system spectroscopic papers or a compilation; size unknown
    without fetching, tables of this kind are typically < 1 MB). The example citation in `ASSUMPTION_LEDGER.md` was
    written from memory and is unverified;
  - Gaia PMs for M31 satellites.
- **Not separated:** binaries vs physics in the faint-end luminosity dependence. Multi-epoch σ for most UFDs would decide
  it.

## Files and run

- `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md` (5f7526ab41, committed alone first); `AMENDMENT_A1.md` (post-result).
- `z2_satellite_systematics.py` → `.out`, `_results.json`, `z2_per_system.csv`, `z2_stage_tables.json` (cached D10
  solves); `*_MUTATE.*`.

```
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/Z2_satellite_systematics/z2_satellite_systematics.py            # exit 0
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/Z2_satellite_systematics/z2_satellite_systematics.py --mutate   # exit 1 (K1-K3 fail)
```
