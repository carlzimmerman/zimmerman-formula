# E03 — A linter for the corpus's own rules
COST: S | script: `TOOLS/lint_corpus.py`

> ENGINEERING / DATA task. Import `TOOLS/mi_constants.py` — never retype a constant.
> `../02_HOUSE_RULES.md` and `../03_NUMERIC_HAZARDS.md` apply.

## The task
The house rules are enforced by memory right now. Make them mechanical.

## Do
Write a linter that scans `real_research/reviews/*.py` and flags:
1. **Tautological checks** — `check(True`, `== a`, `x or True`, `A and (B or True)`, and any `check(` whose
   condition contains no comparison operator at all. (Two real ones were caught by hand here.)
2. **Banned phrasings** from `../07_WRITING_RULES.md`: "derived" near kappa/a_0, "zero free parameters",
   "proves", "theory is closed", "definitively".
3. **Missing credit**: any file using `sqrt(1+1/y)` or the dS-Unruh balance without citing Milgrom 1999.
4. **Retyped constants**: numeric literals matching known constants (9.3614e-11, 5.7888, 5.4194e-10, …) that
   should be imports from `TOOLS/mi_constants.py`.
5. **Single-footing results**: a file quoting a dimensional a₀-dependent number without mentioning ALT.
Report per-file counts and exit non-zero if anything in category 1 or 2 is found.

## Settles if
It runs over the whole corpus, and the categories it flags are real (spot-check ten by hand before trusting
it). False positives are fine if reported as warnings; a false *negative* in category 1 is the failure mode.
