# What remains in the strictly radial propagation proof

19 October 2026. Claims ZAR-P3 through ZAR-P5. These are precise checks of proposed initial-data mechanisms in the strictly radial class. They do not refute confinement in the fixed-gap, unchanged-support canonical subclass. The exact orientation-odd theorem in [P1](ORIENTATION_ODD_INVARIANT.md) uses a larger phase-space class; it is not substituted for the radial problem here.

## Matching initial density current and pressure does not freeze the field

Choose one species and a compact product box inside its equilibrium positivity set, symmetric in radial velocity. Let q(r), chi(v), zeta(L) be smooth bumps supported in that box, with chi even, int chi dv !=0, int zeta dL=0 and int L zeta dL !=0. The last two conditions can be achieved by taking zeta to be the derivative of a nonzero nonnegative bump. For sufficiently small nonzero alpha set

\[
f_{i0}=F_i+\alpha q(r)\chi(v)\zeta(L),
\qquad f_{j0}=F_j\quad(j\ne i).
\tag{25}
\]

The compact box has F_i bounded below, so nonnegativity holds. The data are smooth, initially even in v, supported within the original orbital support, arbitrarily close in X, and have the same fixed negative initial energy gap. Density, radial current and radial pressure initially equal those of F exactly. In fact all initial moments depending only on v vanish for the perturbation because int zeta=0.

Let mu=C_Gamma int f dv dL, j=C_Gamma int v f dv dL, Q=C_Gamma int v^2 f dv dL and Z=C_Gamma int L f dv dL. The exact first moment equation is

\[
\partial_t j=-\partial_rQ+Z/r^3+a_i\mu.
\]

At t=0 both fields equal the equilibrium fields, and the only changed term is Z. Thus

\[
\partial_t j_i(0,r)=
\frac{C_\Gamma\alpha q(r)}{r^3}
\left(\int\chi(v)dv\right)
\left(\int L\zeta(L)dL\right),
\]

\[
\partial_t^2\mu_i(0,r)=-\partial_r\partial_tj_i(0,r)
\not\equiv0.
\tag{26}
\]

This is an actual self-consistent initial derivative, not prescribed forcing. Initial evenness and matching the initial density, current and radial dispersion do not propagate a fixed field. The construction does not establish eventual loss of a binding reserve or escape.

## The exact linear work identity and its pointwise limitation

On a compact interior set of eccentric equilibrium orbits, use action-angle variables (theta,q), q=(J,L), with J=(2 pi)^(-1)oint v dr and D_i=Omega_i(q) partial_theta. Linearize f_i=F_i+epsilon h_i and Phi_i=Phi_i^F+epsilon psi_i. The actual transport linearization is

\[
(\partial_t+D_i)h_i=F_{i,E}D_i\psi_i.
\tag{27}
\]

F_i,E is constant along an equilibrium orbit. Hence on that orbit z_s,

\[
\boxed{\int_0^t\partial_s\psi_i(s,z_s)ds
=\left[\psi_i-\frac{h_i}{F_{i,E}}\right](t,z_t)
-\left[\psi_i-\frac{h_i}{F_{i,E}}\right](0,z_0).}
\tag{28}
\]

This is a useful exact first-order cancellation. It is not a bound: the old quadratic controls int h_i^2/(-F_i,E), not a uniform pointwise quotient h_i/F_i,E. The derivative F_i,E vanishes at the smooth cutoff; perturbations outside the old support also have no such quotient. A pointwise propagated estimate or a nonlinear replacement is still needed.

## The actual coupling has diagonal resonances

Write c=G^2/a_0. The linear potential-density kernels in radial shell measure are

\[
P_{ff}(r,r')=P_{ft}(r,r')=P_{tf}(r,r')
=-G/\max(r,r'),
\]

\[
P_{tt}(r,r')=2c\int_{\max(r,r')}^\infty
\frac{M_{F_t}(s)}{s^4}ds.
\tag{29}
\]

These follow by inserting m_i(s)=int_0^s delta mu_i(r')dr' into the exact potential variations. No external linear-response theorem is imported.

For Fourier coefficients h_i,k=(2 pi)^(-1)int h_i exp(-ik theta)dtheta, the linear initial-value system is

\[
h_{i,k}(t,q)=e^{-ik\Omega_i(q)t}h_{i,k}(0,q)
+ik\Omega_i(q)F_{i,E}\int_0^t
e^{-ik\Omega_i(q)(t-s)}\psi_{i,k}(s,q)ds,
\qquad \psi=\mathcal P h.
\tag{30}
\]

Here the action-space kernel of P can be normalized as

\[
\mathcal K_{ij,kn}(q,q')=
\frac1{(2\pi)^2}\int\!\!\int
e^{-ik\theta}P_{ij}(r_i(\theta,q),r_j(\theta',q'))
e^{in\theta'}d\theta d\theta',
\]

so psi_i,k=sum_j,n int K_ij,kn h_j,n dnu(q'), with dnu=2 pi C_Gamma dJ' dL'. The diagonal free-species kernel has the explicit sign identity

\[
\mathcal K_{ff,kk}(q,q)
=-G\int_0^\infty\frac{|A_k(s;q)|^2}{s^2}ds<0,
\qquad k\ne0,
\tag{31}
\]

\[
A_k(s;q)=\frac1{2\pi}\int
\mathbf1_{\{r(\theta,q)\le s\}}e^{ik\theta}d\theta.
\]

To verify (31), use 1/max(r,r')=int_0^infinity 1_(r<=s)1_(r'<=s)s^(-2)ds. Put pericenter at theta=0. For s strictly between turning radii, r<=s corresponds to [-theta_s,theta_s], so A_k=sin(k theta_s)/(pi k). This is not identically zero on an eccentric orbit. Its support is a bounded s interval away from zero, making the integral finite and strictly positive before multiplication by -G.

The first free-streaming term of (30), inserted into the work on a harmonic k of a receiving orbit, has the factor

\[
-\frac{n\Omega_j(q')}{k\Omega_i(q)-n\Omega_j(q')}
\left(e^{i[k\Omega_i(q)-n\Omega_j(q')]t}-1\right).
\tag{32}
\]

At resonance its limit is -in Omega_j t. The denominator vanishes already at j=i=f, n=k, q'=q, where (31) proves nonzero coupling. Thus a uniform nonresonance condition throughout a smooth occupied action set cannot hold, and termwise division by a denominator bounded away from zero is not a valid route. This does not prove secular growth of the full self-consistent solution. Integration, principal-value cancellation and feedback in (30) have not been discarded from the actual problem.

There is an additional compatibility check on normal modes. A finite-energy mode exp(-i omega t) satisfies

\[
H_{i,k}=\frac{k\Omega_iF_{i,E}}{k\Omega_i-\omega}\Psi_{i,k}.
\tag{33}
\]

At a regular resonant surface with grad_q(k Omega_i-omega) !=0 and -F_i,E>0, a continuous nonzero Psi_i,k would make int |H_i,k|^2/(-F_i,E) diverge across that surface. Consequently such a finite-energy mode must have vanishing Psi_i,k on the regular resonant surface. An arbitrary prescribed resonant pump is therefore not automatically a finite-energy self-consistent mode.

The still open step is a uniform signed-work estimate incorporating the actual feedback and resonances, particularly near the flat support edge. Equations (28)-(33) identify the term to control; they do not supply nonlinear phase mixing or a bound on the outward-crossing reserve. The exterior sphere b from checkpoint 06 has no ordinary equilibrium crossings; these interior formulas study the stronger energy-transfer issue rather than asserting a crossing-map counterexample.

## A nearby homologous breathing ansatz is excluded

Consider separate scale factors a_t(t),a_f(t) and the canonical radial ansatz

\[
f_i(t,r,v,L)=F_i(r/a_i,\ a_iv-a_i'r,\ L).
\tag{34}
\]

Its shell masses are M_i(t,r)=M_i^F(r/a_i). Substitution into transport, using F_i,E<0 on an open warm velocity set, requires

\[
a_i''x=a_i^{\rm phys}(t,a_ix)-a_i^F(x)/a_i^3.
\tag{35}
\]

Near a_t=a_f=1, the rescaled exact-law annuli have a nondegenerate overlap. On this interval put q=1-f for the equilibrium fraction. The free equation in (35) reads

\[
a_f''x=
\frac{GM_b(a_f^{-3}-a_f^{-2})}{x^2}
+\frac{GA}{x}
\left[a_f^{-3}-\frac{f(a_f/a_t)+q}{a_f^2}\right].
\tag{36}
\]

The functions x,x^(-1),x^(-2) are linearly independent on an interval. Positive M_b forces a_f=1, and positive f then forces a_t=1. This closes the nearby independent-homology ansatz in the stated overlap regime. It does not exclude other time-periodic or nonstationary radial solutions.

The remaining initial-data theorem is therefore narrower than the old unrestricted stability claim: establish a propagated invariant or signed-work bound for strictly radial nonstationary data, preferably with a fixed negative initial gap and unchanged original support/Casimirs. Neither the orientation-odd sector, the moment matching conditions, nor the excluded normal-form and homology shortcuts establish that theorem.
