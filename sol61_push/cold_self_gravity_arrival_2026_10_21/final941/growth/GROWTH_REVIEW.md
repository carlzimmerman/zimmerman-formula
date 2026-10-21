# CFG941 corrected growth: arithmetic verified, covariant scope restricted

Pinned revision: `c85e14a0d219b679c819329fb2e94424db83014b`; criteria `0b41bd0cf6bd11c49106cdec1b01c21c89f10cef`, pre-result amendment `7c395c86671d01d94a337e398667ee59036cfa85`. All 11 lane files match their bytes in the result commit. `arithmetic_audit.json` records 26/26 source/cached-arithmetic checks. No original script imports, symbolic runs, numerical eigensolvers, model reruns, or repository writes occurred.

The corrected **two-fluid primary** is n=0.6943301383991246 in saved D6, independently reconstructed here as 0.6943301383991242. The old approximation is 0.6095447174560983 (reconstruction 0.6095447174560988). The value 0.6943295059958442 is a different saved entry: R2's nominal f_t=1 row, which the source code clamps to 1-1e-10, retaining a nearly empty third component. Its roughly 6.3e-7 difference should not be interpreted as an alternative exact two-fluid endpoint or physical correction. The clean two-fluid result is the appropriate quoted value. Both remain far from the declared n=1 +/- 0.001 growth target.

## Independent smallest-matrix derivation

Let f_b=1000/6364 and f_c=5364/6364, with f_b+f_c=1. The source's reduced comoving displacement Lagrangian, at the long-wavelength stiffness limit, is

\[
 L=\frac{a^5}{2}\sum_{i=b,c}\bar\rho_i\dot\psi_i^2
  +\frac{a^5K}{2}(\bar\rho_b\psi_b+\bar\rho_c\psi_c)^2
  -\frac{a^5c_2}{2K}(-K\bar\rho_c\psi_c+b\beta\dot\psi_c)^2,
 \quad \beta=-\frac{K\bar\rho_c}{3H}.
\]

The switch b here is the source's diagnostic boost flag, not the baryon fraction. EdS has a=t^(2/3), H=2/(3t), K rho_total=2/(3t^2), and beta=-f_c/(3t). Multiplying L by an irrelevant constant 3K/2 gives

\[
 L_* = \frac{t^{4/3}}2(f_b\dot\psi_b^2+f_c\dot\psi_c^2)
 +\frac{t^{-2/3}}3(f_b\psi_b+f_c\psi_c)^2
 -\frac{c_2 f_c^2 t^{-2/3}}{12}(2\psi_c+b t\dot\psi_c)^2.
\]

For c2=b=1 the medium inertia factor is I=1-f_c/6=0.859522313010685. The mixed term -f_c^2 t^(1/3) psi_c dot psi_c/3 integrates, up to a boundary, to +f_c^2 t^(-2/3) psi_c^2/18. Together with the tether's direct potential this leaves -5 f_c^2 t^(-2/3) psi_c^2/18, in addition to the total gravity term.

Thus the equations are

\[
 t^2\ddot\psi_b+\frac43t\dot\psi_b
  =\frac23(f_b\psi_b+f_c\psi_c),
\]
\[
 I\left(t^2\ddot\psi_c+\frac43t\dot\psi_c\right)
  =\frac23 f_b\psi_b+\frac{f_c}{9}\psi_c.
\]

For density contrast proportional to comoving displacement, psi proportional to a^n=t^(2n/3), these become

\[
 n(n+\tfrac12)\binom{\psi_b}{\psi_c}
 =\frac32 M\binom{\psi_b}{\psi_c},\quad
 M=\begin{pmatrix}f_b&f_c\\ f_b/I&f_c/(6I)\end{pmatrix}
 =\begin{pmatrix}0.1571338781&0.8428661219\\0.1828153565&0.1634369287\end{pmatrix}.
\]

The larger eigenvalue, computed by the scalar quadratic formula, is mu=0.5528396068592727. The growing root of n^2+n/2-3mu/2=0 is the corrected n above. The residuals of both scalar characteristic equations are below 3e-17. Dropping the boost gives M=[[f_b,f_c],[f_b,0]], mu=0.4508780808711232 and n=0.6095447174560988. Removing the tether quadratic (c2=0) gives n=1. These reproduce the saved K3/K4 and M3 arithmetic without executing their model.

The residual medium diagonal term is also the source's quoted added force: in EdS it is K rho_c/6 times psi_c, equivalent to (K rho_c/3) q_dec psi_c with q_dec=1/2. The inertia reduction beta^2/(K rho_c)=f_c/6 is correctly normalized. These effects change the expanding-background reduced growth even though the static linear tether still cancels the corresponding static self-attraction. A static cancellation and an expanding-background growth exponent must not be conflated.

## What is retained and what is approximated

Retained: the medium's homogeneous timelike chi gradient beta; its quadratic projected-gradient cross term and velocity-squared term; free baryon displacement and medium displacement; the total Newtonian gravitational interaction; background time dependence through a, H and rho; and the source branch lambda_bar=0. The sign of the projected-gradient square is correct. The D5 fixed-FRW geometry check correctly has U^2=|grad_phys delta chi+(dot chi_bar/c^2)V|^2 at quadratic order.

Approximated/fixed: an EdS matter era with the declared constant fractions; nonrelativistic peculiar motions; scalar longitudinal displacements; leading subhorizon/quasistatic elimination of the gravitational potential and delta chi through Poisson equations; stiffness neglected at k_phys L* tending to zero; no pressure/dispersion, radiation perturbations or independent extra-field dynamics. The underlying fixed-FRW D5 constraint retains laplacian(delta chi)/a^2-3H delta chi_dot/c^2 before D6 neglects the time-derivative part in its subhorizon substitution. The growth code uses the Newtonian gravitational potential after elimination, not the complete perturbed metric with lapse/shift constraints solved covariantly.

Consequently **"full quadratic action" is too broad if read literally**: here it means the boost-complete quadratic Lagrangian *within this leading EdS/subhorizon/NR reduction*. It is not a full constrained scalar/vector/tensor expansion of the covariant parent on FRW. Metric-dependent terms in the chi constraint, non-quasistatic effects, a general nonzero-lambda background, finite-k stiffness, and the full constraint degree count require separate analysis. The exact homogeneous lambda=0 branch was independently derived in the prior vector note; it is a branch choice, not the unique homogeneous solution.

The main source does not serialize the corrected 2x2 matrix or an independent corrected-matrix eigencalculation; its visible eigenvalue control is the old CFG938 matrix, while the corrected number comes from the Lagrangian determinant. The present manual reconstruction supplies an independent small-matrix check of that reduced arithmetic. It does not validate all advertised action-level claims.

No tensor/vector stability claim follows from this growth check. In particular the source's reused static dispersion/inertia tests do not solve the expanding-background tensor coefficient or the earlier covariant-action audit. Neither the favorable inertia I here nor n<1 repairs the parent or transfers class-A shear results. No full covariance, ghost-free completion, or dwarf-core mechanism has been established by this correction.
