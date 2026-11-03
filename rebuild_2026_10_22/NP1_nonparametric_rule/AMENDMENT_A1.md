# NP1 Amendment A1, 2026-11-03, pre-result, committed alone before any control or real-data gate number

No control, real fit, gate or oracle number on real data has been read. Before this, I ran three smoke checks:
- planted-data fits, which timed the fit;
- hull membership on real leaves, with no B and no rule;
- a plumbing check: a rule with α = 0, which is the plain law, run through RQ3 with `--no-keys --no-bullet`.

The plumbing check reproduced RQ3's own `results/law.out` card row for row, for example A10 Z −3.94, A30 +9.27 and C1 +16491.96 at canonical. That card is already on record. κ = ½ FITTED. Not theory closed.

1. **L5 hull on four coordinates.** In 5-D, asinh D is a fixed function of the other four leaves. So train and holdout points lie on a curved 4-D surface, and a holdout point can sit on that surface yet outside the 5-D convex hull. On the smoke check, about 12 % of even-SPARC points were in the 5-D hull, against about 91 % in 4-D. So the L5 hull is taken on (log y, log ell, f, s). Reach still uses all five coordinates and the frozen lengths. L3 is unchanged.

2. **Rows decided by the prior mean.** The prior mean is the plain law, so far from all data the rule returns to the law. The law fails C1 (planets, Z +16492) on RQ3's own card. Every rule in this class therefore fails C1 by construction, and the leaves' data can't change that. As frozen, SMOOTH RULE EXISTS couldn't be reached by any rule, which would make the label empty. A new label is added between the frozen ones:
   - **SMOOTH RULE EXISTS IN REACH.** The rule passes gates 1 and 2, and every failing line is out of train's reach. Out of reach means the line is NOT LOCATED, fewer than 90 % of its located points are in the hull, or, for a point-row line, its in-hull subset passes.
   - The out-of-reach failures are listed beside the label.
   - It is weaker than SMOOTH RULE EXISTS, and it's a description of data, not a theory.

   NO SMOOTH RULE IN LEAF SPACE and UNDETERMINED are unchanged. A failing line that is in hull but that the oracle passes still reads UNDETERMINED.

3. **Plumbing smoke outputs** (`rules/smoke_*`, `candidates/np1_smoke_*`, `results/np1_smoke_*`) are gitignored. They aren't results.

Gates, tolerances, split, model class, smoothness selection and controls are unchanged.

κ = ½ FITTED; not theory closed.
