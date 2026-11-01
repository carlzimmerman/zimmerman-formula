# Independent audit of the global prefix continuation

Base checkpoint: **X48-DEN-2026-11-01-A**. Review scope is the new global
conditional theorem and scoped energy obstructions in `prefix_route.md`.
Only this audit file is written by the reviewer; the author owns its note.
The raw model was reconstructed before comparing the proposed proof.
This is a fresh-agent audit, rather than the author's self-review; agreement
between agents is not a substitute for the derivations recorded below.

**Primary verdict: proved as written.** This verdict applies to the
conditional global estimate (P5)--(P6) and the explicitly scoped norm and
instantaneous-energy obstructions. It does **not** apply to the original
common compression interval. No part of the reviewed argument propagates
its global upper-compression hypothesis. The original pointwise estimate,
the prefix coverage step, and (UC) remain open.

## 1. Claim card and exact quantifiers

For each `N>=32`, let the actual unchanged finite-mesh IVP have ordered
positive radii and `K>=0` on `[0,T]`. Fix `U>C_a`,
`UT<=log 2`, and `T<=10^-3`. Assume the **global**, history-dependent
one-sided bound

\[
 x_i(s)\le U\qquad(1\le i\le N,\ 0\le s\le T).          \tag{A1}
\]

No lower bound on x, pointwise K bound, lower density bound, or upper
radius bound is asserted. The comparison dust begins at the common
activation datum and has `r_d=lambda r(0)`, `H=-lambda'/lambda`,
`B=3H`, with `H'=H^2+(4*pi/3)*rho_d`. Define

\[
 d_i=r_i-r_{d,i},\quad w_i=u_i+Hr_i,\quad
 I=\sum_i dm K_iW_i,\quad
 E=\tfrac12\sum_i\mu_i(w_i^2+d_i^2)+I.                  \tag{A2}
\]

The exact audited conclusion is

\[
 E'\le32E+A_Us^2,\quad
 A_U=96MU^2\{(U-2)_++U\},\quad
 E(s)\le\tfrac{A_U}{3}e^{32T}s^3,
 \quad\sum_i\mu_i d_i^2\le C_Us^5.                    \tag{A3}
\]

The constants depend on U and the fixed physical parameters, never on N.
The theorem is a valid implication from (A1), not a construction of a
common T on which (A1) holds. Fixed-N continuity does not supply that
missing quantifier exchange.

## 2. Reconstructed raw identities and physical boundary

The normalization is `rho_q=G=P0=Kstar=1`, `tau=1/2`, with the
pinned damping strength one and memory activation `.01`. From
`material.py` and `transport.py`, on every signed-compression branch,

\[
 S=P+\kappa(x-2)_++\kappa gx,\quad
 P=K\rho^2h,\quad\kappa=\tfrac12\rho Wh,\quad
 g=K/(K+.01),\quad W_\rho=h.                            \tag{A4}
\]

In particular negative x does not permit replacing the signed memory
stress by its positive part. With the two unchanged heaters,

\[
 K_t=Q_o+Q_m+H_K,\quad
 Q_o=\tfrac12h x(x-2)_+,\quad Q_m=\tfrac12h g x^2,
 \quad dm W_i(H_K)_i=L_{i-1}-L_i.                       \tag{A5}
\]

The expression for `Q_o` is zero for `x<=2`, including all expansion.
The original `C=max(x,0)` source gives precisely this piecewise formula.
The outer and inner luminosities are both zero. Therefore

\[
 \begin{split}
 I'&=\sum_i dm\{W_i(Q_o+Q_m+H_K)_i
                                  +K_i\rho_i h_i x_i\}\\
   &=\sum_i V_iS_ix_i.                                  \tag{A6}
 \end{split}
\]

This identity is valid during expansion; its pressure term may be
negative. It does not require a positive thermal flux or a positive
lower gate bound.

From `collapse.py`, with `A_i=4*pi*r_i^2`, the actual momentum equation is

\[
 \mu_i u_i'=A_i(S_i-S_{i+1})-\mu_i m_i/r_i^2,
 \qquad S_{N+1}=0,\quad\mu_N=dm/2.                      \tag{A7}
\]

The exact discrete product telescoping is

\[
 \begin{split}
 \sum_{i=1}^N A_iw_i(S_i-S_{i+1})
 &=\sum_{i=1}^N S_i(A_iw_i-A_{i-1}w_{i-1})\\
 &=\sum_{i=1}^N V_iS_i(B-x_i).                          \tag{A8}
 \end{split}
\]

Here `A_0w_0=0` and `A_i r_i-A_(i-1)r_(i-1)=3V_i`. The exterior
term is exactly zero because its stress is the physical vacuum value.
The half nodal mass cancels against its own occurrence in (A7) before
the summation; it must still be retained in the kinetic norm.

Adding the entire internal energy (A6) to (A8) leaves `B*sum V*S`.
There is no missing homogeneous-reference pressure work in this proof.
If one instead split the mechanical work into `S-S_d`, it would introduce
an explicit term `S_d*A_N*w_N`; that is not the split used here. The dust
is a comparison profile and does not replace the heated actual state.

## 3. Constants, geometry, and the global theorem

The initial activation bound `C_a<6` and the scalar reference equations
give `B<=8` on `[0,10^-3]`. One direct bootstrap check is
`B'=B^2/3+4*pi*rho_d<47` while `B<=8` and
`rho_d<=exp(.008)<2`, so `B<6+.047<8` closes the reference bound.
This is a scalar prescribed-reference calculation, independent of N.

Under (A1), `rho_i<=exp(Us)<=2`. Summing volumes gives

\[
 r_i^3\ge\tfrac12r_i(0)^3,\qquad
 m_i/r_i(0)^3=4\pi/3.                                  \tag{A9}
\]

For `r` between `r_i` and `r_(d,i)` the derivative of
`(4*pi/3)*rho_d*r-m_i/r^2` is bounded by
`8*pi/3+16*pi/3=8*pi`. It vanishes at `r_(d,i)`, so the gravity
error is bounded by `8*pi*|d_i|`, without an upper radius bound.

Direct differentiation of (A2), using (A6)--(A8), consequently gives

\[
 E'=H\sum_i\mu_iw_i^2+\sum_i\mu_iw_i\mathfrak g_i
      +\sum_i\mu_id_i(w_i-Hd_i)+B\sum_iV_iS_i.           \tag{A10}
\]

The first three terms are at most
`(16/3+8*pi+1)*(E-I)<32*(E-I)` by `2|wd|<=w^2+d^2`.
No sign of x is used at this stage.

For all `0<rho<=2`, the exact ramp gives `3/2<=W<=2` and
`0<=h<=1`. Thus

\[
 \sum_iV_iP_i\le\tfrac43I.                              \tag{A11}
\]

The bound `rho<=exp(Us)` also gives
`h<=3(rho-1)_+^2<=12U^2s^2`, whence

\[
 \sum_iV_i\kappa_i\le12MU^2s^2,\qquad
 S_i\le P_i+\kappa_i\{(U-2)_++U\}.                     \tag{A12}
\]

Arbitrarily negative memory stress only decreases this last upper bound.
Multiplication by `0<B<=8` yields (A3), since the internal-energy
coefficient `32/3` is below 32. `E(0)=0` is exact. Ordinary nonsingular
Gronwall proves the `s^3` bound. The identity
`d'=w-Hd`, with `H>=0`, then gives
`||d(s)||_(l2(mu))<=integral_0^s||w(v)||_(l2(mu))dv=O(s^(5/2))`.
All these steps have constants independent of the first radius and N.

## 4. Audit of the two failed propagation inferences

The single-node test in (P16) passes. At dust geometry, cell volumes are
equal. Taking `w_k=D*V_k/A_k` at one annular full-mass node and zero
elsewhere gives exactly

\[
 x_k-B=-D,\qquad x_{k+1}-B=D,\qquad
 \tfrac12\sum_i\mu_iw_i^2=O(D^2N^{-3}).                 \tag{A13}
\]

This is enough to disprove extraction of a pointwise divergence bound
from the nodal norm alone. It is not asserted to be a trajectory or an
energy-level state. The theorem never controls the needed spatial
derivative of nodal flux.

For `E_alpha` with internal-energy coefficient `alpha<1`, set
`eta=1-alpha>0`. The exact stress work is
`sum V*S*(B-eta*x)`. On expansion, writing `x=-q`, it is

\[
 (P-\kappa gq)(B+\eta q).
\]

Its maximum over nonnegative q and its value at `q=P/(2*kappa*g)`
are exactly (P19)--(P20). In particular

\[
 \frac{P^2}{\kappa g}=\frac{2K(K+.01)\rho^3h}{W}.         \tag{A14}
\]

The proposed instantaneous closure therefore requires a quadratic
thermal quantity not bounded by `sum dm K`.

The energy-level construction (P22)--(P25) also passes in its stated
scope. At its special annular cell, `K=tau/dm` and
`q=rho_*(K+.01)/W_*=P/(2*kappa*g)`. The compatible nodal flux
perturbation is bounded by `C*(tau+dm)` on an annulus, so kinetic energy
is uniformly bounded. The internal energy is `tau*W_*` exactly.

For energy matching, the raw geometry gives

\[
 G_N=\sum_i\mu_i m_i/r_i(0)=24\pi A_N,\qquad
 A_N=\tfrac1{18}\sum_i\mu_i r_i(0)^2.
\]

Here `A_N` has positive uniform lower and upper bounds, for example by
using the outer half of the nodes for the lower bound. Thus (P24) is
the exact homogeneous energy-matching equation; its positive root stays
below 7 for `rho_*<1.01`, `C_a<6`. The derivative of kinetic energy
with respect to the background compression is uniformly positive near
that root. The perturbation changes energy and this derivative by
`O(tau+dm)`, so sufficiently small fixed positive tau and all sufficiently
large N give an exact matching root `C_N<8`. This justifies the claimed
uniform choice without numerical root finding.

Including the bounded background `C_N` does not change the leading
thermal work. In fact, on that expanding cell the identity is exactly

\[
 S(B-\eta x)=\frac{\eta P^2}{4\kappa g}
          +\frac{BP}{2}+\kappa gC_N(B-\eta C_N).         \tag{A15}
\]

The coefficient of the diverging term is positive, and its weighted
value is exactly (P25), proportional to `tau^2/dm`. Other cell work and
the relative-kinetic reaction terms are uniformly bounded.

If this construction is used to test a fixed startup instant s with the
stronger instantaneous density bound, choose
`1<rho_*<min(1.01,exp(Us))`. To test the additional thermal input
`I<=C*s^3`, choose tau small enough compared with `s^3` as well. For
each fixed positive s these remain fixed positive choices independent
of N, so the quadratic thermal work still diverges. This is an
instantaneous obstruction; none of these choices asserts the required
cap or heater history before s.

The construction does not refute a differential inequality that uses
additional spatial dissipation, nonlinear thermal control, or actual
startup-history information. It only refutes bounding this stress work
by the listed instantaneous energy and amplitude data. This matches
the note's stated restriction.

## 5. Dependency and obligation matrix

The dependency graph is: exact material stress and heater identities plus
shared heat-flux conservation imply (A6); exact momentum and the physical
vacuum imply (A8); the assumed global cap implies the geometric lower
radius and ramp bounds; these feed (A10)--(A12), ordinary Gronwall, and
the displacement integral. The cap is an input leaf throughout. It is
not produced by any downstream estimate.

| Obligation | Audit result |
| --- | --- |
| Signed stress and both heater branches | Passed from raw source |
| Global heat cancellation with original gates | Passed; no gate derivative used |
| Vacuum boundary and half outer nodal mass | Passed in (A7)--(A8) |
| Only one-sided x bound used | Passed |
| Actual gravity estimate at origin and outer node | Passed |
| Constants 32 and A_U | Passed |
| Fixed-N launch versus common-time quantifiers | Correctly separated |
| Norm-to-compression inference | Refuted in the stated scope by (A13) |
| Fixed-fraction thermal work closure from physical energy alone | Refuted in the stated instantaneous scope by (A14)--(A15) |
| Propagation of global x<=U | Not addressed by a proved implication |
| Original all-origin pointwise estimate, prefix closure, and (UC) | Still open |

The strongest safe statement is precisely the global conditional theorem
(A3). The cheapest next discriminating check is an actual evolution
estimate at a first upper-compression exit that also handles (A14), or
a different functional whose work avoids that term. Reusing the nodal
norm as a compression maximum or assuming an `L^infinity` K bound would
add an unproved leaf.

## 6. Review provenance, source checks, and pinned revisions

The review used the raw functions `collapse.py:64,88,110`,
`material.py:70,84,98,126`, `transport.py:66--94`, and
`convective_transport.py:61--77`, plus the activation contract. No
trajectory, numerical grid, or external regularity theorem is a proof
leaf. The exact energy matching and coefficient estimates above are
analytic and cover every sufficiently large N claimed by the
obstruction; the theorem covers every N in its quantified range.

All recorded input hashes were recomputed from bytes. Focused
proofreading and delimiter/unique-tag/whitespace validation cover this
audit only. No earlier proof note or physical source was edited by the
reviewer. The author corrected the forced missing backslash before
`mathfrak` in (P10); the final hash below includes that typographical
correction and no mathematical revision.

Paths in the following table are relative to `stable_stress_search/`.
The audit is attached to this exact reviewed file revision, not a later
shared HEAD:

| Artifact | SHA-256 |
| --- | --- |
| `entropy_transport/floor_theorem/pointwise_bootstrap_2026_11_01/prefix_route.md` | `80c7df1ec0b7f8d38e732e005be4f7d809eb35a4c457de360b71760d2f6e8f3a` |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/HANDOFF.md` | `c6a5817d38de46af82fdbfe8bbd58e7160cbded3d073788f9c743f0c84d5962d` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/gradient_symmetrizer.md` | `1cd907f4d47552d794282cce7a42a3382fc81c73c9c6ff314cb962ffca39abb6` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/boundary_transfer.md` | `167d6c6fb6362e163c6473e99cbef986c948e124feac10c98ad7131036dfa6f3` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/STATUS.md` | `2f12c417a2a3251f9fa44ebf120d0ac8e3e3628288f66cc442dfe81f0304b3d8` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/bootstrap.md` | `0b201a5eb41353945a1e6a374a69a3e3c290a961d6651ef9d0ff83737d5e6107` |
