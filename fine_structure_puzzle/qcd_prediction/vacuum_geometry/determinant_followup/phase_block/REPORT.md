# Static spherical phase/radial-gauge determinant on a compatible domain

FSP-003 / QCD-V continuation. All changes are confined to phase_block/. Frozen parent reports, scripts and manifests are preserved. This calculation completes the remaining **static grand-spin-zero** gauge sector in a declared auxiliary comparison; it does not perform the angular or Fourier sum or physical vacuum matching.

**Calculated result.** With the boundary conditions derived below, the phase/radial-gauge block and its framed complex ghost give the exact relative Gaussian factor

\[
\boxed{\mathcal Z_{\rm phase+gh}^{(0)}(x)=K(x)^{-1/2}
=\sqrt{\frac{\sinh x}{x}},\qquad x=m_WR.}\tag{P1}
\]

The reference in (P1) is the explicit unbroken saddle \(K=1,h=0\), with the **same mixed vector boundary conditions** and Dirichlet ghost framing. It has different holonomy from the BPS saddle and is an auxiliary comparison, not the desired broken-phase QCD vacuum subtraction.

Combining this comparison with the previously calculated real spherical block, converted to that same reference, gives

\[
\boxed{\mathcal Z_{J=0,n=0}^{(0)}(x)
=\left[\frac{x\sinh^2x}{9I(x)}\right]^{1/2},}\tag{P2}
\]

\[
I(x)=\int_0^x\!dt\left[(\coth t-1/t)^2
+\frac12\left(\frac{\cosh t}{t}-\frac1{\sinh t}\right)^2\right].
\]

No global-rotation or translation collective-coordinate Jacobian is inserted. The compatible finite-wall operators have no exact zero modes in the blocks used here.

## 1. Actual spherical action and radial gauge field

Use the static BPS sector of Euclidean \(SU(2)\) Yang–Mills on \(B_R^3\times S_L^1\), with fixed small circle \(L\). In dimensionless units \(t=m_Wr\), write the standard spherical fields as

\[
A_i^a=\epsilon_{aij}\frac{n_j}{r}(1-\operatorname{Re}W)
+(\delta_{ia}-n_in_a)\frac{\operatorname{Im}W}{r}
+n_in_a a,\qquad \Phi^a=n^aH.
\]

Apart from the fixed overall factor, the radial action is

\[
E=\int dt\left[|W'-iaW|^2
+\frac{(|W|^2-1)^2}{2t^2}
+\frac{t^2h'^2}{2}+|W|^2h^2\right].\tag{P3}
\]

The background is \(W=K=t/\sinh t\), \(a=0\), \(h=\coth t-1/t\). A radial infinitesimal gauge parameter \(\theta n^a\) acts on phase fluctuations as \(\delta v=K\theta\), \(\delta a=\theta'\), where \(W=K+iv\). The actual quadratic phase action is

\[
E_{\rm phase}^{(2)}=\int dt\left[
(v'-aK)^2+2aK'v
+\left(\frac{K^2-1}{t^2}+h^2\right)v^2\right].\tag{P4}
\]

The cross term \(2aK'v\) is necessary; dropping it would break gauge invariance. Put \(\chi=v/K\), \(b=a-\chi'\). The BPS equation for \(K\) reduces (P4) to

\[
E_{\rm phase}^{(2)}=\int K^2b^2dt+[KK'\chi^2]_0^x.\tag{P5}
\]

The boundary term vanishes for fixed tangential data \(v(x)=0\) and a smooth origin. Although \(b\) has no bulk derivative in this expression, simply integrating \(a\) out and discarding a functional Jacobian would lose the gauge and boundary measure. We retain it instead.

The actual fluctuation norm is proportional to \(\int(2v^2+t^2a^2)dt\). Thus

\[
\eta=\sqrt2v,\qquad \zeta=ta,\qquad y=(\eta,\zeta)^T
\]

are canonical, and the Gaussian measure is \(\mathcal D\eta\mathcal D\zeta\). The change from the original radial amplitudes supplies only the background-independent product of \(\sqrt2t\); it cancels in the declared comparison. The reduced ghost is \(u=t\theta\), whose canonical norm is \(\int|u|^2dt\). No \(K\)-dependent measure is discarded.

## 2. Gauge fixing and the complete mixed boundary domain

Define \(c=\sqrt2K/t\) and the gauge generator

\[
Pu=\begin{pmatrix}cu\\(d/dt-1/t)u\end{pmatrix},\qquad
P^\dagger y=c\eta-\zeta'-\zeta/t.
\]

The actual background divergence is
\(G=a'+2a/t-2Kv/t^2\), so \(tG=-P^\dagger y\).
The gauge-invariant part (P5) is one half the squared norm of
\(Q_1y=(d/dt+h)\eta-c\zeta\), and \(Q_1P=0\).
Adding the background Feynman-gauge term \(\tfrac12\int t^2G^2dt\) gives

\[
\mathcal H_{\rm phase}=\mathcal Q^\dagger\mathcal Q,\qquad
\mathcal Q=\frac d{dt}+\begin{pmatrix}h&-c\\-c&1/t\end{pmatrix}.
\tag{P6}
\]

Its actual second-order potential is

\[
U_{\rm phase}=
\begin{pmatrix}
h^2+(3K^2-1)/t^2&-2c(h+1/t)\\
-2c(h+1/t)&2(K^2+1)/t^2
\end{pmatrix}.\tag{P7}
\]

Fixing the tangential connection requires \(\eta(x)=0\). The normal connection is retained freely in the quadratic-form domain. Variation of that form has boundary term \((\mathcal Qy)_1\delta\eta+(\mathcal Qy)_2\delta\zeta\), so its natural second condition is

\[
\boxed{\eta(x)=0,\qquad \zeta'(x)+\zeta(x)/x=0.}\tag{P8}
\]

This is tangential Dirichlet plus background-divergence zero, not Dirichlet for both fields. The framed ghost has \(u(x)=0\). On a ghost eigenfunction, \(Pu\) satisfies both vector conditions because \(P^\dagger Pu=\lambda u\). At the origin the two smooth vector solutions have leading behavior

\[
y_0\sim t e_0,\quad y_2\sim t^3e_2,\qquad
e_0=(\sqrt2,1)^T/\sqrt3,\quad
e_2=(-1,\sqrt2)^T/\sqrt3.\tag{P9}
\]

These are respectively the regular \(l=0\) and \(l=2\) combinations of the leading matrix potential. The scalar ghost and scalar partners have regular \(t^2\) behavior. The opposite irregular branches are excluded. Equations (P8)–(P9) are a self-adjoint mixed domain.

## 3. Factorization with its actual paired boundary conditions

The BPS identities give

\[
\mathcal Q\mathcal Q^\dagger
=\operatorname{diag}(L_A,L_g),\quad
L_A=-d^2/dt^2+h^2+(1+K^2)/t^2,\quad
L_g=-d^2/dt^2+2K^2/t^2.\tag{P10}
\]

For an eigenfunction \(z=\mathcal Qy\), (P8) gives \(z_2(x)=0\). The first component of \(\mathcal Q^\dagger z=\lambda y\) gives

\[
z_1'(x)-h(x)z_1(x)=0.\tag{P11}
\]

Thus \(L_A\) has Robin data and \(L_g\) has Dirichlet data. Both scalar partners have the regular \(l=1\) origin condition. The inverse positive-eigenvalue map is \(y=\mathcal Q^\dagger z/\lambda\); it respects (P8) and (P9). The block has no kernel: \(\mathcal Qy=0\) implies \(y=Pu\), and the remaining equation and boundary data are \(L_gu=0\), \(u(x)=0\). Positivity of the framed ghost forces \(u=0\).

The Robin scalar is positive too: its quadratic form is
\(\int[(-z'+hz)^2+c^2z^2]dt\), and \(c>0\) at every finite radius. Hence no exact zero eigenvalue is removed. This establishes the spectral identity on the stated domains, rather than importing an infinite-space pairing.

The coordinator supplied the elementary candidate

\[
u_A=3(\sinh t/t-t/\sinh t),\qquad u_g=3(t\coth t-1).
\]

Direct substitution verifies \(L_Au_A=L_gu_g=0\), each with Frobenius coefficient one. Moreover

\[
\boxed{u_A'-hu_A=6Kh.}\tag{P12}
\]

The independent phase action/domain derivation was saved in INDEPENDENT_RAW.md before opening the coordinator's raw note. The elementary \(u_A\) candidate and its first check are credited separately; they are not claimed as an independent discovery here.

## 4. Exact determinant with the same mixed vector reference

Let \(Y\) be the regular zero-energy matrix with columns normalized as (P9), and define its boundary determinant

\[
F(x)=\det\begin{pmatrix}
Y_{11}&Y_{12}\\
Y'_{21}+Y_{21}/x&Y'_{22}+Y_{22}/x
\end{pmatrix}.
\]

There is a short normalization-sensitive derivation. The regular gauge solution \(y_g=Pu_g\) obeys \(\mathcal Qy_g=0\) and has origin coefficient \(\sqrt3e_0t\). For the regular \(l=2\) column \(y_2\), \(\mathcal Qy_2\sim5e_2t^2\); its second component therefore equals \(5\sqrt{2/3}u_g\) at every radius by scalar uniqueness. On the wall, the second boundary functional equals \((\mathcal Qy)_2+c\eta\). Taking its determinant on \([y_g,y_2]\) and dividing by \(\sqrt3\) yields

\[
\boxed{F(x)=30xK(x)h(x)^2.}\tag{P13}
\]

For the unbroken auxiliary reference \(K=1,h=0\), the regular columns are exactly \(te_0,t^3e_2\), and the same boundary functional gives \(F_{\rm ref}=10x^3/3\). The regular-cutoff matrix determinant theorem, followed by the shared-origin limit, therefore gives

\[
D_{\rm phase}^{(0)}=F/F_{\rm ref}=9Kh^2/x^2,\qquad
D_g^{(0)}=3h/x.\tag{P14}
\]

The vector Gaussian weight is \((D_{\rm phase}^{(0)})^{-1/2}\); the complex ghost gives \(D_g^{(0)}\). Their product is exactly (P1). There is no unspecified radial-field Jacobian or arbitrary zero-mode removal in this identity.

The matrix determinant theorem is used only at positive origin cutoff, with Hermitian potentials, matched leading differential coefficient and matched outer boundary matrices. Its source is Kirsten–McKane, math-ph/0403050v1, Section 4, equations (40)–(42) and the following unnumbered ratio. Each origin angular channel has the same singular leading part in background and reference, so its cutoff normalization cancels before the cutoff tends to zero, as in the frozen parent derivations.

## 5. A second explicit auxiliary comparison and the small eigenvalue

To connect to the earlier massive \(l=1\) reference, retain the **same actual Robin parameter** \(h(x)\) in numerator and reference. Its regular reference solution is \(u_*=3(\cosh t-\sinh t/t)\), with boundary functional \(3(\cosh x/x-\operatorname{csch}x)\). Consequently

\[
D_A^{(*)}=\frac{2Kh}{\cosh x/x-\operatorname{csch}x},\qquad
\frac{D_g^{(0)}}{D_A^{(*)}}
=\frac{3(\sinh x\cosh x-x)}{2x^3}.\tag{P15}
\]

This is the coordinator's separate candidate comparison, verified here. In (P1), the logarithm after \(x/2-\tfrac12\log(2x)\) is \(\tfrac12\log(1-e^{-2x})\); hence every algebraic inverse-radius term vanishes in that phase-plus-ghost comparison. In (P15), the square-root logarithm after \(x-\tfrac32\log x+\tfrac12\log(3/8)\) is \(\tfrac12\log(1-e^{-4x}-4xe^{-2x})\), likewise exponentially small. These cancellations concern precisely the declared comparisons and domains.

There is a genuine finite-radius small eigenvalue that cannot be dropped. Applying the Robin quadratic form to the regular zero-energy function \(u_A\) gives the rigorous Rayleigh upper bound

\[
0<\lambda_{A,\min}(x)
\le\frac{u_A(x)[u_A'(x)-h(x)u_A(x)]}
{\int_0^x u_A(t)^2dt}
\sim16x^2e^{-2x}.\tag{P16}
\]

It is not an exact collective zero mode: the bound tends to zero as its norm concentrates near the expanding wall, while the corresponding zero-energy bulk solution grows at infinity. Removing it by an infinite-volume zero-mode rule would change the determinant. Equation (P16) is an upper bound with an asymptotic expression for that bound, not a computation of the eigenvalue's exact leading coefficient.

The normalized first-order spectral map contains \(\lambda^{-1/2}\), so it is not uniform in this limit. The vector partner can approach the normalizable infinite-space global-rotation zero mode even though the scalar partner concentrates at the wall. This is precisely why taking the infinite-radius limit and replacing a small eigenvalue by a collective coordinate needs a separate measure derivation. Finite-wall unprimed determinants cannot simply be multiplied by the infinite-space collective-coordinate Jacobian.

## 6. Complete static spherical comparison with the real block

For the real \(\delta K,\delta h\) block calculated in the frozen VECTOR_BLOCK.md, the same unbroken reference has potential \(2I/t^2\), regular determinant \(x^4\), and outer Dirichlet data on both fields. Thus

\[
D_{\rm real}^{(0)}=\frac{9I(x)}{x^2\sinh x}
\sim\frac{9e^x}{8x^4}
\left[1+\frac1x+\frac3{2x^2}+\cdots\right].\tag{P17}
\]

Its boundary data and action match the real part of the present spherical saddle. Together, real and phase blocks exhaust the four real static grand-spin-zero gauge/\(A_4\) components; the single complex radial ghost removes the two gauge-fixed degrees in that sector. Their relative Gaussian product is (P2), with

\[
\log\mathcal Z_{J=0,n=0}^{(0)}
=\log(2/3)+\frac32\log x
-\frac1{2x}-\frac1{2x^2}+O(x^{-3}).\tag{P18}
\]

This \(-1/(2x)\) is calculated for the **complete static spherical determinant in this common auxiliary comparison**, with no collective zero Jacobians. It must not be added to the earlier \(-1/(2x)\) variational zero-mode normalization. Nor is it a full-theory coefficient: the remaining angular/Fourier modes, UV subtraction, deformed-theory profile and physical broken-vacuum reference can change it. Using the frozen real block's different massive reference instead gives its residual \(-1/x\); the contrast illustrates why references cannot be mixed while claiming a unique physical number.

There is a further physical-path qualification. The present family keeps asymptotic \(m_W\) fixed, while its actual wall Higgs value is \(b=m_Wh(m_WR)\). FIXED_BOUNDARY_PATH.md derives \(m_WR=bR+1+\) exponentially small terms. At fixed \(b\), the same dimensionless Gaussian function has residual \(+1/(bR)\) after its leading logarithm, rather than \(-1/(2m_WR)\). The classical BPS action likewise loses its algebraic inverse-radius term at fixed \(b\). This is an explicit boundary-matching dependence, with dimensionful-measure qualifications stated in that separate hand note.

## 7. Computation, limits and next step

The contract and current manifest specify exact symbolic identities and finite numerical comparisons. The test substitutes both scalar solutions, verifies the actual phase Hessian and its diagonal partner, and integrates the original mixed-boundary matrix equation independently of (P13). It retains the scalar Robin state and evaluates its Rayleigh bound. The total static-spherical expression reuses the independently checked real-block integral with its reference converted explicitly.

Runs phase-001 and phase-002 hit their 50-second CPU limits in generic SymPy simplification of the scalar hyperbolic identities, before the numerical stage. Stage output in the second run localized the bottleneck. Their scripts, contracts, manifests and logs are preserved as resource-inconclusive evidence. The third script converts those expressions to exact rational functions of \(x\) and \(e^x\), resolving the same identities without raising the cap.

The current script is check_phase_v3.py with COMPUTATION_CONTRACT_v3.json. Run phase-003 completed in 2.52 seconds of recorded runner wall time, and its v2 manifest validates against current inputs. Direct DOP853 integration of the actual matrix equation with its mixed boundary functional agrees with (P13) at \(x=2,4,6\), each at origin cutoffs \(10^{-3}\) and \(5\times10^{-4}\); the largest relative discrepancy is \(8.49\times10^{-13}\), below the declared conservative \(5\times10^{-6}\) tolerance. These residuals are not certified intervals. Separate 60-digit quadratures evaluate (P16) and (P2) at \(x=5,10,20\); they do not fit any asymptotic coefficient. All numerical/symbolic code is self-contained inside this subdirectory, with the frozen real-block formula identified in the mathematical dependency receipt.

No random fitting, target alpha or observed cosmological input is used. Validate the current record from the repository root:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_prediction/vacuum_geometry/determinant_followup/phase_block/runs/phase-003/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

For a new execution, use the recorded runner contract/argv with a fresh output directory and matching result path. The scalar Robin solution was supplied by the coordinator after the phase action/domain raw derivation was saved; the mixed-matrix boundary determinant was derived here independently, then checked numerically. The coordinator independently reconstructed the same domain map, scalar solution and alternate comparison. This is review provenance, not a substitute for the displayed proofs. Final self-review checked signs, origin normalizations, derivative versus determinant exponents and the distinction between finite positive small modes and exact zero modes.

The next calculation must address additional angular/Fourier sectors in a consistently matched theory and reference; those sums are outside this assignment. A further separate bridge is needed from the fixed-small-circle BPS calculation to physical strongly coupled QCD and its metric stress response. Physical \(c_H\), \(R(\alpha)\), and an alpha root remain uncalculated.
