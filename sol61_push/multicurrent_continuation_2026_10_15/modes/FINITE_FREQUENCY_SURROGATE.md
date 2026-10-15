# A separate pressureless Poisson–Gauss discriminator

2026-10-15. MC-MODES-002. Exact conditional toy calculation, not a background
solution or a halo-instability theorem. Base
`5c06d239febe644b9f485477b4c2f93390a23b3e`.

The positive principal energy and cone result in [PROOF.md](PROOF.md) cannot be
promoted to finite-frequency dynamical health. A simple surrogate demonstrates
the missing implication explicitly. Suppose two pressureless species have
positive constant rest densities \(\rho_a\), masses \(m_a\), and ratios
\(\zeta_a=q_a/m_a\). Freeze a positive electric coefficient \(p\), take a
longitudinal mode with \(k\parallel\mathbf E\), and postulate the *perturbed*
Newtonian Poisson/Gauss equations

\[
 \nabla^2\delta\Phi=4\pi G\sum_a\delta\rho_a,\qquad
 \nabla\cdot(p\,\delta\mathbf E)=\sum_a\zeta_a\delta\rho_a,
 \qquad
 \ddot\xi_a=-\partial_z\delta\Phi+\zeta_a\delta E_z.
\]

Homogeneous background gravity and charge forces have been subtracted or
externally supported by declaration. That support is not derived from the
RTM/portal action. An exactly homogeneous charged, co-moving, nonzero-density
background with a uniform electric field is not a solution of the full Gauss
law. Consequently this toy cannot by itself identify an admitted RTM halo mode.

For a Fourier perturbation, \(\delta\rho_a=-ik\rho_a\xi_a\). Eliminating
the fields and setting \(y_a=\sqrt{\rho_a}\,\xi_a\) gives

\[
 \omega^2y=\mathsf H y,\qquad
 H_{ab}=\sqrt{\rho_a\rho_b}
       \left(\frac{\zeta_a\zeta_b}{p}-g_0\right),\qquad g_0=4\pi G.
\]

Equivalently \(\mathsf H=uu^T/p-g_0vv^T\), where
\(u_a=\zeta_a\sqrt{\rho_a}\), \(v_a=\sqrt{\rho_a}\). Direct expansion gives

\[
 \boxed{\quad\det\mathsf H=
 -\frac{g_0\rho_1\rho_2}{p}(\zeta_1-\zeta_2)^2.\quad}
\]

If both populations are occupied and their ratios differ, the real symmetric
\(2\times2\) matrix has one negative and one positive eigenvalue. This toy
therefore has an exponentially growing pressureless finite-frequency direction.
Its negative quadratic direction can also be seen without the determinant:
choose \(u^Ty=0\); then \(v^Ty\ne0\) when the ratios differ, and
\(y^T\mathsf H y=-g_0(v^Ty)^2<0\). This is an independent sign check.

With \(\zeta_1^2=g_0\), \(\zeta_2=b\zeta_1\),

\[
 \det\mathsf H=-\frac{g_0^2\rho_1\rho_2}{p}(b-1)^2<0
 \quad(b\ne1).
\]

The illustrative same-charge masses give \(b=939.06542194\). At equal ratios,
the determinant vanishes: the rank-one dust mode has squared frequency
\((\rho_1+\rho_2)(\zeta^2/p-g_0)\), with a zero relative direction. At the
single critical ratio and \(0<p<1\), the nonzero toy direction is positive.

Adding diagonal sound-pressure terms gives
\(\mathsf H+k^2\mathrm{diag}(s_1^2,s_2^2)\); if both sound squares are
strictly positive, sufficiently large \(|k|\) makes it positive. The zero-speed
dust principal directions make this finite-frequency test particularly useful,
but they do not justify omitting actual background gradients, supporting forces,
conversion, finite boundaries or the constrained Einstein/matter equations.
No mode growth rate, remnant escape outcome, halo rejection, or branch closure
is inferred here. The result blocks only an automatic inference from principal
health to complete dynamical stability.

The separate [check_jeans_surrogate.py](check_jeans_surrogate.py) verifies the
determinant, an independently constructed charge-neutral negative direction,
the critical-ratio reduction, the equal-ratio spectrum, and four exact rational
examples including opposite-sign ratios and the actual portal mass ratio.
Its manifest is [run_jeans/manifest.json](run_jeans/manifest.json), with declared
scope in [jeans_contract.json](jeans_contract.json). The exact principal run is
retained unchanged. The immutable input snapshots are the same RTM and join
files pinned in that run; this run pins them again and records this note/script.
