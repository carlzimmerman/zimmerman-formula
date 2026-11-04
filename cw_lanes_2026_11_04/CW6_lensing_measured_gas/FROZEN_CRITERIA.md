# CW6_lensing_measured_gas: FROZEN CRITERIA, committed alone before any script or number

**Not blind.** LE1's gap is known: the law sits about 0.09 dex low in KiDS galaxy lensing (A1 +0.089 / +0.050 dex, A30 Z +9.27 / +6.52, G3 z +5.01 / +3.32, canonical / alt). The kSZ amplitudes of GH10 and GH11 are known. GH2 showed, on X53's harness (bins 3-4), that Zhang's gas cut at R_vir lowers the law's χ² (95 to 66) and that a cut at 1.5 R_vir or beyond raises it (136 at 1.5). S2 showed that the fixed 0.5 M★ hot term lowers the B21 colour amplitudes (blue by 0.11, red by 0.23). No CW6 number exists yet. The F1 and F2 tapers have never been fitted to the DR2 points.

κ = ½ FITTED and held fixed. The cold sector stays retired; nothing here adds a particle or a cold component. Not theory closed. Nothing here says the data favour the framework. No downloads. No file outside this folder is edited. Every grader runs from a copy or an exec of the record's text, with the gas term as the only swap.

## Step 0: record check
- GH9, GH10 and GH11 measured the kSZ amplitude A of Zhang's gas template on DESI × ACT points. They graded it against route E's need. None put the measured gas into the law's lensing.
- GH2 put Zhang's X-ray gas (A = 1, sharp cut at k R_vir) into the law on X53's harness, bins 3-4 only. That is not LE1's A30 or G3, not kSZ-normalised, no tapers, no colour split.
- RF4 graded route E, not the law.
- So the question is open.

## Question
Does the gas the record already measured close the law's 0.09 dex galaxy-lensing gap?

## Method
In each harness, the fixed hot-gas term is replaced by a measured extended gas profile. Nothing else changes: stars, cold gas, projection, two-halo, covariance, stacking, data.

### Gas profiles (frozen set)
Shape: Zhang et al. 2024's β-model, β 0.43, r_c 6 kpc, base(r) = [1 + (r/r_c)²]^(-0.645).
- **sharp(k):** base(r) for r ≤ k R_vir, 0 beyond.
- **F1(k):** base(r) × exp(−r²/2(k R_vir)²), to 6 k R_vir (GH10_smooth_gas_taper).
- **F2(k):** base(r) × ½ erfc[ln(r/k R_vir)/(√2 × 0.3)], to 6 k R_vir (GH10_smooth_gas_taper).

Template normalisation, every shape: **Zhang's normalisation inside R_vir**, M_T(< R_vir) = 1.84 M★. The measured profile is M_gas(< r) = A × M_T(< r).

A comes from the published DESI DR2 × ACT DR6 kSZ points (Hadzhiyska et al. 2026, arXiv:2604.19745) in GH10's differential bin (CIGALE log M★ 10.5-11), with GH9's mass-scale offset and GH11's miscentring (satellite fraction 0.24, σ_off 300 kpc), b = 0, all 13 θ, full covariance.

| ID | Shape | A | Source |
|---|---|---|---|
| **P1 PRIMARY** | sharp(1.8) | 0.5417 | GH11 primary |
| P2 | sharp(1) | 0.7449 | GH11 primary |
| P3 | sharp(3) | 0.6051 | GH11 primary |
| P4 | F1(1.8) | fitted here | GH11 primary machinery, F1 template |
| P5 | F2(1.8) | fitted here | GH11 primary machinery, F2 template |
| P6 | sharp(1) | 1 | Zhang's X-ray value inside R_vir, no kSZ |
| B1 | sharp(1.8) | 0.4480 | no miscentring (GH10 primary) |
| B2 | sharp(1.8) | 0.8511 | extreme miscentring (0.5, 500 kpc), GH11 bracket |
| B3 | sharp(1.8) | 0.5417 | lens masses read on CIGALE's scale, see mapping |
| B4, B5 | sharp(1.8) | 0.5417 ± 0.1359 | GH11's e, statistical error with the 10 % r term |

P1 decides the label. P2-P6 are the profile spread. B1-B5 are reported brackets on P1.

**P4 and P5 fits.** GH11's `model(k, f_s, σ_off)` and `fit(m)` (b = 0), copied, with gas images built from the tapered column: τ(R) = σ_T n_e0 fac × 2∫ f(√(R² + l²)) dl to 6 k R_vir. Here n_e0 is GH10's Zhang normalisation and fac = M_base(< R_vir)/M_f(< R_vir). Reported: A, s, e = √(s² + (0.1 A)²), χ², p (12 dof).

### Mapping onto lens mass
- The gas rule takes each harness's own catalogue stellar mass at native h. G3 has no native conversion; it uses its bin mass as is.
- R_vir(M★) is GH10's table of Zhang's Table 1: log M★ 9, 9.5, 10, 10.5, 10.75, 11, 11.25, 11.5 → 82, 102, 131, 178, 210, 295, 480, 950 kpc. It is interpolated linearly in log M★ and clamped at the ends.
- **Primary scale δ = 0:** lens catalogue masses are read on Zhang's (Chen+12) scale, as GH2, X78 and SI2 tie gas to catalogue M★.
- **B3, δ = +0.19 dex:** GH9's median CIGALE − Chen offset is read as the lens offset. Gas mass and R_vir are evaluated at log M★ + 0.19.
- One A for every lens mass. The kSZ bin sits at Zhang-scale log M★ about 10.7-11.15; outside it the ratio is extrapolated.
- Red and blue lenses get the same gas. There is no colour-resolved gas measurement on record.
- Cold gas stays as each harness has it.
- **NV2's external field:** available for no lens sample. NV2's B21 isolated-lens rebuild failed (486,584 against 259,383) and KiDS-bright E1 is noise-dominated. No external field enters any number here.

## Harnesses and samples (both footings, canonical a0 9.3603e-11, alt 1.1312e-10, never pooled)
**H1: LE1's harness on B21's isolated lenses (Brouwer et al. 2021), Fig-3 mass bins, all colours.**
- G1 = RQ3's A30: CRG1's `Stencil`, two-halo b ≥ 0 per bin, native conversion, stack over the lens mass grid, full covariance, χ² on 56 dof, Z = (χ² − 56)/√112. The swap is in G1's baryons, M★ + M_cg + M_hot(< r), where M_hot = 0.5 M★ min(1, (r/100 kpc)³) becomes M_gas(< r).
- Also: A30 with no two-halo term (dof 60), and A1 (LE1's G1 model with G3's statistic: inverse-variance mean of log10(Y/model) over R ≤ 0.31 Mpc, diagonal σ, n 32), overall and per bin.
- G3 = CX1's lensing line, through NP1's `cx_rows`. Its own baryons are a point mass M★ + 0.25 M★. Three rows: CX1's own baryons (the K1 row); G1's inventory with the fixed hot term (reference); G1's inventory with M_gas(< r). The data g_obs = 4GΔΣ and CX1's row sd stay.

**H2: B21's isolated lenses by colour (B21 Fig-8 colour bins), S2's forward model.** S2's text is exec'd up to its K2 block, as BL1 does. Config: S2's L4 row (v3 at y_e = 0, h 0.679, split `typ`, no mass shifts). The hot term fhot × M★ × min(1, (r/100 kpc)³) becomes M_gas(< r) at the catalogue M★. Output: S2's window amplitude A (CFG829's window, 6 B21 points, GLS, full window covariance) for blue, red and all, and the 15-point χ² at A = 1.

**H3: SI2's clean (spectroscopically isolated) lenses by colour.** SI1's head is exec'd as SI2 does (P2 phase B on P2's shear measurement), at R0 (catalogue M★, no red shift), with SI2's colour split (u − r > 2.0).
- The swap is in the law's own-lens table, where P2's `meff_lens` hot term becomes M_gas(< r).
- **Primary:** neighbours carry the same gas, as P2's point masses, M★(1 + cold) + M_gas(< ∞).
- **Reported:** own lens only.
- Samples S3 (I3 hole) and S1 (I1 hole), colours all, red and blue.
- Output: A_in (0.03-0.31 Mpc), A_O1, A_O2 with jackknife σ (36 patches), and the law's 15-bin χ² with Hartlap.
- P2's measurement cache (hash d8787042a095deef) is read from a local scratch copy, passed as an argument and not committed.

## Lines (frozen)
- For each colour-split sample s ∈ {B21c (H2 window A), S1 (H3 A_in), S3 (H3 A_in)} and colour c ∈ {red, blue}: z_c = (A_c − 1)/σ_c, with σ_c statistical, from the same run.
- **Line: |z_c| ≤ 2,** within 2σ of 1.
- **Move:** m_c = (A_c,P − A_c,fixed)/σ_c,fixed.

## Labels (per footing, from P1; precedence top to bottom)
1. **NOT EVALUABLE:** a K1 fails in any harness, K3 fails, or MUTATE does not bite. If K2 fails, only P4 and P5 are NOT EVALUABLE.
2. **OVERSHOOTS (blue)**, or (red), or (red and blue): on some sample, z_c < −2 and m_c ≤ −1. The swap lowered that colour by at least 1σ and left it more than 2σ below 1.
3. **GAP CLOSED:** on all three samples, |z_red| ≤ 2 and |z_blue| ≤ 2.
4. **GAP NARROWED:** on B21c, m_red ≤ −1.
5. **GAP WIDENED:** on B21c, m_red ≥ +1.
6. **GAP UNCHANGED:** otherwise.

Printed beside every label:
- **A30 flag:** PASSES (|Z| ≤ 2), IMPROVES (ΔZ ≤ −1), WORSENS (ΔZ ≥ +1) or SAME.
- A1 and G3 before and after.
- **PROFILE-DEPENDENT** if any of P2-P6 gives a different label, with each one listed.
- B1-B5.

The same rule is printed for every profile.

## Checks
- **K1, H1:** with LE1's fixed gas term, the harness reproduces `le1_real.json` exactly (|d| ≤ 1e-9): A30 law Z +9.27 / +6.52 (χ² 154.1 / 125.0), no two-halo +9.19 / +6.17, A1 +0.0887 / +0.0500 (z +6.69 / +3.78), G3 z +5.01 / +3.32.
- **K1, H2:** with the fixed term, S2's committed L4 row is reproduced (A and σ for blue, red, all, both footings; |d| ≤ 1e-9): canonical 0.878 / 1.313 / 1.207, alt 0.802 / 1.200 / 1.103.
- **K1, H3:** with the fixed term, SI2's committed law numbers at R0 are reproduced (χ²_L, A_in, σ, A_O1, A_O2 for all, red, blue, S1 and S3, both footings; |d| ≤ 1e-9).
- **K2, kSZ copy:**
  - sharp(1.8) through this lane's copy reproduces GH11's primary A 0.5417 and no-miscentring 0.4480 within 1e-3;
  - F2 at width 0.005 gives A within 2 % of sharp(1.8).
- **K3, gas profiles:**
  - M_T(< R_vir) = 1.84 M★ within 1e-4 for every shape at log M★ 10, 10.75, 11.3;
  - the sharp-cut total matches an independent quadrature within 1e-4;
  - F2 at width 0.005 matches the sharp total within 1 %.
- **K4, G3 hook:** fed CX1's own baryons, the swap hook reproduces LE1's G3 z within 1e-9.
- **MUTATE twin:** the gas term is zeroed everywhere (own lens and neighbours; stars and cold gas kept). Outputs are `cw6_<mode>_MUTATE.{json,out}`.
  - It **bites** if, in every harness, sample and footing, the all-lens inner amplitude (A1 amplitude, window A, A_in) rises above both its fixed-term value and its P1 value by at least 0.01, and A30's χ² differs from P1's by at least 5.
  - The MUTATE outputs also go through the label code, printed and not graded.

## Caveats, attached to every label
1. **The kSZ samples aren't isolated.** The satellite fraction is about 0.28 at log M★ > 10.5. Host-halo gas and two-halo signal are not subtracted.
2. **They are matched in mass only roughly.** It is a CIGALE bin, read on Chen's scale through GH9; the lens masses are on their own catalogue scale.
3. **The innermost kSZ aperture is 1′,** about 250 kpc at the bin's redshift. Inside that, the radial shape is Zhang's β-model, assumed.
4. The points are not native: Planck 2018 reconstruction, r 0.64, σ_true 300 km/s. A scales as 300/σ_true.
5. One gas rule serves both colours and every lens mass.
6. A30's two-halo template carries the record's inherited Planck-era power spectrum.
7. In H3, neighbour gas is a point mass.

## Run rules
- `OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 10 python3 -I cw6.py <mode> [--mutate]`, one process per mode, RSS under about 1 GB.
- Modes: `gas` (K3 and the profile table), `ksz` (K2 and the P4, P5 fits), `le1`, `b21c`, `si2 <p2_work_dir>`, `verdict`.
- Outputs are named by mode, and MUTATE outputs carry `_MUTATE`.
- Amendments go in `AMENDMENT_A*.md`, each labelled pre- or post-result.

κ = ½ FITTED; not theory closed.
