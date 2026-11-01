# A time-integrated bound for adverse cut stress

Base: X48-UC-2026-11-01-B. This is an exact consequence of the unchanged
normalized constitutive law, not a proof of the compression bootstrap.
It treats the negative cut stress left open in `bootstrap.md` without
requiring a positive lower compression bound or an upper bound for K.

Let activation be s=0. For any fixed material cell use signed compression
x=-theta, rho(0)=1, K>=0, and

\[
 S=P+\kappa(x-2)_++\kappa g(K)x,\qquad
 \kappa=\tfrac12\rho Wh,\quad g=K/(K+.01),\quad 0\le g\le1.
\]

Suppose only that x(s)<=U on 0<=s<=T, with U>0 and UT<=log(2).
There is no assumed lower bound on x. Then, uniformly in cell index and N,

\[
 \boxed{\int_0^T s^{-p}S_-(s)\,ds
 \le\frac{6U^3e^{2UT}}{3-p}\,T^{3-p},\qquad 0\le p<3.}       \tag{A1}
\]

Here S_-=max(-S,0). The statement is conditional on the actual one-sided
compression cap on this cell. It makes no assumption about heat-flux
gradients or about the total variation of K.

## Proof

The exact primitive from the preceding continuation is

\[
 F(\rho)=\frac{W(\rho)^2-9/4}{4}\ge0,\qquad
 F(1)=0,\qquad \dot F=\kappa x.                         \tag{A2}
\]

Since P and the old heater stress are nonnegative,

\[
 S_-\le\kappa g x_-\le\kappa x_-=(-\dot F)_+.           \tag{A3}
\]

Continuity gives rho<=exp(Us)<=2. Throughout this range W<=2 and

\[
 h(\rho)\le3(\rho-1)_+^2
       \le3U^2e^{2UT}s^2,\qquad
 (\dot F)_+=\kappa x_+\le A s^2,\quad A=6U^3e^{2UT}.    \tag{A4}
\]

Consequently 0<=F(s)<=As^3/3. For w(s)=s^(-p), integrate on [eta,T]:

\[
 \int_\eta^T w\dot F
 =w(T)F(T)-w(\eta)F(\eta)-\int_\eta^T w'F.
\]

The eta boundary term tends to zero for p<3. The remaining two terms
are nonnegative, so the weighted negative variation of F is at most its
weighted positive variation. Both integrals are finite: the positive one
is bounded by A integral_0^T s^(2-p)ds, and the identity first bounds the
negative one on truncated intervals before passage to zero. Equations
(A3)-(A4) now prove (A1).

This proof remains valid when density passes into the quiet interval:
F and kappa are then both zero. Arbitrarily strong expansion does not
invalidate the estimate as long as geometry is valid and the stated
one-sided cap holds.

## Normalized boundary input

For the existing homogeneous reference on 0<s<=.001, its compression is
at least four. Hence rho_d>=1+4s and
h_d>=h(1+4s)=16s^2(3-8s)>=32s^2. Since W_d>=3/2,

\[
 \nu_d\ge\kappa_d\ge24s^2.
\]

It follows that

\[
 \boxed{\int_0^T\frac{S_-(s)}{\nu_d(s)}\,ds
           \le\frac{U^3e^{2UT}}4\,T,\qquad
 T\le\min\{.001,\log(2)/U\}.}                         \tag{A5}
\]

Thus the extra boundary input S_-/nu_d in the exact truncated ghost
formula has a uniform time-integrated bound under the one-sided cap.
An L1-in-time bound is not a pointwise boundary-amplitude bound. To use
it to close central compression still requires a uniform, spatially
separated boundary-transfer estimate for the actual propagator, as well
as the interior nonlinear estimate and proof of the cap. None of those
implications is assumed here. This is not a counterexample to (UC).

All inequalities are exact. No trajectory, numerical entropy seed, source
change or finite-grid extrapolation is used. The source identity and
parameters are those in `../continuation_2026_11_01/effective_flux.md` and
the unchanged material and transport files.
