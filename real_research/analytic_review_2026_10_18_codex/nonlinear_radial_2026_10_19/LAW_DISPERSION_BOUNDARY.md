# What small nonlinear perturbations preserve

19 October 2026. Claim ZAR-N4 and counterexample ZAR-N5. Assume [the nonlinear stability theorem](NONLINEAR_FLOW.md), and choose its initial neighborhood so sup_t X(f(t)-F) < epsilon. The fixed equilibrium still has exactly its original law, warm dispersion and finite boundary. A disturbed solution need not preserve these pointwise.

## The law and gravitational response remain close

At every radius and time,

\[
|m_i(t,r)|\leq\|f_i(t)-F_i\|_1,\qquad
|m_t(t,r)+m_f(t,r)|\leq\epsilon.
\]

Thus on the original law annulus [r_1,r_2],

\[
|M_t(t,r)+M_f(t,r)-Ar|\leq\epsilon,
\quad |M_t(t,r)-fAr|\leq\epsilon,
\quad |M_f(t,r)-(1-f)Ar|\leq\epsilon.
\]

The force errors follow from the exact model, without linearization:

\[
|a_f(t,r)-a_f^0(r)|\leq G\epsilon/r^2,
\]

\[
|a_t(t,r)-a_t^0(r)|\leq G\epsilon/r^2+
\frac{G^2}{a_0r^4}(2T\epsilon+\epsilon^2),
\qquad T=M_{F_t}(\infty).
\]

These bounds are uniform in time and uniform on the law annulus. They control the enclosed-mass and acceleration law. They do not control density gradients or pointwise shell density. Small radial layers can have large relative density changes at small integrated cost.

The instantaneous force-defined circular-speed squares differ by r times these acceleration errors. For small enough tolerance both forces remain inward on the closed law annulus. This does not impose the old stationary Jeans relation on a moving distribution: its moment equation also contains the time derivative of the radial current.

Exact law preservation for every disturbed solution is false. The radial canonical shear (r,v,L) maps to (r,v+epsilon_1 chi(r),L). It leaves the initial density and centered dispersion exactly unchanged, while giving initial shell current j_i = epsilon_1 chi mu_i. Continuity gives

\[
\partial_t\mu_i(0,r)=-\epsilon_1(\chi\mu_i)'(r).
\]

On the law annulus mu_i is constant, so choosing chi' nonzero changes the exact law immediately. This is consistent with stability: the change can remain uniformly small in the norms just proved.

## Radial pressure and dispersion

Let C_Gamma = 4 pi^2 and define shell moments

\[
\mu_i=C_\Gamma\int f_i\,dv\,dL,\quad
j_i=C_\Gamma\int v f_i\,dv\,dL,\quad
Q_i=C_\Gamma\int v^2 f_i\,dv\,dL,\quad
P_i=Q_i-j_i^2/\mu_i.
\]

Use zero for the quotient at vacuum. P_i is the shell pressure of the centered radial dispersion, so sigma_ri^2 = P_i/mu_i where mu_i > 0. The equilibrium is even in v, hence j_i^0 = 0 and P_i^0 = Q_i^0. The X bound directly gives

\[
\sum_i\int|Q_i(t,r)-Q_i^0(r)|dr\leq\epsilon.
\]

It also controls centered pressure:

\[
\sum_i\int|P_i(t,r)-P_i^0(r)|dr\leq C_F\epsilon.
\]

Here is the needed mean-flow estimate. Suppress species and set alpha_minus = C_Gamma int(F-f)_+ dv dL and beta = C_Gamma int v^2|f-F| dv dL. Let V_F bound the equilibrium radial velocities. If mu >= mu_0/2, decompose f-F into its positive and negative parts to obtain
j^2/mu <= 2 beta + 4 V_F^2 alpha_minus. If mu < mu_0/2, alpha_minus >= mu_0/2 and j^2/mu <= Q <= V_F^2 mu_0+beta <= 2 V_F^2 alpha_minus+beta. Therefore |P-P_0| <= C_F(beta+alpha_minus), proving the integrated bound.

There is no uniform pointwise dispersion lower bound in this stability topology. At an annulus point r_star, choose smooth increasing radial maps A_n equal to identity outside a shrinking window of width w_n, with A_n(r_star) = r_star, A_n'(r_star) = n, and A_n' >= 1-O(1/n). A derivative spike of width O(w_n/n^2), balanced on each side by an O(1/n) deficit over the rest of the window, gives such maps. Their canonical lifts are

\[
T_n(r,v,L)=(A_n(r),v/A_n'(r),L),\qquad f_n=F\circ T_n^{-1}.
\]

At r_star,

\[
\mu_n=\mu_0/n,\qquad \sigma_{r,n}^2=\sigma_{r,0}^2/n^2.
\]

Only a vanishing radial-layer mass is affected and velocities remain bounded, so X(f_n-F) and the energy defect tend to zero. Even exactly equimeasurable perturbations therefore admit arbitrarily small pointwise dispersion.

There is a useful qualitative result for perturbations whose positivity set is connected, including all smooth radial canonical images of F. Each equilibrium positivity set is connected: it is a continuous family of filled orbital tubes around the connected circular curve. A classical characteristic diffeomorphism preserves connectedness. If the L1 bound is smaller than each species' original mass below r_1 and above r_2, occupied points persist on both sides of the law annulus. The connected radial projection then covers every radius in [r_1,r_2]. Smooth positivity supplies an open velocity set there, so mu_i and centered sigma_ri^2 are strictly positive at every such radius and every finite time. Continuity gives a positive minimum on the closed annulus at each fixed time, and on each fixed finite time interval for an individual solution. No positive minimum uniform over all time or all nearby data is supplied.

For general nearby data, connectedness is not assumed: an arbitrarily thin initial vacuum layer is allowed by small X. It is also not implied for a weak or energy closure of canonical images. Only the integrated pressure statement is universal in that class.

## Finite support at finite times and bounded bulk mass

The global characteristic theorem gives, for each individual solution,

\[
r\geq\rho>0,\qquad |v|\leq V_*,\qquad
R_{\rm supp}(t)\leq R_{\rm supp}(0)+V_*t.
\]

Thus every finite-time halo remains compact, avoids the central point and has uniformly bounded particle speeds. The full support is not necessarily confined to one time-independent outer radius. The nonlinear stability bound does give uniform bulk confinement:

\[
\sup_{t\geq0}\sum_i\int_{r>R}f_i(t)d\Gamma<\epsilon.
\]

At every time only an arbitrarily small permitted mass lies outside the original outer radius; the identities of those particles may change. This controls a mass quantile, not one fixed set of particle labels, the outermost particle or the spatial first moment.

## An arbitrarily small smooth perturbation with genuine escape

Uniform boundedness of the entire spatial support is false even for small accessible perturbations with the exact initial density and centered dispersion. Put A_G = G(M_b+T+U), using the unchanged total species masses. Choose a fixed positive velocity V_b large enough, and smooth cutoffs chi_d with 0 <= chi_d <= 1, zero for r <= R-d, equal to one for R-d/3 < r < R, and |partial_r^k chi_d| <= C_k d^(-k). Extend them smoothly to zero beyond R. Apply the canonical shear

\[
T_d(r,v,L)=(r,v+V_b\chi_d(r),L),\qquad f_d=F\circ T_d^{-1}.
\]

It preserves all fixed-L height Casimirs, total masses, initial density, initial boundary R and centered radial dispersion. Its energy defect is exactly

\[
\mathcal H(f_d)-\mathcal H(F)
=\tfrac12V_b^2\sum_i\int\chi_d(r)^2\mu_i^0(r)dr\longrightarrow0.
\]

Also X(f_d-F) tends to zero. In fact f_d tends to F in every fixed Ck norm: F and all derivatives are flat at spatial R; this defeats every inverse power of d from differentiating chi_d. The maps themselves are not small in a uniform displacement norm.

There are occupied circular points at radii approaching R and open positive neighborhoods of them. The equilibrium radial velocities there tend to zero. After the boost, a positive-mass open packet therefore has outward velocity and

\[
e_{\rm out}(0)=v(0)^2/2-A_G/r(0)>e_*>0,
\]

by the fixed choice of V_b and sufficiently small d. Along every outward characteristic the exact lower force bound gives

\[
\frac d{dt}\left(v^2/2-A_G/r\right)
=v(\ddot r+A_G/r^2)\geq0.
\]

Such a particle can never turn: at zero velocity the comparison energy would be negative. Hence v(t) >= sqrt(2e_*), and r(t) >= r(0)+sqrt(2e_*)t tends to infinity. The entire support is unbounded over time although its escaping mass is arbitrarily small and the nonlinear stability theorem remains satisfied.

This refutes uniform outer confinement for the open small-DF perturbation class, including small X, energy and every fixed Ck norm. The counterexample removes a uniform negative initial particle-energy gap. If that stronger support condition is additionally imposed, this escape construction does not apply; the present proof does not establish uniform outer confinement for that narrower class. A negative gap maintained for all later times would suffice, since Phi_i(t,r) >= -A_G/r implies r <= A_G/eta when E_i(t) <= -eta. Initial negativity alone is not conserved in a time-dependent self-consistent potential.
