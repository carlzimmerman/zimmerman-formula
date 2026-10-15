# Coupled exterior perturbations

This calculation concerns the homogeneous constant-h exterior of [the prior inverse source](../cold_inverse_source_2026_10_14/REPORT.md), not its wall, launch, or a new finite material phase. Work in the exterior rest frame and unitary gauge ΦA = xA. Four material coordinates fix the coordinate freedom; eliminating nondynamical metric fields leaves physical modes.

Use the reduced Planck mass Mp and positive parameters D,h; set c = 1, τ = t/√D, q = Dk², r = hD/Mp². Prior assigned constants are Kc = 10^12, L = 100, μ = 2. A dot below means derivative in τ. The quadratic matter action has clock term h Kc α²/2, shift term h L Ni²/2, spatial strain −h μ hij²/4, and projected-clock regulator −h D (trace of extrinsic curvature)²/2. Constant background h is not being cut off at the wall.

Choose the wave vector along z. Write hxx = hyy = 2ζ, hzz = 2(ζ+e), and let b be the rescaled shift divergence. Dividing by the common positive normalization gives the scalar Lagrangian

\[
\mathcal L=-3\dot\zeta^2-2\dot\zeta\dot e+2\dot\zeta b
 +q\zeta^2+2q\alpha\zeta
 -\frac r2(3\dot\zeta+\dot e-b)^2
 +\frac{rK_c}2\alpha^2+\frac{rL}{2q}b^2
 -r\mu(3\zeta^2+2\zeta e+e^2).
\]

The Einstein-Hilbert part is independently obtained from its linearized Christoffel ΓΓ action, with matching Euler derivatives up to boundary terms. Solve its algebraic constraints: `α = −2qζ/(rKc)` and `b = q[(2+3r)ζdot+r edot]/[r(q−L)]`. The q = L shift constraint is degenerate and is excluded from this elimination, not classified by a divergent matrix.

For x = (ζ,e), the reduced action is `(xdot^T K xdot − x^T G x)/2`, with

\[
K=\begin{pmatrix}
\frac{(4/r+6)q+(6+9r)L}{q-L}&\frac{L(3r+2)}{q-L}\\
\frac{L(3r+2)}{q-L}&\frac{Lr}{q-L}
\end{pmatrix},\qquad
G=\begin{pmatrix}
-2q+4q^2/(rK_c)+6r\mu&2r\mu\\
2r\mu&2r\mu
\end{pmatrix}.
\]

Thus `det K = L(4+6r)/(q−L)`. For r > 0 and 0 < q < L, the real symmetric K has one eigenvalue of each sign. This is sufficient to reject positivity of the physical quadratic Hamiltonian for the unconfined prototype. It is not a claim about all curvature-coupled theories, nor a calculation of a quantum decay lifetime.

For q > L the scalar K is positive definite. G is positive definite exactly when

\[
\frac{2q^2}{rK_c}-q+2r\mu>0.
\]

At fixed q its zero boundaries are `r± = q[1 ± sqrt(1−16μ/Kc)]/(4μ)`. For the entire earlier frozen-matter band `103 ≤ q ≤ 100000`, both scalar matrices are positive only for

- `0 < r < 2.06000000001648e−10`, or
- `r > 24999.9999998000`.

These are strict quadratic exterior band conditions. Neither removes modes with 0 < q < 100, proves wall stability, or proves a causal UV completion.

Each of the two transverse vectors has positive kinetic coefficient `rL/(q+2rL)` and squared dimensionless frequency `ΩV² = μq/L+2rμ`. Each of the two tensors has positive kinetic coefficient and `ΩT² = q+2rμ`. There are six physical modes in total: two scalar, two vector, two tensor.

The scalar frequencies solve `det(Ω²K−G)=0`. In the decoupling limit r → 0 their sum is `q²/Kc+2μq/L` and their product is `2μq²(q−L)/(KcL)`, recovering the prior frozen clock/longitudinal spectrum. This checks the mixing signs rather than assuming that the earlier spectrum remains valid at finite r.

At r = 25000, q = 100000, both matrices are positive. The scalar Ω² values are approximately 1.5078938014e−8 and 70666.2222343. Differentiating the exact characteristic polynomial gives group speeds −48539.5103453 c and −0.3265111963 c. This is a boundary-sensitive dispersion calculation; the former frozen-matter bound 0.520010100002 c does not apply. Group velocity here does not settle front velocity or communication causality. No claim of superluminal spacecraft motion follows.

Evidence is in [gravity results](gravity_run_v1/calculation/results.json) and [boundary results](boundary_run_v1/calculation/results.json). The original action's engineered background remains an exact formal solution, but it lacks the physical stability needed to call it a viable source. No finite-interface repair is supplied.
