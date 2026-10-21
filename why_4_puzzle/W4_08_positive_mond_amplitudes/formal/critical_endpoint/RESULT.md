# W4-08 critical endpoint: the α_eff = 2 same-state sourced response

2026-10-21. Claude continuation of `CLAUDE_HANDOFF.md`, on the owner's instruction (base origin 215b7dc10).
Criteria: `FROZEN_CRITERIA.md`, committed alone in 582bbb7ad before any script.
**The original target is NOT reached.** No principle forces R_amp = 128π/9 (ξ = ¼). **κ = ½ remains FITTED** (CFG493
κ_Λ 0.417 ± 0.095, κ_crit 0.345 ± 0.078; footings not pooled). Not theory closed.

## Verdicts

| question | frozen verdict | what the calculation shows |
|---|---|---|
| Endpoint response | **UNDETERMINED** | See the four points below. |
| Target R_amp = 128π/9 | **NOT SELECTED** | If the window is accepted, R_amp = (4/3)(H/a_M)² = (4/27)(\|c1\|/\|c2\|)(\|I0\|/x_a). Two tunings are needed, and no declared principle fixes the free ratio. |
| Health | per M6 | Classical static, spherical, leading order: the solution exists and is unique at each radius. Linear de Sitter c_s² = 0 at α = 2 means the theory is strongly coupled around the vacuum. Nothing more is claimed. |

What the calculation shows for the endpoint response:
- **Regular F at α = 2:** no MOND. The law is quartic, μ ∝ g².
- **MOND cusp moved to I0:** at leading order there is a deep-MOND regime between the quartic floor h_c = 18(|c2|/|c1|)H²/a_M
  and a_M.
- **Two new obstructions:**
  - the khronon's convective term runs away beyond r_w ≈ 0.82 (GM a_M)^{1/4}/H;
  - the khronon back-reaction is O((|c1|/|c2|)Φ_N) near sources.
- **On the frozen grid the full system does not converge.** A post-hoc run inside r_w does converge, but its MOND band is
  narrow: 0.87 decades, below the frozen one-decade bar.

## 1. Object and assumptions

The action (SINGLE_FUNCTION §1):

    S = (B/2)∫√−g [R + m²F(I)] + S_m[g],   I = (c2K² − c1 a_μa^μ)/m².

- The clock is hypersurface-orthogonal and timelike; c3 = −c1, c4 = 0; matter couples universally to the metric.
- De Sitter state: I0 = 9c2H²/m² < 0 (c2 < 0), with α_eff = −c1F'(I0) = 2. The source side is x = I − I0 ≥ 0.
- The regime is static, spherical, weak-field and sub-horizon (r ≪ 1/H), in physical (static-patch) coordinates.
- The khronon is stationary, T = t + τ(r), so its normal is a radial potential flow v = u^r. The flat slicing has v = Hr.
- Kept: the clock flow and its convective acceleration, the lapse and the conformal factor, the gradients, and the
  boundary conditions (v(0) = 0 for an extended source; Π → Π0 at the outer edge).
- Dropped:
  - O(Φ, v², H²r²) corrections to the kinematics;
  - the √−g weighting of the perturbation (m²ΔF·Φ ~ h²Φ);
  - time dependence (static source).

## 2. Raw derivation (`derive.py`, 8/8 checks)

**M1, exact kinematics.** For ds² = −A dt² + B_r dr² + r²dΩ² with u = (u^t, v, 0, 0):

    K = v' + v(A'/2A + B_r'/2B_r) + 2v/r,
    a_r = [(B_r v² + 1)A' + (2B_r v' + v B_r')A v]/(2A).

- Exact checks: a·u = 0; on the de Sitter flat slicing K = 3H and a = 0; on Painlevé–Gullstrand Schwarzschild a = 0 (K1).
- Weak field: K = (r²v)'/r² and **a_r = Φ' + v v'**. The second term is the convective acceleration of the clock flow, which
  the earlier flat-static branch set to zero.

**M2, field equations** (sympy Euler–Lagrange on L = r²[2Ψ'² − 4Φ'Ψ' + m²F(I)] − (2/B)ρr²Φ):

    Ψ:        (r²(Ψ' − Φ'))' = 0   →   Ψ = Φ
    Φ:        (r²[4Ψ' − 2α_I a])' = (2/B)ρr²   →   (2 − α_I)Φ' − α_I v v' = 2GM/r²        (α_I ≡ −c1F'(I))
    khronon:  r²(c2F'(I)K)' + v(r²α_I a)' = 0

- **K2, ADM cross-check.** Integrated with v = Hr, the khronon equation gives c2[F'K − F'(I0)K0] = −2H(φ + rφ'). This is
  identical to the unitary-gauge momentum constraint of SINGLE_FUNCTION §5 at linear order: (1 − λ)δK = 2U with
  U = ζ̇ − Hn = −H(φ + rφ').
- **K4.** For H, v → 0 the system returns μ = 1 + c1F'/2.

**M3, endpoint system at leading order** (back-reaction U → 0):

    α_I(I)·K = 2K0,   (2 − α_I) g = 2GM/r²  (+ α_I w_c),   x = [c2(K² − K0²) − c1a²]/m².

The khronon is therefore not passive. It tilts so that α_I K stays at its cosmological value.
- **E-reg (F ∈ C² at I0):** μ_eff = z/(1+z), with z ∝ g² at small g. Quartic (g ∝ M^{1/3}r^{−2/3}); dμ/dg = 0 at g = 0. No
  MOND.
- **E-cusp (F'(I0 + x) = (2/|c1|)[1 − p(√(x/x_a))], p(y) = y + O(y²)):**

      μ_eff = [√(η² + g²) − η]/a_M,   η = |c2|K0²/(|c1|a_M) = 9(|c2|/|c1|)H²/a_M,

  - deep MOND (μ = g/a_M) for η ≪ g ≪ a_M;
  - quartic, μ = g²/(2ηa_M), for g ≪ η;
  - Newton above a_M.
  - The exact solution for the declared p = y/(1+y) is in `derive.out`.
  - **This is the first same-state derivation of the cusp's deep regime on the actual positive vacuum.** It is also the
    reason the regular-branch formula G_bg = G/(1 − α/2) cannot be extended to α = 2.

**M5, the singular δK direction is a constrained direction.**
- The constraint F'(I)K = const has d(F'K)/dK = F' + 2(c2K²/m²)F'' = Q. With the cusp at I0, F'' → −∞ and I0 < 0, so
  Q → +∞ and λ_eff → +∞.
- The map K ↦ F'(I)K is strictly monotone, so the momentum constraint fixes δK uniquely; at linear order δK = −2U/(λ − 1) → 0.
- The reduced scalar coefficient C = 2S/(λ − 1) → 6, which is finite. So the |δK|^{3/2} non-analyticity flagged in the
  handoff does not reach the quadratic scalar action.
- At α = 2: K_z = 6X/(3H² + X) > 0 and V_z = 12H²X²/(3H² + X)² > 0, but the principal c_s² = 0, with sub-horizon Ω² → 2H².
  The scalar has no quadratic gradient energy around the vacuum: **it is strongly coupled at h → 0**. This is the same
  degeneracy as deep-MOND AQUAL in empty space, and it is not resolved here.
- **k = 0:** added matter raises H², which moves I to the side opposite the static sources (I < I0). The homogeneous
  matter response therefore uses the regular opposite branch, G_cos = 2G_bare/S_left.

## 3. Numerical verification (`solve.py`, Plummer source, declared parameters)

Units c = H = 1; c1 = −1, c2 = −1e−5, m = 0.15, a_M = 0.2, GM = 1e−13, b = 1e−8; grid r ∈ [1e−9, 1e−2].
- Phase 1 is the M3 system with the convective term v v' kept.
- Phase 2 adds the back-reaction J with under-relaxation.

| run | phase 1 | local slope −1 ± 0.05 |
|---|---|---|
| E-cusp | Newton at r < 3e−7; MOND band r ∈ [6e−6, 3.5e−5]; closed form matched to 2e−13 (**K6 PASS**) | 0.77 decades |
| E-reg | slope −0.68 at 1e−5 to 1e−4 (quartic) | 0.08 decades |
| control α0 = 1 | far field g = 2GM/r² to 1e−4 (**K3 PASS**: G_bg = G/(1 − α/2)) | 0 |

**Obstruction 1: convective runaway (new).**
- At the endpoint, the Φ equation (2 − α)g = S + αw_c amplifies the clock's convective acceleration by 1/μ.
- In the MOND regime δK ∝ 1/r, so the flow offset w = r⁻²∫δK s² tends to a constant, (3/2)H√(GM/a_M), and w_c ≈ Hw.
- This term outgrows the source beyond **r_w ≈ 0.82 (GM a_M)^{1/4}/H ≈ 0.82 v_f/H**: 3e−4 in grid units, about 2 Mpc for
  v_f = 200 km/s.
- Beyond r_w the static field **grows** (slope +1 at r > 1e−3). The isolated-source solution does not relax to the
  de Sitter state. E-reg shows the same runaway; the α0 = 1 control does not, because it has no 1/μ amplification.
- For real galaxies r_w lies outside the rotation-curve data, but at the scale of galaxy–galaxy lensing (KiDS reaches
  about 3 Mpc). There the static model predicts non-MOND behaviour unless cosmological embedding changes it.

**Obstruction 2: khronon back-reaction (new).**
- The term phase 1 drops is β = (−c1/c2)J/(α0K0), amplified by |c1|/|c2|.
- On the frozen grid β ≈ −13 everywhere, driven by the far-field runaway. Phase 2 diverges, so the frozen verdict is
  **UNDETERMINED**.
- **Post-hoc diagnostic** (no verdict weight), on a grid truncated at r ≤ 1e−4 < r_w:
  - the core term is β ≈ −1.6 (|c1|/|c2|)Φ_N;
  - the full system with back-reaction **converges**, and the MOND band is 0.87 decades.
- The MOND window needs |c1|/|c2| ≳ 18(H/a_M)²(a_M/h_min), i.e. 10⁴ to 10⁵ for one or two decades. So β is about 0.1–1 at
  galactic Φ ~ 1e−6, and about 10–100 near white dwarfs (Φ ~ 1e−4).
- **The leading-order relation α_I K = 2K0 fails near compact sources.** Their strong-field khronon structure is
  uncontrolled.

**Slope evidence is weak at these parameters.** The regular α0 = 1.9 crossover (MU1) also shows a 0.65-decade band at slope
−1. The frozen verdict asks for g ∝ √M/r. The √M (two-mass) test was not run.

**Checks:** K1, K2, K4, M2 and M3 (symbolic) pass; K3, K6 and I1 pass.
- **K5 FAILS as frozen:** I normalised the Φ-equation residual by S alone, and S is tiny in the far field. Relative to the
  largest term the residual is 1.5e−11 (post-hoc line in `solve.out`).
- **MUTATE MU1–MU4 all bite** (exit 1 by design).

**First runs kept** (numerical-method failures, physics unchanged): `solve_firstrun_overflow.out`,
`solve_secondrun_divergent.out`, `solve_thirdrun_control_runaway.out`, `solve_fourthrun_cancellation.out`. The last was
catastrophic cancellation in v v' − H²r. The final solver uses perturbation variables (w, δK, α0 − α analytic) and a
two-phase under-relaxed iteration.

## 4. Amplitudes, tunings and principles (M7)

If the leading-order window is accepted:

    C2 = B (Newton; α_I → 0),   C3 = 2B/(3a_M),   ε = 3BH² (the actual de Sitter stress),
    R_amp = εC3²/C2³ = (4/3)(H/a_M)² = (4/27)(|c1|/|c2|)(|I0|/x_a).

- **Tunings:**
  - T1, criticality: F'(I0) = −2/c1.
  - T2, vacuum at the cusp: F(I0) = −2I0/(3c2) − 4I0/c1.
- **P1, kink self-tuning.** A jump in F' at I0 can pin the Friedmann root there for an open range of F(I0), which removes
  T2. The cost: H ignores added matter up to a threshold density, a plateau. It does not touch T1 or R_amp.
- **P2, scale and conformal invariance of the deep equation.** This holds for every a_M: it fixes the exponent only.
- **P3, the opposite-branch deformation of SINGLE_FUNCTION §7.** Supported on I < I0 and flat at I0, it leaves F(I0),
  F'(I0), the cusp, the vacuum and the MOND law unchanged. It alters only the homogeneous matter response G_cos. It is
  **not excluded**, and it is irrelevant to R_amp.
- **The constant shift of F** (the zero mode) is fixed by T2 inside the endpoint family.
- **Free ratio.** R_amp = 128π/9 needs H/a_M = √(32π/3) = 5.7888, i.e. (|c1|/|c2|)(|I0|/x_a) = 96π. An F with algebraic
  shape constants cannot produce this π. That is the π-parity wall again, now in microscopic variables.

## 5. Precise remaining gap

1. **The far field beyond r_w.** Decide whether cosmological embedding (time dependence, neighbouring masses) removes the
   convective runaway, or whether the endpoint predicts non-MOND lensing at about 1–3 Mpc around isolated galaxies.
2. **Strong-field clock structure.** Near compact objects the back-reaction exceeds 1; the infalling-clock branch and its
   PPN/preferred-frame consequences are needed.
3. **A one-decade MOND window.**
   - It needs a cusp shape p(y) that reaches linearity faster than y/(1+y), together with |c1|/|c2| ≳ 10⁵ against
     obstruction 2.
   - The two-mass √M test should be run with the same parameters.
4. **Health.** The c_s² = 0 strong coupling around the vacuum, time-dependent nonlinear stability, the cutoff and the
   quantum state are all untouched.
5. **Amplitude.** No microscopic relation between the cusp location/width (|I0|/x_a) and the coupling hierarchy
   (|c1|/|c2|) has been found. Without one the target is not selected.

No Lean module was added: none of these results is a clean load-bearing identity that would merit one. The inherited nine
modules keep their scopes.

## Files

- `FROZEN_CRITERIA.md`
- `derive.py` and `derive.out`, with `derive_results.json`
- `solve.py` and `solve.out`, with `solve_results.json`
- `solve_MUTATE.out` and `solve_results_MUTATE.json`
- the four kept first-run outputs listed in §3

Run from the repo root:

```
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/critical_endpoint/derive.py
OMP_NUM_THREADS=1 python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/critical_endpoint/solve.py
W4_08_CE_MUTATE=1 OMP_NUM_THREADS=1 python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/critical_endpoint/solve.py
```
