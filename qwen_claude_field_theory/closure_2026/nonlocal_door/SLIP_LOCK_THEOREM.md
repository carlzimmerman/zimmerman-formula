# The slip-lock theorem — correct MOND lensing REQUIRES a preferred frame (analytic)
**Closes the last single-metric door (un-localized nonlocal F+) and upgrades the 108k numerical pincer
(DC-001) to an analytic theorem.** Script: `ghost_theorem_lensing.py` (exact linearized Ricci, sympy).

## Honesty note (the adversarial audit worked)
My first proof of this claimed "ghost-free ⟺ M positive-definite" and derived a PSD-vs-enhancement
contradiction. **That had a sign error** — the Schur complement gives M = −Lvvᵀ (negative-semidefinite),
and NSD alone does NOT forbid the cell (counterexample M=[[-2,1],[1,-1]] gives η=1, E>1, ghost-free).
A 3-skeptic adversarial workflow (0/3 refuted the conclusion) flagged the wrong mechanism. The
CONCLUSION was right; the MECHANISM is diffeomorphism invariance, not a PSD count. Corrected below.

## The theorem
Newtonian gauge, quasi-static, Fourier (m ≡ M_p²k²). Φ = time potential (matter feels ∇Φ), Ψ =
curvature; lensing ∝ Φ+Ψ; slip η ≡ Ψ/Φ (η=1 ⟺ lensing tracks dynamics, the observed no-slip fact).
1. **Exact linearized Ricci scalar** (from the metric, verified): R⁽¹⁾ = −2∇²Φ + 4∇²Ψ ⇒ covariant
   curvature couples in the FIXED direction v = (−2, 4) ∝ (1, −2).
2. **Diff invariance locks the coupling.** A frame-free extra mode can only couple to the metric through
   covariant curvature, so integrating it out adds M = −L·vvᵀ (L=1/K>0) — pinned to the vvᵀ ray. Any
   number of modes / any nonlocal form factor L(k) stays on the SAME ray.
3. **On the ray, η = (4L+m)/(8L+m).** η=1 has ONLY the trivial solution L=0. Any real coupling gives a
   nonzero slip η≠1 — the f(R) γ=½ disease. Enhancement E=(8L+m)/(6L+m)>1 always comes WITH the slip.
4. **⇒ Frame-free single-metric gravity cannot produce correct MOND lensing.** Enhancement and no-slip
   are incompatible on the diff-invariance-locked ray.

## Why a preferred frame escapes (and why every survivor needed one)
The only way to source the anisotropy (Φ−Ψ) in a direction DECOUPLED from R is a preferred-frame vector
uᵘ: u-projected couplings (u^μu^ν, a·∂χ, …) live OFF the curvature ray and can set η=1 independently of
the enhancement. That is exactly AeST/TeVeS/khronometric. So a preferred-frame carrier is NECESSARY for
MOND lensing — the analytic content behind Bekenstein's disformal being the unique 108k survivor.

## Map after this result
- **Frame-free single-metric ≤2-deriv:** closed (this theorem — always f(R) slip).
- **Preferred-frame single-metric:** the frame is now *forced*, but that branch is where P7/GW170817
  bites (khronometric/AeST → strong coupling / α₂; KM-X1 + door1 this session). Both sub-branches of the
  single-metric ≤2-deriv class are therefore under closure pressure from opposite directions.
- **Honest remaining doors (all EXIT this class):** a genuine second dynamical metric (Hassan-Rosen
  bimetric — massive graviton, its own ghost/《c_T》 bill), higher-derivative gravity, or the a₀-bump
  cluster route. Each carries a specific, known cost to price next.
