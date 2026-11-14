# RRL1R LEAD CHECK (2026-11-14): commit ids, the lead's re-run, the blindness check, and the comparison with RRL1

Written by the lead session after the blind result was committed. TEST lane; adopts nothing, relabels nothing.
The blind agent's files in this folder are not edited.

## Commit ids

| what | local | origin |
|---|---|---|
| frozen criteria + WHAT_I_SAW_AT_START.md (alone) | 36f607a3c4 | 65fb6b74e5 |
| scripts and run outputs | e59cab4a63 | dd4c29ca44 |
| RESULT_BLIND.md | 86aa43ee19 | 8a48187e4c |

The agent's hand-back gave 8e1fd5b361 for the result commit. That id is another session's commit made two seconds
later in the shared checkout; the agent read `git log -1` after it landed. The result file's own commit is 86aa43ee19.

## The lead's re-run

`rrl1r.py` copied alone into a new folder at the same depth (`closure_2026_11_14/RRL1R_leadcheck_copy/`, not
committed, removed afterwards) and run from scratch with the same three inputs: exit 0 after 76 s.
`rrl1r_results.json`, `rrl1r_MUTATE.out`, `mocks_null.jsonl`, `mocks_T1.jsonl` and `mocks_des_null.jsonl` are
byte-identical to the committed files. `rrl1r.out` differs in one line only (line 223, which names the output
folder). This agrees with the agent's own identity check (`rrl1r_identity.out`).

## Blindness

- The agent's transcript was read for its tool calls. It opened the specification file, RAW1's `RESULT.md`,
  `raw1.py` and `raw1_model.py`, MWT1's `mwt1.py`, and its own files. It opened nothing in RRL1's folder, the CJ1
  scorecard, MWT2, the papers folder or the memory folder, and did not use the web. Its git commands were `git add`,
  `git commit`, `git log -1 --format=%h` after each of its own commits, and `git status` on its own folder.
- One route was not closed as intended. Before the launch the lead replaced the RRL1 clause of the memory index line
  with a placeholder, but the agent's starting context still showed the old line, cut off by the index itself at
  "RRL1: hot Milky Way b…" (`WHAT_I_SAW_AT_START.md`). The index a subagent sees is the one loaded when the lead's
  session started, so an edit made during the session does not reach it. The fragment names the bin that RAW1's own
  record already calls hot and carries no label, slope, break value or pass/fail word. The lead's reading: no leak.
- The five commit subjects the agent started with did not mention RRL1.
- The specification handed over was RRL1's `FROZEN_CRITERIA.md` sections 0 to 8, verbatim; its section 9 (RRL1's
  expectation and hand estimate) was withheld.

## Comparison with RRL1 (made after the blind result was committed)

Labels (frozen reading), canonical and alt never pooled:

| case | RRL1 | RRL1R (blind) | same? |
|---|---|---|---|
| census, canonical | MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD]; FRAGILE: score > 0.9 and distances x1.05 give NO POWER; no Sgr band gives FAIL SURVIVES (20-30 COLD); single law gives FAIL SURVIVES (30-40 HOT, 1.125) | the same label; FRAGILE through the same four brackets with the same words (single law 30-40 HOT, 1.125) | yes |
| census, alt | the same label; FRAGILE: single law gives FAIL REMOVED | the same | yes |
| rotation-curve stellar mass, canonical | the same label; FRAGILE: single law gives FAIL REMOVED | the same | yes |
| rotation-curve stellar mass, alt | the same label; robust | the same; robust to every bracket | yes |

Numbers:

| quantity | RRL1 | RRL1R |
|---|---|---|
| PS1 stars in range / footprint cells | 5,421 / 5,143 | 5,421 / 5,143 |
| clump stars / cells masked by the clump rule | 3,077 / 442 | 3,077 / 435 |
| single slope | 4.770 [4.731, 4.809] | 4.769 +/- 0.039 (4.730 to 4.808) |
| broken law: inner, outer, break (kpc) | 5.293 +/- 0.077, 3.934 +/- 0.115, 39.0 +/- 1.2 | 5.291 +/- 0.076, 3.934 +/- 0.115, 39.03 +/- 1.14 |
| 2 Delta ln L against T | 78.1 against 9.45 | 77.78 against 7.977 |
| census canonical f, four bins | 1.058, 1.052, 0.857, 0.887 | 1.058, 1.052, 0.857, 0.887 |
| census alt f, four bins | 1.016, 1.008, 0.820, 0.849 | 1.016, 1.008, 0.820, 0.849 |
| rc canonical f, four bins | 0.994, 0.991, 0.809, 0.838 | 0.993, 0.991, 0.809, 0.839 |
| rc alt f, four bins | 0.979, 0.973, 0.792, 0.820 | 0.978, 0.973, 0.792, 0.820 |
| BHB cells check, 20-45 kpc | 5.139 [4.994, 5.285], CONSISTENT | 5.138 +/- 0.146, CONSISTENT |
| DES single / broken | 4.901; break 76.8 at the edge, outer 1.2 +/- 1.3 | 4.900 +/- 0.082; break 76.8, outer 1.17 +/- 1.62 |
| K3 (RAW1 reproduced) | 1.5e-10 (RAW1's own integral through MWT1's copy) | 7.2e-6 framework cases, 2.5e-5 N (the agent's own integral) |
| T1 | 1 of 50, PASS | 1 of 50, PASS |
| T2 (distance shuffle) | FAILS: break survives, 5.09 / 3.96 / 43.8, 2 Delta ln L 42.5 | FAILS: break survives, 5.012 / 3.951 / 46.4, 2 Delta ln L 31.34 |
| M1 (60 per cent kept beyond 40 kpc) | FAILED TO BITE: break at 58.7 kpc, outer 2.36 | FAILED its own window: break at 48.8 kpc, outer 4.079 (steeper) |
| M2 | bites | bites |

Reading:

- **The blind build confirms RRL1 on all four framework cases and both footings: the same label and the same
  fragility.** The fitted profile agrees to the third decimal and the per-bin f to 0.001. The threshold T differs
  (9.45 and 7.977) because the two builds draw their own null mocks; the break statistic is about 78 in both and
  the detection does not depend on which T is used.
- What this confirmation covers: the arithmetic of the frozen specification, done twice with separate code for
  the RR Lyrae side and, in RRL1R, a separate Jeans integral. What it does not cover: the specification itself.
  Both builds use the same cuts, the same completeness function (r_F = DM + 0.6, from memory, PROVISIONAL), the
  same band mask for Sagittarius and no purity model, so a wrong assumption there is shared by both.
- Both builds name the same soft spot. The outer slope beyond 39 kpc moves from 3.36 (score > 0.6, or the steeper
  completeness) to 4.20 (score > 0.9), it reverses without the Sagittarius mask, and with a single law the
  40-55 kpc bin passes in three of the four cases. The label is FRAGILE in three of four cases for that reason.
- Both builds find that DESI's NFW moves exactly as the framework does, so the cold 40-55 kpc bin is a statement
  about the tracer profile and not about the framework in particular.
- T2 fails in both builds, as the specification expected. M1 fails in both, differently: neither recovers a break
  "near 40" from a planted step. K2 (a planted slope change) is recovered in both.

Scorecard row 28 (halo stars with the slope measured from RR Lyrae) keeps its word, FAILS, with fragility as
before; its blind column changes from "no" to "yes (RRL1R, same label and fragility)".

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
