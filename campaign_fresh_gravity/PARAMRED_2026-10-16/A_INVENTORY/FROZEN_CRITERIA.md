# PARAMRED lane A (INVENTORY): frozen criteria

Written before PARAM_LEDGER.md. Reading and tabulation only. No script, no computation beyond the hand arithmetic listed in §5.
kappa = 1/2 is FITTED. The two footings are never pooled. Cold energy's mass is an input. Not "theory closed".

## 1. What this lane delivers
PARAM_LEDGER.md: one row per input (headline, hidden, selector-internal, optional-branch, lane-specific knob), with the six
requested columns, a consistency audit (canonical claims vs ledger rows), a ranked list of at most 6 reduction leads, and a count.

## 2. Status vocabulary (fixed now)
- derived: follows from S2/S3/S4 or a committed derivation with no extra number.
- fitted: a number chosen/estimated from data inside the framework (kappa).
- measured: an external measurement the framework takes as input (cosmology, Omega_c/Omega_b, census tables).
- one-sided bound: only an inequality is established.
- postulate: stated structural rule, not derived from the action.
- convention: an O(1) or definitional choice (kernel form, footing denominator, sqrt2 in T_vir).
Scope tags: CANON (in THEORY_CANONICAL_2026-10-14 S1-S5 text), HIDDEN (needed by a canonical claim but not written there),
OPTIONAL (S5, a0(z) branches, carrier microphysics), LANE (set by hand in one lane and scored once).

## 3. Counting rule for "genuinely free continuous constants"
A constant counts iff all hold: (i) a real number not fixed by a measured cosmological input or by a derivation in the record;
(ii) it enters the canonical statement or a sealed prediction, or a scored gate of the canonical theory; (iii) it is not
degenerate with, or a pure re-labelling of, another counted constant (the two footings are ONE constant; T_IGM, mu and the
factor sqrt2 are ONE number V_th). Constants that no sealed prediction depends on are still counted but labelled UNUSED.
"Appears to have" = the number the canonical text itself lists as not derived (its section 3).

## 4. Mismatch rule
A mismatch is listed when a canonical claim cites a CFG row whose LEDGER text or result file says something weaker, different,
later-superseded, withdrawn, post-hoc, or a tension. Each mismatch carries the CFG ids and a confidence tag
(VERIFIED from file / LEDGER text, or UNVERIFIED lead). Nothing is fixed here; the orchestrator decides.

## 5. Controls (this lane)
- C1: every numeric quote below comes from a LEDGER row, a results JSON, a README/criteria file, or is marked "hand".
- C2 (hand arithmetic, reported): a0(kappa 1/2, H0 67.4, Omega_L 0.685) = 9.362e-11 (file value 9.3603e-11, 0.02% apart);
  alt footing 1.1312e-10 reproduced; footing ratio 1/sqrt(0.685) = 1.208 = 0.082 dex; omega_c/omega_b = 0.1200/0.02237 = 5.364.
- C3 (negative control): the T12 +2.03 and the CFG493 pulls are read from the committed results JSONs, not from README prose.
- Trial count: 0 hypotheses tested (no derivation attempted). 14 audit comparisons made (listed in the ledger, section 4).

## 6. Outcome classes for this lane
INVENTORY COMPLETE (every input in canonical + v3 + CFG650 criteria has a row) / INVENTORY INCOMPLETE (named gaps). Mismatches
are findings, not failures. Items not located in the record are marked NOT LOCATED.
