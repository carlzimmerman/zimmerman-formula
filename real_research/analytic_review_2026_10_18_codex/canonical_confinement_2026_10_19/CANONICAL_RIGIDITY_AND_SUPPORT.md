# Canonical rigidity and the original support boundary

19 October 2026. Claims ZAR-Q1 through ZAR-Q3. The class here is strictly radial. Write K_i=supp F_i for the original full phase-space supports. Initial data are f_i0=F_i composed with T_i0 inverse, where each T_i0 is symplectic in (r,v) at fixed L and maps K_i onto itself. This is stronger than retaining just the initial spatial radii. It includes nonstationary smooth data, as constructed below. A fixed initial negative gap does not imply conservation of individual energy.

## The initial gap follows from smallness and unchanged support

Let T,U be the unchanged species masses, c=G^2/a_0, and let r_0>0 be the original inner radius. The original occupied energies satisfy E_i^F<=-beta_0<0 on K_i. Put D=sum_i ||f_i0-F_i||_1. Since both tethered cumulative masses lie between zero and T, the exact potential formulas give, for r>=r_0,

\[
|\Phi_f[f_0]-\Phi_f^F|\le GD/r_0,
\qquad
|\Phi_t[f_0]-\Phi_t^F|
\le \left(\frac G{r_0}+\frac{2cT}{3r_0^3}\right)D.
\tag{1}
\]

The cubic estimate uses |M_t^2-(M_t^F)^2|<=2T|M_t-M_t^F|. Define C_gap=G/r_0+2cT/(3r_0^3). If D<=beta_0/(2C_gap), every initial occupied point belongs to K_i and has actual energy

\[
E_i[f_0]\le-\beta_0/2.
\tag{2}
\]

Thus the fixed initial gap is automatic for sufficiently small data in this unchanged-support class. The unproved issue is its later propagation.

## Density invisible canonical motion is impossible

Use the inverse-entropy function Psi_i from [the nonlinear coercivity proof](../nonlinear_radial_2026_10_19/NONLINEAR_COERCIVITY.md). Its height Hessian is bounded below by 1/W, where W=max_i ||-F_i,E||_infinity. Every fixed-L canonical rearrangement preserves its integral, so Delta Psi=0 at every time. The global strong convexity inequality gives

\[
D_0(f):=\sum_i\int E_i^F(f_i-F_i)d\Gamma
=\widetilde D(f)
\ge\frac1{2W}\sum_i\|f_i-F_i\|_2^2.
\tag{3}
\]

This uses the global relative-entropy inequality, not the more delicate local energy-coercivity theorem.

Let mu_i be shell densities, K the full radial-plus-angular kinetic energy, and I=sum_i int r^2 f_i dGamma. Direct integration of transport gives

\[
I''=4K(f)+2\sum_i\int r a_i[f](r)\mu_i(r)dr.
\tag{4}
\]

Suppose nontrivial canonical f_0 has precisely the equilibrium species densities initially. Then its initial forces equal the equilibrium forces, and comparison with the stationary equilibrium virial yields

\[
I''(0)=4[K(f_0)-K(F)]
=4D_0(f_0)
\ge\frac2W\sum_i\|f_{i0}-F_i\|_2^2>0.
\tag{5}
\]

The second equality follows because the fixed-potential integrals of the density difference vanish. Therefore such data cannot keep both original densities even on an initial time interval. Matching the density at one instant is permitted; propagating that equality would contradict (5).

More generally, equality of both actual accelerations with the equilibrium accelerations at every time implies equality of both cumulative masses. The free equation gives m_f=-m_t, and the tethered equation then gives

\[
0=m_t\left[\frac G{r^2}
+\frac{c(M_t+M_t^F)}{r^4}\right].
\tag{6}
\]

The bracket is positive. Static densities give I''=0 and K=K(F) by (4), hence D_0=0 and f=F by (3). This rules out the entire strictly radial canonical field-invisible route. It does not rule out a confined density-breathing solution. The orientation-odd construction in the previous checkpoint is not a counterexample to this statement: it is outside the radial canonical class.

## Identical original full support for all time forces stationarity

Write the upper energy boundary as

\[
B_i(r,v,L)=E_i^F(r,v,L)-b_i(L)=0,
\quad b_i(L)=E_{c,i}(L)+\delta^2\sigma_i(s_i(L)).
\tag{7}
\]

The exact smooth construction has sigma_i(r)=omega_i(r)^2 h(r)^2>0 in the spatial interior, L=L_c,i(s), and F_i>0 for E_c,i<=E<b_i. If the transported supports were exactly K_i throughout a time interval, their smooth upper boundaries must be tangent to the actual transport. Since L is conserved,

\[
\mathscr D_i B_i=v[a_i[f](r)-a_i^F(r)]=0
\quad\hbox{on the upper boundary}.
\tag{8}
\]

At each r in the open halo take L=L_c,i(r). The upper boundary then has v=+sqrt(2 delta^2 sigma_i(r))>0, so (8) gives a_i[f]=a_i^F throughout the interior. Outside the old spatial support, equality follows from the unchanged canonical masses; inside the hollow core both cold cumulative masses vanish. Equation (6) and (3)-(4) force f=F.

Thus an all-time requirement of exactly the original complete phase-space support is incompatible with nonstationarity in this canonical class. This does not apply to keeping the original support only at t=0 and allowing a larger finite enclosing radius later. The latter is the unresolved confinement question.

## An admissible perturbation immediately moves the old boundary

Perturb only the free population. Choose smooth chi(E,L)>=0 with compact support strictly inside the occupied invariant region and a smooth eta(r)>0 on a radial interval intersecting those orbits. Let

\[
g(r,v,L)=\eta(r)v\chi(E_f^F,L),\qquad
f_{f0}^{s}=F_f\circ T_s^{-1},\quad f_{t0}^s=F_t,
\tag{9}
\]

where T_s is the fixed-L Hamiltonian flow generated by g, dot r=g_v, dot v=-g_r. The generator is compactly supported inside K_f, so T_s is identity near its boundary, T_s(K_f)=K_f, and f_f0^s=F_f on a whole boundary collar. Positivity, masses, heights, angular support and all fixed-L Casimirs are exact. These data approach F in every fixed C^k norm and X as s tends to zero.

Define the Poisson bracket {p,q}=p_r q_v-p_v q_r. The first cumulative-mass variation is

\[
\begin{aligned}
\dot M_f^{\,s}(r)|_{s=0}
&=-C_\Gamma\int F_f g_v\,dv\,dL\\
&=C_\Gamma\eta(r)\int v^2\chi(E_f^F,L)F_{f,E}\,dv\,dL<0
\end{aligned}
\tag{10}
\]

where the dot here means parameter derivative, not physical time derivative. The first line follows by integrating -{F_f,g} over all phase radii below r. Boundary terms vanish. The second follows by velocity integration by parts. Consequently, on a smaller interval of strict sign and for small positive s,

\[
a_f[f_0^s]-a_f^F>0,\qquad a_t[f_0^s]-a_t^F>0.
\tag{11}
\]

Choose an upper energy boundary point with v>0 at such a radius. The exact physical derivative of (7) is positive there at t=0. Its transported boundary leaves K_f immediately. The flow maps the full support to the evolved support; continuity from positive interior points confirms occupation outside the old K_f at small positive times. Near the initially untouched collar the transport residual is [a_f[f_0^s]-a_f^F]v F_f,E, nonzero at occupied interior points, so the data are genuinely nonstationary.

Equation (2) supplies one fixed negative initial gap for all sufficiently small s. This construction therefore obeys every specified initial restriction, even equality with F near the full boundary, yet the original orbital support is not invariant. It does not show escape to infinity, expansion beyond every finite radius, or failure of confinement in a larger fixed region. The outer circular tip and an untouched initial collar cannot be used as an invariant barrier without a new argument.
