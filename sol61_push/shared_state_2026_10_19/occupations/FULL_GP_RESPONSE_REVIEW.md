# Independent focused review of the full-GP static l=1 response

2026-10-19. Reviewer: sibling occupations lane. Requested by the parent.
No scientific rerun; only raw equation/code inspection, independent algebra,
existing-output inspection and read-only runner-v2 validation.

**Verdict: computationally verified only in the stated finite BVP range.**
The physical source signs, GP/baryon linearization, COM removal, radial
transformation and quadratic-work identity are correct under the declared
GP plus gamma=5/3 baryon closure. The positive responses in the five tested
source directions are responses about the *same numerical stationary
background*. They neither identify it as a certified constrained minimum
nor prove the complete dynamical spectrum or a positive spectral gap.

## Exact target and evidence

The code audited is
`equilibrium/static_response/check_static_response.py`, SHA256
`a652369330535cc46fbda80929c5714c174297a1fdd8d9d519d9254c206fc9eb`.
Its parameters have SHA256
`78001f1c5d64b3798ce88b16fdd67920b9a79a74fec203c37f0d0fa4c3fe563f`.
The final raw note `equilibrium/static_response/STATIC_RESPONSE.md` was
read after it was frozen, SHA256
`bbbf5e6abf9c93b00b0d96e35af0ced840ef117556efa51e74e5eb5130d453c1`.
The two pinned background files are `equilibrium/run_002/profiles.json`
(`9af24bea714233fd6428495d6b77c65d01efec510c4961e39825f1598ad2c74c`)
and `equilibrium/run_002/results.json`
(`60c5810456f95f50ca0c21fbf485a82750b7db32c449e56bea617f7fa3077df3`).

Observed audit HEAD: `0260149521dd8f672e89397d255974c9e7b7cd8d`.
These are concurrent research files; byte hashes control the reviewed
revision. The run uses `tau=.05,L=14,4piG=1,K=.5,Kb=.4` and the existing
fine stationary background. Its baryon edge is `Rb=2.444647172511382`.
There are five sources at two BVP tolerances, `2e-5` and `2e-7`.

The documented v2 validator was executed with project root against
`equilibrium/static_response/run_002/manifest.json`; it reports
`valid evidence record (run status: completed)`. The actual run took
0.813 seconds under 45-second wall, 30-second CPU, 65536-byte log and
one-thread caps, with empty stderr. No rerun, background regeneration,
resource escalation or source/action edit was performed for this review.

## Independent equation and sign reconstruction

The background obeys

\[
 -\tau\nabla^2f_0+(2Kf_0^2+U_0)f_0=\mu_df_0,\qquad
 (5/2)K_b\rho_{b0}^{2/3}+U_0=\mu_b.
\]

For the *common* applied potential `Ue=-E phi(r) cos(theta)`, use
`delta f=s(r)cos(theta)`, `delta U_self=v(r)cos(theta)` and a COM
multiplier `lambda r cos(theta)`. In the l=1 channel the mass multipliers
have no independent l=1 variation. Direct differentiation gives

\[
 L_ds+f_0v=f_0(E\phi+\lambda r),\quad
 L_d=-\tau\Delta_1+6Kf_0^2+U_0-\mu_d,
\]
\[
 b=\kappa(E\phi+\lambda r-v),\qquad
 \kappa=\frac3{5K_b}\rho_{b0}^{1/3},\qquad
 \Delta_1v=4\pi G(2f_0s+b).
\]

The factor `6K` comes from differentiating the scalar cubic, and the
positive sign of the force term follows from `Hsrc=-E D`. The baryon
susceptibility is the reciprocal derivative of its enthalpy:
`dhb/drhob=(5/3)Kb rhob^(-1/3)`. Since
`rhob=[(mu_b-U0)/(2.5Kb)]_+^(3/2)`, the code's square-root formula for
`kappa` is exactly this expression. The same self-potential `v` couples
to both fluids and is sourced by their total perturbed mass density.

The moving baryon edge causes no separate first-order surface mass delta:
the background density vanishes there as enthalpy to the power `3/2`.
The response coefficient `kappa` vanishes as the square root. This statement
uses the declared gamma=5/3 fluid closure and regular background edge,
not an arbitrary discontinuous-density EOS.

## COM boundary conditions and source projection

The regular origin has `s,v=O(r)`. At the finite Dirichlet scalar boundary,
`s(L)=0`. Imposing `v(L)=v'(L)=0` removes the exterior total l=1 mass
dipole. The free parameter `lambda` supplies the additional constraint,
so these conditions are consistent rather than an unexplained overconstraint.
In fact direct integration of the radial Poisson equation proves

\[
 \frac{4\pi}{3}\int_0^Lr^3(2f_0s+b)dr
 =\frac{4\pi/3}{4\pi G}[L^3v'(L)-L^2v(L)].
\]

This is precisely the code's independent boundary/volume COM moment.
It checks the total source, including live baryons, and not just a scalar
subsystem dipole. A finite box and the interpolated stationary background
remain numerical approximations to the continuum object.

For an affine source `phi=r`, `lambda=-E,s=b=v=0` is the exact internal
solution. It is correctly reproduced by both tested tolerances. This
checks free-fall cancellation but does not prove uniqueness of the full
constrained operator in all perturbation sectors.

For a finite-k l=1 source, `phi=3j1(kr)/k`, the code solves with
`phi/r-1` and `ell=lambda+1` for unit amplitude. It reports the physical
frame multiplier `lambda=ell-1`. Subtracting `r` from the source changes
only its COM multiplier, because `int z delta rho=0`. Hence the direct
and projected susceptibilities differ exactly by the affine COM moment;
the code separately monitors this identity. The small-z series
`3j1(z)/z-1=-z^2/10+z^4/280-z^6/15120+z^8/1330560+...` is correct.

**Finite-k scope:** this is only the l=1 component of `sin(kz)/k`.
The l=3 component contributes at the same leading susceptibility order
`k^4` to the full plane-wave source. The code therefore supplies the
full-GP *l=1* response, not the complete finite-k response. Comparing it
with `k^4 chi_cubic/100` is the correct l=1-only small-k comparison.

## The transformed boundary-value system

Set `s=r a,v=r B` and store the *radial* derivatives `a_r,B_r`.
Then `Delta1(r a)=r a_rr+4a_r`, so

\[
 a_{rr}=-4a_r/r+(Va+f_0B-f_0F)/\tau,\qquad
 B_{rr}=-4B_r/r+4\pi G[2f_0a+\kappa(F-B)],
\]

where `V=6Kf0^2+U0-mud` and `F=phi/r+lambda` at unit amplitude.
These are exactly the code's radial equations.

The inner mapping `r=Rb t(2-t)` has
`r_t/r=1/t-1/(2-t)`. Thus its derivative equation contains
`-4a_r/t+4a_r/(2-t)`; the singular `-4/t` term is correctly assigned
to the solver's `S` matrix, and the regular remainder is in its RHS.
The outer mapping `r=Rb+(L-Rb)t^2` has the ordinary friction
`-4r_t/r`. Both maps have zero first derivative at the baryon edge,
which smooths the square-root coefficient in the respective coordinates.
Matching the stored fields and *radial* derivatives at that edge is the
correct physical matching; matching derivatives with respect to the two
different `t` coordinates instead would be incorrect.

The solver has eight first-order fields and one multiplier, with the
required nine boundary/matching conditions: two regular-center conditions,
three outer conditions, and four interface matches. The supplied analytic
Jacobians agree with this linear system.

## Independent quadratic-work identity

Multiply the scalar response equation by `2s`, integrate by parts, and
multiply the baryon response by `b/kappa`. On adding the two equations,

\[
 \int\left[2\tau|\nabla(sY_{10})|^2+2V(sY_{10})^2
             +\frac{(bY_{10})^2}{\kappa}
             +(2f_0s+b)vY_{10}^2\right]d^3x
 =\int(2f_0s+b)(E\phi+\lambda r)Y_{10}^2d^3x.
\]

Here `Y10` denotes `cos(theta)`, without unit-normalized-harmonic
notation; its angular norm is `4pi/3`. The COM constraint removes the
multiplier term. For unit source amplitude the right side is the static
susceptibility. Radial integration gives the code's terms
`2tau(s'^2+2s^2/r^2)+2V s^2+b^2/kappa+delta rho_total v`.
The gravitational term has the *plus* sign in this expression but is
negative after solving the self-potential; gravity has not been counted
twice or assigned a positive field energy. The code evaluates `b^2/kappa`
as `kappa r^2(F-B)^2`, avoiding a division at the vanishing edge.

## Finite result, obligations and remaining gap

The fine-source susceptibilities are:

| source | projected susceptibility | relative work discrepancy |
|---|---:|---:|
| affine | 0 | 0 |
| cubic r^3 | 513.119479822 | 2.22e-9 |
| q=.1 | 1.434895424e-5 | 3.66e-9 |
| q=.3 | .001150901060 | 3.01e-9 |
| q=1 | .127086793041 | 3.43e-9 |

Here `q=kRb`. The cubic coarse/fine susceptibility change is `2.77e-10`;
the largest reported change over the five sources is also `2.77e-10`.
Some finite-k cases use the same 301-node solution at both requested
tolerances because the first solution already satisfies the tighter
residual. Such zero change is a tolerance check on the same discretization,
not an independent refinement check or evidence of continuum error bounds
or certified digits. The q=.1 projected quadrature error estimate is
1.81e-9 absolute, or 1.26e-4 relative; agreement of the correlated work
integrals to 3.66e-9 does not improve that accuracy certificate. These are
floating quadrature estimates, not rigorous bounds. Fine solver residuals are
at most `1.995e-7`. The largest fine volume COM residual is `3.78e-7`
for the large cubic response; the boundary COM moment is essentially
zero. The finite-k direct/projected difference follows the small residual
COM moment rather than an omitted physical affine response.

The final note's dimensional conversion is also correct for the length-valued
finite-k source. If `a,hc,rho_unit` are length, specific-potential and density
units, then `Dphysical=rho_unit a^4 Ddimless` and
`Ephysical=(hc/a) Edimless`. Therefore
`chiphysical=rho_unit a^5 chi_dimless/hc`. Using
`4piG rho_unit a^2/hc=1` gives `chiphysical=a^3 chi_dimless/(4piG)`.
The corresponding per-volume coefficient retains the actual averaging
volume, probe wavelength and state dependence. This source-unit conversion
does not apply unchanged to the differently dimensioned cubic source.

- Equation/source signs, baryon derivative and physical shared source:
  **passed** by independent reconstruction.
- COM elimination, affine test, transformed ODE and interface conditions:
  **passed** within the declared finite-box problem.
- Quadratic-work identity and angular factor: **passed** analytically;
  the reported finite evaluations agree to the stated precision.
- Ten BVP cases: **finite numerical evidence only**, with validated
  provenance and explicit tolerances.
- Full sine-source angular response: **not computed**; only l=1 is covered.
- Identifying the stationary output with a certified continuum minimum,
  proving all-sector Hessian positivity, or obtaining the dynamical
  spectrum/gap: **not established by this calculation**.
- Local saturators, occupations, abundance and universal gravity/acceleration
  normalization: **outside the demonstrated result**.

The next distinct obligation is a constrained dynamical/Hessian analysis
of this same full-GP stationary candidate. Repeating the static solve or
interpreting positive work in these five directions as a full stability
certificate would not discharge that obligation.

## Final note-hash reconciliation

The author subsequently clarified only the integral typography in equations
(4) and (8): `r^3 d(r) dr` and `r^2 d(r)F(r) dr`. These explicitly denote
the density and its product with the source; they agree with the integrands
audited above and change no mathematical assertion or numerical value.
The final note SHA256 is
`1897068fda6e265e25d513e50da1d0381d15af4040c5410610af13e53490e743`.
The append-only `static_response/NOTE_RECONCILIATION.json` has SHA256
`d0a42e37bb641258ba094374abbf2f408c98d55576d56972a0fa3532ec955e37`.
I checked its two exact replacements against the final note and reversed
them in memory: the reconstructed bytes have the originally reviewed hash
`bbbf5e6abf9c93b00b0d96e35af0ced840ef117556efa51e74e5eb5130d453c1`.
Thus the review applies to the clarified final note. The code, parameters,
background and completed run are unchanged; no scientific rerun is needed
or performed. The finite stationary-background scope and all qualifications
in this review remain in force.
