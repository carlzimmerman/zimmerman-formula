# Coordinator reconstruction of the FGF048 uniform-time gates

This check follows reading the author proof and both independently frozen reviewer
routes. It is not a separately blinded root theorem. The full/narrow audits have
separate responsibility and exact scope; no agent count substitutes for proof.
The author's auxiliary constant a0 in (4.1) is denoted a_init here to avoid
confusion with the physical MOND reference normalization.

The decisive structural split is exact: field speeds lambda(z) and sources
H(q,z) depend on the five field coordinates and log density, not on the O(N)
fluid velocity. Fluid speeds (r+s)/2 plus/minus c are linear. Set A=max|r_x,s_x|
and B=max|z_x|. The equations give A<=A0+integral(A²+G B) and
B<=B0+integral[L1 B²+P(B+A/c)]. Thus A<=a N^4 and B<=beta close on
kappa N^-4 with every constant fixed. The exact material identity Dq=-v_x
then confines q to its initial range plus/minus a kappa. This is where uniform
density is actually proved, rather than inferred from separate O(N) bounds for
r and s. Same-point field displacement <=kappa(Lambda beta+F) retains its chart.
The author's explicit minimum for kappa makes all these bootstrap bounds strict.

For the higher norm, a generic all-component cubic estimate would produce an
unhelpful N^8 bound. The proof instead uses zero fluid-speed Hessian and the fact
that field-speed derivatives see only B=O(1). Its two pair-characteristic
Lipschitz inequalities give Htot' <= E N^4 Htot+D N^8. Initial Htot<=h0 N^7
then yields Htot<=(h0+D kappa)exp(E kappa) N^7 on the claimed interval.
The N^8 forcing integrates to N^4 and is bounded by N^7 for N>=1. No classical
second derivative is assigned at the exact polynomial joins.

This is not merely an a priori estimate conditional on a long solution. For
each fixed N the state/first-derivative/higher-norm bounds make U_t and the
weak time derivative of U_x bounded. Hence both have uniform endpoint traces;
spatial integration identifies a C1,1 trace with the correct gradient. The
finite-N characteristic construction restarts at this trace. Its algorithm
requires compatible C1,1 data in the positive chart, not hydrostatic stationarity
of the restart slice. The restart interval may depend on N. This suffices to
exclude an endpoint before the uniform horizon; no common restart length is
silently assumed. Constraints pass by the integrated field identities.

The force bound integrates g_t=p_x with |p_x|<=beta, giving O(N^-4).
For its first derivative, continuity differentiated along fluid trajectories
gives |q_x| <= (|q0_x|+C_H N^7 t)exp(a N^4 t) <= C_q N^3.
The field-only Lipschitz-gradient inequality therefore has source bounded by
D_z N^7, rather than N^8: the quadratic q_x term is only N^6. Consequently
Hz <= (Hz0+D_z N^7 t)exp(E_z t). Integrating the weak derivative of g_t=p_x
yields |g_x-g0_x| <= exp(E_z kappa)[Hz0 t+(D_z/2)N^7 t²], which is O(N^-1)
on the actual proved interval. Continuity upgrades its a.e. spatial bound.
Neither conclusion is a formal initial Taylor expansion or a sharp asymptotic.

Physical units restore t=(L/v0)theta, g=(v0²/L)g_hat and
g_x=(v0²/L²)(g_hat)_X. Thus the author's response coefficients in (8.1)
have the correct units. The physical density normalization and fixed positive
a_ref are never absorbed into an N-dependent coefficient. Both numerical
MOND normalizations are separate fixed backgrounds, not one common vacuum input.

The physical speed bound S_N<=s0 N loses only O(N^-3) spatial width through
the horizon. Its kappa gate retains a fixed core in the regular patch. The
full evolving source is B_x=Cn+tau phi_tt; both negative field fluxes and moving
boundary energy terms remain. Zero initial velocity gives the exact stationary
hydrostatic control on the physical causal domain.

The narrow frozen reviewer gives a stronger O(N^-5) force estimate conditional
on uniform scaled acoustic gradient-Lipschitz bounds. That is not the author's
accepted rate, and this coordinator check does not promote that extra route.
Likewise the full reviewer's independent scaled-coordinate route is evidence
of its own reasoning, not a substitute for auditing the author's physical-block
proof. The impending reconciliation must state their respective scopes.

No upper-time compression theorem follows: kappa is a sufficiently small fixed
constant. Extending these estimates to the larger old fixed-force upper time
is a new implication. This is a classical local diagnostic result; it does not
establish physical stability, a vacuum completion, metric/photon/two-DOF or
observational closure. Zero mathematical executable computations were used.
Mathematical self-proofreading checked units, signs, N powers and qualifiers;
no author or frozen reviewer mathematical text was edited.
