# SD1 result: the energy reservoir necessarily changes the scale

The explicit positive-scale field can supply DP1's missing energy exchange,
but cannot retain a spatially uniform static acceleration scale around a
nonuniform gravitational field. This is a conditional obstruction, not closure
of the theory. The new potential and kinetic terms are assumptions.

Raw derivation: `DERIVATION.md`. Executable evidence: `check_scale.py`,
`computation_contract.json`, and `run_001/manifest.json` plus `results.json`.
No earlier campaign files were modified, no literature was searched, and no
historical novelty is claimed. The coordinator must review these results before
adopting them as campaign evidence.

## Analytic checkpoint

With a=a_ref exp(chi), the gravitational drive is

    T=-a W_a=gB-2W>0,  T_g=q=g b_g-B>0.

The explicitly assumed scale equation is

    J chi_tt/v_chi²-J Laplacian chi+U'(chi)=T.

Energy exchange is -T chi_t/(4 pi G) in the gravitational sector and the
opposite in the scale sector. Momentum exchange cancels as well. A uniform
static chi requires constant T, hence constant gravitational magnitude g.

The chosen illustrative potential U=S0[cosh(2chi)-1]/4 has a unique homogeneous
equilibrium at each fixed B>0. Its coupled field Schur stiffness is exactly

    M=S0 exp(-2chi0)+B q/b_g>0.

This proves positive quadratic field energy and real positive squared
frequencies for nonzero modes on a nonzero uniform-gradient equilibrium.
The finite-wavelength longitudinal static susceptibility is

    delta g/delta B = (1/b_g)[1+q²/(b_g(M+J k²))].

It predicts an additional positive force response with response length
sqrt(J/M). The model has therefore acquired a concrete size-dependent
correction, governed by new independently unconstrained constants.

## Numerical evidence

The first bounded run completed with **21 checks passed**, no failed
computational checks, and a validated version-2 manifest. Runtime was 1.24 s.
Actual inputs, Python/numpy/scipy versions, output hash, argv, 120 s timeout,
100 s CPU cap and cooperative one-thread cap are recorded. Binary64 results
are not interval-certified proofs.

Independent quadrature/finite differences checked T and its derivatives.
Coupled eigenvalue checks covered 30 equilibria, 71 wave numbers from 1e-4 to
1e3, and three directions. All field eigenvalues were positive; the algebraic
Schur identity agreed to better than 4.6e-14 relative error. The universal
positivity result is supported by the explicit algebra in the derivation,
not inferred from this finite grid.

Nonlinear one-dimensional boundary-value solves checked the susceptibility
at k=1,3 with perturbation amplitudes 0.03,0.01,0.003. At the smallest
amplitude, relative force-response errors were below 3.48e-7. For the declared
inputs B0=1, S0=5 and J=1, the fractional susceptibility enhancement is:

| Branch | k=1 | k=3 |
|---|---:|---:|
| Q | 2.17868% | 0.919874% |
| R | 3.43682% | 1.45360% |

Full spherical solves used the prescribed positive-mass source
B/a_ref=3r/(1+r²)^(3/2), 0<=r<=8, regular center and chi(8)=0. Here r is in
units of a chosen source length, S=S0/a_ref² and ell=sqrt(J/S0) in those units.
The maximal fractional force increases over the fixed-reference law were:

| Branch | S | ell | max chi | max force increase |
|---|---:|---:|---:|---:|
| Q | 5 | 0.2 | 0.0612087 | 2.03417% |
| Q | 5 | 1.0 | 0.0323297 | 1.58157% |
| Q | 20 | 0.2 | 0.0148819 | 0.491865% |
| Q | 20 | 1.0 | 0.00798133 | 0.388030% |
| R | 5 | 0.2 | 0.0735528 | 2.27170% |
| R | 5 | 1.0 | 0.0378009 | 1.75265% |
| R | 20 | 0.2 | 0.0179128 | 0.549391% |
| R | 20 | 1.0 | 0.00933755 | 0.429865% |

Starting from 129 versus 257 nodes changed chi by at most 4.34e-10 on the
reported sample. This checks the declared finite-domain solve; it does not
remove the outer-boundary assumption or prove a global solution. The leading
weak-response approximation differs by at most 3.68% of the chi amplitude
in these examples. Both registered SI normalizations are restored in output;
the dimensionless experiments scale with their assumed coefficients.

A separately manufactured dynamical scale solution checks the scale energy
identity. Its exchange is -0.009236163 in geometric units; the final local
balance residual is 2.66e-10 for both branches, converging under step halving.
The manufactured gravitational magnitude is chosen to match the scale source;
this is an implementation check, not a free coupled matter solution.

## Physical failures and remaining assumptions

1. **Uniform static scale fails:** finite J cannot keep chi exactly constant
   while T varies, absent a tuned extra source or changed coupling.
2. **Literal constant-vacuum identification fails:** a=kappa c sqrt(G rho_Lambda)
   with pointwise constant rho_Lambda forces chi=0, contradicting the preceding
   field equation in a nonuniform field. The conditional survivor requires an
   environmental effective scale around a vacuum-set reference.
3. **The scale field is not automatically vacuum energy:** identifying its own
   homogeneous potential with the required density forces U proportional to
   exp(2chi), which has no finite stationary positive-vacuum point. A canonical
   scalar's gradients/kinetic terms also do not have vacuum stress.
4. **H(z) is not obtained:** the separately prescribed chi=log E history has
   positive chi_tt and nonnegative U' at z>=0, requiring a positive external
   drive even in the homogeneous zero-field model. This check is not an FLRW
   derivation.

Lensing, a physical metric, coupled matter stability, nonlinear global
evolution, parameter inference and observational compatibility remain open.
Positive field energy does not settle any of those obligations.

## Exact provenance

Base Git: `eccd1c0e59459b5ec1acf2e916fb7a05a7f67971`; shared checkout dirty.
The autoresearch instructions are preserved in `AUTORESEARCH_INPUT.md` because
the coordinator's live view may later advance. Its bytes and hash equal the
actual instructions read for this assignment. No old scientific file was copied
and silently modified.

| File | SHA256 |
|---|---|
| campaign_fresh_gravity_astra/CONTRACT.md | db5420f2d60310a6110c90d5354e0416b09e6f764ef48c833d098e29e7d30ebc |
| stage_03/dynamics_precision/DERIVATION.md | 41ad39d1521e7d5b5d974e320478faecd944df8d4608b4869a566624244af3ae |
| AUTORESEARCH_INPUT.md | e04702229680110d3094582e34a1eb00639a45498398651a38a5e69d4d383b86 |
| DERIVATION.md | 2d00fa29165b274d7288505ffc7756c2189a6915dbec6d500fd1a775f6ffb724 |
| check_scale.py | 874d1ad60b813c13169274e63e6afb6d47ef763b9b005c870209447816362cf9 |
| run_001/results.json | db7c8c132aaa5489bf60e957d909edbf0df071da9b1af28c85a66dc82ce4c4dc |

Recheck without overwriting accepted artifacts:

```sh
python3 campaign_fresh_gravity_astra/stage_04/scale_dynamics/check_scale.py /tmp/SD1-recheck.json
```

The full bounded argv is in the manifest. Validation used the installed
computation-audit `validate_manifest.py` with the repository root. Mathematical
self-review and proofreading covered this lane's new files; no independent
acceptance is asserted. The coordinator's external audit belongs in a separate
record.
