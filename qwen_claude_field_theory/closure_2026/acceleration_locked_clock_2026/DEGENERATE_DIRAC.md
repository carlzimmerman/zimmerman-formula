# Exact-luminal ALC corner: ADM/Dirac gate

This gate attacks the unresolved corner left by the constant-aether
regularisation.  The PPN/GW algebra already gives, on the regular denominator
branch,

\[
c_{13}=0,\quad \alpha_1=0\quad\Longrightarrow\quad c_{14}=0.
\]

The new script `alc_degenerate_dirac.py` starts from the displayed covariant
Einstein--aether contractions and derives their local 3+1 form:

\[
\mathcal L_{\rm EA}=(c_1+c_3)K_{ij}K^{ij}+c_2K^2
 -(c_1+c_4)a_i a^i+(c_1-c_3)\omega_{ij}\omega^{ij}.
\]

For a hypersurface-orthogonal clock, \(\omega_{ij}=0\).  Exact tensor
luminality and \(\alpha_1=0\) therefore remove the \(K_{ij}K^{ij}\) and
\(a_i a^i\) coefficients.  The remaining scalar combination is

\[
 c_{123}=c_1+c_2+c_3=c_2.
\]

The unreduced contraction still contains the vorticity coefficient
\(c_1-c_3\).  The script explicitly sets \(\omega_{ij}=0\) before making
the hypersurface-orthogonal claim, so the zero result below is not obtained by
silently dropping an independent variable.

For one nonzero Fourier mode of the clock perturbation, the derived quadratic
mode is

\[
L_k=c_{123}k^4\tau^2-c_{14}k^2\dot\tau^2.
\]

On the exact-luminal branch \(c_{14}=0\), the computed canonical split is:

* If \(c_{123}\ne0\), \(p_\tau=0\) is primary and its preservation gives a
  nonzero secondary proportional to \(c_{123}k^4\tau\).  The actual
  two-by-two Poisson matrix has rank 2, and multiplier preservation closes.
  This is an instantaneous/elliptic constraint channel, not a healthy
  propagating scalar.
* If \(c_{123}=0\), the derived secondary vanishes and the quadratic
  Hamiltonian vanishes.  The Poisson matrix has rank 0: the scalar principal
  symbol is rank-degenerate and nonlinear terms are unsuppressed (the usual
  strong-coupling warning).  This is not a regular two-tensor completion.
* The \(k=0\) mode is evaluated separately; its quadratic Lagrangian and
  momentum both vanish.  It cannot be inferred from the local \(k\ne0\)
  matrix and does not repair the missing homogeneous cosmological dynamics.

The same file differentiates the exact exponential primitive

\[
F(y)=\tfrac12y^2+(1+y)e^{-y}-1,\qquad F'(y)/y=1-e^{-y}.
\]

At every finite \(y>0\), its longitudinal constitutive Hessian is

\[
F''(y)=1+(y-1)e^{-y}>0,
\]

so an acceleration-based covariant completion has a nonzero finite-background
clock principal coefficient unless a separate constraint removes it.  The
script also keeps the distinction between this AQUAL primitive and the ALC
correction \(H=2F-y^2=2(1+y)e^{-y}-2\): the latter has
\(H''=2(y-1)e^{-y}\), which changes sign at \(y=1\).  Thus the exact static
constitutive law can be elliptic while the covariant correction still needs a
full constrained metric-clock principal-symbol audit.

The gate therefore sharpens, but does not overclaim, the status: the
constant-aether exact-luminal branch is **DEAD as a regular healthy
two-tensor completion**; a genuinely nonlocal or different auxiliary action
would still need a full metric/Dirac/PPN/FLRW proof.

Run:

```text
python3 -B alc_degenerate_dirac.py
python3 -B test_alc_degenerate_dirac.py
```
