# Preservation by an ordered auxiliary heat flow

Base checkpoint: **X48-TRANSPORT-2026-11-01-B**. Research note dated
2026-11-01. This is a new analytic route for the unchanged semidiscrete law,
not a numerical fit or a proof of mesh-uniform seeding. No simulation was run.

**Main result.** A positive seed on a fixed central mass prefix preserves a
positive lower bound on every strictly smaller central prefix for all valid
times, uniformly in the number of cells. An eternal positive outer guard is
unnecessary. The proof compares the actual solution with a source-free heat
flow driven by the actual geometry; this auxiliary flow retains decreasing
entropy ordering even when the actual heated solution does not. Entropy
production and a maximum principle then give the lower bound. For each fixed
finite mesh, the same argument and the mechanical energy identity also give
global continuation of the exact semidiscrete ODE. These conclusions do not
establish a uniform continuum geometry bound or a continuum existence theorem.

## 1. Exact objects and hypotheses

Cells have fixed positive masses \(d m_i\), total mass
\(M=\sum_{i=1}^N d m_i\), ordered positive interface radii, and the exact
geometry, material gate, and luminosity from `../convective_transport.py` and
its parents. Write

\[
 W_i=W(\rho_i)>0,\qquad \chi_i=K_i/K_\star,
 \qquad \psi_i=\chi_i(W_i/\rho_q)^{3/2}.
\]

The evolution is

\[
 \dot K_i=H_i(t,K)+Q_i(t,K),\qquad
 H_i=\frac{L_{i-1}-L_i}{d m_i W_i},\qquad Q_i\geq0,
 \quad L_0=L_N=0.
 \tag{1}
\]

The actual code uses equal cell masses; unequal positive masses in (1) are
only a harmless generalization of the argument. Each interior luminosity is

\[
 L_i=c_i(t)\,
 \frac{z_i}{1+z_i}\,[\psi_i-\psi_{i+1}]_+,
 \quad
 z_i=\frac{\ell_g[(\chi_i-\chi_{i+1})/\Delta r_i]_+}
 {\chi_g+(\chi_i+\chi_{i+1})/2},\qquad c_i(t)\geq0,
 \tag{2}
\]

where \(c_i=P_0D A_i h_i h_{i+1}/\Delta r_i\). All physical scales are the
unchanged positive scales of checkpoint B. On every compact interval on
which geometry is valid, coefficients are continuous and finite and the
operator is locally Lipschitz in nonnegative \(K\). No bound on these
coefficients uniform in \(N\) is assumed below.

The supplied source is exactly

\[
 Q_i=K_\star h_i C_i(\tau C_i-1)_+
       +\frac{\zeta_i\theta_i^2}{\rho_iW_i}\geq0,
 \qquad C_i=(-\theta_i)_+.
 \tag{3}
\]

The entropy coordinate and its temperature are

\[
 \sigma_i=(K_i/K_\star)^{1/3},\qquad
 T_i=3K_\star\sigma_i^2W_i
     =3K_\star\rho_q\psi_i^{2/3}.
 \tag{4}
\]

All assertions first concern the exact ODE, not finite-tolerance accepted
steps or dense output. The comparison flow below does not solve a separate
momentum equation. Its geometry is prescribed to equal the actual solution's
geometry at each time. This is a proof device and changes no physical law.

## 2. Comparison and ordering lemmas

For nonnegative arguments, a face luminosity is nondecreasing in its supplying
\(K_i\), and nonincreasing in its receiving \(K_{i+1}\). For example, in the
strict branch \(a=\chi_i>b=\chi_{i+1}\), the derivatives of
\((a-b)/(\chi_g+(a+b)/2)\) have signs

\[
 \partial_a:\ \chi_g+b>0,\qquad
 \partial_b:\ -(\chi_g+a)<0.
\]

The positive temperature-drop factor has the same monotonicities, and both
factors are nonnegative. The zero branches preserve them. Thus \(H\) is a
cooperative ODE operator: its off-diagonal dependence is nondecreasing.
Coordinatewise comparison follows by the ordinary first-contact argument,
with the usual small strict perturbation if a contact is tangential.

Fix a valid time \(t_s\). Let \(k\) solve only

\[
 \dot k_i=H_i(t,k),                         \tag{5}
\]

with the prescribed actual geometry. If \(0\leq k(t_s)\leq K(t_s)\), then
\(k(t)\leq K(t)\) for every later valid time, since (1) is a supersolution of
(5). This comparison does not require entropy ordering of the actual \(K\)
or any monotonicity of the actual density or compression profile.

For (5),

\[
 0\leq\min_i k_i(t_s)\leq k_i(t)
      \leq\max_i k_i(t_s).                  \tag{6}
\]

At a global maximum, incoming flux is zero because the inward supplier has
no larger \(k\); at a global minimum, outgoing flux is zero. Geometry
changes do not affect either sign.

The cone

\[
 k_1\geq k_2\geq\cdots\geq k_N              \tag{7}
\]

is invariant for (5). Indeed, at \(k_i=k_{i+1}\), (2) makes \(L_i=0\), and

\[
 \frac{d}{dt}(k_i-k_{i+1})
 =\frac{L_{i-1}}{d m_iW_i}
  +\frac{L_{i+1}}{d m_{i+1}W_{i+1}}\geq0. \tag{8}
\]

For the actual heated equation there is an additional term
\(Q_i-Q_{i+1}\), whose sign is not controlled. Consequently this proof does
not silently assert ordering invariance for the actual collapse.

## 3. Entropy of the auxiliary flow, including zero temperature

When every \(k_i>0\), let \(S_k=\sum_i d m_i(k_i/K_\star)^{1/3}\). By (4),

\[
 \dot S_k
 =\sum_{i=1}^{N-1}L_i
       \left(\frac1{T_{i+1}(k)}-\frac1{T_i(k)}\right)\geq0. \tag{9}
\]

Every nonzero luminosity requires \(\psi_i>\psi_{i+1}\), hence
\(T_i>T_{i+1}\). There is no time derivative of \(W_i\) in (9), because
the entropy coordinate depends only on \(k_i\). Thus arbitrary moving
geometry does not add a term to (9).

For initial zeros, apply (5) first to initial data \(k(t_s)+\delta\mathbf1\),
with \(\delta>0\). Its minimum remains at least \(\delta\), so (9) is
classical. On every fixed compact valid interval, local Lipschitz continuity
and (6) give convergence of this positive solution to the solution with the
original nonnegative data as \(\delta\downarrow0\). Continuity of the finite
entropy sum passes \(S_k(t)\geq S_k(t_s)\) to that limit. One compares the
actual solution with the zero-limit auxiliary solution; the positive
approximants need not themselves lie below the actual solution.

This avoids assigning a finite classical entropy rate to an initially cold
recipient. It also avoids an unproved sign for an arbitrary regularized
entropy function.

## 4. Quantitative preserved prefix floor

Suppose at one finite valid time

\[
 K_i(t_s)\geq k_0>0\quad (1\leq i\leq j_s),\qquad
 M_s=\sum_{i\leq j_s}d m_i.                \tag{10}
\]

Initialize (5) with \(k_i(t_s)=k_0\) on this prefix and \(0\) outside.
Comparison, (6), (7), and (9) give

\[
 K_i\geq k_i,\qquad
 0\leq k_i\leq k_0,\qquad
 k_i\geq k_{i+1},\qquad
 S_k(t)\geq M_s s_0,
 \quad s_0=(k_0/K_\star)^{1/3}.           \tag{11}
\]

Put \(m_{<i}=\sum_{j<i}d m_j\). The ordered profile obeys

\[
 S_k(t)
 \leq m_{<i}s_0+(M-m_{<i})(k_i/K_\star)^{1/3}.
\]

Combining this inequality with (11) proves the exact bound

\[
 \boxed{\displaystyle
 K_i(t)\geq k_0
   \left(\frac{M_s-m_{<i}}{M-m_{<i}}\right)^3,
 \qquad i\leq j_s,\quad t\geq t_s.}
 \tag{12}
\]

For equal masses, the ratio is \((j_s-i+1)/(N-i+1)\). In particular, if
fixed physical masses satisfy

\[
 0<M_c<M_s\leq M,\qquad
 \sum_{i\leq j_s}d m_i\geq M_s,
\]

then every cell whose inner material mass is at most \(M_c\) satisfies

\[
 \boxed{\displaystyle
 K_i(t)\geq k_0
    \left(\frac{M_s-M_c}{M-M_c}\right)^3>0.}
 \tag{13}
\]

The constant in (13) is independent of \(N\), transport rates, density
bounds, and elapsed time. It protects the zero-inclusive prefix diagnostic
that includes cells intersecting the central mass interval. For example, a
seed through 10% of the total mass preserves the inner 5% at least at
\(k_0(0.05/0.95)^3\). This numerical example only illustrates the exact
formula; it asserts no such seed for the specified collapse.

The strict mass margin matters. If the target approaches the boundary of the
seeded region as \(N\to\infty\), the bound for its last seeded cell can tend
to zero. The lemma therefore replaces an eternal guard by a finite-time
seeded collar of positive material mass.

## 5. Tail version and fixed-mesh global continuation

The same proof applies to any tail of cells \(a,\ldots,N\). Give the
auxiliary tail a closed left boundary. The actual tail has extra inward
luminosity \(L_{a-1}\geq0\), so it remains a supersolution. If just cell
\(a\) has \(K_a(t_a)=\kappa_a>0\), use the tail seed
\((\kappa_a,0,\ldots,0)\). Formula (12) at its first cell gives

\[
 \boxed{\displaystyle
 K_a(t)\geq\kappa_a
 \left(\frac{d m_a}{\sum_{j=a}^N d m_j}\right)^3>0
 \quad(t\geq t_a).}                       \tag{14}
\]

The constant in (14) is generally mesh dependent. Nevertheless it proves
that once a particular finite-mesh cell becomes positive it remains bounded
away from zero for all subsequent valid times.

Here is a global continuation argument for each fixed \(N\) and the code's
exact conservative shell ODE. Assume initially valid geometry, finite state,
\(K_i\geq0\), and the stated positive material parameters. Suppose its
maximal valid interval had finite endpoint \(T\).

1. Classify each cell as warm if \(K_i>0\) at any time before \(T\). Choose
   one such time for each warm cell. There are only finitely many cells, so
   (14) supplies a fixed positive lower bound for each warm cell after a
   single time \(t_*<T\).
2. A cell that is never warm has \(K_i\equiv0\). Its outgoing luminosity is
   zero, while its incoming luminosity and both sources are nonnegative.
   Its old compression source must consequently vanish. Whenever
   \(V_i<d m_i/\rho_q\), its density gate is positive, so
   \(C_i\leq1/\tau\). Integrating the negative part of
   \(d\log V_i/dt=\theta_i\) below that volume threshold gives
   \[
    V_i(t)\geq
    \min\{V_i(0),d m_i/\rho_q\}\,e^{-T/\tau}>0.
    \tag{15}
   \]
3. Let \(r_1\) be the first interface radius and put
   \(B=G\sum_i\mu_i m_i\). Since \(r_i\geq r_1\), the exact discrete
   gravitational energy satisfies \(\Omega\geq-B/r_1\). If cell 1 is cold,
   (15) already bounds \(r_1\) away from zero. If it is warm, after \(t_*\)
   let its protected coefficient be \(c_1>0\). The material weight obeys
   \(W(\rho)\geq\rho\) for every density: \(W-\rho\) decreases from a
   nonnegative value to zero across the ramp, since
   \((W-\rho)'=h-1\leq0\), and is zero in the dense branch. Hence
   \[
    U\geq\frac{c_1(d m_1)^2}{(4\pi/3)r_1^3},\qquad
    E=U+T_{\rm kin}+\Omega
      \geq\frac{c_1(d m_1)^2}{(4\pi/3)r_1^3}-\frac B{r_1}.
    \tag{16}
   \]
   The right side tends to positive infinity as \(r_1\downarrow0\), so
   conserved finite \(E\) supplies \(r_1\geq\epsilon>0\). The earlier
   compact interval through \(t_*\) has valid geometry and contributes a
   positive minimum as well.
4. Thus
   \(0\leq U+T_{\rm kin}=E-\Omega\leq E+B/\epsilon<\infty\).
   Every warm cell satisfies
   \(U\geq c_i(d m_i)^2/V_i\), so its volume also has a positive lower
   bound; every cold cell has (15). Positive node masses bound all velocities
   by the kinetic energy, so all radii remain finite before finite \(T\).
   Finally \(W\geq3\rho_q/2\) bounds every \(K_i\) by the internal energy.
5. On this bounded state set with positive cell volumes and radii, centroid
   separations stay positive. The actual right-hand side has a locally
   Lipschitz extension, including its declared nonnegative-memory stage
   extension. Its solution continues beyond \(T\), contradicting maximality.

Consequently the exact finite-dimensional solution has valid geometry for
all finite times. In particular (12)--(14) then hold for all later times,
not merely up to a possible finite shell collision. The simpler special case
of simultaneous positivity follows immediately by the global-minimum
principle and steps 3--5, but simultaneous positivity is unnecessary for this
fixed-mesh continuation argument.

Every compactness constant in this paragraph can deteriorate with \(N\).
Nothing here proves a bound on individual cell densities uniform in
resolution or excludes a singular weak continuum limit.

## 6. Continuum reading and exact remaining bottleneck

The preservation implication can be stated uniformly over a sequence of
exact meshes: if there exist \(t_s<\infty\), \(k_0>0\), and fixed masses
\(M_c<M_s\) such that (10) holds with seeded mass at least \(M_s\) on every
mesh in the sequence, then (13) holds for every mesh and every
\(t\geq t_s\). A mesh-dependent seeding time bounded by a fixed finite time
also suffices, after using the same estimate from that mesh's own seed time.
The fixed-mesh continuation argument makes the all-time quantifier valid
for each exact ODE.

If these solutions converge strongly enough to a continuum material
coefficient \(K(t,m)\), for example locally in measure on material
space-time, the uniform lower bound passes to the limit almost everywhere
on \(0<m<M_c\), \(t>t_s\). A pointwise value at the exact center additionally
requires a representative with the appropriate spatial regularity. A
direct continuum version of the auxiliary proof is conditional on existence,
comparison, the ordering principle, and entropy inequality for its
degenerate heat equation; this note does not supply that PDE theory.

For the specified virgin sphere, the decisive missing input is therefore
**finite-time, mesh-uniform seeding on a fixed positive-mass prefix strictly
larger than the requested core**. It must be obtained from the actual cold
initial-value problem, with fixed physical coefficients and without a mesh
dependent seed. No measured late endpoint, isentropic equilibrium, or finite
set of grids proves this hypothesis. The other-data ordered cusp does not
refute it. Energy and total entropy alone do not prove seeding; their role
here is to preserve a seed through an ordered auxiliary flow and, at fixed
mesh only, to prevent finite-time geometric breakdown.

## 7. Provenance and verification scope

Repository HEAD when read:
`0fe706856e8a897a9ab350be4931dbf36416ada4`.
The checkpoint artifacts are not identified with that commit; the following
SHA-256 values identify the exact files read. Paths are relative to
`stable_stress_search/entropy_transport` unless prefixed `../`.

| File | SHA-256 |
| --- | --- |
| `README.md` | `8719a07f915902b829030d178636e27602f362c0f0b0e4e9e5d02039f575d2f6` |
| `DERIVATION.md` | `e08312d0dc3be7f3f2d225ca938a7872ceec6d4c2532db2102f54c7a984910da` |
| `ISENTROPIC_LIMIT.md` | `ca3245d9f786c62bdbbe352d257393580b3986c0d5c09d50e279b1900cb08fdb` |
| `convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `../material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `../collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |

Self-review scope: every displayed sign and index, zero-temperature limiting
argument, tail boundary comparison, and fixed-mesh continuation dependency.
No external theorem beyond finite-dimensional locally Lipschitz ODE
comparison and continuation is used. No numerical trajectory is a
load-bearing leaf. An independent audit is still appropriate before this
new lemma is promoted into the project's settled proof record.
