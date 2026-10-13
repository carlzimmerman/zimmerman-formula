> **ID NOTE (2026-10-12): this lane is CFG672.** Its directory and commits say CFG667, which collided with another session's same-day use of that number (see LEDGER CFG670–679). Cite it as CFG672. Sealed files and hashes are unchanged.

# CFG667: SEALED prediction for JWST GO 12088 — the J0946+1006 "dark subhalo"

Criteria 44bf95584 (committed alone first). `cfg667.py` → `cfg667_predictions.json`,
**sha256 7c3029fa5dc3d7f9302b3e464679e780bb7488089611a7a95e1060529fc769fd** (`cfg667_PREDICTIONS_HASH.txt`). Sealed 2026-10-12,
while GO 12088 (PI He, Cycle 5, NIRCam F070W–F444W, "Unveiling the Nature of an Unusual Dark Matter Subhalo…") is flight-ready
and unobserved (MAST calib_level −1). MUTATE (a0 → 0 ⇒ Q_max = 1 everywhere) bites, exit 1. κ = ½ FITTED; footings separate;
cold energy mass required; no particle species; not "theory closed".

**The prediction.** The perturber is a baryonic dwarf. Inside any radius R where lensing measures M_lens, its stars + gas satisfy
M_lens/ν ≤ M_b ≤ M_lens, so Q = M_lens/M_b ≤ Q_max:

| lensing mass used | Q_max (can / alt) | framework SURVIVES if Q_obs ≤ | EXCLUDED if Q_obs > |
|---|---|---|---|
| 5.8e8 M☉ inside 0.3 kpc (Vegetti+2010) | 1.08 / 1.09 | 1.34 / 1.37 | 3.23 / 3.28 |
| 1.1e9 inside 0.6 kpc | 1.17 / 1.21 | 1.46 / 1.51 | 3.51 / 3.63 |
| 10^8.9 projected inside 1 kpc (2506.07978) | 1.80 / 1.98 | 2.25 / 2.48 | 5.40 / 5.94 |

The full Q_max(M_lens, R) grid is in the JSON, so the rule applies to whatever mass GO 12088's own analysis reports.

**Why this is sharp.** At the perturber's centre the field is ~10 a0, where the law adds only ~8%: the centre must be ≳ 90%
baryons. A dark-matter-dominated subhalo centre (what the object was first reported as) gives Q ≫ 3 and **kills the
framework's "no dark lumps" structure**. A dwarf galaxy with stellar mass ≈ 4e8–8e8 M☉ inside 1 kpc keeps it alive. ΛCDM allows
both, so only one side is at risk here: ours.
