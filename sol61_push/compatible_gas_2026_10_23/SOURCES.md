# Sources and provenance
Inherited action, units, thermal source and prior failure records: ../baryon_pressure_2026_10_23/{HANDOFF,DERIVATION,SOURCES,AUDIT}.md and the copied radial_base.py. Initial repository HEAD fbeb5f54aeca61a327cecec9f43a49c94cda38f0; shared dirty tree, this phase writes only its own directory.

Glover (2015), MNRAS453 2901–2918, https://academic.oup.com/mnras/article/453/3/2901/1079636, DOI10.1093/mnras/stv1781, section4.1.2 equations31–33: authenticated HM79 rotational/vibrational LTE formula used here. The paper compares it with a newer fit: agreement within about10% below2000K, with larger differences at higher temperatures. Our results above2000K use the approximate older rate, not a validated chemical network. The GP98 low-density fit and harmonic density bridge come from the previously authenticated Galli & Palla1998 AppendixA (astro-ph/9803315v1); conventions copied from the prior phase. No cosmological or black-hole population claims imported from these papers.

Attempts to open the NIRVANA A&A2018 article/PDF returned403. Its search snippet is not treated as authenticated evidence. The compatible gas discretization is derived explicitly here; it is not claimed to implement a named published compatible-hydrodynamics algorithm.

All physical cooling rates in code are cgs erg/s per molecule and erg cm3/s for the low-density coefficient. One erg/cm3/s=.1 J/m3/s. rho_unit=M0/(4pi ell^3), with M0 in mass units; the radial volume convention omits the4pi by construction. Thermal energy is per unit gas mass in ell^2/t0^2 units.
