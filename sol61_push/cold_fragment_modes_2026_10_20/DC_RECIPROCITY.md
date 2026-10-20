# DC carrier shift and mode-frequency reciprocity

**The identity is correct under the same-grid, smooth-branch, simple-mode assumptions, and it agrees with the completed DC correction to about \(4\times10^{-12}\) relative on the finest grids.** This provides a separate check of the quadratic source, raw mode charge, angular normalization, carrier-frequency derivative, and gyroscopic factors. It is a variational consistency check, not a new nonlinear evolution or physical closure claim.

The identity is

\[
 \boxed{\frac{\delta\omega_{\rm carrier}}{K_{\rm mode}}
           =\frac1\Omega\frac{d\Omega}{dQ}},
\]

where the left side means the leading carrier shift per unit quadratic mode energy at fixed **total** bound charge. The derivative on the right follows the unexcited stationary branch at fixed radial grid and boundary. The parent mode must have \(\Omega\ne0\), nonzero \(K\) norm, and a differentiable simple eigenvalue in its chosen angular sector.

## 1. Canonical-action interpretation

For a slowly modulated conservative mode, its canonical action is \(\mathcal I=K_{\rm mode}/\Omega\), consistent with the already checked intrinsic \(J=m\mathcal I\). A local normal-form energy has

\[
 E(Q,\mathcal I)=E_s(Q)+\Omega(Q)\mathcal I+O(\mathcal I^2).
\]

The carrier frequency is the derivative with respect to total charge at fixed canonical mode action:
\(\partial_QE|_{\mathcal I}=\omega_s(Q)+\Omega_Q\mathcal I+\cdots\).
This gives the displayed shift per \(K\). Holding \(K\) artificially fixed while differentiating would use a different coordinate and miss this term. The following derivation establishes the same result directly from the finite variational equations, without requiring a constructed nonlinear normal form.

## 2. Quadratic-eigenproblem derivative

Use the radial inner product including \(\Delta r\), canonical reduced order \((u,s,\xi,v,t_X)\), and the no-half convention of the natural-source calculation. The selected mode satisfies

\[
 \mathcal A(Q,\Omega)Z=0,\qquad
 \mathcal A=W(Q)-\Omega^2\mathbf1+i\Omega G(Q),
\]

with \(W^T=W\), \(G^T=-G\). For real \(\Omega\), this operator is Hermitian on the fixed Dirichlet grid. Define

\[
 \kappa=\langle Z,(\Omega^2\mathbf1+W)Z\rangle,
 \qquad M_Q=\langle Z,(W_Q+i\Omega G_Q)Z\rangle.
\]

Differentiating and multiplying by \(Z^\dagger\) eliminates \(Z_Q\). Consequently,

\[
 \Omega_Q=\frac{M_Q}{\langle Z,(2\Omega\mathbf1-iG)Z\rangle}
           =\frac{\Omega M_Q}{\kappa}.
\]

The second equality follows from the original eigenproblem, which gives
\(\kappa=2\Omega^2\langle Z,Z\rangle-i\Omega\langle Z,GZ\rangle\).
Both Coriolis terms are required; treating this as an ordinary \(WZ=\Omega^2Z\) derivative would be incorrect. There is no derivative of the eigenvector norm in this formula.

## 3. Independent DC/tangent derivation

Let \(\sigma=\sqrt{4\pi}\), \(a=(-Gp)_{\rm amp}\), and \(P=\langle p,p\rangle\), with the definitions in `DC_CORRECTION_DERIVATION.md`. The derivative of the stationary solution with respect to total charge is the linear tangent \((y_Q,\omega_Q)\) satisfying

\[
 W_{{\rm amp},0}y_Q-\sigma a\omega_Q=0,\qquad
 \sigma\langle a,y_Q\rangle+\sigma^2P\omega_Q=1.
\]

For a general mode normalization, write the carrier correction as
\(\omega_A=\omega+A^2d_\omega+\cdots\). Its completed DC equations are

\[
 W_{{\rm amp},0}w_0-\sigma a d_\omega=S_0,\qquad
 \sigma\langle a,w_0\rangle+\sigma^2P d_\omega=-Q_2^{\rm raw},
\]

where \(S_0=-r\mathcal C(Z/r)/\sigma\) and \(\mathcal C\) is the conjugate cross force. Taking the field equation against \(y_Q\), using self-adjointness and both charge equations, gives

\[
 d_\omega=-\langle y_Q,S_0\rangle-\omega_QQ_2^{\rm raw}.
\]

The part of \(W_Q\) arising from the stationary **field** tangent contracts with \(Z\) to \(-\langle y_Q,S_0\rangle\): it is the same third derivative of the potential, with the \(Y_{00}\) factor \(1/\sigma\). The explicit carrier-frequency derivative obeys

\[
 \langle Z,(W_\omega+i\Omega G_\omega)Z\rangle=-Q_2^{\rm raw}.
\]

This last equality is the direct quadratic Noether-charge formula, including charge two for \(X\). Thus \(M_Q=d_\omega\). Since \(K_{\rm mode}=\kappa A^2\), the shift per unit mode energy is \(d_\omega/\kappa=M_Q/\kappa=\Omega_Q/\Omega\). The source and the raw charge both scale with mode norm, so the result is independent of the arbitrary eigenvector normalization or phase.

This derivation checks the proposed identity; it does not replace the carrier shift by the nonlinear parent oscillation shift. Those remain different coefficients.

## 4. Cached-background numerical check

The calculation reads the six deterministic `natural_run_002` mode/background caches and completed `dc_run_001` outputs. It reconstructs the variational monopole operator from those frozen arrays and solves only the linear stationary tangent bordered system above. It performs **no new BVP, Newton profile, eigenproblem, or outgoing response solve**, and imports no original source module. `dc_run_001/manifest.json` validates with status completed.

The exact local coefficient derivatives used independently are

\[
\begin{aligned}
 (V_u)_Q&=-2\omega\omega_Q+12\lambda f f_Q+a_{\rm coupling}h_Q+2g b_Q,\\
 (V_v)_Q&=-2\omega\omega_Q+4\lambda f f_Q+a_{\rm coupling}h_Q-2g b_Q,\\
 D_Q&=-8\omega\omega_Q,\qquad
 B_Q=(-3M/4+6h)h_Q,\\
 (2gf)_Q&=2g f_Q,\qquad (\sqrt2a_{\rm coupling}f)_Q=\sqrt2a_{\rm coupling}f_Q.
\end{aligned}
\]

Here \(f_Q=y_{Q,u}/(\sigma\sqrt2r)\), \(b_Q=y_{Q,s}/(\sigma\sqrt2r)\), \(h_Q=y_{Q,\xi}/(\sigma r)\). The derivative of \(G\) replaces each \(\omega\) by \(\omega_Q\). The radial derivative and centrifugal operators have zero derivative because each comparison holds its grid and boundary fixed.

At \(L=60,N=1199\):

| \(Q\) | \(\Omega_Q\) | \(\Omega_Q/\Omega\) | Completed DC shift per \(K\) | Relative difference |
|---:|---:|---:|---:|---:|
| 80,000 | \(-3.36516129267\times10^{-7}\) | \(-4.45907758177980\times10^{-6}\) | \(-4.45907758177021\times10^{-6}\) | \(2.16\times10^{-12}\) |
| 160,000 | \(-1.65138206990\times10^{-7}\) | \(-2.94969682744431\times10^{-6}\) | \(-2.94969682743244\times10^{-6}\) | \(4.03\times10^{-12}\) |

All six cases pass the predeclared \(10^{-8}\) relative reciprocity tolerance. The separate source/tangent projection
\(-\langle y_Q,S_0\rangle-\omega_QQ_2^{\rm raw}\) also reproduces the saved DC shift. There are 38 passing cache-audit checks, including stationary-tangent residual, unit charge tangent, mode energy, Hermitian matrix element, unchanged input hashes, and measured RSS below 1 GB. Finest tangent residuals are below \(3.0\times10^{-15}\); peak RSS is 167,772,160 bytes, with conventional thread caps set to one and a 20-second CPU hard limit. This is explicitly recorded as an analytic/cache audit, not a runner-v2 field experiment.

## Limits and provenance

The equality relies on a smooth stationary branch, a simple nonzero-energy mode, consistent charge/harmonic normalization, fixed grid/boundary, and the same action coefficients on both sides. Degenerate modes require a projected matrix derivative; moving boundaries or changing coordinates require their own derivative terms. Numerical agreement at this level is a strong variational consistency check, not a continuum existence theorem, a nonlinear parent-frequency calculation, or an independent demonstration of the full decay trajectory.

The later completed `dc_run_001` supplies the finite order-\(K\) static correction and total-charge cancellation. The earlier natural-radiation review records the scope of its own pre-DC audit; this later result closes that static gate on the declared grids. The nonlinear parent-frequency shift and full evolution remain separate.

The receipt `sources_dc_reciprocity.json` records the contract established before calculation, exact before/after input hashes, reconstructed case results, software versions and resource observations. The analytic reciprocity argument and coefficient derivatives were derived independently before inspecting the numerical comparison. Mathematical self-proofreading covered the eigenproblem signs, the \(\kappa/\Omega\) denominator, angular factors, charge constraint, and distinction between fixed mode action and fixed mode energy.
