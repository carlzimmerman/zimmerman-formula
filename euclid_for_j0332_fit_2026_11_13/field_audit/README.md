# Flattened AQUAL field and lensing audit

`run_01` completed in 38.15 seconds; its manifest validated with current input
hashes. No density-normalization or projection defect was found at the finite
points tested. All requested numerical comparisons were below a relative
vector-deflection tolerance of 0.2%.

| Test | Largest observed relative vector difference |
|---|---:|
| Newtonian field versus independent analytic elliptical Sérsic deflection, 256×48 | 0.13590% |
| Newtonian field versus independent analytic elliptical Sérsic deflection, 512×96 | 0.03583% |
| AQUAL mesh 256×48 → 512×96 | 0.06226% |
| AQUAL outer radius 500 → 1000 Re | 0.003093% |
| LOS quadrature 192 → 768 nodes, all fields | 0.001188% |

The comparison uses M=1e12 Msun, n=5.8687, projected q=.813 and major-axis
Re=1.13918/sqrt(q) arcsec. Positions comprise radii 0.5, 1, 1.5, 2 and 3 arcsec
at angles 0°, 45° and 90° from the projected major axis. Both inclinations 90°
and 60° hold projected flattening fixed, with intrinsic oblate q=.813 and
.7402423 respectively. There are twelve field solves: two inclinations,
Newtonian or simple-mu AQUAL, and three mesh/domain settings. Every field is
projected with 192, 384 and 768 LOS nodes.

The independent Newtonian reference integrates the elliptical projected
surface mass density directly. It does not use the grid, potential, gradients,
or 3D density table in `aqual_lensing.py`. For major-axis coordinates u,v and
D=1−(1−q²)t, it evaluates

    alpha_u = q u ∫_0^1 kappa(sqrt(t [u² + v²/D])) D^(−1/2) dt
    alpha_v = q v ∫_0^1 kappa(sqrt(t [u² + v²/D])) D^(−3/2) dt.

Here kappa=Sigma/Sigma_crit, and Sigma is a Sérsic surface profile normalized
to total projected mass M with ellipse area factor q. In the circular limit,
substitution R'=sqrt(t)R gives `alpha=2/R ∫_0^R kappa(R') R' dR'`, agreeing with
analytic Sérsic projected enclosed mass; that factor check has maximum
relative error 3.11e-15. The actual elliptic integral uses t=s^(2n) to resolve
the central high-n behavior.

All explicitly recomputed discrete field residuals were below 2e-9. Maximum
absolute deposited mass normalization error was 1.09e-5. The outer-domain
comparison at fixed radial cell count also slightly changes radial cell
spacing; it measures their combined effect and does not isolate the boundary
condition alone.

This is finite numerical evidence. The absolute analytic comparison is
Newtonian. AQUAL convergence at these positions is not proof of absolute
nonlinear accuracy, coverage over the image-fit parameter domain, physical
theory correctness, or image-fit quality. In particular, any fit exploring
more extreme Sérsic indices or intrinsic flattenings needs appropriate
additional accuracy checks.

Reproduction from the repository root (use a fresh run directory name if
`run_01` already exists):

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract euclid_for_j0332_fit_2026_11_13/field_audit/contract.json \
  --input euclid_for_j0332_fit_2026_11_13/field_audit/audit.py \
  --input euclid_for_j0332_fit_2026_11_13/aqual_lensing.py \
  --input closure_2026_11_06/QX4_udg/aqual.py \
  --output euclid_for_j0332_fit_2026_11_13/field_audit/run_01 \
  --result euclid_for_j0332_fit_2026_11_13/field_audit/run_01/result.json \
  --timeout 900 --max-output-bytes 262144 --max-cpu-seconds 880 --max-threads 1 \
  -- python3 euclid_for_j0332_fit_2026_11_13/field_audit/audit.py \
  --output euclid_for_j0332_fit_2026_11_13/field_audit/run_01
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  euclid_for_j0332_fit_2026_11_13/field_audit/run_01/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```
