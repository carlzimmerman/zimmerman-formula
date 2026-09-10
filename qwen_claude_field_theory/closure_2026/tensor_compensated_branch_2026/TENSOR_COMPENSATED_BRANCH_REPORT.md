# Tensor-compensated elliptic branch

The constructive action extension is

\[
S_{TC}=S_{DDM}+
\int\sqrt{-g}\;\Lambda^{\mu\nu}
 \left[D_\mu D_\nu\chi-D_\mu a_\nu\right]^{TF},
\]

with (Lambda^{mu\nu}n_\nu=0) and (q_{\mu\nu}\Lambda^{\mu\nu}=0).  In the
static weak-field limit the multiplier equation is the trace-free Hessian
(k^2(\chi-\Phi)^{TF}=0).  The metric trace-free equation has the principal
form

\[
2M^2\mu(y)(v_iv_j)^{TF}+k^2\Lambda_{ij}^{TF}=0,
\]

so, for (k\ne0), (Lambda_{ij}^{TF}) is solved elliptically and cancels
the MOND anisotropic stress.  The induced (\Phi) and (\Psi) scalar shifts
are opposite and cancel in the summed AQUAL equation.  The new operator is
purely spatial, so the tensor principal ratio remains (c_T^2=1).

For a spherical source, the (l=2) tensor
((\hat r_i\hat r_j-\delta_{ij}/3)) has exactly zero angular average; the
homogeneous (k=0) source therefore vanishes in this branch rather than being
silently discarded.

This is a genuine constructive principal-symbol result, but not full closure.
The nonlinear covariant Dirac chain for the tensor multiplier, the complete
3-D metric variation, PPN parameters, FLRW perturbations, and stability remain
to be derived from this action.  The branch is status OPEN, not certified.

## Reproduction

```text
python3 -B tensor_compensated_branch_gate.py
python3 -B run_lean.py
python3 -B -m unittest -v test_tensor_compensated_branch.py
```
