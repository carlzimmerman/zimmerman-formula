# NUF1 — the neutrino-mass floor against DESI DR2 BAO + the compressed CMB prior (geometry only)

Criteria, run script and collector: 84c613b81a (alone first, before any real-data number). No amendment.
Result: `RESULT.md`; labels `nuf1_collect.out`, `nuf1_results.json`. Per-run files `nuf1_<MODE>.{json,out}`.
A test of flat ΛCDM on its own terms. It adopts nothing and edits no ledger; framework footings do not enter.

**Verdict: FLOOR DISFAVOURED / FRAGILE.** Best-fit effective neutrino mass −0.145 eV (68 % −0.228 to −0.060); the
normal-ordering floor 0.059 eV sits at Δχ² 4.38 (2.1σ), the inverted floor 0.10 eV at 6.59. Dropping LRG2, or using the
Lyα AP pair instead of the Lyα BAO pair, makes the floor ALLOWED. All four known-answer checks pass. Without CMB lensing
this is weaker than DESI's 3.0σ, as expected, and it is the same BAO-against-CMB mismatch as the evolving-dark-energy
hint, not an independent one.

Sources (TeX, downloaded 2026-11-13): arXiv:2503.14738 (BAO table, compressed CMB prior, K1 / K2A / K2B targets),
arXiv:2503.14744 (DESI's effective-mass result and the floors, citing NuFIT 6.0), arXiv:2407.10965 (effective-mass
definition), arXiv:2607.27410 (Lyα AP pair).

## Commit ids and re-run check

- Frozen criteria + scripts: local 84c613b81a, origin 5cc8f61272.
- Result: local b6a0fc4d34, origin ed0509d6f9.
- The lead session re-ran `python3 nuf1_run.py primary` on 2026-11-13 after the result was committed: the output is identical to the committed `nuf1_primary.out` and `nuf1_primary.json` except for the runtime line (best m -0.1450 eV, Delta chi2 4.378 at 0.059 eV and 6.594 at 0.10 eV, FLOOR DISFAVOURED).
