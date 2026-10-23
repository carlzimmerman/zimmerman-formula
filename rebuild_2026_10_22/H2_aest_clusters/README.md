# H2_aest_clusters: can AeST supply F1's cluster-core lensing excess?

## Verdict: CANNOT (static term: wrong shape; dust beyond the hydrostatic branch needs a simulation)

- **Frozen rule** (364a56c250): CAN ONLY WITH A FITTED ZERO POINT, at a single grid point μ = 0.7 Mpc⁻¹, Δ = −0.25.
- **AMENDMENT A1** (post-result, 5160a89939): **CANNOT**. The frozen OUTER clause was one-sided. That pass has the
  prediction at 54 % of the OUTER data (A_OUT = 1.85, canonical) and a *negative* ΔΣ in the 2.1–3 Mpc bin; the two OUTER bins
  cancel inside the band sum. With a two-sided OUTER test and a bins 3–7 profile χ² (jackknife covariance, Hartlap), **no (μ, Δ)
  passes any of the four cells**, at allowed or excluded μ.
- **The best profile χ² anywhere is 27.7–39.6.** The law alone gives 27.3–41.8 (5 bins; the pass line is 11.07). So the mass term
  never improves on the law. Where it lifts MID (μ ≈ 0.7), χ² rises to 91–122.
- κ = ½ FITTED. Footings never pooled. No dark-matter particle. Not theory closed. Nothing here says the data favour the framework.

Checks 6/6 PASS, exit 0, 80 s, one thread, max RSS 0.85 GB. `--mutate` (Yukawa sign) fails K3 and K4 (3/6, exit 1).

## What the static term does (computed, both footings, both native h)

**Model.** The model is the AeST quasi-static system, solved exactly in spherical symmetry on each cluster's baryons (VSZ
arXiv:2304.05134 eqs. Phi-Orig and Chi-Orig; SZ21 arXiv:2007.00082 eq. NT_quasi_Phi; both on disk in
`_external_data/aest_papers_2026_10_22/`):

    ∇²Φ̃ + μ²Φ = 4πGρ_b,   ∇·(𝒥′∇χ) = ∇²Φ̃,   Φ = Φ̃ + χ = Ψ.

It uses λ_s → ∞ and C1's capped 𝒥, so μ = x/(1+x) holds exactly. At μ = 0 it reproduces F1's PRIMARY result to 2e-4
(K1, all 4 cells).

**The mass term is the dust (DERIVED).** It acts as an extra source, δρ = −μ²Φ/(4πG). This follows from SZ21:
- 8πG̃ρ = QK′ − K (L396);
- K = −2Λ + K₂(Q−Q₀)² (L300);
- the static Q = (1−Ψ)Q₀ (L361);
- μ² = 2K₂Q₀²/(2−K_B) (L379);
- G = 2G̃/(2−K_B).

So **the μ²Φ term *is* AeST's dust, in hydrostatic balance in the potential well.** This is the record's transcription of
Mistele+23 eq. 2. Its amount is set by the zero point of Φ (VSZ's Δ, Mistele's per-object chemical potential), which is a
free integration constant.

**Its shape is a ramp, then an oscillation.** In every allowed case the boost over the law is about 1.0 in INNER, rises
across MID, and then turns over or goes negative in OUTER (bins 3–7, 0.46–3 Mpc):

| μ [Mpc⁻¹], Δ = 0 (VSZ fiducial) | AeST/law, bins 3–7 (canonical, h 0.672) | A_MID can / alt | A_OUT can / alt | profile χ² can / alt |
|---|---|---|---|---|
| law (μ = 0) | 1 1 1 1 1 | 1.676 / 1.539 | 0.950 / 0.870 | 33.4 / 27.3 |
| 0.1 | 1.00 1.01 1.02 1.04 1.09 | 1.657 / 1.520 | 0.882 / 0.803 | 31.9 / 27.8 |
| 0.3 | 1.03 1.07 1.16 1.34 1.59 | 1.501 / 1.367 | 0.632 / 0.573 | 49.7 / 60.0 |
| 0.5 | 1.09 1.19 1.39 1.64 1.01 | 1.306 / 1.182 | 0.772 / 0.847 | 45.9 / 55.1 |
| 0.7 | 1.17 1.34 1.54 1.34 −0.97 | 1.178 / 1.067 | −6.3 / −2.2 | 267 / 294 |
| 1.0 | 1.30 1.47 1.27 −0.66 −1.11 | 1.258 / 1.274 | −1.0 / −1.1 | 211 / 223 |
| **needed** | **~1.7 1.7 1.7, then ~1 ~1** | 1 | 1 | ≤ 11.07 |

The h = 0.686 cells are within a few % of these (`h2_aest_clusters.out`).

- **Why the shape is wrong.** The added source tracks |Φ|. In the log-deep cluster potential |Φ| is nearly flat out to the zero
  crossing, so the extra mass grows like r³. It boosts 1.5–3 Mpc more than 0.5–1 Mpc, then oscillates beyond the VSZ onset
  radius r_C. The median r_C is 2.8 / 1.3 / 0.95 / 0.76 / 0.60 Mpc at μ = 0.1 / 0.3 / 0.5 / 0.7 / 1.0; the median baryon mass
  is 7.0e13 M☉ and the median r_M is 0.32 Mpc.
- **Moving the zero point does not help.** Changing Δ shifts the oscillation phase but not the ramp: Δ ∈ [−8, 2] was scanned.
- **The best case.** With OUTER held within 2σ, the most the term lifts MID is ×1.02–1.30 at μ ≤ 0.5, against ×1.54–1.72 needed.
  At μ = 0.7 it reaches ×1.60 only by overshooting bin 6 (×2.25) and collapsing bin 7 (×0.2–0.3); χ² is then 119–122.
- **Larger μ does not help either.** At the probes beyond the bound (1.58, 2, 3 Mpc⁻¹), the oscillation moves *into* MID: MID bins
  go negative and χ² is 145–313. **No μ is "needed"; none works.**

**Against the brief's constraints.**
- **C3 (L_eq = √2/μ ≥ 1.41 Mpc ⇔ μ ≤ 1).** The whole allowed grid satisfies it.
- **Galaxy RAR.** The guard is a 1e11 M☉ Hernquist galaxy with the same (μ, Δ). Its force at r ≤ 200 kpc stays within
  0.3–8.6 % of the law at Δ = 0, so it passes VSZ's criterion. But at 1 Mpc the guard galaxy's force **reverses**
  (g/g_law − 1 = −2.2 to −2.7) for μ ≥ 0.5, the range that moves MID at all. The record's transcription of Mistele+23
  (weak-lensing RAR flat to a_b ≥ 1e-15 ⇒ μ² ≤ 1e-3 Mpc⁻²) would exclude that. This is flagged: the paper is not on disk.
- **C2 / BBN / cosmology.**
  - C2's BBN bound K_B < 0.078 enters μ only through (2−K_B) and does not constrain it.
  - SZ21 L412 gives w₀ = 3H₀²Ω₀/(2(2−K_B)μ²), which is about 1e-8 (μ = 1) to 1e-6 (μ = 0.1). That is no bound.
  - SZ21 notes that the quadratic K cannot hold back to a ~ 1e-4 (that would force μ⁻¹ ≲ 1.4 kpc). So today's μ is set by a
    postulated non-quadratic K: **μ is a free constant**, not derived.

## (b) The dust sector beyond the static term

- **What is computable without a simulation.** In the hydrostatic branch, the dust's nonlinear accumulation *is* term (a):
  δρ = μ²|Φ|/(4πG) with the MOND-deep Φ, including its own gravity. That is exactly what was solved above, with its free amount
  (Δ) scanned. So the hydrostatic dust **cannot** fix the core.
  - Its natural extent is the n = 1 polytrope radius π/μ ≥ 3.1 Mpc for μ ≤ 1. That is too extended to concentrate in 0.5–1 Mpc
    without overloading 1.2–3 Mpc.
- **The CDM-like branch** (the dust leaves the quasi-static attractor and virialises). This branch is **non-native**. The only
  numbers are F1's addendum (ΛCDM-PROCESSED NFW, c* = 0.40, upper-bound context only, not recomputed here):
  - at the cosmic ratio sourcing AQUAL: A_MID 0.61 / 0.57 with A_OUTER 0.42 / 0.39;
  - at u = 0.443, Newtonian: A_MID 1.20 / 1.12 with A_OUTER 0.82 / 0.76.
  
  Every row that reaches MID ≈ 1 overshoots OUTER.
- **What a native simulation would need:**
  - an AeST N-body or hydro code that evolves φ, the aether (with its curl mode) and the metric;
  - a K(Q) beyond quadratic that fixes today's μ;
  - initial conditions from an AeST Boltzmann run. That run is not on disk; C2 lists the missing module and adiabatic ICs.
  - It would also need to resolve shell crossing of a single-stream condensate and the negative-density regime that VSZ and
    Mistele flag as possibly unstable.
  
  The record has only a prototype (`real_research/aest_3d_nbody/`, not used).

## Input ledger and caveats

- Inputs and classes are in `ASSUMPTION_LEDGER.md`.
- F1's per-cluster measurement is read-only from F1's scratch cache: sha256 961ea4fc…e720, 326 clusters.
- **Durakovic & Skordis 2023 (arXiv:2312.00889) is not on disk and was not used.** The record (`real_research/AEST_MASS_SCALE_two_doors.md:34`) transcribes its claim that the isothermal-sphere cluster RAR "displays a peak, then drops below the
  MOND expectation". That matches the ramp-then-oscillation found here; it is flagged as transcription only.
- **Approximations.**
  - Spherical symmetry; the aether curl mode vanishes there.
  - VSZ's point-mass Δ prescription is transplanted to an extended profile (H8). The Δ scan covers any error from that.
  - The health of the λ_s → ∞ cap is OPEN (C1, C2).
- **Matmul warnings.** macOS Accelerate prints spurious "divide by zero in matmul" RuntimeWarnings on stderr. Results reproduce
  F1 to 2e-4 (K1) and F1's projector to 1e-4 (K2).
- **Run history.**
  - Run 1 (kept as `h2_aest_clusters_RUN1_rss.out`) failed the frozen K6 at 1.116 GB ru_maxrss. Amendment A0 changed memory
    handling only; the scan lines are identical.
  - The MUTATE run also exceeds 1 GB (1.04).

## Files

- `FROZEN_CRITERIA.md`, committed alone first (364a56c250), with A0 and A1 (5160a89939).
- `h2_aest_clusters.py` → `.out`, `_results.json`; `_MUTATE.*`; `_RUN1_rss.out`.
- Run: `OMP_NUM_THREADS=1 nice -n 15 python3 h2_aest_clusters.py <F1 scratch kids dir> [--mutate]`.
