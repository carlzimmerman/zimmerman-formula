# Pair-merger energy, charge and intrinsic-spin ledger

20 October 2026. Bounded analytic/accounting audit of the same explicitly
modified three-field action. No merger, field evolution or outgoing solve
was run here. Cached mode/radiation manifests were validated against current
inputs. Exact source receipts and cheap numerical evaluations are recorded
in `sources_merger_ledger.json`.

**A positive-charge second-harmonic scalar outlet can pay part of a merger's
excitation and spin budget without violating energy conservation, provided
the remnant loses charge. It cannot be interpreted as cooling a fixed-Q
remnant.** A single fully chiral outlet also fixes the ratio of exported spin
to energy. At low incoming spin it can remove that spin while leaving most
of the binding release to other excitations/channels. Opposite chiralities
can avoid that restriction kinematically; their merger excitation and mixed
nonlinear radiation have not been computed.

## 1. Inputs, units and source revisions

Use `hbar=c=m_Psi=1`, charge weights `q_Psi=1`, `q_X=2`, and the real neutral
chi field. The potential is

```
V = |Psi|^2 + 4.0016 |X|^2
    + 0.002168 (X* Psi^2 + X Psi*^2)
    + lambda |Psi|^4 + 200 chi |Psi|^2 + U(chi),
lambda = 1.99 + 0.002168^2/4.0016,
U = 10000 chi^2/2 - 100 chi^3/8 + chi^4/4.
```

This is the changed common action, not the protected action with the old
`E >= |Q|` bound. Its established classical flat-space certificate is
`E >= 0.85 |Q|`. Q, energies, lengths and frequencies below are dimensionless
action quantities. No physical mass m, size in parsecs, galactic velocity
distribution or observational collision parameter is selected.

The earlier stationary continuum-style branch gives

```
E0(80000)  =  76151.17723365594,
E0(160000) = 149323.62958635326,
D_pair = 2 E0(80000) - E0(160000) = 2978.7248809586163.
```

The true-origin re-solve gives `2978.7248809235753`. The finest *matched
discrete mode backgrounds* instead have `E80=76151.04320363572`,
`E160=149323.43809465464`, and gap `2978.6483126168023`. The 0.0765683
difference is about 0.00257% of the gap. These are distinct numerical
discretizations of the same action. The earlier gap is a reference budget;
tables using it with the finite mode frequency are explicitly frozen-snapshot
estimates, not an exact solution at an uncomputed final charge.

The finest cached quantities are:

| Background Q | omega | Bound quadrupole Omega | Positive Psi lab frequency nu=omega+2Omega | gamma |
|---|---:|---:|---:|---:|
| 80000 | 0.9217875298228656 | 0.07546765515846882 | 1.0727228401398032 | 3.8003453684523445e-6 |
| 160000 | 0.9095163991702602 | 0.055984806795658586 | 1.0214860127615772 | 1.6773340732409204e-7 |

Here gamma multiplies the leading retained rotating-energy law
`dK_mode/dt = -gamma K_mode^2`; it is not a merger capture efficiency.
The lab frequency exceeds the free-Psi threshold 1 in both cases. The other
scalar vacuum channels are closed at the computed second harmonic.

## 2. Exact isolated ledger before making a mode approximation

Let two initially stationary Q=80000 fragments have total charge
`Qi=160000`. Write their actual conserved initial COM-frame energy as
`Ei=2 E0(80000)+delta Ei`. The correction includes relative kinetic energy,
finite-separation interactions and any prepared excitation; it is not
silently set to a gravitational binding or observed dwarf parameter.
Define `D=Ei-E0(Qi)`.

Let outgoing positive-Psi waves carry total charge `q>=0` and lab energy
`Eout`. With no other charge outlet the retained remnant charge is exactly

```
Qf = Qi - q,
Erem = E0(Qf) + epsilon_f,
Ei = E0(Qf) + epsilon_f + Eout + Eother,
Ji = Jf + Jout + Jother.
```

All angular momenta in this equation use the same origin and orientation.
Remnant recoil, residual orbital motion, other fields and external receivers
must be included in `epsilon_f`, `Jf` or the explicit other terms. For a
candidate positive-energy excitation near a stable stationary branch,
`epsilon_f>=0` is the intended interpretation. Positivity relative to that
particular branch is an additional local-stability assumption, not a
consequence of the global `0.85|Q|` floor or a proved ground-state theorem.

Equivalently, without assuming any stationary family between the endpoints,

```
D = epsilon_f + Eout - [E0(Qi)-E0(Qi-q)] + Eother.       (1)
```

If the relevant smooth stationary branch exists throughout that interval,
its constrained first law `dE0/dQ=omega0(Q)` gives

```
D = epsilon_f + Eout - integral_(Qi-q)^Qi omega0(Q) dQ + Eother.   (2)
```

Thus it is incorrect to require `Eout<=D` while also deleting positive
charge from the remnant. The stationary background pays its charge-dependent
energy difference as well. It is equally incorrect to radiate positive q
and keep `Qf=Qi` without a separate charged inflow.

## 3. What one chiral second harmonic exports

Use physical chirality sigma=+1 or -1. The parent bound quadrupole has
`|m_parent|=2`, rotating frequency Omega, and leading positive rotating
energy `K`. Its self-generated highest-weight harmonic has
`|m_out|=4`, rotating frequency `2Omega`, and lab frequency
`nu=omega+2Omega`. Its outgoing flux obeys

```
dEout = nu dq,
dKout = dEout - omega dq = 2Omega dq,
dJout = sigma 4 dq,
J_mode = sigma (2/Omega) K.
```

The chirality signs match the corrected numerical convention; no legacy
time/harmonic sign is reversed only in the outgoing field. In particular
`Jout/Eout = sigma 4/nu`, whereas `Jout/Kout = sigma 2/Omega`.
The large second ratio is not large spin per unit *laboratory* energy.

In a weak, slowly adjusting remnant, `omega` is the stationary chemical
potential at its current retained charge to leading order. Equations (1)-(2)
then reduce to

```
D approximately epsilon_f + 2 integral_0^q Omega(Qi-s) ds + Eother. (3)
```

This relation does not assume that the mode itself has zero quadratic
charge. If its perturbation contributes `delta Q_mode`, a compensating
background shift is required when comparing states at a fixed *total*
retained charge. Expanding
`E0(Qbg+delta Q_mode)=E0(Qbg)+omega delta Q_mode+...` shows why the
quadratic `K=E-omega Q` is the leading excitation energy after that shift.
The static self-mixing and background correction have not been evolved by
the outgoing linear-response calculation.

For frozen coefficients and total rotating energy k carried through this
outlet,

```
q = k/(2Omega),
Eout = [1+omega/(2Omega)] k,
Jout = sigma (2/Omega) k.
```

At Q=160000 this is `q=8.93099447 k`, `Eout=9.12288593 k` and
`|Jout|=35.72397789 k`. The background pays `omega q=8.12288593 k`;
the positive free-Psi rest energy and kinetic energy remain in `Eout`.
No negative-energy carrier is needed.

For a prescribed q and no other losses, equation (2) permits the outlet
only if `Eout-[E0(Qi)-E0(Qi-q)] <= D`; equality applies to a final
stationary, unexcited remnant. Locally this is `2Omega q<=D`. Extending
the actual range requires stationary continuation and frequencies at the
lower retained charges; two computed endpoints are not a bound on all
intermediate Omega or omega.

As a coarse independent necessary check, the exact classical floor and
`Eout>=q` imply
`q <= [Ei-0.85 Qi]/0.15`. At zero additional initial energy the earlier
pair numbers give `q<=108682.36`. This loose floor is not a predicted yield
and does not validate the frozen-frequency extrapolation below.

## 4. Full binding release is not a fixed-Q calculation

If all of the earlier gap were put through the Q=160000 frozen channel,
with zero final excitation, the accounting estimates would be

| Quantity | Frozen-snapshot value |
|---|---:|
| Rotating excitation supplied | 2978.72488096 |
| Positive charge exported | 26602.9754450 |
| Final retained charge | 133397.024555 |
| Charge fraction exported | 16.62686% |
| Laboratory energy exported | 27174.5673149 |
| Intrinsic spin exported in one chirality | 106411.901780 |

Using the matched discrete gap instead gives q=26602.291614,
Qf=133397.708386 and Eout=27173.868791. Neither is an actual evolved
solution. A 16.6% charge change is not a small-background correction, and
the uncomputed branch at Qf must not be assigned the Q=160000 rate or
frequency unchanged. The lab outflow is about 17.84% of the initial pair
energy in this estimate, rather than the stationary fixed-charge gap's
1.96%. These are different ledgers.

There is also an angular-momentum condition. If only one chirality radiates
and the final remnant is stationary and nonspinning, then

```
q = |Ji|/4,
k = Omega |Ji|/2,
D approximately Omega |Ji|/2
```

for complete relaxation through this sole frozen channel. At smaller Ji,
that channel can remove the available spin but cannot exhaust D into an
unexcited nonspinning remnant. It would otherwise over-export net spin and
leave compensating remnant spin or require an external torque.

Opposite chirality supplies an allowed *kinematic* alternative. For positive
charge emissions q+ and q- at the same nu,

```
q = q+ + q-,
Jout = 4(q+ - q-),
k = 2Omega(q+ + q-).
```

Consequently all k can leave with any net spin satisfying
`|Jout|<=2k/Omega`; the two nonnegative fluxes are
`q+/- = k/(4Omega) +/- Jout/8`. A spherical stationary background admits
opposite physical chiralities by rotational symmetry. This does not mean
the already measured single-chiral gamma can be copied into an arbitrary
mixture: coherent mixed parent modes also generate m=0 second harmonics and
different angular overlaps. Their rates and the merger's excitation weights
are uncomputed. A standing or m=0 pattern can export energy with zero net
spin only if its actual same-action outgoing overlap is nonzero.

## 5. Orbital injection and dimensionless occupation

For illustration only, take two identical fragments with rest energy
`Mfrag=E0(80000)` and small relative speed v in the COM frame, and impact
parameter b measured in `1/m` units. Then

```
mu_red = Mfrag/2,
Jorb approximately mu_red b v,
Ekin approximately mu_red v^2/2.
```

These are initial conserved orbital quantities; an interacting merger must
actually transfer some of Jorb to the chiral internal mode. Neither the
existence of the bound mode nor its positive outgoing power proves that
coupling or capture. The following choices are dimensionless examples,
not measured dwarf data or an assumed astrophysical population:

| b | v | Jorb | Ekin | K needed to export all this spin, Q160k snapshot | Parent mode action |
|---:|---:|---:|---:|---:|---:|
| 20 | 1e-4 | 76.15118 | 0.000190378 | 2.1316545 | 38.07559 |
| 20 | 1e-3 | 761.51177 | 0.01903779 | 21.316545 | 380.75589 |

Here the binding gap could energetically supply those K values if a
merger puts it into the mode; the incoming orbital kinetic energy alone
cannot. These spin-removal K values are only 0.0716% and 0.7156% of the
reference binding gap. The rest requires other excitation/radiation or
balanced chiralities. Fragment-centred internal spin is also distinct from
galaxy-centred orbital angular momentum. Moving from one to the other
requires the positional recoil term and an actual directional torque.

The canonical positive mode has action/occupation scale
`n_mode=K/Omega`; one second-harmonic Psi quantum costs two such mode
quanta in the leading rotating-energy bookkeeping. Thus
`q_out= n_mode/2` for complete frozen-coefficient decay and
`|J_mode|=2 n_mode`. Large background charge Q=160000 does not by itself
make a small perturbation highly occupied.

| Chosen Q160k K | n_mode | Total expected positive-Psi count if fully damped | Half-time, 1/m | Half-time / parent period |
|---:|---:|---:|---:|---:|
| 1 | 17.86199 | 8.93099 | 5961841.57 | 53121.55 |
| 5.59848068 | 100 | 50 | 1064903.48 | 9488.57 |
| 55.98480680 | 1000 | 500 | 106490.35 | 948.86 |

The unit-K result is not a parametrically large classical occupation.
Larger occupations can be considered as dimensionless conditional examples;
at n=1000 the full emitted charge fraction is only 0.3125%, and
`gamma K/Omega=0.0001677334`. However the maximum weak *field amplitude*
K_nl has not been established. The required simultaneous conditions are

```
Omega << K << K_nl,
K << 2Omega Qi            (small charge drift),
K << Omega/gamma          (slow damping),
K <= available excitation budget.
```

At Q160k the last two scale bounds before the budget are 17915.14 and
333772.55. They do not supply the missing K_nl bound or quantum-loop control.
At low occupation the classical PDE solution remains mathematically
defined, while interpreting its continuous decay as a physical coherent
many-quantum rate needs additional justification. No physical time can be
assigned from `1/m` without choosing a physical mass scale.

Finally `K(t)=K0/(1+gamma K0 t)` is the leading asymptotic weak-mode law;
the tabulated half-time is not a finite-time claim of complete relaxation.
The calculated single-mode scalar outlet, the required opposite-chirality
or nonspinning outlet, a merger's mode partition and remnant survival must
all be tested before using this ledger as a capture or formation mechanism.
The outer-envelope receiver and Draco/Sextans/Fornax/Leo I mass budgets
remain separate unresolved obligations.
