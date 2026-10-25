# Continue from the populated pressure-supported branch

Latest directory supersedes the claim that the corrected mobile-density model can only form a depleted transition. The full galaxy-law mechanism is still not solved. Read README and DERIVATION; do not promise exact law preservation based on the inner-core error alone.

## Exact starting state

Use run_final_recovery/base_192.json with class Mixed from mixed_carrier.py, n192, domain12, beta=.5, K15, ell10kpc, charge0. Despite the class name, charge0 makes the energy exactly the inherited Stable action; capacity is diagnostic only. R58.9289138633kpc, total mass 5.364Mb, rM9.45225971kpc. Use polish.py (unscaled E,ftol1e-14) for force balance, not the earlier E/100 stopping criterion. Conservative transfer_species remains mandatory. Both species must be remapped in volume and saturation checked.

## Confirmed evidence

MI-14: n144→192 refinements and joint material/phase±1kpc restoration. No empty cells between15kpc and boundary. Material residual1.26e-7 on final base. The four displaced states return within1.3e-6kpc. MI-15: positive active tangent Hessian and density Hessian, fully relaxed boundary stiffness2.16872374e-4Eunit/kpc², independently confirmed by±.2kpc constrained-radius energies and forces within .3%. Fixed-density stiffness4.03042e-4; never omit the density relaxation.

MI-16: n256/domain64/3 extends box at identical interior grid; radial state unchanged, edge massfraction2.2e-12, energy shift9.8e-7 from changed outer quadrature. Two seeds approach outerR58.913kpc on n144 but differ inside .53kpc; scale4 residual1.43e-4, scale8 residual3e-6. Do not say unique formation or exact same global state. Energy minimization is not physical dynamics.

MI-17 assessment uses endpoint-aware errors: .0030116dex to15kpc, .00821153 to30, .05008613 to50. The last50kpc sample is49.64644kpc and alone would report.04837427dex; that would falsely pass a strict.05dex endpoint gate. There remains about 10.9% gravity deficit at50kpc and larger deviation outside. The original pure-T bulk identity is exact only under its stated conditions, not everywhere in this mixed solution.

The historical qouter cut starts near44kpc and gives.282706; it fails the old.05 gate because the transition has moved out. Report that explicitly. Beyond1.2R=70.715kpc, mass=.77524Mb and Tfraction=.008696; totalFmass1.22586Mb. The outer reservoir is free under this physically explicit exterior diagnostic, which does not retroactively change the historical gate.

## Route history and outcomes

MI-1 run_scan: failed derivative assertion before optimization; largest epsilon1e-4 had2.2e-7 truncation error. Preserve. MI-2 run_checked: resolved steps1e-5,3e-6,1e-6 pass<1e-7; saturated local-density carrier fills old gap but mixes shells and leaves law errors. MI-3 run_thickness: narrower/lower-barrier carrier scans. MI-4 run_pressure: larger K and enlarged domains; apparent optimizer success hid central material residuals. MI-5 run_audit: finite tangent/endpoint Hessian diagnostics on MI-3 only; not final evidence.

MI-6 run_polish fixes stopping-scale issue and exposes carrier charge stored in weak inner phase variations, with remote gap atK30. MI-7 run_mixed introduces b(q)=[4q(1−q)]² capacity; still admits alternative mixed layers/remote-gap branches. MI-8 run_continue follows compact wall through pressure changes; K15/30 developed detached material shells. MI-9 run_controls shows charge not necessary atbeta2,K10,ell10. Ell3/5 can produce empty intervals even with better integrated gravity; do not select candidates by law error alone.

MI-10 run_recovery: charge-freebeta2,K10,ell10 continuous interfaceR49kpc restores on 96/144 but lawto50 error.075dex on144. MI-11 run_wide: ell20/30 worsens law. MI-12 run_low_barrier: beta0,.5,1 withK15 andbeta.5,K30; selectedbeta.5,K15 for continuous material plus free exterior and smaller law correction. MI-13 run_seed: beta2,K10 two seed profiles reach coherent outer branch. MI-14–17 described above. All 17 manifests validated,16completed/1failed, no active jobs at closeout.

## Next productive work

Explain/cancel the measured transition force while retaining the demonstrated density support and positive relaxed stiffness. Avoid fitting a radial density or using the target law in the energy. Any new term must retain all mass, phase and mixed derivatives. A galaxy ensemble with physically universal constitutive parameters and physical transport/conversion dynamics would be new work; neither has been established here. Preserve the seed central differences and endpoint-aware diagnostic in subsequent reports. Further parameter searches must discriminate a named mechanism rather than chase a rounded .05dex threshold.
