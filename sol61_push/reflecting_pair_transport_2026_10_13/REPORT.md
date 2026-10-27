# Reflection leaves a bounded candidate, but its power budget is poor

2026-10-13. The previous goal turn calculated interface reflection. This turn includes it in a phase-independent gain bound, then evaluates the size and power of the resulting candidate. These are conditional model results, not empirical evidence or a complete way to manufacture cold energy.

## Phase-independent reflection bound

The counterpropagating matter amplitudes and their conjugates form a four-component linear system. Taking sums of their absolute values in each propagation direction bounds them by a positive two-envelope transport system. With equal passive reflection magnitudes r at both ends, its incoming boundary conditions are

\[
U(0)=rW(0),\qquad W(L)=rU(L),\qquad 0<r<1.
\]

Complex reflection phases cannot increase this positive comparison envelope. This assumes passive frequency-independent boundary magnitudes over the narrow gain band; it does not replace a full dispersive boundary response.

Let G=mu L/v. At zero growth the comparison system rotates its spatial amplitudes by G. Its first critical solution satisfies

\[
(1-r^2)\cos G-2r\sin G=0,
\qquad
\boxed{G_c=\pi/2-2\arctan r.}
\]

The r=0 limit recovers the previous perfectly outgoing threshold. For unequal magnitudes the corresponding expression is pi/2-arctan(r_left)-arctan(r_right); this package computes the equal case.

There is a constructive subthreshold bound, not just a real-root test. In units L=v=1, define a=arctan(r),

\[
U_c(x)=\sin(G_cx+a),\qquad W_c(x)=\cos(G_cx+a).
\]

These positive functions satisfy both reflection boundary conditions. For actual G<Gc, the comparison generator applied to this pair equals -(Gc-G)(Wc,Uc). Since both ratios Wc/Uc and Uc/Wc are at least r, a weighted maximum norm contracts at rate at least r(Gc-G). Restoring units multiplies this rate by v/L. Thus the bound accommodates the most amplifying reflection phases within this fixed-ray envelope model.

Twelve discretized-generator eigenvalue checks test r=0.1, 0.3, 0.7 at 0.8 and 1.2 times threshold, on 160 and 320 cells. Positive eigenvectors and residuals identify the dominant comparison eigenvalue; all signs agree with the threshold. The critical boundary functions and subthreshold supersolution inequalities are checked separately.

## Combining the bound with the computed wall

For a spherical straight-ray model of diameter D, a chord hitting the surface at incidence angle theta has length D cos(theta). With r(theta)=sqrt(R(theta)) from the previous 1 eV wall,

\[
D<D_c(\theta)=\frac{v[\pi/2-2\arctan r(\theta)]}{\mu\cos\theta}
\]

is a sufficient phase-independent condition for that ray channel. This is not the earlier local loss-rate estimate, and it retains distributed pair amplification along the path.

The calculation recomputes the wall reflection at 21 angles from 0 to 89.9 degrees. Each diameter estimate is refined until consecutive grids agree within 0.5%, using spacings down to 0.0025 healing lengths when needed. An initial coarse-grid check failed that criterion at 80 degrees; the angular points were refined instead of weakening the criterion. The imported `wall_solver.py` is the function-and-input-loading portion of the preceding audited scattering script, copied into this package and hash-pinned.

At target excitation fraction eta=10⁻¹²:

| Incidence angle | Critical diameter for that ray |
|---:|---:|
| 0° | 11.62 mm |
| 30° | 12.82 mm |
| 60° | 17.79 mm |
| 80° | 27.17 mm |
| 89.9° | 31.07 mm |

The smallest **sampled** value is 11.62 mm at normal incidence. A 10 mm diameter passes every sampled ray condition, even with the phase-independent reflection bound. This does not prove the minimum over all angles: there is no interval-enclosed angular analysis here. Nor does it establish full three-dimensional stability, angular-mode coupling, finite-source depletion or a physical trap. The uniform ray approximation and locally planar wall are still assumptions.

## Size and power of the conditional candidate

It is important to check what the surviving example actually provides. Take the same prescribed density and a uniform sphere of diameter 1 cm. Use the preceding lowest-population drive estimate and the sqrt(2) steady intensity factor for the biased ramp. Assume each beam has cross-sectional area equal to the sphere's projected area.

| Quantity | Conditional value |
|---|---:|
| Condensate mass | 173.5 kg |
| Spontaneous photon output | 2.73×10⁻¹⁰ W, or 0.273 nW |
| Passive matter-decay power | 9.18 kW |
| Approximate power in each illuminating beam | 1.01 GW |

The beam power is incident optical throughput, not all absorbed power. The matter-decay figure uses the passive width and omits additional stimulated pair output. The photon figure is only spontaneous emission from the prepared population, not transmitted pump light or pump-induced scattering. This is not a complete efficiency calculation, and these values do not establish a bright source.

The trap itself remains stipulated; no mechanism has assembled 173.5 kg of this material or held it in that volume. Its ordinary gravitational field would be attributable to that existing mass, not a newly demonstrated gravitational enhancement. Passing a linear gain bound does not supply those missing ingredients.

## Evidence and interpretation

`run_v2/` is the canonical audited result including the physical budget. `run/` is the earlier angular-only run; its source snapshot is retained as `check_before_budget.py`, rather than treating it as validation of the subsequently extended script. Contracts pin all imported well, pair-gain and drive inputs. The calculation is analytically self-reviewed and numerically checked; no new Lean proof of transport or whole-sample stability is claimed.

A phase-independent candidate window survives the sampled reflection test. That is useful progress, but the dominant unresolved requirements remain the microscopic confining interaction, preparation of the dense inventory and an energetically credible useful output. Further angular refinement alone would not answer those questions. The next route should target a term capable of supplying the required well, while checking whether it is actually determined by the repo's action rather than freely assigned.
