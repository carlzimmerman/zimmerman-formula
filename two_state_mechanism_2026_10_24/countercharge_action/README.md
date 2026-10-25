# Countercharge action: repulsion works; the minimal completion remains inadequate

We constructed an explicit neutral F / positive T / negative C inventory and
derived an electrostatic action from the existing spherical acceleration law.
The T and C charges are equal and opposite; conversion must create or consume
both. Matching the old weak-field tether strength fixes

    q/m = sqrt(4 pi G), alpha_G = Gm²/(hbar c).

Thus the charge coupling is no longer a free scan parameter. With m_C=epsilon*m,
the mass ratio controls the countercarrier response. The field scale is also
fixed by a0 and q/m. The neutral-state gap/rate is still not fixed by gauge
invariance unless a specific microscopic bound state is derived.

**The new action produces repulsive like-charge forces and a conserved energy
ledger. It does not yet produce a successful disk/dwarf/cluster mechanism.**

## What was built and checked

The electric displacement energy and its Legendre-dual Lagrangian are

    h(D)=D0²[-log(1-|D|/D0)-|D|/D0],
    ell(E)=D0|E|-D0² log(1+|E|/D0), D0=a0/sqrt(4pi G).

The resulting 3D equation is div D=rho_q, D=E/(1+|E|/D0), curl E=0. This is a
new variational solver, not the earlier prescribed curl-free D approximation.
It operates on periodic smooth manufactured sources for these tests.

| Check | Result |
|---|---:|
| 3D static field solves | 8, on grids 17³, 25³, 33³ |
| Largest relative Gauss residual | 3.63e-8 |
| Force versus energy-derivative mismatch | 1.86e-8 |
| Neutral-pair field-energy change, 25³ to 33³ | 1.97e-7 relative |
| Neutral-pair force change, 25³ to 33³ | 1.80e-6 relative |
| Like charges / opposite charges | Repel / attract |
| Two-carrier nonlinear mode integrations | 18 |
| Maximum relative mode-energy error, tighter tolerance | 9.68e-9 |
| Unit tests | 4 passed |

The mode calculation includes both inertias and conserves field+kinetic energy
without rescaling. It exhibits plasma oscillations, not invented damping.
The static like-charge unit test uses a uniform compensating background only
for periodic solvability; the physical model does not freeze its countercharges.

## Four restrictions that reduce the remaining search

**1. Countercharges cannot be ignored.** Where cold stationary T needs e=g,
the negative carrier acceleration is -(1+1/epsilon)g. It cannot remain cold and
stationary there. A light carrier responds faster. Its pressure, currents,
escape or rotational support must be part of the mechanism.

**2. The simplest plasma scaling supplies no population selector.** With the
same virial density/temperature prescription in all four numeric families,

    lambda_D/b = (1+epsilon)/6 sqrt((1+eta)/eta),
    omega_p*t_dyn = sqrt(3eta/[epsilon(1+eta)]), eta=5.364.

Mass and radius cancel exactly. At epsilon=.1, these give approximately .200 and
5.03. They therefore cannot select disks over dwarfs or clusters in this proxy.
Real transport, cooling, magnetic effects and gradients could break this scaling;
the calculation does not simulate their evolution or claim all plasma models fail.

**3. Keeping the acceleration relation restricts inner countercharge.** In the
cold spherical branch, at g0=.1a0, epsilon=.1 and a chosen .05 dex tolerance, the
enclosed negative-carrier number must be less than 1.97% of enclosed positive
carriers. Global neutrality then requires most countercharges elsewhere. Moving
them costs field energy. This is a necessary condition for that branch, not an
observed disk bound or a construction that actually moves the charges.

**4. The minimal microscopic and relativistic completions face obstructions.**
The field has a maximum displacement. Gauss's law forces a charged core radius
at least sqrt(Gm/a0). Requiring a controlled Coulomb atom outside that core and
epsilon in [1e-4,1] bounds its binding/virial-temperature ratio below 1.33e-26 even
for the coolest numeric family. This is a continuous analytic bound, not just
a missed point in a scan. It does not establish an ionization timescale.

Separately, the simplest Lorentz-invariant L(S), S=(E²-B²)/2, extension of the
required electric law has a characteristic mode with v²/c²=1+E/D0>1. It fails
the subluminal-propagation condition for that ansatz. A causal microscopic
completion cannot be claimed from the successful electrostatic tests.

## What remains open

There is now an explicit charge-conserving action to analyze, but it is not a
complete viable microscopic theory. A neutral precursor needs specified core or
binding physics; conversion must pay field, rest-mass and radiation energy;
countercharges must evolve; and the relativistic/collective completion must
resolve the propagation issue. None of these can be replaced by a type switch.

The strongest next route is an action for a collective medium or a different
field completion with a derived source response. It must recover the desired
acceleration law in its controlled limit, rather than assume the same local
constitutive law is fundamental at every scale. No new live-gravity formation
or acceleration-relation fit was performed this turn.

## Reproducibility and files

- [ACTION.md](ACTION.md): action, charge inventory, reaction ledger and analytic restrictions.
- [CONTINUOUS_BOUND.md](CONTINUOUS_BOUND.md): elimination of microscopic mass from the Coulomb bound.
- [AUDIT.md](AUDIT.md): evidence scope, force inventory and self-review.
- [field.py](field.py): full 3D electrostatic variational solver.
- [response.py](response.py): nonlinear plasma mode and RAR constraints.
- [run_action/results.json](run_action/results.json): all finite tests and screens.
- [run_bound/results.json](run_bound/results.json): continuous-bound numerical evaluation.
- [run_action/manifest.json](run_action/manifest.json), [run_bound/manifest.json](run_bound/manifest.json): completed hashed run records.

Basic reproduction from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python3 two_state_mechanism_2026_10_24/countercharge_action/test_action.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python3 two_state_mechanism_2026_10_24/countercharge_action/experiment.py --output /private/tmp/countercharge-action-reproduction.json
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python3 two_state_mechanism_2026_10_24/countercharge_action/continuous_bound.py --output /private/tmp/countercharge-bound-reproduction.json
```

For bounded provenance, use contract.json or bound_contract.json, all declared
execution_artifacts as repeated runner --input flags, a fresh output directory
and declared results.json. Time limits were 240 s and 60 s; both runs completed with
empty stderr. Manifests record exact argv and hashes. Prior sources remain intact.

Gauge conventions follow [Tong's QED notes](https://www.damtp.cam.ac.uk/user/tong/qft/six.pdf).
[DeRocco and Giffin's dark-plasma simulations](https://arxiv.org/abs/2411.11958)
motivate retaining collective carrier dynamics; their observational limits have
not been applied to this different nonlinear action. The new conclusions above
come from the stated derivations and tests, not a claim made by those sources.
