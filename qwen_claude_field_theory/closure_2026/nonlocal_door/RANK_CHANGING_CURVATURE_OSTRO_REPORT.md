# Rank-changing curvature projector gate — bounded obstruction

## Result

The smooth projector loophole

\[
H^{\mu\nu}(V)=-(V^2)g^{\mu\nu}+V^\mu V^\nu
\]

is algebraically rank three for a non-null vector and vanishes smoothly at
\(V=0\).  However, a metric-only covariant realization needs a curvature-built
vector; the explicit lowest-order choice audited here is
\(V_\mu=\nabla_\mu R\).

In a principal 1+1 truncation with
\(R=\partial_t^2h+qx\), one has
\(V_t\sim\partial_t^3h\) and

\[
H^{xx}=\varepsilon^2(\partial_t^3h)^2,
\qquad
\mathcal L_{\rm aux}\supset
\lambda C_{xx}\varepsilon^2(\partial_t^3h)^2.
\]

Direct variation gives

\[
\frac{\partial^2\mathcal L_{\rm aux}}
 {\partial(\partial_t^3h)^2}
 =2\lambda C_{xx}\varepsilon^2,
\qquad
E_h\supset-2\lambda C_{xx}\varepsilon^2\partial_t^6h.
\]

Thus the nonzero branch has a higher-derivative metric direction (the local
Ostrogradsky obstruction).  At \(\varepsilon=0\) the Hessian vanishes while a
linear elliptic equation with coefficient \(\varepsilon^2k^2\) requires
\(\chi=J/(\varepsilon^2k^2)\); for positive source \(J\), no finite zero-field
solution exists.  The branch therefore trades the higher-derivative mode for a
rank-changing/strong-coupling singularity and does not provide a controlled
two-tensor-DOF completion.

This is deliberately scoped to the explicit curvature realization and its
principal symbol.  It closes that metric-derived projector branch, not every
genuinely nonlocal phantom-density action.

## Reproducible checks

```text
python3 -B rank_changing_curvature_ostro_gate_2026.py
python3 -B run_lean_rank_changing.py
```

Both scripts compute their coefficients and limits; no expected ranks or
determinants are hard-coded.
