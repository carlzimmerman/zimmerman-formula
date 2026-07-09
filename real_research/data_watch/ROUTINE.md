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
| **DESI w(z)** (the hostage) | DESI dark-energy equation of state. DR2 (3-yr) w(z) public 2025 = the current 4σ+ evolving-DE tailwind; **full 5-yr-survey results expected 2027** (survey finished Apr 2026; no firm "DR3" date yet) | **evolving** DE (w≠−1) consistent with the a₀(z) ρ_DE(z) curve | **reverts to w=−1** → the distinctive content vanishes (theory degenerates to ordinary MOND) |
| **EFE evolves with z** *(corrected 2026-06-09)* | external-field dependence of high-z grouped-galaxy kinematics | a clean **z-dependent** embedded-vs-isolated offset (~0.03–0.06 dex, QUMOND; realization-dependent) | a **z-independent** offset disfavours (the deep-MOND EFE is set by g_ext/g_bar, not g_ext/a₀ — see `EFE_VS_Z_CORRECTION_2026-06-09.md`) |
| **z≈0.4 a₀ bump** | intermediate-z TFR/RC (MUSE-DARK, JWST) | a₀ **peaks +6% near z≈0.4** then declines | **monotonic** a₀(z), no bump |
| **Cluster residual** | eROSITA eRASS2/3, cluster lensing + matched WL+HSE+kinematic at R500 | residual **reconciled** to η~1 at a₀=9.36e-11 (missing baryons / IGIMF / the AeST field) | η(R500) robustly **≥2** in a matched 3-probe analysis **AND framework-specific** (a *shared*-MOND ~2× is NOT a clean kill — see context) |
| **Lensing RAR** | WL radial-acceleration relation. Needs a **calibrated shear catalog + photo-z over ≳1000 deg²** (the Brouwer+2021 KiDS-1000 bar, arXiv:2106.11677). Vehicle CONFIRMED (2026-06-24, from EUCL-ESAC-CR-9-001 rev 1.3 "releasable" product list + DR1-memo EUCL-EST-ME-8-020): **Euclid DR1 ships public shear catalogs over ~1900 deg² (~2× KiDS-1000)** — two pipelines, `DpdSheLensMcFinalCatalog` (LensMC) + `DpdSheMetaCalFinalCatalog` (Metacalibration), plus photo-z (`DpdPhzPfOutputCatalog`) and baryonic photometry/morphology (`DpdMerFinalCatalog`) = the full Brouwer recipe. DR1 in two tranches: **first ~Nov 2026, full mid-2027**; the open variable is now *how much* of the 1900 deg² is WL-**complete** per tranche (gated on external ground-based photo-z; some ice-contam data invalidated), NOT whether shear ships (corrects the earlier "no shear yet" read). DR1 delivers catalogs not the RAR curve — the measurement is a downstream VAC (expect a Brouwer-style paper within months of the shear drop). **Rubin: DESC WL value-added catalog / DR1 — ~2027** (DP1≈15 deg² and DP2≈3000 deg² coadds carry pipeline shapes but are methods-grade, not science shear — SITCOMTN-162). **Trigger on the *first* ≳1000 deg² calibrated shear+photo-z that is WL-complete, not the image drops.** | lensing RAR at the **same a₀** (+ saturation α_∞) | a **different a₀** or large intrinsic scatter |
| **s^TX SME dipole** *(added 2026-06-21)* | gravity-sector SME s̄^μν bounds (Gaia DR4 asteroid astrometry, extended INPOP/EPM, ~2028–32) | a CMB-apex-locked **negative s^TX** dipole consistent with **8.7×10⁻¹⁰ at Saturn-a** (a₀/2\|a\| per body) | a next-gen s^TX fit reaching ~10⁻¹⁰ whose central value is **inconsistent** with 8.7×10⁻¹⁰ → kills the preferred-frame realization |
| **Cassini / Solar System** | post-Newtonian / quadrupole bounds (BepiColombo) | the **a₀/2 channel** read as modified-INERTIA evades (~3 orders safe) | a covariant completion forced to violate **\|γ−1\| < 2×10⁻⁵**, or the a₀/2≈4.7×10⁻¹¹ residual detected as modified-GRAVITY (Kepler-III, ~3.7 orders) |
| **Koide pole drift** *(flavor-side TRACKING, not framework-distinctive; added 2026-06-26)* | PDG charged-lepton mass updates — esp. **m_τ** (Belle II / a future τ-charm factory) → recompute the pole Koide Q = Σmₗ/(Σ√mₗ)², σ_Q, and n-σ from 2/3 | pole Q **stays pinned at 2/3** as σ_Q shrinks (currently 0.66666051, −0.9σ, σ_Q≈6.8×10⁻⁶, τ-limited) → reinforces the at-2/3 + high-μ-drift reading | improved m_τ pulls pole Q **away from 2/3 toward Singh's EJA +0.374% pole-tilt** → the at-2/3 reading dies, shape-hosting disfavored vs the rival EJA |
| **Attribution / priority scoop** *(added 2026-07-07 — not a physics verdict; a credit/priority flag)* | new arXiv/journal work reproducing Carl's **distinctive fingerprints** — the horizon reframing **a₀ = c²√(Λ/32π) = 9.36×10⁻¹¹**, a₀ = cH_Λ/Z, the dS-Unruh interpolation **g_obs=√(g_bar²+g_bar·a₀)**, or the SME s^TX-dipole induced realization — *without* citing his Zenodo DOIs (10.5281/zenodo.**20576485** framework + the a₀(z)/theory/κ set) | n/a (this row flags CREDIT, not truth) | **FLAG**: a paper presents ≥1 distinctive fingerprint above as its own **with no citation** to Carl's DOIs → surface title/authors/id + which fingerprint + verbatim overlap if any. *Note the legal reality: equations/physical facts are not copyrightable — this catches missing-attribution / priority-scooping / verbatim-prose reuse, which is an academic-norms + (for copied text/figures) copyright-of-expression matter, not equation ownership.* |

Already-settled context (don't re-litigate — updated 2026-06-21):
- **Clusters** are a **shared relativistic-MOND gap, NOT a framework-specific failure** — the theory program is closed (cosmic-density route excluded, the AeST phase-pin no-go is airtight), η(R500) is bracketed **[1.0, 2.33]** (consensus ~1.6–1.8 after the framework's own Y-Q field), and the residual is the AeST dark-sector doing a CDM-like job (the pure-"no dark matter" reading is forfeited, the field HAS the 1.46× mass but can't be galaxy-safe AND cluster-clumpy). So a ~2× residual is **expected and shared**, not a clean kill — watch the *magnitude* (matched 3-probe / WL-vs-hydro), not the existence.
- **a₀(z)** is **non-diagnostic, hostage to DESI w(z)**: DESI DR2 (2025) is a **tailwind on the bump-then-decline SHAPE** (2.8–4.2σ evolving DE, DESY5 reproduces +6%/−26% to the digit), but **MUSE-DARK III (Ciocan+2026) is a REAL ~30σ weakening tension** favoring the rival rising branch over 0.5<z<1.44 (it survives its own robustness — NOT merely "ΛCDM-degenerate"), and it all **dissolves to constant-a₀ MOND if w→−1**. The decisive clean test is the **z≳3 BTFR-offset sign**.
- **NEW gravity-side fronts (2026-06-21):** the **s^TX SME boost-dipole** is LIVE at **~1.5×** the tightest published bound (preferred-frame/LV test, MOND-shared; Gaia DR4 ~2028–32); the genuinely MI-vs-MG-distinctive Cassini content is the separate **a₀/2 channel** (~3.7 orders, MI evades / MG excluded, in hand); the **CMB-apex RAR-dipole** (0.062%, fixed sky direction l=264°/b=+48°) is the framework-UNIQUE signature but **below every near-term floor** (systematic-limited).

---

## The daily procedure
1. **Fetch arXiv:** `python real_research/data_watch/arxiv_watch.py --days 2` → new, deduped candidate papers (it marks them seen so they aren't re-reported).
2. **Check announcements:** a quick `WebSearch` for same-day collaboration **data-release news / press releases** (DESI, Gaia, ELT/HARMONI, JWST, ALMA, MUSE-DARK, eROSITA, Euclid, Rubin) — arXiv misses these.
2b. **Sweep the top science magazines** for same-day coverage bearing on a watch item — they often surface a result (and its framing) before or alongside the arXiv/press-release channel, and catch non-collaboration commentary. `WebSearch` the watch topics (dark energy w(z) / DESI, MOND / modified gravity / modified inertia, galaxy rotation curves & acceleration scale, wide binaries, Tully–Fisher) scoped with `allowed_domains` to: **quantamagazine.org, scientificamerican.com, nature.com, science.org, physicsworld.com, skyandtelescope.org, astronomy.com, space.com, phys.org, cerncourier.com, symmetrymagazine.org**. (Note: `newscientist.com` and `arstechnica.com` are currently blocked to the crawler — omit them or they 400 the whole call.) Only count items **dated today/this window**; trace any magazine story back to its underlying paper/release and assess *that* on the framework's footing — never grade the headline.
2c. **Attribution / priority scan.** In the arXiv batch (and the magazine/announcement results), flag any item that presents one of Carl's distinctive fingerprints — **a₀ = c²√(Λ/32π)**, the value **9.36×10⁻¹¹ m/s²** derived from the horizon/dark-energy density, **a₀ = cH_Λ/Z**, the dS-Unruh interpolation **g_obs=√(g_bar²+g_bar·a₀)**, or the SME s^TX-dipole induced realization — as its own result **without citing his Zenodo DOIs** (framework 10.5281/zenodo.20576485 + the a₀(z)/theory/κ set). Report it under **FLAG** (not a physics verdict): title, authors, id, which fingerprint, and any verbatim prose/figure overlap. Do **not** contact anyone or take any action — this is a surfacing-only flag for Carl to decide on. (Legal reality, so the flag stays honest: bare equations/physical facts aren't copyrightable; what's actionable is missing academic attribution / priority, and — only if text or figures are copied verbatim — copyright of *expression*.)
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
