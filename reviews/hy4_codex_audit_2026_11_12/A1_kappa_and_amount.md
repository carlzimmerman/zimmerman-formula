# A1 audit: is kappa or 5.41 derived? (HY4 preview lanes, 2026-11-11/12)

Independent auditor, 2026-11-12. Graded the COMMITTED bytes (HEAD 2207a1df48 lineage). Several
lane files (FRAMEWORK.md, FINAL-17, OUT-2 RESULT, OUT-3 criteria) carry UNCOMMITTED scope
corrections by another session; they were not graded, but where they agree with this audit it says so.
Method: commit order from `git log`; every lane script re-run from a sibling copy at the same depth
(one thread, `nice -n 19`, all under one minute), outputs diffed against the committed ones, copies
deleted; every lane Lean file built with `lake env lean`; decisive steps re-derived in sympy.

## Table

| lane | label claimed | order ok? | re-run reproduces? | grade | one-line reason |
|---|---|---|---|---|---|
| FINAL-9 (Lean static, `fable52_push/FINAL-9_lean_static`) | certified PASS | n/a (no criteria) | Lean exit 0, 18/18 standard axioms | SOUND WITH LIMITS | algebra of the law and its static branch only; nothing about kappa or 5.41 |
| FINAL-10 lean_stress | FAIL (not certified) | n/a | yes: exit 1, 34 error lines, no axiom report | SOUND | the label is the build's own failure |
| FINAL-11 lean_budget | CERTIFIED | n/a | yes: exit 0, 8 standard axiom lines; verify script output identical | SOUND WITH LIMITS | arithmetic only; 25 of 33 theorems have no axiom report; 5.41 is an INPUT (`R_b = 541/100`), `X(x_b R) = R` is the definition of x_b inverted |
| FINAL-12 (Lean background) | FAIL, sorryAx disclosed | n/a | yes: exit 1, 2 errors, 6 sorryAx | SOUND | label matches the build; the audited bytes (sha 670524a1) are untracked; the tracked copy in `closure_2026_11_11/FINAL-12_lean_background` is different bytes (c3cbaaed) |
| FINAL-13 LEAN_AUDIT | 2 PASS / 2 FAIL | n/a | yes: my builds give the same four rows | SOUND WITH LIMITS | the `FINAL9to12/` copies and the `lakefile.toml` target it says it registered are uncommitted; home paths in `audit_lean.py`, `delta.py` |
| FINAL-14 lean_amount | all six items certified | n/a | yes: exit 0, 33/33 standard, 0 sorry | SOUND WITH LIMITS | arithmetic on given constants (5.41 is input); RESULT.md text has `X(21.45)/R_b = 3.87338` (true 3.87354, bracket holds); home paths in RESULT.md and json |
| FINAL-16 KAPPA_REAL | NOT DERIVED, FORM OUTPUT | NO: PREREGISTER, script, outputs, Lean all first appear in one commit f639380e36 although the file says "committed alone" | yes: `final16.out`, `final16_MUTATE.out` byte-identical; Lean exit 0, my axiom probe 4/4 standard | OVERSTATED | the NOT DERIVED verdict stands; but J1 "exact symmetry, kappa the only charged quantity" is not a symmetry of the physical problem (see FRAMEWORK row), and the order claim is false |
| FINAL-17 KAPPA_A | NOT DERIVED; CAPACITY DERIVED | NO: PREREGISTER committed with script and outputs (0fd7e87a46); AMENDMENT_A1 (KA-1 restated, A3 prediction corrected) committed 24 min AFTER the outputs (a12e36e397) | yes: main and MUTATE stdout and json byte-identical (exit 0 / 1); Lean exit 0, 13 standard | OVERSTATED | "capacity DERIVED" is one line of algebra of the law, `g - g^2/(g+a0) = a0 g/(g+a0) < a0` (sympy); A4 "no-go" invalid (needs g_N -> lam g_N at fixed baryons); kappa verdict NOT DERIVED stands |
| FINAL-18 KAPPA_B (fold matching) | NOT DERIVED, fold condition fails 1.2-2.2 dex | yes: PREREGISTER alone 4144abfc80 | `final18.py` main and `--mutate` outputs byte-identical (read the committed `runs/`; the fold runs themselves NOT regenerated); Lean exit 0, probe 10/10 standard; twin exit 1 | SOUND WITH LIMITS | verdict follows from the outputs; upstream fold runs taken as given |
| FINAL-19 KAPPA_C (deep-field column) | NOT DERIVED; saturation forces kappa = sqrt(2 pi) | yes: FROZEN_CRITERIA alone 0eb6a338d5 | yes: main + M1-M4, `.out` and `.json` byte-identical; Lean (symlink to `lean_2026/Fin19KappaColumn.lean`) exit 0, 13 standard | SOUND WITH LIMITS | CONFIRMED `R = sqrt(2 pi f)/kappa`, so R = 1 gives sqrt(2 pi) = 2.5066, 22.1 sigma from 0.4172 +- 0.0946; rests on the pre-registered f = 1 ceiling |
| FINAL-20 kappa_audit | FINAL-16 CLEAN / HOLDS | n/a (audit) | not re-run (compile logs only) | OVERSTATED | repeats FINAL-16's "committed alone" without checking git (false) and endorses the flat-direction argument; written before FINAL-17/18/19 existed; home paths in AUDIT.md, run_compiles.sh |
| OUT-2 KAPPA_RATELOCK | "kappa is an OUTPUT"; commit subject "derived kappa^2 = 2/(3 pi)" | NO: PREREGISTER bundled with script, outputs and Lean in 41307730e1 (a commit titled OUT-3), despite "committed alone" | yes: `out2.out` identical; `out2_MUTATE.py` writes an EMPTY `out2_MUTATE.out` (the committed file was stdout; stdout identical); Lean exit 0, 12 standard; MUTATE twin exit 1, 7 errors | WRONG | see section 2: the postulate is the answer; the 1:1 / H_Lam / 2 pi choice was post-selected from CFG493's pull table (self-disclosed) |
| OUT-3 kappa_equality_fixed | (no RESULT.md) out3.out: K in [3/2, 3], 1/2 not reachable | NO: criteria say the sympy leg ran first; all in 41307730e1 | yes: stdout and json byte-identical | SOUND WITH LIMITS | CONFIRMED `K(x) = 3(x+2)/(2(x+1))` by my own sympy, so the candidate is refuted; no RESULT.md; the promised `OUT3_equality_fixed.lean` and twin do not exist |
| OUT-3 cosmic_share_fold | AMOUNT NOT DERIVED (UNAVAILABLE) | NO: PREREGISTER, script, outputs, RESULT in one commit | yes: `out3csf.out` byte-identical (reads FLD1 runs, not regenerated) | SOUND WITH LIMITS | Part A's reading of R541 is accurate: 5.41 is a CMB best fit and an integration constant; the fold construction misses by 18.5 band-widths |
| OUT-4 KAPPA WINDOW | NOT DERIVED; T* is an equivalence; window 0.378 dex contains 1/2 | yes: FROZEN_CRITERIA alone 57ffe5586a | yes: `out4.out`, `out4_MUTATE.out` byte-identical (exit 0 / 1); Lean exit 0, 0 sorry, no axiom report in file; twin exit 1 | SOUND | CONFIRMED: T* `a0 = c^2/(2 lambda)`, `lambda = c/sqrt(G rho)` is literally kappa = 1/2; `lambda/R_dS = sqrt(8 pi/3) = 2.894` |
| FRAMEWORK.md section 2-4 | G_lambda exact symmetry; kappa a flat direction; kappa = 1/2 "forced" as a convention | n/a | n/a | WRONG | see section 3 |

## 1. Lean: what the certified theorems actually assert

- OUT-2 `kappaSq_from_lock`: IF `H^2 = (8 pi/3) G rho` AND `a0^2 = c^2 H^2/(4 pi^2)` THEN
  `a0^2/(c^2 G rho) = 2/(3 pi)`. The lock is a hypothesis; the theorem is substitution.
- OUT-2 `lock_charged_under_Glambda`: IF `a0^2 = K` and `(lam a0)^2 = K` and `a0 != 0` THEN
  `lam^2 = 1`. True of ANY equation that fixes a0 to a constant, including `kappa = 1/2` itself.
- FINAL-19 `saturation_forces_kappa`: given the two column relations and `Sigma_vac = Sigma_c`,
  `kappa^2 = 2 pi f`. `identity_iff_kappa_half`: the record identity `a0^2/(8 pi G) = rho c^2/(32 pi)`
  holds iff `kappa^2 = 1/4` (so that identity is a restatement, not a derivation).
- FINAL-17: `phantom_capacity` (0 < a0 g/(g+a0) < a0) and covariance identities of the law under
  joint rescaling of a0 and g; algebra, no physics selection.
- FINAL-11/14: `X(x_b R) = R`, numeric brackets with 5.41 supplied as a constant. None derives 5.41.
- OUT-4: T* is equivalent to kappa = 1/2 (13 theorems). No custom axioms anywhere; sorryAx only in
  FINAL-12 (exit 1).

## 2. The OUT-2 tension, resolved

OUT-3, OUT-4 and FINAL-16 to FINAL-20 are right; OUT-2's commit subject is wrong.
(a) The four-line "derivation" is: postulate `a0 = c H_Lam/(2 pi)`, then substitute Einstein's
`H_Lam^2 = (8 pi/3) G rho_Lam`. With kappa defined by `a0 = kappa c sqrt(G rho_Lam)`, the postulate is
algebraically identical to `kappa^2 = 2/(3 pi)` (my sympy residual: exactly 0). Postulating the lock
IS postulating kappa = 0.4607; nothing is derived, the coefficient is moved into a new axiom.
(b) The lane says so itself (PREREGISTER section 2: "postulated here"; D3), but the commit subject,
the RESULT title and "kappa is no longer a fit at all" drop that qualifier.
(c) The value was chosen from three discrete options after CFG493's table showed `c H_Lam/2 pi` had
the smallest pull (D2), and the lock target H_Lam vs H_0 is not selected by the mechanism (D5, 1.27 sigma).
(d) Gate G2 ("capacity fix") cannot fail for any constant-fixing postulate, so it shows nothing.
(e) Numbers are right: 0.460659, 7.87 % below 1/2, offset 0.0356 dex, pull +0.44 sigma (dex).
Unstated in the headline: one imported postulate (KMS-period lock), one winding choice, one target
choice. The uncommitted SCOPE CORRECTION in the working tree says the same.

## 3. FRAMEWORK.md's G_lambda statement

`G_lam: (a0, g) -> (lam a0, lam g)` leaves `g_N = g^2/(g+a0)` covariant only if `g_N -> lam g_N`.
At fixed baryons `g_N = G M_b/r^2` cannot scale. At fixed M_b and r, `dg/da0 != 0` (sympy; deep field
`v^4 = G M_b a0`), so a0, hence kappa, is observable; that is exactly how it is fitted. "Flat
direction", "gauge choice" and "kappa = 1/2 forced as a convention" are therefore wrong. What is true:
the law has one acceleration scale and no internal equation of the adopted action fixes its
coefficient. Measured values also disagree with a convention: kappa = 0.417 +- 0.095 (CFG493 a0),
0.641 (a0 = 1.2e-10); 0.500 only on the canonical footing that defines it.

## 4. Plain answers

**Is kappa derived anywhere?** No. Every lane that outputs a number either assumes it (OUT-2's lock;
OUT-4's T*; FINAL-16's equality epoch, beta = 1) or misses it (FINAL-18 by 1.2-2.2 dex, FINAL-19
gives sqrt(2 pi), OUT-3 gives K >= 3/2, FINAL-17 menu spans 0.80 dex).
**Is 5.41 derived anywhere?** No. It enters FINAL-11/14 as a constant; OUT3_cosmic_share_fold's
fold construction misses by 18.5 band-widths and drifts 1.8 dex; R541's free-integration-constant
statement stands.
**What was established instead:** algebra of the law certified in Lean (FINAL-9/11/14/17/19, OUT-4);
several candidate routes excluded (FINAL-17/18/19, OUT-3, OUT-4 window [0.323, 0.770] contains 1/2);
a conditional result: IF one postulates a 1:1 lock to the de Sitter KMS period, kappa = sqrt(2/(3 pi)),
not distinguishable from 1/2 until a0 is known to about 4 %.

## 5. Hygiene

Home paths (`/Users/...`) in committed files: FINAL-10 `build1.out`, FINAL-13 `audit_lean.py`,
`delta.py`, FINAL-14 `RESULT.md`, `final14_result.json`, FINAL-17 `compile.txt`, FINAL-20
`AUDIT.md`, `compile_ax_FINAL16_head.out`, `run_compiles.sh`, OUT-2 `compile_MUTATE.txt`.
"cold dark matter" / "CDM-like" for the component: none found. "Data favour the framework": none found.
False "committed alone" claims: FINAL-16, FINAL-17, OUT-2 (and FINAL-20 repeating FINAL-16's).
Not checked: regeneration of FLD1/FINAL-18 fold runs (heavy); FINAL-13's own `audit_lean.py` (its
rows checked by my builds instead).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
