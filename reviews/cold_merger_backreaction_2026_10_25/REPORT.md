# Autonomous encounter driving, finite energy supply, and retention

## Outcome

A conservative encounter model generates its own density drive and transfers
orbital energy to the existing scalar. A narrow resonance amplifies a tiny seed
by about 38,771 in the optimized test, but the field returns close to its initial
energy by the sampled end of 100 orbital periods. This is a demonstrated exchange
mechanism, not a predicted retained cold reservoir. The final tiny net transfer
is close enough to numerical ledger errors that its precise value is not a
physical result; the large transient peak is well resolved.

A second calculation exposes a retention problem: the candidate's bulk scalar
mass is larger inside dense clusters. At the 35 existing gas-shell benchmarks,
a locally at-rest excitation has an open propagation channel to the exterior
unless the Einstein lapse falls inward by a very large factor. In a fixed-lapse
WKB picture, escaping excitations become relativistic. This is an escape-channel
test, not a computed escape fraction or a proof against all bound interface modes.

The requested full result remains open. We have not derived real cluster merger
initial conditions, an irreversible retention process, a galaxy-safe force law,
or the microscopic constants. The new calculation replaces the arbitrary
sinusoid with a self-consistent **reduced** orbital coordinate; it must not be
advertised as a self-consistent cosmological or hydrodynamical merger simulation.

## 1. Fixed action and dynamical source

Continue 2e20ebd591 without changing r=1, s=1/4 or eta=1500 pc km/s. In canonical
Einstein units the excitation potential is

    Vex(q,d)=W(q)/D-2+d[A(q)-1], A=sec(q/2),
    W/D=[1+(4 sin²(q/2)-1)²]/cos⁴(q/2).

Let X be a signed separation coordinate for a rigid spherical density profile
passing the sampled field cell. Adopt a density/potential pair of the form

    d(X)=40+16(1+X²)^(-5/2),
    Uorb(X)=-B/sqrt(1+X²), M=B T².

The profile exponent follows from the Laplacian of the softened inverse-radius
potential, whose density is proportional to (1+X²)^(-5/2). However the cell volume,
profile size, baryonic mass and orbit are not independently calibrated here.
B and T specify a reduced experiment; this is not a parameter-free mapping from
the observed clusters. The source background and peak are deliberately the same
scale as the previous oscillator control. A translated rigid profile omits tidal
deformation, gas shocks, pressure and hydrodynamic mixing.

Use the autonomous Hamiltonian

    H = qdot²/2 + Vex(q,d(X)) + M Xdot²/2 + Uorb(X).

Its equations are

    qddot = -partial_q Vex,
    M Xddot = -Uorb'(X)-d'(X)[A(q)-1].

The last term is essential: it is the force on the matter coordinate associated
with field excitation. Thus

    d Efield/dtau = d'(X) Xdot [A-1],
    d Eorb/dtau   = -d'(X) Xdot [A-1],
    dH/dtau=0.

No external driver replenishes lost orbital energy. This Hamiltonian is a
consistent two-coordinate reduction; deriving it with calibrated coefficients
from the full matter-field action remains a distinct missing step.

## 2. Reservoir bound and finite tests

Set B=1e-4 in D energy-density units as an illustrative nonrelativistic mechanical
budget. Start at the orbital turning point X=sqrt(24), Xdot=0, giving Eorb=-B/5.
Start the scalar at q=1e-6, qdot=0. Both are declared initial data, not derived
cosmological conditions. There is no fitted efficiency. The uncoupled orbital
period is 51.96478496 T; the density repeats twice per orbit because d is even.

Since Uorb>=-B and orbital kinetic energy is nonnegative, the exact energy bound is

    Efield <= H+B = 8.0000004e-5 D

for this seed and orbit. With zero seed the classical field remains exactly zero.
The same formula applies to arbitrary amplitudes on the physical scalar branch;
changing initial orbital energy or B changes the available reservoir. This is
why a dynamically generated driver does not by itself select cold abundance.

Six initial controls T=.03,.1,.3,1,3,10 were evolved for 30 uncoupled orbital
periods, each at two tolerances. Their final field energies remain approximately
3.69–4.24e-12 D, compared with 4.00064e-12 D initially. These six points do not
exclude narrow resonances. Tiny orbital losses in the coarse runs are sometimes
smaller than their total-energy error and are not interpreted as measured transfer.

A larger-seed q=.01 control verifies non-negligible backreaction: its field loses
8.1693e-5 D and the orbit gains the same energy, within a total-energy error of
5.1e-14 D. Flipping the feedback-force sign breaks conservation by 1.4696e-4 D
and fails the intentional mutation test. This larger seed is a numerical control,
not an allowed production claim from an initially empty cold sector.

## 3. Resonance search in the orbit-generated spectrum

After the six-point test, an explicitly adaptive scan evaluated the linear
scalar monodromy over the density period for 161 logarithmically spaced T values
from .01 to 2. The orbit itself solves X_ss=-X/(1+X²)^(3/2), with s=tau/T.
Its half-period endpoint and the scalar monodromy determinant are checked.

The largest sampled amplitude multiplier is 1.12343106 per density period at
T=0.465850694. This T is an optimized mathematical control, **not** a cluster
prediction or a new fitted physical constant. It only establishes that the
orbital profile genuinely contains a resonant drive. The finite grid neither
locates every band nor finds a rigorous global maximum.

The full coupled equations at this T, evolved for 100 uncoupled orbital periods,
give:

| Quantity | Coarse tolerance | Tight tolerance |
|---|---:|---:|
| Peak field excitation / D | 1.54753e-7 | 1.55108e-7 |
| Final field excitation / D | 3.96462e-12 | 4.02407e-12 |
| Maximum total-energy error / D | 6.23e-13 | 8.40e-15 |

The resolved peak agrees within about 0.23% and is roughly 38,771 times the seed,
yet remains below 0.2% of the finite reservoir bound. The field subsequently
returns nearly all of that excitation. We do not claim the small final excess is
converged or that every later time returns to the seed. This is one finite
conservative trajectory, not an infinite-time no-retention theorem.

The density waveform is no longer prescribed, but the model still lacks outgoing
spatial modes, dissipative gas physics and a derived irreversible transfer channel.
Stopping the run at its peak, introducing a damping coefficient, or selecting a
special encounter phase would not establish the requested abundance prediction.

In physical units, T/omega_unit is about 6.08 days and the density repetition
period about 158 days, using the inherited mass dictionary. Efficient coupling
comes from the narrow central passage and its harmonics, not simply matching the
fundamental orbital period to twice the scalar frequency. No observed cluster
orbit with these scales has been supplied. The earlier crossing proxies are
.148–1.085 Gyr. Transplanting the optimized waveform to those macroscopic times
would destroy the demonstrated spectral matching; it cannot be done by silently
rescaling the scalar mass or eta.

## 4. Bulk retention is a separate gate

For small excitations around the restored q=0 phase,

    omega_in²/omega_unit²=(d-8)/4,
    omega_out²/omega_unit²=5.76

in the exterior broken vacuum. A slowly varying background gives an effective
position-dependent particle mass. In a static Einstein-frame metric with lapse
N, a locally at-rest excitation at the production point has conserved Killing
energy proportional to N_in omega_in. The exterior continuum opens at
N_out omega_out. A subthreshold excitation therefore requires

    N_in/N_out < omega_out/omega_in = sqrt[23.04/(d-8)].

Evaluate this using the earlier 35 shell-averaged gas densities at H_J=1.8e-18/s:

| Retention / escape diagnostic | Range |
|---|---:|
| Required lapse ratio below | 0.11529–0.65350 |
| Required logarithmic lapse depth | 0.42541–2.16029 |
| Outgoing v/c at equal lapse | 0.75693–0.99333 |
| Single-excitation energy loss fraction to exterior mass threshold | 0.34650–0.88471 |

The inherited sigma=vc speed proxies give v²/c²=5.293e-06–2.5e-05,
far smaller than the order-unity logarithmic lapse depths above. This comparison uses weak-field
cluster intuition/proxies, not a solved lapse in the Palatini candidate. If
its full backreaction instead creates such large metric changes, its compatibility
with observed cluster gravity and the galaxy law must be demonstrated afresh.
The conformal change of mass units cannot remove the conserved Killing-energy
condition; Einstein lapse and Einstein masses must be compared consistently.

At equal lapse, an outward WKB ray can convert its decreasing rest energy into
kinetic energy. The displayed speeds follow from gamma_out=omega_in/omega_out.
They are not predicted measured particle velocities, and do not include reflection,
angular momentum, self-gravity, nonlinear scattering or time-dependent trapping.
The energy-loss fraction refers to keeping the same excitation while making it
subthreshold; real-field interactions need not conserve particle number.

The previous interface study found possible localized low-frequency modes in
idealized walls. They are not contradicted here: their frequency can lie below
the exterior threshold and their interior tail is evanescent. A mechanism must
populate them and show that their location and stress reproduce the interior
cluster profile. All present gas-shell averages exceed the restoration threshold
8, so they supply no resolved transition wall within the tested annulus. Averages
do not rule out local voids, clumping or additional walls. No trapped fraction,
escape time, wall population or nonlinear soliton stability has been calculated.

## 5. Energy supply and galaxy preservation

Orbital damping by scalar radiation could help an encounter merge while sending
energy out of the cluster. That process is not automatically production of a
retained cold mass. One must show both a positive transfer and a confinement or
conversion channel that retains the needed stress-energy.

The earlier integrated gas-kinetic proxies are only 1.55e-6–3.90e-6 of the required
cold rest energy in the 28 complete profile alternatives. They are not a bound
on every reservoir or gravitational assembly history. They do show why a new
large rest-energy component cannot be claimed from an unbudgeted macroscopic
mechanical drive. The present Hamiltonian enforces this bookkeeping rather than
supplying free energy. It does not compute energy extraction from a live vacuum.

No galaxy law has been proven in this Palatini candidate. In the separate spherical
selective-CCT bookkeeping, any additional enclosed cold mass must still obey
M_c<=delta [B_g+sqrt(B_g²+4 A_g B_g)]/2, where A_g=a0 r²/G, B_g=M_b(<r) and delta
is an observational allowance. No allowance or new threshold was chosen. The
encounter mechanism has no derived switch that prevents analogous excitation
or force changes in galaxies. A broad claim of galaxy preservation is therefore
unsupported even if a cluster transfer channel succeeds.

## Evidence, limits, and continuation

Normal, mutation and adaptive-scan runs have separate bounded manifests and
frozen scopes. check.py and scan.py preserve all initial data and numerical
controls. The mutation fails at the expected energy test. Numerical results are
finite and self-reviewed; the exact Hamiltonian energy identity and reservoir
bound do not rely on a finite scan. There is no external theorem or new empirical
merger dataset underlying these controls.

Reproduce from the repository root in fresh output directories:

    python reviews/cold_merger_backreaction_2026_10_25/check.py --output /tmp/cold-merger-check
    python reviews/cold_merger_backreaction_2026_10_25/scan.py --output /tmp/cold-merger-scan

The genuine remaining route is spatial, backreacting matter-field evolution
with independently justified initial conditions and a demonstrated bound final
state. Candidate continuations are emission into interface modes or nonlinear
self-bound configurations; neither is excluded by the bulk WKB test, and neither
is presently derived or populated at the required abundance. They require an
energy-conserving coupling and profile calculation, rather than an arbitrary
friction, conversion efficiency or selected merger schedule. This checkpoint
leaves those routes open and does not report the user's full goal as achieved.
