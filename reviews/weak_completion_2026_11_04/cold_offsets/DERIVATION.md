# Cancellation-safe local orbit ingredient

**Finite outcome:** implementation and finite assertion verified in the stated
range, conditional on floating arithmetic and the supplied local spline
representation. This is an orbit oracle, not a coupled cold cosmological
solution. The authoritative guarded implementation is `oracle_v2.py`, checked
by `check_v2.py` and `run002/manifest.json`. The first successful version and
its record remain unchanged.

## Representation and identity

The population is the actual fresh common30 warm endpoint in
`integration/run_joint006/result.json`: N=.0021690179772784167,
e=.003, mu=2e6 GeV, xi=.02. Its action is replaced, solely for the stress
experiment, by four artificial values J/J_initial=1e-4,1e-8,1e-12,1e-16.
No new physical particle state or late history is inferred from that replacement.

Let x_a be the float minimum returned by the existing oracle and d=x-x_a.
Inside a single spline interval write

    m_s²(x_a+d)=m_s0²+a_s1 d+a_s2 d²+a_s3 d³,
    V(x_a+d)-V(x_a)=v1 d+v2 d²+v3 d³+v4 d⁴.

The fourth term exists only in the exported local gravity polynomial; it is
zero in the ordinary cubic interval used by this warm test. Each finite
translated coefficient is recorded through the pinned implementation and state.
The reference treats those float coefficients as exact real input parameters;
it is not a new error bound for interpolating the exact underlying field theory.

For p_k=Tc q_k, E0=sqrt(m_s0²+p_k²), Delta=m_s²(x_a+d)-m_s0²,
and E=sqrt(E0²+Delta), rationalization gives the exact identity

    E-E0-a_s1 d/(2E0)
      =(Delta-a_s1 d)/(2E0)-Delta²/[2E0(E+E0)²].

The numerator Delta-a_s1 d is evaluated directly as d²(a_s2+a_s3 d),
rather than by subtracting nearby numbers. Combine all first derivatives as

    F_a=v1+Tc³ sum_s,k Y_sk a_s1/(2E0),

where Y=g W f/(2pi²) already contains the number measure. A 70-digit sum
computes F_a from these same finite coefficients. Then

    U(x_a+d)-U(x_a)
      =F_a d+v2 d²+v3 d³+v4 d⁴
       +Tc³ sum Y[(a_s2 d²+a_s3 d³)/(2E0)
                   -Delta²/(2E0(E+E0)²)].

Every term scales with the small excursion, rather than the large total
Hamiltonian. The derivative uses an analogous rationalized identity. Newton
refinement of the local minimum gives d_min=8.783221518634074e-15,
consistent with the independently reconstructed high-precision minimum.
The old float anchor is not simply declared to have exactly zero force.

The oracle solves turning points in displacement scaled by the harmonic
amplitude, and excitation scaled by omega J. Harmonic quantities serve only
as numerical scales and brackets. The action and period always integrate the
nonlinear local Hamiltonian:

    J=sqrt(2M)/pi integral_xL^xR sqrt(epsilon-DeltaU) dx,
    T=sqrt(2M) integral_xL^xR dx/sqrt(epsilon-DeltaU), M=62.

The theta substitution between the actual nonlinear turning points removes
the endpoint singularity. No positive kinetic-energy floor, action floor or
harmonic continuation is used. Nonpositive action, invalid numbers, a
mass-squared clipping crossing, or leaving the supported local spline interval
is rejected explicitly. This is a local positive-J interface; a J=0 manifold
and cross-interval continuation are not implemented.

## Independent finite checks

The high-precision check evaluates direct square-root potential differences at
17 displacements for every artificial action. It does not use the rationalized
remainder. Its independent action reference expands each square root to order
12, retains the resulting degree-36 polynomial at 70 digits, finds its turning
points, and integrates with mpmath Gauss-Legendre quadrature.

For |Delta/E0²|<=z<1, the omitted square-root terms are bounded in absolute
value by E0 z^13/(1-z), since the magnitudes of the relevant binomial
coefficients are below one. Summing positive absolute population weights
provides an explicit uniform potential-tail bound on the tested orbit. The
largest z is .00421269; the largest bound is 6.05e-28 of excitation. This is
far below the observed floating action error, rather than an assumed zero tail.

| J/J_initial | Excitation / mu4 | Half turning-point separation | Harmonic excitation correction |
|---:|---:|---:|---:|
| 1e-4 | 3.1921638975e-15 | .01097494446 | -3.67388e-7 |
| 1e-8 | 3.1921650701e-19 | .0001097494110 | -3.67373e-11 |
| 1e-12 | 3.1921650702e-23 | 1.097494110e-6 | unresolved at roughly 1e-15 relative |
| 1e-16 | 3.1921650702e-27 | 1.097494110e-8 | unresolved at roughly 1e-15 relative |

At the two smallest actions the quoted near-zero float differences are
roundoff, not measurements of a nonzero anharmonic coefficient.

Across all four cases, direct potential errors are at most 2.21e-16 of
excitation; independent action errors are at most 1.34e-15 relative. The
32/64-node excitation comparison differs by at most 1.89e-15. At J/J_initial
=1e-4, the ordinary nonharmonic oracle agrees to 2.85e-10 in excitation and
3.19e-9 in period. At J/J_initial=1e-16, adding epsilon to the float minimum
returns exactly the same float minimum; the separate epsilon remains positive
and verified. The guarded run takes 3.82 s and about 304 MB measured RSS.

The harmonic geometry was therefore extremely accurate at the 1e-8 stress
point of this **new common30 warm population**. This is not a bound at the
older 25-group population or a uniform cold-limit result. The demonstrated
failure is cancellation in total-energy storage and inversion; the nonlinear
oracle now permits that distinction to be checked.

## Linewidth relevance and scope

The smallest tested half-excursion is 1.0975e-8. Its independent displacement
root discrepancy is 1.66e-24, while converting a phase position back to the
absolute warm coordinate has float spacing 4.44e-16. The latter, not the
relative displacement solver, eventually limits a collision factory receiving
only absolute float x. A finite orbit claim must retain both numbers.

For an actual resonance detuning D(x), a necessary numerical check is

    |D'(x)| delta_x + delta_D_matching << Gamma_effective,

with delta_x including the minimum, phase-position quantization, orbital
quadrature, interpolation and dynamical-lag errors. A narrow width does not
justify equating it with zero, and an accurately represented tiny action does
not establish that its actual field minimum lies on the line. This warm
fixture is not at the cold pole, and does not determine the cold effective
width, thermal/current mass shift or real minimum lag. No linewidth accuracy
claim for a physical cold state follows from these stress calculations.

## Required coupled interface, not implemented here

Replacing `orbit()` alone cannot fix a coupled cold history. In particular,
`Etotal=Emin+epsilon` rounds epsilon away in the smallest successful example.
The coupled state needs a separate excitation (or action with stable offset
inversion) and a stable difference of minimum energies between successive
N,Y states. At a common anchor, decompose that minimum difference into the
two small local offsets plus the actual population/redshift energy change.
Do not subtract independently reconstructed large minimum energies.

The actual collision increment must also survive. Forming Y_new-Y_old after
rounding can lose a small increment whose energy exceeds epsilon. Retain the
integrated collision increment or compensated number updates, and enforce the
same physical residual, holes and statistics used by the accepted solver.
For phase-resolved increments, local collision energy conservation permits a
centered energy-flux identity using E(x_phase)-E(x_anchor), evaluated by stable
mass-squared differences. That identity can avoid a large-energy dot-product
cancellation, but it has not been implemented or validated as a coupled update
in this package.

Finally, cumulative FRW work and the minimum-energy changes need compensated
or higher-precision bookkeeping and an independently integrated work check at
the desired excitation scale. An offset orbit does not make the first-order
population update higher order, remove its newborn cascade bias, bound an
adiabatic moving-minimum approximation, or certify an end-to-end cold state.

## Additional conditional cold-pole fixture

`cold_check.py` and `oracle_v3.py` also test the explicitly conditional
scalar-only packet at Tc/mu=1e-6. Its 37 physical momentum cells come from the
existing CC11 elastic grid. The scalar occupation is exactly twice the CC10
memory endpoint's legacy fS; all other common30 occupations are exactly zero.
Its number yield reproduces that old conditional endpoint to the declared
tolerance. It is **not** a continuation of the new common warm state.

Version 3 omits exactly zero-weight species from the Hamiltonian sums and
records them. This is exact algebraic elimination, not an alteration of
occupied masses or derivatives. No inactive negative mass-squared mode was
found in this particular fixture. An occupied negative branch is still refused.

Four artificial harmonic-scale amplitudes 1e-4,1e-6,1e-8,1e-10 all pass the
same nonlinear offset, 32/64-phase, direct 70-digit and independent action
checks. The local curvature is 2.92929177e-14, the period approximately
2.89064259e8, and the refined minimum differs from its float anchor by
-4.37126e-14. The largest direct potential discrepancy is 1.81e-16 of
excitation and the largest independent action discrepancy is 1.68e-15.
At amplitude 1e-4 the harmonic excitation correction is -4.2330e-11; the
smaller displayed corrections are below the observed arithmetic resolution.

At this actual pole region, absolute float position spacing is 3.55e-15.
It is 3.55e-7 of the 1e-8 test amplitude and 3.55e-5 of the 1e-10 amplitude.
This supplies a concrete positional-resolution term for the linewidth test
above, while the independently checked displacement roots are substantially
more accurate. It does not supply the physical width or its mass/current
matching uncertainty. The scalar-only packet has no evolving neutral bath,
inverse source, or newly derived gravity trajectory.

The authoritative cold record is `run004/manifest.json`; the same successful
calculation in `run003` is preserved. Its `coefficient_domain` description
inherited the single stale word "warm" from the template, despite the correct
conditional assertion, inputs, command and results. `contract004.json` corrects
that description before the identical cold calculation is repeated. No
historical bytes or numerical result were repaired.
