# A36 — mutation record

## `--mutate` : drop the `(1+2w^2)` rescaling of the clock source

The load-bearing step of the lane is K2/K3: the foliation lapse carries `w^2(Phi+Psi)`, so the
clock source `S = Pbar.D ln N` is multiplied by exactly `(1+2w^2)`, and that is what makes the P
charge — and therefore the `1/r` part of the potential — frame-dependent in the MOND regime.

The mutation sets that rescaling to zero (`RSCALE = 0`) and leaves everything else untouched.
Nothing else in the script is changed: same background, same propagator, same lapse equation,
same numbers, same thresholds.

Command:

```bash
python3 a36_checks.py --mutate        # exit 1
```

Captured output: `mutate.out`. The checks that break:

| id | clean | mutated |
|---|---|---|
| K7 | `gal = -4*up/(up-1)` (i.e. `4u'/(1-u')`) | `gal = 0` — **FAIL** |
| K8 | `min \|alpha_1\| = 7.34e-02` at 1 kpc | `0.000e+00` — **FAIL** |
| K9 | `max \|alpha_1\| = 5.194` at 30 kpc | `0.000` — **FAIL** |
| K14 | route(b)/route(a) in `[0.58, 7.32]` | `[inf, inf]` — **FAIL** |

9/13 pass under the mutation, so the mutation is *specific*: it kills exactly the checks that
depend on the effect and leaves the kinematic identities (K1-K3), the algebra of the response
(K5, K6) and the numerical machinery (K10-K13) intact. That is the signature of a check with
teeth rather than a script that fails for an unrelated reason.

## What the mutation demonstrates

`alpha_1` in this theory is *entirely* the `(1+2w^2)` rescaling of the clock source acting on a
charge whose potential is `1/r`-like. Remove the rescaling and `alpha_1 = 0` in every regime,
including the galactic one — which is precisely the claim the framework makes and which this lane
falsifies. There is no second, independent contribution at `O(w^2 eps)`: K1's inventory shows that
`E^2` (the only shift-mixing operator) is `O(w^2 eps^2)` on a static background, `W` gives only a
`Phi`-tadpole with no `1/r`, and `(D.P)^2` and `F^2` carry no `N^i` and no `w`-dependence.

## Second mutation considered and rejected

Setting `E^2`'s mixing coefficient to zero changes nothing (K1 still reports one mixing operator,
K5-K14 are unaffected), because `E = 0` on the static galactic background. That is a *negative*
control: it confirms that the shift sector — the operator the task flagged as the likely culprit —
is not the one that produces `alpha_1`. Recorded here so the negative result is not mistaken for
an untested assumption.
