# Coordinator critical reconstruction of FGF047

This is a coordinator check after reading the final author derivation and both
independently frozen reviewer derivations. It is NOT a separately blinded root
proof, and is not a substitute for the independent full construction audit.
No mathematical executable computation was performed.

The author keeps the actual dynamic source B_x=Cn+tau phi_tt. Define
b=sqrt(B_g/tau), h_g=b and L=h_chi. For the diagonal R equations the two
sources are A+Lw-bLk and A-Lw-bLk. Their difference gives g_t=p_x exactly;
their sum gives p_t=b^2 g_x+A+bL(chi_x-k). The scale pair gives k_t=w_x,
and chi_t=w therefore propagates chi_x=k by a time integral. The phi
integral similarly propagates phi_x=g. The constraints are proved for the
limit; they need not hold for individual frozen-coefficient iterates.

The full reviewer's original off-constraint subtraction was wrong and its
pre-author correction is explicit. The correction agrees with both the author
and the separate compatibility derivation. No accepted original-system identity
uses that superseded expression. The original frozen bytes remain preserved.

The compact initial diagonal image has positive distance to the image of a
primitive box bounded away from g=0 and n=0. A cutoff gives global smooth
coefficient bounds; the same-point estimate |u(t,x)-u0(x)|<delta/2 keeps each
iterate inside the unmodified coefficient region. This avoids assuming the
nonconvex coordinate image contains a componentwise rectangular hull. It also
avoids assuming the evolved positive-g margin from static balance.

For author (23), H/4=H0+K M^3+Q M^2+1. Since T<=1,
H0+T(K M^3+Q M^2)<=H/4. The remaining T(LM+P)H<=H/8,
and exp(2LM T)<=exp(1/4)<4/3. Thus the displayed H/2 bound closes.
The pair-characteristic derivative estimate uses only Lipschitz derivatives,
including the exact polynomial joins. C0 contraction alone is not promoted
to C1: the independently bounded derivative Lipschitz seminorm supplies
|d_x|<=2 sqrt(2H |d|_infinity), and the integrated PDE gives the time derivative.
All constants are normalized first, finite for each fixed N, and no uniform
large-N time power follows from this cutoff construction.

On compatible solutions matter plus interaction contributes +np, the Q field
contributes -np-Tw/C, and the scale field contributes +Tw/C. Both field fluxes
are negative, -(pB+Jwk)/C. Moving-cone flux includes the endpoint energy terms.
For the chosen diagonal off-constraint extension the full residual is
-nv(g-phi_x)+p(B_chi-tau bL)(k-chi_x)/C, exactly vanishing on the propagated
constraint surface. This identity distinguishes that extension from the
baseline primitive off-constraint lift. The hydrostatic zero-velocity control
checks the spatial L terms even when w=0 and chi_x is nonzero.

Initial field accelerations vanish, but this is not a frozen-field theorem.
The optional initial third-time derivative in author Section 8 is not used in
the proof and supplies no uniform-time bound. It cannot establish persistence
of the fixed-force breakdown mechanism. The local physical germ is independent
of auxiliary extensions on common finite-speed domains; the explicit guaranteed
time can depend on the extension.

Accepted scope must remain the regular positive-gradient, fixed-reference,
one-dimensional diagnostic Q model. Separate a0 values and frozen H backgrounds
are parameters, not an evolving-H conservation theorem. Added scale dynamics
is not a physical vacuum reservoir or a metric/two-DOF result. No g=0 crossing,
shock, global stability, RAR/M/filtered-MONO transfer or observation is proved.
