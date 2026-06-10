# Provenance — what is borrowed, what is the framework's

*Honest attribution for the theory machinery used in the deep-MOND-sign work (projects 1, 1b, 1c, 3, 4b–4f).
The framework BUILDS ON established results from several groups; the distinctive contribution is the
application to MOND. Stated plainly so no credit is misplaced and the paper cites correctly.*

## Borrowed (established physics — not the framework's)

- **SYK model:** Sachdev & Ye, *PRL* (1993); Kitaev (KITP talks, 2015).
- **Double-scaled SYK; the chord-diagram solution; the transfer matrix; the matter two-point element**
  (everything I computed in projects 4c–4f): **Berkooz, Isachenko, Narovlansky, Torrents**, arXiv:1811.02584
  (2018); **Henry Lin**, arXiv:2208.07032 (2022) for the bulk/chord Hilbert space and matter chords. The
  q-deformed-Schwarzian matter element I validated is *their* object; I only checked a conjectured closed form
  against its known limits.
- **DSSYK ↔ de Sitter static patch (the dual the sign-derivation relies on):** **Narovlansky & Verlinde**,
  arXiv:2310.16994 (2023); **Rahman**, arXiv:2209.09997; **Susskind** and collaborators (the de Sitter /
  static-patch / "separation of scales" program). Susskind is a principal architect of the de-Sitter side.
- **Complexity = Volume / Complexity = Action / the second law of complexity** (the original Project 4
  complexity-sign attempt): **Susskind**, with Stanford, Brown, Roberts, Swingle, Zhao. This thread is his.
- **Emergent / entropic gravity; a0 ~ cH; MOND-like behaviour from horizon degrees of freedom:**
  **Erik Verlinde**, arXiv:1001.0785 (2011) and arXiv:1611.02269 (2016). The a0~cH emergent-gravity idea is
  Verlinde's, NOT Susskind's.
- **MOND:** **Milgrom**, *ApJ* (1983); the RAR/BTFR phenomenology: McGaugh, Lelli, Schombert.
- **Supporting GR/thermo results:** Jacobson 1995 (thermodynamics of spacetime); Cai–Kim 2005 (apparent-horizon
  first law); Deser–Levin 1997 (de Sitter–Unruh temperature); 't Hooft 1985 (brick wall); Skordis–Zlosnik
  2021 (AeST, the covariant MOND theory).

## The framework's own contribution

- **a0 = (c/2)√(Gρ) = cH/Z** as the surface gravity of the cosmic horizon, with the specific Z = 2√(8π/3), and
  the **rising-a0 (apparent-horizon) bet** a0(z) = a0(0)E(z).
- **The bridge to DSSYK:** identifying that the (established) DSSYK de Sitter chord-vacuum spectrum is flat at
  the de Sitter point, that the matter chord couples to it, and that this yields the deep-MOND linear freezing
  → the √-law. The *connection* emergent-MOND ← DSSYK de Sitter horizon DOF is, to the author's knowledge, new;
  Susskind/Verlinde/Berkooz/Lin supply the machinery, not this target.

## Caveat

The novelty claim is bounded by the author's knowledge of the literature, which is incomplete. A proper
literature search is required before claiming the MOND↔DSSYK connection is original. The result is
"established machinery applied to a new target," which is legitimate physics but must be presented as building
on the above, not inventing it.

---
## Triage entry — 2026-06-09 (provenance of orphan working-tree files)
The following were untracked in the working tree, produced by a **prior session dated 2026-06-05**
(not the 2026-06-06+ doors/labels-close session), and are **claimed** here after triage:
- `INTEGRITY_AUDIT.md` — integrity audit grading all 320 `real_research/` scripts (real-data/real-calc/
  literature/theatre). Verified-by: inspection (it is a report, not re-run).
- `reviews/A0_COSMICWEB_ENVIRONMENT_2026-06.md` + `reviews/project_sparc_a0_vs_cosmicweb.py` +
  `data/sparc_a0_environment_table.csv` + `figures/a0_vs_cosmicweb.png` — does a₀ track the cosmic web?
  **NULL** (Spearman −0.08, p=0.38; slope −0.05±0.08; the +0.5 ρ_local fork excluded across 3 external
  density fields; 3σ-detectable-slope floor ~0.15 honestly stated). **Verified-by: re-run, null reproduced.**
  **EFE-adjacent — flag for the EFE workstream (predictions 9/12):** environment-classified a₀ universality.
- `predictions/project_sparc_groupcontrast_kt2017.py` — companion group-contrast script (same June-5 work).

Quarantined (could not attribute to on-topic work): `FIRST_PRINCIPLES_OF_LIVING.html` ("Optimal Human
Flourishing" — off-topic), `figures/fig3_hubble_node.png` (orphan, unreferenced) → moved to `unattributed/`.
Removed: `reviews/REDERIVE_circularity_audit.py` (identical dup of the committed `reviews/labels_close/` copy).
NOT claimed (unsourced working-tree modification, left in place): `reviews/project14_wide_binaries.py`.
