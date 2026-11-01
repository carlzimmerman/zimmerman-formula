# A higher-order conditional interior energy from the actual heat collar

Base checkpoint: **X48-DEN-2026-11-01-A**. Coordinator route, unchanged
equations and data. Observed starting shared HEAD:
`8a293ba8b8411e84c9e37bb9770d1a6f993f606e`. This file does not assert the
actual pointwise bound, a common tight-prefix interval, or (UC).

The new step is to retain the outer relative-memory energy in the heat
collar estimate instead of bounding it immediately by the coarse memory
amplitude. A different physical drop threshold and four nested energy
estimates then improve the conditional inner energy from O(s^5) to O(s^9).
The argument is analytic; no mesh experiment is a proof leaf.

## 1. Exact inherited setting

Use the unchanged normalized law and homogeneous heated reference in
`../density_closure_2026_11_01/gradient_symmetrizer.md`. Write
`v=x-x_d`, `z=log rho`, `e=z-z_d`, `k=K-K_d`, and let

\[
 |v_i(u)|\le1/32\quad
 (i\le\lceil N/2\rceil,\ 0<u\le s\le10^{-3}) .       \tag{T1}
\]

This is a provisional hypothesis on the actual trajectory, including all
cutoff endpoint halos. In particular `2<x<=8`, `2s<=z<=8s`, and
`0<=K,K_d<=1600s^3`. All finite-edge constitutive and geometric estimates
used below are those proved in the pinned gradient and relative-entropy
notes. No exterior active branch is assumed.

For a cell cutoff `phi=chi^2` and face weight `eta=bar phi`, denote the
mechanical/density energy of that note by `T=E_v+G_mid+N_lambda`, where
`lambda=1/16`. In particular

\[
 E_v={1\over2s}\sum V\phi v^2,\quad
 G_{\rm mid}\ge{221\over8}D_\eta(z),\quad
 N_\lambda={1\over32s^3}\sum V\phi e^2 .             \tag{T2}
\]

Let `E_K=(1/2)sum dm W phi k^2`,
`F_0=(1/2)sum a eta ((K_l-K_r)^-)^2`, and
`D_H=sum eta L (K_l-K_r)>=0`. Throughout this note `a_e=A_e^2/dm`
denotes a graph conductance, while the scalar exponent below is denoted b.

## 2. Heat collar without an independent O(s^4) forcing

The exact relative-entropy identity is equation (7) of the pinned entropy
note, before its weight is specialized. Its heat collar is
`B_K=sum Delta phi L bar k`. Equations (11)--(13) there give

\[
 |B_K|\le\tfrac12D_H+{C_B\over8}s^{14}D_\eta(z)
       +C_\chi s^4\sum_iV_i\phi_{{\rm out},i} k_i^2 . \tag{T3}
\]

Indeed use `|Delta phi|<=2 sqrt(eta)|Delta chi|`,
`L^2/a<=16200s^4 LJ`, and
`LJ<=4Lq+C_Bs^14 a(Delta z)^2`, with `q=K_l-K_r` and
`C_B=2.4e16`. The actual cutoff geometry bounds
`sum a(Delta chi)^2 bar(k^2)` by the outer volume norm in (T3).
Since `rho W>=3/2`, that last norm is at most `4E_(K,out)/3`.
This estimate has not used the coarse bound `|k|<=1600s^3`.

Fix any `3<b<4` and put

\[
 G_b=s^{-(3+b)}E_K .                                  \tag{T4}
\]

The full derivative, including `W_t`, weight, reference and collar, gives

\[
 \begin{split}
 G_b'+{3+b\over s}G_b+\tfrac12s^{-(3+b)}D_H
 \le{}&C_b(s^{1-b/2}+s^2)(G_b+E_v+N_\lambda)\\
 &+C s^{11-b}D_\eta(z)+C_\chi s^4G_{b,\rm out}.
 \end{split}                                         \tag{T5}
\]

For clarity the mixed local power is exact: the source bounds
`|Q-Q_d|<=3000s^2|v|+2800s|e|+6.4e5s^2|k|` imply
`s^(-(3+b))*s^2*k*v` and `s^(-(3+b))*s*k*e` have coefficient
`s^(1-b/2)` when measured in the three energies in (T5). This coefficient
is integrable at zero precisely in the range used here. The K-linear and
W-weight work is O(s^2)G_b. The last term of (T5) follows from (T3)
with exactly the same time weight on the outer relative energy.

## 3. A different physical drop threshold

Use the physical threshold `q/d=s^b` in the exact three-class split of
`flux_potential.md` (22). The gate on its high-drop class is at least
`beta_b*s^b`, with the fixed positive number

\[
 \beta_b={\ell_g\over c_g+1600T_0^3+\ell_g T_0^b},
 \qquad T_0=10^{-3} .                                  \tag{T6}
\]

The resulting finite-edge inequality is

\[
 sD_\eta(K)\le2sF_0+{10\over27\beta_b}s^{-(3+b)}D_H
              +16Ms^{1+2b}+4.5\,10^{11}s^{11}D_\eta(z).
                                                               \tag{T7}
\]

Negative K drops give the first term. Small physical positive gradients
give `sum a d^2<=16M` times `s^(1+2b)`. Temperature-closed positive drops
are in the density-controlled class, exactly as in the pinned proof.
This is an instantaneous algebraic split; differentiating the threshold
is unnecessary. In particular no heat ellipticity on closed faces is used.

The exact negative-gradient heat sign and full source estimate (17) in the
relative-entropy note remain unchanged by this threshold choice.

## 4. Combined inequality and activation launch

Combine (T5), (T7), that negative-gradient estimate, and the complete
mechanical inequality (G22) of the midpoint note. A fixed sufficiently
large multiplier A_b for (T5) absorbs the memory cost in (G22), leaving
positive heat dissipation. The small velocity-gradient share in F_0' is
absorbed by its mechanical dissipation. Therefore, for
`Y_b=T+A_b G_b+F_0`, constants independent of N give

\[
 \begin{split}
 Y_b'+c_1sD_\eta(v)+c_2s^{-(3+b)}D_H
 \le{}&\left\{{1\over16s}+C_b(s^{1-b/2}+1)\right\}Y_b\\
 &+C_\chi s^2E_{v,\rm out}+C_\chi s^4G_{b,\rm out}
       +C_bs^{1+2b}.
 \end{split}                                         \tag{T8}
\]

The density remainders in (T5) and (T7) are regular multiples of
G_mid. The exponent `1/16` has not increased: all new positive coefficients
are integrable. Constants can be large but are finite and independent of N.

For each fixed N the conservative activation argument of the pinned entropy
note gives `v=O_N(s)`, `e=O_N(s^2)`, `k=O_N(s^4)`. Consequently

\[
 G_b=O_N(s^{5-b}),\qquad Y_b=O_N(s),\qquad
 s^{-1/16}Y_b\longrightarrow0 .                       \tag{T9}
\]

Here `5-b>1`. This launches (T8) separately on every fixed mesh with zero
integrating-factor trace and no N-dependent initial constant. Under (T1)
the coarse outer bounds are

\[
 E_{v,\rm out}\le C/s,\qquad G_{b,\rm out}\le Cs^{3-b}.
                                                               \tag{T10}
\]

Successive nested energies therefore have powers

\[
 Y_1\le Cs^2,\quad Y_2\le Cs^5,\quad Y_3\le Cs^8,
 \quad Y_4\le C s^{\min(11,\,2+2b)} .                \tag{T11}
\]

Each step uses (T8) with the preceding cutoff as its outer cutoff. For
example, the coarse heat collar is O(s^(7-b)), higher order than O(s);
subsequent heat collars gain five powers of s after integration. Velocity
collars gain three. The scalar integrating factor is valid because the
source exponent plus one always exceeds `1/16`.

In particular, choosing `b=7/2` gives

\[
 Y_{\rm inner}\le Cs^9,\qquad
 \sum_iV_i\phi_{{\rm inner},i}v_i^2\le Cs^{10},\qquad
 \| (S-S_d)/s^2\|_{L^2(V\phi_{\rm inner})}\le Cs^5 . \tag{T12}
\]

The last assertion follows from the exact bound
`|S-S_d|<=C(s^2|v|+s|e|+s^2|k|)` and the three zeroth-order
terms of Y_b. It is still an L2 conclusion, not a maximum bound.

## 5. Origin, endpoint halos, and the finite set of small meshes

For N>=64 use `theta_i=(i-1/2)/N`. Let chi_j, j=0,...,4, equal one
through `(17+2j)/64`, decrease linearly to zero at `(18+2j)/64`, and
remain zero farther out. They have Lipschitz constant 64. Each endpoint of
an edge with `Delta chi_j!=0` lies where chi_(j+1)=1, since
`1/N<=1/64`. All active-edge halos lie strictly inside `ceil(N/2)`.
The innermost cutoff is one at every i<=ceil(N/4), including i=1.
Use the coarse amplitude only on chi_4, then apply (T8) on chi_3, chi_2,
chi_1 and chi_0. This proves (T12) for every N>=64 under (T1).

The finite set 32<=N<64 can be included in an existential common short
time without a numerical computation. Here is the fixed-N local argument
needed for that statement. The exact initial homogeneous state has zero
relative error. At fixed N, the physical outer stress mismatch is O_N(s^2),
the locally Lipschitz reference-subtracted reaction has no forcing, and
the graph coefficients stay bounded. Thus on the full fixed grid
`v=O_N(s^3)`, `e=O_N(s^4)`, `k=O_N(s^6)`.

For a prefix ending at j<N, all mechanical rows annihilate the constant
reference stress. Its only exterior error is the j+1 neighbor. If the
errors there have orders `v=O_N(s^p)`, `e=O_N(s^(p+1))`,
`k=O_N(s^(p+3))`, then the mechanical exterior forcing is O_N(s^(p+2)):
S_x=O(s^2), S_z=O(s), and S_K=O(s^2). Prefix shear and gravity depend
only on that prefix and have locally Lipschitz relative reaction. The
source equation has Q_x=O(s^2), Q_z=O(s), Q_K=O(s^2); its heat term has
the fixed-N bound
`|H_i|<=C_N[s^4 max_neighbor|k|+s^9 max_neighbor|e|]`.
This follows directly from `b_gate<=1`, `h_l h_r=O(s^4)` and
`Delta psi=Wbar^(3/2) Delta k+O(s^5)Delta e`.
Integral Gronwall therefore raises the prefix orders to
`v=O_N(s^(p+3))`, `e=O_N(s^(p+4))`, `k=O_N(s^(p+6))`.

Two inward repetitions give `v=O_N(s^9)`, `e=O_N(s^10)`,
`k=O_N(s^12)` on i<=N-2. Every cell and face in the innermost cutoff
above lies there for 32<=N<64. In particular its Y_(7/2) is O_N(s^17),
which implies (T12) on a positive fixed-N interval. Take the minimum of
these finitely many interval lengths and the maximum of the corresponding
finite constants. This supplies constants and a positive T_* independent
of N for the finite set, to be combined with the conditional N>=64 result.
No minimum over infinitely many mesh-continuity times has been taken.

Thus (T12) is a conditional all-N>=32 estimate on a sufficiently short
common parameter interval, whenever the required actual prefix envelope
holds. The finite-mesh argument does not propagate that envelope for
arbitrarily large N.

## 6. Exact remaining scope

This route improves the available interior powers and keeps the origin in
the sums. It still permits arbitrarily narrow instantaneous velocity spikes;
an energy alone cannot exclude them. A dynamic pointwise estimate and
propagation of (T1), including its outer prefix edge, remain necessary.
The conditional time parameter T_* is not an established actual-solution
common bootstrap interval. Neither (UC) nor the unconditional entropy-floor
theorem follows from (T12).

Input SHA-256 hashes, relative to stable_stress_search:

| Input | SHA-256 |
| --- | --- |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/gradient_symmetrizer.md` | `1cd907f4d47552d794282cce7a42a3382fc81c73c9c6ff314cb962ffca39abb6` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/relative_entropy.md` | `92fb61a920ef28e4e08324dbbcf3495cbf708dcc5f750de866fb1b407a8f56b6` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/flux_potential.md` | `858dae640349b4efdf88cf4d9d98e524115fe9ed5505e56b88cf5961db559e78` |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |

This is an author derivation pending independent review. Exact algebra and
time powers were self-reviewed; no external theorem or trajectory estimate
is used. Mathematical proofreading is separate from proof correctness.
