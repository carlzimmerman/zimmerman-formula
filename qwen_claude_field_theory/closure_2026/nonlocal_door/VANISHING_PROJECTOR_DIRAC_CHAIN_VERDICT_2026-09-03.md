# Vanishing spatial projector: the Dirac chain through the rank bifurcation — 2026-09-03

**Closes the residual named in `METRIC_ONLY_ELLIPTIC_PROJECTOR_RANK_CHANGE_2026-09-03.md`.**
Script: `vanishing_projector_dirac_chain_2026.py` (11/11, sympy Poisson brackets, mutation controls reproduce the
repo's Lorentz-branch ghost and the fixed-background det C = B⁴k⁸).

## The loophole
A Poincaré-equivariant tensor cannot be a nonzero rank-3 spatial projector at Minkowski, but
H^{μν} = X(g^{μν}+u^μu^ν), X = −V² > 0, is rank 3 away from zero field and vanishes smoothly at X = 0. Its
auxiliary sector S_aux = ∫√−g λ(H^{μν}∇_μ∇_νχ − J) changes constraint rank as X → 0. Left open as "a rank
bifurcation rather than a nonexistence theorem."

## The chain (u-frame, mode k ≠ 0)
H^{00} = X(−1+1) = 0 ⇒ **no time derivatives survive**: L = −Xk²λχ − Jλ.
- **X ≠ 0:** primaries p_λ, p_χ; secondaries −Xk²χ − J, −Xk²λ; det C = X⁴k⁸ ≠ 0 ⇒ four second-class, multipliers
  fixed, no tertiary. **DOF = 0.** On-shell χ = −J/(Xk²), λ = 0.
- **X = 0:** φ₄ ≡ 0, φ₃ → −J (a constant). Surviving constraints {p_λ, p_χ} commute ⇒ **first class**, λ, χ pure
  gauge. **DOF = 0.** Consistency requires **J(X=0) = 0**: the source must carry a factor of X.
- With J = XJ̃ the chain is consistent on both branches. **The bifurcation changes the CLASS, not the COUNT.**

## Why it dies anyway
The surviving channel is χ = −J̃/k² with **no ω anywhere**: an instantaneous elliptic potential in the u-frame. That
is the gate-7 failure by definition. By the committed pincer (N_grav=2 ⇔ MOND via second-class constraint ⇔
ω-independent 1/k² ⇔ α₃ = O(1)) it carries α₃ = O(1), excluded ~10¹⁹× (pulsar). The field-dependent projector is a
**local elliptic constraint that switches itself off at zero field** — it lands on the DC-019 / York-CMC / CDE-L4C wall.

## Scope
Conditional on the repo's u-frame k-space reduction and on the pincer's instantaneous ⇒ α₃ link. This closes every
metric-only elliptic projector route that has been written, including the smoothly-vanishing one. What remains for
door B is not a loophole but an unwritten construction: a genuinely retarded (ω-dependent) nonlocal kernel giving
μ = 1−e^{−y} — and §4 of the state-space verdict shows positive spectral weight means extra carrier states (gate 2′).
Never say "door B closed"; say every written route through it is.
