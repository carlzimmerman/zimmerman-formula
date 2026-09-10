# Frame-free curvature slip-lock certificate

The exact linearized Ricci calculation in
`closure_2026/nonlocal_door/ghost_theorem_lensing.py` gives the static
curvature direction (v=(-2,4)) in the ((Phi,Psi)) basis.  Any healthy
frame-free auxiliary mode coupled through a covariant curvature scalar adds
(M=-Lvv^T), with (L>0).  For the GR scalar operator

[
G=\begin{pmatrix}0&2m\\2m&-2m\end{pmatrix},
qquad m=M_P^2 k^2>0,
]

the exact source response computed by SymPy and checked by Lean is

[
\Phi=\frac{\rho(8L+m)}{2m(6L+m)},
\qquad
\Psi=\frac{\rho(4L+m)}{2m(6L+m)}.
]

Therefore

[
\boxed{\eta=\Psi/\Phi=\frac{4L+m}{8L+m}},
\qquad
\boxed{E=\Phi/\Phi_{GR}=\frac{8L+m}{6L+m}}.
]

Lean proves for (L,m>0) that (eta\neq1) and (E>1).  Thus a
frame-free curvature mode can enhance the Newtonian response only by creating
slip; no choice of positive form factor (L(k)) removes this algebraic lock.
The statement is conditional on the linear, single-metric, frame-free
curvature-coupling assumptions.  It is not a universal theorem against
preferred-frame, tensor-auxiliary, or genuinely different metric theories.

## Reproduction

```text
python3 -B frame_free_slip_lock_gate.py
python3 -B run_lean.py
python3 -B -m unittest -v test_frame_free_slip_lock.py
```
