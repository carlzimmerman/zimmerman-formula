# Four derivation chains from Astra

October 8, 2026. Base c05c824e4ac70335e811242df2250526d18983ae. Source hashes and the read-only ownership boundary are in source_manifest.json. These are new combinations relative to the reviewed project records, not a global novelty claim.

The strongest constructive result is a solvable threshold Hamiltonian with a positive three-halves response, together with a bounded gauge-invariant candidate source for investigating the BFSS connection. The BFSS response spectrum has not been calculated. Three further chains transfer Astra's scale response into the actual MONO kernel, include the previously fixed heat scale in the vacuum variation, and turn its static Schur criterion into a retarded response with a bounded slow-mode frequency.

The operative gravity target remains filtered MONO, criterion B, two gravitational polarizations with any matter/clock modes explicitly counted, and independently derived metric potentials. Deep MOND alone is insufficient. None of the chains derives \(k=1/2\), fixes measured versus bare \(G\), or completes the relativistic theory.

## 1. Threshold spectrum to deep MOND

### Starting point and mathematical construction

The inspected [OpenAI BFSS manuscript](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-unique-threshold-bound-state-of-the-SU-N-BFSS-model-September-24-2026/paper.pdf) asserts a unique normalizable zero-energy state for the relative SU(N) model, with continuous spectrum beginning at zero. That theorem has not been independently audited here. It motivates asking for an operator's response spectrum, not treating the state as a positive cosmological constant.

A discrete state coupled to a continuum is an established Friedrichs-type construction, not a newly invented quantum model; see [Xiao and Zhou](https://arxiv.org/abs/1608.00468v2) and [Lakaev and Kurbanov](https://arxiv.org/abs/2004.08815). The following specific calculation is self-contained and does not import their different models' theorems.

Use dimensionless variables on
\[
\mathcal H=\mathbb C|0\rangle\oplus
\big[L^2((0,L),dE)\otimes\mathbb C^3\big].
\]
Let \(H_0|0\rangle=0\), and let \(H_0\) multiply each continuum component by \(E\). For a real vector source \(\mathbf D\), define
\[
H(\mathbf D)=H_0-\sum_iD_i
\big(|0\rangle\langle v,i|+|v,i\rangle\langle0|\big),
\qquad |v(E)|^2=C E^\beta,\quad -1<\beta<0.
\]
The coupling is bounded because \(v\in L^2\). Thus this is a self-adjoint Hamiltonian bounded below for every finite \(\mathbf D\). Only the continuum component parallel to \(\mathbf D\) mixes; the response depends on \(D=|\mathbf D|\).

Writing its negative eigenvalue as \(-\epsilon\), direct elimination of the continuum wavefunction gives
\[
\epsilon=D^2 I(\epsilon),\qquad
I(\epsilon)=C\int_0^L\frac{E^\beta}{E+\epsilon}\,dE.
\]
The right-hand side decreases strictly with \(\epsilon>0\), diverges at zero, and tends to zero at infinity. There is exactly one negative root and therefore a unique ground state for \(D>0\). Its continuum component \(D v(E)/(\epsilon+E)\) is square-integrable. The assertion does not exclude eigenvalues above the continuum.

Substitute \(E=\epsilon x\). For \(-1<\beta<0\),
\[
I(\epsilon)\sim C J_\beta\epsilon^\beta,\qquad
J_\beta=\int_0^\infty\frac{x^\beta}{1+x}\,dx
=\frac{\pi}{\sin[\pi(\beta+1)]}.
\]
Consequently
\[
\boxed{\epsilon(D)\sim
(C J_\beta)^{1/(1-\beta)}
D^{\,2/(1-\beta)}.}
\]
The desired three-halves power occurs precisely at
\[
\boxed{\beta=-\frac13,\qquad
\epsilon(D)\sim A D^{3/2},\qquad
A=\left(\frac{2\pi C}{\sqrt3}\right)^{3/4}.}
\]
The source coupling is linear in the vector \(\mathbf D\); the fractional power comes from eliminating the continuum, rather than placing a fractional power directly in the source term.

Differentiating the exact root equation gives
\[
\epsilon'(D)=\frac{2\epsilon/D}
{1+D^2 C\int_0^L E^\beta/(E+\epsilon)^2\,dE}.
\]
The integral term in the denominator tends to \(-\beta\) as \(D\to0\). Hence
\(\epsilon'\sim [2/(1-\beta)]\epsilon/D\); the response asymptote below follows from this identity, not from an unjustified differentiation of an asymptotic equivalent.

For this exponent, the finite-cutoff correction has an explicit bound. If \(\epsilon_0=A D^{3/2}\), then
\[
0<\epsilon_0-\epsilon
\le 3C L^{-1/3}D^2.
\]
Indeed \(0<I_\infty-I<3C L^{-1/3}\); the increasing function
\(F(e)=e-D^2I_\infty(e)\) has \(F'\ge1\), with
\(F(\epsilon_0)=0\) and \(F(\epsilon)=-D^2(I_\infty-I)\).

### Constitutive map and its limits

Ground energy is concave as a function of a linear source. Hence \(\epsilon=-E_{\rm ground}\) is convex. With a positive conversion factor \(\eta\), use the candidate auxiliary potential
\[
\mathscr H(D)=\frac{D^2}{2}+\eta\epsilon(D).
\]
In a first-order static gravity action containing
\(\mathscr H(\mathbf D)-\mathbf D\cdot\nabla\Phi\), source variation gives
\(\mathbf g=\nabla_{\mathbf D}\mathscr H\), while potential variation gives the source-divergence constraint. This fixes the sign: the positive response is minus the ground energy, not the ground energy itself.

The deep relation is
\[
g\sim\frac{3\eta A}{2}\sqrt D,\qquad
g^2\sim a_{\rm toy}D,\qquad
a_{\rm toy}=\frac94\eta^2
\left(\frac{2\pi C}{\sqrt3}\right)^{3/2}.
\]
With the independently calibrated spherical source law \(D=GM_b/r^2\), this has the deep-MOND form. Restoring physical units requires specifying the conversion of the matrix energy and source to \(\mathscr H\) and gravitational flux; those conversion constants are not predictions.

For finite \(L\), the high-source response is asymptotically linear in \(D\) before adding \(D^2/2\), since \(I(\epsilon)\sim\|v\|^2/\epsilon\). Thus the added Newtonian term dominates at high \(D\). **This is not the exact MONO, RAR or P2 interpolation.** Replacing those kernels with this response changes the model.

### A bounded BFSS source and the decisive unresolved step

The naive relative-SU(N) coupling \(\operatorname{Tr}X_i\) vanishes identically. A cubic vector \(\operatorname{Tr}(X_i\sum_jX_j^2)\) need not vanish for \(N\ge3\), but grows cubically along commuting flat directions and is unsuitable as an unrestricted linear perturbation without stabilization.

A concrete bounded alternative is
\[
R^2=\sum_jX_j^2,\qquad q=\operatorname{Tr}R^2,\qquad
\boxed{O_i(X)=
\frac{\operatorname{Tr}(X_iR^2)}
{(\ell^2+q)^{3/2}},\quad\ell>0.}
\]
It is gauge invariant and transforms as a Spin(9) vector. Hilbert-Schmidt Cauchy-Schwarz gives
\[
\sum_i[\operatorname{Tr}(X_iR^2)]^2
\le q\,\operatorname{Tr}(R^4)\le q^3,
\]
so \(|\mathbf O|\le1\). The multiplication perturbation
\(-\mathbf D\cdot\mathbf O\) is bounded and \(H_0-\mathbf D\cdot\mathbf O\ge-D\). This removes the flat-direction runaway at the operator level. It introduces the positive matrix scale \(\ell\); its value and physical coupling must be justified. The operator vanishes for SU(2), since each traceless Hermitian \(2\times2\) matrix squares to a scalar matrix. SU(3) is the first nontrivial case.

For a rotationally invariant zero state, \(\langle O_i\rangle=0\). The relevant measure is the **operator-weighted spectrum**
\[
d\mu_i(E)=\langle0|O_i Q\,dP_{H_0}(E)\,QO_i|0\rangle,
\qquad Q=1-|0\rangle\langle0|,
\]
not the total density of states. It has finite total mass because \(O_i\) is bounded. The toy model suggests testing whether its density behaves as \(E^{-1/3}\).

There is an equally important second gate. In BFSS the exact projected resolvent contains
\[
QH_0Q-D\,QOQ+\epsilon,
\]
not merely \(QH_0Q+\epsilon\). The toy source was chosen with \(QOQ=0\). A measured \(E^{-1/3}\) unperturbed spectrum alone would therefore not establish the result; the continuum-to-continuum coupling must vanish or be controlled in the relevant scaling limit. Since \(D\) is larger than \(D^{3/2}\) at small \(D\), it cannot simply be discarded.

**Next discriminating calculation:** derive the separated-cluster low-energy asymptotics of this bounded SU(3) vector's matrix elements and of \(QOQ\), retaining the physical source normalization. A regular free nine-dimensional channel has density of states proportional to \(E^{7/2}\); obtaining \(E^{-1/3}\) would require a singular form factor, so the exponent is a serious test, not a generic consequence of a threshold state. The BFSS theorem supplies none of this spectrum automatically.

## 2. MONO response to a vacuum source and a halo mass moment

This transfers the scale-work idea of Astra FGF010/FGF033 from their Q/R diagnostic to a separately varied filtered-MONO static functional. It does not transfer their time-dependent action.

Let \(S_t=e^{t\Delta}\), \(t=\xi^2/2\), \(v=\nabla S_tu\), \(b=|v|\), \(y=b/a\), and
\[
h(y)=y[\nu_{\rm mono}(y)-1],\quad
H(y)=\int_0^y h(s)\,ds,\quad U(b,a)=a^2H(b/a).
\]
On a fixed flat periodic domain, or with variations and boundary conditions eliminating the actual boundary terms, the static functional
\[
I=\frac1{8\pi G}\int
\big[2\nabla\Phi\cdot\nabla u-|\nabla u|^2-2U(|\nabla S_tu|,a)\big]\,d^3x
+\int\rho_b\Phi\,d^3x
\]
gives
\[
\Delta u=4\pi G\rho_b,\qquad
\Delta\Phi=\Delta u+S_t^*\nabla\cdot
[(\nu_{\rm mono}-1)\nabla S_tu].
\]
Thus the outer adjoint and source convention are retained. The boundary assumptions are essential; a periodic Poisson source must have zero mean after any prescribed background subtraction.

The scale-work density at fixed filtered field is
\[
\boxed{T(b,a)=\partial_{\ln a}U
=a^2[2H(y)-yh(y)].}
\]
Its dimensionless derivative is \(h-yh'\). On the RAR segment,
\[
h-yh'=\frac{y^{3/2}e^{\sqrt y}}
{2(e^{\sqrt y}-1)^2}>0.
\]
On the continuation, \(h=h_*+B\log[(y+y_p)/(y_*+y_p)]\), \(B=\delta h_p>0\). There \(d(h-yh')/dy=B y/(y+y_p)^2>0\), and the joined value is already positive. Since \(T(0,a)=0\), **\(T>0\) for every nonzero filtered field on both segments**.

In the static functional, \(\partial_{\ln a}I_{\rm field}=-(4\pi G)^{-1}\int T\). In the corresponding static Lagrangian the sign reverses. A promoted scale coordinate therefore needs an actual balancing equation; a field-independent vacuum minimum cannot silently absorb this source.

The deep expansion gives \(T\sim a^{1/2}b^{3/2}/3\). For an isolated point-source exterior at fixed finite filter length, \(b\sim GM_b/r^2\), and a common far annulus gives
\[
\boxed{\frac1{4\pi G}\int_{\rm annulus}T\,d^3x
\sim\frac{\sqrt a\,(GM_b)^{3/2}}{3G}
\log\frac{R}{r_{\rm in}}.}
\]
This is a **mass-three-halves moment**, not total baryonic mass. At the same far-annulus logarithm, combining two equal masses changes that leading contribution by a factor \(\sqrt2\) relative to the sum of two isolated contributions. This compares asymptotic configurations, not a merger evolution or an additive near-field formula for overlapping halos.

The logarithm requires environmental/outer matching. A single isolated contribution divided by an arbitrarily large volume tends to zero; the expression is not a predicted homogeneous dark-energy density. The new obligation is to derive the population, boundary and renormalization map before claiming that galaxy response selects a universal vacuum value.

## 3. Heat smoothing to a joint vacuum-scale identity

The MONO excess potential is strictly convex in the vector \(v\), because its transverse and radial Hessian eigenvalues are \(h/y>0\) and \(h'>0\) away from zero. At zero the potential is continuous and convex, although its Hessian need not be bounded.

Let
\[
\mathcal E(t,a)=\int U(|e^{t\Delta}v_0|,a)\,d^3x.
\]
On a flat torus, heat convolution is averaging by a positive probability kernel. Jensen's inequality and preservation of volume give
\[
\mathcal E(t+s,a)\le\mathcal E(t,a).
\]
This proof includes zeros of the field and does not assume bounded Hessian there. Away from zeros, ordinary integration by parts gives the stronger identity
\[
\partial_t\mathcal E=-\mathcal D,\qquad
\mathcal D=\int\sum_j
(\partial_jv)^T U_{vv}(\partial_jv)\,d^3x\ge0.
\]
This is monotonicity in an auxiliary smoothing parameter, **not physical dissipation or a proof of time evolution**. It does not say the physical force decreases pointwise.

Now tie \(a=a_{\rm ref}e^\lambda\) and \(\xi=\xi_{\rm ref}e^{-p\lambda}\), \(p\ge0\), keeping geometry and unfiltered \(u\) fixed. Since \(t\propto\xi^2\),
\[
\boxed{\frac{d\mathcal E}{d\lambda}
=\int T\,d^3x+2pt\,\mathcal D>0}
\]
for a nontrivial field where the derivative formula applies. The finite-difference monotonicity survives the zero-field issue: increasing \(a\) raises \(U\), while decreasing the heat time raises its integral.

In particular, a proposed horizon-scale relation \(\xi\propto c^2/a\) corresponds to \(p=1\). The two scale variations reinforce each other. **Allowing the filter to respond does not cancel Astra's scale source for this inverse relation.**

The opposite relation \(\xi\propto a^p\) gives \(\int T-2pt\mathcal D\), so cancellation is possible in principle but depends on spatial gradients and source geometry. A universal coefficient would then require a new theorem relating those functionals across sources. An independent vacuum potential, a curved/lapse-dependent filter or a state-dependent domain changes the variation and must be included explicitly.

## 4. Astra's static Schur bound to a causal memory law

Use only an actual equilibrium and coercive fixed-reference form admitted by FGF033, on its original fixed-wall, fixed-mass domain. It is a diagnostic Q action with an additional global coordinate, not the operative MONO theory.

In mass-normalized coupled bath modes, its quadratic Lagrangian has the form
\[
L_2=\frac12\sum_j(\dot q_j^2-\omega_j^2q_j^2)
+\frac I2\dot\lambda^2-\frac\kappa2\lambda^2
-\lambda\sum_jg_jq_j.
\]
Assume positive bath frequencies and convergent sums below. Astra's static criterion is
\[
\kappa>S,\qquad S=\sum_jg_j^2/\omega_j^2.
\]
Solving the bath initial-value problem and substituting into the global equation gives the exact retarded inverse response
\[
\boxed{D_R(\omega)=\kappa-I(\omega+i0)^2
-\sum_j\frac{g_j^2}{\omega_j^2-(\omega+i0)^2}.}
\]
Equivalently,
\[
I\ddot\lambda+(\kappa-S)\lambda
+\int_0^\tau K(\tau-s)\dot\lambda(s)\,ds
=f_{\rm bath}(\tau)-K(\tau)\lambda(0),
\quad
K(\tau)=\sum_j\frac{g_j^2}{\omega_j^2}\cos(\omega_j\tau).
\]
Here \(f_{\rm bath}=-\sum_jg_j q_{j,\rm free}\), plus any externally specified forcing. The initial term is necessary. This finite conservative bath can recur; the cosine kernel is not pointwise positive friction and no irreversible damping is inferred.

Let \(b\) be the smallest squared frequency of a coupled bath mode. For finite discrete baths with a nonzero coupling at \(b\), the lowest coupled squared frequency \(z_*\) obeys
\[
z_-\le z_*<\min\left(b,\frac{\kappa-S}{I}\right),
\]
\[
z_-=
\frac{\kappa+Ib-\sqrt{(\kappa+Ib)^2-4Ib(\kappa-S)}}{2I}.
\]
Proof: below \(b\), \(D(z)=\kappa-Iz-\sum g_j^2/(\omega_j^2-z)\) strictly decreases from positive to negative infinity. Also
\[
S<\sum_j\frac{g_j^2}{\omega_j^2-z}
\le\frac{S}{1-z/b}.
\]
The two bounds give the stated bracket. Any uncoupled lower bath modes must be considered separately.

Near the static stability threshold,
\[
z_*\sim\frac{\kappa-S}{I+\sum_jg_j^2/\omega_j^4}.
\]
This predicts a soft collective response rather than the bare driver rate \(\sqrt{\kappa/I}\). A cosmological scale cannot be assumed to follow its equilibrium instantaneously near that threshold. Translating the mode to redshift or seconds still requires the actual physical kinetic coefficients and background.

## What is new here and what is inherited

| Chain | Inherited input | Added result | First unresolved physical step |
|---|---|---|---|
| Threshold | BFSS threshold-state claim; familiar discrete-continuum Hamiltonians | Exact \(E^{-1/3}\to D^{3/2}\) construction, cutoff bound and bounded SU(3) vector candidate | Actual operator-weighted BFSS spectrum and continuum coupling |
| Vacuum source | FGF010/033 scale-work logic | Separate MONO variation, strict source sign and exterior mass-three-halves moment | Covariant vacuum/population/boundary matching |
| Joint scale | Operative heat filter and monotone phantom kernel | Nonlinear smoothing inequality and exact inverse-scale reinforcement | Full metric/lapse/domain variation and vacuum balance |
| Memory | FGF033 coercive Hessian and static Schur bound | Retarded kernel, retained initial term and slow-mode bracket | Matching physical action, equilibrium and kinetic normalization |

Searches compared these chains against Astra's current checkpoint, FGF010/033, the 2,000-task index, and the existing Sol61 critical-response, spectral-tail and vacuum-selection reports. Earlier positive-Laplace/Stieltjes results concern acceleration constitutive measures and do not establish a quantum energy-threshold spectrum. The threshold toy is also distinct from the earlier sextic commuting-spinor construction. No exhaustive repository-wide or worldwide novelty claim is made.

The priority is the threshold-spectrum chain because it offers a microscopic origin for the response power with a concrete spectral falsifier. Its normalization remains proportional to independent \(C\), \(\eta\) and the physical source conversion. No count of BFSS zero modes or tensor polarizations fixes those numbers to give \(32\pi^2\).

## Evidence and handoff

The checks use actual MONO joins, two periodic resolutions for heat identities, independent oscillator eigenvalues and history integration, exact incomplete-beta resolvents, and independent threshold quadrature. All physical examples are dimensionless; the results apply to either adopted acceleration footing after its own unit conversion.

The first threshold implementation lost precision by evaluating an incomplete-beta function at an argument almost equal to one. A 60-digit comparison isolated that error. The corrected complementary-argument implementation is a separate file and run; the original failed records remain intact. Final validation and counts are in VALIDATION.md. These are self-reviewed derivations, not independent-agent audits.

Next work should compute or bound the BFSS spectral exponent and \(QOQ\) for the explicit bounded source, before attempting a full galaxy fit or treating the toy coefficient as a vacuum prediction. The MONO and memory chains remain useful acceptance tests for any proposed common action; they must not be merged into a single theory by relabeling their different variables.
