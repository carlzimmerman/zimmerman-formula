# Radial heat histories and the failure of a nonautonomous smoothing transfer

Base checkpoint: **X48-DEN-2026-11-01-A**. Observed input HEAD:
`8a293ba8b8411e84c9e37bb9770d1a6f993f606e`. The source hashes below pin
the inputs independently of subsequent shared-checkout changes. This route
writes only this file. No physical law, activation datum, material parameter,
older note, or numerical grid is changed.

**Result.** There is a new actual-law thermal-history estimate: on a controlled
prefix, the time-integrated luminosity across face j is at most
`2517*j*dm*s^3`, and the origin memory has total variation at most
`(10000/3)*s^3`, uniformly in N. In particular the origin's own accumulated
heat term in the differentiated stress is `O(s^5)`. A separate exact radial
construction refutes a proposed transfer from frozen triangular smoothing to
arbitrary time-dependent closed heat faces. It uses smooth heat clocks,
positive scalar outward heat, the first radial cell, and no mesh experiment.
It is a counterexample for that coefficient-class transfer, **not** for the
specified cold IVP. Neither result proves the requested all-origin estimate
or its common prefix/collar bootstrap.

## 1. Target and inherited actual identities

Write `s=t-t_a`, `z=log rho`, `x=-theta`,

\[
 \kappa=\tfrac12\rho Wh,\quad g=K/(K+1/100),\quad
 \nu=(1+g)\kappa,\quad P=K\rho^2h,\quad
 S=\nu x-2\kappa+P.
 \tag{R1}
\]

On the active prefix the unchanged equations are

\[
 z_t=x,\quad x_t=\mathcal L_rS+R,\quad K_t=Q+H,\qquad
 H_i=\frac{L_{i-1}-L_i}{dm W_i},\quad L_i\ge0,\quad L_0=0,
 \tag{R2}
\]

where both original heaters are retained:

\[
 Q=h\{x(x/2-1)+\tfrac12g x^2\}.
 \tag{R3}
\]

The sufficient pointwise target is, with `f=S-S_d`,

\[
 \|f(s)/s^2\|_{\ell^\infty(I)}\le Cs^\theta,
 \qquad \theta>0,
 \tag{R4}
\]

uniformly in N and through the first cell, on an actual prefix I whose
collars are controlled on the same interval. The constitutive damped-density
argument in the pinned `pointwise_continuation.md` converts (R4) into
`||x-x_d||_infinity<=C(s^theta+s^3)`. The inherited conditional inner energy
has `||f/s^2||_(L2(V phi))<=Cs^3`; it does not itself assert (R4).

The exact old-viscosity primitive and radial flux identity remain

\[
 F(\rho)=\frac{W(\rho)^2-9/4}{4},\quad \dot F=\kappa x,
 \qquad \dot J_i=S_i-B_i,\quad B_i\ge0.
 \tag{R5}
\]

They give a spatially smoothed Volterra equation. The present check concerns
the temporal information needed to recover instantaneous stress; it does
not repeat an inversion of a bounded Green potential.

## 2. An actual prefix luminosity and variation theorem

Assume the actual prefix and its necessary state-box inputs obey, for
`0<s<=T<=10^-3`,

\[
 2<x\le8,\quad 1\le\rho\le1.01,\quad
 3/2\le W\le1.51,\quad h\le200s^2,\quad
 0\le K\le1600s^3,
 \qquad K_i(0)=0.
 \tag{R6}
\]

These are conditional actual-solution hypotheses, not a uniform existence
or bootstrap conclusion. From (R3), `g<=100K`, and (R6),

\[
 0\le Q_i\le200s^2(24+3200K_i)<5000s^2,
 \qquad 0\le \dot W_i=\rho_i h_i x_i\le1616s^2.
 \tag{R7}
\]

For every face j inside the prefix define the physical prefix thermal
content

\[
 E_j^K=\sum_{i\le j}dm W_iK_i.
\]

Exact shared-flux cancellation, including the time derivative of W, gives

\[
 (E_j^K)'=\sum_{i\le j}dm\{W_iQ_i+\rho_i h_i x_iK_i\}-L_j.
 \tag{R8}
\]

The source in braces is at most
`7550*s^2+2585600*s^5<7551*s^2`. Since `E_j^K>=0` and
`E_j^K(0)=0`, integration yields the actual estimate

\[
 \boxed{\quad \int_0^s L_j(v)\,dv\le2517\,j\,dm\,s^3.\quad}
 \tag{R9}
\]

No lower bound on an open heat conductance is used. The exterior luminosity
of a prefix is retained explicitly in (R8), rather than being discarded as
an interior cancellation. From `W>=3/2`, (R2), (R7), and (R9),

\[
 \int_0^s|H_j|\le1678(2j-1)s^3,
 \qquad \operatorname{Var}_{[0,s]}K_j\le3356j s^3.
 \tag{R10}
\]

At the first cell one can do better without summing a prefix. There is no
incoming luminosity, so

\[
 K_1'=Q_1-\frac{L_1}{dm W_1},\qquad
 \int_0^s\frac{L_1}{dm W_1}
       =\int_0^sQ_1-K_1(s)\le\int_0^sQ_1.
\]

Consequently

\[
 \boxed{\quad
 \operatorname{Var}_{[0,s]}K_1\le2\int_0^sQ_1
                    \le\frac{10000}{3}s^3.\quad}
 \tag{R11}
\]

Here total variation means `integral |K_1'|` along the finite-dimensional
actual solution. The signed variation of the moving weight was already
included where needed in (R8); it is absent from this direct equation for
K itself.

The actual constitutive coefficient satisfies
`0<S_K=κ*g'*x+rho^2*h<=1.3e5*s^2`. Thus the origin's heat contribution in
`f_t=nu*L_r f+S_K H+F_local` obeys the further actual bound

\[
 S_{K,1}H_1\le0,\qquad
 \int_0^s|S_{K,1}H_1|\le\frac{6.5\,10^8}{3}s^5.
 \tag{R12}
\]

This is a uniform temporal bound on the origin's **own** heat term.
It is not a bound on the mechanical propagation of heat sources from all
other cells to the origin. In (R10), j can grow with N; replacing that
factor by a uniform constant would require another argument.

## 3. A precise smoothing transfer to test

Freezing the graph and stress coefficient suggests studying

\[
 y_t=-A_N y+cq_t,\qquad q_t=-B_N(t)q,\qquad c>0,
 \tag{R13}
\]

where A_N is the positive radial mechanical operator, B_N(t) is a positive
scalar heat operator, and, as quadratic forms,

\[
 0\le B_N(t)\le\epsilon A_N,\qquad0<\epsilon\le1/2.
 \tag{R14}
\]

For time-independent B, the triangular resolvent contains
`(lambda+A)^(-1)*c*B*(lambda+B)^(-1)`. Its algebra explains the attraction
of applying mechanical smoothing to the first component even when heat
faces close. It does not justify the same smoothing for arbitrary
time-dependent B. A concrete version of that transfer would assert, for a
fixed macroscopic time `t_*>0`,

\[
 \|y(t_*)\|_\infty
 \le C(t_*,c,\epsilon)\{\|y(0)\|_{L^2(V)}
                              +\|q(0)\|_{L^2(V)}\},
 \tag{R15}
\]

with C independent of N and of which heat faces close. The following
construction refutes (R15), even for smooth time dependence. It also
retains the scalar heat maximum principle and bounded nonnegative q.

## 4. Exact radial counterexample to (R15)

Fix homogeneous ordered radial geometry at a density `rho_*>0`:

\[
 r_i=b(i/N)^{1/3},\quad b=(1/(4\rho_*))^{1/3},\quad
 V_i=dm/\rho_*,\quad dm=\pi/(3N).
\]

Let `A_N=-L_r` be the actual radial mechanical graph at this geometry,
including its mechanical exterior Dirichlet face and half outer nodal
mass. Write `a_1=(4*pi*r_1^2)^2/dm` and

\[
 \lambda_N=a_1/V_1=144b^4\rho_*N^{2/3}.
 \tag{R16}
\]

The first cell has exactly one mechanical exit, of rate lambda_N. Denote
`P_N(u)=exp(-u A_N)`. Positivity and its row sums at most one follow
directly from the finite graph generator. Starting from row 1, the
probability of no exit gives, for `u>=0`,

\[
 (P_N(u))_{11}\ge e^{-\lambda_Nu},\qquad
 (P_N(u))_{12}\le1-e^{-\lambda_Nu}\le\lambda_Nu.
 \tag{R17}
\]

These inequalities can equivalently be obtained by adjoining one
absorbing exterior state to the finite generator. No estimate on the
outer graph rates is used.

Set `delta=1/4` and `h_N=delta/lambda_N`. For all sufficiently large N,
`h_N<t_*`. Choose a smooth clock `0<=b_N<=1` supported in
`(t_*-h_N,t_*)`, with integral at least `h_N/2`. Let B_N(t) have only
the first internal heat face open, with conductance
`epsilon*b_N(t)*a_1` and capacities V. Every other heat face is closed.
This is a scalar conservative heat operator and satisfies (R14), because
its sole quadratic-form term is bounded by epsilon times the first term
of the mechanical form. Put

\[
 y(0)=0,\qquad q(0)=q_*e_1,\qquad q_*>0.
 \tag{R18}
\]

The heat solution is constant before `t_*-h_N`. During the final interval,
using local time `r=t-(t_*-h_N)` and
`b(r)=b_N(t_*-h_N+r)`, it is exactly

\[
 q(r)=\frac{q_*}{2}(e_1+e_2)
       +\frac{q_*}{2}
          \exp\!\left[-2\epsilon\lambda_N\int_0^r b(v)\,dv\right]
          (e_1-e_2).
 \tag{R19}
\]

Thus `0<=q<=q_*`, and its only nonzero flux is outward, from cell 1 to
cell 2. Its weighted L2 energy is nonincreasing. Duhamel's formula gives

\[
 \begin{split}
 y_1(t_*)=-c\epsilon\lambda_Nq_*\int_0^{h_N}
 b(r)\exp\!\left[-2\epsilon\lambda_N\int_0^r b(v)\,dv\right]
 \{(P_N(h_N-r))_{11}-(P_N(h_N-r))_{12}\}\,dr.
 \end{split}
 \tag{R20}
\]

By (R17), the expression in braces is at least
`1-2*lambda_N*(h_N-r)>=1/2`. The exponential is at least
`exp(-2*epsilon*delta)>=exp(-1/4)>1/2`. Since the clock integral is at
least `h_N/2`, (R20) proves

\[
 \boxed{\quad |y_1(t_*)|\ge c\epsilon q_*/32.\quad}
 \tag{R21}
\]

On the other hand,

\[
 \|q(0)\|_{L^2(V)}=q_*\sqrt{dm/\rho_*}=O(N^{-1/2}),
 \qquad \|y(0)\|_{L^2(V)}=0.
 \tag{R22}
\]

The right side of (R15) tends to zero, whereas (R21) does not. This
refutes (R15). Alternatively, choosing `q_*=V_1^(-1/2)` gives unit initial
L2 norm and unbounded output; the fixed-amplitude choice above is stronger
for comparing with bounded-state arguments. Positivity, no incoming heat
at the origin, and the actual first-cell mechanical rate all survive.
The failure comes from storing a narrow memory mode while heat is closed
and releasing it only during a final radial mechanical time interval.

## 5. Exact scope and remaining actual obligation

The construction in section 4 is a solution of (R13), **not** of the
unchanged X48 startup IVP. Its adjustable smooth heat clocks do not equal
the actual constitutive gate law. Its intermediate memory spike is not
shown to arise from the prescribed spatially homogeneous cold activation
data. The actual heater (R3), moving geometry, and density/velocity
feedback are not asserted for that construction. It therefore refutes
only an argument that transfers frozen triangular smoothing using the
coefficient upper bound, scalar positivity, outward heat, and L2 data.

This distinction also prevents an incorrect conclusion about (R4). In
actual startup scaling one has mechanical rate proportional to s^2,
heat/mechanical ratio `epsilon=O(s^2)`, coefficient `c=O(1)` for
`y=f/s^2`, and available memory amplitude `q_*=O(s^3)`. The delayed
release just constructed has size `O(s^5)` in y, which is consistent
with a favorable pointwise startup power. It rules out pure L2 transfer,
not a hybrid estimate with a uniform memory-amplitude term, and not (R4).

The executed actual-history estimate (R11)--(R12) excludes uncontrolled
heat variation at the origin itself. It does not exclude a sequence of
late heat releases at radii that influence the origin through mechanical
diffusion, and (R9)--(R10) alone lose the growing cell index there. Thus the
remaining radial obligation is an actual-history estimate controlling
that spatially propagated heat work, or a hybrid stress estimate that
retains the small `||K||_infinity=O(s^3)` contribution and is uniform under
the actual gate evolution. The latter estimate has not been proved here.

No common prefix/collar interval follows from these results. The actual
all-origin bound (R4), the covering bootstrap, and (UC) remain open.
The frozen-to-arbitrary-clock construction is closed by the counterexample;
the actual radial route remains open with the preceding specific transfer
obligation. No claim that the actual route is impossible or exhausted is made.

## 6. Verification, audit, and provenance

All load-bearing steps are finite graph identities, elementary probability
for a finite nonnegative generator, and exact integration. No external
regularity theorem, physical trajectory, or finite mesh sample is used.
The actual-law proof checks the moving W weight, the prefix outer face,
the nonnegative source, the first-cell no-inflow boundary, and the j factor.
The transfer counterexample checks the true radial first-cell scaling,
nonnegative smooth clocks, the form domination, scalar energy dissipation,
and the distinction from the prescribed IVP. It requires only sufficiently
large N, which suffices to refute the asserted uniform-in-N transfer.

Primary self-audit verdict: **proved as written** for (R9)--(R12) under
(R6), and **refuted with the displayed coefficient-class counterexample**
for (R15). The original pointwise target is **not addressed by a complete
proof**: its missing propagated-heat estimate is stated in section 5.
Review provenance is self-review; no independent audit is claimed in this
file. Mathematical proofreading covers only this new note, including
equation labels and the actual-IVP/coefficient-class distinction.

SHA-256 inputs; paths relative to `stable_stress_search/`:

| Input | SHA-256 |
| --- | --- |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/HANDOFF.md` | `c6a5817d38de46af82fdbfe8bbd58e7160cbded3d073788f9c743f0c84d5962d` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/pointwise_continuation.md` | `a2bc945dc7742faa803b0d7b858096a3424f5945ccef1dc02253c9a850701ea9` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/relative_entropy.md` | `92fb61a920ef28e4e08324dbbcf3495cbf708dcc5f750de866fb1b407a8f56b6` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/gradient_symmetrizer.md` | `1cd907f4d47552d794282cce7a42a3382fc81c73c9c6ff314cb962ffca39abb6` |
| `entropy_transport/floor_theorem/continuation_2026_11_01/effective_flux.md` | `ba03913a2d497fcefc346b8f04cc0da2d128a3f7dee34ee535c36155459f3ba3` |
