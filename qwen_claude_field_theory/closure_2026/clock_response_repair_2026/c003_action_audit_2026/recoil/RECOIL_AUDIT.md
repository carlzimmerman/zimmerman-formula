# C003 recoil: independent microphysics audit

Primary proof-audit verdict: **refuted, with the explicit 650 km/s counterexample**, for the L189 implication that an isolated relativistic `X -> X' + phi` massless emission gives `(M-m)/M = (v_k/c)^2/2`. The same expression is a leading approximation to the daughter kinetic energy divided by the initial rest energy. It omits the larger emitted scalar energy.

The literal isolated massless-decay realization is dead with the stated mass-loss budget. A corrected decay/scattering/clock-medium realization remains open; this audit does not prove a no-go theorem for arbitrary clock actions or disprove a cosmological fit. No full field theory was derived or checked by the five Lean certificates.

## Claim card and scope

- Authoritative source: `fable_independent_2026/L189_clock_frame_kicks.py`, opening docstring and V4/G8 check; numbers read from `L189_results.json` at base Git HEAD `1f0306787590840947e8e22cadfcabb9e162bb8d`.
- Claim: a heavier cold state emits a clock/MOND-scalar quantum, gives the daughter an isotropic 650 km/s kick, repeats with Poisson mean `2.3077948724637416`, and preserves matter mass to better than `1e-3` using the quadratic split.
- Audit assumptions: isolated two-body event, local parent rest frame, positive energies, ordinary special-relativistic mass shells, scalar mass `mu >= 0`, daughter speed `0 <= beta < 1`, and a specified state reservoir for repetition. These are assumptions to be implemented by a theory, not consequences of calling a field a clock.
- Units: `c=1` in the derivations; exact SI `c=299792458 m/s` and `v_k=650000 m/s` in the quantitative counterexample. The original rounded `c=299800 km/s` proxy is separately reproduced.
- Arithmetic: exact symbolic rational functions and exact rational counterexample; 80-digit numerical checks on an explicit 72-point massive grid; Poisson sum `k=0,...,59` with a separately computed tail. No random draws.
- Excluded conclusions: no halo retention fit, CLASS spectrum, Lyman-alpha transfer, global Omega_m limit, decay amplitude, stability, or strong-coupling result is inferred.

## Exact event accounting

Let the initial rest mass be `M>0`, daughter mass `m>0`, emitted scalar mass `mu>=0`, and common outgoing momentum magnitude `p`. In the parent rest frame,

\[
 M=E_d+E_\phi,\quad E_d^2-p^2=m^2,\quad E_\phi^2-p^2=\mu^2.
\]

Subtracting the shells and combining with energy conservation gives

\[
 E_d={M^2+m^2-\mu^2\over2M},\qquad
 E_\phi={M^2-m^2+\mu^2\over2M},
\]

\[
 p^2={[(M-m)^2-\mu^2][(M+m)^2-\mu^2]\over4M^2}.
\]

The physical decay domain also requires `M >= m+mu`; real `p` alone would not select the physical branch. Nonzero `p` and positive energies imply the strict inequality `M>m+mu`. The total energy, including all products, is exactly conserved. The sum of the final rest masses is smaller than `M` by the total outgoing kinetic energy:

\[
 M-m-\mu=(E_d-m)+(E_\phi-\mu).
\]

These relations agree with the checked primary reference, PDG *Kinematics*, 2025 update, sec. 49.4.2, equations (49.16)-(49.17). The local derivation, rather than an imported theorem, supplies the audit's algebraic implication. [PDG review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-kinematics.pdf).

For `mu=0`, set `beta=p/E_d`, `q=m/M`, and `a=E_d/M`. Then

\[
 q=\sqrt{1-\beta\over1+\beta},\quad
 a={1\over1+\beta},\quad
 {E_\phi\over M}={\beta\over1+\beta},\quad
 {K_d\over M}=a-q.
\]

Hence

\[
 {M-m\over M}=1-q
 =\beta-\tfrac12\beta^2+O(\beta^3),\qquad
 {K_d\over M}=\tfrac12\beta^2+O(\beta^3).
\]

At 650 km/s:

| Quantity, relative to initial `M` or `Mc^2` | Value |
|---|---:|
| `beta` | 0.002168166618788 |
| Lost daughter rest mass `1-q` | 0.002165821233493 |
| Radiated scalar energy `1-a` | 0.002163475842685 |
| Daughter kinetic heating `a-q` | 0.000002345390808 |
| L189 quadratic mass-split proxy | 0.000002350354984 |

The actual lost daughter rest mass is 921.49 times the L189 proxy. More directly, substituting the alleged daughter mass `m/M=1-beta^2/2` into `q^2(1+beta)=1-beta` gives a nonzero exact rational residue. This is a valid counterexample under the normalized `M=1` positive-energy decay hypotheses. The Lean proof checks the incompatibility without rounding or choosing a numerical square root.

## Massive scalar and the matter bookkeeping exception

For prescribed daughter speed and `y=mu/M`, energy conservation becomes

\[
 1=\gamma x+\sqrt{y^2+\gamma^2\beta^2x^2},\quad
 x={m\over M},\quad\gamma=(1-\beta^2)^{-1/2}.
\]

The physical solution for `0<=y<1` is

\[
 x=\gamma-\sqrt{\gamma^2\beta^2+y^2}
 ={1-y^2\over\gamma+\sqrt{\gamma^2\beta^2+y^2}}.
\]

The second expression is the numerically stable form used by the final script. Increasing `y` at fixed `beta` decreases `x`, so a positive massive scalar cannot reduce the rest mass lost by the original daughter below the massless value. This follows directly from monotonicity of the square root; the 72 numerical cases are supplementary finite checks.

However, the *sum* of retained matter rest masses is different from the mass of `X'` alone. If `phi` is massive, slow, stable, and belongs to the retained gravitating matter inventory, `M-m-mu` can be quadratic even though `M-m` is not. For example `mu/M=0.5` at the stated speed gives `1-m/M = 0.500002350465`, while `1-m/M-mu/M = 0.000002350465`. This is effectively production of two heavy products. Its number densities, trajectories, triggers, and emission thresholds must be included in a new simulation; the L189 single-daughter retention law does not test it. A fixed positive scalar mass also eventually terminates a descending mass ladder.

## Repetition and reservoir

One transition `X -> X'` with a stable `X'` permits one kick. A small splitting alone does not supply another accessible transition. At the fitted Poisson mean,

\[
 P(N\ge2)=1-e^{-n}(1+n)=0.670939319745.
\]

Thus most of the fitted histories require an explicit ladder, repumping, or scattering process. For an ideal massless ladder with equal fractional ratio `q` at every step, `M_N=M_0q^N`. For `N~Poisson(n)` the exact generating-function identity gives

\[
 {\mathbb E[M_N]\over M_0}
 =e^{-n}\sum_{k=0}^{\infty}{(nq)^k\over k!}
 =e^{n(q-1)}.
\]

This rest-mass statement needs the count law and equal fractional splitting, but does not need angular isotropy. A fixed positive lowest mass and a finite number of internal transitions cut off the Poisson law. An infinite ideal ladder can have `q^N>0` for every finite `N` and a finite total available rest energy `M_0`; finite energy by itself does not forbid that mathematical construction. No such spectrum or rate is supplied in L189.

For a finite capacity of eight transitions, the requested count exceeds capacity with probability `0.0006569033`; those eight transitions require `1-q^8=0.0171958` of the initial rest mass reservoir. A single two-state transition misses 67.09% of the requested histories. Additional capacities and their exact Poisson tails are recorded in the results.

For energy bookkeeping in the original inertial frame, add the assumptions of independent rest-frame isotropic emission, an event count independent of emitted directions, and no forces or scalar reabsorption between events. The daughter four-momentum averaged over its rest-frame recoil direction equals `a` times the parent four-momentum. Starting at rest, therefore

\[
 {\mathbb E[E_N]\over M_0}=e^{n(a-1)},\quad
 {\mathbb E[K_N]\over M_0}=e^{n(a-1)}-e^{n(q-1)},\quad
 {\mathbb E[E_{\rm radiation}]\over M_0}=1-e^{n(a-1)}.
\]

These are exact within the stated ideal process. They are not a solution in an expanding halo, and isotropy in the parent rest frame is not exact isotropy in a distinct clock frame.

| Fitted fully exposed population, `n=2.3077948724637416` | Fraction of initial `M_0c^2` |
|---|---:|
| Lost surviving rest mass | 0.004985800565898 |
| Radiated scalar energy | 0.004980414856989 |
| Surviving kinetic energy | 0.000005385708908 |
| Original L189 linear quadratic proxy | 0.000005424137181 |

The L189 inequality `n beta^2/2 < 0.001` is true, but the corrected surviving-rest-mass inequality `1-exp[n(q-1)] < 0.001` is false. It requires `n<0.4619496374` at this speed. This is a failure of the check as applied to the fully exposed population. The universal mean requires the actual exposure distribution, reabsorption, and emitted component stress tensor; it cannot be read from this one conditional `n`. In particular the calculation does not by itself establish an observational Omega_m exclusion.

## Classical clock and constructive escapes

A prescribed frame or smooth deterministic clock value supplies neither a momentum sink nor an energy reservoir by definition. In a homogeneous background, a spatially translation-invariant local coupling cannot arbitrarily choose a stochastic momentum change without dynamical fields, radiation, scatterers, or an effective noise description carrying the compensating momentum. For any field-plus-particle realization the complete stress tensor must account for the outgoing four-momentum. This is the exact missing implication between a clock selector and the stochastic kick process.

A pre-existing propagating clock/MOND scalar could, in principle, carry classical wave energy and momentum. Its quanta need not be a newly introduced field species. That possibility still needs its spectrum, state or internal-energy reservoir, interactions, transition probability, dispersion relation, and stress transfer derived from an action. A field name does not establish these properties, and the present audit does not say they are universally impossible.

The cheapest constructive alternatives to discriminate are:

1. **Scattering or repumping:** give an existing dynamical clock medium an explicit energy and momentum budget, derive the coupled matter/medium collision term, and check whether it produces the fitted distribution and time dependence. The massless isolated-decay lower bound does not apply when an environment absorbs momentum.
2. **Massive retained products:** specify their masses and stable states, and evolve both products. This can preserve the total nonrelativistic mass inventory much better while invalidating the original single-daughter phenomenology.
3. **Nonrelativistic clock dispersion:** an excitation with `omega=c_s|k|`, `c_s << c`, in a Lorentz-breaking medium is not the ordinary massless shell used here. A rough soft-emission balance has radiated energy fraction of order `(c_s/c) beta`, rather than `beta`. The action must establish this dispersion and stability, and include the background recoil; the estimate is a possible escape, not a certificate of a theory.
4. **Accept a corrected ordinary decay:** specify a ladder and include the roughly 0.5% rest-energy transfer for fully exposed matter, then retest cosmology. Calling the energy transfer exactly conserved does not make it conserved *matter rest mass*.

The next constructive input is an explicit existing-field interaction and spectrum/dispersion, so that one can calculate the amplitude or classical force correlator and the complete matter-to-clock stress transfer. The fitted `Gamma` and `v_k` are insufficient to supply those missing data.

## Dependency and obligation audit

| Required implication | Evidence kind | Status |
|---|---|---|
| Positive-energy shells + event conservation -> two-body kinematics | Direct algebra, SymPy; partial Lean certificate; PDG cross-check | Passed |
| Massless recoil speed -> quadratic lost rest mass | Exact rational counterexample; Lean | Failed |
| Quadratic expression -> leading daughter kinetic heating | Exact formulas and expansion | Passed |
| Same speed + positive scalar mass -> smaller daughter loss | Direct physical root | Failed |
| `dm << m` -> repeatable transition with Poisson support | No spectrum or repump mechanism supplied | Incomplete |
| Specified constant fractional ladder + Poisson law -> expected surviving rest mass | Generating-function derivation + independently summed finite series | Passed conditionally |
| Isotropic direction -> deterministic individual `v^2+k v_k^2` | Only the conditional mean follows without further assumptions | Not established; retention audit belongs elsewhere |
| Conserved complete stress energy -> conserved nonrelativistic matter mass | Different quantities and dilution histories | Failed as an inference |
| Classical clock selector -> emitted mode, reservoir, stochastic rate | No field-level derivation in L189 | Incomplete |
| Recoil microphysics -> halo/cosmology gates | Outside this bounded audit | Not addressed |

## Executed checks and provenance

`numeric_run_002` and `lean_run_003` are the successful final runs. Each has a version-2 computation manifest containing actual argv, exit status, UTC times, input hashes before and after, Git commit/dirty state, effective wall/output/thread bounds, scientific result hashes, and stdout/stderr. `RUNS.md` records the failures and corrected causes as well as reproducible commands.

The numerical run checks ten exact identities/compatibility conditions, two independent Poisson sums, and 72 massive grid points. The grid maximum absolute invariant residue is `2.10844e-81`; the `N>=60` Poisson tail is `7.69367e-62`. Compatibility of the alleged quadratic split is recorded as false rather than hard-coding an expected gate verdict.

The Lean file proves five real-algebra theorems. The only reported axioms are the standard `propext`, `Classical.choice`, and `Quot.sound`; there is no `sorryAx` or project-added axiom. The proof does not formalize quantum fields, probability laws, perturbations, or observational closure. Standard compiled Mathlib dependencies are reused and their entire transitive binary closure is not independently hashed.

Skills used: computation-audit and proof-audit structured the claims and executable evidence; literature-check cross-checked only the stated PDG kinematics; proofread-math was used for conservative equation/notation self-review.
