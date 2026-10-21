# Signed finite-volume face transport in the actual-pair runs

**The in-phase collision transports energy and positive Noether charge
outward across R=20, 30 and 40 through the action's actual interior face
currents.** This is stronger than an inventory outside an aperture. It
does not identify all of that transport as free radiation, prove a bound
remnant, or establish escape from the full box or a galaxy.

This audit advances no field. `face_flux.py` reads the four completed
in-phase, half-time-step, finer-space-grid and antiphase snapshot sets.
The v2 bounded audit has **524 passing checks**, validated current input
hashes, measured RSS 245,448,704 bytes and numerical runtime 1.75 seconds.
All four original evolution manifests also validate as completed against
their current inputs. No mode-reference or Newton solve enters this audit.
The exact records are in `face_flux_run_001/` and `sources_face_flux.json`.

## 1. Exact semi-discrete flux for the recorded energy allocation

The solver stores real fields `(Psi_re,Psi_im,X_re,X_im,chi)` and their
ordinary time derivatives on cell-centred cylindrical finite volumes. For
spacing h in both coordinates,

```
w_i = 2pi R_i h^2,
C_ij = w_i L_ij = w_j L_ji,
C_radial = 2pi R_face,     C_axial = 2pi R_i,
fac_a = (1,1,1,1,1/2).
```

Here L is the exact v2 discrete Laplacian. An interior link contributes
`fac_a C_ij (q_ai-q_aj)^2` to the total gradient energy. Half is allocated
to each adjacent cell, matching v2's positive face-energy diagnostic:

```
e_i = w_i [sum_a fac_a v_ai^2 + V(q_i)]
      + (1/2) sum_(j adjacent,a) fac_a C_ij (q_ai-q_aj)^2.
```

Fixed Dirichlet boundary faces have their corresponding half-cell term;
all three audit apertures lie strictly inside the box. The continuous-time
FV equations imply the exact interior identity

```
de_i/dt = -sum_j F^E_(i->j),
F^E_(i->j) = sum_a fac_a C_ij (q_ai-q_aj)(v_ai+v_aj).
```

For complex fields this is

```
F^E_(i->j) = C_ij Re[(Psi_i-Psi_j)* (Psi_dot_i+Psi_dot_j)
                    +(X_i-X_j)* (X_dot_i+X_dot_j)]
             +(C_ij/2)(chi_i-chi_j)(chi_dot_i+chi_dot_j),
```

where the star means complex conjugation. The sign is outward from i to j.
For example a positive-frequency outward travelling Psi phase has both
positive energy and charge flux and `F^E/F^Q=nu`.

The cell charge and its exact current are

```
Q_i = w_i [2 Im(Psi_i* Psi_dot_i)+4 Im(X_i* X_dot_i)],
dQ_i/dt = -sum_j F^Q_(i->j),
F^Q_(i->j) = -2 C_ij Im(Psi_i* Psi_j)
             -4 C_ij Im(X_i* X_j).
```

The g interaction exchanges charge between Psi and X locally; the total
weighted U(1) charge has no local source. A species-only charge ledger
would need that conversion term.

For a cell mask M the outward power is the sum of each oriented link
current multiplied by `M_i-M_j`. Masks are `R_i^2+z_i^2 < radius^2`.
Thus these are exact currents through a voxel spherical control volume,
not interpolated samples on a geometrically smooth sphere.

The code independently differentiates the local energy and charge using
the full five-field acceleration and potential gradient, rather than
checking only a divergence against itself. Maximum normalized instantaneous
continuity residuals are about 1.1e-12. Reconstructed box E/Q and R20 E/Q
agree with the original logs to the declared relative 1e-10 threshold.
These are semi-discrete identities; kick-drift-kick still has its recorded
finite-time-step energy error.

## 2. Measured transport, t=0 to 240

All values are dimensionless action units. “Drop” is initial minus final
cell-mask inventory. “Flux” is the trapezoidal integral of signed face
currents from the 13 snapshots at t=0,20,...,240.

| Case | Radius | E drop | Integral E flux | Q drop | Integral Q flux | Net flux E/Q |
|---|---:|---:|---:|---:|---:|---:|
| in phase | 20 | 21013.936 | 20499.988 | 20205.605 | 19673.731 | 1.04200 |
| in phase | 30 | 18415.127 | 18118.764 | 17473.249 | 17192.882 | 1.05385 |
| in phase | 40 | 11658.943 | 11489.212 | 10854.336 | 10711.476 | 1.07261 |
| half dt | 20 | 21013.671 | 20500.104 | 20205.690 | 19673.772 | 1.04200 |
| half dt | 30 | 18414.790 | 18118.825 | 17473.262 | 17192.903 | 1.05385 |
| half dt | 40 | 11658.524 | 11489.183 | 10854.271 | 10711.414 | 1.07261 |
| finer dx | 20 | 21540.797 | 21097.501 | 20722.875 | 20265.337 | 1.04106 |
| finer dx | 30 | 18795.022 | 18494.870 | 17844.766 | 17565.339 | 1.05292 |
| finer dx | 40 | 11999.083 | 11882.733 | 11184.687 | 11078.078 | 1.07263 |
| antiphase | 20 | 103565.442 | 102642.853 | 108942.134 | 107972.809 | 0.95064 |
| antiphase | 30 | 506.524 | 573.254 | 452.189 | 507.592 | 1.12936 |
| antiphase | 40 | 49.153 | 48.276 | 46.291 | 45.795 | 1.05418 |

For the base in-phase case at R30, the positive and negative E face
integrals are +18149.914 and -31.150. At R40 they are +11492.089 and
-2.877. There is real predominantly outward transport through these larger
surfaces, rather than merely an arbitrary reallocation of a local gradient
energy. The signed Q integrals show the same direction. The complete
positive/negative splits and snapshot time series are retained in JSON.

In the fixed late window t=120...240, base in-phase R30 still carries
integrated net E=17060.632 and Q=16256.887, with E inward contribution
-29.711. R40 carries E=11256.854 and Q=10516.511. No assumption that the
retained core is already stationary is needed for those flux measurements.

## 3. Sampling, refinements and antiphase interpretation

The snapshot-flux quadrature is not exact. For the in-phase base run the
whole-window E/Q reconstruction discrepancies are 2.45%/2.63% at R20,
1.61%/1.60% at R30, and 1.46%/1.32% at R40. The finer spatial run gives
2.06%/2.21%, 1.60%/1.57%, and 0.97%/0.95%. The missing integration
information cannot be recovered from snapshots spaced by 20; recording
the currents every evolution diagnostic or step is the direct next check.
There was no assumption or pass gate that these quadrature errors vanish.

Halving the evolution dt changes the whole-window in-phase face integrals
by less than 6e-6 relative at each radius. Refining dx from 0.75 to 0.5
raises those integrals by about 2.1–3.4%, including changes of the voxel
boundary. These two grids do not supply a continuum error theorem.

The antiphase control is essential: an enormous R20 inventory drop can
coexist with very little transport through R40. Its R20 net transported
E/Q is about 0.951, consistent with transport of bound fragment material
being different from an isolated positive-charge free-Psi radiation
stream. The audit does not classify each crossing excitation. In
particular aperture crossing alone must not be called radiative cooling.
At antiphase R30 the small net signal has a 13.2% E and 12.3% Q
snapshot-quadrature discrepancy; that relative accuracy limitation remains
visible rather than being hidden by the much larger R20 signal.

## 4. What is established and what remains open

The calculation establishes finite-grid outward transport of the same
action's E and conserved Q in the prepared dimensionless in-phase pair,
with useful time/space refinement checks and explicit inward components.
The initial total Q is the actual logged value, about 160485.927 for
that pair, rather than an assumed exact nominal 160000. Charge exported
through a surface reduces its retained inventory; no fixed-Q remnant
assumption is used.

The aggregate E/Q ratios are not a spectrum, a proof of a particular
second-harmonic mode, or a separation of coherent waves from intact
outgoing fragments and near fields. The region's lab-energy loss can
include energy carried with the lost charge and is not all stationary
fixed-charge binding release. A matched stationary lower-Q reference and
late-time morphology remain separate requirements.

The full box has reflecting fixed boundaries and conserves its contents;
crossing R40 does not mean leaving that box permanently. Larger boxes,
longer times, higher-cadence currents and an appropriate outgoing-state
classification are needed for an escape or final-capture statement.
These axisymmetric head-on cases have zero total angular momentum. They
test neither a nonzero-impact-parameter torque nor galaxy-centred angular
momentum export, physical dwarf velocities, an outer-envelope receiver,
or the four dwarf mass budgets.
