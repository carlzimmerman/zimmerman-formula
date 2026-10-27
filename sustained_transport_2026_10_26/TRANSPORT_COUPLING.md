# What the emitting channel sees of the required inward transport

This is a conditional linear statement at the smooth internally quiet initial
profile, with chi=0, common real species phases and zero conversion current.
It is not a theorem that dark directions stay dark under nonlinear evolution.

Let v_e be an infinitesimal common radial velocity at material edge e=(i,j).
Write dr_e=r_j-r_i and r_e=(r_i+r_j)/2. Linearizing the EXACT covariant square
with phase difference sigma v_e dr_e/kappa gives

    ATe=r_e^2 sqrt(rhoTi rhoTj),
    AFe=r_e^2 sqrt(rhoFi rhoFj),
    jTe=ATe v_e, jFe=AFe v_e.

The inherited sigma^2=kappa normalization gives the positive transport energy
T=1/2 sum B_e v_e^2, B_e=(ATe+AFe)dr_e. From the exact charge/current identity,

    Qm_dot=L(v),
    L_e=2 g2 (rhoTj-rhoTi) ATe,
    L(v)=sum L_e v_e.

Thus the leading compact-source monopole sees one linear functional of the
velocity field. Its bright direction in the kinetic metric is b=B^-1 L.
For any trial direction v, define

    v_bright=b L(v)/<b,b>_B,
    v_dark=v-v_bright.

Then L(v_dark)=0 and <v_bright,v_dark>_B=0 exactly. There are many different
enclosed-mass currents in this kernel. Consequently nonzero radiation does not
by itself imply the required radial redistribution, even when all backreaction
is retained. Finite-source corrections, conversion and later Hamiltonian
mixing can couple these directions to radiation; they have not been excluded.

## Diagnostic tied to the actual density deficit

Use the freely obtained static energy equilibrium as a reference, not a fitted
law density. Let delta M_e be reference minus initial enclosed mass. The
common-transport tangent toward that reference is

    v_required,e=-delta M_e/(ATe+AFe).

This is a tangent used to identify coupling, not a prescribed time history or
a force in the simulation. It conserves total mass. Restrict the metric
integration diagnostically to r<200 kpc and B>1e-14 max(B); material evolution
itself has no such restriction.

The bright fraction of its kinetic norm is 0.00057321 (0.057321%). In this
decomposition, the bright part carries only 3.5857e-5 (0.003586%) of the desired
inward 50-kpc mass rate. The remaining rate lies in the instantaneous kernel
of the leading monopole. The direct phase-perturbation source agrees with L(v)
to relative 5.03e-13.

The 0.057321% is a direction/norm projection, NOT a measured radiation efficiency
and NOT a bound on all future radiation. Do not confuse it with the earlier
0.50245% of actual field work found in the first pulse.

Changing the diagnostic outer cutoff from 100 to 200 kpc gives bright kinetic
fractions 0.061623%--0.057321%. Changing the small-metric floor from 1e-12 to
1e-16 has negligible effect. The bright share of the 50-kpc current is unchanged
across all nine cases. This checks tail/normalization sensitivity within the
stated tangent model, not continuum or nonlinear convergence.

In the actual full trajectory, 95.9% of absolute source weight lies inside
10 kpc at 5.7 Myr, increasing to 97.9% at 9.765 Myr. The main law deficit is
near 50 kpc. The mismatch is therefore also visible without choosing a metric.

## The complete force budget at 50 kpc

Differentiate the exact total edge current, including U_dot from BOTH rhoT_dot
and chi_dot. Resolve a_dot into gravity, response, F pressure, binding, covariant
gradient, alignment, carrier-density inertia and current-density companions;
add the separate scalar-phase contribution. This is an accounting decomposition
in the inherited canonical chart; only the sum is invariant.

At 9.765 Myr the inward enclosed-mass acceleration contributions in Mb/Myr^2 are:

| Force contribution | Acceleration |
|---|---:|
| Gravity | +4.80787e-5 |
| Response | -4.46028e-5 |
| Covariant gradient | +2.14670e-8 |
| Scalar phase/backreaction | -2.30270e-8 |
| Remaining companions combined | About -1.1e-11 |
| Net | +3.47424e-6 |

The outward response cancels about 92.77% of the gravitational acceleration.
Scalar backreaction is only about 0.66% of the net acceleration at this radius.
Thus the small current there is not primarily a large scalar drag holding
otherwise rapid infall. All components reconstruct the independent full
Hamiltonian vector field; three directional differences verify their total.
The actual inward mass rate is only 3.38427e-5 Mb/Myr at this state.

The remaining physical dependency is transfer of the broad, weakly emitting
transport into the radiating channel while its density and boundary respond.
Rank-one visibility does not prove that transfer impossible: the full nonlinear
Hamiltonian can mix directions. Actual long evolution or a controlled mixing
reduction is required. Increasing source strength, reporting another pulse,
or moving the composition crossing alone does not establish that dependency.

## Finite source size does not repair this direct overlap in the tested family

For harmonic frequency Omega in dimensionless time, the exact regular radial
retarded form factor is j0(Omega r/c)=sin(Omega r/c)/(Omega r/c). It follows by
performing the inner time integral in the retarded formula; no compact-source
expansion is needed. The linear source functional becomes

    L_e(Omega)=g2 ATe [(-1.5rhoTi+0.5rhoTj) j0(Omega ri/c)
                     +(1.5rhoTj-0.5rhoTi) j0(Omega rj/c)].

At Omega=0 this reduces exactly to L_e above. The source-cell weighted sum and
edge functional agree independently in frequency_visibility_checked. Physical
frequency omega in rad/Myr corresponds to Omega=omega t_dyn.
The Green function/form factor is exact in the continuum radial problem;
the numerical cell-center evaluation is point-cell quadrature, not an exact
resolvent of the finite-volume wave grid. No high-frequency spatial convergence
certificate is claimed by this audit.

The bright kinetic fraction for the same required tangent falls from
0.057321% at zero frequency to 0.054113% at 10 rad/Myr, 0.010934% at 100,
0.00023124% at 500 and 0.00000998% at 1000. These are conditional direction
projections, not a supplied oscillation, a generated power or a no-go theorem.
The sampled finite-size correction therefore does not provide the missing
direct overlap. Spatial/compositional mixing remains a separate obligation.

The 2-kpc scalar exterior also has a discrete wave-frequency ceiling
2c/h=306.60 rad/Myr in physical units. It cannot establish arbitrary escape at
the roughly 500-rad/Myr carrier scale. The current inner-annulus snapshot has
only about 6e-6 of its windowed characteristic spectrum above 300 rad/Myr;
this limitation does not explain the measured slow pulse. Future claims of
fast-carrier radiation must refine the exterior and compare actual flux.
