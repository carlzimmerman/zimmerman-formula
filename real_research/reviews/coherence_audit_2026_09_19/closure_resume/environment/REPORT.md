# Nonlinear clock acceleration: an explicit static construction and its separation cost

2026-09-19. Base commit `23d3890790291c0ec44b4ca7da784a806d7094d2`.
This is a new internal-theory calculation, with no external writes or commits.
It replaces the constant acceleration term by a function of the same invariant and
explicitly retunes the existing scalar kernel; it adds no new field.
It does not certify the cosmological, preferred-frame, causal, or strong-coupling gates.

**Result.** A decreasing clock coefficient is compatible with positive Newtonian normalization,
a monotone MOND mass flux, a bounded extra force, and positive frozen principal matrices.
The explicit `p=1/2` construction below supplies a counterexample to a blanket static no-go.
The proposed `p=1` profile fails longitudinal clock health at the stated contrast.
The main remaining obstruction is separation of environments: positivity of the longitudinal
clock coefficient alone requires an acceleration ratio exceeding approximately five million
between any finite cosmic environment retaining `alpha=0.5` and a local environment at `alpha=1e-7`.
The exactly homogeneous background has zero acceleration and does not test this requirement.

## 1. Action, regime, and factors

Use `c=1`, signature `(-+++)`, and the normalized gravitational action

\[
 S={1\over16\pi G}\int N\sqrt h\,
 [R^{(3)}+K_{ij}K^{ij}-(1+c_2)K^2-2\Lambda
 +f(X)+2d a^iD_i\phi-dJ(Y)-F(Q)]\,dt\,d^3x+S_m,
\]

where `a_i=D_i log N`, `X=a_i a^i`, `Y=D_i phi D^i phi`, and `d=2-K_B=9/5`.
The clock is in unitary gauge; the local static branch has zero shift and
`phi=Qbar t+P(x)`. This calculation keeps the acceleration nonlinearities while
expanding the metric potentials to leading Newtonian order. As in L279, the acceleration
scales are counted at the same weak-field order as the gradients, so their ratios remain finite.
Set `f(0)=J(0)=0`; additive constants otherwise renormalize the vacuum term.

The local static derivative terms are independent of `c2` and of the detailed time function `F`.
Nonzero `Qbar`, condensate density, expansion, and their lower-derivative feedback must still be
retained in the cosmological and finite-wavelength problems. Here `rho` denotes the local
pressureless mass source on the branch where those extra local sources are negligible.

Write `N=1+Psi`, `h_ij=(1-2Phi)delta_ij`, `g=grad Psi`, and `v=grad P`.
After integration by parts the Newtonian Lagrangian is

\[
 L_{\rm NR}=2|\nabla\Phi|^2-4\nabla\Phi\cdot\nabla\Psi
 +f(|g|^2)+2d g\cdot v-dJ(|v|^2)-16\pi G\rho\Psi.
\]

For example, with the conformal spatial metric `h_ij=exp(-2Phi)delta_ij`,
`N sqrt(h) R3=(1+Psi)exp(-Phi)[4 Delta Phi-2(grad Phi)^2]` gives exactly
these Einstein-Hilbert coefficients through quadratic order modulo a boundary derivative.
The exact lapse variation of `N f(a^2)` contributes
`f-2X f_X-2 D_i(f_X a^i)`; the first two terms are beyond the retained Newtonian order.
Spatial stresses from `f` and the scalar also start at the next metric order.

Varying the two metric potentials and the scalar gives

\[
 4\Delta\Phi-2\nabla\cdot(f_X g)-2d\Delta P=16\pi G\rho,
 \qquad \Delta(\Psi-\Phi)=0,
 \qquad \nabla\cdot[J_Yv-g]=0.                 \tag{1}
\]

With vanishing harmonic difference under the usual isolated-source boundary conditions,
`Psi=Phi`, and the two remaining potentials satisfy

\[
 \boxed{\nabla\cdot[A(|g|^2)g-dv]=8\pi G\rho,
 \qquad\nabla\cdot[j(|v|^2)v-g]=0},
 \quad A=2-f_X,\quad j=J_Y.                  \tag{2}
\]

For constant `f_X=alpha`, these reproduce L279's Hamiltonian and scalar equations,
including its factor `beta0=d/(2-alpha)`. In nonspherical geometries the divergence equations
do not imply equality of their vector fluxes: curl terms must be solved.

## 2. Longitudinal, transverse, and arbitrary-direction symbols

Define the clock Hessian eigenvalues

\[
 \alpha_T=f_X,\qquad \alpha_L=f_X+2Xf_{XX},
 \quad A_T=2-\alpha_T,\quad A_L=2-\alpha_L,
\]

and the scalar Hessian eigenvalues

\[
 B_T=j,\qquad B_L=j+2YJ_{YY}.
\]

After eliminating the metric slip, minus the derivative Lagrangian is the energy density
`E=2|g|^2-f(|g|^2)-2d g.v+dJ(|v|^2)`.
Its half-Hessian in independent gradients is

\[
 {1\over2}D^2E=\begin{pmatrix}\mathsf A&-dI\\-dI&d\mathsf B\end{pmatrix},
 \quad \mathsf A=(2-f_X)I-2f_{XX}gg^T,
 \quad \mathsf B=jI+2J_{YY}vv^T.             \tag{3}
\]

For a Fourier direction `khat`, the actual two-potential symbol divided by `|k|^2` is

\[
 M(\hat k)=\begin{pmatrix}A_\theta&-d\\-d&dB_\theta\end{pmatrix},
 \quad A_\theta=2-f_X-2f_{XX}(g\cdot\hat k)^2,
 \quad B_\theta=j+2J_{YY}(v\cdot\hat k)^2.     \tag{4}
\]

Thus the positive static branch has `A_theta>0` and `A_theta B_theta>d`
for every direction. For aligned `g,v`, the endpoint matrices are
`M_T=[[A_T,-d],[-d,d B_T]]` and `M_L=[[A_L,-d],[-d,d B_L]]`.
On an aligned background these two positive matrices suffice, since the intermediate
matrix is their convex combination with weight `cos^2(theta)`. Nonaligned backgrounds
require the full directional condition (4). The construction below proves the stronger
six-gradient positivity in (3), including nonaligned backgrounds.

The response to a small localized density perturbation on a frozen environment is

\[
 G_{\rm eff}(\hat k)={2G\over A_\theta-d/B_\theta}.                \tag{5}
\]

It is directional until an isotropic limit is reached. If a healing term is specifically
`-d ell^2 |D_iD_j P|^2`, replace `B_theta` by `B_theta+ell^2 |k|^2` in (4)-(5).
Then the scalar is suppressed at high spatial frequency and `G_eff -> 2G/A_theta`.
The fourth-order principal diagonal is positive for `ell^2>0` and `A_theta>0`.
This operator regularizes the zero-field MOND degeneracy at each nonzero `k`, but does not
give a uniform second-order lower bound as `k -> 0`.

There is also a direct frozen dynamical check. In the two-derivative short-wavelength
scalar ADM sector, write the spatial scalar metric perturbation as `z`, lapse perturbation
as `n`, and MOND perturbation as `p`. Eliminating the longitudinal shift gives

\[
 K_z={2(2+3c_2)\over c_2},
 \qquad L_{\rm grad}/k^2=2z^2+4zn+\alpha_\theta n^2+2dnp-dB_\theta p^2,
\]

where `alpha_theta=2-A_theta`. Eliminating `n=-(2z+dp)/alpha_theta` produces

\[
 H=\begin{pmatrix}
 4/\alpha_\theta-2&2d/\alpha_\theta\\
 2d/\alpha_\theta&dB_\theta+d^2/\alpha_\theta
 \end{pmatrix},\quad
 \det H={2d\over\alpha_\theta}[(2-\alpha_\theta)B_\theta-d].       \tag{6}
\]

For `c2>0`, positive scalar time coefficient, `0<alpha_theta<2`, and the static
condition, these frozen principal kinetic and gradient matrices are positive.
Finite background `Q`, gradients in the metric, and derivative mixing enter the
lower-order terms omitted here; (6) is not a finite-`k` stability proof.
A negative `alpha_L` gives `H_zz<0` in the longitudinal direction and fails this principal test
even if the static gravitational matrix remains positive.

## 3. Test the proposed f profiles

Let `u=X/Astar^2`, `Delta=alpha_hi-alpha_lo>0`, and

\[
 f_X=\alpha_{\rm lo}+{\Delta\over(1+u)^p},\qquad
 \alpha_L=\alpha_{\rm lo}+\Delta{1+(1-2p)u\over(1+u)^{p+1}}.      \tag{7}
\]

For `p=1/2`, take the explicit action

\[
 \boxed{f(X)=\alpha_{\rm lo}X+
 2\Delta A_*^2[\sqrt{1+X/A_*^2}-1]},\qquad
 \alpha_L=\alpha_{\rm lo}+{\Delta\over(1+u)^{3/2}}.             \tag{8}
\]

Both clock eigenvalues are strictly positive for every `X>=0`, and
`alpha_lo <= alpha_L <= alpha_T <= alpha_hi < 2`.
In particular `A_L>=A_T>=Ahi=2-alpha_hi>0`; decreasing `alpha` improves the
gravitational block. The nonzero `alpha_lo` prevents this classical principal
normalization from vanishing at infinite acceleration. It supplies no EFT cutoff estimate.

For `p=1`, the primitive is `f=alpha_lo X+Delta Astar^2 log(1+u)` and

\[
 \alpha_L=\alpha_{\rm lo}+\Delta{1-u\over(1+u)^2},\qquad
 \min_{u\ge0}\alpha_L=\alpha_{\rm lo}-\Delta/8\quad(u=3).
\]

At `alpha_hi=1/2`, `alpha_lo=1/10^7`, the minimum is exactly
`-4999991/80000000=-0.0624998875`. It is negative from approximately
`u=1.0000008000008` to `u=4999995.9999992`. This is a genuine analytic
counterexample to using that profile with positive longitudinal clock stiffness.
It is not a static gravitational ellipticity failure: `A_L` instead increases there.

## 4. Explicit bounded scalar construction

Set `Ahi=2-alpha_hi`, `Alo=2-alpha_lo`, and `b=d/Ahi`.
For `0<=v=sqrt(Y)<V`, choose

\[
 \boxed{J_Y={b\over1-v/V}},\qquad
 \boxed{J(Y)=-2bV\sqrt Y-2bV^2\log(1-\sqrt Y/V)}.              \tag{9}
\]

The cancellation at `Y=0` gives `J(Y)=bY+(2b/3V)Y^(3/2)+...`.
The radial derivative of `jv` is `B_L=b/(1-v/V)^2`, while `B_T=b/(1-v/V)`.
They are at least `b`, strictly greater for `v>0`.
Together with `mathsf A>=Ahi I`, this proves positivity of (3) away from simultaneous
`g=v=0`: its Schur complement is bounded below by
`d[mathsf B-d/Ahi I]>=0`, and one of the blocks is strictly improved whenever a
background gradient is nonzero. Equivalently, write `A_theta=Ahi+a`, `B_theta=b+b1`;
then `A_theta B_theta-d=Ahi b1+b a+a b1>0` whenever `a+b1>0`.
At `g=v=0`, equality is the intended MOND zero-field degeneracy.
The domain `v<V` has a divergent derivative barrier, not a continuation through a finite
polynomial kernel. Nonlinear solution existence and evolution toward this boundary are not proved.

On an isolated spherical branch with zero scalar flux constant, equations (2) integrate to

\[
 A(g^2)g-dv=2g_b,\quad j(v^2)v=g,
 \quad g_b={GM(<r)\over r^2},\quad
 v={Vg\over g+bV}.                                         \tag{10}
\]

The actual source flux is

\[
 \boxed{\mathcal F(g)=A_{\rm lo}g-
 \Delta A_*{g\over\sqrt{A_*^2+g^2}}-
 dV{g\over g+bV}=2g_b}.                                   \tag{11}
\]

For every `g>0`, it is positive and strictly increasing, because

\[
 {\mathcal F(g)\over g}=(A-A_{\rm hi})+
 A_{\rm hi}{g\over g+bV}>0,
\]
\[
 \mathcal F'(g)=(A_L-A_{\rm hi})+
 A_{\rm hi}\left[1-\left({bV\over g+bV}\right)^2\right]>0.    \tag{12}
\]

These are global analytic inequalities on the stated domain, not a finite numerical scan.
The small-field limit is `mathcal F=g^2 Ahi^2/(dV)+O(g^3)` and the large-field limit is
`mathcal F/g -> Alo`. Define the actually measured asymptotic constant and acceleration by

\[
 \boxed{G_N={2G\over A_{\rm lo}}={G\over1-\alpha_{\rm lo}/2}},
 \quad g_N={G_N M\over r^2},\quad
 \boxed{a_0={dA_{\rm lo}V\over A_{\rm hi}^2}}.                \tag{13}
\]

Then `g^2~a0 g_N` in deep MOND. To fix `a0`, set
`V=a0 Ahi^2/(d Alo)`, approximately `0.62500003125 a0` at the requested coefficients.
The scalar force entering the metric is bounded, and the total excess has the finite ceiling

\[
 0<g-g_N={\Delta A_*g/\sqrt{A_*^2+g^2}+dVg/(g+bV)\over A_{\rm lo}}
 <{\Delta A_*+dV\over A_{\rm lo}}.                           \tag{14}
\]

It approaches this ceiling from below. The relative correction tends to zero and
`G_eff` becomes the positive isotropic value (13). The clock itself contributes the
constant tail `Delta Astar/Alo`; healing the scalar alone cannot remove it.
No Solar-System force bound has been applied here.

The old constant-local-alpha deep-MOND baseline cannot be retained:
`J_Y(0)=d/Alo` gives `Ahi J_Y(0)-d=d(Ahi/Alo-1)<0`.
For the new action the baseline is `b=d/Ahi=1.2`, not approximately `0.9`.
This change also alters the homogeneous perturbation action through `J_Y(0)` and must be
carried into the parent's cosmological analysis. Vanishing homogeneous `Y` does not erase
the quadratic spatial-gradient coefficient.

## 5. Reconstruction of a desired spherical interpolation

Given a desired target `g_N=mu(g)g` with the measured `G_N` in (13), define

\[
 v(g)={g[A(g)-A_{\rm lo}\mu(g)]\over d},\quad
 j(v(g)^2)={g\over v(g)},\quad
 J(v^2)=\int_0^v2g(w)\,dw.                                 \tag{15}
\]

A positive, increasing invertible scalar branch requires

\[
 A-A_{\rm lo}\mu>0,\qquad
 A_L-A_{\rm lo}(\mu+g\mu')>0.                              \tag{16}
\]

If also `mu>0` and `mu+g mu'>0`, the transverse and longitudinal coupled determinants
are positive on that branch:

\[
 A j-d={A_{\rm lo}\mu g\over v}>0,\qquad
 A_L B_L-d={A_{\rm lo}(\mu+g\mu')\over v'}>0.
\]

All directions on the aligned branch follow by the matrix convexity noted after (4).
Nonaligned backgrounds still require (4); the explicit choice (9) meets that stronger
requirement. Formula (15) is a spherical reconstruction,
not an exact field redefinition to arbitrary-source AQUAL.

For (8), a target whose absolute boost vanishes exponentially at high `g` eventually
has `v<0`, because the clock alone has the nonzero tail in (14).
An *exactly constant* total boost `g-g_N=C` instead has

\[
 v={A_{\rm lo}C-\Delta A_*g/\sqrt{A_*^2+g^2}\over d},\qquad
 v'=-{\Delta A_*^3\over d(A_*^2+g^2)^{3/2}}<0.
\]

Thus an exact high-field plateau also fails the positive scalar branch for this profile.
A smooth approach to a ceiling from below, as in (14), works. The old carried exact-saturation
kernel cannot be transferred verbatim to (8).

## 6. Environmental separation is the outstanding loading test

Let `g_cos` be the largest invariant clock acceleration that must retain the cosmological
coefficient and `g_loc` the smallest that must reach the local coefficient.
This is `sqrt(a_i a^i)` in the clock frame. At linear order in a gauge with a clock perturbation
`T`, it involves `|grad(Psi-dot T)|`; it is not automatically the Newtonian metric gradient.

For any positive differentiable `alpha(g)=f_X(g^2)`,

\[
 \alpha_L=\alpha+g\alpha'={d\over dg}[g\alpha(g)]>0
 \quad\Longrightarrow\quad
 {g_{\rm loc}\over g_{\rm cos}}>
 {\alpha(g_{\rm cos})\over\alpha(g_{\rm loc})},
 \quad 0<g_{\rm cos}<g_{\rm loc}.                            \tag{17}
\]

Near the proposed endpoints this is a separation of order `5*10^6`.
It is a profile-independent consequence of the desired longitudinal health condition.
It does not constrain the exactly homogeneous `g_cos=0` configuration.

For (8), demand
`alpha(g_cos)>=alpha_hi-eps_cos Delta` and
`alpha(g_loc)<=alpha_lo+eps_local Delta`, with each epsilon in `(0,1)`.
The exact compatibility interval is

\[
 {g_{\rm cos}\over\sqrt{(1-\epsilon_{\rm cos})^{-2}-1}}
 \le A_*\le
 {g_{\rm loc}\over\sqrt{\epsilon_{\rm local}^{-2}-1}}.         \tag{18}
\]

It is nonempty only when the ratio of those square roots is at most `g_loc/g_cos`.
For a local excess tolerance `kappa alpha_lo`, set
`eps_local=kappa alpha_lo/Delta`; a very small local coefficient makes the upper
bound on `Astar` correspondingly small. If the required finite cosmic and local
acceleration ranges overlap, no single function of `X` can distinguish them.
The construction therefore relocates the loading question to an explicit invariant-range
test; it has not solved that test merely by leaving FLRW's `X=0` unchanged.

## 7. Prior repository work and limits on transfer

- `real_research/clock_2026/L279_quasistatic_slip_from_action.py` and its note derive the
  constant-alpha two-potential factors reproduced here. This calculation extends those
  factors; it does not inherit their old numerical kernel or preferred-frame output.
- `closure_2026/theory_discovery/khronometric_mond_gauntlet_2026.py` studies a clock-only
  acceleration-dependent MOND coefficient `2 exp(-g/a0)`, and already flags strong coupling
  and position-dependent PPN as unresolved. Its health substitution uses an isotropic
  constant-coupling formula. The corresponding longitudinal derivative has a factor
  `(1-g/a0)`, so its positive transverse coefficient alone is insufficient for the
  directional test in (6). This is not a rerun or a blanket rejection of every repair in that branch.
- `closure_2026/linear_curvature_clock_2026/REPORT.md` explicitly retains directional
  coefficients but adds different curvature constraints. Its constraint count and
  radiation result do not transfer to this action.
- `theory_2026/first_principles/sec9_second_variation_symbol.py` derives arbitrary-direction
  symbols for a distinct tidal-curvature two-field action. Its ellipticity or finite-scale
  verdict does not substitute for (3)-(6).

The parent task independently checked the primary-source discussions at
[Milgrom, arXiv:1102.1818v2](https://arxiv.org/pdf/1102.1818) and
[Bonetti and Barausse, arXiv:1502.05554v2](https://arxiv.org/html/1502.05554v2).
Those sources concern acceleration-dependent gravity, possible suppression of cosmic-ray
Cherenkov emission, and preferred-frame/strong-coupling analyses in their own actions.
Their conclusions require a fresh transfer calculation for this additional MOND scalar,
the nonzero acceleration floor, and its healing operator.

For reference, the decoupled clock formula from the ADM block is
`c_clock^2=c2(2-alpha)/[alpha(2+3c2)]`, giving `9/209` and speed approximately `0.2075`
at `alpha=0.5,c2=0.03`. It is not a claim about an eigenvalue of the coupled system,
nor a Cherenkov exclusion or pass. Likewise no old alpha1/alpha2 formula is substituted
with `alpha_lo` to assert a PPN pass.

## 8. Reproducibility and interpretation

`check_environment.py` independently varies the Newtonian action, takes its generic
three-dimensional Taylor Hessian, eliminates frozen ADM auxiliaries, and checks the exact
identities used in the inequalities above. It includes two adverse controls: the `p=1`
longitudinal coefficient and retaining the old `J_Y(0)` baseline.
All calculations use exact SymPy expressions and rational parameters; decimal roots are
reporting only. The analytic domains and non-claims are recorded in `contract.json`.

The bounded runner command and actual provenance are in `run/manifest.json`; scientific
results are in `run/results.json`, with 38 exact checks passing. The manifest records the
dirty working tree, pinned inputs, runtime, software and output hashes. None of the checks
uses a numerical range scan as a universal proof. Equations (12), (17), and the Schur bound
provide the explicit uniform arguments under their stated assumptions.

The next decisive calculation is to carry the corrected `J_Y(0)=1.2` into the same-action
cosmological system and test (18) on the resulting finite clock accelerations. A boosted
environment-dependent PPN calculation and a high-frequency emission/cutoff calculation
remain separate obligations. No full-theory closure is claimed.
