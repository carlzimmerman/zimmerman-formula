# CLEANUP SQUADRON — 2026-07-02

Three pending items closed in one pass. Each item: what ran | verdict | numbers | flag action. Framework footing throughout: ν(y)=√(1+1/y), canonical a₀=9.36e-11 (fork 1.13e-10 run both ways), MI-EFE γ band 1.05–1.10. Retraction stands; no new claims beyond the a₀ reframing.

---

## A. Lensing-RAR first-look — adversarial verification

**What ran.** Committed `real_research/reviews/confront_lensing_rar.py` rerun against the **raw Brouwer+2021 release** (`BROUWER_RAR_DIR` → freshly fetched B21 `rar_data`), exit 0; plus a fully independent re-derivation on a different code path (scipy bounded minimize + closed-form deep-MOND WLS estimator: log a₀ = weighted mean of 2·log g_obs − log g_bar), exit 0. Verifier: scratchpad `verify_lensing_independent.py`; rerun log `verify_rerun.txt`.

**Verdict: UPHELD — flag LIFTED.** `real_research/LENSING_RAR_FIRSTLOOK_2026-07.md` line-3 status flag flips from *pending adversarial verification* → **verified**. Bottom line unchanged: **NON-DIAGNOSTIC on the 9.36e-11 vs 1.2e-10 fork.**

**Numbers (all independently reproduced).**
- Fixed-a₀ ladder (M24, stat+sys): χ²/dof 3.70 (REL) / 3.29 (EXT) / 2.46 (FULL); with +0.1 dex mass-norm sys in quadrature → 0.82 / 0.73 / 0.58. McGaugh-ν@1.2e-10 reference: 0.96 REL. Anchors pass: M24 7.6/11=0.69 ✓; B21 bracket 10.77/1.28/3.03 ✓.
- Free-a₀: 1.517e-10 ±0.044 (REL) / 1.486e-10 ±0.035 (EXT); closed-form estimator 1.526/1.492e-10 (<1% — not a minimizer artifact). 9.36e-11 sits +4.8σ/+5.7σ stat+sys, **+2.3σ/+2.6σ with the 0.1 dex sys** (1.2e-10: +1.0σ/+1.1σ). B21K: 1.77e-10±0.082 / 1.95e-10±0.065 ✓. Jackknife [1.42,1.56]e-10 ✓.
- δ-degeneracy exact to 0.9%: δ*(9.36e-11)=+0.210/+0.201, δ*(1.2e-10)=+0.102/+0.093 — difference 0.1079 dex = exactly the a₀ fork.
- Profiled fork: Δχ² prior A +0.95/+0.91 (M24), +1.11/+1.45 (B21K); one-sided CGM prior B ≤+0.23. Units audit clean (G=4.518e-30 pc³/M☉s² ✓; no h-trap; B21 h70=1 identity). Covariance rebuilt from raw 15×15: reproduces embedded table to 5e-4 dex; max off-diag corr 0.087.

**Correction (one line, no verdict flip).** The 0.1 dex mass-norm sys is a **correlated** normalization; per-point quadrature is slightly generous. Correlated-nuisance profiling: χ²p/dof=1.11 (REL), 9.36e-11 at 2.0σ from the free fit — consistent with the +2.3σ quote, still non-diagnostic under the ±0.2 dex M/L band + CGM window. *(Add this note to the firstlook MD.)*

**Both-ways.** Arrow points high-a₀ (1.5–2e-10 fiducial) on every convention — but the required +0.20 dex coherent baryon uplift sits inside the published band, and the identical logic penalizes canonical MOND 1.2e-10 on B21 masses. No win, no deficit. Fork closes via a sub-0.05-dex absolute baryon budget, not deeper lensing.

---

## B. Growing-ν staircase referee — forecast delta vs published

**What ran.** Scratchpad `growing_nu_staircase_referee.py` (CAMB 1.6.6, exit 0): z-resolved m_ν(z)=m₀√(ρ_DE(z)/ρ_DE0) staircase, growth-matched shell stitch (anchor z=50), conventions identical to committed `real_research/reviews/growing_nu_camb_fisher.py` (k 0.008–0.2, Veff=20 (Gpc/h)³, n̄=1e-3, z=0/0.5/1, amplitude-marginalized). Calibration reproduced the published endpoint bracket exactly (0.65%/1.39%, 1.4σ/3.9σ). Convergence: 4-shell vs 8-shell identical to ≤0.1σ — stitch converged.

**Verdict: WEAKEN (moderate) — published bracket (DOI 10.5281/zenodo.20977421 forecast layer) overstates in-band signal ~×1.5. Correction, not a kill.**

**Delta vs published.**

| Σ_today | published step / SNR | staircase step / SNR |
|---|---|---|
| 0.059 eV (floor) | 0.65% / 1.4σ | **0.43% / 1.0σ** |
| 0.10 eV | 1.4% / 3.9σ | **0.92% / 2.4–2.5σ** |

- Sharper referee finding: a floating **constant** mass m_c≈0.65Σ absorbs the in-band k-step to residual **0.2σ/0.5σ** — P(k, z≤1) alone is near-degenerate. The surviving discriminator is the **cross-epoch split** (LSS Σ_eff≈0.65Σ vs CMB-anchored ≈0), i.e. CMB-S4-class lensing — exactly where the published note originally placed it.
- Forks (both ways): (i) DR2-DESY5 central (−0.752,−0.86) → milder same-signed weakening; (ii) the published exp(−λ₀Δφ)-plateau footing (Σ_eff=0.60Σ at CMB) is the other branch — under it the published 1.4σ/3.9σ stand. **Spread 1.0–1.4σ (floor) / 2.4–3.9σ (0.10 eV) IS the footing uncertainty.** Two-tracer independent-volume ceiling: ×1.15–1.25 (~1.2σ/~3.0σ), does not rescue the floor.
- Physical reality of the separator confirmed: step scale-dependent (k>0.2: 0.70/1.19% vs k<0.01: 0.27%).

**Flag action.** Downgrade the intermediate-strength forecast claim wherever cited; test remains hostage to Σ>floor and w≠−1 (Front B logic unchanged).

---

## C. Milgrom linear no-EFE MOND (arXiv:2503.07106) — DR4 table third line

**What ran.** Scratchpad `milgrom_linear_noefe_wb.py` (exit 0) on the v2 paper (PDF cached in session tool-results): linear DML model (d⁴r/dt⁴=∇ψ, fractional Laplacian; EFE **identically zero** by linearity, Eq 19-20) + β-family (Eq 56). Bridge: quadrature V⁴=V_N⁴+C·MA₀ ⇒ γ=(1+C/y)^¼ — for C=1 this is exactly the framework's own ν, maximally fair. Strict-DML also run.

**Verdict: DR4 pre-registration table GAINS the Milgrom-linear line — four-way γ(s) separation, decided by SHAPE (plateau vs rise), not one number.**

| s (kAU) | Newton | Framework MI-EFE | MG/AQUAL+EFE | **Milgrom linear no-EFE** | β=3/2 MI no-EFE |
|---|---|---|---|---|---|
| 5 | 1.00 | 1.05–1.10 | ~1.10 | 1.06 / 1.07 | 1.11 / 1.13 |
| 10 | 1.00 | 1.05–1.10 | ~1.14 | 1.20 / 1.23 | 1.33 / 1.37 |
| 20 | 1.00 | **plateau** | **plateau** | **1.51 / 1.57** | 1.75 / 1.83 |
| 30 | 1.00 | 1.05–1.10 | ~1.14 | **1.80 / 1.88** | 2.11 / 2.21 |

(γ pairs = canonical / fork a₀; M_tot=1.5 M☉, equal masses; g_ext=1.9e-10 caps the EFE lines.)

**Numbers/verdicts.**
1. γ_linear ≈1.5–1.9 at 20–30 kAU (strict-DML 1.43–1.75); a₀-fork sensitivity ±4%. Chae's flat γ=1.137 band already disfavors the linear model at deep separations IF 20–30 kAU bins hold — currently signal-starved; **DR4 slope test 15–30 kAU is the decision** (flat-1.0 / flat-1.05-1.10 / flat-1.14 / rising-1.5+).
2. Strict linear model has γ<1 for s<9 kAU (0.45 at 2 kAU) — no Newtonian limit; pre-register the bridged curve only, cite the strict curve as the model's own pathology (Milgrom: pure-DML, Ostrogradsky-unstable, "unacceptable as a full-fledged MOND theory").
3. **σ-spread uniqueness CORRECTION:** the non-adiabatic relational σ-spread is **MI-class-generic** (Sec VIII: trajectory-functional inertia), not framework-specific. Framework-specific content = magnitude (6–13%) + MI-EFE γ band 1.05–1.10 only. Cluster σ-spread discriminates MI-class vs MG (MG=0 exactly); framework-vs-Milgrom-linear discrimination = this γ(s) slope. *(Update `project_cluster_standing` phrasing accordingly.)*
4. Mass-ratio lever (weak, second-order): linear C=1 always; β=3/2 C=1.94(q=0.5)→2.0(q=1); AQUAL 0.62/0.61.

**Flag action.** Copy `milgrom_linear_noefe_wb.py` from scratchpad → `reviews/` and commit **before** citing the table publicly (per committed-verifiable-scripts rule; no git in this pass).

---

## Ledger

| Item | Verdict | Flag |
|---|---|---|
| A. Lensing-RAR verification | UPHELD, non-diagnostic on the fork | **LIFTED** (firstlook MD → verified) + one-line correlated-sys note |
| B. Growing-ν staircase | WEAKEN ~×1.5 in-band; cross-epoch split survives | Forecast numbers corrected: 1.4→1.0σ (floor), 3.9→2.4σ (0.10 eV); spread = footing |
| C. Milgrom linear no-EFE | Third DR4 line added; slope test decides | σ-spread re-scoped MI-generic; script needs reviews/ commit |

No front flips. Live fronts remain TWO (s^TX SME dipole; a₀(z) hostage). Scripts: committed `real_research/reviews/confront_lensing_rar.py`; scratchpad `verify_lensing_independent.py`, `growing_nu_staircase_referee.py`, `milgrom_linear_noefe_wb.py` (latter pending reviews/ promotion).