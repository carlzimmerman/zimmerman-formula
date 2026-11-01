# A shared gas-fluctuation clock retains the dwarf-first ordering

This is a finite linear-response discriminator using current measured SPARC
gas forces, not the pending ng80 halo rerun or a physical assembly history.
The exact forced-epicycle model is specified before its first run in
[CONTRACT.md](CONTRACT.md). No gas coupling, clock or velocity threshold was
fitted to the desired residuals. No a0 enters the calculation.

Among 175 cached galaxies, 123 satisfy Q<=2, inclination>=30 degrees and
positive Vflat. There are 120 with a stable, bracketed point at one or more of
2,3,4 Rd. NGC3949, NGC5005 and UGC06667 have none. The three radii are reduced
to one median per galaxy, then equal-galaxy medians are taken in each bin.
The twelve shared histories use rise times 1/5/20/50 Myr and return times
100/200/500 Myr. The primary 5/200 history is inherited from CM1, not selected
after the calculation.

For `x''+kappa^2 x=F(t)`, the residual specific radial energy is exactly
`E_R=|integral_0^infinity F(t) exp(i kappa t) dt|^2/2`. For the difference of
two exponentials in the contract, this gives the analytic impulse used in the
script. The diagnostic `H=2 E_R/V^2` measures radial energy relative to circular
kinetic energy. This is residual coherent epicyclic energy; irreversible halo
heating additionally needs phase mixing or other specified dynamics. It does
not directly predict a change in cumulative halo mass.

## Primary finite result

| Vflat, km/s | n | Median H | Relative to pooled 20–100 dwarfs |
|---|---:|---:|---:|
| 20–60 | 13 | 0.01150 | 3.423 |
| 60–100 | 34 | 0.002099 | 0.625 |
| 100–150 | 23 | 0.0007797 | 0.232 |
| 150–200 | 24 | 0.0002350 | 0.0700 |
| 200–250 | 18 | 0.0001522 | 0.0453 |
| 250–400 | 9 | 0.00003359 | 0.0100 |

For all twelve predetermined histories the two target-bin/dwarf ratios are
below 0.08 (ranges 0.0607–0.0786 and 0.0432–0.0641). This implemented family
does not reverse the mass ordering. Restricting to the original force-screened
subset also retains ratios below one: primary 0.259 and 0.181. That screen is
not sufficient to certify small orbital displacements; see the retained
[post-result amendment](LINEARITY_AMENDMENT.md) and independent review.

The [independent reconstruction](../ER2_response_theory/TEMPORAL_REVIEW.md)
matches all120 galaxies and329 points to6.53e-13 relative. Its post-result
primary screen requiring both the force bound and a conservative all-time
displacement bound retains85 galaxies. The target-bin/dwarf ratios remain
0.3053 and0.1363 (22/16 target galaxies,20 dwarfs). That is a robustness audit,
not a replacement for the frozen result or a nonlinear halo calculation.

These are model/finite-population statements, not an exclusion of all gas
feedback, gas-rich formation histories or nonlinear dynamics. The perturbation
uses the full tabulated gas force; large excursions are linear extrapolations.
The unperturbed orbits are assumed circular and Vobs supplies the frequency.
The downloaded rotation models do not supply the actual fluctuation spectrum,
past gas profile or cold-field response. A mechanism with independently
different histories or spatial structure could change the ordering.

## Verification and regeneration

[run_001/results.json](run_001/results.json) retains every point, galaxy,
exclusion and timescale result. Its [v2 manifest](run_001/manifest.json) has
status **completed** and 179 declared input artifacts, unchanged before/after.
Validation passed against current input hashes. Independent Fourier quadrature
agrees to 9.3e-17 relative; a separate time-domain ODE agrees to 1.8e-9 relative.
Zero force, identical rise/return times, force reversal, exchanging times and
quadratic force scaling all pass their exact controls. Python 3.9.6, NumPy
1.26.2 and SciPy 1.11.4; one numerical thread, no random samples.

Direct scientific regeneration into a fresh directory:

```text
python3 rebuild_2026_10_22/ER2_temporal_route/temporal_response.py --output rebuild_2026_10_22/ER2_temporal_route/reproduction_NEW
```

This direct command makes the scientific result. For a new provenance record,
use the installed computation-audit runner with `computation_contract.json`,
its exact execution_artifacts list and a fresh output directory. The original
manifest records the actual runner argv and all observed hashes. The script
does not execute any command from an evidence record.

The physical distinction between rapid potential fluctuations and reversible
adiabatic response is established in [Pontzen & Governato, arXiv:1106.0499v2,
Section 3](https://arxiv.org/html/1106.0499v2). The oscillator convolution above
is derived here; it is not a transfer of their full self-gravitating simulation
result to this field. No literature novelty claim is made.
