# Independent reviews of the fixed-geometry force and cosmological slice

This is a read-only review of sibling constructions. The reviewer did not
construct or modify their scripts. The targets were the root agent's displayed
formulas, and `filtered_zero_field/check.py` where noted. The root reports were
still being assembled when these implications were reviewed; this note is not
a certification of later unexamined text or source revisions.

## A. Outer filtering at an inner MOND zero

**Verdict:** the spatial regularity bound is correct for a fixed flat compact
torus, positive filter width, and the stated normalized Fourier convention.
Unique prescribed-force particle flow follows with the time assumptions below.
It does not establish source-to-force Lipschitz continuity or the coupled
matter/metric Cauchy problem.

Let the torus have physical Fourier wavevectors k and normalized volume
measure, and set S=exp(xi^2 Delta/2), xi>0. The longitudinal projector P_L(k)
has norm one for k!=0 and vanishes at k=0. For the physical phantom force
a_ph=-S P_L F, Parseval and pointwise Cauchy–Schwarz give

\[
\begin{aligned}
\|D a_{\rm ph}(x)\|_F
&\le\sum_{k\ne0}|k|e^{-\xi^2|k|^2/2}|P_L(k)\widehat F_k|\\
&\le\left[\sum_{k\ne0}|k|^2e^{-\xi^2|k|^2}\right]^{1/2}
\left[\sum_{k\ne0}|\widehat F_k|^2\right]^{1/2}
\le C_{\xi}\|F\|_{L^2}.
\end{aligned}
\]

The matrix Frobenius norm bounds its operator norm, so no missing factor of
sqrt(dimension) is required. The heat sum is finite for every xi>0. The same
argument with higher powers of |k| proves higher spatial regularity. This
works even when the inner phantom constitutive map has an unbounded tangent
at zero: continuity and F in L2 suffice. There is no uniform bound as xi->0.

For the usual physical L2 norm on R3 with unitary Fourier transform, the
corresponding constant is

\[
(2\pi)^{-3/2}\left[\int_{\mathbb R^3}|k|^2e^{-\xi^2|k|^2}d^3k\right]^{1/2}
=\frac{\sqrt3}{4\pi^{3/4}\xi^{5/2}}.
\]

This requires F in L2(R3); an isolated unscreened MOND 1/r tail does not
satisfy that hypothesis. The compact result does not need that isolated-space
extension.

For a time-independent prescribed source, the force is smooth and bounded on
the compact torus. The system xdot=v, vdot=a_ph(x) therefore has a unique
global particle flow. For a time-dependent prescribed source, require
measurability in time and locally integrable bounds on the force and its
spatial Lipschitz constant, for example a locally bounded L2 norm of F(t)
on every finite time interval. These are conditions on the supplied force;
they do not prove that a self-consistent matter evolution maintains them.

The finite code uses a one-coordinate dependence embedded in T3, so its
one-dimensional heat sum is a valid sharper bound for that subspace. Its
Gaussian tail estimate is correct: k^2 exp(-xi^2 k^2) decreases beyond
1/xi, and the chosen cut*xi>=12 implies
\(t^2\le\xi^{-2}e^{\xi^2t^2/2}\). Integrating the remaining Gaussian gives
the displayed two-sided tail 2 exp(-xi^2 cut^2/2)/(xi^4 cut).

Two implementation-scope observations were sent to the author:

- The sampled `force` uses +S P_L F rather than the physical minus sign.
  All recorded norms and refinement ratios are sign invariant. The author
  elected to label it a sign-insensitive representative and preserve the
  existing run hashes, rather than silently changing a recorded run.
- The FFT bound applies exactly to the trigonometric interpolant of the
  sampled F. Grid refinement is numerical evidence for the continuum example,
  not a proved interpolation-error estimate. The analytic continuum bound
  stands independently of that numerical convergence evidence.

The small-source scaling test correctly distinguishes the two questions:
the constitutive map near a zero produces force proportional to sqrt(epsilon),
so its ratio to an epsilon-sized source perturbation diverges. Outer spatial
smoothing does not change that amplitude scaling. Failure of this particular
Lipschitz estimate does not itself prove failure of every possible coupled
well-posedness argument.

## B. Nonlinear inhomogeneous lapse constraint with a global trace mode

**Verdict:** the proposed exact family satisfies the displayed lapse and
momentum constraints with a positive lapse, expanding trace momentum, fixed
action constants, and a quantitative positive kernel-complement gap. This
is a constraint slice, not a proof of Hamilton evolution, preservation of a
full model's additional constraints, or criterion-B Cauchy well-posedness.

On a flat compact connected torus, assume b>0, ell>0 and

\[
H[N]=\int N[A-b|D\ln N|^2],dV,\qquad
A=-\ell q^2+\bar\Lambda+\rho(x),
\]

where q is spatially constant, the trace-free gravitational momentum is zero,
and the canonical matter data have j_i=0. The lapse variation holds those
canonical data fixed. In particular rho in this Hamiltonian must be independent
of N under that variation; substituting a prescribed coordinate phase rate
first would be a different variational problem.

Putting N=y^2>0 gives

\[
H[y]=\int(Ay^2-4b|Dy|^2)dV,\qquad
\delta H=-2\int\delta y\,L y\,dV,\qquad L=-4b\Delta-A.
\]

Thus the sign in Ly=0 is correct. In the convention q=trace(pi)/sqrt(h),
the pure trace momentum is pi^{ij}=sqrt(h) q h^{ij}/3. Its spatial divergence
vanishes for constant q, satisfying the displayed momentum constraint when
matter momentum vanishes. The trace kinetic Hamiltonian gives
K=-3 ell q, so q<0 is expanding in that convention. If q is normalized
differently, this proportionality must be translated before naming the branch.

For an arbitrary specified rho with negative lowest eigenvalue lambda0 of
L0=-4b Delta-(LambdaBar+rho), choosing
q=-sqrt(-lambda0/ell) gives L=L0-lambda0. This chooses a constraint datum q;
it does not retune the action parameter LambdaBar. A positive mean of
LambdaBar+rho suffices for lambda0<0 by the constant Rayleigh test. If
lambda0>=0, the claimed strictly expanding real-q branch does not follow.
The normalized positive groundstate is unique on a connected compact leaf,
and the gap is positive for each fixed smooth source. There is no claimed
uniform gap over unrestricted source profiles.

The explicit family supplied by the author avoids relying on a general
groundstate existence theorem for its construction. On the 2pi torus, set

\[
y=e^{\epsilon\cos x},\quad
A=-4b\Delta y/y=4b\epsilon\cos x-4b\epsilon^2\sin^2x,
\]
\[
\rho=\rho_{\rm base}+A,\quad
\rho_{\rm base}=\ell q^2-\bar\Lambda
\ge4b(|\epsilon|+\epsilon^2),\quad q<0.
\]

Then rho>=0 and Ly=0 exactly. The source is genuinely inhomogeneous for
epsilon!=0. This is an explicitly chosen family of admissible matter data,
not a claim that every prescribed source has this cosine-exponential form.
The action constants remain fixed while q and the initial density are chosen.

For any smooth v, write v=yf. Integration by parts gives the exact identity

\[
\int v L v\,dV=4b\int y^2|Df|^2dV\ge0.
\]

Equality requires Df=0 and hence v=c y on the connected torus. On the
orthogonal complement of y, the condition is int y^2 f=0. Taking the ordinary
mean fbar and using weighted-mean minimization followed by ordinary Poincare,

\[
\int y^2f^2\le\int y^2(f-\bar f)^2
\le\frac{\max y^2}{k_{\min}^2}\int|Df|^2
\le\frac{\max y^2}{\min y^2\,k_{\min}^2}\int y^2|Df|^2.
\]

Therefore the kernel-complement gap is at least
4b (min y/max y)^2 kmin^2=4b exp(-4|epsilon|) kmin^2, with kmin=1 on a
2pi torus. The lapse is strictly positive and is unique up to its constant
normalization in this displayed elliptic problem. Integrating Ly=0 also
gives H[y]=0; the global lapse condition has not been omitted.

Further initial-data constraints in a larger action, their preservation, the
role of matter evolution after its initially resting state, and the full mixed
Cauchy problem still require derivation. No stationary cosmological solution
or all-source/global-in-time theorem is inferred from one valid slice.

## C. IC active-pin physical chart and gradient-coefficient repair

On a separate request from the proof agent, the reviewer read section 6 and
the nonlinear-gradient-repair subsection of `ic27_bridge/REPORT.md`, together
with the corresponding physical-chart part of `check.py`. This audit accepts
the displayed algebra **conditional on the supplied unitary matter equations
and reduced action**, rather than independently deriving that full action.

Using T_B=-R_p/(2vp), pdot=-2Hp and the supplied R_p flow gives
T_Bdot=Psi-deltaS. Substituting deltaS=2v Psi/B+D_c/(2B) recovers the reported
clock flow. Differentiating D_c=(delta_rho+3H J)/p while retaining
Hdot=-(3/2)L rhoP and the matter equations gives
D_cdot=-H D_c+6av rhoP T_B-exp(2S0)J_B. The cancellations of Hdot and the
redshifting wave number were checked directly, not inferred from a scalar
frequency. The other chart relations agree with these identities.

Eliminating Psi and J_B to obtain a local second-order system requires
2v/B-1!=0 and exp(2S0)>0; the stated domain a>0 and 0<B<2v supplies this.
The chart is for p!=0 only. The resulting principal diagonal is the stated
2av(2v/B-1), exp(2S0)w_f, with no missed wave-number principal mixing.
Initial-data/support statements apply to the specified physical chart and
its constraints; this algebra alone is not an arbitrary-source retarded
response theorem.

Replacing B_old by b exp(S) in the actual gradient term gives the same
lapse Euler equation and positive-y factorization audited in section B.
It uses an S-independent A_field and holds the spatial geometry fixed in
that variation. It is an explicit new action term, not a redefinition of
the old B. Finally, with v=exp(S)beta, a=exp(S)a0, B=b exp(S), the physical
speed is 2a0 beta(2beta/b-1). The choice ell=a0=1/(12beta), b=beta gives
exactly 1/6 and respects a0=1/(6beta)-ell.

These checks do not establish the active/pin-off transition, full functional
constraint brackets, pressureless-matter limit, additional matter sectors,
or nonlinear criterion-B evolution. The report states those remaining
obligations explicitly.
