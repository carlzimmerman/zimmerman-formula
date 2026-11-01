# Relative entropy with a physical gradient threshold and nested collars

Base: **X48-NLC-2026-11-01-B**. Write scope: this new file only. All laws,
material scales, activation data, and meshes are unchanged; no integration or
new collapse grid is used. This note supplies exact relative-entropy and
one-sided-gradient estimates, and a conditional composition with the midpoint
density energy in `gradient_symmetrizer.md`. The pointwise implication (UC)
is not proved here.

## 1. Conditional domain and notation

Use the actual normalized law on an active prefix and all collars used below:

\[
 z_t=x,\quad x_t=L_rS+R,\quad K_t=Q+H,\qquad
 H_i=\frac{L_{i-1}-L_i}{dm W_i},\qquad dm=\frac{\pi}{3N}.
 \tag{1}
\]

Assume `2<x<=8`, `0<s<=T<=10^-3`. The prefix bounds are

\[
 2s\le z\le8s,\quad1\le\rho\le1.01,\quad
 3/2\le W\le1.51,\quad11s^2\le h\le200s^2,
 \quad0\le K\le1600s^3.                              \tag{2}
\]

Let `(z_d,x_d,K_d)` be the common spatially homogeneous reference, satisfying
`z_d'=x_d`, `x_d'=R_d`, `K_d'=Q_d`, and the same state bounds. Put

\[
 v=x-x_d,\quad\zeta=z-z_d,\quad k_i=K_i-K_d.
\]

For the sharp density-energy input and the collar iteration, impose the
tighter provisional envelope `|v|<=δ`, where `δ>0` can be chosen small,
through the entire relevant prefix and time interval. This is a bootstrap
hypothesis on the actual trajectory, not a conclusion.

For an internal face write

\[
 q=K_l-K_r,\quad \bar K=(K_l+K_r)/2,\quad
 A=(W_l^{3/2}+W_r^{3/2})/2,\quad B=W_l^{3/2}-W_r^{3/2},
\]
\[
 J=\psi_l-\psi_r=Aq+B\bar K,\quad
 C=\frac{D A_f}{d}h_lh_r,\quad a=\frac{A_f^2}{dm},\quad
 L=C\frac{\ell_gq}{d(c_g+\bar K)+\ell_gq}[J]_+
 \quad(q>0),                                           \tag{3}
\]

and `L=0` for `q<=0`. Here `d` is the actual centroid separation,
`A_f=4*pi*r_f^2`, `D=ell_g=1/10`, and `c_g=1/100`.
The pinned all-geometry estimates in `flux_potential.md` give

\[
 3s^4\le C/a\le16200s^4,\quad
 \sum_ea_ed_e^2\le16M,\quad
 |B|\le373s^2|\Delta z|,\qquad M=\pi/3.                \tag{4}
\]

Every cutoff below is fixed in material coordinates. Take `φ_i=χ_i^2`,
`0<=χ<=1`, and `η_e=barφ_e`; an outer cutoff equals one on the support
of every cell or face where `Δχ` is nonzero. Smooth fixed material
profiles satisfy `|Δχ|<=L_χ/N`. The actual geometry yields

\[
 \sum_ea_e(\Delta\chi)^2\bar u_e^2
 \le C_\chi\sum_iV_i\phi_{\rm out,i}u_i^2,\qquad
 \sum_ea_e(\Delta\chi)^2\le C_\chi,
                                                               \tag{5}
\]

with constants independent of `N`, including the first internal face.
For example the input bound
`a(Δχ)^2<=144*r_f^4*rho_l*L_χ^2*V_l` proves (5), with a fixed change
of constant for the right endpoint. The compressing prefix has radii
bounded by their activation values.

## 2. Exact relative entropy and its weighted source

Define

\[
 E_K=\frac12\sum_i dm W_i\phi_i k_i^2,\quad
 G=s^{-6}E_K,\quad D_H=\sum_e\eta_eL_eq_e.
                                                               \tag{6}
\]

The exact derivative, including reference, weight, and heat collar work, is

\[
 \begin{split}
 G'={}&-\frac6sG-s^{-6}D_H
       +s^{-6}\sum_e\Delta\phi\,L_e\bar k_e\\
 &+s^{-6}\sum_i dm\phi_i
   \{W_i k_i(Q_i-Q_d)+\tfrac12\rho_i h_i x_i k_i^2\}.
 \end{split}                                                    \tag{7}
\]

The collar now has no unconditional sign: `bar k` can be negative. It is
bounded below rather than discarded. Reference `K_d` is spatially constant,
which is why the interior dissipation remains exactly `L*q`.

The complete heater is

\[
 Q=h\{x(x/2-1)+\tfrac12g(K)x^2\},\qquad
 g=K/(K+1/100).
\]

Its state derivatives on the rectangular box (2) satisfy

\[
 |Q_x|\le3000s^2,\quad |Q_z|_{x,K}\le2800s,\quad
 |Q_K|_{x,z}\le6.4\,10^5s^2.
                                                               \tag{8}
\]

Hence the exact local relative source obeys

\[
 |Q-Q_d|\le3000s^2|v|+2800s|\zeta|
                              +6.4\,10^5s^2|k|.        \tag{9}
\]

Use the velocity and density local energies

\[
 E_v=\frac1{2s}\sum_iV_i\phi_i v_i^2,\qquad
 N_\lambda=\frac\lambda{2s^3}\sum_iV_i\phi_i\zeta_i^2,
 \qquad\lambda>0.
\]

Since `dm W=(rho W)V` with `rho W` uniformly bounded, Cauchy--Young in
(7) and (9) gives

\[
 \left|s^{-6}\sum_i dm W_i\phi_i k_i(Q_i-Q_d)\right|
 \le C_\lambda(s^{-1/2}+s^2)(G+E_v+N_\lambda).
                                                               \tag{10}
\]

In particular the mixed coefficient is `s^-1/2`, which is integrable at
activation. The `W_t` term in (7) is bounded by `C*s^2*G`. No positive
constant divided by `s` is introduced by these source estimates.

## 3. Exact heat comparison and relative-entropy collar

The actual outward flux satisfies the finite-edge comparison

\[
 \boxed{\quad L J\le4Lq+C_Bs^{14}a(\Delta z)^2,
 \qquad C_B=2.4\,10^{16}.\quad}                        \tag{11}
\]

To prove it, if `|B|*barK<=Aq`, then `J<=2Aq<4q`, so `LJ<=4Lq`.
In the other case a nonzero luminosity requires `B>0`, and `J<=2B*barK`.
Then `LJ=C*b*J^2<=4C B^2 barK^2`, and (2)--(4) give (11), since
`4*16200*373^2*1600^2<2.4*10^16`. Closed faces contribute zero.

Also

\[
 L^2/a\le16200s^4LJ.                                 \tag{12}
\]

Because `|Δφ|<=2*sqrt(η)*|Δχ|`, (12) gives for any `θ>0`

\[
 \left|\sum_e\Delta\phi\,L_e\bar k_e\right|
 \le\theta\sum_e\eta_eL_eJ_e
 +\frac{16200}{\theta}s^4
           \sum_ea_e(\Delta\chi)^2\bar k_e^2.
                                                               \tag{13}
\]

Both `K` and `K_d` lie in `[0,1600s^3]`, so `|k|<=1600s^3`.
By (5), the last term in (13) is `C_(χ,θ)*s^10`. Combining (11)--(13)
with `θ=1/8` yields

\[
 \left|\sum_e\Delta\phi\,L_e\bar k_e\right|
 \le\tfrac12D_H+\tfrac18C_Bs^{14}D_\eta(z)+C_\chi s^{10}.
                                                               \tag{14}
\]

Consequently the full weighted relative-entropy estimate is

\[
 \boxed{\quad
 G'+\frac6sG+\tfrac12s^{-6}D_H
 \le C_\lambda(s^{-1/2}+s^2)(G+E_v+N_\lambda)
       +\tfrac18C_Bs^8D_\eta(z)+C_\chi s^4.
 \quad}                                                        \tag{15}
\]

This proves the required collar powers without monotonicity of the relative
memory or an assumed memory-gradient norm.

## 4. Threshold `q/d=s^3` and the negative-gradient energy

Put `F_0=(1/2)sum a*η*(q^-)^2`, and

\[
 \beta_* =\frac{\ell_g}{c_g+(1600+\ell_g)T^3}>0.
\]

On `q/d>s^3` the actual gate is at least `β_*s^3`. The exact threshold
split proved in `flux_potential.md`, now with the time-dependent physical
threshold `ε_0(s)=s^3`, therefore gives

\[
 \boxed{\quad
 sD_\eta(K)\le2sF_0+\frac{10}{27\beta_*}s^{-6}D_H
                 +16Ms^7+4.5\,10^{11}s^{11}D_\eta(z).
 \quad}                                                        \tag{16}
\]

This is an instantaneous algebraic split; no derivative of the moving
threshold appears. Temperature-closed positive drops are in its
density-controlled class. Negative drops are exactly in `F_0`.

If `q<0`, then `L_e=0` and
`q_t|heat=L_(e-1)/(dm W_l)+L_(e+1)/(dm W_r)>=0`.
Thus `F_0'|heat<=0` face by face, with no collar exception. Geometry also
has favorable sign, since `a'/a=-(4/3)b_comp<=0`.
Using (8) on neighboring states, for every `ε>0`,

\[
 \begin{split}
 F_0'\le{}&\epsilon sD_\eta(v)
 +\left(\frac{4.5\,10^6}{\epsilon}s^3
                         +1.28\,10^6s^2\right)F_0\\
 &+2800s\sqrt{2F_0D_\eta(z)}.
 \end{split}                                                    \tag{17}
\]

If the midpoint density energy `E_g` satisfies `E_g>=c_g^E D_η(z)`
with `c_g^E>0` independent of `N`, the final term is at most
`C*s*(F_0+E_g)`. In particular (17) has no positive singular coefficient
`C/s`.

## 5. Complete velocity collar scaling

The full stress has the exact finite-edge split

\[
 \Delta S=\bar\nu\Delta v+C_z\Delta z+C_K\Delta K,
 \quad8s^2\le\bar\nu\le306s^2,\quad
 |C_z|\le600s,\quad |C_K|\le1.3\,10^5s^2.
                                                               \tag{18}
\]

Indeed
`ΔS=νbar*Δv+[xbar*(1+gbar)-2]*Δκ+xbar*κbar*Δg+ΔP`;
the input bounds on `κ_z,P_z,P_K,g'` prove the constants in (18).
The localized velocity energy has collar term

\[
 T_v=-s^{-1}\sum_ea_e\bar v_e\Delta\phi_e\Delta S_e.
\]

Let `D_v=sum a*η*νbar*(Δv)^2/s`. Using (5), (18), and
`E_g>=c_g^E D_η(z)`, independent Young parameters give

\[
 \boxed{\quad
 |T_v|\le\epsilon_1D_v+\frac{\epsilon_2}sE_g
          +\epsilon_3sD_\eta(K)
          +C_{\chi,\epsilon_1,\epsilon_2,\epsilon_3}s^2E_{v,\rm out}.
 \quad}                                                        \tag{19}
\]

For the density part this uses specifically
`sum a*sqrt(η)*|Δχ|*|vbar|*|Δz|
 <=ε_2 E_g/s+Cε_2*s*sum a*(Δχ)^2*vbar^2`.
The latter sum is `O(s*E_(v,out))`. The viscosity and memory parts of
(19) follow by choosing the gradient Young weights `νbar/s` and `s`,
respectively. Every additional singular density coefficient in (19) can
therefore be chosen arbitrarily small, at the price of a larger fixed
outer-collar constant. No collar term has been suppressed.

## 6. Conditional composition and the activation trace

For clarity, the remaining density/velocity input is stated exactly. Suppose
the midpoint potential calculation in `gradient_symmetrizer.md`, including
the local `R-R_d` work, gives for `E_b=E_v+E_g+N_λ`

\[
 E_b'+c_0sD_\eta(v)
 \le\frac p sE_b+C E_b+C_MsD_\eta(K)
                              +C_\chi s^2E_{v,\rm out},
                                                               \tag{20}
\]

where `c_0>0`, `E_g>=c_g^E D_η(z)`, all constants are independent of `N`,
and the tighter envelope plus collar Young choices permit `0<=p<1`.
Equation (20) is an explicit input to the composition in this note; its
proof must be checked in that note and is not inferred from positivity of
a frozen symbol.

Choose a fixed large multiplier `A_0` for (15), sufficient to absorb the
`s^-6 D_H` term in `C_M` times (16). Add (17), taking its gradient share
small. The residual `s*F_0`, `s^8 D(z)`, and `s^11 D(z)` are lower-order
multiples of `F_0+E_g`. For
`E=E_b+A_0G+F_0`, the resulting sufficient combined inequality is

\[
 E'+c_1sD_\eta(v)+c_2s^{-6}D_H
 \le\left\{\frac p s+C(s^{-1/2}+1)\right\}E
                      +C_\chi s^4+C_\chi s^2E_{v,\rm out}.
                                                               \tag{21}
\]

Here `c_1,c_2>0`. There is no unresolved heat mean defect in (21): (7)
and (17) are the full heat identities used to derive it.

The sufficient activation condition is

\[
 \lim_{s\downarrow0}s^{-p}E(s)=0\quad\text{for each fixed }N.
                                                               \tag{22}
\]

It is enough to prove `E=O_N(s)` and choose `p<1`; constants in this trace
need not be uniform in `N`. A conservative derivation from the actual
finite-dimensional law is as follows. For each fixed `N`, positive ordered
activation radii make all graph coefficients finite and the right-hand side
locally bounded. Thus `v=O_N(s)` and `ζ=O_N(s^2)`. The uniform heater maximum
bound gives `K=O(s^3)`. On this fixed graph, `b=O_N(s^3)` and
`J=O_N(s^3)`, hence `L=O_N(s^10)` and `H=O_N(s^10)`. By (9), integrating
`k_t=Q-Q_d+H` gives `k=O_N(s^4)`. Consequently

\[
 E_v=O_N(s),\quad N_\lambda=O_N(s),\quad
 G=O_N(s^2),\quad F_0=O_N(s^8),\quad E_g=O_N(s^4),
\]

where the last estimate uses the midpoint energy's local equivalence to
`D_η(z)=D_η(ζ)`. These prove (22) under the stated local existence and
coercivity conditions. This uses fixed-`N` regularity only to launch an
estimate whose constants are already uniform; it assumes no uniform
startup regularity theorem.

Multiplying (21) by its scalar integrating factor, applying (22) separately
for each `N`, and then integrating gives the following two-collar implication.
For the first cutoff, the amplitude envelope bounds
`E_(v,out)<=Cδ^2/s`; hence its forcing is `O(s)` and `E_outer<=C*s^2`
because `p<1<2`. For a nested inner cutoff whose collar lies where that
outer cutoff equals one, `E_(v,out)<=E_outer<=C*s^2`; its forcing is
`O(s^4)` and

\[
 E_{\rm inner}(s)\le C s^5.                            \tag{23}
\]

In particular `sum V φ_inner v^2<=C*s^6`. The constants depend on the
chosen fixed cutoffs and envelope, never on `N`. This is a conditional
first-energy conclusion; proving (20), closing the provisional envelope,
and converting (23) into actual central pointwise control are separate
obligations. No scalar smoothing theorem is substituted for that last
coupled nonlinear pointwise step.

## Verification and pinned inputs

Verification uses exact differentiation and finite-edge Cauchy--Young
estimates; no external theorem or numerical trajectory is load-bearing.
The scalar integration after (21) is conditional on its explicitly named
input (20). Conservative mathematical proofreading covers this file only.

SHA-256 paths are relative to `stable_stress_search/`:

| Input | SHA-256 |
| --- | --- |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/heat_absorption.md` | `b98843cec40271ef4a16bdb6c15baf50a43c203d6367fbf3ae72a4d299b74379` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/flux_potential.md` | `858dae640349b4efdf88cf4d9d98e524115fe9ed5505e56b88cf5961db559e78` |
