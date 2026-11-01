# Actual-geometry all-mesh estimates: progress and the unclosed constitutive term

Base checkpoint: **X48-FLOOR-2026-11-01-B**. Owner: delegated all-mesh
certificate route. Observed Git HEAD: `f55188b7295cfc56670f8e1ef49fe6c8d7ccc191`.
The shared checkout moves concurrently; the input hashes below identify this
attempt. Write scope: this file only. No constitutive law, sphere parameter,
numerical trajectory, or production operator was changed.

**Original goal remains open.** There is no specified-data counterexample in
this note. Three new analytic facts are established: an actual-geometry
boundary barrier under a stated compression-amplitude bootstrap, elimination
of the moving-conductance commutator by using the actual graph propagator,
and a uniform spectral bound for the leading density-memory system. The
bootstrap and the full nonlinear thermal/constitutive remainder are not
proved. The first result covers the cells intersecting the central quarter,
including the ceiling in their index. The conclusions are not finite-grid
extrapolations.

## 1. Exact law and route contract

The target is (UC) for the unchanged `ConvectiveCollapse` sphere: some common
`T>0` such that `C_i(t_a+s)>=4` for `0<=s<=T`, every `N>=32`, and
`i<=ceil(N/4)`. Here `C=max(x,0)`, `x=-theta` is signed compression,
`t_a` is the common cold activation time, and `C_a=5.4145849604...`.
The entropy-floor implication is the source-driven comparison in
`../seed_route.md`; it is not re-proved here.

All quantities below are evaluated on the exact semidiscrete solution while
its geometry is valid. Set `s=t-t_a`, `M=pi/3`, `dm=M/N`, `r_0=u_0=0`,

\[
 V_i={4\pi\over3}(r_i^3-r_{i-1}^3),\qquad
 a_i={(4\pi r_i^2)^2\over\mu_i},\qquad
 \mu_i=dm\ (i<N),\quad\mu_N=dm/2,
\]
\[
 (L_r f)_i={a_i(f_{i+1}-f_i)-a_{i-1}(f_i-f_{i-1})\over V_i},
 \quad a_0=0,\quad f_{N+1}=0.
 \tag{1}
\]

The exact stress, including memory damping and pressure, is

\[
 S_i=P_i+\kappa_i(x_i-2)_++\zeta_i x_i,
 \quad \kappa_i=\tfrac12\rho_i W_i h_i,
 \quad\zeta_i=\kappa_i{K_i\over K_i+.01},
 \quad P_i=K_i\rho_i^2h_i.
 \tag{2}
\]

The exact compression equation from `../startup_energy_route.md` is

\[
 x_i'=R_i+(L_rS)_i,\qquad
 R_i=4\pi\rho_i+{x_i^2\over3}
 +{6r_ir_{i-1}(r_i u_{i-1}-r_{i-1}u_i)^2
       \over(r_i^3-r_{i-1}^3)^2}\ge0.
 \tag{3}
\]

The route tested three distinct proposed failure mechanisms: mesh growth
from moving conductances; high-frequency amplification by density memory;
and the residual heat/stress coupling. The first admits the bounds below;
the second does not blow up in its leading selfadjoint model; the third is
still open for this IVP. No sign argument on arbitrary other initial states
is used as a counterexample to the target.

## 2. Geometry needs compression amplitudes, not spatial derivatives

The telescoping definition of compression gives the exact identities

\[
 {u_i\over r_i}=-{\sum_{j\le i}V_jx_j\over3\sum_{j\le i}V_j},
 \qquad {V_i'\over V_i}=-x_i,
 \qquad {a_i'\over a_i}=4{u_i\over r_i}.
 \tag{4}
\]

Consequently, on any prefix where `|x_j|<=U`, including its entire earlier
history from activation,

\[
 e^{-Us}\le\rho_i\le e^{Us},\qquad
 a_a e^{-Us/3}(i/N)^{1/3}\le r_i
 \le a_a e^{Us/3}(i/N)^{1/3},\qquad a_a=4^{-1/3},
 \tag{5}
\]
\[
 |(\log V_i)'|\le U,\qquad |(\log a_i)'|\le4U/3.
 \tag{6}
\]

These implications do not assume neighboring densities or compressions are
close. The bounds on `r_i` follow by summing the individual cell volumes,
which start at `dm`. They remain valid through arbitrarily sharp differences
of bounded compression.

There is also a quantitative relative-form estimate. Let `d` denote any
homogeneous reference geometry with the same cell masses, and suppose

\[
 \delta=\max_i|\log(\rho_i/\rho_d)|.
\]

Since `r_i^3/(r_i^d)^3` is the average of `V_j/V_j^d` over `j<=i`,

\[
 e^{-\delta}\le V_i/V_i^d\le e^\delta,\qquad
 e^{-4\delta/3}\le a_i/a_i^d\le e^{4\delta/3}.
 \tag{7}
\]

For `D_rf=sum_i a_i(f_{i+1}-f_i)^2`, including the zero exterior value,
the bilinear forms satisfy

\[
 \left|\sum_i(a_i-a_i^d)\Delta f_i\Delta g_i\right|
 \le (e^{4\delta/3}-1)D_df^{1/2}D_dg^{1/2},
 \tag{8}
\]
\[
 \left|\sum_i(V_i-V_i^d)f_i g_i\right|
 \le(e^\delta-1)\|f\|_{V^d}\|g\|_{V^d}.
 \tag{9}
\]

Both follow from Cauchy--Schwarz. They hold for every `N` and have no
`N^2` factor. With `w=x_d-x` and equal activation densities,
`delta(s)<=int_0^s ||w(v)||_infinity dv`. Thus moving geometry is a small
**form** perturbation on a bounded-compression short interval even when its
pointwise operator-norm perturbation is large. This statement alone does
not bound the constitutive gate: `kappa_rho/kappa` is singular at activation.

For later use, the actual-graph scalar energy identity is also exact. If
`f'=nu_d L_r f` with zero exterior value, then

\[
 {d\over ds}\left({1\over2}\sum_iV_i f_i^2\right)
 =-\nu_d D_rf-\frac12\sum_iV_ix_i f_i^2
 \le-\nu_d D_rf+U\left({1\over2}\sum_iV_if_i^2\right).
 \tag{10}
\]

This is the appropriate capacity-form estimate; multiplying an operator
difference by a nonconstant capacity ratio and then silently integrating
by parts would introduce an uncontrolled spatial difference of that ratio.

The same calculation gives a localized estimate on the moving graph. For
`eta_i=exp(sigma i/N)`, `|sigma|=lambda`, set

\[
 C_\lambda=288a_a^4 e^{7UT/3}\lambda^2e^{2\lambda/32}.
\]

For zero-boundary `f`, the exact edge identity is

\[
 \sum_iV_i\eta_i^2f_i(L_rf)_i
 =-D_r(\eta f)+\sum_{i=1}^{N-1}
       a_i f_i f_{i+1}(\eta_{i+1}-\eta_i)^2.
\]

The boundary edge contributes only its negative Dirichlet term. Using
`2|f_if_{i+1}|<=f_i^2+f_{i+1}^2` and collecting the two endpoint
contributions gives

\[
 {d\over ds}\left({1\over2}\sum_iV_i(\eta_i f_i)^2\right)
 \le-\nu_dD_r(\eta f)
 +(U+C_\lambda\nu_d)
       \left({1\over2}\sum_iV_i(\eta_i f_i)^2\right).
 \tag{10a}
\]

Indeed the endpoint cost at row `i` is bounded by
`sum_{j~i} (a_{ij}/V_i)((eta_j-eta_i)/eta_i)^2`;
(5), `dm=M/N`, and `|exp(sigma/N)-1|<=exp(lambda/N)lambda/N`
bound it by `C_lambda`. The center has one edge, and the omitted positive
boundary cost only improves the bound at the outer cell.

Thus the propagator on the actual graph satisfies

\[
 \|\eta P_r(s,v)f\|_{V(s)}
 \le\exp\left[{U(s-v)\over2}
       +{C_\lambda\over2}\int_v^s\nu_d(q)\,dq\right]
       \|\eta f\|_{V(v)}.
 \tag{10b}
\]

For ordered source and observation sets separated by `d>0` in `i/N`, with
all source indices on one side of all observation indices, choosing the sign
of `sigma` toward the observation set yields an additional factor
`exp(-lambda d)` in the corresponding restricted operator norm. This is
an actual moving-graph localized energy bound, uniform in `N`, conditional
only on the stated amplitude bootstrap. It does not estimate the heat
cross term in the full stress equation.

## 3. A boundary barrier on the actual moving graph

Let `nu_d=kappa_d+zeta_d` and `B_d=S_d/nu_d` be the homogeneous reference
quantities already defined in `../startup_energy_route.md`, with the finite
right limit prescribed at activation. That note establishes, without any
trajectory integration,

\[
 0\le\nu_d(s)\le972s^2,\qquad 0\le B_d(s)\le12,
 \qquad 0\le s\le1/1000.
 \tag{11}
\]

**Actual-graph scalar theorem.** Suppose the exact geometry satisfies
`|x_i(s)|<=10` for all cells on `0<=s<=10^{-3}`. The solution of

\[
 b'=\nu_d L_rb,\qquad b(0)=0,\qquad b_{N+1}=B_d
 \tag{12}
\]

then obeys, for every `N>=32`,

\[
 0\le b_i(s)<1/48,
 \qquad i\le\lceil N/4\rceil,\quad 0\le s\le10^{-3}.
 \tag{13}
\]

The compression bound in this theorem is a hypothesis, not a proved property
of the actual IVP.

**Proof.** Positivity and the maximum principle give `0<=b_i<=12`, including
at the actual half-weight outer node. Restrict to `i<N` and use `b_N<=12`
as the comparison boundary. For such rows the two jump rates of `nu_d L_r`
are `beta_i^+=16 pi^2 nu_d r_i^4/(V_i dm)` and
`beta_i^-=16 pi^2 nu_d r_{i-1}^4/(V_i dm)`.

The exact cancellation

\[
 {r_i^4-r_{i-1}^4\over V_i}\le {r_i\over\pi}
 \tag{14}
\]

follows by integrating the inequality
`d(r^4)/d(r^3)=(4/3)r<=(4/3)r_i` over the cell. Hence (5) gives

\[
 0\le\beta_i^+-\beta_i^-
 \le48a_a e^{10T/3}\nu_d N,
\]
\[
 \beta_i^++\beta_i^-
 \le288a_a^4 e^{70T/3}\nu_d N^2,
 \qquad T=10^{-3}.
 \tag{15}
\]

For `E_i=exp[-lambda(1-i/N)]`, Taylor's inequality gives

\[
 {\nu_d L_rE_i\over E_i}
 \le972s^2\left[48a_a e^{10T/3}\lambda
   +144a_a^4e^{70T/3}\lambda^2e^{\lambda/32}\right].
 \tag{16}
\]

For `lambda=9` the coefficient multiplying `s^2` is less than `4*10^6`.
For an elementary generous bound one may use
`a_a<.63`, `a_a^4<.158`, `e^{.023334}<1.024`,
`e^{.003334}<1.004`, `e^{9/32}<1.325`; these inequalities follow directly
from the exponential series. Therefore

\[
 b_i(s)\le12\exp[-9(1-i/N)+4\cdot10^6s^3/3].
 \tag{17}
\]

For all cells intersecting the central quarter,
`i/N<=1/4+1/N<=9/32`. Thus the last bound is at most

\[
 12\exp[-207/32+1/750]<1/48.
\]

For example `207/32-1/750>6.4`, while `e^{6.4}>576`; the latter follows
already from a finite lower partial sum of the exponential series.
This proves (13). No density difference or conductance difference is bounded
pointwise in this argument. QED.

## 4. The moving-conductance commutator can be removed exactly

Use the same `w=x_d-x` as in the startup note, and define on physical cells

\[
 S^{lin}=S_d-\nu_dw,\qquad \delta S=S-S^{lin}.
 \tag{18}
\]

Give `w` the algebraic ghost value `B_d`; then `S^{lin}` and `delta S` both
have zero exterior value. Unlike the reference-graph decomposition, the
following equation has **no moving-conductance remainder**:

\[
 \boxed{\quad
 w'=\nu_d L_rw+(R_d-R)-L_r\delta S.
 \quad} \tag{19}
\]

Indeed, `-L_rS=-L_rS^{lin}-L_r delta S=nu_d L_rw-L_r delta S`, including
the boundary row. This identity is exact for the full law; it does not
remove pressure or memory damping.

Let `P_r(s,v)` be the zero-boundary propagator of `nu_d L_r`. It is positive
and an `l^infinity` contraction for each valid geometry, regardless of
spatial coefficient derivatives. Writing `b` for (12), exact Duhamel gives

\[
 w(s)=b(s)+\int_0^sP_r(s,v)(R_d-R)(v)\,dv
       -\int_0^sP_r(s,v)L_r(v)\delta S(v)\,dv.
 \tag{20}
\]

Since `R>=0`, `R_d<47`, the middle term is at most `47s`. Under the stated
bootstrap, a sufficient remaining bound is therefore

\[
 \sup_{N\ge32}\sup_{0<s\le10^{-3}}
 \max_{i\le\lceil N/4\rceil}
 \left[-\int_0^sP_r(s,v)L_r(v)\delta S(v)\,dv\right]_i\le1.
 \tag{AC}
\]

Together with (13), this would give
`x_i>=C_a-1/48-.047-1>4`. The unclosed assumptions are (AC) and a
noncircular way to establish the geometry/bootstrap on the relevant graph.
Replacing the old propagator by the actual one does not prove either.

There is a second exact normal form that sometimes avoids estimating second
spatial differences. Set `z=delta S/nu_d` for `s>0`. On `[eta,s]`,

\[
 -\int_\eta^sP_r(s,v)L_r(v)\delta S(v)\,dv
 =z(s)-P_r(s,\eta)z(\eta)
       -\int_\eta^sP_r(s,v)z'(v)\,dv.
 \tag{21}
\]

This follows from `partial_v P_r(s,v)=-P_r(s,v)nu_d(v)L_r(v)` and the
product rule. It needs no commutation of generators at distinct times.
For each fixed `N`, the activation expansions give `z(eta)->0`; a uniform
temporal-variation bound is still required to turn (21) into a uniform
estimate. In particular `z'` contains the actual nonlinear heat derivative
through `K'`, and its total variation has not been bounded here. Equation
(21) is an exact alternative obligation, not a hidden regularity assumption.

## 5. Density memory does not cause spectral blowup in its leading model

This subsection is an auxiliary leading-model theorem, not an approximation
theorem for the original IVP. It isolates a genuine cancellation lost by
absolute Jacobian estimates. To leading order at activation, neglecting
thermal terms and geometric variation,

\[
 {\delta S\over\nu_d}\simeq-\alpha y,\qquad
 y(s)={1\over s}\int_0^s w(v)\,dv,\qquad
 \alpha={2(C_a-2)\over C_a}\in(0,2).
 \tag{22}
\]

The coefficient follows from `kappa` being quadratic in `rho-1`:
`delta rho/rho_d=-int w+...`, so
`delta kappa/kappa_d=-(2/C_a)y+...`. The resulting abstract system is

\[
 w_s=s^2L(w+\alpha y),\qquad y_s=(w-y)/s,
 \qquad y(0)=w(0)=w_0,
 \tag{23}
\]

where `L` is any finite-dimensional selfadjoint negative semidefinite
operator. The fixed scalar factor in the leading viscosity may be absorbed
in `L`. Zero-boundary finite graphs (1) with fixed geometry are included.

**Model theorem.** For every `0<alpha<3`, the regular solution of (23)
satisfies

\[
 \|w(s)\|_2\le\|w_0\|_2,\qquad
 \|y(s)\|_2\le\|w_0\|_2,
 \tag{24}
\]

independently of all eigenvalues and the dimension of `L`.

**Proof.** On a spectral mode `L=-lambda`, let `z=lambda s^3/3`.
Then `w_z=-(w+alpha y)` and `y_z=(w-y)/(3z)`. Eliminating `y` gives

\[
 z w_{zz}+(z+b)w_z+a w=0,
 \qquad b=1/3,\quad a=(1+\alpha)/3.
 \tag{25}
\]

Let `mu` be the probability measure on `(0,1)` with density proportional to
`t^{a-1}(1-t)^{b-a}`. It is integrable precisely when
`0<a<b+1`, as holds for `0<alpha<3`. Define

\[
 g(z)=\int_0^1e^{-zt}\,d\mu(t),\qquad
 f(z)=g(z)+(z/b)g'(z)
     =\int_0^1(1-3zt)e^{-zt}\,d\mu(t).
 \tag{26}
\]

Integration of the derivative of
`t^a(1-t)^{b+1-a}e^{-zt}` gives
`zg''+(z+b+1)g'+ag=0`. Substituting this identity and its derivative into
the definition of `f` gives (25). Moreover
`f(0)=1`, `f'(0)=-a/b=-(1+alpha)`, which select the regular solution of
(23). This derivation invokes no special-function table.

For every `q>=0`,

\[
 -3e^{-4/3}\le(1-3q)e^{-q}\le1,
 \qquad 3e^{-4/3}<1.
\]

Thus `|f(z)|<=1` for every `z>=0`. The spectral theorem gives the first
inequality in (24). The identity `y(s)=s^{-1}int_0^s w(v)dv` gives the
second by the triangle inequality. The zero eigenvalue is covered by the
continuous limit `f(0)=1`. QED.

This theorem excludes high-frequency spectral amplification for the stated
leading model and compatible regular initial data. It does not imply an
`l^infinity` contraction, a bound for arbitrary time-dependent forcing,
localization of a boundary input, or stability of the moving nonlinear
coupled system. Those stronger statements require additional arguments.

## 6. Remaining obstruction, disposition, and concrete continuation

The new estimates remove spatial conductance regularity from the scalar
barrier and remove the geometry commutator from the exact Duhamel formula.
They do not permit deleting `delta S`. On the active branch, it includes

\[
 [\kappa(\rho)-\kappa_d](x-2),\quad
 \zeta x-\zeta_d x_d,\quad P-P_d,
\]

as well as the affine bookkeeping in (18). Its leading density-memory part
is of principal size and has the structured sign (22). The nonlinear heat
law remains inside `K`, and (21) makes clear that merely bounding `K` in
amplitude does not bound the required temporal variation. The existing
conditional `K=O(s^3)` maximum estimate is relevant but does not close this
last implication.

No counterexample to UC was found. This route is **open, with partial proved
lemmas**, rather than exhausted. The narrow deferred task is to extend the
density-memory stability mechanism to a localized estimate for the full
`(normalized stress, normalized density, normalized K)` system on the
actual graph, retaining the heat cross term. The algebra (19) and capacity
identities (4)--(10) should be used before estimating a commutator. A
successful continuation must prove (AC), or a comparably explicit local
pointwise bound, and discharge its compression-amplitude bootstrap; an
unweighted `L^2` bound such as (24) alone is insufficient at cells of mass
`dm->0`.

Proof status: self-reviewed elementary finite-dimensional derivations. The
scope of self-review includes the outer half-weight, capacity factors,
signed/positive compression, ghost stress in (19), orientation of the
propagator derivative in (21), the ceiling in (13), and the beta-integral
mode calculation. Mathematical proofreading covered this new file only.
No trajectory computation or external theorem is load-bearing.

## Input provenance

All SHA-256 hashes were read at this attempt; paths are relative to
`stable_stress_search/`.

| Input | SHA-256 |
|---|---|
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/floor_theorem/TARGET.md` | `93792a4df2982bb70bbb68be3878405dbd3f8e2ea735c5f586ce0b28b2394b14` |
| `entropy_transport/floor_theorem/STATUS.md` | `d05a94e8f701f0e1d5076dc9c3fbaf7468bb8b5822a493e64e275d867ae712f6` |
| `entropy_transport/floor_theorem/seed_route.md` | `752944eb3c0c7ff87007b5ca1c3f5a46bb768d8215645914ad6b211cebcd053d` |
| `entropy_transport/floor_theorem/startup_energy_route.md` | `06630aecae84c9b618e84c1ddded3f2025f7a89f7dca634bbbb05f50d0e2380b` |
