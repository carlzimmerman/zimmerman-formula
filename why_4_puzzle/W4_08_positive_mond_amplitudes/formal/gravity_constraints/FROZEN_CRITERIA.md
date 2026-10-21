# Frozen continuation: physical gravitational constraints and normalization

2026-10-20. Base f1565bc90. Previous goal turn: progress, with committed
clock/flux derivations and exact Lean evidence. The unchanged goal is a
healthy microscopic derivation of xi=1/4 and an end-to-end Lean proof.
Partial algebra or a fitted matter coupling does not complete that goal.

Standing empirical status: kappa=1/2 is FITTED. CFG493 gives
kappa_Lambda=0.417+/-0.095 (rho_DE) and kappa_crit=0.345+/-0.078
(rho_crit), on separate footings. Neither enters the action or algebra.

## Inherited evidence and overlap boundary

Read ../clock_flux/RESULT.md, SOURCES.md and REVIEW.md: the rational
chiral static branch has C2=25g/48, C3=10sqrt(5g tau)/9 and
V0=g^2/(12tau). Its rigid scalar-only ratio is conditional, not the
actual tensor-plus-scalar force ratio. Its simple fixed-metric clock
has a retained tilt instability. Full metric constraints were untested.

The campaign exclusion X17 in
campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_DOORS.md applies.
CFG187_aest_lambda_tie_candidate postulates its normalization tie; it is
not a derivation to rerun. sol61_push/CANONICAL_CLOCK_RESULTS.md already
derives eta=2, the flat lambda>1 scalar reduction and a k^4 repair.
sol61_push/VARIABLE_CLOCK_MODES_RESULTS.md already treats its specified
lambda(q)>1 cosmology. SPHERICAL_CLOCK_CONSTRAINTS_RESULTS.md derives
radial constraints for that action but leaves a matched sourced BVP open.
Do not count repetitions as new results. This continuation instead tests
the specific rational matter model coupled to gravity, the singular
pure-BM lambda=1 corner and a deformation invisible to all homogeneous
quadratic constraints. No reserved p63/KAPPA_LOGIC file is touched.

## Exact model choices and discriminators

1. Covariant rational prototype. Add Einstein-Hilbert M_Pl^2 R/2 and
   real unit-clock action -M nabla_mu u_nu nabla^mu u^nu/2 plus a
   multiplier for u^2=-1 to the previous rational component action.
   M>0 has mass dimension two. This c1-only covariant representative is
   an added bosonic model choice, not a derived supergravity completion.
   Use a consistent Bianchi-I background with phi=pz, u=partial_t,
   h=p/a_parallel and F on the regular finite-gradient branch. Derive
   its lapse constraint and pressures rather than perturbing an
   off-shell Minkowski space with nonzero stress. Test a nonzero-k
   local unstable band and compare it to curvature/drift and an explicit
   validity cutoff. A controlled weak-gravity/WKB result must retain
   its range and cannot certify arbitrary finite coupling.
2. Genuine lapse/shift corner. For pure Blanchet-Marsat gravity use
   S=M_Pl^2/2 int Nsqrt(h)[R3+KijKij-K^2-2f(a)], a_i=D_i lnN,
   f(a)=f0-a^2+2a^3/(3a0)+O(a^4). Work on its actual de Sitter
   background H^2=f0/3, f0>0. Derive both lapse and shift equations,
   retain the redshift of k_phys^2 and all temporal boundaries. Do not
   divide the flat shift equation by lambda-1 at lambda=1, infer gauge
   symmetry from zero speed or transfer the old independent-tilt test.
   Optionally add the specified KT term 2mu^2(1/N-1)^2 and distinguish
   exact condensate vacuum from other cosmological states.
3. Normalization discriminator. Derive actual static G and force
   coefficients of the metric theory. Test
   f_delta(a)=f(a)+[2delta/(3a0)]a^3 exp(-a/L), L>0, delta near0.
   Check whether it preserves f(0), f''(0), the high-acceleration
   constant, the homogeneous vacuum and quadratic constraints while
   changing the leading MOND cubic. This is a nonselection test, not
   a claim that every deformation is fully healthy. An optional fixed
   high-acceleration vacuum reference is an additional hypothesis,
   not something GR itself enforces. Any source-dependent stability
   implication must use the exact primary hypotheses and regime.
4. Actual matter/gravity footing. Specify universal conformal coupling
   S_m[exp(2q phi)g,psi] with background conformal factor one for the
   rational prototype. Derive metric and scalar Newton couplings,
   combined UV G, MOND acceleration normalization, physical metric
   potentials and the independent PPN gamma. Keep actual potential
   density V0 separate from a density inferred from Friedmann using
   a chosen G. No target or measured gamma may determine q upstream.

## Inputs, dimensions, option space and completion conditions

Inputs are symbolic G,c,M_Pl,M,g,tau,q,f0,a0,L,delta and the specified
action functions. Use c=hbar=1 during component calculations and restore
c in a gravitational density interpretation. Footing is rho_DE only.
No measured a0, H0, density ratio, kappa or target coefficient enters an
action or selects an interpolation. No loop is invoked; hbar is absent,
not silently set by a Bekenstein-Hawking quarter. These are density/action
routes, not a de Sitter temperature argument. Pi from Einstein/Gauss
normalization is bookkeeping, not a selecting physical principle.

Write the static Gauss law in n>=2 space dimensions before n=3. For the
single-mediator convention use ../AmplitudeBridge.lean. For combined
tensor and scalar forces derive the dictionary anew; importing the old
conditional xi as an observed prediction is a kill condition.
Four-dimensional chiral identities do not derive a dimension-counting 4.

No model currently gives a determinate normalization. Option class is
free/audit (or lean for formal scope); no kappa number or half-output
is to be registered. A conditional target relation may be used only as
a downstream counterfactual for its independent second observable.
If a true selection equation appears, freeze its option space before
any computation or scan. A fit of q, f0 or an endpoint moment is a trade.

Success still requires retained microscopic/quantum health, actual MOND
and Newtonian forces, same-state positive gravitating vacuum stress,
an independent selecting equation, full formal bridges and a second
physical prediction. The same-action second observable here is the
retained scalar/clock mode or unscreened physical PPN gamma. Cassini's
primary gamma measurement is a downstream test only, never a q input.

## Controls and evidence

Preserve a true rational control and separate False controls for any
new Lean module. Planned mutations: drop the de Sitter redshift boundary
cancellation; assert a0 unchanged after delta=1; treat the combined
tensor/scalar force as the old scalar-only dictionary. A negative band
test must use nonzero k and correct polynomial signs. No failed import
or type error counts as a rejecting physical control. Print critical
types and axioms; no admissions, custom axioms or native_decide.

Commit this file alone before scripts or new Lean source. Sequential
one-core light computation only while the 1024^3 simulation is live;
PID8498 was confirmed live at elapsed02:34:13. Lean uses the existing
read-only pin with -j1 -M1024,30s CPU,45s wall. No scan, download, broad
build, job interruption or reserved-file change. Preserve exact input,
log/object hashes, independent analytic scope reviews and genuine
controls. Register distinct scoped results append-only and regenerate
the campaign ledger. The full goal stays active unless its actual
completion or genuine blocked audit is satisfied.
