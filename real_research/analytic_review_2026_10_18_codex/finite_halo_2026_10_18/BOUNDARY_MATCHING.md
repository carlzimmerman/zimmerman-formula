# Finite core and vacuum matching for the kinetic model

18 October 2026. Claims ZAR-F1 through ZAR-F4. Model and prior derivations: [KINETIC_PARTITION.md](../KINETIC_PARTITION.md). All results below are analytic.

## Force dictionary and exterior matching

Use separately conserved tethered and free masses M_t and M_f, positive G and a0, and fixed baryons. The forces are

\[
a_t=-\frac{G(M_b+M_f)}{r^2}+\frac{G^2M_t^2}{a_0r^4},\qquad
a_f=-\frac{G(M_b+M_t+M_f)}{r^2}.
\]

Here M_b is a point mass unless a smooth enclosed profile M_b(r) is explicitly specified. This is the same deep cubic, zero-stiffness effective model, not the full interpolation or a relativistic action.

Outside all sources put T = M_t,total and F = M_f,total. With potentials zero at infinity,

\[
\Phi_t(r)=-\frac\alpha r+\frac\beta{3r^3},\qquad
\Phi_f(r)=-\frac\gamma r,
\quad
\alpha=G(M_b+F),\quad \beta=\frac{G^2T^2}{a_0},\quad
\gamma=G(M_b+T+F).
\]

They follow by integrating the actual forces, including the repulsive exterior term. Attractive tether force at an outer edge R requires alpha R^2 > beta. Its exterior effective orbital potential has

\[
\frac{d}{dr}\left(\frac{\ell^2}{2r^2}+\Phi_t\right)
=\frac{\alpha r^2-\ell^2r-\beta}{r^4}.
\]

For nonzero tether stock, the algebraic continuation of this exterior effective potential has exactly one positive critical radius, a minimum; that radius need not lie outside the sources. In particular there is no exterior maximum or outer escape barrier, and the escape energy is zero. A compact isotropic population ending at R uses the lower cutoff E_c = Phi(R), not the escape cutoff zero.

## A sharp isotropic law edge is impossible

On the old constant-f law profile M_t = f A r, M_f = (1-f) A r, let

\[
A=\sqrt{a_0M_b/G},\quad V^2=GA,
\quad C_t=GM_b(1-f^2),\quad D_t=(1-f)V^2,
\quad C_f=GM_b,\quad D_f=V^2.
\]

The inward accelerations are C_i/r^2 + D_i/r. Setting P_i(R) = 0 in the Jeans moments gives

\[
\sigma_i^2(r)=\frac{C_i}{3r}+\frac{D_i}{2}
-\left(\frac{C_i}{3R}+\frac{D_i}{2}\right)\frac{r^2}{R^2}.
\]

But an isotropic energy-cutoff distribution has

\[
\psi_i=\Phi_i(R)-\Phi_i(r)
=C_i(1/r-1/R)+D_i\ln(R/r),\qquad
\sigma_i^2=\langle v^2\rangle_i/3\leq\frac23\psi_i.
\]

The displayed Jeans solution instead has sigma_i^2/psi_i -> 1 at the edge. It cannot come from a nonnegative compact isotropic distribution, even though its pressure vanishes there. This refutes the naive truncation, not finite isotropic halos with a taper.

More generally, if rho is asymptotic to c(R-r)^p with p > -1 and the inward force is finite and positive at R, integration of the Jeans equation gives sigma^2/psi -> 1/(p+1). The speed-support bound therefore requires p >= 1/2. For an ordinary energy distribution behaving as F(E_c-E) proportional to (E_c-E)^k, k > -1, direct velocity integration gives rho proportional to psi^(k+3/2), consistent with that condition. A reflecting wall or an ambient pressure changes the boundary problem and introduces a surface stress; neither is used here.

The point baryon also prevents a bounded-density isotropic center. Any nonempty finite energy interval of a nonnegative isotropic distribution contributes at least a constant times sqrt(-Phi) to the density as Phi -> -infinity, giving at least an r^-1/2 cusp in the point-mass potential. A smooth baryon core or angular-momentum exclusion must be an explicit choice.

## An explicit finite circular family with an exact law annulus

Choose 0 < r0 < r1 < r2 < R and 0 < f < 1. Define a smooth monotone step S on the real line by S(x) = 0 for x <= 0, S(x) = 1 for x >= 1, and

\[
S(x)=\frac{e^{-1/x}}{e^{-1/x}+e^{-1/(1-x)}}\quad(0<x<1).
\]

Set the total cold cumulative mass to

\[
M(r)=\begin{cases}
ArS((r-r_0)/(r_1-r_0)),&0\leq r\leq r_1,\\
Ar,&r_1\leq r\leq r_2,\\
Ar_2+A\displaystyle\int_{r_2}^{r}[1-S((s-r_2)/(R-r_2))]ds,&r_2\leq r\leq R,\\
M(R),&r\geq R.
\end{cases}
\]

This smooth profile satisfies M' >= 0, M <= A r, is zero inside r0, equals A r exactly on the chosen annulus, and has a smooth outer density taper. The filling region between r0 and r1 avoids an uncounted shell at the inner boundary. Put M_t = f M and M_f = (1-f) M.

For a controlled physical use of the deep cubic approximation, choose r0 much larger than f r_M, where r_M = M_b/A = sqrt(G M_b/a0); then u_t/a0 <= f r_M/r is small throughout the cold support. The exact mathematical annulus statement refers to this cubic effective model, not the full interpolating law.

Their circular speeds are

\[
v_{ct}^2=\frac{G[M_b+(1-f)M]}r-\frac{G^2f^2M^2}{a_0r^3},\qquad
v_{cf}^2=\frac{G(M_b+M)}r.
\]

Since M <= A r and G A^2/a0 = M_b,

\[
v_{ct}^2\geq\frac G r[(1-f^2)M_b+(1-f)M]>0.
\]

At every populated radius, place the mass on circular orbits with uniformly distributed orbital planes and phases. In local velocity coordinates this is the positive stationary measure

\[
\mathcal F_i(r,v)=\frac{\rho_i(r)}{2\pi v_{ci}(r)}
\delta(v_r)\delta(v_\perp-v_{ci}(r)),\qquad
\rho_i=M_i'/(4\pi r^2).
\]

The velocity volume element is dv_r v_perp dv_perp dtheta, so the measure integrates to rho_i. Circular orbits preserve the radius and speed in the self-consistent stationary potential. The orientation average gives zero mean velocity, sigma_r^2 = 0 and sigma_theta^2 = sigma_phi^2 = v_ci^2/2. Thus there is real tangential kinetic dispersion, but this is a singular distribution with no radial warmth.

The potentials throughout the configuration are

\[
\begin{aligned}
\Phi_t(r)&=-G\int_r^\infty\frac{M_b+(1-f)M(s)}{s^2}ds
+\frac{G^2f^2}{a_0}\int_r^\infty\frac{M(s)^2}{s^4}ds,\\
\Phi_f(r)&=-G\int_r^\infty\frac{M_b+M(s)}{s^2}ds.
\end{aligned}
\]

They and their forces match the exterior expressions smoothly. There is no cold mass at the point singularity and no boundary pressure or reflecting wall. All cold kinetic, baryon interaction, quadratic interaction and cubic interaction energies are finite: their mass support is bounded away from zero, and the exterior field-energy integrands decay as r^-2 and r^-4. The excluded baryon's own point self-energy is an unchanged constant.

Visible tracers on the interior annulus feel GM_b/r^2 + GA/r, so the asymptotic amplitude has V^4 = G M_b a0. The amplitude and fraction were imposed in the construction. [RADIAL_STABILITY.md](RADIAL_STABILITY.md) proves the radial shell stability claim for this same configuration.

## Regular warm isotropic finite populations

For this branch explicitly replace the point baryon by a fixed smooth nonnegative compact baryon density. Take

\[
\mathcal F_i(E)=a_i(E_{ci}-E)_+,
\quad h_i=E_{ci}-\Phi_i,
\quad \rho_i=c_i(h_i)_+^{5/2},
\quad p_i=\frac{2c_i}{7}(h_i)_+^{7/2},
\quad c_i=\frac{16\sqrt2\pi}{15}a_i>0.
\]

These velocity integrals give positive bounded isotropic distributions. Their exact self-consistency system is

\[
\begin{aligned}
M_i'&=4\pi r^2c_i(h_i)_+^{5/2},\\
h_t'&=-G(M_b+M_f)/r^2+G^2M_t^2/(a_0r^4),\\
h_f'&=-G(M_b+M_t+M_f)/r^2.
\end{aligned}
\]

Set M_i(0) = 0 and h_i(0) = H_i > 0. The regular central solution has M_i = O(r^3), h_i' = O(r), with tether correction O(r^2). Finite central density and pressure follow.

For an elementary finite-radius existence regime, let rho_b = rho_B > 0 for 0 <= r <= L, followed by a smooth compact taper. Put B = 4 pi rho_B/3 and beta = (4 pi/3)c_t H_t^(5/2). Choose

\[
\beta^2\leq\frac{a_0B}{2GL},\qquad
H_t<GBL^2/4,\qquad H_f<GBL^2/2.
\]

Starting at the center, bootstrap M_t <= beta r^3 while h_t decreases. For r <= L,

\[
h_t'\leq-GB r+(G^2\beta^2/a_0)r^2\leq-GB r/2,
\qquad h_f'\leq-GB r.
\]

They cross their first zero at simple finite radii

\[
R_t\leq2\sqrt{H_t/(GB)}<L,\qquad
R_f\leq\sqrt{2H_f/(GB)}<L.
\]

These estimates close the bootstrap. At the first tether edge, h_t' < 0 implies G M_t(R_t)^2/a0 < R_t^2[M_b(R_t)+M_f(R_t)]. Provisionally continue with zero tether density and freeze its enclosed mass at M_t(R_t). Beyond this edge, r^2[M_b(r)+M_f(r)] increases, so h_t remains negative and that empty continuation is self-consistent: the phase cannot restart. Its total T is therefore M_t(R_t). The free potential is automatically increasing. Define the potentials by their force integrals with zero value at infinity and set E_ci = Phi_i(R_i). This reconstructs the positive cutoff distributions with the selected central heights.

Density and pressure vanish at each population edge, so there is no surface-stress layer. The two cold radii need not coincide. Outside the baryonic support and both cold radii, the potentials match the vacuum formulas. Near zero the quadratic and cubic field integrands are O(r^4) and O(r^5), and their outer tails are integrable. All counted cold energies are finite. This proves actual warm finite equilibria, rather than only Jeans moments, but the explicit regime is baryon-confined and need not have a dark-dominated law annulus.

The stability bound in [RADIAL_STABILITY.md](RADIAL_STABILITY.md) can be satisfied simultaneously by taking both nonzero c_i small at fixed baryons and heights. This is a controlled existence and stability result for a subset of this effective model, not a calibration to observed galaxies.

## Finite matching with compact central baryons

There is a broader finite-radius construction. Set c_t = 0 and take rho_f = c_f h_+^n with 1 < n <= 3, in particular n = 5/2. For any smooth compact nonnegative baryonic profile and central h(0) = H > 0, the free-only h decreases and must reach zero at finite R0.

Indeed, if h stayed positive forever, a positive limiting value would make M_f grow as r^3 and force h negative. Hence its limit is zero and

\[
h(r)=\int_r^\infty\frac{G[M_b(s)+M_f(s)]}{s^2}ds
\geq GM_f(r)/r.
\]

Then M_f' >= 4 pi c_f G^n r^(2-n) M_f^n. Once M_f > 0, integration of the resulting inequality for M_f^(1-n) contradicts positivity, because the integral of r^(2-n) diverges at infinity for n <= 3. The first zero is simple since h'(R0) < 0.

Put c_t = epsilon cbar_t, M_t = epsilon m_t. The rescaled coupled equations are regular in epsilon and their repulsive term is O(epsilon^2). On a finite interval containing the simple seed edge, continuous dependence preserves finite roots for both populations when epsilon > 0 is sufficiently small. The exterior monotonicity argument above prevents a second occupied region.

A common radius can also be arranged by varying the tether central height X near the free height H. At epsilon = 0, h_t(r) = h_0(r) + X-H, while the free edge is R0. Thus h_t(R_f(X,epsilon)) changes sign with X-H near the seed. Continuity gives a nearby common-zero choice for small epsilon; the derivative with respect to X is one at the seed, giving local uniqueness under the ordinary implicit-function hypotheses. At this common radius R the exact central matching condition is

\[
H-X=\int_0^R\left[\frac{GM_t}{r^2}+\frac{G^2M_t^2}{a_0r^4}\right]dr>0.
\]

This constructs finite warm mixed populations around a compact central source. No stability certificate for an arbitrary such continuation is implied.

## Approximate law annuli with regular isotropic distributions

This existence route does not carry a stability verdict. Use a lowered exponential distribution for a free-only seed,

\[
\mathcal F_H(E)=C e^{-H/\sigma^2}
\left(e^{(E_c-E)/\sigma^2}-1\right)_+,
\quad C=\rho_c/(2\pi\sigma^2)^{3/2},\quad h(0)=H.
\]

For finite H, e^z-1 >= z bounds its density below by a positive H-dependent multiple of h^(5/2) on its occupied region. The finite-radius contradiction in the preceding section applies. If w = Phi-Phi(0), its density tends to rho_c exp(-w/sigma^2) as H tends to infinity. Velocity integration and continuous dependence give convergence to the regular isothermal seed on each fixed finite radial interval.

Outside the compact baryons, define u = 4 pi G rho r^2/sigma^2, v = G(M_b+M_f)/(sigma^2 r), s = ln r. The limiting isothermal system has

\[
\dot u=u(2-v),\qquad\dot v=u-v,
\quad \mathcal L=u-2-2\ln(u/2)+(v-2)^2/2,
\quad \dot{\mathcal L}=-(v-2)^2.
\]

Its sublevels keep u positive and bounded and v bounded. Any limiting invariant trajectory must have v = 2 and then u = 2. Consequently M_f/r tends to 2 sigma^2/G. Set 2 sigma^2/G = A. For any positive tolerance and any prescribed finite logarithmic annulus width, first choose a sufficiently distant annulus in that limiting seed, then finite H large enough to approximate it, then a sufficiently small nonzero tether amplitude by the same finite-root continuation. This gives regular finite mixed populations arbitrarily close to M_c/r = A over that annulus.

For precision, at each fixed finite H hold A_H = C exp(-H/sigma^2) fixed during that continuation. Take F_f(E) = A_H(exp((E_cf-E)/sigma^2)-1)_+ and F_t(E) = epsilon A_H(exp((E_ct-E)/sigma^2)-1)_+, with h_f(0) = H and h_t(0) = X adjusted by the preceding common-radius argument. The corresponding density function is continuously differentiable across its cutoff and behaves as a positive constant times h^(5/2), so the continuation hypotheses apply.

This is approximate, with perturbatively small tether stock. Its amplitude is set through sigma, its concentration can be large, and the dilute stability bound has not been verified for it. It does not establish the arbitrary-f finite isotropic successor of the previous exact family.

## The mixed isothermal profile is a spatial saddle

In the large-radius constant-f regime, baryonic attraction and cubic residual are subleading to the 1/r force from the cold masses. Write q = 1-f, sigma_f^2 = GA/2, sigma_t^2 = q sigma_f^2, and perturb the logarithms of the two r^-2 densities by y_t and y_f. Differentiating their isothermal Jeans equations with respect to s = ln r gives to first order

\[
\boldsymbol y''+\boldsymbol y'
+\begin{pmatrix}0&2\\2f&2q\end{pmatrix}\boldsymbol y=0.
\]

The matrix has eigenvalues 2 and -2f. The composition direction therefore has a positive spatial exponent lambda_plus = (-1+sqrt(1+8f))/2. The mixed asymptote is not an attractor of generic outward core integration. A selected trajectory may reach it, but that matching is an additional obligation. This is a radial shooting statement, not a time-dependent Vlasov instability result.
