# Nonlinear absorption of the actual heat commutator

Owner: delegated heat-commutator continuation. Base checkpoint:
**X48-UC-2026-11-01-B**. Observed starting HEAD:
`7b1880de2caded85da4b8c34d84b5dc6c005650e`. The shared checkout changes
concurrently; the input byte hashes below identify the actual law. Write
scope: this file only. No equation, parameter, initial condition, previous
note, or finite-run artifact was changed. No new collapse grids were run.

**Result.** The coefficient commutator (27) in
[the entropy-energy note](../continuation_2026_11_01/entropy_energy.md) has
an explicit, mesh-uniform nonlinear estimate under the stated provisional
compression bootstrap. Its stress and temperature-gradient contributions
are absorbable, and its remaining contribution is
`1.1e19*s^6*D(log rho)`. The proof uses the exact constitutive inverse and
finite differences, without assuming a compression-gradient estimate. A
material cutoff has a uniform, explicitly bounded quadratic work term.
The dangerous heat-divergence time-weight term can also be folded into
the same edge estimate; the other weight derivatives have favorable
signs. This resolves these named commutators subject to the bootstrap;
it does **not** prove the bootstrap, control the density-gradient and
local-reaction terms in the full energy derivative, or prove the
requested common-time central-quarter assertion.

## 1. Conditional theorem and exact finite-edge setting

Use the unchanged normalized law, `dm=M/N`, `M=pi/3`,
`V_i=dm/rho_i`, and `z_i=log rho_i`. Fix a prefix
`I={1,...,J}`. Assume the actual solution starts at common activation
`rho_i(0)=1`, `K_i(0)=0`, and, for every cell in this prefix,

\[
 2<x_i(v)\le8\quad(0<v\le s),\qquad
 0<s\le T_0:=10^{-3}.                                      \tag{H1}
\]

These are hypotheses on the actual solution through time `s`, rather
than a new initial condition or a changed constitutive branch. Nonnegative
`K` is the original accepted-state domain. On this branch put

\[
 \begin{gathered}
 h=(\rho-1)^2(5-2\rho),\quad W'=h,\quad
 \kappa=\tfrac12\rho Wh,\quad
 g=\frac K{K+1/100},\quad \nu=\kappa(1+g),\\
 P=K\rho^2h,\qquad S=\nu x-2\kappa+P,\qquad
 \psi=KW^{3/2},\\
 \alpha=\frac{S_K}{\rho\nu W}
 =\frac{g'x}{\rho W(1+g)}+\frac2{W^2(1+g)}.              \tag{H2}
 \end{gathered}
\]

Take spatially constant references `S_d(s), psi_d(s)` satisfying

\[
 0\le S_d\le2500s^2,\qquad0\le\psi_d\le3000s^3,
 \qquad f=S-S_d,\quad q=\psi-\psi_d.                    \tag{H3}
\]

A homogeneous reference in the same envelope satisfies these bounds.
Only its spatial constancy and displayed bounds enter this lemma; its
time derivatives are not being estimated here.

For an internal edge `e=(i,i+1)` write
`Delta_e u=u_(i+1)-u_i` and `bar u_e=(u_i+u_(i+1))/2`. Use the actual
geometry and the actual outward heat flux, factored as

\[
 a_e=\frac{(4\pi r_i^2)^2}{dm},\qquad
 L_e=-\ell_e\Delta_e\psi,\qquad\ell_e\ge0.             \tag{H4}
\]

On a positive-flux face,
`ell=D*(4*pi*r_i^2/d_i)*h_i*h_(i+1)*b_i`, with the exact
entropy-gradient gate `0<=b_i<=1` and `D=1/10`. Set `ell=0` on an
inactive face. At a zero potential drop this choice still gives the exact
flux. No derivative of the gate is used, including at its switching faces.

For any nonnegative edge weights `w_e`, supported on edges whose two
endpoints belong to `I`, define

\[
 D_w(u)=\sum_e w_ea_e(\Delta_eu)^2,\qquad
 H_w(u)=\sum_e w_e\ell_e(\Delta_eu)^2.                 \tag{H5}
\]

The nonlinear remainder in (27) obeys

\[
 \boxed{\quad
 \sum_e w_e\ell_e\bar f_e^2(\Delta_e\alpha)^2
 \le 2.5\,10^{13}s^4D_w(f)
      +1.1\,10^{19}s^6D_w(z)
      +1.7\,10^{19}s^4H_w(q).
 \quad}                                                \tag{H6}
\]

In particular, for `0<s<=T_*:=10^(-6)` and `Gamma=1`, the exact
interior spatial pairing (24), with these edge weights, satisfies

\[
 \boxed{\quad
 -D_w(f)-\sum_e w_e\ell_e\Delta_e(\alpha f)\Delta_eq-H_w(q)
 \le-\tfrac14D_w(f)-\tfrac18H_w(q)
             +1.1\,10^{19}s^6D_w(z).
 \quad}                                                \tag{H7}
\]

Both constants and times are deliberately conservative and independent
of `N`, of the first-cell radius, of adjacent cell-width ratios, and of
which heat faces are active. `T_*` is a conditional absorption time;
it is not a common existence or compression-bootstrap time.

## 2. Bootstrap consequences, including the density lower bound

The exact equation `z_t=x` and (H1) give

\[
 e^{2s}\le\rho_i(s)\le e^{8s}\le101/100,
 \quad 2s\le\rho_i-1\le(81/10)s,
 \quad 3/2\le W_i\le151/100.                            \tag{H8}
\]

For example, `exp(v)<=1/(1-v)` for `0<=v<1` proves the upper
density bounds for `8s<=.008`. The exact ramp consequently gives

\[
 11s^2\le h_i\le197s^2<200s^2,\qquad 0\le h_i'\le49s.
                                                               \tag{H9}
\]

The lower bound uses `rho-1>=2s` and
`3-2*(rho-1)>=149/50`. Thus the viscosity lower bound used below is
an integrated consequence of the provisional amplitude hypothesis,
not an assumption of positive activation at time zero.

At a prefix maximum of `K`, no inward face can supply heat: its
entropy-gradient gate requires the inward cell to have larger `K`.
Every outgoing luminosity is nonnegative, including the face leaving
the prefix. Hence `H_i<=0` at such a maximum, irrespective of the
exterior state. Both original heaters are retained. Their exact sum is

\[
 Q=h\{x(x/2-1)+\tfrac12gx^2\}
       \le h(24+3200K).                                 \tag{H10}
\]

The upper right derivative of `K_*=max_(i<=J) K_i` therefore satisfies

\[
 D^+K_*\le197s^2(24+3200K_*),\qquad
 K_*(s)\le\frac{24}{3200}
       \{\exp[(630400/3)s^3]-1\}\le1600s^3.             \tag{H11}
\]

For the last inequality use `exp(A)-1<=A*exp(A)` and
`A<=630400/(3*10^9)<1/4000`; then its cubic coefficient is at
most `1576*4000/3999<1600`. This is the exact prefix argument, not
a temperature-potential maximum principle.

Straight substitution in (H2), using (H8)--(H11), now gives

\[
 \begin{array}{c|c}
 \hbox{coefficient}&\hbox{uniform bound on the state box}\\ \hline
 \kappa&8s^2\le\kappa\le153s^2\\
 \nu&8s^2\le\nu\le306s^2\\
 \kappa_z&0\le\kappa_z\le38s\\
 \nu_z&0\le\nu_z\le76s\\
 \nu_K&0\le\nu_K\le15300s^2\\
 P_z&0\le P_z\le82000s^4\\
 P_K&0\le P_K\le205s^2
 \end{array}                                             \tag{H12}
\]

Here `z` derivatives are taken at fixed `x,K`. For audit of the
largest density derivative, put `w=rho*h/W<=135s^2` and use

\[
 \kappa_z=\kappa(1+w)+\tfrac12\rho^2Wh',\qquad
 P_z=K\rho^2(2h+\rho h').                               \tag{H13}
\]

For instance the first bound is at most
`153s^2*(1+135s^2)+(.5)*(1.01)^2*(1.51)*49s<38s`.
Also

\[
 0\le S\le2448s^2+328000s^5<2500s^2,\quad
 0\le\psi\le3000s^3,\quad
 |f|\le2500s^2,\quad|q|\le3000s^3.                     \tag{H14}
\]

All derivative bounds in (H12) hold on the entire rectangular box
`e^(2s)<=rho<=e^(8s), 0<=K<=1600s^3`; thus the mean-value paths
below remain admissible.

## 3. Exact finite-edge Lipschitz estimate and constitutive inverse

Write `A(K)=g'/(1+g)` and `B(K)=1/(1+g)`. Since `c=1/100`,

\[
 A=\frac c{(K+c)(2K+c)},\quad
 B=\frac{K+c}{2K+c},\quad
 A\le100,\quad |A'|\le30000,\quad |B'|\le100.           \tag{H15}
\]

From `alpha=A*x/(rho*W)+2B/W^2`, `0<=rho*h/W<=1`, and (H8),

\[
 0\le\alpha\le536,\quad
 |\alpha_x|\le67,\quad |\alpha_z|\le1070,\quad
 |\alpha_K|\le161000.                                  \tag{H16}
\]

These are derivatives of the exact coefficient, with no singular
factor `1/h`. Finite differences consequently satisfy

\[
 |\Delta\alpha|\le67|\Delta x|+1070|\Delta z|
                                +161000|\Delta K|.       \tag{H17}
\]

An amplitude hypothesis alone would not bound the first difference on
the right. Here the exact stress supplies the required relation. At
the two endpoints of any edge, subtract `S=nu*x-2*kappa+P` to obtain

\[
 \nu_r\Delta x=\Delta f-x_l\Delta\nu
                          +2\Delta\kappa-\Delta P.      \tag{H18}
\]

Use `x_l<=8`, (H12), and `nu_r>=8s^2`. This gives the genuine
finite-edge estimate

\[
 |\Delta x|\le\tfrac18s^{-2}|\Delta f|
               +86s^{-1}|\Delta z|+15326|\Delta K|.      \tag{H19}
\]

For clarity, the density numerator is at most
`(8*76+2*38)*s+82000*s^4`, and the `K` numerator at most
`(8*15300+205)*s^2`. No intermediate compression value is inferred
by inverting a linearly interpolated stress.

Inserting (H19) in (H17) proves

\[
 |\Delta\alpha|\le9s^{-2}|\Delta f|
                   +5800s^{-1}|\Delta z|
                   +1.2\,10^6|\Delta K|.                \tag{H20}
\]

The inverse powers of `s` are compensated by the small factors `ell`
and `f^2` in the actual product. This compensation is the relevant
structure; a bare uniform bound on `alpha` would not suffice.

Finally `psi=K*W^(3/2)` gives another finite-edge identity,

\[
 W_r^{3/2}\Delta K=\Delta q-K_l\Delta(W^{3/2}).
\]

Since
`|(W^(3/2))_z|<373s^2`, `W_r>=3/2`, and `K_l<=1600s^3`,

\[
 |\Delta K|\le.55|\Delta q|+326000s^5|\Delta z|,
 \qquad
 (\Delta K)^2\le.61(\Delta q)^2
                      +2.13\,10^{11}s^{10}(\Delta z)^2. \tag{H21}
\]

This controls the memory gradient by the actual heat dissipation plus
a still smaller density-gradient term. It does not assert comparability
of signed drops or remove the density dependence of the heat law.

## 4. Actual geometry and absorption

The centroid formula in the unchanged source gives, for every ordered
actual geometry,

\[
 4\pi r_i^2d_i\ge V_i/4,\qquad
 \frac{\ell_e}{a_e}\le4D\rho_i h_i h_{i+1}b_i
                         \le16200s^4.                  \tag{H22}
\]

The first inequality follows already from
`r_i-center_i >= (r_i-r_(i-1))/4` and
`V_i<=4*pi*r_i^2*(r_i-r_(i-1))`. This uses the actual cell
geometry, includes the first positive face, and requires no comparison
with a frozen reference graph. Every edge under discussion is internal,
where `mu_i=dm`; the half outer node mass never enters this ratio.

Square (H20) using `(u+v+w)^2<=3*(u^2+v^2+w^2)`, use
`bar f^2<=2500^2*s^4`, and then (H22). Before eliminating `Delta K`
the result is

\[
 \begin{split}
 \sum_e w_e\ell_e\bar f_e^2(\Delta_e\alpha)^2
 \le{}&2.460375\,10^{13}s^4D_w(f)
       +1.021815\,10^{19}s^6D_w(z)\\
      &+2.7\,10^{19}s^4H_w(K).
 \end{split}                                             \tag{H23}
\]

Use (H21) in the final term. Its additional density contribution is at
most `9.31662e34*s^18*D_w(z)`, which is less than
`.1*s^6*D_w(z)` for `s<=T_0`. The heat contribution is
`1.647e19*s^4*H_w(q)`. Rounding upwards proves (H6).

The first cross term in
`Delta(alpha*f)=bar alpha*Delta f+bar f*Delta alpha` is bounded by
`D_w(f)/2+H_w(q)/2`, because

\[
 \max_e\frac{\ell_e\bar\alpha_e^2}{a_e}
 \le16200\cdot536^2s^4<1\quad(s\le T_0).
\]

Young's inequality bounds the remaining commutator by
`H_w(q)/4` plus the left side of (H6). At `s<=10^(-6)`,
`2.5e13*s^4<1/4` and `1.7e19*s^4<1/8`. Combining these inequalities
with the two negative squares proves (H7).

## 5. A cutoff with explicit finite-edge work

Let `0<=chi_i<=1`, `phi_i=chi_i^2`, and require that every edge with
`bar phi_e>0` have both endpoints in the bootstrap prefix. Pair the
spatial equations with `V_i*phi_i*f_i/nu_i` and
`dm*phi_i*q_i/W_i^(1/2)`, respectively. Exact summation by parts
gives the left side of (H7), with `w_e=bar phi_e`, together with

\[
 B_\phi=-\sum_e\Delta_e\phi\{
      a_e\bar f_e\Delta_ef+
      \ell_e\overline{\alpha f}_e\Delta_eq+
      \ell_e\bar q_e\Delta_eq\}.                        \tag{H24}
\]

No exterior stress work remains when `phi_N=0`, and the heat law has
zero exterior luminosities. The origin contributes zero area. These are
the actual finite graph boundaries.
All cell sums in this localization and the energy below are over `I`;
the paired products are extended by zero outside it. Thus no division
by an inactive exterior viscosity is being defined.

Define `K_chi(u)=sum_e a_e*(Delta_e chi)^2*overline(u^2)_e`.
The elementary inequality

\[
 \frac{(\Delta\phi)^2}{\bar\phi}\le4(\Delta\chi)^2
\]

is interpreted as zero if `bar phi=0`. Young's inequality with stress
share `1/8` and heat shares `1/32` for each of the two heat terms yields

\[
 |B_\phi|\le\tfrac18D_{\bar\phi}(f)
      +\tfrac1{16}H_{\bar\phi}(q)
      +9K_\chi(f)+5.2\,10^5s^4K_\chi(q),
 \qquad s\le T_*.                                      \tag{H25}
\]

For example the unsimplified work bound is the sum of
`(Delta chi)^2*[8*a*bar f^2+32*ell*overline(alpha*f)^2
+32*ell*bar q^2]`. Use
`overline(alpha*f)^2<=536^2*overline(f^2)` and (H22) to obtain
(H25). This controls the cutoff commutators without differentiating the
heat gate.

For a material cutoff `chi_i=chi(theta_i)`,
`theta_i=(i-1/2)/N`, with Lipschitz constant `L_chi`,

\[
 K_\chi(u)\le146L_\chi^2\sum_{i\in I}V_i u_i^2.       \tag{H26}
\]

Indeed `|Delta chi|<=L_chi*dm/M`, so
`a_e*(Delta chi)^2<=144*r_i^4*L_chi^2*dm`.
By (H8), every prefix face has `r_i^3<=3M/(4*pi)=1/4`, hence
`r_i<1`, and `dm<=1.01*V_i`. Each cell occurs in at most two edge
averages, proving (H26) without an `N` factor.

One explicit ceiling-correct choice is `J=ceil(N/2)`, with `chi=1`
for `theta<=9/32`, linear to zero at `theta=3/8`, and zero thereafter.
Then `L_chi=32/3`, every cell `i<=ceil(N/4)` has `chi_i=1`,
and every edge with `bar phi>0` has both endpoints in `I` for all
`N>=32`. In particular `K_chi(u)<=17000*sum_I V_i*u_i^2`.

Combining (H7) and (H25), the complete localized spatial pairing is
bounded above by

\[
 -\tfrac18D_{\bar\phi}(f)-\tfrac1{16}H_{\bar\phi}(q)
 +1.1\,10^{19}s^6D_{\bar\phi}(z)
 +9K_\chi(f)+5.2\,10^5s^4K_\chi(q).                    \tag{H27}
\]

Thus its cutoff work has a uniform quadratic norm bound, including on
the collar. This does not establish smallness of the collar's actual
solution or remove the need to propagate a suitable localized norm.

## 6. The heat part of the time-weight derivative is absorbable too

For the full quadratic energy, the additional weight term cannot simply
be dropped: `nu_t=nu_z*x+nu_K*(Q+H)` contains `H` with no pointwise
bound. It can, however, be included in the shared flux before estimating.
Define

\[
 \beta=\frac{\nu_K}{\rho\nu^2W}
       =\frac{A(K)}{\rho W\nu},\qquad
 F_h=\alpha f-\tfrac12\beta f^2.                         \tag{H28}
\]

For `E_S=(1/2)*sum_i V_i*phi_i*f_i^2/nu_i`, its two heat contributions
combine exactly:

\[
 \begin{split}
 &\sum_i\frac{V_i\phi_i f_i}{\nu_i}S_{K,i}H_i
       -\frac12\sum_i\frac{V_i\phi_i f_i^2\nu_{K,i}}{\nu_i^2}H_i\\
 &\hspace{25mm}=-\sum_e\ell_e\Delta_e(\phi F_h)\Delta_eq.
 \end{split}                                             \tag{H29}
\]

Thus no `K_t`, heat-divergence norm, or heat-Jacobian estimate is
assumed. The same state box gives

\[
 0\le\beta\le9s^{-2},\qquad
 |\beta_z|\le86s^{-3},\qquad
 |\beta_K|\le20000s^{-2}.                               \tag{H30}
\]

Indeed `beta_z=-beta*(1+w+nu_z/nu)`, while
`|beta_K|<=|A'|/(rho*W*nu)+beta*nu_K/nu`. Bounds (H12) and (H15)
give respectively `9s^(-2)*(2+9.5/s)<86s^(-3)` and
`(2500+17212.5)*s^(-2)<20000s^(-2)`.

Use the exact product identity

\[
 \Delta F_h=(\bar\alpha-\bar\beta\bar f)\Delta f+G_e,
 \qquad
 G_e=\bar f\Delta\alpha-\tfrac12\overline{f^2}\Delta\beta.
                                                               \tag{H31}
\]

In particular,

\[
 |\bar\alpha-\bar\beta\bar f|\le24000,
 \qquad
 |G_e|\le23000|\Delta f|+2.9\,10^8s|\Delta z|
                              +6.6\,10^{10}s^2|\Delta K|.
                                                               \tag{H32}
\]

The density coefficient before rounding is
`2500*5800*s+(2500^2/2)*86*s=283250000*s`; the memory coefficient
is `2500*1.2e6*s^2+(2500^2/2)*20000*s^2=6.55e10*s^2`.
Squaring (H32), and repeating (H21)--(H23), yields

\[
 \sum_e w_e\ell_eG_e^2
 \le2.6\,10^{13}s^4D_w(f)+4.2\,10^{21}s^6D_w(z)
                              +8\,10^{21}s^4H_w(q).     \tag{H33}
\]

For audit, the pre-conversion constants are `2.57094e13`,
`4.08726e21`, and `1.3068e22` in front of
`s^4*D(f), s^6*D(z), s^4*H(K)`. The converted memory term adds at
most `4.51e37*s^18*D(z)`, whose coefficient after factoring out
`s^6` is less than `46` on `s<=T_0`. These bounds imply (H33).

At `s<=T_*`, the principal cross term spends at most half of each
square because `16200*24000^2*s^4<1`. Young's inequality for `G`
spends `H_w(q)/4` and the right side of (H33). Its stress coefficient
is less than `1/4`, and its heat coefficient is less than `1/8`.
Consequently (H7) continues to hold with `alpha*f` replaced by `F_h`
and its density coefficient replaced by `4.2e21`.

The cutoff also has the same bound (H25): replace
`overline(alpha*f)` in (H24) by `bar F_h`, and note
`|F_h|<11800*|f|`. The extra coefficient in its stress cutoff work
is at most `32*16200*11800^2*s^4<1` on `s<=T_*`.

For clarity, this gives a full actual first-energy inequality with
explicit remaining terms. In this paragraph take the reference
functions in (H3) to be differentiable for `s>0`. Set

\[
 \begin{gathered}
 E_\phi=\tfrac12\sum_i\frac{V_i\phi_i f_i^2}{\nu_i}
          +\tfrac12\sum_i\frac{dm\,\phi_iq_i^2}{W_i^{1/2}},\\
 \mathcal F_i=\nu_iR_i+S_{z,i}x_i+S_{K,i}Q_i-S_d',\\
 \mathcal G_i=W_i^{3/2}Q_i
             +\tfrac32K_iW_i^{1/2}\rho_i h_i x_i-\psi_d'.
 \end{gathered}                                          \tag{H34}
\]

Here `x_t=L_r S+R` is the unchanged exact compression equation.
Differentiation, followed by (H29), gives its spatial pairing with
`F_h`, its local work

\[
 \mathcal R_\phi=
  \sum_i\frac{V_i\phi_i f_i}{\nu_i}\mathcal F_i
   +\sum_i\frac{dm\,\phi_iq_i}{W_i^{1/2}}\mathcal G_i,    \tag{H35}
\]

and the additional terms

\[
 -\tfrac12\sum_i\frac{V_i\phi_i f_i^2}{\nu_i}
      \left[x_i+\frac{\nu_{z,i}}{\nu_i}x_i
                  +\frac{\nu_{K,i}}{\nu_i}Q_i\right]
 -\tfrac14\sum_i\frac{dm\,\phi_iq_i^2}{W_i^{3/2}}
                                      \rho_i h_i x_i\le0. \tag{H36}
\]

All signs use the actual active branch and both positive heaters;
no sign is asserted for the local work (H35). Combining the estimates,

\[
 \boxed{\quad
 E_\phi'\le-\tfrac18D_{\bar\phi}(f)
             -\tfrac1{16}H_{\bar\phi}(q)
       +4.2\,10^{21}s^6D_{\bar\phi}(z)
       +9K_\chi(f)+5.2\,10^5s^4K_\chi(q)+\mathcal R_\phi.
 \quad}                                                \tag{H37}
\]

This inequality controls all time-weight derivatives of this energy.
It still needs a coupled density-gradient energy and an estimate of
the displayed local work; neither is being hidden in an unspecified
coefficient commutator.

## 7. What this closes and what it leaves open

The specific remainder in entropy-energy (27) no longer requires an
unproved bound on `Delta x`, `Delta K`, or `Delta alpha`: (H6) follows
from amplitude bounds and exact product structure. The positive density
stiffness alone was not used as an unproved regularity theorem. The
remaining `s^6*D(z)` term is of lower order against a density-gradient
energy with coefficient comparable to `1`, `s`, or `s^3`, but that
energy's actual time evolution must still be established.

A bound solely by stress and heat dissipation cannot be inferred from
the completed-square argument: when the stress difference vanishes,
the coefficient difference can still be nonzero through the density,
and the term `-ell*bar f*Delta alpha*Delta q` has no fixed sign.
The density contribution in (H6) is therefore an explicit obligation
for the coupled energy, not a declaration that all spatial terms are
dissipative.

The following implications remain outside this proved lemma:

1. Propagate the actual nonlinear density-gradient energy controlling
   `s^6*D(z)` with the needed weights.
2. Estimate the explicit local work (H35), retaining its cancellation
   with a suitable homogeneous reference and the density coupling.
3. Control the collar's quadratic norm in that
   complete energy, then obtain actual radial pointwise smoothing.
4. Establish the provisional prefix amplitude envelope on one common
   time and close `x_i>=4` through `ceil(N/4)`.

In particular, a common absorption time under (H1) is not the requested
common bootstrap time. No leading-model lemma or finite family of
trajectories is promoted to that assertion.

## 8. Verification, review scope, and provenance

This is an algebraic finite-edge proof. Its dependencies are the exact
source formulas, `z_t=x`, finite maximum calculus, explicit centroid
geometry, the elementary exponential bound, and Young's inequality.
No external theorem, continuum limit, numerical trajectory, or mesh
experiment is a proof leaf.

Self-review reconstructed (H18) before using it, checked all mean-value
paths, the prefix maximum at its outer face, the two inactive heat
branches, the origin, the outer half node, cutoff edge halos, and the
ceiling in the target. Focused mathematical proofreading covers this
new file only. An independent audit of this conditional lemma and of
its eventual use in a complete nonlinear energy remains separate.

The primary self-audit verdict is **conditional on (H1)--(H3)** for
(H6), (H7), (H27), and (H37); the latter also uses differentiable
references. The finite-edge constitutive, geometric, summation, weight,
and cutoff obligations passed this self-review. Propagation of (H1),
the coupled density-gradient estimate, local-work control, and the
actual central pointwise implication are **not addressed** by this
lemma. The dependency chain contains no invocation of those missing
implications.

Supplemental verification used exact rational arithmetic for the
displayed coefficient roundings and the absorption inequalities, and
checked the 37 unique equation tags, balanced display delimiters and
braces. These arithmetic checks do not replace the analytic argument
and contain no trajectory or finite-mesh experiment. Scoped whitespace
validation passed. Focused proofreading found no further routine edits
or unresolved notation issues in this new note.

Input SHA-256 hashes; paths are relative to `stable_stress_search`:

| Input | SHA-256 |
| --- | --- |
| collapse.py | 14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf |
| material.py | 4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390 |
| entropy_transport/transport.py | 2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c |
| entropy_transport/convective_transport.py | ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97 |
| entropy_transport/floor_theorem/continuation_2026_11_01/entropy_energy.md | bb4429ad5f3c9345d2c6d44a7864c407e273caad13ed3643fac5aa822c9990e3 |
| entropy_transport/floor_theorem/continuation_2026_11_01/effective_flux.md | ba03913a2d497fcefc346b8f04cc0da2d128a3f7dee34ee535c36155459f3ba3 |
| entropy_transport/floor_theorem/STATUS.md (base checkpoint) | 758f9f04b3cc6e404442d45d15f79d7542598b9702429dc3100b53dc6085d67c |
