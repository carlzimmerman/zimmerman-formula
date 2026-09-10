# Healthy matching and an action-level extension

**Full theory OPEN. No healthy complete candidate, empirical fit or novel
law of nature is certified.** The new constructive input is a varied DHOST
radial action with an independent A3 function, alongside a kinetic-block
check. It is not a transplant of the old KGB health verdict.

## First attempted repair: shared metric pressure

Keep the previous F(X),P(X),G(X) action and global a0=1; replace the imposed
metric target by B=B_log*(1+eta*(r*y)^2), with one shared constant eta.
For fixed finite eta this preserves leading weak-field no-slip, not exact
finite-field logarithmic no-slip. No PPN or baryonic source solution follows.
Eleven continuation values, 0 and +/-{1,10,100,1000,5000}, all match the
seven actual action conditions within 7e-11 in an independent 40-digit
reference. All retain an angular gradient instability. At eta=5000 the
angular speeds-squared are approximately -0.1014694 and -0.1002524.
This is one branch, not an exclusion of the enlarged geometry family.

## Constant-F route: fewer wasted searches

The exact reconstructed scalar principal is independent of positive constant
F and scales as 1/X under clock normalization. Thus those two normalizations
cannot repair health signs. An independently derived geometric angular filter
is in constant_sector/REPORT.md. The bounded 24-point study contains 18
regular points, none healthy; no whole-sector no-go is claimed.

## New constructive action input

The proposed extension, in X=-(grad phi)^2/2 convention, is

    L = sqrt(-g)[F(X) R + P(X) - G(X) box(phi)
                 + D(X) L3 + A4(X) L4 + A5(X) L5] + L_m[g],

with coefficients and literature attribution in SOURCE.md. The previous
derivative-conformal KGB model is D=0. At D!=0 the old Einstein-frame KGB
principal is NOT valid; a new coupled reduction is required. No particles,
halo-specific a0, or additional independent clock have been introduced.
The fitted kappa=1/2 vacuum relation remains input, not derived.

For ds²=-N²dt²+Bdr²+r²dOmega², phi=q t+psi(r), p=psi', z=X',
the quadratic invariants on the auxiliary constraint surface reduce to

    box(phi)=[p'+(N'/N-B'/(2B)+2/r)p]/B,
    L3=-box(phi)*p*z/B, L4=z²/B, L5=p²z²/B².

radial_action.py constructs a first-derivative radial density, including
lambda*(X-q²/(2N²)+p²/(2B)), and actually differentiates it to obtain the
N,B,X,lambda Euler-Lagrange equations and conserved scalar current. It checks
the exact Einstein-Hilbert boundary term and the constant-F KGB current limit.
radial_equations.json contains the explicit resulting equations.

These are necessary gauge-reduced equations. Fixing the radial gauge and
dropping the metric shift before variation does NOT supply the omitted
off-diagonal/angular equations. The auxiliary rewrite must be used with its
constraint; it is not a proved DOF count. The independent unitary kinetic
analysis in dhost_kinetic/ similarly supplies a primary kinetic relation,
not the full temporal Dirac chain or positive scalar energy.

## Next calculation

An exact simplification is available: set D=-F_X/X on X>0. Then
A4=F_X/X, A5=0, and both the unitary trace/clock mixing and acceleration
coefficients vanish. The curvature-sector ADM density becomes
F(X)[R3+Kij Kij-K²], up to its boundary term. This is the known luminal
beyond-Horndeski subbranch (source equation (8) and following text), not a
new discovery or an assertion of healthy MOND. COMMANDS.json records the
symbolic substitution check. It is a concrete simpler input for the next
full variation, while the generic D action is retained.

Use the full metric variation (retain a radial shift and sphere-radius field)
to complete the static system for D!=0, then derive its coupled scalar
principal. Search shared F,P,G,D against the fixed exponential source law and
lensing while enforcing that new principal's health. Any candidate still
needs common baryonic interiors/clock boundary data, nonlinear constraint
closure, zero-mode limits, matter Ward identity, full PPN, GW and FLRW/CMB
checks. The kinetic Lean certificate does not certify these missing results.

run_001 records exact commands, outputs, exit statuses and pinned inputs.
Passing execution means the recorded calculations ran, never that gravity
closure has been achieved. No percentage of all possible theories is reported.

Final suite: 18 new unit tests, 7 existing reference regressions, and 4 Lean
lemmas pass. All 12 recorded executable cases exit 0; both manifests validate.
The Lean axioms are propext, Classical.choice and Quot.sound; no sorryAx.
The radial current uses the negative of the earlier KGB current convention,
which leaves its conservation equation unchanged. A test caught and corrected
an initially missing action-function chain rule in the auxiliary X variation;
the final equations include it. This is a code correction, not new physics.
