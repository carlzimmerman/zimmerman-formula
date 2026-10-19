# Nonlinear radial evolution and Lyapunov stability

19 October 2026. Claims ZAR-N2 and ZAR-N3. The equilibrium is the exact bounded smooth two-population halo of the preceding checkpoint. This theorem permits nearby radial distributions to change their Casimirs; it is not restricted to an exactly equimeasurable perturbation. A fixed positive angular-momentum gap is required.

## Stability statement

Fix I = [ell,Lambda] inside (0,infinity), containing both equilibrium angular supports, and a uniform initial height bound M greater than the equilibrium height. For every epsilon > 0 there is eta > 0 such that the following holds. Let f_i,in be nonnegative smooth compact radial data supported in L in I, with ||f_i,in||_infinity <= M and

\[
X(f_{\rm in}-F)=\sum_i\int(1+v^2+L/r^2)|f_{i,\rm in}-F_i|d\Gamma<\eta.
\]

The self-consistent nonlinear system with the original two forces has a unique global classical radial solution, and

\[
\boxed{\sup_{t\geq0}X(f(t)-F)<\epsilon.}
\]

This is stability of the same fixed equilibrium. It does not assert exact density-law preservation or a fixed outer support radius for disturbed solutions. The modulus eta(epsilon) is not made explicit. Low-angular-momentum collisions outside the fixed gap are outside the theorem.

## Global classical flow and uniform speed bounds

Both species solve

\[
\partial_t f_i+v\partial_r f_i+(L/r^3+a_i[f])\partial_v f_i=0,
\]

\[
a_t=-G(M_b+M_f)/r^2+G^2M_t^2/(a_0r^4),\qquad
a_f=-G(M_b+M_t+M_f)/r^2.
\]

Let T and U be the initial total tethered and free masses, and set A_G = G(M_b+T+U), B_G = G^2T^2/a_0. Along every occupied characteristic,

\[
\frac L{r^3}-\frac{A_G}{r^2}\leq\ddot r
\leq\frac L{r^3}+\frac{B_G}{r^4}.
\]

Define the initial-data constants

\[
E_+=\max\left(0,\sup_{\rm initial\ support}
\left[\frac{v^2}{2}+\frac L{2r^2}-\frac{A_G}{r}\right]\right),
\quad V_0=\sup_{\rm initial\ support}|v|,
\quad
\rho=\frac{\ell}{A_G+\sqrt{A_G^2+2E_+\ell}}>0.
\]

On an inward leg the comparison Kepler energy e_A = v^2/2+L/(2r^2)-A_G/r has derivative v(ddot r-L/r^3+A_G/r^2) <= 0. A later inward leg starts at an outer turning point a >= L/A_G, where e_A <= 0. Therefore every inward leg has e_A <= E_+, giving r >= rho and v^2 <= 2E_+ + A_G^2/ell. Initial radii already satisfy r >= rho by the same quadratic inequality; outward legs increase radius from such a point.

On an outward leg, integrate the upper acceleration bound with respect to radius. Its starting radius is at least rho; its starting speed is zero except for a possibly initial outward leg, whose speed is at most V_0. Thus

\[
|v(t)|^2\leq V_*^2:=\max\left(
2E_++A_G^2/\ell,
V_0^2+\Lambda/\rho^2+2B_G/(3\rho^3)\right).
\]

Tangential speed is at most sqrt(Lambda)/rho. Consequently

\[
r(t)\geq\rho,\qquad
R_{\rm supp}(t)\leq R_{\rm supp}(0)+V_*t.
\]

These are time-uniform inner and velocity bounds, and a finite-time outer bound. They do not require a negative initial particle-energy gap. Their constants depend on the individual initial support; a tiny fast tail can make V_0 large.

The radial flow preserves L, height, phase volume at each L, total species masses and every height Casimir integral. Since v and L are bounded,
mu_i(t,r) <= 2 C_Gamma V_*(Lambda-ell)||f_i,in||_infinity, with C_Gamma = 4 pi^2. All forces and their first radial derivatives are therefore bounded on r >= rho for all time. Higher field derivatives use one fewer derivative of f, because enclosed mass is a radial integral. A local characteristic iteration on the initially separated compact support gives existence and uniqueness; the displayed bounds and derivative Gronwall estimates continue that smooth solution through every finite time. No point-mass collision or finite-time velocity blowup occurs.

Integration by parts on this classical compact support proves conservation of H and of the inverse-entropy Casimirs from [NONLINEAR_COERCIVITY.md](NONLINEAR_COERCIVITY.md). Those entropies are C1 in height. Their possible lack of smoothness in L causes no problem because each fixed-L flow is measure-preserving.

## Compactness for bounded-energy sequences

Here K denotes kinetic energy, not A_G. With S = M_t+M_f and total mass m, angular kinetic energy gives

\[
S(r)\leq2Kr^2/\ell,\qquad
\int r^{-1}dS\leq\sqrt{2mK/\ell}.
\]

Writing P(M_t) = (G/2) int M_t^2/r^2 + (G^2/(3a_0)) int M_t^3/r^4 >= 0, the Hamiltonian satisfies

\[
\mathcal H(f)\geq K-G(M_b+m/2)\sqrt{2mK/\ell}.
\]

Thus bounded masses and an upper bound on conserved energy give a uniform kinetic bound. At fixed r, split the radial velocity integral at a cutoff and optimize it. The uniform height and L-range bounds give

\[
\mu_i(r)^3\leq C M^2(\Lambda-\ell)^2
\int v^2 f_i(r,v,L)\,C_\Gamma\,dv\,dL,
\qquad \|\mu_i\|_{L^3(dr)}^3\leq C K.
\]

Hence cumulative masses are compact locally in the uniform norm. Weak L2 convergence of f identifies their limits: first truncate velocity, then use the kinetic tail bound. The angular estimate handles the inner endpoint.

All nonkinetic energy terms are continuous under this convergence. Indeed central quadratic-field and cubic-field tails are respectively O(a^3 K^2) and O(a^3 K^3), and their outer tails are at most m^2/b and m^3/(3b^3). The baryon tails are O(aK) and O(m/b). The fixed equilibrium potentials also have continuous integrals: separate their point-baryon term from their bounded continuous cold part, which tends to zero at infinity. Kinetic energy itself is lower semicontinuous.

## Nearby invariant leaves

Take any sequence of such states f_n whose initial data approach F in X, and allow their observation times to vary. The transported height distribution at each L equals its initial one. For each bounded-L test and each convex nonnegative increasing height function, weak lower semicontinuity on finite phase boxes, followed by exhaustion, shows that any weak limit f satisfies f precedes_L F. To see the per-L assertion, use height tests (s-alpha)_+ times arbitrary nonnegative L tests. Their initial integrals converge by initial L1 closeness and the uniform height bound. Thus the weak limit belongs to precisely the class in the nonlinear coercivity lemma, even though f_n themselves need not.

The needed global weak subsequence exists because uniform height and mass bounds give a uniform L2 bound. The preceding kinetic and cumulative-mass compactness applies to it. No exact equality of perturbed and equilibrium Casimirs is assumed.

## The nonlinear first-exit argument

Use Dtilde and D_0 from the coercivity proof. Initially Dtilde tends to zero with X: the entropy is uniformly Lipschitz in height on the prescribed height ball, and |E_i^0| <= C(1+v^2+L/r^2). Initial energy also tends to H(F). Explicitly, |m_i(r)| <= X min(1,r^2/ell) in the exact polynomial energy identity bounds the quadratic and cubic defects by C X^2 and C X^3.

Along each solution DeltaPsi is constant and

\[
\widetilde D(f(t))=\Delta\Psi(f_{\rm in})+D_0(f(t)).
\]

It is continuous on finite time intervals. Choose any fixed 0 < tau < d_*, where d_* is the local nonlinear-coercivity radius. Suppose arbitrarily close initial data have first times t_n with Dtilde(f_n(t_n)) = tau. Then

\[
\mathcal H(f_n(t_n))\longrightarrow\mathcal H(F),\qquad
\Delta\Psi(f_{n,\rm in})\longrightarrow0,\qquad
D_0(f_n(t_n))\longrightarrow\tau.
\]

Uniform kinetic and height bounds give a weak limit f in the submajorization class. Nonkinetic energies converge and kinetic energy is lower semicontinuous, so

\[
\mathcal H(f)\leq\mathcal H(F),\qquad D_0(f)\leq\tau<d_*.
\]

For the second inequality separately use D_0 = K(f)-K(F) plus the fixed-potential integrals: the latter are continuous by the compactness bounds above, while K is lower semicontinuous. The coercivity lemma applies to this merely measurable finite-kinetic-energy weak limit, not only to smooth or equimeasurable states.

Local nonlinear coercivity forces D_0(f) = 0 and f = F. Nonkinetic energy convergence and H(f_n) to H(F) now force K(f_n) to K(F). Continuity of the fixed-potential integrals then gives D_0(f_n) to zero, contradicting tau. Thus sufficiently close data cannot exit any sufficiently small Dtilde neighborhood.

Finally X <= C(sqrt(Dtilde)+Dtilde) transfers this uniform-in-time entropy control to the stated X stability. This closes the nonlinear proof without a global entropy Taylor expansion or an assumption that canonical maps remain small forever.
