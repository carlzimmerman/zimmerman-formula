# Flat positive gates: the unrestricted-state obstruction

This analytic extension depends on the GR-inclusive finite-center principal reduction in `DERIVATION.md` section 4. The [independent audit](../health_audit/RESULT.md) supports the reduction on its stated regular-center, nondegenerate, classical-continuum domain and independently checks this calculus lemma. It is not a claim that observed halos or the cosmological solution visit every mathematically allowed state.

## Curvature lemma

Let S be C2 on `[0,infinity)`, strictly positive, nonincreasing, nonconstant, and `S'(0)=0`. Then there exists u>0 with

```text
S'(u)<0,     0<S''(u)<S'(u)^2/[2S(u)].                       (1)
```

Proof. Nonconstancy and monotonicity give a point a with `g(a)=S'(a)<0`. There is b>a with `g(b)>g(a)`; otherwise `S(t)<=S(a)+g(a)(t-a)` eventually becomes negative. Let c be the last minimizer of g on the compact interval `[0,b]`. Since g(0)=0 and g(b)>g(a), c is strictly interior, g(c)<0 and `g'(c)=S''(c)=0`. Positive g' occurs arbitrarily close to the right of c: if g'<=0 throughout any such interval, g could not rise above its minimum, contradicting the choice of the last minimizer. Choose points approaching c with g'>0. Continuity gives g'->0, while `g^2/(2S)` tends to a strictly positive value. One sufficiently close point satisfies (1). QED.

The strict positivity assumption matters: a gate that becomes identically zero may require a separate analysis at its zero/degenerate phase. The lemma does not assume analyticity, a particular exponential shape or a measured density threshold.

## Consequence for the quadratic clock family

Fix any finite positive C and Pi_c and finite gamma>=0. At a u satisfying (1), put `p=u Pi_c` and let q increase through finite positive values. For `H=C(q-1)^2 S`, the exact coefficients are

```text
A0 = 2C q^2 S,
D = C(q-1)^2 S''/Pi_c^2 - gamma,
c = 1+gamma p + C(q^2-1)S'/Pi_c,
A_infinity = A0-c^2/D.
```

Therefore

```text
lim_(q->infinity) A_infinity/(Cq^2) = 2S-S'^2/S'' < 0,
lim_(q->infinity) n_eff/(Cq^2) = 2S-uS' > 0,
lim_(q->infinity) rho/(Cq^2) = S > 0.
```

At sufficiently large *finite* q, D>0, A_infinity<0, n_eff>0 and rho>0. The regular local constraint construction (3)–(4) in the derivation applies at each such finite state. The bounded amplitude `K|P|<a0` is respected by taking a sufficiently small regular patch; it does not impose a bound on the central divergence p or on q. The resulting scalar characteristic has `omega^2~(n_eff/A_infinity)k^2<0` if the principal reduction holds.

Thus no member of this strictly positive flat-origin gate family, with the specified quadratic clock and fixed finite stiffness, is healthy on **every unrestricted admissible local state and arbitrarily short wavelength**. A preserved restricted state domain, an independently justified ultraviolet domain, a non-quadratic clock kinetic term or a changed stiffness/action can alter this conclusion. None is supplied by the unrestricted action alone. This statement does not exclude every modified-gravity theory or every phenomenologically selected solution.

## The weak-offset flat exponential check

For `S=exp(-u^3)`, let t=u^3 and `r=H_Q/Pi>0`. At q->1+ with gamma effects negligible,

```text
c = 1-3tr + higher-order offset/stiffness terms,
A0 D = (r^2/2)(9t^2-6t) + higher-order terms.
```

At u=t=1 this gives

```text
A_infinity/A0 = 1-(1-3r)^2/(1.5r^2).
```

It is negative for `r<(6-sqrt(6))/15` or `r>(6+sqrt(6))/15`, approximately `.236700684` and `.563299316`. The intermediate interval merely passes this high-k sign test. The numerical witness uses the exact, finite-offset and positive-stiffness formulas, not this approximation. The ratio must be evaluated on an actual constrained background before making an astrophysical statement; insertion of an undeformed trial AQUAL profile is not such a solution.
