# FSP-Q: convention invariance and the fixed-mass alpha sensitivity

Parent FSP-001; work package FSP-002. This is a new analytical qualification only: the frozen report, current manifest, scripts and run inputs are unchanged. No new source search, numerical fit, experiment or executed symbolic check was used. The derivation below is independent hand algebra from the displayed matching equations.

## Assumptions and variables

Use natural units. On a smooth local branch, write

\[
\bar H=K G\Lambda^3 c_H(\alpha,x),\qquad
m_p=\Lambda C_p(\alpha,x),\qquad
x_i={\widehat m_i\over\Lambda},\qquad K={8\pi\over3}.
\]

The same specified definitions of the RG-invariant quark masses \(\widehat m_i\), charge normalization and nonperturbative matching are used throughout. Holding quark masses fixed requires that convention to be fixed; RG invariance alone does not remove mass-scheme choices. Any other microscopic parameters, including theta, and \(G\) are held fixed. All relevant quantities are positive, and the matching functions are differentiable. The de Sitter matching mechanism remains conditional for the reasons already stated in `REPORT.md`.

The physical question here holds the measured \(\widehat m_i\) **and** \(m_p\) fixed while varying alpha; \(\Lambda\) adjusts to preserve the proton mass. It therefore differs from the partial derivative at fixed ratios \(x_i\).

## The dimensionless ratio is convention independent

Let an arbitrary positive smooth convention factor \(s\) define \(\Lambda'=s\Lambda\), with \(s\) allowed to depend on alpha and other fixed external parameters. At the same physical theory,

\[
x_i'={x_i\over s},\qquad
C_p'(\alpha,x')={C_p(\alpha,sx')\over s},\qquad
c_H'(\alpha,x')={c_H(\alpha,sx')\over s^3}.
\]

These transformations follow from preservation of the dimensional observables \(m_p\) and \(\bar H\); they are not optional normalizations of those observables. Hence

\[
R'(\alpha,x')={c_H'(\alpha,x')\over C_p'(\alpha,x')^3}
={c_H(\alpha,sx')\over C_p(\alpha,sx')^3}
=R(\alpha,x).
\]

Thus \(R=c_H/C_p^3\) evaluated at corresponding physical inputs is invariant even when the convention factor depends on alpha. Equivalently \(R=\bar H/(KGm_p^3)\). A more general positive, smooth, invertible reparameterization of Lambda has the same conclusion pointwise, by preservation of these observables; the explicit component transformation below assumes \(s=s(\alpha)\) along the held external inputs.

## Correct sensitivity at fixed quark masses and proton mass

Set \(t=\ln\alpha\), \(\ell=\ln\Lambda\), \(p=\ln C_p\), \(h=\ln c_H\), and \(r=\ln R=h-3p\). Define partial sensitivities at fixed ratios or fixed alpha as indicated:

\[
p_\alpha=\left.\partial_t p\right|_x,\quad
h_\alpha=\left.\partial_t h\right|_x,\quad
p_i=\left.\partial_{\ln x_i}p\right|_\alpha,\quad
h_i=\left.\partial_{\ln x_i}h\right|_\alpha,
\qquad P=\sum_i p_i,\quad Q=\sum_i h_i.
\]

Because each physical quark mass is fixed, \(d\ln x_i/dt=-d\ell/dt\). Differentiating the fixed-proton-mass condition yields

\[
0={d\ln m_p\over dt}=p_\alpha+(1-P){d\ell\over dt}.
\]

On the regular branch \(1-P\ne0\),

\[
{d\ell\over dt}=-{p_\alpha\over1-P},\qquad
\boxed{\quad
S_{\rm constrained}
=\left.{d\ln R\over d\ln\alpha}\right|_{\widehat m_i,m_p}
=h_\alpha-{(3-Q)p_\alpha\over1-P}.
\quad}
\]

An independent form obtained by differentiating \(r=h-3p\) is

\[
S_{\rm constrained}
=r_\alpha+{(\sum_i r_i)p_\alpha\over1-P},\qquad
r_\alpha=h_\alpha-3p_\alpha,\quad
\sum_i r_i=Q-3P.
\]

The two forms agree by elementary expansion. If \(1-P=0\), preserving the measured proton mass need not determine a differentiable Lambda branch: the implicit-function step fails. A nonzero \(p_\alpha\) then obstructs the proposed first-order path; if it too vanishes, higher-order information is needed. No sensitivity formula with this denominator is asserted there.

## Why the constrained derivative is also invariant

Let \(\sigma=\ln s\), with dot denoting \(d/dt\) along the fixed external inputs. At corresponding points the transformed partial derivatives obey

\[
p_\alpha'=p_\alpha+(P-1)\dot\sigma,\qquad
h_\alpha'=h_\alpha+(Q-3)\dot\sigma,\qquad
P'=P,\quad Q'=Q.
\]

Substitution gives

\[
h_\alpha'-{(3-Q')p_\alpha'\over1-P'}
=h_\alpha-{(3-Q)p_\alpha\over1-P},
\]

because the two terms proportional to \(\dot\sigma\) cancel. Consistently, \(d\ell'/dt=d\ell/dt+\dot\sigma\).

By contrast, the fixed-ratio partial derivative transforms as

\[
\left.\partial_t r'\right|_{x'}
=\left.\partial_t r\right|_x+(Q-3P)\dot\sigma.
\]

It is not convention invariant under alpha-dependent rescalings unless that additional term vanishes. There is no contradiction: holding \(x'\) constant then describes a different physical path from holding \(x\) constant. The value of R and its derivative along one specified physical path remain invariant.

## Qualification to the report and uncertainty statement

`REPORT.md` explicitly defines \(S_\gamma=\partial\ln R/\partial\ln\alpha\) at independently held quark-mass ratios. Its formula is valid for that stipulated path. It requires this qualification if used for the different calibration proposed here, where physical quark masses and the proton mass are measured inputs: the appropriate denominator is \(S_{\rm constrained}\), not that fixed-ratio partial derivative.

For a locally isolated inverse solution with nonzero \(S_{\rm constrained}\), and quark/proton masses treated as exact held inputs, the first-order relation is

\[
\delta\ln\alpha\simeq{\delta\ln R\over S_{\rm constrained}}.
\]

Here the uncertainty in R includes the observed vacuum/acceleration matching and calculated matching-function uncertainty evaluated on the same constrained branch. If the measured masses have uncertainties, their induced shifts and covariances must be propagated through both the mass constraint and the observed dimensionless ratio; the latter already contains \(m_p^{-3}\), so treating those two appearances as independent would double count. A zero or poorly determined constrained sensitivity gives no well-conditioned alpha extraction. Neither this qualification nor a change of Lambda convention supplies a missing matching coefficient or an electron Yukawa mechanism.
