# CFG925: three small reframings of the pressure-supported excess (A). None resolves it

**Bottom line.**

| reframing (zero new constants) | canonical | alt | in one line |
|---|---|---|---|
| R1 law-Jeans σ_los instead of Wolf (primary: β = 0, R_e aperture) | **NO EFFECT** | **NO EFFECT** | Wolf is already accurate under the law. F0 +0.372 → +0.369 dex (alt +0.332 → +0.329). BRACKET-DEPENDENT: strongly radial anisotropy at R_e gives PARTIAL, at most −0.114 dex |
| R2 self-sourcing, primary R2-A g_b = g(2 − ν(g/a0)) | **WORSENS** | **WORSENS** | acceleration floor (ln 2)² a0. Every class is pushed up 0.1–1.8 dex, rotators break, dwarfs overshoot |
| R2 secondary, R2-B g = ν(g/a0) g_b | WORSENS | WORSENS | every prediction is lowered 0.1–0.7 dex; rotators break |
| R2 literal, g = ν(g/a0) g | ILL-POSED | ILL-POSED | no finite solution (ν > 1 everywhere) |
| R3 include the framework's EFE (E1, the record's coded form) | **WORSENS** | **WORSENS** | satellites +0.48 dex on average. F0 +0.372 → +0.654 dex; the satellite–field gap grows ×2.8–3.9 (ROBUST over E1/E2 and host masses) |
| R3 remove the EFE | NO EFFECT | NO EFFECT | the record's dwarf numbers are already EFE-free, so removing it changes nothing (verified) |

- **What the three reframings show together:**
  - None of them makes the dwarf excess an artefact of how g_obs is estimated.
  - None turns the law's own self-consistency into an extra source.
  - The external field can only make the satellite excess worse.
- The most a declared bracket gives is −0.114 dex of the +0.372 dex dwarf excess (31%). That needs strongly radial orbits beyond
  R_e, which the record has no reason to assume.
- As stated before the run, neither g_bar-only reframing (R2-A, R2-B) can create or remove the red/blue split. The residual F1 − F2
  stays +0.12 to +0.14 dex.

κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are run separately and never pooled. Raw data and framework-native
quantities only. The extra mass is cold energy, not a particle. Not "theory closed". Nothing here says the data favour the
framework.

- **Kind:** HYPOTHESIS TEST (pre-registered). Block 920–929, "small reframings A".
- **Criteria:** `FROZEN_CRITERIA.md`, 661668f32, committed alone before any script or number.
- **Amendment:** `AMENDMENT_A1.md`, cc07e00a3, POST HOC. Written after the first K-only run and before MUTATE/main. It makes the
  K6 solver-residual tolerance conditioning-aware; no value moves.
- **Not blind:** the CFG921/919 facts and the record's notes on EFE sign and coupling G were read first. The analytic
  expectations (R1 NO EFFECT, R2 and R3 WORSENS) are disclosed in the criteria, section 0. All three came true.

## R1: the estimator (law-Jeans σ_los vs Wolf)

**Setup.**
- Sample: CFG880's 83 LVD dwarfs, Υ_V = 2, CFG874 HI gas.
- Stars: Plummer with a = R_e.
- Law potential: g = g_N ν_e(g_N/a0) on stars + gas.
- Spherical Jeans, luminosity-weighted σ_los inside the aperture.
- The excess is graded through CFG921's fact F0, the GLS class mean over CFG919's cells.

| corner | σ_J/σ_W median (range) | F0 canonical, dex | F0 alt, dex | g_bar < 1e-12 mean (68) | CFG828's 21 low-g dwarfs | class |
|---|---|---|---|---|---|---|
| Wolf (baseline) | 1 | +0.372 | +0.332 | +0.533 | +0.438 | — |
| **J0 β = 0, R_e (primary)** | **1.0009 (1.001–1.031)** | **+0.369** | **+0.329** | +0.532 | +0.437 | **NO EFFECT** |
| J1 Osipkov–Merritt r_a = R_e, R_e | 1.139 (1.126–1.159) | +0.258 | +0.218 | +0.420 | +0.325 | PARTIAL |
| J2 β = 0.5, R_e | 1.084 (1.080–1.108) | +0.300 | +0.261 | +0.463 | +0.368 | PARTIAL |
| J0 global aperture (any β, virial) | 0.969 (0.935–0.985) | +0.399 | +0.359 | +0.560 | +0.465 | NO EFFECT |

(The g_bar < 1e-12 and CFG828 columns are canonical.)

**Reading.**
- The Wolf estimator, applied to the law, is accurate to 0.1% in σ for isotropic orbits at the R_e aperture.
- The global σ sits ~3% lower. This is the deep-law virial theorem, σ⁴ = (4/81)GMa0 against Wolf's GMa0/18. The excess grows by
  +0.027 dex.
- Only radial anisotropy at the R_e aperture raises the predicted σ. Even the most radial corner, OM with r_a = R_e (β = 0.5 at R_e,
  0.8 at 2R_e), removes 0.114 dex of the 0.372 dex excess. RESOLVES would need 0.186 dex.
- Constant β = 0.5 with a cored Plummer tracer violates the central slope–anisotropy inequality (γ ≥ 2β). It is kept only because
  it was declared.
- β = 0.9 (MUTATE M1) moves F0 by −0.150 dex, still short of half.
- The dwarf excess is therefore not an estimator artefact under any reasonable orbit structure.
- R1 changes nothing outside dwarfs (lensing, rotation and shear estimators are untouched), so it cannot touch red lenses or clusters.

## R2: self-sourcing (cold energy's own mass in the law's argument)

**Derivation (see criteria section 2).**
- **R2-0, literal.** Take g = ν((g_b + g_c)/a0)(g_b + g_c) with g_c = g − g_b. Under the record's ID ρ_c = ρ_ph, the cold energy
  is the whole non-baryonic part, so this becomes g = ν(g/a0) g.
  - There is no finite solution, because ν_e(y) > 1 for all finite y.
  - The iteration g → ν(g/a0) g runs away: after 200 steps from y_b = 1e-3, 0.1 and 10 it reaches 38.8 / 38.9 / 40.2 a0 and is
    still rising (K6).
- **R2-A, primary.** This is the record's closest well-defined form: CFG638's phantom target is built from ρ_b + ρ_c, with
  ρ_c = ρ_ph kept. It is CFG722's coupling G applied to tethered cold energy, the coupling CFG722 rejects as double counting.
  - The quantity in ν is g_N[ρ_b + ρ_c], which equals g. Then g_c = (ν(g/a0) − 1)g, i.e. g_b = g(2 − ν(g/a0)).
  - It reduces to Newton (g → g_b) at high acceleration and agrees with the plain law to first order in (ν − 1).
  - It is real only above ν = 2, i.e. g ≥ y_f a0 with y_f = (ln 2)² = 0.4805 (also 0.4805 for ν_mono). Every system therefore
    sits at g ≥ 4.5e-11 m/s² (alt 5.4e-11), and its enclosed mass grows ∝ r².
- **R2-B, secondary.** ν takes the total field and the prefactor stays baryonic: g = ν(g/a0) g_b. In the deep limit
  g = a0^{1/3} g_b^{2/3}, which is lower than the law everywhere.

**Shifts and residual facts (canonical; alt alongside in the JSON).**

| fact | observed | R2-A residual (shift) | R2-B residual (shift) |
|---|---|---|---|
| F0 dwarfs | +0.372 | −0.489 (−0.861): overshoot | +0.758 (+0.386) |
| F1 red/sph lenses | +0.127 | −0.680 (−0.807) | +0.493 (+0.366) |
| F5 clusters | +0.243 | −0.174 (−0.417) | +0.475 (+0.232) |
| F2 blue/disc lenses | +0.003 | −0.820 (−0.824) **DAMAGE** | +0.375 (+0.372) **DAMAGE** |
| F3 SPARC small | +0.059 | −0.200 (−0.259) **DAMAGE** | +0.231 (+0.171) **DAMAGE** |
| F4 SPARC large | +0.001 | −0.120 (−0.120) **DAMAGE** | +0.090 (+0.089) **DAMAGE** |

All values are in dex.

- Median element shifts under R2-A:
  - dwarfs +1.02 dex;
  - SPARC points +0.09;
  - blue lens bins +0.38 to +1.23;
  - red lens bins +0.32 to +1.29;
  - clusters +0.12 to +1.77.
- On the canonical footing the cluster excess is the only excess fact R2-A reduces (by 0.069 dex). On the alt footing it overshoots.
  The rotators break in every case. **R2 WORSENS on both footings; so does R2-B.**
- Diagnostic R2-S (no class; needs a supply). Suppose a bound cold surplus existed and sourced the law (H-LINK / coupling G on the
  surplus only). Then the surplus needed per dwarf would be smaller than under Newtonian addition (class A):
  - canonical: ×4.73 (16–84%: 2.96–10.1; 67 dwarfs with an excess);
  - alt: ×5.45 (3.40–11.9).

  CFG888 found that no record formulation writes this coupling, and CFG880/884 found that no single clump fits all dwarfs. So R2-S
  only changes how much cold mass a future supply rule must deliver.

## R3: the sign of the EFE

**Forms and inputs.**
- E1, the record's coded form (CFG883 / CFG919 V4): g = g_N,i ν((g_N,i + g_N,e)/a0).
- E2, 1-D QUMOND subtraction (bracket).
- Host field: Newtonian MW (6e10 M_⊙; bracket 8e10) + M31 (1e11 M_⊙; bracket 1.5e11) at LVD distances, vector-summed.
- Satellites: < 300 kpc from MW/M31, 72 of the 83. Field: 11.
- K7 confirms that E1 and E2 bracket the exact linear QUMOND boost ν_e(1 + L_e/3) in the EFE-dominated limit.

| canonical | satellites' mean EFE shift (median, max) | field mean shift | F0 | CFG874 c (isolated − satellites) | CFG874 class |
|---|---|---|---|---|---|
| E0 none (baseline = record) | 0 | 0 | +0.372 | −0.100 ± 0.091 | UNDECIDED |
| **E1 nominal** | **+0.480 (+0.417, +1.335 Boötes III)** | +0.025 | **+0.654 (+0.282) WORSENS** | **−0.284 ± 0.105** | PARTIAL* |
| E1 bracket masses | +0.530 | +0.035 | +0.688 | −0.309 ± 0.105 | PARTIAL* |
| E2 nominal | +0.710 | +0.120 | +0.834 | −0.370 ± 0.101 | PARTIAL* |
| E2 bracket masses | +0.762 | +0.141 | +0.874 | −0.390 ± 0.100 | PARTIAL* |

All values are in dex.

\*CFG874's own class "PARTIAL" means that isolated dwarfs carry part of the satellites' excess but significantly (≥ 2 se) less.
It is not this lane's grade.

The alt footing gives the same shifts within 0.01 dex: E1 F0 +0.332 → +0.616, c −0.285 ± 0.105.

**Reading.**
- The framework's EFE lowers the law's prediction for every satellite. The largest shifts are for close ultra-faints:
  - Boötes III, +1.34 dex at 47 kpc;
  - Tucana II, +1.25;
  - Tucana IV, +1.25;
  - Segue 1, +1.07;
  - Ursa Major II, +0.97.
- Including it raises the satellites' mean excess from +0.49 to +0.97 dex. Field dwarfs barely move.
- It also turns CFG874's satellite–field comparison from UNDECIDED into "satellites significantly above field dwarfs" (c −0.28 to
  −0.39). The satellite problem gets larger and more satellite-specific.
- Removing the EFE is the record's current choice: the class-A round rule uses only the region's own baryons (CFG888 Q1), and CFG478
  gives the material reading. The baseline is already the lenient one, so there is nothing left to gain from it.
- This confirms the sign already noted by CFG838/CFG842/CFG884, now with numbers.

## Controls

| control | result |
|---|---|
| K1 | CFG919 exec'd read-only (via CFG921): 7/7 of its checks pass, including CFG828 exact and CFG914's 9 |
| K2 | CFG921 prefix exec'd read-only: its K1–K4 and K6 pass (5/5). obs_struct and the fact operators were extracted by AST |
| K3 | CFG921's observed facts F0–F8b (value and se) reproduced on both footings: max diff 0 (F0 +0.856 ln = +0.372 dex) |
| K4 | Wolf path: CFG880 σ_law for 83 × 2 (2e-16); own gas copy = CFG880 gas_in (0); CFG828's 29 rows and its out-of-range mean +0.438 dex (0) |
| K5 | Jeans solver: Newtonian Plummer aperture ⟨σ²⟩ for X = 0.1…∞, L(<X), virial identity (β 0.5 / OM / 0.9), deep-law σ⁴ = (4/81)GMa0. Max rel error 1.2e-5 (bar 1e-2). ⟨σ²⟩(<a) = 0.126929 GM/a, equal to the analytic value |
| K5x (post-freeze diagnostic, not a gate) | the anisotropic R_e aperture weight against a direct line-of-sight projection (Newtonian Plummer β 0 / 0.5 / OM; Antlia II law field β 0.5 / OM): 3.9e-5. Added after the first main run because R1's corner classes rest on β ≠ 0 at R_e. The main run was repeated with it; no number changed |
| K6 (A1 tolerance) | R2 residual ratio 0.11 ≤ 1 (relative 1.5e-10, floating-point limited near the floor). h monotone above the floor. Newtonian limit 1e-8 (ν_e). R2-0: ν > 1 everywhere, iteration runs away |
| K7 | g_e → 0 gives the isolated law exactly. EFE limits at y_e = 0.05: E1 4.991 ≥ exact linear QUMOND 4.249 ≥ E2 2.764. CFG874's primary c, se, E, se reproduced exactly at E0. The EFE-limit numerics agree to 3e-8 |
| MUTATE M1 (R1 β = 0.9) | F0_J −0.150 dex, both footings: **BITES** |
| MUTATE M2 (a0 × 10) | R1 F0_J −0.49 dex and R2-A ΔF0 −0.50 dex, both footings: **BITE**. R3-E1 ΔF0 +0.009 / +0.008 dex: **TOOTHLESS (flagged)**. The deep-regime EFE ratio ≈ √(g_i/(g_i + g_e)) does not depend on a0. |
| MUTATE M3 (host masses × 10) | satellite mean EFE shift +0.36 dex, both footings: **BITES**. The R3 statistic responds to the EFE amplitude, so the R3 class does not rest on a dead statistic |

The MUTATE run exits 3 by design whenever one tooth is toothless (here M2 for R3).

## Limitations

- **R1:**
  - spherical, Plummer stars only; dSph ellipticity and real surface-density profiles are not modelled;
  - gas is treated as the record's spherical enclosed mass;
  - the observed σ's true aperture and member weighting are unknown. R_e and global bracket it, and the global aperture is probably
    closer to multi-R_e member samples;
  - binaries and non-equilibrium are not modelled.
- **R2:**
  - algebraic / spherical forms; clusters use CFG921's "ΔΣ excess ≈ g excess per band" convention;
  - R2-A's floor would also act on the Solar System's outskirts and on cosmology. That is not assessed here, because the galaxy
    rotators already break it.
- **R3:**
  - host fields are baryonic point masses with present-day distances; LMC, M33 and NGC hosts are omitted (a lower bound on g_e for
    their satellites);
  - E1 / E2 bracket the exact QUMOND only in the EFE-dominated limit;
  - no orbit history.
- Early-type galaxies with stellar dynamics: NOT TESTED (no lane input).
- No sealed prediction: nothing RESOLVES.

## Reproduce

One core, `nice -n 10`, peak RSS ≤ 290 MB (`/usr/bin/time -l`), ~5 s each, nothing downloaded:
- `CFG925_KONLY=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg925.py` → `cfg925_K.out`, `cfg925_results_K.json` (exit 0)
- `CFG925_MUTATE=1 ...` → `cfg925_MUTATE.out`, `cfg925_results_MUTATE.json` (exit 3: one toothless tooth, flagged above)
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg925.py` → `cfg925.out`, `cfg925_results.json` (exit 0)

Other lanes' code (CFG921 prefix and helpers, CFG919, CFG914, CFG880, CFG883, CFG874) is exec'd read-only, with open() for writing
refused during the whole run. No other lane's file was edited.
