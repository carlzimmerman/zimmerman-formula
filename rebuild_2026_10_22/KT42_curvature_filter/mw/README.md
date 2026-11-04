# MW: small curvature smoothing preserves the bad force

The full curvature-only filtered action retains KT39's outward force at small
Gaussian widths. At R=12kpc,z=.3kpc, the two fixed witnesses require smoothing
of order100pc to reverse the force at that point. That does not repair the
whole sampled profile: at100pc an outward band remains at z=.32–.56kpc
(canonical) or .32–.57kpc (alternate). At300pc every sampled point on that
particular R12 profile is restoring, but this is not a global galaxy claim.

The refined values below use spatial refinement5 and128 implicit heat steps;
the filter tends to a Gaussian, not a fixed finite-power resolvent law.
Potential derivative units are (km/s)^2/kpc; a negative derivative gives
outward physical acceleration above the midplane.

| a [pc] | canonical dPhi/dz at R12,z.3 | alternate | primary cuts, both feet |
|---:|---:|---:|---|
| 0 | -840.50685 | -932.47021 | pass |
| 1 | -840.38123 | -932.32867 | pass |
| 10 | -827.74667 | -918.07604 | pass |
| 30 | -718.15432 | -795.04743 | pass |
| 100 | 112.79893 | 119.43424 | pass; outward band remains elsewhere |
| 300 | 274.95817 | 286.40257 | pass |
| 1000 | 542.57669 | 576.00056 | fail K0 |

Every sampled case still fails the inherited strict scale-length Lh cut. The
earlier four primary cuts alone are therefore insufficient to establish a
usable galaxy solution. At300pc the unchanged uniform-external-field Solar
test fails by7.88/9.06 times its ceiling; the fixed Draco diagnostic still has
negative virial. No jointly acceptable new case is demonstrated.

## Full action and numerical controls

`filtered_model.py` implements g=G_h psi, Hbar=H_h T_h psi,
T_h=(I-a^2 Delta_h/(2m))^(-m), and the exact composite adjoint
T_h* H_h*. The gradient stays unfiltered. The finite energy derivative is
checked directly; the outer filter is not a postprocessing force prescription.
The inherited gradient/Hessian and Laplacian use cell-volume weights.

- checks_003: weighted-adjoint error1.60e-15, zero-width reproduction1.29e-16,
  energy derivative best relative error1.28e-11. Full response reciprocity
  passes at the best declared step (3.71e-7); the smaller step has larger
  floating cancellation error and is not concealed.
- Independent scalar Gaussian benchmark: maximum error at m32 is.002377
  of peak for a1kpc, declining to.000641 at m128. This is a numerical
  approximation, not an exactly Gaussian finite matrix.
- scan_001:18 fixed-witness cases, nine widths, refinement3/m32.
- heat_refine_001 separates heat refinement m32→128 at fixed spatial grid.
  Maximum R12,z.3 relative change is below5%; the sign is unchanged.
- refine_001:14 cases at refinement5/m128. Comparisons to refinement3/m128
  change that force by less than2%, preserving primary scores' pass/fail.
- domain_001 halves the inner radius and doubles the outer radius at a1,
  100,300pc. Force changes are at most4.15e-5 relative.
- Independent potential differences at three steps agree in sign for all
  refined selected points, with best relative disagreement below.002.
- Root verification regrades48 stored MW scores and checks7152 profilepoints.
  These are observed convergence errors, not certified continuum bounds.

The separate `pass_population/` lane evaluates all52 historical KT39 primary
passes at a = 0, 0.1, and 1 pc. All156 forces are outward; all468 potential differences
agree in sign. This removes the two-witness selection issue within that
selection. It is not a full1375-cell scan of the new action, and no monotonic
or interval argument certifies unsampled widths.

## Preserved failures and reproducibility

The first launch request used an absolute output path, which the runner
rejected before execution. `checks_001_contract.json` remains; no manifest or
physics run exists for it. The launcher was corrected before checks_002.

checks_002 is a valid failed record: the coarse m16 Gaussian approximation
missed the declared.004 benchmark gate. Its immutable code and manifest
remain. `calculate_v2.py` tests m32,64,128 against the same gate; checks_003
passes. No physical cutoff or observational threshold was relaxed.

Each experiment has its prospective contract, exact arguments, unchanged
input hashes, bounded runtime and a manifest. Use `launch_v2.py NEW_NAME --
--mode checks` or `--mode scan --refine ... --steps ... --widths ...` to
regenerate into a fresh directory. Do not overwrite the accepted runs. The
root `verification_001/` validates all13 pre-planet manifests, including the
three failed records elsewhere in the phase, and independently regrades the
saved results. A successful manifest means provenance/execution; the analytic
and numerical checks supply the scientific evidence.
