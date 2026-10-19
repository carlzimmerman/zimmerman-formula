# Nonlinear energy coercivity for the smooth finite halo

19 October 2026. Claim ZAR-N1. The equilibrium F = (F_t,F_f) is exactly [the bounded smooth halo](../smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md). Its profile, parameters and two forces are not changed. This proof supplies a nonlinear local energy minimum on a class containing all angular-momentum-preserving rearrangements and their weak limits. It does not infer a nonlinear theorem from the linear Hessian alone.

## Fixed equilibrium and conventions

Use radial coordinates (r,v,L), where v is radial velocity, L is squared specific angular momentum, and dGamma = C_Gamma dr dv dL, C_Gamma = 4 pi^2. In inequalities C denotes a finite constant depending on the fixed equilibrium and indicated bounds, not on a sequence index. Choose one fixed padded interval I = [ell,Lambda] strictly inside (0,infinity) containing both equilibrium angular-momentum supports. All states below have L in I. For each species let

\[
E_i^0=\frac{v^2}{2}+\frac{L}{2r^2}+\Phi_i^0(r),\qquad
w_i=-F_{i,E},\qquad W=\max_i\|w_i\|_\infty>0.
\]

Each physical occupied orbit has a unique radial well and is periodic, except for its phase-null circular minimum. The original angular supports are compact positive intervals; their upper energy caps are uniformly negative. The fixed smooth distributions have finite W, and w_i > 0 wherever F_i > 0.

For a perturbed state f put m_i = M_{f_i}-M_{F_i}, and let

\[
X(f-F)=\sum_i\int(1+v^2+L/r^2)|f_i-F_i|d\Gamma.
\]

Write K(f) = (1/2) sum_i int(v^2+L/r^2) f_i dGamma. The conserved Hamiltonian is

\[
\mathcal H(f)=K(f)+\int\Phi_b\,d(M_t+M_f)
-\frac G2\int\frac{(M_t+M_f)^2-M_t^2}{r^2}dr
+\frac{G^2}{3a_0}\int\frac{M_t^3}{r^4}dr,
\quad\Phi_b=-GM_b/r.
\]

Potentials are normalized to zero at infinity. The exact energy identity is

\[
\mathcal H(f)-\mathcal H(F)=D_0(f)
+\tfrac12\int m^TH_0m\,dr
+\frac{G^2}{3a_0}\int\frac{m_t^3}{r^4}dr,
\qquad D_0(f)=\sum_i\int E_i^0(f_i-F_i)d\Gamma,
\]

\[
H_0(r)=\begin{pmatrix}
2G^2M_{F_t}/(a_0r^4)&-G/r^2\\
-G/r^2&-G/r^2
\end{pmatrix}.
\]

The kinetic and baryonic terms are linear; the gravitational term is quadratic and the tether term cubic. Thus the last term is the exact remainder, including when the species total masses differ.

## The inverse entropy and its extension

At each originally occupied L, invert the strictly decreasing equilibrium height relation on E_c(L) <= E < E_cap(L). Let e_i(s,L) be this inverse, s_i,max(L) = F_i(E_c(L),L), and define

\[
\Psi_i(s,L)=-\int_0^s e_i(q,L)dq,
\qquad e_i(0,L)=E_{\rm cap,i}(L).
\]

This is C1 and strongly convex in height, with

\[
\Psi_{i,s}(0,L)=-E_{\rm cap,i}(L)>0,\qquad
\Psi_{i,ss}(s,L)=\frac1{w_i(e_i(s,L),L)}\geq\frac1W.
\]

Above s_i,max extend its height derivative by
Psi_s(s,L) = -E_c(L)+(s-s_i,max)/W. For L in I outside the original angular support use Psi_i(s,L) = -E_ci(L)s+s^2/(2W), where E_ci(L) is the global minimum of the original effective radial potential. These extensions are C1 and strongly convex in height; a jump in the second derivative is harmless. Their height derivatives are uniformly bounded on every fixed bounded height interval, and their slopes at zero have a uniform positive lower bound. No smoothness in L is needed for the conserved height integrals.

Define the nonnegative relative entropy

\[
\widetilde D(f)=\sum_i\int[
\Psi_i(f_i,L)-\Psi_i(F_i,L)+E_i^0(f_i-F_i)]d\Gamma.
\]

Where F_i > 0, Psi_s(F_i,L) = -E_i^0. Where F_i = 0, let ehat_i(L) be the upper cap on the original angular interval and the circular minimum outside it; then E_i^0 >= ehat_i(L). Strong convexity gives

\[
\widetilde D(f)\geq\frac1{2W}\sum_i\|f_i-F_i\|_2^2
+\sum_i\int_{\{F_i=0\}}(E_i^0-\widehat e_i(L))f_i\,d\Gamma.
\]

There is one fixed finite phase box B = {a <= r <= b, |v| <= V, L in I}, containing the original support, such that outside B

\[
E_i^0-\widehat e_i(L)\geq c_B(1+v^2+L/r^2)>0.
\]

The inner bound uses L >= ell and the centrifugal 1/r^2 term dominating the point-baryon 1/r term; the outer bound uses the strictly negative caps, and the velocity bound uses the quadratic kinetic energy. On B, weighted L1 is controlled by L2 on a finite measure set. Therefore

\[
X(f-F)\leq C[\sqrt{\widetilde D(f)}+\widetilde D(f)].
\]

The inverse entropy need not be C2 at zero. No uniform third-order Taylor expansion of Psi is used below.

## A weakly closed constraint class

Write f precedes_L F when, species by species and for almost every L, every nonnegative convex increasing height function G with G(0) = 0 satisfies int G(f(r,v,L)) dr dv <= int G(F(r,v,L)) dr dv. Equivalently it suffices to use (s-alpha)_+ for all alpha >= 0. This fixed-L submajorization class includes exact fixed-L equimeasurability, permits mass loss, and is closed under the weak limits used below. The lemma applies to all nonnegative measurable members with finite mass and kinetic energy, including nonsmooth weak limits; no compact spatial support or smooth rearrangement representation is assumed.

It implies f_i <= s_i,max(L), with f_i = 0 outside the original angular support. Since Psi is an admissible convex function,

\[
\Delta\Psi(f):=\sum_i\int[\Psi_i(f_i,L)-\Psi_i(F_i,L)]d\Gamma\leq0,
\qquad D_0=\widetilde D-\Delta\Psi\geq\widetilde D\geq0.
\]

If G(s,L) is a smooth height test with G(0,L) = 0 and bounded first two height derivatives, choose lambda > 0 so Psi_i plus or minus lambda G is still convex increasing. The uniform lower bounds on Psi_s and Psi_ss allow this. Applying the constraint to both signs gives

\[
|\Delta G(f)|\leq-\Delta\Psi(f)/\lambda\leq D_0(f)/\lambda.
\]

In particular each total species mass deficit is O(D_0), using G(s,L) = s. The tail and L2 estimates above hold with D_0 in place of Dtilde.

## The normalized nonlinear tangent

Suppose f_n precedes_L F and d_n = D_0(f_n) decreases to zero through positive values. Let h_n = (f_n-F)/sqrt(d_n). The global L2 bound gives a weakly convergent subsequence h_n to h. The energy-gap estimate makes its limit zero outside the original occupied set: on each compact subset strictly outside that set the normalized L1 mass is O(sqrt(d_n)); the remaining boundary sets have zero phase volume.

The sharp weighted estimate is

\[
\mathcal A[h]=\sum_i\int h_i^2/w_i\,d\Gamma\leq2.
\]

To prove it without a singular entropy Taylor expansion, use convex duality. For any species-vector smooth test phi compactly supported where 0 < F_i < s_i,max and w_i > 0, the relative entropy dominates
sqrt(d_n) int phi(f_n-F) minus the dual Bregman term at Psi_s(F). On this compact set the dual has second derivative w_i, so that term is (d_n/2) int w_i phi^2 + o(d_n), uniformly. Divide by d_n, use Dtilde <= d_n, pass to the weak limit and take the supremum over phi. Exhaustion of the occupied set yields A[h] <= 2. This also fixes h = 0 at zero weight.

Next expand a bounded-C2 height test G at F. Its remainder is O(||f_n-F||_2^2) = O(d_n). The preceding Casimir bound consequently implies

\[
\sum_i\int G_s(F_i,L)h_i\,d\Gamma=0.
\]

Tests can be species-specific and localized in L. Passing to the limit is legitimate on B by weak L2 convergence and outside B by the O(sqrt(d_n)) normalized L1 tail bound; the test need not be globally L2. Inverting F on compact interior energy-angular-momentum bands allows G_s(F,L) to be any smooth test a(E,L) on those bands. Hence h has zero average on almost every periodic radial orbit.

This is exactly membership in the old dynamically accessible closure, not an extra hypothesis. In orbit-time coordinates, the unperturbed generator is frequency times partial_theta, while w is invariant. Its range -w Dg has annihilator w a(E,L) in L2(1/w). Conversely any zero-average orbit function has a periodic primitive. Truncate away from the circular and support boundaries, truncate its nonzero angle Fourier modes, and approximate smoothly there. The resulting generated perturbations -w Dg converge to h in A. Thus h lies in the closure on which the previous coercive quadratic applies.

## Compactness of the normalized fields and the cubic remainder

Let m_n be the cumulative mass difference for f_n. Choose a < r_0 and b > R. Near zero, the gap controls int(L/r^2)f_n by C d_n, so

\[
0\leq m_{i,n}(r)\leq C d_n r^2\quad(r<a).
\]

For r > b, use the O(d_n) total mass deficit and the O(d_n) outer tail mass to get |m_i,n(r)| <= C d_n. On [a,b], truncate velocity to the fixed box. The normalized shell densities are bounded in L2(dr), so their cumulative integrals are compact in the uniform norm. The discarded normalized tail mass is O(sqrt(d_n)). Weak convergence identifies the limit as the cumulative mass m_h of h. Consequently

\[
\frac1{d_n}\int m_n^TH_0m_n\,dr
\longrightarrow\int m_h^TH_0m_h\,dr.
\]

For the singular weights, the inner normalized quadratic tail is O(d_n), using m_n <= C d_n r^2; the outer tail is also O(d_n). The extra tether diagonal weight vanishes inside the hollow core and decays as r^(-4) outside. This proves the full weighted convergence.

The exact cubic remainder divided by d_n tends to zero. Inner and outer contributions are O(d_n^2). On [a,b], sup|m_n| = O(sqrt(d_n)) by the X estimate, while int m_t,n^2/(d_n r^4) is bounded, giving an O(sqrt(d_n)) contribution. This is the required nonlinear remainder estimate.

## Actual nonlinear coercivity

The [old radial quadratic](../smooth_exact_2026_10_18/CLASSICAL_RADIAL_STABILITY.md) gives, for the accessible limit h,

\[
\mathcal A[h]+\int m_h^TH_0m_h\,dr\geq c\mathcal A[h],
\qquad 0<c\leq1.
\]

Combining all preceding limits with the exact energy identity yields

\[
\liminf_n\frac{\mathcal H(f_n)-\mathcal H(F)}{D_0(f_n)}
\geq1+\tfrac12\int m_h^TH_0m_h\,dr
\geq1-\tfrac{1-c}{2}\mathcal A[h]\geq c.
\]

Therefore there is d_* > 0 such that every state in the fixed-L submajorization class with D_0(f) <= d_* satisfies

\[
\boxed{\mathcal H(f)-\mathcal H(F)\geq\tfrac c2 D_0(f)\geq0.}
\]

At D_0 = 0, the strong entropy bound forces f = F. This local nonlinear minimum, including its weak-limit constraint class and exact remainder control, is the input to [the nonlinear evolution theorem](NONLINEAR_FLOW.md).
