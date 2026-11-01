# Flux-generated energy, and a one-sided entropy closure of the memory-gradient term

Base: **X48-NLC-2026-11-01-B**. Write scope: this file only. The unchanged
material, momentum, heater, and outward heat laws are used throughout. No new
collapse grid, integration, modified initial datum, or constitutive law is used.

**Result.** The gradient-dependent flux potential has the exact heat identity
below, including its mean-state term. Its gate-mean derivative generally has a
logarithmic factor; the proposed bound without that factor is false. A density
completion cancels the saturated-branch density defect but creates explicit
inactive-face work, so that proposal is not asserted to close.

There is, however, a simpler actual nonlinear estimate for the particular
mechanical memory-gradient cost. Local quadratic entropy dissipates `L*(K_l-K_r)`.
Together with a one-sided negative-gradient energy, this controls
`s^4 D_a(K)` up to `O(s^4)` forcing and `O(s^14) D_a(log rho)`, uniformly in
every `N`, including the actual first face. Its heat collar work has a favorable
sign for an outward-decreasing material cutoff. This resolves that named
gradient cost under the provisional prefix envelope. It does **not** by itself
close the singular local-reaction estimate, prove a common prefix interval, or
give the pointwise central-quarter assertion (UC).

## 1. Exact face variables and scope

Assume, conditionally, an actual prefix and its required collar satisfy
`2<x_i<=8` on `0<s<=T<=10^-3`. Use

\[
 z=\log\rho,\quad z_t=x,\quad K_t=Q+H,\qquad
 H_i=\frac{L_{i-1}-L_i}{dm\,W_i},\qquad dm=\frac{\pi}{3N}.
 \tag{1}
\]

Both original heaters are retained:

\[
 Q=h\{x(x/2-1)+\tfrac12g(K)x^2\},\quad
 g=\frac K{K+1/100},\quad
 \kappa=\tfrac12\rho Wh,\quad
 S=(1+g)\kappa x-2\kappa+K\rho^2h.                 \tag{2}
\]

The established prefix consequences are

\[
 2s\le z\le8s,\quad 1\le\rho\le1.01,\quad \tfrac32\le W\le1.51,\quad
 11s^2\le h\le200s^2,\quad 0\le K\le1600s^3,
 \quad |(W^{3/2})_z|\le373s^2.                    \tag{3}
\]

For one internal face let `A_f=4*pi*r_f^2`, `d` be the actual centroid
separation, and define

\[
 q=K_l-K_r,\quad k=(K_l+K_r)/2,\quad
 A=(W_l^{3/2}+W_r^{3/2})/2,\quad B=W_l^{3/2}-W_r^{3/2},
 \quad J=Aq+Bk=\psi_l-\psi_r,
\]
\[
 C=\frac{D A_f}{d}h_lh_r,\quad D=\frac1{10},\quad
 \ell_g=\frac1{10},\quad c_g=\frac1{100},\quad
 \tau=\frac{d(c_g+k)}{\ell_g},\quad b(u)=\frac u{\tau+u}.
                                                               \tag{4}
\]

The exact outgoing luminosity is `L=C*b(q)*[J]_+` if `q>0`, and zero
otherwise. The use of `q` in this note is a memory drop; the old stress is
denoted `p=κ(x-2)` below. No smooth state-only metric assumption is made.

## 2. Flux potential: complete derivative and collar work

For `q>0` put

\[
 U(q,k;C,A,B,d)=C\int_0^q\frac u{\tau+u}[Au+Bk]_+\,du,
 \qquad U=0\quad(q\le0).                              \tag{5}
\]

Then `U_q=L` exactly. Write

\[
 I=\int_0^q b(u)\mathbf1_{Au+Bk>0}\,du,\qquad
 G=\int_0^q\frac{u[Au+Bk]_+}{(\tau+u)^2}\,du.
\]

Every derivative needed in the full law is retained:

\[
 U_k=CBI-C\frac d{\ell_g}G,\quad
 U_A=C\int_0^q b(u)u\mathbf1_{Au+Bk>0}\,du,\quad
 U_B=CkI,\quad U_C=U/C,\quad
 U_d=-C\frac{c_g+k}{\ell_g}G.                         \tag{6}
\]

At switching faces use the continuous first derivative or the corresponding
one-sided identity. In particular `U_q=U_k=0` at `q=0`. The full derivative is

\[
 \begin{split}
 U'={}&L(Q_l-Q_r)+U_k\overline Q
       +L(H_l-H_r)+U_k\overline H\\
 &+U_A A'+U_B B'+(U/C)C'+U_d d'.
 \end{split}                                                    \tag{7}
\]

Here `A',B',C',d'` are the actual geometry/density derivatives, not frozen
coefficients. More explicitly,

\[
 (W_i^{3/2})'=\tfrac32W_i^{1/2}\rho_i h_i x_i,\qquad
 \frac{C'}C=\frac{2u_f}{r_f}-\frac{d'}d
       +\frac{\rho_lh_l'}{h_l}x_l+\frac{\rho_rh_r'}{h_r}x_r.
                                                               \tag{8}
\]

The `h'` in (8) is differentiation with respect to density. The centroid
derivative is the derivative of the source's volume-centroid formula.
Neither `K_t` nor a heat term is hidden in (8).

Without a cutoff, exact shared-flux summation gives

\[
 \boxed{\quad
 \left(\sum_eU_e\right)'_{\rm heat}
 =-\sum_i dm\,W_i H_i^2
       +\frac12\sum_e U_{k,e}(H_l+H_r).
 \quad}                                                        \tag{9}
\]

For fixed face weights `η_e`, set
`ηbar_i=(η_(i-1)+η_i)/2`, with missing weights zero. The complete localized
version of (9) is

\[
 \begin{split}
 \left(\sum_e\eta_eU_e\right)'_{\rm heat}
 ={}&-\sum_i dm\,W_i\bar\eta_iH_i^2\\
 &+\frac12\sum_i(\eta_i-\eta_{i-1})(L_i+L_{i-1})H_i\\
 &+\frac12\sum_e\eta_eU_{k,e}(H_l+H_r).
 \end{split}                                                   \tag{10}
\]

Thus localization adds actual heat collar work. For squared cutoffs
`η=χ^2` with `χ` varying by `O(1/N)` per material cell, its quadratic Young
remainder is bounded by
`C_cut*s^4*sum L_e J_e`, using `L_e^2/a_e<=16200*s^4 L_eJ_e` and the
actual geometry; no origin or adjacent-width regularity is required.

There is also an exact skew form, useful before applying Young's inequality.
Set `γ_e=U_(k,e)/L_e` on active faces and zero otherwise. For constant `W`,

\[
 \frac12\sum_eU_{k,e}(H_l+H_r)
 =\frac1{2dm\,W}\sum_i(\gamma_i-\gamma_{i-1})L_iL_{i-1}.
                                                               \tag{11}
\]

For variable `W`, add
`sum_e γ_e L_e^2*(1/W_r-1/W_l)/(2dm)` and replace `1/W` in the displayed
cross term by `1/W_i`. This identity includes all neighboring-flux
cancellation; it does not give the missing sign by itself.

## 3. What the mean derivative actually permits

The density contribution in (6) satisfies

\[
 |CBI|\le\frac{|B|}{A}L.                              \tag{12}
\]

If `B>=0`, use `I<=q*b(q)` and `J>=Aq`. If `B<0`, the integral starts at
`q_0=-Bk/A`; use `I<=b(q)*(q-q_0)` and `J=A*(q-q_0)`.

The gate contribution does **not** in general satisfy
`C*(d/ell_g)*G <= (d/ell_g)*L`. The valid general bound is

\[
 C\frac d{\ell_g}G
 \le\frac d{\ell_g}L\,g_0(q/\tau),\qquad
 g_0(R)=\frac{1+R}{R}\log(1+R)-1
       \le\log(1+R).                                    \tag{13}
\]

Use the continuous value `g_0(0)=0`.

Indeed replace `[Au+Bk]_+` in `G` by its endpoint maximum `J`, and
integrate `u/(τ+u)^2`. If `B<=0`, the stronger bound without `g_0` does
hold by comparing `(u-q_0)/(q-q_0)<=u/q` and integrating
`u^2/(τ+u)^2`.

For the failure of the stronger general claim, take `B>0`, keep
`0<q<<Bk/A` fixed and let `τ` decrease. The `Bk` part of `G` is

\[
 Bk\{\log(1+q/\tau)+\tau/(\tau+q)-1\},
\]

whereas `L/C` tends to `Aq+Bk`. Their ratio is unbounded. Endpoint
memories `K_l=k+q/2,K_r=k-q/2` remain nonnegative. Ordered equal-mass
geometries have `d->0` at a fixed interior material location, so this is
an admissible analytic face comparison, not a trajectory experiment.
The prefactor `d` remains present: this calculation refutes the proposed
constant-one inequality, not every mesh-uniform absorption estimate.

For example, the direct finite-edge Young bound from (9) is

\[
 E_{U,\rm heat}'\le-(1-\epsilon)\sum_i dm\,W_iH_i^2
 +\frac1{8\epsilon\,dm}\sum_e
       U_{k,e}^2(1/W_l+1/W_r).                          \tag{14}
\]

Using (12)--(13), the remaining quantities are explicitly a logarithmically
weighted `sum L*J` and the mixed term
`sum (A_f*Delta z/dm)^2*L*J`, with coefficients of order `s^4` and
`s^8`, respectively. Neither is simply `D_a(z)`. Keeping (11), or another
coupled completion, may improve (14); no impossibility result for doing so
is asserted here.

A concrete saturated-branch completion is

\[
 \mathscr U=A U+\frac C2(B_+k)^2.                       \tag{15}
\]

On `q>0` its heat work equals

\[
 -\sum_i dm\,W_i^{5/2}H_i^2
 +\frac12\sum_e\mathscr R_e(H_l+H_r),\qquad
 \mathscr R=A U_k+C B_+^2k-BL,                         \tag{16}
\]

provided all faces included in the summation are active; otherwise retain
the missing-face terms. The row identity behind (16) is
`A*L*(H_l-H_r)+(B/2)*L*(H_l+H_r)
 =L*(W_l^(3/2)H_l-W_r^(3/2)H_r)`.
As `b->1` on an open face, `mathscr R->0`: for `B<0` the temperature
threshold is essential to this statement. However, on `q<=0` the added
baseline contributes `C B_+^2 k*Hbar` while `L=U_q=0`. Consequently (16)
cannot be extended through inactive faces by declaring their defect zero.
No complete estimate for that continuation is claimed.

## 4. An exact entropy identity that bypasses the mean defect

For a fixed nonnegative material cell cutoff `φ_i` define

\[
 E_K=\frac12\sum_i dm\,W_i\phi_iK_i^2,
 \qquad D_K^{\rm heat}=\sum_e\bar\phi_eL_eq_e.
                                                               \tag{17}
\]

The full, actual nonlinear derivative is

\[
 \boxed{\quad
 E_K'=-D_K^{\rm heat}
 +\sum_e\Delta_e\phi\,L_e\bar K_e
 +\sum_i dm\,\phi_i
   \{W_iK_iQ_i+\tfrac12\rho_i h_i x_iK_i^2\}.
 \quad}                                                        \tag{18}
\]

There is no mean-state heat defect in (18). If `φ` decreases outward,
the heat collar term is nonpositive, since `L>=0,K>=0`. All nonzero faces
in (18) have `q>0`, so `D_K^heat>=0`, including both gates. On (3),
`Q<=11200*s^2`, giving the conservative bound

\[
 E_K'+D_K^{\rm heat}\le3\,10^7 M_\phi s^5,
 \qquad M_\phi=\sum_i dm\,\phi_i,\quad s\le10^{-3}.
                                                               \tag{19}
\]

This is a localized statement for the actual solution. It uses no positive
lower bound on `K` and remains valid at activation.

## 5. All-mesh conversion to the required mechanical gradient

For internal faces `a=A_f^2/dm`. The actual centroid separation obeys

\[
 \frac{dm}{4\rho_l}\le A_fd\le3V_l+V_r\le4dm.
                                                               \tag{20}
\]

The lower bound was proved in the input heat note. For the upper bound,
`d<=width_l+width_r`, `A_f*width_l<=3V_l`, and
`A_f*width_r<=V_r`. These inequalities include the first internal face.
Consequently

\[
 \frac Ca\ge\frac D4h_lh_r\ge3s^4,\qquad
 \sum_e a_ed_e^2\le16M.                              \tag{21}
\]

Fix any physical gradient threshold `ε_0>0`, independent of `N`, and put

\[
 \beta_0=\frac{\ell_g\epsilon_0}
 {c_g+1600T^3+\ell_g\epsilon_0}>0.
\]

Split the faces with `q>0` into three classes:

1. `q<=2|B|k/A`: from (3), `q<=6.64*10^5*s^5*|Delta z|`.
2. `q<=ε_0*d`: their sum `s^4*a*q^2` is at most
   `16M*ε_0^2*s^4`.
3. The remaining faces: `J>=Aq/2`, `b>=β_0`, and (21) gives
   `L*q>=2.7*β_0*s^4*a*q^2`.

The first class includes every temperature-closed face with `q>0`.
The classes may overlap; assigning an overlapping face to the first one
only strengthens the resulting estimate. For fixed `0<=η_e<=1`, define

\[
 D_\eta(z)=\sum_ea_e\eta_e(\Delta_ez)^2,\quad
 F_- =\frac{s^2}{2}\sum_ea_e\eta_e(q_e^-)^2,
 \qquad q^-=\max(-q,0).
\]

The exact finite-edge consequence is

\[
 \boxed{\quad
 s^4D_\eta(K)\le2s^2F_-
 +\frac{10}{27\beta_0}\sum_e\eta_eL_eq_e
 +16M\epsilon_0^2s^4
 +4.5\,10^{11}s^{14}D_\eta(z).
 \quad}                                                        \tag{22}
\]

All constants are independent of `N`, the first radius, and the set of
open gates. Taking `η_e=barφ_e` matches (18). This estimate uses nonlinear
flux dissipation, not a false lower bound on `ell_e/a_e` on all faces.

The preexisting temperature-potential dissipation can also be used directly.
On the third class,
`L*J=C*b*J^2>=2.4*β_0*s^4*a*q^2`. Thus the alternative form is

\[
 s^4D_\eta(K)\le2s^2F_-
 +\frac5{12\beta_0}\sum_e\eta_eL_eJ_e
 +16M\epsilon_0^2s^4
 +4.5\,10^{11}s^{14}D_\eta(z).                       \tag{22a}
\]

Consequently an energy already supplying `sum η L*J` needs only the
one-sided additional gradient term for this particular conversion. The
separate identity (18) provides an alternative with especially simple
outward collar work.

## 6. Negative gradients: exact favorable heat sign and full source bound

If `q_e<0`, then `L_e=0`, and the actual heat equations give

\[
 q_{e,t}|_{\rm heat}
 =\frac{L_{e-1}}{dm W_l}+\frac{L_{e+1}}{dm W_r}\ge0.
                                                               \tag{23}
\]

Thus `(F_-)'_heat<=0` face by face for arbitrary fixed nonnegative face
weights. At `q=0`, the derivative of `(q^-)^2` is zero. Also
`a'/a=-(4/3)b_comp<=0` on the compressing prefix.

Let `p=κ(x-2)` be the old stress and `f=p-p_d`, with spatially constant
reference `p_d`. Direct finite differences using the rectangular `(z,K,x)`
box and `κ>=8s^2`, `κ_z<=38s`, `p<=918s^2` give

\[
 |\Delta x|\le\frac1{8s^2}|\Delta p|
                  +\frac{546}s|\Delta z|,
\]
\[
 |\Delta Q|\le400|\Delta p|
                +1.7\,10^6s|\Delta z|
                +6.4\,10^5s^2|\Delta K|.              \tag{24}
\]

For example, `|Q_x|<=3000s^2`, `|Q_z|_(x,K)<=2800s`, and
`|Q_K|_(x,z)<=6.4*10^5s^2`; substituting the first inequality gives
the second. All mean-value paths for these last three derivatives stay
inside the displayed state box.

With `E_z=(λs^3/2)D_η(z)`, for any `δ>0`, (23)--(24) imply

\[
 \begin{split}
 F_-'\le{}&\frac2sF_-+\delta D_\eta(f)
 +\left(\frac{400^2}{2\delta}+1.28\,10^6\right)s^2F_-\\
 &+\frac{1.7\,10^6}{\sqrt\lambda}s^{1/2}(F_-+E_z).
 \end{split}                                                    \tag{25}
\]

This includes all heater, moving-geometry, and heat work. No positive
memory-gradient norm is needed to propagate `F_-`.

## 7. Consequence for the old-stress coupling, and exact remaining work

The full correction stress is

\[
 S=p+e,\qquad e=g p+2g\kappa+P,
 \qquad P=K\rho^2h.
\]

An exact product split has the form

\[
 \Delta e=\bar g\Delta p+B_z\Delta z+B_K\Delta K,
 \qquad |B_z|\le C_zs^4,\quad |B_K|\le C_Ks^2.
                                                               \tag{26}
\]

Indeed `Δ(gp)=gbar*Δp+pbar*Δg`, and
`Δ(2gκ)=2gbar*Δκ+2κbar*Δg`; the remaining pressure derivatives have
the asserted powers. The constants are finite on (3), by the input
constitutive bounds. Hence the interior old-stress work obeys

\[
 -\sum_ea_e\eta_e\Delta f\Delta(f+e)
 \le-\tfrac12D_\eta(f)+C_z's^8D_\eta(z)
                              +C_K's^4D_\eta(K).        \tag{27}
\]

The `gbar*(Delta f)^2` term is favorable. Combining (22) and (27), a
constant multiple of `E_K` absorbs the positive-gradient part of the last
term, while its negative-gradient part is `2C_K'*s^2 F_-`. The remaining
density term is `C*s^14 D_η(z)`, in addition to the `C*s^8 D_η(z)` already
in (27); these are lower-order multiples of `E_z`. Equation (25) propagates
the extra one-sided energy using an arbitrarily small share of old-stress
dissipation. The preexisting exact old-stress density propagation inequality
continues to apply.

This is a proved conditional closure of the particular interior mechanical
memory-gradient work. It bypasses the defects of (9), so no unproved
absorption of `U_k*Hbar` is used in this conclusion. It is outside the
positive, smooth, state-only coupled-metric class excluded in the input
`coupled_gradient.md`: the added gradient term is one-sided and vanishes on
the opposite open cone.

Still required for a full actual bootstrap are the singular relative
old-stress local-reaction cancellation and the complete stress collar work,
followed by a pointwise estimate reaching the central quarter, including
the origin and the last intersecting cell. A bound of the form
`E'<=C*E/s+C*s^4` cannot be integrated from `E(0)=0` without checking its
activation trace against that exponent. Neither this check nor the needed
pointwise implication follows merely from (22). The original all-`N` (UC)
and unconditional entropy-floor theorem therefore remain open here.

## Verification and provenance

All displayed assertions were checked by direct differentiation, exact
shared-flux summation, finite-edge product identities, and the actual
volume-centroid inequalities (20). No external theorem or trajectory
computation is load-bearing. The independent read-only subagent audit
`/root/boundary_transfer_bootstrap` reconstructed and passed (18)--(25)
from the actual law, including the geometry and all constants. It identified
only the need to state `2s<=z<=8s` explicitly in (3); that precision has
been added. The flux-potential identities (5)--(16), corollary (22a), and
integration with local reaction/collar estimates are analytically
self-reviewed only. No complete bootstrap audit or status upgrade follows.
Conservative mathematical proofreading covered this file only; no
mathematical-token changes were made during that proofreading pass.

SHA-256 paths are relative to `stable_stress_search/`:

| Input | SHA-256 |
| --- | --- |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/STATUS.md` | `abd9759d4896492d2744d2ce7a068a0ad6cbe5185f69d87298ca95dbf4b9cf2a` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/heat_absorption.md` | `b98843cec40271ef4a16bdb6c15baf50a43c203d6367fbf3ae72a4d299b74379` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/viscous_energy.md` | `874881bdaeb046fc607d500fc01d2402e8d4db1264c302e647ac137a39a920a1` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/coupled_gradient.md` | `f0c69a7b65cc8c3581e42d22d5ebbfa2b6cbf21b84a21f9a34e85e412e556492` |
