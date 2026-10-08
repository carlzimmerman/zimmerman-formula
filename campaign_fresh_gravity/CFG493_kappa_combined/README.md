# CFG493: kappa measured from three independent routes. CONSISTENT WITH 1/2 BUT NOT DISCRIMINATING on both footings; the 2-3% goal cannot be reached with present calibrations

Criteria `adffc0550` were committed alone before any script existed. Script: `cfg493_kappa_combined.py` (about 8 s; `--mutate` for the MUTATE run). κ = ½ is FITTED; here κ is MEASURED, never derived. Both footings are reported. No dark-matter particle; the cold mass is still required. On-disk data and committed results only; nothing was fetched.

## Bottom line

- **Combined a₀ = 7.81 × 10⁻¹¹ m s⁻² (log −10.107 ± 0.099 dex).**
  - Canonical footing (ρ_Λ): **κ = 0.417 ± 0.095**.
  - Alt footing (ρ_crit): **κ = 0.345 ± 0.078**.
- **Verdict as frozen: CONSISTENT BUT NOT DISCRIMINATING on both footings.**
  - Canonical: ½ sits at 0.80σ. 1/√π is at 1.33σ, 0.6 at 1.60σ, Milgrom's cH₀/2π at 1.27σ and cH_Λ/2π at 0.44σ. None of them is excluded.
  - Alt: ½ sits at 1.63σ. 1/√π (2.17σ) and 0.6 (2.44σ) are beyond 2σ, but Milgrom's form (1.27σ) is not.
  - The central value leans below ½ on both footings. That is a lean, not a detection.
- **The power label was NOT POSSIBLE before any central value was printed.** The combined error is 0.099 dex, which is 25% in κ. Separating ½ from 1/√π at 2σ needs 0.026 dex, and separating it from every candidate needs 0.018 dex.
- **The 2-3% goal is out of reach with present calibrations.** Set every route's own error to zero and the shared systematics alone still leave **0.0385 dex (9.3%)**. The goal needs 0.009-0.013 dex.
- **Dominant term (frozen rule): statistics**, by a hair. Removing it cuts σ by 0.0134 dex; removing the **shared gas-mass scale** cuts it by 0.0126 dex.
  - The gas scale is the largest *systematic*, and it alone sets the 9% floor.
  - The kernel is the law-definition term. Switching ν_mono to the quadrature form moves every route by +0.06 to +0.09 dex (κ_Λ 0.417 → 0.489). That is more than the whole ½ vs 1/√π gap (0.052 dex).
- **The routes agree only because their errors are large.** P1 and P3 sit 0.29 dex apart (consistency p = 0.37 at the real errors). At 2.5% errors the same central values would be inconsistent at p ~ 10⁻⁶⁷.

## Routes (all on ν_mono, single-dish flux scale, Hubble-flow distances at H₀ = 67.4)

| route | N gal | log a₀ ± total | κ_Λ | κ_crit | GLS weight |
|---|---|---|---|---|---|
| P1 SPARC gas-dominated points, ladder (TRGB/Cepheid) distances | 12 | −10.015 ± 0.141 | 0.516 ± 0.167 | 0.427 ± 0.138 | 0.41 |
| P2 MeerKAT MIGHTEE-HI widths (rest frame), ALFALFA flux scale | 47 | −10.081 ± 0.151 | 0.444 ± 0.154 | 0.367 ± 0.128 | 0.34 |
| P3 WALLABY DR2 gas points (re-fitted here on ν_mono) | 46 | −10.302 ± 0.171 | 0.266 ± 0.105 | 0.220 ± 0.087 | 0.24 |
| **combined (GLS, shared terms modelled)** | | **−10.107 ± 0.099** | **0.417 ± 0.095** | **0.345 ± 0.078** | |

**Error budget per route** (dex in log a₀; a shared term is listed as |lever| × prior σ):

| term | P1 | P2 | P3 |
|---|---|---|---|
| statistics (bootstrap) | 0.090 | 0.033 | 0.104 |
| route-specific reduction | 0.089 (rotation curves: SPARC vs LITTLE THINGS on the same dwarfs) | 0.101 (width recipe: δ and HI-size relation) | 0.094 (distance frame: Hubble flow vs CMB table) + 0.059 (AD / R_d / EFE) |
| flux-tie transfer | 0.027 | 0.090 | 0.035 |
| ladder zero point | 0.022 | — | — |
| **S_gas** (gas-mass scale, 11.5%, shared) | 0.050 | 0.040 | 0.057 |
| S_star (stellar zero point, 17%, shared) | 0.014 | 0.019 | 0.008 |
| S_HF (Hubble-flow scale, ±½ the Planck–SH0ES gap, shared) | 0 | 0.038 | 0.040 |

- **Measured levers** (dex of a₀ per dex):
  - gas: −1.05 (P1), −0.84 (P2), −1.21 (P3);
  - stars: −0.21, −0.28, −0.11;
  - Hubble-flow distance scale: 0, +2.17, +2.28.
- **I2 (M/L-insensitivity) passes for all three routes:** 0.014, 0.019 and 0.008 dex for a ±17% stellar scale.

**Flux tie.** Every route was moved to the single-dish (ALFALFA) scale:
- P1: SPARC M_HI sits 0.053 dex above ALFALFA (CFG306 P6). Correcting for it moves P1 by +0.053.
- P2: the MIGHTEE catalogue holds 0.64× the Arecibo flux (CFG304). Correcting moves P2 by −0.163, from 1.21 to 0.83 × 10⁻¹⁰.
- P3: keeps WALLABY's own catalogue correction.

**P3 is new in this lane.** It re-implements p43 and reproduces p43's 7.282e-11 (quadrature, H₀ 73) and 6.667e-11 (H₀ 70) exactly. On the framework kernel at H₀ 67.4 it gives 4.99 × 10⁻¹¹, the lowest of the three routes. Its distance frame alone is worth ±0.09 dex.

## Controls and MUTATE

- **Main run: 12/12 pass.**
  - K1: footing identities.
  - K2a-d: reproductions of CFG449, CFG306, CFG304 and p43, all exact.
  - I2 ×3.
  - K3 coverage: mean pull +0.006, SD 0.994, P(p < 0.05) 0.0545.
  - K4: GLS sanity.
- **The JSON is byte-identical on a re-run.**
- **MUTATE** (+10% injected into P1, the route with the largest weight): **13/14 pass, with one load-bearing FAILURE, kept.**
  - **M1 pass:** L̂ moves by exactly w × 0.04139 = +0.0172.
  - **M2 (reported):** at the real errors the +10% shift is **not flagged** (p 0.28). P1 sits only +1.08σ from the other two. **A 10% error in one route is invisible today.** This is the power statement, not a failure.
  - **M3 FAIL:** the frozen precision world (route errors 2.5%, shared σ 0.005 dex) gives p = 0.055 with the injection, against < 0.05 required. Without the injection it gives p = 1.
    - The cause is the design of the check. The frozen 0.005 dex shared σ is multiplied by levers up to 2.3, and S_HF acts on P2 and P3 but not on P1. So the realised differential shared term is about 0.011 dex, not 0.005.
    - **Post hoc, print-only, not a check:** scaling the shared σ so that |lever| × σ ≤ 0.005 gives p = 0.013; with the shared terms off, p = 0.007. The machinery flags the tension once the world really is at 2-3%.

## Variants (reported, never the verdict)

| variant | log a₀ ± σ | κ_Λ | κ_crit | canonical / alt |
|---|---|---|---|---|
| V1 SPARC = estimator C | −10.115 ± 0.065 | 0.410 | 0.339 | not discr. / INCONSISTENT |
| V2 SPARC = estimator A | −10.100 ± 0.061 | 0.425 | 0.352 | not discr. / INCONSISTENT |
| V3 quadrature kernel | −10.039 ± 0.099 | 0.489 | 0.405 | not discr. / not discr. |
| V4 no flux tie | −10.031 ± 0.091 | 0.497 | 0.412 | not discr. / not discr. |
| V5 P2 flux offset −0.087 | −10.073 ± 0.099 | 0.451 | 0.373 | not discr. / not discr. |
| V6 HF distances at H₀ 73.04 | −10.062 ± 0.099 | 0.463 | 0.383 | not discr. / not discr. |
| V7 footing rebuilt at 73.04 | −10.062 ± 0.099 | 0.427 | 0.354 | not discr. / not discr. |
| V8 + KiDS late-type rows | −10.065 ± 0.088 | 0.459 | 0.380 | not discr. / not discr. |
| V9 no P1 reduction term | −10.083 ± 0.089 | 0.442 | 0.366 | not discr. / not discr. |
| V10 uniform half-widths | −10.094 ± 0.085 | 0.430 | 0.356 | not discr. / not discr. |
| V11 P1 = CFG397 anchor | −10.047 ± 0.096 | 0.479 | 0.396 | not discr. / not discr. |

- **No variant discriminates on the canonical footing.**
- **V1 and V2 return INCONSISTENT on the alt footing, but their errors are optimistic.** Estimators A and C were given no shared gas lever, so their gas term is treated as independent of P2 and P3. They are also M/L-entangled, which is why the criteria exclude them.

**Report-only rows** (κ_Λ / κ_crit):
- SPARC estimator A: 0.450 / 0.373;
- SPARC estimator B: 0.584 / 0.483;
- SPARC estimator C: 0.434 / 0.359;
- SPARC Hubble-flow gas points: 0.353 / 0.292 at H₀ 73, and 0.301 / 0.249 at 67.4;
- KiDS late-type: 0.835 (z 0.2) and 0.341 (z 0.4);
- KiDS early-type: 1.2-2.3, class-inconsistent;
- PAPER43 pool: 0.444 / 0.368;
- Desmond 2023: 0.636 / 0.526.

## What would cut the error

1. **Statistics and the P1 reduction term (12 galaxies).** More gas-dominated discs with TRGB or Cepheid distances and per-radius mass models would cut both. BIG-SPARC, once released, plus TRGB matching is the realistic source. A decision is also needed on which reduction of the same dwarfs is right (SPARC or LITTLE THINGS, which differ by 0.16-0.20 dex).
2. **The gas-mass scale, which sets the floor.** No sample size removes it. Getting below 9% needs:
   - an absolute HI flux scale good to about 3%, for example single-dish re-observation of the same MIGHTEE and WALLABY gas-dominated galaxies;
   - a measured molecular and CO-dark gas fraction in gas-dominated dwarfs.
   Even with the gas and stellar scales both known to 5%, the MNRAS floor formula gives 3.5%.
3. **WALLABY's distances.** TRGB distances for the WALLABY gas dwarfs would remove the ±0.09 dex Hubble-flow vs CMB-frame term and the S_HF lever.
4. **The kernel.** A 2-3% statement about κ is only meaningful once the kernel is fixed. The quadrature form moves κ_Λ by +17%.

## Hand estimates (before running)

- HE1 hit: P1 −10.015 against −10.03 ± 0.13.
- HE2 hit: P2 −10.081.
- HE3 hit: P3 −10.302 against about −10.25 ± 0.1.
- HE4 hit: −10.107 ± 0.099 against −10.10 ± 0.08.
- HE5 hit: NOT POSSIBLE.
- HE6 hit: CONSISTENT BUT NOT DISCRIMINATING.
- HE7 miss: statistics edges out S_gas by 0.0008 dex.
- HE8 hit: M2 not flagged.

## Disclosures

- **The inclusion rules were written after the route-level numbers had been read.** Criteria section 0 lists them. The KiDS and LITTLE THINGS exclusions follow their own lanes' failed controls, and V8 shows KiDS included anyway.
- **P2 is built from committed CFG306 numbers, not re-run.** The HI-flux lever comes from the k = 0 gas-only grid at H₀ 70 and is applied to the H₀ 67.4 base, which assumes the lever does not depend on H₀. The width recipe's δ and D_HI terms are taken as 1σ.
- **P3's EFE term is half of p43's committed shift**, which was computed with the quadrature-law cubic, not ν_mono.
- **The S_HF prior treats the ladder (P1) and the Hubble-flow routes as uncorrelated.** In reality the ladder zero point and the local H₀ are linked.
- **Ladder distance errors are not propagated galaxy by galaxy** (CFG397's statistic).
- **The MUTATE post-hoc lines were added after M3 failed.** They are print-only; the frozen check and its FAIL stand.

## Files

- `FROZEN_CRITERIA.md`;
- `cfg493_kappa_combined.py`;
- outputs: `cfg493_kappa_combined.out` and `_results.json`; `cfg493_kappa_combined_MUTATE.out` and `_MUTATE_results.json`.
