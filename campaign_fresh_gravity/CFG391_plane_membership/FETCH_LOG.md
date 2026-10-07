# CFG391 FETCH_LOG

All fetches 2026-10-06 with curl (owner-approved for this lane). The raw files sit in `fetched/` (lane-local
.gitignore; papers are not redistributed). Every value used is read from the source text itself, not from a
summariser.

| URL | bytes | sha256 | what |
|---|---|---|---|
| https://arxiv.org/e-print/1204.5176 | 947515 | a9e65368f4f72dd81e99e59efba315e0f939c7eedd29cf246276736d51428f7f | Pawlowski, Pflamm-Altenburg & Kroupa 2012 (MNRAS 423, 1109) LaTeX source (gzip tar) |
| https://arxiv.org/e-print/1911.05081 | 2742488 | 839cbd2124bb4e18656e62c052c9d505a36699498bf9510187a23cf2446036f0 | Pawlowski & Kroupa 2020 (MNRAS 491, 3042) LaTeX source (gzip tar) |
| https://arxiv.org/e-print/1301.0446 | 966263 | 37da1ba8a818bd51bf561af58c9de8601bab60fe2f5efc868ad83bbb15f60f0a | Ibata et al. 2013 (Nature 493, 62) arXiv PDF incl. Supplementary Information (19 pp) |

## Values taken (location in the source)
- PPK12 `VPOS.tex` Table 1 (`tab:normalpositions`, "Directions of normal-vectors"), Galactocentric (l, b):
  DoS 2007 (157.3, -12.7) 11 classicals [Metz 2007]; DoS 2009 (149.6, -5.3); DoS 2009 w/o Her (159.7, -6.8);
  **DoS (156.4, -2.2), 24 satellites [Kroupa 2010]**; Faint DoS (151.4, 9.1); mean orbital pole (177.0, -9.4)
  6 satellites [Metz 2008]; average stream normal (155, -26); Magellanic Stream normal (179, 3) per PK20.
  The recalled value (169.3, -2.8) used by session 06 appears in neither paper.
- PK20 `VPOS_GaiaDR2_arXiv.tex` Sect. 2.3 (itemized list after Table 4): **VPOSnew (164.0, -6.9)** "minor axis
  direction of the overall Milky Way satellite system" [Pawlowski 2015 MNRAS 453, 1047]; VPOSclass (157.3, -12.7)
  [Metz 2007]; M.S. normal (179, 3) [PPK12].
- PK20 Table 4 (`tab:deltasph`), Combined sample, k = 7: average pole (179.5, -9.0), theta_VPOSnew = 16.9 deg,
  Delta_sph = 16.0 deg.
- PK20 Table 3 (`tab:individualpoles`), Combined PMs: l_pole, b_pole, Delta_pole for the 11 classicals
  (Sgr 275.2/-8.0/0.8; LMC 175.3/-5.9/1.1; SMC 191.8/-10.5/1.9; Draco 169.9/-19.3/1.2; UMi 195.5/-8.0/4.3;
  Sculptor 349.3/-2.2/2.0; Sextans 232.7/-49.4/3.4; Carina 160.5/-11.9/6.5; Fornax 176.5/15.8/6.7;
  Leo II 186.3/-21.2/23.2; Leo I 251.1/-38.6/17.9).
- PK20 Sect. 2.3.3 (Combined sample) text: seven of 11 classicals in the dominant pole cluster (LMC, SMC, Draco,
  UMi, Carina, Fornax, Leo II per Table 3 theta_J6), Sculptor counter-orbiting in the same plane; "only
  Sagittarius, Sextans, and Leo I can not be clearly associated to the VPOS".
- Ibata 2013 Supplementary Information Sect. 2 "The planar satellites" (arXiv PDF p. 17): 13 co-rotating =
  And I, III, IX, XI, XII, XIV, XVI, XVII, XXV, XXVI, Cas II, NGC 147, NGC 185; planar but not co-rotating =
  And XIII, And XXVII (15 planar in all); NGC 205, LGS 3, IC 1613 "may plausibly be associated".

No later Pawlowski per-object M31 list was fetched (not needed for the frozen G1-G3 definitions).
