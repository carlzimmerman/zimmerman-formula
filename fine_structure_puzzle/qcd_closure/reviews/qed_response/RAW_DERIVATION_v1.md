# FSP-005 independent raw derivation, v1

Provenance: fresh subagent `qed_response_review`, 2026-10-18/19. This note was written before reading `qed_infrared/DERIVATION.md`, `qed_infrared/REPORT.md`, any infrared implementation/results, or any `qed_resummation/` target. Inputs were the spectrum and conventions in the delegation. No numerical fitting or load-bearing computation is used. All target files remain immutable.

## Claim and conventions

On round S4 of inverse radius H, let D be the coexact Maxwell Hodge Laplacian, with

\[
 D_l=H^2\lambda_l,\qquad \lambda_l=(l+1)(l+2),\qquad
 d_l=\frac{l(l+3)(2l+3)}2,\quad l\geq1.
\]

Use W=-log Z, V=8 pi^2/(3 H^4), and the specifically requested density prescription

\[
 \rho=V^{-1}(1-H\partial_H/4)W.
\]

All H derivatives hold physical masses and couplings fixed. Dimensionless zeta functions below use H=1. The prescription is not silently replaced by a different stress-tensor definition.

## 1. Legitimate continuation of the transverse zeta function

Put n=l+3/2, so n=5/2,7/2,..., lambda=n^2-1/4 and d=n^3-9n/4. For Re s>2, followed by meromorphic continuation,

\[
 \zeta_T(s)=\sum_{j\geq0}\frac{(s)_j}{j!4^j}
 \left[\zeta_H(2s+2j-3,5/2)-\frac94\zeta_H(2s+2j-1,5/2)\right].
\]

The binomial expansion has uniform geometric ratio at most 1/25, and after separating finitely many pole terms its tail is analytic at s=0 and s=-1. Consequently its zeros cannot be substituted termwise across Hurwitz poles.

At zero, j=1 and j=2 contribute -9/32 and +1/64 respectively, using Res(zeta_H,1)=1 and the factor 2 in its argument:

\[
 \zeta_T(0)=\zeta_H(-3,5/2)-\frac94\zeta_H(-1,5/2)-\frac{17}{64}
 =\boxed{\frac{19}{30}}.
\]

At s=-1, the j=2 second Hurwitz term and j=3 first Hurwitz term contribute +9/256 and -1/768. Thus

\[
 \zeta_T(-1)=\zeta_H(-5,5/2)-\frac52\zeta_H(-3,5/2)
 +\frac9{16}\zeta_H(-1,5/2)+\frac{13}{384}
 =\boxed{\frac5{63}}.
\]

The exact Hurwitz values used are -47/24, -3367/960 and -61457/8064 at -1,-3,-5. Keeping only the polynomial sum without its pole-times-zero corrections is invalid.

## 2. Scalar ghost and the global U(1) quotient

The nonconstant scalar spectrum has eigenvalues l(l+3) and degeneracy (l+1)(l+2)(2l+3)/6, l>=1. With the same n it becomes lambda_0=n^2-9/4, d_0=(n^3-n/4)/3. Its continuation is

\[
 \zeta'_0(s)\ \text{(prime here denotes omitted scalar zero mode, not differentiation)}
 =\frac13\sum_{j\geq0}\frac{(s)_j(9/4)^j}{j!}
 [\zeta_H(2s+2j-3,5/2)-\tfrac14\zeta_H(2s+2j-1,5/2)].
\]

To avoid the overloaded prime, denote this function by zeta_S below. At s=0, its pole corrections are -3/32+27/64, giving

\[
 \boxed{\zeta_S(0)=-\frac{61}{90}}.
\]

The gauge quotient, apart from H-independent normalizations, is

\[
 Z=\frac{(\det{}'\Delta_0)^{1/2}}{\operatorname{Vol}(U(1)_{\rm global})
 (\det D)^{1/2}}.
\]

In the canonical L2 metric, a constant gauge parameter alpha has coefficient alpha_0=sqrt(V) alpha. A fixed-period compact U(1) therefore has volume proportional to sqrt(V); normalization scales and its coupling-dependent period only change H-independent factors. Hence log Vol_global=-2 log H+constant. The scalar zero mode must neither be inserted into det' nor divided out a second time.

At fixed reference scale mu,

\[
 W_{\rm Maxwell}=[\zeta_T(0)-\zeta_S(0)-2]\log(H/\mu)+C
 =\boxed{-\frac{31}{45}\log(H/\mu)+C}.
\]

This is the round-sphere Maxwell anomaly magnitude 4a=31/45 in these W and H conventions. Omitting the compact global quotient instead gives the incorrect coefficient 59/45. The requested density functional gives

\[
 \rho_{\rm Maxwell}=\frac{3H^4}{8\pi^2}
 [-\tfrac{31}{45}\log(H/\mu)+C+\tfrac{31}{180}].
\]

The finite local H^4 part depends on normalization/matching.

## 3. Dimension-six transverse kernel

For D[1+e^2(c_R H^2+c_lambda D)], expanded only to its controlled first order,

\[
 \delta W=\frac{e^2H^2}{2}
 [c_R\zeta_T(0)+c_\lambda\zeta_T(-1)]
 =\frac{e^2H^2}{2}[\tfrac{19}{30}c_R+\tfrac5{63}c_\lambda].
\]

Therefore

\[
 \boxed{\delta\rho=\frac{3e^2H^6}{32\pi^2}
 [\tfrac{19}{30}c_R+\tfrac5{63}c_\lambda]}.
\]

Here c_R,c_lambda have mass dimension -2. This determinant term alone is not a physical matching invariant: derivative photon operators proportional to the leading Maxwell equation are redundant under local field redefinitions, with the associated Jacobian and gravitational matching accounted for. Finite curvature-cubed gravitational terms contribute at exactly this H^6 density order on S4. A claimed physical coefficient must specify that full matching prescription. None of these local dimension-six contributions supplies H^1.

## 4. Exact positive Gaussian infrared enhancement

Let M>0 be fixed and

\[
 P=D[1+M^3D^{-3/2}],\qquad x=(M/H)^3.
\]

Every transverse eigenvalue of P is positive. Use the same spectral/zeta subtraction for its exact determinant ratio and for its perturbative expansion. Define

\[
 \Phi(x)=\frac12\zeta_T(3/2)x
 +\frac12\sum_l d_l[\log(1+x/\lambda_l^{3/2})-x/\lambda_l^{3/2}].
\]

The displayed sum converges absolutely, locally uniformly for x>=0; its tail is O(x^2 l^-3). This also follows from the difference of the order-two zeta determinants of P and D, because no integer perturbation order k>=1 places zeta_T(3k/2) at a pole. In particular it is a single common subtraction, not independent adjustment of perturbative and resummed answers.

The first-order term is

\[
 \Phi_1=\frac12\zeta_T(3/2)(M/H)^3,\qquad
 \boxed{\rho_1=\frac{21}{64\pi^2}\zeta_T(3/2)M^3H}.
\]

Its expansion parameter at the lowest transverse mode is x/6^(3/2). It cannot be used for fixed M and H approaching zero.

## 5. Mellin proof of the fixed-M result

No fit is needed. For 4/3<c<2, the convergent log-minus-linear sum gives the Mellin representation

\[
 \Phi(x)=\frac{x}{2}\zeta_T(3/2)
 +\frac1{4\pi i}\int_{c-i\infty}^{c+i\infty}
 \frac{\pi x^s}{s\sin\pi s}\zeta_T(3s/2)\,ds.
\]

The ordinary closed-manifold heat expansion (or the Hurwitz formula above) shows that zeta_T has only its positive poles at q=2 and q=1, with residues 1/2 and -1. The same residues follow directly from the exact smoothed spectral density: d dn=(lambda/2-1)d lambda.

For x large, shift the contour left. At s=1 the Mellin kernel has residue -1, so the integral contributes exactly -x zeta_T(3/2)/2. This cancels the explicit first-order insertion, not only its leading approximation. The other first poles are s=4/3,2/3,0, yielding

\[
 \boxed{\Phi(x)=
 -\frac{\pi}{4\sqrt3}x^{4/3}
 -\frac{\pi}{\sqrt3}x^{2/3}
 +\frac12\zeta_T(0)\log x
 +\frac34\zeta_T^{\,(1)}(0)
 +\frac12\zeta_T(-3/2)x^{-1}+\cdots}.
\]

Here zeta_T^(1) is differentiation. At subsequent s=-n, n>=1, the formal asymptotic coefficient is (-1)^(n+1) zeta_T(-3n/2)/(2n) times x^-n. The contour decay provided by 1/sin(pi s), together with the usual polynomial vertical-strip bounds for spectral zeta, justifies each finite contour shift and its remainder.

In m=M/H notation the powers are m^4, m^2, log m, constant and m^(-3n). There is no m^3 term. Applying the stipulated density functional gives leading terms

\[
 \rho=-\frac{3M^4}{16\pi\sqrt3}
 -\frac{9M^2H^2}{16\pi\sqrt3}
 +\frac{3H^4}{8\pi^2}
 [\tfrac{19}{20}\log(M/H)+\tfrac34\zeta_T^{\,(1)}(0)+\tfrac{19}{80}]
 +O(H^7/M^3).
\]

The M^4 and M^2H^2 terms are local gravitational matching terms and may be shifted by local counterterms. Crucially there is no M^3H term in the full fixed-M determinant, even though it is present in its first-order insertion. Negative renormalized leading coefficients are compatible with positivity of every finite Gaussian eigenvalue, because the determinant ratio requires UV subtraction. Positivity alone says nothing about the sign of the renormalized vacuum density.

## 6. Limits and safe scope

If M^3=e^2 K^3, the first derivative at e^2=0 contains K^3 H. The H->0 limit at fixed nonzero e instead samples x=e^2(K/H)^3 tending to infinity. The limits and the perturbation expansion are nonuniform. An exact Gaussian countermodel is therefore enough to invalidate an inference from a first-order H term to a fixed-coupling asymptotic H term. It does not prove that every possible massless interacting QED completion lacks such a term.

A flat-space gap for charged/current excitations does not, by itself, prove uniform control over metric derivatives, integrated T...TJJ response, finite-volume/global modes, or massless-photon resummations. Conversely a global or finite-soft-mode construction which produces H behavior is not automatically a local QED realization. Each needs its own locality, covariance, source-response and uniform-limit checks. No alpha value or unconditional QCD/QED no-go follows from this note.

## Audit status

Analytic obligations above: passed under the explicitly stated Gaussian/spectral conventions. External identification with a sphere anomaly and local EFT matching remains subject to source checks in the ensuing target audit. No target claim has yet been read or assigned a verdict. No numerical experiment was used.
