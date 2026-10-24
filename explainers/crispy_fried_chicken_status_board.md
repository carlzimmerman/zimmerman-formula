# The Crispy Fried Chicken Status Board

**Crispiest recipe (v3s):** General relativity plus a preferred cosmic time (Khronon) and one extra field giving the simple MOND law (AQUAL, external-field effect included, κ fitted), switched off within L★ ≥ 22 pc by a stiffness that acts only where D·P ≥ 0, plus fitted cold dust; no settling or supply rules.

*Where the current theory, v3s, stands as of 23 October 2026. The board shows v3s only. The theory is not complete. The last plain-v3 board, before v3s was adopted, is kept as [`img/status_board_2026-10-23v3.png`](img/status_board_2026-10-23v3.png). The board before the PAPER60 audit's note corrections is kept as [`img/status_board_2026-10-23late3.png`](img/status_board_2026-10-23late3.png); before the coordinator's decisions on the night batch, as [`img/status_board_2026-10-23late2.png`](img/status_board_2026-10-23late2.png); before the S3, S4, H4 and U1 batch, as [`img/status_board_2026-10-23night.png`](img/status_board_2026-10-23night.png); before the P4 and Q6 recomputes, as [`img/status_board_2026-10-23late.png`](img/status_board_2026-10-23late.png); the first v3-only board, before the S1 and S2 recomputes, as [`img/status_board_2026-10-23eve.png`](img/status_board_2026-10-23eve.png). Earlier pictures, which mixed models, are kept as [`img/status_board_2026-10-23pm.png`](img/status_board_2026-10-23pm.png) (23 October afternoon), [`img/status_board_2026-10-23am.png`](img/status_board_2026-10-23am.png) (23 October morning), [`img/status_board_2026-10-22.png`](img/status_board_2026-10-22.png) (22 October evening) and [`img/status_board_2026-10-21.png`](img/status_board_2026-10-21.png).*

The theory makes one claim: the acceleration scale where galaxies stop obeying Newton, a₀, is set by the density of dark energy.

```
a₀ = κ · c · √(G ρ_Λ),   κ = ½   →   a₀ = 9.36 × 10⁻¹¹ m/s²
```

The ½ is **fitted**, not derived; the current measurement is κ = 0.417 ± 0.095 (CFG493). Every number is quoted on two footings, 9.3603 × 10⁻¹¹ and 1.1312 × 10⁻¹⁰ m/s², and the two are never pooled. The framework also needs a cold component, "cold energy", with Ω_c/Ω_b = 5.364 (an input). It is real gravitating mass, not a particle species; no dark-matter particle is added.

![Status board: every test of the current theory, v3, as a coloured tile](img/status_board.png)

## v3s adopted as the current theory (23 October, owner)

**v3s is v3 with the switched stiffness** −(γ_L/2)[max(D·P, 0)]². It adds no new constant. Source: lane [X3](../rebuild_2026_10_22/X3_switched_stiffness/README.md), commits 8aeba82a87 / 31febd3b70. The coordinator reran it: the main run is identical, and one D10 bracket regenerated from scratch matches 9,384 numbers to 1e-9. The whole theory is on one page in [`V3_FULL_PICTURE.md`](../covariant_push_2026_10_22/V3_FULL_PICTURE.md).

- **Why it was adopted.** v3 as written is Hadamard ill-posed wherever the khronon density is negative, which happens at every two-body saddle and in the external-field lobes ([H4](../rebuild_2026_10_22/H4_v3_saddle_stability/README.md)). The switched form removes that instability:
  - in the nonlinear 1D equations the khronon/dust pair has a sound speed c² = γ_L(D·P + ρ_d)Θ(D·P) ≥ 0;
  - a slab test with no approximations converges under resolution doubling, where v3 diverges;
  - the bound is certified point by point in Lean (`fable_independent_2026/lean_2026/V3_PICTURE_2026_10_23.lean`).
- **What it keeps.** v3s equals v3 wherever D·P ≥ 0, so every screened result carries over:
  - the Sun keeps D·P > 0, with a margin ≥ 1.8e4;
  - the strong-field rows all have D·P > 0.
- **Where the two differ.** Where a static solve has D·P < 0 lobes, X3 re-solved the outer globulars in full; the L★ floor moved by +0.006 %. The dwarf-satellite and Coma tiles (S1) were not re-solved, and their change is expected to be of the same size.
- **Qualifiers** (stated on the Health tile):
  1. the dust density must be ≥ −D·P inside stiff regions, which holds in the μ_K range S4 allows;
  2. at zero dust the interface is a knife edge, so numerics must be sign-consistent;
  3. H4's bounded growth remains at saddles (0.006–0.20 e-folds median). **The v3s lobes around outer globulars and satellites are RESOLVED BENIGN** (H5, `rebuild_2026_10_22/H5_v3s_lobe_growth`, 2cde8548ed / 568a6b6709, 11/11, rerun identical):
     - the PN system is Galilean-covariant, so the lobe pattern rides with the moving system while the host khronon streams through, spending 1–25 Myr in a lobe;
     - the khronon charge's sign is carried along with the flow, so the stream keeps D·P ≈ ρ̄_host > 0 there, which is the stiff side, with nothing to grow;
     - granted the static lobe anyway, N ≤ 0.048 (globulars), ≤ 0.013 (satellites) and ≤ 0.46 (pure radial orbit at apocentre);
  4. the D·P < 0 side's strong coupling: RESOLVED BENIGN (review `reviews/v3s_soft_side_strong_coupling_2026_10_23/`, d27e01f42e, 5/5): the soft-side khronon is a dispersionless fluid, ω² = Kρ_τ(M − 1); 'Λ = 0' came from putting c_π = 0 (the k → ∞ limit) into the relativistic scaling. With c_π(k) = ω/k, the strong-coupling length across all 320 H4 region values is 57 m–54 km, so the soft-side EFT holds on astrophysical scales. Open: classical nonlinearity of real khronon flows, ε_cl = k|v|/ω, possibly O(1) in Mpc bulk flows;
  5. 2D/3D evolution and a proof for a moving interface are open.

**Recoloured with X3 as evidence.** The generator's lane list gains exactly X3, and nothing turned green.
- **Health: ghosts, gradients: 🟥 → 🟨 conditional.** v3s is well-posed where ρ_τ < 0, under the qualifiers above. H4's unbounded rate applies to v3 as written.
- **Leaf problem well-posed: 🟥 → 🟨 conditional.** This is a correction as well as a recompute. H4 §5 states that C8's well-posedness verdict stands for the (P, lapse) leaf problem; H4's ill-posedness is in the khronon/dust evolution and belongs on the Health tile. For v3s, the switched leaf functional stays convex (an obstacle-type free boundary), so the leaf problem is still uniquely solvable (X3). The infinite-volume theorem and the coupled GR + dust problem remain open, as in C8.

## How to read it

The picture shows the current theory, v3, only. It is drawn by [`make_status_board.py`](make_status_board.py); tiles marked **23 OCT** were added, recoloured, greyed or re-annotated on 23 October. The generator refuses any first green except one listed in `VERIFIED_GREEN` (lane, result commit and the coordinator's rerun, with the same lane on the recolour step); a grey tile may also return to green if it was green before it was greyed and its own recompute lane passes it. It refuses any recolour not listed with its evidence lane, and any tile that leaves the board without going to the archive with N0 as its evidence (`--selftest` runs 26 broken cases, each of which must be caught, and checks that the one verified green passes). Each tile is one test. The colour restates a verdict recorded in the campaign LEDGER ([`campaign_fresh_gravity/LEDGER.md`](../campaign_fresh_gravity/LEDGER.md)) or in the dated notes of [`THEORY_CANONICAL_2026-10-18.md`](../campaign_fresh_gravity/THEORY_CANONICAL_2026-10-18.md), and the lane IDs on each tile point to the scripts that produced it. Verdicts come from committed scripts with pass/fail rules frozen *before* the data were read, plus a control that is deliberately broken and must fail. Where a colour depends on a rule added afterwards (post hoc), the tile says so.

| colour | meaning |
|---|---|
| 🟩 **pass** | the theory meets the test within the stated errors |
| 🟨 **conditional** | passes, but only under a stated assumption that is not yet proved |
| 🟦 **not decidable yet** | today's data cannot tell the theory from its rival |
| 🟥 **fails** | the theory misses the test, and audits from the raw data confirm the miss |
| ⬜ **open** | not yet answered, or waiting on data |
| ⬚ **not yet recomputed for v3** (light grey, dashed border) | the tile's lane computed an older model; its old result is kept in the note as "was …", and the tile names the lane that will recompute it for v3 |

## The board now shows v3 only (23 October)

The owner's rule: the board shows only the current best theory, and a failure on it must be a failure of that theory. A tile computed for an older model is recomputed, or shown as not yet recomputed for v3; it never keeps its old colour. Tiles that tested only retired models leave the board and are archived, labelled.

The read-only audit [N0](../rebuild_2026_10_22/N0_board_audit/AUDIT.md) checked each of the 55 tiles of the 23 October afternoon board against v3 ([`THEORY_V3_DRAFT.md`](../covariant_push_2026_10_22/THEORY_V3_DRAFT.md) §1–3). The board follows its classes:

- **Current (15 tiles): colour kept.** The evidence lane computed v3 itself. N0's re-annotations are applied: health cites C5 only; binary pulsars cite C8 only; the screened Cassini tile cites C6 and says that C6's frozen rule reads UNDECIDED on one float-rounding check; the unscreened control cites E2 only; matter conservation cites C4 (the identity holds for any diffeomorphism-invariant action); cluster cores say 326 clusters (F1) and drop H2; the no-go tile drops v4. Cluster cores and isolated lensing at all radii note that v3's μ_K²ψ term is not yet included (S4).
- **Not yet recomputed for v3 (15 tiles): grey, dashed.** The note keeps the old result as "was …", and the label names the recompute lane. The old colour is dropped. Five of these may change colour once recomputed (N0): isolated-galaxy lensing inside 0.31 Mpc, tidal dwarfs and DF2/DF4, the Milky Way's outer slope, Coma's ultra-diffuse galaxies and red lenses. The dwarf satellites were red; N0 expects them to stay red (v3's external-field effect can only raise the excess), but the +0.89 dex has to be recomputed. Galaxy groups were green; CFG543's no-edge row (+0.010 / −0.010) is v3's number, but the external-field check is still to do (S4).
- **Data-gated or open (9 tiles): kept.** ALMA, the Gaia DR4 Milky Way predictions and κ now name the v3 work they need (S3).
- **Old-model only (16 tiles): archived** (list below, and [`img/status_board_archive_retired.png`](img/status_board_archive_retired.png)). Three of them were in the generator's must-stay-red list. They now satisfy it only by sitting red in the archive with N0 as the evidence lane.

No tile turned green. The two v3 counterparts that were not yet tiles were "MW vertical force, AQUAL disc" and "CMB lensing, v3 linear" (Q6). The first is now on the board (P4, below); the second goes on once computed.

### Recomputed for v3 (23 October, evening)

Four grey tiles now carry v3 colours, each from its own recompute lane; the coordinator reran each lane and it reproduced. Three tiles were re-annotated without a colour change. Nothing turned green. Eleven tiles stay grey. The generator now also checks against the first v3-only board: a grey tile can take a colour only through a listed step from grey, naming its own recompute lane, and no tile of that board may be retired.

- **Dwarf satellites vs the screened law: grey → 🟥 fails** ([S1](../rebuild_2026_10_22/S1_v3_hosted_small/README.md)). With the host's external field solved in v3's AQUAL law, the excess is +1.33 / +1.30 dex at the L★ floor and +1.72 / +1.68 dex at 90 pc. The external field costs +0.58 dex: it widens the gap. The cold supply exists ([P1](../rebuild_2026_10_22/P1_dwarf_chemistry/README.md)), but there is no binding mechanism.
- **Coma's ultra-diffuse galaxies: grey → 🟥 fails** (S1). In Coma's measured field they sit +1.12 / +1.08 dex above v3, z_sys +4.3 to +4.7 (canonical) / +4.1 to +4.5 (alt). Isolated, they would be only 1.65 / 1.45σ off; the failure rests on equilibrium in the current field.
- **Isolated-galaxy lensing, inner: grey → 🟨 conditional** ([S2](../rebuild_2026_10_22/S2_v3_lowg_lensing/README.md)). v3 gives blue-lens A = 0.88 / 0.81 at the primary field (corrected by the PAPER60 audit; 0.80 was the alt zero-field cell); the external field adds at most 0.004 here. The verdict is decided by the hot circumgalactic gas and the stellar masses. S4's μ_K² term is not yet in (since computed: see the PAPER60 audit section).
- **Red (early-type) lenses: grey → 🟨 conditional** (S2). The inventory alone is 1.31 / 1.20 short; with CFG667's perturbers and the IMF α–σ relation (CFG926) it is 1.02 / 0.93.
- **Isolated-galaxy lensing, all radii: stays 🟦 not decidable yet**, now with [P2](../rebuild_2026_10_22/P2_spec_isolated_lensing/README.md). Spectroscopic isolation leaves too few lenses (about 22,000–26,000 needed). The data favour the catalogue's external field over none. S4's μ_K² term is still to add (since computed: see the PAPER60 audit section).
- **Dwarf cold supply (chemistry): stays 🟨 in the archive**, with P1 added. The test on the satellites' own metallicity distributions confirms the supply for the median system, but not robustly at 2σ. The tile stays archived: v3 has no supply rule.
- **One selector for the family: stays ⬜ open.** M2's screened tidal charge fails; T1 is testing the external field's strength (no result yet).

### Recomputed for v3 (23 October, late evening)

Two more lanes landed, and the coordinator reproduced both: [P4](../rebuild_2026_10_22/P4_v3_galaxy_tiles/README.md) (rerun identical except for peak memory) and [Q6](../rebuild_2026_10_22/Q6_v3_class/README.md) (the sympy derivation, 19/19 identical). Seven tiles stay grey. Galaxy groups return to green: they were green before they were greyed, and P4's frozen verdict passes them. The generator allows a grey tile back to green only in that case; no tile is green for the first time.

- **Rotation curves (SPARC): grey → 🟨 conditional** (P4). With one Υ per galaxy and the external field solved for 109 galaxies, the rms is 0.054 / 0.054 dex. The median Υ is 0.52 / 0.44; the alt value is below the 0.50–0.80 window. The χ² line fails on both footings (63–64% of galaxies acceptable), and ν_mono does no better.
- **Local a₀ from MeerKAT: stays 🟩 pass, recomputed** (P4). a₀ = 1.31 × 10⁻¹⁰ m/s², against 1.21 × 10⁻¹⁰ from SPARC with the same recipe: +0.032 dex (corrected by the PAPER60 audit; it was double-rounded to +0.033), inside the 0.15 dex line.
- **Galaxy groups: grey → 🟩 pass, the lane's verdict for isolated groups** (P4). On baryons with no supply rule they sit +0.010 / −0.010 dex from the law (Z ±0.31). They would sit above the law if the external field were g_e ≥ 0.03 a₀ (Z 4.7 / 4.5), and no measured group field is on disk.
- **MW vertical force: back from the archive → 🟥 fails** (P4). v3 has no round rule. As an AQUAL disc, K_z at 1.1 kpc is 92.3 / 96.9 against 66.4 ± 2.2 (χ² 178 / 251 against 67.5), for all four baryon models. The tile keeps its old name, "(round rule)", because the generator allows a rename only with N0 as evidence.
- **Tidal dwarfs and NGC 1052-DF2/DF4: grey → 🟥 fails** (P4). With the host field solved, the tidal dwarfs sit −0.59 / −0.62 dex below v3, and DF2/DF4 −1.66 / −1.74 in ln. v3 has no capture rule.
- **Native CMB: grey → 🟥 fails** (Q6). Literal v3 has no radiation era: the stiff a⁻⁶ term of the BS quadratic K wins. On a dust background, plik-lite gives Δχ² = +13,891 against ΛCDM at the BS cap and +18.7 at μ_K = 2542 h/Mpc.
- **Linear growth, v3 Khronon: stays 🟥, Q6 added.** The Boltzmann calculation gives σ₈ = 0.061 at the cap (F3's ODE gave 0.391). Reaching 95% of ΛCDM growth needs μ_K > 2542 h/Mpc.
- **Not drawn: "BBN / radiation era (literal K)"** (Q6). The stiff term beats radiation before z ≈ 1854–3.2 × 10⁵. BBN needs μ_K ≥ 1.84 × 10⁸ h/Mpc, 1.2 × 10⁷ times the BS cap. BS25's DBI K is the literature cure (lane Q7, open). The generator refuses a tile that was on no earlier board, so this one is recorded here and in Q6, and not on the picture.

### Recomputed for v3 (23 October, night)

The coordinator reran and reproduced every lane in this batch: [S3](../rebuild_2026_10_22/S3_v3_mw_seals/README.md), [S4](../rebuild_2026_10_22/S4_v3_muK_clusters/README.md), [P3](../rebuild_2026_10_22/P3_v3_strong_field/README.md), [H4](../rebuild_2026_10_22/H4_v3_saddle_stability/README.md), [U1](../rebuild_2026_10_22/U1_v3_dust_content/README.md), [Q7](../rebuild_2026_10_22/Q7_bs25_cosmology/README.md) and [T1](../rebuild_2026_10_22/T1_efe_strength/README.md). Nine tiles changed colour. The green guard first refused three items; the coordinator then decided them (below). One tile stays grey. Notes may now run to four lines.

- **MW outer slope (Gaia): grey → 🟥 fails** (S3). The shape is excluded: the law's slope is −0.126 / −0.114 against the data's −0.325 (Z −4.37 / −4.62). The algebraic law, ν₁, the AQUAL disc and the external field all fail.
- **Central ellipticals (SLUGGS): grey → 🟦 not decidable yet** (S4, R4 with v3's ν₁). The class is unchanged, so the tile returns to its colour before greying. The tension rises from 2.8σ to 3.1σ (3.3σ without ownership).
- **High-z on halo-free inputs: grey → 🟦** (S4). All six CFG303 classes are unchanged; s★ moves by at most 0.1 dex.
- **CRISTAL z ≈ 5 / ALESS 122.1: grey → 🟦** (S4). NOT ROBUST and NOT DISCRIMINATING, unchanged.
- **Health: 🟨 → 🟥 fails** (H4). There is a gradient instability wherever the khronon density ρ_τ < 0, which happens at every two-body saddle and in the external-field lobes. Its rate Γ = L★k√(2πG|ρ_τ|) is unbounded, and the γ_L screening term drives it. The Solar System is healthy.
- **Leaf problem: 🟨 → 🟥 fails** (H4). The problem is ill-posed at saddles. C8's leaf result holds only where ρ_τ ≥ 0.
- **Black holes (EHT, LIGO ringdown): grey → 🟨 conditional** (P3; the coordinator's decision). Static, non-rotating holes pass: the shifts are ≤ 3 × 10⁻¹¹. Regular holes need an infalling khronon. Rotating and moving holes are open.
- **Strong coupling: grey → 🟨 conditional** (P3; the coordinator's decision). It is an estimate: the loop factor is ≤ 1.3 × 10⁻³, with only 1.7× margin in k at Eöt-Wash's 38.6 μm. Tests below 5 μm would probe it.
- **Tidal dwarfs and NGC 1052-DF2/DF4: 🟥 → 🟩 pass** ([U1](../rebuild_2026_10_22/U1_v3_dust_content/README.md), result 54ee83e54e; the coordinator's rerun reproduced main 15/16 and A2 6/6). This green comes from a new derivation, not a re-scored number.
  - Static AQUAL (P4) read −0.59 dex.
  - v3's own dynamics make a hosted system dust-free: held dust is weightless in its host (theorem T3), so a system falling with its host is Newtonian. Then the tidal dwarfs sit +0.055 ± 0.114 dex and DF2/DF4 +0.30 / −0.24 in ln from v3, with no knob.
  - It is the only first green on the board. It passes through `VERIFIED_GREEN`, a narrow route that names the lane, the result commit and the coordinator's rerun. The recolour step into green must name the same lane. Every other first green is still refused (selftest cases 24–26).
  - The same theorem is why the dwarf satellites fail (+2.0 dex): read the pass and the fail together.
- **Radiative stability stays grey.** P3's README gives no replacement for it.
- **Notes only, colour kept:**
  - Dwarf satellites: +2.00 / +1.99 dex under v3's own dynamics, dust-free (U1). This is structural: the dust coupling would have to change.
  - Coma's ultra-diffuse galaxies: +1.41 dex, z 5.4 (U1), also structural.
  - Cluster cores: no allowed μ_K fixes them (0 of 1,804 cells). A small μ_K leaves the clusters unchanged, and a large one wrecks galaxies first (S4).
  - Native CMB and linear growth: BS25's DBI K fixes BBN only; growth R_B is 0.26–0.32, and BS ran no Boltzmann code (Q7).
  - One selector: no single external-field strength fits (p 0.023 / 0.014). Coma wants it weak, P2's lensing wants it strong, and the satellites sit +0.9 dex high even at ε = 0 (T1).
  - Cold-mass amount: held dust ≤ the phantom density (U1, theorem T1), and hosted systems carry none (T3).
  - Gaia DR4 MW predictions: v3's file is sealed (S3: `SEALED_V3_MW_DR4.json`, 15b7e6ff…). A new observable is the asymmetry in V_c driven by the external field: 3 / 5 / 8 % at 20 / 30 / 60 kpc.
  - ALMA: addendum F is filed (f6f0ba66a4) with v3's AQUAL-disc reading, and the v3aq harness has passed its MOCK test.
  - κ: on AQUAL discs, κ_Λ = 0.499 ± 0.116 and κ_crit = 0.413 ± 0.096 (S3). These are consistent, but they do not discriminate.

### Notes corrected by the PAPER60 audit (23 October)

The working note PAPER60 (`qwen_claude_field_theory/papers_2026/`, audit 249/249 against the lane JSONs) re-read every number on the board. Four notes are corrected. No colour changed, and the guards, self-test and mutation control all pass.

- **Local a₀ from MeerKAT:** +0.032 dex, not +0.033. P4's raw value is 0.0325, which had been rounded twice.
- **Isolated-galaxy lensing, inner:** blue-lens A = 0.88 / 0.81 at the primary field. The 0.80 was the alt footing at zero external field. S4 now gives the tile's range: the μ_K² term leaves isolated galaxies alone only for μ_K < 0.1 Mpc⁻¹.
- **Isolated-galaxy lensing, all radii:** S4 has computed the μ_K² term. It ruins isolated-galaxy lensing for every μ_K ≥ 0.1 Mpc⁻¹ (Δχ² +110 / +190 at 0.1 Mpc⁻¹). The colour stays not decidable for small μ_K.
- **Gravity waves at light speed:** the tensor modes travel at c exactly. P3 corrects the old note's "only the 2 tensor modes propagate": where D·P > 0 the khronon/dust pair also propagates (about 10⁻⁴ c in the Solar System), with a metric coupling of at most 2.3 × 10⁻⁹. So C8's binary-pulsar result stands.

### Recompute lanes

N0's recompute batches run as these lanes (all small: one thread, under 1 GB). The heavy one is L1.

| lane | what it computes for v3 | tiles |
|---|---|---|
| P4 | AQUAL with v3's kernel and the external field solved, for galaxy tiles | rotation curves (SPARC); local a₀ from MeerKAT; galaxy groups; MW vertical force; tidal dwarfs and DF2/DF4 (done 23 October) |
| S1 | small systems in their host's field (AQUAL + stiffness at L★ 24 / 90 pc, external field solved) | dwarf satellites; Coma's ultra-diffuse galaxies; feeds the family selector (done 23 October: both fail) |
| S2 | galaxy–galaxy lensing at low acceleration (F2's AQUAL solver, external field) | isolated-galaxy lensing, inner; red lenses (done 23 October: both conditional) |
| S3 | discs as AQUAL with v3's kernel | the Milky Way's outer slope; κ re-fit; a new sealed Gaia DR4 Milky Way file (before 2 December); v3's ALMA disc reading (before 6 November) (done 23 October) |
| S4 | v3's static μ_K²ψ (dust) term on clusters and the outer-lensing stack; kernel-only swaps | cluster cores and isolated lensing at all radii (caveat); central ellipticals; high-z; CRISTAL / ALESS (R4 and the cluster no-go done 23 October; the outer-lensing stack not yet) |
| P3 | the relativistic sector: strong coupling, black holes, ringdown, neutron stars | strong coupling; black holes; radiative stability (done 23 October: strong coupling and black holes conditional; no radiative-stability result) |
| Q6 | a Khronon-v3 CLASS patch (TT/EE/φφ, P(k)) | native CMB (done 23 October: fails); CMB lensing, v3 linear |
| L1 | heavy | the Khronon-native PM run ([frozen 512³ plan](../rebuild_2026_10_22/L1_khronon_pm/FROZEN_CRITERIA.md)) | v3's nonlinear growth and shear, which stand in for 5 archived tiles; the one open escape of "Covariant completion" |

## Archived: retired models

These tiles tested only models that v3 does not contain (16 retired by N0; the MW vertical force returned to the board on 23 October, recomputed for v3 by P4). Their colours are the 23 October afternoon colours, kept for the record; they are not verdicts on v3. Each was retired on N0's evidence. Picture: [`img/status_board_archive_retired.png`](img/status_board_archive_retired.png).

| tile | old colour | lanes | why it left the board | v3 counterpart |
|---|---|---|---|---|
| v4 well-posedness | 🟥 fails | I1 | v4 (AeST + γ_L) is not the best theory | leaf problem well-posed (C8) |
| Lapse condition, realistic matter | 🟩 pass | CFG312 | the lapse kernel of the filtered C-H/K chassis | inside C8's convex leaf functional (optional check, P3) |
| Structural order (G0) | 🟨 conditional | CFG329 | a gate of the filtered C-H/K chassis; duplicates health and the leaf problem | health (C5) + leaf problem (C8) |
| Zero-field nonlinear, ungated | 🟥 fails | CFG358 | the ungated ν_mono chassis on open FRW | L1's native nonlinear run |
| Globulars + ownership rule | 🟨 conditional | CFG332, CFG333 | ownership classes; v3 has no ownership | outer globulars, L★ floor (D10) |
| Dwarf cold supply (chemistry) | 🟨 conditional | E6, P1 | catchment supply; v3's dust has no supply or capture rule. P1 (23 October): the MDF test confirms the supply for the median, not robust at 2σ | dust capture into satellites (L1) |
| Cosmic shear, native inputs | 🟨 conditional | CFG654-A2, CFG654-A3, CFG909 | the theory-v2 engine (switch, catchment, census edge, settling, QUMOND phantom), which has no parent | F3's linear S₈ and L1's native run |
| Native shear rerun (CFG960) | ⬜ open | CFG960 | the SCT-M engine, not v3. Since scored: SC1x FAILS, KiDS EXCLUDED, Δχ² +47.28; SC2x not run | L1's native run |
| CMB lensing (Planck PR4) | 🟦 not decidable yet | CFG917, CFG927 | theory-v2 runs | C_L^φφ from the v3 CLASS patch (Q6) |
| Growth, zero-knob supply rule | 🟥 fails | CFG555, CFG556, F3, G1 | the settling engine; v3 has no settling | linear growth, v3 Khronon (on the board, 🟥) |
| Linear growth, v4 AeST | 🟥 fails | C7, H1, H3 | v4 is not the best theory | linear growth, v3 Khronon |
| Structure growth, chassis alone | 🟥 fails | L341 | the C-H/K chassis with an unfloored boost on all matter | linear growth, v3 Khronon |
| Ownership from an action | ⬜ open | CFG945, CFG950, CFG953 | the label sector; v3 has no ownership and needs none | none needed |
| Physical parent of the shear engine | ⬜ open | CFG951, CFG954, CFG955 | the parent of the theory-v2 engine; v3 is not it | none needed |
| Energy books of settling | ⬜ open | CFG932, CFG935 | v3 has no settling | none needed |

## What changed on the 23 October afternoon board (before the v3-only rebuild)

Four lanes landed after the morning board: I1, J1 and K1 in [`rebuild_2026_10_22/`](../rebuild_2026_10_22/BRIEF.md), and step N of [C7](../covariant_push_2026_10_22/C7_aest_class/README.md). The summary is §1b of [`THEORY_V3_DRAFT.md`](../covariant_push_2026_10_22/THEORY_V3_DRAFT.md). One tile changed colour; nothing turned green.

- **Linear growth, v4 AeST: 🟨 → 🟥** (C7). On FRW it runs away: P/P_ΛCDM reaches 10²–10⁴¹ by k = 10 h/Mpc, for the dust shape tried. The result is gauge- and tolerance-stable. The escape through a different early K-shape is untested.
- **New tile: v4 well-posedness 🟥** (I1). v4 is ill-posed wherever the aether twists, which is everywhere off exact symmetry. Relayed signals can close loops in time. No healthy completion was found.
- **One selector for the family stays ⬜ open, re-annotated** (J1, K1). The potential-depth selector fails (J1). The owner's idea that cold energy is "a dip into another dimension", tested as the braneworld Weyl term, also fails (K1); its tidal-charge form comes closest on the clusters.
- **New tile: covariant completion 🟥** (I1, C7, F3). The trilemma: Solar-System screening needs γ_L; γ_L is well posed only with an untwisted aether; the untwisted form (v3) fails linear growth. The one open escape is a native nonlinear v3 run.

## What changed overnight (23 October)

Every item is a committed lane in [`rebuild_2026_10_22/`](../rebuild_2026_10_22/BRIEF.md). The v4 candidate (AeST plus the same stiffness term and the exact-law free function) is §1b of [`THEORY_V3_DRAFT.md`](../covariant_push_2026_10_22/THEORY_V3_DRAFT.md). PAPER59 (the covariant theory) is published: DOI [10.5281/zenodo.23585319](https://doi.org/10.5281/zenodo.23585319). One tile changed colour; nothing turned green.

- **Cluster cores stay 🟥, now a real failure.** Rebuilt from the raw eRASS1 × KiDS data, the core excess is 1.68–1.85× (canonical) / 1.54–1.70× (alt) over the law, Z ≈ +5–6 (F1). AeST's own dust has the wrong radial shape to supply it (H2).
- **Isolated-galaxy lensing, all radii: 🟥 → 🟦 not decidable yet** (F2). The frozen failure is not robust: the strict "isolated" sample still leaks satellites' hosts, and the old Δχ² of +100 came from the supply edge, which v3 and v4 do not have.
- **Growth under the zero-knob supply rule stays 🟥** for the old settling engine. The excess belongs to the settling rules, not to v3 or v4 (F3), and it grows with grid resolution (G1).
- **New tile: linear growth, v3 Khronon 🟥.** J′(0) = −1 removes the linear Newtonian term, and the window for the K(Q) mass is empty (F3).
- **New tile: linear growth, v4 AeST 🟨.** The Newtonian term survives on large scales for any free function (H1). Pending: nonlinear behaviour and the native CMB. Open: the contact-term binding between about 1 Mpc and 4 kpc (H3).
- **Health stays 🟨.** v4 is ghost-free at linear order; the criterion that flagged it also flags ordinary self-gravitating dust (H3).
- **Dwarf satellites stay 🟥.** Pre-infall retention fails on native inputs; it closes only with a ΛCDM-processed subhalo mass put in by hand (G2).
- **"Law + a¹ growth + no external-field effect" stays 🟥**: the no-go stands. v4 evades it by having an external-field effect, and its growth is conditional at linear order (H1).

## What changed since 21 October (doors push, audit wave, covariant push; 22 October)

Every item below is a committed lane whose script the coordinator reran and reproduced. Full statement:
[`covariant_push_2026_10_22/THEORY_V3_DRAFT.md`](../covariant_push_2026_10_22/THEORY_V3_DRAFT.md).
Papers: PAPER58 v1.1, DOI [10.5281/zenodo.23579379](https://doi.org/10.5281/zenodo.23579379); PAPER59 (the covariant theory) in draft.

- **Column 1 (chassis) has a new candidate, and a healthy one.** The relativistic theory is now the Blanchet–Skordis
  Khronon theory (arXiv:2404.06584) in its literal form, plus the covector P and one stiffness term −(γ_L/2)(D·P)².
  - Its static limit is AQUAL with μ = x/(1+x), exactly (E2, C4). The field equation is AQUAL, not QUMOND: earlier
    lanes that used QUMOND understated the unscreened Cassini failure.
  - It is conditionally healthy (no ghost, no gradient instability; only the two tensor modes propagate, at c) and its
    leaf problem is well posed (C5, C8). DSF-21's A33 with a P kinetic term (η > 0) is **ill-posed** and is dropped.
  - Cost: P and the khronon are instantaneous constraints. That meets the owner's criterion B and **violates criterion A
    (v ≤ c)** by a real but unmeasurably small signal (C8). Binary pulsars and GW170817 do not constrain it.
  - The stiffness term and the J that gives μ = x/(1+x) are additions to the published theory (C1, C3, C4).
- **Control tile (22 October, evening):** the red "Unscreened law vs Cassini" tile is labelled a *control*: it is the same test with the screening switched off, and its failure shows L★ > 0 is required. It is not a failure of the screened theory, whose Cassini tile is green.
- **🟩 Cassini and the planets pass for the screened theory**: Q₂ is 2.8×10⁷–5.1×10⁹ inside Hees and Park; at
  L★ = 24 pc Mars sees 0.17 of its bound (C6, D7d). The **unscreened** law fails Cassini by 2.4–5.2× (E2), and no
  unscreened member of the record's law family passes both Cassini and SPARC (D7c).
- **🟨 Globulars → L★ floor, measured with the field solved**: L★ ≥ 21.7 pc (canonical) / 22.9 pc (alt) with the SPS
  M/L prior; 3–24 pc across M/L priors (D10). The unscreened law is excluded in every case.
- **Dwarf satellites** (the tile stays 🟥; the cold-supply tile is 🟨): +0.89 dex above the screened prediction (not +2.15 dex above Newton, E3). The theory's
  dynamics cannot fix a satellite's cold supply; the satellites' own chemistry says it is there, conditional on wind
  metallicity and no pre-enrichment (E6).
- **Gaia DR4 (December 2026) is now a clean decider**: screened γ_v − 1 ≈ 8×10⁻⁶ vs law-first (AQUAL) 1.167 / 1.199;
  scored on the whole catalogue under the owner's σ_sys rule (pre-DR4 note, amendment A3).
- **ALMA**: addendum E adds the n = 1 and n = 2 laws as labelled parallel readings (harness ready, MOCK-tested); both
  discs are expected to be unscorable (D4).
- **Native CMB**: a patched CLASS (AeST sector) is built and validated against pristine CLASS to 2×10⁻⁶ (C7); spectra
  not yet run. It tests the dust sector and G_cosmo/G_N only — a₀ is absent from the CMB at linear order (C2).
- **Native shear (CFG960)**: the memory fix (amendment A6) worked; the 1024³ canonical run is past its old failure
  point. No verdict yet.
- **Column 5**: κ is not derived — no horizon construction gives ½ without hand-picking it, and the "thermal" Z/4π is
  Milgrom's relation, a postulate (D5, A75). The dust abundance is an initial condition (C2, C4). L★ is a new fitted
  constant (C3). The skew-sign test of n = 1 vs n = 2 is retired (D1).
- **The picture, tile by tile (22 October evening).** No tile changed colour: no committed 22 October lane passes or fails
  a tile that the 21 October board scored differently, and nothing was turned green. Tiles added (new colour on the board)
  or re-annotated (colour kept), each with its lane:
  - Column 1, re-annotated to the Khronon literal form: gravity waves at c 🟩 (C5, C8); health 🟨 (C5); leaf problem
    well-posed 🟨, weak field only (C8); binary pulsars + GW170817 🟩 (C8); Solar System + Cassini, screened 🟩 (D7d, C6;
    C6's own frozen rule reads UNDECIDED on one float-rounding check).
  - Column 1, added: causality 🟨 "criterion B met, criterion A violated" (C5, C8); unscreened law vs Cassini 🟥 (E2, D7c).
  - Column 2, added: outer globulars, L★ floor 🟨 (D10). The older globulars + ownership tile is kept.
  - Column 3: the Local Group dwarfs tile is re-scored against the screened prediction and **stays 🟥** (E3, E6): +0.89 dex
    above it, and both lanes find no mechanism in the record that packs the cold energy inside the half-light radius.
    Added: dwarf cold supply from the satellites' own chemistry 🟨, conditional on ζ = 1 winds and no pre-enrichment (E6).
  - Column 4, added: native shear rerun ⬜ running (CFG960); native CMB ⬜, validated, spectra pending (C7, C2).
    Re-annotated: ALMA ⬜, harness ready, expected unscorable (D4); Gaia DR4 wide binaries ⬜, screened γ_v − 1 ≈ 8×10⁻⁶ vs
    AQUAL 1.167 / 1.199 (C6, E2, D2).
  - Column 5: κ ⬜ fitted (D5); new tile L★ ⬜ fitted (C3, D10); cold-mass amount ⬜, dust abundance an initial condition (C2, C4).
  - **Still 🟥, being re-examined by the rebuild lanes F1–F3** ([`rebuild_2026_10_22/`](../rebuild_2026_10_22/BRIEF.md)):
    cluster cores (F1), isolated-galaxy lensing at all radii (F2), growth under the zero-knob supply rule (F3), and the
    no-go "law + a¹ growth + no external-field effect" (F1–F3). No rebuild verdict exists yet.
- **Corrected in the record**: the native H₀ is 67.2–68.6 (the ordinary Hubble tension), not 55–57.5 (C2; PAPER58 v1.1).

## What changed since 9 October

- **Cosmic shear moved from "context only" (blue) to conditional (yellow).** Run from the framework's own early-universe inputs, the structure-formation engine is CONSISTENT with raw KiDS-1000 on both footings (CFG654-A2, CFG654-A3). The class is robust; the size of the lead is amplitude-driven (CFG909).
- **The condition is the engine's missing parent.** The engine behind the shear pass has no known physical parent (CFG941, CFG944, CFG946, CFG947, CFG950–CFG955). Two new tiles in column 5 say so.
- **Dwarfs and cluster cores turned red.** The old "Andromeda + Local Volume dwarfs" pass, the old "Milky Way ultra-faint dwarfs" conditional and the old "clusters, Bullet Cluster" pass are replaced by the excess family (new column 3): dwarfs and cluster cores fail (CFG919, CFG922, CFG929). Coma's ultra-diffuse galaxies cannot be decided yet (CFG933, CFG948), and red lenses are conditional on their stellar IMF (CFG926).
- **Isolated-galaxy lensing (KiDS) was split in two.** The inner shortfall that made the old tile blue is repaired by the catchment supply (CFG804, CFG902), so the inner tile passes. At all radii the prediction falls short, and the framework's two-halo term closes only part of the gap, so that tile fails (CFG902, CFG903).
- **New conditional tile:** tidal dwarfs and NGC 1052-DF2/DF4 sit at the Newtonian expectation (CFG936, CFG939).
- **a₀(z) uses the framework's own BAO ruler now** (CFG689). It is still blue: the data cannot decide yet.
- **Gaia DR4 kill line restated** (owner decision, 21 October; CFG943). The DR4 tile stays open.
- **ALMA scoring fixed before the data:** the original frozen plans govern, and one disc excludes no model (owner decision, 20 October; CFG942).
- **Other new tiles:** CMB lensing (blue, CFG917), one selector for the excess family (open), the energy books of settling (open, CFG932, CFG935) and the owner's wave a₀(z) idea (open, CFG956, CFG957).
- **κ** is quoted at its current measured value, 0.417 ± 0.095 (CFG493); it is still fitted.
- **Unchanged:** column 1 and every galaxy tile not named above.

## Column notes up to 22 October (mixed models; kept for the record)

*These notes predate the v3-only board. Many describe tiles that are now archived or not yet recomputed for v3 (the sections above). Where they differ from the picture, the picture and the v3 sections above govern.*

### Column 1 · The relativistic theory (the "chassis")

*Unchanged since 9 October.* This is the full field theory underneath the law: general relativity plus a preferred time direction (a "khronon"). It has to behave like Einstein's gravity wherever Einstein's gravity has been tested.

- **Passes:**
  - gravitational waves travel at exactly light speed;
  - realistic matter keeps the equations well behaved;
  - binary pulsars, with a 490,000× margin;
  - solar-system tests;
  - matter is exactly conserved (G9).
- **Conditional:**
  - well-posedness, in two forms (high-frequency and full nonlinear);
  - strong coupling;
  - structural order (G0): no runaway "ghost" mode, but solvability in the strongly nonlinear regime is unproved;
  - **black holes.** EHT shadows and LIGO ringdowns are matched to better than one part in 10⁹. A *moving* black hole keeps a hidden, Planck-scale defect on its innermost horizon. A 2019 paper's standard would count that as fatal; the owner's reading of it is still pending.

- **Fails, for the ungated chassis only: zero-field nonlinear dependence (G5/G10).** This 1-D test runs the bare relativistic chassis with the law switched on everywhere, including the smooth, expanding cosmic background, where the field is near zero. In that setting the sensitivity to tiny perturbations does not level off at the larger perturbation on the finest grid (N = 2047, CFG358, a knife-edge call). **It does not test candidate B, your live model:** there the law is switched off outside bound halos, so it never acts on that background. Candidate B's full action does not exist yet, so for B this is untested, not passed. This sits alongside the ungated chassis's growth failure in Column 4.

### Column 2 · Galaxies

- **Passes:**
  - **rotation curves.** On raw SPARC the weighted scatter about the law is 0.101 / 0.099 dex, with one global mass-to-light ratio (CFG695). No rotating system carries an excess (CFG919);
  - a₀ measured locally with MeerKAT, 0.9–1.3 × 10⁻¹⁰ (PAPER40);
  - **lensing of isolated galaxies, inside 0.31 Mpc.** The catchment supply suffices with no free parameter (CFG804; rerun with declared units, CFG902; still with the two-halo term, CFG903). Isolated blue (late-type) lenses at the dwarfs' own accelerations sit on the law, A = 1.016 ± 0.086. Under its robustness rule that result is fragile, so read it as "within ~0.1 dex" (CFG829, CFG840);
  - galaxy groups (CFG540/543);
  - the Milky Way's vertical force: round cold energy beats MOND's flattened phantom disc in 32 of 32 cells (CFG516). This separates the theory from MOND, and Gaia DR4 tests it directly.
- **Fails: lensing of isolated galaxies at all radii.** Beyond ~0.4 Mpc the predicted signal falls short (Δχ² +100.1 canonical after a unit fix, CFG902). The framework's own two-halo term closes 57–59% of the gap, but not under stricter isolation (CFG903, PARTIAL).
- **Conditional: tidal dwarfs and NGC 1052-DF2/DF4.** They sit below the law, at the Newtonian expectation (the six tidal dwarfs at −0.69 dex, CFG936). The framework puts them there only by giving them no cold energy. A system that moves through the settled medium faster than its own baryonic escape speed captures none (derived, CFG939). That matches, but the prediction rests on each system's label (debris or primordial), not on an out-of-sample test (CFG936).
- **Conditional: globulars and the ownership rule** (CFG332/333), unchanged.
- **Conditional: Local Group timing.** The earlier 13.5σ miss came mostly from treating the orbit as radial with measurement errors only. With Andromeda's sideways motion it drops to about 2–3σ, and a derived shared cold-energy supply between the two galaxies removes most of the rest. About 4σ remains on the old straight-line statistic (CFG522).
- **Tension: the four central ellipticals (SLUGGS).** With each galaxy's measured globular-cluster profile and orbits, the gap is about +0.07 dex on average, 2.8–3.5σ statistical only (CFG528b). Heavier stars, hot gas and the cold-energy edge all fail to close it. It is not a foreground effect.
- **Not decidable yet (DR4): the Milky Way's outer slope.** At census baryons the law fits the speeds, but Gaia's 15–27 kpc decline is 3–5σ steeper than the law (CFG532b). A standard dark-matter halo fails the same test (3.4σ). The result rests on a disputed distance scale, and Cepheids stay flat. In external galaxies seen through their gas, the law predicts outer slopes with no bias (153 SPARC galaxies, CFG533), so the tension is specific to the Milky Way: how we measure it from inside, or its current disturbance. DR4 fixes the distance scale.

### Column 3 · The excess family (new)

Every system with an excess over the law is pressure-supported, and no rotating system has one. Pressure support alone does not set the amount (CFG919). The family is **open**: the record has no mechanism for it.

- **Fails: Local Group dwarfs.** The 83 Local Volume dwarfs (Milky Way and Andromeda satellites, field dwarfs and ultra-faints) sit +0.37 / +0.33 dex above the law (CFG919).
  - The excess is not an estimator artefact, and an external-field effect would only raise it (CFG925).
  - Satellites of the two hosts carry it alike (CFG843).
  - With the framework's own cold-energy supply, the Milky Way's ultra-faints stay at the bare law, +0.325 / +0.304 dex short of what they show (CFG930).
- **Fails: cluster cores.** Raw KiDS lensing stacked on 318 eRASS1 clusters sits at 1.91 / 1.75 times the law inside ~1 Mpc. The outskirts (1.2–3 Mpc) match the law, but the outer signal scales with gas mass the way Newton does, not the way the law does (CFG687).
  - The baryon census cannot supply the core excess (CFG922).
  - No small reframing removes it. It is real mass the law does not supply (CFG929).
  - Treating cluster cold energy as untethered fits at its primary corner, but only at 6 of 40 corners (fragile). It is CDM-like cluster physics (CFG949).
  - The Bullet Cluster's sub-cluster core is undecided under the rules tested (CFG916, CFG951).
- **Not decidable yet: Coma's ultra-diffuse galaxies.** They sit +0.33 dex above the law, at 2.4–2.6σ in a fragile test (CFG933). The framework allows them at most the law itself, and today's data cannot separate the two (CFG948, control-limited). A purely Newtonian reading is excluded at 5.45σ (CFG948).
- **Conditional: red (early-type) lenses.** Their excess is not caused by neighbours (CFG912). A literature IMF α–σ relation removes it on both footings, provided disc galaxies stay near a Chabrier IMF. That condition is untested, so this may be a stellar-population effect, not cold energy (CFG926).
- **Open: one selector for the whole family.** No one-constant rule reproduces dwarfs, red lenses and cluster cores together: not a density threshold, a kinematic measure, velocity-space capture or late binding (CFG914, CFG919, CFG921). After the IMF correction, one velocity-scale selector fits the galaxy-scale facts but fails the clusters. That re-grade was post-hoc-motivated (CFG928).

### Column 4 · Cosmology, and does a₀ change over cosmic time?

The framework's a₀ follows the dark-energy density. With the framework's own BAO ruler (native sound horizon 147.07 Mpc), DESI BAO plus Pantheon+ give a₀(z)/a₀(0) = 0.91 [0.76, 1.03] at z = 1, 0.94 [0.71, 1.12] at z = 1.5 and 0.91 [0.33, 1.21] at z = 2.33. That is close to a flat line, while the rival a₀ ∝ H(z) gives 1.76, 2.35 and 3.49 (CFG689). Constant dark energy is not rejected (1.97σ). BAO cannot separate the framework from ΛCDM.

![a₀ against redshift: flat line versus the a₀ ∝ H(z) rival](img/a0z_chart.png)

*The chart (1 October) shows the flat line; the native band of CFG689 sits on or just below it.*

- **Not decidable yet: a₀ over time.** The two lines separate at redshift 2–5. At those redshifts the uncertainty in each galaxy's gas mass is still larger than the gap (the "calibration wall", PAPER38). The decisive point is a kinematic a₀ at z ≈ 2.5 with an error of about 0.10 dex (CFG689); no public sample has one. The RC100 and CRISTAL/ALESS tiles are unchanged.
- **Conditional: cosmic shear, native inputs.**
  - The engine is theory-v2: the class-A engine with per-host supply, a condensed source and gas expulsion (CFG650). Run at 1024³ from the framework's own early-universe inputs, it is CONSISTENT with raw KiDS-1000 against its matched control on both footings: Δχ² −10.08 canonical (NC1x) and −9.39 alt (NC2x) (CFG654-A2, CFG654-A3).
  - The class is robust, but the size of the lead is amplitude-driven, so quote the class, not the number (CFG909).
  - The framework wins by having less small-scale power, and the absolute fits are mediocre (χ²_min 144.68 and 145.38 for 108 points).
  - DES Y3 is diagnostic only for NC2x, where it is CONSISTENT (Δχ² −2.15).
  - **The condition:** the engine that produces the pass has no known physical parent (Column 5).
- **Not decidable yet: CMB lensing.** It is SAFE on the relative check. Against raw Planck PR4 lensing it is NOT DIAGNOSTIC as frozen, and CONSISTENT only under a post-hoc addendum, with low power at the simulation box's scales (CFG917). A sealed forecast says S4-class high-L lensing could separate theory-v2 from its control, and ACT-like data could not (CFG927; a forecast, not a measurement).
- **Fails: growth under the zero-knob supply rule.** On the full gravitating mass it is 15–19% too clumpy at 512³ (CFG555/556). Theory-v2 (CFG650) adds per-host supply, a condensed source and gas expulsion to the engine; its test on data is the shear tile.
- **Fails: structure growth, chassis alone.** Without B's switch, all matter feels the MOND boost and structure grows about 7× too fast, which CMB lensing rules out. This variant is dead.
- **Open: ALMA U4_27928 (public 6 November) and GS4_24110 (public 28 November).**
  - The original frozen scoring plans govern (CFG806-U4, CFG809; owner decision, 20 October). The wording clarifications and addenda were filed before any data, and the CFG942 harness implements them.
  - One disc excludes no model.
  - The forecast signal-to-noise is low for both discs, so an upper limit with nothing scored is the likely outcome (CFG942).
  - If GS4 is detected, its framework verdict can be ROBUST on most branches: at 15–17 of 20 CI21 values on the six non-FLOOR branches (CFG809 clarification addendum A).
- **Open: Gaia DR4 wide binaries (December 2026).**
  - The sealed prediction is Newtonian (CFG740).
  - Restated kill line (owner decision, 21 October): DR4 kills it if and only if R − 1 ≥ max(0.01, 3σ_R), with σ_R from the pairs that enter R. A smaller excess reads UNDECIDED.
  - At the plan's sample (~2,100 pairs in R) a full MOND-size boost would be caught only about half the time (44–47%, mock). Reliable discrimination needs ~7,000 pairs (CFG943).
- **Open: Gaia DR4 Milky Way predictions,** sealed 10 October (CFG553).
- **Open: the owner's wave a₀(z) idea.** In this idea a₀ oscillates with redshift as a damped wave. CFG956 bounds the largest wave the framework's own expansion data allow. CFG957 builds physical models and lists the other observables the idea touches. The criteria are frozen; there is no result yet.

### Column 5 · The deep "why", and the engine's missing parent

- **Open: why κ = ½.** It is fitted, measured at 0.417 ± 0.095 (CFG493). Of 439 registered derivation or selection attempts, none derives it (CFG894).
- **Open: what sets the cold-mass amount.** Ω_c/Ω_b = 5.364 and the catchment retention f_ret are inputs. Rebuilt without Planck, 5.364 is recovered but not pinned, and f_ret has mixed provenance (CFG886).
- **Open: ownership from an action.** The labelled-domain and source-changing constructions both need a label sector that has no action (CFG945, CFG950, CFG953).
- **Fails: one local theory that gives the law, a¹ growth and no external-field effect.**
  - With cold energy as the medium whose excess is the phantom, the law's deep limit cancels the medium's own self-gravity (theorem D-T, CFG941).
  - A collapse-gated tether gets a ghost, or needs a vacuum offset 15–25× what the slip bound allows (CFG944).
  - A separate field that supplies the deep law must carry an external-field effect (CFG946).
  - The engine's source relocation cannot be conserved covariantly (CFG947).
- **Open, none known: the physical parent of the shear engine.** Three candidate parents have been tried.
  - The labelled-domain theory fails mergers and clusters (CFG950, CFG951).
  - The source-changing theory is CONDITIONAL on galaxy scale but fails clusters (CFG953, CFG954).
  - The relaxing-cold-dust kinetic parent is NOT CLASSIFIED by its frozen rule. Read post hoc, there is no kinetic parent (CFG955):
    - the engine's relocation step is not the fast-relaxation limit of any locally mass-conserving kinetic theory;
    - the law profile held at the bath temperature is unstable, Bonnor–Ebert-like, with an e-folding time of 0.21–0.25 Gyr in NGC 3198;
    - no relaxation time taken from the record works: the excess is unreachable at any relaxation time, and the cluster-core excess survives.
  - What did work in CFG955: exact mass and momentum conservation, no RMIN, no external-field effect, and a¹ growth.
  - **The current engine's relocation step has no known conservative physics behind it.** The shear passes transfer to no tested parent.
- **Open: the energy books of settling.** The record's settling equation does not conserve energy (CFG932). Every repair that keeps the released energy inside matter misses the law. The one that works needs an energy sink outside the matter sector: a dynamical dark-energy partner and a thermal reservoir (CFG935, post hoc).
- **Conditional: quantum stability (G12).** It needs new physics below about 10⁹ GeV, as every theory of this family does.

## The bottom line (current theory, v3)

For v3, the weak-field tests of gravity pass with the screening switched on: gravitational waves at light speed, binary pulsars and GW170817, and Cassini and the planets at L★ = 24–90 pc. Switched off, the same law fails Cassini (the control). MeerKAT's a₀ and the isolated galaxy groups pass for v3 (P4). The tidal dwarfs and DF2/DF4 pass under v3's own dynamics, which make hosted systems dust-free (U1, theorem T3). Static, non-rotating black holes and the strong-coupling estimate are conditional (P3), and so is causality, and the globulars put L★ ≥ 21.7 / 22.9 pc. v3 fails ten tests computed for it:
- health and the leaf problem, which are ill-posed wherever the khronon density is negative, as at every two-body saddle (H4);
- cluster cores (F1); no allowed μ_K fixes them (S4);
- the dwarf satellites and Coma's ultra-diffuse galaxies in their hosts' fields (S1); the failure is structural under v3's own dynamics, by the same theorem that passes the tidal dwarfs (U1);
- the Milky Way's vertical force as an AQUAL disc (P4) and its outer slope (S3);
- the native CMB, since literal v3 has no radiation era (Q6);
- linear growth (F3, Q6); BS25's DBI K fixes BBN only (Q7);
- and so the covariant completion, whose only open escape is L1's native nonlinear run.

Rotation curves, inner isolated-galaxy lensing and red lenses are conditional (P4, S2). The SLUGGS centrals, high-z and CRISTAL / ALESS stay not decidable (S4). The no-go for "law + a¹ growth + no external-field effect" stands. One tile, radiative stability, is not yet recomputed for v3; P3 gave no result for it. Open: why κ = ½ (S3: consistent, not discriminating), the stiffness length L★, what sets the cold-mass amount, and the one selector for the family (T1: no single external-field strength fits). The dated tests are ALMA U4 (6 November), GS4 (28 November) and Gaia DR4 (December; v3's file is sealed by S3). An undated one is a kinematic a₀ point at z ≈ 2.5, measured to about 0.10 dex. The theory remains incomplete.

---

κ = ½ is fitted, not derived. Cold energy is real gravitating mass that is not a particle species. The board and the archive picture are generated by [`make_status_board.py`](make_status_board.py) (`--mutate` must fail: it strips one tile's evidence lane; `--selftest` breaks each guard in turn and every case must be caught); the 21 October board's script, [`campaign_fresh_gravity/closure_map/status_picture_2026_10_21.py`](../campaign_fresh_gravity/closure_map/status_picture_2026_10_21.py), and the 9 October board's script, [`status_picture_2026_10_03.py`](../campaign_fresh_gravity/closure_map/status_picture_2026_10_03.py), are kept unedited. The a₀ chart is made by [`chart_a0z_one.py`](../campaign_fresh_gravity/CHART_a0z_rar_z0_5_2026-10-01/chart_a0z_one.py).
