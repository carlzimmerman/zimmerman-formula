# AZ38 — realistic solar interior, lane 5(d)

Freeze before graded calculation. Basec1d8e06951. V3X's uniform-density
hedgehog estimate inspected. Filename searches, including ignored files in
_external_data, have not located an authenticated solar-interior table.
No data file was downloaded. Kappa = 1/2 FITTED; not theory closed.

## Full target and missing input

Replace the uniform-density Sun by an authenticated stellar structure
profile and calculate its v3s response/health with the relevant constraints
and convergence. PASS requires the actual profile, provenance, density/
pressure consistency, a converged framework-native calculation and scoped
health gates. A physical FAIL needs an admissible profile and a verified
failed gate. If the necessary data are absent, label NOT EVALUABLE and
record the exact acquisition need; do not call an analytic surrogate a
realistic Sun or a nonlinear-interior solution.

The official source inspected is https://phys.au.dk/~jcd/solar_models/ .
It offers Model S structure variables and a corrected GONG l5bi.d.15
product; its original GONG Ledoux discriminant had a documented issue.
Record this source, product and unknown transfer size in NEEDS_OWNER.

## Authorized local calculation

Derive the leading screened interior relation used by V3X:
K s=-2 Phi_N/L_star², gamma=K L_star²/2, hence c_s²=-Phi_N where s>0.
For spherical nonnegative density,

 -Phi_N(r)=G[M(<r)/r + integral_r^R 4pi rho(q)q dq],

with the regular r0 limit. This is positive for nonzero positive mass.
It is a leading screened estimate, not the full covariant constrained
interior operator; do not certify the approximation's error without data.

Implement this radial Green integral at256 and512 intervals for two exact
fixtures on x=r/R: uniform w(x)=3 and manufactured nonuniform
w(x)=C(1-x²)^3, with integral_0^1 w x² dx=1 fixing C. Here
w=4pi R³rho/M. Derive exact cumulative mass and potential symbolically.
Uniform known answer U=(3-x²)/2, U=-Phi_N/(GM/R). The manufactured profile
is an engine test only, never a measured/calibrated solar model.

Use composite trapezoidal integration and interpolate the fine result onto
coarse nodes. Require maximum absolute potential error and coarse/fine
change <=1e-4 in units GM/R, and mass-integral error <=1e-4. These are
numerical engine checks, not observational acceptance lines. The exact
solutions make both failures and passes independently checkable.

Both footings a0=9.3603e-11 and1.1312e-10 m/s²; L_star endpoints/center
21.68,24,27pc canonical and22.85,24,24.60pc alt. Use GM_sun=1.32712440018e20
SI, R_sun=6.957e8m. Report separately the computed c_s² and the a0-dependent
dimensionless s normalization. Do not pool footings merely because the
leading physical speed is a0-independent. L_star and kappa remain FITTED.

MUTATE reverses the manufactured density sign before integration. It must
fail nonnegative density, positive mass and strict positive stiff-branch
speed. Apply the actual switch: negative s has zero stiff contribution,
not an invented negative c_s². Its signed exact integral remains a valid
numerical known answer and should still pass convergence checks. Uniform
positive-density known answers remain unchanged in both runs.

## Inventory and completion status

Record a rerunnable local filename inventory including ignored data, the
patterns and any candidate matches. A filename search is not a proof that
no unnamed table exists anywhere; report only that no authenticated model
was located. Exclude this lane's own fixtures from candidate discovery.
If a candidate appears, inspect provenance before assigning it as data.
No download, browsing of the model data payload, deposited-paper edit or
other external action. Single thread, <1GB, minutes. Save separate main/
mutant outputs, exact derivation, convergence and input hashes. Then move
to the next lane with the realistic-data verdict still NOT EVALUABLE.
