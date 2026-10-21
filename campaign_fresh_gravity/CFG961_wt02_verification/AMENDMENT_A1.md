# CFG961 AMENDMENT A1 (2026-10-21; POST HOC with respect to development runs, PRE graded run)

Committed alone, after scratch development runs of the §2 machinery and before any graded run of `cfg961.py` in this folder.
The frozen rules (83b04219e) are kept and applied as written; their result is reported alongside. A1 adds one computation and one
reading. It is post hoc: it was written after I saw what the frozen gravity model does to the fast modes.

## A1.1 What the development runs showed

- **Gravity off.** The roots are σ = ±c²k²/(3H) (ratio to c²k²/3H equal to 1 to 1e-6 at c/k = 100 Mpc and to 1e-9 below 1 kpc)
  plus slow roots of order H. This is the frozen secondary model.
- **Gravity on, quasi-static (the frozen primary).** The fast roots shift by 0.9% at kL* ≲ 1. At c/k = 24 pc with L* = 1 kpc
  (kL* = 42) the fast root drops to 0.25 c²k²/3H. The σ⁴ coefficient does not vanish at H → 0 with χ̄̇ = X held fixed.
- **Why: the frozen model is not valid for these modes.**
  - The fast modes evolve at σ ≈ c²k²/(3H). For any sub-horizon k this is faster than ck, so the metric's time derivatives
    (HΦ̇/c² ~ k²Φ) are leading order.
  - The quasi-static model (one potential Φ = Ψ with only −|∇Φ|²/2K) sends the λ-sector's pressure-type source (λ·3Φ̇χ̄̇/c⁴, from
    the slices' extrinsic curvature) into an elliptic Poisson equation. In GR that source feeds the trace-ij equation, Φ̈ + … = 4πGδp,
    and is suppressed by (H/ck)².
  - So the frozen primary model mis-models exactly the modes the question is about.

## A1.2 Added computation (post hoc, carries the substantive class for (a))

**Full-GR scalar sector on flat FRW, from CFG938's action as written.**
- **Metric.** ds² = −c²(1 + 2Ψ)dt² + 2c a ∂_xB dt dx + a²[(1 − 2Φ)δ_ij + 2∂_i∂_jE]dx^i dx^j.
- **Gravity.** EH from √−g R expanded to O(ε²).
- **Matter.** The medium (labels, W, ττ, λ); baryons as a second dust with no λ coupling; Λ.
- **Background.** Tadpoles are checked to vanish with Friedmann (H² = (2K/3)ρ_tot, Ḣ = −Kρ_m) and S1d.
- **Equations.** Euler–Lagrange for all 8 fields (δχ, δλ, ξ_c, ξ_b, Ψ, B, Φ, E). Newtonian gauge B = E = 0 is set after
  variation, giving an 8 × 6 frozen-coefficient system.
- **Roots.** From the 6 × 6 subset that drops the Φ and E rows. Each root is accepted only if the FULL 8 × 6 matrix (rows and
  columns equilibrated) is rank-deficient there: s_min/s_max ≤ 1e-6 at the root, and ≥ 1e-2 at σ(1 ± 1e-3).
- **Grid.** The same scan as frozen §2 (z = 0, 10; H ±; L* = 24 pc and 1 kpc; c/k from 100 Mpc to 24 pc), with the same Hadamard
  thresholds.
- **P2 under A1.** Eigenvector normalised to Kδλ = 1. Report the Bardeen potentials Φ and Ψ (Newtonian gauge), also scaled by
  (ck/H)², and δ_c. Report the residual of the dropped rows. Report which equations can be dropped without losing the fast root;
  this tests the Bianchi identity that ties the λ equation to the trace-ij Einstein equation when χ̄̇ ≠ 0.

## A1.3 Reading (post hoc)

**Class for (a).**
- The frozen-rule class is computed and printed as written (quasi-static primary, K-a1 as worded).
- The substantive class uses the A1.2 full-GR system as "gravity on", the gravity-off system as the secondary, and the frozen
  thresholds otherwise.
- K-a1 is applied to the gravity-off system. In full GR the H → 0 limit at fixed ρ̄ does not exist (Friedmann), and K-a1's
  static target is CFG938's flat, static, gravity-free WKB.

**MUTATE.**
- MU1 and MU2 are also run on the full-GR system.
- MU1 is run with the background clock sign that its own S1d implies (χ̄̇ = +Kρ̄c²/3H), so its tadpoles vanish.
- MU2 keeps χ̄̇ at the as-written value, because χ̄ is then unconstrained.
- MU5 stays gravity-off, as frozen.

No other rule changes. The quasi-static runs stay in the outputs.
