# Independent audit of the finite-(k) AeST ghost-band claim

The repository contains two different finite-(k) reductions.  Rebuilding the
matrices in `B_decoupling_dispersion.py` gives

\[
K=\operatorname{diag}(4K_2,2K_Bk^2),\qquad
\Omega=2(2-K_B)k^2\begin{pmatrix}1&Q_0\\Q_0&Q_0^2\end{pmatrix},
\]

and the exact low-frequency Schur complement is

\[
\Omega_{\rm eff}=0,
\qquad K_{\rm eff}=4K_2+\frac{4k^2}{Q_0^2}.
\]

For the physical decoupling assumptions (K_2>0), (Q_0>0), and (k\ne0),
this is positive and has no sign-flip/ghost band.  The independent script also
checks that this expression is not equal to the separate ghost-band ansatz used
in `fc_flrw_ir_sign_certificate.py` and `fc_finitek_mink_and_expansion.py`.

The source script `C_effective_kinetic_and_decider.py` prints the same positive
Schur-complement expression but then crashes before completion on a symbolic
limit whose result depends on the sign of (H).  The independent check avoids
that unrelated limit and exits 0 with five checks passed.

This does not prove the full gravitational AeST reduction is healthy: metric
backreaction remains to be derived.  It does prove that the repository's current
finite-(k) ghost/rescue argument is not a derivation from its own decoupling
matrices, so Gate 14 cannot be certified from the present files.
