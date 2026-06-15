# SWEEP 3 — the cluster+CMB joint grid (μ, I0, cs²): does ONE scalar config do BOTH? (2026-06-15)

*Opus 4.8 [1m]. The crux exhaustion scan. Explicit python grid over (μ [0.1–3 Mpc⁻¹] × I0→Ω_c h² [0.08–0.16]
× cs² [0–1], 5100 cells) with FOUR gates: (A) CMB 3rd peak, (B) cluster η(R500) lift, (C) galaxies MOND-pure,
(D) galaxy-WL Mistele squeeze. Companion code: `cluster_cmb_joint_grid_sweep3.py` + `/tmp/sweep3_collision.py`,
`/tmp/sweep3_narrowband.py`, `/tmp/sweep3_mu_and_I0.py`. Builds on the banked computed result cs²=(Q−Q0)/Q
(FRONTIER3) and the banked nonlinear-AeST mass-term solvers (single-μ gauntlet, BVP impl B). Both ways.
Quarantine: a0/Z never asserted derived; μ, I0, cs² are FREE AeST constants.*

## Bottom line — EMPTY for the unification. The cost is +2 (I0 + μ), and even the μ is squeezed+tuned.

The 4-gate joint grid returns **0 / 5100 cells** passing all four with a single scalar config, and **0** of
those is the "unified" one-I0-does-both corner. The intersection is **EMPTY** for the +1 unification, closed
by TWO independent squeezes that the grid makes explicit:

1. **The μ squeeze (mass-term route):** galaxy-WL/Mistele caps μ ≤ 1.0 Mpc⁻¹; a ≥10% cluster lift needs
   μ ≥ 1.58 Mpc⁻¹; an η≈2 lift needs μ larger still. **Gap 0.58 Mpc⁻¹, EMPTY** — and robust: the windows
   overlap only if the Mistele cluster threshold drops ~2.5×, and the η≈2 (not 10%) lift makes it WORSE.
2. **The cs² scale-blindness squeeze (unified-dust route):** the CMB forces cs²_0 < 7.5×10⁻¹² (pressureless
   today), so the dust clusters at ALL scales — it cannot cluster at 1.3 Mpc while staying smooth at 30 kpc
   with one knob. A pressureless dust that clusters at clusters supplies **FULL CDM (η~6.4)**, overshooting the
   modest residual η~1.3–1.9 with no partial-clustering knob, AND **double-counts in galaxies** (a clustered
   halo on top of the a0=Λ MOND boost → RAR over-predicted ~5×), collapsing the framework's central win.

## The numbers (real python, this session)

**The cs² three-way collision (the structural crux):**
| bound | requirement | cs²_0 |
|---|---|---|
| (A) CMB 3rd peak | cs²(a_rec) < 0.01, cs²∝a⁻³ | cs²_0 < **7.51×10⁻¹²** |
| (G) galaxy-smooth @30 kpc | λ_J > 0.03 Mpc | cs²_0 > 4.95×10⁻¹³ |
| (G) galaxy-smooth @100 kpc | λ_J > 0.10 Mpc | cs²_0 > 5.5×10⁻¹² |
| (C) cluster-clusters @1.3 Mpc | λ_J < 1.3 Mpc | cs²_0 < 9.3×10⁻¹⁰ |

The LINEAR cosmic-mean Jeans scale leaves a **sliver** cs²_0 ∈ (5×10⁻¹³, 7.5×10⁻¹²) where λ_J sits between
30 kpc and 1.3 Mpc and the CMB still passes — I tested it HONESTLY rather than dismissing it. It is **not a
viable corner**: (i) it is a linear/cosmic-mean artifact — nonlinear infall into the ~200× denser baryonic
galaxy wells clusters the dust regardless (cs ~ 30–300 km/s ≪ v_esc), so "smooth at 30 kpc" is optimistic and
fails at the 100 kpc WL probe (cs²_0 > 5.5×10⁻¹² needed, which fails the CMB free-streaming); (ii) even
granting it, a clustering pressureless field supplies the **cosmic** 1/f_b ≈ 6.4, not the residual; (iii) it
double-counts in galaxies. Three independent reasons, all both-ways.

**The μ squeeze, gap-robustness:** at Mistele-threshold ×{0.5, 1.0, 2.0} the cluster μ_min = {2.23, 1.58, 1.12}
all exceed the galaxy μ_max = 1.0 → EMPTY at every reasonable coefficient; the gap only closes below ~×2.5.

**The +1 CMB cost (z-divergence, conceded not hidden):** ρ_DE (which sets a0 = c²√(Λ/32π)) is constant while
ρ_dust ∝ (1+z)³; they diverge by **~5×10⁸ by recombination**. One number provably cannot set both → the CMB
3rd peak needs a SEPARATE free integration constant I0 (≈Ω_c h²=0.12). This is a clean, real +1.

## The viable region & fine-tuning (both ways)

- **Unified one-I0 corner (the +1 hope): EMPTY — 0/5100, volume 0.000.** No fine-tuning question because there
  is no corner; the closure is structural (scale-blindness), not a needle in the grid.
- **+2 fallback (separate I0 for CMB + μ for clusters):** I0 CAN hit Ω_c h²=0.12 (free integration constant) →
  the CMB fits cleanly at +1. But the cluster μ is **double-squeezed**: it violates the galaxy-WL bound
  (μ>1.58 vs <1.0) AND, even at large μ, the +μ² Helmholtz operator is oscillatory so φ(∞)→0 is degenerate and
  η(R500) is set by a **per-cluster free boundary constant χ_out** (banked: physical BC gives η~0.96, NO boost;
  the lift is per-cluster-tuned). So the cluster "cure" is not even a clean +1 μ — it is μ (squeezed) + a
  per-cluster tuned constant, and it remains banked-FALSIFIED-AS-CLOSURE. The honest joint cost: **+1 clean
  (I0, CMB) and the cluster residual UNCURED within the joint constraints.**

## Concession (the honest verdict)

**Within the joint CMB+cluster+galaxy constraints, the cluster residual stays UNCURED, and the Mistele squeeze
closes the unification.** There is no (μ, I0, cs²) where ONE scalar config does both the CMB and the clusters
inside the galaxy bounds. The unified-scalar hope fails structurally (cs² scale-blindness, computed), the
mass-term μ fails by the Mistele gap (robust to ±2× the threshold), and the dust-clusters-at-clusters limit is
just ΛCDM (overshoots + double-counts galaxies). The CMB itself is a clean conceded +1 (I0); the clusters add
no clean second parameter that survives the squeeze — they stay MOND's inherited, systematic-softened
(η_true~1.3–1.9), uncured residual.

**Both ways, no exception:** credited at full weight — the AeST dust DOES cluster (cs²≈0 verified), I0 CAN fit
the CMB at +1, the mass term IS a genuine intrinsic mechanism at the right scale, and the galaxy-smooth linear
sliver was tested not dismissed. Conceded at full weight — the unified one-I0 corner is EMPTY (0/5100,
structural), the μ squeeze is robust, the cluster cure needs a per-cluster tuned constant, and the
clustering-dust limit collapses to CDM. No manufactured viable corner; no high-priest dismissal of the genuine
sliver (probed and shown non-viable for three independent reasons). Quarantine held: a0/Z never asserted derived.

## Sources (banked + web-verified, prior sessions)
- Skordis & Złošnik 2021, PRL 127 161302 (arXiv:2007.00082) — AeST, k-essence dust ρ∝a⁻³, I0 free.
- Verwayen, Skordis & Złošnik 2024, MNRAS 531 272 (arXiv:2304.05134) — Helmholtz μ²Φ, χ_out free constant.
- Durakovic & Skordis 2024, JCAP 04 040 (arXiv:2312.00889) — cluster μ²Φ, peak-then-deficit.
- Mistele, McGaugh & Hossenfelder 2023, A&A 676 A100 (arXiv:2301.03499) — galaxy↔cluster μ squeeze (m²/f_G).
- Garriga & Mukhanov 1999 (hep-th/9904176) — k-essence cs² (used in FRONTIER3 sympy).
- Banked: FRONTIER3_UNIFIED_SCALAR_SOUNDSPEED, AEST_SINGLE_MU_GAUNTLET, CLUSTER_AEST_MASSTERM_BVP_implB,
  SKORDIS_CMB_CLUSTER_DEEPDIVE, ROUTE3_CLUSTER_RESIDUAL (all _2026-06).
