# Source and acquisition record

Checked 2026-11-05. Numerical factual extracts are retained; full author HTML is ignored locally. Existing project source files were read, not modified.

## S1 — galaxy sizes and black-hole masses

Graham & Sahu, *Appreciating mergers for understanding the non-linear Mbh–M*,spheroid and Mbh–M*,galaxy relations, updated herein, and the implications for the (reduced) role of AGN feedback*, MNRAS 518, 2177–2200 (2023), DOI 10.1093/mnras/stac2019; published online 2022-11-25.

- Article: https://academic.oup.com/mnras/article/518/2/2177/6847192
- Table 1: https://academic.oup.com/view-large/389205838
- Acquisition: direct HTTP returned 403; web tool successfully exposed the public table. Numerical columns were extracted from all original rows L11–L114, with duplicate rendered rows cross-checked and deduplicated. 104 unique names, two missing spheroid sizes, nine author-excluded size rows, one upper limit (also missing size). The analysis uses 93 author-clean size entries.
- Radius: projected, circularized spheroid half-light radius in kpc. Masses and distances follow the table's adopted values, not a claim these are the newest estimates.
- Authenticated title/authors/version and table definitions; checked source spot values for M87 and Andromeda. Not every underlying individual dynamical measurement was re-audited.
- NGC 5055 is excluded by the source; do not treat its tabulated mass as a valid detection in a new residual study.

## S2 — hot gas and environment

Gaspari et al., *The X-ray Halo Scaling Relations of Supermassive Black Holes*, ApJ 884, 169 (2019), DOI 10.3847/1538-4357/ab3c5d; arXiv:1904.10972v2, 2019-10-23.

- Versioned full text: https://arxiv.org/html/1904.10972v2
- Tables 2 and 3: 85 matching optical and X-ray rows, parsed by extract_gaspari.py. Original source SHA256 is stored in data/gaspari.json and records/acquisition.json.
- Optical radius is a total optical half-light radius. X-ray galactic, core, and R500 apertures are distinct. Core and large-scale measurements can be repeated galactic values for noncentral systems; they are not independent repeated observations.
- Environment column names the central system; BCG/BGG/BFG prefixes mark central classifications. Satellite rows carry the central host's name. Counts: 8 cluster centrals, 21 group centrals, 17 field centrals, 9 isolated and 30 satellites.
- Association with hot-gas temperature is already reported by this paper; our analysis is an exploratory reanalysis, not a new discovery or a replication of its Bayesian slope estimates.
- Tables and definitions authenticated/extracted; original mass methods and their selection function are not fully audited. NGC 7331 remains specifically flagged for original-source follow-up.

## S3 — SPARC availability

Local 175-file rotation-curve collection: real_research/data/sparc_data/*_rotmod.dat. Prior provenance audit: real_research/data/SPARC_table.README.md. Its source URL is https://astroweb.case.edu/SPARC/Rotmod_LTG.zip . This session hashed every local file in the robustness manifest and scanned every filename; it did not refetch the archive. Exact-name overlap is NGC5055 and NGC7331. No general population residual fit is justified by this overlap.

## S4 — model equation

Milgrom, *Quasi-linear formulation of MOND*, MNRAS 403, 886 (2010), arXiv:0911.5464v2: https://arxiv.org/abs/0911.5464v2 . Abstract explicitly states the modified Poisson source used in THEORY.md. Verified the model definition; the enclosing-sphere inequality is derived here under additional stated hypotheses. No attribution of that inequality or novelty claim is made.

## Prior internal records

- sonnet55_push/puzzle_32pi/README.md, including withdrawn early no-horizon assertions.
- sol61_push/puzzle_32pi_coefficient_verdict_2026_10_14/RESULT.txt: additive vacuum-offset counterfamily; original 32π target unresolved.
- sol61_push/puzzle_32pi_handoff_2026_10_15/HANDOFF_FOR_CLAUDE.txt: scoped scalar-action failures.
- opus_48_extended_research/reviews/collective_efe/COLLECTIVE_EFE_CLUMPY_VS_SMOOTH_VERDICT_2026-06-20.md: related historical computation; not rerun wholesale. Fresh flux checks and the finite-radius correction are in this campaign.
