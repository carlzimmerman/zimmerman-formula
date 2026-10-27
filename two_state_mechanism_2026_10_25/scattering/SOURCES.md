# Checked primary sources, 2026-10-25

- PySCF configuration interaction documentation:
  https://pyscf.org/user/ci.html . Full configuration interaction includes the
  determinants in the selected orbital basis; it is not complete-basis
  convergence or a continuum scattering calculation. Used PySCF2.11.0.
- Hassaine et al., electron impact rovibrational transitions and dissociative
  recombination of H2+ and HD+, https://arxiv.org/html/2507.14602 . Their MQDT
  treatment requires channel couplings, open/closed-channel elimination and
  nuclear frame transformation. It supports the method requirements here;
  ordinary-hydrogen rate coefficients are NOT imported at mass ratio100.
- Pachucki, Born–Oppenheimer potential for H2:
  https://arxiv.org/abs/1007.0322 . Abstract quotes −1.1744759314002167(3)
  at R=1.4011. This is near, but not exactly at, our R=1.4 comparison.
- Cencek, Ultra-high accuracy calculations for hydrogen molecule and helium
  dimer, https://onlinelibrary.wiley.com/doi/abs/10.1002/qua.21740 . Publisher
  abstract gives BO upper bound −1.174475714220363 at R=1.4. Our DZ/TZ energies
  −1.1646077905882075/−1.1726325713403942 approach this from above, with errors
  about0.009868/0.001843. Thus neither basis is an accurate resonance calculation.

These sources support conventional Coulomb few-body methodology. No novelty
or successful astrophysical mechanism is inferred from them.
