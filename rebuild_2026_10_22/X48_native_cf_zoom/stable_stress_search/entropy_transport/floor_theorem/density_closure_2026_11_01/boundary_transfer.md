# Adverse-boundary transfer and a new common collar estimate

Base: **X48-NLC-2026-11-01-B**, with the unchanged X48 virgin-sphere
equations. Observed shared HEAD: `3d29c9e008429bcc115f0ac1a43532c468aaac79`.
The source hashes below pin the actual inputs. Write scope is this file
only; no equation, initial state, grid, previous proof note, or run artifact
was changed.

**The requested common central-quarter interval is still unproved.** A
uniform time-integral of the adverse ghost value does not follow through
the earlier maximum-principle barrier without an additional kernel estimate.
This note establishes two new facts. First, the coarse moving-graph class
with only density/radius bounds really can have unbounded separated
`L1(time) -> Linfinity` boundary transfer; an exact-geometry capacity-growth
construction demonstrates this. Second, the actual conserved energy and
the one-sided prefix compression cap imply a mesh-uniform bound on the
total time variation of *all prefix cell volumes together*. Consequently
one may select a fixed artificial cut, with a fixed finite halo, whose
capacities remain uniformly close to their activation values throughout
one common time. The counterexample violates the conserved-energy
hypothesis and is not a counterexample to the specified IVP. The last
pointwise kernel implication for the energy-constrained actual class is
not proved here.

## 1. Exact transfer obligation

Use `s=t-t_a`, `M=pi/3`, `dm=M/N`, `a=4^(-1/3)`, and

\[
 V_i={4\pi\over3}(r_i^3-r_{i-1}^3),\quad
 a_i={(4\pi r_i^2)^2\over dm},\qquad
 (L_rf)_i={a_i(f_{i+1}-f_i)-a_{i-1}(f_i-f_{i-1})\over V_i}.
 \tag{BT1}
\]

All edges below lie strictly inside the physical outer node, so their
nodal masses are exactly `dm`. At the activation time `V_i(0)=dm`.
Choose a cut `k`, with physical comparison cells `1,...,k-1`, and put

\[
 Q(s)=\nu_d(s)L_r(s),\qquad
 q^k(s)={\nu_d(s)a_{k-1}(s)\over V_{k-1}(s)}e_{k-1}.
 \tag{BT2}
\]

Here `L_r` has zero cut value, and `P^k(s,v)` is its positive propagator.
For a nonnegative imposed cut value `h`, its exact response is

\[
 b_i(s)=\int_0^s [P^k(s,v)q^k(v)]_i h(v)\,dv.
 \tag{BT3}
\]

The cut-stress identity in `../nonlinear_closure_2026_11_01/bootstrap.md`
has adverse value `h=S_{k,-}/nu_d`. The independent exact constitutive
estimate in `adverse_trace.md` gives, under `x_k<=U`,

\[
 \int_0^T h(s)\,ds\le {U^3e^{2UT}\over4}T,
 \qquad T\le\min(10^{-3},\log(2)/U).
 \tag{BT4}
\]

Thus the needed operator input is a bound

\[
 \sup_{N\ge32}\sup_{i\le\lceil N/4\rceil}
 \sup_{0<v<s\le T}[P^k(s,v)q^k(v)]_i <\infty,
 \tag{BT5}
\]

with a sufficiently small resulting product, or an estimate tailored to
the actual constitutive history that is weaker than (BT5). A bound for
the response to `h=1` controls the *integral* of this kernel, not its
supremum. The earlier exponential barrier establishes the former. It
cannot be multiplied by `||h||_L1` to establish (BT5).

The standard capacity energy also has an important sign distinction:

\[
 {d\over ds}{1\over2}\sum_i V_i f_i^2
 =-\nu_d\sum_i a_i(\Delta f_i)^2
       -{1\over2}\sum_i V_i x_i f_i^2.
 \tag{BT6}
\]

An upper cap `x<=U` permits the last term to be arbitrarily positive.
An estimate of (BT6) from above by `U*energy` requires `x>=-U` instead.
This is why the two-sided-capacity energy in the older actual-graph note
does not automatically apply under the newer one-sided cap.

## 2. Why the coarse geometry class is insufficient

This subsection concerns a deliberately stated coefficient class, not
solutions of the momentum/entropy IVP. The class consists of smooth
ordered radii, the exact volumes and conductances (BT1),
`rho_i=dm/V_i<=exp(1/100)`, `r_i<7/5` on the comparison prefix, and
`x_i=-V_i'/V_i<=U`. No kinetic-energy or momentum equation is imposed.
In this class (BT5) fails, even for a fixed positive observation time
and a macroscopic separation between the cut and the observation cell.

Here is a finite-chain construction and the reason for the divergence.
Take `k=floor(5N/8)` and `j=k-1`, choose a time `s_0>0`, and start with
`V_i=dm`. Put a nonnegative cut pulse of integral one in an interval of
length `epsilon_N=o(N^-2)` near `s_0`. At its end the value at cell `j`
is

\[
 f_j=(1+o(1)){\nu_d(s_0)a_j^-\over dm}=\Theta(N^2),
 \tag{BT7}
\]

and all other contributions are nonnegative. Immediately afterwards,
increase `V_j` smoothly from `dm` to `dm+delta`, on another
`o(N^-2)` interval, leaving every other volume fixed. Here `delta>0`
is small and independent of `N`. Reconstruct all radii by summing the
volumes. This keeps the geometry ordered, decreases the density of the
one changing cell, and has `x_j<=0`, `x_i=0` otherwise. By choosing
`delta` small, all prefix radii remain below `7/5`. During this change
the maximum row rate is `O(N^2)` on this time interval, so its duration
can be chosen sufficiently small that (BT7) changes by a relative
`o(1)`. All these histories may be smoothed; no coefficient jump is
essential.

Freeze the geometry after that change and set the boundary input to
zero. Write `L^+` for this fixed operator and use operational time
`theta=int nu_d ds`. If `H_i(theta)` is the probability that the
finite killed chain with generator `L^+` has reached its cut by time
`theta`, then the elementary resolvent identity is

\[
 \int_0^\tau [e^{\theta L^+}e_j]_i\,d\theta
 ={V_j^+\over a_j^+}H_i(\tau).
 \tag{BT8}
\]

Indeed `L^+1=-(a_j^+/V_j^+)e_j`; integrate
`(d/dtheta)e^{theta L^+}1` to get (BT8). For any fixed positive
operational horizon `tau`, one may choose `delta=delta(tau)>0` so that

\[
 \inf_{N\ \mathrm{sufficiently\ large}}
 H_{\lceil N/4\rceil}(\tau)>0.
 \tag{BT9}
\]

For completeness this last assertion needs no continuum limit. On an
annulus containing the path from `N/4` to the cut, the fixed conductances
are between `cN` and `CN`. Split that annulus into blocks of length
`ell N`, with `ell>0` fixed and small. In a block not containing `j`,
the exact resistance formula gives a lower bound `p>0` for right exit
from its middle; the Green formula bounds the mean exit time by
`C ell^2`. Markov's inequality then gives right exit by
`C'ell^2` with probability at least `p/2`. In the final block the
extra capacity contributes at most `C delta ell` to that mean exit
time. Choose `delta<=ell`. Repeating the finite-chain strong Markov
property over at most `C''/ell` blocks gives a success probability at
least `(p/2)^(C''/ell)>0` within total operational time at most
`C'''ell`. Choose `ell` so that this time is below `tau`.
The constants are independent of `N`; rounding is harmless for all
sufficiently large `N`. This proves (BT9).

Multiply (BT8) by (BT7). Since `a_j^-/a_j^+` is bounded below and
`V_j^+/dm=1+delta/dm`, the time integral of the output at the separated
observation cell is at least `c(tau)N`. On a fixed physical time
interval after `s_0`, operational and physical times are comparable.
Its maximum output therefore diverges with `N`, although the input
has `L1` norm one. This proves the asserted failure for the stated
coarse coefficient class, on arbitrarily small fixed positive horizons.

The construction uses prescribed boundary input, not an assertion that
this input equals an admissible constitutive stress from the full IVP.
Its use is narrowly to rule out an operator estimate based only on the
listed coarse geometry assumptions. In particular it does not refute
(BT5) in the actual energy-constrained class or the desired compression
claim.

## 3. Actual energy forbids that mechanism: uniform flux and volume variation

The following is a new actual-solution estimate. Assume on `[0,T]` only
the one-sided prefix cap

\[
 x_i(s)\le U\quad(i\le J:=\lfloor3N/4\rfloor),\qquad
 UT\le1/100,\quad T\le10^{-3}.
 \tag{BT10}
\]

The lower bound on `x` is unrestricted. The exact physical energy and
`K>=0` imply, by the density/energy geometry lemma of `bootstrap.md`,

\[
 \sum_i\mu_i u_i^2<4,\qquad r_i<R:=7/5\ (i\le J),
 \quad \rho_i\le e^{Us}\ (i\le J).
 \tag{BT11}
\]

Set

\[
 K_0=\lfloor5N/8\rfloor,\quad
 Q_*={4\pi\over3}R^3,\quad m_*={3M\over32},\quad
 B=UQ_*+{8\pi R^2\over\sqrt{m_*}},\quad
 \Lambda=B+2UQ_*.
 \tag{BT12}
\]

**Flux/variation theorem.** Uniformly in `N>=32`, throughout `[0,T]`,

\[
 -UQ_*\le F_i:=4\pi r_i^2u_i\le B\quad(i\le K_0),
 \qquad
 \sum_{i\le K_0}|V_i'|\le\Lambda.
 \tag{BT13}
\]

In particular, for every `0<=v<=s<=T`,

\[
 \sum_{i\le K_0}\operatorname{Var}_{[v,s]}V_i
 \le\Lambda(s-v),\qquad
 \sum_{i\le K_0}|V_i(s)-dm|\le\Lambda s.
 \tag{BT14}
\]

**Proof.** Exact continuity gives

\[
 V_i'=F_i-F_{i-1}=-V_ix_i,\quad F_0=0,\qquad
 F_i=-\sum_{l\le i}V_lx_l.
 \tag{BT15}
\]

Consequently `F_i>=-UQ_*`. Moreover, for `i<=K_0<j<=J`,

\[
 F_j-F_i=-\sum_{l=i+1}^j V_lx_l\ge-UQ_*.
 \tag{BT16}
\]

If `F_i>UQ_*`, every node `j=K_0+1,...,J` thus has
`u_j>=(F_i-UQ_*)/(4 pi R^2)`. Their nodal masses are all `dm`, with
total at least

\[
 (J-K_0)dm\ge M(1/8-1/N)\ge3M/32=m_*.
 \tag{BT17}
\]

The kinetic bound in (BT11) proves the upper bound in (BT13). Next,
`(V_i')_-=(V_ix_i)_+<=UV_i`, and hence

\[
 \sum_{i\le K_0}|V_i'|
 =F_{K_0}+2\sum_{i\le K_0}(V_i')_-
 \le B+2U\sum_{i\le K_0}V_i\le\Lambda.
 \tag{BT18}
\]

Integration proves (BT14). The exterior half-weight causes no change:
it was retained in the global energy lemma, while every node in (BT17)
is an interior full-weight node. QED.

This bounds *spatially summed actual capacity variation*. It does not
assume spatial regularity of compression, bounded expansion, or a lower
density cap. The rapid expansion of a single interior capacity by a
fixed `delta` in Section 2 would require an interval of length at least
`delta/Lambda` by (BT14). It therefore cannot be carried out immediately
after a pulse of duration `o(N^-2)` on an actual solution satisfying
(BT10). This explicitly identifies the missing physical constraint in
that counterexample.

## 4. A fixed cut with uniformly controlled capacity throughout the interval

Let

\[
 \mathcal C_N=\{k:\lceil7N/16\rceil\le k\le\lfloor N/2\rfloor\}.
 \tag{BT19}
\]

For `N>=32`, its cardinality is at least `N/32`. Every `k` and `k-1`
in this set lies below `K_0`, and

\[
 {k-\lceil N/4\rceil\over N}\ge1/8.
 \tag{BT20}
\]

There exists **one fixed index** `k=k(N,T)` in this set such that

\[
 \operatorname{Var}_{[0,T]}V_{k-1}
 +\operatorname{Var}_{[0,T]}V_k
 \le {64\Lambda T\over N}.
 \tag{BT21}
\]

Indeed summing the left side over all candidate cuts counts each cell
at most twice; use (BT14) and divide by `|C_N|`. Therefore throughout
the entire interval, for both `l=k-1,k`,

\[
 |V_l(s)-dm|\le\varepsilon dm,\qquad
 \varepsilon={64\Lambda T\over M}.
 \tag{BT22}
\]

If `T<=M/(128 Lambda)`, these two capacities lie between `dm/2` and
`3dm/2`, and their densities between `2/3` and `2`. The choice of cut
does not change in time, so it introduces no moving-index derivative
into Duhamel's formula. A fixed finite halo is equally available: if
each candidate cut is charged for `H` specified neighboring cells, all
lying below `K_0`, at most `H` counts per cell give a cut with total
halo variation at most `32H Lambda T/N`.

This is a simultaneous-in-time collar consequence of actual energy,
rather than a meshwise-continuity argument. It also shows exactly what
is not obtained: the selected two-cell halo is not an entire uniformly
elliptic macroscopic collar, and the other cells can still have large
relative volume changes. A time-dependent choice of a good-density
cell is unnecessary and has not been used.

## 5. What does and does not close

The strongest new actual statement is (BT13)--(BT22), conditional only
on the one-sided prefix cap (BT10), valid ordered geometry, energy
conservation, and `K>=0`. Under this cap the adverse integral (BT4) is
also available at the selected fixed cut. These are materially stronger
inputs for a separated-boundary theorem than the previous instantaneous
density/radius bounds. They rule out the explicit capacity-inflation
counterexample and provide a cut whose injection-row capacity has
uniform bounded variation relative to `dm`.

They do **not** yet prove (BT5) for the full energy-constrained moving
graph. In particular one cannot use (BT22) at two cells as if every
intermediate cell had comparable capacity; nor can (BT14), an `l1`
variation estimate, be silently replaced by a pointwise derivative bound
for each logarithmic density. The remaining precise scalar obligation
is to prove a separated Poisson-kernel estimate under (BT10)--(BT14),
possibly using the selected cut (BT21), or directly estimate (BT3) for
the actual `S_-` histories using their constitutive primitive.

Nor is a nested-collar nonlinear energy closed by selecting the cut.
The heat/stress Duhamel remainder still needs a pointwise estimate, and
the local energy work still needs a controlled quadratic norm in the
collar. A global kinetic bound controls nodal velocity, not the
compression derivative or normalized stress error. No available estimate
here supplies that missing norm or propagates (BT10) from activation.
Thus the chain to the user's target currently has three separate open
arrows: actual upper-compression bootstrap; scalar adverse-boundary
transfer in the energy-constrained class; and nonlinear interior
pointwise remainder. None is discharged by fixed-mesh activation
continuity, an unweighted `l2` estimate, or the auxiliary counterexample.

## 6. Verification and provenance

The exact equations, signs, flux telescoping, full nodal weights in the
reserved tail, ceiling indices, fixed-in-time cut selection, and
capacity-energy sign in (BT6) were self-reviewed. The counterexample
uses only finite positive matrices and exact resistance/Green identities;
no trajectory, new grid, continuum limit, or external theorem is a proof
leaf. It is explicitly outside the momentum/energy IVP. Independent
review of this note is a separate coordinator obligation.

SHA-256 paths are relative to `stable_stress_search/`:

| Input | SHA-256 |
| --- | --- |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/bootstrap.md` | `0b201a5eb41353945a1e6a374a69a3e3c290a961d6651ef9d0ff83737d5e6107` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/adverse_trace.md` | `9f2ac425673523ec6b64ca4bb2073a4b9d9c3c9291b0b40ef5b7dae640a9f291` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/all_mesh_certificate.md` | `15582ff1b45a715fccc5c84cd4883fa533ce714fb77b7ef091aa53205ba69a18` |
