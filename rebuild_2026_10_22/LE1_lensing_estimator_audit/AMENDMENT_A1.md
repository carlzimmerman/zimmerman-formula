# LE1 AMENDMENT A1: POST-RESULT diagnostics, after `le1_controls` and `le1_real` were read. Changes no line, no swap and no label

Written after reading: KA2a misses its 0.01 line on the SIS (innermost bin 0.989); G1's swap ladder (no single swap brings the law within |Z| 2); G3 passes NP1 (+1.69) where G1 fails it (+8.45) and A1 fails it (+5.43).

Mode `post` (`le1_post.{json,out}`), reported, not graded:
- **P1. Where A30's χ² sits.** Base fit, law and NP1 L3, both footings: χ² contributions r_i (C⁻¹r)_i summed over R ≤ 0.31 and R > 0.31 and per bin, and data/model by radius.
- **P2. The KA2a miss.** (a) The same projector against a truncated-SIS quadrature (truncated at the grid edge, as the grader is), to tell truncation from the inner-disc start. (b) The frozen rule needs the number the miss moves. Replacing the projector inside the key chain isn't run. It is bounded per key as max band deviation × |pred| / s, using KA2a's SIS deviation per band (INNER bins 0-2, MID 3-5, OUTER 6-7) and each key's pred and s from this lane's base key runs, worst over h and f★. Slope keys (-b) are skipped: a uniform scale doesn't move a slope to first order. The verdict reads this bound as the moved number.
- **P3. G3's error budget.** G3 again for law and NP1 with each row's σ set to the data-only error (Fig-3 column 3 over column 1, in dex), in place of CX1's Monte Carlo sd (data plus ASSUMED M★ 0.15 dex and gas share 0.2 ± 0.1, drawn per bin but then averaged over rows as if independent).

`verdict` reads `le1_post.json` only for P2's bound, as the frozen rule's "number it moves" for KA2a. κ = ½ FITTED. Not theory closed.
