# Local startup bootstrap: replacing global amplitude by density and one cut stress

Owner: delegated nonlinear bootstrap route. Base checkpoint:
**X48-UC-2026-11-01-B**, using the exact unchanged virgin-sphere problem.
Observed shared HEAD: `7b1880de2caded85da4b8c34d84b5dc6c005650e`.
The hashes below, rather than the moving shared HEAD, pin the inputs.
Write scope: this file only. No model, numerical grid, initial state, previous
proof note, or status file was changed.

**The common startup interval is still unproved.** This note proves a smaller
geometry requirement for a localized actual-graph comparison. The earlier
global `|x|<=10` bootstrap can be replaced, for the boundary comparison, by
a density cap on the inner three quarters. Conserved energy then controls
the graph geometry, even with arbitrary compression or expansion amplitudes
in the outer quarter. A nonnegative stress at a single artificial cut is
sufficient boundary data; its positive amplitude need not be bounded.
The remaining density, cut-stress sign, and nonlinear pointwise estimates
are not proved here. None is inferred from meshwise continuity.

## 1. Exact contract and identities

Put `s=t-t_a`, `T=1/1000`, `M=pi/3`, `dm=M/N`,
`a=4^(-1/3)`, and

\[
 J=\lfloor3N/4\rfloor,\qquad I=\lceil N/4\rceil,
 \qquad \mu_i=dm\ (i<N),\quad\mu_N=dm/2.
\]

Here `x=-theta` is signed compression and `C=max(x,0)`. At activation,
`rho_i=1`, `K_i=0`, `r_i=a(i/N)^(1/3)`, and `x_i=C_a`, with the exact
activation constant `C_a>16/3` proved in the base entropy note. The target is

\[
 \exists T_*>0\ \forall N\ge32\ \forall s\in[0,T_*]:
 \quad x_i(t_a+s)\ge4\quad(1\le i\le I).
 \tag{UC}
\]

The exact equations on valid ordered geometry are

\[
 V_i={4\pi\over3}(r_i^3-r_{i-1}^3),\quad
 \rho_i={dm\over V_i},\quad
 a_i={(4\pi r_i^2)^2\over\mu_i},\quad a_0=0,
\]
\[
 (L_rf)_i={a_i(f_{i+1}-f_i)-a_{i-1}(f_i-f_{i-1})\over V_i},
 \qquad x_i'=R_i+(L_rS)_i,\qquad R_i\ge0,
 \tag{1}
\]
\[
 S_i=P_i+\kappa_i(x_i-2)_++\zeta_i x_i,
 \quad \kappa_i=\tfrac12\rho_iW_ih_i,\quad
 \zeta_i=\kappa_i{K_i\over K_i+.01},\quad
 P_i=K_i\rho_i^2h_i.
 \tag{2}
\]

The conserved physical energy is

\[
 E_N={1\over2}\sum_i\mu_i u_i^2
       +\sum_i dm\,K_iW_i-\sum_i{\mu_i m_i\over r_i},
 \qquad m_i=i\,dm.
 \tag{3}
\]

Nonnegative `K` and conservation are properties of the exact system, not
accepted-state numerical corrections. At the virgin initial time,
`u_i=-r_i/4`, `r_i=(i/N)^(1/3)`, so exactly

\[
 E_N=(1/32-M)\sum_i\mu_i(i/N)^{2/3}<0.
 \tag{4}
\]

## 2. Prefix density controls the whole gravitational energy

**Geometry lemma.** Suppose on an actual-solution interval `0<=s<=T`
the geometry is ordered and

\[
 \rho_i(s)\le e^{1/100}\quad(1\le i\le J).
 \tag{D}
\]

There is no density, compression, velocity, or entropy amplitude assumption
on `i>J`. Then, throughout this interval,

\[
 \left|\sum_i{\mu_i m_i\over r_i}\right|<2,\qquad
 {1\over2}\sum_i\mu_i u_i^2<2,\qquad
 r_i<7/5\quad(i\le J).
 \tag{5}
\]

**Proof.** Write `q=J/N>=23/32`. For `i<=J`, summing the individual
volumes, rather than estimating their differences, gives

\[
 r_i\ge a e^{-1/300}(i/N)^{1/3}.
\]

For `i>J`, ordering gives `r_i>=r_J`. Since
`min(i,J)>=qi` for every `i<=N`, the two statements combine as

\[
 r_i\ge a e^{-1/300}q^{1/3}(i/N)^{1/3}
 \qquad(1\le i\le N).
 \tag{6}
\]

Consequently

\[
 -E_{{\rm grav},N}
 \le {M e^{1/300}\over a q^{1/3}}
                 \sum_i\mu_i(i/N)^{2/3}
 \le {M^2 e^{1/300}\over a q^{1/3}}=:\Gamma<2.
 \tag{7}
\]

For the last strict bound it suffices to use
`M<22/21`, `a^(-1)<8/5`, `q^(-1/3)<9/8`, and
`e^(1/300)<101/100`; the product
`(22/21)^2*(8/5)*(9/8)*(101/100)` is less than two.
Equations (3)--(4) and nonnegative internal energy give the kinetic bound.

Let `mathcal I(s)=sum_i mu_i*r_i(s)^2`. The elementary weighted Euclidean
norm inequality, integrated in time, gives

\[
 \sqrt{\mathcal I(s)}
 \le\sqrt{\mathcal I(0)}
       +\int_0^s\left(\sum_i\mu_i u_i(v)^2\right)^{1/2}dv
 <{13\over20}+2s\le{163\over250}.
 \tag{8}
\]

Indeed `mathcal I(0)<=a^2 M<(12/19)^2*(22/21)<(13/20)^2`.
For every `i<=J`, all nodes `j>i` have radius at least `r_i`, and their
total nodal weight is

\[
 \sum_{j=i+1}^N\mu_j=(N-i-1/2)dm
 \ge M(1/4-1/(2N))\ge15M/64>15/64.
\]

Thus
`r_i^2 < (163/250)^2*(64/15) < (7/5)^2`.
This proves (5). The actual half mass at the last node is included in both
the energy and tail-mass estimates. QED.

Only an upper density cap was used. Arbitrarily negative signed compression
is compatible with this lemma; it cannot invalidate the graph constants by
itself. Conversely, an assumed prefix upper compression bound `x_i<=10`
would imply (D) through `rho_i(s)=exp(int_0^s x_i(v)dv)`. That implication
does not establish either assumption along the actual solution.

## 3. A localized scalar boundary estimate under (D)

Retain the homogeneous reference coefficient from the base notes,

\[
 0\le\nu_d(s)\le972s^2,\qquad 0\le B_d(s)\le12
 \quad(0\le s\le T).
 \tag{9}
\]

These are bounds on prescribed reference functions; no homogeneity of the
actual solution is asserted. On cells `1,...,J-1`, use their actual graph
and impose `b_J=12`:

\[
 b_i'=\nu_d(L_rb)_i,\qquad b_i(0)=0.
 \tag{10}
\]

**Localized boundary theorem.** Under (D), for every `N>=32`,

\[
 0\le b_i(s)<1/48\qquad(i\le I,\ 0\le s\le T).
 \tag{11}
\]

**Proof.** The scalar maximum principle gives `0<=b<=12`. For `i<J`,
both nodal weights used in the row are `dm`. Its jump rates are

\[
 \beta_i^+=16\pi^2\nu_d r_i^4/(V_i dm),\qquad
 \beta_i^-=16\pi^2\nu_d r_{i-1}^4/(V_i dm).
\]

The exact geometric cancellation from the base note gives
`(r_i^4-r_{i-1}^4)/V_i<=r_i/pi`. Equations (D) and (5) therefore imply,
with `R_*=7/5` and `rho_*=e^(1/100)`,

\[
 0\le\beta_i^+-\beta_i^-\le48R_*\nu_dN,
 \qquad \beta_i^++\beta_i^-\le288\rho_*R_*^4\nu_dN^2.
 \tag{12}
\]

For `E_i=exp[-lambda(J-i)/N]`, Taylor's inequality yields

\[
 {\nu_d(L_rE)_i\over E_i}
 \le972s^2\left[48R_*\lambda
       +144\rho_*R_*^4\lambda^2 e^{\lambda/32}\right].
 \tag{13}
\]

Take `lambda=16`. Using `rho_*<51/50`, `R_*^4<4`, and
`e^(1/2)<5/3`, the coefficient of `s^2` is less than `3*10^8`.
Hence `12 E_i exp(10^8 s^3)` is a supersolution with boundary value
at least 12. For `i<=I`,

\[
 {J-i\over N}\ge {1\over2}-{2\over N}\ge7/16,
 \qquad
 b_i(s)\le12\exp(-7+10^8s^3)\le12e^{-69/10}<1/48.
 \tag{14}
\]

The last strict inequality follows from the exponential series, for example
`e^6>300` and `e^(.9)>1+.9+.9^2/2`. The ceiling in the target is retained.
No derivative of the actual density, compression, or conductance was bounded.
QED.

## 4. The actual artificial boundary needs only a stress sign

For `i<J` define

\[
 w_i=x_d-x_i,\qquad
 \delta S_i=S_i-(S_d-\nu_dw_i).
\]

At the artificial boundary use **algebraic**, not physical, ghost values

\[
 w_J^{\rm ghost}=B_d-S_J/\nu_d,
 \qquad \delta S_J^{\rm ghost}=0\quad(s>0).
 \tag{15}
\]

Then `S_d-nu_d*w_J^ghost=S_J`, so the same exact subtraction as in the
base actual-graph identity gives on every physical cell `i<J`

\[
 w'=\nu_dL_rw+(R_d-R)-L_r\delta S.
 \tag{16}
\]

Here all generators and propagators are restricted to `1,...,J-1` with
zero ghost value when acting on `delta S` or on homogeneous evolution.
Equation (15) supplies the separate boundary input for `w`. In particular,

\[
 S_J\ge0\quad\Longrightarrow\quad
 w_J^{\rm ghost}\le B_d\le12.
 \tag{B}
\]

No upper bound on positive `S_J/nu_d` is needed. For each fixed mesh the
activation expansions give a finite initial ghost limit; variation of
constants can also be applied from `s=eta>0` and then sent to zero.
Neither passage claims a uniform bound on thermal variation.

Let `P^J_r(s,v)` be the positive zero-boundary propagator and set

\[
 \mathcal E_i(s)=-\int_0^s
       [P^J_r(s,v)L_r(v)\delta S(v)]_i\,dv.
 \tag{17}
\]

If (D) and (B) hold, comparison of the boundary part with (10), together
with `R>=0`, `R_d<47`, and the contraction property of `P^J_r`, gives

\[
 w_i(s)\le b_i(s)+47s+\mathcal E_i(s).
 \tag{18}
\]

Therefore the three precise sufficient inputs on the common interval are

\[
 \text{(D)},\qquad\text{(B)},\qquad
 \mathcal E_i(s)\le1\quad(i\le I,\ 0<s\le T).
 \tag{LC}
\]

They imply, without any global amplitude hypothesis,

\[
 x_i(s)>C_a-1/48-47/1000-1>4\qquad(i\le I).
 \tag{19}
\]

For the last inequality even `C_a>16/3` suffices. This is a localized
conditional certificate, not a proof that its three inputs hold.
Condition (B) follows from `x_J>=0`, but expansion can make `S_J` negative
through the signed memory stress. Neither `S>=0` nor `x>=0` is asserted as
a global invariant of the full law. If (B) fails, its exact adverse boundary
input is `(-S_J)_+/nu_d`; its transfer to the observation cells must be
estimated rather than discarded.

## 5. A further exact bound and the first-exit obstruction

The positive-square geometric source has an amplitude bound that does not
cost any mesh derivatives. On a prefix on which `|x_j|<=U`, define for
`i>=2`

\[
 \bar x_{i-1}={\sum_{j<i}V_jx_j\over\sum_{j<i}V_j}.
\]

Telescoping the defining volume divergence gives

\[
 {u_i\over r_i}=-{\sum_{j\le i}V_jx_j\over3\sum_{j\le i}V_j},
\]
\[
 {6r_ir_{i-1}(r_iu_{i-1}-r_{i-1}u_i)^2
                \over(r_i^3-r_{i-1}^3)^2}
 = {2\over3}\left({r_{i-1}\over r_i}\right)^3
                    (x_i-\bar x_{i-1})^2\le8U^2/3.
 \tag{20}
\]

For `i=1` the square vanishes. Thus, if `rho_i<=rho_*` on that prefix,

\[
 0\le R_i\le4\pi\rho_*+3U^2.
 \tag{21}
\]

This can supply the other side of a future amplitude estimate. It gives no
mesh-uniform bound on `L_r S` at a compression extremum, because a
compression extremum need not be a stress extremum.

A valid local first-exit proof would begin, for each fixed `N`, with the
strict activation margin in (D), the positive small-time cut stress from
the activation expansion, and `mathcal E_i(0)=0`. It must then establish
uniform improvements of (D), (B), and (17), or replace (B) by a proved bound
on the adverse boundary transfer. Equations (5), (11), and (18) ensure that
failure of the target inside this bootstrap cannot be blamed on an
uncontrolled outer-quarter graph geometry. They do not prevent one of the
three bootstrap inputs from failing first.

An energy bound alone does not give the missing improvement: (3) controls
nodal velocity in a weighted `l^2` norm, whereas compression differentiates
the nodal flux. The single-cell Green-potential construction in the base
effective-flux note already shows that even an `O(N^-2)` potential error can
hide an order-one central compression defect. Similarly, an amplitude bound
on `delta S/nu_d` does not bound its temporal variation in (17). The heat
coefficient/entropy cancellation is assigned to a separate route; no estimate
from that unresolved calculation is assumed here.

## 6. Outcome and continuation

Evidence label: **proved conditional reduction and auxiliary estimates**.
There is no counterexample to the actual virgin-sphere trajectory.
The global amplitude requirement has been removed from the boundary/geometry
part of the reduction, and the artificial boundary needs a stress sign rather
than a normalized stress amplitude bound. The original (UC) remains open.

Three discriminating attempts were executed: conserved-energy control of
the geometry under a prefix density cap succeeds; exact restriction of the
actual stress equation yields the sign-only boundary condition; a direct
compression-extremum invariant does not close because of the density-memory
stress and the signed memory damping. The latter is a failed argument, not
a refuted trajectory claim.

The next mathematical obligation is to derive (D) and (17) simultaneously
from a localized nonlinear estimate on a slightly larger prefix, while
controlling either the cut-stress sign or its negative boundary transfer.
Uniform regularity, a positive cut stress, or common first-exit times cannot
be supplied by the fixed-mesh activation expansion. This continuation remains
open; it is not exhausted by the present reduction.

## 7. Verification and pinned inputs

The graph restriction, energy signs, radial moment, exterior half weight,
ceiling indices, and numerical constants were rederived from the exact
source. Exact rational arithmetic verifies the generous constants in
(7)--(8) and (13)--(14); these are algebra checks, not trajectory sampling.
No outside theorem or continuum convergence claim is load-bearing.
Mathematical self-proofreading covered this file. Independent review is a
separate coordinator obligation; no fresh-agent audit is claimed here.

SHA-256 paths below are relative to `stable_stress_search/`:

| Input | SHA-256 |
| --- | --- |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/floor_theorem/TARGET.md` | `93792a4df2982bb70bbb68be3878405dbd3f8e2ea735c5f586ce0b28b2394b14` |
| `entropy_transport/floor_theorem/seed_route.md` | `752944eb3c0c7ff87007b5ca1c3f5a46bb768d8215645914ad6b211cebcd053d` |
| `entropy_transport/floor_theorem/startup_energy_route.md` | `06630aecae84c9b618e84c1ddded3f2025f7a89f7dca634bbbb05f50d0e2380b` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/TARGET.md` | `845098298ef29ab6212a0c58edf46287806bb9d5944b794fc7b90e84f1f9b846` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/STATUS.md` | `4b45329feff137ba284c9918165301f5325ac658e59a47606007158231398ee3` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/all_mesh_certificate.md` | `15582ff1b45a715fccc5c84cd4883fa533ce714fb77b7ef091aa53205ba69a18` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/entropy_energy.md` | `bb4429ad5f3c9345d2c6d44a7864c407e273caad13ed3643fac5aa822c9990e3` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/effective_flux.md` | `ba03913a2d497fcefc346b8f04cc0da2d128a3f7dee34ee535c36155459f3ba3` |
