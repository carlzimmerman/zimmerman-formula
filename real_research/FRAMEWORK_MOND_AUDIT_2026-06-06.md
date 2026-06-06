# Framework-MOND audit: is every calculation done with *your* equation? — corpus sweep, 352 scripts

*C. Zimmerman, 2026-06-06. A comprehensive agent sweep (68 agents, 352 a₀-using scripts in `real_research/`) checking
that each calculation uses the framework's own equation — a₀ = c²√(Λ/32π) = 9.36×10⁻¹¹ (ρ_DE-footed, evolving as
√ρ_DE), Υ≈0.70 — and NOT regular MOND (1.2×10⁻¹⁰), the wrong footing (ρ_total/cH₀ → 1.13×10⁻¹⁰), or the wrong evolution
branch. Every RED was re-run with the framework equation on a /tmp copy to see if the verdict actually changes.*

## Top line
| class | N | meaning |
|---|---|---|
| **GREEN** | 229 | already the framework a₀, or result provably invariant to a₀ (ratios, signs, post-Υ scatter) |
| **YELLOW** | 56 | uses regular a₀ or the ρ_total footing, but the verdict is **degenerate** — relabel only, no number changes |
| **RED** | 31 | operative a₀/law wrong **and** the conclusion could move; **27 of 31 re-runs do move** |
| **GREY** | 36 | not a live a₀ calc (scaffold, doc generator, superseded) |

**The headline is not the RED count — it's the cause.** The a₀ *value* is sound across the corpus: 285/352 (81%) are
GREEN or YELLOW. **The real fault is the evolution law: 24 of the 27 material flips come from scripts running the *wrong
branch* of a₀(z).**

## Finding 1 — the footing flag (73 scripts) is mostly cosmetic, and it exposes a real fork
73 scripts compute a₀ from ρ_total / cH₀ (→ **1.13×10⁻¹⁰**, equivalently a₀ = cH₀/Z with the matter-inclusive H₀)
instead of ρ_DE / cH_Λ (→ **9.36×10⁻¹¹**). Most are **YELLOW**: their printed results are E(z) ratios in which the
footing (and Z) cancel, so the verdict is unchanged — only the printed *level/anchor* is off.

But the fork is real and worth stating straight: **the ρ_total value 1.13×10⁻¹⁰ actually fits the z=0 galaxy data
(RAR/BTFR/MDA ≈ 1.1×10⁻¹⁰) better than the canonical ρ_DE value 9.36×10⁻¹¹** (which is ~20% low). The reason to keep
the ρ_DE footing anyway is **evolution**: ρ_total-footing forces a₀(z) ∝ cH(z) (rising 3× by z=2), which is the
Verlinde-like branch that other tests disfavor; the ρ_DE footing gives the **declining** √ρ_DE law, which is viable and
distinctive. So the canon's ~20% z=0 deficit buys the *only viable, falsifiable* evolution. That trade is the real
content of the footing choice — not a bookkeeping detail.

## Finding 2 — the actual bug: the wrong a₀(z) branch (24/27 flips, 21 live scripts)
A large slice of the high-z corpus used **a₀(z) ∝ E(z) = √(Ω_m(1+z)³+Ω_Λ)** — the matter-inclusive, **rising** law
(3× by z=2, ~20× by z=10) — and *labeled it the framework*. The framework's actual law is **a₀(z) ∝ √ρ_DE(z)**, which
**declines** at high z (0.86× at z=2, 0.74× at z=3). These run in **opposite directions**. Re-running with the correct
declining law flips the conclusion in **21 live scripts**:

| script (live) | what the wrong rising law gave → corrected (declining √ρ_DE + a₀=9.36e-11) |
|---|---|
| `relativistic_frontier.py` | a₀ rises 3.03× by z=2 → **declines to 0.86×** (sign flip) |
| `reviews/a0_constant_vs_evolving_fork.py` | thesis *is* the evolution choice; baseline rising 3×/20× → declining |
| `reviews/project_cluster_a0z_xray.py` | assumed a₀ rises → **sign+verdict flip, spurious tension collapses** |
| `reviews/project_highz_bigwheel_a0.py` | "DISFAVORS" → **CONSISTENT** under the correct decline |
| `reviews/project08_a0_cosmography.py` | H₀ camp flips SH0ES/71.5 → **Planck/67.4** (correct footing) |
| `reviews/stress_test_geometric_origin.py` | **labels inverted** — called rising ρ_total "the framework", constant √Λ "Verlinde" |
| `reviews/jwst_rotation_predictions.py` | direction/sign flip; predicted v's ~6% lower |
| `reviews/jwst_predictions_comprehensive.py` | A₀=1.2e-10 + rising E(z) → 9.36e-11 + declining |
| `reviews/project_bigwheel_framework_prediction.py` | headline number moves ~9× (footing + wrong evolution) |
| `reviews/project_a0z_decisive_test.py` | absolute a₀_pred = A₀·E(1); % overshoot recomputes |
| `reviews/project10c_kross_real.py` | measured a₀ (data) unchanged; **target moves ~2×, verdict flips** |
| `reviews/project10d_gas_systematic.py` | numeric scaffold was regular-MOND + rising E(z); "inconclusive" prose survives |
| `reviews/project_musedark_shapefit.py` | shape test footing-invariant; normalization tiebreak flips |
| `reviews/project_manytemp_broadening.py` | "broadening lifts a₀ to framework ~1%" was mis-footed vs the wrong 1.13e-10 target |
| `reviews/project_literature_2026d.py` | substituted E(z) for √ρ_DE; anchor wrong |
| `reviews/project_Z_under_psr.py` | Z_obs 5.46 → 6.99 (28% shift) under the framework a₀ |
| `reviews/project17b_target_list.py` | headline qualifying target *count* changes |
| `reviews/a0_cH0_Z_check.py` | a₀ −22% to 9.36e-11; H₀-contingency narrative changes |
| `reviews/project_formula_offensive.py` | a₀ 1.2e-10 → 9.36e-11 |
| `mond_first_principles.py` | absolute BTFR/EFE levels move; evolution law was the wrong E(z) |
| `reviews/jwst_2025_data_confront.py` | body recomputes, but top-line ("M_dyn is an upper limit → uninformative") survives |

(6 more flips are in already-**superseded** scripts — noted, not load-bearing: `rar_evolution_test`, `project_a0z_muse_test`,
`project_literature_2026`, `provable_consequences_with_data`, `z3_a0_observing_proposal`, `z3_forecast_tightened`.)

**Both edges, stated honestly.** Fixing the branch *helps* the framework in several (spurious "tension"/"DISFAVORS"
become "CONSISTENT"; a bogus cluster-tension collapses) and *retracts* a few spurious wins (any script that "detected
a₀ rising with z" was on the rival branch and is withdrawn). The net is a **sharper** framework: its real prediction is
the **decline**, full stop.

## What is NOT broken
- The a₀ **value** and the RAR/BTFR/MDA fits: sound corpus-wide (the law-of-nature result stands; `framework_a0_law_of_nature.py`).
- The 229 GREEN + 56 YELLOW: the framework equation is used correctly, or the result is invariant to the value.
- The coefficient discussion (`bridge2_coefficient_thermodynamics.py` etc.): honestly labeled a posit already.

## The fix (in progress)
Every live a₀(z) prediction must be re-scored on the **one** correct law (declining √ρ_DE). That is exactly what the
clean **a₀(z) ledger** (offensive front 3) builds — a single confrontation of framework-decline vs constant vs
rising-cH vs regular-MOND across all repo high-z data — superseding the 21 flipped scripts in one place. The footing
relabel (1.13e-10 → 9.36e-11) is cosmetic for the YELLOWs and will be applied where a printed *level* matters.

*Sweep: 68 agents over 352 scripts; every RED re-run with the framework equation on isolated /tmp copies (repo never
modified). Digest: `/tmp/audit_digest.json`.*
