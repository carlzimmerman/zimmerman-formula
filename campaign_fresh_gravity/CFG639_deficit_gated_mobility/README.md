# CFG639: deficit-gated mobility (settle and relax only where cold energy is missing)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (dbe89ed33), 2026-10-12.
- **Hypothesis HG.** The record's settling drift and FIX-2 velocity relaxation act only where d = ρ_ph − ρ_c > 0. Cold energy
  that is not missing is collisionless, so settled halos should pass through each other in a merger while galaxies still settle
  (CFG638: "collisionless in mergers, fluid in galaxies"). No constant is added.
- **Settings:** κ = ½ FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed";
  nothing here says the data favour the framework.

## Status

| part | status |
|---|---|
| A, galaxy side (CFG544 bench) | **DONE. As frozen: NOT DIAGNOSTIC** (tooth A-M1 did not bite). See the reading below |
| B, mergers (CFG623 pipeline) | **DONE (2026-10-12 19:34–20:42), VALID. VG-1 UNDETERMINED; VG-2 UNDETERMINED (Part A).** See Part B below |

## Part A (`cfg639_galaxy.py` → `cfg639_galaxy.out`, `cfg639_galaxy_results.json`)

Run with `OMP_NUM_THREADS=1 nice -n 10 python3 cfg639_galaxy.py`: 2 processes, < 1 GB each, about 12 min, exit 0. CFG544's toy is
imported read-only. The bench uses the exponential kernel, as CFG544/550/554 did (CFG626 found the headlines kernel-robust).

| cell | IC-B (10 Gyr): log X / D / last-2-Gyr drift | G550 | IC-C (5 Gyr): log X / D / last-2-Gyr drift | G550 | gated off (B / C) |
|---|---|---|---|---|---|
| MW can | +0.013 / +0.046 / +0.027, +0.031 | pass | +0.032 / +0.025 / −0.059, −0.080 | **fail (not steady)** | 0.34 / 0.60 |
| MW alt | +0.015 / +0.051 / +0.012, +0.038 | pass | −0.001 / −0.001 / −0.083, −0.076 | **fail (not steady)** | 0.32 / 0.57 |
| cluster can | +0.011 / −0.005 / −0.024, −0.005 | pass | +0.002 / −0.005 / −0.067, −0.119 | **fail (not steady)** | 0.19 / 0.54 |
| cluster alt | +0.006 / −0.010 / −0.025, −0.018 | pass | +0.005 / −0.020 / −0.040, −0.066 | **fail (not steady)** | 0.17 / 0.49 |

- **A-C1 (G ≡ 1 reproduces CFG544 `MW_can|fix2_C`): PASS**, Δlog X = ΔD = 0 exactly.
- **A-M1 (inverted gate must move MW_can IC-C D by > 0.02 vs gated): DOES NOT BITE**, ΔD = +0.0094. Frozen label:
  **NOT DIAGNOSTIC**, so VG-2 will be UNDETERMINED whatever Part B finds.

**Reading (verified as hard as a pass; not a verdict input).**
- The label's wording, "the gate does not act", is **wrong as a description**. The gate switches off 17–34% (IC-B) and 49–60%
  (IC-C) of in-catchment particle-steps.
- Against G ≡ 1, the gated MW_can IC-C run differs: β +0.28 vs +0.06, log X +0.032 vs +0.006, and it is not steady (−0.059 /
  −0.080 vs −0.012 / −0.016).
- The inverted gate moves the edge strongly (r99 1.60 vs 1.29 r_*) but the shell median D only weakly. The frozen tooth measured
  a quantity the gate barely moves; it is a weak tooth, not an inactive gate.
- **Substantive pattern:** infall (IC-B) passes in all 4 cells. The settled-at-rest start (IC-C) is close to the targets at
  5 Gyr (|log X|, |D| ≤ 0.032) but **still evolving in all 4 cells** (D drifting −0.07 to −0.12 per 2 Gyr). Where the halo is
  overfilled, the gate leaves it collisionless, so it neither relaxes nor is pushed out. This is the overfill risk declared
  before the run.
- The overfill excess inside r_* is negative everywhere (−0.05 to −0.13 M_cat), so the CFG544 "as is" core overfill does not
  reappear here. The failure is steadiness, not overfill.

## Corrections and disclosures (2026-10-12)

- **Correction 1 (reporting only).** The first Part A run counted gated-off steps in an instance attribute, so the reported
  fraction read 0.000 in every run. The counter was fixed to the class (`type(self).n_in`) and the run repeated. Every other
  number is identical (diff of `.out` with counter and wall time stripped: identical). The fraction has no verdict weight. The
  first-run log is not kept in the repo.
- Part B's gate statistics are per instance (`self.gstat`) and were not affected.
- Part B import check only (no simulation run) before this commit.

## Files

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | criteria (dbe89ed33) |
| `cfg639_galaxy.py` → `.out`, `_results.json` | Part A |
| `cfg639_merger.py` | Part B (CFG623 main imported read-only; only `settle` gated; runs cached in `runs/`) |
| `run_639.sh` | Part B waiter (log in `../../../_external_data/cfg639_work/waiter.log`, outside the repo) |

## Part B (`cfg639_merger.py` → `cfg639_merger.out`, `cfg639_merger_results.json`, `runs/`)

Run by `run_639.sh` once no 1024³ run was live (started 19:34 with 26 GB free; 15 runs on 4 processes; finished 20:42).

**Controls:** B-R (α = 0 reproduces CFG623 exactly): max 0 kpc on both footings; B-G1 (G ≡ 1 at α = 0.1 reproduces CFG623 `a0.1_can`):
0 kpc; **B-M1 bites**: 71% of cold settle steps gated off in the pericentre window; f moves by 0.545 and β̄ by 0.328 against the
ungated CFG623 cell. Footing validity holds on both footings.

| α | can: f / Z_B / β̄ / Z_H → status | alt: f / Z_B / β̄ / Z_H → status | ungated CFG623 (can) |
|---|---|---|---|
| 0 | +0.181 / +1.09 / +0.063 / +1.47 → ALLOWED | +0.178 / +1.06 / +0.061 / +1.44 → ALLOWED | ALLOWED |
| 0.03 | +0.209 / +1.32 / +0.069 / +1.56 → UNSCORABLE (Bullet stability 1/4) | +0.178 / +1.06 / +0.070 / +1.57 → **ALLOWED** | UNSCORABLE |
| **0.1** | **+0.259 / +1.71 / +0.088 / +1.83** → UNSCORABLE (Bullet stability 2/4 at the first epoch) | **+0.224 / +1.44 / +0.091 / +1.88** → UNSCORABLE (2/4) | **EXCLUDED (f +0.803, Z_B +6.07)** |
| 0.3 | +0.404 / +2.87 / +0.118 / +2.26 → UNSCORABLE | +0.341 / +2.37 / +0.126 / +2.37 → UNSCORABLE | EXCLUDED (f +1.005) |
| 1 | +0.625 / +4.64 / — → UNSCORABLE (Harvey 0/40) | +0.474 / +3.43 / — → UNSCORABLE | UNSCORABLE (f +1.418) |
| 3, 10 | f ≈ 1.0, Z_B ≈ +7.4 to +8.2; Harvey < half → UNSCORABLE | same | UNSCORABLE |

**Frozen verdicts:** allowed set {0} (canonical), {0, 0.03} (alt). **VG-1 (merger rescue): UNDETERMINED** — no α ≥ 0.1 node is scorable
on both footings. **VG-2: UNDETERMINED** (Part A NOT DIAGNOSTIC).

**Reading.**
- **The gate moves the merger result substantially.** At α = 0.1 the Bullet offset falls from f = 0.80 (Z_B +6.1, excluded) to
  f = 0.26 / 0.22 (Z_B +1.7 / +1.4), and the Harvey statistic passes (Z_H 1.8 / 1.9). The node misses ALLOWED only through the frozen
  Bullet stability rule (2 of 4 lensing-peak variants agree at the first bracketing epoch; 3 required), the same bimodal-peak failure
  that left CFG623's α = 0.03 unscorable. α = 0.3 is marginal (Z_B +2.9 / +2.4); α ≥ 1 still gives large offsets.
- So, with the gate, mergers no longer exclude α = 0.1 on value; they leave it unscored. That is not a rescue by the frozen rule, and
  galaxies want α ≳ 0.5 (α = 1 still has Z_B +4.6 / +3.4), so the merger–galaxy tension narrows but is not removed.
- CFG641 (H-CB + gate) runs next once the orchestrator's CFG640 1024³ job ends.
