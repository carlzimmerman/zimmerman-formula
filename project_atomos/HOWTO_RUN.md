# project_atomos — HOWTO RUN

*How to launch the day-long autoresearch run, where the results land, how to read the surfaced clues, and how to
READJUST when it hits a dead end. Pure stdlib + numpy + scipy + sympy + mpmath. Local, no network.*

---

## 0. First, prove the machine is trustworthy (always do this before a real run)

```bash
cd /Users/carlzimmerman/new_physics/project_atomos
python3 run_atomos.py --calibrate          # acceptance test: must be PASS (a0 CERTIFIED, Koide RE-LABELED, 6 dead REJECTED)
```
If calibration is not PASS, do not trust any lead the runner emits. (Last verified: PASS 8/8, 2026-06-25.)

---

## 1. Launch the day-long run (the command)

```bash
cd /Users/carlzimmerman/new_physics/project_atomos
python3 run_atomos.py --hours 24 --all
```

- `--all` sweeps every **precise dimensionless** target (lepton ratios, couplings, PMNS/CKM angles, the Koide Q's);
  bounds and blunt (>~10%) numbers are skipped so a deep formula is never fitted to a 2-digit constant.
- `--hours 24` sets the wall-clock budget. The loop round-robins targets (70% systematic, 30% weighted toward
  promising targets) and checkpoints every 200 gate-evals.
- Run it detached so it survives the terminal:
  ```bash
  nohup python3 run_atomos.py --hours 24 --all > results/run.out 2>&1 &
  ```
- Resume after a kill/restart (the tried-set + best-bits + strategy state are restored):
  ```bash
  python3 run_atomos.py --resume --hours 24 --all
  ```

**Other useful invocations**
```bash
python3 run_atomos.py --target koide_Q_lep --hours 8     # pour a night into ONE target (Koide leptons)
python3 run_atomos.py --all --checkpoint 100 --hours 24  # checkpoint more often (smaller knowledge.json bursts)
python3 run_atomos.py --all --seed 20260625 --hours 24   # different logged seed (reproducible; default 1234)
```

### Caveat before an unattended 24h launch (one durability fix recommended)
`Knowledge.seen_canonical` (the cross-checkpoint tried-set) is **unbounded** and re-serialized whole to
`results/knowledge.json` every checkpoint. In the smoke it reached **50.6 MB after ~887 evals** because it stores every
*enumerated* tree hash (~470× the gate-eval count), not just gate-evaluated ones. Over a full day this grows to hundreds
of MB per checkpoint and risks OOM/thrash. Functionally the run still works; this is a memory concern. Mitigations,
cheapest first:
- Run a **bounded burst** instead: `--hours 6` segments, `--resume` between them, archiving/clearing `knowledge.json`
  between segments; **or**
- Fix in `run_atomos.py` (`Knowledge.to_dict`, line ~227, and the add at line ~977): cap/evict `seen_canonical` (e.g.
  keep only gate-evaluated hashes, or an LRU bound), or write it to a separate append-only shard instead of re-dumping
  whole each checkpoint. `near_misses` is already capped at 100 — only the tried-set needs this.

---

## 2. Where the results land — `results/`

| File | What it holds |
|---|---|
| `results/CLUES.md` | **Read this.** Human-facing, rewritten every checkpoint (readable live mid-run). |
| `results/leads.jsonl` | Certified LEADS — candidates that pass all 3 gates. The headline (expected empty or Koide-class). |
| `results/fdr_dead.jsonl` | The honest dead ledger, one row per eval, each with its failing-gate TELL. |
| `results/near_misses` (in `knowledge.json`) | Top-100 Gate-A survivors that failed B/C — the leads-in-waiting. |
| `results/knowledge.json` | The full accumulator: tried-set, best-bits-per-target, building-block scores, per-target stats. |
| `results/checkpoint.json` | Resumable state for `--resume`. |
| `results/progress.log` | One line per checkpoint (evals, leads, best_bits, novelty, hours left). |
| `results/stats.json` | Machine-readable run stats each checkpoint. |

---

## 3. How to read the clues (`results/CLUES.md`)

Read top to bottom; every number is reported **relative to the measurement uncertainty** (n-σ + surplus bits), never a
bare digit count.
1. **CERTIFIED LEADS** — if non-empty, a candidate passed FDR ∧ forced-kernel ∧ interlock. Check its forced factors'
   registry provenance and its interlock mode. This is the only thing that counts as a discovery.
2. **TOP NEAR-MISSES** — Gate-A survivors (statistically surprising, *within the error bar*) that failed B or C. Each
   row: `n_sigma`, `fdr_bits`, `died@gate`, and the **TELL** (e.g. "factor has no pre-fit provenance", "≥2 free
   numbers", "one-number re-description", "cross-sector kill"). These are the most actionable hints.
3. **RECURRING BUILDING BLOCKS** — which constants / germs / group-invariants / ops keep appearing in Gate-A survivors
   (summed surprise bits). A recurring forced-coefficient candidate is the strongest hint at where a real kernel lives.
4. **PROMISING vs WALL** — per-target best-bits, Gate-A pass-rate, and the dominant `gate_wall`. "wall=B" on a
   high-precision mass ratio is the honest forced-kernel prior showing up; a target with several Gate-A survivors and a
   non-B wall is where to point more evals.
5. **STAGNATION / READJUST LOG** — every autonomous radical-mutation event and what it changed.

**The honest reading.** If the first run's `CLUES.md` shows 0 certified leads and every mass-ratio target walled at
Gate B, that is the **expected, correct** output — the SM mass sector may be genuinely kernel-free (164 prior FDR-dead
re-labelings). It is not a machine failure. The most likely place a real interlock hides is **PMNS mixing** (discrete
flavor symmetry) and the **Koide leptons** — watch those targets' near-misses and building blocks first.

---

## 4. How to READJUST at a dead end (the knobs to change)

The runner readjusts itself on stagnation (escalation menu, logged in `CLUES.md`). To steer it by hand at a dead end,
change these knobs — in rough order of leverage:

1. **The alphabet (highest leverage — the "curate the constants" lever that unlocked a₀).**
   In `run_atomos.py` the radical-mutation menu rotates the active flavor group `none → S3 → A4 → S4 → D27` and toggles
   extra exponents / √-ratios (`StrategyState._esc_deepen_alphabet`, and `build_target_alphabet` /
   `engine/alphabet.py`). To force a discrete-flavor hypothesis from the start, set `StrategyState.active_group` to the
   group you suspect (PMNS → start at `A4`/`S4`) and turn `extra_exponents` on. Bump `Config.max_depth` (4→5) to admit
   deeper trees. **Editing the alphabet IS the physics input** — this is where a real PMNS/Koide interlock would surface.
2. **The target set.** Narrow to where the action is: `--target koide_Q_lep` or a PMNS angle, instead of `--all`. Or
   edit the scheduler / `select_targets()` to abandon walls (`TargetScheduler.abandon`) and pour evals into the
   highest best-bits target.
3. **The strategy mix.** `Config.p_enumerate / p_combine / p_mutate` (default 0.50/0.25/0.25). Raise `p_combine` to
   recombine high-bits survivors toward the Koide interlock signature (tie ≥3 measured leaves); raise `p_mutate` to
   explore around a near-miss. Radical mutation resamples these automatically; set them by hand to bias the search.
4. **The hard filter / interlock depth.** `Config.hard_filter` (`interlock → rep → dimension`) changes which structural
   cut spends the dimensionless freedom; flip to `rep` to chase symmetry-multiplet relations the interlock filter hides.
   Relax `Config.min_interlock` (3→2) to admit two-mass relations, or keep it at 3 to demand the Koide signature.
5. **Stagnation sensitivity.** `Config.stagnation_threshold` (default 1500 evals) — lower it to readjust sooner on a
   wall, raise it to grind a promising region longer before mutating.

After any hand-edit, re-run `--calibrate` to confirm the gate is still trustworthy, then relaunch (use `--resume` to
keep the accumulated tried-set, or start fresh to explore the re-scoped alphabet cleanly).
