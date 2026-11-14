# Exact raw-law charge bound

2026-11-14. This adds a necessary budget constraint, not a new settling surface or switching rule. It does not adopt `min(R_caustic,R_budget)` as a derived model.

## Claim and proof

Let G, a0 and the available cold charge Q be positive. Let b(r) be the nonnegative enclosed baryon source used in the spherical standing-clock law. At each radius r >= 0, define the nonnegative cold mass C(r) by

    C(r)[C(r)+b(r)] = (a0/G) b(r) r^2.

All quantities use consistent physical units. This is equivalent to the exact force law after inserting `g=G(b+C)/r^2` and `g_N=Gb/r^2` at positive radius, with the continuous algebraic extension at r=0.

**Exact pointwise budget criterion.** For every r,

    C(r) <= Q  if and only if  (a0/G) b(r) r^2 <= Q[Q+b(r)].

For fixed b>0, the radius at equality is

    R_budget = sqrt[G Q(Q+b)/(a0 b)].

Proof: for a fixed b>=0, `F(x)=x(x+b)` is strictly increasing on nonnegative x. Therefore `C<=Q` is equivalent to `F(C)<=F(Q)`. Substitution of the defining equation gives the criterion. The fixed-source formula follows by solving its equality. If b=0, C=0 for every finite r, so no finite charge bound follows from that zero source. The fixed-b radius must not be substituted as a constant when b varies with r.

**First-crossing criterion.** If b is continuous and nondecreasing on a finite patch interval `[0,L]`, then C is continuous and nondecreasing there. The allowed radii form an initial closed interval, possibly all of `[0,L]`. If `C(L)>Q`, its endpoint is the unique solution of `C(R_budget)=Q`, and every raw-law settled radius must satisfy `R_set<=R_budget`.

To verify monotonicity, regard C temporarily as a function of two independent variables r and b. For b>0, its partial derivatives are

    partial C / partial r = 2(a0/G) b r / (2C+b) >= 0,
    partial C / partial b = [(a0/G)r^2-C]/(2C+b)
                          = C^2/[b(2C+b)] >= 0.

The radial partial derivative is strictly positive when r>0 and b>0. The expression for C extends continuously to b=0 and r=0. Since C is nondecreasing in each independent argument, nondecreasing b(r) makes the composite C(r,b(r)) nondecreasing, without requiring b to be differentiable. Continuity gives a first equality if `C(L)>Q`; at that equality r and b are positive, so monotonicity in radius makes the crossing unique. If `C(L)<=Q`, the entire patch is budget-allowed and no smaller radius is forced by this criterion.

This is a proof of the charge inequality and its radial consequence under the stated source assumptions. It does not prove that a static solution forms, that the charge reaches the needed distribution, or that a stable dynamical junction exists. It supplies a necessary condition for any model claiming the unscaled law inside a finite patch. Passing the condition supplies only budget compatibility.

## Bounded representative calculation

`budget_bound_v2.py` executes the same actual source prefixes as the earlier mass audit and evaluates the eight saved grid indices 0, 80, 120, 160, 200, 240, 280, 320 at four redshifts and both footings: **64 distinct halos, two source conventions, 128 rows**. This is representative coverage, not the complete 321-mass population.

The budget is the cosmic patch cold amount `Q=(1-FB)Mta/h` in physical Msun. The sources are (1) FRZ1's retained central source on galaxies and its distributed Bar source on clusters, and (2) all explicit Bar baryons. On clusters these two source choices coincide and neither silently includes the nominal baryons in the outer NFW envelope. The roots use the actual analytic baryon profiles, not interpolation between saved radial samples. Saved profiles check the independently evaluated source values.

For each row the calculation tests nondecreasing b and C on 1,001 radii, evaluates the pointwise inequality, and—when a crossing occurs inside rta—solves both `C/Q-1=0` and the normalized quadratic budget equation. The fixed-source galaxy root is also checked against the closed formula. If no crossing occurs inside rta, the reported maximum inside-patch radius is rta and the crossing field is empty. There are **76 inside-patch crossings among the 128 source rows**; the other 52 are explicitly marked as no interior crossing.

All radii below are physical kpc; these selected examples are slow galaxy-branch halos in the actual JNT2 model.

| z | M200m (Msun/h) | footing | retained-source R_budget | all-Bar R_budget | actual R_set at f=3 | rta |
|---|---:|---|---:|---:|---:|---:|
| 0 | 10^12 | canonical | 430.277 | 194.190 | 447.329 | 1076.532 |
| 0 | 10^12 | alt | 391.457 | 180.092 | 447.229 | 1076.532 |
| 2.2 | 10^11 | canonical | 159.783 | 68.937 | 75.816 | 221.070 |
| 2.2 | 10^11 | alt | 145.366 | 63.977 | 75.787 | 221.070 |
| 3 | 10^11 | canonical | 168.265 | 70.095 | 55.882 | 185.827 |
| 3 | 10^11 | alt | 153.083 | 65.055 | 55.855 | 185.827 |
| 4.4 | 10^10 | canonical | 54.841 | 23.396 | 11.057 | 65.859 |
| 4.4 | 10^10 | alt | 49.893 | 21.731 | 11.057 | 65.859 |

The z=0 example at f=3 exceeds both source-specific raw-law budget limits. At z=2.2, f=3 is below the retained-source limit but above the all-Bar limit. At z=3 and z=4.4, f=3 fits both budgets in these examples. Thus the source convention changes the test materially. None of these statements promotes a passing radius into a derived physical boundary.

The source reconstruction differs from the saved profiles by at most 1.02e-16 of Q. Two root formulations agree to 9.92e-13 relative; the maximum root charge residual is 1.02e-12. Closed fixed-source and numerical radii agree to 4.89e-15. The degenerate zero-source check passes.

## Provenance and review

- `run_005` is preserved as a failed v2 record: numerical checks finished, then JSON serialization rejected a NumPy boolean. It is not successful numerical evidence.
- `budget_bound_v2.py` changes only row scalar serialization. `run_006/manifest.json` is the successful v2 record, status `completed`, with its own before/after hashes. `run_006/results.json` and `budget_bounds.csv` contain the results.
- Algebra and domains were independently checked by `/root/independent_final_review`; the initial review found no gap and specifically checked r>0 for strict radial positivity, the b=0 case, and no-crossing patches. This document's mathematical prose was self-proofread.
- Proof dependencies are internal algebra and the stated spherical-law/source conventions; finite numerical checks use the original model code. No external theorem or observational result is needed for the inequality.

Reproduce into a fresh directory:

```bash
python3 codex_mass_budget_2026_11_14/calculation/reproduce.py --stage 5 --run-name reproduce_budget_bound
```
