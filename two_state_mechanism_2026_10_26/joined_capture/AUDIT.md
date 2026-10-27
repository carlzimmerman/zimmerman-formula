# Computation audit

Outcome: finite signed mapping, Hermitian operators and frozen-electronic
nonlocal benchmark verified within numerical tolerances. Full physical rates
remain unresolved; neutral electronic-basis convergence fails the tested refinements.

## Contract and evidence

The executed domain is R=2,3,4 for the capture map; three nuclear collision
energies -.62,-.60,-.58; mu=50; 130,192,266 electronic states; fixed molecular
axis. Initial fourth-order runs retain the changing inner endpoint as diagnostic
history. Corrected-wall runs compare h=.05,.025,.0125, wall=.2,.1,.05, and exterior
R=30,40. The largest electronic basis is tested at h=.025 only; it is not claimed
independently mesh-converged. There are 13 neutral nuclear runs, 27 map/kernel
cases, six BO ionic grids, two nonlocal incident energies, and independent
operator/event tests. See per-run contracts and the aggregate `run_audit` table.

The generic launcher assertion text is broader than the ionic-threshold run's
actual operation; `run_ion.py`, its recorded argv, scope and results explicitly
identify the scalar BO calculation. It does not execute neutral scattering.
The aggregate interpretation here and in DERIVATION.md supplies that narrower
claim; provenance completion alone is not physical validation.

## Signed map

CONGEN excitation signs and Molden symmetry/orbital labels determine the map.
Elementwise reconstructed Q Hamiltonians match at R2 to 2.74e-9 and at R3/4 to
better than 8e-12. Exact old-Q embeddings into the augmented spaces have maximum
isometry error below 1.24e-12. All 27 transferred electronic kernels satisfy the
optical identity. Only the old 42-dimensional Q space was transferred; this does
not converge the old continuum representation or supply entrance phase transport.

## Nuclear convergence at E=-.60

| Test | Ground-to-other neutral probability |
|---|---:|
| 130 states, h=.05, wall=.2, Rmax30 | 1.0776724032e-6 |
| 130 states, h=.025, wall=.2, Rmax30 | 1.0860376854e-6 |
| 130 states, h=.0125, wall=.2, Rmax30 | 1.0871662269e-6 |
| 130 states, h=.025, wall=.1, Rmax30 | 1.1081650296e-6 |
| 130 states, h=.025, wall=.05, Rmax30 | 1.1084371496e-6 |
| 130 states, h=.025, wall=.2, Rmax40 | 1.1140860784e-6 |
| 192 states, h=.05, wall=.2, Rmax30 | 6.0127255984e-6 |
| 192 states, h=.025, wall=.2, Rmax30 | 6.0992890256e-6 |
| 266 states, h=.025, wall=.2, Rmax30 | 6.9794940533e-6 |

The mesh correction helps. The last mesh change in the 130-state sequence is
0.104%, while the 192-to-266-state change is 14.43%. At E=-.58 that basis change
is about 72.12%; at -.62 it is only about 0.0131%. Convergence at one energy
cannot certify the energy-dependent collision rate. Outer matching still shifts
the middle-energy result 2.58%. No fit or type-dependent choice is introduced to
remove these discrepancies. These quantities concern incident neutral modes;
no recombination rate or atomic product branching follows from them.

## Nuclear thresholds and source/escape join

At h=.025, the old-basis BO ionic bound energies are approximately
[-.579067609,-.543793890,-.518949836,-.503745215]. The diffuse-basis values are
[-.579219986,-.544018654,-.519091617,-.503808610]. Both have one open bound
vibrational channel at incident .001 and two at .05. At .199, ionic dissociation
opens and a bound-only model is incomplete. The scalar BO calculation omits
DBOC, finite-mass polarization and rotational corrections.

The frozen-electronic benchmark uses the old-basis thresholds consistently with
the old actual H_QP/H_PP at R2. Optical relative residuals for open sectors are
below 2.65e-15; closed-sector absolute residuals below 4.88e-15. Nuclear threshold
restriction is explicit. Copying the v0 width into four vibrational blocks gives
relative width-operator errors sqrt(3) and 1.06759 at the two incident energies.
Those numbers measure this specified approximation, not error bars on physical DR.

The first nonlocal run reported relative error 1 for zero-width closed sectors
because roundoff was divided by roundoff. The v2 scripts report their absolute
error, retain the original record, and leave the physical matrices unchanged.

## Independent checks and conservation

A two-sector direct inverse agrees with Schur elimination to 1.38e-16.
Effective-channel unitarity residual is 1.12e-16. The free fourth-order dispersion
error decreases by factors 15.96 and 15.99 under mesh halving, consistent with
fourth order. The signed-event ledger has zero tested charge/constituent residual
and energy residual 1.39e-17. These are operator and ledger checks, not a physical
photon trajectory. The stationary optical identity accounts for flux at common
total energy; it does not establish omitted-channel accuracy.

## Provenance and non-claims

All new NPZ arrays are small and published; aggregate inputs hash them. The
Molden inputs are checked against their earlier recorded files. Raw CONGEN inputs
are retained. Original scripts and their contracts are immutable. New versions
record changes separately. `manifest_validation.json` reports validation of every
new manifest against current inputs; execution success and provenance validity
are distinct from scientific convergence.

No nuclear P overlap across R, geometry-dependent global P resolvent, nuclear
product flux, DR thermal coefficients, inverse physical rates, excited-product
branching, new physical photon trajectory, live-gravity disk formation, galaxy
population separation, or galaxy acceleration relation result is established.
