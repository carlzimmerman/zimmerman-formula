# FGF-010 independent audit: SD1 scale, vacuum and stability

Worker: actual Astra agent `/root/proof_precision`; execution
`fgf010_audit_001`. This is not a DeepSeek-model execution. No literature
search was used. All seven candidate hashes specified in FGF-010 matched
before review. Exact task/source hashes are recorded in `INPUT_VERIFICATION.json`
and `result.json`. The raw candidate derivation was read and its central
equations reconstructed before reading the coordinator intake or author README.
Those narrative verdicts were not used as premises.

**Primary verdict: proved as written**, for the exact, scoped algebraic
statements normalized below. Worker outcome: `supports_scoped_claim`.
No counterexample was found to the candidate's uniform-static-scale
obstruction, exchange signs, cosh-potential field-sector Schur theorem or
functionally imposed potential-only vacuum obstruction. This does not endorse
the environmental-scale model as the user's literal universal vacuum law.
It is a changed physical hypothesis. Negative controls below refute broader
statements that the candidate itself appropriately does not assert.

## 1. Exact target and dependencies

Let C=4 pi G, tau=K/c² and sigma=J/v_chi². Assume K,J,v_chi,c,G,a_ref>0,
a=a_ref exp(chi), smooth fields where the stated derivatives exist, and
source acceleration −grad phi. For Q or R separately, b(g;a)=F^(-1)(g;a),
W(g;a)=integral_0^g b(s;a)ds, with W(0;a)=0. The potential is
U(chi)=S0[cosh(2chi)−1]/4, S0>0, except in explicitly marked controls.

The action is

    integral { [tau phi_t²/2−W(|grad phi|;a)
                 +sigma chi_t²/2−J|grad chi|²/2−U(chi)]/C
               −rho phi } dt d³x + matter kinetic action.

Claims audited: variation; sector energy/momentum exchange; necessity of
nonuniform scale in a nonuniform field; homogeneous fixed-flux equilibrium;
linear two-field positivity on a nonzero uniform-gradient source-free
equilibrium; static susceptibility and spherical sign; distinct vacuum
identifications; and the separately prescribed H history.

Dependencies are direct: Q/R homogeneity and monotonicity -> identities for
W,T,q -> variation/exchange and uniform-scale obstruction. Additional cosh
potential plus equilibrium -> positive Schur quantity -> field-mode positivity.
An additional functional density identification -> exponential potential ->
zero-field stationary-vacuum obstruction. No numerical grid is a proof leaf
for these claims. Matter stability and relativistic vacuum stress/metric
interpretations are separate unproved physical inputs.

## 2. Fresh variation and constitutive reconstruction

Homogeneity F(cB;ca)=cF(B;a), c>0, gives b(cg;ca)=cb(g;a) and
W(cg;ca)=c²W(g;a). Differentiating yields

    g W_g+a W_a=2W, W_g=b,
    T=−aW_a=gb−2W,
    q=T_g=g b_g−b,
    b_chi=b−g b_g=−q,
    T_chi at fixed g=2T−gq.

For Q and R, F_B>0, F_a>0 and d(F/B)/dB<0 at B,a>0. Implicit
differentiation gives b_a=−F_a/F_B<0, so W_a<0 and T>0 at g>0.
The decreasing F/B gives F_B<F/B=g/B, hence b_g>B/g and q>0.
At g=0, T=0 by the prescribed primitive. This confirms both signs without
assuming the author's conclusion.

Independent variation of chi gives

    sigma chi_tt−J Delta chi+U'=−W_chi=T.

Variation of phi gives

    tau phi_tt−div(mu grad phi)=−C rho, mu=b/g.

The signs match SD1. The units also close: W,U,T have acceleration squared,
J has acceleration squared times length squared, chi is dimensionless, and
division by C converts each field energy numerator to energy density.

## 3. Energy and momentum exchange

With f=mu grad phi, direct differentiation gives

    e_phi=(tau phi_t²/2+W)/C, S_phi=−phi_t f/C,
    e_phi,t+div S_phi
      =phi_t[tau phi_tt−div f]/C+W_chi chi_t/C
      =−rho phi_t−T chi_t/C.

For e_chi=[sigma chi_t²/2+J|grad chi|²/2+U]/C and
S_chi=−J chi_t grad chi/C,

    e_chi,t+div S_chi
      =chi_t[sigma chi_tt−J Delta chi+U']/C=+T chi_t/C.

The exchange cancels exactly; the usual continuity identity for rho phi and
matter kinetic work cancels −rho phi_t. Fixed external sources or nonzero
boundary flux must still be included in a total balance.

For the phi momentum/stress in DP1, the formerly spatially constant-a identity
now has the extra term −W_chi chi_i/C=+T chi_i/C. Direct differentiation of
p_chi,i=−sigma chi_t chi_i/C and the displayed chi stress gives

    partial_t p_chi,i+partial_j T_chi,ji
      =[−sigma chi_tt+J Delta chi−U']chi_i/C=−T chi_i/C.

Thus both exchange signs cancel. These are conservation identities of this
assumed preferred-frame action. They do not prove positive total matter-plus-
gravity energy, a relativistic stress tensor or cosmological conservation.

## 4. Uniform scale: exact obstruction and a minimal witness

For spatially uniform static chi_c, the scale equation reduces pointwise to

    U'(chi_c)=T(g(x),a_ref exp(chi_c)).

Because T_g=q>0 at g>0, two distinct positive g values cannot share the same
right-hand side. No finite J can remove this contradiction: its gradient
term is exactly zero on the proposed uniform configuration. A source chosen
to cancel the varying right-hand side changes the hypothesis.

A simple smooth local witness uses Q, a_ref=1, phi(x)=x+x²/2 on 0<x<1,
chi=0, and rho(x)=b_g(1+x;1)/C>0. The static phi equation is satisfied by
construction, but the candidate U'(0)=0 differs from T(1+x,1)>0 everywhere.
This refutes a claim that the added field can preserve exactly the reference
scale for arbitrary positive source profiles. The witness is a prescribed
local source, not a constructed self-supported matter equilibrium.

The exact necessary condition also extends to a spatially uniform time-
dependent chi(t): sigma chi_tt+U' is spatially constant at each time, so g
must have constant magnitude at that time absent additional spatial forcing.
This does not rule out a homogeneous-field solution or approximate small
backreaction. It strengthens the same restricted model obstruction without
claiming a no-go for other couplings or sectors.

For the literal core law with exactly fixed rho_Lambda and reference
a_ref=kappa c sqrt(G rho_Lambda), the actual a equals a_ref, hence chi=0.
For this cosh potential even a nonzero *constant* g is incompatible with that
specific chi=0 equilibrium, since U'(0)=0<T(g,a_ref). Allowing a different
constant chi at a chosen constant g is a different identification of a_ref.
The manuscript's varying-field obstruction is correct and conservative.

## 5. Homogeneous equilibrium and full field Hessian

At fixed B0>0, write the equilibrium equation as U'/a²=T(F(B0,a),a)/a².
The left side is S0[1−exp(−4chi)]/(4a_ref²), increasing from zero to a
positive finite limit for chi>=0. The right side is a positive increasing
function of u=B0/a, because at fixed a

    d/dB T(F(B,a),a)=q F_B=q/lambda>0, lambda=b_g.

It decreases with chi and tends to zero as u→0. The latter follows from
F~sqrt(aB), W~g³/(3a) and T~g³/(3a). Continuity gives a unique positive
root; no negative root exists because U'<0 there while T>0. This is a fixed-
flux homogeneous field result; it does not prove nonlinear boundary-value
uniqueness.

On the exact source-free affine background grad phi0=g0 n and chi0 constant,
the quadratic potential for psi=delta phi, eta=delta chi is

    [grad psi dot A grad psi + J|grad eta|² + m eta²]/(2C)
       −q eta n dot grad psi/C,

    A=mu I+(lambda−mu)n n^T,
    m=U''−2T+g0q.

Eliminate the derivative-mixing term along n. At equilibrium U'=T,

    m−q²/lambda
      =U''−2U'+q(g0−q/lambda)
      =S0 exp(−2chi0)+B0 q/lambda>0.

This is the complete positive Schur complement, not merely U''>0. For angle
theta, Lambda=mu sin²theta+lambda cos²theta and
cos²theta/Lambda<=1/lambda, so the same bound controls all directions.
The kinetic coefficients tau/C and sigma/C are positive. Every nonzero
Fourier mode therefore has positive squared frequencies, with determinant

    [Lambda k²−tau omega²]
    [J k²+m−sigma omega²]−q² k² cos²theta=0.

The signs and coefficients match SD1. Constant phi shifts are neutral; at
g0=0 the scalar spatial degeneracy prevents carrying over strict positivity.
Principal high-frequency speeds are sqrt(Lambda/tau) and v_chi. This proves
linear field-sector positivity only on the stated equilibrium, not responsive
matter stability, arbitrary off-equilibrium stability or nonlinear evolution.

### Exact negative control: positive U'' and positive diagonal masses fail

This control deliberately changes the potential, so it is not a refutation
of SD1's cosh-potential theorem. In Q units a_ref=B0=1, chi0=0, g0=sqrt(2),

    lambda=2sqrt(2)/3, q=1/3,
    T0=[sqrt(2)−log(1+sqrt(2))]/2,
    T_chi=2sqrt(2)/3−log(1+sqrt(2)).

Choose U=U0+T0 chi+h chi²/2 with

    h=17sqrt(2)/24−log(1+sqrt(2))>0.

The positivity is exact: 17sqrt(2)/24>1 while log(1+sqrt(2))<1 (since
1+sqrt(2)<5/2<e). The chosen background is an equilibrium, U''=h>0,
and the chi diagonal mass m=sqrt(2)/24>0. Nevertheless

    m−q²/lambda=−sqrt(2)/24<0.

With J=K=c=v_chi=1, parallel k²=sqrt(2)/48, the static coupled determinant
lambda k²[J k²+m−q²/lambda] is negative. Positive kinetic coefficients and
positive individual diagonal field stiffnesses coexist with a mixed-mode
instability. This validates why SD1's full Schur condition is load-bearing;
one cannot replace it with a claim about positive potential curvature alone.

### Responsive matter remains a separate sector

Adding a barotropic fluid to a supported, mean-subtracted homogeneous model
introduces its positive compression energy and the density-potential cross
term. At zero frequency, eliminating eta changes the phi gradient stiffness to
Lambda_eff(k)=Lambda−q² cos²theta/(Jk²+m)>0. The remaining density/phi
potential block has negative determinant when

    cs² Lambda_eff(k) k² < C rho0.

For small nonzero k this occurs for rho0>0 and finite positive cs². Thus
field-sector positivity cannot logically imply coupled matter stability, even
within a deliberately supported local model. Such a homogeneous fluid is not
an unsupplemented isolated background; no physical global instability is
claimed here. The full self-consistent background and its boundaries must be
supplied before astrophysical interpretation.

## 6. Vacuum identifications: functional identity versus one selected state

Three statements must be kept separate.

1. **Fixed vacuum reference only.** Setting a_ref by the core scale is
   consistent with an extra effective a=a_ref exp(chi), but this adds an
   environmental local scale. It does not preserve the literal statement that
   the actual a is fixed pointwise by the same constant rho_Lambda.
2. **Literal fixed vacuum and actual local core a.** It forces chi=0. The
   chi equation then fails under the nonzero source conditions in section 4.
3. **Scale-potential-only density identity for every chi in an interval.**
   Impose U_total(chi)/C=rho_Lambda(chi)c² and
   a_ref² exp(2chi)=kappa² c² G rho_Lambda(chi). Eliminating the density gives

       U_total(chi)=4 pi a_ref² exp(2chi)/kappa².

   A static homogeneous zero-field state has chi_tt=Delta chi=T=0, so its
   field equation requires U_total'=0. The identity instead gives
   U_total'=2U_total>0 at every finite positive-vacuum state. This is a precise
   incompatibility in the specified action and identification. A constant
   added to U cannot fix it while preserving this functional equality.

There is a decisive counterexample to dropping the functional qualifier.
Let Cvac=4 pi a_ref²/kappa²>0 and
U_total=Cvac+S0[cosh(2chi)−1]/4. At the single state chi=0, g=0,
U_total'=0 and U_total=Cvac, so a positive stationary homogeneous potential
vacuum matches the core relation *at that state*. Its first derivative does
not match that of Cvac exp(2chi), and the equality fails away from chi=0.
This does not refute SD1's explicit over-a-range obstruction; it prevents
promoting it into a no-go for every selected positive vacuum or every extra
constant background energy. The nonrelativistic action still supplies no
metric or full gravitational vacuum interpretation.

Nonzero homogeneous g also changes the stationarity equation to U'=T>0;
the zero-field vacuum no-go must not be extended to that driven-field case.
Kinetic/gradient energy of chi is not automatically vacuum energy. Assigning
rho_Lambda proportional to exp(2chi) by definition does not supply an equation
of state, metric coupling or a conserved covariant stress tensor.

## 7. Remaining static response and H-history checks

Linear static perturbations parallel to n obey
delta B=lambda delta g−q eta and (−J partial_x²+m)eta=q delta g.
Solving gives precisely SD1's response

    eta=q delta B/[lambda(M+Jk²)],
    delta g/delta B=(1/lambda)[1+q²/(lambda(M+Jk²))],

where M=m−q²/lambda>0. Its enhancement is positive. It is a one-dimensional
fixed-flux susceptibility, not an unconstrained density-to-force response in
an arbitrary geometry. The weak-response derivatives at fixed B,
partial_chi log g=a/(2(B+a)) for Q and t/[2(exp(t)−1)] for R, also match.
The spherical maximum-principle sign argument is valid for C² chi with the
specified zero outer boundary, regular center and T>=0: a negative interior
minimum makes −J Delta chi+U'<0 and cannot solve the equation.
Existence, uniqueness and boundary-independent amplitude do not follow from
that sign argument.

For the registered prescribed history H=H0 E, E²=.315(1+z)³+.685 and
z_t=−(1+z)H, set Omega_m=.315(1+z)³/E². Then
H_t=−3H² Omega_m/2 and Omega_m,t=−3H Omega_m(1−Omega_m). Direct substitution
gives

    chi_H,t=−3H Omega_m/2,
    chi_H,tt=(9/2)H² Omega_m(1−Omega_m/2)>0.

For z>=0, chi_H>=0 and U'>=0, so sigma chi_H,tt+U'>0. It cannot solve the
homogeneous zero-field chi equation without a drive. This is not an FLRW
equation, does not include Hubble friction, and does not prove that every
cosmological completion fails. Both registered a_ref values are positive and
the same symbolic conclusions hold for either; this proof-only audit makes
no new dimensional numerical prediction.

## 8. Numerical and code coverage

The original version-2 manifest was independently validated against current
inputs and outputs and passed. The 21 stored checks report success. The code
was inspected for the claimed mathematical objects, but the original BVP,
quadrature and spectral numerics were **not rerun or independently replicated**
in this proof audit. Therefore their amplitudes and convergence tables are
not independently accepted numerical results of FGF-010.

Two implementation-scope observations matter:

* `periodic_response` actually imposes homogeneous Neumann derivatives at both
  ends of [0,2pi], with integer cosine forcing. This is compatible with the
  tested linear cosine response, but it is not a direct imposition of periodic
  equality boundary conditions. Calling it a one-dimensional finite BVP is
  precise; it should not imply arbitrary periodic-boundary validation.
* The manufactured energy check solves for a local B chosen to drive the
  prescribed chi. It checks the chi-sector balance, not the existence of a
  free coupled phi/chi/matter trajectory. The author README correctly states
  this limitation.

The spherical runs impose chi(8)=0. Refining their initial mesh does not
establish independence of the finite outer radius. No global BVP uniqueness,
nonlinear stability, empirical parameter calibration, lensing, photon metric,
or cosmological solution was audited or established. There were no failed
source-hash or provenance checks. The counterexamples in this report are
successful exact negative controls, not failed computational experiments.

## 9. Verdict matrix and first remaining implication

| Obligation | Result |
|---|---|
| Action variation; T,q identities and strict signs | passed, exact Q/R algebra |
| Energy and momentum exchange signs | passed, smooth fields with boundary/source accounting |
| Uniform-static-scale obstruction | passed, no extra spatial source; finite J |
| Fixed-flux homogeneous equilibrium | passed, positive B and cosh potential |
| Coupled field Schur positivity and dispersion | passed, nonzero source-free affine equilibrium only |
| Universal stability from U''>0 | refuted by exact altered-potential negative control; not asserted by SD1 |
| Literal constant-vacuum actual-a compatibility | incompatible in this candidate under nonzero field drive |
| Functional potential-only density identity and stationary zero-field vacuum | incompatibility passed exactly |
| No positive vacuum under merely one-state matching | refuted by constant-shifted-cosh control; not SD1's scoped claim |
| Prescribed H history as zero-field solution | correctly rejected for the registered z>=0 trajectory |
| Candidate numerical amplitudes and BVP solver convergence | code/provenance inspected; no independent numerical reproduction |
| Responsive matter, global backgrounds, nonlinear or cosmological stability | not established |

The smallest unresolved physical implication is whether the environmental
actual a is an allowed new hypothesis at all; the construction does not derive
it from the literal constant-vacuum core law. If that strict reading is retained,
this particular reservoir class is excluded as its completion. If the modified
effective-scale hypothesis remains an exploratory candidate, the next
discriminating mathematical task is to build one **jointly balanced finite
barotropic-plus-two-field background**, rather than holding the matter source
fixed. In one dimension the equations can be written

    B'=C rho,
    cs² rho'=−rho F(B,a_ref exp chi),
    −J chi''+U'=T(F(B,a_ref exp chi),a_ref exp chi),

with positive B,rho and explicit wall/flux/chi boundary data. Verify all three
balances and then define the coupled perturbation problem on that same
background. Field-sector positivity alone cannot discharge this obligation.

This report is an independent worker review of pinned SD1 evidence. Promotion
still requires the orchestrator's separate review record pinning this result;
it is not automatically accepted by producing `result.json`.
