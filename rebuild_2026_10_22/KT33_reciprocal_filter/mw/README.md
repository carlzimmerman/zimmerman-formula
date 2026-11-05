# KT33 Milky Way: fixed-width reciprocal completion

This lane tests the fixed-width diagnostic requested in
`reviews/repo_audit_2026_11_03/NEXT_STEP.md`. Original research files are read-only.
The parameters, baryon profiles, priors, simple-nu law, and observational cuts
remain those of KT25. Canonical and alternative footings remain separate.
The experiment is not blind: KT25's nine saved canonical and thirty saved
alternative candidates were known before this rerun.

The reciprocal completion has **0/1,375 passing cells in each footing** at
both original and doubled spatial resolution. Every corrected cell fails the
Ou rotation-curve cut. The full production run completes in 159.66 seconds.

| Production result | Canonical | Alternative |
|---|---:|---:|
| All four cuts | 0/1,375 | 0/1,375 |
| Maximum circular speed, km/s | 217.554890 | 221.854768 |
| Minimum Ou chi-square (ceiling 59.892500) | 183.076924 | 76.848184 |
| K(R0) at that best cell, Msun/pc² | 69.208001 | 70.610559 |
| Vertical chi-square at that best cell | 37.179578 | 36.199962 |
| Strict scale-length passes, whole grid | 0 | 0 |

The best corrected cell in both footings is BV2 with Sigma_b=53.9 Msun/pc²,
M_bb=2.12e10 Msun, R_d=2.6 kpc, h_thin=0.25 kpc, h_thick=0.72 kpc,
thick share 0.35 and R_d,thick=2.0 kpc. Its widths remain 5.4739473917272
and 4.977859602739685 kpc, respectively. Three-times spatial resolution moves
its Ou chi-square to 183.415023 and 77.012479, respectively. The failures
remain well outside the cuts.

All nine saved canonical and thirty saved alternative candidates also lose
their all-four-cut passes. The source-only discrete-energy control has
8/1,375 canonical and 82/1,375 alternative passes at production resolution,
versus 9 and 83 at the initial resolution. Original KT25 reports 9 and 78.
These small source-only count shifts expose the narrow original margins and
are kept separate from the large effect of the outer filter. In the new
source-only production control there are four alternative share-0.12 passes;
there are no canonical ones. No such source-only pass is a corrected pass.

The completed scan evaluates every one of the original **1,375 in-prior cells
per footing**, without parameter fitting. `grid_refined_run/results.json` is
the production result (twice the original radial and angular resolution,
even harmonics through degree 48); `grid_run/results.json` is the initial
coarser, degree-24 diagnostic. `saved_run/results.json` retains all 39 saved
candidate comparisons, including independently reproduced original-source-only
results and plain-QUMOND controls. The first lower-resolution validation failure
is preserved, not erased; its diagnosis is below.

## Equation and discrete adjoint

For each cell, hold its KT25 width fixed during variations:

    Phi = N rho + S* Phi_ph[S rho]
    xi = exp(round(log(0.5 sqrt(Gk (Mstar+Mgas)/a0k))/0.005)*0.005).

The constants and logarithmic quantization are copied literally from KT25.
`Mgas = 11910967635.394314 Msun`. No corrected force was used to refit epsilon,
the scale, the stellar distribution, or any observational line.

Let W be the diagonal matrix of the inherited spherical finite-volume cell
volumes, L its Poisson matrix, and G=(Crr,Cth) its cell gradient. L is
W-self-adjoint. The nonlinear phantom field is computed as

    p = L^-1 (4 pi S rho)
    A = (nu(|Gp|)-1) Gp
    Phi_ph = -L^-1 W^-1 G^T W A.

This is the derivative of the discrete reduced energy
`-(1/(4 pi)) sum_i W_i Psi(|Gp_i|)`, with
`Psi'(q)=(nu(q)-1)q`. Its linear response is symmetric under W before and after
the outer adjoint. The inherited UX5 face-flux QUMOND code reconstructs
tangential gradients but omits their transpose contributions, so merely wrapping
that old finite operator with a Gaussian would not establish an exact discrete
energy gradient. It is retained as a legacy control, rather than silently
equated to this discretization. Both approximate the same continuum QUMOND law.

The isotropic three-dimensional Gaussian is represented in axisymmetry by even
Legendre harmonics, with the azimuth and negative-z reflection included. Radial
quadrature weights are `(r_hi^3-r_lo^3)/3`; angular weights are
`cos(theta_lo)-cos(theta_hi)`. Weighted QR produces an orthonormal angular basis
whose constant mode is exactly one. The symmetric radial kernel for degree l is

    4 pi/(2 pi xi^2)^(3/2) exp[-(r-r')^2/(2 xi^2)]
      * sqrt(pi/(2a)) ive(l+1/2,a),    a=rr'/xi^2.

The raw operator H is W-self-adjoint. Numerical column normalization uses
`d=H 1`, `S=H diag(1/d)`, and **`S*=diag(1/d) H = W^-1 S^T W`**. This preserves
source mass and maps a constant potential to the same constant exactly in exact
arithmetic. S and S* are not conflated. The normalization correction is a
finite-quadrature/boundary convention, not a refitted physical scale.

H acts on the inner sphere out to 120 kpc, and the exterior block is identity.
The source is not cut off or renormalized by its total mass. This finite-domain
approximation is explicitly checked with filter radii 80 and 180 kpc. Neither
a coordinate-wise R,z Gaussian nor a filter lacking the cylindrical Jacobian is
used. Finite harmonic projection can produce minute negative-density tails;
no clipping is applied because that would break linearity and the adjoint.

## Exterior potential, limits, and force components

The Poisson domain initially extends to 18,000 kpc. The cell-gradient transpose
includes its boundary terms; it produces an exterior compensating phantom sheet
in this finite energy. The isolated MOND phantom potential has a logarithmic
asymptote and no preferred zero at infinity. Its arbitrary additive constant
does not contaminate the outer force because `S*1=1`. The same radial lattice
was extended beyond twice its original outer radius: best-cell circular speeds
move by less than `3e-11 km/s`, and Ou chi-square by less than `6e-10`.
The earlier `outer2` test regenerates the logarithmic lattice and mixes boundary
and spacing effects; the same-lattice result is the cleaner boundary check.

`nu=1` yields zero phantom potential exactly. `xi=0` gives the identity filter
and the ordinary QUMOND discrete energy implementation exactly. The latter
converges to the legacy plain-QUMOND calculation: on the original best cells,
the circular-speed discrepancy drops from about 0.09--0.10 km/s at the original
grid to 0.023--0.025 at twice resolution and 0.010--0.011 at three times.

Every score includes the complete vector gradient. In particular
`g_z/a0 = cos(theta) d_r Phi - sin(theta) (1/r) d_theta Phi`; neither term is
discarded. All 43 vertical-force points and all 37 Ou circular-speed points
are stored for every production cell. `audit_run/results.json` also stores
explicit radial and angular contributions at z=1.1 kpc for the original and
corrected best cells, with the same transform-then-interpolate convention as UX5.

## Unchanged cuts

- L1: both `|vc-229.1| <= 9.2 km/s` and
  `|vc-229.052972972973| <= 9.289910216347 km/s`.
- L2a: the 43-point vertical-force chi-square is at most 67.45934792232582.
- L2b: `|K(R0)-66.4| <= 4.4 Msun/pc^2`, with R0=8.122 kpc and z=1.1 kpc.
- L3: the 37-point Ou rotation-curve chi-square is at most 59.89250004508689.
- The separately reported strict test is `|h-2.72| <= 0.30 kpc`.

The prior iterator and each width are rechecked against KT25's exact parameter
grid, including the distinction between B175, BV, and BV2. No thick-disc share
or height is changed after observing the result.

## Numerical checks and retained failures

The weighted-adjoint, mass, constant-potential, and Poisson symmetry checks are
near machine precision. Nonlinear reciprocity is checked both by finite source
differences and an analytic discrete Hessian on a nonspherical axisymmetric
background. The isotropic Gaussian known-solution check is particularly small,
but it alone understates angular error: an independent quadrupole-times-Gaussian
known solution has a relative peak error of about 0.00225 on the original grid,
0.00055 at twice resolution, and 0.00024 at three times.

`refinement_run` intentionally exits nonzero when its initial gates fail:

1. Degree 24 produces negative source tails containing roughly `3e-5--6e-5`
   of the mass in selected cells, exceeding the declared `1e-5` tolerance.
   The production run increases the numerical degree to 48; selected best
   cells then have fractions below `5e-7`, and the smallest-width alternative
   candidate has `3.17e-6`. Degree 64 at three times spatial resolution reduces
   the best-cell tails below `3e-8`. The final audit checks every one of the
   2,750 production sources: maximum negative mass fractions are
   `1.332167576e-6` canonical and `3.165378269e-6` alternative, within the
   unchanged `1e-5` tolerance. Degrees 16--40 change the selected observational
   fields by far less than the remaining failed-cut margins.
2. Adding a potential constant of 12345 produces finite differentiation
   cancellation near the innermost 0.005-kpc cells, where a universal absolute
   `1e-7` derivative tolerance fails. `final_checks_run` instead reports both
   the physical observation-region error (r=4--30 kpc, below `1e-9` in the
   tested cases) and a scale-aware floating-point tolerance proportional to
   `epsilon_machine * |G|1 * (12345+max|Phi_ph|)`. The factor 128 used there is
   a practical numerical allowance, not a rigorous operation-count bound.
   `S*1=1` remains independently checked to a few `1e-15`.

The inherited gas-mass diagnostic is reproduced: integrating the half-space
grid gives `0.5000000079393` of the analytic full gas mass. Multiplying the
diagnostic by the missing factor two gives `1.0000000158786`. This repairs
the accounting convention only; gas density and the KT25 width calculation
are unchanged. KT25's unrelated SPARC-envelope failure is not rerun or waived.

This axisymmetric reflection-symmetric Milky Way model cannot test a general
three-dimensional asymmetric net-force condition by itself. The accompanying
root-lane periodic tests address that separate invariant; no spherical or
axisymmetric cancellation is presented as a general force proof.

The final all-source audit passes. Widths and recalculated cuts agree exactly;
source mass preservation is within `1.05e-14` for every cell. Across the entire
population, doubling spatial resolution changes corrected vc by at most
0.03411 km/s canonical and 0.02704 km/s alternative, and K(R0) by at most
0.05794 and 0.05648 Msun/pc². The largest Ou chi-square shifts are 2.911 and
2.372, respectively. These are numerical comparisons, not rigorous error bars.
The production and three-times-resolution best-cell values remain above the
failed rotation-curve cut by substantial margins.

## Reproduction and provenance

All executables are import-safe. The production child command is

```bash
python3 rebuild_2026_10_22/KT33_reciprocal_filter/mw/mw_reciprocal.py \
  --mode grid --refine 2 --lmax 48 \
  --output rebuild_2026_10_22/KT33_reciprocal_filter/mw/grid_refined_run/results.json
```

The actual run uses the computation-audit bounded runner; its complete argv,
hashes, Python/NumPy/SciPy versions, repository revision/dirty state, runtime,
and resource limits are in `grid_refined_run/manifest.json`. To rerun, select
a **new** output directory and pass the contract's `execution_artifacts` as
the runner's repeated `--input` arguments. The runner refuses to overwrite
an existing run directory. Use `grid_refined_contract.json` for the production
scan, `final_checks_contract.json` for the selected numerical checks, and
`audit_contract.json` for the final population/cut/source audit.

The initial `pilot_run` is `launch-failed`: the host rejected the requested
address-space limit in the subprocess setup. It is preserved. Subsequent runs
use explicit wall, CPU, log-volume and numerical-thread limits, with one
numerical thread and no claimed address-space cap. Production limits are
1800 wall seconds, 1750 CPU seconds, and 1 MiB of logs. Zero process exit is
not itself a scientific validation; the separate gated checks must pass.

The numerical conclusion applies to this fixed-width completion at these
unchanged premises. It neither defines a composition-independent universal
system-mass rule nor establishes relativistic stability or causality. It does
not transfer labels to dwarfs, SPARC, clusters, or retired sectors.
