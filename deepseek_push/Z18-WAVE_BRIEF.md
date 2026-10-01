# Z18-WAVE_BRIEF — LR10B: Lean certificate of the LR10X-corrected rational closed forms

Conductor tick 2026-10-01 (cron, same tick as Z17's landing; LR10-lean was
re-registered RATIONAL-class by Z17). Committed BEFORE any run (house rule 5).
Conductor-run (delegate_task absent; 0 deepseek lanes at spawn).

## Context
- LR10X (Z17, exit 0, 1fa6ff161) adjudicated EXACTLY: a = 37/60 (syntactic zero),
  b = 701/1050, c = 3491/18375 — all pure rational; per-term integrals verified
  vs independent mpmath quad (rel <= 3.9e-30, 30 terms); odd-p parity audit passed.
- E2(q) = 37/60 + (701/1050) q + (3491/18375) q^2; c1(q) = 17/60 + (117/350) q + (627/6125) q^2.
- Door: certify the rationals in Lean, zero-sorry. Payload = the 30 per-term
  integral certificates + channel assembly + c1 coefficients, over 8 single-log
  core integrals int_0^1 u^p log(1+-u) du (p in the term data's support), each via
  the normalized antiderivative ((u^{p+1}-1)/(p+1)) * log(1+-u) - B(u) and mathlib's
  integral_eq_sub_of_hasDerivAt_of_tendsto (the SAME technique as mathlib's own
  integral_log_from_zero_of_pos), with tendsto_log_mul_rpow_nhdsGT_zero supplying
  the (u^{k+1}-1) log(1-u) -> 0 endpoint limit for the log(1-u) cores.

## Gates (frozen BEFORE any run)
- G-L0 (generator, Python): every one of the 30 terms from LR10X_results.json
  (exit 0, loaded-not-transcribed) classified as poly / log(1-u) / log(1+u) with
  rational coefficient and integer power (kill: any unclassifiable term); core
  values derived from the data must be CONSISTENT across all terms sharing a core
  (kill: inconsistency); each core's antiderivative endpoint value B(1) must equal
  the data-derived core value (kill: mismatch) — sympy cross-check.
- G-L1 (Lean): `lake env lean LR10_rat.lean` rc 0; ZERO sorry (tactic-level grep
  = 0, docstring mentions excluded — the Z7 LR4b checker trap); `#print axioms`
  on the three channel laws shows axioms subset of {propext, Classical.choice,
  Quot.sound}.
- G-L2 (independent numeric): spot re-check of every emitted core value against
  mpmath quad at dps 40 (rel <= 1e-30) inside the generator — the Lean file's
  constants must match the LR10X-verified numerics (kill: any mismatch).
- Honest scope (K01 labeling): the geometric reduction chain (moments/J-table,
  exponential coordinates) remains numerically audited (E2F1 G1/G2b, LR10X G-T1)
  and is NOT probability-space-certified — same mechanism class as LR7/LR8/LR9.
  What is certified HERE: the per-term rational integrals, the channel sums,
  and the c1 coefficient assembly, unconditionally, zero-sorry.
- Kill conditions: any G-L0/G-L2 mismatch -> exit 1 before Lean; Lean rc != 0 or
  sorry or axiom overflow -> exit 1 (fires preserved verbatim in LR10B run logs;
  math never tuned).
