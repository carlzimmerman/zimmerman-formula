# Local cold production from density-driven restoration

## Result and scope

The unchanged illustrative Palatini candidate has a local production mechanism:
a density-driven restoration transition leaves coherent scalar oscillations.
Their amplitude can be calculated conditional on a tracking initial state and a
specified density history, without fitting a conversion efficiency. It does
**not** meet the requested parameter-free cluster explanation. Slow assembly
produces at most 6.714e-11 of the previous required cold-source benchmark. An
ideal instantaneous jump supplies enough effective excitation energy in only
1 of 303 cases. Those cases are correlated shell/model/footing combinations,
not 303 independent observations.

This is a calculation in the candidate of `../cold_palatini_filter_2026_10_25`,
following the cluster entry failure of `../cold_filter_reality_2026_10_25`.
The candidate is not a derived completion of the original galaxy law. Existing
r=1, s=1/4 and eta=1500 pc km/s remain inputs, not newly selected constants.
No claim of microscopic symmetry, quantum stability, galaxy preservation,
radial-profile prediction, or parameter-free abundance follows.

## Action and energy accounting

Use canonical q=chi/v and tau=(sqrt(D)/v)t, where D=DeltaV, with Einstein time:

    f=cos²(q/2), y=4 sin²(q/2)
    W/D=[1+(y-1)²]/f², A=f^(-1/2)
    V(q,d)=W/D+d A, d=rho_star/D.

Here rho_star is prescribed conserved Einstein-frame baryonic rest density.
The homogeneous equation is q''+V_q=0. Its energy obeys E'=d' A(q): the changing
external matter source performs work. This is not spontaneous extraction from
an unchanged cosmological constant. A self-consistent treatment must debit that
work from matter and evolve the metric, neither of which is solved here.
Effective excitation includes the q-dependent matter interaction energy; it
cannot automatically be identified with an independently conserved cold mass.
Counting all of it toward the inferred cold requirement is a favorable budget
comparison, not a new gravitational fit.

## Slow crossing, with coefficient derived from the action

Direct symbolic differentiation gives

    V_qq(0,d)=(d-8)/4,
    V_qqqq(0,8)/6=g=9/4.

For d=8+4 gamma tau locally, the leading critical equation is
q''+gamma tau q+g q³=0. With T=gamma^(1/3)tau and
q=gamma^(1/3)Q/sqrt(g), it becomes

    Q''+T Q+Q³=0.

Tracking data Q(-L)=sqrt(L), Q'(-L)=-1/(2sqrt(L)) select a conditional incoming
solution. This is an assumed classical state without pre-existing excitations,
not a derived quantum initial condition. Integrations for L=40,80,160 give late
action means on T=[120,160] of 0.22063614, 0.22064652, 0.22064755. The largest
cutoff difference is about 5.2e-5 fractionally; the two late-window estimates
for L=160 differ by about 3.4e-5. These are finite numerical checks, not an
infinite-time theorem. The deliberate doubled-quartic mutation fails the
independent symbolic derivative check as intended.

The physical dimensionless oscillator action is J=gamma I/g. Adiabatically
transporting it to a restored final density df gives

    rho_exc/D ≈ (gamma I/g) sqrt((df-8)/4), I≈0.22064755.

The approximation requires a slow smooth crossing, small amplitudes, and
adiabatic evolution after leaving the critical layer. It does not solve a
merger, a spatial shock, fragmentation, a quantum spectrum, or subsequent
compression/transport of the produced field. No expansion dilution is modeled.
The small gamma makes the near-critical amplitude expansion self-consistent.

## Mapping to the existing cluster benchmarks

Use the 303 positive required-density cases from the previous wave-relaxation
calculation, with sigma_factor=1. The reference crossing times span about
0.148–1.085 Gyr. Set dot d=8/t_cross as a **proxy**, not a measured history.
Use the 35 gas-shell densities at H_J=1.8e-18/s in the previous reality test.
They are shell averages, not pointwise trajectories. The previous inferred
source follows the CCT inversion, not this Palatini candidate's refitted gravity.

Keep the frame dictionary explicit:

    omega_J=c²/eta,
    omega_unit=omega_J/(2.4 sqrt(5/6)),
    gamma=2/(omega_unit t_cross),
    D/c²=0.75 × 3 H_J²/(8 pi G).

Results:

| Quantity | Range |
|---|---:|
| gamma | 6.5925e-11 to 4.8425e-10 |
| Critical lag time | 45.53 to 88.50 years |
| Produced excitation / D | 2.3743e-11 to 9.8048e-10 |
| Produced / required benchmark | 4.7540e-14 to 6.7139e-11 |

Critical slowing down does create a residual, but ordinary crossing-scale
assembly is too adiabatic to create an appreciable reservoir in this calculation.

## Sudden compression and a conditional energy bound

This follow-up was specified after the slow-run result; see SUDDEN_CRITERIA.md.
Start at rest at the zero-density vacuum q_out=2 asin(1/sqrt(6)), with W/D=1.6
and A_out=sqrt(6/5). Instantly change d from zero to df>8. The exact excitation
above the restored minimum is

    E_jump/D = V(q_out,df)-V(0,df)
             = -0.4 + df [sqrt(6/5)-1].

The original full potential, independently evaluated at both endpoints,
verifies this expression for all benchmark densities. It ranges from 5.5128
to 165.8021 D. Relative to the earlier required source, the range is
0.0082018–15.3869; only **1/303** reaches unity. Even that one is an energy-budget
permission, not demonstrated cold production or retention. A sudden quench
initially creates anharmonic motion; its energy is not all pressureless matter.

For the same homogeneous action, this is also an upper bound for a single
monotonically increasing prescribed d(t), starting at q_out at rest. To see
this, define E=q'²/2+V(q,d) and B=E-V(q_out,d). Then

    B'=d' [A(q)-A_out].

As long as |q|<=q_out, A(q)<=A_out, so B'<=0 for d'>=0. Initially B=0.
The field cannot first exit this interval: at either boundary B=q'²/2>=0,
whereas its interior evolution gives B<=0. Boundary contact with zero speed
has inward force for d>0; at d=0 the initial vacuum is stationary. Thus the
interval is invariant and E_final<=V(q_out,df). Subtracting V(0,df) proves the
bound. Nonnegative homogeneous friction only strengthens it. This argument
uses the physical branch |q|<pi, a canonical kinetic term, and the even
potential above. It is not a bound on local energy density when gradients
transport energy inward, nor on nonmonotonic forcing, initial kinetic energy,
other fields, a contracting volume with anti-friction, or a live matter-metric
system. In particular it must not be advertised as a general collapse no-go.

## What is actually constrained

Changing the rate alone cannot rescue this single homogeneous monotonic
restoration route for 302 of the 303 existing benchmarks under the stated
energy identification. Slow crossing fails much more strongly. Local production
is possible, but its existence does not determine a sufficient abundance.

Spatial concentration or repeated driving remains logically open. It must
supply a conserved energy budget and a derived evolution law; assigning a
production efficiency or repeated-event count would add freedom. Density alone
also supplies no demonstrated cluster-versus-galaxy selector: the same action
responds to a crossing wherever it occurs. The calculation has not established
that either a successful cluster profile or the galaxy law survives. These are
unresolved requirements, not successful outcomes hidden by this negative test.

## Reproduction and evidence

Run from repository root with the recorded Python/numpy/scipy/sympy environment:

    python reviews/cold_local_production_2026_10_25/check.py --output /tmp/cold-local-check
    python reviews/cold_local_production_2026_10_25/sudden.py

The bounded normal run and expected failing mutation have manifests under run/
and mutation/. contract.json and FROZEN_CRITERIA.md record the slow-run scope.
The separate sudden calculation has exact endpoint checks in sudden.py and
all 303 results in sudden_result.json. The monotonic bound is an analytic
argument above, not a claim established by sampling 303 cases. All numerical
inputs are the preceding repository calculations; no new external literature
claim is needed for this derivation.
