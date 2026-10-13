# Positive-contact extension: production survives, transport remains open

2026-10-11. Executes the extension proposed in [CARRIER_MATCHING.md](CARRIER_MATCHING.md).
The full potential is the positive-square charged action plus
lambda_rep |phi|^4. Choose lambda_rep=lambda_min=g^2/Delta. This is a
specified example, not a parameter inferred from the repository or data.

## Production calculation

The Gaussian equations in [CHARGED_PRODUCTION.md](CHARGED_PRODUCTION.md)
apply with total quartic lambda_total=lambda_min+lambda_rep. The source
coupling, masses, initial density, vacuum weights and expansion background
are unchanged. The dimensionless quartic coefficient doubles to
0.2000001. Both its normal and anomalous terms remain included.

[repulsive_envelope.py](repulsive_envelope.py) gives:

| Quadrature | Daughter charge fraction at x=100 | At x=200 |
|---|---:|---:|
| 512, interval [-2,2] | 0.8134957355 | 0.9176124571 |
| 1024, interval [-2,2] | 0.8134957358 | 0.9176124571 |
| 768, interval [-3,3] | 0.8134957326 | 0.9176124571 |

All 15 checks pass. Maximum charge drift is below 6.0e-9 and energy-work
residual below 2.86e-8. The relative covariance diagnostic reaches about
5.8e-4, so these are not certified quantum-state error bounds. This extension
has not received a separate tighter-time-tolerance run; the table's many
digits show quadrature comparison, not a claim of that many accurate digits.
The appropriate conclusion is substantial transient conversion, about 91.8%
at this endpoint. Maximum sampled conversion is about 99.25%; neither number
is a permanent yield. [Results](repulsive_envelope_run/results.json) and
[manifest](repulsive_envelope_run/manifest.json) preserve the experiment.

The classical charge-energy and FLRW comparison bounds survive the added
positive quartic, as shown in CARRIER_MATCHING. The Gaussian quantum
calculation still omits moving sources, non-Gaussian scattering, antiparticles
and a controlled match to the classical theorem.

## Contact matching and its restricted momentum range

Let alpha=lambda_rep/lambda_min. The tree-level effective quartic is

\[
 \lambda_{\rm eff}(s)=\lambda_{\min}
 \left[\alpha-{x\over1-x}\right],\qquad
 x={s-4m^2\over\Delta}.
\]

At threshold it equals lambda_rep>0, reproducing the repulsive contact
structure of the repo's carrier at leading nonrelativistic order:

\[
 g_{\rm NR}={\lambda_{\rm rep}\over2m^2},\quad
 a_s={\lambda_{\rm rep}\over8\pi m},\quad
 \sigma=8\pi a_s^2.
\]

These are natural-unit, vacuum, tree-level threshold relations. They are
not a Bose-enhanced transport rate. For this alpha=1 example the interaction
vanishes again at x=1/2, becomes attractive for 1/2<x<1, and has the source
pole at x=1, where the bare tree expression cannot determine a physical rate.

For opposite incoming momenta in their center-of-mass frame,
x=p^2/(m^2u_*^2). Requiring the source correction to be at most a fraction
tau of the threshold repulsion, below resonance, gives

\[
 x\le{\alpha\tau\over1+\alpha\tau}.
\]

For alpha=1 and 10% tolerance this means p/m<=0.301512 u_*. At u_*=0.001
that corresponds approximately to 90.4 km/s per incoming particle in the
center-of-mass frame. This is a matching-domain statement, not a halo
velocity prediction. The near-resonant production band lies outside this
contact domain. Full two-field dynamics are needed there.

## What the added repulsion actually supplies

[repulsive_scales.py](repulsive_scales.py) evaluates the chosen
lambda_rep=2.0586517129e-63 at m=1e-12 eV. It obtains:

* threshold scattering length a_s=1.61633e-59 m;
* threshold sigma/m=3.68324e-68 cm^2/g;
* coherent contact pressure speed 0.01997 m/s at the inherited illustrative
  galaxy density 1e-21 kg/m^3.

The last value uses c_contact^2=g_NR rho/m^2, with coherent pair factor one.
Independent SI and natural-unit evaluations agree. Both finite checks pass;
[results](repulsive_scales_run/results.json) and
[manifest](repulsive_scales_run/manifest.json) record the arithmetic.
No current empirical bound is inferred from these numbers.

Thus this example supplies positive contact repulsion in its low-momentum
domain but essentially no macroscopic halo support from that pressure at
the inherited density. As in the repo carrier report, support would need
orbital/kinetic stress. The tiny threshold cross section does not by itself
prove slow transport in a highly occupied resonant field; that requires a
consistent collision/correlation calculation including the source channel.

## Research decision

Adding positive repulsion does not automatically stop the approximate
formation mechanism. It can repair the sign of the threshold carrier
coupling while preserving classical energy protection. However, selecting
this arbitrary coefficient does not establish the desired settling rate,
universal halo profile, or vacuum-dependent acceleration scale. A constant
contact Hamiltonian cannot represent the whole resonant momentum range.
The next physical requirement is the coupled transport law, or evidence
that gravity alone supplies the necessary relaxation and profile selection.
No successful halo mechanism is claimed by this example.

A subsequent [3D spatial pilot](SPATIAL_CONVERSION.md), using an explicitly
classical seed, populates moving sources and shows order-one changes in
transient conversion relative to its matched uniform-source control. It
does not replace the quantum initial state, but confirms that homogeneous
source yields cannot be promoted to full nonlinear predictions.
