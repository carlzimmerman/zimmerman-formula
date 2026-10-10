# CFG594 FROZEN CRITERIA: one quick check inside the halo-assumption audit

Date 2026-10-10. Committed alone, before the check script exists and before any number.

The lane is mainly an audit (`HALO_ASSUMPTIONS_AUDIT.md`, which needs no criteria). This file covers the one quick check whose numbers the audit cites as evidence.

Settings: κ = ½ FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) are judged separately and never pooled. Flat a0, candidate B. The cold energy's MASS is still required, with no particle species. This is not "theory closed". No PM runs and no downloads. Other lanes are read only.

## Question

The CFG556 halo-model excess is E = max(R − 1) over 0.05 ≤ k ≤ 1, giving +0.715 (canonical) and +0.883 (alt). How much of it moves when one inherited ingredient at a time is changed by a declared amount? The ingredients come in two groups: those inherited from ΛCDM and those inherited from standard MOND.

This is a SENSITIVITY check on a CONTEXT statistic. The owner rule of 10-10 already took the halo model out of verdicts, and this check gives it no verdict role. It ranks which inherited items could be driving the excess.

## Machinery (read only)

- Exec `../CFG556_halo_model_matter_power/cfg556_halo_model.py` up to its run marker (line 220), with literal text substitutions per variant.
- Then rebuild P_L,std, P_L,ta and the PRIMARY framework case exactly as CFG556's `summarize` does (edge `cen`, census f_ret, scope `ta`): R = 1 + (P_F,ta − P_L,ta)/P_L,std.
- Report E, R(0.35), R(1) and the σ8 ratio for each footing.

## Variants (one at a time; the magnitudes are declared here and not tuned afterwards)

**ΛCDM-inherited**

| id | change |
|---|---|
| L1 / L2 | Duffy08 c(M) normalisation × 0.7 / × 1.3. This changes both the NFW reference and M_ta. |
| L3 / L4 | Moster13 M* × 0.5 / × 2. Total retained baryons are unchanged; only the split between stars and gas moves. |
| L5 | σ8 0.811 → 0.76 in the linear spectrum. This changes the mass-function weights and the 2-halo term for both models. |
| L6 / L7 | Δ_ta 11.81 → 9.45 / 14.17 (× 0.8 / × 1.2). |
| L8 | Tinker08 mass function + Tinker10 bias → Press–Schechter f(ν) with Mo–White bias 1 + (ν² − 1)/δ_c. |
| L9 / L10 | census f_ret × 0.5 / × 2 (capped at 1). |
| L11 / L12 | catchment supply × 0.5 / × 0.75. The edge moves to r_M/ln(1 + f f_b/(s(1 − f_b))), and the remaining mass stays in the shell, so the mass inside r_ta is still conserved. |

**MOND-inherited**

| id | change |
|---|---|
| M0 | Control: the edge is solved numerically from point-mass supply exhaustion, M_b ν(G M_b/(r² a0)) = M_b + supply, using the RAR kernel. It must reproduce the closed form. |
| M1 | Kernel ν_simple = ½ + √(¼ + 1/y) in the profile and in the numerical edge. |
| M2 | Kernel ν_standard = √(½ + √(¼ + 1/y²)) in the profile and in the numerical edge. |
| M3 / M4 | A standard-MOND EFE in the 1-D approximation: g = ν(√(y_in² + y_ext²)) g_N, with y_ext = 0.01 / 0.03. The edge comes from numerical supply exhaustion with the same kernel, capped at r_ta. |

## Classification per variant (per footing, on ΔE = E_variant − E_CFG556)

- **DRIVER:** |ΔE| ≥ 0.25.
- **MODERATE:** 0.10 ≤ |ΔE| < 0.25.
- **MINOR:** |ΔE| < 0.10.
- **SIGN/CUT-SETTING** (an additional flag): E_variant ≤ +0.10, meaning the excess falls to or below CFG361's 10% cut.

An item counts as "able to remove the excess" only if one of its declared variants is CUT-SETTING on both footings.

## Controls

- **C0:** with no substitution, E reproduces cfg556_results.json `{foot}|census|cen` to ≤ 1e-6 absolute on both footings.
- **C1:** M0 reproduces C0's E to ≤ 1e-4 absolute.
- **C2:** f_ret ≡ 1 reproduces CFG556's `{foot}|fret1|cen` E to ≤ 1e-6.
- **C3:** mass inside r_ta is conserved to ≤ 1e-6 relative in every variant. This is checked on every 8th mass.

Any failed control means NO RESULT for the affected variants.

## MUTATE (`CFG594_MUTATE=1`, separate `_MUTATE` outputs)

- **MU1:** supply × 0.2 must classify as DRIVER on both footings.
- **MU2:** replacing the framework profile with the NFW profile itself (CFG556 mode `lta`) must give |E| ≤ 1e-9, which is MINOR and not CUT-SETTING only if the reference is used consistently.

Exit 1 when both teeth bite.

## Reporting

- All numbers come from `cfg594_sensitivity_results.json`.
- The audit cites the class of each item, never the size of the halo-model excess as a verdict.
- Compute: `nice -n 10`, ≤ 2 threads, about 1–3 min.
