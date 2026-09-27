# CD26-2: degenerate lapse velocity, source response, and an integrated penalty

Date: 2026-09-26. Requested checkpoint base: `c8bb508131a7cc72d0cfbb0313c5b79db7189ed2`.
This is a new construction attempt. It does not edit the recipe or success
contract, or replace the previous campaign's conclusions within their hypotheses.
The repository advanced concurrently; each run records its actual HEAD and
unchanged source hashes. All work here is confined to this directory.

**Concurrent target revision:** during this attempt, external commit
`9092fc0fd02b904e87c708971335cd63adb18151` changed the operative spec to `nu_mono`
and criterion B, which allows instantaneous leafwise terms subject to
well-posedness. The verified new spec SHA256 is
`851e44ab8f8a67f2779f16aa01945b149e62d30a7292b73e7ca2419c2b4e0390`.
The exact-exponential AQUAL calculations here retain the original pinned target
as a named research branch. Their instantaneous-tail obstruction is a
criterion-A result, not an automatic failure under revised criterion B.
Negative kinetic/stiffness and preferred-frame problems are separate issues.

## Result and scope

Allowing a degenerate lapse velocity genuinely enlarges the previous kinetic
family. Its regular frozen scalar block has one propagating pole and admits
healthy, subluminal, nontrivially sourced positive-response cells. An explicit
nonlinear spatial penalty can implement their direction-dependent coefficients.
These are constructive results, not a completed gravitational theory.

Three limitations are established separately:

1. On the negative-response branch `E<0`, cancellation of the tested instantaneous
   tidal contact is incompatible with a healthy surviving scalar, even with the
   additional lapse mixing `s`.
2. The positive-response cells leave the moving-source coefficient
   `alpha1=-4 E_infinity` unchanged when the vector sector and matter metric are
   Einstein's. Lapse mixing can cancel `alpha2`, but cannot cancel this `alpha1`.
3. A distinct local scalar/lapse gyroscopic term adds a second scalar pole. A
   gyro constrained to preserve one mode changes its infrared inertia but has
   the original high-momentum limit.

These are statements about the displayed action family, regular frozen
coefficients, and specified sources. In particular, exact exponential AQUAL
does **not** by itself force negative `E` after the bare/measured Newton-constant
normalization is allowed to vary. A wave-speed bound is also not a general
three-dimensional causal-support theorem.

## 1. Same action, additional lapse velocity

Use Fourier spatial momentum `k!=0`, physical potentials `psi,phi`, scalar shift
`beta`, and auxiliary `U`. At frozen constant coefficients let

\[
 K=3\dot\psi-k^2\beta,\qquad
 W=r\dot U+s\dot\phi,\qquad
 T=2+3B,\qquad \kappa=2T/B.
\]

The quadratic density is

\[
\begin{split}
L={}&-6\dot\psi^2+4k^2\beta\dot\psi
 -BK^2-2T K W-3T W^2\\
 &+k^2[2\psi^2-4\phi\psi+E\phi^2-\zeta(U+\phi)^2]
 -R\phi+\dot R\beta-\Pi\psi.
\end{split}
\]

This extends the previous `check_rankone.py` by `s`, rather than retuning `r`.
It is the scalar expansion of the trace factorization

\[
 K_{ij}K^{ij}-(1+B)K^2-2T K(rV_U+sV_N)
 -3T(rV_U+sV_N)^2
 =K_{\rm TF}^{ij}K^{\rm TF}_{ij}
 -(B+2/3)[K+3rV_U+3sV_N]^2.
\]

Here the trace sign must be chosen consistently with the displayed perturbation
convention. `V_U=n^mu partial_mu U`, `V_N=n^mu partial_mu ln N`, and
`N=(-partial T_clock squared)^(-1/2)` give spacetime-scalar realizations using a
clock foliation. The identity establishes velocity degeneracy, not closure of
the nonlinear Hamiltonian constraints or the allowed physical classification of
the surviving clock mode.

There is also an exact off-shell statement, independently checked in
`check_offshell.py`. Let `Q=B+2/3`. With the **standard ADM sign**
`K_ADM=(h^ij hdot_ij-shift terms)/(2N)=-K_display`, the matching density is

\[
 K_{\rm TF}^{ij}K^{\rm TF}_{ij}
 -Q(K_{\rm ADM}-3rV_U-3sV_N)^2.
\]

The six trace-sector coefficients are respectively
`-Q`, `+2(2+3B)r`, `+2(2+3B)s`, `-3(2+3B)r^2`,
`-6(2+3B)rs`, and `-3(2+3B)s^2` multiplying
`K_ADM^2,K_ADM V_U,K_ADM V_N,V_U^2,V_U V_N,V_N^2`.
The Einstein baseline trace coefficient `-2/3` is included in `-Q`.
In the displayed opposite trace convention the two mixed K coefficients
change sign, with all conclusions unchanged.

The trace Hessian is
`-2Q (1,-3r,-3s)^t (1,-3r,-3s)`, of rank one for `Q!=0`, with null vectors
`(3r,1,0)` and `(3s,0,1)`. Together with the five Einstein traceless velocities,
the full metric/lapse/U velocity Hessian has rank six out of eight. Positive
lapse and invertible spatial metric preserve this rank under the change to
coordinate velocities. This holds off shell on arbitrary backgrounds for
constant `r,s,B`; it does not require shift elimination or a Fourier mode.

Write `nu=ln N` and `pi=h_ij pi^ij`. Direct differentiation gives the exact
primary relations

\[
 p_U+2r\pi=0,\qquad p_\nu+2s\pi=0.
\]

The invertible conformal coordinate
`hbar_ij=exp[-2(rU+s ln N)] h_ij` has scalar trace perturbation
`v=psi+rU+sphi`, explaining the same degeneracy in field variables. A spatial
penalty with no velocities preserves these primary relations. Their time
preservation, secondary constraints, Poisson brackets with the Hamiltonian and
matter, and final physical field count are not inferred from rank alone.

Covariance requires terms that a zero-gradient frozen calculation omits. On a
static background with `U0=-ln N0` and `a_i=partial_i ln N0`,

\[
 r\delta V_U+s\delta V_N
 =r\delta\dot U+s\delta\dot\phi+(r-s)a_i\delta N^i
\]

in local units `N0=1`. The shift/background-gradient term, lapse factors,
connection terms, and field-dependent coefficient variations must be retained
in a full background calculation. The formulas below are the supplied frozen
block and its principal local approximation, not that missing calculation.

At zero frequency the independent equations give
`psi=phi`, `U=-phi`, and

\[
 \phi=-{R\over 2k^2(2-E)},\qquad
 {\phi\over\psi_N}={2\over2-E},\qquad
 \psi_N=-{R\over4k^2}.
\]

Thus adding these velocities preserves both the static response and no slip.

## 2. Joint elimination and the exact source transfer

Define `v=psi+rU+sphi`, `delta=r-s`, and

\[
\begin{split}
D={}&E(\zeta-2r^2)+2r^2\zeta+4r^2
 -4r(s+1)\zeta+2\zeta s^2+4\zeta s\\
 ={}&E\zeta+2(2-E)r^2+2\zeta\delta^2-4\zeta\delta.
\end{split}
\]

Shift elimination gives
`k^2 beta=(kappa/2) vdot+Rdot/(2B k^2)`.
The vacuum physical density is

\[
 L_{\rm phys}=\kappa\dot v^2-
 {2\zeta(2-E)\over D}k^2v^2,
 \qquad c_s^2={2\zeta(2-E)\over\kappa D}.
\]

This joint reduction does not spuriously exclude `E=zeta`. Assumptions are
`E!=2`, `zeta!=0`, `D!=0`, `B!=0`, and `kappa>0`; special singular branches are
not analyzed by inverting this block.

For a conserved planar generator `R=-k^2 F`, `Pi=qR`,
`q=omega^2/k^2`, set

\[
 A=\begin{pmatrix}2&-2&0\\-2&E-\zeta&-\zeta\\0&-\zeta&-\zeta\end{pmatrix},
 \quad a=(1,s,r)^t,\quad b={\kappa q\over2}a-qe_\psi-e_\phi,
 \quad h=a^tA^{-1}a={D\over2\zeta(E-2)}.
\]

The fully sourced solution and physical tidal response are

\[
 X=-{R\over2k^2}\left[A^{-1}b-
 {\kappa q A^{-1}a(a^tA^{-1}b)\over1+\kappa qh}\right],
\]
\[
 {\mathcal T\over R}=-{1\over2}\left[b^tA^{-1}b-
 {\kappa q(a^tA^{-1}b)^2\over1+\kappa qh}\right]+{q\over2B},
 \quad\mathcal T=-k^2(\phi+\dot\beta)-\omega^2\psi.
\]

The unreduced Euler equations and this physical-metric observable are checked
independently in `check_lapse.py`. The determinant lemma gives exactly one
regular pole, `1+kappa qh=0`. Polynomial division separates a degree-two contact
polynomial from that pole. The leading coefficient is

\[
 c_2={E r^2-\zeta(r-s)^2\over2D}.
\]

For a smooth compact generator `F`, this term is
`-c2 omega^4 F/k^2`; it has instantaneous inverse-spatial support. The lower
`q` and constant contact terms act locally on this particular generator. A
healthy retarded pole with metric-cone speed cannot cancel its instantaneous
inverse-spatial term. Cancellation of `c2` is necessary in this source test,
not a sufficient theorem for all conserved three-dimensional sources.

On the cancellation locus, a useful polynomial identity avoids fragile case
splits:

\[
 Er^2=\zeta\delta^2\quad\Longrightarrow\quad
 ED=\zeta(E-2\delta)^2,
 \qquad c_s^2={2E(2-E)\over\kappa(E-2\delta)^2}.
\]

For `E<0`, regularity forces the squared denominator to be nonzero, so this
speed is negative. This extends the old obstruction to arbitrary lapse mixing
`s`, including the special cancellation cases `r=0` and `r=s`.

For `0<E<2`, take `r=1,s=2,zeta=E,B=1`. Then

\[
 D=(E+2)^2,\quad v_{\rm static}=2\phi,\quad
 c_s^2={E(2-E)\over5(E+2)^2}\in(0,1/40],
\]
\[
 {1\over40}-c_s^2={(3E-2)^2\over40(E+2)^2}.
\]

This is a nontrivially sourced healthy cell, not the previous `r=1,s=0`
static-decoupling example.

## 3. Nonlinear static integration, normalization, and coefficient jets

The root's independent normalization parameter `C` gives

\[
 F_C(a)=2(1-C)|a|^2+4C a_0^2[1-(1+x)e^{-x}],\qquad x=|a|/a_0.
\]

Combined with the Einstein static term this yields
`-2 C a0^2 G(x)`, where
`G=x^2+2(1+x)exp(-x)-2`, and measured `G_N=G_bare/C`.
Its Hessian eigenvalues are `2 E_T,2 E_L`, where

\[
 E_T=2[1-C(1-e^{-x})],\qquad
 E_L=2[1-C(1+(x-1)e^{-x})].
\]

The bound `0<C<1/(1+exp(-2))` gives `0<E_i<2` for every `x>0`.
Consequently the fixed-normalization negative-E result is not a universal
obstruction to this exact interpolation law.

Choosing independent isotropic constants `zeta,r,s` cannot generally satisfy
the cancellation condition for distinct `E_T,E_L`. The explicit nonlinear
penalty suggested by the root resolves that tangent-coefficient issue:

\[
 L_{\rm pen}=-{r^2\over2\delta^2}w^i
 [\operatorname{Hess}_a F_C(a)]_{ij}w^j,
 \qquad w=D U+a,\quad r\ne0,\quad\delta\ne0.
\]

At `w=0` the penalty and its first variation vanish, and its second variation
gives exactly `zeta_i=r^2 E_i/delta^2` in both directions. The Hessian here is
with respect to the acceleration vector, not a spacetime second derivative.
Away from zero gradients, the density still depends on first spatial
gradients; variations of its coefficients introduce the corresponding field
jets and must not be dropped.

There is a real zero-gradient regularity problem: `F_C` is C2 but generally
not C3, since
`F_C=2|a|^2-(4C/(3a0))|a|^3+O(|a|^4)`.
The raw Hessian penalty is generally not C1 at `a=0,w!=0`. It has a cusp, for
example along `a=t e1` with a fixed perpendicular nonzero `w`.

A first constructive integration removes that first-variation cusp:

\[
L_{\rm pen}^{\rm int}=-{r^2\over\delta^2}
 [F_C(a+w)-F_C(a)-\nabla F_C(a)\cdot w].
\]

Because `F_C` is C2, this integrated density is C1 globally. It retains exactly
the previous second variation at `w=0`, while accounting for all nonlinear
coefficient jets. The integral identity

\[
 F_C(a+w)-F_C(a)-\nabla F_C(a)\cdot w
 =\int_0^1(1-t)w^t H_{F_C}(a+tw)w\,dt
\]

shows positivity and a uniform quadratic lower bound when `C` is in the
strict range above. With fixed boundary/harmonic data admitting `U=-ln N`,
strict convexity in `DU` makes `w=0` the unique fixed-metric static solution.
Off-branch second derivatives at `a=0` can still fail for this asymmetric
Bregman version. The root's subsequent symmetric completion improves it:

\[
 \boxed{L_{\rm pen}^{\rm sym}=-{r^2\over2\delta^2}
 [F_C(a+w)+F_C(a-w)-2F_C(a)].}
\]

This is globally C2 by composition with the C2 radial primitive, including
off-branch configurations at zero acceleration. Its first variation vanishes
at `w=0`, and its quadratic term is again exactly
`-r^2 w^t H_F(a) w/(2 delta^2)`. In particular this improvement does not require
a C3 primitive. Since `F_C` is even, its bracket also equals
`F_C(DU+2a)+F_C(DU)-2F_C(a)`. Let
`m=4[1-C(1+exp(-2))]>0`. Since `H_F>=m I`, the symmetric
difference has the direct representation

\[
 \int_{-1}^1(1-|t|)w^tH_F(a+tw)w\,dt\ \ge m|w|^2.
\]

The symmetric bracket is strictly convex in `w` at fixed `a` because its Hessian is
`H_F(a+w)+H_F(a-w)>=2m I`. Consequently it has the same unique auxiliary
static solution, with the stated boundary/harmonic data. Within the displayed
nonrelativistic weak-field static density this preserves exact general-source
AQUAL after elimination and gives an actual nonlinear density;
it does not use a spherical QUMOND substitution. It is the preferred completion
within this attempt. Its third derivatives need not exist at zero acceleration.
The static convexity argument does not supply full gravitational constraint
closure, a field classification, or a finite-background propagation theorem.
The positive penalty energy is bounded below by
`r^2 m |w|^2/(2 delta^2)` and has `w`-Hessian at least
`r^2 m I/delta^2`. This does not assert joint convexity in the metric and
acceleration variables; the action contains the negative of this penalty.

## 4. Preferred-frame response: what can and cannot be tuned

The independent moving-source calculation follows the local, previously
derived source/boost pipeline in
`real_research/g03_audit_2026/L333_c2_channel_carries_the_phantom.py:137-198`.
Use `R=gamma M`, `Pi=R v^2`, the conserved longitudinal current, and the
unchanged transverse shift `S/J_T=-16 pi G_bare/k^2`. The exact boost and
Fourier Jacobian are included before expanding to order `v^2`.

Normalized by `8 pi G_N M/k'^2`, the rest-frame response is

\[
 1+2E\,v^2+\alpha_2 v^2\cos^2\theta+O(v^4),
 \qquad\alpha_1=-4E,
\]
\[
 \alpha_2=\kappa\left[{(1-\delta)^2\over2-E}-(1-\delta)\right]
 +(2-E)(1/B+2)-1
 ={\kappa(E-2\delta)^2\over4(2-E)}-{E\over2}.
\]

Setting `r=s=0` reproduces the previous khronometric expression
`alpha2=E(E-B+2EB)/(B(2-E))`, an independent sign/convention control.
The transverse direction has `omega=0`, so scalar velocity changes cannot
alter `alpha1` while the static metric and vector sector are fixed.

On the contact-free locus,

\[
 \alpha_2={E\over2}(c_s^{-2}-1).
\]

Thus positive-E subluminal cells have nonnegative `alpha2`; its cancellation
is possible at the luminal values
`delta=E/2 +/- sqrt(E(2-E)/(2 kappa))`.
This is a constructive compatibility condition. It leaves `alpha1=-4E`.
The high-acceleration normalized exact-law branch has `E_infinity=2(1-C)`,
so `alpha1=-8(1-C)`. This architecture alone does not cure that residual.
No observational limit is newly assumed or re-certified here.

## 5. A distinct local gyroscopic route

A genuine lower-order local extension is
`gamma [U V_N-ln N V_U]`. Up to a total derivative, its frozen quadratic form
is a phi/U antisymmetric velocity coupling. With the convention that its
Fourier matrix is `i omega gamma G`, `G_phi,U=1=-G_U,phi`, the determinant is

\[
 -\kappa\gamma^2\omega^4
 -(\kappa k^4D+2\gamma^2k^2)\omega^2
 +2\zeta(2-E)k^6.
\]

For nonzero regular `gamma,kappa`, the quartic coefficient cannot vanish.
It introduces a second scalar pole and fails the one-surviving-scalar
requirement. A large pole mass is not a proof that this extra mode is absent.

More generally, a one-mode-compatible gyro can couple `vdot` only to the two
algebraic variables `n`. For
`L=kappa vdot^2+2 g^t n vdot+k^2(av v^2+2v f^t n+n^t C_n n)`,
joint elimination gives

\[
 \kappa_{\rm eff}(k)=\kappa-{g^tC_n^{-1}g\over k^2},
 \qquad A_{\rm eff}=a_v-f^tC_n^{-1}f.
\]

The exact determinant verifies one pole for regular `C_n`. This local
lower-order route can affect finite momentum stability, but its UV limit
returns the trace/lapse kinetic block. It therefore cannot cancel an existing
nonzero UV inverse-spatial contact across all momenta on the negative-E
branch. This is not an exclusion of arbitrary higher spatial derivative or
momentum-dependent degeneracy architectures. Covariant K/scalar realizations
can also produce shift and static terms; any compensators and their source
response must be derived from one action.

## 6. Computation and formal evidence

`check_lapse.py` checks original action variations, the shift reduction, the
explicit source solution, static gain/no slip, determinant/pole count,
contact division, and constructive-cell identities with exact SymPy arithmetic.
`check_ppn_gyro.py` independently evaluates the moving-source boost and both
gyroscopic determinant structures. No random scan or large simulation is used.

The initial lapse runs reached explicit resource caps while expanding
multi-parameter polynomial division, after passing every residual they
reached. They are retained as failed/incomplete executions, not successes.
Original inputs are preserved under `archive/`; the final implementation uses
independent scalar contractions for the exact division to avoid this expression
swell. This changes computational organization, not the action or assertion.

The Lean source `PushLapse20260926.lean` formalizes real-algebra consequences of
the displayed coefficients. It does not formalize action variation, physical
mode classification, PDE causal support, the integrated penalty's regularity,
or a complete PPN theorem. The first development compile found an insufficiently
explicit denominator rewrite; its archived source is not accepted evidence.

Accepted run identifiers, source hashes, logs, and final validation results are
recorded in `EVIDENCE.md` after the bounded runs complete.
