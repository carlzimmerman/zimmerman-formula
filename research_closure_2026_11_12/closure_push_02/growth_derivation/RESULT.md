# Independent cosmological growth and joint repair audit

The inherited `mu≈25120 Mpc^-1` isolated-fluid growth floor is not certified for the polarization-retaining action. The correct cold, subhorizon two-fluid equations are

```text
delta_d''+(2+h'/h)delta_d'=(K/h^2)[rho_b delta_b+n f delta_d],
delta_b''+(2+h'/h)delta_b'=(K/h^2)[rho_b delta_b+n delta_d],
f=mu^2/[mu^2+(k_com/a)^2],      K=4piG,
```

where primes denote `ln a`. The baryon forcing of the clock is unsuppressed. This gives a scale-dependent growth delay, not the spurious acoustic cutoff from `1-(k_com/a mu)^2`. It does not itself show that the lower-mu branch fits data.

The exact single-clock-plus-Lambda action-to-density map and the independent Newtonian derivation are in [DERIVATION.md](DERIVATION.md). The homogeneous charge `n=F_Q` scales as `a^-3`, while its exact energy is `rho=n+K n^2/(2mu^2)`. The exact density equation retains the background gravitational term that a frozen positive curvature-mode gradient misses. The single-component momentum constraint is not reused unchanged with baryon perturbations.

The zero-stiffness-Hessian endpoint is a specified smooth reference. The original one-sided `Pi_+^2` stiffness has no single FRW Hessian; this work does not silently assign it a linear Fourier transfer function.

An independent finite-q numerical comparison of the exact curvature action and transformed density ODE agrees to `2.43e-11` on the tested z=4→0 background. The accepted [run_002/result.json](run_002/result.json) has **18 passing checks**, including exact identities, a missing-polarization mutation witness, and EdS recovery. Its [canonical v2 manifest](run_002/manifest.json) validates. This run pins immutable snapshots of prior derivations; `run_001` is preserved but pins the live historical MK1 source and is superseded for ongoing reproducibility after its correction notice.

The old growth floor is unnecessary for a distinct conditional obstruction to the same repair. [BBN_STATIC_AUDIT.md](BBN_STATIC_AUDIT.md) independently derives

```text
rho_stiff/rho_r=Omega_d I0/(4 mu^2 Omega_r a^2),
I0=3H0^2 Omega_d.
```

For the frozen `.067` radiation budget at its declared `T=.1 MeV` proxy and unchanged canonical charge history, this requires `mu>=8.8901135e6 Mpc^-1`. Independently reconstructing the finite-Q-band repair's static lapse-flux bound gives necessary upper endpoints `435.3271`, `445.3183`, and `446.3052 Mpc^-1` for the three stated Lambda benchmarks. The largest endpoint is smaller than the conditional early-universe lower bound by a factor `19919.36`; even allowing stiff energy equal to radiation leaves a factor `5156.00` gap.

This joint incompatibility is conditional on the unchanged homogeneous clock history and dust normalization, declared radiation gate, specified weak-field Q/force target and energy suppression, independently admissible rectangular Q–Pi concavity domain, nonnegative normal density, and absence of an added compensating negative-active stress. The static inequality permits deformation of P. It is not a BBN likelihood, an exact thermal calculation, or an exclusion of all possible theory changes.

The independent [bbn_static_run_001/result.json](bbn_static_run_001/result.json) has **23 passing checks** and its [canonical v2 manifest](bbn_static_run_001/manifest.json) validates. It reconstructs the energy from the action and the numerical cap from profile endpoints without importing either companion agent's driver. Read-only inspection of `growth_gate_audit/growth.py` found no sign, factor, drag, species-ordering or source-matrix error in that declared bounded model.

Key SHA-256 provenance:

| artifact | SHA-256 |
|---|---|
| DERIVATION.md | `77bc63d51695df6ca416f20a84d1f0e589ff1c4b8c578970bd8bca0309f15708` |
| run_002/manifest.json | `5b0d6d739564496106855f51ba873364b51a7763e346997861e43ef8409771e5` |
| run_002/result.json | `71e17886f0792ce70d324ee4e76f3ad0dc934ee2b809d3e984582f167ce76a8f` |
| BBN_STATIC_AUDIT.md | `506b6fbd92121e8442ba3978e44dd11e2f5b5c92252d474cfb5306a6e909384b` |
| bbn_static_run_001/manifest.json | `fe4aa9e94de654f6cd070d2b3260d64d77b1a1e87dea13472ba5bb7bbc840b84` |
| bbn_static_run_001/result.json | `d038f9d7603a790a28f29a6bff16e11f5447c6d73edc5f96cf27acc48f3767af` |

The standard cosmology/BBN primary-source checks and their limited role are cited in the two derivations. No earlier canonical CP02 run or other agent's output was edited, and no commit was made by this lane.
