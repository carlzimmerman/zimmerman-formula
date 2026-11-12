# FINAL-10 RESULT: the Lean certificate of the static stress — FAIL (not certified)

**FAIL / FAIL** (the same source is compiled once; there is no footing dependence in a Lean build).
The file does not compile, so there is nothing to certify.

| item | value |
|---|---|
| compile | `lake env lean Final10Stress.lean` -> **EXIT = 1** (`build1.out:368`) |
| errors | **34 error locations** in this folder's `build1.out` (FINAL-13's audit of the same bytes records 20 errors, 7 warnings — the count differs by how continuations are grouped; both are a fail) |
| warnings | 7 (unused `simp` arguments) |
| `#print axioms` report | **none produced.** The file has no `#print axioms` directive — its only mention is the header comment at line 25 ("see the #print axioms report at the bottom") — and the compile exits before any could print |
| theorems declared | 61 |
| `sorry` / `sorryAx` in the source | 0 / 0 |
| sha256 | `ac79188955aef00b97fd820ed3e563dc1c9ef5f55661f764ecf89a0850e6bc9c` — **identical to the bytes FINAL-13 audited** (`FINAL9to12/Final10Stress.lean`) |

FINAL-13's audit row for these exact bytes: **FAIL** (exit 1, 20 errors, 7 warnings, 0 axioms printed).
DOORS.md's entry: "ships 61 theorem declarations but no `#print axioms` report, so there is nothing to
certify yet."

TEST lane, quarantined. No physics claim is made; this is a would-be certificate of the stress
identities. Cold dark energy is a gravitating field component, never a particle. kappa = 1/2 FITTED;
not theory closed. Adopts nothing.

**No new compute.** This file reads `build1.out` and `verify.out` (already in the folder, 2026-11-11),
greps the source for `sorry` / `sorryAx` / `#print axioms`, and hashes the source against FINAL-13's
pinned value. No Lean build was re-run for this label.

---

## 1. What the errors are

The last four, in source order (`build1.out`):

- `522:4` — Type mismatch: `HasDerivAt.differentiableAt (hasDerivAt_isoH x hx0)` has type
  `DifferentiableAt ℝ isoH x`, expected `DifferentiableWithinAt ℝ isoH (interior (Set.Ici 0)) x`.
- `526:31` — `linarith` failed to find a contradiction (`a✝ : x ^ 3 < 0` with `hx0 : 0 < x`): the
  positivity side-condition for the isotropy branch is not discharged.
- `567:6` — `Failed to rewrite using equation theorems for uOf`; `ring` cannot close it (the message
  suggests `ring_nf`).
- `588:52` — unsolved goals: `JF K a0 g * 3 - g^2 * (K + K * uOf a0 g)⁻¹ = JF K a0 g * 3 - g^2 *
  (g * K * a0⁻¹ + K)⁻¹`.

So the file is a genuine work in progress: three of the four are tactic/rewrite failures inside
otherwise well-typed statements, and one is a real `DifferentiableAt` vs `DifferentiableWithinAt`
mismatch. None of them is a physics problem; all of them are proof-engineering. `probe.lean` and
`probe2.lean` in this folder are the scratch files used to locate them.

## 2. What `verify.out` is, and what it does not do

`verify.out` is a **sympy** cross-check of the identities the Lean file is meant to prove, not a Lean
artifact, and it prints no PASS/FAIL/EXIT line. Its content is consistent with the intended theorems:

- the root of `u^2 = x^2 (1 + u)` and the branch residual `u^2 - x^2(1+u) = 0`;
- `R(x) = 2(u - log(1+u)) - x^2` is **positive over the whole grid** (min 3.3308e-04 at x = 0.1,
  max 9.9836e+03 at x = 100);
- the limits `R/x^3 -> 1/3` as x -> 0 and `R/x^2 -> 1` as x -> infinity;
- `Pi_rr/Pi_tt -> -1` as x -> 0 and -> 0 as x -> infinity, with
  `(Pi_rr/Pi_tt) x^2/(2 log x) -> -1`;
- the deep-field form `J = g^2/(2K) - (a0^2/K) u^3/3 + ...` (the deficit is O(u^3) and negative), and
  `R = 2(sinh s - s)` in s = log(1+u).

This is numerical corroboration of the mathematics, and it is worth keeping, but it is not a
certificate: it cannot supply the exit code, the axiom census, or the sorry census the audit grades.

## 3. What it would take to close

Finish the four failing proofs (the `DifferentiableWithinAt` coercion at 522, the positivity argument
at 526, the `uOf` rewrite at 567 and the normal-form goal at 588), add a `#print axioms` directive for
each of the 61 declared theorems, re-run, and capture `EXIT=0` with zero errors. FINAL-13's audit then
re-certifies against the new bytes. No new physics; the mathematics is already corroborated by
`verify.out`.

## 4. Files

`Final10Stress.lean` (sha256 `ac791889…`), `build1.out` (EXIT = 1), `verify.out` (sympy, no verdict
line), `verify_residual.py`, `probe.lean`, `probe2.lean`, and this file. The audit that pinned the
bytes: `hy4_preview_push/FINAL-13_LEAN_AUDIT/AUDIT.md`. The passing sibling of the same campaign:
`hy4_preview_push/FINAL-11_lean_budget/` (EXIT = 0, ALL PASS) and `fable52_push/FINAL-9_lean_static/`
(EXIT = 0).

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
