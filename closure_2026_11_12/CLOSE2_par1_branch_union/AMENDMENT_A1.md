# CLOSE-2 AMENDMENT A1 (post hoc): R7's MUTATE rule, for a member lane that declares a row non-decisive

Committed alone. **Post hoc**: written after `wv1_grade.json` was read for the first time in this lane (R2/R7) and
before `close2_grade.py` was written or run. No threshold, branch definition, membership assignment or union rule
changes. Nothing in sections 1, 2, 4, 5 or 6 of `FROZEN_CRITERIA.md` changes.

## What the frozen rule says, and why it is over-strict here

Frozen R7: "gate health of each member-grading lane (known answers, MUTATE, Lean) ... all true, else that branch is
NO VERDICT."

WV1's committed `wv1_grade.json` carries `M4_bites: false` (canonical and alt). WV1's RESULT.md explains why, and it is
by design: M4 is the control for S3(c), and WV1's frozen criteria make S3(c) **reported, not decisive** ("S3(c) is
reported, not decisive (M4 did not bite)"). M4's failure to bite *strengthens* the case against V1 — the smooth law's
own phantom exceeds Psi's density even under the mutation — it does not weaken the decisive failing part, S3(b), which
has its own biting control (M3).

Applying frozen R7 literally would therefore return NO VERDICT for B-Tm-fine on the strength of a control attached to a
row that no lane uses to set a label. That would hide the actual finding instead of exposing it.

## Replacement (A1)

R7 is refined, for a member lane that declares a row non-decisive in its own frozen criteria, to:

- **R7a (decisive arms).** Every MUTATE arm that guards a **decisive** row of that lane bites. If any such arm does not
  bite, the branch is NO VERDICT.
- **R7b (non-decisive arms).** A non-biting arm guarding a row the member lane's own frozen criteria declare
  non-decisive is **disclosed** (name, value, what it controls) and does not by itself force NO VERDICT.
- **R7c (known answers under the amendment reading).** A frozen known answer that a lane replaced under its own
  committed A1 is read in its replaced form (WV1: KA4(ii) FAIL as frozen -> KA4(ii') PASS under A1), exactly as that
  lane reported both.
- **R7d (Lean).** The lane's Lean file compiles and its false twin fails, as recorded.

For B-Tm-fine this means: R7a rests on M3 (bites, S3(b)); R7b discloses M4 (does not bite, guards S3(c), non-decisive);
R7c reads KA4(ii') under WV1's A1 and KA4(ii) FAIL as frozen; R7d reads `compile.txt` / `compile_MUTATE.txt` (exit 0 /
exit 1). The branch verdict is reported under frozen R7 and under A1, as every other item in this lane is.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
