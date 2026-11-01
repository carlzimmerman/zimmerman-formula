# A relative midpoint gradient potential and a small startup exponent

Base: **X48-NLC-2026-11-01-B**. Write scope: this file only. The exact
material law, radial momentum equation, both heaters, and gated heat flux
are unchanged. No code, initial condition, earlier note, or numerical grid
was changed. The input hashes below pin the source independently of the
moving shared checkout.

**Result.** A convex midpoint gap in the old-viscosity primitive gives
an exact nonlinear cancellation between velocity and density-gradient
work. Its coefficient depends on density, time, and the homogeneous
reference, but not on x or K; its derivative contains neither `x_t` nor
`K_t`. For a tight provisional prefix bound `|x-x_d|<=1/32`, the
resulting weighted energy has positive singular coefficient at most
`1/(16s)`, plus an explicit `4e9*s*D(K)` cost and cutoff work of
size `C*s^2*E_velocity,outer`. Thus the large Fuchsian coefficient
from absolute local stress work is not the obstruction for this energy.

This is a conditional actual mechanical estimate. The exact memory cost
and all heat effects remain in the full equations. Their closure requires
the companion relative entropy estimate; no pointwise compression or
common bootstrap interval is proved here.

## 1. Geometry, reference, cutoffs, and energy

Use `z=log rho`, `x=-theta`, and the same homogeneous heated reference
as (L3) of [local_work.md](local_work.md). Set

\[
 v=x-x_d,\qquad e=z-z_d,\qquad c(s)=x_d(s)-2,
 \qquad \kappa(z)=\tfrac12\rho Wh,\qquad
 g={K\over K+1/100},\quad P=K\rho^2h.
                                                               \tag{G1}
\]

The exact equations on the active prefix are

\[
 x_t=\mathcal L_rS+R,\quad z_t=x,\quad K_t=Q+H,
 \qquad S=(1+g)\kappa x-2\kappa+P,\quad \nu=(1+g)\kappa.
                                                               \tag{G2}
\]

R is the entire gravitational, isotropic, and radial-shear reaction in
(L8), and Q is the sum of the two original heaters. In particular no
heat equation is changed or set to zero in this argument.

Let `I={1,...,J}` be a prefix. Assume, for its actual solution through
time `s<=10^(-3)`,

\[
 2<x_i\le8,\qquad |v_i|\le\delta\le1,
 \qquad \rho_i(0)=1,\ K_i(0)=0.                       \tag{G3}
\]

Then `|e_i|<=delta*s`, `2s<=z_i<=8s`, and all state-box bounds
(H8)--(H14) apply. Also `21/4<x_d<=8`, `0<c'<=35`, and
`13/4<c<=6`. Every average of two prefix densities in z coordinates
therefore satisfies

\[
 m=(z_l+z_r)/2\ge z_d-\delta s\ge17s/4.                \tag{G4}
\]

Take a nonincreasing fixed material cutoff `0<=chi<=1`, set
`phi=chi^2`, and put `eta_e=bar phi_e`. Every edge with `eta>0`
must have both endpoints in the bootstrap prefix. All sums are over
these actual cells or internal edges; no exterior active viscosity is
defined. Write

\[
 \mathscr D_v=\sum_ea_e\eta_e{\bar\nu_e\over s}
                                (\Delta_ev)^2,
 \qquad D_\eta(K)=\sum_ea_e\eta_e(\Delta_eK)^2,
 \quad a_e={(4\pi r_e^2)^2\over dm}.                  \tag{G5}
\]

The actual moving geometry gives
`V_t=-xV` and `a_e'/a_e=4u_e/r_e=-(4/3)<x>_e<=0`.
These identities retain the origin and actual cell volumes. The outer
half nodal mass is absent from internal prefix edges.

Let

\[
 F(z)={W(e^z)^2-9/4\over4},\qquad F_z=\kappa(z).
\]

This is the same exact primitive denoted F(rho) in the effective-flux
note, now composed with rho=e^z. For endpoint values put

\[
 d=z_r-z_l,\quad m=(z_l+z_r)/2,\qquad
 U(z_l,z_r)=2\{F(z_l)+F(z_r)-2F(m)\}.                 \tag{G6}
\]

Define the nonnegative energies

\[
 \begin{split}
 E_v&={1\over2s}\sum_iV_i\phi_i v_i^2,\\
 G&={c(s)\over s}\sum_ea_e\eta_eU(z_l,z_r),\\
 N&={\lambda\over2s^3}\sum_iV_i\phi_i e_i^2,
       \qquad \lambda=1/16,\qquad \mathcal T=E_v+G+N.
 \end{split}                                                   \tag{G7}
\]

U vanishes at the spatially constant reference and is a relative
gradient potential. Its density-only coefficient is essential: no
derivative of an x-dependent gradient metric is introduced.

## 2. Exact potential derivative and explicit nonlinear bounds

At fixed m and d, direct differentiation gives

\[
 U_d=\Delta\kappa,\qquad
 U_m=2\{\kappa_l+\kappa_r-2\kappa(m)\},\qquad
 U_t=\Delta\kappa\,\Delta v+U_m\bar x.                \tag{G8}
\]

In particular the coefficient of `Delta v` is exactly the finite
difference of the actual nonlinear kappa. A trapezoid approximation or
linearized stress is not needed.

Here are uniform bounds on `0<z_l,z_r<=.008`:

\[
 2m d^2\le U\le2.5m d^2,\qquad
 \left|{U_m\over U}-{1\over m}\right|\le20.            \tag{G9}
\]

The quotient is used when d is nonzero; all associated products extend
continuously to zero at d=0. To verify the constants, the exact ramp
implies `kappa(0)=kappa_z(0)=0`, `kappa_zz(0)=9/2`, and
`|kappa_zzz|<=40` on this interval. One direct bound uses

\[
 \kappa_{zzz}=\tfrac12\rho\{A+3A_z+3A_{zz}+A_{zzz}\},
 \qquad A=Wh,
\]

with `W<=1.51`, `h<=.0002`, `|h_z|<=.05`,
`|h_zz|<=7`, `|h_zzz|<=31`, `|W_z|<=.000202`,
`|W_zz|<=.051`, and `|W_zzz|<=7`; the resulting bound is below
39.8. Thus `kappa(z)=(9/4)z^2+r(z)`, with
`|r_z|<=20z^2` and `|r_zz|<=40z`.

For `h_0=|d|/2<=m`, the exact positive kernel formula is

\[
 U=2\int_{-h_0}^{h_0}(h_0-|t|)\kappa_z(m+t)\,dt.
\]

The corresponding formula for `U_m` has `kappa_zz` instead.
The kernel has integral `h_0^2` and mean `t^2=h_0^2/6`.
It follows that

\[
 |U-\tfrac94m d^2|\le\tfrac{35}3m^2d^2,\qquad
 |U_m-\tfrac94d^2|\le20m d^2.
\]

These imply (G9); for the quotient,
`|m U_m-U|<=32m^2d^2` and `m U>=2m^2d^2`, so even the
constant 16 would suffice. Consequently

\[
 G\ge{221\over8}D_\eta(z),\qquad
 \sum_ea_e\eta_e(\Delta\kappa)^2\le53s^2G,
 \quad
 { (\Delta\kappa)^2\over\bar\nu}
                  \le {361\over17}\,{U\over s}.       \tag{G10}
\]

The first uses (G4), `c>=13/4`, and the lower bound for U. The
others use `|kappa_z|<=38s`, `bar nu>=8s^2`, and
`U>=8.5s*d^2`. All are estimates on exact finite differences.

## 3. Cancellation of the leading singular growth

The derivative of the gradient energy is exactly

\[
 \begin{split}
 G'={}&{c\over s}\sum_ea_e\eta_e\Delta\kappa\Delta v\\
 &+\sum_ea_e\eta_e{c\over s}U
       \left({c'\over c}-{1\over s}+\bar x{U_m\over U}\right)
 +{c\over s}\sum_ea_e'\eta_eU .
 \end{split}                                                   \tag{G11}
\]

The last term is nonpositive. To bound the middle term, use the exact
reference identity
`s*x_d(s)-z_d(s)=integral_0^s[x_d(s)-x_d(t)]dt<=35s^2/2`.
Then (G3)--(G4) give

\[
 {\bar x\over m}-{1\over s}
 ={s\bar x-m\over sm}
 \le {8\delta\over17s}+{70\over17}.
\]

Together with (G9), `bar x<=8`, and `c'/c<=140/13`, this proves

\[
 G'\le{c\over s}\sum_ea_e\eta_e\Delta\kappa\Delta v
                  +\left({\delta\over2s}+175\right)G.
                                                               \tag{G12}
\]

Thus the nonlinear potential has no uncancelled leading `G/s` term.
Its singular growth is proportional to the stated relative amplitude
delta. This deduction uses that density error is the time integral of
velocity error; an unrelated amplitude box would not give it.

## 4. Full interior stress work and local reaction

The velocity energy has exact derivative

\[
 E_v'=-{1\over s}\sum_ea_e\Delta(\phi v)\Delta S
       -{E_v\over s}-{1\over2s}\sum_iV_i\phi_i x_iv_i^2
       +{1\over s}\sum_iV_i\phi_i v_i(R_i-R_d).
                                                               \tag{G13}
\]

The spatially constant reference stress is subtracted inside the
cutoff support. No assertion about a ghost reference stress at the
vacuum boundary is used.

An exact endpoint product identity gives

\[
 \Delta S=\bar\nu\Delta v+c\Delta\kappa
       +(\bar v+\bar x\bar g)\Delta\kappa
       +\bar x\bar\kappa\Delta g+\Delta P.            \tag{G14}
\]

The term `-c*sum a eta Delta kappa Delta v/s` in (G13) cancels
the first term of (G11) exactly. The remaining products can all be
estimated without differentiating x or K in time. In detail, allocating
`mathscr D_v/8` to each product gives

\[
 \begin{split}
 {1\over s}\sum a\eta|\bar v\Delta\kappa\Delta v|
       &\le\tfrac18\mathscr D_v+{14\delta^2\over s}G,\\
 {1\over s}\sum a\eta|\bar x\bar g\Delta\kappa\Delta v|
       &\le\tfrac18\mathscr D_v+2.3\,10^{13}s^5G,\\
 {1\over s}\sum a\eta\,82000s^4|\Delta z\Delta v|
       &\le\tfrac18\mathscr D_v+6.1\,10^7s^5G,\\
 {1\over s}\sum a\eta\,122605s^2|\Delta K\Delta v|
       &\le\tfrac18\mathscr D_v+3.8\,10^9sD_\eta(K).
 \end{split}                                                   \tag{G15}
\]

Here `g<=160000s^3`, `|Delta g|<=100|Delta K|`, and the last two
lines together bound the pressure and memory remainder, because
`|P_z|<=82000s^4`, `|P_K|<=205s^2`, and
`|bar x*bar kappa|<=1224s^2`. The first line follows from (G10):
its coefficient before rounding is `722/(17c)<14`. The second is
the same estimate with `delta` replaced by `1.28e6*s^3`.
All mean-value paths remain in the original state box.

For local reaction, retain the exact shear in (L15). The decreasing
cutoff Hardy estimate (L16), `|v|<=delta<=1`, and
`|rho-rho_d|<=1.01|e|` give

\[
 \left|{1\over s}\sum V\phi v(R-R_d)\right|
       \le50E_v+13s^2N/\lambda.                       \tag{G16}
\]

Indeed gravity costs at most `13(E_v+s^2N/lambda)`; the isotropic
kinetic reaction costs at most `11E_v`; shear costs at most
`22delta E_v`. No artificial reference forcing survives. Also

\[
 N'\le{\lambda\over s}E_v-{2\over s}N.               \tag{G17}
\]

For (G17), differentiate the actual volumes and use
`lambda*|e*v|/s^3<=lambda*v^2/(2s^2)
+lambda*e^2/(2s^4)`. Its negative volume term is simply dropped.
Thus the strong density weight causes a small positive velocity loss
which is absorbed by the negative `-E_v/s` already present in (G13).

## 5. Exact collar work and its weighted bound

The collar term left by (G13) is exactly

\[
 B_\chi=-{1\over s}\sum_ea_e\Delta\phi\,\bar v\Delta S.
                                                               \tag{G18}
\]

Let `chi_1` be a larger nonincreasing material cutoff, equal to one
at every endpoint where `Delta chi` is nonzero, and supported with its
edge halo in the same bootstrap prefix. Write `E_(v,1)` for its
velocity energy. If chi has material Lipschitz constant L, the actual
geometry estimate (H26) gives

\[
 K_\chi(v)=\sum_ea_e(\Delta\chi)^2\overline{v^2}
                 \le292L^2sE_{v,1}.                  \tag{G19}
\]

Use `|Delta phi|<=2 sqrt(eta)|Delta chi|`. The full finite stress
bound from (G14) can be simplified on this interval to

\[
 |\Delta S|\le\bar\nu|\Delta v|+8|\Delta\kappa|
                                      +123000s^2|\Delta K|.
\]

For the pressure-density part use `kappa_z>=4z>=8s`, a consequence
of the same Taylor bound used in (G9), to obtain
`82000s^4|Delta z|<=10250s^3|Delta kappa|`.
The complete coefficient of `|Delta kappa|` is then below eight.
The three collar pieces consequently satisfy

\[
 \begin{split}
 |B_{\chi,v}|&\le\tfrac1{16}\mathscr D_v
                         +1.43\,10^6L^2s^2E_{v,1},\\
 |B_{\chi,z}|&\le{G\over32s}
                         +3.2\,10^7L^2s^2E_{v,1},\\
 |B_{\chi,K}|&\le sD_\eta(K)
                         +4.5\,10^{12}L^2s^2E_{v,1}.
 \end{split}                                                   \tag{G20}
\]

For the second line first use (G10) to get
`|B_(chi,z)|<=16 sqrt(53)*sqrt(G)*sqrt(K_chi(v))`, then
Young with coefficient `1/(32s)` for G and (G19). The unrounded
outer coefficient is `990464*32`. The third line uses Young with
coefficient s for the memory-gradient square. These prove the convenient
combined bound

\[
 |B_\chi|\le\tfrac1{16}\mathscr D_v+{G\over32s}
                +sD_\eta(K)+5\,10^{12}L^2s^2E_{v,1}.
                                                               \tag{G21}
\]

No homogeneous collar is assumed. There is no extra collar term in
G', since it is an edge potential with a fixed material edge weight;
its exact time derivative is already (G11). The physical stress boundary
and heat boundary are retained outside the cutoff support.

## 6. Conditional first mechanical inequality with explicit exponent

Combine (G12)--(G17) and (G21), take `delta<=1/32`, and retain the
nonpositive moving-geometry terms. Since

\[
 \delta/2+14\delta^2\le15/512<1/32,
\]

the singular positive contribution of G is less than `G/(16s)`
including the collar. The regular gradient coefficient
`175+(2.3e13+6.1e7)*s^5` is below 176 for `s<=10^(-3)`.
With `lambda=1/16`, the following actual conditional inequality follows:

\[
 \boxed{\quad
 \begin{split}
 \mathcal T'\le{}&-\tfrac7{16}\mathscr D_v
             -{15\over16s}E_v-{2\over s}N+{1\over16s}G
             +250\mathcal T\\
          &+4\,10^9sD_\eta(K)
             +5\,10^{12}L^2s^2E_{v,1}.
 \end{split}\quad}                                    \tag{G22}
\]

In particular its first positive singular exponent is at most `1/16`,
not the large coefficient of an absolute stress-source estimate. This
is an exact nonlinear gradient symmetrizer outside the local-metric
no-go class of (L31)--(L37): it contains a mechanical density gradient.
Its remaining `s*D(K)` is explicitly displayed, rather than presumed
controlled by heat on closed faces.

## 7. Activation trace and what collar iteration would imply

For each fixed finite N the exact solution has a local interval after
activation with all x near C_a, valid geometry, and K nonnegative.
On that interval `rho-1=O_N(s)` and `K=O_N(s^3)` by the original
heater equation and its finite-dimensional heat operator. Hence
`S=O_N(s^2)` and the finite-N coefficients of L remain bounded.
The reference-subtracted reaction is locally Lipschitz in density and
velocity errors, including its quadratic prefix shear. The equation for
v therefore gives, by its integral form and an ordinary finite-N
Gronwall estimate,

\[
 v=O_N(s^3),\qquad e=O_N(s^4),\qquad
 \mathcal T=O_N(s^5).                                 \tag{G23}
\]

Here the global finite-N interval is used only for the activation trace,
not as a common bootstrap interval. The finite-N constants in (G23)
need not be uniform: for any fixed exponent `a<5`,
`tau^(-a)*T(tau)->0` separately for every N. Applying an integrating
factor from tau and then sending tau to zero therefore introduces no
unknown uniform initial constant. Even the weaker trace `O_N(s)`
from continuity of the finite-N right-hand side would suffice for the
exponent `1/16` in (G22).

The memory cost prevents integrating (G22) by itself. A precise
composition is now available from
[relative_entropy.md](relative_entropy.md), equations (15)--(22).
Equation (G22) proves its named mechanical input (20), with
`p=1/16`, `c_0=7/2`, `C_M=4e9`, and
`c_g^E=221/8`. In its notation let
`G_K=s^(-6)*(1/2)*sum dm*W*phi*(K-K_d)^2` and
`F_0=(1/2)*sum a*eta*((K_l-K_r)^-)^2`.
The exact gated-heat threshold estimate there bounds `s*D(K)` by
`2s*F_0+(10/(27beta_*))*s^(-6)*D_H+16M*s^7
+4.5e11*s^11*D(z)`, with fixed `beta_*>0`.
Choose a fixed multiplier
`A_0>4*(4e9)*10/(27beta_*)` for its relative-entropy inequality;
its heat dissipation then absorbs this memory cost with a positive
share left. Its negative-gradient estimate has an arbitrarily small
share of `s*D(v)` and otherwise only integrable coefficients. Thus
for
`Y=mathcal T+A_0*G_K+F_0`, the two independently derived identities
give constants `c_1,c_2,C>0`, independent of N, such that

\[
 Y'+c_1sD_\eta(v)+c_2s^{-6}D_H
 \le\left\{{1\over16s}+C(s^{-1/2}+1)\right\}Y
                  +C_Ls^2E_{v,1}+C_Ls^4.             \tag{G24}
\]

This is a conditional all-N first-energy theorem: take
`delta_0=1/32`, `T_0=10^(-3)`, and require (G3) on all the prefix
cells and collars used. The entropy note proves the exact heat collar
and local terms of (G24), without assuming positive diffusion on every
face. Its fixed-N activation argument gives `Y=O_N(s)`, hence the
required trace `s^(-1/16)*Y(s)->0`. All heat terms are retained in
this composition; no separate bound on `H`, `K_t`, or its gradient is
assumed. The primary conclusion remains conditional on the tight
prefix envelope, rather than on a linearized reference solution.

The collar propagation is now precise. On an outer cutoff the coarse
amplitude bound gives `E_(v,1)<=M*delta^2/(2s)`. The first forcing
in (G24) is O(s), and integration yields Y=O(s^2), uniformly in N.
For an inner cutoff whose larger cutoff is this first one, the forcing
is O(s^4), giving Y=O(s^5), uniformly in N. Constants depend on the
fixed cutoff widths and on the integrable coefficient, not on N.

One explicit ceiling-correct hierarchy, for `N>=32` and the assumed
prefix `I={1,...,ceil(N/2)}`, uses
`theta_i=(i-1/2)/N`. Choose chi_0 equal to one through `9/32`,
linear to zero at `10/32`; chi_1 equal to one through `11/32`,
linear to zero at `12/32`; and chi_2 equal to one through `13/32`,
linear to zero at `14/32`. Each has L=32. Every endpoint where
`Delta chi_0` is nonzero lies where chi_1 is one, and every such
endpoint for chi_1 lies where chi_2 is one, since `1/N<=1/32`.
All active-edge halos lie in I. Also chi_0 is one at every
`i<=ceil(N/4)`, because `theta_i<=1/4+1/(2N)<9/32`.
Use only the coarse velocity amplitude on chi_2, obtain Y=O(s^2)
on chi_1, then Y=O(s^5) on chi_0.

For completeness, integrating `Y'<= (a/s+b)Y+C*s^p` with the
displayed trace gives
`Y(s)<=C*exp(integral_0^s|b|)*s^(p+1)/(p+1-a)` whenever
`p+1>a`. This is the implication just used with `a=1/16`.
The full heat part and its activation trace are proved in the pinned
companion, rather than rederived here.

The conclusion is still not the common-time pointwise assertion. The
tight amplitude hypothesis must cover the entire prefix I and all
collars throughout the interval. Improving an energy, or eventually a
pointwise norm, on chi_0 does not improve that hypothesis at the outer
edge of I. A bootstrap argument needs an additional coverage or
domain-of-validity argument, for example a global weighted estimate or
a separately proved exterior bound. The shrinking interior estimate
cannot itself supply that missing premise. Actual nonlinear pointwise
smoothing and this bootstrap-coverage obligation remain open.

## 8. Scope, checks, and provenance

This argument independently derives the exact midpoint potential and
its weighted mechanical identity; coordination with the flux/entropy
route identified the common cutoff and memory-gradient terms. No
agreement between routes is treated as proof. Self-review covers the
positive kernel, the reference scaling cancellation, all four interior
Young estimates, moving volumes and graph, the support halo, and the
activation trace. Primary verdict: **conditional on (G3), with
delta<=1/32** for (G22), and the same conditional verdict for (G24)
after the explicitly pinned companion composition. The tight amplitude
bootstrap itself, coverage of its outer collar, and pointwise recovery
remain open. Independent review is separate.

Focused mathematical proofreading covered this new file. Exact rational
checks passed for the third-derivative bound, convex-gap kernel constants,
all interior and collar Young roundings, and the singular exponent.
The 24 equation tags are unique, braces and display delimiters balance,
and scoped whitespace validation passed. These checks contain no
physical trajectory integration or numerical mesh experiment.

The material identity `F_z=kappa` and the radial compression equation
are read from the exact source and effective-flux/startup notes. The
Hardy and geometric cutoff bounds used in (G16) and (G19) are proved
in [local_work.md](local_work.md), equations (L14)--(L16), and
the heat note (H26), respectively. No external theorem, trajectory
experiment, continuum approximation, or mesh extrapolation is a proof
leaf.

Input SHA-256 hashes, relative to `stable_stress_search`:

| Input | SHA-256 |
| --- | --- |
| collapse.py | 14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf |
| material.py | 4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390 |
| entropy_transport/transport.py | 2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c |
| entropy_transport/convective_transport.py | ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97 |
| entropy_transport/floor_theorem/density_closure_2026_11_01/local_work.md | 513035e97cabeebda25db702bad64969ba9e0fac3ddc87fd1b0e367edb925a5f |
| entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/heat_absorption.md | b98843cec40271ef4a16bdb6c15baf50a43c203d6367fbf3ae72a4d299b74379 |
| entropy_transport/floor_theorem/density_closure_2026_11_01/relative_entropy.md | 92fb61a920ef28e4e08324dbbcf3495cbf708dcc5f750de866fb1b407a8f56b6 |
