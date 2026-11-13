# Independent audit of the flat-gate curvature lemma

**Verdict: correct only after a stated restriction:** the gate is nonconstant
and defined positively on the entire half-line, as in the precise theorem below.
The often stronger flatness condition S''(0)=0 is unnecessary.

## Precise theorem

Let S be C² on [0,infinity), positive, nonincreasing and nonconstant, with
S'(0)=0. Then there exists u>0 such that

    0 < S''(u) < S'(u)^2/[2 S(u)].                            (L)

No assumption that S tends to zero is needed. The proof allows plateaus,
non-strict monotonicity and oscillatory curvature.

## Proof

Put g=-S'. Then g is C¹, g>=0, g(0)=0, and

    integral_0^R g(u) du = S(0)-S(R) <= S(0).

Nonconstancy supplies a>0 with g(a)>0. Integrability supplies b>a with
g(b)<g(a): otherwise g>=g(a)>0 throughout [a,infinity), contradicting the
integral bound. Let m be the maximum of g on [0,b]. We have m>=g(a)>g(b)
and m>g(0), so its last maximizer c lies strictly inside (0,b), g(c)=m>0,
and g'(c)=0.

By continuity, in a sufficiently small neighborhood of c, g remains positive,
S remains positive and finite, and

    |g'(u)| < g(u)^2/[2 S(u)].

For every sufficiently small eta>0, the definition of the last maximizer gives
g(c+eta)<g(c). The mean-value theorem supplies a point u in (c,c+eta) with
g'(u)<0. Choose eta within the preceding neighborhood. At that point

    0 < -g'(u) < g(u)^2/[2S(u)],

which is precisely(L). This also proves that such points can be chosen
arbitrarily close to the end of a positive maximum plateau. No numerical
sampling or analyticity assumption enters.

## Why every hypothesis matters to the scope

- Constant S=1 has no such point; nonconstancy is necessary.
- The positive nonflat gate S=exp(-u) has
  `S''=S'^2/S`, so(L) never holds; S'(0)=0 cannot simply be dropped.
- A finite domain is insufficient without an endpoint condition. On[0,1/2],
  S=1-u³ is positive, decreasing, C-infinity and satisfies S'(0)=S''(0)=0,
  but S''<0 throughout the interior. The half-line or an equivalent condition
  ensuring a positive interior maximum of -S' is load-bearing.
- The theorem concerns a gate defined and allowed throughout the stated domain.
  It does not prove that every dynamically accessible density range contains
  the witness point. A separately derived restricted state domain changes the
  physical application, not this calculus theorem.

## Consequence for the proposed action, conditional on the audited principal law

For H=C(q-1)² S(Pi/Pic), C>0, Pic>0 and any fixed finite gamma>=0, fix the
witness u from(L), set p=Pic*u>0, and let q grow. The exact coefficients are

    A0=2C q² S,
    c=1+gamma p+C(q²-1)S'/Pic,
    D=C(q-1)² S''/Pic²-gamma,
    A_infinity=A0-c²/D.

Therefore

    A_infinity/(Cq²) -> 2S-S'^2/S'' < 0,
    n_eff/(Cq²) -> 2S-uS' > 0,
    rho/(Cq²) -> S > 0.

D is positive and nonzero for sufficiently large q. All limits hold with
gamma, Pic and C fixed; increasing a finite constant stiffness does not remove
this unrestricted-q family. The regular-center constraint construction then
provides local data with P=0, Pi=p and finite curvature. A sufficiently small
patch remains below the polarization cap. The audited scalar principal law
has negative sound-speed squared there.

This is an obstruction to **uniform health on the unrestricted field domain**
of this action family. It is not a theorem that every state, a specific
cosmological trajectory, or every alternative completion is unstable. It does
not establish the instability inside a UV cutoff or restricted Q/Pi domain
that has been independently specified and justified.

For S=exp(-u³), the relevant ratio simplifies exactly to

    2S-S'^2/S'' = exp(-u³) (3u³-4)/(3u³-2).

It is negative on `(2/3)^(1/3)<u<(4/3)^(1/3)`; at u=1 it equals -exp(-1).
The executable independent checks verify this identity and the stated
counterexamples. The generic proof above is independent of that example.
