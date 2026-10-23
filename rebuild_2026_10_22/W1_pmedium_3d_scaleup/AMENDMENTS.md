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
