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
2M^2 y^2e^{-y}(v_iv_j)^{TF}+k^2\Lambda_{ij}^{TF}=0,
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

The homogeneous background gate is nevertheless explicit: on flat FLRW,
({}^{(3)}R,D_i\chi,\mathcal A_n)=(0,0,0), so Q(0)=0 and the multiplier
constraints are satisfied without forcing H=0.  With positive rho+M^2 Lambda,
the background Friedmann equation has an expanding branch

\[
 H^2=\frac{\rho+M^2\Lambda}{3M^2}>0,
 \qquad c_T^2=1.
\]

This is only a background pass; homogeneous clock perturbations and the full
FLRW scalar/vector stability analysis remain open.

The generated quadratic Dirac audit separates the sectors.  For k!=0 it finds
six primary and six secondary constraints, an actual Poisson-bracket rank of
10, two first-class and ten second-class constraints, and therefore zero
physical scalar DOF from a 14-dimensional scalar phase space.  At k=0 the
same computation gives rank 0 and one homogeneous scalar DOF; this is retained
as an explicit unresolved zero-mode obstruction rather than being discarded.
The Lean certificate proves the exponential TF multiplier solution, the
opposite-shift cancellation, the finite-k DOF arithmetic, and the expanding
FLRW branch implication.

## Reproduction

```text
python3 -B tensor_compensated_branch_gate.py
python3 -B run_lean.py
python3 -B -m unittest -v test_tensor_compensated_branch.py
python3 -B tensor_compensated_dirac_gate.py
python3 -B -m unittest -v test_tensor_compensated_dirac.py
python3 -B flrw_tensor_compensated_gate.py
python3 -B -m unittest -v test_flrw_tensor_compensated.py
```
