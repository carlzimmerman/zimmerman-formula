# CFG190 — MUSE-DARK II (bTFR at z ≈ 1) against MUSE-DARK III (a₀ rising with z): can one a₀(z) law fit both? FROZEN CRITERIA

Written 2026-09-29, at the orchestrator's go, before any CFG190 number.

## Inputs and what was known when this was written

- **Inputs are ABSTRACT-LEVEL or from the data chat's summariser notes** (6aa32738c, 44103dfde; `data_assembly/timeline/MUSE_DARK_A0Z_2026-09-29.md`). They are unverified against the PDFs. No per-galaxy table has been read.
- **MUSE-DARK III** (Ciocan+2026, arXiv:2604.22613):
  - a₀(z) = a₀(0) + a₁z, with a₀(0) = 1.0 ± 0.04 and a₁ = 1.59 ± 0.10 (× 10⁻¹⁰ m s⁻²);
  - a₀(z ≈ 0.87) = 2.38 ± 0.1 × 10⁻¹⁰;
  - M* is fitted inside a DC14 disc–halo model; the gas is a constant-HI-surface-density model; Dalcanton–Stilp pressure support; a fixed interpolation function.
- **MUSE-DARK II** (Jeanneau+2026, arXiv:2603.28856):
  - bTFR zero point at z ~ 1: Δ = 0.00 (+0.06, −0.06) dex "along the mass axis", with the slope fixed to Lelli+2019;
  - velocities at 2.0 R_e from the fitted models; photometric M*; gas from scaling relations.
- **The record's June confrontation** (`real_research/A0Z_MUSE_DARK_III_CONFRONTATION.md`): III graded MIXED, METHOD-SPLIT, NON-DIAGNOSTIC.
  - The rise is ΛCDM-degenerate (Mayer+2023) and method-localised: it appears in RAR fits, while the bTFR arm and the repo's own KMOS3D/KROSS kinematics are flat.
  - MUSE-DARK II was not part of that confrontation.
- **Hand expectation, disclosed:**
  - flat a₀ fits II and not III;
  - III's own linear law fits III and not II, by a margin that depends on the acceleration regime at 2 R_e;
  - a₀ ∝ H(z) sits in between;
  - so no single law fits both.

## Q1 — reconciliation (computed)

- **The laws:**
  - flat;
  - a₀ ∝ E(z), with Ω_m = 0.315 as in the KURVS pipeline;
  - T = t(z)/t₀ (CFG175);
  - III's own linear law, a₀(z)/a₀(0) = 1 + 1.59z.
- **Against III.** Each law's predicted ratio a₀(0.87)/a₀(0) is compared with III's 2.38/1.0.
  - The error on log(2.38/1.0) combines the abstract's ±0.1 and ±0.04 in quadrature. That ignores the intercept–slope correlation (declared).
  - The pull is (predicted − measured)/σ.
- **Against II.** Each law's predicted bTFR offset along the mass axis at fixed V, at z = 1.0 (declared, for "z ~ 1"; the sample spans 0.5–1.5), is compared with 0.00 ± 0.06.
  - The mapping uses P2 at fixed g_obs (fixed V at fixed R): solve g_bar² + g_bar a₀ = g_obs², exactly, for the law's a₀(z) against a₀(0).
  - The declared y = g_bar/a₀ bracket at II's 2.0 R_e is: deep (y → 0, where Δ log M_b = −Δ log a₀), y = 0.3 and y = 1.0. II's per-galaxy y is unread.
- **Rule:** a law "fits both" if |pull| ≤ 2 against III AND against II, at a given y.
  - Declared answers: "no law fits both at any declared y"; "law X fits both at y = …"; or the matrix as it is.

## Q2 — circularity (declared UNDECIDED without tables)

- **The mechanism to test:**
  - III's a_bar uses an M* fitted inside the same DC14 disc–halo model as its halo, so the a₀ it fits can inherit the halo-profile prior.
  - II uses photometric M* and scaling-relation gas.
- **What would decide it:**
  - III's per-galaxy fitted M* against photometric M*;
  - a₀ across the seven halo families provided on the DARK site;
  - a₀ from baryon-only fits.
- The tables are requested through the data chat, if its user agrees. Nothing is downloaded without a go in this chat.

## Q3 — the standing line

- **The rule:** a ROBUST rise kills flat a₀(z).
- **Declared reading:**
  - If no law fits both, II and III are mutually inconsistent under any common a₀(z), and at least one is systematics-dominated. A "robust rise" is then not established; the June verdict (non-diagnostic, method-split) stands, now within one collaboration.
  - If some law fits both, it is reported, together with whether flat is excluded.

## Controls and MUTATE

- **C1:** E(0.87) and t(0.87)/t₀ are computed, and III's linear law at 0.87 gives 2.383.
- **C2:** the P2 fixed-g_obs inversion reproduces the analytic sensitivity d ln g_bar/d ln a₀ = −1/(2y + 1): −1 when deep, −1/3 at y = 1.
- **MUTATE=1:** II's Δ is replaced by −0.38 dex, the value III's rise implies in the deep regime. III's law must then fit both, at least at y → 0, and the headline must change.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour any model, or that the theory is closed.
