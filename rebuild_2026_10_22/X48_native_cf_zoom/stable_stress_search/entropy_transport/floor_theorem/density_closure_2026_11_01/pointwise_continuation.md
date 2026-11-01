# Bounded actual pointwise continuation after the first-energy estimate

Base: **X48-NLC-2026-11-01-B**. Only this note is written. No law, datum,
material parameter, reviewed energy note, or grid is changed. This is one
bounded analytic continuation, not a completed pointwise theorem.

**Verdict.** The new conditional first-energy estimate does not by itself
close the amplitude bootstrap. Actual constitutive inversion reduces the
remaining pointwise problem to a local bound for `(S-S_d)/s^2`. An exact
all-`p` stress identity is derived below. Its heat cross term and coefficient
remainder are retained; no mesh-uniform Moser estimate for them is proved.
This is the first unclosed implication in this continuation.

## 1. Exact equations and what the energy supplies

Use `z=log rho`, `x=-theta`, `psi=K W^(3/2)`, and

\[
 \begin{gathered}
 \kappa=\tfrac12\rho Wh,\quad g=K/(K+1/100),\quad
 \nu=\kappa(1+g),\quad P=K\rho^2h,\quad
 S=\nu x-2\kappa+P,\\
 x_t=L_rS+R,\quad z_t=x,\quad K_t=Q+H,\qquad
 H_i=(L_{i-1}-L_i)/(dm W_i).
 \end{gathered}                                             \tag{1}
\]

The actual active-prefix hypotheses are `2<x<=8`, `2s<=z<=8s`,
`0<=K<=1600s^3`, with the tighter provisional bound `|x-x_d|<=δ` on a
larger prefix and all cutoffs' collars. Let

\[
 v=x-x_d,\quad\zeta=z-z_d,\quad k=K-K_d,\quad
 f=S-S_d,\quad q=\psi-\psi_d.
\]

The conditional inner first-energy estimate of the new notes gives

\[
 \sum_iV_i\phi_i v_i^2\le Cs^6,\quad
 \sum_iV_i\phi_i\zeta_i^2\le Cs^8,\quad
 D_\eta(z)\le Cs^5,\quad
 \sum_i dm W_i\phi_i k_i^2\le Cs^{11}.             \tag{2}
\]

It also gives weighted time integrals of `s*D_η(v)` and
`s^-6*sum η L*(K_l-K_r)`. Bounds (2) are uniform in `N`, conditional on
the actual prefix envelope and on the independently reviewed first-energy
inputs. They contain no pointwise estimate at the origin.

The elementary constitutive state bounds yield

\[
 |f|\le Cs^2|v|+Cs|\zeta|+Cs^2|k|,
 \qquad \|f/s^2\|_{L^2(V\phi)}\le Cs^3.            \tag{3}
\]

The expected scalar radial parabolic smoothing loss on a time window
`[s/2,s]` is `s^-9/4`, because the mechanical diffusion clock is `s^3`
and the origin has radial dimension three. Applied in a setting where it
were proved, (3) would leave the favorable power `s^(3/4)`. This is a
scale calculation, not an application of the leading-model semigroup to
the actual nonlinear system.

## 2. An exact energy-to-pointwise nonimplication

At a fixed positive `s`, take homogeneous geometry and density `rho_d`,
`K=K_d`, and set `x=x_d` except `x_1=x_d+epsilon`, with a fixed small
`epsilon>0` fitting the strict provisional envelope. Then every density
and relative-entropy term in the new energy is zero, including the
midpoint density-gradient energy and the one-sided memory-gradient energy.
The velocity part is exactly

\[
 E_v=\frac{dm}{2\rho_d s}\epsilon^2
     =\frac{M\epsilon^2}{2\rho_d Ns}.
                                                               \tag{4}
\]

For sufficiently large `N`, this is at most `C*s^5`, while
`||v||_infinity=epsilon`. This state has valid ordered geometry and a
compatible radial velocity reconstructed from its cell compressions.
It is an instantaneous admissible state, not a solution launched from the
specified common data. It refutes only a static inference from the new
energy bound to the pointwise bootstrap; it does not refute the IVP or a
genuine dynamic smoothing estimate.

## 3. Constitutive inversion makes the precise remaining target sufficient

At fixed `x_d`, split the exact constitutive difference along state paths:

\[
 f_i=\nu_i v_i+A_i\zeta_i+B_i k_i,\qquad
 A_i>0,\quad a_*/s\le A_i/\nu_i\le a^*/s,\quad
 1/\nu_i\le1/(8s^2),\quad |B_i/\nu_i|\le C.        \tag{5}
\]

Here `A_i` is the density divided difference at fixed `K_i,x_d`, and
`B_i` is the memory divided difference at density `z_d,x_d`. The active
law has `S_z|_(x_d,K)>0` and `S_K>0`; `κ_z>=c*s` and `x_d-2>=c>0`
on a sufficiently short reference interval prove the uniform positive
constant `a_*`. Every path stays in the startup state box. Thus

\[
 \zeta_i'+(A_i/\nu_i)\zeta_i=f_i/\nu_i-(B_i/\nu_i)k_i.
                                                               \tag{6}
\]

Because both memories are `O(s^3)`, (6) implies the following exact
conditional reduction: if, on a fixed inner prefix and all preceding times,

\[
 \|f(s)/s^2\|_\infty\le Cs^\theta,\qquad\theta>0,
                                                               \tag{7}
\]

then integrating the scalar damped equation from the zero density error
gives `||ζ/s||_infinity<=C(s^theta+s^3)`. Substitution in (5) gives
`||v||_infinity<=C(s^theta+s^3)`. All constants are independent of `N`.
No spatial regularity assertion is needed for this last implication.
Accordingly (7), with enough prefix/collar coverage, is a sufficient actual
pointwise target. Its proof is the remaining issue.

For comparison, the outward heat law also gives an actual relative-memory
maximum principle. At a maximum of `K-K_d`, incoming heat is zero and
outgoing heat is nonnegative, so `H<=0`; at its minimum `H>=0`.
On a prefix this argument applies to the upper maximum, while the lower
minimum needs the exterior collar included or its incoming value controlled.
Where both extrema are covered,

\[
 D^+\|k\|_\infty\le Cs^2\|v\|_\infty
                      +Cs\|\zeta\|_\infty+Cs^2\|k\|_\infty.
                                                               \tag{8}
\]

This useful scalar comparison does not control the heat divergence at a
stress extremum.

## 4. The exact actual stress equation and all-p heat defect

The actual differentiated stress and temperature equations are

\[
 f_t=\nu L_rf+S_KH+\mathcal F,\qquad
 \mathcal F=\nu R+S_zx+S_KQ-S_d',
                                                               \tag{9}
\]
\[
 q_t=W^{3/2}H+\mathcal G,\qquad
 \mathcal G=W^{3/2}Q+\tfrac32K W^{1/2}\rho h x-\psi_d'.
                                                               \tag{10}
\]

These retain the full heater and both heat gates. In particular `S_K=O(s^2)`
and the heat conductance/mechanical conductance ratio is `O(s^4)`, but
those upper bounds alone do not bound `H` pointwise.

For `p>=2` and a fixed material cutoff define

\[
 E_p=\frac1p\sum_i\frac{V_i\phi_i}{\nu_i}|f_i|^p,\quad
 J_p(f)=|f|^{p-2}f,\quad
 \alpha=\frac{S_K}{\rho\nu W},\quad
 \beta=\frac{\nu_K}{\rho\nu^2W},\quad
 M_p=\alpha J_p(f)-\frac\beta p|f|^p.
                                                               \tag{11}
\]

Direct differentiation, including the heat part of the state-dependent
weight, gives the complete identity

\[
 \begin{split}
 E_p'={}&-\sum_ea_e\Delta(\phi J_p(f))\Delta f
             +\sum_eL_e\Delta(\phi M_p)\\
 &+\sum_i\frac{V_i\phi_i}{\nu_i}J_p(f_i)\mathcal F_i\\
 &-\frac1p\sum_i\frac{V_i\phi_i}{\nu_i}|f_i|^p
 \left[x_i+\frac{\nu_{z,i}}{\nu_i}x_i
                         +\frac{\nu_{K,i}}{\nu_i}Q_i\right].
 \end{split}                                                    \tag{12}
\]

The last line is nonpositive on the actual branch. The heat term is
`-sum ell*Δpsi*Δ(φ M_p)`, with `ell>=0`, and has no standalone sign.
At `p=2`, this is the full heat-weight flux already treated in
`heat_absorption.md`. At general `p` its interior coefficient remainder is
exactly

\[
 \Delta M_p=\bar\alpha\Delta J_p(f)
       -\frac{\bar\beta}p\Delta|f|^p+\mathcal C_p,
 \qquad
 \mathcal C_p=\overline{J_p(f)}\Delta\alpha
                   -\frac{\overline{|f|^p}}p\Delta\beta.
                                                               \tag{13}
\]

No derivative of the gate was discarded. A separate `p`-energy in `q`
has favorable heat term `sum L*ΔJ_p(q)`, but it does not automatically
control (13): its power weight is on `q`, whereas the mixed heat flux in
(12) is weighted by `f`. The density-dependent parts of `Δalpha,Δbeta`
also leave powers of `f` multiplying density differences. The first-energy
bound controls the unweighted `D(z)`, not these level-dependent terms.

Thus a mesh-uniform level-set or all-`p` estimate for (12)--(13), coupled
to (10) and the damped density equation, is the first unproved step in this
specific pointwise attempt. Merely invoking scalar Moser theory for (9)
would omit precisely its heat cross flux and heat-dependent weight term.
Replacing the actual operator by its homogeneous leading graph would also
remove these terms and is not a continuation proof.

## 5. Scope of the remaining obligation

A successful continuation must prove an estimate implying (7) uniformly at
the first cell as well as the other central-quarter cells. Its spatial
cutoffs must leave a controlled actual collar, and the covered prefix must
contain every `i<=ceil(N/4)`. Constants may depend on fixed cutoffs and the
chosen provisional amplitude margin, but not on `N`, the first radius, or
which heat faces are open. A time-window argument must use only earlier
actual compatible states and then close the assumed amplitude margin.

The new energy estimate supplies the favorable `L^2` powers (2)--(3), and
(5)--(7) supply the exact final constitutive conversion. The missing link
is the actual coupled smoothing/iteration estimate handling (12)--(13).
No failure or existence theorem for such an estimate is inferred. The
all-origin pointwise bootstrap and (UC) remain unproved by this bounded
continuation.

## Provenance and verification

Verification consists of exact constitutive divided differences, actual
shared-flux summation, and differentiation of the displayed weights.
No external regularity theorem or numerical trajectory is load-bearing.
This note is self-reviewed and mathematically proofread; no independent
proof audit is claimed at this stage. The reviewed first-energy files
remain unchanged.

Pinned SHA-256 inputs, paths relative to `stable_stress_search/`:

| Input | SHA-256 |
| --- | --- |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/heat_absorption.md` | `b98843cec40271ef4a16bdb6c15baf50a43c203d6367fbf3ae72a4d299b74379` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/flux_potential.md` | `858dae640349b4efdf88cf4d9d98e524115fe9ed5505e56b88cf5961db559e78` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/relative_entropy.md` | `92fb61a920ef28e4e08324dbbcf3495cbf708dcc5f750de866fb1b407a8f56b6` |
