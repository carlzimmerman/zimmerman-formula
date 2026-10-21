# WT-04: how clocks tick where the framework's extra gravity acts

**Theory class: SAME AS GR WITH SAME MASS** (both footings). The largest framework-minus-GR difference in any clock observable
is 3.8e-6 / 4.2e-6 of the signal (cluster redshift), against the frozen 1e-3 line. **Cluster data class: R-LAW NOT DIAGNOSTIC
(PROVISIONAL)** on both footings, with its primary sitting 1.2–2.7σ short of the measured blueshift. **R-HUT CONSISTENT
(PROVISIONAL)**.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone in 0493b61a5 before any script or number.
  - Amendment A1 (c29715ec0) was committed alone before any number: implementation details and the PROVISIONAL data.
  - Amendment A2 was appended after run 1 and is uncommitted: one control fix and one tooth fix, disclosed below.
- **Settings:**
  - κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; Z = 5.7888.
  - Cold energy is real gravitating mass; no particle species.
  - Framework-native models only. External ingredients (survey kinematic term δ_SB, literature redshift values) are labelled.
  - Not theory closed. Nothing here says the data favour the framework.
- **Run:**
  - `OMP_NUM_THREADS=1 nice -n 10 python3 wt04.py` → `wt04.out`, `wt04_results.json`. Exit 0, 9/9 checks, 5 s, peak RSS 0.18 GB.
  - `WT04_MUTATE=1 …` → `wt04_MUTATE.out`, `wt04_results_MUTATE.json`. Exit 0, all three teeth bite, 12/12 checks.

## (a) Clock potential vs lensing potential: an identity up to the stress term

Sympy, from the static spherically symmetric Einstein equations with an anisotropic source:
- α′ = G(c²m + 4πr³p_r)/(c²r(c²r − 2Gm)).
- Isotropic transform: Ψ′ = Gm/r².
- Hence Φ′ = Gm/r² + 4πG r p_r/c² + (common nonlinear GR term).

Clock rate is set by Φ; lensing by Φ_L = (Φ + Ψ)/2. So **Φ_clock − Φ_L = (Φ − Ψ)/2, with (Φ − Ψ)′ = 4πG r p_r/c²**.

At the same T⁰⁰, the framework differs from GR with pressureless cold mass only through the tether stress p_r = −W_full(u) < 0
(CFG938). The sign is a slightly **shallower** clock potential. A dispersion-supported halo (p_r = ρσ² > 0) has the opposite sign
and a similar size (G1: 3.5e-6 in the cluster redshift).

**Identity flags (no verdict weight):**
- g₀₀ is the potential that moves slow baryons (minimal coupling), so clock data equal dynamics data.
- Clock and lensing information agree except for (Φ − Ψ)/2.

**Sizes:**
- F_a (|δΦ/Φ| along the galaxies): 1.1e-7 canonical / 1.2e-7 alt.
- K1a reproduces CFG938's cluster slip exactly: 5.0780e-6 / 5.7916e-6.

## (b) Time-dilation depth of isolated galaxies: FINITE, set by the cold-energy supply

D = [Φ(∞) − Φ(0)]/c². The framework's cut-off is the canonical supply rule (CFG804): the law holds out to the edge R_e, where its
phantom mass equals 5.364 N M_b (census N = 10 for both galaxies, R_e = 54.14 r_M). The field is Keplerian beyond R_e. Υ = 0.61;
spherical, midplane approximation.

| | footing | R_e | D (law + edge) | D (Newtonian baryons) | ratio | Φ/c² at 30 kpc (law / Newton) |
|---|---|---|---|---|---|---|
| NGC 3198 (M_b 4.72e10) | canonical | 454 kpc | **1.748e-6** | 4.10e-7 | 4.26 | −1.03e-6 / −7.27e-8 |
| | alt | 413 kpc | **1.867e-6** | 4.10e-7 | 4.55 | −1.10e-6 / −7.27e-8 |
| DDO 154 (M_b 3.70e8) | canonical | 40 kpc | **1.111e-7** | 1.02e-8 | 10.8 | −3.11e-8 / −5.9e-10 |
| | alt | 37 kpc | **1.191e-7** | 1.02e-8 | 11.6 | −3.17e-8 / −5.9e-10 |

**What sets it:**
- **Without the edge the depth is infinite.** D_L grows by v_f² ln 10 per decade (NGC 3198 canonical: 1.96e-6, 2.58e-6 and
  3.20e-6 at 1, 10 and 100 Mpc).
- **With the edge it is finite** (D_L unchanged to 4e-10 between 10 and 1000 R_e). This holds by construction: a finite cold
  mass means Keplerian gravity beyond R_e.
- **The supply sets the depth logarithmically.** dD/d ln R_e = 2.69e-7 ≈ v(R_e)²/c² = 2.72e-7. So D ≈ (v_f²/c²)[ln(R_e/r_in) + 1].
- **Report-only variants (NGC 3198, canonical):**

  | variant | D |
  |---|---|
  | ν_mono kernel | 1.738e-6 |
  | supply ×2 | 1.934e-6 |
  | edge at 3 Mpc (KiDS-bound, external) | 2.257e-6 |
  | E1 EFE at 0.01 / 0.03 a0 (assumed values; the record's current choice is no EFE) | 1.21e-6 / 1.06e-6 |

  The EFE makes the depth finite even without an edge.
- **Plainly:** a clock at NGC 3198's centre loses about 24,000 yr per 13.8 Gyr against a clock far away. With baryons only it
  would lose about 5,700 yr.

## (c) Cluster gravitational redshift

**Model.** CFG687 gas + stars for the eRASS1 median cluster (M_gas500 1.16e13, R500 0.79 Mpc), plus the 16% and 84% clusters.

**Kinematic terms.** Derived here; signs match Kaiser 2013.
- Transverse Doppler: (3/2)⟨σ²⟩/c.
- Light cone: +⟨v_z²⟩/c. The Monte Carlo light-cone crossing gives +3.23 ± 0.16 against +3.34 km/s.
- Survey flux term: −δ_SB⟨σ²⟩/c, δ_SB ∈ {0, 2, 4} (EXTERNAL).

**R-LAW (primary, the canonical cluster rule).**
- Setup: ν_mono kernel; cold energy fills the law to the supply edge (census N 1.116, M_c 3.79e14 M_⊙, R_e 2.27 / 2.13 Mpc).
- Δ_grav −2.78 / −2.90 km/s. Kinematic +0.33 / +0.35 km/s (σ_LOS ≈ 450 km/s).
- **Total P = −2.44 / −2.55 km/s.**
- Profile at R = 0.6 and 1.6 Mpc: −2.2 and −3.4 km/s. There are no members beyond R_e / 3 Mpc.
- Band over the 288-member grid: [−12.1, −0.6] (canonical) and [−13.1, −0.6] (alt) km/s. The low end needs the 84% cluster
  with BCG, no edge and δ_SB 4.
- Median-cluster-only band: [−9.2, −1.1] / [−9.9, −1.1].

**R-HUT (CFG949 untethered reading; post hoc, FRAGILE; median parameters only).**
- Δ_grav −7.17 km/s; **P = −6.84 km/s**.
- Profile −6.5, −8.4, −9.5 and −10.0 km/s at R = 0.6, 1.6, 3.3 and 5.2 Mpc.
- Band [−10.1, −5.0] km/s.

**Newtonian baryons only:** Δ_grav −0.51 km/s.

**Framework-internal result (no data):** Δ_grav(R-LAW)/Δ_grav(R-HUT) = **0.39 / 0.41**. Clocks see the same core deficit that
lensing sees (CFG687 A_MID 1.9).

**Data (PROVISIONAL; A1 item 7).** W11 −7.7 ± 3.0, S15 −11 (+7/−5), R23 −11.4 ± 3.3 km/s. J15 (~ −10, no error) is not graded.

| reading | W11 z_mid | S15 z_mid | R23 z_mid | z_near (all) | class |
|---|---|---|---|---|---|
| R-LAW canonical | +1.75 | +1.22 | +2.71 | 0 | **NOT DIAGNOSTIC (PROVISIONAL)** |
| R-LAW alt | +1.72 | +1.21 | +2.68 | 0 | **NOT DIAGNOSTIC (PROVISIONAL)** |
| R-HUT | +0.29 | +0.59 | +1.38 | ≤ 0.38 | **CONSISTENT (PROVISIONAL)** |

**Reading.** The law alone predicts about a third of the measured blueshift. That leans the same way as the lensing core excess,
but it is not a tension: the declared variants (mass, BCG, edge, survey term) reach the data. A lensing-matched mass predicts the
measured size, as GR would for the same mass. The cluster redshift adds no clock-specific test beyond lensing.

## (d) Strong-lens Fermat potential: identical at fixed Σ

At fixed image positions and fixed Σ_lens, ψ is fixed and so is τ. This is an identity.

At fixed T⁰⁰ the only difference is the tether stress (δψ from δΦ/2): 3.2e-8 / 3.8e-8 of the Fermat-potential difference
between 2 and 8 kpc, for a 2e11 M_⊙ Hernquist lens. Measured delays are at the percent level.

## (e) One line

**No.** At the same total mass (baryons + cold energy) there is no clock-rate observable that differs from GR above ~4e-6 of the
signal on either footing. The only formal difference is the tether stress, a post-Newtonian (v²/c²) correction to an already
v²/c² effect. It is opposite in sign to a dispersion-supported halo, and 5–6 orders of magnitude below any measurement.

## Controls and MUTATE

**Controls, all PASS:**
- K1a: CFG938 slip reproduced, relative 0 / 4e-16.
- K1b: CFG804 N 10.000000, log M_ta 12.304, edge 54.14 r_M.
- K1c: CFG949 gas extrapolation 4.5688.
- K2a: solar surface redshift 0.63633 km/s.
- K2b: Plummer Φ(0) ratio 1.0000000.
- K2c: Φ = Ψ = −GM/r.
- K3: NFW 1.3e-9.
- K4: light cone and transverse Doppler.

**MUTATE, all teeth bite:**
- T1: an injected slip of 0.1 flips the class to DISTINCT SIGNATURE (F 0.1).
- T2: a0 → 0 gives Newton (depth ratio 1.000000005; cluster 1.000000000).
- T3: N → ∞ makes the depth NOT FINITE (D_L moves 52% between 10 and 1000 R_e).

**Disclosures (Amendment A2):**
- Run 1 failed K3 on a 0/0 at r = 0, a control-code bug. Classes were withheld. It is kept as `wt04_run1_K3nan.*`.
- MUTATE run 1 failed T2's cluster leg (1.000425) on a tracer-truncation grid mismatch between the two readings. It is kept as
  `wt04_MUTATE_run1_T2grid.*`.
- No class number changed. Report-only band breakdowns were added after run 1.

## Caveats (strongest first)

1. **The theory class holds for CFG938's parent** (CONDITIONAL; its C3 FAIL is inherited). It also needs minimal coupling of
   baryons and photons. A parent with relativistic-scale anisotropic stress could break it, as CFG847 notes.
2. **The cluster comparison is not sample-matched** (eRASS1 X-ray median vs SDSS optical stacks of ~1e14 M_⊙). δ_SB is
   survey-dependent. The data are literature values read through summarised pages (PROVISIONAL).
3. **R-HUT uses CFG949's median c, r_s and M_ta**, not per-cluster native profiles. It inherits CFG949's post hoc and FRAGILE
   status.
4. **"Infinity" is the isolated idealisation.** Neighbours' cold energy (CFG903) and the cosmic background are not included.
   With the edge at 3 Mpc the depth rises ×1.29.

**Sources consulted (PROVISIONAL look-ups, abstract/HTML only):**
- arXiv:1109.6571, read on its abstract page and the ar5iv HTML rendering.
- arXiv:1410.5262, arXiv:2206.05313, arXiv:1410.6050, arXiv:1303.3663 and arXiv:2503.11585.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
