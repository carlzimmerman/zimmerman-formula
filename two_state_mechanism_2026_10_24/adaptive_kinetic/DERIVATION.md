# Adaptive kinetic collision operator and conservative coupling

## Representation and transport

Each positive-weight sample carries (m,x,v,species,state). Baryons are B;
medium samples are F or T and have independent trajectories. An initial spatial
node can carry several independently sampled velocities, with its mass divided
between them. Those samples immediately stream independently. No Maxwellian or
common velocity is imposed during evolution; phase-space positivity and species
mass conservation follow from positive fixed weights and state changes.

The field remains the preceding checkpoint's isolated longitudinal 3D Gaussian
field, u=sum_i in T G m_i F(|y-x_i|/sigma)(y-x_i)/|y-x_i|³, with

    U_T = a0²/(4pi G) integral [-log(1-|u|/a0)-|u|/a0] d³y.

Analytic quadratic energy and exact isolated nonlinear self energies are combined
with Cartesian quadrature of nonlinear interference. Forces differentiate that
same numerical energy. This is a quasistatic curl-free effective closure, not a
solution of the different unrestricted nonlinear polarization minimization.

Gravity now includes the full constant softened self term:

    U_g = -G/2 sum_ij m_i m_j / sqrt(|x_i-x_j|²+epsilon²).

The extra diagonal term is -G sum_i m_i²/(2epsilon); it has zero positional
force. Dividing a coincident sample into equal-velocity samples preserves this
full gravitational density energy. It is neither a correction to integration
error nor a source of reaction energy. Field quadrature, unlike the exact
continuum functional, can retain a small dependence on self-term decomposition;
no charged remeshing or particle merging is performed during a run.

Adaptive kick-drift-kick transport uses the inherited Hamiltonian error test.
No velocity rescaling, global energy projection or unexplained heat correction
is added. Adaptive collision cells do not deposit or remap field mass, so grid
refinement itself has no Hamiltonian-energy change.

## Local kinetic limit and adaptive cells

The previous finite physical kernel was 1/V_h within h=0.1kpc and zero outside.
For density and velocity distributions varying slowly on h, its spatial integral
is one. The leading local Boltzmann collision integral uses local f_B(x,v) and
f_F/T(x,w), rather than requiring two simulation centers within h.

Approximate those distributions in an octree leaf of volume V_c. For a B-medium
sample pair in that leaf, use

    gamma_ij = C m_B [- (v_medium-v_B) dot n]_+ / V_c,
    P_ij = 1-exp(-gamma_ij dt),
    C = 1 cm²/g in the default normal-flux convention.

This has the same incoming-normal normalization as the prior model. Averaged
over isotropic normals, [-v dot n]_+ has mean |v|/4. Thus C must not be compared
directly with an empirical isotropic total scattering cross section without
matching conventions. A 100-times-C run is an explicitly labeled sensitivity
experiment, not a fitted or observationally permitted interaction.

The octree divides occupied space until the maximum numerical width is met,
and splits crowded leaves further, down to maximum_width/8. The crowding target
is 16 times the number of initial velocity samples per spatial node, so simply
adding coincident velocity samples does not change the initial spatial grid.
There is no search-radius expansion to find a partner. Empty mixed-species leaves
have zero estimator. All eligible within-leaf pairs enter the operator with
explicit volume and baryonic mass weights.

Cell width is a numerical approximation scale. A collision between two distinct
macro centers in the same leaf represents locally co-located kinetic mass,
not a physical interaction between those centers at their actual separation.
We choose the actual pair normal for a central impulse; for coincident samples
we use a reproducible isotropic normal. This conserves pair angular momentum,
but finite-cell geometry and velocity gradients create modeling errors. The
operator is DSMC-style with this specific normal-flux/central-impulse closure;
it is not a claim to implement a standard VSS/VHS molecular differential cross
section.

The sampled B/medium masses have ratio5.364, inherited from equal sample counts
and the assumed reservoir ratio. Interpreting those impulses as microscopic
physics requires an additional species-mass/weighting model. Increasing sample
counts also reduces finite field-charging granularity; velocity refinement is
not independent of that discretization effect, even with identical initial
spatial nodes.

Time steps limit displacement to .2 of the current leaf width and the initial
per-particle sum of pair hazards to .1. Individual rates are recalculated after
preceding impulses and their actual maximum hazard-step product is recorded.
Trial grid changes and step rejection do not consume reaction randomness.
The per-snapshot opacity proxy C rho_B Delta_x monitors spatial stiffness; its
normalization is a reference 1/(C rho_B) length, not a calibrated physical mean
free path. Dense stress runs can violate it and are not automatically resolved.

## Conversion and energy receiver

At fixed positions, toggle one medium sample and compute the complete finite
Delta=U_T(after)-U_T(before). B and medium masses and U_g are unchanged. With
reduced mass mu and incoming normal relative speed a, K=mu a²/2. Require
K>=max(Delta,0). For F->T set R=.91(K-Delta); for T->F set R=0. The outgoing
normal speed is sqrt(a²-2(Delta+R)/mu); apply its central equal-and-opposite
impulse and add R to the receiver Q. Thus

    Delta(K_pair+U_T+Q)=0, Delta P_pair=0, Delta L_pair=0.

Baryon-baryon collisions use restitution .5 and the same cell-local construction;
their kinetic loss enters Q. Radiation is an isotropic Newtonian receiver with
no incoming absorption or gravitating/recoiling radiation model. "Capture"
means F->T conversion, not a derived permanent bond to the encountered baryon.
No rotation barrier, object label, prescribed T fraction or global formation
energy pump is used. Full finite field saturation rejects a proposal; it is
never clipped or made energetically cheap by dropping self energy.

## Independent rate benchmarks

For unit total B and medium masses with the same spatial probability density p,
let velocities be independent N(0,I). For any fixed unit collision normal the
relative normal velocity has variance2, so E[(-v_rel dot n)_+]=1/sqrt(pi).
The exact mass-weighted normal-flux integral (C=1) is therefore

    I = integral p(x)² dx / sqrt(pi).

For uniform p on [-1,1]³, the overlap integral is1/8. For the normalized unit
3D Gaussian, it is1/(8 pi^(3/2)). These are independent known targets for both
cell-density overlap and the sampled velocity integral. Spatial node counts,
velocity sample counts, cell widths and random seeds are separately varied.
The benchmark is evaluated without live gravity or reaction thresholds, so
it tests the kinetic integration rather than a formation result.

For cold local distributions, uniform coflow and rigid rotation give zero normal
relative speed in the central-pair construction. A smooth cold compression has
zero collision rate in the exact point-local monokinetic limit but a finite
cell-induced rate proportional to cell width. Its measured decrease under cell
refinement is an error diagnostic, not genuine heat generation to be celebrated.
A fixed-partition boost/rotation check does not prove rotation invariance of a
rebuilt Cartesian octree.

## Interpretation boundaries

Keep numerical conservation, benchmark collision-integral accuracy, live spatial/
velocity convergence, and astrophysical evidence separate. The most refined
manufactured distributions have many more samples than the live simulations.
The local-limit approximation also requires h small against physical gradients;
that assumption is not established everywhere in an evolving system.

The inherited 3D RAR diagnostic uses radial gravitational forces at 12 radii and
24 azimuths in the initial xy plane, centered on current baryons. Nonpositive
radial samples are excluded and counted. This is a nonequilibrium diagnostic,
not a measured rotation-curve fit. Bound free fractions are instantaneous, and
the initial5.364Mb reservoir is assumed. Two dynamical times do not establish
late-time equilibrium or cosmological assembly.

Method background: SPARTA's primary documentation describes cell-based DSMC
collision organization and separate cell/time resolution diagnostics:
https://sparta.github.io/doc/collide.html
https://sparta.github.io/doc/compute_dt_grid.html
https://sparta.github.io/doc/compute_lambda_grid.html
These sources support the numerical framework, not the proposed T/F interaction.
