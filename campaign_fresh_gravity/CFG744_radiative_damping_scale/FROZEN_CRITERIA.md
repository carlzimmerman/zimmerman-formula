# CFG744 — does radiative relaxation reach galaxy scales? (frozen criteria, committed alone)

Block CFG740–749. Written 2026-10-13, before any CFG744 number. κ = ½ fitted; both footings; the cold energy's mass is
required; no particle species; not theory closed.

## Why (a correction to CFG743's reading)
CFG743 compared oscillation **periods** to a bar. Settling needs **damping**. In CFG696 the only damping is radiation; with a
reflecting boundary nothing relaxed. Linearised about the static profile at large s, the equation is
δv_tt = δv″ − (2/s)δv. A perturbation of scale s₀ therefore has ω² ≈ k² + 2/s₀, group velocity ≈ 1/√(2s₀) for k ~ 1/s₀, and
escape time **t_esc ≈ √2 s₀^{3/2}** (code units ℓ_γ/c_P). That is about s₀/π local periods. Galaxies sit at s₀ = r/ℓ_γ ~ 10⁶.

## Tests
- **N1 (numerical, CFG696 code).**
  - Domain S = 400, ds = 0.05, dt = 0.025, t_end = 4000, outgoing boundary; initial state 2× static.
  - Record the mean relative error |q − q_static|/q_static over [0.8 s₀, 1.2 s₀] for s₀ ∈ {10, 20, 40, 80}.
  - t_1% = first time after which it stays below 1%.
  - **PASS (scaling confirmed) iff the log-log slope of t_1% vs s₀ is in [1.2, 1.8]** (theory 1.5).
- **N2 (physical).** t_relax = A s₀^{3/2} ℓ_γ/c_P, with A taken from N1's fit (no new number). Evaluate for M_b ∈ {10⁹, 10¹⁰,
  10¹¹} M☉ at y = 0.1 and 1 (r and ρ_c as in CFG743), both footings, at L* = 5.754 pc, ℓ_γ = L*²/(2r_M), for:
  - **(a) the cold-medium identification:** c_P² = γ/I = 2πG L*² ρ_c(r), with I = 1/ρ_c(r) (the nonlinear identification of
    CFG743);
  - **(b) an independent light field with c_P = c.**
- **PASS for an identification iff t_relax ≤ 4.6 Gyr** (three relaxation times in 13.8 Gyr) **at every (M_b, y).**

## Verdict
- If N1 passes, (a) fails and (b) passes: the radiative mechanism works only for an independent light field. Candidate B with a
  mechanism (the medium identification) has **no relaxation channel** at galaxy scales, unless collisionless relaxation
  supplies one (not shown on the record). The C3 reading in CFG743's post-hoc note is then moot for the medium identification.
- Other outcomes are reported as they fall.

## MUTATE (`CFG744_MUTATE=1`, exit 1 iff it bites)
Reflecting boundary: t_1% must not be reached at s₀ = 80 within t_end.
