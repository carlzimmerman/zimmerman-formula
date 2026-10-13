# Finite-band energy of preparation-pulse fluctuations

Status: the computed linear vacuum excitation energy is negligible relative
to the supplied source density. This is a finite-band numerical estimate of
a conservative pointwise envelope, not a certified integral over all momenta.
It does not establish the origin or abundance of the source.

## Avoiding unresolved interference

The plateau between the two smooth clock edges has constant fluctuation
frequencies sqrt(k^2+4) and k, where k=p/M. Its transfer is an exact free
rotation in its oscillator basis. Only the two short edges need numerical
integration. This independently reproduces the earlier full-duration mode
occupations at nine momenta.

For a real oscillator-normalized transfer R, partition it into 2-by-2 blocks
A,B,C,D for coordinates and momenta. Its Bogoliubov matrix is

    beta = (A-D+i(C+B))/2.

Computing occupations as sums of |beta|^2 avoids subtracting the vacuum
one-half from nearly equal quantities at large k. Let N1 and N2 be the
summed occupations of the first and second edge, each defined with its
correct incoming and outgoing frequencies. For their composition through
any intervening free rotation,

    Ntotal <= [sqrt((1+N2)N1) + sqrt((1+N1)N2)]^2 = B(k).

This follows from beta21=alpha2 beta1 + beta2 alpha1*, with the intervening
unitary phases included, the Frobenius/operator norm inequalities, and
||alpha_i||op <= sqrt(1+||beta_i||F^2). Thus rapid phase interference between
edges cannot exceed B(k). No phase averaging assumption is required.
Since both outgoing frequencies are at most sqrt(1+k^2),

    rho_exc / M^4 <= integral dk k^2 sqrt(1+k^2) B(k)/(2 pi^2)

when both sides are restricted to the same momentum band. This includes
the clock and Y excitations; X remains an uncoupled free oscillator.
The inequality is analytical for exact edge transfers; their numerical
values and the numerical integral still have numerical uncertainty.

## Computed band and numerical checks

For the tuned J=10, delta=0.01 pulse, integrate from k=0.001 to 10000 on a
257-point logarithmic grid. Simpson integration includes the log-coordinate
Jacobian. The estimate for the envelope integral is 8.7073653e6; using every
second grid point gives 8.7050634e6, a relative difference of 0.02644 percent.
This difference is a convergence diagnostic, not a rigorous error bar.

| Upper momentum cutoff p/M | Cumulative envelope integral |
|---|---:|
| 3.1623 | 0.8861 |
| 177.828 | 1.16535e6 |
| 1333.52 | 8.58372e6 |
| 3651.74 | 8.68593e6 |
| 10000 | 8.70737e6 |

The interval from 3651.74 to 10000 adds about 0.246 percent of the final
finite-band value. This supports numerical saturation within the sampled
range but does not bound the remaining tail.

The high-momentum envelope values are 0.0238021 at k=300, 1.68352e-5 at
1000, 2.30560e-8 at 3000 and 7.70264e-12 at 10000. Tightening the edge
integration tolerance from 1e-10 to 2e-12 changes these values by less than
5.2e-10 relatively. These values suggest decreasing high-momentum excitation,
but an asymptotic exponent or full ultraviolet bound cannot be inferred
from four samples alone. The compact potential is C2; its fluctuation
Hessian contains W'', so its limited smoothness must be accounted for in
any tail proof rather than assuming exponential suppression.

## Physical normalization and interpretation

Using the inherited illustrative values M=2.00000099999975e-12 eV and
source density 9.71510619e6 eV^4 gives

    finite-band envelope energy estimate = 1.39318e-40 eV^4,
    fraction of initial source energy    = 1.43404e-47.

These physical parameters are stipulated values used by the formation
example, not abundance predictions. This fraction is about 40 orders of
magnitude below the initial eta about 5e-7 budget. Consequently the sampled
linear vacuum excitations do not threaten that budget at these parameters,
even when the conservative phase-independent envelope is used. This does
not license replacing the full momentum integral by the sampled band.

A macroscopic primordial fluctuation spectrum is a different input from
free oscillator vacuum noise. Its amplitude is not fixed or bounded by this
calculation. Neither nonlinear amplification nor feedback of these quanta
on the clock trajectory is included, although the very small finite-band
energy supports neglecting feedback from that band in this example.

## Reproducibility and remaining gate

`clock_energy.py` pins the earlier tuned background and fluctuation results.
Its manifest is `clock_energy_run/manifest.json`; all 23 declared checks
pass and the manifest validates. Checks include the independent analytical
plateau propagation, the composition envelope, quadrature refinement and
high-momentum tolerance comparisons. This remains self-reviewed evidence.

A full preparation-energy conclusion still requires bounds for k<0.001 and
k>10000, or a justified physical cutoff and its completion. No exact quantum
symmetry restoration, autonomous displacement/phase origin, observed cosmic
abundance, carrier transport or galaxy law is established here.
