# Lensing front — a0 footing audit (Opus 4.8, 2026-06-14)

Framework a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE) = **9.355e-11** (pure dark energy).
Wrong footings watched for: 1.2e-10 (canonical/local McGaugh), 1.13e-10 (rho_total/cH0), 1.0/1.1e-10, fitted.

## 1. Morphology split (8.8sigma) — `reviews/lensing_rar/` — **CLEAN (a0-independent, correct)**
`lr_battery.py`, `esd_conversion.py`, `agentH_perclass_C.py`, `agentZ_second_variable.py`,
`agentK_jackknife_stack.py`, `lr_esd_remeasure.py`, `lr_sersic_crosscheck.py` contain **NO a0 literal at all**.
The split is computed as the early-vs-late g_obs difference at FIXED g_bar bins on Brouwer's released ESD
profiles (g_obs = 4 G DeltaSigma); reproduced 8.8sigma (chi2=119.9/15), 15/15 bins early-above-late, +0.261 dex.
a0 never enters the chi2. The doc states this explicitly (`lr_battery_results.md` "a0-independent: the split is
type-dependence at fixed g_bar... so it does not involve a0 at all"). `lr_data_acquisition.md` line 47 plans the
a0-insensitivity check at BOTH 1.2e-10 AND 9.36e-11. **As-required: the morphology split is a0-INDEPENDENT and the
verdict is on no footing at all (correct). No mis-verdict.**

## 2. `predictions/door1_gravitational_lensing.py` — **FALSE-WIN (mild, cosmetic)**
Line 29: `A0 = 1.2e-10` (canonical/local McGaugh). Line 30 computes `A0_LAMBDA = 9.3623e-11` (the framework value,
verified) and PRINTS it as "Lambda-only" — but the RAR boost table, the figure, and `a0_of_z(a0_0=A0)` all use the
**local 1.2e-10**, not 9.36e-11.
- The verdict ("the framework reproduces the KiDS lensing RAR") is QUALITATIVE, not a chi2.
- Direction: displaying 1.2e-10 lands the nu-curve exactly on Brouwer's OWN adopted a0 — a near-circular,
  tighter-looking "pass." Re-stated at the framework 9.355e-11, deep-MOND g_obs is **-0.054 dex (~12% in boost)
  LOWER**; this is well inside Brouwer's ~0.1-0.2 dex scatter, so the framework STILL passes qualitatively, just a
  softer pass. So the local a0 produced a mild FALSE-WIN presentation, not a false deficit.
- The a0_of_z EVOLUTION block is ratio-only (alpha_inf(z)/alpha_inf(0)), genuinely a0-independent — unaffected.
- **Corrected verdict: framework reproduces the Brouwer lensing RAR within scatter at a0=9.355e-11 (sits ~0.05 dex
  low in deep-MOND, inside the band). Replace the 1.2e-10 anchor with 9.355e-11; the qualitative pass survives.**

## 3. `predictions/door1_lensing_ultra.py` + `predictions/VERIFY_lensing_adversarial.py` — **CLEAN (exemplary)**
Both compute `a0_fw = c^2 sqrt(Lambda/32pi) = 9.3547e-11` from Planck18 (verified, matches the (c/2)sqrt(G rho_Lam)
identity to 7 figs) and use it as the CENTRAL a0 for the absolute deflection. 1.2e-10 (McGaugh RAR) and 9.1e-11
(simple-mu) are used ONLY as the two edges of a MOND interpolating-function SYSTEMATIC band; the script explicitly
notes "framework a0 is -28% relative to McGaugh RAR" and that the framework sits INSIDE the [9.1,12.0]e-11 band.
alpha_inf(1e13,z=0)=5.0815", and the EVOLUTION ratio is coefficient-free. **Correct footing, both-ways framing
already present. No correction needed — this is the gold-standard footing for this front.**

## 4. `a0z_lensing_forecast.py`, `reviews/project19_lensing_evolving_a0.py`, `reviews/widening_lensing_bao_LG_dsph.py` — **CLEAN (a0-independent verdicts; cosmetic literal slip)**
- `a0z_lensing_forecast.py`: pure RATIO (a0(z)/a0(0) via rhoDE/Ez hypotheses); absolute a0 never enters. Verdicts
  (framework +3% bump below floor; rising-rival exclusion) are footing-independent. CLEAN.
- `project19` (line 21) and `widening` (line 19) hard-code `a0 = 1.2e-10`, but every verdict uses it only in
  sqrt(E(z)) scalings or order-of-magnitude worked examples (MOND boost, Crater II EFE, alpha~sqrt(GMa0) RATIO).
  No quantitative pass/fail hinges on the value; swapping 9.36e-11 changes worked numbers by ~12% with NO verdict
  flip. Cosmetic footing slip, NOT a mis-verdict. (Pro-framework note: these are not deficits dressed up.)

## 5. `reviews/toe_law/f4_lensing_wall.out` — **CLEAN (correct footing; framework-internal kill)**
Uses a0 = **9.36e-11** (correct). Tests a PURE-MODIFIED-INERTIA / mediator variant where the metric stays
baryon-only: baryon-only lensing excluded 40.5sigma; framework nu-amplitude-only (no phantom-halo) residual 12.5sigma;
deep-bin amplitude ratio 229.7x. This is NOT a verdict against the framework's actual AeST/phantom-halo lensing
(which lenses on baryons+phantom and passes) — it is a wall the framework USES to argue the MI-only route is dead.
Correct a0, honestly framework-constraining. No mis-verdict; if anything it is framework-unfavourable reported at
full weight on the right footing.

## Net for the lensing front
- The headline morphology split (8.8sigma) is genuinely a0-INDEPENDENT and correct — the prior claim that it is
  "a0-independent" verifies.
- The only footing error of consequence is `door1_gravitational_lensing.py` displaying the local 1.2e-10 — a mild
  **FALSE-WIN** (tighter-looking pass), NOT a false deficit. Corrected, the framework still passes within scatter.
- The rigorous ultra/adversarial scripts and the toe_law wall are already on the correct 9.355e-11 footing.
- No FALSE-DEFICIT found on this front (no "framework lenses too weakly" artifact). The both-ways result: one
  cosmetic false-win to retract (door1 table anchor), no high-priest deficit to retract.
