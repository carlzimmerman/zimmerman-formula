# RFX1 SOURCES (every published number; all web reads PROVISIONAL)

Read 2026-11-12/13 through a page summariser (WebFetch); numbers quoted by the summariser from the abstract page or
the arXiv HTML. The repository's citations/works notes for petersen-2020, erkal-2021, kallivayalil-2013,
van-der-marel-2002, pietrzynski-2019, salem-2015, stanimirovic-2004 and putman-2003 were read first; they hold
bibliographic records and script cross-references only, no numbers used here.

## Mass inventories (read BEFORE the freeze; inputs)

| number | source | where | flag |
|---|---|---|---|
| LMC baryons 3.2e9 Msun (stars 2.7e9 + HI 5e8 x 1.33) | repository hunt_2026/h37_lmc_bound.py line 40, as used by LMC1's criteria (row "LMC baryons") | file | PROVISIONAL (as in LMC1) |
| SMC stellar mass about 3.1e8 Msun; neutral gas 5.6e8 Msun | van der Marel et al., "Kinematical Structure of the Magellanic System", review (arXiv:0809.4268), Section 3 "SMC Kinematics", quoting Stanimirovic et al. 2004; read at https://ned.ipac.caltech.edu/level5/March09/vanderMarel/vanderMarel3.html | Section 3 text | PROVISIONAL; the page does not say whether helium is included; 5.6e8 = 1.33 x 4.2e8, so it is read as including helium |
| SMC dynamical mass 2.4e9 Msun (context only) | Stanimirovic, Staveley-Smith and Jones 2004, ApJ 604, 176, arXiv:astro-ph/0312223, https://arxiv.org/abs/astro-ph/0312223 | abstract | PROVISIONAL; not used |
| Magellanic System gas outside the Clouds, atomic plus ionised, about 2.0e9 Msun; ionised more than twice the atomic | Fox et al. 2014, ApJ 787, 147, arXiv:1404.5514, https://arxiv.org/abs/1404.5514 | abstract | PROVISIONAL; distance assumption and helium not stated in the abstract; the lane applies x 1.33 (upper end) |
| HI of the Magellanic gaseous features 4.87e8 Msun (d / 55 kpc)^2 | Bruens et al. 2005, A&A 432, 45, arXiv:astro-ph/0411453, https://arxiv.org/abs/astro-ph/0411453 | abstract | PROVISIONAL; the summariser labelled it "LMC and SMC combined", the abstract context reads as the system's gaseous features; reported variant only |
| Milky Way hot gas inside 50 kpc 3.846e9 Msun (Miller and Bregman 2015 profile) | repository closure_2026_11_12/MWG1_hot_halo_gas/RESULT.md line 70 | file | PROVISIONAL (MWG1's web read) |
| Milky Way census baryons (McMillan 2017) | copied module (lmc1_core.py / raw1_model.py) | code | raw-derived compilation |

## Reflex / travel velocity measurements (read AFTER the freeze, except the primary as quoted by the lead)

| measurement | paper | URL read | where | numbers |
|---|---|---|---|---|
| PRIMARY | Petersen and Penarrubia 2021, Nature Astronomy 5, 251, "Detection of the Milky Way reflex motion due to the Large Magellanic Cloud infall", arXiv:2011.10581 | https://arxiv.org/abs/2011.10581 | abstract | v_travel 32 +4/-4 km/s toward (l, b) = (56 +/- 9, -34 +10/-9) deg, tracers 40 < r < 120 kpc. Confirms the lead's numbers. |
| variant | Yaaqib, Petersen and Penarrubia 2024, "The radial variation of the LMC-induced reflex motion of the Milky Way disc observed in the stellar halo", arXiv:2402.10841 (the lead wrote "Yaaqoob"; the arXiv page spells "Yaaqib") | https://arxiv.org/html/2402.10841v2 | Table 2 | 20-30 kpc 16 +/- 2 (120, 19); 30-40 kpc 17 +/- 5 (139, -59); 40-50 kpc 23 +/- 7 (64 +23/-24, -47 +20/-16); 50+ kpc 40 +/- 7 (38 +/- 11, -37 +11/-10). The summariser placed Table 2 under a heading about simulations; read as the data fit (the abstract describes measurements). Graded rows: 40-50 and 50+. |
| variant | Chandra et al. 2024/2025, ApJ (DOI 10.3847/1538-4357/addab6), "All-Sky Kinematics of the Distant Halo: The Reflex Response to the LMC", arXiv:2406.01676 | https://arxiv.org/html/2406.01676 | Table 2 (at 100 kpc); Table 1 (linear model endpoints) | at 100 kpc v_travel 37 +/- 9, apex Galactic (-80 +/- 18, -59 +11/-9), components (3, -17, -31); endpoints 40 kpc 6 +5/-4, 120 kpc 47 +/- 12. Right-handed Galactocentric frame, solar velocity (12.9, 245.6, 7.8). The paper says PP21's apex lies in the opposite southern quadrant from its own: a real difference, not a convention. |
| variant | Bystrom et al. 2025, MNRAS, "Exploring the interaction between the MW and LMC with a large sample of blue horizontal branch stars from the DESI survey", arXiv:2410.09149 | https://arxiv.org/html/2410.09149 | Section 3.3, Table 1 | outer halo R > 50 kpc: v_dipole -34.0 +/- 10.6 km/s, apex (-72.7 +/- 21.2, -52.9 +/- 12.6); monopole -24 km/s (abstract). The sign convention of v_dipole was not read; the amplitude 34.0 is graded. |
| variant | Li et al. 2026, "The velocity field of our Milky Way outer stellar halo based on DESI DR2", arXiv:2604.01628 | https://arxiv.org/html/2604.01628 | Section IV.4, Table 3 | 50-120 kpc mu_dipole -24.0 -3.8/+3.7, apex (-34.8, -37.8); 50-60 -18.1 -3.4/+3.6 (-87.6, -48.8); 60-80 -20.0 -4.4/+4.0 (-14.3, -41.6); 80-120 -44.0 -5.4/+5.3 (-28.3, -23.8). The summariser flagged that the text gives l -30 for 50-120 and -19 for 50-60; table values used. |
| not gradable | Erkal et al. 2021, MNRAS 506, 2677, arXiv:2010.13789 | https://arxiv.org/abs/2010.13789 | abstract | no velocity amplitude in the abstract (southern stars blueshifted, northern redshifted, r > 50 kpc); not graded |

Two sources disagree on direction: PP21 and Yaaqib+ 2024 put the apex at positive l (56 / 38), while Chandra+ 2024,
Bystrom+ 2025 and Li+ 2026 put it at negative l (-80 / -73 / -35). Both are listed and graded as variant rows on
amplitude; only the primary enters K3 (frozen).

Data (own-stars item only): https://data.desi.lbl.gov/public/dr1/vac/dr1/mws-bhb/v1.0/MWS_BHB.fits, sha256
5669c8212bf122d20f681ee15d5de1a61d0a4e7d8d2cc8b061211b3317115246, not in the repository.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
