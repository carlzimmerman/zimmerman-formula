# CFG890 — FROZEN CRITERIA: which few-parameter global description of the dwarf excess works best?

Frozen before any script (reservation row CFG890–899, LEDGER). κ = ½ fitted; ν_e(y) = 1/(1 − e^{−√y}); the two a0 footings
(9.3603e-11 canonical, primary; 1.1312e-10 alt) are reported separately and never pooled; no dark-matter particle; not theory
closed. Raw data and framework-native quantities only (no ΛCDM halo profile anywhere).

## Why
The record holds several descriptions of the dwarf excess, each scored on its own subset and statistic: CFG870 (extended cored
component), CFG877 (finite clump), CFG851 (red-lens power-law excess in g_bar), CFG828 (excess only at g_bar ≲ 1e-12). CFG880
showed the finite clump with ONE σ_x leaves an intrinsic scatter of 0.38 in ln σ_x. This lane puts every candidate on the same
83 dwarfs, the same likelihood and the same parameter penalty, and asks: does any FEW-parameter GLOBAL description remove the
scatter, and is the best one mass-like (an added component) or acceleration-like (a change in how g depends on g_bar)?
A free extra mass per dwarf would be dark matter by another name; it is not a candidate here. Every model has at most two global
parameters plus the common intrinsic scatter s_int.

## Sample (LVD csvs only; nothing downloaded) — identical to CFG880's
`real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv`: every dwarf with a measured `vlos_sigma` (no `vlos_sigma_ul`),
r_h (`rhalf_sph_physical`, else `rhalf_physical`) and M_V; excluded rotating / gas-rich set: LMC, SMC, WLM, NGC 6822, IC 1613,
Leo A, Sagittarius dIrr, Pegasus dIrr, M 32. N = 83. Errors: LVD `vlos_sigma_em` / `vlos_sigma_ep`.

## Common inputs (per dwarf i; copied unchanged from CFG880 / CFG874)
- r12 = (4/3) r_h; L_V = 10^{0.4(4.83 − M_V)}; M_gas,in from CFG874's `gas_in()` (copied unchanged, as in CFG880).
- g_N,i = G (Υ_V L_V/2 + M_gas,in)/r12² with Υ_V = 2 (except M6); g_N does not depend on a0.
- σ_law,i²(a0, Υ_V) = g_N ν_e(g_N/a0) r12/3 (Wolf estimator); g_law = σ_law²·3/r12.
- Extra components are added Newtonian (unboosted) as in CFG870/877: σ² = σ_law² + G M_x(<r12)/(3 r12).

## Pre-registered model set (no model may be added after seeing results; post-hoc diagnostics, if any, are labelled)
k = number of global parameters (s_int not counted here; it is added to every model's count for AIC/BIC).
| id | name | σ_model,i² | globals (k) | bounds | type |
|---|---|---|---|---|---|
| M0 | law alone | σ_law²(a0, 2) | — (0) | — | baseline |
| M1 | free a0 for dispersion-supported systems | σ_law²(a_d, 2) | log10 a_d (1) | [−13, −7] | acceleration-like |
| M2 | finite clump (CFG877/880) | σ_law² + G M_x/(3 r12), M_x = min[2σ_x² r³/(G(r² + r_c²)), 81σ_x⁴/(4 G a0)], r_c = 104 pc | σ_x (1) | [0.01, 60] km/s | mass-like |
| M3 | extended cored (CFG870) | σ_law² + V_x² r12²/(3(r12² + r_c²)), r_c = 104 pc | V_x (1) | [0.01, 80] km/s | mass-like |
| M4 | low-g power shape (CFG851 form, free) | σ_law² · 10^{b·max(0, log10 g* − log10 g_N)} | b, log10 g* (2) | b ∈ [−0.5, 1.5], log10 g* ∈ [−15, −8.5] | acceleration-like |
| M5 | extra mass ∝ r (M3 with r_c → 0) | σ_law² + V_x²/3 | V_x (1) | [0.01, 80] km/s | mass-like |
| M6 | free global Υ_V | σ_law²(a0, Υ_V) (gas unchanged) | Υ_V (1) | [0.05, 100] | baryonic normalisation |
| M7 | CFG851 law, fixed | as M4 with (b, log10 g*) = CFG851 red M★-corrected calibration of the footing: canonical (0.059793, −10.04723), alt (0.058763, −10.67418) (`cfg851_results.json`, `<foot>|shift0.123`) | — (0) | — | acceleration-like |
| M8 | low-g step (CFG828) | σ_law² · A for g_N < g_c, else σ_law² | A, g_c (2) | ln A ∈ [ln 0.2, ln 50]; g_c ∈ geometric midpoints of consecutive sorted distinct g_N of the fitted sample | acceleration-like |
| M9 | finite clump, free core | M2 with r_c free | σ_x, r_c (2) | σ_x as M2, r_c ∈ [1, 5000] pc | mass-like |
| M10 | extended, free core | M3 with r_c free (nests M3 and, as r_c → 0, M5) | V_x, r_c (2) | V_x as M3, r_c ∈ [1, 5000] pc | mass-like |
| M11 | acceleration floor | σ_law² + g_f r12/3 | log10 g_f (1) | [−15, −9.5] | acceleration-like |

Type rule (fixed now): a model whose global parameter is an acceleration (a_d, g*, g_c, g_f) is acceleration-like; one whose
global parameter is the velocity scale of an added component (σ_x, V_x) is mass-like. M6 (global Υ_V) is a baryonic
normalisation and is not counted in either type. Disclosed degeneracy: M11 equals an added component of constant surface density
(M_x = g_f r²/G); it is typed acceleration-like by its parameter.

## Likelihood (common to all models)
- σ_true,i = σ_model,i · e^{η_i}, η_i ~ N(0, s_int²) (intrinsic scatter in ln σ, absorbs everything not in the quoted errors).
- σ_obs,i | σ_true,i: split normal, constant normalisation √(2/π)/(e_m + e_p), width e_p when σ_obs < σ_true, else e_m (CFG880's
  convention).
- η_i marginalised per dwarf: on a per-dwarf uniform grid in u = ln σ_true (1001 nodes from ln max(σ_obs − 15 e_m, 0.02 km/s) to
  ln(σ_obs + 15 e_p); trapezoid; log-space sum), plus the lower tail Φ((u_lo − μ_i)/s_int)·ℓ_i(u_lo); for s_int < 4 du_i the grid
  is replaced by 80-node Gauss–Hermite on the exact likelihood; s_int = 0 uses the exact likelihood at σ_model.
- ln L = Σ_i ln L_i. Maximum likelihood over (globals, s_int). s_int ∈ [0, 3].
- Optimiser: 1-parameter models — 41-point prescan then bounded scalar refinement; 2-parameter continuous models — 21×21 prescan
  then Nelder–Mead from the best cell; M8 — every candidate g_c with a bounded 1-D optimisation in ln A. Profiles in s_int are
  warm-started and re-checked with the prescan at the 95% crossings. A global at its bound is flagged.
- Reported per model and footing: globals at the MLE (for 1-parameter models with their 95% profile interval), ŝ_int with 68%
  and 95% profile intervals (Wilks, Δ(−2 ln L) = 1.00 / 3.84, crossings by root finding; no boundary correction), ln L_max,
  ln L at s_int = 0 and Λ_s = 2[ln L(ŝ) − ln L(0)], AIC = 2(k+1) − 2 ln L, BIC = (k+1) ln N − 2 ln L, ΔBIC to the best.
- Outlier residuals at each model's MLE for Crater II, Antlia II, Sextans, Draco, Bootes I: σ_model, r = ln(σ_obs/σ_model) and
  t = r/√(ŝ² + (e/σ_obs)²) (e the side-appropriate error); plus each model's five largest |t|.

## Classes (both footings required)
- A model **WORKS** on a footing if s_int = 0 lies inside its 95% interval (2[ln L_max − ln L_prof(0)] ≤ 3.84).
- **A DESCRIPTION WORKS (<model>)** if at least one model WORKS on both footings; named: the working model with the lowest
  canonical BIC (others listed).
- **NONE WORKS** otherwise; the class line names the best model by BIC on each footing, its ŝ_int (95%) and its type.
- **Type verdict** (always reported): ΔBIC_type = BIC(best acceleration-like) − BIC(best mass-like), per footing.
  MASS-LIKE PREFERRED if ≥ +6 on both footings; ACCELERATION-LIKE PREFERRED if ≤ −6 on both; LEANS MASS-LIKE / LEANS
  ACCELERATION-LIKE if both share a sign, both |Δ| ≥ 2, and not both ≥ 6; otherwise TYPE NOT DECIDED.
- Also reported: ΔBIC(M0 − best) and the scatter removed, 1 − ŝ_best/ŝ_M0.
- **Qualifiers** (pre-registered): if V1 or V2 gives a different canonical type verdict → "(type verdict not robust: V<n> gives
  …)"; if primary is NONE WORKS and some model WORKS on both footings in V1 or V2 → "(a description works only in V<n>: <model>)";
  if a MUTATE control fails → the type verdict is downgraded to "TYPE NOT DECIDED (comparison lacks power: MUTATE-<mode> failed)".

## Variants (both footings, all models)
- V1 drop dwarfs the law alone over-predicts at ≥ 2σ: z_law = (σ_obs − σ_law)/e_p ≤ −2 (per footing; CFG880's V3 rule).
- V2 M_V ≤ −6 only (N 53).
- V3 10% systematic floor, e → √(e² + (0.1 σ_obs)²) both sides (report-only; does not feed the qualifiers).

## Controls
- **K1 (code identity, exact):** (a) σ_law of all 83 dwarfs (Υ_V 2 + gas, both footings) equals CFG880's committed per-dwarf `law`
  (`cfg880_results.json`) to relative |diff| < 1e-12; (b) M2's ln L at s_int = 0 and σ_x = CFG880's committed universal σ̄
  (`sbar_univ`) equals CFG880's committed ln L(s_int = 0) = `lnLmax` − `Lambda`/2 to |diff| < 1e-8, both footings.
  Reported, not an identity: M2 with σ_x fixed at V_x/√2 (7.534 / 7.486) and s_int fitted here, beside CFG880's ŝ = 0.380 (CFG880
  puts the scatter in ln σ_x, this lane in ln σ, so they need not agree).
- **K2 (integrator):** per-dwarf marginal ln L against a brute-force trapezoid in t = η/s_int (±12, 240001 nodes) at
  s_int ∈ {0.002, 0.01, 0.03, 0.1, 0.38, 1.5} and σ_model ∈ {σ_law, 1.5 σ_law} (canonical): max |Δ ln L_i| < 1e-3 for all 83.
- **K3 (optimiser / nesting):** ln L_max(M9) ≥ ln L_max(M2) − 1e-3; ln L_max(M10) ≥ max(M3, M5) − 1e-3; ln L_max(M4), M8 ≥ M0 − 1e-3;
  every MLE ≥ its prescan best. A failure is reported and the affected models re-optimised from more starts before any verdict.
- **MUTATE** (`CFG890_MUTATE=shape|clump`, outputs `cfg890_MUTATE_<mode>.out` / `cfg890_results_MUTATE_<mode>.json`; primary
  sample only, no variants): synthetic σ_obs = σ_truth + split-normal noise with the real e_m / e_p (negative side e_p, positive
  side e_m; floor 0.1 km/s), s_int,true = 0, the full model comparison re-run.
  - `shape` (seed 890): truth M4 with b = 0.20, log10 g* = −11.0 on the footing's law. Behaves if M4 WORKS on both footings, M4 is
    within ΔBIC ≤ 2 of the best on both, and the type verdict is neither MASS-LIKE PREFERRED nor LEANS MASS-LIKE.
  - `clump` (seed 891): truth M2 with σ_x = V_x/√2 of the footing (CFG870: 10.65473/√2, 10.58697/√2). Behaves if M2 WORKS on both,
    is within ΔBIC ≤ 2 of the best on both, and the type verdict is neither ACCELERATION-LIKE PREFERRED nor LEANS
    ACCELERATION-LIKE.

## Hand expectations (disclosed before running)
NONE WORKS is expected: CFG880 showed Draco and Leo II (similar r12 and M_V, small errors) need different excesses, and the
brightest dwarfs (NGC 147, Fornax, Leo I) and Crater II sit below the law, which no added component can lower. M0's ŝ_int is
expected near 0.4–0.5, the best model's near 0.3. Which type wins is not anticipated.

## Disclosures (known before freezing)
- Not blind: all 83 dispersions and CFG880's per-dwarf law values and residuals have been seen; the clump and cored forms were
  calibrated on subsets of this sample (CFG870/877), and CFG851's law on KiDS red lenses (independent of these dwarfs).
- No external field, tides, binaries, anisotropy or per-dwarf Υ is modelled: s_int absorbs them all.
- M1 is footing-independent (a0 is fitted); its numbers are the same on both footings by construction.
- Wilks intervals at the s_int = 0 boundary are conservative for the WORKS test.
- Light single-core compute only (OMP_NUM_THREADS=1, nice 10), beside the running 1024³ job, as allowed by the owner tonight.
