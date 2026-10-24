# X3_switched_stiffness: does −(γ_L/2)[max(D·P, 0)]² make v3 well-posed where ρ_τ < 0, with its screened statics unchanged?

## Verdict (frozen rule, FROZEN_CRITERIA §3): WELL-POSED + STATICS UNCHANGED (with four qualifiers). Reading: CRISP FINDING, scoped.

- **Well-posed where ρ_τ < 0.** The switch turns the stiffness off exactly where D·P < 0. With non-negative dust, that
  covers every point where ρ_τ < 0.
  - There the khronon pair falls back on H4's bounded γ_L = 0 branch: ω² → Kρ_τ(M_θ − 1) as k → ∞.
  - The fluid's nonlinear sound speed squared is c² = γ_L(D·P + ρ_d)Θ(D·P), which is ≥ 0 for every state.
  - The slab rate converges to the localised-mode value 1.224745 (zero dust, both γ_L) and 1.183216 (dust buffer).
    H4's v3 operator doubled per doubling (2.03; this lane's discretisation with the switch removed gives 2.0007).
- **Statics unchanged.**
  - **Solar System / Cassini (C6):** D·P > 0 everywhere within 1 kpc of the Sun, with margin ≥ 1.8 × 10⁴. So C6's solution
    is exactly the switched one (lemma).
  - **Outer globulars (D10):** the clusters' external-field lobes do have D·P < 0, but only at r ≈ 180–1555 pc, far
    outside L★. Inside L★, D·P ≥ +0.076 M☉/pc³ at the floor (≥ +2.4e-3 at L★ = 90 pc). The full D10 re-solve (9000 + 2250 switched solves) moves the floor by
    +0.006 % (canonical, 21.682 pc) and +0.005 % (alt, 22.849 pc). Every band cell moves ≤ 0.042 %, and σ_p moves
    ≤ 3.5e-5.
  - **Strong field (P3):** all 60 P3 rows have D·P > 0, and isolated spherical solutions have D·P ≥ 0.
- **Qualifiers (printed with the verdict).**
  1. **Dust.** Well-posedness needs ρ_d ≥ −D·P wherever D·P > 0. That holds for v3's positive BS dust in the μ_K → 0
     regime. It fails wherever negative dust sits inside a stiff region; S4's hydrostatic dust at μ_K ≥ 0.1 Mpc⁻¹ is
     such a case, and S4 excludes that μ_K.
  2. **Knife edge at zero dust.** The result rests on the switch surface coinciding exactly with ρ_τ = 0. A scheme that
     lets the stiffness act next to a ρ_τ < 0 face grows as N^0.497 (C3b). Smoothing the switch reintroduces c² < 0
     (B2-S). Numerical work needs sign-consistent schemes.
  3. **A bounded instability remains.** Where ρ_τ < 0, H4's γ_L = 0 branch gives 0.006–0.20 e-folds (median) and ≤ 4.2
     at the deepest cells. That is physics, not ill-posedness.
  4. **Strong coupling.** On the D·P < 0 side the pair has no gradient term (c_π = 0), so P3's estimate gives Λ = 0
     there, as in BS's γ_L = 0 theory. The switch trades the Hadamard instability for an EFT-validity question in
     saddle regions (E1).
- **Checks 13/13 PASS, exit 0.** `X3_MUTATE=1` (switch removed) fails B1-S, B2-S, B3-S, C1, C2 and D1 (6/12, exit 1).
- **Run cost.** Main 72 s. Production took 7 runs of 9–30.3 min. The 27-min guard is checked between 3–7 min blocks, so
  **two runs ended at 30.1 and 30.3 min, over the 30-min rule by ≤ 20 s** (disclosed). Worst process 0.53e9 bytes (≈ 0.49 GiB). One thread, nice 15,
  no downloads. The heavy queue was not touched.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² (9.36e-11 / 1.13e-10 inside reused H4 code), never pooled. No
dark-matter particle. Not "theory closed". Nothing here says the data favour the framework.

## 1. The switched operator (Part B; sympy, all residuals identically 0)

v3 with one change, zero new constants: L ⊃ −(γ_L/2)[max(D·P, 0)]², γ_L = K L★²/2, K = 4πG. The switch is exact. It is not
smoothed and has no threshold.

**Dispersion on each side (B1-S; JSON `B1S`).** The linear system is H4's A4 system with the stiffness multiplied by
Θ(D·P₀).
- **D·P₀ > 0 (stiff side):** exactly H4's ω² = ρ_τ[k²/χ − K], χ = k²/(KM_θ + γ_Lk²) + μ_K²/K.
  - At μ_K = 0 this is ω² = Kρ_τ(M_θ − 1 + L★²k²/2).
  - It is ≥ 0 wherever ρ_τ ≥ 0, since M_θ − 1 ≥ 1.0e-4 over 2e4 J_x samples.
- **D·P₀ < 0 (soft side):** ω² = ρ_τ[k²/χ₀ − K], χ₀ = k²/(KM_θ) + μ_K²/K. This is H4's γ_L = 0 branch.
  - lim ω²/k² = 0 and lim_{k→∞} ω² = Kρ_τ(M_θ − 1), which is finite.
  - **The UV growth is bounded where ρ_τ < 0.**

**Nonlinear principal part (B2-S; JSON `B2S`).** In 1D the PN system is exactly a barotropic Euler fluid.
- The σ Euler–Lagrange equation is continuity for ρ_τ = s − μ_K²Ξ/K, with s = ∂_zP (residual 0).
- The P equation plus the Bernoulli definition give D_t v = −∂_z[(γ_L/2)F′(s)] + KW′(KP) − ∂_zφ (residual 0).
- The frozen-coefficient principal symbol is ω² = c²k², with c² = (s₀ + ρ_d)(γ_L/2)F″(s₀).
- The three cases:

  | stiffness F(s) | c² | sign |
  |---|---|---|
  | switch, max(s,0)² | γ_L(s₀ + ρ_d)Θ(s₀) | ≥ 0 on both branches for any state with dust ρ_d ≥ 0 |
  | v3 as written, s² | γ_L(s₀ + ρ_d) | −γ_L s_n < 0 at s₀ = −(ρ_d + s_n) |
  | any smoothing, e.g. [(s + √(s² + ε²))/2]² | εγ_L(5√2 − 8)/16 ≈ −0.058 εγ_L at s₀ = −ε | < 0 for every ε > 0 |

- So the switch cannot be smoothed. Any convex F with F″ > 0 somewhere on s < 0 puts c² < 0 there, and the Hadamard
  instability returns. The exact max(s, 0) is the unique choice in this family; no new constant is needed or admissible.

**Interface D·P = 0 and the leaf problem (B3-S plus derivation; scored parts: C¹, convexity, E_s ≤ E_v3 with equality
iff D·P ≥ 0, scalar reduction).**
- **The switched leaf functional is convex and has a unique solution.** It is C8's
  E[Φ, P] = ∫|∇Φ − KP|²/2K + g(K|P|) + (γ_L/2)(∇·P)₊² + ρΦ.
  - (s₊)² is C¹ and convex (second derivative 2 / 0 on the two branches).
  - It stays strictly convex through g, which is strictly convex in the vector P (g′ = u²/K(a₀−u) > 0 and g″ > 0 for
    u > 0). So there is at most one minimiser.
  - Existence follows from the direct method, as in C8. The stiffness term is weakly lower semicontinuous because
    ∫(s₊)² = sup_{φ≥0}[−2∫P·∇φ − ∫φ²].
  - The leaf problem is therefore still uniquely solvable.
- **What is lost.** C8's principal-symbol bound ≥ min(K, γ_L|ξ|²) now holds only on {D·P > 0}. On {D·P < 0} the
  longitudinal P is algebraic, as in AQUAL (C8's γ_L = 0 case, where uniqueness rests on g). The leaf problem becomes a
  free-boundary (obstacle-type) problem.
- **Interface conditions on Σ = ∂{D·P > 0}:**
  - Φ ∈ C¹ (Gauss's law with a bounded source).
  - The tangential P is continuous, because ∇_t s₊ = 0 on Σ.
  - s₊ is continuous, so D·P → 0 from the stiff side.
  - The normal P is continuous and ∂_n s₊ = 0 (smooth fit). A jump in P·n would put a surface layer into D·P: a positive
    layer has infinite stiffness energy, and a negative one contradicts s₊ ≥ 0 at the boundary of the stiff set.
  - D·P itself may jump downward across Σ, to the AQUAL value on the soft side.
  - The scalar reduction p = ∇χ/(1 + |∇χ|) with χ = Φ + (L★²/2)(∇·p)₊ holds exactly (C6/D10 structure).
- **Lemma (statics).** If the v3 minimiser has D·P ≥ 0 a.e., it is the unique switched minimiser: E_s ≤ E_v3 pointwise,
  with equality there, and every directional derivative is ≥ 0. Where D·P < 0 on a set of positive measure, the two
  solutions differ. The isolated cases of D1(a) confirm it to 8e-14.

**3D bound (derivation).** With 𝓛 = H − KΠ_L − ∇γ(x)∇· and γ = γ_LΘ(D·P₀), the test field r = q·1_{D·P₀≤0} gives
Γ² ≤ K·max_N[M_L |ρ_τ|], uniformly in k. In 1D the sharp form is Γ² ≤ K(M − 1 + f₋)·max_N|ρ_τ|. Localised modes approach
K(M−1)·max_N|ρ_τ|.

## 2. Slab test (Part C; 1D periodic, no WKB; JSON `C`, `C_verdict`)

**Setup.** H4 B2's model: K = 1, M = 2, s₀ = −0.5 + cos 2πz. Own staggered finite-volume discretisation: Θ on nodes,
ρ_τ on faces, and a periodic Poisson term that removes the mean. Γ² is the largest generalised eigenvalue.

| ladder | discretisation | Γ per level | finest ratio | verdict line |
|---|---|---|---|---|
| H4 B2 (H4's own code, A0b) | Fourier–Galerkin, v3 | 7.14, 14.62, 29.84, 60.57 (N 64–512) | 2.0295 | reproduced to 0 |
| C0 | own FV, switch removed, γ_L 1e-3 | 5.04, 9.92, 19.80, 39.61 | 2.0007 | PASS (H4's divergence) |
| C0 | own FV, γ_L = 0 | 1.224253 … 1.224737 | 1.000019 | PASS |
| **C1** zero dust, aligned (N 96–1536) | switch, Θ(0) = 0 | 1.22453, 1.22469, 1.22473, 1.22474, 1.22474 (both γ_L 1e-3, 1e-2) | 1.0000 | **PASS** (bound 1.58114; 0 sign violations) |
| **C2** dust 0.1, H4's grid (N 64–1024) | switch | 1.18271, 1.18309, 1.18318, 1.18321, 1.18321 (both γ_L) | 1.0000 | **PASS** (bound 1.51102; 0 violations) |
| C3a zero dust, H4's grid (N 64–2048) | switch, not sign-consistent at alternate levels | 1.2243 → 1.2247, flat | 1.000 | diagnostic |
| C3b zero dust, aligned | Θ(0) := 1 | γ_L 1e-2: 1.2245, 1.4613, 2.0371, 2.8664, 4.0461; γ_L 1e-3: 1.2247 → 1.282 at N 1536 | 1.412 / 1.047; slope 0.497 / 0.066 | diagnostic: **grows as N^½** |

C1 and C2 converge to the localised-mode values √(K(M−1)·max|ρ_τ|) = 1.224745 and 1.183216 to better than 1e-5,
independent of γ_L. (JSON `C`: `C1_0.001`, `C1_0.01`, `C2_*`, `C3a_*`, `C3b_*`.)

- **Why C3 matters: a knife edge at zero dust.** The continuum switched operator is well posed. But if a discretisation
  (or any physical modification) lets the stiffness act at a point next to ρ_τ < 0, a grid-scale mode straddling that
  point grows as h^−½.
  - **C3b shows it.** Θ(0) := 1 at the interface node makes the slope d ln Γ/d ln N = 0.497 at γ_L = 1e-2.
  - **C3a did not grow up to N = 2048.** There the interface nodes fell at h/3 or 2h/3 from the zero, and the positive
    neighbour face outweighs the negative one.
- **With positive dust there is a finite buffer.** The stiffness acts on {s₀ > 0}, ρ_τ < 0 only on {s₀ < −ρ_d}, so a
  layer of width ρ_d/ρ′ separates them. C2 converges on H4's unaligned grid at every level.
- **Consequence.** Numerical work on the switched theory needs sign-consistent schemes (the analogue of
  positivity-preserving schemes for degenerate fluids; unverified reading, from memory, no lookup). The physical
  well-posedness rests on ρ_τ − D·P = ρ_d ≥ 0.

## 3. Statics (Part D)

**D1: the switched D10 solver is validated (JSON `D1`).**
- (a) Isolated cases have min D·P = +2.2e-9 > 0, and switched equals unswitched to 8e-14 (the lemma).
- (b) With s_g = +1e6 it equals v3; (c) with s_g = −1e6 it equals AQUAL. Both agree to 0.
- (d) Six D10 production cells and D10's central floors (21.680757 / 22.847696 pc) are reproduced exactly.
- (e) Doubling the grid and r_out × 10 changes σ_p by ≤ 7.4e-5.

**D2: C6 Solar System (JSON `D2`).**
- **The Galactic phantom.** From H4's own MW-like disc solver: +0.0447 / +0.0514 M☉/pc³ at the Sun (H4 json identical).
  Its minimum over R 7.2–9.2 kpc, |z| ≤ 1 kpc is **+0.0055 / +0.0062** at (9.0, −0.98) kpc.
- **The Sun's own response does have negative lobes.** In a uniform field (D10's solver, x_e 1.15 / 2.6) they are
  equatorial, at r ≥ 25–170 pc, and at most **3.1e-7 M☉/pc³** deep.
- **Margin.** Total D·P > 0 everywhere inside 1 kpc. Margins run 1.8e4 to 3.2e6 over 12 cells (both footings, L★ floor /
  24 / 90 pc, x_e 1.15 / 2.6).
- **Near zone.** H4's C3 near-zone minimum (≤ 0.1 pc) is +0.045.
- **So C6's Q₂, the planets and the wide binary are unchanged exactly** (lemma). The nearest negative region is the MW's
  external-field lobes at R ≥ 40.7 kpc. Their effect is ~(L★/R)² = 2.8e-7, an estimate.

**D3: P3 strong field (JSON `D3`).** All 60 P3 E4 rows have G_hat > 0. Isolated spherical screened solutions
(y 1e-3–300, Λ 0.1–10) have min/max D·P = +1.6e-7, with every BVP converged. The switched and v3 Euler–Lagrange equations
coincide pointwise where D·P ≥ 0, so P3's BH/NS solutions remain solutions.

**D4: D10 outer globulars.**

*Unswitched D·P maps* (JSON `D4_maps`; Υ 1.6, E_mid; total D·P includes the Galactic phantom at R_GC,
4.6e-5–1.2e-4 M☉/pc³):

| cluster (canonical, L★ floor) | D·P < 0 region | depth | min D·P inside L★ | σ_p switched / v3 − 1 |
|---|---|---|---|---|
| NGC 2419 | r 304–1555 pc | −3.3e-3 | +2.5 | +3e-7 |
| Pal 3 | r 192–502 pc | −2.5e-4 | +0.13 | +2.0e-5 |
| Pal 4 | r 183–580 pc | −4.1e-4 | +0.22 | +1.8e-5 |
| Pal 14 | r 179–319 pc | −1.5e-4 | +0.084 | +3.5e-5 |

- So D·P < 0 does occur in D10's setting: in each cluster's equatorial external-field lobes, 2–20× deeper than the
  Galactic phantom. At L★ = 90 pc the lobes are filled.
- But it occurs only at r ≳ 8 L★, where the stiffness term is already O((L★/r)²). That is why the screened result does
  not move.

*Production* (JSON `D4`; 9000 switched solves plus 2250 for the s_g = 0 variant; 0 unconverged; worst residual 1.0e-10):

| footing | central L★95 switched / D10 | change | band (P1–P3 × E_lo/mid/hi) | D10 lines under the switch |
|---|---|---|---|---|
| canonical | 21.682 / 21.681 pc | +0.006 % | 2.93–22.67 pc, every cell ≤ +0.042 % | FLOOR HOLDS; STRADDLES 20 pc; AQUAL excluded in all cells |
| alt | 22.849 / 22.848 pc | +0.005 % | 4.40–23.80 pc, every cell ≤ +0.034 % | same |

- s_g = 0 variant (no Galactic phantom in the switch): 21.683 / 22.850 pc.
- max |Δσ_p/σ_p| at Υ 1.67, E_mid, L★ 20–90 pc = 3.5e-5.

## 4. Secondary (Part E; report only, no verdict weight)

- **E0.** P3's A69 estimate is reproduced exactly from P3's json rows.
- **E1, strong coupling (JSON `E1`).**
  - **Stiff side, at the H4 saddle depth:** c_π is 0.08–72 m/s, and the strong-coupling length 2π c_π/Λ is 3 mm–0.45 m.
  - **Near the interface:** at ρ_τ = 1e-9 × that depth, c_π ≲ 2.3e-3 m/s and the length is 7 m–1.1 km. The loop factor at
    k = 1/L★ stays ≤ 4.3e-63. So a strongly coupled layer hugs the interface, but it is thin.
  - **Soft side:** the switch removes the pair's gradient term (c_π = 0), so P3's estimate gives Λ = 0 at every k. This
    is BS's own γ_L = 0 situation (C5: "at γ_L → 0 the coupling diverges").
  - **Reading.** The switch cures the Hadamard instability but leaves the D·P < 0 regions outside the weakly coupled EFT,
    by P3's criterion. Whether that matters needs a non-relativistic (dust-like) strong-coupling analysis, which is not
    done here.
- **E2, Lifshitz regulator β(∇·n)², unswitched v3 + β (JSON `E2`; C5 × H4 superposed, ESTIMATE).**
  - **Update (X15, 2026-10-24):** the factor B = βc²/(2 + 3β) is exact, not an estimate. X15's unitary-gauge linear system (GR + P sector + switched stiffness + β) has exactly this khronon root, ω² = βk²(M − 1 + Θ L★²k²/2)/(2 + 3β).
  - At β = 1e-9 (C5's estimated upper edge), the worst e-folds equal H4's bounded branch (0.006–0.20), so the γ_L k² growth
    is fully regulated.
  - At β = 1e-15 they are ≤ 0.29. At β = 1e-18 they reach 0.007–8.9.
  - The worst median region (LMC–MW, alt) reaches 1 e-fold at β = 8.0e-17.
  - **So a Lifshitz term with 1e-16 ≲ β ≲ 1e-9 would also cure H4.** But β is a new constant in v3 (β = 0 in v3), and C5
    flags an infrared band at β > 0 with BS dust. It is not adopted. The switch needs no constant.

## 5. Checks

| check | result | key number |
|---|---|---|
| A0a | PASS | H4's A4 block re-executed verbatim: dispersion and both B1 limits equal H4's json (residual 0) |
| A0b | PASS | H4's `gmax` ladder reproduced to 0; ratio 2.0295 |
| B1-S | PASS | stiff side = H4; soft side UV limit Kρ_τ(M_θ − 1), ω²/k² → 0 |
| B2-S | PASS | c² = γ_L(s₀+ρ_d)Θ(s₀) ≥ 0; v3 −γ_L s_n; smoothing −0.058 εγ_L |
| B3-S | PASS | C¹, convex, E_s = E_v3 iff D·P ≥ 0, reduction exact |
| C0 | PASS | 2.0007; γ_L = 0 → 1.224737 |
| C1 | PASS | finest ratio 1.0000 (both γ_L), bound held, 0 violations |
| C2 | PASS | finest ratio 1.0000, bound held, 0 violations |
| D1 | PASS | (a) 8e-14, (b)–(d) 0, (e) 7.4e-5 |
| D2 | PASS | min total +0.0055 M☉/pc³, margin ≥ 1.77e4 |
| D3 | PASS | 60/60; spherical +1.6e-7 |
| D4 | PASS | central +0.006 / +0.005 %; band ≤ 0.042 %; σ ≤ 3.5e-5; 0/9000 unconverged |
| E0 | PASS | 0 deviation |

MUTATE (`X3_MUTATE=1`, Θ ≡ 1, the switch removed): 6/12, exit 1.
- **B1-S FAIL:** UV coefficient Kγ_Lρ₀/(K + γ_Lμ_K²) ≠ 0.
- **B2-S FAIL:** the "switch" c² < 0 for s < 0.
- **B3-S FAIL.**
- **C1 and C2 FAIL:** the ratio is 2.0009–2.0018 per doubling, which is H4's divergence.
- **D1 FAIL:** (c) gives 0.71.
- D4 production is not rerun in the mutated mode, as frozen.

## 6. Execution history and amendments

No amendments: no pass line, verdict rule or declared input was changed, PRE- or POST-RESULT. Disclosed:
- **Development runs (not kept), after the criteria commit.**
  - Smoke tests: switched-solver timing and convergence, the isolated lemma, one slab level.
  - Two full runs of a scratch copy of the main script.
    - The first peaked at **1.18 GB in one process, over budget** (disclosed). The script was therefore restructured:
      every slab level and every solver part now runs in its own spawned process.
    - The second showed the slab child at 0.93 GiB, which led to one process per slab level (worst 0.40 GB).
  - A dev look at the C3b eigenvector: a grid-scale mode on the two faces next to the stiff interface node.
  - A preliminary aggregation of the production tables before the main run. It gave the same numbers.
- **Production.**
  - Each bracket run stopped at its 27-min guard and resumed by skipping finished blocks: E_mid 3 runs, E_lo 2, E_hi 2.
  - Block sums per run: E_mid 1818 / 1664 / 554 s; E_lo 1806 / 587 s; E_hi 1741 / 525 s. Two runs exceeded 30 min by
    ≤ 20 s, because the guard is checked between blocks.
  - Up to three single-thread runs ran in parallel, each ≤ 0.52e9 bytes RSS.
  - E_mid's first run started from a chained loop. I stopped the loop (not the run) to run the brackets in parallel.
  - The first E_mid run used the file before the main-script refactor. The production code path (`production`,
    `sigma_chain`, `SW`, `s_gal`, the D10 machinery) is identical in both versions; the first 379 lines were verified
    identical at the swap.
- **Final runs.** Main and MUTATE ran on the final script file.

## 7. What this does not show

- **No nonlinear evolution and no 2D/3D time evolution.**
  - The well-posedness evidence is the exact dispersion on each side, the nonlinear principal symbol (frozen
    coefficients), a 1D slab without WKB, and a crude 3D Rayleigh bound (derived, not computed).
  - Non-axisymmetric, moving and rotating backgrounds are not tested.
  - A moving interface (D·P changing sign in time) is covered only by the c² ≥ 0 argument. The degenerate-hyperbolic
    free boundary has no local well-posedness proof here.
- **The linearisation at D·P = 0 is one-sided** (the Lagrangian is C¹ only). The continuum argument and C1 use the value
  that keeps c² = γ_L s₊. C3b shows that any O(h) or O(ε) mismatch reintroduces UV growth.
- **Negative dust is not covered.** If any v3 regime puts negative dust inside a stiff region (S4's hydrostatic dust at
  μ_K ≥ 0.1 Mpc⁻¹), the switch does not help there.
- **Strong coupling is not resolved.** The soft side has c_π = 0. Whether the pair's EFT is valid in saddles is open (E1).
- **Statics are checked only where the record relies on screening:** C6's linear Solar-System setting, D10's
  uniform-field cluster model and P3's spherical rows.
  - P3's BH member radial profiles are not re-derived; only its E4 points and the spherical positivity check.
  - The MW disc used for the Galactic phantom is ILLUSTRATIVE (H4's).
- **Not re-scored under the switch:** galaxy tiles, clusters, lensing and growth. Where they use static solutions with
  D·P < 0 regions at r ≫ L★ (saddles, external-field lobes), the change is expected to be O((L★/r)²) by the same argument,
  but this is not computed here.
- **No data comparison is new here.** D10's statistic is reused unchanged. Nothing here says the data favour the
  framework, and the theory is not closed.

## Input ledger (full: `ASSUMPTION_LEDGER.md`)

| input | class | source |
|---|---|---|
| v3 action, the switch (zero new constants) | FRAMEWORK-NATIVE / lane hypothesis | THEORY_V3_DRAFT §1, C4, C5, C8; X0 MAP §1.C1 |
| H4 PN system, dispersion, B2 model, region depths and e-folds | FRAMEWORK-NATIVE record (H4 code executed read-only) | H4 |
| D10 solver, statistic, likelihood tables; C6 kernel | METHOD / FRAMEWORK-NATIVE record (imported read-only) | D10, C6 |
| globular σ, N, radii | RAW (Baumgardt via D10/CFG332) | D10 |
| L_V, r_h, R_GC, Υ priors, binaries, MW M_b bracket | SURVEY-CALIBRATION | D10, CFG332, CFG334, A60, D7b |
| a₀ footings, κ = ½, L★ grid | FITTED | doors BRIEF, D10 |
| x_e = 1.15–2.6 at the Sun | FRAMEWORK-NATIVE / SURVEY-CALIBRATION | C5 / D7d |
| MW-like disc (5e10 + 1e10 M☉) for the Galactic phantom | ILLUSTRATIVE on H4's solver | H4 S5a |
| P3 E4 rows, A69 estimate; C5 β dispersion/window | FRAMEWORK-NATIVE record / ADOPTED method (estimate) | P3, C5 |

No LCDM-processed input, no standard-MOND machinery (QUMOND not used; D10's E4 bridge not used), no literature input in
any check. No downloads.

## Files

- `x3_switched_stiffness.py`: the lane script.
  - The main run writes `x3_switched_stiffness.out` and `x3_switched_stiffness_results.json`.
  - `X3_MUTATE=1` writes `x3_switched_stiffness_MUTATE.out` and `x3_switched_stiffness_results_MUTATE.json`.
  - `--d10 E_mid|E_lo|E_hi` writes `x3_d10_tables_<bracket>.json` and `x3_d10_<bracket>.out` (D4 production).
- **Run** (each ≤ 30 min, < 1 GB per process, one thread):
  `OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X3_switched_stiffness/x3_switched_stiffness.py [--d10 B]`.
  - It is deterministic: it re-executes itself with PYTHONHASHSEED = 0.
  - Every slab level and every solver part runs in its own spawned process.

**Qualifier 4 resolved (fix-forward, 2026-10-23).** RESOLVED BENIGN (review `reviews/v3s_soft_side_strong_coupling_2026_10_23/`, d27e01f42e, 5/5): the soft-side khronon is a dispersionless fluid, ω² = Kρ_τ(M − 1); 'Λ = 0' came from putting c_π = 0 (the k → ∞ limit) into the relativistic scaling. With c_π(k) = ω/k, the strong-coupling length across all 320 H4 region values is 57 m–54 km, so the soft-side EFT holds on astrophysical scales. Open: classical nonlinearity of real khronon flows, ε_cl = k|v|/ω, possibly O(1) in Mpc bulk flows.
