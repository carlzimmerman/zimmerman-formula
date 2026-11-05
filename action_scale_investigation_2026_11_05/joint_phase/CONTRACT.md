# Joint condensed/gapless spectral-parent feasibility calculation

New user continuation after the previous scoped audit. Base repository
checkpoint7b575ab97064d558000c62c4840112499e69e407; only this investigation's
paths may be written. The new positive-derivation goal remains open.

Changed construction: CFG900 used one nodal spectrum whose universal vacuum
vanishes at zero polarization. Here one sector has a dynamical amplitude
sigma while another remains gapless at p=0. Compute a phase energy difference
and the force coefficient from the same explicitly specified potential.
This is a new conditional mean-field construction, not an established UV
theory, not an adoption, and not a new numerical kappa candidate.

Spectra in a preferred frame, transverse cone momentum q:

    E_A^2=q^2+sigma^2+h^2 p^2,
    E_B^2=q^2+h^2 p^2.

The two transverse momentum directions yield, after constant and quadratic
subtractions, positive cubic terms A R^3/3 and B(hp)^3/3. A,B,t,h>0 are
independent symbolic parameters; p>=0 and R=sqrt(sigma^2+h^2p^2). No target
coefficient, empirical acceleration or vacuum energy is an upstream input.
Use the explicit renormalized potential

    U=U0-t(sigma^2+h^2p^2)/2+A(sigma^2+h^2p^2)^(3/2)/3
        +B h^3 p^3/3+delta p^2/2.

Keep U0 and delta free. The radial quadratic is a premise, not a proved
symmetry of both sectors; the gapless B sector distinguishes p from sigma.
delta=0 is a conditional critical slice, not protected by this construction.
No cosmological equation of state is inferred from a flat-space potential.

At fixed p eliminate sigma on the nonzero-amplitude branch. Derive its
domain, radial curvature, reduced potential and endpoint. Then use the
explicit leading static polarization coupling

    L=-|grad Phi|^2/(2K)+p_vector.grad Phi/K-p^2/(2K)-U_eff(p)
      -rho_b Phi, K=4pi G

with p_vector parallel to grad Phi on the attractive spherical branch.
Derive g_N=g-p and g=p+K U_eff'(p), and obtain the deep response only when
delta=0. Do not suppress the infrared change at delta!=0 or the high-field
branch above the amplitude endpoint. Calculate both stationary vacuum
energy U_cond and its difference from U(0,0). A phase energy difference is
not automatically the gravitating dark-energy density.

General-dimension screen: a codimension nu cone gives a nonanalytic
power nu+1 (logarithmic at the relevant even powers); cubic response here
uses nu=2. This is not a dimension-independent coefficient derivation.
c=hbar=1 conventions do not remove their eventual restoration obligations.
The construction does not pass campaign S6: absolute U0 is not fixed by a
named symmetry/dynamics. Accordingly no numerical kappa search, campaign
hit, register trial or exact-coefficient claim is launched. This calculation
tests whether the changed joint mechanism supplies those missing inputs.

Frozen exact checks: subtracted cone integral; amplitude stationarity and
curvature; reduced energy and phase difference; scalar force elimination;
critical versus noncritical IR response; force/energy matching and free
parameter sensitivity; continuity at the amplitude endpoint. Mutation
discards delta from the force equation and must fail the exact derivative
and noncritical infrared comparisons. Symbolic algebra only, one thread.
No physical halo, covariant completion, health theorem, or novelty claim.
