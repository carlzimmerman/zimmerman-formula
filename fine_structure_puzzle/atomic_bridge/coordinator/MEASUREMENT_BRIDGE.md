# Atomic mass already measures alpha; what extra physics is needed?

Parent FSP-001; work package FSP-002. Checked 2026-10-18 America/New_York.

There is an established, physically useful connection between an atom's mass and alpha. [Parker, Yu, Zhong, Estey and Mueller, *Measurement of the fine structure constant as a test of the Standard Model*, arXiv:1812.04130v2](https://arxiv.org/pdf/1812.04130v2), revised 12 December 2018, second manuscript page, gives the recoil relation

`alpha^2 = (2 R_infinity/c) (m_atom/m_e) (h/m_atom)`.

The experiment measures atomic recoil h/m_atom; independent spectroscopic and mass-ratio information supplies the other factors. The underlying identity is `R_infinity=alpha^2 m_e c/(2h)`. Algebraically the chosen atom's mass cancels. This does not make the independent measurements redundant: they determine the electron mass in physical units and provide an independent test of alpha against electron magnetic-moment extraction. It does mean that a heavier baryonic atom is not by itself a new law selecting alpha.

This source was authenticated by title/authors and arXiv identity; the recoil discussion and equation on manuscript page 2 were checked. It is a measurement source, not a proposed fundamental selector. The paper's historical precision comparisons are not used as current claims.

Similarly [NIST CODATA 2022](https://physics.nist.gov/cuu/pdf/all.pdf) defines the infinite-nuclear-mass Bohr radius and Rydberg constant by

`a_B=hbar/(m_e c alpha)=alpha/(4 pi R_infinity)`.

The adjusted recommended a_B is therefore not an extra microscopic prediction independent of alpha, electron mass and spectroscopy. Reconstructing alpha from those mutually adjusted constants is a consistency identity. A physically measured atomic length, with a separate measurement model and correlations, could instead be part of an alpha determination; that is still an extraction from observations.

The difference between **proton rest mass**, **electron rest mass**, **atomic binding mass**, **nuclear size**, **number of atoms**, and **galaxy baryonic mass** matters for the new programme. The first is mainly a QCD/mass-generation question; the atomic electronic length depends strongly on the second and alpha; atomic populations and their astrophysical calibration are further data. The framework's macroscopic baryonic mass cannot be silently equated to a proton's microscopic mass or to a predicted baryon number.

One relevant existing local calculation is `sol61_push/recombination_and_structure_growth/atomic_recombination/atomic_checks.py`. Its hydrogen/recombination laboratory imports a 13.598-eV ionization energy and an electron mass before evolving the plasma. It supplies conditional recombination responses, not a derived atomic binding energy or alpha. The script was inspected, not rerun or modified in this work package. Its local variable `alpha` in the rate routine is a recombination coefficient, with units, rather than the dimensionless fine structure constant; the distinction prevents a false bridge from similarly named symbols.

The constructive target is stronger and more interesting: derive the electron/QCD mass functions and the charge-normalized Maxwell function from the same microscopic framework dynamics, at an independently selected physical scale and vacuum. Then atomic radii, spectra and baryonic rest masses become joint predictions. FSP-H tests the existing medium's binding effect; FSP-Q and FSP-B test actual proposed mass/vacuum mechanisms. No standard mass-recoil identity is presented as that missing derivation.
