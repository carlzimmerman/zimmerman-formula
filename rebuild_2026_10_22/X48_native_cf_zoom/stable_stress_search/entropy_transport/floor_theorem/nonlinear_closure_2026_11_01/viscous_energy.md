# Exact nonlinear old-viscosity energy and the remaining memory-gradient term

Owner: delegated nonlinear viscous-energy route. Base checkpoint:
**X48-UC-2026-11-01-B**. The input hashes below pin the unchanged operator;
the shared Git HEAD moves concurrently. Write scope: this file only. No
equation, coefficient, initial datum, previous note, or numerical artifact
was changed, and no new collapse grids were run.

**Result.** There is an exact nonlinear old-stress energy whose weight
derivative contains neither `x_t` nor `K_t`. There is also an exact
actual-geometry estimate propagating `s^3 D(log rho)` from old-stress
dissipation. These are estimates for the actual constitutive function,
not its leading homogeneous expansion. They do not close the full law:
pressure and memory create an unweighted mechanical-graph memory gradient.
Adding a memory-gradient energy requires controlling its heat contribution,
which has no unconditional dissipative sign. The explicit state construction
in Section 6 checks that sign failure, including a closed temperature gate.
It is not a trajectory counterexample. The common central-quarter startup
assertion remains unproved by this route.

## 1. Exact coordinates and moving geometry

Set `s=t-t_a`, `z=log rho`, `x=-theta`, and, on the actual active branch,

\[
 \kappa(z)=\tfrac12\rho W(\rho)h(\rho),\qquad
 g(K)=\frac{K}{K+1/100},\qquad P=K\rho^2h,
\]
\[
 q=\kappa(x-2),\qquad e=\kappa gx+P=gq+2g\kappa+P,
 \qquad S=q+e.                                             \tag{1}
\]

Here `q` denotes the **old** stress, not temperature potential. Throughout
this note `psi=K W^(3/2)` is the temperature potential. The full equations
are retained:

\[
 x_t=L_r S+R,\qquad z_t=x,\qquad K_t=Q+H,
 \quad H_i=\frac{L_{i-1}-L_i}{dm\,W_i}.                      \tag{2}
\]

The two heaters are included in `Q`; `L_i` is the actual outward gated
luminosity. The graph is

\[
 V_i=dm/\rho_i,\quad A_i=4\pi r_i^2,\quad
 a_i=A_i^2/\mu_i,\quad a_0=0,\quad
 (L_r f)_i=\frac{a_i\Delta_i f-a_{i-1}\Delta_{i-1}f}{V_i},
 \quad \Delta_i f=f_{i+1}-f_i.                              \tag{3}
\]

The physical exterior stress is zero; `mu_N=dm/2` is retained. All localized
identities below have support strictly inside a prefix on which `x>2`, so
no exterior active-branch formula is imposed. Its one-cell collar must also
lie in that prefix. The center has `a_0=0`.

The exact primitive from the effective-flux note is

\[
 F(\rho)=\frac{W(\rho)^2-9/4}{4},\qquad F_t=\kappa x,
 \qquad q=F_t-2\kappa.                                    \tag{4}
\]

Thus (1) is the exact nonlinear Kelvin--Voigt coordinate suggested by
that primitive. Define

\[
 \beta(z)=\frac{\kappa_z}{\kappa}
 =1+\frac{\rho h}{W}+\frac{\rho h'}h>0.                    \tag{5}
\]

Differentiating `q`, without differentiating `S`, gives

\[
 \boxed{\quad q_t=\kappa L_r(q+e)+\kappa R+\beta xq.\quad}    \tag{6}
\]

Neither `H` nor `K_t` is discarded: it remains in the evolution of the
actual `K` appearing in `e`. It simply does not occur in the coordinate
change (6).

Two geometry facts used below are exact. Put

\[
 b_i=-\frac{3u_i}{r_i}
   =\frac{\sum_{j\le i}V_jx_j}{\sum_{j\le i}V_j}.
\]

Then

\[
 V_i'=-x_iV_i,\qquad \frac{a_i'}{a_i}=\frac{4u_i}{r_i}
 =-\frac43 b_i.                                          \tag{7}
\]

In particular `a_i'<=0` on a compressing prefix. No spatial derivative of
density or conductance enters (7). The exact positive-square remainder can
also be written, for `i>=2`, as

\[
 R_i=4\pi\rho_i+\frac{x_i^2}{3}
       +\frac23\left(\frac{r_{i-1}}{r_i}\right)^3
                      (x_i-b_{i-1})^2.                   \tag{8}
\]

For `i=1` its last term is zero. To obtain (8), use
`b_i-b_(i-1)=(V_i/sum_(j<=i)V_j)*(x_i-b_(i-1))` in the
previous positive-square formula. Consequently, if a prefix obeys
`c<=x<=U`, then

\[
 0\le R_i\le4\pi\rho_i+U^2/3+\tfrac23(U-c)^2.             \tag{9}
\]

This is an amplitude consequence on an actual prefix, with no unproved
shear regularity assumption.

## 2. An actual nonlinear relative old-stress identity

Let `(z_d(s),x_d(s))` be the spatially homogeneous reference in the base
notes, and put

\[
 \kappa_d=\kappa(z_d),\quad q_d=\kappa_d(x_d-2),\quad
 f=q-q_d,\quad \zeta=z-z_d.
\]

The reference is used only for subtraction; it is not asserted to solve
the postactivation vacuum-boundary problem. Choose a fixed material cell
cutoff `chi_i` with the support and collar described after (3), and define

\[
 E_f=\tfrac12\sum_iV_i\chi_i^2\frac{f_i^2}{\kappa_i}.
                                                               \tag{10}
\]

At every positive time on the active prefix this is finite. Its exact
derivative, obtained from (6), is

\[
\begin{split}
 E_f'={}&-\sum_ea_e\Delta_e(\chi^2f)\Delta_e(f+e)\\
 &+\sum_iV_i\chi_i^2 f_i
       \left(R_i-\frac{q_d'}{\kappa_i}
                  +\frac{\beta_ix_iq_d}{\kappa_i}\right)\\
 &+\frac12\sum_iV_i\chi_i^2
                  \frac{x_i(\beta_i-1)}{\kappa_i}f_i^2.
\end{split}                                                   \tag{11}
\]

Here the `e` inside `Delta_e(f+e)` is the correction stress in (1);
the edge subscript on `Delta_e` is unrelated. Spatial constancy of `q_d`
on the cutoff collar is the reason it does not enter that difference.
The proof uses the exact formula

\[
 \left(\frac{V_i}{\kappa_i}\right)'
    =-x_i(1+\beta_i)\frac{V_i}{\kappa_i}.                 \tag{12}
\]

Thus this relative energy does avoid time derivatives of state weights
that would require estimates for `x_t` or `H`. It does **not** have a
nonpositive complete derivative: `beta~1/s`, and its local terms must be
handled with their actual activation scaling.

For example, with bars denoting arithmetic endpoint means,

\[
\begin{split}
 -\sum_ea_e\Delta_e(\chi^2f)\Delta_e(f+e)
 ={}&-\sum_ea_e\overline{\chi^2}_e(\Delta_ef)^2\\
 &-\sum_ea_e\overline{\chi^2}_e\Delta_ef\Delta_ee\\
 &-\sum_ea_e\bar f_e\Delta_e(\chi^2)\Delta_e(f+e).
\end{split}                                                   \tag{13}
\]

The last line is the explicit cutoff work. No boundary work was silently
set to zero. On a compressing prefix `r_i` decreases, and a cutoff with
`|Delta chi|<=L_chi/N` has a mesh-uniform quadratic geometric cost:
`a_i*(Delta chi)^2 <=144*r_i^4*rho_i*L_chi^2*V_i` on internal
faces, since `dm=pi/(3N)`. This bounds the usual cutoff squares under
the amplitude envelope; it does not resolve the second line of (13).

The spatially local density error is also controlled by the same
coordinate, without differentiating a state coefficient. Define

\[
 d_i=-q_d\frac{\kappa_i^{-1}-\kappa_d^{-1}}{z_i-z_d}\ge0,
                                                               \tag{14}
\]

using the continuous divided-difference value when `z_i=z_d`. Then

\[
 \zeta_i'=\frac{f_i}{\kappa_i}-d_i\zeta_i,
\]
\[
 \left(\tfrac12\sum_iV_i\chi_i^2\zeta_i^2\right)'
 =\sum_iV_i\chi_i^2\frac{\zeta_if_i}{\kappa_i}
    -\sum_iV_i\chi_i^2(d_i+x_i/2)\zeta_i^2.                \tag{15}
\]

These formulas are for the full actual solution wherever the active
prefix hypothesis holds. Their validity does not require setting `e=0`.

## 3. Exact propagation of a time-weighted density gradient

Let `eta_e>=0` be fixed edge cutoff weights supported on internal prefix
edges, and write

\[
 D_\eta(v)=\sum_ea_e\eta_e(\Delta_ev)^2.
\]

On an edge, the identity `x=2+q/kappa` gives exactly

\[
 (\Delta_ez)'=A_e\Delta_ef-B_e\Delta_ez,
\]
\[
 A_e=\overline{\kappa^{-1}}_e>0,\qquad
 B_e=-\bar q_e\frac{\Delta_e(\kappa^{-1})}{\Delta_ez}\ge0.
                                                               \tag{16}
\]

At a zero density difference the quotient is evaluated by continuity.
This is an exact nonlinear edge damping; it does not replace `kappa`
by a homogeneous reference. Since `q>0` and `kappa` increases, `B_e`
has the displayed sign even when the two cells have different `x`.

Suppose, conditionally, an actual compressing prefix satisfies

\[
 2<c\le x_i(v)\le U\quad(0<v\le s\le T),\qquad
 UT\le\log(5/4).                                         \tag{17}
\]

Then `rho_i(0)=1` and `z_t=x` imply
`cs<=z_i<=Us`, `cs<=rho_i-1<=e^(UT)Us`, and the exact ramp gives

\[
 \kappa_i(s)\ge k_-s^2,\qquad k_-:=15c^2/8>0.              \tag{18}
\]

Indeed `rho-1<=1/4`, `h=(rho-1)^2(3-2(rho-1))`, and `W>=3/2`.
The lower bound extends to the open assumption `x>2` by taking `c=2`
for (18); strict `c>2` is needed only for a quantitative positive lower
bound on `B_e`.

For any fixed `lambda>0`, define

\[
 E_\nabla=\frac{\lambda s^3}{2}D_\eta(z).
\]

Equations (7) and (16) imply, for every `epsilon>0`,

\[
\begin{split}
 E_\nabla'={}&\frac3sE_\nabla
       +\frac{\lambda s^3}{2}\sum_ea_e'\eta_e(\Delta_ez)^2\\
 &+\lambda s^3\sum_ea_e\eta_e
                 (A_e\Delta_ez\Delta_ef-B_e(\Delta_ez)^2)\\
 \le{}&\epsilon D_\eta(f)
       +\left(3+\frac{\lambda}{2\epsilon k_-^2}\right)
                              \frac{E_\nabla}{s}.
\end{split}                                                   \tag{19}
\]

The second line is the complete cross term; Young's inequality uses
`A_e<=1/(k_-s^2)`. Both the geometry term and the `B_e` term have
favorable signs and were only dropped in the last line. In particular a
remainder `C*s^6*D_eta(z)` from the heat commutator is
`(2C/lambda)*s^3*E_nabla`, which is a lower-order local energy term.
It does not itself prevent a combined time-weighted estimate.

This resolves the **old-stress** density-gradient energy step. The
quantity dissipated by (11) is `D(f)` only after controlling the full
correction-stress cross term in (13). That qualification is essential.

## 4. Where restoring the whole stress changes the graph norm

The exact correction has

\[
 e=gq+2g\kappa+P,\qquad
 e_K\big|_{q,z}=g'(q+2\kappa)+\rho^2h>0.                 \tag{20}
\]

Near activation its state-box size is `e=O(s^5)` and
`e_K=O(s^2)`. Its spatial difference is nevertheless part of
`-sum a Delta f Delta e`. Young's inequality asks for a term of the
form

\[
 C s^4D_\eta(K),\qquad
 D_\eta(K)=\sum_ea_e\eta_e(\Delta_eK)^2.                  \tag{21}
\]

This is the mechanical graph norm. Actual heat dissipation is instead

\[
 H_\eta(\psi)=\sum_e\ell_e\eta_e(\Delta_e\psi)^2,
 \qquad L_e=-\ell_e\Delta_e\psi,\quad\ell_e\ge0.
                                                               \tag{22}
\]

The exact estimate `ell_e/a_e <= C*s^4` is an **upper** bound. It
cannot control (21) by (22); `ell_e` can be zero on a face with a
nonzero memory difference. The small amplitude `K=O(s^3)` does not
bound `D_a(K)` uniformly over arbitrary meshes. No such inference is
used here.

This is the extra difficulty introduced by using the old coordinate to
avoid `K_t` in (12). The companion heat-absorption route uses full stress
instead, folds the heat part of its weight derivative into an exact
flux, and avoids (21) in that particular first energy. Its remaining
density-gradient term still needs propagation. At fixed total stress,

\[
 x_S=1/\nu,\qquad x_z=-S_z/\nu,\qquad x_K=-S_K/\nu,
 \qquad \nu=\kappa(1+g).                                  \tag{23}
\]

Thus propagation by `z_t=x` introduces a mechanical `Delta K` term
with coefficient `S_K/nu=O(1)`. Transforming the density coordinate to
cancel that coefficient adds a heat-divergence term to its evolution.
One must estimate the resulting spatial derivative of `H`; merely
renaming the density coordinate does not remove it.

## 5. Adding a memory-gradient energy: the exact heat term

A natural continuation is an energy containing
`s^2*D_a(K)`: then (21) has size `s^2` times that energy, and the
local heater-gradient terms have the appropriate time powers. The heat
contribution to this proposal is not automatically nonpositive.

Put `p_i=K_i-K_(i+1)` on internal faces and first omit a cutoff. At
fixed instantaneous geometry,

\[
 (p_i)'\big|_{\rm heat}
 =\frac{L_{i-1}}{dm W_i}
 -L_i\left(\frac1{dm W_i}+\frac1{dm W_{i+1}}\right)
 +\frac{L_{i+1}}{dm W_{i+1}}.                              \tag{24}
\]

For the uncut gradient energy the exact heat work is

\[
 \mathcal T_K
 =\left.\frac d{ds}\frac12\sum_{i=1}^{N-1}a_ip_i^2
                                                  \right|_{\rm heat}
 =\sum_{i=1}^{N-1}a_ip_i
 \left[\frac{L_{i-1}}{dm W_i}
 -L_i\left(\frac1{dm W_i}+\frac1{dm W_{i+1}}\right)
 +\frac{L_{i+1}}{dm W_{i+1}}\right].                      \tag{25}
\]

Moving-geometry terms `a_i' p_i^2/2` have the favorable sign (7)
on the bootstrap prefix and are separate from (25). Localization adds
the corresponding explicit cutoff weights. Neither changes the fact
that the heat-only quadratic expression need not be nonpositive.

For comparison, one exact weaker estimate does follow from the outward
gate: heat cannot increase the *unweighted total variation* of `K`.
Since `L_i>0` implies `p_i>0`, summing (24) against a subgradient of
`|p_i|`, with missing endpoint signs set to zero, gives

\[
 \left.D^+\sum_{i=1}^{N-1}|p_i|\right|_{\rm heat}\le0.       \tag{26}
\]

Each nonzero `L_i` is multiplied by a sum of nonpositive neighboring
sign differences. At `p_i=0`, the gate gives `L_i=0`, so (24) gives
`p_i'|heat>=0`; choose its subgradient to be `+1`. This equals the
upper directional derivative of its absolute value, including at zero.
The argument allows arbitrary positive `W_i` and the actual gated flux.
It does not upgrade (26) to the mechanically weighted quadratic norm
in (21), whose face weights grow with the mesh.

## 6. Exact sign failure with the temperature gate retained

Here is a local admissible-state construction showing why the heat term
in (25) cannot simply be dropped. It is not an integration, a new grid,
or a claim about the specified trajectory. Choose three consecutive
active-ramp cells with

\[
 W_1=W_2=W_l<W_3=W_h,\qquad
 (K_1,K_2,K_3)=(k+\varepsilon,k,k-p),
\]
\[
 k>0,\qquad 0<p<k\{1-(W_l/W_h)^{3/2}\},\qquad
 0<\varepsilon<\frac{a_2p}{2a_1}.                         \tag{27}
\]

Here the labels `1,2,3` are local cell labels; the two internal
conductances are their actual positive `a_1,a_2`. Face 1 has an
outward-decreasing `K` and a positive temperature-potential drop, so
`L_1>0`. Face 2 has `K_2>K_3`, but
`K_3 W_h^(3/2)>K_2 W_l^(3/2)`; its temperature gate is closed and
`L_2=0`. Choose neighboring endpoint differences zero so all adjacent
luminosities and their gradient-energy contributions vanish. Formula
(25) then gives exactly

\[
 \mathcal T_K=\frac{L_1}{dm}
 \left[-a_1\varepsilon\left(\frac1{W_1}+\frac1{W_2}\right)
                         +\frac{a_2p}{W_2}\right]>0.       \tag{28}
\]

The densities determine a valid ordered geometry by summing positive
cell volumes; the actual conductances in (27) are those of that
geometry. The memory levels can be scaled down to fit any positive
bound `K<=C_K*s^3`, and the two density levels can be chosen inside
any nontrivial active startup density box. Consequently the construction
also occurs within the provisional amplitude *state box*. It does not
show it is reachable from homogeneous activation.

The positive quantity in (28) may still admit a useful bound involving
density differences, lower-order memory gradients, and a higher heat
dissipation. No such nonlinear commutator estimate has been proved in
this note. The construction only rejects the unproved sign assertion.

Replacing `D_a(K)` by `D_a(psi)` does not create an automatic sign
either. For a mirror construction take

\[
 W_1=W_2=W_h>W_3=W_l,\qquad
 (K_1,K_2,K_3)=(k+\varepsilon,k,k+p),
\]
\[
 0<p<k\{(W_h/W_l)^{3/2}-1\},\qquad
 \Pi_2:=kW_h^{3/2}-(k+p)W_l^{3/2}>0,
\]
\[
 0<\varepsilon<\frac{a_2\Pi_2}{2a_1W_h^{3/2}}.             \tag{29}
\]

Face 1 is active. Face 2 has a positive potential drop `Pi_2`, but
`K_2<K_3`, so its entropy-gradient gate closes: `L_2=0`. Under heat
alone `psi_i'=sqrt(W_i)*(L_(i-1)-L_i)/dm`, giving

\[
 \left.\frac d{ds}\frac12D_a(\psi)\right|_{\rm heat}
 =\frac{\sqrt{W_h}L_1}{dm}
       [-2a_1\varepsilon W_h^{3/2}+a_2\Pi_2]>0.              \tag{30}
\]

Both gate mechanisms therefore matter in a proposed higher-gradient
estimate. Equations (28) and (30) do not rule out a coupled gradient
energy with density cross terms, or a bound on its positive part by
lower-order density work. They rule out dropping the heat term in
either plain gradient square.

## 7. Exact status and verification

Equations (11), (15), and (19) give a new actual nonlinear viscous-energy
route, including moving geometry and an explicit density-gradient energy.
They require no time derivatives of a compression- or memory-dependent
weight. The route does not establish a full-law closed localized energy:
(21), or an estimate for the heat work (25) after adding a memory-gradient
energy, remains required. The companion full-stress energy has a different
version of the same density-gradient propagation problem, described in
(23). A further local pointwise estimate would still be necessary after
closing the energy; the radial Nash obstruction in the base entropy note
has not disappeared.

In particular no common `T>0` with `x_i>=4` for all
`i<=ceil(N/4)`, all `N>=32`, is proved here. No leading-model theorem,
spatially homogeneous postactivation extension, or assumed mesh-uniform
regularity theorem is substituted for that assertion.

Verification: direct differentiation and finite-graph summation by parts
give the displayed identities. Exact symbolic algebra checked the
coefficient of `f^2` in (11), the two-cell identity (16), the conversion
of the geometric square to (8), and the heat-work expressions (28)
and (30).
These checks are algebraic self-checks, not finite-grid trajectory evidence.
Mathematical proofreading covered this file only, with no claimed
independent proof audit.

SHA-256 paths are relative to `stable_stress_search/`:

| Input | SHA-256 |
| --- | --- |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |

The exact primitive and graph conventions were read from
`continuation_2026_11_01/effective_flux.md`,
`continuation_2026_11_01/entropy_energy.md`, and
`startup_energy_route.md`. The companion `heat_absorption.md` was read
for coordination; its changing text is not a pinned proof input to the
identities proved above.
