# A particle-free auxiliary action for unit response: theorem and remaining normalization

Date: 2026-09-20. Investigation began at `928c61c79b4a74bd47ecf515be19da2342cde093`;
the concurrent PD08 update at `89f5ef2e7d8079de87fd86d2f1ada0c6c5992905` was also
read and checked. Original research files are unchanged.

**Result:** an explicit particle-free static action yields the requested chain
by variation: its two equal-weight auxiliary responses have \(p(0)=0\),
\(p'(0)=1\), \(\mu'(0)=2\), and spherical deep-MOND matching gives
\(\kappa=a_0/s=1/2\). **The equal relative weight is an explicit new action
assumption; we have not derived that choice from the existing covariant action,
the independently fixed vacuum scale, or channel counting.** The generalized
action and Lean certificate retain this freedom rather than conceal it.

No dark-matter particle, species mass, independent halo density, or new
propagating matter field is introduced. This is a static gravitational action
with two algebraically eliminated auxiliary variables, not a completed
relativistic or cosmological theory.

## Exact theorem

Fix \(G,s>0\) independently of \(a_0\); when using the repo's vacuum convention,
\(s=c\sqrt{G\rho_\Lambda}\), with \(\rho_\Lambda\) a mass density. Let
\(y=|\nabla\Phi|/s\ge0\), and let the two nondynamical scalar variables have the
explicit field domain \(0<q_1,q_2\le1\). Define

\[
 U(q)=\frac{q^2}{2}-2q+\log q+\frac32,
 \qquad
 W_\lambda(y,q_1,q_2)=y^2(1-q_1q_2)
                   +\frac{U(q_1)+U(q_2)}{\lambda^2},
 \quad \lambda>0,
\]
\[
 S_\lambda=-\int \left[
       \frac{s^2}{8\pi G}W_\lambda(y,q_1,q_2)+\rho_b\Phi
                         \right]d^3x.
\]

**Theorem.** At each \(y\ge0\), the auxiliary stationarity equations have exactly
one solution in the stated domain:

\[
 q_1=q_2=\frac1{1+\lambda y},\qquad
 p_i:=1-q_i=\frac{\lambda y}{1+\lambda y}.
\]

Eliminating them gives the constitutive field equation

\[
 \nabla\cdot[\mu_\lambda(|\nabla\Phi|/s)\nabla\Phi]
       =4\pi G\rho_b,
 \qquad \mu_\lambda(y)=1-(1+\lambda y)^{-2}.
\]

Thus \(p_i(0)=0\), \(p_i'(0^+)=\lambda\), and \(\mu_\lambda'(0^+)=2\lambda\).
For an isolated spherical source with no extra central flux, the deep limit
matches \(g^2=a_0g_N\) with

\[
 \boxed{\frac{a_0}{s}=\frac1{2\lambda}},\qquad
 \boxed{\frac{a_0}{s}=\frac12\ \Longleftrightarrow\ \lambda=1}.
\]

In particular, the **specified equal-weight action** \(S_1\) yields the desired
half without assuming \(p'(0)=1\) or \(\kappa=1/2\) as separate premises.
Selecting this action remains a physical model choice. Constructing its
variational representation does not independently justify that choice.

## Proof and action normalization

Since \(U'(q)=(1-q)^2/q\), the two auxiliary equations are

\[
 (1-q_1)^2=\lambda^2y^2q_1q_2=(1-q_2)^2.
\]

The domain \(q_i\le1\) selects the nonnegative square-root branches, giving
\(q_1=q_2=q\) and \(1-q=\lambda yq\). This proves the solution and its
uniqueness; direct substitution proves existence, including at zero field.
The domain is indispensable: positivity alone permits additional stationary
branches, checked explicitly in `verify.py` and `REVIEW.md`.

On this solution,

\[
 \overline W_\lambda(y)=y^2-
 \frac2{\lambda^2}\left[\log(1+\lambda y)
                  +\frac1{1+\lambda y}-1\right].
\]

Either differentiate this reduced function, or apply the envelope identity
\(\partial_yW=2y(1-q_1q_2)\). In either case
\(\overline W_\lambda'(y)/(2y)=\mu_\lambda(y)\) for \(y>0\), continuously
extended to zero. With the displayed sign, prefactor and matter coupling,
variation of \(\Phi\) with fixed boundary data gives the stated field equation.
No parameter \(a_0\) was inserted into this action or its variations.

The selected auxiliary point maximizes \(W\), rather than minimizes it. Its
two Hessian eigenvalues are \(-2y(1+\lambda y)/\lambda\) and \(-2y/\lambda\).
Their signs do not certify time-dependent health: the auxiliary variables have
no kinetic term, and this package does not supply a covariant dynamical action.
At \(y=0\) this Hessian and the static response ellipticity degenerate.

## What selects the equal weight?

That is the remaining question. All positive \(\lambda\) preserve:

- channel-exchange symmetry and the same allowed auxiliary field domain;
- zero response at zero drive and saturation at unit response;
- a unique auxiliary solution in that domain;
- positive transverse and longitudinal static response at nonzero gradient;
- the independently specified \(s\), the same Newtonian normalization, and
  \(\overline W(0)=0\).

Their small-gradient action is

\[
 s^2\overline W_\lambda(|\nabla\Phi|/s)
   =\frac{4\lambda}{3s}|\nabla\Phi|^3+O(|\nabla\Phi|^4/s^2).
\]

Its cubic coefficient changes while the value and first two derivatives at
zero gradient stay fixed. More generally, in a covariant clock/scalar action
an allowed term proportional to \(Y^{3/2}\), with
\(Y=|D\phi|^2\), contributes only \(O(|\epsilon|^3)\) along smooth admissible
perturbations of a homogeneous state \(D\phi=0\). Background equations and
quadratic perturbation data cannot determine its coefficient by themselves.
This is a local operator-order argument, not a proof of nonlinear stability
or a construction of an observationally viable covariant completion.

Three routes were actually investigated:

1. **Auxiliary action:** the theorem above gives a complete static derivation
   for the selected equal-weight action, but also exposes its coefficient.
2. **Vacuum/flux matching:** `ACTION_ROUTE.md` constructs an explicit family
   with the same vacuum functional, conserved flux and positive flux stiffness,
   but different \(\kappa\); canonical field normalization preserves the free
   coupling ratio. Lean checks the decisive fixed-vacuum identities.
3. **Classical spectral response:** `THERMAL_ROUTE.md` derives the rational
   response from a particle-free activation integral. For normalized bounded
   gap density \(f\), continuous at zero, the infrared response is
   \(p'(0^+)=f(0)\). The required physical input becomes \(f(0)=1\) in fixed
   \(s\)-units; density normalization alone does not establish it.

No examined route independently selects \(\lambda=1\). A next proposal must
derive the relative coefficient or the physical infrared spectral weight; it
must distinguish \(\lambda=1\) from the explicit \(\lambda=2\) alternative
without defining the answer into the normalization.

## The concurrent PD08 claim

PD08's executable `p = Y + c2 * Y**2` inserts the unit derivative before
checking it. One independent dimensional scale does not remove dimensionless
shape coefficients: \(\lambda=1\) and \(\lambda=2\) above both use only \(s\)
as their dimensional acceleration scale. The cited k01 zero-mode result is
about an additive action constant and vacuum normalization; it does not
eliminate the free derivative coefficient. PD08's own final ledger lists the
unit-slope fraction identity as a premise.

There is also a minor prose sign error: the expansion is
\(\mu=2Y+(2c_2-1)Y^2+\cdots\), not \(2Y+(2c_2+1)Y^2+\cdots\). Correcting that
sign does not fix the independent normalization issue. PD08 was inspected as
source; its existing output files were not overwritten.

## Certificates, verification and novelty scope

`UnitResponse.lean` proves fourteen named statements, including auxiliary
existence and uniqueness, derivatives of the derived channel law, the
equal-weight half theorem, the half-if-and-only-if-unit-weight theorem, and
fixed-vacuum coupling freedom. The proofs use ordinary Lean foundations only.
The derivative proof uses the rational function's extension through zero;
restricting it to the physical half-line gives the stated right derivative.

`verify.py` independently differentiates the action, checks the reduced
action and flux, both auxiliary eigenvalues, excluded-branch controls, the
zero-background jet, fixed-vacuum matching and the spectral integral. It then
compiles Lean afresh and rejects compiler warnings or `sorryAx`. The exact
check count, axiom output, toolchain pin, input/output hashes, execution command
and runtime are in `run/result.json`, `run/lean.txt` and `run/manifest.json`.

`REVIEW.md` is a separate adversarial derivation; its domain and interpretation
qualifications have been incorporated here. Compilation proves the statements
in the Lean file, not the variational-calculus bridge or physical applicability.
Those are separately documented and symbolically checked.

The modified-Poisson action and MOND scaling are known structures; see
[Bekenstein and Milgrom (1984), section II](https://adsabs.harvard.edu/pdf/1984ApJ...286....7B). This note
does not claim them as discoveries. The auxiliary construction is an exact
variational representation of the selected constitutive family and provides
no additional reduced static prediction. Worldwide novelty of the particular
representation has not been established. The thermal report cites the primary
sources actually consulted. No completed cosmology, observation fit, or
first-principles selection of \(\kappa=1/2\) is claimed.

For a direct local reproduction, make a fresh output directory under this
folder, then run `python3 verify.py <absolute-output-directory>` from this
folder; it uses the repo's pinned `fable_independent_2026/lean_2026` host and
requires its existing Mathlib installation plus SymPy. The bounded execution
used for the checked-in evidence is recorded as argv in the manifest.
