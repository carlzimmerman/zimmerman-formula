# A smooth distribution with the exact finite halo density

18 October 2026. Claim ZAR-S1. This construction retains the exact density and potentials from [the finite halo](../finite_halo_2026_10_18/BOUNDARY_MATCHING.md), and removes the circular ridge in [the previous warm construction](../warm_radial_2026_10_18/EXACT_WARM_DF.md). All arguments are analytic.

## Target and hypotheses

Fix the same positive point baryon mass M_b, G, a_0, fraction 0 < f < 1, and smooth hollow profile M on Omega = (r_0,R). Its exact law annulus is M = A r on [r_1,r_2], with A = sqrt(a_0 M_b/G), M_t = f M and M_f = (1-f)M. Retain the sufficient core condition r_0 > 2 f^2 r_M/(1-f), r_M = M_b/A, and the parent's controlled deep-cubic regime. The two potentials and their additive constants are fixed throughout this proof.

For either population write mu = M_i', Phi = Phi_i, a = -Phi', and

\[
L_c(r)=r^3\Phi'(r),\quad U(r,L)=\Phi(r)+\frac{L}{2r^2},
\quad E=\frac{v^2}{2}+U(r,L),\quad C=4\pi^2.
\]

Here v is radial velocity and L is squared specific angular momentum; dGamma = C dr dv dL. The parent proves L_c' > 0 globally and a positive lower bound on the closed range [r_0,R]. Every L > 0 has a unique global minimum s(L) = L_c^(-1)(L) of U, with E_c(L) = U(s(L),L) < 0. Put

\[
\omega(s)^2=\frac{L_c'(s)}{s^3}.
\]

On the closed target range, omega and L_c' have positive lower bounds, finite upper bounds and bounded derivatives of every order. The nonzero baryon mass is essential to this statement; a hollow self-generated potential without that central mass is outside this proof.

The specific target uses S(z) = chi(z)/(chi(z)+chi(1-z)), chi(z) = exp(-1/z) for z > 0 and zero otherwise. Before r_1, M = A r S((r-r_0)/(r_1-r_0)); after r_2, mu = A[1-S((r-r_2)/(R-r_2))]. Thus, up to species constants, at distances d from the inner and outer edges,

\[
\mu\asymp d^{-2}e^{-(r_1-r_0)/d}\quad\hbox{(inner)},
\qquad \mu\asymp e^{-(R-r_2)/d}\quad\hbox{(outer)}.
\]

The proof uses these quantitative edge properties. Arbitrary flat densities are not asserted to satisfy its estimates.

## An intrinsic coordinate and the exact density operator

Choose

\[
h(r)=\frac{(r-r_0)^2(R-r)^2}{(R-r_0)^3},\qquad
\frac{dr}{dx}=h(r).
\]

This maps the full real x axis onto Omega. Let u(x) = mu(r(x)). For every nonnegative integer p,

\[
\sup_x\frac{|\partial_x^p u(x)|}{u(x)}<\infty,
\qquad \sup_x|\partial_x^p\log u(x)|<\infty\quad(p\geq1).
\]

Indeed near either edge h is a positive constant times d^2, while log mu is -D/d plus a logarithmic term and a smooth remainder. Repeated h partial_r differentiation leaves these logarithmic derivatives bounded. Moreover u times any finite inverse power of h or d tends to zero with every physical radial derivative.

For s = s(L), y = x(s), define

\[
\sigma(s)=\omega(s)^2h(s)^2,\quad
t=\frac{E-E_c(L)}{\sigma(s)},\quad
F(E,L)=\frac{H(t,y)}{C L_c'(s)\omega(s)h(s)^2Z},
\]

where psi(z) = exp[-1/(1-z)] for z < 1 and zero for z >= 1, and

\[
Z=\int_{\mathbb R^2}\psi((w^2+z^2)/2)\,dw\,dz>0.
\]

Physical states have t >= 0. With v = omega(s)h(s)w and dL = L_c'(s)h(s)dy, the Jacobian gives exactly

\[
\mu_F(r(x))=\mathcal A H(x)
=\frac1Z\int_{\mathbb R^2}
H\left(\frac{w^2}{2}+W(x,y),y\right)dw\,dy,
\]

\[
W(x,y)=\frac{U(r(x),L_c(r(y)))-E_c(L_c(r(y)))}
{\omega(r(y))^2h(r(y))^2}.
\]

This is shell density per dr evaluated at r(x), so the target is u, not h u.

## Uniform orbital geometry

For |x-y| sufficiently small,

\[
W(x,y)=\tfrac12(x-y)^2+(x-y)^3B(x,y),
\]

with every joint intrinsic derivative of B uniformly bounded in that strip. To see this, use U_r(s,L_c(s)) = 0 and U_rr(s,L_c(s)) = omega(s)^2, Taylor-expand in r-s, and use r(x)-r(y) = h(r(y))[(x-y)+O((x-y)^2)]. The latter expansion and all its intrinsic derivatives are uniform because partial_x log h = h'(r) is bounded and the physical derivatives of h, Phi and L_c are bounded. The two factors of h cancel the denominator in W; higher Taylor terms retain nonnegative powers of h.

There are no remote pieces of a sufficiently narrow tube. If m = min_[r0,R] L_c' > 0, then

\[
U(r,L_c(s))-E_c(L_c(s))\geq
\frac{m}{2R^3}(r-s)^2\qquad(r,s\in[r_0,R]).
\]

Also, with H_h = sup |h'|, the radial distance divided by h(s) after an intrinsic displacement of magnitude a is at least (1-exp(-H_h a))/H_h, interpreted as a when H_h = 0. Hence W <= tau sufficiently small implies |x-y| <= C_0 sqrt(tau), uniformly in y. Monotonicity of U away from its global minimum excludes disconnected outer pieces.

Since (s-r_0)/h(s) and (R-s)/h(s) have positive minima, and -E_c is uniformly positive here, one small common delta > 0 ensures all tubes 0 <= t < delta^2 lie inside Omega and below escape. Their occupied velocities are uniformly bounded.

## A local Fourier inverse with a controlled error

Define the harmonic kernel and multiplier

\[
k(z)=\frac1Z\int_{\mathbb R}\psi((w^2+z^2)/2)dw,
\qquad m(\xi)=\int e^{-i\xi z}k(z)dz.
\]

The multiplier is real, even, continuous and m(0) = 1. Choose zeta > 0 with m >= 1/2 for |xi| <= zeta. On circles of period 8 let k_n = 2 pi n/8 and

\[
b_n=\frac{\delta^2}{4+(\delta k_n/\zeta)^2}.
\]

Then b_n <= delta^2/4, |k_n|sqrt(b_n) <= zeta, and sqrt(b_n) times the Japanese bracket of n is uniformly bounded for delta <= delta_0. Choose a translated smooth partition eta_j, j integer, supported in |y-j| < 1, and theta_j equal to one on its support, supported in |y-j| < 2. For a periodic chart function q with Fourier coefficients qhat_n define

\[
R_jq(t,y)=\sum_n\widehat q_n e^{ik_n(y-j)}
\frac{\psi(t/b_n)}{b_n m(k_n\sqrt{b_n})},
\qquad R_\delta q=\sum_j\theta_j R_j(\eta_jq).
\]

The critical mode estimate, uniformly in j,n and delta <= delta_0, is

\[
\mathcal A\left[
\theta_j(y)e^{ik_n(y-j)}\frac{\psi(t/b_n)}{b_n m(k_n\sqrt{b_n})}
\right](x)
=e^{ik_n(x-j)}[\theta_j(x)+e_{j,n}(x)],
\]

\[
\operatorname{supp}e_{j,n}\subset\{|x-j|<3\},\qquad
\sup_x|\partial_x^p e_{j,n}(x)|\leq C_p\sqrt{b_n}
\quad\hbox{for every }p.
\]

For completeness, rescale y = x-sqrt(b_n)z and w = sqrt(b_n)a in the exact integral. Division by b_n cancels its Jacobian. The phase becomes exp(-ik_n sqrt(b_n)z), independent of x, with bounded frequency. The remaining argument is

\[
\frac{a^2}{2}+\frac{W(x,x-\sqrt{b_n}z)}{b_n}
=\frac{a^2+z^2}{2}+O(\sqrt{b_n}),
\]

with all x derivatives of the remainder of this same order, on a common compact (a,z) set. Replace theta_j(x-sqrt(b_n)z) by theta_j(x) and W by its harmonic term. The integral is Z m(k_n sqrt(b_n)) theta_j(x). The smooth, flat cutoff psi and the fundamental theorem of calculus bound the difference and all x derivatives by C_p sqrt(b_n). Uniform localization gives the stated support after shrinking delta_0. This proves the mode estimate.

## The weighted inverse and smoothness

Let chi_j be translated cutoffs equal to one for |x-j| <= 3 and zero for |x-j| >= 4. Define the Banach norms

\[
\|q\|_{X_s}=\sup_j u(j)^{-1}\|\chi_jq\|_{H^s(\mathbb R)}
\qquad(s=0,1,2,\ldots).
\]

Weights u(j) and u(k) are comparable whenever |j-k| is bounded, by the logarithmic-derivative bound. Each output chart meets only finitely many input charts.

The error e_jn has a zero collar on the period-8 circle. Integration by parts in its Fourier coefficients gives

\[
|\widehat e_{j,n}(\ell)|\leq C_N\sqrt{b_n}\langle\ell\rangle^{-N}.
\]

The local matrix for the error has entries ehat_jn(k-n). Since the ratio of H^s weights is at most C_s times the Japanese bracket of k-n to the power s, summing rows and columns gives

\[
\mathcal A R_\delta=I+\mathcal E_\delta,\qquad
\|\mathcal E_\delta\|_{X_s\to X_s}\leq C_s\delta.
\]

Here the leading term is exactly sum_j theta_j eta_j q = q; there is no discarded localization error. Finite overlap and weight comparability give the global estimate from the local row/column sums. For one extra output derivative, use sqrt(b_n) times the Japanese bracket of n bounded, and one extra power of the bracket of k-n. The same sums give

\[
\mathcal E_\delta:X_s\longrightarrow X_{s+1}
\quad\hbox{bounded uniformly for }0<\delta\leq\delta_0.
\]

Initially these identities hold for finite Fourier sums; their estimates extend them to the stated spaces. Choose delta once so the X_5 norm of E_delta is below 1/2. Then I+E_delta is invertible on X_5 by its convergent Neumann series. If e belongs to every X_s, the solution q satisfies q = e-E_delta q, so the one-derivative gain inductively implies q belongs to every X_s. No simultaneous smallness in all Sobolev norms is assumed.

## Exact density with positivity and monotonicity

Start from a broad positive distribution

\[
H_0(t,y)=u(y)\delta^{-2}\psi(t/\delta^2),\qquad
e=u-\mathcal A H_0.
\]

Rescaling y = x-delta z and w = delta a as above, and using the weighted bounds on u, proves ||e||_Xs <= C_s delta for every s. Define

\[
q=(I+\mathcal E_\delta)^{-1}e,\qquad H=H_0+R_\delta q.
\]

Then A H = u exactly, and ||q||_X5 = O(delta). The smoothing bootstrap also gives ||q||_Xs = O_s(delta) for every fixed s.

The correction vanishes for physical t >= delta^2/4. Fourier Cauchy-Schwarz gives the uniform bounds

\[
|R_\delta q(t,y)|\leq C u(y)\delta^{-2}\|q\|_{X_3},\qquad
|\partial_tR_\delta q(t,y)|\leq C u(y)\delta^{-4}\|q\|_{X_5}.
\]

For example b_n^(-m-1) <= C_m delta^(-2m-2) times the Japanese bracket of n to the power 2m+2; absolute coefficient sums are controlled by X_s for s > 2m+5/2. Thus X_3 controls height and X_5 controls the first t derivative. On 0 <= t <= delta^2/4 the baseline satisfies

\[
H_0\geq p_0u\delta^{-2},\qquad
-\partial_tH_0\geq p_1u\delta^{-4},
\]

with fixed p_0,p_1 > 0. Shrinking delta so both O(delta) relative errors are below half these bounds proves H > 0 and H_t < 0 there. For delta^2/4 < t < delta^2 only the baseline remains and the same signs hold. Both vanish smoothly above delta^2. Therefore F is nonnegative and F_E < 0 wherever the physical DF is positive; F_E = 0 at its smooth support boundary.

The correction is signed, but the total distribution is positive. The construction changes the density error without requiring positive residuals at every stage.

For real input data the Fourier coefficients have conjugate symmetry, while b_n and m(k_n sqrt(b_n)) are real and even in n. The reconstructed correction and total distribution are therefore real.

## Removal of the ridge and exact self consistency

All (t,y) derivatives of the correction series converge uniformly locally, with bounds C_mn u(y). Indeed mixed derivatives cost only polynomial powers of the Fourier index, while q belongs to every X_s. This includes t = 0: the accumulating narrow supports do not produce a circular ridge.

To define a smooth function on inaccessible invariant values, multiply H by a nonnegative smooth cutoff equal to one for t >= -1 and zero for t <= -2. The height estimate also holds for negative t because psi is bounded there, while H_0 >= exp(-1) u delta^(-2); hence H remains nonnegative on the lower extension for the same sufficiently small delta. The cutoff does not affect any physical state or its density. Do not set H abruptly to zero at t = 0. Energy monotonicity is asserted on physical states, not on this arbitrary lower extension.

Transforming derivatives back to E,L introduces only finite inverse powers of h and edge distance: L_c', omega and their inverses have bounded physical derivatives. The target's exponential flatness dominates all these factors. F thus extends by zero across L = L_c(r_0), L_c(R) to a bounded C-infinity function of compact invariant support. Its physical phase-space distribution is also C-infinity with compact support, since its orbits remain in the hollow shell and have bounded velocities. In particular its susceptibility and the total integral of -F_E over physical phase space are finite.

These are fixed-delta statements. No bound uniform in delta tending to zero is asserted; the cold circular limit is singular.

Apply the construction separately to the two populations in their fixed target potentials. Their shell densities equal mu_i at every interior radius and vanish outside the exact original shell. Their cumulative masses, total masses, exterior potentials and acceleration laws are therefore exactly the original ones. This is self consistency in the same coupled model, not a tracer approximation or an approximate fit.

## Radial dispersion and the finite boundary

At each interior r, a common open set of eccentric velocities with delta^2/4 < t < delta^2 is occupied by the untouched positive baseline. The intrinsic logarithmic derivatives of u and sigma are bounded. Rescaling this open set as in the baseline density integral gives uniform constants c_1,c_2 > 0 such that

\[
c_1\delta^2\omega(r)^2h(r)^2
\leq\sigma_r^2(r)\leq
c_2\delta^2\omega(r)^2h(r)^2
\qquad(r\in\Omega).
\]

For the lower bound restrict the rescaled variables to a fixed positive-area set where a is bounded away from zero and (a^2+z^2)/2 lies strictly between 1/4 and 1. There the correction is absent, u(y) and sigma(y) are uniformly comparable to their output values, and the positive integral gives shell pressure at least c u(x) sigma(r(x)) delta^2. The upper bound follows from v^2 <= 2 delta^2 sigma(s) on every occupied orbit and the same uniform comparability. Divide by the exact shell density u.

Thus dispersion has a positive lower bound on the closed law annulus and can be made arbitrarily small above. It cools at least as the fourth power of distance at either boundary, consistent with vanishing stress. There is no added wall, mass layer or escaped tail. The preserved law is the density/force/circular-speed law; the previous exact Jeans pressure-gradient correction to dark velocity moments still applies. A particular temperature profile is not selected by this existence theorem.
