# X3_switched_stiffness: does the switched stiffness −(γ_L/2)[max(D·P, 0)]² make v3 well-posed where ρ_τ < 0, with its screened statics unchanged? FROZEN CRITERIA

Written and committed (with `ASSUMPTION_LEDGER.md`) before the lane script exists and before any script has produced a
number. Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md` + `BRIEF_E_AUDIT.md`. Lane launched by
`rebuild_2026_10_22/X0_explanation_map/MAP.md` §1.C1 (C2, C3 secondary). κ = ½ is FITTED. Footings canonical
a₀ = 9.3603e-11 m/s² and alt a₀ = 1.1312e-10 m/s² (record values; 9.36e-11 / 1.13e-10 where a reused lane used those),
never pooled. No dark-matter particle. Never "theory closed"; nothing here says the data favour the framework.

## 0. What was read before freezing, and the not-blind statement

Read: X0 MAP §1.C; H4 (README, FROZEN_CRITERIA + A1, ASSUMPTION_LEDGER, script Parts A–D, results json B1/B2/efolds);
P3 (README, E4 rows and `scales()` in the script, json E4); V1 (README §(e)); M1 README (grep: saddles); C5, C6, C8
READMEs and C6 FROZEN_CRITERIA; D10 (README, FROZEN_CRITERIA, `d10_solver.py`, `d10_native_lstar.py`, its `.out` header
and the json's cluster inputs, verdict block and e_c values).

**Not blind.** Before this file I did hand work only (nothing run, no lane number produced):
- **Dispersion on each side.** With the switch, the linearised P equation has stiffness γ_L Θ(D·P₀). Where D·P₀ > 0 it is
  H4's operator, ω² = ρ_τ[k²/χ − K]; where D·P₀ < 0 it is H4's γ_L = 0 operator, with the finite UV limit Kρ_τ(M_θ − 1).
- **1D Rayleigh bound (hand proof).** Γ² = sup_q [−⟨q, ρ q⟩ / ⟨q, 𝓛⁻¹ q⟩], with 𝓛 = K(M−1) + KΠ₀ − ∂γ(z)∂. The test field
  r = q·1_N (N = {γ = 0}) gives Γ² ≤ K(M − 1 + |N|)·max_N |ρ_τ|, uniformly in resolution, provided the stiffness is off on
  every point where ρ_τ < 0. Localised modes should approach K(M−1)·max_N |ρ_τ|.
- **Nonlinear principal part (hand).** The PN system is a barotropic Euler fluid of density ρ_τ = D·P + ρ_d with enthalpy
  h = γ_L (D·P)₊. So c² = γ_L (D·P + ρ_d) Θ(D·P), which is ≥ 0 for every state when ρ_d ≥ 0. For any smooth convex
  replacement F of s₊², c² ∝ s F″(s) < 0 wherever s < 0 and F″ > 0. So any smoothing of the switch reintroduces the
  Hadamard instability.
- **Discretisation hazard (hand).** If a discrete scheme puts stiffness on a node next to a face where ρ_τ < 0, the discrete
  c² is negative over a layer of width ≲ h/2, where |ρ| ≲ ρ′h/2. I expect a grid-scale rate Γ ~ (ρ′γ_L/h)^½ in that case,
  i.e. ×√2 per doubling.
- **Statics lemma (hand, convex analysis).** If the unswitched minimiser has D·P ≥ 0 a.e., it is the unique minimiser of
  the switched leaf functional (switched ≤ unswitched pointwise, equality there; directional derivatives ≥ 0 along negative
  divergence sheets). If D·P < 0 on a set of positive measure, the solutions differ.
- **Order-of-magnitude expectations (hand, not used as thresholds).**
  - The Sun's own response has negative lobes ~ M☉/(4πL★³) ≈ 1e-5 M☉/pc³. The Galactic phantom at the Sun is +0.045
    (H4 C3), so I expect positive D·P with a large margin.
  - Pal 4's and Pal 14's external-field lobes (r ≳ r_M/x_e ~ 70 pc) should be ~1e-3 M☉/pc³ deep, against a Galactic
    phantom ~5e-5 M☉/pc³ at R_GC ≈ 100 kpc. So D10 is expected to change by an amount I have not estimated.
  - The Lifshitz β term (secondary) should give bounded rates.

## 1. The theory tested and the questions

v3 (THEORY_V3_DRAFT §1; C5's Lagrangian at β = η = γ_F = 0, ξ = 1) with **one change, zero new constants**:

    L/√−g = R/(4K) + P^μA_μ − W(K|P|) − (γ_L/2)[max(D·P, 0)]² + μ_K²(Q−1)²/(2K),   K = 4πG, γ_L = K L★²/2.

The switch is exactly max(D·P, 0). No smoothing, no threshold, no tuning. If a result needs smoothing, its scale is a new
constant: it is reported as such and **not adopted**. At D·P = 0 exactly the second derivative of max(s,0)² is one-sided
(0 from below, γ_L from above). On a measure-zero set this is no constant. Its only role is in discrete co-location; see C1
and C3.

- **Q1 (dispersion).** Each side of D·P = 0, and the interface. What holds across the D·P = 0 surface? Is the leaf
  functional (C8) still convex, and is the leaf problem still uniquely solvable?
- **Q2 (well-posedness, numeric).** A slab like H4 B1/B2 with a sign-changing D·P: does the growth rate converge under
  resolution doubling?
- **Q3 (statics).** Is D·P ≥ 0, with a stated margin, wherever C6 (Sun, planets, Cassini), D10 (outer globulars) and P3
  (strong field) rely on screening? Where it is not, by how much does the screened result change?
- **Q4 (secondary, report only, no verdict weight).** P3's strong-coupling estimate where c_π → 0 (the interface) and on
  the D·P < 0 side; the Lifshitz regulator β(∇·n)² inside C5's window as an alternative cure (β is a new constant there).

## 2. Checks (script prints `ID PASS/FAIL value threshold`; exit 0 iff all PASS)

### Part A: reproduction of H4, read-only
- **A0a.** H4's own A4 sympy block (its source lines executed verbatim from `h4_v3_saddle_stability.py`, nothing edited)
  gives ω² = ρ_τ[k²/χ − K]. The B1 limits computed on it equal H4's json strings: UV coefficient γ_L K ρ₀/(K + γ_L μ_K²);
  γ_L = 0 limit finite. Residuals vs json are identically 0.
- **A0b.** H4's own `gmax` (extracted from H4's source by `ast`, executed unchanged) reproduces H4's json B2 ladder to
  ≤ 1e-12 relative. Γ(512)/Γ(256) ∈ [1.8, 2.2] at γ_L = 1e-3, and the γ_L = 0 ladder lies within 1 % of 1.224745.

### Part B: the switched operator (sympy, exact; residuals identically 0)
- **B1-S (dispersion, each side).** The switched linear system (H4's A4 system with the P-equation stiffness multiplied by
  Θ) gives the following.
  - D·P₀ > 0: exactly H4's ω².
  - D·P₀ < 0: ω² = ρ_τ[k²/χ₀ − K], with χ₀ = k²/(K M_θ) + μ_K²/K.
  - Scored: (i) the D·P₀ > 0 side minus H4's ω² = 0. (ii) On the D·P₀ < 0 side, lim ω²/k² = 0 and
    lim_{k→∞} ω² = Kρ_τ(M_θ − 1) (finite). (iii) At μ_K = 0, the D·P₀ > 0 side has ω² = Kρ_τ(M_θ − 1 + L★²k²/2) ≥ 0
    for ρ_τ ≥ 0.
- **B2-S (nonlinear principal part).** 1D PN Lagrangian with −(γ_L/2)F(∂_zP) for a generic F, μ_K → 0, constant dust
  offset ρ_d. Three sympy steps:
  - (i) The P Euler–Lagrange equation plus the Bernoulli definition give D_t v = −∂_z[(γ_L/2)F′(s)] + (order-0 terms)
    with s = ∂_zP. The σ Euler–Lagrange equation is continuity for s.
  - (ii) The frozen-coefficient principal symbol of (continuity of ρ_τ = s + ρ_d, Euler) is ω² = c²k² with
    c² = (s₀ + ρ_d)(γ_L/2)F″(s₀).
  - (iii) Three cases for F:
    - F = max(s,0)²: c² = γ_L(s₀ + ρ_d)Θ(s₀) ≥ 0 on both branches for ρ_d ≥ 0.
    - F = s² (v3): c² < 0 for s₀ < −ρ_d.
    - Smoothed max, F_ε = [(s + √(s² + ε²))/2]²: c² < 0 at s₀ = −ε, ρ_d = 0, for every ε > 0.
  - PASS iff all three hold: the switch gives c² ≥ 0 everywhere, and v3 and every ε-smoothing give c² < 0 somewhere.
- **B3-S (interface and leaf problem, sympy + stated derivation).**
  - (i) max(s,0)² is C¹ and convex: second derivative 0 / 2 on the two branches, and the first derivative is continuous
    at 0.
  - (ii) Switched energy ≤ unswitched energy, with equality iff s ≥ 0.
  - (iii) The switched static Euler–Lagrange equation ∇Φ + (L★²/2)∇(∇·p)₊ = h(p) reduces, as in C6/D10, to
    p = ∇χ/(1 + |∇χ|) with χ = Φ + (L★²/2)(∇·p)₊.
  - The interface conditions (Φ, ∇Φ, the tangential and normal parts of P; s₊ = 0 and ∂_n s₊ = 0 from the stiff side) and
    the uniqueness/existence argument for the leaf functional are written in the README. They are a derivation, not a
    scored number.

### Part C: slab (numeric; no WKB; 1D periodic, unit length)

**Model (H4 B2's).** K = 1, M = 2, s₀(z) = ρ̄ + Δcos(2πz) with ρ̄ = −0.5 and Δ = 1. ρ_τ = s₀ + ρ_d.

**Discretisation (own, staggered finite volume).**
- Nodes z_i = i/N carry s and the stiffness γ_i = γ_L·Θ(s₀(z_i)), with Θ(0) := 0. Faces z_{i+½} carry δP, q = ∂_zδσ and
  ρ_τ(z_{i+½}).
- 𝓛 = K(M−1)I + K·Π₀ + Dᵀdiag(γ)D, where (Dr)_i = (r_{i+½} − r_{i−½})/h and Π₀ = (1/N)𝟙𝟙ᵀ (periodic Poisson removes the
  mean).
- Γ² = largest eigenvalue of the generalised problem (−ρ_τ) q = Γ² 𝓛⁻¹ q, restricted to zero-mean q.
- **Sign-consistency (discrete c² ≥ 0)** means every node with γ_i > 0 has ρ_τ ≥ 0 on both of its faces. It is checked and
  printed per level.

**Checks.**
- **C0 (validation against H4).** Unswitched (Θ ≡ 1), γ_L = 1e-3, N = 64, 128, 256, 512: Γ(512)/Γ(256) ∈ [1.8, 2.2].
  At γ_L = 0: Γ(512)/Γ(256) ≤ 1.01 and |Γ(512)/1.224745 − 1| ≤ 0.01.
- **C1 (verdict; zero dust, aligned grid).** N = 96, 192, 384, 768, 1536. The zeros of s₀ at z = 1/6 and 5/6 fall exactly on
  nodes, located by integer arithmetic: node i is stiff iff min(i, N−i) < N/6. Run at γ_L = 1e-3 (H4's) and 1e-2. PASS iff,
  for both γ_L:
  - (a) |Γ(1536)/Γ(768) − 1| ≤ 0.10 (four doublings);
  - (b) at every level Γ ≤ √(K(M − 1 + f₋)·max_{faces ρ<0}|ρ_τ|)·(1 + 1e-9), with f₋ the fraction of faces with ρ_τ < 0
    (the rigorous discrete bound);
  - (c) every level is sign-consistent.
  - Reported: Γ(1536) against the localised-mode value √(K(M−1)·1.5) = 1.224745.
- **C2 (verdict; positive dust buffer, H4's unaligned grid).** ρ_d = 0.1 (ILLUSTRATIVE), switch on s₀, N = 64, 128, 256,
  512, 1024, γ_L ∈ {1e-3, 1e-2}. PASS iff (a), (b) and (c) as in C1, with the finest pair 1024/512. Reported: Γ(1024)
  against √(K(M−1)·1.4) = 1.183216.
- **C3 (diagnostic; reported, no pass line, no verdict weight).** Not sign-consistent discretisations of the same continuum
  operator:
  - (a) zero dust on H4's unaligned grid N = 64 … 2048;
  - (b) the aligned grid with Θ(0) := 1 at the interface nodes.
  - Both at γ_L ∈ {1e-3, 1e-2}. Reported: Γ per level, the doubling ratios, the local slope d ln Γ/d ln N at the finest
    pair, and the number of sign-inconsistent node–face pairs.
  - Pre-declared reading: growth in C3 with violations present, and none in C1/C2, means the switched theory needs
    sign-consistent numerics (the analogue of positivity preservation). It is not a continuum ill-posedness. The README
    states the fragility plainly.

### Part D: statics

**D1 (validation of the switched D10 solver).** It is D10's `d10_solver.py`, imported read-only. A subclass replaces the
stiffness term λ·D by λ·[(D + s_g)₊ − s_g] and the Jacobian by I − λ diag(Θ(D + s_g)) J (semi-smooth Newton, D10's line
search). PASS iff all of:
- (a) **Lemma, isolated.** D10's K2 cases (y ∈ {0.04, 3}, Λ ∈ {0.5, 2, 8}, isolated, s_g = 0): min D ≥ 0 on the grid, and
  switched σ_p and the radial field at r = a equal the unswitched to ≤ 1e-8 relative.
- (b) s_g = +1e6: the switched solve equals the unswitched EFE solve (Pal 14-like: y 0.04, x_e 0.14, Λ 1) to ≤ 1e-8.
- (c) s_g = −1e6: the switched solve equals the Λ = 0 (AQUAL) solve to ≤ 1e-8.
- (d) Six D10 production cells (unswitched mode of the subclass) reproduce D10's json `sigma_tables` to ≤ 1e-8 relative.
  D10's central L★95 (21.68 / 22.85) is reproduced from D10's stored tables with this lane's copy of D10's statistic, to
  ≤ 1e-6 pc.
- (e) Switched grid convergence at NGC 2419, Pal 4 and Pal 14: canonical, E_mid, Υ 1.6, L★ = 21.7 pc, with s_g. Doubling
  N_r and N_θ and r_out × 10 changes σ_p by ≤ 5e-3 (D10's K6 line).

**D2 (C6 Solar System and Cassini).**
- The total D·P is ρ_gal + ρ_☉(r, θ).
- ρ_☉ is the Sun's response in a uniform Galactic field (D10's solver, Plummer a = 0.1 pc, N_θ = 32, linear regime).
  It covers x_e ∈ {1.15, 2.6} (C5/D7d), L★ ∈ {floor, 24, 90} pc, both footings, and r from 1e-4 pc to 1 kpc.
- ρ_gal,min is the minimum of the Galactic AQUAL phantom over R ∈ [7.2, 9.2] kpc, |z| ≤ 1 kpc. It comes from H4's own S5a
  MW-like disc solver (`run_level`, fine level, isolated, imported read-only), both footings.
- PASS iff min over the region of (ρ_gal,min + min_θ ρ_☉) > 0, and margin ρ_gal,min / max|min(ρ_☉, 0)| ≥ 10, in every cell.
- Reported: H4's C3 near-zone minimum (≤ 0.1 pc, +0.045). Also the size of the far negative regions' effect (MW
  external-field lobes ≥ 40 kpc, from H4's json) as an O((L★/R)²) estimate.

**D3 (P3 strong field).** PASS iff both:
- (i) all 60 P3 E4 rows have G_hat > 0, and `E4_G_nonpositive` is empty (P3 json);
- (ii) isolated spherical screened solutions (D10's `iso_1d` BVP, y ∈ {1e-3, 0.04, 3, 300}, Λ ∈ {0.1, 1, 10}) have
  s = (r²p)′/r² ≥ −1e-6·max s everywhere.
- Where D·P ≥ 0 the switched and unswitched Euler–Lagrange equations coincide pointwise (B3-S), so P3's solutions remain
  solutions.

**D4 (D10 outer globulars, switched).** D10's full production is re-solved with the switched operator. Per footing ×
bracket × cluster × Υ grid (15) × L★ grid (24), AQUAL and Newton columns are unchanged by construction. The switch acts on
the total D·P = D + s_g, where s_g is the spherical AQUAL phantom of D10's own MW model (Hernquist M_b, a_H = 3 kpc, D10's
law) at the cluster's R_GC, per bracket and footing. The statistic, priors, binaries and likelihood tables are D10's
(json, read-only). Reported first: the unswitched D·P maps at the central cells (Υ 1.6, E_mid, L★ floor / 24 / 90 pc): the
min of D + s_g, its (r, θ), and the extent of D + s_g < 0. Variant: s_g = 0 at E_mid for the three primary clusters
(reported). PASS ("unchanged") iff all of:
- (a) central L★95 (P1, E_mid, f_b 0.3, E-P) changes by ≤ 2 % on both footings;
- (b) every band cell (P1–P3 × E_lo/E_mid/E_hi) changes by ≤ max(2 %, 0.2 pc);
- (c) σ_p at Υ = 1.67 (grid point), E_mid, L★ ∈ [20, 90] pc changes by ≤ 1 % for NGC 2419, Pal 4 and Pal 14;
- (d) ≥ 99 % of production solves converge to scaled residual ≤ 1e-8 (else D4 UNDECIDED).
D10's frozen verdict lines (FLOOR HOLDS / window / AQUAL excluded) are re-read under the switch and reported.

### Part E: secondary (reported only; no pass line except E0)
- **E0.** This lane's copy of P3's A69 estimate reproduces P3's json Λ (V1 and V4) for the planets and galaxy rows,
  canonical 24 pc, to ≤ 1e-9 relative (scored, so the reuse is checked).
- **E1.** Strong coupling at saddles (H4 regions, median depth, both footings, L★ floor). P side at ρ_τ = +|ρ| × {1, 1e-3,
  1e-6, 1e-9}: c_π, Λ, k_sc, and ε at k = 1/L★. N side: c_π = 0 (no gradient term), so P3's estimate gives Λ = 0. Stated
  as such.
- **E2.** Lifshitz regulator, v3 + β(∇·n)² with C5's Minkowski coefficient. ω² = (Kρ_τ + β c²k²/(2+3β))(M − 1 + L★²k²/2)
  (C5 × H4, superposed at leading order: ESTIMATE). Γ_max·T for the H4 regions at β ∈ {1e-9, 1e-12, 1e-15, 1e-18}, and the
  β at which the worst median region reaches 1 e-fold. C5's window upper edge β ≲ 1e-9 is an estimate. β is a new constant
  in v3 and is not adopted.

## 3. Verdict rules (frozen)

**Well-posedness.**
- **WELL-POSED** iff B1-S, B2-S, C1 and C2 all PASS (A0, C0 PASS).
- **STILL ILL-POSED** (mechanism named) iff any of these holds, with A0 and C0 PASS:
  - B1-S finds a non-zero UV coefficient on the D·P₀ < 0 side;
  - B2-S finds c² < 0 for the switch with ρ_d ≥ 0;
  - C1 or C2 fails (a) with Γ(finest)/Γ(previous) > 1.10.
- **UNDECIDED** iff A0 or C0 fails, or C1/C2 fail only (b) or (c) (a code or discretisation defect), or C1 and C2 disagree.

**Statics.**
- **UNCHANGED** iff D1, D2, D3 and D4 PASS.
- **CHANGE (where, by how much)** iff D1 passes and any of D2–D4 fails.
- **UNDECIDED** iff D1 fails or D4(d) fails.

**Overall class** (exactly one):
- WELL-POSED + STATICS UNCHANGED;
- WELL-POSED BUT STATICS CHANGE (where);
- STILL ILL-POSED (mechanism);
- UNDECIDED.

**Always printed with the verdict (qualifiers, not verdict lines):**
- the dust condition ρ_d ≥ −D·P wherever D·P > 0;
- the C3 numerics requirement;
- the bounded instability left where ρ_τ < 0. This is H4's γ_L = 0 branch: 0.006–0.20 e-folds median and ≤ 4.2 at the
  deepest cells (H4 json). It is a physical bounded instability, not a well-posedness failure;
- the E1 strong-coupling reading.

## 4. Mutation

`X3_MUTATE=1` sets Θ ≡ 1 in every switched operator (the switch is removed: v3 as written). B1-S(ii), B2-S, C1, C2 and
D1(c) must FAIL. Production (D4) is not rerun in the mutated mode. Outputs: `x3_switched_stiffness_MUTATE.out`,
`x3_switched_stiffness_results_MUTATE.json`.

## 5. Compute

`OMP_NUM_THREADS=1 nice -n 15`, single thread, < 1 GB RSS, each run ≤ 30 min. D4 production runs separately per MW bracket
(`--d10 E_mid|E_lo|E_hi`). It writes `x3_d10_tables_<bracket>.json` incrementally and resumes by skipping finished
(footing, cluster) blocks; the main run aggregates. Before each run, `compute_queue/heavyq.py status` is read; wait if
free memory is low. No downloads. compute_queue/ and other lanes are never touched.
