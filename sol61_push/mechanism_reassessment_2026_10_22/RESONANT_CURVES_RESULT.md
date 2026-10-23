# A resolved candidate third-harmonic absorption channel

Direct integration along orbital resonances gives a stable nonzero absorptive projection near the cold collective frequency. About98.5% of this projection comes from the third orbital harmonic. The64/128 action-grid projected values agree to .0014% after direct root/coefficient refinement. This is evidence for a kinetic energy-transfer channel without added friction. It is not yet a continuum mode lifetime, a proof of global settling, a formation mechanism or a novelty claim.

## Removing artificial broadening

Let u=L², and let C_n(E,u) be the vector of eight trial-potential Fourier coefficients. The derivative-weighted phase measure is F pi T_r du dE. Taking the retarded boundary value at real positive omega gives

    B(omega)=-Im Pi(omega+i0)
      =sum_n F pi² omega integral du
          sum_(n Omega_r=omega) [T_r C_n C_n^T / |n partial_E Omega_r|].

Since T_r=2pi/Omega_r at a resonant orbit, this simplifies to

    B_n=2pi³ F integral du
          sum_roots [C_n C_n^T/|partial_E Omega_r|].

This formula assumes simple transverse roots. Tangent resonances and endpoint singularities need separate treatment. It is a continuum resonance formula; no numerical Lorentzian width appears in B itself.

Use omega=.8228 and the same finite-A10000 equilibrium, sixteen harmonics and eight field shapes. For comparing projections, hold fixed the S-normalized vector closest to a null direction of Re[S-Pi(.8228+.003i)] on the128 action grid. Its generalized eigenvalue is approximately-.00170. This is an approximate mode direction from finite broadening, not a solved real-boundary-value eigenvector. It is deliberately kept fixed across integration orders so the comparison measures quadrature rather than changes of direction.

## Endpoint and interpolation checks

At each angular-momentum node, supplement the sampled energy range with the circular-orbit frequency and zero nonconstant Fourier coefficients at its lower endpoint, plus a directly integrated cutoff-energy orbit at the upper endpoint. PCHIP interpolation supplies candidate resonance brackets and allows nonmonotonic frequency curves; the128 grid contains34 nonmonotonic rows. Both ends and all polynomial roots within each interpolation interval are considered.

An initial interpolation-only calculation gave close grid agreement but failed independent coefficient spot checks: errors reached .00123 at64 nodes and .000423 at128 nodes. That failed probe is preserved as resonant_checked_probe.json. Agreement between grids alone was therefore insufficient.

The repaired calculation refines every bracketed root using actual orbit periods, evaluates its coefficients directly, and differentiates the actual orbital frequency with respect to energy. Independent spot checks use1024 versus2048 phase nodes and a halved derivative step. Maximum coefficient differences are below2.82e-7, relative resonance errors below4.7e-12, and derivative-step differences below4.0e-7 on the checked subset.

PCHIP bracketing still does not prove completeness against a narrow unsampled pair of roots. The smallest encountered absolute energy derivative is about2.14, so no near-tangent root was encountered in the resolved set. That is not a global exclusion of tangencies at other u or frequencies. Remaining angular-momentum integration uses Gauss quadrature rather than adaptive treatment of every root-entry boundary.

## Results

| quantity |64 action order|128 action order|
|---|---:|---:|
| fixed-mode projection x^T B x | .00618515859 | .00618524389 |
| dilation trial entry B00 | .01652023410 | .01654062513 |
| third-harmonic mode contribution | .00609390558 | .00609391266 |
| fourth-harmonic mode contribution | .00008986970 | .00008986936 |

The full matrix changes by .134% in relative Frobenius norm; the fixed-mode projection changes by .00138%. Both matrices are positive semidefinite to numerical precision. These are different error diagnostics: the very small projected change is not a uniform error bound for all field directions.

The128 grid finds2,13,119,83,45,19,6 roots at harmonics1 through7, respectively, and none in the retained8–16 range. These are quadrature-node root counts, not mass fractions or proofs that higher harmonics never resonate. The third harmonic supplies98.52% of the fixed-mode absorption and the fourth about1.45%. Low harmonics and the remaining resolved contributions are small for this approximate direction.

## Mechanism implication and next obligation

The earlier mass-weighted statistic could not establish absorption; the derivative-weighted prescribed response could not remove broadening; the present resonant-curve calculation supplies a nonzero boundary-value imaginary part with direct orbit checks. This is concrete progress toward evaluating collisionless transfer from the collective motion to resonant particle orbits within the existing identified-medium model.

It is still premature to report a decay rate. The real principal-value matrix and its frequency dependence must be calculated consistently, and the mode direction, field basis, harmonic range and resonance coverage must be refined. A linewidth estimate would require those ingredients, not just division by an unverified response slope. Energy redistribution also does not imply that an arbitrary primordial population can reach the required cold occupation; the earlier phase-space constraints remain.

No dissipative term, external bath or new parent theory was introduced. Any eventual novelty claim must concern a verified consequence of this particular theory, not the general existence of resonant absorption.

## Evidence

resonant_curve_run performs the bounded endpoint-completed, direct-orbit-refined calculation and passes three checks; its manifest validates. Original interpolated probes and the failed coefficient spot-check probe are retained. The direct-run and bounded-run sources are distinct and pinned. Interpretation is self-reviewed.
