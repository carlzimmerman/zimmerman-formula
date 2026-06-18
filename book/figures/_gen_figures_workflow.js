export const meta = {
  name: 'book-figures',
  description: 'Generate honest, self-contained figures + sourced captions for every chapter of the textbook',
  phases: [{ title: 'Figures', detail: 'one agent per chapter reads it and produces matplotlib scripts + sourced caption markdown' }],
}

const chapters = [
  {num:1,file:'01_a_mystery_in_the_spin_of_galaxies.md'},
  {num:2,file:'02_weighing_the_sky_kepler_newton_and_the_l.md'},
  {num:3,file:'03_the_virial_theorem_and_fritz_zwicky_s_he.md'},
  {num:4,file:'04_vera_rubin_and_the_flat_rotation_curves_.md'},
  {num:5,file:'05_two_roads_from_the_fork_a_particle_or_a_.md'},
  {num:6,file:'06_hunting_the_invisible_wimps_axions_and_f.md'},
  {num:7,file:'07_einstein_s_gravity_the_equivalence_princ.md'},
  {num:8,file:'08_the_field_equations_how_matter_tells_spa.md'},
  {num:9,file:'09_an_expanding_universe_hubble_friedmann_a.md'},
  {num:10,file:'10_echoes_of_the_beginning_the_cosmic_micro.md'},
  {num:11,file:'11_1998_the_universe_accelerates_and_dark_e.md'},
  {num:12,file:'12_cdm_and_its_patches_the_honest_ledger_of.md'},
  {num:13,file:'13_what_is_inertia_really.md'},
  {num:14,file:'14_temperature_from_acceleration_the_unruh_.md'},
  {num:15,file:'15_de_sitter_space_a_universe_with_a_temper.md'},
  {num:16,file:'16_entropy_horizons_and_holography.md'},
  {num:17,file:'17_milgrom_s_idea_modifying_dynamics_below_.md'},
  {num:18,file:'18_the_two_great_regularities_rar_and_baryo.md'},
  {num:19,file:'19_what_mond_gets_right_and_its_real_proble.md'},
  {num:20,file:'20_the_central_claim_a_c_32.md'},
  {num:21,file:'21_the_mechanism_de_sitter_unruh_modified_i.md'},
  {num:22,file:'22_what_is_forced_the_form_and_the_8_3_kern.md'},
  {num:23,file:'23_the_one_free_number_why_cannot_be_derive.md'},
  {num:24,file:'24_one_knob_against_six_parameters_and_a_pa.md'},
  {num:25,file:'25_the_signature_prediction_a_tracks_dark_e.md'},
  {num:26,file:'26_how_it_will_be_tested_btfr_sign_desi_and.md'},
  {num:27,file:'27_the_value_of_a_is_not_derived_and_the_st.md'},
  {num:28,file:'28_the_lensing_wall_why_bending_light_stays.md'},
  {num:29,file:'29_the_cluster_residual_and_the_mond_shared.md'},
  {num:30,file:'30_a_bridge_to_particle_physics_the_lorentz.md'},
  {num:31,file:'31_not_a_theory_of_everything_yet_the_hones.md'},
  {num:32,file:'32_what_would_it_take_to_know_a_reader_s_gu.md'},
]

const SOURCE_PALETTE = `
REAL SOURCES — cite ONLY from this palette or the repo itself. NEVER invent a citation, DOI, or arXiv id.

Repo (blob base for any file path): https://github.com/carlzimmerman/zimmerman-formula/blob/main/
Framework published papers (Zenodo):
  - Spine / main result:  https://doi.org/10.5281/zenodo.20721540
  - a0(z) dark-energy scale: https://doi.org/10.5281/zenodo.20737162
  - kappa one-parameter geometry theorem: https://doi.org/10.5281/zenodo.20738055
Repo scripts you may cite as provenance for framework curves:
  - opus_48_extended_research/papers/a0z_desi_figure.py            (the a0(z) curve)
  - opus_48_extended_research/reviews/derivation_chain/mi_ppn_alpha2_verify.py
  - opus_48_extended_research/reviews/KAPPA_FORCING_DOOR_CLOSED_2026-06-17.md

Background literature / data (use the matching one; these are REAL):
  - Rotation curves / dark matter: Rubin & Ford 1970, ApJ 159, 379
  - Cluster missing mass: Zwicky 1933, Helv. Phys. Acta 6, 110 (and 1937, ApJ 86, 217)
  - SPARC galaxy database: http://astroweb.case.edu/SPARC/ ; Lelli, McGaugh & Schombert 2016, AJ 152, 157 (arXiv:1606.09251)
  - Radial Acceleration Relation (RAR): McGaugh, Lelli & Schombert 2016, PRL 117, 201101 (arXiv:1609.05917)
  - Baryonic Tully-Fisher (BTFR): Tully & Fisher 1977, A&A 54, 661 ; McGaugh 2012, AJ 143, 40
  - MOND: Milgrom 1983, ApJ 270, 365 ; review Famaey & McGaugh 2012, Living Rev. Relativity 15, 10 (arXiv:1112.3960)
  - CMB: Planck 2018 results VI, A&A 641, A6 (arXiv:1807.06209)
  - Cosmic acceleration / dark energy: Riess et al. 1998, AJ 116, 1009 ; Perlmutter et al. 1999, ApJ 517, 565
  - DESI evolving dark energy: DESI DR2 2025, arXiv:2503.14738
  - Unruh effect: Unruh 1976, PRD 14, 870 ; Hawking radiation: Hawking 1975, CMP 43, 199
  - de Sitter / Unruh effective temperature: Deser & Levin 1997, Class. Quantum Grav. 14, L163
  - Holographic / entropic gravity: Bekenstein 1973, PRD 7, 2333 ; Verlinde 2011, JHEP 04, 029
  - MacDowell-Mansouri gravity-as-gauge: MacDowell & Mansouri 1977, PRL 38, 739
  - Relativistic MOND (AeST): Skordis & Zlosnik 2021, PRL 127, 161302 (arXiv:2007.00082)
  - UV/IR / degrees-of-freedom bound (CKN): Cohen, Kaplan & Nelson 1999, PRL 82, 4971 (arXiv:hep-th/9803132)
  - Lorentz violation tables (SME): Kostelecky & Russell 2011, Rev. Mod. Phys. 83, 11 (arXiv:0801.0287)
  - Lepton mass coincidence: Koide 1983, PLB 120, 161
`

const STYLE = `
HOUSE STYLE for every script (copy this preamble verbatim, then build the figure):
    import numpy as np, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
        "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
        "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
    C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs
    fig, ax = plt.subplots(figsize=(7,4.3))
    # ... compute purely from formulas / hardcoded published constants ...
    ax.set_xlabel(...); ax.set_ylabel(...); ax.set_title(...)
    ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig("FILENAME.png", bbox_inches="tight"); print("ok")
Use C_FW (purple) for the framework's own curve, C_NEWTON (grey, dashed) for the Newtonian baseline,
C_MOND (teal) for generic MOND, C_DATA (red) for any observational/illustrative band. Add a faint
text-credit in the lower corner only if it doesn't clutter. Log axes where physical (RAR, accelerations).
`

const RULES = `
HONESTY RULES (the author audits these):
  1. Every script is 100% SELF-CONTAINED: numpy + matplotlib only. NO file reads, NO network, NO external data.
     Compute every plotted value from an explicit formula or a hardcoded published constant.
  2. NEVER fabricate observational data and present it as real measurements. Every figure must be honestly one of:
       (a) FRAMEWORK-COMPUTED — plotted from the framework's own equations (a0=c^2*sqrt(Lambda/32pi)=9.36e-11,
           mu_fw(x)=(sqrt(1+4x^2)-1)/(2x), T_eff=(hbar/2pi c k_B)sqrt(a^2+(cH)^2), a0(z)/a0=sqrt(rho_DE(z)/rho_DE0),
           Z=sqrt(32pi/3)=5.789, kappa=1/2 geometry, gamma_slip=2 sqrt(1+a0/g)-1, BTFR v^4=G M a0, etc.);
       (b) PUBLISHED-RELATION — the functional form of a known empirical law (e.g. the RAR fitting function,
           the BTFR slope-4 line) drawn as a CURVE/MODEL and LABELED as the relation, not as data you hold;
       (c) SCHEMATIC — a clearly-labeled conceptual diagram (e.g. Keplerian-decline-vs-flat rotation shapes).
     The caption MUST state which of (a)/(b)/(c) it is. If you draw scattered "points," they must be generated
     from a stated model with stated synthetic scatter and the caption must say "illustrative, model-generated."
  3. Quarantine: a0, Z, kappa, and the SM/particle masses are NEVER described as "derived from first principles."
     a0's FORM is forced; its VALUE and kappa=1/2 and Z are inputs/geometry. Match the book's careful language.
  4. Numbers must be physically right: a0=9.36e-11 m/s^2, H0~70 km/s/Mpc, Z=5.789, kappa=1/2, Lambda~1.1e-52 m^-2.
`

const FIG_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    ch_num: { type: 'integer' },
    figures: {
      type: 'array', minItems: 1, maxItems: 3,
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          filename: { type: 'string', description: 'png basename, MUST start with chNN_ and end .png, lowercase, no spaces' },
          kind: { type: 'string', enum: ['framework-computed', 'published-relation', 'schematic'] },
          py: { type: 'string', description: 'complete self-contained matplotlib script that saves to the filename basename and prints ok' },
          caption_md: { type: 'string', description: 'markdown block: image embed + bold figure caption + a **Source:** line with REAL links' },
          anchor: { type: 'string', description: 'exact ~8-14 word verbatim substring from the chapter body to insert the figure AFTER, or the literal string END to place it just before the Summary' },
        },
        required: ['filename', 'kind', 'py', 'caption_md', 'anchor'],
      },
    },
  },
  required: ['ch_num', 'figures'],
}

phase('Figures')
const results = await parallel(chapters.map(ch => () =>
  agent(
`You are the figure editor for the academic-yet-friendly textbook "A Beautifully Geometric Universe" about Carl Zimmerman's emergent-gravity framework (a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2, a modified-INERTIA theory from de Sitter-Unruh thermodynamics).

TASK: Read the chapter file  book/${ch.file}  (use the Read tool). Then design 2-3 figures (charts/graphs/diagrams) that genuinely illuminate THIS chapter's specific content. Prefer 2-3 for substantive chapters; at least 1. For each figure produce a complete self-contained matplotlib script and an insertion markdown block.

Number the figures ${ch.num}.1, ${ch.num}.2, ... Filenames must start "ch${String(ch.num).padStart(2,'0')}_".

${STYLE}
${RULES}
${SOURCE_PALETTE}

CAPTION FORMAT (exactly this shape, fill in real content):
\`\`\`
![short alt text](figures/<FILENAME>.png)

***Figure ${ch.num}.N — <Title>.*** <1-3 plain-sentence caption: what the reader sees and the honest provenance — say "computed from the framework's equations" / "the published <X> relation plotted as a model" / "schematic illustrating <concept>".>

**Source:** Figure generated by [\`book/figures/<FILENAME>.py\`](https://github.com/carlzimmerman/zimmerman-formula/blob/main/book/figures/<FILENAME>.py). <Then the underlying source: for framework curves cite the repo + the matching Zenodo DOI; for background physics cite the matching real reference from the palette.>
\`\`\`
(The .py link must use the SAME basename as the .png. The image path in the embed is figures/<FILENAME>.png — relative to the book/ folder.)

Return ONLY the structured object (ch_num + figures[]). Make the scripts robust: they will be executed exactly as written from inside book/figures/. Test your formulas mentally; avoid anything that could throw (no divide-by-zero, guard logs, keep arrays finite).`,
    { label: `ch${String(ch.num).padStart(2,'0')}`, phase: 'Figures', schema: FIG_SCHEMA }
  ).then(r => r ? { ...r, ch_num: ch.num, file: ch.file } : null)
))

return results.filter(Boolean)
