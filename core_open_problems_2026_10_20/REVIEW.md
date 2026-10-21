# Coordinator's mathematical review

Review date: 2026-10-20. Base definitions are pinned in `BASELINE_INPUTS.json`.
This review is separate from the workers' independent initial investigations.
Agreement between workers is not a proof certificate.

## Shared normalization and law claims

**Claim 1 — exact algebra under the stated conventions.** Let dark-energy density
mean mass density, \(H_\Lambda^2=8\pi G\rho_{\rm DE}/3\), and
\(a_H=cH_\Lambda\). Then

\[
\frac{a_0}{a_H}=\kappa\sqrt{\frac3{8\pi}}
=\frac1Z\quad(\kappa=1/2),\qquad Z=\sqrt{\frac{32\pi}3}.
\]

Thus \(a_0/a_H=0.172747\), while \((a_0/2)/a_H=0.0863735\).
The latter fraction can refer to the baryonic acceleration at \(g=a_0\)
in the simple law, or to an assigned ambient scale in the quadratic
temperature-excess law. Those are different statements. Neither calculation
derives a physical switch at a fraction of the horizon acceleration.

**Claim 2 — exact static law distinction.** For \(n>0\), \(0<u<a_0/n\),
\(\bar g=u^2/(a_0-nu)\) is strictly increasing, since

\[
\frac{d\bar g}{du}=\frac{u(2a_0-nu)}{(a_0-nu)^2}>0.
\]

It maps the interval onto positive accelerations, so there is exactly one
positive rest-state root for every \(\bar g>0\). The endpoint
\(\bar g=0\) gives \(u=0\). Substitution into \(g=\bar g+u\)
gives the two distinct laws stated in `CONTRACT.md`. Positivity here is a
static monotonicity statement; it does not establish relativistic stability.

**Claim 3 — exact maximum difference at a common footing.** Write
\(y=\bar g/a_0>0\). For unscreened, aligned spherical configurations,

\[
R(y)=\frac{g_1}{g_2}
=\frac{\sqrt y+\sqrt{y+4}}{2\sqrt{y+1}},\qquad
R^2=\frac{y+2+\sqrt{y^2+4y}}{2(y+1)}.
\]

The derivative of \(R^2\) has the sign of
\(-1+(2-y)/\sqrt{y^2+4y}\). For \(y\ge2\) it is negative.
For \(0<y<2\), comparison of the positive terms reduces to
\((2-y)^2-(y^2+4y)=4-8y\). The unique maximum is therefore
\(y=1/2\), where \(R=2/\sqrt3\). At fixed radius the circular-speed
ratio is \(\sqrt R=1.07456993\). This is a conditional model
discriminator, not a predicted observational significance; baryonic calibration,
geometry, environmental fields, and stiffness must be controlled before using it.

**Claim 4 — surface-density geometry.** If spherical acceleration is \(u(r)\),
Gauss's law gives \(M_{\rm ph}(<r)=u(r)r^2/G\), hence
\(\bar\Sigma_{\rm enclosed}=u(r)/(\pi G)\). An infinite symmetric
sheet instead obeys \(u=2\pi G\Sigma\). A projected spherical column
also includes mass outside the enclosing sphere. Consequently, the enclosed
surface-density capacity is not a universal projected-lensing bound. This
restriction follows directly from the geometries, before any lensing completion
is chosen.

The original source action, these algebraic identities, and finite implementation
checks have distinct roles. `review_checks.py` tests 198 exact rational examples,
cross-checks 402 positive accelerations at 70-digit precision, and checks all seven
baseline snapshot hashes. The proofs above supply the continuous-domain argument;
the numerical grid supplies only an implementation check.

## Scope of this checkpoint

The four requested physical origins remain research targets. A report may prove
an obstruction for a specified class without excluding theories outside that
class. The primary verdict for each original physical-origin claim is
**incomplete, with the named missing implication**.

## Lane audit and restrictions

| Lane | Coordinator check | Safe conclusion |
|---|---|---|
| Horizon | Read the scalar-readout regularity argument, detector Fourier calculation and finite-probe entropy calculation; reran the self-contained script. | Analytic temperature-only readout cannot give the exact simple law; thresholds in the specified detector class depend on probe inputs. No universal QFT exclusion or κ derivation. |
| Medium | Reconstructed the potential integral, endpoint powers, three statistical dictionaries, kinetic gradient flow, speed-ratio maximum and density geometries. | The specified regular equilibrium models fail; kinetics reproduces the root conditionally. n remains free. |
| Relativity | Checked static potential variations and the polarized shift elimination. A different worker rederived the zero-P scalar and TT blocks from the raw action before comparison. | Leading static S2 and the stated principal blocks agree. S3 embedding and full physical-background stability remain open. |
| Stiffness | Checked the gravitational elimination and directional Hessian, bond-kernel expansion, pressure/shear distinction, and quantum-pressure derivative count. | L* is a free gradient coefficient in S2; its response scales depend on background and direction. None of the three microscopic dictionaries fixes its value. |

The regular-equilibrium obstruction assumes analyticity and inversion symmetry;
it does not exclude critical thermodynamic limits, gapless states, or driven
media. The kinetic construction is not promoted to a thermodynamic force law.
The finite-stiffness supplement gives a trial-profile residual, not a bound on
the actual velocity error. At 1 kpc the canonical residuals are approximately
4.23% and 3.23%, so the unscreened speed discriminator cannot simply be asserted
throughout the entire stiffness interval.

For the relativistic candidate, independently eliminating the shift variable Y
from

\[
L=\frac\eta2(\dot q-PY)^2-\frac\beta{4K}Y^2
-\frac\gamma2k^2q^2
\]

gives \(Y=-2K\eta P\dot q/D\) and
\(Q=\eta\beta/D\), with \(D=\beta-2K\eta P^2\).
Thus the stated adverse sign and rank-loss locus follow for this supplied
aligned high-frequency block. This calculation verifies its reduction, not
the entire constrained spectrum on a physical halo. The strict endpoint margin
differs from positivity at every finite interior polarization, and an EFT
requires the tested wavelengths to lie below its cutoff.

A material scope issue found during review was corrected in the report:
exact Minkowski at Λ = 0 and finite a₀ treats those parameters independently.
Under S1's relation to cosmological-constant dark energy, that is an auxiliary
family, not the physical zero-acceleration endpoint. A de Sitter calculation
is still required. The candidate's physical one-form P also does not establish
the original conserved mass/current interpretation. These restrictions are
part of the result, not future optional refinements.

For stiffness, the direction-dependent kernel is a positive sum
\(K[B I+(A-B)ee^T+\Pi_T]+\gamma k^2I\) for \(0<s<1\),
since \(B>0\), \(A-B=s/(1-s)^2>0\), and \(\Pi_T\) is a
positive projector. This supplies the all-direction static argument; the
91-matrix scan is only a numerical control. The finite-range lane's η is a
dimensionless bond strength, while the relativity lane's η is a dimensionful
kinetic coefficient. No identification between these unrelated parameters is
being made. The contact-fluid map does not preserve a collisionless medium
automatically, and pressure alone supplies no transverse shear stiffness.

## Reproduction receipt

`verify_bundle.py` re-executed seven commands: all four primary scripts, the
medium's stiffness supplement, the independent relativity review, and the
coordinator's shared-convention check. All exited successfully and reproduced
their mathematical outputs. See `verification.json` for exact script and
reference-output hashes, runtimes, and the observed package versions.

The primary lane records contain 43, 75, 34 and 40 checks respectively; the
independent review contains 16. These are heterogeneous assertions and finite
controls, not a count of established physical predictions. The relativity
author used Python 3.13.9/SymPy 1.13.1; the coordinator used Python 3.9.6/SymPy
1.14.0. Mathematical outputs agreed; software metadata necessarily differed.
The replay comparison preserves check names and pass flags and permits relative
floating-point rounding of 1e-10, with no absolute tolerance that could hide a
nonzero value. Original numerical residual diagnostics remain in lane records.

The horizon and medium lanes retain their failed symbolic-library attempts.
The stiffness lane retains a superseded first run that copied an incorrect SI
conversion; the final version checks dimensions and an independent benchmark.
Those historical records are not represented as current successful evidence.

The shared repository advanced through unrelated commits while this work ran.
The dispatch revision and exact source bytes remain pinned. The release adds
only this package on a separate branch based on the inspected remote revision;
it does not rewrite shared theory statements, existing predictions, or the
user's working branch. Source snapshots are documentary evidence and are not
new endorsements of every historical claim they contain.

Final proofreading covered the five new reports, this review, the contract,
and the overview. No unresolved notation error was identified in that scope.
Remaining mathematical and physical obligations are explicitly listed above
and in the lane reports; proofreading does not validate them.
