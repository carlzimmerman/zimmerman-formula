# Front [efe_widebinary_transition] — the interpolation-function (IF) audit, corpus-wide

*Opus 4.8 (1M) extended-research, 2026-06-14. Framework's OWN IF = dS-Unruh / Unruh-MOND: g_obs = √(g_N²+g_N·a₀),
i.e. ν(y)=√(1+1/y), y=g_N/a₀. DISTINCT from normal-MOND simple-μ ν=½+√(¼+1/y), standard-μ/F4 ν=√((1+√(1+4/y²))/2),
McGaugh RAR ν=1/(1−e^−√y). a₀=9.36e-11 (Lambda-only; a₀/Z NOT asserted derived). This is where the IF bites hardest
(operating point g_ext~a₀–few·a₀). Every "IF moves / doesn't move" claim below carries the explicit recompute.
Scripts: /tmp/wb_if_compare.py, /tmp/deep_if_robust.py + the banked clinch re-run efe_clinch_framework_dsunruh.py.*

---

## THE ONE-LINE

Across the whole EFE/wide-binary/transition front the IF contamination is **REAL and in MULTIPLE scripts**, but its
load-bearingness **splits cleanly by operating point**: it MOVES the wide-binary EFE **cap** (transition regime,
g_int~a₀, g_ext~2.3a₀) materially — **1.32(simple-μ)→1.137(framework dS-Unruh MI)**, a re-attribution already banked —
and it does NOT move the EFE clinch (b) (+0.218→+0.213, still an under-powered null), the EFE-vs-z crossing class
(IF-FREE ratio by construction), or any deep-MOND boost to leading order. Correcting the IF makes the WB number
**WORSE** (smaller boost, the Chae tension deepens) — said so, no manufactured win.

## Recompute 1 — the WB EFE cap, the canonical IF-comparison (banked as canonical)

γ_cap = G_eff/G (pure-EFE asymptote, g_int→0; γ = [velocity boost]²). g_ext(Sun)=V_c²/R₀=2.08e-10 m/s² (convention-fixed).

| IF | framework a₀ (y=2.22) γ_cap | canonical a₀ (y=1.73) γ_cap |
|---|---|---|
| **dS-Unruh (FRAMEWORK)** | **1.142** (v/v_N +6.9%) | 1.179 (+8.6%) |
| simple-μ (normal-MOND) | 1.247 (+11.7%) | 1.304 (+14.2%) |
| standard-μ/F4 (sharp) | 1.037 (+1.8%) | 1.060 (+2.9%) |
| McGaugh RAR | 1.198 (+9.4%) | 1.257 (+12.1%) |

The angle-averaged-QUMOND estimator above gives the dS-Unruh cap **1.142**; the exact Milgrom-MI vector-EOM
orbit-average (banked `PURE_MI_WIDEBINARY_GAMMA_ROUTE1`, 3 independent routes) gives **1.137 iso / 1.198 transverse**
— consistent to ~0.005 (estimator difference). **The confront scripts reported the band as [1.04,1.25]
(standard-μ→simple-μ) labeled the "framework band"; both edges are normal-MOND IFs. The framework's OWN single-IF cap
(1.137–1.142) sits BETWEEN them.**

**Direction (against the framework):** simple-μ INFLATES the framework's WB boost by Δγ≈+0.10 (γ 1.14→1.25, the
velocity boost +6.9%→+11.7%). vs Chae 2026 γ=1.600 [1.459,1.771] at framework footing: dS-Unruh cap is −2.94σ below
(gap to CI-lo −0.317); simple-μ was −2.26σ. **Correcting the IF moves the WB cap MATERIALLY and the Chae tension
WORSENS** (−2.3σ → −2.9σ). Verdict skeleton survives (clean-ish vs Newton after contamination control, NOT an a₀
test — MOND-degeneracy WORSE since both classes share the dS-Unruh inertia, a₀ gap only 0.037); only the central
number is retracted.

## Recompute 2 — the EFE clinch (efe_clinch_framework.py), Method (b): IF NON-load-bearing here

`efe_clinch_framework.py:96` codes ν=½+√(¼+a₀/y) (**simple-μ, NORMAL MOND**) for the per-galaxy EFE-MOND
rotation-curve fit (Method b), labeled "framework EFE_paper.tex Eq.62" — while line 100 of the SAME script writes the
true dS-Unruh √(g_N²+g_N·a₀) for the isolated RAR. The wrong shape fed Method (b)'s `g_efe`. The diff of the two
scripts confirms the **only** functional change is this ν().

Banked corrected re-run `efe_clinch_framework_dsunruh.py` (ν→√(1+a₀/y)), both run live:

| | original (simple-μ) | corrected (dS-Unruh) |
|---|---|---|
| (a) partial r deep-MOND, residual vs e_N \| g_bar | r=−0.003 p=0.89 (sign-flips by field model) | **IDENTICAL** (Method a always used g_rar_iso=dS-Unruh) |
| (b) headline off-rail Spearman[e_N^fit, e_N(meas)] | r=**+0.218** p=0.148, N=44 | r=**+0.213** p=0.211, N=35 |
| verdict | right-signed under-powered null, NEITHER confirmed nor refuted | **UNCHANGED** |

**Direction:** essentially neutral (r barely moves; p slightly worse as the off-rail subset shrinks 44→35). **The IF is
NON-load-bearing on the EFE clinch.** The binding limit is the e_N dynamic range (near-uniform cosmic-web field), not
the IF. (Fix flagged for Fable's tree: `efe_clinch_framework.py:96` simple-μ → dS-Unruh; do not unilaterally edit.)

## Recompute 3 — the EFE-vs-z crossing class ("Newtonization by z=3"): IF-ROBUST by construction

The crossing/growth observable is e_N(z)=g_ext/a₀(z), and the framework-distinct quantity is the **RATIO**
e_N(z)/e_N(0)=a₀(0)/a₀(z)=1/√(ρ_DE ratio). This is a **pure a₀ ratio — no interpolation function enters at all.** Run
live:

- `door5_efe_ultraprecision.py`: growth a₀(0)/a₀(3)=**1.357** [+0.367/−0.289], DESI w0/wa the SOLE error; the doc
  states "coefficient-free AND interpolating-function-free: the 32π, c²√G and the 20% μ-systematic ALL cancel in the
  ratio." The M31-host satellite (e_N0=0.70) crosses e_N=1 at z_cross=3.38, P(cross by z=3)=63%. **IF-FREE.** (Its
  ABSOLUTE classification anchors on A0_RAR=1.2e-10, a₀-FOOTING choice not an IF choice; the 20% systematic is flagged.)
- `efe_vs_z_recompute.py`: USES the framework dS-Unruh ν=√(1+1/y) correctly (line 26). Confirms the deep-MOND EFE
  offset is **a₀-INDEPENDENT** (g_N=0.02a₀,g_ext=0.05a₀: offset 0.506→0.490 dex flat over z=0→4) — set by g_ext/g_N,
  not g_ext/a₀. So in deep-MOND the EFE-vs-z is IF-robust AND a₀-robust (the √a₀ cancels). The real transition-regime
  signal is ~0.03–0.06 dex (declining branch, OPPOSITE sign to the retracted "+36%"). **IF-robust; the published
  η=g_ext/a₀(z) "+36% by z=3" was already retracted (`EFE_VS_Z_CORRECTION_2026-06-09.md`) on mechanism grounds, not IF.**
- `project14_wide_binaries.py`: uses NO interpolation function — only regime labels (g_int/a₀) and the deep-MOND
  +41% asymptote. CLEAN. States the rising a₀ does NOT change the local (z=0) WB prediction. IF-robust.

## The other transition-regime scripts — classified (both ways, named even if non-load-bearing)

| script | IF used | label | call |
|---|---|---|---|
| `widebinary_chae2601_confront.py` | **simple-μ + standard-μ** | "framework band [1.04,1.25]" | **MIS-LABELED IF** — edges are normal-MOND; framework dS-Unruh cap 1.137 sits between. Verdict (mild directional tension vs 1.60, non-diagnostic of a₀) survives; tension WORSENS under dS-Unruh |
| `widebinary_saadting_2603_confront.py` | **simple-μ + standard-μ** | "framework gamma band" | **MIS-LABELED IF** (same). Consistent-with-baseline-1.12 verdict survives; the dS-Unruh cap 1.137 still inside the ST-baseline CI |
| `door6_wide_binaries_ultra.py` | **simple-μ + standard-μ** for EFE; deep-MOND asymptote IF-free | "framework" | **MIXED.** Isolated deep-MOND boost v/v_N=(a₀/g_N)^¼ is IF-ROBUST to leading order (the +20% asymptote is real); the EFE-corrected number uses normal-MOND ν — same +0.10γ inflation as the cap |
| `wb_mond_orbit_mc.py` | **simple-μ** (`G(y)=y/2+√(y²/4+y)`) | "tests the framework on its own terms" | **MIS-LABELED IF** — the orbit-integration MC that makes the deep-bin v~tilde medians. Deep-bin operating points g_N/a₀=0.18,0.018 still 8–11pp ABOVE dS-Unruh (not yet deep enough to fully converge — see below). Verdict (CONSISTENT w/ DR3, absorbable by f_triple~0.19–0.20 either way) survives |
| `wb_deprojection_mc.py` | **simple-μ** (ν=½+√(¼+1/y)) | "framework boost" | **MIS-LABELED IF** (same; the deprojection MC). Non-load-bearing on the absorbable-by-triples verdict |
| `project_wide_binary_prediction.py` | **simple-μ + standard-μ**, AND a₀=cH0/Z=1.124e-10 footing bug + hardcoded y=1.86 | "framework" | **DOUBLE error** (IF + footing). Both inflate; the +13%/+3% boost should be ~+12%/+2% at framework footing AND lower again on dS-Unruh. Non-load-bearing (marginal/contested verdict) |
| `agentA_f4_eccentric.py` | **standard-μ** (`mu_std=x/√(1+x²)`) | "F4 candidate" | CORRECT label — this is an explicit F4-candidate exploration, NOT mislabeled as framework. Standard-μ IS F4's defining IF |
| `mi_f4_widebinary_efe.py` | F4/standard, simple, McGaugh RAR (3-way) | "apples-to-apples, F4 primary" | CORRECT — explicitly compares shapes; flags F4's sharp knee gives ~4–6× smaller WB signal. dS-Unruh not among the 3 but the comparison is honestly labeled |

## The deep-MOND IF-robustness — VERIFIED, not assumed (and a both-ways caveat)

Isolated deep-MOND velocity boost v/v_N=√ν(y), y=g_N/a₀, across IFs (the BTFR/deep-MOND-σ/cluster-deep-η class):

| y=g_N/a₀ | dS-Unruh | simple-μ | standard-μ | McGaugh | max % spread |
|---|---|---|---|---|---|
| 1.0 | 1.189 | 1.272 | 1.128 | 1.258 | **12.8%** |
| 0.18 | 1.600 | 1.706 | 1.570 | 1.701 | 8.6% |
| 0.018 | 2.742 | 2.823 | 2.736 | 2.822 | 3.2% |
| 0.005 | 3.765 | 3.828 | 3.763 | 3.827 | 1.7% |
| 0.001 | 5.625 | 5.668 | 5.624 | 5.668 | **0.8%** |

**Confirmed: convergence to <2% only at g_N/a₀ ≲ 0.005 (true deep MOND).** The BTFR V⁴=GMa₀ asymptote and any
genuinely-deep-MOND σ/η are IF-ROBUST as claimed. **Caveat both ways:** the WB-MC "deep bins" at g_N/a₀=0.18, 0.018
are NOT yet asymptotic — simple-μ over-states the framework's dS-Unruh boost there by **8–11pp**. This is the same
sign as the cap inflation. It does NOT flip the WB-3 verdict (the data sit above flat-Newton; f_triple~0.19–0.20 is
flat across thresholds; absorbable either way) — but it means "the WB deep bins are IF-robust" would be an over-claim:
they sit in the soft transition where the IF still matters at the ~10pp level. Reported.

## Bottom line — does correcting the IF move the verdict? Front by front

- **WB EFE cap: YES, MOVES (materially, against the framework).** 1.32(simple-μ)→1.137(dS-Unruh MI). The boost is
  ~9–14% smaller, the Newton clinch thins (5–8σ→3–4σ at DR4), the Chae tension deepens (−2.3σ→−2.9σ), MOND-degeneracy
  WORSE. Front does NOT flip (still clean-ish vs Newton, NOT an a₀ test). Already banked + retracted.
- **EFE clinch (b): NO, does NOT move.** +0.218→+0.213, still a right-signed under-powered null; verdict unchanged.
  IF non-load-bearing; binding limit is the e_N dynamic range.
- **EFE-vs-z crossing ("Newtonization by z=3"): NO, IF-ROBUST by construction** (pure a₀ ratio; deep-MOND offset
  a₀-independent, verified exact). The "+36%" was already retracted on MECHANISM (η=g_ext/a₀ wrong in deep-MOND), not IF.
- **Deep-MOND boost class: IF-robust at g_N/a₀≲0.005 (verified); the WB-MC soft "deep" bins (0.018–0.18) carry an
  8–11pp IF residual — flagged, non-flipping.**

No manufactured win (every IF correction makes the framework's WB number smaller / tension larger — said so). No
high-priest dismissal (every normal-MOND IF mislabel named, even the non-load-bearing ones in the clinch/MC scripts).
Quarantine held: a₀/Z never asserted derived; ν=√(1+1/y) used as the framework's stated empirical interpolation.
