# The retarded nonlocal MOND kernel is unstable on MOND backgrounds — VERDICT (2026-09-02)

**Result.** At linear order on a uniform MOND background (Z̄ = 4y², WKB), the scalar sector of the in-in theory built on
X = □⁻¹_ret(R_μν u^μ u^ν) with an algebraic f(Z) — the Deffayet–Woodard kernel and the CCNL candidate alike — has
- a **longitudinal gradient instability** for y ≳ 0.5 (transition to Newton): complex ω² with Im ω = (0.2–0.5) ck
  (e-folding 1.3 × 10³ yr at 1 kpc, 13 yr at 10 pc, 2 days at 1000 AU), growth ∝ k (UV-unbounded, no cutoff in the action);
- a **negative-energy propagating mode** (ghost) in the real-frequency deep-MOND window y ≤ 0.25.
Script: `ccnl_inin_linear_scalar_2026.py` (rc=0, 12 checks; the physics checks are findings that can fail to materialise; the
f″→0 ablation is the control). Output in `.out`.

## What was computed
Newtonian gauge, plane symmetry, c = 1, 16πG = 1. Quadratic action from √−g R (exact to O(ε²)), √−g a₀² f(Z) expanded around Z̄
keeping every term with the background gradient s (Z̄ = 4s²/a₀²), √−g ξ(□X − R_uu) at O(ε²) (ξ̄ = 0), and √−g K(Q) for the clock
(manual exact-to-O(ε²) expansion of Q; SymPy's series drops the gradient term). Linear Euler–Lagrange equations → plane-wave
matrix M(ω,k) on (Φ, Ψ, δX, δξ, δϕ). Leading order in a₀ → 0 at fixed y (vacuum-energy and 1PN terms drop; the clock row,
homogeneous in K₂, is normalised). In-in reduction: the auxiliary rows are eliminated by their particular (retarded) solutions,
i.e. the Schur complement; the pure-auxiliary poles det D = −(k−ω)²(k+ω)² are the modes null data removes.

## Internal checks that passed before any physics was read off
| check | result |
|---|---|
| GR + clock limit (kernel off) | (Φ,Ψ) block det = −16k⁴ (no scalar metric mode); the clock mode ω² = u/(1+u)·k² exactly |
| ordinary local auxiliary block at y=1 | [[−4e⁻¹, 1],[1, 0]], det −1 — the 09-02 Dirac audit's matrix, reproduced independently |
| static longitudinal response | Ψk²/ρ = −1/(4μ_∥) with μ_∥ = d(yμ)/dy = 1 − 2f′ − 4Z̄f″ = 1.000 at y=1; Φ = Ψ |
| background residuals | all O(a₀²) (Λ, a₀²f₀, f′s², K₂Q₀²u): a legitimate WKB background |

## The dispersion, and its robustness
At y = 1 (f_exp): (e+3)ω⁴ − (2e−1)k²ω² + e k⁴ = 0, discriminant 1 − 16e < 0.

| test | outcome |
|---|---|
| y-scan, f_exp | stable (real ω²) at y = 0.10, 0.25; complex at y = 0.5, 1, 2, 3, 5, 8 (Im ω/k = 0.21, 0.39, 0.44, 0.36, 0.18, 0.05) |
| DW's own f = ½Z e^{−√Z/3} | complex at y = 0.5, 1, 2, 4 (Im ω/k up to 0.48); real at 0.25 and 8 |
| ablation f″ → 0 at fixed f′ | stable at y = 1, 2 (one real propagating mode): **the instability is the f″ (μ′) term** |
| ablation f′ → 0 at fixed f″ | unstable (Im ω/k = 0.60, 0.52) |
| transverse propagation (k ⊥ ∇X̄) | stable at y = 0.5, 1, 2, 4: **longitudinal only** |
| deep-MOND window energy signs | y = 0.10: modes ω/k = 0.236 (E > 0) and 0.947 (E = −7.8 × 10³); y = 0.25: 0.417 (+), 0.847 (−4.1 × 10²) |
| metric content of the unstable mode | 6% (Φ,Ψ), 86% (X,ξ): nonzero metric content, so it is a mode of the reduced in-in metric equation, not a null-data-removed auxiliary mode |

## Mechanism
MOND requires μ′ ≠ 0. Any carrier of μ(|∇Φ|) that is dynamical — locally (the FC-KH khronometric a_μ-coupling, killed 08-31 by the
radial gradient instability on a₀ < a < 38a₀) or by retardation (here) — turns μ′ into a wrong-sign longitudinal kinetic term in the
transition regime. The static AQUAL operator is elliptic and safe (λ_∥ = μ + yμ′ > 0); the time-dependent completion is not. The
in-in prescription removes only the pure-auxiliary poles at ω = ±k; the metric-coupled modes survive under either definition,
because det M = det D · det M_red.

## Consequences
- **CCNL-MOND is dead at gate 7.** Its 29 local-Lagrangian gate passes stand as computed, and are moot.
- **Deffayet–Woodard 2026 (and the 2011/2014 kernel) inherit the same result**: their paper has no perturbation analysis; the
  Codex sf45 "G2 PASS" was on Minkowski/FLRW, where Z̄ = 0 or f is dead — never on a MOND background.
- **The nonlocal door of `FRIED_CHICKEN_VERDICT_2026-09-01.md` is closed at linear-WKB order.** With the local carriers (α₃ pincer,
  luminality, slip) and the aether (α₁) already closed, every class examined fails. Outcome B, not A.

## Scope, stated honestly
Linear order; uniform-gradient WKB background (a₀ → 0 at fixed y); plane symmetry and Newtonian gauge; the specific kernel
structure (u-projected R_uu, algebraic f(Z), no higher-derivative terms). Not covered: nonlocal form factors acting on the Weyl or
Einstein tensor (the "field-dependent spin-2" residual, for which no action exists); non-WKB backgrounds (a bounded system with
its own scale — the instability's growth ∝ k makes the WKB regime the relevant one); the fully nonlinear problem. A UV completion
with higher spatial derivatives could cap the growth at some k_max, but the action as written has none, and DW state their
philosophy is an IR modification.

## Priority
The radial-gradient-instability mechanism for μ′-carrying relativistic MOND is the repo's FC-KH result (08-31); its appearance in
the nonlocal kernel is new here. The Dirac structure of the localised pair is the 09-02 audit. Literature: no perturbation analysis
of the DW MOND kernel on a MOND background is known to us (DW 2026 §4.2 defers it; Woodard 2014 lists it as future work).

---

## Addendum 2026-09-02 (later): two more doors on the same kernel, both shut

### The spatially projected kernel (the natural next door) — closed
Tonight's mechanism pointed at the term $-4f'(Z)(\partial_tX)^2$ (the time derivative of the retarded scalar inside $f$). AeST avoids
it by projecting its invariant onto the frame's spatial slice, and the kernel already carries a frame, so the same projection is free:
$Z_\perp=(4c^4/a_0^2)\,q^{\mu\nu}\partial_\mu X\partial_\nu X$, $q=g+uu$. Statically $Z_\perp=Z$, so every static gate is untouched.
Script `ccnl_projected_kernel_linear_2026.py` (13 checks, rc=0, `.out`), same machinery, same internal checks (GR limit, $\mu_\parallel$,
$\Phi=\Psi$, the Dirac block). Result: the projection removes the $y=0.5$–$1$ instability but **not the disease**:

| test | projected kernel |
|---|---|
| $f_{\exp}$, $y$-scan | real at $y\le1$; complex at $y=2,3,5,8$ ($\mathrm{Im}\,\omega/k=0.37,0.31,0.16,0.05$) |
| DW's $f$ | complex at $y=1,2,4$ ($\mathrm{Im}\,\omega/k$ up to 0.45); real at 0.25, 0.5, 8 |
| $f''\to0$ | stable (control) |
| transverse | stable (longitudinal only) |
| energy signs, real-frequency $y$ | a negative-energy mode at $y=0.10,0.25,0.5$ ($E=-188,-176,-166$) |

The $f''$ ($\mu'$) term is spatial; projecting the time part of $Z$ cannot remove it, and it still couples through the indefinite
localization pair. The window shifts up; the ghost stays. Closed at the same order.

### A second, independent kill: $c_T\ne c$ on galaxy backgrounds
Every "$c_T=c$" certification of this kernel class (including the Codex sf45 gate and this session's E1–E2) is the linear statement
$R^{(1)}_{uu}[h^{TT}]=0$ on a background where the multiplier vanishes. On a real MOND galaxy it does not vanish: the static
multiplier equation is $\nabla^2\bar\xi=8\nabla\cdot(f'\nabla\bar X)=4\nabla^2\Psi_{\rm ph}$, i.e. $\bar\xi=4\Psi_{\rm ph}$, sourced
by the phantom density, of order $v^2/c^2$ in every MOND zone. Script `ccnl_kernel_tensor_speed_2026.py` (6 checks, rc=0, `.out`):
- $R^{(2)}_{uu}[h^{TT}]=h\ddot h+\tfrac12\dot h^2\ne0$ (exact);
- the TT dispersion of $\sqrt{-g}[R+\bar\xi R_{uu}]$ is $(1-\bar\xi)\omega^2-k^2=0$: $c_T^2=1/(1-\bar\xi)$ — the Case-3a form
  $c_T^2=1/(1-2\lambda)$ with $\lambda=\bar\xi/2$; control $\bar\xi=0\Rightarrow c_T=1$;
- Milky-Way-like galaxy, exponential law: $\Psi_{\rm ph}/c^2=-7.3\times10^{-7}$ at 8 kpc, $\bar\xi=-2.9\times10^{-6}$ (8 kpc),
  $-2.0\times10^{-6}$ (30 kpc);
- $|c_T/c-1|\approx|\bar\xi|/2=1.5\times10^{-6}$ against GW170817's $7\times10^{-16}$: **excess $2\times10^9$**.
A path-average over the MOND zone's fraction of the GW170817 path reduces this by $10^{-1}$–$10^{-2}$, not by $10^9$. The retarded
kernel, once localized on a galaxy, is a clock coupled to $R_{nn}$ — the class the 09-01 verdict already killed by luminality — and it
inherits that kill independently of the instability. Deffayet–Woodard 2011/2014/2026 inherit it too.

### Standing after tonight
The retarded nonlocal MOND kernel fails at two independent gates (stability; tensor speed), for either interpolation function, for
either time-projection of $Z$, and under either definition of the theory. The 09-01 "one door left" is closed by committed computation.
Not covered, still: nonlocal form factors on the Weyl/Einstein tensor without a frame projection — but the slip-lock theorem says a
frame-free single-metric completion cannot produce MOND lensing, so that residual is caught between two closed doors.
