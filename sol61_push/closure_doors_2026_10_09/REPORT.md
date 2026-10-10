# Four closure doors: first calculation and handoff

October 9, 2026. Base c8d5893d6a543495c464dbb3905574e3432a7475.

**The finite-halo door earns a conditional theorem, but its first profile family misses the target shape.** The other three doors have bounded work orders in NEXT_STEPS.md. They have not been simulated.

The comparison target here is the October 9 cold-energy framework's spherical RAR law with a finite supply, not the previous modified-gravity filtered-MONO target. We use an effective force-to-density interpretation. No cold-matter distribution function, stress tensor, actual capture process, lensing law or covariant action is derived.

## 1. Finite susceptibility gives a positive, finite spherical halo

Let mu be a nonzero finite positive measure on (0,infinity), with finite
chi=integral dmu(E)/E, and let eta>0. Define
\[
I(e)=\int\frac{d\mu(E)}{E+e},\quad
J(e)=\int\frac{d\mu(E)}{(E+e)^2},\quad
K_3(e)=\int\frac{d\mu(E)}{(E+e)^3}.
\]
The coupled discrete-state model has ground energy -e(D), where
e=D^2 I(e). Use the previously specified constitutive map
g=D+eta e'(D). In this section D is the Newtonian acceleration in the chosen units.

The excess enclosed-mass ratio is
\[
S(D)=\eta e'(D)/D=\frac{2\eta I^2}{I+eJ}.
\]
Set x=D^2=e/I. Direct differentiation gives
\[
x'=\frac{I+eJ}{I^2}>0,\qquad
x''=\frac{2[(J-eK_3)I+eJ^2]}{I^3}>0,
\]
since J-eK_3=integral E dmu/(E+e)^3>0. Thus S decreases strictly with D. Moreover
\[
e''(D)=\frac{2I^2}{(I+eJ)^3}
\left[(I-eJ)^2+4e^2(IK_3-J^2)\right]>0,
\]
using Cauchy–Schwarz IK_3>=J^2. This is an algebraic proof independent of a ground-state convexity assertion.

Dominated convergence gives I->chi and eJ->0 as e->0; no finite inverse-square moment is required. At large e, S<=2eta I->0. Therefore
\[
\boxed{S(0)=2\eta\chi,\qquad S(\infty)=0.}
\]

For nonnegative spherical baryons, set
D(r)=G M_b(r)/r^2 and M_c(r)=M_b(r)S(D(r)). At positive r,D,
\[
\frac{dM_c}{dr}=
[S+DS']M_b'-\frac{2M_bD}{r}S'\ge0,
\]
because S+DS'=eta e''>0, S'<0, and M_b'>=0. If M_b tends to a positive finite M_infinity,
\[
\boxed{M_c(\infty)=2\eta\chi\,M_\infty.}
\]
For locally absolutely continuous M_b this gives nonnegative effective density almost everywhere. More general nondecreasing M_b gives a nonnegative mass measure, possibly including shells: at fixed r, m->mS(Gm/r^2) is nondecreasing, so jumps preserve positivity. The zero-baryon case is trivial and has no defined mass ratio.

This produces finite positive effective halos without imposing a hard radial cutoff. It does not explain why actual cold energy occupies those halos.

## 2. The detuned bath fixes chi in closed form

Use the normalized Gaussian source and nu=1/3 from
../week_review_2026_10_08/critical_bath/REPORT.md. For positive boundary parameter zeta, the zero-energy Green kernel is
\[
G_\zeta(r,s)=G_+(r,s)
+\frac{(rs)^{1/2-\nu}}{2\nu\zeta}.
\]
The added term changes the origin coefficient ratio to b/a=zeta and solves the homogeneous zero-energy equation; its normalization follows from the Wronskian 2nu. Integrating it against the source gives
\[
\boxed{\chi_\zeta=
\frac{2^{1-\nu}-1}{\nu}
+\frac{2^{-2\nu}\Gamma(1-\nu)}{\nu\zeta}.}
\]
This is checked independently against the mixed-Bessel spectral measure.

For the scout we explicitly calibrate eta=5.364/(2chi_zeta). Thus the mass budget is an input, not a selected prediction. Normalize acceleration by a_toy=(9/4)eta^2 Gamma(1/3)^{3/2}. For sizeable zeta this is the coefficient of the corresponding critical reference model, not a claimed actual intermediate scaling regime.

The dimensionless comparison is
\[
g_{\rm target}/D=
1+\min\left(5.364,\frac1{\exp(\sqrt y)-1}\right),
\qquad y=D/a_{\rm toy}.
\]
It is the full-retention point-source capped RAR comparison only. It does not represent every census retention, a disk, or the old filtered-MONO tail. Dimensionless conclusions apply to either physical a0 footing after its own conversion.

## 3. Bounded scout: shape still needs work

Five zeta values were declared before running; no optimizer or observed galaxy data were used. The illustrative pass gate was maximum total-force discrepancy <=0.05 dex at eleven specified y values from .001 to 100.

| zeta | calibrated eta | maximum force error, dex | shape gate |
|---:|---:|---:|---|
| .001 | .0010473 | .18275 | fail |
| .01 | .0104085 | .18417 | fail |
| .1 | .0980499 | .19787 | fail |
| 1 | .620643 | .28418 | fail |
| 10 | 1.32896 | .38676 | fail |

All five have the stipulated finite outer mass and positive density. The failure is force shape, not negative mass. It is not an observational exclusion of the broad mechanism, nor an exhaustive exclusion of all zeta or other source profiles.

There is a structural distinction from a hard supply edge: S'<0 implies M_c'(r)>0 outside a nonzero point source at every finite radius. This rank-one positive-measure equilibrium mechanism approaches its finite mass asymptotically; it cannot produce an exactly empty outer halo beyond a finite edge. A sharp capture boundary would require additional dynamics or a changed model.

**Decision:** retain the positivity/finite-mass theorem. Do not substitute this Gaussian bath profile for the current successful kernel. For a smooth-edge candidate, the next narrow test is whether another independently motivated source measure improves the shape while preserving the theorem. If an exact capture edge is required, move that task to the transport/occupation dynamics in NEXT_STEPS.md. The bath can separately be tested as an energy receiver for settling.

## 4. Evidence and remaining work

830 finite checks pass in runs/main: normalizations, analytic versus spectral chi, derivative signs at 81 energies per model, asymptotic mass and high-field limits. These counts are implementation checks, not 830 independent physical tests. The density-sign mutation fails all 405 mass-monotonicity checks as intended. Both provenance manifests validate and both stderr logs are empty. Shape-gate failures are reported separately and do not count as failed implementation checks.

The primary analytic theorem was independently checked by a second agent, which supplied the direct e'' proof and the mass-measure regularity caveat. The lead verified and incorporated those changes. No independent audit of a complete physical theory was performed.

checks.py, contract.json and manifests retain the exact grid, bounds, software, hashes and resource limits. Log-energy integration uses [-140,40]; the force table uses shape-preserving interpolation of 81 sampled energies. Near the cap, interpolation and finite sampling are limitations: the table is a scout, not a continuum error supremum or precision data fit.

The other doors remain executable proposals, not results. No work here selects the cold abundance, physical conversion factors, nu=1/3, k=1/2 or 32pi^2.
