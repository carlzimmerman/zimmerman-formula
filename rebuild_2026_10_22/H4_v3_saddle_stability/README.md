# H4_v3_saddle_stability: is v3's khronon/dust pair healthy where the phantom density D·P < 0?

## Verdict (frozen rule, FROZEN_CRITERIA §4): ILL-POSED. Reading: CRISP FINDING.

- **The dispersion relation (weak field, first order in background gradients, with self-gravity):**
  ω² = ρ_τ [k²/χ(k) − 4πG], with χ(k) = k²/(4πG M_θ + γ_L k²) + μ_K²/(4πG) and ρ_τ = D·P + μ_K²(Q̄−1)/(4πG).
  - At μ_K = 0 this is **ω² = 4πG ρ_τ (M_θ − 1 + L★²k²/2)**, with M_θ ∈ [1+x, (1+x)²] from J_x (x = |∇Φ|/a₀).
  - ρ_τ is the khronon fluid's density: the phantom plus the BS dust.
- **Where ρ_τ < 0 the instability is UV-unbounded.** The growth rate is Γ = L★ k √(2πG|ρ_τ|) at large k, linear in k
  with no cap. This is a Hadamard ill-posed initial-value problem.
  - **γ_L is what makes it unbounded.** At γ_L = 0 (pure BS / AQUAL) the same regions have a bounded rate √(4πG|ρ_τ|(M_θ−1)),
    which gives only **0.006–0.20 e-folds** over each region's lifetime. The stiffness term that screens the Solar System
    gives no k⁴ stabilisation. It saturates the khronon fluid's compressibility at 1/γ_L, so the negative "pressure" grows
    as k².
- **Where ρ_τ < 0 (v3's own AQUAL static field, own solver):**
  - every two-body saddle: MW–M31, LMC–MW, a galaxy pair, a cluster pair;
  - with an external field, Mpc-sized equatorial lobes around every system, including single galaxies and discs.
  - **Isolated discs have no negative region on or off the plane** (MW-like and dwarf, both footings).
  - **Screening removes the region in the Solar System.** There D·P is a Yukawa-smoothed copy of the positive mass density
    plus the positive Galactic phantom: at least 0.045 M☉/pc³ (Sun–Earth and Earth–Moon saddles, the Sun–Galaxy null,
    out to 0.1 pc). The pair propagates there at P3's ~1e-4 c.
- **Growth against age.** Every wavelength shorter than λ₁ ≈ 4–330 pc (comparable to L★) grows by more than one e-fold over
  the region's lifetime. At λ = 1 pc that is 4–320 e-folds; at λ = 1 AU it is 0.9–6.7 × 10⁷.
- **No cutoff rescues it.** To keep a saddle below one e-fold, the theory would have to be cut off at wavelengths of tens of
  parsecs. Yet the same γ_L term must act at AU scales (k L★ ~ 10⁷) to screen the Solar System.
- **Nonlinear saturation is not plausible from v3's own terms.** See §3.

| system (illustrative inputs) | ρ_τ < 0 region | verdict (canonical / alt) |
|---|---|---|
| S1 MW–M31 (6e10 + 1e11 M☉, 780 kpc) | saddle, V^⅓ 290 kpc, median \|ρ\| 6.2e-7 / 6.8e-7 M☉/pc³; with g_e = 0.01 a₀, lobes V^⅓ 5.8–6.4 Mpc | ILL-POSED / ILL-POSED |
| S2 LMC–MW (6e10 + 3e9 M☉, 50 kpc) | 12 kpc region 3–9 kpc from the LMC, median 1.0e-4 / 1.1e-4 M☉/pc³ | ILL-POSED / ILL-POSED |
| S3 galaxy pair (5e10 + 5e10, 300 kpc) | saddle, V^⅓ 112 kpc, median 3.3e-6 / 3.6e-6; lobes with g_e | ILL-POSED / ILL-POSED |
| S4 cluster pair (1.5e14 + 1e14, 3 Mpc) | saddle, V^⅓ 0.96 Mpc, median 1.5e-6 / 1.7e-6; lobes with g_e | ILL-POSED / ILL-POSED |
| S5a MW-like disc, S5b dwarf disc | isolated: **none** (on or off the plane); with g_e = 0.01 a₀: equatorial lobes beyond ~40 kpc (MW) / ~6 kpc (dwarf) | ILL-POSED (through the external-field lobes) |
| S6 single galaxy in g_e = 0.01 a₀ | lobes, V^⅓ 3.5–3.9 Mpc, including the upstream null at ~0.7 Mpc | ILL-POSED / ILL-POSED |
| S7 Solar System (Sun–Galaxy, Earth–Moon) | **none**: screened D·P ≥ 0.045 M☉/pc³ | HEALTHY / HEALTHY |
| **overall** | | **ILL-POSED** |

None of these verdicts is dust-conditional. Every region survives a BS dust offset of 3 × 0.26 ρ_crit (the f = 3 maps).

**Checks: 13/14 PASS, exit 1.** The one FAIL is the frozen convergence line C2, kept as frozen (AMENDMENT A1, see below).
- **Mutation.** `H4_MUTATE=1` flips the sign of the first-order term. A4, A6, B2 and B3 FAIL (10/14).
  - The D·P > 0 parts then become unstable, so the Solar System and the isolated discs swap HEALTHY → ILL-POSED.
  - The saddles and lobes become the stable parts. The pair systems stay ILL-POSED because of their positive parts.
- **Run cost.** 171 s; peak RSS 0.45 GB (parent) and 0.88 GB (worst child, one solve per process); one thread; nice 15;
  no downloads. The heavy queue was not touched.

κ = ½ FITTED. Footings 9.36e-11 / 1.13e-10 m/s², never pooled. No dark-matter particle. Not "theory closed". Nothing here says
the data favour the framework.

## 1. The dispersion relation (Part A, sympy; all residuals identically 0)

- **A1. PN Lagrangian.** BS24's PN system with the J term replaced by C4's P sector:
  L = −|∇φ|²/2K − ρ_mφ + P·∇Ξ − W(K|P|) − (γ_L/2)(∇·P)² + μ_K²Ξ²/2K, with Ξ = φ − σ̇ + |∇σ|²/2.
  - The σ equation is exactly the khronon continuity equation ∂_tρ_τ + ∇·(ρ_τ v_τ) = 0, with ρ_τ = ∇·P − μ_K²Ξ/K and
    v_τ = −∇σ.
  - The φ equation is Poisson with ρ_m + ρ_τ.
  - The static limit with P eliminated is AQUAL with μ = x/(1+x).
- **A2. Covariant check of the leaf divergence.** On Minkowski with τ = t + εσ and P ⊥ n:
  - D·P = ∇_μP^μ − P^μA_μ holds identically.
  - The tilt term −P0·∇σ̇ in ∇_μP^μ cancels exactly against the one in P·A. So at O(ε), D·P = ∂_ip_i, and the γ_L term
    puts no P0 into the kinetic term.
  - Without this cancellation γ_L P0²k²ω² would dominate the kinetic term above k ~ 1/(10⁸ m) (hand estimate at u ~ a₀,
    L★ = 24 pc). Checking it was essential.
- **A3. Covariant decoupling, plane-symmetric.**
  - The O(ε²) clock term is −½(∂_zP0_z)σ_z² − pσ_tz plus a total derivative (Euler operator 0).
  - Integrating p out gives χ = k²/(KM + γ_Lk²), which is P3's E1.
  - The W(K|P|) tilt term (|P|² ⊃ −P0²σ_z²) is post-Newtonian order, of relative size g·ℓ/c².
- **A4. PN linear system.** It has Poisson, the full anisotropic W Hessian, continuity and Bernoulli; WKB on a frozen
  background. det = 0 gives ω² = ρ_τ(k²/χ − K) exactly, and it has two limits:
  - **γ_L = 0** reproduces the record's BSK1 M4 (`real_research/bs_khronon_2026/BSK1_moving_source_gate.py`
    L208–240), with f_θ = 1 − 1/M_θ.
  - **No Poisson feedback** reproduces P3's decoupled ω² = ρ_τk²/χ, i.e. c_π² = G/Z.
  - P3's decoupling limit therefore drops the self-gravity term −4πGρ_τ. That term is the same order when kL★ ≲ 1 and
    negligible when kL★ ≫ 1.
- **A5. J_x.** M_T = 1 + x and M_L = (1+x)², from both μ and W.
- **A6. Second frame.** The dispersion is linearised from the nonlinear Bernoulli and continuity about a uniformly moving
  background. It becomes (ω − k·V)² = ρ_τ(k²/χ − K), so the growth rates do not depend on the frame.
- **B1. Limits.**
  - lim ω²/k² = γ_L Kρ_τ/(K + γ_Lμ_K²): non-zero, so Γ ∝ k where ρ_τ < 0. **UV-unbounded.**
  - At γ_L = 0, lim ω² = Kρ_τ(M_θ − 1): finite, so bounded.
- **B2. Without WKB (1D periodic slab, variable ρ_τ(x), Fourier–Galerkin eigenproblem).**
  - With γ_L > 0 the largest growth rate doubles with every doubling of resolution: 7.1, 14.6, 29.8, 60.6. Ratio
    2.03, against the [1.8, 2.2] line. This is the Hadamard signature.
  - With γ_L = 0 it converges to 1.224714, against the prediction √(K(M−1)|min ρ|) = 1.224745.
- **B3. P3's sign convention.** All 48 of P3's E4 rows where self-gravity is negligible are reproduced to 6e-14, both
  footings and every L★. These are lab, planets, double pulsar, BHs and NS, all with D·P > 0 and real c_π.
  - P3's galaxy row is the exception (kL★ = 0.024). There the self-gravity term lowers c_π by 0.866, from 1.57e-4 to 1.36e-4.
  - P3's cosmology row at k = 10 h/Mpc is on the dust's Jeans branch (structure growth), not a sound mode. Neither changes
    a P3 verdict.

## 2. Where ρ_τ < 0 (Part C: own axisymmetric AQUAL solver)

- **The solver.** It is a node-centred finite volume code on a graded (R, z) grid, solved by damped Picard iteration to a
  nonlinear residual below 1e-8, with μ = x/(1+x). Each system is solved at two resolutions, both footings. External fields
  lie along the symmetry axis.
- **C1. Validation against the record.**
  - A single deep lens gives 4πr²ρ = 1 to 0.5 %.
  - The isolated equal deep pair gives C(0.2d) = −0.24049, against A38's −0.2413 (−0.33 %) and A23's −0.2404.
  - In A23's external-field sweep, e = 0.3 gives −0.0218 (A23 −0.0315) and e = 0.68 gives +0.168 (A23 +0.145).
- **The external field does not remove the negative regions; it moves them.** For the deep equal pair, the negative volume
  inside 3d is:

  | e | negative volume inside 3d |
  |---|---|
  | 0 | 0.056 d³ |
  | 0.3 | 0.059 d³ |
  | 0.68 | 47.3 d³ |

  - A23 is right that the mid-plane saddle fills.
  - But equatorial lobes open around the whole system. Their density is ρ_ph ∝ P₂(cos θ)/r³, negative in the plane
    perpendicular to g_e.
  - At f = 0 the lobes reach the box. The f = 3 dust offset bounds them at 1.2–1.5 Mpc.
- **C2 (frozen): FAIL, kept.** The base → fine median depth changes by 11.1 % (S4 alt) and 11.0 % (S2 canonical), against
  10 %. All other maps change by ≤ 5.6 %, and every volume by ≤ 4.0 %.
- **C2b (AMENDMENT A1, post-result): PASS.** The extra-fine level changes the fine level by ≤ 0.8 % in volume and ≤ 1.2 % in
  median, on the four unequal isolated maps. So the base level was too coarse; the reported fine numbers are converged.
- **C3. Solar System, screened linear response about the Galactic P background.**
  - δ(D·P) = ρ_m ∗ K_ℓ with kernel 1/(M_θ − 1 + ℓ²k²), ℓ = L★/√2. It is bounded below by
    (1/4πℓ²r)(1 − √(m_max) r/ℓ), with m_max = 2x_e + x_e².
  - The Galactic phantom at the Sun is +0.045 / +0.051 M☉/pc³ (S5a in-plane, canonical / alt).
  - The minimum D·P over 72 samples is +0.045 M☉/pc³. The samples cover both footings, every L★, x_e = 1.15 and 2.6, the
    Sun–Earth and Earth–Moon Newtonian saddles, the Sun–Galaxy null at ~4,500–7,400 AU, 100 AU and 0.1 pc.
  - So unscreened AQUAL's "MOND bubbles" at Newtonian saddles do not exist in v3.

## 3. Growth against age (Part D; median depth over the near zone; T = min(T_H, ℓ₋/v), illustrative speeds)

| region | T (Gyr) | N, bounded branch (no γ_L) | N(λ = L★) | N(1 pc), L★ floor → 90 pc | N(1 AU) | λ₁ (pc) |
|---|---|---|---|---|---|---|
| S1 MW–M31 saddle (can / alt) | 2.6 | 0.10 / 0.10 | 2.2 / 2.3 | 47–194 / 52–203 | 1e7–4e7 | 47–195 / 52–204 |
| S1 with g_e (lobes) | 13.8 | 0.04 | 1.2 / 1.4 | 26–108 / 32–125 | 5e6–3e7 | 26–125 |
| S2 LMC–MW | 0.04 | 0.06 | 0.41 / 0.42 | 9–36 / 10–38 | 2e6–8e6 | 9–38 |
| S3 galaxy pair | 0.73 | 0.09 | 1.4 / 1.5 | 31–127 / 34–133 | 6e6–3e7 | 31–133 |
| S4 cluster pair | 0.94 | 0.20 | 1.3 | 27–111 / 30–116 | 6e6–2e7 | 27–118 |
| S4 with g_e | 13.8 | 0.006 | 0.19 / 0.22 | 4–17 / 5–20 | 9e5–4e6 | 4–20 |
| S5a MW disc with g_e | 10 | 0.04 | 1.1 / 1.3 | 24–101 / 30–116 | 5e6–2e7 | 24–116 |
| S5b dwarf disc with g_e | 10 | 0.10 / 0.11 | 3.1 / 3.6 | 68–280 / 82–324 | 1e7–7e7 | 68–326 |
| S6 galaxy in g_e | 10 | 0.04 | 1.1 / 1.3 | 24–101 / 30–116 | 5e6–2e7 | 24–116 |

- **Reading the table.**
  - The "imaginary sound speed" is L★√(2πG|ρ_τ|) ≈ 3 m/s at the MW–M31 saddle, so the e-folding time is λ/(2π · 3 m/s):
    53 s at λ = 1 km.
  - For the isolated saddles the maximum depth, excluding the cells next to null points, is 7–14× the median. In the
    external-field maps the maximum sits near the saddle or null, while the median is set by the far lobes. The AQUAL null
    cusp is integrable and is smoothed by L★.
- **Nonlinear saturation (reading).**
  - The khronon charge is conserved (A1), so a negative region cannot dissolve.
  - Where a perturbation makes ρ_τ locally positive, that patch stabilises. Where it makes ρ_τ more negative, the patch grows
    faster, and fastest at the shortest wavelengths.
  - v3's action offers no term that stops this cascade: no k⁴ term, no pressure, and the W cap is inactive in the UV branch.
    It ends where the theory stops being valid: at khronon caustics (|∇σ| → c, Q → 0) or at strong coupling.
- **The μ_K² hydrostatic dust (reading, estimate).**
  - At μ_K = 0.1 Mpc⁻¹ (S4's guard edge) it is 1e-4 to 0.5 of the isolated saddle depths. So it fills none of the saddles,
    though it could fill the shallowest lobes.
  - At BS's cap it would be 1–5000× the saddle depths. But that μ_K is excluded by S4, it changes the static solution, and
    S4 finds the hydrostatic dust itself goes negative where ψ > 0. So no μ_K removes every ρ_τ < 0 region.

## 4. Attempts to break the answer

| attempt | result |
|---|---|
| second route: covariant Stückelberg decoupling (A2, A3) vs PN fluid system (A4) | same kinetic χ and same gradient coefficient (−D·P0); the tilt-term cancellation verified, not assumed |
| frame change (A6) | uniform boost gives (ω − k·V)²: rates unchanged |
| no-WKB check (B2) | resolution-growing rate with γ_L, convergent without |
| sign convention vs P3 (B3) | 48 P3 rows reproduced to 6e-14; the D·P > 0 speeds come out real; the sign that gives P3's 1e-4 c and 0.44 c gives imaginary speeds where D·P < 0 |
| record limits | γ_L = 0 is BSK1 M4 exactly; no Poisson is P3 exactly |
| mutate (first-order sign flipped) | A4, A6, B2, B3 FAIL; the instability moves to the D·P > 0 regions (Solar System ILL-POSED) |
| dust offset f = 3, μ_K estimate | no region removed |
| external field | it moves the negative regions into lobes; it does not remove them |
| solver | reproduces A38 to 0.33 % and A23's sweep; C2 FAIL kept, C2b shows fine is converged to ≤ 1.2 % |

## 5. Corrections to the record

- **P3 README L131** says "G < 0 regions are untested". This lane tests them: ILL-POSED (UV-unbounded). Also, P3's E1/E4
  c_π² = G/Z omits −4πGρ_τ (see A4). The galaxy row is then ×0.866 and the cosmology row is the Jeans branch. No P3 verdict
  changes.
- **C5 README L7** says "no gradient instability on any background tested where the frozen-coefficient (WKB) expansion is
  valid". That holds at leading WKB order only. At first order in background gradients the khronon pair is
  gradient-unstable wherever ρ_τ < 0, with Γ ∝ k.
- **C8 README L41** lists the coupled system's local well-posedness as OPEN. This lane answers it: ill-posed where ρ_τ < 0.
  C8's WELL-POSED verdict stands for the leaf (P, lapse) problem only.
- **BSK1 M5a** (`BSK1_moving_source_gate.py` L301) says "the static MOND halo is a stable state iff 0 < f_θ < 1". That
  assumes ρ_τ > 0. Where ρ_τ < 0 (saddles, external-field lobes) the BS fluid is unstable even for 0 < f_θ < 1. The
  instability is bounded and gives < 0.2 e-fold here.
- **THEORY_V3_DRAFT** needs an update: §3 "instantaneous constraints / well-posedness: WELL-POSED" (L56) and the P3 row's
  "OPEN: possible gradient instability where D·P < 0 (lane H4)" (L81). This lane does not edit those files.
- **A23** (L9, "the dip does not survive") is right about the mid-plane column. But negative phantom regions survive the
  external field as lobes. That matters for health, not for its lensing test.

## What this does not show

- **Scope of the analysis.** It is linear, and first order in background gradients. B2 tests one variable-coefficient
  case without WKB.
  - There is no nonlinear evolution and no proof that some unlisted term stabilises the UV.
  - The action at β = η = γ_F = 0 has none: C5/C8's structure, A2, A3.
- **Geometry.** The maps are axisymmetric. External fields perpendicular to a pair's axis and real many-body
  configurations are not solved. The negative regions are generic in AQUAL (every null point, every external-field lobe),
  so the verdict does not rest on the symmetry.
- **Inputs.** Masses, separations, speeds and lifetimes are ILLUSTRATIVE. The verdict needs only one ρ_τ < 0 region larger
  than 900 pc, and every pair gives one with margins far above factor-2 changes.
- **Strong fields** (NS, BH) are not re-analysed. P3's backgrounds have D·P > 0.
- **No EFT cutoff is derived anywhere in the record.** The cutoff reading in the verdict is an argument, not a computation.

## Execution history (AMENDMENT A1, 002b19eedc, post-result)

1. **Run 1** (kept as `*_RUN1.*`): 12/13, C2 FAIL. It had two code defects:
   - the null finder took the box edge for isolated pairs, so the saddle null of the unequal pairs was not refined;
   - the Picard loop stopped on relative change, with residuals up to 7e-4.
2. **Run 2** was aborted by hand and wrote no outputs. The spherical boundary potential had been integrated from
   r = 1e-6, which cost precision. One child process reached **1.05 GB RSS, over the 1 GB budget** (disclosed).
3. **Run 3** is the production run, after the fixes. Its outputs are the files below.
- No pass line or verdict rule was changed. C2b was added post-result; it was not blind, because a development test had
  given 0.05–0.6 %.

## Input ledger (full: `ASSUMPTION_LEDGER.md`)

| input | class | source |
|---|---|---|
| v3 action; BS24 PN system (transcribed, re-derived in A1) | FRAMEWORK-NATIVE / EXTERNAL (PROVISIONAL transcription) | C4, C5, C8, BSK1 |
| AQUAL μ = x/(1+x), J_x masses | FRAMEWORK-NATIVE | C4 K2, C5 |
| a₀ footings, κ = ½, L★ grid {21.7/22.9, 24, 90} pc | FITTED | doors BRIEF, D10 |
| A38/A23 saddle numbers, P3 E4 rows, BSK1 M4 | FRAMEWORK-NATIVE record, cross-checks only | A38, A23, P3, BSK1 |
| masses, separations, scales, speeds, lifetimes, g_e = 0.01 a₀ | ILLUSTRATIVE | FROZEN_CRITERIA §3 |
| Ω_K = 0.26, H₀ = 68.6 (dust offset) | EXTERNAL (BS25 via C4) / FRAMEWORK-NATIVE | C4 K7, BRIEF |
| x_e = 1.15–2.6 at the Sun | FRAMEWORK-NATIVE / SURVEY-CALIBRATION | C5 inputs (D7d) |

No ΛCDM-processed input and no standard-MOND machinery carries a verdict. QUMOND is not used, and no raw survey data are
used.

## Files

- `h4_v3_saddle_stability.py` writes `.out` and `_results.json` (main run) and `_MUTATE.out` and `_results_MUTATE.json`
  (mutation run, `H4_MUTATE=1`).
- `*_RUN1.*` hold the disclosed first run.
- To run: `OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/H4_v3_saddle_stability/h4_v3_saddle_stability.py`.
  It is deterministic (it re-executes itself with PYTHONHASHSEED = 0) and solves each AQUAL case in its own process.
