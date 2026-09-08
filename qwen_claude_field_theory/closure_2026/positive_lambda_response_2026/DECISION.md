# Positive Lambda does not rescue this spatial-kernel repair

2026-09-08. Base: `c759c46ac02e6c09cd0c7c3cb206b8c31bbc1b97`.

**Overall gravity goal: OPEN. Every finite positive-kinetic, subluminal member
of this parameter family fails the displayed linear physical Cauchy-locality
gate. Its unprojected R3 action also fails a nonlinear
off-shell domain test.** These are scoped mathematical obstructions, not an
empirical verdict, a universal MOND no-go, or a completed relativistic theory.

The previous checkpoint left two crucial gaps: its causal witness used
Lambda=0, and its conserved signed external stress was not healthy matter.
This checkpoint computes the positive-Lambda response and a *different*,
unforced, healthy canonical-matter initial-data witness. It does not identify
the two sources. It also varies a local auxiliary representation and closes
the actual homogeneous Dirac chain, without passing off either partial count
as the full nonlinear gravitational count.

## 1. Fixed theory and conventions

Use c=1, m=M^2>0, physical ADM metric and minimally coupled canonical matter
P(X)=X, X=-(partial sigma)^2/2. The theory is the same explicit Hamiltonian
S=S0+DeltaS_b from the preceding checkpoint:

\[
S_0=\int dT\,d^3x\,[\pi^{ij}\dot h_{ij}+p_\sigma\dot\sigma
-N(\mathcal H_{EH}+\mathcal H_m-m\sqrt h f)
-N^i\mathcal H_i-\lambda(\pi-\sqrt h\tau)],
\]
\[
\mathcal H_{EH}={2(\pi^{ij}\pi_{ij}-\pi^2/2)\over m\sqrt h}
-{m\sqrt h R\over2}+m\Lambda\sqrt h,\quad
\mathcal H_m={p_\sigma^2\over2\sqrt h}
+{\sqrt h\over2}h^{ij}\partial_i\sigma\partial_j\sigma,
\]
\[
\mathcal H_i=-2h_{ij}D_k\pi^{jk}+p_\sigma\partial_i\sigma,
\qquad f=2a_0^2[1-(1+y)e^{-y}],\quad
y=\sqrt{a_i a^i}/a_0,\quad a_i=D_i\log N,
\]
\[
\Delta S_b=-{m\over16}\int dT\,
\langle\sqrt N I,L^{-1}\sqrt N I\rangle_h
-\int dT\,{b\tau_T\over24}\langle L^{-1}I,L^{-1}I\rangle_h,
\quad L=-\Delta_h,\quad I=R-4D_i a^i-2a_i a^i.
\]

Here pi=h_ij pi^ij; the lapse and shift are physical, not a second matter
metric. The clock function is now fixed to
tau(T)=-3m Hd coth(3Hd T), Lambda=3Hd^2>0. This prescribed-clock ADM theory
still lacks a proved full covariant-clock completion. The principal physical
Cauchy calculation fixes b=3/16, the coefficient selected by the previous
curvature-endpoint calculation. It does not combine parameter-distinct models.

On the expanding branch, proper time t=T,

\[
a^3=\sinh(3H_dt),\quad H=H_d\coth(3H_dt),\quad
q=\dot\sigma=\sqrt{6m}H_d\operatorname{csch}(3H_dt),\quad
\dot H=-q^2/(2m),\quad\dot q=-3Hq,\quad\dot\tau=3q^2/2.
\]

An arbitrary constant scale normalization is also allowed. Write
a_initial=a(t0), not a0: a0 always denotes the MOND acceleration scale.
Spatial decay on R3 and a compact mean-zero spectral inverse are different
domains. Neither the inverse prescription nor its exceptional modes is implicit.

## 2. A healthy canonical perturbation with a pre-cone tidal response

`physical_initial_data.py` varies the inherited quadratic action, independently
computes the canonical stress and its four covariant Ward components, and
reconstructs the metric, extrinsic curvature and canonical momenta. Set
N=1+n, h_ij=a^2 exp(2z) delta_ij, N^i=partial_i B, and u=delta sigma.
At b=3/16 the actual elimination gives

\[
n=z=4\dot u/q,\qquad B=-{3q\over2m}\Delta^{-1}u,
\qquad \delta\rho=-3q\dot u,\qquad \delta p_\sigma=9a^3\dot u,
\]
\[
9(\ddot u+3H\dot u)-a^{-2}\Delta u+{3q^2\over2m}u=0,
\qquad
E_{\hat i\hat j}={3q\over4m}D_{ij}\Delta^{-1}(2Hu-\dot u),
\quad D_{ij}=\partial_i\partial_j-\delta_{ij}\Delta/3.
\]

The kinetic coefficient 9 and speed squared 1/9 are differentiated from the
reduced action. They are not a claim of full nonlinear stability. E is the
electric Weyl curvature of the physical metric, not a lapse coordinate effect.
FLRW Weyl is zero, so its linear perturbation is gauge invariant.

Measure comoving distance in units of the chosen inner radius. Choose a smooth
radial cutoff chi=1 for r<=1 and chi=0 for r>=2. Define
g(x)=chi(r)xy, u(t0)=0 and dot u(t0)=epsilon Delta g, epsilon>0.
Direct differentiation yields

\[
\Delta g=xy[\chi''(r)+6\chi'(r)/r].
\]

Thus the *physical canonical initial perturbation* is confined to 1<r<2.
In r<1, all initial lapse, spatial metric, shift, extrinsic curvature,
gravitational momenta, scalar field and scalar momentum agree with the
background. Scalar constraints are satisfied, and TT/vector data are zero.
The initial electric Weyl is nevertheless -3 epsilon q(t0)/(4m) in its xy
component there. Curvature accelerations are derived, not independent data.

This effect persists at strictly positive time, not just on the initial slice.
Let F solve the displayed local matter operator with F(t0)=0, dot F(t0)=g;
then u=epsilon Delta F. The action-derived energy satisfies

\[
e={1\over2}[\dot F^2+|\nabla F|^2/(9a^2)+q^2F^2/(6m)],\quad
J=-\dot F\nabla F/(9a^2),
\]
\[
\dot e+\nabla\cdot J=-3H\dot F^2-H|\nabla F|^2/(9a^2)
-Hq^2F^2/(2m)\le0,\qquad |J\cdot\hat n|\le e/(3a).
\]

The script checks the identity and the flux bound as sums of squares. Local
energy uniqueness therefore gives F=s(t)xy before the primitive's boundary
can arrive, where s(t0)=0, dot s(t0)=1. Set Y=qs. The actual transformation is

\[
\ddot Y+9H\dot Y+(10H^2+8H_d^2)Y=0,
\quad Y(t_0)=0,\quad\dot Y(t_0)=q_0>0,
\qquad E_{\hat x\hat y}=-{3\epsilon\over4m}(\dot Y+HY).
\]

Here q0=q(t0). Let Y=q0 G, H0=H(t0), x=H0(t-t0), g_G=H0 G.
The normalized equation has 0<=p<=9, 0<c<=18. Before any first zero of
g_G', positivity implies 0<=g_G'<=1 and 0<=g_G<=x. Integrating its equation
gives g_G'>=1-9x-9x^2. This is at least 211/400 for x<=1/20, contradicting
such a first zero. Hence G_t+HG>=211/400 on that interval, and

\[
\boxed{|E_{\hat x\hat y}(t,0)|\ge{633\epsilon q_0\over1600m}>0,
\quad 0<t-t_0\le\min\{1/(20H_0),a_{\rm initial}/4\}.}
\]

The metric light distance is <=(t-t0)/a_initial<=1/4, whereas differing
initial canonical data begin at distance one. The matter distance is <=1/12.
This proves nonlocal dependence of the *original metric/matter canonical
evolution* in the linear theory, for every m,Hd,t0>0 on this branch.

Important qualifications:

- For small epsilon the total canonical matter energy stays positive. Signed
  delta rho does not mean a negative-energy matter species.
- The actual Ward identity is bar-div(delta T)+delta-Gamma*Tbar=0 on the
  perturbed Klein-Gordon equation. It is not separate conservation of delta T.
- On R3, decay gives Delta^-1 Delta g=g. On a flat torus of side L>4, g's xy
  parity gives mean zero, so the same inverse identity and local witness hold.
- The elliptic variable L^-2 I, and thus a localized W, need not agree in the
  inner ball. It is constrained by global data, not an extra freely specifiable
  datum of the original nonlocal action. We do not assert equality of all
  localized auxiliary values in a supposed local reformulation.
- A zero-past actuator realization and a nonlinear lift of these constraint
  data have NOT been established. The exact q=0 stratum is not used.
- Compact primitive data do obey an *outer support envelope*. That statement
  does not imply physical locality in a hole where g is harmonic but nonzero.

### The coefficient cannot tune this away

`general_family.py` re-varies the action for arbitrary positive b, derives
K=9/(2b)-15, and reconstructs the general metric. It does NOT assume the
K=9 curvature formula. The actual general result is

\[
n={4\dot u\over q},\quad z={(K+3)\dot u\over3q},\quad
\delta p_\sigma=Ka^3\dot u,
\]
\[
E_{\hat i\hat j}={9-K\over6a^2q}D_{ij}\dot u
+{3q\over4m}D_{ij}\Delta^{-1}(2Hu-\dot u).
\]

The coefficient-dependent *local* term vanishes in the annular hole, because
u=dot u=0 there before propagation. The *nonlocal* term does not. All original
canonical initial data still agree in the hole. Y=qs now obeys

\[
\ddot Y+9H\dot Y+
9[(1+1/K)H^2+(1-1/K)H_d^2]Y=0.
\]

For every finite K>=1 its normalized coefficients satisfy the same bounds
used above. Consequently the boxed positive tidal lower bound is unchanged.
The matter-cone margin is now at least 3/4, since its speed is 1/sqrt(K)<=1;
the K=9 value 11/12 is not imposed on other members. Perturbation amplitude
may be chosen separately for each finite K to keep the metric and matter
perturbations small. No uniform infinite-K limit is claimed.

Solving inequalities of the differentiated kinetic coefficient partitions b>0:

| Parameter interval | Derived linear result |
| --- | --- |
| 0<b<=9/32 | K>=1: positive kinetic coefficient, subluminal matter principal speed, but the physical Cauchy-locality obstruction above |
| 9/32<b<3/10 | 0<K<1: superluminal matter principal speed |
| b=3/10 | K=0: degenerate kinetic branch; regular reduction cannot certify it |
| b>3/10 | K<0: negative kinetic energy |

This rules out coefficient tuning within the regular tested family. It does
not classify the singular b=0/infinite-K theory, certify the K=0 branch, or
prove nonlinear nonexistence for a different clock/kinetic architecture.

## 3. The positive-Lambda signed external probe also fails

`positive_lambda.py` varies the actual general-a,q action with the full a^3
volume and minimal linear source coupling. It does not reuse the stiff result.
For finite K>=1, b=9/[2(K+15)], it derives the dipole-moment operator

\[
L_Y=\partial_t^2+9H\partial_t+
9[(1+1/K)H^2+(1-1/K)H_d^2].
\]

For g=partial_x eta with smooth radial compact unit-integral eta, choose
Sigma00=Rg+C Delta g, Sigma0i=j partial_i g/a^2, Sigmaij=Pg deltaij/a^2.
All four Ward components give P=-dot j-3Hj,
dot R+3H(R+P)=0, dot C+3HC=-j/a^2, with zero past data.
For the radial primitive moment Y, setting Y=(K+3)j/K+Z gives

\[
L_YZ={12H\over K}\dot j+
{9[(4K-3)H^2+3H_d^2]\over K^2}j+{12H\over K}R.
\]

Every displayed weight is positive. The same short-time Green comparison
gives a strict exterior response for j=exp[-delta^2/(t-t0)^2],
delta=1/(20H0), j=0 earlier. At t=t0+delta, r*=1+2delta/a_initial,

\[
|E_{\hat x\hat x}|>{135H_0\over\pi e m K r_*^4}>0.
\]

No incoming vector or tensor perturbation is needed; their source projections
vanish. The source is still a **signed external probe**. The separate result
in section 2 removes that qualification only for its different Cauchy witness.
Three DOP853 checks (K=1,9,100, Hd=m=t0=1), each at two tolerances, corroborate
the bound; the analytic comparison, not the samples, proves it.

## 4. A nonlinear infrared obstruction invisible at quadratic order

`infrared_domain.py` computes Ricci curvature from Christoffels and the exact
radial curved Poisson flux. On R3 take N=1 and h=exp(2zeta) delta with compact
nonconstant zeta. Integration by parts gives

\[
Q=\int\sqrt h I=\int\sqrt h R=2\int e^\zeta|\nabla\zeta|^2>0.
\]

The fixed-support path zeta=2 log(1+epsilon psi), for smooth nonnegative
compact radial nonconstant psi, has Q=32 pi epsilon^2 A, where
A=integral_0^1 r^2 psi'(r)^2 dr>0. Outside support, the decaying inverse has
V=L^-1 I=Q/(4pi r). For L2>L1 beyond support,

\[
\Delta\|V\|_h^2={Q^2\over4\pi}(L_2-L_1),\qquad
\Delta S_2=-{b\tau_TQ^2\over96\pi}(L_2-L_1)
\]

per unit clock time. The norm diverges and the second action term tends to
minus infinity for b tau_T>0. Its amplitude onset is exactly epsilon^4;
quadratic perturbation tests cannot detect it. A smooth positive-amplitude
time interval also makes the time-integrated action diverge. The first kernel
term is finite and cannot cancel the tail. This is a divergence of the
perturbation action relative to the background: the new term is zero on the
background, and the local seed's change is compactly supported. It is not
merely the infinite background volume of a homogeneous R3 cosmology.

Consequently there is no open neighborhood containing all these ordinary
compact-conformal off-shell variations for the *unprojected decaying R3*
functional. If its domain is restricted to integrable sources, these arbitrarily
small variations are instead excluded. This is not an on-shell no-solution
theorem. Compact/projected or infrared-modified actions require their own
variation; projection alone does not remove section 2's linear torus witness.
A smooth zero-monopole dipole control has finite exterior squared norm
d^2/(12pi R), so the code does not claim that every spatial inverse diverges.

## 5. Action variation and genuine partial Dirac closure

Write c_b=b tau_T/24 (not the speed of light), n=log N, and
Y_aux=m U sqrt(N)/8+W. An equivalent local expression *on an admissible
inverse/IBP domain* is

\[
\mathcal L_{aux}/\sqrt h={m\over16}|DU|^2+DW\cdot DV-c_b V^2-Y_{aux}I.
\]

`localized_auxiliary.py` obtains LU=sqrt(N)I, LV=I, LW=2c_b V, the full lapse
variation -m U sqrt(N)I/16+4 Delta Y_aux-4 D_i(Y_aux a^i), and the metric EL
tensor. All six inverse-metric variation directions are independently checked
from Christoffels on conformally curved h, with arbitrary three-coordinate
lapse and auxiliary fields. This is a bounded exact geometric check, not a
formal full-manifold proof. The actual six auxiliary constraints have computed
Poisson rank six for positive spatial eigenvalue and zero auxiliary pairs;
all multiplier-preservation equations are solved with source/coefficient drift.
At zero eigenvalue the computed rank is two and the count is withheld.
Compact-projector variations/global mean multipliers are not included. Even
zero monopole does not ensure W=L^-2(2c_b I) decays; boundary pairings matter.

`constraint_hessian.py` makes the exact time-dependent canonical shift
pi_tilde^ij=pi^ij-(tau/3)sqrt(h)h^ij. Its generator (2tau/3)int sqrt(h)
adds the essential +2tau_T sqrt(h)/3 to the Hamiltonian. Homogeneously, with
h=e^chi gamma, det(gamma)=1, v=e^(3chi/2), the shifted Hamiltonian is

\[
H'=N[(m\Lambda-\tau^2/(3m))v+p_\sigma^2/(2v)]+2\tau_Tv/3.
\]

The primaries are p_N=p_chi=0 and the secondaries are the actual
-partial_N H', -partial_chi H'. On their regular surface rho=p_sigma^2/(2v^2)>0,

\[
\mathsf H_{(N,\chi)}=
\begin{pmatrix}0&-3v\rho\\-3v\rho&3v\tau_T/2\end{pmatrix},
\quad\Omega=\begin{pmatrix}0&\mathsf H\\-\mathsf H&0\end{pmatrix},
\quad\det\mathsf H=-9v^2\rho^2.
\]

The computed Poisson rank is four: zero first-class and four second-class
constraints in this homogeneous scalar subsystem, leaving one matter pair.
Preservation includes tau_T and tau_TT, fixes both multipliers, and yields
N=tau_T/(3rho), H=-tau/(3m). The positive-Lambda solution has N=1, dot N=0
and H>0. At rho=0 the surface is irregular and no regular-branch count is
inherited. Full gravitational counting still needs the mixed lapse/conformal
*functional* Hessian, not merely H_NN or a chosen finite matrix.

## 6. Status, next calculation, and verification standard

As a regular full-theory proposal required to have local physical Cauchy
dependence, this fixed b=3/16 repair is **DEAD at its linear gate**, as are
all finite K>=1 members of this family at that gate. This is
not a nonlinear nonexistence theorem. If those linear perturbations cannot
be lifted, that itself demands a separate analysis of the nonlinear admissible
data/linearization problem; it does not retrospectively certify healthy closure.
The larger MOND/primordial-clock research goal is **OPEN**.

More coefficient fitting, a positive kinetic coefficient, or a larger toy
Poisson matrix cannot repair these findings. A successor must first derive a
gauge-invariant curvature response in which the observable inverse-Laplacian
term cancels, from one explicit action with a specified finite nonlinear
domain. A healthy covariant clock completion is an architectural change and
must be varied and counted afresh. Merely changing topology or projecting out
the homogeneous mode cannot remove the annular linear witness.

PPN beta/gamma/alpha_i, measured G, full nonzero-mode Dirac closure, zero-field
regularity, nonlinear stability and a derived a0-Lambda relation have not been
supplied by this checkpoint. The previous leading static MOND/lensing screens
must not be promoted to those absent results. The proof challenge should keep
these gates distinct, following the useful verification pattern of the linked
fluid repository, not importing its PDE results as gravity evidence.

`closure_extension.py` records six computations and missing gates separately.
The reproduction record distinguishes successful computations from the failed
physics acceptance gates. Exact commands, individual exits and the immutable execution
manifest are in REPRODUCE.md. Mathbox computation/proof audits enforced scoped
hypotheses and negative controls. Self-proofreading covered this report:
initial scale a_initial is kept distinct from MOND a0, Y from Y_aux, and
kinetic K from spatial L; no broader manuscript was rewritten. No Lean build,
empirical-data fit, or global novelty claim is made.
