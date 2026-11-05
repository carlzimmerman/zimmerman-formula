# NO VERDICT — a complete healthy density-tie action is not established

[Clock repair and solved-background tests](clock_repair/RESULT.md) now evaluates
the corrected gradient bound on all24 original radial models: all16 nonzero-
epsilon cases have positive spline envelopes, with gradient penalty at most
7.35e-6 of the conservative positive part. An explicit bounded-expansion action
candidate and unswitched stiffness pass restricted algebraic tests. Its vacuum
Bianchi-I operator sector has an analytic finite-proper-time continuation proof
and six successful nonlinear collapse checks. General inhomogeneous clock
regularity, full coupled health and the candidate's own galaxy backgrounds
remain unproved; the old backgrounds are not transferred to the new action.

The next constraint/on-shell calculation is in
[constraint_continuation/RESULT.md](constraint_continuation/RESULT.md).
Solving lapse and shift on the scalar-only P=0 FRW branch retains a physical
finite-k clock momentum; zero total charge does not set each mode to zero.
A separate finite-Galerkin convexity proof retains this conclusion with the
actual switched stiffness. The earlier large-s static Schur term includes an
unbalanced scalar force; on a static solution it yields an explicit sufficient
gradient bound, rather than a universal on-shell no-go. Exact checks36/36;
two mutations fail4 and2 intended checks. Full charged-background dynamics,
continuum switch regularity and the known nonlinear clock caustics remain open
obligations. No previous full-health or observational verdict is promoted.

New mixed-block result: MIXED_BLOCK_FINDING.md restores the omitted
algebraic scalar–polarization mixing. The restricted kinetic matrix stays
positive and the nonzero frequency can stay real, yet the Hamiltonian is
indefinite when Omega2-A^2/(D-1)<0. For the potential-only constant-w
branch its large-s coefficient is -a*a_phiphi<0. Imposing zero conserved
clock momentum removes this particular negative-energy direction; whether
that is a physical restriction of the complete action is unproved.
This is a restricted Hamiltonian obstruction, not a full-action no-go or
a demonstrated instability on a solved physical background. Exact main
checks19/19; deleting the gyro mixing fails three checks (16/19).

The constant-w exception to the potential-portal objection is an exact
canonical scalar plus baryonic-dust branch. Its restricted static kinetic
block is positive with the khronon velocity retained. This corrects a gap
in an overly general reading of CT7; it does not establish attraction,
the full coupled spectrum, or an arbitrary-history density tie.
Kappa=1/2 FITTED; not theory closed. No action is adopted here.

Criteria committed first as c8314756b2. Main32/32; exponent mutant21/32,
normalization mutant30/32, kinetic-sign mutant25/32. All runs finish in
under4seconds. Both footings are separately graded, with identical
dimensionless principal-block results. No observational fit is made.

## 1. What the universal identity actually forces

For a canonical scalar, X=-dphi.dphi/2>0 and rho_phi=X+V. Within the
unchanged v3s W(P,a) and an algebraic portal a(X,phi), the identity
a²=kappa²*G*(X+V) on an open set fixes a_X=a/[2(X+V)]. A potential-only
a(phi) cannot satisfy that identity for freely variable X.

In K=4*pi*G=1 units, W=a[-P-a log(1-P/a)]. Holding P fixed while
varying rho gives the scalar velocity coefficient

    K_eff = 1-W_rho-v² W_rhorho
          = 1+eps[h(s)-(1+w)s³/(2(1+s))],
    eps=kappa²/(8*pi), h=2[s-log(1+s)]-s²/(1+s),
    P=a*s/(1+s), v²=(1+w)rho.

This reproduces CT14 from derivatives of W. For every fixed1+w>0,
K_eff/s² tends to -eps*(1+w)/2. The w=-1 known answer removes this
velocity term. At s=108.9 and1+w=.05 the coefficient is-0.9226987783;
at s=10 it is1.038202887. The40/80-digit normalized discrepancy over
the frozen fixtures is2.61018e-40, below1e-30.

This obstructs the specified universal algebraic insertion; it is not a
no-go theorem against every derivative, nonminimal, constrained or
noncanonical extension. Nor is s automatically the screened physical
g/a0: it parametrizes the polarization conjugate W_P/a. A background
solution is needed to locate these coefficients in a galaxy or star.

## 2. Exact special-history escape

Let0<beta<1, w=-beta and

    B=2 Mpl sqrt[3(1-beta)]/(3 beta), y=(phi-phi_star)/B>0,
    V=Vstar sinh(y)^[-2(1-beta)/beta],
    rho_phi=2V/(1+beta), rho_b=rho_phi csch(y)²,
    y_N=(3 beta/2)tanh(y), N=log(scale factor).

Friedmann, canonical stress, separate baryon conservation, scalar
continuity and Klein-Gordon all hold exactly. In particular

    H²=rho_phi coth(y)²/(3 Mpl²),
    H_N/H=-3[1-beta tanh(y)²]/2,
    X=(1-beta)rho_phi/2.

For a²=xi*G*V, the choice xi=2*kappa²/(1+beta) gives the exact density
tie and its slope1/2 on this branch. Independent60-digit differentiation
at the nine frozen beta,y points has largest reported normalized
residual2.48921e-60, below1e-40. Vstar=1 and Mpl=1 in the script are
units, not a determination of the cosmic density scale.

The coupling normalization remains free: kappa²=xi*(1+beta)/2.
Setting xi=kappa² breaks the absolute tie while leaving its logarithmic
slope unchanged. Adding1 to the potential exponent while retaining the
branch breaks Friedmann, scalar continuity, constant w, KG and the tie.
The inherited CT7 failures on its other histories remain untouched.

## 3. Static G0 calculation retaining the clock velocity

For the potential-only portal, no derivative of phi enters W. In the
parallel PN Fourier block at mu_K=0, let D=H_L+gamma*k²>1 and
H_L=(1+s)². The relevant quadratic terms are

    L=-k²Phi²/2+k P Phi-k P sigma_dot-D P²/2
      +phi_dot²/2-v Phi phi_dot.

Differentiating L gives the constraint matrix C and mixed matrix Bc in
FROZEN_CRITERIA. Eliminating Phi and P gives

    K11=1+v² D/[k²(D-1)],
    K12=v/(D-1), K22=k²/(D-1),
    det K=(k²+v²)/(D-1)>0.

Thus this kinetic block is positive for all k>0,D>1 and real v, including
the clock velocity. At v=0 it reduces to diag(1,k²/(D-1)). A direct
40/80-digit matrix elimination on48 frozen coefficient fixtures gives
normalized determinant discrepancy1.65109e-40, below1e-30. This is an
analytic sign result with finite corroboration, not an inference from
a parameter scan. Both footings receive the same check independently.

Flipping phi's bare kinetic sign breaks the canonical formulas, the
zero-v known answer and positivity on both footings. It fails7checks.
Algebraic W_phi, W_Pphi and W_phiphi terms do not enter this velocity
Hessian. They do enter the mass and mixed frequency terms. Consequently
this is only part of G0: it does not certify the full spectrum, mu_K!=0,
nonparallel backgrounds, switch interfaces, or coupled metric effects.
The noncanonical AZC1 two-foliation candidate remains separately unresolved.

## 4. Kappa closure remains in force

CFG894's closure and entry rules were read before work. No numerical
kappa-derivation route was opened: this portal supplies no principle fixing
xi and fails the stated reopen condition. CFG894's length-ratio xi is
not CT7's portal coefficient with the same name. No campaign register or
historical verdict was edited.

Free choices: beta, Vstar, phi_star/field origin, selected branch initial
conditions and baryon normalization, xi (equivalently fitted kappa on
this branch), Lstar, mu_K, the v3s W form and switch. The coefficient
fixtures s,k,gamma,v are diagnostic brackets, not measured backgrounds.
Canonical a0=9.3603e-11 and alt1.1312e-10 are labels for separate footings;
neither is an upstream input to a claimed prediction of kappa.

## 5. Reproduce and inspect failures

From the repository root, run the following command with MODE set to
main, exponent, normalization or kinetic:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 astra_goal_2026_11_05/AZ40_canonical_coupling/run.py --mode MODE

Expected exits are0,1,1,1. Each mode writes its own results.json, listing
every failed check, all numerical rows and input hashes. These are exact
identities and high-precision matrix evaluations; there is no numerical
PDE or time integration requiring a mesh/timestep convergence claim.

The first run used structural matrix equality for the zero-v known
answer and reported a false mismatch between algebraically equal forms.
Its script, output and results remain in structural_equality_failure/.
Replacing that check with exact simplification fixed it; criteria,
equations and tolerances were unchanged, and all four modes were rerun.

## Next decisive calculation

Derive the complete constrained perturbation operator for this potential
portal, including the omitted mass/mixed terms, on a solved cosmological
plus screened background. Check regularity and stability of the selected
constant-w branch under perturbations of its initial conditions, rather
than imposing it in the perturbed equations. Until those checks pass,
there is no verified healthy carrier for a sealed lane8 a0(z) prediction.
