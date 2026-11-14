# RRL3R LEAD CHECK (2026-11-14): commit ids, the lead's re-run, the blindness check, and the comparison with RRL2

Written by the lead session after the blind result was committed. TEST lane; adopts nothing, relabels nothing.
The blind agent's files in this folder are not edited.

## Commit ids

| what | local | origin |
|---|---|---|
| WHAT_I_SAW_AT_START.md + frozen criteria (alone) | 33c0932f6c | 5bb846b089 |
| script, the as-frozen run 1 output, the known-answer diagnostic | 929d8af29b | 524eeca7d5 |
| AMENDMENT_A1.md (alone) | 96c6f91588 | 72ca10c54a |
| script under A1 and run 2 outputs | 1b23405533 | 01797a79bd |
| RESULT_BLIND.md | 123fa9bb89 | 4fd8d479cd |

## The lead's re-run

`rrl3r.py` copied alone into a new folder at the same depth (not committed, removed afterwards) and run from scratch
with the same three inputs, without the stored mock files: `rrl3r_results.json`, `rrl3r_MUTATE.out`, `mocks_null.jsonl`
and `mocks_des_null.jsonl` are byte-identical to the committed files. `rrl3r.out` differs only in its elapsed-time
stamps.

## Blindness

- The agent's tool calls were listed by script (62 calls, no web call). None touched a forbidden folder or file: nothing
  in RRL1's or RRL2's folders, nothing of RRL1R's but `rrl1r.py`, nothing of MWT1's but its criteria and `mwt1.py`, no
  scorecard, no papers folder, no memory folder.
- Its starting context (`WHAT_I_SAW_AT_START.md`) held one commit subject of the lead's own, the scorecard's fifteenth
  update, which says "row 28 untouched pending a blind lane". That names no outcome. It also saw the folder name of the
  earlier one-convention lane in a listing and opened nothing in it. The lead's reading: no leak.
- It read one file the specification did not list, RAW1's `raw1_results.json`, for the RAW1 known answer. RAW1 is the
  lane that built the sample and is not forbidden.
- The specification gave it one stored result, MWT1's four f values for a different star-count profile (its KA-2), and
  said so.

## Comparison with RRL2's post hoc reading of the same convention (made after the blind result was committed)

| quantity | RRL2, bracket B1 (not blind, post hoc) | RRL3R (blind, under its A1) |
|---|---|---|
| census canonical, four bins | 1.061, 1.088, 0.972, 0.954 | 1.0607, 1.0880, 0.9721, 0.9537 |
| census alt | 1.019, 1.043, 0.930, 0.912 | 1.0189, 1.0427, 0.9305, 0.9120 |
| rotation-curve mass, canonical / alt | 0.996 / 0.981, 1.025 / 1.006, 0.917 / 0.898, 0.901 / 0.881 | 0.9958 / 0.9809, 1.0251 / 1.0058, 0.9175 / 0.8985, 0.9011 / 0.8812 |
| DESI's NFW | 1.035, 1.034, 0.926, 0.926 | 1.0347, 1.0337, 0.9265, 0.9261 |
| star-count profile | RRL1's 5.29 / 3.93 / 39.0 kpc | 5.291 / 3.934 / 39.03 kpc, its own fit |
| words, census canonical / alt | NO VERDICT (draws 0.82) / PASSES | NO VERDICT (SLOPE) (0.825) / PASSES, both FRAGILE |
| words, rotation-curve mass canonical / alt | PASSES / PASSES | PASSES / NO VERDICT (SLOPE) (0.840, on the boundary), both FRAGILE |
| words, DESI's NFW | PASSES | PASSES, FRAGILE |
| power | its frozen twins were run on another convention and did not bite | null twin 20 of 20 pass; planted cold 40-55 bin caught 18 of 20; planted hot 30-40 bin caught 20 of 20 |

Reading:

- **As frozen the blind lane reads NO VERDICT (KNOWN ANSWER) on every case.** One planted star-count mock came back
  3.1 sigma off. The agent then drew 40 more, found the fit unbiased, and amended the known answer to those 40 seeds
  before any gate number existed. The thresholds were chosen after seeing that diagnostic, and the amendment says so.
  Everything below is the reading under that amendment.
- **The blind build reproduces RRL2's post hoc numbers to the printed digit**, with its own code for the anisotropy,
  the Jeans step and the estimator. Under this convention every bin of every framework case, and of DESI's NFW, is
  inside twice its error.
- **The gate has power under this convention.** The planted 20 per cent cold bin and the planted 25 per cent hot bin
  are caught. That was the open point in RRL2.
- **Two of the four framework cases read NO VERDICT (SLOPE)**, at 0.825 and 0.840 of the profile draws against a
  window that ends at 0.84. So the blind lane gives two fragile hits and two no-verdicts, not four passes.
- **Every case is FRAGILE**, and the brackets say on what: with one constant anisotropy in place of the measured
  profile the 40 to 55 kpc bin is COLD again in four of the five cases; with the RR Lyrae score cut at 0.6 the same;
  with a single star-count law the census canonical case is HOT at 30 to 40 kpc. With no corrections at all, 40 to 55
  kpc is COLD for every framework case and for DESI's NFW, which is what RRL1 and the blind RRL1R read.
- **The gate does not separate the framework from DESI's NFW** under this convention: no framework case passes where
  the NFW fails.
- The agent's main worry is the lead's too: the outer star-count slope moves from 4.20 to 3.36 as the score cut is
  loosened, and DES sees no break. The passes lean on that shallow outer slope.
- What this covers: the arithmetic of the measured-anisotropy convention, done twice, and its power. What it does not
  cover: the catalogues, the cuts, the completeness function and the cold-group star list, which every lane on this row
  shares; and which anisotropy convention is right.

So row 28 now has two blind-checked readings that differ only in convention: a fail with a constant anisotropy (RRL1,
RRL1R) and no fail with the measured one (RRL2 post hoc, RRL3R). The scorecard word is not changed here; that is the
owner's decision.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
