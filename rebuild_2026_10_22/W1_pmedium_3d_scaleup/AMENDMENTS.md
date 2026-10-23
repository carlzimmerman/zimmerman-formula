# W1_pmedium_3d_scaleup — amendments (fix-forward; FROZEN_CRITERIA.md lines unchanged)

## A1 (PRE-RESULT for the port gate; committed before G-P1/G-P2 were run)

FROZEN_CRITERIA §2 item 1 says the C gather uses "the same sequential 27-term sum as `np.sum(axis=1)`", and §0 reports a
plumbing test showing sequential accumulation. That test used a C-contiguous (N, 27, 3) array. In SE-20261023's
`evaluate`, the product `(phi+h).ravel()[ic][:,:,None]*dc` inherits the layout of `dc`, which is a transposed view whose
27-offset axis is the contiguous one, so NumPy 1.26 reduces it with its pairwise summation (eight accumulators):
`0.0 + pairwise(t[0..26])`. A second plumbing test (scratch, one call on a perturbed 8³ lattice with random F, no lane
number) showed sequential order differs from SE in the last bit and the pairwise order matches it bit for bit. The kernel
(`engine/tsc_kernels.c`, `pairwise27`) implements the pairwise order. The governing requirement in §2 — the same
arithmetic and order as `np.sum(axis=1)` in SE's code — is unchanged; only the description of what that order is was
wrong. Plumbing also showed (one evaluation each at 8³ and 12³, before the gate): deposition, the field minimizer, the four
force arrays, the energy, the work and the diagnostics bit-identical to SE's `evaluate`.

Also recorded here (no criterion changes): the engine adds `--stop-after-steps` (a test hook that checkpoints and exits 75
at a given step, used only for the resume evidence alongside a real SIGTERM test) and writes `run_info.json` (wall-clock
fields, excluded from every equivalence comparison).

## A2 (PRE-LADDER; committed before any ladder run) — engine speed-up after the first 64³ probe, re-established evidence

Disclosure, in order:
1. G-P1/G-P2 first passed on the engine as committed in 8d552f5f2f (the A1 kernels, `-O2`; that first gate output did not
   record the engine hash, so gate.py now records it): all six configurations bit-identical to
   SE-20261023 (threads 1 and 4), the drop-h MUTATE failing (8³ strong peak 28.79 vs 2.0004). G-P3 then passed at 16³
   and 32³ after one engine fix: on `--resume` the loader had copied χ and V into C order, while the live run keeps
   them in the Fortran order `ifftn` produces; values were equal but NumPy's full-array sums depend on memory order at
   64³ (scratch test), so the loader now keeps the saved order (`np.load` already returns fresh writable arrays). The
   checkpoint/final-state `.npz` writer was made byte-reproducible (fixed zip timestamps).
2. The first 64³ cost probe (canonical strong, 200 steps) projected **633 s** (0.0580 s/step, footprint 0.366 GB):
   over the §3 limit, so 64³ was to be queued.
3. I then made the C kernels faster without changing arithmetic: indices and the shared weight product hoisted out of
   the inner loops, a branch-based modulo for in-range indices, `-O3 -mcpu=native` (still `-ffp-contract=off`,
   `-fno-fast-math`). This was motivated by the probe. Every piece of evidence was re-run on the final engine
   (`engine/pmedium3d.py` sha256 74249415…, `engine/tsc_kernels.c` sha256 db1d2772…): G-P1 PASS bit-identical (six
   configurations, threads 1 and 4), G-P2 PASS, G-P3 PASS at 16³ and 32³, a partial 64³ resume test bit-identical
   (`probe_n64_*.json`), C-S1 PASS with its mutate caught.
4. Re-probe on the final engine: canonical 64³ projects **575 s** (direct run allowed), alt 64³ projects **618 s**
   (the alt footing needs 11661 steps vs 10607, because t₀ sets t_i in code units) and is therefore **queued**. The rule
   of §3 is applied per footing as measured; no threshold was changed. The canonical 64³ runs are executed directly at
   one thread; if one exceeds 10 min of wall time, that is reported, not hidden.
5. C-S1 script: the frozen rule is |K + U| ≤ 0.10 K. The script's first version also demanded an exactly zero vacuum
   field energy, which fails at 4e-30 (deposit roundoff of a uniform lattice); that extra condition is now reported
   separately with a 1e-12 K tolerance and does not gate.

## A3 (POST-RESULT, after the direct ladder; no frozen line changed) — resolution reading, one overrun, a script fix

1. **Resolution reading.** FROZEN_CRITERIA §4 lists "R = 2.88 kpc: n ≥ 32; R = 1.44 kpc: n ≥ 64; R = 0.3215 kpc: never"
   and also defines resolved as "R ≥ 4 physical cells at z = 10". 2.88 and 1.44 kpc were rounded from 4 × 0.7206 and
   4 × 0.3603 kpc, so the literal arithmetic gives 3.996 cells at 32³ (2.88) and at 64³ (1.44): the two statements disagree
   by 0.1%. I noticed this only after the ladder numbers existed. `analyze.py` therefore reports **both** readings:
   `enum` (the enumerated n-lists, the frozen file's explicit statement) and `strict` (R_cells ≥ 4). Every verdict that
   depends on the reading is shown with both in README and LADDER_RESULTS.json (`strict_reading`). The 128³ runs make
   both readings agree for both radii (8 and 16 cells).
2. **Overrun.** The canonical strong 64³ run took 605 s of wall time at one thread (probe projection 575 s; limit 600 s);
   the weak run took 556 s. Peak footprint 0.345 / 0.349 GB. Reported as A2 item 4 promised; no result is affected.
3. **Script fix.** `analyze.py`'s first run divided by an empty-aperture mass (M_c(<0.3215 kpc) = 0 at n ≤ 32); the change
   is now `None` when the coarser grid's aperture is empty. That aperture is unresolved at every grid under both readings.
4. **ENQUEUE.** est-gb uses the largest peak footprint measured at 32³ and 64³ across ladder runs, resume tests and probes
   (0.106 / 0.376 GB), as §2.4 requires, scaled linearly in n³ to 128³ (2.542 GB) and multiplied by 1.2. The 128³ jobs add
   `--grace 900` (contract §2 permits a per-job grace) because SIGTERM is honoured at step boundaries and the 128³ initial
   minimization may outlast 300 s.
