# Conserving entropy transport: a settled cold-collapse experiment

An outward heat flux gated by adverse entropy ordering, combined with bulk
damping that returns its mechanical work to heat, settles the specified cold
sphere into a finite radial core. The same physical coefficients work at
32, 64, 128 and 256 equal-mass shells. After warming, the central entropy
coefficient remains positive in the recorded samples and approaches an
independent mass-and-energy equilibrium prediction.
This is finite numerical evidence for this initial-value problem. A dynamical
floor theorem uniform in resolution and time, cosmological forest viability,
and three-dimensional halo stability remain open.

The [current analysis](analysis_v2/summary.json),
[manifest](analysis_v2/manifest.json), [numerical methods](NUMERICS.md), and
[conditional stationary prediction](ISENTROPIC_LIMIT.md) contain the evidence.
This experimental addition does not change frozen X48 dynamics or grades.

## Material energy and the stress scale

Let `rho` be the positive inertial density of the clustered component. Set

\[
 P_0=\frac{a_0^2}{8\pi G},\quad K_\star=\frac{P_0}{\rho_q^2},\quad
 \chi=K/K_\star,\quad d=\rho/\rho_q,
\]
\[
 h(d)=\begin{cases}0&d\le1,\\
 3(d-1)^2-2(d-1)^3&1<d<2,\\1&d\ge2.\end{cases}
 \qquad e=K W(\rho),\qquad P=K\rho^2h(d).
\]

Here `W'=h`, `W=3rho_q/2` below the gate, and `W=rho` above `2rho_q`;
[material.py](../material.py) supplies the joining polynomial. The dormant
internal energy must be retained when pressure turns off. The history variable
K is independent of density, so the stress is nonbarotropic. The acceleration
scale a0 normalizes stress; it supplies neither a fixed pressure ceiling nor
a core radius without the additional material scales.

With entropy coordinate `sigma=chi^(1/3)`, the first law gives

\[
 T=\partial_\sigma e=3K_\star\sigma^2W,\qquad
 w=W/\rho_q,\qquad \psi=\chi w^{3/2}.
\]

The dimensionless potential `psi` is a strictly increasing function of T.
Evolving K avoids division by zero when collapse first heats virgin material.

## Selected redistribution law

For adjacent radial cells i and j=i+1, with center separation `Delta r` and
face area A, define `[x]_+=max(x,0)` and

\[
 z_{ij}=\frac{\ell_g[(\chi_i-\chi_j)/\Delta r]_+}
 {\chi_g+(\chi_i+\chi_j)/2},\qquad a_{ij}=\frac{z_{ij}}{1+z_{ij}},
\]
\[
 \boxed{L_{ij}=P_0D\frac{A}{\Delta r}\,
 h_i h_j\,a_{ij}[\psi_i-\psi_j]_+.}
\]

Positive L is outward. Transfer requires both adverse entropy ordering and
an outward temperature drop. Stable entropy ordering or an inactive neighbor
sets the face flux exactly to zero. The fixed length `ell_g` multiplies a
physical gradient; it is not a resolution-dependent mixing length. D has
dimensions length squared per time. This is a phenomenological heat closure,
not resolved material convection. Its finite-volume implementation is
[convective_transport.py](convective_transport.py); its pre-run declaration
is [CONVECTIVE_ROUTE.md](CONVECTIVE_ROUTE.md).

Retain collapse heating, and add memory-activated signed bulk stress:

\[
 \theta=\nabla\cdot v,\quad C=(-\theta)_+,\quad
 q_s=P_0 d w h(\tau C-1)_+,
\]
\[
 \zeta=\alpha_v\tau P_0 d w h\frac{\chi}{\chi+\chi_d},
 \qquad q_d=-\zeta\theta.
\]

Use `P+q_s+q_d` in momentum and, for each cell of fixed mass dm,

\[
 \boxed{\dot K_i=h_iK_\star C_i(\tau C_i-1)_+
 +\frac{\zeta_i\theta_i^2}{\rho_iW_i}
 +\frac{L_{i-1,i}-L_{i,i+1}}{dm_iW_i}.}
\]

The same bulk stress does the mechanical work that supplies its heat.
Luminosities are shared with opposite signs; closed boundary luminosities
are zero. Consequently internal, kinetic and self-gravitational energies
cancel exactly at the semidiscrete level. The time integrator has measured
finite errors. For positive temperatures the entropy equation is

\[
 \rho D_t\sigma+\nabla\cdot(F/T)
 =\frac{q_sC+\zeta\theta^2}{T}
 -\frac{F\cdot\nabla T}{T^2}\ge0.
\]

On each face its heat contribution is
`L_ij(1/T_j-1/T_i)>=0`. At zero temperature the code evolves K directly;
the formal entropy rate can be singular at first heating. Full balances and
the distinction from persistent conduction are in [DERIVATION.md](DERIVATION.md).

## Exact inactivity and the floor mechanism

For every stored K, `rho<=rho_q` gives zero pressure, heaters, viscosity,
and both face luminosities. Initially cold material also stays exactly cold
while no cell meets both `rho>rho_q` and `tau C>1`. The evolving quiet-domain
tests compare directly against independent gravity-only motion, including
an expanding perturbation and dilute material carrying retained heat.
These statements establish conditional forest inactivity. Actual forest
density and compression histories have not been compared with these scales;
small acceleration alone is not the activation criterion of this replacement.

At a global material minimum of K, outward loss is zero and incoming heat is
nonnegative. Both local heaters are nonnegative. While geometry remains valid,

\[
 D_+\min_i K_i\ge\min_i Q_i\ge0,
\]

where Q is the local heater contribution. This preserves an established floor.
For example, mesh-uniform heating `Q_i>=q_0>0` throughout a fixed interval of
length Delta t would produce and preserve `K_min>=q_0 Delta t`. A central
prefix additionally needs its outer guard above the proposed barrier or an
insulated outer face. The present runs record guards and zero-inclusive minima;
they do not prove those hypotheses uniformly in the continuum limit.

There is no inserted entropy floor, sorting, energy reset, or accepted-state
projection. Virgin collapse must seed its own entropy. The law cannot heat a
cold center solely from an outer heater because it transfers heat outward.
It also admits other ordered stationary states with vanishing central K;
the singular thermal cusp in [DERIVATION.md](DERIVATION.md) is an explicit
counterexample to any unconditional claim for all initial data.

## Cold collapse, refinement and relaxation

Units are `G=rho_q=Kstar=1`, hence `a0=sqrt(8pi)`. Fix `tau=0.5`, `D=0.1`,
`alpha_v=1`, `chi_d=chi_g=0.01`, and `ell_g=0.1` on every grid. The initial
sphere has `rho=0.25`, `R=1`, `v=-0.25r`, `K=0`, and `M=pi/3`.
All four grids reach t=32. The following zero-inclusive central minima use
real samples within the same absolute window 24<=t<=32:

| Shells | Minimum inner-5% K/Kstar | Final mean inner-5% density | Relative late density span |
| ---: | ---: | ---: | ---: |
| 32 | 0.3493312591 | 2.310131935 | 1.22609e-4 |
| 64 | 0.3495330395 | 2.319437245 | 1.21227e-4 |
| 128 | 0.3495986336 | 2.321444564 | 1.19069e-4 |
| 256 | 0.3496197548 | 2.322288903 | 1.18470e-4 |

Maximum late hydrostatic residual is `4.53e-5` of gravity; kinetic/binding
ratio is below `2.06e-12`. These meet the declared settling criteria, including
a force check that excludes a verdict based only on small motion. Across
all recorded samples from t>=8, all-material K remains above `0.3337Kstar`
on every tested grid. This is a finite measured floor, not an extrapolated
lower bound for arbitrary N.

Ancestry-aware accepted-state energy error is at most `1.03e-8`; separately,
the maximum error among recorded diagnostic samples, including dense output,
is `4.38e-8`. Neither is a rigorous bound between integration times. Tightening
time tolerances tenfold changes final N256 K, density and radius by less than
`7.62e-9` relatively; tight-chain accepted-state and sampled energy errors
are below `2.65e-9`.

At N64, unperturbed evolution, 1% radius compression, 1% expansion, and a
prepared energy-neutral entropy mode all relax through t=64. Their late
density spans are below `1.08e-7` and hydrostatic residuals below `1.60e-7`.
Radius preparation work is recorded rather than removed. Expansion completes
with an unchanged-RHS Radau-to-BDF continuation; historical capped attempts
retain their original statuses. These are controlled radial relaxation tests,
not a general eigenmode or nonradial stability proof.

![Collapse, contraction and spatial refinement](analysis_v2/settling_refinement.png)

The negative control uses persistent conduction at N32 through t=16; the
selected-law curves use N256 through t=32. Their differing grids and end times
make the visual comparison illustrative. Selected-law N32 independently
settles in the table, while persistent N32 contracts to mean inner-5% density
9.31 and loses central entropy. Damping alone leaves adverse entropy ordering.

The independent regular isentropic calculation uses only continuum initial
mass and total energy. It predicts `K/Kstar=0.3496240637`, finite central
density `2.455533677rho_q`, surface radius 0.537920622 and half-mass radius
0.404769307. The observed N256 central-cell K differs by `9.39e-6` relatively;
its half-mass radius is 0.404771351. This agreement supports a particular
regular endpoint without supplying a convergence theorem. No NFW fit or
unmeasured half-density core radius is used as evidence.

## Reproduction and remaining obligations

Run the new area and inherited material tests separately from the repository root:

```bash
python3 -m unittest discover -s rebuild_2026_10_22/X48_native_cf_zoom/stable_stress_search/entropy_transport -p 'test_*.py' -v
python3 -m unittest discover -s rebuild_2026_10_22/X48_native_cf_zoom/stable_stress_search -p 'test_*.py' -v
```

Every bounded run has a declared contract, exact command, source/restart/output
hashes and logs. [PROVENANCE.md](PROVENANCE.md) indexes them;
[REVIEWS.md](REVIEWS.md) distinguishes independent review scopes.
[STATUS.md](STATUS.md) records the live checkpoint and open obligations.

The outstanding mathematical steps are a mesh-uniform seeding/guard estimate,
controlled geometry and convergence, and nonlinear stability of the coupled
transport equations. Physical tests still needed include cosmological forest
histories, an exterior halo, and responsive rotating baryons. Earlier
[smooth baryonic loading results](../README.md) concern the same pressure law
but separate static configurations; this phase does not add an evolved disc
or baryon-contraction test. The closure remains a proposed Newtonian material
model with additional scales, not a derived microscopic dark-energy theory.
