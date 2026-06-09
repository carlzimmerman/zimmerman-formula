# Zimmerman Theory of Gravity — daily data-watch runbook

**Purpose.** Each day, catch any newly announced astronomy/cosmology result that would **validate or invalidate** the Zimmerman Theory of Gravity (`a₀ = c²√(Λ/32π) = 9.36×10⁻¹¹ m/s²`; published: [Zenodo 10.5281/zenodo.20576485](https://doi.org/10.5281/zenodo.20576485)). Report the verdict **in the Claude session**. This routine is self-contained and depends only on `real_research/` — never on `ai_slop/`.

> **Footing rule (the project's #1 discipline).** Judge every result on the framework's *own* terms — a₀ = 9.36×10⁻¹¹ m/s², the **ρ_DE** (dark-energy-only) footing, the **declining √ρ_DE** evolution branch, Υ≈0.70. Verify a "this invalidates it" claim as rigorously as a "this validates it" claim. When uncertain, mark **WATCH**, not a verdict. Never manufacture a hit; never reflexively dismiss one.

---

## The watch-list — what would confirm or kill each prediction
*(Source of truth: `real_research/papers/ZIMMERMAN_THEORY_OF_GRAVITY.md` §11–12 and `real_research/FALSIFICATION_MATRIX.md`. ★ = decisive / kill-door.)*

| Watch item | What to look for | ✅ VALIDATES if | ❌ INVALIDATES if |
|---|---|---|---|
| **a₀(z) decline** ★ | deep-MOND a₀ measured at z≈2–3 (ELT/HARMONI, JWST/NIRSpec, ALMA) | clean a₀(z=3) ≈ **0.74 a₀(0)**, tracking √ρ_DE, >3σ from both constant and rising | a₀(z=3) **≥ local** (flat) or **rising** ∝√ρ_total (≈×4.6 at z=3) |
| **High-z BTFR offset sign** ★ | the z=0 baryonic Tully–Fisher zero-point measured at z≳3 (JWST + ALMA) | discs ≈ **−7% in V** (−0.033 dex) **below** the z=0 BTFR | discs **at/above** the z=0 BTFR (positive or flat offset) |
| **External Field Effect (z=0)** ★ | environment-dependent rotation curves / SEP-violation tests (independent of Chae) | an **independent ≥3σ** EFE detection by a 2nd method, consistent with a₀=9.36e-11 | a clean **SEP-respecting null** in a high-dynamic-range sample |
| **Wide binaries** ★ | Gaia DR4/DR5 wide-binary gravity tests | a **robust +2–11% boost** at s_t≈9,750 AU surviving triple-rejection | a **hard Newtonian null** at the ~3–15% sensitivity |
| **DESI w(z)** (the hostage) | DESI DR3 dark-energy equation of state | **evolving** DE (w≠−1) consistent with the a₀(z) ρ_DE(z) curve | **reverts to w=−1** → the distinctive content vanishes (theory degenerates to ordinary MOND) |
| **EFE evolves with z** *(corrected 2026-06-09)* | external-field dependence of high-z grouped-galaxy kinematics | a clean **z-dependent** embedded-vs-isolated offset (~0.03–0.06 dex, QUMOND; realization-dependent) | a **z-independent** offset disfavours (the deep-MOND EFE is set by g_ext/g_bar, not g_ext/a₀ — see `EFE_VS_Z_CORRECTION_2026-06-09.md`) |
| **z≈0.4 a₀ bump** | intermediate-z TFR/RC (MUSE-DARK, JWST) | a₀ **peaks +6% near z≈0.4** then declines | **monotonic** a₀(z), no bump |
| **Cluster residual** | eROSITA eRASS2/3, cluster lensing at R500 | residual **reconciled** at a₀=9.36e-11 (missing baryons / IGIMF) | residual stays **~2×** at R500 (standing failure deepens) |
| **Lensing RAR** | weak-lensing radial-acceleration relation (Euclid, Rubin/LSST) | lensing RAR at the **same a₀** (+ saturation α_∞) | a **different a₀** or large intrinsic scatter |
| **Cassini / Solar System** | post-Newtonian / quadrupole bounds (BepiColombo) | — | a covariant completion forced to violate **\|γ−1\| < 2×10⁻⁵** |

Already-settled context (don't re-litigate): clusters and the CMB third peak are **standing failures** of pure MOND (the theory needs a covariant completion); the a₀(z) front is currently **contested, leaning unfavorable** — MUSE-DARK III (Ciocan+2026) reports an *apparent* rise that is ΛCDM-degenerate; the decisive clean test is the **z≈3 BTFR-offset sign**.

---

## The daily procedure
1. **Fetch arXiv:** `python real_research/data_watch/arxiv_watch.py --days 2` → new, deduped candidate papers (it marks them seen so they aren't re-reported).
2. **Check announcements:** a quick `WebSearch` for same-day collaboration **data-release news / press releases** (DESI, Gaia, ELT/HARMONI, JWST, ALMA, MUSE-DARK, eROSITA, Euclid, Rubin) — arXiv misses these.
3. **Assess each item** against the watch-list. Read the abstract; if it bears on a watch item, classify:
   - **✅ VALIDATES** — meets a green-column threshold.
   - **❌ INVALIDATES** — meets a red-column threshold (a *kill*).
   - **⚠️ TENSION** — points against but isn't a clean kill (e.g., contested, ΛCDM-degenerate, or systematics-limited).
   - **👁 WATCH** — relevant, could become decisive, but not yet conclusive.
   - *(skip anything not bearing on a watch item.)*
   Apply the footing rule above. State the **matched prediction** and the **specific threshold** met or missed.
4. **Report in the Claude session** (format below).
5. **Log:** append the report to `real_research/data_watch/log/{YYYY-MM-DD}.md`.

## Report format
```
Zimmerman data-watch — {date}: {X} relevant of {N} scanned

✅/❌/⚠️/👁  {Title}  ({arXiv id})
   → {watch item}: {one line — which threshold it meets/misses, on the framework's footing}
   {link}

(if none) → nothing today.
```
Keep it tight. Lead with any ✅ VALIDATES or ❌ INVALIDATES. If a genuine kill or confirmation appears, say so plainly and point to the exact prediction in the paper §11.

---

## Setup — paste this to Claude (with the repo open) to create the daily routine
> "Create a **daily** scheduled task named `zimmerman-data-watch`. Each day it runs `python real_research/data_watch/arxiv_watch.py --days 2`, then follows `real_research/data_watch/ROUTINE.md` to assess every new paper (plus a quick WebSearch for survey announcements) against the framework's pre-registered predictions, and reports **in this Claude session** anything that VALIDATES or INVALIDATES the theory — naming the prediction and threshold — or says 'nothing today'. Log each run to `real_research/data_watch/log/`."

Notes: the task runs when Claude's scheduler/host is active (if the machine is off, it runs at next activation). To pause/edit/remove it, ask Claude to update the `zimmerman-data-watch` scheduled task. To widen the net, edit the `TERMS` list in `arxiv_watch.py`.
