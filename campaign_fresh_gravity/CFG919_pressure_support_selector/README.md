# CFG919: is the baryons' kinematic state (pressure vs rotation support) the selector of the law's excesses?

**Bottom line.**
- **SELECTOR CONTRADICTED** on both footings, AS FROZEN and UNDER A1 (identical: C1 never fires).
- **FRAGILE:** a doubled systematic floor (V6, 0.10 dex) turns the canonical footing SUPPORTED and the alt footing NOT
  DIAGNOSTIC.
- **The ordering is real.** At matched g_bar, pressure-supported classes sit above rotation-supported ones:
  - ordering statistic T = +0.528, permutation p = 0.002;
  - n > 2 lenses sit above n < 2 lenses by ΔE = +0.29 (z +3.5);
  - no rotating cell carries an excess;
  - no non-globular pressure-supported cell sits on the law where a less pressure-supported one carries the excess.
- **No single amplitude.** No one-parameter form in the kinematic measure fits all classes:
  - F1 (E = A·f_P): χ² 89.4/32, p 2.5e-7 canonical; 93.5/32, p 6.1e-8 alt.
  - F2 (step at v/σ = √3): p 1.4e-8 on both footings.
  - The dwarfs carry ~3–5× the n > 2 lenses' excess at the same g_bar. The clusters' excess rises with g_bar while the dwarfs'
    falls, at the same f_P ≈ 1.
- **Theory: the record's cold-energy equation (CFG638) cannot make a kinematic selector at all.** Any kinematic selector is
  a NEW POSIT (below).

κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled. Raw data and framework-native quantities only. Cold
energy, not a particle. Not "theory closed". Nothing here says the data favour the framework.

- **Kind:** HYPOTHESIS TEST (pre-registered). Block 910–919.
- **Criteria:** `FROZEN_CRITERIA.md`, 8d34dc761, committed alone before any script or number.
- **Amendment:** `AMENDMENT_A1.md`, 5c9edd07b, POST HOC, written after the frozen INJECT failed and before the main run.
- **Not blind:** CFG828 and CFG851 made a contradiction plausible; disclosed in the criteria.

## What was tested

H-KIN: at matched g_bar, E = ln(g_obs/g_pred) is set by one dimensionless pressure-support measure.

**Measures:**
- **Primary:** f_P = 3σ²/(v² + 3σ²), the random fraction of the baryons' kinetic energy.
- **Alternative:** f_sph, the pressure-supported mass fraction.

**Classes and their f_P:**

| class | f_P | basis |
|---|---|---|
| 83 LVD dwarfs (CFG880) | 1.0 | class value; no rotation data on disk |
| SPARC small/large | 3σ²/(V_flat² + 3σ²), σ = 10 km/s | per galaxy |
| B21 isolated lenses n < 2 / n > 2 | 0.2 / 0.8 | declared PROXY: lensing has no kinematics; n describes the central galaxy, while lensing probes 30–300 kpc |
| eRASS1 shear-stack clusters (CFG687, MID+OUTER) | 1.0 | ICM is thermal |
| 31 globulars (CFG883) | ARot/sigma0 (Baumgardt) | measured for 10 of 31; class median for the rest |

**Cells:** 0.5-dex windows in g_bar; floor 0.05 dex per cell.

**Not tested:**
- early-type galaxies with dynamics: no kinematic-state column and only IMF-dependent M* on disk;
- within-class kinematics of dSphs and clusters: no data.

**Inputs:** CFG914's input section exec'd read-only, with all 9 of its K-checks passing. This lane's own SPARC and B21 loaders
are bit-for-bit equal to CFG914's arrays.

## Controls

| control | result |
|---|---|
| K1 CFG828 | reproduced exactly (max diff 0): N_in 8, D +0.051 ± 0.073 dex, out-of-range mean +0.438, SPARC median +0.031 |
| K2 CFG829 | reproduced exactly: blue A 1.016 ± 0.086, red 1.587, class "LAW HOLDS AT LOW g" |
| K3 CFG849 | Sérsic disc 1.066 / sph 1.602 exactly |
| K4 | CFG914's input checks 9/9 |
| K5 | Baumgardt parse (47 Tuc 5.00 / 11.9); f_P of the globulars 0.235–0.999 |
| MUTATE shuffle | **BITES** both footings (exit 1 as designed). On planted data (E = 1.0·f + noise) the true labels give SUPPORTED, T +0.827, A 1.020 ± 0.049; 1000 label shuffles give SUPPORTED in 0.0% (frozen and A1), median T −0.003 |
| INJECT, AS FROZEN | **FAILED**: I1 SUPPORTED 85.0% (< 90%) on both footings. I0 0.5% and I2 92.0% passed. Cause: the frozen C1 clause, see `AMENDMENT_A1.md` |
| INJECT, UNDER A1 | **all met** (exit 0): I1 91.0% with Â median 1.002 (98% within 2σ); I2 92.5%; I0 0.5% |

A1 changes only C1's comparison. A rotating cell must now carry at least the pressure-supported mean excess at that g_bar,
instead of merely lying within 2σ of it. It does not affect the main result: zero C1 elements under either rule.

## Main result (V0)

Class means are GLS over each class's cells. E is in ln units; dex = E/ln 10.

| class | f | canonical E (dex) | alt E (dex) | log g_bar span |
|---|---|---|---|---|
| dwarfs (83 LVD) | 1.00 | +0.856 ± 0.102 (+0.372) | +0.765 ± 0.102 (+0.332) | −14.1..−11.8 |
| SPARC small | 0.075 | +0.137 ± 0.084 (+0.059) | +0.057 ± 0.084 (+0.025) | −11.7..−10.4 |
| SPARC large | 0.012 | +0.002 ± 0.050 (+0.001) | −0.053 ± 0.050 (−0.023) | −11.6..−8.4 |
| lenses n < 2 | 0.20 | +0.008 ± 0.091 (+0.003) | −0.083 ± 0.091 (−0.036) | −13.1..−11.4 |
| lenses n > 2 (+0.123 M*) | 0.80 | +0.293 ± 0.067 (+0.127) | +0.203 ± 0.067 (+0.088) | −13.1..−11.3 |
| eRASS1 clusters | 1.00 | +0.560 ± 0.077 (+0.243) | +0.476 ± 0.077 (+0.207) | −12.7..−10.9 |
| globulars (stiffness-conditional) | 0.935 | +0.254 ± 0.134 (+0.110) | same | −11.7..−9.8 |

**Tests, canonical / alt:**
- C1 (rotating with excess): 0 / 0, both rules.
- C2 (pressure-supported on the law at the same g_bar): 0 / 0.
- W1 (lenses sph − disc): +0.290 (z +3.5), ordered.
- W2 (SPARC galaxies, Spearman of f_P vs residual): ρ −0.17, p 0.04. This is a weak ANTI-ordering, below the frozen violation
  bar (p < 0.01), and confounded with mass.
- W3 (globulars): ρ +0.10, p 0.58.

**Forms:**
- F1: A = 0.558 ± 0.049 / 0.455 ± 0.049. Class z: dwarfs +2.9 / +3.0, n > 2 lenses −2.3 / −2.4. **FAIL** (p ≪ 0.01).
- F2: A = 0.496 / 0.408. Class z: dwarfs +3.5, n > 2 lenses −3.0 / −3.1. **FAIL**.

Both fail, so criterion C3 sets **SELECTOR CONTRADICTED** on both footings.

**Why there is no common form** (the cells, canonical):
- At g_bar 10^−13.2…−12.7, the dwarfs (f = 1) carry E = 1.71 / 1.41. The n > 2 lenses (f = 0.8) carry 0.55 / 0.28 in the same
  windows. A form linear in f allows a ratio of 1.25; the observed ratio is 3–5.
- At f = 1 the dwarfs' E falls with g_bar, from 1.71 at 10^−13.2 to 0.40 at 10^−11.8. The clusters' E rises with g_bar (−0.35 at 10^−12.2 →
  +1.18 at 10^−10.9).
- Opposite g_bar trends at the same kinematic state cannot come from one kinematic measure. Adding an acceleration gate does
  not rescue it: secondary F3 (E = A·f·Θ(g_bar < 1e-12)) FAILs with p 2.5e-16 / 1.2e-13, because the clusters' excess lies
  above 10^−12 (cluster z +6.3 / +5.4).

**Robustness (variants; class unchanged except V6):**
- V1 f_sph, V2 colour bins, V3a/V3b f brackets, V4 globulars vs law+EFE, V5 clusters + INNER, V7 no M* shift: all CONTRADICTED
  on both footings (F1 p ≤ 4e-5).
- **V6 (floor 0.10 dex): canonical SUPPORTED.** F1 A = 0.576 ± 0.077, χ² 45.6/32, p 0.056; dwarfs z +2.6, n > 2 lenses −1.7.
- **V6 alt: NOT DIAGNOSTIC.** F1 p 0.038; F2 p 0.027 / 0.028.
- **Reading:** the contradiction holds if the per-cell systematics are ~0.05 dex. If they are ~0.10 dex (plausible for lens M*,
  CFG840; and dwarf M/L), the linear kinematic form survives on the canonical footing at p = 0.056 with the dwarfs 2.6σ high.
  Label: **FRAGILE**.

## Theory note: can CFG638's cold-energy equation depend on the baryons' kinematic state at fixed g_bar?

**No.** The record's system (CFG638, moments of CFG541/544/554):
- ∂ₜf + ∇ₓ·[(v + v_s)f] − ∇Φ·∇ᵥf = γ∇ᵥ·[(v − u)f + σ_J²∇ᵥf];
- γ = α/τ, τ = (4πGρ_m)^−½;
- v_s = −α 1_B 1_C τ∇ψ, ∇²ψ = 4πG(ρ_ph − ρ_c), ∇²Φ = 4πG(ρ_b + ρ_c).

The baryons enter only through their density ρ_b:
- in Φ;
- in ρ_m (the clock τ);
- in the law's phantom target ρ_ph, built from the baryons' g_N;
- in the region indicators B and C.

No baryon velocity field or stress tensor appears. The bath target σ_J² is a posit (CFG554/558; CFG876 broke a universal
value), not the baryons' dispersion.

In the stationary state v_s = 0, so ∇ψ = 0 and ρ_c = ρ_ph (the deficit closes two-sidedly). Stationary states do not depend on
α, τ or σ_J² (CFG541 V4; CFG638 reading 2): those set timing only. In spherical symmetry ρ_ph(r) is fixed by M_b(<r) alone.
Two systems with the same M_b(<r), one rotating and one dispersion-supported, therefore settle to the same g(r) = g_law. The
equation cannot order the excess by kinematic state, and it cannot produce any excess over the law in equilibrium.

What a kinematic selector would need. Each item is a NEW POSIT, none in the record:
1. **A coupling of cold energy to the baryons' stress tensor.**
   - Ordered rotation is excluded by symmetry: a steady azimuthal flow in axisymmetry transports nothing radially, so only random
     motions could enter.
   - Example forms: a bath target σ_J² ← σ_b², or a drift/source term ∝ ∇·(ρ_b σ_b²).
   - A term ∝ ρ_b σ_b² needs a new velocity scale. Measured against c it is ~σ²/c² ~ 1e-8, which is negligible. So the posit
     brings a new constant.
   - A bath tied to σ_b alone changes the cold energy's velocity structure, not its settled density.
2. **A retention/overfill rule that depends on the baryons' kinematic state.** The two-sided drift removes any surplus above
   ρ_ph, so a retained excess needs its own posit. It sits in the same family as CFG913/915/916's mobility and latching rules,
   which are excluded, contradicted or underdetermined.
3. **Geometry, not kinematics.** Flattened rotating discs and spheroids have different 3-D phantom fields at the same in-plane
   g_bar. This correlates with rotation but is a shape effect. Its sign and size would need a non-spherical calculation; not done
   here.

Even granting such a posit, this lane finds that one kinematic measure does not reproduce the excess amplitudes at the 0.05-dex
floor.

## Limitations

- **Lens proxy.** Lens kinematics are a Sérsic-index proxy.
- **dSph class value.** dSph f_P is a class value (v/σ ≈ 0, bracketed in V3a to v/σ = 0.5 and 1).
- **Globular coverage.** Baumgardt ARot covers only 10 of 31 globulars. Globular elements carry no class weight (stiffness,
  CFG820).
- **Inherited conventions:**
  - dwarfs: Υ_V = 2 and CFG880's gas inside r½; at 10^−12…−11.5 this sample sits +0.18 dex above the law, where CFG828's
    SFH-M/L sample sat with SPARC;
  - B21's published ESD → g_obs conversion;
  - CFG850's +0.123 dex M* on n > 2;
  - CFG687's cluster law with its FP0 a0.
- **Early types with dynamics: NOT TESTED.**
- **Spurious matmul warnings.** The matmul RuntimeWarnings are macOS Accelerate floating-point flags. They are checked against an
  explicit sum, and finiteness is asserted in the code.

## Reproduce

All three runs use one core and < 0.2 GB, and take a few seconds each:
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg919.py` → `cfg919.out`, `cfg919_results.json` (exit 0).
- `CFG919_MUTATE=shuffle ...` → `cfg919_MUTATE_shuffle.out`, `cfg919_results_MUTATE_shuffle.json` (exit 1 = bites).
- `CFG919_MUTATE=inject ...` → `cfg919_MUTATE_inject.out`, `cfg919_results_MUTATE_inject.json` (exit 0 = recovered under A1;
  the frozen-rule failure is printed in the same file).

Nothing was downloaded. No other lane's files were edited: CFG914/880/883/687 code was exec'd read-only, and the
CFG828/829/849/827/824 outputs were read.
