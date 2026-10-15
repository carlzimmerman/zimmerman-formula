# Infinite-domain three-dimensional quadratic-energy theorem

2026-10-14. C3W-001. Self-reviewed analytic derivation, supported by separately frozen computations. This proves the stated linear quadratic-energy estimate for an engineered action. It does not prove nonlinear stability, well-posedness, causal fronts, empirical viability, a finite material interface, or a powered propulsion device.

## 1. Claim and exact theory

Use signature −+++, c = hbar = 1, reduced Planck mass Mp, hmed > 0 and D = Mp²/hmed. On all of R³ choose smooth static b with bounded first two derivatives. The target is

\[
ds_*^2=-dt^2+dx^2+dy^2+[dz+b(x,y,z)dt]^2,
\qquad \Phi_*^A=x^A.
\]

The clock gradient is timelike and the four material gradients are invertible. Define the inverse source

\[
H_{AB}(\Phi)=M_p^2R_{AB}[g_*](\Phi),\qquad
\mathcal L_0=\frac{M_p^2}{2}R
-\frac12H_{AB}(\Phi)\partial\Phi^A\cdot\partial\Phi^B.
\]

This is an inverse construction: its functions encode the target geometry. It is not a proposed identification of observed cold matter. At the target its stress is Mp²G[g*]; the material equations follow from the Bianchi identity and the invertible field map. The earlier source calculation also evaluates all four equations directly.

Let θa be the target coframe `(dt,dx,dy,dz+b dt)` as functions on field space, and

\[
S^{ab}=\theta^a_A\theta^b_B
\left[g^{\mu\nu}\partial_\mu\Phi^A\partial_\nu\Phi^B-g_*^{AB}(\Phi)\right].
\]

In its target normal frame set Ht = Hnn/hmed, ci = Hni/hmed, Hs,ij = Hij/hmed and Bmat = 4I−Hs. Add the strain density

\[
\begin{split}
\frac{\mathcal L_{\rm str}}{h_{\rm med}}={}&
\frac{1-H_t}{8}(S^{00})^2+rac12S_0^TB_{\rm mat}S_0
-\frac12S^{00}(c\cdot S_0)-\frac12\sum_{ij}(S^{ij})^2\\
&+\sum_i c_i\left[\sum_jS^{0j}S^{ij}-\frac12S^{0i}\operatorname{tr}S\right].
\end{split}
\]

Thus Kc = 1, L = 4, μ = 2, A = 1, r = 1 in the preceding conventions. S0 here is the three-vector of S0i, not the source action.

Set

\[
U_\mu=-\frac{\partial_\mu\Phi^0}{\sqrt{-\partial\Phi^0\cdot\partial\Phi^0}},
\quad P^{\mu\nu}=g^{\mu\nu}+U^\mu U^\nu,
\quad \Theta=\nabla_\mu U^\mu,\quad
\mathfrak a_\mu=U^\nu\nabla_\nu U_\mu,
\]

\[
C^{IJ}=P^{\mu\nu}\partial_\mu\Phi^I\partial_\nu\Phi^J-\delta^{IJ},
\quad I,J=1,2,3.
\]

The selected repair is

\[
\mathcal L_{\rm rep}
=\frac{M_p^2}{2}(\Theta-\Theta_*)^2
+\frac{M_p^2}{2}\mathfrak a_\mu\mathfrak a^\mu
+\frac{\kappa M_p^2}{8}\sum_{I,J}
\left[(U\cdot\partial C^{IJ})^2
-\frac12P^{\mu\nu}\partial_\mu C^{IJ}\partial_\nu C^{IJ}\right],
\quad \boxed{\kappa=4},\quad \Theta_*=-b_z.
\]

The total action integrates L0 + Lstr + Lrep under √−g. Every target coefficient is a function of Φ. This strengthens the preceding elastic coefficient from κ = 1 to 4; it does not claim to prove the unchanged κ = 1 action.

On the target, Θ = −bz, acceleration is zero, and C = 0 because the target spatial metric is the identity. All added squares and their first functional variations vanish. The target remains an exact solution for arbitrary smooth static b, including a genuinely spherical profile with bz nonzero. There is no planar Q-to-Θ substitution in this proof.

Define clock-frame Frobenius sup norms

\[
B=\|b\|_\infty,\qquad g=\|\nabla b\|_\infty,
\qquad \eta=\|R_{ab}[g_*]\|_{F,\infty}.
\]

**Theorem.** If

\[
B\le\frac1{10},\qquad
13Dg^2+\frac32D\eta\le\frac14,
\]

the complete constraint-reduced quadratic Hamiltonian satisfies, for real smooth compactly supported spatial metric perturbations Q and velocities u on R³,

\[
\boxed{E_2\ge M_p^2\left[
\frac12\|u\|_2^2+\frac1{10}\|\nabla Q\|_2^2
+\frac1{4D}\|Q\|_2^2\right].}
\]

Norms of symmetric matrices sum all ordered components, so off-diagonal entries occur twice. The lapse and all three shifts are eliminated globally in H¹(R³), rather than frozen or set to zero in the physical dynamics. The estimate extends by the indicated energy-space completion. It includes every wavelength and all propagation directions; no finite box, ultraviolet cutoff or infrared deletion is used.

For smooth finite-energy solutions of the stationary linear Euler–Lagrange system, E2 is conserved and this norm cannot grow without bound. This is the energy-stability conclusion; construction of a full nonlinear evolution or a separate general well-posedness theorem is outside this claim.

## 2. Exact kinetic/constraint completion

Use unitary gauge ΦA = xA. This removes the material-coordinate gauge freedom while retaining all ten metric variables. ADM identities give Θ = K and Cij = γij(inverse)−δij. Neither the new operator nor the rest of this gauge-fixed action has a lapse/shift time derivative. Write

\[
\delta\gamma_{ij}=Q_{ij},\quad u_{ij}=\partial_tQ_{ij},
\quad \delta N=\alpha,\quad\delta\beta^i=v^i,
\quad E_0=-\nabla\beta_*-(\nabla\beta_*)^T,
\quad \beta_*=b e_z.
\]

Our extrinsic-curvature convention is `Kij=(dotγij−Lβγij)/(2N)` and K* = tr E0/2 = −bz. Put Q = 0 while retaining arbitrary u, α and v. A direct second variation gives the exact joint quadratic form

\[
\begin{split}
J_b[u,\alpha,v]={}&\int\frac{M_p^2}{8}
|u-(\nabla v+\nabla v^T)-\alpha E_0|_F^2
+\frac{\kappa M_p^2}{8}|u|_F^2\\
&+\frac{h_{\rm med}}2\alpha^2+2h_{\rm med}|v|^2
+\frac{M_p^2}{2}|\nabla\alpha|^2\,d^3x.
\end{split}
\]

This holds for an arbitrary three-dimensional ∇b, including bz. It is not a high-frequency approximation.

To verify the gravity term, with γ = I at this instant, write E = E0 + εE1, E1 = u−sym∇v, N = 1+εα. The quadratic coefficient of

\[
\frac{\operatorname{tr}E^2-(\operatorname{tr}E)^2}{8N}
+\frac N2\left(\frac{\operatorname{tr}E}{2N}-K_*\right)^2
\]

is `|E1−αE0|²/8`. Thus the nonzero trace of the background does not introduce an omitted lapse–velocity term.

The inverse-source quadratic density at Q = 0 is

\[
\tfrac12v^TH_sv+\alpha H_n\cdot v+\tfrac12H_{nn}\alpha^2.
\]

Its H-dependent pieces cancel the corresponding strain pieces exactly, leaving hmed α²/2 + 2hmed v². The acceleration and elastic terms give the remaining positive terms in Jb. The source coefficients here carry their actual energy-density normalization.

The lapse/shift form Jb[0,α,v] is strictly coercive in H¹×H¹. In particular, the positive α² and v² masses cover arbitrarily long wavelengths. To see control of shift derivatives, use

\[
\|\operatorname{sym}\nabla v\|_2^2
=2\|\nabla v\|_2^2+2\|\nabla\cdot v\|_2^2,
\]

and `sym∇v = (sym∇v+αE0)−αE0` with bounded E0. Consequently the elliptic auxiliary problem has a unique finite-energy minimizer for its bounded linear forcing. For a bounded linear forcing the quadratic functional has a finite infimum. The parallelogram identity makes a minimizing sequence Cauchy in its positive quadratic norm; coercivity identifies its limit in H¹, and variation gives the unique auxiliary equation. Couplings to u∈L² and Q∈H¹ are bounded in that norm; integration by parts puts the spatial-curvature forcing into ∇α·∇Q form.

Let A be the reduced velocity operator. Minimizing Jb over the auxiliaries yields

\[
\frac12\langle u,Au\rangle
\ge\frac{\kappa M_p^2}{8}\|u\|_2^2
=\frac{M_p^2}{2}\|u\|_2^2.
\]

Taking the trial auxiliaries α = v = 0 also bounds this form above by `(1+κ)Mp²||u||²/8`. Thus the kinetic estimate does not deteriorate at short wavelengths.

## 3. A sufficient static energy bound

Define F_b[Q] as the quadratic Lagrangian evaluated at u = α = v = 0. This is a **trial auxiliary configuration for an inequality**, not an assumption about physical lapse/shift fluctuations.

Because the auxiliary Hessian is positive, solving its static constraint minimizes the quadratic Lagrangian:

\[
L_{2,\rm red}[Q,0]\le F_b[Q].
\]

Therefore a strictly negative F_b is sufficient for positive reduced restoring energy. The auxiliary–metric cross terms cannot reverse this implication: their Schur contribution makes the static Lagrangian smaller.

### 3a. Spatial Einstein curvature

The integrated spatial-curvature quadratic form about γ = I is

\[
\frac{L_{R,2}}{M_p^2}=\int\left[
-\frac18|\nabla Q|^2+\frac18|\nabla\operatorname{tr}Q|^2
+\frac14|\partial_iQ_{ij}|^2
-\frac14(\partial_iQ_{ij})\partial_j\operatorname{tr}Q\right]d^3x.
\]

For each Fourier wave vector, rotate it to z. At unit magnitude its Hermitian symbol is `(Q11 Q22−Q12²)/4` for real amplitudes, and

\[
\frac18|Q|_F^2-\frac14(Q_{11}Q_{22}-Q_{12}^2)
=\frac18[(Q_{11}-Q_{22})^2+Q_{33}^2
+4Q_{12}^2+2Q_{13}^2+2Q_{23}^2]\ge0.
\]

Polarization gives the complex Hermitian version. Rotational covariance and the Fourier norm identity give the all-direction, all-wavelength bound

\[
L_{R,2}\le\frac{M_p^2}{8}\|\nabla Q\|_2^2.
\]

### 3b. Background extrinsic curvature and normalized expansion

At u = α = v = 0 put J_ij = ∂iβ*j, E0 = −J−JT and

\[
E_1=-b\partial_zQ-JQ-QJ^T,
\quad e_0=|E_0|\le2g,
\quad e_1=|E_1|\le B|\nabla Q|+2g|Q|.
\]

For γ = I+εQ the combined exact density at N = 1 is

\[
\sqrt\gamma\left[
\frac18\operatorname{tr}(\gamma^{-1}E\gamma^{-1}E)
-\frac{K_*}{2}\operatorname{tr}(\gamma^{-1}E)
+\frac{K_*^2}{2}\right],\qquad E=E_0+\epsilon E_1.
\]

Let t = tr Q and d2 = t²/8−tr(Q²)/4, so |t|≤√3|Q| and |d2|≤|Q|²/4. Its quadratic coefficient, divided by Mp², is

\[
\begin{split}
M_b={}&\frac18\{\operatorname{tr}E_1^2
-4\operatorname{tr}(QE_0E_1)+2\operatorname{tr}(Q^2E_0^2)
+\operatorname{tr}(QE_0QE_0)\\
&+t[\operatorname{tr}(E_0E_1)-\operatorname{tr}(QE_0^2)]
+d_2\operatorname{tr}E_0^2\}\\
&-\frac{K_*}{2}\{\operatorname{tr}(Q^2E_0)-\operatorname{tr}(QE_1)
+\frac t2[\operatorname{tr}E_1-\operatorname{tr}(QE_0)]
+d_2\operatorname{tr}E_0\}+\frac{K_*^2}{2}d_2.
\end{split}
\]

Use |K*|≤g, Frobenius product bounds and √3<7/4. Term by term,

\[
M_b\le\frac18e_1^2+\frac{43}{16}g|Q|e_1
+\frac{79}{16}g^2|Q|^2.
\]

Substitute the bound on e1 and complete the scalar square. This is at most

\[
\frac{55}{32}B^2|\nabla Q|^2
+\frac{397}{32}g^2|Q|^2
\le 2B^2|\nabla Q|^2+13g^2|Q|^2.
\]

The difference at the intermediate Young step is `(51/32)(B|∇Q|−g|Q|)²`. The proof uses the displayed universal norm inequalities; the separate nonlinear local-jet checks audit their action expansion but are not the universal proof.

### 3c. Inverse source, strain and derivative elasticity

Write Rn = Rnn and Rs for the spatial normal-frame Ricci block. The inverse-source static quadratic density is

\[
V_H=M_p^2\left[
\frac{d_2}{2}(R_n-\operatorname{tr}R_s)
-\frac12\operatorname{tr}(R_sQ^2)
+\frac t4\operatorname{tr}(R_sQ)\right].
\]

The previous trace bounds and |Rs|F≤η give

\[
|V_H|\le M_p^2\left(\frac58+\frac{3\sqrt3}{8}\right)\eta|Q|^2
<\frac{3M_p^2}{2}\eta|Q|^2.
\]

The strain contribution at this trial configuration is exactly `−hmed |Q|²/2`. Acceleration gives zero because N is fixed to one for this trial. Derivative elasticity gives

\[
\frac{\kappa M_p^2}{8}\int
[b^2|\partial_zQ|^2-\tfrac12|\nabla Q|^2]d^3x.
\]

Combining 3a–3c with κ = 4,

\[
F_b[Q]\le-M_p^2\left[
\left(\frac18-\frac52B^2\right)\|\nabla Q\|_2^2
+\left(\frac1{2D}-13g^2-\frac32\eta\right)\|Q\|_2^2\right].
\]

Under the theorem hypotheses the coefficients are at least 1/10 and 1/(4D). This completes the static estimate without solving a sampled dispersion relation.

## 4. Constraint reduction and conserved energy

After the unique lapse/shift solution, the stationary quadratic Lagrangian has form

\[
L_{2,\rm red}=\tfrac12\langle u,Au\rangle
+\langle u,\mathcal M Q\rangle-\tfrac12\langle Q,CQ\rangle.
\]

All metric components and mixed terms are retained. The canonical momentum is p = Au+MQ, and

\[
E_2=\tfrac12\langle p-\mathcal M Q,A^{-1}(p-\mathcal M Q)\rangle
+\tfrac12\langle Q,CQ\rangle
=\tfrac12\langle u,Au\rangle+\tfrac12\langle Q,CQ\rangle.
\]

Sections 2–3 give the asserted lower bound. Compact support initially justifies the integrations by parts; bounded coefficient and form estimates extend by completion to the stated finite-energy spaces. Since the background and coefficients are time independent, this E2 is conserved for smooth finite-energy linearized solutions. This is quadratic perturbation energy in unitary time, not a computed fuel budget or a claim about the full nonlinear ADM/canonical energy.

## 5. Explicit spherical wall satisfying the hypotheses

Let

\[
w(u)=\begin{cases}e^{-1/[u(1-u)]},&0<u<1,\\0,&\text{otherwise},\end{cases}
\quad I=\int_0^1w(u)du,
\quad F(u)=I^{-1}\int_0^u w(t)dt,
\]

with F extended as zero/one outside [0,1]. Define `b(r)=V F(2r/R−1)`. This is C∞, b = 0 in r≤R/2 and b = V in r≥R. Thus it has a flat cabin and exactly flat exterior, with a smooth finite transition. The **fields/repair coefficients remain present in the exterior**; this is not a physical interface to ordinary vacuum.

On [1/4,3/4], w≥e^−16/3, so I≥e^−16/3/2. Also w≤e^−4. For q=u(1−u), x=1/q≥4, `|w'|≤x²e^−x≤16e^−4`. Thus

\[
|F'|\le2e^{4/3}<8,\qquad |F''|\le32e^{4/3}<128.
\]

The elementary exponential bound is certified by a finite rational series upper bound with geometric remainder. Radial differentiation gives

\[
B\le V,\qquad g\le\frac{16V}{R},\qquad
\|\nabla^2b\|_{F,\infty}\le\frac{514V}{R^2}.
\]

For the last bound, radial Hessian eigenvalues are b'' and twice b'/r; r≥R/2 in the transition. Their respective absolute bounds are 512V/R² and 32V/R², and `512²+2·32²<514²`.

For reference, the exact normal Ricci components, p_i=∂i b and h_ij=∂i∂j b, are

\[
R_{ab}=\begin{pmatrix}
-bh_{zz}-(p_x^2+p_y^2)/2-p_z^2&h_{xz}/2&h_{yz}/2&-(h_{xx}+h_{yy})/2\\
h_{xz}/2&p_x^2/2&p_xp_y/2&bh_{xz}/2+p_xp_z\\
h_{yz}/2&p_xp_y/2&p_y^2/2&bh_{yz}/2+p_yp_z\\
-(h_{xx}+h_{yy})/2&bh_{xz}/2+p_xp_z&bh_{yz}/2+p_yp_z&bh_{zz}-(p_x^2+p_y^2)/2+p_z^2
\end{pmatrix}.
\]

Splitting it into gradient-square, Hessian-only and b·Hessian parts gives norm bounds √2 g², j and 2Bj, respectively, where j=||Hess b||F,∞. Consequently

\[
\eta\le2[g^2+(1+B)j]\le10[g^2+(1+B)j].
\]

The looser factor ten simplifies a conservative explicit example. For

\[
\boxed{0\le V\le\frac1{10},\qquad R\ge100\sqrt D,}
\]

we have `Dg²≤4/15625`, `Dη≤591/10000` and

\[
13Dg^2+\tfrac32D\eta\le\frac{45989}{500000}
=0.091978<\frac14.
\]

This is a nonempty family of three-dimensional spherical backgrounds satisfying the theorem. The speed is ≤0.1c in restored units. D is an assigned theory scale, not a measured material parameter; this is a sufficient mathematical regime, not an activation curvature or an engineering specification.

The background still requires negative normal energy density,

\[
T_{nn}=M_p^2G_{nn}=-\frac{M_p^2}{4}(b_x^2+b_y^2),
\]

where transverse gradients are nonzero. Positive energy of perturbations does not turn this assigned exotic background stress into ordinary baryons or demonstrate a way to manufacture it.

## 6. Independent checks and precise limits

C3W-001G derives the full four-dimensional Ricci tensor and transforms it to the normal frame. C3W-001E checks the exact joint completion, spatial-curvature and Ricci norm certificates, static coefficient arithmetic and two nonlinear static jets with bz nonzero. C3W-002 separately assembles the entire 3D ADM Galerkin operator, including the nonzero Θ* terms and all metric/auxiliary components, for three periodic curvature controls. Its reduced matrices obey the analytic lower bounds, and its flat six-mode spectrum matches independently derived frequencies. This is an audit of the derivation, not the basis for replacing R³ by a grid.

The proof does not use a named external stability theorem. Its leaves are the displayed local expansions, matrix norm inequalities, Fourier norm identity, positive Hilbert-space auxiliary minimization and quadratic Legendre transform. The restriction to stationary quadratic energy is essential. No nonlinear, causal-front, measured-gravity, material-interface, controller/craft-backreaction or propulsion-energy conclusion is smuggled into the theorem. See [audit](AUDIT.md), [control analysis](CONTROL.md), and [mechanical interpretation](MECHANISM.md).


## Physical vacuum check

The κ=4 tensor branch has `ΩT²=3q/5+4/5` and propagating group speed strictly below `sqrt(3/5)c≈0.775c`. The localized optical window leaves ordinary exterior photons at c. If this uniform infinite medium were interpreted as observed vacuum, that tensor propagation would conflict with the near-light gravitational-wave speed inferred from [GW170817/GRB170817A, section 4.1 and equation 1](https://arxiv.org/pdf/1710.05834). The cited 2017 analysis gives a fractional difference between −3×10^−15 and +7×10^−16 under its stated emission assumptions; no latest-precision claim is needed here. C3W-006 derives the model dispersion independently. Thus the present unconfined phase is a mathematical medium, not a viable literal model of ordinary vacuum. A physical application needs a localized phase and a newly proved match to an acceptable exterior. This restriction does not invalidate the internal quadratic theorem, and it does not prove a no-go for every localized construction.
