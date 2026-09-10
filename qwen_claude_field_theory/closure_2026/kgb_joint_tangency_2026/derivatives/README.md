# Fast exact-form derivative evaluator

Base: `f109d3d8ce1cdab6b5f63bea75bca83a8d4798f9`. This is a computational helper for the same explicit-clock action and imposed global-acceleration target as the preceding `kgb_universal_clock_2026/structure` package. It does not add an action function, fit mass-dependent coefficients, assign a rank, or impose health.

## Interface

```python
from derivatives.fast import single
row = single(eps, y, X, U, w, F, f)
# row['P'], row['H'], row['K'], row['Gamma']
# row['A'], row['B'], row['N']: two-vectors ordered (K, Gamma)
# row['geometry']: r, ry, g, gr, grr, rho, rhor, rhorr, B, Br
```

Here `K=P_X/f` is the normalized pressure derivative, **not** the action coefficient of `(grad X)^2`; `Gamma=G_X/f`, `f=F_X`, and `w=fX'`. Metric `B` is nested under `geometry`; top-level `B` is the two-component preservation coefficient. `W=dw/dr`, `p`, `Q`, the input state and the two chart quantities are also returned. `kappa` and `gamma` aliases support the prior convention.

The physical domain used by the tests has positive `eps,y,X,U,F`, positive metric `B`, and nonzero `f,w`. Interpretation through the invertible conformal map additionally requires `Dfield=2(F-Xf)!=0`; `Dcoord=1+rw/(2F)` is reported for the caller's chart handling. The kernels do not reject algebraic states or silently impose any numerical rank/health cutoffs. The caller must decide admissibility. Complex-step inputs are supported locally on the same square-root branch. No guaranteed floating accuracy is claimed at singularities, severe cancellations, or exponential underflow.

## Derivation and ordering

The first cached SymPy/CSE kernel computes exact-form exponential-target geometry and its radial derivatives. It treats `mu=-expm1(-y)` and `e=exp(-y)` as separate inputs, differentiating with `D_y=partial_y+e partial_mu-e partial_e` and `D_r=D_y/r_y`. This avoids subtracting nearly equal numbers when forming `mu` at small positive `y`.

The second kernel differentiates the preceding package's closed `(P,H,K,Gamma,W)` expressions in independent `X,F,r,g,rho,U,w`. It also carries `gr,rhor` and their derivatives `grr,rhorr`; these are evaluated on the target by the first kernel. Define

\[
L_0=\partial_X-2\partial_U,\quad
L_1=\partial_F+\frac1w\left(\partial_r+g_r\partial_g
+g_{rr}\partial_{g_r}+\rho_r\partial_\rho+\rho_{rr}\partial_{\rho_r}
+W\partial_w-2g(2X+U)\partial_U\right).
\]

For `q=(K,Gamma)`, the evaluator returns

\[
A=L_0q,\quad B=L_1q,\quad
N=L_0A+f(L_1A+L_0B)+f^2L_1B.
\]

The explicit, previously checked simplifications `A_K=-2 Gamma(g+2/r+3w/(2F))/p` and `A_Gamma=-Gamma/U` reduce expression size. Both mixed orders remain; `L0` and `L1` are not commuted. The inner changing vector field is differentiated. With `f_X=j`, the actual first-preservation derivative is `D_X(A+fB)=N+jB`.

Thus a common-mass solve subtracts the two returned `A,B,N` vectors. This API does not declare that the resulting lower, first, or next preservation equations possess a common root or an invariant trajectory.

## Checks and bounds

Four focused tests cover:

1. All lower outputs and `A,B,N` against independent nested `mpmath.diff` at 60 digits on five fixed states, including positive/negative `w` and `f` and both prior haloes. Vector components use relative tolerance `2e-10`; lower outputs use `2e-12`.
2. The prior matched pair independently refined at both 60 and 80 digits, comparing the normalized next determinant at relative tolerance `2e-9`.
3. A separate check through the original `nonaffine_inverse.action_curvatures`: at `j=0`, differentiate its raw `(PXX,GXX)/f` using real centered perturbations along the actual X-flow. Inner curvatures and their vector field are recomputed at each displaced state. Three fixed states use four relative step sizes and require two adjacent estimates with relative infinity-norm error below `1e-5`.
4. Complex-step differentiation of `A+fB` along shared `f_X=j`, checking `N+jB` rather than accidentally holding `f` fixed.

The old raw-curvature check does not differentiate the new kernel to generate its expected result. Its straight outer perturbation is legitimate for a first directional derivative of the already-recomputed inner curvature. A straight second difference of `q` alone would omit the changing-vector-field term and is not used.

Commands from the repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/kgb_joint_tangency_2026/derivatives/test_fast.py
python3 -B qwen_claude_field_theory/closure_2026/kgb_joint_tangency_2026/derivatives/fast.py --repeats 1000
```

The second command benchmarks one-time symbolic setup and 1000 warm scalar evaluations; it is not a scan. `RUN.md` records actual results and the input-hashed run manifest. Existing conditional preservation algebra remains in the preceding package's `SharedControlAlgebra.lean`; no new Lean theorem is claimed for this numerical compiler.

The verdict is **computationally verified only in the stated range**, using analytically generated derivatives. No interval arithmetic, exhaustive search, joint action trajectory, health result, measured mass/normalization, PPN, lensing, time-delay, CMB, or full no-dark-matter theory certificate follows from this helper.
