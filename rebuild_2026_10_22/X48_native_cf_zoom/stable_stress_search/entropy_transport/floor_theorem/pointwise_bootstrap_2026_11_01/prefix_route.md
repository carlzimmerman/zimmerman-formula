# Global startup work and the first missing compression estimate

Base checkpoint: **X48-DEN-2026-11-01-A**. Observed shared HEAD:
`8a293ba8b8411e84c9e37bb9770d1a6f993f606e`. The hashes in Section 6 pin
the inputs independently of concurrent changes. Write scope: this file only.
The virgin sphere, material law, both heaters, gated outward heat flux,
physical vacuum boundary, nodal masses, and numerical records are unchanged.

**The common compression interval remains open.** There is a new global
actual-solution estimate under a *global one-sided* compression cap. It
retains all exterior cells and needs neither bounded expansion nor a
pointwise thermal bound. Relative nodal kinetic energy and total internal
energy are `O(s^3)`; the squared radial displacement from dust is `O(s^5)`.
The physical boundary contributes no uncontrolled work to this estimate.

This result does not propagate its one-sided cap. The attempted dissipative
extension meets a specific additional thermal term, derived below. An
energy-level state construction tests that term and shows why conserved
physical energy cannot bound it. This construction is not a solution from
the virgin initial data and is not a counterexample to the requested IVP.

## 1. Target and first-exit contract

The original conclusion is unchanged:

\[
 \exists T>0\ \forall N\ge32\ \forall s\in[0,T],\qquad
 x_i(t_a+s)\ge4\quad(1\le i\le\lceil N/4\rceil).
 \tag{P1}
\]

Here `x=-V_t/V`, `M=pi/3`, `dm=M/N`, `mu_i=dm` except
`mu_N=dm/2`, and activation is `s=0`. The actual data are
`rho_i(0)=1`, `K_i(0)=0`, `r_i(0)=a(i/N)^(1/3)`,
`u_i(0)=-C_a r_i(0)/3`, where `a=4^(-1/3)` and
`21/4<C_a<6`. The conditional energy at the base checkpoint assumes
`|x-x_d|<=1/32` through `ceil(N/2)` and its cutoff halos. Its inner
improvement does not control the last cell of that assumed prefix.

A possible coverage strategy is to establish a coarser bound on the entire
actual solution, use it to control exterior forcing, and then improve the
interior by the localized estimates. The first coarse bound tested here is

\[
 x_i(s)\le U\quad(1\le i\le N,\ 0\le s\le T),
 \qquad U>C_a,\quad UT\le\log2,\quad T\le10^{-3}.
 \tag{P2}
\]

This is a new **conditional hypothesis**, not a consequence of the prefix
bootstrap. Each fixed finite mesh has an initial interval satisfying (P2),
but a common such interval is not supplied by continuity. No lower bound
on signed compression is imposed in (P2).

## 2. A global actual relative-energy theorem under (P2)

Let `r_d= lambda(s) r(0)` be homogeneous dust continued from activation,
with `rho_d=lambda^(-3)`, `B=x_d`, and `H=B/3=-lambda'/lambda`.
Thus

\[
 H'=H^2+\frac{4\pi}{3}\rho_d,\qquad 0<H\le8/3,
 \qquad \rho_d\le e^{8s}<2.
 \tag{P3}
\]

This reference is used only for radius and velocity. Its thermal coordinate
is zero; it is not asserted to satisfy the actual heated equations. Set

\[
 d_i=r_i-r_{d,i},\qquad w_i=u_i+Hr_i,\qquad
 I=\sum_i dm\,K_iW_i,
 \qquad
 E=\frac12\sum_i\mu_i(w_i^2+d_i^2)+I.
 \tag{P4}
\]

**Global conditional theorem.** For every actual finite-mesh solution
satisfying (P2), valid ordered geometry and `K>=0`,

\[
 E'\le32E+A_U s^2,\qquad
 A_U=96MU^2\{(U-2)_++U\}.
 \tag{P5}
\]

Consequently, with constants independent of N,

\[
 E(s)\le \frac{A_U}{3}e^{32T}s^3,
 \qquad
 \sum_i\mu_i(r_i-r_{d,i})^2\le C_U s^5.
 \tag{P6}
\]

In particular `sum dm K <= (2/3)E=O(s^3)` and
`sum mu (u-u_d)^2=O(s^3)`. There is no lower density bound or bound on
individual `K`, `x_-`, or exterior radius in this theorem.

### Proof, including the physical boundary

The exact constitutive stress on every branch is

\[
 S=P+\kappa(x-2)_++\kappa gx,\quad
 P=K\rho^2h,\quad \kappa=\tfrac12\rho Wh,
 \quad g=K/(K+.01).
 \tag{P7}
\]

The exact global energy-exchange identity, with the shared heat luminosities
telescoped and the two mechanical heaters retained, is

\[
 I'=\sum_iV_iS_ix_i.
 \tag{P8}
\]

It holds during expansion: pressure work need not have a positive sign,
while the old and memory heating powers are nonnegative. The momentum
equation is

\[
 u_i'=\frac{4\pi r_i^2}{\mu_i}(S_i-S_{i+1})
          -\frac{m_i}{r_i^2},\qquad S_{N+1}=0.
\]

Using `r_0=u_0=0` gives the exact summation by parts

\[
 \sum_i4\pi r_i^2w_i(S_i-S_{i+1})
       =\sum_iV_iS_i(B-x_i).
 \tag{P9}
\]

There is no artificial exterior stress or discarded boundary term. In
particular the last nodal mass is the actual half mass, because it cancels
against the same mass in the momentum equation before summation.

The reference equations give

\[
 d_i'=w_i-Hd_i,\qquad
 w_i'=\frac{4\pi r_i^2}{\mu_i}(S_i-S_{i+1})+Hw_i+\mathfrak g_i,
 \quad
 \mathfrak g_i=\frac{4\pi}{3}\rho_dr_i-\frac{m_i}{r_i^2}.
 \tag{P10}
\]

The function defining `mathfrak g_i` vanishes at `r_{d,i}`. By (P2),
`rho_i<=exp(Us)<=2`; summing cell volumes therefore yields
`r_i>=2^(-1/3)r_i(0)`. The same bound holds for `r_d`. On the segment
joining these two radii,

\[
 \left|\partial_r\left(\frac{4\pi}{3}\rho_dr
                         -\frac{m_i}{r^2}\right)\right|
 \le\frac{8\pi}{3}+2\frac{2m_i}{r_i(0)^3}=8\pi.
 \tag{P11}
\]

Here `m_i/r_i(0)^3=4pi/3` exactly, including the last node. Thus
`|mathfrak g_i|<=8pi|d_i|`. No upper radius estimate is required.

Combine (P8)--(P10):

\[
 E'=H\sum_i\mu_iw_i^2+\sum_i\mu_iw_i\mathfrak g_i
       +\sum_i\mu_id_i(w_i-Hd_i)+B\sum_iV_iS_i.
 \tag{P12}
\]

The first three terms are at most
`(16/3+8pi+1)*(E-I)<32*(E-I)`.
Since `x<=U`, `P>=0` and `0<=g<=1`, the pointwise **upper** stress bound is

\[
 S\le P+\kappa\{(U-2)_++U\}.
 \tag{P13}
\]

Arbitrarily negative memory stress causes no loss in this upper estimate.
The exact material bounds `3/2<=W<=2`, `h<=1`, `rho<=2` give

\[
 \sum_iV_iP_i=\sum_i dm\,K_i\rho_ih_i\le\frac43I.
 \tag{P14}
\]

Moreover `h<=3(rho-1)_+^2<=12U^2s^2`, so

\[
 \sum_iV_i\kappa_i=\frac12\sum_i dm\,W_ih_i
                         \le12MU^2s^2.
 \tag{P15}
\]

Equations (P12)--(P15), `B<=8`, and `32>32/3` prove (P5).
The initial relative energy is exactly zero. Ordinary nonsingular Gronwall
gives the first part of (P6). Finally the integral solution of
`d'=w-Hd`, with `H>=0`, yields

\[
 \|d(s)\|_{\ell^2(\mu)}
 \le\int_0^s\|w(v)\|_{\ell^2(\mu)}dv\le C_Us^{5/2},
\]

which proves the stronger displacement estimate. This completes the proof.

## 3. Why this global energy does not propagate the cap

The theorem controls nodal velocity error, not its volume divergence.
At an annular index `k` with `k/N` bounded away from zero and one, keep
the dust geometry, perturb only node `k` by
`w_k=D V_k/(4pi r_k^2)`, and set other `w_i=0`. Then

\[
 x_k-B=-D,\qquad x_{k+1}-B=D\,V_k/V_{k+1}=D,
 \qquad \frac12\sum_i\mu_iw_i^2=O(D^2N^{-3}).
 \tag{P16}
\]

Changing the sign reverses the defect. Thus even the successful `O(s^3)`
global nodal estimate does not exclude an order-one compression spike.
This is a test of the implication from the norm, not a proposed trajectory.
The density-gradient/stress evolution must still exclude these states.

The direct attempt to add global mechanical dissipation is to replace `I`
in (P4) by `alpha I`, with `0<alpha<1`. Put `eta=1-alpha`. Instead of
`B sum V S`, its exact stress contribution is

\[
 \mathcal W_\eta=\sum_iV_iS_i(B-\eta x_i).
 \tag{P17}
\]

On a compressing bounded cell this can provide useful negative quadratic
work. On an expanding cell write `x=-q`, `q>=0`. There the old stress is
zero and the exact local expression is

\[
 S(B-\eta x)=(P-\kappa gq)(B+\eta q).
 \tag{P18}
\]

For `kappa*g>0`, its maximum over `q>=0` is

\[
 BP+\frac{(\eta P-B\kappa g)_+^2}{4\eta\kappa g}.
 \tag{P19}
\]

In particular at `q=P/(2kappa*g)`,

\[
 S(B-\eta x)=\frac12BP+\frac{\eta P^2}{4\kappa g},
 \qquad
 \frac{P^2}{\kappa g}=\frac{2K(K+.01)\rho^3h}{W}.
 \tag{P20}
\]

The formula extends by zero when `K=0` or `h=0`. A corrected upper-work
estimate therefore contains a weighted quadratic thermal term of the form

\[
 \sum_i dm\,K_i(K_i+.01)\frac{\rho_i^2h_i}{W_i}.
 \tag{P21}
\]

The successful theorem bounds `sum dm K` only. Even its startup order
`O(s^3)` does not bound (P21) independently of N. Multiplying a fixed
positive `eta` by a time power leaves this obstruction at every fixed
positive time. Taking `eta=0` recovers (P5), at the cost of the proposed
quadratic dissipation.

## 4. Energy-level test of the expansion term

This section tests an intermediate energy inequality only. The states are
not claimed to be reached from the cold datum or to obey either heater
equation over a time interval.

Fix `1<rho_*<1.01`, `tau>0` small, and an annular cell
`k=floor(N/2)`. Take homogeneous density `rho_*`, set
`K_k=tau/dm`, `K_i=0` otherwise, and put

\[
 r_i=(4\rho_*)^{-1/3}(i/N)^{1/3},\qquad
 q_k=\frac{\rho_*(K_k+.01)}{W_*},\qquad
 x_i=C_N\ (i\ne k),\quad x_k=C_N-q_k.
 \tag{P22}
\]

Choose the compatible velocities from the exact volume-divergence identity

\[
 4\pi r_i^2u_i=-\sum_{j\le i}V_jx_j.
 \tag{P23}
\]

The flux perturbation for every node `i>=k` is
`q_k dm/rho_*=(tau+.01dm)/W_*`. It is bounded independently of N, while
the disturbed nodes stay in an annulus. Hence kinetic energy is uniformly
bounded; the internal energy is exactly `tau W_*`; geometry is ordered;
and, for sufficiently large N, all compression satisfies `x_i<=8` whenever
`C_N<8`. There is no lower compression cap.

These states may also be placed on the exact conserved energy level of the
virgin sphere. To see this without assuming a numerical root, write

\[
 A_N=\frac1{18}\sum_i\mu_i r_i(0)^2,\qquad
 G_N=\sum_i\frac{\mu_im_i}{r_i(0)}=24\pi A_N.
\]

At `tau=0`, apart from an `O(dm)` velocity perturbation, energy matching
is achieved by the homogeneous compression `C_0` defined by

\[
 C_0^2=\rho_*^{2/3}\{C_a^2+24\pi(\rho_*^{1/3}-1)\}.
 \tag{P24}
\]

For `1<rho_*<1.01`, the activation bounds give `0<C_0<7` uniformly in N.
Energy is a quadratic polynomial in `C_N`; its derivative near `C_0` is
uniformly positive. Since the flux perturbation and internal-energy change
are `O(tau+dm)`, a small fixed `tau` and all sufficiently large N admit a
root `C_N=C_0+O(tau+dm)<8` matching the exact energy. The reference
activation energy is `A_N C_a^2-G_N`, by the unchanged dust evolution.
The half outer mass is included in all sums.

At cell k, `kappa*g*q_k=P_k/2`. Since `x_k=C_N-q_k`,
the leading positive part of (P18) is still
`eta P_k^2/(4kappa*g)`, up to terms only linear in `P_k` and bounded
background terms. More explicitly,

\[
 V_k\frac{\eta P_k^2}{4\kappa_kg_k}
 =\frac{\eta\rho_*^2h_*}{2W_*}
       \left(\frac{\tau^2}{dm}+.01\tau\right)
 \longrightarrow+\infty.
 \tag{P25}
\]

Every other cell has bounded compression, zero K, and bounded total work.
The remaining relative-kinetic reaction terms are bounded by the uniform
kinetic energy and geometry. Thus a global differential inequality for
the `alpha I` energy that tries to bound (P17) using only physical energy,
the density cap and the one-sided compression cap has no N-independent
constant. Exact energy equality does not repair that inference.

This does not refute a coupled estimate using gated-heat dissipation, a
nonlinear thermal functional, or the actual startup history. In particular
the large K cell would have a nontrivial outgoing heat flux; no heater or
heat-history claim has been imposed on (P22). It refutes only the stated
instantaneous closure of the globally linear internal-energy functional.

## 5. Route outcome and continuation

Executed routes:

1. The full-boundary relative kinetic plus physical internal energy closes
   globally under (P2), giving (P5)--(P6). Closed heat gates and arbitrary
   expansion cause no loss in this estimate.
2. Recovery of a compression maximum from that norm fails as an inference,
   by the exact divergence calculation (P16).
3. The fixed-fraction internal-energy construction that would add mechanical
   dissipation requires (P21). The energy-level expansion test (P22)--(P25)
   shows why the available physical energy cannot bound this term.

The first unresolved propagation implication is therefore more specific
than an unspecified exterior constant: construct an evolution estimate
that controls the divergence/stress at a first upper-compression exit while
allowing the expansion/thermal interaction in (P18). An actual coupled heat
estimate could absorb (P21), or a different global functional could avoid it.
The equality of heat boundary fluxes in the successful linear-energy
identity does not provide such absorption by itself.

Even if the global cap is obtained, the inner pointwise estimate and its
coverage must still be linked. Conversely, the prefix energy theorem alone
does not imply the new global hypothesis (P2). No chain from the proved
conditional statements to (P1) is asserted. The exterior/global route
remains open; the tests exclude the specified closures, not every global
weighted envelope.

## 6. Verification and provenance

All displayed evolution identities were reconstructed from the four exact
law sources. The proof uses no external theorem beyond finite-dimensional
summation by parts, the mean-value theorem and ordinary Gronwall. The
normalizations, signs, quiet branch, activation datum, origin, vacuum stress,
and exterior half mass were self-audited. The energy-level test includes
compatible nodal velocities and the exact energy level, but is explicitly
not an IVP counterexample. No new trajectory or numerical grid was run.

Self-proofreading covered the entire new file; no earlier file was edited.
Independent audit is a coordinator obligation and is not claimed here.

SHA-256 paths are relative to `stable_stress_search/`:

| Input | SHA-256 |
| --- | --- |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/HANDOFF.md` | `c6a5817d38de46af82fdbfe8bbd58e7160cbded3d073788f9c743f0c84d5962d` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/gradient_symmetrizer.md` | `1cd907f4d47552d794282cce7a42a3382fc81c73c9c6ff314cb962ffca39abb6` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/boundary_transfer.md` | `167d6c6fb6362e163c6473e99cbef986c948e124feac10c98ad7131036dfa6f3` |
| `entropy_transport/floor_theorem/density_closure_2026_11_01/STATUS.md` | `2f12c417a2a3251f9fa44ebf120d0ac8e3e3628288f66cc442dfe81f0304b3d8` |
| `entropy_transport/floor_theorem/nonlinear_closure_2026_11_01/bootstrap.md` | `0b201a5eb41353945a1e6a374a69a3e3c290a961d6651ef9d0ff83737d5e6107` |
