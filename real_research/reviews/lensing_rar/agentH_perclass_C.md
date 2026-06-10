# Agent-H refinement — per-class MEASURED conversion factors for the lensing-RAR early/late split

*Agent H for C. Zimmerman, 2026-06-10. Refines Axis 1 of `lr_battery_results.md` (the flagged "next refinement (not run)").
Bound by `lr_preregistration.md` discipline (hostility inverted; a favorable downgrade ships only if it survives; the
direction of the systematic must EMERGE from the computation, not be asserted). Script: `agentH_perclass_C.py` (+`.out`).
No git operations performed.*

## What was refined
`lr_battery.py` eroded the early/late split with a **generic** concentration bracket — constant
(C_early, C_late) = (nfw_C(10), nfw_C(1)) = (3.53, 4.33) in every bin, premised on "early types are more
concentrated → larger effective x = R/r_s → smaller C". That bracket produced the previous headline:
8.8σ → **5.0σ** (u−r) and 5.8σ → **2.1σ** (Sérsic). This run replaces the bracket with **measured per-class,
per-bin effective conversion factors** built from the actual lens populations.

**Catalog version:** the on-disk `lr_lenses.npz` is **v4** (181,477 isolated lenses — matches the v4 stage output in
`lr_stack_v4.out`; LePhare masses carry the +0.15 dex fluxscale correction; median logM\*: early 10.74, late 10.33).
The prompt's 203,633 figure is the v3 count. **Sensitivity to the version is nil:** a v3-like run (logM\*−0.15 dex,
M_gal rebuilt with the same Boselli f_cold relation) moves the u−r result 8.8σ → 8.7σ (robustness table).

## Chain and pinned relations (every relation carries an arXiv id)
Per lens: M\* (`logM`) → M_halo via SHMR → c via c(M,z) → r_s = r_Δ/c (proper, lens z, Brouwer cosmology h=0.7, Ωm=0.3).
Per g_bar bin b (the 15 released bin centres): the measurement radius is **R = √(G·M_gal/g_bar_b)** per lens (Brouwer's
estimator assigns each source g_bar = G·M_gal/R², so a g_bar bin probes R ∝ √M_gal), windowed to Brouwer's measured
range 0.03 < R < 3 h70⁻¹ Mpc; x = R/r_s; **C_bin^class = ⟨nfw_C(x)⟩** (the validated `esd_conversion.py` table:
point→π, SIS→4, NFW C(2)=4.000).

| ingredient | pinned | variants run |
|---|---|---|
| SHMR | **Moster, Naab & White 2013, arXiv:1205.5807** (Table 1, z-dependent; mass treated as M200c) | **Behroozi, Wechsler & Conroy 2013, arXiv:1207.6105** (Eqs. 3–4 intrinsic fit; M_vir, paired with cvir fits + Bryan–Norman Δvir for self-consistency) |
| type-dependent SHMR | off (type-blind) | **early halos ×2 (logM\*≤10.5) → ×3 (logM\*=11) at fixed M\*** — Mandelbaum+2016, arXiv:1509.06762 (SDSS lensing bimodality); direction independently banked via eROSITA eRASS Paper III (Zhang+2025, **arXiv:2411.19945**: L_X differential is halo-mass-driven) |
| c(M,z) | **Duffy+2008, arXiv:0804.2486** (Table 1 full, c200c = 5.71 (M/2e12 h⁻¹)^−0.084 (1+z)^−0.47) | **Dutton & Macciò 2014, arXiv:1402.7073** (Planck c200c); plus a **conc-tilt** variant: early types take Duffy's *relaxed* fit (6.71, −0.091, −0.44) — the assembly-bias direction (early-forming halos more concentrated at fixed M) |

Machinery validation: the per-bin σ machine reproduces `lr_battery.out` / `lr_sersic_crosscheck.out` **exactly**
(8.8σ/5.0σ u−r; 5.8σ/2.1σ Sérsic), and the χ² is **numerically invariant under any common per-bin factor** — only the
*differential* C_e/C_l can move the significance, so absolute-C model error (e.g. 2-halo terms at large R) cancels
to the extent it is type-shared.

## Finding 1 — the asserted erosion direction does NOT emerge (sign check)
The generic bracket's premise (x_early ≫ x_late at fixed R) implicitly held the halo fixed while moving R. The measured
populations do the opposite of what the bracket assumed, and the two effects nearly cancel:

- at fixed g_bar, early types are probed at **larger R**: R_e/R_l = √(M_gal,e/M_gal,l) = **1.52**;
- but their larger stellar masses put them in larger halos (M13×D08: med logM_h 12.36 vs 11.86; c 5.12 vs 5.65;
  r200 241 vs 167 kpc) whose scale radii are larger by **r_s,e/r_s,l = 1.62**;
- ⇒ x_e/x_l ≈ 0.94 ≈ 1: per-bin **Δlog C = log₁₀(C_e/C_l) runs −0.0002…+0.0030 dex, mean +0.0008** —
  *vs the bracket's asserted −0.089 dex* — and is **positive (split-strengthening) in 14/15 bins**.

Per-bin x distributions (primary config; 16/50/84th pct; full table in `.out`): x runs ~55 (lowest g_bar, R≈2.5 Mpc)
down to ~1.0 (highest g_bar, R≈0.04 Mpc) for **both** classes nearly identically; C runs 3.35→4.36 across bins for both.
The window trims the lowest bin to N_e=70,033 (massive early pushed past 3 Mpc) and the highest to N_l=50,097
(light late falling under 0.03 Mpc); all bins remain ≥50k per class.

## Finding 2 — refined surviving significance (the task's deliverable)

| SHMR | c(M,z) | type-dep M_h | conc-tilt | ⟨ΔlogC⟩ | u−r σ | Sérsic σ |
|---|---|---|---|---|---|---|
| M13 | D08 | – | – | +0.0008 | **8.8** | **5.8** |
| M13 | DM14 | – | – | +0.0009 | 8.8 | 5.8 |
| B13 | D08 | – | – | +0.0007 | 8.8 | 5.8 |
| B13 | DM14 | – | – | +0.0009 | 8.8 | 5.8 |
| M13 | D08 | ×2–3 (Mandelbaum16) | – | +0.0123 | **9.2** | **6.3** |
| B13 | DM14 | ×2–3 | – | +0.0111 | 9.2 | 6.3 |
| M13 | D08 | – | early=relaxed | −0.0039 | **8.6** | **5.6** |
| B13 | D08 | – | early=relaxed | −0.0038 | 8.6 | 5.6 |
| M13 | D08 | ×2–3 | early=relaxed | +0.0070 | 9.0 | 6.1 |

**Refined headline: the split survives the measured type-differential ESD→g_obs conversion at 8.6–9.2σ (u−r) and
5.6–6.3σ (Sérsic) across SHMR (M13/B13, ±type-dependence) × c(M,z) (D08/DM14, ±relaxed tilt) choices**
(baselines 8.8/5.8; the generic bracket had given 5.0/2.1).

Note the irony, reported at full weight both ways: the **type-dependent SHMR — the repo's own banked caveat
(quiescent galaxies occupy higher-mass halos at fixed M\*) — moves the split ABOVE baseline (9.2σ/6.3σ)**, because
heavier early-type halos have larger r_s, lower x, *larger* C_e. The only defensible knob that points in the erosion
direction at all is the assembly-bias concentration tilt, and at its published amplitude (~1.2×) it buys 0.2σ.

Robustness (primary config; u−r | Sérsic): median statistic 8.8|5.8; R² (source-count) weighting 8.8|5.9; no radial
window 8.8|5.8; composite C (halo + point-mass baryons, the more physical total-profile conversion) 8.7|5.7; global
M_h ×1.5 / ×0.67 (halo-definition ambiguity) 8.8|5.8 both; v3-like masses 8.7|5.7.

**Hostile probe** (how big an early-only concentration boost would soften the exposure?): u−r stays above 5σ even at
an indefensible **×6** boost (7.6σ); it never approaches 3σ. Sérsic crosses 5σ only at ×2.5 (published assembly-bias /
relaxed-fit amplitudes are ~1.1–1.3×; ≥×2 has no published support). The 3σ softening threshold named in the task is
**not reachable by any defensible variant on either axis.**

## VERDICT (both ways, full weight)
**The measured concentration differential erodes the split LESS than the generic bracket — by two orders of magnitude
in ΔlogC (≈0.001–0.012 dex vs 0.089 dex), and mostly with the OPPOSITE sign.** The previous "survives at 5.0σ (u−r) /
2.1σ (Sérsic)" numbers in `lr_battery_results.md` were **over-generous to the escape route** and are superseded:

> *the early/late lensing-RAR split survives the measured type-differential ESD→g_obs conversion at
> **8.6–9.2σ (u−r)** and **5.6–6.3σ (Sérsic)**, spread across SHMR (Moster13/Behroozi13, ± the eROSITA-banked
> type-dependent halo-mass offset) and c(M,z) (Duffy08/Dutton-Macciò14, ± relaxed-sample tilt) choices.*

- u−r never drops below ~8.6σ under any defensible variant — the exposure **HARDENS further** (it does not merely
  "survive at 5σ"; the conversion systematic essentially vanishes when measured).
- The Sérsic axis, previously the moderating "Outcome C (~2σ residual, conversion-limited)", is **no longer
  conversion-limited: 5.6–6.3σ** — the cross-check now *agrees* with the u−r axis instead of moderating it, removing
  the axis-dependence caveat from the battery verdict.
- Why the bracket failed: it transferred *galaxy light* concentration (Sérsic n) to the *halo* x = R/r_s while holding
  the halo fixed. In the measured populations the halo grows with the galaxy: r_s rises as fast as the probe radius
  R ∝ √M_gal, so the type-differential in x is ~6%, not the ×10 the bracket assumed.

## Caveats (recorded, none verdict-threatening)
1. **Sérsic-axis populations are proxied by the u−r classes** — the lens catalog carries no Sérsic index (GAP logged in
   `lr_esd_remeasure.py`). Defensible: both axes split the same parent sample ~50/50 and the proxies overlap heavily.
   For the *measured* mechanism to produce erosion on the Sérsic axis, high-n galaxies would have to be **less** massive
   than low-n at fixed selection — the reverse of every known morphology–mass correlation; the proxy if anything
   understates the strengthening (high-n classes likely have an even larger mass differential than the u−r classes).
2. **Pure-NFW C beyond r200** (x up to ~55 at the lowest bins): the released ESD there contains 2-halo contributions the
   one-halo C(x) ignores. This biases the *absolute* C (both classes 3.35 at low g_bar, vs Brouwer's uniform 4 — a
   common-mode ~−0.08 dex that would matter for any *absolute* use of the lensing RAR, e.g. an a₀ inference, flagged
   here as a side note) but cancels in the split statistic, which is proven numerically invariant to common per-bin
   factors; only a *type-differential* 2-halo term survives, and that is the satellite/environment axis (Axis 3),
   explicitly out of scope here.
3. **Halo-mass definition ambiguity** (M13's M200c vs B13's Mvir, relation cosmologies h=0.72/0.671 vs 0.7): probed by
   the global M_h ×1.5/×0.67 rows — no movement at 0.1σ resolution; x ∝ M_h^(~0.42)/√M_gal is too weak a lever.
4. **u−r threshold convention**: the catalog's split is at the LePhare bimodality valley u−r=2.0 (GAP-color logged),
   vs Brouwer's 2.5 in their colour system — a class-membership convention, not a free parameter; the released-profile
   validation in `lr_esd_remeasure.py` adjudicates it, and the C differential is driven by the ~0.4 dex mass offset
   between classes, which is robust to the exact valley cut.
5. This run refines the **conversion axis only**; the gas axis (eROSITA, disfavoured) and the locked wording
   ("exposure to property-independent modified gravity, NOT 'ΛCDM confirmed'") are unchanged from `lr_battery_results.md`.

**Bottom line for the falsification ledger:** the strongest standing exposure was given its most plausible remaining
escape valve at measured (not bracketed) amplitude, and the valve closed: **8.8σ → 8.6–9.2σ (u−r), 5.8 → 5.6–6.3σ
(Sérsic)**. The framework-unfavourable result is now harder than the battery left it, on both morphology axes.
