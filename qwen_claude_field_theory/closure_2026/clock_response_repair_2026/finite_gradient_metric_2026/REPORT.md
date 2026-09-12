# Finite-gradient continuation: Einstein feedback and the charged-background obstruction

2026-09-12. Reviewed live source HEAD `706cd625f648079d318aa968b59fbd45850720f2`, including L192, L193, PAPER19 and its addendum. This continues the missing metric/background calculation from the previous audit. **Full same-action gravity closure remains OPEN.** No coefficient functions, matter species, interpolation law, or gate thresholds were changed.

## What this calculation establishes

1. At zero cubic coupling, the full Einstein principal operator does not erase the earlier scalar hyperbolicity obstruction, conditional on a regular on-shell background jet.
2. With the cubic term retained and Einstein feedback eliminated, the proposed proxy marginal state remains unstable for **every coupling strength** in the stated locally affine, timelike-gradient class. Four Lean lemmas certify the final algebra, not the entire covariant derivation.
3. Independently, the Einstein momentum equation forbids promoting the inherited nonzero-charge history into a homogeneous diagonal-Bianchi-I state with a nonzero constant comoving scalar gradient, homogeneous clock, and comoving ordinary matter. This is exact, including the cubic term.

These are restricted obstructions, not a no-go for all MOND theories or all solutions of this action. No claim of global novelty priority is made.

## One unchanged action and conventions

The audited sector is

\[
S=\int\!d^4x\sqrt{-g}\left[\frac{M^2}{2}(R-2\Lambda)
 +P(X,\tau)-V(\tau)+sW(Y,\tau)+\gamma X\Box\chi\right]+S_m[g,\psi],
\]

with signature \((-+++)\), constant \(M^2>0\) and constant \(\gamma\),
\(X=-\nabla\chi\cdot\nabla\chi\), \(s=\sqrt{-\nabla\tau\cdot\nabla\tau}>0\), and \(Y\) the squared gradient of \(\chi\) projected orthogonal to the clock. Ordinary matter is minimally coupled. Numerical evaluations use the existing frozen action, including its gamma-dependent P/W coefficients. They do not identify its stored reference qbar with the evolved physical Q.

The local clock frame has \(\partial_\mu\tau=(s_0,0,0,0)\), **\(s_0>0\)**, and \(\partial_\mu\chi=(Q,b,d,0)\). This positive clock branch is required by the square-root expansion in `metric_principal.py`. Let \(z=b^2\) be the squared gradient parallel to the wavevector, \(Y=b^2+d^2\), and \(k\ne0\).

## 1. Actual Einstein principal calculation at gamma=0

The script constructs the linearized connection, Ricci tensor and Einstein tensor using ten independent symmetric metric components. It constructs the four coordinate-gauge columns separately, checks their annihilation, and computes ranks rather than entering them as results. For derivative covector \(\xi=(-c,1,0,0)\), harmonic reduction gives

\[
E^{\rm red}_{\mu\nu}=-\tfrac12\xi^2
 (h_{\mu\nu}-\tfrac12\eta_{\mu\nu}h),\qquad
\det E^{\rm red}=-\frac{(c-1)^{10}(c+1)^{10}}{1024}.
\]

The displayed determinant suppresses the nonzero constant Einstein coefficient. Direct ranks at spacelike/null/timelike covectors are 6/4/6, with gauge rank four in each case. The null kernel modulo gauge has dimension two. **This is a linear Einstein principal benchmark, not a nonlinear Dirac count for the whole theory.**

Independent quadratic expansion of the same metric-plus-two-field density computes differential orders: metric-metric matter terms have order zero, mixed terms order one, and scalar-scalar terms order two. The recovered leading scalar block is

\[
\begin{pmatrix}
 Kc^2+8QP_{XX}bc-2P_X+4P_{XX}z+2s_0C&-2QC\\
 -2QC&-F/s_0
\end{pmatrix},
\quad
C=W_Y+2zW_{YY},\quad F=W-2Q^2C-2zW_Y,
\]

where \(K=2P_X+4Q^2P_{XX}\). For \(F\ne0\), clock elimination gives

\[
Kc^2+8QP_{XX}bc-G=0,\quad
G=2P_X-4P_{XX}z-2s_0C\frac{W-2zW_Y}{F}.
\]

Consequently a strictly negative quarter-discriminant \(\Xi=16Q^2P_{XX}^2z+KG\) is not repaired by the lower-order metric terms at gamma=0. The non-real characteristic is non-null, so the harmonic metric block is invertible. The sourced metric amplitude scales as scalar amplitude divided by k; feeding it back changes lower-order terms, not this second-order scalar symbol. A residual harmonic coordinate transformation requires a null covector and cannot remove this branch.

The required on-shell compatibility statement uses the diffeomorphism identity \(\nabla_\mu T^\mu{}_{\nu}=E_\chi\nabla_\nu\chi+E_\tau\nabla_\nu\tau\). Linearized harmonic-constraint violations have wave principal propagation when the scalar equations hold. Thus the non-null branch is not merely a freely chosen constraint violation. This reasoning is an analytical principal-order argument; the script verifies its matrices and differential orders, not a PDE existence theorem.

The result is conditional on a regular on-shell jet. The run does **not** supply one. Zero spatial momentum, F=0, K=0, loss of clock timelikeness, and coincident critical/null limits require separate reductions; none is passed by continuity here.

## 2. Cubic metric feedback and a formal all-coupling obstruction

The [cubic derivation](cubic/REPORT.md) varies the same \(+\gamma X\Box\chi\) term and retains arbitrary background Hessian \(H_{\mu\nu}=\nabla_\mu\nabla_\nu\chi\). Einstein trace reversal supplies the scalar principal correction

\[
\Delta Z^{\mu\nu}_{\gamma^2}
=-\frac{2\gamma^2X}{M^2}(Xg^{\mu\nu}+4v^\mu v^\nu),
\quad v_\mu=\nabla_\mu\chi.
\]

There is also \(4\gamma[(\operatorname{tr}H)g^{\mu\nu}-H^{\mu\nu}]\). **It cannot be discarded on non-affine backgrounds.** The exact theorem below concerns H=0 local jets, not generic expanding solutions.

Write \(p=P_X,r=P_{XX},q=Q^2,w=W_Y,t=2\gamma^2X/M^2\). At the previously proposed proxy marginal relation \(s_0=p(W-2qC)/(WC)\),

\[
\Xi(t)=\Xi(0)+tA+t^2D,
\quad \Xi(0)=-8pz\left(r+\frac{KqCw}{WF}\right),
\]
\[
A=-8pz-2pX-4rX(q-z)-(4q-X)\frac{8pqCzw}{WF},
\qquad D=-3X^2-4X(Y-z).
\]

For \(p,r,X,W,F>0\), \(C,w\ge0\), \(0<z\le Y=q-X\), all three coefficients are strictly negative. Therefore \(\Xi(t)<0\) for every \(t\ge0\). Applying the proxy reduction additionally requires C nonzero and the stated positive clock branch. Coefficients may themselves depend on gamma; the sign result holds pointwise wherever its hypotheses hold.

`AffineCubic.lean` proves the exact polynomial expansion and three sign implications over the reals. All four axiom reports contain only propext, Classical.choice and Quot.sound; no sorry or custom axioms. The action variation, geometric identities, proxy identification and physical hypotheses remain explicit external obligations, not hidden Lean assumptions claimed as proven physics.

Bounded numerical checks retain all ten re-rooted affine longitudinal counterexamples for the actual gamma=1e-6 frozen action. The gamma-dependent coefficients change one old-point discriminant by about 45%; this work does not rely on calling every gamma effect small. Nonzero-Hessian fixtures constructed from the old physical zero-gradient history have mixed results: ten negative and ten positive discriminants across twenty direction/root fixtures. The five physical longitudinal-root/longitudinal-direction examples are negative. These are kinematic off-shell fixtures, **not solved finite-gradient histories**.

## 3. The independent momentum/charge obstruction

The [background calculation](../finite_gradient_background_2026/REPORT.md) derives curvature and metric variations independently for

\[
ds^2=-dt^2+\sum_i a_i^2(t)(dx^i)^2,\quad
\tau=\tau(t),\quad\chi=C(t)+b x,\quad b\ne0\text{ constant}.
\]

With \(Q=\dot C,Y=b^2/a_x^2,\theta=H_x+H_y+H_z\), the exact equations are

\[
\boxed{G_{0x}=0,\quad T_{0x}=bJ_\chi,\quad
J_\chi=2P_XQ-2\gamma\theta Q^2+2\gamma H_xY,
\quad \frac{d}{dt}(a_xa_ya_zJ_\chi)=0.}
\]

Comoving ordinary matter supplies no compensating momentum. The Einstein equation therefore requires zero shift charge for this finite-b homogeneous ansatz, whereas the inherited physical history has conserved charge approximately 0.0971724. At the first tested point the cubic term cancels only 0.00265% of the P-sector momentum flux. All five inherited finite-gradient points fail momentum balance. No coefficients were refitted to cancel it.

An independent energy variation gives \(\rho_{\rm clock}=QJ_\chi-P+V\). The allowed zero-charge ansatz, if it has solutions, obeys \(\rho_{\rm clock}=V-P\); it is a different charge branch, not the inherited dust history with a gradient pasted onto it. The obstruction does not exclude inhomogeneous geometry, tilted matter, differently aligned clock, or all zero-charge solutions.

## Decision and next unavoidable calculation

**DEAD under stated hypotheses:** the charged homogeneous finite-gradient continuation, and the proposed affine proxy marginal cure with positive-domain timelike jets. **OPEN:** the action's genuinely inhomogeneous, non-affine branch and the overall relativistic MOND target.

To pursue the inherited charged branch with the stated clock/matter alignment, the next calculation must solve the **uneliminated Hamiltonian and momentum constraints plus both field equations on actual inhomogeneous finite-gradient data of this unchanged action**, then evaluate the complete scalar-metric principal operator including its solved Hessian. It must account for local shift-current transport instead of silently deleting the inherited charge. A local root, stress degeneracy, or another reconstruction of coefficient functions is not that calculation. If no such healthy continuation exists, this route to the target fails; changing the architecture or pursuing the other explicitly open branches is a separate research decision.

None of the current results establishes the full nonlinear constraint count, global well-posedness, CMB transfer, galaxy dust depletion, empirical PPN bounds, exact MOND force and lensing together, or a first-principles kappa=1/2. The broader framework has not acquired those missing certificates from this calculation.

## Verification and attribution

Sixty-four targeted Python tests passed (16 new and 48 existing regressions); the four-lemma Lean build and all four current-input/output manifest validations exited zero. Independent read-only review checked the metric differential orders, cubic contractions, Hessian signs, discriminant formula and Lean compilation. Passing tests means the displayed restricted calculations reproduced, not that the theory passed every physics gate.

The research-program skill kept one frozen action and separated the parallel metric, cubic and background routes. Computation-audit supplied bounded hash-pinned runs; proof-audit and mathematical self-review kept assumptions and unproved implications explicit. No mathematical-token corrections were needed in final self-review. Carl Zimmerman's finite-gradient/primordial-clock research direction motivates this test; the numerical candidate and criticality claims being tested come from the repository's Claude L192/L193/PAPER19 work. This note neither attributes a new mechanism to a source that did not derive it nor establishes publication priority.

See [exact files](FILES.md), [commands and exit status](COMMANDS.md), and the linked subreports for full evidence.
