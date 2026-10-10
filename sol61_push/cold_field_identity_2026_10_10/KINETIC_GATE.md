# Isotropic support distinguishes two interpolation kernels

This analytic checkpoint continues from efe91e23b. It gives a necessary phase-space consistency test, not a microscopic identification or a successful halo model. The scale a0 and its coefficient are unchanged throughout. No global novelty claim is made: the isotropic-density identity is standard and already appears in CFG130; the application and the kernel distinction are the useful project result. [Source hashes](kernel_sources.json) match that base commit. A separate agent re-derived the isotropic obstruction and checked the continuous repaired-branch argument; this is a reviewed analytic proof, not a machine-checked certificate.

For an ordinary stationary isotropic distribution f(E) >= 0, with specific orbital energy E = v^2/2 + Phi(r),

\[
\rho(\Phi)=4\pi\sqrt2\int_\Phi^\infty f(E)\sqrt{E-\Phi}\,dE.
\]

A fixed finite upper energy cutoff gives the same argument. As Phi increases, the integration domain shrinks and each nonnegative integrand decreases. Thus rho is nonincreasing in Phi, without needing to differentiate f. When differentiation is valid,

\[
\frac{d\rho}{d\Phi}
=-2\pi\sqrt2\int_\Phi^\infty\frac{f(E)}{\sqrt{E-\Phi}}\,dE\le0.
\]

An attractive spherical gravitational field has Phi'(r) = g(r) > 0. Therefore no such equilibrium can have density increasing outward. This includes nonthermal isotropic distributions and ordinary integrable Bose or Fermi distributions. A coherent condensate must instead be treated with its wave equation.

The exponential interpolation nu(y) = 1/(1-exp(-sqrt(y))) gives, outside point or compact baryons,

\[
\rho_c(r)=\frac{M_b}{4\pi r_M^3}
\frac{q^4}{4\sinh^2(q/2)},\quad q=\frac{r_M}{r},\quad
\frac{d\ln\rho_c}{d\ln r}=-4+q\coth(q/2).
\]

There is a unique q_star between 3 and 4 satisfying q_star coth(q_star/2) = 4. Indeed the derivative of q coth(q/2) has the sign of sinh(q)-q, positive for q > 0; its limiting value at zero is 2. Consequently the density rises outward for r < r_M/q_star. If the baryons lie inside R_b < r_M/q_star, the exterior annulus R_b < r < r_M/q_star already proves the obstruction. No central point-source singularity is required inside that annulus.

For a stable isotropic barotrope with c_s^2 = dp/drho >= 0, a proposed additional outward acceleration must obey

\[
a_{\rm extra}=g+\frac{1}{\rho}\frac{dp}{dr}
=g+\frac{c_s^2}{r}\left[q\coth(q/2)-4\right]\ge g
\]

on the hollow annulus. It must exceed gravity if c_s^2 > 0. This bound does not apply to arbitrary entropy gradients or anisotropic stresses. Anisotropic f(E,L), rotation, vortices, time dependence and coherent gradient stresses remain possible mechanisms to examine; none is selected by this proof.

The kernel distinction is essential. [CFG541's nu_m1](../../campaign_fresh_gravity/CFG541_cold_energy_equations_precise/cfg541.py) and [CFG556's nu_k](../../campaign_fresh_gravity/CFG556_halo_model_matter_power/cfg556_halo_model.py) explicitly use the exponential formula. The obstruction already applies at q = 4, where CFG556's high-acceleration clipping is inactive. By contrast, [CFG4_common](../../campaign_fresh_gravity/CFG4_common.py) imports nu_mono from [FP1](../../real_research/derivation_chain_2026/FP1_static_sector.py), which replaces the derivative of h(y) = y[nu(y)-1] by

\[
h'(y)=\max\left(h'_{\rm exp}(y),\frac{D}{y+Y_P}\right),
\qquad D=0.05H_P>0,
\]

where Y_P is the maximum of h_exp and H_P = h_exp(Y_P). [CFG279](../../campaign_fresh_gravity/CFG279_mightee_published_values/README.md) previously reported the naming distinction. The known force-level difference must not be interpreted as a comparable difference in the derived density, which involves a derivative of the force.

For any spherical point-baryon kernel, direct differentiation gives

\[
\rho_c=\frac{a_0}{2\pi G r}K(y),\qquad K=h-yh',\qquad y=r_M^2/r^2.
\]

For the intended continuous repaired rule at y >= Y_P, h'_exp <= 0 and h' = D/(y+Y_P). Since h(Y_P) >= H_P,

\[
K(Y_P)\ge H_P-D/2>0,\qquad
K'(y)=\frac{Dy}{(y+Y_P)^2}>0.
\]

It follows that K remains positive and

\[
\frac{d\rho_c}{dr}
=-\frac{a_0}{2\pi G r^2}[K+2yK']<0.
\]

Thus this repaired inner branch avoids the exponential kernel's forced hollow. This proof concerns the continuous defining rule, not numerical derivatives of its tabulated interpolation. It establishes a necessary local condition only; it does not prove a globally positive distribution, finite-halo support, stability, formation or agreement with the full data.

The useful next route is to constrain the interpolation by nonnegative phase-space support while keeping the stipulated a0 relation fixed. The current central obstruction forces a choice: retain the exact exponential target and supply a qualifying additional dynamical ingredient, or test an admissible interpolation against the same observations. A small force difference alone cannot decide that choice. Neither branch currently closes the theory.
