# CFG590: the framework's matter power against cosmic shear, with the same feedback on both models. Verdict: EXCLUDED on both footings (VARIANT-SENSITIVE: emergent edge); ΛCDM-dark-matter-only + the same feedback: CONSISTENT

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (018145c76). Date: 2026-10-10.
- **Scripts:**
  - `cfg590_shear.py` (about 2 min): `OMP_NUM_THREADS=2 nice -n 10 python3 cfg590_shear.py` writes `cfg590_shear.out` and `cfg590_results.json`. `CFG590_MUTATE=1` writes `_MUTATE.out` / `_MUTATE.json` and exits 1 when all teeth bite.
  - `cfg590_posthoc.py` (post-hoc, NOT a verdict input): redshift scaling of the excess and HMcode extrapolation → `cfg590_posthoc.out` / `.json`.
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 are never pooled; flat a0 = κ c √(G ρ_DE); ν_mono; candidate B. The cold energy's MASS is still required; no particle species. Not "theory closed". Nothing was downloaded; other lanes were read only.
- **Method.** P_X(k, z) = R_X(k) · S_fb(k, z; T) · P_NL(k, z). P_NL is CAMB 1.6.6 HMcode-2020 dark-matter-only (CFG556's cosmology, σ8 = 0.811). S_fb is the HMcode-2020 BAHAMAS-calibrated feedback suppression at log T_AGN = T. It is applied identically to ΛCDM (R ≡ 1) and to the framework (R from CFG556/557/559, z = 0). The effective A_mod is fitted in the data's own form P = P_L + A (P_NL − P_L), through a Limber C_ℓ (ℓ 100–2000; KiDS-like and DES-like n(z) and noise; M1). The CFG526 k = 1, 2, 4 average (M2) is a cross-check. Data, recalled and PROVISIONAL: KiDS-1000 A_mod 0.858 ± 0.052 (Amon & Efstathiou 2022); DES Y3 0.82 ± 0.04 (Preston, Amon & Efstathiou 2023).
- All numbers below come from `cfg590_results.json` / `cfg590_posthoc.json`.

## The answer

**ΛCDM's dark matter alone has too much small-scale power for the shear data.** It has A = 1 against 0.858 / 0.82, so Z = +2.73 (KiDS) and +4.50 (DES). Realistic feedback fixes that. BAHAMAS-like feedback reaches Z = 0 at log T_AGN 7.99 (KiDS) and 8.13 (DES), i.e. S_fb(k = 1, z = 0.5) ≈ 0.90 / 0.88. That is inside the calibrated range (7.3–8.3) and at the edge of the fiducial band (7.6–8.0). So the owner's point stands: the data are not featureless ΛCDM, and the fair comparison applies feedback.

**The framework runs the opposite way.** Its halos ADD small-scale power (R > 1 at k 0.2–3) where the data want LESS. The same feedback cannot remove the excess on top of the deficit the data already ask for.

**Effective A_mod (M1; KiDS / DES):**

| model | feedback off | T 7.6 | T 7.8 | T 8.0 | T 8.3 | ΔA vs ΛCDM (off) |
|---|---|---|---|---|---|---|
| ΛCDM (R = 1) | 1.000 / 1.000 (Z +2.73 / +4.50) | 0.948 / 0.948 | 0.906 / 0.906 | 0.854 / 0.854 | 0.783 / 0.782 (Z −1.45 / −0.94) | — |
| canonical, PRIMARY (CFG559 kinetic) | 1.305 / 1.302 (Z +8.59 / +12.05) | 1.241 / 1.238 | 1.188 / 1.186 | 1.123 / 1.121 | 1.033 / 1.031 (Z +3.36 / +5.27) | +0.305 |
| alt, PRIMARY | 1.455 / 1.452 (Z +11.47 / +15.80) | 1.382 / 1.380 | 1.323 / 1.321 | 1.251 / 1.249 | 1.152 / 1.150 (Z +5.65 / +8.24) | +0.455 |

The A_mod form amplifies R − 1: A − 1 ≈ (R − 1) P_NL/(P_NL − P_L), so R(1) = 1.29 becomes A ≈ 1.30.

**Variants (M1, class over T 7.3–8.3; min Zmax in brackets):**

| R input | canonical | alt |
|---|---|---|
| CFG559 kinetic (PRIMARY) | EXCLUDED (5.27) | EXCLUDED (8.24) |
| CFG559 full supply + kinetic | EXCLUDED (9.11) | EXCLUDED (13.16) |
| CFG557 α-free supply (sharp) | EXCLUDED (8.50) | EXCLUDED (11.62) |
| CFG556 census edge (sharp, full supply) | EXCLUDED (11.69) | EXCLUDED (16.30) |
| CFG556 emergent edge | CONSISTENT (1.76; A 0.78 with no feedback, too LOW at strong feedback; a mapping systematic changes the class → NOT DIAGNOSTIC) | CONSISTENT (0.41; M2 TENSION → NOT DIAGNOSTIC) |
| CFG556 s25 / s55 / f_ret = 1 (reported) | EXCLUDED | EXCLUDED |
| CFG556 r200m scope (reported) | CONSISTENT (1.26, at T 7.3–7.6; A 0.80 even without feedback) | CONSISTENT (0.44) |

Only the variants with R ≤ 1 at k ≈ 1 survive: the emergent edge and the r200m scope. These are the variants that do not settle the whole turnaround catchment inside about r200m.

**S8-equivalent** (DMO ΛCDM with rescaled σ8 matching the M1-weighted C_ℓ amplitude; reported only; KiDS / DES 0.759, recalled):
- ΛCDM: 0.829 with feedback off, 0.811 at T 7.8.
- Framework canonical: 0.887 off, 0.867 at T 7.8.
- Framework alt: 0.913 off, 0.891 at T 7.8.

So the framework moves S8 up, away from the lensing values, by 0.06–0.08 more than ΛCDM.

## How much feedback each model needs (M1)

- **ΛCDM:** Z = 0 at log T_AGN 7.99 (KiDS) and 8.13 (DES). |Z| < 2 for T ∈ [7.9, 8.3] with both datasets. **That is within the hydro-sim range.**
- **Framework PRIMARY:** no crossing anywhere in the search range 7.0–9.0.
  - At the strongest calibrated feedback (8.3): Z = +3.36 / +5.27 (canonical) and +5.65 / +8.24 (alt).
  - Even at T = 9.0 (outside calibration; HMcode saturates there, S_fb(1, 0.5) = 0.822 vs 0.851 at 8.3, from `cfg590_posthoc.out`): Z = +2.06 / +3.54 (canonical) and +4.20 / +6.33 (alt).
  - **The feedback the framework would need is outside the hydro-sim family entirely.** It needs about 0.30 (canonical) / 0.45 (alt) more suppression in A than ΛCDM at the same T. At T 7.8 that is ΔA = +0.282 (canonical) / +0.417 (alt) on KiDS.

## Verdict (frozen rule, M1, full feedback range 7.3–8.3)

- **canonical: EXCLUDED** by cosmic shear. Zmax ≥ 3 at every T (minimum 5.27, set by DES at T 8.3). The class is unchanged under every declared mapping systematic: M2, ℓ_max 1000 / 3000, n(z) mean ±0.1.
- **alt: EXCLUDED.** Minimum Zmax 8.24; unchanged under all systematics.
- **VARIANT-SENSITIVE (both footings):** the CFG556 emergent edge (untruncated declared gas, edge 0.42–0.53 r_ta) is CONSISTENT under M1 on both footings, and NOT DIAGNOSTIC once the mapping systematics are included. That variant was not fitted, and its size is set by the declared outer gas shape (CFG556). All supply-based mainline variants (CFG557, CFG559 primary and full) are EXCLUDED.
- **ΛCDM-dark-matter-only by the same rule: CONSISTENT** with feedback in the calibrated range (|Z| < 2 at T 7.9–8.3, inside the fiducial band at 7.9–8.0), robust under all systematics. **With feedback off it is EXCLUDED** (Zmax 4.50, DES). That is the known A_mod / S8 deficit.
- **Plainly:** the framework's excess (A_eff 1.30–1.46 with no feedback) runs opposite to the data's deficit (0.82–0.86). The comparison is now fair: the same feedback that brings ΛCDM onto KiDS and DES leaves the framework 3–8σ high.

## Redshift caveat, checked as hard as the fail (post-hoc, not a verdict input)

R(k) was computed at z = 0 and taken as z-independent (frozen, disclosed). Cosmic shear weights lens planes at z ≈ 0.1–0.6, where fewer clusters exist. The excess is driven by log M_ta 14–15 one-halo power (CFG556 drivers).
- **Scaled family** R_s = 1 + s (R − 1):
  - canonical drops from EXCLUDED to TENSION below s = 0.64, and to CONSISTENT below s = 0.48;
  - alt drops below 0.43 and 0.33.
- **Crude estimate** (`cfg590_posthoc.py`): the ΛCDM share of P(k = 1) from M200m ≥ 1e14 falls to s(z) = 0.77 at z = 0.3 and 0.60 at z = 0.5. Lens-plane weighted, s_eff = 0.78 (KiDS) and 0.79 (DES), with the median lens plane at z ≈ 0.25.
- **So both footings stay EXCLUDED under that estimate.** The canonical margin is thin, 0.78 against 0.64; alt is robust. The estimate assumes the per-halo framework/ΛCDM profile ratio at fixed mass does not change with z. A halo model run at z = 0.3–0.5 through the CFG556/557/559 machinery would replace it.

## Controls and MUTATE

- **C1** CAMB σ8 = 0.81100: PASS. **C2** fit identity 0: PASS. **C3** ΛCDM A_eff decreases with T: PASS. **C4** max |R(1e-3) − 1| = 1.1e-6: PASS.
- **MU1** (framework R ≡ 1 reproduces ΛCDM's A, Z and class exactly): max |ΔA| = 0, class CONSISTENT = ΛCDM's: bites.
- **MU2** (feedback off gives ΛCDM A = 1 and the framework's featureless row): |A − 1| = 6.7e-16, row difference 0: bites.
- **MU3** (R = 0.5 at k ≥ 1, T 7.3): Z = −5.02 / −5.54, so the sign handling bites.

## Decisive data products (owner's go needed; NOT downloaded; sizes approximate, PROVISIONAL)

The A_mod mapping is a shortcut. A real shear likelihood would replace M1:
1. KiDS-1000 cosmic-shear release: COSEBIs / ξ± / band powers data vector, covariance and n(z) (KiDS website, about 10–50 MB).
2. DES Y3 cosmic-shear 2pt FITS file (ξ± with covariance and n(z)) (DES data release, about 50–150 MB).
3. A prediction code: pyccl (pip, about 50 MB) or CosmoSIS (larger, about 200 MB with standard library). CAMB is already installed and suffices for the Limber step.
4. Optional: A_mod posterior chains (Amon & Efstathiou 2022; Preston+2023) if public (tens of MB), to replace the recalled values.

## Disclosures (dated 2026-10-10)

- **Literature values are recalled and PROVISIONAL:** A_mod, S8, n(z) means, survey areas, n_eff and σ_e. The single-bin Smail n(z) stands in for the real tomographic n(z).
- **One feedback family** (HMcode-2020 / BAHAMAS) was used. The recalled van Daalen+20 / FLAMINGO forms were not used.
- **The framework's baryons are not re-modelled for feedback.** The identical S_fb is applied as instructed.
- **Halo-model double counting** (CFG556): the "ratio form" shrinks R − 1 by about 0.77 at k = 1, which is above the s thresholds (0.64 / 0.43). R for CFG557/559 exists only in the primary form.
- **R(k > 10) = R(10)** (0.45 for CFG556 sharp canonical). At ℓ ≤ 2000 this enters only at low z.
- **Code-path fix before the final run.** The first MUTATE run gave MU1 |ΔA| = 6.7e-16 (floating-point round-off from a separate ΛCDM code path) against the frozen "exactly". ΛCDM was then routed through the same R-interpolation path with R = 1, and main and MUTATE were rerun. No criterion was changed.
