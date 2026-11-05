# AZC1: separate-foliation cuscuton coupled to v3s

Written before the new script or its numerical results. Base read:
`cc8dbeba67bb280ffbf28596a280606cd4a28ed3`; live shared checkout may advance.
Owner request: find the action from the current research. This is a candidate
test, not adoption. Kappa = 1/2 remains fitted. No cold sector reinstatement.

## Target and changed premise

Keep the v3s khronon tau and spatial covector P. Introduce a distinct scalar
phi>0 with timelike gradient X=-dphi.dphi/2>0 and
P_DE=(b/phi)*sqrt(2X)-m2*phi^2/2, b,m2>0.
Set a0=alpha*phi with alpha^2=kappa^2*G*m2/2. No bare Lambda.
All P projections, its acceleration coupling and switched stiffness still use
tau, never phi. This differs from the same-foliation response in the October
cuscuton report. By psi=log(phi/phi_ref) its isolated DE sector is the known
constant-coefficient cuscuton with exponential potential, not a novel DE model.

## Claims to test before assigning any full gate

A. Derive rho_DE=V and rho_X=0, and a0^2=kappa^2 G rho_DE exactly.
B. With K=4pi G, p=K|P|, W=a0^2/K[-p/a0-log(1-p/a0)], check its Legendre
   relation and static spherical law at fixed phi. This is not a full sourced
   solution and does not grade G1/G2/G4.
C. Derive the homogeneous constraint m2 phi^2=3bH for dotphi<0 and
   H^2-Hc H=rho_b/(3 Mpl^2), Hc=b/(2 Mpl^2), in the zero khronon-charge
   homogeneous branch. Check continuity and positive enthalpy for H>Hc.
   Do not assert an attained regular rolling de Sitter endpoint.
D. Test joint convexity of U=K W-p^2/2 in (p,a0) for 0<p<a0.
   Prove signs analytically, corroborate 65 logarithmic points s in
   [1e-8,1e8] at 80 decimal digits. With a0 linear in phi, add the positive
   potential Hessian and cuscuton spatial term. This only tests a restricted
   static energy block, not full constrained gravity health.
E. Derive rather than hide the chart dependence of the cuscuton velocity
   Hessian when spatial dphi is nonzero; do not infer a uniform DOF count from
   its vanishing on homogeneous backgrounds. If singular, leave G0 open.

Known answers: uncoupled cuscuton energy, CT14 W derivatives, zero-field
limits, fixed-a0 law S, dust continuity in the homogeneous branch.
Negative controls: add +X to P_DE (must break rho=V and zero time Hessian);
replace a0 proportional to phi by phi^2 (must break the slope 1/2);
double the p-a0 Hessian cross term (must break positivity somewhere in the
predeclared range). Controls must exit nonzero on the corresponding invariant.

Exact identities use SymPy simplify==0; numerical identity cross-checks use
80-digit mpmath, absolute/relative residual <=1e-50 away from singular endpoints.
Positivity is strict, no tolerance widening. Both acceleration footings are
reported separately where dimensional conversions are made (9.3603e-11 and
1.1312e-10 m/s^2); no dimensional observational calculation is planned here.

## Gate labels and limitations

G0 remains UNDECIDED unless the full lapse, shift, two-foliation constraints and
their preservation have been derived on FRW and inhomogeneous backgrounds.
No matter-free Hessian is a replacement. A local velocity-Hessian change is a
warning, not by itself a physical DOF count. G1-G4 cannot be inherited merely
by matching a fixed-phi force equation. G5-G7 are not graded by this action
construction and existing v3s failures are not rescued.

No fitting or observational scan. First stage: one core, under 1 GiB, bounded
to 60 seconds per symbolic run, recorded by computation-audit runner. No
downloads, publication, or modifications of prior result files. Save the
candidate action, proof, finite evidence, source applicability, and next
unresolved implication even if health remains open.
