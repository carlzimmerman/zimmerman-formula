# The higher-wall premise is testable, and the original pair fails it

2026-09-06. Same Hamiltonian as `METRIC_SHARED_DATA.md`.

**Primary verdict: the original nonnegative-bump experiment is incompatible
with identical C5 Dirichlet KG wall histories, under the stated fixed induced
metric boundary conditions and regular amplitude expansion.** The exact
small-slab coefficient is nonzero. Four full-background numerical examples
reproduce the obstruction. This is an admissibility failure of that proposed
experiment, **not an unconditional causal no-go for the complete theory**.

This resolves rather than silently assumes the next missing implication in
the previous report. The previous common nonlinear constraints and first
preservation calculations remain valid, as does their conditional curvature
coefficient. They do not establish a realizable shared-wall experiment.

## 1. Scope, same action, and normalization

The action/Hamiltonian, finite slab times transverse torus, background seed,
positive-field branch and ordinary canonical KG fields are unchanged. Use
the static background metric

\[
ds^2=-N(z)^2dt^2+B(z)^2dz^2+A(z)^2(dx^2+dy^2),\qquad B=1
\]

only after variation. Define u=N'/N, b=A'/A,
\(\chi=(1-u/a_0)e^{-u/a_0}\). The initial matter states have
\(\phi_i=\epsilon r_i\),
\(N^{-1}\dot\phi_i=\epsilon(v_i\pm U_i\sigma(z/L))\), with the
same r,v,U as before. Each has positive energy even for signed sigma:
\(\rho=3\epsilon^2(1+\sigma^2)\).

All gravitational differences below denote half the difference with the
overall epsilon² removed. At a wall, the matter initial differences and
all their spatial derivatives vanish because sigma has interior support.
The common gravitational data and their first derivatives agree. The first
nonzero metric difference jets are

\[
\delta\ddot A=Aw,\qquad \delta\ddot B=w,\qquad
\delta\ddot N=Nv,\qquad c=\delta\bar\pi'''.
\]

Here the lapse jet v is distinct from the species velocity v_i=1. Fixed
induced N,A at both walls imply w=v=0 there. **B is the normal metric
component and is not fixed by these Dirichlet data.** Imposing all its
higher time jets to be zero would discard its Hamilton equation.

## 2. Obtain the normal fourth metric jet canonically

The plane-symmetric canonical momenta are
\(P_A=4A\pi^{xx}=4A\pi^{yy}\), \(P_B=2B\pi^{zz}\). Directly reducing
the full ADM kinetic term gives

\[
H_{kin}=N\left[-\frac{P_AP_B}{4A}+\frac{BP_B^2}{8A^2}\right].
\]

This is checked from \(N(\pi^{ij}\pi_{ij}-\pi^2/2)/\sqrt h\), not
postulated. At leading difference order, the static vacuum has pi=lambda=0;
products of common order-epsilon² corrections and the difference are higher
order. The initially equal stress and first stress jets give
\(\delta P=\delta\dot P=\delta\ddot P=0\). At the wall the second
stress difference also vanishes. Thus

\[
\delta P_A'''=\delta E_A[w,v],\qquad
\delta P_B'''=\delta E_B[w,v],
\]

where E_A,E_B are the full ungauged variational derivatives already computed
from the same static action. Eliminating the effective multiplier's third
derivative with \(\delta A^{(4)}=0\) leaves

\[
\delta B^{(4)}=N\left[-\frac{\delta E_A}{4A}
+\frac{\delta E_B}{2A^2}\right].
\]

Using the trace constraint and the varied radial equation gives the
independently checked identity

\[
\boxed{\delta B^{(4)}=-\frac{Nc}{2}
-3N^2[(b+u)w'+(b+u\chi)v'].}
\]

The third metric difference jets at the walls vanish, because the second
momentum difference derivatives vanish and the induced third metric jets
are fixed. No analogous argument sets the displayed normal fourth jet to
zero.

## 3. Derive rather than assign the fifth KG jet

The minimally coupled KG equation on a time-dependent plane metric is

\[
\ddot\phi=\left(\frac{\dot N}{N}-2\frac{\dot A}{A}
-\frac{\dot B}{B}\right)\dot\phi
+\frac{N^2}{B^2}\left[\phi''+
\left(\frac{N'}N+2\frac{A'}A-\frac{B'}B\right)\phi'\right]
-N^2m_i^2\phi.
\]

`metric_wall_jets.py` generates its product-rule time jets. In a source-free
initial neighborhood, its third matter difference jet at leading
backreaction order is

\[
\frac{\phi_{i,+}^{(3)}-\phi_{i,-}^{(3)}}{2\epsilon^3}
=Nv_i(v-3w).
\]

This and the fourth jet vanish at each wall. The fifth does not generally:

\[
\boxed{\mathcal J_5:=
\lim_{\epsilon\to0}\frac{\phi_{i,+}^{(5)}-\phi_{i,-}^{(5)}}
{2\epsilon^3N^3v_i}
=v''-3w''-3(b+u)w'
+(5b+6u+3u\chi)v'+\frac{c}{2N}.}
\]

An independent form before using the trace identity is

\[
\mathcal J_5=-\delta B^{(4)}/N^2+3u(v'+w')
+v''-3w''+(3u+2b)(v'-3w').
\]

The script proves equality and substitutes both full lapse/trace constraints
to eliminate w'',v''. No rank, fifth jet, or verdict is prescribed.

The limit notation requires smooth amplitude dependence controlling the
mixed derivatives used here (C3 in amplitude and adequate time/spatial
regularity through the fifth wall jet); equivalently this is the necessary
coefficient condition in a regular perturbative family. Pointwise unrelated
differentiability assumptions are not sufficient.

## 4. Exact nonzero small-slab coefficient

Fix a regular seed with y0>0, chi0!=0 and 1-chi0>0, and then let L tend to
zero. With z=Lx, w=L²W, v=L²V, the already derived limiting equations give

\[
w''=\frac{\chi_0 c}{2(1-\chi_0)},\qquad
v''=-\frac{c}{2(1-\chi_0)}
\]

at either source-free wall, while w',v' are O(L). The weighted mean fixes
\(c\to-9M\), where
\(M=\int_{-1}^{1}(1-x^2)\sigma(x)\,dx>0\) for the original nonnegative bump.
Consequently

\[
\boxed{\mathcal J_5\longrightarrow
-\frac{2\chi_0 c}{1-\chi_0}
=\frac{18\chi_0M}{1-\chi_0}\ne0.}
\]

The uniformly convergent shooting solutions from the preceding report also
control the derivative jets through the first-order ODE. Therefore this
nonzero wall coefficient persists for sufficiently small L; then it
obstructs identical wall histories for sufficiently small amplitudes in a
regular family. No explicit certified universal L or epsilon threshold is
claimed. Exceptional y0=0 and chi0=0 sectors are not covered.

Numerical full-background values of the normalized left/right fifth jets:

| y0 | Lambda/a0² | L | left | right |
|---|---|---|---|---|
| 0.5 | 0 | 0.02 | 3.077637 | 3.114673 |
| 0.5 | 0 | 0.01 | 3.087205 | 3.105722 |
| 10.5 | 32pi | 0.002 | -0.027405 | 0.019765 |
| 10.5 | 32pi | 0.001 | -0.014110 | 0.009411 |

The high-acceleration examples are not yet at the asymptotic same-sign
limit; lower derivative terms matter at these finite L. Independent RK45
and DOP853 solves, actual boundary matrices, differential residuals and
refinement discrepancies are retained in the JSON. Floating-point examples
illustrate, rather than prove, the exact small-L statement.

## 5. A repair that can itself be falsified

The sign of sigma is not an energy condition: each KG state's energy
contains sigma². At frozen coefficients choose
\(f\in C_c^\infty((-1,1))\) with zero integral and a nonzero constant
plateau about an interior observer. Set sigma=-f''. Then the Dirichlet
inverse is P=f, the mean equation gives c=0, and

\[
V=\frac{6f}{1-\chi_0},\qquad W=-\chi_0V.
\]

Both equations are symbolically checked. The curvature \(-3L^2W\) is
nonzero on the plateau, where the matter initial difference vanishes, while
W,V and every spatial derivative vanish near the walls. The fifth-wall
obstruction above therefore vanishes for this leading-order construction.
**This does not prove all-order compatibility or its nonlinear lift.**

For the full variable background, the concrete finite-order test is to
combine compact source basis functions, all outside the observer gap and
wall neighborhoods, and solve the five linear conditions

\[
c=w'(-L)=v'(-L)=w'(L)=v'(L)=0.
\]

Together with the original wall values, these force the homogeneous
response to vanish throughout each source-free wall neighborhood by ODE
uniqueness. The actual control-map rank and a nonzero observer response
must be computed; the frozen limit does not establish their values. This
test is implemented separately in `metric_collar_control.py`; its numerical
results and limitations are recorded in `metric_collar_control_results.json`.
It controls the displayed initial metric jets, not all subsequent evolution.

**Executed full-background control.** Ten smooth basis bumps of width 0.048
are centered at x=±0.20, ±0.33, ±0.46, ±0.59, ±0.72. They avoid the
observer gap |x|<0.15 and wall neighborhoods |x|>0.8. Each response solves
the original Dirichlet and weighted-mean conditions with c free. The
resulting five-by-ten control matrix is row-equilibrated before SVD.
Only the last ten-minus-five right singular vectors are used, which avoids
declaring small singular values to be exact zero modes. Source weights
are then selected for a nonzero observer signal and normalized, followed
by independent integration of the *combined* source, not just reuse of
the design columns.

| y0, Lambda/a0², L | observer / peak curvature | relative wall-neighborhood metric tail | relative integration discrepancy |
|---|---|---|---|
| 0.5, 0, 0.02 | 0.871244 | 1.05e-12 | 1.48e-9 |
| 10.5, 32pi, 0.002 | 0.900149 | 7.57e-10 | 1.08e-7 |

Both matrices have **computed numerical** rank four and augmented
(including observer signal) rank five. Their smallest singular values are
approximately 1.6e-15 and 1.2e-15; even the next value in the first case is
only 6.9e-8. The rank is not certified or imposed. Conditioning warnings
remain in the output. Independent five-component control residuals are
2.71e-13 and 4.87e-10 after the producer's row scaling; normalized fifth-wall
residuals are 7.16e-11 and 8.56e-7. All 22 finite numerical gates pass.
These are controlled initial-jet responses, not measured galaxy signals.

This repairs the identified wall obstruction at the computed order on
the tested full backgrounds. The next unavoidable calculation is an exact
or certified construction of these controls together with their higher
coupled corner jets and nonlinear evolution. Finite-order cancellation
does not imply compatibility to all orders. The earlier common-data
argument allows fixed signed profiles algebraically, but its nonlinear
numerical solver was not rerun for these new source weights.

## 6. Latest parallel work, without mixing actions

Remote main and local HEAD both resolved to `ebc6b05707fb0cec0169ca2d28343e330c3b7dab`.
That pushed commit withdraws g03o/p/q's dust-collapse window because the
capture fractions depend strongly on shell spacing and starting redshift.
`THE_ACTION_2026-09-05.md` section 6 and `g03o_dust_spherical_collapse.out`
explicitly record failed D2-D4. They are not closure evidence.

A useful separate local result is
`../g03_clock_constraint_2026/constraint_gate.py`: the C-H clock's
pre-caustic branch satisfies its actual Hamiltonian, momentum and all ADM
evolution equations. A read-only independent audit reproduced its zero
residuals and intrinsic curvature. Thus exclusion by canonical preservation
does not rescue that branch. This is the C-H clock/heat action, not our CMC
Hamiltonian and not THE_ACTION's dynamical scalar/khronon candidate. No
result is transferred between those three theories.

## 7. Status and reproduction

**Full relativistic MOND theory: OPEN.** The old nonnegative-bump shared-wall
witness is **DEAD under the stated C5 Dirichlet wall requirements**.
The signed-source repair is a different experiment of the same action;
finite-order wall cancellation is not yet complete coupled evolution.

New files in this continuation (same directory):

- `metric_wall_jets.py`, `test_metric_wall_jets.py`, `metric_wall_jets_results.json`
- `metric_collar_control.py`, `test_metric_collar_control.py`, `metric_collar_control_results.json`
- `METRIC_WALL_COMPATIBILITY.md`, `metric_wall_compatibility_manifest.json`

Important commands, run from the repository root:

```sh
git status --short
git log -8 --format='%h %an %s'
git ls-remote origin refs/heads/main
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_metric_wall_jets.py' -v
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_wall_jets.py --output qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_wall_jets_results.json
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_wall_jets.py --require-shared-C5-walls
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_collar_control.py --output qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_collar_control_results.json
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_*.py' -v
```

Five wall-jet tests pass, exit 0; standalone mathematical audit exits 0.
Six signed-control tests pass, exit 0; its standalone exits 0. The final
relevant suite passes **80 tests**, exit 0 (44.291 seconds).
The explicit shared-C5-wall requirement exits **2**, correctly detecting
incompatibility. The initial red-first test exited 1; an intermediate
implementation run also exited 1 on an eager lookup of an unused fourth
background matter jet, corrected by skipping its identically zero damping
coefficient. Final control/suite commands, actual statuses and hashes are
recorded in the manifest. Nothing here changes previous hashed artifacts
or unrelated work. No commit or push in this continuation.

Mathbox audit effect: an explicit unproved assumption in the previous
argument was tested and found to fail, so the causal-witness conclusion
was restricted. Math proofreading covers this new report only; the normal
fourth metric jet is retained as a load-bearing mathematical term.
