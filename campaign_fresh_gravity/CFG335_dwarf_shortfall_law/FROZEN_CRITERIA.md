# CFG335 FROZEN CRITERIA: is the dwarfs' mass shortfall under the law a simple empirical function?

**Lane:** orchestrator, a cheap local lane. The owner said "keep going on research".

**Question.** CFG333 showed the ultra-faints need more mass than any ownership class supplies. For every Local Group / Local Volume dwarf with a resolved dispersion, compute the EXTRA dynamical mass the law needs inside r = (4/3) r_half:

ΔM = M_need − M_b/2,

where M_need solves σ_obs² = g r / 3 with g = ν(g_N/a₀) g_N and g_N = G M_need / r². This is the inverse of the AUDIT_UFD estimator. The baryons are Υ_V = 2 plus 1.33 M_HI, the kernel is the exponential RAR kernel (equal to ν_mono to 5e-9 here), and both footings are used.

Is ΔM (or ΔM / M_b) a simple function of a measured property?

## Inputs (on disk)
- `real_research/data/dsph/lvd_dwarf_mw.csv`, `lvd_dwarf_m31.csv`, `lvd_dwarf_local_field.csv`.
- Resolved dispersions only, with the same cuts as AUDIT_UFD except no M_V cut.
- Systems with ΔM ≤ 0 (law already sufficient) are kept as "no shortfall", with their ΔM shown as signed.

## Candidate relations (fixed in advance; each a log–log OLS with bootstrap errors)
- **F1:** log ΔM against log M_b (slope, intercept, scatter).
- **F2:** log ΔM against log r_half.
- **F3:** a constant ΔM, the "common mass scale" idea of Strigari+2008. Test the scatter of log ΔM against its measurement scatter.
- **F4:** log(ΔM / M_b) against log M_b.

## Decision
A relation counts as **LAW-LIKE** if all three hold:
- its residual scatter is ≤ 0.25 dex;
- it beats the constant (F3) by Δ(scatter) ≥ 0.05 dex, or F3 itself has scatter ≤ 0.25 dex;
- it holds within 2σ across hosts (MW, M31 and field, fitted separately).

Otherwise: **NO SIMPLE LAW**. Report all four relations whatever the outcome. This is descriptive: no mechanism is claimed, and κ = ½ is fixed.

## Controls
- **C1:** inverting then re-predicting gives back σ_obs to 1e-8.
- **C2:** a system whose σ_obs equals the law's prediction gives ΔM = 0 to 1e-8.
- **MUTATE** (CFG335_MUTATE=1): σ_obs is shuffled across systems; F1's scatter must grow.
