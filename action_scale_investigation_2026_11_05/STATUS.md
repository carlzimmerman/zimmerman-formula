# Joint-model continuation: pool speed calculation; coefficient unresolved

Latest checkpoint: joint_phase/PHASE_BOUNDARY_RESULT.md replaces the fixed
radius by a dynamic phase interface with mass-step trapping and force
P+DeltaV-2Sigma/R. Coupled moving-wall radial stability was computed. A
higher-energy interior yields sampled phase-confined damped branches with
roughly flat outer curves; radii approach independent free-boundary BVP roots
under refinement. A failed intermediate solve is preserved and recovered by
continuation. The source family is not uniformly flat and v_edge^4/source
varies strongly. Phase parameters, microscopic feasibility, source origin,
kinetic/nonspherical stability and MOND1/2 remain unresolved.

Latest checkpoint: joint_phase/COOLED_PROFILES_RESULT.md numerically solves
coupled density, temperature, radial flow and self-gravity with excitation
cooling and a prescribed reflecting outer wall. Eleven distinct parameter
configurations yield damped discrete radial modes; selected profiles and modes
converge through96 cells. Discrete number balance is exact and energy-budget
error decreases under refinement. Most rotation curves rise; a strong-gravity
example flattens near the edge. Edge-speed normalization varies with imposed
radius, explained by v_edge^4/S_total=gamma^2 R f/(3K). No vacuum-selected
boundary, universal galaxy stability or MOND1/2 is derived.

Latest checkpoint: joint_phase/RADIATIVE_EXPORT_RESULT.md tests an explicitly
new excited-scalar extension that exports heat through radiation without
consuming heavy particles in its cooling cycle. Decay, thermal excitation,
line-opacity and new-annihilation conditions are derived. Local source/cooling
balance is restoring, but an exact isothermal inward-flow trial still fails
pointwise heat balance. Coupled spatial equations are conservation-checked,
not solved.21 positive checks pass; double-counted pair cooling fails one
control. No finite globally stable halo or universal1/2 is established.

Latest checkpoint: joint_phase/RADIAL_SUPPLY_RESULT.md derives radial
redistribution for the actual mediator source. An explicit long-decay inward
flow repairs the previous no-flow particle-profile mismatch. Its thermal
budget requires conductive heat transport; a wide insulated isothermal shell
fails energy balance. Strong self-scattering improves collisions but reduces
short-path conductivity.12 exact checks pass; omitted source momentum fails
one control. No complete spatial solution, global stability or1/2 is derived.

Latest checkpoint: joint_phase/SELF_COOL_SUPPLY_RESULT.md derives energy-
dependent contact self-scattering and Maxwell evaporative cooling. With fixed
injection, volume and escape potential, conserved particle/energy equations
have a unique positive equilibrium and locally stable density/temperature
modes. Actual retention still requires spatial transport. A no-flow flat tail
requires J proportional r^-4, unlike the existing mediator source, and its
replacement power depends on the unresolved core and microscopic rates.
15 exact checks pass; omitted number-change energy term fails one control.
No global halo stability or MOND1/2 is established.

Latest checkpoint: joint_phase/SPECTRUM_THERMALIZATION_RESULT.md derives a
conditional dilute Wien spectrum and tests repeated scattering, inverse
reactions and virial thermal response. In the uniform cold unreplenished model,
opacity and long material lifetime conflict because sigma_0 c/K=4. Dilute
chemical equilibrium is radiation-dominated in the cold limit. Independent
material thermalization still needs a coupling hierarchy and energy export.
24 exact checks pass; reversed heat-capacity control fails two intended checks.
No complete halo stability, preserved thick-limit rotation curve or1/2 follows.

Latest checkpoint: joint_phase/FRONT_CAPTURE_RESULT.md derives thin-wall motion,
its energy partition, a specified-gas drag limit and ballistic halo energy
retention. An empty accelerating wall stores latent power; radiation requires
a corresponding loss. Hard photons mostly eject cold targets in the single-
scatter limit. Speed and retained power still depend on unselected medium,
wall and spectrum inputs.16 exact checks pass; double-counted-radiation control
fails exactly one. No whole-halo stability or universal1/2 is established.

Latest checkpoint: joint_phase/REPLENISHMENT_RESULT.md tests physical supply:
constant vacuum has zero advective enthalpy flux; spherical ordinary accretion
has derived M^2 scaling with environmental inputs; an expanding phase front
harvests fresh vacuum but fails the simple isotropic phase-pressure halo power
and distant cooling-bath tests. A turnaround sweeping prescription yields a
conditional linear mass power but retains an imposed speed and interception.
16 revised exact checks pass; enthalpy-omission control fails one intended check.
The original central-source cooling comparison is retained and superseded by
correct external-shell geometry. No selected power, stable whole halo or1/2.

Latest checkpoint: joint_phase/BARRIER_SUPPLY_RESULT.md derives a barrier from
an explicit heavy-scalar interaction, including exact coexistence and the
kinetic limitations of its effective expansion. Coupling conversion to bath
escape gives a finite-reservoir energy identity: no nonzero closed stationary
bath exists. Thermal regulation can be transient; replenishment fixes power
through an additional source.18 corrected exact checks pass; depletion-sign
control fails one intended check. An initial solver-domain failure is preserved
and explained. No selected source, whole-halo stability or1/2 is derived.

Latest checkpoint: joint_phase/BOUNDARY_COOLING_RESULT.md derives a soft-radiation
cooling mechanism from the same scalar contact interaction. A local fixed-bath
thermal equilibrium is restoring when16 U_a>rho_pool c^2; supplying that bath
and including its stress remain unresolved. An explicit tilted-quartic wall
and bounce give an exponentially barrier-dependent nucleation rate and a
finite, time-dependent conversion power.15 exact checks pass; cooling-sign
control fails two intended checks. No globally stable finite halo, source
spectrum, selected decay rate or MOND1/2 is derived.

Latest checkpoint: joint_phase/FINITE_HALO_RESULT.md finds that a smooth,
stationary impermeable boundary with annihilation requires net cooling:
H_net(R)=-K n(R)^2 kB T(R)<0. The prior heating-only completion therefore has
no such finite equilibrium to test for stability. Capture/thermalization need
unselected optical-depth and rate hierarchies. Constant vacuum supplies no
local transfer power; phase conversion retains an independent rate and finite
reservoir.12 exact checks pass; compression-omission control fails one intended
check. No finite stable halo, luminosity-vacuum selector or1/2 is established.

Latest checkpoint: joint_phase/TRANSPORT_CAPTURE_RESULT.md derives portal-based
single-scatter capture conditions and a conditional annihilating-fluid outer
balance n~r^-2,u~r^-1,T~constant. It includes exact finite-inertia/energy residuals,
so is not a full halo solution. Existing chi-a scattering relates microscopic
heating and annihilation: the coupling cancels from zeta=c sigma_E/K, yielding
v_flat^4=2 G zeta L_a/c at leading order. Capture efficiency, fluid closure,
hard-recoil retention, spectrum, source and boundaries remain unselected.
14 exact checks pass; the sink-sign control fails its intended check. A
kinematic upper bound zeta<=1/2 is explicitly NOT the MOND coefficient;
no universal luminosity/vacuum relation or1/2 derived.

Latest checkpoint: joint_phase/PARTICLE_REACTION_RESULT.md derives explicit
S->chi chi and chi chi->a a rates with a baryonic mediator portal. Number and
energy moments give a local joint attractor with a stellar energy source.
The resulting reaction profile is exp[-r/(2l)]/r, not a flat-tail density, and
its constant-temperature pressure is not hydrostatic. Conditional peak-speed
v^4 proportional to Mb survives only with assumed L_S proportional to Mb;
its normalization remains free and is not a supported flat-curve prediction.
25 checks pass; dilution mutation fails two intended checks. The prior global
feedback law, phase pressure and1/2 remain underived.

Latest checkpoint: joint_phase/COUPLED_FEEDBACK_RESULT.md constructs a global
phenomenological abundance/temperature feedback with a positive-state Lyapunov
proof of convergence, preserving conditional v^4 proportional to Mb. This is
a postulated source law, not a microscopic derivation or a full halo attractor.
A local power-law reaction calculation identifies a neutral mode in the
scaling-compatible case. 42 checks pass, including12 trajectories; the negative
control fails two intended determinant checks. Pressure, reaction energetics,
transport, and heating/cooling normalization remain unselected. No1/2 derived.

Latest checkpoint: joint_phase/RELAXATION_RESULT.md derives thermal reservoir
relaxation and baryon-powered heating/cooling feedback. Reservoir exchange can
erase abundance memory conditionally but imposes reservoir T and chemical
potential; self-gravity prevents a blanket uniqueness claim. Heating/cooling
plus hydrostatics gives a conditional flat tail, and linear cooling with
L proportional to Mb yields v^4 proportional to Mb. That cooling law has a
marginal isobaric thermal mode; the coefficient contains independent absorption,
luminosity and cooling constants. The phase-pressure boundary remains unselected.
19 checks pass; the isobaric-sign control fails its intended check. No full
halo attractor or 1/2 derived; see the scoped continuations in the result.

Latest checkpoint (2026-11-06): joint_phase/SHARED_INTERACTION_RESULT.md tests
one explicit baryon-triggered scalar phase coupled to a particle-producing
second scalar. It derives phase stress and mode creation together. The induced
pressure contribution has negative compressibility; the direct exterior force
is not MOND. Identical endpoint masses yield different production for different
transition times (six mode solves per implementation). Original 30 checks pass;
sign control fails two intended checks. A direct nonnegative projection resolves
near-zero cancellation and passes 36 checks; all raw records are retained.
Vacuum offset and couplings remain independent. No material halo inventory,
positive isothermal pressure, or universal 1/2 is derived; full formation and
backreaction remain conditional on unspecified microscopic/state inputs.

Latest checkpoint: joint_phase/BARYON_PHASE_RESULT.md adds baryon-loaded
self-gravitating hydrostatics and a matter-coupled two-vacuum model. Fixed
baryons, dispersion and surface pressure admit different pool inventories
(six solves; 27 checks pass; pressure-sign control fails one intended check).
A declining baryonic density can radially stabilize a phase wall under stated
thin-wall assumptions, but its radius depends on baryonic size, phase splitting
and coupling. Vacuum excess alone is not the attractive material pool. A
conserved-charge inventory law is possible conditionally, with unspecified
particle charges/masses. No universal inventory, phase pressure, or 1/2 has
been derived. See the result for scoped dispositions and deferred prerequisites.

Latest user-authorized follow-up: joint_phase/POOL_PRESSURE_RESULT.md computes
the first mass maximum of a pressure-confined isothermal pool. It gives
cs^4=G^(3/2) Mp sqrt(Pext)/1.18222658849960, with the coefficient computed
from the regular Emden equation. All 12 checks pass; the derivative mutation
fails its intended check. Same-phase vacuum pressure cancels at the interface;
Pext=rho_DE c^2, Mp(Mb), and universal marginality are not derived. The finite
edge coefficient differs from the formal infinite-tail coefficient. Cosmic
tidal confinement with fixed dimensionless boundary data gives v^4 scaling
as Mb^(4/3), not Mb. No half coefficient or full galaxy model is obtained.
This is new authorized work, not a revival of rejected turnaround fits.

Latest user-authorized calculation: joint_phase/EDDY_FORCE_RESULT.md derives
the force on stars from the illustrative canonical vortex, including pressure.
The static source is -2U and its leading far force is outward
2pi G n^2 v0^2/r. A finite-charge vortex also has negative active source
relative to its ambient condensate. Six converged profiles verify the core
virial coefficient;31 checks pass and the density-only control fails its
two intended checks. A separate rho_h=A/r^2 overdensity would yield flat
curves, but its required A(M_b,rho_DE) is not derived. This completed bounded
test follows new user authorization; no previous blocked-turn count applies
to it. The overall coefficient remains unresolved, and no action is adopted.
joint_phase/MATERIAL_POOL_DERIVATION.md derives an attractive flat-curve
tail from isothermal hydrostatic balance, rather than imposing a density
profile: v_flat^2=2c_s^2. Its free dispersion does not supply the required
c_s^4=G M_b c sqrt(G rho_DE)/8. This is an analytic alternative concentration
model, not a numerical fit or a completed unified medium.

Current selection boundary: joint_phase/SELECTION_IMPASSE.md rechecks the
adopted action and microscopic mechanism notes and records three consecutive audits
of a research impasse. No coefficient-selecting physical principle has been
identified. The user has been asked for any additional theory-defining
postulate or source. No process is running; the goal is blocked and
unachieved. This revalidation is not a new successful physics calculation.
Earlier active-status statements below describe their historical checkpoints.

The user has now answered with a flow/pool/eddy analogy, explicitly offered
as examples. joint_phase/FLOW_POSTULATE_TRANSLATION.md records a bounded
field-theory translation: a vacuum background plus vortex excitations is
possible, but a simple illustrative action leaves their scales independent
and does not derive the force on stars. The question is no longer unanswered;
the coefficient-selection gap remains. No candidate or retired carrier is
adopted, and no automatic goal resumption is claimed.

The user requested further constructive work after the previous scoped
audit. The new goal is active. joint_phase/RESULT.md computes the phase
energy and cubic response of an explicit condensed-plus-gapless potential.
Its17 exact checks pass; the deliberate mutation fails its two intended
checks. The next step, joint_phase/SEQUESTER_RESULT.md, applies a named global
vacuum cancellation conditionally and removes the arbitrary offset. Its11
exact checks pass. The residual depends on a scalar history and boundary
term; the homogeneous selector still does not contain the response couplings
B,h. No coefficient or protected criticality is derived. A shared interaction
or symmetry must connect those sectors before more homogeneous history solves
could select the coefficient.

joint_phase/INDUCED_RESULT.md tests a changed shared-condensate gravitational
coupling. It derives stable positive scalar-tensor vacuum conditions, the
curvature-induced quadratic response and a tree-level cancellation option.
Its18 exact checks pass. The joint ratio remains
128pi/[r_B^2 x^2 theta^3(x-1)]; even B=A leaves vacuum and mass-ratio data.
No microscopic selection, protected criticality or full source/clock health
is supplied. joint_phase/MERGER_AUDIT.md now checks the proposed combination
with sequestering: in a pure-induced protected action, a global curvature
constraint disappears and the residual vacuum is not selected by it. A
nonzero bare Einstein term changes the previously derived matching formula.
The separate partial results cannot be combined without new equations.
No justified shared microscopic selector has yet been identified. The goal
remains active; no successful coefficient derivation or complete theory is
claimed.

joint_phase/RG_MATCHING_AUDIT.md checks the actual nodal interacting fixed
point: it does not fix the relevant mass detuning or supply the curved-space
matching, and an anomalous response exponent needs a separate MOND check.
The resulting changed construction in joint_phase/LINEAR_INDUCED_RESULT.md
uses F=D sqrt(sigma^2+p^2). Its16 exact identities pass; the tensor ratio
64pi D^3/(C_A C_B^2) cancels the condensate scale. But m_sigma^2/H^2<4,
so scalar exchange cannot be removed by a short Compton wavelength locally.
An explicit conditional local-source calculation shifts the critical
quadratic coefficient from1 to Q=1+2alpha^2 and the operational ratio by
Q^3. Microscopic generation of the curvature/kinetic operators and this
critical matching identity remain the next obligations. This is partial
progress, not a predicted coefficient or adopted action.

joint_phase/NODAL_CURVATURE_RESULT.md now computes a microscopic candidate
for the linear coupling and amplitude kinetic term: the minimally coupled
parity-even Dirac determinant on intrinsic2+1-dimensional leaves. Its15
exact checks pass. The finite cubic is positive, but the linear curvature
threshold is negative, D=-C_A/(12h^2), and Z_sigma=-2D/sigma. A warped
metric distinguishes the intrinsic curvature operator from Einstein R_4.
A constant bare Einstein term alone does not repair positive stationary
vacuum on the stated critical surface. Allowing normal propagation restores
a quartic-logarithmic deep infrared response, with a possible intermediate
cubic regime and an additional crossover scale. This closes that explicit
microscopic bridge, not other interacting/curved completions. No coefficient
is selected; the positive derivation remains open.

joint_phase/ISOTROPIC_LAYER_AUDIT.md changes the microscopic matter and
embedding rather than repeating the Dirac-only test. A parity pair of
Dirac fields plus one massive vector gives positive finite cubic and
curvature coefficients for 1/2<h_v/h_f<2^(1/3). However, a covariant
coarea-weighted isotropic material-layer action has potential stress
w=-2/3 at held condensate and zero tensor spatial stiffness at two
derivatives. A bare Einstein term restores propagation with an independent
coefficient. This is an analytic self-review, not an executable test run;
full vacuum/operational MOND matching and microscopic inter-layer dynamics
remain unresolved. No numerical coefficient is inferred from the sign repair.

joint_phase/CURVED_BAND_RESULT.md retains the quadratic nodal-band operator
on a curved surface instead of replacing it by intrinsic Dirac leaves.
The flat cubic comes from the nodal neighborhood, while the surface-curvature
coefficient comes from the band endpoint and is analytic in Delta^2 for
positive endpoint gap. Fifteen checks pass, including a discrete sphere
sum convergence ladder; the endpoint-removal mutation fails its three
intended matches. A flat-preserving curvature coupling changes that
coefficient independently. Full metric/source matching and microscopic
selection of geometric couplings remain missing; more sphere radii cannot
resolve them. No positive coefficient derivation is claimed.

## Previous investigation outcome: scoped obstructions established

Original user target: derive the acceleration scale and coefficient from an
action, continuing across failed routes. Original target NOT REACHED.
Kappa=1/2 FITTED. No adopted action or shared campaign record changed.
Base e9a6997b51148461ddeb901c0ccfba06f6af16e9; this directory owns all writes.
The positive derivation remains unresolved. The goal's explicitly allowed
obstruction-and-missing-input outcome is documented in FINAL_AUDIT.md,
including its requirement audit and open research handoff. This is not
completion of the theory or exhaustion of all extensions.

## Executed routes

1. Exact adopted-kernel audit: its homogeneous vacuum and quadratic expansion
   cannot fix a0. Promoting only a0 to an auxiliary field gives no finite
   nonzero-acceleration stationary point. Restricted obstruction, not a
   no-go against added dynamics. DERIVATION.md sections 1-2.
2. General two-clock density portal: for smooth healthy bare k-essence,
   the fixed-p kinetic coefficient becomes negative at large polarization;
   retaining the independent clock preserves that negative direction in
   the fixed-metric local block. Full physical sourced application remains
   conditional on matching and reachable scales. DERIVATION.md section 3.
3. Single-clock density-dependent candidate: cosmological kinetic block
   including finite-sound-speed matter is positive. Unlike the independent
   clock, it has no second clock velocity. Linear health is independent of
   b and cannot select it. SINGLE_CLOCK_RESULT.md. No gradient/full-health
   theorem or physical observational pass.
4. Own-action static radial equations obtained and checked symbolically.
   Density dependence adds N W_N to the lapse source. STATIC_RESULT.md,
   including its important restriction of the formal GR metric benchmark.
5. All four frozen finite-shell BVPs converge at two resolutions; maximum
   scaled profile difference2.27e-7. Not a physical galaxy or cosmic match.
6. Radial kinetic/principal-symbol derivation: positive sampled coefficients
   and subluminal local radial characteristic speed on804 points of those
   backgrounds. See RADIAL_RESULT.md for the exact restricted statement.
7. Finite radial box low modes: initial40/80/160 ladder failed convergence;
   separate160/320/640 refinements pass the same2% line on all four cases,
   with positive reported modes. SPECTRUM_RESULT.md retains the initial
   failure and the fixed-interpolant/conditioning limitations.
8. Normalization: an explicit continuous kernel deformation preserves
   background/quadratic data, global convexity and saturation but changes
   the operational MOND scale to a/(1+e). NORMALIZATION_RESULT.md gives
   the exact scoped nonselection theorem and distinguishes the saturation
   scale from the physical force normalization. No full-health result is
   transferred to the deformed actions.
9. Dynamical scale promotion: the exact two-canonical-scalar FRW solution
   retains its arbitrary initial scale offset even with gravitational
   backreaction. The polarization force has one sign; a regular static
   polarized solution with zero total scalar boundary flux is excluded
   for the specified monotone, potential-free promotion. New potentials
   or nonzero flux are outside the result. DYNAMICAL_SCALE_RESULT.md.
10. Near-saturation obstruction: for every positive b, local static d=0
    states at sufficiently large finite p/(a-p) have Mt>0 but D0<0, hence
    negative formal radial squared speed. SATURATION_RESULT.md gives an
    explicit sufficient threshold and local ODE compatibility argument.
    No physical-source or cutoff-valid instability is claimed. Earlier
    healthy finite shells do not establish global health.

## Evidence at this checkpoint

- evidence/main: exact identities and54 independent40/80-digit fixtures;
  completed. evidence/mutate: omitted clock mixing; expected failed identity.
- evidence/single_clock: exact ADM/Schur calculation and72 fixtures;
  completed. evidence/single_clock_mutate: reversed induced term; expected
  failed positivity. These are diagnostic fixtures, not a parameter fit.
- evidence/static: exact radial identities and metric GR benchmark; completed.
  evidence/static_mutate: omitted portal lapse source; expected failed identity.
- All six v2 manifests validated against current input/output hashes. Every
  negative control failed only its intended assertion; main runs completed.
- Subsequent evidence/shell and evidence/radial completed; radial_mutate
  deliberately fails the omitted-portal lapse identity. evidence/spectrum
  is a genuine failed convergence test, not an expected negative control.
  spectrum_refine and spectrum_second completed with refined-grid passes.
- normalization initially failed an expression-tree equality check;
  NORMALIZATION_ERRATUM.md preserves and explains that implementation issue.
  normalization_corrected passes16 exact identities; normalization_mutate
  deliberately fails the operational-scale check.

## Open positive-derivation research

Carrier obligation: address the near-saturation obstruction before treating
the candidate as globally healthy. A physical/cutoff-valid applicability
test, a dynamically preserved state restriction, or an action modification
is required; more refinement of the healthy shells will not suffice.
Extend the candidate beyond the solved finite shell only with this limit
explicitly retained.
The independent background refinement is now complete: all four radial
box cases pass, with relative changes below1e-6 in the lowest three modes
at640 cells. See BACKGROUND_SENSITIVITY_RESULT.md. Angular modes and/or
cosmological/source matching remain next substantive health obligations.
RADIAL_RESULT.md records the analytic ADM argument for the static momentum
and scalar constraints; a separately coded full covariant stress check is
still absent. V=constant is only a restricted static branch.

Normalization obligation: no present action supplies a principle fixing b.
The CFG894 reopen screen stays in force. Do not mistake the imposed portal
a0^2=b rho for a derivation of b=kappa^2 G. A new symmetry, dynamics or
microscopic matching condition must fix an invariant coefficient; merely
trying further numerical values or linear-health fixtures cannot do that.
The next normalization route must fix the invariant physical combination,
not the name of a parameter. NORMALIZATION_RESULT.md now supplies a globally
convex saturation-preserving deformation and explicitly identifies the
missing response/vacuum matching condition. NORMALIZATION_SOURCES.md checks
three primary sources; none supplies that missing condition. The search
was bounded and is not a proof that no new mechanism can exist.

Not attempted here: cosmological matter gradient/mass spectrum, full Dirac
count, quantum matching, nonlinear X>0 preservation, angular stability,
cosmological matching, publication or observational regrading. Routes remain open rather
than exhausted. All audit provenance here is self-review, not independent.
