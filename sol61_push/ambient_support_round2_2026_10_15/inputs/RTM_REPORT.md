# A reciprocal medium can support the proposed tether locally

2026-10-14. RTM-001. Constructed conditional mechanism; physical identification
and the full cold-energy programme remain open. Self-reviewed, not independently
refereed. Base revision cc8dec9c8d92e134e2eded18f5720d07e547ae3f.

The concrete advance is an explicit **current-rest-frame constitutive action**
whose pressureless static limit reproduces the retained tether, and whose
coupled fluid/gauge principal quadratic action has nonnegative energy and no
supermetric propagating characteristic on a stated pure-electric domain. The
all-angle argument below is analytic; 1,350 backgrounds provide implementation
checks, rather than a proof by sampling. This does not identify a new substance.

The proposed interaction is gravity plus a repulsive dark gauge force between
carriers. Baryons attract the carrier gravitationally; the carrier's field pushes
back. It is not a chemical bond to a special baryon. The action treats stars,
neutral hydrogen, molecular gas and hot gas through their gravitational stress;
it contains no vertex selecting a condensed phase. “Condensed baryon” is not an
identified particle in this mechanism. Any claimed exclusive source restriction
needs an additional interaction and evidence.

## 1. What changes relative to the previous obstruction

The retained [gauge-parent result](../cold_horizon_checkpoint_2026_10_14/input_snapshots/GAUGE_PARENT_RESULT.txt)
correctly ruled out its specified metric-causal, local Lorentz-scalar nonlinear
gauge embedding. It used a constitutive function of field invariants alone.
Ordinary minimal current coupling does not remove its supermetric principal
gauge mode. This work changes that hypothesis: electric and magnetic response
are defined relative to the **varied physical carrier current**, which adds
principal fluid/gauge mixing. It is not a correction obtained by adding ordinary
recoil to the same old action. Earlier commentary describing the old model as
merely freezing a medium was imprecise; its own cone calculation stands.

Covariant material-frame electromagnetic fluid actions are an established
framework; Gay-Balmaz, [arXiv:2511.18383v1, §§4.1–4.2](https://arxiv.org/html/2511.18383v1)
defines electric and magnetic fields with the fluid velocity and derives coupled
variational equations. That source supplies context, not the constitutive law,
threshold or proof constructed here. No novelty search or claim is made.

Use signature -+++, c=1 and rationalized gauge units. Let J^mu be an independent
timelike number current, n=sqrt(-J.J), U^mu=J^mu/n, and

\[
 \mathcal E_\mu=F_{\mu\nu}U^\nu,\qquad
 \mathcal B_\mu=({}^\star F)_{\mu\nu}U^\nu,
 \quad \mathcal E=\sqrt{\mathcal E_\mu\mathcal E^\mu}.
\]

A candidate matter action, added to Einstein gravity and neutral baryons, is

\[
 S_c=\int\sqrt{-g}\,d^4x\left[
 -\epsilon(n)+J^\mu(\partial_\mu\vartheta+
 \alpha\partial_\mu\chi+qA_\mu)
 +L_e(\mathcal E)-\tfrac12\beta(\mathcal E,n)\mathcal B^2\right].
\]

The Clebsch fields impose conservation and allow local vortical flow. Both
J and A are varied; U is never an imposed external frame. q denotes particle
charge; beta denotes magnetic response, not a Clebsch field. Choose charge
orientation so that like carrier charges repel. A covariant action gives
reciprocal stress exchange on its equations, but writing it does not establish
global solutions, a finite interface or a healthy microscopic completion.

Take a barotropic fluid with h=epsilon+P=n epsilon_n>0 and
s²=dP/d epsilon=n epsilon_nn/epsilon_n in [0,1). Dust has epsilon=mn and h=mn.
For a local finite-sound-speed witness at n=n0 one may use
epsilon=mn+m s0²(n-n0)²/(2n0); it has P(n0)=0, h(n0)=mn0 and s²(n0)=s0².
This is a local EOS example, not an inferred equation of state over a galaxy.

## 2. Why it tethers in the pressureless Newtonian limit

Preserve the electric constitutive function

\[
 L_e(E)=D_0 E-D_0^2\ln(1+E/D_0),\quad
 D=L'_e(E)=\frac{E}{1+E/D_0},\quad
 E=\frac{D}{1-D/D_0}.
\]

Its electric Hamiltonian is H(D)=D0²[-x-ln(1-x)], x=D/D0 in (0,1).
Assign zeta=q/m=sqrt(4 pi G) and D0=a0/zeta, as in the retained comparison.
Spherical Gauss law counts actual charged carrier rest mass:

\[
 D=\frac{\zeta M_c(<r)}{4\pi r^2},\quad
 u=\zeta D=\frac{GM_c(<r)}{r^2}.
\]

On a rest, purely electric background, the beta B² term and its first
variations vanish. There is no density dependence in Le. The pressureless
static force is therefore unchanged at leading Newtonian order:

\[
 a_r=-(g_b+u)+\zeta E
     =-g_b+\frac{u^2}{a_0-u}.
\]

Thus a carrier at rest can balance where gb=u²/(a0-u). Neutral baryons feel
g=gb+u; eliminating u gives gb=g²/(g+a0), the intended static law. Both the
critical charge/mass ratio and Le were **assigned to construct this behavior**.
They are not explained by the action. Nonzero pressure changes the equilibrium;
the wave checks at finite s² do not certify that this same dust density remains
a global warm-fluid halo solution. Field energy and pressure also gravitate;
this calculation is a leading weak-field rest-mass comparison, not an exact
Einstein solution. No relaxation or capture into this profile is established.

## 3. Recoil supplies a real constraint

Freeze coefficients at a point of a slowly varying rest background E z-hat,
B=0. A literally uniform electric field with nonzero uniform charge would
violate Gauss law; it is not the background solution being asserted here.
Let e,b be field
perturbations and v=dot(xi) the carrier velocity perturbation. Define

\[
 t=D/E=1-x,\quad p=dD/dE=(1-x)^2,\quad
 \Delta=t-\beta,\quad C=E\Delta,\quad M=h+E^2\Delta.
\]

The exact Lorentz transformations through quadratic order give the principal
quadratic Lagrangian

\[
\begin{split}
 L_2={}&\tfrac12 p e_z^2+\tfrac12t(e_x^2+e_y^2)
       -\tfrac12\beta b^2+C(v_xb_y-v_yb_x)\\
      &+\tfrac12M(v_x^2+v_y^2)+\tfrac12h v_z^2
       -\tfrac12 h s^2(\nabla\cdot\xi)^2 .
\end{split}
\]

In particular E_rest² contributes E² v_perp² and
2 E(v_x b_y-v_y b_x); B_rest² contributes the same boost terms. These
reciprocal inertia and mixing terms cannot be discarded. beta's derivatives
start at cubic order around B=0, so do not enter this quadratic principal test.
Minimal charged-current terms, background gradients and gravitational Jeans
terms have lower derivative order and are not certified by this wave test.

Simply choosing beta=p makes the frozen-fluid selected wave luminal, but
the coupled perpendicular dust wave instead has

\[
 c_{\perp}^2=\frac{\beta+C^2/M}{p}>1\quad(\beta=p, E>0).
\]

For finite pressure its coupled pair has z=c² satisfying

\[
 (pz-\beta)(Mz-hs^2)-C^2z=0.
\]

Requiring its fast branch to fit inside the metric cone with positive beta
imposes the local inertial threshold

\[
 h_{\rm eff}=h(1-s^2)>h_{\rm crit},\qquad
 h_{\rm crit}=\frac{E^2t(t-p)}p
              =D_0^2\frac{x^3}{(1-x)^2}.
\]

At equality the available positive magnetic-response window closes. This
threshold concerns this constitutive family; it is not a universal theorem
about every possible carrier theory.

## 4. An explicit response law and an all-angle proof

On the open domain R=h_eff/hcrit>1, choose

\[
 \beta_L=p\frac{h_{\rm eff}-h_{\rm crit}}
                   {h_{\rm eff}-E^2(t-p)}
       =p\frac{R-1}{R-(1-x)},\qquad
 \boxed{\ \beta=\beta_L\frac{R}{R+1}\ }.
\]

This is one engineered material response, not one derived from a measured
material or fundamental carrier. It obeys 0<beta<betaL<p<t and approaches
Maxwell beta=1 as E goes to zero at fixed positive h_eff. That fixed-density
limit does not supply a joint zero-density vacuum limit.

Here is the proof for every wavevector direction. Set |k|=1, let T be any
orthonormal transverse potential basis, epsilon=diag(t,t,p), and eliminate
the nondynamical electric potential by Gauss law. The physical electric
kinetic matrix is

\[
 K_A=T^T\left[\varepsilon-
  \frac{\varepsilon k k^T\varepsilon}{k^T\varepsilon k}\right]T
 \succeq pI.
\]

For the inequality, minimize (Ta+k phi)^T epsilon(Ta+k phi) over phi;
it is at least p|a|². Let Bmap a=k cross(Ta), an isometry on the two
transverse amplitudes. Define

\[
 \mathsf M=\mathrm{diag}(M,M,h),\quad
 \mathsf P=hs^2 k k^T,\quad
 \mathsf C=E\Delta\begin{pmatrix}
 (B_{\rm map})_y\\-(B_{\rm map})_x\\0
 \end{pmatrix}.
\]

Because k k^T <= I,

\[
 \mathsf M-\mathsf P\succeq
 \mathrm{diag}(h_{\rm eff}+E^2\Delta,
 h_{\rm eff}+E^2\Delta,h_{\rm eff})\succ0,
\]

and consequently

\[
 \mathsf C^T(\mathsf M-\mathsf P)^{-1}\mathsf C
 \preceq\frac{E^2\Delta^2}{h_{\rm eff}+E^2\Delta}I.
\]

At c=1 the gauge Schur complement is strictly positive if

\[
 f(\beta)=p-\beta-
 \frac{E^2(t-\beta)^2}{h_{\rm eff}+E^2(t-\beta)}>0.
\]

Direct algebra gives f(betaL)=0 and
f'(beta)=-h_eff²/[h_eff+E²(t-beta)]²<0. Our beta<betaL therefore gives
strict positivity. For any c>=1 the Schur complement divided by c² is

\[
 K_A-\frac{\beta}{c^2}I-
 \mathsf C^T(c^2\mathsf M-\mathsf P)^{-1}\mathsf C.
\]

It increases in matrix order with c², so cannot acquire a zero eigenvalue
outside the metric cone. This is not an angular interpolation assumption.

The same reduced quadratic system has Hamiltonian (unit wave number, with
Fourier sine/cosine phases chosen to absorb the spatial derivative in C)

\[
 H_2=\tfrac12\pi_A^T K_A^{-1}\pi_A+
 \tfrac12(\pi_\xi-\mathsf C A)^T\mathsf M^{-1}
                   (\pi_\xi-\mathsf C A)
 +\tfrac12\beta A^T A+\tfrac12\xi^T\mathsf P\xi\ge0.
\]

The fluid zero/vorticity displacement modes are retained, not counted as
additional light waves. The potential is semidefinite, so displacement zero
modes can have Jordan structure and polynomial drift. Positive local principal
energy is not a proof of strong hyperbolicity in all variables, global nonlinear
wellposedness, absence of dust caustics, finite-wave-number stability or a
complete matter-plus-Einstein stability theorem. Magnetic backgrounds and a
vacuum interface require new calculations.

## 5. A geometric crossover, with its scope exposed

For an ideal point baryon mass M, define rM=sqrt(GM/a0) and rg=2GM/c².
The proposed static dust profile has

\[
 x(r)=\frac{2}{1+\sqrt{1+4r^2/r_M^2}},\qquad
 \rho_c=\frac{a_0}{2\pi G r\sqrt{1+4r^2/r_M^2}},
\]

while the threshold mass density is

\[
 \rho_{\rm crit}=\frac{a_0^2}{4\pi Gc^2}
                    \frac{x^3}{(1-x)^2}.
\]

Near the source rho_c grows as 1/r, but rho_crit grows as 1/r^4.
The ideal profile therefore leaves this causal-medium domain in the interior.
Its leading crossing radius obeys

\[
 \boxed{\ r_{\rm gate}^3=\frac{G^2M^2}{2a_0c^2}
                      =\frac{r_g r_M^2}{4}\ }.
\]

If one **additionally assigns**, rather than derives, a0=alpha c²/L, then
r_gate³=rg² L/(8 alpha). This is a conditional dimensional connection between
the source length and the supplied cosmic acceleration length. It does not
derive a horizon coupling, dark energy or the numerical alpha. rg is a formal
mass length here; an extended galaxy is not a black hole of its total mass.

Using a0=9.360324825e-11 m/s² for illustrative source masses:

| Ideal point source | Exact rho_c=rho_crit radius | Leading cubic radius | rM |
|---|---:|---:|---:|
| 4 million solar masses | 0.082918675 pc | 0.082918579 pc | 77.1785 pc |
| 60 billion solar masses | 50.434191 pc | 50.432755 pc | 9452.3981 pc |

These are model examples, not measurements of specific systems or black-hole
environment predictions. The crossing was calculated without solving gravity
with the full field stress or matching a relativistic core; it cannot replace
those calculations. An extended Plummer baryon source of 60 billion
solar masses and 3-kpc scale passes rho_c/rho_crit>1 over the tested 401 radii
0.001–1,000,000 pc; its minimum ratio is 1.047371e6. The point-source inner
failure is therefore not a theorem that every extended halo has a 50-pc gap.
The ideal outer profiles still have infinite carrier mass without an edge.

## 6. What was actually checked

The canonical [results](run_v2/calculation/results.json) contain 2,148 named
assertions: constitutive and boost identities; the force cancellation and
threshold algebra; 1,350 coupled principal backgrounds; independent dust
dispersion and finite-pressure perpendicular polynomial checks; exact
point-density algebra, two crossing roots and 401 Plummer domain samples.

The grid varies x=.01,.1,.5,.9,.99, R=1.01,2,10,1000,1000000,
s²=0,1e-6,.001,.01,.1,1/3 and nine angles. Its maximum speed is
0.9999995000013732 c; minimum light-cone Schur eigenvalue is
9.9999799e-11 and minimum kinetic eigenvalue is 1.0305071e-6 in the stated
normalization. Independent dispersion errors are <=2.34e-15. Maximum absolute
real numerical eigenvalue is 1.3361e-8 from the retained zero-mode structure;
this is disclosed numerical roundoff, not proof of an instability or of its
absence at finite wavelength.

The first canonical run failed an inappropriate absolute eigenvalue tolerance
on a positive rank-one pressure block of norm 4.85e9. The returned negative
eigenvalue was a relative -1.12e-16. v2 changes only that check to a norm-relative
1e-14 tolerance; it retains every case and the physical limits. Original code,
contract, logs and failure manifest remain intact. Both manifests validate
against the retained input and output hashes. See
[numerical correction](NUMERICAL_CORRECTION.txt) and [reproduction](REPRODUCE.txt).

## 7. Physical verdict

This route supplies a conditional answer to **how a reciprocal tether could
work**: neutral matter's gravity attracts a charged cold medium; a nonlinear
dark electric response opposes collapse; the medium's varied rest frame permits
a separate magnetic response, and sufficient material inertia allows local
waves to remain inside the metric cone. It gives an explicit algebraic window
and a finite-density failure boundary instead of hiding recoil.

It does not show that nature contains this carrier or response law. In
particular:

* No microscopic calculation selects beta, Le, q/m, a0 or the EOS.
* No baryon-phase interaction, assembly/cooling rate, finite halo edge or
  empirical fit has been derived. Static balance is not an attractor theorem.
* One-sign carrier supply still needs charge-neutral production, opposite
  charge/compensation or domains; a homogeneous FRW background cannot simply
  carry an uncompensated homogeneous gauge charge.
* The curvature-generated real neutral scalar studied previously has not
  been converted into these charged carriers. Pair creation, energy transfer
  and the fate of the opposite charge are missing physical equations.
* The action is defined on a timelike-current, finite-density admissible
  domain. No smooth zero-current vacuum, complete magnetic branch, inner
  black-hole solution or cosmological solution has been supplied.
* Cold rest matter with P approximately zero is not dark energy with
  P approximately minus epsilon. A common phase-changing microscopic parent
  and reciprocal exchange budget remain absent. The cubic length relation
  above does not create such a parent.

The local construction advances one previously blocked route; it does not
close the cold-energy/black-hole/dark-energy/horizon programme.
