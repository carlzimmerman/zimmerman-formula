# NV1 Amendment A1, 2026-11-04: written AFTER step 1 (coverage and sign test, committed in bbdb031c76), BEFORE any control or fit

Step 1's numbers have been read (`nv1_coverage.out`). No control, fit, gate or RQ3 card has been run. This amendment records how the code implements the frozen text where the text left a choice, and two departures in step 1. No label, tolerance, gate or control changes.

## Departures in step 1 (post-result, disclosed)
1. **Inner permutation count in the look-elsewhere shuffles.** The real sign test uses 2000 permutations for the train-trend p, as frozen. Inside each of the 1000 E shuffles the re-run uses 500 permutations, for speed. The shuffle fractions printed (SEPARATES 0.004-0.006, PARTIAL or better 0.029-0.041 for E2 and E4) carry that choice. No candidate's real test reads SEPARATES, so no label depends on it.
2. **E1's σ_E.** The text says half the noclu-maxclu bracket per system; the code uses one value, the median half-bracket over the file (0.463 dex). E1 reaches no target row (every target group NOT COMPUTABLE), so this enters nothing.

## Implementation choices (as run in step 1, and for what follows)
3. **"Its 50 nearest train rows"** for a multi-row group (Dw-UFD, Dw, L) is the union over the group's rows of each row's 50 nearest train rows with E, in NP2's kernel metric. For IC 1613 (one row) it is exactly 50.
4. **RQ3 support files.** RQ3's `acceptance.py` imports `old_gates.py` and reads `tolerances.json` and `row_marks.json` from its working directory (the lane), as NP1 and NP2 run it. They are byte-identical copies of RQ3's (`cmp`), not edited.
5. **E-shuffle MUTATE (control 6) for E values the candidate computes on the fly.** Tabulated systems (SPARC discs, LITTLE THINGS, dwarfs, X-COP clusters) get E permuted across systems (seed 20261109); the same shuffled values feed the train rows, the holdouts and RQ3's lookups. E values the candidate computes from the call (lensing's EM1 of total baryons; the Milky Way and planets' LG basin) take the shuffled value of the tabulated system whose original E is nearest. This keeps one permutation everywhere, as frozen.
6. **SUBSET card for E2** drops the SPARC galaxies DDO064 and UGC03546 (BS1 `no_dist`) and the LITTLE THINGS galaxies without E2; every X1 dwarf has E2, so the dwarf list is not filtered.

κ = ½ FITTED; not theory closed.
