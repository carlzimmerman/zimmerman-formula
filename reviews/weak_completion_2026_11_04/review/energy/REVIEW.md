# Independent CC11 energy and narrow transport audit

The claim audited is the finite matched-energy update in `split_energy_v7.py`
(`d2079fafa099f2b2e1b7274f4549856c45e166a8444720b9297f89a7a513cd56`),
with `hybrid_number_v4.py`, `seeded_number_v3.py`, the common 30-group gas,
and frozen `transport_v3.py`/vector table003. **Primary verdict:
computationally verified only in the stated range.** The collision/expansion
split has the correct continuum tangent and a meaningful independent work
test. A direct, unaveraged field/particle control supports its local energy
and bulk-action normalization. Neither that control nor endpoint energy
conservation certifies every newborn population or a cold history.

This report is independent of the author's verdict. The direct integrator,
action quadrature, true-stage reconstruction and birth-chain analysis are new;
the canonical potential/masses, finite collision backend and positive BE solver
are shared inputs. No source, old review or physical state was repaired.

## Continuous identity and finite subflows

For fixed physical comoving numbers `Y`, the scalar potential is
`U(x,N,Y)=V(x)+Tc³ sum_a Y_a E_a(x,N)`. It is affine in Y, with all retained
massive particles contributing to its force. With canonical scalar mass 62,
`J=(1/2pi) integral p dx` over the full orbit and `omega=2pi/period`,

    dE = omega dJ + Tc³ <E_a> dY_a - 3 <rho+P> dN.

The identity `<p²/62>=omega J` follows directly by dividing the action
integral by the period. Averaged friction `3H xdot` therefore gives
`dJ/dN=-3J` on the expansion subflow, and
`dE/dN=-3<kin2+rho+P>`, where `kin2=62 xdot²`.
This is an orbit-averaged identity; the phase-resolved trajectory need not have
an exactly exponential instantaneous action at finite H/omega.

At fixed N the local collisions conserve the included particle energy.
If `Cbar` is their phase average, then
`cov=-Tc³ <E>.Cbar`. Expanding the collision endpoint equation
`E(N,J_new,Y_new)=E(N,J_old,Y_old)` with the actual BE particle increment gives
`Delta J=dt cov/omega+O(dt²)`. Thus conserving this Hamiltonian at the collision
endpoint is a consistent finite definition, not an arbitrary energy ledger reset.
It is also structural: the zero collision-energy residual alone is not an
independent test of the accepted population/action accuracy.

The inspected code splits expansion/collision/expansion, evaluates Simpson
FRW work from stress energy, and carries that work separately from the energy
root. BE is first order in the population equation. Symmetric placement of its
stages does not make the complete state integrator second order.

The concavity diagnosis is correct. Since `Emin(Y)=min_x U(x,Y)` is an infimum
of affine functions of Y, it is concave. Two equal-depth harmonic wells shifted
by d have midpoint potential minimum raised by `k d²/8`. Constraining that
midpoint population to the endpoint minimum energy can leave no orbit.
Using midpoint action and midpoint populations lets the intermediate stage
have its own energy, avoiding that obstruction without an action floor.

## Direct physical orbit, with independent work and action

`direct_orbit.py` starts at the actual fresh packet
`integration/run_initial_vector001/result.json`: `N=0`,
`x=.18444259422092926`, `xdot=0`, the FD charged fermions, the original tiny S/F
seeds, and exactly empty physical vector species. It retains all 30 species,
including bosonic `Vc_L,Vc_T,V8_T,V3_T,V1_T`, in energy, pressure and force.

Each direct interval uses an explicit leapfrog/friction field half flow,
a local positive BE collision at the actual midpoint x and N, and a second
field half flow. Radiation-background N(t) is integrated analytically.
The field map uses forces and velocities; **no action or energy root changes
an accepted direct trajectory**. Independent trapezoidal FRW stress work is
integrated on the two field halves. Action is measured afterwards by adaptive
quadrature of the frozen actual endpoint potential, using independently found
turning points. The same adaptive integral defines the requested initial period.

The initial action is `3.452436196101603e-5`, versus the stored 8-phase
`3.452436629319450e-5`; the fractional difference is `1.25e-7`.
The initial period is `1.243419971795455e7` in mu time, corresponding to
`N_end=1.894790718773337e-6`. Initial excitation is `2.399164148277657e-11 mu^4`.
Both direct runs reach exactly this duration without rejection.

| Direct nominal steps | 64 | 128 |
|---|---:|---:|
| Maximum sampled `abs(E+work-E0)/excitation0` | 9.904018914e-4 | 2.479386884e-4 |
| Endpoint `E+work-E0`, mu^4 | 1.818749541e-16 | 4.393489587e-17 |
| Measured endpoint J | 3.431012704e-5 | 3.430979749e-5 |
| Charged number / initial | .9995189639 | .9995188479 |
| Total Vc number in comoving coordinates | 5.876087724e-8 | 5.854921628e-8 |

The maximum sampled energy error falls by `3.99454` under step halving,
consistent with the explicit field map's second-order error here.
Endpoint J differs by `9.61e-6` relatively and the full physical-number L1
difference is `2.00e-7` of total number. These are measured differences, not
rigorous error bars or proof that all particle bins have that accuracy.
The chi group differs by 2.39% and the two Vc groups by about .34–.38%.
Some rare pointwise occupation changes are larger at finer resolution, so
maximum-bin accuracy cannot be inferred from the bulk norm.

In the 128-step run, the largest local BE collision-energy change is
`1.95215e-22 mu^4`, physical BE balance L1 `5.52e-14`, and the maximum populated
forward omitted fraction is `2.73e-5`. Positivity and Pauli bounds hold at the
recorded states; every accepted step checks them. No negative entropy increment
was observed. The finite momentum support and vector angular/polarization
closure remain shared assumptions, not independently completed continuum tests.
The measured cost was about 1.3 s per direct step. A 256-step job would exceed
the prescribed wall cap; the authorized bounded fallback was 64/128.

## Averaging versus newborn BE timing

One phase16 averaged v7 interval over exactly the same final N was computed
with a fresh E0 and work=0, preserving the ledger through every expansion
segment. It gives `J=3.430411076615080e-5`, about `1.66e-4` below direct128;
its independent work residual is `-8.67e-21 mu^4`.
Its small bulk-number difference does not validate newborn channels:
the chi population is about 5.94 times direct128 and Vc_L about 1.90 times.

There is an independent analytic discriminator. For an initially empty chain
`P1'=a, P2'=b P1, P3'=c P2`, n uniform BE intervals give

    P2_BE / P2_exact = (n+1)/n,
    P3_BE / P3_exact = (n+1)(n+2)/n².

One interval therefore has factors two and six. This is temporal birth ordering,
even with a perfectly fixed source and no phase-averaging error. The new
phase16 controls over the same actual duration give:

| Averaged BE intervals | 1 | 2 | 4 |
|---|---:|---:|---:|
| chi / direct128 | 5.94 | 2.99423439 | 1.87897796 |
| Generation-three toy factor | 6 | 3 | 1.875 |
| Vc_L / direct128 | 1.90145 | 1.44757947 | 1.21602904 |
| Generation-two toy factor | 2 | 1.5 | 1.25 |

Both new controls completed with validated manifests, in 111.7 and 197.9 s.
The chi ratios divided by their toy factors are approximately
`.990/.998/1.002`; this strongly identifies the dominant one-interval newborn
excess as temporal birth ordering. The vector discrepancy is not exhausted by
the toy factors. Four averaged substeps still give J `1.52230e-4` below
direct128 and full-number L1 difference `1.09350e-5`. A finite trend does not
prove the phase-averaged closure for every species or arbitrary history.
The 64/128 chi difference also limits the direct reference to percent-scale
newborn accuracy. No extrapolated infinite-substep abundance is certified.

## True midpoint-stage tolerance and solver scope

The optional previous state is only a Newton guess: every outer iteration
retains the original physical old state in `Y_new-Y_old-dt C=0`.
Four hierarchy passes also alter only a guess. The residual and Jacobian are
in physical number coordinates, with the already required hole signs on both
Jacobian sides. The log/linear route selection changes numerical solution
strategy, not the physical equation. The returned states still have declared
absolute number floors and floating gross-flux allowances; they are not exact
roots at arbitrary boundary scales. Sub-budget guess traces are numerical
error, not a physical production prescription.

`run_stage001` audits an actual fresh 30-group v7 step at `dN=1e-4`, phase8,
outside the harmonic branch. It saves each used operator geometry, then
reconstructs the true midpoint from the returned Y/J and builds a new operator
there. The old physical numbers remain bitwise unchanged.

The source stops after six outers with relative consecutive population change
`4.03e-6` and action change `1.41e-5`, satisfying its `2e-5` criterion.
The last used stage nevertheless differs from the reconstructed stage by
`2.67685e-5` of orbital amplitude in positions and `1.21918e-5` in normalized
phase weights. Physical BE residual L1 is `1.61e-16` at the used operator but
`1.65504e-6` at the true stage. Re-solving the same old state on that stage
changes total Y by `5.75855e-7` relatively. Thus v7's finite outer convergence
must not be described as inner-Newton-level self-consistency. Its work residual
`6.44e-19 mu^4` is much smaller because collision energy is enforced structurally.
`split_energy_v8.py` introduces a different geometry criterion/acceleration;
it was read for context but is not promoted by this v7 audit.

## Small-action qualification and ancestry

`precise_orbit.py` really retains the pre-existing branch at `J<J0*1e-7`:
`E=Emin+omega J` with harmonic positions and weights. Consequently the
`run_small_action002` fixture at `J=J_initial*1e-8` uses harmonic stage geometry.
It also uses the earlier `split_energy_v2.py`, not v7. The fixture supports the
concavity repair and removal of the large artificial-action effect; it does
not certify exact nonharmonic cold evolution or uniform v7 small-J accuracy.

At that fixture, the excitation `3.18086514e-19` sits on total energy near
`4.2e-9`. One float64 total-energy ulp is `8.27180613e-25`, or `2.60049e-6`
of excitation. The reported finest raw relative-action excess `3.73e-7`
is below that characteristic energy-inversion resolution. It is not a
sub-ppm cold-action error certificate. Offset/harmonic error control remains
necessary at still smaller action.

The inspected fresh 25-group coarse002/fine002 branches start at the original
CC10 N=0 FD packet, with E0 and work=0; later new-energy prefixes carry their
own E0/work rather than importing an inaccurate late CC10 prefix. The new
30-group initial packet embeds that same original state and adds physically
empty vectors, with identical initial energy. The direct controls also start
there. Partial evolving histories are not promoted here to completed targets.

## Narrow loop and binary follow-up

`loop_transport.py` embeds precisely the reviewed fixed-pole channels and
passes `source=None`, so it does not silently add the charged current-source
replacement. The inclusive per-component width enters the event coefficient
as `measure_parent Gamma M/E /2`; integrating the isotropic angle gives the
physical parent loss. The stoichiometric daughter weights already sum to two.
There is no additional pair or octet factor after the physical inclusive
width. Group measures supply the inverse degeneracy factors under the declared
spin-symmetric, representation-symmetric occupation closure.

The S/V eta replacement is used dynamically by AngularExact's products and
Jacobian; its already constructed energy/stoichiometry arrays do not depend on
eta. The recorded soft-parent test at `Tc/mu=1e-6`, 72 q nodes through 30000,
retains hard daughters, partners, direct gauge sectors and inverses. It passes
vacuum loss, reviewed chi branches, two daughters, finite-grid detailed balance,
energy and an interior Jacobian test. The hard-support result concerns the
tested soft NR mothers, not arbitrary hard parent populations or an evolving
orbit. Parent mass interpolation deviations are below `1e-8`; the API remains
a fixed-pole approximation and must not be extrapolated in x.

For `binary_events_v2.py`, direct differentiation gives
`dlog(f/A)/dY=1/(measure f A)`. The cancellation-aware source form
`S diag(c net) L_F - S diag(c R) S^T diag[1/(measure f A)]` is therefore correct
in its analytic interior. The new floors on `measure*f` and `measure*A` are in
the right number-coordinate units and leave the physical RHS unchanged.
They fix a finite-matrix overflow problem, not the physical collision rate.

Below the `1e-280` denominator budget, that matrix is a regularized Newton
matrix, not an accurate analytic derivative. For example a half-power daughter
factor at f=`1e-310` can have derivative of order `1e155`, while the floor
suppresses it by about 30 orders of magnitude. The new `1e-288/1e-310` controls
establish finiteness, not derivative accuracy or nonlinear solver convergence
there. Accepted physical residuals and conservation checks remain essential.
No physical Coulomb normalization is supplied by this algebra-only factory.
Both narrow root manifests validate; these source changes were audited rather
than independently re-executed in this review.

## Read-only Coulomb and conditional cold-ledger follow-up

The additional files inspected are `vectors/coulomb/elastic_builder_v2.py`,
`template.py`, `scalar_factory_v2.py`, `cold_stage_v2.py`, and their relevant
controls. The normalization can be reconstructed without their pass flags.
The derivative scalar current gives the direct-t numerator
`s-u=2(s-2m²)+t`; invariant two-body flux therefore gives
`dσ/d(-t)=g^4 C[2(s-2m²)+t]²/[16pi s(s-4m²)(-t+mD²)²]`, as implemented.
Its Moller velocity is `sqrt[s(s-4m²)]/(2 E1 E2)`. The number coefficient
has the required `Tc³ measure_i measure_j` dimensions.

An incoming unordered-pair sum has weight one for `i<j` and one half for
`i=j`. If the same domain includes each transition and its reverse and the
event already uses `F-R`, the reversible event representation needs another
factor one half. Thus the implemented off-diagonal/diagonal factors
`.5/.25` are correct. Removing that second half doubles the continuum weak
collision operator. This is separate from the physical identical-final-state
and exchange issues of a complete amplitude; the source explicitly retains
direct-t leading-log physics and excludes finite-log exchange/contact terms.

The physical scalar occupation conversion is also correct:
legacy `24 W f_legacy/(2pi²)` equals physical
`12 W f_physical/(2pi²)` when `f_physical=2 f_legacy`.
The independent group invariants are
`(4/3)²/8=2/9`, `(3/4)²/3=3/16`, and `(5/12)²=25/144`.
Their screening multipliers `12 C_r/d_A` are `2,3,5`.
The scalar factory embeds those twelve modes into the common gas; it does
not include scattering on every other populated species.

The template reprojects daughter energy fractions using exact new
`K=p²/(E+m)`. Preserving particle number and K preserves full E for this one
fixed scalar mass. The dynamic Coulomb-log multiplier is a tested leading-NR
approximation, not an exact invariant under changing temperature or screening.
Three named packets have template/fresh-builder RHS L1 differences at most
`.20434%`; that is not a uniform changing-bath bound. The fixed final-packet
relaxation changes the shape by `2.14%` over .1 Hubble time, with 4/8-step
shape difference `.02872%`. These are conditional old-packet controls.
The supplied Born kernel does not certify the full low-relative-speed rate;
the documented weak-Born diffusion and finite-log limitations must remain.

The cold chemical sink is `dY/dtau=-Tc³ Y(KY)/2` for the total twelve-mode
population. With per-charge density `n_i=Tc³ Y_i/2`, its pair event rate is
`n^T K n`; total charged loss is twice that rate. This explains the source's
two factors without adding another pair symmetry factor. Actual terminal
cascade cohorts retain their rest masses, momenta, pressure and force.

The signed ledger decomposition has the right signs. If `P` is scalar field
power, `EN` neutral exit energy and `EC` charged energy removal, the memory
residual is `EF=P+EN-EC`. Over a stage, the three measured pieces are

    finite = EF dt/s,
    cell = EC dt/s - E_removed,
    boost = (M R_event - EN) dt/s.

Their sum is `P dt/s + M DeltaY_pair - E_removed`, the actual model collision
increment. The cold action update adds `P dt/omega` at the midpoint and
applies the two expansion damping halves. Consequently `omega J/s` changes
by the same signed `P dt/s`; an absolute-power bound is not substituted for
this signed work.

The charged expansion work is an exact fixed-Y massive redshift difference;
the neutral work is the corresponding redshift difference of separately
retained cohorts. Those are legitimate analytic work evaluations. However,
the residual-subtracted total ledger is partly algebraic: the source defines
`dres=P dt/s+M DeltaY_pair-E_removed` from the assembled collision increment
and subtracts its cumulative sum from `E+work-Einitial`.
Thus its `6e-15` corrected closure is a useful accounting check, not an
independent physical conservation test. The un-subtracted model residuals are
`-4.29033e-21` and `-4.34737e-21` in mu per SM entropy, or
`-3.81901e-8` and `-3.86978e-8` of initial total energy. The finite/cell/boost
pieces reproduce those values with integrated interpolation closures around
`1e-30`. These separately reported nonzero residuals must remain visible.

All three requested Coulomb manifests validate with completed status.
This follow-up is a read-only derivation/code/output audit; no new Coulomb
normalization or nonlinear run was executed here. It uses an old conditional
late packet, not an ancestor of the new warm 30-group history. The later
`cold_stage_v3.py` refinement is outside this pinned review.

## Strongest safe conclusion and first missing cold implication

The new matched collision/expansion method has the correct leading identity;
the independent direct 30-group orbit demonstrates physical field/particle
energy consistency and convergent bulk action in the fresh local window.
The finite stage and newborn-population tolerances are separate from its
excellent structural energy ledger. The next full-history implication is
converged populations and action from this fresh state through the common
warm target and onward, with newborn-time refinement, validated changing-state
phase closure, adequate momentum support, material interactions/coherence and
controlled small-action geometry. Cold abundance and the retained gravity
state still require that complete history. No old late memory yield is joined
to this new early state.

All runs use prior contracts, wall/CPU caps 240/235 s, one numerical thread,
measured RSS, fresh directories and pinned source/data closures. Peak RSS of
the true-stage control is 3.30 GB because it intentionally retains all outer
operators. Exact validation observations, source hashes, commands and resource
results are collected in `provenance.json`. The direct128 reference stays frozen.
