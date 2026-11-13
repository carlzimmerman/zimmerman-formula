# Low-mu continuation: corrected growth, independent background obstruction

The imported mu>=25120/Mpc growth line is not a valid bound for the full polarization-constrained equations. Replacing its acoustic Jeans equation changes the result. Nevertheless, lowering mu to the background-coldness value near 198/Mpc does not rescue either proposed repair on the unchanged homogeneous, source-free clock history: the exact conserved inventory violates the repository's separate specified BBN radiation budget by about two billion times. This obstruction does not depend on a new lensing fit or on the disputed Jeans line.

This result is conditional on the same H(Q,0)=mu²(Q-1)²/(2K) branch and present cold inventory extending through the specified early epoch. It does not exclude an explicitly changed early-time action, source, stress sector or cosmological history. Neither of the studied repairs supplies such a change.

## What changed physically

The full leading conserved density is n=H_Q+Pi. Eliminating the linear polarization gives

```text
delta x = K delta n/[mu²+(k/a)²],
delta_d_ddot+2H delta_d_dot
  = K rho_b delta_b + K nbar mu²/[mu²+(k/a)²] delta_d,
delta_b_ddot+2H delta_b_dot = K(rho_b delta_b+nbar delta_d).
```

The old QX3 code instead uses the isolated-polytrope dark factor `1-(k/(a mu))²`. It can become negative; the corrected factor remains positive. Its mu_J was read into MK1 and PIK1 rather than rederived. See `DERIVATION.md` for the complete scale-factor derivation and precise historical file/line references. Frozen files and outputs are retained unmodified; snapshots are pinned in `sources/index.json`.

## Controlled growth result

All numbers below are total-density **power ratios** to the infinite-mu reference with identical initial data. This is a gamma=0 smooth-endpoint, pressureless-baryon, post-recombination calculation with radiation in the expansion background. The canonical KD1 parameters are h=.6740779913, Omega_b=.0492057631, Omega_d=.2661642311, Omega_r=.00009196275. Initial equal-species growing data use the exact smooth-radiation Meszaros derivative. There is no primordial transfer fit or observational exclusion threshold attached to this table.

| Comoving scale | mu=198.254, z1090 to z3 | mu=25118.864, z1090 to z3 | mu=198.254, reset at z100 to z3 |
|---|---:|---:|---:|
| k=0.2h/Mpc | .839708 | .999987 | .998022 |
| k=1/Mpc | .226380 | .999263 | .906806 |
| k=3h/Mpc | .122690 | .996999 | .732492 |
| k=20/3 Mpc^-1 | .045857 | .968908 | .327836 |
| wavelength 0.42/h Mpc | .033641 | .933199 | .234619 |

The scale labels come from the existing MK1/DT2/QX3 diagnostics; no new data threshold is invented. The last row corresponds to k=2pi h/.42=10.08418/Mpc, which is different from 3h/Mpc. The late-start column resets all pre-z100 suppression and therefore cannot substitute for a full primordial transfer. Baryon-zero catchup initial conditions, z10 and z0 outputs, and both canonical/alt parameter sets are included in the raw results. The z1090 equal-data half-power diagnostic at z3 lies between k=.35655 and .37768/Mpc, not an observationally fitted cutoff.

Small-scale growth remains materially reduced at low mu, even after the old acoustic equation is corrected. These finite ratios do not by themselves establish a replacement PR4 or forest bound. `classy` is unavailable in the current environment, and the historical likelihood equation is inapplicable to this model, so no CMB/Boltzmann claim is inferred from the run.

## The independent exact background result

The exact homogeneous current and energy give

```text
a³n=constant,
rho=n+K n²/(2mu²),
rho_stiff/rho_r = Omega_d I0/[4mu² Omega_r a²].
```

Both repairs retain H(Q,0)=F(Q), so they retain these identities. The early stiff term is exact even where the cold approximation fails. KD1's frozen B1b criterion specifies T=.1MeV, a=2.3486541750e-9 under its temperature convention, and rho_stiff/rho_r<=.067. Re-evaluating that exact declared criterion gives:

| Canonical mu [Mpc^-1] | Stiff/radiation at the specified epoch | Criterion |
|---|---:|---|
| 198.2542324 | 134,723,849.17 | fails |
| 25,118.86432 | 8,392.46266 | fails |
| 8,890,113.535 | .067 | boundary |

The alternate footing gives mu_BBN=8,889,273.437/Mpc. These reproduce the historical KD1 numbers to floating precision. The .067 line is a **declared historical criterion**, approximately Delta N_eff=.5 at that epoch under the frozen post-annihilation convention; this is not a newly measured BBN likelihood or a recomputed thermal network. The stiff component is not a constant Delta N_eff throughout BBN. Its exact assumptions and temperature-convention limitation are stated in `DERIVATION.md`.

For low mu, an early charge inventory at most 2.23005e-5 of today's would be needed to meet the same budget. Conservation fixes the homogeneous comoving inventory; neither late redistribution nor a static EFE boundary creates the missing global charge. Thus the low-mu escape is closed within the stated unchanged-FRW source-free history. Merely replacing 25120 with 198 does not supply a cosmologically admissible repair in that history.

## Checks and provenance

`run_001/manifest.json` is a validated canonical v2 record with status **completed**. `run_001/results.json` has 21 passing checks. The independent fixed-step midpoint solver agrees with DOP853 to 1.823e-6 relative, improves by a factor 4 on halving the step, and tighter DOP853 tolerance changes results by 4.35e-12. Separate checks reproduce EdS growth, the exact smooth-radiation Meszaros solution, the pure-dark high-k freezing limit, and the coupled high-k baryon-feedback eigenmode. Mutating away the scale factor or reinstating the old acoustic source changes the result strongly. Both footings reproduce the exact background normalization and historical BBN bounds.

The maximum cold offset in the main low-mu run is xbar=.000666882, and the smallest sampled initial k/(aH) is 28.15. Solver convergence does not certify the neglected radiation perturbations, baryon thermal effects, recombination initial transfer or full relativistic corrections. The literal one-sided original gamma switch is also outside a unique linear Fourier Hessian at Pi=0; this run is the explicitly specified gamma=0 reference.

HY4 independently read the raw executable and checked the state ordering, Hubble drag, source coefficients, unsuppressed baryon forcing of the clock, separate midpoint matrix, and BBN normalization against its own FRW reduction. No sign/factor error was found. This review explicitly retained the initial-transfer, gamma-switch and frozen-BBN-proxy qualifications above; it is not a proof of a complete cosmology.

The preserved source bytes, executable, contract, raw curves and raw table are local to this lane. No original criteria, historical outputs, or other agent's lane was edited. See `RUN_COMMAND.md` for the exact bounded command.
