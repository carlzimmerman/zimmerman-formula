# Confined nonstationary angular currents with spherical density

19 October 2026. Claim ZAR-P1. This is an initial-data theorem for the central kinetic equations with spherical densities. It allows a distribution depending on angular-momentum orientation, so it is a larger phase-space class than the strictly radial distributions f_i(r,v_r,L) in the previous stability theorem. The distinction is part of the claim.

## Initial condition and conclusion

Keep the exact bounded smooth warm equilibrium F_i(E_i^F,L) and its finite support K_i, including its negative occupied energy cap. Use full coordinates x,u in R^3, with

\[
r=|x|,\quad v_r=u\cdot x/r,\quad
L=|x\times u|^2,\quad
L_z=(x\times u)\cdot e_z,\quad
E_i^F=|u|^2/2+\Phi_i^F(r).
\]

Here e_z is one fixed axis, L is squared specific angular momentum, and L_z is a component of specific angular momentum, so |L_z|<=sqrt(L). The forces are still exactly

\[
a_t=-G(M_b+M_f)/r^2+G^2M_t^2/(a_0r^4),\qquad
a_f=-G(M_b+M_t+M_f)/r^2.
\]

Let 0<theta<1 and choose smooth radial functions h_i0(r,v_r,L) with compact support inside {F_i>0}. Impose the initial pointwise bound

\[
\boxed{f_{i0}(x,u)=F_i(E_i^F,L)+L_z h_{i0}(r,v_r,L),
\qquad |L_z h_{i0}|\le\theta F_i(E_i^F,L).}
\tag{1}
\]

The bound is directly checkable in reduced variables by requiring sqrt(L)|h_i0|<=theta F_i. Require at least one species to have L_z D_i^F h_i0 not identically zero, where

\[
D_i^F=v_r\partial_r+(L/r^3+a_i^F(r))\partial_{v_r}.
\tag{2}
\]

Then there is a global classical genuinely nonstationary solution of the same central kinetic equations. Its species densities and every radial velocity moment equal the equilibrium values exactly for every x and time. The self-consistent fields are consequently Phi_i^F at every time. Its particle energy E_i^F is conserved, and

\[
\boxed{(1-\theta)F_i\le f_i(t)\le(1+\theta)F_i,
\qquad \operatorname{supp}f_i(t)=K_i\quad(t\ge0).}
\tag{3}
\]

Thus the original inner and outer boundaries, density law, population fractions and centered radial dispersion are retained exactly. In particular the original positive annulus dispersion has the same lower bound for all time in this class. No accumulated-work hypothesis is assumed.

## Explicit construction and self consistency

Let S_i^t be the full central characteristic flow of the fixed equilibrium potential. Define the radial passive transport

\[
h_i(t)=h_{i0}\circ(S_i^t)^{-1},\qquad
f_i(t,x,u)=F_i(E_i^F,L)+L_z h_i(t,r,v_r,L).
\tag{4}
\]

Writing h_i as a radial function in (4) is legitimate because the central flow preserves rotational invariance. Along it E_i^F, L and L_z are conserved. Hence (4) solves the full kinetic equation in that fixed central field and transports (1) into (3). The equilibrium support is an invariant compact set separated from r=0, so all characteristics used in (4) exist smoothly for all time. Smoothness is asserted at each finite time, not uniform derivative bounds as time tends to infinity.

For each fixed x consider the velocity rotation

\[
\mathcal T_xu=2(u\cdot\widehat x)\widehat x-u.
\tag{5}
\]

It leaves v_r, L, E_i^F and d^3u unchanged and sends L_z to -L_z. Thus for every radial velocity weight p(r,v_r,L) for which the integral exists,

\[
\int p(r,v_r,L)L_z h_i(t,r,v_r,L)d^3u=0.
\tag{6}
\]

Taking p=1 shows rho_i(t,x)=rho_i^F(r). These are spherical densities, and substituting their enclosed masses into the actual two forces gives exactly a_i^F. Therefore the fixed field used to construct (4) is the self-consistent field of the constructed solution. This is an exact finite-amplitude argument; there is no linearization or unproved future smallness condition.

Taking p=v_r and p=v_r^2 shows that the radial current and radial second moment also remain precisely their equilibrium values. Since the equilibrium radial current is zero and its density is unchanged, the centered radial dispersion is unchanged. The same cancellation holds for every radial moment, including mixed weights involving L. Nonradial currents and stresses need not remain stationary.

## A concrete nonstationary choice

Choose a smooth nonnegative chi_i(E,L), compactly supported in an invariant band strictly inside the occupied equilibrium action domain, with nonempty eccentric orbital interior. Set

\[
h_{i0}=\alpha_i v_r\chi_i(E_i^F,L).
\tag{7}
\]

The compact band has a positive minimum of F_i and bounded sqrt(L)|v_r|chi_i, so sufficiently small nonzero alpha_i verifies (1). Since E_i^F and L are first integrals,

\[
D_i^F h_{i0}
=\alpha_i(L/r^3+a_i^F(r))\chi_i(E_i^F,L)
\not\equiv0.
\tag{8}
\]

The full distribution therefore has nonzero initial time derivative. It is not made nonstationary by relabeling identical particles or adding a massless species.

There is a physical moment detecting the change. Away from the axis use the local azimuthal direction e_phi=(e_z cross x)/|e_z cross x|. Initially the perturbation of the radial-azimuthal stress is

\[
\int v_r u_\phi L_z h_{i0}\,d^3u
=\alpha_i r\sin\vartheta
\int v_r^2u_\phi^2\chi_i(E_i^F,L)\,d^3u,
\tag{9}
\]

which is nonzero where the band intersects the shell. The azimuthal mean-current derivative is also proportional to the velocity integral of -(L/r^3+a_i^F)u_phi^2 chi_i; a suitable band near an eccentric turning point makes it nonzero on some shell. Thus the evolving sector has observable velocity correlations even though its radial moments cancel.

## Initial binding reserve propagates exactly

The original compact orbital support has E_i^F<=-eta_iF<0 for some common eta_iF. Condition (1) uses exactly that same support, and energy conservation under the now proved static field gives

\[
E_i^F(t)=E_i^F(0)\le-\eta_{iF}\qquad(t\ge0).
\tag{10}
\]

All the work rates in the previous checkpoint are identically zero because the densities are static. In particular their signed work and positive-work budgets follow from the initial symmetry condition, rather than being imposed for later times.

For a finite boundary B outside the original support choose the checkable margin

\[
m_{i,*}=\inf_{K_i}
\left[L/(2B^2)+\Phi_i^F(B)-E_i^F\right]>0.
\tag{11}
\]

A sufficiently large B always has this property. The entire bracket is conserved along each trajectory, so the relative-potential reserve in checkpoint 06 remains positive forever. Equivalently the original compact support already remains K_i by (3). At any outward crossing to which the previous vacuum comparison criterion applies, actual and comparison potentials coincide and the energy reserve is the conserved one in (10). This proves propagation from initial data; it does not assume an all-time crossing condition.

## Restricted nonlinear stability

Use the full phase-space norm

\[
X_{\rm full}(f-F)=\sum_i\int(1+|u|^2)|f_i-F_i|d^3x\,d^3u.
\]

The perturbation in (4) is transported by a volume-preserving fixed Hamiltonian flow. Its L1 norm is therefore constant. With W_* = max_i sup_Ki(1+|u|^2),

\[
\boxed{\sup_{t\ge0}X_{\rm full}(f(t)-F)
\le W_*\|f_0-F\|_1\le W_*X_{\rm full}(f_0-F).}
\tag{12}
\]

Two solutions of this class use the same fixed fields, so the same estimate applies to their difference. This is an actual nonlinear Lyapunov estimate within the invariant class, and the relative bound (3) gives a stronger pointwise envelope. It is not a theorem of stability against arbitrary nonspherical perturbations. The old radial stability theorem remains true for its own class but is not invoked as a theorem about the orientation-dependent distributions here.

## The strict radial limitation

At fixed x, the rotation by pi about x is an SO(3) rotation that fixes x and implements (5). A fully SO(3)-invariant phase distribution must be invariant under that rotation. Any correction odd under (5) must therefore vanish in the strictly radial class f(r,v_r,L). Indeed the full rotational average of (4) is F_i at each (r,v_r,L), for every time.

The construction proves an initial-data propagation theorem for genuine angular-current dynamics with spherical density. It does not prove one for a nonstationary radial density or a nonstationary strictly radial distribution. If an arbitrary radial solution g_i(t) replaces F_i, orientation-odd perturbations can ride on its fields, but their support follows g_i; that observation transfers, rather than solves, the unresolved radial confinement problem.
