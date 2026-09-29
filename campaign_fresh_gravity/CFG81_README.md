# CFG81 — a ΛCDM comparator for CFG34's X-ray groups: is B's R2500 shortfall specific to B?

- **Criteria:** frozen before any script or ΛCDM prediction existed, in `CFG81_FROZEN_CRITERIA.md` (27b4bf414).
- **Script:** `CFG81_lcdm_xray_groups.py`, about 4 s.
  - It executes CFG34's pipeline read-only, and h7 through it, up to CFG34's H3 banner. CFG34's own MUTATE is forced off and writes are refused.
  - FB, RHO_C and `halo_mass` come from CFG45's prefix, exactly as CFG69 obtains them.
  - CFG69's `c_duffy_full`, `c_duffy_relaxed`, `c_dm` and `make_nfw` are copied verbatim.
- **Outputs:** `.out` / `_results.json` and the `_MUTATE` pair.
  - The main run **exits 0**: 15/15 checks pass.
  - The MUTATE control (every ΛCDM concentration × 0.1) **exits 1**: C5 and H1 fail.

## Bottom line

**B's shortfall inside R2500 is SPECIFIC-TO-B, on both footings.** A standard NFW halo was given the same baryons, the Duffy+2008 concentration, and each group's hydrostatic mass at R500. It predicts the mass inside R2500 to within 5%: M_HSE/M_Λ = **1.05 (+0.020 dex, +0.25σ)**. B is **1.88× short** there (**2.57σ canonical, 2.63σ alt**).

- **This is a shape test, not a full prediction.**
  - The lane's stellar masses are computed from the hydrostatic M500, so a halo mass inferred from them would be circular.
  - So ΛCDM is handed each group's mass at R500, and B is not.
  - **At R500 the comparison is NOT TESTED.** The lane's data contain no non-circular ΛCDM prediction there.
- **The test discriminates.** With every concentration × 0.1, the ΛCDM gate fails at +3.30σ. The MUTATE flipped it, so the class is not NON-DISCRIMINATING.
- **The class does not move.** Every declared variant gives it, with offsets from −0.044 to +0.100 dex and |z| ≤ 1.23. So does the error model with the hydrostatic allowance removed from both sides: R6, added after the first run, puts ΛCDM at 1.21σ and B at 3.83 / 4.06σ.
- **On equal terms, B's shape is also off, but within 2σ.** Normalised at R500 the way ΛCDM is, B's profile shape alone is short by +0.126 / +0.161 dex (1.37 / 1.79σ); ΛCDM's is short by +0.020.
  - So B's R2500 shortfall is roughly its R500 deficit (+0.150 / +0.124 dex, the baryons the groups have lost) plus a shape deficit of similar size. Medians do not add exactly.

This does not say the data favour ΛCDM, which was given each group's R500 mass. It says that a standard halo shape is not short where B is.

## Results

| | B canonical (CFG34) | B alt (CFG34) | **ΛCDM (shape design)** | class |
|---|---|---|---|---|
| **R2500**: M_HSE/M_model | 1.88 (+0.275 dex) ± 0.107 → **+2.57σ**, FAIL | 1.88 (+0.274) ± 0.104 → **+2.63σ**, FAIL | **1.05 (+0.020) ± 0.081 → +0.25σ** | **SPECIFIC-TO-B** (both footings) |
| **R500** | 1.41 (+0.150) ± 0.084 → +1.80σ (MARGINAL; a CFG34 pass) | 1.33 (+0.124) ± 0.083 → +1.49σ | 1.00, by construction | **NOT TESTED** |
| B − ΛCDM at R2500 | +0.255 dex | +0.254 dex | | |

- **Error components at R2500:**
  - ΛCDM: groups 0.016, stars 0.003, hydrostatic allowance 0.079.
  - B: groups 0.017 / 0.016, stars 0.070 / 0.066, allowance 0.079.
- **ΛCDM has no a₀,** so it gives one set of numbers for both footings.
- **The ΛCDM model:** M_Λ(<r) = M_b(<r) + (1 − f_b) M_NFW(<r).
  - M_b is the lane's own gas and stars, identical to B's.
  - f_b = 0.1571.
  - M_200c is solved per group so that M_Λ(<R500) = M500_HSE at the measured R500.
  - c = Duffy full 200c at z = 0: 3.96–4.69, median 4.42.
  - Every overdensity is taken in the data's own critical density, 3 M500 / (4π · 500 · R500³).
  - The prediction is made at the measured R2500.

**The variants at R2500** (reported only; none changes the class):

| variant | M_HSE/M_Λ | offset (dex) | z | median c | class |
|---|---|---|---|---|---|
| **base** (Duffy full 200c) | **1.05** | **+0.020** | **+0.25** | 4.42 | **SPECIFIC-TO-B** |
| V1 Dutton–Macciò c | 0.98 | −0.008 | −0.10 | 5.53 | SPECIFIC-TO-B |
| V2 Duffy relaxed 200c | 1.00 | +0.002 | +0.02 | 5.10 | SPECIFIC-TO-B |
| V3 R500 normalisation × 1.2 (a 20% differential hydrostatic bias) | 0.90 | −0.044 | −0.55 | 4.31 | SPECIFIC-TO-B |
| V4 R500 normalisation × 0.8 | 1.26 | +0.100 | +1.23 | 4.55 | SPECIFIC-TO-B |
| V3u M500 and M2500 × 1.2 (a uniform bias) | 1.08 | +0.035 | +0.43 | 4.31 | SPECIFIC-TO-B |
| V4u M500 and M2500 × 0.8 | 1.01 | +0.003 | +0.04 | 4.55 | SPECIFIC-TO-B |
| V5 the total mass as one NFW (no separate baryons) | 1.03 | +0.011 | +0.14 | 4.46 | SPECIFIC-TO-B |
| V6 CFG45's RHO_C (H₀ = 67.4, z = 0) in the verbatim `make_nfw` | 1.06 | +0.025 | +0.31 | 4.42 | SPECIFIC-TO-B |
| RM the MUTATE's model (every c × 0.1) | 1.84 | +0.265 | +3.30 | 0.41 | gate FAILS |

**The other reported rows:**
- **R0, the circularity diagnostic.**
  - Every group's stellar mass is exactly the Kravtsov relation at its hydrostatic M500 (max deviation 0).
  - CFG69's Moster `halo_mass` at those group-total stellar masses gives 1.3–3.2 × 10¹⁵ M☉ for groups of 2.1 × 10¹³–1.4 × 10¹⁴ M☉. Ten of the 20 sit at the grid ceiling of 10^15.5.
  - No ratio to the data is formed from it.
- **R3, B's shape-only offset** (R2500 minus R500, per group): canonical +0.126 dex (+1.37σ), alt +0.161 (+1.79σ). ΛCDM's is +0.020 (+0.25σ).
- **R4, per group.**
  - B is short in all 20 groups at R2500: +0.125 to +0.458 dex canonical.
  - ΛCDM's offsets lie from −0.186 to +0.080 dex, 14 of 20 positive.
- **R5, the concentration each group's own M2500/M500 implies** for a single total-mass NFW.
  - The median is 4.95 (range 1.44–7.38), against Duffy's 4.49 at the same M_200c. Thirteen of the 20 lie above Duffy, and all 20 have a solution.
  - Four groups with M2500/M500 ≤ 0.29 (S0753, S0805, IC1633, IC1262) imply c = 1.4–2.4. They carry ΛCDM's four largest over-predictions of the inner mass (−0.09 to −0.19 dex).
- **R6 (added after the first runs; reported only):** with the 0.079-dex allowance removed from both sides, ΛCDM sits at +1.21σ and B at +3.83σ (canonical) and +4.06σ (alt). The class is still SPECIFIC-TO-B.

## Controls (all passed in the main run; none failed)

- **C1:** CFG34's committed B numbers are reproduced through the read-only exec.
  - The RES entries match to max |d| = 0.
  - The four printed result lines are identical character for character.
  - CFG34's own C1, C2 and H1 pass and its H2 fails, as committed.
- **C2:** the NFW engine.
  - M(<R_200c) = M_h to 2.2e-16.
  - The lane's `nfw_M` equals CFG69's verbatim `make_nfw` exactly.
  - The 200c → 500c / 2500c fixed-point conversion equals a direct brentq root solve to 3.6e-14 over 84 conversions, including c × 0.1.
  - M(<r) equals the integral of the NFW density to 2.2e-15.
- **C3:** in every group, the critical density implied by (M500, R500) and by (M2500, R2500) agree to 0.87%. It lies 1.020–1.085 × CFG45's RHO_C (median 1.078).
- **C4:** every ΛCDM run is normalised at the measured R500 to 7.7e-15.
- **C5:** the base's c equals `c_duffy_full` at the solved M_200c exactly.
- **C6 (MUTATE run only):** the MUTATE's base equals the main run's RM row exactly (|d| = 0).

## MUTATE

**Every ΛCDM concentration is multiplied by 0.1** (c = 0.37–0.44). B is not mutated, and C1 still passes.

- **H1 failed:** +0.265 dex, **+3.30σ**, against the main run's +0.020 (+0.25σ). The gate **flipped**, so **the MUTATE is informative** and the class is not NON-DISCRIMINATING.
  - The shift (+0.245 dex) matches the pre-freeze hand estimate of 0.25–0.3 dex.
- **C5 failed by construction.** It is the mutation detector that guarantees exit 1.
- **The failing sets differ:** the main run fails nothing, and the MUTATE fails {C5, H1}.

## Caveats

- **What is tested.** The shape design hands ΛCDM each group's R500 mass. It tests only the concentration–mass relation, together with the lane's baryons, between R500 and R2500. At R500 nothing is tested.
  - B's test is harder, because B predicts both radii from the baryons.
  - The class says a standard halo shape is not short where B is. It does not say that ΛCDM predicts these groups' masses.
- **Circularity.** The lane's only stellar mass comes from the hydrostatic M500, so CFG69's Moster-based base could not be used.
  - The lane has no central-galaxy mass. Moster's relation is for centrals, and fed the group totals it lands at 10¹⁵ M☉ (R0).
- **No adiabatic contraction.** Contraction would add dark mass inside R2500 and move ΛCDM's offset down, toward over-prediction. Feedback-driven expansion would move it the other way. Neither is scored.
- **No concentration scatter.** Only the mean relation is used. The groups' own implied concentrations span 1.4–7.4 (R5). The scatter enters only through the group-to-group error (0.016 dex).
- **The concentration relation.** The z = 0 Duffy row is used, although the groups sit at z ≤ 0.034 (a ≤ 1.6% effect in c). The Dutton–Macciò and relaxed rows move the offset by −0.028 and −0.018 dex.
- **Hydrostatic bias.**
  - The 0.079-dex allowance is almost all of ΛCDM's error. It is generous here, because a uniform bias cancels from a shape test (V3u / V4u: +0.035 / +0.003).
  - A 20% differential bias between the two radii moves the offset from −0.044 to +0.100 dex (V3 / V4).
  - Without the allowance the class still holds (R6).
- **The imported stars** are the same on both sides. ΛCDM's stellar term is 0.003 dex because the R500 normalisation absorbs it; B's is 0.070.
- **The ρ_c convention.** The data's own critical density is about 8% above CFG45's RHO_C. With CFG45's value (V6) the offset is +0.025 instead of +0.020.

## Disclosures

- **Known before freezing,** and listed in the frozen file:
  - CFG34's numbers;
  - the full data table, printed while h7 was read;
  - the data's implied critical density;
  - two feasibility execs, which computed no ΛCDM number;
  - two hand estimates: the top of the Moster grid, and a generic NFW mass ratio at c ≈ 4.5 and c ≈ 0.45, which anticipated the MUTATE's shift.
- **Code edits before the first run** (the script had not yet run):
  - removed a leftover no-op expression in the JSON write;
  - set the fixed-point stopping rule to 4e-16 relative, so it stops within an ulp instead of cycling (C2 still compares at 1e-9);
  - labelled the class line in the MUTATE run;
  - guarded R5 against an empty list.
- **Added after the first runs, reported only: R6.** Nothing else changed. The check outcomes, the ΛCDM numbers and the class are identical to the first main run (14/14) and the first MUTATE run (13/15, failing C5 and H1).
- **Beyond the frozen list** (cosmetic): R4 also prints M2500, and C2(i) also checks the verbatim `make_nfw` at RHO_C.
- **No other file was edited.**

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.
