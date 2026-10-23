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
