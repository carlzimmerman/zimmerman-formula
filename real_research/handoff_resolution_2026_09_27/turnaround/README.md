# HR01 turnaround continuation

Base `48905ae11213afcb9ff1b7726530bb5dd1933fe3`. Source lanes remain unchanged. The original global target is not achieved: kappa=1/2 remains fitted; a0=9.3603e-11/1.1312e-10, Z=5.7888. This directory completes/audits finite XR36 calculations and develops explicit frame, tidal, kinetic and conserved-source continuations.

Primary derivations:

- [Frame and action variation](FRAME_AND_VARIATION.md): exact fixed-region auxiliary-vector action, uniqueness, first-order density tide, local kinetic obstruction, shear repair with its tensor price, scalar Helmholtz-projected repair, and bootstrap seed-mass condition.
- [CMASS and conservation](CMASS_AND_CONSERVATION.md): actual HOD/projector calculation of response/source gates, finite dark-budget replacement, its infrared form factor, paired density-tide ESD, and source-mask variational reciprocity test.
- [Run status](RUN_STATUS.json): machine-readable run reconciliation, mutation differences and verified source hashes (written at final reconciliation).

The fixed-region/frame derivation is correct under its stated restrictions. The global covariant action verdict is **incomplete, with the smallest missing implication**: a differentiable region/frame prescription and independently conserved dark-field dynamics must produce the required source profile while the fully constraint-reduced fluid/metric/clock symbol remains coercive. The nonlocal scalar shear operator is a candidate constitutive class, not that completed action.

## Completed finite bound-region results

XR36 bound main finishes in 437 scientific seconds: 11/16 checks, zero load-bearing failures. Five observational/reporting gates fail. Baseline K1/K2/K3 pass; sharp local gate radius is at most .441 Mpc and R0 at most .444 Mpc around the sampled z=.25 lenses. Sharp B/D1 KiDS Delta chi-square is +972.233/+995.744 (canonical/alternate), compared with the +9 gate. The best natural ramp in the declared set still gives +44.923/+52.774. The tested width scan has no joint KiDS/Local-Group pass.

Local Group sharp R0=.388–.441 Mpc versus the source's .93±.12 target. Sharp timing masses are 1.2707953e12/1.2411204e12 solar masses, above the declared baryon window. These are conditional spherical tracer-shell results, not a general exclusion of all carrier-assisted turnaround models.

At the cluster proxy, the retained-carrier gate reaches 3.18 R200 and R0=4.28 R200; the source therefore leaves its X-COP interior MOND share unchanged. This does not rerun the XR28 outskirts likelihood, and the radial crossed-shell extent is not a derived splashback radius. The flagship/SPARC mask test gives zero deviation at all sampled points; it is not a fresh fit to the full galaxy data.

G9 external-field costs are +630.240/+663.109 for the full all-matter field and +63.600/+75.108 for the H_K1 baryonic field. The uniform-field tolerance inferred by source interpolation is 1.47885e-4/1.06923e-4 a0. The new action audit proves exact cancellation only for a uniform vector field and a fixed region; it corrects the source's blanket second-order tidal-monopole claim.

K4's declared convergence test passes narrowly, but its scope matters: R0 changes by at most 6.4e-6 relative; doubling shells moves the local switch radius .227322→.187067 Mpc (17.7%), and the KiDS score +972.233→+1069.086 (9.96%). Those changes do not rescue the failed observation but prevent a strong assertion that the entire mask geometry is numerically converged. Some ramp R0 values are NaN by design; F checks only its declared selected finite subset, not every JSON number.

## Action and constructive controls

Gate-action main exactly reproduces the existing JSON: 10/11 checks, with A4's predeclared 1-Mpc ghost-scale ceiling false; inverse pole scales are 132.224–1756.046 kpc. MUTATE adds exactly A1's density-gate static-term failure (9/11). All 24 frozen backgrounds have a negative kinetic coefficient at 1/kpc. The source's cluster Gaussian-filter minimum reaches 7.370/7.747 Mpc. Strict positive filtered kinetic symbol requires R>R_min; equality leaves a zero. Neither frozen symbols nor these background samples establish a full nonlinear continuum theorem.

Latest new computation evidence is in `runs/frame_tide_audit_scalar` (13/13), `runs/cmass_source_gate_spectral` (262/262), and `runs/density_tide_pair_verified` (4/4). Their mutations fail named trace-tide, source-mass, and zero-lens/projector controls respectively. The CMASS construction is an inherited-input central-HOD forecast with no covariance likelihood; its conserved replacement avoids additive matter double counting but does not jointly satisfy the inherited radial comparison band. Its compact density form-factor correction tends to zero as k², under the stated finite-support condition. No unchanged-growth theorem follows.

## Provenance and rerunning

`mirror_sources.json` pins copied scientific inputs; `runtime_package_hashes.json` pins locally assembled packages. The mirror has real copied files and no output symlinks. `prepare_mirror.py` made the initial snapshot; later explicitly copied dependencies are included in the hash record. The Python3.9 runtime uses NumPy1.26.2, SciPy1.11.4, SymPy1.14.0, locally rebuilt vanilla CLASS3.3.4.0 and the recorded dependency set. Original XR36 scripts are byte-identical to their source inputs.

Use `run_one.py NAME main LABEL` or `run_one.py NAME mutate LABEL` for a fresh bounded run directory. NAME is an original XR36 script or a local continuation script; LABEL must be new. The runner records actual return code, command, elapsed time, stdout/stderr, scientific JSON, source hashes before/after, and a computation-audit schema-v1 manifest. The v1 schema cannot enforce complete execution dependency provenance; the separate mirrored-input hash audit supplies a practical freshness check without claiming a sandbox. Numerical-library thread caps are cooperative.

`run_sequence.py` was the initial queue. It was paused at its parent while the completed bound child waited to be reaped, releasing the heavy slot to the collapse lane. The bound wrapper elapsed time includes this coordination pause; the scientific log records 437 seconds. Initial action attempts missed a copied dependency, and the first web attempt stopped at missing Astropy; these failed attempts are retained rather than treated as mathematical failures. Subsequent verified runs supersede them by explicit path, not by date order.

## Completed web run and control limitation

The full 128^3 web run and its mutation finished in approximately 42–43 seconds each on this runtime. Main is 10/12 checks with one load-bearing miss: the locally rebuilt CLASS baseline differs from XR26's stored numbers by at most 2.5e-7 relative, exceeding its fixed 1e-9 tolerance. This tolerance was not changed. Consequently the web result is **conditional on the numerical-library/build discrepancy**, not an exact successful baseline reproduction. XR19's eigenvalue census is bit-identical and the plane-wave operator control has maximum relative error 1.7e-10.

Within this proxy, the sharp hybrid's Planck 8–400 linear amplitudes are 1.010780/1.012997; the halofit-base values are 1.136826/1.175385, or 4.49/5.87 source-standard deviations high. H_K1 sharp hybrid's halofit values are 1.065696/1.083661; the alternate footing remains beyond the source's 2-sigma gate. ACT's approximate Planck-bin-weighted linear values are 1.017598/1.021390; corresponding nonlinear values are 1.239322/1.307101. These are proxy weights, not the ACT likelihood.

The web phantom keep fractions are .189 sharp, .477 ramp, .043 all-axes and .832 mutation. The hybrid sigma8 ratios range 1.003428–1.004258. Retaining the yield leaves the forest proxy at zero; gate alone reaches 22.5825 against the .10 criterion because 88–94% of the sampled dense absorbers are trace-turned-around while nearly all still expand along an axis. The finite web census uses the specified Zel'dovich/virialized-axis prescription; it is not a nonlinear particle-mesh evolution.

The web mutation fails the named load-bearing L1 check: amplitudes 1.108701/1.134540 on the linear base; it also turns ACT proxy L4 from pass to fail. Baseline K1 remains failed in both runs, so the control miss is distinguished from the attributable mutation. Bound mutation finishes 10/16 with exactly G1 newly failed. The original gate-action mutation likewise adds exactly A1. All three original source mains and mutations therefore executed to scientific output after resolving the recorded environment stops.

The new W3 comparison is also instructive: raising the threshold enough to include an Mb=1e11 convention-B lens at 1 Mpc would include approximately 79% of this web's mass. This rules out treating threshold broadening as an automatically isolated-galaxy repair; it remains a result about the specified shared expansion-rate mask and web realization.

The subgrid halo L3 exercise produces only 0.1–2.6% additive lensing enhancement in the printed all-matter radius brackets, rather than its pre-run expectation of at least10%. Its report-only check is not an observational acceptance test. No source expectation is promoted to a result when the output disagrees.

## Recommendation disposition and exact handoff

| Requested continuation | Disposition |
|---|---|
| Finish XR36 gate action, bound regions and web | All mains and mutations executed; strict web K1 drift explicitly retained |
| Specify and vary free-fall-frame action | Fixed-region action and uniqueness supplied; moving boundaries/mergers remain |
| Separate uniform-field removal from tides | First-order trace-tide correction derived; exact paired flux/ESD test executed |
| KiDS with web field | Original G9 completed, fails; removing uniform field does not remove density tides |
| Local Group and ramp-width pincer | Original timing/R0 and width scan completed, fail the tested joint requirements |
| Cluster outskirts | Original interior-radius proxy completed; full XR28 outskirts score belongs to the coordinated reproduction lane |
| CMASS | New conditional HOD/source-mask and conserved-replacement projections executed; no measured covariance available |
| Source gate keeps exterior phantom | Verified static mass retention; additive budget fails; capped replacement and conservation-current condition derived |
| Well-posed continuation | Local shear and scalar Helmholtz shear principal symbols derived and checked; full metric/fluid/clock/region proof absent |
| Late-web continuation | Compact conserved replacement has verified k² density-form-factor suppression; dynamic CMB lensing remains open |
| Expensive band-pass PM box | No XR36 full-action/joint-gate survivor established; do not infer that the new static replacement already authorizes/justifies that box |

The next executable research target is the conserved dark replacement coupled to the scalar-projected kinetic completion: formulate the independent dark stress/current, derive its exchange and boundary conditions, and compute the complete linear constraint-reduced symbol before nonlinear evolution. The existing static budget cap and O(k²) form factor are inputs to that target, not a proof that it is realizable. Original lanes, frozen registrations and external publications were not modified.
