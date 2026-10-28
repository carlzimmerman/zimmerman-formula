# SCOPED NO-GO: acceleration-at-turnaround misses the required basin

The requested condensation mechanism and derivation of kappa remain open.
This independent lane proves a restricted local-trigger obstruction, checks
why a turnaround acceleration threshold sits near 10^20 solar masses, and
separates physical kappa fitting from field-normalization convention.
Kappa = 1/2 remains FITTED. No new field equation is asserted derived.

## Decisive results

1. Using BS1's own inherited central mass and radius, the Local Group has
   canonical g_N/a0 = **0.00582085** and simple-law g/a0 = **0.0792604**.
   Its inherited basin M/T = **1.43480**, so BS1 turns its halo on while
   either acceleration-at-turnaround >a0 rule turns it off. Alt gives
   0.00481655, 0.0718514 and 0.658553 separately. These are spherical
   enclosed-mass diagnostics of inherited processed inputs, not newly
   reduced raw velocities or a claim to model the LG's full geometry.
2. The often quoted **~10^20 solar masses** is a scale estimate, not one
   unique threshold. Finite first turnaround, static force balance,
   Newtonian g_N and actual simple-law g give different coefficients.
   At the inherited 13.821005 Gyr age, canonical Newtonian/no-vacuum gives
   **1.46926e20**, Newtonian+vacuum **7.93904e19**, and the self-consistent
   simple-law+vacuum shell toy at g=a0 **3.27359e19 solar masses**.
3. A smooth spherical exterior annulus can change total basin mass from
   T/4 to 5T/4 without changing any local force/density/velocity data in a
   regular interior neighborhood. Therefore a rule using only these local
   data cannot implement a universal basin-mass switch. Nonlocal state or
   boundary information is required in this class. Dust-gravity-alone also
   has an exact mass-rescaling symmetry at fixed dimensionless initial
   history; it cannot select an absolute threshold by itself.

The last result does **not** refute mass-dependent formation histories,
Sigma_coll(M), cosmological P(k), the actual native zoom program, nonlocal
auxiliary fields, or derivative-extended/screened field equations.

## Executed threshold table

All masses below are in solar masses. No footings are pooled. The vacuum
rate is conditional on equation (1), using canonical a0 and fitted kappa,
H_Lambda = sqrt(32 pi/3) a0_canonical/c. The inherited age has CMB-fit
background calibration; the 10–20 Gyr bracket tests that dependence.

| footing | age (Gyr) | Newtonian, no vacuum, g_N=a0 | Newtonian+vacuum, g_N=a0 | simple-law+vacuum toy, g=a0 |
|---|---|---|---|---|
| canonical | 10 | 4.02662e+19 | 2.86605e+19 | 1.15805e+19 |
| alt | 10 | 7.10706e+19 | 5.05863e+19 | 2.04397e+19 |
| canonical | 13.821 | 1.46926e+20 | 7.93904e+19 | 3.27359e+19 |
| alt | 13.821 | 2.59327e+20 | 1.40125e+20 | 5.77795e+19 |
| canonical | 20 | 6.4426e+20 | 2.02834e+20 | 8.68465e+19 |
| alt | 20 | 1.13713e+21 | 3.58005e+20 | 1.53286e+20 |

Static balance is a separate boundary: canonical Newtonian g_N=a0 gives
5.79043e20 solar masses; static simple-law g=a0 gives 2.89522e20. Alt gives
1.02202e21 and 5.11011e20 respectively. Applying the simple response only
*after* solving Newtonian radii gives one-eighth of the Newtonian threshold;
that column is retained in `run3/results.json`, explicitly a postprocessing
diagnostic rather than self-consistent dynamics.

Across all declared threshold conventions and ages, the smallest threshold
is still 2.08206e6 times the inherited canonical T and 1.68672e6 times alt T.
These comparisons use the inherited CL3/BS1 T values; they do not validate
the onepager's claimed single surface-density closure.

## Kappa: exact surviving statement

For the specified simple-law scalar class,

    L = -A F(B |grad psi|^2) - q rho psi,
    F(z) = z - 2 sqrt(z) + 2 ln(1+sqrt(z)) + C,

physical acceleration uses phi=q psi. Then

    G_N = q^2/(8 pi A B),  a0=q/sqrt(B).

The genuine field redefinition psi_new=ell psi sends q to q/ell and B
to B/ell^2, leaving G_N, a0 and physical kappa invariant. Thus a fitted
kappa is not merely a field convention. If a covariant completion identifies
A C with rho_DE c^2, then kappa^2=8 pi/C. The choice C=32 pi is precisely
kappa=1/2; the simple force law leaves C unconstrained. That conditional
normalization obstruction is already anticipated by the prior record. This
lane audits it rather than presenting it as a new universal theorem.

## Verification and provenance

- Exact claims, hypotheses, derivations, restrictions and self-audit:
  `DERIVATIONS.md`. Input ledger and criteria: `FROZEN_CRITERIA.md`.
- Current executable evidence: **run3**, status **completed**, 6/6 checks,
  exit 0, 0.897 s and 0.094 GB peak RSS. Adaptive and independent 20,001-point
  Simpson quadratures differ by at most 4.45e-16 relatively. Original SI
  reconstruction residual is below 9.11e-15.
- Mutation: **run_MUTATE2**, deliberately removes the factor two in the
  transformed Newtonian time integral. Thresholds change, K2 and independent
  SI check K3 fail, 4/6 checks, exit 1, valid failed-run manifest.
- Both current manifests validate against current source and inputs.
- A fresh delegated reviewer independently reconstructed the formulas and
  used a 4,096-panel Simpson+bisection calculation without the project
  script; q and the actual-g beta agree to about 1e-12 relative mass error.
  The root coordinator separately checked the restricted derivations.
- Review-only math proofreading covered this file and DERIVATIONS.md;
  routine changes only, no mathematical-token correction under proofreading.
- Prior failed/provisional runs are retained. `run` failed from cancellation
  in the potential difference near the static endpoint; the current code
  rationalizes it and uses log1p. `run2` predates a strengthened mutation and
  is superseded. `run_MUTATE` only perturbed a benchmark and is superseded
  because it did not exercise the threshold computation. The launch before
  `run` failed before computation because macOS lacks CPU affinity support;
  sandbox also rejected nice/setpriority. Amendment A1 records the control
  change. Current run stays single-threaded with 90 s wall and 60 s CPU caps.
- Base git revision: 7954d48377463cafcae3e8dbb09454134aef384f; existing dirty
  work preserved. No commits: coordinator override due to read-only .git.
- Machine-readable input hashes: `INPUT_SHA256.json`; artifact hashes:
  `SHA256SUMS`. Each v2 manifest separately records input hashes before/after.

## Reproduce

Use Python 3.10+ for the wrapper and installed mathbox bounded runner, with
Python 3.9.6 plus scipy 1.11.4 and sympy 1.14.0 for this recorded computation.
Choose a new output name; existing evidence is never overwritten.

    OMP_NUM_THREADS=1 python3.11 rebuild_2026_10_22/INDEPENDENT_PUSH_2026-10-28/basin_kappa/run_audit.py --runner "$CODEX_HOME/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py" --name reproduced

Append `--mutate` with a different new name for the negative control. A
zero exit verifies the finite checks, not condensation or a covariant theory.

## Prior routes checked and next live obligation

Read the theory equations, rebuild and doors briefs, BS1 criteria, script,
outputs and amendments; the kappa convention audit; puzzle_32pi README,
p24/p25 and p63; kappa_slot README/KS00; D5_kappa_four; nearby U1 shell-theorem
and G2 background records. Thermal normalization, topological number matching,
near-marginal tail fitting and frozen covariant attempts were not relaunched.

The next live step is precise: a proposed condensation mechanism must evolve
an additional state that can acquire common basin information and change cold
sector stability. First test it on the paired annulus initial conditions;
then demonstrate why its mass dependence survives realistic formation histories.
A local force-only rule and dust gravity at fixed dimensionless history do
not supply that missing state. No expensive job is needed to reject those
restricted classes, and no final equation has been invented to replace them.
