# A33 — the master action (lane report)

**Lane:** A33_master_action · **Date:** 2026-10-21 · **Base:** `BRIEF.md`, `FINAL_THEORY.md`,
`core_open_problems_round2_2026_10_20/03_relativity/report.md` §2.
**Script:** `a33_checks.py` (28/28 PASS, exit 0, 1.2 s) · **Output:** `a33.out` · **Data:** `a33_results.json`.
**The document is `MASTER_ACTION.md`** (action, coefficient table, field equations, open list). This file is the
lane card; nothing in it is absent from `MASTER_ACTION.md` or `a33_results.json`.

## Claim

The theory has a single action, and every equation the DSF-21 push derived is a variation, a limit, or an
algebraic consequence of it. In unitary clock gauge, with `K = 4πG`, signature `(−+++)`:

```
L/(N sqrt h) = [R3 + K_ij K^ij - (1+beta) theta^2 - 2 Lambda]/(4K)
               + P^i D_i ln N
               - W(u),  u = K|P|,  W = (a0^2/K)[-u/a0 - ln(1-u/a0)]
               + (eta/2) E_i E^i
               - (gamma/2)(D_i P^i)^2 - (gamma/4) F_ij F^ij
               + L_cold(rho_c, sigma_c ; varsigma) + L_m .
```

The action has **four free numbers** (`κ`, `β`, `η`, `γ`; `κ` and `γ` measured, `β`, `η` only bounded),
**three free functionals** (the `R = 4` scale-setting principle, `ς(r)`, the turn-off form), and **no other
freedom**. `y_t = 66.2999` is *derived*, not free. Five degeneracies are named (γ↔η, γ↔L\*, κ↔a₀,
β↔Λ_bare, ς↔f_ret).

## Derivation

1. **Action.** As above; the cold sector is a collisionless medium (`Vlasov`, `T^c_{μν}` as the second moment,
   `p_c = ρ_cσ_c²` with `σ_c = √(a₀L_*)` a fixed dispersion), split by the *sourcing identity*
   `D_iP^i = ς(ρ_c − ρ̄_c)` — a matching condition, not a Lagrangian term.
2. **Coefficient table** (`MASTER_ACTION.md` §2, `a33_results.json → coefficient_table`, 13 rows). Status per
   coefficient: `D` derived (EH, Λ–a₀ closure, clock = 1, `W`, `L_m`), `M` measured (Λ, γ via `L_*`,
   ρ_c, ς, κ), `F` free (β, η), `C` chosen (γ_F = γ_L), `P` posit (the turn-off form).
3. **Field equations**, all in closed form with coefficients substituted: lapse (Hamiltonian constraint),
   shift (momentum constraint with the P current), P, the cold-sector Vlasov/Jeans pair, and the two
   cosmological equations `3(2+3β)H² = 2Λ + 4Kρ`, `(2+3β)(2Ḣ+3H²) = 2Λ − 4Kp`.
4. **New constraints found while assembling.** (i) The background forces `Λ_bare ≥ 3H₀²/c² = 1.462 Λ_obs`
   (else `β < 0`, which the principal-positivity bound forbids) — the endpoint is a pure de Sitter universe, not
   a ΛCDM one; (ii) `ς` cannot be a coefficient of the action (a constant `ς = 0.4716` deforms the law by 24 %);
   it must be the catchment `f_ret`; (iii) `γ = KL_*²/2` is a *definition* of `L_*`, so it derives nothing —
   `L_*` is measured, not derived; (iv) A3's reduced P equation is missing its `γP″` term (its `Dt` chain never
   applies `∂²L/∂P′²`), which affects no conclusion because that lane evaluates at `P = 0`.
5. **Cold-sector clarification.** `Γ = 2` "pressure" of A16/A20 is the P sector's gradient energy
   `(γ/2)(D·P)²` with `D·P ↔ ρ_c − ρ̄_c`, not the medium's kinetic pressure: the elastic speed is 0.72 m/s
   while the kinetic dispersion is 8.33 km/s. The `r_switch` scaling survives; its attribution changes.

## Status

`DERIVED` (the assembly: every result is a variation of one action) **+ CONDITIONAL** on three unfixed
functionals: the scale-setting functional (`κ`), `ς(r)`, and the turn-off origin. Not `CLOSED` in the
BRIEF's sense — this lane completes the *equations*, not the three missing principles, and says so in §6 of
`MASTER_ACTION.md`.

## Checks (`a33_checks.py`, 28/28 PASS, exit 0)

| id | proves | value |
|---|---|---|
| K1, K1b | lapse eq = Hamiltonian constraint; `R3` on isotropic Schwarzschild | 0; [0,0,0] |
| K2 | P equation (static spherical, `f=1`) from the action | ratio `NV` |
| K3, K3b | `g_N = g²/(g+a₀)`; the quadratic `W` gives a different law | 0; nonzero |
| K4 | the law is AQUAL with `μ = x/(1+x)` | 0 |
| K5 | clock coefficient = 1 (0.55 a₀ deviation at `ξ=2`) | 0 |
| K6 | `c_T² = 1` | 1 |
| K7 | slip `Π = O(ε²)` | `q²`; 0 |
| K8a–c | `θ=0` static; no momentum density; `α₁` from a linear potential | 0,0,0 |
| K9 | `c_s = √(γ/η)` | γ/η |
| K10, K10b | `H² = 2Λ/(3(2+3β))`; second cosmological equation | exact |
| K11a,b | `L_*² = 2γ/K`; `r_switch = L_*√(f_c n(3−n)/2)` | exact |
| K12a,b | unique `u=0`; `m² = K/η` | `[0]`; K/η |
| K13a–c | `ρ_c = ρ̄_c + D·P/ς`; `D·P = ∇·((1−μ)∇Φ)/4πG`; saddle needs `114.8 ρ̄_c` | 0,0,114.8 |
| K14a–c | `Λ = 32πa₀²/c⁴`; `a₀` from Λ; κ = ½ identity | rel 1.2e-3 |
| K15a,b | `ς = f_ret(u/g_c)`; a constant partition is excluded | 0; 0.243 |
| K16 | `Λ_bare ≥ 1.462 Λ_obs` | β = −0.211 |

Mutations (`--mutate`), each exit 1: `clock2` (K1,K2,K5), `nocharge` (K1,K2,K5), `wquad` (K3,K4),
`gamma0` (K11b), `beta0` (K10), `ricciP` (K6). Recorded in `MUTATE.md`.

## What this does not do

- Does not derive `κ`, `ς(r)` or the turn-off; those stay open with the missing premise named.
- Does not solve the exact static system at general `(β, η, γ)` and `f ≠ 1` — the `f`-equation is used only to
  check the exact Schwarzschild solution.
- Does not reproduce A13/A23's saddle *amplitude*: the identities and the sign are verified (K13), the
  amplitude is quoted from A13 and flagged. A from-scratch axisymmetric solve is 35 % off on the single-mass
  validation, so it is not used to adjudicate.
- Does not check the cosmological slip (`E²` active), which A12 leaves open.

## Next

1. Attack `ς(r)` as a retention problem (`f_ret(M, environment)`), not as a term in the action.
2. The one equation that would close `κ`: a local functional, no dimensionful parameter, stationarity on
   de Sitter returning exactly 4.
3. Decide whether the turn-off can be a `P`–curvature coupling; if it can, it belongs in the action and the
   posit disappears.