# OWNER DECISION DRAFT, 2026-11-05 (third note, pre-data): the NSS-off entry of σ_sys(b) as a seed mean

**Status: DRAFT, NOT FILED.** The owner has not yet accepted this. It takes effect only if the owner says so in chat before
any DR4 byte exists (DR4 due 2026-12-02). Filing means:
- this text is committed alone, retitled "filed", with the owner's words quoted;
- the DR3 code-path check in §4 has already passed.

If filed, it supersedes **only one component** of D8 (a) in `OWNER_DECISION_2026-11-05b_DR4_D7_D8.md` (d71a111d1d): how the
NSS-off entry in σ_sys(b) is measured. It edits no frozen file. These are untouched:
- PREREGISTRATION_DR4.md and its amendments;
- the D2 note and A1–A3;
- CFG740, CFG800/825 and CFG943;
- the 10-21 kill-line note;
- `OWNER_DECISION_2026-11-05_DR4_FORKS.md` (413c1c8e24);
- the estimator, cuts, σ_fit, the band rows, the R rule, Newton 1.000, the Arm A anchor and the primary build's frozen seeds.

κ = ½ FITTED; footings never pooled; not theory closed.

## 1. What changes

As filed (D2 A3, D8 (a)), σ_sys(b) is computed as:

  σ_sys(b) = max(0.020, ½ × the full spread of γ̂ across the frozen robustness ladder and the NSS-off rung),

with the NSS-off rung built **once**, at the registered stage-G seed (k = 0).

**Proposed.** The NSS-off entry that goes into that spread becomes

  γ̂_NSS-off ≡ γ̂_0 + Δ̄,   where   Δ̄ = (1/K) Σ_{k=1..K} [ γ̂(rung_k) − γ̂(base_k) ].

- γ̂_0 is the registered primary (build k = 0, frozen seeds).
- rung_k = `build(drop_nss=True, smax_kau=30)` at stage-G seed offset k.
- base_k = the registered build at the same offset k, in the same cut-13 mode as the primary (`cones-literal`, D7 N9).
- Both are fitted by the registered fit path (pipeline `--catalog`, seed 20261216), one footing at a time.
- **K = 50**, the same offsets 1..50 as Amendment 18's sweep, so the base_k fits are shared with G10 wherever the cut-13 mode
  matches. Where it does not match (G10 runs `extract-builder`), base_k is rebuilt in `cones-literal`.

Everything else in σ_sys(b) is unchanged:
- the max with 0.020;
- the ½ × full spread;
- the other ladder rungs, each still built once at k = 0;
- the requirement that definitions (a), (e) and (g2) agree, else UNDECIDED.

The D7 N4.2 test (a shift below 1 σ_fit passes the NSS-off condition) is applied to Δ̄ instead of the single-seed shift.

**Reported beside it, with no verdict weight:**
- the single-seed (k = 0) NSS-off shift and the σ_sys(b) it would have given;
- the SD of the K paired differences and the standard error of Δ̄.

## 2. Why (evidence found after D8 (a) was chosen, all on DR3, all code-path or information only)

- **DP1** (f732b84221): over 8 reseeded builds, the probe's mean NSS-off shift is +0.010 canonical (SD 0.043) and +0.006 alt
  (SD 0.029). For the rung it is +0.004 (SD 0.031) and +0.0006 (SD 0.015). The registered-seed probe read +0.075 / +0.0575.
- **DP2** (583697a4f7) splits DR3's +0.069 canonical probe shift into +0.013 from the 100 NSS-flagged pairs and +0.055 from the
  reseeded stage-G Monte Carlo. Alt splits as +0.017 + +0.022. Mock-triple injection shows the physical NSS screen's shift is
  about 0 or negative.
- **So the single-seed entry measures mostly stage-G seed noise, not the systematic the rung is meant to probe.** That seed
  noise is already measured and reported separately, as σ_build by Amendment 18's K = 50 sweep. In definition (g2) it enters
  σ_sys directly. Counting one draw of it again inside (b) double-counts it, at a size that depends on the draw.
- **DP2:** DR4 N under the frozen cuts is about 8,000 (7,025–8,618), not 30,000. At that N, the chance that a Newtonian sky
  reads decisive against the bare law is 0.80 at σ_sys 0.020, but only 0.12–0.40 at DR3's 0.0375. Whether DR4 decides anything
  hinges on this one term.

With K = 50 the standard error of Δ̄ is about 0.043/√50 ≈ 0.006 canonical and 0.004 alt, below the 0.020 floor.

## 3. What it cannot do, stated now

- **Direction unknown.** It does not fix σ_sys(b) at 0.020. The other rungs (R_chance < 0.001, 3–20 kAU; RUWE if O6 adds it)
  still enter at k = 0, and any of them may set the spread. What DR3's σ_sys(b) would have been under the seed-mean entry is
  not yet computed (§4.4). The amendment may lower σ_sys(b), or leave it unchanged because another rung sets the spread.
- **It can add power only against the bare law.** v3s predicts Newton (CQ2) and can never be confirmed over Newton by DR4. A
  Newtonian sky still reads "v3s survives", never "confirmed".
- **The tuning objection (D8's reason for (a)).** The objection was that changing the binding error term after DR3 showed it
  binding would read as tuning. The answer offered:
  - the change is decided before DR4 exists;
  - it is a variance-reduction of the same quantity, not a new definition;
  - the k = 0 value stays reported beside it;
  - the evidence for it (seed noise dominates the probe) does not depend on which way DR4 falls.

  The owner may still prefer (a). The cost of (a) is stated in D8 itself: a higher chance that DR4 reads UNDECIDED.

## 4. Condition before filing (DR3 code-path check; new code, own FROZEN_CRITERIA committed alone first)

1. A sweep wrapper over DP1's `rung_build(drop, 30, seed_offset=k)` and the registered base at the same k, `cones-literal`,
   K = 50, fitted by the registered path. It must reproduce DP1's 8-reseed rung mean for k = 1..8 exactly (same seeds, same
   code path) before K = 50 is read.
2. A MUTATE that returns the k = 0 shift for every k must make Δ̄ equal the single-seed value, so the check bites.
3. Cost recorded (builds, fits, peak RSS, wall time) and repeated for DR4 at central N. On DR4, every stage-G correlation fetch
   for k ≥ 1 is a delta fetch into the per-seed cache, and is an archive query needing the owner's go (it joins G10/G11).
4. `dp3_sigma_sys.py` takes the seed-mean entry (new option; the single-seed path stays the default until filing). The DR3
   σ_sys(b) under both entries is reported, information only.

If §4 fails or is not run before 2026-12-02, this draft lapses and D8 (a) stands as filed.

## Sources
- D8 (a), D7 N4: `OWNER_DECISION_2026-11-05b_DR4_D7_D8.md` (d71a111d1d).
- Outcome map and the 2c table of band edges vs σ_sys: `OWNER_DECISION_2026-11-05_DR4_FORKS.md` (413c1c8e24).
- DP1 README and `dr3_check.json` (f732b84221); DP2 README and `dp2_dr3_nssoff_results.json` (583697a4f7).
- D2 note A2–A3; Amendment 18 (σ_build, K = 50); CQ2 SEALED_PREDICTION.md.
