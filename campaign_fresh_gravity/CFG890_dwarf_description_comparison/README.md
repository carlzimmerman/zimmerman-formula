# CFG890 — which few-parameter description of the dwarf excess works best? (one sample, one likelihood, one penalty)

Criteria: `FROZEN_CRITERIA.md` (2ebf38985, committed alone before the script; reservation CFG890–899).
Run (one core, about 3 + 8 + 2 × 2.5 min): `CFG890_PART=variants OMP_NUM_THREADS=1 nice -n 10 python3 cfg890.py`, then
`CFG890_MUTATE=shape`, `CFG890_MUTATE=clump`, then the primary `python3 cfg890.py`. The primary run reads the variants and MUTATE
JSONs to apply the pre-registered qualifiers. Post-hoc diagnostics: `CFG890_POSTHOC=binary|decomp`. Each mode writes its own
`.out` / `.json`. numpy/scipy only, well under 1 GB.
κ = ½ fitted; ν_e; the two footings are never pooled; no dark-matter particle; not theory closed.

## Question
The record describes the dwarf excess in several ways: CFG870 (extended cored component), CFG877 (finite clump), CFG851 (red-lens
power law in g_bar) and CFG828 (excess only at g_bar ≲ 1e-12). Each was scored on its own subset with its own statistic. This
lane fits all of them, plus a few simple alternatives, to the same 83 LVD dwarfs (CFG880's sample) with:
- **one likelihood:** σ_obs ~ split normal around σ_model·e^η, with η ~ N(0, s_int²) intrinsic scatter in ln σ;
- **one penalty:** AIC/BIC;
- **at most two global parameters per model.** A free mass per dwarf would be dark matter by another name, so it is not allowed.

The question has two parts. Does any model reach s_int consistent with 0? And is the best model mass-like (an added component)
or acceleration-like (g depends on g_bar differently)?

## Result — CLASS: **NONE WORKS; type: MASS-LIKE PREFERRED** (both footings; no qualifier triggered)
Primary, N = 83. ŝ_int is in ln σ, with its 95% profile interval. ΔBIC is measured from the best model.
| model | type | k | canonical ŝ_int (95%) | ΔBIC | alt ŝ_int (95%) | ΔBIC | globals (canonical; 95% for k = 1) |
|---|---|---|---|---|---|---|---|
| M0 law alone | — | 0 | 0.635 (0.527–0.771) | 96.0 | 0.601 (0.497–0.732) | 89.2 | — |
| M1 free a0 | acc | 1 | 0.448 (0.368–0.548) | 53.6 | 0.448 (0.368–0.548) | 53.7 | a_d 6.0e-10 (3.8–9.6e-10) = 6.4 a0 |
| M2 finite clump (CFG877) | mass | 1 | 0.269 (0.210–0.345) | 3.3 | 0.276 (0.217–0.352) | 4.7 | σ_x 7.45 (6.63–8.19) km/s |
| M3 extended cored, r_c 104 (CFG870) | mass | 1 | 0.294 (0.233–0.374) | 11.9 | 0.300 (0.238–0.380) | 13.3 | V_x 9.00 (7.76–10.29) |
| **M5 extra mass ∝ r** | **mass** | 1 | **0.279 (0.223–0.352)** | **0** | **0.280 (0.224–0.352)** | **0** | **V_x 6.48 (5.56–7.43)** (alt 6.29) |
| M6 free Υ_V | baryon | 1 | 0.474 (0.391–0.578) | 60.2 | 0.468 (0.386–0.572) | 58.9 | Υ_V 9.9 (6.4–15.3) |
| M7 CFG851 law, fixed | acc | 0 | 0.499 (0.407–0.614) | 65.8 | 0.499 (0.407–0.614) | 65.9 | b 0.060, log g† −10.05 (alt −10.67) |
| M8 low-g step (CFG828) | acc | 2 | 0.377 (0.305–0.468) | 39.3 | 0.375 (0.303–0.465) | 38.9 | ×3.34 in g below 10^−12.19 (63 dwarfs) |
| M4 low-g power shape | acc | 2 | 0.394 (0.322–0.487) | 43.4 | 0.396 (0.323–0.488) | 43.8 | b 0.223, log g* −10.81 |
| M11 acceleration floor | acc | 1 | 0.418 (0.344–0.513) | 45.3 | 0.418 (0.343–0.513) | 45.4 | g_f 6.2e-12 (4.1–8.9e-12) |
| M9 clump, free core | mass | 2 | 0.274 (0.214–0.349) | 7.2 | 0.277 (0.219–0.353) | 8.7 | σ_x 7.01, r_c 81 pc |
| M10 extended, free core | mass | 2 | 0.274 (0.219–0.347) | 3.1 | 0.277 (0.221–0.349) | 3.6 | V_x 6.95, r_c 27 pc |

- **No model works.** Every 95% interval on s_int excludes 0, in every model, variant and post-hoc run. The smallest lower limit
  anywhere is 0.172 (V1 canonical, M10). The best description still leaves about 0.28 in ln σ, i.e. ×1.32 in σ and ×1.75 in
  dynamical mass, from dwarf to dwarf. The law alone leaves 0.64; the best model removes 56% of it.
- **Mass-like beats acceleration-like by ΔBIC +39.3 (canonical) / +38.9 (alt):** best mass-like M5 against best
  acceleration-like M8. This is ΔlnL = 17.4 even before M8 is charged for its extra parameter.
- **Which mass-like form is not decided.**
  - M5, a constant extra V² (σ² = σ_law² + (3.7 km/s)²), leads.
  - M10 (extended, r_c ≈ 25 pc) trails by 3.1 / 3.6, and CFG877's finite clump (M2) by 3.3 / 4.7.
  - CFG870's 104-pc core (M3) is clearly worse (+11.9 / +13.3).
  - V2 (M_V ≤ −6) reverses the order: there M2 is best and M5 trails by +4.2 / +3.1.
- **Every acceleration-like description fails:**
  - a single free a0 for dispersion-supported systems wants 6.4 a0 and still leaves 0.45;
  - CFG851's lens law (fixed) cuts the scatter only from 0.64 to 0.50;
  - a free power-law or step in g_bar reaches 0.38–0.39;
  - a global Υ_V wants ~10 and leaves 0.47.

## Variants (pre-registered; type verdict computed from both footings)
| variant | best (canonical / alt) | ŝ_int best (95%) | ΔBIC_type (acc − mass) | type verdict |
|---|---|---|---|---|
| V1 law over-predicts at ≥ 2σ dropped (5 canonical / 7 alt removed) | M5 / M5 | 0.242 (0.185–0.316) / 0.242 (0.184–0.318) | +36.2 / +37.0 | MASS-LIKE PREFERRED |
| V2 M_V ≤ −6 (N 53) | M2 / M2 | 0.239 (0.182–0.318) / 0.250 (0.192–0.331) | +17.3 / +14.1 | MASS-LIKE PREFERRED |
| V3 10% systematic floor (report-only) | M5 / M5 | 0.259 (0.198–0.335) / 0.260 (0.200–0.336) | +38.7 / +38.2 | MASS-LIKE PREFERRED |

Neither qualifier fires. The type verdict is the same in V1 and V2, and no description works in either.

## Outlier residuals (primary, canonical; r = ln(σ_obs/σ_model), t includes ŝ_int; alt within ±0.05 in r)
| | Crater II (2.34) | Antlia II (5.98) | Sextans (7.90) | Draco (9.55) | Bootes I (4.00) |
|---|---|---|---|---|---|
| M0 law | 3.87, r −0.50 | 5.52, +0.08 | 4.40, +0.59 | 4.61, +0.73 | 2.36, +0.53 |
| M5 best | 5.38, −0.83 (t −2.5) | 6.67, −0.11 | 5.77, +0.31 | 5.94, +0.48 (t +1.7) | 4.42, −0.10 |
| M2 clump | 4.48, −0.65 (t −2.0) | 5.72, +0.04 | 5.52, +0.36 | 7.01, +0.31 | 5.96, −0.40 (t −1.4) |
| M4 shape | 8.66, −1.31 (t −3.0) | 12.65, −0.75 (t −1.9) | 7.84, +0.01 | 6.59, +0.37 | 4.34, −0.08 |
| M8 step | 7.06, −1.10 (t −2.6) | 10.09, −0.52 | 8.04, −0.02 | 8.43, +0.12 | 4.31, −0.08 |

- **Crater II sits below every model** (the law alone already over-predicts it).
- **Antlia II separates the types:** mass-like forms fit it, while acceleration-like forms boost it to 10–15 km/s, against 6.0.
- **Sextans goes the other way:** acceleration-like forms fit it exactly, while mass-like forms fall short by +0.3 (cf. CFG884).
- **Draco sits above every model** (+0.12 to +0.73).

The largest residuals under M5 are Andromeda XXVII +3.0, Crater II −2.5 and NGC 147 −2.2. The full per-model tables and top-five
lists are in `cfg890.out`.

## Post-hoc diagnostics (added after the pre-registered runs; not graded)
- **`binary`: binary-corrected σ** (Arroyo-Polonio+2026 flat-f, as CFG880 V4) for 8 UFDs and Crater II. The result is unchanged:
  NONE WORKS, MASS-LIKE PREFERRED (+31.1 / +30.9). M5 still leads (ŝ 0.297, 0.236–0.376), but M2 is now only +1.5 / +2.5 behind.
  So part of M5's lead over the clump comes from binary-inflated ultra-faint dispersions. A constant σ floor is also what unresolved
  binaries add.
- **`decomp`: which dwarfs carry the type verdict.** The per-dwarf Δ_i = ln L_i(M5) − ln L_i(M8) sums to +17.4 canonical.
  - The sum is spread out: +9.0 from M_V ≤ −6 and +8.4 from M_V > −6. By g_N third it is +8.0 (lowest), +6.5 (middle), +3.0 (highest).
  - Removing Crater II and Antlia II still leaves +15.8.
  - Most in favour of mass-like: Segue 1, Eridanus IV, Andromeda II, Horologium I, Willman 1, Cetus, Antlia II.
  - Most in favour of acceleration-like: Tucana V, Andromeda XXVII, Bootes II, Draco, Andromeda IX/V.
  - **Reading:** the excess does not rank with g_bar, which is what an acceleration-like law needs. It behaves more like a roughly
    fixed extra velocity scale added in quadrature.

## Controls
- **K1 PASS (exact):**
  - the per-dwarf σ_law equals CFG880's committed `law` values for all 83 dwarfs on both footings (max relative diff 0);
  - M2's ln L at s_int = 0 and CFG880's universal σ̄ (8.0425 / 8.3499) equals CFG880's committed ln L(s_int = 0) (−448.738864 /
    −514.479845; |diff| 0).
  - Reported, not an identity: with σ_x fixed at 7.534, s_int in ln σ is 0.268. CFG880's 0.380 is a scatter in ln σ_x with σ̄ free,
    a different hierarchy.
- **K2 FAIL as frozen; K2b PASS.**
  - The frozen reference (trapezoid over t = η/s within ±12, 240001 nodes) differs by up to 48.4 in ln L_i (Fornax at 1.5 σ_law,
    s 0.01). The reference itself is at fault: this integrand peaks at t* = −18.8, outside ±12. The ±12 reference gives −482.01; ±40
    and ±60 both give −433.6195; the integrator gives −433.6195 (diff 3e-11).
  - The wider reference (±40, 400001 nodes; added after freezing, before any run) agrees to 2.4e-4 in all 12 cases × 83 dwarfs.
- **K3 PASS everywhere:**
  - every nesting holds (M9 ≥ M2, M10 ≥ M3/M5, M4 and M8 ≥ M0), and every MLE beats its prescan;
  - two profile crossings were improved by the full optimiser (alt V1 M9 +0.034; post-hoc binary alt M9 +0.19), and the scripted
    re-crossing updated their intervals.
- **MUTATE-shape** (truth M4: b 0.20, log g* −11.0; s_int 0; seed 890): recovers M4 (b 0.186, log g* −10.91) with s_int 0.000
  (95% ≤ 0.035). M4 is best by BIC on both footings and ACCELERATION-LIKE PREFERRED (ΔBIC −31 / −34). **Behaves.**
- **MUTATE-clump** (truth M2: σ_x V_x/√2; seed 891): M2 is best with s_int 0.000 (≤ 0.040), M9 also works, and the verdict is
  MASS-LIKE PREFERRED (+136 / +132). **Behaves.**
  - Caveat: the recovered σ_x is 7.82 against a truth of 7.534 (canonical), just outside its profile 95% (7.58–8.10). The alt
    truth 7.486 sits at the edge of 7.48–8.02.
  - This is a single realization; both footings share the seed's noise draws.
- **Power:** the comparison can return A DESCRIPTION WORKS and either type verdict when the truth is one of the models. So a NONE
  WORKS / MASS-LIKE result on the real data is not built in by the method.

## Reading
- **No 0–2-parameter global description removes the dwarf scatter.** A dwarf-to-dwarf spread of about ×1.3 in σ (×1.75 in mass)
  survives every model:
  - after dropping the tidal / external-field candidates (V1);
  - in the bright half only (V2);
  - with a 10% systematic (V3);
  - with binary-corrected UFD dispersions (post-hoc).
  - CFG880's NOT UNIVERSAL is therefore not specific to the clump form. Every simple description tried here leaves it.
- **The description that works best adds mass, not a modified acceleration dependence.** The gap is large (ΔBIC ≈ 39). It is
  broad-based, not carried by one or two outliers, and holds in every variant (+14 to +39). Read within the framework, the excess
  behaves like added cold-energy mass with a velocity scale of a few km/s, not like a change in the law's shape at low g_bar.
- **This is a statement about descriptions, not a mechanism.**
  - Nothing here says what supplies the added mass. The record's supply channels for satellites fail (CFG842).
  - Which mass form is right (constant extra V², small-core extended, or CFG877's finite clump) is not decided: ΔBIC 3–5, and the
    order flips in V2 and narrows with binary correction.
  - CFG870's 104-pc core is disfavoured against the smaller or no core.
- **Not a statement that the data favour the framework.** The law alone is the worst of the 12 models (ΔBIC +96), and the best model needs an
  added, unexplained component. The remaining 0.28 still needs per-dwarf physics: tides, external field, binaries, Υ spread or
  genuinely different cold-energy content.

## Disclosures
- **Not blind:**
  - all 83 dispersions and CFG880's per-dwarf residuals had been seen;
  - the clump and cored forms were calibrated on subsets of this sample (CFG870/877);
  - only CFG851's law comes from independent data (KiDS red lenses).
- **Timing test:** a timing run of four fits (M0, M2, M4, M8, canonical primary) was made while writing the script and showed their
  numbers before the full run. Nothing in the models, criteria or class rules was changed afterwards, and the committed run
  reproduces those numbers.
- **Integrator change (decided before any run):** the frozen per-dwarf grid (±15 errors around σ_obs) was supplemented by two
  301-node pieces reaching μ ± 14 s_int. Without them the grid misses the integrand's peak for models many error bars away. GH and
  s = 0 are as frozen. K2b validates the result.
- **Post-freeze additions, all labelled:** K2b, and the `binary` and `decomp` diagnostics. After adding them, the primary run was
  re-run and is byte-identical apart from timing lines.
- **Interpretation of a qualifier:** the frozen V1/V2 qualifier ("different canonical type verdict") was applied to the type
  verdict computed from both footings of the variant. The canonical-only ΔBIC_type has the same sign and is > 6 in every variant,
  so the reading does not matter here.
- **Type rule:**
  - M11 (acceleration floor) is typed acceleration-like by its parameter. It equals a constant-surface-density added mass, and it
    is not competitive either way (ΔBIC +45).
  - M1 is footing-independent by construction (identical numbers on both footings).
- **Statistics:** Wilks intervals with no boundary correction. BIC with N = number of dwarfs. 12 models were compared; no
  look-elsewhere correction beyond BIC.
- **Not modelled:** external field, tides, anisotropy, per-dwarf Υ and binaries (except the post-hoc run). s_int absorbs them all.
- **Compute:** light single-core runs (OMP_NUM_THREADS=1, nice 10) beside the live 1024³ job, as allowed by the owner tonight. No
  other process was touched.
