# FINAL-11 RESULT: the Lean certificate of the amount budget — CERTIFIED

**CERTIFIED / CERTIFIED** (one source, one compile; a Lean build has no footing dependence, and the
budget arithmetic it certifies is footing-free in form — the two Sigma columns below carry the two
footings' numbers as checked constants).

| item | value |
|---|---|
| compile | `lake env lean Final11Budget.lean` -> **EXIT = 0** (`Final11Budget.out:9`) |
| errors / warnings | **0 / 0** |
| `sorry` / `sorryAx` in the source | **0 / 0** (the one textual hit for "sorry" is the header comment "ZERO `sorry`, ZERO `admit`, ZERO custom axioms") |
| theorems declared | 33 |
| `#print axioms` reports | 8, **every one `[propext, Classical.choice, Quot.sound]`** — the standard set, no custom axiom |
| numerical cross-check | `verify_FINAL11.py` -> `verify_FINAL11.out`: **ALL PASS, EXIT = 0** (22 checks) |
| sha256 | `88241b19ff8427b0ef555e4bafe6f681835c947dd71a2b9ad9e440a119ab2375` — **identical to the bytes FINAL-13 audited** (`FINAL9to12/Final11Budget.lean`) |

FINAL-13's audit row for these exact bytes: **PASS** (exit 0, 0 errors, 0 warnings, 8/8 axioms
standard). `lane_result.json` in this folder records the same exit code and the same eight axiom lines.

TEST lane, quarantined. No physics claim is made; this is a certificate of the amount-budget
arithmetic. Cold dark energy is a gravitating field component, never a particle. kappa = 1/2 FITTED;
not theory closed. Adopts nothing.

**No new compute.** This file reads `Final11Budget.out`, `verify_FINAL11.out`, `lane_result.json`,
greps the source for `sorry` / `sorryAx`, and hashes the source against FINAL-13's pinned value. No
Lean build or verify run was repeated for this label.

---

## 1. What is certified

The eight theorems, each on `[propext, Classical.choice, Quot.sound]`:

`X_pos_and_quad` (X > 0 and X(1 + X) = x^2), `X_break`, `X_break_full` (the break at X = 5.41 and its
bracket 5.8887 < x_break < 5.8889), `ratio_break` (X(x_b R)/R = 1), `demand_over_budget`,
`share_over_delivered`, `gas_column_canonical`, `gas_column_alternative`.

Twenty-five further declarations (33 declared, 8 reported) carry no `#print axioms` line in this run;
they are reported, not certified.

## 2. The numerical cross-check (`verify_FINAL11.out`, ALL PASS)

| item | check | value |
|---|---|---|
| (1b) | X x (1 + X x) - x^2 = 0 | 0; X(21.45) = 20.9558, X(41.98) = 41.4830, X(60.00) = 59.5021, X(98.32) = 97.8213, all > 0 |
| (2) | X(x_b(5.41)) = 5.41; the break bracket | 541/100; 5.88881143 in (58887/10000, 58889/10000); X(-x_b) - X(x_b) = 0 |
| (3) | X(x_b R)/R = 1 | at R = 1/1000, 1/7, 1, 541/100, 10, 12345/10 — 1 in every case |
| (4) | X/R_b at the four radii | 3.87354 (bracket 3.87–3.88), 7.66783, 10.99854, 18.08157 |
| (5) | X_s/D_low, X_s/D_high | 65.31284 (bracket 65.3–65.4); 42.5 exactly (= 85/2), bracket 42.49–42.51 |
| (6) | Sigma, canonical / alternative | 0.012872974 (bracket 0.012872–0.012874) / 0.015557095 (0.015557–0.015558) |

## 3. What this certificate does not do

- It certifies arithmetic, not physics: no rotation curve, cluster, lensing or CMB row is graded here.
- It does not derive the share or a0; it certifies the relations among them as written.
- 25 of the 33 declared theorems are unreported by `#print axioms` in this run and are therefore not
  covered by the certificate. If the record wants them covered, the fix is a criteria-level edit (add
  the directives and re-run), not new mathematics.

## 4. The sibling copy

`fable52_push/FINAL-11_lean_budget/` holds a **different** file (sha256 `ecdcbb78…`, 17 theorems, 17
axiom lines, all standard, no `EXIT=` line recorded). Its own RESULT.md records NO VERDICT —
INCOMPLETE RECORD. This folder holds the certified bytes.

## 5. Files

`Final11Budget.lean` (sha256 `88241b19…`), `Final11Budget.out` (EXIT = 0, 8 axiom lines),
`verify_FINAL11.py` -> `verify_FINAL11.out` (ALL PASS, EXIT = 0), `lane_result.json`
(`exit_code: 0`, the axiom lines and the ratios table), `build1.out` (empty), and this file.
The audit that pinned the bytes: `hy4_preview_push/FINAL-13_LEAN_AUDIT/AUDIT.md`.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
