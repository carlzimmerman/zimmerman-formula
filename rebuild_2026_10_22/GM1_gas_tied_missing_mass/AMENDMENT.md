# GM1 amendment, written after the first complete run

**K7 failed as frozen.** The law's median SPARC residual at LW1's Upsilon is +0.005 on canonical and +0.022 on alt, against a line of 0.02. The line stays and K7 stays FAIL in `gm1.out`.

The frozen rule, "failed check: no verdict", is departed from in one narrow way: T1, T2 and T3 labels are still given, because no SPARC number enters them. Only T4b reads SPARC, and T4b alt carries this flag. T4b has no label. The owner may reject this departure; in that case read the T1-T3 labels as not issued.

Why the miss isn't taken to be a reader fault, without moving the line: LW1's Upsilon is the median of per-galaxy fits, not a global zero-point, so a fixed-Upsilon median need not vanish. A rough per-galaxy fit in this lane (K7b, not the grader's fit) gives median Upsilon 0.49, 0.41 against 0.52, 0.44. That checks the reader only to about 0.03 in Upsilon.

**Added after the result, reported only, in no label:** T3 cell B with errors capped at 0.2 dex or at the median, medians of cell B, F1 and F2 in cell A, S2 medians; Okabe exponent on the catalogue axis (the frozen T2 ARTEFACT clause needs it but the frozen list omitted it, so it decides that clause); KiDS k3(1) in Okabe's gas bins; the same 35 clusters on both shears; an Okabe binning mock; Lovisari+20 rows.

**Changed from the frozen text, disclosed:** T2a reports means as frozen, and K1 compares LM1's medians because LM1's table holds medians. K5 had a nan from empty bins on the first run; bins with W = 0 or V <= 0 are now excluded. Cell B's frozen mock was not changed.
