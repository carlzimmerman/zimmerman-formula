# Cold-shell cosmology diagnostic — completed bounded continuation

**Outcome:** an independently specified pressureless Newtonian reference passes
the exact homogeneous-expansion benchmark, then develops central focusing under
the prescribed Plummer baryon ramp after **0.0399623282449 Gyr** from z=10
(z=9.40336590312). This survives inclusion of homogeneous baryons and Lambda,
exact enclosed cold mass, and removal of artificial central absorption. It is
**not** a corrected DT2 charge evolution, a validation of its old event times,
or a theory-closure result. No EFE, retained halo mass, or settled radius follows.

The contract and analytical benchmark were written before execution in
[CONTRACT.md](CONTRACT.md). The independent equations are implemented in
[cold_shells.py](cold_shells.py), without importing DT2. Only this new directory
was edited for this continuation; original source bytes were snapshotted.

## Confirmed issues in the earlier DT2 stencil

The inspected source is pinned in [sources/dt2_form.py](sources/dt2_form.py),
SHA-256 `098e1906c919886e82370a43098d551a01faed04dae22e05f80d6f90aa084b9c`.
This avoids ambiguity from simultaneous documentation edits in the live source.

1. Its force includes cold mass and the central baryon source, but not the
   homogeneous baryons or Lambda used in H(a): source lines31–33,55–56,98–111.
   The homogeneous acceleration coefficient should be
   `-Omega_m H0^2/(2a^3)+Omega_Lambda H0^2`, whereas the continuum cold-only
   force supplies `-Omega_c H0^2/(2a^3)` before stencil errors.
2. `Fv[0]=v_half[0]` at line130 assigns the first cell-center velocity to the
   inner face. Even at zero timestep, v=H r_center gives the wrong inner-face
   velocity H r_center instead of H F0. The relative error is **3.06922% at
   N=130** and **1.49774% at N=260**. Uniform velocity interpolation at interior
   faces does not repair that boundary error. Homology is not exact.
3. `cumsum(dm)-dm/2+Mcen` at line108 is not exact uniform-volume enclosed mass
   at the volume-weighted radius in line103. It also omits the cold inner ball,
   since M_cen initially vanishes (line91). With density rho, the exact mass at
   a radius r_j in cell [F_j,F_(j+1)] is
   `M_inner + sum(previous dm) + 4pi*rho*(r_j^3-F_j^3)/3`.
   At the first center, the old/exact mass ratio is **.0875531 at N=130** and
   **.0438326 at N=260**. The missing homogeneous ball inside1kpc contains
   **197081.1076 Msun**. Restoring that ball alone leaves the half-cell
   discretization error **.0852212%** and **.0213508%**, respectively.

The old first event is a chosen **.5kpc inner-face cutoff**, not automatically
a shell crossing (source lines82–83,134–142). Changing these details can change
its time and meaning. The earlier corrected reduced-code events near .13–.15Gyr
are therefore not converged estimates of this new central-limit event.

## Independent reference and benchmark

Use physical cold shells, exact conserved initial enclosed mass, uniform
Omega_b=.05, Lambda=.69, Omega_c=.26, H0=70km/s/Mpc, z_i=10. The initial physical
shell labels are1..2000kpc. A separate smooth xi->0 limit represents the central
uniform core. Its regularized equation reaches the true central density
singularity, rather than stopping at an arbitrary finite radius. It adds no
point mass, absorbs no shell, and stops at first focusing.

The Plummer excess is `10^10.45 Msun * min(t/1Gyr,1)` with1kpc softening, the same
central source inputs as the earlier driver. This is externally prescribed
injection above the homogeneous baryons, not a derived mass-conserving baryonic
assembly history. The reference has no pressure or polarization and no a0;
canonical and alternative a0 footings would therefore be identical here.

The exact homogeneous proof is in CONTRACT.md: with no central source,
`u=r/r_initial=a/a_initial` solves the equations and initial data. The numerical
run reaches z=0 after12.8856802067Gyr, with maximum relative errors:

| Quantity | Maximum error |
|---|---:|
| finite-shell radius divided by exact a/a_i | 5.619e-13 |
| central-limit radius scale | 7.900e-13 |
| finite-shell velocity | 1.337e-12 |
| independent physical-time u comparison, absolute | 4.707e-12 |

All velocities remain positive, including the early epoch with negative
acceleration. **Inward acceleration alone is not collapse.**

The regularization also passes an independent analytic radial freefall test:
from rest with no external force, `t_focus=pi/(2sqrt(2A))=1.1795082168834938Gyr`;
the candidate RHS gives1.1795082168834927Gyr (relative error8.882e-16).

## Centrally forced result and error controls

Accepted strict runs:

| Run | N | rtol/atol | focus time, Gyr | max constraint residual |
|---|---:|---:|---:|---:|
| central_130_strict |130|2e-12/1e-14|.03996232824486856|8.203e-9|
| central_260_strict |260|2e-13/1e-15|.03996232824488185|5.461e-9|

The constraint is `2w^2-A-E s^2=0` for u_center=s^2 and dt/dtau=s^2. Its
predeclared maximum acceptance threshold remained2e-7. The initial loose
`central_130` run **failed** that threshold and is preserved with its failed
manifest and traceback. It emitted no accepted results/trajectory. Tightening
the tolerance, without changing equations or thresholds, produced the accepted
runs. The intermediate `central_260` run also passed and is retained.

The strict focus-time difference is1.329e-14Gyr. This is a repeatability check,
not a physical error bar. **N counts independent shell samples** of an exact
enclosed-mass ODE; the central-limit marker is independent of that spatial grid.
The focus convergence is principally a time-tolerance/regularization check,
not convergence of a spatial PDE. All production calculations took less than
.1s inside the numerical driver; the runner imposed55 CPU/60 wall seconds.

At the accepted fine-grid event:

- Central-limit turnaround occurred at.00477387970593Gyr.
- The initially1kpc finite shell turned around at.00804673444548Gyr, having
  first expanded to1.007793711925kpc. At central focusing it is at
  **.567971698246kpc**, moving inward at **36.1153365131kpc/Gyr**.
- Only3.99623282449% of the final prescribed central baryon mass is on.
- No finite-radius shell crossing precedes the central focus. CONTRACT.md gives
  the analytical shell-order argument for this Plummer model; all sampled
  normalized finite-shell gaps are positive as an additional numerical check.
- Minimum sampled finite-cell density is **1125.956521758 times today's cold
  mean**, and the central-limit minimum is **1312.684417534**. Initial Hubble
  expansion does dilute the matter below its initial1331. These sampled densities
  stay above216 and26, but that does not derive equivalence to any DT2 branch.
- The independent physical-time force implementation agrees to1.989e-13 in u
  and6.423e-12/Gyr in u_dot across the recorded finite shells and times.

The central marker represents an infinitesimal uniform core: its first focusing
is not a claim that a finite retained mass has already formed a galaxy. The
first finite shell has not reached the origin. There is no post-caustic
continuation or present-day settled halo in these outputs.

## What this resolves and what remains missing

The benchmark and original failing witnesses establish that the old background
discretization was not exact, and show that a central forcing event need not
disappear when those background problems are removed. The new pressureless
reference develops genuine central focusing. It does **not** establish that the
old cutoff event was physical, nor that the nonlinear DT2 model has this event.

A faithful DT2 implementation needs a derived continuity equation and spatial
current for the conserved charge `N=rho_d+div P`, along with its coupled momentum,
polarization and metric equations and boundary conditions. Advecting rho_d as
fixed material shell mass is generally different from advecting N; fixing
Friedmann sources or face interpolation cannot supply the missing current.
The earlier asserted favorable-bracket/strong-gradient rationale is not a
proof that its rho_d shell evolution preserves the full theory's characteristic
flow or caustics. One must derive when any reduced current becomes rho_d*v and
control the omitted terms on the actual trajectory. This reference assumes a
separate pressureless material, so it makes no such identification.

An EFE-dependent effective gravitational mass is likewise not a conserved cold
mass by definition. Neither this calculation nor the earlier static EFE solver
provides the conversion/transport law needed for the proposed combined route.
The next discriminating theory step is that explicit current and its reduction,
followed by the homogeneous benchmark on the **derived** system. A late-time
settling or retention simulation before this step would add an unproved model.

## Reproduction and provenance

Observed base HEAD: `2ffc012fa56dcdcbb4b3d5f169ba757fe482bcb8`; source snapshots
and hashes are in[source_provenance.json](source_provenance.json). Exact argv,
software versions, resource caps, dirty status, hashes before/after and elapsed
times are in each run's v2 manifest. Raw sampled trajectories are compressed NPZ
files beside accepted results. Use fresh output directories for reproduction.

Commands (relative to repository root; replace output names with fresh paths):

```bash
python3 research_closure_2026_11_12/combined_route/cosmology_diagnostic/cold_shells.py --n 130 --output NEW_HOMOGENEOUS
python3 research_closure_2026_11_12/combined_route/cosmology_diagnostic/cold_shells.py --n 130 --central --rtol 2e-12 --atol 1e-14 --output NEW_CENTRAL_130
python3 research_closure_2026_11_12/combined_route/cosmology_diagnostic/cold_shells.py --n 260 --central --rtol 2e-13 --atol 1e-15 --output NEW_CENTRAL_260
python3 research_closure_2026_11_12/combined_route/cosmology_diagnostic/regression_checks.py --output NEW_REGRESSION.json
```

Actual bounded invocations are recorded in[run_commands.txt](run_commands.txt).
All six manifests validate against current inputs: five completed, one preserved
failed computation. The16 checks in[regression/results.json](regression/results.json)
pass, including direct witnesses that reject all three original background
errors. [verification.json](verification.json) records validator output.
[artifact_hashes.json](artifact_hashes.json) records final artifact hashes.

**Evidence classification:** finite implementation and numerical assertions
verified within the stated tolerances, supported by exact homogeneous,
regularization and shell-order arguments. Equivalence to DT2/v3 remains
unestablished; theoretical closure remains open.
