# PQ: nonlinear future-global homogeneous branch and de Sitter attraction

**Verdict: proved under the restrictions stated below.** This is a
nonlinear homogeneous solution family of the same CA4-GNC-PQ common action,
with the metric and all five carrier fields evolving. It is stronger than
a fixed-background carrier theorem, but is not a global theorem for
inhomogeneous initial data or the complete gravitational Cauchy problem.

## Precise claim and action reduction

Use compact flat spatial topology `T^3`, proper cosmological time `tau`,
`ds^2=-d tau^2+a(tau)^2 dx^2`, no ordinary matter, bare `Lambda=0`, and
the homogeneous inactive branch. Assume

```
Mpl>0, M>0, m>0, mu>0, V0>0, gamma real and finite,
a(0)>0, finite canonical homogeneous initial fields and velocities,
H(0)=+sqrt[(E(0)+V0)/(3 Mpl^2)].
```

Here `Mpl^2=(8 pi G_bare)^(-1)` is the cosmological Einstein coefficient;
it is not obtained by silently substituting the local measured Newton
constant. The host parameters obey their declared PQ domain. None of
their nonzero-momentum stability estimates is needed for this homogeneous
theorem.

Let `phi=(u1,u2)`, `chi=(u3,u4)`, `s=u5`, all canonically normalized,
with `Psi=(u1+i u2)/sqrt(2)` and `Chi=(u3+i u4)/sqrt(2)`. Write

```
Vmix = M^2 |phi|^2/2 + m^2 |chi+gamma s phi|^2/2 + mu^2 s^2/2,
V = V0 + Vmix,
E = |v|^2/2 + Vmix,  v=du/dtau.
```

The exact action is specified by
[FINAL_ACTION.md](../action/FINAL_ACTION.md),
[PERSPECTIVE_VARIANT.md](../action/PERSPECTIVE_VARIANT.md) and
[VACUUM_STIFFNESS_VARIANT.md](../action/VACUUM_STIFFNESS_VARIANT.md).
The last adds `-V0 zeta z^2`, with `z=Z-<Z>_h`, to the perspective
carrier. The auxiliary `t=1+z` is distinct from the time coordinate.

Choose `Z=U=W=L=lambda0=0` and the clock equal to proper cosmological
time. Then `N=1`, `X_clock=1`, all spatial gradients vanish,
`K=3H` is spatially constant, `Q_K=0`, `z=0`, `t=1`, and
`Y_h=-theta<0`. Every added gravitational term and its first variation
vanish: this includes the centered-trace mean, the compensator, the heat
multiplier equations and the quadratic vacuum repair. The homogeneous
carrier source also vanishes after projection,
`sigma-<N sigma>_h/N=0`, even when its energy is nonzero. The projector
metric/clock contributions vanish on this branch. At `t=1`, `K_d-W_d`
is exactly the ordinary covariant canonical scalar Lagrangian.

These facts check the full equations on the ansatz, rather than only
substituting the ansatz into the action before varying. The remaining
minisuperspace action per unit coordinate volume is, before fixing lapse,

```
L = -3 Mpl^2 a adot^2/N + a^3 |udot|^2/(2N) - N a^3(V0+Vmix).
```

Thus the exact reduced equations are

```
u'=v,
v'=-3H v-grad Vmix(u),
a'=H a,
3 Mpl^2 H^2=E+V0,
H'=-|v|^2/(2 Mpl^2),
E'=-3H |v|^2.
```

The sign of the square root selects the expanding branch. The constraint
`C=3 Mpl^2 H^2-E-V0` obeys `C'=0` under the displayed evolution. No
decay rate, energy sink, independent fluid, or particle population has
been added.

## Future-global proof

Set `Hmin=sqrt[V0/(3 Mpl^2)]>0`. The constraint gives
`H=sqrt[(E+V0)/(3 Mpl^2)]>=Hmin`. This is a smooth function of `(u,v)`
because of the strict floor. Since `E'<=0`, write `E0=E(0)` and obtain

```
|v| <= sqrt(2 E0),
|phi| <= sqrt(2 E0)/M,
|s| <= sqrt(2 E0)/mu,
|chi+gamma s phi| <= sqrt(2 E0)/m,
|chi| <= sqrt(2 E0)/m + |gamma| (sqrt(2 E0)/mu)(sqrt(2 E0)/M).
```

Hence every energy sublevel is compact, despite the interaction potential
not being globally convex. The polynomial force is bounded and locally
Lipschitz on this compact set. The finite-dimensional local ODE solution
therefore cannot reach a finite-time continuation obstruction. It exists
for every `tau>=0`. Moreover,

```
Hmin <= H(tau) <= H(0),
a(0) exp(Hmin tau) <= a(tau) <= a(0) exp(H(0) tau).
```

The scale factor is positive and finite at every finite proper time.
This also supplies a global future timelike clock on this exact family;
it does not infer one from the phase of either complex carrier field.

## Attraction to the zero excitation state

Integrating the energy identity gives

```
integral_0^infinity |v|^2 d tau <= E0/(3 Hmin).
```

Both `v` and `v'` are bounded on the compact energy sublevel, so
`|v|^2` is uniformly continuous. If it stayed above a fixed positive
threshold along an unbounded sequence, bounded derivative would give
infinitely many disjoint intervals of uniformly positive integral. This
contradicts the displayed finite integral. Therefore `v(tau)->0`.

For completeness, the remaining position convergence does not assume
`v'->0`. The autonomous `(u,v)` trajectory is precompact and its energy
has a limit `Einf`. Let `p` be any accumulation point at times
`tau_n->infinity`. By continuous dependence on initial conditions, every
fixed finite forward segment from `p` is the limit of the segments from
`(u(tau_n),v(tau_n))`. Its energy is identically `Einf`, since
`E(tau_n+sigma)->Einf` for each finite `sigma>=0`. The exact dissipation
identity and `H>=Hmin` force `v=0` on this limiting segment. Its equation
then requires `grad Vmix(u)=0`.

There is exactly one critical point. First the `chi` equation gives
`chi+gamma s phi=0`; inserting this into the `phi` equation gives
`M^2 phi=0`; the `s` equation then gives `mu^2 s=0`. Thus
`phi=chi=s=0`. Every accumulation point is consequently the origin.
Compactness now implies

```
u(tau)->0,  v(tau)->0,  E(tau)->0,
H(tau)->Hmin,  H'(tau)->0.
```

This is asymptotic de Sitter expansion in the stated Hubble/curvature
sense. No exponential convergence rate, or finite limiting value of
`a exp(-Hmin tau)`, is inferred from this argument.

The strict `mu>0` restriction is substantive. At `mu=0`,
`phi=chi=v=0` with arbitrary constant `s` is an exact line of equilibria;
convergence of all fields to zero is false. The earlier massless slow-wave
witness is a different parameter regime. For the contracting branch the
energy derivative has the opposite sign, so this future-global proof
does not apply. Removing `V0` also removes this proof's strict Hubble floor.

## Exact charge and interpretation

Use the positive charge convention for a `Psi=A exp(-i M tau)` rotation:

```
j_Psi = u2 v1-u1 v2,
j_Chi = u4 v3-u3 v4,
S = gamma m^2 s (u1 u4-u2 u3),
j_Psi' + 3H j_Psi = S,
j_Chi' + 3H j_Chi = -S.
```

Therefore `a^3(j_Psi+j_Chi)` is exactly conserved, and component charge
transfer is internal. Its nonzero constant is consistent with attraction:
the physical charge density decays as `a^-3`, while the spatial volume
grows. This is cosmological dilution, not outward clearing from a halo or
destruction of conserved charge. In particular, homogeneous initial data
cannot test outgoing packet transport. Initial energy and total charge
remain free initial data, not a predicted dark-sector abundance.

## Bounded independent finite control

[homogeneous_frw_refined_check.py](homogeneous_frw_refined_check.py),
with its [contract](homogeneous_frw_refined_contract.json), integrates all
five fields, their velocities, `H` and `log(a)`, plus energy and component
charge ledgers. `H` is independently evolved by Raychaudhuri, so the
Friedmann constraint is a genuine numerical check, not imposed at each
step. Symbolic checks separately verify its exact propagation, the energy
and current identities, critical-point elimination, and the massless
flat-direction control. A finite-difference potential derivative check
audits the numerical force implementation; the zero-field de Sitter
solution checks the background normalization.

The accepted run is
[run_homogeneous_frw_002/manifest.json](run_homogeneous_frw_002/manifest.json)
and contains 43 exact/finite checks. Parameters are
`Mpl=100, V0=.01, M=3, m=1, mu=.5, gamma=.2`, initially rotating
`Psi` amplitude one, rotating `Chi` amplitude `.001`, `s=.001`,
`sdot=0`, and `a=1`. The initial excitation energy is
`18.000002565`. DOP853 solves to `tau=6000`, retaining 3001 times,
with `(rtol,atol)=(3e-11,3e-14)` and `(3e-13,3e-16)`.

The finer result is:

| Quantity | Result |
| --- | ---: |
| `E(6000)/V0` | `1.1702946309746118e-4` |
| `H(6000)/Hmin` | `1.0000585133060877` |
| `a(6000)` | `248.69694080651578` |
| Maximum Friedmann residual divided by `V0` | `1.4525056504788303e-9` |
| Maximum energy-ledger error divided by initial excitation energy | `8.07452754936474e-13` |
| Maximum relative comoving-charge error | `1.2410734966163118e-10` |
| Relative final Hubble difference between tolerances | `5.61770225893099e-8` |
| Relative final scale-factor difference between tolerances | `1.5720218193848723e-7` |

The finite calculation illustrates the exact branch and checks its
implementation. It is not the infinite-time proof, an observational fit,
or evidence of inhomogeneous stability. The very small net component
transfer in this homogeneous witness is not used as a conversion claim.

The first run,
[run_homogeneous_frw_001/manifest.json](run_homogeneous_frw_001/manifest.json),
is preserved and **excluded**: at looser tolerances it failed the final
two-tolerance Hubble-agreement assertion. Both trajectories had passed
initial-density-scaled constraint bounds, which did not ensure the stated
accuracy relative to the much smaller late vacuum density. The refined
run tightened both integrations and added an explicit vacuum-density
residual test. The failed source [homogeneous_frw_check.py](homogeneous_frw_check.py)
is unchanged; no failed output is counted as accepted evidence.

The run is bounded by 120 seconds wall time and 110 seconds per-process
CPU, with a cooperative numerical-library thread cap of one. No memory or
CPU-affinity cap is claimed. Exact manifest provenance distinguishes the
finite result from this analytic proof, which is not Lean-formalized.

## Scope and source versions

This proves future-global homogeneous dynamics and attraction for every
finite homogeneous datum in the specified expanding, positive-mass,
positive-floor branch. The spatially inhomogeneous constraints, switching
regions, general clock/metric evolution, full Dirac count, observational
requirements and a coupled global PDE theorem remain outside the proof.
The theorem does not transfer automatically to another action or potential.

The action sources were read at these SHA-256 values:

- `FINAL_ACTION.md`: `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`.
- `PERSPECTIVE_VARIANT.md`: `36efa45459468d22c1f2553cbcd5d2a2349bef56c6df1e03a5b9fefb9806d78b`.
- `VACUUM_STIFFNESS_VARIANT.md`: `7d64ced9c768ade3c728b78d80f919d1a086344bbb143fbe9a0251cd1bd35598`.

The shared repository was dirty at HEAD
`ecffd2af3623ff3e32318234fd51e1fac50b9126`. The argument uses elementary
finite-dimensional continuation and continuous dependence, proved applicable
by the explicit compact bounds above; no unverified external cosmological
theorem is used to supply the convergence conclusion.
