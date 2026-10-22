# A52 — mutations

Four mutations, each breaks **exactly one** declared check and nothing else. Run:

    python3 a52_checks.py --mutate=M1     # exit 1, 16/17 (K2 fails)
    python3 a52_checks.py --mutate=M2     # exit 1, 16/17 (K6 fails)
    python3 a52_checks.py --mutate=M3     # exit 1, 16/17 (K12 fails)
    python3 a52_checks.py --mutate=M4     # exit 1, 16/17 (K11 fails)

Captured stdout: `a52_MUTATE_M1.out` … `a52_MUTATE_M4.out`; the corresponding JSON is
`a52_results_M1.json` etc. (the clean run writes `a52_results.json`). Each mutated run prints
`MUTATION CONFIRMED (<id>): broken checks <K>`.

## M1 — the comparison target replaced by the integer 12

`k2()` compares every candidate against 12.0 instead of 2√(32π/3). The row `12` then becomes a
6-digit hit and is not a rewrite of the target.

    K2    FAIL hits=1 (distinct values=1), non-rewrite hits=1, closest miss=1.0866% ...
    A52 COMPLETE: 16/17 checks PASS.
    MUTATION CONFIRMED (M1): broken checks K2

Why it bites: K2 is the check that distinguishes "the only hits are algebraic rewrites of the
target" from "some other closed form hits it". If the target were the integer 12, a non-rewrite hit
would exist and the numerology verdict would be wrong. The mutation shows K2 tests the identity of
the hit set, not merely that some hit exists.

## M2 — the Friedmann normalisation dropped

`k6()` replaces `H = sqrt(8πGρ/3)` by `H = sqrt(8πGρ)` (drops the 1/3), i.e. it pretends the
Einstein–Friedmann coefficient is 8π rather than 8π/3.

    K6    FAIL residuals (4*sqrt(pi)*(-sqrt(6) + 3*sqrt(2))/(3*kappa),0,
          8*sqrt(pi)*(-sqrt(6) + 3*sqrt(2))/3) ; 2cH/a0=11.5776200729 ; a0=9.354173e-11
    A52 COMPLETE: 16/17 checks PASS.
    MUTATION CONFIRMED (M2): broken checks K6

Why it bites: the entire question is whether 11.5776 is the Einstein 8π/3 normalisation restated.
A 3× error in that normalisation is the single most likely bookkeeping slip in the derivation, and
K6 is an *exact symbolic* identity test (residual must be exactly 0), so it fails on any change to
the coefficient. Note that the printed numerical ratio is still the correct one — K6 tests the
symbols, which is why the mutation surfaces as a nonzero residual rather than a shifted number.

## M3 — the look-elsewhere pool emptied

`k12()` reports zero hits at 1 % (as if the pool contained nothing near the target).

    K12   FAIL hits@1%=0 of 4008 window values (0.0%) ; hits@0.01%=9
    A52 COMPLETE: 16/17 checks PASS.
    MUTATION CONFIRMED (M3): broken checks K12

Why it bites: K12 is the negative control — it asserts that a 1 % coincidence is *cheap*
(base rate > 5 % of the order-10 window). If the pool really had no hits, the look-elsewhere
argument would collapse and a 1 % match would be evidence. The mutation shows the check measures
the base rate, not just the existence of a pool.

## M4 — κ measured to 0.5 % instead of 22.8 %

`k11()` sets κ_meas = 0.500 ± 0.005.

    K11   FAIL N(kappa_meas)=11.578+-0.116 ; z(2Z)=0.00 ; z(12)=3.65 ;
          sigma_kappa(3sig)=0.00608 vs 0.005
    A52 COMPLETE: 16/17 checks PASS.
    MUTATION CONFIRMED (M4): broken checks K11

Why it bites: K11 asserts both that the current data *cannot* distinguish 11.5776 from 12 (both
within 1σ) and that a 10× improvement in σ(κ) is still needed for a 3σ separation. With a 0.5 %
measurement the second condition fails (the required σ is 0.00608, the current one 0.005), which is
exactly the point: the number's empirical status depends on σ(κ), and K11 is sensitive to it.

## What is *not* mutated

K1, K3, K4, K5, K7, K8, K9, K10, K13–K17 are not mutated. K8 (the product/curve test) and K9 (the
irrationality proof) are exact symbolic statements whose failure modes (a sign error, a wrong
level-set dimension) are already exercised by their own residual/dimension assertions; mutating them
would only re-test arithmetic. K13–K15 are counting statements about a declared pool — changing the
pool is a different analysis, not a bug, and is reported in the report's "What this does not do".
