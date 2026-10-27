# Independent source-critical derivation (before author target)

Created after PRETARGET.md was pinned and after reading the two primary PDFs
directly with a fresh pdftotext extraction and visual inspection. No author RAW,
coefficient file, source summary, code, run001, report or historical review has
been opened. No candidate soft factor was supplied to this reviewer.

## Source authentication and exact extraction

Checked 2026-10-19. Locally supplied primary PDFs have visible version stamps:
Bernard, Kaiser, Schmidt, Meissner, “Consistent calculation of the nucleon
electromagnetic polarizabilities in chiral perturbation theory beyond next-to-
leading order”, arXiv:hep-ph/9309211v1, 1 Sep 1993. PDF printed pages 4-5
(PDF pages 5-6), Eqs. (6)-(10), were extracted afresh and visually checked.
SHA256 09af9bc7bfc8fc07b22e344a60aa922da0efe4d2fda0c5e23ffda2819e3c94f4.

Bernard, Kaiser, Meissner, Schmidt, “Aspects of nucleon Compton scattering”,
arXiv:hep-ph/9311354v1, 24 Nov 1993. Printed pp. 5-6 (PDF pp. 6-7), Eqs.
(5)-(9), especially the pole-subtraction paragraph at the start of printed p. 6.
SHA256 d86056f9b18b305ac7b36b69497fc77df3ca9745ac7624cc967a23f1f2f5dcbe.
Authentication here establishes the supplied PDF's visible primary-source
identity/version and retained hash; no external server hash was independently
fetched. Existing author-generated text extractions were not used.

The first paper works in SU(2), m_u=m_d, and includes all O(q^4) terms in its
specified heavy baryon expansion. Its coefficient C=e^2/(96*pi^2*F_pi^2).
Its magnetic-moment convention is kappa=(kappa_s+tau_3*kappa_v)/2, so
kappa_s=kappa_p+kappa_n, not half that sum.

## Algebra independently reconstructed from Eqs. (6)-(9)

Let L=log(M_pi/mu), P=g_A^2/(96*pi^3*F_pi^2*m), and hats mean division by
u=e^2. All displayed chiral LECs and the renormalization scale mu are fixed.
Eq. (7a): x_p-x_n=9-3=6; y_p-y_n=71-39=32.
Eq. (8a): x'_p-x'_n=(3+kappa_s)-(1-kappa_s)=2+2*kappa_s;
y'_p-y'_n=(37/2+6*kappa_s)-(13/2-6*kappa_s)=12+12*kappa_s.
Therefore, through O(q^4), writing the independent renormalized polarizability
counterterm differences separately,

  Delta alpha_hat = P*(6 L+4) + Delta delta_alpha_hat(mu),
  Delta beta_hat = P*(6(1+kappa_s)L+3(1+kappa_s))
                   + Delta delta_beta_hat(mu),
  Delta(alpha_hat+beta_hat)
    =P*(6(2+kappa_s)L+7+3*kappa_s)+Delta delta_plus_hat(mu),
  Delta(alpha_hat-beta_hat)
    =P*(-6*kappa_s L+1-3*kappa_s)+Delta delta_minus_hat(mu).

Here Delta=p-minus-n. The O(q^3) 1/M_pi terms cancel. Both c_2 log terms and
c^+ terms cancel in the difference. The last two lines agree with Eq. (10),
which was checked as a separate checksum after doing the subtraction. The
logarithmic coefficients in alpha_hat and beta_hat are respectively

  g_A^2/(16*pi^3*F_pi^2*m),
  g_A^2*(1+kappa_s)/(16*pi^3*F_pi^2*m).

The alpha_hat-minus-beta_hat coefficient is
-g_A^2*kappa_s/(16*pi^3*F_pi^2*m).

These are source-verified EFT coefficients, not exact values of the physical
polarizabilities at a selected mass. Fixing LECs and mu is necessary: assigning
arbitrary mass-dependent finite counterterms could cancel an apparent log.
The paper's running counterterms cancel mu dependence, not a mass logarithm
throughout a chiral family at fixed LECs. Treating F_pi,g_A,m,kappa_s as the fixed
inputs at this order is part of this coefficient extraction; inserting their
own mass expansions changes the order bookkeeping.

## Pole subtraction and what the second paper establishes

The paragraph on printed p. 6 explicitly excludes nucleon-pole-graph
contributions when defining the polarizabilities and separates anomalous-
magnetic-moment pole contributions using the Powell cross section convention.
This is a positive source check of the real-Compton polarizability convention.
It is not, by itself, a complete specification of every off-shell contact in
an arbitrary doubly-virtual Born-subtraction convention. The EFT bridge below
uses the gauge-invariant local O(k^2) effective action with this real-Compton
normalization. Differences in analytic off-shell convention must be matched
consistently; no conclusion about all hard virtual momenta follows.

## Independent full soft contraction and sign

Starting from Delta L_M=2*pi*(alpha E_M^2+beta B_M^2), Wick rotation gives
Delta L_E=2*pi*(alpha E_E^2-beta B_E^2), as derived before source access.
For Euclidean k=(k4,k1,k2,k3), v=(1,0,0,0), define

  G_ab=k^2 delta_ab-k_a k_b,
  E_ab=k4^2 delta_ab+k^2 v_a v_b-k4(k_a v_b+v_a k_b).

A_a E_ab A_b=E_E^2; A_a(G-E)_ab A_b=B_E^2. Both E and G are transverse.
The photon two-point kernel obtained by two derivatives of the action is

  K_ab=4*pi*((alpha+beta)*E_ab-beta*G_ab).

Thus 1/2 Tr[K D] equals
2*pi*((alpha+beta)*(k^2+2*k4^2)-3*beta*k^2)*D(k).
SO(4) averaging <k4^2>=k^2/4 gives exactly

  3*pi*(alpha-beta)*k^2*D(k).

In a subtraction/dispersive language, the -3*beta term and the
(3/2)*(alpha+beta) term must both be retained. Their sum is
(3/2)*(alpha-beta). Keeping the magnetic subtraction term alone, or using the
real-photon alpha+beta coefficient alone, would give the wrong full invariant
soft contraction. The tensor derivation includes both and checks the Wick
relative sign. This decomposition is an effective-action representation of the
complete O(k^2) tensor, not a rederivation of a full dispersion integral.
Longitudinal propagator terms vanish against these transverse kernels.

For D_lambda(k)=1/(k^2+lambda^2), a rotationally invariant cutoff Lambda on the
soft region gives exactly

 I_lambda-I_0 = integral_{|k|<Lambda} d^4k/(2*pi)^4
                [k^2/(k^2+lambda^2)-1]
 =[-lambda^2 Lambda^2+lambda^4 log((Lambda^2+lambda^2)/lambda^2)]/(16*pi^2).

The induced soft mass difference is 3*pi*(alpha-beta)*(I_lambda-I_0).
Accordingly the coefficient of lambda^4 log(lambda^2) is
-3*(alpha-beta)/(16*pi); equivalently the coefficient of lambda^4 log(lambda)
is -3*(alpha-beta)/(8*pi). The log argument needs a scale, whose change only
moves an analytic lambda^4 term. Dividing by u and taking p-minus-n, the mixed
log(M_pi/mu)*lambda^4 log(lambda^2) coefficient at this chiral order is

  +3*g_A^2*kappa_s/(256*pi^4*F_pi^2*m),

with the displayed mass-shift and photon-propagator normalizations. A convention
for a differently normalized Compton tensor may rescale intermediate K, but
must reproduce the action-level contraction after its external prefactors.

## Exceptions, limits, and exact implication

At kappa_s=0 the O(q^4) p-minus-n log of alpha-beta vanishes exactly: this
particular projected leading-log witness is absent. That does not equate the
NB tensors: the electric log is still nonzero for g_A!=0, and even the
alpha-beta expression has an analytic constant and independent counterterms.
A claim of a nonzero projected coefficient must explicitly assume kappa_s!=0
(and nonzero g_A, finite positive F_pi,m). Fixed m_u=m_d>0 alone does not imply
that extra condition or an exact physical value of kappa_s.

The small photon mass/soft k limit is taken at fixed positive M_pi, with
lambda,|k| << M_pi. The chiral log is then a coefficient in a second, chiral
expansion at fixed LECs. Taking M_pi->0 first invalidates uniform use of the
local O(k^2) soft action; the limits cannot be freely interchanged. The leading
1/M_pi terms cancel in this p-minus-n comparison, but that cancellation does
not restore a uniform all-order expansion.

The exact covariance theorem is W(Q')=W(Q), T_p^NB(Q')=T_n^NB(Q). It does not
force T_p^NB(Q')=T_p^NB(Q). The checked chiral logarithms demonstrate that a
same-proton equality cannot be a universal consequence across this chiral
family. They do not prove nonzero full projected response at every positive
mass or determine a full metric/vacuum response, A, R or alpha.

## Current verdict before author comparison

The exact flavor-covariance distinction is proved under the stated invariant-
regulator/matching hypotheses. The source chiral coefficients and full soft
contraction are established at the stated EFT order and ordered limits. Any
unrestricted claim of nonzero projected logarithm needs the kappa_s exception;
any full nonperturbative response value still requires further input.
