# KT40 scaling mechanism checkpoint

The fixed p=9/8, ell=3 kpc law screens by spatial variation of the Newtonian field, not acceleration alone. Its full curvature stress is essential. The equations and a leading Solar asymptotic proof are in [DERIVATION.md](DERIVATION.md). This explains the tested response; it does not derive the chosen parameters or provide a microscopic theory.

## Main equations

    chi=(ell/L)^(2p)(g/a0)^(2p-2), L=|g|/||H||,
    Lcrit=ell(g/a0)^(1/9) at p=9/8,
    chi_Plummer(a) proportional to M^(1/4) a^(-11/4),
    Q2 ~ (3/2)c(eta,p) a0/ell for ell/rM large.

Weak acceleration turns off curvature sensitivity very slowly: chi scales as the one-quarter power of a fixed-profile mass rescaling. The mandatory B stress further reduces the dwarf virial response in the examples below. Neither chi nor A alone is an observable prediction.

## Solar mechanism, unchanged inputs

| Quantity | Canonical | Alternate |
|---|---:|---:|
| External-field curvature crossover (pc) | 1.696720 | 1.684860 |
| Solar/external acceleration equality (pc) | 0.0245142 | 0.0245142 |
| Q2 / (a0/ell), leading coefficient | -0.158273169 | -0.152400972 |
| Predicted leading Q2 (s^-2) | -1.600387923e-31 | -1.862324397e-31 |
| Relative difference from full Solar calculation | 2.324e-08 | 2.391e-08 |
| Magnitude of A / B quadrupole | 1.745e-08 | 1.787e-08 |

Exact chi=1 roots along three directions agree with the external-field approximation to6.3e-5 relative. The physical Solar scale is about1.7pc in this diagnostic, not the formal isolated-Sun crossing near0.8kpc. The B response dominates the quadrupole. The large-lambda coefficient has an explicit convergent one-dimensional integral and an angular-cancellation/dominated-convergence derivation. The fixed-eta point-source limit is not a general mass-decoupling, Galactic-embedding or microscopic-regularization theorem.

## Dwarf mechanism at the existing Upsilon3 samples

Canonical examples, variances in (km/s)^2; these numbers reproduce the original2000-point finite-domain response.

| Object | chi at r=a | Newton variance | A variance | B variance | Total sigma | Plain sigma |
|---|---:|---:|---:|---:|---:|---:|
| Sculptor | 236.78212 | 10.97824 | 25.73908 | -11.72516 | 4.99922 | 8.53950 |
| Fornax | 31.75500 | 35.08365 | 114.15939 | -44.52075 | 10.23339 | 14.44557 |
| Leo I | 401.10028 | 27.22837 | 29.79497 | -15.03662 | 6.47972 | 10.69071 |

For Sculptor, the original lower2-sigma dispersion bound is6.4km/s, while this response gives4.9992km/s even at the sampled Upsilon3 endpoint. The B stress subtracts roughly40–50% of A in these examples. This is a finite-profile result, not a universal sign theorem. Expanded-domain checks of each separate term retain that interpretation; the largest original-domain A shift is2.71e-5 relative and the expanded-domain convergence shift is6.46e-6.

The complete table covers24 objects, both footings and Upsilon1,2,3, with four local radii per configuration:144 configurations and576 local scale/force records. It is explanatory coverage of the already accepted41-Upsilon run, not a new observational search. The reconstructed dispersions agree with the saved values to7.2e-15km/s.

## Evidence and limits

Accepted dimensional/scaling table: [run_002/results.json](run_002/results.json). Exact crossover check: [crossovers_001/results.json](crossovers_001/results.json). Separate-component convergence: [refinement_002/results.json](refinement_002/results.json). All source inputs and numerical limits are pinned in manifests. [PROVENANCE_NOTES.md](PROVENANCE_NOTES.md) preserves the initial dimensional-conversion defect and the first finite-domain convergence failure.

No MW score, baryonic density, data, empirical cut or gravity parameter was changed. Nonspherical MW support, matter dynamics, satellite external fields and a microscopic origin are separate obligations.
