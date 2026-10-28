# DY1_group_dynamics_audit: the groups' σ is sound; HG2's negative sign survives the dynamics audit

Criteria: `FROZEN_CRITERIA.md` (6707283e80, committed alone, before any script or number); no amendment.
Machinery: GA1's committed script (133f61510d), executed read-only; it in turn executes HO1, also read-only.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not matter and not a
particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen, PRIMARY): **DYNAMICS AUDIT DOES NOT HELP** (canonical and alt)

| run | rows (BRIGHT, shared-bin BRIGHT / FAINT) | measured D [95 %] | D_pred, base picture (canonical / alt) | all-law | class |
|---|---|---|---|---|---|
| Step 0 = V-cat (GA1 PRIMARY) | 188 (12; 8 / 82) | −0.362 [−0.605, −0.139] | +0.306 / +0.282 | +0.173 | gap 0.668 |
| **PRIMARY: σ from member velocities, Nm ≥ 5** | 188 (12; 8 / 96) | **−0.373 [−0.622, −0.139]** | **+0.326 / +0.306** | +0.165 | **DOES NOT HELP** (gap 0.699) |
| V-10: Nm ≥ 10 | 75 (12; 8 / 47) | −0.337 [−0.600, −0.106] | +0.350 / +0.341 | +0.181 | DOES NOT HELP |
| V-kT: GA1 MISMATCHED dropped | 184 (8; 6 / 28) | −0.313 [−0.646, −0.072] | +0.320 / +0.307 | +0.155 | DOES NOT HELP |

The power is 0.28–0.36, below HG2's 0.50 bar (reported only).

## The audit itself

**σ from member velocities against the catalogue σ.**
- σ_aud is the gapper estimator with 3σ clipping. K1 recovers 295 against 300 km/s on a synthetic sample.
- σ_aud / σ_cat has a median of **1.074**, 16–84 % range [1.01, 1.17], over 188 groups.
- No group falls below 5 velocity members.
- **The catalogue dispersions are sound.** They are about 7 % low on average, the same for both arms.

**The four kT–σ mismatches persist with measured σ:**
- J1242+0241: β_spec 0.16;
- J1030−3519: 0.10;
- J0416−5546: 0.09;
- the Virgo σ-794 group: 2.63.

All four have 10–714 velocity members, so the mismatch is not a σ error. It is an X-ray association or temperature
issue, and dropping them (V-kT) does not change the class.

## Reading

**Across GA1 and DY1, HG2's negative sign survives every data-only audit:**
- duplicate matches;
- the gas mass, from an XMM scaling;
- the gas extent;
- σ from member velocities;
- membership floors;
- kT–σ consistency.

In every variant the measured D is negative (−0.31 to −0.40), and every picture with g_pred = F(g_bar) predicts it
positive (+0.15 to +0.35).

**What is left:**
- (i) **The estimator's geometry:** g_obs = 3σ²/r at (4/3) R_h, compared with a lensing-calibrated reference curve.
  This was not audited here, because no on-disk alternative estimator exists for these groups.
- (ii) **Small numbers:** 6–11 bright groups in shared σ bins, power at most 0.45.
- (iii) **A real effect:** X-ray-bright groups really are dynamically lighter, at fixed σ, than their counted baryons
  imply relative to isolated lenses. No mechanism in the record produces that.

That reading is stated, not graded. The honest status is that HG2's sign is an **unexplained, underpowered tension**,
not a refutation.

## Checks: 4/4

- **K0:** Step 0 reproduces GA1's PRIMARY (D −0.3623; D_pred +0.3059 / +0.2821).
- **K1:** the gapper estimator, as above.
- **K2:** g_obs = 3σ_aud²/r to 1e-12.
- **K3:** peak RSS 0.70 GB, one thread.
- **Rerun:** the results JSON is byte-identical (`15ae8ae9…b65c`).
- **MUTATE twin** (`DY1_MUTATE=1`, σ_aud × 1.5 in the rows): K2 fails, checks 3/4, exit 1.
