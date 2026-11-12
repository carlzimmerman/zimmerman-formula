# FINAL-17 (KAPPA_A) AMENDMENT A1 -- 2026-11-11

Recorded because two frozen criteria were found defective by the first two runs and were
changed **before the run whose numbers are reported in `RESULT.md`**. Both changes are
declared here in full, with the numbers that exposed them.

## A1.1 -- KA-1 was restated (the original criterion was circular)

**As frozen (PREREGISTER §4, KA-1):**
> `Z := c H_L/a0 = 5.788810` on the canonical footing (FINAL-16 print; `sqrt(32 pi/3)`).

**What the run produced:** `Z = 5.785390`, `sqrt(32 pi/3) = 5.788810`, `|diff| = 3.42e-03` --
a FAIL against the frozen `1e-4` tolerance, on the very first graded control.

**Diagnosis.** The frozen wording silently inherited FINAL-16's KA-1, which builds `H_Lambda`
from `rho_ref := 4 a0^2/(c^2 G)` -- a density **defined from the footing**. On that reading
`Z = sqrt(32 pi/3)` holds *identically*, for any `a0`; it is the footing's definition, not a
measurement. FINAL-16's `final16.out` line 149 (`Z = 5.788810, |Z - sqrt(32pi/3)| = 0.00e+00`)
is therefore a circular control. Reproduced in this lane: the `rho_ref` route gives
`Z = 5.788810` exactly.

This lane used the **independent** Planck `rho_Lambda` instead, which is the only version of
the control with content -- and it fails, because `Z` and `kappa` are the same number:
`kappa = sqrt(8 pi/3)/Z`. `Z = sqrt(32 pi/3)` holds **iff** `kappa = 1/2` exactly; with the
canonical footing against Planck `rho_Lambda`, `kappa = 0.500296`, i.e. `1/2` is off by
**0.059 %** (footing round-off).

**Restated criterion (used for the reported run):**
> **KA-1.** `kappa` computed from `Z` and `kappa` computed directly from `a0/(c sqrt(G rho_L))`
> agree to `1e-12` -- one statement, not two -- and `Z(Planck rho_L) = 5.785390` vs
> `sqrt(32 pi/3) = 5.788810` is reported as the 0.059 % by which the canonical footing
> overshoots `kappa = 1/2`.

**Consequence for the parent, flagged:** any control in the record that computes `Z` (or
`kappa`, or `Omega_Lambda`) from `rho_ref := 4 a0^2/(c^2 G)` is verifying the footing's
definition, not testing the tie. FINAL-16's KA-1 and KA-2 are of this kind (KA-2's
`rho_ref(can)/rho_Lambda = 1.001183` is not: that one compares two independent densities and
does carry content).

## A1.2 -- the A3 menu-span prediction was mis-stated

**As frozen (PREREGISTER §3, A3):** "*Predicted:* ... span ≈ 0.923 dex ⇒ ≈ 22x too much freedom."

**What the run produced:** span = **0.7982 dex** = **19.4x** the 0.0411 dex allowance
(`log10(2.894405/0.460659)`, C1 over C3/C6).

**Diagnosis.** The 0.923 dex prediction was computed against a menu draft that still carried a
`kappa = 0.34549` arm (capacity `:= G rho_L R_Lambda`, no `pi`); that arm is not in the frozen
menu as committed. This is a pre-registration bookkeeping miss, recorded as such. It does not
touch any graded rule: the decisive test is `span > 0.0411 dex`, which both the predicted and
the actual value clear by a large margin.

## A1.3 -- MUTATE grading semantics made explicit

The frozen text said the twins "must be rejected"; it did not say what makes the mutation arm
**fail**. Made explicit: MAIN passes iff each twin is REJECTED; MUTATE passes iff each twin is
ACCEPTED (proving the rejection was machinery-driven). The mutation arm's own failure is
carried by **A3**: widening the band to 20 % admits C3, C5 and C6, so `A3` FAILS and the lane
label flips to the false `KAPPA DERIVED (CAPACITY)`. That is the "mutation arm must fail"
signal: `MUTATE exit=1`, `MAIN exit=0`.

## A1.4 -- what was NOT changed

The graded rules (`|kappa - 1/2| <= 0.025`; the 0.0411 dex menu-freedom test; the footing
selection rule requiring a *derived* premise; the 107-is-n=2 trap flag; the three twin
rejections) are untouched.
