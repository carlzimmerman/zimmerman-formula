# Quadratic perspective extension: independent bounded proof review

Reviewed 2026-09-26 from the transport lane. This addendum checks the
explicit proposed functional below. It does not replace or silently
change any source hash in [FINAL_HOST_REVIEW.md](FINAL_HOST_REVIEW.md).
No new numerical run, compiler result, or coupled-gravity theorem is
claimed.

## Claim and hypotheses

On a smooth compact connected closed leaf, retain smooth fixed `h`,
`N>0`, `b`, and `epsilon >= epsilon_min>0`, with `m>0`. Let
`A=V0 zeta>0` be a fixed constant. On positive mean-one functions define

```
H_Q[t] = integral N [m |Dt-b|^2 + epsilon/t + q(t)],
q(t) = A(t-1)^2,
<t>_h = 1.
```

The earlier fixed-data existence, uniqueness, smoothness and strict
positivity argument survives, with the multiplier bound changed as below.
The added term also strengthens the joint auxiliary/momentum Hessian.

## Multiplier and barrier calculation

Use the previous convex C2 regularization `f_delta` of `1/t`, allowing
all real `t` during regularized minimization. The regularized functional
is strictly convex and coercive on the mean-one affine H1 space. Its Euler
equation is

```
-2m div_h[N(Dt-b)] + N epsilon f_delta'(t) + N q'(t) + lambda = 0.
```

In particular the exact multiplier identity now includes the new term:

```
lambda = -<N [epsilon f_delta'(t) + 2A(t-1)]>_h.
```

The two pointwise inequalities needed for the estimate are

```
f_delta + t f_delta' >= 0,
q + t q' = A(3t^2-4t+1) = 3A(t-2/3)^2 - A/3 >= -A/3.
```

Integration and testing by `t-1` therefore give

```
lambda Vol_h
  = -integral N t [epsilon f_delta'(t)+q'(t)]
    -2m ||Dt||_N^2 + 2m <b,Dt>_N
  <= integral N [epsilon f_delta(t)+q(t)]
     + (A/3) integral N + (m/2)||b||_N^2
  <= integral N epsilon + (3m/2)||b||_N^2 + (A/3) integral N.
```

The final step compares the minimizing functional to `t=1`, using
`delta<1` and `q(1)=0`. Define

```
lambda_max,Q = [integral N epsilon + (3m/2)||b||_N^2
                + (A/3) integral N] / Vol_h,
C_Q = lambda_max,Q + 2m ||div_h(N b)||_infinity > 0.
```

Mean-one normalization ensures that a global minimum satisfies
`t_min<=1`, even before positivity has been established. Consequently
`q'(t_min)=2A(t_min-1)<=0`. At this minimum the Euler equation gives

```
N epsilon [-f_delta'(t_min)]
  = lambda + 2m div_h(N b) - 2m div_h(N Dt) + N q'(t_min)
  <= C_Q.
```

If `t_min<=delta`, then `-f_delta'(t_min)>=1/delta^2`. Choosing

```
0 < delta < min(1, sqrt(N_min epsilon_min / C_Q))
```

gives a contradiction. The minimizer thus solves the original equation,
and the same argument supplies

```
t_min >= sqrt(N_min epsilon_min / C_Q) > 0.
```

The domination identity `1/t-f_delta(t)=(1-t/delta)^3/t>=0` for
`0<t<delta` is unaffected by the added quadratic term. The regularized
minimizer is therefore a global minimizer of the original positive-domain
functional. Strict convexity ensures uniqueness. The positive separation
and fixed smooth coefficients allow the same elliptic bootstrap to a
smooth finite solution. All compactness and regularity claims retain the
fixed-data scope of the previous review.

## Joint momentum variation

If `epsilon=sum p_a^2/2+W`, with fixed smooth `W>=V0>0`, the pointwise
second variation in momentum increment `dp` and auxiliary increment `v`,
including the gradient term after integration, is

```
integral N [2m |Dv|^2
            + sum (dp_a-p_a v/t)^2/t
            + 2W v^2/t^3 + 2A v^2].
```

The added contribution is exactly `+2A v^2`. Thus this extension preserves
joint convexity and improves the fixed-data auxiliary curvature. It does
not by itself establish the full reduced gravitational kinetic signature,
time-dependent lapse bounds, constraint propagation, or global health of
the coupled common action. A cosmological-background calculation is a
separate test.
