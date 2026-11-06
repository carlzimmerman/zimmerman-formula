# EB1_seed_epoch: can the law's web rule form A2744-QSO1's seed in time?

Criteria 7ac6bbb3f9 (alone, before any script), script 0f55942e3a before any run, Amendment A1 77f1c1ba5f (K2 was
vacuous as frozen; restated before the main run). Kappa = 1/2 FITTED. Not theory closed. No dark-matter particle,
no cold component. Nothing here says the data favour the framework. **Conditional on WG2's R1 rule, which already
fails the CMB-lensing shape (WG2-WG6), and on an isolated sphere.**

## Labels (frozen gate G1, primary cell: B2, A_s 2.1e-9, z_on 50, e = 0, TIE, eps 0.1, M_seed 1e5)

| rule | footing | log M_BH 7.7 | log M_BH 6.9 |
|---|---|---|---|
| R0 law off (Newton, baryons only) | canonical | **NO** | **NO** |
| R1 law on (WG2 QUMOND, isolated) | canonical | **EASY** (nu 1, clump 1e6 collapses z 11.29) | **EASY** (same) |
| R1 law on | alt | **EASY** (z 11.94) | **EASY** |

Checks: K1 1.68652 (EdS 1.6865) PASS; K2 (A1) final states agree to 1e-16 PASS; K3 sigma_b(1e6) converged
(CLASS grid to 692 Mpc^-1, Silk-damped) PASS; K4 EdS age 2e-16 PASS. MUTATE (G halved): K1 FAILS, exit 1 (bites).
JSON note: K1's `pass` field serialised as null (numpy bool, `default=None`); the printed run and the number
(1.68652 vs 1.6865, 0.001 %) show PASS. Fixed in EB1b's serialisation; not rerun here.

## What the numbers say

1. **Baryons alone under Newton make nothing.** No clump of 1e6-1e13 Msun at up to 5 sigma collapses by z 0, for
   every A_s, background and turn-on. sigma_b is 1.06e-3 at z 50 and flat below the Silk mass (the field has no
   small-scale power). This is the known no-cold-matter problem, seen at seed scales.
2. **Under R1 on an isolated sphere, collapse is bottom-up and almost independent of the fluctuation.**
   z_coll (3 sigma, canonical): 1e6 Msun 11.75, 1e8 7.13, 1e10 3.77, 1e12 1.58, 1e13 0.80 (alt 0.2-0.7 higher
   in z). Changing nu_pk from 1 to 5 moves z_coll by at most 0.74; A_s x4 moves it at most 0.34. Deep-law collapse goes as
   roughly delta^(-1/4) in time, so every patch of a given mass collapses at about the same epoch. Small first.
3. **The timing gate is easy in that reading.** A 1e6 Msun clump collapses at z 11.3-11.9, 378-408 Myr; Eddington
   growth at eps 0.1 (t_E 50.1 Myr) then reaches 10^7.7 by z 7.0451 (771 Myr) from a 1e5 seed. With eps 0.2 most
   cells become NO or NO (age) (t_E 112.6 Myr is too slow from any seed but 1e6).
4. **The external field decides it.** With a frozen scalar external field e = 0.03 or 0.1 a0, nothing collapses at
   any mass by z 0. WG2's own law-on box (A_s 2.1e-9 run) puts the ambient Newtonian field at 0.026 a0 at z 50 falling to
   0.006 at z 10 (corrected: an earlier draft of this line quoted 0.005-0.018 from WG2's A_s 1e-9 run). EB1 did not
   freeze that value; EB1b (criteria 0ff17cf4ce, written after this result and labelled post-result) runs it:
   **with that field nothing collapses in time; QSO1's gate is NO everywhere** (see ../EB1b_web_efe/README.md).

Other rows: B1 (baryons-only expansion) collapses much earlier (1e6 at z 26); RIVAL a0 E(z) earlier still
(1e6 at z 30.6), z_on 200 earlier (1e6 at z 19.5). All in `eb1_results.json`.

## Limits
- Isolated sphere; scalar EFE ansatz; gas pressure, cooling and fragmentation ignored (EB4, EB5).
- The 10 % clump-to-seed fraction is declared, not derived. Timing only; no abundance (EB2).
- The rule R1 is the record's web rule and it fails CMB lensing; this lane does not rescue it.

Run: `python3 eb1.py` (~25 min on a loaded machine, one thread); `EB1_MUTATE=1 python3 eb1.py` exits 1.
