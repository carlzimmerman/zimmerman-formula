# W4-08 critical endpoint: the α_eff = 2 same-state sourced response (frozen criteria, committed alone)

**Status: FROZEN 2026-10-21, before any script, numerical solution or Lean file for this packet.** Append-only.
Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`. Continuation of `CLAUDE_HANDOFF.md`, which hands this lane to Claude on the owner's
instruction. Base: origin/main 215b7dc10.
**κ = ½ is FITTED** (CFG493: κ_Λ 0.417 ± 0.095, κ_crit 0.345 ± 0.078; footings never pooled). Not theory closed.

## Object

Single-function generalized-aether / khronometric action (SINGLE_FUNCTION.md §1):

    S = (B/2) ∫√(−g)[R + m²F(I)] + S_m[g],     I = (c2 K² − c1 a_μa^μ)/m²,

with a hypersurface-orthogonal timelike clock, universal metric matter, c3 = −c1 and c4 = 0.
- **De Sitter state:** I0 = 9c2H²/m²; 3H² = (m²/2)[2I0F'(I0) − F(I0)]; α_eff = −c1F'(I0);
  λ_eff = 1 − c2[F'(I0) + 2I0F''(I0)].
- **This packet treats only the degenerate endpoint α_eff = 2** on the actual positive de Sitter state. The regular branch
  (0 < α < 2), already established, is used only as a control.

## Question

At α_eff = 2, derive the full constrained, nonlinear static sourced response on the same de Sitter state, retaining:
- the clock (khronon), lapse, shift (the foliation flow), curvature and boundary conditions;
- the gradients and the convective part of the clock acceleration.

Does a controlled attractive MOND regime exist?
- **If yes:** derive the operational C2 (Newton force), C3 (MOND cubic) and same-state vacuum ε; expose every surviving
  parameter; test the declared principles below for selecting R_amp = εC3²/C2³; state the status of the opposite-branch
  deformation.
- **If no:** record the exact obstruction.

## Method (declared now)

- **M1, exact kinematics (sympy).** For ds² = −A(r)dt² + B_r(r)dr² + r²dΩ² and khronon T = t + τ(r):
  - Compute u_μ, K = ∇_μu^μ and a_μ = u^ν∇_νu_μ exactly.
  - Expand to the sub-horizon weak-field order with v ≡ u^r.
  - Check the exact identities on the flat de Sitter slicing (K = 3H, a = 0) and on Painlevé–Gullstrand Schwarzschild
    (a = 0).
  - Derive the weak-field forms of K and a_r (expected: K = (r²v)'/r², a_r = Φ' + vv').
- **M2, reduced field equations (sympy Euler–Lagrange).**
  - Reduce the action to (Φ, Ψ, v) in the Newtonian limit, with the de Sitter background carried by the flow v = Hr + w and
    Φ_dS = −H²r²/2.
  - Derive the Ψ, Φ and khronon equations.
  - Cross-check independently: the khronon equation must agree with the ADM momentum constraint in unitary gauge (shift
    elimination of SINGLE_FUNCTION §5, kept nonlinear in the trace).
- **M3, endpoint analysis** (α(I0) = 2), for two declared function classes:
  - **E-reg:** F is C² at I0 with F''(I0) ≠ 0.
  - **E-cusp:** F'(I0 + x) = (2/|c1|)[1 − p(√(x/x_a))] for x ≥ 0, with p(y) = y + O(y²); this is the flat-static MOND
    cusp relocated to I0.
  - For each, derive the leading static law, the regime boundaries (h_c), the khronon back-reaction condition and the
    Newtonian-regime foliation tilt.
  - Report a closed-form effective μ if one exists.
- **M4, numerical verification.**
  - Solve the static spherical system for a Plummer source by fixed-point iteration on (Φ', v), with v(0) = 0 and
    v → Hr at the outer edge.
  - Units c = H = 1. Declared values, not tuned to any target:
    - c1 = −1, m = 0.15 and a_M ≡ m√(x_a/|c1|) = 0.2;
    - GM = 1e−13, Plummer radius 1e−8, grid r ∈ [1e−9, 1e−2].
  - Three runs:
    - **E-cusp:** c2 = −1e−5, p(y) = y/(1+y).
    - **E-reg:** c2 = −1e−5, F'(I0 + x) = (2/|c1|)/(1 + x/x_a).
    - **Control L-reg:** α = 1, F'(I0 + x) = (1/|c1|)/(1 + x/x_a).
  - Report g(r), local log-slopes, the regime boundaries and comparison with M3's closed forms.
- **M5, the δK direction and k = 0.** Show whether the shift (momentum) constraint fixes δK uniquely, i.e. whether the map
  is monotone, when the cusp is at I0. Derive the homogeneous (k = 0) Friedmann response near the cusp.
- **M6, health and source analysis.**
  - What is established: classical static spherical existence and uniqueness, and the regimes.
  - What is not:
    - linear de Sitter c_s at α = 2 (strong coupling around h = 0);
    - time-dependent nonlinear stability;
    - khronon tilt near compact objects;
    - preferred-frame and PPN effects;
    - the quantum state and cutoff.
  - No health theorem is claimed from positive quadratic coefficients.
- **M7, amplitudes and principles** (only if a MOND regime exists).
  - Give C2, C3, ε and R_amp in terms of F's parameters, and list the tunings needed (criticality; vacuum at the cusp).
  - Test these declared principles for fixing R_amp:
    - P1, vacuum-at-cusp by a kink (F' jump) instead of tuning;
    - P2, deep-MOND scale/conformal invariance of the static equation;
    - P3, the status of SINGLE_FUNCTION §7's opposite-branch deformation and of the constant (zero-mode) shift of F.
  - No coefficient is fitted or scanned. 128π/9 appears only in the final comparison line.

## Checks (must pass)

- **K1:** the exact kinematic identities of M1 (de Sitter flat slicing; PG Schwarzschild).
- **K2:** the covariant khronon equation equals the ADM momentum-constraint route (symbolic).
- **K3:** the control α = 1 reproduces G_bg = G_bare/(1 − α/2) numerically, to 1%.
- **K4:** the H → 0, v → 0 limit reproduces SINGLE_FUNCTION's flat-static μ = 1 + c1F'/2.
- **K5:** numerical residuals below 1e−8 (relative) at convergence.
- **K6:** M3's closed-form effective μ matches the E-cusp numerics to within 2% in the declared regimes.
- **I1:** the compute code contains no target value (128π/9, 32π, Z, ξ = ¼). The final comparison is in a separate marked
  block.

## Controls (MUTATE, separate outputs; exit 1 when all bite)

- **MU1:** E-reg with α(I0) = 1.9 instead of 2 restores a linear far-field response (local slope of g → −2).
- **MU2:** E-cusp with the cusp removed (p regular, p'(0) = 0 at the same x_a) loses the MOND slope (−1).
- **MU3:** E-cusp with c2 → −1e−3 raises h_c by 100×, moving the quartic floor into the declared grid.
- **MU4:** E-cusp with the cusp sign reversed (p → −p) breaks the attractive deep branch: no physical solution, or
  repulsive.

## Verdict (frozen)

- **Endpoint:**
  - **MOND WINDOW AT THE ENDPOINT:** E-cusp has a same-state static regime with g ∝ √M/r over at least one decade in g,
    attractive, with Newton above.
  - **NO MOND AT THE ENDPOINT:** neither class gives it.
  - **UNDETERMINED:** the numerics or the derivation do not close.
- **Target:**
  - **SELECTED:** a declared principle fixes R_amp = 128π/9 with no free parameter.
  - **NOT SELECTED:** otherwise; list the surviving parameters.
- **Health:** stated per M6. A classical static window is never reported as a healthy microscopic model.

## Hand expectation (disclosed; derived on paper before freezing)

- K = (r²v)'/r², a = Φ' + vv'. Khronon: r²(c2F'K)' = −v(r²α_I a)'. Φ: (2 − α_I)Φ' − α_I vv' = 2GM/r².
- So F'(I)K ≈ F'(I0)K0 up to O((|c1|/|c2|)Φ) terms.
- **E-reg:** quartic, g ∝ M^{1/3}r^{−2/3}; no MOND.
- **E-cusp:**
  - μ_eff = (√(h_c² + 4h²) − h_c)/(2a_M), with h_c = 18(|c2|/|c1|)H²/a_M: MOND for h_c ≪ h ≪ a_M, quartic below,
    Newton above.
  - In the Newtonian regime the khronon tilts, K ≈ √(|c1|/|c2|)h.
  - Back-reaction parameter (|c1|/|c2|)·v_f².
- The δK direction is fixed by a monotone constraint (λ_eff → ∞). The k = 0 response is square-root, with amplitude
  ∝ (|c2|/|c1|)^{3/2}.
- R_amp = (4/3)(H/a_M)²; two tunings; **NOT SELECTED.**

## Register

Rows (AU/FN, not determinate trials) with live ids rechecked before appending, then `kappa_campaign_lee.py`. Light: sympy
and numpy, one core, under 1 GB, minutes. No Lean unless a genuinely new load-bearing result needs it. No downloads.
