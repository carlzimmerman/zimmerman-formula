# AS079 — Entropy second variation on the constrained shell

**Run:** `AS079_r001_deepseek-v4-flash-0731_20260928T130645Z`
**Seed:** `deepseek_push/astra_spawn_ideas/AS079_entropy_second_variation_on_the_constrained_shell.md`
**Seed sha256:** `a12c8abd5ef444d40115ffda5907391bdbd529ebe5e3ef778cc9d3c287c87f98` (verified; file executed as on disk)
**Worker:** deepseek/deepseek-v4-flash-0731 via Hermes Agent (subagent), host macOS 26.5.2
**Started / finished (UTC):** 2026-09-28T09:49Z (compute) / 2026-09-28T14:08Z (package); compute run stamp 20260928T130645Z

---

## 1. Framework cell (as adopted)

- Cosmological acceleration: `a0 = kappa * c * sqrt(G*rho_Lambda)`, **kappa = 1/2 ADOPTED**.
- Baryonic scale: `r_M = sqrt(G M_b / a0)`, natural logarithmic well constant `C = sqrt(G M_b a0) = v_flat^2` (G084).
- Virial temperature: `sigma^2 = C/2` (G091/g03g chain), so `beta = 1/sigma^2` and the profile exponent is
  `gamma = beta * C = 2` (certified: theorem `exponent_two`, Lean).
- Entropy `S = -∫ ρ ln ρ dV`; energy `E = ∫ ρ(3σ²/2 + Φ) dV` with the fixed log well `Φ = C ln(r/r_ref)`, `r_ref = r_M`.
- Dimensionless: `u = r/r_M`, `dV = 4πu²du`, `ρ̃ = ρ r_M³/M_b` (∫ρ̃ dṼ = 1), `ẽ = e/C = 3/2 + ln u` with σ² = C/2, i.e. `ẽ = 3/4 + ln u`.
- EL identity on the shell: `-ln ρ̃0 - 1 - α̃ - 2(3/4 + ln u) = 0`; stationary profile `ρ̃0(u) = A u⁻²` with
  `α̃ = ln(1/Z) − 5/2`, `Z = ∫u⁻²dṼ = 4π(u_R − u_in)` exactly on the trapezoid grid (certified identity: `el_identity`, Lean).
- **Numerics:** G = 6.67430e-11, c = 299792458, M_sun = 1.98847e30, pc = 3.085677581491367e16 (SI). G_N/G_bare/G_cosmo kept separate (only G enters; no bare/cosmo substitution made in this task).
- Branches: filtered MONO + criterion B operative (FRIED_CHICKEN_SPEC amendment, verified at start).

## 2. Claim under test (exact statement)

On a spherical shell Ω = {r_in ≤ r ≤ R} with the fixed log well and the (M, E) constraints
`∫ρ dV = M_b`, `∫ρ e dV = E₀`, for any admissible (mass/energy-conserving) mode `v = δρ`:

```
δ²S|_v = -∫ (δρ)²/ρ₀ dV  < 0       (strictly concave tangent direction)
```

derived from `δ²S = -∫(δρ)²/ρ dV` at fixed potential; the first variation vanishes on the tangent space; the
finite-amplitude gap `S(ρ₀) − S(ρ₀+εv) = ∫[ρ ln(ρ/ρ₀) − (ρ−ρ₀)]dV ≥ 0` with equality iff ρ = ρ₀ (unique maximum).

## 3. Derivation of every intermediate factor, sign, unit

**Second variation.** S = −∫ρlnρ dV; ρ = ρ₀ + εv. Term-by-term:
- `dS(ρ₀)·v = −∫(ln ρ₀ + 1)v dV` → on the tangent space vanishes by the pointwise EL identity
  `(ln ρ₀ + 1) = −(α̃ + 2ẽ)` (each grid point; certified), plus `∫v dV = 0`, `∫ẽv dV = 0` (projection, exact to ~1e-15).
- `d²S(ρ₀)(v,v) = −∫ v²/ρ₀ dV < 0` — pure quadratic in the mode, **no constraint curvature**: the constraints are
  affine in ρ, so the constrained and unconstrained second variations coincide. This is the entire content of
  "second variation on the constrained shell": the log-well constraint manifold's geometry is inherited from the
  tangent plane, and the Hessian restricts to it unchanged.

**Units/factors.** All checks run dimensionless (u, ρ̃, ẽ); conversion factors 1/σ², C, r_M carry no numerical
value here except through the exponent identity γ = βC = 2 (certified). The minus sign: S is convex in ρ
(S″ = −1/ρ < 0 → concavity of the negative-entropy functional), so the second variation is negative.

**Back-of-envelope check of the sign for G_N-vs-G:** numerical values are acceleration/proper-distance based
(r_M from G M_b / a0); only G enters (M_b = M_sun, a0 = κc√(Gρ_Λ) with κ = 1/2). G_bare/G_cosmo are untouched.

## 4. Execution structure (steps of the seed, all 6 check groups)

- **C1** — EL stationarity of the u⁻² profile (symbolic: sympy pointwise identity check; `el_identity` certified in Lean).
- **C2** — admissible perturbations: 6 interior fixtures × (sin kπx, k = 1..4,6, and two bumps) × 2 amplitudes = **84**
  central differences `S(ε)+S(−ε)−2S(0)`; Gram–Schmidt projection off the **dV-weighted** constraint gradients
  `gM = dṼ`, `gE = ẽ·dṼ` (modified Gram–Schmidt: gE orthogonalized against gM first — sequential subtraction is
  WRONG: it reintroduces the mass component; this bug was found and fixed). Max post-projection constraint
  residuals `|∫v dV| = 2.8e-15`, `|∫ẽv dV| = 1.7e-15`; max `|dS·v| = 1.6e-15`; all 84 central values < 0 and equal to
  `−ε²∫v²/ρ₀` to max relative `3.1e-4` (the O(ε⁴) Taylor remainder, predicted by C2d).
- **C3** — independent representations:
  - C3a: 50-dps mpmath central difference (sin2, ε=2e-3, fixture 0.01/0.62). Residual = O(ε⁴) term
    `−(ε⁴/6)∫v⁴/ρ₀³` to 1.19e-5 relative; subtracting the exact O(ε⁶) term `−(1/15)ε⁶∫v⁶/ρ₀⁵` leaves the O(ε⁸)
    tail at 4.3e-14 relative; 50-dps equals float64 residual to 3.6e-14 (no floating-point contamination).
  - C3b: direct differentiation `d²S/dε²|₀` via exact ray derivative finite differences = −∫v²/ρ₀ to 5.9e-8 relative.
  - C3c: global Bregman gap at ε = 0.05, pointwise integrand `ρ ln(ρ/ρ₀) − (ρ−ρ₀) ≥ 0` everywhere (min −1.1e-13 at
    (0.01,0.62) = float noise; exact statement certified in Lean: `kl_nonneg`, `kl_pos_of_ne`); gap 2.273e-3 and
    3.483e-3 at the two fixtures, accounted for to 0.09%/0.01% by the quadratic+cubic+quartic Taylor terms
    (ε²/2·A₂ − ε³/6·A₃ + ε⁴/12·A₄; A₂=∫v²/ρ₀, A₃=∫v³/ρ₀², A₄=∫v⁴/ρ₀³ — coefficients derived, not fitted).
- **C4 (negative control, capable of failing)** — the SAME bump **without** projection: `∫w dV = +0.103 ≠ 0`
  (mass violating, REJECTED as a constrained test); `dS·w = −0.348 ≠ 0` and the linear term dominates the
  quadratic for all ε (ratios 4e3 → 8e5): the sign of δ²S along w is true but IRRELEVANT (w leaves the manifold).
  Projected control of the same bump: admissible (`∫v dV = 5.9e-17`) and passes: central −3.367e-6 = −ε²∫v²/ρ₀
  to 4.2e-6 relative.
- **C5** — transfer checks (regimes):
  - C5a deep exterior (y ≤ 0.01 < y_star, MONO = RAR on the splice): kernel/log-well acceleration ratio
    `1 + 1/(2u) + 1/(12u²) + …`: 5.0833% at 10 r_M, 0.5008% at 100 r_M; leading term analytic and matched.
  - C5b exterior EL residual: spread vs log well ~1e-15 (exact stationary point of the log-well problem on every
    shell); vs the FULL MONO-deep potential exactly `2·spread(Φ̃_full − ln u)`: 0.0506 (10,2), 0.0908 (10,10),
    0.0050 (100,2), 0.0090 (100,10) — O(1/u), i.e. the interior ansatz is a CONTROLLED deep-exterior fixture.
  - C5c interior: the log well is NOT the full nu_mono potential in the knee region: spread vs MONO up to 311
    ((0.01,0.62)) down to 1.24; vs Newtonian equals exactly `2·[(1/u_in − 1/u_R) − ln(u_R/u_in)]` on all six
    fixtures (ratio 1.000 each) — quantified grounds for the seed's warning that interior fixtures test the
    imposed-log-well ansatz, not the operative kernel.
- **C6** — boundary cases: (a) thin shells R → r_in: `cos(gM,gE)` 0.6345 → 0.999999 (constraint pair degenerates;
  tangent codimension-2 structure persists, dS·v still ~1e-16); (b) singular inner limit r_in → 0: ρ₀ = u⁻²
  integrable, M = 1.0000000000, S(ρ₀) = −9.031e-1 finite, Hessian stays negative (δ²S = −3.317e-2 at r_in/R = 1e-6).

**Negative control capable of failing:** C4 (mass-violating perturbation) — it does fail as an admissible mode
(C4 REJECTED) and the projected control passes (C4b). C5c also "fails forward": the transfer check shows the
interior nu_mono residual is O(1–10), proving non-transferability quantitatively. Both behaved as designed;
no check was weakened to pass.

## 5. Independent verification

`AS079_second_variation_alg.lean` (also in this run dir) certifies in Lean 4 (mathlib, leanprover/lean4:v4.34.0-rc2,
zero `sorry`, `#print axioms` = {propext, Classical.choice, Quot.sound} only, verified by
`cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS079_second_variation_alg.lean`, exit 0):
(A) `log_le_sub_one`; (B) `kl_nonneg` — pointwise Bregman ≥ 0; (C) `kl_pos_of_ne` — equality only at the maximizer;
(D) `exponent_two` — γ = βC = 2; (E) `el_identity` — the EL identity; (F) `second_order_exact` — exact pointwise
central-difference decomposition; (G) `second_order_bound` — ε²u² ≤ −(log(1+εu)+log(1−εu)).

## 6. Execution bounds actually enforced

- Wall: `ulimit -t 120` + `alarm(120)` in-script; actual 8.718 s (< 120 s) — enforced, not merely declared.
- Memory: RLIMIT + in-script RSS check at 512 MB; actual peak RSS 92.5 MB.
- Threads: 1 (OMP/OPENBLAS/MKL/NUMEXPR/VECLIB pinned to 1; single process).
- Grid: geometric, n = 1200; fixtures as above; mpmath 50 dps for C3a.

## 7. Limitations (what this does NOT establish)

- Not a statement about the physical MONO kernel: interior fixtures test the imposed-log-well ansatz (C5c
  quantifies the O(1–10) deviation); exterior decks only reach `1 + 1/(2u)`-level corrections to the kernel.
- No global (whole-space, unconstrained) maximizer: fixed-well boundary conditions; no proof that the constrained
  maximizer exists for all (M_b, E₀) (C6b only probes the singular limit).
- No dependence on G_N vs G_bare/G_cosmo established; only G enters here.
- Float numerics are residual-driven (no booleans): all PASS values are actual residuals as recorded in
  raw_output.log / raw_output.json.