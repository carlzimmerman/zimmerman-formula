# Stability and radial warmth under confinement conditions

19 October 2026. Claim ZAR-C4. Restrict the perturbations of the [proved nonlinear stability theorem](../nonlinear_radial_2026_10_19/NONLINEAR_FLOW.md) by either the outward launch cap in [C1](EXTERIOR_LAUNCH_CRITERION.md) or one of the work budgets in [C2 and C3](BINDING_WORK_AND_CURRENTS.md). These restrictions select solutions of the same equations. They do not introduce a wall, remove a population or alter the equilibrium.

The resulting theorem combines the following statements. Every sufficiently small allowed initial perturbation has a global classical radial evolution, remains uniformly close to F in X for all time, and, provided its stated confinement condition holds, has one time-independent outer enclosing radius. The positive inner radius, distribution height, particle speeds and spatial density remain bounded as before. The enclosing radius can exceed the equilibrium edge R_F; exact preservation of that edge is not asserted.

Outside the enclosing radius the masses equal the conserved totals T,U. The vacuum potentials are therefore the fixed expressions

\[
\Phi_f(r)=-G(M_b+T+U)/r,
\qquad
\Phi_t(r)=-G(M_b+U)/r+G^2T^2/(3a_0r^3).
\]

The finite-time smooth density and potentials match these expressions without a surface layer. Uniform confinement supplies an enclosing vacuum region; it need not make the occupied boundary stationary.

## The density law and pressure estimates survive

On the original law annulus [r_1,r_2], the [previous exact estimates](../nonlinear_radial_2026_10_19/LAW_DISPERSION_BOUNDARY.md) give

\[
|M_t(t,r)+M_f(t,r)-Ar|\le\epsilon,
\quad |M_t(t,r)-fAr|\le\epsilon,
\quad |M_f(t,r)-(1-f)Ar|\le\epsilon.
\]

Force errors and force-defined circular-speed errors remain uniformly small for all time. The confinement certificates add no theorem of exact density-law equality. In the general stability class, continuity shows an immediate law change under a nonconstant radial shear; that example is not asserted to satisfy the new all-time confinement certificates. The inherited conclusion for the restricted class is uniform closeness.

With shell density mu_i, shell current j_i and raw second moment Q_i, let P_i=Q_i-j_i^2/mu_i, zero in vacuum. Then

\[
\sum_i\int|P_i(t,r)-P_i^0(r)|dr\le C_F\epsilon
\qquad(t\ge0).
\tag{25}
\]

For connected smooth positivity sets, including smooth radial canonical images of F, each species' radial dispersion stays strictly positive on the closed law annulus at each finite time. A positive minimum exists on every finite time interval for each individual solution. Neither the new support bound nor the old energy estimate supplies an all-time pointwise lower constant.

## Uniform warmth at any fixed radial resolution

There is nevertheless an all-time positive lower bound for a mass-weighted radial dispersion averaged over any fixed annulus interval J. Put

\[
m_{i,J}(t)=\int_J\mu_i(t,r)dr,\quad
p_{i,J}(t)=\int_JP_i(t,r)dr,\quad
\overline\sigma_{i,J}^2=p_{i,J}/m_{i,J}.
\]

If p_i,J^0>C_F epsilon, then (25) and the mass estimate imply

\[
\boxed{\overline\sigma_{i,J}^2(t)
\ge\frac{p_{i,J}^0-C_F\epsilon}{m_{i,J}^0+\epsilon}>0
\quad(t\ge0).}
\tag{26}
\]

This is also a lower bound for the radial variance computed about the entire bin's mean velocity: that variance contains the nonnegative variance of local mean velocities in addition to p_i,J/m_i,J. Equation (26) requires no pointwise density or derivative control.

More uniformly, fix a resolution d>0 no larger than r_2-r_1. For each species let p_* be the positive minimum of P_i^0 and mu^* the maximum of mu_i^0 on [r_1,r_2]. If C_F epsilon <= p_*d/2, every interval J in the law annulus with length at least d obeys

\[
\overline\sigma_{i,J}^2(t)
\ge\frac{p_*}{2(\mu^*+\epsilon/d)}>0.
\tag{27}
\]

This finite-resolution warmth already follows from nonlinear stability; the confinement hypothesis adds the hard enclosing radius. No radial temperature is set to zero to obtain either statement.

For a separate pointwise sufficient condition, the transported height bound ||f_i||_infinity<=M and finite L width give g_i(v)=C_Gamma int f_i dL<=H=C_Gamma M(Lambda-ell). At fixed shell mass mu_i and mean velocity, filling an interval at height H minimizes the centered second moment, giving

\[
P_i\ge\mu_i^3/(12H^2),\qquad
\sigma_{ri}^2\ge\mu_i^2/(12H^2).
\tag{28}
\]

Thus an additionally established uniform positive shell-density floor would suffice for a pointwise dispersion floor. No such floor has been derived from the present estimates. The thin-layer compression from checkpoint 05 retains compact initial support while making dispersion arbitrarily small at a point, demonstrating the limitation of instantaneous small X plus compact support. That example has not been shown to satisfy the new all-time confinement certificates, so it does not refute an additional theorem for their narrower class. Equation (28) is a sufficient estimate, not a necessity claim about the weakest possible warmth assumption.

The remaining confinement issue is specific: prove one of the all-time launch or work conditions from a nonstationary, verifiable initial-data class of this self-consistent system. It is not resolved by the old Lyapunov norm. All claims here concern the same spherical deep-cubic model and positive angular gap; no nonspherical stability, observational calibration or global novelty result is asserted.
