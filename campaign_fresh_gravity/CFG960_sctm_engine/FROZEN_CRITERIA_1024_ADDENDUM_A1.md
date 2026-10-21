# CFG960 FROZEN_CRITERIA_1024 — ADDENDUM A1 (2026-10-21): the primary variant is CFG953's census own baryons (A5)

Committed ALONE, after AMENDMENT A5 (85ee7487d) and the primary-variant 128³ validation (57520ed5c), and before any 1024³ CFG960 job.
`FROZEN_CRITERIA_1024.md` (6530f8961) is not edited. Where this addendum and that file differ, this addendum governs. Everything
not named here is unchanged, including the statistic, the classes and the pre-declared reading.

## 1. The primary variant

The jobs **SC1x (canonical) and SC2x (alt)** test CFG953's SCT-M as written. "Own baryons" follow CFG953's census convention:
- each labelled particle carries f_b f_ret m_p;
- f_ret = the engine's census retained fraction of the owning peak's turnaround mass, the same `fret_of` / M_ta that M3 uses;
- a fully converted domain therefore has N = M_c/M_b = (1 − f_b)/(f_b f_ret): 53.7 at the floor (M_ta < 10^12.5 h⁻¹ M☉), falling to
  ≈ 6.0 at f_ret = 0.90.

The reason is fidelity to CFG953 (A5), not any preview.

## 2. Secondary variant, registered, reported only, NOT queued

**SC1m / SC2m** are the M2-condensed variant (FROZEN_CRITERIA.md U5; `CFG960_OWNB=cond`), defined in `run_960.py`.
- `chain960.sh` does not run them; the owner may run them later.
- If run, they are scored by the same `cfg960_score.py` (MUTATE first) and reported next to the primary, with no verdict weight.

## 3. Updated pins (replacing §1 and V1 of FROZEN_CRITERIA_1024.md)

| file | sha256 |
|---|---|
| `cfg960_sctm_pm.py` | e1fe3b3d56b9cf52c374a46dc74f19b5ead9e152b46906f608648417199c74d5 |
| `run_960.py` | 50ea595268219d3018240c49e7747ee7a4ada3d365718497a9368adc041a80f0 |
| `chain960.sh` | eb8925d92eced4efd8169e209176d52a2293b37d4f6786e9f03f320ed71bf550 |
| `cfg960_score.py` | 9a84005fc22aa8e30e1778b2645dd4a5f8f665bfd3d428dcb58fe9d4d10cefd7 |
| CFG654 engine / CFG654 scorer | unchanged (7058f433… / e5e3da3b…), asserted at import |

**V1 (VOID).** A run is VOID if its JSON's `engine_sha256` ≠ e1fe3b3d…74d5, or if `sct.own_baryons` ≠ "census f_ret (A5 primary)" for
SC1x / SC2x. V2–V4 are unchanged.

## 4. Gate

The chain's gate additionally waits while any other python process has RSS > 1 GB. Unchanged: no heavy job, free + inactive ≥ 46 GB,
free disk ≥ 45 GB; abort at RSS > 52 GB or swap growth > 4 GB; up to 3 checkpoint resumes per job.

## 5. Seen before this addendum (disclosed)

**Primary 128³ validation (cfg960_validate.out, commit 57520ed5c): every gate of FROZEN_CRITERIA.md §2 PASSES.**

| gate | result |
|---|---|
| V-K | exact; fields bit-identical |
| V-IC | PASS |
| V-MASS | ≤ 2.2e-16 |
| V-MOM | ≤ 1.24e-9 with M3 off |
| V-N1 | (a) 0.996–1.002; (b) 0.9791 / 0.9688 / 0.9521 |
| V-LAW | ≤ 3.1% |
| V-SCORE | exact |
| V-MEM | PASS |
| V-MUT | bites |

**PREVIEW 128³, NOT A VERDICT.** P_grav/P_S0 at k = 0.3 / 0.5 / 1, z = 0:
- canonical 1.011 / 1.062 / 1.207;
- alt 1.013 / 1.070 / 1.256.

At 128³ the bodies are compact (r_e ≤ 3.1 dx) and more concentrated than the resolution-limited dust halos. The M2 variant's preview
(0.959 / 0.881 / 0.628 and 0.965 / 0.902 / 0.679) was listed in §0. Neither preview predicts the 1024³ sign or size: the domain floor
is ≈ 1e12 h⁻¹ M☉ at 128³ against ≈ 2e9 at 1024³, and halo cores are unresolved at 128³.

## 6. §8 (shared or conditional), amended

Own baryons = CFG953's census f_ret, which is empirical (CFG515) and inherited, as in CFG953. The M2-condensed alternative is the
secondary variant. All other items of §8 stand. V-N1's growth sub-line now passes for the primary; A2's failure record concerns the
secondary (M2) variant's validation.

## 7. Cost and start

The cost estimate is unchanged: about 18–30 h and 43–47 GB per footing. The primary's compact bodies need fewer painted points and
nodes than the M2 variant.

The start command is unchanged (from the repository root):

    cd campaign_fresh_gravity/CFG960_sctm_engine && nohup bash chain960.sh > ../../../_external_data/cfg960_work/chain960_nohup.log 2>&1 &

Reading (unchanged, §6 of FROZEN_CRITERIA_1024.md): **SCT-M passes the shear side iff SC1x and SC2x are both CONSISTENT on raw
KiDS-1000 with Δχ² ≤ 0 vs NCS0** and no diagnostic survey is EXCLUDED or TENSION.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
