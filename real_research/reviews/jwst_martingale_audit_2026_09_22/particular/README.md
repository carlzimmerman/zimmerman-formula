# Particular-solution audit

Qwen 35ddaa6d2d014ca8adda499b4cedb956 finally uses the correct operator,
but does not solve its coefficient equations. Its handwritten regrouping moves
b1*s from the s coefficient into the s*z coefficient. It consequently inserts
wrong coefficients and its own output prints residual 3*k*s*(1-z)/2, not zero.
The related nonexistence assertion in 2f2c32187591488e9b4e52fbe00261fe is false.
Its claimed s*z^2 obstruction is identically zero in its actual output.

The independent script constructs the same ansatz and matches ALL bivariate
coefficients using SymPy solve, with gauge P(1,0)=0. No fitted or preinserted
solution is used. The five nontrivial coefficient equations are

    4*a2-k*b1 = 0
    b1+3*k*c/10-k = 0
    2*b1-9*k*c/10 = 0
    2*a1-k*b0+2*c-2 = 0
    b0+k = 0.

The unique gauged solution is

    P = (7k^2/20+1/3) + (-k^2/2-1/3)s + (3k^2/20)s^2
        + (-k+3ks/5)z + (4/3)z^2.
    h(z)=P(1,z)-z^2=z^2/3-2kz/5.

The symbolic interior equation vanishes exactly. P+1 also passes; P+s has
residual 2z. The wrong Qwen polynomial has residual 3ks(1-z)/2, with physical
witness 3/8 at k=1,s=1/4,z=0. Nine checks pass and the manifest validates.
This is an exact counterexample to the asserted nonexistence, not a full
second-moment boundary solution. In particular, h is not zero and may not be
discarded. No transport simulation or literature novelty claim is made here.

Next Qwen work: derive the stopped boundary correction and certify its extrema
over the actual outgoing interval. Then validate the resulting relation with
independently implemented transport. The audited solution is a prerequisite
that should be reused; repeating coefficient guesses is an exhausted route.
