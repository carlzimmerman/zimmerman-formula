# A19 — mutations

Three mutations, selected so that each destroys a *different* load-bearing input of the
argument. Each is run as `python3 a19_checks.py --mutate=<id>`; the mutated stdout is in
`a19_MUTATE_<id>.out` and the mutated results in `a19_results_<id>.json`. All three exit 1.

| id | what it corrupts | which check must fire | observed |
|---|---|---|---|
| M1 | the Einstein denominator: `8π → 4π` in `ρ_DE = Λc⁴/(8πG)` | K2 (the number 4) | `R = 7.99004`, `κ = 0.353774` → 16/17 |
| M2 | the cell topology: `χ = 1 → 2` (4-ball → S⁴) | K2 (via `L/ℓ_E`) | `L/ℓ_E = 1.41333` (was 1.99876) → 16/17 |
| M3 | the channel count: count off-shell components as physical | K7 | "honest max 3" becomes 4 → 16/17 |

## M1 — drop a factor 2 from Einstein's 8π

    $ python3 a19_checks.py --mutate=M1
    K2   FAIL R = 7.99004, kappa = 0.353774, n = 2.82667     |R-4| < 0.01  [L/ell_E = 1.99876]
    A19 COMPLETE: 16/17 checks PASS.

`R` doubles exactly, as it must: `R ∝ 1/(8π)`. This is the mutation that matters most in this
subject — the BRIEF §1 warns that any "derivation" of κ must not smuggle the 8π/3 bookkeeping.
An argument that loses one factor of 2 in `ρ_DE` returns κ = 1/√8 = 0.3536 instead of ½, and the
check has no tolerance for it (threshold 0.01 on `R`). Note K1 still passes: K1 is the symbolic
identity, deliberately written with an explicit `8π` so that it certifies the *algebra* rather
than the constant choice — which is why the constant choice needs its own check.

## M2 — swap the cell topology

    $ python3 a19_checks.py --mutate=M2
    K2   FAIL R = 3.99502, kappa = 0.500311, n = 1.99876     |R-4| < 0.01  [L/ell_E = 1.41333]
    A19 COMPLETE: 16/17 checks PASS.

With χ = 2 the Euler balance puts the cell radius at √(16π/Λ) instead of √(8π/Λ), so `L/ℓ_χ`
falls from 2 to √2 — the consistent κ would then be 1/(2√2) = 0.3536. The check fires on
`L/ℓ_E`, i.e. on the geometric input, not on `R` itself — which is the point: this lane's claim
is that the *two* inputs (β, χ) are what κ is made of, and mutating either one moves the answer.

## M3 — count ghosts as physical

    $ python3 a19_checks.py --mutate=M3
    K7   FAIL massless 2, massive 3, off-shell 4 (honest max 3) no honest count == 4  [off-shell 4 = 3 physical + 1 constraint]
    A19 COMPLETE: 16/17 checks PASS.

The mutation returns the off-shell component count (D = 4) as if it were a physical count, which
is precisely the error that would let candidate (ii) "derive" 4. K7's threshold is a set
membership — 4 must not be in the honest set — so the mutation cannot slip through.

## What is *not* mutated, and why

The theorem-shaped claims (K13, K16) are not tied to a constant or a topology; they are
statements about the *form* of the answer (κ = ℓ₁/L; dof = 0 ⇒ R ≠ 4). A mutation that broke them
would have to change the algebra of the ledger, and K1/K16 already pin that algebra symbolically
against the definitions of ρ_DE, a₀ and ℓ₁. The three mutations above therefore cover the three
places where a number enters by hand.
