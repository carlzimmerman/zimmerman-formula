# XR25 — does the chain's final gravity core survive strong-field tests?

The core is FP14's (commit 03db97f14): FP7's AQUAL-type root with the leaf-averaged c₂ term replaced by its c₂ → ∞ limit
(the constant-mean-curvature multiplier −2μ(K − ⟨K⟩ₕ)), α_c a regulator in [8.2×10⁻¹⁶, 3.2×10⁻⁹], ξ the one knob in
[0.0243 / 0.0268 pc, 100 pc], and φ's inertia λ either 0 (FP14) or > 0 (FP13's state separator H_S requires it). Both a₀
footings (9.3603 / 11.312 × 10⁻¹¹ m s⁻²) enter wherever a₀ does. κ = ½ stays FITTED. Nothing here closes the theory.

Scripts (each writes its own `.out`, `_MUTATE.out`, `_results[_MUTATE].json`; run from the repository root, `MUTATE=1` for
the control):
- `XR25_ppn_preferred_frame.py`: α₁, α₂ from the action at c₂ = ∞, against lunar laser ranging and the pulsar bounds.
- `XR25_pulsar_radiation.py`: neutron-star sensitivities, dipole and scalar-quadrupole radiation with the MOND sector live,
  J1738+0333, J0348+0432, J0737−3039A/B, and GW170817's −1PN bound.
- `XR25_cmc_compact_objects.py`: whether the CMC leaves exist around neutron stars and black holes; the universal horizon.
- `XR25_lambda_regulator.py`: the λ question under H_S (added at the coordinator's request).
- `XR25_common.py`: the shared block (re-derived second-order action), FP2's moving-source pipeline, a TOV solver.

| lane | main | MUTATE | what the MUTATE does |
|---|---|---|---|
| ppn | 11/13 pass, rc 0 (two reported as-run checks FAIL, see disclosures) | rc 1 | finite c₂ = 7.29×10⁻³, α_c = 10⁻³: α₁ = −4×10⁻³ violates every bound |
| radiation | 15/15, rc 0 | rc 1 | α = 0.02, λ = 0.01 (the literature's generic point): dipole radiation kills all three pulsars and GW170817 |
| cmc | 13/13, rc 0 | rc 1 | a non-critical foliation (C = 0.98 C_crit): the aether's acceleration diverges |
| lambda | 10/10, rc 0 | rc 1 | the c₂ floor: no λ window left (λ_max ≈ −2×10⁻⁵) |

## The answer

**1. Preferred-frame PPN — passes, with α₂ sitting exactly on the pulsar bound at the window's top (by construction).**
At c₂ = ∞ the core gives γ = 1, α₃ = 0, α₁ = −4α_c and α₂ = α_c(2α_c − 1)/(2 − α_c) ≈ −α_c/2 (derived from the action; these
are the c₂ → ∞ limits of FP7's committed forms). At the regulator's cap:

| bound | value used | the core | fraction |
|---|---|---|---|
| α₁, lunar laser ranging (Müller, Williams & Turyshev 2008) | \|α₁\| < 2.5×10⁻⁴ (2σ) | 1.28×10⁻⁸ | 5×10⁻⁵ |
| α̂₁, PSR J1738+0333 (Shao & Wex 2012) | 3.7×10⁻⁵ (95%) | 1.28×10⁻⁸ | 3.5×10⁻⁴ |
| α₂, lunar laser ranging | 6.8×10⁻⁵ | 1.63×10⁻⁹ | 2.4×10⁻⁵ |
| α₂, solar spin (Nordtvedt 1987) | 2.4×10⁻⁷ | 1.60×10⁻⁹ | 6.7×10⁻³ |
| α̂₂, isolated MSPs (Shao et al. 2013) | 1.6×10⁻⁹ (95%) | 1.60×10⁻⁹ | 1.00 |

The MOND sector's leak where the bounds live is at most 2.9×10⁻¹¹ (α₂ at 1 AU, ξ at its floor, λ = 274.8) — 4×10⁻⁷ of the
only bound at that scale. α̂ − α = O(α_c · s) ≲ 10⁻¹⁶. The α₂ row is marginal by construction: FP2 set α_c's cap at the
pulsar bound, so the window is PPN-safe, not PPN-predicted.

**2. Dipole radiation — negligible for every pulsar.**
- Khronon sensitivities: s = (α₁ − 2α₂/3)Ω/m (Foster 2007) = (11/3)α_c|Ω/m| — 0.43 α_c for J1738+0333's pulsar (TOV,
  SLy-type) — bracketed ×3 for strong-field effects (Yagi et al. 2014); ≤ 4×10⁻⁹ at the cap, exactly 0 at α_c = 0.
- The MOND scalar has no charge of its own. Its source is the chassis, whose total is the lapse flux 4πG M_Komar = 4πG M
  (checked to 10⁻¹⁰ on every star), so its dipole is the gravitational-mass dipole and only the khronon's sensitivities feed it.
- Dipole coefficient: C = √(3α_c/2) (the pure khronon, λ- and C_φ-free) wherever the heat filter is closed on the radiated
  branch. With the MOND sector live, 528 of 648 cells sit on the filter's transition branch (k ξ ≈ 3–5), where C is
  0.1–1.8×10⁴ times the khronon's. This includes every ξ up to 100 pc at α_c's floor.
- The pulsars' P_b-dot, dipole part / total deviation from GR (worst over α_c, ξ, λ, both footings and both AQUAL
  channels), against the 1σ errors:
  - J1738+0333: 1.2×10⁻¹⁵ / 9.9×10⁻⁹, against 13% (Freire et al. 2012).
  - J0348+0432: 2.8×10⁻¹⁶ / 1.5×10⁻⁸, against 18% (Antoniadis et al. 2013).
  - J0737−3039A/B: 3.8×10⁻¹⁷ / 9.1×10⁻⁹, against 6.3×10⁻⁵ (Kramer et al. 2021).

  The totals are the O(α_c) quadrupole corrections, not the dipole.
- Strong-field regime (the scalar formally unfiltered, y ≫ 1). Where α_c C_φ ≫ 1 the mode is the khronon. Where
  α_c C_φ ≪ 1 it is φ-dominated and superluminal, with C up to 1.1×10⁶ times the khronon's. It still multiplies
  (s₁ − s₂)² = O(α_c²): negligible.
- Prediction (unobservable): slow binaries (P ≳ 1 yr) in deep-MOND fields, with ξ near its floor, radiate more scalar than
  tensor power (up to 2×10⁷ at P = 100 yr, C^Q = 100).

**3. The CMC leaves — they exist around stars; around black holes they stop at r = 3M/2, and at α_c > 0 the c₂ = ∞ limit is singular there at first order.**
- **Static neutron stars:** the K = 3H₀ foliation is unique and regular (tilt ~7×10⁻²³ at the surface). At K₀ = 0 it is
  the static slicing.
- **Moving neutron stars:** the O(v) maximal perturbation obeys D_i(N² D^i ψ) = 0. With N > 0 there is no singular point,
  and the solution is nodeless and tends to the boost.
- **Black holes, the foliation:** the only regular stationary maximal foliation is Estabrook et al.'s C_crit = 3√3M²/4. Its
  leaves asymptote to the cylinder r = 3M/2, itself a K = 0 leaf, with an infinitely long throat.
  - That surface is a universal horizon: nothing escapes from inside it at any speed.
  - The aether is regular there (a² = 8/(9M²)).
  - The rate that makes the khronon analytic across it is κ_UH = 2√6/(9M) = 0.544/M.
  - Kottler's CMC value K₀ = √(3Λ) cancels Λ exactly; the horizon moves by ~10⁻²² for a 10 M☉ hole.
- **Black holes at α_c = 0:** moving holes are regular. The O(v) khronon is Kovachik–Sibiryakov's eq. (4.17), soft
  exponent √2 − 1; the aether is C¹ at the universal horizon (their "weak singularity"). The khronon is a stealth field and
  the sensitivity is 0.
- **Black holes at α_c > 0 with c₂ = ∞ — a first-order failure.** The khronon equation forces C₁ = 0 and gives
  μ ≈ −(4√3/27)(α_c/M) ln|r/(3M/2) − 1|, log-divergent at the universal horizon. This was checked two independent ways
  (to 5×10⁻⁹).
  - The multiplier's stress trace is 6μ̇ (its Weyl weight, checked), which diverges as α_c/(r − 3M/2): a curvature
    singularity at O(α_c).
  - At finite c₂ the decoupled static solutions are regular (they force U″(ξ_*) = 0); the limit is not uniform.
  - The expansion breaks down only inside the full theory's spin-0 layer, Δr ≈ (3/4)√α_c M (4×10⁻⁵ M at the cap).
    Whether a regular solution exists there is **OPEN**. Ramos & Barausse 2019 (full system, finite couplings) find singular
    moving holes; Kovachik & Sibiryakov 2023/25 find regular ones in the decoupling limit, which does not cover c₂ → ∞.
  - **FP14's "c₂ → ∞ is regular" is established on Minkowski and FRW, not on black holes.**
- **Ringdown:** GR's to O(α_c) ≤ 3×10⁻⁹. Tensor modes have c_T = 1 and are set at the light ring; the universal horizon is
  inside both horizons.
- **Criterion B:** a global preferred time exists on the exterior (the universal horizon is the leaf at τ = ∞), and no
  signal runs backward. Between 3M/2 and 2M the fast khronon and the leafwise-instantaneous channels do reach the exterior,
  which B allows. B's well-posedness clause is **open** at the universal horizon when c₂ = ∞.

**4. Inspiral (−1PN).**
- At LIGO frequencies the radiated scalar is the pure khronon. For GW170817, B = (5/32) C (s₁ − s₂)² ≤ 9.7×10⁻²³, against
  B ≤ 1.2×10⁻⁵ (90%; Abbott et al. 2019, PRL 123, 011102). δφ̂₋₂ = −4B/7.
- GW170817 alone bounds α_c only at ≤ 0.022 (with the ×3 bracket), far weaker than the PPN cap.
- GWTC binary black holes are **not** used. Their −1PN bounds need black-hole sensitivities, which vanish at α_c = 0 and
  are not established at α_c > 0, c₂ = ∞ (item 3). If s_BH = O(α_c), B_BBH ≲ 10⁻²¹.

**5. λ under H_S (the coordinator's item) — a regulator for strong-field physics, a knob in the MOND regime.**
- **Required > 0.** With the yield off (z < 0.635) and the band-pass closed, φ's row is 4λω²A_φ: no equation at λ = 0
  (FP13 A1, re-derived from FP14's block).
- **λ-inert across (0, 274.4]:**
  - every strong-field observable: the PPN λ-part is ≤ 6×10⁻⁷ of the bound at its scale, and the pulsar totals are
    unchanged;
  - H_S's σ₈ and forest at c₂ = ∞: spread 2.5×10⁻⁴, band kept, forest 0;
  - the static gates, which carry no λ.
- **Not λ-inert in the MOND regime.** At c₂ = ∞ the khronon contributes only 3 to λ_eff = λ + 3, so:
  - the tracking speed at C^Q = 100 falls from 17,300 to 1,800 km/s;
  - galaxy-outskirt α₂v² (620 km/s) rises from 1.3×10⁻³ to 0.12.

  λ is observable-inert only below ≈ 0.03 (1%). FP14's λ-inertness was measured at the c₂ floor, where λ_eff = λ + 277.
- **The upper bound is tracking:** λ ≤ 274.4 at c₂ = ∞. At FP2's c₂ floor the window is empty (λ_max ≈ −2×10⁻⁵, the floor
  constant's rounding), so FP13's λ > 0 needs c₂ > 7.289×10⁻³.
- **Strong coupling:**
  - About exact zero field the quadratic action is 2λφ̇² alone: Λ_sc = 0 for every λ, and the canonically normalised cubic
    coupling grows as λ^(−3/2).
  - In real backgrounds the khronon's inertia keeps ℓ_sc ≤ 1 mm as λ → 0.
  - Sub-ξ φ fluctuations (λ_eff = λ, invisible to the metric) reach ℓ_sc ≤ 1.5 cm.
  - No Cherenkov bound applies: the coupling at cosmic-ray k carries e^(−10⁵⁰).

## Controls (all pass on the final runs)
- **PPN:**
  - GR limit.
  - FP2's committed B3 α₁, α₂ strings EXACTLY, and FP7's committed D2 strings EXACTLY (blocks re-derived here).
  - **Yagi, Blas, Barausse & Yunes 2014 eqs. (48)–(49)** EXACTLY for general (α, β, λ), with their c_s² (eq. 118) and
    c_T² = 1/(1 − β). The chain maps as (α, β, λ)_BPS = (α_c, 0, c₂).
  - FP2's committed B4 numbers.
- **Radiation:**
  - Einstein's quadrupole formula from the residue machinery.
  - Yagi et al.'s dipole C and scalar 𝒜₁ term (eqs. 121–124) at three khronometric points, to 10⁻¹²; the c₂ = ∞ residues
    (1/(3α_c²), 1/12) analytically.
  - The numerical engine against the analytic σ = 0 values.
- **CMC:**
  - Estabrook's limit surface; Kovachik–Sibiryakov eq. (3.12) (the static current, from the action) and eq. (4.17) (the O(v)
    equation).
  - Exponents −1 ± √2 (Ramos–Barausse's −2 ± √2).
  - The record's L33 horizon formula, with its next order.
- **λ:**
  - FP13's committed H1 headline (σ₈ ×4, flagships ×4, SPARC, KiDS) EXACTLY, from FP13's code copied unchanged.
  - FP14's committed λ scan EXACTLY.
  - FP7 B6's 12 strong-coupling rows EXACTLY.

## Disclosures (every exploratory or failed run)
- **ppn:**
  - Two MUTATE runs preceded the final pair. P2's and P3's pre-declared absolute thresholds (10⁻¹¹, 10⁻¹²) failed at ~3×10⁻¹¹
    at 1 AU, where the only α₂ bound is LLR's.
  - Both were re-specified per scale (< 10⁻³ of that scale's bound). The as-run forms are kept as reported checks
    P2abs / P3abs, which FAIL in both final runs.
  - A coding error in K4 (a spurious 1/k², unsquared roots) was fixed.
  - The pair was re-run at the end on unchanged code.
- **radiation:**
  - The first MUTATE crashed after the controls: the TOV bracket overshot M_max, and was moved.
  - R-K1's midpoint angular grid failed at 1.2×10⁻⁵ and was replaced by Gauss–Legendre, which is exact.
  - A second MUTATE failed R-K3's 10⁻⁴⁰ threshold after the precision was lowered to 40 digits; the threshold is now 10⁻³⁰.
  - The first main run crashed in M2 (mpmath root finder); roots are now found by log-bisection.
  - An exploratory scan then showed the transition branch at ξ = 100 pc for α_c at its floor. H4/M2 was re-specified to
    classify cells by whether the filter is open on their radiated branch, not by ξ.
  - M2's positivity clause failed twice before its final form:
    - first on ±10⁻³⁷ roundoff of decoupled φ poles;
    - then because the khronon's own pole keeps its full residue when the filter is closed.

    The final form is: no negative spectral weight beyond roundoff anywhere, and strictly positive on coupled branches. A
    scratch diagnostic located both.
  - The pulsar rows and GW170817's row did not change across these runs.
- **cmc:**
  - The first MUTATE failed two check implementations:
    - K4 compared with the leading term only, at double precision; it now uses the next order and 60-digit roots;
    - N1's finite differences included the grid's first points; the grid is finer and r < 0.05R is excluded.
  - K3's tolerance was set to 10⁻¹⁰ for float-evaluated ratios.
  - Two slow symbolic paths were killed and rewritten: K3 is now numeric, and N2 linearises before simplifying.
  - A scratch exec of the first three sections wrote a scratch `.out` into this folder; it was deleted.
  - B3b (the Weyl-weight check) was added after the first main run; MUTATE and main were then re-run.
- **lambda:** L2 (λ_max ≥ 1) and L3 (observable-level λ-inertness, not the radiated coefficient's spread) were fixed before
  this lane's first run, after the radiation lane's numbers were known.
- Tracking's exact bound is 274.4; the PPN and radiation scans used 274.8, slightly beyond it.
- Neutron-star sensitivities use Foster's weak-field form with a ×3 strong-field bracket, not a strong-field O(v) NS solution.
  The black-hole analysis is first order in α_c.
- **Not covered:**
  - merger dynamics;
  - black-hole sensitivities at α_c > 0;
  - the full nonlinear black hole at c₂ = ∞.

## Files
`XR25_README.md`, `XR25_common.py`, and for each lane `ppn_preferred_frame`, `pulsar_radiation`, `cmc_compact_objects`,
`lambda_regulator`: `XR25_<lane>.py`, `.out`, `_MUTATE.out`, `_results.json`, `_results_MUTATE.json`.
