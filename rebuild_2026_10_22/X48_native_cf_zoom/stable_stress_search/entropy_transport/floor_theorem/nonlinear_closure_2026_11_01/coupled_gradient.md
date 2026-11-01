# Coupled density–memory gradient metrics: exact heat defect and a local obstruction

Owner: delegated coupled-gradient continuation. Base checkpoint:
**X48-UC-2026-11-01-B**. Observed HEAD:
`e5f4a22020b90034b79532e5ead3b7d7e9050e78`. The shared checkout changes
concurrently; the final hashes pin the inputs. Write scope: this file only.
No law, parameter, initial condition, previous note, or finite-run artifact
was changed. No collapse grids were run.

**Result.** A positive thermodynamic Hessian does not yield the required
coupled quadratic gradient estimate for this heat law. More generally,
there is no smooth, state-only, positive local Riemann metric on `(z,K)`
whose mechanical-graph gradient energy has a heat derivative bounded above,
on the whole provisional startup state box, by mesh-independent, locally bounded functions
of zeroth- and first-gradient norms. The entropy-gradient gate gives a
rank-one heat principal row whose direction changes with the local density
gradient. A state-only positive metric cannot symmetrize all those rows.
The precise positive defect is fourth order, not the already-recorded sign
failure for plain `D(K)` or `D(psi)`.

This is an obstruction to the stated energy class, not a counterexample to
the specified initial-value problem, a proof that every nonlinear gradient
energy fails, or a disproof of (UC). An estimate using additional
trajectory information, higher mechanical derivatives, or a genuinely
gradient-dependent nonquadratic potential is outside the theorem.

## 1. Exact law and the class being tested

Use `s=t-t_a`, `z=log rho`, `x=-theta`, and the unchanged active-branch law

\[
 \kappa=\tfrac12\rho Wh,\quad g=K/(K+1/100),\quad
 \nu=\kappa(1+g),\quad P=K\rho^2h,\quad
 S=\nu x-2\kappa+P,\quad\psi=KW^{3/2},                 \tag{1}
\]
\[
 x_t=L_rS+R,\qquad z_t=x,\qquad K_t=Q+H,\qquad
 H_i=\frac{L_{i-1}-L_i}{dm\,W_i}.                       \tag{2}
\]

`Q` contains both original heaters. The physical outer luminosity and the
origin luminosity vanish. Write `A_e=4*pi*r_e^2`, `a_e=A_e^2/dm` on
internal faces, `d_e` for the actual centroid separation, and `Delta u=u_r-u_l`.
On an active heat face the exact luminosity is

\[
 L_e=\frac{D A_e}{d_e}h_lh_r b_e(\psi_l-\psi_r),\qquad
 b_e=\frac{\ell_g(K_l-K_r)}
 {d_e[c_g+(K_l+K_r)/2]+\ell_g(K_l-K_r)},                 \tag{3}
\]

where `D=ell_g=1/10`, `c_g=1/100`. Otherwise `L_e=0`. In particular
`L_e=-ell_e Delta psi`, `ell_e>=0`, exactly as in `heat_absorption.md`.

That companion note gives, conditionally on `2<x<=8` in a prefix and
`0<s<=10^(-6)`, a first-energy estimate whose remaining gradient work is
`4.2e21*s^6*D(z)`, together with explicit cutoff and local-reaction work.
Its heat-dependent time weight has already been included in its flux.
The present question is whether adding a coupled `(z,K)` gradient energy
can propagate that density norm without assuming separate `K` diffusion.

The class tested here is

\[
 E_M=\frac12\sum_e a_e\eta_e\,d_e^{,T}M_e d_e,
 \qquad d_e=\binom{\Delta_ez}{\Delta_eK},\qquad
 M_e=M(s;y_l,y_r),\quad y=(z,K),                       \tag{4}
\]

where `eta>=0` is fixed, supported strictly inside the active prefix,
`M` is symmetric and smooth in its state arguments near a warm diagonal,
and `M(s;y,y)` is positive definite there. Here the vector `d_e` in (4)
is distinct from the scalar centroid separation in (3).

This includes positive time weights, thermodynamic-Hessian metrics,
smooth changes to entropy or temperature coordinates, and smooth
state-path averages between the endpoint states. It excludes dependence
on the difference divided by centroid separation, dependence singular at
coincident endpoint states, and energies containing gradients of `x` or
`S`. Such exclusions matter: these are possible ways to go beyond the
theorem, not ruled-out methods. Smooth extra positive geometry factors with a finite nonzero local limit,
uniformly in `N`, do not change the local obstruction. Mesh-vanishing
factors that remove the required gradient coercivity are outside this
claim.

## 2. Exact finite-edge derivative, including all heat coefficient work

Put `m_e=(M_zK,M_KK)` and define

\[
 w_e=a_e\eta_e\,m_e\cdot d_e,
\]
\[
 G_i=w_{i-1}-w_i+
  \frac12\sum_{e\ni i}a_e\eta_e\,
                     d_e^{,T}(\partial_{K_i}M_e)d_e.  \tag{5}
\]

Missing edges have zero weight. This is exactly `partial E_M/partial K_i`
with instantaneous geometry fixed; no coefficient derivative is omitted.
The heat part of the full derivative is consequently

\[
 \boxed{\quad
 (E_M)'_{\rm heat}
   =\sum_iG_iH_i
   =\sum_eL_e\Delta_e\!\left(\frac{G}{dm\,W}\right)
   =-\sum_e\ell_e\Delta_e\psi\,
                         \Delta_e\!\left(\frac{G}{dm\,W}\right).
 \quad}                                                     \tag{6}
\]

In particular (6) includes the `M_K H` terms that a calculation with
frozen thermodynamic Hessian would miss. For completeness the rest of
the derivative is exactly

\[
\begin{split}
 E_M'-(E_M)'_{\rm heat}={}&
 \frac12\sum_ea_e'\eta_e d_e^TM_ed_e
 +\sum_ea_e\eta_e d_e^TM_e\binom{\Delta_ex}{\Delta_eQ}\\
 &+\frac12\sum_ea_e\eta_e d_e^T
 \left[\partial_sM_e+
 \sum_{j\in\{l,r\}}\big((\partial_{z_j}M_e)x_j
                         +(\partial_{K_j}M_e)Q_j\big)\right]d_e.
                                                               \tag{7}
\end{split}
\]

The actual geometry gives `a_e'/a_e=4u_e/r_e=-(4/3)b_e^comp<=0` on
the compressing prefix, with `b^comp` the volume-weighted mean of `x`
inside the face. It is unrelated to the heat gate `b` in (3).
Thus (6)–(7) are exact for the full law, require no `K_t` norm or
coefficient-time-derivative bound, and leave a definite explicit heat
defect to analyze. Relative differences against spatially constant
references give the same leading defect; their derivatives add lower
derivative work.

## 3. Necessary principal sign condition for a positive local metric

Work in an interior interval at positive material radius, so no origin
embedding or boundary issue is involved. At a warm state fix the local
physical gradients

\[
 p=-z_r,\qquad q=-K_r>0,\qquad
 J=\psi_Kq+\psi_zp>0,\qquad
 b(q)=\frac{\ell_gq}{c_g+K+\ell_gq}.                    \tag{8}
\]

The continuum notation here only extracts the principal coefficients of
the exact finite-edge law (3). It is not a replacement evolution law.
The luminosity divided by area has local limit
`mathcal J=C b(q)J`, where `C=D h^2`. Its gradient derivatives are

\[
 D_z=C b\psi_z>0,\qquad
 D_K=C[b\psi_K+b_qJ]>0,\qquad
 b_q=\frac{\ell_g(c_g+K)}{(c_g+K+\ell_gq)^2}>0.         \tag{9}
\]

Consequently the heat row has principal part

\[
 K_t=\gamma(D_z z_{rr}+D_KK_{rr})+
            \hbox{terms of lower differential order},\qquad
 \gamma=1/(\rho W)>0.                                 \tag{10}
\]

For a state-only metric the highest-order part of (6), after a local
summation by parts, is a positive geometric factor times

\[
 -\gamma\,[M_{zK}z_{rr}+M_{KK}K_{rr}]
                  [D_z z_{rr}+D_KK_{rr}].              \tag{11}
\]

State, geometry, and metric derivatives are lower order at the frozen
point. In particular the exact `M_K H` terms in (6) do not alter (11).
The product in (11) is nonnegative for every pair `(z_rr,K_rr)` if and
only if the two rows are positive multiples. Since `M_KK,D_K>0`, this
is equivalent to

\[
 \boxed{\qquad\frac{M_{zK}}{M_{KK}}
   =\eta_h(p,q):=\frac{b\psi_z}{b\psi_K+b_qJ}.\qquad}  \tag{12}
\]

Here is a direct check of necessity. Write `r_M=M_zK/M_KK` and
`r_h=D_z/D_K`. If they differ, take

\[
 v=\binom{1}{-(r_M+r_h)/2}.
\]

Then

\[
 (m\cdot v)(D\cdot v)
       =-\tfrac14M_{KK}D_K(r_M-r_h)^2<0.                \tag{13}
\]

Thus (11) is strictly positive in this high-frequency direction. This
argument tests the full coupled quadratic form, with its density cross
term; it makes no assumption that `D(K)` dissipates separately.

## 4. The gate makes the necessary condition incompatible with a state-only metric

At any fixed warm ramp state `K>0`, `rho>1`, one has

\[
 \psi_K=W^{3/2}>0,\qquad
 \psi_z=\tfrac32K W^{1/2}\rho h>0.
\]

For fixed `q>0` vary `p` while keeping `J>0`. From (12),

\[
 \frac{\partial\eta_h}{\partial p}
 =-\frac{b b_q\psi_z^2}{[b\psi_K+b_qJ]^2}<0.           \tag{14}
\]

The ratio on the left of (12) is determined by the state, whereas the
right side takes distinct values at the same state and two admissible
density gradients, for example `p=0` and any `p>0`. No state-only metric
can satisfy (12) for both. Positive reduced density stiffness does not
remove this dependence: `S_z-S_K*eta_h>0` can hold at both gradients
while the required heat symmetrizer directions differ.

The thermodynamic-Hessian proposal fails particularly explicitly.
For `e(v,sigma)=sigma^3 W(1/v)`, `v=1/rho`, `sigma=K^(1/3)`, pull back
the positive Hessian `D^2_(v,sigma)e` as a quadratic form to `(z,K)`.
The matrix is

\[
 M_{\rm th}=
 \begin{pmatrix}
 K\rho(2h+\rho h')&\rho h\\
 \rho h&2W/(3K)
 \end{pmatrix},\qquad
 \frac{(M_{\rm th})_{zK}}{(M_{\rm th})_{KK}}
       =\frac{3K\rho h}{2W}=\frac{\psi_z}{\psi_K}.      \tag{15}
\]

It is positive definite in the warm ramp. But at every open heat branch,

\[
 0<\eta_h<\psi_z/\psi_K,                               \tag{16}
\]

because `b_qJ>0`. Equations (13) and (16) give an explicit positive
fourth-order direction for this otherwise positive Hessian. A gradient
square in `psi` plus a positive density square has exactly the same row
ratio `psi_z/psi_K`, so it encounters the same obstruction. Smooth changes
to `(z,sigma)` or other state entropy variables merely pull a positive
state-only metric back to the class (4), and do not avoid (14).

## 5. Why first-gradient stress and heat dissipation cannot absorb the defect

The sign test is also an all-mesh obstruction to a bound, not just to
declaring the gradient heat work nonpositive. Fix any `s_0>0` in the
conditional absorption interval, and choose strict interior state values

\[
 2s_0<z_0<8s_0,\qquad 0<K_0<1600s_0^3,
 \qquad 2<x_0<8.                                      \tag{17}
\]

Choose one of two smooth local base profiles through this state, with
the `p,q` choices used above, for which `r_M!=r_h`. A sufficiently small
positive-radius interval lies wholly in the active heat branch and in
the strict state box. The direction `v` from (13) still gives a uniformly
negative row product on a smaller interval. Select a smooth material
cutoff `chi` supported there and put, on the actual equal-mass cells,

\[
 y_i^{(N)}=y_i^0+\varepsilon_N(-1)^i\chi_i v,
 \qquad\varepsilon_N=N^{-3/2},\qquad x_i^{(N)}=x_i^0.   \tag{18}
\]

The ordered actual radii are reconstructed from these positive cell
densities. Every coefficient in the following scaling comes from (3),
(5), and the exact centroid formula. On this fixed interior interval,

\[
 a_e\asymp N,\qquad d_e^{\rm centroid}\asymp N^{-1},\quad
 dm\asymp N^{-1}.
\]

Base state drops are `O(N^(-1))`; the perturbation drops are
`O(N^(-3/2))`. Thus the physical gradient perturbation tends to zero,
both gates stay strictly open, and all zeroth- and first-gradient norms
of these states stay bounded. In fact the perturbation contribution to
every mechanical first-gradient quadratic norm is

\[
 O(N^2\varepsilon_N^2)=O(N^{-1}).                       \tag{19}
\]

To see the higher heat term directly, at frozen coefficients the
alternating perturbation gives

\[
 \delta G_i=4a_i\varepsilon_N(-1)^i\chi_i(m\cdot v)
                          +\hbox{lower-order terms},
\]
\[
 \delta H_i=-\frac{4A_i}{dm\,W_i d_i^{\rm centroid}}
        \varepsilon_N(-1)^i\chi_i(D\cdot v)
                          +\hbox{lower-order terms}.   \tag{20}
\]

There are `asymp N` cells in the interval. Equations (13), (20) give
the positive heat increment

\[
 \sum_i\delta G_i\delta H_i
           =c N^4\varepsilon_N^2+o(N^4\varepsilon_N^2)
           =cN+o(N),\qquad c>0.                        \tag{21}
\]

These asymptotics can be read entirely as finite-edge Taylor expansions:
the gate perturbation is `O(N*epsilon_N)=O(N^(-1/2))`, so its nonlinear
remainder is smaller than the displayed term. State-factor variations
in the luminosity have one fewer difference than its gradient variation;
the same is true of centroid and cumulative-radius variations. The
coefficient-derivative terms in `G` in (5) also have fewer differences.
On the smooth base, `G_i^0=O(N^(-1))`; pairing it with the quadratic
flux remainder is `o(N)`. Cutoff changes and smooth coefficient changes
are lower order too. These statements use an interval away from zero
radius and strict open gates, so no endpoint or switching derivative is
being suppressed. They establish (21) for the exact discrete law.

Meanwhile `E_M`, `D(z)`, `D(K)`, `D(S)`, and `H(psi)` remain bounded.
The remaining terms (7) are bounded: `x` stays smooth, `Q` is a smooth
state function of `(z,K,x)`, and `a'/a` is bounded by the compression
amplitude. The companion first stress/temperature energy has only
first-gradient spatial work, including its heat-weight flux, and also
stays bounded along (18). Its local work is bounded at fixed `s_0`.
Any smooth state-only zeroth-order energy has the same property after
one shared-flux summation by parts.

Therefore no inequality consisting of that first energy plus (4), with
only these zeroth- and first-gradient terms on the right and constants
independent of `N`, can hold throughout the provisional state box.
Multiplication of (4) by any positive power of `s` does not help: fix
`s=s_0` and let `N` increase. Small `K`, small `h`, and the bound
`ell/a<=C*s^4` make `c` small but do not eliminate the unbounded factor
`N` in (21).

This is an analytic sequence of instantaneous admissible states, not a
new integration, grid experiment, or reachable-trajectory construction.
Its force is precisely to exclude a closure justified by the amplitude
state box alone within the specified local metric class.

## 6. Consequence for the actual bootstrap and what remains outside the obstruction

The result identifies the additional structure a successful gradient
route must use. A frozen metric may align its heat row with `eta_h` for
one gradient, but the required alignment is gradient dependent. Simply
replacing the metric coefficient by `eta_h(p,q)` is not yet an energy:
the Hessian with respect to gradients of the proposed energy density,
and the derivatives of the gate-dependent coefficients, must then be
computed. Positive stiffness and a pointwise symmetrizer do not provide
that integrability or the resulting energy identity.

The obstruction permits nonquadratic flux-generated potentials, BV
estimates supplemented by a mechanism converting them to the required
mechanical norm, higher stress derivative dissipation, and estimates
using proved restrictions on gradients along the actual activation
trajectory. No bound for these alternatives is asserted here. In
particular the heat-only unweighted BV contraction in `viscous_energy.md`
does not by itself control `D_a(K)` uniformly in `N`.

The new conclusion is thus stronger and more specific than the previous
plain-gradient sign examples: the whole positive smooth state-only
Riemann-metric continuation of the first stress energy is incompatible
with a state-box-uniform first-gradient closure. It cannot supply the
missing nonlinear bootstrap inequality. The conditional heat absorption
and favorable reduced stiffness remain valid. A common `T`, collar
control, the central pointwise implication, and (UC) remain unproved.

## Verification and pinned inputs

Verification was direct differentiation of (4), exact shared-flux
summation by parts, the rank-one quadratic calculation (13), and the
finite-edge scaling (18)–(21). The thermodynamic pullback in (15) was
checked directly from the displayed Hessian in `entropy_energy.md`.
This is an analytic self-check; no finite trajectory or external theorem
is load-bearing. No independent proof audit is claimed in this file.

SHA-256 paths are relative to `stable_stress_search/`:

| Input | SHA-256 |
| --- | --- |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/entropy_energy.md` | `bb4429ad5f3c9345d2c6d44a7864c407e273caad13ed3643fac5aa822c9990e3` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/heat_absorption.md` | `b98843cec40271ef4a16bdb6c15baf50a43c203d6367fbf3ae72a4d299b74379` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/viscous_energy.md` | `874881bdaeb046fc607d500fc01d2402e8d4db1264c302e647ac137a39a920a1` |
