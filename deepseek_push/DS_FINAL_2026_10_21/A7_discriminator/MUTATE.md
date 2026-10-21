# A7 MUTATE — swapping the two laws must flip the sign of Δχ²

Run:

    python3 a7_checks.py --mutate        # -> a7_results_MUTATE.json, a7_MUTATE.out

## What the mutation does

`--mutate` swaps the label→law map used by the scoring layer: label `n1` now carries
`g² − g_N² = a₀ g_N` and label `n2` carries `g_N = g²/(g + a₀)`. The fits, the Υ grid, the
point selection, the error model and the decision rule are unchanged — only which physical
law is called "n=1" and which "n=2". This is the mutation the task asks for: it must flip the
sign of Δχ² and nothing else.

## Baseline (a7.out)

    [canonical] chi2_n1=7259.38  chi2_n2=7478.83  dchi2(n2-n1)=+219.453
    [alt]       chi2_n1=7908.09  chi2_n2=7563.43  dchi2(n2-n1)=-344.663

## Mutated (a7_MUTATE.out)

    === PRIMARY: total chi^2 (a single Upsilon per galaxy, both laws, each footing separately) ===
      [canonical] a0=9.360e-11  chi2_n1=7478.83  chi2_n2=7259.38  dchi2(n2-n1)=-219.453  |  n1 wins 87  n2 wins 84  ties 0 of 171
            per-galaxy dchi2: median +0.015  mean -1.283  sd 22.721  [p5 -27.306, p95 +16.964, min -143.130, max +122.243]
            sign test p=0.879 ; bootstrap sd of total 294.44 -> z=-0.75

    K5 PASS mutation=True ; reported(label-based) dchi2 canonical -219.453 alt +344.663 ; physical(law-based) dchi2 canonical +219.453 alt -344.663 ; residual=0.00e+00 | threshold 1e-9 (exact sign flip)
         vs committed baseline a7_results.json: max |mutated + baseline| = 0.00e+00 (threshold 1e-9)

    === VERDICT (frozen rule: |dchi2|>=9 kills; both footings must agree) ===
      [canonical] dchi2 = -219.453  ->  n=1 KILLED (3sigma, n=2 preferred)   [literal rule; bootstrap says 0.75 sigma from zero]
      [alt] dchi2 = +344.663  ->  n=2 KILLED (3sigma, canonical preferred)   [literal rule; bootstrap says 1.21 sigma from zero]
      combined: NO KILL: the two laws are not separated at 3sigma on both footings

    A7 COMPLETE: 8/8 checks PASS.

Everything else is invariant under the swap: χ²/dof (2.266 / 2.334), the Υ distributions, the
stacked residual table, the forecasts and the variants change sign (variants: +529.37 →
−529.37, +10535.03 → −10535.03, +195.06 → −195.06, +3064.32 → −3064.32 on the canonical
footing), while their magnitudes are unchanged to the last printed digit.

## Why this proves the check has teeth

K5 does not compare a number with its own negation. It scores Δχ² twice from the *same fits*
through the *same code path*: once with the run's label→law map and once with the physical
law identities, and requires

- primary run: `|Δχ²_label − Δχ²_law| ≤ 1e-9` (the map is the identity),
- mutated run: `|Δχ²_label + Δχ²_law| ≤ 1e-9` (the map is the swap),

plus, when `a7_results.json` exists, `|Δχ²_mutated + Δχ²_baseline| ≤ 1e-9` against the
committed primary output. If the swap were applied to the fits but not to the reporting layer
(or the reverse), the two would agree in sign and K5 would fail. The mutation therefore also
demonstrates that the sign of the reported Δχ² is a property of the *comparison*, not of the
data: the data cannot tell the two laws apart at this precision, which is the lane's result.

## Second, non-graded mutation (informational)

Dropping the 5 % error floor is *not* a valid mutation of the comparison — it changes the
likelihood, not the labels. It is reported as variant V2 in `report.md` and in
`a7_results.json`: Δχ² becomes +10535.03 / +3946.47, i.e. the comparison is then dominated by
the worst-fit points rather than by the laws. It is listed here only to record that it was
tried and why it is not the mutation of record.
