# Z17-WAVE_BRIEF — LR10 stage-1: zero-recognition exact confirmation of the E2F1 closed forms

Conductor tick 2026-10-01 (cron), conductor-run (delegate_task absent per tool_search
2026-10-01; 0 deepseek lanes running at spawn — only the separate agent harness PID
95861 and hermes gateway processes, untouched per house rule 8). Committed BEFORE any
run per house rule 5 / Z6-Z16 precedent.

## Context (surviving numbers, file refs)
- E2F1 (Z16, commit 167f11fab, exit 0) banked the exact closed forms of the E2(q)
  coefficients: a = 37/60; b = (217 - 489 ln2 - 8 pi^2 + 251 zeta(3))/151;
  c = (17 + 47 pi^2 - 423 ln2 - 137 zeta(3))/121
  (deepseek_push/E2F1_results.json -> symbolic, status CLOSED).
- HONEST GAP: E2F1's S5 leg (E2F1_closed_form.py, `rint`) obtained these forms by
  `sp.nsimplify(tot, [log 2, pi^2, zeta(3)], tolerance=1e-11)` — LATTICE
  RECOGNITION from a symbolic-exact `tot`, never a symbolic zero test. The register
  ops note records the recognition delicacy: b's exact form sits 3.6e-13 from the
  WRONG rational 701/1050; only the derived basis + cross-gates (G3/G4/G5) separate
  them. Recognition at 1e-11 is evidence, not exactness.
- LR10 door (Z16 ops note): Lean certificate of the closed forms; "own algebra audit
  first". THIS brief registers the audit stage (LR10X); the Lean stage (LR10-lean,
  basis integrals with Li3(1/2)-class lemmas) stays OPEN and is NOT attempted here.

## Goal
Lane LR10X (files LR10X_exact_check.py/.out/.json, LR10X_stdout_*.txt):
re-derive the symbolic-exact `tot` for each channel (a, b, c) via the E2F1 S4/S5
exponential-coordinate chain (12 inner moments + 4 J-table entries closed
symbolically, then term-wise r-integration in the log basis — code path reproduced
verbatim from the committed E2F1_closed_form.py, no math edits), then test the
closed forms (loaded-not-transcribed from E2F1_results.json `symbolic`) against
`tot` EXACTLY — zero recognition, zero tolerance, no lattice.

## Pre-registered gates (BEFORE any run)
- G-X1 (primary, per channel): d = tot - closed_form; EXACT syntactic zero after
  sp.cancel(sp.expand(sp.simplify(d))) == 0.
  Branch (i): syntactic 0 reached -> channel BANKED-EXACT.
  Branch (ii): syntactic leg open within the 240 s/channel time-box but
  d.equals(0) is True (sympy symbolic zero-test, independent numeric-sampling
  machinery) -> channel BANKED-ZEROTEST, syntactic leg recorded OPEN (never silent).
- G-X2 (per channel): mpmath dps=50 evaluation of the closed form (atoms mp.log 2,
  mp.pi**2, mp.zeta(3)) vs mpmath dps=50 evaluation of the exact `tot` —
  rel dev <= 1e-30.
- G-X3 (loaded-not-transcribed): vs E2F1_results.json g3 num (the independent
  numeric pipeline): |N(tot,50) - num|/|num| <= 1e-12.
- KILL CONDITIONS (exit 1, no exceptions): any G-X2/G-X3 fire; tot - form
  nonzero under BOTH syntactic simplify AND .equals; time-box exhaustion on ALL
  branches of a channel; any uncaught exception. A fired gate is preserved
  verbatim; math is never tuned to a gate.
- Honest statuses only: BANKED-EXACT / BANKED-ZEROTEST / OPEN — nothing in
  between. K01 labeling: this lane certifies EXACTNESS of already-measured forms
  (algebra-of-the-derivation audit); the physics payload remains E2F1's.

## House rules 1-10 apply verbatim (LOOP_CONDUCTOR.md). No git commits by the
lane; conductor commits work+math only (LR10X_* + Z17-WAVE_BRIEF.md + register
row). Raw data untouched; astra_spawn_ideas + _g208 probes untouched (rule 8).

## AMENDMENT 1 (pre-run, before LR10X run-1)
E2F1's `rint` used a term cache keyed on srepr[:120] — a runtime optimization with
a real collision risk (two distinct terms sharing a 120-char srepr prefix would
collapse). LR10X reproduces the S4/S5 chain VERBATIM except: the term cache is
DROPPED (straight Add over all terms) — tooling only, no math change; if the cache
did collapse terms in E2F1's tot, the G-X1/G-X2/G-X3 gates will fire and that is
E2F1 tooling verdict, recorded honestly.

## AMENDMENT 2 (pre-run-2, after LR10X run-1 fire)
Run-1 fired honestly: uncaught KeyError 'g3' — E2F1's G3 numeric pipeline values
were never saved to E2F1_results.json (log lines only); fire verbatim in
LR10X_stdout_0.txt. Fix forward (gate VALUES unchanged): G-X3 now = G-X3a (fresh
verbatim re-run of the E2F1 S1 numeric pipeline, GL(90,70,70) + GL(140,110,110)
rule-doubling gate 1e-11, vs N(tot,50) at <= 1e-12) + G-X3b (numeric values parsed
from the G3 lines of E2F1_results.json's own log — loaded-not-transcribed, 12-digit
precision on disk — vs tot at <= 2e-12, the parse-precision floor).
