# FRONT [clusters] — galaxy-cluster a0 footing audit (independent re-confirm)

Auditor: opus_48, 2026-06-14. Framework a0 = (c/2)√(G ρ_DE) = c²√(Λ/32π) = **9.36e-11 m/s²** (pure dark energy).
Rule (both ways): a verdict computed at the WRONG a0 is invalid — retract a false-deficit (made framework look
worse) AND a false-win (made it look better). Data: real eRASS1 (Bulbul+2024), N=9830 clean clusters.

## Scripts inspected (all cluster scripts under real_research/)
| script | a0 used | footing | role |
|---|---|---|---|
| `real_research/reviews/clusters_eta_audit.py` | **9.36e-11** (A0_FRAME), 1.2e-10 shown as labeled rival | FRAMEWORK | independent eta audit — CLEAN |
| `real_research/clusters_framework_a0.py` | **9.36e-11** (A0_FRAME), 1.2e-10 labeled "RIVAL regular MOND" | FRAMEWORK | canonical front script — CLEAN |
| `real_research/predictions/door6_galaxy_clusters.py` | **1.2e-10** (`a0 = A0_RAR`, line 173) | **CANONICAL McGaugh** | **published prediction + figure — MIS-FOOTED** |
| `real_research/reviews/cluster_a0_from_density_HIS_FORMULA.py` | a0(cosmic)≈1.2e-10, in-cluster ~14× | env/density fork | exploratory, not an eta verdict — CLEAN(ish) |
| `real_research/reviews/project16_clusters.py` | rising a0(z)∝E(z), no numeric a0 | RIVAL rising branch | prose narrative, honest negative — superseded |
| `real_research/reviews/project_erass1_cluster_a0_fork.py` | 1.2e-10 (universal galaxy a0) | shared baseline | SHAPE/env fork; "cat iii, does not bear on a0~√ρ_Λ" — CLEAN |
| `real_research/reviews/project_cluster_a0z_xray.py` | 1.2e-10 + rising E(z) | RIVAL rising branch | forecast, methodological null — superseded |
| `real_research/reviews/project_cluster_erass1_a0z.py` | 1.2e-10 + rising E(z) | RIVAL rising branch | "R500 CANNOT test it" null — superseded |
| `real_research/reviews/project_cluster_evolving_a0.py` | 1.2e-10 + rising E(z) | RIVAL rising branch | honest WORSE verdict — superseded |
| `real_research/reviews/cluster_residual_evolution.py` | 1.2e-10 + rising E(z) | RIVAL rising branch | honest negative — superseded |

## THE ONE REAL FOOTING ERROR (a FALSE WIN — anti-framework correction)

`real_research/predictions/door6_galaxy_clusters.py` line 173:
```python
a0 = A0_RAR  # use the canonical RAR value for the central MOND prediction
```
with `A0_RAR = 1.2e-10` (line 156). The central published residual is therefore computed at the **canonical
McGaugh a0, not the framework's 9.36e-11**. This is the script that writes `figures/door6_galaxy_clusters.png`
and feeds the published paper.

Re-checked on the real eRASS1 sample (N=9830), simple-nu (door6's own interpolation):
| a0 footing | eta (median) |
|---|---|
| door6's a0 = 1.2e-10 (canonical) | **1.92** |
| FRAMEWORK a0 = 9.36e-11 | **2.15** |

Deep-MOND: eta ∝ 1/√a0, so the LOWER framework a0 gives the LARGER residual. door6 reports the **milder**
(1.92) number → the published liability is **understated by ~12%** relative to the framework's own footing.
Direction = **FALSE WIN** (the framework's hardest regime is reported as less-bad than its own a0 implies).

### Where it propagates into the paper (ZIMMERMAN_THEORY_OF_GRAVITY.md)
- **Scorecard row 17 (line 261): `η = 1.92 ± 0.20`** — this IS the door6 / 1.2e-10 number (the ±0.20 is door6's
  MC error budget). **WRONG FOOTING in the published scorecard.**
- BUT §10.1 (line 224) and falsifier C5 (line 296) correctly cite `clusters_framework_a0.py` and report the
  FRAMEWORK-footing numbers: **2.07 (regular MOND) → 2.33 (framework)**, "2.33× at R500." CORRECT FOOTING.

So the paper is internally **inconsistent on footing**: the prose/falsifier rows use the framework a0 (2.33),
the scorecard headline uses the canonical a0 (1.92). The 1.92 should be restated as ~2.15 (simple-nu) or
~2.33 (sqrt(g²+ga0) interp) at a0=9.36e-11. The correction makes the FAIL grade slightly worse, not better —
it is anti-framework, and required by the #1 rule exactly as a false-deficit would be.

### Reconciliation of the two interpolation conventions (both reproduced exactly)
| interp | regular MOND (1.2e-10) | framework (9.36e-11) |
|---|---|---|
| sqrt(g²+ga0) — `clusters_framework_a0.py` | 2.07 | **2.33** |
| simple-nu — `door6` | 1.92 | **2.15** |

In every convention the framework a0 → larger residual. There is NO interpolation choice at which 9.36e-11
beats 1.2e-10 on clusters. The deficit is real and robust; only its published *magnitude* was mis-footed low.

## The rival rising-a0(z)∝E(z) scripts — superseded? (both ways)
The four scripts `project_cluster_a0z_xray.py`, `project_cluster_erass1_a0z.py`, `project_cluster_evolving_a0.py`,
`cluster_residual_evolution.py` all use **1.2e-10 + the RISING law a0(z)∝E(z)** — i.e. BOTH the canonical a0
AND the wrong (matter-inclusive cH/Verlinde) branch. `clusters_framework_a0.py` (lines 6-7) explicitly names
all four as having "used the WRONG RISING law … AND the wrong a0=1.2e-10."

- **Mis-verdict risk: NONE.** Every one of these delivers an honest NEGATIVE or a methodological NULL
  ("WORSE", "cannot test", "cannot cure", "carries NO clean a0(z) signal"). None manufactures a win; none is a
  false deficit on the framework's *canonical* footing (they score the rival branch, which the framework no
  longer claims). So no eta mis-verdict propagates from them.
- **Provenance hazard (the "both ways" catch): YES, mild.** Their *self-headers* call the rising law
  "the framework's rising a0 = cH(z)/Z" / "this framework's DISTINCTIVE claim" — because when written, the
  rising branch was *believed* to be the framework's law. A reader opening any of them in isolation would
  think the rising-E(z) law IS the framework and would NOT see it flagged superseded unless they also read
  `clusters_framework_a0.py`. They are flagged superseded ONLY in the canon script's header, not in their own
  files. Recommendation (non-blocking, do not edit real_research/): add a one-line "SUPERSEDED: the framework
  law is the DECLINING √ρ_DE, not this rising E(z); see clusters_framework_a0.py" banner to each of the four.

## Verdict
- **door6_galaxy_clusters.py + paper scorecard row 17 (η=1.92±0.20): FALSE-WIN, mis-footed at canonical
  1.2e-10.** Re-state on the framework footing: η ≈ 2.15 (simple-nu) / 2.33 (sqrt interp) at a0=9.36e-11. The
  cluster FAIL is real and gets modestly WORSE under the correction (anti-framework). The paper's §10.1 / C5
  already carry the correct 2.33 — only the scorecard headline and the door6 central value lag.
- **clusters_framework_a0.py, clusters_eta_audit.py: CLEAN** (framework a0 throughout; 1.2e-10 only ever a
  labeled rival).
- **The four rising-a0(z) scripts: superseded rival branch, no mis-verdict** (honest negatives), but a mild
  provenance hazard — self-flagged only via the canon script, could mislead a reader in isolation.
