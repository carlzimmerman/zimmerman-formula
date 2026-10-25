# CCT-011: material labels, stars and matched dwarf assembly

**The tested history has not produced a verified four-dwarf solution.** The new calculation distinguishes moving density wells from mass-current labels. Some diagnostic labels travel with the stellar probes, but Draco's label density fails a necessary consistency check. The matched Fornax/Leo I pilots terminate at a numerical angular limit, so neither their final retained mass nor absence of overboost has been demonstrated. A phase-factoring prototype supplies a concrete numerical next step, not a new physical source or a completed mechanism.

This is the selectively coupled continuous CCT wave candidate, with eta1500 pc km/s. It is not literal v3s/AeST/Khronon or retired SCT-M, and it does not establish that nature's cold component is a nonparticle field. Eta, supply and the incoming history remain postulates.

## Material flow and stars: new finite test

Replayed the exact source-free Draco/Sextans fields from t120 to130. Sampled512 mass-weighted diagnostic labels inside the selected radius-Rstar core and512 independent whole-cloud labels. Advected them with j/rho from a spline reconstruction of the wave, including absorber weight loss. The two label groups overlap and estimate different integrals; their weights must not be summed as additional physical mass. They never enter Poisson's equation. Evolved the same128 passive stellar probes as CCT010 in the full nonspherical cold potential plus the rigid baryonic background.

| Measured endpoint quantity | Draco | Sextans |
|---|---:|---:|
| Interval | 12.40 Myr | 52.96 Myr |
| Initial tagged aperture mass | 4.12 million Msun | 6.41 million Msun |
| Diagnostic tag fraction remaining within Rstar of stars | 58.40% | 65.23% |
| Tagged COM / stellar COM separation | 20.28 pc | 29.25 pc |
| Estimated tagged mass near stars | 2.406 million Msun | 4.182 million Msun |
| **Actual total field mass** in the same stellar aperture | **1.982 million Msun** | **5.416 million Msun** |
| Conditional reference mass in that aperture | 11.615 million Msun | 8.623 million Msun |

The actual mass is the angular-cap integral of the finite field density, using the evolved stellar centre. References remain the earlier conditional profiles, not measured global cold-mass floors. The same CCT010 profile diagnostics remain deficient: Draco's spherical equilibrium diagnostic is about7.13km/s versus9.55 observed; Sextans' canonical isotropic actual-position survey diagnostic remains2DeltaNLL63.63 above its previous conditional reference. Those are equilibrium/monopole diagnostics, not a fit of the evolved stellar DF.

The label COM is closer to the stars than the tracked well/aperture COM was. **That is an improvement in the diagnostic, not validated material survival.** Draco's tag estimate is21.4% larger than the entire cold field mass in that aperture. A positive material subset cannot exceed the total. The excess is4.73 nominal sampling standard errors, but that number excludes quadrature, interpolation and finite-generator errors and is not a statistical exclusion. Sextans passes this necessary domination inequality; that alone does not validate its material transport.

Tag timesteps were halved. Endpoint retained fractions agree for both galaxies. Median final tag-position differences are5.7e-5pc /0.0030pc; Sextans has an individual19.2pc discrepancy. Whole-cloud radial CDF errors remain about3.3–3.4%, comparable to initial sampling errors. This global agreement does **not** test the tiny Draco core accurately enough. No low-density threshold events or outer-domain censors were recorded. Labels count spatial overlap over a short interval, not binding to a permanent remnant or survival for a galaxy's lifetime. Stars are circular passive cohorts, not the observed live DF, and do not backreact on the cold field.

## Why current labels can disagree with the field

The finite solver evolves P(Phi psi), not the unprojected local product Phi psi. Its angular potential step obeys

    rho_t + div j = S_P,
    S_P = (2/eta) Im[psi* P(Phi psi)],

before the absorber and radial-discretization corrections. Integral S_P vanishes by Hermiticity, but the local source does not. Therefore good global mass/energy/Jz ledgers do not certify local material transport with j/rho alone. The saved endpoints have about2.7–2.9% relative angular potential residual norm. Endpoint absolute local source rates inside the selected apertures are roughly1.3–1.4% of core mass per code time for Draco and0.33–0.48% for Sextans. These are not integrated error estimates, and the whole21% Draco mismatch is not attributed uniquely to this one term.

The source formula was checked against the pointwise density derivative. A product-complete angular fixture eliminates the local source to1.31e-15, while its smaller projection has a nonzero source. Free boosted/spreading Gaussian velocities and trajectories pass independent analytic checks. This identifies a concrete finite-generator obstruction, not a physical no-go for a continuum wave mechanism. See MECHANISM_AUDIT.md.

## Same assembly prescription for Fornax and Leo I

Used the same physical eta, catchment5.364*200*Mformed, initial scaleRstar, angular seed and local escape-reference10km/s pulse as the Draco/Sextans family, with no gas. This local reference is **not** an independently paid far-field capture history. Physical parameters were not fitted to make either galaxy pass.

Their shorter wavelengths need more radial resolution. Fornax nr8192 misses the independent initial phase-gradient kinetic reference by3.13%; nr16384 reduces that to0.79%. Leo I nr4096 gives0.77%. This preflight does not certify later-time radial resolution.

Both L8,|m|<=4 pilots reached the5% edge-occupancy stop: code t0.5 for Fornax and1.25 for Leo I. First L12,|m|<=8 attempts also stopped, but their incoming waves had been recomputed on different angular grids. That changed the initial fields substantially despite a small energy difference. Those runs are retained as **unmatched initial-condition controls**, not clean convergence evidence.

The definitive larger-basis repeats copy the smaller run's **exact initial field**, padding new modes with zero:

| Fixed-initial larger-basis pilot | Fornax | Leo I |
|---|---:|---:|
| Radial nodes | 16384 | 4096 |
| Angular cuts | L12,|m|<=8 | L12,|m|<=8 |
| Requested endpoint | t130 | t130 |
| Actual stop | t1.25 | t4.0 |
| Physical elapsed time | 1.83 Myr | 2.58 Myr |
| Fraction at |m|=8 at the stop | 11.59% | 6.67% |
| Relative energy-ledger residual | 0.114% | 0.0853% |
| Reported producer RSS | 793 MB | 261 MB |

The initial fields match exactly after padding; initial energies differ only at roundoff. At the last common lower-basis times, normalized radial-CDF differences are2.20e-7 /5.83e-7. Nevertheless, larger angular support is rapidly populated and those runs still stop. **No trusted late remnant or final no-overboost result exists.** Last-snapshot spherical gravity diagnostics are55/77km/s versus observed12.1/9.29, but these are unresolved early pre-stellar snapshots, not late-time stellar predictions or physical exclusions. Export might change them later; that later evolution was not resolved.

The edge threshold is an exploratory numerical gate, not an amended original physical criterion. All six pilots and the initial-phase failures remain in the record. The highest reported RSS among the earlier attempts was987MB; the final in-place Green/chunking implementation reduced Fornax to793MB. RSS is sampled before terminal field serialization, so it is not a certificate from an external hard memory monitor. No shared heavy job was started, restarted or duplicated.

## A concrete numerical advance: phase factoring

The short incoming carrier costs many radial nodes without by itself representing new density structure. The exact substitution psi=A exp(iS/eta) separates that carrier from the amplitude; density and physical momentum are reconstructed with the carrier included. The equation and gravity bookkeeping are derived in MECHANISM_AUDIT.md and checked symbolically.

Implemented and executed a **1D periodic, mean-subtracted Poisson toy**, with an integer constant-gradient carrier. Its factored64-node amplitude reproduces a direct1024-node high-carrier calculation to2.40e-10 relative amplitude error; mass and momentum residuals are below3e-14. The deliberately unresolved direct64-node carrier fails the physical-momentum check. The factored128-node control also agrees. This is an implemented, audited numerical prototype, not a3D variable-phase galaxy solver or a solution of counterstreaming/caustics. See phase_benchmark_001/result.json and its v2 manifest.

## What the next calculation must establish

1. Implement a locally conservative, density-equivariant transport representation, resolving both radial phase and generated angular modes. Validate the core itself with a positive-subset mass bound, not only whole-cloud CDF or M/E/Jz. Carry linear momentum and absorber recoil consistently.
2. Benchmark a variable-phase extension against resolved original waves, including crossing streams and a self-gravitating translated remnant, before using the phase-factoring prototype to reduce the radial cost. It does not automatically solve angular dynamics.
3. Include live stellar backreaction and the same gravity action in the cold evolution. Tags add no force; cold density is sourced once; baryon-only Xi is not reapplied to cold mass. Current passive probes are a scoped approximation.
4. Complete one independently specified supply/energy/angular-spectrum history for all four dwarfs. Require profiles at actual survey coverage, stellar survival, retained and escaped mass, and conserved energy/spin transport. CCT008 stationary occupations may not be reset by hand into a pure coherent history.

The positive-subset bound already says that no relabeling of the measured Draco/Sextans snapshots can turn their insufficient central field mass into the chosen reference profiles. It does not exclude future inflow, another assembly history, another admissible profile, or a different underlying action.

## Evidence and reproduction

Sources, raw initial/final fields, labels, stellar positions, six stopped assembly pilots, unmatched controls, failed implications and input hashes are preserved. Twelve timed producer runs have manually reconciled v2 records under run_manifests/; the first Fornax preflight did not record UTC/software and is retained explicitly as untimed. Producer runtimes are internal timed intervals, and raw git revisions were sampled at output creation. Missing observations were not invented. The final audit authenticates saved dynamics; it does not rerun them. The phase toy has its own fresh bounded-runner execution record. See ASSEMBLY_PROTOCOL.md, MATERIAL_PROTOCOL.md, run_record_index.json and the final audit manifest.

Prior audited packets and frozen criteria are unchanged. No automation, external publication or messages to other chats were made. Repository pushing is explicitly authorized by the user; the commit/push result is reported only after verification.
