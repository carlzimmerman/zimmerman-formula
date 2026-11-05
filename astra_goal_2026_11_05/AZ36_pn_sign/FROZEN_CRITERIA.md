# AZ36 — PN correction signs, lane 5(b)

Freeze before graded computation. Base08f4af4afc; C5's exact ADM action,
V3X's asserted PN remainder and H4's decoupling derivation inspected.
An analytic candidate radial reduction was developed before this freeze;
this is not blind. Kappa = 1/2 FITTED; not theory closed.

## Actual target

Determine whether corrections omitted from V3X's PN quadratic action can
flip physical kinetic/gradient signs on the adopted screened background.
A full PASS requires the constrained covariant quadratic operator, all
physical modes/directions, and the background on which signs are claimed.
A full FAIL requires an admissible on-shell mode with the wrong sign and
appropriate constraint/gauge treatment. Otherwise the full label is
NO VERDICT, even if the exact radial theorem below is established.

## Exact radial route

Use unitary khronon tau=t, areal radius r, spatial metric
h=diag(A²,r²,r²sin²theta), lapse N, radial shift b. Let w=A P^r,
s=(w'+2w/r)/A, Q=1/N. beta=eta=gamma_F=0, xi=1, K=4piG, c=1.
The action density after angular integration (omitting4pi) is

 N A r² [R3+KijKij-Ktrace²]/(4K) + r² w N'
 - N A r² W(Kw) - N A r² F(s)
 + A r² mu² (1-N)²/(2K N).

F(s)=gamma max(s,0)²/2, gamma=K L_star²/2. Work on the open s>0 branch;
do not take a two-sided Hessian at s=0. Matter variations are
E_N^m=-A r² rho_m and E_A^m=N r² p_r; perturbations of independent matter
degrees of freedom are not thereby solved.

Derive R3 and the extrinsic-curvature invariants independently from the
metric. Verify the shift integration-by-parts identity and eliminate b
only where its quadratic coefficient is nonzero. Derive the static
E_N-(A/N)E_A identity, including W, stiffness and K(Q) terms. Test whether
it yields a sign-definite radial kinetic coefficient on s>0, N<=1,
rho_m+p_r>=0. Explicitly treat D=A'+AN'/N=0 as a constraint-degenerate
case, not as an infinite physical kinetic coefficient or ghost.

Derive the high-frequency radial spatial Schur complement with both lapse
and polarization kept until elimination. Compare independent sequential
elimination and inverse-block evaluation. Retain mu², background stiffness
and local lapse/radial metric factors; verify the physical speed is the
coordinate speed multiplied by A²/N². Do not confuse the principal UV sign
with every finite-wavelength eigenvalue.

Known answers: exact Schwarzschild R3=0; P-free/mu-free vacuum gives D=0
and the shift equation constrains A_dot=0; gamma->0 has no leading radial
gradient term; N=A=1 with small gamma*s and negligible mu reproduces the
PN leading c²=gamma*s. All symbolic identities must have residual zero.

MUTATE flips gamma's sign on the positive-divergence branch, with all other
terms unchanged. This must produce a negative radial principal speed in
the declared low-density coefficient domain, while algebraic identities
and GR controls remain valid. It is a changed action, not an on-shell
observable computed by silently reusing a main solution.

## Finite coefficient verification and footings

Canonical a0=9.3603e-11, alt1.1312e-10 m/s², never pooled. L_star at
canonical21.68,24,27pc and alt22.85,24,24.60pc. mu^-1=100kpc is inherited
and illustrative, not newly fitted. Use positive y=|gamma|s at
1e-12,1e-6,1e-3; N=1-2e-6,1-1e-6,1; A=1,1+2e-6; and
z=|gamma|(rho_m+p_r)=0,1e-6,1e-3. These are coefficient-domain checks,
not computed Solar profiles or exact global backgrounds. The theorem,
if proved, supplies its conditions; numerical samples do not prove them.

Evaluate40/80-digit precision pairs and float64. Relative agreement must
be <=1e-30 for the precision pair and <=1e-12 for float64 (nonzero values).
The main sign gate is strict positivity of radial kinetic and gradient
coefficients under the derived hypotheses. No external observational line
is used. SI a0 is used only to report separate dimensionless density scales;
the exact sign theorem must not depend on choosing a footing.

## Scope and continuation

Investigate whether the radial identity suffices for V3X's nonspherical
background. If transverse metric/polarization mixing or angular propagation
remains missing, record the exact unproved block and keep the full label
NO VERDICT. No numerical smallness bound substitutes for this block.
Write derivation, script, both output trees, known answers, precision pairs,
input hashes and README. Single thread, <1GB, minutes, no downloads.
