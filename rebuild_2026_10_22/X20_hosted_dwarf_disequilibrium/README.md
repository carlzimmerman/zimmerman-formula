# X20_hosted_dwarf_disequilibrium: is the hosted-dwarf extra tides or binaries?

## Verdict

**NOT SUPPORTED, on both footings.** The hosted dwarfs' extra over the isolated law is neither tidal disequilibrium nor
binary inflation. Their X19 labels (EXTRA) stand, and so does X19's "no low-dimensional selector".

| test | canonical | alt | JSON key |
|---|---|---|---|
| T1: Spearman(E, log τ), same-host permutation p | +0.003, p 0.11 | +0.012, p 0.10 | `footings.<f>.T1` |
| T2: equilibrium subset τ ≤ 0.1 (PRIMARY) | N 54, +0.480 ± 0.083, Z 5.8 **EXTRA** | N 54, +0.445 ± 0.082, Z 5.4 **EXTRA** | `footings.<f>.T2["0.1"]` |
| T2 reported, τ ≤ 0.03 / 0.3 | Z 5.6 / 6.0, EXTRA | Z 5.3 / 5.6, EXTRA | `T2["0.03"]`, `T2["0.3"]` |
| B: σ factor needed (UFD / bright M31 / M31 others) | 0.50 / 0.78 / 0.41 | 0.54 / 0.81 / 0.45 | `footings.<f>.B` |
| B: binary room left after X1 (σ_f07/σ_free) | median 0.92, min 0.82 → **CANNOT** for all three | same | |

κ = ½ FITTED. Footings never pooled. Not "theory closed". Nothing here says the data favour the framework.

**Checks 9/9 PASS** (K0 reproduces X19's plain medians exactly; K1 g_obs round trip 0.012 dex; K2 positive control
p = 5e-5; K3 negative control 99 % / 98.5 % of shuffles p > 0.01; K4 0.27 GB). `--mutate` fails K0 on both footings, exit 1.

## What it says

- **Tides.** Most hosted dwarfs sit far inside their own pull: median τ = g_tid/g_iso = 0.012, and 54 of 61 have τ ≤ 0.1.
  The excess does not rise with τ (ρ ≈ 0), and the most tidally safe dwarfs carry the same excess as the rest
  (τ ≤ 0.03: +0.49 dex, N 44). The two systems at τ > 0.3 are the only ones near zero.
- **Binaries.** Erasing the classes needs σ cut by 0.41–0.81. X1 already applied the Arroyo-Polonio free-f correction; going
  to f = 0.7 removes at most a further 18 % (median 8 %). Even the full f07/f0 range (median 0.78, min 0.51), ignoring X1's
  correction, reaches only the bright M31 class's need.
- **Qualifier (A3).** τ uses the current host distance, a lower bound on the orbit's peak tidal stress. τ ∝ 1/d², so a
  pericentre at d/3 raises τ ninefold. The median would then be about 0.1: still mostly safe, and T1 is about ranks, which
  a uniform rescaling does not change. Orbit-by-orbit pericentres are not on disk.
- Reported: Spearman(E, ellipticity) +0.16 (60 systems), weak. Crater II (τ 0.18, E −0.44) and Sagittarius (τ 1.4,
  E −0.15) are the tidally exposed ones, and they are *below* the law, not above it.
- Mutate side note (no weight): against the B_EFE baseline the same machinery returns PARTIAL, because the EFE prediction
  itself depends on the host field (shared with τ). That is by construction, which is why the verdict runs on B_iso.

## Files

`FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md` (87b6832e84, before any number); `x20_hosted_dwarf_disequilibrium.py`;
`.out` / `_results.json`; `_MUTATE` outputs.

    OMP_NUM_THREADS=1 python3 x20_hosted_dwarf_disequilibrium.py            # exit 0, 9/9
    OMP_NUM_THREADS=1 python3 x20_hosted_dwarf_disequilibrium.py --mutate   # exit 1, K0 fails
