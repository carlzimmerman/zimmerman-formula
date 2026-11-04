# Independent audit of cutoff p=6 constitutive monotonicity

**Claim.** For all real y>0 and t>=3/2, define

    s(y) = (sqrt(1+4/y)-1)/2,
    nu(y) = 1+s(y) exp[-(y/t)^6].

Then `nu(y)>1`, `nu'(y)<0`, and `nu(y)+y nu'(y)>0`.

**Primary verdict: proved as written.** This is a computer-assisted exact
rational certificate on a compact interval, combined with valid analytic
reductions covering both tails and every allowed t. No mathematical gap was
found in the reviewed proof or script. The conclusion concerns this exact
constitutive function. It is not a proof of dynamical stability, relativistic
health, observational success, or the accuracy of a floating-point field solver.

This is an independent reconstruction by the sibling audit agent, not a review
of its own proof or implementation. The existing bounded run was inspected and
its manifest validated. No independent rerun of the full rational certificate
was performed; its arithmetic result is accepted only after code review and
provenance validation. No frozen input was edited.

## Dependencies and obligation matrix

The proof chain is:

1. Exact response definition -> formula for its total radial slope F.
2. Reparameterization z=(y/t)^6 -> increasing F in t on z>=1/12.
3. Elementary inequalities -> positive lower and upper tails.
4. Exact rational root and exponential enclosures -> interval lower bound.
5. Complete interval enumeration plus positive recorded minimum -> compact proof.
6. Union of the three regions -> all y>0 and t>=3/2.

The leaves are internal elementary analysis, exact integer/rational arithmetic,
the reviewed program, and its recorded completed run. No external theorem or
floating transcendental evaluation is load-bearing.

| Obligation | Assessment |
|---|---|
| Positivity of nu-1 and negativity of nu' | passed for exact finite y,t |
| Derivative identity for F | passed, independently differentiated |
| Quantifiers under the z substitution | passed; bijective y>0 <-> z>0 at each fixed t>0 |
| Reduction to t=3/2 on z>=1/12 | passed; monotonicity is at fixed z, which suffices |
| Small-z tail for every t>=3/2 | passed with strict positive margin |
| Large-z tail and rational Taylor bound | passed |
| Sixth-root and square-root enclosure direction | passed |
| Exponential lower/upper enclosures | passed for the whole declared domain |
| Product signs and interval negative-term maximization | passed |
| Contiguous compact coverage and exact count | passed, no sampling gap |
| Exact run result and input provenance | passed; completed manifest validates |
| Literal global strict inequalities in rounded numerical implementation | not claimed or established |
| Other powers, t<3/2, dynamics, or data fit | out of scope |

## Analytic reconstruction

From `s(s+1)=1/y` one obtains

    y s'(y) = -s(s+1)/(2s+1),
    s+y s' = s^2/(2s+1) = B(s).

Since `y z'=6z`, independent differentiation gives

    F(z,t) = d[y nu(y)]/dy
           = 1+exp(-z)[B(s)-6zs],
    y=t z^(1/6).

Both factors in the excess are positive and strictly decreasing with y.
Their derivative sum is strictly negative, proving the other two assertions
without relying on the F certificate.

The derivative of B is

    B'(s)=2s(s+1)/(2s+1)^2
         =1/2-1/[2(2s+1)^2] < 1/2.

For z>=1/12, `B'(s)-6z<0`, including the endpoint. At fixed z, increasing t
increases y and decreases s. Therefore F increases with t, and a lower bound
at t=3/2 is valid for every t>=3/2 in this region. This is not an assertion
about increasing t at fixed physical y; that stronger assertion is unnecessary.

For 0<z<=1/12, `s<1/sqrt(y)<z^(-1/12)` because t>=3/2>1. Positivity of B
and `exp(-z)<1` give

    F > 1-6zs > 1-6z^(11/12)
      >= 1-6(1/12)^(3/4) > 0.

The middle inequality uses z<1 and 11/12>3/4. The last is equivalent to
`6^4<12^3`, namely 1296<1728, so it is exact. No near-zero field was omitted.

For z>=10 at t=3/2, y>1/2 implies s<1. Since `z exp(-z)` decreases for z>1,

    F > 1-6z exp(-z) >= 1-60 exp(-10).

The exponential Taylor partial sum is exactly
`1+10+10^2/2+10^3/6+10^4/24=1933/3`, with a positive remainder. Hence
`F>1-180/1933=1753/1933>0`. The fixed-z t reduction covers all larger t.

## Exact implementation audit

`root_bounds(x,k)` scales x by D^k with D=10^10, floors the resulting rational,
and finds the integer kth-root floor. It then returns n/D and (n+1)/D and
explicitly checks their kth powers bracket x. The integer root bisection starts
with an upper power-of-two bound strictly above the positive input's root;
its loop retains the root bracket and terminates at adjacent integers.
The square-root path uses Python's exact integer `isqrt`. No float conversion
enters any enclosure.

For z>0, root bounds `r_lo<=z^(1/6)<r_hi` give the reversed reciprocal bounds

    1+4/[(3/2)r_hi] <= 1+4/[(3/2)z^(1/6)]
                     <= 1+4/[(3/2)r_lo].

The subsequent square-root enclosures and subtraction/division therefore give
valid s bounds. The denominator r_lo is positive throughout z>=1/12. The lower
s bound is nonnegative: the enclosed square-root argument exceeds one, so its
integer square-root floor at decimal scale is at least D. Thus multiplying
positive lower bounds in the B term is legitimate.

For 0<=x<=10 and N=128, both bases are positive and

    (1-x/N)^N <= exp(-x) <= (1+x/N)^(-N).

The directions follow respectively from `log(1-v)<=-v` and `log(1+v)<=v`.
Integer exponentiation and negative integer powers of Fraction objects remain
exact rational operations.

On a closed interval [a,b], s decreases and B increases with its argument, so
the positive term is at least `L(b) B(s_lower(b))`. The function
`x exp(-x)` reaches its maximum at m=1 if 1 belongs to the interval, at b if
b<1, and at a if a>1. Therefore the negative term is bounded below by
`-6 m U(m) s_upper(a)`. Combining these independent bounds gives exactly the
implemented enclosure

    F >= 1+L(b) B(s_lower(b))-6 m U(m) s_upper(a).

No sign-sensitive step reverses an inequality. Although independently bounding
the terms loses sharpness, it cannot invalidate this lower bound.

The loop starts at 1/12, assigns `b=min(a+1/500,10)`, and updates a=b using
exact fractions. Every right endpoint is the next left endpoint, so there are
no holes. The first 4,958 intervals have full length; the final interval has
length 1/1500 and ends exactly at 10. Thus the count is
`ceil((10-1/12)*500)=4959`, matching both the assertion and saved result.
The endpoints overlap the analytic tail regions and are also included in
the compact certificate.

The saved exact minimum is positive. The shorter fraction obtained by flooring
it to six decimal places is checked to lie below it and equals

    23487/1000000 = 0.023487.

Its worst enclosing interval is `[347/375,1391/1500]`. This is a lower bound
for the compact region, not a claimed accurate numerical value of the true
minimum. The exact fraction is retained in the result file.

## Scope and numerical implementation

`response.py` uses the same mathematical excess and derivative formulas for
the cutoff family. Its vectorized implementation floors tiny y, clips the
logarithmic exponent, and uses finite-precision exponentials. At large y the
excess can underflow and nu can round to one, so the exact strict inequalities
`nu>1` and `nu'<0` must not be asserted literally of every rounded output.
The proof explicitly separates its exact constitutive claim from those
floating-point implementation tests; that separation is correct. The cutoff
power is exactly six and the certified parameter domain is t>=3/2 only.

Positivity of `d[y nu]/dy` is one constitutive property of the radial response.
It does not by itself establish positive energy of every dynamical mode,
well-posedness of a relativistic theory, or preservation of an observational
fit after changing the response.

## Provenance and remaining gap

No mathematical gap remains for the stated exact claim. The trusted computation
base is Python integer/Fraction arithmetic, the reviewed script, and the saved
bounded execution; an independent rerun could add implementation provenance
but is not required to repair an identified defect.

The reviewed shared HEAD was `7f4f3e98ceee243769e33f63c4143d912c1cef42`.
The exact audited inputs/results have SHA-256:

- `response/MONOTONICITY_PROOF.md`: `9ec220587c32dc72fca9920300cc6fa4d9262560e5241276a394c893868a64b1`
- `response/monotonicity_exact.py`: `be42e453d6195ffb5dc597b0c1bdd4ba166c7c659d5f3b583fa4268ce315e899`
- `response/monotonicity_001/results.json`: `9a3e7a1aab84e5eca2aad39b08a1b20501c608bc7f0c05367d24212fdeffa90c`
- `response/monotonicity_001/manifest.json`: `74ab1fa9400809deef2a3b0b60ef72451453541ec1326f7b4f3c094800a10cef`

Validation used the installed mathbox computation-audit command:

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py rebuild_2026_10_22/KT36_action_response_search/response/monotonicity_001/manifest.json --root "$PWD"

It returned a valid evidence record with run status `completed`. Final
self-proofreading covered this audit's formulas, inequalities, domains,
coverage count and nonclaims; no mathematical tokens in the reviewed proof or
program were changed.
