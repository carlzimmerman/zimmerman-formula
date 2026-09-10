# Exact exponential York/QUMOND slip gate

For the corrected static carrier
\[
L_Q=-2h^{ij}\Phi_i\Psi_j+a_0^2F(u),\qquad
u=h^{ij}\Psi_i\Psi_j/a_0^2,\qquad F'(u)=\nu_{\exp}(\sqrt u),
\]
the Euler--Lagrange equations are
\[
D^2\Psi-4\pi G\rho=0,\qquad
D^2\Phi-D_i(\nu_{\exp}D^i\Psi)=0.
\]
These are obtained by direct differentiation of the action, not by inserting
the equations phenomenologically.

On a no-slip branch \(\Phi_i=\Psi_i=q_i\), differentiating the same density with
respect to diagonal inverse-metric entries gives the traceless difference
\[
\Delta_{ij}=(\nu_{\exp}-2)(q_i^2-q_j^2).
\]
More generally, replacing the fixed cross coefficient by \(A(u)\) changes the
coefficient to \(F'(u)-2[A(u)+uA'(u)]\), while the \(\Phi\) equation becomes
\(D_i[A(u)D^i\Psi]\). Retaining the ordinary Poisson equation for arbitrary
sources therefore selects \(A=1\), returning the coefficient above.
The exact exponential constitutive factor is
\[
\nu_{\exp}(x)=\frac1{1-e^{-x}},\qquad x=|\nabla\Psi|/a_0,
\]
so \(\nu_{\exp}=2\) only at the isolated point \(x=\log 2\). Lean proves that
\(\nu_{\exp}\) cannot equal 2 for every positive \(x\), using strict
monotonicity of the exponential at \(x=1,2\). Thus this carrier cannot supply
\(\Phi=\Psi\) on a finite-acceleration galactic branch; a multiplier does not
remove the residual summed metric stress (see the C4 certificate).

This is a bounded action-level obstruction for the York/QUMOND carrier, not a
universal no-go theorem for every nonlocal relativistic architecture.

## Reproduce

python3 -B exact_exponential_york_slip_gate_2026.py

python3 -B run_lean_exact_york_slip.py
