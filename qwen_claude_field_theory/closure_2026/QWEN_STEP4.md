# QWEN: run step 4. One idea, one script, then stop.

You are a local worker. **Fresh context, one job, then stop.** This file is your whole brief —
you do not need to read the rest of the repo to start, though the files named below are worth
opening.

**Time box: 40 minutes.** If you are not producing a number by then, write what you have, grade
it `NOT COMPUTED`, say exactly what blocked you, and stop. **A stalled session is the only real
failure mode.** Partial results with a clear statement of the wall you hit are worth far more
than nothing.

---

## The one job

Compute the **secondary constraint** for the interaction below, and determine whether it exists
and propagates. Write it to
`qwen_claude_field_theory/closure_2026/sf14_secondary_constraint_2026.py`.

Everything the calculation needs is already fixed. **You are not choosing anything.**

---

## What is already settled (do NOT re-derive, do NOT re-choose)

| quantity | value | from |
|---|---|---|
| the projected relative connection | `C_M^i_jk = (³Γ^i_jk − ³Γ̂^i_jk) − K̂_jk u^i` | `sf13a` |
| the shift redefinition | `u^i = (N^i − N̂^i)/N̂`, invertible for N̂ > 0 | `sf13a` |
| the contraction | **the MIXED one**, `C_M^i_jk C_M^j_ik = −\|∇ψ\|²`, so **c = −1** | `sf13b`, `sf13d` |
| the scalar | `X = c\|∇ψ\|²/a₀²(𝒬)` with c = −1 | `sf13b` |
| the interaction | `V = m²M_eff² · N√h [F(X) + (N̂/N)B(X)]` | `sf13c` |
| the physical function | `A(x) = α̂F′ = (√(4x²+1) − 2x − 1)/(2rx + 2x − √(4x²+1) + 1)` | `sf13e` |
| the only parameter | `r = M_f²/M_g²` | `sf13c` |
| the EH normalisation | k = −2, M² = 1/(8πG), **calibrated against ∇²Φ = 4πGρ** | `sf13d` |
| a₀ | 9.3619e-11 canonical / 1.1279e-10 alt. **Report both.** | framework |

`κ = ½` is **FITTED**, measured 0.529 ± 0.034. **Never write that it is derived.**

## What is already known about the lapses

- `X` is **lapse-free** after the redefinition (`sf13a` B2, verified: ∂X/∂N = ∂X/∂N̂ = 0).
- Therefore the interaction's own lapse Hessian is **identically zero — all four entries**
  (`sf13a` C1). The **primary** constraint exists.
- **That is where the knowledge stops.** Your job is the *secondary* constraint.

---

## The calculation, concretely

1. Write the total Hamiltonian in ADM variables: `h_ij, π^ij, ĥ_ij, π̂^ij`, lapses `N, N̂`,
   and the redefined shifts `u^i, N̂^i`.
2. The primary constraint is the coefficient of `N` in `H`. Call it `C`.
3. Compute `{C, H}` — the secondary constraint. **The part that matters:** `X` contains
   `³Γ^i_jk − ³Γ̂^i_jk`, i.e. **spatial derivatives of the metrics**. Integration by parts in the
   bracket will therefore generate `∇_i N` and `∇_i N̂` terms. **Carry them. Do not drop them.**
   Whether they cancel, or survive and constrain, is the entire question.
4. Then compute `{C, C}` and `{C, H_i}` (the momentum constraint) and report whether the pair is
   second class.

**Use sympy.** For step 3 you may work at a simplified but non-trivial configuration (e.g.
conformally perturbed spatial metrics, one spatial dimension for the derivative structure) — say
explicitly which configuration you used and that the result is representative, not general.

---

## What counts as which verdict — declared in advance

- **PASS** — a secondary constraint exists and propagates. The ghost degree of freedom is
  removed. That would close the last structural gate on this architecture.
- **KILL** — no secondary constraint, or it fails to propagate. **A kill is a publishable
  result.** Say which bracket failed and why.
- **PARTIAL** — you computed the bracket but cannot decide propagation. Report the bracket.
- **NOT COMPUTED** — you hit a wall. Say which one.

---

## The rules that have actually cost us on this exact problem

Read `RETRACTIONS.md` at the repo root before you start. Six errors are logged there from three
days. These four are the ones that bit *this* calculation:

1. **A partial-derivative zero is not a Hessian degeneracy.** Made twice. `∂²L/∂N² = 0` with a
   surviving mixed entry gives `det H = −(mixed)² ≠ 0`. **Check the full matrix.**
2. **A coefficient asserted is a coefficient wrong.** The α sign was asserted twice and reversed
   twice. **Calibrate every sign against a control** — for gravity, the Newtonian limit.
3. **Matching limits is not matching a function.** A wrong interpolation function passed both its
   deep-MOND and Newtonian limit checks and was still wrong.
4. **Verify a "fails" claim as rigorously as a "works" claim.** Roughly half the logged errors
   are manufactured deficits and half are manufactured wins. Both are equally penalised. After
   removing a false kill, **re-run the other sectors before declaring survival.**

Plus the standing repo rules:

5. Every load-bearing claim needs numbered `[ok]`/`[FAIL]` checks and a non-zero exit on failure.
   **No script, no claim.**
6. Never write "no dark matter" — the slogan is **"no dark-matter PARTICLE."** Ω_dm is full here
   as a field's conserved shift charge.
7. Never write that the theory is closed.
8. **Scope fence: write only inside `qwen_claude_field_theory/closure_2026/`.** Read anything.
   Append to the top-level `RETRACTIONS.md` only if you withdraw a claim.
9. Never invent an equation number, a citation, or a DOI. Mark anything you did not verify
   `UNVERIFIED`.

---

## When you finish

Append **exactly one row** to `closure_2026/LEDGER.md` (create it if absent):

```
| SF14 | secondary constraint bracket | <the decisive number or expression> | PASS / KILL / PARTIAL / NOT COMPUTED |
```

Then write a result section at the top of your script's docstring saying, in plain terms, what
happened — **including a paragraph arguing against your own conclusion.** That paragraph is
mandatory. Then stop.
