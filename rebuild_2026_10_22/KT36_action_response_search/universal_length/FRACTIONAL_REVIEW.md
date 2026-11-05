# Independent review: fractional cutoff monotonicity

Claim reviewed: for the exact rational p=63/10 and every real t>=3163/2000,

```
nu(y)=1+s(y) exp[-(y/t)^p],
s(y)=(sqrt(1+4/y)-1)/2,
```

satisfies nu>1, nu'<0, and d[y nu]/dy>0 for every y>0.

**Primary verdict: proved as written.** The analytic reduction and the exact
rational compact certificate are correct under the usual exact-integer
arithmetic model. This is a constitutive theorem, not dynamical stability,
relativistic health, an observational pass, or closure of the parameter family.

Reviewer: sibling `cassini_sign_route`, 2026-11-04. The review independently
reconstructed the inequalities and inspected the raw implementation. The
new execution is a replay of that audited implementation, not an independent
second certificate implementation.

## Dependency graph and obligations

The proof uses only the stated scalar definition, elementary calculus,
positive-root enclosures, and finite exact rational inequalities:

```
definition -> s(s+1)=1/y and derivative identity
           -> F(z,t)=1+exp(-z)[B(s)-p z s]
           -> analytic small-z tail
           -> monotonicity in t for z>=1/(2p)
           -> analytic large-z tail
           -> compact exact interval certificate at t=3163/2000
           -> F>0 for all y>0 and all admitted t.
```

| Obligation | Finding |
|---|---|
| Scalar domain and exact rational parameters | passed |
| nu>1 and nu'<0 | passed directly from s>0, s'<0, p>0 |
| Differentiation and B(s) | passed |
| Monotonicity in t at fixed z | passed |
| Small- and large-z analytic tails | passed |
| Rational root and exponential enclosures | passed |
| Exhaustive compact interval coverage | passed; 4,961 adjacent intervals |
| Strict positivity on each compact interval | passed; replay completed |
| Original contract's conventions | failed locally: copied p=6 text |
| Correctly stated replay provenance | passed; fresh manifest validated |
| Floating implementation/observational predictions | out of scope |

There is no external theorem leaf or circular dependency. The exact
computation supplies only the compact inequality; the analytic argument is
essential for the unbounded y and t quantifiers.

## Independent derivation

Differentiating s(s+1)=1/y gives y s'=-s(s+1)/(2s+1). Thus, with z=(y/t)^p,

```
F=d[y nu]/dy=1+exp(-z)[B(s)-p z s],
B(s)=s^2/(2s+1),
B'(s)=1/2-1/[2(2s+1)^2] < 1/2.
```

At fixed z, y=t z^(1/p) increases with t and s decreases. If z>=1/(2p),
then B'(s)-p z<0, so F increases with t. The endpoint t0 is therefore
the worst case in that entire region; this does not assume monotonicity at
fixed y, which would be a different assertion.

For 0<z<=1/(2p), s<1/sqrt(y)<z^(-1/(2p)), since t>1. Discarding the
positive B term and replacing exp(-z) by 1 only in the negative term gives

```
F>1-p z^(1-1/(2p))
 >=1-p(2p)^(-3/4)
 =1-(p/8)^(1/4)>0.
```

The exponent comparison requires p>=2 and z<1, both satisfied. For z>=10,
s<1 and z exp(-z) decreases, giving F>1-80 exp(-10)>1693/1933>0.
The latter inequality follows from the positive Taylor polynomial
exp(10)>1933/3. These tails include the compact endpoints with slack and
leave no uncovered limiting case. The singular point y=0 is correctly
excluded from the claim.

## Exact compact certificate audit

At p=63/10, z^(1/p)=z^(10/63). The implementation first encloses the
positive 63rd root by adjacent decimal rationals and then raises the
positive endpoints to power 10. The reciprocal and square-root bounds in
s reverse or preserve order correctly. Each root enclosure is checked by
integer-power inequalities against the original Fraction; no floating
transcendental approximation enters the certificate.

For 0<=x<=10 and N=128,

```
(1-x/N)^N <= exp(-x) <= (1+x/N)^(-N).
```

The bases are positive. The proof correctly uses the lower exponential bound
at the upper interval endpoint for the positive B term, and the upper bound
at the maximizer of x exp(-x) for the negative term. B is increasing in s,
and s decreases in z. Therefore its interval lower expression is a valid
lower bound on F throughout the interval, including both endpoints.

The iterator starts at 5/63, advances by exactly 1/500 using Fractions,
shortens only the last interval, and asserts the final endpoint is exactly
10 and the count equals the exact ceiling of interval length divided by
step. All 4,961 intervals are visited; no sample/filter substitutes for
coverage. Every bound is asserted strictly positive. The recorded common
compact lower bound is 12671/1000000, obtained by rounding the exact minimum
fraction downward and explicitly comparing it with that fraction.

## Provenance defect and corrected replay

The original `response/contract_monotonicity_fractional.json` contains a
stale conventions string with exponent 6 and coefficient 6. Its assertion,
bound parameters, code, proof, and output all instead specify 63/10. This
is a real local metadata contradiction; it does not invalidate the inspected
algebra or the computation actually performed. The original pinned contract
was retained unchanged, and the author was notified.

The new `fractional_review_contract.json` states the fractional formula
correctly. `fractional_review_001/manifest.json` completed and validates
against its input hashes. Its output is exactly equal to the original
fractional result, including the complete minimum fraction and worst interval.
It records the original contract as an input, preserving the discrepancy
rather than silently rewriting history.

Exact reviewed source hashes:

```
FRACTIONAL_MONOTONICITY_PROOF.md
  6ba2b6e11c5cc399aa91ef648299e96ac84630101d6a57c220ba42690bb12b27
monotonicity_fractional.py
  b7373c4886c9136821ca0605e9c17b27887ef30face9747108d2ef53551f08f2
monotonicity_exact.py
  be42e453d6195ffb5dc597b0c1bdd4ba166c7c659d5f3b583fa4268ce315e899
```

No mathematical gap remains in the stated constitutive theorem. The theorem
concerns exact rational p and the exact real function; floating response
evaluation, numerical Solar/MW integrals, other parameter values, and global
viability require their own evidence. A finite observational parameter miss
must not be promoted to an exclusion of this entire response family.
