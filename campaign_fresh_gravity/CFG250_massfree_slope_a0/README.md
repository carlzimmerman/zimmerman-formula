# CFG250 — a mass-free a₀ from rotation-curve SHAPE at z ≈ 1.5 (KURVS): phase 1, theory and mock pre-flight

- **Criteria:** `../CFG250_FROZEN_CRITERIA.md`. It was written in phase 1, before any measured KURVS V or σ was used. It is not blind; the disclosures are in its section 1.
- **Phase 1 only.** No measured velocity or dispersion was read.
  - From the figure digitisations this lane read marker radii, error bars and clip flags.
  - From the catalogue it read z, M*, R_eff and the inclinations.
  - The exact columns are in `CFG250_preflight.py`'s header.
  - There were no downloads, no edits to existing files and no commit.

## Files

| file | what | runtime |
|---|---|---|
| `cfg250_common.py` | kernels P2 / ν_mono and a₀, imported read-only from `CFG4_common`; Φ, s(y), D(y) tables; thin-disc field; K21 α(x); output tee | — |
| `CFG250_slope_theory.py` → `.out`, `_results.json` | theory: 7/7 checks | ~1 s |
| `CFG250_preflight.py` → `.out`, `_results.json` | mocks: exits 0 | ~2 min on the loaded machine |
| `CFG250_preflight_MUTATE.out`, `_MUTATE_results.json` | `MUTATE=1`: V × (\|R\|/kpc)^0.1; controls fail, exits 1 as required | ~2 min |

Re-running either script reproduces its outputs identically, apart from the wall-time line.

## Plan

**The idea.** Outside the baryons, a point mass gives s = d ln V_c²/d ln R = 1 − 2 dlnΦ/dlny. Under P2, s = −y/(1+y). So a measured pair (s, g_obs) gives a₀ = g_obs/Φ(y(s)) with no stellar or gas mass.

**The generalisation used here.** At a radius where the baryon shape has Newtonian slope s_N, D ≡ dlnΦ/dlny = (1 − s)/(1 − s_N). This is the shape-aware DS estimator.
- It is still free of the mass normalisation, but it needs the baryon shape.
- It is the frozen primary. The point-mass PM form is reported.

**The flat-versus-rival gap.** E(1.5) = 2.368 (0.374 dex); at the ten discs' median z of 1.529 the gap is 0.381 dex.

## Theory results (`CFG250_slope_theory.out`)

- **The point-mass approximation fails at KURVS radii.**
  - For a typical disc (log M* 10.14, R_d 2.29 kpc, gas μ = 0.67 at 2 R_d), the baryons' Newtonian slope is s_N = +0.23, −0.24, −0.56 and −0.91 at 2, 3, 4 and 6 R_d.
  - The MOND curve is still rising at 2–3 R_d.
  - The PM a₀ is therefore +∞ at 2–3 R_d, +0.87 dex at 4 R_d, and +0.11 (flat) / +0.24 (rival) dex at 6 R_d. The bias always has the rival's sign.
  - Any larger or more extended gas makes it worse.
- **The gas wall returns as a shape wall.** DS is exact with the true shape. Across μ 0.25–4 and R_gas 1–3 R_d its bias spans −0.31 to +0.55 dex at 4 R_d and −0.25 to +0.31 dex at 6 R_d, as large as the 0.38 dex signal.
- **Pressure shifts the slope.**
  - Exactly, s_a − s_c = (ΔP/V_a²)(1 − s_c); the check is 195 pairs to 7e-7.
  - At σ = 45 km/s the k = 2 term is 45–80% of V_c² at 2–4 R_d (flat law).
  - Analysing a k = 1 truth with k = 2 moves s by +0.11 to +0.43.
  - Over-correction always reads as a larger a₀, the rival's direction.
- **The required accuracy is tight.** A coherent slope error of +0.11 to +0.16 mimics the whole flat → rival gap.
- **The kernel matters.** ν_mono approaches deep MOND as s ≈ −√y/2, P2 as s ≈ −y. At a fixed (s, g_obs) the two kernels' a₀ differ by −0.19 to +0.70 dex; the large values come in the deep regime.

## Pre-flight result (`CFG250_preflight.out`, mocks only)

- **Controls pass:**
  - C1 point mass, 5e-6 dex;
  - C1b declared-shape disc, 1e-5 dex;
  - C2 Newtonian: an upper limit at the lower grid edge;
  - C3 the smearing-free matched mock is unbiased: +0.013 ± 0.174.
- **C4 coverage is 0.66.** The reported σ is conservative by about 1.5×; this is reported, not load-bearing (disclosed).
- **The MUTATE bites.** The controls shift by +0.46 and +0.61 dex, and C3 fails (−0.13 ± 0.19; in the pressure regime the amplitude change wins). The run exits 1.
- **Beam smearing dominates the slope.** With KURVS's 0.57″ seeing and 0.6″ bins, smearing alone biases the frozen window's ln V² slope by +1.01 on average (per disc +0.57 to +1.63).

  | smearing configuration | mean slope bias |
  |---|---|
  | primary (0.57″ PSF, 0.6″ bins) | +1.01 |
  | 0.1″ bins | +0.70 |
  | optimistic (Hα scale 1.5 R_d) | +0.58 |
  | pessimistic | +1.65 |
  | AO-like 0.15″ | +0.09 |

  The inner, brighter, slower gas is mixed into every outer marker: the flux-weighted centroid shifts inward by about σ_PSF²/R_d ≈ 2.5 kpc.
- **H0 FAILS.** The frozen seeing-limited primary puts the stack at the grid edge and has it model-rejected in 100% of mocks under both laws.
- **Without smearing, systematics still dominate.** In the AO or forward-model limit:
  - S_stat = 2.1 at σ 45 (2.3–2.4 at σ 20–30), but σ_sys = 0.50 dex (pressure ≥ 0.30, shape 0.40, inclination 0.06), so S_tot = 0.65.
  - The frozen rule reads "both allowed" in 99% of flat-truth mocks. P(lean rival | flat truth, marginal) = 0.00.
  - σ_sys is a lower bound, because half the σ ≥ 45 pressure cells leave the grid.
- **PM is unusable.** Per-disc s ≥ 0 in 42–99% of fits, and the stack sits at a grid edge.
- **The mocks cannot rotate out to KURVS radii.** Under flat a₀ with μ = 0.67 and k = 2, 36% of mock markers at σ 45 (71% at σ 60) are pressure-dominated and dropped. This is the slope-side face of CFG141's "both laws need about 4 M* of gas under P2".

**Can it discriminate on KURVS as is? No.** The phase-2 verdict is NON-DIAGNOSTIC by construction.

**What would make it work** (smearing-free mocks, same ten discs):

| change | S_tot |
|---|---|
| cold tracer (σ 10 km/s) only | 0.68 |
| cold tracer + measured gas extent (shape axis removed) | 1.97 |
| + markers to 10 R_d | **3.21** |
| AO-like 0.15″ + cold tracer + measured gas shape | 2.28 |

- The AO row carries a residual smearing bias of +0.24 / +0.12 dex, so the smearing must be forward-modelled even with AO.
- Tripling the sample multiplies S_stat by 1.73 but leaves σ_sys unchanged.
- In short, the estimator needs four things together:
  1. a pressure-free tracer (CO, V/σ ≳ 10), or a validated pressure model;
  2. a measured gas extent (CO or dust sizes) to fix s_N;
  3. smearing controlled (AO or 3D forward modelling);
  4. radii reaching about 8–10 R_d, where s_N → −1.

## Phase-2 plan (requires the orchestrator's go)

1. **Run the frozen estimator on the measured markers once,** in both modes (main and `MUTATE=1`), as a REPORTED measurement:
   - per-disc s, g_obs and domain status (finite, lower limit or upper limit) under P0, k1, k2 and K21 × {0.6, 1, 1.4};
   - the stacked Λ̂ with limits;
   - all variants in sections 3–4.

   The verdict is NON-DIAGNOSTIC (H0 failed). The pre-registered expectation is in criteria section 8: k = 2 slopes above the DS domain, meaning a₀ lower limits, and bearing on neither law.
2. **Or, better, do not spend phase 2 on seeing-limited KURVS.** Point it at data that meet the four requirements above:
   - CO kinematics with measured gas sizes (e.g. the NOEMA3D discs of CFG213/214);
   - or DysmalPy-style 3D fits that forward-model the smearing.

   Any such lane needs its own frozen criteria.
3. **Untested** (declared):
   - thick discs (the in-plane thin-disc field);
   - anisotropic dispersion;
   - non-circular motions;
   - Moffat PSF wings;
   - the true Hα profile;
   - the COSMOS half of KURVS;
   - the QUMOND/AQUAL field of a disc versus the algebraic ν relation used here.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
