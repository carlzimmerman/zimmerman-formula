# High-H conversion: nonlinear test and a second quantum channel

This calculation does not determine the final cold abundance. It tests the
late instability with the original action and identifies an additional
quantum conversion channel that a decay-only continuation misses.

The late Phi phase-space state is not available from the earlier simulation.
Therefore the new nonlinear runs are conditional tests, not a continuation
of the quantum source with fully derived Cauchy data. No cold seed is inserted.

## Local nonlinear experiment

The original m, M, g and lambda are unchanged. At the previously derived
probe a=1.3145655926e11, the no-transfer X envelope is A=1677.81415 GeV.
Start a local window at an X zero crossing, with its corresponding radial
velocity. Use neutral warm Phi waves in two momentum bands, each normalized
to rhoPhi=Cphi/a^4=8.33768e-5 GeV^4. This energy is a prescribed test value:
the old mass-inclusive bound does not uniquely fix the late energy or waves.
The X energy initially is 11.26474535 GeV^4.

The periodic 3D solver evolves both complex fields, cubic conversion,
quartic backreaction and spatial gradients. It has no phenomenological
number sink. It now separately records X kinetic/gradient/mass energy,
Phi kinetic/gradient/potential energy, and signed interaction energy.

Natural units are Omega=sqrt(2gA), F=Omega/sqrt(lambda), q=field/F,
z=Omega*t. The box length is 32/Omega. Four X cycles are evolved at fixed
expansion factor; H*dt is approximately 9.8e-9, so neglecting expansion
within this local test is justified. The initial bands are p/Omega in
[0.2,0.8] and [0.8,1.2]. Random Fourier coefficients are identical between
spatial refinements, with seed 2026102301. Projection of the initial momenta
sets the classical U(1) charge to zero. This is a test family of warm waves,
not an exact quantum-vacuum density matrix or a late state derived from it.

The preliminary 24^3 and 32^3 runs fail their UV-resolution requirement.
They are preserved as failed evidence records. In particular, their small
energy errors are not sufficient evidence that the excited spectrum is
resolved. Refined results and validity diagnostics are appended below.

## Why growing Phi energy is not the conversion efficiency

For locally fixed X, the exact minimum over Phi is

    Vmin,Phi(X) = -max(2g|X|-m^2,0)^2/(4 lambda).

Thus define energy above the instantaneous valley by

    Eexc = Ephi + Vinteraction - <Vmin,Phi> >= 0.

Ephi alone includes energy borrowed through a negative interaction term.
Neither Ephi nor Eexc is a conserved particle number. X energy loss must be
measured separately; even that can be reversible over subsequent cycles.
At large A the fractional valley-depth scale is

    epsilon = g^2/(lambda M^2) = 1.3328e-4.

This scale explains why a strong instantaneous negative curvature can coexist
with a small first energy transfer. It is not an all-time upper bound.
Homogeneous 1000-cycle controls retain almost all X energy, but their detailed
long-time phases differ under time-step refinement. These controls exclude
spatial fragmentation and cannot establish a cosmological survival fraction.

## A quantum route that can bypass blocked single-particle decay

The same action gives X + anti-X -> Phi + anti-Phi through one exchanged Phi.
At rest, the tree amplitude is 4g^2/(t-m^2), with t-m^2=-M^2.
The nonrelativistic cross section is

    sigma v = g^4/(2 pi M^6) sqrt(1-m^2/M^2)
            = 4.75243068e-8 GeV^-2.

The exchanged line is spacelike at this threshold; there is no on-shell
X pole or real-intermediate-state subtraction in this particular tree.
Independent angular quadrature agrees with the analytic finite-velocity
integral, including its threshold limit. This channel was already present
in the low-H diagnostics; its importance for the dense high-H continuation
is the new application, not a new interaction or a novelty claim.

For balanced X and anti-X with total density nX, the forward loss law is

    dnX/dt + 3H nX = -(sigma v/2) nX^2.

If a surviving high-H reservoir continued with its free envelope until
A=0.001 GeV, then gA/m^2=0.002168, nX=2.0004e-9 GeV^3 and
H=3.90251e-21 GeV. Its vacuum forward rate would be

    Gamma_ann/H = nX sigma v/(2H) = 12180.3.

This is a test of the proposed reservoir continuation, not a prediction that
it reaches this epoch unchanged. In particular, the Born vacuum result is
not a full calculation for a coherent X field in a correlated Phi medium.

There is a kinematic window worth pursuing: if a quasiparticle treatment
is valid and M/2 < mPhi,eff < M, ordinary X decay is closed while pair
conversion remains open. With a common effective Phi mass in the final and
exchanged lines and negligible X mass shift, the threshold propagator still
has t-mPhi,eff^2=-M^2. The rate changes by the final phase-space factor.
This approximation does not establish that the evolving medium occupies
that window; its self-energies and nonadiabatic phases must be computed.

## What can and cannot be said about cooling and survival

Vacuum pair conversion emits daughters with p=sqrt(M^2-m^2)=1.73251 MeV,
initially v=0.86608. If interactions subsequently cease, their momenta
redshift to p/m of order 1e-8 at visible T=0.8 eV for the displayed weak-field
anchor. Cooling itself is therefore compatible with this channel. This is
not a free-streaming transfer function or a bound-core calculation.

Forward-only integration with fixed radiation degrees of freedom gives a
remaining X fraction 1/(1+Gamma_ann/H)=8.2093e-5 and a Phi number approximately
equal to the original total X number. It gives one Phi per lost X, whereas
single-X decay gives two. Those are bookkeeping results of different reaction
networks, not interchangeable abundance estimates.

The illustrative forward-only yield is 2.91844e-7 if g*=g*s=106.75 is kept
constant, or 5.18073e-7 if they are instead held at 10.75. These constants
are alternative diagnostic cosmologies, not a realistic QCD entropy history
or an uncertainty bracket. The high-H source normalization was originally
chosen using an abundance estimate; proximity to the target is not an
independent prediction or a parameter-free success.

None of these forward-only yields includes inverse production, Bose factors,
coherent correlations, effective masses, or the early relativistic 4-to-2
network. They must not be reported as surviving cold abundances. A late
threshold 4-to-2 check can test a gas after it has cooled, but cannot bound
the missing earlier hot losses. No population is fed into collapse.

## Relation to existing work

Tachyonic resonance from trilinear couplings is an established mechanism:
[Dufaux et al. (2006)](https://arxiv.org/abs/hep-ph/0602144).
A different real-field inflationary model can also return to parent-field
domination after an early conversion stage:
[Antusch, Marschall and Torrenti (2025)](https://arxiv.org/abs/2507.13465).
These sources motivate distinguishing excitation from sustained depletion;
neither establishes the outcome for this charged two-field action.

## Completed refinement and audit

The 96^3 run passes the declared Hamiltonian, charge and UV checks. The
late-cycle averaged X energy loss is 3.44710e-5 of its initial energy;
at the end of four cycles it is 9.52313e-5. Thus about 99.9905% remains in X
at this endpoint of this conditional classical trajectory. This is not a
cosmological survival fraction. The averaged loss at 64^3 was 3.40991e-5;
the endpoint changes by about 8% relative between these grids. No claim of
percent-level endpoint accuracy or all-time convergence is made.

The 96^3 maximum total-energy error is 5.18e-8 relative to initial X energy,
and absolute charge drift is 4.29e-15 in simulation units. The final fraction
of free quadratic Phi energy beyond 60% of a one-axis Nyquist frequency is
0.003215 (0.322%), down from 4.43% at 64^3. The preceding coarse and refinement
batches remain marked failed because their UV checks did not pass.

The Phi positive-energy gain averaged over the final two cycles is 1.42741e-4
of initial X energy; the signed interaction contributes -1.08252e-4.
Most of that positive-energy gain is therefore not net reservoir depletion.
The final energy-weighted physical wavenumber is approximately 0.200 GeV,
so the produced fluctuations cannot be called cold at this epoch.

The same resolved state raises a quantum-control warning: a free-mode
occupation proxy puts 13.8% of quadratic Phi energy in modes with f<1 and
43.8% in modes with f<10. These are diagnostic occupations, not an interacting
quantum particle measurement. The result is enough to reject a uniformly
large-occupation approximation as an established late kinetic closure.
Resolving the classical lattice does not resolve this quantum limitation.

For the separate conditional pair-conversion anchor, replacing the daughter
mass by 0.6M, 0.75M or 0.95M leaves single decay closed but gives Born forward
pair-conversion rates 11251H, 9302H or 4391H, respectively. These rates
presuppose a valid quasiparticle treatment with those effective masses.
They identify a possible bypass of single-decay blocking; they do not
establish a self-consistent in-medium evolution.

If the forward-only daughters subsequently redshift freely by a factor
866.26, their momentum is 0.002m, below the narrow-resonance scale u*=0.02.
For the corresponding hypothetical balanced incoherent gas, the saved
threshold 4-to-2 coefficient gives Gamma_4to2/H=5.70e-13 and a subsequent
forward fractional loss approximately 8.15e-14. The important uncomputed
loss is earlier, while the population is hotter and still coupled. This
late check cannot be applied backward to that interval.

The independent audit reconstructs the final Hamiltonian from saved arrays,
checks the component sum and differentiates the potential independently.
Its initial 1e-12 summation comparison was too strict for the serial sums
over up to 884736 cells (observed discrepancy at most 3.71e-11). The preserved
first audit therefore fails. Version 2 uses a documented 32*Ncells*epsilon
summation allowance. This is distinct from the separately measured trajectory
energy error and does not relax the UV or dynamical convergence requirements.

Evidence: `late_conversion_96_run`, `late_homogeneous_probe_run`,
`highH_annihilation_gate_run`, and `late_transfer_audit_v2_run`.
The full scripts, binary initial/final states, CSV histories, contracts and
manifests are retained. `late_transfer.png` shows the energy accounting.
The final high-H cold yield and its coupling to collapse remain undetermined.

All seven new run manifests validate against their current inputs. The four
current positive evidence records listed above have status `completed`;
the two coarse lattice batches and the original over-strict summation audit
retain status `failed`. All launched calculations have finished.
