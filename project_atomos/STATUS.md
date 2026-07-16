# project_atomos — STATUS

*As of 2026-06-25. The machine that replicates the a₀-discovery process (constrained symbolic regression + the
forced-kernel/interlock gate) and aims it at all of particle physics. Both-ways honest: it is built to report
FDR-DEAD when the sector is kernel-free and to certify a real interlock only when all three gates pass.*

---

## What is built (all three pieces are in place and verified)

### 1. Dataset + measurement uncertainties — `targets/pdg_constants.py` (+ `targets/TARGETS.md`)
- **71 targets** (51 directly measured + 20 derived), mpmath at 40 dps with graceful float fallback, pure stdlib.
- Importable from any module; `get(key) -> (value, sigma, rel_precision, n_digits_known)` — the exact tuple the brief
  requires. n-sigma hit predicates wired (`within(candidate, k)`, `n_sigma_of`).
- **Uncertainty is the first-class axis** (Carl's emphasis (a)): `precise_targets()` / `weak_targets()` partition the
  **25 sharp** targets (leptons, α, g−2, m_p/m_e, Koide Q — rel err ≤1e-4) from the **46 weak** ones (light quarks
  10–23%, PMNS/CKM angles 2–14%, bounds), so the engine never fits a deep formula to a blunt number. Every derived
  ratio carries a **propagated** sigma (quadrature; numerical partials for the Koide invariants).
- Sanity check holds: Koide Q_lep = 0.6666605 (**0.91σ** from 2/3, tau-error-limited — honest, not a 6-digit illusion);
  cross-fermion falsification visible (Q_up=0.849, Q_down=0.731 ≠ 2/3).

### 2. Calibration / acceptance test — `calibration/calibrate.py`
- **VERDICT: PASS (8/8).** Re-confirmed live this session (`python3 run_atomos.py --calibrate` and the full driver).
- Certifies the two known positives, rejects the six known negatives, each **for the right reason**:
  - **a₀** √(8π/3) → CERTIFIED (B decomposes `einstein_8pi · friedmann_third`, overdetermined ≥3 forced places, 1 free κ).
  - **Koide Q=2/3** → REAL-PUZZLE-RE-LABELED (A passes via the random-mass-triple null, P≈2.5e-5 ≈ 1-in-40k ≈ documented
    1-in-48k, **15.3 surplus bits**; C ties 3 masses with 0 params; **B honestly FAILS** "√2 in only 1 forced place").
  - 4Z²+3, 64π+Z, Z+11, 6π⁵, 3/13, "dS-Unruh forces √2" → all **FDR-DEAD** at the required first gate.
- Adversarial both-ways checks pass: a factor relabel (5.79≠√(8π)) is rejected; a single-appearance kernel is rejected
  as "definition, not kernel"; a **hypothetical genuinely-forced Koide** (r=√2 forced in 2 places) *does* pass B (B is
  not rigged to always-fail); Koide's B-failure is robust even to dishonest `free_params=1` under-reporting; structural
  nulls are seeded/deterministic (two runs identical).
- One mis-certification was found and fixed during calibration: a comparative-density route was added to `gate/fdr.py`
  so "dS-Unruh forces √2" scores **−0.64 surplus bits** ("no denser than a random O(1)") — the documented honest tell.

### 3. Overnight runner — `run_atomos.py`
- A timed (default 24h, `--hours`) loop ported from hali_flow's `haliflow_8hr_cosmos.run_discovery`, but with the
  **3-part gate as the fitness function in place of R²** (the one porting rule that makes it science). Engine closeness
  (n-sigma, fit-bits) is advisory only — it decides what to hand the gate, never what counts as a discovery.

---

## Does the runner work + accumulate + surface clues + readjust? — YES, verified end-to-end this session

- **Works.** A ~50s smoke (`--target r_mu_e`) ran 887 gate-evals cleanly, 0 manufactured leads, walled at **Gate B**
  exactly as the honest prior predicts (mass ratios have no forced kernel). The trivial identity m_μ/m_e passes Gate A
  (n_sigma=0.00, 13.8 bits) and dies Gate B "forced structure appears in 0 independent places" — no win is faked.
- **Accumulates.** A persistent `Knowledge` object writes `results/knowledge.json` + `results/checkpoint.json` every
  checkpoint: cross-checkpoint tried-set (`seen_canonical` hashes), best-**bits**-per-target, capped top-100
  near-misses, `building_block_scores`, per-target gate-wall stats. `--resume` restores it so nights compound.
- **Surfaces clues.** `results/CLUES.md` is rewritten every checkpoint with: CERTIFIED LEADS; TOP NEAR-MISSES (each
  Gate-A survivor tagged n_sigma / fdr_bits / died@gate / failing-gate tell); RECURRING BUILDING BLOCKS; PROMISING-vs-
  WALL per target; STAGNATION/READJUST log. Plus the honest `results/fdr_dead.jsonl` dead ledger (one row per eval).
- **Readjusts.** Stagnation (no best-bits gain over `STAGNATION_THRESHOLD` evals **and** novelty collapse) fires an
  ordered radical-mutation escalation: (1) deepen/re-scope the alphabet (max_depth 4→5, then rotate flavor group
  none→S3→A4→S4→D27 + extra exponents — the highest-leverage "curate the constants" lever that unlocked a₀), (2) switch
  the hard filter, (3) re-weight the scheduler off wall targets, (4) randomize the strategy mix + reset novelty tracker.
  Each event is logged to `CLUES.md`.

## Is uncertainty wired? — YES, proven two ways
- **Scoring** (`engine/scoring.py`): the same candidate value scored against a tight σ (8 digits) earns fit_bits≈26.6;
  against a loose σ (2 digits) the 6-digit match is **demoted** to ≈6.6 bits. A 6-digit match to a 2-digit constant
  earns nothing beyond 2 digits.
- **Gate** (`gate/fdr.py`): the PDG σ becomes the FDR window. Same baked value: loose tol=1e-2 → BAKED-dense; tight
  tol=1e-6 → 6.7 surplus bits (still <10-bit threshold, correctly stays FDR-DEAD). Tolerance flows
  PDG σ → scoring cap → FDR window throughout.

---

## Both-ways honest standing
- **Ready for a real day-long run? ALMOST.** Calibration PASSES, the runner works end-to-end, uncertainty is wired,
  clues + readjust fire. **One durability fix should land before an unattended 24h launch** (see HOWTO_RUN §Caveat):
  `Knowledge.seen_canonical` is unbounded and re-serialized whole to `knowledge.json` every checkpoint; it hit
  **50.6 MB after only ~887 evals** in the smoke (it tracks every *enumerated* tree, ~470× the gate-eval count). Over a
  full day this balloons to hundreds of MB per checkpoint and risks OOM/thrash. `near_misses` is correctly capped;
  only the tried-set is unbounded. Functionally nothing is broken — this is a memory-durability concern for the long run.
- **The honest prior (do not flinch, do not be defeated).** The SM **mass** sector likely lacks a forced kernel (the
  Yukawa eigenvalues are free; the zimmerman-formula corpus already found 164 FDR-dead mass re-labelings), so the first
  run's leads may **all be FDR-DEAD** — and that is the correct, honest output, not a failure of the machine. The most
  likely place a *real* interlock hides is **PMNS mixing (discrete flavor symmetry — A4/S4/Δ(27)) and the Koide leptons**
  (a genuine FDR-surviving, parameter-free interlock the framework only re-labels). The machine is built to certify such
  a thing if it is there and to report FDR-DEAD honestly if it is not. Same bar both ways; quarantine held (a₀/Z/κ/SM
  never asserted-derived).
