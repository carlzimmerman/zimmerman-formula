# NC result: a completed local transfer channel, not a formed galaxy

The original goal remains open. This phase derives a missing term in the local
reduction of the existing CC interaction and verifies a nonlinear material-mode
to escaping-wave channel with reciprocal backreaction. It does not establish
that an actual galaxy supplies those modes or forms the required law.
All galaxy tests here use the inherited synthetic Plummer benchmark, not a new
real-galaxy population fit.

## The missing term and its independent check

The full CC action already contained conservative nonlinear inertia. The first
local triad reduction omitted that term while adding radiation, so its weak
cascade was not a test of the complete CC dynamics. No new operator or galaxy-
residual cancellation force was added to the full action.

[CC_CUBIC_DERIVATION.md](CC_CUBIC_DERIVATION.md) derives the density kinetic
metric(1+eta)/(rho k²), eta=g2²rho³/c², and its full cubic Hamiltonian. This
includes the velocity, quantum pressure, nonlocal response and nonlinear
inertia vertices. The latter can dominate the small remainder after bare
velocity and quantum terms cancel. For transverse short waves its coupling
rate at fixed density amplitude scales eta/(1+eta)^(3/2), with local maximum
at eta=2. This is not a global cooling optimum or a derived microscopic g2.

The independent audit eliminates the original variable-density phase/scalar
spatial square before differentiating. Mixed third derivatives agree with the
complete cubic vertex to2.6e-14 for eta0,.001,.1,1. The earlier bare vertex
also passes its own independent third derivative check; its scope was the
bare Hamiltonian, not full CC. See run_cc_vertex_audit and run_vertex_audit.

## Pump depletion, reaction and actual outgoing waves

The local model uses actual benchmark coefficients near3.02kpc and the already
specified g2=171.680273197 (old global eta=.01), giving local eta=1.01823.
Six material modes include two noncollinear parent pairs and their daughters.
The initial density perturbation normalization is5%, not the full infall
release. The parent occupations are declared inputs, not actual measured
angular occupations. Their modal Hamiltonian is coupled reciprocally to a
radial massless field with zero incident field and an absorber outside the
local material patch. The field force, pump depletion and all near-field
reaction in this retained model evolve together. No emitted-power fraction,
Markov damping coefficient, or prescribed oscillation supplies energy.

| Local test | Time(Myr) | Maximum daughter material energy | Actual sponge export |
|---|---:|---:|---:|
| Complete cubic, dt=.005 |150|27.7925%|3.70176%|
| Complete cubic, dt=.0025 |100|27.79254%|2.41635%|
| Complete cubic, wave h=1kpc |100|27.79185%|2.41642%|
| Omit conservative nonlinear inertia |100|3.15991%|2.70876%|
| Zero compression interaction |100|0.000725%|0|

Percentages refer to the initial LOCAL mode energy, not a galaxy's binding
release. The150Myr run has relative total-energy error2.25e-10 and shift-charge
error3.38e-14. The time-halved run has energy error2.99e-11. The exported
energy is actual positive outer absorption; near-field storage is separate.

The detector spectrum confirms daughter-frequency radiation. With two windows,
its fraction of the windowed radiation-component signal is12.18–12.42%,
versus.189–.196% when nonlinear inertia is omitted. The daughter-band energy
is about53–56 times larger in that controlled comparison. The bands are near
2Omega_parent and2Omega_daughter, around2.13 and4.27rad/Myr. Detector spectral
proxies are not the same as finite-radius total flux or differently delayed
sponge loss. See run_analyze_wave/results.json.

At the bare resonance, the complete cubic transfers much more energy to daughters but exports slightly
LESS total energy than the omission control by100Myr. This tradeoff is retained,
not hidden by quoting only the stronger daughter line. More cascading is not
itself more effective cooling.

The next discriminator includes the reaction-induced resonance shift. Fixed
angles predicted from that same field self energy increase peak daughter
transfer to64.79% and outgoing export to5.0308% by150Myr, versus27.79% and3.7018%
at bare resonance, with the same parent energy and coupling. Full initial-shift
compensation also improves export (4.0527%). No angle varies during a run.
See NONLINEAR_PHASE_MATCH.md; the half-time-step control is recorded separately.
These are local geometry tests, not an actual infall angular distribution.

A reciprocal channel ablation keeps the conservative dynamics but removes
only the daughter term from both wave charge and material reaction. It reduces
the daughter-frequency fraction to.089–.091% (versus12.18–12.42%) and100Myr
export to2.19108%. This supports attribution to the daughter radiation channel;
the residual band need not be assigned to that channel.

The predicted half-shift case also passes its dedicated half-time-step check:
peak daughter64.78622%, export5.0307957% by150Myr, versus64.78620% and5.0307958%
at the base step. Relative total-energy error falls to4.78e-11. Both constant
predicted angles improve export over the bare linear resonance in this model.
The wave bath, source energy and coupling remain the same.

The model is a local cubic/WKB truncation with a stated3D extension, fixed mean
background and declared weak parents. It omits higher material interactions
and cannot test a moving galaxy interface, outer F reservoir, mass redistribution
or a law. The5% density number is an initial normalization, not a proven bound
on every later density extremum. The global g2 remains a hypothesis.

## Actual infall: what was measured rather than assumed

The full NT action was re-evolved with free complex fields, finite carrier and
reciprocal waves, resolving material-gradient work by force. At30Myr the high
kinetic band grows from1.04e-6 to.001372Eunit; its discrete work identity closes
6.35e-16. A kinetic label can also represent phase winding, so it is not called
a full Hamiltonian occupation spectrum. Independent actual density/current
histories find7.28–7.48% of inner density-variation and1.96–1.97% of inner
current weighted spectral proxies above1rad/Myr. These support real fast
compressive content but do not determine nonradial modal occupations or
prove sustained mean-flow feeding of the local cascade.

## A numerical material-wave trap was removed

The old material mesh coarsened beyond80kpc and cannot carry short material
waves through that region even when mass and energy are conserved. A matched
energy1 wave packet after250Myr has mass beyond90kpc1.9e-27 on the old mesh,
versus essentially1 on both new .125 and.0625kpc meshes. Mass and energy errors
are of order1e-13. This is a propagation-control result, not a galaxy result.

The refined full model keeps the material grid uniform from.5 to320kpc and
retains the complete outer reservoir to6.6Mpc. All material forces and the
physical response are unchanged. The finer mesh is a new regime, not another
attempt to fit the old trapped profile. A complete material force derivative
check passes6.8e-9; the nonzero-scalar CC force check passes2.6e-8.
Initial species masses are positively and conservatively interpolated; this
does not certify a new fine-grid equilibrium.

## Global tests still do not satisfy the user's joint conditions

The refined REFERENCE g2=0 infall reaches134.778Myr before a minimum-step
failure. It has law error16.6458%, density rebound6.383, boundary62.905kpc and
outer T fraction5.27e-5. The physical cap has not been reached. The gap is
worse, and the law has not formed. Its F100kpc ledger closes4.2e-12; positive
raw energy flux is still accompanied by inward mass, not demonstrated
positive outgoing excitation cooling. A step failure is not a late-time no-go.

Selected overlapping fine-grid time-halving checks at58.218Myr differ in law
error by5.4e-7 percentage points, boundary by.00131kpc and rebound4.6e-5.
Material h-halving at62.060Myr differs in law error.00091 percentage points,
boundary.0378kpc and rebound.0136. These check selected observable behavior,
not every high-frequency phase or a continuum/global theorem.

The complete CC candidate was separately tested on the refined material and
inner-collocated scalar grids, with every density/carrier/boundary variable
free and the exact quadratic charge. The infall run reaches only.319752Myr
within its480-second bound; law error remains17.3679%, density rebound1 and
outer T fraction4.1e-14. Its energy error is9.81e-10 and mass error4.9e-14.
The all-F birth run reaches8.21Myr with T mass.0004375Mb, nine phase crossings
and law error473.69%. Its rebound diagnostic is undefined for that small
structure, so it is not counted as a filled galaxy transition. Both are resource-limited, not successful
formation histories or evidence ruling out eventual formation.

The old active-radial restoring minimum remains a valid inherited finite-grid
static statement, and the CC extension leaves its relaxed static energy
unchanged. This phase does not establish restoration together with the active
cascade in a fully formed galaxy. Noncollinear local triads further require
angular seeds/evolution; a spherical global run cannot validate that part.

## Numerical hypotheses kept separate

Momentum reparameterization did not improve the stalled defect. Trigonometric
carrier divided differences conserve the fixed-density potential but do not
fix full density-inertia work. Recovery probes do cure one time-step-controller
hysteresis but not every stiff step. Diagonal, phase and frozen-density scalar
Schur preconditioners did not converge the tested large full-CC step; those
failed roots were not accepted as physical trajectories. The first comparison
script used mismatched sampled times; run_compare_checked is authoritative.
See DEPENDENCY_IMPACT.md for corrections without overwriting frozen evidence.

The next dependency is the mean-flow obligation in MEAN_FLOW_OBLIGATION.md:
actual infall occupations and their reciprocal mean stress must supply the
channel while density and the boundary form the law. A local reservoir of
prepopulated weak modes does not establish that obligation.

A coupling homotopy inside the nonlinear solver does recover one accurate
large full-CC step at the target coupling. Reusing it permits two accepted
steps, then the third trial fails. The corrected accepted-state audit reports
only.005Myr, energy error2.77e-10 and charge1.14e-13. This is not a production
solver or physical evidence from the rejected third root.
