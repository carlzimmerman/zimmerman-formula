# Convention translation after the independent raw derivation

The immutable `RAW_DERIVATION_v1.md` interpreted the delegation's compressed
expression `(1-D/4)W/V` as `V^-1(1-D/4)W`. The authoritative project observable
in `fine_structure_puzzle/qcd_prediction/coordinator/METRIC_RESPONSE.md` is
instead unambiguously

\[
 f=W/V,\qquad \rho_E=(1-D/4)f=-\frac{DW}{4V},\qquad D=H\partial_H.
\]

The coordinator confirmed this convention after the raw was saved. This is a
translation of an ambiguous delegation, not a discrepancy in either target.
All spectral, determinant and Mellin formulas in the raw are unchanged. Every
stress formula below uses the authoritative convention, holding M, masses,
couplings and matched comparison inputs fixed.

Writing Omega4=8 pi^2/3 and A=(19/30)c_R+(5/63)c_lambda, the translations are

\[
 \rho_{\gamma}=\frac{31H^4}{180\Omega_4},\qquad
 \delta\rho_{\gamma,6}=-\frac{e^2H^6}{4\Omega_4}A,
\]

\[
 \rho_{1}=\frac{3\zeta_T(3/2)M^3H}{8\Omega_4}
 =\frac{9\zeta_T(3/2)M^3H}{64\pi^2}.
\]

For the full positive Gaussian model, at fixed M>0,

\[
 \delta\rho=-\frac{\pi M^4}{4\sqrt3\Omega_4}
 -\frac{\pi M^2H^2}{2\sqrt3\Omega_4}
 +\frac{19H^4}{80\Omega_4}+O(H^{4+3\sigma}),\qquad0<\sigma<1.
\]

This agrees with the coordinator's `qed_resummation/RAW_DERIVATION_v1.md`.
The fixed-M absence of H and the nonuniform small-charge limit are unaffected
by translating the convention.

## Analytic nonvanishing of the tempting first-order coefficient

This additional check was derived after the target read; it was not part of
the independent raw. It uses no numerical sum or fit. At q=5/2, set n=q+k,
k>=0. The convergent Hurwitz representation at s=3/2 gives

\[
 \zeta_T(3/2)=-2-\frac94\zeta_H(2,q)
 +\sum_n\left(1-\frac9{4n^2}\right)
 \left[\left(1-\frac1{4n^2}\right)^{-3/2}-1\right].
\]

For 0<=u<=1/25,

\[
 (1-u)^{-3/2}-1\leq(1-u)^{-2}-1
 =\frac{2u-u^2}{(1-u)^2}\leq\frac{625}{288}u<\frac52u.
\]

The positive correction sum is therefore at most (5/8) zeta_H(2,q).
Consequently zeta_T(3/2)<-2, proving that the first-order M^3 H coefficient is
strictly nonzero in the stated common subtraction. Its cancellation in the
full fixed-M asymptotic expansion is substantive. Positivity of the underlying
Gaussian does not require positivity of this UV-subtracted coefficient.
