# C4 slip-lock multiplier: constructive action-level result

I tested the most favorable static scalar reduction of a traceless geometric
multiplier. The action is

\[
L=2k^2\Phi\Psi-k^2(\Phi^2+\Psi^2)+U(\Phi)+\Sigma(\Phi)\Psi
 +\lambda k^2(\Phi-\Psi)-J\Phi,
\]

with \(U'(\Phi)=M\) the desired MOND flux and \(\Sigma\) the MOND carrier's
traceless Hilbert stress. Direct differentiation gives

\[
\begin{aligned}
E_\Phi&=-J+M-2k^2\Phi+2k^2\Psi+k^2\lambda,\\
E_\Psi&=2k^2\Phi-2k^2\Psi+\Sigma-k^2\lambda,\\
E_\lambda&=k^2(\Phi-\Psi).
\end{aligned}
\]

For \(k\ne0\), the multiplier enforces \(\Phi=\Psi\), but the multiplier
cancels identically from the sum:

\[
E_\Phi+E_\Psi=M+\Sigma-J.
\]

Therefore imposing the exact MOND equation \(M=J\) simultaneously with both
metric equations forces \(\Sigma=0\). For the exponential Class-A carrier,

\[
\Sigma_{\rm cov}(s)=-\mu(s)s^2=-[1-e^{-s/a_0}]s^2\ne0
\quad(s>0),
\]

so the multiplier enforces no slip only by leaving the MOND equation
inconsistent. A local compensator with \(C_\Psi=-\Sigma(\Phi)\) and
\(C_\Phi=0\) also fails the mixed-variation integrability condition whenever
\(\Sigma'\ne0\).

This closes the C4 multiplier attempt at the static action level. It is a
bounded action-level obstruction, not a universal theorem against genuinely
nonlocal phantom-density actions.

## Reproducible commands

```text
python3 -B slip_lock_multiplier_candidate.py
python3 -B run_lean_slip_lock.py
```

The Python gate reports 8/8 checks; Lean certifies the multiplier constraint,
the summed Euler equation, and the implication
\(M=J\) plus both metric equations \(\Rightarrow\Sigma=0\).
