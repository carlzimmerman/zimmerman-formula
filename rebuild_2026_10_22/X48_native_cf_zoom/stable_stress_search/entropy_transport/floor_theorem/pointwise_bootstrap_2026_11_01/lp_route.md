# Actual all-p heat flux: two entropy obstructions and a finite-p repair

Base checkpoint: **X48-DEN-2026-11-01-A**. Delegated route: actual
all-p/level-set stress flux. Observed source HEAD:
`8a293ba8b8411e84c9e37bb9770d1a6f993f606e`. The shared checkout may move;
the byte hashes below identify the inputs. Write scope is this file only.
The physical law, startup datum, heaters, gates, and all run artifacts are
unchanged. No numerical trajectory is used.

**Primary verdict: incomplete for the original pointwise target.** A
separate q-p entropy cannot absorb the full stress heat flux for any
`p>2`, even at constant density and constant stress. The proposed repair
with a stress-dependent quadratic q entropy creates a new mechanical
cross flux on faces where the actual heat gate is closed. Both statements
are proved below for instantaneous admissible edge states; neither
refutes the specified IVP or (UC). A constant-weight quadratic companion
does absorb the full heat flux for every finite p. Its dependence on the
provisional stress amplitude prevents the available first energy from
giving a better supremum bound by this estimate alone.

## 1. Target, hypotheses, and exact identity

The target remains a common time and positive exponent such that, for
every `N>=32`,

\[
 \left\|\frac{S-S_d}{s^2}\right\|_{\ell^\infty(I_{\rm central})}
       \le C s^\theta,\qquad \theta>0.                    \tag{P1}
\]

The actual provisional prefix, including each cutoff collar, has
`2<x<=8`, `2s<=z=log rho<=8s`, `0<=K<=1600s^3`, and
`0<s<=T<=10^-3`. The tight bound `|x-x_d|<=delta` is assumed where
needed; it is not proved here. Write

\[
 \begin{gathered}
 \kappa=\tfrac12\rho Wh,\quad c=1/100,\quad
 g=\frac K{K+c},\quad \nu=\kappa(1+g),\quad P=K\rho^2h,\\
 S=\nu x-2\kappa+P,\quad f=S-S_d,\quad
 q=KW^{3/2}-\psi_d,\qquad L_e=-\ell_e\Delta_eq,
 \quad\ell_e\ge0.
 \end{gathered}                                             \tag{P2}
\]

All differences are right minus left. Mechanical conductance is
`a_e=(4*pi*r_e^2)^2/dm`. The pinned heat calculation proves, on every
internal actual face including the first positive face,

\[
 \ell_e/a_e\le16200s^4.                                  \tag{P3}
\]

For `p>=2`, `J_p(f)=|f|^(p-2)f`, and a fixed material cutoff phi,
the stress energy and its complete heat cotangent are

\[
 E_p=\frac1p\sum_i\frac{V_i\phi_i}{\nu_i}|f_i|^p,
 \quad M_p=\alpha J_p(f)-\frac\beta p|f|^p,
 \quad \alpha=\frac{S_K}{\rho\nu W},\quad
 \beta=\frac{\nu_K}{\rho\nu^2W}.                        \tag{P4}
\]

Its exact spatial pairing is

\[
 -\sum_ea_e\Delta(\phi J_p(f))\Delta f
       +\sum_eL_e\Delta(\phi M_p).                      \tag{P5}
\]

In particular the heat part of the state-dependent `1/nu` time weight
is present in the beta term. The finite-edge remainder is exactly

\[
 \Delta M_p=\bar\alpha\Delta J_p(f)
       -\frac{\bar\beta}{p}\Delta|f|^p
       +\overline{J_p(f)}\Delta\alpha
       -\frac{\overline{|f|^p}}p\Delta\beta.             \tag{P6}
\]

Equations (P4)--(P6) use the actual state, not a frozen heat coefficient
or a differentiated gate. Local reaction, time-weight, and cutoff work
remain the terms stated in `pointwise_continuation.md`; the interior
statements below are not full evolution estimates.

## 2. Exact stress-coordinate structure, including the weight term

Fix z and s and use `(f,K)` as state coordinates. Set

\[
 b=2\rho/W,\qquad A=2K+c,\qquad T_f=f+S_d+2\kappa.
\]

The exact inverse is

\[
 x=\frac{T_f-b\kappa K}{\nu},\qquad
 \beta=\frac{c}{\rho W\kappa A^2},\qquad
 \alpha=\frac1{\rho W}
   \left\{\frac{c(T_f/\kappa-bK)}{A^2}
                       +\frac{b(K+c)}A\right\}.        \tag{P7}
\]

Thus `alpha_f=beta`. Differentiating (P4) at fixed z and K gives the
useful exact cancellation

\[
 \partial_fM_p=(p-1)\alpha|f|^{p-2}.                    \tag{P8}
\]

The `beta*J_p` contribution from `alpha_f` cancels the derivative of
the heat-weight term. At fixed **positive** `f=F`, however,

\[
 \boxed{\quad
 \left.\partial_KM_p\right|_{f=F,z}
 =-\frac{4cF^{p-1}}{\rho W\kappa(2K+c)^3}
   \left\{S_d+2\kappa+(1-1/p)F+\frac{b\kappa c}{2}\right\}<0.
 \quad}                                                     \tag{P9}
\]

For direct verification,
`alpha_K=-(4c*T_f/kappa+2*b*c^2)/(rho*W*A^3)` and
`beta_K=-4c/(rho*W*kappa*A^3)`. Inserting these two derivatives into
`F^(p-1)*alpha_K-F^p*beta_K/p` proves (P9).
All coefficients are evaluated on the same actual constitutive state.

## 3. A sharp obstruction to a separate q-p entropy

Fix any sufficiently small positive time of the homogeneous reference.
It has `kappa_d>0` and `0<K_d<1600s^3`: positivity follows from the
positive original heater, and the strict upper bound follows from the
strict estimate preceding the rounded bound in (H11) of
`heat_absorption.md`. Put both endpoint densities equal to `rho_d`.
Choose `F>0` so small that the inverse state with `f=F,K=K_d` is
strictly inside `|x-x_d|<delta`; for example take
`F=delta*nu_d/4`. Now let, with `w_0=W_d^(3/2)`,

\[
 K_l=K_d+\varepsilon/w_0,\quad
 K_r=K_d-\varepsilon/w_0,\quad
 f_l=f_r=F,\quad q_l=\varepsilon,\quad q_r=-\varepsilon.
                                                               \tag{P10}
\]

Use (P7) separately to choose both x values. For sufficiently small
positive epsilon all states remain in the strict physical and tight
bootstrap boxes. The density, geometry, and radial cell compressions are
admissible; nodal velocities can be reconstructed by
`4*pi*r_i^2*u_i=-sum_(j<=i) V_j*x_j`. This is an instantaneous state,
not a proposed replacement startup datum.

Both original heat gates are open: `K_l>K_r` and `psi_l>psi_r`.
Therefore `L>0`, without needing a positive lower bound for the gate.
There is no mechanical stress dissipation and no density-gradient cost.
But (P9) gives

\[
 \Delta M_p=-\frac{2\varepsilon}{w_0}
       M_{p,K}(F,z_d,K_d)+o(\varepsilon)>0,
 \qquad L\Delta J_p(q)=-2L\varepsilon^{p-1}<0.           \tag{P11}
\]

Consequently

\[
 \frac{L\Delta M_p}{-L\Delta J_p(q)}
 =-\frac{M_{p,K}(F,z_d,K_d)}{w_0}
               \varepsilon^{2-p}+o(\varepsilon^{2-p})
          \longrightarrow+\infty\qquad(p>2).           \tag{P12}
\]

For every finite multiplier Gamma, the proposed dissipativity estimate

\[
 -a\Delta J_p(f)\Delta f+L\Delta M_p
             +\Gamma L\Delta J_p(q)\le C D(z)          \tag{P13}
\]

fails on this face for sufficiently small epsilon. This remains true if
the right side contains any weighted density-gradient square: it is
zero here. The actual gradient gate cancels from the ratio (P12), so its
vanishing as epsilon tends to zero does not rescue (P13). The failure is
precisely in the coefficient remainder of (P6), including its beta part.
For p=2 the ratio has a finite limit, consistent with the reviewed
quadratic heat absorption.

This refutes a gradient-only interior entropy estimate of the form (P13).
It does not refute an estimate with additional local work, a mixed
entropy, a spatial-gradient energy, or the actual solution launched from
the fixed virgin data.

## 4. Execute the stress-dependent quadratic repair

Let `w=w(f,s)` be a nonnegative smooth proposed level weight; use
`w=(f-k)_+^(p-2)` inside a smooth active region `f>k`, or `w=f^(p-2)`
there. Consider the actual companion

\[
 B_w=\frac\lambda2\sum_i dm\,\phi_iW_i^{-1/2}
                                     q_i^2w(f_i,s),\qquad\lambda>0.
                                                               \tag{P14}
\]

Retain both the f derivative and its heat part. Exact differentiation of
`E_p+B_w` gives the spatial pairing

\[
 \begin{split}
 &-\sum_ea_e\Delta(\phi T_w)\Delta f
                      +\sum_eL_e\Delta(\phi U_w),\\
 T_w={}&J_p(f)+\frac\lambda2\rho\nu W^{-1/2}q^2w_f,\\
 U_w={}&M_p+\lambda wq
               +\frac{\lambda S_K}{2W^{3/2}}q^2w_f.
 \end{split}                                                   \tag{P15}
\]

For example the mechanical part of `B_w'` is
`(lambda/2)*sum dm*phi*W^(-1/2)*q^2*w_f*nu*L_r f`, producing
the second term in `T_w`. Its heat part follows from
`q_t|heat=W^(3/2)H`, `f_t|heat=S_K H`, and
`dm*W*H=L_(i-1)-L_i`, producing the last two terms in `U_w`.
The explicit `w_s` term and the remaining state weights are local time
work; no heat flux has been omitted.

This candidate repair has a new exact obstruction. At constant z, choose
an interior state with `f=F>k`, `q=q_0>0`, and `w_f(F,s)>0`. At fixed f,

\[
 \partial_K T_w
 =\frac\lambda2\rho W^{-1/2}w_f
        \{\nu_Kq_0^2+2\nu q_0 W^{3/2}\}>0.             \tag{P16}
\]

Take neighboring states with `Delta K=h_0>0` and
`Delta f=-t*h_0`, where `t>0` is sufficiently small. They have the
original outward heat gate **closed**, so `L=0`. Taylor expansion gives

\[
 -a\Delta T_w\Delta f
 =a t\{(T_w)_K-t(T_w)_f\}h_0^2+o(h_0^2)>0.             \tag{P17}
\]

Choose t small enough for the bracket to be positive, which is possible
because (P16) is strict. Density-gradient work is zero. The states can be
kept strictly inside the tight bootstrap box as before. Hence a
stress-dependent quadratic q weight does not by itself yield a
dissipative state-only entropy uniformly over the original gate states.
The problem has moved to a mechanical memory-gradient term on a closed
heat face; it has not been eliminated.

There is a useful local necessity statement. Write a smooth cell entropy
as `sum V_i e(x_i,z_i,K_i,s)` and require nonpositive interior spatial
work for all neighboring states at fixed z, including closed heat faces.
In `(f,z,K)` coordinates its mechanical cotangent `e_x` must satisfy

\[
 \left.\partial_K e_x\right|_{f,z}=0.                   \tag{P18}
\]

Otherwise choose `Delta K>0` and choose the sign and arbitrarily small
ratio `Delta f/Delta K` to make `-a*Delta(e_x)*Delta f` positive,
exactly as in (P17). Locally, (P18) forces

\[
 e=\frac{H(f,z,s)}\nu+h(z,K,s),\qquad H_f=e_x.           \tag{P19}
\]

Thus any successful smooth state-only repair preserving mechanical
dissipativity on every closed face must reduce to a stress potential
plus an f-independent memory potential. This necessary condition does
not constrain dynamic estimates that also use an independent spatial
memory-gradient energy.

## 5. A surviving finite-p interior absorption with a constant weight

Here is a positive uniform statement. Fix `p>=2` and arbitrary
nonnegative edge weights eta, supported on faces within the provisional
prefix. Put

\[
 \begin{gathered}
 A_s=2500s^2,\quad R_e=\max(|f_l|,|f_r|),\quad
 D_p=\sum_e\eta_ea_e\Delta J_p(f)\Delta f,\\
 H_q=\sum_e\eta_e\ell_e(\Delta q)^2,\quad
 D_z=\sum_e\eta_ea_e(\Delta z)^2.
 \end{gathered}                                             \tag{P20}
\]

At p=2 interpret `R^0=1`. The elementary scalar inequality

\[
 \Delta J_p(f)\Delta f\ge\tfrac12R_e^{p-2}(\Delta f)^2
                                                               \tag{P21}
\]

holds for arbitrary signed endpoints. For equal signs the quotient is
at least `R^(p-2)`; for opposite signs use
`(1+t^(p-1))/(1+t)>=1/2`, `0<=t<=1`.

The exact coefficient bounds in (H20), (H21), and (H30) of
`heat_absorption.md`, applied to (P6), give

\[
 |\Delta M_p|\le R^{p-2}\{A_0p|\Delta f|
                       +B_0s|\Delta z|+C_0s^2|\Delta q|\},
 \quad A_0=50000,\ B_0=3.1\,10^8,\ C_0=3.7\,10^{10}.
                                                               \tag{P22}
\]

For transparency, before eliminating `Delta K`, one can take the
coefficients
`536*(p-1)+45000`, `2.8325e8*s`, and `6.55e10*s^2`.
Use `|Delta K|<=.55*|Delta q|+326000*s^5*|Delta z|`;
the extra density coefficient is less than `1*s` on `s<=10^-3`.
All constants are deliberately rounded up. This estimate retains the
full alpha and beta remainder; it is not a gate linearization.

Let `D_0=16200` and choose the time-independent multiplier

\[
 \Gamma_p=2+2D_0A_0^2p^2T^4+C_0T^2.                     \tag{P23}
\]

Young's inequality, (P3), and (P21) imply

\[
 \boxed{\quad
 -D_p-\sum_e\eta_e\ell_e\Delta q\Delta M_p
                    -\Gamma_p A_s^{p-2}H_q
 \le-\tfrac34D_p-A_s^{p-2}H_q
       +\frac{D_0B_0^2}{4}s^6
                       \sum_e\eta_ea_eR_e^{p-2}(\Delta z)^2.
 \quad}                                                     \tag{P24}
\]

Indeed the first term in (P22) costs at most
`(1/8)*sum eta*a*R^(p-2)*(Delta f)^2`
plus `2*D_0*A_0^2*p^2*s^4*sum eta*ell*R^(p-2)*(Delta q)^2`.
The density term costs that weighted heat square once, plus
`D_0*B_0^2*s^6/4` times the displayed density square. The last term
costs `C_0*s^2` times the weighted heat square. Since `R<=A_s`,
(P23) leaves the stated negative unweighted heat share. This proves
(P24) for every N and every pattern of open and closed original gates.

The companion generating the last term on the left is

\[
 \frac{\Gamma_p A_s^{p-2}}2
               \sum_i dm\,\phi_i W_i^{-1/2}q_i^2.       \tag{P25}
\]

It is a constant spatial weight, so it creates no new mechanical
cotangent. Its explicit time derivative has the additional local term
`(2p-4)/s` times (P25). Cutoff fluxes, the weighted density term in
(P24), this time term, and the full local reaction must be included in
any evolution or iteration theorem. None is discarded by (P24).

## 6. Why the proved finite-p repair does not give (P1)

The point is the amplitude factor `A_s^(p-2)`, not loss of uniformity
in N. Even if an evolution argument gave the favorable hypothetical
bound

\[
 \sum_i V_i\phi_i\frac{|f_i|^p}{\nu_i}
       \le C_p A_s^{p-2}s^m                            \tag{P26}
\]

with a fixed positive m and `C_p^(1/p)` bounded, its p-th root only
gives the startup stress scale `s^2` as `p` tends to infinity.
The fixed power `s^m` disappears. The same happens with the actual
small quadratic-memory input: the measure of an energy contribution
`A_s^(p-2)*||q||_2^2` disappears under a p-th root, leaving `A_s`.
Thus (P24) is a valid finite-p heat absorption, but (P26) alone cannot
improve the provisional amplitude to `s^(2+theta)`.

To replace `A_s` by the size of an active stress level, one must restore
an f-dependent weight. Its exact additional terms are (P15). A possible
continuation is to control the new closed-face mechanical term using a
level-dependent version of the one-sided K-gradient energy from
`relative_entropy.md`. This has not been proved: if

\[
 F_w=\tfrac12\sum_e a_e\eta_e\bar w_e
                               ((K_l-K_r)^-)^2,
\]

then differentiating its weight introduces, among other terms,

\[
 \frac14\sum_ea_e\eta_e((K_l-K_r)^-)^2
            \{w_{f,l}\nu_l(L_rf)_l+w_{f,r}\nu_r(L_rf)_r\}.
                                                               \tag{P27}
\]

The reviewed unweighted negative-gradient estimate does not contain
(P27). A bound for it by the proposed level energies and dissipations,
uniform in N and near the active-level boundary, is the new specific
obligation. The route remains open with this spatial-gradient repair
deferred; the two counterexamples rule out only gradient-free local
entropy absorptions.

Even a future proof of (P1) would still need the independent prefix and
collar coverage argument on the common time interval. No passage here
establishes (UC) or the downstream all-time floor.

## 7. Dependency and review record

The dependency chain for (P24) is: the unchanged material and gated-flux
definitions; the reviewed state-box and actual-geometry bounds in
`heat_absorption.md`; the exact all-p identity in
`pointwise_continuation.md`; and the elementary finite-edge estimates
proved above. The two obstructions use the same exact constitutive law,
strict admissibility, and one-variable Taylor expansion. No external
regularity theorem or finite-grid experiment is a proof leaf.

| Obligation | Status in this note |
| --- | --- |
| Include heat-dependent stress weight and both coefficient differences | Passed: (P4)--(P9), (P22) |
| Absorb by a separate q-p entropy for p>2 | Refuted in the precise gradient-only form (P13) |
| Repair with a smooth f-dependent quadratic companion alone | Refuted as uniform state-only dissipativity: (P15)--(P19) |
| Finite-p interior absorption by a constant quadratic companion | Proved conditional on the actual provisional state box: (P24) |
| Level-dependent spatial memory-gradient estimate | Open, with exact new term (P27) |
| All-origin positive-power supremum estimate and common prefix closure | Not proved |

Self-review reconstructed the heat and mechanical cotangents separately,
checked the positive and closed gate cases, signed f endpoints in (P21),
strict admissibility of both instantaneous constructions, and the p=2
boundary case. This is a self-audit, not an independent audit. Focused
mathematical proofreading covers this new file only. No earlier note was
edited and no computation is offered as proof of a statement for all N.
Validation checked the 27 unique equation tags, balanced display delimiters
and braces, no trailing whitespace, and scoped `git diff --check`. These
are formatting checks; the proofs above supply the universal edge claims.

Input SHA-256 hashes, paths relative to `stable_stress_search/`:

| Input | SHA-256 |
| --- | --- |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/HANDOFF.md` | `c6a5817d38de46af82fdbfe8bbd58e7160cbded3d073788f9c743f0c84d5962d` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/TARGET.md` | `eda9c4e07e8df39e836013134fb7e0e27cb2a95a43add1c6cc649b6afcfcb06f` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/pointwise_continuation.md` | `a2bc945dc7742faa803b0d7b858096a3424f5945ccef1dc02253c9a850701ea9` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/gradient_symmetrizer.md` | `1cd907f4d47552d794282cce7a42a3382fc81c73c9c6ff314cb962ffca39abb6` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/relative_entropy.md` | `92fb61a920ef28e4e08324dbbcf3495cbf708dcc5f750de866fb1b407a8f56b6` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/heat_absorption.md` | `b98843cec40271ef4a16bdb6c15baf50a43c203d6367fbf3ae72a4d299b74379` |
