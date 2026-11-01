# Independent audit of preservation and finite-mesh continuation

Date: 2026-11-01. Primary verdict: **proved as written**, for the two claims
in `preservation_route.md` normalized below. This does not assert that the
specified virgin collapse has a mesh-uniform positive seed. That input remains
open. The source-driven comparison implication in `seed_route.md` also passes
the checks below, under its stated local-heater hypothesis.

## Claim cards and scope

**P: preservation.** Fix a finite ordered shell mesh, positive cell masses,
total mass `M`, and the exact nonnegative-K evolution of the selected outward
gated flux. If at a finite valid time `t_s` a central prefix of mass at least
`M_s` has `K_i >= k_0 > 0`, then for every `0 < M_c < M_s <= M`, every cell
whose inner material mass is at most `M_c` satisfies

\[
 K_i(t)\ge k_0\left(\frac{M_s-M_c}{M-M_c}\right)^3
 \quad(t\ge t_s).
\]

The same `k_0,M_c,M_s,M` give the same constant for every mesh. This is a
conditional implication: a common seed is a hypothesis, not a conclusion.
The exact cellwise bound is formula (12) of the audited note. Unequal masses
are used only in the abstract heat comparison; the continuation statement
below concerns the actual equal-mass code.

**G: global finite-mesh geometry.** For every fixed integer `N >= 2`, finite
initial state with strictly ordered positive interface radii and `K_i >= 0`,
and the stated positive material scales and selected transport parameters,
the exact conservative shell ODE has a solution with positive shell volumes
and ordered radii for every finite future time. Constants may depend on `N`
and on the initial state. This is not a continuum continuation theorem or a
mesh-uniform density bound.

The variables are real; all entropy arguments use the physical nonnegative
branch. The ODE's negative-stage extension is relevant only to local
Lipschitz continuation at `K=0`. Numerical accepted steps and dense output
are not the objects proved about.

## Dependency graph

The load-bearing graph contains no numerical trajectory or external physical
assumption:

1. Source definitions of geometry, `W`, `h`, heaters, and shared luminosity
   -> nonnegative orthant invariance and local Lipschitz vector field.
2. Face monotonicities -> cooperative prescribed-geometry heat operator ->
   actual solution dominates a source-free auxiliary solution.
3. Zero face luminosity at equal neighboring auxiliary K -> descending
   auxiliary order; maximum principle -> `0 <= k <= k_0`.
4. Thermodynamic normalization plus hot-to-cold face sign -> auxiliary
   entropy nondecrease, including initial zeros by positive approximation.
5. Seed entropy + order + maximum -> exact cellwise bound -> fixed-mass
   mesh-independent smaller-prefix bound (P).
6. Tail comparison -> permanent positive floor for each cell that ever
   becomes warm. Cells never warm -> bounded compressive logarithmic volume
   rate whenever their density gate is positive.
7. Exact mechanical energy identity + warm/cold bounds -> positive volume
   lower bounds and finite state bounds on every finite interval -> ODE
   continuation (G).

All leaves in 1--7 are source definitions, elementary inequalities, or
finite-dimensional locally Lipschitz ODE comparison/continuation. There is no
circular use of G in deriving the heat inequalities: those inequalities are
first proved on arbitrary compact intervals of valid actual geometry, and
only then used to rule out a finite maximal endpoint.

## Obligation matrix

| Obligation | Result | Decisive check |
| --- | --- | --- |
| Exact source and face indexing | passed | Code luminosity entry `i` is the common face between mathematical cells `i` and `i+1`; `-diff(L)/(dm W)` is incoming minus outgoing. |
| Positivity through `K_i=0` | passed | Outgoing entropy gate is zero; incoming flux and heaters are nonnegative. The damping memory gate is zero at zero K. |
| Cooperative heat operator | passed | Supplying K increases both nonnegative factors of L; receiving K decreases both. Incoming dependence and negative outgoing dependence give nonnegative off-diagonal effects. |
| Auxiliary order under arbitrary actual geometry | passed | At `k_i=k_{i+1}`, `L_i=0` and the difference derivative is `L_{i-1}/(dm_i W_i)+L_{i+1}/(dm_{i+1} W_{i+1}) >= 0`. |
| Actual ordering | out of scope | Neither proof needs it; actual heater differences need not have a sign. |
| Entropy normalization and moving W | passed | `d sigma/dk=1/(3 Kstar sigma^2)` and `T=3 Kstar sigma^2 W=3 Kstar rho_q psi^(2/3)`; sigma has no density dependence. |
| Initial zeros in auxiliary flow | passed | Positive constant approximation stays positive and bounded; finite-dimensional continuous dependence passes the entropy inequality to the limit. |
| Prefix algebra and cell intersection diagnostic | passed | Inner mass, rather than outer mass or cell center, is used; a positive fixed mass margin gives the claimed uniform constant. |
| Tail bound | passed | Closing the tail's left boundary removes a nonnegative actual inflow, so comparison is in the required direction. |
| Never-warm cell classification | passed | Nonnegative terms summing to `dot K_i=0` force the original heater to vanish; on `rho_i>rho_q` this implies `C_i<=1/tau`. |
| Energy cancellation for unchanged ODE | passed | The same total stress enters momentum and the material work law; heat flux telescopes. |
| Finite-N continuation | passed | A central energy barrier controls `r_1`; energy then bounds velocities, warm volumes and all K, while cold volumes have their own lower bound. |
| Source-driven auxiliary in `seed_route.md` | passed | Ordered prefix forcing preserves auxiliary order; entropy production integrates to `J_s dm B^(1/3)`. |
| Actual mesh-uniform virgin-sphere seeding | not addressed | The needed source or compression lower bound is explicitly an unproved hypothesis. |
| Continuum existence/convergence and central representative | out of scope | No compactness, PDE comparison, or pointwise center theorem is supplied. |

## Independent derivation of the decisive steps

### The heat operator and zeros

At fixed prescribed geometry write the face luminosity as `L(a,b)` with
`a=K_i/Kstar`, `b=K_{i+1}/Kstar`. On `a>b`, the raw entropy ratio has
derivatives proportional to `chi_g+b` and `-(chi_g+a)`. The function
`z/(1+z)` preserves these signs. The other factor is
`[A_i a-A_{i+1}b]_+`, where `A_j=(W_j/rho_q)^(3/2)>0`; it has the same
monotonicities. Both factors are nonnegative, and the zero branches retain
the monotonicities. Positive, unequal `W_j` do not invalidate this step.

Consequently `H_i=(L_{i-1}-L_i)/(dm_i W_i)` is cooperative. At `k_i=0`, its
outgoing luminosity is zero and its incoming luminosity is nonnegative. For
the full equation the original heater is nonnegative, and damping heating
is nonnegative and vanishes at zero K. This proves nonnegative orthant
invariance for the exact ODE; it does not rely on a solver's step rejection.

The heat-only auxiliary may use any continuous valid actual geometry.
No auxiliary momentum equation is needed. At a global auxiliary maximum
the incoming entropy gate vanishes, and at a global minimum the outgoing
entropy gate vanishes. Thus its minimum cannot fall and its maximum cannot
rise. On a boundary of the descending cone its equality face has zero gate,
and the displayed difference derivative in the matrix is nonnegative.
The locally Lipschitz tangent/first-contact argument therefore preserves the
cone. Neither monotonicity of density nor ordering of actual heated K occurs
in these arguments.

### Entropy, approximation, and the prefix indices

For positive auxiliary entries,

\[
 \frac{d}{dt}\sum_i dm_i(k_i/K_\star)^{1/3}
 =\sum_{i=1}^{N-1}L_i
   \left(\frac1{T_{i+1}}-\frac1{T_i}\right)\ge0.
\]

A nonzero `L_i` requires `psi_i>psi_{i+1}`, equivalently `T_i>T_{i+1}`.
Only `k_i` is differentiated in the entropy coordinate; moving density
weights enter instantaneous temperatures but generate no additional term.
Adding `delta` to all initial auxiliary entries gives minimum at least
`delta` and maximum at most `k_0+delta`. On every compact valid interval the
heat vector field is uniformly locally Lipschitz on that finite box. Taking
`delta` to zero passes the finite entropy sum inequality to the unique
nonnegative auxiliary. The positive approximants need not be below actual
K; the limiting auxiliary is the one used in comparison.

Initialize a descending auxiliary with `k_0` on the seeded prefix and zero
elsewhere. Put `s_0=(k_0/Kstar)^(1/3)` and `x=m_<i`. Then

\[
 M_s s_0\le S_k(t)
 \le x s_0+(M-x)(k_i/K_\star)^{1/3}.
\]

This directly yields formula (12). The ratio `(M_s-x)/(M-x)` decreases
in `x` when `M_s<=M`, so `x<=M_c` gives formula (13). In particular a cell
intersecting the material interval `0<m<M_c` has `x<M_c` and is included.
The assertion with `x=M_c` is also valid and only includes an extra boundary
cell when a mesh interface coincides with `M_c`.

The endpoint `M_s=M` gives ratio one, as the global minimum principle
requires. For `N=2` and a seed only in cell 1, the exact first-cell formula
is `K_1>=k_0/8`; a zero outer initial cell is permitted. At the outermost
cell a one-cell tail gives ratio one and no outgoing loss. These checks
also confirm the `j_s-i+1` and `N-i+1` indices.

### Tail floors and the geometry continuation argument

Restrict to cells `a,...,N` and close the auxiliary's inner boundary. The
actual first tail cell has the additional nonnegative term
`L_{a-1}/(dm_a W_a)`. Seeding only cell `a` gives
`K_a(t)>=kappa_a [dm_a/sum_{j=a}^N dm_j]^3` thereafter. If a finite maximal
valid time `T` existed, choose one positive time for each ever-warm cell.
Finiteness of N makes the maximum of these finitely many times less than T;
after that time every warm cell has a fixed positive tail floor. If there
are no warm cells this selection is unnecessary.

A cell never positive has `K_i=0` identically by nonnegativity. Its outgoing
flux and memory heater are zero, and all remaining terms in its K equation
are nonnegative. Therefore the old heater vanishes. Whenever
`V_i<dm_i/rho_q`, its gate is strictly positive, so `C_i<=1/tau`, including
the possibility `C_i=0`. Since `dot log V_i=theta_i`, each excursion below
the threshold can shrink at logarithmic rate at most `1/tau`. This proves

\[
 V_i(t)\ge\min\{V_i(0),dm_i/\rho_q\}e^{-T/\tau}>0.
\]

The source has `W'=h`, `0<=h<=1`, `W=rho` in the dense branch, and
`W>=3rho_q/2`. Thus `W>=rho` at every positive density. With

\[
 U=\sum_i dm_i K_iW_i,\quad
 T_{kin}=\tfrac12\sum_i\mu_i u_i^2,\quad
 \Omega=-G\sum_i\mu_i m_i/r_i,
\]

`rho_dot=-rho theta` gives
`U_dot=-sum_i V_i(P_i+q_i)theta_i`; the conduction term has zero sum.
Telescoping the staggered force gives the opposite stress work in kinetic
energy. Gravitational power cancels `Omega_dot`. This independently verifies
constant exact E for the unchanged heat-plus-damping ODE, including the
signed damping pressure `q_d=-zeta theta` in expansion.

Let `B=G sum_i mu_i m_i`. The ordering gives `Omega>=-B/r_1`. A cold cell 1
already controls `r_1` by the cold-volume bound. If cell 1 is warm with
protected coefficient `c_1>0`, then

\[
 E\ge \frac{c_1(dm_1)^2}{(4\pi/3)r_1^3}-\frac B{r_1}
 \longrightarrow+\infty\quad(r_1\downarrow0).
\]

Finite E therefore gives `r_1>=epsilon>0`, including the earlier compact
interval before all selected warm times. Then
`U+T_kin=E-Omega<=E+B/epsilon`. Positive node masses bound every velocity;
over finite T all radii remain finite. Each warm cell has
`U>=c_i(dm_i)^2/V_i`, so its volume is bounded below too. Finally
`U>=dm_i K_i(3rho_q/2)` bounds every K.

With radii bounded above, volume lower bounds imply positive interface gaps.
The volume centroids lie strictly inside their ordered cells; on this
compact finite-dimensional geometry set their separations have a positive
minimum. All denominators in the actual vector field are now bounded away
from zero. The max functions and memory gates have locally Lipschitz stage
extensions through K=0. The fractional-power temperature diagnostic is not
used in the evolution vector field. ODE continuation contradicts a finite
maximal endpoint. No step here supplies constants uniform in N.

## Supplemental check of the source-driven seed extension

For the prefix-forced auxiliary in `seed_route.md`, descending order survives
because the forcing `q(s) 1_{i<=J_s}` is descending. Its maximum is at most
`B(s)=int_0^s q`. In the stated units `Kstar=1`, its source entropy term is
at least `J_s dm q/(3B^(2/3))` away from zeros. To check the zero case, start
all entries at `eta>0`. The precise integrated lower bound is

\[
 S_{k,\eta}(s)\ge Ndm\eta^{1/3}
 +J_sdm\big[(\eta+B(s))^{1/3}-\eta^{1/3}\big].
\]

The heat contribution is nonnegative. Continuous dependence and `eta->0`
give `S_k>=J_s dm B^(1/3)`. In the revised seed note, combining with
`S_k<=(J_c-1)dm B^(1/3)+(N-J_c+1)dm k_{J_c}^{1/3}` proves the sharpened
(S1), with ratio `(J_s-J_c+1)/(N-J_c+1)`. Only the first `J_c-1` cells
need the separate maximum bound; every cell from `J_c` onward is bounded
above by `k_{J_c}`. This includes `J_c=J_s` and the small-grid cases.
Turning the auxiliary source off preserves its order, maximum bound and
entropy bound; actual sources remain nonnegative, so the same estimate
persists. This extension does not presume an exterior guard.

The exact cold phase, density threshold, and fixed-N continuity seeding
check against the source. In particular `M=pi/3`, the node gravity yields
`a''=-M/a^2`, and `C_a=5.4145849604427>4`. A fixed-N interval with `C_i>=4`
gives `Q_i>=64s^2(3-8s)` and seed `64T_N^3(1-2T_N)>0` when `T_N<=1/4`.
Its duration is not asserted uniform. The common leading activation cubic
and the explicit free-surface `N^2 s^3` correction also have the stated
normalizations: `mu_N=M/(2N)` gives surface acceleration coefficient
`24a_a^2N q_2 s^2`; integrating and using
`partial theta_N/partial u_N=3N/a_a` gives (S5).

Under (UC), `rho_dot=rho C`, `rho>=exp(cs)`, and monotonicity of h give the
stated q and B in (S3). The revised (S4) takes `J_s=ceil(N/4)` and
`J_c=ceil(N/20)` for every `N>=2`. Here `J_s-J_c+1>=N/5` and
`N-J_c+1<=N`, so the ratio is at least `1/5`. Thus the conditional floor is
`(64/125)T^3(1-2T)>0`. At small N the wider source prefix must heat the
entire last cell intersecting the quarter, exactly as the note states.
Consequently the source-driven extension removes the heat redistribution
obstacle but leaves (UC) unproved. Its heuristic penetration scales have
not been used here.

## Revision audit: startup bounds and total-stress equations

This extension reviews `seed_route.md` at actual SHA-256
`752944eb3c0c7ff87007b5ca1c3f5a46bb768d8215645914ad6b211cebcd053d`,
superseding the earlier source-driven subsection's conservative indexing.
The original preservation claim and its source hashes are unchanged. The
scope of the new check is the sharpened (S1)--(S4), (S6)--(S8), the scalar
stress obstruction, and the stated frozen-coefficient calculation. These
claims pass in their explicitly conditional or active-branch scope.

**Exact compression identity.** For signed compression `x=-theta`, direct
differentiation gives `x_dot=x^2-V_ddot/V`. Inserting the source nodal
momentum equation yields exactly the stress operator in (S6), the
gravitational difference `4pi G dm/V`, and the displayed R. On the active
branch `rho>1,C>2`, signed compression x equals the heater's positive
compression C, so (S6) is the claimed equation for C there. At a center
face the inner term is zero; at the exterior `S_{N+1}=0` and the actual
half node weight are required and retained. This is not a differentiable
equation for `max(-theta,0)` across `theta=0`.

Independently completing the square gives

\[
 R_i={C_i^2\over3}
 +{6ab(a u_{i-1}-b u_i)^2\over(a^3-b^3)^2}\ge0,
 \qquad a=r_i,\quad b=r_{i-1}.
\]

Equivalently the quadratic-form matrix in `(u_i,u_{i-1})` has the stated
diagonal entries and off-diagonal entry `-9a^2b^2`; its determinant is
`18ab(a^3-b^3)^2`. At `b=0` the remaining diagonal is nonnegative. Thus
there is no missing radial-shear sign assumption.

In the active normalized branch the total stress is exactly
`S=A b(K) C-A+K rho^2 h`. Its derivatives satisfy
`S_C=A b>0`,
`S_rho=A'(bC-1)+K(2rho h+rho^2 h')>0`, and
`S_K=A C b'(K)+rho^2h>0`. Here `b'(K)=.005/(K+.01)^2` and
`A' > 0`. Applying the ordinary chain rule with
`rho_dot=rho C` and `K_dot=Q+H` proves (S7). All its stated local reaction
terms are nonnegative; `S_K H` has no minimum-principle sign.

**Stress-minimum obstruction.** At constant active density, choose a bounded
nonnegative K profile with a positive fixed-amplitude jump downwards at an
interior positive mass radius. Choose constant S sufficiently large and
define C by the note's formula. This gives `2<C<=u` for some finite u
independent of N. It defines admissible velocities, not merely independent
cellwise divergence data: explicitly

\[
 u_i=-{\sum_{j\le i}V_j C_j\over4\pi r_i^2}.
\]

At the chosen K peak the incoming entropy gate is zero and its outward
luminosity is strictly positive, so `H_i<0` although `S_i` is a local
minimum. At fixed positive radius, `Delta r=O(1/N)`, `dm=O(1/N)`, and
the entropy gate tends to one for the fixed jump; hence this negative term
has magnitude of order `N^2`. Bounded C and constant rho give bounded
nodal velocities and velocity gradients under the displayed reconstruction,
so R and the other local reaction terms remain bounded. Thus sufficiently
large meshes even have negative `S_dot` at that interior constant-stress
point. This refutes discarding the heat term by a scalar stress minimum
sign argument. It is not a counterexample to (UC), since these instantaneous
states are not asserted to be reached from the specified initial data.

**Conditional amplitude bound.** On the actual central prefix, the bootstrap
`0<C_i<=u` gives `rho_i<=exp(us)` from its common activation density one.
At a prefix maximum of K the incoming supplier is within the same prefix
and cannot have strictly larger K; the exterior face can only remove heat.
The old heater is at most `u(u/2-1)h`, and damping heating is exactly
`.5 h C^2 K/(K+.01) <= 50u^2 h K`. The Dini maximum inequality in (S8)
therefore follows with no exterior-guard or heat-derivative assumption.
Integrating it gives the stated exponential bound. For
`T<=log(2)/u`, using `h(d)<=3(d-1)^2` and
`exp(uv)-1<=u exp(uT)v` gives the displayed cubic integral bound.

For `u=6,T=.005`, independent scalar evaluation gives

\[
 M_K(T)\le5.7586465542475474\cdot10^{-5},\qquad
 {(P+q_d)\over A}\le0.0172165834132935<0.0173.
\]

The relative stress formula is applied for `s>0` where A is positive, and
has continuous value zero in the right limit at activation. These are
conditional amplitude bounds. They do not establish either a lower or an
upper compression bootstrap and do not control stress curvatures.

Finally, for the stated constant-coefficient model,
`V=C+beta K/(nu-kappa)` does satisfy `V_t=nu V_xx` when `nu>kappa>=0`.
The activation ratio follows directly from the constitutive derivatives:
`S_K/S_C -> 4/3+100C_a`. This finite frozen-coefficient calculation is not
a diagonalization of the variable, nonlinear shell equations. The note
correctly leaves that implication open.

## Finite startup probe audit: first record

Outcome: **audited, not executed**. The implementation and serialized
assertion are consistent for the stated six finite grids, subject to
ordinary floating numerical error. This audit did not rerun an evolution.
The record is observational support for a startup estimate, not a theorem
for all N or for every time in an interval.

The documented command is `python3 .../floor_theorem/startup_probe.py
--output .../floor_theorem/startup_finite/result.json`, from the repository
root with the exact paths recorded in the manifest. Defaults select
`N=32,64,128,256,512,1024`, nominal duration `.005`, wall cap six seconds
per case, `rtol=2e-9`, `atol=1e-11`, and `max_step=.01`. The manifest
records process completion in 3.230174 seconds, exit status zero, a 45-second
wall cap and 40-second CPU cap, and fixed NumPy/SciPy versions. It pins
input hashes both before and after the run.

`StartupObserver` overrides diagnostics only. Its `(N+3)//4` includes
exactly every cell intersecting the quarter, and it reports compression
`max(-theta,0)` and the original source separately. It inherits the physical
fields and RHS unchanged. The preactivation integration in `refinement.py`
uses the exact K=0 invariant subspace until the activation event and then
hands the same state with zero K to the unchanged full physical RHS. This
is a numerical integration choice with finite event tolerance, not an
injected seed or an accepted-state projection. Prefix minima use all cells
intersecting the requested mass fraction, including a partial final cell.

The first result has **exactly two retained postactivation diagnostic rows
per N: the activation handoff and the final time**. The `samples=81`
argument is distributed over the entire cold-plus-warm duration by
`refinement.simulate`; its short warm phase receives only two samples.
Thus the contract/manifest field `samples_per_phase=81` is nominal metadata,
not the actual warm observation count. The serialized traces and this
two-row scope are authoritative for mathematical coverage. The explicit
non-claims about between-sample bounds remain correct. No continuous-time
startup assertion follows from these endpoint checks.

Recomputing summaries from the serialized traces gives minimum observed
quarter compression `5.414584959519096` over the six cases, with every
recorded sample above four. Each case reached nominal time
`0.5957973398405011`; actual duration after numerical activation was between
`.004999999980517145` and `.004999999981903702`. Final inner-five-percent
minimum K is about `3.61600123e-5`. The final dense-output and accepted-state
K minima differ by at most one ULP; they should not be compared by exact
floating equality. All cases report zero invalid dense samples and zero
accepted negative-K rejections. The maximum recorded energy-error bound
for accepted states is `2.1547535852488961e-10`, and the separately reported
maximum sampled error is `5.772157196659577e-10`. Neither is an interval
certificate or a rigorous bound on exact dynamics.

Manifest validation command:

```text
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py rebuild_2026_10_22/X48_native_cf_zoom/stable_stress_search/entropy_transport/floor_theorem/startup_finite/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Result: `valid evidence record (run status: completed); mathematical
interpretation requires review`. Current input and output hashes match the
manifest. This verifies byte-level provenance, not the mathematical target.

| Additional input or record | Actual SHA-256 read |
| --- | --- |
| `floor_theorem/startup_probe.py` | `8a83b7d26652be3c20181f4a94213b13ab3a7f892a2fbfef15b2abf284218272` |
| `refinement.py` | `faa09a692bb072a3198b18e53a711aa49cb51aef88fbdf5a94909ec46d37c523` |
| `floor_theorem/startup_finite_contract.json` | `b4243f1ad7da69ef1e2aec10b90a0c98c1a95a84b4d85bd3c3de88b1ba13af05` |
| `floor_theorem/startup_finite/manifest.json` | `6435d8877dafdf7bfb1c46f98100a86f12550210f76b978f151b697b1f7a7b1e` |
| `floor_theorem/startup_finite/result.json` | `3dca297152a24e8cadae597b5e81fa93e55a6241298eb14274ec7033d7ef2242` |

The observed HEAD for this revision audit was
`40d43dbb8a9f1517e214302380f7659df7626e6a`. Exact source and result hashes,
rather than a moving shared-checkout HEAD, identify the reviewed artifacts.

## Finite startup probe audit: resolved observation schedule (v2)

Outcome: **audited, not executed**. The v2 driver and stored finite assertion
pass this review, conditional on floating numerical error. No simulation
was rerun by this audit. The first driver and first record above remain
historical evidence with their two-row limitation; v2 supplies a separate
denser observation schedule, not a reinterpretation of the first record.

`startup_probe_v2.py` uses the same observer and invokes the existing exact
cold invariant-subspace phase with two samples until physical activation.
It passes that phase's unchanged final state to the existing
`convective.simulate` function, now with **81 warm samples** and final time
`activation+0.005`. Wall and RHS budgets are reduced by cold-phase use;
retry allowance is reduced by its cold domain rejections. No fields,
forces, heater, luminosity, physical parameter, seed, or state projection is
changed. The cold root locator remains a floating event calculation.

The accepted-state energy bound correctly references the original initial
energy: cold relative error plus warm relative error multiplied by the
handoff/original energy ratio. The record separately reports zero handoff
energy difference in every case, so there is no omitted reset term in the
triangle inequality. Exact K=0 handoff is also reported and verified in all
six cases. Sampled energy error is computed separately against the original
energy over both cold and warm diagnostic histories.

I independently parsed the full result and checked for each
`N=32,64,128,256,512,1024`: completed status; exactly 81 actual warm rows;
strictly increasing times; offsets matching `s_j=.005*j/80` to floating
roundoff; matching serialized minima and sample-pass flags; zero handoff
energy difference; zero K handoff; zero invalid dense samples; and zero
accepted negative-K rejections. The actual final offset in every case is
`0.0050000000000000044`, the expected floating representation of the
requested duration.

| N | Actual warm rows | Minimum sampled quarter C | Final inner-five-percent minimum K |
| ---: | ---: | ---: | ---: |
| 32 | 81 | 5.414584959525123 | 3.6160012752054674e-5 |
| 64 | 81 | 5.414584959532656 | 3.6160012750829255e-5 |
| 128 | 81 | 5.414584959536470 | 3.6160012749094795e-5 |
| 256 | 81 | 5.414584959537543 | 3.6160012746722913e-5 |
| 512 | 81 | 5.414584959529882 | 3.6160012739108130e-5 |
| 1024 | 81 | 5.414584959511289 | 3.6160012722190725e-5 |

The largest accepted-state energy-error bound is
`2.154751844772262e-10`; the largest separately sampled relative energy
error is `2.1676171968465496e-10`. These are numerical diagnostics,
not rigorous exact-solution bounds. This record has no interval arithmetic,
no convergence certificate over arbitrary N, and no lower bound between
diagnostic times. In particular all six successful finite sample checks do
not establish (UC) or the all-resolution target. They discriminate against
a large sampled central compression loss over this declared short window.

The documented command is the manifest's repository-root invocation of
`startup_probe_v2.py --output .../startup_finite_v2/result.json`, with all
other bounds supplied by the pinned defaults. The v2 manifest records
`run.status=completed`, exit status zero, runtime 4.210262 seconds, the same
45-second runner wall cap and 40-second CPU cap, and the exact cold and warm
sample counts in its contract. Its current input/output hashes pass the
installed computation-audit validator with `--root` pointed at the
repository; the result was again `valid evidence record (run status:
completed); mathematical interpretation requires review`.

| v2 input or record | Actual SHA-256 read |
| --- | --- |
| `floor_theorem/startup_probe_v2.py` | `2ae52135753191f0f7e9b95e26d095dfb1a7d8122b5cd9f9b88a7511eb4e9f01` |
| `floor_theorem/startup_finite_v2_contract.json` | `edc459fef86403eb92c5b291a584f2de218b63093a73582400c8394ccba15248` |
| `floor_theorem/startup_finite_v2/manifest.json` | `da5f3caea04d6b4aed5c637bceae2fdb0c994d1b97a944da469d8012dd22eaed` |
| `floor_theorem/startup_finite_v2/result.json` | `fde3c8b6494959f733163f89c7affa94a3e2be0b2639edec35df2ec9647af30c` |

The observed HEAD during v2 review was
`19ed7a5bc82c89938a1feceb445cc36735753b40`. The v2 manifest's execution
HEAD is `40d43dbb8a9f1517e214302380f7659df7626e6a`; its dirty working-tree
source hashes, which currently validate unchanged, identify the actual
executed bytes.

## Remaining gap and strongest safe statement

There is no missing implication within P or G under their stated exact-ODE
hypotheses. A positive broader-prefix seed implies a positive smaller-prefix
floor independent of elapsed time and mesh size; each fixed mesh continues
globally with valid geometry. These are the strongest audited statements.

For the original virgin-sphere, all-resolution floor objective, the smallest
remaining input is a finite-time positive seed on a fixed mass prefix with
seed strength and startup time controlled uniformly in N. The sufficient
formulation (UC) in `seed_route.md` remains an open way to obtain it. Ordinary
fixed-N continuity and a shared activation cubic do not prove that estimate.
The cheapest next load-bearing check is a proof of an interior compression
bound with a positive duration uniform in N, or a direct uniform K-seed
estimate. Additional finite-grid runs cannot replace that leaf. Continuum
existence and passage to a pointwise central representative remain separate.

## Source checks, commands, and review provenance

This is a fresh delegated independent proof audit. The critical inequalities
and mechanical energy cancellation above were reconstructed from the four
source files, not accepted from a prior review. The author notes were the
targets, not evidence for their own conclusions. No simulation was rerun.
Stored trajectories were inspected only in the separate finite-record audit;
none is a load-bearing leaf of the proof claims. No external literature
claim is load-bearing.

Commands executed included direct numbered source reads, direct note reads,
`git rev-parse HEAD`, scoped `git status --short`, SHA-256 calculation with
Python `hashlib`, and an independent scalar evaluation of the dust formulas
using Python `math` and SciPy quadrature. That last check returned
`t_a=0.5907973398405011` and cubic coefficient `271.02131326812383`; these
decimals are annotations, not proof inputs. Applicable `AGENTS.md` and local
`.mathbox` searches found none in the target ancestry or workspace.

The observed repository HEAD after reading and hashing the target sources
was `b601d76632c3860b73c6951813784a02f6818a2f`; a later concurrent observation
was `f3e1877327435b9f714f491349fdb32e8d1d0bad`. The target artifacts were
reported untracked. Accordingly neither commit identifies these source
bytes; the SHA-256 table below is the exact revision authority for this
audit. Historical HEAD `0fe706...` printed inside the notes is not claimed
to be the current repository revision.

Paths below are relative to `stable_stress_search/entropy_transport/`.

| Input | Actual SHA-256 read |
| --- | --- |
| `floor_theorem/preservation_route.md` | `c91f3e4800adf45d26f5b8472de2bffb9c933d906059573bb46d5df0ce1108fd` |
| `floor_theorem/seed_route.md` (current extended revision) | `752944eb3c0c7ff87007b5ca1c3f5a46bb768d8215645914ad6b211cebcd053d` |
| `convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `../material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `../collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `README.md` | `8719a07f915902b829030d178636e27602f362c0f0b0e4e9e5d02039f575d2f6` |
| `DERIVATION.md` | `e08312d0dc3be7f3f2d225ca938a7872ceec6d4c2532db2102f54c7a984910da` |

The earlier initial review covered seed-note hash
`42f27b18a706447b89d28ffdfe2183a51d85b30d76afd7ddf74f07dace2aeb6b`.
The revision-audit section above identifies the additional current scope.

Only this review file was written by this audit. No source, data, existing
route note, pinned checkpoint note, or ledger was changed.
