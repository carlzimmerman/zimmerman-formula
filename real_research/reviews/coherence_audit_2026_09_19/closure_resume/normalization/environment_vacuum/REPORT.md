# Positive environmental vacuum: sharp area bound and a finite healthy construction

This is a separate follow-up to the original normalization audit. The previous report and computation record are unchanged. Base commit: `23d3890790291c0ec44b4ca7da784a806d7094d2`, with a dirty shared workspace. The evolving environment agent's source was copied byte-for-byte into `environment_source_snapshot.py`; `source_provenance.json` records its original path and SHA-256, and the run manifest pins the snapshot.

**Claim under test.** In the action sector `S=(16 pi Gbare)^(-1) integral sqrt(-g)[R+f(X)]`, let `X=g^2=a_i a^i`, `alpha=f_X`, with positive transverse and longitudinal coefficients `alpha>0` and `alpha_L=alpha+2X alpha_X>0`. Can a decreasing interpolation from `alpha_hi≈1/2` to `alpha_lo≈10^-7`, with the empty high-acceleration prescription `f(X)-alpha_lo X -> 0`, generate a positive vacuum and derive `kappa=1/2` from the same MOND scale?

**Primary verdict: incomplete, with the exact missing implication isolated.** The vacuum sign is positive, and a finite, smooth, strictly healthy interpolation exists. However, a sharp area bound forces a small coefficient if the acceleration at which `alpha` remains order one is identified with `a0`. An explicit interpolation with no independent ratio between its two turnover scales predicts `kappa≈0.00253` when its initial scale equals `a0`. Obtaining one half requires an additional relation between scales. Principal positivity alone does not forbid one half: a controlled undershoot of the asymptotic coefficient evades the bound, but then fixes the vacuum by an unexplained cancellation.

These statements concern the displayed action sector and its two principal coefficient conditions. They do not certify the complete coupled action, PPN, the tensor cone, cosmological perturbations, or the required MOND shape.

## 1. Sign and convention, derived with the lapse

Write `a=alpha_lo>0` and `h(X)=alpha(X)-a`. When `I=integral_0^infinity h(X)dX` is finite, the specified boundary condition uniquely sets

```text
f(X)=a X-integral_X^infinity h(s)ds,
f(0)=-I.
```

At homogeneous `X=0`, the action density is `Lvac=-N A(t)^3 I/(16 pi Gbare)`, where `A(t)` denotes the FLRW scale factor. Retaining and varying `N` gives

```text
rho_vac=I/(16 pi Gbare),
Lambda_eff=8 pi Gbare rho_vac=I/2.
```

Thus `I>0` indeed gives positive vacuum energy. The sign differs from the earlier attractive scalar-carrier primitive, and that earlier sign obstruction must not be transferred here.

If the coefficient uses `Gbare`,

```text
kappa_bare=sqrt(8 pi) a0/sqrt(Lambda_eff),
kappa_bare^2=16 pi a0^2/I.
```

The same environment source's static high-acceleration normalization instead gives `G_N/Gbare=2/(2-a)`. If the empirical coefficient uses measured `G_N`, its exact expression is

```text
kappa_N^2=8 pi (2-a) a0^2/I.
```

The fractional correction is only `a/2` in the squared coefficient at the proposed small `a`, but it is retained in every numerical result below. Therefore `kappa_N=1/2` requires `I=32 pi(2-a)a0^2`.

## 2. Sharp profile-independent area lower bound

Let `g0>0` and `alpha(g0^2)=A>a`. Since

```text
sigma(g)=g alpha(g^2),
sigma'(g)=alpha_L(g^2)>0,
```

one has `alpha(g^2)>A g0/g` for `g>g0`. Assume first that `alpha>=a` everywhere. For `g0<=g<=A g0/a`, this forces the positive area

```text
I >= 2 integral_g0^(A g0/a) g [A g0/g-a] dg
  = g0^2 (A-a)^2/a.
```

This tail-only result does not assume monotonicity of `alpha` itself. If `alpha` is also nonincreasing, its inner area is at least `(A-a)g0^2`, giving the sharpened bound

```text
I >= g0^2 A(A-a)/a.
kappa_N^2 <= [8 pi(2-a)a/(A(A-a))] (a0/g0)^2.
```

Strict health makes equality unattainable, but the bound is the sharp infimum. To prove sharpness, fix `0<epsilon<1` and use the continuous piecewise profile

```text
alpha(g^2)=A,                                      0<=g<=g0,
          epsilon a+(A-epsilon a)g0/g,             g0<g<ge,
          a,                                      g>=ge,
ge=(A-epsilon a)g0/[(1-epsilon)a].
```

It has `alpha_L=A, epsilon a, a` in the respective regions, and exactly

```text
I_epsilon=g0^2(A-a)(A-epsilon a)/[(1-epsilon)a]
          -> g0^2 A(A-a)/a as epsilon -> 0+.
```

The corner derivatives can be smoothed without losing positivity or approaching a different infimum. One precise construction is convolution in `t=log g` by a positive smooth kernel: both linear inequalities `alpha_t<=0` and `alpha+alpha_t>0` are preserved, constant end regions remain, and the weighted integral tends to its original value as the convolution width shrinks. The piecewise formula is a sharpness witness, while the next section supplies a fully explicit globally smooth profile.

At `A=1/2`, `a=10^-7`, and `g0=a0`,

```text
kappa_N < 0.00448399330942.
```

One half therefore needs `a0/g0>111.507748896`. This bound applies at a point where the coefficient still equals one half. A smooth profile with `alpha(0)=1/2` need not reach exactly one half at any positive `g0`; for that profile one must substitute its actual `alpha(g0^2)`. The sharp result is a scale/amplitude tradeoff, not an assertion that the value at the origin alone bounds an otherwise unspecified transition scale.

The same inequality also quantifies an early drop: if `g0=a0`, obtaining one half requires

```text
A(A-a) <= 32 pi(2-a)a,
A <= [a+sqrt(a^2+128 pi(2-a)a)]/2.
```

At `a=10^-7` this upper limit is about `0.00448404`, so an order-one coefficient cannot remain until `g=a0`.

## 3. Globally smooth finite-integral profile

Let `Delta=alpha_hi-a>0`, choose `B>0`, and set

```text
C/B=Delta/a > 1,
alpha(g^2)=a+Delta/[sqrt(1+g^2/B^2)(1+g^2/C^2)].
```

It is smooth in `X=g^2`, strictly decreasing, equals `alpha_hi` at the origin, and approaches `a` with excess proportional to `g^-3`. Its two scales are tied by the endpoint coefficients, so `C/B` is not an independent parameter in this construction.

Direct differentiation gives

```text
alpha_L=a
 +Delta/[(1+g^2/B^2)^(3/2)(1+g^2/C^2)]
 -2 Delta g^2/[C^2 sqrt(1+g^2/B^2)(1+g^2/C^2)^2].
```

Use `sqrt(1+g^2/B^2)>=g/B`. With `t=g/C`, the magnitude of the negative term is at most `(Delta B/C) 2t/(1+t^2)^2`. The latter dimensionless function has unique positive maximum `3sqrt(3)/8` at `t=1/sqrt(3)`. Hence

```text
alpha_L >= a[1-3sqrt(3)/8] > 0
```

for every `g`. This is an analytic bound, not a sampled stability test.

With `r=C/B>1`, direct integration gives

```text
I=2 Delta B^2 r^2 atan(sqrt(r^2-1))/sqrt(r^2-1)
  ~ pi Delta B^2 r = pi Delta^2 B^2/a.
```

The antiderivative and endpoint relation are checked exactly. For `alpha_hi=1/2`, `a=10^-7`,

| Quantity | Result |
| --- | --- |
| `C/B` | `4,999,999` |
| `I/B^2` | `7,853,977.49238` |
| `kappa_N`, taking `B=a0` | `0.00252982273191` |
| `kappa_N`, taking `B=bV` | `0.00337309680722` |
| Required `B/a0` for `kappa_N=1/2` | `0.00505964546381` |

The `bV` identification uses the environment source's own scalar-flux calibration: `b=d/(2-alpha_hi)` and `a0=d(2-a)V/(2-alpha_hi)^2`, so `bV/a0=(2-alpha_hi)/(2-a)`. Replacing the environment profile by a smooth even-in-`g` function with the same endpoints preserves the leading deep-MOND cancellation and its `g^2` coefficient; its first correction from `alpha` is of order `g^3`. This observation does not guarantee the transition kernel or all coupled principal conditions.

Unlike the `p=1/2` profile, this finite profile has `g(alpha-a)->0`. It therefore removes the clock-acceleration contribution to the *asymptotic constant force residual*; the scalar sector's residual remains to be derived from its own action. It also takes a very long range in acceleration to reach the small asymptotic coefficient. These consequences must be included in any environmental screening comparison.

The construction also preserves the environment source's coupled principal-matrix sufficient condition. Indeed `alpha_L<=a+Delta=alpha_hi` from the displayed positive-minus-negative decomposition, while `alpha_T=alpha<=alpha_hi`. Every directional coefficient therefore satisfies `0<alpha_theta<=alpha_hi`. For its retuned scalar kernel `B_theta>=b=d/(2-alpha_hi)`, set `Ahi=2-alpha_hi`, `deltaA=(2-alpha_theta)-Ahi>=0`, and `deltaB=B_theta-b>=0`. Then exactly

```text
(2-alpha_theta) B_theta-d
   = Ahi deltaB+b deltaA+deltaA deltaB >= 0.
```

The frozen dynamic spatial determinant differs from this by the positive factor `2d/alpha_theta`; the source's kinetic assumptions are unchanged. This transfers the existing static and frozen principal-symbol sufficient condition, including its designed zero-gradient MOND degeneracy. It does not establish finite-wavelength cosmological health or a complete nonlinear Dirac analysis.

The construction answers the existence question positively but does not derive one half. The additional identification `B/a0≈0.00505965` is precisely the missing physical relation, rather than a numerical result supplied by principal health.

## 4. A genuine escape from the bound, with its cost exposed

The condition `alpha>=a` is essential. To see this constructively, start from the smooth profile above and let

```text
w(t)=16(t-1)^2(2-t)^2 for 1<=t<=2, and zero otherwise,
alpha_new(g^2)=alpha(g^2)-eta a w(g/L),
eta=1/100.
```

The bump and its first derivative vanish at the endpoints. On its support, `0<=w<=1`, `|w'|<=8`, and `|w+t w'|<=17`. Thus

```text
alpha_new >= a(1-eta)>0,
alpha_L,new >= a[1-3sqrt(3)/8-17eta]
             = a[83/100-3sqrt(3)/8]>0.
```

The profile is `C^1` in `g`, including the compact-support joints; consequently the principal coefficients are continuous. It can be made smoother with a positive compact convolution if desired, preserving the strict margins. This explicit example is already sufficient for the displayed first-gradient action's classical coefficients.

Its area changes by the exact amount

```text
Delta I=-eta a L^2 integral_1^2 2t w(t)dt
       =-(8/5) eta a L^2.
```

The core and asymptotic endpoint coefficients are unchanged, while varying `L` continuously lowers the vacuum area through any desired smaller positive value and eventually makes it negative. Principal positivity therefore cannot universally bound the coefficient once undershoot is allowed.

For the example with `B=a0`, selecting the area needed for one half requires

```text
L/a0=70,061,474.9277,
I_target/I_original=0.0000256000122195.
```

This cancels `99.9974399988%` of the original positive area. The exact location is obtained by solving `L^2=(I_original-I_target)/[(8/5)eta a]`; that equation transparently inserts the desired coefficient unless a further physical mechanism selects `L`. Thus this is a valid escape from a proposed universal no-go and an available constrained family for further research, but it is **not** a derivation of `kappa=1/2`.

## 5. What is established and what remains

| Obligation | Status | Evidence |
| --- | --- | --- |
| The proposed high-field subtraction produces positive vacuum | Passed for positive finite `I` | Independent lapse variation |
| Monotone principal health permits finite `I` | Passed | Explicit smooth profile with analytic uniform health bound |
| Such health allows arbitrary vacuum area at a fixed order-one core scale without an undershoot | Failed | Sharp area lower bound |
| The explicit endpoint-tied profile gives one half when `B=a0` or `B=bV` | Failed | Exact integral and coefficient |
| Principal positivity alone excludes one half | Refuted | Controlled compact undershoot family |
| An existing physical principle selects the remaining ratio or cancellation | Incomplete | No such equation supplied by the inspected action |
| Finite profile preserves the source's coupled principal-symbol sufficient condition | Passed under its stated scalar-kernel/kinetic assumptions | `alpha_theta<=alpha_hi` and the exact determinant decomposition |
| Full covariant model satisfies all remaining gravitational gates | Not addressed | Requires full coupled analysis beyond the principal symbol |

The next executable physical step is to propagate the finite profile through the environment agent's scalar-flux and full principal-matrix gates, then check whether a separately derived scale relation can coexist with the needed separation of cosmic and local invariants. This report supplies a finite profile suitable for that calculation. It does not invent a condition that fixes `B/a0`, or treat the undershoot location as derived merely because a desired coefficient can determine it.

## Reproduction

`check_environment_vacuum.py` verifies 31 exact identities and proof ingredients, with the inequality reductions written above. `run/results.json` includes exact expressions and 20-digit evaluations. `run/manifest.json` records source and output hashes, the full argv, base commit and dirty state, Python 3.9.6, SymPy 1.14.0, and limits. The run completed with exit zero in under one second; the version-2 manifest validated with `--root` and input freshness checks. No randomness, observational data, external downloads, or reference-cosmology matching is used. The result is exact within the stated algebraic domain; the numerical values summarize those exact formulas.
