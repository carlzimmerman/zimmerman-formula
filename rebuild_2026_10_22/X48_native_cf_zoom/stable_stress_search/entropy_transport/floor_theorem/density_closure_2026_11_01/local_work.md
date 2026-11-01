# Reference cancellation, radial shear, and uniform collar work

Base checkpoint: **X48-NLC-2026-11-01-B**, continuing the unchanged
X48-UC-2026-11-01-B source. Observed shared HEAD:
`6874d71f1f0eeb57ade18956f8d71c583cb8e1c1`. The source hashes at the
end pin the inputs independently of concurrent changes. This route owns
this file only. No law, code, parameter, initial condition, or numerical
record was changed; no new grids were run.

**Result.** The local work (H35) of
[heat_absorption.md](../nonlinear_closure_2026_11_01/heat_absorption.md)
has the genuine reference-subtracted estimate

\[
 |\mathcal R_\phi(s)|\le {2\,10^7\over s}
                   \{E_\phi(s)+Z_\phi(s)\},\qquad
 Z_\phi={1\over2}\sum_iV_i\phi_i(z_i-z_d)^2.             \tag{L1}
\]

It holds under that note's provisional prefix envelope, for nonincreasing
material cutoffs and the exact heated homogeneous reference defined below.
All constants are independent of N. In particular, there is no reference
forcing of size `rho*R` left in this estimate. The radial shear is retained
as the square of a difference from an inner volume average, and is bounded
without a compression-gradient assumption. The new density energy satisfies
an explicit estimate of the same `1/s` type.

The cutoff work also admits both a nested-energy bound and a coarse actual
`O(s^4)` bound on its collar, using only the prefix envelope. These facts
remove the local-reaction and mesh dependence of collar work as unspecified
terms. They do **not** prove propagation of the prefix envelope, eliminate
the `s^6 D(z)` term in (H37), or launch a singular Gronwall argument at
activation. The common-time central-quarter assertion remains open.

## 1. Exact hypotheses and reference

Use the exact geometry, active constitutive law, and notation (H1)--(H5).
In particular `dm=M/N`, `M=pi/3`, `V_i=dm/rho_i`, `z=log rho`, and

\[
 S=\nu x-2\kappa+P,\quad
 \kappa=\tfrac12\rho Wh,\quad \nu=\kappa(1+g),\quad
 P=K\rho^2h,\quad g={K\over K+1/100},\quad \psi=KW^{3/2}.
                                                               \tag{L2}
\]

On a prefix `I={1,...,J}` assume the actual solution has
`2<x_i(v)<=8` for `0<v<=s<=10^(-3)`, common activation density one,
and initial K zero. This is the same provisional amplitude hypothesis as
(H1). Define the reference by the ordinary differential equations

\[
 z_d'=x_d,\qquad
 x_d'=R_d=4\pi e^{z_d}+x_d^2/3,\qquad
 K_d'=Q(z_d,x_d,K_d),\qquad
 Q=h\{\tfrac12(1+g)x^2-x\},                             \tag{L3}
\]

with `z_d(0)=K_d(0)=0` and the unchanged activation compression
`x_d(0)=C_a`. Set `S_d=S(z_d,x_d,K_d)` and
`psi_d=psi(z_d,K_d)`. Both original heaters are present in Q. This is a
homogeneous local reference with zero heat flux; it is not asserted to
solve the actual vacuum-boundary problem.

The bounds `21/4<C_a<6`, `x_d<=8` on `s<=10^(-3)`, and
`rho_d<=exp(8s)` follow from the reference argument in
[startup_energy_route.md](../startup_energy_route.md), section 2. The
same scalar heater inequality used in (H10)--(H11) gives
`K_d<=1600s^3`. Hence the reference and the whole line segment joining
it to any prefix state lie in the rectangular box

\[
 2\le x\le8,\qquad e^{2s}\le\rho\le e^{8s}\le1.01,
 \qquad 0\le K\le1600s^3.                              \tag{L4}
\]

All bounds (H8)--(H14) apply to both endpoints. In particular
`|f|<=2500s^2`, `|q|<=3000s^3`, where
`f=S-S_d`, `q=psi-psi_d`. Write `e=z-z_d`, `v=x-x_d`, and
`k=K-K_d`. Let `phi_i=chi_i^2`, with `0<=chi<=1` nonincreasing in
the material index. Every edge with `bar phi>0` must have both endpoints
in I; in particular the cutoff vanishes before the unbootstrapped region.
Use exactly the energy (H34),

\[
 E_\phi=E_{S,\phi}+E_{q,\phi}
 ={1\over2}\sum_i{V_i\phi_i f_i^2\over\nu_i}
  +{1\over2}\sum_i{dm\,\phi_iq_i^2\over\sqrt{W_i}}.
                                                               \tag{L5}
\]

## 2. Finite constitutive inverse at a cell

The subtraction argument (H18)--(H21) applies equally to the actual and
reference states at one cell: its proof only uses state values and a
mean-value path in (L4). Therefore

\[
 \begin{split}
 |v|&\le\tfrac18s^{-2}|f|+86s^{-1}|e|+15326|k|,\\
 |k|&\le .55|q|+326000s^5|e|,\\
 |v|&\le\tfrac18s^{-2}|f|+87s^{-1}|e|+8500|q|.
 \end{split}                                                   \tag{L6}
\]

For the last inequality, the additional coefficient of `s^(-1)|e|`
is at most `15326*326000*s^6<5e-9` on this time interval. No spatial
gradient estimate, interpolated constitutive branch, or inversion of a
linearized reference law is being used.

The energy weights imply the useful elementary comparisons

\[
 \sum V\phi f^2\le612s^2E_{S,\phi},\qquad
 \sum V\phi q^2\le2.5E_{q,\phi},\qquad
 {dm\over\sqrt W}\le V.                                \tag{L7}
\]

They use `8s^2<=nu<=306s^2`, `1.5<=W<=1.51`, and
`1<=rho<=1.01`. The second inequality follows from
`rho/sqrt(W)>.8`.

## 3. Reference-subtracted reaction terms

Separate the gravitational and isotropic kinetic reaction from shear:

\[
 R_i=R_0(z_i,x_i)+T_i,\quad
 R_0=4\pi e^z+x^2/3,\quad
 T_i={6r_ir_{i-1}(r_iu_{i-1}-r_{i-1}u_i)^2
                  \over(r_i^3-r_{i-1}^3)^2}.           \tag{L8}
\]

Put `Psi(z,K)=K W^(3/2)` and define local state functions

\[
 A=\nu R_0+S_zx+S_KQ,\qquad
 B=\Psi_zx+\Psi_KQ.                                   \tag{L9}
\]

The reference ODE gives the exact identities `S_d'=A_d` and
`psi_d'=B_d`. Consequently the (H34) source terms are exactly

\[
 \mathcal F_i=A_i-A_d+\nu_iT_i,\qquad
 \mathcal G_i=B_i-B_d.                                 \tag{L10}
\]

The leading reference reaction is thus subtracted before taking any
absolute value. Replacing `F` by a bound on `nu*R+S_z*x+S_K*Q`
would lose this cancellation.

Here are explicit derivative bounds on the whole box (L4):

| State function | x derivative | z derivative | K derivative |
| --- | ---: | ---: | ---: |
| A | `1300s` | `900` | `250000s` |
| B | `6100s^2` | `2600s` | `1.3e6 s^2` |

All entries bound absolute values. To make the second-derivative input
auditable, the exact polynomial ramp and `W'=h` give

\[
 \begin{gathered}
 |h_z|\le50s,\quad |h_{zz}|\le7,\quad
 |W_z|\le202s^2,\quad |W_{zz}|\le51s,\\
 |\kappa_{zz}|\le6,\quad |\nu_{zz}|\le12,\quad
 |\nu_{zK}|\le3800s,\quad |\nu_{KK}|\le3.06\,10^6s^2,\\
 |P_{zz}|\le12000s^3,\quad |P_{zK}|\le52s,\\
 |S_z|\le610s,\quad |S_{zz}|\le110,\quad
 |S_K|\le123000s^2,\quad |S_{zK}|\le30500s,
 \quad |S_{KK}|\le2.5\,10^7s^2,\\
 |Q|\le5000s^2,\quad |Q_x|\le3000s^2,\quad
 |Q_z|\le1250s,\quad |Q_K|\le640000s^2.                \tag{L11}
 \end{gathered}
\]

For example `h_zz=rho*h'+rho^2*h''`, with `h''<=6` on
this ramp. Also

\[
 \kappa_{zz}=\tfrac12\rho\{
 (W+2W_z+W_{zz})h+2(W+W_z)h_z+Wh_{zz}\}.
                                                               \tag{L12}
\]

Substitution proves the displayed bound six. The small K box gives
`g<=100K<=.00016`, so
`Q/h<=24+3200K<25`. This sharper bound, with `h_z<=50s`,
gives `Q_z<=1250s`. To obtain the A row, differentiate (L9), using
`R_0<=35`, `R_(0,x)<=6`, and `R_(0,z)<=13`. For example

\[
 |A_x|\le1836s^2+1218s+4.455\,10^8s^4<1300s,
\]

and
`|A_z|<=880+2660s+3978s^2+3.0625e8s^3<900`.
For the B row use
`Psi_K<2`, `|(Psi_K)_z|<=373s^2`,
`|Psi_z|<=6e5s^5`, and `|Psi_zz|<=151000s^4`.
These are direct state derivatives; there is no heat divergence or
derivative of the entropy gate in them.

Apply the mean-value theorem in (L4), then the first two inequalities
of (L6). Rounding upwards gives

\[
 \begin{split}
 |A-A_d|&\le200s^{-1}|f|+120000|e|+1.2\,10^7s|q|,\\
 |B-B_d|&\le800|f|+530000s|e|+5.3\,10^7s^2|q|.
 \end{split}                                                   \tag{L13}
\]

For audit, before the final rounding the three coefficients in the
first line are at most `162.5`, `112700+6.58e12s^6`, and
`11095590`. In the second line they are `762.5`,
`527200+3.10e13s^6`, and `52133730`, respectively. The factors
`s^(-1)`, one, and s in the first line are essential.

## 4. Shear is an inner volume-average difference

Continuity and `r_0=u_0=0` give

\[
 u_i=-{\sum_{j\le i}V_jx_j\over4\pi r_i^2}
     =-{r_i\over3}\langle x\rangle_i,\qquad
 \langle x\rangle_i={\sum_{j\le i}V_jx_j\over\sum_{j\le i}V_j}.
                                                               \tag{L14}
\]

For `i>=2`, substitution in (L8) and
`r_i^3-r_(i-1)^3=3V_i/(4pi)` give exactly

\[
 T_i={2\over3}{r_{i-1}^3\over r_i^3}
          (v_i-\langle v\rangle_{i-1})^2,
 \qquad T_1=0.                                         \tag{L15}
\]

The spatially constant reference disappears from the difference even
though these are actual volume averages. No geometry is replaced by the
homogeneous reference geometry.

Here is an elementary finite Hardy bound adequate for this term:

\[
 \sum_{i=2}^JV_i\phi_i\langle v\rangle_{i-1}^2
          \le7\sum_{i=1}^JV_i\phi_i v_i^2,
 \qquad
 \sum_iV_i\phi_iT_i\le11\sum_iV_i\phi_i v_i^2.          \tag{L16}
\]

To prove the first, `dm/1.01<=V_j<=dm` implies
`|<v>_n|<=1.01*n^(-1)*sum_(j<=n)|v_j|`.
Cauchy--Schwarz with factors `j^(-1/4)` and `j^(1/4)|v_j|`
gives

\[
 \left({1\over n}\sum_{j\le n}|v_j|\right)^2
 \le2n^{-3/2}\sum_{j\le n}j^{1/2}v_j^2.
\]

Since phi is nonincreasing, `phi_(n+1)<=phi_j` for `j<=n`, and
`sum_(n>=j)n^(-3/2)<=3j^(-1/2)`. Sum the preceding bound to
obtain constant `6*1.01^3<7` after the volume comparisons. Then
`(v_i-<v>_(i-1))^2<=2v_i^2+2<v>_(i-1)^2` in (L15) gives
`(4/3)*(1+7)<11`. This proof includes the first cell and uses no
unstated bound on adjacent cell widths.

## 5. Local work and the zeroth-order density energy

By (L10), the work (H35) splits into A work, B work, and
`sum V_i phi_i f_i T_i`. The first line of (L13), Young's inequality,
and (L7) give

\[
 \left|\sum{V\phi f\over\nu}(A-A_d)\right|
 \le {12120400\over s}E_{S,\phi}
       +{7500\over s}\sum V\phi e^2
       +1.875\,10^6sE_{q,\phi}.                        \tag{L17}
\]

For example split its density product as
`120000*|f*e|/nu <=60000*f^2/(s*nu)+60000*s*e^2/nu`.
The latter coefficient is `7500/s` after `nu>=8s^2`.
The same splitting of the q product yields the stated q term.
Similarly the second line of (L13) gives

\[
 \left|\sum{dm\,\phi q\over\sqrt W}(B-B_d)\right|
 \le {800\over s}E_{S,\phi}
 +(306000s^3+662500s+1.06\,10^8s^2)E_{q,\phi}
 +265000s\sum V\phi e^2.                               \tag{L18}
\]

For shear, use `|f|<=2500s^2`, (L16), (L6), and (L7):

\[
 \begin{split}
 \left|\sum V\phi fT\right|
 &\le27500s^2\sum V\phi v^2\\
 &\le790000E_{S,\phi}
       +6.25\,10^8\sum V\phi e^2
       +1.5\,10^{13}s^2E_{q,\phi}.                    \tag{L19}
 \end{split}
\]

The unrounded density coefficient is `27500*3*87^2=624442500`.
Since `sum V phi e^2=2Z_phi`, (L17)--(L19) imply (L1) on
`s<=10^(-3)`. In particular, the largest stress coefficient after
factoring `1/s` is below `1.213e7`; the density coefficient is below
`1.266e6`, and the temperature coefficient is below `16000`.

The additional density energy requires no heat estimate. Since
`e_t=v` and `V_t=-xV`,

\[
 Z_\phi'=\sum V\phi ev-\tfrac12\sum V\phi xe^2
 \le\sum V\phi |ev|
 \le {39\over s}E_{S,\phi}
      +{8675\over s}Z_\phi+10625sE_{q,\phi}
 \le{9000\over s}(E_\phi+Z_\phi).                     \tag{L20}
\]

For the f product in (L6) use
`|e*f|/(8s^2)<=f^2/(16s^3)+e^2/(16s)`; for the q
product use `8500|e*q|<=4250(e^2/s+s*q^2)`.
This proves (L20), including the actual moving cell volumes.

## 6. Collar work is uniform without global homogeneity

Let chi_0 be a material cutoff with Lipschitz constant L, and let
`phi_1=chi_1^2` be another nonincreasing cutoff, supported in the
same bootstrap prefix and equal to one at every endpoint of an edge
where `Delta chi_0` is nonzero. Denote `phi_0=chi_0^2`.
The proof of (H26) localizes to these endpoints, so

\[
 K_{\chi_0}(u)\le146L^2\sum V\phi_1u^2.
\]

Combining this with (L7), for `s<=10^(-3)`, yields

\[
 \boxed{\quad
 9K_{\chi_0}(f)+5.2\,10^5s^4K_{\chi_0}(q)
 \le9\,10^5L^2s^2E_{\phi_1}.
 \quad}                                                \tag{L21}
\]

Here the stress coefficient before rounding is
`9*146*612=804168`; the heat coefficient is `1.898e8*s^4`,
which is at most `190*s^2`. The larger constant in (L21) is
intentional. The estimate transfers work only to a larger cutoff on
the same actual solution. It assumes no homogeneous collar.

There is also a coarse actual collar bound already implied by the
bootstrap. Since `|e|<=6s`, `sum_I V<=M`, and `sum_I dm<=M`,

\[
 E_{\phi_1}+Z_{\phi_1}
 \le M(390625s^2+18s^2+3.7\,10^6s^6)
 <4.3\,10^5s^2.                                       \tag{L22}
\]

Consequently the work in (L21) is at most
`3.9e11*L^2*s^4`, uniformly in N. For the explicit cutoff in
section 5 of the heat note, one may instead use all prefix cells in
(H26) directly, with `L=32/3`; no larger cutoff or exterior amplitude
bound is needed for this coarse estimate. The sharper nested estimate
(L21) is available whenever there is room for its support halo.

Combining (H37), (L1), and (L20), on the conditional heat absorption
time `s<=10^(-6)`, gives the actual inequality

\[
 \begin{split}
 (E_{\phi_0}+Z_{\phi_0})'
 \le{}&-\tfrac18D_{\bar\phi_0}(f)
        -\tfrac1{16}H_{\bar\phi_0}(q)
        +4.2\,10^{21}s^6D_{\bar\phi_0}(z)\\
     &+{2.001\,10^7\over s}(E_{\phi_0}+Z_{\phi_0})
        +9\,10^5L^2s^2E_{\phi_1}.
 \end{split}                                                   \tag{L23}
\]

This is a closed expression for the previously unspecified local work
and cutoff work. It is not a closed estimate for all terms on its right.

## 7. Exact limitation and continuation

No density-gradient dissipation has been proved by (L20); the positive
`s^6 D(z)` term in (L23) remains a separate obligation. Also the
nonintegrable coefficient `C/s` matters. The facts that the energies
vanish at activation and are `O(s^2)` do not launch Gronwall with a
coefficient this large. For instance `y(s)=s^2` satisfies
`y'<=C*y/s`, `y(0)=0` for every `C>=2`. Starting at a positive
time tau and sending tau to zero leaves an uncontrolled term
`(s/tau)^C*y(tau)`. Finite nesting of cutoffs alone does not repair
that startup problem.

Thus (L22) is uniform collar control in the coarse bootstrap norm,
not a proof of collar smallness at the strength needed for pointwise
compression. A successful continuation must keep more of the signed
reaction/weight cancellation in (H36), or use a suitably coupled energy,
and then control density gradients and obtain actual pointwise smoothing.
The initial activation data, the provisional prefix envelope, and the
central-quarter conclusion are not identified with one another here.

## 8. Provenance and review scope

The proof uses only the unchanged finite-cell equations, exact polynomial
material law, the reference ODE, finite summation, elementary integral
estimates of numerical series, and Young's inequality. There are no
external theorem or numerical-trajectory leaves. The local estimate uses
the heat note's conditional state box and constitutive inverse, and the
exact radial compression identity from the startup note. The cutoff
estimate uses the actual conductance geometry already proved in (H26).

Primary self-review verdict: **conditional on the actual prefix envelope**
for (L1), (L20)--(L23), with the stated monotonicity and halo requirements
for the cutoffs. Source/reference cancellation, constitutive paths,
central-cell shear, finite Hardy weights, moving volumes, coefficient
powers, and collar endpoints were checked. Propagating the envelope,
the density-gradient estimate, singular-startup cancellation, and the
pointwise central implication are not proved here. Independent review
of this new local estimate is separate.

Focused mathematical proofreading covered this file in self-review mode;
no further routine edits or mathematical-token corrections were needed.
Exact rational checks passed for the derivative table, constitutive
conversion, Hardy constant, local-work coefficient roundings, and nested
cutoff coefficient. The first 23 equation tags are unique, display delimiters
and braces balance, and scoped whitespace validation passed. These checks
are algebraic validation, not numerical solution evidence.

Input SHA-256 hashes; paths are relative to `stable_stress_search`:

| Input | SHA-256 |
| --- | --- |
| collapse.py | 14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf |
| material.py | 4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390 |
| entropy_transport/transport.py | 2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c |
| entropy_transport/convective_transport.py | ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97 |
| entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/heat_absorption.md | b98843cec40271ef4a16bdb6c15baf50a43c203d6367fbf3ae72a4d299b74379 |
| entropy_transport/floor_theorem/startup_energy_route.md | 06630aecae84c9b618e84c1ddded3f2025f7a89f7dca634bbbb05f50d0e2380b |

## 9. Further step: a uniformly controlled reaction-flow chart

The singular coefficient in (L1) is not an intrinsic singularity of the
physical reaction ODE. This section constructs its flow coordinates and
tests the transformed spatial principal part. It is a further argument,
not an assertion that (L23) already closes.

For a prefix of any length J, let `X=(rho,x,K)`, and put

\[
 w_i=\rho_i^{-1},\quad W_i^m=\sum_{j\le i}w_j,\quad
 p_i={w_i\over W_i^m},\quad \beta_i=1-p_i,\quad
 m_i={\sum_{j\le i}w_jx_j\over W_i^m}.
\]

The superscript m distinguishes the prefix mass-coordinate sum from the
material function W. Define `T_1=0`, and, for `i>=2`,

\[
 T_i={2\over3}\beta_i(x_i-m_{i-1})^2.
\]

This is exactly (L15), expressed in physical cell variables, because
`r_(i-1)^3/r_i^3=W_(i-1)^m/W_i^m=beta_i`.
Define the autonomous reaction vector field

\[
 \mathscr F_i(X)=
  \left(\rho_ix_i,\;
    4\pi\rho_i+x_i^2/3+T_i,\;
    h_i\{\tfrac12(1+g_i)x_i^2-x_i\}\right).
                                                               \tag{L24}
\]

On the actual branch `rho>=1`, `x>2`, `K>=0`, this is exactly the
nonspatial part of the unchanged equation, including both heaters and
the entire radial shear. In particular, no term of R has been discarded.
The full prefix equation is

\[
 X'=\mathscr F(X)+\mathscr P(X),\qquad
 \mathscr P(X)=(0,\mathcal L_rS,H).                    \tag{L25}
\]

Fluxes through the prefix boundary remain in P. The reaction field itself
depends only on cells inside the prefix.

There is a small coordinate-domain issue at the boundary of the physical
state set. Backward reaction flow of an admissible heated state can
cross K=0, and an actual x arbitrarily close to two can cross x=2.
For a classical differentiable coordinate chart, use the displayed active
formula in (L24) on the auxiliary open box

\[
 \mathscr D=\{.98<\rho_i<1.03,\;1<x_i<9,
                         \;-.001<K_i<.001\}.
\]

Here g is its same rational formula, whose pole `K=-.01` lies outside
the box; h and W retain their original density branches. The active
heater polynomial in x is continued only to define coordinates outside
the actual branch. This auxiliary vector field agrees exactly with the
physical reaction at every actual state used in (L25). No solution of
the physical equations outside their accepted-state domain is asserted,
and no physical law or code is altered. Alternatively the clipped old
heater gives an exact locally Lipschitz reaction flow on its larger
algebraic domain, with the same Lipschitz estimates; the smooth active
continuation is used below to have an ordinary Jacobian throughout the
chart. Since h and its first derivative agree at rho=1, (L24) is C1 on
the chart even at activation.

Here are explicit bounds showing that the chart is uniform in J and N.
Equip cell vectors with either the maximum norm or the fixed-mass norm

\[
 \|\delta X\|_{2,dm}^2
 =dm\sum_{i\le J}(|\delta\rho_i|^2+|\delta x_i|^2
                                      +|\delta K_i|^2).
\]

On the chart, weighted prefix averages have maximum-norm operator norm
one. Their fixed-mass L2 operator norm is at most
`(1.03/.98)*sqrt(6)<2.6`, by the elementary series proof used for
(L16). This holds also for the shifted operator `m_(i-1)`, with its
first output zero. Differentiating the averages gives

\[
 \delta m_i=\langle\delta x\rangle_i
     -\left\langle (x-m_i){\delta\rho\over\rho}
                                                  \right\rangle_i,
 \quad
 \delta\beta_i=p_i\left\{{\delta\rho_i\over\rho_i}
                  -\left\langle{\delta\rho\over\rho}
                                                \right\rangle_i\right\}.
                                                               \tag{L26}
\]

Since `|x-m|<=8`, these imply
`||delta beta||_(2,dm)<=4||delta rho||_(2,dm)` and
`||delta m||_(2,dm)<=2.6||delta x||_(2,dm)
+(8/.98)*2.6||delta rho||_(2,dm)`. Consequently

\[
 \|\delta R\|_{2,dm}
 \le411\|\delta\rho\|_{2,dm}+45\|\delta x\|_{2,dm}.
                                                               \tag{L27}
\]

For example the density coefficient before rounding is bounded by
`13+(128/3)*4+(32/3)*(8/.98)*2.6<411`; the compression
coefficient is `6+(32/3)*(1+2.6)<45`.
The maximum-norm bound similarly gives
`||delta R||_infty<=237||delta rho||_infty
+28||delta x||_infty`.

On the auxiliary box, `|g|<=1/9`, `g'<=124`, `h<=.003`, and
`|h'|<=.18`. Thus Q has derivative bounds `7`, `.027`, and `16`
with respect to rho, x, and K. The first component of F has derivative
bounds nine and 1.03. The Frobenius norm of the scalar majorant matrix

\[
 \begin{pmatrix}9&1.03&0\\411&45&0\\7&.027&16\end{pmatrix}
\]

is less than 500. The corresponding maximum-norm bounds are less than
300. Therefore

\[
 \|D\mathscr F\|_{2,dm\to2,dm}\le500,\qquad
 \|D\mathscr F\|_{\infty\to\infty}\le300,              \tag{L28}
\]

with constants independent of N, J, and the first-cell radius.

Let `T=10^(-3)` and let B be the physical state box
`1<=rho<=1.01`, `2<=x<=8`, `0<=K<=1600T^3`.
The chart vector field has componentwise magnitudes at most
`9.27`, `83`, and `.108` on D. Starting in B, its forward and
backward flow for time of magnitude at most T therefore stays inside D:
the respective displacements are at most `.00927`, `.083`, and
`.000108`, each less than the distance from B to the corresponding
chart boundary. This is a direct first-exit argument, valid for each
finite J. Write this flow as `Phi_t^(J)`. It follows from (L28) and the
variational equation that

\[
 \begin{split}
 \|\Phi_t(X)-\Phi_t(\widetilde X)\|_{2,dm}
  &\le e^{500|t|}\|X-\widetilde X\|_{2,dm},\\
 \|D\Phi_t\|_{2,dm\to2,dm},\;
 \|(D\Phi_t)^{-1}\|_{2,dm\to2,dm}
  &\le e^{500|t|}.
 \end{split}                                                   \tag{L29}
\]

The analogous maximum-norm estimates have exponent 300. The inverse
in the second line is evaluated along the same flow segment; it is the
derivative of the backward flow. These statements hold in neighborhoods
of B for which the indicated flow segments remain in D. The flow fixes
the homogeneous subspace: when all cells have the same rho, x, and K,
the shear vanishes exactly and the common values solve (L3). In
particular `Phi_s(X_a)=X_d(s)` for the constant activation state X_a.

## 10. The pullback removes the local reaction exactly

Define, along the actual prefix solution,

\[
 Y(s)=\Phi_{-s}(X(s)),\qquad J_s(Y)=D\Phi_s(Y).
\]

The group identity for this autonomous auxiliary flow gives
`partial_s Phi_(-s)(X)=-D Phi_(-s)(X)*F(X)`.
Because F agrees with the physical reaction at the actual state,
the chain rule and (L25) give the exact equation

\[
 \boxed{\quad
 Y'=J_s(Y)^{-1}\mathscr P(\Phi_s(Y)),\qquad
 Y_d=X_a\text{ is constant}.
 \quad}                                                \tag{L30}
\]

There is no local reaction term and no coefficient of size `1/s` in
this equation arising from differentiating the reaction flow. The
Jacobian and its inverse are bounded by (L29). This is a genuine removal
of the Fuchsian reaction seen after constitutive inversion, not a
restatement of a norm depending on a compression error. It does not
remove boundary fluxes, the actual geometry of L, or the heat flux H.

For a nonhomogeneous state J is generally a nonlocal prefix operator:
(L26) shows its dependence on all inner cells. Bounds in the fixed-mass
L2 norm do not by themselves control its commutator with a spatial
difference. Hence one cannot infer the sign of the spatial energy work
in (L30) solely from (L29). There is a sharper obstruction even at the
homogeneous reference, where the Jacobian is local and this commutator
does not occur.

## 11. Why a uniformly coercive local quadratic metric cannot follow

Consider the internal spatial principal linearization at the homogeneous
reference. Its heat gate is closed. The exact gated luminosity has zero
first variation there: both its entropy-gradient gate and its potential
drop vanish, so its product is at least quadratic in perturbation size
at a fixed finite mesh and a fixed positive s. The mechanical principal
matrix in the physical variables `(rho,x,K)` is therefore

\[
 \mathsf A_X=\mathsf e_x\otimes\nabla S
 =\begin{pmatrix}0&0&0\\ S_\rho&\nu&S_K\\0&0&0\end{pmatrix}.
                                                               \tag{L31}
\]

The scalar graph Laplacian multiplies this matrix. Geometry variations
acting on the constant internal reference stress give no internal
principal contribution. Exterior reference work remains a boundary term.
The derivative of shear also vanishes at the homogeneous state because
the difference in (L15) is zero. Thus `D Phi_s(X_a)` is an identical
local three-by-three matrix at every prefix cell, and the transformed
internal principal matrix is exactly

\[
 \mathsf A_Y=J_s^{-1}\mathsf A_XJ_s.                    \tag{L32}
\]

Suppose a local quadratic metric M for the physical variables were
uniformly bounded and uniformly positive definite as `s` decreases to
zero, and its principal graph energy were dissipative. For a rank-one
matrix `u*v^T`, positive semidefiniteness of
`sym(M*u*v^T)` requires `M*u=lambda*v`, with `lambda>=0`.
Indeed, if the two vectors are not parallel, the restriction of the
symmetric product to their two-dimensional span has negative
determinant. For (L31), positivity of M implies `lambda>0`, and its
rho-x and x-x entries consequently satisfy

\[
 {M_{\rho x}\over M_{xx}}={S_\rho\over\nu}.            \tag{L33}
\]

This is also necessary if one permits an additional zero-order energy
error with a constant independent of N: a negative direction in the
principal quadratic form would be amplified by arbitrarily large
internal graph frequencies as N increases.

Put `a=C_a`. The exact reference ODE and polynomial ramp give

\[
 \begin{gathered}
 \rho_d=1+as+O(s^2),\quad K_d=O(s^3),\\
 \nu_d=\tfrac94a^2s^2+O(s^3),\qquad
 S_{\rho,d}=\tfrac92a(a-2)s+O(s^2),\\
 {S_{\rho,d}\over\nu_d}
       ={b\over s}+O(1),\qquad b={2(a-2)\over a}>0.
 \end{gathered}                                               \tag{L34}
\]

The big-O constants here concern the fixed reference ODE and have no N
dependence. If M had `M>=c I` and `||M||<=C`, with c and C positive
and independent of s, the left side of (L33) would be bounded by C/c.
The right side diverges by (L34). This is impossible. Since J and its
inverse are uniformly bounded by (L29), a uniformly coercive local
metric for (L32) would pull back to one for (L31). Reaction-flow
coordinates therefore do not supply such a metric either.

The obstruction concerns local quadratic metrics uniformly equivalent
to the physical L2 norm as `s->0`, whose internal spatial work is
dissipative up to uniform zero-order terms. It does not rule out a
degenerate time-weighted metric, gradient or nonlocal energies,
frequency-dependent estimates, or the desired compression theorem.

## 12. The natural pullback metric remains time-degenerate

At the linearized level the existing energy `E+Z` has the local physical
quadratic form, omitting its common volume factor,

\[
 \mathsf m_X(\delta X)=
 { (S_\rho\delta\rho+\nu\delta x+S_K\delta K)^2\over\nu}
 +{(\delta\rho)^2\over\rho^2}
 +{\rho\over\sqrt W}
       (\Psi_\rho\delta\rho+\Psi_K\delta K)^2.         \tag{L35}
\]

Its pullback is exactly `m_Y(delta Y)=m_X(J_s delta Y)`.
Along the reference, the largest eigenvalue of this form stays
comparable to one and its smallest eigenvalue is comparable to `s^2`.
For example `m_X(e_x)=nu~s^2`, while its density and K coercivities
stay positive; the exact three squares in (L35) show the matching lower
bound of order `s^2`. Multiplication by the bounded invertible J in
(L29) preserves these orders. Thus the chart does not turn the existing
energy into a nondegenerate metric, even though it exactly removes the
reaction from the equation.

The leading two-by-two calculation makes the cross energy visible.
Use `(delta rho,delta x)` and momentarily suppress K perturbations.
Write `gamma=9a^2/4`. At the reference,
`nu=gamma*s^2+O(s^3)`, `S_rho/nu=b/s+O(1)`, and the mechanical
part of the flow Jacobian has

\[
 J_s=\begin{pmatrix}1+O(s)&s+O(s^2)\\O(s)&1+O(s)\end{pmatrix}.
\]

Consequently the transformed mechanical principal matrix has leading
form

\[
 \mathsf A_Y=\nu
 \begin{pmatrix}
 -b+O(s)&-(1+b)s+O(s^2)\\
 b/s+O(1)&1+b+O(s)
 \end{pmatrix}.                                      \tag{L36}
\]

For its displayed leading matrix, the actual pullback of the stress
and density squares in (L35) is

\[
 \mathsf m_Y^{\rm lead}
 =\gamma s^2\{(b/s)\delta Y_\rho+(1+b)\delta Y_x\}^2
                +(\delta Y_\rho+s\delta Y_x)^2.       \tag{L37}
\]

This includes the density-compression cross term of order s. It does
symmetrize the leading rank-one principal matrix: for
`u=(-s,1)^T`, `v=(b/s,1+b)^T`, its metric matrix satisfies
`M*u=gamma*s^2*v`. But its determinant is `gamma*s^2` and its
condition number grows as `s^(-2)`. Its time derivative is not a
uniformly bounded multiple of the metric. For example, in the pure
`delta Y_x` direction its value is
`[gamma*(1+b)^2+1]*s^2`, whose logarithmic derivative is `2/s`.
Using this metric in the reaction-free equation therefore requires a
separate signed treatment of its time dependence and its coupling to
the density direction. The absence of F from (L30) alone supplies
neither treatment.

This does not prove that the coefficient two is an unavoidable loss
in a sharper estimate on the actual startup data: the activation pullback
has zero error in every component, and the spatial forcing and possible
gradient corrections matter. It proves that merely using the bounded
reaction chart and the pullback of `E+Z` does not remove the singular
metric derivative. Normalizing (L37) by `s^(-2)` makes the density
coefficient singular instead. A successful further energy must handle
that density coupling rather than declare the time weight harmless.

## 13. Outcome of the reaction-flow attempt and review boundary

The physical reaction vector field is uniformly regular at activation.
Equations (L24)--(L30) give an actual uniformly bi-Lipschitz coordinate
map and remove all local reactions, including shear, from the equation
on the provisional prefix. No constitutive inverse or `1/s` coefficient
is needed to construct that map. This resolves the question whether
the local singularity can be removed at the equation level: it can.

The same step does not produce a uniform nondegenerate local energy.
The closed-gate mechanical principal matrix forces (L33), and its
`b/s` ratio survives every uniformly bounded reaction chart. The
available cross energy (L37) is explicitly time-degenerate. In the
nonhomogeneous problem the chart also introduces nonlocal spatial
commutators. Controlling these by a complete gradient or nonlocal
energy, together with startup time weights and actual pointwise
smoothing, remains open. This is a precise obstruction to the proposed
chart-only closure, not a counterexample to the specified trajectory.

Self-review of this appended argument checked the exact prefix weights,
the first-cell convention, the coordinate extension off the physical
branch, forward and backward chart existence, the two operator norms,
the homogeneous invariant branch, the zero first variation of gated
heat, rank-one symmetrization, and all powers in (L34)--(L37).
Its primary verdict is **conditional on the actual prefix envelope**
for the transformed actual equation, with the stated no-go conclusion
restricted to uniformly coercive local quadratic metrics. Independent
review remains separate; no common-time amplitude or seeding claim is
made.

Validation after the append: all 37 equation tags are unique, braces and
display delimiters balance, and scoped whitespace validation passed.
Exact rational checks passed for the enlarged-box Hardy constant,
reaction derivative bounds in both norms, and the forward/backward
first-exit margins. These checks contain no physical trajectory run.
