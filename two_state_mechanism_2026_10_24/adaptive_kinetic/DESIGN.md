# Adaptive kinetic capture: experiment contract and implementation plan

Authorized continuation of field3d_capture. Use an adaptive-cell stochastic
kinetic collision operator (DSMC-style), separate phase-space particles for B/F/T,
and the existing conservative full 3D longitudinal field. This is an effective
kinetic model, not a derived microscopic cross section or a different polarization
closure. No galaxy-type switches or imposed T fractions.

The local Boltzmann approximation replaces the tiny finite-volume encounter
kernel by reconstructed cell densities: gamma_ij = C m_b [-v_ij dot n]_+ / V_cell.
The 0.1kpc kernel has unit spatial integral; this limit assumes its range is
small relative to density/velocity variation scales. Cell size is numerical,
not a new physical range. Different macro-particle centers in a cell stand for
co-located collision distributions; central impulses conserve total P and L,
but finite-cell geometry is an approximation tested by spatial refinement.
Do not claim that every macro-center separation is a physical encounter.

An octree refines occupied regions to a maximum cell width and further divides
crowded leaves. Unlike the former expanding-neighbor radius, it never grows a
cell around a particle until a partner is found. Empty leaves have zero collision
estimate. All particle pairs in a leaf are considered, with proper volume and
mass weights; no unreported nearest-neighbor extrapolation.

Vary spatial carriers and velocity samples per carrier separately. Replicated
velocity beams start at the same spatial nodes with divided masses; they then
transport independently. This is a sampled velocity distribution, not a Maxwellian
closure imposed during evolution. Include the constant softened gravitational
self energy so splitting coincident equal-velocity samples leaves density energy
unchanged. This constant changes neither gravity forces nor collision work.

Use the existing exact finite field-energy jump, central reaction impulse and
radiative receiver. No kinetic-energy rescaling, energy projection or artificial
formation source. Full Hamiltonian forces and time-step error control remain.
A max displacement/cell-width and per-particle hazard bound resolve kinetic
splitting. Report accumulated expected proposals as well as realized events.

Before live interpretation, test:
1. Uniform and Gaussian manufactured distributions against known density-overlap
   and Gaussian-velocity collision integrals; vary spatial and velocity sampling.
2. Partition volume/containment, rotation/boost properties of the instantaneous
   kernel on a fixed partition, and physical-range independence of the local limit.
3. Self-energy-invariant velocity replication and a reacting nonzero-field test.
4. Cross all four mass/size inputs with rotating/unordered initial conditions;
   refine spatial carriers, velocity sampling, cell width, and selected time steps.

All runs bounded and hashed using computation-audit. Controls may fail; retain
failures and distinguish implementation, local kinetic convergence, Hamiltonian
conservation and astrophysical claims. Existing illustrative targets:95%T in
rotating systems,90%bound-free retention, .05dex RAR. These are not observational
likelihoods. Finite failed targets are not a universal no-go theorem.
