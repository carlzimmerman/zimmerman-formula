# Exact F(Q)\(\Theta\) reduced-energy gate

The exact principal scalar sector of
\[
S=\int\sqrt{-g}\left[\frac{M^2}{2}R-K(Q)+F(Q)\Theta
 +2M^2a_0^2G(|V|/a_0)\right]
\]
has, after the action-derived Dirac reduction,
\[
\Omega=-\frac{4M^2k^2}{Q_0},\qquad
H_{\rm red}=-2M^2k^2\left[A(y_0)p^2+z^2\right],
\]
where
\[
A(y)=1+(y-1)e^{-y}>0\qquad(y>0).
\]
Eliminating \(p\) from the first-order reduced action gives
\[
L_{\rm red}
=-\frac{2M^2k^2}{Q_0^2A(y_0)}\,\dot z^{\,2}
 \text{(non-kinetic terms)}.
\]
The Python gate derives this coefficient by differentiation. Lean proves
\(A(y)>0\) for \(y>0\) and therefore proves the coefficient is strictly
negative whenever \(M^2>0\), \(k\ne0\), and \(Q_0\ne0\).

The same calculation with an arbitrary principal jet gives
\[
K_{\rm red}=-\frac{U_{nz}^{\,2}k^2}{2Q_0^2U_{pp}}.
\]
Lean proves this is negative whenever the MOND stiffness \(U_{pp}\) is
positive and the metric--clock braid \(U_{nz}\) is nonzero. The ghost is
therefore structural within this mixed principal class, not a tuned numerical
artifact.

Thus the displayed F(Q)\(\Theta\) sector's one local scalar is a ghost on
the nonzero-mode branch, even though its characteristic polynomial is
oscillatory. This is a scoped obstruction to the displayed action, not a
universal no-go: adding a regulator or extra aether operator changes the
action and requires a fresh full Dirac, PPN, \(c_T\), Ward, FLRW, and
stability analysis.

## Reproduce

python3 -B fqtheta_reduced_energy_gate.py

python3 -B run_lean_reduced_energy.py
