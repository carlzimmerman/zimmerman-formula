# Two-current common-frame principal modes

2026-10-15. MC-MODES-001. Conditional local extension, directly derived here;
self-reviewed, not an independent referee certificate. Base checkpoint
`5c06d239febe644b9f485477b4c2f93390a23b3e`.

**Result.** A common frame built from the actual total rest-mass current has a
healthy *principal-energy and propagating-cone* extension about a co-moving,
pure-electric state on an explicit finite-density domain. A second dust current
adds a positive-inertia relative zero mode; it does not force a new principal
ghost. Different pressures change the causal threshold to a harmonic effective
inertia and can add a coupled relative sound mode. Charges still set separate
finite-frequency plasma terms and species forces. This result supplies neither
an on-shell two-species static halo nor a covariant gravity/matter health theorem.

## 1. Constitutive choice and actual species

Use signature \(-+++\), \(c=1\), rationalized gauge units, two conserved number
currents \(J_a^\mu\), \(n_a=\sqrt{-J_a^2}>0\), and positive rest masses \(m_a\).
The candidate frame is the **chosen rest-mass-current frame**

\[
 K^\mu=m_1J_1^\mu+m_2J_2^\mu,\qquad
 U^\mu=K^\mu/\sqrt{-K^2}.
\]

It is varied with both currents. This is a constitutive assumption; it is not
derived from the portal or from a microscopic common medium. Rest-mass weights
are not charge weights, and they need not be energy/enthalpy weights away from
dust. Opposite charges would still enter \(K\) with positive mass weights.
The candidate matter action relevant for this calculation is

\[
 S_{\rm mat}=\int\sqrt{-g}\,d^4x\left\{
 \sum_{a=1}^2\left[-\epsilon_a(n_a)+J_a^\mu
  (\partial_\mu\vartheta_a+\alpha_a\partial_\mu\chi_a+q_aA_\mu)\right]
 +L_e(\mathcal E)-\tfrac12\beta(\mathcal E,n_1,n_2)\mathcal B^2
 \right\},
\]

with \(\mathcal E_\mu=F_{\mu\nu}U^\nu\),
\(\mathcal B_\mu=({}^\star F)_{\mu\nu}U^\nu\). Here \(\alpha_a,\chi_a\)
are Clebsch labels; \(\chi_1\) is not a particle identity. The species have
separate inertias \(h_a=n_a\epsilon'_a=\epsilon_a+P_a>0\) and sound squares
\(s_a^2=n_a\epsilon''_a/\epsilon'_a\in[0,1)\). No entrainment or mixed density
energy is postulated. A conversion action, if added, needs its own reciprocal
equations; it is not contained in the conservation Clebsch terms written here.

For the illustrative portal identification the actual inputs are
\(m_1=m_\chi=939.06542194\,\mathrm{MeV}\),
\(m_2=m_S=1\,\mathrm{MeV}\), and \(q_1=q_2=q\), so that
\((q_2/m_2)/(q_1/m_1)=939.06542194\). None of the following algebra replaces
these inertias by equal masses or these ratios by a common critical ratio.

Freeze coefficients at a point of a smooth co-moving background,
\(J_a=n_a(1,0,0,0)\), with \(\mathbf E=E\hat z\), \(\mathbf B=0\).
The background need not be spatially uniform. Its existence as a solution of
all species equations is an additional condition: unequal charge-to-mass ratios
generally obstruct simultaneous pressureless static force balance.
Write \(\mathbf v_a=\dot{\boldsymbol\xi}_a\) and

\[
 \rho_a=m_an_a,\quad \rho=\rho_1+\rho_2,\quad
 w_a=\rho_a/\rho,\quad \mathbf V=w_1\mathbf v_1+w_2\mathbf v_2.
\]

To first order, the varied frame velocity is \(\delta\mathbf U=\mathbf V\).
Variations of the weights affect its velocity only at second order; because the
pure-electric constitutive action has no term linear in frame velocity, they
do not add to the quadratic principal action. Density derivatives of \(\beta\)
also start at cubic order, since \(\mathcal B=0\) on this background.

## 2. Quadratic action with separate inertias

Keep the RTM electric law, so that

\[
 t=D/E=1-x,\quad p=dD/dE=(1-x)^2,\quad
 \Delta=t-\beta,\quad C=E\Delta,\quad a=E^2\Delta,
 \qquad 0<x<1.
\]

Direct contraction of \(F_{\mu\nu}U^\nu\) through second order gives

\[
 [\mathcal E^2]_2=|\mathbf e|^2+E^2V_\perp^2
                   +2E(V_xb_y-V_yb_x),\qquad
 [\mathcal B^2]_2=|\mathbf b|^2+E^2V_\perp^2
                   +2E(V_xb_y-V_yb_x).
\]

The electric square also has its background and linear terms; the brackets
denote only its quadratic coefficient. Expanding \(L_e\) with its longitudinal
Hessian \(p\) gives the principal Lagrangian

\[
\begin{split}
 L_2={}&\tfrac12p e_z^2+\tfrac12t(e_x^2+e_y^2)
       -\tfrac12\beta |\mathbf b|^2
       +C(V_xb_y-V_yb_x)+\tfrac12 a V_\perp^2\\
      &+\tfrac12\sum_a h_a|\dot{\boldsymbol\xi}_a|^2
       -\tfrac12\sum_a h_as_a^2
                   (\nabla\!\cdot\boldsymbol\xi_a)^2.
\end{split}                                                    \tag{1}
\]

This replaces the *frame velocity*, not the separate species inertia, by a
weighted average. Minimal charge coupling is of lower differential order in
the displacement/potential variables and is treated separately below.

For a unit wavevector \(k\), let \(T\) be a transverse orthonormal potential
basis, \(B_{\rm map}a=k\times(Ta)\), \(\varepsilon=\mathrm{diag}(t,t,p)\),
and \(R_b(b_x,b_y,b_z)^T=(b_y,-b_x,0)^T\). Eliminating the principal Gauss
constraint gives

\[
 K_A=T^T\left[\varepsilon-
  \frac{\varepsilon kk^T\varepsilon}{k^T\varepsilon k}\right]T
 \succeq pI_2.
\]

Use species-major order \((\xi_{1x},\xi_{1y},\xi_{1z},
\xi_{2x},\xi_{2y},\xi_{2z})\), \(H=\mathrm{diag}(h_1,h_2)\),
\(w=(w_1,w_2)^T\), and \(\Pi_\perp=\mathrm{diag}(1,1,0)\). The matrices are

\[
 \mathsf M=H\otimes I_3+a ww^T\otimes\Pi_\perp,\qquad
 \mathsf P=\mathrm{diag}(h_1s_1^2,h_2s_2^2)\otimes kk^T,
 \qquad
 \mathsf C=C\,w\otimes(R_bB_{\rm map}).                     \tag{2}
\]

For \(\beta>0\), \(\Delta>0\) these have positive kinetic matrices and
nonnegative potential matrices. With Fourier phases absorbing the spatial
derivative in \(\mathsf C\), the Hamiltonian is

\[
 H_2=\tfrac12\pi_A^TK_A^{-1}\pi_A+
 \tfrac12(\pi_\xi-\mathsf C A)^T\mathsf M^{-1}
                (\pi_\xi-\mathsf C A)
 +\tfrac12\beta|A|^2+\tfrac12\xi^T\mathsf P\xi\ge0.        \tag{3}
\]

This retains zero/vorticity displacement modes. The semidefinite potential
permits zero-frequency Jordan structure and polynomial displacement drift.

## 3. Exact all-angle cone condition for this co-moving family

Define the positive effective inertia

\[
 \boxed{\quad h_*=
 \left[\frac{w_1^2}{h_1(1-s_1^2)}+
       \frac{w_2^2}{h_2(1-s_2^2)}\right]^{-1}.\quad}         \tag{4}
\]

Since \(kk^T\preceq I_3\), set
\(H_{\rm eff}=\mathrm{diag}(h_1(1-s_1^2),h_2(1-s_2^2))\) to obtain

\[
 \mathsf M-\mathsf P\succeq H_{\rm eff}\otimes I_3
                       +a ww^T\otimes\Pi_\perp\succ0.
\]

The mixing image lies in the spatial perpendicular plane. The rank-one
inverse identity gives

\[
 w^T(H_{\rm eff}+a ww^T)^{-1}w=\frac1{h_*+a},\qquad
 \mathsf C^T(\mathsf M-\mathsf P)^{-1}\mathsf C
 \preceq\frac{C^2}{h_*+a}I_2.                              \tag{5}
\]

Here \(B_{\rm map}\) is an isometry and \(\|R_b\|\le1\). Thus the
light-cone Schur complement is positive if

\[
 f(\beta)=p-\beta-
 \frac{E^2(t-\beta)^2}{h_*+E^2(t-\beta)}>0.                \tag{6}
\]

For any squared phase speed \(z\ge1\), the gauge Schur complement divided
by \(z\) is

\[
 K_A-\frac\beta zI_2-
 \mathsf C^T(z\mathsf M-\mathsf P)^{-1}\mathsf C.
\]

It increases with \(z\), so strict positivity at \(z=1\) excludes every
propagating principal root with \(|c|\ge1\). The argument is valid for every
wavevector direction, rather than inferred by angular sampling.

The perpendicular sector \(k=\hat x\), \(A=A_z\), saturates (5) and
\(K_A=p\); hence (6) is also its exact light-cone discriminator. Write

\[
 h_{\rm crit}=\frac{E^2t(t-p)}p
              =D_0^2\frac{x^3}{(1-x)^2},\qquad R=h_*/h_{\rm crit}.
\]

On \(h_*>h_{\rm crit}\), one may choose the explicit response

\[
 \beta_L=p\frac{h_*-h_{\rm crit}}{h_*-E^2(t-p)}
        =p\frac{R-1}{R-(1-x)},\qquad
 \boxed{\ \beta=\beta_L\frac{R}{R+1}\ } .                 \tag{7}
\]

It obeys \(0<\beta<\beta_L<p<t\). Direct algebra gives
\(f(\beta_L)=0\) and
\(f'(\beta)=-h_*^2/[h_*+E^2(t-\beta)]^2<0\), proving (6).
If \(h_*\le h_{\rm crit}\), \(f(0)\le0\) and every \(0<\beta<t\) has
\(f(\beta)<0\). The perpendicular Schur function is then negative at
\(z=1\) and tends to \(p>0\) as \(z\to\infty\), so it has a
supermetric root. Thus this same constitutive family has a real two-current
threshold, not an unconditional health extension. The density-dependent
response (7) is engineered; neither its physical origin nor its continuation
off this finite-density pure-electric domain is supplied here.

## 4. Relative modes and exact perpendicular dispersion

Set \(W=w_1^2/h_1+w_2^2/h_2\) and \(h_c=W^{-1}\). For each spatial
component decompose \(v=h_cH^{-1}w V+r\), \(w^Tr=0\). Then

\[
 v^THv=h_cV^2+r^THr.
\]

The frame couples only to \(V\); the relative inertia stays positive. If
both species have the same sound square \(s^2\), this decomposition also
diagonalizes their pressure term: a relative sound mode has \(c^2=s^2\),
along with retained transverse zero/vorticity modes. For dust,
\(h_a=\rho_a\), \(h_c=h_*=\rho\) and the actual relative velocity
\(v_1-v_2\) has reduced inertia \(\mu=\rho_1\rho_2/\rho>0\):

\[
 \sum_a\rho_a|v_a|^2=\rho|V|^2+
            \frac{\rho_1\rho_2}{\rho}|v_1-v_2|^2.          \tag{8}
\]

Thus a second *co-moving background* dust species introduces a relative
zero-speed principal mode, not a forced principal ghost. This does not test
finite background relative streaming or two-stream instability.

For different sound squares, the perpendicular \(A_z,\xi_{1x},\xi_{2x}\)
sector has an exact cubic in \(z=c^2\). Let

\[
 d_a=h_a(z-s_a^2),\qquad S(z)=w_1^2d_2+w_2^2d_1.
\]

Then

\[
 \boxed{\quad
 (pz-\beta)[d_1d_2+zaS(z)]-zC^2S(z)=0 .\quad}             \tag{9}
\]

It follows by taking the determinant of the \(3\times3\) speed pencil with
fluid block \(z(H+a ww^T)-\mathrm{diag}(h_as_a^2)\) and off-diagonal block
\(cCw\). For equal sound square it factors as

\[
 h_1h_2(z-s^2)\left\{
 (pz-\beta)[(1+aW)z-s^2]-zC^2W\right\}=0.                \tag{10}
\]

For unequal sounds the relative pressure mode generally mixes with the frame
mode; positive energy and (4)–(7) still give the stated cone condition.
One cannot replace (4) by \((h_1+h_2)(1-s^2)\) for arbitrary weights and
unequal pressures. Removing species 2 before dividing by its inertia recovers
\(w_1=1\), \(h_*=h_1(1-s_1^2)\), and exactly the RTM single-fluid
perpendicular polynomial. Formula (9) with a finite decoupled spectator instead
factors that polynomial times \(h_2(z-s_2^2)\).

## 5. Charge and finite-frequency terms are a different calculation

Let \(Q_a=q_an_a\). Current perturbations are
\(\delta j_Q^i=\sum_aQ_av_a^i\) and
\(\delta j_Q^0=-\sum_aQ_a\nabla\cdot\xi_a\). Their quadratic minimal
coupling has one derivative in \((A,\xi)\), while the terms in (1) have two.
Gauss elimination therefore adds Coulomb/plasma terms at finite frequency;
it does not replace \(h_a\) by a charge-weighted mass in the principal pencil.

As a clean lower-order control, take \(k\parallel E\) and the longitudinal
electrostatic subsystem. It has \(\mathbf b=0\), no frame boost mixing, and
electric coefficient \(p\). Eliminating the electric potential gives

\[
 L_{\parallel}=\tfrac12\sum_a h_a|\dot\xi_a|^2
  -\tfrac12 k^2\sum_a h_as_a^2|\xi_a|^2
  -\frac1{2p}\left|\sum_aQ_a\xi_a\right|^2.               \tag{11}
\]

For dust, its exact squared frequencies are

\[
 \omega^2=0,\qquad
 \omega_p^2=\frac1p\left(\frac{Q_1^2}{h_1}+
                              \frac{Q_2^2}{h_2}\right)
            =\frac1p\sum_a\frac{q_a^2n_a}{m_a}.           \tag{12}
\]

The neutral displacement satisfies \(\sum_aQ_a\xi_a=0\). It need not be
the frame-relative displacement. Even if the background net charge vanishes,
the plasma scale generally remains. Formula (11) is a homogeneous local
electrostatic control; background gradients, gravity/Jeans terms and conversion
can change the full finite-wavelength spectrum. A large \(q_S/m_S\) can thus
matter greatly at finite frequency and for species force balance without
appearing as a new principal ghost in (1).

## 6. Reproduction, provenance and limits

The reusable script is [check_two_current.py](check_two_current.py). It uses
exact SymPy rational functions for tensor-boost identities, separate-inertia
decomposition, the direct cubic determinant, equal-sound factorization,
single-species control, rank-one inverse, threshold identities, dust reduction
and the electrostatic plasma polynomial. A separate exact rational grid checks
the actual \(2\times2\) light-cone Schur matrix at 72 backgrounds:

* \(D_0=1\), \(x\in\{1/10,1/2,9/10\}\), remnant rest-mass fraction
  \(\rho_2/\rho\in\{1/1000,1/2\}\);
* sound-square pairs \((0,0)\), \((1/10,1/3)\),
  \(h_*/h_{\rm crit}\in\{101/100,2\}\);
* unit directions \((k_x,k_z)=(0,1),(3/5,4/5),(1,0)\).

These are local EOS witnesses with \(h_a=m_an_a\) at the background point;
nonzero sound square is allowed by an EOS with \(P_a=0\) at that point and
positive \(\epsilon_a''\). This is not an inferred EOS over a halo.
The independent matrix construction tests first and determinant principal
minors in exact arithmetic; it does not calculate approximate eigenvalues.
The bounded grid is an implementation check, not the all-angle proof above.

The claim-supporting inputs are the immutable checkpoint copies
`../inputs/RTM_REPORT.md` (SHA256
`1940b17de6e270567b2c0a9d617b9fc2d34c6cfd7b7228153a649fa51d761046`),
`../inputs/JOIN_RESULT.txt` (SHA256
`9a174a71b55ba199b6ef6b2995f501be50c7179abe5422b6c16f958c2880ee92`), and
`../inputs/source_manifest.json`; the latter pins original source paths and
tracked/untracked status. The run additionally pins this proof and script.
See [computation_contract.json](computation_contract.json),
[run_exact/manifest.json](run_exact/manifest.json) and
[run_exact/results.json](run_exact/results.json). Actual command and software
versions are in the manifest. [REPRODUCE.txt](REPRODUCE.txt) gives the command.

**Exact remaining implication.** The admitted two-current candidate must still
supply an on-shell population/pressure/current background and its reciprocal
conversion dynamics. This proof covers only local principal propagation about
co-moving, pure-electric, occupied states with the stated diagonal barotropic
matter action. It does not establish strong hyperbolicity at zero modes,
nonlinear well-posedness, finite-drift health, a magnetic background, a vacuum
or interface completion, constrained Einstein/matter kinetic signs, remnant
retention, static galaxy law, lensing, production, cosmology or empirical
viability. A prescribed common frame alone supplies none of those missing
equations.
