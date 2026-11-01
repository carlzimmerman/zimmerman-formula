# Independent audit of the startup-energy reduction

Base checkpoint: **X48-TRANSPORT-2026-11-01-B**. Exact normalized
`ConvectiveCollapse` shell ODE, with the physical nonnegative-K domain.
Audited proof: `startup_energy_route.md`, SHA-256
`06630aecae84c9b618e84c1ddded3f2025f7a89f7dca634bbbb05f50d0e2380b`.
The shared checkout HEAD at the audit read was
`19ed7a5bc82c89938a1feceb445cc36735753b40`; content hashes below identify
the proof and source actually reviewed.

**Scoped verdicts.**

| Claim audited | Verdict |
| --- | --- |
| Exact positive-square signed-compression identity, equation (3) | **Proved as written**, on valid ordered geometry. |
| Homogeneous principal-graph penetration theorem, equation (6), for every `N>=32` and `0<=s<=.001` | **Proved as written**, for the scalar reference problem (5). |
| Exact full-system Duhamel reduction and `(NE) => C_i>4` on `i<=floor(N/4)`, `0<=s<=.001` | **Proved as a conditional implication**, assuming the actual solution has valid geometry and satisfies (NE). |

No error was found in the scoped signs, normalizations, special boundary
diagonal, or constants. The audit does **not** establish (NE), a uniform
compression bound for the full system without (NE), or an unconditional
mesh-uniform entropy floor. The scalar graph theorem cannot substitute for
the nonlinear remainder estimate.

## 1. Reconstruction from the actual shell equations

From `SphericalCollapse.geometry` and `rhs`, in one-based indexing,

\[
 V_i={4\pi\over3}(r_i^3-r_{i-1}^3),\qquad
 \dot V_i=4\pi(r_i^2u_i-r_{i-1}^2u_{i-1}),
\]
\[
 \dot u_i={4\pi r_i^2\over\mu_i}(S_i-S_{i+1})
              -{Gm_i\over r_i^2},\qquad S_{N+1}=0.
\]

Here `r_0=u_0=0`, `m_i=i dm`, `mu_i=dm` except
`mu_N=dm/2`, and `dm=(pi/3)/N`. The source law has `G=1`.
The signed variable is `x_i=-Vdot_i/V_i`; only after proving positivity may
one identify it with the nonnegative compression `C_i=(-theta_i)_+`.

For nonnegative K, the source stress is exactly

\[
 S_i=K_i\rho_i^2h_i+\kappa_i(x_i-2)_++\zeta_i x_i,
\quad \kappa_i={1\over2}\rho_iW_i h_i,
\quad \zeta_i=\kappa_i{K_i\over K_i+.01}.
\]

This uses all the pinned choices: `tau=1/2`, damping strength one,
`P0=rho_q=Kstar=1`. In particular the old source involves `(x-2)_+`,
not `x-2` on the negative-compression branch; the signed damping stress is
`+zeta*x`. The proof note preserves these distinctions.

## 2. Claim 1: the positive-square identity passes

Differentiating `x=-Vdot/V` gives

\[
 \dot x_i=x_i^2-{4\pi\over V_i}
 \left[2(r_iu_i^2-r_{i-1}u_{i-1}^2)
        +r_i^2\dot u_i-r_{i-1}^2\dot u_{i-1}\right].
\]

The gravitational part of the bracket is
`-G(m_i-m_(i-1))=-G dm`, including in the outermost cell.
It contributes `+4pi G rho_i`. Dividing the pressure force by the actual
nodal weights instead contributes

\[
 {a_i(S_{i+1}-S_i)-a_{i-1}(S_i-S_{i-1})\over V_i},
 \qquad a_i={(4\pi r_i^2)^2\over\mu_i}.
\]

Thus the Laplacian sign in (1) and (3) is correct: positive neighboring
stress increases x, and a positive local stress against a lower neighbor
can decrease x. The half outer node weight doubles `a_N`; it does not
change the gravitational mass difference.

For the kinetic completion put `r=r_i`, `q=r_(i-1)`, `u=u_i`,
`v=u_(i-1)`, and `D=r^3-q^3`. Since `x=-3(r^2u-q^2v)/D`,

\[
 \begin{aligned}
 x^2-{6(ru^2-qv^2)\over D}-{x^2\over3}
 &= {6\big[(r^2u-q^2v)^2-(ru^2-qv^2)D\big]\over D^2}\\
 &= {6rq(rv-qu)^2\over D^2}\ge0.
 \end{aligned}
\]

This proves exactly the displayed identity (3), with
`R_i=4pi*rho_i+x_i^2/3+square>=0`. At the center `q=0`, the square
vanishes and the kinetic contribution remains `x_i^2/3`; no undefined
central weight enters. The center convention `a_0=0` is sufficient.

The auxiliary old-heater-only threshold observation is also consistent:
at `x_i=2`, its own old stress is zero, neighboring old stresses and the
exterior stress are nonnegative, and the vector field points into `x_i>=2`.
This observation does not apply unchanged after restoring thermal pressure
and memory damping.

## 3. Claim 2: the reference graph and every explicit constant pass

### Reference bounds close before `.01`

Let `alpha=4^(1/3)`. The stated bounds on alpha and pi yield exact rational
certificates for the initial compression:

\[
 C_a^2>{21299\over768}
       =\left({21\over4}\right)^2+{131\over768},\qquad
 C_a^2<{26604\over875}<36.
\]

On a bootstrap interval with `rho_d<=2`, `x_d<=8`,

\[
 \dot x_d=4\pi\rho_d+x_d^2/3
       <{976\over21}<47.
\]

Consequently `x_d<6+.47<8` through `.01`, while

\[
 \rho_d\le e^{8s}\le{1\over1-8s}\le{25\over23}<2,
 \qquad
 \rho_d-1\le{8s\over1-8s}\le{200\over23}s<9s.
\]

The bounds are strict at a possible first exit, so continuation closes the
bootstrap. Dust compression stays positive, so the reference radius decreases
and `a(s)<=a(0)<1`.

The gate and viscosity bounds follow with no hidden mesh constant:

\[
 h_d\le3(\rho_d-1)^2\le243s^2,\qquad
 \kappa_d\le2h_d\le486s^2,\qquad
 \nu_d=\kappa_d+\zeta_d\le4h_d\le972s^2.
\]

The homogeneous K equation has original heating at most `24h_d` and
memory heating at most `32h_d`, hence
`Kdot_d<=56h_d<=13608s^2` and `K_d<=4536s^3<1` through `.01`.
Since `W_d>=1.5`, `rho_d<=2`, and `x_d<=8`,

\[
 0\le B_d={S_d\over\nu_d}
 \le x_d+{P_d\over\kappa_d}
 =x_d+{2K_d\rho_d\over W_d}<12.
\]

At zero, both numerator and denominator vanish; their ratio has the
claimed finite limit `C_a-2`. Prescribing that limit as boundary data is
legitimate for the finite-dimensional problem. It does not force the
interior initial values to equal the boundary limit. The boundary forcing
is multiplied by a coefficient vanishing at zero.

### The discrete rates have the stated normalization

On reference geometry,

\[
 V_i^d={4\pi a^3\over3N},\qquad
 {a_i^d\over V_i^d}=36aN^2(i/N)^{4/3}\quad(i<N).
\]

Thus the two jump rates are precisely those in the note. For `i<N`,

\[
 b_i^++b_i^-\le72\cdot972s^2N^2,\qquad
 0\le b_i^+-b_i^-\le48\cdot972s^2N.
\]

The last inequality uses
`z^(4/3)-(z-1/N)^(4/3)<=4/(3N)` on the unit interval. At the center
`b_1^-=0`; the proof does not require a ghost contribution there.

At row N the outward rate is **twice** `36nu_d*a*N^2` because
`mu_N=dm/2`. The proof does not apply the ordinary-rate formula to that
row. Instead, the whole scalar graph first gives `0<=w<=12`, after which
the ordinary graph on rows `1,...,N-1` uses `w_N<=12` as its right boundary.
This restriction is valid and avoids the doubled boundary coefficient.

For completeness, the full zero-boundary matrix has nonnegative
off-diagonal entries and diagonal `-(b_i^++b_i^-)`. Its row sum is zero
except at N, where it is `-b_N^+<=0`. This establishes positivity and
the infinity-norm contraction used later. Omitting the outward term in
that diagonal would give a different operator; the audited note retains it.

### The exponential barrier proves the strict numerical bound

For `E_i=exp[-lambda(1-i/N)]`, put `h=lambda/N`. The exact rate expression is

\[
 {\nu_d\mathcal L_dE_i\over E_i}
 =b_i^+(e^h-1)+b_i^-(e^{-h}-1)
 \le h(b_i^+-b_i^-)+{h^2e^h\over2}(b_i^++b_i^-).
\]

For `N>=32`, this gives exactly (8). Therefore
`12E_i exp[Psi(lambda)s^3/3]` is a supersolution on rows `i<N`;
it dominates zero initial data and has right boundary at least 12.
For lambda eight,

\[
 \Psi(8)=373248+2239488e^{1/4}
       <3359232<4000000,
\]

using `e^(1/4)<4/3`. The time exponent at `.001` is below `1/750`,
which is below the note's looser `1/500`. To certify its final displayed
strict inequality without relying on a decimal approximation, use
`e^3>sum_(n=0)^8 3^n/n!=89641/4480>20` and
`e^(1/500)<500/499`. Then

\[
 12e^{-6+1/500}<{12\over400}{500\over499}
 ={15\over499}<{1\over32}.
\]

For `i<=floor(N/4)`, `E_i<=e^(-6)`. These inequalities prove (6)
uniformly over the entire stated range, including nonmultiples of four.
Only this homogeneous scalar problem has been bounded here.

## 4. Claim 3: the Duhamel reduction and conditional implication pass

In this section the actual `w=x_d-x` differs from the scalar solution,
which the note renames `w^0`. The definition
`Slin_i=S_d-nu_d*w_i` uses a spatially constant reference stress and
viscosity, but an actual compression deviation.

The ghost prescription is essential:

\[
 w_{N+1}=B_d=S_d/\nu_d
 \quad\Longrightarrow\quad S^{lin}_{N+1}=0,
 \qquad \delta S_{N+1}=0.
\]

Consequently, including the center and outer row,

\[
 \mathcal L_dS^{lin}=-\nu_d\mathcal L_dw.
\]

Without that ghost convention a boundary forcing term would be missing.
With it, direct substitution gives

\[
 \begin{aligned}
 \nu_d\mathcal L_dw
 +(\mathcal L_d-\mathcal L_r)S^{lin}
 -\mathcal L_r\delta S
 &=-\mathcal L_r(S^{lin}+\delta S)\\
 &=-\mathcal L_rS.
 \end{aligned}
\]

Together with `wdot=R_d-R-L_rS`, this proves (9)-(10) exactly.
No derivative of `nu_d` is needed, because the evolved coordinate in this
identity is w, not stress. The full thermal pressure, memory stress,
heater coefficients, actual K, and moving geometry all remain inside the
specified remainder. This is an algebraic identity, not a smallness bound.

Let `A_N(s)` be the zero-exterior matrix verified above and `P_N(s,v)`
its positive contractive propagator. The scalar solution `w^0` accounts for
the nonzero boundary forcing. The actual initial deviation is zero, so
variation of constants gives exactly (11), with no additional initial or
boundary term. The right-hand ratio's finite zero-time extension and the
vanishing principal coefficient make the representation regular at zero.

The exact square identity supplies `R>=0` componentwise. The reference
bootstrap supplies `0<R_d<47`. Positivity and contraction then yield

\[
 \int_0^sP_N(s,v)(R_d-R)\,dv
 \le47\int_0^sP_N(s,v)\mathbf1\,dv
 \le47s\mathbf1.
\]

Thus the one-sided, localized upper bound in (NE) is sufficient. No
absolute-value estimate on that integral is needed. For every indicated
central cell and time, (NE) implies

\[
 w_i\le1/32+47/1000+1,
\]
\[
 x_i=x_d-w_i\ge C_a-1/32-47/1000-1
 >{33374\over8000}=4.17175>4.
\]

At s zero, `x_i=C_a>4` directly. On positive times this lower bound makes
signed x equal to the heater's positive compression C. It proves the
claimed `c=4`, `T=.001` compression hypothesis **if (NE) holds**.

This audit stops at that conditional conclusion. It does not independently
reaudit the subsequent source-driven entropy comparison or promote the
note's conditional epsilon formula to an unconditional floor theorem.

## 5. Exact unresolved obligation and audit scope

The missing input is precisely the upper bound in (NE) on the Duhamel
contribution of

\[
 (\mathcal L_d-\mathcal L_r)S^{lin}-\mathcal L_r\delta S
\]

for the actual solution, uniformly for `N>=32` through `.001`.
The identity, positivity of R, and scalar barrier do not bound this term.
Valid actual geometry is also required for the formulas; no uniform
geometry estimate is created by the Duhamel identity itself.

The audit therefore supports the note's restricted status: an exact
reduction and a proved scalar theorem, with the nonlinear input still open.
No source modification, trajectory integration, grid extrapolation,
continuum theorem, or unproved finite-speed assertion was used.

Review provenance: independent derivation by the delegated obstruction
auditor from the proof and raw source; a separate bounded arithmetic pass
checked the rational and exponential constants from the displayed
definitions. That arithmetic pass received no author verdict. Mathematical
self-proofreading covered this report's definitions, signs, indices,
delimiters, and scope statements; no change to an audited proof note was made.

## 6. Pinned inputs and verification

Paths below are relative to `entropy_transport/`.

| Input | SHA-256 |
| --- | --- |
| `floor_theorem/startup_energy_route.md` | `06630aecae84c9b618e84c1ddded3f2025f7a89f7dca634bbbb05f50d0e2380b` |
| `floor_theorem/seed_route.md` | `752944eb3c0c7ff87007b5ca1c3f5a46bb768d8215645914ad6b211cebcd053d` |
| `convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `../collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `../material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |

Verification consisted of direct source/proof reads, the explicit algebra
and elementary inequalities displayed above, content hashing, and a tiny
exact-fraction arithmetic check in the separate constants pass. No evolution
tests or simulations were run. Only `STARTUP_ENERGY_AUDIT.md` is written by
this audit.
