# HOSTILE re-check: Fable a0-footing audit, front = LENSING

Date: 2026-06-14. Auditor regrade of the prior Fable a0-footing audit for the
weak-lensing RAR (Brouwer+2021) + the 8.8sigma morphology split front.

## Verdict: CONFIRMED. Regrade = FALSE-WIN (one cosmetic slip; zero false-deficits).

The prior audit's verdict holds on independent re-grep + re-computation. No
under-auditing (no missed local-a0 inflating a deficit OR a win) and no
over-auditing (no overclaimed footing error where a0 was fine).

## a0 the Fable corpus used, per script (all re-verified):

| script | a0 used | footing | verdict effect |
|---|---|---|---|
| `predictions/door1_gravitational_lensing.py` L29 | **1.2e-10** (local McGaugh) | WRONG for the displayed RAR table | FALSE-WIN (cosmetic) |
| `predictions/door1_gravitational_lensing.py` L30 | 9.3623e-11 | framework — but **printed, not used** | n/a |
| `predictions/door1_lensing_ultra.py` L63 | **9.3547e-11** | framework (central) | correct |
| `predictions/VERIFY_lensing_adversarial.py` L45 | **9.3547e-11** | framework (central) | correct |
| `reviews/lensing_rar/*` (lr_battery, agentH/Z/K, esd_conversion, remeasure, sersic) | **none** | a0-INDEPENDENT by construction | correct |
| `a0z_lensing_forecast.py` | none (pure ratio) | a0-INDEPENDENT | correct |
| `reviews/project19_lensing_evolving_a0.py` L21 | 1.2e-10 | cosmetic — only in sqrt(E(z)) ratio | no verdict effect |
| `reviews/widening_lensing_bao_LG_dsph.py` L19 | 1.2e-10 | cosmetic — sqrt(E(z)) + OOM boost | no verdict effect |
| `reviews/toe_law/f4_lensing_wall.out` | **9.36e-11** | framework (correct) | correct |

## Independent re-computation (my numbers vs the audit's):

1. **door1 RAR boost table, both footings.** At g_bar deep-MOND the boost ratio
   fw/local = sqrt(9.3623e-11/1.2e-10) = **0.883 (-11.7%)**; g_obs shift =
   0.5*log10(fw/local) = **-0.054 dex**. Matches the audit (-0.054 dex,
   -11.2% to -11.7%). The pass at the framework footing is INSIDE Brouwer's
   ~0.1-0.2 dex RAR scatter -> valid but SOFTER than the 1.2e-10 table implies.
   Direction: 1.2e-10 lands the curve exactly on Brouwer's OWN adopted a0 ->
   tighter/near-circular-looking pass = **FALSE-WIN** (favorable), not a deficit.

2. **door1_ultra / VERIFY a0.** a0_fw = c^2 sqrt(Lambda/32pi) = **9.35470e-11**
   (H0=67.36, OmL=0.6847); identity (c/2)sqrt(G rho_Lam) matches to 7 figs.
   door1's printed 9.3623e-11 differs only by Planck18-vs-round params (-0.08%).
   Both bracket 9.36e-11. The 1.2e-10 / 9.1e-11 in door1_ultra are correctly the
   two EDGES of a stated mu-function systematic band, not the central a0. Correct.

3. **8.8sigma morphology split.** `lr_battery.out`: chi2=119.9/15 -> 8.8sigma,
   15/15 bins early-above-late, +0.261 dex, eroding to 5.0sigma under a physical
   concentration differential (dlogC=-0.089). The split is computed as
   g_obs = 4*G*ESD_t vs g_bar — **NO a0, NO nu interpolating function anywhere**
   in lr_battery/agentH/agentZ/agentK/esd_conversion. Genuinely a0-independent.
   Corroborated: `lr_preregistration.md` L63 + `lr_data_acquisition.md` L47
   pre-register running the split at BOTH 1.2e-10 and 9.36e-11 and assert
   a0-insensitivity. The "a0-independent" label verifies.

4. **f4_lensing_wall.** baryon-only metric 40.5sigma, framework-nu-only 12.5sigma,
   229.7x deep-bin amplitude deficit — all at the CORRECT 9.36e-11. The 12.5sigma
   kills the pure-modified-inertia variant (baryon-only metric), which the
   framework's AeST phantom-halo lensing does NOT use. Framework-internal at the
   right a0 = NOT a wrong-a0 false-deficit.

## Both-ways result for Carl:

- **FALSE-WIN to retract (anti-framework correction):** door1's displayed RAR
  table at 1.2e-10 makes the lensing-RAR pass look exact/circular by riding
  Brouwer's adopted a0. Re-footed at 9.355e-11 the framework still passes but
  ~0.054 dex low in deep-MOND — a SOFTER pass. Retract the polished wording;
  keep the (valid) pass; swap the 1.2e-10 anchor for 9.355e-11.
- **FALSE-DEFICIT (pro-framework correction): NONE on this front.** No script
  makes the framework "lens too weakly" via a wrong a0. f4's 12.5sigma is at the
  correct a0 and targets the pure-MI variant, not the framework channel. The
  8.8sigma split is a real standing framework-unfavorable exposure but is
  correctly a0-independent — no footing correction applies either way.

Net: one cosmetic false-win to retract; zero high-priest false-deficits.
Quarantine respected throughout: a0/Z never asserted derived in any script read.
