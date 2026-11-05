# W1_pmedium_3d_scaleup — the 3D P-medium core peak: reproduced, ported, laddered, certificate

Lane of `rebuild_2026_10_22/` (rules: `../BRIEF.md`; this lane's `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md`,
`AMENDMENTS.md` A1–A4). κ = ½ is FITTED. a₀ enters only through the unit system (t₀ = √(ℓ₀/a₀), M₀ = a₀ℓ₀²/G), so every
ladder number is given on both footings (canonical a₀ = 9.3603e-11, alt 1.1312e-10 m/s²), never pooled. No observational
data enter. Nothing in `sol61_push/` was edited, moved or deleted.

Subject: the parallel lane `sol61_push/spatial_expansion_2026_10_23/` (SE-20261023): a reduced preferred-frame action with
cold and baryon particles, a saturating polarization P (force P/(1−|P|)) and a scalar χ, in an imposed EdS periodic box,
seeded by a single quiet sinusoidal mode per axis. Its blocker: strong-seed (.03) peaks 2.00 / 2.76 / 3.27 at 8³/12³/16³
do not converge, runs were bounded to ~300 s, and there was no isolated binding certificate.

## Verdicts (z = 10; κ = ½ FITTED; both footings, never pooled; final after the queue round of 2026-10-24/29)

| item | result |
|---|---|
| Reproduction R | **R-PASS, byte-identical**: all 12 SE outputs (9 evolutions, check, force, summary) re-run from byte copies reproduce the recorded `result.json` sha256 exactly |
| Port gate G-P1 | **PASS, bit-identical** to SE's `evolve` at 8³/12³/16³, weak and strong (threads 1 and 4); 15× faster at 16³ (40.4 s → 2.6 s, one thread); re-passed on the A4 engine |
| MUTATE G-P2 | **PASS**: dropping the h-force on cold particles breaks the gate (8³ strong peak 28.79 vs 2.0004; final positions off by 1.15 cells) |
| Contract G-P3 | **PASS** at 16³ and 32³ (threads 1 = 4 bit-identical; two real SIGTERMs → exit 75 → `--resume` bit-identical; `--resume` on a complete run exits 0), bit-identical partial resume at 64³; in production the weak 128³ jobs were preempted and resumed 15–16 times each |
| **Canonical 128³** | **INIT-FAIL** (§3): initial-minimizer residual 2.03e-5 (strong) / 1.03e-5 (weak) > 1e-5. Not used for any verdict; diagnostics only. A4 fix + 2 rerun jobs listed (`ENQUEUE_A4_commands.txt`) |
| Strong peak δ_c, **alt** | **CONVERGED** through 128³: 2.016 / 2.772 / 3.265 / 4.053 / 4.408 / 4.587 at 8–128³ (64→128 change 4.1% ≤ 5%; observed order p ≈ 0.99 on 32/64/128) |
| Strong peak δ_c, **canonical** | **NOT CONVERGED (PROVISIONAL)** at its finest valid grid pair: 4.104 → 4.480 (32→64, 9.2%). The INIT-FAIL 128³ run gives 4.727 (diagnostic: 5.5% over 64³) |
| Weak peak δ_c | CONVERGED on both: alt .03698 → .03683 (64→128, 0.41%); canonical .03779 → .03783 (32→64, 0.09%) |
| Core mass M_c(<2.88 kpc) | **alt CONVERGED under both readings**: 1.5231e7 → 1.5303e7 M☉ (64→128, 0.47%; 8 and 16 cells). Canonical 1.5148e7 → 1.5156e7 (32→64, 0.05%): CONVERGED (enumerated reading) / UNRESOLVED (strict), PROVISIONAL |
| Core mass M_c(<1.44 kpc) | **alt**: 2.469e6 → 2.532e6 M☉ (64→128, 2.5%): CONVERGED (enumerated) / UNRESOLVED (strict: 3.996 cells at 64³). Canonical: UNRESOLVED until a valid 128³ |
| Core mass M_c(<0.3215 kpc) | unresolved at every grid (1.78 cells at 128³) |
| Binding certificate | **NOT CERTIFIED** on both footings, both apertures, both readings (alt at 128³; canonical at 64³, PROVISIONAL). E_iso < 0 at all 11 snapshots of the last e-fold but it changes ≈ 18–20×. At z = 10 the strong-seed core region is at **turnaround** (2K/|U| = 0.005 inside 1.44 kpc at 128³ alt, from 0.97 one e-fold earlier), not virialized. Weak seed: Hubble-flow dominated (2K/\|U\| ≈ 2) |

## 1. Reproduction (FROZEN_CRITERIA §1)

`repro/` holds byte copies of SE's `model.py`, `run_v2.py`, `check.py`, `force_check.py`, `summarize.py`, `CONTRACT.md` and the
parent `fragment_radiation_2026_10_22/model.py` (`PROVENANCE.json`: every copy hashes equal to its source; SE's
`CHECKPOINT.sha256` verified OK before copying). `repro/run_repro.sh` re-runs SE's nine recorded command lines plus the
three checks on `/usr/bin/python3` (3.9.6, NumPy 1.26.2, SciPy 1.11.4, as SE's manifests record). `verify_repro.py`:
**12/12 byte-identical** (`REPRO_RESULT.json`); its `--mutate` (a 1e-6 change in one recorded leaf) is caught. So SE's
numbers are exactly what its code produces: peaks .036786 / .037363 (weak 8³/12³), 2.000410 / 2.762995 / 3.270372
(strong 8³/12³/16³), the early/earlier preparation-history peaks .041552 / .063124, the check values and the failed
force-step and convergence gates as recorded.

## 2. Port and gate (§2)

`engine/pmedium3d.py` + `engine/tsc_kernels.c`: SE's Model, `fields` (instantaneous minimum + tangent), `evaluate` and
`evolve` with identical NumPy expressions; TSC deposition/gather in C with SE's weight arithmetic, `np.bincount`
accumulation order and NumPy's pairwise order for the 27-term force sum (A1), compiled without FMA contraction; one force
evaluation per step (SE's second `evaluate` repeats identical inputs). Threads split x-slabs (deposit) and particles
(gather), so results do not depend on the thread count. Contract: SIGTERM/SIGINT → checkpoint at the next step boundary
→ exit 75; rolling checkpoints every 600 s; `--resume` (complete → exit 0; else newest checkpoint; else fresh); every
output written tmp → fsync → `os.replace`; `.npz` byte-reproducible; resume keeps the arrays' memory order, which NumPy's
reductions depend on at 64³ (A2). `gate.py` → `gate_results.json` (G-P1 PASS, bit-identical, engine sha256 74249415…),
`gate_results_MUTATE.json` (G-P2 PASS); `resume_test.py` → `resume_test_n16.json`, `resume_test_n32.json`; `probe.py` →
`probe_n64_canonical.json`, `probe_n64_alt.json`. Certificate self-test `selftest_cert.py`: unperturbed Hubble sphere,
(K + U)/K = 0.036 on both footings (PASS ≤ 0.10); without the Hubble term it fails (C-S1m).

Speed: one thread, 16³ 2.6 s (SE 40.4 s), 32³ 41–46 s, 64³ 556–605 s; peak footprint 0.05 / 0.10 / 0.35–0.38 GB.
The canonical strong 64³ run took 605 s against the 600 s direct-run limit (projected 575 s); disclosed in A3.

## 3. Ladder (z = 10)

Peak cold contrast δ_c (SE's `contrast_c_max`, a cell maximum):

| footing / seed | 8³ | 12³ | 16³ | 32³ | 64³ | 128³ |
|---|---|---|---|---|---|---|
| canonical weak .001 | .03679 | .03736 | .03758 | .03779 | .03783 | (.03764, INIT-FAIL) |
| canonical strong .03 | 2.0004 | 2.7630 | 3.2704 | 4.1045 | 4.4804 | (4.7272, INIT-FAIL) |
| alt weak .001 | .03595 | .03650 | .03671 | .03692 | .03698 | .03683 |
| alt strong .03 | 2.0157 | 2.7721 | 3.2650 | 4.0532 | 4.4082 | 4.5872 |

Canonical 8/12/16³ ladder peaks equal SE's recorded peaks bit for bit (`analyze.py` check). Baryon peaks are higher
(canonical strong 3.31 → 10.44 from 8³ to 64³; alt 10.90 at 128³). Max work residual ≤ 9.2e-5 at every grid, ≤ 3.6e-7 at
128³. All 64³-alt and 128³ jobs ran the A2 engine (sha256 74249415…).

Cold mass in fixed physical apertures about the iterated centre, strong seed (M☉; below ~2 cells the counts are lattice
noise; canonical and alt agree to the shown digits at 8–32³ because particle masses in M☉ do not depend on the footing):

| aperture | footing | 16³ | 32³ | 64³ | 128³ | cells at 64³ / 128³ |
|---|---|---|---|---|---|---|
| 0.3215 kpc | alt | 0 | 0 | 1.67e4 | 3.55e4 | 0.89 / 1.78 |
| 1.44 kpc | alt | 1.07e6 | 2.669e6 | 2.469e6 | 2.532e6 | 3.996 / 7.99 |
| 1.44 kpc | canonical | 1.07e6 | 2.669e6 | 2.469e6 | (2.532e6, INIT-FAIL) | |
| 2.88 kpc | alt | 1.335e7 | 1.5148e7 | 1.5231e7 | 1.5303e7 | 7.99 / 15.98 |
| 2.88 kpc | canonical | 1.335e7 | 1.5148e7 | 1.5156e7 | (1.5222e7, INIT-FAIL) | |

At 128³ (alt) δ_ap,c = 3.54 inside 1.44 kpc and 2.43 inside 2.88 kpc; at 64³ (canonical) baryons inside 1.44 kpc are
8.27e5 M☉ (baryon fraction 0.25 against the cosmic 0.157).

**Convergence verdict (§5).** Alt footing, final: the strong-seed cell peak is CONVERGED (4.1% from 64³ to 128³,
with the step shrinking at about first order: 24%, 8.8%, 4.1%), and the aperture masses are CONVERGED (2.88 kpc under both
readings, 0.47%; 1.44 kpc under the enumerated reading, 2.5%). Canonical footing: NOT CONVERGED at its finest valid pair
(32³/64³, 9.2%), PROVISIONAL until an A4 128³ run passes its initial-state gate. Its INIT-FAIL 128³ diagnostics track the
alt values closely (peak 4.727, 5.5% over 64³; masses within 0.6% of alt). Weak seed: CONVERGED on both footings. The cell
peak is the statistic that converges last; the aperture mass settles first.

## 4. Binding certificate (§6)

E_iso = K (cold + baryon, physical velocities including the Hubble flow, about the centre-of-mass velocity) + U (isolated
pairwise, softened by one physical cell) + E_field (SE's five non-negative field energy densities inside R), at 11
snapshots across the last e-fold (z = 28.9 → 10).

| run, aperture | E_iso (code units) z = 28.9 → 10 | max \|E−E_end\| / \|E_end\| | 2K/\|U\| | N_c inside | E_field/\|U\| at z = 10 |
|---|---|---|---|---|---|
| alt 128³, 1.44 kpc | −1.42e-3 → −7.49e-5 | 17.9 | 0.97 → 0.005 | 60688 → 9712 | 0.08 |
| alt 128³, 2.88 kpc | −2.61e-2 → −1.40e-3 | 17.6 | 1.22 → 0.039 | 423927 → 58708 | 0.02 |
| canonical 64³, 1.44 kpc | −2.04e-3 → −1.01e-4 | 19.3 | 0.99 → 0.005 | 7616 → 1184 | 0.07 |
| canonical 64³, 2.88 kpc | −3.73e-2 → −1.97e-3 | 17.9 | 1.24 → 0.043 | 52840 → 7268 | 0.02 |

Negative: yes. Stable: no. Over the last e-fold matter flows out of the fixed physical aperture with the (decelerating)
Hubble flow, and at z = 10 the central region is at maximum expansion (K ≈ 0). An overdense region in EdS has negative
energy and will collapse, so "negative" alone certifies nothing; a stationary core would hold E_iso constant. **NOT
CERTIFIED** on the alt footing at 128³ (both apertures, both readings; resolved at 8 and 16 cells) and on the canonical
footing at 64³ (PROVISIONAL). The pattern is the same at every resolved grid; the energies agree between 64³ and 128³
(alt) to 3–10%, so this is a property of the configuration, not of resolution. The region Hamiltonian E_H(R) and its integrated expansion work ∫W_A d ln A are
in `LADDER_RESULTS.json` (open region, so no balance is expected: ΔE_H = +2.5e-4 vs ∫W_A = +4.2e-4 at 1.44 kpc).

## 5. What the runs say about the model (diagnostics; hand reasoning labelled)

- **The medium is linear here.** At z = 10, strong seed, 64³: max|P| = 1.6e-4 (the saturation P/(1−|P|) and the .985 guard
  are never approached), χ ∈ [1.00358, 1.00362]. *Hand reasoning from SE's equations:* |P| → O(1) needs |∇h| ~ 1 in code
  units, i.e. densities of order M₀/(4πℓ₀³) ≈ 1.2e8 M☉/kpc³, comparable to the canonical core density (7.9e7 M☉/kpc³) and
  ~2×10³ times the z = 10 mean; these runs reach a few times the mean.
- **The h-force is what holds the cold peak down.** Without it (MUTATE) the 8³ strong peak is 28.8 instead of 2.0. *Hand
  reasoning:* SE's linearized minimum is h_k = δρ_c,k/(1 + k²ℓ₀²) (its own Helmholtz start), so the cold particles feel
  Φ + h with their self-gravity reduced by 1/(1 + k²ℓ₀²): below ~ℓ₀ = 0.44 kpc (physical) cold matter barely
  self-gravitates while baryon gravity is unscreened. The box is 0.52 ℓ₀ at z_i and 52 ℓ₀ at z = 10, which fits weak growth
  ×37.8 rather than the EdS ×100, and baryon-enriched peaks. A quantitative check is a linear two-fluid calculation (not
  done here).
- **Footings.** a₀ enters only through t₀ and M₀; in code units this changes the field time scales relative to the Hubble
  time, not the screening ratio. At the same grid the alt-footing weak peaks are 2.3% below canonical and the strong
  peaks differ by +0.8% (8³) to −1.3% (32³).

## 6. Queue jobs

**Round 1 (done 2026-10-24/29, 6 jobs).** The commands are in `ENQUEUE_commands.txt`: alt 64³ ×2 and 128³ ×4, at est-gb
0.5 / 3.1, threads 4 / 8, priority 254–259. All exited 0. The queue measured peaks of 0.376–0.380 GB (64³) and
1.93–2.11 GB (128³). Wall time was 6.5 min (64³), 2.8 h (128³ canonical strong) and 3.2 h (128³ alt strong). The
canonical 128³ pair is INIT-FAIL (A4).

**Round 2 — ENQUEUE (A4 reruns, 2 jobs; this lane does not enqueue).** After they land, run
`/usr/bin/python3 analyze.py` (it reads `runs/ladder_a4/` over `runs/ladder/`) and commit the new result files and
`LADDER_RESULTS.json`.

```bash
python3 compute_queue/heavyq.py add --id W1A4_n128_strong_can --cwd rebuild_2026_10_22/W1_pmedium_3d_scaleup \
    --cmd "/usr/bin/python3 engine/pmedium3d.py --n 128 --amp 0.03 --footing canonical --threads 8 --outdir runs/ladder_a4" \
    --resume-cmd "/usr/bin/python3 engine/pmedium3d.py --n 128 --amp 0.03 --footing canonical --threads 8 --outdir runs/ladder_a4 --resume" \
    --est-gb 2.6 --threads 8 --priority 259 --done-file runs/ladder_a4/n128_strong_can/result.json --grace 900 \
    --note "W1 lane A4 rerun n128_strong_can (INIT-FAIL fix); checkpoint 336 MB (+ final_state.npz 336 MB)"

python3 compute_queue/heavyq.py add --id W1A4_n128_weak_can --cwd rebuild_2026_10_22/W1_pmedium_3d_scaleup \
    --cmd "/usr/bin/python3 engine/pmedium3d.py --n 128 --amp 0.001 --footing canonical --threads 8 --outdir runs/ladder_a4" \
    --resume-cmd "/usr/bin/python3 engine/pmedium3d.py --n 128 --amp 0.001 --footing canonical --threads 8 --outdir runs/ladder_a4 --resume" \
    --est-gb 2.6 --threads 8 --priority 258 --done-file runs/ladder_a4/n128_weak_can/result.json --grace 900 \
    --note "W1 lane A4 rerun n128_weak_can (INIT-FAIL fix); checkpoint 336 MB (+ final_state.npz 336 MB)"
```

## 7. What Codex's lanes should do next

See `NOTE_FOR_CODEX.md` (in this directory). In short: use this engine (bit-identical to SE, preemptible); stop grading
convergence by the cell maximum and use fixed physical aperture masses; the quiet one-mode seed in this box reaches
turnaround, not a core, by z = 10, with the medium in its linear regime — a core test needs either evolution past
turnaround to virialization, or seeds/box chosen so the collapsed region reaches ~10³–10⁴ × mean density with ≥ 4 cells per
ℓ₀ (n ≳ 210 in this box at z = 10), and then the certificate (`Model.certificate`) read at stationarity. The
converged alt ladder shows the core does not appear by refinement alone: the region is resolved and converged, and it is
at turnaround.

## Files

`FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md`, `AMENDMENTS.md` (A1 pairwise order; A2 speed-up after the first probe and
the re-established evidence; A3 resolution readings, the 605 s overrun, ENQUEUE estimates; A4 canonical 128³ INIT-FAIL
and the restart fix); `PROVENANCE.json`,
`REPRO_RESULT*.json`, `repro/`; `engine/`; `gate.py`, `gate_results*.json`; `resume_test.py`, `resume_test_n*.json`;
`probe.py`, `probe_n64_*.json`; `selftest_cert.py`, `selftest_cert*.json`; `ladder.py`, `runs/ladder/*/result.json`,
`runs/ladder/ladder_log.json`, `ENQUEUE_commands.txt`, `ENQUEUE_A4_commands.txt`; `analyze.py`, `LADDER_RESULTS.json` (both resolution readings),
`LADDER_RESULTS_MUTATE.json` (planted defects caught); `NOTE_FOR_CODEX.md`. Final states (`*.npz`) are not committed.
Nothing here says the data favour the framework; no data were used. Not "theory closed".
