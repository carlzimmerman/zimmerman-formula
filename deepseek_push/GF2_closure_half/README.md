# GF2 — The closure half: κ = ½ derived as the self-source closure coefficient

**Lane GF2, `deepseek_push`, 2026-10-08. Run: `python3 GF2_closure_half.py` → `GF2 COMPLETE: 15/15`
(exit 0). MUTATE: `GF2_MUTATE=1` → 13/15, L4/L5 fail as declared.**

## The result

The record has always treated `σ² = C/2` (`C = √(GM_ba₀)`) as the anchor **rung 4 import**. It is
not an import. It is the **closure coefficient** of the framework's committed static
configuration, derivable in two exact lines:

```
P1  the sector's static branch is the log potential  Φ = C ln r        [committed, certified]
P2  Poisson (standard):  ∇²Φ = 4πGρ        ⇒  ρ = C/(4πG) r⁻²          [γ = 2 FORCED]
P3  stationarity + barotropy (standard):  σ² ρ′/ρ = −Φ′  ⇒  σ² (−2/r) = −C/r  ⇒  σ² = C/2
------------------------------------------------------------
κ := σ²/v_flat² = (C/2)/C = ½            EXACTLY.   Zero number-imports.
```

- **L1 (exact, 4 sub-checks):** the chain above, sympy residual 0; `σ² = √(GM_ba₀)/2` falls out with
  the committed normalization `C = √(GM_ba₀)` (numeric control: 119.21 km/s vs the registered MW
  119.2 km/s at M_b = 6.5e10; 132.76 km/s vs T13's canonical at 1e11).
- **L2, the uniqueness lemma (new):** among power-law configurations with their own gravity, **γ = 2
  is the unique self-sourced hydrostatic equilibrium.** The closure defect
  `∇²(C ln r) − 4πGA r⁻ᵞ` has r-derivative `−4πGA(2−γ)r^{1−γ}` — vanishes for all r iff γ = 2 —
  and the hydrostatic r-power balance (`−1` vs `1−γ`) matches iff γ = 2. There is no second member
  to select among; nothing empirical is needed to pick it.
- **L3, the premise ledger:** P1 committed-certified (G081 V1 "the phantom is its own source in
  closed form"; G031 isothermal; the G154/G227 Gauss-map flux, **Lean**), P2/P3 textbook,
  `C = √(GM_ba₀)` committed (enters σ²'s *value*, not κ — κ is a₀-free). **Entries carrying the
  number ½: 0.** And a separate audit: **0 of the 5 statistical principles** (virial, max-entropy,
  equipartition, free-energy, z=0-homogeneity) used — the opus_48 "shared equilibrium premise
  family" critique does not apply to this route.

## What this closes

- **T13's registered open item** (its audit, 2026-10-07, line 89): *"the derivation of the SIS state
  from the kernel + hydrostatics"* — supplied: kernel (log branch) → Poisson → SIS state → σ² = v²/2.
  The T-flow's μ-constancy (T3/T10) gives an independent dynamical route to the same state.
- **The spine's entrance E2** (G227 roadmap: `virial_rung4` / `maxentropy_phantom`, the HARD pair):
  the anchor now has a *static* derivation; the virial/max-entropy routes stand as independent
  consistency checks, not necessities.
- **GF1's V4 home (ii)**: the "anchor ⟸ σ² = C/2" circle closes. GF1's web then carries the result:
  `κ = 1/n` ⇒ `n = 2` ⇒ the germ `a₀ = c√(Gρ_Λ)/2` — one statement, now with both faces derived:
  the π's are bookkeeping (GF1) and the 2 is the closure coefficient (GF2).

## Why this is not circular (the referee's first attack)

The premise is P1: the configuration *is* the self-sourced log pair — the framework's committed
static solution (certified in the cited files; the fused-germ lane's own reading). The number ½ is
**nowhere in P1**: the closure maps structure → number. Sensitivity is demonstrated: mutate the
branch to a general exponent and the closure output moves (γ = 2.1 ⇒ κ = 0.476, defect nonzero:
MUTATE run). If the log exactness is ever softened to asymptotia, the closure output degrades
gracefully to `κ = ½` in the deep limit — stated, not hidden.

## Borders (explicit)

1. **P1 acceptance** — cited; not re-certified here.
2. **Stationarity/barotropy** — named standard premises (the weakest available: no ensemble).
3. **The vacuum coupling** (why a₀'s *value* is the vacuum's scale: `a₀ ↔ ρ_Λ` normalization):
   OUT of scope here; committed temperature-ladder machinery (G132/G151/G163), cited, not re-run.
4. **Flag (not adjudicated):** during preparation, a re-derivation of G081's linearized momentum
   equation did not reproduce its `[SELF-CONSISTENT]` mode equation (G081's form omits the standard
   `−δρ∇Φ₀` force term); this lane does not use G081's mode machinery (only V1's closure identity),
   and flags the point for the audit register.

## Files

- `GF2_closure_half.py` — the lane (controls → closure → uniqueness → ledger → honesty; MUTATE env).
- `GF2_closure_half.out` — 15/15, exit 0; `..._run1_ledger_count_bug` — first run (14/15, a ledger
  counter counted its own sentinel row; fix-forward, both preserved, append-only).
- `GF2_closure_half_MUTATE.out`, `GF2_results_MUTATE.json` — declared flips (L4, L5).
- `GF2_results.json`, `GF2_results_run1.json` — structured results.

Registers: a₀ = 9.3619e-11, G = 6.674e-11, M☉ = 1.98892e30; MW σ register 119.2 km/s; T13 formula
control 132.76 km/s (M_b = 1e11). Citations: G081 (closure identity), G031/G086 (isothermal
sector), G227 (Gauss-map flux, Lean), G084 (max-entropy context), T13 + its sibling audit, GF1
(the one-integer web).
