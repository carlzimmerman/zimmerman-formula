# A14 — mutation

## What is mutated

`python3 a14_checks.py --mutate` adopts **the other distance bookkeeping**: under a
distance rescaling `D -> fD` it holds the baryonic velocities fixed and moves only
the radii, so that `g_bar -> g_bar/f` instead of staying invariant. It then applies
the same belief consistently to the scatter test, predicting a per-galaxy a0 scatter
of `1 x rms(e_D/D)` instead of `2 x rms(e_D/D)`, i.e. `a0 ∝ 1/f` instead of `a0 ∝ 1/f²`.

This is not a strawman. It is **exactly the convention lane A9 used** (A9 K2: "every
residual, every rms, every slope is invariant; only `a0` moves, as `a0 ∝ 1/D`"), and
it is a natural slip: if you treat the tabulated `V_disk`/`V_gas` columns as data
rather than as mass models evaluated at the adopted distance, moving the radius is
the only move you see. What it silently does is rescale the baryonic mass as
`M ∝ D` rather than `M ∝ D²`, which is not a distance change at all.

## Why the checks have teeth

`K4` refits the same galaxies with every distance multiplied by `f = 1.10` and asks
whether the recovered `a0` obeys `a0 f²/a0 = 1`. `K5` asks the same question a second,
independent way, with no rescaling: whether the *observed* per-galaxy a0 scatter
(0.207 dex) matches the scatter the published `e_D` predicts. Both are one-line
consequences of the same exponent, so a wrong exponent must break both — and it does.

## Mutated output (captured in `a14_MUTATE.out`)

```
K4  the distance scaling: a0 -> a0/f^2, by refitting rescaled data
        canon a0(f=1) = 6.61977e-11   a0(f=1.10) = 6.02761e-11   a0*f^2/a0 = 1.1018
        quad  a0(f=1) = 7.93973e-11   a0(f=1.10) = 7.22954e-11   a0*f^2/a0 = 1.1018
  K4   FAIL |a0 f^2/a0 - 1| = 0.1018 at f = 1.10 (canonical law)
        threshold: < 0.05

K5  the same exponent from the data's own scatter (no rescaling experiment)
        per-galaxy a0 spans 3.67e-11 .. 1.55e-10 (0.207 dex)
        published e_D/D: rms 0.242  (f_D=1: 0.29, f_D=2: 0.04)
        [MUTATE] adopting the 1/f bookkeeping, as A9 K2 did
        predicted scatter: p=2 -> 0.210 dex,  p=1 -> 0.105 dex,  measured 0.207 dex
        => the measured scatter is what p=2 predicts with ZERO intrinsic a0 scatter;
           p=1 would need 0.178 dex of intrinsic scatter on top.
  K5   FAIL measured 0.207 dex; adopted p=1 predicts 0.105, p=2 predicts 0.210
        threshold: closer to the adopted exponent and measured/pred < 1.35
```

Tail: `A14 COMPLETE: 11/13 checks PASS.` — exit code **1**.

## The size of the failure is the diagnostic

`a0 f²/a0 = 1.1018` is not a random 10% — it is **exactly `f`**, the signature of a
`1/f` scaling masquerading as a `1/f²` one. And K5's failure is not marginal either:
under the mutant the observed scatter (0.207 dex) is **twice** the prediction
(0.105 dex), which is what "the data already know the exponent" looks like.

## What the mutation does *not* break

K1/K2 (the sample and its depth), K3 (the Upsilon lever), K6–K12 (the a0 values,
the kappa grid, the budget, the forecast, the robustness scans) are unaffected,
because the mutation only touches the distance transformation, which the primary
fit does not use. That is the point of separating the two: **the a0 measurement and
the distance systematic are independent statements**, and the mutation shows that
the second one is separately falsifiable by the data.
