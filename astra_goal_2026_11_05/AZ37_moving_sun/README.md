# NO VERDICT — selected moving-Sun prediction

Lane5(c), criteria80a14d9d9c. Kappa = 1/2 FITTED; not theory closed.
The v3s action admits an exact conditional GR/geodesic branch, but the
tested incoming flows develop downstream focusing and the Galactic
charged-background matching is unsolved. Static Solar predictions cannot
be transferred unchanged merely by citing AS3's alpha_1 result.

## Results

- **Exact branch:** P=0, Q=1 and a geodesic hypersurface-orthogonal khronon
  make every extra action term's value and first variation vanish. The
  metric is GR on this branch, with alpha_1=alpha_2=0 relative to its own G.
  This is a branch-existence statement conditional on a smooth congruence,
  not a determination of the actual Galactic initial/boundary conditions.
- **Incoming flow:** all eight velocity/impact-parameter cases focus on
  the downstream axis; the calculation is repeated on each footing.
  Minimum periapsis is0.0080533AU, above the illustrative solar radius.
  Maximum coarse/fine relative change is2.47e-9 against1e-5; maximum scaled
  energy drift is1.68e-10 against1e-7. The caustic concerns the congruence,
  not the GR metric, and is not a proof that every moving v3s solution fails.
- **Charged response:** all72 finite-time Fourier cells per footing pass
  their ODE and convolution checks. Phase speeds span753.5–938.4m/s
  canonical and851.6–916.9m/s alt, below the assumed220/369km/s source
  speeds. Resonant direction cosines are0.00204–0.00427 and0.00230–0.00417.
  The finite-time resonant response is regular; the stationary transfer
  has a pole. This defeats a uniform static-to-moving transfer assumption.

The largest |rho_tau/rho_source| in the declared short-time test is
5.384e-15 canonical and6.191e-15 alt. These are Fourier-density response
estimates for zero initial perturbations at one/ten crossing times. They
are not alpha_1, a measured force, a long-time bound or a full Solar solution.

## Controls, inputs and precision

`branch_and_flow.py`: main87/87, exit0. The flat-congruence mutant passes
69/103, exit1; it fails Q=1/geodesic consistency plus every focusing and
Schwarzschild-energy gate. Its straight-ray known answer and convergence
checks pass. Different check counts include the mutant's extra flat-ray
control. `response.py`:36/36, exit0; maximum ODE pair change5.32e-12 against
1e-7, maximum50-digit convolution difference1.55e-46. This invariant
subtest is retained in both output trees; the global mutation already bites.

The two a0 footings are recorded separately. The GR branch's geodesics do
not depend on a0, an exact property rather than a pooled fit. Lengths are
the inherited FITTED CQ7 endpoints/center. Galactic densities0.0447/0.0514
Msun/pc³ and x_e1.15/2.6 are provisional H4 background transcriptions, not
fresh profile solves. Velocities and impact parameters are declared test
assumptions; v3s does not fix the Galactic khronon rest frame. No observational
preferred-frame bound is newly graded.

Main flow took under0.4s, mutant under6s, response under1s, each single
threaded and below100MB RSS. Inputs and software versions are hashed/recorded
in the JSON. No tolerance changes, downloads, historical-lane edits or
post-result amendments were needed.

## Reproduce and continue

From the repository root:

```sh
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ37_moving_sun/branch_and_flow.py
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ37_moving_sun/branch_and_flow.py --mutate
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ37_moving_sun/response.py
```

Expected exits0,1,0. See `DERIVATION.md` for exact formulas and self-review.
The remaining obligation is nonlinear moving-source matching to Galactic
polarization, including downstream regularity and the physical metric
response. The next scheduled lane checks the solar interior assumption.
