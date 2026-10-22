# A83 — mutations

Five dials. Each edits one anchor in one module, recompiles the mutated copy with the project's own
`lake env lean`, and must be **killed**: either the compiler rejects it, or a banned token reaches the
mutated source. `python3 a83_checks.py --mutate all` runs all five, records them in
`a83_mutations.json` / `a83_mutations.out`, and exits 0 iff every one is killed.

The distinction matters for `inject_sorry`: Lean *accepts* a `sorry` with a warning and exits 0, so a
checker that only looks at the exit code would pass a file containing a hole. The harness therefore
also scans the mutated source (comments stripped) for `sorry`/`admit`/`native_decide`; that is the
gate that kills it. The same scan runs on the delivered modules (check L3).

| # | dial | file | edit | why it is load-bearing | observed |
|---|---|---|---|---|---|
| 1 | `vacuum_only_beta` | `A83/BlockD.lean` | `beta_of_r`'s conclusion changed from A78's matter-inclusive `β = (2/3)Ω_L(r−1)` to A33's vacuum-only `β = (2/3)(Ω_L r − 1)` | the proof is `linarith` from `2+3β = 2(Ω_L r + Ω_m)`, `Ω_L+Ω_m = 1`; the vacuum-only form does not follow, so this dial tests that the theorem really uses the matter term | **KILLED** — exit 1, `linarith failed to find a contradiction` (BlockD:31) |
| 2 | `inject_sorry` | `A83/BlockA.lean` | the proof of `Kmat_det` replaced by `sorry` | tests the token gate: Lean exits 0 with a warning, but a certificate with a hole must not pass | **KILLED** — Lean exit 0, but `sorry` count 1 → rejected by L3 |
| 3 | `break_alpha_gamma` | `A83/BlockA.lean` | `Gmat`'s second diagonal changed from `γ * p ^ 2` to `γ * p ^ 4` | destroys the single-stiffness matrix: `γ • Gmat 1 1 p` no longer matches, so `Gmat_single_stiffness_iff`'s reverse direction fails; tests that the theorem is tied to the quoted matrix, not to a scalar identity | **KILLED** — exit 1, `unsolved goals` (BlockA:95) |
| 4 | `unreduced_wavelength` | `A83/BlockC.lean` | `a0_full`'s conclusion changed from `… = a0Thermal c H / (2π)` to `… = a0Thermal c H` | drops the 2π from the unreduced branch; tests that the `48π⁴` branch really carries the factor `(2π)²` | **KILLED** — exit 1, `unsolved goals` (BlockC:146) |
| 5 | `drop_Omega_m` | `A83/BlockD.lean` | `beta_of_r`'s hypothesis changed from `2 + 3β = 2(Ω_L r + Ω_m)` to `2 + 3β = 2Ω_L r` | tests that the theorem is not provable from the vacuum-only relation — i.e. that A78's correction is in the statement and used by the proof | **KILLED** — exit 1, `linarith failed to find a contradiction` (BlockD:31) |

Each mutation is a single textual substitution on a copy in `_scratch/mut_<name>/`; the delivered
modules and the project build are untouched by mutation runs.

## In-place confirmation — each mutant makes the verification exit 1

A killed copy could in principle be a copy that differs from the delivered module in some other way.
`--mutate inplace:<name>` closes that gap: it edits the **built module and its lane copy in place**,
runs the full `a83_checks.py`, records the exit status and the failing checks, and restores both files
byte-for-byte in a `finally` block (the restore is hash-asserted). The result is the direct form of
"each mutation forces exit 1":

| dial | verification exit | failing checks |
|---|---|---|
| `vacuum_only_beta` | 1 | L1 (build fails), L2 (audit fails) |
| `inject_sorry` | 1 | L3 (token `sorry`), L5 (`sorryAx` in the axiom set) |
| `break_alpha_gamma` | 1 | L1, L2 |
| `unreduced_wavelength` | 1 | L1, L2 |
| `drop_Omega_m` | 1 | L1, L2 |

`inject_sorry` is the informative one: Lean exits **0** on the mutant, so L1 and L2 pass — the
certificate is rejected by the token scan (L3) and, independently, by the axiom audit (L5), which sees
`sorryAx` where the standard three axioms should be. Recorded in `a83_mutations_inplace.json` /
`a83_mutations_inplace.out`.

Reproduce:

```bash
cd deepseek_push/DS_FINAL_2026_10_21/A83_lean_spine
python3 a83_checks.py --mutate all                 # 5/5 KILLED, exit 0
python3 a83_checks.py --mutate inplace:all         # 5/5 force verification exit 1, then restore
A83_MUTATE=inject_sorry python3 a83_checks.py      # same dial via the environment variable
```
