# Actual linear evolution and a growing global mode

2026-09-06. Continuation of `METRIC_CONTROL_EVOLUTION.md`.
Inspected HEAD: `6978397a4bc47f0e1bf1ded52103371a3419fff4`.

**Strongest result:** the constrained plane vacuum problem reduces to a
finite-dimensional evolution plus spatial gauge freedom. Assuming the
already identified augmented spatial inverse exists, this gives actual
linear solutions and continuous dependence, not merely formal time jets.
The computed fixed-wall evolution has growing global modes on all four
tested backgrounds. **Fixed-wall linear stability: FAIL. Full theory: OPEN.**

This is not an empirical prediction, a proof of historical novelty, a local
scalar-ghost diagnosis, or a universal no-go for relativistic MOND.

## 1. Same action, same boundaries

Keep the CMC Hamiltonian, ordinary minimally coupled KG matter, and
\(F(z)=2[1-(1+\sqrt z)e^{-\sqrt z}]\) of the preceding reports. No kernel
or coupling is changed. The background is
\(ds^2=-N(z)^2dt^2+dz^2+A(z)^2(dx^2+dy^2)\) on
\([-L,L]\times T^2\), with a smooth positive-field branch. The induced
wall lapse N and transverse scale A are fixed; the normal metric B is not.
The action was varied before setting background B=1.

Work at linear gravitational amplitude about the static vacuum. This is
the epsilon-squared gravitational order in the earlier matter experiment.
Write fractional perturbations \(\alpha=\delta A/A,\beta=\delta B\),
\(v=\delta N/N\), and \(b_0=A'/A,u=N'/N\). Set

\[
D=\beta-\alpha,\qquad V_0=\int A^2dz,\qquad
Q=V_0^{-1}\int A^2(3\alpha+D)dz,\qquad \bar p=\delta\bar\pi.
\]

Thus Q is the fractional spatial-volume perturbation. The homogeneous
trace momentum is retained. It is not set to zero to remove an instability.

## 2. Solve the canonical constraints first

The plane kinetic Hamiltonian is

\[
H_{kin}=\int N[-P_AP_B/(4A)+BP_B^2/(8A^2)]dz.
\]

At linear order the CMC constraint gives

\[
P_B=\tfrac23A^2\bar p+P,\qquad
P_A=\tfrac43A\bar p-P/A.
\]

The radial momentum constraint becomes

\[
(AP)'=AJ,\qquad J=\sum p_\phi\phi'.
\]

In vacuum, therefore, \(P=C(t)/A\). Direct Hamilton differentiation gives

\[
\dot D=\frac{3N}{4A^2}P,\qquad
\dot Q=-\frac{\langle N\rangle}{2}\bar p,\qquad
\langle N\rangle=V_0^{-1}\int A^2Ndz.
\]

Define
\[
f=\frac{3N}{4A^3},\qquad \kappa=\int f/A\,dz>0,
\qquad X=\kappa^{-1}\int D/A\,dz.
\]
Then \(D=D_g+fX\), with \(\int D_g/A=0\), and \(\dot X=C\).

**The discarded functional direction really is spatial gauge.** For any
such Dg, let \(\xi=A\int_{-L}^{z}D_g/A\,ds\). Then xi vanishes at both
walls, \(D_g=\xi'-b_0\xi\), and its reconstruction is
\(\alpha=b_0\xi,\beta=\xi',v=u\xi\).
The code verifies all three linearized spatial Euler–Lagrange equations
for this perturbation on the full constrained background. The gauge
profile is static in vacuum. Conversely, Q and X are invariant under
these boundary-fixing spatial transformations, by integration by parts.

## 3. Two spatial solves determine the entire vacuum evolution

For specified D,Q, reconstruct alpha,v and \(d=\dot{\bar p}\) from

\[
\mathcal J_\ell[\alpha,v]=-\delta E_\ell[0,D,0],\qquad
\mathcal J_\tau[\alpha,v]=2d/N-\delta E_\tau[0,D,0],
\]
\[
\alpha=v=0\text{ at both walls},\qquad
\int A^2\alpha=\frac{V_0Q-\int A^2D}{3}.
\]

The operators are the actual linearized spatial variations of the same
action. Every lower-derivative term is included. The augmented inverse is
the same one proved to exist on sufficiently small regular slabs in
`METRIC_SHARED_DATA.md`; fixed finite numerical cases additionally carry
ODE, boundary, mean, and independent integration checks.

The remaining force is

\[
\dot P=\delta EL_B-\tfrac23A^2d,\qquad
\dot C=A\delta EL_B-\tfrac23A^3d.
\]

It is spatially constant: the radial Noether identity gives
\(\delta EL_B'=A'\delta EL_A+N'\delta EL_N\); the lapse equation sets
delta EL_N=0 and the trace equation gives
\(A\delta EL_A+\delta EL_B=2A^2d\).
Differentiating the displayed force therefore gives zero exactly.

The gauge reconstruction has zero d and force. Thus solving only
\((D,Q)=(f,0)\) and \((0,1)\) determines the four coefficients below:

\[
\boxed{\frac d{dt}
\begin{pmatrix}X\\C\\Q\\\bar p\end{pmatrix}
=\begin{pmatrix}
0&1&0&0\\F_X&0&F_Q&0\\
0&0&0&-\langle N\rangle/2\\d_X&0&d_Q&0
\end{pmatrix}
\begin{pmatrix}X\\C\\Q\\\bar p\end{pmatrix}.}
\]

This is an evolution equation derived from constraints and Hamilton's
equations, not an imposed dispersion relation. Matrix exponentiation
provides actual linear vacuum solutions. To reconstruct the multiplier,
set \(\ell_{eff}/2=\dot\alpha+NP_B/(4A^2)\). The Q equation ensures its
weighted mean vanishes; the D equation then supplies the radial metric
velocity. The trace equation and the computed PB force supply the PA
momentum equation. Thus no remaining plane Hamilton equation is replaced
by the matrix ansatz. On a fixed regular slab its
finite matrix and bounded gauge reconstruction give continuous dependence
on constrained initial data. An exponentially growing finite-dimensional
mode is compatible with this well-posedness; well-posed does not mean stable.
No uniform shrinking-slab bound or nonlinear existence theorem is implied.

## 4. Symplectic and boundary checks

Pulling back the canonical one-form gives

\[
\Theta=\kappa C\,dX+\frac{2V_0}{3}\bar p\,dQ,\qquad
H_{kin}=\frac{\kappa C^2}{2}-\frac{V_0\langle N\rangle}{6}\bar p^2.
\]

The reduced form is nondegenerate. Its computed matrix rank is reported,
not assigned. The necessary reciprocity condition
\(\kappa F_Q=(2V_0/3)d_X\) is independently satisfied by the spatial
responses. The global trace kinetic term is negative, but a local ghost
or full quantum interpretation is not inferred from that sign alone.

Numerically the state is \(Y=(X,LC,Q,L\bar p)\) and time is
\(\tau=t/L\). The reported symplectic matrix is L times the literal
pullback in these coordinates; its symmetric product with the generator
is the Hessian of \(L^2H_{physical}\). This common positive normalization
does not change the evolution or energy signs.

There is no extra zero-total-energy equation in the specified Dirichlet
problem. For the boundary-completed density
\(\mathscr H_D=H_{kin}+H_m-L_{static}\), lapse homogeneity yields

\[
H_D=\int N\frac{\delta H_D}{\delta N}dz
+\left[N\frac{\partial\mathscr H_D}{\partial N'}\right]_{-L}^{L}.
\]

On the lapse constraint this is the boundary charge

\[
\boxed{H_D=\left[-\frac{4NAA'}B
-\frac{4A^2 e^{-y}N'}B\right]_{-L}^{L},\quad
y=\frac{N'}{NBa_0}.}
\]

The code verifies the Euler homogeneity and charge expressions exactly.
Fixing wall N,A does not fix their normal derivatives or this charge.
An arbitrary global lapse rescaling would violate the prescribed wall
lapse. Importing a zero-energy constraint from a closed-leaf problem would
change the boundary problem. No such extra constraint has been identified
that removes these modes.

## 5. The stability gate fails

Two independent spatial integrators determine each matrix. Matrix
exponentiation is checked against a separate time integration, and the
quadratic invariant is checked along that evolution.

| y0 | Lambda/a0 squared | L | Largest real growth exponent in tau |
|---:|---:|---:|---:|
| 0.5 | 0 | 0.02 | 0.106155796 |
| 0.5 | 0 | 0.01 | 0.075260637 |
| 10.5 | 32 pi | 0.002 | 2.636758053 |
| 10.5 | 32 pi | 0.001 | 1.003208903 |

Physical-coordinate growth rates are these numbers divided by L, in the
code's c=a0=1 units. The first two cases have one real growing/decaying
pair and one oscillatory pair. The third has two real pairs. The fourth
has a complex quartet with nonzero real parts.

The block determinant independently gives

\[
p(\lambda)=\lambda^4+(h d_Q-F_X)\lambda^2
+h(F_Qd_X-F_Xd_Q),\qquad h=\langle N\rangle/2,
\]

using consistently time-scaled coefficients for the numerical matrix.
For y0=0.5,L=0.02 it is approximately
\(\lambda^4+0.000240075365\lambda^2-0.000129696977\).
The negative constant forces a positive real root for this computed
polynomial; the conclusion does not depend only on an eigensolver label.

At high field a float characteristic-polynomial comparison initially
failed because large products nearly cancel. That audit failure was not
hidden or fixed by loosening the threshold: the final code verifies the
determinant identity with exact rational representations of the computed
binary matrix and checks its roots at 50-digit precision. This certifies
the identity for that matrix, **not** the continuum BVP coefficients.

Eigenvector condition numbers are about 2.8e3–2.5e4. Growth exceeds the
refinement-and-conditioning sensitivity scale by at least 6e5 in all
four cases. Those scales are not interval error enclosures. The two slab
sizes are different regulated systems, not a claim of a UV dispersion law.
These results reject linear stability of the tested fixed-wall global
branches. They do not establish an instability of every cosmology,
every boundary completion, or the unregulated bulk theory.

## 6. Smooth conserved forcing: analytic extension and its limit

For a prescribed smooth matter stress satisfying the canonical Ward
identity, set
\[
I_J(z,t)=\int_{-L}^z AJ\,ds,\quad AP=C+I_J,\quad
g_J=\kappa^{-1}\int f I_J/A\,dz.
\]
Then \(\dot X=C+g_J\),
\(\dot D_g=f(I_J-g_J)\), and the latter is a known zero-weight-mean
profile. The source-only spatial solve supplies d_src and a force obeying
\((A\dot P)'=A\dot J\). Hence

\[
\dot C=F_XX+F_QQ+F_{src}(t),\quad
\dot{\bar p}=d_XX+d_QQ+d_{src}(t),\quad
\dot Q=-\langle N\rangle\bar p/2.
\]

Here \(F_{src}=A\dot P_{src}-\partial_t I_J\) is spatially constant.
The fixed inhomogeneous matrix equation has the variation-of-constants
solution. This removes the merely-formal obstruction to **linear** forced
evolution for smooth admissible stresses, assuming the same spatial inverse.
The forced case has not been numerically evolved in this script.

The preceding nonlocal curvature calculation can therefore be interpreted
within actual leading-order linear evolution, not just an arbitrary jet
sequence. Upgrading it to a nonlinear causal no-go still requires a regular
nonlinear solution family and its admissibility. No nonlinear existence or
full matter-backreaction theorem is claimed.

## 7. Status, latest work, and the next calculation

**DEAD as a claim of linear stability on these tested Dirichlet vacuum
patches; OPEN as a full field theory.** The linear existence gap is narrowed
substantially, but now the retained global sector supplies a concrete
instability to explain. It cannot be removed by silently imposing
bar p=0, Q=0, or an absent zero-energy equation.

Next, reconstruct the growing eigenmode in the full boundary phase space
and test nonlinear constraint/compatibility admissibility with the same
boundary charge. That determines how directly this linear instability
extends to a regular nonlinear branch. Changing the global completion is
a different declared calculation and must preserve the original physical
requirements; it is not an automatic repair.

Latest inspected committed work remains g03r. The newly observed untracked
g03s growth experiment uses the other dynamical scalar model and includes
surrogate dynamics. Its inspected output was incomplete, not a completed
PASS or FAIL of cosmological closure. Neither supplies a gate for this CMC
Hamiltonian. No external novelty claim or new empirical fit is made here.

## 8. Files and reproduction

Five new files: this report, `metric_global_evolution.py`,
`test_metric_global_evolution.py`, `metric_global_evolution_results.json`,
and `metric_global_evolution_manifest.json`. Previous files are unchanged.
No commit or push was made.

From the repository root:

```bash
OPENBLAS_NUM_THREADS=1 python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_metric_global_evolution.py' -v
OPENBLAS_NUM_THREADS=1 python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_global_evolution.py --output qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_global_evolution_results.json
OPENBLAS_NUM_THREADS=1 python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_global_evolution.py --require-no-growing-global-mode
OPENBLAS_NUM_THREADS=1 python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_*.py' -v
```

Final runs: new tests **10/10, exit 0** (3.558 seconds); full regression
suite **98/98, exit 0** (52.195 seconds); producer **exit 0** (4.051811
seconds); strict no-growth requirement **exit 2**. Earlier test-first runs
exited 1 before implementation. The initial high-field float-polynomial
comparison also exited 1; its cancellation was diagnosed and the exact
matrix identity check added before the final reruns. `git diff --check`
exited 0.

Exact exit statuses, software versions, numerical bounds, and hashes are
recorded in the manifest. Audit exit 0 is separate from stability: the
strict stability requirement exits 2 for failure or an unresolved result.
