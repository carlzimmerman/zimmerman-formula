# Extension: compact-zero gates are also covered

This is a new, explicit extension of GATE_LEMMA.md. Its original strictly
positive theorem and hash are preserved. No conclusion is drawn by dividing
by S at a point where S=0.

**Verdict: proved as written.** Let S be C² on[0,infinity), nonnegative,
nonincreasing and nonconstant, with S(0)>0 and S'(0)=0. Then there exists u>0
with **S(u)>0** and

    0 < S''(u) < S'(u)^2/[2S(u)].

Proof: set g=-S'. As before, g is nonnegative, C¹, g(0)=0 and integrable,
because `integral_0^R g=S(0)-S(R)<=S(0)`. Choose a with g(a)>0 and b>a with
g(b)<g(a). The last maximizer c of g on[0,b] is interior, has g(c)>0 and
g'(c)=0. Crucially **S(c)>0**: if S(c)=0, nonnegativity and differentiability
would make c a local minimum of S and force S'(c)=0, contradicting g(c)>0.
Continuity therefore gives a neighborhood with S>0 and
`|g'|<g²/(2S)`. Since c is the last maximizer, g(c+eta)<g(c) for every small
eta>0. The mean-value theorem supplies u in(c,c+eta) with g'(u)<0. This is
the claimed strict inequality at positive S.

In particular, a C² compact-support gate that eventually becomes identically
zero cannot evade the curvature witness by using an exact zero region. The
witness lies before that region. The high-q principal-family argument is
evaluated at this positive-S point, so its nondegenerate local coefficients
are unaffected by any separate degeneracy where S=0.

An explicit example is

    S(u)=(1-u³)^3 for0<=u<=1, and S(u)=0 foru>=1.

It is C², nonincreasing, flat through second order at the origin, and matches
the zero extension through second order at1. At u=2^(-1/3), S=1/8 and

    2S-S'^2/S'' = -1/32 <0,     S''>0.

The separate finite-domain exception remains valid: if the action is only
defined on a bounded positive-gate interval ending before such a witness,
this half-line theorem does not apply. Likewise the extension does not prove
that a particular dynamical trajectory reaches the witness. Those are state
domain/evolution restrictions, not an escape based solely on compact zeroes.
