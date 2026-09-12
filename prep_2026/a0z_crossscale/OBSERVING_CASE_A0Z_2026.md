# Observing case: does the MOND acceleration scale evolve? One deep-MOND rotator at z ≈ 2.5 decides

*Companion to the pre-registered measurement, DOI 10.5281/zenodo.22563139 (2026-09-06). Written 2026-09-10 for observers; every number
below is either frozen in that deposit or taken from the committed target ledger (`highz_target_score_2026.py`). Nothing here is a claim
that the framework is right; it is the case for the one measurement that can tell.*

## 1. The question, in one paragraph

Galaxy rotation curves obey the radial-acceleration relation with a scale a₀ ≈ 1.2×10⁻¹⁰ m/s². Two readings of that scale make opposite
predictions for its redshift dependence. If a₀ is tied to the dark-energy density, a₀ = κc√(Gρ_Λ), it is **constant** (ρ_Λ is constant for
w = −1). If it is the emergent scale of ΛCDM haloes, it tracks √(Gρ_crit) ∝ H(z) and **rises**: by z ≈ 2.5, H has grown by a factor of
about 2.1, so a deep-MOND galaxy of fixed baryonic mass rotates 2.1^{1/4} = 1.20× faster than the local Tully–Fisher relation says.
No present archive object separates the two (the twelve published constraints are exhausted and prior-dominated). One galaxy that is
genuinely deep-MOND, rotation-dominated, gas-measured and lens-controlled is enough.

## 2. The two predictions (frozen)

| quantity at z ≈ 2.5, fixed baryonic mass | flat a₀ (framework) | rising a₀ (ΛCDM-native) |
|---|---|---|
| deep-MOND Tully–Fisher zero-point shift Δ_BTFR = log M_b − 4 log V_f − C₀ | **0.00 dex** | **+0.33 dex** |
| flat rotation speed of a 60 km/s dwarf | 60 km/s | 72 km/s |
| required precision per decisive galaxy | σ(Δ_BTFR) ≤ 0.13 dex | same |

C₀ is frozen from the local calibration (both a₀ footings, 9.36×10⁻¹¹ and 1.13×10⁻¹⁰ m/s²) before any high-redshift value is examined.
Estimator: galaxy median, then median across galaxies. No drift nuisance is added after observation.

## 3. The target gate (a galaxy enters the decisive sample only if all hold)

1. **Deep MOND:** g_bar(R_out) < 0.30 a₀ on both footings and at the upper end of the mass uncertainty, from the resolved stellar + gas
   distribution (preferred < 0.20 a₀).
2. **Rotation:** V_rot/σ > 1.5 from a forward-modelled source-plane disc fit (dispersion, inclination, beam smearing, asymmetric drift,
   clumps, outflows fitted together); preferred > 2; regular monotonic velocity field.
3. **Lens control:** δlog₁₀μ < 0.08 dex and no credible alternative reconstruction outside the systematic budget.
4. **Geometry:** 35° < i < 75°; ≥ 5 independent source-plane resolution elements along the kinematic major axis.
5. **Redshift window:** 2.32 < z < 3.12, so Hα and [O III] fall together in NIRSpec G235H/F170LP (1.66–3.17 μm, R ≈ 2700) and CO(3–2)
   (345.8 GHz rest) falls in ALMA Band 3. ([C II] at z ≈ 2.5 is in the Band 8/9 gap.)

A galaxy failing (1) or (2) is rejected without interpretation as a Tully–Fisher test.

## 4. The funnel

**Stage 1 — JWST/NIRSpec IFU, G235H/F170LP.** Deep enough for a 2-D velocity field; build a forward-modelled source-plane velocity cube
(never de-lens a derived rotation curve). Advance only if the rotation gate passes and g_bar,* + g_gas,max(R_out) < 0.3 a₀ with a
conservative upper estimate of the still-unmeasured gas, so ALMA time is never spent on a galaxy that could not discriminate a₀.

**Stage 2 — ALMA Band 3, CO(3–2).** Integrated molecular gas mass and a resolved CO velocity field: the decisive galaxy needs two
independent dynamical tracers, and a material CO/optical discrepancy invalidates the target rather than widening its error bar.
M_b = M_* + 1.36 (M_HI + M_H₂) with X_CO and excitation uncertainties propagated explicitly.

**Error budget (per decisive galaxy):** δV_rot/V < 5% from the combined tracers; δlog₁₀M_b < 0.10 dex; 0.05–0.07 dex left for
inclination, lens reconstruction and asymmetric drift; hence δlog₁₀μ ≲ 0.05–0.08 dex. That lensing requirement alone removes
MACS J0451 (lens models disagree, 21.5 vs 49).

## 5. Candidate pool (from the committed ledger of 21 objects, both footings scored)

The honest state of the ledger: **no known object passes the flagship gate today.** Every rotator with measured kinematics is
high-acceleration, and every deep-MOND candidate lacks resolved rotation. The decisive galaxy must be *found*, starting from a genuinely
low-mass, highly magnified lensed disc and proving it rotates — not from a known rotator hoped to be deep-MOND.

Inside the simultaneous NIRSpec + Band 3 window (2.32 < z < 3.12), in ledger order:

| object | z | μ | status | why it is or is not a flagship |
|---|---|---|---|---|
| Cl 0949+5153 arc | 2.39 | 7.3 | rank 4 | deep-MOND score 0.52, but a merger; rotation unknown |
| A1689B11 | 2.54 | 7.2 | rank 6 | V/σ = 8.7 (excellent rotator) but high acceleration (D = 0) — a **control**, not a flagship |
| A68-HLS115 | 2.49 | 5.3 | rank 11 | no kinematics; single lens model |
| Abell 68 C4 | 2.622 | — | unscored | low-mass lensed candidate; Hα + [O III] + CO(3–2) all reachable; **first Stage-1 target** |
| Abell 68 C20b | 2.689 | — | unscored | same class; **second Stage-1 target** |

Outside the window but informative: SL2S 0217 (z = 1.84, μ = 17, deep-MOND score 0.92, rotation unknown; CO(4–3) in Band 4) is the
best deep-MOND candidate in the ledger and a natural Stage-1 target if the window is relaxed to Hα-only.

**Controls (mandatory):** one high-acceleration rotator in the same window (A1689B11) to verify that the pipeline returns the local
Tully–Fisher zero-point where both predictions agree; one cold-tracer control (zC-400569, z = 2.24, V/σ = 20) for the CO/optical
tracer comparison.

## 6. Time (order-of-magnitude, not an exposure-time-calculator run — flagged)

- Stage 1: NIRSpec IFU, ~3–5 h on-source per candidate for a resolved Hα velocity field at μ ~ 5–10 (2–4 candidates ⇒ 10–20 h).
- Stage 2: ALMA Band 3 CO(3–2), ~5–10 h per source for a resolved line at ~10⁹ M_⊙ of H₂ magnified ×5–10 (1–2 sources ⇒ 10–20 h).
- Total: one JWST small programme plus one ALMA proposal; decisive outcome with a single surviving galaxy.

## 7. Decision rule (frozen)

Near 0.00 dex: the constant-a₀ law survives and the ΛCDM-native rise is excluded at the stated precision. Near +0.33 dex: the framework's
constancy prediction is falsified and the emergent-scale reading survives. Inconsistent with both: evidence against both, reported as such.
Any other significant displacement falsifies the framework's low-redshift constancy prediction.

## 8. Why an observer should want this regardless of the answer

Either outcome is a publishable, pre-registered result about whether the galactic acceleration scale is a cosmological constant or a
by-product of halo assembly. The gate is strict enough that a null on the gate (no galaxy passes) is itself informative about the
deep-MOND population at z ≈ 2.5. The pipeline, the frozen constant, the estimator and the decision rule are all public and dated before the data.

*Provenance: DOI 10.5281/zenodo.22563139; `prep_2026/a0z_crossscale/highz_target_score_2026.py` (ledger and scores);
`a0z_fork_likelihood_2026.py` (why the archives cannot decide).*

---
**Correction pending (2026-09-12, L189).** The framework's own necessity certificate (L166) and its Lyman-α gate require a clustering cold component whose halos persist around z ≈ 2.5 galaxies (the forest's k = 5 h/Mpc structures are those halos). A 3e11 M☉ halo at z = 2.5 contributes a dark fraction ≈ 0.38 inside R_e = 3 kpc of a 1e10 M☉-baryon rotator, shifting the framework's BTFR zero-point at z ≈ 2.5 by ≈ +0.05 dex in velocity (+0.2 dex in mass). The "0.00 dex vs +0.33 dex" gap stated above assumed baryons-only galaxies and shrinks to ≈ 0.1 dex in mass zero-point, below the ±0.13 dex resolution of the funnel. The decision rule must be recomputed with the retained halo included before any observing time is requested; a v2 of the published case (DOI 10.5281/zenodo.22700993) is pending.
