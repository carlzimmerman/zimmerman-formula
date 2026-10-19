# Exact finite density from warm bound orbit packets

18 October 2026. Claim ZAR-W1. Input is the explicit finite profile in [BOUNDARY_MATCHING.md](../finite_halo_2026_10_18/BOUNDARY_MATCHING.md), with its same spherical forces and separately conserved populations. No baryon profile or force law is replaced in this construction.

## Admissible fixed target

Take positive G, a0 and point mass M_b, a fraction 0 < f < 1, A = sqrt(a0 M_b/G), and the prior smooth hollow M with M' > 0 on Omega = (r0,R), M <= A r, and an exact M = A r law annulus [r1,r2] strictly inside Omega. Require

\[
r_0>\frac{2f^2}{1-f}\,r_M,\qquad r_M=M_b/A.
\]

Put M_t = f M, M_f = (1-f) M and mu_i = M_i'. The unchanged forces are

\[
a_t=-G(M_b+M_f)/r^2+G^2M_t^2/(a_0r^4),\qquad
a_f=-G(M_b+M_t+M_f)/r^2.
\]

Use their prior potentials Phi_i, normalized to zero at infinity. Write L = ell^2 for squared specific angular momentum and

\[
L_{ci}(r)=r^3\Phi_i'(r),\quad
U_i(r,L)=\Phi_i(r)+L/(2r^2),\quad
E_i=v_r^2/2+U_i(r,L).
\]

The prior derivative formula and the strict core inequality give L_ci' > 0 throughout the occupied interval. In both empty regions M' = 0 and the derivative is again positive. L_ci increases from zero to infinity on 0 < r < infinity. Thus every L > 0 has a unique global circular minimum at s_i(L) = L_ci^(-1)(L), since

\[
\partial_rU_i=(L_{ci}(r)-L)/r^3.
\]

Its minimum E_ci(L) is negative, its curvature omega_i(s)^2 = L_ci'(s)/s^3 is positive, and sufficiently narrow energy tubes contain only bound orbits close to that minimum. This global minimum is essential; a second remote well would spoil the packet localization.

## Positive invariant packets

Suppress the population index temporarily. The spherical phase volume is

\[
d^3x\,d^3v=C\,dr\,dv_r\,dL,\qquad C=4\pi^2.
\]

Let g >= 0 be smooth with compact support inside Omega. Choose the smooth cutoff

\[
\psi(z)=\begin{cases}e^{-1/(1-z)},&z<1,\\0,&z\geq1.\end{cases}
\]

Only z >= 0 is physically accessible. In that range psi is positive and strictly decreasing until its cutoff; it is deliberately nonzero at z = 0. A bump supported strictly between zero and one would have a rising part and would fail the monotonicity needed for the stability proof.

For epsilon > 0 small enough define

\[
N_\epsilon(s)=\int_0^\infty\!dr\int_{\mathbb R}\!dv_r\,
\psi\left(\frac{v_r^2/2+U(r,L_c(s))-E_c(L_c(s))}
{\epsilon^2\omega(s)^2}\right).
\]

The energy tube can be chosen to remain inside Omega, below escape energy, and within a chosen small neighborhood of its circular center. Define

\[
F_{g,\epsilon}(E,L)=
\frac{g(s(L))}{C L_c'(s(L))N_\epsilon(s(L))}
\psi\left(\frac{E-E_c(L)}{\epsilon^2\omega(s(L))^2}\right).
\]

The prefactor is extended by zero outside the compact center support. This is a smooth nonnegative invariant phase-space packet, with F_E < 0 wherever occupied. Its shell mass density is

\[
T_\epsilon g(r)=C\int F_{g,\epsilon}(E(r,v_r,L),L)\,dv_r\,dL
=\int g(s)K_\epsilon(r,s)ds,
\]

where

\[
K_\epsilon(r,s)=N_\epsilon(s)^{-1}
\int\psi\left(\frac{v_r^2/2+U(r,L_c(s))-E_c(L_c(s))}
{\epsilon^2\omega(s)^2}\right)dv_r.
\]

The kernel is positive and its integral over r is exactly one. Changing variable L = L_c(s) also shows that the packet mass is exactly int g(s)ds.

## The row limit that makes the construction work

Column normalization alone does not imply that T_epsilon approximates the identity. Fix a compact center set inside Omega and expand its unique minima uniformly. With y = (r-s)/epsilon and v_r = epsilon omega(s) w,

\[
\frac{v_r^2/2+U(r,L_c(s))-E_c(L_c(s))}{\epsilon^2\omega(s)^2}
=\tfrac12(w^2+y^2)+O(\epsilon).
\]

All packet support lies in a strip |r-s| <= C0 epsilon. Flatness of psi at its cutoff permits the uniform integral expansion

\[
N_\epsilon(s)=\epsilon^2\omega(s)[Z+O(\epsilon)],
\quad K_\epsilon(r,s)=\epsilon^{-1}k((r-s)/\epsilon)+O(1),
\]

where

\[
Z=2\pi\int_0^1\psi(u)du,\qquad
k(y)=\frac{\int_{\mathbb R}\psi((w^2+y^2)/2)dw}{Z},\qquad
\int k(y)dy=1.
\]

The O(1) kernel error integrates over an O(epsilon) center interval. Hence T_epsilon g converges uniformly to g, including on a fixed compact enlargement containing all sufficiently narrow packet supports; both functions are zero beyond that enlargement. This establishes the needed row limit.

## Positive residual filling

Apply the packet operator separately to each species in its own unchanged target potential. Let u_0 = mu_i, and choose nested compact intervals K_n exhausting Omega, with one K_n containing the entire closed law annulus. For the positive smooth residual u_(n-1), choose a compact smooth cutoff 0 <= theta_n <= 1, with theta_n = 1 on K_n, and set

\[
g_n=\tfrac12\theta_n u_{n-1}.
\]

Choose a compact enlargement J_n inside Omega containing the support of g_n and its sufficiently narrow packets. Its minimum residual m_n = min_Jn u_(n-1) is positive. The row limit allows epsilon_n small enough that

\[
\|T_{\epsilon_n}g_n-g_n\|_\infty\leq m_n/4.
\]

Writing q_n = T_epsilon_n g_n gives

\[
0\leq q_n\leq\tfrac34u_{n-1}\quad\hbox{everywhere},\qquad
q_n\geq\tfrac14u_{n-1}\quad\hbox{on }K_n.
\]

Outside J_n the packet vanishes. Thus u_n = u_(n-1)-q_n remains smooth and strictly positive, and decreases geometrically on every fixed compact interior interval. The residual is bounded by the original smooth density near the edges; it tends to zero everywhere and uniformly. Consequently

\[
F_i(E,L)=\sum_{n=1}^\infty F_{i,g_n,\epsilon_n}(E,L)
\]

has exactly the prescribed mu_i. Tonelli and telescoping give its finite mass,

\[
\int F_i\,d^3x\,d^3v=\sum_n\int g_n(s)ds
=\int\mu_i(r)dr.
\]

This is an ordinary phase-space L1 function, not a circular delta measure. Because both densities are recovered exactly, the prescribed potentials and the response force are exactly self-consistent. Merely broadening the old orbit weights without this density correction would not have that property.

## Radial width and boundary stress

All widths can additionally obey epsilon_n <= epsilon_star 2^(-n), a common bound below escape energy, and any desired small upper limit |v_r| < eta v_ci(r). Tangential departures can also be kept comparably small. Uniform compact radial and angular-momentum bounds give a common finite velocity bound.

The radial pressure of a packet covering a radius is strictly positive there: it contains an open set of velocities with nonzero v_r. A stage covering the whole closed law annulus has a smooth strictly positive pressure on that annulus. Its positive minimum, divided by the target density maximum, gives a strictly positive lower bound on the final sigma_ri^2 there. Radial warmth is therefore finite and genuinely nonzero over that entire interval. Its lower bound is an existence result, not a prescribed or calibrated temperature.

The total radial pressure satisfies p_ri <= Vmax^2 rho_i, so it tends to zero at both smooth density edges. Every orbit remains inside the original cold support. There is no reflecting wall, leaked outer mass, added pressure layer or change to the exterior field.

## Which law is preserved

Exact density preserves the force and its circular-speed law. The warm population's velocity moments obey the stationary radial Jeans identity, in the interior where the packet sum is interpreted weakly if necessary,

\[
\langle v_\perp^2\rangle_i=v_{ci}^2+2\sigma_{ri}^2+
\frac r{\rho_i}\frac{d(\rho_i\sigma_{ri}^2)}{dr}.
\]

On the law annulus rho_i is proportional to r^(-2), so the identity reduces to

\[
\langle v_\perp^2\rangle_i=v_{ci}^2+r\frac{d\sigma_{ri}^2}{dr}.
\]

This first-derivative identity can in fact be read classically inside Omega. For each smooth packet, Jeans gives |p_rn'| <= C rho_n with a common C, because r is bounded away from zero and all forces and occupied velocities are bounded. Uniform convergence of the residual shell density bounds both the pressure tails and their derivative tails uniformly. Therefore total radial pressure is C1, despite the possible singular phase-space ridge. The total tangential second moment is continuous by the same uniform moment-tail bound.

Thus the construction does not assert that every dark velocity moment equals the old circular speed. A constant radial dispersion on that annulus would give that equality, but the positive residual construction does not prescribe the dispersion profile. Its exact preserved statement concerns density and acceleration; simultaneous prescription of a nonzero temperature profile is an additional moment problem.

## Regularity and weak stationarity

Since omega is bounded on the closed finite radial range and widths tend to zero geometrically, only finitely many packets contribute near any accessible point E > E_ci(L). There the sum is smooth, and its energy derivative is strictly negative wherever occupied. On the circular ridge E = E_ci(L), the sum may become unbounded. That ridge has zero phase volume, and assigning it a value changes no density or moment.

Each packet is invariant under the same Hamiltonian flow. Passing the stationary transport identity through the L1 sum against compact smooth tests proves weak stationarity of the total distribution. The common velocity bound gives finite kinetic moments and finite total energy with the unchanged field terms.

The ridge qualification cannot be discarded: chi_i = int(-F_i,E)d^3v need not be finite, and a formal derivative of F_i under a canonical displacement need not be an ordinary L1 function. [ACCESSIBLE_STABILITY.md](ACCESSIBLE_STABILITY.md) defines and controls the corresponding energy-space perturbations without assuming finite chi. A bounded smooth distribution across the ridge and a classical differentiable Vlasov theorem remain separate open obligations.
