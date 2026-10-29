# MC27: exact kinetic realizability versus a dynamical pressure closure

Date: 2026-10-27. Requested checkpoint: `4aea352e6bf1ee7791a7d2b5ef01340b3e8ca709`.
Live repository; this route changes only `kinetic_closure/`. The input
`../TARGET.md` had SHA256
`6557b82c6b3fdfd823db1eb133d857254e17757645d75498b01ac2fa79aae8ef`.

**Verdict on the requested full derivation: incomplete.** A positive isotropic
distribution with finite local velocity moments can give an *exact* logotropic
inner equilibrium, including the exact quarter-density core coefficient. A
constructive example is proved below. Its stress amplitude remains free, and
neither Vlasov evolution nor the equilibrium construction supplies the required
time-dependent pressure closure or selects that amplitude from Lambda.

The construction is not the lowered-tail family in `../finite_tail/`. No
claim of literature novelty is made. The analytical arguments here are new
route work and self-reviewed; the independent quadrature is only a finite
implementation check. The proof-audit skill was applied to the proposed arrows
from equilibrium to closure, finite moments to impossibility, and fluid to
kinetic marginal stability. The literature-check skill was used on the cited
source's precise stability and divergent-pressure statements.

## 1. Objects, conventions, and the exact moment obstruction

Use a nonrelativistic mass distribution `f(t,r,v) >= 0`. Its velocity moments are

\[
\rho=\int f\,d^3v,\quad \rho u_i=\int v_i f\,d^3v,\quad
\Pi_{ij}=\int w_iw_j f\,d^3v,\quad
Q_{ijk}=\int w_iw_jw_kf\,d^3v,\quad w=v-u.
\]

Write `q_i=Q_{jji}/2`, `p=tr(Pi)/3`, `theta=div u`, and `D=partial_t+u.grad`.
The Vlasov equation with an acceleration independent of velocity gives exactly,
where the required moments and boundary integrations exist,

\[
D\rho=-\rho\theta,\qquad
D\Pi_{ij}+\Pi_{ij}\theta+\Pi_{ik}\partial_k u_j
+\Pi_{jk}\partial_k u_i+\partial_kQ_{ijk}=0.
\tag{1}
\]

The force terms cancel from the central second-moment equation. If the stress
is instantaneously isotropic, its trace gives

\[
Dp+\frac53p\theta+\frac23\nabla\cdot q=0.\tag{2}
\]

If `p=p(rho)` is also imposed dynamically, (2) requires

\[
\nabla\cdot q=\frac12[3\rho p'(\rho)-5p]\theta.
\tag{3}
\]

Thus `p=A ln(rho/rho_ref)` with fixed `A,rho_ref` requires
`div q=(3A-5p)theta/2`. With zero heat flux, compression instead gives
`p/rho^(5/3)` constant along the flow. Moreover, the traceless part of (1)
requires `(partial_k Q_ijk)^TF = -2p S_ij`, where `S` is the traceless symmetric
velocity gradient, if isotropy is to persist. A scalar equilibrium barotrope
does not provide either third-moment condition. Shell crossing alone supplies
neither condition.

There is no pointwise algebraic obstruction to finite moments and a prescribed
positive pressure: a Gaussian with variance `p(rho)/rho` realizes any `p>0`.
That is not yet a common stationary function of particle energy, a solution of
the coupled spatial problem, or an evolution law. The stronger construction
below addresses a common stationary `f(E)`.

## 2. Ergodic equilibrium and the scope of the divergent-tail obstruction

Let `E=v^2/2+Phi`, `u=0`, and `f=f(E)`. The potential includes any specified
velocity-independent external contribution. A stationary distribution of this
form solves the stationary Vlasov equation. Its moments are

\[
\rho(\Phi)=4\pi\sqrt2\int_\Phi^{E_b}f(E)(E-\Phi)^{1/2}\,dE,
\quad
P(\Phi)=\frac{8\pi\sqrt2}{3}\int_\Phi^{E_b}f(E)(E-\Phi)^{3/2}\,dE.
\tag{4}
\]

Here `E_b` may be infinity; all limiting differentiations need the displayed
moments/boundary terms to exist. Finite pressure gives the exact identity
`dP/dPhi=-rho`. Hence on any exact-log interval

\[
\frac{dP}{d\ln\rho}=A>0
\quad\Longrightarrow\quad
\rho'(\Phi)=-\frac{\rho^2}{A}
\quad\Longrightarrow\quad
\rho(\Phi)=\frac{A}{\Phi-\Phi_*}.\tag{5}
\]

If this is required for **every** `Phi>Phi_*`, with a common ergodic distribution
and no confining cutoff, right-Abel inversion uniquely gives

\[
f(E)=\frac{3A}{8\pi\sqrt2}(E-\Phi_*)^{-5/2}.\tag{6}
\]

For example, substituting (6) in (4) uses
`B(3/2,1)=2/3` and reproduces (5). Invertibility follows by differentiating the
density once, applying the Abel integral a second time, using
`B(1/2,1/2)=pi`, and differentiating the resulting cumulative integral of `f`.
These steps can be justified by nonnegative Tonelli integrals on truncated
intervals followed by limits. Formula (6) has `f~v^-5`, so the pressure integral
has the logarithmically divergent tail `v^4 f dv ~ dv/v`. Its kinetic energy
density is `3P/2`, which diverges too. The global-family requirement therefore
has no positive finite-second-moment realization under these hypotheses.

This is **not** a no-go theorem on a finite potential interval. Data on that
interval do not fix the Abel inversion's higher-energy completion. Nor can an
exact log law with fixed `A>0` continue to a regular vacuum edge: kinetic
pressure is nonnegative and approaches zero with density at the compact edge,
while an absolute `A ln(rho/rho_ref)` becomes negative as `rho -> 0`. The exterior
must change its equation of state, be confined by a boundary, or acquire
additional nonkinetic stress.

## 3. Constructive finite-energy exact-log inner family

Take independent constants `A>0` (pressure units), `Delta_m>0` (specific energy
units), and a potential offset `Phi_*`. Define

\[
x=\frac{\Phi-\Phi_*}{\Delta_m},\qquad \rho_m=\frac{A}{\Delta_m},
\qquad \rho(\Phi)=\rho_m R(x),
\]

\[
R(x)=\begin{cases}
x^{-1},&0<x\leq1,\\
(3-x)^2/4,&1\leq x\leq3,\\
0,&x\geq3.
\end{cases}\tag{7}
\]

`R` and `R'` agree at both joins. It is `C1`, positive on `(0,3)`, decreasing,
and convex. Its almost-everywhere second derivative is `2/x^3` on `(0,1)`,
`1/2` on `(1,3)`, and zero beyond. There are no delta functions in `R''` because
`R'` is continuous. `R''` has downward jumps at 1 and 3.

Put `e=(E-Phi_*)/Delta_m` and

\[
f(E)=A\Delta_m^{-5/2} F(e),\qquad
F(e)=\frac{1}{\sqrt8\pi^2}\int_e^3
\frac{R''(s)}{\sqrt{s-e}}\,ds\quad(0<e<3),\qquad F(e)=0\ (e\geq3).
\tag{8}
\]

Only energies `e>=x0>0` are accessed by a halo whose potential minimum is `x0`.
No claim is made about an extension through the formal singularity `e=0`.
`F>0` inside its support. Every local velocity moment is finite for each fixed
`x>0`, because velocities satisfy `v^2 <= 2 Delta_m(3-x)` and `F` is bounded on
that accessible energy interval.

Here is a direct proof of reconstruction, so no unverified inversion theorem
is a load-bearing citation. With `A=Delta_m=1`, substitute (8) in the first
integral (4) and swap the nonnegative integrals. The inner beta integral is

\[
\int_x^s(E-x)^{1/2}(s-E)^{-1/2}\,dE=\frac\pi2(s-x).
\]

All prefactors cancel to give
`rho_f(x)=integral_x^3 (s-x)R''(s)ds=R(x)`, using `R(3)=R'(3)=0`.
The corresponding pressure beta integral is `(3pi/8)(s-x)^2`, giving
`P_f(x)=(1/2)integral_x^3(s-x)^2 R''(s)ds=integral_x^3R(s)ds`.
Restoring units,

\[
P(\Phi)=A\begin{cases}
-\ln x+2/3,&0<x\leq1,\\
(3-x)^3/12,&1\leq x\leq3,\\
0,&x\geq3.
\end{cases}\tag{9}
\]

Consequently the inner interval `rho>=rho_m` has exactly

\[
P=A\ln(\rho/\rho_{\rm ref}),\qquad
\rho_{\rm ref}=\rho_m e^{-2/3}.\tag{10}
\]

This is the **absolute finite kinetic pressure**, not a subtracted divergent
pressure. The exterior completion fixes its offset. The particular quadratic
completion is a constructive choice, not a claimed dynamically selected law.
More generally an exterior `R=[(n+1-x)/n]^n`, `1<=x<=n+1`, `n>1`, matches the
same `C1` inner density and gives inner offset `n/(n+1)` instead of `2/3`.
Thus even within this elementary class the exterior information is not unique.

For a closed form in the chosen `n=2` example let `K=1/(sqrt8 pi^2)` and
`y=sqrt((1-e)/e)`. Then

\[
F(e)=K\begin{cases}
e^{-5/2}\left[\frac{y}{(1+y^2)^2}+\frac{3y}{2(1+y^2)}
+\frac32\arctan y\right]+\sqrt{3-e}-\sqrt{1-e},&0<e<1,\\
\sqrt{3-e},&1\leq e<3.
\end{cases}\tag{11}
\]

Monotonicity is exact, not just sampled. Write (8) as
`K integral_0^infty R''(e+t) dt/sqrt(t)` with `R''=0` above 3. The function
`R''` is nonnegative and nonincreasing, so this integral decreases with `e`,
strictly before the cutoff. `F` is continuous but not `C1` at `e=1`:
`F(1-epsilon)-F(1)=3K sqrt(epsilon)+O(epsilon)`. Therefore
`F'(1-epsilon) ~ -3K/(2 sqrt(epsilon))`. At the escape edge,
`F=K sqrt(3-e)` also has an unbounded negative derivative. A theorem requiring
a bounded or continuous derivative needs a smoothing argument; none is silently
assumed here. On both open pieces, `F'<0`. The leading behavior at `e->0+`
is `F~3/(8pi sqrt2) e^-5/2`, but this is at the excluded lower energy endpoint,
not an infinite-velocity tail of an individual finite halo.

## 4. The exact quarter-density core survives this completion

For a baryon-free Newtonian spherical equilibrium, neglecting the Lambda force
across the core, set `rho_c=rho(0)` and `theta=rho_c/rho`. Inside the log interval,
Poisson's equation gives

\[
\theta''+\frac2\xi\theta'=\theta^{-1},\qquad
\theta(0)=1,\quad\theta'(0)=0,\qquad
r=\sqrt{\frac{A}{4\pi G\rho_c^2}}\,\xi.\tag{12}
\]

If `0<x0<=1/4`, the quarter-density location has `x=4x0<=1`, entirely inside
the exact-log interval. It therefore has the same dimensionless `xi_quarter`
as the untruncated logotropic core, and exactly

\[
\rho_c r_{1/4}=\xi_{1/4}\sqrt{\frac{A}{4\pi G}}.\tag{13}
\]

The value `xi_quarter=5.84477267596` is inherited from `../TARGET.md`, not
recomputed by this route. Equation (13) is conditional on a regular
self-consistent spherical solution reaching the matching interval; the root
route separately checks the global Poisson solution. Baryons, anisotropy, and
a non-negligible Lambda force alter (12). Exact inner equilibrium has now been
realized with finite kinetic moments; **A still is an arbitrary positive
parameter**. Specifying the desired surface density and solving (13) for A
would impose its coefficient, not derive it.

## 5. Entropy and the fluid-versus-collisionless stability distinction

Fine-grained Vlasov evolution conserves each Casimir `integral C(f) d^3r d^3v`
under the usual no-flux/integrability assumptions. It neither chooses a unique
coarse entropy nor erases the initial phase-level information. At fixed mass
and kinetic energy, maximization of ordinary Boltzmann entropy instead yields
a Gaussian in velocity; it does not derive (8). Choosing another entropy or a
phase-level prior can generate other stationary distributions, but those
choices and their normalization must be supplied or dynamically derived.

Even when an ergodic equilibrium has `P=P(rho)`, its kinetic perturbations need
not obey that scalar barotrope. Dynamically accessible perturbations preserve
all Casimirs and may develop anisotropic stress and third moments. Varying a
family parameter such as the cutoff or amplitude generally changes those
invariants. A zero derivative of a fluid mass curve does not establish a
neutral dynamically accessible kinetic mode.

Source check: Chavanis, *Polytropes, logotropes, the universal value of the
surface density of dark matter halos, and the value of the cosmological
constant*, [arXiv:2603.21302v1](https://arxiv.org/html/2603.21302v1), checked
2026-10-27. Section III.3, equations (117)-(125), treats the uncut distribution,
its divergent kinetic pressure, subtraction, and a temperature-dependent
coefficient. Section III.6 states Antonov's sufficient implication: stable
barotropic fluid implies stable isotropic stellar equilibrium, not its converse.
Its examples explicitly separate the two stability ranges. Its final remark
distinguishes a sufficient energy-turning-point criterion from stronger kinetic
criteria and flags confinement subtleties. Thus a first fluid mass turning
point is **inapplicable as a necessary kinetic instability criterion** without
an additional closure argument. This checks the source's claim and its scope;
it does not independently certify its cited general stability theorems or apply
them through the derivative cusps in (11).

There is also an energy distinction. If a barotropic *fluid* energy density
`u(rho)` satisfies `P=rho u'-u`, the log law gives

\[
u(\rho)=-A\ln(\rho/\rho_{\rm ref})-A+C\rho.\tag{14}
\]

By contrast, isotropic nonrelativistic random kinetic energy is exactly
`u_kin=3P/2`. They are different functionals; a generalized kinetic free energy
is not the kinetic energy. Subtraction of an infinite pressure constant cannot
be taken as a finite stress-energy or vacuum equation of state without an
additional gravitational prescription. The compact construction avoids that
divergence but does not make the two functionals interchangeable.

## 6. Fixed-Lambda scaling excludes a coefficient from this parent alone

Consider exactly the Newtonian Vlasov-Poisson-Lambda equations

\[
\partial_t f+v\cdot\nabla_r f-\nabla_r\Phi\cdot\nabla_v f=0,
\qquad \nabla^2\Phi=4\pi G\rho-\Lambda c^2.
\]

For any `lambda>0`, define, at the same time coordinate,

\[
f_\lambda(t,r,v)=\lambda^{-3}f(t,r/\lambda,v/\lambda),\qquad
\Phi_\lambda(t,r)=\lambda^2\Phi(t,r/\lambda).\tag{15}
\]

Each Vlasov term scales by `lambda^-3`. The Laplacian in (15) equals the
original Laplacian at `r/lambda`; meanwhile `rho_lambda(t,r)=rho(t,r/lambda)`.
Thus the equations hold with the *same* `G,Lambda,c`. The moments transform as
`u_lambda=lambda u`, `Pi_lambda=lambda^2 Pi`, `q_lambda=lambda^3 q` at the
scaled position. In particular

\[
P_\lambda=\lambda^2P,\qquad A_\lambda=\lambda^2 A,\qquad
M_\lambda=\lambda^3M,\qquad
(\rho_c r_{1/4})_\lambda=\lambda\rho_c r_{1/4}.\tag{16}
\]

Finite support and any dynamically determined turnaround radius scale too.
The dimensionless ratio `A/(rho_Lambda c^2)` is not invariant. Therefore these
equations alone, with freely scaled initial/boundary data, cannot imply a
unique universal value for that ratio. This remains a local continuous
counterfamily if lambda is restricted to keep velocities nonrelativistic.

Scope: the transformation changes initial phase-space invariants; for example
`integral f^n d^3r d^3v` scales as `lambda^(6-3n)`. It does not exclude selection
by a specified primordial distribution, a microphysical scale, or a relativistic
horizon boundary. Such input breaks the symmetry and is the precise next
missing ingredient, not something already present in this parent system.

## 7. Claims and remaining obligations

| Claim | Evidence and scope |
|---|---|
| No automatic dynamical log closure | Exact moment equations (1)-(3); proved under finite-moment hypotheses |
| Uncut all-potential exact log density forces divergent pressure | Abel uniqueness and tail power count, section 2; restricted global-family no-go |
| Finite-moment exact-log inner family exists | Constructive (7)-(11), direct beta-integral proof; numerical cross-check in `run_001/` |
| The same quarter-density core coefficient can survive a finite exterior | Conditional equation (13); global spherical solve delegated to root |
| A fluid turning point necessarily selects the kinetic cutoff | Unsupported; sufficient fluid-to-kinetic implication cannot be reversed |
| Vlasov-Poisson-Lambda alone fixes the coefficient | Refuted for unrestricted scaled initial/boundary data by (15)-(16) |
| A dynamically selected finite-energy log closure and vacuum normalization | Not established |

The next useful physical claim must specify an interaction or initial-state
principle that both enforces the required moment evolution and breaks (15).
Choosing the finite completion, an entropy prior, or a core pressure from the
desired surface density does not yet supply that claim.
