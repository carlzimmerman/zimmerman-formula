# A measurable bound on the two omitted sea classes

This is a finite-regulator Cauchy–Schwarz bound for the actual gauge measure,
not a numerical error estimate. It does not require positivity of a
disconnected spectral density. It requires a positive normalized gauge
probability measure and finite second moments for the displayed variables;
reweighting with a sign/phase needs a separate bound including its
normalization. At zero theta and the usual positive-mass 2+1 QCD measure this
is the intended setting. All variables below may be complex.

Write Xc=X-<X>, sigma_X^2=<|Xc|^2>, and
Y_ab=(T_a-<T_a>)(T_b-<T_b>). The covariance here has no complex conjugation,
as in the derivative formula, but the variance used in its bound does.
The third joint cumulant obeys

\[
\kappa(B,T_a,T_b)=\langle B_cY_{ab}\rangle
                =\langle B_c(Y_{ab}-\langle Y_{ab}\rangle)\rangle.
\]

Therefore the residual after retaining the same-loop sea term satisfies

\[
\boxed{|\Delta C_{ab}^{sea}|\le
 \frac{|\delta|}{3}(\sigma_{B_a}\sigma_{T_b}
                    +\sigma_{B_b}\sigma_{T_a})
 +\frac{\delta^2}{9}\sigma_B\sigma_{Y_{ab}}.}
\tag{B1}
\]

The right side uses gauge fluctuations of the residual divided-difference
loops, rather than variances of independently subtracted light and strange
traces. An even simpler, potentially weaker replacement is

\[
\sigma_{Y_{ab}}\le
 \big\langle|T_{a,c}|^2|T_{b,c}|^2\big\rangle^{1/2}
 \le[\langle|T_{a,c}|^4\rangle\langle|T_{b,c}|^4\rangle]^{1/4}.
\tag{B2}
\]

These follow by applying Cauchy–Schwarz to each covariance and then the
triangle inequality. They bound exact gauge moments. Sample estimates need
uncertainty intervals, autocorrelation analysis and separation/control of
auxiliary-noise variance before becoming confidence statements.

At a finite regulator, with b_ab the right side of (B1), the missing
photon-convolved derivative has the conditional bound

\[
|\Delta C_u|\le\tfrac12\sum_{ab}|G_{ab}|b_{ab}.
\tag{B3}
\]

For the finite-T log-correlator coefficient divide (B3) by |C0(T)|. A proton
mass bound additionally needs division by T, a controlled large-T limsup,
all relevant counterterms and nonzero correlator normalization. Large gauge
fluctuations, the small baryon correlator, UV growth and nonuniform
mass/curvature limits can make this bound weak or divergent.

There are **no measured residual variances available here**, so (B1) gives no
numerical physical error bar. The explicit delta and delta squared factors
express vanishing orders near the SU3 point. They are not smallness bounds at
physical ms/ml: the resolvents, normalized baryon weights, gauge measure and
infrared gaps can vary strongly with mass, curvature and volume. The exact
estimator remains valid where the propagators and normalizations exist, even
when truncating in delta is poor.
