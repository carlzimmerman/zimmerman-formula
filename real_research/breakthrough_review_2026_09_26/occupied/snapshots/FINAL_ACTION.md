# CA4-GNC — the final CD26-4 common-action candidate

**Frozen candidate, not completed theory.** This is one explicit action
joining the filtered gravity host, a geometric convex gate with a fixed
compensator, and the transport lane's five real classical fields. It repairs
three concrete defects: a compact zero-mode contradiction, a mismatched
carrier subtraction source, and the old finite-alpha frozen scalar crossing.
It intentionally changes the off-branch force and the globally ungated MOND
equations. Full coupled global evolution, exact target phenomenology, PPN,
and the full constraint count remain unproved. A separate canonical two-cell
control also defeats an automatic reduced-kinetic-positivity claim for the
exponential carrier at large amplitude; see section 8 and the separately
defined perspective variant. No old empirical pass is
assigned to this action.

Assigned base: `ecffd2af3623ff3e32318234fd51e1fac50b9126`, plus prior dirty
work. Earlier attempts are preserved in `ACTION_REPORT.md` (unprojected
bridge) and `MAIN_ACTION.md` (CA4-PN weighted gate). The latter has a new
transition lapse bound, which motivates the present compensated variant.
There are no further unstated gate versions in this definition.

## 1. Fields, operators, potential, and endpoints

Use `c=1`, signature `-+++`, `M_P^2=(8pi G_bare)^(-1)>0`. Declare
`0<alpha<2`, `c_N=1-alpha/2>0`, `c2>0`, `xi>0`, `0<ell<4`,
`theta>0`, `delta>0` and constant `Lambda`. Their values are inputs.

The independent physical metric is `g`. Ordinary matter and photons
couple only through `S_b[g]`. A varied clock `tau`, with
`X_tau=-g^{mu nu}tau_mu tau_nu>0`, defines

\[
 n_\mu=-\tau_\mu/\sqrt{X_\tau},\quad N=X_\tau^{-1/2},\quad
 h_{\mu\nu}=g_{\mu\nu}+n_\mu n_\nu,
\]
\[
 a_\mu=n^\nu\nabla_\nu n_\mu=D_\mu\ln N,
 \quad K_{\mu\nu}=h_\mu{}^\rho h_\nu{}^\sigma\nabla_\rho n_\sigma,
 \quad K=h^{\mu\nu}K_{\mu\nu}.
\]

Leaves are compact, connected, closed and spacelike. All scalar products
below use `h` on a leaf. Define the varied intrinsic mean

\[
 \langle A\rangle_h=\frac{\int_{\Sigma_\tau}\sqrt h A}{\int_{\Sigma_\tau}\sqrt h},
 \quad z=Z-\langle Z\rangle_h,\quad Q_K=K-\langle K\rangle_h.
\]

`Z,U` are independent scalar auxiliaries. The mean is **not lapse-weighted**.
`Z -> Z+c(tau)` is an exact redundancy, and its mean can be fixed as a
normalization rather than inverted by a Poisson solver.

The five real carrier fields are `phi1,phi2,chi1,chi2,s`. Let
`phi=(phi1,phi2)`, `chi=(chi1,chi2)` and choose the transport interaction

\[
 \boxed{V=\tfrac12m_H^2|\phi|^2
 +\tfrac12m_L^2|\chi+\gamma s\phi|^2+\tfrac12\mu^2s^2,}
 \quad m_H,m_L>0,\quad\mu^2\ge0,\quad\gamma\in\mathbb R. \tag{1}
\]

Equivalently `Psi=(phi1+i phi2)/sqrt(2)` and
`Chi=(chi1+i chi2)/sqrt(2)`. This is exactly the positive-square potential
in `transport/CONVERSION.md`, with its canonical normalization. It is
nonnegative and includes the compulsory quartic interaction. The optional
strict `mu>0` branch is distinguished from the massless slow-wave witness;
no numerical witness or cosmological abundance is silently fixed here.

For these five fields collectively denoted `varphi_A`, define

\[
 K_d=\tfrac12\sum_A(n\cdot\partial\varphi_A)^2,\quad
 W_d=\tfrac12\sum_A|D\varphi_A|^2+V,
\]
\[
 {\cal L}_d=e^zK_d-e^{-z}W_d,\quad
 \rho_d=e^zK_d+e^{-z}W_d=\partial_z{\cal L}_d. \tag{2}
\]

The density identity follows also from the fixed-h lapse variation. The
carrier uses the composite lapse `N_d=N exp(-z)`, not a second independent
metric. Its coupling is nonminimal and not universal: the composite
characteristic metric is `g_d=g+(1-exp(-2z))n n`. Baryons and photons use
the single physical metric `g`.

The heat generator is the actual intrinsic Laplacian

\[
 \Delta_hF=\operatorname{div}_hDF
 =h^{\mu\nu}\nabla_\mu\nabla_\nu F+K n^\mu\partial_\mu F,
 \qquad S_h=e^{b\Delta_h},\quad b=\xi^2/2.
\]

Introduce independent scalar heat fields `W(r,x),L(r,x)` for `0<=r<=b`
and multiplier `lambda0(x)`. This auxiliary coordinate is not physical
time. Let

\[
 J(p)=2a_0^2q(|p|^2/a_0^2),\quad q(0)=0,\quad
 q'(y^2)=\nu_{\rm mono}(y)-1,
\]
\[
 Y_h=J(DW_b)+\ell\Delta_hW_b-\theta,\quad f=G'(Y_h). \tag{3}
\]

`nu_mono` is the actual XC4 derivative-floor construction, joining RAR at
`y_star≈2.3374`; its zero-field and splice regularity are not replaced by
an unannounced smooth kernel. `J_p=4(nu_mono−1)p`; its regular nonzero
Hessian eigenvalues are `4 C_T,4 C_L`.

`G` is the specified C4 convex polynomial ramp. Put `r=Y/delta`:
`G(Y)=0` for `Y<=0`,
`G(Y)=delta(7r^5-14r^6+10r^7-(5/2)r^8)` for `0<Y<delta`,
and `G(Y)=Y-delta/2` for `Y>=delta`. In the transition,
`G'=35r^4-84r^5+70r^6-20r^7` and
`G''=140r^3(1-r)^3/delta`, so `0<=G'<=1` and
`0<=G''<=35/(16delta)`. This matches the assembly/evolution ramp controls;
the initially drafted infinitely smooth bump is not the frozen definition.
`ell` is dimensionless in these units;
`J,theta,delta` have dimension length^-2. The a0–vacuum relation remains
an optional input, not a consequence of this action.

## 2. The complete action

\[
\boxed{\begin{split}
S_{\rm GNC}={M_P^2\over2}\int d^4x\sqrt{-g}\Big\{
&R^{(4)}-2\Lambda+\alpha|a-DZ|^2-c_2Q_K^2
 +4a\cdot DZ-2|DZ|^2-4c_N DZ\cdot DU\\
&+c_N[ G(Y_h)+\ell a\cdot DW_b]\\
&+c_N\int_0^bdr\,L(r,x)[\partial_rW(r,x)-\Delta_hW(r,x)]
 +c_N\lambda_0[W(0,x)-U(x)]\Big\}\\
&+\int d^4x\sqrt{-g}[e^zK_d-e^{-z}W_d]+S_b[g]+S_{\rm GHY}.
\end{split}} \tag{4}
\]

There is no undefined extra auxiliary density. All displayed fields are
varied. Use the standard Einstein cap terms
`S_GHY=M_P^2 sum_caps integral sqrt(|gamma|) epsilon K_out`, where
`epsilon=-1` on spacelike caps. With the future-directed convention for
`n`, the final cap contributes `-M_P^2 integral sqrt(h) K`, the initial cap
the opposite sign. These convert the Einstein bulk to
`R3+Kij Kij-K^2` under the stated convention. Fix the induced cap metric
and clock jets, or use variations supported away from caps; carrier
endpoints have their standard fixed-field prescription. Heat endpoints
are varied, as in section 3. There are no spatial boundary terms.

The fixed compensator `+c_N ell a dot DW_b` is present globally, including
the inactive branch. It is not multiplied by `f`. Multiplying it by `f`
would define another action and alter the analysis below. Replacing
`Q_K^2` by `K^2` is likewise a separate, explicitly compared variant.

## 3. Derived heat, U, Z, carrier and mean equations

Write `div_N v=N^-1 D_i(Nv^i)`, `Delta_N=div_N D`, and
`S_N^dagger=N^-1 S_h N`. The actual first variation with respect to `W_b` is

\[
 R_W=-\operatorname{div}_N(fJ_p+\ell a)
             +\ell N^{-1}\Delta_h(Nf). \tag{5}
\]

This includes measure terms. Equivalently
`R_W=-div_N(fJ_p)+ell(f-1)div_N a+2ell a dot Df+ell Delta_h f`.
The heat equations and endpoints are

\[
 \partial_rW=\Delta_hW,\quad W_0=U,\quad
 \partial_rL=-N^{-1}\Delta_h(NL),\quad L_b=-R_W,\quad\lambda_0=L_0.
\]

The independent auxiliary equations are

\[
 \boxed{4\Delta_N Z=S_N^\dagger[
 \operatorname{div}_N(fJ_p+\ell a)-\ell N^{-1}\Delta_h(Nf)],} \tag{6}
\]
\[
 \boxed{2M_P^2c_N\operatorname{div}_N(DZ-a+DU)
       +\rho_d-\langle N\rho_d\rangle_h/N=0.} \tag{7}
\]

The source in (7) has exactly zero `N sqrt(h)` integral. Without the
action-level projection it would be `rho_d`, incorrectly forcing a
positive homogeneous carrier to vanish on every closed leaf.

For `A=e^z`, `B=e^-z`, set
`C_d^{mu nu}=B h^{mu nu}-A n^mu n^nu`. The five carrier equations are

\[
 \nabla_\mu(C_d^{\mu\nu}\partial_\nu\phi_a)
 -B[m_H^2\phi_a+\gamma m_L^2s(\chi_a+\gamma s\phi_a)]=0,
\]
\[
 \nabla_\mu(C_d^{\mu\nu}\partial_\nu\chi_a)
 -Bm_L^2(\chi_a+\gamma s\phi_a)=0\quad(a=1,2),
\]
\[
 \nabla_\mu(C_d^{\mu\nu}\partial_\nu s)
 -B[\mu^2s+\gamma m_L^2\phi\cdot(\chi+\gamma s\phi)]=0. \tag{8}
\]

The diagonal U(1) current is conserved. Its component currents have
opposite exchange `B gamma m_L^2 s(phi1 chi2−phi2 chi1)`, so conversion
does not delete total charge. In a fixed flat leaf chart the exact energy
exchange is `partial_t rho_d+div F_d=-zdot rho_d`, with
`F_d=-B sum_A dotvarphi_A Dvarphi_A`. The same action supplies the opposite
exchange through its projected host; a changing gate is not an external
unrecorded energy source.

The physical fixed-h lapse density remains `rho_d`, but the projector
adds the spatial stress

\[
 \Delta T^{ij}_{\rm mean}=-[\langle N\rho_d\rangle_h/N]z h^{ij},
 \qquad\delta_h\langle Z\rangle_h=\tfrac12\langle z h^{ij}\delta h_{ij}\rangle_h.
 \tag{9}
\]

At fixed `g,Z`, let `B_Z=n(Z)+Kz`. Then
`d<Z>_h/dtau=<N B_Z>_h` and

\[
 \delta_\tau z=\langle N\delta\tau B_Z\rangle_h
                   -\delta\tau\langle N B_Z\rangle_h,
\]
\[
 E_{\tau,\rm mean}=\langle N\rho_d\rangle_h B_Z
                          -\rho_d\langle N B_Z\rangle_h. \tag{10}
\]

These supplement the local `n,h` variation of the carrier. For the `K`
mean also include the explicit `delta K` and leaf deformation. The clock
variation uses `delta_tau n_mu=-h_mu^nu partial_nu(delta tau)/sqrt(X_tau)`
and varies `h,a,K,Delta_h` and both means. The filter variation is

\[
 \delta S_h=\int_0^b e^{(b-r)\Delta_h}(\delta\Delta_h)e^{r\Delta_h}dr.
 \tag{11}
\]

These are required terms in `delta S/delta tau=0` and the spatial metric
equation. Neither is replaced by a frozen heat kernel or frozen mean.

## 4. Exact lapse constraint and canonical trace terms

Unlike the weighted CA4-PN argument, `Y_h` is lapse-independent at fixed
`h,U`. Including the measure and compensator gives

\[
 \delta_{\ln N}\int N\sqrt h[G(Y_h)+\ell a\cdot DW_b]
 =\int N\sqrt h\delta\ln N[G(Y_h)-\ell\Delta_hW_b]. \tag{12}
\]

Put `T_K=Kij Kij-K^2`, `A_K=<N Q_K>_h` and
`V_a=alpha|a-DZ|^2+4a dot DZ-2|DZ|^2-4c_N DZ dot DU`. The exact unitary
fixed-h lapse equation after imposing heat constraints is

\[
\begin{split}
{M_P^2\over2}\{&R^{(3)}-T_K-2\Lambda
 +c_2[-Q_K^2+2KQ_K-2KA_K/N]\\
&+V_a-\operatorname{div}_N[2\alpha(a-DZ)+4DZ]
 +c_N[G(Y_h)-\ell\Delta_hW_b]\}=\rho_b+\rho_d. \tag{13}
\end{split}
\]

The metric momentum and spatial constraint are

\[
 \pi^{ij}={M_P^2\sqrt h\over2}
 [K^{ij}-Kh^{ij}-c_2(Q_K-A_K/N)h^{ij}],
\]
\[
 -2D_j\pi^j{}_i+\sum_A\pi_A D_i\varphi_A
                      +({\rm ordinary\ matter\ momentum})_i=0,
 \quad\pi_A=\sqrt h e^z n(\varphi_A). \tag{14}
\]

The mean terms follow from actual variation; both were checked with
independent two-cell exact algebra. The spatial metric equation includes
(9), (11), all gradient contractions and the centered-trace mean
variation. Its full reduced symbol/constraint preservation has not been
completed. The displayed equations and action specify that remaining
calculation without asserting it has already been solved.

Ordinary matter's separate covariant conservation follows from `S_b[g]`;
neither the gate nor the carrier couples directly to baryon fields.
The carrier stress alone exchanges with the host. General covariance of
the whole varied action supplies the full Ward identity, but does not
constitute a global mixed Cauchy theorem.

## 5. Newton normalization, reciprocal forces, and the known target change

In the inactive or formal constant-gate leading weak-field expansion,
independent static potentials satisfy
`ds^2=-(1+2Phi)dt^2+(1-2Psi)dx^2`. Before eliminating either, the Einstein
part is `2|D Psi|^2−4 D Phi dot D Psi`; thus the leading spatial metric
equation gives `Delta(Psi−Phi)=0`, with the stated nonzero-mode/boundary
normalization. This ordering does not establish no slip for arbitrary
transition jets or derivative scalings. The full metric equation retains
filter, projector and gate stress, and its general no-slip limit is open.

With the compensated gate displayed separately, the remaining base
quadratic density in units `M_P^2/2` is

\[
 -2c_N|D(\Phi-Z)|^2-4c_N DZ\cdot DU.
\]

The locally measured high-wavenumber Newton constant is therefore
`G_N=G_bare/c_N`. This is derived, not identified with the bare coupling.
The old choice `alpha a^2` without the normalization change instead leaves
`Delta(U-alpha Phi/2)=rho_b/(2M_P^2)` and leaks the carrier through the
kernel argument.

For a **formal constant gate** and one Fourier mode, set
`S_k=exp(-xi^2 k^2/2)`,

\[
 Q=1-(1-f)\ell S_k/4,\qquad D=1+f C S_k^2.
\]

If `u_b,u_d` are Newtonian source potentials computed with `G_N`, direct
variation gives

\[
 U=u_b/Q,\quad\Phi=D u_b/Q^2+u_d/Q,\quad
 \Phi-z=u_b/Q+u_d. \tag{15}
\]

The two cross responses are equal. On the physically allowed homogeneous
inactive branch the perturbative `f=0` matrix is

\[
 -{4\pi G_N\over k^2}
 \begin{pmatrix}Q^{-2}&Q^{-1}\\Q^{-1}&1\end{pmatrix},\quad
 Q=1-\ell S_k/4. \tag{16}
\]

Hence the compensator changes inactive long-wavelength baryon gravity
and cross-species response. For `ell=.04` solely as an illustration, the
long-wave factors are `1.02030405` and `1.01010101`. No claim is made that
this parameter satisfies cosmological or local data. At high `k`, heat
suppression gives `Q->1` and restores the local Newton normalization.

For a formal full-on operator `f=1`,

\[
 G(Y_h)+\ell a\cdot DW_b
 =J(DW_b)-\theta-\delta/2+\ell\Delta_NW_b.
\]

The last term is an exact leaf divergence under `N sqrt(h)`, so the bulk
variation is the original `J` variation with a constant vacuum-shaped
offset. That offset is not discarded. On local plateau patches the
boundary/interface terms must be retained.

**A global full-on state is impossible on the declared compact leaf with
theta>0.** At a maximum of smooth `W_b`, `DW_b=0`, `Delta_h W_b<=0`, and
`Y_h<=-theta`. Consequently the full-on identities are formal or local
frozen-coefficient identities, not a homogeneous cosmological background.
Moreover the heat kernel connects every region of a connected compact
leaf: a local `f=1` patch does not reproduce the exact globally ungated
filtered equation. Interface and off-region terms remain in the outer
filter. The action **modifies the exact global target**, rather than merely
leaving its verification unfinished. Controlled approximate matching
would require quantitative interface/heat-tail bounds and fresh data tests.

The L361 regional screening mechanism is absent. No old KiDS, DE1–DE4,
forest or transport-kick pass is transferred to (4).

## 6. What is proved about convexity and the frozen scalar block

At fixed positive `N,h`, `G(J(D S_h U)+ell Delta_h S_h U-theta)` is convex
in `U`, since `J` is convex and `Delta_h S_h U` is affine. The fixed
compensator is linear in `U` and leaves this Hessian unchanged. Including
`2|DU-a|^2` gives strong convexity modulo constant `U`. The actual
zero-field singular tangent is treated by convexity, not by pretending
`J` is twice differentiable there.

On a local/formal carrier-free plateau, the normalized host gives

\[
 L_{2,\rm red}=\frac{2(2+3c_2)}{c_2}\dot\psi^2
       -\frac{2(2-\alpha)}{2C+\alpha}k^2\psi^2,
\quad c_s^2=\frac{c_2(2-\alpha)}{(2+3c_2)(2C+\alpha)}. \tag{17}
\]

Both the independent four-row determinant and constrained quadratic
substitution verify this result. The original unnormalized host's
`2-alpha(1+C)` numerator crossing is absent. Finite `C>=0`, `0<alpha<2`
and `c2>0` give positive kinetic and restoring-gradient coefficients.

In the compensated gate's frozen principal calculation, the evolution
lane derives

\[
 Q=1-(1-f)\ell S_k/4,\quad
 D=1+f C S_k^2+\frac{G''}{4}S_k^2[(J')^2+\ell^2k^2],
\]
\[
 \alpha_{\rm eff}=2-(2-\alpha)Q^2/D.
\]

Thus `1-ell/4<=Q<=1`, `D>=1`, and
`alpha<=alpha_eff<2` for finite `D`. The scalar principal speed is
`c2(2-alpha_eff)/[(2+3c2)alpha_eff]>0`. Our computation independently
checks these algebraic reductions and the plateau limit; the full
background principal derivation and its limitations are recorded in the
evolution lane. Lower-order lapse-measure, curved metric, projector and
clock terms remain outside this frozen result.

This avoids CA4-PN's unfiltered transition increment
`(c_N/2)G'' ell^2|DW|^2` to the lapse-gradient coefficient. Finite operator
bounds near transverse active zeros are useful local evolution estimates;
neither finite-point positivity nor a fixed-lapse Hessian proves global
coupled gravity regularity.

On the homogeneous inactive branch the tensor principal action is
Einstein's `M_P^2 a^3[hdot_ij^2-a^-2(Dh_ij)^2]/8`, with speed one. The
five carrier velocity coefficients are `exp(z)>0`, with characteristic
speed `exp(-z)` relative to the foliation. Uniform estimates still require
bounds on `z` and geometry. The provisional content is two tensor modes,
the explicitly visible host clock scalar, and five real carrier pairs;
the complete Dirac analysis can neither be replaced by this provisional
count nor assumed to remove a scalar.

## 7. Homogeneous cosmology and transport scope

On a homogeneous FRW leaf, `W_b` is constant, `Y_h=-theta<0`, `f=G=0`,
`a=DU=DZ=0`, `z=0`, and `Q_K=0`. Equation (7) has zero projected source
even when `rho_d>0`. The compensator vanishes. Every first variation of
`-c2 Q_K^2` vanishes because `Q_K=0`, including the mean and lapse
variations, not merely substitution into its value.

The same action therefore admits

\[
 3M_P^2H^2=M_P^2\Lambda+\rho_b+\rho_d,\quad
 -2M_P^2\dot H=\rho_b+P_b+\rho_d+P_d,
 \quad G_{\rm cosm}/G_N=c_N. \tag{18}
\]

The carrier obeys its canonical homogeneous five-field equations and its
total conserved diagonal charge. A positive right side admits an
expanding branch. Its initial charge, energy and field composition remain
initial data, not derived abundance.

The different uncentered variant `-c2 K^2` would instead give
`3M_P^2(1+3c2/2)H^2=M_P^2Lambda+rho` and
`G_cosm/G_N=c_N/(1+3c2/2)`. The mean-subtracted trace is an explicit action
choice; its additional terms are already included in (13)–(14).

The transport lane proves conversion and a global energy-space result on
its stated fixed-background field system, and demonstrates outgoing
packets with a complete charge/energy ledger. Those statements support
the potential and equations (1), (8); they do not prove the same estimates
for the coupled projected gravity action, derive a cosmological clearing
rate, or establish the old halo-kick prescription.

## 8. Evidence and acceptance scope

The action lane has three independent preserved runs:

- `run1/`: 46 checks of the bridge, exponential source identity, reciprocity,
  density-gate negative control and heat derivative.
- `revised_run1/`: 28 checks of the Newton-normalized scalar action,
  independent static potentials, compact projection and weighted-gate
  variation.
- `compensated_run1/`: 24 checks of the final compensator variations,
  reciprocal static response, frozen Schur algebra and centered-trace
  lapse/momentum terms.

The final action combines only the explicitly translated terms above.
Passing these 98 checks does not establish its full nonlinear equations'
global health. The canonical projected Z constraint is strongly convex at
fixed canonical carrier data, but that does not make its joint momentum
Hessian positive. The evolution lane exhibits an exact two-cell exponential
control with reduced momentum Hessian exp(-z)(1-z)/(1+z), negative for z>1.
It disproves that automatic inference, without claiming to construct a
full gravitational background. `PERSPECTIVE_VARIANT.md` defines a different
carrier coupling with a jointly convex canonical block and a changed exact
subtraction source. Its results are not assigned to equation (4). The final known distinctions are:

| Requirement or bridge | Status for CA4-GNC |
|---|---|
| One explicit common action and exact field source/transport equations | Defined and varied at the displayed scope |
| Ordinary-matter minimal coupling and its separate Ward identity | Preserved |
| Compact homogeneous carrier and expanding branch | Admitted; not an abundance/cosmology fit |
| Measured high-k Newton constant and reciprocal static forces | Derived |
| Original global filtered MOND equation | Modified by gate/interfaces; not an exact pass |
| Regional-screening and previous empirical gates | Not inherited |
| Fixed-lapse auxiliary strong convexity | Established on the declared leaf domain |
| Frozen principal scalar/tensor/carrier signs | Positive under stated hypotheses; not full background health |
| Full constraints, global time preservation and coupled evolution | Open |
| PPN, general no slip, GW sector on arbitrary backgrounds, data fits | Open |

`EVIDENCE.md` and `source_provenance.json` pin the actual sources, runs and
scope. The bare scale relation, ramp thresholds and carrier parameters are
not described as first-principles predictions.
