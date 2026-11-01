# CRG1 BUILD: DISCLOSURES

kappa = 1/2 is FITTED. Cold dark energy is a gravitating field component. Nothing here says the data favour the framework.

## 1. Exposure to prior numbers (separation)

**No read I made went outside the build folder.** No file in the parent repository, transcript or memory file was opened, listed or searched by a tool call. The Tier C files of SPEC section 7 weren't opened.

**But my session context was not clean.** Before the task reached me, the harness loaded into my context a memory index and a git summary from the parent project. I didn't ask for them and can't unsee them. They contain earlier values and verdicts, including:

- "M3 +4.41" and "keys fail 12/15": touches C1 K (and C3 K, which is C1's row)
- SPARC line "Υ 0.75/0.76": touches C1 S
- "Upsilon 0.35 FAILS": touches C2 S
- "X-COP ONLY", "X-COP passes", "LITTLE THINGS" cost: touches C1 X, C1 LT
- "η_conv 21.5": touches A1 (also given in the spec)
- commit subjects saying FG1's C1, C2, C3, C4 all fail and route E does not survive: touches every candidate's verdict
- the SPEC/criteria flag "0.0541 against 0.0795", which you told me to ignore: touches C4 S, and the first number equals my C4 canonical rms

Some of my cells print the same values as these lines. **So that agreement is not fully blind evidence for those cells.** What I can state: no reading, code path or fix was chosen by reference to them; the code follows the spec's equations; the primary readings were fixed before each cell ran. I can't prove that from inside. The criteria say a forbidden read voids the cells it touched. This wasn't a read I made, so voiding is the owner's call. An independent check would be a rerun in a session without that context, using these scripts or a fresh build.

## 2. Fixes during the build

1. **AQUAL solver, inner-flux sign (crg1_efe.py).** First solve gave negative M. Found by the spec's own sanctioned comparison with `efe_table_*`, and by the finite-volume balance: outward flux at the inner face is -(1/r_min^2) A. One sign changed. This ran before any K cell.
2. **K1 shear mock (crg1_k1_shear.py).** As written the mock has no scatter, so sigma is rounding error, about 1e-15. See NEW_AMBIGUITIES NA6. A twin with real scatter was added; the as-written check is kept.
3. **Zoom known answer.** First version copied the measuring lines into the test. Refactored so the test and the real path call `shape_measure`.
4. **numpy warnings.** `matmul` on this numpy/Accelerate build raises spurious floating-point flags. Warnings are silenced in crg1_clusters.py; values were read as finite and the mock reproduces its target.

No K check failed on the final code apart from the mutations, which must fail and do.

## 3. Results seen before the final run

I viewed my own values once to look for bugs, then did a clean rebuild. Changes after that view were additive only: alternate readings NA4b, NA9b, NA13b, a saturation counter, and a rewrite of `stack` with the same arithmetic. No primary code path changed, and no primary reading was changed.

## 4. Departures from the written output format

- Results are in `crg1_results.json` in the build folder, per the task, not `results/` per SPEC section 9.
- Run time and peak memory are in `crg1_runtime.json` and `crg1_run.log`, not in the results file, so that K3 can be byte-identical.
- K1 needs the zoom and C(s) steps, so those two run first. K1 then runs before K2 and before any graded cell.
- `K_S`, `eta per seed` and C(s) comparisons use values SPEC section 8 sanctions as known answers.
- A resumable design replaces signal handling: every finished cell is written atomically and skipped on restart. A SIGTERM loses at most one cell. Resume was not exercised by a real kill, since no run was interrupted.

## 5. Not recomputed or not computed

- Tier C (MW, DM, IC; C2 G, C2 Ln): not done, per the task. C2 G was computed as a labelled extra, since the spec offers the equations; it's not graded here.
- A2(b): original float64 not available. The per-seed eta check shows no change at float32 (max difference in the results file).
- A17(b): not computed, per the spec.
- Non-native values in the chain are as listed in SPEC section 10, left in place.
