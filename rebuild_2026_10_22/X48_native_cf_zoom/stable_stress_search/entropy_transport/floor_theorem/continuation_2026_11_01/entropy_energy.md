# Entropy variables and a density-gradient symmetrizer for startup

Owner: delegated entropy/energy continuation. Base checkpoint:
**X48-FLOOR-2026-11-01-B**. Observed Git revisions during the read:
f55188b7295cfc56670f8e1ef49fe6c8d7ccc191 and
c00c9f6ed7b3aef6e017507abee29e5dd1e37624; the shared checkout changes
concurrently. Exact inputs are pinned in the final table. Write scope: this
file only. No law, initial condition, previous route note, shared status, or
finite-run artifact was changed.

**Result: the original uniform startup assertion remains unproved.** New
results here are the complete heat edge variation, positivity of the density
stiffness after the full local heat principal coupling, an actual-geometry
conductance comparison, a dissipative density-gradient energy, and an
all-mesh pointwise smoothing theorem for the leading coupled system. The coefficient commutator and the localized
pointwise estimate needed to close a common-time amplitude bootstrap remain
unproved. No mesh-uniform regularity theorem is assumed.

## Exact variables and target

Use the unchanged normalized parameters, \(dm=M/N\), \(M=\pi/3\),
\(\mu_i=dm\) for \(i<N\), \(\mu_N=dm/2\), and cells \(i=1,\ldots,N\).
Set
\[
 V_i=dm/\rho_i,\quad z_i=\log\rho_i,\quad
 x_i=-\dot V_i/V_i,\quad W_i=W(\rho_i),\quad h_i=h(\rho_i),
 \qquad W'(\rho)=h(\rho).
\]
The missing statement is a common \(T>0\), independent of every \(N\ge32\),
such that
\[
 x_i(t_a+s)\ge4,\quad 0\le s\le T,\quad
 1\le i\le\lceil N/4\rceil .                         \tag{UC}
\]
Here \(t_a=0.5907973398405\ldots\), \(\rho(t_a)=1\), \(K(t_a)=0\), and
\(x(t_a)=C_a=5.4145849604\ldots\) are the exact common activation data from
the preceding seed route. Decimal annotations are not proof inputs. The
ceiling includes every cell intersecting the central material quarter; a
bound only through \(\lfloor N/4\rfloor\) misses the last intersecting cell
when \(N\) is not divisible by four.

On the active branch \(\rho>1,\ x>2\), write
\[
 \kappa=\tfrac12\rho Wh,\quad g(K)=\frac K{K+c_d},
 \quad c_d=1/100,\quad \nu=\kappa(1+g),\quad
 P=K\rho^2h,\quad S=\nu x-2\kappa+P.                 \tag{1}
\]
The exact equations are
\[
 \dot x=\mathcal L_rS+R,\quad \dot z=x,\quad
 \dot K=Q+H,\qquad H_i=\frac{L_{i-1}-L_i}{dm\,W_i},   \tag{2}
\]
with \(R\ge0\) as proved in the preceding startup energy note. The source
\(Q\) retains both original and memory heaters. All derivations below start
from this complete system.

## 1. Thermodynamic convexity, degeneracy, and localized heat balance

Put \(v=1/\rho\), \(\sigma=K^{1/3}\). Then
\[
 e(v,\sigma)=\sigma^3W(1/v),\quad T=e_\sigma=3\sigma^2W,\quad
 P=-e_v=\sigma^3\rho^2h,\quad
 \psi=KW^{3/2}=(T/3)^{3/2}.                         \tag{3}
\]
In the ramp, with \(t=\rho-1\), direct expansion gives
\[
 W-\rho h=\tfrac32(1-t^2)^2\ge0.                   \tag{4}
\]
Below the ramp \(h=0\); above it \(W=\rho,\ h=1\). Thus
\(0\le\rho h/W\le1\) at every density. The Hessian is
\[
 e_{\sigma\sigma}=6\sigma W,\quad
 e_{\sigma v}=-3\sigma^2\rho^2h,\quad
 e_{vv}=\sigma^3\rho^3(2h+\rho h'),
\]
\[
 \det D^2e
 =3\sigma^4\rho^3\{2W(2h+\rho h')-3\rho h^2\}
 \ge3\sigma^4\rho^3W(h+2\rho h')\ge0.              \tag{5}
\]
The physical relative energy
\[
 e(v,\sigma)-e(v_d,\sigma_d)
       +P_d(v-v_d)-T_d(\sigma-\sigma_d)             \tag{6}
\]
is consequently nonnegative. At activation it is just \(KW\), and gives
no density coercivity. Along the homogeneous warming reference,
\(\sigma_d\asymp s,\ \rho_d-1\asymp s\), so
\[
 e_{\sigma\sigma}\asymp s,\quad e_{vv}\asymp s^4,\quad
 e_{\sigma v}=O(s^4),\quad \det D^2e\asymp s^5.     \tag{7}
\]
Uniform unscaled coercivity is false.

For any fixed cutoff \(\phi_i\), let \(\Delta_e f=f_{i+1}-f_i\) and
\(\bar f_e=(f_i+f_{i+1})/2\). For any spatially constant \(T_d>0\), exact
shared-luminosity summation gives, on a warm interval,
\[
 \begin{split}
 \left.\frac d{dt}\sum_i dm\,\phi_i(e_i-T_d\sigma_i)
                                                  \right|_{\rm heat}
 ={}&-T_d\sum_e\bar\phi_e L_e\Delta_e(1/T)\\
 &+\sum_e\Delta_e\phi\,L_e
                    [1-T_d\overline{(1/T)}_e].
 \end{split}                                                   \tag{8}
\]
For a positive-luminosity face, write \(L_e=-\ell_e\Delta_e\psi\) with
\(\ell_e\ge0\). Then
\[
 L_e\Delta_e(1/T)\ge
 \tfrac29\ell_e\psi_{\max,e}^{-5/3}(\Delta_e\psi)^2\ge0. \tag{9}
\]
This follows from \(1/T=(1/3)\psi^{-2/3}\). At zero temperature (8) is
used after fixed-mesh positivity or by positive-temperature regularization;
it does not assume uniform startup positivity. The cutoff term is actual
transport and cannot be discarded.

## 2. Complete heat edge variation

At one internal face use subscripts \(l,r\), centroid separation \(d>0\),
area \(A=4\pi r_{\rm face}^2\), and
\[
 D_K=K_l-K_r,\quad D_\psi=\psi_l-\psi_r,\quad
 \gamma=c_g+(K_l+K_r)/2,\quad c_g=1/100,\quad
 b=\frac{\ell_gD_K}{d\gamma+\ell_gD_K},\quad \ell_g=1/10.
\]
On the open branch \(D_K>0,\ D_\psi>0\), the exact outgoing luminosity is
\[
 L=C h_lh_r bD_\psi,\qquad C=DA/d,\qquad D=1/10.     \tag{10}
\]
Here \(b\) denotes only the face gate. At fixed geometry,
\[
 b_l=\frac{\ell_gd(c_g+K_r)}{(d\gamma+\ell_gD_K)^2}>0,\qquad
 b_r=-\frac{\ell_gd(c_g+K_l)}{(d\gamma+\ell_gD_K)^2}<0.
\]
The four exact thermodynamic edge derivatives are
\[
 \begin{aligned}
 L_{K_l}&=Ch_lh_r[bW_l^{3/2}+b_lD_\psi],\\
 L_{K_r}&=Ch_lh_r[-bW_r^{3/2}+b_rD_\psi],\\
 L_{z_l}&=Ch_r[\rho_lh_l'bD_\psi+
                    h_lb\,\tfrac32K_lW_l^{1/2}\rho_lh_l],\\
 L_{z_r}&=Ch_l[\rho_rh_r'bD_\psi-
                    h_rb\,\tfrac32K_rW_r^{1/2}\rho_rh_r].
 \end{aligned}                                                   \tag{11}
\]
In particular \(L_{z_r}\) has no fixed sign. Dropping the density columns
does not linearize the actual law. The variation including geometry is
\[
 \begin{split}
 \frac{\delta L}{L}={}&2\frac{\delta r_{\rm face}}{r_{\rm face}}
 -(2-b)\frac{\delta d}{d}
 +\frac{\rho_lh_l'}{h_l}\delta z_l
 +\frac{\rho_rh_r'}{h_r}\delta z_r\\
 &+(1-b)\left[\frac{\delta K_l-\delta K_r}{D_K}
             -\frac{\delta K_l+\delta K_r}{2\gamma}\right]
 +\frac{\delta\psi_l-\delta\psi_r}{D_\psi},
 \end{split}                                                   \tag{12}
\]
\[
 \delta\psi_i=W_i^{3/2}\delta K_i+
                    \tfrac32K_iW_i^{1/2}\rho_i h_i\delta z_i.    \tag{13}
\]
The divisions in (12) are only for its open branch. At branch boundaries
use (11) by limits or direct one-sided differentiation of (10). If both
drops vanish, the directional first derivative is zero. If only one drop
vanishes and the other is positive, a one-sided derivative can be nonzero.
A neutral entropy gradient therefore does not delete the heat Jacobian.

The heat row further contains the denominator variation
\[
 \delta H_i=\frac{\delta L_{i-1}-\delta L_i}{dm W_i}
                      -H_i\frac{\rho_i h_i}{W_i}\delta z_i.       \tag{14}
\]
When using cell density variations, equal masses give the exact geometric
variation
\[
 \delta r_i=-\frac1{4\pi r_i^2}\sum_{j\le i}V_j\delta z_j.        \tag{15}
\]
The centroid variation is the derivative of the explicit centroid formula
in the source. Thus geometry cannot be freely frozen in a nonlinear
density-coordinate estimate.

The complete coupled graph variation is
\[
 \begin{aligned}
 \delta\dot x={}&\mathcal L_r(\nu\delta x+S_z\delta z+S_K\delta K)
                       +(\delta\mathcal L_r)S+\delta R,\\
 \delta\dot z={}&\delta x,\\
 \delta\dot K={}&\delta Q+\delta H,
 \end{aligned}                                                   \tag{16}
\]
with \(\delta H\) given by (11)--(15). This is not the scalar homogeneous
principal graph.

## 3. Positive density stiffness survives the heat principal coupling

**Constitutive lemma.** On \(\rho>1,\ x>2,\ K\ge0\),
\[
 c_\psi:=S_z-S_K\frac{\psi_z}{\psi_K}
       \ge\kappa[(x-2)+g]+\tfrac12P>0.              \tag{17}
\]
To prove this, set \(w=\rho h/W\) and \(j=\rho h'/h\). Equations (4) and
(1) give \(0\le w\le1,\ j\ge0,\ Kg'=g(1-g)\), and
\[
 \begin{split}
 c_\psi={}&\kappa\{[(1+g)x-2](1+w+j)
                         -\tfrac32wxg(1-g)\}\\
 &+P(2+j-\tfrac32w). 
 \end{split}                                                   \tag{18}
\]
Writing \(x=2+e\), the brace is
\[
 e\{(1+g)(1+w+j)-\tfrac32wg(1-g)\}
                       +g(2+2j-w+3wg).
\]
The first brace is at least one since it equals
\(1+g+w(1-g/2+3g^2/2)+(1+g)j\). The second parenthesis is at least one.
The pressure coefficient is at least \(1/2\). This proves (17).

The entropy-gradient gate also contributes to the local-gradient
principal symbol. To retain it, at an active local gradient set
\[
 q=-\partial_rK>0,\quad p=-\partial_rz,\quad
 J=\psi_Kq+\psi_zp>0,\quad
 b(q)=\frac{\ell_gq}{c_g+K+\ell_gq},\quad C=Dh^2.
\]
The outgoing heat flux is \(Cb(q)J\). Its gradient derivatives are
\[
 J_K=C[b\psi_K+b_qJ]>0,\qquad J_z=Cb\psi_z\ge0,\qquad
 0\le\eta_h:=J_z/J_K\le\psi_z/\psi_K.                \tag{19}
\]
Up to positive radial factors, the second-derivative matrix in variables
\((x,z,K)\) is
\[
 \mathsf A=
 \begin{pmatrix}
 \nu&S_z&S_K\\
 0&0&0\\
 0&J_z/W&J_K/W
 \end{pmatrix}.                                                 \tag{20}
\]
It has eigenvalues \(\nu,\ J_K/W,\ 0\). The heat principal coordinate
\(\theta=\delta K+\eta_h\delta z\) leaves density coefficient
\[
 c_h=S_z-S_K\eta_h\ge c_\psi>0.                    \tag{21}
\]
In temperature-potential coordinates the heat density column is
\(J_z-J_K\psi_z/\psi_K\le0\), rather than zero. This is the column from
differentiating the entropy-gradient gate. Equations (19)--(21) retain it.
Matrix (20) is the local-gradient symbol; the full finite-grid Jacobian is
(11)--(16), including coefficient and geometry variations. Positivity of
these symbol eigenvalues is not a nonlinear regularity estimate.

## 4. Uniform actual-geometry conductance comparison and exact cross term

Across an internal face put
\[
 a_i=\frac{(4\pi r_i^2)^2}{\mu_i},\qquad
 \ell_i=\frac{D\,4\pi r_i^2}{d_i}h_i h_{i+1}b_i.
\]
Every ordered geometry satisfies
\[
 \frac{\ell_i}{a_i}\le4D\rho_i h_i h_{i+1}b_i.       \tag{22}
\]
Indeed the left centroid satisfies
\[
 r_i-r_{c,i}=\frac{r_i-r_{i-1}}4
 \frac{r_i^2+2r_ir_{i-1}+3r_{i-1}^2}
      {r_i^2+r_ir_{i-1}+r_{i-1}^2}
 \ge\frac{r_i-r_{i-1}}4.
\]
The right centroid is beyond \(r_i\), whence
\(4\pi r_i^2d_i\ge V_i/4\). Internal \(\mu_i=dm\) gives (22).
No neighboring-density or cell-width comparability hypothesis is needed.

Put \(f=S-S_d,\ q=\psi-\psi_d\), with spatially constant references, and
\[
 \alpha_i=\frac{S_{K,i}}{\rho_i\nu_iW_i}
      =\frac{g_i'x_i+2\rho_i/W_i}{\rho_iW_i(1+g_i)}. \tag{23}
\]
Pair \(S_{\rm spatial}'=\nu\mathcal L_rS+S_KH\) and
\(\psi_{\rm heat}'=W^{3/2}H\) with \(V_if_i/\nu_i\) and
\(\Gamma\,dm\,q_i/W_i^{1/2}\), where \(\Gamma>0\) is spatially constant.
On an active component the exact interior edge expression is
\[
 -\sum_ea_e(\Delta_ef)^2
 -\sum_e\ell_e\Delta_e(\alpha f)\Delta_eq
 -\Gamma\sum_e\ell_e(\Delta_eq)^2.                  \tag{24}
\]
For the full graph add the stress outer work \(-a_Nf_NS_N\); there is no
heat boundary work. Interior cutoffs instead give their explicit cutoff
edge terms. Formula (24) is a pairing identity. It is not the full time
derivative of a quadratic energy: state-dependent weight derivatives,
local reactions, and cutoffs are additional terms.

Since
\[
 \Delta(\alpha f)=\bar\alpha\Delta f+\bar f\Delta\alpha,           \tag{25}
\]
the first cross term spends at most half of the stress and heat squares
whenever
\[
 \Gamma\ge\max_e\frac{\ell_e\bar\alpha_e^2}{a_e}.     \tag{26}
\]
This algebraic condition has a uniform near-activation bound. Under the
provisional envelope \(2<x\le8,\ \rho\le\exp(8s),\
0<s\le10^{-3}\), one has \(\rho\le2,\ h\le243s^2,\ \alpha\le536\).
Equation (22) gives
\[
 \ell_e\bar\alpha_e^2/a_e\le1.4\,10^{10}s^4\le0.014,
\]
so \(\Gamma=1\) suffices for this part, uniformly in every \(N\) and the
actual geometry. The amplitude envelope is a bootstrap hypothesis, not a
proved common-time assertion.

The remaining spatial commutator is exactly
\[
 \mathcal C=-\sum_e\ell_e\bar f_e\Delta_e\alpha\Delta_eq,\qquad
 |\mathcal C|\le\frac\Gamma4\sum_e\ell_e(\Delta_eq)^2+
 \frac1\Gamma\sum_e\ell_e\bar f_e^2(\Delta_e\alpha)^2. \tag{27}
\]
The last term, the weight time derivatives, and the cutoff terms have not
been bounded for the actual startup solutions. Bounded \(\alpha\) does not
give a mesh-uniform gradient or commutator bound. Formula (23) cancels the explicit factor \(h\), but
its spatial differences still contain differences of the compression.

## 5. A dissipative density-gradient energy for the leading coupled system

At common activation,
\[
 \kappa_d=k_2s^2+O(s^3),\quad k_2=\tfrac94C_a^2,\qquad
 S_z(\rho_d,K_d,x_d)=c_1s+O(s^2),\quad
 c_1=\tfrac92C_a(C_a-2)>0.                          \tag{28}
\]
The homogeneous \(K_d=O(s^3)\) leaves these leading coefficients
unchanged. For \(\xi=x-x_d,\ \zeta=\log(\rho/\rho_d)\), the leading
compression/density subsystem is
\[
 \dot\xi=\mathcal L_d(s)[\nu(s)\xi+c(s)\zeta],\quad
 \dot\zeta=\xi,\qquad \nu=k_2s^2,\quad c=c_1s.       \tag{29}
\]
The off-diagonal stress is the same size as the principal stress when
\(\zeta=O(s)\); it has not been treated as a small arbitrary remainder.

**Linear coupled energy theorem.** On a finite graph let
\(\mathcal L=V^{-1}\operatorname{div}(a\Delta)\), with positive cell
weights and nonnegative edge conductances, and zero exterior data. Suppose
\(V_i'\le0,\ a_e'\le0,\ \nu\ge0,\ c>0,\ c'\ge0\).
Every solution of \(\xi_t=\mathcal L(\nu\xi+c\zeta),\
\zeta_t=\xi\) satisfies
\[
 \mathcal E=\frac1{2c(s)}\sum_iV_i\xi_i^2+
                       \frac12\sum_ea_e(\Delta_e\zeta)^2,
\]
\[
 \begin{split}
 \dot{\mathcal E}={}&-\frac\nu c\sum_ea_e(\Delta_e\xi)^2
 -\frac{c'}{2c^2}\sum_iV_i\xi_i^2\\
 &+\frac1{2c}\sum_iV_i'\xi_i^2+
                   \frac12\sum_ea_e'(\Delta_e\zeta)^2\le0.
 \end{split}                                                   \tag{30}
\]
Proof: pairing the first equation with \(\xi/c\) gives the mixed term
\(-\sum a\Delta\xi\Delta\zeta\). Differentiating the second energy term
gives precisely its opposite since \(\zeta_t=\xi\). The other terms are
the four displayed terms. This is a finite-graph identity independent of
the number of cells.

The actual homogeneous dust graph has
\[
 V_{d,i}'/V_{d,i}=-x_d<0,\qquad
 a_{d,e}'/a_{d,e}=-4x_d/3<0.
\]
Consequently (30) applies to (29), retaining moving reference weights and
the half outer node mass. No uniform positive first-cell radius is used.
Boundary and local reaction forcing give explicit work terms; they were
set to zero only in this stated homogeneous problem.

For a fixed graph, the constant multiple with
\(b_0=2(C_a-2)/C_a\),
\[
 \frac{\|\xi\|_V^2}{2s}
           +\frac{b_0k_2}{2}\sum_ea_e(\Delta_e\zeta)^2
\]
has derivative
\(-k_2s\sum a(\Delta\xi)^2-\|\xi\|_V^2/(2s^2)\).
Thus the normalized density equation
\((\zeta/s)_t=[\xi-\zeta/s]/s\) admits an exact coupled cancellation.

A nonlinear extension must replace \(c(s)\) by the state-dependent
positive stiffness (17) or (21). Its differentiation introduces the
actual heat-divergence and coefficient-gradient terms. Equation (30) does
not estimate those terms, and freezing them would omit the nonlinear step.

## 6. Why the energies do not yet give central pointwise startup

Small physical relative energy does not bound a divergence. At a
homogeneous warm reference perturb one node at a fixed positive material
radius by velocity \(\epsilon/N\), leaving density and entropy unchanged.
The thermodynamic relative energy (6) is zero; relative kinetic energy is
\(O(\epsilon^2/N^3)\). The two neighboring cell compressions change by
\(O(\epsilon)\), while their weighted bulk dissipation is only
\(O(\nu\epsilon^2/N)\). These are admissible instantaneous states, with
bounded active compression for small epsilon. They are not asserted to
occur in the specified initial-value problem. They disprove the proposed
energy-to-pointwise inference, not (UC).

Even one stress graph derivative has no uniform central infinity-norm
embedding. On the homogeneous graph put \(f_1=1\) and every other value
zero. Then
\[
 \|f\|_{V_d}^2=O(N^{-1}),\quad
 \sum_ea_{d,e}(\Delta_ef)^2=a_{d,1}=O(N^{-1/3}),\quad
 \|f\|_\infty=1.                                  \tag{31}
\]
Here \(r_1^4\asymp N^{-4/3}\), \(\mu_1\asymp N^{-1}\). The central
graph has radial three-dimensional degeneracy. An unweighted
one-dimensional Sobolev embedding in the mass coordinate would be false.
A genuine local smoothing, iteration, or higher derivative estimate is
necessary after closing the first energy. The following continuation proves
one such smoothing theorem for the leading model only.

## 7. Leading-model pointwise smoothing, proved without a regularity lemma

The leading-model multiplier in the companion all-mesh note can be
upgraded from a spectral bound to a pointwise smoothing estimate. This
does not approximate the nonlinear solution, but it resolves the missing
pointwise implication for that particular linear model.

Fix any homogeneous geometry \(r_i=b_*(i/N)^{1/3}\), density
\(\rho_*=1/(4b_*^3)>0\), with \(M=\pi/3\), and retain the half outer node mass.
The cell weights are \(V_i=M/(N\rho_*)\); for \(i<N\),
\[
 a_i=48\pi b_*^4N^{-1/3}i^{4/3},
\]
and the outer Dirichlet conductance is twice the same formula. Put
\(\mathscr D(f)=\sum_{i=1}^Na_i(f_{i+1}-f_i)^2\), \(f_{N+1}=0\).
Direct telescoping and Cauchy--Schwarz give
\[
 |f_i|^2\le\mathscr D(f)\sum_{j=i}^Na_j^{-1}
 \le C_R\mathscr D(f)(i/N)^{-1/3},
 \qquad C_R=(12\pi b_*^4)^{-1}.                    \tag{32}
\]
Here \(\sum_{j=i}^\infty j^{-4/3}\le4i^{-1/3}\). Thus the weighted
mass of the superlevel set obeys
\[
 \sum_{|f_i|>u}V_i\le C_0\mathscr D(f)^3u^{-6},
 \qquad C_0=(M/\rho_*)C_R^3.                      \tag{33}
\]
For every cutoff amplitude \(u_0>0\), the layer-cake formula and the
additional bound \(\sum_{|f_i|>u}V_i\le\|f\|_1/u\) give
\[
 \|f\|_2^2
 \le2u_0\|f\|_1+\tfrac12C_0\mathscr D(f)^3u_0^{-4}.
\]
Choosing \(u_0^5=C_0\mathscr D(f)^3/\|f\|_1\) proves the all-mesh Nash
inequality
\[
 \|f\|_2^{10/3}\le
 C_N\mathscr D(f)\|f\|_1^{4/3},\qquad
 C_N=(5/2)^{5/3}C_0^{1/3}.                       \tag{34}
\]
The zero function is handled separately. No continuum Sobolev theorem or
unstated geometric regularity assumption enters (32)--(34).

Let \(A=-\mathcal L\) on this fixed graph and \(P(t)=e^{-tA}\). Positivity
and the elementary graph maximum principle imply weighted \(L^1\)
contraction. For \(v=P(t)f\), \(Y=\|v\|_2^2\), (34) gives
\[
 Y'=-2\mathscr D(v)
 \le-\frac2{C_N}\frac{Y^{5/3}}{\|f\|_1^{4/3}}.
\]
Integration, followed by selfadjoint duality, yields
\[
 \|P(t)\|_{1\to2}\le(3C_N/4t)^{3/4},\qquad
 \|P(t)\|_{2\to\infty}\le(3C_N/4t)^{3/4}.          \tag{35}
\]
In particular the constant is independent of \(N\).

Consider the regular leading-model system
\[
 w_s=k_2s^2\mathcal L(w+\alpha y),\qquad
 y_s=(w-y)/s,\qquad w(0)=y(0)=w_0,
 \quad \alpha=2(C_a-2)/C_a.                       \tag{36}
\]
Write \(\tau=k_2s^3/3\), \(a=(1+\alpha)/3\), \(b=1/3\), and let
\(\mu\) be the probability measure on \((0,1)\) proportional to
\(t^{a-1}(1-t)^{b-a}\,dt\). The exact operator formulas are
\[
 w(s)=\int_0^1(I-3t\tau A)e^{-t\tau A}w_0\,d\mu(t),\qquad
 y(s)=\int_0^1e^{-t\tau A}w_0\,d\mu(t).             \tag{37}
\]
For a direct verification put \(g(z)=\int e^{-zt}d\mu\) and
\(f=g+3zg'\). Integration of the derivative of
\(t^a(1-t)^{b+1-a}e^{-zt}\) gives
\(zg''+(z+b+1)g'+ag=0\). Hence
\(f'+f=-\alpha g\), \(3zg'=f-g\), and \(f(0)=g(0)=1\), exactly the
two spectral equations in (36). Finite-dimensional spectral calculus
then proves (37). The companion all-mesh note gives the same integral
representation independently.

Splitting the heat semigroup in half and using
\(\sup_{\lambda\ge0}|1-3q\lambda|e^{-q\lambda/2}\le1+6/e\), (35) gives
\[
 \|(I-3qA)e^{-qA}\|_{2\to\infty}
 \le2^{3/4}(1+6/e)(3C_N/4q)^{3/4}.                \tag{38}
\]
Therefore, if \(a>3/4\), both fields in (36) satisfy
\[
 \max\{\|w(s)\|_\infty,\|y(s)\|_\infty\}
 \le C_*\tau^{-3/4}\|w_0\|_2,\quad
 C_*=2^{3/4}(1+6/e)(3C_N/4)^{3/4}
                         \int_0^1t^{-3/4}d\mu(t)<\infty.        \tag{39}
\]
This is an explicit all-mesh \(L^2\)-to-pointwise bound, of order
\(s^{-9/4}\), for the full leading compression/density system.

For the specified activation,
\[
 a=1-\frac4{3C_a}>\frac34
 \quad\Longleftrightarrow\quad C_a>\frac{16}3.       \tag{40}
\]
The last inequality follows directly from the exact activation formula:
use \(\pi>31/10\), \(4^{1/3}>19/12\), and rational arithmetic to bound
\[
 C_a^2
 =9\,4^{2/3}\left[\frac1{16}+\frac{2\pi}3(4^{1/3}-1)\right]
 >\frac{361}{16}\left[\frac1{16}+\frac{31}{15}\frac7{12}\right]
 =\frac{329593}{11520}>\frac{256}9 .
\]
Thus the integral in (39) is finite for the actual coefficients, though
its constant is not small. At \(a=3/4\) this particular integral estimate
diverges; no impossibility theorem is inferred at that threshold.

This executes the pointwise continuation of the leading-model spectral
theorem. It does not yield a boundary-forced nonlinear estimate: the
model's singular time dependence prevents replacing arbitrary forcing by
the regular-data multiplier (37), and the actual heat and constitutive
remainders are still present. Equations (34)--(39) supply a legitimate
regularity building block rather than assuming the needed nonlinear
regularity conclusion.

## Precise remaining step and proof status

The derived lemmas remove two potential obstructions: the density
stiffness stays positive after the full local heat principal coupling,
and the actual-geometry heat/stress conductance ratio is uniformly
bounded. The leading density coupling has the dissipative gradient energy
(30), and its fixed-graph regular-data evolution has the all-mesh
pointwise smoothing estimate (39). These are new exact statements and do
not prove (UC).

What remains is a localized nonlinear energy extending (30), using (24),
which bounds (27), state-dependent weight time derivatives, and cutoff
work by its dissipation and a mesh-independent interior forcing norm.
It must then yield a discrete local pointwise estimate compatible with
(31), closing \(|x-x_d|<C_a-4\) on every cell intersecting the central
quarter. The exterior layer must enter through estimated cutoff work;
bounded boundary stress or a homogeneous postactivation extension cannot
be assumed.

No common \(T\), (NE), or unconditional entropy floor is proved in this
file. The specific missing work is the nonlinear coefficient and
pointwise closure, not positivity of the frozen principal eigenvalues.
This route remains open.

## Verification and provenance

All formulas were derived from the exact source and rechecked by
substitution and summation by parts. No external regularity theorem,
trajectory integration, finite-grid extrapolation, or numerical experiment
is load-bearing. No new grids were run. Self-review checked the
temperature factor three, heat density columns, edge Jacobian versus
local-gradient symbol, half outer node weight, branch divisions, the
ceiling in (UC), and the central scaling in (31). Mathematical
proofreading covered this new file only.

SHA-256 hashes, with input paths relative to stable_stress_search:

| Input | SHA-256 |
| --- | --- |
| collapse.py | 14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf |
| material.py | 4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390 |
| entropy_transport/convective_transport.py | ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97 |
| entropy_transport/transport.py | 2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c |
| entropy_transport/README.md | 8719a07f915902b829030d178636e27602f362c0f0b0e4e9e5d02039f575d2f6 |
| entropy_transport/DERIVATION.md | e08312d0dc3be7f3f2d225ca938a7872ceec6d4c2532db2102f54c7a984910da |
| entropy_transport/floor_theorem/STATUS.md | d05a94e8f701f0e1d5076dc9c3fbaf7468bb8b5822a493e64e275d867ae712f6 |
| entropy_transport/floor_theorem/seed_route.md | 752944eb3c0c7ff87007b5ca1c3f5a46bb768d8215645914ad6b211cebcd053d |
| entropy_transport/floor_theorem/startup_energy_route.md | 06630aecae84c9b618e84c1ddded3f2025f7a89f7dca634bbbb05f50d0e2380b |
