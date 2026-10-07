# Z19-WAVE_BRIEF — parity-law origin door (door 2 of the Z18 ops note)

**Lane:** PL1 (owns PL1_* files in deepseek_push/). Conductor-run (delegate_task absent,
tool_search 2026-10-07: no matching capability), per Z6–Z18 precedent.

## Context (surviving numbers, file refs)
- LR10B (3dba2f805): rational moment chain c1(q) = 17/60 + (117/350)q + (627/6125)q²
  Lean-certified zero-sorry. E2(q) = 37/60 + (701/1050)q + (3491/18375)q² exact
  (LR10X_results.json, exit 0).
- LR10X G-T3 observed SYNTACTICALLY: log(1+r) appears ONLY at odd r-powers in the
  expanded channel integrands (LR10X_exact_check.py G-T3 block). The ln2-kill follows
  because the ln2 coefficient of ∫₀¹ r^p ln(1+r)dr = [1−(−1)^(p+1)]/(p+1) vanishes at
  odd p. WHY the odd-p structure holds is unexplained — this door's payload.

## Goal (B-class structural lemma candidate, K01 labeling)
Explain the parity law structurally: hypothesis H — every closed moment/J in the S4
block (LR10X_exact_check.py, verbatim) is LINEAR in A := atanh(r), with A-coefficient
an ODD function of r; hence the log-part of each channel integrand is
atanh(r)·(odd polynomial in r), an even-in-r object whose atanh power series is an
even-power series in r with rational coefficients — forcing rational totals, no ln2,
no π², no ζ(3). Mechanism sketch: r = tanh(u) is an odd diffeomorphism and the
estimator's u-integrand is even in u, so even-in-r structure is inherited.
The mechanism leg (u-evenness origin) is attempted but BANKED ONLY IF machine-checked;
else recorded as conjecture with the exact-level results still bankable.

## Pre-registered gates (kill = door dies honestly; fires preserved verbatim)
- G-P0 loaded-not-transcribed: the S4 block is copied VERBATIM from
  LR10X_exact_check.py (byte-identical core lines); any transcription = fire.
- G-P1 parity reproduction: odd-p audit of log(1+r) over ALL terms of channels a/b/c
  reproduces LR10X G-T3 (0 violations).
- G-P2 A-linearity: expanding each channel integrand in the indeterminate A = atanh(r),
  every term has A-degree ≤ 1 (no atanh², no log² anywhere).
- G-P3 oddness: for each channel, the A-coefficient O(r) satisfies O(−r) = −O(r)
  syntactically (sp.expand(O.subs(r,−r) + O) == 0).
- G-P4 consequence cross-check: totals recomputed from the A-linear decomposition are
  syntactic zeros vs (37/60, 701/1050, 3491/18375) from LR10X_results.json.
- G-P5 mechanism (conjecture-grade unless it passes): each individual moment/J is
  A-linear with odd A-coefficient; if any single object carries A-degree ≥ 2, the
  product-level cancellation is recorded as the finding and G-P5 FAILS honestly.
- KILL: any G-P1..G-P4 fire ⇒ PL1 verdict DIED, register row appended verbatim, no
  tuning of the math. Instrument/script bugs may be fixed forward with the fire
  preserved verbatim in PL1_stdout_0.txt (Z15–Z18 run-history discipline).

## Deliverables
PL1_parity.py / PL1_parity.out / PL1_parity_results.json / PL1_stdout_0.txt;
register row appended by the conductor; commit work+math only (no raw data).
