# Short-time central seeding: exact reduction and remaining uniform estimate

Owner: delegated seed route. Base checkpoint: `X48-TRANSPORT-2026-11-01-B`.
Base Git revision: `0fe706856e8a897a9ab350be4931dbf36416ada4`.
Write scope: this file only. No evolution law or production code was changed.

**Status.** A central entropy floor is proved conditional on one mesh-uniform
short-time compression bound. The nonlinear, outward-only heat flux does not
require a separate seeding guard: a source-driven comparison solution handles
arbitrary heat redistribution along the actual valid geometry. The needed
compression bound has not been proved. Fixed-resolution positive seeding is
proved, but its interval need not be uniform in resolution. Neither this
failure of uniformity in the proof nor the free-surface calculation below
refutes the desired uniform central floor.

## Target and exact objects

Use the nonnegative, ordered-shell semidiscrete ODE of
`convective_transport.ConvectiveCollapse`, with equal cell masses
`dm=M/N`, `M=pi/3`, `N>=2`, and the parameters in the README:
`G=rho_q=Kstar=1`, `tau=1/2`, `D=1/10`, `alpha_v=1`,
`chi_d=chi_g=1/100`, `ell_g=1/10`. Initial data are
`rho=1/4`, `R=1`, `u=-r/4`, `K=0`.

The intended uniform conclusion requires fixed `f_c>0`, `T>0`, and
`epsilon>0`, independent of `N`, such that every cell intersecting the central
material mass fraction `f_c` has `K>=epsilon` at `t_a+T`. Preservation is
understood for later times for which the physical shell solution exists with
strictly positive shell volumes and centroid separations. This note proves a
conditional version, and an unconditional fixed-`N` version. It proves no
continuum convergence or global geometry theorem.

Write the actual evolution as

\[
 \dot K_i=Q_i(t)+H_i(t,K),\qquad
 H_i(t,k)=\frac{L_{i-1}(t,k)-L_i(t,k)}{dm\,W_i(t)},
\]

where `Q` is the sum of the original compression heater and memory-damping
heater, and all geometric coefficients in `H` are taken from the actual
solution. Both heaters are nonnegative. Faces are numbered so that `L_i`
lies between cells `i` and `i+1`; `L_0=L_N=0`.

## Exact dust phase and fixed-resolution seeding

The cold solution before activation is exactly homologous on every grid:

\[
 r_i(t)=a(t)(i/N)^{1/3},\quad
 a''=-\frac{\pi}{3a^2},\quad a(0)=1,\quad a'(0)=-\frac14,
\]
\[
 \rho_i=\frac1{4a^3},\qquad C_i=C_d=-3a'/a,\qquad
 (a')^2=\frac1{16}+\frac{2\pi}{3}(a^{-1}-1).
\]

At `a_a=4^(-1/3)`, the common density reaches one. The corresponding
compression is

\[
 C_a=\frac3{a_a}
 \sqrt{\frac1{16}+\frac{2\pi}{3}(a_a^{-1}-1)}
 =5.4145849604\ldots>4.
\]

Thus activation starts at the density crossing, independently of `N`:

\[
 t_a=\int_{a_a}^{1}
 \frac{da}{\sqrt{1/16+(2\pi/3)(a^{-1}-1)}}
 =0.5907973398405\ldots .
\]

For each fixed `N`, local ODE existence and continuity give `T_N>0` such
that geometry is valid and every `C_i(t_a+s)>=4` for `0<=s<=T_N`.
Decrease `T_N` if necessary so `T_N<=1/4`. Continuity yields
`rho_i>=exp(4s)>=1+4s`, and monotonicity of `h` gives

\[
 Q_i\ge4h(1+4s)
 =64s^2(3-8s),\qquad 0\le s\le T_N.
\]

The global minimum principle therefore proves

\[
 \min_iK_i(t_a+T_N)
 \ge64T_N^3(1-2T_N)>0.
\]

This floor persists while geometry remains valid. This is an exact statement
for every fixed `N`; it does not supply a common positive `T_N` or floor.

More precisely, the one-sided activation expansion is, for each fixed `N`,

\[
 K_i(t_a+s)
 =C_a^3(\tfrac12C_a-1)s^3+o_N(s^3),
 \qquad C_a^3(\tfrac12C_a-1)=271.0213132681\ldots .
\]

Indeed `rho_i-1=C_as+o_N(s)`, `h=3C_a^2s^2+o_N(s^2)`,
so the original heater is
`3C_a^3(C_a/2-1)s^2+o_N(s^2)`. The memory heater is higher order.
For fixed `N` the transport term is also higher order: `K=O_N(s^3)`,
`h_i h_j=O_N(s^4)`, and its instability gate vanishes at `K=0`.
The shared leading coefficient is not a uniform-remainder theorem.

## A source-driven comparison theorem removes the heat/guard obstacle

**Theorem (conditional seeding, exact at every fixed `N`).** On a compact
valid-geometry interval `[t_a,t_a+T]`, suppose the actual local heater obeys

\[
 Q_i(t_a+s)\ge q(s){\bf1}_{i\le J_s},\qquad q(s)\ge0,
 \qquad B(s)=\int_0^s q(v)\,dv.
\]

Then, for every integer `1<=J_c<=J_s<=N`,

\[
 \boxed{\quad
 \min_{i\le J_c}K_i(t_a+s)
 \ge B(s)\left(\frac{J_s-J_c+1}{N-J_c+1}\right)^3.
 \quad}                                                   \tag{S1}
\]

In particular no lower bound for a single exterior guard is required. The
same bound with `B(T)` holds at all later valid-geometry times, even if the
actual heater subsequently turns off.

**Proof.** Let `k` solve the auxiliary ODE using the actual geometry,

\[
 \dot k_i=q(s){\bf1}_{i\le J_s}+H_i(t_a+s,k),\qquad k_i(0)=0.
\]

At fixed geometry, a face luminosity is nondecreasing in its supplying
`k_i` and nonincreasing in its receiving `k_{i+1}`. For example, on
`k_i>k_{i+1}`, the derivative of the raw gate ratio
`(k_i-k_{i+1})/[chi_g+(k_i+k_{i+1})/2]` has these signs, and so does the
positive temperature-potential drop. Hence `H` is cooperative and
comparison gives `K_i>=k_i`.

The auxiliary solution stays nonnegative and nonincreasing in the radial
index. For the latter claim, at a first equality `k_i=k_{i+1}`, its shared
face flux is zero, and

\[
 (\dot k_i-\dot k_{i+1})\big|_{k_i=k_{i+1}}
 =q({\bf1}_{i\le J_s}-{\bf1}_{i+1\le J_s})
 +\frac{L_{i-1}}{dmW_i}+\frac{L_{i+1}}{dmW_{i+1}}\ge0.
\]

At an auxiliary global maximum there is no incoming flux, so
`max_i k_i<=B(s)`. Its entropy `S_k=sum_i dm*k_i^(1/3)` obeys

\[
 \frac{dS_k}{ds}
 \ge\frac{J_sdm\,q(s)}{3B(s)^{2/3}},
 \qquad S_k(s)\ge J_sdm\,B(s)^{1/3}.                 \tag{S2}
\]

The heat contribution has the exact nonnegative pairwise sign
`L(1/T_right-1/T_left)`. To justify (S2) through zeros, initialize the
auxiliary at `k_i(0)=eta>0`, use `max k<=eta+B`, integrate, then let
`eta` decrease to zero by finite-dimensional continuous dependence. This
gives (S2) without division by zero at activation.

For a descending auxiliary profile with `k<=B`,

\[
 S_k\le (J_c-1)dm\,B^{1/3}+(N-J_c+1)dm\,k_{J_c}^{1/3}.
\]

Combining this with (S2) proves (S1). After the seeding interval continue
the auxiliary with zero source. It remains descending, its maximum remains
at most `B(T)`, and its entropy is nondecreasing. The identical estimate
therefore persists, and comparison still applies since the actual source
remains nonnegative. QED.

This argument depends neither on a heat-flux derivative bound nor on
finite-speed heat transport. Time-dependent density weights cause no extra
entropy term because the entropy coordinate is `k^(1/3)`, independent of
the density.

## An explicit sufficient uniform compression lemma

Choose any fixed `c` with `2<c<C_a`. Suppose the following estimate is
proved for a common positive `T<=1/c`, on a prescribed wider central prefix:

\[
 C_i(t_a+s)\ge c,\qquad i\le J_s(N),\quad
 0\le s\le T,\quad N\ge N_0.                         \tag{UC}
\]

The density equation is exact, `dot rho_i=rho_i C_i`, on this interval;
therefore `rho_i>=exp(cs)>=1+cs`. A valid common source is

\[
 q(s)=c^3(\tfrac12c-1)s^2(3-2cs),\quad
 B(T)=c^3(\tfrac12c-1)T^3(1-\tfrac12cT).             \tag{S3}
\]

This uses only the original compression heater, so the memory damping can
only help. Formula (S1) now supplies a uniform seed whenever the ratio
`(J_s-J_c+1)/(N-J_c+1)` has a fixed positive lower bound.

For example take `c=4`, every `N>=2`, `J_s=ceil(N/4)`, and
`J_c=ceil(N/20)` (every cell intersecting the inner five percent). Then

\[
 \frac{J_s-J_c+1}{N-J_c+1}\ge\frac15,\qquad
 \boxed{\epsilon=\frac{64}{125}T^3(1-2T)>0.}          \tag{S4}
\]

Thus (UC) for every cell intersecting the central quarter proves an
explicit, persistent inner-five-percent floor for every `N>=2`. The rounding
bound follows from `J_s>=N/4`, `J_c<=N/20+1`, and
`N-J_c+1<=N`. At small `N` the source prefix includes the whole last cell
that intersects the central quarter: for example at `N=2` it is the first
half of the mass. The sharper discrete `+1` is legitimate because only the
first `J_c-1` cells need the separate maximum bound in the entropy estimate.
It avoids a finite-small-grid exception without replacing (UC) by a finite
collection of numerical checks.

## Why a sharp interior dust cone is not available

Once compression and density are active,

\[
 q_s=\rho W h(\tfrac12C-1),\qquad
 -\partial_\theta q_s=\tfrac12\rho Wh>0.
\]

Since `theta=div u`, the momentum term `-grad q_s` includes positive bulk
velocity diffusion. The memory bulk stress adds another such term. A
finite acoustic speed does not establish an exact postactivation region
unaffected by the boundary. The gate vanishes at activation, but becomes
positive immediately afterwards. This is already visible directly in the
semidiscrete equations, without invoking any external PDE theorem.

Let `s=t-t_a`, `a=a_a`, and

\[
 q_2=\frac92C_a^2(\tfrac12C_a-1)>0.
\]

All cells have `q_s=q_2s^2+o_N(s^2)`. The exterior stress is zero.
Consequently the free-surface node, whose weight is `mu_N=dm/2`, has
the following leading correction to continued dust motion:

\[
 u_N-u_N^{dust}=8a^2Nq_2s^3+o_N(s^3),
\]
\[
 \theta_N-\theta_N^{dust}=24aN^2q_2s^3+o_N(s^3).
                                                               \tag{S5}
\]

For each fixed `N`, the other node velocities have no `s^3` correction;
the exterior force is `4pi a^2 q_s/(M/(2N))`, and
`partial theta_N/partial u_N=3N/a`, which gives (S5).
It follows that a global-in-space continuity estimate with an `N`-independent
Taylor remainder cannot be inferred from local smoothness. The surface
stiffness is explicit. In particular a proof that simply continues the
globally homogeneous sphere past `t_a` is false.

The heuristic scale suggested by (S5) is `s~N^(-2/3)` for order-one
boundary compression changes, and the associated degenerate viscosity
suggests a physical penetration length of order `s^(3/2)` near activation.
These scales are **heuristic**, not a mesh-uniform upper bound on penetration.
They identify the estimate a parabolic barrier or localized energy argument
would have to prove. They do not show that the fixed central quarter loses
compression on such a scale.

Even the entropy gate alone does not justify a generic sharp causal cone:
around a constant positive `K` with an outward-decreasing density weight,
the temperature drop has a nonzero density contribution. The entropy gate
is then first order in the entropy gradient, so linear diffusion can appear
in a perturbation of `K`. The source-driven comparison above avoids needing
any finite-speed assertion for this flux.

## Direct attack on the compression bound: total stress

This section attacks (UC) itself rather than treating the conditional
reduction as an endpoint. It gives an exact scalar parabolic part, an
obstruction to using its scalar maximum principle, and a uniform conditional
bound on the size of the thermal correction.

In active compression let

\[
 A(\rho)=\rho W h,\quad
 b(K)=\tfrac12\left(1+\frac{K}{K+0.01}\right),\quad
 p(K,\rho)=K\rho^2h,\qquad
 S=P+q_s+q_d=A b C-A+p.
\]

In `rho>1`, `C>2`, `K>=0`, the three partial derivatives satisfy

\[
 S_C=Ab>0,\qquad S_\rho>0,\qquad S_K>0.
\]

The positivity of `S_rho` follows from `A'>0`, `bC-1>0`, and
`p_rho>=0`; the other two signs are direct.

There is an exact discrete analogue of the divergence evolution equation.
With `V_i=dm/rho_i` and the natural zero center term,

\[
 \dot C_i=\frac{16\pi^2}{V_i}\left[
  \frac{r_i^4}{\mu_i}(S_{i+1}-S_i)
 +\frac{r_{i-1}^4}{\mu_{i-1}}(S_{i-1}-S_i)\right]
 +4\pi G\rho_i+R_i,                              \tag{S6}
\]
\[
 R_i=C_i^2-\frac{8\pi}{V_i}
       (r_i u_i^2-r_{i-1}u_{i-1}^2)\ge0.
\]

At the exterior use `S_{N+1}=0`; the actual half-weight `mu_N=dm/2`
is retained in (S6). To check the last sign, put
`a=r_i`, `b=r_{i-1}`, `D=a^3-b^3`. The numerator `D^2 R_i` is a
quadratic form in `u_i,u_{i-1}` with diagonal coefficients
`3a^4+6ab^3`, `3b^4+6a^3b`, and off-diagonal coefficient
`-9a^2b^2`. Its determinant is `18abD^2>=0`, and its diagonal
coefficients are nonnegative. This also covers `b=0` directly. Formula
(S6) follows by differentiating `C_i=-dot V_i/V_i` and inserting the
declared node momentum equation; the gravitational difference is exactly
`4pi G dm/V_i`.

Writing the positive-neighbor operator in (S6) as `mathcal A_i S`,
the exact total-stress equation is

\[
 \dot S_i=S_{C,i}\mathcal A_iS
 +S_{C,i}(4\pi G\rho_i+R_i)
 +\rho_i C_iS_{\rho,i}+S_{K,i}Q_i+S_{K,i}H_i.       \tag{S7}
\]

All displayed local reaction terms are nonnegative. The last heat term has
no sign at a minimum of `S`. This is an actual obstruction to the proposed
scalar stress maximum principle, not merely a missing estimate. At constant
`rho>1`, prescribe nonconstant nonnegative `K` and choose

\[
 C_i=\frac{S_0+A-K_i\rho^2h}{A b(K_i)}>2
\]

so that `S_i=S_0` everywhere. A cell at a peak of `K`, with a smaller
outward neighbor and no larger inward neighbor, has `H_i<0`, even though
it is also a minimum of `S`. For a fixed-amplitude jump at a fixed positive
mass radius, this heat term scales like `N^2`, while bounded `C` and
`rho` give bounded local reaction terms. Thus the heat term cannot be
discarded at stress minima using signs alone. These are admissible
instantaneous shell states; they are not claimed to occur in the specified
startup solution.

The corresponding continuum identity, useful for a possible barrier proof,
is

\[
 D_t C=16\pi^2\rho\,\partial_m(r^4 S_m)
       +4\pi G\rho+\operatorname{tr}((\nabla v)^2).
\]

In material mass coordinates the scalar stress diffusion has no uncontrolled
coefficient derivative: `partial_m(r^4)=r/(pi rho)`. In particular this
coordinate choice avoids inserting a density-gradient bound into the drift
of the scalar stress operator. It does not remove `S_K H` from (S7).

### Uniform smallness of thermal and memory stress under a compression bootstrap

Suppose on any central prefix, over `0<=s<=T`, one already has
`0<C_i<=u`, with `u>2`. Then `rho_i<=exp(us)`. The maximum `M_K`
of `K` over that prefix has no positive heat contribution: an incoming
face would require a strictly larger supplying `K` within the same prefix,
and the outer face only removes heat. Hence

\[
 D^+ M_K\le h(e^{us})(a_u+b_uM_K),\quad
 a_u=u(\tfrac12u-1),\quad b_u=50u^2,
\]
\[
 M_K(s)\le\frac{a_u}{b_u}
 \left[\exp\left(b_u\int_0^s h(e^{uv})\,dv\right)-1\right]. \tag{S8}
\]

This is a resolution-independent estimate and does not assume a bounded
heat-flux derivative. For `T<=log(2)/u`,

\[
 \int_0^s h(e^{uv})\,dv\le u^2e^{2uT}s^3.
\]

For instance `u=6`, `T=0.005` gives

\[
 M_K(T)\le\frac1{150}
  [\exp(64800e^{0.06}T^3)-1]<5.77\times10^{-5}.
\]

On this same bootstrap interval the non-original part of the stress obeys

\[
 \frac{P+q_d}{A}
 =K\frac{\rho}{W}+\tfrac12 C\frac{K}{K+0.01}
 \le M_K\frac{e^{uT}}{1.5}
     +\frac{u}{2}\frac{M_K}{M_K+0.01}.
\]

For the displayed values the right side is less than `0.0173`. This is a
proved conditional amplitude bound; it does not itself establish the
compression bootstrap. In particular small amplitude alone does not bound
the spatial second derivatives in (S7).

### A surviving continuation and its exact missing step

The constant-coefficient principal model

\[
 C_t=\nu C_{xx}+\beta K_{xx},\qquad K_t=\kappa K_{xx},
 \qquad \nu>\kappa\ge0,
\]

does admit a useful diagonalization:
`V=C+beta K/(nu-kappa)` obeys `V_t=nu V_xx`.
Consequently a large pointwise heat cross derivative need not create a
large compression change; its integrated effect is controlled by the
amplitude of `K`. In the formal homogeneous startup principal part,

\[
 \frac\beta\nu=\frac{S_K}{S_C}
 \longrightarrow\frac43+100C_a,
\]

which is finite even though both bulk diffusion and the density gate
vanish at activation. Estimate (S8) is therefore relevant to a perturbative
stress argument. This frozen-coefficient calculation is exact for its
stated model, but is not a diagonalization of the full shell equations.
The full gated heat flux also includes density-potential differences,
and the needed variable-coefficient/localized estimate has not been derived.
It is a plausible untried continuation, not an exhausted route or a proof
of (UC). An attempt to use `S-lambda K` with a constant `lambda` in the
full equations simply leaves uncancelled spatial `K` differences and
does not supply the missing maximum principle.

## Proof status, checks, and continuation

Executed routes:

1. Exact cold homology and one-sided activation expansion: proved for each
   fixed `N`; common leading cubic coefficient obtained. Obstruction to
   uniformization: the explicit surface `N^2s^3` correction.
2. Sharp finite-domain-of-dependence argument: unavailable; the bulk stress
   has positive velocity diffusion once active. This failure applies to this
   proof mechanism, not to the uniform floor claim.
3. Source-driven monotone auxiliary: proved, subject only to the stated
   local-heater lower bound. It removes the nonlinear heat-loss and permanent
   guard obligations from seeding.
4. Uniform interior compression: open. No numerical run was used as proof.
   The total-stress equation and small thermal-amplitude estimate above were
   derived directly; a scalar stress maximum principle fails because of
   the exact heat cross term.

The smallest remaining leaf is (UC), not a new heat comparison principle.
A meaningful continuation is a mesh-uniform localized comparison/energy
estimate for the degenerate bulk-viscous momentum equation from the
simultaneous activation data, controlling the central-quarter divergence
against the zero-stress surface. It must retain the physical free surface
and the stress work; replacing the full operator by homogeneous dust after
activation does not address the leaf. No such estimate is supplied here.

Review provenance: mathematical self-review of the fixed-`N` expansion and
the comparison proof; coordinator independent review was requested for the
source-driven auxiliary. The source files are the authority; no external
source-dependent theorem is used. Displayed decimal constants were evaluated
from the exact one-dimensional dust formulas using Python `math` and SciPy
quadrature, only as non-load-bearing annotations. No large-grid evolution was
run. The theorem uses exact formulas and inequalities, not those decimals.

### Pinned input hashes (SHA-256)

Paths are relative to `stable_stress_search/`.

| Input | SHA-256 |
| --- | --- |
| `entropy_transport/README.md` | `8719a07f915902b829030d178636e27602f362c0f0b0e4e9e5d02039f575d2f6` |
| `entropy_transport/DERIVATION.md` | `e08312d0dc3be7f3f2d225ca938a7872ceec6d4c2532db2102f54c7a984910da` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/refinement.py` | `faa09a692bb072a3198b18e53a711aa49cb51aef88fbdf5a94909ec46d37c523` |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |

Reproduction checks performed: `git rev-parse HEAD`, direct reads of all
seven pinned inputs, `sha256sum` on those inputs, and direct evaluation of
the dust crossing integral and cubic coefficient. The new note is the only
owned write. The original goal remains open at (UC).
