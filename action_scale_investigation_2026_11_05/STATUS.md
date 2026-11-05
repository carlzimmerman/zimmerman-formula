# Active joint-model continuation

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
