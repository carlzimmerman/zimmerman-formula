# Pressure, density and expansion: which inverse is identifiable?

CD26-3, 2026-09-26. The operative filtered `nu_mono` target and criterion B
remain unchanged. This route derives conditional inverses; it does not claim
an observational fit or identify the microscopic origin of dark energy.

## 1. Fix the units and the hypothesis before inverting

Here `a` is the dimensionless FLRW scale factor, `a0` is an acceleration,
`epsilon` is energy density and `p` is pressure, both in J/m³. Define positive
tension `Pi = -p`. Mass density is `rho = epsilon/c²`. Let
`g = G_cosm/G_N > 0`, with constant measured `G_N`, `g` and `kappa` unless
explicitly stated otherwise. The two distinct promotions are

\[
 a_0^2=\kappa^2G_N\epsilon_X
 \quad\hbox{(density)},\qquad
 a_0^2=\kappa^2G_N\Pi_X
 \quad\hbox{(pressure)}.
\]

They agree for a pure vacuum with `p_X=-epsilon_X`; they do not agree for a
general evolving clock or effective fluid. Their common static-vacuum value
does not select their dynamics. The repository's `L273_desi_a0z_band.py`
already made the forward pressure/density distinction. The present additions
are the inverse integration constant, the dust-insensitive pressure test and
the identifiability/conditioning audit. In `stage17_a0z_from_the_action_2026.py`,
the promotion `a0²=kappa² G_N(-K)` remains an input to that construction;
deriving its consequences does not derive the promotion itself.

## 2. Pressure alone leaves a conserved integration constant

For a separately conserved homogeneous sector,

\[
 \dot\epsilon_X+3H(\epsilon_X-\Pi_X)=0,
 \qquad \frac{d(a^3\epsilon_X)}{da}=3a^2\Pi_X.
\]

On a monotone expanding interval with `a>0`, its inverse is

\[
 \epsilon_X(a)=a^{-3}\left[C+3\int_{a_*}^{a}
                   \tilde a^2\Pi_X(\tilde a)\,d\tilde a\right].
\]

One density boundary value fixes `C`. For constant positive pressure magnitude,

\[
 \epsilon_X=\Pi_0+D a^{-3},\qquad
 w_X=-\frac{\Pi_0}{\Pi_0+D a^{-3}}.
\]

Every `D>=0` gives a positive-density family with the same constant `Pi` and
the same pressure-promoted `a0`. Only `D=0` gives `w=-1`. This integration
constant is a mathematical homogeneous dust term, not evidence for a new
particle species. A clock-charge interpretation would require the common
action and its stress tensor. Energy exchange with other sectors changes
the continuity equation and hence this inverse.

Even acceleration is not inferred from `Pi` alone: for this component
`epsilon_X+3p_X=D a^-3-2Pi_0`. In the Einstein-form acceleration equation its
contribution changes sign at `D a^-3=2Pi_0`; ordinary sources also contribute.

For density promotion, conservation instead fixes

\[
 w_X=-1-\frac23\frac{d\ln a_0}{d\ln a}.
\]

For pressure promotion, on a region with `w_X<0` and positive density,

\[
 \frac{d\ln\Pi_X}{d\ln a}
 =\frac{1}{w_X}\frac{dw_X}{d\ln a}-3(1+w_X),
 \qquad \frac{d\ln\Pi_X}{d\ln a}=2\frac{d\ln a_0}{d\ln a}.
\]

This is a first-order equation for `w_X`, requiring a boundary value. Treating
the density-promotion formula as a pressure inverse removes a physical
integration constant by assumption.

## 3. A pressure test that cancels the dust split

Suppose the background equations take the Einstein form with constant
`G_cosm=g G_N`, or define an effective stress through that form. Write
`K=k c²/a²`. Then

\[
 \epsilon_{\rm tot}=\frac{3c^2}{8\pi G_{\rm cosm}}(H^2+K),
 \qquad
 p_{\rm tot}=-\frac{c^2}{8\pi G_{\rm cosm}}
                   (2\dot H+3H^2+K).
\]

Subtract independently justified ordinary-source density and pressure to
obtain an effective `X` sector. In modified gravity these formulas can define
a geometric effective fluid; they do not prove it is a material field.
Constitutive equations and perturbations must come from the action.

For flat space and negligible ordinary pressure, define

\[
 Q=2\dot H+3H^2
   =3H^2-(1+z)\frac{dH^2}{dz}
   =H^2(1-2q_{\rm dec}).
\]

Then `Pi_X=c²Q/(8 pi g G_N)`. The pressure promotion predicts

\[
 a_0^2=\frac{\kappa^2c^2}{8\pi g}Q,
 \qquad
 \boxed{\mathcal N(z)=
 \left[\frac{a_0(z)}{a_0(0)}\right]^2\frac{Q(0)}{Q(z)}=1}.
\]

The ratio requires `a0(0) != 0` and `Q(z)>0`. With `H=H0 E(z)`, constant
`H0`, `kappa` and `g` cancel in this theoretical ratio. Observational
distance calibration and cross-covariance do not automatically cancel.

Set `F=H²` and differentiate with respect to `a`. The exact identity

\[
 a\frac{d}{da}(F+D_Ha^{-3})+3(F+D_Ha^{-3})=aF'+3F
\]

shows why no assumed pressureless dark-matter abundance enters `Q`. This
does not assume the existence of such particles. It means background
pressure cannot determine an arbitrary conserved dust contribution.

Conversely the proposed pressure law predicts the entire family

\[
 \frac{d(a^3H^2)}{da}=B a^2 a_0(a)^2,
 \quad B=\frac{8\pi g}{\kappa^2c^2},
 \quad H^2=a^{-3}\left[C_H+B\int_{a_*}^a
                   \tilde a^2a_0(\tilde a)^2d\tilde a\right].
\]

Constant `a0` gives `H²=B a0²/3+D_H a^-3`. The resemblance to the usual
vacuum-plus-dust background is an equation-level degeneracy; it neither
requires particle dark matter nor establishes a microscopic replacement.
This type of background ambiguity is known in the literature; see the
[source check](../SOURCE_CHECK.md).

If ordinary pressure is not negligible, use
`Pi_X=c²(Q+K)/(8 pi G_cosm)+p_ordinary`; curvature and radiation corrections
must be included before testing the ratio. Running couplings introduce
`kappa(z)²/g(z)` into it. A departure from one tests the combined hypotheses,
not uniquely the existence or nature of dark energy.

## 4. A local acceleration inverse has a kernel-dependent domain

For the isolated, spherical, unfiltered, ungated algebraic laws only, put
`r=g_bar/g_obs`, with `0<r<1`, and `L=-ln(1-r)>0`. The two inverses are

\[
 a_{0,\mathrm{RAR}}=\frac{g_{\rm bar}}{L^2},
 \qquad
 a_{0,\mathrm{AQUALexp}}=\frac{g_{\rm obs}}{L},
 \qquad \frac{a_{0,\mathrm{AQUALexp}}}{a_{0,\mathrm{RAR}}}=\frac{L}{r}.
\]

They solve respectively `g_obs=g_bar/(1-exp(-sqrt(g_bar/a0)))` and
`g_bar=g_obs(1-exp(-g_obs/a0))`. They are not interchangeable inversions of
the same interpolating law. Both give `a0≈g_obs²/g_bar` in the deep regime.
At fixed `g_bar`, the absolute logarithmic sensitivities to `g_obs` are

\[
 C_{\rm RAR}=\frac{2r}{(1-r)L},\qquad
 C_{\rm AQUALexp}=1+\frac{r}{(1-r)L}.
\]

Both approach 2 as `r→0` and diverge as `r→1`. Thus the near-Newtonian inverse
is ill-conditioned. Values `r>=1` have no finite positive inverse in these
enhancement-only laws. Real uncertainties cannot be ignored by cutting such
points silently.

The present theory uses filtered, gated `nu_mono`. Its general inverse must
solve the physical source-to-force problem with geometry, the filter,
boundary conditions and environments. Even where `nu_mono` matches RAR
locally, a nonlocal filter prevents an arbitrary pointwise inverse. The
formulas above are controls and limiting cases, not a substitute galaxy fit.

## 5. Executed evidence and scope

`run1/results.json` records 21 exact symbolic checks, six numerical forward/
inverse controls across `r=0.001…0.999` and six synthetic expansion epochs.
The chosen illustration `w0=-0.8, wa=-0.4` is not a DESI fit. It obeys the
pressure ratio exactly while a density-promoted scale inserted into that
pressure test fails by more than 20% at the largest illustrated redshift.

`InversePressure20260926.lean` states the integrating-factor derivative,
the constant-pressure dust family, uniqueness after one density boundary,
the cost of setting pressure magnitude equal to density, dust cancellation
and the normalized algebraic null. The compiler record establishes only
these statements. It does not formalize the Einstein equations, the complete
integral inverse, data reduction or the microscopic field-to-stress bridge.
See the campaign's verification record for accepted compile attempts.

The standalone [figure](plot_run2/inverse_relationships.pdf) illustrates
the two distinct promotions and the free constant-pressure density family.
