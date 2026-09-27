# Response/inertia construction routes D1 and D3 — 2026-09-26

**The full recipe remains open.** This work derives three concrete construction
results from common actions: an auxiliary-weight compatibility identity, an
integrated exact-exponential action with a healthy causal low-acceleration
principal sector, and a degenerate kinetic extension that keeps a healthy wave
at high acceleration but fails a conserved-source instantaneous-response test.
Generalizing the latter to arbitrary rank-one mixing does not remove that
conflict on its regular high-acceleration branch.

These are scoped results for the displayed action families. They do not exclude
all relativistic MOND actions, certify physical degrees of freedom, or satisfy
the full recipe. No earlier report, recipe, specification or other agent's files
were changed.

## Contract and provenance

Base requested by the coordinator was
`03524d209b7ca0c3900f47ccf5dfe42f9187d7c3`, with the prior closure-resume artifacts
present. Concurrent external work advanced HEAD to
`f3b848273e635b81bc328882db0ffb4206d86e45`; the new runs pin that observed revision
and unchanged source hashes. Sources are the C-H `ACTION.md` scalar action and
L340's scalar equations, plus the previous
`closure_resume_2026_09_26/recipe_construction_followup.md`.

Use `c=1`, real frozen coefficients, Fourier `k>0`, and independently varied
lapse `phi`, spatial potential `psi`, shift `beta` and scalar `U`. Source coupling
is `−R phi + Rdot beta −t_s psi`, with `R` carrying the original gravitational
normalization. The static Newtonian reference is `psi_N=−R/(4k²)`.
Exceptional zero denominators, `k=0`, zero gradient, actual curved background
solutions and the full nonlinear Hamiltonian require separate analysis.

The first route preserves the Einstein scalar metric structure and changes its
auxiliary/clock terms. The second uses a **direct nonlinear AQUAL primitive**;
it does not infer general-source AQUAL from a spherical QUMOND inverse law.

## D1: independent auxiliary weights do not free the static and dynamical signs

Consider the same-action scalar Lagrangian

\[
\begin{aligned}
L={}&-6\dot\psi^2+4k^2\beta\dot\psi+2k^2\psi^2-4k^2\phi\psi\\
&+2Pk^2(U-\phi)^2+2Qk^2U^2+Ak^2\phi^2
-B(3\dot\psi-k^2\beta)^2.
\end{aligned}
\]

On a regular branch define

\[
E=A+\frac{2PQ}{P+Q},\qquad \kappa=\frac{2(2+3B)}B.
\]

Independent static variations give

\[
\psi=\phi,\qquad \frac{\phi}{\psi_N}=\frac2{2-E}.
\]

Independently eliminating all three auxiliaries in the real-time action gives

\[
L_{\rm red}=\kappa\dot\psi^2-2k^2\frac{2-E}{E}\psi^2,
\qquad c_s^2=\frac{2(2-E)}{\kappa E}.
\]

Thus a positive time kinetic coefficient and `0<E<2` are compatible. But exact
matching to a static inverse-response eigenvalue `1/mu_i` fixes

\[
E_i=2(1-\mu_i).
\]

For exponential AQUAL at `x=|grad Phi|/a0>0`,

\[
\mu_T=1-e^{-x},\quad \mu_L=1+(x-1)e^{-x},\qquad
E_T=2e^{-x},\quad E_L=2(1-x)e^{-x}.
\]

The longitudinal `E_L` is negative for `x>1`. At that exact static response,
the displayed regular scalar has negative `omega²` whenever `kappa>0`.
Independent `P,Q,A` cannot cure this while keeping the same source/metric
structure and exact static response. The previous large-`alpha_c` healthy
example escaped by changing the static response; it remains a useful bounded
example but does not solve this matching problem.

This is not a failure of static AQUAL ellipticity: both `mu_T,mu_L` are positive
at `x>0`. It is a conflict specific to the additional dynamical scalar mechanism.
In the deep limit `E_i→2` from below, this branch's restoring coefficient tends
to zero. A uniform positive lower sound-speed bound or controlled zero-field
limit does not follow from pointwise health.

## D3a: time-derivative terms with a positive-definite kinetic matrix

Add terms that vanish on static fields,

\[
J\dot U^2+H\dot\psi\dot U+4Zk^2\beta\dot U.
\]

After independently eliminating lapse and shift, write
`L=dot q^T K dot q−k² q^T V q`, `q=(psi,U)`. The matrices are

\[
K=\begin{pmatrix}
\kappa&H/2+2Z(2+3B)/B\\
H/2+2Z(2+3B)/B&J+4Z^2/B
\end{pmatrix},
\]
\[
V=\begin{pmatrix}
-2(A+2P-2)/(A+2P)&4P/(A+2P)\\
4P/(A+2P)&-2(AP+AQ+2PQ)/(A+2P)
\end{pmatrix}.
\]

The potential is unchanged by these time-derivative additions. Its stationary
`U` direction `q=(1,−V12/V22)` has exactly

\[
q^T Vq=\frac{2(2-E)}E.
\]

For `E<0`, that direction has negative potential energy. If `K` is positive
definite, the Rayleigh quotient of `K^(-1/2) V K^(-1/2)` therefore has a negative
direction and at least one negative squared frequency. This argument applies to
the entire displayed regular kinetic family, not a sampled parameter grid.
It does not apply to a degenerate kinetic matrix; that door is tested below.

## An integrated constructive low-acceleration action

Define a nonlinear static correction on a fixed flat leaf,

\[
\mathcal F(a)=4a_0^2[1-(1+x)e^{-x}],\qquad x=|a|/a_0,
\qquad \mathcal L_{\rm corr}=\mathcal F(\nabla\Phi)
-\zeta|\nabla(U+\Phi)|^2.
\]

Take constant nonzero `zeta`. The `U` equation is
`Delta(U+Phi)=0`. With `U+Phi=0` on the boundary of a bounded domain, or with the
corresponding constant/harmonic freedom fixed on a closed leaf, it gives
`U=−Phi` up to an irrelevant fixed constant. A compact static leaf requires the
usual compatible mean-source prescription; an isolated positive mass is not
silently placed on a flat torus.

The independently varied spatial potential equals the lapse potential at this
weak-field static order. After these eliminations, the **general-source**
nonrelativistic density, including the original Einstein piece and matter, is

\[
\mathcal L_{\rm NR}=-\frac{a_0^2}{8\pi G}
G\!\left(\frac{|\nabla\Phi|}{a_0}\right)-\rho_b\Phi,
\quad G(x)=x^2+2(1+x)e^{-x}-2.
\]

This follows from the exact identity `−2a0²x²+F=−2a0²G`. Its fixed-boundary
variation gives `div[(1−exp(−|grad Phi|/a0)) grad Phi]=4πG rho_b`, including
nonspherical sources. This identifies the nonlinear static law, not just one
tangent or a spherical fit. The spatial variational calculus itself is explained
here; the symbolic file checks the primitive and its derivatives.

The complete radial Hessian gives

\[
E_T=\frac{\mathcal F'(x)}{2a_0^2x}=2e^{-x},\qquad
E_L=\frac{\mathcal F''(x)}{2a_0^2}=2(1-x)e^{-x}
=E_T+xE_T'.
\]

The derivative term in `E_L` is essential. It would be lost by simply inserting
the field-dependent transverse coefficient into a quadratic action. Here the
primitive is varied first, so both jets and their integrability are explicit.

Add `−B K²+J(n·partial U)²` as the trial clock terms. On the same frozen
static-background principal calculation, use `B=2/5`, `J=16`, `zeta=1/4`.
The scalar matrices after lapse/shift elimination are

\[
K=16I,\qquad
V(E)=\begin{pmatrix}
4/(E-\zeta)-2&2\zeta/(E-\zeta)\\
2\zeta/(E-\zeta)&\zeta E/(E-\zeta)
\end{pmatrix}.
\]

For `0<x<=1/2`, both exact Hessian eigenvalues have `1/2<E<2`.
Indeed `E_L>=exp(−1/2)>1/2`, while `E_T<2`; intermediate directions lie between
them. The elementary exponential bound follows, for example, from
`exp(t)<1/(1−t)` at `0<t<1`, applied at `t=1/2`.

The leading minors establish both positive gradient energy and metric-cone
subluminality:

\[
V_{11}>0,\quad \det V=\frac{2(2-E)}{4E-1}>0,
\]
\[
16-V_{11}>0,\quad
\det(16I-V)=\frac{54(21E-10)}{4E-1}>0.
\]

Thus both principal squared speeds are strictly between zero and one on that
branch. The exact static primitive holds beyond this branch, but its health
does not: the longitudinal unit-speed boundary is
`x=1−W(5e/21)≈0.5763163395`; the lapse Schur denominator vanishes at
`x=1−W(e/8)≈0.7384213325`. Here `W` is the real principal Lambert function.

This construction has **two** scalar modes in the displayed nondegenerate
block. It does not certify the recipe's field count, acceptable PPN, nonlinear
health or zero-gradient limit. Its value is that exact nonlinear static
integrability and a bounded healthy causal principal sector coexist in one
specified local construction. Neither the kinetic coefficients nor a dark
matter particle abundance are hidden in that statement.

## D3b: degenerate kinetic extension and the sourced response

A genuine next possibility is to remove a negative-potential direction by a
constraint rather than make every scalar kinetic direction positive. Let
`V_U=n·partial U` and add

\[
-B K^2+t K V_U+J V_U^2,\qquad
t=-2r(2+3B),\quad J=-3r^2(2+3B).
\]

This has an exact ADM kinetic factorization, before any scalar Fourier
specialization:

\[
K_{ij}K^{ij}-(1+B)K^2+tKV_U+JV_U^2
=K_{ij}^{\rm TF}K_{\rm TF}^{ij}
-(B+2/3)(K+3rV_U)^2.
\]

For constant coefficients the trace/`U` Hessian is structurally degenerate.
That identity is not a Dirac constraint count or a proof of causal propagation.
The frozen scalar kinetic matrix is
`K=kappa [[1,r],[r,r²]]`, with physical time-derivative combination
`v=psi+rU` and `kappa=2(2+3B)/B`.

Define

\[
D_r=E(\zeta-2r^2)+2r^2\zeta+4r^2-4r\zeta.
\]

Joint elimination of the remaining auxiliary variables gives

\[
\boxed{L_v=\kappa\dot v^2-
\frac{2\zeta(2-E)}{D_r}k^2v^2},\qquad
c_s^2=\frac{2\zeta(2-E)}{\kappa D_r}.
\]

In particular, `r=1` gives `D_r=(2−zeta)(2−E)`, so the wave speed is independent
of the exact exponential tangent. At `B=2/5`, `zeta=1/4`, it is `c_s²=1/56`,
including negative longitudinal `E` at `x>1`. This is a real healthy-wave
construction, not merely an attempted one.

It is insufficient: the static solution has `psi=Phi,U=−Phi`, so for `r=1`
the scalar `v` vanishes and does not carry the static MOND field. The full
conserved-source response exposes the missing channel. With
`j=Rdot`, `t_s=(omega²/k²)R`, comparison to `E=0` gives

\[
\Delta\phi=\Delta\psi=
\frac{E(k^2+\omega^2)R}{4k^4(E-2)},\quad
\Delta\beta=0,\quad \Delta U=-\Delta\psi.
\]

The physical linear tidal component in the stated convention is
`R_0x0x=−k²(phi+betadot)−omega² psi`, hence

\[
\Delta R_{0x0x}=-\frac{E(k^2+\omega^2)^2R}{4k^4(E-2)}.
\]

This difference has no temporal wave pole and contains inverse spatial powers.
A healthy independent wave therefore does not establish causal MOND response.

## General rank-one mixing: contact cancellation versus health

The `r=1` decoupling might have been special, so the full sourced response was
also solved at arbitrary real `r`. Set `q=omega²/k²`, `T=2+3B`, and define

\[
\begin{aligned}
n_3&=Tr^2(E-\zeta),\\
n_2&=3Tr^2(E-\zeta)-2Tr^2+2Tr\zeta-(2B+1)E\zeta,\\
n_1&=2Tr(r-\zeta)+\zeta(B+E),\qquad n_0=-B\zeta,\\
d_1&=2TD_r,\qquad d_0=2B\zeta(E-2).
\end{aligned}
\]

The exact scalar tidal transfer is

\[
\frac{R_{0x0x}}R=\frac{n_3q^3+n_2q^2+n_1q+n_0}{d_1q+d_0}.
\]

It separates into a contact polynomial `c2 q²+c1 q+c0` and one wave pole:

\[
c_2=\frac{n_3}{d_1}=\boxed{\frac{r^2(E-\zeta)}{2D_r}},\quad
c_1=\frac{n_2-d_0c_2}{d_1},\quad
c_0=\frac{n_1-d_0c_1}{d_1},
\]
\[
\frac{R_{0x0x}}R=c_2q^2+c_1q+c_0+
\frac{n_0-d_0c_0}{d_1(q-c_s^2)}.
\]

Choose an explicitly conserved scalar source generated by a smooth function
`F(t,x)` on a periodic slab, with its relevant zero mode fixed:
`T00=partial_x²F`, `T0x=−partial_t partial_xF`, `Txx=partial_t²F`.
All other components vanish. Both conservation equations hold identically.
Its Fourier density is `R=−k²F`, with the required `j` and `t_s` above.
It may be a signed perturbation around a background; no isolated positive-mass
creation is being assumed.

For this generator, the `q²` contact term is
`−c2 omega⁴ F/k²`: an instantaneous inverse spatial Laplacian. The `q` and
constant contacts instead become local differential terms in `F`. If the wave
pole has a stable speed at most one, its retarded Green function cannot cancel
this instantaneous nonlocal support. Thus **vanishing `c2` is necessary** for
causal response to this source class; it is not by itself sufficient for every
source or geometry.

On a regular branch, cancellation requires `r=0` or `E=zeta`. For exact
high-acceleration longitudinal response `E<0`, either option fails health:

- `r=0`: `V_eff=2(2−E)/E<0`.
- `E=zeta`: `D_r=(E−2r)²>0` on the regular branch and
  `V_eff=2E(2−E)/(E−2r)²<0`.

Consequently **no regular cell of this rank-one trace-mixing family combines
the exact high-acceleration tangent, positive scalar kinetic/gradient energy,
and cancellation of this instantaneous physical tidal term**. The argument
allows either nonzero sign of `zeta`; it does not merely eliminate the positive
sample used above. It holds pointwise if `r` or `zeta` is chosen as a function
of the frozen background. Such functional choices still require a nonlinear
completion and its new jets on changing backgrounds.

`D_r=0`, zero kinetic coefficient, `zeta=0`, new constraint content, different
source/metric structure and other derivative operators are separate branches;
they were not divided through and declared excluded. This is a scoped mechanism
obstruction, not a universal theorem about modified gravity.

## Verification, failures retained and next step

- `run_001`: 24 exact symbolic residuals plus the `x=2` high-response negative
  control; common static/dynamical action, integrated primitive jets and the
  bounded positive/causal minors. Completed in 1.43 s.
- `run_degenerate_001`: failed a manually entered Hessian determinant prefactor
  (expected 16 instead of actual 8). The failed source is preserved at
  `archive/check_degenerate_run001.py`, matching its original input hash.
  No physics conclusion was taken from that failed run.
- `run_degenerate_002`: corrected prefactor, full joint reduction, independent
  sourced matrix inversion and tidal identity all pass. Completed in 1.34 s.
- `run_rankone_001`: arbitrary-`r` reduction, exact source transfer, full
  polynomial/pole division, dangerous-contact coefficient and both cancellation
  branches pass. Completed in 12.22 s.
- `DoorsResponse20260926.lean`: eleven checked real-algebra declarations cover
  static matching, negative speed, potential minors, causal-complement minors
  and the general rank-one cancellation-implies-instability implication.
  Their allowed axioms are only `propext`, `Classical.choice`, `Quot.sound`.
  They do not formalize action variation, retarded-support analysis or the
  physical applicability of the frozen source. The separate formal run is
  recorded under `run_lean_002`; the preceding `run_lean_001` hit its wrapper's
  100-second timeout without a mathematical failure report. Its original wrapper
  is retained at `archive/verify_lean_run001.py`. The retry uses an explicit
  single Lean worker and a larger bounded wall/CPU allowance.

Contracts, exact commands, pinned source hashes, software versions, result
hashes, exit status and enforced limits are in the run manifests. Runs are
small symbolic calculations, with no random search, observational fit or broad
simulation. The theorem domains and analytic sign/interval arguments above are
essential; a successful executable alone does not establish them.

Accepted manifests are `run_001/manifest.json`,
`run_degenerate_002/manifest.json`, `run_rankone_001/manifest.json`, and
`run_lean_002/manifest.json`; each passed the computation-audit validator with
`--root`, including current input and output hash checks. The final Lean source
SHA-256 is
`e52114ec7cbd7ccfadb1b5cde67758ae647048e947f32d917cbe93e55370d603`.
`run_lean_002/stdout.txt` contains all eleven printed axiom lists, and
`run_lean_002/results.json` records their acceptance. There are no custom physics
axioms or `sorryAx` dependencies. Mathematical self-review covered all new
displays, denominator restrictions, source conventions and scope statements;
the only prose correction was “casual” to “causal” in the run summary.

The direct integrated primitive and the explicit source-transfer formulas are
the reusable gains. A useful further route must change the dynamical constraint
or source structure responsible for the negative-potential/contact alternative,
then rederive the exact static law and physical tidal response together. Merely
retuning these auxiliary weights, making the same kinetic matrix positive, or
choosing another regular rank-one mixing repeats the resolved obstruction.
The broader construction remains open, including the coordinator's separate
weighted-filter auxiliary repair; that fixed-leaf result is not imported here
as a propagation certificate.
