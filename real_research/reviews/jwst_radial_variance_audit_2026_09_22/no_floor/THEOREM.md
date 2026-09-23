# No positive universal relative-delay-variance floor in the uncapped profile class

Verdict: proved within the stated stochastic model by Codex self-review of
the supplied family and the prior majorant; independent peer review and
literature novelty remain unverified. This is not observational confirmation.

Consider central photons, speed and sphere radius one, no absorption, all
photons counted, and conservative unpolarized Thomson scattering. Write
s=r^2, D=T-Z as in ../analytic/THEOREM.md. For every integer n>=1 set

    a_n=1/(2^n-1), A=2/log(2), k_n(s)=A/(a_n+s).

Every member is smooth, strictly positive and bounded. There is no bound on
opacity common to the entire family: max k_n=A(2^n-1) increases without bound.
The means also vary. The result does not concern a common opacity cap or a
fixed mean delay.

The exact mean is

    E[D_n]=integral_0^1 r*k_n(r^2) dr
          =(1/2)integral_0^1 k_n(s) ds
          =(A/2)log((1+a_n)/a_n)=n.

The factor 1/2 comes from ds=2r dr. Omitting it changes the observable's
normalization, not the physics. For the negative fixture a'_n=1/(2^(2n)-1)
with the same A, the actual mean is 2n, so the same claimed-mean-n identity
fails. That fixture still has vanishing relative variance; its role is only
to detect normalization errors.

For arbitrary a,A>0 the smooth majorant in ../analytic/THEOREM.md satisfies

    LU+2m=-4Aa z^2/[3(a+s)^2]<=0,
    U(1,z)-z^2=(11/9)[z-3k(1)/11]^2>=0.

Its F(0)^2 contribution to U(0,0) cancels the square of the actual mean,
giving the general upper bound

    Var(D) <= 11/9 + A^2/[11(1+a)^2]
                +(A^2/3)[log((1+a)/a)-1/(1+a)].

For each finite n, bounded rate gives the geometric escape tail and square
integrability required by the previous stopping argument. The proof is applied
separately to each finite n; no limit process or uniform escape-tail estimate
is assumed, and the singular limiting opacity is never declared admissible.

Put L=log(2), q=2^(-n). Substitution gives

    Var(D_n) <= B_n
       =11/9+4(1-q)^2/(11L^2)+4(nL-1+q)/(3L^2)
       <=11/9+4/(11L^2)+4n/(3L).

The last inequality uses 0<q<1 and removes only nonpositive terms. The positive
atanh series gives L>2/3. Hence 4/(11L^2)<9/11 and 4/(3L)<2, so

    Var(D_n) < 202/99+2n < 3+2n,
    0<=Var(D_n)/E[D_n]^2 < 2/n+3/n^2 -> 0.

For any C>0, choose an integer n>max(1,5/C). Since 2/n+3/n^2<=5/n for n>=1,
that admissible profile has Var(D_n)<C*E[D_n]^2. Thus there is no positive
universal constant floor over this uncapped radial class.

The constants are obtained from the generator majorant and exact inequalities,
not fitted variances. No numerical variance or finite list of n proves the
limit. The executable audit checks the general generator identities, sequence
normalization, bound differences, exact logarithm inequalities, and limit.
It complements the finite-n stopping argument above.

This theorem does not claim that the bound 2n+3 is optimal or that Qwen's
unsupported smaller constants are false; their proof is simply absent.
The two nominal Qwen passes 38deac5c and 2b16414b remain rejected. The first
inserts constants without derivation, while the second tests only a wrongly
normalized mean. Known inhomogeneous transport and martingale methods are
not discoveries. See SOURCES.md for the limited novelty check.
