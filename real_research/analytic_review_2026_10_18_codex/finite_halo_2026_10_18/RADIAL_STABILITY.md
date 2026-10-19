# Radial energy estimates for finite kinetic halos

18 October 2026. Claims ZAR-S1 and ZAR-S2. These results refer only to the spherical effective energy in [the parent note](../KINETIC_PARTITION.md) and the finite equilibria in [BOUNDARY_MATCHING.md](BOUNDARY_MATCHING.md).

## Circular shell variations

Let mu_i(r) = M_i'(r), and give each baseline shell its circular specific angular momentum ell_i. Keep that angular momentum fixed while displacing its radius to r + epsilon xi_i(r). Smooth bounded C1 displacements must preserve positive radii and the ordering within each population. Different populations may interpenetrate. With fixed baryons, augment the potential energy U by the angular orbital energy,

\[
W=U+\sum_i\int\frac{\ell_i^2}{2r_i^2}dM_i,
\qquad \ell_i^2=-r^3a_i.
\]

The cumulative mass variations are

\[
\delta M_i=-\mu_i\xi_i,\qquad
\delta^2M_i=(\mu_i\xi_i^2)'.
\]

Write the non-baryonic field energy as int F(M_t,M_f,r) dr. Its Hessian entries are

\[
F_{tt}=\frac{2G^2M_t}{a_0r^4},\qquad
F_{tf}=-G/r^2,\qquad F_{ff}=-G/r^2.
\]

After integrating the second mass variation by parts and using circular force balance,

\[
W''=\sum_i\int\mu_i(-a_i'-3a_i/r)\xi_i^2dr
+\sum_{ij}\int F_{ij}\mu_i\mu_j\xi_i\xi_jdr.
\]

The surface term vanishes for smooth compact cold densities and bounded displacements. Differentiate the actual accelerations. The tethered density term -2G^2 M_t mu_t/(a0 r^4) in -a_t'-3a_t/r cancels F_tt mu_t^2. The free self-density term cancels F_ff mu_f^2. The remaining terms yield

\[
\boxed{W''=\int\left[
\mu_t\kappa_t^2\xi_t^2+\mu_f\kappa_f^2\xi_f^2
+\frac{G\mu_t\mu_f}{r^2}(\xi_t-\xi_f)^2\right]dr,}
\]

where for any fixed nonnegative enclosed baryon profile,

\[
\begin{aligned}
\kappa_t^2&=\frac{G(M_b+M_f)}{r^3}+\frac{GM_b'}{r^2}
+\frac{G^2M_t^2}{a_0r^5},\\
\kappa_f^2&=\frac{G(M_b+M_t+M_f)}{r^3}+\frac{GM_b'}{r^2}.
\end{aligned}
\]

For the hollow finite construction with point M_b > 0 and outer radius R, kappa_i^2 >= kappa0^2 = G M_b/R^3. Thus W'' >= kappa0^2 sum int mu_i xi_i^2 dr. Coefficients are bounded on its finite hollow support.

In the Hilbert norm ||xi||_mu^2 = sum int mu_i xi_i^2 dr, this quadratic defines a bounded positive self-adjoint operator. For example its tether component is kappa_t^2 xi_t + G mu_f(xi_t-xi_f)/r^2; the free component has the reciprocal expression. The linear radial evolution is xi_double_dot + L xi = 0 and has the conserved energy

\[
E_{\rm lin}=\tfrac12\|\dot\xi\|_\mu^2+\tfrac12W''[\xi].
\]

It controls both weighted displacement and radial velocity uniformly in time, proving linear Lyapunov stability of coherent angular-momentum-preserving radial shell maps. The positive cross square includes relative displacement of the populations. It does not control displacement derivatives, finite-time shell crossing in nonlinear evolution, or arbitrary warm phase-space perturbations.

## Radial splitting and frozen-orbit checks

A broader positive-second-variation statement is available with an additional core condition. If particles initially at the same radius have displacements with mean xi_bar_i and variance Var(xi_i), the same mass-variation calculation gives

\[
W''=W''_{\rm coherent}[\bar\xi]
+\sum_i\int\mu_i\kappa_{{\rm bg},i}^2\operatorname{Var}(\xi_i)dr,
\qquad
\kappa_{{\rm bg},i}^2=-a_i'-3a_i/r=(\ell_{ci}^2)'/r^3.
\]

The extra coefficients are frozen-background epicyclic frequencies, rather than the collective kappa_i. On the exact law annulus both are positive. On arbitrary steep filling layers the tethered coefficient need not be positive. For the constant-f construction with M <= A r, the sufficient condition

\[
r_0>\frac{2f^2}{1-f}\frac{M_b}{A}
\]

makes it positive throughout the support. Indeed,

\[
(\ell_{ct}^2)'=G[M_b+(1-f)M]+\frac{G^2f^2M^2}{a_0r^2}
+M'\left[G(1-f)r-\frac{2G^2f^2M}{a_0r}\right],
\]

and the bracket is then positive. The free coefficient is positive without this extra restriction. Positive radial velocity perturbation energy can be added as usual.

This proves a positive radial, angular-momentum-preserving second variation including splitting. The general time-dependent Vlasov stability theorem for the singular circular measure is not supplied by that fact. The stated linear Lyapunov theorem above remains attached to its explicit coherent shell evolution.

## The smooth isotropic potential Hessian

For independent enclosed-mass perturbations m_t and m_f, the exact potential Hessian is

\[
\delta^2U=\int\left[
\frac{2G^2M_t}{a_0r^4}m_t^2
-\frac{2G}{r^2}m_tm_f-\frac G{r^2}m_f^2\right]dr.
\]

The pointwise matrix is indefinite: its determinant is -G^2/r^4 - 2G^3 M_t/(a0 r^6) < 0. This does not prove instability, because kinetic phase-space constraints supply another term. It does refute an argument based on the positive cubic term alone.

Let a compact isotropic equilibrium have f_i^0 = F_i(E_i), w_i = -F_i'(E_i) > 0 in its occupied phase space, and chi_i(r) = int w_i d^3v. For radial perturbations h_i initially supported in that occupied region, with each population's total mass conserved, define

\[
\mathcal A[h]=\sum_i\iint\frac{h_i^2}{w_i}\,d^3x\,d^3v,
\qquad Q[h]=\mathcal A[h]+\delta^2U.
\]

The support is invariant under the unperturbed energy flow; the linear forcing vanishes outside it. Weighted Cauchy-Schwarz in velocity yields

\[
\mathcal A[h]\geq\sum_i\int_0^R
\frac{m_i'^2}{4\pi r^2\chi_i}\,dr.
\]

Terms with chi_i = 0 are interpreted by the supported limit m_i' = 0 there. Write m = m_t+m_f and chi = chi_t+chi_f. A second weighted Cauchy-Schwarz gives

\[
m(r)^2\leq\mathcal A[h]\int_0^r4\pi s^2\chi(s)ds.
\]

Since the total perturbation mass vanishes outside R, integration over 0 < r < R gives

\[
G\int_0^R\frac{m(r)^2}{r^2}dr\leq\eta\mathcal A[h],
\qquad \eta=4\pi G\int_0^R\chi(s)(s-s^2/R)ds.
\]

Rewrite the field Hessian as -G int m^2/r^2 + G int m_t^2/r^2 + the positive cubic term. Consequently,

\[
\boxed{\eta<1\quad\Longrightarrow\quad Q[h]\geq(1-\eta)\mathcal A[h].}
\]

This is a sufficient criterion, not a necessary stability boundary.

## Conservation and an attainable smooth stability regime

The linearized kinetic equation gives

\[
\tfrac12\frac{d\mathcal A}{dt}
=-\sum_i\int\delta j_i\cdot\nabla\delta\Phi_i\,d^3x.
\]

Symmetry of the reciprocal potential Hessian and linear continuity give exactly the opposite derivative for delta^2 U/2. Thus Q is conserved. For a regular compact core with bounded susceptibility, as in the constructed cutoff equilibria, the positive field terms are bounded above by a finite constant times A: near zero, M_t = O(r^3) and m_t^2 <= A int_0^r 4 pi s^2 chi_t ds = O(r^3) A. There is no divergent field contribution. Therefore Q <= C A for some finite C, and

\[
\mathcal A[h(t)]\leq\frac C{1-\eta}\mathcal A[h(0)].
\]

For a well-posed linearized flow in this supported weighted space, this is radial linear Lyapunov stability. It is not unrestricted nonlinear stability; nonlinear perturbations can change occupied support and invalidate the fixed susceptibility estimate.

For the finite linear-cutoff DFs in BOUNDARY_MATCHING,

\[
\chi_i=\tfrac52c_i(h_i)_+^{3/2}\leq\tfrac52c_iH_i^{3/2}.
\]

If chi_t+chi_f <= chi_max, then eta <= (2 pi/3)G R^2 chi_max. The baryonic-plateau existence proof bounds R independently of c_i. Both nonzero c_i can therefore be chosen small enough that the existence inequalities and eta < 1 hold simultaneously. This proves finite warm equilibria with an attainable radial linear stability certificate. It does not prove that observed dark-dominated halos belong to that dilute regime.

## An exact diagnostic when the sufficient bound fails

At fixed density perturbation the velocity Cauchy-Schwarz bound is attained by h_i = w_i m_i'/(4 pi r^2 chi_i). Hence positivity of the full radial energy-Casimir Hessian is equivalent to positivity of

\[
\int_0^R\left[
\frac{m_t'^2}{4\pi r^2\chi_t}+\frac{m_f'^2}{4\pi r^2\chi_f}
+\frac{2G^2M_t}{a_0r^4}m_t^2
-\frac{2Gm_tm_f+Gm_f^2}{r^2}\right]dr,
\qquad m_i(0)=m_i(R)=0.
\]

For example a free-only perturbation with integral m_f'^2/(4 pi r^2 chi_f) < G integral m_f^2/r^2 gives a negative energy-Casimir direction. Such a direction defeats this minimization certificate; it does not alone prove a growing Vlasov mode. Failure of eta < 1 is weaker still and establishes neither sign of the exact form.

No three-dimensional extension, physical conversion law, dissipation channel, cosmological formation or general nonlinear stability is implied by either radial result.
