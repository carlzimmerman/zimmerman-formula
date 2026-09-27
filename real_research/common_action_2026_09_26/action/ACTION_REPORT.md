# CD26-4: an explicit common-action trial and its first exact obstructions

**Superseded bridge trial.** Use `MAIN_ACTION.md` for the main CA4-PN
candidate. This earlier unprojected trial has a compact zero-mode
contradiction: integrating its Z equation forbids positive carrier energy.
Also, its unchanged `alpha a^2` term makes the exact leading source relation
`Delta(U-alpha Phi/2)=rho_b/(2M^2)`, rather than the alpha-free relation
written in its static discussion below. Those earlier static formulas
apply only when the alpha correction is omitted at the stated order.
The revised action explicitly repairs both defects and uses a changed
convex gate. This file is retained as the derivation and failure record,
not as an alternative completed model.

Starting revision `ecffd2af3623ff3e32318234fd51e1fac50b9126`, plus the existing
working tree. This route changes only its new `action/` directory.

**Result.** L361 admits an exact nonrelativistic rewrite in the physical
baryon potential. That rewrite forces a nonminimal coupling of the carrier.
An exponential completion repairs the linear coupling's finite-amplitude
kinetic signs and makes the carrier's actual lapse density equal its
subtraction source. Below is one explicit covariant action with all gate
and heat auxiliaries specified. It retains ordinary-matter minimal coupling
and the fixed-gate Newtonian/filtered-MOND limit. It is a new trial action,
not a full-health or empirical certificate: the active plateau reduces to
the C-H/K host, and a dynamical gate changes its constraint and principal
operators. The existing finite-alpha host obstruction remains applicable
where that reduction is valid.

## 1. The least expensive compatibility test: which potential is physical?

L361 uses Newtonian `phi`, regional potentials `psi,w,chi`, and a prescribed
mask `f`. Its source terms are

\[
 - (\rho_b+\rho_d)\phi-f\rho_b(\psi-\chi).
\]

Define `P=psi-chi`, `Z=fP`, and the **physical baryon potential** `Phi=phi+Z`.
The exact change of variables is

\[
 -(\rho_b+\rho_d)\phi-f\rho_bP
 =-\rho_b\Phi-\rho_d\Phi+Z\rho_d,\quad
 -|D\phi|^2=-|D\Phi|^2+2D\Phi\cdot DZ-|DZ|^2. \tag{1}
\]

Thus minimally coupling baryons to a metric whose lapse is `phi`, while
retaining their extra `fP` force, would fail the separate ordinary-matter
conservation requirement. The rewrite identifies the metric lapse with
`Phi`. A carrier which is invisible to the MOND kernel then has an explicit
nonminimal interaction. One cannot simultaneously let it source only the
Newtonian field and feel the full baryonic MOND force in this static
variational construction.

For a constant gate and one Fourier mode, let `g=(8pi G)^(-1)`,
`A_k=k^2+mu^2`, `mu^2=m^2(1-f)`, and `s_k=exp(-b k^2)`. Linearize the
phantom primitive as `q=C|D S w|^2/a0^2`. Directly varying the four
potentials gives the source response

\[
 \binom{\Phi_b}{\Phi_d}=
 -\frac1{2g}
 \begin{pmatrix}
 k^{-2}+f^2(Cf s_k^2k^2-\mu^2)/A_k^2 & k^{-2}\\
 k^{-2}&k^{-2}
 \end{pmatrix}\binom{\rho_b}{\rho_d}. \tag{2}
\]

The cross responses are equal. At `f=1,mu=0`, the baryonic self-response is
`-(1+C s_k^2)/(2g k^2)` and the carrier self/cross responses are Newtonian.
The equality follows both from the field equations and the symmetric
Hessian of the on-shell source action. It is verified without assigning
the carrier force independently. An environmental gate depending on source
density changes the on-shell Hessian; omitting that derivative can falsely
produce an asymmetric force law.

## 2. A constructive carrier completion

For real classical carrier fields `varphi_A`, let

\[
 K_d=\tfrac12\sum_A(n^\mu\partial_\mu\varphi_A)^2,\quad
 W_d=\tfrac12\sum_A|D\varphi_A|^2+V(\varphi),\quad V\ge0.
\]

A Cartesian pair permits the U(1) clock/charge field already constructed
in CD26-2, with no phase-coordinate singularity at amplitude zero. An
additional trigger field, if used, is another counted field; no abundance
or particle population is imposed by the action.

The literal first-order lift of (1), `L0+Z rho0`, gives

\[
 {\cal L}_{d,\rm lin}=(1+Z)K_d-(1-Z)W_d.
\]

At fixed `Z`, its strict kinetic/gradient condition is `|Z|<1`. Its
subtraction source is `partial L/partial Z=rho0=K_d+W_d`, whereas its actual
lapse density is `(1+Z)K_d+(1-Z)W_d`. Their difference is `Z L0`.
Consequently replacing a prescribed pressureless source by a dynamical
relativistic field is not an exact unchanged substitution.

Use instead the explicit completion

\[
 \boxed{{\cal L}_d=e^ZK_d-e^{-Z}W_d,\qquad
 \rho_d=e^ZK_d+e^{-Z}W_d
       =\left.\frac{\partial{\cal L}_d}{\partial Z}\right|_{g,n,\varphi}.} \tag{3}
\]

The density equality follows independently by varying `N Ld` at fixed
`Z,h,shift,varphi_dot`. It is exact, and the action agrees with the required
linear source coupling through first order in `Z`. In ADM coordinates it
is canonical matter with the **composite** lapse `N_d=N exp(-Z)` and the
same spatial metric and shift. Equivalently the composite characteristic
metric is `g_d=g+(1-exp(-2Z)) n n`. There is no independent second metric,
but the carrier is explicitly **not minimally coupled to the ordinary
physical metric**. Baryons and photons remain minimally coupled to `g`.

The carrier principal coefficients are `A=e^Z>0`, `B=e^-Z>0`; its speed
relative to the preferred frame is `c_d^2=B/A=e^-2Z`. Every finite `Z` has
a future cone compatible with that foliation. Uniform hyperbolicity and
energy estimates require a bound on `|Z|`; positivity alone does not
propagate such a bound. Superluminal values are not themselves a failure
of the active criterion B. They do not establish the mixed Cauchy theorem.

## 3. One fully specified covariant trial action

Use `c=1`, signature `-+++`, and `M^2=(8pi G)^(-1)>0`, with bare `G`.
The varied preferred clock `tau` defines

\[
 X=-g^{\mu\nu}\tau_\mu\tau_\nu>0,\quad
 n_\mu=-\tau_\mu/\sqrt X,\quad h_{\mu\nu}=g_{\mu\nu}+n_\mu n_\nu,
 \quad a_\mu=n^\nu\nabla_\nu n_\mu,
\]

and `D`, `Kij`, `K`, and `sigmaij=Kij-hij K/3` are the intrinsic derivative,
extrinsic curvature, trace and shear. Define
`Delta_h=div_h D=h^{mu nu}nabla_mu nabla_nu+K n^mu partial_mu` on a smooth,
compact connected closed leaf. The inclusion of `K n(partial)` is essential.
Take `S=exp(b Delta_h)`, `b=xi^2/2>0`; its constant mode has gain one.

All scalar fields `Z,f,psi,w,chi,eta,lambda` are independent before variation;
`eta,lambda` are multipliers. Let `mu^2=m^2(1-f)` and `P=psi-chi`. The heat
fields `W(z,x),L(z,x),lambda0(x)` have `0<=z<=b`, with the local density

\[
 {\cal H}_{\rm heat}=\int_0^b dz\,L(\partial_zW-\Delta_hW)
       +\lambda_0(W_0-w).
\]

Use the actual XC4 monotone primitive

\[
 q'(s^2)=\nu_{\rm mono}(s)-1,\quad q(0)=0,\quad
 q(s^2)=2\int_0^s h_{\rm mono}(t)dt.
\]

Here the derivative floor joins `h_RAR` at `y_star≈2.3374`, before its
maximum, not at the old approximate peak description. The primitive has
the zero-gradient and splice regularity documented in XC4/XC5; no smooth
regularization is inserted silently.

The trial is

\[
\begin{split}
S={}&\int\sqrt{-g}\,\Big\{
 \frac{M^2}{2}[R^{(4)}-2\Lambda+\alpha_c a^2-c_2K^2]
 +{\cal L}_d+\eta[Z-f(\psi-\chi)]+\lambda[f-F(I)]\\
&+M^2[2a\cdot DZ-|DZ|^2-2D\psi\cdot Dw-2\mu^2\psi w
 +|Dw|^2+a_0^2 f q(|DW_b|^2/a_0^2)
 +|D\chi|^2+\mu^2\chi^2+{\cal H}_{\rm heat}]
\Big\}+S_b[g]+S_{\rm GHY}. \tag{4}
\end{split}
\]

`S_b` includes minimally coupled ordinary matter and photons. The standard
Einstein GHY terms are imposed on the initial/final caps; use interior
variations or fix the metric and clock jets there. Heat endpoints are
varied, not assigned independent data. There is no spatial boundary.
The action is fundamental and spatially nonlocal at leaf level; no hidden
frequency cutoff has been imposed.

For an explicit globally defined gate choose the previously audited smooth
step `F(t)=g(t)/(g(t)+g(1-t))`, where `g(t)=exp(-1/t)` for `t>0` and zero
otherwise, with

\[
 I=\frac{27\Lambda[R^{(3)}+\sigma^2]}
         {8x_c(K^4+\epsilon\Lambda^2)},\qquad
 \Lambda,\epsilon,x_c>0. \tag{5}
\]

This is smooth for all finite curvature and trace, `0<=f<=1`, and has
exact plateaus. The regulator and transition width are declared choices.
It changes the historical hard threshold near `K=0` and throughout its
transition; the DE1–DE4 empirical gates cannot be imported unchanged.
`m,xi,a0,epsilon,xc,alpha_c,c2,Lambda` are action inputs, not derived here.
The possible `a0–Lambda` relation and measured-versus-bare Newton coupling
remain separate tests.

The **fixed-gate comparison** removes `lambda[f-F(I)]` and holds `f(x)`
prescribed. It is not the autonomous completed theory: an inhomogeneous
external mask supplies momentum/stress exchange. Both variants use the
same remaining terms in (4).

## 4. Actual variations and the terms a frozen gate omits

Let `div_N v=N^-1 D_i(N v^i)` in adapted coordinates. The heat endpoints
and adjoint are

\[
 \partial_zW=\Delta_hW,\quad W_0=w,\quad
 \partial_zL=-N^{-1}\Delta_h(NL),\quad
 L_b=2\operatorname{div}_N[f q' DW_b],\quad\lambda_0=L_0,
\]

so `W_b=S w` and `S_N^dagger=N^-1 S N`. The outer filter is this weighted
adjoint, not generally `S`. With
`j=f q'(|DW_b|^2/a0^2) DW_b`, the independent regional equations are

\[
\begin{aligned}
2M^2\operatorname{div}_N(DZ-a)+\rho_d+\eta&=0,\\
2M^2(\Delta_N-\mu^2)w-f\eta&=0,\\
-2M^2(\Delta_N-\mu^2)\chi+f\eta&=0,\\
(\Delta_N-\mu^2)\psi-\Delta_Nw-S_N^\dagger\operatorname{div}_Nj&=0,\\
Z-f(\psi-\chi)&=0,\qquad f-F(I)=0. \tag{6}
\end{aligned}
\]

Here `Delta_N=div_N D` occurs in action Euler equations, while the heat
constraint itself still uses **geometric** `Delta_h`. These operators must
not be interchanged. On an invertible leaf branch the second and third
equations imply `chi=w`; on a pure zero-mass leaf their constant difference
requires a zero-mode normalization rather than a fictitious Poisson inverse.

Varying `f` gives

\[
 \lambda=-B_f,\quad
 B_f=M^2[2m^2\psi w+a_0^2q(|DW_b|^2/a_0^2)-m^2\chi^2]
       -\eta(\psi-\chi). \tag{7}
\]

Therefore the metric/clock variation from the gate, after its multiplier
equations, contains **`B_f delta F(I)`**. It does not vanish because a
mask happens to solve a prescribed switching formula. For the geometry
(5), putting `D0=K^4+epsilon Lambda^2` and `Rcal=R3+sigma^2`,

\[
 \delta F=F'(I)\left[
 \frac{27\Lambda}{8x_cD_0}\delta\mathcal R
 -\frac{4IK^3}{D_0}\delta K\right]. \tag{8}
\]

All measure, inverse-metric, shear-contraction, and clock-normal variations
in these scalars are retained. The quadratic action also includes
`delta B_f delta F` and `B_f delta^2 F`, not just the first variation.
For an isotropic tensor perturbation, the shear in `Rcal` is quadratic and
cannot be dropped by observing that the first-order TT trace vanishes.

The filter's metric/clock contribution is likewise nonzero:

\[
 \delta S=\int_0^b e^{(b-s)\Delta_h}(\delta\Delta_h)e^{s\Delta_h}ds,
\quad
 \delta\tau n_\mu=-h_\mu{}^\nu\partial_\nu\delta\tau/\sqrt X. \tag{9}
\]

Together (6)–(9), the action's independent `g,tau` Euler equations, and the
carrier equation below define the complete trial. Explicitly the metric
equation is `M^2(Gmunu+Lambda gmunu)=T_b+T_d+T_reg+T_gate+T_khr`, with
each non-Einstein tensor obtained by varying its displayed density in (4),
including (8) and (9). The clock equation is the corresponding variation
through `n,h,a,K,Delta_h,I`. **The full reduced metric/clock symbol and
Dirac constraint algebra have not been computed here.** This is an
explicit variational definition, not a claimed solved gravitational system.

At leading static weak-field order, physical `Phi=ln N` and independently
varied spatial potential give `Psi=Phi` by the Einstein spatial equation;
the added terms enter its stress only at higher weak order. The lapse and
`Z` equations then give

\[
 2M^2\Delta(\Phi-Z)=\rho_b+\rho_d,\qquad \eta=\rho_b,
\]

and hence the L361 regional equations, with the **filtered phantom** term
`S div[f (nu_mono−1) DSw]`. Filtering the full `Q` while keeping an
unfiltered Newtonian subtraction would introduce a spurious Newtonian
filter. Equation (4) instead uses `|Dw|^2+a0^2 f q(|DSw|^2/a0^2)` to
preserve the unfiltered Newtonian part. This weak, static identification
does not extend `eta=rho_b` or the no-slip relation to the full relativistic
action; pressure, curvature, filter and gate stresses remain there.

Ordinary matter's equation derives solely from `S_b[g]`, so its separate
covariant conservation follows from its own diffeomorphism identity.
For an external gate, the nonordinary sector has the spurion term
`B_f partial_nu f` in its on-shell Ward identity. A dynamical gate transfers
that exchange into its actual metric/clock equations. If the gate instead
depends directly on baryon density, its variation enters the baryon
equations and this minimal-matter conservation proof no longer applies.

## 5. Carrier transport follows from the same interaction

Writing `A=e^Z`, `B=e^-Z`, define

\[
 C^{\mu\nu}=B h^{\mu\nu}-A n^\mu n^\nu.
\]

Variation of each real field gives

\[
 \nabla_\mu(C^{\mu\nu}\partial_\nu\varphi_A)-B V_{,A}=0. \tag{10}
\]

For a U(1) pair and an invariant potential,
`J^mu=C^{mu nu}(varphi1 partial_nu varphi2−varphi2 partial_nu varphi1)`
is conserved (its overall sign convention is immaterial). In a fixed flat
leaf chart the carrier energy and flux obey

\[
 E_d=\tfrac12A\dot\varphi^2+B(\tfrac12|D\varphi|^2+V),\quad
 {\bf F}_d=-B\sum_A\dot\varphi_A D\varphi_A,
\]
\[
 \partial_t E_d+\operatorname{div}{\bf F}_d=-\dot Z\,\rho_d. \tag{11}
\]

This is exchange with the action's `Z`/constraint/gravity sector, not
disappearance of energy. Since `Z` is constrained in (4), the canonical
independent-gate global ODE theorem developed in the assembly route is a
separate submodel until a common constraint-preserving reduction proves the
same coercive energy. The density identity in (3) supplies its exact source
interface, but does not prove expulsion, free streaming, abundance, or
cosmological transport rates. Charge remains conserved; a density-triggered
potential transition cannot simply delete it.

## 6. Why a dynamical mask can lose health

**Density dependence.** Even the exponential completion loses its simple
positive-kinetic argument if `Z` is composed with a kinetic density. In
declared dimensionless units take

\[
 K=v^2/2,\quad W=0,\quad
 Z(K)=\frac{1}{2[1+(K-1)^2]},\quad L=e^{Z(K)}K.
\]

The gate is smooth and `0<Z<=1/2`. Nevertheless at `K=1`,
`Z_K=0`, `Z_KK=-1`, and

\[
 \boxed{\frac{d^2L}{dv^2}=L_K+2K L_{KK}=-e^{1/2}<0.} \tag{12}
\]

A density scale can restore dimensions; it is an additional declared
choice, not part of the witness's sign. This is a concrete counterexample
to inferring the composed action's health from frozen-gate coefficients.
It is not a no-go for every density gate or constrained completion.

**Geometry dependence.** In unitary gauge `K` contains metric velocities,
and `R3` contains two spatial derivatives. Eliminating the constraints
`f=F(I)`, `Z=fP` inside `|DZ|^2` produces terms proportional to
`-M^2 P^2 F_K^2 |D delta K|^2` and
`-M^2 P^2 F_R^2 |D delta R3|^2`, as well as cross terms. Thus the gate
changes the spatially dependent kinetic operator and raises spatial
derivative order. The first sign alone is not a reduced ghost proof,
because the lapse, shift, and regional potentials remain constrained.
It does prove that a principal symbol computed with `delta f=0` is the
wrong symbol in the transition.

The pure fixed-auxiliary contribution `B_f delta^2 F` also changes tensor
normalization and scalar curvature/trace coefficients, as derived in the
earlier D4/D6 audit. Its positive or negative `k^4` terms must now be judged
by criterion B and well-posedness, not the retired metric speed bound.
One cannot import that smaller frozen-`B_f` sector as the full symbol of
(4), either.

**Independent amplitude and convex perspective.** For a convex radial
primitive `J(p)`, multiplying by an independent activation gives
`E=f J(p)+Vgate(f)`. At `f>0`, its joint Hessian needs

\[
 V_{\rm gate}''\ge\frac1f\nabla J^T(H_J)^{-1}\nabla J.
\]

For deep MOND `J proportional |p|^(3/2)` the right side is `3J/f`.
A fixed bounded gate-potential curvature cannot control unbounded `p`.
In contrast the perspective `A J(p/A)` is jointly convex for `A>0`:
its second variation is
`A^-1(delta p−p delta A/A)^T H_J(p/A)(delta p−p delta A/A)`.
For the deep primitive it equals `J(p)/sqrt(A)`. Suppression therefore
requires `A` large and exact off requires `A=infinity`; it is not the old
finite zero/one switch. For a general kernel it also changes the argument
to `p/A`. This is a constructive changed constitutive route, with a clear
price, rather than an unchanged empirical gate certificate.

## 7. Host reduction and the scope of this construction

On an active plateau `f=1,mu=0`, with carrier absent, eliminate `chi=w`
and write `psi=Z+chi`. The relevant density becomes

\[
 M^2[2a\cdot DZ-|DZ|^2-2DZ\cdot Dw+a_0^2q].
\]

The `Z` equation on the normalized leaf gives `DZ=a-Dw`; substitution
returns `M^2[|Dw-a|^2+a0^2 q]`, exactly the C-H sector plus the displayed
`alpha_c,c2` terms. Thus the evolution lane's finite-alpha C-H/K health
test is a real compatibility test of this plateau, not an unrelated
model. Conversely, adding the exponential carrier or a dynamical gate
does not itself repair any host instability on that carrier-free plateau.
Any filtered-operator gate repair must be reinserted into (4) and varied.

L340's health calculations were frozen-coefficient and on a bounded
nonzero-acceleration scan. XC3 adds static-background foliation/filter
vertices but omits full curved metric mixing. XC4 corrects the splice and
its regularity. XC5 establishes fixed-positive-lapse auxiliary convexity
for the actual monotone kernel, not coupled physical-time well-posedness.
These are inputs and diagnostics; none is a global evolution certificate
for (4).

The next required calculation is therefore the complete reduced
metric/clock/regional/carrier symbol on a nonempty constrained background,
including the transition and zero-field domains, or a changed host/gate
with a coercive constraint-preserving energy. The action here makes that
calculation well-defined and repairs a specific density/source mismatch.
It does not claim the user's common-action/global-health/transport closure.

## Evidence

`check_action.py` and `contract.json` implement conditional exact variations,
reciprocity, the exponential repair, negative controls, convex perspective,
and a ten-node noncommuting heat-variation difference test. The run and its
manifest are retained in `run1/`; source provenance is separate. No old
campaign, halo mock or large simulation is executed. A passing bounded
check is not a full theory certificate.
