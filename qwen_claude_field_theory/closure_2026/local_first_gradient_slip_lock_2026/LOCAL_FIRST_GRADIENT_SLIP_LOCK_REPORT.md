# Local first-gradient no-slip slip-lock theorem

For (p_i=\partial_i\Phi), (q_i=\partial_i\Psi), write every rotationally
invariant local first-gradient density as (L(u,v,w)), where

\[
u=h^{ij}p_ip_j,\qquad v=h^{ij}q_iq_j,\qquad w=h^{ij}p_iq_j.
\]

On (p=q), direct chain-rule variation gives the two principal fluxes and
the traceless Hilbert coefficient

\[
A=2L_u+L_w,\qquad B=2L_v+L_w,qquad C_{TF}=L_u+L_v+L_w.
\]

If both independent potential equations are to share the same MOND flux
(A=B=\mu)—the local condition needed for (Phi=\Psi) for arbitrary
sources—then (L_u=L_v) and therefore

\[
\boxed{C_{TF}=\mu}.
\]

For the exact kernel (mu(y)=1-e^{-y}), (C_{TF}>0) for every (y>0).
Thus no local rotationally invariant first-gradient scalar carrier can
simultaneously have a nonzero MOND flux and vanishing traceless stress.

The Python gate derives the identities symbolically; Lean proves the algebraic
lock and the strict exponential sign.  This explains the independent
cuscuton and acceleration-khronon failures and identifies the remaining escape
space: a genuinely nonlocal metric operator or a higher-rank compensator whose
full covariant constraint algebra must still be constructed.

The Lean theorem `anisotropic_no_slip_contradiction` closes the final local
component: if the traceless field equation contains
`C*(p1^2-p2^2)=0` on a patch with `p1^2 != p2^2`, equal MOND fluxes imply a
contradiction for every `y>0`.  This is derived from the field-equation
component, not from an assumed PPN parameter.

This is not a universal no-go for all relativistic MOND theories: the theorem
does not cover nonlocal kernels, independent tensor auxiliaries, or multiple
physical metrics.

## Reproduction

```sh
python3 -B qwen_claude_field_theory/closure_2026/local_first_gradient_slip_lock_2026/local_first_gradient_slip_lock.py
python3 -B qwen_claude_field_theory/closure_2026/local_first_gradient_slip_lock_2026/run_lean_local_slip_lock.py
```
