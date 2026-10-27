# Self-audit of the state-preparation checkpoint

Primary verdict for the original galaxy claim: **incomplete, with the smallest
missing implication being a microscopic collective electric response and its
physical preparation/inventory mapping**. No disk/dwarf/cluster success is
claimed. This is self-review, not an independent referee report.
Exact reviewed source hashes are in AUDITED_HASHES.json; inputs derive from
checkpoint fd502a8f56846535ea2126b2ef667b1f1e005fdf plus this new stage.

## Dependency and obligation checks

| Claim | Evidence and verdict | Limits |
|---|---|---|
| Quadratic unitary dynamics preserves mode covariance eigenvalues | Direct commutator/Bloch-length proof; passed under blockwise quadratic assumptions | Does not prohibit interactions or subsystem cooling |
| Diagonal polarization upper bound | Cauchy-Schwarz at fixed final Hamiltonian; passed | Not a bound on arbitrary instantaneous polarization |
| Controlled preparation reaches small source remainder | 17 midpoint runs plus 4 independent ODE runs; computationally verified in recorded range | Protocol, band, filling and initial temperature are supplied |
| Energy/work accounting | Exact discrete quench/rotation identity, checked against continuous-work integration | Exact ledger is not by itself a temporal convergence test |
| Actual finite-time average | Exact final-H precession integral; multiple mode resolutions and tolerances | Finite averaging, not irreversible thermalization or live feedback |
| Contact-channel ordered gap | Differentiate the displayed free energy; numerical independent minimization at 9 couplings | Thermodynamic mean-field model, not exact many-body phase |
| Interaction response and unique unbroken root | p'<=1 gives monotonic inverse for lambda<1; expansion checked by direct substitution | The field-coupled and transverse-order channels are distinct models |
| Static acceleration diagnostic | 101-point lambda grid, bounded chi optimization, 4001-point dense check | No global optimum proof, data fit or derived constants |
| Autonomous energy conservation | Differentiate H and cancel coordinate/field/precession terms; eight runs | Homogeneous, fixed D, no spatial gravity or countercharge transport |
| Local current + Fermi mass incompatibility | Algebraic elimination, phase-space volume and 16 finite cases | Only same fundamental local nonrelativistic fermionic units |
| Independent vacuum emission gate | Standard rate with explicit rationalized-unit conversion and approximation cap | Not collective radiation or a general cooling bound |
| Spin-liquid literature transfer | Exact source locators and operator/symmetry checks recorded separately | No verified 3D dark-medium implementation |

## Numerical distinctions that matter

1. The small source remainder is the observable compared throughout. Reporting
   only relative polarization error would conceal large force errors.
2. Midpoint angular preparation at N=768, dt=.05 gives relative diagonal source
   error0.003937746697. Independent DOP853 gives0.003937746858 at N=1536. At
   N=768, tightening rtol1e-9 to1e-11 preserves that diagonal value. Continuous
   work residuals are below1e-13. The fixed-field hold [1000,2000] gives error
   0.003926532302 at N=1536, versus0.003925322957 at N=768. This is evidence for
   the stated finite average, not an instantaneous asymptotic theorem.
3. Initial instantaneous polarization comparisons at96/192 modes were not
   converged. The separate ODE hold check resolves the final instantaneous source
   error at768/1536 modes to about -0.00298703. The diagonal statistic must not be
   relabeled as a measured instantaneous response.
4. The autonomous I=100 trajectory was not mode-converged at32/64 modes. At
   128/256 modes, final m agrees within5e-13, last-fifth mean E within3.1e-12,
   and RMS m within2e-13. The tighter same-N DOP853/RK45 comparison isolates ODE
   tolerance from mode quadrature. I=1 and10000 remain finite illustrative runs,
   not a fully converged inertia phase diagram.
5. The autonomous reference uses the continuum cold constitutive curve. Finite
   quadrature gives a tiny reference mismatch at32 modes; convergence at128/256
   supports the reported8.122631 energy excess. It is not claimed that a closed
   mixed-state orbit can actually reach a pure ground state.
6. Static-fit error is log10[g_model/g_simple(g_b,model)], NOT horizontal baryonic
   acceleration error. The baseline is reoptimized on the SAME1e-4..1e4 range.
   Some fixed-lambda optimizations hit the upper susceptibility bound and are
   explicitly marked boundary-limited. Medium gravity and inner countercharge
   are absent from this conditional spherical diagnostic.
7. The joint mass bound distinguishes constituent m_+, total unit mass M and
   effective band parameters. It does not confuse an emergent band's effective
   mass with the rest mass sourcing gravity. The envelope p<=M*c is an explicit
   generous nonrelativistic assumption, not a consequence of relativistic v<c.
8. The radiative mass examples are hypothetical independent emitters, not
   candidates that also pass the joint band/inventory bounds. The one-transition
   criterion and all-dark-mass inventory are deliberately optimistic.

## Provenance and failure handling

All8 manifests freshly validate against the current inputs. Seven record
completed runs. `run_combined` records an output-directory typo in the command,
not a failed assertion or physical counterexample. Its stderr and failed status
are retained. The corrected invocation `run_combined_v2` ran unchanged scientific
inputs successfully. Valid provenance of a failed run is not successful evidence.
Successful run stderr files are empty. The generated figure was visually checked.
No pinned source was modified after its recorded successful run.

## What remains open

The local fundamental-fermion construction is rejected under the displayed
hypotheses. Emergent quasiparticles are outside that rejection, but require a
new constitutive/mass/current mapping and a physical electric operator. Spatial
energy export, initial state formation, countercharge transport, common scales,
live3D gravity, lensing and population separation have not been demonstrated.
Do not identify magnetic field with galaxy rotation or use an imposed protocol
as a galaxy classifier. This checkpoint narrows viable constructions; it does
not establish a new dark-matter theory.
