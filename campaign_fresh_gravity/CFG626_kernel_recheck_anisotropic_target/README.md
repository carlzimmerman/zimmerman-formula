# CFG626: kernel re-check of CFG620 (anisotropic maximum-entropy velocity target) with the repaired nu_mono

**Criteria:** `FROZEN_CRITERIA.md`, committed alone first (1c69c8300). CFG620's results and the external orbit-selection review
(`sol61_push/orbit_selection_2026_10_11/REPORT.md`, read as data) were seen before the freeze and are stated there.

**Method.** CFG620's pipeline (`cfg620.py`, `cfg620_lib.py`) is imported read only and run unchanged by the thin driver
`cfg626.py`. The only change is the kernel. The exponential form 1/(1 - exp(-sqrt y)) is replaced by the repaired nu_mono,
built verbatim from `CFG596_lean_pm_1024/cfg596_pm.py` (Y_P = 2.5396, DELTA = 0.05). The swap reaches:
- CFG544 `nu_m1`, so every use of `Mph_enc`;
- CFG541 `nu_m1`, so `Model`, r_* and dW;
- the CFG544 copy inside CFG550/CFG554;
- CFG620's `law_S`.

Cell geometry comes from CFG541's own `Model` in both modes.

**Settings.** kappa = 1/2 is FITTED. The footings (9.3603e-11 can / 1.1312e-10 alt) are never pooled. The cold energy's mass is
still required. No dark-matter particle. This is not a closed theory. Every number below is read from `cfg626_crep.json`,
`cfg626_results_mono*.json`, `cfg626_compare.json` or CFG620's committed JSON (the exp column).

## Reproduction control C-REP: PASS

The exp kernel through the CFG626 driver reproduces CFG620 **exactly**:
- the cells (r_*, M_cat, dt, C4, r99, r_pk) and dW: relative deviation 0;
- CS, Part S and Part N (solver errors, beta medians, edge ratios, every LP d_min): identical;
- the 18 bench runs (A_C_a1.0 to 13.8 Gyr, b_C, C2p, in all 6 cells): maximum absolute deviation 0.0 at every read.

The kernel table matches the exponential form to 5.7e-9 for y <= 2. It first departs by > 1e-3 at y = 2.57. nu_mono/nu_exp is
1.011 at y = 5, 1.023 at y = 10 and 1.019 at y = 30.

## Side by side (exp = CFG620; mono = this lane; can / alt)

| headline | exp | mono | verdict |
|---|---|---|---|
| 1. Hollow exists (cluster, compact; Part S and toy) | yes in all 4 cells | **no in all 4** (monotone; the law profile has an inner cusp) | **KERNEL-DEPENDENT** (both footings) |
| 2. Hollow / inner region held by FIX-A (H, IC-B) | cluster +0.006 / +0.001; compact +0.029 / -0.013 | inner region r < r_pk,exp: cluster +0.005 / -0.000; compact -0.015 / -0.012 (held) | **KERNEL-DEPENDENT** (see below) |
| 2'. FIX-2 (forced isotropy) overfill of that region, H at B / C | cluster +0.44/+0.41, +0.43/+0.42; compact +0.37/+0.37, +0.38/+0.38 (>= 0.3: overfills) | cluster +0.20/+0.18, +0.20/+0.19; compact +0.13/+0.11, +0.15/+0.14 (< 0.3) | dependent |
| 3. Anisotropy: median beta for 0.05 r_M <= r < r_pk,exp | cluster -5.82 / -5.82; compact -0.73 / -0.58 | cluster -0.077 / -0.077; compact **+0.005 / +0.006** | **KERNEL-DEPENDENT** |
| 3. LP ISO d_min in that region (isotropic support exists iff <= 0.02) | cluster 0.82 / 0.82 (none); compact 0.024 (none) / 0.000 (binning artefact) | 0.000 in all 4 (exists) | dependent |
| 3. Bulk median beta; edge sigma_r^2/sigma_t^2 | cluster -0.26; edge 0.015 / 0.029 | cluster -0.072; edge 0.022 / 0.029 | (cluster bulk exceeds 0.1 under exp) |
| 4. Edge, frozen times (FIX-A alpha 1, B / C) | cluster +0.120/+0.125 can, +0.079/+0.129 alt: SOFTENED | cluster +0.124/+0.125 can, +0.083/+0.129 alt: SOFTENED | **ROBUST** |
| 4. Edge at 13.8 Gyr, alpha 1, 2 (all 24 runs) | -0.013 to +0.066 (all sharp) | -0.013 to +0.063 (all sharp) | robust |
| 5. G550 at frozen times, per cell (B, C) | can: MW FF, cl PF, cp FF; alt: MW FF, cl PP, cp **PF** | can: same; alt: MW FF, cl PP, cp **FF** | can **ROBUST**; alt **DEPENDENT in detail** (compact_alt IC-B d logX_J -0.0480 to -0.0501, against a 0.05 limit); target label robust |
| 6. Steady and sharp by 13.8 Gyr at alpha >= 1 | 24/24 | 24/24 | **ROBUST** |
| 7. alpha x 0.5 (IC-B edge) | +0.49 to +0.60, all fail | +0.49 to +0.60, all fail | **ROBUST** (NOT alpha-ROBUST under both) |
| 8. Overfill P (5 Gyr) | 0.36/0.37, 0.42/0.50, 0.31/0.32 | 0.36/0.38, 0.43/0.49, 0.33/0.32 | **ROBUST** (NOT HANDLED) |
| 9. KiDS edge reading (sharp row, CFG559 kinetic gain withdrawn) | sharp branch | sharp branch | **ROBUST** |

Row 4's per-footing frozen-time label also counts as robust. Under both kernels, the 13.8-Gyr edge is sharp on both footings.

**Reported, no verdict weight:**
- Energy is COMPATIBLE under both kernels: IC-B net 0.25 to 0.40 under mono, against 0.25 to 0.39 under exp.
- No blow-up under either kernel.
- The Lyapunov largest rise is 0.0136 (mono) against 0.0131 (exp).
- FIX-AG H, cluster: +0.13 (mono) against +0.27 to +0.28 (exp). Compact: -0.06 to -0.01 (mono).
- Part S and Part N are self-consistent in all 6 cells under mono. The mono solver errors are at 1e-15, against CFG620's
  cluster_alt Part N miss of 1.9e-3.
- The inner region holds about twice the law mass under mono: compact 12.3 against 6.5 particles, cluster 239 against 113.

## Verdict per headline

- **KERNEL-DEPENDENT** (both footings):
  - the hollow;
  - the meaning of "hollow held";
  - the tangential anisotropy (beta -0.6 to -5.8);
  - the isotropy obstruction (LP ISO, and FIX-2's 10^0.37–0.44 overfill).

  Under the repaired kernel, the compact and point-mass halos have an inner cusp, not a hollow. The maximum-entropy target there
  is nearly isotropic (cluster beta of about -0.08, compact beta of about 0), and locally isotropic support exists (d_min 0).
  Forced isotropy (FIX-2) overfills that region only by 10^0.11–0.20, below the frozen 0.3 tooth. CFG620's "anisotropy is what
  holds the compact hollow" is therefore a property of the exponential kernel. This agrees with the external review's
  statement.
- **KERNEL-ROBUST** (both footings):
  - the frozen-time edge label (SOFTENED) and the sharp 13.8-Gyr end state;
  - the target label INCONSISTENT (steadiness at 10 / 5 Gyr);
  - the steady, sharp settling by 13.8 Gyr at alpha >= 1;
  - NOT alpha-ROBUST at alpha x 0.5;
  - overfill NOT HANDLED;
  - the KiDS reading, which withdraws CFG559's kinetic gain. It is now a same-kernel reading, because CFG559's KiDS profile
    already used nu_mono.
- **G550 per-cell pattern:** robust on can, dependent on alt in one borderline cell (compact_alt IC-B). It does not change any
  label.

## Frozen label

The six labels are unchanged: target INCONSISTENT, edge SOFTENED, works in compact NO, overfill NOT HANDLED, NOT alpha-ROBUST,
Lyapunov NOT ESTABLISHED.

The control summary flag `controls_pass_CS_read_outside_layer` changes from true to false. The only cause is C5, the
exponential-kernel reproduction of CFG544, which cannot hold under mono by construction. The criteria replace C5 with C-REP, which
passes. With that replacement the mono control reading is the same as CFG620's:
- CS outside the layer: pass;
- C2' pass (|D| <= 0.004, |log X_J| <= 0.022, edge -0.006 to -0.007);
- mass exact;
- C4 at about 1e-4 (CFG544 precedent);
- as frozen: NO LABEL, as in CFG620.

Under mono the target label's hollow item is the inner-region item (held in all 4 cells), so that item is not what makes the label
INCONSISTENT. G550 steadiness is.

## MUTATE (mono, exit 0)

- **MI: does not bite.**
  - (a) is vacuous: there are no Part S hollow cells.
  - (b) edge bites: FIX-2's edges are +0.22 to +0.43.
  - (b) hollow fails: FIX-2's inner H is +0.11 to +0.20, below 0.3.
- **MF: bites.** Its LP part is vacuous (no hollow). The bench arm fails the edge in every cell (+0.25 to +0.50).
- **MT: bites.**

Under exp, MI also did not bite, but for a different reason (marginal compact LP).

## Disclosures (dated 2026-10-11)

1. The inner-region fallback was triggered in all 4 formerly hollow cells. It was declared in the criteria. In code units the
   inner radius is 0.0405 r_* for the cluster and 0.0038 / 0.0036 r_* for the compact cell.
2. Under mono, r_* moves by less than 2e-7 relative and dW changes slightly. Both come from CFG541's Model with the repaired
   kernel.
3. Sympy K4 is the exponential-kernel KINETIC_GATE identity. It is kept unchanged and passes, but its premise does not apply to
   the repaired kernel.
4. Toy limits are those of CFG620 and CFG544. In particular the compact inner region holds about 12 particles under mono, against
   6 under exp.
5. Machine: 2 processes, about 1.2 GB total RSS, `nice -n 10`. The cfg596 and cfg625 jobs were not touched. Console logs were
   deleted. The work directory is `../_external_data/cfg626_work/`.

## Files

- `cfg626.py`: the driver. Set `CFG626_KERNEL` to mono or exp and `CFG626_MODE` to main, mutate or crep.
- `cfg626_compare.py`: the side-by-side table and verdicts.
- `cfg626_results_mono.json`, `cfg626_results_mono_MUTATE.json`, `cfg626_mono.out`, `cfg626_mono_MUTATE.out`.
- `cfg626_crep.json`.
- `cfg626_compare.json` and `cfg626_compare.out`.
