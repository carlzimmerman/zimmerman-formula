# Capture and release: exact obstructions and an admissible reaction subsystem

20 October 2026. Assessment base `f659e6d8e1ee4cf2b756f091aff56b018da1fb1e`.
This is a separately dated analytic research attempt and focused audit. It does
not change CFG913/915/916, frozen criteria, or their classifiers.

**Normalized claim audited.** Does CFG916 LR-c, as actually written, supply a
conservative or thermodynamically derived transition of one cold medium that
caps capture at the current phantom, permanently protects retained overfill,
and releases member mass on crossing the adopted Jacobi sphere?

**Primary audit verdict: incomplete, with the smallest missing implication at
O1/O4.** The density projection and owner label do not specify a binding state,
phase-space transition, reciprocal work, or receiver. Exact LR-c is not a
regular finite-time conservative flow on its stated state space. Exact
one-way capture is also incompatible with finite-temperature detailed balance
at finite binding free energy. These are restricted mathematical obstructions,
not a universal impossibility theorem for capture and release.

The new constructive result below is a genuine mass-conserving reaction
subsystem with an explicit free-energy inequality. It demonstrates what a
physical completion must add and which exact LR-c properties it gives up.
A separate analytic Hill example refutes the interpretation of a spherical
Jacobi cut as a necessary condition for being bound. A two-stage rate lemma
quantifies the additional clock omitted by instantaneous release.

## Contract, dictionary and sources

The authoritative project standard is
`sol61_push/THEORY_NEXT_STEPS_2026-10-15.md`, especially O1, O3 and O4. It asks
for reciprocal currents, conversion work, physical initial states, a derived
partition, and shared gravity before another empirical score. CFG916 explicitly
lists capped capture, ownership and irreversible release as new posits.

- `t` below is CFG915/916's latched population, with drift/relaxation coefficient
  `alpha_t=0`. It is dynamically their collisionless class, not the canonical
  S3 meaning of a tethered, responsive polarization carrier.
- `f` is CFG915/916's mobile population, `alpha_f=0.5` or `1`.
- `C=m_ph` is the current nonnegative target cell mass. The capture proof uses
  a single eligible innermost cell, so the no-inner-deficit predicate is exactly
  satisfied and no clipping or nonspherical interpretation is needed.
- Both labels are positive real mass and their sum is counted once. Switching
  a label does not by itself change position, velocity, orbital energy or
  gravitational mass.
- All thermal statements assume a bath with positive temperature, finite state
  free energies and regular finite transition rates. Zero temperature, infinite
  barriers, external driving and hidden receivers are outside those statements.
- The reaction construction uses dimensionless particle/site numbers in one
  representative cell, fixed total number `N`, fixed site number `C`, and a
  binding energy per particle `B`. It is not an action derived from S2.

Exact source bytes, sizes and their hashes at the base are recorded in
`source_hashes.json`. All inspected sources equal their base-commit versions.
HEAD was initially the requested base and later changed externally to
`8d34dc761eb1d5b26bc96b302672a935a22c442c`. This agent performed no Git mutation.
Both observations are recorded; the assessment target remains the requested
base plus the pinned unmodified source bytes.

Principal locators:

| Obligation or definition | Exact source |
|---|---|
| finite local mobility classes fail; no universal no-go asserted | CFG913 `README.md`, opening and class table; `FROZEN_CRITERIA.md` |
| naming, alpha_t=0, LC and missing finite capture rate | CFG915 `README.md`, assumptions and G/PH1; `cfg915.py:156-300` |
| capped capture and retained overfill after falling phantom | CFG916 `FROZEN_CRITERIA.md:33-41` |
| owner state and irreversible release | CFG916 `FROZEN_CRITERIA.md:44-53` |
| spherical Jacobi prescription and effective masses | CFG916 `FROZEN_CRITERIA.md:55-75` |
| literal implementation of capture and release | CFG916 `cfg916.py:235-263` |
| inherited static release approximation and clocks | CFG916 `README.md`, M and PH1; `cfg916.py:1250-1267`; `cfg916_results.json/post_hoc/PH1_residual_tolerance` |
| existing kinetic equation already exchanges bath/field energy | CFG638 `README.md`, system and energy row |
| canonical action and population mismatch | canonical 2026-10-14 S2-S4; CFG888 `README.md`, equation dictionary |

The dependency graph is:

`canonical carrier/source mapping -> physical internal binding state + receiver
-> phase-space capture/release + ownership evolution -> finite release and
transport -> one candidate's galaxy/dwarf/merger/cluster scores`.

CFG916 tests a phenomenological projection downstream of the first two open
arrows. Its declared static scores do not establish those arrows.

## 1. Exact capped capture cannot be a regular conservative finite-time map

In an eligible cell the literal LR-c operation is

    delta = min(f, max(C-t,0)),
    (t,f) -> (t+delta,f-delta).

Take `C=1`, `N=t+f=2`. Both admissible states

    (t,f)=(0,2),       (t,f)=(1/2,3/2)

are mapped to `(1,1)`. All entries are nonnegative, both cells are settled,
and the innermost-cell condition removes the nonlocal deficit issue. The actual
CFG916 method, extracted without executing its module, returns these exact
binary-representable values. An independent rational oracle agrees.

**Lemma 1.** No regular Hamiltonian flow over a finite time on a state space
containing only the retained cold/source fields can equal this operation while
leaving every other field identical for these two inputs.

**Proof.** A regular Hamiltonian initial-value flow is injective: follow the
unique trajectory backward from its final state. Two distinct complete initial
states cannot have the same complete final state. The two inputs above would.
The same elementary uniqueness argument applies to any regular deterministic
ODE flow for which backward uniqueness holds. In a Hamiltonian extension some
additional coordinates must distinguish the outputs; they are not optional
if exact projection is to be its reduction. QED.

This does not prohibit an irreversible coarse-grained rule, a singular
infinite-rate limit, or approximate capture. It proves that using the literal
projection as the entire conservative dynamics omits a state/receiver. A
mass-conservation check on `t+f` cannot check that missing energy or information.

For fixed total cell mass `N >= sup C`, repeated eligible capture with no
release gives the exact history identity

    t_final = max(t_initial, sup_t min(N,C(t))).

For example the target history `1/2 -> 1 -> 1/2` leaves `t=1`, while a constant
target `1/2` leaves `t=1/2`, at the same final baryons and total cold mass. This
is allowed hysteresis, not a contradiction. It says that a physical state must
carry the memory whose alpha suppression is being invoked. Present density
and a current tidal radius do not determine it.

## 2. Finite-temperature detailed balance forbids exact absorbing capture

For one parcel at a fixed environment, let finite free energies be `E_f` and
`E_t`, `B=E_f-E_t`, and `theta=k_B T>0`. Finite equilibrium weights obey

    pi_t/pi_f = exp(B/theta),
    pi_f k_ft = pi_t k_tf.

Both weights are positive. Therefore `k_ft>0` implies `k_tf>0`. Exact permanent
retention with `k_tf=0` and an active capture channel is incompatible with this
detailed-balance contract. Exact instantaneous removal of all eligible `f`
also requires an infinite-rate or nonregular limit rather than finite rates.

Finite binding can make these errors small. For the two-state model,

    p_f,eq = 1/(1+exp(B/theta));
    p_f,eq <= epsilon requires B/theta >= ln((1-epsilon)/epsilon).

Neither `B`, `theta`, the barrier nor a reactivity appears in the LR-c rule.
They cannot be inferred from its having no newly scanned numerical constant.

This argument applies to time-reversal-related microscopic channels in a
specified bath. Astrophysical stripping can be driven, nonthermal and open;
then the drive, escaping products, receiver and inverse channel must be
specified instead. It is not legitimate to promote the equilibrium lemma to
a prohibition of all dissipative processes.

## 3. An explicit admissible capture/release subsystem

A small completion can be written without a chosen density gate. Use actual
binding sites, not a label-only projection. Let `t` be occupied sites,
`s=C-t` vacant sites, and `f=N-t` free particles. For fixed positive `N,C`,
the domain is `0 <= t <= min(N,C)`. Define

    F = theta [ f(ln f-1) + t(ln t-1) + s(ln s-1) ] - B t,
    a = lambda exp(B/(2theta)) f s,
    b = lambda exp(-B/(2theta)) t,
    R = a-b,
    dot t=R,  dot f=-R,  dot s=-R,    lambda>0.

The logarithms use fixed reference units; their reference chemical potentials
are absorbed in `B`. At the lower boundary `R>=0`; at the upper boundary
`R<=0`, so the physical domain is invariant. `N=f+t` and `C=s+t` are exact
stoichiometric invariants. On the interior,

    dF/dt = [theta ln(t/(fs))-B]R
           = -theta(a-b) ln(a/b) <= 0.

The last inequality follows directly from monotonicity of `ln`. This is a
thermodynamically admissible reversible reaction; the entropy production is
explicit. Its unique equilibrium satisfies

    t / [(N-t)(C-t)] = exp(B/theta).

The left side strictly increases from zero to infinity, proving uniqueness.
For every finite `B/theta`, `0<t_eq<min(N,C)`. For `N=2,C=1`, the equilibrium
at `B=0` is `2-sqrt(2)`, not one. Thus the construction supplies capture and
release, but does not silently preserve exact saturation or permanent tags.

Its mechanical/thermal ledger is also explicit. Let the internal binding
energy be `U_bind=-Bt`. For fixed `B`, capture rate `R>0` reduces that energy
by `B R`; the bath gains the same energy. Release absorbs it. If a host/tidal
variable changes `B`,

    dot U_bind = -B R - t dot B,
    dot E_bath = B R,
    dot E_source = t dot B.

These three contributions sum to zero. With spatially varying `B(x)`, the
bound material feels the force `+grad B`; the source must feel its reciprocal
reaction. Omitting that force/work would destroy the proposed budget.
Here the capture subproblem is co-located and carries no momentum impulse.
A full orbital capture that changes velocity or transfers material to a
host frame must separately include recoil, stress and its kinetic-energy
exchange. This packet does not supply them.

**New capacity/history obstruction.** Interpreting the current phantom as
this physical site capacity fails on LR-c's dwarf route. If baryon loss lowers
`C` below retained `t`, then `s=C-t<0`, outside the admissible domain. One must
release the excess, retain a separate material site/history stock, or abandon
the binding-site interpretation. Retaining historical sites can be physical,
but then the present-phantom capture cap is a second constitutive rule, not
automatically a consequence of occupancy. This is an exact domain obstruction
to this minimal completion, not a no-go for all forms of memory.

The construction adds a real binding state, site inventory, binding free
energy, bath and reactivity. None is derived by the cold label assignment or
the static S2 action. It is a useful explicit continuation, not a proposed
replacement empirical gate or a complete carrier action.

## 4. The adopted spherical Jacobi radius is not an escape criterion

CFG916 is entitled to declare its spherical release cut. The stronger physical
reading used in its D discussion, that all cold matter outside `r_J` is
unbound, is false even in the elementary circular-orbit Hill problem.

Take a smooth Plummer member of potential

    Phi_m=-mu/sqrt(x^2+y^2+z^2+a^2),

in the Hill tidal field of a point-mass host with circular frequency `Omega`.
The equations in the co-rotating frame are

    xddot-2Omega ydot = 3Omega^2 x - partial_x Phi_m,
    yddot+2Omega xdot = -partial_y Phi_m,
    zddot = -Omega^2 z - partial_z Phi_m.

These are the local second-order expansion of ordinary rotating Newtonian
gravity; the point-mass host has the factor `3-gamma=3` appearing in CFG916.
The x-axis saddle radius solves

    mu/(r_J^2+a^2)^(3/2)=3Omega^2,

which is precisely `r_J^3=Gm(<r_J)/(3Omega^2)` for this member mass profile.
The subspace `x=y=xdot=ydot=0` is exactly invariant. Its vertical equation is

    zddot = -Omega^2 z - mu z/(z^2+a^2)^(3/2),
    H_z = zdot^2/2 + V_z(z),
    V_z=Omega^2 z^2/2-mu/sqrt(z^2+a^2).

`V_z` is even, strictly increasing for `z>0`, regular at zero and tends to
infinity. Every nonzero finite-amplitude orbit is therefore bounded and
periodic. Choose units `Omega=r_J=1`, `a=1/2`,
`mu=3(5/4)^(3/2)` and vertical amplitude `A=3/2`. This orbit spends positive
time at `r=|z|>r_J` and remains bound forever in this exact model.

Its conserved Jacobi energy is `9/8-15sqrt(2)/8 = -1.52665...`, while the
x-axis saddle energy is `-21/4`. Its energy surface has open necks but its
particular invariant orbit does not escape. Thus even an above-saddle energy
alone is not a sufficient escape test. A distribution, escape channel and
transport time matter.

This is a valid analytic counterexample to the universal spherical-boundness
claim. It is a measure-zero invariant family; no robust three-dimensional
stability or retained mass fraction is inferred from it. It does not re-score
the phenomenological CFG916 cut, invalidate the radius as a scale, or predict
the Bullet. It prevents treating that cut as a derived phase-space theorem.

The scalar orbit was checked over eight normalized time units at two steps.
Absolute energy errors were `1.34e-10` and `8.45e-12`; the orbit crossed zero
four times and spent about 63% of the sampled interval outside the spherical
radius. The infinite-time boundedness follows from `V_z -> infinity`, not
from this finite integration.

## 5. Finite release adds a second necessary clock

CFG916 PH1 assumes every stripped element becomes mobile immediately, then
uses a linear median transport clock to estimate residual memory. A physical
finite release rate adds a delay even in the most favorable no-recapture case.

Let `T` denote still-latched member memory, `F` released but still-in-place
memory, and `X` transported-away memory. With constant positive release `k`
and drain `Gamma`,

    dot T=-kT,  dot F=kT-Gamma F,  dot X=Gamma F,
    T(0)=T0, F(0)=X(0)=0.

All three states remain nonnegative and `T+F+X=T0`. The exact in-place
fraction is

    q(t)=(T+F)/T0
        =[Gamma exp(-kt)-k exp(-Gamma t)]/(Gamma-k),   k != Gamma,
        =(1+Gamma t)exp(-Gamma t),                   k = Gamma.

For finite positive rates, `q(t)>exp(-Gamma t)` and `q(t)>exp(-kt)` for
`t>0`. Therefore `-ln(q_max)/Gamma` is only an infimum as `k -> infinity`;
finite release needs strictly more time. Necessary conditions for a chosen
age `tau` are

    Gamma tau > ln(1/q_max),    k tau > ln(1/q_max),

with a stricter joint condition given by the exact formula. Re-capture or
returned debris cannot improve this minimal one-way bound.

The following uses PH1's own residual tolerances and its *eRASS1 median* clock
for both samples, exactly as the source code does. It preserves that disclosed
linear approximation and is not a new cluster PDE or a frozen classifier.

| footing / sample | q_max | instantaneous release minimum, alpha_f=0.5 | k=Gamma minimum, alpha_f=0.5 |
|---|---:|---:|---:|
| canonical eRASS1 | 0.57244 | 1.809 Gyr | 4.724 Gyr |
| canonical ACCEPT | 0.41234 | 2.873 Gyr | 6.410 Gyr |
| alt eRASS1 | 0.34786 | 3.244 Gyr | 6.843 Gyr |
| alt ACCEPT | 0.34369 | 3.281 Gyr | 6.897 Gyr |

At `alpha_f=1` all times halve under this same conditional clock model.
There is no measured release age or derived `k` in these numbers.

For comparison, an illustrative first-release survival requirement of half
the dwarf stock over 12 Gyr implies `k_D <= ln(2)/12 = 0.05776/Gyr`, provided
a release event means irreversible loss and replenishment is absent. If the
same parcel-loss rate were used in clusters, the best possible residual after
3 Gyr would already exceed `exp(-3k_D)>=0.841`, before adding transport delay;
all PH1 thresholds are lower. Thus a *universal constant parcel-loss rate*
cannot meet those illustrative two ages. The necessary rate contrast is

    k_C/k_D > 12 ln(1/q_max)/(tau_C ln 2),

which is 3.22–6.16 for `tau_C=3 Gyr`, before the drain penalty. This is a
conditional necessary constraint on a physical energy/barrier mechanism.
The three-Gyr age is an example, not a measured cluster input, and none of
this excludes state-dependent, driven or reversible retention mechanisms.

## Obligation matrix and exact continuation

| Obligation | Verdict |
|---|---|
| literal cap preserves positivity and total cold mass | passed for the formula; exact one-cell replay and rational oracle agree |
| literal cap is a regular conservative flow with no extra state | failed by Lemma 1 |
| exact one-way capture has finite-T detailed balance at finite energy | failed under the stated bath contract |
| a reaction subsystem with actual mass/energy/entropy bookkeeping exists | passed for Section 3, conditional on its new site/bath/B/lambda inputs |
| this subsystem derives exact LR-c and its baryon-loss memory | failed: finite reverse flux; falling-capacity domain obstruction |
| spherical Jacobi cut is a necessary test of orbital boundness | refuted by the analytic vertical-orbit counterexample |
| CFG916 frozen static classes change | out of scope; no classes changed |
| finite release retains CFG916 PH1 timing | conditional: only the instantaneous limit attains that lower bound |
| a single physical candidate satisfies G, D, B and M | not addressed; remains open |

The cheapest useful next calculation is not a finer arbitrary gate. Specify
one actual internal degree of freedom that stores the latch, its reciprocal
binding energy `B`, its receiver and its material/site inventory. Derive its
phase-space reaction kernel and finite release rate. In a falling-baryon toy
host first verify positive site/history stock, energy exchange and whether the
retained t survives without violating the capacity domain. In a fixed tidal
host next compare escape flux with the spherical release projection. Only
then transport that same candidate's released mass using the sequential clock
or the existing one-dimensional PDE, and score its own predictions.

The strongest supported closure result is therefore a restricted obstruction
plus a counted reaction continuation. It closes the claim that LR-c itself is
already a physical transition. It leaves physical capture, warm support,
driven stripping, new internal memory and full-theory closure open.

## Reproduction, audit and limitations

No existing experiment was rerun. The script reads the lane AST and executes
only the isolated `Run3.capture` method. All finite inputs are declared in
the script and `computation_manifest.json`; all source hashes are checked
before/after. Run from repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 reviews/final_closure_push_2026_10_20/capture_dynamics/check_capture.py
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py reviews/final_closure_push_2026_10_20/capture_dynamics/computation_manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Outcome: six check groups pass; 303 interior reaction states, two deterministic
scalar-orbit integrations and eight conditional rate cases. Runtime about
0.08 seconds, observed peak RSS about 43 MB; one process and one numerical
thread. No hard memory cap was imposed; these are observed usage figures.
The v2 manifest validates with `run.status=completed`. The first manifest
validation rejected `declared_results` encoded as objects rather than path
strings; the encoding was corrected and the same bounded computation rerun.
No mathematical assertion or source lane changed in that repair.

Review provenance: the focused audit of the original LR-c implication and the
new lemmas here are **self-reviewed** in the same context. The analytic proofs
are not certified by the finite samples or by agreement with another agent.
No external theorem or novelty assertion is required for the elementary
arguments given above. The reaction construction is a new, explicitly scoped
research continuation, not a repair silently inserted into CFG916's proof.

A subsequent coordinator reconstruction is recorded separately in
`COORDINATOR_RECONSTRUCTION.md`. It re-derives the projection, reaction
inequality, energy ledger, Hill counterexample and sequential clock after
reading this result. It is a same-team non-blind review and agrees only with
the narrow hypotheses and limitations above; it is not microscopic validation.
