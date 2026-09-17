# SPEC_B — the WINDOW THEOREM lane (subagent task)

Write a self-contained research lane at
`/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/navier_stokes_attempt/N05_window_theorem.py`
(plus its `.out` via `python3 N05_window_theorem.py | tee N05_window_theorem.out`
and a `N05_window_theorem_results.json`), and a proof-article
`N05_WINDOW_THEOREM.md` in the same folder.

## The theorem to state, prove (paper-level), and verify numerically

THEOREM (the window theorem — framework-conditioned regularity for classical 3D
periodic Navier-Stokes, ν > 0, f = 0 or smooth forcing):
Let u be a smooth solution on its maximal lifespan [0, T*) with
    sup_{(t,x) ∈ [0,T*)×𝕋³} |Du/Dt| ≤ a₀·W ,   W := 7/2  (the measured floor, 3.5)
where Du/Dt = ∂_t u + (u·∇)u is the MATERIAL acceleration.  Then T* = ∞:
the solution is globally smooth.

PROOF (elementary; write it fully in N05_WINDOW_THEOREM.md):
1. For the flow map X(t; x0) (a diffeo of the torus for smooth u), d/dt u(t,X(t;x0))
   = Du/Dt(t, X(t;x0)), so |u(t,X(t;x0))| ≤ |u(0,x0)| + ∫₀ᵗ |Du/Dt| ≤ U0 + a₀·W·t
   (bound the pointwise derivative of |u| by |Du/Dt| — elementary real analysis).
   Since the flow map is onto at every t: sup_x |u(t,x)| ≤ U0 + a₀·W·t  on [0,T*).
2. Hence u ∈ L^∞(0,T*; L^∞).  By the Prodi–Serrin continuation criterion
   (2/q + 3/p ≤ 1; here q = p = ∞), the solution extends beyond T*:
   T* cannot be finite.  q.e.d.
3. COROLLARY (the framework read): singularity formation requires the flow to
   LEAVE the measured window — any finite-time singularity must have
   |Du/Dt| > 3.5·a₀ somewhere before the singular time.  The window floor is a
   certified no-singularity domain: flows whose material-acceleration content
   stays ≤ 3.5·a₀ (window-class flows: ISM, halo gas, disk-scale dynamics where
   the framework's law is O(1)-active) are provably globally smooth.
4. HONESTY BOX (mandatory, in both files): this is NOT the Clay problem. The
   theorem is conditional: it is vacuous if some flow does leave the window
   (the classical Clay question is exactly whether the exit happens). What is
   claimed: (i) the framework's measured floor places a certified regularity
   ceiling at |Du/Dt| = 3.5·a₀ — below it, no singularity is possible;
   (ii) the Clay singular regime, if it exists, lives strictly ABOVE the floor
   (the Newtonian face of the law). The Serrin criterion is CITED, not derived
   (Prodi 1959; Serrin 1962; also Kato 1984 for the L∞ class).

## The lane: N05_window_theorem.py — checks (PASS/FAIL prints + results JSON)
Use `python3` (miniconda base: numpy+scipy+sympy+matplotlib available).
- G21 THE WINDOW CONSTANTS: a₀ = 9.3619e-11 m/s² (kappa=1/2 canonical), W = 7/2
  exactly (the floor, from LAW_STATEMENT.md — cite the file); the ceiling
  |Du/Dt|_max = a₀·W = 3.2767e-10 m/s²; the trajectory bound
  U(t) ≤ U0 + a₀·W·t computed for t = 10 Gyr: ΔU = 1.034e7 m/s (loose but finite —
  note the bound's honesty).
- G22 THE BOUND VERIFIED ON TRAJECTORY DATA: integrate test trajectories of a
  smooth velocity field on the torus: u(x) = (sin x2 cos x3, sin x3 cos x1,
  sin x1 cos x2)-class (div-free), with a synthetic material acceleration a(t)
  applied along the trajectory: verify |u(t)| ≤ |u(0)| + ∫|a| holds to 1e-8
  relative (RK4 integrate the ODE ẋ = u(x), and the |u|-budget in the same step).
- G23 SERRIIN-CONTINUATION STEP PRESENT: the md file states the criterion with
  citation (Prodi 1959; Serrin 1962) and cites that bounded L∞(0,T;L∞) implies
  continuation; a text gate checks the string 'Serrin' appears in both files.
- G24 WINDOW-CLASS FLOW CATALOG: compute η = |a|/a₀ for named window-class flows:
  LMC ISM cloud accel classes, MW disk a = U²/R ≈ 1.9e-10 m/s² (η ≈ 2.0), halo
  gas at η ≈ 0.1-1: tabulate η vs the floor 3.5: report which classes are
  THEOREM-COVERED (η ≤ 3.5) and which are above (Clay-possible).
- G25 THE EXIT RECASTING: the corollary numbers: singularity candidates must
  exceed |Du/Dt| = 3.28e-10 m/s²; at the singular time the enstrophy divergence
  is forced ABOVE the window — written as the falsifier recipe: an observed
  window-class flow (η ≤ 3.5) that develops a singularity would falsify Serrin,
  i.e., cannot happen; a numerical blowup attempt in the window class must fail —
  register the Galerkin evidence link (N04) and the equilibrium run (N04b).
End with `<N05_window_theorem> COMPLETE: N/M checks PASS.` and the verdict line:
'THEOREM: window-class flows are globally smooth (bound + Serrin); Clay singularities,
if any, live above the measured floor — the window is a certified no-singularity domain.'

## House rules
- Files land ONLY in the navier_stokes_attempt folder. No git. No absolute paths
  in committed content. python3 = /opt/homebrew/Caskroom/miniconda/base/bin/python3.
- The md file must contain the full proof (steps 1-2 above, written out rigorously
  with the estimates displayed), the honesty box, the citations, and a falsifier
  recipe section.
- Report back: the .out tail, the check list, the md word count, and any gate you
  had to amend (with the reason).