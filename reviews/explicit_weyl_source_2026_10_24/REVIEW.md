# Focused self-review

Primary verdict: correct only under the stated patch, source-regime and action restrictions. Neither tested candidate supplies the requested protecting/selection symmetry. This is self-review, not independent verification. Frozen inputs: 2b29534c88 and e5333eab45; base 69f1f60587.

## Weyl construction

- Invariance of ghat, Uhat and psihat: exponents cancel directly. For chi, delta theta=omega cancels delta log sigma=-omega, including derivatives. Unit-vector norm is unchanged.
- Gauge fixing: omega=log(sigma/f) sends sigma to f and every other variable to its listed invariant. This is valid only for positive sigma; no global claim is made.
- Operator weights: sqrt(-g), sigma^(D-p), Y^(p/2) have weights D, -(D-p), -p. Each total is zero, so their coefficients cannot be related by this Ward identity alone.
- Matter control: ds_g has weight +1 and sigma weight -1; the point-particle action is invariant. In D=4 the Dirac mass density has weight 4-1-3=0. Hatted kinetic action is invariant by construction, including the spin connection.
- Source check: the physical scalar chi is independent of the compensator gauge direction. Metric-vector mixing sources chi as in the parent. A fictitious direct source obtained by varying sigma alone at fixed other gauge-dependent fields is not used.
- Dimension check: after gauge fixing, [alpha]=mass^3, [quadratic contribution]=mass^2, [gamma]=mass, [V]=mass^4 for dimensionless chi. Canonical variables and all cancellations of f,c_K in RESULT.md follow from K=c_K f^2.
- Coefficient mutation: c_3 and c_0 can be varied separately without changing any transformation. A change of c_0 need not preserve a particular gravitational solution, so this is an allowed-operator test and not a stable-vacuum counterfamily theorem.
- Quantum scope: exact classical invariance is proved; an anomaly-free quantum completion is not. Even an exact quantum Ward identity permits the separately invariant operators. No claim that every such operator is necessarily generated is made.

## Fluid continuation

- Determinant invariance: det(J B J^T)=(det J)^2 det B=det B for a volume-preserving internal map. Arbitrary functions of b remain allowed.
- Static variation: the cofactor identity follows by antisymmetrizing commuting second derivatives. Its Euler variation vanishes for compact support and fixed orientation. This is not true for all time-dependent configurations.
- Lapse control: b=det(partial_i X^I)/sqrt(h), so the covariant density is N det J. Differentiating N prevents the flat-space boundary argument from erasing gravitational coupling. Invertible cofactor matrix makes partial_i N=0 the strictly static linear-b equation.
- Minimal example: X^I=x^I gives cofactor delta_I^i; the static equation is partial_I N=0. Replacing N by a nonconstant potential immediately violates it, checking the force conclusion independently of a spherical ansatz.
- EOS: rho=-F and p=F-bF_b give rho=V+m b, p=-V. A fluid element accelerates rather than supporting a static MOND field; no claim about all nonlinear F or multi-component fluids follows.
- Distinction from earlier determinant route: n comoving fields form a fluid current, whereas the previous n+1-field spacetime Jacobian was a different constrained medium. Their equations and state freedoms are not identified.

## Source and review boundaries

Official HTML versions 1307.1848v3 and 1210.1561v3 were authenticated by header and relevant sections. The first supplies general Weyl-lift/homogeneity background; the second supplies the fluid symmetry and stress formulas. Neither source proves a successful MOND/vacuum selection mechanism. No novel-result priority is claimed. No executable experiment or independent reproduction was performed. Mathematical prose and displayed dimensions were proofread in the new files; no unrelated manuscript was edited.
