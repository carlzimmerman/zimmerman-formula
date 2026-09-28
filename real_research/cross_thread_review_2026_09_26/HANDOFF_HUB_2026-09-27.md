# Handoff: the calculation hub, the review lanes, and the fresh-gravity campaign (2026-09-27)

**What this session was.**
- The calculation hub. At the author's instruction, calculations are consolidated in one thread.
- The review lanes XR1–XR36, in this folder.
- The fresh-gravity campaign CFG0–CFG6, in `campaign_fresh_gravity/`.

**Why it is being handed off.** The token budget ran out.

**The derivation chain** has its own handoff: `real_research/derivation_chain_2026/HANDOFF_2026-09-27.md` (b5bdb73e8).

## Read first: the standing rules and the author's direction

- **Standing rules.**
  - κ = ½ is FITTED (Z = 5.7888, never ~21). Use both footings (a₀ = 9.3603e-11 / 1.1312e-10 m/s²). Never write
    "closed".
  - Every load-bearing claim needs a committed script with controls and a MUTATE that must fail.
  - No personal names in files or commit messages. Commit only your own paths. Never edit another lane's files.
  - Never edit `PREREGISTRATION_DR4.md` or any `*_HASH.txt`. Amendments are append-only, on the author's go.
  - Zenodo deposits only on the author's go.
- **The author's direction as of 2026-09-27.**
  1. Zero knobs beyond κ.
  2. Build on the framework's own findings and reduce the parameter space. The inventory is
     `campaign_fresh_gravity/CFG0_own_findings_inventory.md`.
  3. Constructive: "answers, not more no-gos". A failed gate is a design constraint.
  4. The fresh campaign imports no published theory as a base (`campaign_fresh_gravity/CHARTER.md`).

## Where the physics stands

**Holding up**
- **Early universe.** It is GR + CDM (XR26): the TT/TE/EE spectra equal ΛCDM's to 7.8e-8, and BBN is standard.
- **a₀ and Λ.** a₀ is tied to Λ by the unimodular (Henneaux–Teitelboim) multiplier, and exactly flat (XR20). The
  khronon's foliation and the unimodular clock combine as two structures without merging (XR30).
- **Strong field** passes (XR25). λ must be declared ≤ 0.03 (XR18b).
- **The Milky Way's outer decline** is reproduced, but with 7.3–8.2e10 M☉ of stars (XR29).
- **SLACS** needs an IMF 0.1 dex heavier than Salpeter (XR33). CFG1 rates it contested, because IMF methods disagree
  by 0.26–0.30 dex.
- **The Local Group's R0 tension** is shared with ΛCDM (FP18): 4.0σ with honest errors (CFG1).
- **M\*'s KiDS pass** survives the projector fix, with its worst cell at −21.7 against the +4 bar (XR35).

**The walls**
- **The band-pass separator family (H_Y, H_S, H_K1) is squeezed from three sides:**
  - KiDS with the web's field in the kernel fails: +111 to +153 against +9 (FP23).
  - Cluster outskirts cap its length at L₀ ≲ 1–1.3 Mpc (XR28).
  - CMASS lensing comes out with the wrong sign (FP23).

  CMB lensing passes only on the linear base in the adopted baryons-only reading. The all-matter reading is excluded
  (FP22, XR26).
- **The dark sector (FK1 conversion).** Its window is empty (FP16, FP25). But CFG1 finds the X-COP failure SOFT: a
  hydrostatic bias b ≈ 0.14 lies inside the published 0.06–0.2.
- **Environment failures.** The LV dwarfs and Coma UDGs fail, inherited from MOND itself, and CFG1 finds they are not
  soft (XR27, CFG1).

**The live constructive lines**
1. **CFG4's target law.** One effective description fits every model-independent fact, in a narrow window:
   - a₀ law flat in z;
   - the galaxy law ν(g_bar/a₀);
   - a switch that is ON only inside turned-around, bound, top-level systems with M_b ≥ M\*, where M\* = a₀ξ²/G is
     the ξ knob;
   - a phantom that ends at a density edge x_e ∈ [0.31, 0.48] of the turnaround radius;
   - a cold fluid with Ω_c h² = 0.12, which is CDM wherever the law is off, and which in bound regions IS the phantom
     (the max rule).

   Its minimal conflict is KiDS's reach against Planck's Ω_c, at the strictest reading. **Its smallest resolving
   ingredient** is a phantom edge at the system's own shell-crossing (splashback) radius, carried by the top-level
   system. That costs no new constant if derived, and it is the job for CFG2, CFG3 and CFG5.
2. **XR36's turnaround gate.** MOND is on only where the baryon flow has turned around (θ_b ≤ 0).
   - Its first script, the gate's action (`XR36_gate_action`), finished; the other two did not.
   - It must specify the kernel's frame. The natural choice is the region's free-falling frame, subtracting its mean
     acceleration so that a uniform external field drops out.
   - It must pass KiDS with the web's field (reuse FP23's machinery), cluster outskirts (XR28) and CMASS (FP23).
   - FP25 found θ_b fails as a CARRIER trigger, but a reversible MOND gate on θ_b is not killed by that.
3. **CFG2 and CFG5: no MOND field at all.**
   - CFG2: GR plus the framework's dark field, regulated in bound systems.
   - CFG5: the RAR written in as a fossil of collapse.
   - Both were stopped mid-run. Their MUTATE runs are done; their main runs are not.
4. **CFG6.**
   - Keep flat a₀ (the unimodular branch) as the prediction. Carry the leaf-averaged √ρ_DE tie as ONE labelled variant,
     giving a band of [−0.14, +0.04] dex at z = 2.5.
   - **Credit.** The record's own credit ledger (`book/BOOK_AUDIT_LEDGER_2026-07.md`) credits the a₀ ∝ √ρ_DE scaling
     for evolving dark energy to Limbach, Psaltis & Özel 2008 (arXiv:0809.2790). What is new is the κ = ½ form and its
     DESI-era predictions, not the scaling itself.
   - PAPER7 v3 called the density mapping "rejected", while FP0 R3b adopted it. CFG6's recommendation resolves the
     conflict.

**Constant count**

- **The current chain (CFG0, after XR18b):**
  - fitted 5: κ, m, ε, ζ, q;
  - declared 2 knobs (ξ, L_Λ), plus 3 natural choices (n, the ramp, c_y);
  - tied 1: a₀ ↔ Λ;
  - derived 0;
  - regulators 2: λ ≤ 0.03 and α_c;
  - eliminated 1: c₂, which is still open at black-hole horizons (XR25);
  - initial data 2: the dark amount and the misalignment.
- **CFG4's target law:**
  - fitted 3: κ, M\* (the same knob as ξ), Ω_c h²;
  - declared 3: ν's shape, the max rule, x_e;
  - it carries none of ε, ζ, q, L_Λ, n, the ramp or c_y.

**Withdrawn claims to stop citing**
- "The kernel removes 74–89% of cluster dark matter" (RETRACTIONS.md, f3162921e). The current figure is 48%
  accounted for at R500.
- "S8 neutral by theorem", withdrawn as a theorem.
- k04's "stable (F6)" four-form verdict (XR31). The four-form route is unstable for 2.39 < g_N/a₀ < 155.

## Lane status

**Committed and reproduced by the hub:**
- XR11–XR15, and XR14's score;
- XR17, XR18, XR18b, XR19, XR20;
- XR21 stage 1 (its LCDM controls and web channel);
- XR25, XR27, XR30, XR31, XR33, XR35.

**Committed with the hub's re-run still owed:**
- XR22, XR23, XR26, XR28, XR29 and XR32. They are listed with their known risks in `REPRO_PENDING.md`.
- CFG0, CFG1, CFG4 and CFG6.

**Committed as INCOMPLETE.** The usage limit stopped these agents. Do not cite them.
- **XR21 stage 2a.** This is the decisive CMB-lensing box for H_K1 in the adopted 'chain' reading.
  - `XR21_pm_core.py` gained the H_K1 readout, and `XR21_s2a_cmb_lensing.py` exists. No stage-2a outputs.
  - Resume: 256³, 100 Mpc/h, both footings, a matched ΛCDM box, and a MUTATE with no floor. Push the result through
    XR26's machinery to Planck 8–400 and ACT DR6.
  - Meet XR18b's five conditions:
    - λ ≤ 0.03;
    - L(a) and y_th(a) prescribed from the scale factor;
    - an analytic ramp;
    - two cell sizes;
    - monitoring of low-field regions.
  - After FP23 and XR28, first decide whether the chain keeps a band-pass separator at all.
- **XR24,** the Local Group numerical action: partial.
- **XR34,** the forest kernel-argument re-score (DE11, DE11b, L346, L347, L358, L359, L362): partial.
  - Its first pool hung after a worker died under memory pressure. Use at most 2 workers, with maxtasksperchild or
    imap and per-task logging.
- **XR36:** only its first script, the gate action, finished (see above).
- **CFG2, CFG3 and CFG5:** partial. The MUTATE runs are done for CFG2 and CFG5; the main runs are not.

## Blocked: the author has approved, but a tool permission is needed

- **PAPER6 v2.** Its source, `qwen_claude_field_theory/papers_2026/PAPER6_kappa_no_go_2026.tex`, is corrected and
  committed. The five v2 edits:
  - the abstract's four-form item;
  - the version-2 date;
  - "205 AU" corrected to about 640 AU;
  - a correction paragraph on the instability band;
  - a conclusion caveat.

  What remains:
  - bump the `.zenodo.json` version to 2026-09-27-v2 and add the correction to its description;
  - run `tectonic PAPER6_kappa_no_go_2026.tex`;
  - run `python3 qwen_claude_field_theory/papers_2026/zenodo_publish_paper6_2026.py --newversion 22559892`.

  Claude Code's auto-mode classifier blocked the metadata step as "Create Public Surface". It needs a Bash permission
  rule, or the author runs the steps.
- **The DR4 amendments.** Both are approved; neither is drafted yet.
  - Amendment 13(a): the four-form variant recorded in Amendment 11 is unstable (XR31;
    `kappa_closure/k04_F6_CORRECTION_2026-09-27.md`).
  - Amendment 13(b): register the chain's law with a separation-resolved statistic that measures ξ (XR22: σ(ln ξ) ≈
    0.20 / 0.15 at the floor). The frozen statistic can kill the chain only from above, at γ̂ ≳ 1.157 / 1.174.
  - First re-run XR22. Its `XR22_common.py` was edited during lane 1's main run.
  - Filing means appending to `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md` and writing `AMENDMENT13_HASH.txt` in
    `AMENDMENT12_HASH.txt`'s format, before 2026-12-02. It may hit the same permission block.

## How the hub re-ran lanes

Each lane was reproduced in a scratch mirror:
1. Copy the lane's `.py` files into a mirror directory.
2. Make every other entry a symlink to the repository, including `.git`, because some lanes read committed files with
   `git show HEAD:`. Don't link the lane's `.out` or `_results*.json`, but do link its input tables.
3. Run MUTATE first, then main.
4. Diff each `.out` and JSON against the committed copy, ignoring timing lines.

Keep the machine's load in mind. Twice today swap nearly filled when about 15 lanes ran at once.

## Recommended order

1. **Finish XR36 with the kernel-frame prescription.** It is the leading switch candidate, and it is also CFG4's T3.
2. **Derive CFG4's smallest ingredient,** the shell-crossing edge, in CFG2, CFG3 or CFG5. Finish their main runs.
3. **XR21 stage 2a**, if the chain keeps a band-pass separator.
4. **Re-run XR22, then draft and file the DR4 amendments.** The author has approved them.
5. **The PAPER6 v2 deposit.** The author has approved it; it needs the permission.
6. **The owed re-runs:** `REPRO_PENDING.md`, CFG0, CFG1, CFG4, CFG6.

## Addendum: the crispiest of astra's 2,000 seeded ideas (`deepseek_push/astra_spawn_ideas/`)

The seeds are AS001–AS2000: 20 groups of 100, of which 423 are P0. All are "proposed; not dispatched". The hub's
pick, in light of today's results, is below.

1. **AS1526, a splashback-like caustic of a derived carrier orbit family.**
   - **The idea.** Derive the first-apocenter (splashback) surface from the dynamics instead of prescribing an edge.
   - **Why it ranks first.** CFG4 found exactly one missing ingredient: a phantom edge at the bound system's own
     shell-crossing radius, carried by the top-level system. If that edge is DERIVED as the first-apocenter caustic,
     the target law loses its declared edge x_e and may resolve its one conflict, KiDS's reach against Planck's Ω_c.
     The KiDS reach has to be checked with FP23's web-field machinery.
   - **Tests already built.** The same edge meets three pieces of existing machinery at once:
     - XR28's splashback data (DES/ACT/redMaPPer);
     - KiDS, via FP23 with the exact projector;
     - CMB lensing, via XR26.
   - **Adapt, don't run as written.** Apply it to the cold component plus baryons in the adopted reading, or in
     CFG2/CFG5's no-MOND form. Keep its control that bars cold-particle splashback formulas in the coherent-wave
     regime.
2. **Runner-up: AS378, the gas-rich BTFR zero point with separate mass accounting.** It is the cleanest standalone
   measurement of the framework's one fitted number. It is cheap and uses SPARC on disk. Its reach is capped by the
   distance scale: a₀ ∝ D⁻², so the result maps onto the H0 tension, as PAPER6 notes.
3. **Third: AS411 and AS414, the precision and likelihood design for a₀(z).** These design the decisive flat-a₀ test,
   and they feed the z ≈ 2.5 JWST/ALMA measurement.

**Why AS440 does not rank.** AS440 (filter-length transfer from galaxies to binaries) is weak. Galaxies do not
constrain ξ: the heat filter moves forces by less than 1e-3 at 0.1–30 kpc (XR29). Gaia DR4 measures ξ directly (XR22).

## Addendum, 2026-09-27 (late): DR4 amendment numbering

The DR4 preregistration's Amendment 13 was filed on the owner's instruction as **Arm C**, the hierarchical-ownership arm
(γ_v = 1.000 exactly; `prep_2026/gaia_dr4_prep/AMENDMENT13_HASH.txt`).

The item planned above as "Amendment 13(a)/(b)" was never filed. It covers the four-form variant's instability and a
separation-resolved statistic for the chain's law. It takes the next free number, 14, if it is filed. XR22 must be
re-run first.
