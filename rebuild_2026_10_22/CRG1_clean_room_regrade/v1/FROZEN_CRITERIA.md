# CRG1_clean_room_regrade: FROZEN CRITERIA, committed alone before any spec, script or number of this lane

**Question.** Does FG1's scorecard survive being rebuilt from its definitions and raw data by code that shares nothing with the existing graders? Opened by the owner, 2026-11-01. This is a data-side audit, not a mechanism lane: no new physics, no new fitted number, no new simulation. Either direction counts: a fail that turns out to be a grader fault and a pass that does are reported the same way.

**Why.** Everything after FG1 reads its table. A grader defect sat in four outer keys from X71/GS1 until 10-31. FG1's own outputs carry an unresolved flag (`x62_x43copy_law_a2.out`, `x62_x43copy_on_shpS9_L7.082_T12.3_B.out`: "K0 rule forced to Sigma_a0 reproduces X38 ... FAIL", SPARC 0.0541 against 0.0795).

**Not blind, disclosed.** The author of these criteria has read FG1's criteria, including its expected failures, and many older numbers on record. FG1's table had not landed at this freeze. Separation below is by instruction on one filesystem, not enforced by a sandbox. Stated in the verdict.

## Stages
1. **SPEC.** A spec agent writes `SPEC.md`: every line, statistic, sample cut, footing, background, input file and pass rule in prose and equations. It may read criteria and code, because some definitions exist only in code. It writes no result number, only inputs. A definition it can't close from the record goes in an **AMBIGUITIES** list, with each plain reading stated. That list is itself a finding.
2. **BUILD.** A fresh implementer agent gets only `SPEC.md`, these criteria and a copied `inputs/` folder. It reads no grader code, no result JSON, no lane README and no FG1 output, and imports nothing from the repo. A forbidden read is disclosed and voids the cells it touched.
3. **SEAL.** Results are written and committed, with sha256, before any comparison. No FG1 number is opened by the implementer.
4. **COMPARE.** A separate script reads the sealed results and FG1's table and assigns classes. After the seal, any fix goes in a separately named v2, with its cause stated. v1 stays and is reported first.

## Inputs
Raw and measured data only: SPARC rotmods and table, LITTLE THINGS, X-COP, eRASS1 catalogue and shear stacks, group and dwarf tables, as the spec names them. Zoom outputs: η is re-estimated from run outputs where they are on disk. Otherwise the stack is taken as given and tagged **[INPUT AS GIVEN]**, because this lane doesn't rerun simulations. CFG and ledger gates apply: the 404 `SPARC_table.txt` isn't data; the RC100 corrected copy is used if RC100 enters.

## Scope
| Tier | Lines | Candidates | Treatment |
|---|---|---|---|
| **A** recomputed | S, Tl, LT, K (all 15, both h cells), X | C1, C3, C4; C2 where NR3's response has a spec that closes | full rebuild |
| **B** recomputed if the spec closes | G, Ln, Dw | C3, C4; C1 where it closes | rebuild, else trace |
| **C** traced | MW, DM, IC, and any B cell not closed | all | the source file and value are checked and the path is stated; tagged **NOT RECOMPUTED** |

**NOT RECOMPUTED is never agreement,** and NOT GRADED in FG1 stays NOT GRADED here. Canonical is primary, alt reported, never pooled. C3's approximation on Tl and LT and its floor disclosure carry over from FG1 as stated there.

## Classes, per cell, frozen
| Statistic | MATCH | CLOSE |
|---|---|---|
| rms, Υ, median E, tilt | \|d\| ≤ 0.01 | \|d\| ≤ 0.03 |
| Z of a key, X-COP, group or dwarf Z | \|d\| ≤ 0.10 | \|d\| ≤ 0.30 |
| Δχ² | \|d\| ≤ 1 | \|d\| ≤ 3 |

Pass/fail on the line must also agree. **DISAGREE:** beyond CLOSE, or the line's pass/fail differs in any case, including inside the tolerance. A disagreement within the tolerance of a pass line is still reported as a flip.

## Verdict
- **REPRODUCED:** every Tier A cell MATCH or CLOSE, and no pass/fail flip in Tier A or B.
- **REPRODUCED WITH GAPS:** the same, with some Tier A cells not recomputed, listed.
- **DISAGREES:** any DISAGREE, listed. Each is then diagnosed against the definitions and data to say which code is wrong, or whether the spec is ambiguous. A diagnosis naming FG1 doesn't edit FG1: it's reported to the owner and FG1's session.
- Per candidate, the regrade's own verdict is stated by FG1's rule. Route E's overall sentence is restated only if it changes.

Reported, not graded: the AMBIGUITIES list; the x62 flag, as harness mode or fault, resolved by the spec agent if the record allows; run time and memory.

**Expectation on record, mine.** Most Tier A cells match, no line flips, and any disagreement is likeliest in K's outer keys or from an ambiguity in the chain of inherited definitions. No call on C2's cells.

## Checks
- **K1 injection.** Synthetic inputs with known answers go through the same code before real data: a mock SPARC set at known Υ recovered within 0.01; a mock shear stack at a known excess recovered within 0.10 in Z.
- **K2 data.** Row counts and file hashes of every input are printed, and the sample sizes are checked against SPEC.md.
- **K3 repeat.** Rerun of results byte-identical, seeds fixed.
- **MUTATE.** ν set to 1 in the law, separate outputs: S must fail. Excess sign flipped in K's mock: K1 must fail, exit 1.
- **K4 trace.** Every Tier C value appears in its named file, by JSON key or literal.

Any K failure before the seal: no verdict, fix, rerun, and disclose it.

## Limits
Runs after FG1's table lands, and FG1's files are never edited. It can't catch an error in the raw data, in a shared published definition, or in a zoom taken as given. It says nothing on whether the theory is right. One thread, nice 15, under 1 GB, small on disk; yields to live runs. Local commits; push when finished; no deposit without the owner's go.

κ = ½ FITTED. T LOCATED, not derived. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.
