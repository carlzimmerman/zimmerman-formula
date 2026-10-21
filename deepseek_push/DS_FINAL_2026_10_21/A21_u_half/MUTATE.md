# A21 — mutations

Three mutations, each a realistic slip for this lane, each invoked by a flag and each recorded as
captured stdout beside the main run. Every mutation must break at least one declared check; all
three exit 1.

    python3 a21_checks.py             -> a21.out,             a21_results.json             exit 0
    python3 a21_checks.py --mutate    -> a21_MUTATE.out,      a21_results_MUTATE.json      exit 1
    python3 a21_checks.py --mutate2   -> a21_MUTATE2.out,     a21_results_MUTATE2.json     exit 1
    python3 a21_checks.py --mutate3   -> a21_MUTATE3.out,     a21_results_MUTATE3.json     exit 1

## M1 — the denominator slip (the lane's central error)

`n_supply()` returns `R_cosmic` instead of `R_cosmic/f_ret`: the catchment is identified with the
system, i.e. `f_ret = 1`. This is the slip that produces the lane's premise if it is made at *one*
anchor only: it turns `u(MW)` into `25.043/5.364 = 4.668` while leaving the cluster at `0.488`.

Breaks **K6, K7** (23/25):

    K6 FAIL u_MW=4.66842+-0.9774 0.46684+-0.002, 0<Z<1.5 :: MW anchor: -4.26 sigma from 1/2
    K7 FAIL u_joint=0.47733+-0.03622 ... chi2=18.81, p=0.00 ; anchors agree at 4.29 sigma
    A21 COMPLETE: 23/25 checks PASS.

The MW needs 4.7x more cold energy than the entire catchment holds — the two anchors then disagree
at 4.3σ, and "u ≈ 1/2 at both" is gone. K8 still passes under M1 by construction: it computes the
f_ret ratio from `f_ret_of()` directly, which is the point — the audit of §K8 is *about* the table,
not about the supply call.

## M2 — the amplitude slip

`lambda_req` is set to `A_law` (1.9102) instead of `A_law(A_newton−1)/(A_newton−A_law)` (2.1206), i.e.
the ΔΣ amplitude `A` is read as the rescaling `λ`. This is A18's M2 repeated on the new route.

Breaks **K4, K5, K15, K21** (21/25):

    K4 FAIL u_data=0.52351+-0.03251 0.47157+-0.001
    K5 FAIL -0.723 ...
    K15 FAIL 3f_b=0.47138 matches u_data to -1.60 sigma
    K21 FAIL ... sigma_u<=0.00784 ... N>=8299
    A21 COMPLETE: 21/25 checks PASS.

`u` moves from 0.472 to 0.524 — still under 1σ from 1/2, which is exactly why the check is on the
*value*, not on the distance: a slip that cannot be distinguished by the 1/2 test alone is still a
slip.

## M3 — the response-function shortcut

`u` is read off the response at `x = 1`: `u := μ(1) = φ = 1.618`. This is the literal form of the
lane's third candidate route.

Breaks **K16, K21** (23/25):

    K16 FAIL mu(1)=1.6180, 1-mu=-0.6180 ... :: neither
    K21 FAIL sigma_u<=0.37268 ... 
    A21 COMPLETE: 23/25 checks PASS.

K16's teeth are the two clauses `|u_data − μ(1)| > 0.5` and `|u_data − (1−μ(1))| > 0.5`: the
substitution makes the first identically zero, so the check fails by construction exactly when the
shortcut is taken.
