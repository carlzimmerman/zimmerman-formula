# CC11 matched Hamiltonian/action energy update

Base checkpoint: `dca7a564b31be47fe51049509ade99042a3a2afb`; exact source
and input versions are pinned by the fresh v2 records. All physical scales
remain e=.003, mu=2e6 GeV, xi=.02 and the existing leading gravity packet.
This work changes time discretization, not the potential, vertices or sectors.

## Continuous identity and the diagnosed finite defect

For the all-species orbit Hamiltonian E(N,J,Y), Y denotes physical comoving
number coordinates and J is the scalar action with radial coefficient 62.
In the continuum orbit integral,

    dE = omega dJ + Tc^3 <E_a> dY_a  at fixed N.

Every local collision operator retains all daughter energies. With its phase
average Cbar and centered covariance cov,

    cov = Tc^3 [<E.C>-<E>.<C>],
    dJ/dN|collision = cov/(omega H), dY/dN=Cbar/H,
    dE/dN|collision = Tc^3 <E.C>/H = 0.

The independent CC10 diagnostic verifies the local gradient identity at ppm
scale and the expansion identity at about 4e-8. Its finite-step decomposition
shows that BE populations on old geometry, log-action Heun using start/end
covariances, and nonlinear Hamiltonian reconstruction do not share the same
finite increments. No large normalization or factor correction is inferred.

## Physical subflows and the independent work check

The new composition has three stages:

1. Expansion over dN/2 at fixed Y, using J_new=J_old exp(-3 dN/2).
2. Collision at N_mid. Solve the positive quantum population BE equation,
   then determine the new action from the same actual population increment
   by E(N_mid,J_new,Y_new)=E(N_mid,J_old,Y_old).
3. Expansion over dN/2 with the new Y and the same action damping law.

The collision endpoint equation is a discrete Hamiltonian conservation
condition, not a change of the energy ledger. Its infinitesimal limit gives
the continuous action covariance through the orbit gradient identity above.
BE remains first-order; symmetric placement of expansion stages does not
make the whole method second-order.

FRW work is integrated independently on each expansion segment from

    W'(N)=3 <kin2+rho+P>, kin2=62 xdot^2.

The work integral uses Simpson evaluations at the segment start, middle and
end, with actual gas distributions, redshifted momenta and orbit geometry.
It is never assigned from E_old-E_new. The global check is reconstructed
Hamiltonian E plus this independent work minus the fresh initial energy.
The collision invariant is structural; the work comparison still tests the
expansion/force/action geometry, energy roots and temporal composition.

## Why the midpoint action, rather than midpoint energy, matters

The collision geometry is an outer fixed point. Every trial re-solves the
population equation from the original old physical state. It does not
accumulate fictitious extra reaction time. Its geometry uses

    Y_stage=(Y_old+Y_new)/2, J_stage=(J_old+J_new)/2.

Both the population and action fixed-point changes are checked. The stage
energy may differ from endpoint energy by O(dN^2). Forcing a linearly
interpolated population onto the old energy surface is invalid near J=0.

The obstruction is explicit. E_min(Y)=min_x[V(x)+rho(x,Y)] is concave in Y.
Take two endpoint harmonic wells

    U0(x)=E0+k x^2/2,
    U1(x)=E0+k(x-d)^2/2.

Both have zero-excitation energy E0, but the linearly interpolated population
has U_mid=(U0+U1)/2 and minimum E0+k d^2/8. An orbit constrained to energy E0
does not exist there. A midpoint action of zero instead evaluates the
intermediate minimum at its own stage energy, with no artificial oscillation.

This distinguishes the promoted action-centered version from the failed
energy-surface midpoint version. No action floor, accepted clipping or
unjustified adiabatic-minimum replacement is introduced.

There is an inherited *geometry approximation*: `precise_orbit.py` switches
to the local harmonic well when J<J_initial*1e-7. It still evolves the
requested positive J; it does not replace J by a minimum value. The
`run_small_action002` test uses that branch. Its energy and timestep controls
therefore certify the finite harmonic-geometry method at the tested state,
not arbitrary small-action nonharmonic accuracy. A separate cancellation-safe
oracle is being developed in `../cold_offsets/`; its validation must precede
using this branch for a cold-state conclusion.

## Positive population solve and exactly empty new species

The backend protocol is unchanged: physical-number RHS and Jacobian, gross
forward-plus-reverse measure, and explicit Pauli availability. All solver
versions preserve physical-domain line searches and retain fermion holes.
The seeded solver uses the previous outer-iteration root only as a Newton
guess; the old state and BE residual remain unchanged.

Exactly empty new species can receive a positive Newton guess while their
physical old occupation remains exactly zero. A scalar FF<->P<->VV control
demonstrates V born from P within the same step, and agrees with a 90-digit
BE reference. This is not an initial particle-production prescription.

The fresh N=0 S/F packet also exposes a distinct initialization issue: almost
all non-F coordinates contain the declared tiny seed. A single positive-gain
predictor leaves daughters of newly born parents at that seed and can give
an incorrect-sign Newton direction. The later solver propagates positive
gain guesses over four hierarchy passes across rare coordinates before
solving the unchanged full BE equation. The predictor is not accepted as a
physical update. The actual N=0 matched-step control verifies the result.

Every iteration checks the actual physical-number residual. Number-coordinate
merit floors are numerical error budgets, not rates or physical sources;
holes retain the explicit relative scheme. Failed solver versions and their
traces are preserved, rather than relabeled as physical escape.

## Declared finite controls

`run_one_step001` compares a single step at the actual fresh checkpoint.
At dN=5e-5 the old Heun/BE coupling has an energy/work defect of 3.1753e-4
of orbital excitation. The split with independently integrated FRW work
reduces this to about 3e-10 for the tested old/mid geometry variants.
This is a local discriminator, not a completed fresh history.

`run_small_action001` confirms the old-geometry moving-minimum problem:
at actual warm Y with J=J_initial*1e-8 and dN=1e-5 it creates excess action
73.8 times the physical initial action. The old energy-surface midpoint then
fails its closed-orbit or outer-convergence conditions.

`run_small_action002` tests the corrected midpoint action. Relative excess
over the physical linear collision tangent is -.004732 at dN=1e-5,
-3.18e-5 at dN=2.5e-6 and +3.73e-7 at dN=6.25e-7. All quantum bounds,
entropy and endpoint energy checks pass. This is a finite moving-minimum
control; it is not a uniform cold-limit theorem.

`run_seed001` checks optional seeded Newton guesses against the unseeded
same action-centered fixed point: physical-number L1 difference 8.8e-17
relative and action difference 1.6e-14 relative. These guesses change cost,
not the numerical physical equation.

`precise_orbit.py` is an immutable copy of the prior orbit implementation
with only the total-energy action root tightened to xtol=1e-30, rtol=1e-15.
This permits excitation-scale controls; no physical Hamiltonian is changed.
Very small cold excitation ultimately needs offset/harmonic resolution or a
separately controlled moving-minimum approximation, rather than a hidden J
floor. Those extensions are not silently assumed here.

Fresh coarse/fine histories start from the original N=0 packet and work=0.
Continuations are accepted only from this package's saved matched-energy
ancestry. Completion, energy error relative to excitation, and population/
action refinement are recorded separately. A partial checkpoint is not the
full benchmark. Vector transport and on-shell decay matching remain separate
dependencies owned by the coordinator and the other work packages.

## Completed fresh benchmark and remaining state error

`run_benchmark001` consolidates the complete ancestry of both fresh histories
at N=.0021690179772784167. The coarse maximum step is 1e-4 and the fine
maximum step is 5e-5; both use eight phase nodes and the same frozen v7
numerical method. Their independent global work residuals divided by orbital
excitation are 3.59850e-7 and 1.16579e-7, respectively. The old preferred
history had .238459 at this checkpoint. The requested finite energy-error
threshold of 1% of excitation is met by both fresh histories, with refinement.

This ledger agreement is distinct from state convergence. The endpoint
action changes from 2.12177629116e-6 to 2.22418570094e-6 (+4.8266%);
charged yield changes by -.03857%, U1 yield by -1.7141%, and mean U1
momentum by -1.3100%. Full-number relative L1 difference is .00571873.
Consequently the first-order population/action solution is not claimed to
have 1% action accuracy. The data contain actual fresh populations and work,
not an energy reset at an inaccurate ancestor.

The optional population-midpoint wrapper evaluates the collision RHS at
arithmetic means of old/new f and separately retained availability, with
Jacobian multiplied by one half. It keeps the endpoint-domain line search.
For linear decay, the midpoint amplification is (1-z/2)/(1+z/2), so z>2
must be rejected rather than clipped. Its separate bounded control tests
the common warm state with 1/2/4 substeps; the fresh benchmark above remains
on BE until actual order, entropy and quantum-bound checks justify promotion.

`run_midpoint001` exhausted its 235 CPU-second limit inside the first
actual dN=5e-5 warm step, without an accepted endpoint. Its known linear
z=1 positive root and z=4 negative-root rejection pass. This is resource
inconclusiveness, not a physical exclusion of the warm state.

`run_midpoint002` reduced the common interval to 1e-6 and capped each
refinement case at 50 wall seconds. The one- and two-substep cases
complete, remain positive with entropy increase, have physical-number
residuals about 1e-16 to 1e-15, and independent work residuals about
-6e-11 of excitation. Their actions are 2.2213297135116743e-6 and
2.2213297129103686e-6. The four-substep case exhausts its case budget
after three substeps; its third partial-step physical-number residual
8.14e-11 exceeds the diagnostic 1e-12 target. Thus the record fails its
completion assertion, provides no 1/2/4 order estimate, and does not
promote midpoint populations. BE remains the reference method. Neither
the stiff toy nor positive partial states establish a higher-order quantum
history.
