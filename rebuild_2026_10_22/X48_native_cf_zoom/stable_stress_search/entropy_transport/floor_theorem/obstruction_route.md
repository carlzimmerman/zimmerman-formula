# Adversarial route: startup, the free surface, and the exact remaining gap

**Normalized target.** For the pinned virgin sphere and fixed physical parameters,
find a material mass fraction `f>0`, a time `t_seed`, and `epsilon>0`, independent
of the equal-mass shell count `N`, such that the exact semidiscrete solution has
`K_i(t)>=epsilon` for every cell intersecting `0<=m<=f M` and every
`t>=t_seed`. The geometry must remain ordered so that this statement is defined.
Energy conservation and exact constitutive inactivity at `rho<=rho_q` are
separate required identities. Inactivity is a conditional property of a dilute
cell, not a claim that the collapsing sphere stays dilute.

**Primary verdict: incomplete, with the smallest missing implication identified.**
The actual discretization admits a rigorous positive global floor and global
ordered evolution for **each fixed finite N**, with constants depending on N.
A common activation time does not by itself make these constants uniform.
No counterexample to the requested uniform central floor was found. A new
broader-prefix comparison argument, communicated by the parallel route and
checked below, removes the need for a separately assumed permanent warm guard.
The remaining load-bearing obligation is a mesh-uniform positive seed on a
fixed positive mass prefix at one common finite time.

This is an independent adversarial derivation from the source law. The
preservation lemma in section 4 was supplied later by the parallel route and
then checked independently; its provenance is not independent discovery.
No numerical trajectory, production run, or source-code change is used here.

## 1. Exact object and checkpoint

Base checkpoint: **X48-TRANSPORT-2026-11-01-B**, as recorded in
`CHECKPOINT_2026_11_01.md`, descended from A at
`c4b97598e8b6b408dd75d724ea469a81a2bd4ea9`. The current shared checkout HEAD
when read was `0fe706856e8a897a9ab350be4931dbf36416ada4`; the audited experimental
files are untracked there. Therefore the content hashes below, rather than
HEAD alone, identify the actual mathematical operator reviewed.

The authoritative operator is `ConvectiveCollapse.fields`, inheriting mechanics
and the local source from `TransportCollapse`, `SphericalCollapse`, and
`material.py`. The driver `refinement.py` does not alter the exact ODE: its
cold phase integrates an invariant subspace and hands off at activation.
The present argument concerns that ODE in exact arithmetic, not the capped
floating-point Radau/BDF algorithms or their dense interpolants.

Use the normalized units of the runs:

\[
 G=\rho_q=K_*=P_0=1,\quad \tau=1/2,\quad M=\pi/3,\quad
 dm=M/N,\quad \mu_i=dm\ (i<N),\quad\mu_N=dm/2.
\]

The initial data are
`r_i=(i/N)^(1/3)`, `u_i=-r_i/4`, and `K_i=0`, with `N>=2`.
Let `V_i=4pi(r_i^3-r_(i-1)^3)/3`, `rho_i=dm/V_i`,
`theta_i=Vdot_i/V_i`, and `r_0=0`. The declared gravitational potential is

\[
 \Omega_N=-\sum_{i=1}^N G\mu_i m_i/r_i,\qquad m_i=i\,dm.
\]

The prefix convention includes every cell intersecting the requested fraction,
so the last included index is `ceil(f*N)` in one-based indexing. A first-cell
claim is not a fixed-positive-mass-fraction claim as `N` grows.

## 2. A rigorous fixed-N seed and global continuation

### The cold phase is exactly homologous on every mesh

Until simultaneous source activation, pressure, damping, and transport vanish.
Writing `r_i(t)=a(t)(i/N)^(1/3)` gives exactly

\[
 \ddot a=-GM/a^2,\qquad a(0)=1,\quad\dot a(0)=-1/4,
\]
\[
 \rho_i=1/(4a^3),\qquad C_i=-\theta_i=-3\dot a/a.
\]

The factor `mu_N=dm/2` affects pressure acceleration but not this gravitational
acceleration. The first integral is

\[
 \dot a^2=1/16+2GM(1/a-1).
\]

At `a_a=4^(-1/3)` all cells reach `rho=1` together. At that event

\[
 t_a=0.5907973398405011\ldots,\quad
 c=C_a=5.414584960442701\ldots,\quad
 b=\tau c-1=1.7072924802213505\ldots>0.
\]

The density threshold, rather than the compression threshold, is therefore
the last inactive condition. These scalar values were obtained from the
displayed first integral and one quadrature; the proof needs only `c>2`.

### Every finite mesh seeds all of its cells

Fix N. The ODE is locally Lipschitz on ordered positive geometry and
nonnegative K, using the documented locally Lipschitz stage extension if an
open domain is desired. The nonnegative orthant is invariant: at `K_i=0`,
outward loss is zero and incoming heat and local sources are nonnegative.
At the activation state the total material stress
vanishes. Hence the velocity and density derivatives there are still those
of the homologous dust motion. With `s=t-t_a` tending to zero from above,

\[
 \rho_i=1+c s+o_N(s),\qquad C_i=c+o_N(1),
\]
\[
 h_i=3c^2s^2+o_N(s^2),\qquad
 Q_{{\rm old},i}=3c^3 b\,s^2+o_N(s^2).
\]

Here and below a remainder with subscript N is not asserted uniform in N.
Because N is fixed and finite, these asymptotics hold simultaneously for all
its cells.

At any global material minimum of K, outward heat loss vanishes: the next
cell cannot have smaller K, so the adverse-entropy gate is zero. Incoming
heat and both local sources are nonnegative. Thus the global minimum is
nondecreasing and, during startup, its derivative is bounded below by the
minimum original heater. Integrating gives

\[
 \min_i K_i(t_a+s)\ge c^3b\,s^3+o_N(s^3)>0
\]

for sufficiently small positive s depending on N. The coefficient is
`c^3*b=271.02131326812406...`. One may obtain the matching leading term for
each K by the maximum principle and a local Gronwall estimate, but it is not
needed for positivity. In particular, there exist `s_N>0` and `k_N>0` such
that all cells have `K>=k_N` at `t_a+s_N` and retain it thereafter while
geometry is valid. No heat imported from outside is needed for this result.

### Energy then prevents any later finite-time loss of geometry at fixed N

The material weight satisfies `W(rho)>=rho` for every positive rho: it equals
rho above the gate ramp; on the ramp `W-rho` decreases to zero because
`W'-1=h-1<=0`; below the ramp `W=3/2>=rho`.

After the positive seed, the exact semidiscrete energy identity gives

\[
 E_N=T_N+U_N+\Omega_N,\quad
 U_N\ge k_N dm^2\sum_i1/V_i.
\]

Put `A_N=G sum_i mu_i m_i`. Ordered geometry implies

\[
 |\Omega_N|\le A_N/r_1,\qquad
 E_N\ge {3k_Ndm^2\over4\pi r_1^3}-{A_N\over r_1}.
\]

The right side tends to positive infinity as `r_1` tends to zero. Therefore
`r_1>=r_*(N)>0` for the entire subsequent valid trajectory. It follows that
`T_N+U_N<=E_N+A_N/r_*(N)=H_N<infinity`. Consequently

\[
 V_i\ge k_Ndm^2/H_N>0,\qquad
 |u_i|\le\sqrt{2H_N/\mu_i},\qquad
 K_i\le H_N/(dm\,\min W).
\]

Radii cannot diverge during a finite interval because the velocities are
bounded. The positive cell-volume bound and that finite upper radius bound
give a positive shell-gap bound on each finite interval. Centroid separations
therefore stay positive too. All ODE coordinates and denominators remain in
a compact subset of the valid finite-dimensional domain on every finite
interval. Ordinary ODE continuation then proves global ordered evolution
for this fixed N.

**Strongest unconditional conclusion obtained here:** for every finite
`N>=2`, the specified exact semidiscrete evolution exists for all nonnegative
time and has a strictly positive, N-dependent all-material floor after an
N-dependent startup time. The proof provides no uniform lower bound on
`k_N`, `s_N`, density, or normalized cell geometry as N tends to infinity.

## 3. Why common activation does not make this proof mesh-uniform

The homogeneous cold phase is exact. Continuing that homogeneous ansatz after
activation is not exact. For a spatially constant positive stress `S`, every
interior node has zero pressure force, but the free outer node has

\[
 \ddot r_N|_{\rm stress}=4\pi r_N^2 S/\mu_N
 ={8\pi N\over M}r_N^2 S.
\]

The difference is present before thermal pressure matters: the original
compression stress already satisfies

\[
 q_s=q_2s^2+o_N(s^2),\qquad q_2={9\over2}c^2b
 =225.24273210533264\ldots.
\]

The thermal pressure and memory damping are higher order at this onset.
Relative to the continued dust trajectory, integration of the outer force
therefore gives, for each fixed N,

\[
 \delta r_N={8\pi N a_a^2q_2\over12M}s^4+o_N(s^4),
\]
\[
 \delta\rho_N=-\beta N^2s^4+o_N(s^4),\qquad
 \delta\theta_N=4\beta N^2s^3+o_N(s^3),
\]
\[
 \beta={8\pi^2a_a^4q_2\over3M^2}
 =851.3641785460212\ldots.
\]

There are no lower-order bulk perturbations that cancel these coefficients:
the common original stress cancels at interior nodes. These derivatives
already show N-dependent surface response. The formal distinguished scale
`s~N^(-2/3)` makes the surface divergence correction order one and its density
correction comparable with the initial density excess `c s`. This scale is a
diagnostic of the nonuniform Taylor argument, **not** a proved asymptotic
boundary-layer solution: the displayed `o_N` remainders cannot themselves be
used at an N-dependent time without further estimates.

Accordingly:

- A local-existence or continuity interval at the common activation state may
  shrink with N. Finite-dimensional continuity alone cannot establish a common
  heating duration.
- A spatially uniform bulk source does not make the post-activation finite
  sphere an exactly homogeneous solution. The free-surface force is a real
  term of this discretization, not a solver artifact.
- This surface calculation does **not** refute a uniform seed on any fixed
  central fraction strictly inside the sphere. A spatially localized estimate
  controlling surface influence could still prove such a seed.
- It also does not prove that the all-material floor tends to zero. Surface
  material may later receive outward heat. No such limiting trajectory has
  been constructed here.

The source and viscosity have physical coefficients; their differentiated
spatial operator contains inverse cell spacings. Replacing a mesh-uniform
estimate by an unweighted ODE Lipschitz bound will generally expose those
spacings. A suitable argument has to respect physical distance or material
mass and control the coupled motion, not just count cells.

## 4. Broader-prefix entropy comparison removes a permanent-guard assumption

This lemma was proposed by the parallel route after the preceding startup
calculation. Its key implications were checked directly from the raw flux.

Assume that at one common time `t_s` the actual solution has
`K_i(t_s)>=kappa>0` for `i<=j_s`, where `j_s=ceil(g*N)` and `g>f>0` are fixed.
Freeze **only the choice of geometry history** to the actual evolving one,
and let k solve the source-free heat equation on that history:

\[
 \dot k_i={L_{i-1}(k)-L_i(k)\over dm W_i(t)},\qquad
 k_i(t_s)=\begin{cases}\kappa&i\le j_s,\\0&i>j_s.\end{cases}
\]

This auxiliary flow is a comparison device; it is not asserted to satisfy
the actual momentum equation.

1. At fixed geometry each L is nondecreasing in its supplying k and
   nonincreasing in its receiving k. For example, where `x>y>=0`,
   `(x-y)/(chi_g+(x+y)/2)` has positive x derivative and negative y derivative;
   the same signs hold for the positive temperature difference. Thus the heat
   vector field is cooperative. Since the actual local heaters are
   nonnegative and actual initial K dominates k, `K_i(t)>=k_i(t)`.
2. The cone `k_1>=...>=k_N>=0` is invariant. At an adjacent equality
   `k_i=k_(i+1)`, their shared flux L_i is exactly zero, irrespective of the
   unequal W values, and
   `d(k_i-k_(i+1))/dt=L_(i-1)/(dm W_i)+L_(i+1)/(dm W_(i+1))>=0`.
   The maximum principle also gives `max k_i<=kappa`.
3. `S_k=dm sum_i k_i^(1/3)` is nondecreasing. Its face contribution at positive
   temperatures is a positive constant times
   `L_i[1/(W_(i+1) k_(i+1)^(2/3))-1/(W_i k_i^(2/3))]>=0`.
   Zero coordinates do not invalidate this conclusion. One rigorous finite-N
   interpretation is to compose single-face heat flows with geometry held
   fixed on small time slices. Each pair flow has the entropy inequality,
   including a zero receiving coordinate by continuity. These compositions
   converge to the nonautonomous locally Lipschitz heat ODE on finite time
   intervals; continuity of S passes the inequality to its limit.

For `i<=j_s`, order and the maximum bound imply

\[
 j_s\kappa^{1/3}\le\sum_j k_j^{1/3}
 \le(i-1)\kappa^{1/3}+(N-i+1)k_i^{1/3},
\]

and hence

\[
 K_i(t)\ge k_i(t)\ge\kappa
 \left({j_s-i+1\over N-i+1}\right)^3,\qquad t\ge t_s.
\]

For every `i<=ceil(f*N)`, the ratio is at least `g-f`; a simple uniform
choice is therefore

\[
 \boxed{K_i(t)\ge\kappa(g-f)^3\quad
 (i\le\lceil fN\rceil,\ t\ge t_s).}
\]

This argument uses the outward entropy gate, hot-to-cold transfer, and total
material entropy. It needs neither a permanent outside guard nor density
upper bounds after the seed. The fixed-N global continuation result above
supplies valid actual geometry for all finite times. Uniform estimates on
that geometry would still be needed for a separate continuum convergence
theorem.

The README's guard requirement is correct for directly applying a constant
barrier to a bare prefix; it is not an impossibility theorem for other prefix
arguments. The auxiliary comparison is a stronger preservation mechanism.
It still needs the uniform seed as a hypothesis.

## 5. Tempting objections that do not refute the specified claim

| Proposed objection | Exact scope and verdict |
| --- | --- |
| A cold exterior makes the global minimum zero. | It invalidates a global-minimum proof for that state. It does not preclude a central fixed-mass floor; section 4 explicitly tolerates an initially cold exterior. |
| The surface cell starts heating on a shrinking time scale. | It identifies nonuniformity in the naive all-cell startup proof. It does not establish a central-floor counterexample or a limiting surface entropy. |
| The first-cell mass tends to zero. | It prevents promoting first-cell numerical evidence to a finite-mass core theorem. It does not invalidate an estimate covering all `ceil(f*N)` cells. |
| The law cannot heat a zero-K center from an outer heater. | Correct for such data because the flux is outward only. The specified data heat the center locally at the same cold activation event as the other cells. |
| Finite energy and entropy increase force a positive central floor. | False as an invariant-only argument. The dense central cusp has `rho~r^(-4/3)` and `K~r^2`, with finite central contributions to mass, internal and gravitational energies, and entropy, while its central infimum is zero. |
| The ordered stationary-cusp route refutes virgin-sphere evolution. | It does not. It concerns different initial data. A full stationary free-surface example also requires continuation through the gate; a bare dense truncation is insufficient. |
| Finite-N shell crossing might end the seeded argument. | For this exact initial-value problem the fixed-N seed and energy argument in section 2 exclude later finite-time geometry loss. Their constants are not mesh-uniform. |
| Four meshes through finite time establish all N and all later times. | They do not. Recorded positive samples remain numerical evidence; no intervening-time or continuum estimate is supplied by sampling. |

The cusp has `m~r^(5/3)`, so `K~m^(6/5)` near its center. An infimum of zero
persists on every positive central mass interval, while the contribution to
all the listed integrals remains finite. It can be patched to a regular
finite exterior as admissible state data without claiming the patch is
stationary. This exhibits noncoercivity of finite integral bounds. This
report neither constructs a full stationary free-surface continuation nor
matches a cusp trajectory to the specified virgin data or its exact energy.

## 6. Dependency and obligation audit

The implication graph for the semidiscrete target can now be written as

`raw law -> cold homology -> simultaneous activation -> fixed-N seeding ->
fixed-N minimum principle + energy coercivity -> fixed-N global solution`,

and, on a second branch,

`mesh-uniform broader-prefix seed -> cooperative auxiliary heat flow +
descending order + entropy increase -> uniform eternal smaller-prefix floor`.

The missing connection is from the specified cold initial data to the
mesh-uniform broader-prefix seed, not from a seed to infinite-time
preservation. A common cold activation time alone does not supply that
connection.

| Obligation | Audit result |
| --- | --- |
| Exact operator, initial data, cell convention, and physical parameters | Passed from the source definitions. |
| Semidiscrete energy identity | Passed: shared luminosities telescope; the same stress enters pressure work and heating; the declared node potential cancels gravitational work. |
| Exact dilute inactivity | Passed for arbitrary retained K when `rho_i<=rho_q`; both adjacent luminosities and all local material stresses/sources vanish. Shared node motion can still change future density. |
| Positive seed for every fixed finite N | Passed by the common positive startup heater and the global minimum principle. |
| Global ordered geometry for every fixed finite N | Passed by the seeded floor and the explicit energy coercivity estimate. |
| A seed `kappa>0` on `ceil(g*N)` cells at one common time, uniformly in N | Not proved. The simple local-continuity proof is not uniform. |
| Uniform eternal floor on a smaller prefix, conditional on that seed | Passed by the auxiliary comparison calculation in section 4. |
| Continuum solution, convergence, and continuum geometry | Not addressed; these require additional compactness/consistency and continuation estimates. |
| A counterexample from the stated virgin initial data | None established. |

The cheapest meaningful next theoretical check is a localized short-time
estimate after `t_a`: exhibit fixed `g>0`, `s_0>0`, and positive lower bounds
for density excess and compression on a central material region during a
fixed subinterval. A heat-equation subsolution or another source comparison
would then have to convert those bounds into `K>=kappa` on a broader prefix.
An equivalent direct uniform bound on K at one common time is sufficient.
The estimate must control the coupled free-surface influence rather than
postulate that the bulk stays exactly homogeneous.

Finite exceptional shell counts can be absorbed using the fixed-N theorem:
if a uniform seed/floor is proved for all sufficiently large N, reduce epsilon
and increase the common time over the finitely many remaining N. Thus proving
the asymptotic mesh statement suffices for an all-`N>=2` semidiscrete claim.

## 7. Source hashes and checks

SHA-256 values, relative to the entropy_transport directory:

| Source | SHA-256 |
| --- | --- |
| `CHECKPOINT_2026_11_01.md` | `8195cdb66a110578608a00c8e23f28b67646448b955a84fe02d447129026d3fc` |
| `README.md` | `8719a07f915902b829030d178636e27602f362c0f0b0e4e9e5d02039f575d2f6` |
| `DERIVATION.md` | `e08312d0dc3be7f3f2d225ca938a7872ceec6d4c2532db2102f54c7a984910da` |
| `NUMERICS.md` | `a603ebc876fec044518985174efe160cd4a8ae2618dcb8e13cd5803190dd27a3` |
| `convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `refinement.py` | `faa09a692bb072a3198b18e53a711aa49cb51aef88fbdf5a94909ec46d37c523` |
| `../collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `../material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |

Checks performed: read the current README, derivation, checkpoint, numerical
methods, raw source law/driver/material, and relevant constitutive tests;
reconstructed the exact cold motion and energy cancellation; evaluated only
the displayed scalar dust quadrature and onset coefficients with Python
`math`/SciPy `quad`; hashed the nine listed inputs. No collapse simulation,
production job, external theorem, or test result is used as a proof of the
uniform statement. The source tests were read, not rerun by this route.

Only this report is written by this route. The experimental source files,
status documents, and prior run outputs are unchanged.
