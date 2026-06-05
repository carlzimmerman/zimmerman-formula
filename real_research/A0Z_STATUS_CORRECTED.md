> **⚠️ FURTHER SUPERSEDED (2026-06-05) by [`A0Z_MUSE_DARK_III_CONFRONTATION.md`](A0Z_MUSE_DARK_III_CONFRONTATION.md)**
> (+ `reviews/project_a0z_MUSE_DARK_III_confrontation.py`). That file fixes the deeper error this whole document
> shares: it treats the **rising** a₀∝cH(z) as "the framework's prediction." It is **not** — the **canonical**
> reading is a₀=(c/2)√(G·ρ_Λ), which is **constant (ΛCDM) / declining (DESI)**; the rising ∝E(z) branch is the
> ρ_total footing-bug. So MUSE's rise is in tension with the *canonical* reading and *overshoots* the rising
> branch. Verified significance is ~30σ on the authors' offset (~15σ on the slope), not the "~19σ" below. Net
> grade: **WEAKENED & CONTESTED, leaning unfavourable** — the rise is real but ΛCDM-degenerate, so a₀(z) neither
> confirms nor cleanly refutes the framework. The "a₀ rises ≈×3 = confirmed" verdict below is **retracted**.
>
> **⚠️ SUPERSEDED IN PART (June 2026) by `reviews/project_a0z_reconciled.py`.** A primary-literature sweep with
> corrected attributions overturns two claims below: (1) **"constant-a₀ MOND is excluded" is FALSE** — McGaugh+
> 2024 (arXiv:2406.17930) and Milgrom 2017 (arXiv:1703.06110) favor constant a₀, the mainstream position; (2)
> **"Mayer confirms the framework" is WRONG** — Mayer+ **2022** (arXiv:2206.04333) is a *ΛCDM simulation* whose
> apparent-a₀ rise *favors ΛCDM and is used to reject constant-a₀ MOND*; the framework's rise is degenerate with
> ΛCDM, not confirmed. The strongest measured rise (MUSE-DARK III 2026, arXiv:2604.22613) is real (~19σ) but runs
> *faster than cH(z)*, is read as ΛCDM by its authors, and has a +0.45 dex stellar-mass escape hatch. Honest net:
> a₀∝cH(z) is **consistent-with-but-not-confirmed and in genuine tension** with the mainstream high-z data — not
> killed, but contested and leaning unfavorable. Read `project_a0z_reconciled.py` for the corrected status.

# a₀(z) Status — Corrected After Further Research (Mayer 2023 sims; MUSE multi-halo robustness)

**C. Zimmerman, June 2026.** *An honest correction. Further research undercut the "a₀ is flat / MUSE's rise is a
DC14-halo artifact" line I pushed in `project_evolution_derived.py`, `project_a0z_model_independent.py`, and
`project_density_evolution_test.py`. This document is the authoritative, corrected status. Numbers:
`reviews/project_*` and the comparison reproduced inline.*

## What forced the correction

Two findings from continued research:
1. **MUSE-DARK III is robust across halo models.** Their own Appendices D/E: *"A larger value of a₀|z∼1 is found
   regardless of the model used to derive the total and baryonic accelerations"* (DC14, NFW, Burkert). So the
   rising a₀ is **not a DC14-specific artifact** — my central mechanism for dismissing it is weakened.
2. **Independent ΛCDM hydro simulations find a₀ rises.** Mayer et al. (2023): a₀ grows by **~×3 from z=0 to z=2**.
   That **matches the framework's *original* bare apparent-horizon prediction** (α=1, a₀ ∝ E(z), E(2)=3.03) — and
   **disfavors the "dynamical-flat" refinement I proposed last turn** (×1.2).

## The corrected comparison (a₀(z)/a₀(0) at z=2)

| prediction / measurement | ×at z=2 | status |
|---|---|---|
| constant-a₀ MOND (standard) | 1.0 | **excluded by all** |
| framework *dynamical-flat* (my last turn) | 1.2 | **disfavored by sims — I over-corrected** |
| a₀ ∝ (1+z)^0.75 (some sims) | 2.3 | mild, in framework band |
| **framework bare apparent, a₀ ∝ E(z) (ORIGINAL)** | **3.0** | **= Mayer sims; confirmed** |
| Mayer et al. 2023 hydro sims | 3.0 | independent ΛCDM sim |
| MUSE-DARK III (measured) | 4.0 | ~30% above framework/sims |

## What I got right, and what I over-claimed

- **Right:** a₀ **evolves (rises)** — this excludes standard *constant*-a₀ MOND, and the literature agrees MUSE
  rises "faster than H(z)." Galaxy compaction **does** contribute to the f_DM drop (a real effect).
- **Over-claimed:** that a₀ is ~**flat** and MUSE's rise is a **DC14 artifact**. It is not: MUSE is robust across
  DC14/NFW/Burkert, and independent hydro sims find a₀ ×3. So a₀ **genuinely rises ~×3** (= the framework's bare
  α=1). My density-evolution argument was a **valid alternative** (the inner f_DM *can* be flat-a₀ + compaction),
  **not an exclusion** of the rise — and the full-RAR + sim evidence disfavors the flat alternative.

## Corrected framework status (the a₀(z) front)

- **Genuine positive:** the framework's *original* prediction **a₀ ∝ cH(z) ∝ E(z)** (α=1, ×3.0 at z=2) is
  **independently confirmed by ΛCDM hydro simulations** (Mayer 2023, ×3), and **excludes constant-a₀ MOND**. The
  framework predicted an evolving a₀ before the measurements; a₀ does evolve, at ≈ the predicted rate.
- **Residual tension:** MUSE measures **×4** — ~30% above the framework/sims **×3**. Compaction-conflation may
  explain *part* of the excess, but not all (multi-halo robust). **Unresolved.**
- **Honest limit on distinctiveness:** the framework's α=1 does **not** distinguish it from ΛCDM (the hydro sims
  also give ×3). It distinguishes from *constant*-a₀ MOND. So "a₀ rises" is now a **confirmed but not
  framework-unique** result; the framework's distinctive content lives in the *coefficient* (Z = cH₀/a₀, the
  a₀–H₀ link) and the *origin* (emergent horizon), not in the mere fact of evolution.

## Net

I flip-flopped on the *rate* this session (rising → declining → rising → flat → **rising**, ×3) as data and
theory came in; the robust, now-best-supported statement is: **a₀ evolves and rises ≈ ×3 from z=0 to z=2 (α≈1),
confirmed by hydro sims, matching the framework's original a₀ ∝ cH(z); MUSE's ×4 is ~30% high and unresolved;
constant-a₀ MOND is excluded.** The previous "flat / artifact" docs are superseded by this one on the *direction*;
their identification of compaction as a *contributing* systematic stands.
